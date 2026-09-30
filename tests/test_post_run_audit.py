"""Synthetic offline evidence for the WF-01 one-pass audit contract."""

import json
import subprocess
import sys
from pathlib import Path

import pytest

from scripts.post_run_audit import _read_skill, audit


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
        _call(4, 2, "a1", "mcp_career-emulator_take_action", {"choice": 1, "notes": "[CTRL G=? P=A R=PASS X=-] Proceed"}),
        _result(5, 2, "a1", "mcp_career-emulator_take_action", {"success": True}),
        _result(6, 6, "o2", "mcp_career-emulator_observe", _observe(6, 2, "半年评审")),
        _call(7, 7, "a2", "mcp__career-emulator__take_action", {"choice": 1, "notes": "[CTRL G=Output P=A R=PASS X=-] HiddenRisk-1"}),
        _result(8, 7, "a2", "mcp__career-emulator__take_action", {"success": False, "error": "Ability not found"}),
        _result(9, 9, "o3", "mcp_career-emulator_observe", _observe(24, 3, "季度主行动")),
        _call(10, 10, "a3", "mcp_career-emulator_take_action", {"choice": 1, "notes": "[CTRL G=Output P=A R=PASS X=-] Proceed"}),
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
    assert [item["overall_status"] for item in summary["adherence_evidence"]["compression"]["recovery"]] == ["RECOVERY_FAIL", "RECOVERY_FAIL"]
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


def _replace_action_notes(events: Path, notes: list[str]) -> None:
    rows = [json.loads(line) for line in events.read_text(encoding="utf-8").splitlines()]
    actions = [row for row in rows if row["kind"] == "tool_call" and "take_action" in row["payload"]["tool_call"]["name"]]
    for row, note in zip(actions, notes, strict=True):
        args = json.loads(row["payload"]["tool_call"]["arguments"])
        args["notes"] = note
        row["payload"]["tool_call"]["arguments"] = json.dumps(args)
    events.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows), encoding="utf-8")


def test_delivery_marker_states_coverage_and_pre_review_inputs(tmp_path: Path) -> None:
    events, transcript, score, runner, _ = _fixtures(tmp_path)
    prefix = "[CTRL G=? P=A R=PASS X=-] "
    _replace_action_notes(events, [
        prefix + "[DL n=0 focus=NONE evidence=NA checkpoint=0 recognition=0]",
        prefix + "[DL n=1 focus=DELIVERY_CLAIMED evidence=UNVERIFIED checkpoint=1 recognition=?]",
        prefix + "[DL n=1 focus=DELIVERED evidence=PUBLICLY_VERIFIED checkpoint=1 recognition=1]",
    ])
    summary = audit(events, transcript, score, runner)
    coverage = summary["adherence_evidence"]["delivery_marker_coverage"]
    assert coverage["status"] == "DELIVERY_MARKER_COVERAGE_PASS"
    assert (coverage["attempts"], coverage["valid"], coverage["missing"], coverage["malformed_or_duplicate"]) == (3, 3, 0, 0)
    assert [item["state"]["focus"] for item in summary["adherence_evidence"]["delivery_states_by_action"]] == ["NONE", "DELIVERY_CLAIMED", "DELIVERED"]
    assert [item["state"]["focus"] for item in summary["mechanism_inputs"]["pre_first_review_delivery_states"]] == ["NONE"]
    assert summary["mechanism_inputs"]["trigger_classification"] == "UNKNOWN_REQUIRES_SEMANTIC_AUDIT"


