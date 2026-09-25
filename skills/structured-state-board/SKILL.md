---
name: structured-state-board
description: 每次 fresh observe 后快速整理当前 session 的公开状态与趋势，并按需维护有界事实快照；不规划、不判断风险、不提交动作。
---

# Structured State Board｜公开状态快照

## 职责

只整理当前 CareerSim game session 中可核实的公开事实、来源新鲜度及可直接比较的近期变化。Board 不拥有 Phase、Survival band、Primary Gap、风险结论或动作建议；这些分别由 `rolling-planning` 与 `risk-review` 负责。JiuwenSwarm conversation ID 不等于 `game_session_id`。

## QUICK_SCAN｜每次 fresh observe

每次得到 fresh `observe` 后，快速读取并与最近的同局公开状态比较：

- 当前月份及下一个公开半年 review window；
- Health、Dignity、Network、Wealth、Level、Output、Skill；
- 最近公开 promotion / performance feedback 与明确 warning；
- 以上可比较字段的方向：`UP / DOWN / STABLE / UNKNOWN`，注明比较依据；
- 最近动作效果是否仍可直接归因、是否有中间事件或其它动作污染。

QUICK_SCAN 是供 `CONTROL_SCAN` 与当前决策使用的事实输入，不要求每次复述整份 Board。Board 不自行推断隐藏风险，不把时间相邻写成因果。

## FULL SNAPSHOT｜有条件刷新

新局、季度 checkpoint（首次 Energy 决策前）、半年 review 前、promotion / feedback 结果后、survival band 或 material public state 改变、Primary Gap 改变，或 context recovery 时，建立/替换一个精简快照：

```text
game_session_id: <已确认的 CareerSim session ID>
month / review_window: <公开值 / UNKNOWN>
public_state:
  Health: <值 / UNKNOWN>
  Dignity: <值 / UNKNOWN>
  Network: <值 / UNKNOWN>
  Wealth: <值 / UNKNOWN>
  Level: <值 / UNKNOWN>
  Output: <值 / UNKNOWN>
  Skill: <值 / UNKNOWN>
trends: <字段方向 + 可比较来源 / UNKNOWN>
recent_effects: # 最多两条；无则 []
  - action: <已确认的合法动作>
    target_or_relevant_field: <公开字段 / 目标>
    before_after: <直接可比的公开变化 / UNKNOWN>
    source: <confirmed result / fresh observe / bounded same-session recovery>
unknown: <影响当前判断但无法公开确认的事项>
freshness: <最近 authoritative observe 与公开月份>
```

完整快照保持有界，只替换当前事实，不累积 transcript。recent effects 最多两条；仅在前后状态可直接比较、且没有事件/其它动作污染时记具体 delta，否则写 `UNKNOWN` 或省略。Board 不评价效果、不推荐动作、不生成 Primary Gap。

## Context recovery

先确认相同 `game_session_id`，再取得 fresh observe。只有恢复 Board 或最近效果确有必要时，才查看同一 session 最近最多五条公开日志，并最多恢复两条可直接确认的 effect；session 不符、来源不清或状态过期时丢弃旧缓存并标 `UNKNOWN`。不读数据库、隐藏字段、其它对局或本机取证材料；不建立文件型 / durable Memory。

## 权限

- Board 只负责事实与 freshness；Planning 负责战略，Risk 负责候选风险。
- 不因 QUICK_SCAN 自动触发 FULL SNAPSHOT 或额外审查；material change / 明确 checkpoint 才刷新完整快照。
- Can Submit Action: No。不得调用 `new_game`、`observe` 或 `take_action`；只整理正常流程已取得的结果。
- 三 Skill 的高频功能使用不等于每步重新 `read_file(Skill)`；上下文丢失且规则无法恢复时才重读相关 Skill。
