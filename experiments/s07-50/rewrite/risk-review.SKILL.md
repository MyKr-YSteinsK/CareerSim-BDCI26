---
name: risk-review
description: "Immediately before action, route the final candidate through a quick ordinary-cost gate or a full material-risk review and return one auditable result."
---

# Risk Review

## Purpose and inputs

Review only Planning's final legal candidate using the current Board, MODE, public candidate consequences, and confirmed public receipts. Planning owns plan and ranking; Risk does not select or optimize the whole decision. The manifest owns the global evidence firewall.

## Decision procedure

### Step 1 — Route

Ask: does this candidate directly engage a current material public risk or binding constraint (including an action about that risk, one that may worsen it, or one chosen to contain it)?

- **NO → QUICK_GATE.** If only ordinary workload, small H/D cost, soft friction, uncertainty, or opportunity cost is present, return `PASS`.
- **YES → FULL_REVIEW.** Assess only the public risk and this candidate. `PASS` is not an available result on this branch.

### Step 2 — Full review result

| Public finding | Result |
| --- | --- |
| Candidate adequately handles the material risk and remains acceptable | `ALLOW` |
| Material concern remains, but changing the candidate is not justified | `WARN` |
| Candidate does not handle a clear risk and one directly relevant legal alternative does materially better | `RECONSIDER` |
| Decision-relevant public evidence is missing, stale, or ambiguous | `UNKNOWN` |

Do not manufacture label diversity. A safe candidate can receive `ALLOW` after Full Review.

### Step 3 — Close

Return one result and one concise public-evidence reason. After `RECONSIDER`, Planning may compare one relevant alternative once; review the selected alternative independently. A second `RECONSIDER` leaves the path incomplete. CTRL records the selected submitted candidate's final result; the manifest owns structural closure and submission preflight.

## Output

```text
RISK: PASS|ALLOW|WARN|RECONSIDER|UNKNOWN
REASON: <one concise public-evidence reason>
```

## Boundary examples

- Ordinary workload/opportunity cost only: `QUICK_GATE → PASS`.
- Acute unresolved symptom, candidate continues high-intensity work, and a directly relevant safer legal option exists: `FULL_REVIEW → RECONSIDER`.
- Acute symptom, candidate directly rests/contains the risk and remains acceptable: `FULL_REVIEW → ALLOW`.
- Active confidentiality risk, candidate uses the compliant handling path: `FULL_REVIEW → ALLOW`.

## Invariants

- Never return PASS after Full Review. Do not infer hidden risk, thresholds, or event-title answers.
- Can Submit Action: No. Do not call `new_game`, `observe`, or `take_action`.
