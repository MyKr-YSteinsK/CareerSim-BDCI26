"""Pure repository/static checks for the S06-01 candidate; never invokes runtime."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
BASE = "0a2ccaa03c3865bc88e533108bb52ccc7c5f7ff2"
ARTIFACT = "experiments/S06-01-adaptive-controller-static"
SKILLS = (
    "career-action-trace",
    "risk-review",
    "structured-state-board",
    "rolling-planning",
)
ALLOWED = {
    "docs/project/ARCHITECTURE_DECISIONS.md",
    "docs/project/CURRENT_STATE.md",
    *(f"skills/{skill}/SKILL.md" for skill in SKILLS if skill != "career-action-trace"),
    f"{ARTIFACT}/RESULT.md",
    f"{ARTIFACT}/benchmark_observation_matrix.md",
    f"{ARTIFACT}/candidate_manifest.json",
    f"{ARTIFACT}/runtime_manifest.json",
    f"{ARTIFACT}/static_regression_matrix.md",
    f"{ARTIFACT}/verify_static_contract.py",
}


def git(*args: str, text: bool = True) -> str | bytes:
    result = subprocess.run(
        ["git", *args],
        cwd=REPO,
        check=True,
        capture_output=True,
        text=text,
    )
    return result.stdout.strip() if text else result.stdout


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(REPO))
    from career_sim_runner.skill_contract import validate_manifest, validate_skill_frontmatter

    require(git("rev-parse", "origin/main") == BASE, "origin/main differs from the frozen S06-01 base")
    require(git("merge-base", "--is-ancestor", BASE, "HEAD") == "", "base is not an ancestor")

    changed = set(git("diff", "--name-only", BASE, "HEAD").splitlines())
    dirty = set()
    for line in git("status", "--porcelain").splitlines():
        path = line[3:]
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        dirty.add(path)
    require(changed <= ALLOWED, f"out-of-scope committed paths: {sorted(changed - ALLOWED)}")
    require(dirty <= ALLOWED, f"out-of-scope working-tree paths: {sorted(dirty - ALLOWED)}")
    require("skills/career-action-trace/SKILL.md" not in changed, "Trace changed in this branch")

    skill_dirs = sorted(
        path.name
        for path in (REPO / "skills").iterdir()
        if path.is_dir() and (path / "SKILL.md").is_file()
    )
    require(skill_dirs == sorted(SKILLS), f"unexpected project Skill set: {skill_dirs}")

    candidate_path = REPO / ARTIFACT / "candidate_manifest.json"
    runtime_path = REPO / ARTIFACT / "runtime_manifest.json"
    candidate = json.loads(candidate_path.read_text(encoding="utf-8"))
    runtime_bytes = runtime_path.read_bytes()
    runtime = json.loads(runtime_bytes)
    require(candidate["candidate_id"] == "candidate-v3-adaptive-controller-static", "candidate id mismatch")
    require(candidate["base_main_sha"] == BASE, "candidate base mismatch")
    require(candidate["parent_candidate_id"] == "candidate-v2-final-offline", "parent candidate mismatch")
    require(
        git("merge-base", "--is-ancestor", candidate["candidate_implementation_commit"], "HEAD") == "",
        "candidate implementation commit is not in current ancestry",
    )
    require(candidate["target"] == "STABLE_QUANTITATIVE_80_PLUS" and candidate["target_is_proven"] is False, "target boundary mismatch")
    require(candidate["final_skills"] == list(SKILLS), "manifest Skill set mismatch")
    require(runtime["team"].strip() and runtime["name"].strip(), "manifest team/name is empty")
    require(runtime["mode"] == "agent", "manifest mode must remain single-agent")
    require(runtime["instruction"].strip(), "runtime instruction is empty")
    require(not validate_manifest(runtime), "Runner manifest contract validation failed")
    require(runtime_path.relative_to(REPO).as_posix() == candidate["runtime_manifest"]["canonical_path"], "runtime manifest path mismatch")
    require(hashlib.sha256(runtime_bytes).hexdigest() == candidate["runtime_manifest"]["sha256"], "runtime manifest SHA-256 mismatch")
    require(
        hashlib.sha256(runtime["instruction"].encode("utf-8")).hexdigest()
        == candidate["runtime_manifest"]["instruction_sha256"],
        "runtime instruction SHA-256 mismatch",
    )

    for skill in SKILLS:
        skill_dir = REPO / "skills" / skill
        require(not validate_skill_frontmatter(skill_dir), f"frontmatter invalid: {skill}")
        live_blob = git("hash-object", str(skill_dir / "SKILL.md"))
        require(live_blob == candidate["skill_blobs"][skill], f"Skill blob mismatch: {skill}")
        base_blob = git("rev-parse", f"{BASE}:skills/{skill}/SKILL.md")
        require(base_blob == candidate["parent_skill_blobs"][skill], f"parent Skill blob mismatch: {skill}")
    require(
        candidate["skill_blobs"]["career-action-trace"]
        == "5a1e3ceca8ffc2132303e43bc9f1c1dd630847a8",
        "frozen Trace blob mismatch",
    )

    context = candidate["context"]
    byte_total = 0
    line_total = 0
    for skill in SKILLS:
        object_id = git("hash-object", str(REPO / "skills" / skill / "SKILL.md"))
        content = git("cat-file", "blob", object_id, text=False)
        byte_total += len(content)
        line_total += content.count(b"\n")
    require(byte_total == context["final_total_blob_bytes"], "final Skill blob byte total mismatch")
    require(line_total == context["final_total_lines"], "final Skill line total mismatch")
    parent_bytes = sum(
        len(git("show", f"{BASE}:skills/{skill}/SKILL.md", text=False)) for skill in SKILLS
    )
    parent_lines = sum(
        git("show", f"{BASE}:skills/{skill}/SKILL.md", text=False).count(b"\n") for skill in SKILLS
    )
    require(parent_bytes == context["parent_total_blob_bytes"], "parent Skill blob byte total mismatch")
    require(parent_lines == context["parent_total_lines"], "parent Skill line total mismatch")
    delta = byte_total - parent_bytes
    require(delta == context["absolute_delta_bytes"], "context byte delta mismatch")
    require(round(delta * 100 / parent_bytes, 2) == context["percentage_delta"], "context percentage mismatch")

    instruction = runtime["instruction"].lower()
    for cue in (
        "first energy decision",
        "rolling-planning/skill.md",
        "fresh public observe",
        "primary gap",
        "advertised menu effects",
        "adjacent comparable checkpoints",
        "one no-progress checkpoint",
        "risk budget",
        "48-month horizon",
        "evaluator weights",
        "hidden thresholds",
        "two strongest legal candidates",
        "risk-review=reconsider",
        "sole action submitter",
    ):
        require(cue in instruction, f"runtime instruction missing cue: {cue}")

    planning_text = (REPO / "skills/rolling-planning/SKILL.md").read_text(encoding="utf-8")
    board_text = (REPO / "skills/structured-state-board/SKILL.md").read_text(encoding="utf-8")
    risk_text = (REPO / "skills/risk-review/SKILL.md").read_text(encoding="utf-8")
    for cue in (
        "marginal public benefit",
        "saturation of one component neither discredits nor proves",
        "Severe warning/consequence",
        "two adjacent comparable checkpoints",
        "One miss never forces a switch",
    ):
        require(cue.lower() in planning_text.lower(), f"Planning mechanism missing: {cue}")
    require("at most two `recent_effects`" in board_text, "Board recent-effects bound missing")
    require("Soft Cost alone is opportunity cost" in risk_text, "Risk soft-cost boundary missing")
    require("clearly identifies a relevant material risk" in risk_text, "Risk material-risk gate missing")

    changed_text = "\n".join(
        (REPO / path).read_text(encoding="utf-8")
        for path in sorted(changed)
        if (REPO / path).is_file()
    )
    require(
        re.search(r"\b[A-Z0-9_]{2,}=[A-Za-z0-9+/=_-]{32,}", changed_text) is None,
        "credential-like assignment found",
    )
    require(not any(Path(path).name == ".env" for path in changed), ".env is in changed paths")
    require(all(candidate[key] is False for key in ("gameplay_validated", "provider_validated", "stable_80_plus_proven", "next_game_authorized")), "candidate validation/authorization flags must be false")

    for markdown_path in (
        REPO / ARTIFACT / "RESULT.md",
        REPO / ARTIFACT / "benchmark_observation_matrix.md",
    ):
        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", markdown_path.read_text(encoding="utf-8")):
            if target.startswith(("https://", "http://", "#", "mailto:")):
                continue
            local_target = target.split("#", 1)[0]
            require((markdown_path.parent / local_target).exists(), f"broken local link in {markdown_path.name}: {target}")

    print("PASS: base ancestry, scope, four Skills, frontmatter, manifest contract, hashes, context accounting, controller cues, links, and hygiene")


if __name__ == "__main__":
    main()
