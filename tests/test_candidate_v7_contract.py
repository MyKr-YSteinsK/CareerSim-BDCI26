"""Static identity and inherited strategy-contract checks for the current Candidate."""

import hashlib
import json
import subprocess
from pathlib import Path

from career_sim_runner.skill_contract import validate_skill_frontmatter


ROOT = Path(__file__).resolve().parents[1]
BASE_MAIN_SHA = "591ce8a203c4e7dda18ced9031c4c2bf6b4c844a"
PARENT_CANDIDATE_ID = "candidate-v7t-execution-semantic-repair"
CURRENT_CANDIDATE_ID = "candidate-v7u-runtime-adherence-protocol"
SKILL_ORDER = (
    "structured-state-board",
    "rolling-planning",
    "delivery-progress",
    "risk-review",
)
EXPECTED_SKILLS = set(SKILL_ORDER)


def _json(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def _skill(name: str) -> str:
    return (ROOT / f"skills/{name}/SKILL.md").read_text(encoding="utf-8")


def _git_bytes(revision: str, path: str) -> bytes:
    return subprocess.check_output(["git", "show", f"{revision}:{path}"], cwd=ROOT)


def _git_blob_id(path: str) -> str:
    return subprocess.check_output(
        ["git", "hash-object", f"--path={path}", str(ROOT / path)],
        cwd=ROOT,
        text=True,
    ).strip()


def _section(text: str, start: str, end: str) -> str:
    start_index = text.index(start)
    end_index = text.index(end, start_index + len(start))
    return text[start_index:end_index]


def test_candidate_identity_hashes_parent_manifest_and_four_skill_blobs() -> None:
    candidate = _json("configs/current_candidate.json")
    manifest_path = ROOT / "configs/runtime_manifest.json"
    manifest_bytes = manifest_path.read_bytes()
    manifest = json.loads(manifest_bytes.decode("utf-8"))
    parent = json.loads(_git_bytes(BASE_MAIN_SHA, "configs/current_candidate.json"))
    parent_manifest_bytes = _git_bytes(BASE_MAIN_SHA, "configs/runtime_manifest.json")
    parent_manifest = json.loads(parent_manifest_bytes.decode("utf-8"))
    parent_skills = [
        {
            "name": name,
            "git_blob": subprocess.check_output(
                ["git", "rev-parse", f"{BASE_MAIN_SHA}:skills/{name}/SKILL.md"],
                cwd=ROOT,
                text=True,
            ).strip(),
            "path": f"skills/{name}/SKILL.md",
        }
        for name in SKILL_ORDER
    ]

    assert candidate["candidate_id"] == CURRENT_CANDIDATE_ID
    assert candidate["parent_candidate_id"] == PARENT_CANDIDATE_ID
    assert candidate["base_main_sha"] == BASE_MAIN_SHA
    assert candidate["status"] == "STATIC_IMPLEMENTED_NOT_RUNTIME_VALIDATED"
    assert candidate["decision"] == "S08_10_RUNTIME_ADHERENCE_PROTOCOL_REPAIR"
    assert manifest["name"] == CURRENT_CANDIDATE_ID
    assert manifest["mode"] == "agent"
    assert len(manifest["instruction"]) <= 5200
    assert candidate["runtime_manifest"]["sha256"] == hashlib.sha256(manifest_bytes).hexdigest()
    assert candidate["runtime_manifest"]["instruction_sha256"] == hashlib.sha256(
        manifest["instruction"].encode("utf-8")
    ).hexdigest()

    assert parent["candidate_id"] == PARENT_CANDIDATE_ID
    assert parent_manifest["name"] == PARENT_CANDIDATE_ID
    assert candidate["parent_identity"] == {
        "runtime_manifest_sha256": parent["runtime_manifest"]["sha256"],
        "instruction_sha256": parent["runtime_manifest"]["instruction_sha256"],
        "skills": parent_skills,
    }
    parent_manifest_hashes = {
        hashlib.sha256(parent_manifest_bytes).hexdigest(),
        hashlib.sha256(parent_manifest_bytes.replace(b"\n", b"\r\n")).hexdigest(),
    }
    assert candidate["parent_identity"]["runtime_manifest_sha256"] in parent_manifest_hashes

    entries = candidate["skills"]
    assert {entry["name"] for entry in entries} == EXPECTED_SKILLS
    assert len(entries) == 4
    assert {entry["git_blob"] for entry in entries} == {
        _git_blob_id(entry["path"]) for entry in entries
    }
    assert candidate["strategy_delta"] == "RUNTIME_ADHERENCE_PROTOCOL_ONLY"
    assert candidate["design_intent"] == "HIGH_CEILING_WITH_RECOVERABLE_FAILURE_FLOOR"
    assert candidate["runtime_contract_delta"] == [
        "FRESH_OBSERVE_CONTROL_STATE",
        "EXPLICIT_RECONSIDER_BRANCH_ENUM",
        "NAMED_DELIVERY_CHECKPOINT_ENUM",
        "PER_ACTION_ENERGY_REPLAN",
    ]
    assert candidate["architecture"] == parent["architecture"]
    assert candidate["runner_sha"] == parent["runner_sha"]
    assert candidate["validation"] == {
        "runtime_validated": False,
        "gameplay_validated": False,
        "provider_validated": False,
        "survival_improvement_proven": False,
        "score_improvement_proven": False,
        "long_horizon_adherence": False,
        "stable_80_plus_proven": False,
        "hidden_test_transfer_proven": False,
        "next_game_authorized": False,
    }


def test_four_skills_have_valid_frontmatter_chinese_prose_and_fixed_tokens() -> None:
    skill_dirs = {
        child.name
        for child in (ROOT / "skills").iterdir()
        if child.is_dir() and (child / "SKILL.md").is_file()
    }
    assert skill_dirs == EXPECTED_SKILLS

    for name in SKILL_ORDER:
        path = ROOT / "skills" / name / "SKILL.md"
        text = path.read_text(encoding="utf-8")
        assert validate_skill_frontmatter(path.parent) == []
        frontmatter = text.split("---", 2)[1]
        assert f"name: {name}" in frontmatter
        assert "description:" in frontmatter
        assert any("\u4e00" <= char <= "\u9fff" for char in text)
        assert "Can Submit Action: No." in text

    board = _skill("structured-state-board")
    delivery = _skill("delivery-progress")
    planning = _skill("rolling-planning")
    risk = _skill("risk-review")
    assert "PROGRESSION_RESPONSE: S=<GAIN|NO_GAIN|UNKNOWN> N=<GAIN|NO_GAIN|UNKNOWN> O=<GAIN|NO_GAIN|UNKNOWN>" in board
    assert "MODE = <A|S>" in planning and "RECOVERY = <NONE|PROGRESSION|RESOURCE|RISK|DELIVERY|UNKNOWN>" in planning
    assert "[DL i=<NONE|D#|UNKNOWN> n=<0-3>" in delivery
    assert "RISK: PASS|ALLOW|WARN|RECONSIDER|UNKNOWN" in risk


def test_review_deficits_route_to_progression_without_automatic_sticky_or_mode_s() -> None:
    board = _skill("structured-state-board")
    planning = _skill("rolling-planning")
    manifest = _json("configs/runtime_manifest.json")["instruction"]

    board_review = board[: board.index("## PROGRESSION_RESPONSE")]
    for marker in ("低绩效", "`no-promotion`", "普通绩效不足", "单独不能形成 binding `STICKY`"):
        assert marker in board_review
    assert "只有 fresh public evidence 明确显示尚未解除的重大约束时才进入" in board_review

    progression = _section(planning, "### `PROGRESSION`", "### `RESOURCE`")
    assert "低绩效、`no-promotion`" in progression
    assert "### `PROGRESSION`" in progression
    assert "保持 `MODE=A`" in progression
    mode = _section(planning, "## MODE", "## Progression Routing")
    for marker in ("低绩效", "`no-promotion`", "weak Skill / Network / Output", "不能触发 `MODE=S`"):
        assert marker in mode
    assert "只有 fresh public evidence 明确显示 material survival / safety / job-continuity / trust / compliance / confidentiality / affordability / income-continuity constraint" in mode
    assert "低绩效、`no-promotion`" in manifest
    assert "不是 `MODE=S`" in manifest
    assert "在 A 中修复绩效和晋升" in manifest


def test_material_job_threat_can_bind_and_performance_repair_can_relieve_it() -> None:
    board = _skill("structured-state-board")
    planning = _skill("rolling-planning")
    manifest = _json("configs/runtime_manifest.json")["instruction"]

    assert "明确 dismissal / job-continuity threat" in board
    assert "只有 fresh public evidence 明确表明" in board
    resource = _section(planning, "### `RESOURCE`", "### `RISK`")
    assert "重大 binding constraint" in resource
    assert "只做解除当前约束所需的最小合理动作" in resource
    assert "约束已解除或场景结束；立即回 `MODE=A`，恢复原 `REVIEW_PLAN`" in resource
    assert "job-continuity threat" in planning
    assert "直接修复绩效、完成关键交付或恢复晋升成长" in planning
    assert "不得把 `S` 机械理解为低调、停止成长" in planning
    assert "job-continuity threat" in manifest
    assert "直接修复绩效或交付属于 constraint relief" in manifest


def test_progression_response_tracks_clean_gain_no_gain_reset_and_multidimensional_value() -> None:
    board = _skill("structured-state-board")
    planning = _skill("rolling-planning")
    response = _section(board, "## PROGRESSION_RESPONSE", "## EFFECTS")
    for marker in (
        "紧邻 fresh observe 中该维度真实增加",
        "满足清晰归因条件，但该维度保持不变",
        "其它维度沿用上一版同局 Board",
        "后续 clean `GAIN` 覆盖旧 `NO_GAIN`",
        "Level 改变时，`S/N/O` 全部重置为 `UNKNOWN`",
        "session 改变时全部重置",
        "不得推断 cap、threshold、formula、eligibility 或 hidden cause",
    ):
        assert marker in response
    routing = _section(planning, "## Progression Routing", "## Ranking")
    assert "一个维度 `NO_GAIN` 不抹掉其它 `GAIN/UNKNOWN` 价值" in routing
    assert "不立即重复同一个 no-gain 投入" in routing
    assert "Level change 后所有 response 重新开放" in routing
    assert "Skill 不因 terminal-score saturation 假设被降权" in routing


def test_non_specific_coverage_exempts_current_level_no_gain_until_reset() -> None:
    planning = _skill("rolling-planning")
    routing = _section(planning, "## Progression Routing", "## Ranking")

    assert "只对当前 `GAIN/UNKNOWN` 的 Skill / Network / Output 维度维持 coverage" in routing
    assert "不得因另一维最近更显著而长期忽略仍为 `GAIN/UNKNOWN` 的维度" in routing
    assert "当前 Level 的 `NO_GAIN` 维度不受 coverage 义务约束" in routing
    assert "直到 Level change 或后续 clean `GAIN` 重置/覆盖" in routing
    scenario = {"S": "GAIN", "N": "UNKNOWN", "O": "NO_GAIN"}
    coverage_candidates = {
        dimension for dimension, response in scenario.items() if response in {"GAIN", "UNKNOWN"}
    }
    assert coverage_candidates == {"S", "N"}
    assert "O" not in coverage_candidates
    after_clean_gain = {**scenario, "O": "GAIN"}
    assert "O" in {
        dimension for dimension, response in after_clean_gain.items() if response in {"GAIN", "UNKNOWN"}
    }
    after_level_change = dict.fromkeys(scenario, "UNKNOWN")
    assert set(after_level_change) == {
        dimension
        for dimension, response in after_level_change.items()
        if response in {"GAIN", "UNKNOWN"}
    }


def test_review_window_preserves_promotion_readiness_and_checkpoint() -> None:
    planning = _skill("rolling-planning")
    review_window = _section(planning, "## 长期规划一致性", "## Failure Recovery Contract")
    assert "良好绩效 + `no-promotion` 仍表示 promotion readiness 未完成" in review_window
    assert "下一次公开正式 Review 是当前准备 checkpoint" in review_window
    routing = _section(planning, "## Progression Routing", "## Ranking")
    assert "Skill 不因 terminal-score saturation 假设被降权" in routing
    assert "它始终可能具有 promotion value" in routing


def test_risk_recovery_cleanup_is_bounded_and_risk_does_not_replan() -> None:
    planning = _skill("rolling-planning")
    risk = _skill("risk-review")
    manifest = _json("configs/runtime_manifest.json")["instruction"]
    cleanup = _section(planning, "### `RISK`", "### `DELIVERY`")
    assert "fresh public warning 明确表示风险 elevated / accumulating / needs handling" in cleanup
    assert "存在明确 reparative legal option" in cleanup
    assert "一次 bounded cleanup" in cleanup
    assert "完成一次 cleanup 后必须 fresh observe，并默认回长期主线" in cleanup
    assert "同一风险仍未解除/再次 elevated" in cleanup
    assert "出现新的同类 warning" in cleanup
    assert "无关的新 evidence 不得重置限制" in cleanup
    assert "在下一 Review 前允许一次 bounded cleanup" in cleanup
    cleanup_exit = (
        "完成一次 cleanup 后必须 fresh observe，并默认回长期主线。只有后续 fresh public evidence "
        "明确表明同一风险仍未解除/再次 elevated，或出现新的同类 warning，才允许再次 cleanup；"
        "无关的新 evidence 不得重置限制"
    )
    assert cleanup_exit in cleanup
    assert cleanup_exit in manifest
    assert "只有风险升级为 material survival / job-continuity / trust / compliance / confidentiality crisis 时才进入 `MODE=S`" in cleanup
    assert "不重新做 candidate ranking" in risk
    assert "一个 public warning 允许 Planning 考虑 bounded cleanup，不等于 Risk 自动 `RECONSIDER`" in risk


def test_planning_explicitly_uses_current_participant_visible_event_semantics() -> None:
    planning = _skill("rolling-planning")
    evidence = _section(planning, "## 证据优先级", "## 长期规划一致性")
    mode = _section(planning, "## MODE", "## Progression Routing")

    assert "最新 fresh observe 中参与者可见的 event 描述与合法 choice 语义" in evidence
    assert "结合 Board 与当前 participant-visible event/choice 语义" in mode
    assert "尚未解除的 binding constraint" in mode
    assert "不得只根据状态数字或旧 Review 判断" in mode


def test_delivery_tracks_before_first_review_and_receipts_do_not_verify_results() -> None:
    delivery = _skill("delivery-progress")
    planning = _skill("rolling-planning")
    pre_review = _section(delivery, "## 职责", "## Lifecycle")
    assert "第一次正式 Review 前若尚无有效 `REVIEW_PLAN`" in pre_review
    assert "当前公开 commitment、近期 checkpoint" in pre_review
    assert "第一次正式 Review 后" in pre_review
    assert "receipt 只证明工具执行，不证明 career result" in delivery
    assert "不能单独验证交付" in delivery
    recovery = _section(planning, "### `DELIVERY`", "## MODE")
    assert "### `DELIVERY`" in recovery
    assert "优先完成、验证或修复高价值近端交付" in recovery
    assert "Planning 可以把完成或验证它作为 `RECOVERY=DELIVERY`" in delivery


def test_manifest_preserves_whole_game_persistence_preflight_and_recovery_order() -> None:
    manifest = _json("configs/runtime_manifest.json")["instruction"]
    assert "structured game state 仍 active 时，在同一 assistant execution 中持续运行工具循环" in manifest
    assert "`DECISION_CLOSED` 只关闭当前 action selection，不结束 assistant execution" in manifest
    assert "每次 successful take_action 后立即 fresh observe 并进入下一决策" in manifest
    assert "不得因为 action、month、quarter、Review、promotion、局部 closure" in manifest
    assert "CONTROL_STATE=READY|OBSERVE_REQUIRED|BLOCKED" in manifest
    assert "successful `take_action`" in manifest
    assert "唯一合法的下一 gameplay call 是同一 session 的 fresh `observe`" in manifest
    assert "[CTRL G=<gap|?> P=<A|S|?> R=<PASS|ALLOW|WARN|RECONSIDER|UNKNOWN> RB=<NONE|DONE|BLOCKED>]" in manifest
    assert "checkpoint=<NEAR|NOT_NEAR|UNKNOWN>" in manifest
    assert "CONTROL_STATE=READY" in manifest and "RB in {NONE,DONE}" in manifest

    recovery = manifest[manifest.index("CONTEXT RECOVERY"):]
    ordered = (
        "确认同一 game_session_id",
        "fresh observe",
        "依次重读四个 Skills",
        "重建 Board",
        "重建 Delivery 或 UNKNOWN",
        "从同局公开证据恢复",
        "RECOVERY_READY",
    )
    assert [recovery.index(item) for item in ordered] == sorted(recovery.index(item) for item in ordered)
    assert "identity、observe 或 Skill reread 失败时保持 pending，不提交动作" in recovery


def test_evidence_firewall_and_no_fixed_hidden_rules_are_explicit() -> None:
    candidate = _json("configs/current_candidate.json")
    runtime = _json("configs/runtime_manifest.json")["instruction"] + "\n" + "\n".join(
        _skill(name) for name in SKILL_ORDER
    )
    for marker in ("HiddenRisk", "hidden counters", "internal score", "internal event id/effect", "EXCLUDE_FROM_STRATEGY"):
        assert marker in runtime
    for rejected in (
        "EXACT_DEV_SCORE_WEIGHTS_IN_RUNTIME",
        "EXACT_PROMOTION_OR_HIDDEN_RISK_THRESHOLDS",
        "EVENT_ID_OR_TITLE_TO_CHOICE_LOOKUP",
        "FIXED_STORY_ANSWER",
        "HIDDEN_CAP_INFERENCE_FROM_NO_GAIN",
    ):
        assert rejected in candidate["rejected_mechanisms"]
    assert "不得推断隐藏 threshold/cap/weight" in runtime
    assert "固定事件答案" in runtime


def test_board_runner_and_dependency_files_remain_frozen() -> None:
    candidate = _json("configs/current_candidate.json")
    board = "skills/structured-state-board/SKILL.md"
    assert (ROOT / board).read_bytes() == _git_bytes(BASE_MAIN_SHA, board)
    for relative in ("pyproject.toml", "uv.lock", "career_sim_runner"):
        changed = subprocess.check_output(
            ["git", "diff", "--name-only", BASE_MAIN_SHA, "--", relative],
            cwd=ROOT,
            text=True,
        ).strip()
        assert changed == ""
    assert candidate["runner_sha"] == "f61c738c72e51b77298cc1c14c7c6ebf4b6c527d"

    state = (ROOT / "docs/project/CURRENT_STATE.md").read_text(encoding="utf-8")
    assert f"Current Candidate: {CURRENT_CANDIDATE_ID}" in state
    assert "NEXT_GAME = NOT_AUTHORIZED" in state
