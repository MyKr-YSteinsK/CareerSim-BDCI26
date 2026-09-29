import ast
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import skill_behavior_eval as eval_tool  # noqa: E402


def test_case_loader_and_fixed_case_set():
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


def test_case_loader_rejects_invalid_schema(tmp_path):
    path = tmp_path / "bad.json"
    path.write_text('{"schema_version":99,"cases":[]}', encoding="utf-8")
    try:
        eval_tool.load_cases(path)
    except ValueError as exc:
        assert "Unsupported eval case schema" in str(exc)
    else:
        raise AssertionError("invalid eval schema must be rejected")


def test_delivery_identity_pair_bundles_to_respect_80_request_cap():
    units = eval_tool.evaluation_units(eval_tool.load_cases())
    assert len(units) == 20
    assert len([unit for unit in units if len(unit) == 2]) == 1
    assert len(units) * 2 * eval_tool.REPETITIONS == 80


def test_rewrite_and_current_integrated_prompts_load_their_own_text():
    cases = [next(case for case in eval_tool.load_cases() if case["id"] == "X2_ADVANCE_ANCHOR_CONFLICT")]
    current = eval_tool.build_prompt("current", cases)
    rewrite = eval_tool.build_prompt("rewrite", cases)
    assert '"name": "candidate-v7n-public-state-delivery-constraint-hardening"' in current
    assert '"name": "experimental-s07-50-skill-authoring-rewrite"' in rewrite
    assert "experimental-s07-50-skill-authoring-rewrite" in rewrite
    assert "step 1 — constraint gate" in rewrite.casefold()
    assert current != rewrite


def test_json_parser_and_critical_grading():
    case = next(case for case in eval_tool.load_cases() if case["id"] == "P1_ACUTE_TO_S")
    raw = '{"BINDING_CONSTRAINT":"YES","MODE":"S","GAP":"safety","CANDIDATE":"pause"}'
    grade = eval_tool.grade_case(case, json.loads(raw), raw)
    assert grade["status"] == "PASS"
    assert eval_tool.parse_json_output("```json\n" + raw + "\n```") == json.loads(raw)
    delivery_case = next(case for case in eval_tool.load_cases() if case["id"] == "D1_PRAISE_NOT_VERIFICATION")
    missing = eval_tool.grade_case(delivery_case, {"items": {}}, "{\"items\":{}}")
    assert missing["status"] == "FAIL"


def test_repetition_classification_preserves_technical_unknown():
    assert eval_tool.classify_repetitions([{"grade": {"status": "PASS"}}, {"grade": {"status": "PASS"}}]) == "SYSTEMATIC_PASS"
    assert eval_tool.classify_repetitions([{"grade": {"status": "PASS"}}, {"grade": {"status": "FAIL"}}]) == "FRAGILE"
    assert eval_tool.classify_repetitions([{"grade": {"status": "FAIL"}}, {"grade": {"status": "FAIL"}}]) == "FAIL"
    assert eval_tool.classify_repetitions([{"grade": {"status": "PASS"}}, {"grade": {"status": "TECHNICAL_UNKNOWN"}}]) == "TECHNICAL_UNKNOWN"


def test_secret_redaction_never_returns_the_value():
    secret = "synthetic-secret-value"
    redacted = eval_tool.redact_secrets(f"Authorization: Bearer {secret}; api_key={secret}", [secret])
    assert secret not in redacted
    assert redacted.count("[REDACTED]") >= 2


def test_provider_request_requires_credential_without_reading_other_runtime_state(monkeypatch):
    monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)
    try:
        eval_tool.provider_config()
    except RuntimeError as exc:
        assert str(exc) == "provider credential unavailable"
    else:
        raise AssertionError("provider config should fail closed without a credential")


def test_provider_config_uses_non_secret_alias_defaults(monkeypatch):
    monkeypatch.setenv("DEEPSEEK_API_KEY", "synthetic-secret-value")
    monkeypatch.delenv("MODEL_NAME", raising=False)
    monkeypatch.delenv("API_BASE", raising=False)
    monkeypatch.delenv("SKILL_EVAL_MODEL", raising=False)
    monkeypatch.delenv("SKILL_EVAL_API_BASE", raising=False)
    key, model, base = eval_tool.provider_config()
    assert key == "synthetic-secret-value"
    assert model == "deepseek-flash"
    assert base == "https://api.deepseek.com"


def test_rewrite_sections_and_example_limits():
    expected = {
        "structured-state-board.SKILL.md": ("## Boundary examples", 3),
        "rolling-planning.SKILL.md": ("## Boundary examples", 4),
        "delivery-progress.SKILL.md": ("## Boundary examples", 4),
        "risk-review.SKILL.md": ("## Boundary examples", 4),
    }
    folder = ROOT / "experiments" / "s07-50" / "rewrite"
    for name, (section, count) in expected.items():
        text = (folder / name).read_text(encoding="utf-8")
        assert text.startswith("---\nname:")
        assert section in text
        example_block = text.split(section, 1)[1].split("\n## ", 1)[0]
        assert sum(line.startswith("- ") for line in example_block.splitlines()) == count


def test_harness_has_no_game_or_database_side_effect_clients():
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
