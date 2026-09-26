import json

import pytest

from scripts.public_mechanical_probe import (
    MechanicalProbe,
    MechanicalTracker,
    MinIdControl,
    ProbeLocalState,
    SimplePublicGrowthPrior,
    StallAwarePublicGrowth,
    classify_structural_context,
    project_public_snapshot,
    with_public_material_risk,
)


def observe_payload(
    *,
    session_id="s-1",
    month=1,
    status=None,
    choices=None,
    alive=True,
    failed=False,
    extra=None,
):
    payload = {
        "session_id": session_id,
        "current_state": {
            "session_id": session_id,
            "time": {"current_month": month, "current_quarter": 1, "current_year": 1},
            "status": status or {"output": 10, "health": 8},
            "simulation_flags": {"alive": alive, "failed": failed},
        },
        "current_event": {"title": "Public event", "description": "Public description"},
        "choices": choices if choices is not None else [{"choice": 1, "action": "A", "description": "A"}],
        "events": "public feed",
    }
    if extra:
        payload.update(extra)
    return payload


def snapshot(**kwargs):
    return project_public_snapshot(observe_payload(**kwargs))


def test_public_projection_is_strict_and_records_unknown_names():
    projected = project_public_snapshot(
        observe_payload(
            extra={
                "hidden_counter": 99,
                "current_state": {
                    **observe_payload()["current_state"],
                    "status": {"output": 10, "hidden_risk": 7},
                    "private_formula": {"value": 1},
                },
            }
        )
    )

    assert projected.session_id == "s-1"
    assert projected.time.current_month == 1
    assert projected.status["output"] == 10
    assert projected.choices[0].choice == 1
    assert "hidden_counter" in projected.ignored_fields
    assert "current_state.private_formula" in projected.ignored_fields
    assert "current_state.status.hidden_risk" in projected.ignored_fields
    assert not hasattr(projected, "hidden_counter")
    assert "hidden_counter" not in projected.status
    assert "hidden_risk" not in projected.status


def test_min_id_control_returns_integer_one():
    projected = snapshot(choices=[{"choice": 3}, {"choice": 1}, {"choice": 2}])
    decision = MinIdControl().choose(projected, ProbeLocalState())

    assert decision.status == "ACTION"
    assert decision.choice == 1
    assert isinstance(decision.choice, int)


def test_empty_choices_defer_without_guessing():
    projected = snapshot(choices=[])
    decision = MinIdControl().choose(projected)

    assert decision.status == "UNSUPPORTED"
    assert decision.choice is None


def test_structural_context_uses_exact_public_action_labels_only():
    energy = snapshot(choices=[{"choice": 3, "action": "高强度工作", "description": "ordinary"}])
    main = snapshot(choices=[{"choice": 4, "action": "申请关键项目", "description": "ordinary"}])
    story = snapshot(
        choices=[{"choice": 1, "action": "ordinary option", "description": "申请关键项目"}],
    )

    assert classify_structural_context(energy) == "ENERGY"
    assert classify_structural_context(main) == "MAIN"
    assert classify_structural_context(story) == "UNKNOWN_CONTEXT"


def test_p1_growth_prior_and_explicit_public_risk_override():
    projected = snapshot(
        choices=[
            {"choice": 7, "action": "健康恢复"},
            {"choice": 3, "action": "高强度工作"},
        ]
    )
    policy = SimplePublicGrowthPrior()

    assert policy.choose(projected).choice == 3
    risky = with_public_material_risk(projected, "MATERIAL")
    assert policy.choose(risky).choice == 7


def test_unknown_context_uses_common_min_id_fallback_for_p1_and_p2():
    projected = snapshot(choices=[{"choice": 5, "action": "story A"}, {"choice": 2, "action": "story B"}])

    assert SimplePublicGrowthPrior().choose(projected).choice == 2
    assert StallAwarePublicGrowth().choose(projected).choice == 2


def test_p2_one_no_progress_checkpoint_does_not_switch():
    public = snapshot(
        status={"output": 10},
        choices=[{"choice": 1, "action": "高强度工作"}, {"choice": 2, "action": "人脉维护"}],
    )
    probe = MechanicalProbe(StallAwarePublicGrowth())
    assert probe.choose(public).choice == 1
    probe.record_checkpoint(public, target="output", path="energy:growth")
    assert probe.choose(public).choice == 1
    observation = probe.record_checkpoint(public, target="output", path="energy:growth")

    assert observation.stall_signal == "NONE"
    decision = probe.choose(public)
    assert decision.choice == 1
    assert decision.structural_switch is False


