"""Quarter continuation and confirmed restart safety using synthetic engines only."""

import asyncio
import json
import threading
import uuid
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import ProxyHandler, Request, build_opener

import pytest

from hpl_client.controller import HumanGameController
from hpl_client.fixtures import FixtureRecorder
from hpl_client.game_adapter import PublicGameAdapter
from hpl_client.path_contract import HPLLayout
from hpl_client.presentation import choice_disabled_reason
from hpl_client.recorder import RunRecorder
from hpl_client.web import LocalWebServer, WebApplication, fixture_controller


class QuarterMultiActionFixture:
    """Synthetic public API fixture for repeated choices in one quarter."""

    costs = {1: 2, 2: 1, 3: 1}

    def __init__(self, *, fail_on_call=None):
        self.energy = 3
        self.action_calls = []
        self.fail_on_call = fail_on_call

    async def new_game(self):
        return type("NewGameReceipt", (), {"session_id": "quarter-fixture", "error": ""})()

    async def enrollment_handbook(self):
        return "Synthetic quarterly action fixture."

    async def observe(self, session_id):
        in_quarter = self.energy > 0
        choices = (
            [
                {"choice": 1, "action": "Quarter action costing two", "energy_cost": 2},
                {"choice": 2, "action": "Quarter action costing one B", "energy_cost": 1},
                {"choice": 3, "action": "Quarter action costing one C", "energy_cost": 1},
            ]
            if in_quarter
            else [{"choice": 4, "action": "Next quarter main action"}]
        )
        return type(
            "Observation",
            (),
            {
                "current_state": {
                    "session_id": session_id,
                    "time": {"current_month": 3, "current_quarter": 1, "current_year": 1},
                    "status": {
                        "level": "L1",
                        "health": 5,
                        "dignity": 5,
                        "skill": 1,
                        "network": 1,
                        "output": 0,
                        "wealth": 1,
                        "energy": self.energy,
                    },
                },
                "current_event": {
                    "title": "Quarterly energy allocation" if in_quarter else "Quarterly main action",
                    "description": "Synthetic fixture event.",
                },
                "choices": choices,
                "warning": "",
                "ending_score": None,
            },
        )()

    async def take_action(self, session_id, choice, notes=""):
        self.action_calls.append(choice)
        if self.fail_on_call == len(self.action_calls):
            raise OSError("fixture outcome unknown")
        cost = self.costs.get(choice)
        if cost is None or cost > self.energy:
            return type("Receipt", (), {"success": False, "error": "invalid or insufficient"})()
        self.energy -= cost
        return type("Receipt", (), {"success": True, "error": None})()


class QuarterRecorder(FixtureRecorder):
    def __init__(self):
        self.submissions = []

    def submission(self, selection):
        self.submissions.append(selection)


def quarter_controller(engine):
    recorder = QuarterRecorder()
    controller = HumanGameController(lambda _: (PublicGameAdapter(engine, "quarter-fixture"), recorder))
    return controller, recorder


@pytest.mark.parametrize(
    ("choices", "energies"),
    [([1, 2], [1, 0]), ([2, 1], [2, 0])],
    ids=["cost-2-then-1", "cost-1-then-2"],
)
def test_quarter_multi_action_continues_through_fresh_public_observations(choices, energies):
    engine = QuarterMultiActionFixture()
    controller, recorder = quarter_controller(engine)

    async def exercise():
        assert await controller.start("fixture")
        assert controller.view.facts["state"]["energy"] == 3
        first_revision = controller.view.revision
        assert await controller.choose(choices[0], first_revision, "quarter-fixture")
        first_result = controller.view
        assert first_result.facts["state"]["energy"] == energies[0]
        if energies[0] == 1:
            assert first_result.facts["event"]["title"] == "Quarterly energy allocation"
            assert choice_disabled_reason(first_result.facts["choices"][0], 1)
            assert choice_disabled_reason(first_result.facts["choices"][1], 1) is None
        assert first_result.revision != first_revision
        assert await controller.choose(choices[1], first_result.revision, "quarter-fixture")
        assert controller.view.facts["state"]["energy"] == energies[1]
        assert controller.view.facts["event"]["title"] == "Quarterly main action"
        assert controller.view.projection["unknown_fields"] == []

    asyncio.run(exercise())
    assert engine.action_calls == choices
    assert [item["choice"] for item in recorder.submissions] == choices


def test_quarter_insufficient_energy_and_stale_revision_reject_without_mutation():
    engine = QuarterMultiActionFixture()
    controller, recorder = quarter_controller(engine)

    async def exercise():
        assert await controller.start("fixture")
        first_revision = controller.view.revision
        assert await controller.choose(1, first_revision, "quarter-fixture")
        current = controller.view
        before = (engine.energy, list(engine.action_calls), list(recorder.submissions))
        assert not await controller.choose(2, first_revision, "quarter-fixture")
        assert not await controller.choose(1, current.revision, "quarter-fixture")
        assert (engine.energy, engine.action_calls, recorder.submissions) == before
        assert controller.view is current

    asyncio.run(exercise())
    assert engine.action_calls == [1]
    assert len(recorder.submissions) == 1


