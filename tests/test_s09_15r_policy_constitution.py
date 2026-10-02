"""Written-policy acceptance and executable offline measurement, not model behavior."""
import hashlib
import json
from pathlib import Path
import subprocess

import pytest

from career_sim_runner.skill_contract import validate_submission_contract
from scripts.package_candidate import build_submission
from scripts.policy_trace_audit import extract, parse_trace
from scripts.post_run_audit import CTRL, DL, audit

ROOT = Path(__file__).resolve().parents[1]
BASE = '10734f0d23b015e0e686bd87a9dd2b8660c8760e'
ID = 'candidate-v10a-policy-constitution'
FIXTURES = json.loads((ROOT/'tests/fixtures/v10a_policy_traces.json').read_text(encoding='utf-8'))
TEXT = (ROOT/'skills/rolling-planning/SKILL.md').read_text(encoding='utf-8')
START, END = '2026-10-01T16:00:00+00:00', '2026-10-01T17:00:00+00:00'
SESSION = 'a' * 32


def source(path):
    return subprocess.check_output(['git', 'show', f'{BASE}:{path}'], cwd=ROOT)


@pytest.mark.parametrize('scenario,clauses', [
    ('01_new_project_no_commitment', ('MAIN-1', 'strong prior, not a fixed answer')),
    ('02_near_real_result_convert', ('Near valuable realization', 'REAL RESULT → VISIBILITY/RECOGNITION')),
    ('03_generic_report_no_real_result', ('strong priority 必须有 real-result basis', '不能仅标签/反馈就泛化汇报')),
    ('04_loaded_ownership_mentor_can_win', ('ownership 已重', 'MAIN-3', '新机会集')),
    ('05_rotation_escape_stagnation', ('Skill/role diversification', 'stalled-path escape', '可赢 generic Apply')),
    ('06_compliance_bind_contain', ('Binding? PROTECT/CONTAIN', 'trust/compliance/confidentiality')),
    ('07_uncertainty_not_avoid', ('MAIN-4', 'ordinary uncertainty 不自动赢')),
    ('08_no_promotion_rebuild_direction', ('Review/promotion/no-promotion 重建下一窗口方向', 'no-promotion 不自动 S')),
    ('09_responsive_output_can_continue', ('responsive Output 可继续', 'Known responsive capital? EXPLOIT')),
    ('10_ng_output_responsive_network', ('clean NO_GAIN → known responsive alternative 优先', 'known high-value responsive path 优先')),
    ('11_ng_no_alt_untested_skill_compare', ('无更高价值 known responsive 合法替代', '合法未测试且公开语义支持高价值 growth family', '不自动选择')),
    ('12_ng_real_delivery_independent_value', ('stalled path 仅因强独立 Delivery/多维价值可胜出', 'real result 待包装')),
    ('13_ng_preparation_no_real_result', ('无 real result + repeated preparation NO_GAIN 不继续刷', '不能仅因 Primary Gap=Output 立即重复')),
    ('14_level_reset_options', ('重置 S/N/O response 为 UNKNOWN', '旧 NO_GAIN 不永久继承')),
    ('15_ordinary_cost_not_recovery', ('轻微 Health cost', '单独不证明 binding', '不设数值阈值')),
    ('16_acute_warning_minimum_protection', ('acute symptoms 即使显示资源充足也可 bind', '最小机会成本保护')),
    ('17_trust_compliance_protection', ('明确 compliance/trust crisis', '生存/合规/信任无重大 binding')),
    ('18_resolved_return_advance', ('fresh evidence 证明解除 → 立即回 A', '不补满资源')),
    ('19_skill_gain_not_fixed_recipe', ('Skill GAIN 不等于 always Skill', '不预定 recipe/batch/剩余序列')),
    ('20_responsive_no_forced_probe', ('存在 responsive path 不为覆盖率探索', '无 exploration quota')),
])
def test_twenty_written_counterfactuals(scenario, clauses):
    assert all(c in TEXT for c in clauses), scenario


