---
name: rolling-planning
description: Use at every quarterly first Energy decision when its checkpoint is missing, and after material feedback, severe public consequences, continuation/context loss, or stale/missing planning state to re-read this Skill and rebuild one fresh public-evidence-based Primary Gap; compare repeated actions with observed effects, apply a bounded risk budget and 48-month horizon, and never submit actions.
---

# Rolling Planning

## Purpose

Set a short priority and medium objective from fresh public evidence; not an agent, action policy, memory system or score predictor.

## When to use

- After a new game's first valid observation, set the initial priority.
- Before the first quarterly Energy decision, verify that a current-quarter checkpoint exists; if missing or unverifiable, re-read this Skill and create one from fresh public observation before choosing Energy.
- Reuse that checkpoint for the same-quarter main action unless material feedback or a material public-state change occurs.
- After semiannual feedback, a severe public warning/consequence, continuation/context loss, or any missing, stale, or mismatched checkpoint, re-read this Skill and rebuild from fresh public observation.

Do not invoke for every monthly story. HR praise, no new warning, accepted action or submitted mitigation alone does not resolve risk or trigger material reprioritization. Normal growth without material risk needs no extra Risk review or conservative default.

## Input and evidence rules

Use only the confirmed current game session, latest authoritative public `observe`, same-session board if available, confirmed action results, and available public handbook rules. Separate observed facts, inferences, and unknowns.

Never use another run, post-outcome facts not yet visible, raw database, hidden counters/thresholds, or evaluator weights. Sequence alone does not prove causation.

## Planning procedure

1. At each quarter's first Energy decision, if no verifiable checkpoint exists for that quarter, re-read this Skill and build one from fresh public `observe` before choosing Energy. Reuse it for the same-quarter main action unless material feedback/state changes. Re-read and rebuild after semiannual feedback, severe warning/consequence, context loss, or a missing/stale checkpoint.
2. Use only the confirmed game session and fresh Board/observe. After context loss, an unverifiable prior objective has `UNKNOWN` progress; never inherit it from memory or guesswork.
3. Maintain exactly one `Primary Gap`: a public career/resource gap or evidenced progression stall. No balanced-growth default or fixed priority. Set one observable objective to the next quarterly/semiannual review; promise no promotion, score, or event outcome. At quarterly Energy, compare legal options' marginal public benefit for this gap against Energy/opportunity cost; saturation of one component neither discredits nor proves a composite option best.
4. At strategic checkpoints label prior-objective progress `ADVANCING`, `STALLED`, or `UNKNOWN` from comparable fresh public evidence. For repeated actions, treat advertised effects as hypotheses and prefer reliable same-session observed effects; ambiguous attribution, intervening causes, or no comparison means `UNKNOWN`.
5. Mark `STALLED` only after the same action for the same gap has no observed progress at two adjacent comparable checkpoints. Then compare a different-type legal alternative and its public benefit/opportunity cost. One miss never forces a switch; comparison is required, selection is not. The old action may continue for a changed gap or reliable benefit to that gap, with an explicit reason.
6. `Risk Budget`: `TIGHT` for fresh material health/trust/compliance/retaliation/survival risk; `AVAILABLE` only with no fresh material warning and visible relevant safety margin; otherwise `UNKNOWN`. Safety is a constraint, not the default objective. Ordinary soft costs (small Health/Dignity loss, time, friction, pressure) are opportunity costs, not automatic vetoes of high-upside growth. Compare public benefits, risks, and costs; invent no thresholds.
7. Use only the public current month and 48-month horizon. As time shortens, prioritize legal paths with observable progress toward a stalled gap over remote/uncertain payoff. Infer no promotion month or hidden threshold.
8. For ordinary non-strategic story choices, compare at most the two strongest legal candidates once; without fresh evidence, reopen only on new public evidence or `risk-review=RECONSIDER`.
9. Severe warning/consequence, persistent retaliation/escalation, or major survival/trust cost that undermines the objective reopens `Primary Gap`. Compare legal continuation, de-escalation, transfer/exit/mitigation by public benefit/loss, exposure, cost, and `UNKNOWN`; mark unavailable choices. Principle, duty, or recent promotion is no proof of safety; conservative/reduced-exposure choices are no fixed answer. The same Agent decides.

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
