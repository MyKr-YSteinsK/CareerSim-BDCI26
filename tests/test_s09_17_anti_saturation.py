"""Written-policy regression and typed assertion fixtures; no model execution.

The semantic fixtures describe assertion scope, certainty and public support.
Their oracle is deliberately test-only: it does not parse free-form LLM prose,
rank live choices, or prove that an LLM follows the written policy.
"""
import hashlib
import json
from pathlib import Path
import subprocess

import pytest

ROOT = Path(__file__).resolve().parents[1]
BASE = '678c161f70e8e7d01839d10de9868156c430ffec'
ID = 'candidate-v10b-policy-constitution-anti-saturation'
TEXT = (ROOT / 'skills/rolling-planning/SKILL.md').read_text(encoding='utf-8')


def source(path):
    return subprocess.check_output(['git', 'show', f'{BASE}:{path}'], cwd=ROOT)


def assertion_supported(scope, certainty, public_basis, local_response=None):
    """Support a typed fixture's assertion, never infer a global cap from NG.

    A public completion/cap is scoped to exactly the opportunity/dimension it
    describes. Acknowledging UNKNOWN is allowed even if vocabulary includes cap.
    A current-path discount is distinct from saturation of a whole family.
    """
    if certainty == 'UNKNOWN':
        return True
    if scope == ('local_path', 'Skill'):
        return local_response in ('NO_GAIN', 'REPEATED_NO_GAIN')
    return public_basis is not None and public_basis['scope'] == scope


# Each route below is an authored counterfactual expectation, not an executed
# candidate action or a policy-ranking implementation. The exact-body regression
# below proves that pre-existing controllers enforcing these routes are retained.
SCENARIOS = [
    ('01_skill_100_no_cap', 'Skill=100, no public upper bound', 'UNKNOWN',
     ('不得仅因数值高', '均保持 UNKNOWN')),
    ('02_high_skill_clean_ng', 'High Skill; clean current-path NO_GAIN', 'LOCAL_DISCOUNT',
     ('local NO_GAIN 仍只折价当前 Level/context/dimension/family', '不保证高数值仍会增长')),
    ('03_two_ng_same_context', 'Two NO_GAIN at same Level/context', 'STRONGER_LOCAL_DISCOUNT_NOT_FAMILY_CAP',
     ('一次或少量 local NO_GAIN、近期停滞', '不推 cap、不重复刷 gap')),
    ('04_level_change', 'Prior NG followed by new Level', 'RESET_UNKNOWN',
     ('重置 S/N/O response 为 UNKNOWN', '旧 NO_GAIN 不永久继承')),
    ('05_same_level_new_context_gain', 'Same Level; later different context yields GAIN', 'REOPEN_CURRENT_RESPONSE',
     ('当前 Level/context 有 fresh positive evidence', 'NO_GAIN 不永久放弃')),
    ('06_explicit_completion', 'Public certification completion reached', 'STOP_THIS_OPPORTUNITY_ONLY',
     ('公开上限/完成只约束对应维度/机会，不外推', '对应上限/完成条件')),
    ('07_network_responsive_skill_ng', 'Known high-value Network response; local Skill NG', 'EXPLOIT_NETWORK',
     ('known high-value responsive path 优先', 'clean NO_GAIN → known responsive alternative 优先')),
    ('08_near_real_delivery', 'Near real Delivery independently needs preparation', 'DELIVERY_CAN_WIN',
     ('Near valuable realization? FINISH/VERIFY/CONVERT', '强独立 Delivery/多维价值可胜出')),
    ('09_acute_binding', 'Fresh acute material threat', 'PROTECT_CAN_WIN',
     ('Binding? PROTECT/CONTAIN', 'acute symptoms 即使显示资源充足也可 bind')),
    ('10_no_alt_untested_skill', 'No responsive alternative; legal untested Skill', 'BOUNDED_COMPARISON_NOT_AUTOMATIC_SELECTION',
     ('加入 top candidate comparison', '不自动选择', 'UNKNOWN 不臆造 eligibility')),
    ('11_high_skill_low_network_skill_gain', 'High Skill is responsive, Network lower', 'SKILL_CAN_CONTINUE_NO_BALANCING',
     ('Known responsive capital? EXPLOIT', '不按最低数字、固定菜单、S/N/O 比例或频次决定')),
    ('12_skill_ng_strong_ownership', 'Local Skill NG and strong ownership Main', 'OWNERSHIP_CAN_WIN',
     ('New ownership? CREATE', 'ownership/真实结果/多维资本/期权价值')),
]


@pytest.mark.parametrize('name,context,route,clauses', SCENARIOS)
def test_twelve_written_scenarios(name, context, route, clauses):
    assert context and route
    assert all(clause in TEXT for clause in clauses), name
    # Even scenarios favoring a different route do not establish a whole-family
    # saturation assertion; NG remains useful for current-path discount.
    assert not assertion_supported(('dimension', 'Skill'), 'ASSERTED', None, 'NO_GAIN')
    assert assertion_supported(('dimension', 'Skill'), 'UNKNOWN', None, 'NO_GAIN')


