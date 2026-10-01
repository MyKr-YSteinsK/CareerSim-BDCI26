"""Persistent Human Play Lab launcher: no-write preflight by default."""

from __future__ import annotations

import argparse
import asyncio
import builtins
import importlib.metadata as metadata
import importlib.util
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import uuid
from datetime import datetime, timezone
from io import StringIO
from pathlib import Path
from typing import Any, Callable, TextIO


WORKTREE_ROOT = Path(__file__).resolve().parents[1]
if str(WORKTREE_ROOT) not in sys.path:
    sys.path.insert(0, str(WORKTREE_ROOT))

from scripts.hpl_evidence_writer import write_run_evidence  # noqa: E402
from scripts.hpl_preflight import (  # noqa: E402
    EXPECTED_DATA_VERSION,
    EXPECTED_EMULATOR_VERSION,
    build_preflight,
)
from scripts.hpl_public_evidence import SCHEMA_VERSION  # noqa: E402
from hpl_client.path_contract import (  # noqa: E402, F401
    HPLLayout,
    _path_key,
    _is_within,
    _paths_overlap,
    protected_agent_paths,
    assert_isolated_run_root,
    engine_constructor_kwargs,
)


LAUNCHER_VERSION = "hpl-02/v1"
ENVIRONMENT_SCHEMA_VERSION = "hpl-environment/v1"
LOGS_BLOCK_MESSAGE = "HPL: raw logs are disabled by the public-evidence firewall"
_RUN_ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{0,63}$")
_ANSI_PATTERN = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]")
_FORBIDDEN_PACKAGE_NAMES = frozenset(
    {
        "anthropic",
        "deepseek",
        "fastmcp",
        "langchain",
        "litellm",
        "mcp",
        "openai",
        "jiuwenswarm",
    }
)


def resolve_layout(script_path: Path | str = __file__) -> HPLLayout:
    worktree_root = Path(script_path).resolve().parents[1]
    workspace_root = worktree_root.parent.parent.parent
    expected_worktree = workspace_root / ".local" / "worktrees" / "human-play-lab"
    if _path_key(worktree_root) != _path_key(expected_worktree):
        raise RuntimeError(f"HPL launcher must run from the persistent worktree: {expected_worktree}")
    sandbox_root = workspace_root / ".local" / "runtime" / "human-play-lab"
    return HPLLayout(workspace_root.resolve(), worktree_root.resolve(), sandbox_root.resolve(strict=False))


def _git_value(layout: HPLLayout, *args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=layout.worktree_root,
        check=True,
        capture_output=True,
        text=True,
        timeout=10,
    )
    return result.stdout.strip()


def _installed_distributions() -> list[dict[str, str]]:
    found: dict[str, str] = {}
    for distribution in metadata.distributions():
        name = distribution.metadata.get("Name")
        if name:
            found[name.lower().replace("_", "-")] = distribution.version
    return [{"name": name, "version": version} for name, version in sorted(found.items())]


def _module_root(module_name: str) -> Path:
    spec = importlib.util.find_spec(module_name)
    if spec is None or spec.origin is None:
        raise RuntimeError(f"HPL package module is not installed: {module_name}")
    return Path(spec.origin).resolve().parent


