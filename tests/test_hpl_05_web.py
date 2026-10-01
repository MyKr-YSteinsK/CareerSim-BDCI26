"""Fixture-only HTTP contracts; no CareerSim engine construction or gameplay."""

import json
import socket
import threading
import uuid
from urllib.error import HTTPError
from urllib.request import ProxyHandler, Request, build_opener

import pytest

from hpl_client.controller import HumanGameController
from hpl_client.fixtures import FixtureEngine, FixtureRecorder
from hpl_client.game_adapter import PublicGameAdapter
from hpl_client.web import LocalWebServer, WebApplication, fixture_controller


@pytest.fixture
def client(tmp_path):
    app = WebApplication(fixture_controller(tmp_path))
    server = LocalWebServer(app)
    thread = threading.Thread(target=server.serve_forever, kwargs={"poll_interval": 0.01})
    thread.start()
    yield server, app
    server.shutdown()
    thread.join()
    server.server_close()
    app.close()


def request(server, path="/api/state", body=None, *, headers=None, raw=None):
    defaults = {"Content-Type": "application/json", "X-HPL-Token": server.application.token, "Origin": server.origin}
    defaults.update(headers or {})
    data = raw if raw is not None else json.dumps(body).encode() if body is not None else None
    req = Request(server.origin + path, data=data, headers=defaults)
    try:
        with build_opener(ProxyHandler({})).open(req, timeout=5) as response:
            return response.status, response.read(), response.headers
    except HTTPError as error:
        return error.code, error.read(), error.headers


def post(server, operation, **fields):
    status, blob, _ = request(server, "/api/" + operation, {"request_id": str(uuid.uuid4()), **fields})
    return status, json.loads(blob)


def start(server):
    status, result = post(server, "start", participant="P017")
    assert status == 200
    return result["state"]


def selection(state, **overrides):
    return {"choice": 1, "revision": state["revision"], "run_id": state["run_id"], **overrides}


def test_root_static_public_fixture_and_no_initial_game(client):
    server, app = client
    assert server.server_address[0] == "127.0.0.1"
    assert app.controller.view is None and app.controller.recorder is None
    code, content, headers = request(server, "/")
    assert code == 200 and b"game-panel" in content
    assert "frame-ancestors 'none'" in headers["Content-Security-Policy"]
    assert request(server, "/app.js")[0] == request(server, "/app.css")[0] == 200
    for path in ("/../controller.py", "/evidence/manifest.json", "/runtime", "/?path=secret", "/api/state?path=x"):
        assert request(server, path)[0] == 404
    state = start(server)
    assert state["mode"] == "FIXTURE / NON_GAME"
    assert state["facts"]["state"]["energy"] == 2
    assert state["facts"]["handbook"]
    assert state["choices"][0]["disabled_reason"] is None
    assert "精力不足" in state["choices"][1]["disabled_reason"]
    assert "human_interpretation" not in state["facts"]
    assert "_engine" not in json.dumps(state)


@pytest.mark.parametrize(
    "headers",
    [
        {"Host": "attacker.invalid"},
        {"Origin": "https://attacker.invalid"},
        {"X-HPL-Token": "wrong"},
        {"Sec-Fetch-Site": "cross-site"},
    ],
)
def test_cross_origin_and_token_rejection_no_mutation(client, headers):
    server, app = client
    code, _, _ = request(server, "/api/start", {"request_id": str(uuid.uuid4()), "participant": "x"}, headers=headers)
    assert code == 403 and app.controller.view is None
    assert request(server, headers={"Host": "evil.invalid"})[0] == 403


@pytest.mark.parametrize(
    "override",
    [
        {"choice": 2},
        {"choice": 99},
        {"choice": True},
        {"choice": "1"},
        {"revision": 0},
        {"revision": True},
        {"run_id": "wrong-run"},
        {"path": "C:/private"},
    ],
)
def test_invalid_action_is_no_engine_or_evidence_mutation(client, override):
    server, app = client
    state = start(server)
    before = app.controller.view
    journal = app.controller.recorder.root / "staging/public_journal.jsonl"
    raw = journal.read_bytes()
    code, result = post(server, "choose", **selection(state, **override))
    assert code == 409 and result["status"] == "INVALID_ACTION / NO_MUTATION"
    assert app.controller.view == before and journal.read_bytes() == raw
    assert app.controller._adapter._engine.action_calls == 0


@pytest.mark.parametrize("body", [b"[]", b"null", b"{", b"{}", b'{"choice":1,"choice":2}'])
def test_malformed_requests_are_no_mutation(client, body):
    server, app = client
    status, data, _ = request(server, "/api/start", raw=body)
    assert status in (400, 409)
    assert json.loads(data)["status"] == "INVALID_ACTION / NO_MUTATION"
    assert app.controller.view is None


def test_ending_actual_fixture_export_duplicate_stale_and_download(client):
    server, app = client
    state = start(server)
    engine = app.controller._adapter._engine
    root = app.controller.recorder.root
    body = {"request_id": str(uuid.uuid4()), **selection(state)}
    code, blob, _ = request(server, "/api/choose", body)
    assert code == 200
    result = json.loads(blob)["state"]
    assert result["phase"] == "ENDED"
    assert result["finalization_status"] == "SUCCESSFULLY_FINALIZED_AND_EXPORTED"
    assert result["export_name"].startswith("CareerSim-FIXTURE-P017-Score82.00-P3-")
    assert not root.exists() and app.controller.export_path.is_file()
    assert request(server, "/api/choose", body)[0] == 409
    assert post(server, "choose", **selection(state))[0] == 409
    assert engine.action_calls == 1
    code, archive, _ = request(server, "/api/export")
    assert code == 200 and archive.startswith(b"PK")
    assert request(server, "/api/export", headers={"X-HPL-Token": "wrong"})[0] == 404


