"""Human-owned lifecycle and single submission gate."""

import asyncio
import importlib.metadata as metadata
import os
import re
import uuid

from scripts.hpl_evidence_writer import _KNOWN_SECRET_PATTERNS
from scripts.hpl_play import (
    _git_value,
    _load_environment_manifest,
    assert_isolated_run_root,
    engine_constructor_kwargs,
    resolve_layout,
)
from scripts.hpl_public_evidence import SCHEMA_VERSION

from hpl_client.game_adapter import PublicGameAdapter
from hpl_client.recorder import RunRecorder, now


def create_human_run(tag):
    """Called only by the user's GUI Start action, never at app startup."""
    layout = resolve_layout()
    _, identity = _load_environment_manifest(layout)
    for package in ("flet", "flet-desktop"):
        if metadata.version(package) != "1.0.1":
            raise RuntimeError("HPL requires Flet desktop 1.0.1")
    identifier = uuid.uuid4().hex
    root = layout.runs_root / identifier
    assert_isolated_run_root(root, layout)
    root.mkdir(parents=True, exist_ok=False)
    runtime = root / "runtime"
    logs = runtime / "logs"
    logs.mkdir(parents=True)
    os.environ["CAREER_EMULATOR_DB"] = str(runtime / "career_emulator.sqlite3")
    os.environ["CAREER_EMULATOR_LOG_DIR"] = str(logs)
    manifest = {
        "run_id": identifier,
        "authorization_id": "USER_GUI_START_CLICK",
        "human_tag": tag,
        "started_at": now(),
        "ended_at": "PENDING",
        "hpl_commit": _git_value(layout, "rev-parse", "HEAD"),
        "launcher_version": "hpl-03/v1",
        "python_version": identity["python_version"],
        "career_emulator_version": "1.0.1",
        "career_emulator_bdci26_version": "1.0.0",
        "dataset_source": "HPL_INSTALLED_BDCI26_DEV",
        "dataset_split": "dev",
        "dataset_root": "career_emulator_bdci26/dev/dataset",
        "hpl_venv_root": "HPL_DEDICATED_VENV",
        "hpl_runtime_root": "runs/" + identifier,
        "provider_used": False,
        "provider_evidence_basis": "Validated HPL dependency closure; direct local GameEngine; no provider path",
        "public_evidence_schema_version": SCHEMA_VERSION,
    }
    recorder = RunRecorder(root, manifest)
    try:
        from career_emulator.game import GameEngine

        engine = GameEngine(
            **engine_constructor_kwargs(identity["dataset"]["engine_paths"], runtime / "career_emulator.sqlite3")
        )
        # Storage defaults freeze on first import. Explicitly route every fresh run's
        # existing store before any engine IO, including subsequent games in this process.
        engine.store.log_dir = logs
    except Exception as error:
        recorder.failure(error)
        raise
    return PublicGameAdapter(engine, identifier), recorder


class HumanGameController:
    def __init__(self, factory=create_human_run):
        self._factory = factory
        self._adapter = None
        self.recorder = None
        self.view = None
        self.phase = "START"
        self.busy = False
        self.error = ""
        self.history = []
        self._submitted = set()

    async def start(self, tag="local"):
        if self.busy or self.phase == "ACTIVE":
            return False
        tag = tag.strip() or "local"
        if len(tag) > 64 or _KNOWN_SECRET_PATTERNS.search(tag) or re.search(r"[\x00-\x1f]", tag):
            self.error = "参与者标签无效，请使用简短昵称。"
            return False
        self.busy = True
        self.error = ""
        self.view = None
        self.history = []
        self._submitted.clear()
        self.recorder = None
        try:
            self._adapter, self.recorder = self._factory(tag)
            self.view = await self._adapter.start()
            self.recorder.transition(self.view)
            self.phase = self.view.phase
            return True
        except (Exception, asyncio.CancelledError) as error:
            self._fail(error)
            return False
        finally:
            self.busy = False

    async def choose(self, choice, revision, run_id=None):
        if self.busy or self.phase != "ACTIVE" or not self.view:
            return False
        if revision != self.view.revision or revision in self._submitted:
            return False
        if run_id is not None and run_id != self.view.run_id:
            return False
        legal = {item["choice"]: item for item in self.view.facts["choices"]}
        if type(choice) is not int or choice not in legal:
            return False
        self.busy = True
        self._submitted.add(revision)
        selection = {"choice": choice, "action": legal[choice]["action"]}
        try:
            self.recorder.submission(selection)
            view = await self._adapter.act(choice)
            self.recorder.transition(view, selection)
            self.history.append(selection)
            self.history = self.history[-8:]
            self.view = view
            self.phase = view.phase
            return True
        except (Exception, asyncio.CancelledError) as error:
            self._fail(error)
            return False
        finally:
            self.busy = False

    def _fail(self, error):
        self.phase = "TECHNICAL_FAILURE"
        self.error = "本局发生技术失败，已停止操作。动作结果未知，请保留本局资料并开始全新一局。"
        if self.recorder:
            try:
                self.recorder.failure(error)
            except Exception:
                self.error += " 公共归档未完成；本地 journal 与技术日志仍保留。"
