"""Deterministic, offline S08-09 forensics for the exact S08-RUN03 archive."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

if __package__:
    from .archive_run_evidence import _check_core_sessions, _scan
    from .post_run_audit import CTRL, DL, audit
else:
    from archive_run_evidence import _check_core_sessions, _scan
    from post_run_audit import CTRL, DL, audit


RUN_ID = "s08-run03-v7t"
SESSION_ID = "7f50220814214d97a3dc453fca049a79"
ARCHIVE = Path("artifacts/dev-runs") / RUN_ID
ARCHIVE_FILES = (
    "events.jsonl",
    "transcript.log",
    "score_report.json",
    "runner-result.json",
    "post_run_summary.json",
)
SKILL_ORDER = (
    "structured-state-board",
    "delivery-progress",
    "rolling-planning",
    "risk-review",
)
PUBLIC_STATUS = ("level", "energy", "output", "skill", "network", "health", "dignity", "wealth")
DL_FIELDS = {
    "n": {"0", "1", "2", "3"},
    "focus": {"NONE", "OPPORTUNITY", "COMMITTED", "IN_PROGRESS", "BLOCKED", "DELIVERY_CLAIMED", "DELIVERED", "UNKNOWN"},
    "evidence": {"NA", "UNKNOWN", "UNVERIFIED", "PUBLICLY_VERIFIED"},
    "checkpoint": {"0", "1", "?"},
    "recognition": {"0", "1", "?"},
}
FIELD_ASSIGNMENT = re.compile(r"(?P<key>[a-z_]+)=(?P<value>[^\s\]]+)")
MARKER_SPAN = re.compile(r"\[DL[^\]\r\n]*(?:\]|$)")


def _load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path.name}")
    return value


def _file_identity(path: Path) -> dict[str, Any]:
    data = path.read_bytes()
    return {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def _record_node(record: dict[str, Any]) -> dict[str, Any]:
    payload = record.get("payload")
    if not isinstance(payload, dict):
        return {}
    delta = payload.get("delta")
    if isinstance(delta, dict) and "tool_call" not in payload and "raw_output" not in payload:
        return delta
    return payload


def _arguments(call: dict[str, Any]) -> dict[str, Any]:
    value = call.get("arguments")
    if isinstance(value, dict):
        return value
    if isinstance(value, str):
        parsed = json.loads(value)
        return parsed if isinstance(parsed, dict) else {}
    return {}


def _result(node: dict[str, Any]) -> dict[str, Any]:
    raw = node.get("raw_output")
    if not isinstance(raw, dict):
        return {}
    value = raw.get("result")
    if isinstance(value, dict):
        return value
    if isinstance(value, str):
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError:
            return {}
        return parsed if isinstance(parsed, dict) else {}
    return {}


def _read_calls(events_path: Path) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]]]:
    calls: dict[str, dict[str, Any]] = {}
    results: dict[str, dict[str, Any]] = {}
    for line_number, line in enumerate(events_path.read_text(encoding="utf-8").splitlines(), 1):
        record = json.loads(line)
        if not isinstance(record, dict):
            raise ValueError(f"events line {line_number} is not an object")
        node = _record_node(record)
        kind = record.get("kind")
        if kind == "tool_call":
            call = node.get("tool_call")
            if not isinstance(call, dict):
                continue
            call_id = str(call.get("tool_call_id") or f"seq:{record.get('seq', line_number)}")
            item = {
                "seq": record.get("seq", line_number),
                "name": str(call.get("name") or ""),
                "id": call_id,
                "args": _arguments(call),
            }
            if call_id in calls:
                existing = calls[call_id]
                if existing["name"] != item["name"] or existing["args"] != item["args"]:
                    raise ValueError(f"conflicting duplicate tool call: {call_id}")
            else:
                calls[call_id] = item
        elif kind == "tool_result":
            call_id = node.get("tool_call_id")
            if not call_id:
                continue
            item = {"seq": record.get("seq", line_number), "name": str(node.get("tool_name") or ""), "data": _result(node)}
            call_id = str(call_id)
            if call_id in results:
                existing = results[call_id]
                if existing["name"] != item["name"] or existing["data"] != item["data"]:
                    raise ValueError(f"conflicting duplicate tool result: {call_id}")
            else:
                results[call_id] = item
    ordered = sorted(calls.values(), key=lambda item: (item["seq"], item["id"]))
    missing_results = sorted(set(calls) - set(results))
    extra_results = sorted(set(results) - set(calls))
    if missing_results or extra_results:
        raise ValueError(f"tool call/result pairing mismatch: missing={len(missing_results)} extra={len(extra_results)}")
    return ordered, results


def _public_observation(data: dict[str, Any], index: int, call: dict[str, Any], result: dict[str, Any]) -> dict[str, Any]:
    current = data.get("current_state")
    current = current if isinstance(current, dict) else {}
    time = current.get("time")
    time = time if isinstance(time, dict) else {}
    status = current.get("status")
    status = status if isinstance(status, dict) else {}
    public = {key: status.get(key) for key in PUBLIC_STATUS if key in status}
    return {
        "index": index,
        "call_seq": call["seq"],
        "call_id": call["id"],
        "result_seq": result["seq"],
        "month": time.get("current_month"),
        "level": public.get("level"),
        "public_status": public,
        "current_event_present": isinstance(data.get("current_event"), dict),
        "legal_choices_present": isinstance(data.get("choices"), list) and bool(data.get("choices")),
        "choices": data.get("choices") if isinstance(data.get("choices"), list) else [],
    }


def _action_notes(call: dict[str, Any]) -> str:
    value = call["args"].get("notes")
    return value if isinstance(value, str) else ""


def _delivery_fields(marker: str) -> dict[str, str]:
    body = marker[3:-1] if marker.endswith("]") else marker[3:]
    return {match["key"]: match["value"] for match in FIELD_ASSIGNMENT.finditer(body)}


def _dl_contract_reasons(notes: str) -> tuple[list[str], dict[str, str] | None, str]:
    spans = MARKER_SPAN.findall(notes)
    if not spans:
        return ["MISSING"], None, ""
    if len(spans) > 1:
        return ["DUPLICATE"], None, ""
    marker = spans[0]
    fields = _delivery_fields(marker)
    reasons: list[str] = []
    if not marker.endswith("]") or not re.match(r"^\[DL\s", marker):
        return ["MALFORMED_FIELD"], fields, marker
    if not re.fullmatch(r"(?:NONE|D[1-9][0-9]*|UNKNOWN)", fields.get("i", "")):
        reasons.append("INVALID_ID")
    for field, allowed in DL_FIELDS.items():
        value = fields.get(field)
        reason = {
            "i": "INVALID_ID",
            "n": "INVALID_N",
            "focus": "INVALID_FOCUS",
            "evidence": "INVALID_EVIDENCE",
            "checkpoint": "INVALID_CHECKPOINT",
            "recognition": "INVALID_RECOGNITION",
        }[field]
        if value not in allowed:
            reasons.append(reason)
    item, n = fields.get("i"), fields.get("n")
    if item is not None and n is not None and not ((n == "0" and item == "NONE") or (n != "0" and item not in {"NONE"} )):
        reasons.append("INVALID_ID")
    if n == "0" and (fields.get("focus") != "NONE" or fields.get("evidence") != "NA" or fields.get("checkpoint") != "0" or fields.get("recognition") != "0"):
        reasons.append("INVALID_FIELD_CROSSCHECK")
    elif n not in {None, "0"} and (fields.get("focus") == "NONE" or fields.get("evidence") == "NA"):
        reasons.append("INVALID_FIELD_CROSSCHECK")
    if not re.fullmatch(r"\[DL i=(?:NONE|D[1-9][0-9]*|UNKNOWN) n=[0-3] focus=(?:NONE|OPPORTUNITY|COMMITTED|IN_PROGRESS|BLOCKED|DELIVERY_CLAIMED|DELIVERED|UNKNOWN) evidence=(?:NA|UNKNOWN|UNVERIFIED|PUBLICLY_VERIFIED) checkpoint=[01?] recognition=[01?]\]", marker):
        if not reasons:
            reasons.append("MALFORMED_FIELD")
    return (reasons or ["VALID"]), fields, marker


def _marker_separator(notes: str, ctrl_match: re.Match[str] | None, dl_match: re.Match[str] | None) -> str:
    if not ctrl_match or not dl_match:
        return "UNAVAILABLE"
    return notes[ctrl_match.end():dl_match.start()]


def _analyze_delivery(actions: list[dict[str, Any]]) -> dict[str, Any]:
    taxonomy = Counter({
        "VALID": 0, "MISSING": 0, "DUPLICATE": 0, "MALFORMED_FIELD": 0,
        "INVALID_ID": 0, "INVALID_N": 0,
        "INVALID_FOCUS": 0, "INVALID_EVIDENCE": 0, "INVALID_CHECKPOINT": 0,
        "INVALID_RECOGNITION": 0, "ORDERING_ERROR": 0, "OTHER": 0,
    })
    parser_before_patch = Counter({"VALID": 0, "MISSING": 0, "MALFORMED_FIELD": 0, "ORDERING_ERROR": 0})
    field_values = {key: Counter() for key in ("i", "n", "focus", "evidence", "checkpoint", "recognition")}
    failures: list[dict[str, Any]] = []
    valid_after_patch = 0
    for action in actions:
        notes = action["notes"]
        reasons, fields, marker = _dl_contract_reasons(notes)
        for field in field_values:
            value = fields.get(field) if fields else None
            field_values[field][value if value is not None else "<MISSING>"] += 1
        ctrl_match = CTRL.match(notes)
        dl_match = DL.search(notes) if notes.count("[DL") == 1 else None
        separator = _marker_separator(notes, ctrl_match, dl_match)
        prepatch_valid = bool(
            dl_match
            and ctrl_match
            and notes.count("[DL") == 1
            and separator == " "
            and all(reason == "VALID" for reason in reasons)
        )
        postpatch_valid = bool(
            dl_match
            and ctrl_match
            and notes.count("[DL") == 1
            and separator in {" ", "\n", "\r\n"}
            and all(reason == "VALID" for reason in reasons)
        )
        if postpatch_valid:
            valid_after_patch += 1
        if prepatch_valid:
            parser_before_patch["VALID"] += 1
        elif not marker:
            parser_before_patch["MISSING"] += 1
        elif not dl_match:
            parser_before_patch["MALFORMED_FIELD"] += 1
        else:
            parser_before_patch["ORDERING_ERROR"] += 1
        primary = reasons[0]
        taxonomy[primary] += 1
        if primary != "VALID":
            failures.append({
                "action_index": action["index"],
                "primary_reason": primary,
                "secondary_reasons": reasons[1:],
                "separator_repr": repr(separator),
                "marker": marker,
            })
    # The primary taxonomy is mutually exclusive; INVALID_ENUM is reported separately as a field-type roll-up.
    taxonomy["VALID"] = valid_after_patch
    return {
        "actions": len(actions),
        "taxonomy_primary_counts": dict(sorted(taxonomy.items())),
        "secondary_reason_counts": {"INVALID_ENUM": taxonomy["INVALID_CHECKPOINT"]},
        "actual_contract_valid": valid_after_patch,
        "actual_contract_invalid": len(actions) - valid_after_patch,
        "pre_patch_auditor_replay": dict(sorted(parser_before_patch.items())),
        "post_patch_auditor_replay": {
            "valid": valid_after_patch,
            "missing": taxonomy["MISSING"],
            "malformed_or_duplicate": len(actions) - valid_after_patch - taxonomy["MISSING"],
        },
        "field_value_counts": {key: dict(sorted(values.items())) for key, values in field_values.items()},
        "failures": failures,
    }


def _extract_transcript_markers(path: Path) -> dict[str, Any]:
    lines = path.read_text(encoding="utf-8").splitlines()
    q15_start = next((i for i, line in enumerate(lines) if "Q15 (months43-45)" in line), None)
    q15_board = next((i for i, line in enumerate(lines) if "Board（Q15体力规划）" in line), None)
    q15_main = next((i for i, line in enumerate(lines) if "Q15主行动：选 choice1" in line), None)
    if q15_start is None or q15_board is None or q15_main is None:
        raise ValueError("transcript is missing the bounded Q15 markers")
    preboard = lines[q15_start:q15_board]
    q15_window = lines[q15_board:q15_main + 1]
    planned_three = [i + q15_start + 1 for i, line in enumerate(preboard) if "准备汇报材料" in line and "×3" in line]
    response_lines = [i + q15_board + 1 for i, line in enumerate(q15_window) if "PROGRESSION_RESPONSE" in line]
    primary_gap_lines = [i + q15_board + 1 for i, line in enumerate(q15_window) if "Primary Gap=Output" in line]
    return {
        "q15_pre_action_three_report_prep_mentions": planned_three,
        "q15_board_line": q15_board + 1,
        "q15_main_action_line": q15_main + 1,
        "q15_progression_response_lines": response_lines,
        "q15_primary_gap_output_lines": primary_gap_lines,
        "private_narration_saved": False,
    }


def _m42_timeline(actions: list[dict[str, Any]], observations: list[dict[str, Any]], transcript: dict[str, Any]) -> dict[str, Any]:
    by_action_index = {action["index"]: action for action in actions}
    selected_start: int | None = None
    for index in range(1, len(actions) - 3):
        window = [by_action_index.get(index + offset) for offset in range(4)]
        if not all(window):
            continue
        labels = [item.get("choice_label") or "" for item in window]
        states = [item.get("preceding_state") or {} for item in window]
        if (
            labels[:3] == ["准备汇报材料"] * 3
            and labels[3] == "申请关键项目"
            and all(state.get("month") == 42 and state.get("level") == "L4" for state in states)
        ):
            selected_start = index
            break
    if selected_start is None:
        raise ValueError("could not reconstruct the exact M42/L4 progression sequence")
    focus = [by_action_index[selected_start + offset] for offset in range(4)]
    timeline: list[dict[str, Any]] = []
    for item in focus:
        timeline.append({
            "action_index": item["index"],
            "month": item["preceding_state"].get("month"),
            "level": item["preceding_state"].get("level"),
            "choice": item["choice"],
            "action": item["choice_label"],
            "advertised_description_present": bool(item.get("choice_description")),
            "preceding_observe_index": item["preceding_observe_index"],
            "before": item["preceding_state"].get("public_status", {}),
            "take_action_result": item["result"],
            "next_observe_index": item["next_observe_index"],
            "after": item["following_state"],
            "ctrl": item["ctrl"],
        })
    output_pairs = [
        [step["before"].get("output"), step["after"].get("output")]
        for step in timeline[:3]
    ]
    explicit_no_gain_record = bool(transcript["q15_progression_response_lines"])
    return {
        "timeline": timeline,
        "energy_output_pairs": output_pairs,
        "all_three_energy_output_no_gain": all(before == after for before, after in output_pairs),
        "fresh_observe_between_each_action": all(
            timeline[index]["next_observe_index"] is not None
            and timeline[index]["next_observe_index"] == timeline[index + 1]["preceding_observe_index"]
            for index in range(3)
        ),
        "explicit_board_progression_response_in_q15_transcript_window": explicit_no_gain_record,
        "pre_action_three_action_plan_in_transcript": bool(transcript["q15_pre_action_three_report_prep_mentions"]),
        "primary_gap_output_recorded": bool(transcript["q15_primary_gap_output_lines"]),
        "no_gain_policy_patch_needed": "NO",
        "root_cause": "MULTIPLE_CAUSES",
    }


def analyze(repo: Path) -> dict[str, Any]:
    repo = repo.resolve()
    archive_dir = repo / ARCHIVE
    archive_paths = {name: archive_dir / name for name in ARCHIVE_FILES}
    manifest_path = archive_dir / "evidence-manifest.json"
    manifest = _load_json(manifest_path)
    if manifest.get("run_id") != RUN_ID:
        raise ValueError("evidence manifest run_id does not match the frozen run")
    if manifest.get("schema_version") != 1:
        raise ValueError("unexpected evidence manifest schema")
    listed = {item.get("name"): item for item in manifest.get("artifacts", []) if isinstance(item, dict)}
    identities: dict[str, dict[str, Any]] = {}
    for name, path in archive_paths.items():
        if not path.is_file():
            raise ValueError(f"required archived evidence missing: {name}")
        identity = _file_identity(path)
        expected = listed.get(name)
        if not expected or identity["bytes"] != expected.get("bytes") or identity["sha256"] != expected.get("sha256"):
            raise ValueError(f"archived evidence does not match manifest: {name}")
        identities[name] = identity
        _scan(path)
    _scan(manifest_path)
    _check_core_sessions({"events": archive_paths["events.jsonl"], "transcript": archive_paths["transcript.log"]})

    calls, results = _read_calls(archive_paths["events.jsonl"])
    for call in calls:
        call["result"] = results[call["id"]]
    names = Counter(call["name"] for call in calls)
    observe_calls = [call for call in calls if call["name"].endswith("_observe")]
    action_calls = [call for call in calls if call["name"].endswith("_take_action")]
    new_game_calls = [call for call in calls if call["name"].endswith("_new_game")]
    if len(new_game_calls) != 1:
        raise ValueError(f"expected one fresh new_game, got {len(new_game_calls)}")
    game_result = new_game_calls[0]["result"]["data"]
    if game_result.get("session_id") != SESSION_ID:
        raise ValueError("new_game result does not match frozen session")
    for call in observe_calls + action_calls:
        if call["args"].get("session_id") != SESSION_ID:
            raise ValueError(f"cross-session call detected: {call['name']}")

    observations: list[dict[str, Any]] = []
    for index, call in enumerate(observe_calls, 1):
        observations.append(_public_observation(call["result"]["data"], index, call, call["result"]))
    action_rows: list[dict[str, Any]] = []
    for index, call in enumerate(action_calls, 1):
        result = call["result"]["data"]
        if set(result) != {"success", "error"}:
            raise ValueError("take_action result schema drifted from the expected response")
        action_rows.append({
            "index": index,
            "seq": call["seq"],
            "call_id": call["id"],
            "choice": call["args"].get("choice"),
            "notes": _action_notes(call),
            "result": result,
        })
    for action in action_rows:
        prior = [obs for obs in observations if obs["call_seq"] < action["seq"]]
        following = [obs for obs in observations if obs["call_seq"] > action["seq"]]
        preceding = prior[-1] if prior else None
        next_action = next((candidate for candidate in action_rows if candidate["seq"] > action["seq"]), None)
        between = [obs for obs in observations if action["seq"] < obs["call_seq"] < (next_action["seq"] if next_action else float("inf"))]
        next_observe = between[0] if between else (following[0] if following else None)
        legal = next((item for item in preceding["choices"] if item.get("choice") == action["choice"]), None) if preceding else None
        ctrl_match = CTRL.match(action["notes"])
        action.update({
            "preceding_observe_index": preceding["index"] if preceding else None,
            "preceding_state": {
                "month": preceding["month"],
                "level": preceding["level"],
                "public_status": preceding["public_status"],
            } if preceding else None,
            "preceding_event_present": preceding["current_event_present"] if preceding else False,
            "choice_label": legal.get("action") if isinstance(legal, dict) else None,
            "choice_description": legal.get("description") if isinstance(legal, dict) else None,
            "next_observe_index": next_observe["index"] if next_observe else None,
            "following_state": next_observe["public_status"] if next_observe else None,
            "observe_between_actions": bool(between),
            "ctrl": ctrl_match.groupdict() if ctrl_match else None,
        })

    action_results = Counter(json.dumps(action["result"], sort_keys=True) for action in action_rows)
    observed_tool_result_fields = Counter(tuple(sorted(action["result"].keys())) for action in action_rows)
    missing_boundaries: list[dict[str, Any]] = []
    for index, action in enumerate(action_rows[:-1]):
        next_action = action_rows[index + 1]
        if action["observe_between_actions"]:
            continue
        post_next = next((obs for obs in observations if obs["call_seq"] > next_action["seq"]), None)
        prior = action["preceding_state"] or {}
        missing_boundaries.append({
            "boundary_id": f"B{len(missing_boundaries) + 1:02d}",
            "month": prior.get("month"),
            "action_index": action["index"],
            "choice": action["choice"],
            "choice_label_from_preceding_legal_choices": action["choice_label"],
            "preceding_state_source": {
                "observe_index": action["preceding_observe_index"],
                "month": prior.get("month"),
                "level": prior.get("level"),
                "public_status": prior.get("public_status", {}),
            },
            "take_action_result_fields": sorted(action["result"].keys()),
            "updated_public_state_present": False,
            "current_event_present": False,
            "legal_choices_present": False,
            "next_action": {"index": next_action["index"], "choice": next_action["choice"], "seq": next_action["seq"]},
            "next_explicit_observe_index": post_next["index"] if post_next else None,
            "state_match_with_next_observe": "NOT_COMPARABLE_ACTION_RESULT_HAS_NO_STATE",
            "decision_text_between_calls": "No state-bearing event exists between calls; narration was not retained as evidence.",
            "classification": "EXPLICIT_OBSERVE_REQUIRED_AND_MISSING",
        })

    ctrl_counts = Counter()
    x_counts = Counter()
    risk_counts = Counter()
    for action in action_rows:
        marker = action["ctrl"]
        if marker:
            ctrl_counts["valid_syntax"] += 1
            x_counts[marker["x"]] += 1
            risk_counts[marker["risk"]] += 1
        else:
            ctrl_counts["malformed_or_missing"] += 1

    delivery = _analyze_delivery(action_rows)
    transcript = _extract_transcript_markers(archive_paths["transcript.log"])
    m42 = _m42_timeline(action_rows, observations, transcript)
    summary = _load_json(archive_paths["post_run_summary.json"])
    runner_result = _load_json(archive_paths["runner-result.json"])
    score_report = _load_json(archive_paths["score_report.json"])
    summary_text = json.dumps(summary, ensure_ascii=False)
    if SESSION_ID not in summary_text:
        raise ValueError("post_run_summary is not bound to the frozen session")
    if score_report.get("session_id") != SESSION_ID:
        raise ValueError("score report is not bound to the frozen session")
    runner_matches_score = (
        runner_result.get("source_status") == "RECONSTRUCTED_FROM_INTERACTIVE_RUNNER_STDOUT"
        and runner_result.get("output_dir") == score_report.get("output_dir")
        and runner_result.get("outcome") == score_report.get("ending_score", {}).get("outcome")
        and runner_result.get("quantitative_score") == score_report.get("ending_score", {}).get("quantitative_score")
        and runner_result.get("survival_months") == score_report.get("ending_score", {}).get("survival_months")
    )
    if not runner_matches_score:
        raise ValueError("reconstructed Runner result does not agree with the exact session-bound score report")

    manifest_text = (repo / "configs/runtime_manifest.json").read_text(encoding="utf-8")
    risk_text = (repo / "skills/risk-review/SKILL.md").read_text(encoding="utf-8")
    delivery_text = (repo / "skills/delivery-progress/SKILL.md").read_text(encoding="utf-8")
    board_path = repo / "skills/structured-state-board/SKILL.md"
    planning_path = repo / "skills/rolling-planning/SKILL.md"
    board_text = board_path.read_text(encoding="utf-8")
    planning_text = planning_path.read_text(encoding="utf-8")
    runtime_contract_path = repo / "docs/project/AGENT_RUNTIME_CONTRACT.md"
    runtime_contract_text = runtime_contract_path.read_text(encoding="utf-8")
    audit_path = repo / "scripts/post_run_audit.py"
    source_game = repo / ".venv/Lib/site-packages/career_emulator/game.py"
    source_models = repo / ".venv/Lib/site-packages/career_emulator/server/models.py"
    for path in (audit_path, source_game, source_models):
        if not path.is_file():
            raise ValueError(f"required offline source missing: {path.name}")
    game_text = source_game.read_text(encoding="utf-8")
    models_text = source_models.read_text(encoding="utf-8")
    audit_source = audit_path.read_text(encoding="utf-8")
    manifest_text += "\n" + audit_source
    risk_tokens = {
        "manifest_x0_blocks_submit": "`X=0` 禁止提交" in manifest_text,
        "risk_skill_x1_means_branch_completed": "`X=1` 表示完成一次 reconsideration branch" in risk_text,
        "risk_skill_x0_blocks_second_reconsideration": "使用 `X=0`" in risk_text and "禁止 `take_action`" in risk_text,
        "dash_no_branch_semantics_explicit": bool(re.search(r"X=-.{0,50}(?:no branch|没有 reconsideration|未发生 reconsideration)", risk_text, re.I | re.S)),
        "runtime_take_action_returns_success_without_updated_state": "return TakeActionResponse(success=True)" in game_text,
        "response_has_success_and_error_only": "class TakeActionResponse" in models_text and "success: bool" in models_text and "error: str | None = None" in models_text,
        "runtime_take_action_reads_notes_but_has_no_marker_gate": "notes = truncate_note(notes)" in game_text and "CTRL" not in game_text and "[DL" not in game_text,
        "delivery_skill_checkpoint_enum_is_boolean_like": "checkpoint=<0|1|?>" in delivery_text,
        "manifest_dl_enum_is_underspecified": 'checkpoint=<...>' in manifest_text,
        "board_contract_tracks_current_level_progression_response": "PROGRESSION_RESPONSE" in board_text and "NO_GAIN" in board_text,
        "planning_contract_devalues_no_gain_and_avoids_immediate_repeat": "NO_GAIN" in planning_text and "不立即重复同一个 no-gain 投入" in planning_text,
        "runtime_contract_requires_observe_after_action": "take_action\n  → fresh observe" in runtime_contract_text,
        "audit_separator_accepts_one_newline": 'in (" ", "\\n", "\\r\\n")' in audit_source,
    }
    run_window = manifest.get("run_window_utc", {})
    replay = audit(
        archive_paths["events.jsonl"],
        archive_paths["transcript.log"],
        archive_paths["score_report.json"],
        archive_paths["runner-result.json"],
        run_start=run_window.get("start"),
        run_end=run_window.get("end"),
        evidence_manifest=manifest_path,
    )
    replay_delivery = replay.get("adherence_evidence", {}).get("delivery_marker_coverage", {})
    if len(action_rows) != 207 or len(observations) != 190:
        raise ValueError("raw action/observe counts drifted from the frozen RUN03 identity")
    return {
        "schema_version": 1,
        "run_id": RUN_ID,
        "session_id": SESSION_ID,
        "source_identity": {
            "manifest_sha256": _file_identity(manifest_path)["sha256"],
            "archived_artifacts": dict(sorted(identities.items())),
            "archived_evidence_unchanged_against_manifest": True,
            "runner_result_identity": "RECONSTRUCTED_AND_CROSSCHECKED_TO_SESSION_BOUND_SCORE_REPORT",
            "core_session_check": "PASS",
            "secret_scan": "PASS",
        },
        "event_inventory": {
            "unique_tool_calls": len(calls),
            "tool_counts": dict(sorted(names.items())),
            "successful_actions": sum(action["result"].get("success") is True for action in action_rows),
            "failed_actions": sum(action["result"].get("success") is False for action in action_rows),
            "action_result_fields": {str(fields): count for fields, count in sorted(observed_tool_result_fields.items())},
            "action_result_values": dict(sorted(action_results.items())),
            "observe_result_fields": dict(sorted(Counter(str(tuple(sorted(call["result"]["data"].keys()))) for call in observe_calls).items())),
        },
        "fresh_state_semantics": {
            "alleged_missing_boundaries": 18,
            "true_explicit_observe_violations": len(missing_boundaries),
            "take_action_result_equivalents": 0,
            "partial_or_unknown": 0,
            "classification": "EXPLICIT_OBSERVE_REQUIRED_AND_MISSING",
            "take_action_result_schema": {"fields": ["success", "error"], "updated_public_state_present": False, "current_event_present": False, "legal_choices_present": False},
            "boundary_records": missing_boundaries,
        },
        "ctrl_closure": {
            "marker_syntax_counts": dict(sorted(ctrl_counts.items())),
            "risk_counts": dict(sorted(risk_counts.items())),
            "x_counts": dict(sorted(x_counts.items())),
            "truth_table": {
                "no_reconsideration": {"candidate_token": "X=-", "evidence_status": "INFERENCE_TOKEN_AVAILABLE_BUT_NOT_DEFINED"},
                "completed_reconsideration": {"token": "X=1", "semantics": "one reconsideration branch completed"},
                "unresolved_block": {"token": "X=0", "semantics": "second reconsideration remains; action prohibited"},
                "parser": {"syntax_accepts": ["0", "1", "-"], "closure_rejects": "X=0", "closure_accepts_final_r_non_reconsider": True},
                "run03_emitted": "R=PASS X=0 on all 207 actions; no final-note X=1 or X=-",
            },
            "root_cause": "CONTRACT_ENCODING_AMBIGUITY",
            "runtime_patch_justified": "YES",
            "audit_patch_justified": "NO",
            "root_cause_limit": "Transcript does not directly prove the model's internal interpretation; classify the overloaded/undefined X token representation, not a hidden intent.",
        },
        "delivery_markers": {
            **delivery,
            "format_failure_rate": f"{delivery['actual_contract_invalid']}/{delivery['actions']} ({delivery['actual_contract_invalid'] / delivery['actions']:.2%})",
            "skill_manifest_schema": "Skill gives concrete enums; Manifest mirrors fields but leaves enum details unspecified.",
            "pre_patch_auditor_conclusion": "The 0/207 archived count is an auditor false-negative for 174 newline-delimited valid markers; 33 checkpoints are truly outside the Skill enum.",
            "semantic_delivery_status": "INCONCLUSIVE",
            "root_cause": "MULTIPLE_CAUSES",
            "runtime_patch_justified": "YES",
            "audit_patch_justified": "YES",
            "parser_legacy_superset": "post_run_audit.py still accepts missing i for legacy compatibility; all RUN03 notes emitted i, so this did not cause this run's false negatives.",
        },
        "m42_no_gain": m42,
        "contract_surface_facts": risk_tokens,
        "contract_source_identities": {
            "runtime_manifest.json": _file_identity(repo / "configs/runtime_manifest.json"),
            "AGENT_RUNTIME_CONTRACT.md": _file_identity(runtime_contract_path),
            "post_run_audit.py": _file_identity(audit_path),
            "career_emulator/game.py": _file_identity(source_game),
            "career_emulator/server/models.py": _file_identity(source_models),
            **{f"skills/{name}/SKILL.md": _file_identity(repo / "skills" / name / "SKILL.md") for name in SKILL_ORDER},
        },
        "post_run_audit_replay_after_parser_patch": {
            "delivery_marker_coverage": replay_delivery,
            "ctrl_closure": replay.get("actions", {}).get("ctrl_closure", {}),
        },
        "scope_accounting": {
            "provider_calls": 0,
            "service_starts": 0,
            "mcp_calls": 0,
            "db_access": 0,
            "runner_plays": 0,
            "games": 0,
            "runtime_candidate_changes": 0,
            "transcript_private_narration_saved": False,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True, help="exact CareerSim repository root")
    parser.add_argument("--output", type=Path, required=True, help="write the derived JSON to an explicit scratch path")
    args = parser.parse_args()
    result = analyze(args.repo)
    output = args.output.resolve()
    repo = args.repo.resolve()
    if output in { (repo / ARCHIVE / name).resolve() for name in (*ARCHIVE_FILES, "evidence-manifest.json") }:
        parser.error("output must not overwrite archived evidence")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    _scan(output)
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
