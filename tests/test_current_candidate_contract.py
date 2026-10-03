"""Durable current-Candidate identity and written-policy checks; no model oracle."""

import hashlib
import json
import re
import shutil
import subprocess
from pathlib import Path

import pytest
import yaml

from scripts.package_candidate import build_submission


ROOT = Path(__file__).resolve().parents[1]
SKILLS = {"career-state-brief", "career-decision"}
FIELDS = {
    "SESSION_BASIS", "REVIEW_OBJECTIVE", "RESULT_COMMITMENT",
    "UNRESOLVED_CONSTRAINT", "PATH_UPDATE_STOP",
}


def _json(root: Path, path: str) -> dict:
    return json.loads((root / path).read_text(encoding="utf-8"))


def _skill(name: str) -> str:
    return (ROOT / "skills" / name / "SKILL.md").read_text(encoding="utf-8")


def _section(text: str, title: str) -> str:
    return text.split(f"## {title}\n", 1)[1].split("\n## ", 1)[0]


def _save(root: Path, path: str, data: dict) -> None:
    (root / path).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def test_current_identity_active_set_and_static_nonclaims() -> None:
    candidate = _json(ROOT, "configs/current_candidate.json")
    manifest = _json(ROOT, "configs/runtime_manifest.json")
    assert candidate["candidate_id"] == manifest["name"] == "candidate-v12-lean-career-brief"
    assert manifest["mode"] == "agent"
    assert candidate["status"] == "STATIC_IMPLEMENTED_NOT_RUNTIME_VALIDATED"
    assert candidate["architecture"]["action_submitter"] == "Single Agent"
    assert candidate["architecture"]["skill_count"] == 2
    assert set(candidate["architecture"]["active_skills"]) == SKILLS
    assert {entry["name"] for entry in candidate["skills"]} == SKILLS
    assert len(candidate["skills"]) == 2
    assert {p.parent.name for p in (ROOT / "skills").glob("*/SKILL.md")} == SKILLS
    assert candidate["architecture"]["team_swarm"] == "NOT_IMPLEMENTED"
    assert candidate["architecture"]["fifth_skill"] == "NOT_IMPLEMENTED"
    for flag in (
        "runtime_validated", "gameplay_validated", "provider_validated",
        "score_improvement_proven", "stable_75_plus_proven", "stable_80_plus_proven",
        "hidden_test_transfer_proven", "next_game_authorized",
    ):
        assert candidate["validation"][flag] is False
    assert all(value is False for value in candidate["validation"].values())


def test_fallback_identity_ancestry_and_protected_files() -> None:
    candidate = _json(ROOT, "configs/current_candidate.json")
    fallback = candidate["fallback"]
    assert fallback["candidate_id"] == candidate["parent_candidate_id"] == "candidate-v8a-v7o-donor-core-transplant"
    assert fallback["main_sha"] == candidate["base_main_sha"]
    assert fallback["accepted_parent_sha"] == candidate["parent_sha"]
    parent = candidate["parent_sha"]
    subprocess.run(["git", "merge-base", "--is-ancestor", candidate["base_main_sha"], parent], cwd=ROOT, check=True)
    old = json.loads(subprocess.check_output(["git", "show", f"{parent}:configs/current_candidate.json"], cwd=ROOT))
    assert old["candidate_id"] == fallback["candidate_id"]
    assert old["status"] == "FINAL_FROZEN_FOR_SUBMISSION"
    assert old["runtime_manifest"] == fallback["runtime_manifest"]
    assert old["skills"] == fallback["skills"]
    blob = subprocess.check_output(
        ["git", "rev-parse", f"{fallback['main_sha']}:configs/current_candidate.json"], cwd=ROOT, text=True,
    ).strip()
    assert blob == fallback["current_candidate_git_blob"]
    for path in (
        "career_sim_runner", "pyproject.toml", "uv.lock", "docs/project/OFFICIAL_SOURCE_LOCK.md",
        "scripts/build_final_solution.py", "submission_materials",
    ):
        assert not subprocess.check_output(["git", "diff", parent, "--", path], cwd=ROOT).strip()


def test_current_hashes_yaml_and_ownership() -> None:
    candidate = _json(ROOT, "configs/current_candidate.json")
    data = (ROOT / "configs/runtime_manifest.json").read_bytes()
    manifest = json.loads(data)
    assert hashlib.sha256(data).hexdigest() == candidate["runtime_manifest"]["sha256"]
    assert hashlib.sha256(manifest["instruction"].encode("utf-8")).hexdigest() == candidate["runtime_manifest"]["instruction_sha256"]
    for entry in candidate["skills"]:
        path = ROOT / entry["path"]
        text = path.read_text(encoding="utf-8")
        assert yaml.safe_load(text.split("---", 2)[1])["name"] == entry["name"]
        assert yaml.safe_load(text.split("---", 2)[1])["description"]
        assert "Can Submit Action: No." in text
        assert hashlib.sha256(path.read_bytes()).hexdigest() == entry["sha256"]
        blob = subprocess.check_output(["git", "hash-object", f"--path={entry['path']}", str(path)], cwd=ROOT, text=True).strip()
        assert blob == entry["git_blob"]


