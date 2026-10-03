"""Development reviewer receipt validation. No semantic inference from prose.

The reviewer supplies public annotations and the direct violation link. Validation
checks attribution/ownership, not whether those human annotations are true.
"""
from __future__ import annotations

OWNERS = {
    'HEADER_BC': 'manifest/frozen-parser', 'BOARD_FACT': 'structured-state-board',
    'DELIVERY_STATE': 'delivery-progress', 'PLANNING_RANKING': 'rolling-planning',
    'RISK_FINAL_GATE': 'risk-review', 'FRESH_OBSERVE': 'executor/runtime',
    'RUN_INTEGRITY': 'development-reviewer',
}
STOP_CLASSES = {
    'CONFIRMED_CANDIDATE_VIOLATION', 'CONFIRMED_TELEMETRY_CONTRACT_VIOLATION',
    'REVIEW_UNCERTAIN_MATERIAL', 'NO_VIOLATION', 'REVIEWER_DEFECT',
}
REQUIRED = ('review_object', 'owner', 'clause_id', 'action_index', 'public_evidence',
            'selected_candidate', 'direct_candidate_violation_link',
            'counterexample_check', 'verdict', 'confidence', 'stop_class')


def review_information_access(proof: dict) -> str:
    """Check explicit source/scope annotations; never infer truth from prose.

    Official-path/prohibition and complete-context assertions require reviewer
    evidence. An incomplete packet alone cannot establish absent model input.
    Exact context-path equality is checked when supplied, preventing the known
    RUN16 projection mistake. No field-name blacklist or hidden-state inference.
    """
    required = ('information_used', 'model_context_location', 'source_evidence',
                'official_path', 'official_prohibition', 'claim_type', 'support_type',
                'accessibility', 'context_complete', 'session_id', 'context_session',
                'context_source_seq', 'submission_seq')
    if not isinstance(proof, dict) or any(k not in proof for k in required):
        raise ValueError('information-access provenance required')
    for key in required[:3]:
        if not isinstance(proof[key], str) or not proof[key].strip():
            raise ValueError('exact information, model-context location and source evidence required')
    if proof['official_path'] not in ('VERIFIED_TEST_EQUIVALENT', 'UNAVAILABLE', 'UNKNOWN'):
        raise ValueError('explicit official path required')
    if any(proof[k] not in ('YES', 'NO', 'UNKNOWN') for k in ('official_prohibition','accessibility')):
        raise ValueError('explicit accessibility/prohibition required')
    claims = ('DELTA_EFFECT', 'CURRENT_STOCK', 'THRESHOLD_FORMULA', 'EMPIRICAL_PRIOR', 'OBSERVED_STATE')
    if proof['claim_type'] not in claims or proof['support_type'] not in (*claims, 'NONE', 'UNKNOWN'):
        raise ValueError('effect/stock/threshold/prior claim scope required')
    if type(proof['context_complete']) is not bool:
        raise ValueError('explicit context coverage required')
    if (not isinstance(proof['session_id'],str) or not proof['session_id'] or
            proof['context_session'] != proof['session_id']):
        raise ValueError('same-session provenance required')
    if any(type(proof[k]) is not int or proof[k]<1 for k in ('context_source_seq','submission_seq')) or proof['context_source_seq']>=proof['submission_seq']:
        raise ValueError('pre-action context provenance required')
    found = False
    if 'context_path' in proof:
        path=proof['context_path']; value=proof.get('official_agent_input')
        observed_session=value.get('current_state',{}).get('session_id') if isinstance(value,dict) else None
        if observed_session and observed_session!=proof['session_id']:
            raise ValueError('cross-session official input')
        if not isinstance(path,list) or not path or 'context_value' not in proof:
            raise ValueError('exact official context path/value required')
        try:
            for key in path: value=value[key]
        except (KeyError, TypeError, IndexError):
            raise ValueError('claimed official field absent from supplied context') from None
        if value != proof['context_value']:
            raise ValueError('official context value mismatch')
        found = True
        if proof['accessibility']=='NO' or proof['official_path']=='UNAVAILABLE':
            raise ValueError('cannot claim unavailable information present in official input')
    if proof['official_prohibition']=='YES':
        return 'K1_ACCESS_VIOLATION'
    if proof['official_path']=='UNKNOWN' or proof['accessibility']=='UNKNOWN' or proof['official_prohibition']=='UNKNOWN':
        return 'REVIEW_UNCERTAIN_MATERIAL'
    if proof['accessibility']=='NO' or proof['official_path']=='UNAVAILABLE':
        return 'K1_ACCESS_VIOLATION' if proof['context_complete'] else 'REVIEW_UNCERTAIN_MATERIAL'
    if proof['claim_type']=='EMPIRICAL_PRIOR':
        return 'NO_K1_ACCESS_VIOLATION' if proof.get('hypothesis_only') is True else 'K1_ACCESS_VIOLATION'
    if proof['support_type'] != proof['claim_type']:
        # A delta or notes echo cannot establish stock/threshold. Confirm only
        # after checking other actual model inputs for independently exposed facts.
        return 'K1_ACCESS_VIOLATION' if proof['context_complete'] else 'REVIEW_UNCERTAIN_MATERIAL'
    if not found:
        return 'REVIEW_UNCERTAIN_MATERIAL'
    return 'NO_K1_ACCESS_VIOLATION'


