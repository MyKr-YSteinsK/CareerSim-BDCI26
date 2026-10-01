"""Offline single-run gate tests: synthetic engine only, never real gameplay."""

import json
import uuid

import pytest

from hpl_client.controller import HumanGameController
from hpl_client.fixtures import FixtureEngine
from hpl_client.game_adapter import PublicGameAdapter
from hpl_client.recorder import RunRecorder
from hpl_client.web_smoke import SingleRunWebApplication


def start(app, participant="P019"):
    return app.operation("start", {"request_id": str(uuid.uuid4()), "participant": participant})


@pytest.mark.parametrize("failure", [False, True])
def test_one_attempt_survives_end_failure_and_restart(tmp_path, failure):
    calls = []

    def factory(tag):
        calls.append(tag)
        if failure:
            raise RuntimeError("synthetic pre-game failure")
        root = tmp_path / "fixture-run"
        root.mkdir()
        return PublicGameAdapter(FixtureEngine(), "fixture-no-game"), RunRecorder(root, {})

    controller = HumanGameController()
    app = SingleRunWebApplication(controller, tmp_path / "authorization", factory)
    try:
        assert app.state()["start_available"] is True
        assert start(app)[0] is (not failure)
        assert len(calls) == 1
        assert app.state()["start_available"] is False
        if not failure:
            controller.phase = "ENDED"
            assert controller.recorder.manifest["authorization_id"] == "HPL-05A/USER_WEB_START_CLICK"
        original_view = controller.view
        assert start(app) == (False, "SINGLE_RUN_BUDGET_EXHAUSTED/NO_MUTATION")
        assert controller.view is original_view
        records = [json.loads(line) for line in app.timings.read_text().splitlines()]
        completed = [r for r in records if r["event"] == "operation_complete"]
        assert len(completed) == 1 and completed[0]["seconds"] >= 0
    finally:
        app.close()
    restarted = SingleRunWebApplication(HumanGameController(), tmp_path / "authorization", factory)
    try:
        assert start(restarted)[0] is False
        assert len(calls) == 1
    finally:
        restarted.close()


def test_invalid_tag_does_not_reserve_attempt(tmp_path):
    def forbidden(tag):
        raise AssertionError("invalid input reached factory")

    app = SingleRunWebApplication(HumanGameController(), tmp_path, forbidden)
    try:
        assert start(app, "bad\nparticipant")[0] is False
        assert not app.receipt.exists()
        assert app.state()["start_available"] is True
    finally:
        app.close()
