"""Bounded public-only behavioral evaluation for isolated Skill copies.

Provider requests are opt-in (`--run-provider`) and use a direct OpenAI-compatible
HTTPS request. This module never starts a local runtime or reads gameplay data.
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
MAX_PROVIDER_REQUESTS = 80
REPETITIONS = 2
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
    """Bundle only the paired Delivery identity cases to fit the strict 80-call cap."""
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    units: list[list[dict[str, Any]]] = []
    for case in cases:
        group = case.get("request_group")
        if group:
            groups[group].append(case)
        else:
            units.append([case])
    for group_cases in groups.values():
        units.append(group_cases)
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
    candidate = raw.strip()
    if candidate.startswith("```"):
        candidate = re.sub(r"^```(?:json)?\s*|\s*```$", "", candidate, flags=re.I)
    try:
        return json.loads(candidate)
    except json.JSONDecodeError:
        match = re.search(r"\{[\s\S]*\}", candidate)
        if not match:
            return None
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            return None


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
            passed = str(expected).casefold() not in (actual if isinstance(actual, str) else json.dumps(actual, ensure_ascii=False)).casefold()
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
    # The non-secret default pair matches the accepted local run configuration;
    # overrides use names only and values are never printed.
    model = os.environ.get("SKILL_EVAL_MODEL") or os.environ.get("MODEL_NAME") or "deepseek-flash"
    base = os.environ.get("SKILL_EVAL_API_BASE") or os.environ.get("API_BASE") or "https://api.deepseek.com"
    return api_key, model, base.rstrip("/")


def request_completion(prompt: str, *, api_key: str, model: str, base_url: str, timeout: int = 90) -> tuple[str, str | None]:
    body = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0,
        "max_tokens": 500,
        "stream": False,
    }).encode("utf-8")
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
    with opener.open(request, timeout=timeout) as response:
        payload = json.loads(response.read().decode("utf-8"))
    return str(payload["choices"][0]["message"]["content"]), payload.get("model")


def run_provider(*, max_requests: int = MAX_PROVIDER_REQUESTS, output_path: Path | None = None) -> dict[str, Any]:
    cases = load_cases()
    units = evaluation_units(cases)
    planned = len(units) * 2 * REPETITIONS
    if planned > min(max_requests, MAX_PROVIDER_REQUESTS):
        raise ValueError(f"planned provider requests exceed hard cap: {planned}")
    api_key, model, base_url = provider_config()
    rows: list[dict[str, Any]] = []
    requests_made = 0
    consecutive_failures = 0
    stopped_early = False
    safe_secrets = [api_key]

    def save_progress() -> None:
        if output_path:
            snapshot = {
                "classification": "MICRO_EVAL_ONLY",
                "model_alias": model,
                "endpoint_host": re.sub(r"^https?://", "", base_url).split("/")[0],
                "provider_requests": requests_made,
                "planned_provider_requests": planned,
                "technical_failures": sum(1 for row in rows if "technical_failure" in row),
                "stopped_early": stopped_early,
                "summary": summarize_rows(rows, cases),
                "rows": rows,
            }
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(json.dumps(snapshot, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    for version in ("current", "rewrite"):
        for unit in units:
            prompt = build_prompt(version, unit)
            for repetition in range(1, REPETITIONS + 1):
                if requests_made >= min(max_requests, MAX_PROVIDER_REQUESTS):
                    stopped_early = True
                    break
                requests_made += 1
                row_base = {
                    "version": version,
                    "case_ids": [case["id"] for case in unit],
                    "repetition": repetition,
                    "request_index": requests_made,
                }
                try:
                    raw, response_model = request_completion(prompt, api_key=api_key, model=model, base_url=base_url)
                except (urllib.error.URLError, TimeoutError, OSError, KeyError, ValueError) as exc:
                    code = getattr(exc, "code", None)
                    rows.append({**row_base, "technical_failure": type(exc).__name__, "http_status": code})
                    save_progress()
                    consecutive_failures += 1
                    if consecutive_failures >= 2:
                        stopped_early = True
                        break
                    # One bounded retry is permitted; it is already the next scheduled repetition.
                    continue
                consecutive_failures = 0
                safe_raw = redact_secrets(raw, safe_secrets)
                parsed = parse_json_output(safe_raw)
                for case in unit:
                    if len(unit) == 1:
                        answer = parsed
                    elif isinstance(parsed, dict):
                        answer = parsed.get(case["id"])
                    else:
                        answer = None
                    grade = grade_case(case, answer, safe_raw)
                    rows.append({
                        **row_base,
                        "case_id": case["id"],
                        "provider_reported_model": response_model,
                        "observable_output": safe_raw,
                        "output_chars": len(safe_raw),
                        "grade": grade,
                    })
                save_progress()
            if stopped_early:
                break
        if stopped_early:
            break

    summary = summarize_rows(rows, cases)
    result = {
        "classification": "MICRO_EVAL_ONLY",
        "model_alias": model,
        "endpoint_host": re.sub(r"^https?://", "", base_url).split("/")[0],
        "provider_requests": requests_made,
        "planned_provider_requests": planned,
        "technical_failures": sum(1 for row in rows if "technical_failure" in row),
        "stopped_early": stopped_early,
        "summary": summary,
        "rows": rows,
    }
    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return result


def summarize_rows(rows: list[dict[str, Any]], cases: list[dict[str, Any]]) -> dict[str, Any]:
    case_by_id = {case["id"]: case for case in cases}
    outcome: dict[str, Any] = {}
    length_by_version_skill: dict[str, dict[str, list[int]]] = defaultdict(lambda: defaultdict(list))
    for row in rows:
        if "case_id" not in row:
            continue
        case_id = row["case_id"]
        version = row["version"]
        skill = case_by_id[case_id]["skill"]
        outcome.setdefault(case_id, {}).setdefault(version, []).append(row)
        length_by_version_skill[version][skill].append(row["output_chars"])
    classifications = {}
    for case in cases:
        case_id = case["id"]
        classifications[case_id] = {}
        for version in ("current", "rewrite"):
            classifications[case_id][version] = classify_repetitions(outcome.get(case_id, {}).get(version, [])) if len(outcome.get(case_id, {}).get(version, [])) == 2 else "TECHNICAL_UNKNOWN"
    medians = {
        version: {
            skill: statistics.median(values) if values else None
            for skill, values in by_skill.items()
        }
        for version, by_skill in length_by_version_skill.items()
    }
    return {"case_classifications": classifications, "median_output_chars_by_version_and_skill": medians}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-provider", action="store_true", help="send bounded provider-only micro-eval requests")
    parser.add_argument("--max-requests", type=int, default=MAX_PROVIDER_REQUESTS)
    parser.add_argument("--output", type=Path, default=EXPERIMENT / "evals" / "provider_results.json")
    args = parser.parse_args()
    cases = load_cases()
    units = evaluation_units(cases)
    planned = len(units) * 2 * REPETITIONS
    if planned > MAX_PROVIDER_REQUESTS or args.max_requests > MAX_PROVIDER_REQUESTS:
        parser.error("provider request limit may not exceed 80")
    if not args.run_provider:
        print(json.dumps({"mode": "offline-plan", "logical_cases": len(cases), "request_units": len(units), "planned_provider_requests": planned, "hard_cap": MAX_PROVIDER_REQUESTS}, indent=2))
        return 0
    try:
        result = run_provider(max_requests=args.max_requests, output_path=args.output)
    except RuntimeError as exc:
        if str(exc) == "provider credential unavailable":
            print("BEHAVIORAL_EVAL_PROVIDER_PATH_UNAVAILABLE")
            return 2
        raise
    print(json.dumps({key: value for key, value in result.items() if key != "rows"}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
