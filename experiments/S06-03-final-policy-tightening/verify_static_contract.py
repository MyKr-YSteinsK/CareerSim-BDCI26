"""Offline-only verifier for the S06-03 v3b candidate and exact submission."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path, PurePosixPath

import yaml


ROOT = Path(__file__).resolve().parents[2]
EXPERIMENT = "experiments/S06-03-final-policy-tightening"
CANDIDATE_PATH = f"{EXPERIMENT}/candidate_manifest.json"
RUNTIME_PATH = f"{EXPERIMENT}/runtime_manifest.json"
SKILLS = (
    "career-action-trace",
    "risk-review",
    "structured-state-board",
    "rolling-planning",
)
EXPECTED_PARENT_SKILLS = {
    "career-action-trace": "5a1e3ceca8ffc2132303e43bc9f1c1dd630847a8",
    "risk-review": "6680e45d1a45a9aed5e6e3dc5dd5458b49ad7852",
    "structured-state-board": "d7d330e01dc0a0d2472878577c9b4db833fbffb5",
    "rolling-planning": "4d21dafabce2273f6e09e4b137bf72ac37c82132",
}
TRACE_BLOB = "5a1e3ceca8ffc2132303e43bc9f1c1dd630847a8"
BASE_MAIN = "043ecd1db24249d3557c2cfbc6ec8febb4f3866b"
ALLOWED_CHANGED = {
    "skills/rolling-planning/SKILL.md",
    "skills/structured-state-board/SKILL.md",
    "docs/project/CURRENT_STATE.md",
    "docs/project/ARCHITECTURE_DECISIONS.md",
    f"{EXPERIMENT}/runtime_manifest.json",
    f"{EXPERIMENT}/candidate_manifest.json",
    f"{EXPERIMENT}/RESULT.md",
    f"{EXPERIMENT}/static_regression_matrix.md",
    f"{EXPERIMENT}/benchmark_observation_matrix.md",
    f"{EXPERIMENT}/verify_static_contract.py",
}


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def blob(revision: str, path: str) -> bytes:
    return subprocess.check_output(["git", "show", f"{revision}:{path}"], cwd=ROOT)


def blob_id(revision: str, path: str) -> str:
    return git("rev-parse", f"{revision}:{path}")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def skill_metrics(revision: str) -> tuple[int, int]:
    contents = [blob(revision, f"skills/{name}/SKILL.md") for name in SKILLS]
    return sum(map(len, contents)), sum(len(item.splitlines()) for item in contents)


def frontmatter(text: str) -> dict[str, object]:
    if not text.startswith("---\n"):
        raise ValueError("Skill file does not begin with YAML frontmatter")
    _, raw, _ = text.split("---", 2)
    parsed = yaml.safe_load(raw)
    if not isinstance(parsed, dict):
        raise ValueError("Skill frontmatter is not a YAML mapping")
    return parsed


def require(condition: bool, label: str, detail: str = "") -> None:
    print(f"{'PASS' if condition else 'FAIL'} | {label}" + (f" | {detail}" if detail else ""))
    if not condition:
        raise AssertionError(label)


def verify(materialize: bool) -> None:
    candidate = json.loads((ROOT / CANDIDATE_PATH).read_text(encoding="utf-8"))
    runtime_checkout = json.loads((ROOT / RUNTIME_PATH).read_text(encoding="utf-8"))
    base = candidate["base_main_sha"]
    implementation = candidate["candidate_implementation_commit"]
    runtime_raw = blob(implementation, RUNTIME_PATH)
    runtime = json.loads(runtime_raw.decode("utf-8"))
    require(runtime_checkout == runtime, "runtime JSON matches canonical Git artifact")
    instruction = runtime.get("instruction", "")
    instruction_bytes = instruction.encode("utf-8")
    head = git("rev-parse", "HEAD")

    require(candidate["candidate_id"] == "candidate-v3b-final-policy", "candidate identity")
    require(candidate["parent_candidate_id"] == "candidate-v3-adaptive-controller-static", "parent candidate")
    require(base == BASE_MAIN, "accepted S06-02 base", base)
    require(candidate["accepted_s06_02_reconciliation_commit"] == BASE_MAIN, "S06-02 acceptance ancestry")
    require(git("merge-base", "--is-ancestor", base, head) == "", "base is ancestor of final HEAD")
    require(git("merge-base", "--is-ancestor", implementation, head) == "", "implementation commit is ancestor of final HEAD")
    require(git("branch", "--show-current") == "codex/s06-03-final-policy-tightening", "task branch")

    dirs = {p.name for p in (ROOT / "skills").iterdir() if p.is_dir() and (p / "SKILL.md").is_file()}
    require(dirs == set(SKILLS), "exactly four project-owned Skills")
    names: list[str] = []
    for name in SKILLS:
        text = (ROOT / "skills" / name / "SKILL.md").read_text(encoding="utf-8")
        fields = frontmatter(text)
        require(fields.get("name") == name and bool(fields.get("description")), f"frontmatter: {name}")
        names.append(str(fields["name"]))
    require(len(names) == len(set(names)), "unique Skill names")

    require(runtime.get("team", "").strip() not in {"", "enter your team name here"}, "submission team field")
    require(runtime.get("name") == "candidate-v3b-final-policy", "submission name field")
    require(runtime.get("mode") == "agent", "submission mode field")
    require(bool(instruction.strip()), "non-empty runtime instruction")
    require(candidate["runtime_manifest"]["canonical_path"] == RUNTIME_PATH, "canonical runtime manifest path")
    require(candidate["runtime_manifest"]["sha256"] == sha256(runtime_raw), "runtime manifest SHA-256")
    require(candidate["runtime_manifest"]["instruction_sha256"] == sha256(instruction_bytes), "instruction SHA-256")
    require(candidate["runtime_manifest"]["instruction_bytes"] == len(instruction_bytes), "instruction byte count")

    require(candidate["parent_v3_skill_blobs"] == EXPECTED_PARENT_SKILLS, "recorded v3 parent Skill identities")
    for name in SKILLS:
        path = f"skills/{name}/SKILL.md"
        require(blob_id(base, path) == EXPECTED_PARENT_SKILLS[name], f"accepted v3 parent blob: {name}")
        identity = blob_id(implementation, path)
        require(candidate["skill_blobs"][name] == identity, f"candidate Skill blob: {name}", identity)
    require(candidate["skill_blobs"]["career-action-trace"] == TRACE_BLOB, "Trace frozen identity")
    require(blob_id(implementation, "skills/career-action-trace/SKILL.md") == TRACE_BLOB, "Trace Git blob unchanged")
    require(blob_id(implementation, "skills/risk-review/SKILL.md") == EXPECTED_PARENT_SKILLS["risk-review"], "Risk Skill unchanged")

    planning = (ROOT / "skills/rolling-planning/SKILL.md").read_text(encoding="utf-8").lower()
    board = (ROOT / "skills/structured-state-board/SKILL.md").read_text(encoding="utf-8").lower()
    cue = instruction.lower()
    required_planning = (
        "new quarter alone does not require a full skill reread",
        "exactly one `primary gap`",
        "advancing` requires observable improvement in the primary gap itself",
        "supporting signals only and cannot alone establish `advancing`",
        "two adjacent comparable checkpoints",
        "one miss never forces a switch",
        "risk budget = available",
        "clearly stronger public-evidence-based upside",
        "most mature, safest, or least-offensive",
        "public current month and 48-month horizon",
        "do not assign fixed weights or a numeric score",
        "at most the two strongest legal candidates once",
    )
    for phrase in required_planning:
        require(phrase in planning, "Planning semantics", phrase)
    required_board = (
        "at most the five most recent public log entries",
        "confirm the careersim `game_session_id`",
        "fresh public `observe`",
        "up to two recent strategic action/effect pairs",
        "keep at most two `recent_effects`",
        "otherwise write `unknown` or omit it",
        "not to label progress or recommend an action",
    )
    for phrase in required_board:
        require(phrase in board, "Board recovery semantics", phrase)
    required_cue = (
        "at each quarter's first energy",
        "a new quarter alone does not require a full reread",
        "material-risk gate, gap contribution, useful secondary public benefits, soft cost/opportunity cost, then uncertainty",
        "risk budget is tight/available/unknown",
        "prefer that higher-upside path",
        "only gap movement or direct gap-related public progression can be advancing",
        "two adjacent comparable no-progress checkpoints",
        "at most two strongest legal options once",
        "single agent remains the sole action submitter",
    )
    for phrase in required_cue:
        require(phrase in cue, "Always-visible controller cue", phrase)

    policies = planning + "\n" + board + "\n" + cue
    forbidden_patterns = (
        r"(?i)\b(?:health|dignity)\s*(?:>=|>|at least)\s*\d+",
        r"(?i)\b(?:risk score|aggression score|fixed loss budget|score-to-80 runtime rule)\b",
        r"(?i)event[- ]title\s*→\s*[^\n]+",
    )
    for pattern in forbidden_patterns:
        require(re.search(pattern, policies) is None, "no hidden numeric policy", pattern)
    require("evaluator weights" in cue and "hidden thresholds" in cue, "runtime cue explicitly excludes evaluator/hidden thresholds")
    require("game_session_id" in board and "new game session always starts a clean board" in board, "session isolation")
    require(candidate["gameplay_validated"] is False, "gameplay remains unvalidated")
    require(candidate["provider_validated"] is False, "provider remains unvalidated")
    require(candidate["stable_80_plus_proven"] is False, "stable 80+ remains unproven")
    require(candidate["next_game_authorized"] is False, "next game remains unauthorized")

    base_metrics = skill_metrics(base)
    final_metrics = skill_metrics(implementation)
    context = candidate["context"]
    require(base_metrics == (19235, 283), "v3 parent context identity", f"{base_metrics[0]} bytes / {base_metrics[1]} lines")
    require(tuple(context["parent_v3_total_blob_bytes_lines"]) == base_metrics, "recorded v3 context")
    require(tuple(context["final_v3b_total_blob_bytes_lines"]) == final_metrics, "recorded v3b context")
    delta_bytes = final_metrics[0] - base_metrics[0]
    delta_lines = final_metrics[1] - base_metrics[1]
    percentage = round(delta_bytes * 100 / base_metrics[0], 2)
    require(context["absolute_delta_bytes"] == delta_bytes, "context byte delta", str(delta_bytes))
    require(context["absolute_delta_lines"] == delta_lines, "context line delta", str(delta_lines))
    require(context["percentage_delta"] == percentage, "context percentage delta", str(percentage))

    changed = set(git("diff", "--name-only", base, head).splitlines())
    require(changed <= ALLOWED_CHANGED, "changed-file scope", ", ".join(sorted(changed - ALLOWED_CHANGED)))
    no_frozen_changes = subprocess.run(
        ["git", "diff", "--quiet", base, head, "--", "career_sim_runner", "pyproject.toml", "uv.lock", "docs/project/OFFICIAL_SOURCE_LOCK.md"],
        cwd=ROOT,
        check=False,
    ).returncode == 0
    require(no_frozen_changes, "Runner/dependency/Source Lock unchanged")
    require(f"experiments/S06-01-adaptive-controller-static/runtime_manifest.json" not in changed,
            "historical v3 runtime manifest unchanged")
    tracked = git("ls-tree", "-r", "--name-only", head).splitlines()
    env_paths = [p for p in tracked if PurePosixPath(p).name == ".env"]
    require(not env_paths, "no tracked .env", ", ".join(env_paths))
    changed_contents = [blob(head, path) for path in sorted(changed) if path.lower().endswith((".md", ".json", ".py"))]
    secret_like = re.compile(rb"(?i)(?:sk-[A-Za-z0-9_-]{24,}|api[_-]?key\s*[:=]\s*['\"][^'\"]{24,})")
    require(not any(secret_like.search(data) for data in changed_contents), "no secret-like value in changed artifacts")

    matrix = (ROOT / f"{EXPERIMENT}/static_regression_matrix.md").read_text(encoding="utf-8")
    statuses = re.findall(r"^\|\s*(?:0?[1-9]|[1-5][0-9])\s*\|.*\|\s*PASS\s*\|\s*$", matrix, re.MULTILINE)
    require(len(statuses) == 56, "56 static regression rows marked PASS", str(len(statuses)))
    links = (
        (f"{EXPERIMENT}/RESULT.md", "candidate_manifest.json"),
        (f"{EXPERIMENT}/RESULT.md", "static_regression_matrix.md"),
        (f"{EXPERIMENT}/RESULT.md", "benchmark_observation_matrix.md"),
        (f"{EXPERIMENT}/RESULT.md", "verify_static_contract.py"),
        (f"{EXPERIMENT}/static_regression_matrix.md", "verify_static_contract.py"),
        (f"{EXPERIMENT}/benchmark_observation_matrix.md", "../S06-01-adaptive-controller-static/benchmark_observation_matrix.md"),
    )
    for source, target in links:
        require((ROOT / source).parent.joinpath(target).is_file(), "local Markdown link", f"{source} → {target}")

    if materialize:
        workspace = ROOT.parents[2]
        destination = workspace / ".local/runtime/s06-candidate-v3b-final-policy/submission"
        if destination.exists():
            raise FileExistsError(f"Refusing to overwrite existing submission directory: {destination}")
        destination.mkdir(parents=True, exist_ok=False)
        files = [(RUNTIME_PATH, "manifest.json")]
        files.extend((f"skills/{name}/SKILL.md", f"skills/{name}/SKILL.md") for name in SKILLS)
        for source, target in files:
            target_path = destination / target
            target_path.parent.mkdir(parents=True, exist_ok=True)
            target_path.write_bytes(blob(implementation, source))
        expected = {"manifest.json", *(f"skills/{name}/SKILL.md" for name in SKILLS)}
        actual = {p.relative_to(destination).as_posix() for p in destination.rglob("*") if p.is_file()}
        require(actual == expected, "materialized submission layout")
        for source, target in files:
            require((destination / target).read_bytes() == blob(implementation, source), f"materialized bytes: {target}")
        print(f"MATERIALIZED | {destination}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--materialize", action="store_true", help="write an exact local static submission copy; never install or run it")
    args = parser.parse_args()
    verify(args.materialize)


if __name__ == "__main__":
    main()
