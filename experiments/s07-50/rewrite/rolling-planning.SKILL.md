---
name: rolling-planning
description: "After Board and Delivery are ready, maintain the review objective, classify current binding constraints, rank legal choices, and return one candidate."
---

# Rolling Planning

## Purpose and inputs

Own the review objective, Primary Gap, MODE, and candidate ranking. Consume the same-session Board, Delivery state, formal feedback, public legal choices, public Handbook, and confirmed receipts. The manifest owns the global evidence firewall; Risk alone owns the final risk result.

State:

```text
REVIEW_PLAN = <Objective | Primary Gap | Next Observable Checkpoint>
MODE = A | S
```

## Decision procedure

### Step 1 — Constraint gate

Ask whether current unresolved participant-visible evidence threatens physical/psychological safety, job continuity, trust/compliance/confidentiality continuity, or immediate affordability/income continuity.

- **YES:** set `BINDING_CONSTRAINT=YES`, `MODE=S`. An explicit acute warning controls even if displayed H/D/W values look adequate.
- **NO:** set `BINDING_CONSTRAINT=NO`, `MODE=A` and use normal progression ranking.

Ordinary workload, mild fatigue without an explicit acute warning, soft relationship friction, uncertainty, and opportunity cost alone answer NO. Return to A after fresh public evidence resolves the condition or ends the risk-bearing situation.

### Step 2 — Review plan

Before the first formal review, the Primary Gap may be unknown; pursue broad Skill/Network/Output progression and apply the existing evidence-gated pre-first-review result-realization prior. After formal feedback, anchor the gap to the clearest public deficit. Change the plan only on a review/promotion/no-advance, public completion, invalidated path, or infeasibility. An ordinary Story or transient fluctuation does not replace the gap. On recovery, rebuild from same-session public evidence; unrecoverable fields are `UNKNOWN`.

Evidence order for the plan: formal review/promotion/no-advance; fresh observed result; current public state/warning; Delivery evidence; advertised option hint. A lower-priority signal cannot override a contradictory higher-priority one. Public hints remain soft; do not infer thresholds or caps.

### Step 3 — Rank candidates

- In **S**, contain or resolve the constraint at the smallest reasonable opportunity cost while preserving progression.
- In **A**, keep the existing promotion-first order: current review gap; visible delivery relevant to the next checkpoint; broad Skill/Network/Output gains; long-horizon option value. Accept ordinary soft costs when progression is materially stronger.
- Before the first review only, prefer a legal action that can realize a current-session evidenced result over a generic workload push when the existing prior's conditions hold. This prior expires at the first formal review or when its result/commitment is verified, invalidated, blocked, or displaced by a binding constraint.
- For Energy, set one `QUARTER_INTENT` at the first Energy choice of each quarter. Replan remaining Energy only after material new evidence.

### Step 4 — Close and output

For one fresh observe, set MODE and plan once; remove unacceptable/dominated options, retain at most two competitive candidates, compare once, and emit exactly one candidate. Do not reopen on unchanged evidence. Risk may reopen selection only after `RECONSIDER`, once, for one directly relevant alternative; submit only after the selected candidate's final Risk result and valid CTRL closure. Recovery semantics remain the manifest's responsibility.

## Boundary examples

- Ordinary deadline pressure plus mild tiredness: `BINDING_CONSTRAINT=NO`, `MODE=A`.
- Explicit unresolved acute symptoms: `BINDING_CONSTRAINT=YES`, `MODE=S`, regardless of an adequate displayed Health value.
- Fresh public evidence says the acute condition resolved: it no longer forces S; classify current evidence normally.
- A formal review asks for clearer results and an unrelated Story follows: retain the review gap.

## Output

```text
PLAN: G=<gap|?> P=<A|S|?> checkpoint=<short checkpoint>
CANDIDATE: choice=<one legal integer> reason=<one concise public-evidence reason>
```

## Invariants

- Promotion-first strategy and the existing result-realization prior are preserved; this Skill does not invent a score formula or fixed event answer.
- Planning selects; Delivery verifies lifecycle evidence; Risk reviews the final candidate.
- Can Submit Action: No. Do not call `new_game`, `observe`, or `take_action`.