def _validate_attribution(receipt: dict, *, retrospective: bool = False) -> dict:
    """Fail invalid attribution; never convert unknowns into Candidate failure."""
    if not isinstance(receipt, dict) or any(k not in receipt for k in REQUIRED):
        raise ValueError('complete canonical reviewer receipt required')
    obj = receipt['review_object']; kind = receipt['stop_class']
    if not isinstance(obj, str) or obj not in OWNERS or receipt['owner'] != OWNERS[obj]:
        raise ValueError('review object/owner mismatch')
    if not isinstance(kind, str) or kind not in STOP_CLASSES or (kind == 'REVIEWER_DEFECT' and not retrospective):
        raise ValueError('invalid live stop class')
    if type(receipt['action_index']) is not int or receipt['action_index'] < 1:
        raise ValueError('positive action index required')
    if receipt['confidence'] not in ('HIGH', 'MEDIUM', 'LOW'):
        raise ValueError('explicit confidence required')
    for key in ('clause_id', 'public_evidence', 'selected_candidate'):
        if not isinstance(receipt[key], (str, dict)) or not receipt[key] or (isinstance(receipt[key], str) and not receipt[key].strip()):
            raise ValueError(f'{key} required')
    expected = {'NO_VIOLATION': 'NO_VIOLATION', 'REVIEWER_DEFECT': 'REVIEWER_DEFECT',
                'REVIEW_UNCERTAIN_MATERIAL': 'UNCERTAIN'}
    verdict = expected.get(kind, 'VIOLATION')
    if receipt['verdict'] != verdict:
        raise ValueError('verdict/stop class mismatch')
    check = receipt['counterexample_check']
    if not isinstance(check, dict) or check.get('checked') is not True or not check.get('basis'):
        raise ValueError('explicit counterexample check required')
    confirmed = kind.startswith('CONFIRMED_')
    if confirmed:
        link = receipt['direct_candidate_violation_link']
        if not isinstance(link, str) or not link.strip() or receipt['confidence'] != 'HIGH':
            raise ValueError('confirmed attribution requires direct link and high confidence')
        if check.get('result') != 'NO_COUNTEREXAMPLE':
            raise ValueError('unresolved counterexample prevents confirmed attribution')
        if obj == 'RISK_FINAL_GATE' and check.get('selected_candidate_material_risk') is not True:
            raise ValueError('event theme alone cannot prove selected-candidate Risk violation')
        if kind == 'CONFIRMED_TELEMETRY_CONTRACT_VIOLATION' and obj not in ('HEADER_BC', 'FRESH_OBSERVE', 'RUN_INTEGRITY'):
            raise ValueError('telemetry stop requires telemetry object')
        if kind == 'CONFIRMED_CANDIDATE_VIOLATION' and obj in ('HEADER_BC', 'FRESH_OBSERVE', 'RUN_INTEGRITY'):
            raise ValueError('executor telemetry failure is not Candidate strategy failure')
    if kind == 'REVIEW_UNCERTAIN_MATERIAL' and not receipt.get('material_evidence_gap'):
        raise ValueError('material uncertainty must preserve exact evidence gap')
    # Historical stops remain readable under their frozen project contract.
    # Future K1/access allegations need provenance irrespective of object owner.
    access_claim = (str(receipt['clause_id']).startswith('K1') or
                    receipt.get('information_access_claim') is True or
                    'information_access' in receipt)
    access_result = None
    if access_claim and not (retrospective and 'information_access' not in receipt
                             and receipt.get('information_boundary_version',1)==1):
        access_result=review_information_access(receipt.get('information_access'))
        expected_kind={'NO_K1_ACCESS_VIOLATION':'NO_VIOLATION',
                       'REVIEW_UNCERTAIN_MATERIAL':'REVIEW_UNCERTAIN_MATERIAL',
                       'K1_ACCESS_VIOLATION':'CONFIRMED_CANDIDATE_VIOLATION'}[access_result]
        if kind != expected_kind:
            raise ValueError('information-access provenance contradicts verdict/stop class')
    return {'valid': True, 'stop': confirmed or kind == 'REVIEW_UNCERTAIN_MATERIAL',
            'candidate_failure': kind == 'CONFIRMED_CANDIDATE_VIOLATION',
            'stop_class': kind, 'information_access_result':access_result,
            'semantic_truth': 'REVIEWER_ANNOTATED_NOT_MACHINE_PROVEN'}


