import json

from scripts.public_mechanical_probe import (
    MechanicalProbe,
    MechanicalTracker,
    MinIdControl,
    ProbeLocalState,
    project_public_snapshot,
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
    assert not hasattr(projected, "hidden_counter")
    assert "hidden_counter" not in projected.status


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