def test_constitution_priority_one_ranking_and_regression_interfaces():
    assert len(TEXT) <= 7500
    assert TEXT.index('## CONSTITUTION') < TEXT.index('## Evidence')
    assert all(f'**C{i}｜' in TEXT for i in range(1,11))
    assert '高于后续解释性 prose' in TEXT and TEXT.count('## One Master Ranking') == 1
    for clause in ('EXCLUDE_FROM_STRATEGY until verified public', 'event answer lookup',
                   '最多两个 genuinely competitive candidates', 'Risk=RECONSIDER 最多一次',
                   'Can Submit Action: No.',
                   'DECISION_CLOSED 不结束 assistant execution', '每次 action 后 fresh observe',
                   'UNKNOWN 不当 GAIN', '不连续 probe 两个未知 family',
                   'Primary Gap 是 attention cue', 'context recovery', '不建 durable ledger'):
        assert clause in TEXT


def test_identity_hashes_and_no_evidence_transfer():
    c = json.loads((ROOT/'configs/current_candidate.json').read_text(encoding='utf-8'))
    parent = json.loads(source('configs/current_candidate.json'))
    m = json.loads((ROOT/'configs/runtime_manifest.json').read_text(encoding='utf-8'))
    assert c['candidate_id'] == m['name'] == ID
    assert c['parent_candidate_id'] == parent['candidate_id']
    assert c['parent_identity']['skills'] == parent['skills']
    assert c['validation'] == {k:False for k in parent['validation']}
    assert c['runtime_manifest']['sha256'] == hashlib.sha256((ROOT/'configs/runtime_manifest.json').read_bytes()).hexdigest()
    old_manifest = json.loads(source('configs/runtime_manifest.json')); old_manifest['name'] = ID
    assert old_manifest == m
    for item in c['skills']:
        assert item['git_blob'] == subprocess.check_output(['git','hash-object',item['path']],cwd=ROOT,text=True).strip()
    for path in ('skills/structured-state-board/SKILL.md','skills/delivery-progress/SKILL.md','skills/risk-review/SKILL.md','scripts/post_run_audit.py','pyproject.toml','uv.lock'):
        assert not subprocess.check_output(['git','diff','--name-only',BASE,'--',path],cwd=ROOT,text=True).strip()


def test_canonical_offline_package(tmp_path):
    build_submission(ROOT, tmp_path/'submission')
    result = validate_submission_contract(tmp_path/'submission')
    assert result['submission_mode'] == 'skill_bundle'
    assert set(result['skill_ids']) == {'structured-state-board','rolling-planning','delivery-progress','risk-review'}


@pytest.mark.parametrize('name', ['positive','negative','ambiguous'])
def test_trace_fixtures(name):
    case = FIXTURES[name]; result = parse_trace(case['notes'])
    assert result['status'] == case['expected_status']
    assert int(result['selected']) == case['selected']


@pytest.mark.parametrize('mutation', ['missing','duplicate','contradiction','wrong_basis','wrong_prior','bad_family'])
def test_trace_invalid_fails_closed(mutation):
    notes = FIXTURES['positive']['notes']
    notes = {'missing':notes.replace('[PROBE','[OTHER'), 'duplicate':notes+notes,
             'contradiction':notes.replace('K=11111','K=10111'),
             'wrong_basis':notes.replace('B=PROBE','B=OTHER'),
             'wrong_prior':notes.replace('RP=UNKNOWN','RP=GAIN'),
             'bad_family':notes.replace('S=1 F=S','S=1 F=N')}[mutation]
    assert parse_trace(notes)['status'] in {'MISSING_OR_MALFORMED','INCONSISTENT'}


