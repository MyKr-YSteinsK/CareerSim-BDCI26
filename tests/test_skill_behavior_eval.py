import ast
import json
import sys
import urllib.error
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import skill_behavior_eval as eval_tool  # noqa: E402


def _success_observation(content, *, finish_reason="stop", reasoning="private-reasoning"):
    payload = {
        "model": "deepseek-flash",
        "choices": [
            {
                "finish_reason": finish_reason,
                "message": {"content": content, "reasoning_content": reasoning},
            }
        ],
        "usage": {
            "prompt_tokens": 31,
            "completion_tokens": 22,
            "total_tokens": 53,
            "completion_tokens_details": {"reasoning_tokens": 17 if reasoning else 0},
        },
    }
    return {"metadata": eval_tool._extract_response(payload, 200)["metadata"], "observable_content": content}


def test_fixed_public_only_case_set_and_request_budget():
    cases = eval_tool.load_cases()
    ids = {case["id"] for case in cases}
    assert len(cases) == 21
    assert {
        "B1_WEALTH_COPY_TRAP", "B2_MIXED_ATTRIBUTION", "B3_ACUTE_WARNING",
        "B4_INTERNAL_NUMERIC_BAIT", "P1_ACUTE_TO_S", "P2_MILD_TO_A",
        "P3_RESOLVED_BACK_TO_NORMAL", "P4_REVIEW_GAP_STABILITY",
        "D1_PRAISE_NOT_VERIFICATION", "D2_ADOPTION_IS_VERIFICATION",
        "D3_TOOL_SUCCESS_NOT_RESULT", "D4_RETIRE_COMPLETED_ITEM", "D5_ID_CONTINUITY",
        "R1_ORDINARY_PASS", "R2_ACUTE_BAD_CANDIDATE", "R3_ACUTE_SAFE_CANDIDATE",
        "R4_COMPLIANCE_SAFE_CANDIDATE", "X1_HIDDEN_NUMERIC_BAIT",
        "X2_ADVANCE_ANCHOR_CONFLICT", "X3_DELIVERY_TO_PLANNING", "X4_FULL_REVIEW_LABEL",
    } == ids
    assert len(eval_tool.evaluation_units(cases)) == 20
    assert eval_tool.offline_plan()["planned_matrix_provider_requests"] == 80
    assert eval_tool.MAX_TOTAL_PROVIDER_REQUESTS == 85


def test_case_loader_rejects_invalid_schema(tmp_path):
    path = tmp_path / "bad.json"
    path.write_text('{"schema_version":99,"cases":[]}', encoding="utf-8")
    try:
        eval_tool.load_cases(path)
    except ValueError as exc:
        assert "Unsupported eval case schema" in str(exc)
    else:
        raise AssertionError("invalid eval schema must be rejected")


def test_request_contract_uses_explicit_official_default_thinking_and_json():
    payload = eval_tool.request_payload("deepseek-flash", "return JSON")
    assert payload["thinking"] == {"type": "enabled"}
    assert payload["reasoning_effort"] == "high"
    assert payload["max_tokens"] == 4096
    assert payload["response_format"] == {"type": "json_object"}
    assert payload["stream"] is False
    assert "temperature" not in payload
    assert eval_tool.REQUEST_CONTRACT["thinking_condition"] == "OFFICIAL_DEFAULT_THINKING"
    assert eval_tool.REQUEST_CONTRACT["runtime_equivalence"] == "RUNTIME_MODE_NOT_VERIFIED"


