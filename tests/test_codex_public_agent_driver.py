from __future__ import annotations

import importlib.util
from pathlib import Path
import sys

import pytest


MODULE_PATH = Path(__file__).parents[1] / "scripts" / "codex_public_agent_driver.py"
SPEC = importlib.util.spec_from_file_location("codex_public_agent_driver", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
driver = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = driver
SPEC.loader.exec_module(driver)


def test_requires_explicit_legal_choice_and_rationale() -> None:
    assert driver.parse_player_input("2 | 当前公开选项更符合我对眼前风险的判断。", [1, 2]).choice == 2
    with pytest.raises(ValueError):
        driver.parse_player_input("", [1, 2])
    with pytest.raises(ValueError):
        driver.parse_player_input("3 | 理由。", [1, 2])
    with pytest.raises(ValueError):
        driver.parse_player_input("1,2 | 理由。", [1, 2])


def test_projection_discards_unknown_values_but_keeps_names() -> None:
    snapshot = driver.project_public_snapshot(
        {
            "session_id": "public-session",
            "current_state": {
                "session_id": "public-session",
                "time": {"current_month": 3, "secret_clock": 999},
                "status": {"health": 70, "secret_score": 12345},
                "simulation_flags": {"alive": True, "hidden_counter": 42},
            },
            "current_event": {"title": "Public title", "description": "Visible text", "private_tag": "x"},
            "choices": [{"choice": 2, "action": "Public action", "description": "Visible choice", "internal_id": 9}],
            "unrecognized": {"sensitive": "must not escape"},
        }
    )
    assert snapshot["session_id"] == "public-session"
    assert snapshot["status"] == {"health": 70}
    assert snapshot["choices"] == [{"choice": 2, "action": "Public action", "description": "Visible choice"}]
    rendered = str(snapshot)
    assert "must not escape" not in rendered
    assert "12345" not in rendered
    assert "current_state.status.secret_score" in snapshot["ignored_field_names"]


def test_unknown_terminal_or_empty_choice_does_not_invent_action() -> None:
    snapshot = driver.project_public_snapshot({"session_id": "s", "choices": [], "private_action": 1})
    assert snapshot["choices"] == []
    assert snapshot["terminal"] is None
    assert "private_action" in snapshot["ignored_field_names"]


def test_player_input_validation_is_not_an_action_selector() -> None:
    source = MODULE_PATH.read_text(encoding="utf-8")
    assert "WAITING_FOR_PLAYER_CHOICE>" in source
    assert "parse_player_input(line, legal_ids)" in source
    assert "min(public" not in source
    assert "SimplePublicGrowthPrior" not in source
    assert "MechanicalPolicy" not in source
