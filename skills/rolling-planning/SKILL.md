---
name: rolling-planning
description: Use at every quarterly first Energy decision to refresh or create a fresh public-evidence Planning checkpoint; reread this Skill for initial detailed setup, material feedback/consequences, continuation/context loss, stale or ambiguous checkpoints, or when its procedure cannot be reconstructed; compare repeated actions with observed effects, apply a bounded risk budget and 48-month horizon, and never submit actions.
---

# Rolling Planning

## Purpose

Set a short priority and medium objective from fresh public evidence; not an agent, action policy, memory system or score predictor.

## When to use

- After a new game's first valid observation, read this Skill for detailed initial planning and set the initial priority.
- At each quarter's first Energy decision, use fresh public state to refresh or create that quarter's checkpoint before choosing Energy. A new quarter alone does not require a full Skill reread.
- Reuse that checkpoint for the same-quarter main action unless material feedback or a material public-state change occurs.
- Re-read this Skill and rebuild from fresh public observation after semiannual feedback, a severe public warning/consequence, continuation/context loss, stale or ambiguous checkpoint semantics, or when the detailed procedure cannot be reliably reconstructed.

Do not invoke for every monthly story. HR praise, no new warning, accepted action or submitted mitigation alone does not resolve risk or trigger material reprioritization. Normal growth without material risk needs no extra Risk review or conservative default.

## Input and evidence rules

Use only the confirmed current game session, latest authoritative public `observe`, same-session board if available, confirmed action results, and available public handbook rules. Separate observed facts, inferences, and unknowns.

Never use another run, post-outcome facts not yet visible, raw database, hidden counters/thresholds, or evaluator weights. Sequence alone does not prove causation.

## Planning procedure

1. At each quarter's first Energy decision, refresh or create a checkpoint from fresh public `observe` before choosing Energy; a new quarter or missing current-quarter checkpoint alone does not require rereading this Skill. Reuse it for the same-quarter main action unless material feedback/state changes. Apply the conditional reread triggers listed above.
2. Use only the confirmed game session and fresh Board/observe. After continuation/context loss, confirm the game session and rebuild from fresh public state; an unverifiable prior objective has `UNKNOWN` progress. Never inherit it from Memory or guesswork.
3. Maintain exactly one `Primary Gap`: a public career/resource gap or evidenced progression stall. No balanced-growth default or fixed priority. Set one observable objective to the next quarterly/semiannual review; promise no promotion, score, or event outcome. At quarterly Energy, compare legal options' marginal public benefit for this gap against Energy/opportunity cost; saturation of one component neither discredits nor proves a composite option best.
4. At strategic checkpoints label prior-objective progress `ADVANCING`, `STALLED`, or `UNKNOWN` from comparable fresh public evidence. `ADVANCING` requires observable improvement in the Primary Gap itself or direct public performance/progression evidence explicitly related to it. Praise, collaboration bonuses, ordinary positive feedback, relationship gains, or a one-off successful event are supporting signals only and cannot alone establish `ADVANCING`; without direct comparable Gap evidence use `UNKNOWN`, unless step 5 establishes `STALLED`. For repeated actions, treat advertised effects as hypotheses and prefer reliable same-session observed effects; ambiguous attribution, intervening causes, or no comparison means `UNKNOWN`.
5. Mark `STALLED` only after the same action for the same gap has no observed progress at two adjacent comparable checkpoints. Then compare a different-type legal alternative and its public benefit/opportunity cost. One miss never forces a switch; comparison is required, selection is not. The old action may continue for a changed gap or reliable benefit to that gap, with an explicit reason.
6. `Risk Budget`: `TIGHT` for fresh material health/trust/compliance/retaliation/survival risk; `AVAILABLE` only with no fresh material warning and visible relevant safety margin; otherwise `UNKNOWN`. Safety is a constraint, not the default objective. Ordinary soft costs (small Health/Dignity loss, time, friction, pressure) are opportunity costs, not automatic vetoes of high-upside growth. Compare public benefits, risks, and costs; invent no thresholds.
7. For ordinary choices, compare legal candidates in this order: material-risk gate; contribution to the current `Primary Gap`; useful secondary public benefits; `Soft Cost` / opportunity cost; unresolved `UNKNOWN`. Do not default to the most mature, safest, or least-offensive option, and do not assign fixed weights or a numeric score. When `Risk Budget = AVAILABLE`, no fresh material risk exists, one legal path has clearly stronger public-evidence-based upside for the `Primary Gap`, and its extra cost is mainly `Soft Cost`, prefer that higher-upside path. If Gap upside is similar or `UNKNOWN`, a lower-cost/lower-exposure path may win. A `TIGHT` budget permits material risk to outweigh growth upside; current-candidate risk review remains with `risk-review`.
8. Use only the public current month and 48-month horizon. As time shortens, prioritize legal paths with observable progress toward a stalled gap over remote/uncertain payoff. Infer no promotion month or hidden threshold.
9. For ordinary non-strategic story choices, compare at most the two strongest legal candidates once; without fresh evidence, reopen only on new public evidence or `risk-review=RECONSIDER`.
10. Severe warning/consequence, persistent retaliation/escalation, or major survival/trust cost that undermines the objective reopens `Primary Gap`. Compare legal continuation, de-escalation, transfer/exit/mitigation by public benefit/loss, exposure, cost, and `UNKNOWN`; mark unavailable choices. Principle, duty, or recent promotion is no proof of safety; conservative/reduced-exposure choices are no fixed answer. The same Agent decides.

## Output

Return a compact checkpoint of no more than six short lines:

- `Horizon`: public current month / 48-month horizon and next review point.
- `Primary Gap`: exactly one revisable, public-evidence-based objective.
- `Progress`: `ADVANCING`, `STALLED`, or `UNKNOWN`, with comparable evidence basis.
- `Recent Effect`: reliable same-session observed effect, or `UNKNOWN`.
- `Risk Budget`: `TIGHT`, `AVAILABLE`, or `UNKNOWN`.
- `Path Trade-off`: at most two legal paths; include marginal benefit and opportunity cost when relevant.

If no relevant choice is currently legal, mark it unavailable and wait for a legal decision point; do not invent one.

## Action authority and fallback

- **Can Submit Action: No.**
- Do not call `new_game`, `observe`, or `take_action`, or alter legal choices or action notes.
- The Single Agent alone submits actions and may adapt or reject this recommendation.
- If the session, state, or choices are stale or ambiguous, report the uncertainty and return to the normal loop for fresh public state. Never guess a game ID or block the normal decision process.
- Keep the checkpoint within the current drive conversation, scoped to this game session. Do not write files, global Memory, Skill state, Runner output, or emulator data; do not carry it into another game.