def test_request_completion_keeps_safe_metadata_but_never_reasoning_text(monkeypatch):
    payload = {
        "model": "deepseek-flash",
        "choices": [{
            "finish_reason": "stop",
            "message": {
                "content": '{"status":"OK"}',
                "reasoning_content": "NEVER_PERSIST_THIS_PRIVATE_REASONING",
            },
        }],
        "usage": {
            "prompt_tokens": 12,
            "completion_tokens": 34,
            "total_tokens": 46,
            "completion_tokens_details": {"reasoning_tokens": 29},
        },
    }

    class FakeResponse:
        status = 200

        def __enter__(self):
            return self

        def __exit__(self, *_args):
            return False

        def read(self):
            return json.dumps(payload).encode("utf-8")

    class FakeOpener:
        def open(self, _request, timeout):
            assert timeout == eval_tool.REQUEST_TIMEOUT_SECONDS
            return FakeResponse()

    monkeypatch.setattr(eval_tool.urllib.request, "build_opener", lambda *_args: FakeOpener())
    observation = eval_tool.request_completion(
        "json prompt", api_key="synthetic-secret", model="deepseek-flash", base_url="https://api.deepseek.com"
    )
    metadata = observation["metadata"]
    assert observation["observable_content"] == '{"status":"OK"}'
    assert metadata == {
        "http_success": True,
        "http_status": 200,
        "provider_reported_model": "deepseek-flash",
        "finish_reason": "stop",
        "content_present": True,
        "content_chars": len('{"status":"OK"}'),
        "reasoning_content_present": True,
        "reasoning_chars": len("NEVER_PERSIST_THIS_PRIVATE_REASONING"),
        "prompt_tokens": 12,
        "completion_tokens": 34,
        "reasoning_tokens": 29,
        "total_tokens": 46,
    }
    assert "NEVER_PERSIST_THIS_PRIVATE_REASONING" not in json.dumps(observation)
    assert "reasoning_content" not in observation


def test_http_and_transport_failures_capture_status_without_body(monkeypatch):
    class FakeOpener:
        def __init__(self, error):
            self.error = error

        def open(self, *_args, **_kwargs):
            raise self.error

    http_error = urllib.error.HTTPError(
        "https://api.deepseek.com/chat/completions", 429, "rate limited", None, None
    )
    monkeypatch.setattr(
        eval_tool.urllib.request, "build_opener", lambda *_args: FakeOpener(http_error)
    )
    result = eval_tool.request_completion(
        "prompt", api_key="not-printed", model="deepseek-flash", base_url="https://api.deepseek.com"
    )
    assert result["failure_kind"] == "HTTP_ERROR"
    assert result["metadata"]["http_status"] == 429
    assert not result["metadata"]["http_success"]
    assert "rate limited" not in json.dumps(result)

    monkeypatch.setattr(
        eval_tool.urllib.request,
        "build_opener",
        lambda *_args: FakeOpener(urllib.error.URLError("connection reset")),
    )
    result = eval_tool.request_completion(
        "prompt", api_key="not-printed", model="deepseek-flash", base_url="https://api.deepseek.com"
    )
    assert eval_tool.classify_observation(result) == "TRANSPORT_ERROR"
    assert "connection reset" not in json.dumps(result)


def test_empty_content_classification_uses_finish_and_reasoning_metadata():
    cases = [
        (_success_observation("", finish_reason="length", reasoning=""), "EMPTY_CONTENT_LENGTH"),
        (_success_observation("", finish_reason="stop", reasoning="private-reasoning"), "EMPTY_CONTENT_WITH_REASONING"),
        (_success_observation("", finish_reason="stop", reasoning=""), "EMPTY_CONTENT_OTHER"),
    ]
    for observation, expected in cases:
        assert eval_tool.classify_observation(observation) == expected
        assert observation["metadata"]["http_success"] is True
        assert observation["observable_content"] == ""


def test_nonempty_json_and_unparseable_output_have_distinct_categories():
    valid = _success_observation('{"MODE":"S"}')
    invalid = _success_observation("MODE=S")
    assert eval_tool.classify_observation(valid) == "VALID_OBSERVABLE_OUTPUT"
    assert eval_tool.classify_observation(invalid) == "UNPARSEABLE_OBSERVABLE_OUTPUT"
    assert eval_tool.classify_observation(
        _success_observation('{"partial":', finish_reason="length")
    ) == "TRUNCATED_OUTPUT"


