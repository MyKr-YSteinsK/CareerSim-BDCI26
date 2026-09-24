#!/usr/bin/env python3
"""Deterministic, offline parser for PAR-01's frozen historical run set.

Reads only named completed historical events/score artifacts and committed
canonical evidence. Transcripts are identity-checked but never copied.
"""
from __future__ import annotations

import ast
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
UNKNOWN = "UNKNOWN"
RISK_RE = re.compile(r"\[S03_RISK:(ALLOW|WARN|RECONSIDER)\]")
SKILL_RE = re.compile(r"\[S\d{2}_[A-Z0-9_:-]+\]")

RUNS = [
    {
        "run_id": "S01",
        "role": "unscoped baseline placeholder; no specialized strategy",
        "result": {"status": "scored_terminal", "score": 26.95, "partial_score": 18.86, "survival_months": 19, "grade": "E", "completed": False, "outcome": "eliminated", "termination_reason": UNKNOWN},
        "result_evidence": "experiments/S01-03-baseline/RESULT.md",
        "canonical_score_sha256": "f84598d1df614131f90362a9f3ea83ebe381f5c5b755922187f4868d59b07686",
        "events": {"path": r"D:\CS\CareerSim-s01-03-runner-baseline\.career_sim_runner\career_emu\outputs\local-s01-baseline\20260922T123030Z\events-20260922T123030Z.jsonl", "sha256": "49242bf7e68edb05c3b29f59602c0b0b11da377a9f4deda5a78ad7cd6bf45510", "bytes": None},
        "transcript": {"path": r"D:\CS\CareerSim-s01-03-runner-baseline\.career_sim_runner\career_emu\outputs\local-s01-baseline\20260922T123030Z\transcript-20260922T123030Z.log", "sha256": "ee77106c551a2dccc8ae909fde6bbc1596992b3f40f3c568c69139c3abe5c0af", "bytes": None},
        "score_artifact": {"path": r"D:\CS\CareerSim-s01-03-runner-baseline\.career_sim_runner\career_emu\outputs\local-s01-baseline\20260922T123030Z\score_report.json", "sha256": "f84598d1df614131f90362a9f3ea83ebe381f5c5b755922187f4868d59b07686", "bytes": None},
    },
    {
        "run_id": "S03-14",
        "role": "partial early-run risk correctness smoke; not a score benchmark",
        "result": {"status": "partial_unscored", "score": UNKNOWN, "partial_score": UNKNOWN, "survival_months_observed": 9, "grade": UNKNOWN, "completed": False, "outcome": UNKNOWN, "termination_reason": UNKNOWN},
        "result_evidence": "experiments/S03-14-risk-correctness-live-smoke/smoke_evidence.json",
        "events": {"path": r"D:\CS\CareerSim\.local\worktrees\s03-14-risk-correctness-live-smoke\.career_sim_runner\career_emu\outputs\local-s03-14-risk-correctness-live-smoke\20260923T130444Z\events-20260923T130444Z.jsonl", "sha256": "C12C77BDC5738BBF3A0913AA3CAD9786DFAF7CB9D3156D736C1621AF0E5FCD2B", "bytes": 365106},
        "transcript": {"path": r"D:\CS\CareerSim\.local\worktrees\s03-14-risk-correctness-live-smoke\.career_sim_runner\career_emu\outputs\local-s03-14-risk-correctness-live-smoke\20260923T130444Z\transcript-20260923T130444Z.log", "sha256": "2E3A5C95A83014047C2822BE0A04E16200A69F681DD372CBC1281B734F7FFD0C", "bytes": 64540},
        "score_artifact": {"path": r"D:\CS\CareerSim\.local\worktrees\s03-14-risk-correctness-live-smoke\.career_sim_runner\career_emu\outputs\local-s03-14-risk-correctness-live-smoke\20260923T130444Z\score_report.json", "sha256": "123ACEF655EE5C30CEA8C309C5CE3C4E7C99705D9649E7A0880A2FDE8B3B4F17", "bytes": 1254},
    },
    {
        "run_id": "SCORE-01",
        "role": "scored low-score checkpoint",
        "result": {"status": "scored_terminal", "score": 33.06, "partial_score": 23.14, "survival_months": 24, "grade": "D", "completed": False, "outcome": "eliminated", "termination_reason": UNKNOWN},
        "result_evidence": "experiments/S04-03-score-directed-integrated-run/score01_trajectory.json",
        "canonical_source": {"commit": "e4c88c253820ca4abc511c0ec7f73468674a0de7"},
        "events": {"path": r"D:\CS\CareerSim\.local\worktrees\score-01-full-score-checkpoint\.career_sim_runner\career_emu\outputs\local-score-01-full-score-checkpoint\20260923T144458Z\events-20260923T144458Z.jsonl", "sha256": "C208BF46E811176E19EF42B83BEB6C39796F54A5EF6F2B22818F867ED6E0E262", "bytes": 975641},
        "transcript": {"path": r"D:\CS\CareerSim\.local\worktrees\score-01-full-score-checkpoint\.career_sim_runner\career_emu\outputs\local-score-01-full-score-checkpoint\20260923T144458Z\transcript-20260923T144458Z.log", "sha256": "FC5557673CB0CA31191347D5511C34D63ADEDF1E23A17EE60404AC8B92451C1A", "bytes": 229510},
        "score_artifact": {"path": r"D:\CS\CareerSim\.local\worktrees\score-01-full-score-checkpoint\.career_sim_runner\career_emu\outputs\local-score-01-full-score-checkpoint\20260923T144458Z\score_report.json", "sha256": "1B61B22A980E65A89170FD25B054A2563CE5ECF2D82BFFD4DFD15948CCF08669", "bytes": 2951},
    },
    {
        "run_id": "S04-03",
        "role": "scored high-score candidate with rolling-planning and state-board skills loaded",
        "result": {"status": "scored_terminal", "score": 76.04, "partial_score": 53.23, "survival_months": 48, "grade": "A", "completed": True, "outcome": "completed", "termination_reason": UNKNOWN},
        "result_evidence": "experiments/S04-03-score-directed-integrated-run/run_evidence.json",
        "events": {"path": r"D:\CS\CareerSim\.local\worktrees\s04-03-score-directed-integrated-run\.career_sim_runner\career_emu\outputs\local-s04-03-score-directed-integrated-run\20260923T160734Z\events-20260923T160734Z.jsonl", "sha256": "a964db295f0135f4dc41f135b3ed3d8513a196fbbb689f36d47f76c957ef7d79", "bytes": 2027675},
        "transcript": {"path": r"D:\CS\CareerSim\.local\worktrees\s04-03-score-directed-integrated-run\.career_sim_runner\career_emu\outputs\local-s04-03-score-directed-integrated-run\20260923T160734Z\transcript-20260923T160734Z.log", "sha256": "49cbfcee32dd88d1573d4e0a068de543e3993d45384dc72854bfa91aaebfec71", "bytes": 753385},
        "score_artifact": {"path": r"D:\CS\CareerSim\.local\worktrees\s04-03-score-directed-integrated-run\.career_sim_runner\career_emu\outputs\local-s04-03-score-directed-integrated-run\20260923T160734Z\score_report.json", "sha256": "034a8bb6f04bc961f5c733b92e311de7df4700db7eea5a4843eef4536447ccbe", "bytes": 2998},
    },
]

