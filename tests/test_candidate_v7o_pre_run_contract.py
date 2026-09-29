"""Static strategy and runtime-contract checks for v7r; not runtime enforcement."""

import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE_MAIN_SHA = "94b6acf771442cc3435af6ac1a43c25c9722bd5d"
V7N_MANIFEST_BASE_SHA = "23b5c52cdcd18aaf3f2613654b0d9d2302343661"


def _manifest() -> tuple[dict, str]:
    value = json.loads((ROOT / "configs/runtime_manifest.json").read_text(encoding="utf-8"))
    return value, value["instruction"]


def _skill(name: str) -> str:
    return (ROOT / f"skills/{name}/SKILL.md").read_text(encoding="utf-8")


def _section(text: str, start: str, end: str) -> str:
    start_index = text.index(start)
    end_index = text.index(end, start_index + len(start))
    return text[start_index:end_index]


def _v7n_manifest() -> str:
    raw = subprocess.check_output(
        ["git", "show", f"{V7N_MANIFEST_BASE_SHA}:configs/runtime_manifest.json"], cwd=ROOT
    )
    return json.loads(raw.decode("utf-8"))["instruction"]


def test_whole_game_persistence_and_same_execution_contract() -> None:
    _, instruction = _manifest()
    for marker in (
        "While structured game state is active, continue the tool loop in the same assistant execution",
        "DECISION_CLOSED closes only the current action selection, not the assistant execution",
        "After every successful take_action, immediately fresh-observe and begin the next cycle",
        "Do not voluntarily stop after an action, month, quarter, review, promotion",
        "Complete normally only when structured game state says ended or an unrecoverable runtime/tool failure blocks progress",
        "Structured game.ended owns natural terminal; transcript text does not",
        "Do not send a voluntary terminal answer while the game remains active",
    ):
        assert marker in instruction


def test_skill_load_policy_and_context_recovery_are_ordered() -> None:
    _, instruction = _manifest()
    startup = instruction[instruction.index("STARTUP AND ORDINARY FLOW"):instruction.index("WHOLE-GAME EXECUTION")]
    recovery = instruction[instruction.index("CONTEXT RECOVERY"):]
    skill_names = (
        "structured-state-board",
        "rolling-planning",
        "delivery-progress",
        "risk-review",
    )
    assert "read all four Skills once" in startup
    assert "do not reread SKILL.md" in startup
    assert all(name in startup for name in skill_names)
    assert "reread all four Skills in order" in recovery
    assert all(name in startup for name in skill_names)
    ordered = (
        "stop action submission",
        "confirm same game_session_id",
        "fresh observe",
        "reread all four Skills",
        "rebuild Board",
        "rebuild Delivery",
        "restore Review Plan",
        "Emit RECOVERY_READY",
        "then resume",
    )
    assert [recovery.index(item) for item in ordered] == sorted(recovery.index(item) for item in ordered)
    assert "remain RECOVERY_PENDING and do not act" in recovery
    assert "resume, compaction, or recovery signal is actually presented" in recovery
    assert "Do not claim automatic detection of an unexposed host compression event" in recovery
    assert "CurrentRoundCompressor" not in recovery


def test_manifest_owns_global_contracts_without_copying_skill_procedures() -> None:
    value, instruction = _manifest()
    assert value["name"] == "candidate-v7r-early-promotion-rescue"
    assert len(instruction) <= 5200
    assert "Poor performance and no-promotion alone are progression evidence, not MODE=S." in instruction
    assert "Absent an explicit material job-continuity threat, repair review gaps in MODE=A." in instruction
    reduction = 1 - len(instruction) / len(_v7n_manifest())
    assert reduction >= 0.35
    for owner in (
        "structured-state-board=facts",
        "rolling-planning=strategy/objectives/ranking",
        "delivery-progress=current-session delivery lifecycle",
        "risk-review=final candidate risk gate",
    ):
        assert owner in instruction
    assert "Single Agent is the only action submitter" in instruction
    assert "PRE_FIRST_REVIEW_RESULT_REALIZATION_PRIOR" not in instruction
    assert "Full Review" not in instruction
    assert "IN_PROGRESS -> DELIVERY_CLAIMED -> DELIVERED" not in instruction
    assert "Do not duplicate Skill procedures" in instruction


def test_compression_resilient_kernel_and_best_effort_recovery_are_explicit() -> None:
    _, instruction = _manifest()
    assert "COMPRESSION-RESILIENT CRITICAL KERNEL" in instruction
    assert "Default MODE=A unless" in instruction
    assert "Numeric levels, declines, or inferred thresholds alone never justify MODE=S" in instruction
    assert "After review, follow the clearest public progression gap" in instruction
    assert "Do not claim automatic detection of an unexposed host compression event" in instruction
    kernel = instruction[instruction.index("COMPRESSION-RESILIENT CRITICAL KERNEL"):instruction.index("STARTUP AND ORDINARY FLOW")]
    for marker in (
        "a good grade without promotion still leaves promotion readiness unresolved",
        "Fresh observed no-gain outranks advertised gain for that dimension",
        "do not repeatedly spend scarce quarterly actions on a no-gain path",
        "clear the signal after Level change or contradictory fresh gain",
        "Do not demote Skill from promotion planning because of terminal-score saturation assumptions",
        "Never infer hidden thresholds, caps, risk scores, or eligibility",
    ):
        assert marker in kernel


