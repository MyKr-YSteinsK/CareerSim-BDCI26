"""Written policy + hand-annotated principle contrasts; NOT model execution.

No action oracle or runtime enforcement. Fixtures compare evidence handling,
not exact Story choices, success probabilities or promotion thresholds.
"""
import copy
import hashlib
import json
from pathlib import Path
import subprocess

import pytest

ROOT = Path(__file__).resolve().parents[1]
BASE = 'a825c2d7463880ef15ee87f57878be66d748fd09'
P = (ROOT / 'skills/rolling-planning/SKILL.md').read_text(encoding='utf-8')
M = json.loads((ROOT / 'configs/runtime_manifest.json').read_text(encoding='utf-8'))
CASES = json.loads((ROOT / 'tests/fixtures/v11b_early_result_cases.json').read_text(encoding='utf-8'))
BASIS = {'deadline', 'commitments', 'resource_margin', 'complexity_workload',
         'completion_criteria', 'result_before_review', 'safety_compliance_trust',
         'delayed_capital_option_value'}


def prior(path):
    return subprocess.check_output(['git', 'show', f'{BASE}:{path}'], cwd=ROOT)


def annotation_valid(facts, response):
    """Validate authored reasoning annotations, never choose a gameplay option."""
    applies = facts['before_first_review'] and facts['competing_routes']
    if response['early_comparison'] != applies:
        return False
    if applies and set(response['public_comparison_basis']) != BASIS:
        return False
    if not applies and response['public_comparison_basis']:
        return False
    if response['ordinary_v11_ranking'] is not True:
        return False
    if response['numeric_promotion_target'] is not None or response['hidden_probability'] is not None:
        return False
    if response['fixed_route'] or response['invented_opportunity'] or response['output_catch_up']:
        return False
    if response['cross_game_memory'] or response['global_cap'] or response['ignores_integrity']:
        return False
    if response['feasibility_known'] != facts['feasibility_evidence']:
        return False
    if response['discount_delay'] != (applies and facts['public_delay']):
        return False
    if response['local_response_rerank'] != facts['fresh_no_gain']:
        return False
    if facts['fresh_no_gain'] and response['discount_scope'] != 'CURRENT_LEVEL_CONTEXT_DIMENSION_FAMILY':
        return False
    if facts['short_downside'] and not response['compares_short_downside']:
        return False
    if facts['long_in_window'] and not response['long_route_can_compete']:
        return False
    if facts['thin_margin'] and not response['preserves_g3']:
        return False
    if facts['material_risk'] and not response['persistent_risk_authority']:
        return False
    if facts['public_result'] and not response['visibility_can_compete']:
        return False
    if facts['clean_growth'] and not response['clean_aggression']:
        return False
    return True


@pytest.mark.parametrize('case', CASES, ids=lambda c: c['name'])
def test_principle_annotations_and_negative_contrasts(case):
    assert annotation_valid(case['facts'], case['annotation'])
    bad = copy.deepcopy(case['annotation'])
    bad.update(case['negative'])
    assert not annotation_valid(case['facts'], bad)
    for clause in case['written_basis']:
        assert clause in P


@pytest.mark.parametrize('clause', [
    '仅首个formal Review前', '公开期限/时长、承诺、H/资源余量、复杂度/负荷、完成标准',
    '下次Review前可见结果、安全/合规/信任下行及延期后资本/期权价值',
    '可兑现性证据不足UNKNOWN，不猜概率', '短路结果可达、长路有排期风险且资源支持可偏短',
    '长路窗口内可完且价值强，或短路有安全/质量下行可偏长',
    '公开延期即折价，守诚信重评合法项；无机会不编造',
    '首评后按上述v11排序',
    'advertised gain未兑现以fresh response重排当前合法ownership/result/capital；不补固定O',
])
def test_new_written_comparative_principles(clause):
    assert clause in P
    assert clause not in prior('skills/rolling-planning/SKILL.md').decode('utf-8')


@pytest.mark.parametrize('mutation', [
    {'local_response_rerank': False}, {'discount_scope': 'ALL_CAREER_GROWTH'},
    {'numeric_promotion_target': 'O>=3'}, {'hidden_probability': 0.9},
    {'cross_game_memory': True}, {'invented_opportunity': True},
])
def test_local_adaptation_rejects_new_controller_or_hidden_recipe(mutation):
    case = next(c for c in CASES if c['name'] == 'RUN20_a13_a14_like_fresh_no_gain')
    bad = copy.deepcopy(case['annotation'])
    bad.update(mutation)
    assert not annotation_valid(case['facts'], bad)


