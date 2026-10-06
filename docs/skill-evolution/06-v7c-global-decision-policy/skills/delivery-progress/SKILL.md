---
name: delivery-progress
description: "仅在当前 session 出现与当前职业目标相关的公开机会、承诺、里程碑、阻塞、交付回执或 review 证据时，更新有界生命周期摘要；不规划、不判风险、不提交动作。"
---

# Delivery Progress｜公开交付生命周期

## 职责与证据边界

只维护当前 game session 中、仍与 Planning 的 Primary Gap 或 review objective 相关的公开交付 lifecycle：

`Opportunity → Commitment / Ownership → Delivery → Observable Evidence → Recognition / Review Impact`

这些阶段是公开证据标签，不是隐藏 simulator stage，也不要求每个项目按固定顺序经过每一阶段。只用 Board 的 fresh public facts、当前公开 event/receipt、当前 session compact lifecycle summary，以及相关 public feedback/review。不得读隐藏状态、数据库、其它 session、局后材料、Dev event catalog 或跨局记忆。

Planning 是唯一 strategy owner。Delivery 不选 Primary Gap、不排候选、不判断 Material Risk、不拥有 Risk Budget，也不提交 action。

## Trigger｜稀疏更新

仅当新公开证据可能改变当前生命周期或 review 解释时更新：

- 与当前 career objective 相关的新 opportunity；
- 明确的 commitment / ownership；
- 公开 milestone、dependency 或 blocker 的变化；
- delivery receipt 或 observable result；
- 与该 lifecycle 直接相关的 formal feedback / review / recognition。

没有相关新证据时做 QUICK no-op；如 Planning 请求，只返回现有活动项的短摘要，不重新分析或重述故事。事件标题、菜单描述和关键词本身不是 trigger 依据。

## 生命周期记录

每条 compact 记录按公开事实表达：

- `item`: 对公开目标/工作项的最短可识别摘要；
- `stage`: `OPPORTUNITY` / `COMMITTED` / `IN_PROGRESS` / `BLOCKED` / `DELIVERY_CLAIMED` / `DELIVERED` / `CLOSED`；
- `owner`、`dependency`、`next_checkpoint`、due window：只有公开明确提及时才填写；
- `evidence_status`: `UNKNOWN` / `UNVERIFIED` / `PUBLICLY_VERIFIED`，并保留对应公开 receipt 的简短摘要；
- `recognition_link`: 仅记录公开 feedback 明确连到该 item 的证据；否则 `UNKNOWN`。

阶段不代表完成证明。公开完成陈述但没有可核对结果时记 `DELIVERY_CLAIMED` + `UNVERIFIED`；receipt 直接验证结果时记 `DELIVERED` + `PUBLICLY_VERIFIED`。一般表扬、升职或 review 变化不能自动归因于某 item。证据没有说明负责人、日期或依赖时不补写，也不将“没有观察到”解释成“没有发生”。

## State Bound 与输出

仅保留最多 3 条 active lifecycle，以及最多 1 条与当前 review objective 直接相关的最近 closed evidence。每项限一条短记录，不累计 transcript。超出上限时保留最可能改变当前决策的明确承诺、近期 checkpoint 或活跃 blocker；省略项以后若重新相关，只能用当前 session 可恢复的公开证据重建，不能猜测中间状态。

输出格式保持紧凑：

`item | stage | public owner/dependency | next public checkpoint | evidence_status | recognition_link`

无新 trigger 时只报告 no-op 或相关现状。必要字段缺证据就写 `UNKNOWN / UNVERIFIED`，不展开长篇推理。

## 协作与恢复

- Board 拥有当前公开事实与来源；本 Skill 仅持有这些事实之间的 lifecycle 关系，不复制通用状态快照。
- Planning 读取 compact summary 决定它是否改变 objective、Primary Gap 或候选比较；Planning 不重写 lifecycle。
- Risk 仅在具体候选的公开 dependency 与 Material Risk 直接相关时读取相关摘要。缺少交付/回执本身不是风险。
- 当前 session 的 recovery epoch 必须先 fresh observe、确认相同 `game_session_id`，再从该 session 可见记录重建。snapshot、旧意图或跨局资料不能代替 receipt；不能重建的状态保留 UNKNOWN。

## 权限

- Can Submit Action: No。不得调用 `new_game`、`observe` 或 `take_action`；只消费正常流程已取得的公开事实与回执。
- 不创建 Agent、Team、Memory、事件答案表或第二个策略 owner。
