"""Local HTTP presentation over the existing serialized Human controller."""

import asyncio
import json
import secrets
import threading
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

from hpl_client.controller import HumanGameController
from hpl_client.export import verify_zip
from hpl_client.fixtures import FixtureEngine
from hpl_client.game_adapter import PublicGameAdapter
from hpl_client.presentation import choice_disabled_reason
from hpl_client.recorder import RunRecorder, now
from hpl_client.path_contract import HPLLayout, assert_isolated_run_root, engine_constructor_kwargs, DATASET_PATHS
from scripts.hpl_public_evidence import SCHEMA_VERSION, project_cli_frame

ASSETS = Path(__file__).with_name("web_assets")


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate JSON key")
        result[key] = value
    return result


def manifest(tag, identifier, fixture):
    return {
        "run_id": identifier,
        "authorization_id": "FIXTURE_NON_GAME" if fixture else "USER_WEB_START_CLICK",
        "human_tag": ("FIXTURE-" + tag)[:64] if fixture else tag,
        "started_at": now(),
        "ended_at": "PENDING",
        "hpl_commit": "HPL_WEB_DEVELOPMENT",
        "launcher_version": "hpl-05/fixture-non-game" if fixture else "hpl-05/local-web",
        "python_version": "3.12.10",
        "career_emulator_version": "1.0.1",
        "career_emulator_bdci26_version": "1.0.0",
        "dataset_source": "HPL_INSTALLED_BDCI26_DEV",
        "dataset_split": "dev",
        "dataset_root": "career_emulator_bdci26/dev/dataset",
        "hpl_venv_root": "HPL_WEB_DEDICATED_VENV",
        "hpl_runtime_root": "runs/" + identifier,
        "provider_used": False,
        "provider_evidence_basis": "FIXTURE / NON_GAME"
        if fixture
        else "Validated isolated local Web runtime; direct GameEngine; no provider path",
        "public_evidence_schema_version": SCHEMA_VERSION,
    }


class EndingFixtureEngine(FixtureEngine):
    async def take_action(self, *args, **kwargs):
        result = await super().take_action(*args, **kwargs)
        self.ending = True
        return result


def fixture_controller(root):
    """Real recorder/finalizer, synthetic engine, fixture-only filesystem scope."""
    workspace = Path(root) / "fixtures"
    layout = HPLLayout(workspace, workspace / "fixture-worktree", workspace)

    def factory(tag):
        identifier = uuid.uuid4().hex
        run = layout.runs_root / identifier
        assert_isolated_run_root(run, layout)
        run.mkdir(parents=True)
        recorder = RunRecorder(run, manifest(tag, identifier, True))
        return PublicGameAdapter(EndingFixtureEngine(energy=2), identifier), recorder

    return HumanGameController(factory, layout=layout)


def web_human_factory(tag):
    """Future user Start only; never called at server startup or fixture validation."""
    import os
    import subprocess

    from scripts.hpl_web_runtime import runtime_root, startup_check
    from scripts.hpl_play import resolve_layout

    startup_check()
    layout = resolve_layout()
    identifier = uuid.uuid4().hex
    run = layout.runs_root / identifier
    assert_isolated_run_root(run, layout)
    run.mkdir(parents=True, exist_ok=False)
    logs = run / "runtime" / "logs"
    logs.mkdir(parents=True)
    db = run / "runtime" / "career_emulator.sqlite3"
    os.environ["CAREER_EMULATOR_DB"] = str(db)
    os.environ["CAREER_EMULATOR_LOG_DIR"] = str(logs)
    fields = manifest(tag, identifier, False)
    fields["hpl_commit"] = subprocess.check_output(
        ["git", "-C", str(layout.worktree_root), "rev-parse", "HEAD"], text=True
    ).strip()
    recorder = RunRecorder(run, fields)
    try:
        from career_emulator.game import GameEngine

        dev = runtime_root() / "venv/Lib/site-packages/career_emulator_bdci26/dev/dataset"
        paths = {key: str(dev / name) for key, name in DATASET_PATHS.items()}
        engine = GameEngine(**engine_constructor_kwargs(paths, db))
        engine.store.log_dir = logs
    except Exception as error:
        recorder.failure(error)
        raise
    return PublicGameAdapter(engine, identifier), recorder


