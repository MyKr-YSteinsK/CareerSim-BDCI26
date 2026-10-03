"""Offline reviewer annotations, incremental artifacts, transport/classification."""
import ast
import copy
import io
import json
from pathlib import Path
import subprocess
import sys

import pytest

from scripts.basis_preflight_audit import check_basis, parse_five_marker_header
from scripts.live_review_packet import ReviewStream, drain
from scripts.post_run_audit import audit
from scripts.reviewer_gate import OWNERS, validate_receipt as _validate_receipt

def validate_receipt(receipt, *, retrospective=True):
    return _validate_receipt(receipt, retrospective=retrospective)


ROOT=Path(__file__).resolve().parents[1]
CASES=json.loads((ROOT/'tests/fixtures/reviewer_gate_cases.json').read_text(encoding='utf-8'))
HEADER='[CTRL G=? P=A R=PASS RB=NONE] [DL i=NONE n=0 focus=NONE evidence=NA checkpoint=NOT_NEAR recognition=0] [POL B=OTHER F=OTHER RP=NA] [PROBE K=0???? E=0 C=0 S=0 F=NONE] [BC=PASS S=NONE CAP=NONE]'
SESSION='a'*32
START='2026-10-02T15:06:35.161860+00:00'
END='2026-10-02T15:10:21.345664+00:00'


def receipt(case):
    kind=case['expected']
    return dict(review_object=case['review_object'], owner=OWNERS[case['review_object']],
        clause_id=case['clause_id'],action_index=case['action_index'],
        public_evidence=case['public_evidence'],selected_candidate=case['selected_candidate'],
        direct_candidate_violation_link=case['direct_link'],
        counterexample_check={'checked':True,'result':'NO_COUNTEREXAMPLE' if kind.startswith('CONFIRMED') else 'COUNTEREXAMPLE_FOUND',
            'basis':case['counterexample'],'selected_candidate_material_risk':case.get('selected_candidate_material_risk')},
        verdict='VIOLATION' if kind.startswith('CONFIRMED') else 'NO_VIOLATION',
        confidence='HIGH',stop_class=kind)


@pytest.mark.parametrize('case',CASES,ids=lambda c:c['name'])
def test_historical_review_cases(case):
    result=validate_receipt(receipt(case))
    assert result['stop_class']==case['expected']
    assert result['stop']==case['expected'].startswith('CONFIRMED_')
    if 'annotation' in case:
        # Explicit certificate-only counterfactual for legacy RUN13; no raw rewrite.
        notes=case['notes'].replace('[BC=PASS]',case.get('projected_certificate','[BC=PASS]'))
        checked=check_basis(notes,case['annotation'])
        assert checked['status']==('PASS' if case['expected']=='NO_VIOLATION' else 'BLOCKED')
        if case.get('reason'): assert case['reason'] in checked['reasons']
    if case['review_object']=='HEADER_BC': assert not parse_five_marker_header(case['notes'])['valid']


@pytest.mark.parametrize('index',[0,1])
def test_event_theme_cannot_become_candidate_failure(index):
    r=receipt(CASES[index]); r.update(verdict='VIOLATION',stop_class='CONFIRMED_CANDIDATE_VIOLATION',direct_candidate_violation_link='Event is compliance themed')
    r['counterexample_check']['result']='NO_COUNTEREXAMPLE'
    with pytest.raises(ValueError,match='event theme'): validate_receipt(r)


@pytest.mark.parametrize('field',['direct_candidate_violation_link','counterexample_check','owner','confidence'])
def test_incomplete_or_mismatched_receipt_fails(field):
    r=receipt(CASES[4]); r.pop(field)
    with pytest.raises(ValueError): validate_receipt(r, retrospective=False)


def test_missing_direct_link_cannot_be_confirmed():
    r=receipt(CASES[4]); r['direct_candidate_violation_link']=None
    with pytest.raises(ValueError,match='direct link'): validate_receipt(r)


@pytest.mark.parametrize('link',[True,[],17,'   '])
def test_direct_link_must_be_substantive_text(link):
    r=receipt(CASES[4]); r['direct_candidate_violation_link']=link
    with pytest.raises(ValueError,match='direct link'): validate_receipt(r)


def test_uncertainty_may_stop_but_is_not_candidate_failure():
    r=receipt(CASES[0]); r.update(verdict='UNCERTAIN',stop_class='REVIEW_UNCERTAIN_MATERIAL',confidence='LOW',material_evidence_gap='Selected candidate evidence not available in bounded packet')
    out=validate_receipt(r); assert out['stop'] and not out['candidate_failure']
    del r['material_evidence_gap']
    with pytest.raises(ValueError,match='exact evidence gap'): validate_receipt(r)


