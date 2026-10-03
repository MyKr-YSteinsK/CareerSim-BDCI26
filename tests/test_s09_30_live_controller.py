"""Exercise the real supervisor stop seam with fake process handles, never live."""
import copy
import json
from pathlib import Path
import subprocess

import pytest

from scripts.live_run_controller import LiveRunController, supervise_runner
from scripts.post_run_audit import audit
from scripts.reviewer_gate import S1_ISSUES
from tests.test_s09_24_reviewer_reliability import SESSION, CASES, receipt, stream, result, observe
from tests.test_s09_29_reviewer_severity import HIST, new, s2
from tests.test_s09_26_official_access import proof
from tests.test_post_run_audit import _fixtures

ROOT=Path(__file__).resolve().parents[1]


class FakeRunner:
    def __init__(self,exit_code=None):
        self.returncode=exit_code;self.terminations=0
    def poll(self):return self.returncode
    def terminate(self):self.terminations+=1;self.returncode=1


def controller(tmp_path,session=SESSION,**kwargs):
    process=FakeRunner();notifications=[]
    c=LiveRunController(process,tmp_path/'controller',session,
        emit=lambda tag,**data:notifications.append((tag,data)),**kwargs)
    return c,process,notifications


@pytest.mark.parametrize('case',HIST,ids=lambda c:c['name'])
def test_historical_future_controller_emits_no_stop(case,tmp_path):
    c,runner,_=controller(tmp_path,session=case['session'])
    c.monitor.actions=case['legacy']['action_index']
    r=new(case['legacy'],issue=case['issue_type'],session=case['session'])
    outcome=c.consume_receipt(r,receipt_id=case['source'])
    assert outcome['accepted'] and outcome['severity']==case['expected_severity']
    assert outcome['live_action']=='CONTINUE' and outcome['score_evidence_eligible']=='YES'
    assert not outcome['stop_request_emitted'] and runner.terminations==0
    assert not (c.output/'development-stop.json').exists()
    saved=json.loads((c.output/'reviewer-receipts.json').read_text(encoding='utf-8'))
    assert saved['receipts']==[r]
    if case['name'].startswith('RUN18'):
        assert outcome['policy_verdict']=='FAIL' and r['run_validity']=='VALID'
        assert r['public_evidence']['submission_seq']==117


@pytest.mark.parametrize('issue',sorted(S1_ISSUES))
def test_S1_never_reaches_process_stop_seam(issue,tmp_path):
    c,runner,events=controller(tmp_path);c.monitor.actions=40
    d=new(issue=issue);out=c.consume_receipt(d,receipt_id='S1')
    assert out['accepted'] and not out['stop_request_emitted']
    assert runner.terminations==0 and out['run_continues']
    assert events[-1][0]=='POLICY_WARNING_CONTINUE'
    assert out['receipt_id']=='S1' and out['warning_time']


def test_RUN16_official_delta_is_S0_controller_continue(tmp_path):
    c,runner,_=controller(tmp_path);c.monitor.actions=11
    r=receipt(CASES[0]);r.update(review_object='PLANNING_RANKING',owner='rolling-planning',
        clause_id='K1/OFFICIAL-ACCESS',information_boundary_version=2,information_access=proof(),action_index=11)
    out=c.consume_receipt(new(r,issue='OFFICIAL_EFFECT'),receipt_id='RUN16 official delta')
    assert out['severity']=='S0' and out['live_action']=='CONTINUE'
    assert out['score_evidence_eligible']=='YES' and runner.terminations==0


@pytest.mark.parametrize('issue',['IDENTITY_CORRUPTION','STATE_ATTRIBUTION_CORRUPTION',
    'TEST_CONTAMINATION','MEASUREMENT_FAILURE','UNAUTHORIZED_RUNTIME_MUTATION'])
def test_validated_S2_emits_exactly_one_controlled_stop(issue,tmp_path):
    c,runner,_=controller(tmp_path);c.monitor.actions=1
    out=c.consume_receipt(s2(issue),receipt_id='S2')
    assert (out['severity'],out['live_action'],out['stop_request_emitted'])==('S2','STOP',True)
    assert runner.terminations==1 and out['score_evidence_eligible']=='NO'
    stop=json.loads((c.output/'development-stop.json').read_text(encoding='utf-8'))
    assert stop['stop_authority']=='VALIDATED_S2' and stop['controller_authorized_stop']
    c.consume_receipt(s2(issue),receipt_id='duplicate')
    assert runner.terminations==1


def test_exact_cross_session_stream_creates_validated_S2_not_marker_stop(tmp_path):
    c,runner,_=controller(tmp_path)
    c.process_available(stream(1))
    data=observe();data['current_state']['session_id']='other'
    c.process_available([result(100,'other','mcp_career-emulator_observe',data)])
    assert runner.terminations==1 and c.receipts[-1]['severity']=='S2'
    assert c.stop_metadata['stop_authority']=='VALIDATED_S2'


