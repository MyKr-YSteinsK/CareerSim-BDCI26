---
name: rolling-planning
description: "Use for every CareerSim decision after fresh Board and Delivery are available. 维护跨 Review 的长期晋升目标、当前 Review Window、失败恢复状态与一个 Primary Gap；默认 MODE=A，仅在明确重大生存或连续性约束下临时 MODE=S；比较合法选项并返回唯一 CANDIDATE，不提交动作。"
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

长期主线默认保持：

`SURVIVE → PROMOTE → COMPOUND`

failure recovery 只能暂时改变短期路径，不得无依据改写长期主线。

Review Window：

1. 第一次正式 Review 前允许 `Primary Gap=UNKNOWN`；优先可靠交付与广义 Skill / Network / Output 成长。
2. 正式 Review 后，用最明确的公开 progression deficit 更新 `Primary Gap`。
3. 反馈不具体时使用 `DIRECT_PROGRESSION_EVIDENCE`；不得编造隐藏晋升条件。
4. 良好绩效 + `no-promotion` 仍表示 promotion readiness 未完成。
5. 下一次公开正式 Review 是当前准备 checkpoint。
6. Review 已经结算后，之后动作只能服务下一 checkpoint，不能补救已经发生的 Review。
7. 普通 Story 或一次短期波动不得随意改写 `Primary Gap`。

## Failure Recovery Contract

### `PROGRESSION`

触发：低绩效、`no-promotion`、公开 Skill/Network/Output/delivery 表现不足、晋升准备未完成。

处理：

- 保持 `MODE=A`；
- 重建 `Primary Gap`；
- 使用 `PROGRESSION_RESPONSE` 与 Delivery 找仍有响应、且能在下一 Review 前兑现的路径；
- 不因失败本身进入长期保守。

退出：promotion；Review 明确显示原 gap 已解决；或 fresh evidence 证明当前路径失效并完成重规划。

### `RESOURCE`

触发：fresh public evidence 明确显示 Health / Dignity / Wealth / affordability / income continuity 已形成重大 binding constraint。

处理：

- `MODE=S`；
- 只做解除当前约束所需的最小合理动作；
- 尽量保留 progression value。

退出：fresh public evidence 显示约束已解除或场景结束；立即回 `MODE=A`，恢复原 `REVIEW_PLAN`。

禁止：为了“更安全”把资源补满后长期停留在 S。

### `RISK`

触发：fresh public warning 明确表示风险 elevated / accumulating / needs handling，且存在明确 reparative legal option。

处理：

- 通常保持 `MODE=A`；
- 在下一 Review 前允许一次 bounded cleanup 作为高优先候选；
- 只有风险升级为 material survival / job-continuity / trust / compliance / confidentiality crisis 时才进入 `MODE=S`。

退出：完成一次 cleanup 后必须 fresh observe，并默认回长期主线。只有后续 fresh public evidence 明确表明同一风险仍未解除/再次 elevated，或出现新的同类 warning，才允许再次 cleanup；无关的新 evidence 不得重置限制。

### `DELIVERY`

触发：active commitment 接近 checkpoint，但处于 blocked / unverified / delayed；当前选择明确牺牲近端交付确定性；或 Review 反馈直接指向 delivery / ownership。

处理：

- 通常保持 `MODE=A`；
- 优先完成、验证或修复高价值近端交付；
- 不为 speculative long-horizon gain 无理由牺牲当前 Review 前明确交付。

退出：item `DELIVERED + PUBLICLY_VERIFIED`；commitment 公开取消/被替代；或 fresh evidence 表明继续投入已不是最佳 Review path。

## MODE

判断 MODE 前，必须结合 Board 与当前 participant-visible event/choice 语义判断是否存在尚未解除的 binding constraint；不得只根据状态数字或旧 Review 判断。

以下内容单独不能触发 `MODE=S`：

- 低绩效；
- `no-promotion`；
- weak Skill / Network / Output；
- generic “improve performance”；
- 一次数值下降；
- 普通工作负荷、疲劳、摩擦或不确定性。

只有 fresh public evidence 明确显示 material survival / safety / job-continuity / trust / compliance / confidentiality / affordability / income-continuity constraint，或明确重大 Health/Dignity/Wealth 资源约束已经使正常活动不可行时，才使用 `S`。

`S` 必须有明确 binding reason 与退出条件。约束解除后立即回 `A`。

## Progression Routing

读取 Board `PROGRESSION_RESPONSE`：

- `GAIN`：当前 Level 下该维度最近可响应；
- `NO_GAIN`：只降低该维度当前边际价值；
- `UNKNOWN`：保持开放，不当成 cap。

规则：

1. multidimensional action 中，一个维度 `NO_GAIN` 不抹掉其它 `GAIN/UNKNOWN` 价值。
2. 有仍有响应的合法路径时，不立即重复同一个 no-gain 投入只为再次确认。
3. Level change 后所有 response 重新开放。
4. non-specific Review 下，只对当前 `GAIN/UNKNOWN` 的 Skill / Network / Output 维度维持 coverage；不得因另一维最近更显著而长期忽略仍为 `GAIN/UNKNOWN` 的维度。当前 Level 的 `NO_GAIN` 维度不受 coverage 义务约束，直到 Level change 或后续 clean `GAIN` 重置/覆盖。specific feedback 可以集中投入，但不得依赖 hidden threshold/cap。
5. 不设固定比例、固定 target、隐藏阈值。
6. Skill 不因 terminal-score saturation 假设被降权；它始终可能具有 promotion value。

## Ranking

`MODE=A` 下依次偏好：

1. 当前 `Primary Gap` 的直接、可观察进展；
2. 下一 Review 前可兑现的 delivery / ownership；
3. still-responsive 的 Skill / Network / Output 多维成长；
4. long-horizon compounding / option value。

Review 前，explicit near-term delivery delay / first-delivery uncertainty 是真实负证据。若一个合法选项保持当前交付确定性，另一个只提供 speculative long-horizon gain 且明确损害近端交付，优先交付确定路径；除非 safety/compliance 或 specific Review feedback 明确支持后者。

`MODE=S` 下依次偏好：

1. 不继续恶化 binding constraint；
2. 直接解除或控制该约束；
3. 在安全前提下保留尽可能多 progression value。

如果明确的 job-continuity threat 本身由绩效或交付失败造成，那么直接修复绩效、完成关键交付或恢复晋升成长可以是 `MODE=S` 下最直接的 constraint-relief action；不得把 `S` 机械理解为低调、停止成长或选择最保守动作。

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