def _environment_identity(layout: HPLLayout) -> dict[str, Any]:
    expected_venv = (layout.sandbox_root / "venv").resolve(strict=False)
    active_venv = Path(sys.prefix).resolve()
    agent_venv = (layout.workspace_root / ".venv").resolve(strict=False)
    if _path_key(active_venv) != _path_key(expected_venv):
        raise RuntimeError(f"Human launcher interpreter is not the dedicated HPL venv: {expected_venv}")
    if _paths_overlap(active_venv, agent_venv):
        raise RuntimeError("Human Python environment overlaps the formal Agent root .venv")
    if not (3, 11) <= sys.version_info[:2] < (3, 14):
        raise RuntimeError(f"HPL Python must be >=3.11,<3.14, found {sys.version.split()[0]}")

    emulator_version = metadata.version("career-emulator")
    data_version = metadata.version("career-emulator-bdci26")
    if emulator_version != EXPECTED_EMULATOR_VERSION:
        raise RuntimeError(f"Expected career-emulator=={EXPECTED_EMULATOR_VERSION}, found {emulator_version}")
    if data_version != EXPECTED_DATA_VERSION:
        raise RuntimeError(f"Expected career-emulator-bdci26=={EXPECTED_DATA_VERSION}, found {data_version}")

    package_roots = {
        "career-emulator": _module_root("career_emulator"),
        "career-emulator-bdci26": _module_root("career_emulator_bdci26"),
    }
    for name, root in package_roots.items():
        if not _is_within(root, active_venv):
            raise RuntimeError(f"{name} resolves outside the dedicated HPL venv: {root}")

    resolved = _installed_distributions()
    desktop_identity = None
    if any(item["name"] == "flet" for item in resolved):
        from scripts.hpl_desktop_runtime import desktop_runtime_identity

        for name in ("flet", "flet-desktop"):
            if metadata.version(name) != "1.0.1" or not _is_within(_module_root(name.replace("-", "_")), active_venv):
                raise RuntimeError("Flet 1.0.1 must resolve inside the HPL venv")
        desktop_identity = desktop_runtime_identity(active_venv)
    forbidden = [
        item["name"] for item in resolved if item["name"].replace("_", "-").casefold() in _FORBIDDEN_PACKAGE_NAMES
    ]
    if forbidden:
        raise RuntimeError("HPL venv contains Agent/provider runtime packages: " + ", ".join(forbidden))

    probe = build_preflight(layout.sandbox_root / "sandbox" / ".identity-probe" / "runtime")
    dataset_root = Path(probe["dataset"]["root"]).resolve()
    data_distribution_root = package_roots["career-emulator-bdci26"]
    if not _is_within(dataset_root, data_distribution_root):
        raise RuntimeError("Pinned Dev dataset resolves outside the HPL BDCI26 distribution")
    return {
        "python_version": sys.version.split()[0],
        "python_executable": str(Path(sys.executable).resolve()),
        "python_prefix": str(active_venv),
        "python_base_prefix": str(Path(sys.base_prefix).resolve()),
        "package_identity": {
            "career-emulator": emulator_version,
            "career-emulator-bdci26": data_version,
        },
        "package_roots": {name: str(path) for name, path in package_roots.items()},
        "resolved_distributions": resolved,
        "desktop_runtime": desktop_identity,
        "forbidden_agent_provider_packages": forbidden,
        "dataset": probe["dataset"],
        "optional_external_share_dependency": (
            "gitcode-api is an upstream optional sharing dependency; the HPL CLI callback is replaced with a no-op"
            if any(item["name"] == "gitcode-api" for item in resolved)
            else None
        ),
    }


def _uv_version() -> str:
    executable = shutil.which("uv")
    if executable is None:
        return "UNKNOWN"
    return subprocess.run(
        [executable, "--version"], check=True, capture_output=True, text=True, timeout=10
    ).stdout.strip()


