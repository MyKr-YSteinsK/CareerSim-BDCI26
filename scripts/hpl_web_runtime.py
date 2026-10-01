"""Rebuild and verify the isolated signed-Python, no-native-msgpack runtime."""

import argparse
import hashlib
import importlib.metadata as metadata
import json
import platform
import shutil
import sys
import tempfile
import venv
from pathlib import Path

WORKTREE = Path(__file__).resolve().parents[1]
if str(WORKTREE) not in sys.path:
    sys.path.insert(0, str(WORKTREE))

from scripts.hpl_play import resolve_layout  # noqa: E402
from scripts.hpl_preflight import verify_dataset_mirror, verify_distribution_dataset  # noqa: E402

BASE_DLL_SHA256 = "9a0e3435aaa680d868150f87ab3e388ad2eebc22f87e036155c7b4eda8cd2120"
BASE_EXE_SHA256 = "4d6f5f81a4bca11191c4c7c6b43632694d0a4ce74e068619d8fdc161d469859a"


def runtime_root():
    return resolve_layout().sandbox_root / "local-web-client"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def reject_links(path):
    for entry in (path, *path.parents):
        if entry.is_symlink() or getattr(entry, "is_junction", lambda: False)():
            raise RuntimeError("HPL Web paths cannot traverse links")


def writable(path):
    reject_links(path)
    path.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryFile(dir=path) as stream:
        stream.write(b"HPL writable check")
        stream.flush()


def build_runtime():
    """Copy pinned local RECORD-verified inputs; never update the parent evidence."""
    sandbox = resolve_layout().sandbox_root
    root = runtime_root()
    base = sandbox / "packaging-python" / "cpython-3.12.10"
    if Path(sys.executable).resolve() != (base / "python.exe").resolve():
        raise RuntimeError("Build requires the accepted official CPython base interpreter")
    if digest(base / "python.exe") != BASE_EXE_SHA256 or digest(base / "python312.dll") != BASE_DLL_SHA256:
        raise RuntimeError("Signed CPython identity drift")
    if root.exists():
        raise RuntimeError("Runtime already exists; inspect it rather than overwrite")
    reject_links(root)
    root.mkdir(parents=True)
    venv.EnvBuilder(with_pip=True).create(root / "venv")
    source_root = sandbox / "msgpack-probe"
    identities = json.loads((source_root / "copy-identity.json").read_text(encoding="utf-8"))
    source = source_root / "venv" / "Lib" / "site-packages"
    target = root / "venv" / "Lib" / "site-packages"
    files = {}
    for distribution in identities:
        for item in distribution["files"]:
            relative = Path(item["path"])
            if relative.is_absolute() or ".." in relative.parts or relative.suffix in (".pyd", ".dll", ".exe"):
                raise RuntimeError("Unexpected source dependency path/native binary")
            src, dst = source / relative, target / relative
            reject_links(src)
            if digest(src) != item["sha256"]:
                raise RuntimeError("HPL-04C source identity drift")
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src, dst)
            files[dst.relative_to(root).as_posix()] = digest(dst)
    dev = target / "career_emulator_bdci26" / "dev" / "dataset"
    mirror = target / "career_emulator" / "data" / "dataset"
    shutil.copytree(dev, mirror)
    for file in mirror.rglob("*"):
        if file.is_file():
            files[file.relative_to(root).as_posix()] = digest(file)
    identity = {
        "schema": "hpl-web-runtime/v1",
        "base": str(base),
        "python": "3.12.10",
        "packages": {d["name"]: d["version"] for d in identities},
        "source_wheels": {d["name"]: d["source"] for d in identities},
        "files": files,
        "dataset": verify_dataset_mirror(dev, mirror),
        "omission": "msgpack/_cmsgpack.cp312-win_amd64.pyd",
    }
    (root / "identity.json").write_text(json.dumps(identity, indent=2), encoding="utf-8")
    print("HPL Web runtime built; no source patch, no download, complete Dev mirror")


