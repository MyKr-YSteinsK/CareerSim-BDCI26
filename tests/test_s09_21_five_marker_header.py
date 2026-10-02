"""Static serialization and explicitly annotated semantics; no LLM/live proof."""
import hashlib
import json
from pathlib import Path
import subprocess
import pytest
from scripts.basis_preflight_audit import check_basis, measure_receipts, parse_five_marker_header

ROOT=Path(__file__).resolve().parents[1]
BASE='554acbc3ec0cb75ea9f76087d65dc48ed41986a2'
def load(p): return json.loads((ROOT/p).read_text(encoding='utf-8'))
KERNEL=load('tests/fixtures/v10c_kernel_cases.json')
CASES=load('tests/fixtures/v10d_five_marker_header.json')
EVIDENCE=KERNEL[0]['evidence']

@pytest.mark.parametrize('case',CASES,ids=lambda c:c['name'])
def test_layout(case):
    result=check_basis(case['notes'],EVIDENCE)
    assert result['status']==case['expected']
    assert result['may_submit']==(case['expected']=='PASS')
    assert parse_five_marker_header(case['notes'])['valid']==result['may_submit']
    if not result['may_submit']: assert 'SCHEMA' in result['reasons']

@pytest.mark.parametrize('case',KERNEL,ids=lambda c:c['name'])
def test_preserved_kernel_semantics_in_submitted_shape(case):
    # Explicit output serialization projection, not a historical receipt backfill.
    result=check_basis(case['notes']+' [BC=PASS]',case['evidence'])
    assert result['status']==case['expected']
    if case['reason']: assert case['reason'] in result['reasons']

@pytest.mark.parametrize('case',load('tests/fixtures/v10c_run11_contract_replay.json')['cases'],ids=lambda c:str(c['action']))
def test_run11_annotated_serialization_projection(case):
    result=check_basis(case['notes']+' [BC=PASS]',case['evidence'])
    assert result['status']==case['expected']
    assert set(case['reasons'])<=set(result['reasons'])

def test_receipt_claim_does_not_override_schema_or_semantics():
    h=CASES[10]['notes']
    assert check_basis(h,dict(EVIDENCE,restricted_basis=True))['status']=='BLOCKED'
    m=measure_receipts(['prefix '+h,h,h.replace('[BC=PASS]','[BC=BLOCKED WHY=SCHEMA]')])
    assert m['basis_check_pass']==2
    assert m['full_five_marker_coverage']==1
    assert m['submitted_BC_PASS_with_invalid_header']==1
    assert m['action_submitted_despite_BLOCKED']==1
    assert m['basis_receipt_coverage_status']=='FAIL'
    assert m['restricted_basis_blocked'] is None

def test_frozen_assets_and_identity():
    for p in ['skills/'+n+'/SKILL.md' for n in ('structured-state-board','delivery-progress','rolling-planning','risk-review')]+['scripts/policy_trace_audit.py','scripts/post_run_audit.py','scripts/package_candidate.py','pyproject.toml','uv.lock']:
        before=subprocess.check_output(['git','show',f'{BASE}:{p}'],cwd=ROOT).replace(b'\r\n',b'\n')
        assert before==(ROOT/p).read_bytes().replace(b'\r\n',b'\n')
    c=load('configs/current_candidate.json');m=load('configs/runtime_manifest.json')
    assert c['candidate_id']==m['name']=='candidate-v10d-anchored-five-marker-preflight'
    assert c['parent_candidate_id']=='candidate-v10c-compaction-agnostic-kernel'
    assert c['strategy_delta']=='NONE' and not any(c['validation'].values())
    assert hashlib.sha256((ROOT/'configs/runtime_manifest.json').read_bytes()).hexdigest()==c['runtime_manifest']['sha256']
    assert hashlib.sha256(m['instruction'].encode()).hexdigest()==c['runtime_manifest']['instruction_sha256']
    old=json.loads(subprocess.check_output(['git','show',f'{BASE}:configs/runtime_manifest.json'],cwd=ROOT))['instruction']
    assert old[old.index('K1 PUBLIC'):old.index('STARTUP / NORMAL FLOW')]==m['instruction'][m['instruction'].index('K1 PUBLIC'):m['instruction'].index('STARTUP / NORMAL FLOW')]
    assert len(m['instruction'])<=1.10*len(old)
    assert 'SUBMITTED ACTION NOTES MUST BEGIN EXACTLY WITH THE FIVE-MARKER HEADER.' in m['instruction']

def test_sanitized_run12_replay():
    r=load('docs/project/reviews/S09-21_RUN12_HEADER_REPLAY.json')
    assert len(r['actions'])==3
    for a in r['actions']:
        assert a['new_original']['status']=='BLOCKED'
        assert 'SCHEMA' in a['new_original']['reasons']
        assert not a['new_original']['may_submit']
        assert check_basis(a['sanitized_corrected_header'],EVIDENCE)['status']=='PASS'
        assert a['corrected_projection']['status']=='PASS'
        assert a['old_offline_oracle']['status']=='BLOCKED'
