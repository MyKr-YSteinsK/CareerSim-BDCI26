# S06-24｜v6 Run #1 Runtime Validation

## Identity and boundary

- Repository/base before run: `main == origin/main == 1114a04b75548cf52f030d123564e527060fc061`; repository was clean.
- Candidate: `candidate-v6-auditable-control-loop`.
- Runtime manifest SHA-256: `bcf459da811f55b8a26a76d2ee6e93da10deb4b720cc732d19a3ce12d8fa2985`; instruction SHA-256: `7131bbd652452c71571f1ab99451f210e6e52601e9d66144d3d665337b4eb33c`.
- Skill blobs: risk-review `a6a09a4894caaca15f4aa5005911bad3b399b464`; rolling-planning `138a2a9ef7626e892b36b0e8e29a934a90709228`; structured-state-board `0afafcfbd2e8d87e5a9cc9944be0cd639c3b61bd`.
- Frozen Runner: `f61c738c72e51b77298cc1c14c7c6ebf4b6c527d`; installed versions: jiuwenswarm `0.2.4b3`, openjiuwen `0.1.16.post2`, career-emulator `1.0.1`, career-emulator-bdci26 `1.0.0`.
- Preflight passed: existing installed v6 identity was reused without reinstall; exactly three participant Skills were enabled, retrieval was disabled and react mode was `all`; required five CareerSim MCP tools were registered and the shared runtime was exclusive. No provider ping or test prompt was sent.
- No policy, runtime manifest, or Skill was changed after observing this run.

## Run outcome

`quantitative_score: 75.29` · `competition_partial_score: 52.70` · `survival_months: 48` · `grade: A`

- Classification: `VALID_48M_COMPLETION`; Runner exit code 0, `completed=true`.
- Play began `2026-09-25 17:44:17.491 +08:00`; the first terminal score timestamp was `18:10:53.348 +08:00` (about 26m36s). One fresh `new_game`; no second game or continuation.
- Drive session: `career-sim-runner-15004a268a02`; game session: `7b59b85ad19b4597927cf50fc716f9ac`; output identity: `20260925T094419Z`.
- The final fresh observe showed M49/Q17, the administrative post-completion state; the scored game outcome is 48 months.
- Promotions observed: L1→L2 at M6, L2→L3 at M12, L3→L4 at M18, L4→L5 at M36, and L5→L6 at M48.

| Dimension | Raw | Weighted score |
|---|---:|---:|
| Level | 6 | 18.00 |
| Wealth | 39.5 | 9.88 |
| Resilience | 17 | 12.75 |
| Skill | 142 | 15.00 |
| Risk Control | 0 | 10.00 |
| Network | 58 | 9.67 |

Quarterly main actions: `申请关键项目` 14/16 (M3, M6, M9, M12, M15, M18, M21, M24, M30, M33, M36, M39, M42, M48); `低调避险` 2/16 (M27, M45).

Energy actions (41): `准备汇报材料` 15, `健康恢复` 10, `人脉维护` 8, `高强度工作` 5, `处理历史埋雷` 2, `心理修复` 1.

## Provider usage and runtime lifecycle

- Plan24 startup overhead: 1 successful DeepSeek `deepseek-flash` response, input/output/total `200/1/201`; no independent provider ping or test prompt.
- Runner gameplay aggregate: input `40,372,074`, output `247,309`, total `40,619,383`; reported cache tokens `39,865,088`; by-model `deepseek-flash`. Runner/provider reported cost `0.0`; actual billed cost is **UNKNOWN**, not zero.
- Two additional successful non-streaming responses were produced by JiuwenSwarm `CurrentRoundCompressor`, outside the Runner gameplay aggregate. Compression #1: input `161,005`, output `2,724`, total `163,729`; compression #2: input `160,576`, output `3,798`, total `164,374`; combined `321,581/6,522/328,103`, cache hit `318,080`, miss `3,501`; model `deepseek-flash`. The compressor responses contained `<coverage_check>` and `<state_snapshot>` sections. This usage remains separate from Runner gameplay accounting; actual billed cost is UNKNOWN.
- Observed during Plan24: startup + Runner aggregate + those two responses = input `40,693,855`, output `253,832`, total `40,947,687`. Including the separately observed S06-23 setup response (`200/1/201`) in the pre-game setup history gives cumulative `40,694,055/253,833/40,947,888`. No actual cost is available.
- Service lifecycle: one start, one official graceful stop, zero restart retries. Final service state was stopped; ports 19092, 20000, 20001, and 6173 were free.

## Runtime adherence audit

