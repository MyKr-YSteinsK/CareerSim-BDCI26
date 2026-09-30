"""Exact-source, public-only resource timelines for S09-04; never runs a game.

Reuses S09-02 attribution/deduplication. Legal menus are evidence, not an
effect/answer map. Intervention, fragility and reasonableness are human review.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from scripts.s09_02_failure_floor_joint_forensics import extract_records, snapshot
from scripts.s08_11_high_score_core_forensics import _decoded_object, _node, _tool_result

ROOT = Path(__file__).resolve().parents[1]
LOCAL = ROOT / ".career_sim_runner/career_emu/outputs/local-s06-adaptive-controller"


@dataclass(frozen=True)
class Source:
    name: str
    stamp: str
    session: str
    months: int
    events_bytes: int
    events_sha256: str
    transcript_bytes: int
    transcript_sha256: str
    report: str
    window: tuple[str, str] | None = None


# Identities registered in the canonical reports before this task.
SOURCES = (
    Source("v7x", "20260930T131104Z", "700f8ed814844694869d93461e7ef748", 8,
           376682, "8e757e1f207c54c10c7ce9281bf8169c086b916e3ebac8784784775ec557be4a",
           79869, "333d4b1d05c11b75670f956aef964894c63697bbfa46d76519ea9596d0b69d52",
           "docs/project/runs/v7x-run1-validation.md",
           ("2026-09-30T13:11:04+00:00", "2026-09-30T13:14:16.638819+00:00")),
    Source("v4", "20260924T160806Z", "fdcaa70a85f44662a6a329513c175676", 6,
           263552, "9bf8bed1d02435047df40300ff306231dfa938b91cb87d3ef5b082e35d7359e5",
           44237, "fe20250c032c67d5681b6a7dd726114182b97bc180ee94768f95f99fae99d896",
           "docs/project/runs/v4-run1-health-forensic.md"),
)


def verified_bytes(path: Path, size: int, digest: str) -> bytes:
    content = path.read_bytes()
    if len(content) != size or hashlib.sha256(content).hexdigest() != digest:
        raise ValueError("canonical source identity mismatch; content withheld")
    return content


def validate_window(records: list[dict], window: tuple[str, str] | None) -> None:
    if window is None:
        return
    start, end = map(datetime.fromisoformat, window)
    for record in records:
        stamp = record.get("ts")
        if not isinstance(stamp, str):
            raise ValueError("missing timestamp for exact-window source")
        at = datetime.fromisoformat(stamp)
        if at.tzinfo is None or not start <= at <= end:
            raise ValueError("record outside authorized run window; content withheld")


def decision_menus(records: list[dict], session: str) -> dict[int, dict]:
    calls, seen_results, menus = {}, set(), {}
    latest = None
    for record in records:
        node = _node(record)
        if record.get("kind") == "tool_call":
            call = node.get("tool_call")
            if not isinstance(call, dict):
                continue
            call_id = call.get("tool_call_id")
            if not call_id or call_id in calls:
                continue
            name = str(call.get("name") or "")
            calls[call_id] = name
            if "take_action" in name and latest is not None:
                args = _decoded_object(call.get("arguments"))
                choice = args.get("choice")
                chosen = latest["choices"].get(choice) if isinstance(choice, int) and not isinstance(choice, bool) else None
                menus[record.get("seq", 0)] = {
                    "pre_observe_seq": latest["seq"],
                    "legal_choices": list(latest["choices"].values()),
                    "selected_public_choice": chosen,
                }
        elif record.get("kind") == "tool_result":
            call_id = node.get("tool_call_id")
            if not call_id or call_id in seen_results or call_id not in calls:
                continue
            seen_results.add(call_id)
            if "observe" in calls[call_id]:
                data = _tool_result(node)
                if not isinstance(data.get("current_state"), dict):
                    continue
                latest = snapshot(data, record.get("seq", 0))
                latest["choices"] = {key: value for key, value in latest["choices"].items() if type(key) is int}
                if latest["session"] != session:
                    raise ValueError("observe session mismatch; content withheld")
    return menus


def public_timeline(records: list[dict], session: str, months: int) -> dict:
    run = extract_records(records, session, months)
    menus = decision_menus(records, session)
    rows = []
    negative_since_recovery = 0
    for action in run["actions"]:
        menu = menus.get(action["seq"], {})
        before, after = action["before"], action["after"]
        delta = action["deltas"].get("health")
        if delta is None:
            trend = "UNKNOWN"
            negative_since_recovery = 0
        elif delta > 0:
            trend = "RECOVERING"
            negative_since_recovery = 0
        elif delta < 0:
            negative_since_recovery += 1
            trend = "REPEATED_ATTRITION" if negative_since_recovery > 1 else "DECLINING"
        else:
            trend = "STABLE"
        # A fixed projection; no notes, hidden flags/effects, IDs or scores.
        rows.append({
            "index": action["index"], "month": action["month"], "kind": action["kind"],
            "pre": before, "event": action["title"], "context": action["context"],
            "choice": menu.get("selected_public_choice"), "legal_choices": menu.get("legal_choices", []),
            "mode": action["mode"] or "UNKNOWN", "recovery": action["recovery"] or "UNKNOWN",
            "risk": action["risk"] or "UNKNOWN", "post": after,
            "post_month": action.get("after_month"), "post_context": action.get("post_context"),
            "delta_health": delta,
            "delta_class": {"ACTION_ATTRIBUTABLE": "CLEAN", "MIXED_OR_UNATTRIBUTABLE": "MIXED"}.get(action["attribution"], "UNKNOWN"),
            "attribution_reason": action["reason"], "trend": trend,
            "result": action["result"], "terminal_link": action["immediate_terminal"],
            "source_seq": {"pre_observe": menu.get("pre_observe_seq"), "action": action["seq"], "post_observe": action.get("post_seq")},
        })
    return {"decision_rows": rows, "observes": run["observes"], "actions": run["attempted"],
            "delta_class_counts": {key: sum(r["delta_class"] == key for r in rows) for key in ("CLEAN", "MIXED", "UNKNOWN")},
            "trend_definition": "Sign of public H delta; REPEATED_ATTRITION means >=2 negative changes since last positive/unknown delta. No runtime state/threshold or causal interpretation."}


def build_report() -> dict[str, Any]:
    runs = {}
    for spec in SOURCES:
        directory = LOCAL / spec.stamp
        events = directory / f"events-{spec.stamp}.jsonl"
        transcript = directory / f"transcript-{spec.stamp}.log"
        content = verified_bytes(events, spec.events_bytes, spec.events_sha256)
        # Verify held transcript identity; do not copy raw/private reasoning.
        verified_bytes(transcript, spec.transcript_bytes, spec.transcript_sha256)
        records = [json.loads(line) for line in content.decode("utf-8").splitlines() if line.strip()]
        validate_window(records, spec.window)
        runs[spec.name] = {
            "tier": "A", "canonical_report": spec.report,
            "sources": {"events": {"path": str(events.relative_to(ROOT)), "bytes": spec.events_bytes, "sha256": spec.events_sha256},
                        "transcript": {"path": str(transcript.relative_to(ROOT)), "bytes": spec.transcript_bytes, "sha256": spec.transcript_sha256}},
            "window_utc": spec.window or "exact hash-bound run file; no broader log read",
            **public_timeline(records, spec.session, spec.months),
        }
    return {"schema_version": 1, "task": "S09-04", "runs": runs,
            "limitations": "Public temporal deltas and menu semantics only; CLEAN is stream-attributable, not isolated causal choice effect. Intervention/fragility/ranking classifications require reviewer judgement. No unchosen effects or runtime calls."}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / ".local/scratch/s09-04/resource_trajectory.json")
    args = parser.parse_args()
    content = (json.dumps(build_report(), ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(content)
    print(json.dumps({"output": str(args.output), "bytes": len(content), "sha256": hashlib.sha256(content).hexdigest()}))


if __name__ == "__main__":
    main()