def test_delivery_marker_accepts_current_session_item_identity(tmp_path: Path) -> None:
    events, transcript, score, runner, _ = _fixtures(tmp_path)
    prefix = "[CTRL G=? P=A R=PASS X=-] "
    _replace_action_notes(events, [
        prefix + "[DL i=NONE n=0 focus=NONE evidence=NA checkpoint=0 recognition=0]",
        prefix + "[DL i=D1 n=1 focus=IN_PROGRESS evidence=UNVERIFIED checkpoint=1 recognition=0]",
        prefix + "[DL i=UNKNOWN n=1 focus=DELIVERY_CLAIMED evidence=UNKNOWN checkpoint=? recognition=?]",
    ])
    summary = audit(events, transcript, score, runner)
    coverage = summary["adherence_evidence"]["delivery_marker_coverage"]
    states = summary["adherence_evidence"]["delivery_states_by_action"]
    assert coverage["status"] == "DELIVERY_MARKER_COVERAGE_PASS"
    assert (coverage["valid"], coverage["identity_missing"]) == (3, 0)
    assert [item["state"]["item_id"] for item in states] == ["NONE", "D1", "UNKNOWN"]


def test_delivery_marker_accepts_contract_ordered_markers_on_separate_lines(tmp_path: Path) -> None:
    events, transcript, score, runner, _ = _fixtures(tmp_path)
    prefix = "[CTRL G=? P=A R=PASS X=-]\n"
    _replace_action_notes(events, [
        prefix + "[DL i=NONE n=0 focus=NONE evidence=NA checkpoint=0 recognition=0]",
        prefix + "[DL i=D1 n=1 focus=IN_PROGRESS evidence=UNVERIFIED checkpoint=1 recognition=0]",
        prefix + "[DL i=D2 n=1 focus=COMMITTED evidence=UNVERIFIED checkpoint=2 recognition=1]",
    ])

    coverage = audit(events, transcript, score, runner)["adherence_evidence"]["delivery_marker_coverage"]

    assert (coverage["valid"], coverage["missing"], coverage["malformed_or_duplicate"]) == (2, 0, 1)


def test_delivery_missing_malformed_duplicate_unknown_and_internal_redaction(tmp_path: Path) -> None:
    events, transcript, score, runner, _ = _fixtures(tmp_path)
    prefix = "[CTRL G=? P=A R=PASS X=-] "
    _replace_action_notes(events, [
        prefix + "[DL n=1 focus=UNKNOWN evidence=UNKNOWN checkpoint=? recognition=?]",
        prefix + "No marker",
        prefix + "[DL n=1 focus=DELIVERED evidence=PUBLICLY_VERIFIED checkpoint=1 recognition=1 HiddenRisk=999] [DL n=0 focus=NONE evidence=NA checkpoint=0 recognition=0]",
    ])
    summary = audit(events, transcript, score, runner)
    coverage = summary["adherence_evidence"]["delivery_marker_coverage"]
    assert coverage["status"] == "DELIVERY_MARKER_COVERAGE_FAIL"
    assert (coverage["valid"], coverage["missing"], coverage["malformed_or_duplicate"]) == (1, 1, 1)
    assert summary["actions"]["evidence_discipline_categories"]["delivery_marker_internal_reference"] == 1
    assert "HiddenRisk=999" not in json.dumps(summary, ensure_ascii=False)
    assert summary["adherence_evidence"]["delivery_states_by_action"][0]["state"]["focus"] == "UNKNOWN"


def test_delivery_single_malformed_and_clean_duplicate_are_rejected(tmp_path: Path) -> None:
    events, transcript, score, runner, _ = _fixtures(tmp_path)
    prefix = "[CTRL G=? P=A R=PASS X=-] "
    empty = "[DL n=0 focus=NONE evidence=NA checkpoint=0 recognition=0]"
    _replace_action_notes(events, [prefix + empty, prefix + "[DL n=0 focus=NONE evidence=NA checkpoint=1 recognition=0]", prefix + empty + " " + empty])
    coverage = audit(events, transcript, score, runner)["adherence_evidence"]["delivery_marker_coverage"]
    assert (coverage["valid"], coverage["missing"], coverage["malformed_or_duplicate"]) == (1, 0, 2)
    assert coverage["status"] == "DELIVERY_MARKER_COVERAGE_FAIL"


