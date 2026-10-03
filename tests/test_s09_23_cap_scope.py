"""Explicit growth-cap scope annotations; historical evidence remains immutable."""
import hashlib
import json
from pathlib import Path
import subprocess

import pytest
from scripts.basis_preflight_audit import check_basis, measure_receipts, parse_five_marker_header

ROOT = Path(__file__).resolve().parents[1]
BASE = 'e0a5f2ee598d26fb012e3792ed974060113c1fe3'


def load(path):
    return json.loads((ROOT/path).read_text(encoding='utf-8'))


CASES = load('tests/fixtures/v10f_cap_scope_cases.json')
EVIDENCE = CASES[10]['evidence']


def explicit_growth_projection(evidence):
    """Test-only annotation mapping for already classified historical scenarios.

    No production fallback: caller must choose growth vs bounded scope explicitly.
    """
    e = dict(evidence)
    e['growth_cap_claim'] = e.pop('saturation_claim', None)
    e['bounded_state_fact'] = False
    for before, after in (
        ('explicit_public_completion', 'explicit_public_growth_cap'),
        ('claim_scope', 'growth_cap_scope'),
        ('public_completion_scope', 'public_growth_cap_scope'),
    ):
        e[after] = e.pop(before, None)
    return e


@pytest.mark.parametrize('case', CASES, ids=lambda c: c['name'])
def test_bounded_state_vs_growth_scope(case):
    result = check_basis(case['notes'], case['evidence'])
    assert result['status'] == case['expected']
    assert result['may_submit'] == (case['expected'] == 'PASS')
    assert result['annotation_schema_version'] == 2
    if case['reason']:
        assert result['reasons'][0] == case['reason']
    else:
        assert result['cap_claim_consistent']


@pytest.mark.parametrize('case', load('tests/fixtures/v10e_explicit_basis_cases.json'), ids=lambda c: c['name'])
def test_previous_explicit_basis_scenarios_with_explicit_scope_projection(case):
    notes = case['notes']
    e = explicit_growth_projection(case['evidence'])
    if case['name'] in ('15_D_range', '19_capacity'):
        # These two historical scenarios are direct bounded-state/budget facts;
        # the new contract deliberately changes their certificate projection.
        e.update(growth_cap_claim=False, bounded_state_fact=True,
                 explicit_public_growth_cap=False, growth_cap_scope=None, public_growth_cap_scope=None)
        notes = notes.replace('CAP=PUBLIC_SCOPED]', 'CAP=NONE]')
    result = check_basis(notes, e)
    assert result['status'] == case['expected']
    if case['reason']:
        assert result['reasons'][0] == case['reason']


@pytest.mark.parametrize('case', load('tests/fixtures/v10d_five_marker_header.json'), ids=lambda c: c['name'])
def test_frozen_header_layout_projection(case):
    notes = case['notes'].replace('[BC=PASS]', '[BC=PASS S=NONE CAP=NONE]')
    result = check_basis(notes, EVIDENCE)
    assert result['status'] == case['expected']
    assert parse_five_marker_header(notes)['valid'] == result['may_submit']
    if not result['may_submit']:
        assert 'SCHEMA' in result['reasons']


def project_legacy(case):
    e = explicit_growth_projection(case['evidence'])
    s = 'ACUTE' if e.get('fresh_material_binding') is True else 'NONE'
    if s != 'NONE':
        e['public_binding_class'] = s
    cap = 'PUBLIC_SCOPED' if e['growth_cap_claim'] is True else 'NONE'
    return case['notes'] + f' [BC=PASS S={s} CAP={cap}]', e


@pytest.mark.parametrize('case', load('tests/fixtures/v10c_kernel_cases.json'), ids=lambda c: c['name'])
def test_other_kernel_annotations_preserved(case):
    notes, evidence = project_legacy(case)
    result = check_basis(notes, evidence)
    assert result['status'] == case['expected']
    if case['reason']:
        assert case['reason'] in result['reasons']


@pytest.mark.parametrize('case', load('tests/fixtures/v10c_run11_contract_replay.json')['cases'], ids=lambda c: str(c['action']))
def test_run11_annotated_growth_projection(case):
    notes, evidence = project_legacy(case)
    result = check_basis(notes, evidence)
    assert result['status'] == case['expected']
    assert set(case['reasons']) <= set(result['reasons'])


@pytest.mark.parametrize('context', [
    'H=3 alone implies S', 'Ordinary numeric Health decline implies S',
    'Continue S until numeric recovery target reached without fresh warning',
])
def test_additional_numeric_S_negatives(context):
    notes = CASES[10]['notes'].replace('P=A', 'P=S')
    result = check_basis(notes, dict(EVIDENCE, fresh_material_binding=False, only_numeric_basis=True))
    assert result['reasons'] == ['NUMERIC_S'], context


def test_required_exact_held_replays():
    replay = load('docs/project/reviews/S09-23_CAP_SCOPE_REPLAY.json')
    assert replay['RUN14_CAP_SCOPE_REPLAY'] == '2/2 PASS'
    assert [x['action'] for x in replay['run14']] == [12, 13]
    for row in replay['run14']:
        assert row['new_result']['status'] == 'PASS'
        assert row['annotation']['bounded_state_fact'] is True
        assert row['annotation']['growth_cap_claim'] is False
        assert row['frozen_v10e_result']['reasons'] == ['SATURATION']
        assert not row['historical_notes_changed']
    assert replay['RUN13_SEMANTIC_REPLAY'] == '4/4 EXPECTED'
    assert [x['result']['reasons'] for x in replay['run13']] == [['NUMERIC_S'], ['NUMERIC_S'], [], ['SATURATION']]
    assert replay['RUN12_HEADER_REPLAY'] == '3/3 CORRECTLY_BLOCKED'
    assert all('SCHEMA' in x['result']['reasons'] for x in replay['run12'])