def test_unknown_action_stops_without_observe_or_retry(tmp_path):
    class Broken(FixtureEngine):
        observes = 0

        async def observe(self, session_id):
            self.observes += 1
            return await super().observe(session_id)

        async def take_action(self, *args, **kwargs):
            self.action_calls += 1
            raise OSError("unknown outcome")

    engine = Broken()
    controller = HumanGameController(lambda tag: (PublicGameAdapter(engine, "fixture"), FixtureRecorder()))
    app = WebApplication(controller)
    try:
        assert app.operation("start", {"request_id": str(uuid.uuid4()), "participant": "fixture"})[0]
        state = app.state()
        assert not app.operation("choose", {"request_id": str(uuid.uuid4()), **selection(state)})[0]
        assert app.state()["phase"] == "TECHNICAL_FAILURE"
        assert not app.operation("choose", {"request_id": str(uuid.uuid4()), **selection(state)})[0]
        assert engine.action_calls == 1 and engine.observes == 1
    finally:
        app.close()


def test_shutdown_releases_listener(tmp_path):
    app = WebApplication(fixture_controller(tmp_path))
    server = LocalWebServer(app)
    thread = threading.Thread(target=server.serve_forever, kwargs={"poll_interval": 0.01})
    thread.start()
    port = server.server_port
    try:
        assert post(server, "shutdown")[0] == 200
        thread.join(timeout=5)
        assert not thread.is_alive()
    finally:
        server.server_close()
        app.close()
    with socket.socket() as connection:
        connection.bind(("127.0.0.1", port))


def test_startup_refuses_wrong_interpreter_without_game():
    from scripts.hpl_web_runtime import startup_check

    with pytest.raises(RuntimeError, match="dedicated HPL-05"):
        startup_check()


def test_export_failure_is_retained_and_retry_is_not_an_action(client):
    server, app = client
    state = start(server)
    engine = app.controller._adapter._engine
    finalizer = app.controller._finalizer
    app.controller._finalizer = lambda *args: (_ for _ in ()).throw(OSError("fixture export failure"))
    status, result = post(server, "choose", **selection(state))
    assert status == 200 and result["state"]["finalization_status"] == "EXPORT_FAILED_RETAINED"
    assert app.controller.recorder.root.exists()
    app.controller._finalizer = finalizer
    status, result = post(server, "export")
    assert status == 200 and result["state"]["finalization_status"] == "SUCCESSFULLY_FINALIZED_AND_EXPORTED"
    assert engine.action_calls == 1


def test_start_duplicate_and_missing_fields_have_no_factory_mutation(client):
    server, app = client
    body = {"request_id": str(uuid.uuid4()), "participant": "fixture"}
    assert request(server, "/api/start", body)[0] == 200
    recorder = app.controller.recorder
    assert request(server, "/api/start", body)[0] == 409
    assert app.controller.recorder is recorder
    assert post(server, "choose", choice=1)[0] == 409
    assert app.controller._adapter._engine.action_calls == 0


def test_writable_gate_fails_closed_before_any_controller(tmp_path, monkeypatch):
    from scripts.hpl_web_runtime import writable

    def deny(*args, **kwargs):
        raise PermissionError("fixture read-only storage")

    monkeypatch.setattr("scripts.hpl_web_runtime.tempfile.TemporaryFile", deny)
    with pytest.raises(PermissionError):
        writable(tmp_path)


def test_future_human_factory_routes_every_run_using_only_fake_constructor(tmp_path, monkeypatch):
    import os
    import sys
    from types import SimpleNamespace

    from hpl_client.web import web_human_factory
    from scripts.hpl_play import HPLLayout

    layout = HPLLayout(tmp_path, tmp_path / "worktree", tmp_path / "sandbox")
    monkeypatch.setattr("scripts.hpl_play.resolve_layout", lambda: layout)
    monkeypatch.setattr("scripts.hpl_web_runtime.startup_check", lambda: {})
    monkeypatch.setattr("scripts.hpl_web_runtime.runtime_root", lambda: tmp_path / "web")
    monkeypatch.setattr("subprocess.check_output", lambda *args, **kwargs: "fixture-commit\n")
    monkeypatch.setenv("CAREER_EMULATOR_DB", "fixture-before")
    monkeypatch.setenv("CAREER_EMULATOR_LOG_DIR", "fixture-before")
    engines = []

    class FakeConstructor:
        def __init__(self, **kwargs):
            assert str(kwargs["db_path"]) == os.environ["CAREER_EMULATOR_DB"]
            assert str(kwargs["db_path"].parent / "logs") == os.environ["CAREER_EMULATOR_LOG_DIR"]
            self.store = SimpleNamespace(log_dir="old-default")
            engines.append(self)

    monkeypatch.setitem(sys.modules, "career_emulator.game", SimpleNamespace(GameEngine=FakeConstructor))
    _, first = web_human_factory("fixture")
    _, second = web_human_factory("fixture")
    assert first.root != second.root
    for engine, recorder in zip(engines, (first, second), strict=True):
        assert engine.store.log_dir == recorder.root / "runtime/logs"
        assert recorder.manifest["launcher_version"] == "hpl-05/local-web"
        assert not (recorder.root / "runtime/career_emulator.sqlite3").exists()
