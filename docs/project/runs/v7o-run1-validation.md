# TASK_RESULT｜S08-RUN01

## Status and identity

- Status: `RUN_ACCEPTED_WITH_RECORDED_CORRECTNESS_LIMITATIONS`
- Run classification: `VALID_48M_COMPLETION`
- Candidate: `candidate-v7o-execution-persistence-convergence`
- Parent: `candidate-v7n-public-state-delivery-constraint-hardening`
- Base: `main@b2e7ea6441da9c314d8a0ffbf29b9d5800ced10d`
- Final branch: `main`; final commit is the commit containing this report.
- Game authorization: `CONSUMED`
- Fresh session: `ab65fb3e46964184b0936fee4d7b3c49`
- Frozen Runner SHA: `f61c738c72e51b77298cc1c14c7c6ebf4b6c527d`
- Runner result: exit 0; one `new_game`; no replacement or resume.

## Live execution

- P1 targeted preflight completed before the run: 29 tests passed; Candidate package identity and four Skill files matched; `max_retries=2` was confirmed in the local `career_emu` config without emitting its contents.
- Runner child PATH fingerprint: `0b6d6533e52a903a652a18f409fd6771de0087e4b8ec3b99c960a662bb47dde9`. Proxy environment fingerprint: `d02b952be3761e598f9dfbbcae31a71208367034b3f0623a2a5be86e17e83f0b`.
- One actual bare `jiuwenswarm-start --list` invocation exited 0. One service lifecycle reached all four expected listeners. One Runner `play --submission` was started without `--continue`; Candidate install/reload occurred only inside that invocation.
- Runner window: `2026-09-29T11:54:38.998424+00:00`–`2026-09-29T12:16:22.501988+00:00` (21m43.503564s).
- One graceful `--stop career_emu` exited 0; all expected listeners were released. The attached service-start process returned exit 1 after that stop. The run had already reached readiness and Runner completion; the launcher exit cause is unresolved and retained as an execution issue.
- Standalone provider probes: 0. Database queries: 0. Additional service lifecycles: 0. Replacement games: 0.
- A first local PATH helper raised `AttributeError` before spawning a child process; it was corrected before the one actual `--list`. This tooling error did not consume an extra CLI invocation.

## Outcome

- One fresh session reached a structured natural terminal at public month 49 after 48 survival months. Events, transcript, final observe, and score report session identity match.
- Score source: session-matched final observe. Quantitative score `71.83`; competition partial `50.28`; survival `48` months; grade `A`; completed=true.
- Final public state: Level L5; Health 9; Dignity 10; Skill 130; Network 53; Output 37; Wealth 43; Energy 0.
- Review checkpoints: M6, M12, M18, M24, M30, M36, M42, M48. Observed level changes: M6, M12, M18, M36. Quarterly Main actions: 16.
- Usage: 41,778,768 input tokens; 154,920 output tokens; 41,933,688 total. Actual billed cost is `UNKNOWN`.
- This single run does not prove causal score or survival improvement, stable 80+, or hidden-test transfer.

## Persistence and provider

- Successful actions: 205/205; observes: 206; action errors: 0; unknown results: 0; noncanonical routes: 0.
- Reconstructing the frozen Runner completion/duplicate-frame behavior from this run's events gives 3 counted completion boundaries, 2 continuation sends, and 3 normal productive boundaries. Action counts by boundary were 202 / 2 / 1; actions per normal productive boundary were 68.33.
- Relative to v7n's 21 boundaries, 20 sends, and 23/14=1.64 actions per productive boundary, persistence is `PERSISTENCE_DIRECTIONALLY_IMPROVED` for this session. This is descriptive evidence from one run, not a probability or causal estimate.
- No `max_continuations` termination or Runner `e2a.error` boundary was observed. Zero-work provider-error terminations at the Runner boundary: 0.
- The run-window LLM log has 3 `APIConnectionError` line matches across 2 minute buckets. Service stdout has 12 `APIConnectionError`, 6 `ConnectError`, and 3 `FrameworkError` line matches; service stderr has 9 `APIConnectionError`, 6 `ConnectError`, and 7 `UnicodeEncodeError` matches. These are per-stream line counts, not unique failures; traceback lines may duplicate an underlying error. The logs do not expose a request ID or retry marker that binds the provider matches to specific retries/boundaries. Provider path completed this session; retry=2 effectiveness is `INCONCLUSIVE`.

## Correctness audit