VOCABULARY = ('capped', 'cap reached', 'saturated', 'enough', 'no longer useful',
              '已封顶', '已经够了', '没必要再投入', '这个维度无用了', '到顶', '已满')


@pytest.mark.parametrize('word', VOCABULARY)
@pytest.mark.parametrize('basis', ['HIGH_NUMBER', 'ONE_LOCAL_NO_GAIN', 'RECENT_STAGNATION'])
def test_vocab_semantic_assertions_not_substring_ban(word, basis):
    # Same word: unsupported family assertion rejected; UNKNOWN accepted;
    # scoped explicit public evidence accepted. Keyword presence is never a ban.
    claims = [
        dict(surface=word, scope=('dimension', 'Skill'), certainty='ASSERTED', public=None),
        dict(surface=f'是否 {word} UNKNOWN', scope=('dimension', 'Skill'), certainty='UNKNOWN', public=None),
        dict(surface=f'public evidence: {word}', scope=('opportunity', 'certification'), certainty='ASSERTED',
             public=dict(scope=('opportunity', 'certification'), evidence='public completion reached')),
    ]
    assert basis and claims[0]['surface'] in VOCABULARY
    assert [assertion_supported(c['scope'], c['certainty'], c['public'], 'NO_GAIN') for c in claims] == [False, True, True]


def test_explicit_cap_and_completion_do_not_spill_to_other_scopes():
    cap = dict(scope=('dimension', 'Health'), evidence='public upper bound reached')
    completion = dict(scope=('opportunity', 'certification'), evidence='public completed')
    assert assertion_supported(('dimension', 'Health'), 'ASSERTED', cap)
    assert not assertion_supported(('dimension', 'Skill'), 'ASSERTED', cap)
    assert assertion_supported(('opportunity', 'certification'), 'ASSERTED', completion)
    assert not assertion_supported(('dimension', 'Skill'), 'ASSERTED', completion)
    assert assertion_supported(('local_path', 'Skill'), 'ASSERTED', None, 'NO_GAIN')
    assert assertion_supported(('local_path', 'Skill'), 'ASSERTED', None, 'REPEATED_NO_GAIN')
    assert not assertion_supported(('local_path', 'Skill'), 'ASSERTED', None, 'GAIN')


def test_only_c6_guard_added_all_other_policy_bytes_normalized_identical():
    old = source('skills/rolling-planning/SKILL.md').decode('utf-8').replace('\r\n', '\n')
    lines = TEXT.splitlines(keepends=True)
    guard = [line for line in lines if line.startswith('  **Do not invent saturation.**')]
    assert len(guard) == 1 and len(guard[0]) <= 450
    assert TEXT.replace(guard[0], '') == old
    assert TEXT.index(guard[0]) > TEXT.index('**C6｜')
    assert TEXT.index(guard[0]) < TEXT.index('**C7｜')
    assert all(f'**C{i}｜' in TEXT for i in range(1, 11))
    assert '不强制学习/探索/重试' in guard[0]
    assert '不保证高数值仍会增长' in guard[0]
    # Master ranking, Main/Energy, trace schema, modes and probe conditions are
    # unchanged because the entire text outside the one inserted line is equal.
    assert len(TEXT) == len(old) + len(guard[0])


def test_v10b_identity_exact_parent_no_validation_transfer():
    parent = json.loads(source('configs/current_candidate.json'))
    c = json.loads((ROOT/'configs/current_candidate.json').read_text(encoding='utf-8'))
    manifest = json.loads((ROOT/'configs/runtime_manifest.json').read_text(encoding='utf-8'))
    old_manifest = json.loads(source('configs/runtime_manifest.json'))
    assert c['candidate_id'] == manifest['name'] == ID
    assert c['parent_candidate_id'] == parent['candidate_id']
    assert c['strategy_delta'] == 'ANTI_UNSUPPORTED_SATURATION_WORLD_MODEL_GUARD'
    assert c['parent_identity']['skills'] == parent['skills']
    assert c['parent_identity']['runtime_manifest_sha256'] == parent['runtime_manifest']['sha256']
    assert c['validation'] == {key: False for key in parent['validation']}
    old_manifest['name'] = ID
    assert manifest == old_manifest
    assert c['runtime_manifest']['sha256'] == hashlib.sha256((ROOT/'configs/runtime_manifest.json').read_bytes()).hexdigest()
    assert c['runtime_manifest']['instruction_sha256'] == hashlib.sha256(manifest['instruction'].encode()).hexdigest()
    for item in c['skills']:
        blob = subprocess.check_output(['git', 'hash-object', item['path']], cwd=ROOT, text=True).strip()
        assert item['git_blob'] == blob
    for path in ('skills/structured-state-board/SKILL.md', 'skills/delivery-progress/SKILL.md',
                 'skills/risk-review/SKILL.md', 'scripts/post_run_audit.py', 'scripts/policy_trace_audit.py',
                 'tests/test_s09_15r_policy_constitution.py', 'tests/fixtures/v10a_policy_traces.json',
                 'pyproject.toml', 'uv.lock'):
        assert source(path).replace(b'\r\n', b'\n') == (ROOT/path).read_bytes().replace(b'\r\n', b'\n')
