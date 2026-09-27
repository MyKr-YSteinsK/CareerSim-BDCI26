"""Static identity, ownership, and policy contract for the formal Candidate."""

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
BASE_MAIN_SHA = "d10f354f5338e7950bd49efeba7b9d524e82f23a"
PARENT_CANDIDATE_ID = "candidate-v7b-semantic-generalization"
NEW_MECHANISMS = {
    "PUBLIC_DURATION_IN_LEVEL_CONTEXT",
    "REVIEW_WINDOW_REALIZATION_AWARENESS",
    "TIME_TO_REALIZATION_AWARENESS",
    "QUALITATIVE_COMMITMENT_CONGESTION",
    "CLOSE_BEFORE_OPEN_WHEN_GLOBALLY_DOMINANT",
    "LATE_HORIZON_REALIZATION_BIAS",
    "HIERARCHICAL_DECISION_POLICY",
    "PROGRESSIVE_DISCLOSURE_RUNTIME_KERNEL",
}


def _git_blob_id(path: Path) -> str:
    relative_path = path.relative_to(ROOT).as_posix()
    return subprocess.check_output(
        ["git", "hash-object", f"--path={relative_path}", str(path)],
        cwd=ROOT,
        text=True,
    ).strip()


def _git_bytes(revision: str, path: str) -> bytes:
    spec = f":{path}" if revision == ":" else f"{revision}:{path}"
    return subprocess.check_output(["git", "show", spec], cwd=ROOT)


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_json_bytes(content: bytes) -> dict:
    return json.loads(content.decode("utf-8"))


def _skill_blobs_at(revision: str) -> list[dict]:
    return [
        {
            "name": name,
            "git_blob": subprocess.check_output(
                ["git", "rev-parse", f"{revision}:skills/{name}/SKILL.md"],
                cwd=ROOT,
                text=True,
            ).strip(),
        }
        for name in (
            "structured-state-board",
            "rolling-planning",
            "delivery-progress",
            "risk-review",
        )
    ]


def test_candidate_identity_matches_v7b_parent_and_staged_artifacts() -> None:
    candidate = _load_json(ROOT / "configs/current_candidate.json")
    manifest_path = ROOT / "configs/runtime_manifest.json"
    manifest = _load_json(manifest_path)
    manifest_bytes = _git_bytes(":", "configs/runtime_manifest.json")

    assert candidate["candidate_id"] == "candidate-v7c-global-decision-policy"
    assert candidate["parent_candidate_id"] == PARENT_CANDIDATE_ID
    assert candidate["status"] == "STATIC_IMPLEMENTED_NOT_RUNTIME_VALIDATED"
    assert candidate["decision"] == "S07_26_STATIC_GLOBAL_DECISION_POLICY"
    assert candidate["strategy_delta"] == "HIERARCHICAL_DECISION_POLICY_AND_PROGRESSIVE_DISCLOSURE"
    assert candidate["base_main_sha"] == BASE_MAIN_SHA
    assert manifest["name"] == candidate["candidate_id"]
    assert manifest["mode"] == "agent"
    assert candidate["runtime_manifest"]["path"] == "configs/runtime_manifest.json"
    assert candidate["runtime_manifest"]["sha256"] == hashlib.sha256(manifest_bytes).hexdigest()
    assert candidate["runtime_manifest"]["instruction_sha256"] == hashlib.sha256(
        manifest["instruction"].encode("utf-8")
    ).hexdigest()

    parent_manifest_bytes = _git_bytes(BASE_MAIN_SHA, "configs/runtime_manifest.json")
    parent_manifest = _load_json_bytes(parent_manifest_bytes)
    parent_candidate = _load_json_bytes(
        _git_bytes(BASE_MAIN_SHA, "configs/current_candidate.json")
    )
    parent_skill_ids = _skill_blobs_at(BASE_MAIN_SHA)
    assert parent_candidate["candidate_id"] == PARENT_CANDIDATE_ID
    assert parent_manifest["name"] == PARENT_CANDIDATE_ID
    assert candidate["parent_identity"] == {
        "runtime_manifest_sha256": hashlib.sha256(parent_manifest_bytes).hexdigest(),
        "instruction_sha256": hashlib.sha256(
            parent_manifest["instruction"].encode("utf-8")
        ).hexdigest(),
        "skills": parent_skill_ids,
    }

    skill_entries = candidate["skills"]
    assert len(skill_entries) == 4
    assert {entry["name"] for entry in skill_entries} == EXPECTED_SKILLS
    current_skill_ids = {entry["name"]: entry["git_blob"] for entry in skill_entries}
    parent_skill_map = {entry["name"]: entry["git_blob"] for entry in parent_skill_ids}
    for entry in skill_entries:
        path = ROOT / entry["path"]
        assert entry["path"] == f"skills/{entry['name']}/SKILL.md"
        assert entry["git_blob"] == _git_blob_id(path)
    assert current_skill_ids["structured-state-board"] != parent_skill_map["structured-state-board"]
    assert current_skill_ids["rolling-planning"] != parent_skill_map["rolling-planning"]
    assert current_skill_ids["delivery-progress"] == parent_skill_map["delivery-progress"]
    assert current_skill_ids["risk-review"] == parent_skill_map["risk-review"]

    actual_skill_dirs = {
        child.name
        for child in (ROOT / "skills").iterdir()
        if child.is_dir() and (child / "SKILL.md").is_file()
    }
    assert actual_skill_dirs == EXPECTED_SKILLS
    architecture = candidate["architecture"]
    assert architecture["skill_count"] == 4
    assert set(architecture["active_skills"]) == EXPECTED_SKILLS
    assert architecture["action_submitter"] == "Single Agent"
    assert architecture["memory"] == "NOT_IMPLEMENTED"
    assert architecture["fifth_skill"] == "DEFERRED"
    assert architecture["team_swarm"] == "DEFERRED"
    assert candidate["design_intent"] == "HIERARCHICAL_LONG_HORIZON_REALIZATION_POLICY"
    assert all(value is False for value in candidate["validation"].values())

    parent_adopted = set(parent_candidate["adopted_mechanisms"])
    assert parent_adopted <= set(candidate["adopted_mechanisms"])
    assert NEW_MECHANISMS <= set(candidate["adopted_mechanisms"])
    assert set(parent_candidate["runtime_contract_delta"]) <= set(
        candidate["runtime_contract_delta"]
    )
    assert "HIERARCHICAL_GLOBAL_DECISION_ORDER" in candidate["runtime_contract_delta"]


