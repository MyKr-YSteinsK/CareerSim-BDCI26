# Agent Runtime Contract｜运行时总合同

## 1. 优先级

本合同面向运行模型与 Codex。优先级：

`执行语义正确 > 无冲突 > 关键规则显著 > Token 成本 > 人类可读性`

中文用于 CareerSim 自然语言判断；以下 machine-facing tokens 固定英文，不翻译：

`MODE / REVIEW_PLAN / RECOVERY / PROGRESSION_RESPONSE / GAIN / NO_GAIN / UNKNOWN / PASS / ALLOW / WARN / RECONSIDER / CONTROL_STATE / READY / OBSERVE_REQUIRED / BLOCKED / PREFLIGHT / CTRL / RB / NONE / DONE / NEAR / NOT_NEAR / RECOVERY_PENDING / RECOVERY_READY`

关键规则允许在 manifest 与所属 Skill 中重复，用于 compression 后保留和显著性强化；重复不得产生不同触发条件、不同 owner 或不同退出规则。

## 2. 架构

### S10-08 branch-only topology exception

S10-08 明确授权的 `candidate-v14-experience-routed-policy` 是三 Skill 静态实验：core 接管局内公开事实 capsule/交付证据/一次全菜单比较，atlas 仅路由局部 reference，guard 仅筛查当前 material constraint；Single Agent 仍唯一提交者。以下四 Skill 图及 CTRL/DL 格式描述 frozen v8a/历史候选，不要求 v14 启动读取已替换的四份正文或输出旧开发 marker。v14 使用 fresh capsule；语义约束（same-session、公开证据、合法且可负担 choice、READY→preflight→一个 action→OBSERVE_REQUIRED→fresh observe、未知副作用 BLOCKED、可见上下文恢复及整局持续）保留。guard 尚未加载且无 material danger 时不新增一次形式性 Risk 调用。只改变知识 owner/表示与暴露时机，不改 Runner、工具或 recovery 授权；后续 live 仍需 Task 明列预算。该例外不是 Main 验收或官方 fallback 替换。详见 [S10-08 review](reviews/S10-08_EXPERIENCE_ROUTED_POLICY_STATIC_REVIEW.md)。

```text
fresh observe
  → structured-state-board
  → delivery-progress
  → rolling-planning
  → risk-review
  → CONTROL_STATE=READY
  → preflight
  → PREFLIGHT=PASS
  → exactly one take_action
  → CONTROL_STATE=OBSERVE_REQUIRED
  → fresh observe
```

### Executor Control State

The executor owns `CONTROL_STATE=READY|OBSERVE_REQUIRED|BLOCKED`; no Skill may declare `READY` on its behalf.

- `READY` is established after a same-session fresh observe, rebuilt Board and Delivery, one new Planning pass, and final Risk. Preflight is not part of `READY` creation.
- Preflight consumes that existing `READY`. It checks the same `game_session_id`, one legal integer choice, and Board/Delivery/Planning/final Risk from the same fresh observe; final `R!=RECONSIDER`; CTRL `RB in {NONE,DONE}`; and valid CTRL/DL markers.
- On success, `PREFLIGHT=PASS` authorizes exactly one submission of the current choice. It does not create `READY` or a reusable authorization. Any failed check sets `BLOCKED` and forbids `take_action`.
- A successful `take_action` consumes the `READY` decision and one-use preflight, then sets `OBSERVE_REQUIRED`. Its `{success,error}` receipt has no fresh public state and cannot update Board/Delivery, return `READY`, or authorize another action.
- While `OBSERVE_REQUIRED`, reuse no candidate or prior state and submit no action. The only next gameplay call is a same-session fresh `observe`.
- After that observe, rebuild Board (including current-Level `PROGRESSION_RESPONSE`), Delivery, Planning, and final Risk; then establish `READY`. Only afterward may a new preflight run.
- Failed/unknown action outcome, failed observe, session mismatch, or preflight failure sets `BLOCKED`. Submit no action; use only the existing bounded same-session recovery contract.
- `RECOVERY_PENDING` keeps the state blocked. `RECOVERY_READY` alone authorizes no action; restart with a same-session fresh observe, rebuild Board/Delivery/Planning/final Risk, establish `READY`, then run a new preflight.

