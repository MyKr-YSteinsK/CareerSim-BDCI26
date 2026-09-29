"""Static identity and correctness-contract checks for the current v7 Candidate."""

import hashlib
import json
import re
import subprocess
from pathlib import Path

from career_sim_runner.skill_contract import validate_skill_frontmatter


ROOT = Path(__file__).resolve().parents[1]
BASE_MAIN_SHA = "23b5c52cdcd18aaf3f2613654b0d9d2302343661"
S08_04_COMMIT_SHA = "aba687672cda4164c75a7b57d2bad4ae01902654"
PARENT_CANDIDATE_ID = "candidate-v7n-public-state-delivery-constraint-hardening"
CURRENT_CANDIDATE_ID = "candidate-v7o-execution-persistence-convergence"
SKILL_ORDER = (
    "structured-state-board",
    "rolling-planning",
    "delivery-progress",
    "risk-review",
)
EXPECTED_SKILLS = set(SKILL_ORDER)
REQUIRED_DELTA = {
    "WHOLE_GAME_EXECUTION_PERSISTENCE",
    "MANIFEST_SEMANTIC_DEDUPLICATION",
    "NORMAL_FLOW_NO_SKILL_REREAD",
    "HIDDEN_FIELD_SALIENCE_HARDENING",
    "NUMERIC_STATE_NOT_AUTOMATIC_BINDING_CONSTRAINT",
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
    assert candidate["decision"] == "S08_04_EXECUTION_PERSISTENCE_CONVERGENCE"
    assert candidate["strategy_delta"] == "MODE_BINDING_CORRECTNESS_CLARIFICATION_ONLY"
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
    runtime_paths = [candidate["runtime_manifest"]["path"], *(entry["path"] for entry in entries)]
    for relative_path in runtime_paths:
        expected_blob = subprocess.check_output(
            ["git", "rev-parse", f"{S08_04_COMMIT_SHA}:{relative_path}"],
            cwd=ROOT,
            text=True,
        ).strip()
        assert _git_blob_id(ROOT / relative_path) == expected_blob
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
    candidate = _load_json(ROOT / "configs/current_candidate.json")
    combined = planning + "\n" + manifest

    assert "Maximize long-horizon progression" in planning
    assert "`A` = Advance. Default." in planning
    assert candidate["design_intent"] == "PROMOTION_FIRST_WITH_SURVIVAL_FLOOR"
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
    assert "exactly one legal integer choice" in manifest
    assert not re.search(r"(?:fixed|standard)\s+Energy\s+bundle", combined, re.IGNORECASE)


def test_risk_gates_candidates_without_replanning() -> None:
    risk = (ROOT / "skills/risk-review/SKILL.md").read_text(encoding="utf-8")
    assert "Planning's final legal candidate" in risk
    assert "Never re-plan the whole decision" in risk
    assert "Risk does not own the Review Plan or candidate ranking" in risk
    assert "Compare at most that alternative" in risk


def test_manifest_retains_action_preflight_and_same_session_recovery() -> None:
    manifest = _load_json(ROOT / "configs/runtime_manifest.json")["instruction"]
    assert "Before each take_action" in manifest
    assert "exactly one legal integer choice" in manifest
    assert "current game_session_id" in manifest
    assert "exactly one `[CTRL" in manifest
    assert "exactly one `[DL" in manifest
    recovery = manifest[manifest.index("CONTEXT RECOVERY"):]
    for marker in (
        "CurrentRoundCompressor",
        "confirm the same game_session_id",
        "fresh observe",
        "reread all four Skills",
        *SKILL_ORDER,
        "rebuild Board",
        "rebuild Delivery",
        "restore the Review Plan",
        "UNKNOWN",
        "RECOVERY_PENDING",
        "RECOVERY_READY",
        "do not act",
    ):
        assert marker in recovery
    ordered = (
        "stop action submission",
        "confirm the same game_session_id",
        "fresh observe",
        "reread all four Skills",
        "rebuild Board",
        "rebuild Delivery",
        "restore the Review Plan",
        "RECOVERY_READY",
        "resume the loop only then",
    )
    assert [recovery.index(step) for step in ordered] == sorted(recovery.index(step) for step in ordered)


def test_public_evidence_whitelist_excludes_internal_fields_everywhere() -> None:
    texts = {
        name: (ROOT / f"skills/{name}/SKILL.md").read_text(encoding="utf-8")
        for name in SKILL_ORDER
    }
    manifest = _load_json(ROOT / "configs/runtime_manifest.json")["instruction"]
    for field in ("Health", "Dignity", "Skill", "Network", "Output", "Wealth", "Level", "Energy"):
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


def test_s07_48_board_copies_fresh_public_values_and_quarantines_mixed_effects() -> None:
    board = (ROOT / "skills/structured-state-board/SKILL.md").read_text(encoding="utf-8")
    manifest = _load_json(ROOT / "configs/runtime_manifest.json")["instruction"]
    state_contract = _section(board, "## Contract", "## Procedure")
    for field in ("Health", "Dignity", "Skill", "Network", "Output", "Wealth", "Level", "Energy"):
        assert field in state_contract
    for marker in (
        "Copy `Health`, `Dignity`, `Skill`, `Network`, `Output`, `Wealth`, `Level`, and `Energy` directly",
        "Preserve each reported value and precision",
        "Never calculate, round, predict, reconcile, or replace a `STATE` value",
        "EFFECTS: UNKNOWN / MIXED",
        "explicit current acute physical or psychological symptom",
        "Ordinary fatigue",
        "Downstream Planning/Risk receive the whitelisted Board",
        "never quote, compare, summarize, or reason from their values",
    ):
        assert marker in board
    assert "salary/bonus text" in board
    assert "Do not infer thresholds, counters, caps" in board
    assert "instruction-only" in manifest and "deterministic raw-payload filter" in manifest


def test_s07_48_delivery_identity_proof_and_non_saturating_retirement() -> None:
    delivery = (ROOT / "skills/delivery-progress/SKILL.md").read_text(encoding="utf-8")
    manifest = _load_json(ROOT / "configs/runtime_manifest.json")["instruction"]
    for marker in (
        "agent-generated `D1`, `D2`, … identity",
        "never reuse one for another item during that session",
        "monotonic `NEXT_ID` cursor",
        "Reset only after verifying a different fresh `game_session_id`",
        "mark identity `UNKNOWN`",
        "Store a short `proof_basis` attached to that item",
        "generic `success=true`",
        "Generic praise",
        "does not verify delivery",
        "explicitly connects recognition to that item's result",
        "completed items without an active checkpoint",
        "Do not use arbitrary TTLs or fixed months",
        "Three genuinely active items are valid",
        "replace the least relevant item",
        "[DL i=<NONE|D#|UNKNOWN> n=<0-3>",
        "i=NONE focus=NONE evidence=NA checkpoint=0 recognition=0",
    ):
        assert marker in delivery
    assert "[DL i=<NONE|D#|UNKNOWN> n=<0-3>" in manifest
    assert "cross-game memory" in delivery.lower()


def test_s07_48_explicit_binding_constraint_and_full_risk_labels() -> None:
    planning = (ROOT / "skills/rolling-planning/SKILL.md").read_text(encoding="utf-8")
    risk = (ROOT / "skills/risk-review/SKILL.md").read_text(encoding="utf-8")
    manifest = _load_json(ROOT / "configs/runtime_manifest.json")["instruction"]
    mode = _section(planning, "## Select MODE", "## Rank legal candidates")
    for marker in (
        "Before progression ranking",
        "unresolved binding constraint",
        "explicit acute physical symptoms",
        "An acute symptom remains binding even if the displayed Health/Dignity/Wealth value appears adequate",
        "Return to `MODE=A` when fresh public evidence indicates",
        "mild fatigue without an explicit material symptom/warning",
        "do not use a numeric threshold",
    ):
        assert marker in mode
    assert "explicit acute physical symptom" in risk
    assert "A safe, constructive candidate still receives Full Review" in risk
    assert "After Full Review, never output `PASS`" in risk
    assert "`ALLOW`" in risk
    assert "risk-review=final candidate risk gate" in manifest
    assert "Full Review" not in manifest and "mild fatigue" not in manifest.lower()


def test_planning_and_risk_details_remain_skill_owned_and_preserved() -> None:
    manifest = _load_json(ROOT / "configs/runtime_manifest.json")["instruction"]
    assert "rolling-planning=strategy, objectives, and ranking" in manifest
    assert "Early evidence-gated pre-first-review prior" not in manifest
    assert "On context recovery (" not in manifest

    planning = (ROOT / "skills/rolling-planning/SKILL.md").read_text(encoding="utf-8")
    parent_planning = _git_bytes(BASE_MAIN_SHA, "skills/rolling-planning/SKILL.md").decode("utf-8")
    assert _section(planning, "## Same-observation decision budget", "## Select MODE") == _section(parent_planning, "## Same-observation decision budget", "## Select MODE")
    assert _section(planning, "#### Pre-first-review result realization prior", "### MODE=S") == _section(parent_planning, "#### Pre-first-review result realization prior", "### MODE=S")
    assert _section(planning, "## Quarterly control", "## Output") == _section(parent_planning, "## Quarterly control", "## Output")
    risk = (ROOT / "skills/risk-review/SKILL.md").read_text(encoding="utf-8")
    parent_risk = _git_bytes(BASE_MAIN_SHA, "skills/risk-review/SKILL.md").decode("utf-8")
    assert _section(risk, "After `RECONSIDER`", "## Close") == _section(parent_risk, "After `RECONSIDER`", "## Close")


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
    assert "Planning closed on exactly one candidate" in manifest
    assert "Never act before closure" in manifest


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
    assert "X=0" in risk + planning + manifest
    assert "at most one fresh observe/rebuild cycle" in risk + planning
    assert "R=UNKNOWN" in risk + planning
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
    assert "rolling-planning=strategy, objectives, and ranking" in manifest
    assert not any(term in prior.lower() for term in ("month 3", "month 6", "m3", "m6", "two reports"))


def test_candidate_and_state_record_static_closure_without_validation_transfer() -> None:
    candidate = _load_json(ROOT / "configs/current_candidate.json")
    state = (ROOT / "docs/project/CURRENT_STATE.md").read_text(encoding="utf-8")
    review = (ROOT / "docs/project/reviews/S08-04_EXECUTION_PERSISTENCE_PRE_RUN_CONVERGENCE.md").read_text(encoding="utf-8")
    decisions = (ROOT / "docs/project/ARCHITECTURE_DECISIONS.md").read_text(encoding="utf-8")
    current_section = state.split("## Current candidate\n", 1)[1].split("\n## ", 1)[0]
    current_line = next(line for line in current_section.splitlines() if line.startswith("- Current Candidate:"))

    assert candidate["parent_candidate_id"] == PARENT_CANDIDATE_ID
    assert "S07-48" in state and "S07-47" in state and CURRENT_CANDIDATE_ID in state
    assert current_line.startswith("- Current Candidate: candidate-v7o-execution-persistence-convergence")
    assert "v7o runtime/gameplay/provider/long-horizon/survival/score/stable-80+/hidden-transfer validation flags remain false" in current_line
    assert "NEXT_GAME = NOT_AUTHORIZED" in current_line
    assert candidate["strategy_delta"] == "MODE_BINDING_CORRECTNESS_CLARIFICATION_ONLY"
    assert "New strategy mechanism: `NO`." in review
    assert "Behavior-relevant correctness/policy delta: `YES`" in review
    assert "Execution persistence delta: `YES`." in review
    assert "NO_STRATEGY_DELTA" not in review
    assert "NO_STRATEGY_DELTA" not in current_section
    assert "## AD-018" in decisions and "S07-37" in decisions
    assert "PROMOTION_FIRST_WITH_SURVIVAL_FLOOR" in decisions
    assert "NEXT_GAME = NOT_AUTHORIZED" in state
    assert "NEXT_GAME = NOT_AUTHORIZED" in decisions
