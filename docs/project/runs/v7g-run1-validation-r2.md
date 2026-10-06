# S07-33R — v7g Run #1 Validation (Readiness-Based Recovery)

## Result

- Gameplay: `VALID_48M_COMPLETION` — one fresh game completed 48 months.
- Runtime: `RUNTIME_ADHERENCE_FAIL` — action schema and observe sequencing passed, but context-compression recovery was not evidenced.
- Strategy: `PROMOTION_FIRST_ADHERENCE_FAIL` — multiple ordinary-event Primary Gap changes and numeric HiddenRisk reasoning conflict with the candidate's public-evidence contract.
- Candidate remains `candidate-v7g-compact-skill-contracts`; no prompt, Skill, strategy, Runner, provider configuration, dependency, or dataset change was made during or after play.
- This is one descriptive observation. It does not prove causal score/survival improvement, stable 80+, or hidden-test transfer. `next_game_authorized=false`.

## Identity and preflight

- Task: S07-33R; launch base `main@f3e5db32f3821480627316393c834cf1ec88b240`, equal to `origin/main`; worktree was clean.
- Candidate: `candidate-v7g-compact-skill-contracts`; parent `candidate-v7f-promotion-first-survival-floor`; metadata status remains `STATIC_IMPLEMENTED_NOT_RUNTIME_VALIDATED`.
- Frozen Runner Git blob: `f61c738c72e51b77298cc1c14c7c6ebf4b6c527d`.
- Runtime manifest SHA-256: `1633dbb9e7948131c91a075d340930c2536c76a04538d13360603631e45c47d6`.
- Instruction SHA-256: `8ba742657e8ddaf521d6b2acab82f7f8655eac81bc43015580321aee455037ac`.
- Skill Git blobs: Board `ec751e0b03c49d13641513eaa2f7c8bb00faa11`; Planning `11c2b09a684bd9ac9d3b676dd690ea56337c5fcb`; Delivery `c40a4f8487d99b76154894d859d6d81a6fcd8dd4`; Risk `d2c6e14c8e6ae3d3ebce12c43815f3a45cbfae6a`.
- The intended provider remained DeepSeek `deepseek-flash` at `api.deepseek.com`; credential presence was checked without displaying its value. The Dev dataset and frozen root `.venv` Python were present. S07-32's 11 targeted static checks and package/frontmatter checks were reused; Candidate bytes and dependencies had not drifted, so the static suite was not rerun.
- Canonical helper built `.local/runtime/s07-33r-v7g-run1/submission`. Runner submission validation passed: manifest identity matched the Candidate, `mode=agent`, exactly four Skills, and bundled bytes matched repository files. No separate install was performed; install/reload occurred through the successful Runner play path.
- At S07-33R run time, the active instance configuration supplied DB path `D:\CS\CareerSim-s03-02-risk-review\.career_sim_runner\career_emu\career_emulator.sqlite3`, rather than the root Runner default. That configured path was used for the run. S07-33R did not open, query, parse, or hash the DB and made no runtime configuration change. S11-11 later remediated the active configuration and retired the legacy workspace; see [the retirement record](../LOCAL_WORKSPACE_RETIREMENT.md).

## Readiness and corrected launch

- `career_emu` start was invoked once at `2026-09-28T05:52:02.7248323Z` (13:52:02.724 +08), using the previously proven `jiuwenswarm-start.exe --name career_emu all` command with a hidden background process. PID: `21088`.
- At `2026-09-28T05:52:30.7823101Z`, 28.06 seconds after launch, the manager reported `running` and all required listeners (19092, 20000, 20001, 6173) were ready. Runner play began immediately after readiness. The background launcher's own exit code was not captured (`UNKNOWN_NOT_CAPTURED`); this did not determine readiness. GBK/Unicode logging errors were present while the service remained ready.
- The service emitted its expected automatic startup prewarm: 200 input / 1 output / 201 total tokens. No independent prompt or provider test was sent. Tool-name registration text was not counted as a game-tool invocation.
- First Runner CLI attempt failed before `new_game`: its child PATH omitted the root `.venv\Scripts`, so the command could not resolve `jiuwenswarm-start`. The failure was captured and had no game-state mutation. PATH was corrected for the next child process only; the same service lifecycle then entered the one successful play. This was one pre-game command-layer correction permitted by the Plan; it was not a second game or service start.
- The Runner was invoked with the frozen root Python and the current configured DB path. The successful process began at `2026-09-28T05:54:13.7189862Z`; actual `new_game` occurred once at `2026-09-28T05:54:21.006245Z`.

