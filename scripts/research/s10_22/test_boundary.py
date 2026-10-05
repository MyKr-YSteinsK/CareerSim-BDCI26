"""Firewall, subprocess isolation, semantics and seeded trajectory checks."""
import ast
import asyncio
import copy
import hashlib
import json
from pathlib import Path
import unittest

from harness import projection, PolicyProcess, make_engine, episode, ROOT, POLICY, disable_network
from policy import Policy, validate, story_score
from search import BASE, OUT, write


def fixture():
    return {'current_state': {'time': {'current_month': 3}, 'status': {
        'health': 7, 'dignity': 7, 'skill': 4, 'network': 3, 'output': 2,
        'wealth': 4, 'energy': 3, 'level': 'L1', 'duration_in_level': 3,
        'hidden_risk': 999, 'failure_counter': 999}, 'statistics': {'secret': 999},
        'failure_rule_remaining_hp': {'secret': 999}},
        'current_event': {'title': '季度精力分配', 'description': '分配当前精力',
            'event_id': 'secret_event', 'future_events': ['secret'], 'remaining_energy': 3},
        'choices': [{'choice': 1, 'action': '准备汇报材料', 'energy_cost': 1,
            'action_id': 'secret_action', 'status_updates': {'HiddenRisk': -999},
            'next_node': 'secret'}, {'choice': 2, 'action': '人脉维护', 'energy_cost': 1}],
        'events': '当前公开反馈', 'ending_score': {'quantitative_score': 999}}


class FirewallTests(unittest.TestCase):
    def test_official_then_allowlist(self):
        from career_emulator.server.models import ObserveResponse
        f=fixture()
        response=ObserveResponse(f['current_state'],f['current_event'],f['choices'],f['events'],f['ending_score'])
        public=projection(response.to_mcp_dict());validate(public)
        payload=json.dumps(public)
        for forbidden in ('hidden_risk','failure_counter','statistics','remaining_hp','event_id',
                          'future_events','action_id','status_updates','next_node','ending_score','999','secret'):
            self.assertNotIn(forbidden,payload)

    def test_input_poison_rejected(self):
        public=projection(fixture())
        for field in ('HiddenRisk','statistics','failure_rule_remaining_hp','ending_score','event_id'):
            for layer in ('top','status','event','choice'):
                o=copy.deepcopy(public)
                target={'top':o,'status':o['status'],'event':o['event'],'choice':o['choices'][0]}[layer]
                target[field]=123
                with self.subTest(field=field,layer=layer),self.assertRaises(ValueError):validate(o)
        o=copy.deepcopy(public);o['status']['health']={'hidden':999}
        with self.assertRaises(ValueError):validate(o)
        o=copy.deepcopy(public);o['month']={'hidden':999}
        with self.assertRaises(ValueError):validate(o)

    def test_policy_has_no_engine_file_network_imports(self):
        t=ast.parse(POLICY.read_text(encoding='utf-8'))
        for n in ast.walk(t):
            if isinstance(n,ast.Import): self.assertTrue(all(x.name in {'json','re','sys'} for x in n.names))
            self.assertFalse(isinstance(n,ast.ImportFrom))
            if isinstance(n,ast.Call) and isinstance(n.func,ast.Name):
                self.assertNotIn(n.func.id,{'open','exec','eval','__import__'})
        source=' '.join(n.id for n in ast.walk(t) if isinstance(n,ast.Name))
        for forbidden in ('career_emulator','read_text','read_bytes','socket','subprocess','pathlib'):
            self.assertNotIn(forbidden,source)

    def test_subprocess_and_story_control(self):
        p=PolicyProcess()
        try:
            p.call({'reset':BASE});o=projection(fixture());reply=p.call({'observation':o})
            self.assertIsInstance(reply['choice'],int)
            self.assertIn(reply['choice'],[1,2])
            self.assertEqual(reply['kind'],'energy')
            self.assertEqual(reply['family'],'report')
            bad=copy.deepcopy(o);bad['status']['HiddenRisk']=99
            with self.assertRaises(RuntimeError):p.call({'observation':bad})
            self.assertGreater(story_score('公司数据涉及保密','申请授权并脱敏'),story_score('公司数据涉及保密','私下发送给外部'))
            self.assertGreater(story_score('身体报警医生建议休息','暂停工作就医'),story_score('身体报警医生建议休息','继续硬扛通宵'))
        finally:p.close()

    def test_same_level_flat_and_level_reset(self):
        p=Policy(BASE);o=projection(fixture());first=p.choose(o)
        o2=copy.deepcopy(o);o2['status']['energy']=2
        p.choose(o2)
        self.assertEqual(p.response['report']['flats'],1)
        o3=copy.deepcopy(o2);o3['status']['level']='L2';p.choose(o3)
        self.assertEqual(p.response,{})

    def test_failed_gate_blocks_macro_before_episode(self):
        from search import batch
        with self.assertRaisesRegex(RuntimeError,'feasibility gate failed'):
            asyncio.run(batch('screen',['B2_v6d_like']))


async def reproducibility():
    disable_network();engine=make_engine();process=PolicyProcess()
    try:
        rows=[await episode(engine,process,219999,BASE,trace=True) for _ in range(3)]
    finally:process.close()
    cleaned=[{k:v for k,v in r.items() if k!='seconds'} for r in rows]
    write('reproducibility-attempt.json', {'rows':rows})
    assert cleaned[1]==cleaned[2], 'warm engine same seed not reproducible'
    write('reproducibility.json', {'seed':219999,'episodes':3,'pass':True,
        'cold_vs_warm_equal':cleaned[0]==cleaned[1],
        'trajectory_hash':hashlib.sha256(json.dumps(cleaned[1],sort_keys=True).encode()).hexdigest(),
        'actions':rows[0]['action_count'],'score_schema':list((rows[0]['score'] or {}).keys())})
    print(json.dumps({'reproducibility':'PASS','score_schema':rows[0]['score']},ensure_ascii=False))


if __name__=='__main__':
    result=unittest.TextTestRunner().run(unittest.defaultTestLoader.loadTestsFromTestCase(FirewallTests))
    if not result.wasSuccessful():raise SystemExit(1)
    asyncio.run(reproducibility())
