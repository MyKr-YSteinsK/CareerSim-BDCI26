"""Written-policy and annotated comparisons only; no model or gameplay evidence."""
import copy
import hashlib
import json
from pathlib import Path
import subprocess

import pytest

from career_sim_runner.skill_contract import validate_submission_contract
from scripts.package_candidate import build_submission

ROOT=Path(__file__).resolve().parents[1]
BASE='1f992d7d24c2a39d6cf55147327cdcbb9e6f9f4b'
DATA=json.loads((ROOT/'tests/fixtures/v10h_dynamic_survival_cases.json').read_text(encoding='utf-8'))
TEXT=(ROOT/'skills/rolling-planning/SKILL.md').read_text(encoding='utf-8')

def old(path):
    return subprocess.check_output(['git','show',f'{BASE}:{path}'],cwd=ROOT)

def comparison_valid(case, response):
    """Check supplied human annotations, not free text or model choice optimality.

    thin_margin is a scenario annotation, never computed from a Health cutoff.
    There is no production evaluator/certificate or new runtime state here.
    """
    facts=case['facts']; options={x['choice']:x for x in case['choices']}
    rows=response.get('comparison',[])
    if response.get('chosen') not in options or len(rows)!=2:return False
    if len({x['choice'] for x in rows})!=2 or not all(x['choice'] in options for x in rows):return False
    if response['chosen'] not in {x['choice'] for x in rows}:return False
    if not all(x.get('current_value') and x.get('downside') for x in rows):return False
    if response.get('fresh_state')!={'H':facts['H'],'E':facts['E']}:return False
    if response.get('mode') != ('S' if facts['acute'] else 'A'):return False
    if facts['thin_margin'] and not response.get('workload_penalty'):return False
    if response.get('prior')!='UNCERTAIN_QUALITATIVE' or response.get('future_recovery')!='UNKNOWN':return False
    if response.get('precommitted_next') is not None or response.get('health_target') is not None:return False
    selected=options[response['chosen']]
    delta=selected.get('delta')
    if isinstance(delta,(int,float)) and facts['H']+delta<=0 and not facts.get('survival_critical'):return False
    if any(x.get('health_delta')!=options[x['choice']].get('delta','UNKNOWN') for x in rows):return False
    if response.get('selection_basis')!='CURRENT_COMPARATIVE_VALUE':return False
    if facts['energy_followup']:
        if not response.get('discarded_sequence'):return False
        if response.get('read_response')!=facts['realized_response']:return False
        if response.get('local_discount')!='CURRENT_PATH_ONLY':return False
    return True

@pytest.mark.parametrize('case',DATA['cases'],ids=lambda c:c['name'])
def test_annotated_comparison_contrasts(case):
    assert comparison_valid(case,case['annotated_comparison'])
    # Full ranking remains free: another nonfatal legal option may win.
    alternative=copy.deepcopy(case['annotated_comparison'])
    if case['name']=='RUN17_a22':
        alternative['chosen']=2
        assert comparison_valid(case,alternative)

@pytest.mark.parametrize('name',DATA['negative_mutations'])
def test_semantic_counterexamples_not_certificate_only(name):
    case=copy.deepcopy(next(c for c in DATA['cases'] if c['name']==('RUN17_a12_fresh' if name in ('stale_sequence','lowest_stat','balanced_recipe','no_gain_cap','missing_fresh_response') else 'RUN17_a22')))
    r=case['annotated_comparison']
    if name=='missing_comparison':r['comparison']=[]
    elif name=='empty_value':r['comparison'][0]['current_value']=''
    elif name=='missing_workload_penalty':r['workload_penalty']=False
    elif name=='unavailable_recovery':r['chosen']=999
    elif name=='block_all_actions':r['chosen']=None
    elif name=='numeric_S':r['mode']='S'
    elif name=='planned_second_recovery':r['precommitted_next']=6
    elif name=='maximize_health':r['health_target']=10
    elif name=='stale_values':r['fresh_state']['H']=8
    elif name=='fixed_safe_rule':r['prior']='H>=3_SAFE'
    elif name=='unlabeled_exact_delta':r['comparison'][0]['health_delta']=-2
    elif name=='unknown_cost_zero':r['comparison'][0]['health_delta']=0
    elif name=='stale_sequence':r['discarded_sequence']=False
    elif name=='lowest_stat':r['selection_basis']='LOWEST_N'
    elif name=='balanced_recipe':r['selection_basis']='NEXT_N_THEN_O'
    elif name=='no_gain_cap':r['local_discount']='GLOBAL_CAP'
    elif name=='missing_fresh_response':r['read_response']='OLD_PLAN'
    assert not comparison_valid(case,r)

