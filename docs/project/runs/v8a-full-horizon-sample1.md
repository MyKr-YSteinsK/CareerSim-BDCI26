# S09-RUN07｜v8a Full-Horizon Distribution Sample #1

## Result

- Decision: `S09_RUN07_V8A_FULL_HORIZON_SAMPLE1_COMPLETE_RETURN_TO_STAGE`.
- Classification: `VALID_48M_COMPLETION`; one fresh game completed 48 survival months and ended naturally at structured Month 49.
- Candidate: `candidate-v8a-v7o-donor-core-transplant`; frozen identity gates passed. Run base and `origin/main`: `5d2358f48a89ad5a2eb16012f700449436818cec`; Runner SHA: `f61c738c72e51b77298cc1c14c7c6ebf4b6c527d`.
- Session: `258f135bc8e0459482ad7cc3be04c1ac`.
- Candidate/Skill/manifest/Runner/dependencies/retry bytes were not changed. The verified four-Skill package from `.local/runtime/s09-run06-v8a/submission` was reused for this unchanged Candidate; `max_retries=2`.
- Run window: `2026-10-01T11:39:58.310740Z`–`2026-10-01T12:51:10.411189Z` (71m12s). One service start, one Runner play, one fresh game; authorization consumed.
- Startup readiness passed on all required ports. Runner exited 0. Graceful stop exited 0, manager stopped, and ports 19092/20000/20001/6173 were free. The foreground service-start wrapper later exited 1 after a Windows GBK logging error; no restart occurred.

## Outcome and checkpoints

- Final: quantitative `72.65`; competition partial `50.86`; `48m`; grade `A`; final Level `L5`; completed=true. Final public state at M49: H10/D10/W35/S119/N54/O35/E0.
- Promotion months: M6, M12, M24, M42. This sample restores M6/M12 promotion but has no M18 promotion.
- Checkpoint rows use the last fresh public observation in each Review month. Grade and Level transitions were captured in the live checkpoint reports.

| Review | Grade | Level | Promotion | H/D/W/S/N/O |
|---|---|---|---|---|
| M6 | C | L1→L2 | Yes | 5/10/2/12/5/6 |
| M12 | B | L2→L3 | Yes | 10/10/1/22/3/5 |
| M18 | B | L3→L3 | No | 10/10/5/42/12/16 |
| M24 | B | L3→L4 | Yes | 9/10/9/45/21/19 |
| M30 | B | L4→L4 | No | 9/10/14/64/27/26 |
| M36 | B | L4→L4 | No | 9/10/19/85/35/25 |
| M42 | A | L4→L5 | Yes | 9/10/25/102/43/26 |
| M48 | B | L5→L5 | No | 10/10/34/118/54/33 |

## Runtime and behavior evidence

- 203/203 actions succeeded; 0 failed/unknown. Exact event order shows 203/203 action→fresh-observe pairs; 204 observes total, including initial observation. One `new_game`; no provider-error zero-work termination was observed.
- Marker counts: MODE A=194, S=9; Risk PASS=195, ALLOW=8; recovery field `RB=NONE` on all 203. These are emitted-marker counts, not independent semantic validation. S actions occurred during Health stabilization at M2–M6 and one M12 psychological-safety decision.
- Public resource/continuity path included M12 stress and medical leave followed by a one-week milestone delay at M13; a limited data-exposure response at M16–M17; a data-falsification/retaliation path at M28; and an M44 consent issue for AI training data, where the Agent asked for updated terms and opt-out while the emitted Risk marker was PASS.
- The action-note audit found three `HiddenRisk-1` numeric references (actions 126, 150, 152), contrary to the runtime manifest's evidence firewall. No hidden threshold or causal conclusion is inferred.
- At M36, one bounded risk-cleanup action was followed by another risk-reduction choice after fresh observations, with no distinct intervening warning visible in those action rationales. This remains a review item, not a causal finding.
- Delivery audit coverage is `0/203` accepted. All emitted `[CTRL…][DL…]` pairs are directly adjacent. The runtime manifest requires exactly one CTRL then one DL at the start and illustrates them on separate lines; it does not explicitly state whether adjacency is invalid. The current parser accepts a space or newline but rejects adjacency. Record this as an unresolved parser/format contract boundary; Delivery lifecycle semantics and overclaim status remain inconclusive.
- Runner stdout contained no explicit compression/recovery marker. Compression count, continuation sends, execution-boundary count, and Skill rereads are `UNKNOWN`; the one-pass audit lists `llm_log_not_supplied_compression_unknown` and `transcript_session_marker_unknown`. No extra live query was made.
- Usage: 43,044,759 input / 273,063 output / 43,317,822 total tokens; actual billed cost `UNKNOWN`.

