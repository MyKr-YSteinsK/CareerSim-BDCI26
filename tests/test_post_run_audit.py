"""Synthetic offline evidence for the WF-01 one-pass audit contract."""

import json
import subprocess
import sys
from pathlib import Path

from scripts.post_run_audit import audit


SESSION = "a" * 32


def _record(seq: int, minute: int, kind: str, payload: dict) -> dict:
    return {"seq": seq, "ts": f"2026-09-28T10:{minute:02d}:00+00:00", "kind": kind, "payload": payload}


def _call(seq: int, minute: int, call_id: str, name: str, args: dict) -> dict:
    return _record(seq, minute, "tool_call", {"tool_call": {"tool_call_id": call_id, "name": name, "arguments": json.dumps(args)}})


def _result(seq: int, minute: int, call_id: str, name: str, data: dict) -> dict:
    return _record(seq, minute, "tool_result", {"tool_call_id": call_id, "tool_name": name, "raw_output": {"result": json.dumps(data)}})


def _observe(month: int, level: int, title: str, terminal: bool = False) -> dict:
    payload = {
        "current_state": {
            "session_id": SESSION,
            "time": {"current_month": month, "current_quarter": (month + 2) // 3},
            "status": {"level": level, "health": 8, "output": 12, "HiddenRisk": 999},
            "simulation_flags": {"failed": terminal, "failure_reason": "Completed the 48-month simulation." if terminal else ""},
        },
        "current_event": {"title": title},
        "choices": [{"choice": 1, "action": "申请关键项目" if title == "季度主行动" else "继续工作"}],
    }
    if terminal:
        payload["ending_score"] = {"quantitative_score": 64.0, "competition_partial_score": 44.8, "survival_months": 48, "grade": "B", "completed": True}
    return payload


def _fixtures(tmp_path: Path) -> tuple[Path, Path, Path, Path, Path]:
    events = tmp_path / "events.jsonl"
    rows = [
        _call(1, 0, "n", "mcp_career-emulator_new_game", {}),
        _result(2, 0, "n", "mcp_career-emulator_new_game", {"session_id": SESSION}),
        _result(3, 1, "o1", "mcp_career-emulator_observe", _observe(1, 1, "入职")),
        _call(4, 2, "a1", "mcp_career-emulator_take_action", {"choice": 1, "notes": "[CTRL G=? P=A R=PASS X=0] Proceed"}),
        _result(5, 2, "a1", "mcp_career-emulator_take_action", {"success": True}),
        _result(6, 6, "o2", "mcp_career-emulator_observe", _observe(6, 2, "半年评审")),
        _call(7, 7, "a2", "mcp__career-emulator__take_action", {"choice": 1, "notes": "[CTRL G=Output P=A R=PASS X=0] HiddenRisk-1"}),
        _result(8, 7, "a2", "mcp__career-emulator__take_action", {"success": False, "error": "Ability not found"}),
        _result(9, 9, "o3", "mcp_career-emulator_observe", _observe(24, 3, "季度主行动")),
        _call(10, 10, "a3", "mcp_career-emulator_take_action", {"choice": 1, "notes": "[CTRL G=Output P=A R=PASS X=0] Proceed"}),
        _result(11, 10, "a3", "mcp_career-emulator_take_action", {"success": True}),
        _result(12, 11, "o4", "mcp_career-emulator_observe", _observe(49, 5, "游戏结束", terminal=True)),
    ]
    events.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows), encoding="utf-8")
    transcript = tmp_path / "transcript.log"
    transcript.write_text(f"SESSION={SESSION}\nDelivery: NO_CHANGE\n", encoding="utf-8")
    score_report = tmp_path / "score_report.json"
    score_report.write_text(json.dumps({"session_id": "", "ending_score": {"quantitative_score": 64.0}, "token_usage": {"input_tokens": 100, "output_tokens": 20, "total_tokens": 120}}), encoding="utf-8")
    runner_result = tmp_path / "runner-result.json"
    runner_result.write_text('{"exit_code": 0}', encoding="utf-8")
    llm_log = tmp_path / "llm.log"
    old = "".join(f"2026-09-27 18:00:{second:02d} CurrentRoundCompressor\n" for second in range(23))
    llm_log.write_text(old + "2026-09-28 18:05:00 CurrentRoundCompressor\n2026-09-28 18:08:00 CurrentRoundCompressor\n", encoding="utf-8")
    return events, transcript, score_report, runner_result, llm_log


