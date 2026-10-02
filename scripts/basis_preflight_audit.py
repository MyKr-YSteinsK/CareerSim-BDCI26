"""Offline kernel contract oracle and receipt measurement, never a live interceptor.

Semantic projections must be explicitly annotated from public evidence. This module
does not classify arbitrary prose, call a model, or prove a PASS receipt truthful.
"""
from __future__ import annotations

from collections import Counter
import re

from scripts.policy_trace_audit import POL, PROBE, parse_header, parse_trace
from scripts.post_run_audit import CTRL, DL

S_CLASSES = ('NONE', 'ACUTE', 'TRUST', 'JOB', 'AFFORDABILITY', 'OTHER_PUBLIC_BINDING')
PASS_CERTIFICATE = r'\[BC=PASS S=(?P<s_basis>' + '|'.join(S_CLASSES) + r') CAP=(?P<cap_basis>NONE|PUBLIC_SCOPED)\]'
BC = re.compile(PASS_CERTIFICATE + r'|\[BC=BLOCKED WHY=(?P<why>PUBLIC|SATURATION|NUMERIC_S|STALE_CLEANUP|SCHEMA|CONTROL)\]')
REASONS = ("PUBLIC", "SATURATION", "NUMERIC_S", "STALE_CLEANUP", "SCHEMA", "CONTROL")
HEADER_SCHEMA_VERSION = 3
FIVE_MARKER = re.compile(CTRL.pattern + ' ' + DL.pattern + ' ' + POL.pattern + ' ' + PROBE.pattern + ' ' + PASS_CERTIFICATE)


def parse_five_marker_header(notes: str) -> dict:
    """Submitted v10e notes only; non-submitted BLOCKED receipts are separate.

    Compose frozen parsers at character zero, with one ASCII space per marker
    boundary. Never trim prefixes or rewrite historical notes to obtain a PASS.
    """
    match = FIVE_MARKER.match(notes)
    once = all(notes.count(prefix) == 1 for prefix in ('[CTRL', '[DL', '[POL', '[PROBE', '[BC'))
    if not match or not once:
        return dict(valid=False, reason='SCHEMA', header_end=None)
    c, d = CTRL.match(notes), DL.search(notes)
    tail = notes[match.end():]
    suffix_valid = not tail or tail.startswith((' ', '\n', '\r\n'))
    current_enums = c['rb'] is not None and d['item_id'] is not None and d['checkpoint'] in ('NEAR', 'NOT_NEAR', 'UNKNOWN')
    valid = bool(suffix_valid and current_enums and parse_header(notes)['valid']
                 and parse_trace(notes)['status'] in ('VALID', 'AMBIGUOUS'))
    return dict(valid=valid, reason=None if valid else 'SCHEMA', header_end=match.end() if valid else None)


def parse_basis_receipt(text: str) -> dict:
    matches = list(BC.finditer(text))
    if len(matches) != 1 or text.count('[BC=') != 1:
        return dict(status='UNKNOWN', reason=None, valid=False)
    marker = matches[0][0]
    match = matches[0]
    return dict(status='BLOCKED' if match['why'] else 'PASS', reason=match['why'], valid=True,
                S_basis=match['s_basis'], CAP_basis=match['cap_basis'], marker=marker)