def startup_check():
    root = runtime_root()
    reject_links(root)
    if Path(sys.prefix).resolve() != (root / "venv").resolve() or platform.python_version() != "3.12.10":
        raise RuntimeError("Use the dedicated HPL-05 official CPython 3.12.10 runtime")
    identity = json.loads((root / "identity.json").read_text(encoding="utf-8"))
    base = resolve_layout().sandbox_root / "packaging-python" / "cpython-3.12.10"
    if Path(sys.base_prefix).resolve() != base.resolve():
        raise RuntimeError("Unexpected base interpreter")
    if digest(base / "python.exe") != BASE_EXE_SHA256 or digest(base / "python312.dll") != BASE_DLL_SHA256:
        raise RuntimeError("Signed CPython identity drift")
    installed = {d.metadata["Name"].lower().replace("_", "-"): d.version for d in metadata.distributions()}
    expected = {name.lower().replace("_", "-"): version for name, version in identity["packages"].items()}
    pins = {"career-emulator": "1.0.1", "career-emulator-bdci26": "1.0.0", "msgpack": "1.2.3"}
    if any(expected.get(name) != version for name, version in pins.items()):
        raise RuntimeError("Frozen HPL Web package identity drift")
    if installed != {**expected, "pip": "25.0.1"}:
        raise RuntimeError("HPL Web dependency closure drift")
    for relative, expected_hash in identity["files"].items():
        path = root / relative
        reject_links(path)
        if not path.resolve().is_relative_to(root.resolve()) or digest(path) != expected_hash:
            raise RuntimeError("HPL Web package/data identity drift")
    site = root / "venv" / "Lib" / "site-packages"
    if list(site.rglob("*.pyd")) or list(site.rglob("*.dll")):
        raise RuntimeError("Unexpected native dependency in HPL Web environment")
    import msgpack

    if msgpack.Packer.__module__ != "msgpack.fallback" or hasattr(msgpack, "_cmsgpack"):
        raise RuntimeError("HPL Web requires msgpack.fallback")
    dev = site / "career_emulator_bdci26" / "dev" / "dataset"
    verify_distribution_dataset(dev)
    if verify_dataset_mirror(dev, site / "career_emulator" / "data" / "dataset") != identity["dataset"]:
        raise RuntimeError("Complete Dev mirror drift")
    writable(root)
    writable(resolve_layout().runs_root)
    writable(root / "fixtures")
    return identity


def loaded_native_modules():
    """Read-only Windows module inspection for the fixture startup gate."""
    import ctypes
    from ctypes import wintypes

    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    psapi = ctypes.WinDLL("psapi", use_last_error=True)
    kernel.GetCurrentProcess.restype = wintypes.HANDLE
    psapi.EnumProcessModules.argtypes = [
        wintypes.HANDLE,
        ctypes.POINTER(wintypes.HMODULE),
        wintypes.DWORD,
        ctypes.POINTER(wintypes.DWORD),
    ]
    psapi.GetModuleFileNameExW.argtypes = [wintypes.HANDLE, wintypes.HMODULE, wintypes.LPWSTR, wintypes.DWORD]
    modules = (wintypes.HMODULE * 2048)()
    needed = wintypes.DWORD()
    handle = kernel.GetCurrentProcess()
    if not psapi.EnumProcessModules(handle, modules, ctypes.sizeof(modules), ctypes.byref(needed)):
        raise RuntimeError("Cannot inventory native modules")
    if needed.value > ctypes.sizeof(modules):
        raise RuntimeError("Native module inventory buffer too small")
    paths = []
    for index in range(needed.value // ctypes.sizeof(wintypes.HMODULE)):
        buffer = ctypes.create_unicode_buffer(32768)
        if not psapi.GetModuleFileNameExW(handle, modules[index], buffer, len(buffer)):
            raise RuntimeError("Cannot resolve loaded native module")
        paths.append(buffer.value)
    return sorted(set(paths))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--build", action="store_true")
    args = parser.parse_args()
    if args.build:
        build_runtime()
    else:
        print(json.dumps(startup_check(), indent=2))