@pytest.mark.parametrize('clause',[
    'A 内比较 fresh H余量','公开负荷/时长','不确定历史冲击prior',
    '合法恢复/低负荷项及 binding Delivery/trust/job','低H减容错，不自动S',
    'H+广告ΔH≤0非普通成长，除非生存critical','无广告不等于零成本',
    '不猜delta/概率/安全值','ownership不抵消下行','菜单无恢复不臆造',
    '未来恢复不保证','一次保护→fresh重排','不连订/补满',
    '理由须弃旧序','fresh H/E/realized response','对比合法替代解释胜出',
    '不能只说“下一项/最低数/N再O/均衡”',
])
def test_new_written_requirements_reject_parent_omissions(clause):
    assert clause in TEXT
    assert clause not in old('skills/rolling-planning/SKILL.md').decode('utf-8')

def test_scope_kernel_and_identity():
    c=json.loads((ROOT/'configs/current_candidate.json').read_text(encoding='utf-8'))
    parent=json.loads(old('configs/current_candidate.json'))
    m=json.loads((ROOT/'configs/runtime_manifest.json').read_text(encoding='utf-8'))
    pm=json.loads(old('configs/runtime_manifest.json'))
    assert c['candidate_id']==m['name']=='candidate-v10h-dynamic-survival-margin'
    assert c['parent_candidate_id']==parent['candidate_id']
    assert c['parent_identity']['skills']==parent['skills']
    assert c['strategy_delta']=='A_MODE_DYNAMIC_SURVIVAL_MARGIN'
    assert c['information_policy_delta']==parent['information_policy_delta']
    assert not any(c['validation'].values())
    assert c['submission_fallback']['candidate_id']==parent['submission_fallback']['candidate_id']
    assert c['header_schema_version']==parent['header_schema_version']
    assert c['basis_annotation_schema_version']==parent['basis_annotation_schema_version']
    for prefix in ('K1 OFFICIAL-ACCESS','K2 SATURATION','K4 CLEANUP','K5 SUMMARY'):
        assert next(s for s in m['instruction'].splitlines() if s.startswith(prefix))==next(s for s in pm['instruction'].splitlines() if s.startswith(prefix))
    start='SYSTEM ACTION PREFLIGHT / BASIS_CHECK'
    assert m['instruction'][m['instruction'].index(start):]==pm['instruction'][pm['instruction'].index(start):]
    before=old('skills/rolling-planning/SKILL.md').decode('utf-8').replace('\r\n','\n')
    assert [s for s in TEXT.splitlines() if not s.startswith(('- **C10','Energy 不预定'))]==[s for s in before.splitlines() if not s.startswith(('- **C10','Energy 不预定'))]
    for text,prior,budget in ((TEXT,before,1.05),(m['instruction'],pm['instruction'],1.03)):
        assert len(text)<=len(prior)*budget
        assert len(text.encode())<=len(prior.encode())*budget
    for path in ('skills/structured-state-board/SKILL.md','skills/delivery-progress/SKILL.md','skills/risk-review/SKILL.md',
                 'scripts/reviewer_gate.py','scripts/basis_preflight_audit.py','scripts/live_review_packet.py',
                 'scripts/post_run_audit.py','scripts/package_candidate.py','pyproject.toml','uv.lock'):
        # Git blobs are LF; Windows checkout uses CRLF. Scope is separately
        # checked against the held parent package's exact Skill bytes offline.
        assert (ROOT/path).read_bytes().replace(b'\r\n',b'\n')==old(path).replace(b'\r\n',b'\n')
    assert not subprocess.check_output(['git','diff',BASE,'--','career_sim_runner'],cwd=ROOT)
    assert c['runtime_manifest']['sha256']==hashlib.sha256((ROOT/'configs/runtime_manifest.json').read_bytes()).hexdigest()
    assert c['runtime_manifest']['instruction_sha256']==hashlib.sha256(m['instruction'].encode()).hexdigest()
    for skill in c['skills']:
        assert skill['git_blob']==subprocess.check_output(['git','hash-object',skill['path']],cwd=ROOT,text=True).strip()

def test_four_skill_offline_package(tmp_path):
    build_submission(ROOT,tmp_path/'submission')
    details=validate_submission_contract(tmp_path/'submission')
    assert details['submission_mode']=='skill_bundle' and len(details['skill_ids'])==4
