---
name: rolling-planning
description: "Use for every CareerSim decision after fresh Board and Delivery are available. 维护晋升复利主线、当前 Review checkpoint 与有界恢复；将 Primary Gap 作为方向性提示，默认 MODE=A，仅在明确重大约束下短暂 MODE=S；比较合法选项并返回唯一 CANDIDATE，不提交动作。"
---

# Rolling Planning｜滚动规划与失败恢复

## 职责

本 Skill 是唯一战略层。

目标：

> 在守住 survival floor 的前提下，最大化 48 个月长期晋升与职业资本；坏局面出现时进行有界恢复，恢复后回到长期主线。

维护：

```text
REVIEW_PLAN = <Long Horizon | Primary Gap | Next Review Checkpoint>
MODE = <A|S>
RECOVERY = <NONE|PROGRESSION|RESOURCE|RISK|DELIVERY|UNKNOWN>
```

- `A=Advance`：默认。
- `S=Stabilize`：只用于明确、当前、重大的生存/连续性约束。
- `RECOVERY` 描述当前失败模式，不自动决定 `MODE`。

禁止：使用 `HiddenRisk`、hidden counters、internal score、internal event id/effect、其它隐藏/私有证据、固定事件答案、隐藏阈值、跨局记忆或自行提交动作。

## 证据优先级

只使用同局白名单 Board、Delivery、正式 Review、最新 fresh observe 中参与者可见的 event 描述与合法 choice 语义、公开合法选项、Handbook 与已确认公开结果。

progression 判断优先级：

1. 正式 `Review / promotion / no-advance`；
2. clean fresh observed result；
3. 当前 `STATE / STICKY / PROGRESSION_RESPONSE`；
4. Delivery 证据；
5. advertised effect / public hint。

低优先级证据不得覆盖高优先级冲突证据。

## 长期规划一致性

长期目标固定为：

`SURVIVE AS A HARD FLOOR → PROMOTE → COMPOUND CAREER CAPITAL`

Survival / Continuity 是 hard floor，不是持续最大化目标。没有 fresh participant-visible material constraint 时，默认 MODE=A，把行动预算用于 promotion 和 career-capital compounding。Recovery 只能临时改变短期路径，解除约束或修复后回主线。

每次 Formal Review 后重建：

- 当前 Level、S/N/O progression response 与公开 career capital；
- 最新公开 Review feedback、仍可用的成长路径与真实 Delivery exception；
- 当前公开 horizon 内下一项可由合法行动影响的 checkpoint。

`REVIEW_PLAN = <Long Horizon | Primary Gap | Next Realizable Checkpoint>`：

- `Long Horizon` 始终是稳定约束下的 promotion compounding；
- `Primary Gap` 是最新 Review / public progression evidence 给出的方向性提示，不是永久目标；具体反馈不清时用 `DIRECT_PROGRESSION_EVIDENCE`；
- 每次 Formal Review 都更新整个 plan，旧 gap、rationale 和 ranking 不自动继承；Review 已结算后，行动服务下一 checkpoint，不能补救已结束的 Review。

低绩效、`no-promotion`、弱 S/N/O、一般 Story 或短期波动都不单独改写长期主线或触发 MODE=S。良好绩效 + `no-promotion` 仍表示 promotion readiness 未完成；当前公开 horizon 内下一次真实 Formal Review 是准备 checkpoint。第一次 Review 前可用 `Primary Gap=UNKNOWN`，先做广义成长与可靠交付。

## Failure Recovery Contract

### `PROGRESSION`

触发：低绩效、`no-promotion`、公开 Skill/Network/Output 或 delivery 表现不足、晋升准备未完成。保持 `MODE=A`，重建方向性 gap；先从 `PROGRESSION_RESPONSE` 与合法选项中找仍有响应、能在 checkpoint 前兑现的 promotion path。失败本身不授权长期保守。

退出：promotion；Review 明确显示原方向已解决；或 fresh evidence 证明原路径无响应且已完成正向重分配。

### `RESOURCE`

触发：fresh public evidence 明确表明 Health / Dignity / Wealth、affordability 或 income continuity 已形成重大 binding constraint，使正常活动受到实质限制。

处理：`MODE=S` 只做解除当前约束所需的最小合理动作，并尽量保留 progression value。fresh public evidence 显示约束已解除或场景结束后，立即回 `MODE=A` 并恢复长期主线。不得补满资源或为“更安全”延长 S。

