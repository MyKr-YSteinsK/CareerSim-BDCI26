"""Source-backed historical projections and synthetic severity decisions, offline only."""
import copy
import json
from pathlib import Path
import subprocess
import sys

import pytest

from scripts.post_run_audit import audit
from scripts.reviewer_gate import (INTEGRITY_FIELDS, S1_ISSUES, S2_ISSUES,
    aggregate_reviews, development_classification, severity_receipt, validate_receipt)
from tests.test_s09_24_reviewer_reliability import CASES, receipt, SESSION, fixture_files
from tests.test_s09_26_official_access import proof
from tests.test_post_run_audit import _fixtures

ROOT = Path(__file__).resolve().parents[1]
HIST = json.loads((ROOT/'tests/fixtures/reviewer_severity_cases.json').read_text(encoding='utf-8'))
VALID = {k: 'VALID' for k in INTEGRITY_FIELDS}


def new(legacy=None, issue='ENERGY_RECIPE', session=SESSION, **kwargs):
    legacy = copy.deepcopy(legacy or receipt(CASES[4]))
    return severity_receipt(legacy, session_id=session, issue_type=issue,
        run_integrity=kwargs.pop('run_integrity', VALID), **kwargs)


@pytest.mark.parametrize('case', HIST, ids=lambda c: c['name'])
def test_historical_severity_projection_and_original_compatibility(case):
    old = copy.deepcopy(case['legacy'])
    historical = validate_receipt(old, retrospective=True)
    future = new(old, issue=case['issue_type'], session=case['session'])
    checked = validate_receipt(future)
    assert old == case['legacy']
    assert historical['stop'] == old['stop_class'].startswith('CONFIRMED_')
    assert checked['severity'] == case['expected_severity']
    assert checked['policy_verdict'] == ('FAIL' if checked['severity']=='S1' else 'PASS')
    assert not checked['stop'] and checked['live_action']=='CONTINUE'
    assert checked['run_validity']=='VALID' and checked['score_evidence_eligible']=='YES'


def test_run12_attribution_is_established_separately_from_header():
    actual = json.loads((ROOT/'docs/project/runs/v10c-run12-early-contract-evidence.json').read_text(encoding='utf-8'))
    assert actual['successful_actions']==actual['fresh_action_observe']==3
    assert actual['observes']==4 and actual['session']==actual['last_public_state']['session_id']
    assert actual['metrics']['full_five_marker_valid']==0
    # S1 is based on the independent action/session evidence, not the marker.
    assert all(c['expected_severity']=='S1' for c in HIST if c['name'].startswith('RUN12'))


def test_run18_mandatory_exact_receipt_projection():
    d=json.loads((ROOT/'docs/project/runs/v10h-run18-dynamic-survival-evidence.json').read_text(encoding='utf-8'))
    c=next(c for c in HIST if c['name']=='RUN18_a12_remaining_recipe')
    assert c['legacy']==d['stop_receipt']
    assert d['classification']=='DEVELOPMENT_ABORT_CANDIDATE_VIOLATION'
    result=validate_receipt(new(c['legacy'],session=d['session']))
    assert (result['policy_verdict'],result['severity'],result['live_action'],result['score_evidence_eligible'])==('FAIL','S1','CONTINUE','YES')


def test_run16_official_delta_is_S0_not_contamination():
    old=receipt(CASES[0]);old.update(review_object='PLANNING_RANKING',owner='rolling-planning',
        action_index=11,clause_id='K1/OFFICIAL-ACCESS',information_boundary_version=2,information_access=proof())
    out=validate_receipt(new(old,issue='OFFICIAL_EFFECT'))
    assert out['severity']=='S0' and not out['stop'] and out['score_evidence_eligible']=='YES'


@pytest.mark.parametrize('issue', sorted(S1_ISSUES))
def test_each_policy_failure_continues_without_stop_request(issue):
    old=receipt(CASES[7] if issue in ('MARKER_DRIFT','FRESH_RERANK_DRIFT') else CASES[4])
    if issue=='FRESH_RERANK_DRIFT':old.update(review_object='FRESH_OBSERVE',owner='executor/runtime')
    out=validate_receipt(new(old,issue=issue))
    assert out['severity']=='S1' and out['candidate_failure']==(old['review_object']=='PLANNING_RANKING')
    assert out['live_action']=='CONTINUE' and not out['stop']


