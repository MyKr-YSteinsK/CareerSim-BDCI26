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
from hpl_client.export import finalize_success
from hpl_client.presentation import choice_disabled_reason
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
    def __init__(self, factory=create_human_run, *, finalizer=finalize_success, layout=None):
        self._factory = factory
        self._adapter = None
        self.recorder = None
        self.view = None
        self.phase = "START"
        self.busy = False
        self.error = ""
        self.history = []
        self._submitted = set()
        self._finalizer = finalizer
        self._layout = layout
        self.rejection = ""
        self.action_status = "IDLE"
        self.export_path = None
        self.export_message = ""
        self.finalization_status = "NOT_STARTED"

    async def start(self, tag="local"):
        if self.busy or self.phase == "ACTIVE":
            return False
        tag = tag.strip() or "local"
        if len(tag) > 64 or _KNOWN_SECRET_PATTERNS.search(tag) or re.search(r"[\x00-\x1f]", tag):
            self.error = "参与者标签无效，请使用简短昵称。"
            return False
        self.busy = True
        self.error = ""
        self.rejection = ""
        self.export_path = None
        self.export_message = ""
        self.finalization_status = "NOT_STARTED"
        self.view = None
        self.history = []
        self._submitted.clear()
        self.recorder = None
        try:
            self._adapter, self.recorder = self._factory(tag)
            self.view = await self._adapter.start()
            self.recorder.transition(self.view)
            self.phase = self.view.phase
            if self.phase == "ENDED":
                await self._finalize_ended()
            return True
        except (Exception, asyncio.CancelledError) as error:
            self._fail(error)
            return False
        finally:
            self.busy = False

    async def choose(self, choice, revision, run_id=None):
        if self.busy:
            return self._reject("该操作正在提交，请等待当前操作完成。")
        if self.phase != "ACTIVE" or not self.view:
            return self._reject("当前操作仍在处理中，或本局已停止。")
        if revision != self.view.revision or revision in self._submitted:
            return self._reject("选项已更新或已提交，请使用当前画面的选择。")
        if run_id is not None and run_id != self.view.run_id:
            return self._reject("这不是当前局的选择，请使用当前画面。")
        legal = {item["choice"]: item for item in self.view.facts["choices"]}
        if type(choice) is not int or choice not in legal:
            return self._reject("无效选择，请使用当前显示的选项。")
        energy = self.view.facts["state"].get("energy")
        rejection = choice_disabled_reason(legal[choice], energy)
        if rejection:
            return self._reject(f"{rejection}。尚未提交动作，可以继续当前局。")
        self.rejection = ""
        self.action_status = "SUBMITTING"
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
            self.action_status = "SUCCESS"
            self.rejection = ""
            if self.phase == "ENDED":
                await self._finalize_ended()
            return True
        except (Exception, asyncio.CancelledError) as error:
            self._fail(error)
            return False
        finally:
            self.busy = False

    def _fail(self, error):
        self.phase = "TECHNICAL_FAILURE"
        self.action_status = "TECHNICAL_FAILURE"
        self.error = "本局发生技术失败，已停止操作。动作结果未知，请保留本局资料并开始全新一局。"
        if self.recorder:
            try:
                self.recorder.failure(error)
            except Exception:
                self.error += " 公共归档未完成；本地 journal 与技术日志仍保留。"

    def _reject(self, message):
        self.rejection = message
        self.action_status = "INVALID_ACTION / NO_MUTATION"
        return False

    async def _finalize_ended(self):
        if self.phase != "ENDED" or not self.recorder:
            return False
        if self.export_path:
            return True
        if self.recorder.root is None:  # Explicit in-memory no-game fixture.
            self.export_message = "离线展示：未生成真实对局包。"
            return False
        self.finalization_status = "EXPORTING"
        try:
            operation = asyncio.create_task(
                asyncio.to_thread(self._finalizer, self.recorder.root, self._layout or resolve_layout())
            )
            try:
                result = await asyncio.shield(operation)
            except asyncio.CancelledError:
                # A known ended game must not be reclassified as an unknown
                # mutation while the filesystem worker is still publishing it.
                result = await operation
            self.export_path, self.finalization_status = result
            self.export_message = (
                "数据包已保存。"
                if self.finalization_status == "SUCCESSFULLY_FINALIZED_AND_EXPORTED"
                else "数据包已验证保存；部分临时资料未能清理，已保留。"
            )
            self._adapter = None
            return True
        except Exception:
            self.finalization_status = "EXPORT_FAILED_RETAINED"
            self.export_message = "导出未完成，本局数据已保留。可重试导出，不会重复游戏操作。"
            return False

    async def finish_export(self):
        """No gameplay calls. Export failures retain the ended run for retry."""
        if self.busy:
            return False
        self.busy = True
        try:
            return await self._finalize_ended()
        finally:
            self.busy = False
