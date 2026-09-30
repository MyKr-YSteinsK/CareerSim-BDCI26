"""Offline contracts for the HPL-04 portable bundle and startup gate."""

import asyncio
import json
import importlib.util
import hashlib
import zipfile
from pathlib import Path

import pytest

from hpl_client import runtime_paths
from hpl_client.runtime_paths import RuntimeLayout, packaged_startup_self_check, resolve_packaged_layout


_PACKAGE_MANIFEST_PATH = Path(__file__).resolve().parents[1] / "packaging" / "windows" / "package_manifest.py"
_PACKAGE_MANIFEST_SPEC = importlib.util.spec_from_file_location("hpl_package_manifest", _PACKAGE_MANIFEST_PATH)
assert _PACKAGE_MANIFEST_SPEC and _PACKAGE_MANIFEST_SPEC.loader
package_manifest = importlib.util.module_from_spec(_PACKAGE_MANIFEST_SPEC)
_PACKAGE_MANIFEST_SPEC.loader.exec_module(package_manifest)


def _portable_zip(path: Path, *, forbidden_entry: str | None = None, source_path_leak: bool = False) -> None:
    root = "CareerSim-Human-v1"
    resources = package_manifest.REQUIRED_RESOURCES
    files = {resource: f"fixture:{resource}".encode() for resource in resources}
    while len(files) < package_manifest.EXPECTED_DATASET_FILE_COUNT:
        name = f"fixture_data/resource_{len(files):03d}.data"
        files[name] = f"fixture:{name}".encode()
    inventory = {
        "files": {resource: hashlib.sha256(content).hexdigest() for resource, content in files.items()},
        "directories": sorted({Path(resource).parent.as_posix() for resource in files}),
    }
    manifest = {
        "runtime_mode": "PACKAGED_MODE",
        "app_version": "1.0.0",
        "python_version": "3.12.10",
        "pyinstaller_version": "6.16.0",
        "flet_version": "1.0.1",
        "career_emulator_version": "1.0.1",
        "career_emulator_bdci26_version": "1.0.0",
        "dataset": {
            "source_distribution": {
                "distribution": "career-emulator-bdci26",
                "version": "1.0.0",
                "record_sha256": "0" * 64,
                "dataset_file_count": len(files),
            },
            "file_count": len(files),
            "tree_sha256": package_manifest.tree_hash(inventory),
            "inventory": inventory,
            "required_resources": list(resources),
            "performance_score_config": "career_emulator/data/dataset/performance_score/config.data",
        },
        "packaged_resources": {
            "flet_desktop_runtime": package_manifest.FLET_RUNTIME_ARCHIVE,
            "flet_desktop_runtime_sha256": hashlib.sha256(b"fixture-flet-runtime").hexdigest(),
        },
    }
    entries = {
        f"{root}/CareerSim Human.exe": b"fixture-executable",
        f"{root}/BUILD_MANIFEST.json": json.dumps(manifest).encode(),
        f"{root}/README.txt": b"D:\\CS\\CareerSim" if source_path_leak else b"portable fixture",
        f"{root}/LICENSES/LICENSE.txt": b"license",
        f"{root}/_internal/flet_desktop/app/flet-windows.zip": b"fixture-flet-runtime",
    }
    entries.update({f"{root}/_internal/career_emulator/data/dataset/{name}": content for name, content in files.items()})
    if forbidden_entry:
        entries[f"{root}/{forbidden_entry}"] = b"forbidden"
    with zipfile.ZipFile(path, "w") as archive:
        for name, content in entries.items():
            archive.writestr(name, content)


def test_portable_verifier_accepts_default_dataset_fixture_and_rejects_agent_path(tmp_path):
    valid = tmp_path / "valid.zip"
    _portable_zip(valid)
    result = package_manifest.verify(valid)
    assert result["dataset_file_count"] == package_manifest.EXPECTED_DATASET_FILE_COUNT

    invalid = tmp_path / "invalid.zip"
    _portable_zip(invalid, forbidden_entry=".env/config.json")
    with pytest.raises(ValueError, match="forbidden path/config marker"):
        package_manifest.verify(invalid)

    leaked = tmp_path / "leaked.zip"
    _portable_zip(leaked, source_path_leak=True)
    with pytest.raises(ValueError, match="leaks a repository"):
        package_manifest.verify(leaked)