## Interpretation and validation

- Descriptive comparison with v7o (`71.83 / 50.28 / 48m / A / L5`): this sample is +0.82 quantitative and +0.58 partial, with the same survival/grade/Level. This is one observation, not a causal or stable improvement claim.
- Competitive ceiling evidence: a completed 48-month A/L5 result at 72.65. Failure-floor evidence: full survival despite the public stress, resource, and compliance paths above. This does not establish a score distribution, stable performance, or hidden-test transfer.
- `gameplay_validated=true` and `provider_validated=true` apply only to this session. `runtime_validated=false` and `long_horizon_adherence=false` remain because marker/evidence-discipline findings are unresolved. Improvement, stable-80+, and transfer flags remain false. `NEXT_GAME=NOT_AUTHORIZED`; no replacement is authorized.
- No Candidate/Skill/manifest/runtime patch was made. Earlier FORENSIC_HOLDs remain unchanged.

## Evidence and hold

The exact raw events and transcript remain local, together with the original score report, reconstructed Runner receipt, one-pass summary, and stdout. Runner did not emit a separate result JSON; `runner-result.json` was reconstructed from the exact Runner stdout and records that fact.

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| `D:\CS\CareerSim\.career_sim_runner\career_emu\outputs\local-s06-adaptive-controller\20261001T114001Z\events-20261001T114001Z.jsonl` | 2,054,860 | `977f19aa89dbc12d4c1482ceff440ca98d28946737632e9c547b7d04dedb095d` |
| `D:\CS\CareerSim\.career_sim_runner\career_emu\outputs\local-s06-adaptive-controller\20261001T114001Z\transcript-20261001T114001Z.log` | 844,896 | `d5217f33c10c5c303b7048e6e263ea8041ad42d7288393a56fa577a73e28192d` |
| `D:\CS\CareerSim\.career_sim_runner\career_emu\outputs\local-s06-adaptive-controller\20261001T114001Z\score_report.json` | 2,750 | `5b3057030887109b0588b0b101a12616b40e806b5c8625b1931cba2840d59dff` |
| `.local/runtime/s09-run07-v8a/runner-result.json` | 446 | `7e7bdc810920ab862299cbee4e67b2573bbc64aeeda747c1b3fcc9e4d12ac26d` |
| `.local/runtime/s09-run07-v8a/post_run_summary.json` | 195,716 | `853b384a3e3084cce2c19d77c1d086b2ae4775e144fd66c607b2f9da3c87bc7c` |

`FORENSIC_HOLD=ACTIVE`: retain the listed exact run artifacts and the local Run07 stdout/receipt for Stage/Main review of the Delivery separator boundary, numeric HiddenRisk references, and M36 repeated risk response. Run window is above; ownership is the S09 Stage/Main review. Release only after independent review accepts the limits and confirms raw evidence is no longer required. No evidence archive was created from the unscanned raw logs.

`S09_RUN07_GAME_AUTHORIZATION=CONSUMED` · `NEXT_GAME=NOT_AUTHORIZED` · `NO_REPLACEMENT_RUN_AUTHORIZED`.