def test_no_violation_never_stops_and_retrospective_defect_is_separate():
    r=receipt(CASES[0]); assert not validate_receipt(r)['stop']
    r.update(verdict='REVIEWER_DEFECT',stop_class='REVIEWER_DEFECT')
    with pytest.raises(ValueError): validate_receipt(r, retrospective=False)
    result=validate_receipt(r,retrospective=True)
    assert not result['stop'] and not result['candidate_failure']


def record(seq,kind,payload):
    return {'seq':seq,'ts':'2026-10-02T15:07:00+00:00','kind':kind,'payload':payload}


def call(seq,cid,name,args):
    return record(seq,'tool_call',{'tool_call':{'tool_call_id':cid,'name':name,'arguments':json.dumps(args)}})


def result(seq,cid,name,data):
    return record(seq,'tool_result',{'tool_call_id':cid,'tool_name':name,'raw_output':{'result':json.dumps(data)}})


def observe(month=1,feed=''):
    return {'current_state':{'session_id':SESSION,'time':{'current_month':month},
        'status':{'level':'L1','health':5,'dignity':10,'skill':3,'network':2,'output':1,'wealth':2,'energy':1,'HiddenRisk':999},
        'simulation_flags':{'alive':True,'failed':False}},
        'current_event':{'title':'公开事件','description':'公开语义','event_id':'filtered-id'},
        'events':feed,'choices':[{'choice':1,'action':'合法选项','description':'公开描述','next_node':'filtered-id'}]}


def stream(actions=40):
    rows=[call(1,'new','mcp_career-emulator_new_game',{}),result(2,'new','mcp_career-emulator_new_game',{'session_id':SESSION}),result(3,'o0','mcp_career-emulator_observe',observe())]
    for n in range(1,actions+1):
        rows.extend([call(n*3+1,'a'+str(n),'mcp_career-emulator_take_action',{'choice':1,'notes':HEADER}),
            result(n*3+2,'a'+str(n),'mcp_career-emulator_take_action',{'success':True}),
            result(n*3+3,'o'+str(n),'mcp_career-emulator_observe',observe(6 if n>=3 else 1,'【半年谈话】半年绩效奖金（C）' if n==3 else ''))])
    return rows


def test_packet_emits_at_each_boundary_before_next_action():
    monitor=ReviewStream(); packets=[]
    for row in stream():
        out=monitor.feed(row); packets.extend(out)
        for packet in out:
            if packet['type']=='HEARTBEAT_REVIEW_PACKET':
                assert packet['emitted_at_source_seq']==row['seq']
                assert packet['actions_read_at_emission']==packet['boundary_successes']
                assert all(x['fresh_observe'] for x in packet['rows'])
                assert packet['rows'][-1]['selected_candidate']['choice']==1
                assert 'filtered-id' not in json.dumps(packet) and 'hiddenrisk' not in json.dumps(packet).lower()
    heartbeats=[x for x in packets if x['type']=='HEARTBEAT_REVIEW_PACKET']
    assert [x['boundary_successes'] for x in heartbeats]==[3,12,40]
    assert all(x['semantic_verdict']=='PENDING_HUMAN_REVIEW' for x in heartbeats)


def test_formal_review_progress_is_emitted_before_pending_semantic_review_finishes():
    monitor=ReviewStream(); output=[]
    for row in stream(3): output.extend(monitor.feed(row))
    assert [x['type'] for x in output]==['FORMAL_REVIEW_PROGRESS','HEARTBEAT_REVIEW_PACKET']
    assert output[0]['report_required_now'] and output[0]['month']==6
    assert output[0]['source_seq']==12
    assert output[1]['semantic_verdict']=='PENDING_HUMAN_REVIEW'


def test_tail_partial_writes_and_duplicates():
    monitor=ReviewStream((1,)); content=''.join(json.dumps(x)+'\n' for x in stream(1))
    handle=io.StringIO(content[:-2]); out=[]
    drain(handle,monitor,out.append); assert not out
    pos=handle.tell(); handle.seek(0,2); handle.write(content[-2:]); handle.seek(pos)
    drain(handle,monitor,out.append); assert len(out)==1
    assert not monitor.feed(stream(1)[-1])


def test_cross_session_rejected():
    monitor=ReviewStream(session=SESSION)
    row=result(1,'x','mcp_career-emulator_observe',observe()); data=observe(); data['current_state']['session_id']='b'*32
    row=result(1,'x','mcp_career-emulator_observe',data)
    with pytest.raises(ValueError,match='cross-session'): monitor.feed(row)