def _recovery_events(events: Path, mechanism: str, count: int = 4, late: bool = False, results: bool = True, early: bool = False, failed: bool = False) -> None:
    rows = [json.loads(line) for line in events.read_text(encoding="utf-8").splitlines()]
    observe = _result(100, 9, "or", "mcp_career-emulator_observe", _observe(24, 3, "继续"))
    rows.append(observe)
    for index, skill in enumerate(("structured-state-board", "rolling-planning", "delivery-progress", "risk-review")[:count]):
        name = "skill_tool" if mechanism == "skill_tool" else "read_file"
        args = {"skill_name": skill} if mechanism == "skill_tool" else {"path": f"C:/Users/Yukis/.jiuwenswarm-instances/career_emu/agent/workspace/skills/{skill}/SKILL.md"}
        call = _call(101 + index * 2, 9, f"r{index}", name, args)
        call["ts"] = f"2026-09-28T10:{(4 if early else 9):02d}:{10 + index * 2:02d}+00:00"
        rows.append(call)
        if results:
            result = _result(102 + index * 2, 9, f"r{index}", name, {"success": not (failed and index == 3), "content": "read"})
            result["ts"] = f"2026-09-28T10:{(4 if early else 11 if late else 9):02d}:{11 + index * 2:02d}+00:00"
            rows.append(result)
    events.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows), encoding="utf-8")


def test_recovery_accepts_structured_skill_tool_and_exact_read_file(tmp_path: Path) -> None:
    for mechanism in ("skill_tool", "read_file"):
        folder = tmp_path / mechanism
        folder.mkdir()
        events, transcript, score, runner, log = _fixtures(folder)
        _recovery_events(events, mechanism)
        summary = audit(events, transcript, score, runner, log, log_utc_offset="+08:00")
        recovery = summary["adherence_evidence"]["compression"]["recovery"]
        assert [item["tool_order_status"] for item in recovery] == ["FAIL", "PASS"]
        assert [item["overall_status"] for item in recovery] == ["RECOVERY_FAIL", "TOOL_ORDER_PASS_REBUILD_UNVERIFIED"]
        assert set(recovery[-1]["rebuild_evidence"].values()) == {"UNKNOWN"}


def test_recovery_rejects_three_reads_late_reads_and_calls_without_results(tmp_path: Path) -> None:
    for label, count, late, results, early, failed in (("three", 3, False, True, False, False), ("late", 4, True, True, False, False), ("claim", 4, False, False, False, False), ("startup", 4, False, True, True, False), ("failed", 4, False, True, False, True)):
        folder = tmp_path / label
        folder.mkdir()
        events, transcript, score, runner, log = _fixtures(folder)
        _recovery_events(events, "read_file", count, late, results, early, failed)
        summary = audit(events, transcript, score, runner, log, log_utc_offset="+08:00")
        assert summary["adherence_evidence"]["compression"]["recovery"][-1]["overall_status"] == "RECOVERY_FAIL"


def test_recovery_path_must_target_exact_installed_skill_file() -> None:
    root = "C:/Users/Yukis/.jiuwenswarm-instances/career_emu/agent/workspace/skills"
    assert _read_skill("read_file", {"path": root + "/risk-review/SKILL.md"}) == "risk-review"
    for path in (root, root + "/risk-review", root + "/risk-review/README.md", root + "/risk-review/SKILL.md.bak", "skills/risk-review/SKILL.md", root + "/../skills/risk-review/SKILL.md"):
        assert _read_skill("read_file", {"path": path}) is None
    assert _read_skill("read_file", {"note": root + "/risk-review/SKILL.md"}) is None


def test_ctrl_closure_accepts_ordinary_unknown_and_reconsidered_paths(tmp_path: Path) -> None:
    events, transcript, score, runner, _ = _fixtures(tmp_path)
    _replace_action_notes(events, [
        "[CTRL G=? P=A R=PASS X=-] Proceed",
        "[CTRL G=? P=A R=PASS X=1] Proceed",
        "[CTRL G=? P=A R=UNKNOWN X=-] Proceed",
    ])
    closure = audit(events, transcript, score, runner)["actions"]["ctrl_closure"]
    assert closure["status"] == "CTRL_CLOSURE_PASS"
    assert closure["valid"] == 3


