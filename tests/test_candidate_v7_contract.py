"""Static identity, ownership, and v7e lean review controller contract."""

import hashlib
import json
import re
import subprocess
from pathlib import Path

from career_sim_runner.skill_contract import validate_skill_frontmatter


ROOT = Path(__file__).resolve().parents[1]
BASE_MAIN_SHA = "786db94f6683fd0c11aa6eae85ca11a95a1e032a"
PARENT_CANDIDATE_ID = "candidate-v7d-strategic-continuity"
CURRENT_CANDIDATE_ID = "candidate-v7e-lean-review-controller"
SKILL_ORDER = (
    "structured-state-board",
    "rolling-planning",
    "delivery-progress",
    "risk-review",
)
EXPECTED_SKILLS = set(SKILL_ORDER)
V7E_MECHANISMS = {
    "FORMAL_REVIEW_ANCHORED_PLAN",
    "ORDINARY_STORY_GAP_STABILITY",
    "BINDING_AFFORDABILITY_GUARD",
    "PUBLIC_HINT_SOFT_EVIDENCE_ONLY",
    "NO_HIDDEN_CAP_INFERENCE_FROM_NO_GAIN",
    "ONE_PASS_BOUNDED_DELIBERATION",
    "QUARTER_ENERGY_INTENT_PERSISTENCE",
}


def _git_blob_id(path: Path) -> str:
    relative_path = path.relative_to(ROOT).as_posix()
    return subprocess.check_output(
        ["git", "hash-object", f"--path={relative_path}", str(path)],
        cwd=ROOT,
        text=True,
    ).strip()


def _git_bytes(revision: str, path: str) -> bytes:
    return subprocess.check_output(["git", "show", f"{revision}:{path}"], cwd=ROOT)


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _skill_blobs_at(revision: str) -> list[dict]:
    return [
        {
            "name": name,
            "git_blob": subprocess.check_output(
                ["git", "rev-parse", f"{revision}:skills/{name}/SKILL.md"],
                cwd=ROOT,
                text=True,
            ).strip(),
            "path": f"skills/{name}/SKILL.md",
        }
        for name in SKILL_ORDER
    ]