def test_last_review_context_survives_into_next_submitted_action():
    monitor=ReviewStream(); output=[]
    for row in stream(12): output.extend(monitor.feed(row))
    packet=next(x for x in output if x.get('boundary_successes')==12)
    facts=packet['rows'][3]['relevant_review_sticky_facts']
    assert facts['last_public_review']['month']==6
    assert facts['last_public_review']['source_seq']==12
    assert facts['skill_sticky']=='UNKNOWN_NOT_SEPARATELY_EMITTED'


def fixture_files(tmp_path):
    events=tmp_path/'events.jsonl'; events.write_text(''.join(json.dumps(x)+'\n' for x in stream(3)),encoding='utf-8')
    transcript=tmp_path/'transcript.log'; transcript.write_text('SESSION='+SESSION,encoding='utf-8')
    runner=tmp_path/'runner.json'; runner.write_text(json.dumps({'exit_code':1,'play_start_utc':START,'play_end_utc':END}),encoding='utf-8')
    return events,transcript,runner


def test_exact_run15_window_through_actual_cli(tmp_path):
    events,transcript,runner=fixture_files(tmp_path); out=tmp_path/'summary.json'
    subprocess.run([sys.executable,'scripts/post_run_audit.py','--events',str(events),'--transcript',str(transcript),
        '--runner-result',str(runner),'--run-window-from-runner','--output',str(out)],cwd=ROOT,check=True,capture_output=True)
    summary=json.loads(out.read_text(encoding='utf-8')); window=summary['run']
    assert (window['input_start_exact'],window['input_end_exact'])==(START,END)
    assert (window['start_utc'],window['end_utc'])==(START,END)
    assert 'run_window_unknown_or_invalid' not in summary['limitations']
    assert window['runner_exit_code']==1
    assert summary['outcome']['classification']=='PARTIAL_EXECUTION_EXIT_CAUSE_UNKNOWN'


@pytest.mark.parametrize('kind,expected',[
    ('CONFIRMED_CANDIDATE_VIOLATION','DEVELOPMENT_ABORT_CANDIDATE_VIOLATION'),
    ('CONFIRMED_TELEMETRY_CONTRACT_VIOLATION','DEVELOPMENT_ABORT_TELEMETRY_CONTRACT'),
    ('REVIEW_UNCERTAIN_MATERIAL','DEVELOPMENT_ABORT_REVIEW_UNCERTAIN_MATERIAL'),
    ('REVIEWER_DEFECT','DEVELOPMENT_CENSORED_BY_REVIEWER_FALSE_POSITIVE'),
])
def test_development_termination_not_provider_failure(tmp_path,kind,expected):
    events,transcript,runner=fixture_files(tmp_path)
    r=receipt(CASES[7] if kind=='CONFIRMED_TELEMETRY_CONTRACT_VIOLATION' else CASES[4]); r['action_index']=2
    r['stop_class']=kind
    if kind=='REVIEW_UNCERTAIN_MATERIAL': r.update(verdict='UNCERTAIN',material_evidence_gap='Exact claimed binding not available')
    if kind=='REVIEWER_DEFECT': r['verdict']='REVIEWER_DEFECT'
    stop=tmp_path/'stop.json'; stop.write_text(json.dumps({'session_id':SESSION,'controller_authorized_stop':True,'reviewer_receipt':r}),encoding='utf-8')
    summary=audit(events,transcript,None,runner,run_window_from_runner=True,development_stop=stop)
    assert summary['outcome']['classification']==expected
    assert summary['run']['runner_exit_code']==1
    assert summary['outcome']['terminal_fresh_score']=='UNKNOWN'


def test_development_stop_bad_session_or_no_violation_rejected(tmp_path):
    events,transcript,runner=fixture_files(tmp_path); stop=tmp_path/'stop.json'
    for session in ('b'*32,SESSION):
        stop.write_text(json.dumps({'session_id':session,'controller_authorized_stop':True,'reviewer_receipt':receipt(CASES[0])}),encoding='utf-8')
        with pytest.raises(ValueError): audit(events,transcript,None,runner,development_stop=stop)


