---
name: rolling-planning
description: "每次 fresh Board/Delivery 后应用；晋升优先、广义成长与 ownership，最小必要保护；维护 Review Plan，比较当前合法候选，不提交动作。"
---

# Rolling Planning｜晋升优先与广义成长

## Objective / State

Maximize long-horizon progression while preserving a survival floor.

判断与输出用中文；以下策略条款同样约束中文判断。

```text
REVIEW_PLAN = <Objective | Primary Gap | Next Observable Checkpoint>
MODE = A | S
```

`A=Advance` 默认；`S=Stabilize` 仅用于当前重大公开生存/资源约束。Single Agent 执行；Planning 唯一拥有目标与排序。

## Evidence / Recovery interface

只消费同 session fresh Board、Delivery、当前 participant-visible event description 与 legal choice semantics、公开 Handbook、正式反馈与已确认公开结果。`HiddenRisk`、hidden counters、internal score、internal event id/effect、public-status-unclear fields 一律 `EXCLUDE_FROM_STRATEGY until verified public`。禁止跨局记忆、hidden/private/Dev evidence、隐藏阈值/公式、事件答案映射。

先判断 fresh binding constraint，再以正式 Review/promotion/no-advance → fresh observed result → 当前 public state/warning → Delivery → advertised effect/hint 更新计划；低优先级不能覆盖明确冲突。

`RECOVERY=NONE|PROGRESSION|RESOURCE|RISK|DELIVERY|UNKNOWN` 仅作现有接口标签，不新增排序树：绩效不足是 A 下调整方向；重大资源约束才 S；公开 warning 或交付修复由相应公开证据支持，完成后回主线。Risk 只 gate 最终候选，Delivery 只报告 lifecycle。明确 public warning 且有 reparative legal option 时可一次 bounded cleanup；fresh observe 后默认回主线，仅持续/再次/新的同类 warning 才允许再次 cleanup。

context recovery 由 executor 按 manifest 完成同 session fresh observe、四 Skills 重读、Board/Delivery 重建后恢复 `REVIEW_PLAN / RECOVERY`；缺失字段 UNKNOWN，未完成不排序。

## Maintain the Review Plan

- Before the first formal review, allow `Primary Gap=UNKNOWN`. Pursue visible delivery and broad Skill / Network / Output progression.
- After formal feedback, anchor the gap to the clearest public progression deficit.
- Revise the plan only when:
  - formal review / promotion / no-advance changes the evidence;
  - the objective is publicly completed;
  - fresh evidence invalidates the current gap/path; or
  - the current objective is no longer feasible.
- Do not change the gap because of an ordinary Story or one transient state fluctuation.

Review 是方向性反馈；gap 不构成硬 gating tree，也不取消其它更强 ownership、多维成长或可兑现结果。无未来公开 checkpoint 时只比较剩余 horizon 内可实现的价值，不虚构未来 Review。

## Select MODE

Before progression ranking, evaluate the current whitelisted Board and participant-visible event/choice semantics for an unresolved binding constraint. Do not inspect prohibited raw numeric fields, and do not use a numeric threshold.

A displayed H/D/W number or an ordinary one-step decrease alone does not establish a binding constraint and does not justify `MODE=S`. Use `MODE=S` only when current public evidence establishes a material survival, safety, job-continuity, affordability, or income-continuity constraint. A clearly depleted public resource may bind when public evidence establishes that normal activity is infeasible.

Set `MODE=S` while fresh public evidence shows a current, unresolved constraint that materially threatens survival, safety, or job continuity, including explicit acute physical symptoms, explicit psychological/safety danger, explicit job-continuity warning, an active trust/compliance/confidentiality crisis, or a direct affordability/income-continuity crisis. An acute symptom remains binding even if the displayed Health/Dignity/Wealth value appears adequate. Choose the smallest reasonable action that addresses or avoids worsening the binding condition while preserving progression where possible.

Return to `MODE=A` when fresh public evidence indicates that binding condition is resolved or the risk-bearing situation has ended. A numeric state change or unrelated positive feedback alone does not establish resolution. Ordinary workload, mild fatigue without an explicit material symptom/warning, soft relationship friction, generic uncertainty, and ordinary opportunity cost do not by themselves require `MODE=S`.

When no unresolved binding constraint is present, use `A` and continue promotion-first progression.

In `S`, keep the constraint visible in the current plan, remove or contain it with the smallest reasonable opportunity cost, and return to `A` once fresh public evidence resolves it.

Wealth stress is an income-recovery problem, not a reason for permanent low-profile play: avoid discretionary cost while continuing to repair performance, promotion, and income capacity.

