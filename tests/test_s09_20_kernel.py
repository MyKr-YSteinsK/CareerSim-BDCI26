"""Static written-contract + annotated evidence oracle, not LLM behavior tests."""
import hashlib
import json
from pathlib import Path
import subprocess

import pytest

from career_sim_runner.skill_contract import validate_submission_contract
from scripts.basis_preflight_audit import check_basis, measure_receipts, parse_basis_receipt
from scripts.package_candidate import build_submission

ROOT = Path(__file__).resolve().parents[1]
BASE = '63c703f8979a4bebf7d1bc72249019a56343550e'
CASES = json.loads((ROOT/'tests/fixtures/v10c_kernel_cases.json').read_text(encoding='utf-8'))
REPLAY = json.loads((ROOT/'tests/fixtures/v10c_run11_contract_replay.json').read_text(encoding='utf-8'))
MANIFEST = json.loads((ROOT/'configs/runtime_manifest.json').read_text(encoding='utf-8'))
INSTRUCTION = MANIFEST['instruction']


@pytest.mark.parametrize('case', CASES, ids=lambda c:c['name'])
def test_scenarios(case):
    result = check_basis(case['notes'], case['evidence'])
    assert result['status'] == case['expected']
    if case['reason']:
        assert case['reason'] in result['reasons']
    assert result['may_submit'] == (case['expected'] == 'PASS')
    assert parse_basis_receipt(result['receipt'])['valid']


@pytest.mark.parametrize('case', REPLAY['cases'], ids=lambda c:f"a{c['action']}")
def test_run11_contract_projection(case):
    result = check_basis(case['notes'], case['evidence'])
    assert result['status'] == case['expected']
    assert set(case['reasons']) <= set(result['reasons'])
    assert '[BC=' not in case['notes']  # Never retroactively attribute a receipt.


def test_manifest_contract_ownership_and_retirement():
    for literal in ('K1 PUBLIC', 'K2 SATURATION', 'K3 MODE', 'K4 CLEANUP', 'K5 SUMMARY',
                    'SYSTEM ACTION PREFLIGHT / BASIS_CHECK', '[POL B=<PROTECT|DELIVER|RESPONSIVE',
                    '[PROBE K=<five 0/1/?>', 'POL/PROBE 必需', 'EXCLUDE_FROM_STRATEGY until verified public',
                    'STOP_BEFORE_ACTION', '至多一次 bounded re-plan', '共用最多一次 closure budget',
                    'affected state/semantics UNKNOWN', '[BC=PASS]', '不是外部工具拦截器',
                    'summary', '首次 action 前依次读取', 'OBSERVE_REQUIRED'):
        assert literal in INSTRUCTION
    assert 'RECOVERY_PENDING' not in INSTRUCTION and 'RECOVERY_READY' not in INSTRUCTION
    assert 'epoch 检测或强制四 Skill 重读' in INSTRUCTION
    assert len(INSTRUCTION) <= 1.10 * len(json.loads(subprocess.check_output(
        ['git','show',f'{BASE}:configs/runtime_manifest.json'],cwd=ROOT))['instruction'])


def test_protected_strategy_and_minimal_ownership_change():
    path='skills/rolling-planning/SKILL.md'
    old=subprocess.check_output(['git','show',f'{BASE}:{path}'],cwd=ROOT).decode().replace('\r\n','\n')
    new=(ROOT/path).read_text(encoding='utf-8')
    def strategy(t):
        start=t.index('## CONSTITUTION'); end=t.index('## One Master Ranking')
        left=t[start:end].split('context recovery')[0]
        ranking=t[end:t.index('## Decision closure')]
        probe=t[t.index('POL：B=最终候选依据'):]
        return left,ranking,probe
    assert strategy(old) == strategy(new)
    for p in ('skills/structured-state-board/SKILL.md','skills/delivery-progress/SKILL.md',
              'skills/risk-review/SKILL.md','scripts/post_run_audit.py','scripts/package_candidate.py',
              'pyproject.toml','uv.lock'):
        before=subprocess.check_output(['git','show',f'{BASE}:{p}'],cwd=ROOT).replace(b'\r\n',b'\n')
        assert before == (ROOT/p).read_bytes().replace(b'\r\n',b'\n')


