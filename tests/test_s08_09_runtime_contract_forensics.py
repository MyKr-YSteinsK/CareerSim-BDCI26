"""Offline regression tests for the S08-09 frozen-run forensic parser."""

import json
from pathlib import Path

from scripts.s08_09_runtime_contract_forensics import _analyze_delivery, _read_calls, analyze


def test_delivery_taxonomy_separates_newline_false_negative_from_checkpoint_enum() -> None:
    prefix = "[CTRL G=? P=A R=PASS X=0]\n"
    actions = [
        {"index": 1, "notes": prefix + "[DL i=NONE n=0 focus=NONE evidence=NA checkpoint=0 recognition=0]"},
        {"index": 2, "notes": prefix + "[DL i=D1 n=1 focus=IN_PROGRESS evidence=UNVERIFIED checkpoint=1 recognition=0]"},
        {"index": 3, "notes": prefix + "[DL i=D2 n=1 focus=COMMITTED evidence=UNVERIFIED checkpoint=2 recognition=1]"},
    ]

    result = _analyze_delivery(actions)

    assert result["taxonomy_primary_counts"]["VALID"] == 2
    assert result["taxonomy_primary_counts"]["INVALID_CHECKPOINT"] == 1
    assert result["secondary_reason_counts"]["INVALID_ENUM"] == 1
    assert result["pre_patch_auditor_replay"] == {
        "MALFORMED_FIELD": 1,
        "MISSING": 0,
        "ORDERING_ERROR": 2,
        "VALID": 0,
    }
    assert result["post_patch_auditor_replay"] == {"malformed_or_duplicate": 1, "missing": 0, "valid": 2}


def test_event_decoder_deduplicates_runner_event_encodings(tmp_path: Path) -> None:
    call = {
        "tool_call_id": "call-1",
        "name": "mcp_career-emulator_take_action",
        "arguments": json.dumps({"session_id": "a" * 32, "choice": 1, "notes": "note"}),
    }
    result_data = {"success": True, "error": None}
    rows = [
        {"seq": 1, "kind": "tool_call", "payload": {"delta": {"tool_call": call}}},
        {"seq": 2, "kind": "tool_call", "payload": {"tool_call": call}},
        {"seq": 3, "kind": "tool_result", "payload": {"delta": {"tool_call_id": "call-1", "tool_name": call["name"], "raw_output": {"result": json.dumps(result_data)}}}},
        {"seq": 4, "kind": "tool_result", "payload": {"tool_call_id": "call-1", "tool_name": call["name"], "raw_output": {"result": json.dumps(result_data)}}},
    ]
    source = tmp_path / "events.jsonl"
    source.write_text("".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8")

    calls, results = _read_calls(source)

    assert len(calls) == 1
    assert calls[0]["seq"] == 1
    assert results["call-1"]["data"] == result_data


def test_frozen_run_forensics_reconstructs_exact_boundaries_and_m42() -> None:
    repo = Path(__file__).resolve().parents[1]

    result = analyze(repo)

    boundaries = result["fresh_state_semantics"]["boundary_records"]
    assert len(boundaries) == 18
    assert {item["classification"] for item in boundaries} == {"EXPLICIT_OBSERVE_REQUIRED_AND_MISSING"}
    assert [item["action_index"] for item in boundaries] == [61, 62, 74, 75, 87, 88, 100, 101, 113, 114, 126, 127, 139, 140, 152, 153, 165, 166]
    assert result["fresh_state_semantics"]["take_action_result_equivalents"] == 0

    delivery = result["delivery_markers"]
    assert delivery["taxonomy_primary_counts"]["VALID"] == 174
    assert delivery["taxonomy_primary_counts"]["INVALID_CHECKPOINT"] == 33
    assert delivery["field_value_counts"]["checkpoint"] == {"0": 5, "1": 169, "2": 16, "3": 10, "4": 7}

    m42 = result["m42_no_gain"]
    assert [item["action_index"] for item in m42["timeline"]] == [178, 179, 180, 181]
    assert m42["energy_output_pairs"] == [[26, 26], [26, 26], [26, 26]]
    assert m42["fresh_observe_between_each_action"] is True
    assert m42["root_cause"] == "MULTIPLE_CAUSES"
