"""Deterministic offline, public-only S09-02 cohort extraction.

No simulator/provider imports. Sources are exact recorded files or Git objects.
Month/Level/review transitions and batched/unknown actions never enter clean
action-shock statistics. Clean means stream-attributable, not causal isolation
of an event's stochastic outcome. No hidden effect or answer map is consulted.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any

from scripts.s08_11_high_score_core_forensics import (
    _action_kind, _action_result, _category, _decoded_object, _node,
    _public_snapshot, _tool_result,
)

ROOT = Path(__file__).resolve().parents[1]
HISTORY = "8a93378a8d9ef5598e925048db39ee931e207bab"
WINDOWS = ((1, 6), (7, 12), (13, 18), (19, 24), (25, 36), (37, 48))
STATS_DIMENSIONS = ("health", "wealth")
PUBLIC_DIMENSIONS = ("health", "wealth", "dignity", "skill", "network", "output")
LOCAL = ".career_sim_runner/career_emu/outputs/local-s06-adaptive-controller"
# Expected hashes were registered in formal Run records before this extraction.
LOCAL_RUNS = {
    "v4": ("20260924T160806Z", "fdcaa70a85f44662a6a329513c175676", 6, "9bf8bed1d02435047df40300ff306231dfa938b91cb87d3ef5b082e35d7359e5"),
    "v6": ("20260925T094419Z", "7b59b85ad19b4597927cf50fc716f9ac", 48, "2cce87eb6afd8aea5a9651f75621ae7c2b303e8c00c7f2ac417dc65c030371d8"),
    "v7d": ("20260927T143425Z", "5667ea7c7f7b4566ab805d05a2dc1b8c", 15, "e4e388517aff115747fabe068a76b1bc3d960b43900373d4eca804097348be78"),
    "v7g": ("20260928T055416Z", "d4464a311c924e73b9e23eebd6f71f6d", 48, "73cb4de9f2568e343be252630a64dbef289e92aec121bae07ef8fbd3a6cff3c4"),
    "v7i": ("20260928T112740Z", "cec080dd3c1d43a0b9cb92945e9a824e", 48, "a1c3bae1b775de9771a1e7ba3bfea4383f684f743b22ecfddd621c4b0399010c"),
}
ARCHIVE_RUNS = {
    "v7o": ("s08-run01-v7o", "ab65fb3e46964184b0936fee4d7b3c49", 48),
    "v7q": ("s08-run02-v7q", "e12d08fe0d0b4fb0b4cac12d5123839e", 24),
    "v7t": ("s08-run03-v7t", "7f50220814214d97a3dc453fca049a79", 48),
    "v7v": ("s08-run04-v7v", "6761193aab14417fac35125321eda37b", 48),
    "v7w": ("s09-run01-v7w", "57b66b2fb19f483ba9de86b23f160f4c", 24),
}
WARNING_TERMS = {
    "HEALTH": ("心悸", "胸闷", "感染", "急性", "眼前一黑", "健康恶化"),
    "CONTINUITY": ("信任危机", "裁员", "淘汰", "失业", "连续两次", "解除劳动"),
    "TRUST_COMPLIANCE": ("保密", "机密", "合规", "报复", "信任", "举报"),
    "PUBLIC_RISK": ("风险上升", "风险累积", "风险积累", "风险升高", "需要处理"),
    "DELIVERY": ("延期", "阻塞", "延迟", "验收", "交付"),
    "AFFORDABILITY": ("无法支付", "负担不起", "现金流", "资金紧张"),
}


def numeric(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def classify_pair(before: dict, after: dict | None, attempts: int, result: str,
                  explicit_session: bool, intervening_mutation: bool = False) -> tuple[str, str]:
    if not before or after is None or result != "SUCCESS" or not explicit_session:
        return "UNKNOWN", "missing_fresh_pair_receipt_or_session"
    if not isinstance(before.get("month"), int) or not isinstance(after.get("month"), int) or not before["status"].get("level") or not after["status"].get("level"):
        return "UNKNOWN", "missing_public_time_or_level"
    if attempts != 1 or intervening_mutation:
        return "MIXED_OR_UNATTRIBUTABLE", "multiple_or_unidentified_mutations"
    if before["month"] != after["month"]:
        return "MIXED_OR_UNATTRIBUTABLE", "month_transition"
    if before["status"].get("level") != after["status"].get("level"):
        return "MIXED_OR_UNATTRIBUTABLE", "level_transition"
    if any(before.get(k) != after.get(k) for k in ("quarter", "year")):
        return "MIXED_OR_UNATTRIBUTABLE", "quarter_or_year_transition"
    pre_energy, post_energy = before["status"].get("energy"), after["status"].get("energy")
    if numeric(pre_energy) and numeric(post_energy) and post_energy > pre_energy:
        return "MIXED_OR_UNATTRIBUTABLE", "energy_refill_or_automatic_boundary"
    if any(token in before["title"] + after["title"] for token in ("绩效", "晋升", "半年", "季度奖金")):
        return "MIXED_OR_UNATTRIBUTABLE", "review_or_automatic_settlement"
    return "ACTION_ATTRIBUTABLE", "one_success_fresh_same_month_level"


def snapshot(result: dict, seq: int) -> dict:
    public = _public_snapshot(result)
    event = result.get("current_event")
    event = event if isinstance(event, dict) else {}
    title = event.get("title") if isinstance(event.get("title"), str) else ""
    description = event.get("description") if isinstance(event.get("description"), str) else ""
    options = {}
    for choice in result.get("choices") or []:
        if not isinstance(choice, dict) or not isinstance(choice.get("choice"), int):
            continue
        options[choice["choice"]] = {
            key: choice[key] for key in ("action", "description") if isinstance(choice.get(key), str)
        }
    return dict(seq=seq, session=public["session_id"],
                month=public["time"].get("current_month"), status=public["status"],
                quarter=public["time"].get("current_quarter"), year=public["time"].get("current_year"),
                title=title, description=description, choices=options)


def markers(args: dict) -> dict:
    # Keep only enum evidence from the notes, never free-form reasoning.
    text = args.get("notes")
    text = text if isinstance(text, str) else ""
    def enum(pattern: str) -> str | None:
        match = re.search(pattern, text)
        return match.group(1) if match else None
    return {
        "mode": enum(r"\bP\s*=\s*(A|S)\b"),
        "risk": enum(r"\bR\s*=\s*(PASS|ALLOW|WARN|RECONSIDER|UNKNOWN)\b"),
        "recovery": enum(r"\bRECOVERY\s*[:=]\s*(NONE|PROGRESSION|RESOURCE|RISK|DELIVERY|UNKNOWN)\b"),
        "review_plan_literal": "REVIEW_PLAN" in text,
    }


def extract_records(records: list[dict], session: str, survival: int) -> dict:
    calls, seen_results = {}, set()
    observations, actions, interval = [], [], []
    latest = None
    intervening = False
    for record in records:
        node = _node(record)
        seq = record.get("seq", 0)
        if record.get("kind") == "tool_call":
            call = node.get("tool_call")
            if not isinstance(call, dict):
                continue
            call_id = call.get("tool_call_id")
            if not call_id or call_id in calls:
                continue
            args = _decoded_object(call.get("arguments"))
            name = str(call.get("name") or "")
            calls[call_id] = dict(name=name, seq=seq)
            if "take_action" in name:
                if latest is None:
                    continue
                supplied = args.get("session_id")
                if supplied is not None and supplied != session:
                    raise ValueError("action session differs from recorded identity; content withheld")
                selected = latest["choices"].get(args.get("choice"), {})
                label = selected.get("action")
                kind = _action_kind(latest["title"])
                kind = "story" if kind == "other" else kind
                row = dict(index=len(actions) + 1, seq=seq, month=latest["month"],
                           kind=kind, action=label, choice_description=selected.get("description"),
                           title=latest["title"], context=latest["description"],
                           category=_category(label or "", kind),
                           before=latest["status"], after=None, result="UNKNOWN",
                           explicit_session=supplied == session, result_seq=None,
                           attribution="UNKNOWN", reason="no_post_observe",
                           immediate_terminal=False, **markers(args))
                calls[call_id]["action"] = row
                actions.append(row)
                interval.append(row)
            elif latest and not any(read in name for read in
                                    ("observe", "read_file", "handbook", "check_latest_logs")):
                intervening = True
            continue
        if record.get("kind") != "tool_result":
            continue
        call_id = node.get("tool_call_id")
        if not call_id or call_id in seen_results or call_id not in calls:
            continue
        seen_results.add(call_id)
        call = calls[call_id]
        if "action" in call:
            call["action"]["result"] = _action_result(node)
            call["action"]["result_seq"] = seq
        elif "observe" in call["name"]:
            data = _tool_result(node)
            if not isinstance(data.get("current_state"), dict):
                continue
            current = snapshot(data, seq)
            if current["session"] != session:
                raise ValueError("observe session differs from recorded identity; content withheld")
            current["call_seq"] = call["seq"]
            for row in interval:
                # A receipt arriving after the next observe call cannot prove its boundary.
                receipt = row["result"] if row["result_seq"] is not None and row["result_seq"] < call["seq"] else "UNKNOWN"
                row["attribution"], row["reason"] = classify_pair(
                    latest, current, len(interval), receipt, row["explicit_session"], intervening)
                row["after"] = current["status"]
                row["after_month"] = current["month"]
                row["post_seq"] = seq
                row["post_title"] = current["title"]
                row["post_context"] = current["description"]
            current["preceding_actions"] = [row["index"] for row in interval]
            observations.append(current)
            interval, intervening, latest = [], False, current
    if observations:
        final = observations[-1]
        if final["month"] not in (survival, survival + 1):
            raise ValueError("final public month inconsistent with formal run; content withheld")
        for index in final["preceding_actions"]:
            actions[index - 1]["immediate_terminal"] = True
    for row in actions:
        row["deltas"] = {
            dim: row["after"][dim] - row["before"][dim]
            for dim in PUBLIC_DIMENSIONS
            if row["after"] and numeric(row["before"].get(dim)) and numeric(row["after"].get(dim))
        }
        row["warning_keyword_families"] = [
            family for family, terms in WARNING_TERMS.items() if any(t in row["context"] for t in terms)
        ]
    # No sessions, choice effect objects, IDs, flags, score objects or history events leave this layer.
    safe_observations = [{key: ob[key] for key in ("seq", "month", "status", "title")} for ob in observations]
    return dict(observations=safe_observations, actions=actions,
                attempted=len(actions), observes=len(observations),
                attribution_counts=dict(Counter(a["attribution"] for a in actions)),
                reason_counts=dict(Counter(a["reason"] for a in actions)))


def quantile(values: list[float], p: float) -> float:
    ordered = sorted(values)
    index = (len(ordered) - 1) * p
    lower, upper = math.floor(index), math.ceil(index)
    return ordered[lower] + (ordered[upper] - ordered[lower]) * (index - lower)


def envelope(runs: dict[str, dict], dim: str) -> dict:
    clean, mixed, unknown = [], [], 0
    for name, run in runs.items():
        for row in run["actions"]:
            if dim not in row["deltas"]:
                unknown += 1
                continue
            point = dict(run=name, action_index=row["index"], month=row["month"],
                         level=row["before"].get("level"), family=row["kind"],
                         action=row["action"], title=row["title"], pre=row["before"][dim],
                         post=row["after"][dim], delta=row["deltas"][dim],
                         immediate_terminal=row["immediate_terminal"], seq=row["seq"],
                         post_seq=row["post_seq"], reason=row["reason"])
            if row["attribution"] == "ACTION_ATTRIBUTABLE":
                clean.append(point)
            elif row["attribution"] == "MIXED_OR_UNATTRIBUTABLE":
                mixed.append(point)
            else:
                unknown += 1
    negative = [point for point in clean if point["delta"] < 0]
    losses = [-point["delta"] for point in negative]
    ordered = sorted(negative, key=lambda p: (p["delta"], p["run"], p["seq"]))
    return dict(
        attributable_n=len(clean), negative_n=len(negative),
        zero_n=sum(p["delta"] == 0 for p in clean),
        positive_n=sum(p["delta"] > 0 for p in clean),
        negative_loss_histogram=dict(sorted(Counter(str(v) for v in sorted(losses)).items())),
        loss_quantiles={name: quantile(losses, p) for name, p in
                        (("median", .5), ("p75", .75), ("p90", .9), ("p95", .95))
                       if len(losses) >= (20 if p >= .9 else 5)},
        quantile_rule="linear interpolation; median/P75 require N>=5, P90/P95 N>=20; descriptive dependent action sample",
        observed_max_loss=max(losses) if losses else None,
        contributing_runs=dict(Counter(p["run"] for p in clean)),
        negative_runs=dict(Counter(p["run"] for p in negative)),
        top_k=ordered[:10], terminal_negative=[p for p in ordered if p["immediate_terminal"]],
        mixed_n=len(mixed), mixed_terminal_negative=[p for p in mixed if p["delta"] < 0 and p["immediate_terminal"]],
        mixed_negative_top_k=sorted(
            [p for p in mixed if p["delta"] < 0], key=lambda p: (p["delta"], p["run"], p["seq"]))[:10],
        unknown_n=unknown,
    )


def window_summary(run: dict, start: int, end: int) -> dict:
    rows = [a for a in run["actions"] if isinstance(a["month"], int) and start <= a["month"] <= end]
    obs = [o for o in run["observations"] if isinstance(o["month"], int) and start <= o["month"] <= end]
    mode = Counter(a["mode"] or "UNKNOWN" for a in rows)
    mixtures = {}
    for kind in ("main", "energy", "story"):
        subset = [a for a in rows if a["kind"] == kind]
        n = len(subset)
        mixtures[kind] = dict(n=n, actions=dict(Counter(a["action"] or "UNKNOWN" for a in subset)),
                             successful_n=sum(a["result"] == "SUCCESS" for a in subset),
                             unknown_n=sum(a["result"] == "UNKNOWN" for a in subset),
                             category_shares={k: round(v / n, 4) for k, v in
                                              sorted(Counter(a["category"] for a in subset).items())} if n else {})
    return dict(window=f"M{start}-M{end}", actions=len(rows), mode=dict(mode),
                s_share=round(mode["S"] / len(rows), 4) if rows else None,
                last_public=obs[-1]["status"] if obs else None,
                public_ranges={d: [min(vals), max(vals)] for d in PUBLIC_DIMENSIONS
                               if (vals := [o["status"][d] for o in obs if numeric(o["status"].get(d))])},
                mixtures=mixtures, recoveries=dict(Counter(a["recovery"] or "UNKNOWN" for a in rows)),
                review_plan_literals=sum(a["review_plan_literal"] for a in rows),
                warning_keyword_actions=dict(Counter(k for a in rows for k in a["warning_keyword_families"])))


def historical_run(number: int) -> dict:
    name = f"candidate_run{number}_trajectory.json"
    ref = f"{HISTORY}:experiments/S04-04-high-score-confirmation/{name}"
    content = subprocess.check_output(["git", "show", ref], cwd=ROOT)
    data = json.loads(content)
    states = data["monthly_public_state"] if number == 1 else data["milestones"]
    public = [{k: r[k] for k in ("month", "quarter", "level", *PUBLIC_DIMENSIONS) if k in r}
              for r in states if "level" in r]
    if number == 1:
        quarters = [{k: r[k] for k in ("month", "energy_actions", "main_action")} for r in data["quarterly_decisions"]]
    else:
        quarters = [{"month": r["month"], "main_action": r["action"],
                     "energy_actions": next((e["selected_actions"] for e in data["quarterly_energy_action_selections"]
                                              if e["month"] == r["month"]), [])}
                    for r in data["quarterly_main_actions"]]
    return dict(tier="B", source=ref, bytes=len(content), sha256=hashlib.sha256(content).hexdigest(),
                public_states=public, quarters=quarters, shock_eligible=False)


def build_report() -> dict:
    runs = {}
    for name, (stamp, session, survival, expected) in LOCAL_RUNS.items():
        path = ROOT / LOCAL / stamp / f"events-{stamp}.jsonl"
        runs[name] = load_run(path, session, survival, expected)
    for name, (folder, session, survival) in ARCHIVE_RUNS.items():
        directory = ROOT / "artifacts/dev-runs" / folder
        manifest = json.loads((directory / "evidence-manifest.json").read_text(encoding="utf-8"))
        expected = next(item["sha256"] for item in manifest["artifacts"]
                        if item["name"] == "events.jsonl")
        runs[name] = load_run(directory / "events.jsonl", session, survival, expected)
    for run in runs.values():
        run["windows"] = [window_summary(run, a, b) for a, b in WINDOWS]
        run["progression_energy"] = progression_energy(run["actions"])
    return dict(schema_version=1, task="S09-02", historical={"v1#1": historical_run(1), "v1#2": historical_run(2)},
                runs=runs, shock_envelope={dim: envelope(runs, dim) for dim in STATS_DIMENSIONS},
                limitation="Observed sample only; no simulator/Test maximum, independence, causal policy gain or numeric mode threshold.")


def progression_energy(actions: list[dict]) -> dict:
    targets = {"SKILL_GROWTH": "skill", "NETWORK_GROWTH": "network", "OUTPUT_VISIBILITY": "output"}
    counts = Counter()
    samples, immediate_repeats = [], []
    for i, row in enumerate(actions):
        dim = targets.get(row["category"]) if row["kind"] == "energy" else None
        if not dim:
            continue
        delta = row["deltas"].get(dim)
        response = ("GAIN" if delta > 0 else "NO_GAIN" if delta == 0 else "DECLINE"
                    ) if row["attribution"] == "ACTION_ATTRIBUTABLE" and delta is not None else "MIXED_OR_UNKNOWN"
        counts[(dim, response)] += 1
        samples.append(dict(index=row["index"], month=row["month"], level=row["before"].get("level"),
                            dimension=dim, response=response))
        if response == "NO_GAIN" and i + 1 < len(actions):
            nxt = actions[i + 1]
            if nxt["category"] == row["category"] and nxt["before"].get("level") == row["before"].get("level"):
                immediate_repeats.append(dict(index=row["index"], next_index=nxt["index"], month=row["month"],
                                              dimension=dim, next_attribution=nxt["attribution"],
                                              next_delta=nxt["deltas"].get(dim)))
    return dict(scope="explicit Energy label dimensions only; no inferred Story/hidden advertising",
                counts=[dict(dimension=d, response=r, n=n) for (d, r), n in sorted(counts.items())],
                samples=samples, immediate_same_dimension_repeats_after_clean_no_gain=immediate_repeats)


def load_run(path: Path, session: str, survival: int, expected: str) -> dict:
    content = path.read_bytes()
    digest = hashlib.sha256(content).hexdigest()
    if digest.lower() != expected.lower():
        raise ValueError("recorded source hash mismatch; stop affected evidence branch")
    records = [json.loads(line) for line in content.decode("utf-8").splitlines() if line.strip()]
    result = extract_records(records, session, survival)
    return dict(tier="A", source=str(path.relative_to(ROOT)), bytes=len(content), sha256=digest,
                formal_survival_months=survival, **result)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / ".local/scratch/s09-02/failure_floor_joint_forensics.json")
    args = parser.parse_args()
    data = build_report()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    content = (json.dumps(data, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")
    args.output.write_bytes(content)
    print(json.dumps({"output": str(args.output), "sha256": hashlib.sha256(content).hexdigest(),
                      "runs_A": len(data["runs"]), "runs_B": len(data["historical"])}, ensure_ascii=False))


if __name__ == "__main__":
    main()
