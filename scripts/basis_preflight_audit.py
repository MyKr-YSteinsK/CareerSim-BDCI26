"""Offline kernel contract oracle and receipt measurement, never a live interceptor.

Semantic projections must be explicitly annotated from public evidence. This module
does not classify arbitrary prose, call a model, or prove a PASS receipt truthful.
"""
from __future__ import annotations

from collections import Counter
import re

from scripts.policy_trace_audit import POL, PROBE, parse_header, parse_trace
from scripts.post_run_audit import CTRL, DL

BC = re.compile(r"\[BC=(?:PASS|BLOCKED WHY=(?:PUBLIC|SATURATION|NUMERIC_S|STALE_CLEANUP|SCHEMA|CONTROL))\]")
REASONS = ("PUBLIC", "SATURATION", "NUMERIC_S", "STALE_CLEANUP", "SCHEMA", "CONTROL")


def parse_basis_receipt(text: str) -> dict:
    matches = list(BC.finditer(text))
    if len(matches) != 1 or text.count('[BC=') != 1:
        return dict(status='UNKNOWN', reason=None, valid=False)
    marker = matches[0][0]
    return dict(status='PASS' if marker == '[BC=PASS]' else 'BLOCKED',
                reason=None if marker == '[BC=PASS]' else marker.split('WHY=')[1][:-1], valid=True)


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
    if evidence.get('saturation_claim') is not False and not (
        evidence.get('explicit_public_completion') is True
        and evidence.get('claim_scope') == evidence.get('public_completion_scope')
        and bool(evidence.get('claim_scope'))
    ):
        failures.append('SATURATION')
    header, trace = parse_header(notes), parse_trace(notes)
    if header.get('mode') == 'S' and evidence.get('fresh_material_binding') is not True:
        failures.append('NUMERIC_S')
    if evidence.get('cleanup') is not False and evidence.get('fresh_cleanup_authorization') is not True:
        failures.append('STALE_CLEANUP')
    if not header['valid'] or trace['status'] not in ('VALID', 'AMBIGUOUS'):
        failures.append('SCHEMA')
    markers = [regex.search(notes) for regex in (CTRL, DL, POL, PROBE)]
    if not all(markers) or any(a.end() >= b.start() for a, b in zip(markers, markers[1:]) if a and b):
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
                receipt='[BC=PASS]' if not failures else f'[BC=BLOCKED WHY={failures[0]}]',
                control_state='BLOCKED' if failures else 'READY', may_submit=not failures)


def measure_receipts(action_notes: list[str], decision_receipts: list[str] | None = None) -> dict:
    """Report claims; missing non-submitted receipt coverage stays UNKNOWN.

    decision_receipts must be a scoped, deduplicated projection of executor output,
    never tool echoes or compressed summaries. No inference from historical prose.
    """
    actions = [parse_basis_receipt(n) for n in action_notes]
    blocked = None if decision_receipts is None else Counter(
        p['reason'] for p in map(parse_basis_receipt, decision_receipts) if p['status'] == 'BLOCKED'
    )
    return dict(
        basis_check_present=sum('[BC=' in n for n in action_notes),
        basis_check_valid=sum(p['valid'] for p in actions),
        basis_check_pass=sum(p['status'] == 'PASS' for p in actions),
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
        basis_receipt_coverage_status=('UNKNOWN' if not actions else 'PASS' if all(p['status'] == 'PASS' for p in actions) else 'FAIL'),
        receipt_interpretation='EXPLICIT_CLAIMS_NOT_SEMANTIC_OR_ENFORCEMENT_PROOF',
    )
