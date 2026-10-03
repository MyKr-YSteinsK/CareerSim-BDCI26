"""Synthetic v12 compatibility regression; never calls runtime/provider."""
import json
from pathlib import Path

import pytest

from scripts import post_run_audit as legacy
from scripts.v12_screening_audit import SKILLS, audit, provenance


@pytest.mark.parametrize("text,advertised,expected", [
    ("当前菜单 HiddenRisk+1", "HiddenRisk+1", "ADVERTISED_CONFIGURED_DELTA"),
    ("HiddenRisk +1", "HiddenRisk+1", "ADVERTISED_CONFIGURED_DELTA"),
    ("HiddenRisk-1", "HiddenRisk+1", "UNKNOWN"),
    ("HiddenRisk=7", "HiddenRisk+1", "HIDDEN_STOCK_OR_RECONSTRUCTION_VIOLATION"),
    ("累计 HiddenRisk+1", "HiddenRisk+1", "HIDDEN_STOCK_OR_RECONSTRUCTION_VIOLATION"),
])
def test_delta_provenance(text, advertised, expected):
    assert provenance(text, advertised) == expected


def fixture(tmp_path: Path, reread: bool):
    sid = "a" * 32
    rows = []
    def row(kind, payload, minute):
        rows.append({"kind": kind, "ts": f"2026-10-03T10:{minute:02d}:00+00:00", "payload": payload})
    def result(cid, name, value, minute):
        row("tool_result", {"tool_call_id": cid, "tool_name": name, "raw_output": {"result": json.dumps(value)}}, minute)
    def read(skill, minute):
        cid = f"r-{skill}-{minute}"
        row("tool_call", {"tool_call": {"tool_call_id": cid, "name": "read_file", "arguments": {"file_path": f"C:/x/agent/workspace/skills/{skill}/SKILL.md"}}}, minute)
        result(cid, "read_file", {"content": "body"}, minute)
    result("n", "new_game", {"session_id": sid}, 0)
    for skill in SKILLS:
        read(skill, 1)
    def observe(minute):
        result(f"o-{minute}", "observe", {"current_state": {"session_id": sid, "time": {"current_month": 1}, "status": {"level": 1}, "simulation_flags": {"alive": True, "failed": False}}, "choices": [{"choice": 1, "status_updates": "HiddenRisk+1"}]}, minute)
    observe(2)
    if reread:
        observe(4)
        for skill in SKILLS:
            read(skill, 5)
    row("tool_call", {"tool_call": {"tool_call_id": "a", "name": "mcp_career-emulator_take_action", "arguments": {"choice": 1, "notes": "菜单 HiddenRisk+1"}}}, 6)
    result("a", "take_action", {"success": True}, 6)
    events = tmp_path / "events.jsonl"
    events.write_text("\n".join(json.dumps(r) for r in rows), encoding="utf-8")
    transcript = tmp_path / "transcript.log"
    transcript.write_text(f"SESSION={sid}\nSESSION_BASIS\n", encoding="utf-8")
    runner = tmp_path / "result.json"
    runner.write_text('{"exit_code": 1}', encoding="utf-8")
    log = tmp_path / "llm.log"
    log.write_text("2026-10-03T10:03:00+00:00 CurrentRoundCompressor\n" if reread else "", encoding="utf-8")
    return dict(events=events, transcript=transcript, score_report=None, runner_result=runner, llm_log=log)


def test_old_markers_not_required_and_legacy_unchanged(tmp_path):
    inputs = fixture(tmp_path, False)
    old = legacy.audit(**inputs)
    summary = audit(**inputs)
    assert old["actions"]["ctrl_closure"]["status"] == "CTRL_CLOSURE_FAIL"
    assert summary["actions"]["ctrl_closure"]["status"] == "NOT_APPLICABLE"
    assert summary["adherence_evidence"]["delivery_marker_coverage"]["status"] == "NOT_APPLICABLE"
    assert summary["adherence_evidence"]["compression"]["exercise_status"] == "NOT_EXERCISED"
    assert summary["v12"]["startup_reads"] == sorted(SKILLS)
    assert summary["v12"]["hiddenrisk_references"][0]["category"] == "ADVERTISED_CONFIGURED_DELTA"
    assert "HiddenRisk+1" not in json.dumps(summary)
    assert legacy.audit(**inputs) == old


def test_two_skill_recovery_not_four_and_semantics_not_inferred(tmp_path):
    summary = audit(**fixture(tmp_path, True))
    recovery = summary["adherence_evidence"]["compression"]["recovery"][0]
    assert recovery["reread_skills"] == sorted(SKILLS)
    assert recovery["overall_status"] == "TOOL_ORDER_PASS_REBUILD_UNVERIFIED"
    assert summary["v12"]["brief_semantics"] == "UNKNOWN_REQUIRES_SEMANTIC_AUDIT"


def test_visible_compression_without_rereads_fails(tmp_path):
    inputs = fixture(tmp_path, False)
    inputs["llm_log"].write_text("2026-10-03T10:03:00+00:00 CurrentRoundCompressor\n", encoding="utf-8")
    recovery = audit(**inputs)["adherence_evidence"]["compression"]["recovery"][0]
    assert recovery["overall_status"] == "RECOVERY_FAIL"
