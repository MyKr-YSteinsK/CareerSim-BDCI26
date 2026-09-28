"""Static identity and compact Skill-contract checks for the v7 Candidate."""

import hashlib
import json
import re
import subprocess
from pathlib import Path

from career_sim_runner.skill_contract import validate_skill_frontmatter


ROOT = Path(__file__).resolve().parents[1]
BASE_MAIN_SHA = "dc5e85cdaef136c9bc573a04c13a3e691bcf7790"
PARENT_CANDIDATE_ID = "candidate-v7f-promotion-first-survival-floor"
CURRENT_CANDIDATE_ID = "candidate-v7g-compact-skill-contracts"
SKILL_ORDER = (
    "structured-state-board",
    "rolling-planning",
    "delivery-progress",
    "risk-review",
)
EXPECTED_SKILLS = set(SKILL_ORDER)
REQUIRED_DELTA = {
    "PROFESSIONAL_SKILL_CONTRACT_REFACTOR",
    "CONCISE_IMPERATIVE_WORKFLOWS",
    "EXPLICIT_INPUT_OUTPUT_CONTRACTS",
    "REDUCED_CROSS_SKILL_DUPLICATION",
    "PRESERVED_PROMOTION_FIRST_SURVIVAL_FLOOR",
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


def _runtime_text() -> str:
    paths = [
        ROOT / f"skills/{name}/SKILL.md" for name in SKILL_ORDER
    ] + [ROOT / "configs/runtime_manifest.json"]
    return "\n".join(path.read_text(encoding="utf-8") for path in paths)


def _section(text: str, start: str, end: str) -> str:
    start_index = text.index(start)
    end_index = text.index(end, start_index + len(start))
    return text[start_index:end_index]


def test_candidate_identity_hashes_parent_manifest_and_four_skill_blobs() -> None:
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
    assert candidate["decision"] == "S07_32_STATIC_COMPACT_SKILL_CONTRACTS"
    assert candidate["strategy_delta"] == "PROFESSIONAL_SKILL_CONTRACT_REFACTOR"
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
    assert REQUIRED_DELTA <= set(candidate["adopted_mechanisms"])
    assert set(candidate["runtime_contract_delta"]) == REQUIRED_DELTA
    assert candidate["design_intent"] == "PROMOTION_FIRST_WITH_SURVIVAL_FLOOR"

    assert set(candidate["validation"]) == {
        "runtime_validated",
        "gameplay_validated",
        "provider_validated",
        "survival_improvement_proven",
        "score_improvement_proven",
        "long_horizon_adherence",
        "stable_80_plus_proven",
        "hidden_test_transfer_proven",
        "next_game_authorized",
    }
    assert all(value is False for value in candidate["validation"].values())
    assert candidate["architecture"]["skill_count"] == 4
    assert set(candidate["architecture"]["active_skills"]) == EXPECTED_SKILLS
    assert candidate["architecture"]["action_submitter"] == "Single Agent"
    assert candidate["architecture"]["memory"] == "NOT_IMPLEMENTED"
    assert candidate["architecture"]["fifth_skill"] == "DEFERRED"
    assert candidate["architecture"]["team_swarm"] == "DEFERRED"


def test_four_skill_frontmatter_describes_scope_trigger_and_ownership() -> None:
    skill_dirs = {
        child.name
        for child in (ROOT / "skills").iterdir()
        if child.is_dir() and (child / "SKILL.md").is_file()
    }
    assert skill_dirs == EXPECTED_SKILLS

    for name in EXPECTED_SKILLS:
        path = ROOT / "skills" / name / "SKILL.md"
        content = path.read_text(encoding="utf-8")
        assert validate_skill_frontmatter(path.parent) == []
        frontmatter = content.split("---", 2)[1]
        match = re.search(r'^description:\s*"(.+)"\s*$', frontmatter, re.MULTILINE)
        assert match is not None
        description = match.group(1)
        assert description.lower().startswith("use ")
        assert len(description) > 80
        assert re.search(r"\b(?:after|during|every|when|before)\b", description, re.IGNORECASE)
        assert re.search(r"\b(?:normalize|maintain|track|pass|rank|submit)\b", description, re.IGNORECASE)

    board = (ROOT / "skills/structured-state-board/SKILL.md").read_text(encoding="utf-8")
    planning = (ROOT / "skills/rolling-planning/SKILL.md").read_text(encoding="utf-8")
    delivery = (ROOT / "skills/delivery-progress/SKILL.md").read_text(encoding="utf-8")
    risk = (ROOT / "skills/risk-review/SKILL.md").read_text(encoding="utf-8")
    manifest = _load_json(ROOT / "configs/runtime_manifest.json")["instruction"]

    assert "Facts only" in board
    assert "objective" in planning.lower() and "candidate" in planning.lower()
    assert "Planning owns objective" in delivery and "Delivery owns only lifecycle state" in delivery
    assert "Risk owns final candidate risk review" in delivery
    assert "Risk does not own the Review Plan or candidate ranking" in risk
    assert "Single Agent is the only action submitter" in manifest
    for owner in (
        "structured-state-board=facts",
        "rolling-planning=strategy",
        "delivery-progress=current-session delivery lifecycle",
        "risk-review=final candidate risk gate",
    ):
        assert owner in manifest


def test_promotion_first_advance_and_temporary_survival_floor_remain() -> None:
    planning = (ROOT / "skills/rolling-planning/SKILL.md").read_text(encoding="utf-8")
    manifest = _load_json(ROOT / "configs/runtime_manifest.json")["instruction"]
    combined = planning + "\n" + manifest

    assert "Maximize long-horizon progression" in planning
    assert "`A` = Advance. Default." in planning
    assert "Promotion-first with Survival Floor" in manifest
    assert "switch to temporary stabilization" in planning.lower()
    assert "return to `A`" in planning
    assert "permanent low-profile play" in planning
    assert "MODE=A" in combined and "MODE=S" in combined


def test_wealth_stress_keeps_income_and_progression_recovery_active() -> None:
    planning = (ROOT / "skills/rolling-planning/SKILL.md").read_text(encoding="utf-8")
    wealth = _section(planning, "Wealth stress is an income-recovery problem", "## Rank legal candidates")
    assert "avoid discretionary cost" in wealth.lower()
    assert "repair performance, promotion, and income capacity" in wealth
    assert "not a reason for permanent low-profile play" in wealth


def test_failure_directions_are_not_converted_to_exact_triggers() -> None:
    runtime = _runtime_text()
    forbidden = (
        r"two\s+consecutive\s+D.{0,40}(?:dismiss|fire|eliminat)",
        r"second\s+(?:blowup|incident).{0,40}(?:trust crisis|eliminat)",
        r"(?:Health|Wealth|Network|Dignity).{0,20}(?:<=|<|≤)\s*\d+.{0,35}(?:fail|dismiss|eliminat)",
        r"连续\s*(?:两|\d+)\s*次.{0,35}(?:解雇|出局|信任危机)",
        r"第二次.{0,15}爆雷.{0,30}(?:信任危机|出局)",
        r"(?:健康|财富|人脉|尊严).{0,15}(?:<=|<|≤)\s*\d+.{0,30}(?:失败|出局)",
    )
    assert not any(re.search(pattern, runtime, re.IGNORECASE) for pattern in forbidden)
    assert "Do not infer thresholds, counters" in runtime
    assert "Do not invent numeric thresholds, hidden counts" in runtime


def test_public_hint_and_no_gain_do_not_create_hidden_rules() -> None:
    planning = (ROOT / "skills/rolling-planning/SKILL.md").read_text(encoding="utf-8")
    assert "soft evidence only" in planning
    assert "OBSERVED_NO_GAIN" in planning and "UNKNOWN" in planning
    assert "Do not infer a cap or formula" in planning
    assert "hidden threshold/cap" in planning


def test_story_and_energy_have_no_fixed_answer_or_bundle() -> None:
    planning = (ROOT / "skills/rolling-planning/SKILL.md").read_text(encoding="utf-8")
    manifest = _load_json(ROOT / "configs/runtime_manifest.json")["instruction"]
    combined = planning + "\n" + manifest
    story = _section(planning, "## Story stop rule", "## Quarterly control")
    energy = _section(planning, "## Quarterly control", "## Output")

    assert "Stop when one candidate is clearly preferred" in story
    assert "Do not use hidden/private/Dev-only evidence" in manifest
    assert "event-to-answer lookup" in manifest
    assert "not a fixed menu answer" in combined.lower()
    assert "a fixed optimal action" in planning.lower()
    assert "QUARTER_INTENT" in energy
    assert "exactly one integer choice per action" in manifest
    assert not re.search(r"(?:fixed|standard)\s+Energy\s+bundle", combined, re.IGNORECASE)


def test_risk_gates_candidates_without_replanning() -> None:
    risk = (ROOT / "skills/risk-review/SKILL.md").read_text(encoding="utf-8")
    assert "Planning's final legal candidate" in risk
    assert "Never re-plan the whole decision" in risk
    assert "Risk does not own the Review Plan or candidate ranking" in risk
    assert "Compare at most that alternative" in risk


def test_manifest_retains_action_preflight_and_same_session_recovery() -> None:
    manifest = _load_json(ROOT / "configs/runtime_manifest.json")["instruction"]
    assert "Before take_action verify" in manifest
    assert "choice is exactly one legal integer" in manifest
    assert "confirmed current session_id" in manifest
    assert "exactly one [CTRL" in manifest
    recovery = manifest[manifest.index("On context recovery:"):]
    for marker in ("confirm same game_session_id", "fresh observe", "reread all four Skills"):
        assert marker in recovery


def test_candidate_and_state_record_compact_refactor_without_validation_transfer() -> None:
    candidate = _load_json(ROOT / "configs/current_candidate.json")
    state = (ROOT / "docs/project/CURRENT_STATE.md").read_text(encoding="utf-8")
    decisions = (ROOT / "docs/project/ARCHITECTURE_DECISIONS.md").read_text(encoding="utf-8")

    assert candidate["parent_candidate_id"] == PARENT_CANDIDATE_ID
    assert "S07-32" in state and CURRENT_CANDIDATE_ID in state
    assert re.search(r"Current Candidate:\s+`candidate-v7g-compact-skill-contracts`", state)
    assert "all v7g validation flags are false" in state
    assert "## AD-016" in decisions and "S07-32" in decisions
    assert "PROMOTION_FIRST_WITH_SURVIVAL_FLOOR" in decisions
    assert "NEXT_GAME = NOT_AUTHORIZED" in state
    assert "NEXT_GAME = NOT_AUTHORIZED" in decisions
