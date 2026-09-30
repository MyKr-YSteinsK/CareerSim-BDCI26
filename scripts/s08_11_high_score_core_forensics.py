"""Extract public action-mix facts from four explicitly identified CareerSim runs.

This offline parser consumes only selected legal-choice labels from take_action,
the preceding participant-visible choices, and a strict public-state allowlist.
It intentionally ignores action notes, transcripts, event descriptions, scores,
hidden/internal fields, and all unrelated event payload data.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any


RUN_ORDER = ("v6", "v7o", "v7t", "v7v")
CANDIDATE_SOURCE_COMMITS = {
    "v6": "1114a04b75548cf52f030d123564e527060fc061",
    "v7o": "b2e7ea6441da9c314d8a0ffbf29b9d5800ced10d",
    "v7t": "e4ec82958ccfcac23ca8b28af14e69be1c470fa2",
    "v7v": "fd30db289d4c16fbcd587bb61b40cb0117cab396",
}
PUBLIC_STATUS = {
    "level",
    "health",
    "dignity",
    "skill",
    "network",
    "output",
    "wealth",
    "energy",
    "duration_in_level",
}
PHASES = (
    ("M1-M18", 1, 18),
    ("M19-M36", 19, 36),
    ("M37-M48", 37, 48),
)
REVIEW_WINDOWS = (
    ("M1-M6", 1, 6),
    ("M7-M12", 7, 12),
    ("M13-M18", 13, 18),
)
ENERGY_TARGET = {
    "OUTPUT_VISIBILITY": "output",
    "SKILL_GROWTH": "skill",
    "NETWORK_GROWTH": "network",
    "HEALTH_RECOVERY": "health",
    "DIGNITY_RECOVERY": "dignity",
}
SESSION_RE = re.compile(r"[0-9a-fA-F]{32}\Z")


@dataclass(frozen=True)
class RunSpec:
    name: str
    events_path: Path
    session_id: str


def _node(record: dict[str, Any]) -> dict[str, Any]:
    payload = record.get("payload")
    if not isinstance(payload, dict):
        return {}
    delta = payload.get("delta")
    if isinstance(delta, dict) and "tool_call" not in payload and "raw_output" not in payload:
        return delta
    return payload


def _decoded_object(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        return value
    if isinstance(value, str):
        try:
            decoded = json.loads(value)
        except json.JSONDecodeError:
            return {}
        return decoded if isinstance(decoded, dict) else {}
    return {}


def _call_arguments(call: dict[str, Any]) -> dict[str, Any]:
    return _decoded_object(call.get("arguments"))


def _tool_result(node: dict[str, Any]) -> dict[str, Any]:
    raw = node.get("raw_output")
    if not isinstance(raw, dict):
        return {}
    return _decoded_object(raw.get("result"))


def _action_result(node: dict[str, Any]) -> str:
    raw = node.get("raw_output")
    raw = raw if isinstance(raw, dict) else {}
    result = _tool_result(node)
    if result.get("success") is True or raw.get("success") is True:
        return "SUCCESS"
    if (
        result.get("success") is False
        or raw.get("success") is False
        or node.get("is_error")
        or node.get("error")
        or raw.get("isError")
        or raw.get("error")
        or result.get("isError")
        or result.get("error")
    ):
        return "ERROR"
    return "UNKNOWN"


def _public_snapshot(result: dict[str, Any]) -> dict[str, Any]:
    state = result.get("current_state")
    state = state if isinstance(state, dict) else {}
    status = state.get("status")
    status = status if isinstance(status, dict) else {}
    time = state.get("time")
    time = time if isinstance(time, dict) else {}
    public_status = {
        str(key).lower(): value
        for key, value in status.items()
        if str(key).lower() in PUBLIC_STATUS
        and isinstance(value, (str, int, float))
        and not isinstance(value, bool)
    }
    public_time = {
        key: time[key]
        for key in ("current_month", "current_quarter", "current_year")
        if isinstance(time.get(key), int) and not isinstance(time.get(key), bool)
    }
    return {
        "session_id": state.get("session_id") or result.get("session_id"),
        "time": public_time,
        "status": public_status,
    }


def _choice_map(result: dict[str, Any]) -> dict[int, str]:
    choices = result.get("choices")
    if not isinstance(choices, list):
        return {}
    output: dict[int, str] = {}
    for item in choices:
        if not isinstance(item, dict):
            continue
        number = item.get("choice")
        label = item.get("action")
        if isinstance(number, int) and not isinstance(number, bool) and isinstance(label, str):
            output[number] = label
    return output


def _action_kind(event_title: str) -> str:
    title = event_title.strip()
    if title == "季度主行动选择":
        return "main"
    if title == "季度体力行动分配":
        return "energy"
    return "other"


def _category(label: str, kind: str) -> str:
    text = label.casefold()
    if kind == "main":
        if "关键项目" in label or "key project" in text:
            return "Apply/Key Project"
        if any(token in label for token in ("汇报成果", "汇报结果", "汇报工作")) or "report results" in text:
            return "Report/Results"
        if "低调避险" in label or "low-profile" in text or "risk avoidance" in text:
            return "Low-profile/Risk avoidance"
        return "Other"
    if kind != "energy":
        return "OTHER"
    if "准备汇报材料" in label or "report preparation" in text:
        return "OUTPUT_VISIBILITY"
    if "技能学习" in label or "技能训练" in label or "skill learning" in text or "skill training" in text:
        return "SKILL_GROWTH"
    if any(token in label for token in ("人脉维护", "建立导师关系")) or "network maintenance" in text or "mentor relationship" in text:
        return "NETWORK_GROWTH"
    if "健康恢复" in label or "health recovery" in text:
        return "HEALTH_RECOVERY"
    if "心理修复" in label or "尊严恢复" in label or "dignity recovery" in text:
        return "DIGNITY_RECOVERY"
    if "处理历史埋雷" in label or "risk cleanup" in text:
        return "RISK_CLEANUP"
    return "OTHER"


def _period(month: Any, periods: tuple[tuple[str, int, int], ...]) -> str | None:
    if not isinstance(month, int) or isinstance(month, bool):
        return None
    return next((name for name, lower, upper in periods if lower <= month <= upper), None)


def _mix(rows: list[dict[str, Any]], kind: str, periods: tuple[tuple[str, int, int], ...]) -> dict[str, Any]:
    selected = [row for row in rows if row["kind"] == kind and row["label"] is not None]
    output: dict[str, Any] = {"total": len(selected), "periods": []}
    for period_name, lower, upper in periods:
        subset = [row for row in selected if isinstance(row["month"], int) and lower <= row["month"] <= upper]
        category_counts = Counter(row["category"] for row in subset)
        label_counts = Counter(row["label"] for row in subset)
        denominator = len(subset)
        output["periods"].append(
            {
                "name": period_name,
                "count": denominator,
                "categories": [
                    {"category": key, "count": count, "share": round(count / denominator, 4) if denominator else 0.0}
                    for key, count in sorted(category_counts.items())
                ],
                "action_labels": [
                    {"label": key, "count": count, "share": round(count / denominator, 4) if denominator else 0.0}
                    for key, count in sorted(label_counts.items())
                ],
            }
        )
    output["outside_or_unknown_month"] = sum(
        1 for row in selected if _period(row["month"], periods) is None
    )
    return output


def _energy_responses(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    counts: Counter[tuple[str, str, str, str]] = Counter()
    for row in rows:
        if row["kind"] != "energy" or row["label"] is None:
            continue
        target = ENERGY_TARGET.get(row["category"])
        before = row["before"].get(target) if target else None
        after = row["after"].get(target) if target and row["after"] else None
        if not isinstance(before, (int, float)) or isinstance(before, bool) or not isinstance(after, (int, float)) or isinstance(after, bool):
            response = "UNATTRIBUTABLE"
        elif after > before:
            response = "GAIN"
        elif after == before:
            response = "NO_GAIN"
        else:
            response = "DECLINE"
        counts[(row["category"], row["label"], target or "NONE", response)] += 1
    return [
        {"category": category, "action": action, "public_dimension": target, "observed_response": response, "count": count}
        for (category, action, target, response), count in sorted(counts.items())
    ]


def _file_identity(path: Path) -> dict[str, Any]:
    digest = hashlib.sha256()
    size = 0
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            size += len(block)
            digest.update(block)
    return {"path": str(path.resolve()), "bytes": size, "sha256": digest.hexdigest()}


def extract_run(spec: RunSpec) -> dict[str, Any]:
    if spec.name not in CANDIDATE_SOURCE_COMMITS:
        raise ValueError(f"unsupported run name: {spec.name}")
    if not SESSION_RE.fullmatch(spec.session_id):
        raise ValueError("run session identity must be an explicit 32-character hex value")
    if not spec.events_path.is_file():
        raise FileNotFoundError(spec.events_path)

    identity = _file_identity(spec.events_path)
    calls: dict[str, dict[str, Any]] = {}
    action_by_id: dict[str, dict[str, Any]] = {}
    seen_call_ids: set[str] = set()
    seen_result_ids: set[str] = set()
    actions: list[dict[str, Any]] = []
    latest: dict[str, Any] | None = None
    pending_action: dict[str, Any] | None = None
    observations: list[dict[str, Any]] = []
    missing_observe_boundaries = 0
    take_action_without_session_arg = 0

    with spec.events_path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.strip():
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"events line {line_number} is not valid JSON") from exc
            if not isinstance(record, dict):
                raise ValueError(f"events line {line_number} is not an object")
            kind = record.get("kind")
            node = _node(record)

            if kind == "tool_call":
                call = node.get("tool_call")
                if not isinstance(call, dict):
                    continue
                call_id = str(call.get("tool_call_id") or f"seq:{record.get('seq', line_number)}")
                if call_id in seen_call_ids:
                    continue
                seen_call_ids.add(call_id)
                name = str(call.get("name") or "")
                args = _call_arguments(call)
                calls[call_id] = {"name": name}
                if "take_action" not in name:
                    continue
                if pending_action is not None and pending_action["after"] is None:
                    missing_observe_boundaries += 1
                    pending_action = None
                action_session = args.get("session_id")
                if latest is None or latest["session_id"] != spec.session_id:
                    continue
                if action_session is not None and action_session != spec.session_id:
                    continue
                if action_session is None:
                    # Bind a malformed call only to the immediately preceding same-session observe.
                    take_action_without_session_arg += 1
                choice = args.get("choice")
                label = latest["choices"].get(choice) if isinstance(choice, int) and not isinstance(choice, bool) else None
                title = latest["event_title"]
                action_kind = _action_kind(title)
                row = {
                    "month": latest["month"],
                    "level": latest["status"].get("level"),
                    "kind": action_kind,
                    "category": _category(label, action_kind) if isinstance(label, str) else "OTHER",
                    "label": label if isinstance(label, str) else None,
                    "before": latest["status"],
                    "after": None,
                    "result": "UNKNOWN",
                }
                actions.append(row)
                action_by_id[call_id] = row
                continue

            if kind != "tool_result":
                continue
            call_id = str(node.get("tool_call_id") or "")
            if not call_id or call_id in seen_result_ids:
                continue
            seen_result_ids.add(call_id)
            call_name = str(node.get("tool_name") or calls.get(call_id, {}).get("name") or "")

            if "take_action" in call_name and call_id in action_by_id:
                row = action_by_id[call_id]
                row["result"] = _action_result(node)
                if row["result"] == "SUCCESS":
                    pending_action = row
                continue

            if "observe" not in call_name:
                continue
            result = _tool_result(node)
            if not isinstance(result.get("current_state"), dict):
                continue
            public = _public_snapshot(result)
            if public["session_id"] != spec.session_id:
                if pending_action is not None and pending_action["after"] is None:
                    missing_observe_boundaries += 1
                    pending_action = None
                continue
            event = result.get("current_event")
            event = event if isinstance(event, dict) else {}
            snapshot = {
                "month": public["time"].get("current_month"),
                "status": public["status"],
                "event_title": str(event.get("title") or ""),
                "choices": _choice_map(result),
                "session_id": public["session_id"],
            }
            observations.append(snapshot)
            if pending_action is not None and pending_action["after"] is None:
                pending_action["after"] = public["status"]
                pending_action = None
            latest = snapshot

    if pending_action is not None and pending_action["after"] is None:
        missing_observe_boundaries += 1

    successful = [row for row in actions if row["result"] == "SUCCESS"]
    final_public = observations[-1] if observations else None
    checkpoint_public_states = {}
    for month in (6, 12, 18, 24, 30, 36, 42, 48):
        checkpoint = next((item for item in reversed(observations) if item["month"] == month), None)
        checkpoint_public_states[f"M{month}"] = checkpoint["status"] if checkpoint else "UNKNOWN"
    review_adjacent_story_actions = []
    for row in successful:
        month = row["month"]
        if row["kind"] != "other" or row["label"] is None or not isinstance(month, int):
            continue
        for review_month in (6, 12, 18, 24, 30, 36, 42, 48):
            if review_month - 2 <= month <= review_month:
                review_adjacent_story_actions.append(
                    {
                        "review_month": review_month,
                        "month": month,
                        "selected_legal_action": row["label"],
                    }
                )
    promotions: list[dict[str, Any]] = []
    previous_level: Any = None
    for snapshot in observations:
        level = snapshot["status"].get("level")
        if level is not None and previous_level is not None and level != previous_level:
            promotions.append({"month": snapshot["month"], "from_level": previous_level, "to_level": level})
        if level is not None:
            previous_level = level

    classified = [row for row in successful if row["kind"] in {"main", "energy"}]
    return {
        "run": spec.name,
        "candidate_id": {
            "v6": "candidate-v6-auditable-control-loop",
            "v7o": "candidate-v7o-execution-persistence-convergence",
            "v7t": "candidate-v7t-execution-semantic-repair",
            "v7v": "candidate-v7v-preflight-ordering-repair",
        }[spec.name],
        "candidate_source_commit": CANDIDATE_SOURCE_COMMITS[spec.name],
        "events": identity,
        "observes_in_session": len(observations),
        "take_action_attempts_in_session": len(actions),
        "take_action_successes": sum(row["result"] == "SUCCESS" for row in actions),
        "take_action_errors": sum(row["result"] == "ERROR" for row in actions),
        "take_action_unknown_results": sum(row["result"] == "UNKNOWN" for row in actions),
        "take_action_without_session_arg": take_action_without_session_arg,
        "unclassified_or_other_successes": sum(
            row["kind"] not in {"main", "energy"} or row["label"] is None for row in successful
        ),
        "missing_action_to_observe_boundaries": missing_observe_boundaries,
        "final_public_state": {
            "month": final_public["month"],
            "status": final_public["status"],
        } if final_public else "UNKNOWN",
        "last_public_state_at_review_month": checkpoint_public_states,
        "observed_level_changes": promotions,
        "review_adjacent_story_actions": review_adjacent_story_actions,
        "action_mix_by_run_phase": {
            "main": _mix(classified, "main", PHASES),
            "energy": _mix(classified, "energy", PHASES),
        },
        "action_mix_by_early_review_window": {
            "main": _mix(classified, "main", REVIEW_WINDOWS),
            "energy": _mix(classified, "energy", REVIEW_WINDOWS),
        },
        "energy_public_before_after_response": _energy_responses(classified),
    }


def build_report(specs: list[RunSpec]) -> dict[str, Any]:
    names = [spec.name for spec in specs]
    if len(names) != len(set(names)) or set(names) != set(RUN_ORDER):
        raise ValueError("exactly one explicit events path and session identity is required for v6, v7o, v7t, and v7v")
    by_name = {spec.name: spec for spec in specs}
    return {
        "schema_version": 1,
        "evidence_policy": "PUBLIC_LEGAL_CHOICES_AND_WHITELISTED_PUBLIC_STATUS_ONLY",
        "excluded_inputs_and_fields": [
            "action notes",
            "transcript content",
            "current-event descriptions and identifiers",
            "hidden/internal state and score fields",
            "provider, service, and database evidence",
        ],
        "interpretation_limit": "before-after status changes are descriptive associations, not causal action effects or hidden-cap evidence",
        "runs": [extract_run(by_name[name]) for name in RUN_ORDER],
    }


def _parse_run(value: str) -> RunSpec:
    parts = value.split("|", 2)
    if len(parts) != 3:
        raise ValueError("--run must be NAME|EXPLICIT_EVENTS_PATH|SESSION_ID")
    name, path, session_id = parts
    if not name or not path or not session_id:
        raise ValueError("--run must include a name, explicit events path, and session identity")
    return RunSpec(name=name, events_path=Path(path), session_id=session_id)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", action="append", required=True, metavar="NAME|EVENTS|SESSION_ID")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(".local/scratch/s08-11/high_score_core_forensics.json"),
    )
    args = parser.parse_args(argv)
    try:
        specs = [_parse_run(value) for value in args.run]
        report = build_report(specs)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    print(f"wrote {args.output.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
