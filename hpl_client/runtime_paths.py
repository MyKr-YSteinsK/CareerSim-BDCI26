"""Development and portable runtime paths for the Human Play Lab client."""

from __future__ import annotations

import hashlib
import json
import re
import sys
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from scripts.hpl_preflight import DATASET_PATHS, REQUIRED_DATASET_RESOURCES


EXPECTED_VERSIONS = {
    "career_emulator": "1.0.1",
    "career_emulator_bdci26": "1.0.0",
    "flet": "1.0.1",
}
BUILD_MANIFEST_NAME = "BUILD_MANIFEST.json"
PORTABLE_APP_VERSION = "1.0.0"
EXPECTED_DATASET_FILE_COUNT = 194
FLET_RUNTIME_ARCHIVE = Path("flet_desktop") / "app" / "flet-windows.zip"


@dataclass(frozen=True)
class RuntimeLayout:
    """Writable and read-only roots used by a packaged application."""

    mode: str
    application_root: Path
    bundle_root: Path
    sandbox_root: Path
    runs_root: Path
    exports_root: Path
    diagnostics_root: Path
    dataset_root: Path
    build_manifest_path: Path

    @property
    def workspace_root(self) -> Path:
        # The cleanup guard uses this only to reject protected Agent paths. A
        # portable bundle has no repository, so its application directory is
        # the only safe equivalent.
        return self.application_root

    @property
    def worktree_root(self) -> Path:
        return self.application_root


def is_packaged_mode() -> bool:
    return bool(getattr(sys, "frozen", False))


def _bundle_root() -> Path:
    root = Path(getattr(sys, "_MEIPASS", Path(sys.executable).parent)).resolve()
    if not root.is_dir():
        raise RuntimeError(f"Portable bundle root is unavailable: {root}")
    return root


def _is_link(path: Path) -> bool:
    return path.is_symlink() or getattr(path, "is_junction", lambda: False)()


def _ensure_writable(path: Path, *, label: str = "UserData") -> None:
    if _is_link(path):
        raise RuntimeError(f"{label} 不能是符号链接或 junction：{path}")
    try:
        path.mkdir(parents=True, exist_ok=True)
    except OSError as error:
        raise RuntimeError(f"无法写入便携版 {label}：{path}") from error
    probe = path / f".hpl-write-probe-{uuid.uuid4().hex}"
    try:
        probe.write_bytes(b"HPL")
    except OSError as error:
        raise RuntimeError(f"无法写入便携版 {label}：{path}") from error
    finally:
        try:
            probe.unlink(missing_ok=True)
        except OSError:
            pass


def resolve_packaged_layout(*, ensure_writable: bool = True) -> RuntimeLayout:
    if not is_packaged_mode():
        raise RuntimeError("Packaged runtime paths requested by a non-packaged process")
    application_root = Path(sys.executable).resolve().parent
    bundle_root = _bundle_root()
    sandbox_root = application_root / "UserData"
    layout = RuntimeLayout(
        mode="PACKAGED_MODE",
        application_root=application_root,
        bundle_root=bundle_root,
        sandbox_root=sandbox_root,
        runs_root=sandbox_root / "Runs",
        exports_root=sandbox_root / "Exports",
        diagnostics_root=sandbox_root / "Diagnostics",
        dataset_root=bundle_root / "career_emulator" / "data" / "dataset",
        build_manifest_path=application_root / BUILD_MANIFEST_NAME,
    )
    if ensure_writable:
        _ensure_writable(application_root, label="应用目录")
        for root, label in (
            (layout.sandbox_root, "UserData"),
            (layout.runs_root, "UserData\\Runs"),
            (layout.exports_root, "UserData\\Exports"),
            (layout.diagnostics_root, "UserData\\Diagnostics"),
        ):
            _ensure_writable(root, label=label)
    return layout


