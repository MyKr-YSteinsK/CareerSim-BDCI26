"""Frozen public-semantic nuisance baseline and categorical macro approximations.

Research only. No CareerSim imports, event identities, scores, or effect tables.
Run as a JSON-lines subprocess; an episode reset also resets all local evidence.
"""
import json
import re
import sys

STATUS = {'health', 'dignity', 'skill', 'network', 'output', 'wealth', 'energy',
          'level', 'duration_in_level'}
OBS = {'month', 'status', 'event', 'choices', 'feedback'}
EVENT = {'title', 'description', 'rules', 'remaining_energy', 'energy_budget', 'max_selections'}
CHOICE = {'choice', 'action', 'description', 'energy_cost'}


def validate(o):
    if type(o.get('month')) is not int or not isinstance(o.get('feedback'), str):
        raise ValueError('non-public month/feedback type')
    if set(o) != OBS or set(o['status']) - STATUS or set(o['event']) - EVENT:
        raise ValueError('non-public observation field')
    for c in o['choices']:
        if set(c) - CHOICE or not isinstance(c.get('choice'), int):
            raise ValueError('non-public choice field')
    for value in [*o['status'].values(), *o['event'].values(), o['feedback']]:
        if not isinstance(value, (str, int, float, bool, type(None))):
            raise ValueError('nested non-public value')
    for c in o['choices']:
        if any(not isinstance(v, (str, int, float, bool, type(None))) for v in c.values()):
            raise ValueError('nested choice value')


def has(text, words):
    return any(w in text for w in words.split('|'))


def story_score(situation, text):
    # Generic functional verbs only; never a story title/description -> answer map.
    score = 0
    if has(text, '伪造|造假|隐瞒|掩盖|甩锅|泄露|泄密|盗用|报复|绕过审批|违规|篡改'):
        score -= 12
    if has(text, '明确授权|申请授权|征得同意|合规|脱敏|匿名化|审批|遵守保密|如实|坦诚|主动报告|及时报告'):
        score += 5
    if has(text, '沟通|协商|澄清|确认|讨论|反馈|求助|请教|一起|合作'):
        score += 2
    if has(text, '承担|负责|交付|验证|复盘|指导|分享|分析|解决|推动|学习'):
        score += 2
    if has(text, '梳理|分工|阶段|优先级|计划|范围|评估|边界'):
        score += 1
    if has(text, '不管|不理|无视|随便|敷衍|装作|硬扛|通宵|强行|孤注一掷'):
        score -= 4
    if has(situation, '住院|晕倒|急诊|严重透支|身体报警|医生建议|胸痛'):
        if has(text, '休息|就医|请假|暂停|健康|调整工作量'):
            score += 10
    if has(situation, '严重超负荷|无法承受|严重过劳|任务超载'):
        if has(text, '协商|调整|分工|优先级|拒绝|求助'):
            score += 4
    if has(situation, '保密|机密|公司数据|敏感数据|个人信息'):
        if has(text, '直接发送|私下发送|拷贝给|发给外部|私人邮箱'):
            score -= 10
    return score


def family(text):
    if has(text, '汇报'): return 'report'
    if has(text, '人脉'): return 'network'
    if has(text, '高强度'): return 'intensive'
    if has(text, '健康恢复'): return 'health'
    if has(text, '埋雷'): return 'cleanup'
    if has(text, '技能学习'): return 'skill'
    if has(text, '心理恢复'): return 'psychological'
    return 'other'