def test_structured_natural_terminal_cannot_be_reclassified_as_development_abort(tmp_path):
    events,transcript,runner=fixture_files(tmp_path)
    rows=[json.loads(x) for x in events.read_text().splitlines()]
    data=json.loads(rows[-1]['payload']['raw_output']['result']); data['game']={'ended':True}
    rows[-1]['payload']['raw_output']['result']=json.dumps(data)
    events.write_text(''.join(json.dumps(x)+'\n' for x in rows),encoding='utf-8')
    assert audit(events,transcript,None,runner)['outcome']['classification']=='EARLY_NATURAL_TERMINAL'
    r=receipt(CASES[0]); r.update(verdict='REVIEWER_DEFECT',stop_class='REVIEWER_DEFECT')
    stop=tmp_path/'stop.json'; stop.write_text(json.dumps({'session_id':SESSION,'controller_authorized_stop':True,'reviewer_receipt':r}),encoding='utf-8')
    with pytest.raises(ValueError,match='natural terminal'): audit(events,transcript,None,runner,development_stop=stop)


def test_selected_candidate_material_risk_can_support_review_label_violation():
    r=receipt(CASES[0]); r.update(verdict='VIOLATION',stop_class='CONFIRMED_CANDIDATE_VIOLATION',
        selected_candidate='Share marked confidential file',direct_candidate_violation_link='Chosen candidate itself discloses confidential material while using Quick Gate PASS')
    r['counterexample_check'].update(result='NO_COUNTEREXAMPLE',selected_candidate_material_risk=True)
    assert validate_receipt(r)['stop']


def test_runner_window_rejects_conflicting_cli_override(tmp_path):
    events,transcript,runner=fixture_files(tmp_path)
    with pytest.raises(ValueError,match='mutually exclusive'):
        audit(events,transcript,None,runner,run_start=START,run_end=END,run_window_from_runner=True)


@pytest.mark.parametrize('category',['PROVIDER','RUNTIME'])
def test_explicit_technical_evidence_is_separate(tmp_path,category):
    events,transcript,runner=fixture_files(tmp_path)
    data=json.loads(runner.read_text()); data['technical_failure_evidence']={'category':category,'source':'exact scoped stdout receipt'}
    runner.write_text(json.dumps(data),encoding='utf-8')
    summary=audit(events,transcript,None,runner)
    assert summary['outcome']['classification']=='TECHNICAL_'+category+'_FAILURE'


@pytest.mark.parametrize('value',[None,17,'10/02/2026 23:06:35','2026-10-02T15:06:35'])
def test_bad_runner_timestamp_fails_without_coercion(tmp_path,value):
    events,transcript,runner=fixture_files(tmp_path)
    runner.write_text(json.dumps({'exit_code':1,'play_start_utc':value,'play_end_utc':END}),encoding='utf-8')
    with pytest.raises(ValueError): audit(events,transcript,None,runner,run_window_from_runner=True)


def test_poll_reader_cli_replay_is_public_and_does_not_mutate_input(tmp_path):
    events,_,_=fixture_files(tmp_path); before=events.read_bytes(); out=tmp_path/'packets'
    completed=subprocess.run([sys.executable,'-m','scripts.live_review_packet','--events',str(events),'--output-dir',str(out),
        '--heartbeats','3'],cwd=ROOT,check=True,capture_output=True,text=True)
    assert events.read_bytes()==before
    lines=[json.loads(x) for x in completed.stdout.splitlines()]
    assert [x['type'] for x in lines]==['FORMAL_REVIEW_PROGRESS','HEARTBEAT_REVIEW_PACKET']
    assert (out/'heartbeat-3.json').exists() and (out/'review-6.json').exists()


def test_read_only_modules_have_no_live_side_effect_imports():
    for path in ('scripts/live_review_packet.py','scripts/reviewer_gate.py'):
        source=(ROOT/path).read_text(encoding='utf-8'); tree=ast.parse(source)
        imports=[]
        for node in ast.walk(tree):
            if isinstance(node,ast.Import): imports.extend(x.name for x in node.names)
            if isinstance(node,ast.ImportFrom): imports.append(node.module)
        assert not any(x and x.split('.')[0] in ('subprocess','requests','socket','sqlite3','career_sim_runner','jiuwenswarm','openai') for x in imports)


def test_protected_candidate_assets_unchanged():
    paths=['configs/runtime_manifest.json','configs/current_candidate.json','uv.lock','pyproject.toml','scripts/package_candidate.py','scripts/basis_preflight_audit.py','scripts/policy_trace_audit.py']
    paths += ['skills/'+s+'/SKILL.md' for s in ('structured-state-board','rolling-planning','delivery-progress','risk-review')]
    for path in paths:
        old=subprocess.check_output(['git','show','45ffc07:'+path],cwd=ROOT)
        assert old.replace(b'\r\n',b'\n')==(ROOT/path).read_bytes().replace(b'\r\n',b'\n')