## Live accounting

| Operation | Observed |
|---|---|
| `career_emu` service start / graceful stop | 1 / 1. Stop returned 0 at 2026-09-28 14:19:26.849 +08; final manager status was `stopped`, and required listeners were released. No restart. |
| Runner `play` command attempts | 2 CLI attempts: one pre-game PATH-resolution failure and one successful play path. The failure preceded install and `new_game`; one actual game was started. |
| Install/reload | 0 separate install commands; Runner play performed its normal install/reload. |
| Actual `new_game` / game sessions | 1 / 1. Game session `d4464a311c924e73b9e23eebd6f71f6d`; drive session `career-sim-runner-7c24f7aa9d6f`. No resume or second game. |
| `observe` / `take_action` | 196 / 195. All 195 actions succeeded; 0 schema rejects, missing choices, multi-choice, non-integer, or invalid-choice submissions. |
| Handbook / Skill calls | 1 handbook; each of the four Skills was read once before the first observe/action. No post-compression Skill reread was recorded. Latest-log calls were not reported in the event summary. |
| Context compression | 2 `CurrentRoundCompressor` completions. Required four-Skill and state/plan recovery was not evidenced. |
| Separate provider prompt/test | 0. No standalone smoke game. |

### Token usage

| Source | Input | Output | Total |
|---|---:|---:|---:|
| Automatic startup prewarm | 200 | 1 | 201 |
| Runner gameplay aggregate (`deepseek-flash`) | 35,703,176 | 219,824 | 35,923,000 |
| `CurrentRoundCompressor` #1 | 156,766 | 6,670 | 163,436 |
| `CurrentRoundCompressor` #2 | 160,830 | 3,658 | 164,488 |
| Total observed across the lifecycle | 36,020,972 | 230,153 | 36,251,125 |

Runner reported 35,243,392 cache tokens (98.7% hit rate) and `total_cost=0.0`; actual billed cost is `UNKNOWN`. The compressor/prewarm rows are separate from the Runner aggregate. Runner process start to score report was approximately 24m40s.

## Outcome and score

- Score report time: `2026-09-28T06:18:53.966938Z` (14:18:53.966 +08); Runner play exit code `0`; `completed=true`.
- Quantitative score `54.52`; competition partial `38.17`; survival `48` months; grade `C`; terminal reason: “Completed the 48-month simulation.” The terminal administrative observe was at M49 after the completed 48-month game and is not an extra game month.
- Final score dimensions (raw / normalized / weighted): Level `5 / 50 / 15.00`; Wealth `19.1 / 23.88 / 4.78`; Resilience `16 / 80 / 12.00`; Skill `102 / 85 / 12.75`; Risk Control `6 / 40 / 4.00`; Network `36 / 60 / 6.00`. The reported total 54.52 is authoritative; rounded component weights need not sum exactly to it.
- Public terminal state at M49: L5, Health 6, Dignity 10, Skill 102, Network 36, Output 32, Wealth 19, Energy 0; `alive=false`, `failed=true` accompanied the explicit completed-game reason. Score report survival/completion fields govern the outcome classification.

## Public trajectory

Tuple is `Level / Health / Dignity / Skill / Network / Output / Wealth / Energy`; values are participant-visible `observe` results. `duration_in_level` was not included in this compact extraction.

