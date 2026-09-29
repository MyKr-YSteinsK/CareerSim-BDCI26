"""Offline, run-scoped CareerSim evidence extraction. No runtime imports or calls."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


SKILLS = ("structured-state-board", "rolling-planning", "delivery-progress", "risk-review")
PUBLIC_STATUS = {"level", "health", "dignity", "skill", "network", "output", "wealth", "energy", "duration_in_level"}
SCORE_FIELDS = {"quantitative_score", "competition_partial_score", "survival_months", "grade", "completed", "outcome"}
MAIN_ACTIONS = {"申请关键项目", "向领导汇报成果", "低调避险", "不行动"}
CTRL = re.compile(r"^\[CTRL G=(?P<gap>[^\]\r\n]+?) P=(?P<phase>A|S|\?) R=(?P<risk>PASS|ALLOW|WARN|RECONSIDER|UNKNOWN) X=(?P<x>0|1|-)\]")
DL = re.compile(r"\[DL (?:(?:i=(?P<item_id>NONE|D[1-9][0-9]*|UNKNOWN)) )?n=(?P<n>[0-3]) focus=(?P<focus>NONE|OPPORTUNITY|COMMITTED|IN_PROGRESS|BLOCKED|DELIVERY_CLAIMED|DELIVERED|UNKNOWN) evidence=(?P<evidence>NA|UNKNOWN|UNVERIFIED|PUBLICLY_VERIFIED) checkpoint=(?P<checkpoint>[01?]) recognition=(?P<recognition>[01?])\]")
SKILL_PATH = re.compile(r"(?:^|/)agent/workspace/skills/(structured-state-board|rolling-planning|delivery-progress|risk-review)/SKILL\.md$", re.I)
INTERNAL_MARKER = re.compile(r"hidden|internal|event[_ -]?id|threshold|counter|score|risk", re.I)
SESSION = re.compile(r"\b(?:game_session_id|session_id|SESSION)\b[\"']?\s*[:=]\s*[\"']?([0-9a-f]{32})\b", re.I)
STAMP = re.compile(r"\b(20\d\d-\d\d-\d\d[ T]\d\d:\d\d:\d\d(?:\.\d+)?(?:Z|[+-]\d\d:\d\d)?)")
REVIEW = re.compile(r"半年.{0,8}评审|绩效.{0,8}评审|晋升.{0,8}评审|半年绩效评级|半年谈话|formal review|performance review", re.I)
QUARTER_MAIN = re.compile(r"季度.{0,8}主行动|quarterly.{0,8}main", re.I)
HIDDEN_NUMERIC = re.compile(r"\bHiddenRisk\s*(?:[:=]\s*)?[+-]?\d+\b", re.I)
INTERNAL_SCORE_NUMERIC = re.compile(r"\b(?:internal_score|hidden_score)\s*(?:[:=]\s*)?[+-]?\d+\b", re.I)
SENSITIVE_G = re.compile(r"hidden|internal|event[_ -]?id|threshold|counter", re.I)
DELIVERY_MARKERS = ("stage=", "evidence_status=", "recognition_link=", "next_checkpoint=", "COMMITTED", "IN_PROGRESS", "BLOCKED", "DELIVERY_CLAIMED", "DELIVERED", "PUBLICLY_VERIFIED")


def parse_time(value: str, naive_offset: timezone | None = None) -> datetime | None:
    """Return a UTC timestamp; never guess a timezone for a naive log timestamp."""
    try:
        parsed = datetime.fromisoformat(value.strip().replace(" ", "T", 1).replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        if naive_offset is None:
            return None
        parsed = parsed.replace(tzinfo=naive_offset)
    return parsed.astimezone(timezone.utc)


def parse_offset(value: str | None) -> timezone | None:
    if value is None:
        return None
    match = re.fullmatch(r"([+-])(\d\d):(\d\d)", value)
    if not match or int(match[2]) > 23 or int(match[3]) > 59:
        raise ValueError("--log-utc-offset must have the form +08:00")
    minutes = (int(match[2]) * 60 + int(match[3])) * (1 if match[1] == "+" else -1)
    return timezone(timedelta(minutes=minutes))


def file_identity(path: Path) -> dict[str, Any]:
    digest = hashlib.sha256()
    size = 0
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            size += len(block)
            digest.update(block)
    return {"name": path.name, "bytes": size, "sha256": digest.hexdigest()}


def _node(record: dict[str, Any]) -> dict[str, Any]:
    payload = record.get("payload")
    if not isinstance(payload, dict):
        return {}
    delta = payload.get("delta")
    return delta if isinstance(delta, dict) and "tool_call" not in payload and "raw_output" not in payload else payload


def _result(node: dict[str, Any]) -> dict[str, Any]:
    raw = node.get("raw_output")
    if not isinstance(raw, dict):
        return {}
    result = raw.get("result")
    if isinstance(result, dict):
        return result
    if isinstance(result, str):
        try:
            decoded = json.loads(result)
        except json.JSONDecodeError:
            return {}
        return decoded if isinstance(decoded, dict) else {}
    return {}


def _arguments(call: dict[str, Any]) -> dict[str, Any]:
    value = call.get("arguments")
    if isinstance(value, dict):
        return value
    if isinstance(value, str):
        try:
            decoded = json.loads(value)
        except json.JSONDecodeError:
            return {}
        return decoded if isinstance(decoded, dict) else {}
    return {}


def _read_skill(name: str, args: dict[str, Any]) -> str | None:
    """Accept only an explicit installed SKILL.md target, never a text mention."""
    if not ("skill_tool" in name or "read_file" in name):
        return None
    for key in ("path", "file_path", "filename"):
        path = args.get(key)
        if not isinstance(path, str) or ".." in path.replace("\\", "/").split("/"):
            continue
        normalized = path.replace("\\", "/")
        if not re.match(r"^(?:[A-Za-z]:/|/)", normalized):
            continue
        match = SKILL_PATH.search(normalized)
        if match:
            return match[1].lower()
    if "skill_tool" in name:
        # The skill tool accepts a skill id directly; a successful result proves the read.
        skill = next((args[key] for key in ("skill_name", "skill_id", "skill", "name") if key in args), None)
        if isinstance(skill, str) and skill in SKILLS:
            return skill
    return None


def _successful_read(node: dict[str, Any]) -> bool:
    raw = node.get("raw_output")
    if not isinstance(raw, dict) or node.get("is_error") or node.get("error") or raw.get("isError") or raw.get("error"):
        return False
    result = _result(node)
    return not (result.get("error") or result.get("isError")) and result.get("success") is not False and raw.get("success") is not False and bool(raw.get("result"))


def _public_state(data: dict[str, Any]) -> dict[str, Any]:
    state = data.get("current_state")
    state = state if isinstance(state, dict) else {}
    status = state.get("status")
    status = status if isinstance(status, dict) else {}
    time = state.get("time")
    time = time if isinstance(time, dict) else {}
    return {
        "session_id": state.get("session_id") or data.get("session_id"),
        "time": {key: time.get(key) for key in ("current_month", "current_quarter", "current_year") if isinstance(time.get(key), int) and not isinstance(time.get(key), bool)},
        "status": {key.lower(): value for key, value in status.items() if key.lower() in PUBLIC_STATUS and isinstance(value, (str, int, float)) and not isinstance(value, bool)},
    }


def _fresh_score(data: dict[str, Any]) -> dict[str, Any]:
    score = data.get("ending_score")
    if not isinstance(score, dict):
        return {}
    return {key: value for key, value in score.items() if key in SCORE_FIELDS and isinstance(value, (str, int, float, bool))}


def _log_compressions(path: Path, start: datetime, end: datetime, offset: timezone | None) -> tuple[list[str], int]:
    found: set[tuple[str, str]] = set()
    unscoped = 0
    current: datetime | None = None
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            stamp = STAMP.search(line)
            if stamp:
                current = parse_time(stamp[1], offset)
            if "CurrentRoundCompressor" not in line:
                continue
            if current is None:
                unscoped += 1
            elif start <= current <= end:
                found.add((current.isoformat(), line.strip()))
    return sorted(stamp for stamp, _ in found), unscoped


def _transcript_evidence(path: Path) -> tuple[list[str], dict[str, int]]:
    sessions: set[str] = set()
    markers: Counter[str] = Counter()
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            sessions.update(match.lower() for match in SESSION.findall(line))
            for marker in DELIVERY_MARKERS:
                markers[marker] += line.count(marker)
    return sorted(sessions), dict(sorted(markers.items()))


def audit(
    events: Path,
    transcript: Path,
    score_report: Path | None,
    runner_result: Path,
    llm_log: Path | None = None,
    run_start: str | None = None,
    run_end: str | None = None,
    log_utc_offset: str | None = None,
    evidence_manifest: Path | None = None,
) -> dict[str, Any]:
    """Extract one deterministic summary from explicit offline inputs."""
    if bool(run_start) != bool(run_end):
        raise ValueError("--run-start and --run-end must be supplied together")
    offset = parse_offset(log_utc_offset)
    limitations: set[str] = set()
    new_game_ids: list[str] = []
    observe_ids: list[str] = []
    observes: list[dict[str, Any]] = []
    calls: dict[str, dict[str, Any]] = {}
    action_calls: list[dict[str, Any]] = []
    timeline: list[tuple[datetime, str, str | None]] = []
    first_ts: datetime | None = None
    last_ts: datetime | None = None
    latest_observe: dict[str, Any] | None = None
    seen_calls: set[str] = set()
    seen_results: set[str] = set()
    review_checkpoints: list[dict[str, Any]] = []
    promotions: list[dict[str, Any]] = []
    quarter_main: list[dict[str, Any]] = []
    pre_review_choices: list[dict[str, Any]] = []
    first_review_month: int | None = None
    first_review_order: int | None = None
    previous_level: Any = None
    ctrl = Counter()
    closure = Counter()
    ctrl_states: list[dict[str, Any]] = []
    phase_counts = Counter()
    risk_counts = Counter()
    x_counts = Counter()
    violations = Counter()
    note_delivery = Counter()
    delivery_coverage = Counter()
    delivery_actions: list[dict[str, Any]] = []

    with events.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.strip():
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"events line {line_number} is not JSON") from exc
            if not isinstance(record, dict):
                raise ValueError(f"events line {line_number} is not an object")
            ts = parse_time(str(record.get("ts", "")))
            if ts is not None:
                first_ts = ts if first_ts is None else min(first_ts, ts)
                last_ts = ts if last_ts is None else max(last_ts, ts)
            kind = record.get("kind")
            node = _node(record)
            if kind == "tool_call":
                call = node.get("tool_call")
                if not isinstance(call, dict):
                    continue
                call_id = str(call.get("tool_call_id") or f"seq:{record.get('seq', line_number)}")
                if call_id in seen_calls:
                    continue
                seen_calls.add(call_id)
                name = str(call.get("name") or "")
                args = _arguments(call)
                calls[call_id] = {"name": name, "args": args}
                if "take_action" in name:
                    choice = args.get("choice")
                    notes = args.get("notes")
                    notes = notes if isinstance(notes, str) else ""
                    ctrl["attempts"] += 1
                    ctrl["valid"] += int(bool(CTRL.match(notes)) and notes.count("[CTRL") == 1)
                    ctrl["missing"] += int("[CTRL" not in notes)
                    ctrl["malformed_or_duplicate"] += int("[CTRL" in notes and (not CTRL.match(notes) or notes.count("[CTRL") != 1))
                    ctrl["single_integer_choice"] += int(isinstance(choice, int) and not isinstance(choice, bool))
                    ctrl_match = CTRL.match(notes)
                    if not ctrl_match or notes.count("[CTRL") != 1:
                        closure["malformed_or_missing_ctrl"] += 1
                        gap, phase, risk, x = ("UNKNOWN",) * 4
                    else:
                        gap, phase, risk, x = ctrl_match.group("gap", "phase", "risk", "x")
                        if len(gap) > 80 or SENSITIVE_G.search(gap):
                            gap = "REDACTED_INTERNAL_REFERENCE"
                            violations["ctrl_gap_prohibited_or_unbounded_reference"] += 1
                        if x == "0":
                            closure["submitted_incomplete_x0"] += 1
                        elif risk == "RECONSIDER":
                            closure["submitted_nonfinal_r_reconsider"] += 1
                        else:
                            closure["valid"] += 1
                    ctrl_states.append({"action_index": len(action_calls) + 1, "month": latest_observe.get("month") if latest_observe else "UNKNOWN", "G": gap, "P": phase, "R": risk, "X": x})
                    phase_counts[phase] += 1
                    risk_counts[risk] += 1
                    x_counts[x] += 1
                    violations["numeric_hiddenrisk_reference"] += int(bool(HIDDEN_NUMERIC.search(notes)))
                    violations["numeric_internal_score_reference"] += int(bool(INTERNAL_SCORE_NUMERIC.search(notes)))
                    for marker in DELIVERY_MARKERS:
                        note_delivery[marker] += notes.count(marker)
                    delivery_coverage["attempts"] += 1
                    dl_count = notes.count("[DL")
                    dl_match = DL.search(notes) if dl_count == 1 else None
                    marker_text = notes[notes.index("[DL"):].split("]", 1)[0] if dl_count else ""
                    marker_spans = re.findall(r"\[DL[^\]\r\n]*(?:\]|$)", notes)
                    contaminated = any(INTERNAL_MARKER.search(span) for span in marker_spans)
                    if contaminated:
                        violations["delivery_marker_internal_reference"] += 1
                    dl_n = int(dl_match["n"]) if dl_match else None
                    dl_item_id = dl_match["item_id"] if dl_match else None
                    valid_identity = (
                        dl_item_id is None
                        or (dl_n == 0 and dl_item_id == "NONE")
                        or (dl_n is not None and dl_n > 0 and dl_item_id != "NONE")
                    )
                    valid_dl = bool(
                        dl_match and ctrl_match and not contaminated
                        and notes[ctrl_match.end():dl_match.start()] == " "
                        and dl_match[0] == "[DL" + marker_text.split("[DL", 1)[-1] + "]"
                        and valid_identity
                        and ((dl_n == 0 and dl_match["focus"] == "NONE" and dl_match["evidence"] == "NA" and dl_match["checkpoint"] == "0" and dl_match["recognition"] == "0")
                             or (dl_n != 0 and dl_match["focus"] != "NONE" and dl_match["evidence"] != "NA"))
                    )
                    delivery_coverage["valid"] += int(valid_dl)
                    delivery_coverage["missing"] += int(dl_count == 0)
                    delivery_coverage["malformed_or_duplicate"] += int(dl_count > 0 and not valid_dl)
                    delivery_coverage["identity_missing"] += int(valid_dl and dl_item_id is None)
                    if valid_dl:
                        delivery_actions.append({"action_index": len(action_calls) + 1, "event_order": line_number, "month": latest_observe.get("month") if latest_observe else "UNKNOWN", "state": {"item_id": dl_item_id or "UNKNOWN", "n": dl_n, "focus": dl_match["focus"], "evidence": dl_match["evidence"], "checkpoint": dl_match["checkpoint"], "recognition": dl_match["recognition"]}})
                    action = {"id": call_id, "name": name, "ts": ts, "choice": choice, "result": "UNKNOWN"}
                    action_calls.append(action)
                    if ts is not None:
                        timeline.append((ts, "take_action", None))
                    if latest_observe is not None:
                        choices = latest_observe.get("choices", {})
                        selected = choices.get(choice) if isinstance(choice, int) and not isinstance(choice, bool) else None
                        title = latest_observe.get("event_title", "")
                        month = latest_observe.get("month")
                        if selected and (QUARTER_MAIN.search(title) or selected in MAIN_ACTIONS):
                            quarter_main.append({"month": month, "action": selected, "source": "public_choice"})
                continue
            if kind != "tool_result":
                continue
            call_id = str(node.get("tool_call_id") or "")
            if not call_id or call_id in seen_results:
                continue
            seen_results.add(call_id)
            tool_name = str(node.get("tool_name") or calls.get(call_id, {}).get("name") or "")
            result = _result(node)
            if "new_game" in tool_name:
                session_id = result.get("session_id")
                if isinstance(session_id, str) and session_id:
                    new_game_ids.append(session_id)
            elif "observe" in tool_name and isinstance(result.get("current_state"), dict):
                public = _public_state(result)
                session_id = public.get("session_id")
                if isinstance(session_id, str) and session_id:
                    observe_ids.append(session_id)
                state = result["current_state"]
                flags = state.get("simulation_flags") if isinstance(state.get("simulation_flags"), dict) else {}
                event = result.get("current_event") if isinstance(result.get("current_event"), dict) else {}
                title = str(event.get("title") or "")[:200]
                feed = str(result.get("events") or "")[:4000]
                month = public["time"].get("current_month")
                score = _fresh_score(result)
                choices = {item.get("choice"): str(item.get("action") or "")[:200] for item in result.get("choices", []) if isinstance(item, dict) and isinstance(item.get("choice"), int)} if isinstance(result.get("choices"), list) else {}
                snapshot = {"ts": ts, "public": public, "score": score, "flags": {key: flags.get(key) for key in ("failed", "alive", "failure_reason")}, "month": month, "event_title": title, "choices": choices}
                observes.append(snapshot)
                latest_observe = snapshot
                if ts is not None:
                    timeline.append((ts, "observe", session_id if isinstance(session_id, str) else None))
                if REVIEW.search(title + " " + feed):
                    if first_review_order is None:
                        first_review_order = line_number
                    if first_review_month is None and isinstance(month, int):
                        first_review_month = month
                    checkpoint = {"month": month, "event_title": title, "source": "public_observe"}
                    if checkpoint not in review_checkpoints:
                        review_checkpoints.append(checkpoint)
                level = public["status"].get("level")
                if level is not None and previous_level is not None and level != previous_level:
                    promotions.append({"month": month, "from_level": previous_level, "to_level": level, "source": "observed_level_change"})
                if level is not None:
                    previous_level = level
                if first_review_month is None and len(pre_review_choices) < 80:
                    pre_review_choices.append({"month": month, "event_title": title, "legal_actions": list(choices.values())})
            elif "take_action" in tool_name or call_id in {item["id"] for item in action_calls}:
                for action in reversed(action_calls):
                    if action["id"] == call_id:
                        raw = node.get("raw_output")
                        if result.get("success") is True or (isinstance(raw, dict) and raw.get("success") is True):
                            action["result"] = "SUCCESS"
                        elif result.get("success") is False or node.get("is_error") or node.get("error") or (isinstance(raw, dict) and (raw.get("isError") or raw.get("error"))):
                            action["result"] = "ERROR"
                        break
            read_skill = _read_skill(calls.get(call_id, {}).get("name", tool_name), calls.get(call_id, {}).get("args", {}))
            if read_skill and ts is not None and _successful_read(node):
                timeline.append((ts, "skill_read", read_skill))

    transcript_ids, transcript_delivery = _transcript_evidence(transcript)
    transcript_text = transcript.read_text(encoding="utf-8")
    transcript_discipline = {
        "numeric_hiddenrisk_reference": len(HIDDEN_NUMERIC.findall(transcript_text)),
        "numeric_internal_score_reference": len(INTERNAL_SCORE_NUMERIC.findall(transcript_text)),
        "basis": "TEXT_MATCHES_NOT_SEMANTIC_VERDICT",
    }
    score_data = json.loads(score_report.read_text(encoding="utf-8")) if score_report is not None else {}
    if score_report is None:
        limitations.add("score_report_missing_partial_audit")
    runner_data = json.loads(runner_result.read_text(encoding="utf-8"))
    if not isinstance(score_data, dict) or not isinstance(runner_data, dict):
        raise ValueError("score report and runner result must be JSON objects")
    unique_new = sorted(set(new_game_ids))
    unique_observe = sorted(set(observe_ids))
    session = unique_new[0] if len(unique_new) == 1 else "UNKNOWN"
    events_identity = "PASS" if len(new_game_ids) == 1 and unique_observe == [session] else "FAIL_OR_UNKNOWN"
    transcript_identity = "PASS" if transcript_ids == [session] else ("UNKNOWN" if not transcript_ids else "MISMATCH")
    if events_identity != "PASS":
        limitations.add("fresh_session_identity_not_established_from_events")
    if transcript_identity != "PASS":
        limitations.add("transcript_session_marker_" + transcript_identity.lower())
    report_id = score_data.get("session_id")
    score_report_identity = "MISSING" if score_report is None else ("MATCH" if report_id == session and session != "UNKNOWN" else ("EMPTY" if not report_id else "MISMATCH"))
    if score_report_identity != "MATCH":
        limitations.add("score_report_session_field_" + score_report_identity.lower())
    matching_observes = [item for item in observes if item["public"]["session_id"] == session]
    terminal = matching_observes[-1] if matching_observes else None
    fresh_score = terminal["score"] if terminal and events_identity == "PASS" else {}
    if not fresh_score:
        limitations.add("fresh_terminal_score_not_observed")
    runner_exit = runner_data.get("exit_code", runner_data.get("runner_exit_code", "UNKNOWN"))
    if not isinstance(runner_exit, int) or isinstance(runner_exit, bool):
        runner_exit = "UNKNOWN"
        limitations.add("runner_exit_code_unknown")
    terminal_flags = terminal["flags"] if terminal else {}
    completed = bool(terminal and ("Completed the 48-month simulation" in str(terminal_flags.get("failure_reason") or "") or fresh_score.get("completed") is True) and terminal["month"] == 49 and runner_exit == 0)
    if not completed:
        limitations.add("terminal_48m_completion_not_established")
    if first_review_month is None:
        limitations.add("first_formal_review_not_identified")
    if len(pre_review_choices) >= 80:
        limitations.add("pre_first_review_choice_list_truncated_at_80")
    if run_start and run_end:
        start, end = parse_time(run_start), parse_time(run_end)
        source = "explicit"
    elif events_identity == "PASS":
        start, end = first_ts, last_ts
        source = "events"
    else:
        start = end = None
        source = "UNKNOWN"
    if start is None or end is None or start > end:
        limitations.add("run_window_unknown_or_invalid")
        start = end = None
    compression: dict[str, Any] = {"status": "UNKNOWN", "count": "UNKNOWN", "events_utc": [], "recovery": []}
    if llm_log is not None:
        if start is not None and end is not None:
            stamps, unscoped = _log_compressions(llm_log, start, end, offset)
            compression.update({"status": "SCOPED" if not unscoped else "PARTIAL", "count": len(stamps) if not unscoped else "UNKNOWN", "events_utc": stamps})
            if unscoped:
                limitations.add("llm_compressor_lines_without_usable_timestamp")
            ordered = sorted(timeline, key=lambda item: item[0])
            for stamp in stamps:
                comp_ts = parse_time(stamp)
                assert comp_ts is not None
                next_action = next((ts for ts, kind, _ in ordered if kind == "take_action" and ts > comp_ts), None)
                if next_action is None:
                    compression["recovery"].append({"at_utc": stamp, "tool_order_status": "UNKNOWN", "rebuild_evidence": {key: "UNKNOWN" for key in ("board", "delivery", "review_plan", "recovery_ready")}, "overall_status": "UNKNOWN_NO_NEXT_ACTION"})
                    continue
                between = [(kind, value) for ts, kind, value in ordered if comp_ts < ts < next_action]
                fresh_observe = any(kind == "observe" and value == session for kind, value in between)
                first_fresh = next((ts for ts, kind, value in ordered if comp_ts < ts < next_action and kind == "observe" and value == session), None)
                reread = sorted({value for ts, kind, value in ordered if first_fresh is not None and first_fresh < ts < next_action and kind == "skill_read" and value in SKILLS})
                tool_status = "PASS" if fresh_observe and len(reread) == 4 else "FAIL"
                if tool_status == "PASS":
                    limitations.add("recovery_rebuild_semantics_not_machine_verified")
                compression["recovery"].append({"at_utc": stamp, "fresh_observe": fresh_observe, "reread_skills": reread, "tool_order_status": tool_status, "rebuild_evidence": {key: "UNKNOWN" for key in ("board", "delivery", "review_plan", "recovery_ready")}, "overall_status": "TOOL_ORDER_PASS_REBUILD_UNVERIFIED" if tool_status == "PASS" else "RECOVERY_FAIL"})
        else:
            limitations.add("llm_log_not_counted_without_run_window")
    else:
        limitations.add("llm_log_not_supplied_compression_unknown")
    usage = score_data.get("token_usage")
    usage = usage if isinstance(usage, dict) else {}
    token_usage = {key: usage.get(key, "UNKNOWN") for key in ("input_tokens", "output_tokens", "total_tokens")}
    token_usage["binding"] = "SESSION_MATCH" if score_report_identity == "MATCH" else "RUNNER_REPORT_DIAGNOSTIC_ONLY"
    token_usage["actual_billed_cost"] = "UNKNOWN"
    identities = {name: file_identity(path) for name, path in (("events", events), ("transcript", transcript), ("score_report", score_report), ("runner_result", runner_result)) if path is not None}
    if llm_log is not None:
        identities["llm_log"] = file_identity(llm_log)
    if evidence_manifest is not None:
        identities["evidence_manifest"] = file_identity(evidence_manifest)
    delivery_coverage["status"] = "UNKNOWN" if not action_calls else ("DELIVERY_MARKER_COVERAGE_PASS" if delivery_coverage["valid"] == len(action_calls) else "DELIVERY_MARKER_COVERAGE_FAIL")
    pre_review_delivery = [item for item in delivery_actions if first_review_order is not None and item["event_order"] < first_review_order]
    closure["status"] = "UNKNOWN" if not action_calls else ("CTRL_CLOSURE_PASS" if closure["valid"] == len(action_calls) else "CTRL_CLOSURE_FAIL")
    closure["basis"] = "MARKER_CONSISTENCY_ONLY"
    if x_counts["1"]:
        limitations.add("ctrl_x1_branch_use_not_independently_verified")
    gaps = [item["G"] for item in ctrl_states]
    partial = bool(not completed and events_identity == "PASS" and transcript_identity == "PASS" and terminal and isinstance(runner_exit, int) and runner_exit != 0 and not fresh_score)
    public_observes = [{"at_utc": item["ts"].isoformat() if item["ts"] else "UNKNOWN", "public": item["public"], "alive": item["flags"].get("alive"), "failed": item["flags"].get("failed"), "event_title": item["event_title"]} for item in matching_observes]
    natural_terminal = True if completed or fresh_score else (False if terminal_flags.get("alive") is True and terminal_flags.get("failed") is False else "UNKNOWN")
    gap_changes = sum(a != b for a, b in zip(gaps, gaps[1:]) if a != "UNKNOWN" and b != "UNKNOWN" and a != "REDACTED_INTERNAL_REFERENCE" and b != "REDACTED_INTERNAL_REFERENCE")
    return {
        "schema_version": 1,
        "inputs": identities,
        "run": {"session_id": session, "new_game_count": len(new_game_ids), "observe_count": len(observes), "events_identity": events_identity, "transcript_identity": transcript_identity, "transcript_session_ids": transcript_ids, "runner_exit_code": runner_exit, "window_source": source, "start_utc": start.isoformat() if start else "UNKNOWN", "end_utc": end.isoformat() if end else "UNKNOWN"},
        "outcome": {"classification": "VALID_48M_COMPLETION" if completed else ("PARTIAL_GAMEPLAY_TECHNICAL_FAILURE" if partial else "UNKNOWN"), "natural_terminal_observed": natural_terminal, "max_month": max((item["month"] for item in matching_observes if isinstance(item["month"], int)), default="UNKNOWN"), "last_observe_alive": terminal_flags.get("alive", "UNKNOWN"), "last_observe_failed": terminal_flags.get("failed", "UNKNOWN"), "terminal_fresh_score": fresh_score or "UNKNOWN", "score_source": "fresh_final_observe" if fresh_score else "UNKNOWN", "score_report_session_field": score_report_identity, "terminal_public_state": terminal["public"] if terminal else "UNKNOWN"},
        "trajectory": {"public_observations": public_observes, "review_checkpoints": review_checkpoints, "promotion_checkpoints": promotions, "quarterly_main_actions": quarter_main},
        "actions": {"attempts": len(action_calls), "success": sum(item["result"] == "SUCCESS" for item in action_calls), "errors": sum(item["result"] == "ERROR" for item in action_calls), "unknown_results": sum(item["result"] == "UNKNOWN" for item in action_calls), "noncanonical_routes": sum(item["name"] != "mcp_career-emulator_take_action" for item in action_calls), "ctrl": dict(sorted(ctrl.items())), "ctrl_closure": dict(sorted(closure.items())), "ctrl_states_by_action": ctrl_states, "ctrl_trajectory": {"P_counts": dict(sorted(phase_counts.items())), "R_counts": dict(sorted(risk_counts.items())), "X_counts": dict(sorted(x_counts.items())), "G_change_count": gap_changes, "G_values_in_order": gaps, "G_semantic_justification": "NOT_INFERRED"}, "evidence_discipline_categories": dict(sorted(violations.items()))},
        "adherence_evidence": {"transcript_evidence_discipline_categories": transcript_discipline, "compression": compression, "delivery_marker_coverage": dict(sorted(delivery_coverage.items())), "delivery_states_by_action": delivery_actions, "delivery_marker_mentions": {"transcript": transcript_delivery, "action_notes": dict(sorted(note_delivery.items()))}, "delivery_lifecycle_status": "MARKERS_OBSERVED_NOT_ADHERENCE_PROOF" if delivery_actions or any(transcript_delivery.values()) or any(note_delivery.values()) else "NOT_OBSERVED"},
        "mechanism_inputs": {"first_formal_review_month": first_review_month if first_review_month is not None else "UNKNOWN", "pre_first_review_public_choices": pre_review_choices, "pre_first_review_delivery_states": pre_review_delivery, "trigger_classification": "UNKNOWN_REQUIRES_SEMANTIC_AUDIT"},
        "usage": token_usage,
        "limitations": sorted(limitations),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("events", "transcript", "runner-result", "output"):
        parser.add_argument("--" + name, type=Path, required=True)
    parser.add_argument("--score-report", type=Path, help="omit for partial technical-failure evidence; a supplied path must exist")
    parser.add_argument("--llm-log", type=Path)
    parser.add_argument("--run-start", help="timezone-aware ISO timestamp")
    parser.add_argument("--run-end", help="timezone-aware ISO timestamp")
    parser.add_argument("--log-utc-offset", help="offset for naive cumulative-log timestamps, e.g. +08:00")
    parser.add_argument("--evidence-manifest", type=Path)
    args = parser.parse_args()
    inputs = [args.events, args.transcript, args.score_report, args.runner_result, args.llm_log, args.evidence_manifest]
    if args.output.resolve() in {path.resolve() for path in inputs if path is not None}:
        parser.error("output must not overwrite an input artifact")
    try:
        summary = audit(args.events, args.transcript, args.score_report, args.runner_result, args.llm_log, args.run_start, args.run_end, args.log_utc_offset, args.evidence_manifest)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        parser.error(str(exc))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
