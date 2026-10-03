"""Future P3 supervisor for an already-authorized Runner process.

No Candidate/game choice, service start, provider probe or DB API. Importing this
module does nothing. A future live Plan must authorize the Runner and this
supervisor; offline tests use a fake process and immutable event replay.
"""
from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
import json
from pathlib import Path
import time

from scripts.live_review_packet import ReviewStream
from scripts.post_run_audit import _node, _result
from scripts.reviewer_gate import INTEGRITY_FIELDS, S1_ISSUES, severity_receipt, validate_receipt


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def write_json(path, value):
    path = Path(path)
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    temporary.replace(path)


class LiveRunController:
    """Owns reviewer stop authority, not Agent decisions or live authorization.

    Call after fresh session establishment, with the exact process handle and
    a new run-local output directory. Drain available events before decisions.
    Terminal facts come only from existing output; no extra gameplay queries.
    """
    def __init__(self, runner, output_dir: Path, session_id: str, *,
                 evaluation_mode='FULL_SCORE_EVALUATION', censor_authorization=None,
                 run_budget=1, emit=None, clock=utc_now):
        if not isinstance(session_id, str) or not session_id.strip():
            raise ValueError('exact fresh session required')
        self.mode = evaluation_mode
        if type(run_budget) is not int or run_budget < 1:
            raise ValueError('explicit positive authorized run budget required')
        self.censor = deepcopy(censor_authorization)
        if self.mode not in ('FULL_SCORE_EVALUATION', 'MECHANISM_VALIDATION_CENSOR'):
            raise ValueError('unknown evaluation mode')
        if self.mode == 'MECHANISM_VALIDATION_CENSOR':
            auth = self.censor
            if (not isinstance(auth, dict) or auth.get('authorized_before_run') is not True
                    or type(auth.get('budget')) is not int or auth['budget'] != run_budget
                    or auth.get('issue_type') not in S1_ISSUES
                    or auth.get('stop_class') != 'MECHANISM_VALIDATION_CENSORED'
                    or not all(isinstance(auth.get(k), str) and auth[k].strip() for k in
                        ('plan','target_mechanism','issue_type','exact_censor_trigger','why_score_unimportant'))):
                raise ValueError('mechanism mode must be authorized before supervisor starts')
        elif self.censor is not None:
            raise ValueError('full-score supervisor cannot carry censor authorization')
        self.runner = runner
        self.output = Path(output_dir)
        if (self.output/'controller-state.json').exists() or (self.output/'development-stop.json').exists():
            raise ValueError('fresh controller output required; no resume/replacement')
        self.output.mkdir(parents=True, exist_ok=True)
        self.session = session_id
        self.monitor = ReviewStream(session=session_id)
        self.clock = clock
        self.emit = emit or (lambda tag, **data: print(tag+' '+json.dumps(data, ensure_ascii=True), flush=True))
        self.receipts = []; self.seen_decisions = set(); self.rejected = []
        self.natural = None; self.technical = None; self.stop_metadata = None
        self.timeline = []; self.telemetry_warnings = []; self.event_seen = set()
        self.integrity_pending = []
        self.save()

    def save(self):
        write_json(self.output/'reviewer-receipts.json', dict(schema_version=3,
            session_id=self.session, receipts=self.receipts))
        write_json(self.output/'controller-state.json', dict(schema_version=1,
            session_id=self.session, evaluation_mode=self.mode,
            natural_terminal=self.natural, technical_failure=self.technical,
            stop_request_emitted=self.stop_metadata is not None,
            actual_actions_read=self.monitor.actions, rejected=self.rejected,
            telemetry_warnings=self.telemetry_warnings, decisions=self.timeline))

    def feed_events(self, records):
        """Formal/promotion notifications precede semantic decision processing."""
        for record in records:
            node = _node(record); kind = record.get('kind')
            cid = (node.get('tool_call',{}).get('tool_call_id') if kind=='tool_call'
                   else node.get('tool_call_id'))
            key = (kind, cid)
            if cid and key in self.event_seen: continue
            if cid: self.event_seen.add(key)
            previous_level = self.monitor.last_level
            # This public follower never stops on an attributable malformed
            # header or stale semantic choice. It preserves those rows for v3 review.
            try:
                packets = self.monitor.feed(record)
            except ValueError as exc:
                # An exact conflicting session is an objective attribution fault,
                # not a strategy/marker error. Preserve source then request v3 S2.
                if 'session' not in str(exc): raise
                if self.monitor.actions == 0:
                    self.technical_failure(dict(category='RUNTIME',source=f"events seq{record.get('seq')}: {exc}"))
                    return
                self._session_corruption(record, str(exc))
                continue
            for packet in packets:
                packet['packet_emitted_utc'] = self.clock()
                if packet['type']=='FORMAL_REVIEW_PROGRESS':
                    write_json(self.output/f"review-{packet['month']}.json", packet)
                    self.emit('FORMAL_REVIEW_PROGRESS', **packet)
                else:
                    write_json(self.output/f"heartbeat-{packet['boundary_successes']}.json", packet)
                    self.emit('HEARTBEAT_REVIEW_READY', action=packet['boundary_successes'])
            if kind=='tool_result' and 'observe' in str(node.get('tool_name','')):
                data = _result(node)
                flags = data.get('current_state',{}).get('simulation_flags',{})
                score = data.get('ending_score')
                ended = (data.get('game',{}).get('ended') is True or bool(score)
                    or flags.get('alive') is False or flags.get('failed') is True)
                if ended and self.natural is None:
                    self.natural = dict(source_seq=record.get('seq'), observed_utc=record.get('ts'),
                        controller_seen_utc=self.clock(), source='exact same-session structured observe')
                    self.emit('NATURAL_TERMINAL', **self.natural)
                if previous_level and self.monitor.last_level != previous_level:
                    self.emit('PROMOTION', before=previous_level, after=self.monitor.last_level)
            self.save()

    def _session_corruption(self, record, error):
        integrity = {k:'VALID' for k in INTEGRITY_FIELDS}
        integrity['state_attribution'] = 'INVALID'
        raw = dict(review_object='RUN_INTEGRITY',owner='development-reviewer',
            clause_id='Integrity/CrossSession',action_index=self.monitor.actions,
            public_evidence=dict(expected_session=self.session,source_seq=record.get('seq'),error=error),
            selected_candidate='Recorded current-run action',
            direct_candidate_violation_link='Exact event carries missing/conflicting session; current run attribution fails',
            counterexample_check=dict(checked=True,result='NO_COUNTEREXAMPLE',
                basis='Frozen ReviewStream session checks on existing structured events; no marker/prose inference'),
            verdict='VIOLATION',confidence='HIGH',stop_class='CONFIRMED_TELEMETRY_CONTRACT_VIOLATION')
        kwargs = dict(evaluation_mode=self.mode)
        if self.censor is not None: kwargs['censor_authorization']=self.censor
        receipt = severity_receipt(raw,session_id=self.session,issue_type='STATE_ATTRIBUTION_CORRUPTION',
            run_integrity=integrity,severity_evidence=dict(source=f"exact events seq{record.get('seq')}",
                direct_link=error),**kwargs)
        self.integrity_pending.append((receipt,f"events#{record.get('seq')}"))

    def technical_failure(self, evidence):
        """Normal unrecoverable technical path; raw exit alone is not proof."""
        if not isinstance(evidence, dict) or evidence.get('category') not in ('PROVIDER','RUNTIME') or not evidence.get('source'):
            raise ValueError('explicit scoped unrecoverable technical evidence required')
        if self.natural is not None:
            self.emit('TECHNICAL_AFTER_NATURAL', **evidence)
            return
        self.technical = dict(evidence, seen_utc=self.clock())
        self.save()
        if self.runner.poll() is None:
            self.runner.terminate()
        self.emit('TECHNICAL_TERMINAL', **self.technical)

    def consume_receipt(self, receipt, *, receipt_id):
        """Rejected/legacy/tampered receipts cannot terminate the process."""
        try:
            checked = validate_receipt(receipt)
            if receipt['session_id'] != self.session or receipt['action_index'] > self.monitor.actions:
                raise ValueError('receipt must bind same session and a recorded action')
            if checked['evaluation_mode'] != self.mode:
                raise ValueError('receipt cannot select controller evaluation mode')
            if self.mode == 'MECHANISM_VALIDATION_CENSOR':
                if receipt.get('censor_authorization') != self.censor:
                    raise ValueError('receipt censor authorization differs from pre-run Plan')
                if checked['severity']=='S1' and checked['live_action']=='STOP' and receipt.get('censor_trigger') != self.censor['exact_censor_trigger']:
                    raise ValueError('exact preauthorized censor trigger not established')
            key = (receipt['action_index'], receipt['issue_type'])
            if key in self.seen_decisions:
                raise ValueError('duplicate decision')
        except (ValueError, KeyError, TypeError) as exc:
            entry = dict(receipt_id=str(receipt_id), time=self.clock(), reason=str(exc),
                         stop_request_emitted=False)
            self.rejected.append(entry); self.save()
            self.emit('RECEIPT_REJECTED_NO_STOP', **entry)
            return dict(accepted=False, stop_request_emitted=False)
        self.seen_decisions.add(key)
        self.receipts.append(deepcopy(receipt))
        entry = dict(receipt_id=str(receipt_id), warning_time=self.clock(),
            action_index=receipt['action_index'], issue_type=receipt['issue_type'],
            policy_verdict=checked['policy_verdict'], severity=checked['severity'],
            live_action=checked['live_action'], score_evidence_eligible=checked['score_evidence_eligible'],
            actual_action_at_decision=self.monitor.actions, run_continues=True,
            stop_request_emitted=False)
        self.timeline.append(entry); self.save()
        # Terminal precedence: natural > explicit technical > v3 S2 > exact
        # preauthorized censor > S1 warning > S0. No legacy stop_class branch.
        if self.natural is not None:
            entry.update(suppressed_by='NATURAL_TERMINAL', run_continues=False)
        elif self.technical is not None:
            entry.update(suppressed_by='TECHNICAL_UNRECOVERABLE', run_continues=False)
        elif self.stop_metadata is not None or self.runner.poll() is not None:
            entry.update(suppressed_by='RUNNER_ALREADY_STOPPED', run_continues=False)
        elif checked['live_action']=='STOP':
            self._emit_reviewer_stop(receipt, checked, receipt_id, entry)
        elif checked['severity']=='S1':
            self.emit('POLICY_WARNING_CONTINUE', **entry)
        else:
            self.emit('REVIEW_CONTINUE', **entry)
        self.save()
        return dict(entry, accepted=True)

    def _emit_reviewer_stop(self, receipt, checked, receipt_id, entry):
        """The only reviewer-derived stop-emission seam, after v3 validation."""
        checked = validate_receipt(receipt)
        if (receipt['session_id'] != self.session or receipt['action_index'] > self.monitor.actions
                or checked['evaluation_mode'] != self.mode or self.natural is not None
                or self.technical is not None or self.stop_metadata is not None
                or self.runner.poll() is not None):
            raise ValueError('stop seam requires active same-session validated authority')
        is_s2 = checked['severity']=='S2' and checked['live_action']=='STOP'
        censor = (self.mode=='MECHANISM_VALIDATION_CENSOR' and checked['severity']=='S1'
                  and checked['live_action']=='STOP' and receipt.get('censor_authorization')==self.censor
                  and receipt.get('censor_trigger')==self.censor['exact_censor_trigger'])
        if not (is_s2 or censor):
            raise ValueError('no v3 reviewer stop authority')
        request = self.clock()
        # Validated receipt/envelope is durable before the process-control call.
        self.runner.terminate()
        self.stop_metadata = dict(session_id=self.session, controller_authorized_stop=True,
            reviewer_receipt=deepcopy(receipt), receipt_id=str(receipt_id),
            stop_request_utc=request, actual_actions_read=self.monitor.actions,
            stop_authority='VALIDATED_S2' if is_s2 else 'AUTHORIZED_MECHANISM_CENSOR')
        write_json(self.output/'development-stop.json', self.stop_metadata)
        entry.update(stop_request_emitted=True, run_continues=False, stop_request_utc=request)
        self.emit('REVIEWER_CONTROLLED_STOP', **entry)

    def process_available(self, records, decision_files=(), *, technical_evidence=None):
        self.feed_events(records)
        if technical_evidence is not None: self.technical_failure(technical_evidence)
        pending = list(self.integrity_pending)
        self.integrity_pending.clear()
        for path in decision_files:
            try:
                decision = json.loads(Path(path).read_text(encoding='utf-8'))
                if not isinstance(decision.get('receipts'), list) or not decision['receipts']:
                    raise ValueError('nonempty receipts required')
            except (OSError, ValueError, TypeError) as exc:
                self.rejected.append(dict(receipt_id=str(path),time=self.clock(),reason=str(exc),stop_request_emitted=False))
                self.save(); continue
            for index, receipt in enumerate(decision['receipts']):
                pending.append((receipt,f'{path}#{index}'))
        def priority(item):
            try:
                checked=validate_receipt(item[0])
                return (0 if checked['severity']=='S2' else 1 if checked['live_action']=='STOP'
                        else 2 if checked['severity']=='S1' else 3)
            except (ValueError, KeyError, TypeError): return 4
        for receipt, receipt_id in sorted(pending,key=priority):
            self.consume_receipt(receipt,receipt_id=receipt_id)


