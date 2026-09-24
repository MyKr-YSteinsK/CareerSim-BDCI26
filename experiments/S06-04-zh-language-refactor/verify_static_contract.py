"""Offline-only identity, language, semantic-matrix, and static-submission checks for S06-04."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path, PurePosixPath

import yaml


ROOT = Path(__file__).resolve().parents[2]
WORKSPACE = ROOT.parents[2]
EXPERIMENT = "experiments/S06-04-zh-language-refactor"
RUNTIME_PATH = f"{EXPERIMENT}/runtime_manifest.json"
CANDIDATE_PATH = f"{EXPERIMENT}/candidate_manifest.json"
SEMANTIC_MATRIX_PATH = f"{EXPERIMENT}/semantic_equivalence_matrix.md"
REGRESSION_MATRIX_PATH = f"{EXPERIMENT}/static_regression_matrix.md"
BASE_MAIN = "201fe14daf89919f984aa5a9e3ffbc2818f5ab3f"
S06_03_HEAD_BEFORE_ACCEPTANCE = "bf6f38954c979210abd2d27b2c602e55f1777be3"
S06_03_ACCEPTANCE_COMMIT = "201fe14daf89919f984aa5a9e3ffbc2818f5ab3f"
BRANCH = "codex/s06-04-zh-language-refactor"
SKILLS = (
    "career-action-trace",
    "risk-review",
    "structured-state-board",
    "rolling-planning",
)
PARENT_SKILL_BLOBS = {
    "career-action-trace": "5a1e3ceca8ffc2132303e43bc9f1c1dd630847a8",
    "risk-review": "6680e45d1a45a9aed5e6e3dc5dd5458b49ad7852",
    "structured-state-board": "d356b71e27ab208ed28022972b96e06d8ef23721",
    "rolling-planning": "6a7512b2f86bf7c33e39f110ea429e54aa05bcb7",
}
PLANNING_FIELDS = (
    "Horizon",
    "Primary Gap",
    "Progress",
    "Recent Effect",
    "Risk Budget",
    "Path Trade-off",
)
PLANNING_PROGRESS = ("ADVANCING", "STALLED", "UNKNOWN")
RISK_STATES = ("ALLOW", "WARN", "RECONSIDER", "UNKNOWN")
BOARD_FIELDS = (
    "game_session_id",
    "game_time_or_phase",
    "observed",
    "inferred",
    "unknown",
    "recent_effects",
    "action",
    "target_or_relevant_field",
    "before_after",
    "source",
    "source_or_freshness",
)
MARKERS = (
    "[S02_SKILL_USED]",
    "[S03_RISK:ALLOW]",
    "[S03_RISK:WARN]",
    "[S03_RISK:RECONSIDER]",
    "[S03_RISK:UNKNOWN]",
)
ALLOWED_CHANGED = {
    "skills/career-action-trace/SKILL.md",
    "skills/risk-review/SKILL.md",
    "skills/structured-state-board/SKILL.md",
    "skills/rolling-planning/SKILL.md",
    "docs/project/CURRENT_STATE.md",
    "docs/project/ARCHITECTURE_DECISIONS.md",
    f"{EXPERIMENT}/runtime_manifest.json",
    f"{EXPERIMENT}/candidate_manifest.json",
    f"{EXPERIMENT}/semantic_equivalence_matrix.md",
    f"{EXPERIMENT}/static_regression_matrix.md",
    f"{EXPERIMENT}/RESULT.md",
    f"{EXPERIMENT}/verify_static_contract.py",
}


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def git_blob(revision: str, path: str) -> bytes:
    return subprocess.check_output(["git", "show", f"{revision}:{path}"], cwd=ROOT)


def blob_id(revision: str, path: str) -> str:
    return git("rev-parse", f"{revision}:{path}")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def require(condition: bool, label: str, detail: str = "") -> None:
    print(f"{'PASS' if condition else 'FAIL'} | {label}" + (f" | {detail}" if detail else ""))
    if not condition:
        raise AssertionError(label + (f": {detail}" if detail else ""))


def parse_frontmatter(text: str) -> tuple[dict[str, object], str]:
    normalized = text.replace("\r\n", "\n")
    if not normalized.startswith("---\n"):
        raise ValueError("Skill does not begin with YAML frontmatter")
    _, raw, body = normalized.split("---", 2)
    data = yaml.safe_load(raw)
    if not isinstance(data, dict):
        raise ValueError("Skill frontmatter is not a YAML mapping")
    return data, body


def visible_prose(markdown: str) -> str:
    lines: list[str] = []
    in_fence = False
    for line in markdown.splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence:
            lines.append(line)
    text = "\n".join(lines)
    return re.sub(r"`[^`]*`", " ", text)


def language_counts(text: str) -> tuple[int, int]:
    han = len(re.findall(r"[\u4e00-\u9fff]", text))
    latin = len(re.findall(r"[A-Za-z]", text))
    return han, latin


def context_metrics(blobs: list[bytes]) -> dict[str, int]:
    texts = [item.decode("utf-8") for item in blobs]
    return {
        "bytes": sum(map(len, blobs)),
        "lines": sum(len(item.splitlines()) for item in texts),
        "chars": sum(map(len, texts)),
    }


def current_candidate_files() -> set[str]:
    changed = set(git("diff", "--name-only", BASE_MAIN, "HEAD").splitlines())
    status = git("status", "--porcelain")
    for line in status.splitlines():
        if line:
            path = line[3:]
            if " -> " in path:
                path = path.split(" -> ", 1)[1]
            changed.add(path.strip('"'))
    return changed


def source_checks() -> tuple[dict[str, str], dict[str, object], bytes, dict[str, str]]:
    runtime_path = ROOT / RUNTIME_PATH
    runtime_raw = runtime_path.read_bytes()
    runtime = json.loads(runtime_raw.decode("utf-8"))
    require(set(runtime) == {"team", "name", "mode", "instruction"}, "runtime manifest keys")
    require(runtime["name"] == "candidate-v3c-zh-aligned-policy", "runtime candidate name")
    require(runtime["mode"] == "agent" and bool(str(runtime["team"]).strip()), "submission team/mode")
    instruction = runtime["instruction"]
    require(isinstance(instruction, str) and bool(instruction.strip()), "non-empty runtime instruction")
    instruction_han, instruction_latin = language_counts(re.sub(r"`[^`]*`", " ", instruction))
    require(instruction_han > instruction_latin, "Chinese-dominant runtime instruction", f"Han={instruction_han}, Latin={instruction_latin}")

    skill_paths = [p / "SKILL.md" for p in (ROOT / "skills").iterdir() if p.is_dir() and (p / "SKILL.md").is_file()]
    names_on_disk = {path.parent.name for path in skill_paths}
    require(names_on_disk == set(SKILLS), "exactly four project-owned Skills", ", ".join(sorted(names_on_disk)))

    bodies: dict[str, str] = {}
    descriptions: dict[str, str] = {}
    for name in SKILLS:
        text = (ROOT / "skills" / name / "SKILL.md").read_text(encoding="utf-8")
        fields, body = parse_frontmatter(text)
        require(fields.get("name") == name, f"frontmatter identity: {name}")
        description = fields.get("description")
        require(isinstance(description, str) and bool(description.strip()), f"frontmatter description: {name}")
        desc_han, desc_latin = language_counts(re.sub(r"`[^`]*`", " ", str(description)))
        require(desc_han > desc_latin, f"Chinese-dominant description: {name}", f"Han={desc_han}, Latin={desc_latin}")
        prose = visible_prose(body)
        body_han, body_latin = language_counts(prose)
        require(body_han > body_latin, f"Chinese-dominant body: {name}", f"Han={body_han}, Latin={body_latin}")
        english_only = [
            paragraph.strip()
            for paragraph in re.split(r"\n\s*\n", prose)
            if language_counts(paragraph)[0] == 0 and language_counts(paragraph)[1] >= 32
        ]
        require(not english_only, f"no long English-only prose: {name}")
        bodies[name] = text
        descriptions[name] = str(description)

    trace = bodies["career-action-trace"]
    require("take_action" in trace and "notes" in trace, "Trace API fields")
    require("[S02_SKILL_USED]" in trace, "Trace marker exact")
    require("` [S02_SKILL_USED]`" in trace and "若 `notes` 为空，则只写 `[S02_SKILL_USED]`，前面不加空格" in trace,
            "Trace suffix and empty-notes spacing")
    require("只通过现有 `take_action` 工具提交一次" in trace, "Trace one-submit rule")

    risk = bodies["risk-review"]
    for token in RISK_STATES:
        require(f"`{token}`" in risk, f"Risk enum: {token}")
    for marker in MARKERS[1:]:
        require(marker in risk, f"Risk marker exact: {marker}")
    require("Soft Cost 单独只是机会成本，不能触发 `RECONSIDER`" in risk, "Soft Cost alone boundary")
    require("以下三项同时成立" in risk and "当前公开证据明确指出相关 `Material Risk`" in risk,
            "Risk reconsider all-conditions gate")
    require("rolling-planning` 负责" in risk and "本 Skill 只审查当前候选" in risk, "Risk Budget ownership/current candidate scope")
    require("处理历史埋雷" in risk and "实际效果仍为未知" in risk, "historical landmine special rule")

    board = bodies["structured-state-board"]
    for field in BOARD_FIELDS:
        require(field in board, f"Board field: {field}")
    for tool in ("new_game", "observe", "take_action"):
        require(tool in board, f"Board API: {tool}")
    require("最多五条公开日志" in board and "最多两组" in board, "Board bounded recovery 5/2")
    require("本局 `recent_effects` 最多两条" in board, "Board recent_effects cap")
    require("不得仅凭先后顺序声称因果" in board, "Board no sequence causality")
    require("不得" in board and "拥有 `Primary Gap`" in board and "推荐动作" in board, "Board no planning/recommendation")
    require("不得写入 `MEMORY.md`" in board and "新游戏 session 也必须从干净状态板开始" in board,
            "Board persistence/session isolation")

    planning = bodies["rolling-planning"]
    for field in PLANNING_FIELDS:
        require(f"{field}:" in planning, f"Planning field: {field}")
    for enum in PLANNING_PROGRESS:
        require(f"`{enum}`" in planning, f"Planning progress enum: {enum}")
    for enum in ("TIGHT", "AVAILABLE", "UNKNOWN"):
        require(f"`{enum}`" in planning, f"Risk Budget enum: {enum}")
    for tool in ("new_game", "observe", "take_action"):
        require(tool in planning, f"Planning API: {tool}")
    planning_steps = {
        int(match.group(1)): match.group(2)
        for match in re.finditer(r"(?m)^(\d+)\. (.+)$", planning)
    }
    require(set(planning_steps) == set(range(1, 11)), "ten Planning procedure steps")
    require("Energy" in planning_steps[1] and "observe" in planning_steps[1], "quarterly checkpoint control tokens")
    require("Primary Gap" in planning_steps[3], "single Primary Gap token")
    require(all(token in planning_steps[4] for token in ("ADVANCING", "STALLED", "UNKNOWN", "advertised effect", "observed effect")),
            "progress/effect control tokens")
    require("STALLED" in planning_steps[5] and "checkpoint" in planning_steps[5], "stall checkpoint control tokens")
    require(all(token in planning_steps[6] for token in ("Risk Budget", "TIGHT", "AVAILABLE", "UNKNOWN")), "Risk Budget states")
    ranking = planning_steps[7]
    ranking_tokens = ("Material Risk", "Primary Gap", "次级公开收益", "Soft Cost", "UNKNOWN")
    positions = [ranking.index(token) for token in ranking_tokens]
    require(positions == sorted(positions), "ordinary qualitative decision order")
    require(all(token in ranking for token in ("AVAILABLE", "Material Risk", "Soft Cost")), "controlled-aggression control tokens")
    require("48-month horizon" in planning_steps[8], "public horizon token")
    require("risk-review=RECONSIDER" in planning_steps[9], "ordinary-event reopen token")
    require("Primary Gap" in planning_steps[10] and "UNKNOWN" in planning_steps[10], "severe-review control tokens")
    output_schema = planning.split("## 输出", 1)[1].split("## 动作权限", 1)[0]
    require(all(f"{field}:" in output_schema for field in PLANNING_FIELDS), "six-field Planning output")

    instruction_plain = instruction.replace("`", "")
    runtime_tokens = (
        "rolling-planning", "Energy", "Planning checkpoint", "Primary Gap", "Material Risk", "Soft Cost",
        "Risk Budget", "TIGHT", "AVAILABLE", "UNKNOWN", "ADVANCING", "observed effect", "advertised effect",
        "STALLED", "48-month horizon", "risk-review=RECONSIDER", "Single Agent",
    )
    require(all(token.lower() in instruction_plain.lower() for token in runtime_tokens), "runtime structured control tokens")
    cue_order = ("重大风险门槛", "对 `Primary Gap` 的贡献", "次级公开收益", "`Soft Cost`/机会成本", "`UNKNOWN`")
    cue_positions = [instruction.index(token) for token in cue_order]
    require(cue_positions == sorted(cue_positions), "runtime qualitative decision order")

    semantic_text = (ROOT / SEMANTIC_MATRIX_PATH).read_text(encoding="utf-8")
    semantic_rows = re.findall(r"^\|\s*(?:CT|RR|SB|RP|RT)-\d{2}\s*\|.*\|\s*(EQUIVALENT|BLOCKED)\s*\|", semantic_text, re.MULTILINE)
    require(len(semantic_rows) == 104, "semantic equivalence rows", str(len(semantic_rows)))
    require(set(semantic_rows) == {"EQUIVALENT"}, "all semantic rows EQUIVALENT")
    require("strategy delta = NONE" in semantic_text, "semantic matrix strategy delta")

    regression_text = (ROOT / REGRESSION_MATRIX_PATH).read_text(encoding="utf-8")
    regression_rows = re.findall(r"^\|\s*(\d{1,2})\s*\|.*\|\s*(PASS|FAIL|PENDING)\s*\|\s*$", regression_text, re.MULTILINE)
    require(len(regression_rows) == 67, "67 acceptance matrix rows", str(len(regression_rows)))
    require({status for _, status in regression_rows} == {"PASS"}, "all static acceptance rows PASS")

    return bodies, runtime, runtime_raw, descriptions


def verify_candidate_manifest(runtime: dict[str, object], runtime_raw: bytes) -> str:
    candidate = json.loads((ROOT / CANDIDATE_PATH).read_text(encoding="utf-8"))
    require(candidate.get("candidate_id") == "candidate-v3c-zh-aligned-policy", "candidate ID")
    require(candidate.get("parent_candidate_id") == "candidate-v3b-final-policy", "parent candidate ID")
    require(candidate.get("base_main_sha") == BASE_MAIN, "accepted S06-03 main base")
    require(candidate.get("accepted_s06_03_branch") == "codex/s06-03-final-policy-tightening", "accepted S06-03 branch")
    require(candidate.get("accepted_s06_03_head_before_reconciliation") == S06_03_HEAD_BEFORE_ACCEPTANCE,
            "S06-03 pre-reconciliation HEAD")
    require(candidate.get("s06_03_acceptance_reconciliation_commit") == S06_03_ACCEPTANCE_COMMIT,
            "S06-03 acceptance reconciliation commit")
    implementation = str(candidate.get("candidate_implementation_commit", ""))
    require(bool(re.fullmatch(r"[0-9a-f]{40}", implementation)), "candidate implementation commit identity", implementation)
    require(git("merge-base", "--is-ancestor", implementation, "HEAD") == "", "implementation commit ancestor of HEAD")
    require(git("merge-base", "--is-ancestor", BASE_MAIN, implementation) == "", "updated main ancestor of implementation")
    require(git("merge-base", "--is-ancestor", S06_03_HEAD_BEFORE_ACCEPTANCE, BASE_MAIN) == "",
            "accepted S06-03 source ancestor of updated main")
    require(git("branch", "--show-current") == BRANCH, "S06-04 branch identity")

    recorded_parent = candidate.get("parent_v3b_skill_blobs")
    require(recorded_parent == PARENT_SKILL_BLOBS, "recorded v3b Skill identities")
    recorded_final = candidate.get("skill_blobs")
    require(isinstance(recorded_final, dict), "candidate Skill identity mapping")
    for name in SKILLS:
        path = f"skills/{name}/SKILL.md"
        require(blob_id(BASE_MAIN, path) == PARENT_SKILL_BLOBS[name], f"v3b parent blob: {name}")
        actual = blob_id(implementation, path)
        require(recorded_final.get(name) == actual, f"v3c implementation blob: {name}", actual)
        require((ROOT / path).read_bytes() == git_blob(implementation, path), f"working copy matches implementation: {name}")

    runtime_info = candidate.get("runtime_manifest")
    require(isinstance(runtime_info, dict), "runtime identity mapping")
    require(runtime_info.get("canonical_path") == RUNTIME_PATH, "canonical runtime path")
    runtime_from_commit = git_blob(implementation, RUNTIME_PATH)
    require(runtime_raw == runtime_from_commit, "runtime manifest matches implementation blob")
    require(runtime_info.get("sha256") == sha256(runtime_from_commit), "runtime manifest SHA-256")
    instruction_bytes = str(runtime["instruction"]).encode("utf-8")
    require(runtime_info.get("instruction_sha256") == sha256(instruction_bytes), "instruction SHA-256")
    require(runtime_info.get("instruction_bytes") == len(instruction_bytes), "instruction byte count")
    require(runtime_info.get("instruction_chars") == len(str(runtime["instruction"])), "instruction Unicode character count")
    require(candidate.get("semantic_equivalence_matrix_path") == SEMANTIC_MATRIX_PATH, "semantic matrix path")
    require(candidate.get("strategy_delta") == "NONE", "strategy delta NONE")
    require(candidate.get("language_refactor_only") is True, "language-only refactor flag")
    for key in ("gameplay_validated", "provider_validated", "stable_80_plus_proven", "next_game_authorized"):
        require(candidate.get(key) is False, f"candidate remains unvalidated: {key}")

    context = candidate.get("context")
    require(isinstance(context, dict), "context/language metrics")
    parent_metrics = context_metrics([git_blob(BASE_MAIN, f"skills/{name}/SKILL.md") for name in SKILLS])
    final_metrics = context_metrics([git_blob(implementation, f"skills/{name}/SKILL.md") for name in SKILLS])
    for key, measured in (("parent_v3b", parent_metrics), ("final_v3c", final_metrics)):
        require(context.get(f"{key}_skill_totals") == measured, f"{key} Skill context metrics", str(measured))
    delta = {key: final_metrics[key] - parent_metrics[key] for key in parent_metrics}
    require(context.get("skill_delta") == delta, "Skill context delta", str(delta))
    pct_bytes = round(delta["bytes"] * 100 / parent_metrics["bytes"], 2)
    pct_chars = round(delta["chars"] * 100 / parent_metrics["chars"], 2)
    require(context.get("skill_delta_percent_bytes") == pct_bytes, "Skill byte delta percent", str(pct_bytes))
    require(context.get("skill_delta_percent_chars") == pct_chars, "Skill character delta percent", str(pct_chars))

    parent_runtime_raw = git_blob(BASE_MAIN, "experiments/S06-03-final-policy-tightening/runtime_manifest.json")
    parent_runtime = json.loads(parent_runtime_raw.decode("utf-8"))
    parent_instruction = str(parent_runtime["instruction"])
    parent_runtime_info = candidate.get("parent_runtime_manifest")
    require(isinstance(parent_runtime_info, dict), "parent runtime identity mapping")
    require(parent_runtime_info.get("canonical_path") == "experiments/S06-03-final-policy-tightening/runtime_manifest.json",
            "parent runtime manifest path")
    require(parent_runtime_info.get("sha256") == sha256(parent_runtime_raw), "parent runtime manifest SHA-256")
    require(parent_runtime_info.get("instruction_sha256") == sha256(parent_instruction.encode("utf-8")),
            "parent instruction SHA-256")
    language_metrics = context.get("runtime_instruction")
    expected_language_metrics = {
        "parent_v3b_bytes": len(parent_instruction.encode("utf-8")),
        "parent_v3b_chars": len(parent_instruction),
        "final_v3c_bytes": len(instruction_bytes),
        "final_v3c_chars": len(str(runtime["instruction"])),
        "delta_bytes": len(instruction_bytes) - len(parent_instruction.encode("utf-8")),
        "delta_chars": len(str(runtime["instruction"])) - len(parent_instruction),
    }
    require(language_metrics == expected_language_metrics, "runtime instruction language metrics", str(expected_language_metrics))

    tokens = candidate.get("structured_tokens_preserved")
    require(isinstance(tokens, dict), "structured token inventory")
    require(tokens.get("skill_names") == list(SKILLS), "Skill token inventory")
    require(tokens.get("planning_fields") == list(PLANNING_FIELDS), "Planning field inventory")
    require(tokens.get("planning_progress_enums") == list(PLANNING_PROGRESS), "Planning progress enum inventory")
    require(tokens.get("risk_enums") == list(RISK_STATES), "Risk enum inventory")
    require(tokens.get("board_fields") == list(BOARD_FIELDS), "Board field inventory")
    require(tokens.get("tool_api_names") == ["new_game", "observe", "take_action"], "tool/API inventory")
    require(candidate.get("markers_preserved") == list(MARKERS), "trace/risk marker inventory")
    return implementation


def verify_artifact_identity(implementation: str) -> None:
    head = git("rev-parse", "HEAD")
    require(git("merge-base", "--is-ancestor", BASE_MAIN, head) == "", "base main ancestor of HEAD")
    changed = current_candidate_files()
    unexpected = sorted(changed - ALLOWED_CHANGED)
    require(not unexpected, "changed file scope", ", ".join(unexpected))
    for path in ("career_sim_runner", "pyproject.toml", "uv.lock", "docs/project/OFFICIAL_SOURCE_LOCK.md"):
        result = subprocess.run(["git", "diff", "--quiet", BASE_MAIN, "HEAD", "--", path], cwd=ROOT, check=False)
        require(result.returncode == 0, f"frozen path unchanged: {path}")
    result = subprocess.run(["git", "diff", "--quiet", BASE_MAIN, "HEAD", "--", "experiments/S06-03-final-policy-tightening"], cwd=ROOT, check=False)
    require(result.returncode == 0, "S06-03 historical artifacts unchanged")

    state = (ROOT / "docs/project/CURRENT_STATE.md").read_text(encoding="utf-8")
    require("S06-03: `COMPLETE_ACCEPTED_BY_MAIN`" in state, "dynamic state S06-03 acceptance")
    require("S06-04: `ZH_LANGUAGE_REFACTOR_READY_FOR_MAIN_REVIEW`" in state, "dynamic state S06-04 status")
    require("S06_CANDIDATE: `candidate-v3c-zh-aligned-policy`" in state, "dynamic state v3c candidate")
    require("NEXT_GAME: `NOT_AUTHORIZED`" in state, "dynamic state preserves Game Gate boundary")
    require("gameplay effectiveness" in state and "NOT_PROVEN" in state, "dynamic state gameplay limitation")
    adr = (ROOT / "docs/project/ARCHITECTURE_DECISIONS.md").read_text(encoding="utf-8")
    require("中文主体 + English structured control tokens" in adr, "ADR language architecture decision")
    require("strategy delta = NONE" in adr, "ADR no strategy delta")
    require("gameplay A/B 未证明分数收益" in adr, "ADR makes no score-benefit claim")

    tracked = git("ls-tree", "-r", "--name-only", "HEAD").splitlines()
    env_files = [p for p in tracked if PurePosixPath(p).name.lower() == ".env"]
    require(not env_files, "no tracked .env", ", ".join(env_files))
    changed_content: list[bytes] = []
    for path in sorted(changed):
        local = ROOT / path
        if local.is_file():
            changed_content.append(local.read_bytes())
        else:
            try:
                changed_content.append(git_blob("HEAD", path))
            except subprocess.CalledProcessError:
                continue
    secret_like = re.compile(rb"(?i)(?:sk-[A-Za-z0-9_-]{24,}|api[_-]?key\s*[:=]\s*['\"][^'\"]{24,})")
    require(not any(secret_like.search(data) for data in changed_content), "no secret-like values in candidate files")

def materialize(implementation: str) -> None:
    destination = WORKSPACE / ".local/runtime/s06-candidate-v3c-zh-aligned-policy/submission"
    require(not destination.exists(), "materialization target does not exist", str(destination))
    relative = destination.relative_to(WORKSPACE).as_posix()
    ignored = subprocess.run(["git", "check-ignore", "-q", relative], cwd=WORKSPACE, check=False).returncode == 0
    require(ignored, "static submission target is gitignored", relative)
    destination.mkdir(parents=True, exist_ok=False)
    files = [(RUNTIME_PATH, "manifest.json")]
    files.extend((f"skills/{name}/SKILL.md", f"skills/{name}/SKILL.md") for name in SKILLS)
    for source, target in files:
        path = destination / target
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(git_blob(implementation, source))
    expected = {"manifest.json", *(f"skills/{name}/SKILL.md" for name in SKILLS)}
    actual = {path.relative_to(destination).as_posix() for path in destination.rglob("*") if path.is_file()}
    require(actual == expected, "static submission layout", ", ".join(sorted(actual)))
    for source, target in files:
        require((destination / target).read_bytes() == git_blob(implementation, source), f"static submission byte identity: {target}")
    print(f"MATERIALIZED | {destination}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-only", action="store_true", help="check source text/matrices before candidate metadata exists")
    parser.add_argument("--materialize", action="store_true", help="write an ignored static copy; never install or run it")
    parser.add_argument("--require-clean", action="store_true", help="require a clean branch worktree")
    parser.add_argument("--require-remote", action="store_true", help="require fetched origin branch SHA to match HEAD")
    args = parser.parse_args()

    _, runtime, runtime_raw, _ = source_checks()
    if not args.source_only:
        implementation = verify_candidate_manifest(runtime, runtime_raw)
        verify_artifact_identity(implementation)
        if args.materialize:
            materialize(implementation)
        if args.require_clean:
            require(not git("status", "--porcelain"), "clean worktree")
        if args.require_remote:
            local = git("rev-parse", "HEAD")
            remote = git("rev-parse", f"origin/{BRANCH}")
            require(local == remote, "remote branch matches HEAD", remote)
    print("RESULT | S06-04 offline static contract PASS")


if __name__ == "__main__":
    main()