# Low-confidence narrative families use title keywords only; exact title is primary.
FAMILY_RULES = [
    ("quarterly_energy_allocation", ("季度体力行动分配",)),
    ("quarterly_main_action", ("季度主行动选择",)),
    ("onboarding", ("新员工手册",)),
    ("health_wellbeing", ("健康", "体检", "健身", "带病", "加班", "酒后", "休息", "作息", "咖啡因")),
    ("ethics_risk", ("风险", "违规", "合规", "隐私", "匿名", "保密", "截图", "埋雷", "漏洞")),
    ("customer_delivery", ("客户", "交付", "延期", "Bug", "迁移", "大促", "上线")),
    ("performance_growth", ("晋升", "绩效", "调薪", "升职", "评审", "成果", "OKR", "关键项目")),
    ("workplace_relationship", ("同事", "领导", "Leader", "新人", "实习生", "袁野", "小周", "小葵")),
    ("technical_decision", ("技术", "架构", "代码", "CI", "数据库", "重构", "认证", "框架")),
]

def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))

def verify_artifact(spec: dict[str, Any]) -> dict[str, Any]:
    path = Path(spec["path"])
    out = {"path": spec["path"], "expected_bytes": spec.get("bytes"), "expected_sha256": spec["sha256"].lower()}
    if not path.is_file():
        out.update({"status": "UNAVAILABLE", "actual_bytes": None, "actual_sha256": None})
        return out
    data = path.read_bytes()
    actual_hash = sha256(data)
    ok = actual_hash == spec["sha256"].lower() and (spec.get("bytes") is None or len(data) == spec["bytes"])
    out.update({"actual_bytes": len(data), "actual_sha256": actual_hash, "status": "MATCH" if ok else "RAW_IDENTITY_MISMATCH"})
    return out

def decode_tool_result(frame: dict[str, Any]) -> tuple[dict[str, Any] | None, str | None]:
    delta = (frame.get("payload") or {}).get("delta") or {}
    text = delta.get("result")
    if not isinstance(text, str):
        return None, None
    try:
        outer = ast.literal_eval(text)
        if isinstance(outer, dict) and isinstance(outer.get("result"), str):
            inner_text = outer["result"]
            try:
                inner = json.loads(inner_text)
                return (inner if isinstance(inner, dict) else None), inner_text
            except json.JSONDecodeError:
                return None, inner_text
    except (ValueError, SyntaxError):
        pass
    return None, text

def parse_arguments(text: str) -> tuple[dict[str, Any], str | None]:
    try:
        return json.loads(text), None
    except json.JSONDecodeError:
        # One SCORE-01 call captured an unquoted 32-hex session ID.
        fixed = re.sub(r'("session_id"\s*:\s*)([0-9a-f]{32})(\s*,)', r'\1"\2"\3', text, count=1)
        try:
            return json.loads(fixed), "SESSION_ID_WAS_UNQUOTED_IN_RAW_ARGUMENTS"
        except json.JSONDecodeError:
            return {}, "ARGUMENTS_JSON_UNPARSEABLE"

