"""Current v13 identity, frozen shell and written policy contract checks.

A-H validate static rule coverage only. They do not execute an LLM or establish
that a runtime Candidate follows the policy in a game.
"""
import hashlib
import json
import re
import subprocess
from pathlib import Path

import pytest
from career_sim_runner.skill_contract import validate_skill_frontmatter

ROOT = Path(__file__).resolve().parents[1]
BASE = "8267d420da29888d0a05403991f8980e251aaa0c"
CURRENT = "candidate-v13-empirical-promotion-playbook"
PARENT = "candidate-v8a-v7o-donor-core-transplant"
SKILLS = ("structured-state-board", "rolling-planning", "delivery-progress", "risk-review")


def git_bytes(path):
    return subprocess.check_output(["git", "show", f"{BASE}:{path}"], cwd=ROOT)


def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf8"))


def planning():
    return (ROOT / "skills/rolling-planning/SKILL.md").read_text(encoding="utf8")


def section(rule):
    return planning().split(f"### {rule}｜", 1)[1].split("\n### ", 1)[0].split("\n## ", 1)[0]


def test_current_identity_parent_fallback_flags_and_source_hashes():
    c = load("configs/current_candidate.json")
    parent = json.loads(git_bytes("configs/current_candidate.json"))
    manifest = load("configs/runtime_manifest.json")
    assert c["candidate_id"] == manifest["name"] == CURRENT
    assert c["parent_candidate_id"] == parent["candidate_id"] == PARENT
    assert c["base_main_sha"] == BASE
    assert c["status"] == "STATIC_IMPLEMENTED_NOT_RUNTIME_VALIDATED"
    assert c["decision"] == "S10_05_EMPIRICAL_PROMOTION_POLICY_STATIC"
    assert c["architecture"] == parent["architecture"]
    assert c["runtime_contract_delta"] == parent["runtime_contract_delta"]
    assert c["runner_sha"] == parent["runner_sha"]
    assert set(c["validation"]) == set(parent["validation"]) | {"stable_75_plus_proven"}
    assert all(value is False for value in c["validation"].values())
    assert c["fallback"]["candidate_id"] == PARENT
    assert c["fallback"]["source_commit"] == BASE
    assert c["fallback"]["status"] == parent["status"]
    assert c["fallback"]["runtime_manifest_sha256"] == parent["runtime_manifest"]["sha256"]
    assert c["fallback"]["skills"] == parent["skills"]
    assert c["fallback"]["historical_gameplay_evidence_transfers_to_current_candidate"] is False
    assert c["parent_identity"] == {
        "runtime_manifest_sha256": parent["runtime_manifest"]["sha256"],
        "instruction_sha256": parent["runtime_manifest"]["instruction_sha256"],
        "skills": parent["skills"],
    }
    # Canonical LF metadata remains portable in a CRLF Windows checkout.
    mb = (ROOT / c["runtime_manifest"]["path"]).read_bytes().replace(b"\r\n", b"\n")
    assert c["runtime_manifest"]["sha256"] == hashlib.sha256(mb).hexdigest()
    assert c["runtime_manifest"]["instruction_sha256"] == hashlib.sha256(manifest["instruction"].encode()).hexdigest()
    assert len(c["skills"]) == 4 and {x["name"] for x in c["skills"]} == set(SKILLS)
    for entry in c["skills"]:
        blob = subprocess.check_output(["git", "hash-object", f"--path={entry['path']}", entry["path"]], cwd=ROOT, text=True).strip()
        assert blob == entry["git_blob"]
    assert c["empirical_policy"]["rules"] == [f"R{i}" for i in range(1, 10)]
    assert c["empirical_policy"]["evidence_admission_decision"] == "EVIDENCE_DELTA_DEFERRED_TO_KEEP_POLICY_EXPERIMENT_CLEAN"


def test_exact_frozen_skills_runner_dependencies_and_historical_evidence():
    for name in SKILLS:
        path = ROOT / f"skills/{name}/SKILL.md"
        assert validate_skill_frontmatter(path.parent) == []
        assert "Can Submit Action: No." in path.read_text(encoding="utf8")
        if name != "rolling-planning":
            assert path.read_bytes().replace(b"\r\n", b"\n") == git_bytes(f"skills/{name}/SKILL.md")
    protected = ["career_sim_runner", "pyproject.toml", "uv.lock", "skills/structured-state-board", "skills/delivery-progress", "skills/risk-review", "docs/project/research", "docs/project/runs", "configs/retry_policy.json"]
    assert subprocess.check_output(["git", "diff", "--name-only", BASE, "--", *protected], cwd=ROOT).strip() == b""


