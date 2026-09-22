---
name: career-action-trace
description: Use when the CareerSim agent is about to submit a take_action decision; preserve the chosen option and add a distinctive S02 verification marker to the normal decision trace.
---

# Career Action Trace

## When to use

Use this skill immediately before each Career Emulator `take_action` call.

## Required action

- Keep the choice selected by the normal CareerSim decision process unchanged.
- Keep the existing concise reason in the `notes` argument.
- Append exactly ` [S02_SKILL_USED]` to `notes`. If `notes` is empty, use `[S02_SKILL_USED]`.
- Submit the action through the existing `take_action` tool only once.

## Boundaries

- This is a trace marker only. It does not choose or rank choices, change strategy, or alter game state.
- The normal game loop owns `new_game`, `observe`, and termination handling; this skill does not call them.
- Do not create another agent, action submitter, memory, plan, or risk-control state.
