"""Read existing Runner JSONL only; promptly emit bounded reviewer packets/progress.

No Runner, DB, provider or game imports. No NLP verdicts or process control.
Invoke as `python -m scripts.live_review_packet --events EXACT --output-dir LOCAL`.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
import json
from pathlib import Path
import re
import time

from scripts.post_run_audit import _arguments, _node, _public_state, _result
from scripts.basis_preflight_audit import BC, parse_five_marker_header
from scripts.post_run_audit import CTRL, DL
from scripts.policy_trace_audit import POL, PROBE


def official_observation(data: dict) -> dict:
    """Preserve locked1.0.1 Agent fields, applying its serializer exclusions only.

    Read an existing MCP result, never a simulator object. Hidden *stock* is
    filtered in state; HiddenRisk *delta* is retained in choice status_updates.
    This is observation context, not proof of full prior model-context coverage.
    """
    payload = deepcopy({k: data[k] for k in
        ('current_state', 'current_event', 'choices', 'events', 'ending_score') if k in data})
    state = payload.get('current_state', {})
    for key in ('statistics', 'active_nodes', 'completed_nodes', 'monthly_event_queue',
                'monthly_action_count', 'monthly_event_limit', 'initialization_seen',
                'pending_fixed_event', 'quarter_energy_remaining', 'quarter_main_action_done',
                'fixed_event_choice_count', 'failure_rule_remaining_hp'):
        state.pop(key, None)
    if isinstance(state.get('status'), dict):
        state['status'] = {k: v for k, v in state['status'].items() if 'hidden' not in k.lower()}
    event = payload.get('current_event')
    if isinstance(event, dict):
        for key in ('event_id', 'node_id', 'doc_id', 'decision_type', 'event_type'):
            event.pop(key, None)
    for choice in payload.get('choices', []):
        for key in ('next_node', 'consequence_index', 'action_id'):
            choice.pop(key, None)
    return payload


class ReviewStream:
    def __init__(self, heartbeats=(3, 12, 40), session=None):
        if not heartbeats or any(type(n) is not int or n < 1 or n > 40 for n in heartbeats):
            raise ValueError('bounded heartbeat actions must be 1..40')
        self.heartbeats = set(heartbeats)
        self.limit = max(heartbeats)
        self.session = session
        self.calls = {}; self.seen = set(); self.rows = []
        self.latest = None; self.pending = None; self.actions = 0
        self.successes = 0; self.reviews = set(); self.last_level = None
        self.last_review = None

    def feed(self, record: dict) -> list[dict]:
        """Emit in the same feed call as the boundary, before next action is read."""
        kind=record.get('kind'); node=_node(record); output=[]
        call=node.get('tool_call', {})
        cid=call.get('tool_call_id') if kind=='tool_call' else node.get('tool_call_id')
        if not cid or (kind,cid) in self.seen:
            return []
        self.seen.add((kind,cid))
        name=str(call.get('name','')) if kind=='tool_call' else str(node.get('tool_name') or self.calls.get(cid,''))
        if kind=='tool_call':
            self.calls[cid]=name
            if 'take_action' not in name: return []
            args=_arguments(call)
            submitted_session=args.get('session_id') or args.get('game_session_id')
            if submitted_session and self.session and submitted_session!=self.session:
                raise ValueError('cross-session action')
            self.actions+=1; notes=str(args.get('notes',''))
            context=self.latest or {}
            choices=context.get('choices',[])
            selected=next((x for x in choices if x.get('choice')==args.get('choice')),None)
            marker={label:(match[0] if (match:=regex.search(notes)) else 'UNKNOWN')
                    for label,regex in [('CTRL',CTRL),('DL',DL),('POL',POL),('PROBE',PROBE),('BC',BC)]}
            header=parse_five_marker_header(notes)
            self.pending={'session':self.session,'action_index':self.actions,
                'source_seq':record.get('seq'),'submitted_utc':record.get('ts'),
                'public_before':context.get('public','UNKNOWN'),
                'official_before':context.get('official','UNKNOWN'),
                'before_source':context.get('source','UNKNOWN'),
                'event':context.get('event','UNKNOWN'),'choices':choices,
                'selected_candidate':selected or 'UNKNOWN','notes':notes,
                'markers':marker,'header':header,
                'risk_reason':'UNKNOWN_NOT_SEPARATELY_EMITTED',
                'public_reason':notes[header['header_end']:] if header['valid'] else 'UNKNOWN_MALFORMED_HEADER',
                'relevant_review_sticky_facts':{'current_public_feed':context.get('feed',''),
                    'last_public_review':self.last_review,'skill_sticky':'UNKNOWN_NOT_SEPARATELY_EMITTED'},
                'receipt':'PENDING','fresh_observe':False}
            return output
        if kind!='tool_result': return output
        data=_result(node)
        if 'new_game' in name:
            new=data.get('session_id')
            if new:
                if self.session and new!=self.session: raise ValueError('cross-session stream')
                self.session=new
            return output
        if 'take_action' in name and self.pending:
            self.pending['receipt']='SUCCESS' if data.get('success') is True else 'FAILED_OR_UNKNOWN'
            if data.get('success') is True: self.successes+=1
            return output
        if 'observe' not in name or not isinstance(data.get('current_state'),dict): return output
        pub=_public_state(data); new=pub.get('session_id')
        if not new or (self.session and new!=self.session): raise ValueError('missing/cross-session observation')
        self.session=new
        event=data.get('current_event') or {}
        official=official_observation(data)
        self.latest={'public':pub,'event':official.get('current_event'),
            'choices':official.get('choices',[]), 'official':official,
            'source':{'seq':record.get('seq'),'utc':record.get('ts'),'tool':name,
                      'tool_call_id':cid,'scope':'LOCKED_1_0_1_OFFICIAL_OBSERVE_NOT_FULL_MODEL_HISTORY'},
            'feed':data.get('events','')}
        feed=str(self.latest['feed']); month=pub.get('time',{}).get('current_month')
        level=pub.get('status',{}).get('level')
        # Public formal Review appears in this observation, not in a final report.
        if month in (6,12,18,24,30,36,42,48) and month not in self.reviews and ('半年谈话' in feed or event.get('title')=='半年评审'):
            grade=re.search(r'半年绩效奖金[（(]([A-E])[）)]',feed)
            notification={'type':'FORMAL_REVIEW_PROGRESS','session':new,'source_seq':record.get('seq'),
                'observed_utc':record.get('ts'),'month':month,'grade':grade[1] if grade else 'UNKNOWN',
                'level_before':self.last_level,'level_after':level,'public_feedback':feed,
                'report_required_now':True}
            output.append(notification)
            self.last_review=dict(notification)
            self.reviews.add(month)
        self.last_level=level
        if self.pending:
            row=self.pending; self.pending=None
            row.update(fresh_observe=True,observe_seq=record.get('seq'),observed_utc=record.get('ts'),
                       public_after=pub,official_after=official)
            if len(self.rows)<self.limit: self.rows.append(row)
            if self.successes in self.heartbeats and row['receipt']=='SUCCESS':
                output.append({'type':'HEARTBEAT_REVIEW_PACKET','session':new,'boundary_successes':self.successes,
                    'information_boundary_version':2,
                    'emitted_at_source_seq':record.get('seq'),'actions_read_at_emission':self.actions,
                    'semantic_verdict':'PENDING_HUMAN_REVIEW','rows':list(self.rows)})
        return output


def drain(stream, reviewer: ReviewStream, emit):
    """Tail only complete JSONL lines; leave partial writes unread for next poll."""
    while True:
        offset=stream.tell(); line=stream.readline()
        if not line: return
        if not line.endswith('\n'): stream.seek(offset); return
        for packet in reviewer.feed(json.loads(line)): emit(packet)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--events',type=Path,required=True)
    parser.add_argument('--output-dir',type=Path,required=True)
    parser.add_argument('--session')
    parser.add_argument('--heartbeats',default='3,12,40')
    parser.add_argument('--follow',action='store_true')
    parser.add_argument('--poll-seconds',type=float,default=.25)
    args=parser.parse_args()
    if not .05<=args.poll_seconds<=1: parser.error('poll interval must be .05..1 seconds')
    if args.events.resolve().is_relative_to(args.output_dir.resolve()): parser.error('output directory must be separate from raw events')
    reviewer=ReviewStream(tuple(int(n) for n in args.heartbeats.split(',')),args.session)
    args.output_dir.mkdir(parents=True,exist_ok=True)
    def emit(packet):
        name=('heartbeat-'+str(packet['boundary_successes']) if packet['type']=='HEARTBEAT_REVIEW_PACKET' else 'review-'+str(packet['month']))+'.json'
        (args.output_dir/name).write_text(json.dumps(packet,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        # Emit compact notification immediately, never dump a private transcript.
        notice={k:v for k,v in packet.items() if k not in ('rows','public_feedback')}
        print(json.dumps(notice,ensure_ascii=True),flush=True)
    with args.events.open(encoding='utf-8') as stream:
        while True:
            drain(stream,reviewer,emit)
            if not args.follow: return 0
            time.sleep(args.poll_seconds)


if __name__=='__main__': raise SystemExit(main())