@pytest.mark.parametrize('mutation',['legacy','v2','missing_severity','tamper','session','mode'])
def test_invalid_authority_rejected_without_process_side_effect(mutation,tmp_path):
    c,runner,_=controller(tmp_path);c.monitor.actions=40
    d=new()
    if mutation=='legacy':d=receipt(CASES[4])
    if mutation=='v2':d=receipt(CASES[4]);d['schema_version']=2
    if mutation=='missing_severity':d.pop('severity')
    if mutation=='tamper':d['live_action']='STOP'
    if mutation=='session':d['session_id']='wrong'
    if mutation=='mode':d=new(evaluation_mode='MECHANISM_VALIDATION_CENSOR',censor_authorization=auth())
    out=c.consume_receipt(d,receipt_id=mutation)
    assert not out['accepted'] and not out['stop_request_emitted'] and runner.terminations==0
    assert not (c.output/'development-stop.json').exists()


def auth():
    return dict(plan='Synthetic preauthorized run',target_mechanism='Energy',
        exact_censor_trigger='confirmed remaining recipe',issue_type='ENERGY_RECIPE',
        budget=1,why_score_unimportant='Mechanism validation only',authorized_before_run=True,
        stop_class='MECHANISM_VALIDATION_CENSORED')


def test_censor_can_only_stop_exact_pre_run_mode_authorization(tmp_path):
    a=auth();c,runner,_=controller(tmp_path,evaluation_mode='MECHANISM_VALIDATION_CENSOR',censor_authorization=a)
    c.monitor.actions=40
    d=new(evaluation_mode=c.mode,censor_authorization=a)
    assert not c.consume_receipt(d,receipt_id='missing trigger')['accepted']
    d['censor_trigger']='wrong'
    assert not c.consume_receipt(d,receipt_id='wrong trigger')['accepted']
    d['censor_trigger']=a['exact_censor_trigger']
    changed=copy.deepcopy(d);changed['censor_authorization']['budget']=2
    assert not c.consume_receipt(changed,receipt_id='wrong budget')['accepted']
    unrelated=new(issue='LOWEST_STAT',evaluation_mode=c.mode,censor_authorization=a)
    assert not c.consume_receipt(unrelated,receipt_id='unrelated')['stop_request_emitted']
    assert runner.terminations==0
    assert c.consume_receipt(d,receipt_id='exact')['stop_request_emitted']
    assert runner.terminations==1 and c.stop_metadata['stop_authority']=='AUTHORIZED_MECHANISM_CENSOR'


def test_censor_mode_blocks_before_supervisor_start_without_authorization(tmp_path):
    with pytest.raises(ValueError,match='authorized before'):
        controller(tmp_path,evaluation_mode='MECHANISM_VALIDATION_CENSOR')
    a=auth();a['authorized_before_run']=False
    with pytest.raises(ValueError):controller(tmp_path,evaluation_mode='MECHANISM_VALIDATION_CENSOR',censor_authorization=a)
    with pytest.raises(ValueError):controller(tmp_path,evaluation_mode='MECHANISM_VALIDATION_CENSOR',censor_authorization=auth(),run_budget=2)
    assert not (tmp_path/'controller').exists()


def test_reviewer_stop_seam_itself_revalidates_authority(tmp_path):
    c,runner,_=controller(tmp_path);c.monitor.actions=40
    r=new()
    with pytest.raises(ValueError,match='no v3 reviewer stop authority'):
        c._emit_reviewer_stop(r,{'severity':'S2','live_action':'STOP'},'tampered checked output',{})
    assert runner.terminations==0


@pytest.mark.parametrize('issue',['ENERGY_RECIPE','MEASUREMENT_FAILURE'])
def test_natural_terminal_precedes_delayed_policy_or_S2_stop(issue,tmp_path):
    c,runner,events=controller(tmp_path)
    c.process_available(stream(3))
    data=observe();data['game']={'ended':True}
    c.process_available([result(100,'terminal','mcp_career-emulator_observe',data)])
    r=s2(issue) if issue=='MEASUREMENT_FAILURE' else new()
    r['action_index']=1
    out=c.consume_receipt(r,receipt_id='late')
    assert out['suppressed_by']=='NATURAL_TERMINAL' and not out['stop_request_emitted']
    assert runner.terminations==0 and c.natural['source_seq']==100
    assert not (c.output/'development-stop.json').exists()


def test_natural_simulator_flags_and_ending_score_precede_S2(tmp_path):
    c,runner,_=controller(tmp_path);c.process_available(stream(1))
    d=observe();d['current_state']['simulation_flags'].update(alive=False,failed=True)
    d['ending_score']={'completed':False,'survival_months':6}
    c.process_available([result(100,'end','mcp_career-emulator_observe',d)])
    assert c.natural is not None
    c.consume_receipt(s2('IDENTITY_CORRUPTION'),receipt_id='late')
    assert runner.terminations==0


