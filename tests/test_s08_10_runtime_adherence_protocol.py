"""Offline contract and regression checks for S08-10 v7u."""

import json
import subprocess
from pathlib import Path

from scripts.s08_09_runtime_contract_forensics import analyze as analyze_run03


ROOT = Path(__file__).resolve().parents[1]
BASE = "591ce8a203c4e7dda18ced9031c4c2bf6b4c844a"
V7V_BASE = "882d47202d4d8d8305acbf7edb451ee8d68fe1ce"
SKILLS = ("structured-state-board", "rolling-planning", "delivery-progress", "risk-review")


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def _json(path: str) -> dict:
    return json.loads(_read(path))


def _base_text(path: str) -> str:
    return subprocess.check_output(["git", "show", f"{BASE}:{path}"], cwd=ROOT, text=True, encoding="utf-8")


def test_executor_control_state_is_explicit_and_cross_file_consistent() -> None:
    manifest = _json("configs/runtime_manifest.json")["instruction"]
    runtime = _read("docs/project/AGENT_RUNTIME_CONTRACT.md")
    risk = _read("skills/risk-review/SKILL.md")
    delivery = _read("skills/delivery-progress/SKILL.md")

    state_steps = (
        "`CONTROL_STATE=READY|OBSERVE_REQUIRED|BLOCKED` 由执行器维护",
        "successful `take_action` 消耗 READY 与单次 preflight",
        "下一 gameplay call 只能同 session fresh `observe`",
        "fresh observe 后重建 Board",
        "action 失败/未知、observe 失败、session mismatch",
    )
    assert all(step in manifest for step in state_steps)
    assert [manifest.index(step) for step in state_steps] == sorted(manifest.index(step) for step in state_steps)
    assert "Its `{success,error}` receipt has no fresh public state" in runtime
    assert "only next gameplay call is a same-session fresh `observe`" in runtime
    assert "`CONTROL_STATE=READY`" in risk
    assert "`RECOVERY_PENDING` 保持 `CONTROL_STATE=BLOCKED`" in manifest
    assert "`RECOVERY_READY` 不授权 action" in manifest

    ctrl_v2 = "[CTRL G=<gap|?> P=<A|S|?> R=<PASS|ALLOW|WARN|RECONSIDER|UNKNOWN> RB=<NONE|DONE|BLOCKED>]"
    dl_v2 = "[DL i=<NONE|D#|UNKNOWN> n=<0-3> focus=<NONE|OPPORTUNITY|COMMITTED|IN_PROGRESS|BLOCKED|DELIVERY_CLAIMED|DELIVERED|UNKNOWN> evidence=<NA|UNKNOWN|UNVERIFIED|PUBLICLY_VERIFIED> checkpoint=<NEAR|NOT_NEAR|UNKNOWN> recognition=<0|1|?>]"
    assert ctrl_v2 in manifest and ctrl_v2 in risk
    assert dl_v2 in manifest and dl_v2 in delivery
    current_runtime_contract = "\n".join((manifest, runtime, risk, delivery))
    assert "X=" not in current_runtime_contract
    assert "RB=NONE" in risk and "RB=DONE" in risk and "RB=BLOCKED" in risk
    assert "RB in {NONE,DONE}" in manifest


def test_quarterly_energy_invalidates_batch_intent_after_fresh_no_gain() -> None:
    planning = _read("skills/rolling-planning/SKILL.md")
    start = planning.index("## Quarterly Control")
    end = planning.index("## Decision Budget", start)
    quarter = planning[start:end]

    assert "QUARTER_INTENT = <MODE | current target>" in quarter
    assert "不得预先承诺剩余 Energy 的动作数量、选择序列或固定批次" in quarter
    ordered = (
        "fresh same-session observe",
        "Board rebuild and PROGRESSION_RESPONSE update",
        "Delivery rebuild",
        "new Planning pass for remaining Energy",
        "Risk and executor preflight",
        "submit exactly one action",
        "CONTROL_STATE=OBSERVE_REQUIRED",
    )
    assert [quarter.index(step) for step in ordered] == sorted(quarter.index(step) for step in ordered)
    assert "丢弃旧剩余动作意图" in quarter
    assert "Energy=3、Output=26" in quarter
    assert "第二次 immediate Report Preparation 不符合合同" in quarter
    assert "不立即重复同一个 no-gain 投入" in planning