def check_basis(notes: str, evidence: dict) -> dict:
    """Evaluate explicit sanitized annotations, not their semantic truth.

    Summary content deliberately has no authority; no epoch parameter exists.
    Unknown safety basis fails closed. Explicit cap/completion supports only the
    claimed scope, never a broader family. BC is output and never input to ranking.
    """
    failures = []
    if evidence.get('public_basis') is False or evidence.get('restricted_basis') is True:
        failures.append('PUBLIC')
    elif evidence.get('public_basis') is not True or evidence.get('restricted_basis') is not False:
        failures.append('CONTROL')
    certificate = parse_basis_receipt(notes)
    cap_claim = evidence.get('saturation_claim')
    cap_consistent = (
        cap_claim is True and certificate.get('CAP_basis') == 'PUBLIC_SCOPED'
        and evidence.get('explicit_public_completion') is True
        and evidence.get('claim_scope') == evidence.get('public_completion_scope')
        and bool(evidence.get('claim_scope'))
    ) or (cap_claim is False and certificate.get('CAP_basis') == 'NONE')
    # Missing/malformed certificate is SCHEMA, but cannot hide a semantic failure.
    if (certificate['valid'] and not cap_consistent) or (cap_claim is not False and not (
        evidence.get('explicit_public_completion') is True
        and evidence.get('claim_scope') == evidence.get('public_completion_scope')
        and bool(evidence.get('claim_scope'))
    )):
        failures.append('SATURATION')
    header = parse_header(notes)
    s_basis = certificate.get('S_basis')
    binding_consistent = (s_basis == 'NONE') or (
        s_basis in S_CLASSES[1:] and evidence.get('fresh_material_binding') is True
        and evidence.get('public_binding_class') == s_basis
    )
    numeric_only = evidence.get('fresh_material_binding') is False and evidence.get('only_numeric_basis') is True
    mode_s_consistent = header.get('mode') != 'S' or (
        s_basis in S_CLASSES[1:] and evidence.get('fresh_material_binding') is True
    )
    if numeric_only or (certificate['valid'] and not binding_consistent) or not mode_s_consistent:
        failures.append('NUMERIC_S')
    if evidence.get('cleanup') is not False and evidence.get('fresh_cleanup_authorization') is not True:
        failures.append('STALE_CLEANUP')
    if not parse_five_marker_header(notes)['valid']:
        failures.append('SCHEMA')
    c = re.match(r'^\[CTRL .*? R=(\w+) RB=(\w+)\]', notes)
    if not c or c[1] == 'RECONSIDER' or c[2] not in ('NONE', 'DONE'):
        failures.append('CONTROL')
    if any(evidence.get(key) is not True for key in (
        'same_session', 'fresh_observe', 'rebuilt_passes', 'legal_integer_choice', 'current_candidate'
    )):
        failures.append('CONTROL')
    failures = list(dict.fromkeys(failures))
    status = 'BLOCKED' if failures else 'PASS'
    return dict(status=status, reasons=failures,
                receipt=certificate['marker'] if not failures else f'[BC=BLOCKED WHY={failures[0]}]',
                S_basis=s_basis, CAP_basis=certificate.get('CAP_basis'),
                MODE_S_consistent=mode_s_consistent, binding_consistent=binding_consistent,
                cap_claim_consistent=cap_consistent,
                control_state='BLOCKED' if failures else 'READY', may_submit=not failures)


def measure_receipts(action_notes: list[str], decision_receipts: list[str] | None = None) -> dict:
    """Report claims; missing non-submitted receipt coverage stays UNKNOWN.

    decision_receipts must be a scoped, deduplicated projection of executor output,
    never tool echoes or compressed summaries. No inference from historical prose.
    """
    actions = [parse_basis_receipt(n) for n in action_notes]
    layouts = [parse_five_marker_header(n)['valid'] for n in action_notes]
    blocked = None if decision_receipts is None else Counter(
        p['reason'] for p in map(parse_basis_receipt, decision_receipts) if p['status'] == 'BLOCKED'
    )
    return dict(
        basis_check_present=sum('[BC=' in n for n in action_notes),
        basis_check_valid=sum(p['valid'] for p in actions),
        basis_check_pass=sum(p['status'] == 'PASS' for p in actions),
        submitted_BC_certificate_coverage=sum(p['status'] == 'PASS' and valid for p, valid in zip(actions, layouts)),
        S_basis=dict(Counter(p.get('S_basis') for p in actions if p['status'] == 'PASS')),
        CAP_basis=dict(Counter(p.get('CAP_basis') for p in actions if p['status'] == 'PASS')),
        MODE_S_inconsistent_claims=sum(parse_header(n).get('mode') == 'S' and p.get('S_basis') == 'NONE'
                                       for n, p in zip(action_notes, actions)),
        semantic_consistency='UNKNOWN_WITHOUT_EXPLICIT_PUBLIC_ANNOTATIONS',
        restricted_basis_blocked=None if blocked is None else blocked['PUBLIC'],
        saturation_basis_blocked=None if blocked is None else blocked['SATURATION'],
        numeric_S_blocked=None if blocked is None else blocked['NUMERIC_S'],
        stale_cleanup_blocked=None if blocked is None else blocked['STALE_CLEANUP'],
        action_submitted_despite_BLOCKED=sum(p['status'] == 'BLOCKED' for p in actions),
        CTRL_coverage=sum(bool(CTRL.match(n)) and n.count('[CTRL') == 1 for n in action_notes),
        DL_coverage=sum(parse_header(n)['valid'] for n in action_notes),
        POL_coverage=sum(bool(POL.search(n)) and n.count('[POL') == 1 for n in action_notes),
        PROBE_coverage=sum(bool(PROBE.search(n)) and n.count('[PROBE') == 1 for n in action_notes),
        POL_PROBE_coverage=sum(parse_trace(n)['status'] in ('VALID', 'AMBIGUOUS') for n in action_notes),
        full_five_marker_coverage=sum(layouts),
        submitted_BC_PASS_with_invalid_header=sum(p['status'] == 'PASS' and not valid for p, valid in zip(actions, layouts)),
        header_schema_version=HEADER_SCHEMA_VERSION,
        basis_receipt_coverage_status=('UNKNOWN' if not actions else 'PASS' if all(p['status'] == 'PASS' and valid for p, valid in zip(actions, layouts)) else 'FAIL'),
        receipt_interpretation='EXPLICIT_CLAIMS_NOT_SEMANTIC_OR_ENFORCEMENT_PROOF',
    )
