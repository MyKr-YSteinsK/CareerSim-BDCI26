"""Thin interactive transport for the S07-15 Codex-as-Player discovery runs.

NO_POLICY_LOGIC: this module never selects an action. A choice is sent only
after an explicit player input line naming a currently legal integer choice.
The MCP child is direct career-emulator-mcp; this does not start AgentServer.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PUBLIC_STATUS_FIELDS = {
    "level",
    "health",
    "dignity",
    "skill",
    "network",
    "output",
    "wealth",
    "energy",
    "duration_in_level",
}
PUBLIC_TOP_FIELDS = {
    "session_id",
    "current_state",
    "current_event",
    "choices",
    "events",
    "ending_score",
    "terminal",
    "game_over",
}
PUBLIC_STATE_FIELDS = {"session_id", "time", "status", "simulation_flags"}
PUBLIC_TIME_FIELDS = {"current_month", "current_quarter", "current_year"}
PUBLIC_FLAG_FIELDS = {"alive", "failed", "terminal", "game_over"}
PUBLIC_EVENT_FIELDS = {"title", "description"}
PUBLIC_CHOICE_FIELDS = {"choice", "action", "description"}
PUBLIC_RECEIPT_FIELDS = {"success", "status", "reason", "message", "result", "feedback", "description"}
PUBLIC_SCORE_DIMENSIONS = {
    "level",
    "wealth",
    "resilience",
    "skill",
    "risk",
    "risk_control",
    "network",
    "output",
}
PUBLIC_SCORE_COMPONENTS = {"raw", "raw_value", "score", "weighted", "weighted_score", "points"}


@dataclass(frozen=True)
class PlayerInput:
    choice: int
    rationale: str


def parse_player_input(
    line: str,
    legal_choice_ids: Sequence[int],
    blocked_choice_ids: Sequence[int] = (),
) -> PlayerInput:
    """Parse explicit '<integer> | <one-sentence rationale>' player input."""

    if "|" not in line:
        raise ValueError("input must be '<legal integer> | <one-sentence rationale>'")
    choice_text, rationale = line.split("|", maxsplit=1)
    choice_text = choice_text.strip()
    rationale = rationale.strip()
    try:
        choice = int(choice_text)
    except ValueError as exc:
        raise ValueError("choice must be one integer") from exc
    if choice not in legal_choice_ids:
        raise ValueError("choice is not in the latest public legal-choice list")
    if choice in blocked_choice_ids:
        raise ValueError("this choice was just explicitly rejected in an unchanged public state")
    if not rationale or len(rationale) > 500:
        raise ValueError("provide one brief rationale (1-500 characters)")
    return PlayerInput(choice, rationale)


def _scalar(value: Any) -> bool:
    return value is None or isinstance(value, (str, bool, int, float))


def _project_public_score_dimensions(value: Any, ignored: set[str]) -> dict[str, Any]:
    """Retain only recognized public ending dimensions and numeric score components."""

    if not isinstance(value, Mapping):
        ignored.add("ending_score.dimensions")
        return {}

    dimensions: dict[str, Any] = {}
    for name, detail in value.items():
        normalized_name = str(name).strip().lower().replace(" ", "_")
        prefix = f"ending_score.dimensions.{name}"
        if normalized_name not in PUBLIC_SCORE_DIMENSIONS:
            ignored.add(prefix)
            continue
        if isinstance(detail, (int, float)) and not isinstance(detail, bool):
            dimensions[str(name)] = detail
            continue
        if isinstance(detail, Mapping):
            components = {}
            for component, score in detail.items():
                if (
                    str(component).lower() in PUBLIC_SCORE_COMPONENTS
                    and isinstance(score, (int, float))
                    and not isinstance(score, bool)
                ):
                    components[str(component)] = score
                else:
                    ignored.add(f"{prefix}.{component}")
            if components:
                dimensions[str(name)] = components
            else:
                ignored.add(prefix)
            continue
        ignored.add(prefix)
    return dimensions


def _unwrap_public_payload(value: Any) -> Mapping[str, Any]:
    current = value
    for key in ("result", "data", "observation"):
        if isinstance(current, Mapping) and not any(
            name in current for name in ("current_state", "current_event", "choices", "session_id")
        ):
            nested = current.get(key)
            if isinstance(nested, Mapping):
                current = nested
    return current if isinstance(current, Mapping) else {}


def project_public_snapshot(payload: Mapping[str, Any]) -> dict[str, Any]:
    """Keep a small participant-visible allowlist; unknown values are discarded."""

    raw = _unwrap_public_payload(payload)
    ignored = {str(key) for key in raw if key not in PUBLIC_TOP_FIELDS}
    state = raw.get("current_state")
    state = state if isinstance(state, Mapping) else {}
    ignored.update(f"current_state.{key}" for key in state if key not in PUBLIC_STATE_FIELDS)
    raw_time = state.get("time")
    raw_time = raw_time if isinstance(raw_time, Mapping) else {}
    ignored.update(f"current_state.time.{key}" for key in raw_time if key not in PUBLIC_TIME_FIELDS)
    time = {key: raw_time[key] for key in PUBLIC_TIME_FIELDS if _scalar(raw_time.get(key)) and key in raw_time}

    raw_status = state.get("status")
    raw_status = raw_status if isinstance(raw_status, Mapping) else {}
    status = {
        str(key): value
        for key, value in raw_status.items()
        if str(key) in PUBLIC_STATUS_FIELDS and _scalar(value)
    }
    ignored.update(f"current_state.status.{key}" for key in raw_status if key not in PUBLIC_STATUS_FIELDS)

    raw_flags = state.get("simulation_flags")
    raw_flags = raw_flags if isinstance(raw_flags, Mapping) else {}
    flags = {
        str(key): value
        for key, value in raw_flags.items()
        if str(key) in PUBLIC_FLAG_FIELDS and _scalar(value)
    }
    ignored.update(f"current_state.simulation_flags.{key}" for key in raw_flags if key not in PUBLIC_FLAG_FIELDS)

    raw_event = raw.get("current_event")
    raw_event = raw_event if isinstance(raw_event, Mapping) else {}
    event = {str(key): value[:4000] for key, value in raw_event.items() if key in PUBLIC_EVENT_FIELDS and isinstance(value, str)}
    ignored.update(f"current_event.{key}" for key in raw_event if key not in PUBLIC_EVENT_FIELDS)

    choices: list[dict[str, Any]] = []
    raw_choices = raw.get("choices", [])
    if isinstance(raw_choices, Sequence) and not isinstance(raw_choices, (str, bytes, bytearray)):
        for index, item in enumerate(raw_choices):
            if not isinstance(item, Mapping):
                ignored.add(f"choices[{index}]")
                continue
            ignored.update(f"choices[{index}].{key}" for key in item if key not in PUBLIC_CHOICE_FIELDS)
            choice_id = item.get("choice")
            if isinstance(choice_id, int) and not isinstance(choice_id, bool):
                choices.append(
                    {
                        "choice": choice_id,
                        "action": str(item.get("action", ""))[:1000],
                        "description": str(item.get("description", ""))[:2000],
                    }
                )
    elif "choices" in raw:
        ignored.add("choices")

    feed = raw.get("events")
    public_feed = feed[:4000] if isinstance(feed, str) else ""
    if "events" in raw and not isinstance(feed, str):
        ignored.add("events")

    ending_score: dict[str, Any] = {}
    raw_score = raw.get("ending_score")
    if isinstance(raw_score, Mapping):
        for key, value in raw_score.items():
            if key == "dimensions":
                dimensions = _project_public_score_dimensions(value, ignored)
                if dimensions:
                    ending_score["dimensions"] = dimensions
            elif _scalar(value):
                ending_score[str(key)] = value
            else:
                ignored.add(f"ending_score.{key}")
    elif "ending_score" in raw:
        ignored.add("ending_score")

    session_id = state.get("session_id") or raw.get("session_id")
    terminal_values = [raw.get("terminal"), raw.get("game_over"), flags.get("terminal"), flags.get("game_over")]
    terminal = next((value for value in terminal_values if isinstance(value, bool)), None)
    if terminal is None:
        if flags.get("alive") is False or flags.get("failed") is True:
            terminal = True
        elif flags.get("alive") is True and flags.get("failed") is False:
            terminal = False

    return {
        "session_id": session_id if isinstance(session_id, str) else None,
        "time": time,
        "status": status,
        "event": event,
        "choices": choices,
        "public_feed": public_feed,
        "public_flags": flags,
        "terminal": terminal,
        "ending_score": ending_score,
        "ignored_field_names": sorted(ignored),
    }


def compare_public_state(before: Mapping[str, Any], after: Mapping[str, Any]) -> str:
    """Conservatively compare only fresh, participant-visible state fields."""

    before_session = before.get("session_id")
    after_session = after.get("session_id")
    if not isinstance(before_session, str) or not before_session:
        return "UNKNOWN_CRITICAL_STATE"
    if not isinstance(after_session, str) or not after_session:
        return "UNKNOWN_CRITICAL_STATE"
    if before_session != after_session:
        return "SESSION_MISMATCH"

    changed = False
    for key in ("time", "status"):
        old = before.get(key)
        new = after.get(key)
        if not isinstance(old, Mapping) or not old or not isinstance(new, Mapping) or not new:
            return "UNKNOWN_CRITICAL_STATE"
        if set(old) != set(new):
            return "UNKNOWN_CRITICAL_STATE"
        changed = changed or old != new

    old_flags = before.get("public_flags", {})
    new_flags = after.get("public_flags", {})
    if not isinstance(old_flags, Mapping) or not isinstance(new_flags, Mapping):
        return "UNKNOWN_CRITICAL_STATE"
    if bool(old_flags) != bool(new_flags) or set(old_flags) != set(new_flags):
        if not changed:
            return "UNKNOWN_CRITICAL_STATE"
    elif old_flags != new_flags:
        changed = True

    old_terminal = before.get("terminal")
    new_terminal = after.get("terminal")
    if old_terminal is not None and not isinstance(old_terminal, bool):
        return "UNKNOWN_CRITICAL_STATE"
    if new_terminal is not None and not isinstance(new_terminal, bool):
        return "UNKNOWN_CRITICAL_STATE"
    if (old_terminal is None) != (new_terminal is None):
        if not changed:
            return "UNKNOWN_CRITICAL_STATE"
    elif old_terminal != new_terminal:
        changed = True

    return "STATE_CHANGED" if changed else "STATE_UNCHANGED"


def _rejection_context(snapshot: Mapping[str, Any]) -> tuple[Any, ...]:
    """Identify the public menu context for preventing an immediate resend."""

    event = snapshot.get("event")
    event_context = (
        event.get("title"),
        event.get("description"),
    ) if isinstance(event, Mapping) else (None, None)
    choices = snapshot.get("choices")
    choice_context = tuple(
        (choice.get("choice"), choice.get("action"), choice.get("description"))
        for choice in choices
        if isinstance(choice, Mapping)
    ) if isinstance(choices, list) else ()
    return snapshot.get("session_id"), event_context, choice_context


@dataclass(frozen=True)
class ActionReconciliation:
    classification: str
    comparison: str
    snapshot: dict[str, Any] | None
    receipt: dict[str, Any]
    rejected: bool


async def reconcile_completed_action(
    before: Mapping[str, Any],
    result: Any,
    fresh_observe: Any,
) -> ActionReconciliation:
    """Reconcile every completed MCP result against exactly one fresh observe."""

    payload, text, is_error = _decode_result(result)
    receipt = _public_receipt(payload, text)
    raw = _unwrap_public_payload(payload)
    status = str(receipt.get("status", "")).lower()
    negative = (
        is_error
        or raw.get("success") is False
        or status in {"rejected", "invalid", "invalid_choice", "action_rejected"}
    )
    try:
        snapshot = await fresh_observe()
    except Exception:
        return ActionReconciliation("UNKNOWN_SIDE_EFFECT", "OBSERVE_FAILED", None, receipt, False)
    if not isinstance(snapshot, Mapping):
        return ActionReconciliation("UNKNOWN_SIDE_EFFECT", "OBSERVE_UNCONFIRMED", None, receipt, False)

    comparison = compare_public_state(before, snapshot)
    if comparison in {"SESSION_MISMATCH", "UNKNOWN_CRITICAL_STATE"}:
        return ActionReconciliation("UNKNOWN_SIDE_EFFECT", comparison, None, receipt, False)
    if negative and comparison == "STATE_UNCHANGED":
        return ActionReconciliation(
            "EXPLICIT_ACTION_REJECTION_CONFIRMED", comparison, dict(snapshot), receipt, True
        )
    if negative and comparison == "STATE_CHANGED":
        return ActionReconciliation(
            "ACTION_RESPONSE_FALSE_BUT_PUBLIC_STATE_CHANGED", comparison, dict(snapshot), receipt, False
        )
    classification = (
        "ACTION_RESPONSE_STATE_CHANGED" if comparison == "STATE_CHANGED"
        else "ACTION_RESPONSE_STATE_UNCHANGED"
    )
    return ActionReconciliation(classification, comparison, dict(snapshot), receipt, False)


def _decode_result(result: Any) -> tuple[Any, str, bool]:
    """Decode MCP structured content or text without trusting unknown fields."""

    is_error = bool(getattr(result, "isError", False))
    structured = getattr(result, "structuredContent", None)
    if structured is None:
        structured = getattr(result, "structured_content", None)
    if structured is not None:
        return structured, "", is_error
    texts = [getattr(item, "text", "") for item in getattr(result, "content", ())]
    text = "\n".join(item for item in texts if isinstance(item, str))
    if text:
        try:
            return json.loads(text), text, is_error
        except json.JSONDecodeError:
            return {"text": text}, text, is_error
    return {}, "", is_error


def _find_session_id(value: Any) -> str | None:
    if isinstance(value, Mapping):
        found = value.get("session_id")
        if isinstance(found, str) and found:
            return found
        for key in ("result", "data", "observation", "current_state"):
            found = _find_session_id(value.get(key))
            if found:
                return found
    return None


def _public_receipt(value: Any, text: str) -> dict[str, Any]:
    raw = _unwrap_public_payload(value)
    receipt = {
        str(key): item[:2000] if isinstance(item, str) else item
        for key, item in raw.items()
        if key in PUBLIC_RECEIPT_FIELDS and _scalar(item)
    }
    if not receipt and text:
        receipt["text"] = text[:2000]
    return receipt


def _schema_summary(tool: Any) -> dict[str, Any]:
    schema = getattr(tool, "inputSchema", None) or getattr(tool, "input_schema", None) or {}
    props = schema.get("properties", {}) if isinstance(schema, Mapping) else {}
    required = schema.get("required", []) if isinstance(schema, Mapping) else []
    safe_props = {}
    if isinstance(props, Mapping):
        for key, value in props.items():
            if isinstance(value, Mapping):
                safe_props[str(key)] = {name: value[name] for name in ("type", "description") if name in value}
            else:
                safe_props[str(key)] = {}
    return {"name": getattr(tool, "name", ""), "required": list(required), "properties": safe_props}


def validate_tool_contract(tools: Sequence[Any]) -> dict[str, Any]:
    by_name = {getattr(tool, "name", ""): tool for tool in tools}
    missing = {"new_game", "observe", "take_action"} - set(by_name)
    if missing:
        raise RuntimeError(f"required participant-facing tools are missing: {sorted(missing)}")
    summaries = {name: _schema_summary(by_name[name]) for name in ("new_game", "observe", "take_action")}
    expected = {"observe": {"session_id"}, "take_action": {"session_id", "choice", "notes"}}
    for name, fields in expected.items():
        if not fields.issubset(set(summaries[name]["properties"])):
            raise RuntimeError(f"{name} schema lacks required public fields: {sorted(fields)}")
    choice_type = summaries["take_action"]["properties"].get("choice", {}).get("type")
    if choice_type != "integer":
        raise RuntimeError("take_action.choice is not declared as one integer")
    return {"tool_names": [getattr(tool, "name", "") for tool in tools], "required_schemas": summaries}


def _minimal_child_env(output_dir: Path) -> dict[str, str]:
    """Only add local CareerSim paths; the MCP SDK inherits its safe OS allowlist."""

    env = {
        "PATH": str(Path(sys.executable).parent),
        "CAREER_EMULATOR_DB": str(output_dir / "career_emulator.sqlite3"),
        "CAREER_EMULATOR_LOG_DIR": str(output_dir / "emulator-logs"),
    }
    for name in ("SYSTEMROOT", "WINDIR", "TEMP", "TMP", "USERPROFILE", "HOMEDRIVE", "HOMEPATH"):
        value = os.environ.get(name)
        if value:
            env[name] = value
    return env


def _timestamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


class JsonlEvidence:
    def __init__(self, path: Path, *, append: bool = False) -> None:
        self.path = path
        self.file = path.open("a" if append else "x", encoding="utf-8", newline="\n")

    def write(self, kind: str, **fields: Any) -> None:
        self.file.write(json.dumps({"at": _timestamp(), "kind": kind, **fields}, ensure_ascii=False) + "\n")
        self.file.flush()

    def close(self) -> None:
        self.file.close()


def _print_snapshot(snapshot: Mapping[str, Any], label: str) -> None:
    print(f"\n=== {label} ===", flush=True)
    print(f"Session: {snapshot['session_id'] or '(not repeated in payload; query session retained)'}", flush=True)
    time = snapshot["time"]
    print(
        "Time: " + ", ".join(f"{key.removeprefix('current_')}={value}" for key, value in time.items())
        if time
        else "Time: UNKNOWN",
        flush=True,
    )
    print("Status: " + (json.dumps(snapshot["status"], ensure_ascii=False) if snapshot["status"] else "UNKNOWN"), flush=True)
    if snapshot["event"]:
        print("Current public event: " + json.dumps(snapshot["event"], ensure_ascii=False), flush=True)
    if snapshot["public_feed"]:
        print("Public feedback/events: " + snapshot["public_feed"], flush=True)
    choices = snapshot["choices"]
    print("Legal public choices:", flush=True)
    for choice in choices:
        print(
            f"  {choice['choice']}: {choice['action']}"
            + (f" — {choice['description']}" if choice["description"] else ""),
            flush=True,
        )
    if not choices:
        print("  (none)", flush=True)
    print(f"Public terminal: {snapshot['terminal']}", flush=True)
    if snapshot["ending_score"]:
        print("Public ending score: " + json.dumps(snapshot["ending_score"], ensure_ascii=False), flush=True)
    if snapshot["ignored_field_names"]:
        print("Ignored unknown field names: " + ", ".join(snapshot["ignored_field_names"]), flush=True)


def _resume_counts(path: Path, session_id: str) -> tuple[int, int]:
    """Require a known, nonterminal public checkpoint before reconnecting."""

    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
    sessions = {row.get("session_id") for row in rows if row.get("kind") == "new_game"}
    if sessions != {session_id}:
        raise ValueError("resume session does not match the single recorded new_game")
    observes = [row for row in rows if row.get("kind") == "observe"]
    if not observes or observes[-1].get("snapshot", {}).get("session_id") != session_id:
        raise ValueError("no same-session public observe checkpoint")
    if observes[-1]["snapshot"].get("terminal") is not False:
        raise ValueError("resume requires a nonterminal public checkpoint")
    attempts = [row for row in rows if row.get("kind") == "take_action"]
    if not attempts or attempts[-1].get("outcome") != "ACTION_RESPONSE_STATE_CHANGED":
        raise ValueError("last action outcome is not confirmed as state changed")
    boundary = [row for row in rows if row.get("kind") not in {"stop", "bridge_shutdown"}]
    if boundary[-1].get("kind") != "take_action":
        raise ValueError("resume checkpoint is not at a closed action boundary")
    if boundary[-2].get("kind") != "observe":
        raise ValueError("last action lacks its immediately preceding public observe")
    return len(observes), len(attempts)


async def run_pilot(output_dir: Path, resume_session_id: str | None = None) -> int:
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    if resume_session_id is None:
        if output_dir.exists():
            raise FileExistsError(f"refusing to reuse existing task evidence directory: {output_dir}")
        output_dir.mkdir(parents=True, exist_ok=False)
        (output_dir / "emulator-logs").mkdir()
        prior_observes, action_attempts = 0, 0
    else:
        prior_observes, action_attempts = _resume_counts(
            output_dir / "public-trajectory.jsonl", resume_session_id
        )
    evidence = JsonlEvidence(output_dir / "public-trajectory.jsonl", append=resume_session_id is not None)
    executable = Path(sys.executable).parent / "career-emulator-mcp.exe"
    if not executable.is_file():
        evidence.close()
        raise FileNotFoundError(f"direct MCP executable not found: {executable}")

    params = StdioServerParameters(
        command=str(executable),
        args=["--update", "skip"],
        cwd=str(executable.parent),
        env=_minimal_child_env(output_dir),
    )
    print("Starting one direct career-emulator-mcp child; no AgentServer/provider is used.", flush=True)
    evidence.write("direct_mcp_start", executable=str(executable), args=params.args, cwd=params.cwd)
    session_id: str | None = resume_session_id
    status_code = 1
    try:
        async with stdio_client(params) as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as client:
                initialized = await client.initialize()
                evidence.write("initialize", protocol_version=str(initialized.protocolVersion))
                listed = await client.list_tools()
                contract = validate_tool_contract(listed.tools)
                seed_control = any(
                    "seed" in name.lower() or "replay" in name.lower()
                    for name in contract["required_schemas"]["new_game"]["properties"]
                )
                evidence.write("list_tools", **contract, public_seed_control=seed_control)
                print("Required public tool schemas:", json.dumps(contract, ensure_ascii=False), flush=True)
                print("Public new_game seed/replay control:", "FOUND" if seed_control else "NOT FOUND", flush=True)

                if resume_session_id is None:
                    new_game_result = await client.call_tool("new_game", arguments={})
                    new_payload, new_text, new_error = _decode_result(new_game_result)
                    session_id = _find_session_id(new_payload)
                    evidence.write(
                        "new_game",
                        result_status="MCP_ERROR" if new_error else "RETURNED",
                        session_id=session_id,
                        public_receipt=_public_receipt(new_payload, new_text),
                    )
                    if new_error or not session_id:
                        print("new_game did not return a clearly usable session identity; stopping without retry.", flush=True)
                        evidence.write("stop", reason="NEW_GAME_ERROR_OR_SESSION_UNKNOWN")
                        return 2
                    print(f"Fresh public session: {session_id}", flush=True)
                else:
                    evidence.write("resume_session", session_id=session_id, prior_action_attempts=action_attempts)
                    print(f"Resuming public session: {session_id}; no new_game call.", flush=True)

                observe_count = prior_observes

                async def observe_and_render(label: str) -> dict[str, Any] | None:
                    nonlocal observe_count
                    observe_count += 1
                    result = await client.call_tool("observe", arguments={"session_id": session_id})
                    payload, text, is_error = _decode_result(result)
                    if is_error:
                        evidence.write("observe_error", count=observe_count, public_receipt=_public_receipt(payload, text))
                        return None
                    snapshot = project_public_snapshot(_unwrap_public_payload(payload))
                    returned_session = snapshot["session_id"]
                    if not returned_session:
                        evidence.write("stop", reason="OBSERVE_SESSION_ID_MISSING", expected=session_id)
                        return None
                    if returned_session != session_id:
                        evidence.write("stop", reason="OBSERVE_SESSION_MISMATCH", expected=session_id, returned=returned_session)
                        return None
                    evidence.write("observe", count=observe_count, snapshot=snapshot)
                    _print_snapshot(snapshot, label)
                    return snapshot

                current = await observe_and_render("FRESH PUBLIC OBSERVE")
                if current is None:
                    print("Observe failed or session identity mismatched; stopping.", flush=True)
                    return 3

                blocked_choices: set[int] = set()
                blocked_context: tuple[Any, ...] | None = None
                while current["terminal"] is not True:
                    if blocked_choices and blocked_context != _rejection_context(current):
                        blocked_choices.clear()
                        blocked_context = None
                    legal_ids = [choice["choice"] for choice in current["choices"]]
                    if not legal_ids:
                        print("No legal public choices are available and terminal status is not confirmed; stopping.", flush=True)
                        evidence.write("stop", reason="NO_LEGAL_CHOICES_WITHOUT_PUBLIC_TERMINAL")
                        return 4
                    available_ids = [choice for choice in legal_ids if choice not in blocked_choices]
                    if not available_ids:
                        print("Every current legal choice was explicitly rejected in this unchanged state; stopping without resend.", flush=True)
                        evidence.write("stop", reason="NO_UNBLOCKED_LEGAL_CHOICES", blocked_choices=sorted(blocked_choices))
                        return 4
                    if action_attempts >= 350:
                        print("Authorized action-attempt ceiling reached; stopping without another call.", flush=True)
                        evidence.write("stop", reason="ACTION_ATTEMPT_LIMIT", attempts=action_attempts)
                        return 5

                    print(
                        "WAITING_FOR_PLAYER_CHOICE> enter '<legal integer> | one-sentence rationale'. "
                        + (f" Temporarily blocked rejected choices: {sorted(blocked_choices)}." if blocked_choices else "")
                        + " No action is sent until explicit input.",
                        flush=True,
                    )
                    line = input().strip()
                    try:
                        player_input = parse_player_input(line, legal_ids, sorted(blocked_choices))
                    except ValueError as exc:
                        print(f"Input rejected locally; no MCP call made: {exc}", flush=True)
                        continue

                    selected = next(choice for choice in current["choices"] if choice["choice"] == player_input.choice)
                    action_attempts += 1
                    evidence.write(
                        "player_decision",
                        month=current["time"].get("current_month"),
                        event=current["event"],
                        choice=player_input.choice,
                        public_action=selected["action"],
                        rationale=player_input.rationale,
                    )
                    print(f"Sending explicit player choice {player_input.choice}: {selected['action']}", flush=True)

                    try:
                        action_result = await client.call_tool(
                            "take_action",
                            arguments={
                                "session_id": session_id,
                                "choice": player_input.choice,
                                "notes": player_input.rationale,
                            },
                        )
                    except Exception as exc:
                        evidence.write("stop", reason="TAKE_ACTION_TRANSPORT_OUTCOME_UNKNOWN", error_type=type(exc).__name__)
                        print("take_action transport outcome unknown; stopping, no resend.", flush=True)
                        return 6

                    reconciliation = await reconcile_completed_action(
                        current,
                        action_result,
                        lambda: observe_and_render("FRESH PUBLIC OBSERVE AFTER ACTION RESPONSE"),
                    )
                    evidence.write(
                        "take_action",
                        attempt=action_attempts,
                        outcome=reconciliation.classification,
                        state_comparison=reconciliation.comparison,
                        public_receipt=reconciliation.receipt,
                    )
                    if reconciliation.snapshot is None:
                        print("Post-action observe could not safely confirm current public state; stopping without resend.", flush=True)
                        evidence.write("stop", reason=reconciliation.classification)
                        return 8
                    if reconciliation.rejected:
                        blocked_choices.add(player_input.choice)
                        blocked_context = _rejection_context(reconciliation.snapshot)
                        print(
                            f"Choice {player_input.choice} was explicitly rejected and public state is unchanged; "
                            "choose another currently legal option.",
                            flush=True,
                        )
                    elif reconciliation.comparison == "STATE_CHANGED":
                        blocked_choices.clear()
                        blocked_context = None
                    current = reconciliation.snapshot

                print("Public terminal state confirmed.", flush=True)
                evidence.write("terminal", snapshot=current, action_attempts=action_attempts)
                status_code = 0
    except KeyboardInterrupt:
        evidence.write("stop", reason="INTERRUPTED_BY_OPERATOR", session_id=session_id, action_attempts=action_attempts)
        print("Interrupted; no further calls will be sent.", flush=True)
        status_code = 130
    except Exception as exc:
        evidence.write("stop", reason="UNHANDLED_LOCAL_OR_MCP_ERROR", error_type=type(exc).__name__, session_id=session_id)
        print(f"Bridge stopped on {type(exc).__name__}; no retry is attempted.", flush=True)
        status_code = 9
    finally:
        evidence.write("bridge_shutdown", session_id=session_id, action_attempts=action_attempts)
        evidence.close()
        print("Direct MCP context closed; shutdown requested for the same child.", flush=True)
    return status_code


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--resume-session-id", help="reconnect to a recorded public session without new_game")
    args = parser.parse_args()
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    return asyncio.run(run_pilot(args.output_dir.resolve(), args.resume_session_id))


if __name__ == "__main__":
    raise SystemExit(main())
