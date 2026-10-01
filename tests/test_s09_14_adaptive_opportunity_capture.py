"""S09-14 static checks for the bounded untested opportunity probe."""

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARENT = "a2bf214b6f4c6923399f80ada03b4d61d97f6eaa"
ID = "candidate-v9a-adaptive-opportunity-capture"


def text(path):
    return (ROOT / path).read_text(encoding="utf-8")


def source(path):
    return subprocess.check_output(["git", "show", f"{PARENT}:{path}"], cwd=ROOT).decode("utf-8")


def test_identity_is_a_v8a_child_and_runtime_instruction_is_unchanged():
    now = json.loads(text("configs/current_candidate.json"))
    parent = json.loads(source("configs/current_candidate.json"))
    manifest = json.loads(text("configs/runtime_manifest.json"))
    parent_manifest = json.loads(source("configs/runtime_manifest.json"))
    assert now["candidate_id"] == manifest["name"] == ID
    assert now["parent_candidate_id"] == parent["candidate_id"]
    assert now["base_main_sha"] == PARENT
    assert now["parent_identity"]["skills"] == parent["skills"]
    assert manifest["instruction"] == parent_manifest["instruction"]
    assert now["validation"] and not any(now["validation"].values())


def test_only_planning_changes_among_the_four_skills():
    changed = set(
        subprocess.check_output(
            ["git", "diff", "--name-only", PARENT, "HEAD", "--", "skills"],
            cwd=ROOT,
            text=True,
        ).splitlines()
    )
    assert changed == {"skills/rolling-planning/SKILL.md"}


def test_probe_is_optional_local_and_bounded():
    planning = text("skills/rolling-planning/SKILL.md")
    required = (
        "fresh clean NO_GAIN",
        "已知 responsive alternative",
        "尚未测试、但从公开语义看有明确成长价值",
        "最多两个候选",
        "可选 probe",
        "不是为了“覆盖率”强制探索",
        "只执行一次",
        "随后 fresh observe",
        "不自动连续 probe",
        "不把 UNKNOWN 当 GAIN",
        "当前 Level/context/family 的局部证据",
    )
    assert all(item in planning for item in required)


def test_known_response_and_binding_constraints_still_win_first():
    planning = text("skills/rolling-planning/SKILL.md")
    assert "先找当前 Level/context 下已经有响应" in planning
    assert "生存/合规/信任约束和 near-term Delivery 始终优先" in planning
    assert "存在 responsive alternative 时不立即重复同一路径" in planning


def test_existing_safety_and_no_gain_boundaries_are_preserved():
    planning = text("skills/rolling-planning/SKILL.md")
    for clause in (
        "minimum necessary protection",
        "旧 S/旧理由不续期",
        "不把局部 NO_GAIN 传播给未测试 family",
        "不推断全局 cap、eligibility",
        "Level change 后依 Board 重置",
        "ONE FRESH OBSERVE = ONE PLANNING PASS",
        "Can Submit Action: No",
    ):
        assert clause in planning


def test_no_exploration_quota_or_new_mode_is_introduced():
    planning = text("skills/rolling-planning/SKILL.md")
    for forbidden in ("exploration budget", "探索配额", "探索次数配额", "MODE=E", "EXPLORE_MODE"):
        assert forbidden not in planning
    assert len(planning) < len(source("skills/rolling-planning/SKILL.md")) + 1200
