"""Bounded public-only behavioral evaluation for isolated Skill copies.

Provider requests are opt-in and use a direct OpenAI-compatible HTTPS request.
This module never starts a local runtime or reads gameplay data.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import statistics
import urllib.error
import urllib.request
from collections import defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
EXPERIMENT = ROOT / "experiments" / "s07-50"
CASES_PATH = EXPERIMENT / "evals" / "eval_cases.json"
DEFAULT_OUTPUT_PATH = ROOT / "experiments" / "s07-50r" / "evals" / "provider_results.json"

PREFLIGHT_REQUEST_CAP = 1
SANITY_REQUEST_CAP = 4
MAX_MATRIX_REQUESTS = 80
MAX_TOTAL_PROVIDER_REQUESTS = 85
REPETITIONS = 2
TARGET_MODEL = "deepseek-flash"
TARGET_BASE_URL = "https://api.deepseek.com"
MAX_TOKENS = 4096
REQUEST_TIMEOUT_SECONDS = 90

SKILL_FILES = {
    "board": "structured-state-board.SKILL.md",
    "planning": "rolling-planning.SKILL.md",
    "delivery": "delivery-progress.SKILL.md",
    "risk": "risk-review.SKILL.md",
}
GLOBAL_FIREWALL = (
    "Use only participant-visible public evidence. Exclude hidden/internal fields and any "
    "field whose public status is unclear. Never quote, compare, summarize, or reason from "
    "prohibited numeric fields."
)
REQUEST_CONTRACT = {
    "thinking_condition": "OFFICIAL_DEFAULT_THINKING",
    "thinking": {"type": "enabled"},
    "reasoning_effort": "high",
    "max_tokens": MAX_TOKENS,
    "temperature": "OMITTED_THINKING_MODE",
    "stream": False,
    "response_format": {"type": "json_object"},
    "runtime_equivalence": "RUNTIME_MODE_NOT_VERIFIED",
}
FINISH_REASONS = {
    "stop",
    "length",
    "content_filter",
    "tool_calls",
    "insufficient_system_resource",
    "aborted",
}
EMPTY_CATEGORIES = {
    "EMPTY_CONTENT_LENGTH",
    "EMPTY_CONTENT_WITH_REASONING",
    "EMPTY_CONTENT_OTHER",
}
TECHNICAL_CATEGORIES = EMPTY_CATEGORIES | {
    "TRANSPORT_ERROR",
    "HTTP_ERROR",
    "INVALID_RESPONSE_ENVELOPE",
    "TRUNCATED_OUTPUT",
    "INCOMPLETE_PROVIDER_OUTPUT",
}


def load_cases(path: Path = CASES_PATH) -> list[dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("schema_version") != 1 or not isinstance(payload.get("cases"), list):
        raise ValueError("Unsupported eval case schema")
    cases = payload["cases"]
    ids = [case.get("id") for case in cases]
    if not all(isinstance(case_id, str) and case_id for case_id in ids):
        raise ValueError("Every eval case needs a non-empty id")
    if len(ids) != len(set(ids)):
        raise ValueError("Eval case ids must be unique")
    required = {"skill", "input", "assertions", "critical"}
    if any(not required.issubset(case) for case in cases):
        raise ValueError("Eval case is missing required fields")
    return cases


def evaluation_units(cases: list[dict[str, Any]]) -> list[list[dict[str, Any]]]:
    """Bundle only the paired Delivery identity cases to fit the 80-call matrix."""
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    units: list[list[dict[str, Any]]] = []
    for case in cases:
        group = case.get("request_group")
        if group:
            groups[group].append(case)
        else:
            units.append([case])
    units.extend(groups.values())
    units.sort(key=lambda unit: min(case["id"] for case in unit))
    return units


def load_version(version: str) -> tuple[str, dict[str, str]]:
    if version not in {"current", "rewrite"}:
        raise ValueError(f"Unknown version: {version}")
    folder = EXPERIMENT / version
    skills = {
        skill: (folder / filename).read_text(encoding="utf-8")
        for skill, filename in SKILL_FILES.items()
    }
    manifest = (folder / "runtime_manifest.json").read_text(encoding="utf-8")
    return manifest, skills


def _format_expected_shape(skill: str) -> str:
    if skill == "board":
        return '{"STATE":{"H":"...","D":"...","S":"...","N":"...","O":"...","W":"...","L":"...","E":"..."},"STICKY":"...","EFFECTS":"..."}'
    if skill == "planning":
        return '{"BINDING_CONSTRAINT":"YES|NO|UNKNOWN","MODE":"A|S|UNKNOWN","GAP":"...","CANDIDATE":"..."}'
    if skill == "delivery":
        return '{"items":{"D1":{"id":"D1","item":"...","stage":"...","evidence":"UNKNOWN|UNVERIFIED|PUBLICLY_VERIFIED","proof_basis":"...","recognition":"0|1|?","active":true}}}'
    if skill == "risk":
        return '{"ROUTE":"QUICK_GATE|FULL_REVIEW","RISK_RESULT":"PASS|ALLOW|WARN|RECONSIDER|UNKNOWN","REASON":"..."}'
    return '{"board":{"STATE":{},"STICKY":"...","EFFECTS":"..."},"delivery":{"items":{}},"planning":{"BINDING_CONSTRAINT":"...","MODE":"...","GAP":"...","CANDIDATE":"..."},"risk":{"ROUTE":"...","RISK_RESULT":"...","REASON":"..."}}'


def build_prompt(version: str, cases: list[dict[str, Any]]) -> str:
    manifest_text, skills = load_version(version)
    integrated = any(case["skill"] == "integrated" for case in cases)
    skill = "integrated" if integrated else cases[0]["skill"]
    if integrated:
        context = "EXPERIMENTAL RUNTIME MANIFEST:\n" + manifest_text
        for skill_name, body in skills.items():
            context += f"\n\nSKILL {skill_name}:\n{body}"
    else:
        context = "GLOBAL FIREWALL:\n" + GLOBAL_FIREWALL
        context += f"\n\nSKILL UNDER TEST ({skill}):\n{skills[skill]}"

    if len(cases) == 1:
        body = f"CASE {cases[0]['id']}\nSYNTHETIC INPUT:\n{cases[0]['input']}"
        shape = _format_expected_shape(skill)
    else:
        body = "\n\n".join(
            f"CASE {case['id']} (independent context; reset state between cases)\nSYNTHETIC INPUT:\n{case['input']}"
            for case in cases
        )
        shape = "{" + ",".join(f'"{case["id"]}":{_format_expected_shape(case["skill"])}' for case in cases) + "}"
    return (
        "Apply the supplied instructions to the synthetic case(s). Treat each case as an "
        "independent context; do not transfer state between cases. Return only the compact "
        "JSON object shown below. Do not provide chain-of-thought or hidden reasoning. "
        "Use public evidence only. Keep reasons concise.\n\n"
        + context
        + "\n\n"
        + body
        + "\n\nREQUIRED OUTPUT SHAPE (JSON only):\n"
        + shape
    )


def parse_json_output(raw: str) -> Any:
    """Parse only a direct JSON document; wrappers violate the requested output contract."""
    try:
        parsed = json.loads(raw.strip())
    except (json.JSONDecodeError, TypeError):
        return None
    return parsed if isinstance(parsed, dict) else None


def _get_path(value: Any, path: str) -> Any:
    if path == "$raw":
        return value
    current = value
    for part in path.split("."):
        if isinstance(current, dict):
            current = current.get(part)
        elif isinstance(current, list) and part.isdigit():
            index = int(part)
            current = current[index] if index < len(current) else None
        else:
            return None
    return current


def grade_case(case: dict[str, Any], answer: Any, raw: str) -> dict[str, Any]:
    if isinstance(answer, dict) and case["id"] in answer and case["skill"] != "integrated":
        answer = answer[case["id"]]
    if not isinstance(answer, dict):
        return {"status": "FAIL", "passed": False, "assertions": [], "parseable": False}
    checks = []
    all_pass = True
    for assertion in case["assertions"]:
        path = assertion["path"]
        actual = raw if path == "$raw" else _get_path(answer, path)
        op = assertion["op"]
        expected = assertion["value"]
        if op == "eq":
            passed = actual == expected
        elif op == "one_of":
            passed = actual in expected
        elif op == "eq_ci":
            passed = str(actual).casefold() == str(expected).casefold()
        elif op == "not_eq_ci":
            passed = actual is not None and str(actual).casefold() != str(expected).casefold()
        elif op == "contains":
            passed = isinstance(actual, str) and str(expected).casefold() in actual.casefold()
        elif op == "contains_any":
            passed = isinstance(actual, str) and any(str(item).casefold() in actual.casefold() for item in expected)
        elif op == "not_contains":
            candidate = actual if isinstance(actual, str) else json.dumps(actual, ensure_ascii=False)
            passed = str(expected).casefold() not in candidate.casefold()
        else:
            raise ValueError(f"Unsupported assertion op: {op}")
        checks.append({"path": path, "op": op, "passed": passed})
        all_pass = all_pass and passed
    return {"status": "PASS" if all_pass else "FAIL", "passed": all_pass, "assertions": checks, "parseable": True}


def classify_repetitions(case_results: list[dict[str, Any]]) -> str:
    statuses = [row["grade"]["status"] for row in case_results]
    if any(status == "TECHNICAL_UNKNOWN" for status in statuses):
        return "TECHNICAL_UNKNOWN"
    passes = sum(status == "PASS" for status in statuses)
    if passes == 2:
        return "SYSTEMATIC_PASS"
    if passes == 1:
        return "FRAGILE"
    return "FAIL"


def redact_secrets(value: str, secrets: list[str] | None = None) -> str:
    secrets = [secret for secret in (secrets or []) if secret]
    result = value
    for secret in secrets:
        result = result.replace(secret, "[REDACTED]")
    result = re.sub(r"(?i)(authorization\s*:\s*bearer\s+)[^\s,;]+", r"\1[REDACTED]", result)
    result = re.sub(r"(?i)(api[_-]?key\s*[=:]\s*)[^\s,;]+", r"\1[REDACTED]", result)
    return result


def provider_config() -> tuple[str, str, str]:
    api_key = os.environ.get("DEEPSEEK_API_KEY", "")
    if not api_key:
        raise RuntimeError("provider credential unavailable")
    model = os.environ.get("SKILL_EVAL_MODEL") or os.environ.get("MODEL_NAME") or TARGET_MODEL
    base = os.environ.get("SKILL_EVAL_API_BASE") or os.environ.get("API_BASE") or TARGET_BASE_URL
    base = base.rstrip("/")
    if model != TARGET_MODEL or base != TARGET_BASE_URL:
        raise RuntimeError("provider target does not match verified alias and endpoint")
    return api_key, model, base


def request_payload(model: str, prompt: str) -> dict[str, Any]:
    return {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        **{
            key: value
            for key, value in REQUEST_CONTRACT.items()
            if key in {"thinking", "reasoning_effort", "max_tokens", "stream", "response_format"}
        },
    }


def _safe_reported_model(value: Any) -> str | None:
    if isinstance(value, str) and re.fullmatch(r"[A-Za-z0-9._-]{1,100}", value):
        return value
    return None


def _safe_finish_reason(value: Any) -> str | None:
    if isinstance(value, str) and value in FINISH_REASONS:
        return value
    return None


def _safe_nonnegative_int(value: Any) -> int | None:
    if type(value) is int and value >= 0:
        return value
    return None


def _empty_response_metadata(http_status: int | None, http_success: bool) -> dict[str, Any]:
    return {
        "http_success": http_success,
        "http_status": http_status,
        "provider_reported_model": None,
        "finish_reason": None,
        "content_present": False,
        "content_chars": None,
        "reasoning_content_present": False,
        "reasoning_chars": None,
        "prompt_tokens": None,
        "completion_tokens": None,
        "reasoning_tokens": None,
        "total_tokens": None,
    }


def _extract_response(payload: Any, http_status: int) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise ValueError("invalid response envelope")
    choices = payload.get("choices")
    if not isinstance(choices, list) or not choices or not isinstance(choices[0], dict):
        raise ValueError("missing response choices")
    choice = choices[0]
    message = choice.get("message")
    if not isinstance(message, dict):
        raise ValueError("missing response message")
    content_value = message.get("content")
    reasoning_value = message.get("reasoning_content")
    if content_value is not None and not isinstance(content_value, str):
        raise ValueError("invalid final content type")
    if reasoning_value is not None and not isinstance(reasoning_value, str):
        raise ValueError("invalid reasoning metadata type")
    usage = payload.get("usage")
    usage = usage if isinstance(usage, dict) else {}
    completion_details = usage.get("completion_tokens_details")
    completion_details = completion_details if isinstance(completion_details, dict) else {}
    reasoning_tokens = completion_details.get("reasoning_tokens", usage.get("reasoning_tokens"))
    metadata = {
        "http_success": 200 <= http_status < 300,
        "http_status": http_status,
        "provider_reported_model": _safe_reported_model(payload.get("model")),
        "finish_reason": _safe_finish_reason(choice.get("finish_reason")),
        "content_present": content_value is not None,
        "content_chars": len(content_value) if isinstance(content_value, str) else None,
        "reasoning_content_present": reasoning_value is not None,
        "reasoning_chars": len(reasoning_value) if isinstance(reasoning_value, str) else None,
        "prompt_tokens": _safe_nonnegative_int(usage.get("prompt_tokens")),
        "completion_tokens": _safe_nonnegative_int(usage.get("completion_tokens")),
        "reasoning_tokens": _safe_nonnegative_int(reasoning_tokens),
        "total_tokens": _safe_nonnegative_int(usage.get("total_tokens")),
    }
    return {"metadata": metadata, "observable_content": content_value}


def request_completion(
    prompt: str,
    *,
    api_key: str,
    model: str,
    base_url: str,
    timeout: int = REQUEST_TIMEOUT_SECONDS,
) -> dict[str, Any]:
    body = json.dumps(request_payload(model, prompt)).encode("utf-8")
    request = urllib.request.Request(
        base_url + "/chat/completions",
        data=body,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        method="POST",
    )

    class RejectRedirects(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, new_url):
            return None

    opener = urllib.request.build_opener(RejectRedirects())
    try:
        with opener.open(request, timeout=timeout) as response:
            status = int(response.status)
            try:
                payload = json.loads(response.read().decode("utf-8"))
                extracted = _extract_response(payload, status)
            except (UnicodeDecodeError, json.JSONDecodeError, TypeError, ValueError):
                return {
                    "metadata": _empty_response_metadata(status, 200 <= status < 300),
                    "failure_kind": "INVALID_RESPONSE_ENVELOPE",
                    "observable_content": None,
                }
            if not extracted["metadata"]["http_success"]:
                extracted["failure_kind"] = "HTTP_ERROR"
            return extracted
    except urllib.error.HTTPError as exc:
        return {
            "metadata": _empty_response_metadata(int(exc.code), False),
            "failure_kind": "HTTP_ERROR",
            "observable_content": None,
        }
    except (urllib.error.URLError, TimeoutError, OSError):
        return {
            "metadata": _empty_response_metadata(None, False),
            "failure_kind": "TRANSPORT_ERROR",
            "observable_content": None,
        }


def classify_observation(observation: dict[str, Any]) -> str:
    failure_kind = observation.get("failure_kind")
    if failure_kind:
        return failure_kind
    metadata = observation["metadata"]
    if not metadata["http_success"]:
        return "HTTP_ERROR" if metadata["http_status"] is not None else "TRANSPORT_ERROR"
    content = observation.get("observable_content")
    finish_reason = metadata.get("finish_reason")
    if finish_reason == "length":
        return "EMPTY_CONTENT_LENGTH" if not content else "TRUNCATED_OUTPUT"
    if not isinstance(content, str) or not content:
        if metadata.get("reasoning_chars") or metadata.get("reasoning_tokens"):
            return "EMPTY_CONTENT_WITH_REASONING"
        return "EMPTY_CONTENT_OTHER"
    if finish_reason in {"aborted", "insufficient_system_resource", "content_filter"}:
        return "INCOMPLETE_PROVIDER_OUTPUT"
    if parse_json_output(content) is None:
        return "UNPARSEABLE_OBSERVABLE_OUTPUT"
    return "VALID_OBSERVABLE_OUTPUT"


def update_failure_streaks(
    category: str,
    *,
    technical_streak: int,
    empty_streak: int,
) -> tuple[int, int, bool]:
    if category in EMPTY_CATEGORIES:
        technical_streak += 1
        empty_streak += 1
    elif category in TECHNICAL_CATEGORIES:
        technical_streak += 1
        empty_streak = 0
    else:
        technical_streak = 0
        empty_streak = 0
    return technical_streak, empty_streak, technical_streak >= 2 or empty_streak >= 2


def _new_state(model: str, base_url: str) -> dict[str, Any]:
    return {
        "schema_version": 2,
        "classification": "MICRO_EVAL_ONLY",
        "provider_contract": {
            "model_alias": model,
            "endpoint_host": re.sub(r"^https?://", "", base_url).split("/")[0],
            **REQUEST_CONTRACT,
        },
        "request_caps": {
            "preflight": PREFLIGHT_REQUEST_CAP,
            "sanity": SANITY_REQUEST_CAP,
            "matrix": MAX_MATRIX_REQUESTS,
            "total": MAX_TOTAL_PROVIDER_REQUESTS,
        },
        "new_provider_requests": 0,
        "stages": {},
        "requests": [],
        "case_results": [],
    }


def _assert_safe_state(value: Any) -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            if key.casefold() in {"reasoning_content", "api_key", "authorization"}:
                raise ValueError("refusing to persist a prohibited provider field")
            _assert_safe_state(item)
    elif isinstance(value, list):
        for item in value:
            _assert_safe_state(item)


def _save_state(path: Path, state: dict[str, Any]) -> None:
    _assert_safe_state(state)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _load_state(path: Path, model: str, base_url: str) -> dict[str, Any]:
    if not path.exists():
        return _new_state(model, base_url)
    state = json.loads(path.read_text(encoding="utf-8"))
    expected = _new_state(model, base_url)["provider_contract"]
    if state.get("schema_version") != 2 or state.get("provider_contract") != expected:
        raise RuntimeError("existing evaluation state has a different provider contract")
    if any(row.get("request_state") == "IN_FLIGHT" for row in state.get("requests", [])):
        raise RuntimeError("a provider request has an unresolved in-flight outcome; do not repeat it")
    if state.get("new_provider_requests", 0) > MAX_TOTAL_PROVIDER_REQUESTS:
        raise RuntimeError("provider request cap already exceeded")
    return state


def _ensure_new_stage(state: dict[str, Any], stage: str) -> None:
    if stage in state["stages"]:
        raise RuntimeError(f"{stage} stage already recorded; refusing duplicate provider requests")


def _start_request(
    state: dict[str, Any],
    path: Path,
    *,
    stage: str,
    version: str | None = None,
    case_ids: list[str] | None = None,
    repetition: int | None = None,
    retry_of: int | None = None,
) -> dict[str, Any]:
    if state["new_provider_requests"] >= MAX_TOTAL_PROVIDER_REQUESTS:
        raise RuntimeError("absolute provider request cap reached")
    row = {
        "request_index": state["new_provider_requests"] + 1,
        "stage": stage,
        "version": version,
        "case_ids": case_ids or [],
        "repetition": repetition,
        "retry_of_request_index": retry_of,
        "request_state": "IN_FLIGHT",
    }
    state["new_provider_requests"] += 1
    state["requests"].append(row)
    _save_state(path, state)
    return row


def _perform_request(
    state: dict[str, Any],
    path: Path,
    *,
    prompt: str,
    api_key: str,
    model: str,
    base_url: str,
    stage: str,
    version: str | None = None,
    case_ids: list[str] | None = None,
    repetition: int | None = None,
    retry_of: int | None = None,
) -> tuple[dict[str, Any], str | None]:
    row = _start_request(
        state,
        path,
        stage=stage,
        version=version,
        case_ids=case_ids,
        repetition=repetition,
        retry_of=retry_of,
    )
    observation = request_completion(prompt, api_key=api_key, model=model, base_url=base_url)
    category = classify_observation(observation)
    raw_output = observation.get("observable_content")
    safe_output = redact_secrets(raw_output, [api_key]) if isinstance(raw_output, str) else None
    row.update(observation["metadata"])
    row["output_classification"] = category
    row["observable_output"] = safe_output
    row["output_chars"] = len(safe_output) if isinstance(safe_output, str) else observation["metadata"]["content_chars"]
    row["request_state"] = "COMPLETED"
    _save_state(path, state)
    return row, safe_output


def _case_answers(unit: list[dict[str, Any]], raw: str) -> dict[str, Any]:
    parsed = parse_json_output(raw)
    if len(unit) == 1:
        return {unit[0]["id"]: parsed}
    return parsed if isinstance(parsed, dict) else {}


def _record_case_results(
    state: dict[str, Any],
    *,
    unit: list[dict[str, Any]],
    raw: str | None,
    category: str,
    row: dict[str, Any],
) -> list[dict[str, Any]]:
    if category in {"VALID_OBSERVABLE_OUTPUT", "UNPARSEABLE_OBSERVABLE_OUTPUT"} and isinstance(raw, str):
        answers = _case_answers(unit, raw)
        results = []
        for case in unit:
            answer = answers.get(case["id"])
            grade = grade_case(case, answer, raw)
            if category == "UNPARSEABLE_OBSERVABLE_OUTPUT":
                grade["status"] = "FAIL"
                grade["passed"] = False
                grade["parseable"] = False
            result = {
                "stage": row["stage"],
                "version": row.get("version"),
                "case_id": case["id"],
                "repetition": row.get("repetition"),
                "request_index": row["request_index"],
                "critical": case["critical"],
                "output_classification": category,
                "grade": grade,
            }
            state["case_results"].append(result)
            results.append(result)
        return results
    results = []
    for case in unit:
        result = {
            "stage": row["stage"],
            "version": row.get("version"),
            "case_id": case["id"],
            "repetition": row.get("repetition"),
            "request_index": row["request_index"],
            "critical": case["critical"],
            "output_classification": category,
            "grade": {
                "status": "TECHNICAL_UNKNOWN",
                "passed": False,
                "assertions": [],
                "parseable": False,
            },
        }
        state["case_results"].append(result)
        results.append(result)
    return results


def preflight_prompt() -> str:
    return (
        'Return only this compact JSON object and no other text: {"status":"OK"}. '
        "Do not provide chain-of-thought. The output must be valid JSON."
    )


def run_preflight(output_path: Path = DEFAULT_OUTPUT_PATH) -> dict[str, Any]:
    api_key, model, base_url = provider_config()
    state = _load_state(output_path, model, base_url)
    _ensure_new_stage(state, "preflight")
    if state["new_provider_requests"] != 0:
        raise RuntimeError("preflight must be the first request in a new S07-50R evaluation")
    state["stages"]["preflight"] = {"status": "RUNNING", "request_count": 0}
    _save_state(output_path, state)
    row, raw = _perform_request(
        state,
        output_path,
        prompt=preflight_prompt(),
        api_key=api_key,
        model=model,
        base_url=base_url,
        stage="preflight",
    )
    parsed = parse_json_output(raw or "")
    passed = (
        row["output_classification"] == "VALID_OBSERVABLE_OUTPUT"
        and parsed == {"status": "OK"}
        and row.get("finish_reason") != "length"
    )
    state["stages"]["preflight"] = {
        "status": "PASS" if passed else "FAIL",
        "gate": "PREFLIGHT_PASS" if passed else "PROVIDER_PREFLIGHT_FAIL",
        "request_count": 1,
        "request_index": row["request_index"],
    }
    _save_state(output_path, state)
    return state["stages"]["preflight"]


def _find_case(case_id: str, cases: list[dict[str, Any]]) -> dict[str, Any]:
    return next(case for case in cases if case["id"] == case_id)


def run_sanity(output_path: Path = DEFAULT_OUTPUT_PATH) -> dict[str, Any]:
    api_key, model, base_url = provider_config()
    state = _load_state(output_path, model, base_url)
    _ensure_new_stage(state, "sanity")
    if state.get("stages", {}).get("preflight", {}).get("status") != "PASS":
        raise RuntimeError("sanity gate requires PREFLIGHT_PASS")
    cases = load_cases()
    sanity_slots = [
        ("B1_WEALTH_COPY_TRAP", "current"),
        ("B1_WEALTH_COPY_TRAP", "rewrite"),
        ("R3_ACUTE_SAFE_CANDIDATE", "current"),
        ("R3_ACUTE_SAFE_CANDIDATE", "rewrite"),
    ]
    stage = {"status": "RUNNING", "request_count": 0, "results": []}
    state["stages"]["sanity"] = stage
    _save_state(output_path, state)
    for case_id, version in sanity_slots:
        case = _find_case(case_id, cases)
        row, raw = _perform_request(
            state,
            output_path,
            prompt=build_prompt(version, [case]),
            api_key=api_key,
            model=model,
            base_url=base_url,
            stage="sanity",
            version=version,
            case_ids=[case_id],
            repetition=1,
        )
        case_result = _record_case_results(
            state,
            unit=[case],
            raw=raw,
            category=row["output_classification"],
            row=row,
        )[0]
        stage["request_count"] += 1
        stage["results"].append(
            {
                "version": version,
                "case_id": case_id,
                "output_classification": row["output_classification"],
                "behavioral_grade": case_result["grade"]["status"],
                "request_index": row["request_index"],
            }
        )
        if row["output_classification"] != "VALID_OBSERVABLE_OUTPUT":
            stage.update({"status": "FAIL", "gate": "PROVIDER_SANITY_GATE_FAIL"})
            _save_state(output_path, state)
            return stage
        _save_state(output_path, state)
    stage.update({"status": "PASS", "gate": "PROVIDER_SANITY_GATE_PASS"})
    _save_state(output_path, state)
    return stage


def summarize_state(state: dict[str, Any], cases: list[dict[str, Any]]) -> dict[str, Any]:
    matrix_results: dict[str, dict[str, list[dict[str, Any]]]] = defaultdict(lambda: defaultdict(list))
    case_by_id = {case["id"]: case for case in cases}
    for result in state.get("case_results", []):
        if result.get("stage") == "matrix":
            matrix_results[result["case_id"]][result["version"]].append(result)
    classifications: dict[str, dict[str, str]] = {}
    critical_regressions = []
    for case in cases:
        case_id = case["id"]
        classifications[case_id] = {}
        for version in ("current", "rewrite"):
            results = matrix_results.get(case_id, {}).get(version, [])
            classifications[case_id][version] = (
                classify_repetitions(results) if len(results) == REPETITIONS else "TECHNICAL_UNKNOWN"
            )
        if case["critical"]:
            current = classifications[case_id]["current"]
            rewrite = classifications[case_id]["rewrite"]
            if current == "SYSTEMATIC_PASS" and rewrite != "SYSTEMATIC_PASS":
                critical_regressions.append(
                    {"case_id": case_id, "current": current, "rewrite": rewrite}
                )
    lengths: dict[str, dict[str, list[int]]] = defaultdict(lambda: defaultdict(list))
    for request in state.get("requests", []):
        if request.get("stage") != "matrix" or request.get("request_state") != "COMPLETED":
            continue
        version = request.get("version")
        ids = request.get("case_ids") or []
        if version not in {"current", "rewrite"} or not ids:
            continue
        skill = case_by_id[ids[0]]["skill"]
        chars = request.get("output_chars")
        if type(chars) is int:
            lengths[version][skill].append(chars)
    medians = {
        version: {
            skill: statistics.median(values) if values else None
            for skill, values in sorted(by_skill.items())
        }
        for version, by_skill in sorted(lengths.items())
    }
    return {
        "case_classifications": classifications,
        "critical_regressions": critical_regressions,
        "median_output_chars_by_version_and_skill": medians,
    }


def _matrix_schedule(cases: list[dict[str, Any]]) -> list[tuple[str, list[dict[str, Any]], int]]:
    units = evaluation_units(cases)
    return [
        (version, unit, repetition)
        for version in ("current", "rewrite")
        for unit in units
        for repetition in range(1, REPETITIONS + 1)
    ]


def run_matrix(output_path: Path = DEFAULT_OUTPUT_PATH) -> dict[str, Any]:
    api_key, model, base_url = provider_config()
    state = _load_state(output_path, model, base_url)
    _ensure_new_stage(state, "matrix")
    if state.get("stages", {}).get("preflight", {}).get("status") != "PASS":
        raise RuntimeError("matrix requires PREFLIGHT_PASS")
    if state.get("stages", {}).get("sanity", {}).get("status") != "PASS":
        raise RuntimeError("matrix requires PROVIDER_SANITY_GATE_PASS")
    cases = load_cases()
    schedule = _matrix_schedule(cases)
    if len(schedule) != MAX_MATRIX_REQUESTS:
        raise RuntimeError("fixed matrix no longer matches the 80-request contract")
    stage: dict[str, Any] = {
        "status": "RUNNING",
        "request_count": 0,
        "planned_request_slots": MAX_MATRIX_REQUESTS,
        "retry_used": False,
        "stopped_reason": None,
    }
    state["stages"]["matrix"] = stage
    _save_state(output_path, state)

    technical_streak = 0
    empty_streak = 0
    stop_reason: str | None = None
    schedule_completed = 0

    def call_slot(
        version: str,
        unit: list[dict[str, Any]],
        repetition: int,
        retry_of: int | None = None,
    ) -> tuple[dict[str, Any], str | None]:
        return _perform_request(
            state,
            output_path,
            prompt=build_prompt(version, unit),
            api_key=api_key,
            model=model,
            base_url=base_url,
            stage="matrix",
            version=version,
            case_ids=[case["id"] for case in unit],
            repetition=repetition,
            retry_of=retry_of,
        )

    for version, unit, repetition in schedule:
        if stage["request_count"] >= MAX_MATRIX_REQUESTS:
            stop_reason = "MATRIX_REQUEST_CAP_REACHED_AFTER_RETRY"
            break
        prior_technical_streak = technical_streak
        row, raw = call_slot(version, unit, repetition)
        stage["request_count"] += 1
        category = row["output_classification"]
        technical_streak, empty_streak, should_stop = update_failure_streaks(
            category,
            technical_streak=technical_streak,
            empty_streak=empty_streak,
        )
        chosen_row, chosen_raw = row, raw
        if should_stop:
            _record_case_results(
                state, unit=unit, raw=raw, category=category, row=row
            )
            stop_reason = "TWO_CONSECUTIVE_PROVIDER_TECHNICAL_FAILURES"
            _save_state(output_path, state)
            break

        if (
            category == "TRANSPORT_ERROR"
            and prior_technical_streak == 0
            and not stage["retry_used"]
            and stage["request_count"] < MAX_MATRIX_REQUESTS
            and state["new_provider_requests"] < MAX_TOTAL_PROVIDER_REQUESTS
        ):
            stage["retry_used"] = True
            retry_row, retry_raw = call_slot(
                version, unit, repetition, retry_of=row["request_index"]
            )
            stage["request_count"] += 1
            retry_category = retry_row["output_classification"]
            technical_streak, empty_streak, should_stop = update_failure_streaks(
                retry_category,
                technical_streak=technical_streak,
                empty_streak=empty_streak,
            )
            chosen_row, chosen_raw, category = retry_row, retry_raw, retry_category
            if should_stop:
                _record_case_results(
                    state, unit=unit, raw=retry_raw, category=retry_category, row=retry_row
                )
                stop_reason = "TWO_CONSECUTIVE_PROVIDER_TECHNICAL_FAILURES"
                _save_state(output_path, state)
                break

        _record_case_results(
            state, unit=unit, raw=chosen_raw, category=category, row=chosen_row
        )
        schedule_completed += 1
        _save_state(output_path, state)
    else:
        stop_reason = None

    complete = schedule_completed == len(schedule)
    if complete:
        stage["status"] = "COMPLETE"
    elif stop_reason == "MATRIX_REQUEST_CAP_REACHED_AFTER_RETRY":
        stage["status"] = "PARTIAL_REQUEST_CAP"
    else:
        stage["status"] = "PARTIAL_PROVIDER_STOP"
    stage["stopped_reason"] = stop_reason
    stage["logical_request_slots_completed"] = schedule_completed
    state["summary"] = summarize_state(state, cases)
    _save_state(output_path, state)
    return {
        "status": stage["status"],
        "request_count": stage["request_count"],
        "logical_request_slots_completed": schedule_completed,
        "planned_request_slots": MAX_MATRIX_REQUESTS,
        "stopped_reason": stop_reason,
        "summary": state["summary"],
    }


def offline_plan() -> dict[str, Any]:
    cases = load_cases()
    units = evaluation_units(cases)
    return {
        "mode": "offline-plan",
        "classification": "MICRO_EVAL_ONLY",
        "logical_cases": len(cases),
        "request_units": len(units),
        "planned_matrix_provider_requests": len(units) * 2 * REPETITIONS,
        "preflight_cap": PREFLIGHT_REQUEST_CAP,
        "sanity_cap": SANITY_REQUEST_CAP,
        "matrix_cap": MAX_MATRIX_REQUESTS,
        "absolute_new_request_cap": MAX_TOTAL_PROVIDER_REQUESTS,
        "request_contract": REQUEST_CONTRACT,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-provider", action="store_true", help="send provider-only requests")
    parser.add_argument(
        "--stage",
        choices=("preflight", "sanity", "matrix"),
        default="preflight",
        help="run one gated stage; matrix requires both earlier stages to pass",
    )
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_PATH)
    args = parser.parse_args()
    if not args.run_provider:
        print(json.dumps(offline_plan(), indent=2, ensure_ascii=False))
        return 0
    try:
        if args.stage == "preflight":
            result = run_preflight(args.output)
        elif args.stage == "sanity":
            result = run_sanity(args.output)
        else:
            result = run_matrix(args.output)
    except RuntimeError as exc:
        if str(exc) == "provider credential unavailable":
            print("BEHAVIORAL_EVAL_PROVIDER_PATH_UNAVAILABLE")
            return 2
        if str(exc) == "provider target does not match verified alias and endpoint":
            print("PROVIDER_TARGET_UNVERIFIED")
            return 2
        print(json.dumps({"status": "STOPPED", "reason": str(exc)}, ensure_ascii=False))
        return 2
    print(json.dumps(result, indent=2, ensure_ascii=False))
    if result.get("status") in {"FAIL", "PARTIAL_PROVIDER_STOP", "PARTIAL_REQUEST_CAP"}:
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