- Board: 111/111 parsed Board snapshots have an exact field-value match to a public observe from the same month. Transcript messages are not event-timestamped, so latest-observe ordering is not independently proven.
- MODE: seven action markers use phase `P=S`. M17's psychological-distress event and M20's acute physical-symptom event have explicit public cues; M7's burnout signal is borderline. Four M36 actions used `MODE=S` based on a declining public Health number and an inferred failure threshold, while the event was about career strategy and contained no material public warning. This is a numeric-only false `MODE=S` finding under the Plan's rule.
- Hidden fields: transcript matching found 7 numeric HiddenRisk text matches and 0 numeric HiddenRisk/internal-score matches in action notes. The audit labels transcript matches as text matches, not a semantic verdict. No hidden numeric values are reproduced here.
- CTRL: valid single-integer choice markers and closure passed 205/205. Risk gate markers were present 205/205: PASS=169, ALLOW=36, WARN=0, RECONSIDER=0.
- Delivery: DL syntax and coverage passed 205/205. All markers represented the empty state; Delivery item identity, evidence, recognition, and lifecycle transitions were not exercised.
- Compression/recovery: five compressor markers were found in the run window. Of four markers followed by another action, two had a fresh same-session observe but no required four-Skill reread, and two had no fresh observe. All four failed the required tool-order check. The last marker had no next action, so status is `UNKNOWN_NO_NEXT_ACTION`. Rebuild semantics are not machine-verified.
- Runtime and long-horizon adherence remain `false`; completion alone does not override the recovery and MODE findings.

## Evidence

- Exact Runner output directory: `.career_sim_runner/career_emu/outputs/local-s06-adaptive-controller/20260929T115441Z/`.
- Archived evidence: [artifacts/dev-runs/s08-run01-v7o](../../../artifacts/dev-runs/s08-run01-v7o/). Existing archive tooling's secret scan and core session-consistency check passed. Raw local files remain under `.local/runtime/s08-run01/`; the original run outputs were not deleted.
- Events: 2,067,779 bytes; SHA-256 `b6eb500f9e8ad3966e595e65a5d558c2c8b50097bf908fd8b93a1b5f14567df4`.
- Transcript: 391,194 bytes; SHA-256 `a15555f91ae738859844cd0ffc2768ea00ab79c5f2adf10bc7144d7e3742b0e7`.
- Score report: 1,205 bytes; SHA-256 `f5916ad029f9ed0b162885d7c939c4d3d0889c82fba5f79e14b1fd3c6f05080d`.
- Runner result: 277 bytes; SHA-256 `35de0677816136591a23c5ed847c8d7fb249c585fcf090ec08c96215e24bef6a`.
- One-pass `post_run_summary.json`: 263,268 bytes; SHA-256 `f0961f094132a09a44cadcc32b6cc50e11c086e3612cc89276d749f8b8c54067`. It was generated without an LLM log and therefore records compression as unknown. The separately bounded compression/provider parse used the exact run window; its source diagnostics are included in the archive.
- Archived run-window LLM log: 2,239,905 bytes; SHA-256 `6a727f69e00acd56dcf80ba5605cc076cc68a5046463cb2cfb16e2cc09b0eec4`.
- Archived run-window service log: 4,776,463 bytes; SHA-256 `fa20f750679c9a52112c4dbf232bd246587974538d699300e6da38769f80d81a`. Its UTF-8 archive slice combines the captured CP936 stdout and UTF-8 stderr; original captures remain unchanged locally.
- No shared database, `.env`, credentials, or unrelated sessions were archived.

## Repository updates and limits

- `configs/current_candidate.json`: `gameplay_validated=true` and `provider_validated=true` for this single session. `runtime_validated=false`, `long_horizon_adherence=false`, and all improvement/transfer flags remain false.
- `docs/project/CURRENT_STATE.md` and `docs/project/RUN_HISTORY.md` now record the outcome and limitations.
- Candidate behavior, Skills, Runner, dependency identity, retry config, and runtime files were not modified. Only validation flags changed in the Candidate manifest.
- Status remains `RUN_ACCEPTED_WITH_RECORDED_CORRECTNESS_LIMITATIONS`; S08 remains active and no Stage completion is asserted.

## Authorization and next decision

```text
S08_RUN01_GAME_AUTHORIZATION = CONSUMED
NEXT_GAME = NOT_AUTHORIZED
NO_REPLACEMENT_RUN_AUTHORIZED
```

Next decision: `S08_RUN_ACCEPTED_RETURN_FOR_SCORE_AND_STRATEGY_REVIEW`.

## S11-08｜FORENSIC_HOLD / S11 Retention Boundary

S09-11 explicitly reaffirmed that the original v7o raw `FORENSIC_HOLD` remained retained; S09-12 later recorded both runs' exact raw and original holds as active. The original hold-creation record was not recovered. The S08-RUN01 archive-introduction commit `3fd64bead5600c2f0bab677e7b832fe3678bdf12` establishes when the tracked run report/archive entered Git, not when or why a hold was created.

