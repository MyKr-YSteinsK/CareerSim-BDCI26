"""Static strategy and runtime-contract checks for v7p; not runtime enforcement."""

import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE_MAIN_SHA = "3fd64bead5600c2f0bab677e7b832fe3678bdf12"
V7N_MANIFEST_BASE_SHA = "23b5c52cdcd18aaf3f2613654b0d9d2302343661"


def _manifest() -> tuple[dict, str]:
    value = json.loads((ROOT / "configs/runtime_manifest.json").read_text(encoding="utf-8"))
    return value, value["instruction"]


def _skill(name: str) -> str:
    return (ROOT / f"skills/{name}/SKILL.md").read_text(encoding="utf-8")


def _v7n_manifest() -> str:
    raw = subprocess.check_output(
        ["git", "show", f"{V7N_MANIFEST_BASE_SHA}:configs/runtime_manifest.json"], cwd=ROOT
    )
    return json.loads(raw.decode("utf-8"))["instruction"]


def test_whole_game_persistence_and_same_execution_contract() -> None:
    _, instruction = _manifest()
    for marker in (
        "While the structured game is active, continue the tool loop within the same assistant execution",
        "DECISION_CLOSED closes only the current action selection; it does not complete the assistant execution",
        "After every successful take_action, immediately obtain a fresh observe and begin the next decision cycle",
        "Do not voluntarily stop after one action, month, quarter, review, promotion",
        "Complete normally only when structured game state says the game ended or an unrecoverable runtime/tool failure",
        "Structured game.ended owns the natural terminal; transcript text does not",
        "Do not send a voluntary terminal user-facing answer while the game remains active",
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
    assert "read each of the four Skills once" in startup
    assert "do not reread SKILL.md" in startup
    assert all(name in startup for name in skill_names)
    assert "reread all four Skills in order" in recovery
    assert all(name in recovery for name in skill_names)
    ordered = (
        "stop action submission",
        "confirm the same game_session_id",
        "obtain a fresh observe",
        "reread all four Skills",
        "rebuild Board",
        "rebuild Delivery",
        "restore the Review Plan",
        "Emit RECOVERY_READY",
        "resume the loop only then",
    )
    assert [recovery.index(item) for item in ordered] == sorted(recovery.index(item) for item in ordered)
    assert "remain RECOVERY_PENDING and do not act" in recovery
    assert "resume, compaction, or recovery signal is actually presented" in recovery
    assert "Do not claim automatic detection of an unexposed host compression event" in recovery
    assert "CurrentRoundCompressor" not in recovery


def test_manifest_owns_global_contracts_without_copying_skill_procedures() -> None:
    value, instruction = _manifest()
    assert value["name"] == "candidate-v7p-score-gap-convergence"
    assert len(instruction) <= 5200
    reduction = 1 - len(instruction) / len(_v7n_manifest())
    assert reduction >= 0.35
    for owner in (
        "structured-state-board=facts",
        "rolling-planning=strategy, objectives, and ranking",
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
    assert "Default to MODE=A" in instruction
    assert "Numeric levels, declines, or inferred thresholds alone never justify MODE=S" in instruction
    assert "After review, follow the clearest public progression gap" in instruction
    assert "Do not claim automatic detection of an unexposed host compression event" in instruction


def test_review_gap_directness_is_general_and_feedback_gated() -> None:
    planning = _skill("rolling-planning")
    assert "Primary Gap=DIRECT_PROGRESSION_EVIDENCE" in planning
    assert "most direct observable path to the review/promotion objective" in planning
    assert "generic relationship-building or role-breadth options" in planning
    assert "specifically names Network/breadth as the primary gap" in planning
    assert "never a fixed answer or eligibility claim" in planning
    assert "Do not prefer pure Skill growth solely for direct terminal score" in planning
    assert "Skill remains valuable when public review or progression evidence makes it instrumental" in planning


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
        "unusable input",
        "Do not inspect, quote, compare, summarize, remember, or reason from them",
        "instruction-only",
        "there is no deterministic raw-payload filter",
        "EXCLUDE_FROM_STRATEGY",
        "CTRL notes, DL, or action rationale",
    ):
        assert marker in instruction
    assert "Board → Delivery → Planning → Risk → preflight → take_action → fresh observe → continue" in instruction
    assert "exactly one legal integer choice" in instruction
    assert "Planning closed on exactly one candidate" in instruction
    assert "final Risk review complete" in instruction
    assert "exactly one `[CTRL" in instruction and "exactly one `[DL" in instruction
    assert "CTRL R always records the selected submitted candidate's final Risk result" in instruction
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
    assert "HiddenRisk" in instruction and "unusable input" in instruction
    assert "ignore them at source" in instruction.casefold()
    assert "there is no deterministic raw-payload filter" in instruction


def test_static_scenario_successful_action_continues_the_same_execution() -> None:
    _, instruction = _manifest()
    assert "While the structured game is active, continue the tool loop within the same assistant execution" in instruction
    planning = _skill("rolling-planning")
    assert "After every successful take_action, immediately obtain a fresh observe" in instruction
    assert "begin the next decision cycle" in instruction


def test_static_scenario_formal_review_is_not_an_execution_terminal() -> None:
    _, instruction = _manifest()
    planning = _skill("rolling-planning")
    assert "review, promotion, local decision closure" in instruction
    assert "Do not send a voluntary terminal user-facing answer while the game remains active" in instruction
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

    candidate = json.loads((ROOT / "configs/current_candidate.json").read_text(encoding="utf-8"))
    assert candidate["runner_sha"] == "f61c738c72e51b77298cc1c14c7c6ebf4b6c527d"
