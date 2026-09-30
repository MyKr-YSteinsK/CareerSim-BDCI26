from __future__ import annotations

import json
from pathlib import Path

from scripts.s08_11_high_score_core_forensics import RunSpec, build_report, extract_run


SESSION = "0123456789abcdef0123456789abcdef"


def _record(kind: str, call_id: str, payload: dict) -> dict:
    return {"kind": kind, "seq": 1, "payload": {**payload, "tool_call_id": call_id}}


def _call(call_id: str, name: str, arguments: dict) -> dict:
    return _record("tool_call", call_id, {"tool_call": {"tool_call_id": call_id, "name": name, "arguments": arguments}})


def _result(call_id: str, name: str, result: dict) -> dict:
    return _record("tool_result", call_id, {"tool_name": name, "raw_output": {"result": result}})


def _observe(call_id: str, month: int, title: str, status: dict, choices: list[dict]) -> list[dict]:
    result = {
        "success": True,
        "current_state": {
            "session_id": SESSION,
            "time": {"current_month": month, "current_quarter": (month + 2) // 3, "current_year": 1},
            "status": {"level": "L1", **status, "internal_score": 999, "HiddenRisk": 12345},
            "internal_payload": {"must_not_be_used": "private"},
        },
        "current_event": {"title": title, "description": "participant-visible context"},
        "choices": choices,
    }
    name = "mcp_career-emulator_observe"
    return [
        _call(call_id, name, {"session_id": SESSION}),
        _result(call_id, name, result),
    ]


def test_extracts_legal_main_and_energy_choices_with_public_deltas(tmp_path: Path) -> None:
    events = tmp_path / "events.jsonl"
    records: list[dict] = []
    records += _observe("o1", 3, "季度主行动选择", {"skill": 10, "network": 2, "output": 4, "wealth": 8}, [{"choice": 1, "action": "申请关键项目"}])
    records.append(_call("a1", "mcp_career-emulator_take_action", {"session_id": SESSION, "choice": 1, "notes": "HiddenRisk=987; ignored"}))
    records.append(_result("a1", "mcp_career-emulator_take_action", {"success": True}))
    records += _observe("o2", 3, "季度体力行动分配", {"skill": 11, "network": 2, "output": 4, "wealth": 8}, [{"choice": 0, "action": "准备汇报材料"}])
    records.append(_call("a2", "mcp_career-emulator_take_action", {"session_id": SESSION, "choice": 0, "notes": "internal_score=1000; ignored"}))
    records.append(_result("a2", "mcp_career-emulator_take_action", {"success": True}))
    records += _observe("o3", 3, "普通事件", {"skill": 11, "network": 2, "output": 5, "wealth": 8}, [])
    # Duplicate stream frames share call ids and must not inflate counts.
    records.append(_call("a2", "mcp_career-emulator_take_action", {"session_id": SESSION, "choice": 0, "notes": "duplicate"}))
    records.append(_result("a2", "mcp_career-emulator_take_action", {"success": True}))
    events.write_text("\n".join(json.dumps(record) for record in records) + "\n", encoding="utf-8")

    result = extract_run(RunSpec("v7v", events, SESSION))

    assert result["take_action_attempts_in_session"] == 2
    assert result["take_action_successes"] == 2
    assert result["observes_in_session"] == 3
    assert result["missing_action_to_observe_boundaries"] == 0
    assert result["action_mix_by_run_phase"]["main"]["periods"][0]["count"] == 1
    assert result["action_mix_by_run_phase"]["energy"]["periods"][0]["count"] == 1
    response = result["energy_public_before_after_response"][0]
    assert response["category"] == "OUTPUT_VISIBILITY"
    assert response["public_dimension"] == "output"
    assert response["observed_response"] == "GAIN"
    serialized = json.dumps(result, ensure_ascii=False)
    assert SESSION not in serialized
    assert "HiddenRisk" not in serialized
    assert "internal_score" not in serialized
    assert "987" not in serialized


def test_categories_and_period_shares_are_explicit() -> None:
    events = [
        {"kind": "main", "category": "Apply/Key Project", "label": "申请关键项目", "month": 3},
        {"kind": "main", "category": "Other", "label": "建立导师关系", "month": 6},
        {"kind": "energy", "category": "NETWORK_GROWTH", "label": "人脉维护", "month": 9},
    ]
    from scripts.s08_11_high_score_core_forensics import _category, _mix

    assert _category("主动曝光成果", "main") == "Other"
    assert _category("高强度工作", "energy") == "OTHER"
    mix = _mix(events, "main", (("M1-M6", 1, 6), ("M7-M12", 7, 12)))
    assert mix["periods"][0]["count"] == 2
    assert {item["category"]: item["share"] for item in mix["periods"][0]["categories"]} == {
        "Apply/Key Project": 0.5,
        "Other": 0.5,
    }
    assert mix["periods"][1]["count"] == 0


def test_malformed_call_without_session_arg_binds_only_to_same_session_observe(tmp_path: Path) -> None:
    events = tmp_path / "events.jsonl"
    records = _observe("o1", 3, "季度体力行动分配", {"health": 4}, [{"choice": 0, "action": "健康恢复"}])
    records.append(_call("a1", "mcp_career-emulator_take_action", {"choice": [1, 2]}))
    records.append(_result("a1", "mcp_career-emulator_take_action", {"success": False, "error": "invalid arguments"}))
    events.write_text("\n".join(json.dumps(record) for record in records) + "\n", encoding="utf-8")

    result = extract_run(RunSpec("v6", events, SESSION))

    assert result["take_action_attempts_in_session"] == 1
    assert result["take_action_successes"] == 0
    assert result["take_action_errors"] == 1
    assert result["take_action_without_session_arg"] == 1


def test_build_report_requires_the_four_explicit_run_identities(tmp_path: Path) -> None:
    empty = tmp_path / "events.jsonl"
    empty.write_text("", encoding="utf-8")
    specs = [RunSpec(name, empty, SESSION) for name in ("v6", "v7o", "v7t", "v7v")]
    report = build_report(specs)
    assert [item["run"] for item in report["runs"]] == ["v6", "v7o", "v7t", "v7v"]
    assert report["evidence_policy"] == "PUBLIC_LEGAL_CHOICES_AND_WHITELISTED_PUBLIC_STATUS_ONLY"
