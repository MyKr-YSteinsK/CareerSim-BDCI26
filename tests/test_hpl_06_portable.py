"""Portable path/lifecycle contracts using synthetic fixtures only."""

import asyncio
import json
import zipfile
from pathlib import Path
from types import SimpleNamespace

import pytest

from hpl_client.export import verify_zip
from hpl_client.path_contract import assert_isolated_run_root
from hpl_client.portable_web import PortableLayout, create_controller, reject_links, writable, startup_check, digest
from scripts.hpl_web_portable_build import archive, scan


@pytest.fixture
def layout(tmp_path):
    result = PortableLayout(tmp_path)
    for path in (result.runs_root, result.exports_root, result.diagnostics_root):
        writable(path)
    return result


def test_fixture_public_export_and_cleanup(layout):
    controller = create_controller(layout, {"source_commit": "fixture-test"}, Path("unused"), fixture=True)
    assert controller.recorder is None
    assert asyncio.run(controller.start("P020"))
    run_root = controller.recorder.root
    assert run_root.parent == layout.runs_root
    view = controller.view
    assert asyncio.run(controller.choose(1, view.revision, view.run_id))
    assert controller.phase == "ENDED"
    assert controller.export_path.parent == layout.exports_root
    fields, frames, _ = verify_zip(controller.export_path, run_root.name)
    assert fields["hpl_venv_root"] == "PORTABLE_EMBEDDED_PYTHON"
    assert fields["provider_evidence_basis"] == "FIXTURE / NON_GAME"
    assert frames and not run_root.exists()
    assert not list(layout.sandbox_root.rglob("*.sqlite3"))


@pytest.mark.parametrize("relative", ["../outside", ".", "nested/run"])
def test_portable_run_requires_direct_child(layout, relative):
    with pytest.raises(ValueError):
        assert_isolated_run_root(layout.runs_root / relative, layout)


def test_success_probe_removes_itself(layout):
    writable(layout.sandbox_root)
    assert not list(layout.sandbox_root.glob(".write-probe-*"))


def test_writable_error_has_no_fallback(tmp_path, monkeypatch):
    original = Path.open

    def denied(path, *args, **kwargs):
        if path.name.startswith(".write-probe"):
            raise PermissionError("fixture denied")
        return original(path, *args, **kwargs)

    monkeypatch.setattr(Path, "open", denied)
    with pytest.raises(PermissionError):
        writable(tmp_path)
    assert list(tmp_path.iterdir()) == []


@pytest.mark.parametrize(
    "name,content", [(".env", "fixture"), ("app.py", "D:\\CS\\private"), ("app.py", "sk-" + "a" * 32)]
)
def test_release_scan_rejects_private_content(tmp_path, name, content):
    (tmp_path / name).write_text(content)
    with pytest.raises(ValueError):
        scan(tmp_path)


def test_scan_classifies_runtime_token_literals(tmp_path):
    (tmp_path / "web.py").write_text("token = secrets.token_urlsafe(32)")
    assert scan(tmp_path)[0]["tokens"]


def test_archive_is_deterministic_and_keeps_userdata(tmp_path):
    root = tmp_path / "app"
    (root / "UserData/Runs").mkdir(parents=True)
    (root / "README.txt").write_text("fixture")
    a, b = tmp_path / "a.zip", tmp_path / "b.zip"
    archive(root, a)
    archive(root, b)
    assert a.read_bytes() == b.read_bytes()
    with zipfile.ZipFile(a) as z:
        assert "CareerSim-Human-Web/UserData/Runs/" in z.namelist()


def test_links_rejected(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "is_symlink", lambda p: p == tmp_path)
    with pytest.raises(RuntimeError):
        reject_links(tmp_path / "Runtime")


@pytest.mark.parametrize("tamper", ["bytes", "extra"])
def test_startup_integrity_fails_before_package_or_game_import(tmp_path, monkeypatch, tamper):
    from hpl_client import portable_web as module

    (tmp_path / "Runtime").mkdir()
    (tmp_path / "App").mkdir()
    for name in ("Runtime/python.exe", "启动 CareerSim.cmd", "README-使用说明.txt"):
        (tmp_path / name).write_bytes(b"fixture")
    files = {p.relative_to(tmp_path).as_posix(): digest(p) for p in tmp_path.rglob("*") if p.is_file()}
    (tmp_path / "App/package-manifest.json").write_text(json.dumps({"files": files}))
    monkeypatch.setattr(module.sys, "executable", str(tmp_path / "Runtime/python.exe"))
    monkeypatch.setattr(module.platform, "python_version", lambda: "3.12.10")
    monkeypatch.setattr(module.sys, "prefix", module.sys.base_prefix)
    monkeypatch.setattr(module.sys, "flags", SimpleNamespace(isolated=True))
    if tamper == "bytes":
        (tmp_path / "Runtime/python.exe").write_bytes(b"tampered")
    else:
        (tmp_path / "Runtime/unexpected.py").write_bytes(b"fixture")
    with pytest.raises(RuntimeError, match="integrity mismatch|inventory mismatch"):
        startup_check(tmp_path)
    assert not (tmp_path / "UserData").exists()
