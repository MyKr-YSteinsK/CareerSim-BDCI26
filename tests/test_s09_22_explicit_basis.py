"""Certificate v3: explicit annotations, never arbitrary-prose truth inference."""
import hashlib
import json
from pathlib import Path
import subprocess

import pytest
from scripts.basis_preflight_audit import check_basis, measure_receipts, parse_five_marker_header

ROOT = Path(__file__).resolve().parents[1]
BASE = '787d2b051cc8bb106a9355748a6f20edb8a4a188'


def load(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8'))


CASES = load('tests/fixtures/v10e_explicit_basis_cases.json')
EVIDENCE = CASES[0]['evidence']


@pytest.mark.parametrize('case', CASES, ids=lambda c: c['name'])
def test_explicit_semantic_scenarios(case):
    result = check_basis(case['notes'], case['evidence'])
    assert result['status'] == case['expected']
    assert result['may_submit'] == (case['expected'] == 'PASS')
    if case['reason']:
        assert result['reasons'][0] == case['reason']


@pytest.mark.parametrize('case', load('tests/fixtures/v10d_five_marker_header.json'), ids=lambda c: c['name'])
def test_s09_21_layout_preserved_under_explicit_serialization_projection(case):
    # Change certificate only; prefixes, gaps, duplicates and omissions remain.
    notes = case['notes'].replace('[BC=PASS]', '[BC=PASS S=NONE CAP=NONE]')
    result = check_basis(notes, EVIDENCE)
    assert result['status'] == case['expected']
    assert parse_five_marker_header(notes)['valid'] == result['may_submit']
    if case['expected'] == 'BLOCKED':
        assert 'SCHEMA' in result['reasons']


def project_legacy(case):
    """Explicit test adapter; does not rewrite archived historical fixtures."""
    e = dict(case['evidence'])
    s = 'ACUTE' if e.get('fresh_material_binding') is True else 'NONE'
    if s != 'NONE':
        e['public_binding_class'] = s
    cap = 'PUBLIC_SCOPED' if e.get('saturation_claim') is True else 'NONE'
    return case['notes'] + f' [BC=PASS S={s} CAP={cap}]', e


@pytest.mark.parametrize('case', load('tests/fixtures/v10c_kernel_cases.json'), ids=lambda c: c['name'])
def test_existing_kernel_annotations_preserved(case):
    notes, evidence = project_legacy(case)
    result = check_basis(notes, evidence)
    assert result['status'] == case['expected']
    if case['reason']:
        assert case['reason'] in result['reasons']


@pytest.mark.parametrize('case', load('tests/fixtures/v10c_run11_contract_replay.json')['cases'], ids=lambda c: str(c['action']))
def test_run11_annotated_projection(case):
    notes, evidence = project_legacy(case)
    result = check_basis(notes, evidence)
    assert result['status'] == case['expected']
    assert set(case['reasons']) <= set(result['reasons'])


def test_claim_measurement_is_not_semantic_truth():
    notes = [CASES[0]['notes'], CASES[24]['notes'], 'prefix ' + CASES[0]['notes']]
    m = measure_receipts(notes, ['[BC=BLOCKED WHY=NUMERIC_S]', '[BC=BLOCKED WHY=SATURATION]'])
    assert m['header_schema_version'] == 3
    assert m['basis_check_pass'] == 3
    assert m['submitted_BC_certificate_coverage'] == 2
    assert m['S_basis'] == {'NONE': 2, 'ACUTE': 1}
    assert m['CAP_basis'] == {'NONE': 3}
    assert m['basis_receipt_coverage_status'] == 'FAIL'
    assert m['numeric_S_blocked'] == m['saturation_basis_blocked'] == 1
    assert m['semantic_consistency'] == 'UNKNOWN_WITHOUT_EXPLICIT_PUBLIC_ANNOTATIONS'
    assert check_basis(notes[1], CASES[24]['evidence'])['status'] == 'BLOCKED'
    s_none = measure_receipts([CASES[22]['notes']])
    assert s_none['MODE_S_inconsistent_claims'] == 1


def test_certificate_enum_fields_and_duplicates_fail_closed():
    n = CASES[0]['notes']
    certificate = '[BC=PASS S=NONE CAP=NONE]'
    for bad in ('[BC=PASS]', '[BC=PASS CAP=NONE S=NONE]', '[BC=PASS S=? CAP=NONE]',
                '[BC=PASS S=NONE\nCAP=NONE]', '[BC=PASS S=NONE CAP=NONE extra=1]',
                certificate + ' ' + certificate, '[BC=BLOCKED WHY=SCHEMA]'):
        result = check_basis(n.replace(certificate, bad), EVIDENCE)
        assert result['status'] == 'BLOCKED'
        assert 'SCHEMA' in result['reasons']


def test_annotated_run13_replay_and_run12_original_negative():
    replay = load('docs/project/reviews/S09-22_RUN13_SEMANTIC_REPLAY.json')
    assert replay['RUN13_SEMANTIC_REPLAY'] == '4/4 EXPECTED'
    assert [a['action'] for a in replay['actions']] == [35, 36, 37, 38]
    assert [a['result']['status'] for a in replay['actions']] == ['BLOCKED', 'BLOCKED', 'PASS', 'BLOCKED']
    assert [a['result']['reasons'] for a in replay['actions']] == [['NUMERIC_S'], ['NUMERIC_S'], [], ['SATURATION']]
    assert replay['RUN12_HEADER_REPLAY'] == '3/3 CORRECTLY_BLOCKED'
    for row in replay['run12_original_negative']:
        assert row['result']['status'] == 'BLOCKED' and 'SCHEMA' in row['result']['reasons']
    assert not replay['historical_notes_changed']
    assert not replay['raw_or_private_logs_archived']


def test_identity_prompt_burden_and_frozen_assets():
    protected = ['skills/' + n + '/SKILL.md' for n in
                 ('structured-state-board', 'rolling-planning', 'delivery-progress', 'risk-review')]
    protected += ['scripts/policy_trace_audit.py', 'scripts/post_run_audit.py',
                  'scripts/package_candidate.py', 'pyproject.toml', 'uv.lock']
    for path in protected:
        before = subprocess.check_output(['git', 'show', f'{BASE}:{path}'], cwd=ROOT)
        assert before.replace(b'\r\n', b'\n') == (ROOT/path).read_bytes().replace(b'\r\n', b'\n')
    c, m = load('configs/current_candidate.json'), load('configs/runtime_manifest.json')
    assert c['candidate_id'] == m['name'] == 'candidate-v10e-explicit-basis-preflight'
    assert c['parent_candidate_id'] == 'candidate-v10d-anchored-five-marker-preflight'
    assert c['strategy_delta'] == 'NONE' and not any(c['validation'].values())
    assert c['header_schema_version'] == 3
    assert hashlib.sha256((ROOT/'configs/runtime_manifest.json').read_bytes()).hexdigest() == c['runtime_manifest']['sha256']
    assert hashlib.sha256(m['instruction'].encode()).hexdigest() == c['runtime_manifest']['instruction_sha256']
    old = json.loads(subprocess.check_output(['git', 'show', f'{BASE}:configs/runtime_manifest.json'], cwd=ROOT))['instruction']
    assert len(m['instruction']) <= len(old) * 1.05
    for prefix in ('K1 PUBLIC', 'K4 CLEANUP', 'K5 SUMMARY'):
        assert next(s for s in old.splitlines() if s.startswith(prefix)) == next(s for s in m['instruction'].splitlines() if s.startswith(prefix))
    # Everything after the kernel and before preflight remains byte-for-byte text.
    assert old[old.index('STARTUP / NORMAL FLOW'):old.index('SYSTEM ACTION PREFLIGHT')] == m['instruction'][m['instruction'].index('STARTUP / NORMAL FLOW'):m['instruction'].index('SYSTEM ACTION PREFLIGHT')]
