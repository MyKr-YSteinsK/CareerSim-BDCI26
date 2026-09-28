---
name: risk-review
description: "Use immediately before every take_action on Planning's final candidate. Pass ordinary growth costs; escalate only when fresh public evidence shows a direct material threat to survival, job continuity, trust, compliance, confidentiality, safety, or an already-binding Health/Dignity/Wealth constraint. Never re-plan the whole decision."
---

# Risk Review

## Contract

Input:
- Planning's final legal candidate;
- fresh Board;
- current `MODE`;
- candidate's public consequences.

Output exactly one result:

```text
RISK: PASS|ALLOW|WARN|RECONSIDER|UNKNOWN
REASON: <one concise public-evidence reason>
```

## Quick gate

Return `PASS` when the candidate has only ordinary:
- workload;
- small Health/Dignity cost;
- relationship friction;
- uncertainty;
- opportunity cost;

and no fresh public evidence makes that cost material.

Do not block a high-value growth path merely because it is not the safest option.

## Full review

Run a full review only when the candidate directly touches a material public risk such as:
- severe Health or psychological danger;
- job-continuity / dismissal danger;
- trust crisis or credible retaliation;
- compliance / confidentiality / safety;
- explicit affordability pressure;
- direct worsening of the binding constraint that caused `MODE=S`.

For Wealth stress, distinguish discretionary spending from progression/income recovery. Do not reject a growth action solely because Wealth is low when the action directly supports performance, promotion, or job continuity.

## Result rules

`ALLOW` — material risk was reviewed and the candidate remains acceptable.<br>
`WARN` — material concern exists but current evidence does not justify switching.<br>
`RECONSIDER` — material risk is clear, the candidate does not handle it, and one directly relevant legal alternative exists. Compare at most that alternative, then close the decision.
`UNKNOWN` — decision-relevant evidence is stale, missing, or ambiguous.

Do not invent numeric thresholds, hidden counts, failure probabilities, or hidden-risk values.

## Close

After the final risk result, the decision is closed unless new public evidence arrives.

Risk does not own the Review Plan or candidate ranking.

Can Submit Action: No. Do not call `new_game`, `observe`, or `take_action`.
