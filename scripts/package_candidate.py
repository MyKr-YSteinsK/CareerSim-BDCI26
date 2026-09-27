"""Build the current Candidate's Runner-compatible local submission bundle."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


EXPECTED_SKILLS = (
    "structured-state-board",
    "rolling-planning",
    "delivery-progress",
    "risk-review",
)


def build_submission(repo_root: Path, output_dir: Path) -> None:
    """Copy canonical manifest and Skill bytes into a new submission directory."""
    repo_root = repo_root.resolve()
    manifest_path = repo_root / "configs" / "runtime_manifest.json"
    candidate_path = repo_root / "configs" / "current_candidate.json"
    manifest_bytes = manifest_path.read_bytes()
    manifest = json.loads(manifest_bytes.decode("utf-8"))
    candidate = json.loads(candidate_path.read_text(encoding="utf-8"))

    candidate_id = candidate.get("candidate_id")
    if not candidate_id:
        raise ValueError("Current Candidate identity is missing")
    if manifest.get("name") != candidate_id or manifest.get("mode") != "agent":
        raise ValueError("Canonical manifest identity or mode does not match current Candidate")
    if not str(manifest.get("instruction") or "").strip():
        raise ValueError("Canonical manifest instruction is missing")

    candidate_skill_names = {entry["name"] for entry in candidate.get("skills", [])}
    if candidate_skill_names != set(EXPECTED_SKILLS):
        raise ValueError("Candidate metadata does not identify exactly the current four Skills")

    source_skills_dir = repo_root / "skills"
    source_skill_names = {
        child.name
        for child in source_skills_dir.iterdir()
        if child.is_dir() and (child / "SKILL.md").is_file()
    }
    if source_skill_names != set(EXPECTED_SKILLS):
        raise ValueError("Repository Skill sources do not match the current four Skills")

    skill_bytes = {
        name: (source_skills_dir / name / "SKILL.md").read_bytes()
        for name in EXPECTED_SKILLS
    }
    output_dir = output_dir.resolve()
    if output_dir.exists() and any(output_dir.iterdir()):
        raise FileExistsError(f"Refusing to overwrite non-empty output directory: {output_dir}")
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "manifest.json").write_bytes(manifest_bytes)
    for name, content in skill_bytes.items():
        destination = output_dir / "skills" / name / "SKILL.md"
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(content)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    build_submission(args.repo_root, args.output)
    print(args.output.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