def test_p2_two_comparable_stalls_trigger_one_structural_alternative():
    public = snapshot(
        status={"output": 10},
        choices=[{"choice": 1, "action": "高强度工作"}, {"choice": 2, "action": "人脉维护"}],
    )
    probe = MechanicalProbe(StallAwarePublicGrowth())
    assert probe.choose(public).choice == 1
    probe.record_checkpoint(public, target="output", path="energy:growth")
    probe.record_checkpoint(public, target="output", path="energy:growth")
    assert probe.tracker.observations[-1].stall_signal == "NONE"
    probe.record_checkpoint(public, target="output", path="energy:growth")

    decision = probe.choose(public)
    assert decision.status == "ACTION"
    assert decision.choice == 2
    assert decision.structural_switch is True
    assert probe.report().to_dict()["chosen_actions"] == [1, 2]
    assert probe.report().to_dict()["structural_switch_count"] == 1

    # A second stall cannot open another rotation in this bounded policy.
    after_switch = probe.choose(public)
    assert after_switch.structural_switch is False


def test_p2_stall_without_structural_alternative_defers():
    public = snapshot(choices=[{"choice": 1, "action": "高强度工作"}], status={"output": 10})
    probe = MechanicalProbe(StallAwarePublicGrowth())
    assert probe.choose(public).choice == 1
    probe.record_checkpoint(public, target="output", path="energy:growth")
    probe.record_checkpoint(public, target="output", path="energy:growth")
    probe.record_checkpoint(public, target="output", path="energy:growth")

    decision = probe.choose(public)
    assert decision.status == "DEFER"
    assert decision.choice is None


@pytest.mark.parametrize("policy", [MinIdControl(), SimplePublicGrowthPrior(), StallAwarePublicGrowth()])
def test_policies_only_emit_legal_integer_or_defer(policy):
    projected = snapshot(
        choices=[{"choice": 8, "action": "ordinary"}, {"choice": 4, "action": "ordinary"}],
    )
    decision = policy.choose(projected)

    assert decision.status in {"ACTION", "DEFER", "UNSUPPORTED"}
    if decision.status == "ACTION":
        assert decision.choice in {4, 8}
        assert isinstance(decision.choice, int)


def test_one_no_progress_checkpoint_is_not_stalled():
    tracker = MechanicalTracker()
    first = tracker.record_checkpoint(snapshot(status={"output": 10}), target="output", path="choice:1")
    second = tracker.record_checkpoint(snapshot(status={"output": 10}), target="output", path="choice:1")

    assert first.comparable is False
    assert second.comparable is True
    assert second.progress == "NO_PROGRESS"
    assert second.stall_signal == "NONE"


def test_two_comparable_no_progress_checkpoints_emit_stall_signal():
    tracker = MechanicalTracker()
    tracker.record_checkpoint(snapshot(status={"output": 10}), target="output", path="choice:1")
    second = tracker.record_checkpoint(snapshot(status={"output": 10}), target="output", path="choice:1")
    third = tracker.record_checkpoint(snapshot(status={"output": 10}), target="output", path="choice:1")

    assert second.stall_signal == "NONE"
    assert third.progress == "NO_PROGRESS"
    assert third.stall_signal == "MECHANICAL_STALL_SIGNAL"


def test_changed_path_or_missing_target_is_not_stalled():
    tracker = MechanicalTracker()
    tracker.record_checkpoint(snapshot(status={"output": 10}), target="output", path="choice:1")
    changed = tracker.record_checkpoint(snapshot(status={"output": 10}), target="output", path="choice:2")
    missing = tracker.record_checkpoint(snapshot(status={"health": 8}), target="output", path="choice:2")

    assert changed.comparable is False
    assert changed.stall_signal == "NONE"
    assert missing.comparable is False
    assert missing.reason == "target_value_unavailable"
    assert missing.stall_signal == "NONE"


def test_probe_report_is_bounded_json_and_records_milestones():
    probe = MechanicalProbe()
    public = snapshot(status={"output": 10}, alive=True, failed=False)
    terminal = snapshot(status={"output": 10}, alive=False, failed=True, month=2)

    assert probe.choose(public).choice == 1
    probe.record_checkpoint(public, target="output", path="choice:1")
    probe.record_action_receipt(True)
    probe.record_checkpoint(terminal, target="output", path="choice:1", promotion_label="M2")
    report = probe.report().to_dict()

    assert report["policy_name"] == "MIN_ID_CONTROL"
    assert report["chosen_actions"] == [1]
    assert report["action_receipts"] == [{"success": True, "status": "SUCCESS"}]
    assert report["promotion_milestones"][0]["label"] == "M2"
    assert report["terminal_milestones"][0]["kind"] == "terminal"
    json.dumps(report)


def test_probe_passes_bounded_local_state_to_policy():
    probe = MechanicalProbe()
    public = snapshot()

    assert probe.choose(public).choice == 1
    probe.record_checkpoint(public, target="output", path="choice:1")
    assert probe.choose(public).choice == 1

    assert probe.report().to_dict()["repeated_action_count"] == 2


def test_module_has_no_live_transport_or_provider_dependency():
    from pathlib import Path

    source = Path("scripts/public_mechanical_probe.py").read_text(encoding="utf-8")
    for forbidden in ("stdio_client", "career-emulator-mcp", "DEEPSEEK_API_KEY", "subprocess"):
        assert forbidden not in source
