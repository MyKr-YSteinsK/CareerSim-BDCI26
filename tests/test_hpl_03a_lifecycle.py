"""HPL-03A ending, safe archive publication, and scoped cleanup contracts."""

import asyncio
import shutil
import zipfile
import hashlib
import json

import pytest

from hpl_client.cleanup import assert_cleanup_target, cleanup_success
from hpl_client.export import ARTIFACTS, export_run, finalize_success, readable_filename, verify_zip
from hpl_client.fixtures import FixtureEngine
from hpl_client.game_adapter import PublicGameAdapter
from hpl_client.recorder import RunRecorder
from scripts.hpl_play import HPLLayout, resolve_layout


def setup_ended_run(tmp_path, monkeypatch=None, *, suffix="a", tag="P017", score=68.25, level="L2", finalize=True):
    workspace = tmp_path / "workspace"
    sandbox = workspace / ".local" / "runtime" / "human-play-lab"
    worktree = workspace / ".local" / "worktrees" / "human-play-lab"
    runs = sandbox / "runs"
    runs.mkdir(parents=True, exist_ok=True)
    layout = HPLLayout(workspace, worktree, sandbox)
    root = runs / (suffix * 32)
    root.mkdir()
    (root / "runtime" / "logs").mkdir(parents=True)
    (root / "runtime" / "career_emulator.sqlite3").write_bytes(b"fixture-db-private")
    (root / "runtime" / "logs" / "session.log").write_text("fixture-private-log", encoding="utf-8")
    fields = {
        "authorization_id": "USER_GUI_START_CLICK",
        "human_tag": tag,
        "started_at": "2026-10-01T18:34:12+08:00",
        "ended_at": "2026-10-01T19:34:12+08:00",
        "hpl_commit": "fixture-parent",
        "launcher_version": "hpl-03/v1",
        "python_version": "3.12.13",
        "career_emulator_version": "1.0.1",
        "career_emulator_bdci26_version": "1.0.0",
        "dataset_source": "HPL_INSTALLED_BDCI26_DEV",
        "dataset_split": "dev",
        "dataset_root": "career_emulator_bdci26/dev/dataset",
        "hpl_venv_root": "HPL_DEDICATED_VENV",
        "hpl_runtime_root": "runs/" + root.name,
        "provider_used": False,
        "provider_evidence_basis": "offline fixture",
        "public_evidence_schema_version": "hpl-public-evidence/v1",
    }
    recorder = RunRecorder(root, {"run_id": root.name, **fields})
    if monkeypatch:
        monkeypatch.setattr("hpl_client.recorder.now", lambda: fields["ended_at"])
    engine = FixtureEngine(ending=True, energy=8)
    view = asyncio.run(PublicGameAdapter(engine, root.name).start())
    frame = view.facts
    frame["state"]["level"] = level
    frame["final_result"]["quantitative_score"] = score
    from dataclasses import replace

    view = replace(view, projection={**view.projection, "observed_fact": frame})
    if finalize:
        recorder.transition(view)
        assert recorder.manifest["run_status"] == "ENDED"
    return layout, root, recorder


def test_filename_contract_formats_public_score_level_and_local_end_time():
    manifest = {"human_tag": "P017", "ended_at": "2026-10-01T19:34:12+08:00"}
    frames = [{"observed_fact": {"state": {"level": "L2"}, "final_result": {"quantitative_score": 68.25}}}]
    assert readable_filename(manifest, frames) == "CareerSim-P017-Score68.25-L2-20261001-193412.zip"
    manifest["human_tag"] = "P/017:*?"
    frames[0]["observed_fact"]["state"].pop("level")
    frames[0]["observed_fact"]["final_result"].pop("quantitative_score")
    assert readable_filename(manifest, frames) == "CareerSim-P_017-ScoreNA-LNA-20261001-193412.zip"


def test_success_publication_is_verified_before_whole_run_cleanup(tmp_path, monkeypatch):
    layout, root, _ = setup_ended_run(tmp_path, monkeypatch)
    stable, status = finalize_success(root, layout)
    assert status == "SUCCESSFULLY_FINALIZED_AND_EXPORTED"
    assert stable.parent == layout.sandbox_root / "exports"
    manifest, frames, content = verify_zip(stable, root.name)
    assert manifest["run_status"] == "ENDED"
    assert frames[-1]["observed_fact"]["state"]["session_id"] == manifest["session_id"]
    assert set(content) == set(ARTIFACTS)
    assert stable.name == "CareerSim-P017-Score68.25-L2-20261001-193412.zip"
    assert not root.exists()
    with zipfile.ZipFile(stable) as archive:
        assert set(archive.namelist()) == {*ARTIFACTS, "README.txt"}
        assert b"fixture-db-private" not in b"".join(archive.read(name) for name in archive.namelist())