def _canonical_text_bytes(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n")


def test_candidate_identity_hashes_parent_and_four_skill_blobs() -> None:
    candidate = _load_json(ROOT / "configs/current_candidate.json")
    manifest_path = ROOT / "configs/runtime_manifest.json"
    manifest = _load_json(manifest_path)
    manifest_bytes = _canonical_text_bytes(manifest_path)
    parent_manifest_bytes = _git_bytes(BASE_MAIN_SHA, "configs/runtime_manifest.json")
    parent_manifest = json.loads(parent_manifest_bytes.decode("utf-8"))
    parent_candidate = json.loads(_git_bytes(BASE_MAIN_SHA, "configs/current_candidate.json"))
    parent_skills = _skill_blobs_at(BASE_MAIN_SHA)

    assert candidate["candidate_id"] == CURRENT_CANDIDATE_ID
    assert candidate["parent_candidate_id"] == PARENT_CANDIDATE_ID
    assert candidate["status"] == "STATIC_IMPLEMENTED_NOT_RUNTIME_VALIDATED"
    assert candidate["decision"] == "S07_30_STATIC_LEAN_REVIEW_CONTROLLER"
    assert candidate["base_main_sha"] == BASE_MAIN_SHA
    assert manifest["name"] == CURRENT_CANDIDATE_ID and manifest["mode"] == "agent"
    assert candidate["runtime_manifest"]["path"] == "configs/runtime_manifest.json"
    assert candidate["runtime_manifest"]["sha256"] == hashlib.sha256(manifest_bytes).hexdigest()
    assert candidate["runtime_manifest"]["instruction_sha256"] == hashlib.sha256(
        manifest["instruction"].encode("utf-8")
    ).hexdigest()

    assert parent_candidate["candidate_id"] == PARENT_CANDIDATE_ID
    assert parent_manifest["name"] == PARENT_CANDIDATE_ID
    assert candidate["parent_identity"] == {
        "runtime_manifest_sha256": parent_candidate["runtime_manifest"]["sha256"],
        "instruction_sha256": parent_candidate["runtime_manifest"]["instruction_sha256"],
        "skills": parent_skills,
    }
    assert candidate["parent_identity"]["runtime_manifest_sha256"] == hashlib.sha256(
        parent_manifest_bytes
    ).hexdigest()

    entries = candidate["skills"]
    assert {entry["name"] for entry in entries} == EXPECTED_SKILLS
    assert len(entries) == 4
    assert {entry["git_blob"] for entry in entries} == {
        _git_blob_id(ROOT / entry["path"]) for entry in entries
    }
    parent_map = {entry["name"]: entry["git_blob"] for entry in parent_skills}
    current_map = {entry["name"]: entry["git_blob"] for entry in entries}
    for unchanged in ("structured-state-board", "delivery-progress", "risk-review"):
        assert current_map[unchanged] == parent_map[unchanged]
    assert current_map["rolling-planning"] != parent_map["rolling-planning"]

    assert all(value is False for value in candidate["validation"].values())
    assert candidate["architecture"]["skill_count"] == 4
    assert set(candidate["architecture"]["active_skills"]) == EXPECTED_SKILLS
    assert candidate["architecture"]["action_submitter"] == "Single Agent"
    assert candidate["architecture"]["memory"] == "NOT_IMPLEMENTED"
    assert candidate["architecture"]["fifth_skill"] == "DEFERRED"
    assert candidate["architecture"]["team_swarm"] == "DEFERRED"
    assert V7E_MECHANISMS <= set(candidate["adopted_mechanisms"])
    assert "PUBLIC_HINT_AS_CONFIRMED_HARD_RULE" in candidate["rejected_mechanisms"]
    assert "HIDDEN_CAP_INFERENCE_FROM_NO_GAIN" in candidate["rejected_mechanisms"]


def test_four_skills_frontmatter_and_ownership_boundaries() -> None:
    board = (ROOT / "skills/structured-state-board/SKILL.md").read_text(encoding="utf-8")
    planning = (ROOT / "skills/rolling-planning/SKILL.md").read_text(encoding="utf-8")
    delivery = (ROOT / "skills/delivery-progress/SKILL.md").read_text(encoding="utf-8")
    risk = (ROOT / "skills/risk-review/SKILL.md").read_text(encoding="utf-8")

    skill_dirs = {
        child.name
        for child in (ROOT / "skills").iterdir()
        if child.is_dir() and (child / "SKILL.md").is_file()
    }
    assert skill_dirs == EXPECTED_SKILLS
    for name in EXPECTED_SKILLS:
        path = ROOT / "skills" / name
        assert validate_skill_frontmatter(path) == []
        assert "Can Submit Action: No" in (path / "SKILL.md").read_text(encoding="utf-8")

    assert "CurrentLevelDuration" in board and "duration_in_level" in board
    assert "strategy owner" in planning.lower()
    ownership_lines = [
        line for line in planning.splitlines()
        if "Planning" in line and "create / overwrite / complete" in line and "Delivery state" in line
    ]
    assert len(ownership_lines) == 1
    assert "Active Review Plan" not in board + delivery + risk
    assert "lifecycle" in delivery.lower()
    assert "candidate-specific" in risk.lower() and "material risk" in risk.lower()


def test_manifest_preserves_single_agent_control_order_and_recovery() -> None:
    candidate = _load_json(ROOT / "configs/current_candidate.json")
    instruction = _load_json(ROOT / "configs/runtime_manifest.json")["instruction"]

    positions = [instruction.index(name) for name in SKILL_ORDER]
    assert positions == sorted(positions)

    legal_candidate = instruction.index("legal candidate")
    flow_start = instruction.rfind("fresh observe", 0, legal_candidate)
    flow = instruction[flow_start:]
    controller_order = (
        "fresh observe",
        "Board",
        "Delivery",
        "Planning",
        "legal candidate",
        "Risk gate",
        "DECISION_CLOSED",
        "take_action",
        "fresh observe",
    )
    cursor = 0
    for item in controller_order:
        cursor = flow.index(item, cursor) + len(item)

    assert "participant-visible public facts" in instruction
    assert "state-changing action" in instruction and "fresh observe" in instruction
    assert "one integer" in instruction or "一个整数" in instruction
    assert "Active Review Plan" in instruction
    assert "Primary Gap" in instruction
    assert "ordinary Story" in instruction or "Story" in instruction
    assert "game_session_id" in instruction and "recovery" in instruction.lower()
    assert "UNKNOWN" in instruction and "fresh observe" in instruction
    for marker in (
        "hidden score weights/thresholds/caps",
        "event/title/keyword/choice lookup",
        "fixed promotion month/phase",
        "cross-game Memory",
        "Team/Swarm",
        "fifth Skill",
    ):
        assert marker in instruction
    assert candidate["architecture"]["action_submitter"] == "Single Agent"


def test_v7e_anchors_review_protects_affordability_and_limits_story_reasoning() -> None:
    planning = (ROOT / "skills/rolling-planning/SKILL.md").read_text(encoding="utf-8")
    manifest = _load_json(ROOT / "configs/runtime_manifest.json")["instruction"]
    combined = planning + "\n" + manifest

    for marker in ("Review Objective", "Primary Gap", "Next Observable Checkpoint", "formal review / promotion / no-advance"):
        assert marker.lower() in combined.lower()
    assert any("Story" in line and "Primary Gap" in line for line in planning.splitlines())

    for marker in ("Wealth", "affordability warning", "affordability", "binding", "job continuity"):
        assert marker.lower() in planning.lower()
    assert "\u975e\u6b63" in planning

    for marker in ("public hint", "simulator hard rule", "confirmed hard indicator"):
        assert marker.lower() in planning.lower()
    for marker in ("OBSERVED_NO_GAIN", "hidden cap", "hidden threshold", "UNKNOWN"):
        assert marker.lower() in planning.lower()
    assert "\u539f\u56e0\u4fdd\u6301" in planning

    assert "bounded deliberation" in planning.lower()
    assert "top 2" in planning
    assert "reconsider" in manifest.lower() and "fresh evidence" in manifest.lower()
    assert "Risk gate" in manifest
    assert "Energy intent" in planning
    assert "material change" in planning
    assert "one integer" in manifest or "一个整数" in manifest


def test_candidate_rejects_hidden_rules_and_unbounded_policy_expansion() -> None:
    candidate = _load_json(ROOT / "configs/current_candidate.json")
    planning = (ROOT / "skills/rolling-planning/SKILL.md").read_text(encoding="utf-8")
    manifest = _load_json(ROOT / "configs/runtime_manifest.json")["instruction"]
    decisions = (ROOT / "docs/project/ARCHITECTURE_DECISIONS.md").read_text(encoding="utf-8")

    for rejected in (
        "EXACT_DEV_SCORE_WEIGHTS_IN_RUNTIME",
        "EXACT_PROMOTION_THRESHOLD_OR_CAP_MAPPING",
        "EVENT_ID_OR_TITLE_TO_CHOICE_LOOKUP",
        "FIXED_PROMOTION_MONTH",
        "FIXED_PLAN_DURATION",
        "PUBLIC_HINT_AS_CONFIRMED_HARD_RULE",
        "HIDDEN_CAP_INFERENCE_FROM_NO_GAIN",
        "UNBOUNDED_STORY_RECONSIDERATION",
        "ENERGY_REPLAN_WITHOUT_MATERIAL_CHANGE",
    ):
        assert rejected in candidate["rejected_mechanisms"]
    for marker in ("Memory=NOT_IMPLEMENTED", "Team/Swarm", "fifth Skill=DEFERRED"):
        assert marker in manifest
    assert all(value is False for value in candidate["validation"].values())
    assert candidate["validation"]["next_game_authorized"] is False
    assert not re.search(r"\b(?:TODO|FIXME)\b", planning + manifest + decisions, re.I)


def test_s07_30_governance_records_v7e_as_the_only_current_identity() -> None:
    candidate = _load_json(ROOT / "configs/current_candidate.json")
    state = (ROOT / "docs/project/CURRENT_STATE.md").read_text(encoding="utf-8")
    decisions = (ROOT / "docs/project/ARCHITECTURE_DECISIONS.md").read_text(encoding="utf-8")

    assert candidate["candidate_id"] == CURRENT_CANDIDATE_ID
    assert "S07-30" in state and CURRENT_CANDIDATE_ID in state
    assert re.search(r"Current Candidate:\s+\x60candidate-v7e-lean-review-controller", state)
    assert not re.search(r"Current Candidate:\s+\x60candidate-v7d", state)
    assert "## AD-014" in decisions and "S07-30" in decisions
    for marker in (
        "formal review",
        "affordability",
        "public hint",
        "hidden cap",
        "top two",
        "Energy intent",
        "NEXT_GAME = NOT_AUTHORIZED",
    ):
        assert marker.lower() in decisions.lower()
    assert "S07 remains ACTIVE" in state
    assert "NEXT_GAME = NOT_AUTHORIZED" in state
