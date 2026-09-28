# S07-38 — v7i Run #1 one-game gate: technical failure before game evidence

## Result and identity

- Status: `PARTIAL / TECHNICAL_FAILURE`. The authorized single Runner play path failed before any fresh game observation. No retry, resume, second game, second service start, or strategy patch occurred. Return to Main for review.
- Launch base: `main@89d97f6500e1873700e5129f779bdc3356989293`, equal to `origin/main`; working tree clean. Candidate: `candidate-v7i-pre-review-result-realization-probe`; parent: `candidate-v7h-evidence-recovery-hardening`.
- Candidate bytes matched the S07-38 lock: manifest SHA-256 `0946e8b3c7cff62661bfb948a9e0cde39fce664847cb41bae4390587ae6c4fa3`; instruction SHA-256 `0dd590d21e036e5dc4cdde25553d250ac87439ab4cc1af29bc75c07367026721`; Skill Git blobs Board `1707e8183e3b7f4c299838b4fc2c0f01de7581e2`, Planning `67947aa2928eae2f09f94edfafd08fda00311fd5`, Delivery `48dcbece745734a16f1b5caffadce55d7e7ecf97`, Risk `06bb1289499356d2d882dc4336eb17832f8e2fdf`.
- The frozen root `.venv` existed; Runner, `pyproject.toml`, and `uv.lock` were unchanged since the prior successful v7g run. The active instance configuration named the official-compatible `api.deepseek.com` host, `deepseek-flash`, and a present credential; the Dev distribution and configured DB path existed. Credential value was not displayed. S07-37's 14 passing static tests were reused because the Candidate bytes had not changed.
- The canonical helper built `.local/runtime/s07-38-v7i-run1/submission`; manifest identity/mode, exactly four Skills, and each bundled file's byte identity with the repository passed. Runner `play --submission` performed its normal install/reload; there was no separate install command. The configured shared DB was not opened, queried, parsed, or hashed.

## Startup, failure, and cleanup

| Item | Observed accounting |
|---|---|
| `career_emu` start | 1 at `2026-09-28T10:35:04.9145191Z`; hidden launcher PID 2704. |
| Readiness | Manager reported `running` (service PID 2172), and ports 19092, 20000, 20001, 6173 were listening before Runner start at `10:35:40.5974024Z`. Exact readiness instant was not timestamped; the observed upper bound from start to Runner was 35.68 s. |
| Startup prewarm | No successful completion or token usage was observed. The pre-Runner LLM log window contains two connection-error events. This is not v7i provider validation. |
| Runner `play` | 1 invocation with root `.venv` Python, the packaged v7i submission, and the current configured DB path; `10:35:40.5974024Z`–`10:36:03.8126762Z`; exit 1, `max_continuations`. No `--continue`. |
| Runner frames | 41 `e2a.complete/succeeded` final frames, with no transcript file. The Runner gameplay usage object reports 0 input/output/total tokens; this is not a claim of zero billed usage. |
| Provider | During the Runner window, 23 LLM start/error pairs were logged; errors were `APIConnectionError / Connection error`. No successful gameplay response was observed. Network/provider root cause beyond that error is `UNKNOWN`. |
| Game tools | Actual `new_game`, `observe`, and `take_action` calls observed: 0. The only `new_game` text in the scoped Runner service log was MCP tool registration, not invocation. A separate DB confirmation was prohibited, so game-state mutation is not independently DB-verified. No second play was attempted. |
| Service stop | 1 graceful stop at `10:38:02.5799124Z`–`10:38:03.8182367Z`, exit 0. Manager then reported `stopped`; all four listeners were released. No restart. |
| Billed cost | `UNKNOWN`; the Runner's `total_cost=0.0` is not a billing record. |