每次 fresh observe 从 A 重新判断；旧 S/旧理由不续期，只有当前 fresh evidence 仍证明 unresolved material constraint 才重新 S。只做 minimum necessary protection；不为补满资源延长 S。poor grade / no-promotion / weak S/N/O 单独不触发 S。

## Rank legal candidates

### MODE=A

Prefer, in order:

1. direct progress on the current review gap;
2. visible delivery / ownership likely to matter at the next checkpoint;
3. options that publicly improve multiple progression dimensions among Skill / Network / Output;
4. long-horizon compounding and future option value.

Accept ordinary soft costs when the progression upside is materially stronger.

#### Pre-first-review result realization prior

Apply `PRE_FIRST_REVIEW_RESULT_REALIZATION_PRIOR` only before the first formal review, in `MODE=A` with no binding public survival/resource constraint. Require current-session whitelisted Board/Delivery evidence of an existing high-value commitment with a concrete public result/checkpoint opportunity (including work in progress or near completion), or `DELIVERY_CLAIMED + UNVERIFIED`; also require a legal action that can finish/validate it, present an actual result, or obtain a public receipt. Check `stage`, `evidence_status`, `recognition_link`, and `next_checkpoint`; a report-like menu label, pure information gathering, or a claim without an underlying result is insufficient.

When triggered, prefer that result-realization action over another generic workload push with no stronger current result evidence. Do not displace a clearly superior time-sensitive progression opportunity. If no such delivery basis exists, use the ordinary broad Skill / Network / Output ranking. If the result is already `DELIVERED + PUBLICLY_VERIFIED`, do not repeat a presentation merely to repackage it.

Exit this prior at the first formal review, when the result becomes publicly verified, when the commitment becomes invalid or blocked, or when a material constraint requires `MODE=S`. After formal review, its feedback-anchored `REVIEW_PLAN` owns the objective. This is neither a fixed report action nor a promotion threshold; do not infer hidden eligibility from it.

### MODE=S

Prefer candidates that:
1. do not worsen the binding constraint;
2. directly relieve it or protect job continuity;
3. preserve as much review/progression value as possible.

Do not convert `S` into permanent risk avoidance.

### Delivery constraint

If an active high-value commitment is near a public result, prefer finishing/validating it over opening a weaker speculative commitment. Do not block a clearly superior new opportunity merely because an old item exists.

## Public-hint / local response discipline

Treat statements such as “this may help performance/promotion” as soft evidence only.

Never convert them into:
- a confirmed hidden requirement;
- a hidden threshold/cap;
- a fixed optimal action.

If advertised gain is absent after a fresh observe, record `OBSERVED_NO_GAIN` or `OBSERVED_COST`; keep the cause `UNKNOWN`. Do not infer a cap or formula.

消费 Board `PROGRESSION_RESPONSE`：clean NO_GAIN 只折价已测试的当前 Level/context/dimension/action family；UNKNOWN 保持开放，多维动作保留其它维度及 ownership/结果价值。不把局部 NO_GAIN 传播给未测试 family，不推断全局 cap、eligibility 或恢复无成长机会成本。Level change 后依 Board 重置；存在 responsive alternative 时不立即重复同一路径。

## Quarterly control

`QUARTER_INTENT = <MODE | current target>` 仅当前目标，不预定剩余序列或配额。每次只选一个 Energy action；执行后由 executor fresh observe → Board（含 PROGRESSION_RESPONSE）→ Delivery → new Planning pass → final Risk → READY → preflight，再决定下一动作。receipt 不提供 public state；旧计划不能授权动作。

For the quarterly Main Action, apply the same ranking. When no material constraint exists, give a strong prior to broad-growth options that combine visible ownership with multiple public progression gains; this is a prior, not a fixed menu answer.

## Decision budget / output

`ONE FRESH OBSERVE = ONE PLANNING PASS`：确认 MODE/REVIEW_PLAN，删掉明显不可接受或被支配选项；最多两个 genuinely competitive candidates，比较一次，输出唯一 CANDIDATE。无 genuinely new public evidence 不重开。

Risk=RECONSIDER 仅允许一次直接相关替代项比较，再取得所选候选自己的最终 Risk；使用当前 CTRL `RB=NONE|DONE|BLOCKED`，最终仍 RECONSIDER/未闭合则 BLOCKED，不提交。UNKNOWN 最多一次 fresh observe/rebuild，仍不明则一次 bounded legal decision，不反复规划。executor 独占 CONTROL_STATE/READY/preflight。

只返回：

```text
PLAN: G=<gap|?> P=<A|S|?> F=<NONE|PROGRESSION|RESOURCE|RISK|DELIVERY|UNKNOWN> checkpoint=<short checkpoint>
CANDIDATE: choice=<one legal integer> reason=<one concise public-evidence reason>
```

**Can Submit Action: No.** 不调用 `new_game`、`observe` 或 `take_action`。
