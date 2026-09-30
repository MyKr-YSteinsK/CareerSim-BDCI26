"""S09-03 static regression: fresh binding evidence must reauthorize every S decision."""

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "74e856c5be7a9a134f93e9876ffbfd14398199ab"
CURRENT = "candidate-v7x-fresh-binding-reauthorization"
PARENT = "candidate-v7w-high-score-core-recovery"
MECHANISM = "FRESH_BINDING_BASIS_REQUIRED_FOR_EACH_STABILIZATION_DECISION"
V7X_STATIC = "43258d41a02ac65c9f1e5d0367ca7612a36c7da7"


def _text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def _json(path: str) -> dict:
    return json.loads(_text(path))


def _v7x_json(path: str) -> dict:
    # S09-03 static facts precede v7x gameplay and the v7y descendant.
    return json.loads(subprocess.check_output(["git", "show", f"{V7X_STATIC}:{path}"], cwd=ROOT))


def test_v7x_identity_and_validation_reset() -> None:
    candidate = _v7x_json("configs/current_candidate.json")
    assert candidate["candidate_id"] == CURRENT
    assert candidate["parent_candidate_id"] == PARENT
    assert candidate["base_main_sha"] == BASE
    assert candidate["strategy_delta"] == MECHANISM
    assert candidate["adopted_mechanisms"][-1] == MECHANISM
    assert all(value is False for value in candidate["validation"].values())


def test_nonsticky_s_reauthorization_is_explicit_but_not_forced_one_turn_exit() -> None:
    planning = _text("skills/rolling-planning/SKILL.md")
    manifest = _json("configs/runtime_manifest.json")["instruction"]

    for text in (planning, manifest):
        assert "fresh observe" in text
        assert "旧" in text and "S" in text and "授权" in text
        assert "重新授权" in text or "重授权" in text
        assert "unresolved" in text
    assert "上一次 `MODE=S` 授权自动失效" in planning
    assert "本轮从 `MODE=A` 重新判断" in planning
    assert "可以连续重授权 `S`" in planning
    assert "这不是强制单回合退出" in planning
    assert "不靠旧S/旧reason续期" in manifest
    assert "同一 threat 明确 unresolved 可连续重授权" in manifest


def test_strategy_control_surfaces_other_than_planning_are_frozen() -> None:
    for path in (
        "skills/structured-state-board/SKILL.md",
        "skills/delivery-progress/SKILL.md",
        "skills/risk-review/SKILL.md",
        "pyproject.toml",
        "uv.lock",
        "career_sim_runner",
    ):
        changed = subprocess.check_output(
            ["git", "diff", "--name-only", BASE, "--", path],
            cwd=ROOT,
            text=True,
            encoding="utf-8",
        ).strip()
        assert changed == ""


def test_manifest_delta_is_name_plus_critical_kernel_only() -> None:
    current = _v7x_json("configs/runtime_manifest.json")
    parent = json.loads(
        subprocess.check_output(["git", "show", f"{BASE}:configs/runtime_manifest.json"], cwd=ROOT)
    )
    assert current["name"] == CURRENT
    assert parent["name"] == PARENT
    assert current["team"] == parent["team"]
    assert current["mode"] == parent["mode"]
    assert len(current["instruction"]) <= 5200

    start = "CRITICAL KERNEL\n"
    end = "\n\nSTARTUP AND FLOW\n"
    cur_prefix, cur_tail = current["instruction"].split(start, 1)
    par_prefix, par_tail = parent["instruction"].split(start, 1)
    cur_kernel, cur_suffix = cur_tail.split(end, 1)
    par_kernel, par_suffix = par_tail.split(end, 1)

    assert cur_prefix == par_prefix
    assert cur_suffix == par_suffix
    assert cur_kernel != par_kernel
    assert "MODE=A 使用 Promotion Portfolio" in cur_kernel
    assert "clean NO_GAIN/non-responsive path" in cur_kernel
    assert "terminal-horizon direct realization" in cur_kernel


def test_no_empirical_shock_value_is_promoted_to_runtime_threshold() -> None:
    runtime = _text("skills/rolling-planning/SKILL.md") + "\n" + _json("configs/runtime_manifest.json")["instruction"]
    for forbidden in (
        "Health<=2",
        "Health <= 2",
        "Wealth<=4",
        "Wealth <= 4",
        "H<=2",
        "W<=4",
        "observed max =",
    ):
        assert forbidden not in runtime
