"""Offline lifecycle/duplicate/unknown outcome regressions."""

import asyncio

from hpl_client.controller import HumanGameController
from hpl_client.fixtures import FixtureEngine, FixtureRecorder
from hpl_client.game_adapter import PublicGameAdapter


def test_concurrent_double_callback_and_stale_revision_submit_once():
    class SlowEngine(FixtureEngine):
        calls = 0

        async def take_action(self, *args, **kwargs):
            self.calls += 1
            await asyncio.sleep(0)
            return await super().take_action(*args, **kwargs)

    engine = SlowEngine()
    controller = HumanGameController(lambda tag: (PublicGameAdapter(engine, "fixture"), FixtureRecorder()))

    async def exercise():
        assert await controller.start()
        assert not await controller.start()
        revision = controller.view.revision
        results = await asyncio.gather(controller.choose(1, revision), controller.choose(1, revision))
        assert sorted(results) == [False, True]
        assert not await controller.choose(1, revision)
        assert not await controller.choose(99, controller.view.revision)
        assert not await controller.choose(1, controller.view.revision, "previous-run")
        assert not await controller.choose(True, controller.view.revision)

    asyncio.run(exercise())
    assert engine.calls == 1


def test_unknown_mutation_never_observes_or_retries_and_allows_only_fresh_start():
    class BrokenEngine(FixtureEngine):
        observes = 0
        calls = 0

        async def observe(self, session_id):
            self.observes += 1
            return await super().observe(session_id)

        async def take_action(self, *args, **kwargs):
            self.calls += 1
            raise OSError("unknown mutation")

    engine = BrokenEngine()
    controller = HumanGameController(lambda tag: (PublicGameAdapter(engine, "fixture"), FixtureRecorder()))

    async def exercise():
        await controller.start()
        assert not await controller.choose(1, controller.view.revision)
        assert controller.phase == "TECHNICAL_FAILURE"
        assert not await controller.choose(1, controller.view.revision)
        assert engine.observes == 1 and engine.calls == 1
        assert not controller.busy
        assert await controller.start()

    asyncio.run(exercise())


def test_journal_io_failure_resets_gate_without_submitting():
    class BrokenRecorder(FixtureRecorder):
        def journal(self, *args):
            raise OSError("disk unavailable")

    controller = HumanGameController(lambda tag: (PublicGameAdapter(FixtureEngine(), "fixture"), BrokenRecorder()))

    async def exercise():
        await controller.start()
        assert not await controller.choose(1, controller.view.revision)
        assert controller.phase == "TECHNICAL_FAILURE" and not controller.busy

    asyncio.run(exercise())


def test_startup_no_factory_and_secret_tag_rejected_before_factory():
    def forbidden(tag):
        raise AssertionError("factory must not be called")

    controller = HumanGameController(forbidden)
    assert controller.phase == "START"
    assert not asyncio.run(controller.start("api_key=not-a-participant-tag"))


def test_fresh_run_constructor_routes_db_and_logs_before_io(tmp_path, monkeypatch):
    import os
    import sys
    from types import SimpleNamespace

    from hpl_client import controller as module
    from scripts.hpl_play import HPLLayout
    from scripts.hpl_preflight import DATASET_PATHS

    layout = HPLLayout(
        tmp_path, tmp_path / ".local/worktrees/human-play-lab", tmp_path / ".local/runtime/human-play-lab"
    )
    monkeypatch.setattr(module, "resolve_layout", lambda: layout)
    identity = {
        "python_version": "fixture",
        "dataset": {"engine_paths": {key: str(tmp_path / key) for key in DATASET_PATHS}},
    }
    monkeypatch.setattr(module, "_load_environment_manifest", lambda value: ({}, identity))
    monkeypatch.setattr(module, "_git_value", lambda *args: "fixture-commit")
    monkeypatch.setattr(module.metadata, "version", lambda name: "1.0.1")
    monkeypatch.setenv("CAREER_EMULATOR_DB", "fixture-old-db")
    monkeypatch.setenv("CAREER_EMULATOR_LOG_DIR", "fixture-old-log")
    engines = []

    class Engine:
        def __init__(self, **kwargs):
            assert str(kwargs["db_path"]) == os.environ["CAREER_EMULATOR_DB"]
            self.store = SimpleNamespace(log_dir="import-frozen-old-run")
            self.db_path = kwargs["db_path"]
            engines.append(self)

    monkeypatch.setitem(sys.modules, "career_emulator.game", SimpleNamespace(GameEngine=Engine))
    _, first = module.create_human_run("fixture")
    _, second = module.create_human_run("fixture")
    assert first.root != second.root
    for engine, recorder in zip(engines, (first, second), strict=True):
        assert engine.db_path == recorder.root / "runtime/career_emulator.sqlite3"
        assert engine.store.log_dir == recorder.root / "runtime/logs"
        assert engine.db_path.is_relative_to(layout.runs_root)
