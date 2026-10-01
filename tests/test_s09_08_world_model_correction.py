"""Written-contract coverage and protected diff; no LLM/game behavior oracle."""

import hashlib
import json
import re
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
BASE = "f5dc8454269933efc6f4d31869d7edcbd3bcdc28"
CURRENT = "candidate-v7z-world-model-correction"
DELTA = "LOCAL_RESPONSE_DOES_NOT_IMPLY_GLOBAL_CAP"
START = "## Local Response / World Model Boundary\n"
END = "## Ranking\n"


def text(path):
    return (ROOT / path).read_text(encoding="utf-8")


def base_text(path):
    return subprocess.check_output(["git", "show", f"{BASE}:{path}"], cwd=ROOT).decode("utf-8").replace("\r\n", "\n")


def correction():
    return text("skills/rolling-planning/SKILL.md").split(START)[1].split(END)[0]


def test_identity_hashes_four_skills_and_validation_reset():
    candidate = json.loads(text("configs/current_candidate.json"))
    manifest = json.loads(text("configs/runtime_manifest.json"))
    parent = json.loads(base_text("configs/current_candidate.json"))
    assert candidate["candidate_id"] == manifest["name"] == CURRENT
    assert candidate["parent_candidate_id"] == parent["candidate_id"]
    assert candidate["base_main_sha"] == BASE
    assert candidate["strategy_delta"] == candidate["adopted_mechanisms"][-1] == DELTA
    assert candidate["adopted_mechanisms"][:-1] == parent["adopted_mechanisms"]
    assert candidate["parent_identity"]["skills"] == parent["skills"]
    assert candidate["parent_identity"]["runtime_manifest_sha256"] == parent["runtime_manifest"]["sha256"]
    assert candidate["parent_identity"]["instruction_sha256"] == parent["runtime_manifest"]["instruction_sha256"]
    assert candidate["runtime_manifest"]["sha256"] == hashlib.sha256((ROOT / "configs/runtime_manifest.json").read_bytes()).hexdigest()
    assert candidate["runtime_manifest"]["instruction_sha256"] == hashlib.sha256(manifest["instruction"].encode()).hexdigest()
    assert len(candidate["skills"]) == candidate["architecture"]["skill_count"] == 4
    assert all(value is False for value in candidate["validation"].values())
    for entry in candidate["skills"]:
        assert entry["git_blob"] == subprocess.check_output(["git", "hash-object", entry["path"]], cwd=ROOT, text=True).strip()


@pytest.mark.parametrize("scenario,clauses", [
    ("A_Output_no_gain_others_unknown_no_binding", ("clean public pair", "dimension / action family", "evidence window", "UNKNOWN", "不能自动赋值为零", "MODE=A")),
    ("B_multiple_local_no_gains", ("即使 S/N/O 各有局部 NO_GAIN", "不证明当前 Level 全局 saturation", "responsibility / project ownership / cross-functional / visible-result", "未测试的合法 family")),
    ("C_recovery_and_unknown_growth", ("survival/risk value", "UNKNOWN / promotion value 必须同时比较", "不得以“其它维度封顶”宣称恢复无机会成本", "不取消必要保护")),
    ("D_Mentor_visible_output_cost", ("明确损失个人产出", "mentor/network upside", "真实比较该 public tradeoff", "不得因假设 Output cap 将产出损失视为零")),
    ("E_first_review_local_response", ("首次正式 Review 前", "broad promotion-compounding prior", "不因单个局部 NO_GAIN 收缩为单维 greedy search", "不是 promotion relevance 的唯一代理", "不固定动作、月份或 S/N/O 配额")),
    ("F_fresh_material_threat", ("material binding threat", "binding Delivery", "material public risk", "fresh Story exposure guard", "不改变 Fresh-binding S 或 survival floor")),
])
def test_static_acceptance_scenario_clauses(scenario, clauses):
    # Input categories are named above; this verifies required prohibitions /
    # preserved exceptions exist, not that a model will execute them correctly.
    assert all(clause in correction() for clause in clauses), scenario


def test_local_label_preserves_board_enum_and_no_hidden_model():
    rule = correction()
    for clause in ("不新增 Board enum 或状态表", "跨月、Review", "保持 `UNKNOWN`", "不得用过去 Story gain 保证当前 Main gain", "只折价已测试的局部路径", "promotion eligibility 已知", "不得构造 hidden promotion model"):
        assert clause in rule
    assert not re.search(r"(?:Health|H)\s*(?:<=|<|>=|>)\s*\d", rule, re.I)


def test_only_one_planning_section_added_all_existing_rules_frozen():
    current = text("skills/rolling-planning/SKILL.md")
    assert current.count(START) == 1
    before, tail = current.split(START)
    assert before + END + tail.split(END, 1)[1] == base_text("skills/rolling-planning/SKILL.md")


@pytest.mark.parametrize("path", [
    "skills/structured-state-board/SKILL.md", "skills/delivery-progress/SKILL.md",
    "skills/risk-review/SKILL.md", "career_sim_runner", "pyproject.toml", "uv.lock",
])
def test_protected_sources_unchanged(path):
    assert subprocess.check_output(["git", "diff", "--name-only", BASE, "--", path], cwd=ROOT, text=True).strip() == ""


def test_manifest_only_two_strategy_paragraphs_change():
    current = json.loads(text("configs/runtime_manifest.json"))
    parent = json.loads(base_text("configs/runtime_manifest.json"))
    assert len(current["instruction"]) <= 5000
    assert {k: v for k, v in current.items() if k not in ("name", "instruction")} == {k: v for k, v in parent.items() if k not in ("name", "instruction")}
    paragraphs = []
    for item in (current, parent):
        parts = item["instruction"].split("\n\n")
        selected = [p for p in parts if p.startswith(("MODE=A：", "clean NO_GAIN"))]
        assert len(selected) == 2
        paragraphs.append([p for p in parts if p not in selected])
    assert paragraphs[0] == paragraphs[1]
    for clause in ("UNKNOWN保留价值", "action family/证据窗", "恢复/避险有成长机会成本", "Story产出成本不得以cap折零", "首评前不做单维贪心", "即时数值非唯一晋升代理"):
        assert clause in current["instruction"]


def test_no_fixed_answer_threshold_or_runtime_marker_schema_added():
    runtime_delta = correction()
    assert "申请关键项目" not in runtime_delta
    assert not re.search(r"\bM(?:6|12)\b|choice\s*=\s*\d", runtime_delta)
    candidate = json.loads(text("configs/current_candidate.json"))
    parent = json.loads(base_text("configs/current_candidate.json"))
    for key in ("architecture", "runtime_contract_delta", "runner_sha", "deferred_mechanisms", "rejected_mechanisms"):
        assert candidate[key] == parent[key]