| Historical field | Reconstructed value | Evidence status | Source |
|---|---|---|---|
| Hold identity / legacy task | S08-RUN01 / v7o raw hold; no separate formal hold ID recovered. | `LATER_REAFFIRMED` | [S08-RUN01 record](v7o-run1-validation.md); [S09-11 review](../reviews/S09-11_V8A_V7O_TRANSPLANT_FIDELITY_REVIEW.md) |
| Hold existence | Original v7o raw hold was retained at S09-11 and later recorded active at S09-12. | `LATER_REAFFIRMED` | [S09-11 review](../reviews/S09-11_V8A_V7O_TRANSPLANT_FIDELITY_REVIEW.md); [S09-12 review](../reviews/S09-12_V8A_TWO_SAMPLE_TRAJECTORY_DIVERGENCE_REVIEW.md) |
| Exact paths | Original hold membership for each archive member is `UNKNOWN`. | `UNKNOWN` | [S09-11 review](../reviews/S09-11_V8A_V7O_TRANSPLANT_FIDELITY_REVIEW.md) does not enumerate the original hold roster. |
| Hold owner | `UNKNOWN`. | `UNKNOWN` | No original hold record found in tracked history or inspected local metadata. |
| Original reason | `UNKNOWN`. | `UNKNOWN` | The run result and later fidelity review do not state the original hold reason. |
| Original creation point | `UNKNOWN`; commit `3fd64bead5600c2f0bab677e7b832fe3678bdf12` introduced the report/archive, not a hold-creation record. | `UNKNOWN` | Run record and archive-introduction commit `3fd64bead5600c2f0bab677e7b832fe3678bdf12`. |
| Later reaffirmation | S09-11 states both original raw holds were retained; S09-12 states both exact raw holds remained active. | `LATER_REAFFIRMED` | [S09-11 review](../reviews/S09-11_V8A_V7O_TRANSPLANT_FIDELITY_REVIEW.md); [S09-12 review](../reviews/S09-12_V8A_TWO_SAMPLE_TRAJECTORY_DIVERGENCE_REVIEW.md) |
| Release condition | `UNKNOWN`; no tracked source supplies or records satisfaction of the original condition. | `UNKNOWN` | [S09-11 review](../reviews/S09-11_V8A_V7O_TRANSPLANT_FIDELITY_REVIEW.md) records no release or cleanup authorization. |
| Current disposition | `UNKNOWN_REVIEW_REQUIRED`; S11 Main retains the core raw pair and protects the other six members under unknown scope. `HOLD_RELEASE_COUNT=0`. | `MAIN_CURRENT_DECISION` | [S11 final evidence ledger](../FINAL_EVIDENCE_REVIEW.md#forensic_hold-台账); S11-08 Main retention decision. |

All eight tracked archive members have `UNKNOWN` original hold membership. The current roles below are S11 retention decisions, not reconstructed historical scope.

| File | Original Hold Membership | Current Retention Role | Evidence Basis |
|---|---|---|---|
| `events.jsonl` | `UNKNOWN` | `KEEP_CANONICAL_RAW` | S09-11 used events through the first M6 review (seq187); S11 Main now keeps this representative full-run raw. Bounded use does not prove the original hold roster. |
| `transcript.log` | `UNKNOWN` | `KEEP_CANONICAL_RAW` | S09-11 used transcript lines 1–561; S11 Main now keeps this representative full-run raw. Bounded use does not prove the original hold roster. |
| `score_report.json` | `UNKNOWN` | `HOLD_PROTECTED_UNKNOWN_SCOPE` | Tracked archive member; no source confirms original hold membership. |
| `runner-result.json` | `UNKNOWN` | `HOLD_PROTECTED_UNKNOWN_SCOPE` | Tracked archive member; no source confirms original hold membership. |
| `post_run_summary.json` | `UNKNOWN` | `HOLD_PROTECTED_UNKNOWN_SCOPE` | Tracked archive member; no source confirms original hold membership. |
| `llm-run.log` | `UNKNOWN` | `HOLD_PROTECTED_UNKNOWN_SCOPE` | Tracked archive member; no source confirms original hold membership. |
| `service-run.log` | `UNKNOWN` | `HOLD_PROTECTED_UNKNOWN_SCOPE` | Tracked archive member; no source confirms original hold membership. |
| `evidence-manifest.json` | `UNKNOWN` | `HOLD_PROTECTED_UNKNOWN_SCOPE` | Tracked archive member; no source confirms original hold membership. |

No hold is released and no cleanup is authorized by S11-08. The `KEEP_CANONICAL_RAW` decision for events/transcript is a current S11 Main retention policy, not historical hold metadata; all six other members remain protected until a later explicit Main disposition.
