"""Source-based policy / reviewer regression, not model adherence or live tests."""
import ast
import copy
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import subprocess

import pytest

from career_sim_runner.skill_contract import validate_submission_contract
from scripts.live_review_packet import ReviewStream, official_observation
from scripts.basis_preflight_audit import check_basis
from scripts.package_candidate import build_submission
from scripts.reviewer_gate import review_information_access, validate_receipt
from tests.test_s09_24_reviewer_reliability import SESSION, HEADER, call, result, observe, receipt, CASES

ROOT=Path(__file__).resolve().parents[1]
BASE='6efb27128ed1727d7def7ae21d64d9b67e512495'
def load(path):
    return json.loads((ROOT/path).read_text(encoding='utf-8'))
MATRIX=load('docs/project/reviews/S09-25_INFORMATION_ACCESS_MATRIX.json')
FIXTURE=load('tests/fixtures/v10g_official_access_cases.json')
ITEMS={x['information_item']:x for x in MATRIX['information_matrix']}


def proof(**changes):
    p=dict(information_used='option advertises HiddenRisk+1',
        model_context_location='RUN16 observe seq107, choices[0].status_updates.HiddenRisk',
        source_evidence='S09-25 RUN16_provenance.a11; locked1.0.1 official MCP serializer',
        official_path='VERIFIED_TEST_EQUIVALENT',official_prohibition='NO',
        claim_type='DELTA_EFFECT',support_type='DELTA_EFFECT',accessibility='YES',
        session_id=SESSION,context_session=SESSION,context_source_seq=107,submission_seq=109,
        context_complete=False,official_agent_input={'choices':[{'status_updates':{'HiddenRisk':1}}]},
        context_path=['choices',0,'status_updates','HiddenRisk'],context_value=1)
    p.update(changes)
    return p


@pytest.mark.parametrize('case',FIXTURE['cases'],ids=lambda c:c['name'])
def test_access_contrasts(case):
    p=proof(**case['changes'])
    if case.get('remove_context'):
        for k in ('official_agent_input','context_path','context_value'): p.pop(k,None)
    assert review_information_access(p)==case['expected']


@pytest.mark.parametrize('item',MATRIX['information_matrix'],ids=lambda i:i['information_item'])
def test_matrix_source_not_a_second_policy_table(item):
    # Matrix status is canonical. Conditional/authoring facts stay hypotheses;
    # investigative surface is UNKNOWN, never invented access/permanent ban.
    status=item['recommended_status']
    p=proof(information_used=item['information_item'],model_context_location=item['official_test_agent_path'],
            source_evidence='S09-25 '+str(item['evidence']))
    if status=='BAN':
        p.update(accessibility='NO',official_path='UNAVAILABLE',context_complete=True,support_type='NONE')
        for k in ('official_agent_input','context_path','context_value'):p.pop(k)
    elif status=='INVESTIGATE':
        p.update(accessibility='UNKNOWN',official_path='UNKNOWN')
    elif status=='CONDITIONAL' or item['source_surface'] not in ('observe',):
        p.update(claim_type='EMPIRICAL_PRIOR',support_type='EMPIRICAL_PRIOR',hypothesis_only=True)
    expected={'ALLOW':'NO_K1_ACCESS_VIOLATION','CONDITIONAL':'NO_K1_ACCESS_VIOLATION',
              'BAN':'K1_ACCESS_VIOLATION','INVESTIGATE':'REVIEW_UNCERTAIN_MATERIAL'}[status]
    assert review_information_access(p)==expected


def test_required_matrix_coverage():
    assert len(ITEMS)==69
    assert len(FIXTURE['required_matrix_items'])>=14
    assert set(FIXTURE['required_matrix_items']) <= ITEMS.keys()


@pytest.mark.parametrize('surface,context,path,value,kind',[
    ('Handbook',{'handbook':'official salary table'},['handbook'],'official salary table','OBSERVED_STATE'),
    ('same-session logs',{'entries':[{'message':'promotion announced'}]},['entries',0,'message'],'promotion announced','OBSERVED_STATE'),
    ('observe Health',{'current_state':{'status':{'health':2}}},['current_state','status','health'],2,'OBSERVED_STATE'),
    ('formal Review',{'events':'grade B; promoted L2'},['events'],'grade B; promoted L2','OBSERVED_STATE'),
])
def test_official_other_surfaces_admitted_without_polling(surface,context,path,value,kind):
    p=proof(information_used=surface,official_agent_input=context,context_path=path,
            context_value=value,claim_type=kind,support_type=kind)
    assert review_information_access(p)=='NO_K1_ACCESS_VIOLATION'