def test_ctrl_closure_rejects_incomplete_contradictory_and_malformed_paths(tmp_path: Path) -> None:
    events, transcript, score, runner, _ = _fixtures(tmp_path)
    _replace_action_notes(events, [
        "[CTRL G=? P=A R=PASS X=0] Incomplete",
        "[CTRL G=? P=A R=RECONSIDER X=1] Nonfinal",
        "[CTRL G=? P=A R=RECONSIDER X=-] Nonfinal",
    ])
    closure = audit(events, transcript, score, runner)["actions"]["ctrl_closure"]
    assert closure["status"] == "CTRL_CLOSURE_FAIL"
    assert closure["submitted_incomplete_x0"] == 1
    assert closure["submitted_nonfinal_r_reconsider"] == 2
    _replace_action_notes(events, ["[CTRL broken]", "[CTRL G=? P=A R=PASS X=-] [CTRL duplicate]", "[CTRL G=? P=A R=UNKNOWN X=-]"])
    closure = audit(events, transcript, score, runner)["actions"]["ctrl_closure"]
    assert closure["status"] == "CTRL_CLOSURE_FAIL"
    assert closure["malformed_or_missing_ctrl"] == 2


def test_closed_delivery_focus_is_not_active(tmp_path: Path) -> None:
    events, transcript, score, runner, _ = _fixtures(tmp_path)
    prefix = "[CTRL G=? P=A R=PASS X=-] "
    _replace_action_notes(events, [
        prefix + "[DL n=0 focus=NONE evidence=NA checkpoint=0 recognition=0]",
        prefix + "[DL n=1 focus=CLOSED evidence=PUBLICLY_VERIFIED checkpoint=0 recognition=1]",
        prefix + "[DL n=0 focus=CLOSED evidence=PUBLICLY_VERIFIED checkpoint=0 recognition=1]",
    ])
    coverage = audit(events, transcript, score, runner)["adherence_evidence"]["delivery_marker_coverage"]
    assert (coverage["valid"], coverage["malformed_or_duplicate"]) == (1, 2)


def test_same_month_delivery_actions_use_review_event_order(tmp_path: Path) -> None:
    events, transcript, score, runner, _ = _fixtures(tmp_path)
    rows = [json.loads(line) for line in events.read_text(encoding="utf-8").splitlines()]
    first_observe = next(row for row in rows if row["kind"] == "tool_result" and row["payload"].get("tool_call_id") == "o1")
    data = json.loads(first_observe["payload"]["raw_output"]["result"])
    data["current_state"]["time"]["current_month"] = 6
    data["current_event"]["title"] = "项目进展"
    first_observe["payload"]["raw_output"]["result"] = json.dumps(data, ensure_ascii=False)
    events.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows), encoding="utf-8")
    marker = "[DL n=0 focus=NONE evidence=NA checkpoint=0 recognition=0]"
    _replace_action_notes(events, ["[CTRL G=? P=A R=PASS X=-] " + marker] * 3)
    summary = audit(events, transcript, score, runner)
    assert summary["mechanism_inputs"]["first_formal_review_month"] == 6
    assert [item["action_index"] for item in summary["mechanism_inputs"]["pre_first_review_delivery_states"]] == [1]
    assert [item["month"] for item in summary["mechanism_inputs"]["pre_first_review_delivery_states"]] == [6]
    assert summary["mechanism_inputs"]["trigger_classification"] == "UNKNOWN_REQUIRES_SEMANTIC_AUDIT"


def test_final_r_and_independent_x_marker_combinations(tmp_path: Path) -> None:
    for risk in ("PASS", "ALLOW", "WARN", "UNKNOWN"):
        for x in ("-", "1"):
            folder = tmp_path / f"{risk}-{x}"
            folder.mkdir()
            events, transcript, score, runner, _ = _fixtures(folder)
            note = f"[CTRL G=Output P=A R={risk} X={x}] Proceed"
            _replace_action_notes(events, [note] * 3)
            closure = audit(events, transcript, score, runner)["actions"]["ctrl_closure"]
            assert closure["status"] == "CTRL_CLOSURE_PASS"
            assert closure["valid"] == 3
            assert closure["basis"] == "MARKER_CONSISTENCY_ONLY"


