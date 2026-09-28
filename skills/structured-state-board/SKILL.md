---
name: structured-state-board
description: "每次 fresh observe 后整理当前 session 的公开事实、正式反馈和仍未解除的生存风险方向；不做策略、不猜隐藏阈值、不提交动作。"
---

# Structured State Board｜公开事实板

Board 只负责把当前局里已经公开的事实整理清楚，不决定下一步做什么。

## Fresh state

每次 fresh observe 后确认：

- `game_session_id`
- 当前月份、季度、Level、公开的职级停留月份
- Health、Dignity、Skill、Network、Output、Wealth、Energy
- 最近一次 formal performance / promotion / no-advance
- 当前公开 warning
- 当前事件和合法选项

运行时如果公开字段名是 `duration_in_level`，就按它原样记录；如果是 `CurrentLevelDuration` 也同样记录。缺失或冲突时写 `UNKNOWN`，不自己反推。

before/after 只有在同一 session、单一动作、没有中间事件污染时才做直接归因。否则写 `UNKNOWN`。

## Sticky facts

下面这些公开事实即使这个月没有变化，只要 fresh evidence 还没有显示它已经解除，就继续显式保留：

- Wealth 已经很低、非正，或持续恶化；
- 明确 affordability / payment / income warning；
- Health 或 Dignity 明显恶化，或者有明确身体、心理、组织 warning；
- formal performance 为 C/D、no-advance 或其它明确负面反馈；
- Network 长期明显走弱或出现孤立 warning；
- 已公开出现的事故、爆雷、信任、合规、保密或安全 warning。

这些只说明“当前公开风险还在”，不等于知道失败阈值、累计次数或隐藏计数。

## Formal progression evidence

正式绩效、晋升和未晋升是长期规划最重要的公开证据，Board 必须保留：

- review 月份
- performance grade
- feedback 原意的短摘要
- promotion / no-advance
- 当时的 Level、Skill、Network、Output、Wealth

只保留最近两个 review checkpoint，避免无限累计。

## Recent effects

最多保留两条对下一次决策最有用、而且可以直接归因的公开结果：

`action / path → observed gain / no-gain / cost`

不能确认原因时只写 observed result，不解释成隐藏机制。

## Recovery

发生上下文恢复时：

1. 确认同一 `game_session_id`；
2. fresh observe；
3. 重建当前公开状态和 Sticky facts；
4. 必要时只查看同一 session 的少量最近公开日志；
5. 无法恢复的 review/effect 写 `UNKNOWN`。

旧 snapshot、旧意图、其它对局和局后分析都没有当前事实权威。

不读数据库、不读隐藏字段、不使用其它 game session，不建立跨局 Memory。

Can Submit Action: No。不得调用 `new_game`、`observe` 或 `take_action`。