def test_run16_exact_delta_before_a11_and_reclassified_receipt():
    a=MATRIX['RUN16_provenance']['a11']
    assert a['observe_seq']==107 and a['observe_seq']<a['submit_seq']
    assert a['high_intensity_choice']['status_updates']['HiddenRisk']==1
    assert 'HiddenRisk+1' in a['notes'] and not a['current_state_has_hidden_stock']
    p=proof(official_agent_input={'choices':[a['high_intensity_choice']]})
    r=receipt(CASES[0]); r.update(review_object='PLANNING_RANKING',owner='rolling-planning',
        action_index=11,clause_id='K1/OFFICIAL-ACCESS',information_boundary_version=2,information_access=p)
    checked=validate_receipt(r,retrospective=True)
    assert checked['information_access_result']=='NO_K1_ACCESS_VIOLATION'
    assert not checked['stop'] and not checked['candidate_failure']
    # All-action optimality and score are outside this access-only receipt.
    r.update(stop_class='CONFIRMED_CANDIDATE_VIOLATION',verdict='VIOLATION',
             direct_candidate_violation_link='Agent mentioned HiddenRisk+1')
    r['counterexample_check'].update(result='NO_COUNTEREXAMPLE')
    with pytest.raises(ValueError,match='contradicts'):validate_receipt(r,retrospective=True)


@pytest.mark.parametrize('missing',['information_used','model_context_location','source_evidence',
    'official_path','official_prohibition','claim_type','support_type','accessibility','context_complete'])
def test_provenance_required(missing):
    p=proof();p.pop(missing)
    with pytest.raises(ValueError):review_information_access(p)


def test_packet_omission_cannot_confirm_unavailable_information():
    p=proof(accessibility='NO',official_path='UNAVAILABLE',context_complete=False)
    for k in ('official_agent_input','context_path','context_value'):p.pop(k)
    assert review_information_access(p)=='REVIEW_UNCERTAIN_MATERIAL'
    r=receipt(CASES[0]);r.update(clause_id='K1/OFFICIAL-ACCESS',information_access=p,
        stop_class='REVIEW_UNCERTAIN_MATERIAL',verdict='UNCERTAIN',
        material_evidence_gap='Full pre-action official model context unavailable')
    assert not validate_receipt(r,retrospective=True)['candidate_failure']


def test_missing_provenance_cannot_confirm_K1_but_old_stop_remains_readable():
    r=receipt(CASES[4]);r.update(clause_id='K1/PUBLIC')
    with pytest.raises(ValueError,match='provenance'):validate_receipt(r)
    assert validate_receipt(r,retrospective=True)['valid']
    r['information_boundary_version']=2
    with pytest.raises(ValueError,match='provenance'):validate_receipt(r,retrospective=True)


@pytest.mark.parametrize('change',[
    {'accessibility':'NO'},{'context_value':7},
    {'context_path':['current_state','status','hidden_risk']},
])
def test_false_missing_or_mismatched_effect_proof_rejected(change):
    with pytest.raises(ValueError):review_information_access(proof(**change))


@pytest.mark.parametrize('change',[
    {'context_session':'b'*32},{'context_source_seq':109},{'submission_seq':106},
    {'official_agent_input':{'current_state':{'session_id':'b'*32},'choices':[{'status_updates':{'HiddenRisk':1}}]}},
])
def test_cross_session_or_future_evidence_cannot_support_access(change):
    with pytest.raises(ValueError):review_information_access(proof(**change))


