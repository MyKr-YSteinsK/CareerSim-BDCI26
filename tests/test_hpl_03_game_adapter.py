"""Direct API fixtures, never import or create a real engine."""

import asyncio
import json
from types import SimpleNamespace

import pytest

from hpl_client.fixtures import FixtureEngine
from hpl_client.game_adapter import PublicGameAdapter


class HostileEngine(FixtureEngine):
    async def observe(self, session_id):
        result = await super().observe(session_id)
        result.current_state["status"]["hidden_risk"] = "PRIVATE_SENTINEL"
        result.current_state["private"] = "PRIVATE_SENTINEL"
        result.current_event.update(event_id="PRIVATE_SENTINEL", node_id="PRIVATE_SENTINEL")
        result.choices[0]["status_updates"] = {"hidden_risk": "PRIVATE_SENTINEL"}
        return result


def test_adapter_public_firewall_and_handbook():
    adapter = PublicGameAdapter(HostileEngine(), "fixture")
    view = asyncio.run(adapter.start())
    assert "PRIVATE_SENTINEL" not in json.dumps(view.projection)
    assert view.projection["public_status"] == "PUBLIC_FIELDS_ALLOWLISTED"
    assert "human_interpretation" not in view.facts
    assert view.facts["state"]["month"] == 5
    assert view.facts["handbook"]
    assert view.facts["warning"]
    assert view.phase == "ACTIVE"


def test_final_fields_drop_dimensions_and_derive_official_cli_outcome():
    class EndEngine(FixtureEngine):
        async def observe(self, session_id):
            raw = await super().observe(session_id)
            raw.choices = []
            raw.ending_score = {
                "completed": True,
                "grade": "A",
                "survival_months": 48,
                "quantitative_score": 80,
                "competition_partial_score": 42,
                "dimensions": "PRIVATE_SENTINEL",
                "weights": "PRIVATE_SENTINEL",
            }
            return raw

    view = asyncio.run(PublicGameAdapter(EndEngine(), "fixture").start())
    assert view.phase == "ENDED"
    assert view.facts["final_result"]["outcome"] == "48-month completion"
    assert "PRIVATE_SENTINEL" not in json.dumps(view.projection)


@pytest.mark.parametrize("failure", ["start", "action", "session", "state"])
def test_invalid_receipt_or_observation_fails_closed(failure):
    class BadEngine(FixtureEngine):
        async def new_game(self):
            if failure == "start":
                return SimpleNamespace(error="bad", session_id="")
            return await super().new_game()

        async def take_action(self, *args, **kwargs):
            return SimpleNamespace(success=False, error="bad")

        async def observe(self, session_id):
            raw = await super().observe(session_id)
            if failure == "session":
                raw.current_state["session_id"] = "other"
            if failure == "state":
                raw.current_state["status"] = {}
            return raw

    async def exercise():
        adapter = PublicGameAdapter(BadEngine(), "fixture")
        await adapter.start()
        if failure == "action":
            await adapter.act(1)

    with pytest.raises(RuntimeError):
        asyncio.run(exercise())


def test_installed_101_api_and_real_dataclass_shape_without_game():
    import subprocess
    from scripts.hpl_play import resolve_layout

    layout = resolve_layout()
    code = """
import asyncio, inspect, importlib.metadata
from career_emulator.game import GameEngine
from career_emulator.server.models import CareerState, ObserveResponse, NewGameResponse
from hpl_client.game_adapter import PublicGameAdapter
assert importlib.metadata.version("career-emulator") == "1.0.1"
for name in ("new_game", "observe", "take_action", "enrollment_handbook"):
    assert inspect.iscoroutinefunction(getattr(GameEngine, name))
assert list(inspect.signature(GameEngine.take_action).parameters) == ["self", "session_id", "choice", "notes"]
class Fake:
    async def new_game(self): return NewGameResponse(session_id="offline-fixture")
    async def enrollment_handbook(self): return "fixture handbook"
    async def observe(self, session_id):
        state = CareerState().to_visible_dict()
        state["session_id"] = session_id
        return ObserveResponse(current_state=state, current_event={"title":"fixture", "description":"fixture"}, choices=[{"choice":1,"action":"fixture"}])
view = asyncio.run(PublicGameAdapter(Fake(), "fixture").start())
assert view.phase == "ACTIVE" and "hidden_risk" not in view.facts["state"]
print("INSTALLED_API_NO_GAME_PASS")
"""
    result = subprocess.run(
        [str(layout.sandbox_root / "venv/Scripts/python.exe"), "-c", code],
        cwd=layout.worktree_root,
        capture_output=True,
        text=True,
        timeout=20,
    )
    assert result.returncode == 0, result.stderr
    assert "INSTALLED_API_NO_GAME_PASS" in result.stdout
