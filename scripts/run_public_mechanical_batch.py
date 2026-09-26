"""Bounded direct-public-MCP batch runner for S07-07.

The live path is opt-in through ``--live`` and is intentionally serialized.
Importing this module, running its tests, or calling the offline helpers never
starts a process or calls MCP. Only participant-visible projected fields enter
the controller and compact reports.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import sys
from collections.abc import Mapping, Sequence
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Protocol

from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client

from scripts.public_mechanical_probe import (
    ActionDecision,
    MechanicalProbe,
    MinIdControl,
    PublicSnapshot,
    SimplePublicGrowthPrior,
    StallAwarePublicGrowth,
    classify_structural_context,
    project_public_snapshot,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
MCP_EXECUTABLE = REPO_ROOT / ".venv" / "Scripts" / "career-emulator-mcp.exe"
DEFAULT_RUNTIME_ROOT = REPO_ROOT / ".local" / "runtime" / "s07-07-mechanical-batch"
DEFAULT_EVIDENCE_PATH = REPO_ROOT / "docs" / "project" / "runs" / "s07-07-mechanical-probe-batch.json"
ACTION_CEILING = 300

# Only direct, public action-label semantics are mapped. Multi-target or
# hidden-risk actions remain unmapped so the tracker cannot invent causality.
STRUCTURAL_TARGETS: dict[str, tuple[str, str]] = {
    "人脉维护": ("network", "energy:network"),
    "健康恢复": ("health", "energy:health"),
    "心理修复": ("dignity", "energy:dignity"),
    "准备汇报材料": ("output", "energy:output"),
}


class PublicBatchError(RuntimeError):
    """Base class for bounded public-interface failures."""


class ExplicitToolError(PublicBatchError):
    """The server returned an explicit MCP/tool error, not an unknown outcome."""


class PublicBoundaryError(PublicBatchError):
    """A response exposed a field that cannot safely enter the public projection."""


class UnknownSideEffectError(PublicBatchError):
    """Transport/timeout state is not safe to retry."""


class ProtocolError(PublicBatchError):
    """The public protocol or response shape cannot be used safely."""


class PublicToolClient(Protocol):
    async def initialize(self) -> None: ...

    async def list_tools(self) -> list[dict[str, Any]]: ...

    async def call_tool(self, name: str, arguments: dict[str, Any]) -> Mapping[str, Any]: ...


def _is_json_scalar(value: Any) -> bool:
    return value is None or isinstance(value, (str, bool, int, float))


def _public_score(value: Any) -> dict[str, Any] | None:
    if not isinstance(value, Mapping):
        return None
    result: dict[str, Any] = {}
    for key, item in value.items():
        if _is_json_scalar(item):
            result[str(key)] = item
    return result or None


def _unwrap_mapping(value: Mapping[str, Any]) -> Mapping[str, Any]:
    nested = value.get("result")
    if isinstance(nested, Mapping) and len(value) <= 2:
        return nested
    return value


def decode_mcp_result(result: Any) -> Mapping[str, Any]:
    """Decode one already-received MCP result without logging raw content."""

    if bool(getattr(result, "isError", False)):
        raise ExplicitToolError("server returned an explicit MCP tool error")

    structured = getattr(result, "structuredContent", None)
    if isinstance(structured, Mapping):
        return _unwrap_mapping(structured)

    content = getattr(result, "content", None)
    if isinstance(content, Sequence):
        for block in content:
            if getattr(block, "type", None) != "text":
                continue
            text = getattr(block, "text", "")
            if not isinstance(text, str):
                continue
            try:
                decoded = json.loads(text)
            except json.JSONDecodeError:
                continue
            if isinstance(decoded, Mapping):
                return _unwrap_mapping(decoded)
    raise ProtocolError("MCP result did not contain a public JSON mapping")


class MCPClientAdapter:
    """Adapt the frozen MCP SDK session to the offline-testable client shape."""

    def __init__(self, session: ClientSession) -> None:
        self.session = session

    async def initialize(self) -> None:
        await self.session.initialize()

    async def list_tools(self) -> list[dict[str, Any]]:
        result = await self.session.list_tools()
        tools: list[dict[str, Any]] = []
        for tool in result.tools:
            schema = getattr(tool, "inputSchema", {})
            if hasattr(schema, "model_dump"):
                schema = schema.model_dump(by_alias=True)
            if not isinstance(schema, Mapping):
                schema = {}
            tools.append({"name": str(getattr(tool, "name", "")), "inputSchema": dict(schema)})
        return tools

    async def call_tool(self, name: str, arguments: dict[str, Any]) -> Mapping[str, Any]:
        try:
            result = await self.session.call_tool(name, arguments)
        except (TimeoutError, ConnectionError, BrokenPipeError, OSError) as exc:
            raise UnknownSideEffectError(f"MCP {name} transport failed: {type(exc).__name__}") from exc
        return decode_mcp_result(result)


def validate_public_tools(tools: Sequence[Mapping[str, Any]]) -> tuple[list[str], bool]:
    """Validate only the public tool names and input contracts needed here."""

    normalized = {str(tool.get("name", "")): tool for tool in tools}
    names = sorted(name for name in normalized if name)
    suspicious_tokens = ("private", "hidden", "internal", "debug", "admin")
    if any(any(token in name.lower() for token in suspicious_tokens) for name in names):
        raise PublicBoundaryError("suspicious non-public tool name exposed")

    required = {"new_game", "observe", "take_action"}
    if not required.issubset(normalized):
        raise ProtocolError("required public CareerSim tools are incomplete")

    def schema_for(name: str) -> Mapping[str, Any]:
        schema = normalized[name].get("inputSchema", {})
        return schema if isinstance(schema, Mapping) else {}

    observe_required = set(schema_for("observe").get("required", []))
    action_required = set(schema_for("take_action").get("required", []))
    if "session_id" not in observe_required or {"session_id", "choice", "notes"} - action_required:
        raise ProtocolError("public observe/take_action schema is incompatible")

    action_properties = schema_for("take_action").get("properties", {})
    choice_schema = action_properties.get("choice", {}) if isinstance(action_properties, Mapping) else {}
    if not isinstance(choice_schema, Mapping) or choice_schema.get("type") not in {"integer", "number"}:
        raise ProtocolError("public take_action.choice is not an integer-compatible field")

    new_properties = schema_for("new_game").get("properties", {})
    if not isinstance(new_properties, Mapping):
        new_properties = {}
    seed_fields = {str(key) for key in new_properties if str(key).lower() in {"seed", "replay", "random_seed"}}
    return names, bool(seed_fields)


def project_session_snapshot(payload: Mapping[str, Any], expected_session_id: str) -> PublicSnapshot:
    """Project one observe payload and fail closed on identity/private leakage."""

    candidate = dict(payload)
    if "session_id" not in candidate:
        candidate["session_id"] = expected_session_id
    snapshot = project_public_snapshot(candidate)
    if snapshot.session_id != expected_session_id:
        raise PublicBoundaryError("public session identity changed")
    suspicious = tuple(
        field
        for field in snapshot.ignored_fields
        if any(token in field.lower() for token in ("hidden", "private", "secret", "internal"))
    )
    if suspicious:
        raise PublicBoundaryError("public response contained hidden/private field material")
    return snapshot


def structural_target_for_choice(snapshot: PublicSnapshot, choice_id: int) -> tuple[str, str] | None:
    """Return a directly mapped public target/path, or fail closed."""

    if classify_structural_context(snapshot) not in {"ENERGY", "MAIN"}:
        return None
    selected = next((choice for choice in snapshot.choices if choice.choice == choice_id), None)
    if selected is None:
        return None
    return STRUCTURAL_TARGETS.get(selected.action.strip())


@dataclass
class SessionResult:
    session_index: int
    policy_code: str
    policy_name: str
    status: str = "NOT_STARTED"
    session_id: str | None = None
    natural_terminal: bool = False
    survival_months: int | None = None
    successful_actions: int = 0
    unsupported_decisions: int = 0
    invalid_calls: int = 0
    repeated_action_count: int = 0
    longest_repeated_structural_path: int = 0
    repeated_investment_after_no_progress: int = 0
    comparable_checkpoints: int = 0
    advancing: int = 0
    no_progress: int = 0
    stall_signals: int = 0
    bounded_responses_after_stall: int = 0
    structural_switch_count: int = 0
    public_warning_count: int = 0
    promotion_months: list[int] = field(default_factory=list)
    final_public_level: str | None = None
    final_public_status: dict[str, Any] = field(default_factory=dict)
    ending_score: dict[str, Any] | None = None
    public_tool_names: list[str] = field(default_factory=list)
    public_seed_control: str = "UNKNOWN"
    observe_count: int = 0
    new_game_count: int = 0
    take_action_count: int = 0
    initialize_count: int = 0
    list_tools_count: int = 0
    direct_server_starts: int = 0
    shutdown_count: int = 0
    risk_override_exercised: bool = False
    error_code: str | None = None
    stop_batch: bool = False
    local_evidence: dict[str, Any] = field(default_factory=dict)
    trace: list[dict[str, Any]] = field(default_factory=list)

    def compact_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data.pop("trace", None)
        return data

    def local_dict(self) -> dict[str, Any]:
        data = self.compact_dict()
        data["trace"] = self.trace
        return data


def _policy_for(code: str) -> Any:
    return {
        "P0": MinIdControl,
        "P1": SimplePublicGrowthPrior,
        "P2": StallAwarePublicGrowth,
    }[code]()


def _session_id_from_new_game(payload: Mapping[str, Any]) -> str:
    session_id = payload.get("session_id")
    if not isinstance(session_id, str) or not session_id:
        raise ProtocolError("new_game did not return a public session_id")
    return session_id


def _record_public_snapshot(result: SessionResult, snapshot: PublicSnapshot) -> None:
    if snapshot.public_feed.strip():
        result.public_warning_count += 1


async def run_one_session(
    client: PublicToolClient,
    *,
    policy_code: str,
    session_index: int,
    action_ceiling: int = ACTION_CEILING,
) -> SessionResult:
    policy = _policy_for(policy_code)
    result = SessionResult(session_index, policy_code, policy.name)
    probe = MechanicalProbe(policy)
    previous_snapshot: PublicSnapshot | None = None
    previous_level: str | None = None
    pending_no_progress_choice: int | None = None

    try:
        result.initialize_count += 1
        await client.initialize()
        result.list_tools_count += 1
        tool_names, seed_found = validate_public_tools(await client.list_tools())
        result.public_tool_names = tool_names
        result.public_seed_control = "FOUND" if seed_found else "NO_PUBLIC_SEED_CONTROL_FOUND"

        result.observe_count = 0
        result.new_game_count += 1
        payload = await client.call_tool("new_game", {})
        result.session_id = _session_id_from_new_game(payload)

        result.observe_count += 1
        observed_payload = await client.call_tool("observe", {"session_id": result.session_id})
        snapshot = project_session_snapshot(observed_payload, result.session_id)
        _record_public_snapshot(result, snapshot)
        previous_level = snapshot.status.get("level") if isinstance(snapshot.status.get("level"), str) else None

        while snapshot.terminal is not True:
            decision: ActionDecision = probe.choose(snapshot)
            if decision.status != "ACTION":
                result.unsupported_decisions += 1
                result.status = "POLICY_MECHANICALLY_INVALID_OR_INCOMPLETE"
                result.error_code = decision.status
                break
            legal_ids = {item.choice for item in snapshot.choices}
            if decision.choice not in legal_ids:
                result.invalid_calls += 1
                result.status = "PROTOCOL_FAILURE"
                result.error_code = "POLICY_RETURNED_NONLEGAL_CHOICE"
                result.stop_batch = True
                break
            if result.successful_actions >= action_ceiling:
                result.status = "ACTION_CEILING"
                result.error_code = "ACTION_CEILING_REACHED"
                result.stop_batch = True
                break

            if pending_no_progress_choice == decision.choice:
                result.repeated_investment_after_no_progress += 1
            result.take_action_count += 1
            try:
                receipt = await client.call_tool(
                    "take_action",
                    {
                        "session_id": result.session_id,
                        "choice": decision.choice,
                        "notes": "S07-07 public mechanical probe",
                    },
                )
            except ExplicitToolError:
                result.invalid_calls += 1
                result.status = "PROTOCOL_FAILURE"
                result.error_code = "EXPLICIT_TAKE_ACTION_ERROR"
                result.stop_batch = True
                break
            if receipt.get("success") is not True:
                result.invalid_calls += 1
                result.status = "PROTOCOL_FAILURE"
                result.error_code = "EXPLICIT_TAKE_ACTION_REJECTION"
                result.stop_batch = True
                break

            result.successful_actions += 1
            probe.record_action_receipt(True)
            result.observe_count += 1
            observed_payload = await client.call_tool("observe", {"session_id": result.session_id})
            fresh = project_session_snapshot(observed_payload, result.session_id)
            _record_public_snapshot(result, fresh)

            current_level = fresh.status.get("level") if isinstance(fresh.status.get("level"), str) else None
            promotion_label = current_level if previous_level and current_level and current_level != previous_level else None
            target_path = structural_target_for_choice(snapshot, decision.choice)
            checkpoint = None
            if target_path is not None:
                target, path = target_path
                checkpoint = probe.record_checkpoint(
                    fresh,
                    target=target,
                    path=path,
                    promotion_label=promotion_label,
                )
                result.longest_repeated_structural_path = max(
                    result.longest_repeated_structural_path,
                    checkpoint.repeated_action_count,
                )
                if checkpoint.comparable:
                    result.comparable_checkpoints += 1
                    if checkpoint.progress == "ADVANCING":
                        result.advancing += 1
                        pending_no_progress_choice = None
                    elif checkpoint.progress == "NO_PROGRESS":
                        result.no_progress += 1
                        pending_no_progress_choice = decision.choice
                    if checkpoint.is_stalled:
                        result.stall_signals += 1
            if decision.structural_switch:
                result.bounded_responses_after_stall += 1

            if promotion_label:
                result.promotion_months.append(fresh.time.current_month or 0)
            result.trace.append(
                {
                    "month": fresh.time.current_month,
                    "quarter": fresh.time.current_quarter,
                    "context": classify_structural_context(snapshot),
                    "choice": decision.choice,
                    "action": next(
                        (item.action for item in snapshot.choices if item.choice == decision.choice),
                        "",
                    ),
                    "checkpoint": checkpoint.to_dict() if checkpoint else None,
                    "terminal": fresh.terminal,
                }
            )
            previous_snapshot = snapshot
            snapshot = fresh
            previous_level = current_level

        result.repeated_action_count = probe.report().repeated_action_count
        result.structural_switch_count = probe.report().to_dict()["structural_switch_count"]
        result.natural_terminal = snapshot.terminal is True
        result.survival_months = snapshot.time.current_month
        result.final_public_level = snapshot.status.get("level") if isinstance(snapshot.status.get("level"), str) else None
        result.final_public_status = dict(snapshot.status)
        if result.status == "NOT_STARTED":
            result.status = "COMPLETED" if result.natural_terminal else "INCOMPLETE"
        if isinstance(observed_payload.get("ending_score"), Mapping):
            result.ending_score = _public_score(observed_payload.get("ending_score"))
        return result
    except PublicBoundaryError:
        result.status = "PUBLIC_INTERFACE_BOUNDARY_REVIEW_REQUIRED"
        result.error_code = "PUBLIC_BOUNDARY"
        result.stop_batch = True
        return result
    except (UnknownSideEffectError, TimeoutError, ConnectionError, BrokenPipeError, OSError):
        result.status = "UNKNOWN_SIDE_EFFECT"
        result.error_code = "TRANSPORT_OR_TIMEOUT"
        result.stop_batch = True
        return result
    except (ProtocolError, ExplicitToolError):
        result.status = "PROTOCOL_FAILURE"
        result.error_code = "PUBLIC_PROTOCOL"
        result.stop_batch = True
        return result


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _write_local_evidence(result: SessionResult, session_dir: Path, stderr: str) -> None:
    session_dir.mkdir(parents=True, exist_ok=True)
    report_path = session_dir / "session_summary.json"
    report_path.write_text(json.dumps(result.local_dict(), ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
    stderr_path = session_dir / "server-stderr.log"
    stderr_path.write_text(stderr, encoding="utf-8")
    result.local_evidence = {
        "session_summary": {"path": str(report_path), "bytes": report_path.stat().st_size, "sha256": _sha256(report_path)},
        "server_stderr": {"path": str(stderr_path), "bytes": stderr_path.stat().st_size, "sha256": _sha256(stderr_path)},
    }


def _unexpected_runtime_text(stderr: str) -> bool:
    lowered = stderr.lower()
    return any(token in lowered for token in ("deepseek", "agentserver", "jiuwenswarm", "prewarm", "provider"))


def _planned_slots(p2_live_evaluable: bool) -> list[str]:
    order = ["P0", "P1", "P2", "P1", "P2", "P0", "P2", "P0", "P1"]
    return [code for code in order if p2_live_evaluable or code != "P2"]


def _totals(results: Sequence[SessionResult]) -> dict[str, int]:
    keys = (
        "direct_server_starts",
        "initialize_count",
        "list_tools_count",
        "new_game_count",
        "observe_count",
        "take_action_count",
        "successful_actions",
        "shutdown_count",
    )
    return {key: sum(getattr(result, key) for result in results) for key in keys}


async def run_live_batch(runtime_root: Path = DEFAULT_RUNTIME_ROOT, evidence_path: Path = DEFAULT_EVIDENCE_PATH) -> dict[str, Any]:
    if not MCP_EXECUTABLE.is_file():
        raise FileNotFoundError(f"MCP executable missing: {MCP_EXECUTABLE}")
    runtime_root.mkdir(parents=True, exist_ok=False)

    p2_live_evaluable = bool(STRUCTURAL_TARGETS)
    planned = _planned_slots(p2_live_evaluable)
    results: list[SessionResult] = []
    stop_reason: str | None = None

    for index, policy_code in enumerate(planned, start=1):
        session_dir = runtime_root / f"{index:02d}-{policy_code.lower()}"
        session_dir.mkdir(parents=True, exist_ok=False)
        stderr_buffer = io.StringIO()
        result = SessionResult(index, policy_code, _policy_for(policy_code).name, direct_server_starts=1)
        server_started = False
        try:
            env = {
                "CAREER_EMULATOR_DB": str(session_dir / "probe.sqlite3"),
                "CAREER_EMULATOR_LOG_DIR": str(session_dir / "logs"),
                "CAREER_EMULATOR_DATASET": "dev",
                "CAREER_EMULATOR_DATASET_SOURCE": "distribution",
                "CAREER_EMULATOR_MAX_SESSIONS": "1",
            }
            params = StdioServerParameters(
                command=str(MCP_EXECUTABLE),
                args=["--update", "skip"],
                env=env,
                cwd=str(MCP_EXECUTABLE.parent),
            )
            async with stdio_client(params, errlog=stderr_buffer) as (read_stream, write_stream):
                server_started = True
                async with ClientSession(read_stream, write_stream) as session:
                    result = await run_one_session(
                        MCPClientAdapter(session),
                        policy_code=policy_code,
                        session_index=index,
                    )
                result.direct_server_starts = 1
        except (UnknownSideEffectError, TimeoutError, ConnectionError, BrokenPipeError, OSError):
            result.status = "UNKNOWN_SIDE_EFFECT"
            result.error_code = "SERVER_START_OR_TRANSPORT"
            result.stop_batch = True
        except Exception:
            result.status = "PROTOCOL_FAILURE"
            result.error_code = "HARNESS_EXCEPTION"
            result.stop_batch = True
        finally:
            result.shutdown_count = int(server_started)
            stderr = stderr_buffer.getvalue()
            if _unexpected_runtime_text(stderr):
                result.status = "UNEXPECTED_AGENT_OR_PROVIDER_DEPENDENCY"
                result.error_code = "AGENT_OR_PROVIDER_TEXT_IN_SERVER_STDERR"
                result.stop_batch = True
            _write_local_evidence(result, session_dir, stderr)
            results.append(result)

        print(
            f"session {index}/{len(planned)} {policy_code}: {result.status}; "
            f"actions={result.successful_actions}; month={result.survival_months}",
            flush=True,
        )

        if index == 1 and result.status != "COMPLETED":
            stop_reason = "MECHANICAL_PROBE_BATCH_STOPPED_AT_GATE_A"
            break
        if result.stop_batch:
            stop_reason = "MECHANICAL_PROBE_BATCH_STOPPED_ON_RUNTIME_BOUNDARY"
            break

    evidence_path.parent.mkdir(parents=True, exist_ok=True)
    batch = {
        "task": "S07-07",
        "base": "0a61130736408f56a98e4f3af71dd32c4e1cba80",
        "candidate": "candidate-v6c-compliance-cleanup",
        "p2_live_evaluable": p2_live_evaluable,
        "planned_order": planned,
        "executed_order": [result.policy_code for result in results],
        "sessions": [result.compact_dict() for result in results],
        "totals": _totals(results),
        "provider_calls": 0,
        "agentserver_starts": 0,
        "runner_play": 0,
        "skill_installs_or_reloads": 0,
        "stop_reason": stop_reason,
        "decision": (
            "MECHANICAL_PROBE_BATCH_COMPLETE"
            if len(results) == len(planned) and all(item.status == "COMPLETED" for item in results)
            else stop_reason or "MECHANICAL_PROBE_BATCH_STOPPED_ON_RUNTIME_BOUNDARY"
        ),
    }
    evidence_path.write_text(json.dumps(batch, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
    return batch


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the authorized S07-07 public mechanical batch.")
    parser.add_argument("--live", action="store_true", help="Explicitly authorize this task's direct-MCP live path.")
    parser.add_argument("--runtime-root", type=Path, default=DEFAULT_RUNTIME_ROOT)
    parser.add_argument("--evidence-path", type=Path, default=DEFAULT_EVIDENCE_PATH)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if not args.live:
        print("No live operation: pass --live explicitly for the authorized S07-07 batch.")
        return 2
    import anyio

    anyio.run(run_live_batch, args.runtime_root, args.evidence_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