def s2(issue, uncertain=False):
    old=receipt(CASES[7]);old.update(review_object='RUN_INTEGRITY',owner='development-reviewer',
        clause_id='Integrity/'+issue,action_index=1,
        direct_candidate_violation_link='Synthetic independent identity/context evidence corrupts attribution')
    integrity=dict(VALID);integrity[S2_ISSUES[issue]]='UNCERTAIN' if uncertain else 'INVALID'
    evidence=dict(source='Synthetic exact source seq, not an official hidden rule',
        direct_link={'IDENTITY_CORRUPTION':'Expected manifest hash A, observed mid-run hash B',
            'TEST_CONTAMINATION':'Raw private Test/DB content actually injected and used in ranking',
            'STATE_ATTRIBUTION_CORRUPTION':'Successful effect followed by unknown session/state; retry can duplicate effect',
            'MEASUREMENT_FAILURE':'Events belong to another run; current action cannot be attributed',
            'UNAUTHORIZED_RUNTIME_MUTATION':'Unauthorized dependency/config mutation during run'}[issue],
        dependency_used=True,proven_unavailable_to_Test=True)
    return new(old,issue=issue,run_integrity=integrity,severity_evidence=evidence)


@pytest.mark.parametrize('issue', sorted(S2_ISSUES))
def test_synthetic_invalidating_regressions_hard_stop(issue):
    out=validate_receipt(s2(issue))
    assert (out['severity'],out['live_action'],out['run_validity'],out['score_evidence_eligible'])==('S2','STOP','INVALID','NO')
    assert out['stop'] and not out['candidate_failure']


def test_cross_session_and_unsafe_side_effect_have_same_bounded_S2_axis():
    for fact in ('action session B while fresh observe is session A',
                 'successful action outcome unknown; resend can duplicate effect'):
        d=s2('STATE_ATTRIBUTION_CORRUPTION');d['severity_evidence']['direct_link']=fact
        assert validate_receipt(d)['stop']


def test_unrecoverable_context_uncertainty_is_not_candidate_failure():
    d=s2('MEASUREMENT_FAILURE',uncertain=True)
    out=validate_receipt(d)
    assert out['stop'] and out['score_evidence_eligible']=='UNKNOWN' and not out['candidate_failure']


def test_policy_uncertainty_alone_never_stops_valid_full_score_run():
    old=receipt(CASES[0]);old.update(verdict='UNCERTAIN',stop_class='REVIEW_UNCERTAIN_MATERIAL',
        confidence='LOW',material_evidence_gap='Choice quality/rationale uncertain; exact state/session still attributable')
    out=validate_receipt(new(old,issue='POLICY_UNCERTAINTY'))
    assert (out['policy_verdict'],out['severity'],out['live_action'],out['score_evidence_eligible'])==('UNKNOWN','S0','CONTINUE','YES')


@pytest.mark.parametrize('field', ['source','direct_link','dependency_used','proven_unavailable_to_Test'])
def test_contamination_requires_independent_proof(field):
    d=s2('TEST_CONTAMINATION');d['severity_evidence'].pop(field)
    with pytest.raises(ValueError):validate_receipt(d)


def test_proven_private_input_uses_existing_K1_provenance():
    old=receipt(CASES[4]);p=proof(accessibility='NO',official_path='UNAVAILABLE',
        context_complete=True,support_type='NONE')
    for k in ('official_agent_input','context_path','context_value'):p.pop(k)
    old.update(clause_id='K1/PrivateTest',information_boundary_version=2,information_access=p)
    d=s2('TEST_CONTAMINATION')
    d=new(old,issue='TEST_CONTAMINATION',run_integrity=d['run_integrity'],severity_evidence=d['severity_evidence'])
    assert validate_receipt(d)['stop']


def test_invented_hidden_stock_is_not_proven_private_dependency():
    old=receipt(CASES[4]);p=proof(claim_type='CURRENT_STOCK',support_type='DELTA_EFFECT',context_complete=True)
    old.update(clause_id='K1/UnsupportedStock',information_boundary_version=2,information_access=p)
    d=new(old,issue='UNSUPPORTED_CAP')
    assert validate_receipt(d)['severity']=='S1'
    corruption=s2('TEST_CONTAMINATION')
    with pytest.raises(ValueError,match='not proven contamination'):
        new(old,issue='TEST_CONTAMINATION',run_integrity=corruption['run_integrity'],severity_evidence=corruption['severity_evidence'])


@pytest.mark.parametrize('field,value', [('severity','S2'),('live_action','STOP'),('policy_verdict','PASS'),
    ('run_validity','INVALID'),('score_evidence_eligible','NO')])
def test_cannot_promote_S1_by_editing_decision_fields(field,value):
    d=new();d[field]=value
    with pytest.raises(ValueError,match='contradict'):validate_receipt(d)


def test_unknown_issue_or_integrity_cannot_create_new_S2_category():
    d=new();d['issue_type']='SLOW_REVIEWER'
    with pytest.raises(ValueError):validate_receipt(d)
    d=new();d['run_integrity']['measurement']='UNCERTAIN'
    with pytest.raises(ValueError,match='independent S2'):validate_receipt(d)