| Month | Public state tuple | Note |
|---:|---|---|
| M1 | L1 / 5 / 8 / 3 / 1 / -1 / 1 / 3 | Initial state |
| M3 | L1 / 5 / 10 / 8 / 3 / 0 / 1 / 0 | |
| M6 | L1 / 5 / 9 / 9 / 3 / 3 / 2 / 0 | C review; no promotion |
| M9 | L1 / 5 / 10 / 9 / 3 / 3 / 3 / 0 | |
| M12 | L2 / 4 / 10 / 10 / 6 / 6 / 3 / 0 | Promoted L1→L2 |
| M18 | L3 / 7 / 10 / 26 / 6 / 7 / 6 / 0 | Promoted L2→L3 |
| M24 | L3 / 8 / 10 / 41 / 19 / 16 / 7 / 0 | |
| M30 | L4 / 10 / 10 / 45 / 19 / 18 / 2 / 0 | Promoted L3→L4; Wealth near its observed low |
| M36 | L4 / 8 / 9 / 63 / 35 / 25 / 7 / 0 | |
| M42 | L4 / 9 / 10 / 76 / 36 / 26 / 11 / 0 | |
| M48 | L5 / 6 / 10 / 101 / 35 / 30 / 18 / 0 | Promoted L4→L5 |
| M49 | L5 / 6 / 10 / 102 / 36 / 32 / 19 / 0 | Administrative post-completion observe |

## Reviews and promotions

| Month | Public review | Promotion / feedback |
|---:|---|---|
| M6 | C, lower | No advance; asked for clearer results. |
| M12 | C again | L1→L2; feedback continued to distinguish being busy from winning. |
| M18 | B, improved | L2→L3; transcript/report noted social friction following rapid advancement. |
| M24 | B (+0.25) | No advance; similar clearer-result feedback. |
| M30 | B (+0.25) | L3→L4; leader feedback still challenged the result signal. |
| M36 | B (+0.35) | No advance; met expectations, without a standout. |
| M42 | B (+0.35) | No advance; remained under observation and was asked for clearer results. |
| M48 | A (+1.05) | L4→L5; feedback emphasized Output and relationships. |

Promotion months observed: M12, M18, M30, M48. These are run observations, not inferred thresholds.

## Strategy audit

### Review Plan / Primary Gap (`G`)

- The initial Objective/Gap/checkpoint was present. The event record contains 19 G-marker changes, including the initial `?` to a clearer-results gap after M6.
- Several later changes to health/crisis-stop directions occurred around ordinary Story/Energy events (including M21, M23, M28, M29, M31, M33, M36, M42, M45) and often reverted soon afterward. `危机止损与恢复` recurred without a formal review immediately preceding each change. The compact audit does not assign a precise “unsupported” count to all 19 transitions; the ordinary-event changes are nevertheless inconsistent with the candidate's review/evidence-gated revision rule.
- The repeated marker churn weakens evidence that a stable Review Plan was preserved. Formal review and ordinary-event changes are distinguishable in the event stream; no strategy patch was made.

### Mode (`P`) and quarterly Main actions

- All 16/16 quarterly Main actions, Q1 M3 through Q16 M48, were `申请关键项目` (apply for key projects), a broad-growth/visible-ownership choice. No low-profile Main action was recorded. This frequency alone does not establish benefit.
- Action notes recorded P=`A` 162 times and P=`S` 33 times, with 40 A↔S transitions. P was marked S at M30 and A otherwise in the summarized quarter markers. Some shifts may reflect material Health/risk evidence; the audit does not claim every transition was unsupported. The per-transition public-trigger link was not consistently reconstructable from compact metadata.

### Wealth response

- Public Wealth was positive in every checkpoint; the lowest observed public value was 1 at M1. It fell from 7 at M24 to 2 at M30, then recovered to 19 at the terminal public state (score raw Wealth 19.1). No non-positive public Wealth was observed.
- The agent kept choosing key projects through the dip. It also used recovery/crisis Gap markers around some ordinary events. The run does not isolate which choices caused Wealth changes or prove a reliable recovery policy.

### Energy choices

There were 34 recorded Energy choices: 11 high-intensity work, 11 report preparation, 8 health recovery, 3 historical-risk cleanup, and 1 network maintenance.

