"""S09-05 static regression for bounded A-mode Story exposure guard."""

import json
import re
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
BASE = "da5359d2d9a978475484300cf1f4a75013393329"
CURRENT = "candidate-v7y-story-exposure-guard"
PARENT = "candidate-v7x-fresh-binding-reauthorization"
MECHANISM = "M5_STORY_EXPOSURE_GUARD_AS_BOUNDED_A_MODE_RANKING_PRIOR"


def _text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def _json(path: str) -> dict:
    return json.loads(_text(path))


def test_identity_and_validation_reset() -> None:
    c = _json("configs/current_candidate.json")
    assert c["candidate_id"] == CURRENT
    assert c["parent_candidate_id"] == PARENT
    assert c["base_main_sha"] == BASE
    assert c["strategy_delta"] == MECHANISM
    assert c["adopted_mechanisms"][-1] == MECHANISM
    assert all(value is False for value in c["validation"].values())


def test_guard_is_a_mode_current_story_and_low_cost_only() -> None:
    planning = _text("skills/rolling-planning/SKILL.md")
    manifest = _json("configs/runtime_manifest.json")["instruction"]

    assert "Current Story exposure guard" in planning
    assert "保持 `MODE=A`" in planning
    assert "physical / safety / workload exposure" in planning
    assert "不明显牺牲 binding Delivery、income continuity 或明确高价值 progression" in planning
    assert "与最佳成长候选价值相近" in planning
    assert "一次 choice 后即失效" in planning
    assert "不得推断未选项 hidden effect" in planning

    assert "当前 Story 若明确 physical/safety/workload exposure" in manifest
    assert "保持 A" in manifest
    assert "成本不明或 high tradeoff 不触发" in manifest


def test_no_fragile_state_or_numeric_health_gate_is_added() -> None:
    runtime = _text("skills/rolling-planning/SKILL.md") + "\n" + _json("configs/runtime_manifest.json")["instruction"]
    for forbidden in (
        "RESOURCE_STATE=",
        "FRAGILE_A_MODE",
        "Health<=2",
        "Health <= 2",
        "Health<",
        "Health <",
        "每季度一次Health",
        "S直到补满",
    ):
        assert forbidden not in runtime


def test_manifest_is_compressed_and_preserves_core_markers() -> None:
    manifest = _json("configs/runtime_manifest.json")["instruction"]
    assert len(manifest) <= 5000
    for marker in (
        "fresh observe 后旧 S 授权失效",
        "Formal Review 后重建 Portfolio",
        "Promotion Portfolio",
        "clean NO_GAIN",
        "terminal-horizon direct realization",
        "CONTROL_STATE=READY|OBSERVE_REQUIRED|BLOCKED",
        "QUARTER_INTENT=<MODE|current target>",
    ):
        assert marker in manifest


def test_board_delivery_risk_runner_and_dependencies_are_frozen() -> None:
    for path in (
        "skills/structured-state-board/SKILL.md",
        "skills/delivery-progress/SKILL.md",
        "skills/risk-review/SKILL.md",
        "career_sim_runner",
        "pyproject.toml",
        "uv.lock",
    ):
        changed = subprocess.check_output(
            ["git", "diff", "--name-only", BASE, "--", path],
            cwd=ROOT,
            text=True,
            encoding="utf-8",
        ).strip()
        assert changed == ""


def _base_text(path: str) -> str:
    return subprocess.check_output(["git", "show", f"{BASE}:{path}"], cwd=ROOT).decode("utf-8")


def test_only_one_planning_rule_is_added_and_other_sections_are_identical() -> None:
    planning = _text("skills/rolling-planning/SKILL.md")
    added = [line for line in planning.splitlines(keepends=True) if "**Current Story exposure guard：**" in line]
    assert len(added) == 1
    assert planning.replace(added[0], "", 1) == _base_text("skills/rolling-planning/SKILL.md")
    # Includes all pre-existing MODE/RECOVERY, Portfolio, NO_GAIN, Review,
    # Final Horizon, Quarterly Energy/Main and decision-budget contracts.


def test_non_kernel_runtime_instruction_and_manifest_metadata_are_identical() -> None:
    current = _json("configs/runtime_manifest.json")
    parent = json.loads(_base_text("configs/runtime_manifest.json"))
    start, end = "CRITICAL KERNEL\n", "\n\nSTARTUP AND FLOW\n"
    for manifest in (current, parent):
        assert manifest["instruction"].count(start) == manifest["instruction"].count(end) == 1
    assert current["instruction"].split(start)[0] == parent["instruction"].split(start)[0]
    assert current["instruction"].split(end)[1] == parent["instruction"].split(end)[1]
    assert {k: v for k, v in current.items() if k not in {"name", "instruction"}} == {
        k: v for k, v in parent.items() if k not in {"name", "instruction"}
    }


@pytest.mark.parametrize("scenario,clauses", [
    ("A_current_exposure_comparable_growth", ("最新 fresh public context", "physical / safety / workload exposure", "合法低暴露 option", "与最佳成长候选价值相近", "保持 `MODE=A`")),
    ("B_high_tradeoff_and_binding_delivery", ("不明显牺牲 binding Delivery", "income continuity", "job continuity", "明确高价值 progression", "high-tradeoff 选项不触发")),
    ("C_numeric_only_or_generic_fatigue_workload", ("单纯数值低", "普通疲劳/负荷")),
    ("D_prior_exposure_expired", ("仅对当前 Story/event 生效", "过去暴露/恢复", "一次 choice 后即失效", "下一 fresh observe 重新判断")),
    ("E_ambiguous_cost_or_unchosen_effect", ("成本不明", "不得推断未选项 hidden effect")),
])
def test_static_scenario_trigger_and_exclusion_clauses(scenario: str, clauses: tuple[str, ...]) -> None:
    # Checks written protocol coverage, not model execution or career outcome.
    guard = next(line for line in _text("skills/rolling-planning/SKILL.md").splitlines() if "**Current Story exposure guard：**" in line)
    assert all(clause in guard for clause in clauses), scenario


def test_compressed_kernel_retains_nonsticky_s_strength_and_local_response_scope() -> None:
    instruction = _json("configs/runtime_manifest.json")["instruction"]
    kernel = instruction.split("CRITICAL KERNEL\n")[1].split("\n\nSTARTUP AND FLOW\n")[0]
    for clause in ("仅当前 fresh public evidence", "material binding threat", "不靠旧S/旧reason续期", "同一 threat 明确 unresolved 可连续重授权", "minimum necessary stabilization", "strong default prior", "当前 Level/context path", "positive reallocation", "income/job continuity", "普通疲劳/负荷"):
        assert clause in kernel
    runtime = instruction + _text("skills/rolling-planning/SKILL.md")
    assert not re.search(r"\b(?:Health|H)\s*(?:<=|<|>=|>)\s*(?:\d|X\b)", runtime, re.I)