def test_mode_B_requires_prior_exact_censor_authorization():
    auth=dict(plan='Synthetic authorized Plan',target_mechanism='fresh Energy rerank',
        exact_censor_trigger='confirmed ENERGY_RECIPE',why_score_unimportant='mechanism-only experiment',
        issue_type='ENERGY_RECIPE',budget=1,authorized_before_run=True,stop_class='MECHANISM_VALIDATION_CENSORED')
    d=new(evaluation_mode='MECHANISM_VALIDATION_CENSOR',censor_authorization=auth)
    assert validate_receipt(d)['stop']
    assert not validate_receipt(new(issue='LOWEST_STAT',evaluation_mode='MECHANISM_VALIDATION_CENSOR',censor_authorization=auth))['stop']
    for field in ('plan','exact_censor_trigger','why_score_unimportant','budget','authorized_before_run'):
        broken=dict(auth);broken.pop(field)
        with pytest.raises(ValueError):new(evaluation_mode='MECHANISM_VALIDATION_CENSOR',censor_authorization=broken)


def test_legacy_stop_can_only_be_read_under_explicit_retrospective_mode():
    old=receipt(CASES[4])
    assert validate_receipt(old,retrospective=True)['stop']
    with pytest.raises(ValueError,match='schema_version=3'):validate_receipt(old)


def test_retrospective_flag_cannot_bypass_v3_access_provenance():
    d=new();d['clause_id']='K1/PrivateInput'
    with pytest.raises(ValueError,match='provenance'):validate_receipt(d,retrospective=True)
    d=new();d['schema_version']=99
    with pytest.raises(ValueError,match='unsupported'):validate_receipt(d,retrospective=True)


def test_empty_review_envelope_does_not_claim_policy_PASS():
    out=aggregate_reviews(dict(schema_version=3,session_id=SESSION,receipts=[]),SESSION,0)
    assert out['policy_adherence']=='UNKNOWN' and out['S1_count']==0


def envelope(tmp_path, decisions):
    path=tmp_path/'reviews.json';path.write_text(json.dumps(dict(schema_version=3,session_id=SESSION,receipts=decisions)),encoding='utf-8')
    return path


def test_full_natural_score_with_S1_is_valid_and_not_censored(tmp_path):
    e,t,sc,r,_=_fixtures(tmp_path);d=new();d['action_index']=1
    out=audit(e,t,sc,r,reviewer_receipts=envelope(tmp_path,[d]))
    assert out['outcome']['classification']=='VALID_FULL_RUN_WITH_POLICY_VIOLATIONS'
    assert out['outcome']['terminal_fresh_score']['quantitative_score']==64.0
    assert out['reviewer']['terminal_classification']=='VALID_48M_COMPLETION'
    assert out['reviewer']['S1_count']==1 and out['reviewer']['policy_adherence']=='FAIL'
    assert not out['reviewer']['stopped'] and not out['reviewer']['stop_requested']
    assert out['reviewer']['score_evidence_eligible']=='YES'


def test_early_natural_terminal_stays_valid_with_S1(tmp_path):
    e,t,sc,r,_=_fixtures(tmp_path)
    lines=[json.loads(x) for x in e.read_text(encoding='utf-8').splitlines()]
    data=json.loads(lines[-1]['payload']['raw_output']['result']);data['ending_score'].update(completed=False,survival_months=6)
    data['current_state']['time']['current_month']=6
    lines[-1]['payload']['raw_output']['result']=json.dumps(data);e.write_text(''.join(json.dumps(x)+'\n' for x in lines),encoding='utf-8')
    d=new();d['action_index']=1
    out=audit(e,t,sc,r,reviewer_receipts=envelope(tmp_path,[d]))
    assert out['outcome']['classification']=='VALID_NATURAL_TERMINAL_WITH_POLICY_VIOLATIONS'
    assert out['reviewer']['score_evidence_eligible']=='YES'


def test_partial_score_eligibility_does_not_fabricate_final_score(tmp_path):
    e,t,r=fixture_files(tmp_path);d=new();d['action_index']=1
    out=audit(e,t,None,r,reviewer_receipts=envelope(tmp_path,[d]))
    assert out['reviewer']['score_evidence_eligible']=='YES' and not out['reviewer']['score_observed']
    assert out['outcome']['classification']=='PARTIAL_EXECUTION_EXIT_CAUSE_UNKNOWN'


def test_S1_cannot_be_mislabeled_as_actual_development_stop(tmp_path):
    e,t,r=fixture_files(tmp_path);d=new();d['action_index']=1
    stop=tmp_path/'stop.json';stop.write_text(json.dumps(dict(session_id=SESSION,controller_authorized_stop=True,reviewer_receipt=d)),encoding='utf-8')
    with pytest.raises(ValueError,match='CONTINUE'):audit(e,t,None,r,development_stop=stop)


