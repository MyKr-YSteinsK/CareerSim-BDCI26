"""Evaluator-only official Dev engine adapter; policy sees JSON public projection.

No Jiuwen/provider/network/shared DB. Opaque in-memory persistence replaces I/O,
not game mechanics. Do not import this module into policy.py.
"""
import asyncio
import copy
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import random
import socket
import subprocess
import sys
import time
from unittest.mock import patch
from uuid import UUID

ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT / '.venv/Lib/site-packages/career_emulator_bdci26/dev/dataset'
POLICY = Path(__file__).with_name('policy.py')
STATUS = {'health', 'dignity', 'skill', 'network', 'output', 'wealth', 'energy', 'level', 'duration_in_level'}


class MemoryStore:
    def __init__(self, *args, **kwargs): self.sessions = {}
    async def save_session(self, session): self.sessions[session.session_id] = copy.deepcopy(session)
    async def load_session(self, sid): return copy.deepcopy(self.sessions.get(sid))
    async def append_log(self, entry): pass
    def delete_session_callback(self): return lambda sid, obj: self.sessions.pop(sid, None)


def projection(raw):
    # raw must already be official MCP serialization. Stronger fail-closed allowlist.
    state = raw['current_state']; event = raw.get('current_event') or {}
    if type(state['time']['current_month']) is not int:
        raise ValueError('non-public month type')
    scalar = lambda v: isinstance(v, (str, int, float, bool, type(None)))
    return {'month': state['time']['current_month'],
        'status': {k: v for k, v in state['status'].items() if k in STATUS and scalar(v)},
        'event': {k: v for k, v in event.items() if k in {'title', 'description', 'rules', 'remaining_energy', 'energy_budget', 'max_selections'} and scalar(v)},
        'choices': [{k: v for k, v in c.items() if k in {'choice', 'action', 'description', 'energy_cost'} and scalar(v)} for c in raw['choices']],
        'feedback': raw.get('events', '')}


class PolicyProcess:
    def __init__(self):
        env = {k: v for k, v in os.environ.items() if k in ('SYSTEMROOT', 'WINDIR', 'TEMP', 'TMP')}
        env.update(PYTHONIOENCODING='utf-8', PYTHONHASHSEED='0')
        self.p = subprocess.Popen([sys.executable, '-I', str(POLICY)], stdin=subprocess.PIPE,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8', env=env)
    def call(self, request):
        # -I ignores PYTHONIOENCODING on Windows. ASCII-escaped wire data is
        # invariant under the child's locale and preserves Chinese semantics.
        self.p.stdin.write(json.dumps(request, ensure_ascii=True) + '\n'); self.p.stdin.flush()
        line = self.p.stdout.readline()
        if not line: raise RuntimeError('policy process ended')
        result = json.loads(line)
        if 'error' in result: raise RuntimeError(result['error'])
        return result
    def close(self):
        self.p.stdin.close(); self.p.wait(timeout=10)
        self.p.stdout.close(); self.p.stderr.close()


def make_engine():
    from career_emulator import game
    paths = {k + '_dir': DATA / v for k, v in {
        'event': 'action_pool', 'fixed_event': 'initialization_n_regular',
        'failure_conditions': 'failure_conditions', 'salary_conditions': 'salary_conditions',
        'promotion': 'promotion', 'talk_mechanism': 'talk_mechanism', 'ending_score': 'ending_score'}.items()}
    with patch.object(game, 'SessionStore', MemoryStore): engine = game.GameEngine(**paths)
    return engine


async def episode(engine, process, seed, config, trace=False):
    from career_emulator import game
    started = time.perf_counter()
    sid = hashlib.sha256(f'S10-22:{seed}'.encode()).hexdigest()[:32]
    random.seed(seed)
    engine.store.sessions.clear()
    process.call({'reset': config})
    actions = []; reviews = []; promotions = []; last_level = None
    with patch.object(game, 'uuid4', lambda: UUID(hex=sid)):
        created = await engine.new_game()
    if created.error: raise RuntimeError(created.error)
    for step in range(1000):
        raw = (await engine.observe(created.session_id)).to_mcp_dict()
        public = projection(raw)
        level = public['status']['level']
        if last_level and level != last_level: promotions.append(public['month'])
        if public['feedback'] and any(w in public['feedback'] for w in ('绩效', '评级', '晋升', '升职')):
            reviews.append({'month': public['month'], 'status': public['status'], 'feedback': public['feedback']})
        last_level = level
        if not public['choices']:
            flags = raw['current_state'].get('simulation_flags', {})
            return {'seed': seed, 'score': raw.get('ending_score'), 'month': min(public['month'], 48),
                'complete': public['month'] == 49, 'terminal_reason': flags.get('failure_reason'),
                'status': public['status'], 'promotions': promotions, 'reviews': reviews,
                'action_count': len(actions), 'actions': actions if trace else None,
                'seconds': time.perf_counter() - started}
        selected = process.call({'observation': public})
        choice = next(c for c in public['choices'] if c['choice'] == selected['choice'])
        result = (await engine.take_action(created.session_id, selected['choice'], 'S10-22 public-only deterministic research')).to_dict()
        if not result['success']: raise RuntimeError(result['error'])
        actions.append({'month': public['month'], 'kind': selected['kind'], 'family': selected['family'],
            'choice': choice, 'public': public if trace else None})
    raise RuntimeError('bounded episode exceeded 1000 steps')


def identity():
    files = sorted(p for p in DATA.rglob('*') if p.is_file())
    entries = [(p.relative_to(DATA).as_posix(), hashlib.sha256(p.read_bytes()).hexdigest()) for p in files]
    package = ROOT / '.venv/Lib/site-packages/career_emulator'
    code = [(p.relative_to(package).as_posix(), hashlib.sha256(p.read_bytes()).hexdigest()) for p in sorted(package.rglob('*.py'))]
    return {'packages': {k: importlib.metadata.version(k) for k in ('career-emulator', 'career-emulator-bdci26')},
        'dataset': str(DATA), 'dataset_files': len(entries), 'dataset_sha256': hashlib.sha256(json.dumps(entries).encode()).hexdigest(),
        'engine_code_sha256': hashlib.sha256(json.dumps(code).encode()).hexdigest(),
        'rng': 'SHA256(S10-22:seed) UUID; global random.seed(seed); PYTHONHASHSEED=0',
        'python': sys.version, 'network': 'socket.connect and connect_ex denied', 'storage': 'opaque deepcopy memory; no DB/log persistence'}


def no_network(*args, **kwargs): raise RuntimeError('network forbidden in offline research')


def disable_network():
    # Windows asyncio creates a local socketpair during loop construction;
    # install the deny gate after construction, before engine/provider imports.
    socket.socket.connect = no_network
    socket.socket.connect_ex = no_network
