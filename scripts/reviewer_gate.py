"""Development reviewer receipt validation. No semantic inference from prose.

The reviewer supplies public annotations and the direct violation link. Validation
checks attribution/ownership, not whether those human annotations are true.
"""
from __future__ import annotations

OWNERS = {
    'HEADER_BC': 'manifest/frozen-parser', 'BOARD_FACT': 'structured-state-board',
    'DELIVERY_STATE': 'delivery-progress', 'PLANNING_RANKING': 'rolling-planning',
    'RISK_FINAL_GATE': 'risk-review', 'FRESH_OBSERVE': 'executor/runtime',
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


def validate_receipt(receipt: dict, *, retrospective: bool = False) -> dict:
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
        if kind == 'CONFIRMED_TELEMETRY_CONTRACT_VIOLATION' and obj not in ('HEADER_BC', 'FRESH_OBSERVE'):
            raise ValueError('telemetry stop requires telemetry object')
        if kind == 'CONFIRMED_CANDIDATE_VIOLATION' and obj in ('HEADER_BC', 'FRESH_OBSERVE'):
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
    if receipt['action_index'] > action_count:
        raise ValueError('reviewed action absent from exact run')
    if not checked['stop'] and checked['stop_class'] != 'REVIEWER_DEFECT':
        raise ValueError('NO_VIOLATION cannot authorize development stop')
    return DEVELOPMENT_CLASSES[checked['stop_class']]