def write_environment_manifest(layout: HPLLayout, *, refresh: bool = False) -> dict[str, Any]:
    """Create the local, non-secret package/sandbox identity record once."""
    identity = _environment_identity(layout)
    manifest = {
        "schema_version": ENVIRONMENT_SCHEMA_VERSION,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "repository": "MyKr-YSteinsK/CareerSim-BDCI26",
        "hpl_branch": _git_value(layout, "branch", "--show-current"),
        "hpl_setup_commit": _git_value(layout, "rev-parse", "HEAD"),
        "installer": {"name": "uv", "version": _uv_version()},
        "platform": {
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
        },
        "python": {
            "version": identity["python_version"],
            "executable": identity["python_executable"],
            "prefix": identity["python_prefix"],
            "base_prefix": identity["python_base_prefix"],
        },
        "hpl_venv_root": str(layout.sandbox_root / "venv"),
        "formal_agent_root_venv_used": False,
        "package_identity": identity["package_identity"],
        "package_roots": identity["package_roots"],
        "resolved_distributions": identity["resolved_distributions"],
        "desktop_runtime": identity["desktop_runtime"],
        "forbidden_agent_provider_packages": identity["forbidden_agent_provider_packages"],
        "optional_external_share_dependency": identity["optional_external_share_dependency"],
        "dataset": identity["dataset"],
        "runtime_root": str(layout.sandbox_root),
        "runs_root": str(layout.runs_root),
        "provider_status": "STATIC_CLI_PATH_ONLY_NO_HUMAN_RUN",
    }
    path = layout.environment_manifest_path
    if path.is_symlink():
        raise RuntimeError("environment_manifest.json must not be a symlink")
    if layout.sandbox_root.is_symlink() or layout.runs_root.is_symlink():
        raise RuntimeError("HPL sandbox and runs roots must not be symlinks")
    path.parent.mkdir(parents=True, exist_ok=True)
    layout.runs_root.mkdir(parents=True, exist_ok=True)
    if path.exists():
        existing = json.loads(path.read_text(encoding="utf-8"))
        if (
            existing.get("package_identity") != manifest["package_identity"]
            or existing.get("package_roots") != manifest["package_roots"]
        ):
            raise RuntimeError("Existing HPL environment manifest does not match the installed environment")
        if not refresh:
            return existing
        import hashlib

        previous = path.read_bytes()
        digest = hashlib.sha256(previous).hexdigest()
        backup = path.with_name(f"environment_manifest.{digest}.json")
        if not backup.exists():
            backup.write_bytes(previous)
        manifest["previous_manifest_sha256"] = digest
    path.write_text(json.dumps(manifest, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    return manifest


def _load_environment_manifest(layout: HPLLayout) -> tuple[dict[str, Any], dict[str, Any]]:
    path = layout.environment_manifest_path
    if path.is_symlink() or not path.is_file():
        raise RuntimeError(f"HPL environment manifest is missing: {path}")
    manifest = json.loads(path.read_text(encoding="utf-8"))
    identity = _environment_identity(layout)
    expected_pairs = (
        (manifest.get("hpl_branch"), _git_value(layout, "branch", "--show-current")),
        (manifest.get("package_identity"), identity["package_identity"]),
        (manifest.get("package_roots"), identity["package_roots"]),
        (manifest.get("resolved_distributions"), identity["resolved_distributions"]),
        (manifest.get("desktop_runtime"), identity["desktop_runtime"]),
        (manifest.get("dataset", {}).get("root"), identity["dataset"]["root"]),
        (manifest.get("python", {}).get("executable"), identity["python_executable"]),
        (manifest.get("python", {}).get("prefix"), identity["python_prefix"]),
    )
    if any(recorded != current for recorded, current in expected_pairs):
        raise RuntimeError("HPL environment identity drifted from sandbox/environment_manifest.json")
    return manifest, identity


def build_dry_run_plan(
    layout: HPLLayout, run_id: str | None = None, authorization_id: str | None = None
) -> dict[str, Any]:
    """Validate the dedicated environment and show a prospective run without writes."""
    environment, _identity = _load_environment_manifest(layout)
    identifier = run_id or uuid.uuid4().hex
    if not _RUN_ID_PATTERN.fullmatch(identifier):
        raise ValueError("run_id must use only letters, digits, underscore, or hyphen")
    run_root = layout.runs_root / identifier
    if run_root.exists() or run_root.is_symlink():
        raise ValueError(f"prospective run root already exists: {run_root}")
    assert_isolated_run_root(run_root, layout)
    runtime = build_preflight(run_root / "runtime")
    return {
        "mode": "DRY_RUN_PREFLIGHT",
        "GAME_STARTED": False,
        "LIVE_AUTHORIZED": False,
        "authorization_gate": {
            "explicit_live_intent": False,
            "authorization_id_present": bool(authorization_id and authorization_id.strip()),
            "live_allowed": False,
        },
        "prospective_run_root": str(run_root),
        "run_root_created": False,
        "hpl_branch": environment["hpl_branch"],
        "hpl_setup_commit": environment["hpl_setup_commit"],
        "hpl_venv_root": environment["hpl_venv_root"],
        "package_identity": runtime["package_identity"],
        "package_roots": runtime["package_roots"],
        "dataset": runtime["dataset"],
        "runtime": runtime["runtime"],
        "provider_called": False,
        "dataset_updated": False,
        "protected_agent_path_overlap": False,
    }


def live_gate_allows(live_intent: bool, authorization_id: str | None) -> bool:
    """Return false without live intent; reject live intent without an authorization identity."""
    if not live_intent:
        return False
    if not authorization_id or not authorization_id.strip():
        raise PermissionError("Live intent requires a non-empty Main authorization identity")
    return True


def make_input_interceptor(
    reader: Callable[[str], str],
    write_message: Callable[[str], None],
    on_forward: Callable[[str, str], None] | None = None,
    on_blocked: Callable[[str], None] | None = None,
) -> Callable[[str], str]:
    """Block the raw logs command at the participant input boundary."""

    def guarded_input(prompt: str = "") -> str:
        while True:
            value = reader(prompt)
            if value.strip().casefold() == "logs":
                write_message(LOGS_BLOCK_MESSAGE)
                if on_blocked:
                    on_blocked(value)
                continue
            if on_forward:
                on_forward(prompt, value)
            return value

    return guarded_input


async def _disabled_share_callback(*_args: Any, **_kwargs: Any) -> None:
    """Replace the optional GitCode upload callback without reading its token."""


def wire_official_cli(cli_module: Any, engine: Any) -> None:
    """Patch only the official CLI's engine factory and optional share callback."""
    cli_module.get_default_engine = lambda: engine
    cli_module.offer_share = _disabled_share_callback


class _TeeTextIO:
    def __init__(self, target: TextIO, transcript: TextIO, capture: StringIO) -> None:
        self.target = target
        self.transcript = transcript
        self.capture = capture

    @property
    def encoding(self) -> str:
        return self.target.encoding or "utf-8"

    def write(self, value: str) -> int:
        self.transcript.write(value)
        self.capture.write(value)
        return self.target.write(value)

    def flush(self) -> None:
        self.transcript.flush()
        self.target.flush()

    def isatty(self) -> bool:
        return self.target.isatty()

    def writable(self) -> bool:
        return True

    def write_input(self, value: str) -> None:
        self.write(f"\n[HPL INPUT] {value}\n")

    def write_blocked(self) -> None:
        self.write("\n[HPL BLOCKED INPUT] logs\n")

    def captured_text(self) -> str:
        return self.capture.getvalue()


def _clean_line(line: str) -> str:
    return _ANSI_PATTERN.sub("", line).rstrip("\r")


def _is_heading(line: str, heading: str) -> bool:
    normalized = "".join(character for character in _clean_line(line) if character.isascii() and character.isalpha())
    expected = "".join(character for character in heading if character.isascii() and character.isalpha())
    return normalized.casefold() == expected.casefold()


def _number_line(lines: list[str], pattern: re.Pattern[str], start: int, end: int) -> tuple[int, re.Match[str]] | None:
    for index in range(start, min(end, len(lines))):
        match = pattern.search(lines[index])
        if match:
            return index, match
    return None


def parse_cli_transcript(transcript: str) -> list[dict[str, Any]]:
    """Parse only fields visibly rendered by the official participant CLI.

    Event and node identifiers are detected from the rendered suffix but replaced with a
    constant marker so the public projector can record only their paths.
    """
    lines = [_clean_line(line) for line in transcript.splitlines()]
    frames: list[dict[str, Any]] = []
    frame_line_indexes: list[int] = []
    session_pattern = re.compile(r"\bSession:\s*(\S+)")
    time_pattern = re.compile(r"(?P<level>.*?)\bMonth\s+(\d+)\s*\|\s*Quarter\s+(\d+)\s*\|\s*Year\s+(\d+)")
    energy_pattern = re.compile(r"Energy\s+(-?\d+)\s*\|\s*Output\s+(-?\d+)\s*\|\s*Wealth\s+(-?\d+)")
    status_pattern = re.compile(
        r"Dignity\s+(-?\d+)\s*\|\s*Health\s+(-?\d+)\s*\|\s*Network\s+(-?\d+)\s*\|\s*Skill\s+(-?\d+)"
    )
    choice_pattern = re.compile(r"^(\d+)\.\s+(.*?)(?:\s+\((\d+)\))?$")

    index = 0
    while index < len(lines):
        session_match = session_pattern.search(lines[index])
        if not session_match:
            index += 1
            continue
        state_result = _number_line(lines, time_pattern, index + 1, index + 5)
        if state_result is None:
            index += 1
            continue
        time_index, time_match = state_result
        state: dict[str, Any] = {
            "session_id": session_match.group(1),
            "level": time_match.group("level").strip(" │|"),
            "month": int(time_match.group(2)),
            "quarter": int(time_match.group(3)),
            "year": int(time_match.group(4)),
        }
        energy_result = _number_line(lines, energy_pattern, time_index + 1, time_index + 4)
        status_result = _number_line(lines, status_pattern, time_index + 1, time_index + 5)
        resource_end = time_index
        if energy_result:
            resource_end = max(resource_end, energy_result[0])
            state.update(
                energy=int(energy_result[1].group(1)),
                output=int(energy_result[1].group(2)),
                wealth=int(energy_result[1].group(3)),
            )
        if status_result:
            resource_end = max(resource_end, status_result[0])
            state.update(
                dignity=int(status_result[1].group(1)),
                health=int(status_result[1].group(2)),
                network=int(status_result[1].group(3)),
                skill=int(status_result[1].group(4)),
            )

        event_heading = None
        search_end = len(lines)
        for cursor in range(resource_end + 1, len(lines)):
            if session_pattern.search(lines[cursor]) or _is_heading(lines[cursor], "Ending Score"):
                search_end = cursor
                break
            if _is_heading(lines[cursor], "Event"):
                event_heading = cursor
                break

        frame: dict[str, Any] = {"state": state}
        if event_heading is not None:
            warning_lines = [
                line.strip()
                for line in lines[resource_end + 1 : event_heading]
                if line.strip() and "[HPL INPUT]" not in line and "[HPL BLOCKED INPUT]" not in line
            ]
            if warning_lines:
                if any("Extra statistics:" in line for line in warning_lines):
                    state["statistics"] = "<present>"
                    warning_lines = [line for line in warning_lines if "Extra statistics:" not in line]
                if warning_lines:
                    frame["warning"] = "\n".join(warning_lines)

            title_index = event_heading + 1
            while title_index < len(lines) and not lines[title_index].strip():
                title_index += 1
            event_title = lines[title_index].strip() if title_index < len(lines) else ""
            description_lines: list[str] = []
            choice_heading = None
            cursor = title_index + 1
            while cursor < len(lines):
                if _is_heading(lines[cursor], "Choice"):
                    choice_heading = cursor
                    break
                if session_pattern.search(lines[cursor]) or _is_heading(lines[cursor], "Ending Score"):
                    break
                if lines[cursor].strip() and "[HPL INPUT]" not in lines[cursor]:
                    description_lines.append(lines[cursor].strip())
                cursor += 1

            event_data: dict[str, Any] = {"title": event_title, "description": "\n".join(description_lines)}
            id_match = re.fullmatch(r"(?P<title>.*?)\s+\((?P<ids>[^()]*)\)", event_title)
            if id_match and ":" in id_match.group("ids"):
                event_data["title"] = id_match.group("title").strip()
                event_data["event_id"] = "<present>"
                event_data["node_id"] = "<present>"
            frame["event"] = event_data

            if choice_heading is not None:
                choices: list[dict[str, Any]] = []
                for cursor in range(choice_heading + 1, len(lines)):
                    line = lines[cursor].strip()
                    if not line or line.startswith("Choice number") or session_pattern.search(line):
                        if line.startswith("Choice number") or session_pattern.search(line):
                            break
                        continue
                    if _is_heading(line, "Event") or _is_heading(line, "Ending Score"):
                        break
                    match = choice_pattern.fullmatch(line)
                    if match:
                        choice: dict[str, Any] = {"choice": int(match.group(1)), "action": match.group(2)}
                        if match.group(3) is not None:
                            choice["energy_cost"] = int(match.group(3))
                        choices.append(choice)
                if choices:
                    frame["choices"] = choices
            frames.append(frame)
            frame_line_indexes.append(index)
            index = (choice_heading + 1) if choice_heading is not None else max(event_heading + 1, search_end)
            continue
        frames.append(frame)
        frame_line_indexes.append(index)
        index = max(index + 1, search_end)

    for heading_index, line in enumerate(lines):
        if not _is_heading(line, "Handbook"):
            continue
        end = heading_index + 1
        while end < len(lines) and "Press ENTER to continue" not in lines[end]:
            end += 1
        handbook = "\n".join(part.strip() for part in lines[heading_index + 1 : end] if part.strip())
        prior = [
            frame_index for frame_index, source_line in enumerate(frame_line_indexes) if source_line < heading_index
        ]
        if prior and handbook:
            frames[prior[-1]]["handbook"] = handbook

    ending_heading = next((i for i, line in enumerate(lines) if _is_heading(line, "Ending Score")), None)
    if ending_heading is not None and frames:
        result: dict[str, Any] = {}
        dimension_present = False
        for line in lines[ending_heading + 1 :]:
            grade = re.match(r"\s*([A-F])\s*:\s*(.*)$", line)
            if grade:
                result["grade"] = grade.group(1)
                continue
            outcome = re.search(r"(48-month completion|Early elimination)\s*\|\s*Survived\s+(\d+)\s+months", line)
            if outcome:
                result["outcome"] = outcome.group(1)
                result["survival_months"] = int(outcome.group(2))
                continue
            quantitative = re.search(r"Quantitative score:\s*(-?\d+(?:\.\d+)?)", line)
            if quantitative:
                result["quantitative_score"] = float(quantitative.group(1))
                continue
            partial = re.search(r"Score breakdown:\s*(-?\d+(?:\.\d+)?)", line)
            if partial:
                result["competition_partial_score"] = float(partial.group(1))
                continue
            if "weight" in line and "contribution" in line:
                dimension_present = True
        if dimension_present:
            result["dimensions"] = "<present>"
        if result:
            frames[-1]["final_result"] = result
    return frames


def attach_public_selection(frames: list[dict[str, Any]], frame_index: int, raw_choice: str) -> None:
    """Attach a human choice only when it matches a currently rendered legal choice."""
    if frame_index < 0 or frame_index >= len(frames):
        return
    try:
        choice_number = int(raw_choice.strip())
    except ValueError:
        return
    frame = frames[frame_index]
    for choice in frame.get("choices", []):
        if choice.get("choice") == choice_number:
            frame["human_selection"] = {"choice": choice_number, "action": choice["action"]}
            return


def _provider_evidence(identity: dict[str, Any], share_callback_disabled: bool) -> dict[str, Any]:
    if identity["forbidden_agent_provider_packages"]:
        raise RuntimeError("Provider/Agent package appeared in HPL runtime identity")
    if not share_callback_disabled:
        raise RuntimeError("External share callback must be disabled before a Human run")
    return {
        "provider_used": False,
        "provider_evidence_basis": [
            "dedicated HPL venv contains no Jiuwen/MCP/LLM provider runtime package",
            "career-emulator 1.0.1 participant CLI path was source-inspected as local GameEngine/SQLite",
            "optional GitCode share callback is replaced before CLI play",
        ],
        "evidence_scope": "STATIC_LAUNCHER_AND_DEPENDENCY_IDENTITY; no Human Run has occurred",
    }


def _write_noop_message(message: str) -> None:
    print(message)


def _record_run(
    layout: HPLLayout, run_root: Path, authorization_id: str, human_tag: str, identity: dict[str, Any]
) -> None:
    runtime = run_root / "runtime"
    db_path = runtime / "career_emulator.sqlite3"
    log_dir = runtime / "logs"
    transcript_dir = run_root / "transcript"
    transcript_path = transcript_dir / "terminal.txt"
    preflight = build_preflight(runtime)
    assert_isolated_run_root(run_root, layout)
    run_root.mkdir(parents=True, exist_ok=False)
    for directory in (runtime, log_dir, transcript_dir, run_root / "scratch"):
        directory.mkdir()

    # These must be set before importing career_emulator.cli/game/storage.
    os.environ["CAREER_EMULATOR_DB"] = str(db_path)
    os.environ["CAREER_EMULATOR_LOG_DIR"] = str(log_dir)

    from career_emulator import cli  # noqa: PLC0415
    from career_emulator.game import GameEngine  # noqa: PLC0415

    engine = GameEngine(**engine_constructor_kwargs(preflight["dataset"]["engine_paths"], db_path))
    wire_official_cli(cli, engine)
    if cli.get_default_engine() is not engine:
        raise RuntimeError("Official CLI engine hook did not retain the pinned HPL GameEngine")
    share_callback_disabled = cli.offer_share is _disabled_share_callback
    provider = _provider_evidence(identity, share_callback_disabled=share_callback_disabled)
    cli.configure_stdio(sys.stdout)
    cli.configure_stdio(sys.stderr)

    capture = StringIO()
    selections: dict[int, dict[str, Any]] = {}
    original_stdout, original_stderr, original_input = sys.stdout, sys.stderr, builtins.input
    with transcript_path.open("w", encoding="utf-8", newline="\n") as transcript_file:
        stdout_tee = _TeeTextIO(original_stdout, transcript_file, capture)
        stderr_tee = _TeeTextIO(original_stderr, transcript_file, capture)

        def record_input(prompt: str, value: str) -> None:
            stdout_tee.write_input(value)
            if value.strip().isdigit():
                frames = parse_cli_transcript(stdout_tee.captured_text())
                if frames:
                    attach_public_selection(frames, len(frames) - 1, value)
                    selection = frames[-1].get("human_selection")
                    if selection:
                        selections[len(frames) - 1] = selection

        def record_blocked(value: str) -> None:
            stdout_tee.write_blocked()

        sys.stdout = stdout_tee  # type: ignore[assignment]
        sys.stderr = stderr_tee  # type: ignore[assignment]
        builtins.input = make_input_interceptor(original_input, _write_noop_message, record_input, record_blocked)
        started_at = datetime.now(timezone.utc).isoformat()
        try:
            asyncio.run(cli.play())
        finally:
            sys.stdout.flush()
            sys.stderr.flush()
            sys.stdout, sys.stderr, builtins.input = original_stdout, original_stderr, original_input
        captured = capture.getvalue()

    frames = parse_cli_transcript(captured)
    for frame_index, selection in selections.items():
        if frame_index < len(frames):
            frames[frame_index]["human_selection"] = selection
    session_ids = [
        frame["state"]["session_id"] for frame in frames if isinstance(frame.get("state", {}).get("session_id"), str)
    ]
    manifest = {
        "run_id": run_root.name,
        "authorization_id": authorization_id,
        "session_id": session_ids[0] if session_ids and len(set(session_ids)) == 1 else None,
        "human_tag": human_tag,
        "started_at": started_at,
        "ended_at": datetime.now(timezone.utc).isoformat(),
        "hpl_commit": _git_value(layout, "rev-parse", "HEAD"),
        "launcher_version": LAUNCHER_VERSION,
        "python_version": identity["python_version"],
        "career_emulator_version": identity["package_identity"]["career-emulator"],
        "career_emulator_bdci26_version": identity["package_identity"]["career-emulator-bdci26"],
        "dataset_source": "distribution",
        "dataset_split": "dev",
        "dataset_root": preflight["dataset"]["root"],
        "hpl_venv_root": identity["python_prefix"],
        "hpl_runtime_root": str(run_root),
        "provider_used": provider["provider_used"],
        "provider_evidence_basis": provider["provider_evidence_basis"],
        "provider_evidence_scope": provider["evidence_scope"],
        "public_evidence_schema_version": SCHEMA_VERSION,
    }
    write_run_evidence(run_root, manifest, frames, transcript_path=transcript_path)
    print(f"HPL evidence written under {run_root / 'evidence'}")


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live", action="store_true", help="Explicit live intent; requires a Main authorization ID.")
    parser.add_argument("--authorization-id", default=None, help="Non-empty Main gate identity required with --live.")
    parser.add_argument(
        "--refresh-environment-manifest",
        action="store_true",
        help="Explicitly record an authorized HPL dependency change; preserve the old manifest.",
    )
    parser.add_argument("--tag", default="manual", help="Human research tag recorded in a future authorized run.")
    parser.add_argument(
        "--write-environment-manifest",
        action="store_true",
        help="One-time local package identity setup; does not launch the emulator or create a run.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        layout = resolve_layout()
        if args.write_environment_manifest or args.refresh_environment_manifest:
            if args.live or args.authorization_id:
                raise ValueError("environment setup cannot be combined with live arguments")
            manifest = write_environment_manifest(layout, refresh=args.refresh_environment_manifest)
            print(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True))
            return 0
        if not live_gate_allows(args.live, args.authorization_id):
            print(
                json.dumps(
                    build_dry_run_plan(layout, authorization_id=args.authorization_id), ensure_ascii=False, indent=2
                )
            )
            return 0
        _environment, identity = _load_environment_manifest(layout)
        run_id = uuid.uuid4().hex
        run_root = layout.runs_root / run_id
        assert_isolated_run_root(run_root, layout)
        _record_run(layout, run_root, args.authorization_id, args.tag, identity)
        return 0
    except (OSError, RuntimeError, ValueError, PermissionError, subprocess.SubprocessError) as error:
        print(f"HPL preflight blocked: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