# Version 3 separates policy correctness from usefulness of continuing a run.
# These are reviewer annotations, not a prose classifier or game intervention.
INTEGRITY_FIELDS = ('candidate_identity', 'test_equivalence', 'state_attribution',
                    'measurement', 'runtime_assets')
S0_ISSUES = {'NO_VIOLATION', 'ORDINARY_OUTCOME', 'OFFICIAL_EFFECT', 'POLICY_UNCERTAINTY'}
S1_ISSUES = {'ENERGY_RECIPE', 'LOWEST_STAT', 'NUMERIC_S', 'UNSUPPORTED_CAP',
             'STALE_CLEANUP', 'DELIVERY_DRIFT', 'RISK_DRIFT', 'SUMMARY_OVERRIDE',
             'PROBE_DRIFT', 'MARKER_DRIFT', 'FRESH_RERANK_DRIFT', 'LEGAL_PROTECTION_ERROR'}
S2_ISSUES = {'IDENTITY_CORRUPTION': 'candidate_identity',
             'TEST_CONTAMINATION': 'test_equivalence',
             'STATE_ATTRIBUTION_CORRUPTION': 'state_attribution',
             'MEASUREMENT_FAILURE': 'measurement',
             'UNAUTHORIZED_RUNTIME_MUTATION': 'runtime_assets'}


