"""Offline v12 adapter; WF-01 historical extraction remains unchanged.

Numeric mentions are provenance candidates, never automatic semantic verdicts.
No provider, DB, service, candidate mutation, or implicit latest-run discovery.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path

from scripts import post_run_audit as legacy

SKILLS = ("career-state-brief", "career-decision")
BRIEF_FIELDS = ("SESSION_BASIS", "REVIEW_OBJECTIVE", "RESULT_COMMITMENT", "UNRESOLVED_CONSTRAINT", "PATH_UPDATE_STOP")
NUMERIC = re.compile(r"\bHiddenRisk\s*(?:[:=]\s*)?[+-]?\d+\b", re.I)


def provenance(text: str, advertised: str) -> str:
    """Only signed, exact current advertised mentions get delta admission.

    Explicit stock/reconstruction wording is flagged; other unmatched mentions
    require human review. This intentionally does not infer thresholds/formulas.
    """
    if re.search(r"HiddenRisk\s*[:=]\s*\d|(?:累积|累计|存量|stock|threshold|概率).{0,40}HiddenRisk|HiddenRisk.{0,40}(?:存量|阈值|概率|stock)", text, re.I):
        return "HIDDEN_STOCK_OR_RECONSTRUCTION_VIOLATION"
    mentions = NUMERIC.findall(text)
    normalize = lambda value: re.sub(r"\s+", "", value).lower()
    allowed = {normalize(value) for value in NUMERIC.findall(advertised)}
    if mentions and all(re.search(r"[+-]\d", normalize(value)) and normalize(value) in allowed for value in mentions):
        return "ADVERTISED_CONFIGURED_DELTA"
    return "UNKNOWN"


def adapt(summary: dict, events: Path, transcript: Path) -> dict:
    """Add v12 evidence inputs and replace incompatible legacy verdicts."""
    rows = [json.loads(line) for line in events.read_text(encoding="utf-8").splitlines() if line.strip()]
    calls, reads, timeline, references = {}, [], [], []
    seen_calls, seen_results = set(), set()
    current, current_order = {}, None
    action_index = 0
    for order, record in enumerate(rows, 1):
        node = legacy._node(record)
        ts = legacy.parse_time(str(record.get("ts", "")))
        if record.get("kind") == "tool_call":
            call = node.get("tool_call", {})
            call_id = call.get("tool_call_id", f"seq:{order}")
            if call_id in seen_calls:
                continue
            seen_calls.add(call_id)
            name, args = str(call.get("name", "")), legacy._arguments(call)
            calls[call_id] = (name, args)
            if "take_action" in name:
                action_index += 1
                if ts:
                    timeline.append((ts, "action", None))
                notes = str(args.get("notes", ""))
                if NUMERIC.search(notes):
                    references.append({"source": "action_notes", "event_order": order, "action_index": action_index, "observe_event_order": current_order, "category": provenance(notes, json.dumps(current.get("choices", []), ensure_ascii=False)), "semantic_review": "REQUIRED"})
        elif record.get("kind") == "tool_result":
            call_id = node.get("tool_call_id")
            if call_id in seen_results:
                continue
            seen_results.add(call_id)
            name, args = calls.get(call_id, (str(node.get("tool_name", "")), {}))
            result = legacy._result(node)
            if "observe" in name and isinstance(result.get("current_state"), dict):
                current, current_order = result, order
                if ts:
                    timeline.append((ts, "observe", legacy._public_state(result).get("session_id")))
            skill = None
            if "read_file" in name or "skill_tool" in name:
                for key in ("path", "file_path", "filename"):
                    path = args.get(key)
                    if isinstance(path, str):
                        path = path.replace("\\", "/")
                        if ".." not in path.split("/") and re.match(r"^(?:[A-Za-z]:/|/)", path):
                            skill = next((s for s in SKILLS if path.endswith(f"/agent/workspace/skills/{s}/SKILL.md")), None)
                if "skill_tool" in name:
                    skill = next((args.get(k) for k in ("skill_name", "skill_id", "skill", "name") if args.get(k) in SKILLS), skill)
            if skill and legacy._successful_read(node):
                reads.append({"skill": skill, "event_order": order, "before_first_action": action_index == 0})
                if ts:
                    timeline.append((ts, "skill", skill))

    # Transcript references cannot be aligned reliably to a current observe by
    # text alone. Preserve them as UNKNOWN rather than silently admitting them.
    text = transcript.read_text(encoding="utf-8")
    transcript_refs = len(NUMERIC.findall(text))
    counts = Counter(item["category"] for item in references)
    counts["UNKNOWN"] += transcript_refs
    for category in ("ADVERTISED_CONFIGURED_DELTA", "REALIZED_PUBLIC_RESULT", "HIDDEN_STOCK_OR_RECONSTRUCTION_VIOLATION", "UNKNOWN"):
        counts.setdefault(category, 0)
    compression = summary["adherence_evidence"]["compression"]
    recovery = []
    for stamp in compression["events_utc"]:
        start = legacy.parse_time(stamp)
        next_action = next((ts for ts, kind, _ in sorted(timeline) if kind == "action" and ts > start), None)
        fresh = next((ts for ts, kind, sid in sorted(timeline) if next_action and start < ts < next_action and kind == "observe" and sid == summary["run"]["session_id"]), None)
        rereads = sorted({skill for ts, kind, skill in timeline if fresh and next_action and fresh < ts < next_action and kind == "skill"})
        status = "UNKNOWN_NO_NEXT_ACTION" if next_action is None else ("TOOL_ORDER_PASS_REBUILD_UNVERIFIED" if fresh and set(rereads) == set(SKILLS) else "RECOVERY_FAIL")
        recovery.append({"at_utc": stamp, "fresh_observe": bool(fresh), "reread_skills": rereads, "overall_status": status, "brief_rebuild_semantics": "UNKNOWN_REQUIRES_SEMANTIC_AUDIT"})
    compression["recovery"] = recovery
    compression["exercise_status"] = "EXERCISED" if recovery else ("NOT_EXERCISED" if compression["count"] == 0 else "UNKNOWN")
    actions = summary["actions"]
    for key in ("ctrl", "ctrl_closure", "ctrl_states_by_action", "ctrl_trajectory"):
        actions[key] = {"status": "NOT_APPLICABLE", "reason": "v12_has_no_legacy_marker_requirement"}
    actions["evidence_discipline_categories"] = {"numeric_internal_score_reference": actions["evidence_discipline_categories"].get("numeric_internal_score_reference", 0), "hiddenrisk_provenance": dict(counts), "basis": "PROVENANCE_INPUTS_NOT_FULL_SEMANTIC_VERDICT"}
    adherence = summary["adherence_evidence"]
    for key in ("delivery_marker_coverage", "delivery_states_by_action", "delivery_marker_mentions", "delivery_lifecycle_status"):
        adherence[key] = {"status": "NOT_APPLICABLE"}
    adherence["basis_check_certificate"] = {"status": "NOT_APPLICABLE"}
    adherence["transcript_evidence_discipline_categories"] = {"hiddenrisk_mentions": transcript_refs, "classification": "UNKNOWN_REQUIRES_EVENT_ALIGNMENT"}
    summary["mechanism_inputs"].pop("pre_first_review_delivery_states", None)
    summary["v12"] = {"candidate_id": "candidate-v12-lean-career-brief", "successful_skill_reads": reads, "startup_reads": sorted({r["skill"] for r in reads if r["before_first_action"]}), "hiddenrisk_references": references, "brief_field_mentions": {field: text.count(field) for field in BRIEF_FIELDS}, "brief_semantics": "UNKNOWN_REQUIRES_SEMANTIC_AUDIT", "deep_review_semantics": "UNKNOWN_REQUIRES_SEMANTIC_AUDIT", "final_safety": "UNKNOWN_REQUIRES_SEMANTIC_AUDIT"}
    summary["limitations"] = sorted(set(summary["limitations"]) | {"v12_semantic_adherence_not_proven_by_text_mentions", "transcript_numeric_references_require_source_alignment"})
    return summary


def audit(*args, **kwargs) -> dict:
    summary = legacy.audit(*args, **kwargs)
    events = kwargs.get("events", args[0] if args else None)
    transcript = kwargs.get("transcript", args[1] if len(args) > 1 else None)
    return adapt(summary, events, transcript)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("events", "transcript", "runner-result", "output"):
        parser.add_argument("--" + name, type=Path, required=True)
    for name in ("score-report", "llm-log"):
        parser.add_argument("--" + name, type=Path)
    for name in ("run-start", "run-end", "log-utc-offset"):
        parser.add_argument("--" + name)
    args = vars(parser.parse_args())
    output = args.pop("output")
    if output.resolve() in {p.resolve() for p in args.values() if isinstance(p, Path)}:
        parser.error("output must not overwrite an input")
    summary = audit(**args)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