def test_fresh_score_and_cumulative_log_scoping(tmp_path: Path) -> None:
    events, transcript, score_report, runner_result, llm_log = _fixtures(tmp_path)
    summary = audit(events, transcript, score_report, runner_result, llm_log, log_utc_offset="+08:00")
    assert summary["run"]["events_identity"] == "PASS"
    assert summary["run"]["transcript_identity"] == "PASS"
    assert summary["outcome"]["classification"] == "VALID_48M_COMPLETION"
    assert summary["outcome"]["score_source"] == "fresh_final_observe"
    assert summary["outcome"]["terminal_fresh_score"]["quantitative_score"] == 64.0
    assert summary["outcome"]["score_report_session_field"] == "EMPTY"
    assert summary["adherence_evidence"]["compression"]["count"] == 2
    assert [item["status"] for item in summary["adherence_evidence"]["compression"]["recovery"]] == ["FAIL", "FAIL"]
    assert summary["trajectory"]["promotion_checkpoints"][0] == {"month": 6, "from_level": 1, "to_level": 2, "source": "observed_level_change"}
    assert summary["trajectory"]["quarterly_main_actions"] == [{"month": 24, "action": "申请关键项目", "source": "public_choice"}]
    assert summary["actions"]["attempts"] == 3
    assert summary["actions"]["success"] == 2
    assert summary["actions"]["errors"] == 1
    assert summary["actions"]["noncanonical_routes"] == 1
    assert summary["actions"]["ctrl"]["valid"] == 3
    assert summary["actions"]["evidence_discipline_categories"]["numeric_hiddenrisk_reference"] == 1
    assert "HiddenRisk-1" not in json.dumps(summary, ensure_ascii=False)
    assert "hiddenrisk" not in summary["outcome"]["terminal_public_state"]["status"]
    assert json.dumps(summary, ensure_ascii=False, sort_keys=True) == json.dumps(audit(events, transcript, score_report, runner_result, llm_log, log_utc_offset="+08:00"), ensure_ascii=False, sort_keys=True)


def test_unscoped_cumulative_log_does_not_claim_zero(tmp_path: Path) -> None:
    events, transcript, score_report, runner_result, llm_log = _fixtures(tmp_path)
    summary = audit(events, transcript, score_report, runner_result, llm_log)
    assert summary["adherence_evidence"]["compression"]["status"] == "PARTIAL"
    assert summary["adherence_evidence"]["compression"]["count"] == "UNKNOWN"
    assert "llm_compressor_lines_without_usable_timestamp" in summary["limitations"]


def test_cli_writes_deterministic_summary(tmp_path: Path) -> None:
    events, transcript, score_report, runner_result, llm_log = _fixtures(tmp_path)
    output = tmp_path / "post_run_summary.json"
    command = [
        sys.executable, str(Path(__file__).resolve().parents[1] / "scripts" / "post_run_audit.py"),
        "--events", str(events), "--transcript", str(transcript),
        "--score-report", str(score_report), "--runner-result", str(runner_result),
        "--llm-log", str(llm_log), "--log-utc-offset", "+08:00", "--output", str(output),
    ]
    subprocess.run(command, check=True, capture_output=True, text=True)
    first = output.read_bytes()
    subprocess.run(command, check=True, capture_output=True, text=True)
    assert output.read_bytes() == first
    assert json.loads(first)["adherence_evidence"]["compression"]["count"] == 2