def test_manifest_changes_only_name_and_critical_kernel_and_planning_is_shorter():
    current = load("configs/runtime_manifest.json")
    parent = json.loads(git_bytes("configs/runtime_manifest.json"))
    assert current.keys() == parent.keys()
    assert current["team"] == parent["team"] and current["mode"] == parent["mode"] == "agent"
    def split(text):
        prefix, rest = text.split("CRITICAL KERNEL\n", 1)
        kernel, suffix = rest.split("\n\nSTARTUP AND FLOW\n", 1)
        return prefix, kernel, suffix
    before, after = split(parent["instruction"]), split(current["instruction"])
    assert before[0] == after[0] and before[2] == after[2]
    assert len(current["instruction"]) < 5000
    old = git_bytes("skills/rolling-planning/SKILL.md").decode("utf8")
    assert len(planning()) < len(old) * .65
    assert len(planning().splitlines()) < len(old.splitlines())
    for token in ["REVIEW_PLAN = <Objective | Primary Gap | Next Observable Checkpoint>", "MODE = A | S", "RECOVERY=NONE|PROGRESSION|RESOURCE|RISK|DELIVERY|UNKNOWN", "PLAN:", "CANDIDATE: choice=<one legal integer>", "ONE FRESH OBSERVE = ONE PLANNING PASS", "genuinely competitive candidates", "Risk=RECONSIDER", "RB=NONE|DONE|BLOCKED"]:
        assert token in planning()
    assert re.findall(r"^### (R[1-9])｜", planning(), re.M) == [f"R{i}" for i in range(1, 10)]


# Written scenarios from the task: assert the governing rule contains both the
# intended decision and its guard/exception. No fake deterministic policy engine.
@pytest.mark.parametrize("case,rule,requirements", [
    ("A_M6_deliverability", "R3", ["窗口内能完成", "明确 owner", "公开结果", "长期方案明确能及时完成", "material quality/safety/compliance cost"]),
    ("B_clean_NO_GAIN", "R5", ["相同 Level/可比 context", "clean NO_GAIN", "折价", "responsive alternative", "独立价值", "Level/context/material condition", "一次 flat 不构成永久 cap"]),
    ("C_one_step_Energy", "R6", ["每次只选一个 Energy action", "one action → fresh observe → re-rank", "丢弃旧 remaining-action intent", "禁止整季 recipe、multi-step sequence/批次"]),
    ("D_conditional_key_project", "R7", ["不是 default answer", "实际可兑现 ownership", "负荷可承受", "blocked/stale", "条件不成立时比较", "不固定替代顺序"]),
    ("E_ordinary_cost", "R8", ["普通负 Health", "workload", "不自动 S", "无数字阈值"]),
    ("F_material_danger", "R8", ["只有当前未解除", "acute physical", "explicit trust/job/compliance/confidentiality escalation", "高 Health 不证明", "最小必要保护", "解除或场景结束即回 A"]),
    ("G_result_hierarchy", "R4", ["promise/progress < delivered/completed < externally/publicly recognized result", "generic praise", "不等于 verified deliverable", "不是 hidden score 或 promotion requirement"]),
    ("H_no_advance", "R9", ["no-advance 必须重排", "哪些结果未兑现", "不响应", "最可兑现", "不能继续 stale recipe", "机械追 lowest stat"]),
])
def test_static_scenario_rule_and_exceptions(case, rule, requirements):
    text = section(rule)
    for requirement in requirements:
        assert requirement in text, (case, requirement)
    if case.startswith("E_"):
        assert "普通成本可为明显更强的成长/结果接受" in section("R7")


def test_no_research_dump_and_no_evidence_admission_delta():
    runtime = planning() + load("configs/runtime_manifest.json")["instruction"]
    for forbidden in ["1,626", "75.29", "72.65", "9/3/3/2", "3/6/16/26/38", "RUN07", "RUN08", "S10-04", "自研内核 vs", "18个月必升"]:
        assert forbidden not in runtime
    assert "public-status-unclear numeric status_updates" in planning()
    assert "EXCLUDE_FROM_STRATEGY until verified public" in planning()
    assert "不得推断隐藏 threshold/cap/weight" in runtime
    state = (ROOT / "docs/project/CURRENT_STATE.md").read_text(encoding="utf8")
    assert f"Current Candidate: `{CURRENT}`" in state
    assert "IN_FLIGHT_EVIDENCE" in state and "NEXT_GAME=NOT_AUTHORIZED" in state