### `RISK`

触发：fresh public warning 明确表示风险 elevated / accumulating / needs handling，且存在明确 reparative legal option。通常保持 `MODE=A`，至多一次 bounded cleanup；完成一次 cleanup 后 fresh observe，默认回长期主线。只有同一风险仍未解除/再次 elevated，或出现新的同类 warning，才允许再次 cleanup。无关证据不得重置限制。只有风险成为 material survival / job-continuity / trust / compliance / confidentiality crisis 才进入 `MODE=S`。

### `DELIVERY`

触发：fresh public evidence 表明 checkpoint=NEAR、active blocker、高价值结果未验证且当前可验证、explicit Review linkage，或当前选择会明显破坏已确认的高价值近端交付。通常保持 `MODE=A`，优先完成、验证或修复高价值近端交付；只对该 exception 给予短期优先。普通 `IN_PROGRESS + NOT_NEAR` 且无 blocker/linkage 只作背景证据，不持续抬高 ranking。交付完成并公开验证、commitment 取消/替代，或 fresh evidence 改变 Review path 后退出。

## MODE

判断 MODE 前，必须结合 Board 与当前 participant-visible event/choice 语义及 fresh observe，确认是否存在尚未解除、当前 binding 的 material constraint；不得只根据状态数字或旧 Review 判断。

以下内容单独不能触发 `MODE=S`：

- 低绩效；
- `no-promotion`；
- weak Skill / Network / Output；
- generic “improve performance”；
- 一次数值下降；
- 普通工作负荷、疲劳、摩擦或不确定性。

只有 fresh public evidence 明确显示 material survival / safety / job-continuity / trust / compliance / confidentiality / affordability / income-continuity constraint，或重大 Health/Dignity/Wealth 约束已使正常活动不可行时，才使用 `S`。

`S` 必须有明确 binding reason 与退出条件，只执行 minimum necessary stabilization。约束解除后立即回 `A`。低绩效、`no-promotion`、弱 Skill/Network/Output、普通疲劳/负荷/摩擦/不确定性均不单独触发 `S`。

## Progression Routing

读取 Board `PROGRESSION_RESPONSE`：

- `GAIN`：当前 Level 下该维度最近可响应；
- `NO_GAIN`：只降低该维度当前边际价值；
- `UNKNOWN`：保持开放，不当成 cap。

规则：

1. clean `NO_GAIN` 只局部降低当前 Level/context 下对应 dimension/path 的即时边际价值；先刷新当前 response，再扫描其余合法 promotion-relevant 路径并做 positive reallocation。
2. 有 still-responsive progression path 时，不因一个 `NO_GAIN` 转向低价值 Health/safety filler，也不立即重复同一路径。
3. multidimensional action 中，一个维度 `NO_GAIN` 不抹掉其它 `GAIN/UNKNOWN` 价值；只要其它 promotion-relevant 维度仍 `GAIN/UNKNOWN`，不得整体否决该 action。
4. non-specific Review 下，只保护当前 `GAIN/UNKNOWN` 的 Skill / Network / Output；当前 Level 的 `NO_GAIN` 不承担 coverage 义务，直到 Level change 或后续 clean `GAIN` 重置/覆盖。Level change 后所有 response 重新开放。
5. specific feedback 可短期集中，但 `Primary Gap` 只在路径仍 responsive 且无更高价值选项时影响 ranking。不得推断 hidden/permanent cap、eligibility 或 promotion impossibility。
6. 不设固定 action、比例、target、月份或隐藏阈值；Skill 不因 terminal-score saturation 假设被降权。

## Ranking

`MODE=S` 只处理当前 binding constraint，并保留可行的 progression value；约束解除后立即回 `A`。

无 binding constraint 时默认 `MODE=A`，按以下顺序选择：