def _tree_inventory(root: Path) -> dict[str, Any]:
    if root.is_symlink() or not root.is_dir():
        raise RuntimeError(f"Bundled dataset is unavailable: {root}")
    files: dict[str, str] = {}
    directories: list[str] = []
    for path in sorted(root.rglob("*")):
        if path.is_symlink() or getattr(path, "is_junction", lambda: False)():
            raise RuntimeError(f"Bundled dataset contains a link: {path}")
        relative = path.relative_to(root).as_posix()
        if path.is_file():
            files[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
        elif path.is_dir():
            directories.append(relative)
    if not files:
        raise RuntimeError("Bundled dataset is empty")
    return {"files": files, "directories": directories}


def _tree_hash(inventory: dict[str, Any]) -> str:
    encoded = json.dumps(inventory, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def _file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _read_build_manifest(layout: RuntimeLayout) -> dict[str, Any]:
    path = layout.build_manifest_path
    if path.is_symlink() or not path.is_file():
        raise RuntimeError(f"Portable BUILD_MANIFEST.json is missing: {path}")
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        raise RuntimeError("Portable BUILD_MANIFEST.json is not valid JSON") from error
    if manifest.get("app_version") != PORTABLE_APP_VERSION:
        raise RuntimeError("Portable application version is not supported")
    if manifest.get("runtime_mode") != "PACKAGED_MODE":
        raise RuntimeError("Portable build manifest does not describe PACKAGED_MODE")
    dataset = manifest.get("dataset", {})
    source_distribution = dataset.get("source_distribution", {})
    if (
        dataset.get("split") != "dev"
        or dataset.get("default_root") != "career_emulator/data/dataset"
        or source_distribution.get("distribution") != "career-emulator-bdci26"
        or source_distribution.get("version") != EXPECTED_VERSIONS["career_emulator_bdci26"]
        or source_distribution.get("dataset_file_count") != EXPECTED_DATASET_FILE_COUNT
        or dataset.get("file_count") != EXPECTED_DATASET_FILE_COUNT
        or not re.fullmatch(r"[0-9a-f]{64}", source_distribution.get("record_sha256", ""))
    ):
        raise RuntimeError("Portable manifest does not identify the complete pinned BDCI26 Dev dataset")
    return manifest


def packaged_startup_self_check(layout: RuntimeLayout) -> dict[str, Any]:
    """Validate immutable bundled resources before any game can be created."""
    manifest = _read_build_manifest(layout)
    flet_archive = layout.bundle_root / FLET_RUNTIME_ARCHIVE
    if flet_archive.is_symlink() or not flet_archive.is_file():
        raise RuntimeError(f"Portable Flet desktop runtime archive is missing: {flet_archive}")
    expected_flet_hash = manifest.get("packaged_resources", {}).get("flet_desktop_runtime_sha256")
    if not expected_flet_hash or _file_hash(flet_archive) != expected_flet_hash:
        raise RuntimeError("Portable Flet runtime archive does not match BUILD_MANIFEST.json")
    required = [layout.dataset_root / resource for resource in REQUIRED_DATASET_RESOURCES]
    missing = [str(path.relative_to(layout.bundle_root)) for path in required if not path.is_file()]
    if missing:
        raise RuntimeError("Portable bundle is missing required resources: " + ", ".join(missing))
    inventory = _tree_inventory(layout.dataset_root)
    expected_dataset = manifest.get("dataset", {})
    if inventory != expected_dataset.get("inventory"):
        raise RuntimeError("Portable Dev dataset bytes do not match BUILD_MANIFEST.json")
    if len(inventory["files"]) != EXPECTED_DATASET_FILE_COUNT or len(inventory["files"]) != expected_dataset.get("file_count"):
        raise RuntimeError("Portable Dev dataset file count does not match BUILD_MANIFEST.json")
    if _tree_hash(inventory) != expected_dataset.get("tree_sha256"):
        raise RuntimeError("Portable Dev dataset tree hash does not match BUILD_MANIFEST.json")
    engine_paths = {name: str(layout.dataset_root / relative) for name, relative in DATASET_PATHS.items()}
    if any(not Path(path).is_dir() for path in engine_paths.values()):
        raise RuntimeError("Portable Dev dataset is missing an official GameEngine directory")
    if any(not path.is_dir() for path in (layout.sandbox_root, layout.runs_root, layout.exports_root, layout.diagnostics_root)):
        raise RuntimeError("Portable writable roots are unavailable")
    return {
        "manifest": manifest,
        "dataset": {"file_count": len(inventory["files"]), "tree_sha256": _tree_hash(inventory)},
        "engine_paths": engine_paths,
        "flet_runtime_archive": str(flet_archive),
        "runtime_root": str(layout.sandbox_root),
        "exports_root": str(layout.exports_root),
        "diagnostics_root": str(layout.diagnostics_root),
        "external_python_fallback": False,
        "network_startup": False,
    }


def configure_packaged_flet(layout: RuntimeLayout) -> None:
    """Keep Flet's unpacked desktop client and fallback path inside HPL runtime.

    Flet normally uses ``%USERPROFILE%\\.flet`` and downloads its client when
    the bundled archive is not found. A portable bundle must use its own
    immutable archive and keep the unpacked client under the HPL LocalAppData
    sandbox, so a developer cache or network cannot silently become a runtime
    dependency.
    """
    import flet_desktop

    bundle_bin = layout.bundle_root / FLET_RUNTIME_ARCHIVE.parent
    flet_desktop.get_package_bin_dir = lambda: str(bundle_bin)

    def _portable_client_storage(fingerprint: str | None = None) -> Path:
        name = f"flet-desktop-portable-{flet_desktop.version.version}"
        if fingerprint:
            name += f"-{fingerprint}"
        path = layout.diagnostics_root / "flet-client" / name
        path.parent.mkdir(parents=True, exist_ok=True)
        return path

    flet_desktop.__get_client_storage_dir = _portable_client_storage

    def _network_fallback_disabled(_file_name: str) -> str:
        raise RuntimeError("Portable Flet runtime archive is unavailable; network fallback is disabled")

    flet_desktop.__download_flet_client = _network_fallback_disabled


def packaged_identity(layout: RuntimeLayout) -> dict[str, Any]:
    manifest = _read_build_manifest(layout)
    return {
        "python_version": manifest["python_version"],
        "hpl_commit": manifest["hpl_source_commit"],
        "engine_paths": {name: str(layout.dataset_root / relative) for name, relative in DATASET_PATHS.items()},
        "dataset_root": "career_emulator/data/dataset",
        "build_manifest": manifest,
    }
