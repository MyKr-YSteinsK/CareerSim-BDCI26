# S07-33 — v7g Run #1 Validation

## Result

- Task status: `PARTIAL`; the authorized service lifecycle completed, but no Runner play or fresh game was started.
- Gameplay classification: `TECHNICAL_FAILURE` (pre-game operational stop; not a natural game termination).
- Runtime classification: `RUNTIME_ADHERENCE_INCOMPLETE`.
- Strategy classification: `PROMOTION_FIRST_ADHERENCE_INCOMPLETE`.
- No strategy, Skill, prompt, or dependency changes were made.

## Identity

- Candidate source base: `529f70cc0538c86933659c6186495d5defad889c` (`main`, equal to `origin/main` before this report).
- Candidate: `candidate-v7g-compact-skill-contracts`; parent: `candidate-v7f-promotion-first-survival-floor`.
- Candidate status: `STATIC_IMPLEMENTED_NOT_RUNTIME_VALIDATED`.
- Runtime manifest SHA-256: `1633dbb9e7948131c91a075d340930c2536c76a04538d13360603631e45c47d6`.
- Runtime instruction SHA-256: `8ba742657e8ddaf521d6b2acab82f7f8655eac81bc43015580321aee455037ac`.
- Skill Git blobs: Board `ec751e0b03c49d13641513eaa2f7c8bb00faa11`; Planning `11c2b09a684bd9ac9d3b676dd690ea56337c5fcb`; Delivery `c40a4f8487d99b76154894d859d6d81a6fcd8dd4`; Risk `d2c6e14c8e6ae3d3ebce12c43815f3a45cbfae6a`.
- Effective configured provider: DeepSeek `deepseek-flash` at `api.deepseek.com`; credential presence was checked without displaying values.
- Installed dev dataset check: PASS. Canonical package helper built `.local/runtime/s07-33-v7g-run1/submission`; bundle name/mode, four Skill files, and byte identity against the repository all passed. The v7g bundle was not installed.
- S07-32's targeted 11 tests were reused; no tests were rerun for this docs-only handoff.

## Live Accounting

| Operation | Observed |
|---|---|
| `career_emu` service start | 1 invocation; manager reported `running` at 2026-09-28 13:26:24.917. The launcher later exited `1` while logging GBK `UnicodeEncodeError`s. |
| `career_emu` graceful stop | 1; exit `0` at 2026-09-28 13:28:43.812; manager reported `stopped`, with no remaining Jiuwen processes or listeners on ports 19092, 20000, 20001, or 6173. |
| Candidate install / config reload | 0; Runner was not invoked. |
| Runner `play` | 0. |
| Actual `new_game` tool calls / game sessions | 0 / 0. The four `new_game` text hits in startup logs are MCP resource-registration records across two Agent prepare sessions, not tool invocations. No game session ID exists. |
| `observe` / `take_action` attempts / successes / schema rejects | 0 / 0 / 0. |
| Handbook / log calls | 0 / 0. |
| Context compression / recovery | 0 / `NOT_TRIGGERED` (no game). |
| Provider work | One automatic service-start prewarm DeepSeek chat completion; no explicit prompt, independent provider ping, or benchmark request was submitted. |
| Provider usage | `deepseek-flash`: 200 prompt tokens, 1 completion token, 201 total, recorded at 13:27:01. Actual billed cost: `UNKNOWN`. This prewarm preceded v7g installation and does not validate v7g. |

A separate pre-game command mistake occurred at 13:19:59: invoking `jiuwenswarm-agentserver.exe --help` initialized the user default JiuwenSwarm skill registry. It updated `C:\Users\Yukis\.jiuwenswarm\agent\workspace\skills\skills_state.json`; the prior bytes were unavailable, so no restoration was attempted. The default instance and `career_emu` both reported stopped after the process exited. Captured default-instance logs showed no DeepSeek, API request, completion, or token-usage markers. The exact post-initialization state and log snapshots remain local under the evidence directory below.

## Plan Deviations

- The `jiuwenswarm-agentserver.exe --help` command was mistakenly treated as read-only help. It initialized the separate user-default Skill registry. The exact post-state and nearby logs were preserved; no cleanup or restoration was attempted without a prior-state snapshot.
- After the authorized `career_emu` lifecycle was stopped, the service-start log audit established that its one completion was automatic startup prewarm and that `new_game` mentions were resource registration. The service lifecycle has already been consumed, so no restart or Runner play was attempted.

## Score and Career Trajectory

- No Runner score report, `events-*.jsonl`, or `transcript-*.log` was generated.
- Quantitative score, competition partial score, survival months, grade, completion/elimination, terminal reason, final Level/Wealth/Skill/Network/Output/Health/Dignity: `NOT_RUN` / unavailable, not zero.
- M1/M3/M6/M9/M12/M18/M24/M36/M48 checkpoints, reviews, promotions, monthly trajectory, Review Plan, MODE, Wealth handling, Main choices, Energy, Story deliberation, Risk behavior, public-hint discipline, and Skill recovery: `NOT_RUN`.
- Candidate runtime preflight, action schema, CTRL integrity, fresh-observe discipline, and compression recovery: `NOT_EXERCISED`.