def test_packaged_startup_self_check_requires_performance_score_default_resource(tmp_path, monkeypatch):
    bundle = tmp_path / "bundle"
    dataset = bundle / "career_emulator" / "data" / "dataset"
    (dataset / "performance_score").mkdir(parents=True)
    config = dataset / "performance_score" / "config.data"
    config.write_bytes(b"fixture-config")
    flet_archive = bundle / "flet_desktop" / "app" / "flet-windows.zip"
    flet_archive.parent.mkdir(parents=True)
    flet_archive.write_bytes(b"fixture-flet-runtime")
    application = tmp_path / "app"
    application.mkdir()
    sandbox = application / "UserData"
    exports = sandbox / "Exports"
    runs = sandbox / "Runs"
    diagnostics = sandbox / "Diagnostics"
    sandbox.mkdir()
    exports.mkdir(parents=True)
    runs.mkdir(parents=True)
    diagnostics.mkdir(parents=True)
    inventory = runtime_paths._tree_inventory(dataset)
    (application / "BUILD_MANIFEST.json").write_text(
        json.dumps(
            {
                "runtime_mode": "PACKAGED_MODE",
                "app_version": "1.0.0",
                "dataset": {
                    "split": "dev",
                    "file_count": 1,
                    "tree_sha256": runtime_paths._tree_hash(inventory),
                    "inventory": inventory,
                    "default_root": "career_emulator/data/dataset",
                    "source_distribution": {
                        "distribution": "career-emulator-bdci26",
                        "version": "1.0.0",
                        "dataset_file_count": 1,
                        "record_sha256": "0" * 64,
                    },
                },
                "packaged_resources": {
                    "flet_desktop_runtime_sha256": hashlib.sha256(b"fixture-flet-runtime").hexdigest(),
                },
            }
        ),
        encoding="utf-8",
    )
    layout = RuntimeLayout(
        mode="PACKAGED_MODE",
        application_root=application,
        bundle_root=bundle,
        sandbox_root=sandbox,
        runs_root=runs,
        exports_root=exports,
        diagnostics_root=diagnostics,
        dataset_root=dataset,
        build_manifest_path=application / "BUILD_MANIFEST.json",
    )
    monkeypatch.setattr(runtime_paths, "REQUIRED_DATASET_RESOURCES", ("performance_score/config.data",))
    monkeypatch.setattr(runtime_paths, "DATASET_PATHS", {"performance_score": "performance_score"})
    monkeypatch.setattr(runtime_paths, "EXPECTED_DATASET_FILE_COUNT", 1)
    checked = packaged_startup_self_check(layout)
    assert checked["dataset"]["file_count"] == 1
    assert checked["engine_paths"]["performance_score"].endswith("performance_score")
    assert checked["external_python_fallback"] is False

    config.unlink()
    with pytest.raises(RuntimeError, match="performance_score.*config.data"):
        packaged_startup_self_check(layout)


def test_build_contract_uses_hpl_only_runtime_and_onedir():
    build = Path(__file__).resolve().parents[1] / "scripts" / "build-hpl-portable.ps1"
    source = build.read_text(encoding="utf-8")
    assert "--onedir" in source
    assert "packaging-python" in source
    assert "VIRTUAL_ENV = $packageVenv" in source
    assert ".local\\runtime\\human-play-lab" in source
    assert "career_emulator/data/dataset" in source
    assert "runtime 'venv\\Scripts\\python.exe'" not in source
    assert "uv run" not in source
    assert "root .venv" not in source