def test_hashed_runtime_sources_checkout_with_lf() -> None:
    candidate = _json(ROOT, "configs/current_candidate.json")
    paths = [candidate["runtime_manifest"]["path"], *(entry["path"] for entry in candidate["skills"])]
    attributes = subprocess.check_output(["git", "check-attr", "eol", "--", *paths], cwd=ROOT, text=True)
    assert len(attributes.splitlines()) == 3
    assert all(line.endswith(": eol: lf") for line in attributes.splitlines())


def test_brief_is_one_logical_current_state_with_explicit_recovery_limits() -> None:
    candidate = _json(ROOT, "configs/current_candidate.json")
    brief = candidate["career_brief"]
    assert brief["mechanism"] == "CONVERSATION_RESIDENT"
    assert set(brief["fields"]) == FIELDS and len(brief["fields"]) == 5
    assert brief["writer"] == "career-state-brief"
    assert brief["physical_context_deletion"] is False
    assert brief["durable_persistence_proven"] is False
    state = _skill("career-state-brief")
    field_block = re.search(r"```text\n(.*?)\n```", state, re.S).group(1)
    assert {line.split(":", 1)[0] for line in field_block.splitlines()} == FIELDS
    assert "supersedes" in state and "旧对话没有物理删除" in state
    assert "session 改变立即丢弃整份旧 Brief" in state
    assert "普通 action 不全量输出 Brief" in state
    assert "不为了简短静默删除" in state
    recovery = _section(state, "Recovery")
    for fragment in ("fresh observe", "重读两个职责文档", "最小同局官方", "UNKNOWN", "同一 session"):
        assert fragment in recovery
    assert "不是 fresh public truth" in recovery
    assert "无法确认 session、fresh observe 或文档读取失败时不动作" in recovery


@pytest.mark.parametrize("scenario,skill,section,required", [
    ("missing choice metadata degrades safely", "career-state-brief", "三类证据", ("未返回的字段不猜测", "不因缺字段阻断整局")),
    ("advertised HiddenRisk is not a measured stock", "career-state-brief", "三类证据", ("HiddenRisk", "不是当前 hidden stock", "累积 deltas 估算隐藏存量")),
    ("success receipt cannot verify delivery", "career-state-brief", "三类证据", ("receipt 只证明工具执行", "不证明职业成果", "advertised delta 不能更新 current state")),
    ("generic praise does not clear prior trust concern", "career-state-brief", "更新与失效", ("同 scope", "公开解除证据", "generic praise、无新 warning 不证明解除")),
    ("mixed changes do not prove clean no gain", "career-state-brief", "更新与失效", ("无 Review/promotion/salary/延迟结果等混杂", "混杂、未测与缺证据均 UNKNOWN")),
    ("level change invalidates old tested path", "career-state-brief", "更新与失效", ("Level 改变时清除", "不把旧 NO_GAIN 当永久 cap")),
    ("ordinary cost does not veto superior growth", "career-decision", "Ordinary decision", ("普通 workload", "本身不否决更强成长", "真正可达的恢复路径")),
    ("early result feasibility has exceptions", "career-decision", "Ordinary decision", ("首评前尤其比较现实可交成果", "不挡明显更强时限机会", "没有这样的菜单机会不伪造")),
    ("local no gain leaves untested families open", "career-decision", "Ordinary decision", ("已测 action family", "未知 family 仍开放", "不构建全局cap")),
    ("energy success does not authorize a batch", "career-decision", "Ordinary decision", ("每次只推荐一个Energy action", "没有余动作序列/固定配额", "执行后fresh observe")),
    ("replacement choice still gets its own safety check", "career-decision", "Final selected-candidate safety", ("最多做一次替代比较", "替代也必须再检查其自身安全", "session不确定", "不提交")),
    ("ordinary story and duplicate checkpoint do not deep review", "career-decision", "Same-agent material-checkpoint Deep Review", ("每个新Story菜单不自动deep review", "同checkpoint重复observe不重评", "合并一次深评")),
    ("unknown action cannot be blindly retried", "career-decision", "Executor handoff", ("unknown action outcome", "停止提交", "不能盲重发", "仍unknown")),
    ("a closed choice is not whole-game termination", "career-decision", "Executor handoff", ("已有session绝不第二次", "whole-game loop", "不因一个choice", "game.ended")),
])
def test_written_behavior_contract_scenarios(scenario: str, skill: str, section: str, required: tuple) -> None:
    """Check operative policy boundaries; does not predict a model's chosen action."""
    policy = _section(_skill(skill), section)
    for fragment in required:
        assert fragment in policy, f"{scenario}: missing policy boundary {fragment}"