def test_ctrl_v2_rb_states_and_named_delivery_checkpoints(tmp_path: Path) -> None:
    events, transcript, score, runner, _ = _fixtures(tmp_path)
    _replace_action_notes(events, [
        "[CTRL G=? P=A R=PASS RB=NONE]\n[DL i=NONE n=0 focus=NONE evidence=NA checkpoint=NOT_NEAR recognition=0]",
        "[CTRL G=Output P=A R=ALLOW RB=DONE] [DL i=D1 n=1 focus=COMMITTED evidence=UNVERIFIED checkpoint=NEAR recognition=0]",
        "[CTRL G=Output P=A R=PASS RB=BLOCKED] [DL i=D2 n=1 focus=IN_PROGRESS evidence=UNKNOWN checkpoint=UNKNOWN recognition=?]",
    ])
    summary = audit(events, transcript, score, runner)
    closure = summary["actions"]["ctrl_closure"]
    actions = summary["actions"]
    coverage = summary["adherence_evidence"]["delivery_marker_coverage"]

    assert closure["status"] == "CTRL_CLOSURE_FAIL"
    assert closure["valid"] == 2
    assert closure["submitted_blocked_rb"] == 1
    assert [item["RB"] for item in actions["ctrl_states_by_action"]] == ["NONE", "DONE", "BLOCKED"]
    assert actions["ctrl_trajectory"]["RB_counts"] == {"BLOCKED": 1, "DONE": 1, "NONE": 1}
    assert coverage["valid"] == 3
    assert [item["state"]["checkpoint"] for item in summary["adherence_evidence"]["delivery_states_by_action"]] == [
        "NOT_NEAR", "NEAR", "UNKNOWN"
    ]


def test_ctrl_v2_reconsider_remains_nonfinal_even_with_done_rb(tmp_path: Path) -> None:
    events, transcript, score, runner, _ = _fixtures(tmp_path)
    _replace_action_notes(events, ["[CTRL G=? P=A R=RECONSIDER RB=DONE] Proceed"] * 3)
    closure = audit(events, transcript, score, runner)["actions"]["ctrl_closure"]

    assert closure["status"] == "CTRL_CLOSURE_FAIL"
    assert closure.get("valid", 0) == 0
    assert closure["submitted_nonfinal_r_reconsider"] == 3


def test_ctrl_trajectory_is_compact_deterministic_and_redacts_internal_gap(tmp_path: Path) -> None:
    events, transcript, score, runner, _ = _fixtures(tmp_path)
    _replace_action_notes(events, [
        "[CTRL G=Skill P=A R=PASS X=-] Proceed",
        "[CTRL G=Skill P=S R=ALLOW X=1] Proceed",
        "[CTRL G=Output P=A R=UNKNOWN X=-] Proceed",
    ])
    actions = audit(events, transcript, score, runner)["actions"]
    assert [(item["action_index"], item["month"], item["G"], item["P"], item["R"], item["X"]) for item in actions["ctrl_states_by_action"]] == [
        (1, 1, "Skill", "A", "PASS", "-"),
        (2, 6, "Skill", "S", "ALLOW", "1"),
        (3, 24, "Output", "A", "UNKNOWN", "-"),
    ]
    assert actions["ctrl_trajectory"] == {
        "P_counts": {"A": 2, "S": 1},
        "R_counts": {"ALLOW": 1, "PASS": 1, "UNKNOWN": 1},
        "X_counts": {"-": 2, "1": 1},
        "G_change_count": 1,
        "G_values_in_order": ["Skill", "Skill", "Output"],
        "G_semantic_justification": "NOT_INFERRED",
    }
    assert "ctrl_x1_branch_use_not_independently_verified" in audit(events, transcript, score, runner)["limitations"]
    _replace_action_notes(events, [
        "[CTRL G=Skill P=A R=PASS X=-] Proceed",
        "[CTRL G=HiddenRisk-999 P=A R=PASS X=-] Proceed",
        "[CTRL G=Output P=A R=PASS X=-] Proceed",
    ])
    summary = audit(events, transcript, score, runner)
    assert summary["actions"]["ctrl_states_by_action"][1]["G"] == "REDACTED_INTERNAL_REFERENCE"
    assert "HiddenRisk-999" not in json.dumps(summary, ensure_ascii=False)


