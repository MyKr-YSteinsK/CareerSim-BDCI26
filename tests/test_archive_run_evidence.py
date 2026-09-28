"""Synthetic archive and secret-boundary checks for WF-01."""

import json
import subprocess
from pathlib import Path

import pytest

from scripts.archive_run_evidence import UnsafeEvidence, archive


def _files(tmp_path: Path) -> tuple[Path, Path]:
    repo = tmp_path / "repo"
    repo.mkdir()
    source = tmp_path / "source"
    source.mkdir()
    (source / "events.jsonl").write_text('{"kind":"observe"}\n', encoding="utf-8")
    (source / "transcript.log").write_text("SESSION=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n", encoding="utf-8")
    (source / "llm.log").write_text(
        "2026-09-27 18:00:00 CurrentRoundCompressor\n"
        "2026-09-28 18:05:00 CurrentRoundCompressor\n"
        "2026-09-28 18:08:00 CurrentRoundCompressor\n",
        encoding="utf-8",
    )
    return repo, source


def test_archive_scans_slices_and_stages_only_named_artifacts(tmp_path: Path) -> None:
    repo, source = _files(tmp_path)
    subprocess.run(["git", "init", "-q", str(repo)], check=True)
    (repo / ".gitignore").write_text("artifacts/\n", encoding="utf-8")
    dest = archive(
        repo,
        source,
        "synthetic-run",
        {"events": "events.jsonl", "transcript": "transcript.log"},
        {"llm": "llm.log"},
        "2026-09-28T10:00:00+00:00",
        "2026-09-28T10:10:00+00:00",
        "+08:00",
        stage=True,
    )
    assert dest == repo / "artifacts" / "dev-runs" / "synthetic-run"
    assert (dest / "llm-run.log").read_text(encoding="utf-8").count("CurrentRoundCompressor") == 2
    manifest = json.loads((dest / "evidence-manifest.json").read_text(encoding="utf-8"))
    assert manifest["run_id"] == "synthetic-run"
    assert {item["name"] for item in manifest["artifacts"]} == {"events.jsonl", "transcript.log", "llm-run.log"}
    staged = subprocess.run(["git", "-C", str(repo), "diff", "--cached", "--name-only"], check=True, capture_output=True, text=True).stdout.splitlines()
    assert set(staged) == {
        "artifacts/dev-runs/synthetic-run/events.jsonl",
        "artifacts/dev-runs/synthetic-run/transcript.log",
        "artifacts/dev-runs/synthetic-run/llm-run.log",
        "artifacts/dev-runs/synthetic-run/evidence-manifest.json",
    }


def test_secret_refusal_leaves_no_archive(tmp_path: Path) -> None:
    repo, source = _files(tmp_path)
    (source / "runner-result.json").write_text('{"api_key":"sk-exampleSecretValue123456"}\n', encoding="utf-8")
    with pytest.raises(UnsafeEvidence, match="content withheld"):
        archive(repo, source, "unsafe-run", {"runner_result": "runner-result.json"}, {}, stage=False)
    assert not (repo / "artifacts" / "dev-runs" / "unsafe-run").exists()


def test_source_path_cannot_escape_explicit_run_dir(tmp_path: Path) -> None:
    repo, source = _files(tmp_path)
    (tmp_path / "outside.jsonl").write_text('{}\n', encoding="utf-8")
    with pytest.raises(UnsafeEvidence, match="within --source-dir"):
        archive(repo, source, "escaped-run", {"events": "../outside.jsonl"}, {})


def test_cross_session_core_is_refused(tmp_path: Path) -> None:
    repo, source = _files(tmp_path)
    (source / "events.jsonl").write_text(
        '"session_id":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"\n'
        '"session_id":"bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"\n',
        encoding="utf-8",
    )
    with pytest.raises(UnsafeEvidence, match="multiple session markers"):
        archive(repo, source, "mixed-run", {"events": "events.jsonl"}, {})
    assert not (repo / "artifacts" / "dev-runs" / "mixed-run").exists()