- Tool calls, deduplicated by tool-call ID: `new_game=1`, `observe=204`, `take_action attempts=203` (202 successful state-changing calls and one malformed unsuccessful attempt), `check_latest_logs=3`, `show_employee_handbook=1`, `read_file=3`. All observations used the same game session.
- The malformed attempt at event sequence 1017 sent `choice=6,7,3` during an Energy multi-selection. The tool rejected it as invalid arguments JSON before executing the action; it did not mutate game state.
- All three Skill bodies were read once before the first action. Two `CurrentRoundCompressor` epochs then occurred (triggered at 17:52:56 and 18:01:32; completed at 17:53:09 and 18:01:50), each producing a compressed state snapshot. No three-Skill reread followed either snapshot. Under the S06-25 recovery definition, this is a missed context-recovery rebuild.
- Fresh-state discipline: all 202 successful state-changing `take_action` calls were followed by a fresh observe before the next successful state-changing action. One additional malformed attempt changed no game state. The 204 observations include the initial observe.
- Legacy Trace/S02/S03 marker or file-reference patterns were not observed.
- CTRL audit for original v6: 418 marker-shaped transcript occurrences (416 `CTRL:`-style fields and 2 `CTRL marker:` forms) versus 203 attempts. Flattened transcript evidence has no reliable model-turn IDs, so pairs, missing/orphan/duplicate markers, coverage, and same-turn/X gating cannot be certified. These free-text occurrences are not a canonical action-linked audit surface; S06-25 retires that surface. Raw field text included N=2, Q=63, H=0, R=20, P=0, C=0 occurrences; counts are transcript occurrences, not unique decisions.
- N: new-session marker text observed. Q: quarterly marker text occurred, but duplicates make exact checkpoint-to-quarter coverage ambiguous. H: **MISSED**—semiannual review/promotion points occurred without the required H marker. R: review-reset marker text appeared, but exact pairing is ambiguous. P: `STALLED` was **NOT_TRIGGERED**; the strict two-comparable-checkpoint condition was not established. C marker text was absent; separately, two actual compression/recovery epochs occurred and the three Skills were not reread afterward.
- At M6, public Health fell 6→5→4 alongside a health warning; the transcript recognized `Risk Budget=TIGHT`. After Health recovered to 6 and the warning cleared, it later used `AVAILABLE`. This is descriptive evidence only.
- One M13 health-risk choice caused a genuine `RECONSIDER`: a lower-load legal alternative was compared and selected, then the chosen candidate was gated again. Marker text was duplicated in the transcript. No causal benefit is inferred.
- A repeated `准备汇报材料` choice showed no observed Output increase; the agent noted saturation and selected another Energy action. This does not establish the strict two-checkpoint stall rule.
- Ordinary story decisions repeatedly reopened deliberation without new public evidence, including examples at M1 and M48; the bounded top-two/stop rule was not reliably followed.
- Board fact summaries/scans recurred through the run; low-frequency-only Board behavior is not supported by this transcript.

**Runtime correctness: `RUNTIME_ADHERENCE_FAIL`** (missed H trigger and visibly unbounded ordinary-event reconsideration; CTRL/action verification also remains ambiguous).
**Gameplay observation: `VALID_48M_COMPLETION`**. These classifications are independent: this was valid gameplay evidence despite runtime-contract failures.

## Raw evidence (local, not committed)

Output directory: `D:\CS\CareerSim\.career_sim_runner\career_emu\outputs\local-s06-adaptive-controller\20260925T094419Z\`

| File | Bytes | SHA-256 |
|---|---:|---|
| `events-20260925T094419Z.jsonl` | 2,061,570 | `2CCE87EB6AFD8AEA5A9651F75621AE7C2B303E8C00C7F2AC417DC65C030371D8` |
| `transcript-20260925T094419Z.log` | 822,693 | `13BD4DE5FC9B9A25B564072125CB0D373B92402CF5F28D59E4930B96A741FDA0` |
| `score_report.json` (current local copy) | 2,722 | `277809FBDAE10D2242FD6A3ECBEE3731C7ECE2BE1B5D7E8222B4115C60517D37` |

Service logs remain local under `D:\CS\CareerSim\.local\runtime\s06-plan24-v6-run1\`: stdout 2,543,004 bytes, SHA-256 `C9B804FC946402C8591FF34AE733A3063BEEE72A92547F737A3A8047F120CE28`; stderr 1,814,471 bytes, SHA-256 `A400FCACAF25043A581A566C13A21451877163EAFE2BC5B14C4D20A4BC4361A0`.

The score report was observed first with a nonempty matching session ID (2,754 bytes; SHA-256 `A8BC9428DB13EE7F4BF272F73861A2CFC13BDC4EED6DABA597494A8439F8A01E`), then its local file changed before service stop (current report has an empty `session_id`, updated `scored_at`, and unchanged score fields). The cause is **UNKNOWN**. Runner output and game events independently identify the session; raw evidence was not restored or rewritten.

## Candidate flags and limits

- `gameplay_validated=true`, `provider_validated=true` record that a real game completed and gameplay provider responses succeeded.
- `survival_improvement_proven=false`, `score_improvement_proven=false`, `long_horizon_adherence=false`, `stable_80_plus_proven=false`, `hidden_test_transfer_proven=false`, `next_game_authorized=false`.
- One run does not establish causality, improvement, stable 80+, or hidden-test transfer. No post-hoc policy change was made during S06-24; S06-25 records the separate v6b correctness patch.
- Target remains `STABLE_QUANTITATIVE_80_PLUS`; it is not achieved. S06 remains in progress and Design Freeze remains active.
- Next decision belongs to Main: `RETURN_TO_MAIN_FOR_BOUNDED_CORRECTNESS_DECISION`. The Plan24 one-game authorization is consumed; this record does not authorize another game.
- Proposed later-stage idea only: `BATCH_EXPLORATION_AND_POLICY_PROBING` (E1 frozen-policy repeatability, E2 controlled ablations, E3 exploration probes); it is not authorized or started here.

## Execution issues

Three local-only diagnostic attempts failed on event-schema/report-format assumptions or Python syntax. They caused no provider, service, game, or other live action. The corrected event-sequence audit passed.