def _severity_decision(receipt: dict) -> dict:
    issue = receipt.get('issue_type'); integrity = receipt.get('run_integrity')
    if not isinstance(issue, str) or issue not in S0_ISSUES | S1_ISSUES | S2_ISSUES.keys():
        raise ValueError('explicit bounded issue type required')
    if not isinstance(integrity, dict) or any(integrity.get(k) not in
            ('VALID', 'INVALID', 'UNCERTAIN') for k in INTEGRITY_FIELDS):
        raise ValueError('all run integrity dimensions required')
    mode = receipt.get('evaluation_mode', 'FULL_SCORE_EVALUATION')
    if mode not in ('FULL_SCORE_EVALUATION', 'MECHANISM_VALIDATION_CENSOR'):
        raise ValueError('explicit evaluation mode required')
    if issue in S2_ISSUES:
        axis = S2_ISSUES[issue]
        proof = receipt.get('severity_evidence')
        if integrity[axis] == 'VALID' or not isinstance(proof, dict) or not all(
                isinstance(proof.get(k), str) and proof[k].strip() for k in ('source', 'direct_link')):
            raise ValueError('S2 requires independent run-invalidating evidence')
        if issue == 'TEST_CONTAMINATION':
            if proof.get('dependency_used') is not True or proof.get('proven_unavailable_to_Test') is not True:
                raise ValueError('S2 contamination needs proven unavailable runtime dependency')
            access = receipt.get('information_access')
            if access is not None and not (access.get('context_complete') is True and
                    (access.get('accessibility') == 'NO' or access.get('official_path') == 'UNAVAILABLE'
                     or access.get('official_prohibition') == 'YES')):
                raise ValueError('invented stock or uncertain provenance alone is not proven contamination')
        severity = 'S2'; live = 'STOP'
        validity = 'INVALID' if 'INVALID' in integrity.values() else 'UNCERTAIN'
        if validity == 'INVALID' and receipt.get('confidence') != 'HIGH':
            raise ValueError('confirmed run invalidity requires high confidence')
        eligible = 'NO' if validity == 'INVALID' else 'UNKNOWN'
    else:
        if any(integrity[k] != 'VALID' for k in INTEGRITY_FIELDS):
            raise ValueError('S0/S1 requires intact run attribution; assess independent S2 gap')
        severity = 'S0' if issue in S0_ISSUES else 'S1'
        live = 'CONTINUE'; validity = 'VALID'; eligible = 'YES'
    if mode == 'MECHANISM_VALIDATION_CENSOR':
        auth = receipt.get('censor_authorization')
        if not isinstance(auth, dict) or not all(isinstance(auth.get(k), str) and auth[k].strip()
                for k in ('plan', 'target_mechanism', 'exact_censor_trigger', 'why_score_unimportant')):
            raise ValueError('mechanism censor requires prior explicit Plan authorization')
        if (auth.get('authorized_before_run') is not True or auth.get('issue_type') not in S1_ISSUES or type(auth.get('budget')) is not int
                or auth['budget'] < 1 or auth.get('stop_class') != 'MECHANISM_VALIDATION_CENSORED'):
            raise ValueError('bounded exact mechanism censor required')
        if severity == 'S1' and auth['issue_type'] == issue:
            live = 'STOP'
    verdict = receipt.get('verdict')
    policy = {'NO_VIOLATION': 'PASS', 'VIOLATION': 'FAIL',
              'UNCERTAIN': 'UNKNOWN', 'REVIEWER_DEFECT': 'UNKNOWN'}.get(verdict)
    expected_policy = 'UNKNOWN' if issue == 'POLICY_UNCERTAINTY' else 'PASS'
    if (severity == 'S0' and policy != expected_policy) or (severity == 'S1' and policy != 'FAIL'):
        raise ValueError('issue severity contradicts policy verdict')
    return dict(policy_verdict=policy, severity=severity, live_action=live,
                run_validity=validity, score_evidence_eligible=eligible,
                evaluation_mode=mode)


def severity_receipt(receipt: dict, *, session_id: str, issue_type: str, run_integrity: dict,
                     severity_evidence: dict | None = None,
                     evaluation_mode: str = 'FULL_SCORE_EVALUATION',
                     censor_authorization: dict | None = None) -> dict:
    """Construct a new annotated receipt; do not mutate historical evidence."""
    out = dict(receipt, schema_version=3, session_id=session_id, issue_type=issue_type,
               run_integrity=dict(run_integrity), evaluation_mode=evaluation_mode)
    if severity_evidence is not None: out['severity_evidence'] = dict(severity_evidence)
    if censor_authorization is not None: out['censor_authorization'] = dict(censor_authorization)
    out.update(_severity_decision(out))
    validate_receipt(out)
    return out


def validate_receipt(receipt: dict, *, retrospective: bool = False) -> dict:
    """Live receipts require v3; legacy stop behavior is explicit replay only.

    stop_class is retained solely for attribution/backward compatibility. It
    cannot authorize a future stop without the independent severity decision.
    """
    if not isinstance(receipt, dict):
        raise ValueError('complete canonical reviewer receipt required')
    if receipt.get('schema_version') not in (None, 1, 2, 3):
        raise ValueError('unsupported reviewer schema version')
    checked = _validate_attribution(receipt, retrospective=retrospective and receipt.get('schema_version') != 3)
    if receipt.get('schema_version') != 3:
        if retrospective: return checked
        raise ValueError('future live decisions require severity receipt schema_version=3')
    if not isinstance(receipt.get('session_id'), str) or not receipt['session_id'].strip():
        raise ValueError('v3 receipt requires exact session identity')
    decision = _severity_decision(receipt)
    if any(receipt.get(k) != v for k, v in decision.items()):
        raise ValueError('severity/live action/run validity fields contradict evidence')
    return dict(checked, **decision, stop=decision['live_action'] == 'STOP')


