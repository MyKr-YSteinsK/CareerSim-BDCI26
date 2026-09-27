"""Static identity and ownership contract for the current formal Candidate."""

import hashlib
import json
import re
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


def _load_json_from_bytes(content: bytes) -> dict:
    return json.loads(content.decode("utf-8"))


def test_candidate_identity_matches_manifest_and_exact_skill_blobs() -> None:
    candidate = _load_json(ROOT / "configs/current_candidate.json")
    manifest_path = ROOT / "configs/runtime_manifest.json"
    manifest_bytes = subprocess.check_output(
        ["git", "show", ":configs/runtime_manifest.json"], cwd=ROOT
    )
    manifest = _load_json(manifest_path)

    assert candidate["candidate_id"] == "candidate-v7a-promotion-frontier"
    assert candidate["parent_candidate_id"] == "candidate-v7-global-trajectory-delivery"
    assert candidate["status"] == "STATIC_IMPLEMENTED_NOT_RUNTIME_VALIDATED"
    assert candidate["base_main_sha"] == "21b5153b86a0b7e7ce2c31278620202b6739c536"
    assert manifest["name"] == candidate["candidate_id"]
    assert manifest["mode"] == "agent"
    assert candidate["runtime_manifest"]["path"] == "configs/runtime_manifest.json"
    assert candidate["runtime_manifest"]["sha256"] == hashlib.sha256(manifest_bytes).hexdigest()
    assert candidate["runtime_manifest"]["instruction_sha256"] == hashlib.sha256(
        manifest["instruction"].encode("utf-8")
    ).hexdigest()

    parent_manifest_bytes = subprocess.check_output(
        ["git", "show", f"{candidate['base_main_sha']}:configs/runtime_manifest.json"], cwd=ROOT
    )
    parent_manifest = _load_json_from_bytes(parent_manifest_bytes)
    parent_candidate_bytes = subprocess.check_output(
        ["git", "show", f"{candidate['base_main_sha']}:configs/current_candidate.json"], cwd=ROOT
    )
    parent_candidate = _load_json_from_bytes(parent_candidate_bytes)
    assert candidate["parent_identity"] == {
        "runtime_manifest_sha256": hashlib.sha256(parent_manifest_bytes).hexdigest(),
        "instruction_sha256": hashlib.sha256(parent_manifest["instruction"].encode("utf-8")).hexdigest(),
        "skills": [
            {"name": entry["name"], "git_blob": entry["git_blob"]}
            for entry in parent_candidate["skills"]
        ],
    }

    skill_entries = candidate["skills"]
    assert len(skill_entries) == 4
    assert {entry["name"] for entry in skill_entries} == EXPECTED_SKILLS
    parent_skill_ids = {
        entry["name"]: entry["git_blob"] for entry in candidate["parent_identity"]["skills"]
    }
    current_skill_ids = {entry["name"]: entry["git_blob"] for entry in skill_entries}
    for entry in skill_entries:
        path = ROOT / entry["path"]
        assert entry["path"] == f"skills/{entry['name']}/SKILL.md"
        assert entry["git_blob"] == _git_blob_id(path)
    for name in EXPECTED_SKILLS - {"rolling-planning"}:
        assert current_skill_ids[name] == parent_skill_ids[name]
    assert current_skill_ids["rolling-planning"] != parent_skill_ids["rolling-planning"]

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
    assert {
        "PUBLIC_PROMOTION_FRONTIER_DIAGNOSIS",
        "CROSS_DIMENSION_PROGRESSION_BOTTLENECK",
        "GLOBAL_MARGINAL_VALUE_AWARENESS",
        "EARLY_HORIZON_PROGRESSION_BIAS",
        "EXPLICIT_PUBLIC_AFFORDABILITY_CONSTRAINT",
    } <= set(candidate["adopted_mechanisms"])


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


def test_promotion_frontier_is_qualitative_and_free_of_threshold_mappings() -> None:
    candidate = _load_json(ROOT / "configs/current_candidate.json")
    manifest = _load_json(ROOT / "configs/runtime_manifest.json")
    planning = (ROOT / "skills/rolling-planning/SKILL.md").read_text(encoding="utf-8")
    deployable_policy = planning + "\n" + manifest["instruction"]
    audited_surface = deployable_policy + "\n" + json.dumps(candidate, ensure_ascii=False)

    for phrase in (
        "Promotion Frontier / Progression Readiness",
        "定性诊断",
        "不得估算 promotion probability",
        "不作为持久 enum 或 telemetry",
        "两个相邻 comparable checkpoints",
        "Risk Budget=AVAILABLE",
        "binding compliance constraint",
        "inability to pay",
        "不设 Wealth cutoff",
    ):
        assert phrase in deployable_policy

    assert manifest["name"] == candidate["candidate_id"]
    assert "fixed promotion month" in manifest["instruction"]
    assert "fixed action ratio/Energy bundle" in manifest["instruction"]
    assert "event/title/keyword/choice lookup" in manifest["instruction"]
    assert "exact promotion threshold" not in deployable_policy.lower()
    assert "USER_PROVIDED_UNVERIFIED_EXTERNAL_MECHANISM_SIGNAL" not in audited_surface
    forbidden_patterns = (
        r"\b[SON]\s*(?:>=|<=|≥|≤|=|>|<)\s*\d+",
        r"(?:^|\n)\s*(?:L|Level)\s*\d+\s*(?:→|:|=)\s*[SON]\s*(?:>=|<=|≥|≤|=)\s*\d+",
        r"\b(?:cap|封顶)\s*(?:=|:|≥|<=|>=)\s*\d+",
        r"\bM\d{1,2}\s*(?:must|必须)\s*(?:reach|达到|L\d)",
    )
    for pattern in forbidden_patterns:
        assert re.search(pattern, audited_surface, flags=re.IGNORECASE) is None