def test_active_runtime_has_no_retired_protocol_dependency() -> None:
    manifest = _json(ROOT, "configs/runtime_manifest.json")["instruction"]
    runtime = manifest + "\n" + "\n".join(_skill(name) for name in SKILLS)
    for token in (
        "[CTRL", "[DL", "RB=", "CONTROL_STATE", "OBSERVE_REQUIRED", "PREFLIGHT=",
        "DELIVERY_CLAIMED", "NEXT_ID", "REVIEW_PLAN", "QUARTER_INTENT", "BC=", "certificate",
        "structured-state-board", "delivery-progress", "rolling-planning", "risk-review",
    ):
        assert token not in runtime
    assert not re.search(r"(?:D[123]|STALLED|CP=|Risk Budget)", runtime)
    contract = (ROOT / "docs/project/AGENT_RUNTIME_CONTRACT.md").read_text(encoding="utf-8")
    assert "S10 FAMILY A STATIC ARCHITECTURE / NOT RUNTIME VALIDATED" in contract
    assert "CONVERSATION_RESIDENT" in contract
    assert "未来S10 live audit需窄适配" in contract
    assert not re.search(r"(?:读取|重读)四", runtime + contract)
    for term in ("fresh observe", "game.ended", "unknown outcome", "两个竞争候选", "Deep Review"):
        assert term in manifest


@pytest.fixture
def candidate_copy(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    (repo / "configs").mkdir(parents=True)
    for name in ("runtime_manifest.json", "current_candidate.json"):
        shutil.copyfile(ROOT / "configs" / name, repo / "configs" / name)
    for name in SKILLS:
        shutil.copytree(ROOT / "skills" / name, repo / "skills" / name)
    return repo


@pytest.mark.parametrize("mutation", [
    "manifest_identity", "manifest_mode", "empty_instruction", "manifest_bytes",
    "instruction_digest", "duplicate_active", "count", "missing_entry", "duplicate_entry",
    "unsafe_name", "wrong_path", "extra_source", "missing_source", "invalid_frontmatter", "skill_bytes",
])
def test_packager_rejects_inconsistent_inputs_before_output(candidate_copy: Path, mutation: str, tmp_path: Path) -> None:
    repo = candidate_copy
    candidate = _json(repo, "configs/current_candidate.json")
    manifest = _json(repo, "configs/runtime_manifest.json")
    if mutation == "manifest_identity":
        manifest["name"] = "wrong-candidate"
    elif mutation == "manifest_mode":
        manifest["mode"] = "team"
    elif mutation == "empty_instruction":
        manifest["instruction"] = " "
    elif mutation == "manifest_bytes":
        manifest["instruction"] += "changed"
    elif mutation == "instruction_digest":
        candidate["runtime_manifest"]["instruction_sha256"] = "invalid"
    elif mutation == "duplicate_active":
        candidate["architecture"]["active_skills"].append("career-decision")
    elif mutation == "count":
        candidate["architecture"]["skill_count"] = 4
    elif mutation == "missing_entry":
        candidate["skills"].pop()
    elif mutation == "duplicate_entry":
        candidate["skills"][1] = candidate["skills"][0].copy()
    elif mutation == "unsafe_name":
        candidate["architecture"]["active_skills"][0] = "../outside"
    elif mutation == "wrong_path":
        candidate["skills"][0]["path"] = "../outside/SKILL.md"
    elif mutation == "extra_source":
        extra = repo / "skills" / "extra" / "SKILL.md"
        extra.parent.mkdir()
        extra.write_text("extra", encoding="utf-8")
    elif mutation == "missing_source":
        (repo / "skills" / "career-decision" / "SKILL.md").unlink()
    elif mutation == "invalid_frontmatter":
        (repo / "skills" / "career-decision" / "SKILL.md").write_text("no YAML", encoding="utf-8")
    elif mutation == "skill_bytes":
        with (repo / "skills" / "career-decision" / "SKILL.md").open("a", encoding="utf-8") as handle:
            handle.write("changed")
    _save(repo, "configs/current_candidate.json", candidate)
    if mutation in {"manifest_identity", "manifest_mode", "empty_instruction", "manifest_bytes"}:
        _save(repo, "configs/runtime_manifest.json", manifest)
    output = tmp_path / "rejected-output"
    with pytest.raises(ValueError):
        build_submission(repo, output)
    assert not output.exists()


def test_packager_refuses_existing_nonempty_output(candidate_copy: Path, tmp_path: Path) -> None:
    output = tmp_path / "existing"
    output.mkdir()
    sentinel = output / "user-file.txt"
    sentinel.write_text("keep", encoding="utf-8")
    with pytest.raises(FileExistsError):
        build_submission(candidate_copy, output)
    assert sentinel.read_text(encoding="utf-8") == "keep"
    assert list(output.iterdir()) == [sentinel]
