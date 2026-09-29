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

First select `MODE` against current binding public survival/resource constraints. The following order interprets progression evidence for `REVIEW_PLAN`; older progression feedback cannot override a current material Health/Dignity/Wealth/job/trust/compliance/safety constraint:

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

## Same-observation decision budget

ONE FRESH OBSERVE = ONE PLANNING PASS. In that pass, set `MODE + REVIEW_PLAN`, eliminate clearly unacceptable or dominated legal options, retain at most two genuinely competitive options, compare them once using the ranking below, and emit exactly one final `CANDIDATE`. Keep the comparison sufficient for a difficult choice but the output concise; do not narrate self-dialogue or cycle through candidates.

After emitting `CANDIDATE`, Planning is closed for this observation. `PASS`, `ALLOW`, or `WARN` from Risk closes the decision immediately. Only Risk=`RECONSIDER` may reopen selection once per fresh evidence state: compare at most one directly relevant legal alternative, select once, and obtain that selected candidate's own final Risk result. CTRL `R` records that final result, not the initial `RECONSIDER`; set `X=1` when this one branch completed, or `X=-` when no branch was used. If the selected candidate's gate again returns `RECONSIDER`, the path is incomplete (`X=0`): do not search another alternative or submit until genuinely new public evidence arrives. `UNKNOWN` does not authorize a new Planning pass: normal public flow may resolve it through at most one fresh observe/rebuild cycle, with a new pass only on genuinely new evidence; otherwise choose once from available public evidence with `R=UNKNOWN` and `X=-` or `X=1` according to branch use. A new thought about unchanged evidence never reopens Planning; only a new observe, action receipt, or formal feedback with genuinely new public evidence can start a new pass. Do not submit before closure; `X=0` forbids submission.

## Select MODE

Before progression ranking, evaluate the current whitelisted Board and participant-visible event/choice semantics for an unresolved binding constraint. Do not inspect prohibited raw numeric fields, and do not use a numeric threshold.

Set `MODE=S` while fresh public evidence shows a current, unresolved constraint that materially threatens survival, safety, or job continuity, including explicit acute physical symptoms, explicit psychological/safety danger, explicit job-continuity warning, an active trust/compliance/confidentiality crisis, or a direct affordability/income-continuity crisis. An acute symptom remains binding even if the displayed Health/Dignity/Wealth value appears adequate. Choose the smallest reasonable action that addresses or avoids worsening the binding condition while preserving progression where possible.

Return to `MODE=A` when fresh public evidence indicates that binding condition is resolved or the risk-bearing situation has ended. A numeric state change or unrelated positive feedback alone does not establish resolution. Ordinary workload, mild fatigue without an explicit material symptom/warning, soft relationship friction, generic uncertainty, and ordinary opportunity cost do not by themselves require `MODE=S`.

When no unresolved binding constraint is present, use `A` and continue promotion-first progression.

In `S`, keep the constraint visible in the current plan, remove or contain it with the smallest reasonable opportunity cost, and return to `A` once fresh public evidence resolves it.

Wealth stress is an income-recovery problem, not a reason for permanent low-profile play: avoid discretionary cost while continuing to repair performance, promotion, and income capacity.

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
