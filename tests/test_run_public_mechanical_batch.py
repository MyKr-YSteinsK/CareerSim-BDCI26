import asyncio
from pathlib import Path

import pytest

from scripts.run_public_mechanical_batch import (
    main,
    run_one_session,
    structural_target_for_choice,
    validate_public_tools,
)
from scripts.public_mechanical_probe import project_public_snapshot


TOOLS = [
    {"name": "new_game", "inputSchema": {"type": "object", "properties": {}, "required": []}},
    {
        "name": "observe",
        "inputSchema": {"type": "object", "properties": {"session_id": {"type": "string"}}, "required": ["session_id"]},
    },
    {
        "name": "take_action",
        "inputSchema": {
            "type": "object",
            "properties": {
                "session_id": {"type": "string"},
                "choice": {"type": "integer"},
                "notes": {"type": "string"},
            },
            "required": ["session_id", "choice", "notes"],
        },
    },
]


def observe_payload(month, output, *, alive=True, failed=False):
    return {
        "current_state": {
            "time": {"current_month": month, "current_quarter": 1, "current_year": 1},
            "status": {"level": "L1", "output": output, "health": 5, "network": 1, "dignity": 5},
            "simulation_flags": {"alive": alive, "failed": failed},
        },
        "current_event": {"title": "public", "description": "public"},
        "choices": []
        if not alive
        else [
            {"choice": 1, "action": "准备汇报材料", "description": "public"},
            {"choice": 2, "action": "健康恢复", "description": "public"},
        ],
        "events": "",
    }


class FakePublicClient:
    def __init__(self, *, terminal=True):
        self.terminal = terminal
        self.actions = 0
        self.calls = []

    async def initialize(self):
        self.calls.append("initialize")

    async def list_tools(self):
        self.calls.append("list_tools")
        return TOOLS

    async def call_tool(self, name, arguments):
        self.calls.append((name, arguments))
        if name == "new_game":
            return {"session_id": "fake-session"}
        if name == "observe":
            if self.actions == 0:
                return observe_payload(1, 0)
            if self.actions == 1:
                return observe_payload(2, 1)
            return observe_payload(3, 1, alive=not self.terminal, failed=self.terminal)
        if name == "take_action":
            self.actions += 1
            return {"success": True, "error": None}
        raise AssertionError(name)


@pytest.mark.asyncio
@pytest.mark.parametrize("policy_code", ["P0", "P1", "P2"])
async def test_fake_client_full_mini_loop_wires_all_policies(policy_code):
    result = await run_one_session(FakePublicClient(), policy_code=policy_code, session_index=1, action_ceiling=5)

    assert result.status == "COMPLETED"
    assert result.natural_terminal is True
    assert result.session_id == "fake-session"
    assert result.new_game_count == 1
    assert result.observe_count == 3
    assert result.successful_actions == 2
    assert result.public_seed_control == "NO_PUBLIC_SEED_CONTROL_FOUND"


def test_structural_target_mapping_fails_closed_for_multi_target_or_story_actions():
    mapped = project_public_snapshot(observe_payload(1, 0))
    assert structural_target_for_choice(mapped, 1) == ("output", "energy:output")

    story = project_public_snapshot(
        {
            **observe_payload(1, 0),
            "choices": [{"choice": 1, "action": "story option", "description": "public"}],
        }
    )
    assert structural_target_for_choice(story, 1) is None


def test_public_tool_contract_and_no_seed_control():
    names, seed_control = validate_public_tools(TOOLS)

    assert {"new_game", "observe", "take_action"}.issubset(names)
    assert seed_control is False


def test_live_path_requires_explicit_flag_and_import_is_side_effect_free():
    assert main([]) == 2
    source = Path("scripts/run_public_mechanical_batch.py").read_text(encoding="utf-8")
    assert "if __name__ == \"__main__\"" in source
    assert "--live" in source
    assert "subprocess" not in source


@pytest.mark.asyncio
async def test_action_ceiling_is_bounded_without_retry():
    result = await run_one_session(FakePublicClient(terminal=False), policy_code="P0", session_index=1, action_ceiling=1)

    assert result.status == "ACTION_CEILING"
    assert result.stop_batch is True
    assert result.successful_actions == 1