def test_compressor_microseconds_distinguish_events_and_exact_duplicate_dedups(tmp_path: Path) -> None:
    events, transcript, score, runner, log = _fixtures(tmp_path)
    old = "".join(f"2026-09-27 18:00:{second:02d} CurrentRoundCompressor\n" for second in range(23))
    first = "2026-09-28 18:08:00.340444 CurrentRoundCompressor completed\n"
    second = "2026-09-28 18:08:00.840444 CurrentRoundCompressor completed\n"
    log.write_text(old + first + first + second, encoding="utf-8")
    compression = audit(events, transcript, score, runner, log, log_utc_offset="+08:00")["adherence_evidence"]["compression"]
    assert compression["count"] == 2
    assert compression["events_utc"] == ["2026-09-28T10:08:00.340444+00:00", "2026-09-28T10:08:00.840444+00:00"]


def test_recovery_ready_text_cannot_upgrade_tool_order_to_full_recovery(tmp_path: Path) -> None:
    events, transcript, score, runner, log = _fixtures(tmp_path)
    _recovery_events(events, "read_file")
    with transcript.open("a", encoding="utf-8") as handle:
        handle.write("RECOVERY_READY Board rebuilt Delivery rebuilt Review Plan restored\n")
    recovery = audit(events, transcript, score, runner, log, log_utc_offset="+08:00")["adherence_evidence"]["compression"]["recovery"][-1]
    assert recovery["tool_order_status"] == "PASS"
    assert recovery["overall_status"] == "TOOL_ORDER_PASS_REBUILD_UNVERIFIED"
    assert set(recovery["rebuild_evidence"].values()) == {"UNKNOWN"}


