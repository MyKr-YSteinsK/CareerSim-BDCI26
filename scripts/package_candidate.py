"""Build the current Candidate's Runner-compatible local submission bundle."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


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

    entries = candidate.get("skills", [])
    names = [entry["name"] for entry in entries]
    architecture = candidate.get("architecture", {})
    if (
        not 2 <= len(names) <= 4
        or len(set(names)) != len(names)
        or any(not re.fullmatch(r"[a-z][a-z0-9-]*", name) for name in names)
        or set(architecture.get("active_skills", [])) != set(names)
        or architecture.get("skill_count") != len(names)
        or any(entry.get("path") != f"skills/{entry['name']}/SKILL.md" for entry in entries)
    ):
        raise ValueError("Candidate Skill declarations are inconsistent or unsafe")

    source_skills_dir = repo_root / "skills"
    if not source_skills_dir.resolve().is_relative_to(repo_root):
        raise ValueError("Skill directory escapes repository")
    source_skill_names = {
        child.name
        for child in source_skills_dir.iterdir()
        if child.is_dir() and (child / "SKILL.md").is_file()
    }
    if source_skill_names != set(names):
        raise ValueError("Repository Skill sources do not match Candidate declarations")

    # Preserve normal progressive-disclosure Markdown references, without
    # admitting arbitrary local runtime assets or following links outside sources.
    skill_bytes = {}
    for name in names:
        source = source_skills_dir / name
        if source.is_symlink() or not source.resolve().is_relative_to(source_skills_dir.resolve()):
            raise ValueError("Linked Skill sources are not allowed")
        for path in sorted(source.rglob("*")):
            if path.is_symlink() or not path.resolve().is_relative_to(source.resolve()):
                raise ValueError("Linked or escaping Skill references are not allowed")
            if path.is_file():
                relative = path.relative_to(source)
                if relative != Path("SKILL.md") and not (
                    relative.parts[0] == "references" and path.suffix == ".md"
                ):
                    raise ValueError(f"Unexpected Skill asset: {relative}")
                skill_bytes[Path(name) / relative] = path.read_bytes()
    output_dir = output_dir.resolve()
    if output_dir.exists() and any(output_dir.iterdir()):
        raise FileExistsError(f"Refusing to overwrite non-empty output directory: {output_dir}")
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "manifest.json").write_bytes(manifest_bytes)
    for relative, content in skill_bytes.items():
        destination = output_dir / "skills" / relative
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
