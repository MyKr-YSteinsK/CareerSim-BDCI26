---
name: structured-state-board
description: "Use after every fresh observe and during same-session recovery to normalize public state, formal review evidence, unresolved failure-direction signals, and up to two attributable recent effects. Facts only: do not plan, infer hidden rules, assess risk, or submit actions."
---

# Structured State Board

## Contract

Input:
- latest fresh `observe`;
- confirmed result of the immediately preceding action;
- same-session public logs only when recovery requires them.

Output one compact replacement board:

```text
SESSION: <game_session_id> | M=<month> Q=<quarter>
STATE: H=<Health> D=<Dignity> S=<Skill> N=<Network> O=<Output> W=<Wealth> L=<Level> E=<Energy>
TENURE: <public field/value | UNKNOWN>
REVIEW: <latest formal grade/feedback/promotion/no-advance | none>
PROGRESSION_RESPONSE:
  S=<GAIN|NO_GAIN|UNKNOWN>
  N=<GAIN|NO_GAIN|UNKNOWN>
  O=<GAIN|NO_GAIN|UNKNOWN>
  LEVEL=<current Level>
STICKY: <unresolved public warning(s) | none>
EFFECTS: <up to 2 attributable recent effects | none>
UNKNOWN: <decision-relevant unresolved facts | none>
```

## Procedure

1. Verify `game_session_id` and freshness. Discard stale or cross-session context.
2. Construct a public evidence view before returning facts to Planning or Risk. Copy `Health`, `Dignity`, `Skill`, `Network`, `Output`, `Wealth`, `Level`, and `Energy` directly from the latest fresh participant-visible `current_state.status`; copy public time and `duration_in_level` from that observation. Preserve each reported value and precision. If a field is missing or its public status is unclear, write `UNKNOWN`.
3. Never calculate, round, predict, reconcile, or replace a `STATE` value using salary/bonus text, events, advertised effects, previous observations, or action notes. Keep relevant public salary or event information as a separate fact; wait for a fresh observation to update `STATE`.
4. Preserve the latest formal review, promotion, or no-advance evidence.
5. Keep a public fact in `STICKY` only while fresh evidence shows an unresolved material warning, condition, or continuity problem, including:
   - an affordability / income-continuity crisis;
   - an explicit material Health or Dignity warning;
   - an explicit participant-visible material dismissal or job-continuity threat;
   - sustained Network isolation or an explicit isolation warning;
   - an accident, trust, compliance, confidentiality, or safety warning;
   - a clearly depleted public resource when public evidence establishes that normal activity is infeasible.
   A poor grade, no-advance result, or ordinary performance deficit alone stays in `REVIEW` as a Planning progression problem; it does not create binding `STICKY` state. Performance evidence enters `STICKY` only when participant-visible feedback explicitly states a material dismissal or job-continuity threat.
   A numeric fluctuation or ordinary one-step decline alone remains a `STATE` observation; it does not create a binding `STICKY` warning.
6. An explicit current acute physical or psychological symptom, or material safety warning, is decision-relevant and must enter `STICKY` even when numeric status appears adequate. Keep it unresolved until fresh public evidence explicitly indicates resolution or the risk-bearing situation has ended. Ordinary fatigue, workload, uncertainty, or mild soft cost alone does not create a binding warning.
7. Keep at most the last two formal review checkpoints.
8. Maintain `PROGRESSION_RESPONSE` independently for Skill (`S`), Network (`N`), and Output (`O`) at the current public Level. If the session or Level changed, reset all three responses to `UNKNOWN`. Otherwise carry forward each untouched dimension from the preceding same-session Board. For each dimension explicitly advertised as a positive change by the immediately preceding confirmed legal action, compare the public value with its preceding observation: record `GAIN` if it increased and `NO_GAIN` if it stayed unchanged only when the fresh observe cleanly separates that action from salary, review, promotion, unrelated events, and intervening actions; otherwise record `UNKNOWN`. A later clean advertised gain overwrites `NO_GAIN`. Never infer a cap, threshold, formula, eligibility, or hidden cause.
9. Keep at most two recent effects. Attribute a state change only when one confirmed action is followed by a fresh observe and the public evidence separates its effect from other causes. A salary, bonus, review, promotion, unrelated event, or intervening action contaminates attribution; report `EFFECTS: UNKNOWN / MIXED` rather than assigning the combined delta to one action. `PROGRESSION_RESPONSE` is the compact long-lived current-Level carrier; keep `EFFECTS` bounded.
10. On recovery, verify the same session and rebuild this replacement Board from a fresh observe first; consult only a small amount of same-session public log history if required. Reconstruct progression responses only from bounded same-session public evidence; otherwise mark them `UNKNOWN`. Mark missing public review evidence `UNKNOWN`; do not carry a stale Board forward.

## Invariants

- Separate observed facts from `UNKNOWN`.
- Exclude `HiddenRisk`, hidden counters, internal score components, internal event identifiers/effects, and other non-public or public-status-unclear fields, even if a tool payload includes numeric `status_updates`. Never copy their values into the Board, CTRL notes, or action rationale; `EXCLUDE_FROM_STRATEGY until verified public`.
- Downstream Planning/Risk receive the whitelisted Board plus participant-visible event and legal-choice semantics only. When raw tool payloads also contain prohibited or public-status-unclear numeric fields, ignore them at source; never quote, compare, summarize, or reason from their values in visible reasoning, plan, candidate reason, Risk reason, CTRL, or DL.
- Do not infer thresholds, counters, caps, hidden risk, or causal rules.
- Do not use other games, database contents, or post-game forensic artifacts.
- Do not accumulate a transcript.
- Can Submit Action: No.