def test_candidate_identity_and_no_transferred_validation():
    c=json.loads((ROOT/'configs/current_candidate.json').read_text(encoding='utf-8'))
    assert c['candidate_id'] == MANIFEST['name'] == 'candidate-v10c-compaction-agnostic-kernel'
    assert c['parent_candidate_id'] == 'candidate-v10b-policy-constitution-anti-saturation'
    assert c['strategy_delta'] == 'NONE' and not any(c['validation'].values())
    assert c['runtime_manifest']['sha256'] == hashlib.sha256((ROOT/'configs/runtime_manifest.json').read_bytes()).hexdigest()
    assert c['runtime_manifest']['instruction_sha256'] == hashlib.sha256(INSTRUCTION.encode()).hexdigest()
    for item in c['skills']:
        assert item['git_blob'] == subprocess.check_output(['git','hash-object',item['path']],cwd=ROOT,text=True).strip()


def test_offline_package(tmp_path):
    build_submission(ROOT,tmp_path/'submission')
    result=validate_submission_contract(tmp_path/'submission')
    assert result['submission_mode'] == 'skill_bundle'
    assert len(result['skill_ids']) == 4


def test_receipt_measurement_missing_is_unknown_and_no_enforcement_claim():
    notes=CASES[0]['notes']
    missing=measure_receipts([notes])
    assert missing['basis_check_present'] == 0
    assert missing['restricted_basis_blocked'] is None
    actual=measure_receipts([notes+' [BC=PASS]',notes+' [BC=BLOCKED WHY=SCHEMA]'],
                            ['[BC=BLOCKED WHY=PUBLIC]','[BC=BLOCKED WHY=SATURATION]',
                             '[BC=BLOCKED WHY=NUMERIC_S]','[BC=BLOCKED WHY=STALE_CLEANUP]'])
    assert actual['basis_check_valid'] == 2 and actual['action_submitted_despite_BLOCKED'] == 1
    assert all(actual[k] == 1 for k in ('restricted_basis_blocked','saturation_basis_blocked','numeric_S_blocked','stale_cleanup_blocked'))
    assert not parse_basis_receipt('[BC=PASS] [BC=PASS]')['valid']
    assert not parse_basis_receipt('[BC=BLOCKED]')['valid']


def test_reordered_schema_fails_and_no_summary_override():
    c=CASES[0]
    notes=c['notes']; p=notes.index(' [POL'); q=notes.index(' [PROBE')
    assert check_basis(notes[:p]+notes[q:]+notes[p:q],c['evidence'])['status'] == 'BLOCKED'
    assert check_basis(CASES[4]['notes'],c['evidence'])['status'] == 'BLOCKED'
    assert check_basis(c['notes'],c['evidence'])['status'] == 'PASS'


def test_exact_window_audit_receipts_and_dedup(tmp_path):
    from scripts.policy_trace_audit import extract
    session='a'*32
    obs=dict(current_state=dict(session_id=session,time=dict(current_month=3),status=dict(level='L1',skill=2)),
             current_event=dict(title='public'),choices=[dict(choice=1,action='public action')],events='')
    call=dict(tool_call_id='a1',name='take_action',arguments=dict(session_id=session,choice=1,
              notes=CASES[0]['notes']+' [BC=BLOCKED WHY=SCHEMA]'))
    parts=[('tool_result',dict(tool_call_id='o1',tool_name='observe',raw_output=dict(result=obs))),
           ('tool_call',dict(tool_call=call)),('tool_call',dict(tool_call=call)),
           ('tool_result',dict(tool_call_id='a1',tool_name='take_action',raw_output=dict(result=dict(success=True)))),
           ('tool_result',dict(tool_call_id='o2',tool_name='observe',raw_output=dict(result=obs)))]
    records=[dict(seq=i,ts='2026-10-02T12:00:00+00:00',kind=k,payload=p) for i,(k,p) in enumerate(parts,1)]
    records.append(dict(seq=9,ts='2026-10-01T12:00:00+00:00',kind='tool_call',payload=dict(tool_call=dict(call,tool_call_id='outside'))))
    path=tmp_path/'events.jsonl';path.write_text(''.join(json.dumps(r)+'\n' for r in records),encoding='utf-8')
    result=extract(path,'2026-10-02T11:00:00+00:00','2026-10-02T13:00:00+00:00')
    assert result['actions'] == 1
    assert result['basis_preflight']['action_submitted_despite_BLOCKED'] == 1
    assert result['basis_preflight']['basis_check_valid'] == 1
    assert result['basis_preflight']['stale_cleanup_blocked'] is None