def test_checkpoint_aware_marginal_progression_contract() -> None:
    planning = _skill("rolling-planning")
    required = (
        "A good formal grade without promotion still means promotion readiness is unresolved",
        "Use the next public formal review as the checkpoint for promotion preparation",
        "Do not demote Skill because of terminal-score saturation assumptions",
        "Fresh observed no-gain outranks the advertised effect",
        "Do not immediately repeat the same action merely to confirm it",
        "discount only the dimension with current no-gain evidence",
        "clear it after a Level change",
        "Do not infer a cap or formula",
    )
    for marker in required:
        assert marker in planning
    assert "Do not prefer pure Skill growth solely for direct terminal score" not in planning
    assert "another still-responsive progression path exists" in planning
    assert "retain any other still-responsive public benefit" in planning
    assert "after a later clean fresh observe shows that dimension increasing again" in planning


def test_v7r_board_separates_review_from_sticky_and_tracks_progression_response() -> None:
    board = _skill("structured-state-board")
    assert "REVIEW: <latest formal grade/feedback/promotion/no-advance | none>" in board
    assert "PROGRESSION_RESPONSE:" in board
    for marker in (
        "S=<GAIN|NO_GAIN|UNKNOWN>",
        "N=<GAIN|NO_GAIN|UNKNOWN>",
        "O=<GAIN|NO_GAIN|UNKNOWN>",
        "LEVEL=<current Level>",
        "A poor grade, no-advance result, or ordinary performance deficit alone",
        "does not create binding `STICKY` state",
        "explicitly states a material dismissal or job-continuity threat",
        "If the session or Level changed, reset all three responses to `UNKNOWN`",
        "carry forward each untouched dimension",
        "record `GAIN` if it increased and `NO_GAIN` if it stayed unchanged",
        "A later clean advertised gain overwrites `NO_GAIN`",
        "Reconstruct progression responses only from bounded same-session public evidence",
        "otherwise mark them `UNKNOWN`",
        "keep `EFFECTS` bounded",
    ):
        assert marker in board


def test_v7r_mode_split_and_progression_responses_cover_review_scenarios() -> None:
    planning = _skill("rolling-planning")
    mode = _section(planning, "## Select MODE", "## Rank legal candidates")
    for marker in (
        "Poor grade, no-advance, weak Skill/Network/Output",
        "do not by themselves justify `MODE=S`",
        "repair performance and promotion in `MODE=A`",
        "Only an explicit participant-visible material dismissal or job-continuity threat",
        "explicit acute physical symptoms",
        "active trust/compliance/confidentiality crisis",
        "direct affordability/income-continuity crisis",
    ):
        assert marker in mode

    response = planning[planning.index("Consume the Board's current-Level `PROGRESSION_RESPONSE`"):planning.index("When the current review gap is unresolved")]
    for marker in (
        "`GAIN` is current evidence",
        "`NO_GAIN` discounts only that dimension",
        "`UNKNOWN` stays open",
        "retains value from responsive or unknown dimensions",
        "do not starve one of Skill, Network, or Output across scarce quarterly opportunities",
        "Specific formal feedback may concentrate effort",
        "Do not impose a fixed ratio",
    ):
        assert marker in response


def test_v7r_delivery_certainty_and_public_warning_cleanup_are_bounded() -> None:
    planning = _skill("rolling-planning")
    delivery = _section(planning, "### Review-window delivery certainty", "### MODE=S")
    for marker in (
        "Before the next public formal review",
        "delays current scheduled deliverables",
        "near-term delivery certainty for speculative long-horizon learning",
        "introduces first-delivery uncertainty",
        "preserves current delivery certainty",
        "unless the uncertain option is required for safety/compliance",
        "specific formal review feedback directly makes it the stronger progression response",
        "not a fixed-month rule or Story answer",
        "does not ban long-term learning",
    ):
        assert marker in delivery

    cleanup = _section(planning, "### Public warning cleanup", "### MODE=A")
    for marker in (
        "risk is elevated, accumulating, or needs handling",
        "legal option explicitly repairs that warned risk",
        "one bounded cleanup before the next formal review",
        "Do not repeat cleanup without a new public warning or other fresh evidence",
        "A warning alone does not create permanent `MODE=S`",
        "acute survival or safety constraints still outrank cleanup",
        "Never infer hidden Risk values",
    ):
        assert marker in cleanup


def test_public_risk_review_still_gates_material_compliance_and_confidentiality() -> None:
    risk = _skill("risk-review")
    assert "compliance / confidentiality / safety" in risk
    assert "material public risk" in risk
    assert "Do not invent numeric thresholds, hidden counts, failure probabilities, or hidden-risk values" in risk


