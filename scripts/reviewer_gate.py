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
    return {'valid': True, 'stop': confirmed or kind == 'REVIEW_UNCERTAIN_MATERIAL',
            'candidate_failure': kind == 'CONFIRMED_CANDIDATE_VIOLATION',
            'stop_class': kind, 'semantic_truth': 'REVIEWER_ANNOTATED_NOT_MACHINE_PROVEN'}


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
