---
name: rolling-planning
description: "Use for every CareerSim decision after the fresh Board is available. Maintain one review-window objective and progression gap, default to aggressive career advancement, switch to temporary stabilization only for material public survival constraints, rank current legal candidates, and return one final candidate without submitting it."
---

# Rolling Planning

## Objective

Maximize long-horizon progression while preserving a survival floor.

State:

```text
REVIEW_PLAN = <Objective | Primary Gap | Next Observable Checkpoint>
MODE = A | S
```

`A` = Advance. Default.<br>
`S` = Stabilize. Temporary response to a material public survival/resource constraint.

## Evidence order

Consume only the same-session whitelisted public Board and Delivery summary, formal feedback, public legal choices, Handbook, and confirmed public receipts/logs. Ignore `HiddenRisk`, hidden counters, internal score components, internal event identifiers/effects, and public-status-unclear fields even when present in a tool payload; never use numeric internal-looking values in the Review Plan, candidate reason, CTRL notes, or action rationale. `EXCLUDE_FROM_STRATEGY until verified public`.

Use evidence in this order:

1. formal review / promotion / no-advance;
2. fresh observed action result;
3. current public state and explicit warning;
4. Delivery evidence;
5. advertised option effect or public hint.

A lower-priority signal must not override a contradictory higher-priority signal.

After context recovery and the required same-session fresh observe and four-Skill reread, restore `REVIEW_PLAN` from current-session public formal feedback and whitelisted Board/Delivery evidence. Set any unrecoverable Objective, Primary Gap, or Next Observable Checkpoint to `UNKNOWN`; do not reuse a stale plan or rank an action before recovery completes.

## Maintain the Review Plan

- Before the first formal review, allow `Primary Gap=UNKNOWN`. Pursue visible delivery and broad Skill / Network / Output progression.
- After formal feedback, anchor the gap to the clearest public progression deficit.
- Revise the plan only when:
  - formal review / promotion / no-advance changes the evidence;
  - the objective is publicly completed;
  - fresh evidence invalidates the current gap/path; or
  - the current objective is no longer feasible.
- Do not change the gap because of an ordinary Story or one transient state fluctuation.

## Select MODE

Use `A` unless fresh public evidence shows a material constraint.

Switch to `S` only for a current constraint such as:
- severe Health/Dignity deterioration or explicit warning;
- depleted/deteriorating Wealth with affordability or income pressure;
- explicit job-continuity, compliance, confidentiality, safety, or trust danger.

In `S`, remove the immediate danger with the smallest reasonable opportunity cost, then return to `A` once the constraint is relieved.

Wealth stress is an income-recovery problem, not a reason for permanent low-profile play: avoid discretionary cost while continuing to repair performance, promotion, and income capacity.

## Rank legal candidates

### MODE=A

Prefer, in order:

1. direct progress on the current review gap;
2. visible delivery / ownership likely to matter at the next checkpoint;
3. options that publicly improve multiple progression dimensions among Skill / Network / Output;
4. long-horizon compounding and future option value.

Accept ordinary soft costs when the progression upside is materially stronger.

### MODE=S

Prefer candidates that:
1. do not worsen the binding constraint;
2. directly relieve it or protect job continuity;
3. preserve as much review/progression value as possible.

Do not convert `S` into permanent risk avoidance.

### Delivery constraint

If an active high-value commitment is near a public result, prefer finishing/validating it over opening a weaker speculative commitment. Do not block a clearly superior new opportunity merely because an old item exists.

## Public-hint discipline

Treat statements such as “this may help performance/promotion” as soft evidence only.

Never convert them into:
- a confirmed hidden requirement;
- a hidden threshold/cap;
- a fixed optimal action.

If advertised gain is absent after a fresh observe, record `OBSERVED_NO_GAIN` or `OBSERVED_COST`; keep the cause `UNKNOWN`. Do not infer a cap or formula.

## Story stop rule

- Eliminate clearly dominated or clearly unacceptable options.
- Compare only the small set that remains genuinely competitive.
- Stop when one candidate is clearly preferred under `MODE + REVIEW_PLAN`.
- Do not reopen the same decision without new public evidence.

## Quarterly control

At the first Energy decision of a quarter, set:

```text
QUARTER_INTENT = <MODE | target | intended use of remaining Energy>
```

Submit Energy one integer at a time. After each action, fresh observe. Replan the remaining Energy only after material new evidence.

For the quarterly Main Action, apply the same ranking. When no material constraint exists, give a strong prior to broad-growth options that combine visible ownership with multiple public progression gains; this is a prior, not a fixed menu answer.

## Output

Return only:

```text
PLAN: G=<gap|?> P=<A|S|?> checkpoint=<short checkpoint>
CANDIDATE: choice=<one legal integer> reason=<one concise evidence-based reason>
```

Do not call `new_game`, `observe`, or `take_action`. Can Submit Action: No.