def public_state(observation: dict[str, Any] | None) -> dict[str, Any] | str:
    if not observation:
        return UNKNOWN
    state = observation.get("current_state") or {}
    time, status = state.get("time") or {}, state.get("status") or {}
    flags = state.get("simulation_flags") or {}
    return {
        "time": {"month": time.get("current_month", UNKNOWN), "quarter": time.get("current_quarter", UNKNOWN), "year": time.get("current_year", UNKNOWN)},
        "status": {k: status.get(k, UNKNOWN) for k in ("level", "duration_in_level", "skill", "network", "output", "health", "dignity", "wealth", "energy")},
        "alive": flags.get("alive", UNKNOWN),
        "failed": flags.get("failed", UNKNOWN),
        "failure_reason": flags.get("failure_reason", UNKNOWN),
    }

def event_family(title: str) -> tuple[str, str]:
    if not title:
        return UNKNOWN, "LOW"
    for family, words in FAMILY_RULES:
        if any(word in title for word in words):
            return family, "HIGH" if family in {"quarterly_energy_allocation", "quarterly_main_action", "onboarding"} else "LOW"
    return ("narrative_chain" if "长链" in title else "narrative_event", "LOW")

def state_delta(before: Any, after: Any) -> dict[str, Any] | str:
    if not isinstance(before, dict) or not isinstance(after, dict):
        return UNKNOWN
    left, right = before.get("status", {}), after.get("status", {})
    changes = {}
    for key in ("skill", "network", "output", "health", "dignity", "wealth", "energy", "level"):
        a, b = left.get(key), right.get(key)
        if a != UNKNOWN and b != UNKNOWN and a != b:
            changes[key] = {"before": a, "after": b, "delta": b - a if isinstance(a, (int, float)) and isinstance(b, (int, float)) else None}
    return changes or "NO_PUBLIC_STATUS_CHANGE_OBSERVED"

