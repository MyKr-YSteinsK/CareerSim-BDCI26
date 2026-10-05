"""Sequential paired-seed search, fixed Story and pre-frozen independent holdout."""
import argparse
import asyncio
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import statistics
import time

from harness import ROOT, PolicyProcess, make_engine, episode, identity, disable_network

OUT = ROOT / '.local/runtime/s10-22-policy-search'
BASE = dict(health='trend', flat=1, repair='explicit', main='conditional',
            momentum='preserve', reset='broad', lane='responsive', skill='disabled')
POLICIES = {
    'B0_balanced': dict(BASE, momentum='balanced', repair='once'),
    'B1_v6_like': dict(BASE, main='aggressive', reset='result', flat=2, repair='once'),
    'B2_v6d_like': dict(BASE),
    'B3_survival': dict(BASE, health='buffer', main='risk'),
    'P4_momentum': dict(BASE, reset='stay', main='aggressive', repair='current'),
    'P5_network': dict(BASE, lane='network', reset='broad'),
    'P6_report': dict(BASE, lane='report', reset='result', flat=2),
    'P7_skill_responsive': dict(BASE, skill='responsive'),
    'P8_skill_lagging': dict(BASE, skill='lagging', reset='broad'),
    'P9_acute_only': dict(BASE, health='acute', repair='current'),
    'P10_stay_no_discount': dict(BASE, reset='stay', flat=0, repair='once'),
    'P11_current_warning': dict(BASE, repair='current', health='buffer'),
}
SEEDS = {'sanity': list(range(220000, 220016)), 'screen': list(range(221000, 221032)),
         'confirm': list(range(222000, 222096)), 'holdout': list(range(223000, 223128))}


def write(name, value):
    (OUT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')


def digest(value): return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def freeze():
    OUT.mkdir(parents=True, exist_ok=True)
    if (OUT/'freeze.json').exists(): raise RuntimeError('freeze already exists; do not overwrite')
    source = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in Path(__file__).parent.glob('*.py')}
    value = {'frozen_at': datetime.now(timezone.utc).isoformat(), 'code': source,
        'policies': POLICIES, 'seeds': SEEDS, 'seed_hashes': {k: digest(v) for k,v in SEEDS.items()},
        'identity': identity(), 'selection': 'screen top two non-baselines by >=75 rate then q90 among floor no more than 2 extra terminals vs B2; always retain B0-B3. Confirm finalists unchanged; final holdout once, no retuning.',
        'floor_gate': 'at least 8/16 sanity episodes complete, multiple Energy/Main decisions; otherwise no macro search',
        'story': 'fixed functional verb scoring; tie lowest legal choice; no event/title answer keys; no reward tuning',
        'feasibility_interface_probes': {'partial_episodes': 2, 'full_episodes': 0,
            'score_opened': False, 'note': 'initialization/menu checks only; one stopped at 30 actions, one at natural terminal without score display'}}
    write('freeze.json', value)
    return value


def metrics(rows):
    scores = [r['score']['quantitative_score'] for r in rows if not r.get('technical_error')]
    # Score key validated from public terminal payload; never sent to policy.
    good = [r for r in rows if not r.get('technical_error')]
    if not scores: return {'n':len(rows),'technical_failures':len(rows)}
    ordered=sorted(scores)
    def q(f):
        pos=(len(ordered)-1)*f; lo=int(pos); hi=min(lo+1,len(ordered)-1)
        return ordered[lo]*(hi-pos)+ordered[hi]*(pos-lo) if hi!=lo else ordered[lo]
    levels=Counter(r['status']['level'] for r in good)
    return {'n':len(rows), 'valid_n':len(good), 'technical_failures':len(rows)-len(good),
        'complete':sum(r['complete'] for r in good), 'rate48':sum(r['complete'] for r in good)/len(rows),
        'early_terminal_rate':sum(not r['complete'] for r in good)/len(rows),
        'terminal_reasons':dict(Counter(r['terminal_reason'] for r in good if not r['complete'])),
        'levels':dict(levels), 'L5_rate':sum(int(r['status']['level'][1:])>=5 for r in good)/len(rows),
        'L6_rate':sum(int(r['status']['level'][1:])>=6 for r in good)/len(rows),
        'mean':statistics.mean(scores),'median':statistics.median(scores),
        'q10':q(.1),'q25':q(.25),'q75':q(.75),'q90':q(.9),'max':max(scores),
        'p70':sum(x>=70 for x in scores)/len(rows),'p75':sum(x>=75 for x in scores)/len(rows),
        'promotion_counts':dict(Counter(len(r['promotions']) for r in good)),
        'promotion_months':dict(Counter(m for r in good for m in r['promotions']))}


async def batch(stage, ids):
    if stage != 'sanity':
        sanity = json.loads((OUT/'sanity-summary.json').read_text(encoding='utf-8'))
        if sanity['policies']['B0_balanced']['complete'] < 8:
            raise RuntimeError('frozen feasibility gate failed; macro search prohibited')
    disable_network()
    frozen=json.loads((OUT/'freeze.json').read_text(encoding='utf-8'))
    for name, sha in frozen['code'].items():
        assert hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest()==sha, name
    engine=make_engine(); process=PolicyProcess(); started=time.perf_counter()
    target=OUT/f'{stage}.jsonl'
    if target.exists(): raise RuntimeError('no automatic rerun/overwrite')
    summary={}; allrows=[]
    try:
        # Official lazy process globals become initialized through real public
        # play. Warmup is retained, never a searched/evaluation seed.
        warmup=await episode(engine,process,219999,BASE,trace=True)
        write(f'{stage}-warmup.json',warmup)
        with target.open('w',encoding='utf-8') as f:
            for pid in ids:
                rows=[]
                for seed in frozen['seeds'][stage]:
                    try: row=await episode(engine,process,seed,frozen['policies'][pid],trace=stage=='sanity')
                    except Exception as exc: row={'seed':seed,'technical_error':str(exc)}
                    row['policy_id']=pid; row['config']=frozen['policies'][pid]
                    rows.append(row); allrows.append(row)
                    f.write(json.dumps(row,ensure_ascii=False)+'\n');f.flush()
                # Sanity is terminal/surface feasibility only; do not optimize score.
                summary[pid]=metrics(rows)
                print(json.dumps({'stage':stage,'policy':pid,'metrics':summary[pid]},ensure_ascii=False),flush=True)
    finally: process.close()
    write(f'{stage}-summary.json', {'stage':stage,'policies':summary,'seconds':time.perf_counter()-started,
        'episodes':len(allrows),'finished_at':datetime.now(timezone.utc).isoformat(),'processes':2,'engine_processes':1})


def main():
    parser=argparse.ArgumentParser();parser.add_argument('stage',choices=['freeze',*SEEDS]);parser.add_argument('--policies',nargs='+')
    a=parser.parse_args()
    if a.stage=='freeze': print(json.dumps(freeze(),ensure_ascii=False,indent=2))
    else: asyncio.run(batch(a.stage,a.policies or (['B0_balanced'] if a.stage=='sanity' else list(POLICIES))))


if __name__=='__main__':main()
