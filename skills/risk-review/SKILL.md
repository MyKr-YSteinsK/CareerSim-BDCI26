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

Use only whitelisted current-session public facts, participant-visible option text, and confirmed public receipts/logs. Ignore `HiddenRisk` (including numeric changes), hidden counters, internal score components, internal event identifiers/effects, and public-status-unclear payload fields even when a tool exposes them. Never put these values in a Risk reason, CTRL notes, or action rationale; `EXCLUDE_FROM_STRATEGY until verified public`.

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
`UNKNOWN` — decision-relevant public evidence is stale, missing, or source-ambiguous, so the candidate cannot receive a normal gate result yet. If normal public flow can resolve it, allow at most one fresh observe/rebuild cycle; genuinely new evidence may start one new Planning pass. If ambiguity remains and no further public evidence is obtainable within normal flow, make one bounded legal decision from available public evidence with final CTRL `R=UNKNOWN`; use `X=-` without reconsideration or `X=1` after one completed reconsideration branch. Do not loop observe/replan, invent facts, or infer hidden state.

After `RECONSIDER`, compare at most one directly relevant legal replacement and give the selected candidate its own final Risk gate before submission. CTRL `R` records that selected candidate's final `PASS|ALLOW|WARN|UNKNOWN` result; `X=1` records the completed reconsideration branch. If the selected candidate's Risk gate again returns `RECONSIDER`, do not open a second branch or coerce it into `PASS`: the path remains incomplete with `X=0`, and `take_action` is forbidden until genuinely new public evidence arrives. With no reconsideration use `X=-`; any `X=0` forbids submission.

Do not invent numeric thresholds, hidden counts, failure probabilities, or hidden-risk values.

## Close

After the final risk result, the decision is closed unless new public evidence arrives.

Risk does not own the Review Plan or candidate ranking.

Can Submit Action: No. Do not call `new_game`, `observe`, or `take_action`.
