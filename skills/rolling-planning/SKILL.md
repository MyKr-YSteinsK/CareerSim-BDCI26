---
name: rolling-planning
description: "每次决策必须应用；唯一战略 owner，维护公开 Primary Gap、Progress、含公开 survival trend 的 Risk Budget 与必要 checkpoint；不提交动作。"
---

# Rolling Planning｜公开证据滚动规划

## 职责与快速扫描

Planning 是唯一战略 owner。每次决策基于当前 session 的 fresh public facts 与 Board 事实做短 scan：survival constraint、一个 Primary Gap、Progress、remaining realizable horizon。动作改变状态后，先 fresh observe 并更新事实；不得用变更前 scan 决定下一 Energy/Main action。take_action.notes 的唯一控制前缀由 persistent instruction 生成；Planning 不复制标记格式或提交动作。

只使用当前 game_session 的 fresh public evidence、Board 可核实事实与公开 Handbook。不得使用其它对局、局后信息、hidden threshold、evaluator weight 或 Dev 内部公式。

## Planning state

每次决策维护：

- 一个公开 Primary Gap，或证据不足时 UNKNOWN；
- Progress = ADVANCING / STALLED / UNKNOWN；
- Risk Budget = AVAILABLE / TIGHT / UNKNOWN；
- Horizon：公开剩余时间与仍可实现的收益窗口。

Risk Budget 是候选无关的当前约束状态，只由 fresh public facts 支持：AVAILABLE 表示未观察到当前 material survival constraint 收紧预算；TIGHT 表示观察到该约束正在收紧可接受风险预算；UNKNOWN 表示证据过期、缺失或不清。Planning 不在候选生成前评估具体候选的 Material Risk；先生成候选，再由 Risk 做 candidate-specific gate。不得用数值阈值或隐藏库存定义这些语义。

公开 survival trend 也是候选无关 Risk Budget 的输入。fresh public evidence shows a binding survival trend when Health is visibly low or repeatedly declining across comparable fresh observations; or when another public survival-relevant dimension (Dignity / Network / Wealth / formal feedback) shows sustained deterioration together with a credible public survival warning/consequence. Recent shock direction and a realistically reachable recovery opportunity affect how strongly to protect the buffer. Do not use numeric thresholds, hidden streak counters, fixed recovery quotas, or treat one isolated small delta as a universal trigger.

当 Risk Budget=TIGHT 是由直接相关的公开 survival trend 导致时，应暂缓或拒绝会直接加重该约束的非必要 Growth，直到 fresh public evidence 显示 buffer 已有足够恢复。这不等于禁止所有 Growth；不加重该约束的 Growth 仍可比较，并由 Risk gate 具体候选。

安全是约束，不是默认优化目标。Risk Budget AVAILABLE 且无 Material Risk 时，普通 Soft Cost 本身不能自动否决对当前 gap 有更强公开贡献的合法 Growth path。TIGHT 只约束与公开生存风险直接相关的候选；UNKNOWN 不得伪装成安全。

## Full checkpoint 与 review reset

以下触发 full checkpoint：

- new game/session baseline；
- 当季首次 Energy 决策前；
- 已知半年 review 前最后一个可行动窗口的轻量 reserve check；
- 实际观察到 formal review / feedback / promotion / public no-advance result；
- strict STALLED；
- context recovery；

同时发生的触发合并为一个 checkpoint。普通 derived label 变化不得递归触发 full checkpoint。无需 FOUNDATION / PROMOTION / COMPOUNDING / FINAL_SPRINT 或 promotion-readiness enum；若 phase/mode 名称不改变当前选择，不输出。

压缩/恢复后以 fresh public state 重建 Planning；不得把框架生成的 state snapshot 当作策略权威。持久 instruction 负责将压缩快照识别为 recovery epoch 并重读三份 Skill。

单独的 material fresh public-state change 只触发 Board refresh 与 Planning quick scan；按需更新 Risk Budget / Primary Gap，不自动打开 full checkpoint。若同时满足上述 canonical trigger，合并处理；不得因派生状态或 gap 更新递归触发 checkpoint。

实际观察到 promotion、formal review/feedback 或公开 no-advance result 后：

- 刷新 Board facts；
- 使旧 Progress comparison 失效；
- 以 fresh evidence 建立新 baseline；
- 重新选择 / 保留 / UNKNOWN 一个 Primary Gap；

多个 full-checkpoint trigger 同时发生时合并为一次 rebuild；不得由 Agent 另行输出 checkpoint marker。只有满足下述双 checkpoint 条件才可写 STALLED。

不得从 silence 推断 review 结果、延续旧 Level 的 Progress baseline，或估算 promotion probability / hidden threshold。

## Checkpoint output

完整 checkpoint 最多 6 字段：

    Horizon
    Primary Gap
    Progress
    Recent Effect
    Risk Budget
    Path Trade-off

Path Trade-off 最多两个合法路径，不复制 Board 快照或 transcript。季度首次 Energy checkpoint 必须 jointly compare Energy 与 Main complementarity；quarterly policy 只保留：one gap、直接相关 survival constraint、Energy/Main 互补、重复投资前检查新鲜 observed effect / saturation。

在已知半年 review 前最后一个可行动窗口，检查 fresh survival facts、warning、剩余 story exposure 与可验证 recovery opportunity；不依赖 review 后的 Energy 挽救已发生的伤害。

## Progress / STALLED

只用 Primary Gap 本身或直接相关的公开 career progress；表扬、菜单描述或不可比状态不足以判定 ADVANCING。

- advertised effect 是菜单先验；同局可靠 comparable observed effect 优先。
- 同一 strategic action、同一 Primary Gap、两个相邻 comparable checkpoints 均无 observed target progress，才标 STALLED。
- action/gap/target 改变、state stale、story/event 污染、来源不清或 before/after 不可比时标 UNKNOWN；不得把一次无增长判为 STALLED。
- STALLED 后只比较一个不同类型的合法 alternative；switch 不强制。有新证据说明旧 path 仍适用时可继续。

## Energy、Main 与 story

Energy 与 Main 按当前 gap 联合规划，但每个 state-changing action 后都要 fresh observe、Board scan、Planning quick scan，再决定下一项；不得复用旧 scan。不能编码 fixed bundle、menu catalog 或固定赢家。

普通非战略 story 最多比较两个最强合法候选一次。无新证据不重开，除非 Risk 返回 RECONSIDER。没有事件标题答案、action lookup 或固定 primitive ranking。

DECISION_CLOSED：最终候选完成最终 Risk gate 后，若没有新的 fresh observe、tool result、event content 或其它公开证据，Planning 立即结束比较并交接已 gate 候选；不重开路径或重新讨论标记。只有新公开证据才重新打开。

## 权限与边界

- Planning 只给 Single Agent 有界建议；Can Submit Action: No。不得调用 new_game、observe 或 take_action。
- 不建立 durable/cross-game Memory，不创建第二审查者、Agent、Team 或 Swarm；不使用 hidden thresholds、evaluator weights 或 Dev 公式。
- session、month、state、effect 或 option 不 fresh / 不可比时标 UNKNOWN，回正常流程取得 fresh public evidence。