def test_http_200_empty_is_technical_unknown_not_behavioral_fail():
    case = next(case for case in eval_tool.load_cases() if case["id"] == "B1_WEALTH_COPY_TRAP")
    observation = _success_observation("", finish_reason="stop", reasoning="")
    category = eval_tool.classify_observation(observation)
    assert category == "EMPTY_CONTENT_OTHER"
    grade = {
        "status": "TECHNICAL_UNKNOWN" if category in eval_tool.TECHNICAL_CATEGORIES else "FAIL",
        "passed": False,
    }
    assert grade["status"] == "TECHNICAL_UNKNOWN"
    assert case["critical"]


def test_two_consecutive_empty_or_technical_failures_stop_and_empty_does_not_reset():
    technical, empty, stop = eval_tool.update_failure_streaks(
        "EMPTY_CONTENT_OTHER", technical_streak=0, empty_streak=0
    )
    assert (technical, empty, stop) == (1, 1, False)
    technical, empty, stop = eval_tool.update_failure_streaks(
        "TRANSPORT_ERROR", technical_streak=technical, empty_streak=empty
    )
    assert (technical, empty, stop) == (2, 0, True)

    technical, empty, stop = eval_tool.update_failure_streaks(
        "EMPTY_CONTENT_WITH_REASONING", technical_streak=0, empty_streak=0
    )
    technical, empty, stop = eval_tool.update_failure_streaks(
        "EMPTY_CONTENT_LENGTH", technical_streak=technical, empty_streak=empty
    )
    assert stop and technical == 2 and empty == 2

    technical, empty, stop = eval_tool.update_failure_streaks(
        "TRANSPORT_ERROR", technical_streak=0, empty_streak=0
    )
    technical, empty, stop = eval_tool.update_failure_streaks(
        "HTTP_ERROR", technical_streak=technical, empty_streak=empty
    )
    assert stop and technical == 2

    technical, empty, stop = eval_tool.update_failure_streaks(
        "VALID_OBSERVABLE_OUTPUT", technical_streak=1, empty_streak=1
    )
    assert (technical, empty, stop) == (0, 0, False)


def test_preflight_requires_exact_compact_json_and_no_truncation():
    assert eval_tool.parse_json_output('{"status":"OK"}') == {"status": "OK"}
    fence = chr(96) * 3
    assert eval_tool.parse_json_output(f"{fence}json\n{{'status':'OK'}}\n{fence}") is None
    row = {"output_classification": "VALID_OBSERVABLE_OUTPUT", "finish_reason": "length"}
    parsed = {"status": "OK"}
    passed = (
        row["output_classification"] == "VALID_OBSERVABLE_OUTPUT"
        and parsed == {"status": "OK"}
        and row.get("finish_reason") != "length"
    )
    assert not passed


def test_sanity_and_matrix_are_gated_by_prior_stage_status(tmp_path, monkeypatch):
    output = tmp_path / "state.json"
    monkeypatch.setattr(
        eval_tool, "provider_config",
        lambda: ("synthetic-secret", "deepseek-flash", "https://api.deepseek.com"),
    )
    state = eval_tool._new_state("deepseek-flash", "https://api.deepseek.com")
    state["stages"]["preflight"] = {"status": "FAIL"}
    eval_tool._save_state(output, state)
    calls = []
    monkeypatch.setattr(eval_tool, "request_completion", lambda *_args, **_kwargs: calls.append(1))
    try:
        eval_tool.run_sanity(output)
    except RuntimeError as exc:
        assert "PREFLIGHT_PASS" in str(exc)
    else:
        raise AssertionError("sanity must require preflight")
    try:
        eval_tool.run_matrix(output)
    except RuntimeError as exc:
        assert "PREFLIGHT_PASS" in str(exc)
    else:
        raise AssertionError("matrix must require preflight and sanity")
    assert calls == []


