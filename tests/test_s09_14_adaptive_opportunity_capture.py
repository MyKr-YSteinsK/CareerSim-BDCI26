"""Written-policy scenarios and frozen identity checks, without model/game calls.

These assertions check the supplied Skill contract, not an LLM's choices or score.
"""

import hashlib
import json
import re
import subprocess
from pathlib import Path

import pytest

from career_sim_runner.skill_contract import validate_submission_contract
from scripts.package_candidate import build_submission


ROOT = Path(__file__).resolve().parents[1]
BASE = "a2bf214b6f4c6923399f80ada03b4d61d97f6eaa"
PARENT = "candidate-v8a-v7o-donor-core-transplant"
CANDIDATE = "candidate-v9a-adaptive-opportunity-capture"
DELTA = "ADAPTIVE_OPPORTUNITY_CAPTURE_WITH_BOUNDED_UNTESTED_PROBE"
PLANNING = "skills/rolling-planning/SKILL.md"
HEADER = "### Bounded untested probe\n\n"


def source(path):
    return subprocess.check_output(["git", "show", f"{BASE}:{path}"], cwd=ROOT)


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


def probe_block():
    return read(PLANNING).split(HEADER)[1].split("## Quarterly control\n")[0]


def test_identity_parent_hashes_and_no_inherited_validation():
    parent = json.loads(source("configs/current_candidate.json"))
    candidate = json.loads(read("configs/current_candidate.json"))
    manifest = json.loads(read("configs/runtime_manifest.json"))
    assert candidate["candidate_id"] == manifest["name"] == CANDIDATE
    assert candidate["parent_candidate_id"] == parent["candidate_id"] == PARENT
    assert candidate["base_main_sha"] == BASE
    assert candidate["status"] == "STATIC_ONLY_NOT_SUBMISSION_VALIDATED"
    assert candidate["strategy_delta"] == DELTA
    assert candidate["validation"] == {key: False for key in parent["validation"]}
    assert candidate["parent_identity"] == {
        "runtime_manifest_sha256": parent["runtime_manifest"]["sha256"],
        "instruction_sha256": parent["runtime_manifest"]["instruction_sha256"],
        "skills": parent["skills"],
    }
    assert candidate["runtime_manifest"]["sha256"] == hashlib.sha256(
        (ROOT / "configs/runtime_manifest.json").read_bytes()
    ).hexdigest()
    assert candidate["runtime_manifest"]["instruction_sha256"] == hashlib.sha256(
        manifest["instruction"].encode()
    ).hexdigest()
    for skill in candidate["skills"]:
        assert skill["git_blob"] == subprocess.check_output(
            ["git", "hash-object", skill["path"]], cwd=ROOT, text=True
        ).strip()
    for key in ("architecture", "runtime_contract_delta", "runner_sha", "strategy_donor"):
        assert candidate[key] == parent[key]
    assert candidate["adopted_mechanisms"] == parent["adopted_mechanisms"] + [DELTA]


def test_manifest_changes_only_candidate_name_and_preserves_full_shell():
    parent = json.loads(source("configs/runtime_manifest.json"))
    parent["name"] = CANDIDATE
    assert json.loads(read("configs/runtime_manifest.json")) == parent


def test_planning_is_parent_plus_one_short_local_response_block():
    planning = read(PLANNING)
    insertion = HEADER + probe_block()
    assert planning.count(HEADER) == 1
    assert planning.replace(insertion, "", 1) == source(PLANNING).decode()
    assert len(insertion) <= 800  # Static prose budget, never a gameplay threshold.
    assert HEADER not in source(PLANNING).decode()


