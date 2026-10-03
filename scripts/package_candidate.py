"""Build the current Candidate's Runner-compatible local submission bundle."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

import yaml


def canonical_skill_names(candidate: dict) -> tuple[str, ...]:
    """Resolve an explicit active set; never discover extra submission Skills."""
    architecture = candidate.get("architecture", {})
    active = architecture.get("active_skills")
    entries = candidate.get("skills")
    if not isinstance(active, list) or not active or not isinstance(entries, list):
        raise ValueError("Candidate must define an explicit nonempty active Skill set")
    if any(not isinstance(name, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) for name in active):
        raise ValueError("Active Skill names must be safe canonical directory names")
    if len(active) != len(set(active)) or architecture.get("skill_count") != len(active):
        raise ValueError("Active Skill count or names are inconsistent")
    names = [entry.get("name") for entry in entries if isinstance(entry, dict)]
    if (
        len(names) != len(entries)
        or any(not isinstance(name, str) for name in names)
        or len(names) != len(active)
        or set(names) != set(active)
    ):
        raise ValueError("Candidate Skill entries do not match the active set exactly")
    for entry in entries:
        if entry.get("path") != f"skills/{entry['name']}/SKILL.md":
            raise ValueError("Candidate Skill paths must match their canonical names")
    return tuple(sorted(active))


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

    expected_skills = canonical_skill_names(candidate)
    identity = candidate.get("runtime_manifest", {})
    if identity.get("path") != "configs/runtime_manifest.json":
        raise ValueError("Candidate runtime manifest path is not canonical")
    if identity.get("sha256") != hashlib.sha256(manifest_bytes).hexdigest():
        raise ValueError("Canonical manifest bytes do not match Candidate identity")
    if identity.get("instruction_sha256") != hashlib.sha256(manifest["instruction"].encode("utf-8")).hexdigest():
        raise ValueError("Canonical instruction does not match Candidate identity")

    source_skills_dir = repo_root / "skills"
    source_skill_names = {
        child.name
        for child in source_skills_dir.iterdir()
        if child.is_dir() and (child / "SKILL.md").is_file()
    }
    if source_skill_names != set(expected_skills):
        raise ValueError("Repository Skill sources do not match the explicit active set")

    for name in expected_skills:
        source = source_skills_dir / name
        if source.is_symlink() or (source / "SKILL.md").is_symlink():
            raise ValueError("Canonical Skill sources must not be symbolic links")
    skill_bytes = {
        name: (source_skills_dir / name / "SKILL.md").read_bytes()
        for name in expected_skills
    }
    entries = {entry["name"]: entry for entry in candidate["skills"]}
    for name, content in skill_bytes.items():
        parts = content.decode("utf-8").split("---", 2)
        frontmatter = yaml.safe_load(parts[1]) if len(parts) == 3 and not parts[0].strip() else None
        if not isinstance(frontmatter, dict) or frontmatter.get("name") != name or not frontmatter.get("description"):
            raise ValueError(f"{name}: invalid canonical YAML frontmatter")
        if "sha256" in entries[name] and entries[name]["sha256"] != hashlib.sha256(content).hexdigest():
            raise ValueError(f"{name}: Skill bytes do not match Candidate identity")
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
