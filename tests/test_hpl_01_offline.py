"""No-game tests for HPL preflight and public evidence projection."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from scripts.hpl_preflight import build_preflight
from scripts.hpl_public_evidence import project_cli_frame


def test_preflight_plans_isolated_storage_without_creating_it(tmp_path: Path) -> None:
    runtime_root = tmp_path / "not-created" / "hpl-run-01"

    plan = build_preflight(runtime_root)

    assert not runtime_root.exists()
    assert plan["execution"] == {
        "cli_launched": False,
        "game_started": False,
        "provider_called": False,
        "dataset_updated": False,
    }
    assert plan["package_identity"] == {
        "career-emulator": "1.0.1",
        "career-emulator-bdci26": "1.0.0",
    }
    assert plan["dataset"]["split"] == "dev"
    assert plan["dataset"]["current_default_identity"] in {"UNKNOWN", "PATH_MATCHES_PINNED_DEV"}
    assert set(plan["dataset"]["engine_paths"]) == {
        "event_dir",
        "fixed_event_dir",
        "failure_conditions_dir",
        "salary_conditions_dir",
        "promotion_dir",
        "talk_mechanism_dir",
        "ending_score_dir",
    }
    assert plan["runtime"]["environment_before_emulator_import"]["CAREER_EMULATOR_DB"].endswith(
        "career_emulator.sqlite3"
    )
    assert plan["runtime"]["environment_before_emulator_import"]["CAREER_EMULATOR_LOG_DIR"].endswith("logs")


def test_preflight_rejects_relative_or_reused_runtime_targets(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="absolute"):
        build_preflight(Path("relative-runtime"))

    runtime_root = tmp_path / "used"
    runtime_root.mkdir()
    (runtime_root / "logs").mkdir()
    with pytest.raises(ValueError, match="already exists"):
        build_preflight(runtime_root)


def test_installed_cli_storage_honors_process_environment_without_writing(tmp_path: Path) -> None:
    db_path = tmp_path / "isolated" / "human.sqlite3"
    log_dir = tmp_path / "isolated" / "logs"
    env = os.environ.copy()
    env["CAREER_EMULATOR_DB"] = str(db_path)
    env["CAREER_EMULATOR_LOG_DIR"] = str(log_dir)
    probe = (
        "import json; from career_emulator.storage import DEFAULT_DB_PATH, DEFAULT_LOG_DIR; "
        "print(json.dumps({'db': str(DEFAULT_DB_PATH), 'logs': str(DEFAULT_LOG_DIR)}))"
    )

    result = subprocess.run(
        [sys.executable, "-c", probe],
        check=True,
        capture_output=True,
        text=True,
        env=env,
        timeout=30,
    )

    assert json.loads(result.stdout) == {"db": str(db_path), "logs": str(log_dir)}
    assert not db_path.exists()
    assert not log_dir.exists()


def test_public_projection_drops_hidden_and_unknown_values() -> None:
    frame = {
        "state": {
            "session_id": "session-public-01",
            "month": 1,
            "quarter": 1,
            "year": 1,
            "level": "L1",
            "health": 8,
            "dignity": 5,
            "skill": 4,
            "network": 3,
            "output": 6,
            "wealth": 10,
            "energy": 8,
            "HiddenRisk": "DO_NOT_STORE_HIDDEN_RISK_8431",
            "statistics": {"counter": "DO_NOT_STORE_COUNTER_8432"},
        },
        "event": {
            "title": "Public event",
            "description": "Participant-visible description",
            "event_id": "DO_NOT_STORE_EVENT_ID_8433",
            "node_id": "DO_NOT_STORE_NODE_ID_8434",
        },
        "choices": [
            {
                "choice": 1,
                "action": "Participant-visible choice",
                "energy_cost": 2,
                "status_updates": {"health": "DO_NOT_STORE_EFFECT_8435"},
            }
        ],
        "human_selection": {"choice": 1, "action": "Participant-visible choice"},
        "warning": "Participant-visible warning",
        "final_result": {
            "outcome": "48-month completion",
            "survival_months": 48,
            "grade": "B",
            "quantitative_score": 64.0,
            "competition_partial_score": 44.8,
            "dimensions": [{"component": "DO_NOT_STORE_COMPONENT_8436"}],
        },
        "public_log": [
            {"month": 1, "event_title": "Public event", "choice": 1, "action": "Participant-visible choice"},
            {"effects": "DO_NOT_STORE_LOG_EFFECT_8437"},
            "Log file: D:\\private\\human.log",
        ],
        "human_interpretation": {"text": "My interpretation", "created_at": "2026-09-30T00:00:00+08:00"},
    }

    projected = project_cli_frame(frame)
    serialized = json.dumps(projected, ensure_ascii=False)

    assert projected["schema_version"] == "hpl-public-evidence/v1"
    assert projected["public_status"] == "PUBLIC_STATUS_UNKNOWN"
    assert projected["observed_fact"]["state"]["health"] == 8
    assert projected["observed_fact"]["event"]["title"] == "Public event"
    assert projected["observed_fact"]["choices"][0]["action"] == "Participant-visible choice"
    assert projected["observed_fact"]["human_selection"]["choice"] == 1
    assert projected["observed_fact"]["public_log"] == [
        {"month": 1, "event_title": "Public event", "choice": 1, "action": "Participant-visible choice"}
    ]
    assert projected["human_interpretation"]["text"] == "My interpretation"
    assert "human_interpretation" not in projected["observed_fact"]
    assert "observed_fact" in projected and "human_interpretation" in projected
    assert projected["unknown_fields"] == sorted(projected["unknown_fields"])
    assert any("HiddenRisk" in path for path in projected["unknown_fields"])
    assert any("event_id" in path for path in projected["unknown_fields"])
    assert any("node_id" in path for path in projected["unknown_fields"])
    assert any("status_updates" in path for path in projected["unknown_fields"])
    assert any("dimensions" in path for path in projected["unknown_fields"])
    assert any("public_log[1].effects" in path for path in projected["unknown_fields"])
    assert any("public_log[2]" in path for path in projected["unknown_fields"])
    assert all(
        marker not in serialized
        for marker in (
            "DO_NOT_STORE_HIDDEN_RISK_8431",
            "DO_NOT_STORE_COUNTER_8432",
            "DO_NOT_STORE_EVENT_ID_8433",
            "DO_NOT_STORE_NODE_ID_8434",
            "DO_NOT_STORE_EFFECT_8435",
            "DO_NOT_STORE_COMPONENT_8436",
            "DO_NOT_STORE_LOG_EFFECT_8437",
        )
    )


def test_allowlisted_frame_is_clean_and_keeps_interpretation_separate() -> None:
    frame = {
        "state": {"month": 1},
        "event": {"title": "Public event", "description": "Visible description"},
        "choices": [{"choice": 1, "action": "Visible action", "energy_cost": 2}],
        "human_selection": {"choice": 1, "action": "Visible action"},
        "warning": "Visible warning",
        "handbook": "Visible handbook",
        "action_receipt": {"status": "accepted", "message": "Visible receipt"},
        "final_result": {"outcome": "complete", "survival_months": 1},
        "review": {"month": 1, "text": "Visible review"},
        "promotion": {"month": 1, "from_level": "L1", "to_level": "L2"},
        "public_log": [{"month": 1, "event_title": "Public event", "choice": 1, "action": "Visible action"}],
        "human_interpretation": {"created_at": "2026-09-30T00:00:00+08:00", "text": "My interpretation"},
    }

    projected = project_cli_frame(frame)

    assert projected["public_status"] == "PUBLIC_FIELDS_ALLOWLISTED"
    assert projected["unknown_fields"] == []
    assert projected["human_interpretation"]["text"] == "My interpretation"
    assert "human_interpretation" not in projected["observed_fact"]


def test_hidden_looking_text_is_marked_unknown_and_omitted() -> None:
    projected = project_cli_frame({"warning": "HiddenRisk=900"})

    assert projected["public_status"] == "PUBLIC_STATUS_UNKNOWN"
    assert projected["observed_fact"] == {}
    assert "warning" in projected["unknown_fields"]
    assert "event.event_id" not in projected["unknown_fields"]
    assert "event.node_id" not in projected["unknown_fields"]