## Promotion Progression

- Promotion months, level transitions, formal-review results, and no-advance results: `NOT_RUN`.
- M6/M12/M18/M24/M36/M48 review checkpoints: `NOT_RUN`.

## Strategy Behavior

- G stability/changes, P transitions and triggers, Wealth response, quarterly Main choices, Energy intents/actions, Story deliberation, public-hint discipline, hidden-inference violations, and Risk behavior: `NOT_RUN`.

## Runtime Audit

The service loaded and registered the Career Emulator MCP server and its tools, but logs contain no actual game-tool invocation. One automatic prewarm completion occurred during service startup; no v7g submission was installed and no gameplay strategy was exercised. Therefore the runtime and strategy questions in S07-33 remain unanswered.

The service startup CLI emitted repeated GBK encoding errors for Unicode status symbols and ultimately returned exit code `1`, despite the manager showing `running`. The service was gracefully stopped once. Because this task authorizes only one service lifecycle, no second start was attempted after that stop.

## Raw Local Evidence

Output directory: `D:\CS\CareerSim\.local\runtime\s07-33-v7g-run1\` (`.local` only; raw files are not committed).

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| Service start stdout/stderr | 221,656 | `09dd07622acc522005dde5342410612e121448c7752edce4570cf994e8e3655f` |
| Service stop stdout/stderr | 495 | `fef46d73a01142b56c6acf4b4009f1b0f64f9a6baac396c9661fc73c53cb43ed` |
| `career-emu-agent_server.log` snapshot | 6,504,655 | `af9e614b6b923ec4ef78e72b3c945daa3af291e4db57d5b7b4d1915ba7dd9b68` |
| `career-emu-full.log` snapshot | 6,950,111 | `8a93a5d503707cf45ce8f20c47a39552b8dbb3c4d90711d95a985a58fbcb05b4` |
| `career-emu-gateway.log` snapshot | 445,456 | `28e30b1b837e73446528bfa7b96999c25635316c4b68ba8526e87b47128b201f` |
| `career-emu-ws-dev.log` snapshot | 941 | `3de64074f809a18d9646f99e96cfc80a462450d19894c1b1c9b88c70aced382c` |
| `default-full.log` snapshot | 7,964 | `d5d4ded68521283ff577fb29b5b9f4646e733cede18f3cfebbf4c275538aa01b` |
| `default-gateway.log` snapshot | 7,964 | `d5d4ded68521283ff577fb29b5b9f4646e733cede18f3cfebbf4c275538aa01b` |
| `default-full-after-careeremu-stop.log` | 8,346 | `17875fc6342188f6fcd02ec39a2d58d03c79eeaef6ec4373bbf8f8b67518c493` |
| `default-gateway-after-careeremu-stop.log` | 8,346 | `17875fc6342188f6fcd02ec39a2d58d03c79eeaef6ec4373bbf8f8b67518c493` |
| `default-skills_state.json` snapshot | 841 | `a5b6bc723bea8483ba187984a36493ba35ca56633d6913767bc0cb0c156833c6` |

Snapshots are under `D:\CS\CareerSim\.local\runtime\s07-33-v7g-run1\incident\`. Runner events, transcript, and score report: `NOT_CREATED`. The shared Career Emulator DB was not opened, queried, parsed, or hashed.

## Validation Flags and Limitations

The current Candidate metadata remains unchanged: `provider_validated=false`, `gameplay_validated=false`, `runtime_validated=false`, `long_horizon_adherence=false`, `survival_improvement_proven=false`, `score_improvement_proven=false`, `stable_80_plus_proven=false`, `hidden_test_transfer_proven=false`, and `next_game_authorized=false`. No valid game observation was obtained, so `RUN_HISTORY.md` was not updated. `CURRENT_STATE.md` records this pre-game attempt separately.

## Interpretation

- **FACT:** v7g package identity and four Skill bytes passed; the configured `career_emu` service reached running and was gracefully stopped; one 201-token DeepSeek completion was logged during automatic prewarm; no Runner play or actual game tool call occurred; the service launcher returned `1` with GBK encoding errors.
- **INFERENCE:** the `new_game` log strings were tool/resource registration, not game starts; no CareerSim game session was created by this attempt.
- **HYPOTHESIS:** the prewarm completion is normal JiuwenSwarm startup behavior. The present evidence establishes that it occurs in this environment, but not whether every future service start will produce a completion.

This attempt proves no gameplay effect, survival or score change, causal improvement, long-horizon adherence, stable 80+, or hidden-test transfer. Return to Main for review; do not start another service lifecycle or game under this Task.

Final handoff: `RETURN_TO_MAIN_AFTER_V7G_ONE_GAME` (no game was actually started in this attempt).