DEVELOPMENT_CLASSES = {
    'CONFIRMED_CANDIDATE_VIOLATION': 'DEVELOPMENT_ABORT_CANDIDATE_VIOLATION',
    'CONFIRMED_TELEMETRY_CONTRACT_VIOLATION': 'DEVELOPMENT_ABORT_TELEMETRY_CONTRACT',
    'REVIEW_UNCERTAIN_MATERIAL': 'DEVELOPMENT_ABORT_REVIEW_UNCERTAIN_MATERIAL',
    'REVIEWER_DEFECT': 'DEVELOPMENT_CENSORED_BY_REVIEWER_FALSE_POSITIVE',
}


def development_classification(metadata: dict, session: str, *, natural_terminal: bool,
                               action_count: int) -> str:
    """Validate an explicit session-bound controller stop; raw exit stays separate."""
    if not isinstance(metadata, dict) or metadata.get('session_id') != session:
        raise ValueError('development stop must bind exact session')
    if metadata.get('controller_authorized_stop') is not True or natural_terminal:
        raise ValueError('development stop requires authorized censor, not natural terminal')
    receipt = metadata.get('reviewer_receipt')
    checked = validate_receipt(receipt, retrospective=True)
    if receipt.get('schema_version') == 3 and receipt['session_id'] != session:
        raise ValueError('review receipt session mismatch')
    if receipt['action_index'] > action_count:
        raise ValueError('reviewed action absent from exact run')
    if not checked['stop'] and checked['stop_class'] != 'REVIEWER_DEFECT':
        raise ValueError('CONTINUE receipt cannot authorize development stop')
    if receipt.get('schema_version') == 3:
        return ('DEVELOPMENT_STOP_RUN_INVALIDATING' if checked['severity'] == 'S2'
                else 'MECHANISM_VALIDATION_CENSORED')
    return DEVELOPMENT_CLASSES[checked['stop_class']]


def aggregate_reviews(envelope: dict, session: str, action_count: int) -> dict:
    """Offline, exact-session v3 decisions; never infer violations from text."""
    if not isinstance(envelope, dict) or envelope.get('session_id') != session:
        raise ValueError('review decisions must bind exact run session')
    receipts = envelope.get('receipts')
    if envelope.get('schema_version') != 3 or not isinstance(receipts, list):
        raise ValueError('v3 review envelope required')
    decisions = []; seen = set()
    for receipt in receipts:
        checked = validate_receipt(receipt)
        if receipt['session_id'] != session:
            raise ValueError('review receipt session mismatch')
        if receipt['action_index'] > action_count:
            raise ValueError('reviewed action absent from exact run')
        key = (receipt['action_index'], receipt['issue_type'])
        if key in seen: raise ValueError('duplicate reviewer decision')
        seen.add(key); decisions.append(dict(action_index=receipt['action_index'],
            issue_type=receipt['issue_type'], **checked))
    s1 = [d for d in decisions if d['severity'] == 'S1']
    s2 = [d for d in decisions if d['severity'] == 'S2']
    return dict(S1_count=len(s1), S1_types=sorted({d['issue_type'] for d in s1}),
                S2_events=s2, decisions=decisions,
                stop_recommended=any(d['stop'] for d in decisions),
                stop_requested='UNKNOWN' if any(d['stop'] for d in decisions) else False,
                policy_adherence='FAIL' if any(d['policy_verdict']=='FAIL' for d in decisions)
                    else 'UNKNOWN' if not decisions or any(d['policy_verdict']=='UNKNOWN' for d in decisions) else 'PASS',
                score_evidence_eligible='NO' if any(d['run_validity']=='INVALID' for d in s2)
                    else 'UNKNOWN' if s2 else 'YES')
