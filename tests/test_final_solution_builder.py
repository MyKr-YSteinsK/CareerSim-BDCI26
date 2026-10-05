"""Focused offline tests for the final solution builder using synthetic repos."""

import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import zipfile
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
BUILDER_PATH = ROOT / "scripts/build_final_solution.py"
EXPECTED_SKILLS = (
    "structured-state-board",
    "rolling-planning",
    "delivery-progress",
    "risk-review",
)
EXPECTED_MEMBERS = {
    "manifest.json",
    "README.md",
    "design/skills_design.md",
    "design/decision_report.md",
    *(f"skills/{skill}/SKILL.md" for skill in EXPECTED_SKILLS),
}
SPEC = importlib.util.spec_from_file_location("career_sim_final_builder", BUILDER_PATH)
assert SPEC is not None and SPEC.loader is not None
builder = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(builder)


def _git(repo: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True, text=True)


def _git_blob(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()


def _synthetic_repo(
    path: Path,
    *,
    status: str = "FINAL_FROZEN_FOR_SUBMISSION",
    candidate_skill_names: tuple[str, ...] = EXPECTED_SKILLS,
    missing_material: str | None = None,
    secret_material: str | None = None,
) -> Path:
    repo = path.resolve()
    repo.mkdir(parents=True)
    manifest = {
        "name": "candidate-synthetic-final",
        "mode": "agent",
        "instruction": "Synthetic public-only final package fixture.",
    }
    manifest_bytes = (json.dumps(manifest, indent=2) + "\n").encode("utf-8")
    (repo / "configs").mkdir()
    (repo / "configs/runtime_manifest.json").write_bytes(manifest_bytes)

    skill_entries = []
    for skill in EXPECTED_SKILLS:
        data = (
            f'---\nname: {skill}\ndescription: "Synthetic offline test Skill."\n---\n'
            f"# {skill}\nFixture content.\n"
        ).encode("utf-8")
        target = repo / "skills" / skill / "SKILL.md"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        if skill in candidate_skill_names:
            skill_entries.append(
                {"name": skill, "path": f"skills/{skill}/SKILL.md", "git_blob": _git_blob(data)}
            )

    candidate = {
        "candidate_id": manifest["name"],
        "status": status,
        "validation": {"next_game_authorized": False},
        "runtime_manifest": {
            "sha256": hashlib.sha256(manifest_bytes).hexdigest(),
            "instruction_sha256": hashlib.sha256(manifest["instruction"].encode("utf-8")).hexdigest(),
        },
        "skills": skill_entries,
    }
    (repo / "configs/current_candidate.json").write_text(
        json.dumps(candidate, indent=2) + "\n", encoding="utf-8"
    )

    materials = {
        "README.md": "Synthetic competition README.\n",
        "design/skills_design.md": "Synthetic Skills design.\n",
        "design/decision_report.md": "Synthetic decision report.\n",
    }
    for relative, contents in materials.items():
        if relative == missing_material:
            continue
        if relative == secret_material:
            contents = 'Synthetic file\napi_key = "syntheticcredentialvalue123"\n'
        target = repo / "submission_materials" / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(contents, encoding="utf-8")

    _git(repo, "init", "-b", "main")
    _git(repo, "config", "user.name", "Synthetic Test")
    _git(repo, "config", "user.email", "synthetic@example.invalid")
    _git(repo, "add", "configs", "skills", "submission_materials")
    _git(repo, "commit", "-m", "synthetic final package fixture")
    _git(repo, "update-ref", "refs/remotes/origin/main", "HEAD")
    return repo


def _build(repo: Path, output: Path, *, archive_layout: str = "solution-dir") -> dict:
    return builder.build(
        repo,
        team="CareerSim Synthetic Team",
        submission_name="synthetic-final",
        output=output,
        archive_layout=archive_layout,
    )


def test_builder_rejects_candidate_that_is_not_final_frozen(tmp_path: Path) -> None:
    repo = _synthetic_repo(tmp_path / "repo", status="STATIC_IMPLEMENTED_NOT_RUNTIME_VALIDATED")
    with pytest.raises(RuntimeError, match="candidate status must be FINAL_FROZEN_FOR_SUBMISSION"):
        _build(repo, tmp_path / "out/solution.zip")


@pytest.mark.parametrize("team", ("enter your team name here", "local-offline-test"))
def test_builder_rejects_placeholder_or_local_team_labels(tmp_path: Path, team: str) -> None:
    repo = _synthetic_repo(tmp_path / "repo")
    with pytest.raises(RuntimeError, match="real competition team name"):
        builder.build(
            repo,
            team=team,
            submission_name="synthetic-final",
            output=tmp_path / "out/solution.zip",
            archive_layout="solution-dir",
        )


def test_builder_requires_exactly_four_canonical_skills(tmp_path: Path) -> None:
    repo = _synthetic_repo(tmp_path / "repo", candidate_skill_names=EXPECTED_SKILLS[:-1])
    with pytest.raises(RuntimeError, match="exactly the expected four Skills"):
        _build(repo, tmp_path / "out/solution.zip")


@pytest.mark.parametrize(
    "missing",
    ("README.md", "design/skills_design.md", "design/decision_report.md"),
)
def test_builder_requires_readme_and_both_design_documents(tmp_path: Path, missing: str) -> None:
    repo = _synthetic_repo(tmp_path / "repo", missing_material=missing)
    with pytest.raises(RuntimeError, match="missing final submission material"):
        _build(repo, tmp_path / "out/solution.zip")


def test_builder_stops_on_secret_like_credential_assignment(tmp_path: Path) -> None:
    repo = _synthetic_repo(tmp_path / "repo", secret_material="README.md")
    with pytest.raises(RuntimeError, match="possible secret detected"):
        _build(repo, tmp_path / "out/solution.zip")


def test_default_cli_build_is_whitelisted_deterministic_and_exact_after_extraction(tmp_path: Path) -> None:
    repo = _synthetic_repo(tmp_path / "repo")
    output_a = tmp_path / "first/solution.zip"
    output_b = tmp_path / "second/solution.zip"
    env = os.environ.copy()
    inherited = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = str(ROOT) + (os.pathsep + inherited if inherited else "")

    command = [
        sys.executable,
        str(BUILDER_PATH),
        "--repo-root",
        str(repo),
        "--team",
        "CareerSim Synthetic Team",
        "--name",
        "synthetic-final",
        "--output",
        str(output_a),
    ]
    subprocess.run(command, cwd=repo, env=env, check=True, capture_output=True, text=True)
    provenance_b = _build(repo, output_b)

    assert hashlib.sha256(output_a.read_bytes()).hexdigest() == hashlib.sha256(output_b.read_bytes()).hexdigest()
    with zipfile.ZipFile(output_a) as archive:
        names = set(archive.namelist())
        assert names == {f"solution/{relative}" for relative in EXPECTED_MEMBERS}
        extracted = {name.removeprefix("solution/"): archive.read(name) for name in names}

    manifest = json.loads(extracted["manifest.json"].decode("utf-8"))
    canonical = json.loads((repo / "configs/runtime_manifest.json").read_text(encoding="utf-8"))
    assert manifest["instruction"] == canonical["instruction"]
    for skill in EXPECTED_SKILLS:
        relative = f"skills/{skill}/SKILL.md"
        assert extracted[relative] == (repo / relative).read_bytes()

    sha_path = output_a.with_suffix(output_a.suffix + ".sha256")
    assert sha_path.read_text(encoding="utf-8") == (
        f"{hashlib.sha256(output_a.read_bytes()).hexdigest()}  {output_a.name}\n"
    )
    provenance_path = output_a.with_name("solution-manifest.json")
    provenance_a = json.loads(provenance_path.read_text(encoding="utf-8"))
    assert provenance_a["status"] == "FINAL_SUBMISSION_PACKAGE_READY"
    assert provenance_a["archive_layout"] == "solution-dir"
    assert provenance_a["zip"]["sha256"] == hashlib.sha256(output_a.read_bytes()).hexdigest()
    assert provenance_b["zip"]["sha256"] == provenance_a["zip"]["sha256"]


def test_contents_only_layout_requires_explicit_builder_argument(tmp_path: Path) -> None:
    repo = _synthetic_repo(tmp_path / "repo")
    output = tmp_path / "contents-only/solution.zip"
    result = _build(repo, output, archive_layout="contents-only")
    with zipfile.ZipFile(output) as archive:
        names = set(archive.namelist())
    assert names == EXPECTED_MEMBERS
    assert not any(name.startswith("solution/") for name in names)
    assert result["archive_layout"] == "contents-only"


def _exact_fixture(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Use real immutable v6 bytes, synthetic committed docs/freeze, no runtime install."""
    repo = _synthetic_repo(tmp_path / "repo")
    freeze = json.loads((ROOT / "docs/project/FINAL_SUBMISSION_IDENTITY.json").read_text(encoding="utf-8"))
    freeze.update(team="CareerSim Synthetic Team", name="synthetic-final")
    path = repo / "docs/project/FINAL_SUBMISSION_IDENTITY.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(freeze), encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "explicit historical freeze")
    _git(repo, "update-ref", "refs/remotes/origin/main", "HEAD")
    original = builder._source_blob
    def read(source_repo: Path, commit: str, rel: str) -> bytes:
        return original(ROOT if commit == builder.EXACT_V6_SOURCE else source_repo, commit, rel)
    monkeypatch.setattr(builder, "_source_blob", read)
    return repo


def test_exact_v6_ignores_later_checkout_and_preserves_git_bytes(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    repo = _exact_fixture(tmp_path, monkeypatch)
    output = tmp_path / "out/final.zip"
    result = builder.build(repo, team="CareerSim Synthetic Team", submission_name="synthetic-final",
                           output=output, archive_layout="solution-dir", exact_v6=True)
    with zipfile.ZipFile(output) as archive:
        assert set(archive.namelist()) == {f"solution/{p}" for p in builder._expected_relpaths(tuple(builder.EXACT_V6_BLOBS))}
        manifest = json.loads(archive.read("solution/manifest.json"))
        source = json.loads(builder._source_blob(repo, builder.EXACT_V6_SOURCE, "configs/runtime_manifest.json"))
        assert {k for k in source if source[k] != manifest[k]} == {"team", "name"}
        for skill, blob in builder.EXACT_V6_BLOBS.items():
            assert _git_blob(archive.read(f"solution/skills/{skill}/SKILL.md")) == blob
    assert result["runtime_source_commit"] == builder.EXACT_V6_SOURCE
    before = output.read_bytes()
    with pytest.raises(RuntimeError, match="do not overwrite/rebuild"):
        builder.build(repo, team="CareerSim Synthetic Team", submission_name="synthetic-final",
                      output=output, archive_layout="solution-dir", exact_v6=True)
    assert output.read_bytes() == before


def test_exact_v6_rejects_uncommitted_freeze_and_wrong_identity(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    repo = _exact_fixture(tmp_path, monkeypatch)
    kwargs = dict(team="Wrong Team", submission_name="synthetic-final", output=tmp_path / "out/final.zip",
                  archive_layout="solution-dir", exact_v6=True)
    with pytest.raises(RuntimeError, match="freeze identity mismatch"):
        builder.build(repo, **kwargs)
    (repo / "docs/project/FINAL_SUBMISSION_IDENTITY.json").write_text("{}", encoding="utf-8")
    with pytest.raises(RuntimeError, match="working tree is not clean"):
        builder.build(repo, **kwargs)


def test_final_builder_requires_main(tmp_path: Path) -> None:
    repo = _synthetic_repo(tmp_path / "repo")
    _git(repo, "checkout", "-b", "codex/unfrozen")
    with pytest.raises(RuntimeError, match="requires main"):
        _build(repo, tmp_path / "out/final.zip")
