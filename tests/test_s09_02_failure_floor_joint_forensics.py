"""Synthetic public-only fixtures; no runtime/provider access."""
import json

import pytest

from scripts.s09_02_failure_floor_joint_forensics import envelope, extract_records

SID = "a" * 32


def record(seq, kind, call_id, name, value):
    node = ({"tool_call": {"tool_call_id": call_id, "name": name, "arguments": json.dumps(value)}}
            if kind == "tool_call" else
            {"tool_call_id": call_id, "tool_name": name, "raw_output": {"result": value}})
    return {"seq": seq, "kind": kind, "payload": node}


def observed(h=5, w=5, month=1, level="L1", energy=0):
    return {"current_state": {"session_id": SID,
                             "time": {"current_month": month},
                             "status": {"health": h, "wealth": w, "level": level, "energy": energy,
                                        "private_hidden_value": 998},
                             "simulation_flags": {"private_flag": "DO_NOT_COPY"}},
            "current_event": {"title": "普通故事", "description": "公开内容", "document": "DO_NOT_COPY"},
            "choices": [{"choice": 7, "action": "合法选项",
                         "status_updates": {"private_effect": "DO_NOT_COPY"}}],
            "events": [{"private_history": "DO_NOT_COPY"}]}


def stream(before, after, receipt=True, batch=False, explicit=True):
    result = [
        record(1, "tool_call", "o1", "observe", {"session_id": SID}),
        record(2, "tool_result", "o1", "observe", before),
        record(3, "tool_call", "a1", "take_action",
               {"choice": 7, **({"session_id": SID} if explicit else {})}),
        record(4, "tool_result", "a1", "take_action", {"success": receipt}),
    ]
    if batch:
        result += [record(5, "tool_call", "a2", "take_action", {"session_id": SID, "choice": 7}),
                   record(6, "tool_result", "a2", "take_action", {"success": True})]
    result += [record(7, "tool_call", "o2", "observe", {"session_id": SID}),
               record(8, "tool_result", "o2", "observe", after)]
    return result


@pytest.mark.parametrize("after,kind,loss", [
    (observed(h=3), "ACTION_ATTRIBUTABLE", 2),
    (observed(), "ACTION_ATTRIBUTABLE", None),
    (observed(h=7), "ACTION_ATTRIBUTABLE", None),
    (observed(h=2, month=2), "MIXED_OR_UNATTRIBUTABLE", None),
    (observed(h=2, level="L2"), "MIXED_OR_UNATTRIBUTABLE", None),
    (observed(h=0, energy=3), "MIXED_OR_UNATTRIBUTABLE", None),
])
def test_pair_and_terminal(after, kind, loss):
    run = extract_records(stream(observed(), after), SID, after["current_state"]["time"]["current_month"])
    row = run["actions"][0]
    assert row["attribution"] == kind
    assert row["immediate_terminal"] is True
    stats = envelope({"fixture": run}, "health")
    assert stats["observed_max_loss"] == loss
    if loss:
        assert len(stats["terminal_negative"]) == 1
    if kind == "MIXED_OR_UNATTRIBUTABLE":
        assert len(stats["mixed_terminal_negative"]) == 1


def test_missing_dimension_is_not_zero():
    after = observed()
    del after["current_state"]["status"]["health"]
    run = extract_records(stream(observed(), after), SID, 1)
    stats = envelope({"fixture": run}, "health")
    assert stats["attributable_n"] == 0
    assert stats["zero_n"] == 0 and stats["unknown_n"] == 1


@pytest.mark.parametrize("kwargs", [{"receipt": None}, {"explicit": False}, {"batch": True}])
def test_ambiguous_receipt_session_and_batch(kwargs):
    run = extract_records(stream(observed(), observed(h=1), **kwargs), SID, 1)
    assert envelope({"fixture": run}, "health")["attributable_n"] == 0


def test_duplicate_frames_and_private_exclusion():
    rows = stream(observed(), observed(h=3))
    rows = [r for r in rows for _ in (0, 1)]
    run = extract_records(rows, SID, 1)
    assert run["attempted"] == 1 and run["observes"] == 2
    assert run["actions"][0]["action"] == "合法选项"  # explicit choice ID, not list index
    content = json.dumps(run)
    for forbidden in ("private_", "DO_NOT_COPY", SID, "simulation_flags", "status_updates"):
        assert forbidden not in content


def test_session_mismatch_stops():
    after = observed()
    after["current_state"]["session_id"] = "b" * 32
    with pytest.raises(ValueError, match="session differs"):
        extract_records(stream(observed(), after), SID, 1)


def test_missing_time_and_late_receipt_not_clean():
    # Direct classifier evidence: no month is not a stable-month boundary.
    from scripts.s09_02_failure_floor_joint_forensics import classify_pair
    before = {"month": None, "status": {"level": "L1"}, "title": ""}
    assert classify_pair(before, before, 1, "SUCCESS", True)[0] == "UNKNOWN"
    rows = stream(observed(), observed(h=3))
    rows[3]["seq"] = 9
    assert extract_records(rows, SID, 1)["actions"][0]["attribution"] == "UNKNOWN"


def test_quantile_small_sample_and_unknown_result():
    run = extract_records(stream(observed(), observed(w=1), receipt=None), SID, 1)
    assert envelope({"fixture": run}, "wealth")["unknown_n"] == 1
    run = extract_records(stream(observed(), observed(w=1)), SID, 1)
    assert envelope({"fixture": run}, "wealth")["loss_quantiles"] == {}
