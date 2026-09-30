"""Project participant-facing CLI captures through the HPL public evidence allowlist."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any


SCHEMA_VERSION = "hpl-public-evidence/v1"

PUBLIC_STATE_FIELDS = frozenset(
    {
        "session_id",
        "month",
        "quarter",
        "year",
        "level",
        "health",
        "dignity",
        "skill",
        "network",
        "output",
        "wealth",
        "energy",
    }
)
PUBLIC_EVENT_FIELDS = frozenset({"title", "description"})
PUBLIC_CHOICE_FIELDS = frozenset({"choice", "action", "energy_cost"})
PUBLIC_SELECTION_FIELDS = frozenset({"choice", "action"})
PUBLIC_LOG_FIELDS = frozenset({"month", "event_title", "choice", "action"})
PUBLIC_RECEIPT_FIELDS = frozenset({"status", "message"})
PUBLIC_RESULT_FIELDS = frozenset(
    {"outcome", "survival_months", "grade", "quantitative_score", "competition_partial_score"}
)
PUBLIC_REVIEW_FIELDS = frozenset({"month", "text"})
PUBLIC_PROMOTION_FIELDS = frozenset({"month", "from_level", "to_level"})
PUBLIC_INTERPRETATION_FIELDS = frozenset({"created_at", "text"})
PUBLIC_FRAME_FIELDS = frozenset(
    {
        "state",
        "event",
        "choices",
        "human_selection",
        "warning",
        "handbook",
        "action_receipt",
        "final_result",
        "review",
        "promotion",
        "public_log",
        "human_interpretation",
    }
)

_FIELD_ALLOWLISTS = {
    "state": PUBLIC_STATE_FIELDS,
    "event": PUBLIC_EVENT_FIELDS,
    "human_selection": PUBLIC_SELECTION_FIELDS,
    "action_receipt": PUBLIC_RECEIPT_FIELDS,
    "final_result": PUBLIC_RESULT_FIELDS,
    "review": PUBLIC_REVIEW_FIELDS,
    "promotion": PUBLIC_PROMOTION_FIELDS,
}
_HIDDEN_LOOKING_TEXT = (
    "hiddenrisk",
    "hidden risk",
    "hidden counter",
    "internal score",
    "status_updates",
    "failure_rule_remaining",
    "event_id",
    "node_id",
    "threshold",
    "隐藏风险",
    "隐藏阈值",
    "内部得分",
)


def _unknown_paths(value: Any, path: str, output: list[str]) -> None:
    """Record field paths only; never copy the corresponding values."""
    if isinstance(value, Mapping) and value:
        for key, nested in value.items():
            _unknown_paths(nested, f"{path}.{key}", output)
    elif isinstance(value, (list, tuple)) and value:
        for index, nested in enumerate(value):
            _unknown_paths(nested, f"{path}[{index}]", output)
    else:
        output.append(path)


def _copy_scalar_fields(value: Any, path: str, allowed: frozenset[str], unknown: list[str]) -> dict[str, Any]:
    """Copy only allowed scalar fields from a single mapping."""
    if not isinstance(value, Mapping):
        _unknown_paths(value, path, unknown)
        return {}

    projected: dict[str, Any] = {}
    for key, item in value.items():
        field_path = f"{path}.{key}"
        if key not in allowed:
            _unknown_paths(item, field_path, unknown)
            continue
        if isinstance(item, (Mapping, list, tuple)):
            _unknown_paths(item, field_path, unknown)
            continue
        if item is not None and not isinstance(item, (str, int, float, bool)):
            unknown.append(field_path)
            continue
        if isinstance(item, str) and any(marker in item.casefold() for marker in _HIDDEN_LOOKING_TEXT):
            unknown.append(field_path)
            continue
        projected[str(key)] = item
    return projected


def project_cli_frame(frame: Mapping[str, Any]) -> dict[str, Any]:
    """Return allowlisted participant-visible facts and paths for anything omitted."""
    # Unallowlisted identifiers and score dimensions are recorded as paths only
    # when they actually appear in the captured frame.
    unknown: list[str] = []
    for key, value in frame.items():
        if key not in PUBLIC_FRAME_FIELDS:
            _unknown_paths(value, str(key), unknown)

    observed: dict[str, Any] = {}
    for name, allowed in _FIELD_ALLOWLISTS.items():
        if name in frame:
            projected = _copy_scalar_fields(frame[name], name, allowed, unknown)
            if projected:
                observed[name] = projected

    if "choices" in frame:
        choices = frame["choices"]
        if isinstance(choices, list):
            projected_choices = [
                _copy_scalar_fields(choice, f"choices[{index}]", PUBLIC_CHOICE_FIELDS, unknown)
                for index, choice in enumerate(choices)
            ]
            observed["choices"] = projected_choices
        else:
            _unknown_paths(choices, "choices", unknown)

    for name in ("warning", "handbook"):
        if name not in frame:
            continue
        value = frame[name]
        if isinstance(value, str) and not any(marker in value.casefold() for marker in _HIDDEN_LOOKING_TEXT):
            observed[name] = value
        else:
            _unknown_paths(value, name, unknown)

    if "public_log" in frame:
        lines = frame["public_log"]
        if isinstance(lines, list):
            safe_entries = [
                _copy_scalar_fields(entry, f"public_log[{index}]", PUBLIC_LOG_FIELDS, unknown)
                for index, entry in enumerate(lines)
            ]
            observed["public_log"] = [entry for entry in safe_entries if entry]
        else:
            _unknown_paths(lines, "public_log", unknown)

    unknown_fields = sorted(set(unknown))
    result: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "public_status": "PUBLIC_STATUS_UNKNOWN" if unknown_fields else "PUBLIC_FIELDS_ALLOWLISTED",
        "observed_fact": observed,
        "unknown_fields": unknown_fields,
    }
    if "human_interpretation" in frame:
        interpretation = _copy_scalar_fields(
            frame["human_interpretation"], "human_interpretation", PUBLIC_INTERPRETATION_FIELDS, unknown
        )
        result["human_interpretation"] = interpretation
        result["unknown_fields"] = sorted(set(unknown))
        if result["unknown_fields"]:
            result["public_status"] = "PUBLIC_STATUS_UNKNOWN"
    return result