def test_name_collision_appends_small_suffix_without_overwrite(tmp_path, monkeypatch):
    layout, root_a, _ = setup_ended_run(tmp_path, monkeypatch, suffix="a")
    zip_a, _ = finalize_success(root_a, layout)
    original = hashlib.sha256(zip_a.read_bytes()).hexdigest()
    layout, root_b, _ = setup_ended_run(tmp_path, monkeypatch, suffix="b")
    zip_b, _ = finalize_success(root_b, layout)
    assert zip_b.name == "CareerSim-P017-Score68.25-L2-20261001-193412-2.zip"
    assert hashlib.sha256(zip_a.read_bytes()).hexdigest() == original


def test_zip_verification_failure_retains_run_and_never_publishes(tmp_path, monkeypatch):
    layout, root, _ = setup_ended_run(tmp_path, monkeypatch)
    monkeypatch.setattr("hpl_client.export.verify_zip", lambda *args: (_ for _ in ()).throw(ValueError("bad ZIP")))
    with pytest.raises(ValueError, match="bad ZIP"):
        finalize_success(root, layout)
    assert root.exists()
    assert not (layout.sandbox_root / "exports").exists()


def test_cleanup_rechecks_the_stable_zip_and_retains_material_when_it_fails(tmp_path, monkeypatch):
    layout, root, _ = setup_ended_run(tmp_path, monkeypatch)
    source = export_run(root)
    directory = layout.sandbox_root / "exports"
    directory.mkdir()
    stable = directory / source.name
    shutil.copyfile(source, stable)
    monkeypatch.setattr(
        "hpl_client.cleanup.verify_zip", lambda *args: (_ for _ in ()).throw(ValueError("bad stable ZIP"))
    )
    with pytest.raises(ValueError, match="bad stable ZIP"):
        cleanup_success(root, stable, layout)
    assert root.exists()