def test_certificate_coverage_remains_claims_only():
    notes = [CASES[10]['notes'], CASES[0]['notes'], 'prefix '+CASES[10]['notes']]
    result = measure_receipts(notes)
    assert result['header_schema_version'] == 3
    assert result['basis_check_pass'] == 3
    assert result['submitted_BC_certificate_coverage'] == 2
    assert result['S_basis'] == {'NONE': 3}
    assert result['CAP_basis'] == {'NONE': 3}
    assert result['semantic_consistency'] == 'UNKNOWN_WITHOUT_EXPLICIT_PUBLIC_ANNOTATIONS'
    assert check_basis(notes[1], CASES[0]['evidence'])['reasons'] == ['SATURATION']


def test_schema_not_relaxed():
    n = CASES[10]['notes']
    cert = '[BC=PASS S=NONE CAP=NONE]'
    for bad in ('[BC=PASS]', '[BC=PASS CAP=NONE S=NONE]', '[BC=PASS S=? CAP=NONE]',
                '[BC=PASS S=NONE\nCAP=NONE]', cert+' '+cert, '[BC=BLOCKED WHY=SCHEMA]'):
        result = check_basis(n.replace(cert, bad), EVIDENCE)
        assert result['status'] == 'BLOCKED' and 'SCHEMA' in result['reasons']


def test_frozen_K3_Skills_measurement_and_identity():
    paths = ['skills/'+n+'/SKILL.md' for n in
             ('structured-state-board', 'delivery-progress', 'rolling-planning', 'risk-review')]
    # S09-24 explicitly authorizes post-run transport/classification hardening.
    paths += ['scripts/policy_trace_audit.py',
              'scripts/package_candidate.py', 'pyproject.toml', 'uv.lock',
              'tests/fixtures/v10e_explicit_basis_cases.json',
              'docs/project/reviews/S09-22_RUN13_SEMANTIC_REPLAY.json',
              'docs/project/runs/v10e-run14-semantic-evidence.json']
    for path in paths:
        old = subprocess.check_output(['git', 'show', f'{BASE}:{path}'], cwd=ROOT)
        assert old.replace(b'\r\n', b'\n') == (ROOT/path).read_bytes().replace(b'\r\n', b'\n')
    assert not subprocess.check_output(['git', 'diff', BASE, '--', 'career_sim_runner'], cwd=ROOT)
    old_oracle = subprocess.check_output(['git', 'show', f'{BASE}:scripts/basis_preflight_audit.py'], cwd=ROOT).decode()
    new_oracle = (ROOT/'scripts/basis_preflight_audit.py').read_text(encoding='utf-8')
    start, end = '    header = parse_header(notes)', "    if evidence.get('cleanup')"
    assert old_oracle[old_oracle.index(start):old_oracle.index(end)] == new_oracle[new_oracle.index(start):new_oracle.index(end)]
    c, m = load('configs/current_candidate.json'), load('configs/runtime_manifest.json')
    assert c['candidate_id'] == m['name'] == 'candidate-v10f-cap-scope-correction'
    assert c['parent_candidate_id'] == 'candidate-v10e-explicit-basis-preflight'
    assert c['strategy_delta'] == 'NONE' and not any(c['validation'].values())
    assert c['header_schema_version'] == 3 and c['basis_annotation_schema_version'] == 2
    assert hashlib.sha256((ROOT/'configs/runtime_manifest.json').read_bytes()).hexdigest() == c['runtime_manifest']['sha256']
    assert hashlib.sha256(m['instruction'].encode()).hexdigest() == c['runtime_manifest']['instruction_sha256']
    old = json.loads(subprocess.check_output(['git', 'show', f'{BASE}:configs/runtime_manifest.json'], cwd=ROOT))['instruction']
    assert len(m['instruction']) <= len(old)*1.03
    for prefix in ('K1 PUBLIC', 'K3 MODE', 'K4 CLEANUP', 'K5 SUMMARY'):
        assert next(x for x in old.splitlines() if x.startswith(prefix)) == next(x for x in m['instruction'].splitlines() if x.startswith(prefix))
    assert old[old.index('STARTUP / NORMAL FLOW'):old.index('SYSTEM ACTION PREFLIGHT')] == m['instruction'][m['instruction'].index('STARTUP / NORMAL FLOW'):m['instruction'].index('SYSTEM ACTION PREFLIGHT')]


def test_severity_default_preserves_only_run_invalidating_stops():
    workflow = (ROOT/'docs/project/LIVE_RUN_WORKFLOW.md').read_text(encoding='utf-8')
    assert 'S1_POLICY_DRIFT => RECORD_AND_CONTINUE' in workflow
    assert 'S2_RUN_INVALIDATING => STOP' in workflow
    assert 'FULL_SCORE_EVALUATION' in workflow
    assert 'unsafe ambiguous side effect' in workflow
    assert 'MECHANISM_VALIDATION_CENSOR' in workflow
    assert 'CERTIFICATE_OR_SEMANTIC_DRIFT => EARLY_ABORT' not in workflow
