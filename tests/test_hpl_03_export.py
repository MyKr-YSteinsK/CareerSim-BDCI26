"""Public journal and share-safe ZIP regressions."""

import asyncio
import hashlib
import json
import zipfile

import pytest

from hpl_client.export import ARTIFACTS, export_run
from hpl_client.fixtures import FixtureEngine
from hpl_client.game_adapter import PublicGameAdapter
from hpl_client.recorder import RunRecorder


def prepare(tmp_path):
    root = tmp_path / "fixture-run"
    root.mkdir()
    manifest = {
        key: "fixture"
        for key in (
            "authorization_id",
            "human_tag",
            "started_at",
            "ended_at",
            "hpl_commit",
            "launcher_version",
            "python_version",
            "career_emulator_version",
            "career_emulator_bdci26_version",
            "dataset_source",
            "dataset_split",
            "dataset_root",
            "hpl_venv_root",
            "hpl_runtime_root",
        )
    }
    manifest.update(
        run_id=root.name,
        provider_used=False,
        provider_evidence_basis="offline fixture",
        public_evidence_schema_version="hpl-public-evidence/v1",
    )
    recorder = RunRecorder(root, manifest)
    view = asyncio.run(PublicGameAdapter(FixtureEngine(), root.name).start())
    recorder.transition(view)
    return root, recorder


def test_journal_survives_before_finalize_and_zip_has_exact_public_files(tmp_path):
    root, recorder = prepare(tmp_path)
    assert (root / "staging" / "public_journal.jsonl").is_file()
    assert not (root / "evidence").exists()
    recorder.finish("ENDED")
    (root / "private.sqlite3").write_text("DO_NOT_EXPORT")
    archive = export_run(root)
    with zipfile.ZipFile(archive) as bundle:
        assert set(bundle.namelist()) == {*ARTIFACTS, "README.txt"}
        assert all(b"DO_NOT_EXPORT" not in bundle.read(name) for name in bundle.namelist())


@pytest.mark.parametrize("tamper", ["hash", "run", "session", "secret", "path", "public"])
def test_export_rejects_corruption_even_with_recomputed_hashes(tmp_path, tamper):
    root, recorder = prepare(tmp_path)
    recorder.finish("ENDED")
    evidence = root / "evidence"
    manifest = json.loads((evidence / "manifest.json").read_text())
    if tamper == "run":
        manifest["run_id"] = "other"
    elif tamper == "session":
        manifest["session_id"] = "other"
    elif tamper == "secret":
        manifest["human_tag"] = "api_key=secret-secret"
    elif tamper == "path":
        manifest["dataset_root"] = "D:/Agent/private"
    (evidence / "manifest.json").write_text(json.dumps(manifest))
    if tamper == "public":
        frame = json.loads((evidence / "trajectory.jsonl").read_text(encoding="utf-8"))
        frame["observed_fact"]["state"]["hidden_risk"] = 5
        (evidence / "trajectory.jsonl").write_text(json.dumps(frame) + "\n")
    if tamper != "hash":
        integrity = json.loads((evidence / "integrity.json").read_text())
        integrity["canonical_artifact_sha256"] = {
            name: hashlib.sha256((evidence / name).read_bytes()).hexdigest() for name in ARTIFACTS[:-1]
        }
        (evidence / "integrity.json").write_text(json.dumps(integrity))
    with pytest.raises(ValueError):
        export_run(root)


def test_failure_retains_local_traceback_and_unknown_outcome(tmp_path):
    root, recorder = prepare(tmp_path)
    recorder.submission({"choice": 1, "action": "offline selection"})
    recorder.failure(OSError("technical fixture"))
    manifest = json.loads((root / "evidence" / "manifest.json").read_text())
    assert manifest["action_outcome"] == "UNKNOWN_AFTER_TECHNICAL_FAILURE"
    assert manifest["run_status"] == "TECHNICAL_FAILURE"
    assert (root / "scratch" / "technical_error.log").is_file()
    frame = json.loads((root / "evidence" / "trajectory.jsonl").read_text(encoding="utf-8"))
    assert frame["observed_fact"]["human_selection"]["choice"] == 1
    assert export_run(root).is_file()