def phase(month: Any) -> str:
    if not isinstance(month, int):
        return UNKNOWN
    start = ((month - 1) // 6) * 6 + 1
    return f"month_{start:02d}_{start + 5:02d}"

def extract_performance_feedback(observation: dict[str, Any] | None) -> Any:
    if not observation:
        return UNKNOWN
    event = observation.get("current_event") or {}
    title = event.get("title", "")
    description = event.get("description", "")
    events = observation.get("events", "")
    parts = []
    # These phrases identify public review/score events, rather than an agent's
    # own mention of performance in an action note.
    if isinstance(events, str) and re.search(r"【半年谈话】|绩效奖金|晋升通知|观察名单|评审会上", events):
        parts.append({"source": "observe.events", "excerpt": events[:900]})
    if isinstance(title, str) and re.search(r"绩效评审|晋升评审|半年绩效", title):
        parts.append({"source": "current_event.title", "excerpt": title})
    if isinstance(description, str) and re.search(r"绩效评级|绩效评审|晋升评审|绩效反馈", description):
        parts.append({"source": "current_event.description", "excerpt": description[:500]})
    return {"public_evidence": parts} if parts else UNKNOWN

def scan_board_transcript(spec: dict[str, Any]) -> dict[str, Any]:
    lines = Path(spec["path"]).read_text(encoding="utf-8").splitlines()
    board_line = next((
        i for i, line in enumerate(lines, 1)
        if all(re.search(rf"{word}\s*:", line, re.I) for word in ("observed", "inferred", "unknown"))
    ), None)
    later = [
        i for i, line in enumerate(lines, 1)
        if board_line is not None and i > board_line
        and re.search(r"structured state board|state board|game_session_id|freshness", line, re.I)
    ]
    return {
        "transcript_path": spec["path"],
        "transcript_sha256": spec["sha256"].lower(),
        "board_like_output_line": board_line or UNKNOWN,
        "observed_inferred_unknown_labels_present": board_line is not None,
        "free_text_freshness_label_present": any(
            board_line is not None and re.search(r"freshness\s*:", line, re.I)
            for line in lines[max(0, board_line - 3):min(len(lines), board_line + 2)]
        ),
        "explicit_game_session_id_field_in_board": False,
        "later_explicit_board_keyword_matches": len(later),
        "later_keyword_line_numbers": later,
    }

def decode_run(run: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    artifacts = [verify_artifact(run[k]) for k in ("events", "transcript", "score_artifact")]
    usable = all(x["status"] == "MATCH" for x in artifacts)
    report = {
        "run_id": run["run_id"], "role": run["role"], "result": run["result"],
        "result_evidence": run.get("result_evidence"), "canonical_source": run.get("canonical_source"),
        "raw_artifacts": artifacts, "raw_usable_for_fine_grained_analysis": usable,
    }
    if not usable:
        report["detailed_records"] = 0
        report["exclusion_reason"] = "RAW_IDENTITY_MISMATCH_OR_UNAVAILABLE; canonical facts only"
        return [], report

    frames = [json.loads(line) for line in Path(run["events"]["path"]).read_text(encoding="utf-8").splitlines() if line.strip()]
    results, result_texts, result_seqs = {}, {}, {}
    for frame in frames:
        if frame.get("kind") == "tool_result":
            delta = (frame.get("payload") or {}).get("delta") or {}
            call_id = delta.get("tool_call_id")
            decoded, raw_text = decode_tool_result(frame)
            if call_id:
                if decoded is not None:
                    results[call_id] = decoded
                if raw_text is not None:
                    result_texts[call_id] = raw_text
                result_seqs[call_id] = frame["seq"]

    calls, observations, actions, skill_loads = [], [], [], []
    for frame in frames:
        if frame.get("kind") != "tool_call":
            continue
        tc = (frame.get("payload") or {}).get("tool_call") or {}
        name, call_id = tc.get("name", ""), tc.get("tool_call_id")
        if "skill_tool" in name:
            args, _ = parse_arguments(tc.get("arguments", "{}"))
            skill_loads.append(args.get("skill_name", UNKNOWN))
        if name.endswith("_observe"):
            output = results.get(call_id)
            if isinstance(output, dict) and "current_state" in output:
                item = {"kind": "observe", "frame": frame, "output": output, "call_id": call_id}
                observations.append(item)
                calls.append(item)
            else:
                calls.append({"kind": "observe_unavailable", "frame": frame, "output": None, "call_id": call_id})
        elif name.endswith("_take_action"):
            args, arg_issue = parse_arguments(tc.get("arguments", "{}"))
            output, result_text = results.get(call_id), result_texts.get(call_id, "")
            if isinstance(output, dict) and output.get("success") is True:
                status, error = "SUCCESS", None
            elif "success=False" in result_text:
                status, error = "FAILED_ARGUMENT_VALIDATION", "Invalid tool arguments JSON" if "Invalid tool arguments JSON" in result_text else "TOOL_REJECTED"
            elif isinstance(output, dict) and output.get("success") is False:
                status, error = "FAILED", output.get("error") or "TOOL_REPORTED_FAILURE"
            elif call_id not in result_seqs:
                status, error = "UNKNOWN", None
            else:
                status, error = "SUCCESS_FIELD_UNREPORTED", None
            item = {
                "kind": "action", "frame": frame, "call_id": call_id, "args": args,
                "argument_issue": arg_issue, "submission_status": status, "error_class": error,
                "result_seq": result_seqs.get(call_id),
            }
            actions.append(item)
            calls.append(item)
    calls.sort(key=lambda x: x["frame"]["seq"])

    latest = None
    actions_by_observation: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for item in calls:
        if item["kind"] == "observe":
            latest = item
        elif item["kind"] == "action":
            item["observation"] = latest
            if latest:
                actions_by_observation[latest["frame"]["seq"]].append(item)
    after_observation = {}
    for action in actions:
        seq = action["frame"]["seq"]
        next_obs = next((x for x in observations if x["frame"]["seq"] > seq), None)
        intervening = next((x for x in actions if seq < x["frame"]["seq"] < (next_obs["frame"]["seq"] if next_obs else 10**12)), None)
        if next_obs and intervening is None:
            after_observation[seq] = next_obs

    rows, title_context_counts = [], Counter()
    s04_checkpoints = [
        {"checkpoint_id": 1, "horizon": "next quarter", "public_gap": "L1, Skill 1, Network 1, Output 0", "priority": "Build capability and visible output before the promotion window.", "recommended_actions": UNKNOWN, "evidence": "run_evidence.json rolling_planning.checkpoints[0]"},
        {"checkpoint_id": 2, "horizon": "Q2 through Month 6 review", "public_gap": "Network 3 and Output 2 lagged Skill 9; Health 4 was declining.", "priority": "Boost Network and Output while recovering Health.", "recommended_actions": ["人脉维护", "准备汇报材料", "健康恢复"], "evidence": "run_evidence.json rolling_planning.checkpoints[1]"},
        {"checkpoint_id": 3, "horizon": "Q3 through Month 12 review", "public_gap": "Health 3, public performance C, Leader requested clearer Output.", "priority": "Recover Health buffer and increase visible Output.", "recommended_actions": ["健康恢复", "准备汇报材料", "健康恢复"], "evidence": "run_evidence.json rolling_planning.checkpoints[2]"},
    ]
    for action in actions:
        frame, obs_item = action["frame"], action.get("observation")
        observation = obs_item["output"] if obs_item else None
        args = action["args"]
        event = (observation or {}).get("current_event") or {}
        title = event.get("title", UNKNOWN)
        family, family_confidence = event_family(title if isinstance(title, str) else "")
        state = public_state(observation)
        time = state.get("time", {}) if isinstance(state, dict) else {}
        month = time.get("month", UNKNOWN)
        context = f"{run['run_id']}:{obs_item['frame']['seq'] if obs_item else 'UNKNOWN'}"
        group = actions_by_observation.get(obs_item["frame"]["seq"], []) if obs_item else []
        group_index = group.index(action) + 1 if action in group else 1
        group_size = len(group)
        if title not in title_context_counts:
            title_context_counts[title] = 0
        if group_index == 1:
            title_context_counts[title] += 1
        occurrence = title_context_counts[title]
        choices = observation.get("choices", []) if observation else []
        choice = next((x for x in choices if x.get("choice") == args.get("choice")), None)
        if group_index == 1:
            binding = "DIRECT_OBSERVE_MENU"
        elif all(x["submission_status"] == "FAILED_ARGUMENT_VALIDATION" for x in group[:group_index - 1]):
            binding = "RETRY_AFTER_ARGUMENT_REJECTION"
        else:
            binding = "OBSERVATION_REUSED_AFTER_PRIOR_ACTION"
        after = after_observation.get(frame["seq"])
        state_after = public_state(after["output"]) if after else UNKNOWN
        left = state.get("status", {}) if isinstance(state, dict) else {}
        right = state_after.get("status", {}) if isinstance(state_after, dict) else {}
        if isinstance(state, dict) and isinstance(state_after, dict):
            level_change = {"before": left.get("level", UNKNOWN), "after": right.get("level", UNKNOWN), "scope": "after action/group; no causal attribution"} if left.get("level") != right.get("level") else "NONE_OBSERVED"
        else:
            level_change = UNKNOWN
        note = args.get("notes", "")
        note = note if isinstance(note, str) else str(note)
        markers = SKILL_RE.findall(note)
        risk = RISK_RE.findall(note)
        selected = {
            "choice": args.get("choice", UNKNOWN),
            "option_action_from_observation": choice.get("action", UNKNOWN) if choice else UNKNOWN,
            "choice_binding": binding,
            "energy_cost": choice.get("energy_cost", UNKNOWN) if choice else UNKNOWN,
            "public_status_updates": choice.get("status_updates", UNKNOWN) if choice else UNKNOWN,
        } if args.get("choice", UNKNOWN) != UNKNOWN else UNKNOWN
        legal = [
            {"choice": c.get("choice", UNKNOWN), "action": c.get("action", UNKNOWN), "energy_cost": c.get("energy_cost", UNKNOWN), "public_status_updates": c.get("status_updates", UNKNOWN)}
            for c in choices
        ] if observation else UNKNOWN
        feedback_before = extract_performance_feedback(observation)
        feedback_after = extract_performance_feedback(after["output"] if after else None)
        feedback = {
            "before_action_observation": feedback_before,
            "after_action_group_observation": feedback_after,
        } if feedback_before != UNKNOWN or feedback_after != UNKNOWN else UNKNOWN
        planning = UNKNOWN
        if run["run_id"] == "S04-03":
            if frame["seq"] == min(x["frame"]["seq"] for x in actions):
                planning = s04_checkpoints[0]
            elif title == "季度体力行动分配" and month == 3:
                planning = s04_checkpoints[1]
            elif title == "季度体力行动分配" and month == 6:
                planning = s04_checkpoints[2]
        if action["submission_status"] == "FAILED_ARGUMENT_VALIDATION":
            scope, delta = "call_rejected_before_game_action", UNKNOWN
        elif after:
            scope, delta = "next_observe_after_action", state_delta(state, state_after)
        elif group_index < group_size:
            scope, delta = "shared_action_group_no_intervening_observe", UNKNOWN
        else:
            scope, delta = "no_subsequent_public_observation", UNKNOWN
        confidence = "LOW" if action["submission_status"] in {"UNKNOWN", "SUCCESS_FIELD_UNREPORTED"} else ("MEDIUM" if binding == "OBSERVATION_REUSED_AFTER_PRIOR_ACTION" else "HIGH")
        rows.append({
            "run_id": run["run_id"], "run_role": run["role"], "record_id": f"{run['run_id']}:action:{frame['seq']}",
            "month": month, "quarter": time.get("quarter", UNKNOWN), "year": time.get("year", UNKNOWN), "phase": phase(month),
            "event_title": title, "event_family": family, "event_family_confidence": family_confidence, "event_context_occurrence": occurrence,
            "public_state_before": state, "legal_choices": legal, "selected_choice": selected,
            "selected_action": choice.get("action", UNKNOWN) if choice else UNKNOWN, "reasoning_excerpt": note[:360] if note else UNKNOWN,
            "skill_markers": markers, "planning_checkpoint": planning, "risk_marker": risk[-1] if risk else "NOT_MARKED",
            "confirmed_result": {
                "tool_submission": action["submission_status"], "error_class": action["error_class"] or UNKNOWN,
                "result_scope": scope, "action_group_index": group_index, "action_group_size": group_size,
                "public_state_delta": delta, "argument_parse_note": action["argument_issue"] or UNKNOWN,
            },
            "public_state_after": state_after, "performance_feedback": feedback,
            "promotion_or_level_change": level_change, "terminal_signal": "NONE_OBSERVED",
            "evidence_ref": {
                "artifact": "raw events", "path": run["events"]["path"], "sha256": run["events"]["sha256"].lower(),
                "observe_seq": obs_item["frame"]["seq"] if obs_item else UNKNOWN, "action_call_seq": frame["seq"],
                "action_result_seq": action["result_seq"] or UNKNOWN, "post_observe_seq": after["frame"]["seq"] if after else UNKNOWN,
                "transcript_sha256_verified_not_copied": run["transcript"]["sha256"].lower(),
            },
            "confidence": confidence, "confidence_note": "Confidence rates field provenance only, not causal attribution.",
        })
    if rows:
        rows[-1]["terminal_signal"] = {**run["result"], "source": "committed RESULT/canonical evidence; raw score artifact identity verified"}

    snapshots: dict[int, list[dict[str, Any]]] = defaultdict(list)
    level_changes, previous_level = [], UNKNOWN
    for obs in observations:
        state = public_state(obs["output"])
        if not isinstance(state, dict) or not isinstance(state["time"]["month"], int):
            continue
        month = state["time"]["month"]
        entry = {"month": month, "quarter": state["time"]["quarter"], "year": state["time"]["year"], "public_state": state, "event_title": (obs["output"].get("current_event") or {}).get("title", UNKNOWN), "observe_seq": obs["frame"]["seq"]}
        snapshots[month].append(entry)
        level = state["status"].get("level", UNKNOWN)
        if previous_level != UNKNOWN and level != UNKNOWN and level != previous_level:
            level_changes.append({"month": month, "from": previous_level, "to": level, "observe_seq": obs["frame"]["seq"], "current_event_title": entry["event_title"], "source": "direct public observe sequence; no threshold inferred"})
        previous_level = level

    def last_live(horizon: int):
        found = [x for month, entries in snapshots.items() if month <= horizon for x in entries if x["public_state"]["alive"] is True]
        return max(found, key=lambda x: (x["month"], x["observe_seq"])) if found else None

    horizons = {}
    for h in (6, 12, 18, 24, 36, 48):
        exact = [x for x in snapshots.get(h, []) if x["public_state"]["alive"] is True]
        horizons[str(h)] = {"exact_live_snapshot": exact[-1] if exact else UNKNOWN, "last_live_at_or_before_horizon": last_live(h) or UNKNOWN, "horizon_complete_live": bool(exact)}
    windows = []
    for start, end in ((1, 6), (7, 12), (13, 18), (19, 24), (25, 36), (37, 48)):
        base = (snapshots.get(1) or [None])[0] if start == 1 else last_live(start - 1)
        endpoint = last_live(end)
        exact = any(x["public_state"]["alive"] is True for x in snapshots.get(end, []))
        status = "COMPLETE_LIVE_WINDOW" if exact else ("PARTIAL_OR_TERMINAL_BEFORE_WINDOW_END" if endpoint and endpoint["month"] < end else "NO_PUBLIC_ENDPOINT")
        windows.append({"window": f"{start}-{end}", "start_snapshot": base or UNKNOWN, "last_live_endpoint_at_or_before_window_end": endpoint or UNKNOWN, "exact_live_window_end_available": exact, "observed_delta": state_delta(base["public_state"], endpoint["public_state"]) if base and endpoint else UNKNOWN, "window_status": status})

    successful = [x for x in rows if x["confirmed_result"]["tool_submission"] == "SUCCESS"]
    main = Counter(x["selected_action"] for x in successful if x["event_title"] == "季度主行动选择")
    energy = [x for x in successful if x["event_title"] == "季度体力行动分配"]
    energy_counts = Counter(x["selected_action"] for x in energy)
    by_quarter: dict[str, list[dict[str, Any]]] = defaultdict(list)
    energy_points = 0
    for x in energy:
        cost = x["selected_choice"].get("energy_cost", UNKNOWN)
        if isinstance(cost, int):
            energy_points += cost
        by_quarter[str(x["month"])].append({"action": x["selected_action"], "energy_cost": cost, "risk_marker": x["risk_marker"], "action_call_seq": x["evidence_ref"]["action_call_seq"]})
    risk_counts = Counter(x["risk_marker"] for x in rows if x["risk_marker"] != "NOT_MARKED")
    report.update({
        "raw_event_frames": len(frames), "valid_public_observations": len(observations), "action_attempts": len(rows),
        "action_status_counts": dict(Counter(x["confirmed_result"]["tool_submission"] for x in rows)),
        "skill_tool_loads": skill_loads, "risk_marker_counts": dict(risk_counts),
        "risk_marker_rate_per_action_attempt": round(sum(risk_counts.values()) / len(rows), 4) if rows else None,
        "quarterly_main_actions": dict(main),
        "quarterly_energy": {"choice_counts": dict(energy_counts), "energy_points_observed": energy_points, "actions_by_allocation_month": dict(sorted(by_quarter.items(), key=lambda x: int(x[0])))},
        "monthly_public_snapshots": {str(m): {"first": v[0], "last": v[-1], "observations": len(v)} for m, v in sorted(snapshots.items())},
        "level_changes": level_changes, "common_horizon_snapshots": horizons, "six_month_windows": windows, "detailed_records": len(rows),
    })
    return rows, report

def matched_event_cases(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_run = {}
    for run in RUNS:
        contexts: dict[int, list[dict[str, Any]]] = defaultdict(list)
        for row in records:
            if row["run_id"] == run["run_id"] and isinstance(row["evidence_ref"]["observe_seq"], int):
                contexts[row["evidence_ref"]["observe_seq"]].append(row)
        counter, index = Counter(), {}
        for _, group in sorted(contexts.items()):
            title = group[0]["event_title"]
            if title in {"新员工手册", "季度体力行动分配", "季度主行动选择"}:
                continue
            counter[title] += 1
            index[(title, counter[title])] = group
        by_run[run["run_id"]] = index
    left, right = by_run.get("SCORE-01", {}), by_run.get("S04-03", {})
    cases = []
    for key in sorted(left.keys() & right.keys()):
        a_group, b_group = left[key], right[key]
        a = next((x for x in a_group if x["confirmed_result"]["tool_submission"] == "SUCCESS"), a_group[0])
        b = next((x for x in b_group if x["confirmed_result"]["tool_submission"] == "SUCCESS"), b_group[0])
        sa, sb = a["public_state_before"]["status"], b["public_state_before"]["status"]
        same_phase, same_level = a["phase"] == b["phase"], sa.get("level") == sb.get("level")
        limits = {"health": 2, "skill": 5, "network": 3, "output": 3, "dignity": 2}
        close = all(isinstance(sa.get(k), (int, float)) and isinstance(sb.get(k), (int, float)) and abs(sa[k] - sb[k]) <= lim for k, lim in limits.items())
        grade = "YES" if same_phase and same_level and close else ("PARTIAL" if same_level and close else "NO")
        same_choice = a["selected_action"] == b["selected_action"]
        lesson = "Same option at this exact-title occurrence; differing later trajectories are not a causal test." if same_choice else (
            "Potential matched choice contrast, but one run per condition cannot establish an effect." if grade == "YES" else (
                "State is close by the set tolerance, but phase differs; descriptive only." if grade == "PARTIAL" else "State, level, phase, or chain context differs too much for a choice lesson."
            )
        )
        after_a = next((x["public_state_after"] for x in reversed(a_group) if x["public_state_after"] != UNKNOWN), UNKNOWN)
        after_b = next((x["public_state_after"] for x in reversed(b_group) if x["public_state_after"] != UNKNOWN), UNKNOWN)
        cases.append({
            "event_title": key[0], "same_title_occurrence_index": key[1],
            "run_a": {"run_id": "SCORE-01", "month": a["month"], "public_state_before": a["public_state_before"], "selected_action": a["selected_action"], "confirmed_result": a["confirmed_result"], "public_state_after_action_context": after_a},
            "run_b": {"run_id": "S04-03", "month": b["month"], "public_state_before": b["public_state_before"], "selected_action": b["selected_action"], "confirmed_result": b["confirmed_result"], "public_state_after_action_context": after_b},
            "matching_rule": "Exact title and ordinal observed context within title; no hidden chain state used.",
            "same_six_month_phase": same_phase, "same_level": same_level, "core_public_state_within_tolerance": close,
            "comparable": grade, "supported_lesson": lesson,
            "unsupported_causal_claim": "Choice caused the score or survival difference.",
        })
    return cases

def main() -> None:
    all_rows, run_reports = [], []
    for run in RUNS:
        rows, report = decode_run(run)
        all_rows.extend(rows)
        run_reports.append(report)
    title_runs, family_counts = defaultdict(set), defaultdict(Counter)
    for row in all_rows:
        title_runs[row["event_title"]].add(row["run_id"])
        family_counts[row["run_id"]][row["event_family"]] += 1
    shared_titles = [{"event_title": t, "runs": sorted(ids), "run_count": len(ids)} for t, ids in sorted(title_runs.items()) if len(ids) >= 2]
    cases = matched_event_cases(all_rows)
    differing = [x for x in cases if x["run_a"]["selected_action"] != x["run_b"]["selected_action"]]
    comparable_different = [x for x in differing if x["comparable"] == "YES"]
    run_evidence = read_json(REPO / "experiments/S04-03-score-directed-integrated-run/run_evidence.json")
    s03 = read_json(REPO / "experiments/S03-14-risk-correctness-live-smoke/smoke_evidence.json")
    s01_score = REPO / "experiments/S01-03-baseline/score_report.json"
    s01_hash = sha256(s01_score.read_bytes()) if s01_score.is_file() else None
    integrity = {r["run_id"]: r["raw_artifacts"] for r in run_reports}
    status_counts, risk_counts = Counter(), Counter()
    for row in all_rows:
        status_counts[row["confirmed_result"]["tool_submission"]] += 1
        if row["risk_marker"] != "NOT_MARKED":
            risk_counts[row["risk_marker"]] += 1
    summary = {
        "schema_version": "PAR-01-1.0",
        "scope": {
            "analysis": "Offline public-state/action-trace mining from the four frozen runs only.",
            "live_run_authorized": False, "S04_04_read": False, "raw_transcripts_committed": False,
            "hidden_emulator_state_used": False,
            "primary_source": "Hash-verified raw events and score reports plus committed canonical evidence.",
            "reasoning_excerpt_source": "take_action notes in raw events; transcript hashes were verified but raw transcript content was not copied.",
            "missing_value_policy": "UNKNOWN",
        },
        "input_runs": run_reports,
        "raw_integrity": {
            "all_expected_raw_artifacts_match": all(x["status"] == "MATCH" for artifacts in integrity.values() for x in artifacts),
            "artifacts_by_run": integrity, "S01_committed_score_report_sha256": s01_hash,
            "S01_committed_score_report_matches_result_sha": s01_hash == RUNS[0]["canonical_score_sha256"],
            "S03_canonical_evidence_decision": s03["decision"],
        },
        "dataset": {
            "trajectory_records": len(all_rows),
            "run_counts": {r["run_id"]: sum(x["run_id"] == r["run_id"] for x in all_rows) for r in RUNS},
            "action_status_counts": dict(status_counts), "risk_marker_counts": dict(risk_counts),
            "distinct_exact_event_titles": len(title_runs), "exact_event_titles_shared_by_two_or_more_runs": len(shared_titles),
            "matched_SCORE01_vs_S04_contexts": len(cases), "differing_choice_contexts": len(differing),
            "differing_choice_contexts_meeting_strict_comparability": len(comparable_different),
        },
        "semantic_event_family_counts": {rid: dict(c) for rid, c in family_counts.items()},
        "semantic_matching_rule": {
            "method": "Deterministic ordered title-keyword rules in analysis.py; no embeddings, LLM, transcript text, or hidden state.",
            "confidence": "LOW for inferred narrative families; HIGH only for exact system/quarterly titles.",
            "false_positive_risk": "Titles may contain overlapping themes; family counts are orientation only. Exact title and public state are used for case matching.",
        },
        "matched_decision_cases": cases, "common_exact_event_titles": shared_titles,
        "score01_vs_s04_canonical_comparison": read_json(REPO / "experiments/S04-03-score-directed-integrated-run/score_comparison.json"),
        "rolling_planning_forensics": {
            **run_evidence["rolling_planning_use"],
            "observed_action_pattern": "Quarterly main action was 申请关键项目 in all 7 SCORE-01 and all 16 S04-03 main-action choices.",
        },
        "structured_state_board_forensics": {
            **run_evidence["structured_state_board"],
            "transcript_behavior": {
                **scan_board_transcript(RUNS[3]["transcript"]),
                "initial_priority_alignment": "The immediately following initial rolling plan prioritized Skill, Network, and Output; this is observable alignment, not an isolated board effect.",
                "interpretation": "One initial board-like output was referenced in the initial planning block; later board refresh/use and score contribution are not proven.",
            },
        },
        "source_discrepancies": [
            {
                "run_id": "SCORE-01",
                "canonical_status": "score01_trajectory.json reports 97 success and 1 success_field_unreported.",
                "raw_status": "Hash-verified raw event call seq 406 was rejected at seq 407 with Invalid tool arguments JSON; the corrected call seq 410 succeeded at seq 411.",
                "handling": "Retain both call records; count the first as failed pre-dispatch and the second as the accepted action. Do not count the rejected call as a game action.",
                "confidence": "HIGH from direct raw tool-result text; canonical status-summary discrepancy preserved.",
            }
        ],
        "analysis_boundaries": [
            "Four independent run trajectories are not randomized treatment arms; only three have terminal scores.",
            "Different fresh-game event sequences, chain stages, and survival length confound cross-run differences.",
            "A take_action note records the agent's stated rationale, not proof the rationale was correct.",
            "Repeated actions before a fresh observe share the last visible menu; intermediate public_state_after is UNKNOWN.",
            "One SCORE-01 invalid-JSON attempt was rejected before dispatch; the subsequent valid call is recorded separately.",
            "Risk-control score normalization alone does not prove risk-review effectiveness.",
            "No hidden promotion threshold or exact elimination cause is inferred.",
        ],
    }
    (HERE / "cross_run_trajectory.jsonl").write_text(
        "".join(json.dumps(x, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n" for x in all_rows),
        encoding="utf-8", newline="\n",
    )
    (HERE / "cross_run_summary.json").write_text(json.dumps(summary, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({
        "trajectory_records": len(all_rows), "run_counts": summary["dataset"]["run_counts"],
        "action_status_counts": dict(status_counts), "risk_marker_counts": dict(risk_counts),
        "event_title_count": len(title_runs), "shared_exact_title_count": len(shared_titles),
        "matched_benchmark_contexts": len(cases), "different_choices": len(differing),
        "strictly_comparable_different_choices": len(comparable_different),
        "raw_integrity_all_match": summary["raw_integrity"]["all_expected_raw_artifacts_match"],
        "S01_canonical_score_hash_match": summary["raw_integrity"]["S01_committed_score_report_matches_result_sha"],
    }, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
