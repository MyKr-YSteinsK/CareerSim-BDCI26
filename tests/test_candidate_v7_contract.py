"""Static identity and ownership contract for the current formal Candidate."""

import hashlib
import json
import subprocess
from pathlib import Path

from career_sim_runner.skill_contract import validate_skill_frontmatter


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_SKILLS = {
    "structured-state-board",
    "rolling-planning",
    "delivery-progress",
    "risk-review",
}


def _git_blob_id(path: Path) -> str:
    relative_path = path.relative_to(ROOT).as_posix()
    return subprocess.check_output(
        ["git", "hash-object", f"--path={relative_path}", str(path)],
        cwd=ROOT,
        text=True,
    ).strip()


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_candidate_identity_matches_manifest_and_exact_skill_blobs() -> None:
    candidate = _load_json(ROOT / "configs/current_candidate.json")
    manifest_path = ROOT / "configs/runtime_manifest.json"
    manifest_bytes = subprocess.check_output(
        ["git", "show", ":configs/runtime_manifest.json"], cwd=ROOT
    )
    manifest = _load_json(manifest_path)

    assert candidate["candidate_id"] == "candidate-v7-global-trajectory-delivery"
    assert candidate["parent_candidate_id"] == "candidate-v6c-compliance-cleanup"
    assert candidate["status"] == "STATIC_IMPLEMENTED_NOT_RUNTIME_VALIDATED"
    assert manifest["name"] == candidate["candidate_id"]
    assert manifest["mode"] == "agent"
    assert candidate["runtime_manifest"]["path"] == "configs/runtime_manifest.json"
    assert candidate["runtime_manifest"]["sha256"] == hashlib.sha256(manifest_bytes).hexdigest()
    assert candidate["runtime_manifest"]["instruction_sha256"] == hashlib.sha256(
        manifest["instruction"].encode("utf-8")
    ).hexdigest()

    skill_entries = candidate["skills"]
    assert len(skill_entries) == 4
    assert {entry["name"] for entry in skill_entries} == EXPECTED_SKILLS
    for entry in skill_entries:
        path = ROOT / entry["path"]
        assert entry["path"] == f"skills/{entry['name']}/SKILL.md"
        assert entry["git_blob"] == _git_blob_id(path)

    actual_skill_dirs = {
        child.name for child in (ROOT / "skills").iterdir() if child.is_dir() and (child / "SKILL.md").is_file()
    }
    assert actual_skill_dirs == EXPECTED_SKILLS
    architecture = candidate["architecture"]
    assert architecture["skill_count"] == 4
    assert set(architecture["active_skills"]) == EXPECTED_SKILLS
    assert architecture["action_submitter"] == "Single Agent"
    assert architecture["memory"] == "NOT_IMPLEMENTED"
    assert architecture["fifth_skill"] == "DEFERRED"
    assert architecture["team_swarm"] == "DEFERRED"
    assert all(value is False for value in candidate["validation"].values())


def test_four_skill_frontmatter_and_single_action_authority() -> None:
    board = (ROOT / "skills/structured-state-board/SKILL.md").read_text(encoding="utf-8")
    planning = (ROOT / "skills/rolling-planning/SKILL.md").read_text(encoding="utf-8")
    delivery = (ROOT / "skills/delivery-progress/SKILL.md").read_text(encoding="utf-8")
    risk = (ROOT / "skills/risk-review/SKILL.md").read_text(encoding="utf-8")

    for name in sorted(EXPECTED_SKILLS):
        skill_dir = ROOT / "skills" / name
        assert validate_skill_frontmatter(skill_dir) == []
        content = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
        assert "Can Submit Action: No" in content

    assert "delivery lifecycle" in board and "Board 不拥有" in board
    assert "唯一战略 owner" in planning and "不创建、覆盖或补全 Delivery 状态" in planning
    assert "Planning 是唯一 strategy owner" in delivery and "Delivery 不选 Primary Gap" in delivery
    assert "单纯未交付、延期、没有回执或 UNKNOWN 本身不构成 Risk trigger" in risk


def test_manifest_orders_delivery_before_planning_and_recovers_all_four_skills() -> None:
    manifest = _load_json(ROOT / "configs/runtime_manifest.json")
    instruction = manifest["instruction"]
    flow = instruction.split("每次决策顺序：", 1)[1].splitlines()[0]
    markers = [
        "fresh observe",
        "Board",
        "Delivery",
        "Planning",
        "legal candidate",
        "Risk",
        "DECISION_CLOSED",
        "take_action",
        "fresh observe",
    ]
    positions = []
    cursor = 0
    for marker in markers:
        position = flow.index(marker, cursor)
        positions.append(position)
        cursor = position + len(marker)
    assert positions == sorted(positions)

    recovery = instruction.split("Compression/recovery epoch", 1)[1]
    for skill in sorted(EXPECTED_SKILLS):
        assert skill in recovery
    assert "当前 session" in recovery
    assert "UNKNOWN" in recovery
    assert "换候选仍须过 gate 但 R 不变" in instruction
    assert "未触发 RECONSIDER 时 R=最终普通 gate 且 X=-" in instruction
