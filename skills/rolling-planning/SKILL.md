---
name: rolling-planning
description: "每次决策必须应用；唯一战略 owner，连接剩余职业轨迹、review objective 与当前合法决策，并维护公开 Primary Gap、Progress、Risk Budget 和必要 checkpoint；不提交动作。"
---

# Rolling Planning｜公开证据滚动规划

## 职责与快速扫描

Planning 是唯一战略 owner。每次决策基于当前 session 的 fresh public facts 与 Board 事实做短 scan：剩余职业轨迹、下个 review window、survival constraint、一个 Primary Gap、Progress 与 remaining realizable horizon。稳健提升 progression、可见交付、复利资产和终局选择空间是 global objective；风险作为约束，不是默认优化目标，也不使用隐藏分数权重。动作改变状态后，先 fresh observe 并更新事实；不得用变更前 scan 决定下一 Energy/Main action。take_action.notes 的唯一控制前缀由 persistent instruction 生成；Planning 不复制标记格式或提交动作。

只使用当前 game_session 的 fresh public evidence、Board 可核实事实与公开 Handbook。不得使用其它对局、局后信息、hidden threshold、evaluator weight 或 Dev 内部公式。

## Planning state

每次决策维护：

- 一个公开 Primary Gap，或证据不足时 UNKNOWN；
- Progress = ADVANCING / STALLED / UNKNOWN；
- Risk Budget = AVAILABLE / TIGHT / UNKNOWN；
- Global Horizon：剩余职业轨迹与仍可实现的 progression / compounding 窗口；
- Review Horizon：到下一个公开 formal review / promotion feedback 的窗口；
- Action Horizon：当前合法候选如何服务 review objective。

## v7 Career trajectory 与目标选择

Global Objective：在合规、生存及有公开依据的重大风险约束下，稳健提升剩余职业生涯的 progression、可见交付、复利资产与终局选择空间。Level/promotion、Skill、Network、Output、Wealth 和可选机会是公开轨迹反馈，不设固定权重或月份 KPI。Promotion/no-promotion 是 progression feedback，可触发 review reset；它本身不是行动配方或成功保证。

Primary Gap 仍只有一个，但表示当前公开证据下最可能限制下一阶段稳健 progression 的主要瓶颈，不自动等于当前最低数值。来源可包括 review feedback、晋升/未晋升结果、交付证据、career-capital imbalance、复利资产趋势和公开生存约束；证据不足时为 UNKNOWN。每个 local candidate 都须连回 Review Horizon objective；该 objective 再连回 Global Horizon。

## Promotion Frontier / Progression Readiness

Promotion Frontier 是对下一阶段 progression 可能受何种公开条件约束的定性诊断，不是隐藏 eligibility checker。只在 FULL checkpoint 维护紧凑的 current-session profile，基于 fresh public Level/promotion/review feedback、Skill、Output、Network、Wealth、Delivery evidence 与其它直接相关事实；QUICK 决策不必重述。

Profile 可包含：Level / review feedback、career-capital balance、likely progression bottleneck、相对领先且边际价值可能较低的维度、next observable progression evidence。证据不足时标 UNKNOWN。不得估算 promotion probability、threshold distance、hidden target 或 cap，也不将任何单一维度自动视为晋升条件。

## Delivery lifecycle integration

Planning 读取 Delivery Skill 的当前 session compact summary，只用于判断机会、承诺、交付、证据和公开 review 联系是否改变 Primary Gap 或候选比较。Planning 拥有策略与 Primary Gap；不创建、覆盖或补全 Delivery 状态。申请/活动/口头完成/一般表扬不自动等于交付、验证或 recognition。缺失的公开回执保持 UNKNOWN。

只有 Delivery 中的公开承诺、checkpoint、阻塞、结果或 review 证据实质改变当前 objective / gap 时，才触发相应的 Full checkpoint；无关 lifecycle 更新只做 quick scan，不展开长分析。

## Cross-dimension bottleneck 与 global marginal value

若某 career-capital dimension 已相对相关维度明显领先，而 review、progression 或 delivery evidence 指向另一处约束，不因领先维度仍能增长就默认继续投资。比较应关注新增长对 Review Horizon 与 Global Horizon 的边际贡献，而不是追平数值或套用比例。

支持这种判断的公开信号可包括：formal feedback 反复指向同一短板；领先维度继续局部增长但未伴随 progression outcome 改善；或 delivery / recognition chain 显示瓶颈在另一环节。不得只因不同维度的数值大小不同就推断 bottleneck。