def test_packaged_layout_writes_only_to_application_userdata(tmp_path, monkeypatch):
    application = tmp_path / "portable"
    bundle = application / "_internal"
    bundle.mkdir(parents=True)
    executable = application / "CareerSim Human.exe"
    executable.write_bytes(b"fixture")
    monkeypatch.setattr(runtime_paths.sys, "frozen", True, raising=False)
    monkeypatch.setattr(runtime_paths.sys, "executable", str(executable))
    monkeypatch.setattr(runtime_paths.sys, "_MEIPASS", str(bundle), raising=False)
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path / "external-localappdata"))

    layout = resolve_packaged_layout()

    assert layout.sandbox_root == application / "UserData"
    assert layout.runs_root == application / "UserData" / "Runs"
    assert layout.exports_root == application / "UserData" / "Exports"
    assert layout.diagnostics_root == application / "UserData" / "Diagnostics"
    assert all(path.is_dir() for path in (layout.runs_root, layout.exports_root, layout.diagnostics_root))
    assert not (tmp_path / "external-localappdata").exists()


def test_dev_dataset_source_is_bound_to_installed_distribution_record():
    from importlib.metadata import distribution

    installed = distribution("career-emulator-bdci26")
    source = Path(installed.locate_file("career_emulator_bdci26/dev/dataset"))
    identity = package_manifest._dataset_distribution_identity(package_manifest.inventory(source))

    assert identity["distribution"] == "career-emulator-bdci26"
    assert identity["version"] == "1.0.0"
    assert identity["dataset_file_count"] == 194
    assert len(identity["record_sha256"]) == 64


def test_export_failure_keeps_run_and_copies_diagnostic_to_userdata(tmp_path):
    from hpl_client.controller import HumanGameController
    from hpl_client.recorder import RunRecorder

    root = tmp_path / "portable" / "UserData" / "Runs" / "fixture-run"
    diagnostics = tmp_path / "portable" / "UserData" / "Diagnostics"
    root.mkdir(parents=True)
    diagnostics.mkdir(parents=True)
    recorder = RunRecorder(root, {"run_id": root.name}, diagnostics_root=diagnostics)
    controller = HumanGameController(
        finalizer=lambda *_args: (_ for _ in ()).throw(OSError("offline fixture export failure")),
        layout=object(),
    )
    controller.phase = "ENDED"
    controller.recorder = recorder

    assert asyncio.run(controller.finish_export()) is False
    assert root.is_dir()
    assert (root / "scratch" / "export_error.log").is_file()
    assert (diagnostics / "fixture-run-export_error.log").is_file()
    assert "offline fixture export failure" in (diagnostics / "fixture-run-export_error.log").read_text()


def test_packaged_startup_fails_closed_before_flet_when_application_dir_is_unwritable(tmp_path, monkeypatch):
    from hpl_client import app

    application = tmp_path / "portable"
    bundle = application / "_internal"
    bundle.mkdir(parents=True)
    executable = application / "CareerSim Human.exe"
    executable.write_bytes(b"fixture")
    monkeypatch.setattr(runtime_paths.sys, "frozen", True, raising=False)
    monkeypatch.setattr(runtime_paths.sys, "executable", str(executable))
    monkeypatch.setattr(runtime_paths.sys, "_MEIPASS", str(bundle), raising=False)
    monkeypatch.setattr(runtime_paths, "_ensure_writable", lambda *_args, **_kwargs: (_ for _ in ()).throw(RuntimeError("无法写入便携版 应用目录")))
    monkeypatch.setattr(app.ft, "run", lambda *_args, **_kwargs: pytest.fail("Flet must not start when UserData cannot be created"))
    report = tmp_path / "startup-failed.json"

    app.launch(fixture=True, smoke_report=report)

    result = json.loads(report.read_text(encoding="utf-8"))
    assert result["startup_gate"] == "FAIL_CLOSED"
    assert not result["page_session_connected"]
    assert not result["real_engine_imported"]
    assert "桌面、D 盘" in result["startup_error"]
    assert not (application / "UserData").exists()
