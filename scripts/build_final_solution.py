"""Build the final competition `solution.zip` from one frozen CareerSim Candidate.

This is an offline packaging tool. It performs no provider, service, MCP, DB, or
game operation.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import tempfile
import zipfile
from pathlib import Path, PurePosixPath

from career_sim_runner.skill_contract import (
    list_bundle_skill_ids,
    validate_manifest,
    validate_skill_frontmatter,
    validate_submission_contract,
)

EXPECTED_SKILLS = (
    "structured-state-board",
    "rolling-planning",
    "delivery-progress",
    "risk-review",
)
FINAL_STATUS = "FINAL_FROZEN_FOR_SUBMISSION"
EXACT_V6_SOURCE = "1114a04b75548cf52f030d123564e527060fc061"
EXACT_V6_BLOBS = {
    "risk-review": "a6a09a4894caaca15f4aa5005911bad3b399b464",
    "rolling-planning": "138a2a9ef7626e892b36b0e8e29a934a90709228",
    "structured-state-board": "0afafcfbd2e8d87e5a9cc9944be0cd639c3b61bd",
}
EXACT_V6_MANIFEST_SHA = "bcf459da811f55b8a26a76d2ee6e93da10deb4b720cc732d19a3ce12d8fa2985"
EXACT_V6_INSTRUCTION_SHA = "7131bbd652452c71571f1ab99451f210e6e52601e9d66144d3d665337b4eb33c"
PLACEHOLDERS = ("TODO_FINAL", "FINALIZE_ME", "YOUR_TEAM_NAME")
SECRET_PATTERNS = (
    re.compile(r"(?i)\b(?:api[_-]?key|access[_-]?token|secret|password)\b\s*[:=]\s*[\"']?([A-Za-z0-9_./+\-=]{12,})"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{16,}\b"),
)
FIXED_ZIP_DT = (2026, 1, 1, 0, 0, 0)


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _git(repo: Path, *args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=repo, text=True).strip()


def _git_blob_id(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode()
    return hashlib.sha1(header + data).hexdigest()


def _require_clean_synced_main(repo: Path) -> str:
    if _git(repo, "branch", "--show-current") != "main":
        raise RuntimeError("final build requires main branch")
    if _git(repo, "status", "--porcelain"):
        raise RuntimeError("working tree is not clean")
    head = _git(repo, "rev-parse", "HEAD")
    origin = _git(repo, "rev-parse", "origin/main")
    if head != origin:
        raise RuntimeError(f"HEAD {head} != origin/main {origin}")
    return head


def _scan_text(label: str, data: bytes) -> None:
    text = data.decode("utf-8")
    for marker in PLACEHOLDERS:
        if marker in text:
            raise RuntimeError(f"{label}: unresolved placeholder {marker}")
    for pattern in SECRET_PATTERNS:
        match = pattern.search(text)
        if match:
            raise RuntimeError(f"{label}: possible secret detected by {pattern.pattern!r}")


def _write_zip(
    output: Path,
    solution_root: Path,
    *,
    archive_layout: str,
) -> None:
    members = sorted(p for p in solution_root.rglob("*") if p.is_file())
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for source in members:
            rel = PurePosixPath(source.relative_to(solution_root).as_posix())
            arc = PurePosixPath("solution") / rel if archive_layout == "solution-dir" else rel
            info = zipfile.ZipInfo(str(arc), date_time=FIXED_ZIP_DT)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            zf.writestr(info, source.read_bytes())


def _safe_extract_and_verify(zip_path: Path, temp_root: Path, archive_layout: str) -> Path:
    with zipfile.ZipFile(zip_path) as zf:
        names = zf.namelist()
        if len(names) != len(set(names)):
            raise RuntimeError("ZIP contains duplicate members")
        for name in names:
            p = PurePosixPath(name)
            if p.is_absolute() or ".." in p.parts:
                raise RuntimeError(f"unsafe ZIP member: {name}")
        zf.extractall(temp_root)
    return temp_root / "solution" if archive_layout == "solution-dir" else temp_root


def _expected_relpaths(skills: tuple[str, ...] = EXPECTED_SKILLS) -> set[str]:
    paths = {
        "manifest.json",
        "README.md",
        "design/skills_design.md",
        "design/decision_report.md",
    }
    for skill in skills:
        paths.add(f"skills/{skill}/SKILL.md")
    return paths


def _source_blob(repo: Path, commit: str, path: str) -> bytes:
    return subprocess.check_output(["git", "show", f"{commit}:{path}"], cwd=repo)


def _load_exact_v6(repo: Path, team: str, name: str) -> tuple[dict, bytes]:
    """Explicit user-selected historical source; never infer from later runtime."""
    freeze = json.loads(_source_blob(repo, "HEAD", "docs/project/FINAL_SUBMISSION_IDENTITY.json"))
    expected = {
        "status": FINAL_STATUS,
        "decision": "SELECT_EXACT_V6_FOR_SINGLE_SHOT",
        "candidate_id": "candidate-v6-auditable-control-loop",
        "source_commit": EXACT_V6_SOURCE,
        "team": team,
        "name": name,
        "mode": "agent",
        "archive_layout": "solution-dir",
    }
    if any(freeze.get(k) != v for k, v in expected.items()):
        raise RuntimeError("exact v6 final freeze identity mismatch")
    if freeze.get("validation", {}).get("next_game_authorized") is not False:
        raise RuntimeError("exact v6 freeze must forbid next game")
    candidate = json.loads(_source_blob(repo, EXACT_V6_SOURCE, "configs/current_candidate.json"))
    data = _source_blob(repo, EXACT_V6_SOURCE, "configs/runtime_manifest.json")
    if candidate["candidate_id"] != expected["candidate_id"] or _sha256(data) != EXACT_V6_MANIFEST_SHA:
        raise RuntimeError("exact v6 historical Candidate/manifest mismatch")
    if _sha256(json.loads(data)["instruction"].encode("utf-8")) != EXACT_V6_INSTRUCTION_SHA:
        raise RuntimeError("exact v6 historical instruction mismatch")
    if {e["name"]: e["git_blob"] for e in candidate["skills"]} != EXACT_V6_BLOBS:
        raise RuntimeError("exact v6 historical Skill identity mismatch")
    if freeze["skills"] != candidate["skills"] or freeze["runtime_manifest"] != candidate["runtime_manifest"]:
        raise RuntimeError("final freeze differs from verified historical source")
    candidate["status"] = FINAL_STATUS  # Packaging provenance only; no Candidate file rewritten.
    return candidate, data


def build(
    repo: Path,
    *,
    team: str,
    submission_name: str,
    output: Path,
    archive_layout: str,
    exact_v6: bool = False,
) -> dict:
    repo = repo.resolve()
    if not team.strip():
        raise RuntimeError("team name is required")
    lowered = team.strip().lower()
    if lowered in {"enter your team name here", "your-team-name"} or lowered.startswith("local-"):
        raise RuntimeError("team must be the real competition team name, not a local/placeholder label")
    if not submission_name.strip():
        raise RuntimeError("submission name is required")

    commit = _require_clean_synced_main(repo)
    if exact_v6:
        if archive_layout != "solution-dir":
            raise RuntimeError("exact v6 requires solution/ ZIP root")
        candidate, canonical_manifest_bytes = _load_exact_v6(repo, team, submission_name)
        runtime_manifest = json.loads(canonical_manifest_bytes)
        expected_skills = tuple(sorted(EXACT_V6_BLOBS))
    else:
        candidate = json.loads((repo / "configs/current_candidate.json").read_text(encoding="utf-8"))
        canonical_manifest_bytes = (repo / "configs/runtime_manifest.json").read_bytes()
        runtime_manifest = json.loads(canonical_manifest_bytes)
        expected_skills = EXPECTED_SKILLS

    if candidate.get("status") != FINAL_STATUS:
        raise RuntimeError(f"candidate status must be {FINAL_STATUS}")
    if candidate.get("validation", {}).get("next_game_authorized") is not False:
        raise RuntimeError("final Candidate must have next_game_authorized=false")
    if runtime_manifest.get("mode") != "agent":
        raise RuntimeError("final runtime manifest mode must be agent")
    if runtime_manifest.get("name") != candidate.get("candidate_id"):
        raise RuntimeError("runtime manifest name does not match final Candidate")

    if _sha256(canonical_manifest_bytes) != candidate["runtime_manifest"]["sha256"]:
        raise RuntimeError("runtime manifest SHA-256 does not match current_candidate.json")
    if _sha256(str(runtime_manifest["instruction"]).encode("utf-8")) != candidate["runtime_manifest"]["instruction_sha256"]:
        raise RuntimeError("runtime instruction SHA-256 does not match current_candidate.json")

    canonical_skills: dict[str, bytes] = {}
    entries = {e["name"]: e for e in candidate.get("skills", [])}
    if set(entries) != set(expected_skills):
        raise RuntimeError("final Candidate does not identify exactly the expected four Skills" if not exact_v6 else "exact v6 must identify three Skills")
    for skill in expected_skills:
        source = repo / "skills" / skill / "SKILL.md"
        data = _source_blob(repo, EXACT_V6_SOURCE, f"skills/{skill}/SKILL.md") if exact_v6 else source.read_bytes()
        if _git_blob_id(data) != entries[skill]["git_blob"]:
            raise RuntimeError(f"{skill}: canonical Git blob does not match current_candidate.json")
        canonical_skills[skill] = data

    materials = repo / "submission_materials"
    doc_sources = {
        "README.md": materials / "README.md",
        "design/skills_design.md": materials / "design/skills_design.md",
        "design/decision_report.md": materials / "design/decision_report.md",
    }
    doc_bytes: dict[str, bytes] = {}
    for rel, source in doc_sources.items():
        if not source.is_file():
            raise RuntimeError(f"missing final submission material: {source}")
        data = _source_blob(repo, commit, f"submission_materials/{rel}") if exact_v6 else source.read_bytes()
        _scan_text(rel, data)
        doc_bytes[rel] = data

    final_manifest = dict(runtime_manifest)
    final_manifest["team"] = team.strip()
    final_manifest["name"] = submission_name.strip()
    manifest_bytes = (json.dumps(final_manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    _scan_text("manifest.json", manifest_bytes)

    output = output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists():
        if exact_v6:
            raise RuntimeError("signed exact v6 ZIP already exists; do not overwrite/rebuild")
        output.unlink()

    with tempfile.TemporaryDirectory(prefix="career-sim-final-", dir=output.parent if exact_v6 else None) as td:
        temp = Path(td)
        solution = temp / "solution"
        solution.mkdir()

        (solution / "manifest.json").write_bytes(manifest_bytes)
        for rel, source in doc_sources.items():
            dst = solution / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_bytes(doc_bytes[rel])
        for skill, data in canonical_skills.items():
            dst = solution / "skills" / skill / "SKILL.md"
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_bytes(data)
            _scan_text(f"skills/{skill}/SKILL.md", data)

        actual = {p.relative_to(solution).as_posix() for p in solution.rglob("*") if p.is_file()}
        expected = _expected_relpaths(expected_skills)
        if actual != expected:
            raise RuntimeError(f"unexpected final file set: actual={sorted(actual)} expected={sorted(expected)}")

        details = validate_submission_contract(solution)
        manifest_errors = validate_manifest(final_manifest)
        if manifest_errors:
            raise RuntimeError("; ".join(manifest_errors))
        if tuple(details["skill_ids"]) != tuple(sorted(expected_skills)):
            raise RuntimeError(f"unexpected validated Skill ids: {details['skill_ids']}")
        for skill in expected_skills:
            errors = validate_skill_frontmatter(solution / "skills" / skill)
            if errors:
                raise RuntimeError("; ".join(errors))

        _write_zip(output, solution, archive_layout=archive_layout)

        extract_root = temp / "extract"
        extracted_solution = _safe_extract_and_verify(output, extract_root, archive_layout)
        extracted_actual = {
            p.relative_to(extracted_solution).as_posix()
            for p in extracted_solution.rglob("*")
            if p.is_file()
        }
        if extracted_actual != expected:
            raise RuntimeError("extracted ZIP file set differs from expected official layout")
        validate_submission_contract(extracted_solution)

        # Exact post-extraction identity.
        extracted_manifest = json.loads((extracted_solution / "manifest.json").read_text(encoding="utf-8"))
        if extracted_manifest["instruction"] != runtime_manifest["instruction"]:
            raise RuntimeError("extracted manifest instruction differs from canonical runtime instruction")
        for skill, canonical in canonical_skills.items():
            if (extracted_solution / "skills" / skill / "SKILL.md").read_bytes() != canonical:
                raise RuntimeError(f"{skill}: extracted Skill differs from canonical bytes")
        for rel, source in doc_sources.items():
            if (extracted_solution / rel).read_bytes() != doc_bytes[rel]:
                raise RuntimeError(f"{rel}: extracted material differs from canonical submission_materials")

        member_hashes = {
            rel: _sha256((extracted_solution / rel).read_bytes())
            for rel in sorted(expected)
        }

    zip_sha = _sha256(output.read_bytes())
    sha_path = output.with_suffix(output.suffix + ".sha256")
    sha_path.write_text(f"{zip_sha}  {output.name}\n", encoding="utf-8")

    provenance = {
        "status": "FINAL_SUBMISSION_PACKAGE_READY",
        "git_commit": commit,
        "runtime_source_commit": EXACT_V6_SOURCE if exact_v6 else commit,
        "candidate_id": candidate["candidate_id"],
        "candidate_status": candidate["status"],
        "team": team.strip(),
        "submission_name": submission_name.strip(),
        "archive_layout": archive_layout,
        "zip": {
            "path": str(output),
            "sha256": zip_sha,
            "bytes": output.stat().st_size,
        },
        "runtime_manifest_sha256": candidate["runtime_manifest"]["sha256"],
        "runtime_instruction_sha256": candidate["runtime_manifest"]["instruction_sha256"],
        "final_manifest_sha256": _sha256(manifest_bytes),
        "members": member_hashes,
    }
    provenance_path = output.with_name("solution-manifest.json")
    provenance_path.write_text(json.dumps(provenance, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return provenance


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--team", required=True)
    parser.add_argument("--name", required=True, dest="submission_name")
    parser.add_argument("--output", type=Path, default=Path("dist/final/solution.zip"))
    parser.add_argument("--exact-v6", action="store_true", help="Use the explicitly frozen S10-23R-v2 Git source; no runtime changes.")
    parser.add_argument(
        "--archive-layout",
        choices=("solution-dir", "contents-only"),
        default="solution-dir",
        help="Use contents-only only when final official upload instructions explicitly require it.",
    )
    args = parser.parse_args()
    result = build(
        args.repo_root,
        team=args.team,
        submission_name=args.submission_name,
        output=args.output,
        archive_layout=args.archive_layout,
        exact_v6=args.exact_v6,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
