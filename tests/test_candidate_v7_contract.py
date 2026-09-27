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
BASE_MAIN_SHA = "7b05c492bc5a5083226c4b7a64c1ce9482852941"
PARENT_CANDIDATE_ID = "candidate-v7a-promotion-frontier"
NEW_STORY_MECHANISMS = {
    "EVENT_AGNOSTIC_STORY_SEMANTIC_PRIORS",
    "FACT_GROUNDED_ACCOUNTABLE_HANDLING",
    "CLEAR_OWNERSHIP_AND_OBSERVABLE_CHECKPOINT",
    "REVERSIBILITY_AND_OPTIONALITY_PRIOR",
    "PROPORTIONAL_ESCALATION",
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

    assert candidate["candidate_id"] == "candidate-v7b-semantic-generalization"
    assert candidate["parent_candidate_id"] == PARENT_CANDIDATE_ID
    assert candidate["status"] == "STATIC_IMPLEMENTED_NOT_RUNTIME_VALIDATED"
    assert candidate["base_main_sha"] == BASE_MAIN_SHA
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
    assert parent_candidate["candidate_id"] == PARENT_CANDIDATE_ID
    parent_skill_ids = []
    for entry in parent_candidate["skills"]:
        actual_parent_blob = subprocess.check_output(
            ["git", "rev-parse", f"{candidate['base_main_sha']}:{entry['path']}"],
            cwd=ROOT,
            text=True,
        ).strip()
        assert entry["git_blob"] == actual_parent_blob
        parent_skill_ids.append({"name": entry["name"], "git_blob": actual_parent_blob})
    assert parent_candidate["runtime_manifest"]["sha256"] == hashlib.sha256(parent_manifest_bytes).hexdigest()
    assert parent_candidate["runtime_manifest"]["instruction_sha256"] == hashlib.sha256(
        parent_manifest["instruction"].encode("utf-8")
    ).hexdigest()
    assert candidate["parent_identity"] == {
        "runtime_manifest_sha256": hashlib.sha256(parent_manifest_bytes).hexdigest(),
        "instruction_sha256": hashlib.sha256(parent_manifest["instruction"].encode("utf-8")).hexdigest(),
        "skills": parent_skill_ids,
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
    assert NEW_STORY_MECHANISMS <= set(candidate["adopted_mechanisms"])
    assert "BOUNDED_EVENT_AGNOSTIC_STORY_SEMANTIC_COMPARISON" in candidate["runtime_contract_delta"]


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


def test_story_semantic_priors_stay_bounded_growth_preserving_and_event_agnostic() -> None:
    candidate = _load_json(ROOT / "configs/current_candidate.json")
    manifest = _load_json(ROOT / "configs/runtime_manifest.json")
    planning = (ROOT / "skills/rolling-planning/SKILL.md").read_text(encoding="utf-8")
    runtime_instruction = manifest["instruction"]
    start = planning.index("### 陌生 Story 的事件无关语义比较")
    end = planning.index("\nDECISION_CLOSED：", start)
    story_policy = planning[start:end]

    for heading in (
        "Evidence-first / truthfulness",
        "Accountable direct handling",
        "Ownership / verification",
        "Reversibility / optionality",
        "Proportional escalation",
    ):
        assert heading in story_policy

    for marker in (
        "无 Material Risk",
        "权力滥用",
        "可信报复风险",
        "必须升级",
        "直接处理已失败",
        "超出权限",
        "confidentiality/compliance/safety",
        "不得补造",
        "Delivery 独占 lifecycle state",
        "不因另一候选更礼貌、保守或可逆就自动压掉它",
        "severity、scope、repeated failure",
        "repeated failure",
        "不是第二 strategy owner、Risk gate 或独立 score function",
        "不触发额外 Skill 全文读取或每个 Story 的 FULL checkpoint",
        "event/title/keyword→choice lookup",
        "Dev event catalog",
        "fixed answer",
        "fixed escalation count",
    ):
        assert marker in story_policy

    assert story_policy.index("fresh public facts") < story_policy.index("生成合法候选")
    assert story_policy.index("生成合法候选") < story_policy.index("Risk gate")
    assert "bounded, context-sensitive semantic comparison" in runtime_instruction
    assert "clearly higher public Growth value" in runtime_instruction
    assert "candidate-specific Material Risk gate" in runtime_instruction
    assert "fixed answer" in runtime_instruction.lower()
    assert "fixed escalation count" in runtime_instruction.lower()
    assert "FIXED_STORY_ANSWER" in candidate["rejected_mechanisms"]
    assert "NUMERIC_ESCALATION_LADDER" in candidate["rejected_mechanisms"]
    assert all(value is False for value in candidate["validation"].values())