class Policy:
    def __init__(self, config):
        self.config = config
        self.last = None
        self.response = {}
        self.warning = False
        self.repaired = False
        self.mode = 'unknown'
        self.health_trend = False
        self.growth = {k: 0 for k in ('skill', 'network', 'output')}

    def choose(self, o):
        validate(o)
        s = o['status']; e = o['event']; cs = o['choices']
        text = o['feedback'] + ' ' + e.get('description', '')
        promoted_now = False
        if self.last:
            old, chosen, kind = self.last
            if s.get('level') != old['status'].get('level'):
                self.response = {}; self.growth = dict.fromkeys(self.growth, 0)
                self.mode = 'promoted'
                promoted_now = True
            if s.get('health', 0) != old['status'].get('health', 0):
                self.health_trend = s['health'] < old['status']['health']
            if kind == 'energy' and old['month'] == o['month'] and old['status'].get('level') == s.get('level'):
                f = family(chosen['action'])
                target = {'report': 'output', 'intensive': 'output', 'network': 'network',
                          'skill': 'skill', 'health': 'health', 'psychological': 'dignity'}.get(f)
                if target:
                    delta = s[target] - old['status'][target]
                    prev = self.response.get(f, {'flats': 0})
                    self.response[f] = {'gain': delta > 0, 'flats': 0 if delta > 0 else prev['flats'] + 1}
                    if target in self.growth: self.growth[target] += max(0, delta)
        serious = has(text, '自求多福|全要炸|严重警告|严重风险|信任危机|开除|解雇|泄密|重大事故|合规警告')
        mild = has(text, '积累了一些风险|潜在风险|历史遗留风险|风险隐患|埋的雷')
        clearance = has(text, '风险已解除|风险已经解除|隐患已消除|隐患已经消除|合规问题已解决|合规问题已经解决')
        if serious or mild: self.warning = True; self.repaired = False
        elif clearance: self.warning = False
        elif self.config['repair'] == 'current': self.warning = False
        elif self.config['repair'] == 'once' and self.repaired: self.warning = False
        if has(o['feedback'], '半年绩效|绩效评级|绩效等级|半年度') and not promoted_now:
            self.mode = 'result' if has(text, '成果|产出|结果|业绩') else 'visibility'
        acute = has(text, '住院|急诊|身体报警|严重透支|健康警告|健康堪忧|严重过劳')
        recover = acute or (self.config['health'] != 'acute' and self.health_trend)
        if self.config['health'] == 'buffer':
            recover = recover or has(text, '疲惫|劳累|加班|压力|身心|繁重')
        # First selection is initialization, macro classification is menu-based.
        fs = [family(c['action']) for c in cs]
        if any(f != 'other' for f in fs) and has(e.get('description', '') + e.get('title', ''), '精力|Energy|季度行动'):
            kind = 'energy'
            budget = min(s.get('energy', 0), e.get('remaining_energy', s.get('energy', 0)))
            legal = [c for c in cs if c.get('energy_cost', 0) <= budget]
            if not legal: raise ValueError('no affordable public Energy option')
            ranked = []
            for c in legal:
                f = family(c['action']); value = {'report': 4, 'network': 3, 'skill': 1,
                    'intensive': 2, 'health': 0, 'cleanup': 0, 'psychological': 0, 'other': -3}[f]
                if f == 'cleanup' and self.warning: value += 14
                if f == 'health' and recover: value += 16
                if f == 'psychological' and has(text, '崩溃|精神健康|抑郁|心理警告'): value += 16
                r = self.response.get(f)
                if r and r['gain']: value += 2
                flats = self.config['flat']
                if r and flats and r['flats'] >= flats: value -= 6
                if self.mode == 'promoted' and self.config['momentum'] == 'preserve' and f in ('report', 'network', 'intensive', 'skill'): value += 1
                if self.mode in ('result', 'visibility'):
                    if self.config['reset'] == 'result' and f == 'report': value += 2
                    if self.config['reset'] == 'broad' and f in ('network', 'skill'): value += 2
                if self.config['lane'] == 'network' and f == 'network': value += 3
                if self.config['lane'] == 'report' and f == 'report': value += 2
                if self.config['lane'] == 'responsive' and f == 'network' and self.growth['network'] < self.growth['output']: value += 2
                if f == 'skill':
                    if self.config['skill'] == 'disabled': value -= 8
                    elif self.config['skill'] == 'responsive' and self.response.get('report', {}).get('flats', 0): value += 4
                    elif self.config['skill'] == 'lagging' and self.growth['skill'] < max(self.growth.values()): value += 4
                if f == 'intensive':
                    if self.config['main'] == 'aggressive' and (has(text, '交付|截止|里程碑') or self.response.get('report', {}).get('flats', 0)): value += 4
                    if recover or serious: value -= 16
                ranked.append((value, -c.get('energy_cost', 0), -c['choice'], c))
            chosen = max(ranked, key=lambda x: x[:3])[3]
            if family(chosen['action']) == 'cleanup': self.repaired = True
        elif any(has(c['action'], '关键项目|低调避险|跳槽') for c in cs):
            kind = 'main'
            ranked = []
            for c in cs:
                a = c['action']; value = 0
                if has(a, '关键项目'): value = 5
                if has(a, '低调避险') and (acute or serious or (self.warning and self.config['main'] == 'risk')): value = 9
                if has(a, '关键项目') and self.config['main'] == 'aggressive' and not acute and not serious: value += 2
                ranked.append((value, -c['choice'], c))
            chosen = max(ranked, key=lambda x: x[:2])[2]
        else:
            kind = 'story'
            chosen = max(cs, key=lambda c: (story_score(e.get('description', ''), c['action']), -c['choice']))
        self.last = (o, chosen, kind)
        return {'choice': chosen['choice'], 'kind': kind, 'family': family(chosen['action']), 'mode': self.mode}


def main():
    p = None
    for line in sys.stdin:
        try:
            request = json.loads(line)
            if 'reset' in request:
                p = Policy(request['reset']); reply = {'reset': True}
            else:
                reply = p.choose(request['observation'])
            print(json.dumps(reply, ensure_ascii=False), flush=True)
        except Exception as exc:
            print(json.dumps({'error': str(exc)}), flush=True)


if __name__ == '__main__': main()
