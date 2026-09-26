# S07-14｜Clean Codex Public-Agent Pilot v2 Review

## Result

**`CODEX_PUBLIC_AGENT_ROUTE_PROMISING`** — as a research route, not as a claim that Codex outperforms a formal Candidate.

The one direct-public-MCP session reached a completed 48-month terminal: `65.16 / 45.61 / 48m / B`. This is a substantially longer Codex-as-Player trajectory than the prior S07-13 pilot, which stopped at M3 on an unresolved completed `success=false` response. S07-14's bridge reconciled its M48 explicit rejection by one fresh same-session observe, did not resend the rejected choice, and continued to terminal. The S07-11/S07-12 mechanical batches were also short-lived (S07-11 sessions stopped at M3; S07-12 only 1/4 passed M3 and none reached M12), but these were different unseeded sessions and are not controlled comparisons.

## What the run supports

- Direct Codex decisions over public observations can form a coherent, long-horizon trajectory in one session.
- Public-state-aware recovery was visible in several cases, including responding to observed health costs and converting a confirmed rejected Energy action into a different Codex-selected legal action.
- The action record shows frequent critical-project Main choices (11/16), periodic reports/resources/exposure/mentoring, and substantial story-semantic choices. The run did not use a mechanical policy selector.
- Technical outcome: valid completed public game, one confirmed rejection safely reconciled, normal direct-MCP shutdown, no unknown side effect.
- Gameplay outcome: completed B-grade run, not a high-score result. Public final score dimensions were not retained in the projection.

## Limits and review boundary

- Prior public trajectories and policy discussion were explicitly accepted as priors. **`NOT_A_BLINDED_POLICY_EVALUATION`**; no claim of independent prior-free discovery is made.
- One run cannot establish repeatability, variance, causal strategy effects, superiority over S06/v6 or mechanical policies, or stable 80+.
- The score outcome was lower than the known S06 v6 one-run result (`75.29 / 52.70 / 48m / A`), but Candidate, runtime mode, and decision process differ; this is descriptive only.
- No public seed/replay control was established by this run. Codex token/cache usage and platform cost were unavailable; provider calls were zero.
- Final score-dimension details were omitted by the driver's allowlisted projection. The public terminal status fields are retained in the local trajectory; no database was inspected to fill the gap.
- Submitted choices and short rationales are auditable; private chain-of-thought, repeated unsubmitted deliberation, and a formal `STALLED` state are not measured.

## Safety and repository scope

- Authorization: `AUTHORIZE_S07_14_CLEAN_CODEX_PUBLIC_AGENT_PILOT`.
- Fresh game/new_game: `1/1`; direct MCP lifecycle `1`; AgentServer/provider/DeepSeek/Runner gameplay/install/reload/second game: `0`.
- No hidden/private simulator data, decoded tables, hidden thresholds/formula, or event-to-answer lookup was accessed. The player phase used the permitted bridge/tests and public session information; repository historical public evidence was only consulted after terminal for descriptive comparison.
- Formal Candidate, Skills, runtime manifest, Runner, dependency files, `CURRENT_STATE.md`, and ADR were not changed.
- The local raw public trajectory is ignored by Git and identified in the run record by path, bytes and SHA-256.

## Recommendation

Return to Main with `CODEX_PUBLIC_AGENT_ROUTE_PROMISING`. If Main wants to test repeatability or isolate mechanisms, request a separate bounded multi-run design and live authorization. This pilot authorizes no second game and changes no Candidate.