def test_exact_two_planning_replacements_and_minimal_manifest_mirror():
    before = prior('skills/rolling-planning/SKILL.md').decode('utf-8').replace('\r\n', '\n')
    changed = ('local clean NO_GAIN', 'Main用同一排序')
    before_lines = [s for s in before.splitlines() if not s.startswith(changed)]
    current_lines = [s for s in P.splitlines() if not s.startswith(('advertised gain未兑现', 'Main用同一排序'))]
    assert current_lines == before_lines
    parent = json.loads(prior('configs/runtime_manifest.json'))
    mirror = '首评前ownership路线按Planning比较公开窗口内成果可兑现性与下行，长资产/短路径均非固定答案；advertised未兑现仅fresh局部重排，不补固定O/推cap。'
    assert M['instruction'].count(mirror) == 1
    assert M['instruction'].replace(mirror, '') == parent['instruction']
    assert {k: v for k, v in M.items() if k not in {'name', 'instruction'}} == {
        k: v for k, v in parent.items() if k not in {'name', 'instruction'}}
    assert len(P) <= len(before) * 1.06
    assert len(M['instruction']) <= len(parent['instruction']) * 1.03
    # No new marker, enum, certificate, preflight or controller in the ABI.
    heading = 'SYSTEM ACTION PREFLIGHT / BASIS_CHECK'
    assert M['instruction'].split(heading)[1] == parent['instruction'].split(heading)[1]


def test_candidate_identity_parent_hashes_flags_and_protected_scope():
    c = json.loads((ROOT / 'configs/current_candidate.json').read_text(encoding='utf-8'))
    parent = json.loads(prior('configs/current_candidate.json'))
    assert c['candidate_id'] == M['name'] == 'candidate-v11b-early-result-feasibility'
    assert c['parent_candidate_id'] == parent['candidate_id']
    assert c['parent_identity']['skills'] == parent['skills']
    assert c['parent_identity']['runtime_manifest_sha256'] == parent['runtime_manifest']['sha256']
    assert c['parent_identity']['instruction_sha256'] == parent['runtime_manifest']['instruction_sha256']
    assert c['base_evidence_sha'] == BASE
    assert c['strategy_delta'] == 'PRE_FIRST_REVIEW_RESULT_FEASIBILITY_COMPARISON'
    assert c['secondary_strategy_delta'] == 'LOCAL_REALIZED_RESPONSE_REPLAN'
    assert c['submission_fallback'] == parent['submission_fallback']
    assert not any(c['validation'].values())
    for key in ('runner_sha', 'header_schema_version', 'basis_annotation_schema_version',
                'information_policy_delta', 'runtime_contract_delta', 'architecture'):
        assert c[key] == parent[key]
    assert c['runtime_manifest']['sha256'] == hashlib.sha256((ROOT / 'configs/runtime_manifest.json').read_bytes()).hexdigest()
    assert c['runtime_manifest']['instruction_sha256'] == hashlib.sha256(M['instruction'].encode()).hexdigest()
    for skill in c['skills']:
        assert skill['git_blob'] == subprocess.check_output(['git', 'hash-object', skill['path']], cwd=ROOT, text=True).strip()
    for path in ('skills/structured-state-board/SKILL.md', 'skills/delivery-progress/SKILL.md',
                 'skills/risk-review/SKILL.md', 'scripts/reviewer_gate.py', 'scripts/live_run_controller.py',
                 'scripts/live_review_packet.py', 'scripts/basis_preflight_audit.py',
                 'scripts/post_run_audit.py', 'scripts/package_candidate.py', 'pyproject.toml', 'uv.lock'):
        assert (ROOT / path).read_bytes().replace(b'\r\n', b'\n') == prior(path).replace(b'\r\n', b'\n')
    assert not subprocess.check_output(['git', 'diff', BASE, '--', 'career_sim_runner', 'submission', 'submissions'], cwd=ROOT)


def test_ordinary_v11_protections_remain_written():
    for clause in ('CLEANUP_ACTION != RISK_CLEARED', '同scope explicit public de-escalation',
                   'ownership不能自动覆盖风险', 'RESULT_CONVERSION_GAP', 'stale `IN_PROGRESS + UNVERIFIED`',
                   'H+广告ΔH≤0非普通成长', '无广告不等于零成本', '不猜delta/概率/安全值',
                   'clean growth保持进攻', 'local clean NO_GAIN只折价当前Level/context/dimension/family',
                   '高数/局部停滞不证明career cap', '无更强替代时可比较一个合法未测试high-value family',
                   'ONE ENERGY STEP = choose best current marginal action only',
                   '一个action→fresh observe再重排', 'HiddenRisk ±N', 'Can Submit Action: No.'):
        assert clause in P
