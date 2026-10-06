---
name: structured-state-board
description: 在新局、季度规划、重大状态变化或上下文恢复时维护同一游戏 session 的稀疏公开事实缓存；不规划、不提交动作。
---

# Structured State Board｜稀疏事实缓存

## 职责与刷新时机

只回答“当前有哪些已确认的公开事实、来源是否新鲜、哪些关键项仍未知”。不回答应该做什么，不解释风险，不拥有目标或策略。

仅在以下时机建立或刷新：

1. 新局首次有效 `observe` 后；
2. 每季度 Planning checkpoint 前；
3. 新鲜公开重大后果/状态变化导致需要重新规划时；
4. continuation/context loss 恢复时；
5. session 不匹配、Board 缺失、失效或含糊时。

普通月度事件和每次动作回执不自动触发完整 Board 刷新。

## 证据与格式

只使用当前 CareerSim 游戏 session 的公开 `observe`、已确认动作回执，以及上下文恢复所需的同局公开信息。JiuwenSwarm conversation ID 不是游戏 session ID。fresh observe 优先；动作前后字段无法直接比较、可能被中间事件污染或来源不清时，写 `UNKNOWN` 或省略，不推断因果。

在当前 conversation 中维护精简替换快照：

```text
game_session_id: <已确认的 CareerSim session ID>
game_time_or_phase: <公开值 / UNKNOWN>
facts:
  - <当前决策相关的公开事实> [source: fresh observe / confirmed result; time: <公开时间>]
unknown:
  - <影响决策但无法由公开证据确认的事项>
recent_effects: # 最多两条；无则 []
  - action: <已确认的合法动作>
    target_or_relevant_field: <公开字段/目标>
    before_after: <直接可比的公开变化 / UNKNOWN>
    source: <confirmed result / fresh observe / bounded same-session recovery>
source_or_freshness: <最新权威 observe 与公开游戏时间>
```

只保留当前决策需要的事实；不建长期 `inferred` 列表，不累积 transcript。`recent_effects` 最多两条，只记录直接确认的事实，不评价、不推荐、不认领 Primary Gap。

上下文丢失时，先确认同一游戏 session 并获取 fresh observe。只有确需恢复 Board/Planning 或最近效果时，才查看同一 session 最近最多五条公开日志；最多恢复两条可直接确认的 recent effect。session 不符即丢弃旧缓存。不得读隐藏计数、数据库、其他对局、本机取证材料或持久化 Memory。

## 权限与回退

- Board 只整理事实与新鲜度；`rolling-planning` 负责解释进展、目标和路径，`risk-review` 负责当前候选的重大风险。
- 不调用 `new_game`、`observe` 或 `take_action`，不改选项或动作记录；Can Submit Action: No。
- session 或来源无法确认时，保留 `UNKNOWN`，由正常流程获取 fresh observe 后重建。Board 不阻断决策，也不跨局继承。
