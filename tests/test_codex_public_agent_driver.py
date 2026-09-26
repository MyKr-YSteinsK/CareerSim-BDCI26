from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager
import importlib.util
from types import ModuleType, SimpleNamespace
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
    assert "parse_player_input(line, legal_ids, sorted(blocked_choices))" in source
    assert "min(public" not in source
    assert "SimplePublicGrowthPrior" not in source
    assert "MechanicalPolicy" not in source


def _state(month: int = 1, health: int = 70, *, terminal: bool = False) -> dict[str, object]:
    return {
        "session_id": "pilot-session",
        "time": {"current_month": month},
        "status": {"health": health},
        "public_flags": {"alive": not terminal, "failed": terminal},
        "terminal": terminal,
    }


def _mcp_result(payload: object, *, is_error: bool = False) -> SimpleNamespace:
    return SimpleNamespace(structuredContent=payload, content=[], isError=is_error)


def test_public_state_comparator_covers_change_and_unknown_cases() -> None:
    base = _state()
    assert driver.compare_public_state(base, _state()) == "STATE_UNCHANGED"
    assert driver.compare_public_state(base, _state(month=2)) == "STATE_CHANGED"
    assert driver.compare_public_state(base, _state(health=69)) == "STATE_CHANGED"
    assert driver.compare_public_state(base, _state(terminal=True)) == "STATE_CHANGED"

    other_session = _state()
    other_session["session_id"] = "other-session"
    assert driver.compare_public_state(base, other_session) == "SESSION_MISMATCH"
    missing_status = _state()
    missing_status["status"] = {}
    assert driver.compare_public_state(base, missing_status) == "UNKNOWN_CRITICAL_STATE"
    assert driver.compare_public_state(base, {**base, "time": {}}) == "UNKNOWN_CRITICAL_STATE"


def test_completed_negative_response_reconciles_once_and_blocks_only_if_unchanged() -> None:
    async def run() -> None:
        observed: list[dict[str, object]] = []

        async def unchanged() -> dict[str, object]:
            result = _state()
            observed.append(result)
            return result

        rejected = await driver.reconcile_completed_action(
            _state(), _mcp_result({"success": False}), unchanged
        )
        assert len(observed) == 1
        assert rejected.classification == "EXPLICIT_ACTION_REJECTION_CONFIRMED"
        assert rejected.rejected is True
        assert rejected.receipt["success"] is False

        protocol_error = await driver.reconcile_completed_action(
            _state(), _mcp_result({"message": "public tool error"}, is_error=True), unchanged
        )
        assert protocol_error.classification == "EXPLICIT_ACTION_REJECTION_CONFIRMED"

        async def changed() -> dict[str, object]:
            return _state(month=2, health=69)

        changed_result = await driver.reconcile_completed_action(
            _state(), _mcp_result({"success": False, "reason": "not affordable"}), changed
        )
        assert changed_result.classification == "ACTION_RESPONSE_FALSE_BUT_PUBLIC_STATE_CHANGED"
        assert changed_result.rejected is False
        assert changed_result.receipt["reason"] == "not affordable"

        async def unconfirmed() -> None:
            return None

        unknown = await driver.reconcile_completed_action(
            _state(), _mcp_result({}, is_error=True), unconfirmed
        )
        assert unknown.classification == "UNKNOWN_SIDE_EFFECT"
        assert unknown.snapshot is None

    asyncio.run(run())


def _install_fake_mcp(monkeypatch: pytest.MonkeyPatch, client: object, tmp_path: Path) -> None:
    @asynccontextmanager
    async def fake_stdio_client(_params: object):
        yield (object(), object())

    class FakeClientSession:
        def __init__(self, _read: object, _write: object) -> None:
            pass

        async def __aenter__(self) -> object:
            return client

        async def __aexit__(self, *_args: object) -> None:
            return None

    fake_mcp = ModuleType("mcp")
    fake_mcp.__path__ = []  # type: ignore[attr-defined]
    fake_mcp.ClientSession = FakeClientSession  # type: ignore[attr-defined]
    fake_mcp.StdioServerParameters = lambda **kwargs: SimpleNamespace(**kwargs)  # type: ignore[attr-defined]
    fake_client = ModuleType("mcp.client")
    fake_client.__path__ = []  # type: ignore[attr-defined]
    fake_stdio = ModuleType("mcp.client.stdio")
    fake_stdio.stdio_client = fake_stdio_client  # type: ignore[attr-defined]
    fake_mcp.client = fake_client  # type: ignore[attr-defined]
    fake_client.stdio = fake_stdio  # type: ignore[attr-defined]
    monkeypatch.setitem(sys.modules, "mcp", fake_mcp)
    monkeypatch.setitem(sys.modules, "mcp.client", fake_client)
    monkeypatch.setitem(sys.modules, "mcp.client.stdio", fake_stdio)

    executable_dir = tmp_path / "Scripts"
    executable_dir.mkdir()
    (executable_dir / "career-emulator-mcp.exe").touch()
    monkeypatch.setattr(driver.sys, "executable", str(executable_dir / "python.exe"))