@pytest.mark.parametrize("scenario,local_clauses,inherited_clauses", [
    ("output_no_gain_untested_skill_enters_comparison_not_auto_win", (
        "仅当拟继续路径有 fresh clean local NO_GAIN/stagnation",
        "合法未测试、公开语义支持高价值的 growth family",
        "加入 top candidate comparison", "不自动选择",
        "职业价值、ownership/visible result、多维价值、普通成本、交付成本及生存/合规约束",
    ), ()),
    ("output_no_gain_exploit_responsive_network_before_probe", (
        "当前 Level/context 无更高价值的 known responsive 合法替代",
        "binding 保护 → exploit 已知高价值响应路径 → 比较 bounded probe",
    ), ("存在 responsive alternative 时不立即重复同一路径",)),
    ("network_no_gain_preserves_ownership_story_value", (
        "ownership/visible result、多维价值",
        "stalled path 仅凭仍有强独立多维/交付价值可胜出",
    ), ("当前 participant-visible event description 与 legal choice semantics",
        "gap 不构成硬 gating tree", "多维动作保留其它维度及 ownership/结果价值")),
    ("near_delivery_can_block_output_no_gain_probe", (
        "probe 会明显破坏近期 binding 交付义务时，禁止加入", "交付成本",
    ), ("If an active high-value commitment is near a public result",)),
    ("explicit_health_safety_threat_blocks_probe", (
        "生存/合规/信任有重大 binding 约束", "时，禁止加入",
    ), ("explicit acute physical symptoms", "smallest reasonable action",
        "Return to `MODE=A` when fresh public evidence")),
    ("explicit_compliance_trust_threat_blocks_probe", (
        "生存/合规/信任有重大 binding 约束", "binding 保护 → exploit",
    ), ("active trust/compliance/confidentiality crisis", "明确 public warning",
        "仅持续/再次/新的同类 warning 才允许再次 cleanup")),
    ("probe_gain_updates_local_response_without_quota", (
        "probe 胜出只选一次 action，executor 随后 fresh observe",
        "响应只更新 current Level/context/local family/dimension",
        "GAIN 不证明该 family 最好", "不新增 S/N/O 或 exploration quota",
    ), ("ONE FRESH OBSERVE = ONE PLANNING PASS",)),
    ("probe_no_gain_local_discount_no_automatic_second_probe", (
        "NO_GAIN 仅局部折价，不永久放弃",
        "结果不授权下一次 probe，不连续 probe 两个未知 family",
        "不推全局 cap、隐藏阈值或永久偏好",
    ), ("不把局部 NO_GAIN 传播给未测试 family",)),
    ("level_change_reopens_existing_option_value_rule", (
        "当前 Level/context", "current Level/context/local family/dimension",
    ), ("Level change 后依 Board 重置", "UNKNOWN 保持开放")),
    ("strong_responsive_path_no_unnecessary_exploration", (
        "无更高价值的 known responsive 合法替代",
        "UNKNOWN 不当 GAIN，不为覆盖率探索，不固定 Skill 偏好",
        "仍最多两个候选、比较一次",
    ), ("use `A` and continue promotion-first progression",)),
])
def test_ten_written_policy_scenarios(scenario, local_clauses, inherited_clauses):
    assert all(clause in probe_block() for clause in local_clauses), scenario
    assert all(clause in read(PLANNING) for clause in inherited_clauses), scenario


@pytest.mark.parametrize("path", [
    "skills/structured-state-board/SKILL.md", "skills/delivery-progress/SKILL.md",
    "skills/risk-review/SKILL.md", "career_sim_runner", "pyproject.toml", "uv.lock",
])
def test_frozen_surfaces_have_no_delta_from_exact_v8a_parent(path):
    assert not subprocess.check_output(
        ["git", "diff", "--name-only", BASE, "--", path], cwd=ROOT, text=True
    ).strip()


def test_public_only_no_lookup_quota_or_added_machine():
    block = probe_block()
    assert not re.search(r"\bM\d+\b|\b(?:event_id|event_title)\s*=", block)
    assert "Output" not in block and "Network" not in block and "技能学习" not in block
    assert "不新增 S/N/O 或 exploration quota、budget、ledger、state machine" in block
    assert "UNKNOWN 不当 GAIN" in block
    assert "EXCLUDE_FROM_STRATEGY until verified public" in read(PLANNING)
    parent = json.loads(source("configs/current_candidate.json"))
    candidate = json.loads(read("configs/current_candidate.json"))
    assert candidate["rejected_mechanisms"] == parent["rejected_mechanisms"]


def test_v8a_fallback_is_rebuildable_and_valid_without_install(tmp_path):
    candidate = json.loads(read("configs/current_candidate.json"))
    parent = json.loads(source("configs/current_candidate.json"))
    fallback = candidate["submission_fallback"]
    assert fallback["candidate_id"] == PARENT and fallback["source_commit"] == BASE
    assert fallback["runtime_manifest"] == parent["runtime_manifest"]
    assert fallback["skills"] == parent["skills"]
    assert fallback["v9a_submission_replacement"] == "NOT_AUTHORIZED"
    repo = tmp_path / "fallback-source"
    for path in ["configs/current_candidate.json", "configs/runtime_manifest.json"] + [
        skill["path"] for skill in parent["skills"]
    ]:
        destination = repo / path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(source(path))
    bundle = tmp_path / "fallback-bundle"
    build_submission(repo, bundle)
    assert json.loads((bundle / "manifest.json").read_text(encoding="utf-8"))["name"] == PARENT
    details = validate_submission_contract(bundle)
    assert details["submission_mode"] == "skill_bundle"
    assert set(details["skill_ids"]) == set(candidate["architecture"]["active_skills"])
    for skill in parent["skills"]:
        assert (bundle / skill["path"]).read_bytes() == source(skill["path"])