def test_partial_without_score_deduplicates_and_preserves_audits(tmp_path: Path) -> None:
    events, transcript, score, runner, _ = _fixtures(tmp_path)
    rows = [json.loads(line) for line in events.read_text(encoding="utf-8").splitlines()]
    rows[-1] = _result(12, 11, "o4", "mcp_career-emulator_observe", _observe(20, 3, "仍在进行"))
    data = json.loads(rows[-1]["payload"]["raw_output"]["result"])
    data["current_state"]["simulation_flags"].update(alive=True, failed=False)
    rows[-1]["payload"]["raw_output"]["result"] = json.dumps(data)
    earlier = next(row for row in rows if row["payload"].get("tool_call_id") == "o3")
    earlier["payload"]["raw_output"]["result"] = json.dumps(_observe(18, 3, "季度主行动"))
    events.write_text("".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8")
    marker = "[CTRL G=? P=A R=PASS X=-] [DL n=0 focus=NONE evidence=NA checkpoint=0 recognition=0]"
    _replace_action_notes(events, [marker] * 3)
    rows = [json.loads(line) for line in events.read_text(encoding="utf-8").splitlines()]
    duplicates = [{**row, "payload": {"delta": row["payload"]}} for row in rows]
    events.write_text("".join(json.dumps(row) + "\n" for row in rows + duplicates), encoding="utf-8")
    runner.write_text('{"exit_code": 1}', encoding="utf-8")
    score.unlink()
    summary = audit(events, transcript, None, runner)
    assert summary["run"]["session_id"] == SESSION
    assert summary["run"]["new_game_count"] == 1
    assert summary["run"]["observe_count"] == 4
    assert summary["run"]["events_identity"] == "PASS"
    assert summary["actions"]["attempts"] == 3
    assert summary["actions"]["ctrl_closure"]["valid"] == 3
    assert summary["adherence_evidence"]["delivery_marker_coverage"]["valid"] == 3
    assert summary["outcome"]["classification"] == "PARTIAL_GAMEPLAY_TECHNICAL_FAILURE"
    assert summary["outcome"]["max_month"] == 20
    assert summary["outcome"]["natural_terminal_observed"] is False
    assert summary["outcome"]["last_observe_alive"] is True
    assert summary["outcome"]["terminal_fresh_score"] == "UNKNOWN"
    assert summary["outcome"]["score_report_session_field"] == "MISSING"
    assert summary["usage"]["total_tokens"] == "UNKNOWN"
    assert "score_report" not in summary["inputs"]
    output = tmp_path / "partial.json"
    subprocess.run([sys.executable, str(Path(__file__).resolve().parents[1] / "scripts/post_run_audit.py"), "--events", str(events), "--transcript", str(transcript), "--runner-result", str(runner), "--output", str(output)], check=True, capture_output=True)
    assert json.loads(output.read_text(encoding="utf-8")) == summary


def test_partial_session_mismatch_cannot_claim_valid_partial(tmp_path: Path) -> None:
    events, transcript, _, runner, _ = _fixtures(tmp_path)
    runner.write_text('{"exit_code": 1}', encoding="utf-8")
    transcript.write_text("SESSION=" + "b" * 32, encoding="utf-8")
    summary = audit(events, transcript, None, runner)
    assert summary["run"]["transcript_identity"] == "MISMATCH"
    assert summary["outcome"]["classification"] == "UNKNOWN"


def _screening_stop_fixtures(tmp_path: Path) -> tuple[Path, Path, Path, Path, Path]:
    events, transcript, score, runner, _ = _fixtures(tmp_path)
    rows = [json.loads(line) for line in events.read_text(encoding="utf-8").splitlines()]
    last_observe = rows[-1]
    data = _observe(24, 3, "半年绩效评审")
    data["current_state"]["simulation_flags"].update(alive=True, failed=False)
    last_observe["payload"]["raw_output"]["result"] = json.dumps(data, ensure_ascii=False)
    events.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows), encoding="utf-8")
    score.unlink()
    runner.write_text('{"exit_code": 0}', encoding="utf-8")
    metadata = tmp_path / "screening-stop.json"
    metadata.write_text(json.dumps({
        "schema_version": 1,
        "classification": "SCREENING_STOP_CENSORED",
        "decision": "STOP_SCREENING",
        "session_id": SESSION,
        "checkpoint_month": 24,
        "checkpoint_complete": True,
        "stop_month": 24,
        "continued_to_m48": False,
        "reason": "CLEARLY_BEHIND_NO_MATERIAL_COUNTERSIGNAL",
    }), encoding="utf-8")
    return events, transcript, runner, score, metadata


def test_screening_stop_is_censored_and_keeps_score_unknown(tmp_path: Path) -> None:
    events, transcript, runner, _, metadata = _screening_stop_fixtures(tmp_path)
    summary = audit(events, transcript, None, runner, screening_metadata=metadata)
    assert summary["run"]["session_id"] == SESSION
    assert summary["run"]["runner_exit_code"] == 0
    assert summary["outcome"]["classification"] == "SCREENING_STOP_CENSORED"
    assert summary["outcome"]["max_month"] == 24
    assert summary["outcome"]["last_observe_alive"] is True
    assert summary["outcome"]["last_observe_failed"] is False
    assert summary["outcome"]["natural_terminal_observed"] is False
    assert summary["outcome"]["terminal_fresh_score"] == "UNKNOWN"
    assert summary["screening"]["continued_to_m48"] is False
    assert summary["screening"]["checkpoint_month"] == 24
    assert summary["actions"]["ctrl"]["attempts"] == 3
    assert summary["adherence_evidence"]["delivery_marker_coverage"]["attempts"] == 3
    assert "screening_metadata_does_not_prove_safe_runtime_stop" in summary["limitations"]
    output = tmp_path / "screened-partial.json"
    subprocess.run([
        sys.executable,
        str(Path(__file__).resolve().parents[1] / "scripts" / "post_run_audit.py"),
        "--events", str(events), "--transcript", str(transcript), "--runner-result", str(runner),
        "--screening-metadata", str(metadata), "--output", str(output),
    ], check=True, capture_output=True, text=True)
    assert json.loads(output.read_text(encoding="utf-8")) == summary


