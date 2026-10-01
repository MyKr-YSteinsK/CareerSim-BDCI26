"""Static donor fidelity, shell preservation and five written scenario contracts.

No provider calls or simulated model behavior; scenarios check policy clauses only.
"""
import hashlib
import json
import re
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
BASE = "9376b11d7a65231dc2c20fc910b7313bec36187c"
DONOR = "b2e7ea6441da9c314d8a0ffbf29b9d5800ced10d"
ID = "candidate-v8a-v7o-donor-core-transplant"


def text(path):
    return (ROOT / path).read_text(encoding="utf-8")


def source(revision, path):
    return subprocess.check_output(["git", "show", f"{revision}:{path}"], cwd=ROOT).decode("utf-8")


def test_identity_and_all_validation_flags_reset():
    c = json.loads(text("configs/current_candidate.json"))
    m = json.loads(text("configs/runtime_manifest.json"))
    parent = json.loads(source(BASE, "configs/current_candidate.json"))
    assert c["candidate_id"] == m["name"] == ID
    assert c["parent_candidate_id"] == parent["candidate_id"]
    assert c["base_main_sha"] == BASE
    assert c["strategy_donor"]["source_commit"] == DONOR
    assert c["architecture"] == parent["architecture"]
    assert c["runtime_contract_delta"] == parent["runtime_contract_delta"]
    assert c["validation"] and not any(c["validation"].values())
    assert c["parent_identity"]["skills"] == parent["skills"]
    assert c["runtime_manifest"]["sha256"] == hashlib.sha256((ROOT / "configs/runtime_manifest.json").read_bytes()).hexdigest()
    assert c["runtime_manifest"]["instruction_sha256"] == hashlib.sha256(m["instruction"].encode()).hexdigest()
    for skill in c["skills"]:
        assert skill["git_blob"] == subprocess.check_output(["git", "hash-object", skill["path"]], cwd=ROOT, text=True).strip()


def test_direct_donor_ranking_mode_and_review_sections_are_present_verbatim():
    donor = source(DONOR, "skills/rolling-planning/SKILL.md")
    planning = text("skills/rolling-planning/SKILL.md")
    for start, end in (
        ("## Maintain the Review Plan\n", "## Same-observation decision budget\n"),
        ("## Select MODE\n", "## Rank legal candidates\n"),
        ("## Rank legal candidates\n", "## Public-hint discipline\n"),
        ("## Public-hint discipline\n", "## Story stop rule\n"),
    ):
        assert donor.split(start)[1].split(end)[0].strip() in planning
    main_prior = "For the quarterly Main Action, apply the same ranking. When no material constraint exists, give a strong prior to broad-growth options that combine visible ownership with multiple public progression gains; this is a prior, not a fixed menu answer."
    assert main_prior in donor and main_prior in planning


def test_execution_shell_is_preserved_and_old_x_branch_not_imported():
    now = json.loads(text("configs/runtime_manifest.json"))["instruction"]
    old = json.loads(source(BASE, "configs/runtime_manifest.json"))["instruction"]
    assert now.split("\n\nSTARTUP AND FLOW\n")[1] == old.split("\n\nSTARTUP AND FLOW\n")[1]
    assert now.split("\n\nOWNERSHIP\n")[0] == old.split("\n\nOWNERSHIP\n")[0]
    planning = text("skills/rolling-planning/SKILL.md")
    assert "RB=NONE|DONE|BLOCKED" in planning
    assert "X=0" not in planning and "X=1" not in planning
    assert "new Planning pass" in planning and "旧计划不能授权动作" in planning
    assert "Can Submit Action: No" in planning


@pytest.mark.parametrize("path", [
    "skills/structured-state-board/SKILL.md", "skills/delivery-progress/SKILL.md",
    "skills/risk-review/SKILL.md", "career_sim_runner", "pyproject.toml", "uv.lock",
])
def test_protected_surfaces_are_parent_identical(path):
    assert not subprocess.check_output(["git", "diff", "--name-only", BASE, "--", path], cwd=ROOT, text=True).strip()


@pytest.mark.parametrize("scenario,clauses", [
    ("normal_early_growth", ("Maximize long-horizon progression", "broad Skill / Network / Output progression", "use `A` and continue promotion-first progression")),
    ("single_local_no_gain", ("只折价已测试", "UNKNOWN 保持开放", "不把局部 NO_GAIN 传播给未测试 family", "多维动作保留其它维度")),
    ("fresh_material_threat_then_resolved", ("smallest reasonable action", "Return to `MODE=A` when fresh public evidence", "旧 S/旧理由不续期", "不为补满资源延长 S")),
    ("narrow_review_gap", ("anchor the gap to the clearest public progression deficit", "gap 不构成硬 gating tree", "其它更强 ownership、多维成长或可兑现结果")),
    ("ownership_vs_low_value_action", ("strong prior to broad-growth options that combine visible ownership", "multiple public progression gains", "not a fixed menu answer", "Accept ordinary soft costs")),
])
def test_five_offline_scenario_policy_clauses(scenario, clauses):
    assert all(clause in text("skills/rolling-planning/SKILL.md") for clause in clauses), scenario


def test_simplification_and_no_historical_answer_lookup():
    planning = text("skills/rolling-planning/SKILL.md")
    manifest = json.loads(text("configs/runtime_manifest.json"))["instruction"]
    old = json.loads(source(BASE, "configs/runtime_manifest.json"))["instruction"]
    assert len(planning) < len(source(BASE, "skills/rolling-planning/SKILL.md"))
    assert len(manifest) < len(old)
    for retired in ("Promotion Portfolio", "Dominance expiry", "Story exposure guard", "Failure Recovery Contract"):
        assert retired not in planning
    assert "S09-09" not in planning and DONOR not in planning
    assert not re.search(r"M(?:3|6|12|18)\s*(?:->|→|=)", planning)
    assert "HiddenRisk" in planning and "EXCLUDE_FROM_STRATEGY" in planning
    assert "全局 cap" in planning and "eligibility" in planning
    c = json.loads(text("configs/current_candidate.json"))
    assert "EVENT_ID_OR_TITLE_TO_CHOICE_LOOKUP" in c["rejected_mechanisms"]
