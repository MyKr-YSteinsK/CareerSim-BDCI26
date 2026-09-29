---
name: structured-state-board
description: "Use after every fresh observe and during same-session recovery. 将当前局公开状态、正式 Review、未解除重大警告，以及当前 Level 下 Skill/Network/Output 的可归因响应整理成唯一紧凑 Board；只记录事实，不规划、不评估候选风险、不推断隐藏规则、不提交动作。"
---

# Structured State Board｜结构化状态板

## 职责

本 Skill 是当前游戏 session 的事实层。只负责整理：

- 当前公开状态；
- 最新正式 `Review / promotion / no-advance`；
- 尚未解除的重大公开约束；
- 当前 Level 下 `Skill / Network / Output` 的可归因成长响应；
- 仍无法确认的决策相关事实。

禁止：制定战略目标、排序合法选项、执行 Risk gate、推断隐藏机制、提交动作。

## 输入

只使用：

- 最新 fresh `observe`；
- 紧邻前一动作的已确认公开结果；
- 当前 session 的上一版 Board；
- recovery 必要时的少量同局公开日志。

禁止使用其他 game、隐藏字段、数据库、局后取证结论或跨局记忆。

## 输出

每次输出完整替换 Board：

```text
SESSION: <game_session_id> | M=<month> Q=<quarter>
STATE: H=<Health> D=<Dignity> S=<Skill> N=<Network> O=<Output> W=<Wealth> L=<Level> E=<Energy>
TENURE: <public value | UNKNOWN>
REVIEW: <latest formal grade/feedback/promotion/no-advance | none>
PROGRESSION_RESPONSE: S=<GAIN|NO_GAIN|UNKNOWN> N=<GAIN|NO_GAIN|UNKNOWN> O=<GAIN|NO_GAIN|UNKNOWN> LEVEL=<Level>
STICKY: <unresolved binding public warning(s) | none>
EFFECTS: <up to 2 attributable recent effects | none>
UNKNOWN: <decision-relevant unresolved facts | none>
```

## STATE

1. 先确认 `game_session_id` 与 freshness。session 不匹配时丢弃旧 Board。
2. `STATE` 只从最新参与者可见的 `current_state.status` 直接复制，保持原值与精度。
3. 字段缺失或公开身份不明确时写 `UNKNOWN`。
4. 不根据工资、bonus、事件描述、advertised effect、旧观察或 action notes 计算、补全、修正或预测 `STATE`。
5. 其它公开信息如有价值，作为独立事实保留；等待 fresh observe 更新 `STATE`。

## REVIEW 与 STICKY

`REVIEW` 保存最新正式绩效、晋升、未晋升及公开反馈。

以下内容单独不能形成 binding `STICKY`：

- 低绩效；
- `no-promotion`；
- 普通绩效不足；
- Skill / Network / Output 偏弱；
- 一次数值下降；
- 普通工作负荷、疲劳或不确定性。

这些属于 Planning 的 progression 问题。

只有 fresh public evidence 明确显示尚未解除的重大约束时才进入 `STICKY`，例如：

- affordability / income-continuity crisis；
- 明确重大 Health / Dignity warning；
- 明确 dismissal / job-continuity threat；
- 明确严重 Network isolation，且公开文本说明其已经威胁 job continuity / trust；
- material accident / trust / compliance / confidentiality / safety crisis；
- 公开资源明显枯竭，且正常活动已不可行。

acute physical / psychological / safety warning 必须进入 `STICKY`，即使公开数值看起来尚可。

只有 fresh public evidence 明确表明约束已解除，或对应风险场景已经结束，才移出 `STICKY`。

## PROGRESSION_RESPONSE

目的：保留“当前 Level 下，该成长维度最近一次可归因投入是否真实生效”的事实；不得推断 cap。

分别维护 `S / N / O`：

- `GAIN`：某合法动作公开说明会正向影响该维度，且紧邻 fresh observe 中该维度真实增加；
- `NO_GAIN`：满足清晰归因条件，但该维度保持不变；
- `UNKNOWN`：未测试、证据缺失或存在混杂。

规则：

1. 只有“紧邻动作 → fresh observe”，且不存在 review、promotion、salary、无关事件或其它动作混杂时才更新。
2. 只更新该动作明确涉及的维度；其它维度沿用上一版同局 Board。
3. 后续 clean `GAIN` 覆盖旧 `NO_GAIN`。
4. Level 改变时，`S/N/O` 全部重置为 `UNKNOWN`。
5. session 改变时全部重置。
6. `NO_GAIN` 只说明当前 Level/context 下最近一次可归因投入未产生该公开增长；不得推断 cap、threshold、formula、eligibility 或 hidden cause。

## EFFECTS

最多保留两个 recent effects。

只有清晰归因时记录具体 effect。若存在 salary、review、promotion、无关 event 或其它 plausible cause，写：

`EFFECTS: UNKNOWN / MIXED`

`PROGRESSION_RESPONSE` 是 current-Level 的紧凑事实载体；`EFFECTS` 只保存最近局部变化。

## Recovery

出现 resume / compaction / recovery 后：

1. 确认仍为同一 `game_session_id`；
2. 先 fresh observe；
3. 重建 `STATE / REVIEW / STICKY`；
4. 仅在必要时读取少量同局公开历史，重建 `PROGRESSION_RESPONSE / EFFECTS`；
5. 无法可靠恢复的字段写 `UNKNOWN`；
6. 不沿用无法验证的旧 Board。

## 不变量

- observed fact 与 `UNKNOWN` 必须分开。
- `HiddenRisk`、hidden counters、internal score、internal event id/effect、public-status-unclear numeric fields 一律 `EXCLUDE_FROM_STRATEGY`。
- 不引用、不比较、不总结、不记忆上述受限值。
- 不累积完整 transcript。
- **Can Submit Action: No.**
