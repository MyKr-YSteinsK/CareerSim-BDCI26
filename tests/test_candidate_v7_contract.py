"""Static identity and correctness-contract checks for the current v7 Candidate."""

import hashlib
import json
import re
import subprocess
from pathlib import Path

from career_sim_runner.skill_contract import validate_skill_frontmatter


ROOT = Path(__file__).resolve().parents[1]
BASE_MAIN_SHA = "17af11d737f8d686e5d1212396234cbb064b2fcd"
PARENT_CANDIDATE_ID = "candidate-v7l-pre-game-contract-hardening"
CURRENT_CANDIDATE_ID = "candidate-v7m-final-r-recovery-audit-hardening"
SKILL_ORDER = (
    "structured-state-board",
    "rolling-planning",
    "delivery-progress",
    "risk-review",
)
EXPECTED_SKILLS = set(SKILL_ORDER)
REQUIRED_DELTA = {
    "FINAL_R_AND_INDEPENDENT_X",
    "ONE_RECONSIDER_BRANCH_MAXIMUM",
    "CURRENT_SURVIVAL_MODE_BEFORE_PROGRESSION_EVIDENCE_ORDER",
    "PRESERVE_V7L_DELIVERY_AND_RECOVERY_CONTRACTS",
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
    assert candidate["decision"] == "S07_45_STATIC_FINAL_R_RECOVERY_AUDIT_HARDENING"
    assert candidate["strategy_delta"] == "FINAL_PRE_GAME_CORRECTNESS_AND_AUDIT_ONLY"
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
    assert candidate["adopted_mechanisms"] == parent_candidate["adopted_mechanisms"]
    assert set(candidate["runtime_contract_delta"]) == REQUIRED_DELTA
    for key in ("deferred_mechanisms", "rejected_mechanisms", "architecture", "design_intent", "runner_sha"):
        assert candidate[key] == parent_candidate[key]
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
    recovery = manifest[manifest.index("On context recovery ("):]
    for marker in (
        "CurrentRoundCompressor",
        "confirm same game_session_id",
        "fresh observe",
        "reread all four Skills",
        *SKILL_ORDER,
        "rebuild Board",
        "rebuild Delivery",
        "restore Review Plan",
        "UNKNOWN",
        "RECOVERY_PENDING",
        "RECOVERY_READY",
        "do not act",
    ):
        assert marker in recovery
    ordered = (
        "STOP action submission",
        "confirm same game_session_id",
        "fresh observe",
        "reread all four Skills",
        "rebuild Board",
        "rebuild Delivery",
        "restore Review Plan",
        "RECOVERY_READY",
        "only then resume the decision loop",
    )
    assert [recovery.index(step) for step in ordered] == sorted(recovery.index(step) for step in ordered)


def test_public_evidence_whitelist_excludes_internal_fields_everywhere() -> None:
    texts = {
        name: (ROOT / f"skills/{name}/SKILL.md").read_text(encoding="utf-8")
        for name in SKILL_ORDER
    }
    manifest = _load_json(ROOT / "configs/runtime_manifest.json")["instruction"]
    for field in ("Health", "Dignity", "Skill", "Network", "Output", "Wealth", "Level", "Energy"):
        assert field in manifest
        assert field in texts["structured-state-board"]
    for source in ("formal review", "legal-choice text", "public Handbook", "public action receipts"):
        assert source in manifest
    for name in SKILL_ORDER:
        assert "HiddenRisk" in texts[name]
        assert "public-status-unclear" in texts[name]
    for target in ("Board", "Planning", "Delivery", "Risk", "CTRL notes", "action rationale"):
        assert target in manifest
    assert "numeric status_updates" in manifest
    assert "EXCLUDE_FROM_STRATEGY" in manifest


def test_v7l_strategy_recovery_and_other_skills_are_unchanged() -> None:
    manifest = _load_json(ROOT / "configs/runtime_manifest.json")["instruction"]
    parent = json.loads(_git_bytes(BASE_MAIN_SHA, "configs/runtime_manifest.json"))["instruction"]
    assert manifest.replace(
        _section(manifest, "Decision loop:", "\nStrategy kernel"),
        _section(parent, "Decision loop:", "\nStrategy kernel"),
    ).replace(
        _section(manifest, "notes begin with", "\nOn context recovery"),
        _section(parent, "notes begin with", "\nOn context recovery"),
    ) == parent
    assert _section(manifest, "Early evidence-gated pre-first-review prior:", "\nFormal review/promotion/no-advance") == _section(parent, "Early evidence-gated pre-first-review prior:", "\nFormal review/promotion/no-advance")
    assert _section(manifest, "On context recovery (", "No Team/Swarm") == _section(parent, "On context recovery (", "No Team/Swarm")

    for name in ("structured-state-board", "delivery-progress"):
        assert _canonical_text_bytes(ROOT / f"skills/{name}/SKILL.md") == _git_bytes(BASE_MAIN_SHA, f"skills/{name}/SKILL.md")
    planning = (ROOT / "skills/rolling-planning/SKILL.md").read_text(encoding="utf-8")
    parent_planning = _git_bytes(BASE_MAIN_SHA, "skills/rolling-planning/SKILL.md").decode("utf-8")
    assert planning.replace(_section(planning, "First select `MODE`", "1. formal review"), _section(parent_planning, "Use evidence in this order:", "1. formal review")).replace(_section(planning, "After emitting `CANDIDATE`", "\n## Select MODE"), _section(parent_planning, "After emitting `CANDIDATE`", "\n## Select MODE")) == parent_planning
    risk = (ROOT / "skills/risk-review/SKILL.md").read_text(encoding="utf-8")
    parent_risk = _git_bytes(BASE_MAIN_SHA, "skills/risk-review/SKILL.md").decode("utf-8")
    assert risk.replace(_section(risk, "`UNKNOWN` —", "Do not invent numeric thresholds"), _section(parent_risk, "`UNKNOWN` —", "Do not invent numeric thresholds")) == parent_risk
    delivery = (ROOT / "skills/delivery-progress/SKILL.md").read_text(encoding="utf-8")
    assert "Use after every fresh public Board" in delivery
    assert "current bounded same-session Delivery state" in delivery
    assert "n=0" in delivery and "NO_CHANGE" in delivery


def test_one_observe_one_pass_and_risk_only_reconsideration() -> None:
    planning = (ROOT / "skills/rolling-planning/SKILL.md").read_text(encoding="utf-8")
    manifest = _load_json(ROOT / "configs/runtime_manifest.json")["instruction"]
    section = _section(planning, "## Same-observation decision budget", "## Select MODE")
    for marker in (
        "ONE FRESH OBSERVE = ONE PLANNING PASS",
        "set `MODE + REVIEW_PLAN`",
        "eliminate clearly unacceptable or dominated",
        "at most two genuinely competitive options",
        "compare them once",
        "exactly one final `CANDIDATE`",
        "Only Risk=`RECONSIDER` may reopen selection once",
        "at most one directly relevant legal alternative",
        "`PASS`, `ALLOW`, or `WARN`",
        "`UNKNOWN` does not authorize a new Planning pass",
        "A new thought about unchanged evidence never reopens Planning",
        "Do not submit before closure",
    ):
        assert marker in section
    for marker in (
        "ONE OBSERVE = ONE PLANNING PASS",
        "at most two genuinely competitive choices once",
        "exactly one final CANDIDATE",
        "Only Risk=RECONSIDER may reopen selection once",
        "at most one directly relevant legal alternative",
        "Never take_action before closure",
    ):
        assert marker in manifest


def test_pre_game_delivery_and_ctrl_contract_is_consistent() -> None:
    delivery = (ROOT / "skills/delivery-progress/SKILL.md").read_text(encoding="utf-8")
    risk = (ROOT / "skills/risk-review/SKILL.md").read_text(encoding="utf-8")
    planning = (ROOT / "skills/rolling-planning/SKILL.md").read_text(encoding="utf-8")
    manifest = _load_json(ROOT / "configs/runtime_manifest.json")["instruction"]
    assert "Use after every fresh public Board" in delivery
    assert "Update only on new public evidence" in delivery
    assert "explicit empty state" in delivery and "carry forward" in delivery
    assert "BLOCKED` is optional" in delivery
    assert "IN_PROGRESS -> DELIVERY_CLAIMED -> DELIVERED" in delivery
    assert "latest still-valid `REVIEW_PLAN`" in delivery
    assert "Delivery never waits for a newly recomputed plan" in delivery
    assert "Planning alone chooses the new objective" in delivery
    assert "successful MCP/`take_action` receipt proves execution only" in delivery
    assert "generic `success=true`" in delivery
    assert "DELIVERED + PUBLICLY_VERIFIED" in delivery
    assert "|CLOSED|UNKNOWN>" not in delivery + manifest
    assert "recent `CLOSED` item is not active" in delivery
    assert "CTRL `R` records that selected candidate's final" in risk
    assert "CTRL `R` records that final result" in planning
    assert "CTRL R always records the selected submitted candidate's final Risk result" in manifest
    assert "do not open a second branch" in risk
    assert "do not search another alternative" in planning
    assert "do not open a second branch" in manifest
    assert "X=0" in risk + planning + manifest
    assert "at most one fresh observe/rebuild cycle" in risk + planning + manifest
    assert "R=UNKNOWN" in risk + planning + manifest
    assert "older progression feedback cannot override" in planning


def test_pre_first_review_prior_semantic_cases_a_to_e() -> None:
    planning = (ROOT / "skills/rolling-planning/SKILL.md").read_text(encoding="utf-8")
    prior = _section(planning, "#### Pre-first-review result realization prior", "### MODE=S")
    manifest = _load_json(ROOT / "configs/runtime_manifest.json")["instruction"]

    # A: existing public delivery and a legal result action beat unsupported workload.
    for marker in (
        "before the first formal review",
        "MODE=A",
        "no binding public survival/resource constraint",
        "current-session whitelisted Board/Delivery evidence",
        "existing high-value commitment",
        "work in progress or near completion",
        "DELIVERY_CLAIMED + UNVERIFIED",
        "legal action",
        "prefer that result-realization action over another generic workload push",
    ):
        assert marker in prior
    # B: a report-like label without underlying delivery never triggers the prior.
    for marker in ("menu label", "underlying result is insufficient", "If no such delivery basis exists"):
        assert marker in prior
    # C: the first formal review ends this prior and returns control to the review plan.
    assert "Exit this prior at the first formal review" in prior
    assert "feedback-anchored `REVIEW_PLAN` owns the objective" in prior
    # D: a material public constraint restores the existing MODE=S ordering.
    assert "material constraint requires `MODE=S`" in prior
    # E: a verified result with no new gap is not repeatedly packaged.
    assert "DELIVERED + PUBLICLY_VERIFIED" in prior
    assert "when the result becomes publicly verified" in prior
    assert "do not repeat a presentation" in prior

    assert "fixed report action" in prior
    assert "promotion threshold" in prior
    assert "not a fixed menu answer" in planning
    assert "clearly superior time-sensitive" in prior
    assert "After the first formal review" in manifest
    assert not any(term in prior.lower() for term in ("month 3", "month 6", "m3", "m6", "two reports"))


def test_candidate_and_state_record_static_closure_without_validation_transfer() -> None:
    candidate = _load_json(ROOT / "configs/current_candidate.json")
    state = (ROOT / "docs/project/CURRENT_STATE.md").read_text(encoding="utf-8")
    decisions = (ROOT / "docs/project/ARCHITECTURE_DECISIONS.md").read_text(encoding="utf-8")

    assert candidate["parent_candidate_id"] == PARENT_CANDIDATE_ID
    assert "S07-37" in state and CURRENT_CANDIDATE_ID in state
    assert re.search(r"Current Candidate:\s+candidate-v7m-final-r-recovery-audit-hardening", state)
    assert "all v7i validation flags are false" in state
    assert "## AD-018" in decisions and "S07-37" in decisions
    assert "PROMOTION_FIRST_WITH_SURVIVAL_FLOOR" in decisions
    assert "NEXT_GAME = NOT_AUTHORIZED" in state
    assert "NEXT_GAME = NOT_AUTHORIZED" in decisions
