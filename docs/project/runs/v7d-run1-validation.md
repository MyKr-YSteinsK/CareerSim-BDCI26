# S07-29 — Candidate v7d Run #1 Validation

## Result and identity

- Gameplay: `VALID_EARLY_TERMINATION`; runtime adherence: `RUNTIME_ADHERENCE_FAIL`.
- Candidate: `candidate-v7d-strategic-continuity`, parent `candidate-v7c-global-decision-policy`.
- Candidate source commit: `0b7a3e226ba1e88983f8eebe1daef2ffa0f5d3eb`.
- Canonical LF manifest SHA-256: `22e63b86b98daa009838353491f629119b45d74da94adb6c0c1ff2c7ba6cef00`; instruction SHA-256: `72b851877971c998aeba804ae62275d0651be83bea717b6d7b6552fdb36317f3`.
- Skill Git blobs: Board `e76cb289833ad00a7c40c331cb8d6035bde15221`; Planning `7c9c226c3df80f386d1dcf0eb083cc912e5b55e3`; Delivery `9a84f723da92971850f167a3eebdc862ff95c20c`; Risk `b59fd1c8bc54d9b3469b4de22f3d5f8c126fb2ef`.
- Bundle at `.local/runtime/s07-29-v7d-run1/submission`: Runner submission validation passed; exactly four Skills, all byte-identical to repository sources. The actual shared install had exactly four enabled Skills with matching bytes; manifest was v7d, mode `agent`.

The worktree uses CRLF for `configs/runtime_manifest.json`; its on-disk SHA-256 and the copied bundle SHA-256 are `ebb4fd3cfc97e6b077f98b996a691271ef9d144bbd7bdff7fef4e230edb0423d`. The canonical LF identity stored in Candidate metadata and frozen by this Plan is `22e63b86b98daa009838353491f629119b45d74da94adb6c0c1ff2c7ba6cef00`; bundle and worktree bytes match exactly.

## One-game outcome

- Service lifecycle: `career_emu` started once and gracefully stopped once; final status `stopped`.
- Runner play invocations: 1. Fresh `new_game`: 1. Session: `5667ea7c7f7b4566ab805d05a2dc1b8c`; drive session: `career-sim-runner-f8c66284976e`.
- Start timestamp from Runner output directory: `2026-09-27T14:34:25Z`; score report timestamp: `2026-09-27T14:45:47.671208Z`; elapsed run time: about 11m23s.
- Outcome: eliminated naturally at Month 15; Runner play exit code 0. Quantitative score `17.02`; competition partial `11.92`; grade `E`; `completed=false`. No promotion observed; final Level `L1`.
- Last participant-visible state: `duration_in_level=15`, Skill 9, Network 3, Output 2, Wealth 0, Health 6, Dignity 9, Energy 0. The runtime field was `duration_in_level`; `CurrentLevelDuration` itself was not present in that payload.
- Runner score dimensions: Level 3.00, Wealth 0.15, Resilience 11.25, Skill 1.12, Risk Control 1.00, Network 0.50 weighted points.
- Participant-visible progression feedback included performance C / no advance at the M6 review. The run ended before long-horizon behavior could be assessed.

## Provider and usage

- Static config checked before play: OpenAI-compatible interface, host `api.deepseek.com`, model `deepseek-flash`; credential presence was `PRESENT`. No secret value was read into output.
- Runner reported model `deepseek-flash`: 11,021,480 input tokens, 118,749 output tokens, 11,140,229 total. Cache usage was unavailable. Runner-reported cost was `0.0`; actual billed cost is `UNKNOWN`.
- No separate provider ping, test prompt, or second game workload was issued. AgentServer logs in the run window contained no error, traceback, timeout, or connection-error markers.

## Runtime adherence

- Single Agent mode. The first action came after reads of `structured-state-board`, `rolling-planning`, `delivery-progress`, and `risk-review`.
- There were 60 `observe` calls and 60 `take_action` attempts. Fifty-nine actions succeeded with one integer `choice`; each successful state-changing action was followed by a fresh observe before the next action. One attempt omitted required `choice` and was rejected by schema validation before mutation.
- All 60 action notes had one valid CTRL prefix. No `RECONSIDER` path was used. `DECISION_CLOSED` did not appear literally in the transcript; closure is inferred from the risk/action/observe sequence. The missing-choice attempt makes runtime adherence fail even though the agent recovered and continued.
- Four Skills were loaded before the first action. No context compression or recovery epoch was observed, so recovery adherence is untested.
- Direct DB contents and bytes were not read or hashed. Runner scoring used the configured DB path through the normal play/report path.

## Strategic adherence

The transcript expressed an initial objective to build compounding career capital through the first formal review, one broad early-career gap, and a review/promotion checkpoint. After fresh M6 performance-C/no-advance feedback and Network at 1, it revised toward Network/trust recovery and a later public review checkpoint.

After M6, the G marker moved repeatedly among performance, hidden risk, health, Output, Skill, and Delivery themes without a documented FULL plan revision for every change. One action note described mentoring as an “implicit hidden hard indicator” for performance A. This supports a material anti-churn concern and records an agent inference; it does not establish a simulator rule. Output was used as a public progression signal in action rationale. Level, review feedback, and `duration_in_level` were also referenced. No explicit Delivery receipt or commitment realization was established before termination. One handbook call and two latest-log calls occurred; no repeated handbook/search loop was observed. Late-horizon bias was not testable.

## Evidence and limits

Raw local evidence is retained under `.career_sim_runner/career_emu/outputs/local-s06-adaptive-controller/20260927T143425Z/` and was not committed:

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| Events JSONL | 756,124 | `e4e388517aff115747fabe068a76b1bc3d960b43900373d4eca804097348be78` |
| Transcript | 405,132 | `93a852f97f4b7f13decce82b29ccb52d0bb18db931d0241793474ace4e09527f` |
| Runner score report | 2,733 | `0dd880b4f7fc154c18f15b1520e25be04f4375153d1b76753a1db2a75024927b` |

Service logs remain local under `C:\Users\Yukis\.jiuwenswarm-instances\career_emu\agent\.logs`; `agent_server.log` SHA-256 is `a016a63b03b768e7f4099fbc0be229f09e76096bbfb55a925d82a9f3cf2b0eef`, and `full.log` SHA-256 is `d39bef2761a144ad14f04bf04abc3c1d9341ae8578e595d63106d0d48ab505b7`.

During startup the JiuwenSwarm foreground wrapper logged GBK Unicode encoding errors but reached `running`. The graceful stop command returned 0 and final status was `stopped`; the foreground wrapper later exited 1 while logging. No restart followed. The standard instance-root port/data `.env` was generated; `config.yaml` and `config/.env` write times remained unchanged.

Post-run Candidate flags: `provider_validated=true`, `gameplay_validated=true` for this one run, `runtime_validated=false`, `long_horizon_adherence=false`; survival/score improvement, stable 80+, hidden-test transfer, and `next_game_authorized` remain false. This single early termination proves no causal improvement, stable score, long-horizon adherence, or hidden-test transfer. `S07=ACTIVE`; `NEXT_GAME=NOT_AUTHORIZED`.