def _matrix_state(path):
    state = eval_tool._new_state("deepseek-flash", "https://api.deepseek.com")
    state["stages"]["preflight"] = {"status": "PASS"}
    state["stages"]["sanity"] = {"status": "PASS"}
    eval_tool._save_state(path, state)
    return state


def test_matrix_stops_after_two_consecutive_empty_responses(tmp_path, monkeypatch):
    output = tmp_path / "matrix-empty.json"
    _matrix_state(output)
    monkeypatch.setattr(
        eval_tool, "provider_config",
        lambda: ("synthetic-secret", "deepseek-flash", "https://api.deepseek.com"),
    )
    calls = []

    def empty_response(*_args, **_kwargs):
        calls.append(1)
        return _success_observation("", reasoning="")

    monkeypatch.setattr(eval_tool, "request_completion", empty_response)
    result = eval_tool.run_matrix(output)
    saved = json.loads(output.read_text(encoding="utf-8"))
    assert result["status"] == "PARTIAL_PROVIDER_STOP"
    assert result["stopped_reason"] == "TWO_CONSECUTIVE_PROVIDER_TECHNICAL_FAILURES"
    assert result["request_count"] == 2
    assert len(calls) == 2
    assert saved["new_provider_requests"] == 2
    assert saved["requests"][0]["http_success"] is True
    assert saved["requests"][0]["output_classification"] == "EMPTY_CONTENT_OTHER"


def test_matrix_retries_one_isolated_transport_error_then_stops_on_second(tmp_path, monkeypatch):
    output = tmp_path / "matrix-transport.json"
    _matrix_state(output)
    monkeypatch.setattr(
        eval_tool, "provider_config",
        lambda: ("synthetic-secret", "deepseek-flash", "https://api.deepseek.com"),
    )
    calls = []

    def transport_error(*_args, **_kwargs):
        calls.append(1)
        return {
            "metadata": eval_tool._empty_response_metadata(None, False),
            "failure_kind": "TRANSPORT_ERROR",
            "observable_content": None,
        }

    monkeypatch.setattr(eval_tool, "request_completion", transport_error)
    result = eval_tool.run_matrix(output)
    saved = json.loads(output.read_text(encoding="utf-8"))
    assert result["status"] == "PARTIAL_PROVIDER_STOP"
    assert result["request_count"] == 2
    assert len(calls) == 2
    assert saved["requests"][1]["retry_of_request_index"] == saved["requests"][0]["request_index"]
    assert saved["stages"]["matrix"]["retry_used"] is True
    assert saved["new_provider_requests"] == 2


def test_preflight_then_sanity_gate_persists_only_safe_response_data(tmp_path, monkeypatch):
    output = tmp_path / "state.json"
    secret = "synthetic-secret-do-not-write"
    monkeypatch.setattr(
        eval_tool, "provider_config",
        lambda: (secret, "deepseek-flash", "https://api.deepseek.com"),
    )

    def fake_request(prompt, **_kwargs):
        if '"status"' in prompt and '"OK"' in prompt:
            return _success_observation('{"status":"OK"}', reasoning="never-store-this")
        return _success_observation(
            '{"STATE":{"W":"4"},"STICKY":"","EFFECTS":"UNKNOWN"}', reasoning="never-store-this"
        )

    monkeypatch.setattr(eval_tool, "request_completion", fake_request)
    assert eval_tool.run_preflight(output)["gate"] == "PREFLIGHT_PASS"
    sanity = eval_tool.run_sanity(output)
    assert sanity["gate"] == "PROVIDER_SANITY_GATE_PASS"
    assert sanity["request_count"] == 4
    saved = output.read_text(encoding="utf-8")
    assert secret not in saved
    assert "never-store-this" not in saved
    decoded = json.loads(saved)
    assert decoded["new_provider_requests"] == 5
    assert all(row["request_state"] == "COMPLETED" for row in decoded["requests"])


