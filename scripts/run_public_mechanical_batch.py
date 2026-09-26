"""Bounded direct-public-MCP batch runner for S07 mechanical-probe tasks.

The live path is opt-in through ``--live`` and is intentionally serialized.
Importing this module, running its tests, or calling the offline helpers never
starts a process or calls MCP. Only participant-visible projected fields enter
the controller and compact reports.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections.abc import Mapping, Sequence
from dataclasses import asdict, dataclass, field, replace
from pathlib import Path
from typing import Any, Protocol

from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client

try:
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
except ModuleNotFoundError:  # Direct ``python scripts/run_public_mechanical_batch.py`` execution.
    from public_mechanical_probe import (  # type: ignore[no-redef]
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
S07_07_BASE_SHA = "0a61130736408f56a98e4f3af71dd32c4e1cba80"

# Only direct, public action-label semantics are mapped. Multi-target or
# hidden-risk actions remain unmapped so the tracker cannot invent causality.
STRUCTURAL_TARGETS: dict[str, tuple[str, str]] = {
    "人脉维护": ("network", "energy:network"),
    "健康恢复": ("health", "energy:health"),
    "心理修复": ("dignity", "energy:dignity"),
    "准备汇报材料": ("output", "energy:output"),
}
REJECTION_COMPARE_STATUS = frozenset(
    {"level", "health", "dignity", "skill", "network", "output", "wealth", "energy", "duration_in_level"}
)


class PublicBatchError(RuntimeError):
    """Base class for bounded public-interface failures."""


class ExplicitToolError(PublicBatchError):
    """The server returned an explicit MCP/tool error, not an unknown outcome."""

    def __init__(self, receipt: Mapping[str, Any] | None = None) -> None:
        super().__init__("server returned an explicit MCP tool error")
        self.receipt = bounded_rejection_receipt(receipt)


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


def bounded_rejection_receipt(value: Mapping[str, Any] | None) -> dict[str, Any]:
    """Keep only small participant-visible scalar error fields, never raw MCP content."""

    allowed = ("success", "error", "message", "reason", "status", "code", "error_code")
    receipt: dict[str, Any] = {}
    if isinstance(value, Mapping):
        for key in allowed:
            item = value.get(key)
            if isinstance(item, bool) or (isinstance(item, (int, float)) and not isinstance(item, bool)):
                receipt[key] = item
            elif isinstance(item, str):
                one_line = " ".join(item.split())
                if len(one_line) <= 160 and not any(
                    token in one_line.lower() for token in ("api_key", "bearer ", "password", "secret")
                ):
                    receipt[key] = one_line
    if not any(key in receipt for key in ("error", "message", "reason", "status", "code", "error_code")):
        receipt["reason_status"] = "EXPLICIT_REJECTION_NO_PUBLIC_REASON"
    return receipt


def _result_mapping(result: Any) -> Mapping[str, Any] | None:
    structured = getattr(result, "structuredContent", None)
    if isinstance(structured, Mapping):
        return _unwrap_mapping(structured)
    content = getattr(result, "content", None)
    if isinstance(content, Sequence):
        for block in content:
            if getattr(block, "type", None) != "text":
                continue
            body = getattr(block, "text", None)
            if not isinstance(body, str):
                continue
            try:
                decoded = json.loads(body)
            except json.JSONDecodeError:
                continue
            if isinstance(decoded, Mapping):
                return _unwrap_mapping(decoded)
    return None


def decode_mcp_result(result: Any) -> Mapping[str, Any]:
    """Decode one already-received MCP result without logging raw content."""

    decoded = _result_mapping(result)
    if bool(getattr(result, "isError", False)):
        raise ExplicitToolError(decoded)
    if decoded is not None:
        return decoded
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


def compare_rejection_observes(
    before: PublicSnapshot, after: PublicSnapshot, expected_session_id: str
) -> tuple[str, dict[str, Any]]:
    """Use only complete public core fields; text/choice drift is not mutation proof."""

    if before.session_id != expected_session_id or after.session_id != expected_session_id:
        return "REJECTION_STATE_UNCERTAIN", {}
    if any(
        value is None
        for snap in (before, after)
        for value in (snap.time.current_month, snap.time.current_quarter, snap.time.current_year, snap.alive, snap.failed)
    ):
        return "REJECTION_STATE_UNCERTAIN", {}
    if any(
        key not in snap.status or snap.status[key] is None
        for snap in (before, after)
        for key in REJECTION_COMPARE_STATUS
    ):
        return "REJECTION_STATE_UNCERTAIN", {}

    delta: dict[str, Any] = {}
    for key in ("current_month", "current_quarter", "current_year"):
        old, new = getattr(before.time, key), getattr(after.time, key)
        if old != new:
            delta[key] = {"before": old, "after": new}
    for key in sorted(REJECTION_COMPARE_STATUS):
        old, new = before.status[key], after.status[key]
        if old != new:
            delta[key] = {"before": old, "after": new}
    for key in ("alive", "failed"):
        old, new = getattr(before, key), getattr(after, key)
        if old != new:
            delta[key] = {"before": old, "after": new}
    if delta:
        return "EXPLICIT_REJECTION_WITH_PUBLIC_STATE_CHANGE", delta
    if before.event != after.event or before.public_feed != after.public_feed or set(before.choices) != set(after.choices):
        return "REJECTION_STATE_UNCERTAIN", {}
    return "EXPLICIT_REJECTION_CONFIRMED_NO_MUTATION", {}


def _public_decision_state_key(snapshot: PublicSnapshot) -> tuple[Any, ...]:
    """Key temporary rejections to the current projected public decision state."""

    return (
        snapshot.session_id,
        snapshot.time.current_month,
        snapshot.time.current_quarter,
        snapshot.time.current_year,
        tuple(sorted(snapshot.status.items())),
        snapshot.alive,
        snapshot.failed,
        snapshot.event.title,
        snapshot.event.description,
        tuple(sorted((item.choice, item.action, item.description) for item in snapshot.choices)),
    )


def is_public_affordability_rejection(receipt: Mapping[str, Any]) -> bool:
    """Recognize only an explicit, narrowly phrased public resource-insufficiency receipt."""

    import re

    texts = [receipt.get(key) for key in ("error", "message", "reason")]
    for text in texts:
        if not isinstance(text, str):
            continue
        normalized = " ".join(text.lower().split())
        if re.fullmatch(r"insufficient (?:energy|resource) for .+: \d+(?:\.\d+)? remaining", normalized):
            return True
    return False


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
    explicit_rejections: int = 0
    recovered_rejections: int = 0
    rejected_choice_ids: list[int] = field(default_factory=list)
    rejection_events: list[dict[str, Any]] = field(default_factory=list)
    rejection_receipt: dict[str, Any] | None = None
    rejection_recovery: str | None = None
    rejection_public_delta: dict[str, Any] = field(default_factory=dict)
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
    server_start_attempted: int = 0
    transport_entered: int = 0
    child_spawn_confirmed: bool | None = None
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
    code = code[:-1] if code.endswith("R") else code
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
    result: SessionResult | None = None,
    task_id: str = "S07-07",
) -> SessionResult:
    recovery_enabled = policy_code in {"P1R", "P2R"}
    base_policy_code = policy_code[:-1] if recovery_enabled else policy_code
    policy = _policy_for(base_policy_code)
    if result is None:
        name = f"{policy.name}+PUBLIC_AFFORDABILITY_RECOVERY" if recovery_enabled else policy.name
        result = SessionResult(session_index, policy_code, name)
    probe = MechanicalProbe(policy)
    previous_snapshot: PublicSnapshot | None = None
    previous_level: str | None = None
    pending_no_progress_choice: int | None = None
    rejected_for_state: set[int] = set()
    successful_for_state: set[int] = set()
    current_decision_state: tuple[Any, ...] | None = None

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
            state_key = _public_decision_state_key(snapshot)
            if current_decision_state != state_key:
                rejected_for_state.clear()
                successful_for_state.clear()
                current_decision_state = state_key
            policy_snapshot = (
                replace(
                    snapshot,
                    choices=tuple(
                        choice for choice in snapshot.choices
                        if choice.choice not in rejected_for_state | successful_for_state
                    ),
                )
                if recovery_enabled and (rejected_for_state or successful_for_state)
                else snapshot
            )
            if recovery_enabled and (rejected_for_state or successful_for_state) and not policy_snapshot.choices:
                all_ids = {item.choice for item in snapshot.choices}
                if all_ids and all_ids.issubset(rejected_for_state):
                    result.status = "POLICY_NO_AFFORDABLE_PUBLIC_ACTION"
                    result.error_code = "ALL_CURRENT_PUBLIC_CHOICES_EXPLICITLY_REJECTED"
                else:
                    result.status = "POLICY_DECISION_STATE_EXHAUSTED"
                    result.error_code = "PUBLIC_CHOICES_ALREADY_ATTEMPTED_IN_UNCHANGED_STATE"
                break
            decision: ActionDecision = probe.choose(policy_snapshot)
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
            if result.take_action_count >= action_ceiling:
                result.status = "ACTION_CEILING"
                result.error_code = "ACTION_CEILING_REACHED"
                result.stop_batch = True
                break

            if pending_no_progress_choice == decision.choice:
                result.repeated_investment_after_no_progress += 1
            result.take_action_count += 1
            rejection: Mapping[str, Any] | None = None
            try:
                receipt = await client.call_tool(
                    "take_action",
                    {
                        "session_id": result.session_id,
                        "choice": decision.choice,
                        "notes": f"{task_id} public mechanical probe",
                    },
                )
            except ExplicitToolError as exc:
                rejection = exc.receipt
            else:
                if receipt.get("success") is not True:
                    rejection = bounded_rejection_receipt(receipt)
            if rejection is not None:
                result.invalid_calls += 1
                result.explicit_rejections += 1
                result.rejection_receipt = dict(rejection)
                result.observe_count += 1
                try:
                    recovery_payload = await client.call_tool("observe", {"session_id": result.session_id})
                    state_payload = recovery_payload.get("current_state")
                    observed_id = (
                        state_payload.get("session_id")
                        if isinstance(state_payload, Mapping) and state_payload.get("session_id")
                        else recovery_payload.get("session_id")
                    )
                    if observed_id is not None and observed_id != result.session_id:
                        result.status = "UNKNOWN_SIDE_EFFECT"
                        result.error_code = "REJECTION_STATE_UNCERTAIN"
                        result.rejection_recovery = "REJECTION_STATE_UNCERTAIN"
                        result.stop_batch = True
                        break
                    recovery = project_session_snapshot(recovery_payload, result.session_id)
                except PublicBoundaryError:
                    result.status = "PUBLIC_INTERFACE_BOUNDARY_REVIEW_REQUIRED"
                    result.error_code = "REJECTION_RECOVERY_PUBLIC_BOUNDARY"
                    result.stop_batch = True
                    break
                except (UnknownSideEffectError, ExplicitToolError, ProtocolError, TimeoutError, ConnectionError, BrokenPipeError, OSError):
                    result.status = "UNKNOWN_SIDE_EFFECT"
                    result.error_code = "REJECTION_RECOVERY_OBSERVE_UNKNOWN"
                    result.stop_batch = True
                    break
                comparison, delta = compare_rejection_observes(snapshot, recovery, result.session_id)
                result.rejection_recovery = comparison
                result.rejection_public_delta = delta
                if comparison == "EXPLICIT_REJECTION_CONFIRMED_NO_MUTATION":
                    if recovery_enabled and is_public_affordability_rejection(rejection):
                        result.recovered_rejections += 1
                        result.rejected_choice_ids.append(decision.choice)
                        rejected_for_state.add(decision.choice)
                        result.rejection_recovery = "PUBLIC_AFFORDABILITY_REJECTION_CONFIRMED"
                        result.rejection_events.append(
                            {
                                "choice": decision.choice,
                                "classification": result.rejection_recovery,
                                "receipt": dict(rejection),
                                "public_delta": {},
                            }
                        )
                        if len(rejected_for_state | successful_for_state) >= len({item.choice for item in snapshot.choices}):
                            if len(rejected_for_state) == len({item.choice for item in snapshot.choices}):
                                result.status = "POLICY_NO_AFFORDABLE_PUBLIC_ACTION"
                                result.error_code = "ALL_CURRENT_PUBLIC_CHOICES_EXPLICITLY_REJECTED"
                            else:
                                result.status = "POLICY_DECISION_STATE_EXHAUSTED"
                                result.error_code = "PUBLIC_CHOICES_ALREADY_ATTEMPTED_IN_UNCHANGED_STATE"
                        else:
                            snapshot = recovery
                            observed_payload = recovery_payload
                            continue
                    else:
                        result.status = "POLICY_ACTION_REJECTED"
                        if recovery_enabled:
                            result.rejection_recovery = "EXPLICIT_REJECTION_NON_AFFORDABILITY"
                            result.rejection_events.append(
                                {
                                    "choice": decision.choice,
                                    "classification": result.rejection_recovery,
                                    "receipt": dict(rejection),
                                    "public_delta": {},
                                }
                            )
                elif comparison == "EXPLICIT_REJECTION_WITH_PUBLIC_STATE_CHANGE":
                    result.status = "EXPLICIT_REJECTION_STATE_CHANGED"
                else:
                    result.status = "UNKNOWN_SIDE_EFFECT"
                    result.error_code = "REJECTION_STATE_UNCERTAIN"
                    result.stop_batch = True
                snapshot = recovery
                observed_payload = recovery_payload
                break

            result.successful_actions += 1
            probe.record_action_receipt(True)
            result.observe_count += 1
            observed_payload = await client.call_tool("observe", {"session_id": result.session_id})
            fresh = project_session_snapshot(observed_payload, result.session_id)
            _record_public_snapshot(result, fresh)
            if _public_decision_state_key(fresh) != current_decision_state:
                rejected_for_state.clear()
                successful_for_state.clear()
                current_decision_state = _public_decision_state_key(fresh)
            elif recovery_enabled:
                successful_for_state.add(decision.choice)

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


def _write_local_evidence(result: SessionResult, session_dir: Path, stderr_path: Path) -> None:
    session_dir.mkdir(parents=True, exist_ok=True)
    report_path = session_dir / "session_summary.json"
    report_path.write_text(json.dumps(result.local_dict(), ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
    result.local_evidence = {
        "session_summary": {"path": str(report_path), "bytes": report_path.stat().st_size, "sha256": _sha256(report_path)},
        "server_stderr": (
            {"path": str(stderr_path), "bytes": stderr_path.stat().st_size, "sha256": _sha256(stderr_path)}
            if stderr_path.exists()
            else {"path": str(stderr_path), "status": "UNAVAILABLE_PRESPAWN"}
        ),
    }


def _unexpected_runtime_text(stderr: str) -> bool:
    for line in stderr.splitlines():
        lowered = line.lower().replace("\\", "/")
        # A FastMCP import warning names its auth/providers module; this is
        # not evidence that an AgentServer or model provider was invoked.
        if "fastmcp/server/auth/providers/jwt.py:" in lowered and "authlibdeprecationwarning" in lowered:
            continue
        if any(token in lowered for token in ("deepseek", "agentserver", "jiuwenswarm", "prewarm", "provider")):
            return True
    return False


def _planned_slots(p2_live_evaluable: bool) -> list[str]:
    order = ["P0", "P1", "P2", "P1", "P2", "P0", "P2", "P0", "P1"]
    return [code for code in order if p2_live_evaluable or code != "P2"]


def _totals(results: Sequence[SessionResult]) -> dict[str, int]:
    keys = (
        "server_start_attempted",
        "transport_entered",
        "direct_server_starts",
        "initialize_count",
        "list_tools_count",
        "new_game_count",
        "observe_count",
        "take_action_count",
        "successful_actions",
        "explicit_rejections",
        "recovered_rejections",
        "shutdown_count",
    )
    return {key: sum(getattr(result, key) for result in results) for key in keys}


async def run_live_batch(
    runtime_root: Path = DEFAULT_RUNTIME_ROOT,
    evidence_path: Path = DEFAULT_EVIDENCE_PATH,
    *,
    policy_order: Sequence[str] | None = None,
    task_id: str = "S07-07",
    base_sha: str = S07_07_BASE_SHA,
) -> dict[str, Any]:
    if policy_order is None:
        planned = _planned_slots(bool(STRUCTURAL_TARGETS))
    else:
        planned = list(policy_order)
        if not planned or len(planned) > 6 or any(code not in {"P1", "P2", "P1R", "P2R"} for code in planned):
            raise ValueError("explicit policy_order must contain 1-6 P1/P2/P1R/P2R sessions")
    if not task_id or not base_sha:
        raise ValueError("task_id and base_sha must be non-empty")
    if not MCP_EXECUTABLE.is_file():
        raise FileNotFoundError(f"MCP executable missing: {MCP_EXECUTABLE}")
    runtime_root.mkdir(parents=True, exist_ok=False)

    p2_live_evaluable = bool(STRUCTURAL_TARGETS)
    results: list[SessionResult] = []
    stop_reason: str | None = None

    for index, policy_code in enumerate(planned, start=1):
        session_dir = runtime_root / f"{index:02d}-{policy_code.lower()}"
        session_dir.mkdir(parents=True, exist_ok=False)
        stderr_path = session_dir / "server-stderr.log"
        base_policy = policy_code[:-1] if policy_code.endswith("R") else policy_code
        policy_name = _policy_for(base_policy).name
        if policy_code.endswith("R"):
            policy_name += "+PUBLIC_AFFORDABILITY_RECOVERY"
        result = SessionResult(index, policy_code, policy_name)
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
            # Validate the local OS handle before touching the SDK transport.
            # StringIO.fileno() is an OSError and used to be misreported as a
            # live/unknown server start despite failing before child creation.
            with stderr_path.open("w", encoding="utf-8") as stderr_file:
                stderr_file.fileno()
                result.server_start_attempted = 1
                async with stdio_client(params, errlog=stderr_file) as (read_stream, write_stream):
                    result.transport_entered = 1
                    result.child_spawn_confirmed = True  # SDK yields only after process creation.
                    result.direct_server_starts = 1
                    async with ClientSession(read_stream, write_stream) as session:
                        await run_one_session(
                            MCPClientAdapter(session),
                            policy_code=policy_code,
                            session_index=index,
                            result=result,
                            task_id=task_id,
                        )
                result.shutdown_count = 1  # stdio_client exit completed.
        except Exception:
            if result.server_start_attempted:
                result.status = "UNKNOWN_SIDE_EFFECT"
                result.error_code = "LIVE_SERVER_START_OR_TRANSPORT_UNKNOWN"
            else:
                result.status = "TOOLING_OR_PRESPAWN_ERROR"
                result.error_code = "PRESPAWN_LOCAL_FAILURE"
                result.child_spawn_confirmed = False
            result.stop_batch = True
        finally:
            stderr = stderr_path.read_text(encoding="utf-8", errors="replace") if stderr_path.exists() else ""
            if _unexpected_runtime_text(stderr):
                result.status = "UNEXPECTED_AGENT_OR_PROVIDER_DEPENDENCY"
                result.error_code = "AGENT_OR_PROVIDER_TEXT_IN_SERVER_STDERR"
                result.stop_batch = True
            _write_local_evidence(result, session_dir, stderr_path)
            results.append(result)

        print(
            f"session {index}/{len(planned)} {policy_code}: {result.status}; "
            f"actions={result.successful_actions}; month={result.survival_months}",
            flush=True,
        )

        if task_id == "S07-07" and index == 1 and result.status != "COMPLETED":
            stop_reason = "MECHANICAL_PROBE_BATCH_STOPPED_AT_GATE_A"
            break
        if result.stop_batch:
            stop_reason = "MECHANICAL_PROBE_BATCH_STOPPED_ON_RUNTIME_BOUNDARY"
            break

    evidence_path.parent.mkdir(parents=True, exist_ok=True)
    batch = {
        "task": task_id,
        "base": base_sha,
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
            "MECHANICAL_PROBE_BATCH_EXECUTION_COMPLETE"
            if len(results) == len(planned) and all(
                item.status in {"COMPLETED", "POLICY_ACTION_REJECTED", "EXPLICIT_REJECTION_STATE_CHANGED", "POLICY_NO_AFFORDABLE_PUBLIC_ACTION", "POLICY_DECISION_STATE_EXHAUSTED", "POLICY_MECHANICALLY_INVALID_OR_INCOMPLETE"}
                for item in results
            )
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
