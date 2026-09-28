"""Static identity and public-policy contract for the current v7 Candidate."""

import hashlib
import json
import re
import subprocess
from pathlib import Path

from career_sim_runner.skill_contract import validate_skill_frontmatter


ROOT = Path(__file__).resolve().parents[1]
BASE_MAIN_SHA = "7aed55348ce49eded8e14d79fea31ae815092fc9"
PARENT_CANDIDATE_ID = "candidate-v7e-lean-review-controller"
CURRENT_CANDIDATE_ID = "candidate-v7f-promotion-first-survival-floor"
SKILL_ORDER = (
    "structured-state-board",
    "rolling-planning",
    "delivery-progress",
    "risk-review",
)
EXPECTED_SKILLS = set(SKILL_ORDER)
DELIVERY_BLOB = "9a84f723da92971850f167a3eebdc862ff95c20c"
REQUIRED_MECHANISMS = {
    "PROMOTION_FIRST_WITH_SURVIVAL_FLOOR",
    "PRE_REVIEW_BALANCED_SNO_PROGRESSION",
    "FORMAL_REVIEW_ANCHORED_GAP",
    "INCOME_RECOVERY_NOT_PASSIVE_SAFETY",
    "STRONG_BROAD_GROWTH_MAIN_ACTION_PRIOR",
    "TEMPORARY_STABILIZE_THEN_RETURN_TO_ADVANCE",
    "STICKY_PUBLIC_FAILURE_DIRECTION_FACTS",
    "PUBLIC_HINT_SOFT_ONLY",
    "NO_HIDDEN_CAP_FROM_NO_GAIN",
    "BOUNDED_NON_NUMERIC_STORY_SHORTLIST",
    "QUARTER_ENERGY_INTENT",
    "TAKE_ACTION_ARGUMENT_PREFLIGHT",
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


def _deployable_text() -> str:
    paths = [
        ROOT / "skills/structured-state-board/SKILL.md",
        ROOT / "skills/rolling-planning/SKILL.md",
        ROOT / "skills/risk-review/SKILL.md",
        ROOT / "configs/runtime_manifest.json",
        ROOT / "configs/current_candidate.json",
    ]
    return "\n".join(path.read_text(encoding="utf-8") for path in paths)


def _section(text: str, start: str, end: str) -> str:
    start_index = text.index(start)
    end_index = text.index(end, start_index + len(start))
    return text[start_index:end_index]


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
    assert candidate["decision"] == "S07_31R_STATIC_PROMOTION_FIRST_SURVIVAL_FLOOR"
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
    assert current_map["delivery-progress"] == parent_map["delivery-progress"] == DELIVERY_BLOB
    for replaced in ("structured-state-board", "rolling-planning", "risk-review"):
        assert current_map[replaced] != parent_map[replaced]

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
    assert REQUIRED_MECHANISMS <= set(candidate["adopted_mechanisms"])


def test_four_skills_have_valid_frontmatter_and_preserve_ownership() -> None:
    skill_dirs = {
        child.name
        for child in (ROOT / "skills").iterdir()
        if child.is_dir() and (child / "SKILL.md").is_file()
    }
    assert skill_dirs == EXPECTED_SKILLS
    for name in EXPECTED_SKILLS:
        path = ROOT / "skills" / name
        assert validate_skill_frontmatter(path) == []

    board = (ROOT / "skills/structured-state-board/SKILL.md").read_text(encoding="utf-8")
    planning = (ROOT / "skills/rolling-planning/SKILL.md").read_text(encoding="utf-8")
    delivery = (ROOT / "skills/delivery-progress/SKILL.md").read_text(encoding="utf-8")
    risk = (ROOT / "skills/risk-review/SKILL.md").read_text(encoding="utf-8")
    assert "Sticky facts" in board and "UNKNOWN" in board
    assert "strategy owner" in planning.lower()
    assert "lifecycle" in delivery.lower()
    assert "Material Risk" in risk
    assert "不得调用" in board and "take_action" in board
    assert "Planning 不调用" in planning and "take_action" in planning
    assert "Can Submit Action: No" in delivery and "Can Submit Action: No" in risk
    assert _git_blob_id(ROOT / "skills/delivery-progress/SKILL.md") == DELIVERY_BLOB


def test_deployable_policy_uses_public_failure_directions_without_invented_triggers() -> None:
    text = _deployable_text()
    forbidden_claims = (
        r"连续\s*两次.{0,16}(?:D|低绩效).{0,24}(?:解雇|开除|出局|dismiss|fire)",
        r"第二次.{0,12}(?:爆雷|blowup).{0,24}(?:信任危机|dismiss|eliminat)",
        r"(?:Health|Wealth|Network|Dignity|健康|财富|人脉|尊严).{0,16}(?:<=|<|≤|低于|小于)\s*\d+.{0,24}(?:失败|出局|dismiss|eliminat)",
        r"连续\s*\d+\s*个?月.{0,24}(?:失败|出局|终止|dismiss|eliminat)",
    )
    assert not any(re.search(pattern, text, re.IGNORECASE) for pattern in forbidden_claims)
    assert "阈值、计数、连续触发条件不公开" in text or "阈值、计数、连续触发条件" in text
    assert not re.search(r"Risk\s*Budget\s*=\s*TIGHT", text, re.IGNORECASE)


def test_planning_separates_progression_gap_from_temporary_survival_mode() -> None:
    planning = (ROOT / "skills/rolling-planning/SKILL.md").read_text(encoding="utf-8")
    manifest = _load_json(ROOT / "configs/runtime_manifest.json")["instruction"]
    combined = planning + "\n" + manifest

    assert re.search(r"Primary Gap[^\n]{0,50}progression gap", planning, re.IGNORECASE)
    assert "formal review" in planning.lower() and "promotion" in planning.lower()
    assert "普通 Story" in planning and "G" in planning
    assert "P=A" in combined and "P=S" in combined
    assert "临时 Stabilize" in planning or "临时 P=S" in manifest
    assert "回到 P=A" in planning or "解除后立即回 A" in manifest


def test_pre_review_plan_keeps_gap_unknown_and_advances_sno() -> None:
    planning = (ROOT / "skills/rolling-planning/SKILL.md").read_text(encoding="utf-8")
    before_review = _section(planning, "### 第一次 review 之前", "## 2. Default mode")
    assert re.search(r"G\s*=\s*\?", before_review)
    for dimension in ("Skill", "Network", "Output"):
        assert dimension in before_review
    assert "可见交付" in before_review


def test_quarterly_main_action_uses_a_strong_but_nonmandatory_growth_prior() -> None:
    planning = (ROOT / "skills/rolling-planning/SKILL.md").read_text(encoding="utf-8")
    main_action = _section(planning, "### Quarterly Main Action", "## 3. Energy")
    assert "申请关键项目" in main_action
    for dimension in ("Output", "Skill", "Network"):
        assert dimension in main_action
    assert "强默认候选" in main_action
    assert "不是固定答案" in main_action
    assert "review feedback" in main_action.lower() or "formal feedback" in main_action.lower()


def test_wealth_danger_prompts_income_and_progression_recovery() -> None:
    planning = (ROOT / "skills/rolling-planning/SKILL.md").read_text(encoding="utf-8")
    wealth = _section(planning, "### Wealth", "### Health / Dignity")
    assert "Income Recovery Alert" in wealth
    assert "绩效和晋升" in wealth
    assert "月薪" in wealth or "salary" in wealth.lower()
    assert "非必要 Wealth 花费" in wealth
    assert "低调保守模式" in wealth


def test_risk_allows_ordinary_growth_cost_without_material_risk() -> None:
    risk = (ROOT / "skills/risk-review/SKILL.md").read_text(encoding="utf-8")
    assert "普通 workload" in risk
    assert "PASS" in risk
    assert "不能因为 Growth action 有成本就自动拦截" in risk
    assert "Growth action 不因为 Wealth 低就被 Risk 否决" in risk


def test_story_shortlist_is_bounded_by_dominance_not_a_fixed_count() -> None:
    planning = (ROOT / "skills/rolling-planning/SKILL.md").read_text(encoding="utf-8")
    story = _section(planning, "## 9. Story", "## 10. Take-action preflight")
    assert "progression" in story.lower()
    assert "明显更强" in story
    assert "不规定固定 shortlist 数量" in story
    assert not re.search(r"shortlist.{0,24}\b\d+\b|top\s*\d+", story, re.IGNORECASE)


def test_observed_no_gain_does_not_become_a_hidden_cap() -> None:
    planning = (ROOT / "skills/rolling-planning/SKILL.md").read_text(encoding="utf-8")
    assert "OBSERVED_NO_GAIN" in planning
    assert re.search(r"no-gain[^\n]{0,100}(?:不推断|UNKNOWN|unknown)", planning, re.IGNORECASE)
    assert "cap、threshold、formula" in planning


def test_take_action_preflight_requires_one_legal_integer_choice() -> None:
    planning = (ROOT / "skills/rolling-planning/SKILL.md").read_text(encoding="utf-8")
    manifest = _load_json(ROOT / "configs/runtime_manifest.json")["instruction"]
    combined = planning + "\n" + manifest
    assert "当前合法选项中的**一个整数**" in planning
    assert "choice" in combined and "session_id" in combined
    assert "candidate 已最终确定" in planning or "candidate已闭合" in manifest
    assert "notes 首位且仅有一个" in planning or "notes首位且仅一个" in manifest


def test_candidate_and_project_state_record_v7f_without_runtime_claims() -> None:
    candidate = _load_json(ROOT / "configs/current_candidate.json")
    state = (ROOT / "docs/project/CURRENT_STATE.md").read_text(encoding="utf-8")
    decisions = (ROOT / "docs/project/ARCHITECTURE_DECISIONS.md").read_text(encoding="utf-8")

    assert candidate["parent_candidate_id"] == PARENT_CANDIDATE_ID
    assert "S07-31R" in state and CURRENT_CANDIDATE_ID in state
    assert re.search(r"Current Candidate:\s+`candidate-v7f-promotion-first-survival-floor`", state)
    assert "all v7f validation flags are false" in state
    assert "## AD-015" in decisions and "S07-31R" in decisions
    assert "candidate-v7e-lean-review-controller" in decisions
    assert "NEXT_GAME = NOT_AUTHORIZED" in state
    assert "NEXT_GAME = NOT_AUTHORIZED" in decisions
    assert "candidate-v7f-public-survival-controller" not in state + decisions