def supervise_runner(runner, *, events: Path, output_dir: Path, session_id: str,
                     decision_dir: Path, evaluation_mode='FULL_SCORE_EVALUATION',
                     censor_authorization=None, run_budget=1, emit=None, poll_seconds=.25):
    """Canonical future launcher seam: pass its Popen handle after fresh game.

    Caller owns authorized service lifecycle/P1 gates/one Popen play/cleanup.
    Exact events/session must be established from that play, never a latest search.
    No import-time start and no exception->reviewer-stop fallback.
    """
    if not .05 <= poll_seconds <= 1: raise ValueError('bounded polling interval required')
    controller = LiveRunController(runner,output_dir,session_id,
        evaluation_mode=evaluation_mode,censor_authorization=censor_authorization,
        run_budget=run_budget,emit=emit)
    processed = set()
    with Path(events).open(encoding='utf-8') as stream:
        while True:
            records = []
            while True:
                pos = stream.tell(); line = stream.readline()
                if not line or not line.endswith('\n'):
                    stream.seek(pos); break
                records.append(json.loads(line))
            # Drain events/terminal/formal Review before consuming delayed decisions.
            paths = sorted(p for p in Path(decision_dir).glob('*-decision.json') if p not in processed)
            controller.process_available(records,paths)
            processed.update(paths)
            if runner.poll() is not None:
                # Result preserves raw exit without inventing Provider causality.
                controller.emit('RUNNER_TERMINAL',exit=runner.poll())
                return controller
            time.sleep(poll_seconds)