def test_current_packet_preserves_all_official_fields_and_source_freshness():
    data=observe()
    data['current_event'].update(rules=['once'],remaining_energy=3,energy_budget=3,max_selections=3,
                                allow_no_action=True,document={'check_command':'show_employee_handbook'})
    data['choices'][0].update(energy_cost=2,status_updates={'Output':2,'HiddenRisk':1},action_id='filtered')
    data['current_state'].update(statistics={'secret':7},monthly_action_count=99,available_choice_count=1)
    data['raw_private_object']={'private_test':'not-Agent-input'}
    initial=copy.deepcopy(data);monitor=ReviewStream((1,),session=SESSION)
    monitor.feed(result(107,'o1','mcp_career-emulator_observe',data))
    monitor.feed(call(109,'a1','mcp_career-emulator_take_action',{'session_id':SESSION,'choice':1,'notes':HEADER+' HiddenRisk+1'}))
    monitor.feed(result(110,'a1','mcp_career-emulator_take_action',{'success':True}))
    after=copy.deepcopy(data);after['current_state']['status']['output']=3
    packet=monitor.feed(result(111,'o2','mcp_career-emulator_observe',after))[0];row=packet['rows'][0]
    assert data==initial
    assert row['official_before']==official_observation(initial)
    assert row['official_after']==official_observation(after)
    assert row['choices'][0]['status_updates']=={'Output':2,'HiddenRisk':1}
    assert row['selected_candidate']==row['choices'][0]
    assert row['event']['remaining_energy']==3 and row['event']['rules']==['once']
    assert row['before_source']['seq']==107 and row['source_seq']==109 and row['observe_seq']==111
    assert 'HiddenRisk+1' in row['notes'] and row['fresh_observe']
    assert row['public_before']['status']['output']==1 and row['public_after']['status']['output']==3
    serialized=json.dumps(packet)
    for excluded in ('filtered-id','action_id','statistics','monthly_action_count','raw_private_object','private_test'):
        assert excluded not in serialized
    assert 'HiddenRisk' not in row['official_before']['current_state']['status']


def test_cross_session_action_excluded():
    monitor=ReviewStream((1,),session=SESSION)
    monitor.feed(result(1,'o','mcp_career-emulator_observe',observe()))
    with pytest.raises(ValueError,match='cross-session action'):
        monitor.feed(call(2,'a','take_action',{'session_id':'b'*32,'choice':1,'notes':HEADER}))
    assert monitor.actions==0 and monitor.pending is None


def test_preserves_locked_serializer_extension_fields_not_name_blacklist():
    data=observe();data['choices'][0].update(internal_named_official_effect={'HiddenRisk':1})
    assert official_observation(data)['choices'][0]['internal_named_official_effect']=={'HiddenRisk':1}


def test_packet_exclusions_match_pure_locked_serializer():
    # Execute only the four pure response helpers/constants/dataclass. No package
    # import, game engine, storage, provider or service initialization.
    path=ROOT/'.venv/Lib/site-packages/career_emulator/server/models.py'
    expected=next(x['sha256'] for x in MATRIX['sources']['PUBLISHED_WHEEL']['files']
                  if x['path']=='career_emulator/server/models.py')
    assert hashlib.sha256(path.read_bytes()).hexdigest()==expected
    tree=ast.parse(path.read_text(encoding='utf-8'))
    names={'_strip_mcp_choice','_strip_mcp_state','_strip_mcp_event','ObserveResponse',
           'MCP_HIDDEN_STATE_KEYS','MCP_HIDDEN_EVENT_KEYS'}
    nodes=[n for n in tree.body if getattr(n,'name',None) in names or
           isinstance(n,ast.Assign) and any(getattr(t,'id',None) in names for t in n.targets)]
    env={'Any':object,'dataclass':dataclass}
    exec(compile(ast.Module(body=nodes,type_ignores=[]),str(path),'exec'),env)
    data=observe();data['current_event'].update(remaining_energy=3,rules=['once'])
    data['choices'][0].update(status_updates={'HiddenRisk':1,'Output':2},energy_cost=2)
    data['current_state'].update(statistics={'secret':8},quarter_energy_remaining=3)
    response=env['ObserveResponse'](data['current_state'],data['current_event'],data['choices'],data['events'])
    assert official_observation(data)==response.to_mcp_dict()


def test_official_delta_does_not_bypass_K3_binding_requirement():
    e=copy.deepcopy(load('tests/fixtures/v10f_cap_scope_cases.json')[10]['evidence'])
    e.update(public_basis=True,restricted_basis=False,fresh_material_binding=False,
             only_numeric_basis=True,public_binding_class='NONE')
    notes=HEADER.replace('P=A','P=S')+' option advertises HiddenRisk+1'
    out=check_basis(notes,e)
    assert out['status']=='BLOCKED' and 'NUMERIC_S' in out['reasons']