@pytest.mark.parametrize("status", ["ACTIVE", "TECHNICAL_FAILURE"])
def test_cleanup_rejects_independent_hold_and_active_or_technical_run(tmp_path, monkeypatch, status):
    layout, root, _ = setup_ended_run(tmp_path, monkeypatch)
    (root / "FORENSIC_HOLD").write_text("fixture", encoding="utf-8")
    with pytest.raises(ValueError, match="forensic hold"):
        assert_cleanup_target(root, layout)
    (root / "FORENSIC_HOLD").unlink()
    manifest = json.loads((root / "staging" / "manifest.json").read_text(encoding="utf-8"))
    manifest["run_status"] = status
    (root / "staging" / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    with pytest.raises(ValueError, match="normal ended"):
        finalize_success(root, layout)
    assert root.exists()


def test_hpl_run01_identity_is_rejected_before_path_inspection():
    layout = resolve_layout()
    target = layout.runs_root / "47472aa8b73b4bf6847209f99a8abb39"
    with pytest.raises(ValueError, match="protected"):
        assert_cleanup_target(target, layout)


@pytest.mark.parametrize(
    "energy,choice,revision,run_id",
    [
        (1, 1, 1, "fixture"),
        (8, 99, 1, "fixture"),
        (8, True, 1, "fixture"),
        (8, "1", 1, "fixture"),
        (8, 1, 0, "fixture"),
        (8, 1, 1, "old-run"),
    ],
)
def test_invalid_action_has_no_engine_or_canonical_mutation(energy, choice, revision, run_id):
    from hpl_client.controller import HumanGameController
    from hpl_client.fixtures import FixtureRecorder

    class Recorder(FixtureRecorder):
        transitions = 0
        submissions = 0

        def transition(self, *args):
            self.transitions += 1

        def submission(self, *args):
            self.submissions += 1

    engine, recorder = FixtureEngine(energy=energy), Recorder()
    controller = HumanGameController(lambda tag: (PublicGameAdapter(engine, "fixture"), recorder))

    async def exercise():
        assert await controller.start()
        before = controller.view
        assert not await controller.choose(choice, revision, run_id)
        assert controller.view == before

    asyncio.run(exercise())
    assert engine.action_calls == 0
    assert recorder.transitions == 1 and recorder.submissions == 0
    assert controller.phase == "ACTIVE" and not controller.error
    assert controller.action_status == "INVALID_ACTION / NO_MUTATION" and controller.rejection


def test_duplicate_callback_is_rejected_without_technical_failure():
    from hpl_client.controller import HumanGameController
    from hpl_client.fixtures import FixtureRecorder

    class SlowEngine(FixtureEngine):
        async def take_action(self, *args, **kwargs):
            await asyncio.sleep(0)
            return await super().take_action(*args, **kwargs)

    engine = SlowEngine()
    controller = HumanGameController(lambda tag: (PublicGameAdapter(engine, "fixture"), FixtureRecorder()))

    async def exercise():
        await controller.start()
        first = asyncio.create_task(controller.choose(1, controller.view.revision, "fixture"))
        await asyncio.sleep(0)
        assert not await controller.choose(1, controller.view.revision, "fixture")
        assert controller.rejection and controller.action_status == "INVALID_ACTION / NO_MUTATION"
        assert controller.phase == "ACTIVE"
        assert await first
        assert not await controller.choose(1, 1, "fixture")

    asyncio.run(exercise())
    assert engine.action_calls == 1 and controller.phase == "ACTIVE"


def test_terminal_action_automatically_exports_and_cleans(tmp_path, monkeypatch):
    from hpl_client.controller import HumanGameController

    layout, root, recorder = setup_ended_run(tmp_path, monkeypatch, finalize=False)
    # Start from an unfinalized synthetic run; no prior canonical bundle.
    recorder = RunRecorder(root, {**recorder.manifest, "run_status": "ACTIVE", "ended_at": "PENDING"})

    class EndingEngine(FixtureEngine):
        async def take_action(self, *args, **kwargs):
            receipt = await super().take_action(*args, **kwargs)
            self.ending = True
            return receipt

    engine = EndingEngine()
    controller = HumanGameController(lambda tag: (PublicGameAdapter(engine, root.name), recorder), layout=layout)

    async def exercise():
        assert await controller.start()
        assert await controller.choose(1, controller.view.revision, root.name)
        assert controller.phase == "ENDED"
        assert controller.finalization_status == "SUCCESSFULLY_FINALIZED_AND_EXPORTED"
        assert not await controller.choose(1, controller.view.revision, root.name)

    asyncio.run(exercise())
    assert engine.action_calls == 1 and controller.export_path.is_file() and not root.exists()


def test_export_failure_retry_is_only_io_and_keeps_ended_phase(tmp_path, monkeypatch):
    from hpl_client.controller import HumanGameController

    layout, root, recorder = setup_ended_run(tmp_path, monkeypatch)
    engine = FixtureEngine(ending=True)
    calls = []

    def flaky_finalizer(root, layout):
        calls.append(root)
        if len(calls) == 1:
            raise OSError("fixture disk error")
        return finalize_success(root, layout)

    controller = HumanGameController(
        lambda tag: (PublicGameAdapter(engine, root.name), recorder), finalizer=flaky_finalizer, layout=layout
    )

    async def exercise():
        assert await controller.start()
        assert root.exists() and controller.phase == "ENDED"
        assert controller.finalization_status == "EXPORT_FAILED_RETAINED"
        assert "已保留" in controller.export_message
        assert await controller.finish_export()

    asyncio.run(exercise())
    assert len(calls) == 2 and engine.action_calls == 0 and not root.exists()


def test_windows_lock_keeps_verified_archive_and_pending_cleanup(tmp_path, monkeypatch):
    layout, root, _ = setup_ended_run(tmp_path, monkeypatch)
    monkeypatch.setattr(
        "hpl_client.cleanup.shutil.rmtree", lambda *args: (_ for _ in ()).throw(PermissionError("locked"))
    )
    stable, status = finalize_success(root, layout)
    assert root.exists() and status == "CLEANUP_PENDING"
    verify_zip(stable, root.name)


def test_ended_export_cancellation_waits_for_known_io_result(tmp_path):
    import threading
    from types import SimpleNamespace
    from hpl_client.controller import HumanGameController

    started, release = threading.Event(), threading.Event()

    def finalizer(root, layout):
        started.set()
        assert release.wait(5)
        return tmp_path / "fixture.zip", "SUCCESSFULLY_FINALIZED_AND_EXPORTED"

    controller = HumanGameController(finalizer=finalizer, layout=object())
    controller.phase = "ENDED"
    controller.recorder = SimpleNamespace(root=tmp_path)

    async def exercise():
        task = asyncio.create_task(controller.finish_export())
        assert await asyncio.to_thread(started.wait, 5)
        task.cancel()
        await asyncio.sleep(0)
        release.set()
        assert await task

    asyncio.run(exercise())
    assert controller.phase == "ENDED" and not controller.busy
    assert controller.finalization_status == "SUCCESSFULLY_FINALIZED_AND_EXPORTED"
