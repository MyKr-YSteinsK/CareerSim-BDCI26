---
name: structured-state-board
description: "After each fresh observation, normalize same-session public facts for downstream Skills. Copy state, preserve current warnings, and report only attributable effects."
---

# Structured State Board

## Purpose

Produce a compact, current-session public evidence view. Board owns fact normalization; it does not choose actions or assess risk.

## Inputs

Latest fresh `observe`, its `game_session_id`, the confirmed preceding action receipt, and a small amount of same-session public history only when recovery requires it.

## Procedure

1. Confirm the observation is fresh and belongs to the active session. Otherwise stop and mark the identity/status unknown.
2. **COPY STATE ONLY.** Copy `Health`, `Dignity`, `Skill`, `Network`, `Output`, `Wealth`, `Level`, and `Energy` from the latest participant-visible current state into H/D/S/N/O/W/L/E. Preserve the reported value and precision. Missing or unclear fields become `UNKNOWN`.
3. Keep salary, bonus, event text, and advertised effects as separate public facts when relevant. They never change the copied STATE.
4. Carry the latest formal review, promotion/no-advance, and unresolved material public warnings. Keep an explicit acute physical/psychological symptom or safety warning in `STICKY` until fresh public evidence says it resolved or the risk-bearing situation ended. Ordinary fatigue or workload alone is not a binding warning.
5. Attribute an effect only when one confirmed action is followed by a fresh observation and no salary, review, promotion, unrelated event, or other action contaminates the change. Otherwise report `UNKNOWN / MIXED`.
6. Return the replacement board in the output schema. Separate observed facts from unknowns.

## Output

```text
SESSION: <game_session_id> | M=<month> Q=<quarter>
STATE: H=<...> D=<...> S=<...> N=<...> O=<...> W=<...> L=<...> E=<...>
TENURE: <public value|UNKNOWN>
REVIEW: <latest public result|none|UNKNOWN>
STICKY: <unresolved public warning(s)|none>
EFFECTS: <attributable effect(s)|UNKNOWN / MIXED|none>
UNKNOWN: <decision-relevant unknowns|none>
```

## Boundary examples

- Fresh public state reports Wealth=4; separate public text announces a salary increase. Output W=4; do not calculate a replacement value.
- An action is followed by a salary or review event before the next comparable state. Attribute no precise single-action effect; use `UNKNOWN / MIXED`.
- Public evidence reports acute physical symptoms while numeric Health appears adequate. Keep the symptom in `STICKY`.

## Invariants

- Board STATE is mechanical extraction, not interpretation. Never infer, reconcile, round, average, or predict a current value.
- The runtime manifest owns the global evidence firewall. Normalize only participant-visible facts and exclude fields whose public status is unclear.
- Do not build a transcript or promote an ordinary soft cost into a warning without public evidence.

Can Submit Action: No.