def test_screening_stop_rejects_mismatched_session_and_natural_terminal(tmp_path: Path) -> None:
    events, transcript, runner, _, metadata = _screening_stop_fixtures(tmp_path)
    payload = json.loads(metadata.read_text(encoding="utf-8"))
    payload["session_id"] = "b" * 32
    metadata.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(ValueError, match="session_id must match"):
        audit(events, transcript, None, runner, screening_metadata=metadata)

    payload["session_id"] = SESSION
    metadata.write_text(json.dumps(payload), encoding="utf-8")
    rows = [json.loads(line) for line in events.read_text(encoding="utf-8").splitlines()]
    data = json.loads(rows[-1]["payload"]["raw_output"]["result"])
    data["current_event"]["title"] = "普通工作"
    rows[-1]["payload"]["raw_output"]["result"] = json.dumps(data, ensure_ascii=False)
    events.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows), encoding="utf-8")
    with pytest.raises(ValueError, match="M24 review before the latest M24 state"):
        audit(events, transcript, None, runner, screening_metadata=metadata)

    data["current_event"]["title"] = "半年绩效评审"
    data["current_state"]["simulation_flags"].update(alive=False, failed=True)
    rows[-1]["payload"]["raw_output"]["result"] = json.dumps(data, ensure_ascii=False)
    events.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows), encoding="utf-8")
    with pytest.raises(ValueError, match="nonterminal alive public state"):
        audit(events, transcript, None, runner, screening_metadata=metadata)

    data["current_state"]["simulation_flags"].update(alive=True, failed=False)
    rows[-1]["payload"]["raw_output"]["result"] = json.dumps(data, ensure_ascii=False)
    events.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows), encoding="utf-8")
    runner.write_text('{"exit_code": 1}', encoding="utf-8")
    with pytest.raises(ValueError, match="Runner exit_code=0"):
        audit(events, transcript, None, runner, screening_metadata=metadata)


def test_public_review_feed_and_energy_are_not_confused_with_main(tmp_path: Path) -> None:
    events, transcript, score, runner, _ = _fixtures(tmp_path)
    rows = [json.loads(line) for line in events.read_text(encoding="utf-8").splitlines()]
    row = next(row for row in rows if row["payload"].get("tool_call_id") == "o2")
    data = json.loads(row["payload"]["raw_output"]["result"])
    data["current_event"]["title"] = "季度体力行动分配"
    data["events"] = "【半年谈话】整体达标，亮点不突出。半年绩效奖金（C）"
    data["choices"][0]["action"] = "健康恢复"
    row["payload"]["raw_output"]["result"] = json.dumps(data, ensure_ascii=False)
    events.write_text("".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8")
    with transcript.open("a", encoding="utf-8") as handle:
        handle.write("HiddenRisk=999")
    summary = audit(events, transcript, score, runner)
    assert summary["mechanism_inputs"]["first_formal_review_month"] == 6
    assert summary["trajectory"]["quarterly_main_actions"] == [{"month": 24, "action": "申请关键项目", "source": "public_choice"}]
    assert summary["adherence_evidence"]["transcript_evidence_discipline_categories"]["numeric_hiddenrisk_reference"] == 1
    assert "HiddenRisk=999" not in json.dumps(summary)


def test_explicit_missing_score_path_is_not_silently_ignored(tmp_path: Path) -> None:
    events, transcript, score, runner, _ = _fixtures(tmp_path)
    score.unlink()
    with pytest.raises(FileNotFoundError):
        audit(events, transcript, score, runner)
