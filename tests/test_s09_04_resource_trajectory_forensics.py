"""Synthetic exact-source/public-menu tests; no simulator/provider imports."""
import hashlib
import json

import pytest

from scripts.s09_04_resource_trajectory_forensics import (
    public_timeline, validate_window, verified_bytes,
)

SID = "a" * 32


def record(seq, kind, call_id, name, value):
    node = ({"tool_call": {"tool_call_id": call_id, "name": name, "arguments": json.dumps(value)}}
            if kind == "tool_call" else
            {"tool_call_id": call_id, "tool_name": name, "raw_output": {"result": value}})
    return {"seq": seq, "kind": kind, "payload": node}


def observe(health=3, month=1):
    return {
        "current_state": {"session_id": SID, "time": {"current_month": month},
                          "status": {"health": health, "wealth": 2, "energy": 2, "level": "L1", "private_stat": 999},
                          "simulation_flags": {"private_flag": "DO_NOT_COPY"}},
        "current_event": {"title": "公开工作场景", "description": "当前已知需要额外加班", "event_id": "DO_NOT_COPY"},
        "choices": [
            {"choice": 7, "action": "继续关键工作", "description": "公开成长语义", "status_updates": {"private_effect": "DO_NOT_COPY"}},
            {"choice": 9, "action": "休息", "description": "公开恢复语义", "private_cost": "DO_NOT_COPY"},
        ],
        "score": {"internal_score": "DO_NOT_COPY"},
    }


def stream(after=None):
    return [
        record(1, "tool_call", "o1", "observe", {"session_id": SID}),
        record(2, "tool_result", "o1", "observe", observe()),
        record(3, "tool_call", "a1", "take_action", {"session_id": SID, "choice": 7,
               "notes": "[CTRL G=SURVIVAL P=S R=PASS RB=NONE] RECOVERY=RESOURCE private_reasoning DO_NOT_COPY"}),
        record(4, "tool_result", "a1", "take_action", {"success": True}),
        record(5, "tool_call", "o2", "observe", {"session_id": SID}),
        record(6, "tool_result", "o2", "observe", after or observe(health=2)),
    ]


def test_menu_and_public_only_projection():
    row = public_timeline(stream(), SID, 1)["decision_rows"][0]
    assert row["choice"] == {"action": "继续关键工作", "description": "公开成长语义"}
    assert row["legal_choices"][1] == {"action": "休息", "description": "公开恢复语义"}
    assert (row["mode"], row["risk"], row["recovery"]) == ("S", "PASS", "RESOURCE")
    assert row["source_seq"] == {"pre_observe": 2, "action": 3, "post_observe": 6}
    dumped = json.dumps(row)
    for token in (SID, "DO_NOT_COPY", "private_", "internal_score", "event_id", "status_updates", "simulation_flags"):
        assert token not in dumped
    assert "intervention" not in row and "fragility" not in row  # semantic review is external


@pytest.mark.parametrize("month,expected", [(1, "CLEAN"), (2, "MIXED")])
def test_attribution_not_temporal_causality(month, expected):
    row = public_timeline(stream(observe(health=0, month=month)), SID, month)["decision_rows"][0]
    assert row["delta_class"] == expected
    assert row["delta_health"] == -3


def test_duplicate_transport_and_newest_menu():
    records = stream()
    records += [record(7, "tool_call", "a2", "take_action", {"session_id": SID, "choice": 9}),
                record(8, "tool_result", "a2", "take_action", {"success": True}),
                record(9, "tool_call", "o3", "observe", {"session_id": SID}),
                record(10, "tool_result", "o3", "observe", observe(health=4))]
    records[5]["payload"]["raw_output"]["result"]["choices"][1]["action"] = "新的休息菜单"
    run = public_timeline([r for r in records for _ in (0, 1)], SID, 1)
    assert run["actions"] == 2 and run["observes"] == 3
    assert run["decision_rows"][1]["choice"]["action"] == "新的休息菜单"
    assert run["decision_rows"][1]["source_seq"]["pre_observe"] == 6


def test_missing_post_observation_is_unknown_and_legacy_markers_unknown():
    rows = stream()[:4]
    del rows[2]["payload"]["tool_call"]["arguments"]
    row = public_timeline(rows, SID, 1)["decision_rows"][0]
    assert row["delta_class"] == "UNKNOWN" and row["post"] is None
    assert row["choice"] is None
    assert row["mode"] == row["recovery"] == row["risk"] == "UNKNOWN"


def test_session_mismatch_stops():
    records = stream()
    records[5]["payload"]["raw_output"]["result"]["current_state"]["session_id"] = "b" * 32
    with pytest.raises(ValueError, match="session"):
        public_timeline(records, SID, 1)


def test_hash_and_byte_identity(tmp_path):
    path = tmp_path / "source.json"
    path.write_bytes(b"exact")
    digest = hashlib.sha256(b"exact").hexdigest()
    assert verified_bytes(path, 5, digest) == b"exact"
    with pytest.raises(ValueError, match="identity mismatch"):
        verified_bytes(path, 6, digest)
    with pytest.raises(ValueError, match="identity mismatch"):
        verified_bytes(path, 5, "0" * 64)


def test_exact_window_excludes_missing_naive_or_out_of_window():
    window = ("2026-09-30T13:11:04+00:00", "2026-09-30T13:14:17+00:00")
    validate_window([{"ts": window[0]}, {"ts": window[1]}], window)
    for bad in ({}, {"ts": "2026-09-30T13:11:04"}, {"ts": "2026-09-30T13:15:00+00:00"}):
        with pytest.raises(ValueError):
            validate_window([bad], window)


def test_batch_not_clean_and_bool_not_a_menu_id():
    records = stream()
    records[1]["payload"]["raw_output"]["result"]["choices"].append({"choice": True, "action": "DO_NOT_COPY"})
    records[4:4] = [record(4.1, "tool_call", "a2", "take_action", {"session_id": SID, "choice": 9}),
                    record(4.2, "tool_result", "a2", "take_action", {"success": True})]
    run = public_timeline(records, SID, 1)
    assert run["delta_class_counts"]["MIXED"] == 2
    assert "DO_NOT_COPY" not in json.dumps(run)