def test_quarter_duplicate_and_unknown_second_action_do_not_retry():
    engine = QuarterMultiActionFixture(fail_on_call=2)
    controller, _ = quarter_controller(engine)

    async def exercise():
        assert await controller.start("fixture")
        old_revision = controller.view.revision
        assert await controller.choose(1, old_revision, "quarter-fixture")
        current_revision = controller.view.revision
        result = await asyncio.gather(
            controller.choose(2, current_revision, "quarter-fixture"),
            controller.choose(2, current_revision, "quarter-fixture"),
        )
        assert sorted(result) == [False, False]
        assert controller.phase == "TECHNICAL_FAILURE"
        assert not await controller.choose(2, current_revision, "quarter-fixture")
        assert not await controller.quick_restart("fixture", "quarter-fixture")

    asyncio.run(exercise())
    assert engine.action_calls == [1, 2]


def test_web_api_accepts_second_quarter_action_using_updated_revision():
    engine = QuarterMultiActionFixture()
    controller, _ = quarter_controller(engine)
    app = WebApplication(controller, fixture=True)
    try:
        started, _ = app.operation("start", {"request_id": str(uuid.uuid4()), "participant": "fixture"})
        assert started and app.state()["restart_available"]
        state = app.state()
        first_id = str(uuid.uuid4())
        first_request = {
            "request_id": first_id,
            "choice": 1,
            "revision": state["revision"],
            "run_id": state["run_id"],
        }
        accepted, _ = app.operation("choose", first_request)
        assert accepted
        after_first = app.state()
        assert after_first["facts"]["state"]["energy"] == 1
        assert after_first["choices"][0]["disabled_reason"]
        assert after_first["choices"][1]["disabled_reason"] is None
        accepted, _ = app.operation(
            "choose",
            {
                "request_id": str(uuid.uuid4()),
                "choice": 2,
                "revision": after_first["revision"],
                "run_id": after_first["run_id"],
            },
        )
        assert accepted
        assert app.state()["facts"]["state"]["energy"] == 0
        assert app.state()["facts"]["event"]["title"] == "Quarterly main action"
        assert not app.operation("choose", first_request)[0]
    finally:
        app.close()


def _run_factory(layout, created):
    def factory(tag):
        run_id = uuid.uuid4().hex
        root = layout.runs_root / run_id
        root.mkdir(parents=True)
        recorder = RunRecorder(
            root,
            {
                "run_id": run_id,
                "authorization_id": "USER_WEB_START_CLICK",
                "human_tag": tag,
                "provider_used": False,
            },
        )
        engine = QuarterMultiActionFixture()
        created.append((root, engine))
        return PublicGameAdapter(engine, run_id), recorder

    return factory


def test_confirmed_quick_restart_deletes_only_current_active_run_and_starts_fresh(tmp_path):
    layout = HPLLayout(tmp_path, tmp_path / "worktree", tmp_path / "sandbox")
    exports = layout.sandbox_root / "exports"
    exports.mkdir(parents=True)
    saved_export = exports / "prior-verified-export.zip"
    saved_export.write_bytes(b"preserved export")
    created = []
    controller = HumanGameController(_run_factory(layout, created), layout=layout)

    async def exercise():
        assert await controller.start("P017")
        old_root, old_engine = created[0]
        old_id = controller.view.run_id
        assert old_root.exists() and controller.can_quick_restart()
        assert await controller.quick_restart("P017", old_id)
        new_root, new_engine = created[1]
        assert not old_root.exists() and new_root.exists()
        assert saved_export.read_bytes() == b"preserved export"
        assert controller.phase == "ACTIVE" and controller.view.run_id != old_id
        assert old_engine.action_calls == new_engine.action_calls == []

    asyncio.run(exercise())
    assert len(created) == 2


def test_successfully_exported_ending_can_restart_and_deletes_only_its_zip(tmp_path):
    controller = fixture_controller(tmp_path)

    async def exercise():
        assert await controller.start("P017")
        old_id = controller.view.run_id
        assert await controller.choose(1, controller.view.revision, old_id)
        assert controller.phase == "ENDED"
        assert controller.finalization_status == "SUCCESSFULLY_FINALIZED_AND_EXPORTED"
        export = controller.export_path
        assert export.is_file() and not controller.recorder.root.exists()
        unrelated_export = export.parent / "unrelated-history.zip"
        unrelated_export.write_bytes(b"another run")
        assert controller.can_quick_restart()
        assert await controller.quick_restart("P017", old_id)
        assert controller.phase == "ACTIVE" and controller.view.run_id != old_id
        assert not export.exists()
        assert unrelated_export.read_bytes() == b"another run"

    asyncio.run(exercise())


