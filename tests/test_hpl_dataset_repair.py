"""Offline regressions for HPL-RUN01 package-default dataset routing."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest

from scripts.hpl_preflight import (
    DATASET_PATHS,
    REQUIRED_DATASET_RESOURCES,
    install_hpl_dataset_mirror,
    verify_dataset_mirror,
)


def test_installed_performance_score_default_path_resolves_without_game(tmp_path: Path) -> None:
    workspace = Path(__file__).resolve().parents[4]
    human_python = workspace / ".local/runtime/human-play-lab/venv/Scripts/python.exe"
    runtime = tmp_path / "not-created"
    probe = (
        "import sys; sys.dont_write_bytecode = True; import json; "
        "from pathlib import Path; from scripts.hpl_preflight import build_preflight; "
        "from career_emulator.failure_conditions import _PERFORMANCE_SCORE_CONFIG_PATH; "
        "p = _PERFORMANCE_SCORE_CONFIG_PATH; p = p if p.is_file() else p.with_suffix('.data'); "
        f"plan = build_preflight(Path({str(runtime)!r})); "
        "print(json.dumps({'resolved': str(p), 'exists': p.is_file(), 'dataset': plan['dataset']}))"
    )
    result = subprocess.run(
        [str(human_python), "-c", probe], check=True, capture_output=True, text=True, timeout=30
    )
    record = json.loads(result.stdout)
    assert record["exists"] is True
    assert Path(record["resolved"]) == Path(record["dataset"]["current_default_path"]) / "performance_score/config.data"
    assert record["dataset"]["distribution_record_verified"] is True
    assert record["dataset"]["default_mirror"]["status"] == "COMPLETE_BYTE_IDENTICAL_DEV_MIRROR"
    assert record["dataset"]["default_mirror"]["file_count"] == 194
    assert not runtime.exists()


@pytest.mark.parametrize("damage", ["missing_performance", "changed_file", "extra_file", "missing_source_resource"])
def test_complete_mirror_rejects_missing_changed_or_extra_files(tmp_path: Path, damage: str) -> None:
    source, mirror = tmp_path / "source", tmp_path / "mirror"
    for directory in (*DATASET_PATHS.values(), "performance_score"):
        (source / directory).mkdir(parents=True)
    for relative in REQUIRED_DATASET_RESOURCES:
        (source / relative).write_bytes(b"opaque synthetic fixture")
    shutil.copytree(source, mirror)
    assert verify_dataset_mirror(source, mirror)["status"] == "COMPLETE_BYTE_IDENTICAL_DEV_MIRROR"
    if damage == "missing_performance":
        (mirror / "performance_score/config.data").unlink()
    elif damage == "changed_file":
        (mirror / "promotion/config.data").write_bytes(b"changed")
    elif damage == "extra_file":
        (mirror / "unexpected.data").write_bytes(b"extra")
    else:
        (source / "performance_score/config.data").unlink()
        (mirror / "performance_score/config.data").unlink()
    with pytest.raises(RuntimeError, match="differs|incomplete"):
        verify_dataset_mirror(source, mirror)


def test_mirror_installer_refuses_formal_agent_interpreter() -> None:
    with pytest.raises(RuntimeError, match="dedicated HPL interpreter"):
        install_hpl_dataset_mirror()