GLOBAL_MARGINAL_VALUE_LOW 仅是 Path Trade-off 中可使用的语义描述：某路径仍可能带来局部增长，但对当前 progression frontier / global objective 的贡献较低。它不作为持久 enum 或 telemetry，不要求 STALLED，也不能由单次小幅变化推出。STALLED 仍仅表示相同 action/gap 在两个相邻 comparable checkpoints 均无目标进展；两者判断对象不同。

Risk Budget 是候选无关的当前约束状态，只由 fresh public facts 支持：AVAILABLE 表示未观察到当前 material survival constraint 收紧预算；TIGHT 表示观察到该约束正在收紧可接受风险预算；UNKNOWN 表示证据过期、缺失或不清。Planning 不在候选生成前评估具体候选的 Material Risk；先生成候选，再由 Risk 做 candidate-specific gate。不得用数值阈值或隐藏库存定义这些语义。

公开 survival trend 也是候选无关 Risk Budget 的输入。fresh public evidence shows a binding survival trend when Health is visibly low or repeatedly declining across comparable fresh observations; or when another public survival-relevant dimension (Dignity / Network / Wealth / formal feedback) shows sustained deterioration together with a credible public survival warning/consequence. Recent shock direction and a realistically reachable recovery opportunity affect how strongly to protect the buffer. Do not use numeric thresholds, hidden streak counters, fixed recovery quotas, or treat one isolated small delta as a universal trigger.

当 Risk Budget=TIGHT 是由直接相关的公开 survival trend 导致时，应暂缓或拒绝会直接加重该约束的非必要 Growth，直到 fresh public evidence 显示 buffer 已有足够恢复。这不等于禁止所有 Growth；不加重该约束的 Growth 仍可比较，并由 Risk gate 具体候选。

安全是约束，不是默认优化目标。Risk Budget AVAILABLE 且无 Material Risk 时，普通 Soft Cost 本身不能自动否决对当前 gap 有更强公开贡献的合法 Growth path。TIGHT 只约束与公开生存风险直接相关的候选；UNKNOWN 不得伪装成安全。

### Explicit affordability evidence

Fresh public evidence of debt, inability to pay, an affordability crisis, or a severe financial warning may immediately make affordability a binding survival/resource constraint and tighten the candidate-independent Risk Budget. Credible sustained financial deterioration with a public consequence can also matter without waiting for an arbitrary checkpoint count. Do not use a fixed Wealth cutoff: an ordinary cost, small spend, or isolated Wealth decrease alone does not make the budget TIGHT. Planning owns the budget; Risk still gates each concrete candidate.

### Early-horizon progression bias

当剩余职业轨迹较长、Risk Budget=AVAILABLE，且公开状态未显示 binding compliance constraint 时，提高能推进 Promotion Frontier、可见交付或受约束 career-capital dimension 的合法 Growth path 的相对优先级，因为它可能留下更长的复利窗口。Planning 不预判 candidate-specific Material Risk；每个候选仍须通过最终 Risk gate，公开重大风险优先。这是随公开剩余 horizon 调整的策略偏置，不是固定月份规则或每步必选 Growth。

## Full checkpoint 与 review reset

以下触发 full checkpoint：

- new game/session baseline；
- 当季首次 Energy 决策前；
- 已知半年 review 前最后一个可行动窗口的轻量 reserve check；
- 实际观察到 formal review / feedback / promotion / public no-advance result；
- 与当前 Primary Gap 相关、且实质改变目标或结果解释的 Delivery evidence / blocker；
- strict STALLED；
- context recovery；

同时发生的触发合并为一个 checkpoint。普通 derived label 变化不得递归触发 full checkpoint。无需 FOUNDATION / PROMOTION / COMPOUNDING / FINAL_SPRINT 或 promotion-readiness enum；若 phase/mode 名称不改变当前选择，不输出。

压缩/恢复后以 fresh public state 重建 Planning；不得把框架生成的 state snapshot 当作策略权威。持久 instruction 负责将压缩快照识别为 recovery epoch 并重读四份 Skill；Delivery 只从当前 session 公开证据恢复 lifecycle，证据不全时保持 UNKNOWN。

单独的 material fresh public-state change 只触发 Board refresh 与 Planning quick scan；按需更新 Risk Budget / Primary Gap，不自动打开 full checkpoint。若同时满足上述 canonical trigger，合并处理；不得因派生状态或 gap 更新递归触发 checkpoint。

