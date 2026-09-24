---
name: structured-state-board
description: Use within one CareerSim game session to keep a compact observed/inferred/unknown working board from fresh public observations and confirmed action results; never submit actions.
---

# Structured State Board

## Purpose

Keep one compact working board for the current CareerSim game so the same Agent can recover decision context during a long playthrough. This Skill organizes information already available to the Agent. It is not global memory, cross-game learning, a planner, a risk policy, a hidden-state estimator, or another action submitter.

## Trigger

Refresh the board:

- after a successful `new_game` and the first valid `observe`;
- when a fresh `observe` changes a material public state, event, warning, or legal choice;
- after a confirmed action result, using the next fresh `observe` to refresh current state;
- when continuing after context loss; or
- whenever the board is missing, stale, ambiguous, or for another game session.

Do not update for every token or log line. Keep only the current board and context needed for the current decision; do not accumulate an unlimited history.

## Input

Use only the current game's public information already obtained by the normal Agent loop:

- the CareerSim **game** `session_id` returned by `new_game` or confirmed by `observe`;
- the latest `observe` public `current_state`, current event/visible feedback, and legal choices;
- a confirmed `take_action` result; and
- no more than the five most recent public log entries for this same game session, only when needed after context loss to recover at most two relevant strategic action/effect pairs.

The JiuwenSwarm drive/conversation ID is not the game session key. Do not read hidden counters, guessed thresholds, secret/post-game fields, raw emulator databases, local forensic artifacts, or another game's board. A prediction or unconfirmed model guess is never an observed fact.

## Board format

Emit one concise replacement board in the current drive conversation. Include only fields relevant to the next decision:

```text
game_session_id: <confirmed CareerSim game session ID>
game_time_or_phase: <publicly observed value, or unknown>
observed:
  - <public fact or confirmed action result> [source: latest observe / action result; time: <visible game time>]
inferred:
  - <limited inference> [based on: <observed item>; confidence: <brief qualifier>]
unknown:
  - <decision-relevant fact that current public evidence cannot establish>
recent_effects: # at most two entries for this session; use [] when none
  - action: <confirmed public legal action>
    target_or_relevant_field: <public field/objective>
    before_after: <confirmed comparable delta or UNKNOWN>
    source: <confirmed result / immediate fresh observe / bounded same-session public log>
source_or_freshness: <latest authoritative observe and visible game time; note any bounded log used>
```

Keep `observed`, `inferred`, and `unknown` separate. A public warning may be recorded as observed; its severity, cause, likely consequence, or recommended response remains an inference or belongs to `risk-review`. Omit empty details or write `none`; never fill a field just to make the board look complete.

## Update and session rules

- A fresh authoritative `observe` takes precedence over an older board. A confirmed action result records only what the result confirms; a predicted effect stays inferred or unknown until observed.
- After continuation/context loss, first confirm the CareerSim `game_session_id` and obtain a fresh public `observe` through the normal Agent loop. Only if needed, inspect at most the five most recent public log entries for that same session, solely to recover up to two recent strategic action/effect pairs. Recover a pair only when the public evidence directly confirms the action and comparable before/after values; otherwise write `UNKNOWN` or omit it. Do not replay broader history or use logs for event-answer lookup.
- Keep at most two `recent_effects` for this game session. Record an effect only when the action is confirmed and the before/after public field is directly comparable using an immediate fresh `observe`, confirmed result, or the bounded same-session public logs allowed for context recovery. If an intervening event/action or another plausible public cause can explain the delta, record `UNKNOWN` or omit it; do not claim causation from sequence alone.
- `recent_effects` is an observed-fact surface, not an assessment: do not label effects good/bad, recommend actions, or own the `Primary Gap`. `rolling-planning` uses reliable comparable effects to assess progress; stale or ambiguous effects are `UNKNOWN`.
- Never let an inference overwrite or silently promote an observed item. Keep its basis explicit; remove or downgrade an inference when fresh evidence no longer supports it.
- Check `game_session_id` before reusing any board. On mismatch, discard the old board and start a clean one for the confirmed current game.
- A new game session always starts a clean board, even if the JiuwenSwarm conversation continues.
- If the game session ID is missing, evidence is stale/ambiguous, or the board is absent after context loss, mark unsupported details `unknown`. The same Agent obtains a fresh `observe` in its normal loop and rebuilds the board; only then may it use the bounded recovery above. Do not guess the session ID or carry the old board forward.
- Keep the board bounded to the current game snapshot and only the few prior public facts needed for the current decision. Do not create a running transcript or unlimited history.

## Normal decision loop and authority

This Skill only returns the board. It does not call `new_game`, `observe`, `take_action`, or advance a month/phase. If fresh state is needed, the same Agent gets it through the normal game loop.

```text
observe
→ structured-state-board refresh
→ normal candidate selection
→ risk-review when triggered
→ same Agent final decision
→ take_action
→ next fresh observe
→ board refresh
```

- **Can Submit Action: No.**
- The normal Single Agent remains the only `take_action` submitter and chooses the final legal action.
- Do not create another Agent, Team, Swarm, planner, or action submitter.
- `career-action-trace` retains its existing trace-marker behavior; this Skill adds no action marker and does not alter the chosen option or action notes.

## Persistence boundary

The board is bounded working context in the same JiuwenSwarm drive conversation. It is not durable storage. Do not write `MEMORY.md`, `projects/<drive ID>`, Skill files, Runner outputs, or the emulator database. Do not assume context compression preserves the board. After context loss, use the confirmed game session ID and fresh public `observe` to rebuild it. Never inherit a board across game sessions or claim cloud file persistence.

## Compatibility and fallback

- Risk meaning, severity, and action trade-offs stay with `risk-review`. This board may preserve the visible warning as observed and keep its interpretation separate as inferred.
- If evidence cannot support a board item, move it to `unknown` or omit it. If the game session cannot be confirmed, do not reuse a previous board.
- Missing, stale, mismatched, or ambiguous board state never authorizes a guessed action. The same Agent returns to its normal loop, refreshes public state, and makes the decision; bounded log recovery is only to restore facts for Planning's recent-effect/progress assessment, not to label progress or recommend an action. The board itself never blocks or submits an action.