def test_four_skill_frontmatter_and_ownership_boundaries() -> None:
    board = (ROOT / "skills/structured-state-board/SKILL.md").read_text(encoding="utf-8")
    planning = (ROOT / "skills/rolling-planning/SKILL.md").read_text(encoding="utf-8")
    delivery = (ROOT / "skills/delivery-progress/SKILL.md").read_text(encoding="utf-8")
    risk = (ROOT / "skills/risk-review/SKILL.md").read_text(encoding="utf-8")

    for name in sorted(EXPECTED_SKILLS):
        skill_dir = ROOT / "skills" / name
        assert validate_skill_frontmatter(skill_dir) == []
        content = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
        assert "Can Submit Action: No" in content

    assert "CurrentLevelDuration" in board and "duration_in_level" in board
    assert "UNKNOWN" in board and "不得从月份" in board
    assert "Planning 负责策略" in board
    assert "strategy owner" in planning
    assert "Planning must not create, overwrite, or complete Delivery state" in planning
    assert "strategy owner" in delivery and "Primary Gap" in delivery
    assert "risk-review" in risk


def test_manifest_preserves_control_order_action_and_recovery_invariants() -> None:
    manifest = _load_json(ROOT / "configs/runtime_manifest.json")
    instruction = manifest["instruction"]
    parent_manifest = _load_json_bytes(_git_bytes(BASE_MAIN_SHA, "configs/runtime_manifest.json"))

    first_action = instruction.split("首个 action 前", 1)[1].splitlines()[0]
    skill_order = [
        "structured-state-board",
        "rolling-planning",
        "delivery-progress",
        "risk-review",
    ]
    positions = [first_action.index(name) for name in skill_order]
    assert positions == sorted(positions)

    flow = instruction.split("每次决策：", 1)[1].splitlines()[0]
    markers = [
        "fresh observe",
        "Board",
        "Delivery",
        "Planning",
        "legal candidate",
        "Risk gate",
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

    for marker in (
        "participant-visible public facts",
        "合法选项",
        "每个 state-changing action 后必须 fresh observe",
        "[CTRL G=<gap|?> P=<A|S|?> R=<PASS|ALLOW|WARN|RECONSIDER|UNKNOWN> X=<0|1|->]",
        "RECONSIDER 最多比较一个直接相关合法 alternative",
        "X=1 且 R=RECONSIDER 保持",
        "未完成时 X=0，禁止提交",
        "Energy 每次只传一个整数",
        "take_action 后 fresh observe",
        "最终 Risk gate 后若没有新 fresh observe/tool result/event/public evidence",
        "不重开",
        "不盲目重发",
    ):
        assert marker in instruction

    recovery = instruction.split("Recovery epoch", 1)[1]
    assert "同一 game_session_id" in recovery
    assert "fresh observe" in recovery
    assert "当前 session public evidence" in recovery
    assert "UNKNOWN" in recovery
    assert "Skill" in recovery
    assert "game_session_id" in recovery

    assert len(instruction) < len(parent_manifest["instruction"]) * 0.6
    assert "CURRENT_REVIEW_WINDOW" not in instruction
    assert "COMMITMENT_LOAD" not in instruction
    assert "Evidence-first / truthfulness" not in instruction
    assert "Planning" in instruction
    assert "LIGHT / MEANINGFUL / CONGESTED" not in instruction


def test_hierarchical_policy_covers_public_tenure_review_timing_and_commitments() -> None:
    candidate = _load_json(ROOT / "configs/current_candidate.json")
    manifest = _load_json(ROOT / "configs/runtime_manifest.json")
    board = (ROOT / "skills/structured-state-board/SKILL.md").read_text(encoding="utf-8")
    planning = (ROOT / "skills/rolling-planning/SKILL.md").read_text(encoding="utf-8")
    policy = planning + "\n" + manifest["instruction"]

    layer_positions = [
        planning.index(f"### Layer {number}")
        for number in range(8)
    ]
    assert layer_positions == sorted(layer_positions)
    global_order = manifest["instruction"].split("Global priority kernel", 1)[1].splitlines()[0]
    ordered_markers = [
        "binding public constraints",
        "Promotion Frontier / one Primary Gap",
        "current review-window realization",
        "global compounding / actual remaining horizon",
        "commitment efficiency / time-to-realization",
        "near-tie Story semantic priors",
        "candidate-specific Risk gate",
    ]
    positions = [global_order.index(marker) for marker in ordered_markers]
    assert positions == sorted(positions)

    for marker in (
        "CurrentLevelDuration",
        "duration_in_level",
        "fresh",
        "UNKNOWN",
        "不得从月份",
    ):
        assert marker in board
    for marker in (
        "CurrentLevelDuration / duration_in_level",
        "qualitative progression context",
        "duration 只作当前职级 tenure context",
        "不估计阈值",
        "Time-to-Realization",
        "CURRENT_REVIEW_WINDOW",
        "LATER_WINDOW",
        "BEYOND_VISIBLE_HORIZON",
        "UNKNOWN",
        "Commitment Load",
        "LIGHT / MEANINGFUL / CONGESTED / UNKNOWN",
        "不设数量阈值",
        "不持久化 enum/telemetry",
        "Survival readiness",
        "Progression realization readiness",
        "close / deliver / verify / recognize",
        "blocked",
        "剩余 horizon",
        "Long remaining horizon",
        "Intermediate horizon",
        "Short remaining horizon",
        "near-tie",
        "candidate-specific Risk gate",
        "两个相邻 comparable checkpoints",
        "observed effect",
        "advertised effect",
    ):
        assert marker.lower() in policy.lower()

    assert "deadline/action count" in planning.lower() or "数量阈值" in planning
    assert "fixed promotion month" in manifest["instruction"]
    assert "fixed commitment count" in manifest["instruction"]
    assert "fixed commitment count/action ratio/Energy bundle" in manifest["instruction"]
    assert "event/title/keyword/choice lookup" in manifest["instruction"]

    adopted = set(candidate["adopted_mechanisms"])
    assert NEW_MECHANISMS <= adopted
    assert {
        "PUBLIC_PROMOTION_FRONTIER_DIAGNOSIS",
        "CROSS_DIMENSION_PROGRESSION_BOTTLENECK",
        "GLOBAL_MARGINAL_VALUE_AWARENESS",
        "EARLY_HORIZON_PROGRESSION_BIAS",
        "EXPLICIT_PUBLIC_AFFORDABILITY_CONSTRAINT",
        "EVENT_AGNOSTIC_STORY_SEMANTIC_PRIORS",
        "FACT_GROUNDED_ACCOUNTABLE_HANDLING",
        "CLEAR_OWNERSHIP_AND_OBSERVABLE_CHECKPOINT",
        "REVERSIBILITY_AND_OPTIONALITY_PRIOR",
        "PROPORTIONAL_ESCALATION",
    } <= adopted
    for preserved_marker in (
        "affordability crisis",
        "无力支付",
        "soft cost",
        "Energy",
        "Main",
        "Delivery lifecycle",
        "STALLED",
        "advertised effect",
        "DECISION_CLOSED",
        "Recovery",
    ):
        assert preserved_marker.lower() in policy.lower()


def test_static_scenarios_cover_horizon_readiness_dominance_and_near_ties() -> None:
    planning = (ROOT / "skills/rolling-planning/SKILL.md").read_text(encoding="utf-8")
    lower = planning.lower()

    # Long horizon: growth can compound when public constraints permit it.
    assert "long remaining horizon" in lower
    assert "risk budget" in lower and "available" in lower
    assert "binding compliance/survival constraint" in lower
    assert "relative attractiveness" in lower or "相对优先级" in planning

    # Before review: test both survival and progression realization.
    assert "survival readiness" in lower
    assert "progression realization readiness" in lower
    assert "delivery / evidence / recognition" in lower
    assert "activity" in lower and "result" in lower

    # Short horizon: prefer realizable value without a fixed phase month.
    assert "short remaining horizon" in lower
    assert "beyond_visible_horizon" in lower
    assert "actual remaining public horizon" in lower
    assert "m36/m42" in lower and "terminal phase" in lower

    # Close-before-open has explicit exceptions for blocked or superior new paths.
    assert "close / deliver / verify / recognize" in lower
    assert "old item blocked" in lower or "blocked" in lower
    assert "opportunity" in lower
    assert "global marginal value" in lower
    assert "remaining horizon" in lower

    # Story priors distinguish near ties while preserving stronger public Growth.
    assert "progression value 接近" in planning or "outcome 不确定" in planning
    assert "明显更高公开 growth value" in lower
    assert "它不作为 growth 的默认刹车" in lower
    assert "severity" in lower and "escalation" in lower


def test_candidate_and_policy_reject_thresholds_lookups_and_persistence_expansion() -> None:
    candidate = _load_json(ROOT / "configs/current_candidate.json")
    manifest = _load_json(ROOT / "configs/runtime_manifest.json")
    planning = (ROOT / "skills/rolling-planning/SKILL.md").read_text(encoding="utf-8")
    board = (ROOT / "skills/structured-state-board/SKILL.md").read_text(encoding="utf-8")
    audited = planning + "\n" + board + "\n" + manifest["instruction"]
    all_metadata = json.dumps(candidate, ensure_ascii=False).upper()

    for rejected in (
        "FIXED_DURATION_IN_LEVEL_THRESHOLD",
        "FIXED_PHASE_MONTHS",
        "FIXED_COMMITMENT_COUNT_THRESHOLD",
        "FIXED_LATE_HORIZON_MONTH",
        "FIXED_TIME_TO_REALIZATION_MAPPING",
        "EVENT_ID_OR_TITLE_TO_CHOICE_LOOKUP",
    ):
        assert rejected in candidate["rejected_mechanisms"]

    for pattern in (
        r"\b(?:duration_in_level|CurrentLevelDuration)\s*(?:>=|<=|≥|≤|=|>|<)\s*\d+",
        r"\b(?:commitment|active item|项目)\s*(?:>=|<=|≥|≤|=|>|<)\s*\d+",
        r"(?:^|\n)\s*(?:M|Month)\s*\d{1,2}\s*(?:must|必须|→)\s*",
        r"\b(?:cap|封顶)\s*(?:=|:|≥|<=|>=)\s*\d+",
    ):
        assert re.search(pattern, audited, flags=re.IGNORECASE) is None

    forbidden = (
        "DURABLE_OR_CROSS_GAME_MEMORY",
        "FIFTH_SKILL",
        "TEAM_OR_SWARM",
        "FIXED_ACTION_PRIORITY_RANKING",
        "EVENT_ID_OR_TITLE_TO_CHOICE_LOOKUP",
    )
    for item in forbidden:
        assert item in all_metadata
    assert candidate["architecture"]["skill_count"] == 4
    assert candidate["architecture"]["memory"] == "NOT_IMPLEMENTED"
    assert candidate["architecture"]["team_swarm"] == "DEFERRED"
    assert all(value is False for value in candidate["validation"].values())
