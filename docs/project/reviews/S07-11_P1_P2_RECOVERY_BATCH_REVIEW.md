# S07-11｜显式拒绝恢复与六局 Mechanical Batch

## Identity / boundary

- Base: `main@8b98ef6f3410e1ee239b3416e2879107396caf3e`; current Candidate remained `candidate-v6c-compliance-cleanup` (not executed as an Agent).
- Authorization: task-scoped, direct public MCP only; P1→P2→P1→P2→P1→P2, six fresh sessions. No AgentServer, provider, Runner play, Skill install, or Candidate change.
- Compact evidence: [`../runs/s07-11-p1-p2-recovery-batch.json`](../runs/s07-11-p1-p2-recovery-batch.json). Ignored per-session public trace, session summary and server stderr: `D:\CS\CareerSim\.local\runtime\s07-11-p1-p2-recovery-batch\`; individual SHA-256/bytes are in the compact evidence. Raw/local artifacts were not committed.

## Rejection recovery

The harness now retains only bounded participant-visible rejection fields (including MCP `isError` structured/JSON errors), issues **one** fresh observe on the same session, and compares complete projected public time/status/terminal fields. Event text or legal-choice changes alone do not prove state mutation. Clearly unchanged → `POLICY_ACTION_REJECTED`; clearly changed → `EXPLICIT_REJECTION_STATE_CHANGED` with public delta; missing/contradictory evidence or failed recovery observe → stop on Unknown Side Effect. The rejected action is never resent. Action ceiling now counts attempts, not merely successes.

Targeted offline tests cover the receipt shapes, unchanged/changed/missing/mismatched public state, failed recovery, continuation into the next fresh slot, budgets, and existing P1/P2 behavior. No policy selection semantics changed after the first `new_game`.

## Fresh sessions

| Slot | Policy | Public session ID | Outcome | Month | Attempts / successes / rejections | Grade / score | Stall / switches |
| --- | --- | --- | ---: | ---: | ---: | --- | ---: |
| 1 | P1 | `0b455fc88ccc4de19bf7176eefb771fa` | `POLICY_ACTION_REJECTED` | 3 | 12 / 11 / 1 | UNKNOWN | 0 / 0 |
| 2 | P2 | `13eb0a8c3a67425389f18cabca799ed8` | `POLICY_ACTION_REJECTED` | 3 | 12 / 11 / 1 | UNKNOWN | 0 / 0 |
| 3 | P1 | `de9d6a692a634672b9f5bdad66d41660` | `POLICY_ACTION_REJECTED` | 3 | 12 / 11 / 1 | UNKNOWN | 0 / 0 |
| 4 | P2 | `c138011479f0440098f172e44752a8d6` | `POLICY_ACTION_REJECTED` | 3 | 12 / 11 / 1 | UNKNOWN | 0 / 0 |
| 5 | P1 | `6ec265490df341ef9028f1db194862b3` | `POLICY_ACTION_REJECTED` | 3 | 12 / 11 / 1 | UNKNOWN | 0 / 0 |
| 6 | P2 | `d1945b3f8c7b4f7ba035137d91c02171` | `POLICY_ACTION_REJECTED` | 3 | 12 / 11 / 1 | UNKNOWN | 0 / 0 |

Every explicit public receipt reported `Insufficient energy for high_intensity_work: 1 remaining`. In all six slots, the immediate recovery observe confirmed unchanged projected public state; no rejected action was resent. The public final Energy was 1, Level L1. Each session closed its direct MCP child normally. The identical rejection occurred despite different public story trajectories; it is a repeatable **mechanical affordability failure in this probe policy**, not proof of deterministic replay or a hidden game rule. The legal displayed choice was not necessarily affordable. Neither P1 nor P2 reached a comparable progress checkpoint or natural terminal; P2's stall response was not exercised. P1 vs P2 score/survival comparison is therefore unavailable.

P1 fresh aggregate: 3 rejected / 0 completed, month range 3–3, 33 successes / 36 attempts, 0 stalls. P2 fresh aggregate: the same. These are unpaired independent sessions with no public seed control; no causal or stable-performance claim follows.

## Prior partial session (excluded)

S07-10 P1 `6a1bffe3a533494eb7352ad2f0436869`: M3, 11 successes / 12 attempts, no ending score, rejection receipt not retained and post-rejection state unknown. It is not counted in either S07-11 aggregate. S07-11 addresses that evidence gap but does not retroactively determine S07-10 state.

## Live accounting / decision

- Direct MCP start attempts / confirmed starts / clean shutdowns: **6 / 6 / 6** (budget ≤12 attempts).
- Initialize / list_tools / new_game: **6 / 6 / 6**; observe: **78**; take_action attempts / successes / explicit rejections: **72 / 66 / 6**. Per slot: one `new_game`, two observes around rejection plus 11 post-success observes = 13, and 12 action attempts; below all ceilings.
- AgentServer / provider / DeepSeek / Runner play / Skill install or reload: **0**. No observed residual task MCP process after shutdown.
- `MECHANICAL_PROBE_PRODUCED_ACTIONABLE_HYPOTHESIS`: a minimal public affordability guard is needed for these mechanical controllers to reach later checkpoints. This is a hypothesis/engineering decision for S07/Main, **not** a Candidate or Skill change authorized here. The batch executed all six slots safely, but no full mechanical session completed. Cheap-probe information about score, progression and P2 stall adaptation remains limited. Do not treat this as Agent policy effectiveness evidence.

Next: return to S07/Main for `REAL_AGENT_VALIDATION` planning and a decision whether any further cheap probe is worth its cost. No new game is authorized by this review; do not build another probe framework automatically.