def test_global_evidence_firewall_and_action_preflight() -> None:
    _, instruction = _manifest()
    for marker in (
        "HiddenRisk",
        "internal score components",
        "numeric status_updates without verified public status",
        "public-status-unclear fields",
        "are unusable.",
        "Do not inspect, quote, compare, summarize, remember, or reason from them",
        "instruction-only",
        "no deterministic raw-payload filter exists",
        "EXCLUDE_FROM_STRATEGY",
        "CTRL, DL, or action rationale",
    ):
        assert marker in instruction
    assert "Flow: fresh observe → Board → Delivery → Planning → Risk → preflight → take_action → fresh observe → continue" in instruction
    assert "exactly one legal integer choice" in instruction
    assert "Planning closed on exactly one candidate" in instruction
    assert "final Risk complete" in instruction
    assert "exactly one `[CTRL" in instruction and "exactly one `[DL" in instruction
    assert "CTRL R records the submitted candidate's final Risk result" in instruction
    assert "X=0 forbids submission" in instruction


def test_static_scenario_ordinary_workload_and_numeric_fluctuation_do_not_force_s() -> None:
    board = _skill("structured-state-board")
    planning = _skill("rolling-planning")
    # Scenario: on-call/exercise versus non-urgent work, mild fatigue, a routine
    # public number fluctuation, and no explicit acute symptom.
    scenario = "on-call exercise; non-urgent work; mild fatigue; ordinary one-step decline; no acute symptom"
    assert "non-urgent work" in scenario and "no acute symptom" in scenario
    assert "A numeric fluctuation or ordinary one-step decline alone remains a `STATE` observation" in board
    assert "it does not create a binding `STICKY` warning" in board
    assert "A displayed H/D/W number or an ordinary one-step decrease alone does not establish a binding constraint" in planning
    assert "does not justify `MODE=S`" in planning


def test_static_scenario_explicit_acute_symptom_or_direct_continuity_crisis_can_bind() -> None:
    board = _skill("structured-state-board")
    planning = _skill("rolling-planning")
    assert "explicit current acute physical or psychological symptom" in board
    assert "must enter `STICKY`" in board
    assert "explicit acute physical symptoms" in planning
    assert "direct affordability/income-continuity crisis" in planning
    assert "A clearly depleted public resource may bind" in planning
    assert not re.search(r"(?:Health|Dignity|Wealth)\s*(?:<=|<|≤)\s*\d+", planning + board)


def test_static_scenario_hidden_numeric_field_is_firewalled_without_claiming_filtering() -> None:
    _, instruction = _manifest()
    # Synthetic scenario data only; the numeric value is never used as a rule or threshold.
    raw_payload = {"participant_visible_state": {"health": "public"}, "HiddenRisk": 17}
    assert isinstance(raw_payload["HiddenRisk"], int)
    assert "HiddenRisk" in instruction and "are unusable" in instruction
    assert "ignore them at source" in instruction.casefold()
    assert "no deterministic raw-payload filter exists" in instruction


def test_static_scenario_successful_action_continues_the_same_execution() -> None:
    _, instruction = _manifest()
    assert "While structured game state is active, continue the tool loop in the same assistant execution" in instruction
    planning = _skill("rolling-planning")
    assert "After every successful take_action, immediately fresh-observe" in instruction
    assert "begin the next cycle" in instruction


def test_static_scenario_formal_review_is_not_an_execution_terminal() -> None:
    _, instruction = _manifest()
    planning = _skill("rolling-planning")
    assert "quarter, review, promotion, local closure" in instruction
    assert "Do not send a voluntary terminal answer while the game remains active" in instruction
    assert "formal review / promotion / no-advance" in planning
    assert "fresh observe" in planning


def test_delivery_risk_blobs_and_frozen_runner_are_unchanged_from_base() -> None:
    for relative in (
        "skills/delivery-progress/SKILL.md",
        "skills/risk-review/SKILL.md",
    ):
        expected = subprocess.check_output(
            ["git", "rev-parse", f"{BASE_MAIN_SHA}:{relative}"], cwd=ROOT, text=True
        ).strip()
        actual = subprocess.check_output(
            ["git", "hash-object", f"--path={relative}", str(ROOT / relative)],
            cwd=ROOT,
            text=True,
        ).strip()
        assert actual == expected

    for relative in ("pyproject.toml", "uv.lock"):
        expected = subprocess.check_output(
            ["git", "rev-parse", f"{BASE_MAIN_SHA}:{relative}"], cwd=ROOT, text=True
        ).strip()
        actual = subprocess.check_output(
            ["git", "hash-object", f"--path={relative}", str(ROOT / relative)],
            cwd=ROOT,
            text=True,
        ).strip()
        assert actual == expected

    frozen_changes = subprocess.check_output(
        ["git", "diff", "--name-only", BASE_MAIN_SHA, "--", "career_sim_runner"],
        cwd=ROOT,
        text=True,
    ).strip()
    assert frozen_changes == ""

    candidate = json.loads((ROOT / "configs/current_candidate.json").read_text(encoding="utf-8"))
    assert candidate["runner_sha"] == "f61c738c72e51b77298cc1c14c7c6ebf4b6c527d"