def test_absolute_total_and_matrix_caps_cannot_be_exceeded(tmp_path):
    path = tmp_path / "state.json"
    state = eval_tool._new_state("deepseek-flash", "https://api.deepseek.com")
    state["new_provider_requests"] = eval_tool.MAX_TOTAL_PROVIDER_REQUESTS
    eval_tool._save_state(path, state)
    loaded = eval_tool._load_state(path, "deepseek-flash", "https://api.deepseek.com")
    try:
        eval_tool._start_request(loaded, path, stage="matrix")
    except RuntimeError as exc:
        assert "absolute provider request cap" in str(exc)
    else:
        raise AssertionError("total cap must be hard")
    assert eval_tool.MAX_MATRIX_REQUESTS == 80
    assert eval_tool.PREFLIGHT_REQUEST_CAP + eval_tool.SANITY_REQUEST_CAP + eval_tool.MAX_MATRIX_REQUESTS == 85


def test_unresolved_in_flight_request_blocks_duplicate_provider_call(tmp_path):
    path = tmp_path / "state.json"
    state = eval_tool._new_state("deepseek-flash", "https://api.deepseek.com")
    state["requests"] = [{"request_index": 1, "request_state": "IN_FLIGHT"}]
    state["new_provider_requests"] = 1
    eval_tool._save_state(path, state)
    try:
        eval_tool._load_state(path, "deepseek-flash", "https://api.deepseek.com")
    except RuntimeError as exc:
        assert "unresolved in-flight outcome" in str(exc)
    else:
        raise AssertionError("unknown provider outcome must not be blindly repeated")


def test_rewrite_and_formal_candidate_boundaries_are_separate():
    cases = [next(case for case in eval_tool.load_cases() if case["id"] == "X2_ADVANCE_ANCHOR_CONFLICT")]
    current = eval_tool.build_prompt("current", cases)
    rewrite = eval_tool.build_prompt("rewrite", cases)
    assert '"name": "candidate-v7n-public-state-delivery-constraint-hardening"' in current
    assert '"name": "experimental-s07-50-skill-authoring-rewrite"' in rewrite
    assert "step 1 — constraint gate" in rewrite.casefold()
    assert current != rewrite
    identity = json.loads((ROOT / "configs" / "current_candidate.json").read_text(encoding="utf-8"))
    assert identity["candidate_id"] == "candidate-v7w-high-score-core-recovery"
    assert eval_tool.EXPERIMENT == ROOT / "experiments" / "s07-50"
    assert eval_tool.DEFAULT_OUTPUT_PATH == ROOT / "experiments" / "s07-50r" / "evals" / "provider_results.json"


def test_secret_redaction_and_state_guard():
    secret = "synthetic-secret-value"
    redacted = eval_tool.redact_secrets(
        f"Authorization: Bearer {secret}; api_key={secret}", [secret]
    )
    assert secret not in redacted
    assert redacted.count("[REDACTED]") >= 2
    try:
        eval_tool._assert_safe_state({"reasoning_content": "private"})
    except ValueError as exc:
        assert "prohibited provider field" in str(exc)
    else:
        raise AssertionError("reasoning text must never be persisted")


def test_harness_has_no_game_database_or_framework_side_effect_clients():
    source = (ROOT / "scripts" / "skill_behavior_eval.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    imported = {
        alias.name.split(".")[0]
        for node in ast.walk(tree)
        if isinstance(node, (ast.Import, ast.ImportFrom))
        for alias in node.names
    }
    assert not imported.intersection({"subprocess", "sqlite3", "requests", "httpx"})
    assert "DEEPSEEK_API_KEY" in source
    for forbidden in ("new_game", "take_action", "career_emu", "shared_db", "sqlite3"):
        assert forbidden not in source
