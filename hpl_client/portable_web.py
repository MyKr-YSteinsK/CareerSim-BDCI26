"""Relocatable local Web entry; imports no repository or development environment."""

import argparse
import hashlib
import importlib.metadata as metadata
import json
import os
import platform
import sys
import uuid
import webbrowser
from dataclasses import dataclass
from pathlib import Path

from hpl_client.controller import HumanGameController
from hpl_client.game_adapter import PublicGameAdapter
from hpl_client.path_contract import DATASET_PATHS, REQUIRED_DATASET_RESOURCES, assert_isolated_run_root
from hpl_client.recorder import RunRecorder
from hpl_client.web import EndingFixtureEngine, LocalWebServer, WebApplication, manifest


@dataclass(frozen=True)
class PortableLayout:
    application_root: Path
    mode: str = "WEB_PORTABLE"

    @property
    def workspace_root(self):
        return self.application_root

    @property
    def sandbox_root(self):
        return self.application_root / "UserData"

    @property
    def runs_root(self):
        return self.sandbox_root / "Runs"

    @property
    def exports_root(self):
        return self.sandbox_root / "Exports"

    @property
    def diagnostics_root(self):
        return self.sandbox_root / "Diagnostics"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def reject_links(path):
    if any(p.is_symlink() or getattr(p, "is_junction", lambda: False)() for p in (path, *path.parents)):
        raise RuntimeError("Portable paths cannot traverse links")


def writable(path):
    reject_links(path)
    path.mkdir(parents=True, exist_ok=True)
    probe = path / (".write-probe-" + uuid.uuid4().hex)
    try:
        with probe.open("xb") as stream:
            stream.write(b"HPL")
    finally:
        probe.unlink(missing_ok=True)


def startup_check(root):
    root = root.resolve()
    reject_links(root)
    runtime = root / "Runtime"
    if Path(sys.executable).resolve() != runtime / "python.exe" or platform.python_version() != "3.12.10":
        raise RuntimeError("Use only the bundled official Python 3.12.10")
    if sys.prefix != sys.base_prefix or not sys.flags.isolated:
        raise RuntimeError("Portable runtime isolation is unavailable")
    identity = json.loads((root / "App" / "package-manifest.json").read_text(encoding="utf-8"))
    actual_files = {
        p.relative_to(root).as_posix()
        for top in ("Runtime", "App")
        for p in (root / top).rglob("*")
        if p.is_file() and p != root / "App" / "package-manifest.json"
    }
    actual_files.update({"启动 CareerSim.cmd", "README-使用说明.txt"})
    if actual_files != set(identity["files"]):
        raise RuntimeError("Portable file inventory mismatch")
    for relative, expected in identity["files"].items():
        path = root / relative
        reject_links(path)
        if not path.resolve().is_relative_to(root) or digest(path) != expected:
            raise RuntimeError("Portable integrity mismatch: " + relative)
    packages = {d.metadata["Name"].lower().replace("_", "-"): d.version for d in metadata.distributions()}
    expected = {k.lower().replace("_", "-"): v for k, v in identity["packages"].items()}
    pins = {"career-emulator": "1.0.1", "career-emulator-bdci26": "1.0.0", "msgpack": "1.2.3"}
    if any(expected.get(name) != version for name, version in pins.items()):
        raise RuntimeError("Portable frozen package versions mismatch")
    if packages != expected:
        raise RuntimeError("Portable dependency identity mismatch")
    import msgpack

    if any(obj.__module__ != "msgpack.fallback" for obj in (msgpack.Packer, msgpack.Unpacker, msgpack.unpackb)):
        raise RuntimeError("Portable msgpack fallback is required")
    if list((runtime / "Lib/site-packages").rglob("*.pyd")):
        raise RuntimeError("Unexpected native Python dependency")
    dataset = runtime / "Lib/site-packages/career_emulator/data/dataset"
    dataset_files = {p.relative_to(dataset).as_posix(): digest(p) for p in dataset.rglob("*") if p.is_file()}
    if len(dataset_files) != 194 or dataset_files != identity["dataset_files"]:
        raise RuntimeError("Portable complete Dev dataset identity mismatch")
    if any(not (dataset / relative).is_file() for relative in REQUIRED_DATASET_RESOURCES):
        raise RuntimeError("Portable default dataset resources are missing")
    for path in sys.path:
        if not Path(path).resolve().is_relative_to(root):
            raise RuntimeError("External Python search path")
    layout = PortableLayout(root)
    try:
        for path in (root, layout.sandbox_root, layout.runs_root, layout.exports_root, layout.diagnostics_root):
            writable(path)
    except OSError as error:
        raise RuntimeError("请完整解压并把文件夹移动到桌面、D 盘或其他普通可写目录后重试。") from error
    return layout, identity, dataset