def stream(tmp_path, notes, delta=1, month_change=False, duplicate=False):
    rows=[]
    def emit(kind,payload):
        rows.append(dict(seq=len(rows)+1,ts='2026-10-01T16:30:00+00:00',kind=kind,payload=payload))
    def obs(cid,skill,month=9):
        emit('tool_result',dict(tool_call_id=cid,tool_name='mcp_career-emulator_observe',raw_output=dict(result=dict(current_state=dict(session_id=SESSION,time=dict(current_month=month),status=dict(level='L2',skill=skill,network=7,output=6)),current_event=dict(title='季度体力行动分配'),choices=[dict(choice=2,action='技能学习',status_updates=dict(Skill=1,HiddenRisk=999))],events=''))))
    obs('o1',20)
    for i,note in enumerate(notes):
        cid=f'a{i}'
        emit('tool_call',dict(tool_call=dict(tool_call_id=cid,name='mcp_career-emulator_take_action',arguments=dict(session_id=SESSION,choice=2,notes=note))))
        if duplicate: rows.append(dict(rows[-1]))
        emit('tool_result',dict(tool_call_id=cid,tool_name='mcp_career-emulator_take_action',raw_output=dict(result=dict(success=True))))
        obs(f'o{i+2}',20+delta*(i+1),10 if month_change else 9)
    events=tmp_path/'events.jsonl'; events.write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows),encoding='utf-8')
    return events


@pytest.mark.parametrize('delta,expected', [(1,'GAIN'),(0,'NO_GAIN'),(-1,'UNKNOWN_OR_MIXED')])
def test_probe_action_fresh_response(tmp_path,delta,expected):
    p=stream(tmp_path,[FIXTURES['positive']['notes']],delta,duplicate=True)
    result=extract(p,START,END)
    assert result['measurement_status']=='PASS' and result['actions']==1
    assert result['metrics']['probe_selected_count']==1
    assert result['rows'][0]['probe_response']==expected
    assert 'HiddenRisk' not in json.dumps(result)


def test_ambiguous_missing_and_transition_not_zero(tmp_path):
    r=extract(stream(tmp_path,[FIXTURES['ambiguous']['notes']]),START,END)
    assert r['measurement_status']=='STOP_BEFORE_PROVIDER' and r['metrics']['probe_eligible_count'] is None
    r=extract(stream(tmp_path,['ordinary legacy notes']),START,END)
    assert r['trace_covered']==0 and r['metrics']['probe_selected_count'] is None
    r=extract(stream(tmp_path,[FIXTURES['positive']['notes']],month_change=True),START,END)
    assert r['metrics']['probe_UNKNOWN_count']==1


def test_negative_and_blocked_are_measured(tmp_path):
    blocked=FIXTURES['negative']['notes'].replace('K=10111','K=11101').replace('B=RESPONSIVE','B=PROTECT')
    r=extract(stream(tmp_path,[FIXTURES['negative']['notes'],blocked]),START,END)
    assert r['measurement_status']=='PASS'
    assert r['metrics']['probe_eligible_count']==0 and r['metrics']['probe_blocked_by_binding_constraint_count']==1


def test_consecutive_probe_chain_detected(tmp_path):
    r=extract(stream(tmp_path,[FIXTURES['positive']['notes']]*2),START,END)
    assert r['metrics']['consecutive_probe_violations']==1


def test_run10_separator_is_actual_auditor_condition(tmp_path):
    # Full existing auditor path, not a relaxed second parser.
    notes=FIXTURES['negative']['notes']; events=stream(tmp_path,[notes])
    transcript=tmp_path/'transcript.log'; transcript.write_text(f'SESSION={SESSION}',encoding='utf-8')
    receipt=tmp_path/'receipt.json'; receipt.write_text('{"exit_code":0}',encoding='utf-8')
    good=audit(events,transcript,None,receipt,run_start=START,run_end=END)
    assert good['adherence_evidence']['delivery_marker_coverage']['valid']==1
    events=stream(tmp_path,[notes.replace('] [DL','][DL')])
    bad=audit(events,transcript,None,receipt,run_start=START,run_end=END)
    assert bad['adherence_evidence']['delivery_marker_coverage']['valid']==0
    assert DL.search(notes) and DL.search(notes.replace('] [DL','][DL'))
    assert extract(events,START,END)['measurement_status']=='STOP_BEFORE_PROVIDER'


def test_window_session_and_legality_fail_closed(tmp_path):
    p=stream(tmp_path,[FIXTURES['positive']['notes']])
    with pytest.raises(ValueError): extract(p,'2026-10-01T16:00:00',END)
    text=p.read_text(encoding='utf-8').replace('"choice": 2, "notes"','"choice": 99, "notes"')
    p.write_text(text,encoding='utf-8')
    with pytest.raises(ValueError,match='public menu'): extract(p,START,END)
