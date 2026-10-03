"""Written contracts + hand-annotated counterexamples, NOT model execution tests.

The evaluator below checks supplied semantic annotations. It is not a game
controller, runtime enforcement layer, hidden state estimator or choice oracle.
"""
import copy
import hashlib
import json
from pathlib import Path
import subprocess

import pytest

ROOT = Path(__file__).resolve().parents[1]
BASE = '72b31304936f61386b7cd9fd2ec5630cdb69cf22'
CASES = json.loads((ROOT/'tests/fixtures/v11_strategy_reset_cases.json').read_text(encoding='utf-8'))
P = (ROOT/'skills/rolling-planning/SKILL.md').read_text(encoding='utf-8')
B = (ROOT/'skills/structured-state-board/SKILL.md').read_text(encoding='utf-8')
D = (ROOT/'skills/delivery-progress/SKILL.md').read_text(encoding='utf-8')
R = (ROOT/'skills/risk-review/SKILL.md').read_text(encoding='utf-8')

def old(path):
    return subprocess.check_output(['git','show',f'{BASE}:{path}'],cwd=ROOT)

def annotated_valid(facts, response):
    """Several legal choices may pass; does not assert an optimal Story answer."""
    active = (facts.get('material_warning',False) or facts.get('prior_active',False)) and not facts.get('public_clearance',False)
    if response['risk_active'] != active:
        return False
    if active and facts.get('accountability') and response['gate'] != 'FULL':
        return False
    if response['mode']=='S' and not (active or facts.get('acute_binding')):
        return False
    if facts.get('public_clearance') and not facts.get('other_binding') and response['mode']!='A':
        return False
    if facts.get('result_gap') and response['gap']!='RESULT_CONVERSION_GAP':
        return False
    if facts.get('stale_unverified') and response['delivery_authority']=='STRONG':
        return False
    if response['basis']=='REPORT' and not (facts.get('result_basis') or facts.get('independent_value')):
        return False
    if response['basis']=='FARM_NO_GAIN':
        return False
    if response['basis'] not in facts['allowed_bases']:
        return False
    if response.get('future_sequence') or response.get('numeric_lowest_only'):
        return False
    if response.get('invent_stock') or response.get('hidden_threshold'):
        return False
    if facts.get('thin_health_margin') and not response.get('compares_downside'):
        return False
    if facts.get('official_delta') and not response.get('allows_official_delta'):
        return False
    return True

@pytest.mark.parametrize('case',CASES,ids=lambda c:c['name'])
def test_annotated_scenarios_and_negative_contrasts(case):
    assert annotated_valid(case['facts'],case['response'])
    bad=copy.deepcopy(case['response'])
    bad.update(case['negative'])
    assert not annotated_valid(case['facts'],bad)
    for skill,clause in case['clauses'].items():
        assert clause in {'Planning':P,'Board':B,'Delivery':D,'Risk':R}[skill]

@pytest.mark.parametrize('clause',[
    'early caution仅影响普通成本，不自动S',
    'CLEANUP_ACTION != RISK_CLEARED',
    '无fixed quota/无限cleanup loop',
    'ownership不能自动覆盖风险',
    'RESULT_CONVERSION_GAP',
    'generic reporting不能长期替代真实成果兑现',
    'ONE ENERGY STEP = choose best current marginal action only',
    'H+广告ΔH≤0非普通成长，除非生存critical',
    '无广告不等于零成本',
    '菜单无恢复不臆造',
    '不猜delta/概率/安全值',
])
def test_score_critical_written_principles(clause):
    assert clause in P

def test_narrow_skill_patch_and_unchanged_execution_abi():
    # Board/Delivery/Risk retain every parent line except the explicit replacement
    # around Board STICKY; no wholesale rewrite of four Skills.
    for name,text in [('delivery-progress',D),('risk-review',R),('structured-state-board',B)]:
        parent=old(f'skills/{name}/SKILL.md').decode('utf-8').splitlines()
        assert all(line in text for line in parent if line.strip())
    manifest=json.loads((ROOT/'configs/runtime_manifest.json').read_text(encoding='utf-8'))
    prior=json.loads(old('configs/runtime_manifest.json'))
    heading='SYSTEM ACTION PREFLIGHT / BASIS_CHECK'
    assert manifest['instruction'].split(heading)[1]==prior['instruction'].split(heading)[1]
    for current,parent in [(P,old('skills/rolling-planning/SKILL.md').decode()),(manifest['instruction'],prior['instruction'])]:
        assert len(current)<len(parent)
        assert len(current.encode())<len(parent.encode())
    assert 'CLEANUP_ACTION != RISK_CLEARED' in manifest['instruction']
    assert '默认回主线' not in P and '一次 cleanup 后 fresh observe，默认回主线' not in manifest['instruction']

def test_identity_and_frozen_scope():
    c=json.loads((ROOT/'configs/current_candidate.json').read_text(encoding='utf-8'))
    m=json.loads((ROOT/'configs/runtime_manifest.json').read_text(encoding='utf-8'))
    parent=json.loads(old('configs/current_candidate.json'))
    assert c['candidate_id']==m['name']=='candidate-v11-result-conversion-risk-persistence'
    assert c['parent_candidate_id']==parent['candidate_id']
    assert c['parent_identity']['skills']==parent['skills']
    assert c['submission_fallback']==parent['submission_fallback']
    assert not any(c['validation'].values())
    assert c['runtime_manifest']['sha256']==hashlib.sha256((ROOT/'configs/runtime_manifest.json').read_bytes()).hexdigest()
    assert c['runtime_manifest']['instruction_sha256']==hashlib.sha256(m['instruction'].encode()).hexdigest()
    for skill in c['skills']:
        assert skill['git_blob']==subprocess.check_output(['git','hash-object',skill['path']],cwd=ROOT,text=True).strip()
    for path in ['scripts/reviewer_gate.py','scripts/live_run_controller.py','scripts/live_review_packet.py',
                 'scripts/basis_preflight_audit.py','scripts/post_run_audit.py','scripts/package_candidate.py','pyproject.toml','uv.lock']:
        assert (ROOT/path).read_bytes().replace(b'\r\n',b'\n')==old(path).replace(b'\r\n',b'\n')
    assert not subprocess.check_output(['git','diff',BASE,'--','career_sim_runner','submission','submissions'],cwd=ROOT)

def test_legacy_counterexample_boundaries():
    # RUN14/15: a public bounded range is not a career cap; event theme is not
    # candidate-specific risk. RUN16: advertised delta allowed, not stock.
    m=json.loads((ROOT/'configs/runtime_manifest.json').read_text(encoding='utf-8'))['instruction']
    assert 'D/H公开最大值' in m and 'CAP=NONE' in m
    assert 'status_updates含HiddenRisk ±N允许作ADVERTISED_EFFECT' in m
    assert '不得delta累计重建stock' in m
    assert '不是按event title/theme自动拦截' in R
    assert '合法纠正流程的候选可ALLOW' in R
    assert '无new evidence不重开' in P