def create_controller(layout, identity, dataset, *, fixture=False):
    def factory(tag):
        # Called only on user Start. Server/startup checks never construct a game.
        identifier = uuid.uuid4().hex
        root = layout.runs_root / identifier
        assert_isolated_run_root(root, layout)
        root.mkdir(exist_ok=False)
        logs = root / "runtime/logs"
        logs.mkdir(parents=True)
        db = root / "runtime/career_emulator.sqlite3"
        fields = manifest(tag, identifier, fixture)
        fields.update(
            hpl_commit=identity["source_commit"],
            launcher_version="hpl-06/fixture-non-game" if fixture else "hpl-06/portable-web",
            hpl_venv_root="PORTABLE_EMBEDDED_PYTHON",
            hpl_runtime_root="UserData/Runs/" + identifier,
            dataset_root="career_emulator/data/dataset",
        )
        recorder = RunRecorder(root, fields, diagnostics_root=layout.diagnostics_root)
        try:
            if fixture:
                engine = EndingFixtureEngine(energy=2)
            else:
                os.environ["CAREER_EMULATOR_DB"] = str(db)
                os.environ["CAREER_EMULATOR_LOG_DIR"] = str(logs)
                from career_emulator.game import GameEngine

                engine = GameEngine(db_path=db, **{key: dataset / value for key, value in DATASET_PATHS.items()})
                engine.store.log_dir = logs
        except Exception as error:
            recorder.failure(error)
            raise
        return PublicGameAdapter(engine, identifier), recorder

    return HumanGameController(factory, layout=layout)


def runtime_observation(root):
    from ctypes import WinDLL, byref, create_unicode_buffer, sizeof
    from ctypes import wintypes

    kernel, psapi = WinDLL("kernel32"), WinDLL("psapi")
    kernel.GetCurrentProcess.restype = wintypes.HANDLE
    psapi.EnumProcessModules.argtypes = [wintypes.HANDLE, wintypes.HMODULE * 2048, wintypes.DWORD, wintypes.LPDWORD]
    psapi.GetModuleFileNameExW.argtypes = [wintypes.HANDLE, wintypes.HMODULE, wintypes.LPWSTR, wintypes.DWORD]
    modules, needed = (wintypes.HMODULE * 2048)(), wintypes.DWORD()
    handle = kernel.GetCurrentProcess()
    if not psapi.EnumProcessModules(handle, modules, sizeof(modules), byref(needed)) or needed.value > sizeof(modules):
        raise RuntimeError("Native module inventory unavailable")
    native = []
    for module in modules[: needed.value // sizeof(wintypes.HMODULE)]:
        buffer = create_unicode_buffer(32768)
        if not psapi.GetModuleFileNameExW(handle, module, buffer, len(buffer)):
            raise RuntimeError("Native module path unavailable")
        native.append(buffer.value)
    origins = sorted({getattr(m, "__file__", "") for m in sys.modules.values() if getattr(m, "__file__", "")})
    if any(not Path(p).resolve().is_relative_to(root) for p in origins):
        raise RuntimeError("Imported module outside the extracted package")
    return {"executable": sys.executable, "sys_path": sys.path, "import_origins": origins, "native": native}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture", action="store_true")
    parser.add_argument("--no-browser", action="store_true")
    parser.add_argument("--self-check", action="store_true")
    parser.add_argument("--ready-file", type=Path)
    args = parser.parse_args()
    server = app = None
    root = Path(__file__).resolve().parents[2]
    try:
        layout, identity, dataset = startup_check(root)
        if args.self_check:
            print("Portable runtime/data/UserData integrity PASS")
            return 0
        # Route package import-time defaults to package-local diagnostics before import.
        os.environ["CAREER_EMULATOR_DB"] = str(layout.diagnostics_root / "unused-startup.sqlite3")
        os.environ["CAREER_EMULATOR_LOG_DIR"] = str(layout.diagnostics_root)
        if args.fixture:

            def offline(event, values):
                if event == "socket.connect" and values[1][0] != "127.0.0.1":
                    raise RuntimeError("Fixture forbids external network")

            sys.addaudithook(offline)
        from career_emulator.game import GameEngine  # noqa: F401

        app = WebApplication(create_controller(layout, identity, dataset, fixture=args.fixture), fixture=args.fixture)
        server = LocalWebServer(app)
        if args.ready_file:
            path = args.ready_file.resolve()
            reject_links(path)
            if path.parent != layout.diagnostics_root or path.exists():
                raise RuntimeError("Ready file must be fresh and inside UserData/Diagnostics")
            path.write_text(
                json.dumps({"url": server.origin, "pid": os.getpid(), **runtime_observation(root)}), encoding="utf-8"
            )
        print("CareerSim Human Web: " + server.origin, flush=True)
        if not args.no_browser and not webbrowser.open(server.origin):
            print("请在浏览器打开以上地址。", flush=True)
        server.serve_forever(poll_interval=0.1)
        return 0
    except KeyboardInterrupt:
        return 0
    except Exception as error:
        print("启动失败：" + str(error), file=sys.stderr, flush=True)
        return 1
    finally:
        if server:
            server.server_close()
        if app:
            app.close()


if __name__ == "__main__":
    raise SystemExit(main())
