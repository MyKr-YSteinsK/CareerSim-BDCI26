"""Static packaging contract for the current Candidate bundle."""

import json
import subprocess
import sys
from pathlib import Path

from career_sim_runner.skill_contract import list_bundle_skill_ids, validate_submission_contract


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_SKILLS = {
    "structured-state-board",
    "rolling-planning",
    "delivery-progress",
    "risk-review",
}


def _build(output: Path) -> None:
    subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/package_candidate.py"),
            "--repo-root",
            str(ROOT),
            "--output",
            str(output),
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )


def test_candidate_bundle_is_deterministic_and_matches_runner_contract(tmp_path: Path) -> None:
    first = tmp_path / "submission-a"
    second = tmp_path / "submission-b"
    _build(first)
    _build(second)

    relative_files = {
        path.relative_to(first).as_posix()
        for path in first.rglob("*")
        if path.is_file()
    }
    assert relative_files == {
        "manifest.json",
        *(f"skills/{name}/SKILL.md" for name in EXPECTED_SKILLS),
    }
    for relative in relative_files:
        assert (first / relative).read_bytes() == (second / relative).read_bytes()

    manifest_bytes = (ROOT / "configs/runtime_manifest.json").read_bytes()
    assert (first / "manifest.json").read_bytes() == manifest_bytes
    manifest = json.loads(manifest_bytes.decode("utf-8"))
    assert manifest["mode"] == "agent"
    assert manifest["name"] == "candidate-v7q-checkpoint-marginal-progression"
    assert manifest["instruction"]
    assert set(list_bundle_skill_ids(first)) == EXPECTED_SKILLS
    for name in EXPECTED_SKILLS:
        assert (first / "skills" / name / "SKILL.md").read_bytes() == (
            ROOT / "skills" / name / "SKILL.md"
        ).read_bytes()

    details = validate_submission_contract(first)
    assert details["submission_mode"] == "skill_bundle"
    assert details["skill_ids"] == sorted(EXPECTED_SKILLS)