def test_quick_restart_refuses_held_failed_export_and_stale_runs(tmp_path):
    layout = HPLLayout(tmp_path, tmp_path / "worktree", tmp_path / "sandbox")
    created = []
    controller = HumanGameController(_run_factory(layout, created), layout=layout)

    async def exercise():
        assert await controller.start("P017")
        root, _ = created[0]
        current_id = controller.view.run_id
        (root / "FORENSIC_HOLD.txt").write_text("hold", encoding="utf-8")
        assert not controller.can_quick_restart()
        assert not await controller.quick_restart("P017", current_id)
        assert not await controller.quick_restart("P017", "stale-run")
        assert root.exists() and len(created) == 1

        (root / "FORENSIC_HOLD.txt").unlink()
        receipt_path = root / "staging" / "manifest.json"
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        receipt.update(run_status="TECHNICAL_FAILURE", action_outcome="UNKNOWN_AFTER_TECHNICAL_FAILURE")
        receipt_path.write_text(json.dumps(receipt), encoding="utf-8")
        assert not controller.can_quick_restart()
        assert not await controller.quick_restart("P017", current_id)
        assert root.exists() and len(created) == 1

        controller.phase = "ENDED"
        controller.finalization_status = "EXPORT_FAILED_RETAINED"
        assert not controller.can_quick_restart()
        assert not await controller.quick_restart("P017", current_id)
        assert root.exists() and len(created) == 1

    asyncio.run(exercise())


def test_quick_restart_cleanup_failure_never_starts_new_run(tmp_path, monkeypatch):
    layout = HPLLayout(tmp_path, tmp_path / "worktree", tmp_path / "sandbox")
    created = []
    controller = HumanGameController(_run_factory(layout, created), layout=layout)

    async def exercise():
        assert await controller.start("P017")
        root = created[0][0]
        monkeypatch.setattr(
            "hpl_client.controller.discard_active_run", lambda *a, **k: (_ for _ in ()).throw(OSError())
        )
        assert not await controller.quick_restart("P017", controller.view.run_id)
        assert controller.action_status == "RESTART_FAILED / NO_NEW_RUN"
        assert controller.phase == "ACTIVE" and root.exists() and len(created) == 1

    asyncio.run(exercise())


@pytest.fixture
def web_client(tmp_path):
    app = WebApplication(fixture_controller(tmp_path))
    server = LocalWebServer(app)
    thread = threading.Thread(target=server.serve_forever, kwargs={"poll_interval": 0.01})
    thread.start()
    yield server, app
    server.shutdown()
    thread.join()
    server.server_close()
    app.close()


def _post(server, path, body):
    headers = {
        "Content-Type": "application/json",
        "X-HPL-Token": server.application.token,
        "Origin": server.origin,
    }
    request = Request(server.origin + path, data=json.dumps(body).encode(), headers=headers)
    try:
        with build_opener(ProxyHandler({})).open(request, timeout=5) as response:
            return response.status, json.loads(response.read())
    except HTTPError as error:
        return error.code, json.loads(error.read())


def test_web_restart_requires_confirmation_ui_and_runs_only_synthetic_fixture(web_client):
    server, app = web_client
    assert b"restart-confirm" in Path(__file__).parents[1].joinpath("hpl_client/web_assets/index.html").read_bytes()
    assets = (Path(__file__).parents[1] / "hpl_client" / "web_assets" / "app.js").read_text(encoding="utf-8")
    assert '$("restart-open").addEventListener("click"' in assets
    assert '$("restart-confirm-go").addEventListener("click"' in assets
    assert '$("restart-confirm").showModal()' in assets
    assert 'operation("restart"' in assets
    assert app.controller.view is None

    status, result = _post(
        server,
        "/api/start",
        {"request_id": str(uuid.uuid4()), "participant": "FIXTURE-P017"},
    )
    assert status == 200 and result["state"]["mode"] == "FIXTURE / NON_GAME"
    old_root = app.controller.recorder.root
    old_engine = app.controller._adapter._engine
    old_id = app.controller.view.run_id
    assert result["state"]["restart_available"] is True
    assert old_root.exists() and old_engine.action_calls == 0

    status, result = _post(
        server,
        "/api/restart",
        {"request_id": str(uuid.uuid4()), "participant": "FIXTURE-P017", "run_id": old_id},
    )
    assert status == 200 and result["state"]["mode"] == "FIXTURE / NON_GAME"
    assert result["state"]["phase"] == "ACTIVE"
    assert not old_root.exists() and app.controller.recorder.root.exists()
    assert app.controller.view.run_id != old_id
    assert old_engine.action_calls == app.controller._adapter._engine.action_calls == 0