| Quarter | Month | Recorded Energy choices |
|---|---:|---|
| Q1 | M3 | Historical-risk cleanup; health recovery |
| Q2 | M6 | High-intensity work; health recovery |
| Q3 | M9 | High-intensity work; report preparation |
| Q4 | M12 | Historical-risk cleanup; report preparation |
| Q5 | M15 | High-intensity work; report preparation |
| Q6 | M18 | High-intensity work; network maintenance |
| Q7 | M21 | Two health recovery choices; report preparation |
| Q8 | M24 | High-intensity work; report preparation |
| Q9 | M27 | High-intensity work; report preparation |
| Q10 | M30 | Historical-risk cleanup; report preparation |
| Q11 | M33 | High-intensity work; report preparation |
| Q12 | M36 | High-intensity work; health recovery |
| Q13 | M39 | High-intensity work; report preparation |
| Q14 | M42 | Two health recovery choices; report preparation |
| Q15 | M45 | High-intensity work; health recovery |
| Q16 | M48 | High-intensity work; report preparation |

The compact audit does not show a documented quarter-long intent/replan reason for every choice. The G changes around ordinary events are noted above; no unsupported fixed Energy rule is inferred.

### Story deliberation and Risk

- Transcript marker counts: 3,732 `Hmm`, 335 occurrences of “let me reconsider”, and 348 total `reconsider` occurrences. These counts indicate repeated reopening/verbose deliberation; no long reasoning text is reproduced here. Classification: `PATHOLOGICAL` under this Task's bounded-story audit categories. This was not repeated tool submission: action count remained one successful call per action and there were no schema rejects.
- CTRL marker checks: all 195 action notes had exactly one valid CTRL prefix; `R=PASS` 170 times and `R=ALLOW` 25 times. No malformed CTRL note was observed.
- The raw `observe` result included a `choices.status_updates` field named `HiddenRisk`, while participant-facing choice descriptions were qualitative. Twelve action rationales used exact numeric HiddenRisk change claims. This is the observed fact; the values are not copied into this report. It raises a public-interface/hidden-mechanic discipline concern and contributes to `PROMOTION_FIRST_ADHERENCE_FAIL`; Main should review whether that field is admissible under the public-evidence boundary.
- No causal claim is made about Risk Control score or any hidden game mechanic.

## Runtime adherence and compression recovery

- One Single Agent submitted all actions. `new_game` was event sequence 4; the four Skill calls (Board, Planning, Delivery, Risk) occurred after game start and before the first observe/action (first observe sequence 18; first action sequence 30).
- There were 196 observes and 195 successful state-changing actions. Each action was followed by a fresh observe before the next successful action. All `take_action` results were successful and schema-conforming.
- Two actual `CurrentRoundCompressor` completions were found in service logs, at approximately 14:04 and 14:13 +08. No Skill reread followed either compression: the complete Skill-tool count remained four. Fresh observations/action sequencing continued, but four-Skill reread plus Board rebuild and Delivery/Review Plan restore were not evidenced. Recovery is therefore a contract failure, not `NOT_TRIGGERED`.
- Gameplay completion and correct action schema do not override this runtime failure. `runtime_validated=false` and `long_horizon_adherence=false` remain appropriate.

## Descriptive historical comparison

Public state tuple is `Level / Health / Skill / Network / Output / Wealth`. Historical records are not paired or controlled; v1 #1 was retained as checkpoint-only evidence, and v6 as a different candidate/run. Values are descriptive only.

| Run | M6 | M12 | M18 | M24 | Terminal |
|---|---|---|---|---|---|
| v1 #1, 76.04 / 48m / A | L2/7/13/5/6/2 | L3/7/24/7/7/4 | L4/10/44/19/16/6 | L4/8/63/36/26/10 | M48 L6; promotions M6/M12/M18/M36/M48 |
| v6 #1, 75.29 / 48m / A | L2/6/11/3/5/3 | L3/5/23/8/7/4 | L4/9/38/19/17/8 | L4/8/61/30/26/11 | M48 L6; promotions M6/M12/M18/M36/M48 |
| v7d #1, 17.02 / 15m / E | L1; C/no advance | Later comparable milestone not retained before M15 termination | Ended before M18 | Ended | M15 L1, no promotion; Wealth 0 |
| v7g #1, 54.52 / 48m / C | L1/5/9/3/3/2 | L2/4/10/6/6/3 | L3/7/26/6/7/6 | L3/8/41/19/16/7 | M48 L5; promotions M12/M18/M30/M48 |