def test_technical_precedence_requires_direct_evidence_not_exit_code(tmp_path):
    c,runner,_=controller(tmp_path);c.monitor.actions=1
    with pytest.raises(ValueError):c.technical_failure(dict(exit_code=1))
    c.technical_failure(dict(category='PROVIDER',source='Exact scoped unrecoverable failure'))
    out=c.consume_receipt(s2('IDENTITY_CORRUPTION'),receipt_id='late')
    assert out['suppressed_by']=='TECHNICAL_UNRECOVERABLE' and runner.terminations==1
    assert not (c.output/'development-stop.json').exists()


def test_formal_review_precedes_pending_semantic_warning_and_never_pauses(tmp_path):
    c,runner,events=controller(tmp_path)
    path=tmp_path/'h1-decision.json';d=new();d['action_index']=3
    path.write_text(json.dumps({'receipts':[d]}),encoding='utf-8')
    c.process_available(stream(3),[path])
    tags=[x[0] for x in events]
    assert tags.index('FORMAL_REVIEW_PROGRESS')<tags.index('POLICY_WARNING_CONTINUE')
    assert tags.index('FORMAL_REVIEW_PROGRESS')<tags.index('HEARTBEAT_REVIEW_READY')
    assert runner.terminations==0


def test_attributable_malformed_header_does_not_trigger_blanket_stop(tmp_path):
    c,runner,_=controller(tmp_path);rows=stream(3)
    for row in rows:
        call=row['payload'].get('tool_call',{})
        if 'take_action' in call.get('name',''):
            args=json.loads(call['arguments']);args['notes']='prose '+args['notes'];call['arguments']=json.dumps(args)
    c.process_available(rows)
    assert not c.monitor.rows[0]['header']['valid'] and runner.terminations==0
    d=new(receipt(CASES[7]),issue='MARKER_DRIFT');d['action_index']=1
    assert not c.consume_receipt(d,receipt_id='header')['stop_request_emitted']


def test_S2_prioritized_over_censor_within_same_batch(tmp_path):
    a=auth();c,runner,_=controller(tmp_path,evaluation_mode='MECHANISM_VALIDATION_CENSOR',censor_authorization=a)
    c.monitor.actions=40
    target=new(evaluation_mode=c.mode,censor_authorization=a);target['censor_trigger']=a['exact_censor_trigger']
    d=s2('IDENTITY_CORRUPTION');d['evaluation_mode']=c.mode;d['censor_authorization']=a
    path=tmp_path/'both-decision.json';path.write_text(json.dumps({'receipts':[target,d]}),encoding='utf-8')
    c.process_available([],[path])
    assert runner.terminations==1 and c.stop_metadata['stop_authority']=='VALIDATED_S2'


def test_real_supervisor_loop_wires_process_and_full_score_audit(tmp_path):
    e,t,score,r,_=_fixtures(tmp_path);decisions=tmp_path/'decisions';decisions.mkdir()
    d=new();d['action_index']=1
    (decisions/'h1-decision.json').write_text(json.dumps({'receipts':[d]}),encoding='utf-8')
    # Natural outcome already present in stream. The loop still drains it first.
    process=FakeRunner(exit_code=0)
    c=supervise_runner(process,events=e,output_dir=tmp_path/'supervisor',session_id=SESSION,
        decision_dir=decisions,emit=lambda *a,**k:None)
    assert process.terminations==0 and c.natural and len(c.receipts)==1
    out=audit(e,t,score,r,reviewer_receipts=c.output/'reviewer-receipts.json')
    assert out['outcome']['classification']=='VALID_FULL_RUN_WITH_POLICY_VIOLATIONS'
    assert not out['reviewer']['stopped'] and out['reviewer']['score_evidence_eligible']=='YES'


def test_supervisor_loop_S2_reaches_actual_stop_request_seam(tmp_path):
    e=tmp_path/'events.jsonl';e.write_text(''.join(json.dumps(r)+'\n' for r in stream(1)),encoding='utf-8')
    decisions=tmp_path/'decisions';decisions.mkdir()
    (decisions/'h1-decision.json').write_text(json.dumps({'receipts':[s2('MEASUREMENT_FAILURE')]}),encoding='utf-8')
    process=FakeRunner()
    c=supervise_runner(process,events=e,output_dir=tmp_path/'supervisor',session_id=SESSION,
        decision_dir=decisions,emit=lambda *a,**k:None)
    assert process.terminations==1 and c.stop_metadata


def test_protected_assets_and_tracked_history_are_immutable():
    paths=['configs','skills','career_sim_runner','pyproject.toml','uv.lock','docs/project/runs']
    assert not subprocess.check_output(['git','diff','8925f25','--',*paths],cwd=ROOT,text=True).strip()
