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
STICKY: <unresolved public warning(s) | none>
EFFECTS: <up to 2 attributable recent effects | none>
UNKNOWN: <decision-relevant unresolved facts | none>
```

## Procedure

1. Verify `game_session_id` and freshness. Discard stale or cross-session context.
2. Copy the current public state exactly. Record `CurrentLevelDuration` or `duration_in_level` only when participant-visible; otherwise `UNKNOWN`.
3. Preserve the latest formal review, promotion, or no-advance evidence.
4. Keep a public fact in `STICKY` until fresh evidence resolves it when it concerns:
   - depleted or deteriorating Wealth / affordability / income;
   - Health or Dignity deterioration or explicit warning;
   - negative formal performance or no-advance;
   - sustained Network isolation or explicit isolation warning;
   - accident, trust, compliance, confidentiality, or safety warning.
5. Keep at most the last two formal review checkpoints.
6. Keep at most two recent effects. Attribute an effect only when one action is followed by a fresh observe with no intervening event/action contamination.
7. On recovery, rebuild from fresh observe first; consult only a small amount of same-session public log history if required.

## Invariants

- Separate observed facts from `UNKNOWN`.
- Do not infer thresholds, counters, caps, hidden risk, or causal rules.
- Do not use other games, database contents, or post-game forensic artifacts.
- Do not accumulate a transcript.
- Can Submit Action: No.