def test_v7t_strategy_and_frozen_surfaces_are_preserved() -> None:
    candidate = _json("configs/current_candidate.json")
    parent = json.loads(subprocess.check_output(["git", "show", f"{BASE}:configs/current_candidate.json"], cwd=ROOT))
    assert candidate["strategy_delta"] == "RUNTIME_GATE_ORDERING_CORRECTION_ONLY"
    assert candidate["adopted_mechanisms"] == parent["adopted_mechanisms"]
    assert candidate["rejected_mechanisms"] == parent["rejected_mechanisms"]
    assert candidate["architecture"] == parent["architecture"]
    assert candidate["runner_sha"] == parent["runner_sha"]

    board = "skills/structured-state-board/SKILL.md"
    assert (ROOT / board).read_bytes() == subprocess.check_output(["git", "show", f"{BASE}:{board}"], cwd=ROOT)

    base_planning = _base_text("skills/rolling-planning/SKILL.md")
    current_planning = _read("skills/rolling-planning/SKILL.md")
    assert base_planning.split("## Quarterly Control", 1)[0] == current_planning.split("## Quarterly Control", 1)[0]
    assert base_planning.split("## Decision Budget", 1)[1] == current_planning.split("## Decision Budget", 1)[1]

    base_delivery = _base_text("skills/delivery-progress/SKILL.md")
    current_delivery = _read("skills/delivery-progress/SKILL.md")
    checkpoint_explanation = "`checkpoint=NEAR` 需要公开证据表明该 item 与当前 Review Window 或 commitment 的 near-term checkpoint 相关；`NOT_NEAR` 表示没有此类公开依据；证据不足时用 `UNKNOWN`。不得用数字倒计时推导 near status。\n\n"
    current_delivery = current_delivery.replace(checkpoint_explanation, "")
    current_delivery = current_delivery.replace("checkpoint=<NEAR|NOT_NEAR|UNKNOWN>", "checkpoint=<0|1|?>")
    current_delivery = current_delivery.replace("checkpoint=NOT_NEAR recognition=0", "checkpoint=0 recognition=0")
    assert current_delivery == base_delivery

    for relative in ("pyproject.toml", "uv.lock", "career_sim_runner"):
        changed = subprocess.check_output(["git", "diff", "--name-only", BASE, "--", relative], cwd=ROOT, text=True).strip()
        assert changed == ""

    planning = current_planning
    risk = _read("skills/risk-review/SKILL.md")
    for invariant in (
        "保持 `MODE=A`",
        "只做解除当前约束所需的最小合理动作",
        "fresh public warning 明确表示风险 elevated / accumulating / needs handling",
        "完成一次 cleanup 后必须 fresh observe，并默认回长期主线",
        "最新 fresh observe 中参与者可见的 event 描述与合法 choice 语义",
        "hidden threshold/cap",
    ):
        assert invariant in planning or invariant in risk


def test_v7v_candidate_is_unvalidated_and_run03_audit_is_unchanged() -> None:
    candidate = _json("configs/current_candidate.json")
    assert candidate["candidate_id"] == "candidate-v7v-preflight-ordering-repair"
    assert candidate["parent_candidate_id"] == "candidate-v7u-runtime-adherence-protocol"
    assert candidate["base_main_sha"] == V7V_BASE
    assert all(value is False for value in candidate["validation"].values())

    result = analyze_run03(ROOT)
    coverage = result["post_run_audit_replay_after_parser_patch"]["delivery_marker_coverage"]
    assert (coverage["valid"], coverage["malformed_or_duplicate"], coverage["missing"]) == (174, 33, 0)
    assert result["source_identity"]["archived_evidence_unchanged_against_manifest"] is True
    assert result["scope_accounting"]["provider_calls"] == 0
    assert result["scope_accounting"]["games"] == 0
