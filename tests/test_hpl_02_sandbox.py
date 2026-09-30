"""Offline acceptance tests for the isolated Human Play Lab sandbox."""

from __future__ import annotations

import asyncio
import json
import subprocess
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest

from scripts.hpl_evidence_writer import write_run_evidence
from scripts.hpl_play import (
    HPLLayout,
    assert_isolated_run_root,
    attach_public_selection,
    engine_constructor_kwargs,
    live_gate_allows,
    make_input_interceptor,
    parse_cli_transcript,
    resolve_layout,
    wire_official_cli,
)
from scripts.hpl_preflight import DATASET_PATHS
from scripts.hpl_public_evidence import project_cli_frame


def _manifest() -> dict[str, Any]:
    return {
        "run_id": "fixture-run-01",
        "authorization_id": "MAIN-GATE-FIXTURE",
        "session_id": "session-public-01",
        "human_tag": "fixture",
        "started_at": "2026-09-30T00:00:00+00:00",
        "ended_at": "2026-09-30T00:01:00+00:00",
        "hpl_commit": "a874f5471bbff4c46216f36174acb4d785c05cc4",
        "launcher_version": "hpl-02/v1",
        "python_version": "3.12.13",
        "career_emulator_version": "1.0.1",
        "career_emulator_bdci26_version": "1.0.0",
        "dataset_source": "distribution",
        "dataset_split": "dev",
        "dataset_root": "D:/HPL/venv/site-packages/career_emulator_bdci26/dev/dataset",
        "hpl_venv_root": "D:/HPL/venv",
        "hpl_runtime_root": "D:/HPL/runs/fixture-run-01",
        "provider_used": False,
        "provider_evidence_basis": ["synthetic offline fixture"],
        "public_evidence_schema_version": "hpl-public-evidence/v1",
    }


def _frame() -> dict[str, Any]:
    return {
        "state": {"session_id": "session-public-01", "month": 1, "health": 8},
        "event": {
            "title": "Visible event",
            "description": "Visible event description",
            "event_id": "DO_NOT_STORE_EVENT_ID_9301",
            "node_id": "DO_NOT_STORE_NODE_ID_9302",
        },
        "choices": [{"choice": 1, "action": "Visible choice", "energy_cost": 2, "status_updates": {"health": -1}}],
        "human_selection": {"choice": 1, "action": "Visible choice"},
        "final_result": {
            "outcome": "48-month completion",
            "survival_months": 48,
            "grade": "B",
            "quantitative_score": 64.0,
            "dimensions": [{"label": "DO_NOT_STORE_DIMENSION_9303"}],
        },
        "human_interpretation": {"created_at": "2026-09-30T00:00:00+00:00", "text": "My interpretation"},
    }