实际观察到 promotion、formal review/feedback 或公开 no-advance result 后：

- 刷新 Board facts；
- 使旧 Progress comparison 失效；
- 刷新 Promotion Frontier / Progression Readiness；
- 判断 likely bottleneck 是否改变；
- 以 fresh evidence 建立新 baseline；
- 重新选择 / 保留 / UNKNOWN 一个 Primary Gap；

多个 full-checkpoint trigger 同时发生时合并为一次 rebuild；不得由 Agent 另行输出 checkpoint marker。只有满足下述双 checkpoint 条件才可写 STALLED。

不得从 silence 推断 review 结果、延续旧 Level 的 Progress baseline，或估算 promotion probability / hidden threshold。

## Checkpoint output

完整 checkpoint 最多 6 字段：

    Horizon
    Promotion Frontier
    Primary Gap
    Progress / Recent Effect
    Risk Budget
    Path Trade-off

Path Trade-off 最多两个合法路径，不复制 Board 快照或 transcript。季度首次 Energy checkpoint 必须 jointly compare Energy 与 Main complementarity；quarterly policy 只保留：one gap、直接相关 survival constraint、Energy/Main 互补、重复投资前检查 fresh observed effect 与该路径的 global marginal value。

在已知半年 review 前最后一个可行动窗口，检查 fresh survival facts、warning、剩余 story exposure 与可验证 recovery opportunity；不依赖 review 后的 Energy 挽救已发生的伤害。

## Candidate comparison 与 anti-myopia

每个合法候选须简短回答：它如何服务当前 Review Horizon objective、推进 Promotion Frontier / 当前 Primary Gap，并贡献于 Global Horizon？比较 progression relevance、公开交付/结果价值、复利价值、global marginal value、horizon fit、可逆性、资源/机会成本、依赖负担与当前生存约束；candidate-specific Material Risk 留给 Risk 最终 gate。该比较是语义判断，不是隐藏权重或数值加权公式。

避免局部指标持续增长却不推进整体 progression、无 binding risk 时因普通 Soft Cost 放弃高价值 Growth、反复做活动却缺少交付/证据/recognition，以及永久保守。若候选局部有收益但其 global marginal value 已低，应明确比较其它公开 bottleneck 与 review objective。只在相同目标和可比 checkpoint 下按现有 STALLED 规则复核无进展；不设置固定季度行动比例、固定 Energy bundle 或月份晋升 KPI。

## Progress / STALLED

只用 Primary Gap 本身或直接相关的公开 career progress；表扬、菜单描述或不可比状态不足以判定 ADVANCING。

- advertised effect 是菜单先验；同局可靠 comparable observed effect 优先。
- 同一 strategic action、同一 Primary Gap、两个相邻 comparable checkpoints 均无 observed target progress，才标 STALLED。
- action/gap/target 改变、state stale、story/event 污染、来源不清或 before/after 不可比时标 UNKNOWN；不得把一次无增长判为 STALLED。
- STALLED 后只比较一个不同类型的合法 alternative；switch 不强制。有新证据说明旧 path 仍适用时可继续。

## Energy、Main 与 story

Energy 与 Main 按当前 gap 联合规划，但每个 state-changing action 后都要 fresh observe、Board scan、Planning quick scan，再决定下一项；不得复用旧 scan。不能编码 fixed bundle、menu catalog 或固定赢家。

普通非战略 story 只对少量最相关合法候选做一次有界比较；无 fresh public evidence 不重开，除非 Risk 返回 RECONSIDER 并按其合同复核一个直接相关合法 alternative。没有事件标题答案、action lookup 或固定 primitive ranking。

DECISION_CLOSED：最终候选完成最终 Risk gate 后，若没有新的 fresh observe、tool result、event content 或其它公开证据，Planning 立即结束比较并交接已 gate 候选；不重开路径或重新讨论标记。只有新公开证据才重新打开。

## 权限与边界

- Planning 只给 Single Agent 有界建议；Can Submit Action: No。不得调用 new_game、observe 或 take_action。
- 不建立 durable/cross-game Memory，不创建第二审查者、Agent、Team 或 Swarm；不使用 hidden thresholds、evaluator weights 或 Dev 公式。
- session、month、state、effect 或 option 不 fresh / 不可比时标 UNKNOWN，回正常流程取得 fresh public evidence。
