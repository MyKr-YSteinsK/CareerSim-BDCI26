"""Static governance and submission-contract checks for Candidate evolution."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTRACTS = {
    "agent_runtime": ROOT / "docs/project/AGENT_RUNTIME_CONTRACT.md",
    "candidate_evaluation": ROOT / "docs/project/CANDIDATE_EVALUATION_CONTRACT.md",
    "live_run_progress": ROOT / "docs/project/LIVE_RUN_PROGRESS_CONTRACT.md",
    "final_submission": ROOT / "docs/project/FINAL_SUBMISSION_CONTRACT.md",
}


def test_all_four_contracts_are_readable_and_have_document_structure() -> None:
    for path in CONTRACTS.values():
        text = path.read_text(encoding="utf-8")
        assert text.startswith("# ")
        assert len(text.strip()) > 500
        assert "\ufffd" not in text

    assert "FINAL_FROZEN_FOR_SUBMISSION" in CONTRACTS["final_submission"].read_text(encoding="utf-8")
    assert "Candidate" in CONTRACTS["candidate_evaluation"].read_text(encoding="utf-8")
    assert "progress" in CONTRACTS["live_run_progress"].read_text(encoding="utf-8").casefold()


def test_repository_governance_files_reference_contracts_without_copying_them() -> None:
    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    workflow = (ROOT / "docs/project/LIVE_RUN_WORKFLOW.md").read_text(encoding="utf-8")

    for filename in (
        "AGENT_RUNTIME_CONTRACT.md",
        "CANDIDATE_EVALUATION_CONTRACT.md",
        "FINAL_SUBMISSION_CONTRACT.md",
    ):
        assert filename in agents
    assert "task-specific permissions" in agents
    assert "LIVE_RUN_PROGRESS_CONTRACT.md" in workflow
    assert "grants no additional runtime operation, probe, or retry authority" in workflow
    assert "Use the [Live Run Progress Reporting Contract]" in workflow

    for key, path in CONTRACTS.items():
        content = path.read_text(encoding="utf-8").strip()
        if key == "live_run_progress":
            assert content not in workflow
        if key != "live_run_progress":
            assert content not in agents


def test_current_candidate_is_distinct_from_final_submission_and_builder_whitelist_is_exact() -> None:
    candidate = json.loads((ROOT / "configs/current_candidate.json").read_text(encoding="utf-8"))
    final_identity = json.loads((ROOT / "docs/project/FINAL_SUBMISSION_IDENTITY.json").read_text(encoding="utf-8"))
    builder = (ROOT / "scripts/build_final_solution.py").read_text(encoding="utf-8")
    assert candidate["candidate_id"] == "candidate-v8a-v7o-donor-core-transplant"
    assert candidate["status"] == "FINAL_FROZEN_FOR_SUBMISSION"
    assert candidate["candidate_id"] != final_identity["candidate_id"]
    assert candidate["validation"]["runtime_validated"] is False
    assert candidate["validation"]["gameplay_validated"] is True
    assert candidate["validation"]["provider_validated"] is True
    assert candidate["validation"]["next_game_authorized"] is False
    assert "FINAL_FROZEN_FOR_SUBMISSION" in builder
    assert '"README.md"' in builder
    assert '"design/skills_design.md"' in builder
    assert '"design/decision_report.md"' in builder
    for skill in (
        "structured-state-board",
        "rolling-planning",
        "delivery-progress",
        "risk-review",
    ):
        assert f'"{skill}"' in builder
    assert '"skills"' in builder and '"SKILL.md"' in builder
    assert "provider, service, MCP, DB, or" in builder
    assert "game operation" in builder


def test_current_state_and_review_record_static_scope_and_no_live_authority() -> None:
    state = (ROOT / "docs/project/CURRENT_STATE.md").read_text(encoding="utf-8")
    review = (ROOT / "docs/project/reviews/S08-08_V7S_ZH_EXECUTION_CONTRACT_CONVERGENCE.md").read_text(encoding="utf-8")
    current_section = state.split("## 4. 当前 Checkout 说明\n", 1)[1].split("\n## ", 1)[0]
    authorization_section = state.split("## 7. 当前授权边界\n", 1)[1].split("\n## ", 1)[0]

    assert "candidate-v8a-v7o-donor-core-transplant" in current_section
    assert "并非最终 exact-v6 ZIP 身份" in current_section
    assert "delivery-progress" in current_section
    assert "NEW_GAME = NOT_AUTHORIZED" in authorization_section
    assert "TAKE_ACTION = NOT_AUTHORIZED" in authorization_section
    assert "V7S_READY_FOR_GAME_GATE" in review
    assert "no provider call" in review.casefold()
    assert "Planner" in review