def test_policy_and_prompt_burden_and_strategy_preserved():
    c=load('configs/current_candidate.json');m=load('configs/runtime_manifest.json')
    old=json.loads(subprocess.check_output(['git','show',BASE+':configs/runtime_manifest.json'],cwd=ROOT))
    assert c['candidate_id']==m['name']=='candidate-v10g-official-runtime-evidence-boundary'
    assert c['parent_candidate_id']=='candidate-v10f-cap-scope-correction'
    assert c['strategy_delta']=='NONE' and not any(c['validation'].values())
    assert c['information_policy_delta']=='SOURCE_BASED_TEST_ACCESS_ADMISSIBILITY'
    assert len(m['instruction'])<=len(old['instruction'])*1.05
    assert len((ROOT/'configs/runtime_manifest.json').read_bytes())<=1.05*len(
        subprocess.check_output(['git','show',BASE+':configs/runtime_manifest.json'],cwd=ROOT))
    for word in ('K1 OFFICIAL-ACCESS','choices[].status_updates','HiddenRisk ±N','ADVERTISED_EFFECT',
                 'REALIZED_PUBLIC_RESPONSE','hypothesis','可达性未知保持 UNKNOWN','单独不授权S'):
        assert word in m['instruction']
    for prefix in ('K4 CLEANUP','K5 SUMMARY'):
        assert next(x for x in m['instruction'].splitlines() if x.startswith(prefix))==next(x for x in old['instruction'].splitlines() if x.startswith(prefix))
    assert m['instruction'][m['instruction'].index('STARTUP / NORMAL FLOW'):]==old['instruction'][old['instruction'].index('STARTUP / NORMAL FLOW'):]
    path='skills/rolling-planning/SKILL.md'
    before=subprocess.check_output(['git','show',BASE+':'+path],cwd=ROOT).decode().replace('\r\n','\n')
    after=(ROOT/path).read_text(encoding='utf-8')
    start,end='## Evidence / interfaces','## Review Plan / MODE / recovery'
    assert before[:before.index(start)]==after[:after.index(start)]
    assert before[before.index(end):]==after[after.index(end):]
    assert c['runtime_manifest']['sha256']==hashlib.sha256((ROOT/'configs/runtime_manifest.json').read_bytes()).hexdigest()
    assert c['runtime_manifest']['instruction_sha256']==hashlib.sha256(m['instruction'].encode()).hexdigest()
    for skill in c['skills']:
        assert skill['git_blob']==subprocess.check_output(['git','hash-object',skill['path']],cwd=ROOT,text=True).strip()


def test_offline_package(tmp_path):
    path=tmp_path/'submission';build_submission(ROOT,path)
    valid=validate_submission_contract(path)
    assert valid['submission_mode']=='skill_bundle' and len(valid['skill_ids'])==4


def test_protected_assets_and_immutable_history():
    paths=['skills/delivery-progress/SKILL.md','scripts/package_candidate.py','scripts/basis_preflight_audit.py',
           'scripts/policy_trace_audit.py','pyproject.toml','uv.lock',
           'docs/project/reviews/S09-25_INFORMATION_ACCESS_MATRIX.json',
           'docs/project/runs/v10f-run16-reviewer-validation.md','docs/project/runs/v10f-run16-reviewer-evidence.json']
    for path in paths:
        old=subprocess.check_output(['git','show',BASE+':'+path],cwd=ROOT)
        assert old==(ROOT/path).read_bytes() or old.replace(b'\r\n',b'\n')==(ROOT/path).read_bytes().replace(b'\r\n',b'\n')
    assert not subprocess.check_output(['git','diff',BASE,'--','career_sim_runner'],cwd=ROOT)
    for path in ('scripts/live_review_packet.py','scripts/reviewer_gate.py'):
        tree=ast.parse((ROOT/path).read_text(encoding='utf-8'))
        imports=[n.module for n in ast.walk(tree) if isinstance(n,ast.ImportFrom)]
        imports += [a.name for n in ast.walk(tree) if isinstance(n,ast.Import) for a in n.names]
        assert not any(s and s.split('.')[0] in ('subprocess','requests','socket','sqlite3','career_emulator','jiuwenswarm','openai') for s in imports)