The v7g run reached 48 months but ended below the two selected high-score references on quantitative score, terminal Level, Output, and Wealth. The action/review timelines differ and the runs are unseeded; this is not evidence that any single strategy choice caused the difference.

## Candidate validation flags

| Flag | Value after this run | Basis |
|---|---:|---|
| `provider_validated` | `true` | Real DeepSeek responses during the fresh game |
| `gameplay_validated` | `true` | One fresh game completed naturally at 48 months |
| `runtime_validated` | `false` | Compression recovery contract failed |
| `long_horizon_adherence` | `false` | Requires 48m plus Runtime PASS and Strategy PASS |
| `survival_improvement_proven` | `false` | One unpaired run cannot prove improvement |
| `score_improvement_proven` | `false` | One unpaired run cannot prove improvement |
| `stable_80_plus_proven` | `false` | Not achieved or established |
| `hidden_test_transfer_proven` | `false` | Not tested |
| `next_game_authorized` | `false` | This one-game authorization is consumed; Main review required |

Candidate identity, status, manifest, instruction, and Skills remain unchanged.

## Raw local evidence (not committed)

Run output directory: `D:\CS\CareerSim\.career_sim_runner\career_emu\outputs\local-s06-adaptive-controller\20260928T055416Z\`.

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| `events-20260928T055416Z.jsonl` | 1,903,318 | `73cb4de9f2568e343be252630a64dbef289e92aec121bae07ef8fbd3a6cff3c4` |
| `transcript-20260928T055416Z.log` | 641,028 | `d3f879a9ecc01c845bac70468bbceba8634dbfc28826da445e8b2e73e79f46b7` |
| `score_report.json` | 2,755 | `52ee2bb53653c805ce724137087dc395883ae8ee0d03afab4f969e1bf173fffe` |

Task-local runtime evidence directory: `D:\CS\CareerSim\.local\runtime\s07-33r-v7g-run1\`.

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| Service start stdout | 1,185,318 | `1c611c5a313f2652eec92760bf76946d5d6056306262dd8bbdff34b2eb007797` |
| Service start stderr | 2,739,783 | `3c7109a609e015ee15086a69045d4aefb60ff3e2a255f16236f2d0367d7120a2` |
| Service stop log | 495 | `dd54fb06d532a3f4df362ea3e048622d8e4d4757814f0fde6821eec71a8da9dc` |
| Failed pre-game Runner stdout | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| Failed pre-game Runner stderr | 1,364 | `37c0c473d4e0f8142ea2693de59a44f5a816c15c2bb1f5aa20893c9df80f5c57` |
| Successful Runner stdout | 340,299 | `46520c105ceaab0480f090a2ca18e3b29f115cd972f928a5e5f719f76f390851` |
| Successful Runner stderr | 270 | `3e5cfdd5044f32c5d97177db55ad6989173055126e8d097f4cd6800b89f4c774` |

The raw transcript/events/score and service logs remain local and are retained for Main review. No raw runtime artifact, DB, `.env`, credential, or submission bundle is committed. No forensic hold was released by this Task.

## FACT / INFERENCE / HYPOTHESIS

- **FACT:** Candidate identity and all four Skill bytes matched preflight; the service became ready once; one fresh v7g game completed 48 months; score was 54.52 / 38.17 / C; 195 actions succeeded with no schema rejection; two compression epochs occurred with no subsequent Skill reread evidenced; service was gracefully stopped and verified stopped.
- **FACT:** 19 G-marker changes were observed, including ordinary-event changes; 12 rationales used numeric HiddenRisk change claims while the raw observe payload exposed a `HiddenRisk` status field. Story reconsideration markers were frequent.
- **INFERENCE:** The G churn and HiddenRisk reasoning are inconsistent with v7g's review-anchored/public-evidence strategy contract; missing post-compression Skill and plan recovery violates runtime adherence. These support the Runtime and Strategy FAIL classifications.
- **HYPOTHESIS:** A stable review-to-result plan and lower deliberation verbosity may improve future execution quality. This single unpaired game does not test that causal claim.

Final handoff: `RETURN_TO_MAIN_AFTER_V7G_S07_33R_ONE_GAME`
