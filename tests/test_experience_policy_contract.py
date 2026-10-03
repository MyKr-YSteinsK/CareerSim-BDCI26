"""Offline artifact/fixture contracts; does not execute a model or select actions.

Walkthroughs are manual applications of the written policy by Codex. These tests
check completeness and obvious contradictions, not Flash's semantic adherence.
"""
import hashlib
import json
import re
import shutil
from pathlib import Path

import pytest

from scripts.package_candidate import build_submission

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = json.loads((ROOT / 'tests/fixtures/experience_policy_scenarios.json').read_text(encoding='utf-8'))
CASES = FIXTURE['cases']


def test_topology_budget_and_reference_integrity():
    candidate = json.loads((ROOT / 'configs/current_candidate.json').read_text(encoding='utf-8'))
    manifest = json.loads((ROOT / 'configs/runtime_manifest.json').read_text(encoding='utf-8'))
    assert candidate['architecture']['skill_count'] == 3
    assert candidate['architecture']['startup_body_reads'] == ['career-policy-core']
    assert not any(candidate['validation'].values())
    assert hashlib.sha256((ROOT / 'configs/runtime_manifest.json').read_bytes()).hexdigest() == candidate['runtime_manifest']['sha256']
    assert len(manifest['instruction']) < 2000
    budgets = {'career-policy-core': (1500, 2500), 'career-policy-atlas': (1, 2000), 'career-survival-guard': (1000, 1800)}
    for name, (low, high) in budgets.items():
        text = (ROOT / f'skills/{name}/SKILL.md').read_text(encoding='utf-8')
        body = text.split('---', 2)[2].strip()
        assert low <= len(body) <= high
    refs = candidate['skills'][1]['references']
    assert len(refs) == 6
    router = (ROOT / 'skills/career-policy-atlas/SKILL.md').read_text(encoding='utf-8')
    for ref in refs:
        path = ROOT / ref['path']
        assert path.name in router
        assert hashlib.sha256(path.read_bytes()).hexdigest() == ref['sha256']
        text = path.read_text(encoding='utf-8')
        for section in ['WHEN', 'OBJECTIVE', 'PREFER', 'AVOID', 'LOOKAHEAD', 'EXCEPTIONS', 'EVIDENCE']:
            assert re.search(rf'^(?:## )?{section}$', text, re.M)
        assert len(text) < 1800
        assert not re.search(r'RUN\d+|event_id|75\.29|34\.01|M\d+|HiddenRisk\s*=', text)


def test_public_scenario_coverage():
    assert len(CASES) >= 20
    assert len({c['id'] for c in CASES}) == len(CASES)
    assert {c['origin'] for c in CASES} == {'DONOR_CONTRAST', 'NEGATIVE_FAILURE', 'SYNTHETIC', 'AMBIGUOUS'}
    assert FIXTURE['evaluation_mode'] == 'OFFLINE_WRITTEN_POLICY_WALKTHROUGH_NOT_MODEL_EVAL'


@pytest.mark.parametrize('case', CASES, ids=[c['id'] for c in CASES])
def test_written_walkthrough_has_fresh_public_capsule_and_complete_comparison(case):
    capsule = case['capsule']
    assert set(capsule) == {'session', 'month', 'level', 'next_checkpoint', 'resources', 'warning',
                            'objective', 'last_formal_feedback', 'local_clean_responses', 'deliverable', 'legal_choices'}
    walk = case['written_walkthrough']
    for response in capsule['local_clean_responses']:
        assert response['level'] == capsule['level']
        assert response['scope'] == 'same-menu'
    choices = capsule['legal_choices']
    assert [r['choice'] for r in walk['all_choice_review']] == [m['choice'] for m in choices]
    for option, review in zip(choices, walk['all_choice_review'], strict=True):
        assert review['immediate'] == option['semantics']
        assert 'UNKNOWN' in review['next_checkpoint']
        assert review['affordable'] == (option['energy_cost'] <= capsule['resources']['Energy'])
        assert review['assessment']
    selected = next(m for m in choices if m['choice'] == walk['choice'])
    assert selected['energy_cost'] <= capsule['resources']['Energy']
    assert walk['choice'] in case['acceptable_choices']
    assert (ROOT / 'skills/career-policy-atlas/references' / walk['card']).is_file()
    assert walk['card'] == case['expected_route']
    assert walk['guard'] == case['guard_required'] == (capsule['warning'] != 'NONE')
    assert walk['hidden_evidence_used'] is False
    assert walk['survival_constraint_respected'] is True
    assert walk['reason'] == case['expected_principle']


def test_packaging_refuses_unexpected_asset_before_writing(tmp_path):
    source = tmp_path / 'source'
    shutil.copytree(ROOT / 'skills', source / 'skills')
    shutil.copytree(ROOT / 'configs', source / 'configs')
    (source / 'skills/career-policy-atlas/references/local.db').write_bytes(b'not a policy reference')
    output = tmp_path / 'output'
    with pytest.raises(ValueError, match='Unexpected Skill asset'):
        build_submission(source, output)
    assert not output.exists()


def test_packaging_preserves_nonempty_output(tmp_path):
    output = tmp_path / 'output'
    output.mkdir()
    sentinel = output / 'existing.txt'
    sentinel.write_text('preserve', encoding='utf-8')
    with pytest.raises(FileExistsError):
        build_submission(ROOT, output)
    assert sentinel.read_text(encoding='utf-8') == 'preserve'


def test_packaging_rejects_inconsistent_identity(tmp_path):
    source = tmp_path / 'source'
    shutil.copytree(ROOT / 'skills', source / 'skills')
    shutil.copytree(ROOT / 'configs', source / 'configs')
    path = source / 'configs/current_candidate.json'
    candidate = json.loads(path.read_text(encoding='utf-8'))
    candidate['architecture']['active_skills'].append('undeclared-skill')
    path.write_text(json.dumps(candidate), encoding='utf-8')
    with pytest.raises(ValueError, match='inconsistent or unsafe'):
        build_submission(source, tmp_path / 'output')