def _fake_tools() -> list[SimpleNamespace]:
    return [
        SimpleNamespace(name="new_game", inputSchema={"properties": {}}),
        SimpleNamespace(name="observe", inputSchema={"properties": {"session_id": {"type": "string"}}}),
        SimpleNamespace(
            name="take_action",
            inputSchema={"properties": {
                "session_id": {"type": "string"},
                "choice": {"type": "integer"},
                "notes": {"type": "string"},
            }},
        ),
    ]


def _observe_payload(month: int, *, terminal: bool = False) -> dict[str, object]:
    return {
        "session_id": "pilot-session",
        "current_state": {
            "session_id": "pilot-session",
            "time": {"current_month": month},
            "status": {"health": 70 if month == 1 else 69},
            "simulation_flags": {"alive": not terminal, "failed": terminal},
        },
        "current_event": {"title": "Public event", "description": "Participant-visible."},
        "choices": [
            {"choice": 1, "action": "First public action", "description": "Option one"},
            {"choice": 2, "action": "Second public action", "description": "Option two"},
        ],
        "terminal": terminal,
    }


def test_run_reconciles_rejection_blocks_resend_and_returns_to_player(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    class FakeClient:
        def __init__(self) -> None:
            self.observe_count = 0
            self.actions: list[int] = []

        async def initialize(self) -> SimpleNamespace:
            return SimpleNamespace(protocolVersion="test")

        async def list_tools(self) -> SimpleNamespace:
            return SimpleNamespace(tools=_fake_tools())

        async def call_tool(self, name: str, arguments: dict[str, object]) -> SimpleNamespace:
            if name == "new_game":
                return _mcp_result({"session_id": "pilot-session"})
            if name == "observe":
                self.observe_count += 1
                if self.observe_count == 1 or self.observe_count == 2:
                    return _mcp_result(_observe_payload(1))
                if self.observe_count == 3:
                    return _mcp_result(_observe_payload(2))
                return _mcp_result(_observe_payload(3, terminal=True))
            if name == "take_action":
                choice = int(arguments["choice"])
                self.actions.append(choice)
                if len(self.actions) == 1:
                    return _mcp_result({"success": False})
                return _mcp_result({"success": True})
            raise AssertionError(f"unexpected tool call: {name}")

    fake_client = FakeClient()
    _install_fake_mcp(monkeypatch, fake_client, tmp_path)
    inputs = iter([
        "1 | This public option fits the current evidence.",
        "1 | Try the same choice again.",
        "2 | Use a different legal option after the explicit rejection.",
        "1 | The public state changed, so reconsider the previously rejected choice.",
    ])
    monkeypatch.setattr("builtins.input", lambda: next(inputs))

    result = asyncio.run(driver.run_pilot(tmp_path / "pilot-evidence"))
    assert result == 0
    assert fake_client.actions == [1, 2, 1]
    assert fake_client.observe_count == 4


def test_transport_exception_stops_without_read_only_replay_or_action_retry(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    class FakeClient:
        def __init__(self) -> None:
            self.observe_count = 0
            self.actions: list[int] = []

        async def initialize(self) -> SimpleNamespace:
            return SimpleNamespace(protocolVersion="test")

        async def list_tools(self) -> SimpleNamespace:
            return SimpleNamespace(tools=_fake_tools())

        async def call_tool(self, name: str, arguments: dict[str, object]) -> SimpleNamespace:
            if name == "new_game":
                return _mcp_result({"session_id": "pilot-session"})
            if name == "observe":
                self.observe_count += 1
                return _mcp_result(_observe_payload(1))
            if name == "take_action":
                self.actions.append(int(arguments["choice"]))
                raise ConnectionError("synthetic transport interruption")
            raise AssertionError(f"unexpected tool call: {name}")

    fake_client = FakeClient()
    _install_fake_mcp(monkeypatch, fake_client, tmp_path)
    monkeypatch.setattr("builtins.input", lambda: "1 | A single test choice.")

    result = asyncio.run(driver.run_pilot(tmp_path / "pilot-evidence"))
    assert result == 6
    assert fake_client.actions == [1]
    assert fake_client.observe_count == 1
