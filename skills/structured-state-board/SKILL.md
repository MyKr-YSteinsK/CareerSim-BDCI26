---
name: structured-state-board
description: "每次 fresh observe 后必须应用；只整理当前 session 的公开事实、freshness 与可归因变化；不规划、不判风险、不提交动作。"
---

# Structured State Board｜公开事实

## 职责与边界

Board 只整理当前 CareerSim game session 可核实的公开事实、来源/freshness 和可直接比较的变化。conversation ID 不等于 game_session_id。Board 不拥有 Phase/Mode、Risk Budget、Primary Gap、Progress/STALLED、风险结论、review reset 或动作建议；Planning 负责策略，Risk 负责当前候选。

## QUICK_SCAN｜每次 fresh state

每次正常流程取得 fresh public state 后：

- 确认当前 game_session_id、月份和公开 review window；
- 读取 Health、Dignity、Network、Wealth、Level、Output、Skill 七项当前值；
- 核对最近公开 formal feedback / review result / promotion result 与明确 warning；
- 对可比较字段标记方向与来源；稳定事实不必重复叙述，只突出 changed / relevant / unknown；
- 判断近期 before/after 是否被事件、其它动作、过期状态或不明来源污染；不能直接归因时记 UNKNOWN。

QUICK_SCAN 为 Planning 与当前决策供事实，不生成 CONTROL marker，也不复述整份快照。时间相邻不等于因果；不读取或推断 hidden state。

## 有界事实快照

只在以下情形建立或替换 compact full snapshot：

- new game/session；
- 当季首次 Energy planning point；
- 实际观察到的 formal review / feedback / promotion result；
- 可能改变当前事实判断的 material fresh public-state change；
- context recovery。

多个触发同时发生只做一个快照。快照只替换当前事实，不累积 transcript。保留最新 formal feedback / review result / promotion result 及其公开来源、月份和 freshness。

recent_effects 最多两条，仅记录同一 session 内、来源明确且没有中间事件/其它动作污染的公开 before/after。只记录可直接归因的字段变化；否则写 UNKNOWN 或省略。Board 不评价效果，也不把 observed change 自动称为 strategy success。

## Context recovery

若当前上下文含 framework 生成的 <state_snapshot>，视为 context-recovery epoch；snapshot 只是工作上下文，不是策略权威。先确认相同 game_session_id 并取得 fresh public state，再据此重建当前 Board。只有恢复事实确有必要时，才查看同一 session 最近最多五条公开日志，且最多恢复两条可直接确认的 effect。session 不符、来源不清或状态过期时丢弃旧事实并标 UNKNOWN。fresh state 优先于日志。

不读数据库、隐藏字段、其它对局或本机取证材料；不建立文件型 / durable Memory。

## 权限

- Can Submit Action: No。不得调用 new_game、observe 或 take_action，只整理正常流程已取得的状态与结果。
- 不因 QUICK_SCAN 自动触发 full snapshot；derived Planning label 变化不是 Board trigger。
- Skill 功能使用不要求每步重读完整文件；上下文规则无法恢复时，只重读必要规则。
