---
name: risk-review
description: Use before a CareerSim take_action decision when the latest public observe or feedback contains a risk, landmine, hidden-issue, trust-crisis, or clear performance warning, or when a currently legal choice explicitly offers risk mitigation; return ALLOW, WARN, RECONSIDER, or UNKNOWN without submitting an action.
---

# Risk Review

## Purpose

Before the same Single Agent submits a CareerSim action, review only the latest public evidence:

1. identify whether the current observe or visible feedback contains a clear risk warning;
2. check whether the current legal choices contain a directly relevant mitigation option;
3. check whether the candidate action ignores that public risk; and
4. state the risk and opportunity-cost trade-off without treating the most conservative action as automatically best.

This is an event-driven, warning-driven review. Do not run it as an always-on replacement for normal decision making.

## Trigger

Run this Skill only when the current public context contains one or more of:

- an explicit risk warning;
- a landmine or hidden-issue warning;
- a trust or trust-crisis warning;
- a clear performance-risk warning; or
- a currently legal choice that visibly offers risk mitigation while the latest public context contains a related warning.

Use meaning from the current public text, not a guessed keyword count. Never use hidden counters, hidden thresholds, random probabilities, post-game score fields, or an inferred risk value.

## Material Risk and Soft Cost

Material Risk is an explicit severe Health, trust/crisis, confidentiality/compliance, retaliation/escalation, termination/survival, or other major public consequence. Soft Cost is small Health/Dignity loss, time, ordinary friction/pressure, or uncertainty.

Soft Cost alone is opportunity cost—not a `RECONSIDER` trigger or automatic veto of high-upside growth. If both occur, assess full evidence without discounting Material Risk. `rolling-planning` owns strategic `Risk Budget`; this Skill reviews only the current candidate.

## Input

Use only information legally visible at the current decision point:

- the latest `observe` result already available to the Agent;
- the current public state;
- the current event and its visible feedback;
- the current legal choices; and
- public Handbook rules already available to the Agent.

Do not require or create a separate Memory system. Do not use stale information from another session.

## Output

Return exactly one lightweight state: `ALLOW`, `WARN`, `RECONSIDER`, or `UNKNOWN`, with a short evidence-based explanation.

### `ALLOW`

There is not enough current public material-risk evidence to require changing the candidate action. Soft Cost alone does not require a risk-driven candidate change.

### `WARN`

Public risk evidence exists, but no clear low-ambiguity mitigation choice is currently legal, or the evidence is insufficient to recommend switching. Warn only; do not force a different action.

### `RECONSIDER`

Use only when all three conditions hold:

1. current public evidence clearly identifies a relevant material risk;
2. a directly relevant mitigation action is present in the current legal choices; and
3. the current candidate does not address that risk.

Ask the Agent to compare the original candidate with the legal mitigation choice once more. `RECONSIDER` is not an instruction to choose the most conservative action.

### `UNKNOWN`

Use when the session, state, choices, or public evidence is missing, stale, ambiguous, or insufficient. Return to the normal decision process without blocking or inventing a rule.

## Special rule: `处理历史埋雷`

Mention `处理历史埋雷` only when that exact action is present in the current legal choices and the current public context contains a related risk, landmine, or trust warning. Treat its true effect as unknown.

Never invent the action when it is absent, claim that one use removes risk, impose a warning-count threshold, or select it unconditionally each quarter.

## Action authority

- **Can Change Candidate Action:** Yes, only by asking the same Agent to compare current legal alternatives.
- **Can Submit Action:** No.

This Skill must not call `observe`, `take_action`, or `new_game`. The normal loop remains:

`observe → normal candidate selection → risk-review when triggered → same Agent final decision → take_action`

There must remain exactly one action submitter. Do not create another Agent, action submitter, Team, Swarm, Memory, Planning system, database, or persistent risk state.

## Failure fallback

If the review cannot establish a fresh public basis, return `UNKNOWN`, do not intercept the action, and let the normal Agent decision proceed.

## Traceability marker

When this Skill actually runs, preserve the Agent's original concise reason and append exactly one matching marker to the final `take_action` `notes`:

- ` [S03_RISK:ALLOW]`
- ` [S03_RISK:WARN]`
- ` [S03_RISK:RECONSIDER]`
- ` [S03_RISK:UNKNOWN]`

Keep any existing `[S02_SKILL_USED]` marker unchanged. The marker is execution evidence only; it is not an environment fact or a risk counter. This Skill still does not submit the action.