`RB=BLOCKED` always forbids submission.

Single Agent 是唯一 action submitter。

四个 Skill：

| Skill | 唯一 owner | 明确禁止 |
|---|---|---|
| Board | public facts、Review、STICKY、PROGRESSION_RESPONSE | planning、risk gate、submit |
| Delivery | current-session delivery lifecycle | Objective/Gap、candidate ranking、risk gate、submit |
| Planning | long horizon、Review Window、failure recovery、candidate ranking | 修改事实、提交 |
| Risk | final candidate risk gate | 重做长期规划、提交 |

## 3. Evidence

只用 current-session participant-visible public evidence。

`HiddenRisk`、hidden counters、internal scores、internal event ids/effects、public-status-unclear numeric fields：`EXCLUDE_FROM_STRATEGY`。

任何 Skill 都不得根据 unavailable/hidden evidence 推断 threshold、cap、weight、eligibility、failure probability 或固定最优 action。

## 4. Long Horizon

默认主线：

`SURVIVE → PROMOTE → COMPOUND`

正式 Review 是长期控制 checkpoint。坏局面只能暂时改变短期路径，不得无依据覆盖长期主线。

poor grade / no-promotion 属于 progression failure；本身不等于 survival crisis。

## 5. Failure Recovery

统一分类：

- `PROGRESSION`：MODE=A，修复绩效/晋升 gap；
- `RESOURCE`：明确重大 Health/Dignity/Wealth/continuity 约束时 MODE=S，最小必要稳定化；
- `RISK`：明确 public warning 时 bounded cleanup；只有升级为 material crisis 才可能 S；
- `DELIVERY`：修复 near-checkpoint commitment/result，不自动 S；
- `UNKNOWN`：证据不足，不猜测。

任何 recovery 必须有退出条件。`MODE=S` 解除 binding constraint 后立即退出。

若明确的 job-continuity threat 本身由绩效或交付失败造成，直接修复绩效、完成关键交付或恢复晋升成长可以是 `MODE=S` 下最直接的 constraint-relief action；不得把 `S` 机械理解为低调、停止成长或选择最保守动作。

## 6. Progression Response

Board 维护当前 Level 的 `S/N/O = GAIN|NO_GAIN|UNKNOWN`。

Planning 使用这些事实做 marginal routing：

- `NO_GAIN` 只折价该维度；
- 不立即重复无增益路径；
- 多维 action 保留其它维度价值；
- Level change 后全部重置；
- 不推断 cap。

## 7. Decision Budget

`ONE FRESH OBSERVE = ONE PLANNING PASS`

Planning 最多比较两个 genuinely competitive candidates。Risk 只有一次 bounded `RECONSIDER` 分支。没有 genuinely new public evidence 不得重新规划。

Quarterly Energy is strictly sequential: each cycle selects one Energy action, takes it only after Risk/preflight, obtains a same-session fresh observe, rebuilds Board and `PROGRESSION_RESPONSE`, updates Delivery, and runs a new Planning pass for remaining Energy. The prior remaining-action sequence is discarded; it never authorizes a batch.

## 8. Whole-game Persistence

active game 必须持续执行。一次 action closure 不是 assistant execution terminal。

自然结束只认 structured `game.ended`；技术终止必须有明确 runtime/tool failure。

## 9. Context Recovery

只有 observable recovery signal 才触发 recovery。顺序固定：

`same session → fresh observe → reread 4 Skills → rebuild Board → rebuild Delivery → restore Planning → RECOVERY_READY → fresh observe → rebuild Board/Delivery/Planning/final Risk → READY → new preflight`

未完成时禁止 action。

## 10. 修改合同

后续 Candidate 若改变上述 owner、MODE 语义、failure taxonomy、evidence firewall、decision budget 或 action preflight，必须明确标为 behavior/architecture delta，不得以语言/格式重构名义静默修改。
