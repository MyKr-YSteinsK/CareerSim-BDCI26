---
name: delivery-progress
description: "Use after every fresh public Board. 维护当前 session 中与 Review 相关的最多三个 delivery items，记录 commitment、进行中、blocked、claimed、verified 与 recognition 证据；只管理交付生命周期，不决定目标、不排序动作、不评估风险、不提交动作。"
---

# Delivery Progress｜交付进展

## 职责

本 Skill 只回答：

> 当前 Review 相关的公开工作项做到哪一步、下一 checkpoint 是什么、结果是否已经被公开验证。

第一次正式 Review 前若尚无有效 `REVIEW_PLAN`，使用当前公开 commitment、近期 checkpoint 与明显交付相关性判断 item 是否值得跟踪。第一次正式 Review 后，以最新仍有效的 `REVIEW_PLAN` 为主要相关性依据。

Delivery 不等待 Planning 重新计算，也不自行发明 Objective / `Primary Gap`。

职责边界：

- Board：公开事实；
- Planning：Objective / `Primary Gap` / candidate ranking；
- Risk：final candidate risk gate；
- Delivery：当前 session 的 delivery lifecycle。

## Lifecycle

```text
OPPORTUNITY -> COMMITTED -> IN_PROGRESS -> DELIVERY_CLAIMED -> DELIVERED -> CLOSED
                 \-> BLOCKED -> IN_PROGRESS / DELIVERY_CLAIMED
```

这些是 evidence labels，不是 simulator hidden state，也不是强制顺序。

每项格式：

```text
<local_id> | <short public item> | stage | owner/dependency | next_checkpoint | proof_basis | evidence_status | recognition_link
```

`evidence_status`：

- `UNKNOWN`
- `UNVERIFIED`
- `PUBLICLY_VERIFIED`

## Identity

`local_id=D1,D2,...` 只在当前 game session 内使用。

1. fresh session 从 `D1` 开始。
2. 每个 distinct public work item 使用新 ID。
3. 同局已用 ID 不复用，即使 item 已 retired。
4. 维护 `NEXT_ID`。
5. 只有确认 session 改变才重置。
6. recovery 后若 ID/cursor 无法可靠恢复，写 `UNKNOWN`；不得猜测或复用 uncertain ID。

## 更新规则

只在 fresh public evidence 改变以下内容时更新：

- opportunity relevance；
- commitment / ownership；
- milestone / blocker；
- delivery result；
- 与 item 明确关联的正式 Review / recognition。

### 结果验证

- `DELIVERY_CLAIMED + UNVERIFIED`：声称完成，但公开证据尚未验证真实结果。
- `DELIVERED + PUBLICLY_VERIFIED`：当前 session 的 participant-visible evidence 明确验证真实结果或 milestone。

成功的 MCP / `take_action` receipt 只证明工具执行，不证明 career result。

generic praise、普通 promotion/review、成功沟通、action receipt、未来承诺都不能单独验证交付。

`recognition_link=1` 仅在公开证据明确把 recognition 与该 item 的结果关联时使用；否则 `0` 或 `?`。

## 与 Review / Recovery 的关系

如果高价值 active item 接近公开 checkpoint：

- Planning 可以把完成或验证它作为 `RECOVERY=DELIVERY` 或普通 Advance 路径；
- 本 Skill 只报告 lifecycle，不决定是否继续投入。

context recovery 后，只恢复 fresh same-session public evidence 能支持的 item。无法恢复的 stage / proof / recognition 写 `UNKNOWN`。

## Bound

保留：

- 最多 3 个 active items；
- 最多 1 个与当前 Review objective 直接相关的 recent closed item。

active item 必须仍有公开证据支持 unresolved commitment、work in progress、blocker、near checkpoint 或 review linkage。

超过 active limit 时，仅按当前决策相关性保留：明确 commitment、near checkpoint、active blocker、verified review linkage。不要为了降低 `n` 人为删除真实 active item。

## 输出

每次 fresh Board 后输出当前完整 bounded Delivery state，并给最相关 item 一个 marker：

```text
[DL i=<NONE|D#|UNKNOWN> n=<0-3> focus=<NONE|OPPORTUNITY|COMMITTED|IN_PROGRESS|BLOCKED|DELIVERY_CLAIMED|DELIVERED|UNKNOWN> evidence=<NA|UNKNOWN|UNVERIFIED|PUBLICLY_VERIFIED> checkpoint=<NEAR|NOT_NEAR|UNKNOWN> recognition=<0|1|?>]
```

`checkpoint=NEAR` 需要公开证据表明该 item 与当前 Review Window 或 commitment 的 near-term checkpoint 相关；`NOT_NEAR` 表示没有此类公开依据；证据不足时用 `UNKNOWN`。不得用数字倒计时推导 near status。

- `n` = active item 数量；
- `i` 必须映射到当前 Delivery state 中唯一 item；
- recent `CLOSED` item 不计入 `n`，也不能成为 action-note focus；
- `n=0` 时使用 `i=NONE focus=NONE evidence=NA checkpoint=NOT_NEAR recognition=0`。

marker 只记录现有 Delivery evidence，不自动改变 Planning ranking。

## 不变量

- current-session public evidence only。
- 不使用 hidden state、其它 game 或 durable cross-game memory。
- 不等待 Planning 重新计算才能维护已存在 lifecycle；但绝不自行创建 Objective / `Primary Gap`。
- **Can Submit Action: No.**
- 不调用 `new_game`、`observe` 或 `take_action`。
