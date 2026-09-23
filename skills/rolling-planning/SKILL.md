---
name: rolling-planning
description: Use at a new game's first observation, quarterly resource and main-action decisions, and material performance/state feedback to maintain one compact, revisable public-evidence-based career priority; never submit actions.
---

# Rolling Planning

## Purpose

Translate fresh public CareerSim state into one short-horizon priority and one medium-horizon objective. This Skill adds a bounded planning checkpoint to the existing Single Agent loop; it is not a new agent, action policy, persistent memory system, or score predictor.

## When to use

- After the first valid observation of a new game session, establish the initial priority.
- Before quarterly Energy allocation and the quarterly main action, compare the current public state and legal choices with the active priority.
- After a semiannual performance result or another material public outcome that changes the plan.
- When a previously repeated strategic action has not produced an observed improvement in its intended public state.

Do not invoke this Skill for every monthly story choice. Use it only at these strategic checkpoints or when a material outcome invalidates the active plan.

## Input and evidence rules

Use only the current game's confirmed session ID, the latest public `observe`, the same-session `structured-state-board` when available, confirmed action results, and public handbook rules already available to the Agent. Treat the latest `observe` as authoritative. Keep observed facts, inferences, and unknowns separate.

Do not use another run's transcript, score report, raw database, hidden counters, inferred thresholds, or unpublished evaluator weights. Do not assume an action caused an outcome merely because it preceded that outcome.

## Planning procedure

1. Check that the state and board belong to the current game session; if not, discard stale context and continue with the normal loop's fresh public observation.
2. Identify the most decision-relevant public constraint or gap, considering visible performance feedback, level progression, Skill, Network, Output, Wealth, Health, Dignity, Energy, and active public risks. Use only public facts and do not assume a fixed priority order.
3. Keep one objective through the next quarterly or semiannual review, whichever is the relevant horizon. Prefer an observable objective such as producing a clear deliverable, developing a needed capability, strengthening a relevant relationship, or protecting a threatened resource. Do not promise a promotion, score, or event outcome.
4. At a quarterly choice, compare only currently legal options. Briefly state how the leading option supports the objective and what it trades off; retain the Single Agent's final judgment, especially when immediate survival and growth conflict.
5. After material feedback, compare the plan with the newly observed result and revise if the evidence warrants it. If a repeated action has not produced the intended observed progress, reconsider the alternatives rather than repeating it by default; repetition may still be chosen when its current evidence supports it.
6. Keep the plan concise and replace the prior checkpoint instead of accumulating history.

## Output

Return a compact checkpoint, normally no more than five short lines:

- `Horizon`: next quarter or next semiannual review.
- `Observed gap`: the relevant public fact(s), or `unknown`.
- `Priority`: one revisable objective.
- `Choice trade-off`: at most two currently legal candidates when a quarterly choice is available.
- `Review trigger`: the next feedback or public state change that should prompt revision.

For a non-quarterly material feedback event, omit `Choice trade-off` if no relevant strategic choice is currently legal.

## Action authority and fallback

- **Can Submit Action: No.**
- This Skill does not call `new_game`, `observe`, or `take_action`, and does not alter legal choices or action notes.
- The existing Single Agent remains the only action submitter and may accept, adapt, or reject the planning recommendation.
- If the session, state, or choices are stale or ambiguous, report the uncertainty and return to the normal loop for fresh public state. Never guess a game ID or block the normal decision process.
- Keep the checkpoint within the current drive conversation, scoped to this game session. Do not write files, global Memory, Skill state, Runner output, or emulator data; do not carry it into another game.