class WebApplication:
    """One event loop and operation lock; HTTP never touches simulator/DB state."""

    def __init__(self, controller, *, fixture=True):
        self.controller = controller
        self.fixture = fixture
        self.token = secrets.token_urlsafe(32)
        self._seen = set()
        self._lock = threading.RLock()
        self._loop = asyncio.new_event_loop()
        self._worker = threading.Thread(target=self._loop.run_forever, daemon=True)
        self._worker.start()

    def state(self):
        with self._lock:
            controller = self.controller
            # Defense in depth: reproject public facts, never serialize raw engine/controller.
            facts = project_cli_frame(controller.view.facts)["observed_fact"] if controller.view else {}
            choices = [
                dict(item, disabled_reason=choice_disabled_reason(item, facts.get("state", {}).get("energy")))
                for item in facts.get("choices", [])
            ]
            return {
                "mode": "FIXTURE / NON_GAME" if self.fixture else "HUMAN / LOCAL",
                "token": self.token,
                "phase": controller.phase,
                "busy": controller.busy,
                "run_id": controller.view.run_id if controller.view else None,
                "revision": controller.view.revision if controller.view else 0,
                "facts": facts,
                "choices": choices,
                "history": controller.history,
                "error": controller.error,
                "rejection": controller.rejection,
                "action_status": controller.action_status,
                "export_message": controller.export_message,
                "finalization_status": controller.finalization_status,
                "export_name": controller.export_path.name if controller.export_path else None,
            }

    def operation(self, name, body):
        with self._lock:
            request_id = body.get("request_id") if isinstance(body, dict) else None
            try:
                valid_id = type(request_id) is str and str(uuid.UUID(request_id)) == request_id
            except ValueError:
                valid_id = False
            if not valid_id or request_id in self._seen or len(self._seen) >= 10000:
                return False, "INVALID_ACTION / NO_MUTATION"
            expected = {
                "start": {"request_id", "participant"},
                "choose": {"request_id", "choice", "revision", "run_id"},
                "export": {"request_id"},
                "shutdown": {"request_id"},
            }
            if name not in expected or set(body) != expected[name]:
                return False, "INVALID_ACTION / NO_MUTATION"
            if name == "start" and (type(body["participant"]) is not str or len(body["participant"]) > 64):
                return False, "INVALID_ACTION / NO_MUTATION"
            if name == "choose" and (
                type(body["choice"]) is not int or type(body["revision"]) is not int or type(body["run_id"]) is not str
            ):
                return False, "INVALID_ACTION / NO_MUTATION"
            self._seen.add(request_id)
            if name == "shutdown":
                return True, "SHUTDOWN"
            if name == "start":
                task = self.controller.start(body["participant"])
            elif name == "export":
                task = self.controller.finish_export()
            else:
                task = self.controller.choose(body["choice"], body["revision"], body["run_id"])
            accepted = asyncio.run_coroutine_threadsafe(task, self._loop).result()
            return accepted, self.controller.action_status

    def close(self):
        with self._lock:
            asyncio.run_coroutine_threadsafe(self._loop.shutdown_default_executor(), self._loop).result()
            self._loop.call_soon_threadsafe(self._loop.stop)
            self._worker.join()
            self._loop.close()


class LocalWebServer(ThreadingHTTPServer):
    daemon_threads = False
    allow_reuse_address = False

    def __init__(self, application):
        self.application = application
        super().__init__(("127.0.0.1", 0), Handler)
        self.origin = f"http://127.0.0.1:{self.server_port}"


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass  # Tokens/request contents never go to access logs.

    def reply(self, status, content, content_type="application/json; charset=utf-8"):
        if not isinstance(content, bytes):
            content = json.dumps(content, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header(
            "Content-Security-Policy",
            "default-src 'self'; script-src 'self'; style-src 'self'; connect-src 'self'; "
            "object-src 'none'; frame-ancestors 'none'; base-uri 'none'; form-action 'self'",
        )
        self.end_headers()
        self.wfile.write(content)

    def allowed_host(self):
        hosts = self.headers.get_all("Host", [])
        return hosts == [urlsplit(self.server.origin).netloc]

    def authenticated(self):
        return secrets.compare_digest(self.headers.get("X-HPL-Token", ""), self.server.application.token)

    def do_GET(self):
        if not self.allowed_host():
            return self.reply(403, {"error": "Unexpected Host"})
        assets = {
            "/": ("index.html", "text/html; charset=utf-8"),
            "/app.js": ("app.js", "text/javascript; charset=utf-8"),
            "/app.css": ("app.css", "text/css; charset=utf-8"),
        }
        if self.path in assets:
            name, content_type = assets[self.path]
            return self.reply(200, (ASSETS / name).read_bytes(), content_type)
        if self.path == "/api/state":
            return self.reply(200, self.server.application.state())
        if self.path == "/api/export" and self.authenticated():
            app = self.server.application
            with app._lock:
                path = app.controller.export_path
                if path and app.controller.view:
                    try:
                        verify_zip(path, app.controller.view.run_id)
                        return self.reply(200, path.read_bytes(), "application/zip")
                    except (OSError, ValueError):
                        return self.reply(409, {"error": "Export unavailable; retained for review"})
        return self.reply(404, {"error": "Not found"})

    def do_POST(self):
        try:
            if self.headers.get("Content-Type") != "application/json" or self.headers.get("Transfer-Encoding"):
                raise ValueError("Expected JSON body")
            length = int(self.headers.get("Content-Length", "0"))
            if not 0 < length <= 8192:
                raise ValueError("Body size")
            self.connection.settimeout(5)
            raw = self.rfile.read(length)
            if len(raw) != length:
                raise ValueError("Incomplete body")
            # Drain bounded bodies before refusal: closing with unread POST bytes
            # can reset the TCP connection on Windows and discard the 403 reply.
            if not self.allowed_host() or not self.authenticated() or self.headers.get("Origin") != self.server.origin:
                return self.reply(403, {"error": "Local launch token / origin required"})
            if self.headers.get("Sec-Fetch-Site") not in (None, "same-origin"):
                return self.reply(403, {"error": "Cross-origin request rejected"})
            body = json.loads(raw, object_pairs_hook=unique_object)
            name = self.path.removeprefix("/api/") if self.path.startswith("/api/") else ""
            accepted, status = self.server.application.operation(name, body)
        except (ValueError, TypeError, TimeoutError, json.JSONDecodeError):
            return self.reply(400, {"accepted": False, "status": "INVALID_ACTION / NO_MUTATION"})
        self.reply(
            200 if accepted else 409, {"accepted": accepted, "status": status, "state": self.server.application.state()}
        )
        if accepted and name == "shutdown":
            threading.Thread(target=self.server.shutdown, daemon=True).start()