The new diagnostic output directory was `D:\CS\CareerSim\.career_sim_runner\career_emu\outputs\local-s06-adaptive-controller\20260928T103543Z\`. Its `score_report.json` carries drive session `career-sim-runner-02af021e00db` but game session `d4464a311c924e73b9e23eebd6f71f6d`, the earlier v7g Run #1 session. Its `54.52 / 38.17 / 48m / C` score is **stale historical data**, not a v7i outcome. The report's `completed=true` belongs to that old session and is excluded from every S07-38 result and comparison.

## Mechanism, early window, and correctness audit

| Required field | S07-38 observation |
|---|---|
| Pre-first-review opportunity table | No fresh public Board/Delivery state or legal candidate was produced. Eligible/applied/selected/result fields are `UNAVAILABLE`, not negative observations. |
| `TRUE_TRIGGER / CORRECT_NON_TRIGGER / FALSE_TRIGGER / MISSED_TRIGGER / AMBIGUOUS` | 0 classifiable decisions; none of these counts evaluates the mechanism. |
| Mechanism outcome | `MECHANISM_INCONCLUSIVE`. This is not `MECHANISM_NOT_TRIGGERED`, which requires a valid game with no qualifying opportunity. H-V7I-01 is not informed by this attempt. |
| M1 initial state, Story choices, M3 Energy/Main, M6 review feedback/grade/promotion | `UNAVAILABLE`; no fresh game observation. No month-end state was substituted for review-time evidence. |
| M1/M3/M6/M9/M12/M18/M24/M36/M48 trajectory, final public dimensions | `UNAVAILABLE`; the old v7g score report is excluded. |
| Public evidence/HiddenRisk discipline | No v7i Board, PLAN/CANDIDATE, Risk, CTRL, or action rationale was observed. Numeric internal references observed in v7i decision text: 0; discipline classification is `NOT_EVALUABLE`, not PASS. |
| Action preflight | 0 observed attempts, 0 successes, 0 schema rejects, 0 missing/multiple/noninteger choices, 0 malformed CTRL, 0 observed duplicate side effects. Preflight adherence is `NOT_EVALUABLE`. |
| Decision closure | No v7i candidate/Risk decision; reopening and token inefficiency are `NOT_EVALUABLE`. |
| Context compression/recovery | No observed compressor epoch. `RECOVERY_PATH_NOT_TRIGGERED`; the recovery implementation was not exercised. |

Classifications: gameplay `TECHNICAL_FAILURE`; runtime `RUNTIME_ADHERENCE_INCOMPLETE`; strategy `PROMOTION_FIRST_ADHERENCE_INCOMPLETE`; mechanism `MECHANISM_INCONCLUSIVE`; evidence discipline `NOT_EVALUABLE`; recovery `RECOVERY_PATH_NOT_TRIGGERED`. `provider_validated`, `gameplay_validated`, `runtime_validated`, and `long_horizon_adherence` remain false. `survival_improvement_proven`, `score_improvement_proven`, `stable_80_plus_proven`, `hidden_test_transfer_proven`, and `next_game_authorized` also remain false.

## Score and historical comparison

S07-38 quantitative score, competition partial score, survival months, grade, promotion months, and final dimensions are all `UNKNOWN / NOT_OBSERVED`. `UNPAIRED_SINGLE_RUN_DESCRIPTIVE_ONLY` is the comparison boundary, but no v7i game result exists to compare with v7g #1 (`54.52 / 38.17 / 48m / C`), v6 #1 (`75.29 / 52.70 / 48m / A`), or v1 #1/#2. No directional-above/similar/below label is assigned.

## Raw evidence and hold

All raw files below remain local and uncommitted. The service log copies are frozen under `D:\CS\CareerSim\.local\runtime\s07-38-v7i-run1\raw-service-snapshot\`; the Runner events and diagnostic score remain in the unique output directory above. `evidence-manifest.json` at the run root records each absolute path, byte count, and SHA-256; its own SHA-256 is `452188879cafef44bff398f407d04bb38ef32bc92e52c012873ce2ac9ac60505`.

| Local raw artifact | Bytes | SHA-256 |
|---|---:|---|
| `service-start.stdout.log` | 521421 | `aadb5e65b2a8e08cf7e105930b94b4e136061930c30d1bc06ff9389d2460f3d5` |
| `service-start.stderr.log` | 3378217 | `e7a0a57b0e546db13ba9bc25931d00c7e2329403b98e8bc3a8d3a84ad5a848cd` |
| `service-stop.log` | 493 | `77cdfd6727dca3d7c768f8ea3a1f86d66b074dc27e68f10ad8cd40871bda9063` |
| `runner-console.log` | 2637 | `9339ebe4a324f33d974a636bbb48470fd55e0745f3c1a69258550d508f6ad619` |
| `events-20260928T103543Z.jsonl` | 6223 | `c4b80869380c1305a0f6992ba6e79012591a80819fd8fb921ee66722c8b1cb7b` |
| `score_report.json` (stale diagnostic) | 2577 | `0ef17bc96f744493fd8083affd9201cbfbf1080c891deee1433ef3f91f6d5da1` |
| `raw-service-snapshot/llm.log` | 13263737 | `ef62f0a39ed15e8e66135e9ac815b36bbf24481aec16f91b84664d94d939f848` |
| `raw-service-snapshot/runner.log` | 2858979 | `69d39a57134243d360cee3014121e6e33ea8b93948f509e8b39336eead0407c9` |
| `raw-service-snapshot/server.log` | 119920 | `a39ce64568b617d6af4296731c5e2087565b645d439d145e5cc8caf00e0236a3` |
| `raw-service-snapshot/session.log` | 27566 | `b8637b3ee447088cd964a0658280ea5aba9ccea4cf0dcbca3971d8c5d1f9f099` |
| `raw-service-snapshot/jiuwen.log` | 5363017 | `87b93388a818024f5110a3f5dca2c9866c160ad30eb7f0af005bea3481774148` |

Expected transcript path `...\20260928T103543Z\transcript-20260928T103543Z.log` does not exist; it must not be reported as captured. No DB file, secret, raw transcript, log, runtime bundle, or raw score is committed.

`FORENSIC_HOLD`: S07-38 owns the local run directory and unique Runner output directory. The held window is service start `10:35:04Z` through stop `10:38:03Z` on 2026-09-28. Retain the manifest-listed files at least until Main accepts the failure classification, confirms whether the missing transcript/stale-score behavior needs reanalysis, and explicitly releases the hold. Hashes are identifiers, not substitutes for raw files. No cleanup authorization is inferred.

## Interpretation and handoff

- **FACT:** One authorized service lifecycle reached readiness and stopped cleanly; one Runner play path failed after repeated LLM connection errors. No fresh game tool call, public observation, or successful gameplay provider response is visible in the retained evidence. The emitted score belongs to the earlier v7g session.
- **INFERENCE:** The immediate technical blocker is provider connectivity during startup and the Runner drive. Its underlying network or provider cause is unknown; the stale score reflects a failed-run reporting hazard, not a v7i score.
- **HYPOTHESIS:** H-V7I-01 remains untested. This attempt supplies no evidence of mechanism execution or score benefit.
- **Limit:** The Plan prohibited DB inspection and a second play; actual game-state mutation was therefore not independently checked through the DB. The missing transcript limits deeper action-level audit. No further game is authorized by this Task.

`RETURN_TO_MAIN_AFTER_V7I_ONE_GAME`
