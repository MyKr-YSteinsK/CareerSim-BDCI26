import io
import sys
from contextlib import asynccontextmanager
from pathlib import Path

import pytest
from mcp.client.stdio import StdioServerParameters, stdio_client

import scripts.run_public_mechanical_batch as batch_runner
from scripts.run_public_mechanical_batch import (
    ProtocolError,
    _unexpected_runtime_text,
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


def test_fastmcp_auth_provider_path_warning_is_not_a_model_call():
    warning = (
        "D:\\CS\\CareerSim\\.venv\\Lib\\site-packages\\fastmcp\\server\\auth\\providers\\jwt.py:10: "
        "AuthlibDeprecationWarning: authlib.jose module is deprecated"
    )
    assert _unexpected_runtime_text(warning) is False
    assert _unexpected_runtime_text(warning + "\nprovider request started") is True


@pytest.mark.asyncio
async def test_action_ceiling_is_bounded_without_retry():
    result = await run_one_session(FakePublicClient(terminal=False), policy_code="P0", session_index=1, action_ceiling=1)

    assert result.status == "ACTION_CEILING"
    assert result.stop_batch is True
    assert result.successful_actions == 1


@pytest.mark.asyncio
async def test_sdk_stringio_fails_before_harmless_child_spawn_but_file_sink_works(tmp_path):
    marker = tmp_path / "harmless-child-ran.txt"
    code = f"from pathlib import Path; Path({str(marker)!r}).write_text('ran')"
    params = StdioServerParameters(command=sys.executable, args=["-c", code])

    with pytest.raises(io.UnsupportedOperation, match="fileno"):
        async with stdio_client(params, errlog=io.StringIO()):
            pass
    assert not marker.exists()
    assert issubclass(io.UnsupportedOperation, OSError)

    with (tmp_path / "stderr.log").open("w", encoding="utf-8") as stderr_file:
        assert stderr_file.fileno() >= 0
        async with stdio_client(params, errlog=stderr_file):
            pass
    assert marker.read_text(encoding="utf-8") == "ran"


class FakeSessionContext:
    async def __aenter__(self):
        return self

    async def __aexit__(self, *_args):
        return None


async def fake_batch(
    tmp_path,
    monkeypatch,
    client=None,
    transport_failure=False,
    stderr_text="",
    *,
    policy_order=None,
    task_id="S07-07",
    base_sha=batch_runner.S07_07_BASE_SHA,
    return_report=False,
    created_clients=None,
):
    monkeypatch.setattr(batch_runner, "MCP_EXECUTABLE", Path(sys.executable))
    monkeypatch.setattr(batch_runner, "_planned_slots", lambda _p2: ["P0"])
    monkeypatch.setattr(batch_runner, "ClientSession", lambda *_args: FakeSessionContext())
    def make_client(_session):
        instance = client if client is not None else FakePublicClient()
        if created_clients is not None:
            created_clients.append(instance)
        return instance

    monkeypatch.setattr(batch_runner, "MCPClientAdapter", make_client)

    @asynccontextmanager
    async def fake_stdio(_params, *, errlog):
        assert errlog.fileno() >= 0
        if transport_failure:
            raise OSError("unconfirmed transport start")
        errlog.write(stderr_text)
        errlog.flush()
        yield object(), object()

    monkeypatch.setattr(batch_runner, "stdio_client", fake_stdio)
    report = await batch_runner.run_live_batch(
        tmp_path / "runtime",
        tmp_path / "batch.json",
        policy_order=policy_order,
        task_id=task_id,
        base_sha=base_sha,
    )
    if return_report:
        return report
    return report["sessions"][0], report["totals"]


@pytest.mark.asyncio
async def test_explicit_s07_10_order_runs_only_six_p1_p2_sessions_and_records_identity(tmp_path, monkeypatch):
    order = ["P1", "P2"] * 3
    clients = []
    report = await fake_batch(
        tmp_path,
        monkeypatch,
        policy_order=order,
        task_id="S07-10",
        base_sha="test-base-sha",
        return_report=True,
        created_clients=clients,
    )

    assert report["task"] == "S07-10"
    assert report["base"] == "test-base-sha"
    assert report["planned_order"] == order
    assert report["executed_order"] == order
    assert [row["policy_code"] for row in report["sessions"]] == order
    assert report["totals"]["direct_server_starts"] == 6
    assert report["totals"]["new_game_count"] == 6
    assert report["provider_calls"] == 0
    assert report["agentserver_starts"] == 0
    assert len(clients) == 6
    assert all(
        call[1]["notes"] == "S07-10 public mechanical probe"
        for client in clients
        for call in client.calls
        if isinstance(call, tuple) and call[0] == "take_action"
    )


@pytest.mark.asyncio
async def test_explicit_policy_order_rejects_p0_or_more_than_six_before_creating_runtime(tmp_path, monkeypatch):
    monkeypatch.setattr(batch_runner, "MCP_EXECUTABLE", Path(sys.executable))
    monkeypatch.setattr(batch_runner, "_planned_slots", lambda _p2: ["P0"])

    with pytest.raises(ValueError, match="1-6 P1/P2"):
        await batch_runner.run_live_batch(
            tmp_path / "too-many",
            tmp_path / "too-many.json",
            policy_order=["P1"] * 7,
            task_id="S07-10",
            base_sha="test-base-sha",
        )
    with pytest.raises(ValueError, match="1-6 P1/P2"):
        await batch_runner.run_live_batch(
            tmp_path / "p0",
            tmp_path / "p0.json",
            policy_order=["P0"],
            task_id="S07-10",
            base_sha="test-base-sha",
        )

    assert not (tmp_path / "too-many").exists()
    assert not (tmp_path / "p0").exists()


@pytest.mark.asyncio
async def test_local_stderr_open_failure_is_prespawn_tooling_error(tmp_path, monkeypatch):
    original_open = Path.open

    def fail_local_sink(self, mode="r", *args, **kwargs):
        if self.name == "server-stderr.log" and mode == "w":
            raise OSError("local sink unavailable")
        return original_open(self, mode, *args, **kwargs)

    monkeypatch.setattr(Path, "open", fail_local_sink)
    session, totals = await fake_batch(tmp_path, monkeypatch)
    assert session["status"] == "TOOLING_OR_PRESPAWN_ERROR"
    assert session["error_code"] == "PRESPAWN_LOCAL_FAILURE"
    assert session["child_spawn_confirmed"] is False
    assert session["local_evidence"]["server_stderr"]["status"] == "UNAVAILABLE_PRESPAWN"
    assert totals["server_start_attempted"] == 0
    assert totals["direct_server_starts"] == 0
    assert totals["initialize_count"] == 0
    assert totals["shutdown_count"] == 0


@pytest.mark.asyncio
async def test_transport_failure_before_yield_remains_unknown(tmp_path, monkeypatch):
    session, totals = await fake_batch(tmp_path, monkeypatch, transport_failure=True)
    assert session["status"] == "UNKNOWN_SIDE_EFFECT"
    assert session["error_code"] == "LIVE_SERVER_START_OR_TRANSPORT_UNKNOWN"
    assert session["child_spawn_confirmed"] is None
    assert totals["server_start_attempted"] == 1
    assert totals["transport_entered"] == 0
    assert totals["direct_server_starts"] == 0
    assert totals["shutdown_count"] == 0


@pytest.mark.asyncio
async def test_entered_transport_with_initialize_failure_preserves_counts(tmp_path, monkeypatch):
    class InitializeFails(FakePublicClient):
        async def initialize(self):
            raise OSError("no initialization response")

    session, totals = await fake_batch(tmp_path, monkeypatch, client=InitializeFails())
    assert session["status"] == "UNKNOWN_SIDE_EFFECT"
    assert session["child_spawn_confirmed"] is True
    assert totals["transport_entered"] == 1
    assert totals["direct_server_starts"] == 1
    assert totals["initialize_count"] == 1
    assert totals["list_tools_count"] == 0
    assert totals["shutdown_count"] == 1


@pytest.mark.asyncio
async def test_initialize_success_then_protocol_failure_preserves_counts(tmp_path, monkeypatch):
    class ListFails(FakePublicClient):
        async def list_tools(self):
            raise ProtocolError("synthetic public schema error")

    session, totals = await fake_batch(tmp_path, monkeypatch, client=ListFails())
    assert session["status"] == "PROTOCOL_FAILURE"
    assert totals["initialize_count"] == 1
    assert totals["list_tools_count"] == 1
    assert totals["new_game_count"] == 0
    assert totals["shutdown_count"] == 1


@pytest.mark.asyncio
async def test_file_backed_transport_completes_and_stderr_is_retained(tmp_path, monkeypatch):
    session, totals = await fake_batch(tmp_path, monkeypatch, stderr_text="harmless child diagnostic\n")
    assert session["status"] == "COMPLETED"
    assert session["child_spawn_confirmed"] is True
    assert totals["server_start_attempted"] == 1
    assert totals["transport_entered"] == 1
    assert totals["direct_server_starts"] == 1
    assert totals["initialize_count"] == 1
    assert totals["list_tools_count"] == 1
    assert totals["shutdown_count"] == 1
    stderr_path = tmp_path / "runtime" / "01-p0" / "server-stderr.log"
    assert stderr_path.read_text(encoding="utf-8") == "harmless child diagnostic\n"
    assert session["local_evidence"]["server_stderr"]["bytes"] == stderr_path.stat().st_size
