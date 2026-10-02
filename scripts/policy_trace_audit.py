"""Offline v10a decision-trace measurement. No provider, game, DB or runtime imports.

Markers are public reasoning claims, not an oracle of policy correctness. Missing
or ambiguous core traces fail measurement readiness instead of becoming zero.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re

from scripts.post_run_audit import CTRL, DL, INTERNAL_MARKER, _arguments, _node, _public_state, _result, parse_time

SCHEMA_VERSION = 1
POL = re.compile(r"\[POL B=(PROTECT|DELIVER|RESPONSIVE|OWNERSHIP|VISIBILITY|PROBE|OTHER) F=(S|N|O|MAIN|STORY|RESOURCE|OTHER) RP=(GAIN|NO_GAIN|UNKNOWN|NA)\]")
PROBE = re.compile(r"\[PROBE K=([01?]{5}) E=([01?]) C=([01?]) S=([01?]) F=(S|N|O|OTHER|NONE|\?)\]")
DIMENSIONS = {"S": "skill", "N": "network", "O": "output"}


def parse_header(notes: str) -> dict:
    """Consume the existing header contract; never relax or rewrite its parser."""
    c, d = CTRL.match(notes), DL.search(notes)
    valid = bool(c and d and notes.count('[CTRL') == notes.count('[DL') == 1)
    if valid:
        valid &= notes[c.end():d.start()] in (' ', '\n', '\r\n')
        valid &= not INTERNAL_MARKER.search(d[0])
        n, item = int(d['n']), d['item_id']
        valid &= item is None or (n == 0 and item == 'NONE') or (n > 0 and item != 'NONE')
        valid &= (n == 0 and d['focus']=='NONE' and d['evidence']=='NA' and d['checkpoint'] in ('0','NOT_NEAR') and d['recognition']=='0') or (n > 0 and d['focus']!='NONE' and d['evidence']!='NA')
    return dict(valid=bool(valid), mode=c['phase'] if c else None,
                delivery=d.groupdict() if valid else None)


def parse_trace(notes: str) -> dict:
    """Strict parse and consistency; no inference from prose or hidden fields."""
    p, q = POL.search(notes), PROBE.search(notes)
    if notes.count("[POL") != 1 or notes.count("[PROBE") != 1 or not p or not q:
        return {"status": "MISSING_OR_MALFORMED"}
    basis, family, prior = p.groups()
    k, eligible, compared, selected, probe_family = q.groups()
    expected = "1" if k == "11111" else "0" if "0" in k else "?"
    valid = eligible == expected and ((basis == "PROBE") == (selected == "1"))
    if eligible == "1":
        valid &= compared == "1" and selected in "01" and probe_family in (*DIMENSIONS, "OTHER")
    elif eligible == "0":
        valid &= compared == selected == "0" and probe_family == "NONE"
    else:
        valid &= compared == "?" and selected == "0" and probe_family == "?"
    if selected == "1":
        valid &= prior == "UNKNOWN"
        valid &= family == probe_family
    return dict(status=("AMBIGUOUS" if eligible == "?" else "VALID") if valid else "INCONSISTENT",
                basis=basis, family=family, response_prior=prior,
                conditions=k, eligible=eligible, compared=compared,
                selected=selected, probe_family=probe_family)


def fresh_response(row: dict) -> str:
    before, after = row["before"], row.get("after", {})
    if not row.get("fresh_after") or row.get("receipt") != "SUCCESS":
        return "UNKNOWN_OR_MIXED"
    if before.get("level") != after.get("level") or row["month"] != row.get("after_month") or row.get("new_feed"):
        return "UNKNOWN_OR_MIXED"
    family = row["trace"].get("probe_family")
    dims = [DIMENSIONS[family]] if family in DIMENSIONS else row["advertised_dimensions"]
    if not dims or any(not isinstance(before.get(d), (int, float)) or not isinstance(after.get(d), (int, float)) for d in dims):
        return "UNKNOWN_OR_MIXED"
    delta = [after[d] - before[d] for d in dims]
    if any(d > 0 for d in delta):
        return "GAIN"
    return "NO_GAIN" if all(d == 0 for d in delta) else "UNKNOWN_OR_MIXED"


def extract(events: Path, run_start: str, run_end: str) -> dict:
    start, end = parse_time(run_start), parse_time(run_end)
    if start is None or end is None or start > end:
        raise ValueError("explicit timezone-aware run window required")
    latest, session, pending = None, None, None
    seen_calls, seen_results, rows, by_id = set(), set(), [], {}
    action_notes = []
    sequence_errors = 0
    for line in events.read_text(encoding="utf-8").splitlines():
        record = json.loads(line)
        stamp = parse_time(str(record.get("ts", "")))
        if stamp is None:
            raise ValueError("event timestamp unavailable")
        if not start <= stamp <= end:
            continue
        n = _node(record)
        if record.get("kind") == "tool_call":
            call = n.get("tool_call", {}); cid = call.get("tool_call_id")
            if not cid or cid in seen_calls:
                continue
            seen_calls.add(cid)
            if "take_action" not in str(call.get("name", "")):
                continue
            args = _arguments(call)
            if latest is None:
                raise ValueError("action lacks same-session fresh observe")
            if pending is not None:
                sequence_errors += 1
            if args.get("session_id") != session:
                raise ValueError("action session mismatch")
            choices = latest.get("choices", [])
            option = next((v for v in choices if v.get("choice") == args.get("choice") and type(args.get("choice")) is int), None)
            if option is None:
                raise ValueError("action choice not in current public menu")
            pub = _public_state(latest)
            row = dict(action=len(rows)+1, seq=record["seq"], observe_seq=latest["_source_seq"],
                       month=pub["time"].get("current_month"), before=pub["status"],
                       event=latest.get("current_event", {}).get("title"),
                       choice=args["choice"], selected_family=option.get("action"),
                       advertised_dimensions=[k.lower() for k,v in option.get("status_updates", {}).items() if k.lower() in DIMENSIONS.values() and isinstance(v, (int, float)) and v > 0],
                       trace=parse_trace(str(args.get("notes", ""))),
                       header=parse_header(str(args.get("notes", ""))), receipt="UNKNOWN", fresh_after=False)
            rows.append(row); by_id[cid] = row
            action_notes.append(str(args.get('notes', '')))
            pending = row
        elif record.get("kind") == "tool_result":
            cid = n.get("tool_call_id")
            if not cid or cid in seen_results:
                continue
            seen_results.add(cid); data = _result(n)
            name = str(n.get("tool_name", ""))
            if "take_action" in name and cid in by_id:
                by_id[cid]["receipt"] = "SUCCESS" if data.get("success") is True else "FAIL" if data.get("success") is False else "UNKNOWN"
            elif "observe" in name and data.get("current_state"):
                pub = _public_state(data)
                observed_session = pub.get("session_id")
                if not observed_session or (session is not None and session != observed_session):
                    raise ValueError("observe session mismatch")
                session = observed_session
                if pending is not None:
                    pending.update(after=pub["status"], after_month=pub["time"].get("current_month"),
                                   after_seq=record["seq"], fresh_after=True,
                                   new_feed=bool(data.get("events")) and data.get("events") != latest.get("events"))
                    pending = None
                latest = dict(data, _source_seq=record["seq"])
    covered = [r for r in rows if r["trace"]["status"] == "VALID"]
    usable = bool(rows) and len(covered) == len(rows) and sequence_errors == 0 and all(r["fresh_after"] and r["receipt"] == "SUCCESS" and r['header']['valid'] for r in rows)
    counts = Counter(); basis = Counter(); chains = 0; repeats = 0; level_resets = 0
    previous = None
    for row in rows:
        t = row["trace"]
        if t["status"] == "VALID":
            basis[t["basis"]] += 1
            counts["probe_eligible_count"] += t["eligible"] == "1"
            counts["probe_compared_count"] += t["compared"] == "1"
            counts["probe_selected_count"] += t["selected"] == "1"
            k = t["conditions"]
            counts["probe_blocked_by_binding_constraint_count"] += k[0] == "1" and (k[3] == "0" or k[4] == "0")
            if t["selected"] == "1":
                response = fresh_response(row)
                row["probe_response"] = response
                counts[{"GAIN":"probe_GAIN_count", "NO_GAIN":"probe_NO_GAIN_count", "UNKNOWN_OR_MIXED":"probe_UNKNOWN_count"}[response]] += 1
            if previous and previous["trace"].get("selected") == t["selected"] == "1":
                chains += 1
        if previous:
            level_resets += previous["before"].get("level") != row["before"].get("level")
            same_family = previous["selected_family"] == row["selected_family"] and previous["before"].get("level") == row["before"].get("level")
            if same_family and previous["advertised_dimensions"] and fresh_response(previous) == "NO_GAIN":
                repeats += 1
        previous = row
    metric_names = ("probe_eligible_count", "probe_compared_count", "probe_selected_count", "probe_GAIN_count", "probe_NO_GAIN_count", "probe_UNKNOWN_count", "probe_blocked_by_binding_constraint_count")
    # Optional v10c receipts do not change historical trace parsing/readiness.
    from scripts.basis_preflight_audit import measure_receipts
    basis_preflight = measure_receipts(action_notes)
    metrics = {name: counts[name] if usable else None for name in metric_names}
    metrics["consecutive_probe_violations"] = chains if usable else None
    return dict(schema_version=SCHEMA_VERSION,
                source=dict(events_sha256=hashlib.sha256(events.read_bytes()).hexdigest(), run_start=run_start, run_end=run_end),
                measurement_status="PASS" if usable else "STOP_BEFORE_PROVIDER",
                interpretation="Public trace claims and attributable numeric responses; not LLM semantic correctness or causal value.",
                actions=len(rows), trace_covered=len(covered), trace_statuses=dict(Counter(r["trace"]["status"] for r in rows)),
                action_fresh_observe=sum(r["fresh_after"] for r in rows), sequence_errors=sequence_errors,
                metrics=metrics, confirmed_lower_bounds={name:counts[name] for name in metric_names},
                basis_counts=dict(basis), level_reset_events=level_resets,
                mode_counts=dict(Counter(r['header']['mode'] for r in rows)),
                valid_delivery_headers=sum(r['header']['valid'] for r in rows),
                immediate_local_NO_GAIN_repeats=repeats, basis_preflight=basis_preflight, rows=rows)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--events", type=Path, required=True)
    parser.add_argument("--run-start", required=True)
    parser.add_argument("--run-end", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.resolve() == args.events.resolve():
        parser.error("output must not overwrite raw evidence")
    summary = extract(args.events, args.run_start, args.run_end)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(summary, ensure_ascii=False, indent=2)+'\n', encoding="utf-8")
    print(args.output)
    return 0 if summary["measurement_status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