1. **Time-sensitive realization exception：**明确且当前可实现的 Review/promotion realization；满足 `DELIVERY` 触发条件的近端交付、blocker、高价值待验证结果或 explicit Review linkage，优先于普通 Portfolio 比较。
2. **Promotion Portfolio：**条件式比较 broad progression 与 Primary Gap，不设固定全局先后。
   - **Broad compounding** 是 strong default prior：still-responsive Skill / Network / Output、career capital、ownership / visibility、verified realizable result，以及多维 promotion-relevant 合法行动。
   - **Conditional Primary Gap** 只有在最新 Review feedback fresh 且 specific、对应路径仍 responsive、存在 participant-visible legal action 且进展能在 next realizable checkpoint 前兑现时，才获得 strong directional weight；没有更高优先级 realization exception 或更新的 superseding / clean `NO_GAIN` evidence 时，可以短期成为 dominant path。不得仅因过去投入而维持其 dominance。
   - **Dominance expiry：**新 Formal Review 重建 Portfolio、fresh evidence supersedes gap、对应路径变为 `NO_GAIN` / non-responsive，或 checkpoint 已过时，旧 gap 不再 dominant 且不跨 Review 自动继承；不得长期因此压掉其它 still-responsive promotion-relevant paths。
3. **Long-horizon option value：**不牺牲当前明确可兑现机会时保留未来复利价值。
4. **Filler：**只有当前没有 meaningful progression / realization path 时才考虑低价值 safety / filler。

不得把普通 `IN_PROGRESS` 当成全局高优先级；action 名称、固定比例或数字下降本身不决定 ranking。

## Final Horizon

使用公开固定 48-month horizon，不构造不存在的未来 Review。当剩余 horizon 内已没有下一项 Formal Review 时，从 review preparation 切换到 `terminal-horizon direct realization`：优先当前可立即兑现的 career capital、public-state value、ownership / visibility、verified result 与有依据的 survival protection。不得以 M54 / future Review 为理由做准备，也不得编码固定 promotion month。

如果明确的 job-continuity threat 由绩效或交付失败造成，直接修复绩效、完成关键交付或恢复晋升成长可作为 constraint relief；`MODE=S` 不等于停止成长。

## Quarterly Control

季度第一次 Energy 只记录当前目标：

```text
QUARTER_INTENT = <MODE | current target>
```

不得预先承诺剩余 Energy 的动作数量、选择序列或固定批次。旧 `QUARTER_INTENT` 是目标提示，不授权后续动作。

每轮只能选一个 Energy action，并依次完成：

```text
fresh same-session observe
→ Board rebuild and PROGRESSION_RESPONSE update
→ Delivery rebuild
→ new Planning pass for remaining Energy
→ Risk and executor preflight
→ submit exactly one action
→ CONTROL_STATE=OBSERVE_REQUIRED
```

动作 receipt 只有 `success/error`，不能解除 `OBSERVE_REQUIRED`、更新 Board 或授权下一动作。每次 fresh observe 后，丢弃旧剩余动作意图；Board、Delivery、Planning 和 Risk 完成新一轮后才可重新 READY。observe 失败或 session 不匹配时为 `BLOCKED`，禁止 action。

出现 clean `OBSERVED_NO_GAIN` 后，Board 先记录该维度 `NO_GAIN`，然后必须重建 Planning 并重新分配剩余 Energy。若存在 responsive alternative，不得立即再次选择同一个 no-gain action；旧批次计划不能覆盖该门禁。

例如 Energy=3、Output=26：第一次 Report Preparation 后 fresh observe 仍为 Output=26 时，下一轮必须看到 Board `O=NO_GAIN` 并执行新的 Planning pass；存在 responsive alternative 时，第二次 immediate Report Preparation 不符合合同。

越接近下一 Review，剩余 Energy/Main opportunity 越稀缺；无 binding constraint 时，优先 still-responsive、能在 checkpoint 前兑现的 promotion-relevant progress。

Main Action 使用同一 ranking，不按菜单名字固定答案。

## Decision Budget

`ONE FRESH OBSERVE = ONE PLANNING PASS`

每次：

1. 确认 `MODE + RECOVERY + REVIEW_PLAN`；
2. 删除明显不可接受或被支配的选项；
3. 最多保留两个 genuinely competitive candidates；
4. 比较一次；
5. 输出唯一 `CANDIDATE`。

只有 Risk=`RECONSIDER` 可在同一 fresh evidence 下重开一次，并且只比较一个直接相关替代项。

没有 new public evidence 不得反复自我辩论、重复规划或换候选。

## 输出

只返回：

```text
PLAN: G=<gap|?> P=<A|S|?> F=<NONE|PROGRESSION|RESOURCE|RISK|DELIVERY|UNKNOWN> checkpoint=<short checkpoint>
CANDIDATE: choice=<one legal integer> reason=<one concise public-evidence reason>
```

**Can Submit Action: No.**
不得调用 `new_game`、`observe` 或 `take_action`。