def test_S2_stop_aggregation_and_natural_invalidation_are_distinct(tmp_path):
    e,t,r=fixture_files(tmp_path);d=s2('MEASUREMENT_FAILURE')
    stop=tmp_path/'stop.json';stop.write_text(json.dumps(dict(session_id=SESSION,controller_authorized_stop=True,reviewer_receipt=d)),encoding='utf-8')
    out=audit(e,t,None,r,development_stop=stop)
    assert out['outcome']['classification']=='DEVELOPMENT_STOP_RUN_INVALIDATING'
    assert out['reviewer']['stopped'] and out['reviewer']['score_evidence_eligible']=='NO'
    e,t,sc,r,_=_fixtures(tmp_path)
    out=audit(e,t,sc,r,reviewer_receipts=envelope(tmp_path,[d]))
    assert out['outcome']['classification']=='RUN_EVIDENCE_INVALID_OR_UNCERTAIN'
    assert out['reviewer']['natural_terminal'] and not out['reviewer']['stopped']
    assert out['reviewer']['stop_recommended'] and out['reviewer']['stop_requested']=='UNKNOWN'
    assert out['outcome']['terminal_fresh_score']['quantitative_score']==64.0


def test_actual_stop_must_be_in_supplied_review_envelope(tmp_path):
    e,t,r=fixture_files(tmp_path);d=s2('IDENTITY_CORRUPTION')
    stop=tmp_path/'stop.json';stop.write_text(json.dumps(dict(session_id=SESSION,
        controller_authorized_stop=True,reviewer_receipt=d)),encoding='utf-8')
    with pytest.raises(ValueError,match='absent from review envelope'):
        audit(e,t,None,r,development_stop=stop,reviewer_receipts=envelope(tmp_path,[]))


def test_mode_B_classification_and_unknown_stop_receipt_rejection(tmp_path):
    d=s2('IDENTITY_CORRUPTION');meta=dict(session_id=SESSION,controller_authorized_stop=True,reviewer_receipt=d)
    assert development_classification(meta,SESSION,natural_terminal=False,action_count=1)=='DEVELOPMENT_STOP_RUN_INVALIDATING'
    with pytest.raises(ValueError):development_classification(meta,SESSION,natural_terminal=True,action_count=1)
    auth=dict(plan='Authorized',target_mechanism='Energy',exact_censor_trigger='ENERGY_RECIPE',
        why_score_unimportant='Mechanism only',issue_type='ENERGY_RECIPE',budget=1,authorized_before_run=True,stop_class='MECHANISM_VALIDATION_CENSORED')
    d=new(evaluation_mode='MECHANISM_VALIDATION_CENSOR',censor_authorization=auth);meta['reviewer_receipt']=d
    assert development_classification(meta,SESSION,natural_terminal=False,action_count=40)=='MECHANISM_VALIDATION_CENSORED'


def test_aggregate_rejects_wrong_session_missing_action_and_duplicates():
    d=new();d['action_index']=1
    env=dict(schema_version=3,session_id=SESSION,receipts=[d])
    for mutate in ('envelope_session','receipt_session','missing_action','duplicate'):
        x=copy.deepcopy(env)
        if mutate=='envelope_session':x['session_id']='other'
        if mutate=='receipt_session':x['receipts'][0]['session_id']='other'
        if mutate=='missing_action':x['receipts'][0]['action_index']=100
        if mutate=='duplicate':x['receipts'].append(copy.deepcopy(d))
        with pytest.raises(ValueError):aggregate_reviews(x,SESSION,1)


def test_actual_offline_cli_receipt_argument(tmp_path):
    e,t,sc,r,_=_fixtures(tmp_path);d=new();d['action_index']=1;reviews=envelope(tmp_path,[d]);out=tmp_path/'out.json'
    subprocess.run([sys.executable,'-m','scripts.post_run_audit','--events',str(e),'--transcript',str(t),
        '--runner-result',str(r),'--score-report',str(sc),'--reviewer-receipts',str(reviews),
        '--output',str(out)],cwd=ROOT,check=True,capture_output=True)
    assert json.loads(out.read_text(encoding='utf-8'))['reviewer']['S1_count']==1


def test_frozen_assets_and_historical_reports_are_unchanged():
    paths=['configs','skills','career_sim_runner','pyproject.toml','uv.lock','tests/fixtures/reviewer_gate_cases.json']
    paths += [str(p.relative_to(ROOT)) for p in (ROOT/'docs/project/runs').glob('*')]
    assert not subprocess.check_output(['git','diff','91ca9b6','--',*paths],cwd=ROOT,text=True).strip()