def test_dry_run_launcher_is_no_write_and_live_gate_fails_closed() -> None:
    layout = resolve_layout()
    interpreter = layout.sandbox_root / "venv" / "Scripts" / "python.exe"
    launcher = layout.worktree_root / "scripts" / "hpl_play.py"
    existing_runs = {path.name for path in layout.runs_root.iterdir()} if layout.runs_root.is_dir() else set()
    result = subprocess.run(
        [str(interpreter), str(launcher)],
        check=True,
        capture_output=True,
        text=True,
        timeout=30,
    )
    plan = json.loads(result.stdout)
    run_root = Path(plan["prospective_run_root"])

    assert plan["mode"] == "DRY_RUN_PREFLIGHT"
    assert plan["GAME_STARTED"] is False
    assert plan["LIVE_AUTHORIZED"] is False
    assert plan["run_root_created"] is False
    assert plan["provider_called"] is False
    assert plan["dataset_updated"] is False
    assert not run_root.exists()
    assert not (run_root / "runtime" / "career_emulator.sqlite3").exists()
    assert not (run_root / "runtime" / "logs").exists()

    import_probe = subprocess.run(
        [
            str(interpreter),
            "-c",
            f"import sys; sys.path.insert(0, {str(layout.worktree_root)!r}); "
            "import scripts.hpl_play; print('career_emulator' in sys.modules)",
        ],
        check=True,
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert import_probe.stdout.strip() == "False"

    authorization_without_live = subprocess.run(
        [str(interpreter), str(launcher), "--authorization-id", "MAIN-GATE-01"],
        check=True,
        capture_output=True,
        text=True,
        timeout=30,
    )
    auth_only_plan = json.loads(authorization_without_live.stdout)
    assert auth_only_plan["authorization_gate"] == {
        "explicit_live_intent": False,
        "authorization_id_present": True,
        "live_allowed": False,
    }
    assert Path(auth_only_plan["prospective_run_root"]).exists() is False

    live_without_authorization = subprocess.run(
        [str(interpreter), str(launcher), "--live"],
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert live_without_authorization.returncode == 2
    assert "authorization" in live_without_authorization.stderr.casefold()
    assert ({path.name for path in layout.runs_root.iterdir()} if layout.runs_root.is_dir() else set()) == existing_runs

    assert live_gate_allows(False, None) is False
    assert live_gate_allows(False, "MAIN-GATE-01") is False
    assert live_gate_allows(True, "MAIN-GATE-01") is True
    with pytest.raises(PermissionError, match="authorization"):
        live_gate_allows(True, " ")


def test_logs_are_intercepted_and_safe_inputs_are_forwarded() -> None:
    inputs = iter(["logs", "handbook", "1", "quit"])
    messages: list[str] = []
    forwarded: list[tuple[str, str]] = []
    blocked: list[str] = []
    guard = make_input_interceptor(
        lambda prompt: next(inputs),
        messages.append,
        lambda prompt, value: forwarded.append((prompt, value)),
        blocked.append,
    )

    returned = [guard("choice: "), guard("choice: "), guard("choice: ")]

    assert returned == ["handbook", "1", "quit"]
    assert messages == ["HPL: raw logs are disabled by the public-evidence firewall"]
    assert blocked == ["logs"]
    assert forwarded == [("choice: ", "handbook"), ("choice: ", "1"), ("choice: ", "quit")]


def test_official_cli_engine_and_share_hooks_are_narrowly_replaced() -> None:
    called: list[bool] = []

    async def original_share(*_args: Any, **_kwargs: Any) -> None:
        called.append(True)

    cli = SimpleNamespace(get_default_engine=lambda: "default", offer_share=original_share)
    engine = object()

    wire_official_cli(cli, engine)
    asyncio.run(cli.offer_share(engine, "session"))

    assert cli.get_default_engine() is engine
    assert called == []


def test_engine_arguments_pin_exactly_the_seven_hpl_dataset_directories(tmp_path: Path) -> None:
    paths = {name: str(tmp_path / relative) for name, relative in DATASET_PATHS.items()}
    db_path = tmp_path / "runtime" / "career_emulator.sqlite3"

    kwargs = engine_constructor_kwargs(paths, db_path)

    assert set(kwargs) == set(DATASET_PATHS) | {"db_path"}
    assert kwargs["db_path"] == db_path
    assert all(kwargs[name] == Path(paths[name]) for name in DATASET_PATHS)


def test_transcript_parser_removes_ids_and_internal_score_dimensions() -> None:
    transcript = """\x1b[32mStarted session: session-public-01\x1b[0m

 State  Session: session-public-01
 L1 Month 1 | Quarter 1 | Year 1
Energy   8 | Output   6 | Wealth   10
Dignity  5 | Health   8 | Network  3 | Skill  4

 Event
Visible event (SECRET-EVENT-9304:SECRET-NODE-9305)
Participant-visible description

 Choice
1. Visible choice (2)
Choice number, 'handbook', 'logs', or 'quit':

 Ending Score
B: Good outcome
48-month completion | Survived 48 months
Quantitative score: 64.0/100
Score breakdown: 44.8/60
Dimension A: 12.0 → 10.0 (weight 25%, contribution 2.5)
"""
    frames = parse_cli_transcript(transcript)
    assert len(frames) == 1
    attach_public_selection(frames, 0, "1")
    projected = project_cli_frame(frames[0])
    serialized = json.dumps(projected, ensure_ascii=False)

    assert projected["observed_fact"]["event"]["title"] == "Visible event"
    assert projected["observed_fact"]["human_selection"]["action"] == "Visible choice"
    assert projected["observed_fact"]["final_result"]["grade"] == "B"
    assert "event.event_id" in projected["unknown_fields"]
    assert "event.node_id" in projected["unknown_fields"]
    assert any("final_result.dimensions" in path for path in projected["unknown_fields"])
    assert all(value not in serialized for value in ("SECRET-EVENT-9304", "SECRET-NODE-9305", "Dimension A"))


def test_writer_creates_separate_canonical_artifacts_and_deterministic_hashes(tmp_path: Path) -> None:
    roots = [tmp_path / "one" / "fixture-run-01", tmp_path / "two" / "fixture-run-01"]
    transcript_bytes = b"raw local transcript fixture\n"
    integrity_records = []
    for root in roots:
        root.mkdir(parents=True)
        transcript = root / "transcript" / "terminal.txt"
        transcript.parent.mkdir()
        transcript.write_bytes(transcript_bytes)
        integrity_records.append(write_run_evidence(root, _manifest(), [_frame()], transcript_path=transcript))

    first = roots[0] / "evidence"
    canonical_text = "\n".join(path.read_text(encoding="utf-8") for path in sorted(first.glob("*.json*")))
    trajectory = json.loads((first / "trajectory.jsonl").read_text(encoding="utf-8"))

    assert {path.name for path in first.iterdir()} == {
        "manifest.json",
        "trajectory.jsonl",
        "summary.json",
        "integrity.json",
    }
    assert "human_interpretation" not in trajectory["observed_fact"]
    assert trajectory["human_interpretation"]["text"] == "My interpretation"
    assert trajectory["public_status"] == "PUBLIC_STATUS_UNKNOWN"
    assert "DO_NOT_STORE_EVENT_ID_9301" not in canonical_text
    assert "DO_NOT_STORE_NODE_ID_9302" not in canonical_text
    assert "DO_NOT_STORE_DIMENSION_9303" not in canonical_text
    assert any("status_updates" in path for path in trajectory["unknown_fields"])
    assert integrity_records[0]["canonical_artifact_sha256"] == integrity_records[1]["canonical_artifact_sha256"]
    assert integrity_records[0]["public_only_validation"] == "PASS"
    assert integrity_records[0]["secret_scan_status"] == "PASS_PATTERN_SCAN_ONLY"
    assert integrity_records[0]["transcript"]["present"] is True

    empty_root = tmp_path / "empty" / "empty-run"
    empty_root.mkdir(parents=True)
    empty_manifest = _manifest()
    empty_manifest["run_id"] = "empty-run"
    write_run_evidence(empty_root, empty_manifest, [])
    empty_summary = json.loads((empty_root / "evidence" / "summary.json").read_text(encoding="utf-8"))
    assert empty_summary["public_status"] == "PUBLIC_STATUS_UNKNOWN"

    clean_root = tmp_path / "clean" / "clean-run"
    clean_root.mkdir(parents=True)
    clean_manifest = _manifest()
    clean_manifest["run_id"] = "clean-run"
    clean_frame = {
        "state": {"month": 1},
        "event": {"title": "Visible event", "description": "Visible text"},
        "choices": [{"choice": 1, "action": "Visible choice", "energy_cost": 1}],
        "human_selection": {"choice": 1, "action": "Visible choice"},
        "human_interpretation": {"text": "My thought"},
    }
    write_run_evidence(clean_root, clean_manifest, [clean_frame])
    clean_summary = json.loads((clean_root / "evidence" / "summary.json").read_text(encoding="utf-8"))
    clean_trajectory = json.loads((clean_root / "evidence" / "trajectory.jsonl").read_text(encoding="utf-8"))
    assert clean_summary["public_status"] == "PUBLIC_FIELDS_ALLOWLISTED"
    assert clean_trajectory["unknown_fields"] == []
    assert "human_interpretation" not in clean_trajectory["observed_fact"]

    missing_provider_evidence_root = tmp_path / "missing-provider-evidence" / "fixture-run-01"
    missing_provider_evidence_root.mkdir(parents=True)
    invalid_manifest = _manifest()
    invalid_manifest.pop("provider_used")
    with pytest.raises(ValueError, match="provider_used"):
        write_run_evidence(missing_provider_evidence_root, invalid_manifest, [])


def test_clean_frame_stays_allowlisted_and_interpretation_is_not_a_fact() -> None:
    projected = project_cli_frame(
        {
            "state": {"month": 1},
            "event": {"title": "Visible event", "description": "Visible text"},
            "choices": [{"choice": 1, "action": "Visible choice", "energy_cost": 1}],
            "human_selection": {"choice": 1, "action": "Visible choice"},
            "human_interpretation": {"text": "My thought"},
        }
    )

    assert projected["public_status"] == "PUBLIC_FIELDS_ALLOWLISTED"
    assert projected["unknown_fields"] == []
    assert "human_interpretation" in projected
    assert "human_interpretation" not in projected["observed_fact"]


def test_hpl_run_root_rejects_overlap_with_existing_agent_runtime(tmp_path: Path) -> None:
    workspace = tmp_path / "CareerSim"
    hpl_root = workspace / ".local" / "runtime" / "human-play-lab"
    agent_runtime = workspace / ".local" / "runtime" / "formal-agent"
    agent_runtime.mkdir(parents=True)
    layout = HPLLayout(
        workspace_root=workspace,
        worktree_root=workspace / ".local" / "worktrees" / "human-play-lab",
        sandbox_root=hpl_root,
    )

    assert_isolated_run_root(hpl_root / "runs" / "test-run", layout)
    with pytest.raises(ValueError, match="protected Agent path"):
        assert_isolated_run_root(agent_runtime / "test-run", layout)


def test_evidence_writer_has_no_simulator_or_database_imports() -> None:
    source = (Path(__file__).parents[1] / "scripts" / "hpl_evidence_writer.py").read_text(encoding="utf-8")

    assert "sqlite3" not in source
    assert "career_emulator.storage" not in source
    assert "SessionStore" not in source
