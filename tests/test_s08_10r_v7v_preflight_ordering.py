"""Static regression for the v7v acyclic READY/preflight/action contract."""

import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = "882d47202d4d8d8305acbf7edb451ee8d68fe1ce"
V7V_SNAPSHOT = "62b4937af10bd6fd8fea4cc794ac1b986cb7863e"
SKILLS = ("structured-state-board", "rolling-planning", "delivery-progress", "risk-review")


def _text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def _json(path: str) -> dict:
    return json.loads(_text(path))


def _git_bytes(revision: str, path: str) -> bytes:
    return subprocess.check_output(["git", "show", f"{revision}:{path}"], cwd=ROOT)


def test_runtime_graph_is_acyclic_and_preflight_consumes_ready() -> None:
    manifest = _json("configs/runtime_manifest.json")["instruction"]
    contract = _text("docs/project/AGENT_RUNTIME_CONTRACT.md")

    manifest_flow = (
        "fresh observe → Board → Delivery → Planning → final Risk → READY "
        "→ PREFLIGHT=PASS → one take_action → OBSERVE_REQUIRED。"
    )
    assert manifest_flow in manifest
    flow = contract.split("```text\n", 1)[1].split("\n```", 1)[0]
    ordered = (
        "fresh observe",
        "structured-state-board",
        "delivery-progress",
        "rolling-planning",
        "risk-review",
        "CONTROL_STATE=READY",
        "preflight",
        "PREFLIGHT=PASS",
        "exactly one take_action",
        "CONTROL_STATE=OBSERVE_REQUIRED",
    )
    assert [flow.index(step) for step in ordered] == sorted(flow.index(step) for step in ordered)

    assert "preflight 不计入 READY" in manifest
    assert "Preflight is not part of `READY` creation." in contract
    assert "Preflight consumes that existing `READY`." in contract
    assert "CONTROL_STATE=READY" in contract
    assert "same `game_session_id`" in contract
    assert "same fresh observe" in contract
    assert "final `R!=RECONSIDER`" in contract
    assert "`RB in {NONE,DONE}`" in contract
    assert "valid CTRL/DL markers" in contract
    assert "`PREFLIGHT=PASS` authorizes exactly one submission" in contract
    assert "does not create `READY` or a reusable authorization" in contract
    assert "Any failed check sets `BLOCKED` and forbids `take_action`." in contract

    assert "preflight 全部完成后成立" not in manifest
    assert "preflight before returning to `READY`" not in contract


def test_action_consumes_single_use_preflight_and_recovery_rebuilds_ready() -> None:
    manifest = _json("configs/runtime_manifest.json")["instruction"]
    contract = _text("docs/project/AGENT_RUNTIME_CONTRACT.md")

    assert "successful `take_action` 消耗 READY 与单次 preflight" in manifest
    assert "receipt 仅含 success/error、无 public state" in manifest
    assert "不得更新 Board/Delivery 或返回 READY" in manifest
    assert "successful `take_action` consumes the `READY` decision and one-use preflight" in contract
    assert "cannot update Board/Delivery, return `READY`, or authorize another action" in contract
    assert "reuse no candidate or prior state" in contract
    assert "only next gameplay call is a same-session fresh `observe`" in contract
    assert "After that observe, rebuild Board" in contract
    assert "then establish `READY`. Only afterward may a new preflight run." in contract
    assert "`RECOVERY_READY` alone authorizes no action" in contract
    assert "establish `READY`, then run a new preflight" in contract
    assert "`RECOVERY_READY` 不授权 action" in manifest
    assert "→ READY → new preflight" in manifest


def test_v7w_identity_preserves_v7v_runtime_shell_and_validation_boundary() -> None:
    candidate = _json("configs/current_candidate.json")
    manifest_path = ROOT / "configs/runtime_manifest.json"
    manifest_bytes = manifest_path.read_bytes()
    manifest = json.loads(manifest_bytes.decode("utf-8"))
    parent = json.loads(_git_bytes(V7V_SNAPSHOT, "configs/current_candidate.json"))

    assert candidate["candidate_id"] == "candidate-v7w-high-score-core-recovery"
    assert candidate["parent_candidate_id"] == "candidate-v7v-preflight-ordering-repair"
    assert candidate["base_main_sha"] == V7V_SNAPSHOT
    assert candidate["status"] == "STATIC_IMPLEMENTED_NOT_RUNTIME_VALIDATED"
    assert candidate["decision"] == "S09_01_STATIC_STRATEGY_IMPLEMENTATION"
    assert candidate["strategy_delta"] == "STABILITY_CONSTRAINED_PROMOTION_COMPOUNDING"
    assert manifest["name"] == candidate["candidate_id"]
    assert manifest["mode"] == "agent"
    assert len(manifest["instruction"]) <= 5200
    assert candidate["runtime_manifest"]["sha256"] == hashlib.sha256(manifest_bytes).hexdigest()
    assert candidate["runtime_manifest"]["instruction_sha256"] == hashlib.sha256(
        manifest["instruction"].encode("utf-8")
    ).hexdigest()
    assert candidate["runtime_contract_delta"] == parent["runtime_contract_delta"]
    assert candidate["architecture"] == parent["architecture"]
    assert candidate["adopted_mechanisms"][: len(parent["adopted_mechanisms"])] == parent[
        "adopted_mechanisms"
    ]
    assert candidate["adopted_mechanisms"][-1] == "TERMINAL_HORIZON_DIRECT_REALIZATION"
    assert candidate["rejected_mechanisms"] == parent["rejected_mechanisms"]
    assert candidate["validation"] and all(value is False for value in candidate["validation"].values())

    actual_skills = {entry["name"]: entry for entry in candidate["skills"]}
    assert set(actual_skills) == set(SKILLS)
    for skill in SKILLS:
        path = f"skills/{skill}/SKILL.md"
        parent_blob = subprocess.check_output(
            ["git", "rev-parse", f"{V7V_SNAPSHOT}:{path}"], cwd=ROOT, text=True, encoding="utf-8"
        ).strip()
        working_blob = subprocess.check_output(
            ["git", "hash-object", f"--path={path}", str(ROOT / path)],
            cwd=ROOT,
            text=True,
            encoding="utf-8",
        ).strip()
        assert actual_skills[skill]["git_blob"] == working_blob
        if skill == "rolling-planning":
            assert working_blob != parent_blob
        else:
            assert working_blob == parent_blob


def test_manifest_markers_energy_strategy_and_runner_surfaces_are_unchanged() -> None:
    manifest = _json("configs/runtime_manifest.json")["instruction"]
    risk = _text("skills/risk-review/SKILL.md")
    delivery = _text("skills/delivery-progress/SKILL.md")
    planning = _text("skills/rolling-planning/SKILL.md")

    assert "RB=<NONE|DONE|BLOCKED>" in manifest and "RB=<NONE|DONE|BLOCKED>" in risk
    assert "checkpoint=<NEAR|NOT_NEAR|UNKNOWN>" in manifest
    assert "checkpoint=<NEAR|NOT_NEAR|UNKNOWN>" in delivery
    assert "QUARTER_INTENT=<MODE|current target>" in manifest
    assert "QUARTER_INTENT = <MODE | current target>" in planning
    for path in ("pyproject.toml", "uv.lock", "career_sim_runner"):
        changed = subprocess.check_output(
            ["git", "diff", "--name-only", BASE, "--", path], cwd=ROOT, text=True, encoding="utf-8"
        ).strip()
        assert changed == ""
