"""Offline integrity tests for deduplication, boundaries and evidence firewall."""
import hashlib
import json

import pytest

from scripts.build_policy_transition_dataset import parse_run, phase, text_signals


SID = "a" * 32


def fixture(tmp_path, *, success=True, string_choice=False, duplicate=True, final_observe=True):
    rows = []

    def call(cid, name, args):
        row = {"kind": "tool_call", "seq": len(rows) + 1, "payload": {"tool_call": {"tool_call_id": cid, "name": name, "arguments": args}}}
        rows.append(row)
        if duplicate:
            rows.append(row)

    def result(cid, name, data):
        row = {"kind": "tool_result", "seq": len(rows) + 1, "payload": {"tool_call_id": cid, "tool_name": name, "raw_output": {"result": json.dumps(data, ensure_ascii=False)}}}
        rows.append(row)
        if duplicate:
            rows.append(row)

    def observe(month, level, output, feed="", terminal=False):
        data = {"current_state": {"session_id": SID, "time": {"current_month": month, "current_quarter": 2}, "status": {"level": level, "duration_in_level": 5, "output": output, "health": 5, "skill": 9, "network": 3, "wealth": 2, "dignity": 10, "energy": 3, "HiddenRisk": 987654}, "simulation_flags": {"alive": not terminal, "failed": terminal}}, "current_event": {"title": "公共事件", "description": "项目准备中", "internal_event_id": "NEVER_COPY"}, "choices": [{"choice": 1, "action": "准备汇报材料", "energy_cost": 1, "status_updates": {"Output": 1, "HiddenRisk": 1}}], "events": feed}
        if terminal:
            data["ending_score"] = {"quantitative_score": 60.0, "survival_months": 6, "outcome": "eliminated", "completed": False}
        return data

    result("n", "new_game", {"session_id": SID})
    result("o1", "observe", observe(5, "L1", 2))
    call("a1", "take_action", {"session_id": SID, "choice": "1" if string_choice else 1})
    result("a1", "take_action", {"success": success})
    result("o2", "observe", observe(6, "L2", 3, "【半年谈话】半年绩效奖金（C）：-0.3"))
    call("a2", "take_action", {"session_id": SID, "choice": 1})
    result("a2", "take_action", {"success": True})
    if final_observe:
        result("o3", "observe", observe(6, "L2", 99, terminal=True))
    path = tmp_path / "events.jsonl"
    path.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows), encoding="utf-8")
    return {"run": "TEST", "candidate": "TEST", "events": str(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "quantitative_score": 60.0 if final_observe else None, "survival_months": 6 if final_observe else None, "final_or_last_level": "L2"}


def test_review_boundary_does_not_leak_same_month_later_actions(tmp_path):
    rows, reviews, stats = parse_run(fixture(tmp_path))
    assert len(rows) == 2 and len(reviews) == 1
    review = reviews[0]
    assert review["pre"]["O"] == 2
    assert review["first_review_state"]["O"] == 3
    assert review["pre_observe_line"] < review["trigger_action_line"] < review["post_observe_line"]
    assert review["promoted"] is True
    assert rows[-1]["post_O"] == 99
    assert rows[0]["next_review_grade"] == "C"
    assert rows[-1]["next_review_grade"] is None
    assert stats["excluded"]["duplicate_wire_calls"] == 2


def test_only_advertised_hidden_delta_and_public_whitelist(tmp_path):
    rows, reviews, _ = parse_run(fixture(tmp_path))
    encoded = json.dumps([rows, reviews])
    assert "987654" not in encoded and "NEVER_COPY" not in encoded
    assert rows[0]["advertised_HiddenRisk_delta_if_visible"] == 1
    assert "realized_HiddenRisk_delta" not in rows[0]


def test_successful_historical_string_choice_retains_original_type(tmp_path):
    rows, _, _ = parse_run(fixture(tmp_path, string_choice=True))
    assert rows[0]["selected_choice_index"] == 1
    assert rows[0]["raw_choice_argument_type"] == "str"
    assert rows[0]["official_success_with_string_choice"] is True


def test_failure_not_transition_or_trustworthy_review_pre_state(tmp_path):
    rows, reviews, stats = parse_run(fixture(tmp_path, success=False))
    assert len(rows) == 1
    assert reviews[0]["pre"] is None
    assert reviews[0]["boundary_status"] == "INSUFFICIENT_PRE_BOUNDARY"
    assert stats["excluded"]["failed_or_unknown_receipt"] == 1


def test_partial_no_post_state_or_terminal_not_imputed(tmp_path):
    rows, _, stats = parse_run(fixture(tmp_path, final_observe=False))
    assert len(rows) == 1
    assert rows[0]["terminal_within_6m"] is None
    assert stats["excluded"]["no_post_observe_at_end"] == 1
    assert stats["natural_terminal"] is False


def test_hash_mismatch_fails_closed(tmp_path):
    source = fixture(tmp_path)
    source["sha256"] = "0" * 64
    with pytest.raises(ValueError, match="hash mismatch"):
        parse_run(source)


def test_main_zero_energy_cost_is_not_energy():
    assert phase({}, [{"action": "申请关键项目", "energy_cost": 0}]) == "MAIN"


def test_generic_praise_not_concrete_result():
    assert text_signals("HR笑着说最近干得还不错，继续保持")["result_strength"] == 0
    assert text_signals("项目如期上线，业务方很满意")["result_strength"] == 3
