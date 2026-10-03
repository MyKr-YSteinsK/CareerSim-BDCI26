"""Explicit-path offline public transition mining; no DB/provider/runtime calls.

JSONL is the dependency-free canonical format. Text labels are research proxies,
not game state or causal evidence. Only advertised HiddenRisk deltas are retained.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

from scripts.post_run_audit import _arguments, _node, _result

STATS = {"H": "health", "D": "dignity", "S": "skill", "N": "network", "O": "output", "W": "wealth", "E": "energy"}
GRADE = re.compile(r"半年绩效(?:奖金|评级|考核)?\s*[（(：:]\s*([ABCD][+-]?)")
REVIEW = re.compile(r"半年谈话|半年绩效|formal review|performance review", re.I)
RESULT = re.compile(r"如期上线|顺利上线|成功上线|正式上线|上线后|已经上线|体系上线|交付完成|完成交付|通过验收|验收通过|成功交付|已交付|顺利交付|项目落地|顺利亮相|体系顺利上线")
RECOGNITION = re.compile(r"业务.{0,8}满意|客户.{0,8}(?:满意|认可)|Leader.{0,8}(?:认可|表扬)|领导.{0,8}(?:认可|表扬)|组织者.{0,8}(?:感激|感谢)|获得.{0,8}(?:认可|赞赏)", re.I)
DELAY = re.compile(r"进度严重落后|里程碑.{0,8}(?:miss|错过|未完成)|延[期后]|卡住|受阻|无法.{0,8}交付", re.I)
WARNING = re.compile(r"眼前一黑|胸闷|心悸|手发麻|积攒了不少风险|信任危机|爆雷|不妙.{0,8}绩效|炒鱿鱼|纪律处分|严重.{0,8}(?:风险|警告)")
CONSTRAINT = re.compile(r"deadline|截止|工期|排期|延期|保密|泄露|信任|风险|健康|胸闷|手发麻|眼前一黑|晋升|绩效", re.I)
FEATURES = {
    "SHORT_CYCLE_DELIVERABLE": r"如期|开源|原型|最小.{0,4}方案|成熟.{0,5}(?:方案|技术栈)|先.{0,10}交付|快速.{0,8}(?:交付|上线)",
    "LONG_CYCLE_TECH_ASSET": r"自研|长期.{0,5}资产|搭建.{0,5}体系|引入新框架|基建|数月",
    "OWNERSHIP": r"牵头|负责人|统筹|顶上|主动承担|关键项目|推动.{0,8}(?:落地|修复)",
    "VISIBLE_RESULT": r"交付|上线|验收|成果|里程碑|亮相|量化.{0,8}(?:价值|ROI)|可见",
    "RECOGNITION_SEEKING": r"汇报|申请晋升|邀.{0,6}(?:领导|Leader|客户)|展示成果|向.{0,8}说明贡献",
    "STAKEHOLDER_ALIGNMENT": r"协调|沟通|对齐|协商|客户确认|评估影响|共同|明确.{0,5}(?:范围|责任|需求)",
    "TRANSPARENCY": r"澄清|如实|坦诚|透明|正式升级|明确风险|记录.{0,5}(?:事实|责任)|披露",
    "MENTORING": r"指导|辅导|帮.{0,8}复盘|带教|帮助新人",
    "NETWORKING": r"人脉|关系|同事|合作|团队|协作",
    "COMPLIANCE_SAFE": r"合规|拒绝.{0,8}(?:接收|抄袭|泄露|报销)|保密|合法|诚实|不撒谎",
    "RISKY_SHORTCUT": r"抄袭|暗借|隐瞒|绕过|伪造|悄悄|硬撑|跟着去.{0,5}报销|甩锅",
    "RESOURCE_RECOVERY": r"休息|健康恢复|心理修复|理疗|调整作息|清理.{0,5}隐患|处理历史埋雷",
    "AVOIDANCE": r"不管|婉拒|不再掺和|保持沉默|低调避险|不行动|等.{0,8}处理",
    "REPORT_ONLY": r"准备汇报材料|向领导汇报成果",
}


def digest(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def number(value: Any) -> int | float | None:
    return value if isinstance(value, (int, float)) and not isinstance(value, bool) else None


def choice_index(value: Any) -> int | None:
    # Some historical successful calls supplied "1" and the official tool
    # accepted it. Retain the original type, normalize only unambiguous digits.
    if isinstance(value, int) and not isinstance(value, bool):
        return value
    return int(value) if isinstance(value, str) and re.fullmatch(r"[0-9]+", value) else None


def public_status(state: dict) -> dict:
    status = state.get("status") or {}
    lower = {str(k).lower(): v for k, v in status.items()}
    return {key: number(lower.get(name)) for key, name in STATS.items()} | {"level": lower.get("level"), "tenure": number(lower.get("duration_in_level"))}


def advertised(choice: dict) -> dict:
    updates = choice.get("status_updates")
    updates = updates if isinstance(updates, dict) else {}
    lower = {str(k).lower(): v for k, v in updates.items()}
    # No hidden stock comes from current_state, receipts, or other objects.
    return {key: number(lower.get(name)) for key, name in STATS.items()} | {"HiddenRisk": number(lower.get("hiddenrisk"))}


def public_event(event: Any) -> dict:
    event = event if isinstance(event, dict) else {}
    return {key: event[key] for key in ("title", "description", "rules", "remaining_energy", "energy_budget", "max_selections") if key in event}


def menu(choices: Any) -> list[dict]:
    if not isinstance(choices, list):
        return []
    return [{"choice": item.get("choice"), "action": str(item.get("action") or ""), "description": str(item.get("description") or ""), "energy_cost": number(item.get("energy_cost")), "advertised": advertised(item)} for item in choices if isinstance(item, dict)]


def phase(event: dict, choices: list[dict]) -> str:
    if any(c["action"] in ("申请关键项目", "低调避险") for c in choices):
        return "MAIN"
    if any(c["energy_cost"] is not None for c in choices):
        return "ENERGY"
    if "手册" in str(event.get("title", "")):
        return "HANDBOOK"
    return "STORY"


def text_signals(text: str) -> dict:
    delivered, recognized = bool(RESULT.search(text)), bool(RECOGNITION.search(text))
    # Generic praise alone is never an externally verified deliverable.
    return {"delivered": delivered, "recognized": recognized, "delay": bool(DELAY.search(text)), "warning": bool(WARNING.search(text)), "constraint": bool(CONSTRAINT.search(text)), "result_strength": 3 if delivered and recognized else (2 if delivered else (1 if re.search(r"推进|进展|计划|准备|承诺|开展", text) else 0)), "basis": "LEXICAL_RESEARCH_PROXY_REQUIRES_SEMANTIC_REVIEW"}


def snapshot(data: dict, line: int, seq: Any) -> dict:
    state = data["current_state"]
    event, choices = public_event(data.get("current_event")), menu(data.get("choices"))
    time = state.get("time") or {}
    return {"line": line, "seq": seq, "session": state.get("session_id") or data.get("session_id"), "month": number(time.get("current_month")), "quarter": number(time.get("current_quarter")), "status": public_status(state), "event": event, "choices": choices, "feed": str(data.get("events") or ""), "flags": {key: (state.get("simulation_flags") or {}).get(key) for key in ("alive", "failed", "failure_reason")}, "score": {key: val for key, val in (data.get("ending_score") or {}).items() if key in ("quantitative_score", "competition_partial_score", "survival_months", "completed", "outcome", "grade")}, "fingerprint": digest({"event": event, "choices": choices})}


def parse_run(source: dict) -> tuple[list[dict], list[dict], dict]:
    path = Path(source["events"])
    content = path.read_bytes()
    if hashlib.sha256(content).hexdigest() != source["sha256"]:
        raise ValueError(f"{source['run']}: source hash mismatch")
    calls, seen_results, new_ids = {}, set(), []
    current = pending = None
    transitions, reviews, observations = [], [], []
    exclusions = Counter()
    review_keys = set()
    for line, raw in enumerate(content.decode("utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        record = json.loads(raw)
        node = _node(record)
        if record.get("kind") == "tool_call":
            call = node.get("tool_call") or {}
            cid = call.get("tool_call_id")
            if not cid:
                exclusions["call_without_identity"] += 1
                continue
            if cid in calls:
                exclusions["duplicate_wire_calls"] += 1
                continue
            name, args = str(call.get("name") or ""), _arguments(call)
            calls[cid] = {"name": name, "args": args, "line": line, "seq": record.get("seq")}
            if "take_action" in name:
                if pending:
                    exclusions["no_observe_before_next_action"] += 1
                    if pending["receipt"] != "SUCCESS":
                        exclusions["superseded_failed_or_unknown_receipt"] += 1
                pending = {"cid": cid, "call": calls[cid], "pre": current, "receipt": "UNKNOWN"}
            continue
        if record.get("kind") != "tool_result":
            continue
        cid = node.get("tool_call_id")
        if not cid:
            continue
        if cid in seen_results:
            exclusions["duplicate_wire_results"] += 1
            continue
        seen_results.add(cid)
        name = str(node.get("tool_name") or calls.get(cid, {}).get("name") or "")
        data = _result(node)
        if "new_game" in name and data.get("session_id"):
            new_ids.append(data["session_id"])
        if "take_action" in name and pending and cid == pending["cid"]:
            raw_result = node.get("raw_output") or {}
            pending["receipt"] = "SUCCESS" if data.get("success") is True or raw_result.get("success") is True else ("FAIL" if data.get("success") is False or node.get("error") or node.get("is_error") or raw_result.get("isError") else "UNKNOWN")
        if "observe" not in name or not isinstance(data.get("current_state"), dict):
            continue
        post = snapshot(data, line, record.get("seq"))
        observations.append(post)
        match = GRADE.search(post["feed"])
        review_key = (post["month"], match[1] if match else None)
        formal = bool(match and REVIEW.search(post["feed"]) and review_key not in review_keys)
        if formal:
            review_keys.add(review_key)
            # ONLY the action's preceding fresh observe is admissible. Never
            # borrow subsequent same-month capital, later terminal, or reward.
            pre = pending["pre"] if pending else None
            valid = bool(pre and pending["receipt"] == "SUCCESS" and pre["session"] == post["session"])
            recent = [o for o in observations[:-1] if o["line"] > (reviews[-1]["post_observe_line"] if reviews else 0)]
            result_before = [o for o in recent if text_signals(str(o["event"].get("description", "")))["delivered"]]
            warning_before = [o for o in recent if text_signals(o["feed"] + " " + str(o["event"].get("description", "")))["warning"]]
            review = {"run_id": source["run"], "session_id": post["session"], "month": post["month"], "grade": match[1], "level_before": pre["status"]["level"] if valid else None, "tenure_before": pre["status"]["tenure"] if valid else None, "level_after": post["status"]["level"], "promoted": pre["status"]["level"] != post["status"]["level"] if valid else None, "pre": pre["status"] if valid else None, "first_review_state": post["status"], "pre_observe_line": pre["line"] if valid else None, "trigger_action_line": pending["call"]["line"] if valid else None, "trigger_action_id": pending["cid"] if valid else None, "post_observe_line": line, "source_path": str(path), "boundary_status": "EXACT_ACTION_FRESH_PAIR" if valid else "INSUFFICIENT_PRE_BOUNDARY", "pre_result_observe_lines": [o["line"] for o in result_before], "pre_warning_observe_lines": [o["line"] for o in warning_before], "pre_result_strength": max((text_signals(str(o["event"].get("description", "")))["result_strength"] for o in recent), default=0), "public_result_basis": "RESEARCH_TEXT_LABEL; PRE_OBSERVATIONS_ONLY", "first_review_feedback": post["feed"][:2000]}
            reviews.append(review)
            review["pre_constraint_observe_lines"] = [
                o["line"] for o in recent
                if text_signals(o["feed"] + " " + str(o["event"].get("description", "")))["constraint"]
            ]
        if pending:
            pre = pending["pre"]
            args = pending["call"]["args"]
            index = choice_index(args.get("choice"))
            selected = next((c for c in pre["choices"] if choice_index(c["choice"]) == index), None) if pre and index is not None else None
            if pending["receipt"] != "SUCCESS":
                exclusions["failed_or_unknown_receipt"] += 1
            elif not pre or pre["session"] != post["session"]:
                exclusions["missing_or_mismatched_pre_state"] += 1
            elif not selected or index is None:
                exclusions["choice_not_current_legal_integer"] += 1
            elif pre["status"] == post["status"] and pre["month"] == post["month"] and pre["fingerprint"] == post["fingerprint"]:
                exclusions["receipt_without_visible_state_or_event_change"] += 1
            else:
                cross = pre["month"] != post["month"]
                promoted = pre["status"]["level"] != post["status"]["level"]
                post_text = str(post["event"].get("description", "")) + " " + post["feed"]
                signals = text_signals(post_text)
                row = {"run_id": source["run"], "candidate_id": source["candidate"], "final_score": number(source.get("quantitative_score")), "final_survival_months": number(source.get("survival_months")), "final_level": source.get("final_or_last_level"), "session_id": pre["session"], "month": pre["month"], "quarter": pre["quarter"], "level": pre["status"]["level"], "tenure_in_level": pre["status"]["tenure"], "phase": phase(pre["event"], pre["choices"]), "event_public_fingerprint": pre["fingerprint"], "event_public_summary": str(pre["event"].get("description", ""))[:1800], "choice_count": len(pre["choices"]), "selected_choice_index": args.get("choice"), "selected_choice_text": selected["action"], "selected_choice_description": selected["description"], "selected_action_features": [key for key, pattern in FEATURES.items() if re.search(pattern, selected["action"] + " " + selected["description"])], "legal_choice_features": [{"choice": c["choice"], "features": [key for key, pattern in FEATURES.items() if re.search(pattern, c["action"] + " " + c["description"])]} for c in pre["choices"]], "advertised_energy_cost": selected["energy_cost"], "advertised_HiddenRisk_delta_if_visible": selected["advertised"]["HiddenRisk"], "cross_month": cross, "review_in_transition": formal, "review_grade": match[1] if formal else None, "promotion_in_transition": promoted, "level_after": post["status"]["level"], "post_month": post["month"], "public_result_signal": signals["delivered"], "public_recognition_signal": signals["recognized"], "public_warning_signal": signals["warning"], "public_constraint_signal": signals["constraint"], "public_delay_signal": signals["delay"], "result_strength_proxy": signals["result_strength"], "post_public_text": post_text[:2800], "response_scope": "MIXED_CROSS_MONTH_REVIEW_OR_LEVEL" if cross or formal or promoted else "LOCAL_SAME_MONTH_LEVEL; DELAYED_EVENT_EFFECTS_STILL_POSSIBLE", "source_path": str(path), "source_sha256": source["sha256"], "action_tool_call_id": pending["cid"], "action_raw_line": pending["call"]["line"], "action_seq": pending["call"]["seq"], "pre_observe_raw_line": pre["line"], "post_observe_raw_line": line, "pre_observe_seq": pre["seq"], "post_observe_seq": post["seq"]}
                for dim in STATS:
                    before, after = pre["status"][dim], post["status"][dim]
                    row.update({f"pre_{dim}": before, f"post_{dim}": after, f"advertised_{dim}_delta": selected["advertised"][dim]})
                    if dim != "E":
                        row[f"realized_{dim}_delta"] = after - before if before is not None and after is not None else None
                row.update(selected_choice_index=index, raw_choice_argument_type=type(args.get("choice")).__name__, official_success_with_string_choice=isinstance(args.get("choice"), str))
                transitions.append(row)
            pending = None
        current = post
    if pending:
        exclusions["no_post_observe_at_end"] += 1
    sessions = {o["session"] for o in observations}
    if len(new_ids) != 1 or sessions != {new_ids[0]}:
        raise ValueError(f"{source['run']}: fresh session identity not established")
    terminal = next((o for o in reversed(observations) if o["score"]), None)
    if terminal and number(source.get("quantitative_score")) != terminal["score"].get("quantitative_score"):
        raise ValueError(f"{source['run']}: terminal score mismatch")
    for row in transitions:
        future = next((r for r in reviews if r["post_observe_line"] >= row["post_observe_raw_line"]), None)
        row.update(next_review_month=future["month"] if future else None, next_review_grade=future["grade"] if future else None, next_review_promotion=future["promoted"] if future else None, terminal_within_6m=bool(terminal["month"] <= row["month"] + 6) if terminal and row["month"] is not None else None)
    stats = {"run_id": source["run"], "candidate_id": source["candidate"], "session_id": new_ids[0], "source_path": str(path), "sha256": source["sha256"], "bytes": len(content), "identity_reference": source.get("identity_reference"), "observes": len(observations), "transitions": len(transitions), "reviews": len(reviews), "promotions": sum(r["promoted"] is True for r in reviews), "phase_counts": dict(Counter(r["phase"] for r in transitions)), "excluded": dict(exclusions), "natural_terminal": bool(terminal), "terminal_observe_line": terminal["line"] if terminal else None, "terminal_public_score": terminal["score"] if terminal else None, "final_public_state": observations[-1]["status"] if observations else None, "max_month": max((o["month"] for o in observations if o["month"] is not None), default=None)}
    return transitions, reviews, stats


def build(manifest: Path, output_dir: Path) -> dict:
    data = json.loads(manifest.read_text(encoding="utf-8"))
    transitions, reviews, runs = [], [], []
    for source in data["runs"]:
        t, r, s = parse_run(source)
        transitions.extend(t)
        reviews.extend(r)
        runs.append(s)
    output_dir.mkdir(parents=True, exist_ok=True)
    for name, rows in (("policy_transitions.jsonl", transitions), ("promotion_frontiers.jsonl", reviews)):
        (output_dir / name).write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows), encoding="utf-8")
    result = {"schema_version": 1, "method": "EXPLICIT_HASH_LOCKED_SINGLE_SESSION_DEDUP_SUCCESS_ACTION_FRESH_OBSERVE", "runs": runs, "transitions": len(transitions), "reviews": len(reviews), "promotions": sum(r["promoted"] is True for r in reviews), "limitations": ["Logged policy data, no controlled causality", "Text labels are lexical proxies, require semantic validation", "Mixed transitions excluded from local clean response estimates", "All future outcomes are labels, never features for preceding decisions", "UNKNOWN/null never imputed"]}
    (output_dir / "dataset_summary.json").write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sources", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(build(args.sources, args.output_dir), ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
