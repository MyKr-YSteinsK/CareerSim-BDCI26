# S09-RUN10 — v9a first full-horizon validation

## Identity and boundary

- Status: Complete; `IN_FLIGHT_EVIDENCE` on `codex/s09-14-v9a-static`, not merged main evidence.
- Candidate/execution: `candidate-v9a-adaptive-opportunity-capture` at `1cc20d7a09b8ac8e34c963ae1016f64e25d99d00`; parent v8a; main submission freeze `6a4037fdf2b75c105cfe0b40b93ea68d3dd0a6f3`.
- Frozen delta confirmed at preflight: `ADAPTIVE_OPPORTUNITY_CAPTURE_WITH_BOUNDED_UNTESTED_PROBE`. Protected Board/Delivery/Risk bytes and runtime instruction unchanged; Runner `f61c738c72e51b77298cc1c14c7c6ebf4b6c527d`. Reused 38 static PASS; no tests rerun, no Candidate/Skill/manifest/retry/Runner patch or validation-flag update.
- Preflight clean, CLI/PATH prerequisite PASS, retry=2; service readiness PASS in 106.438s within 120s. Service start/play/fresh game/stop each 1; no replacement, continue, manual intervention or provider probe.
- Interactive stdout progress: preflight/session start, all eight formal checkpoints, promotions, public warnings and MODE transitions reported; reporting extra queries=0. No censor.

## Outcome

`VALID_48M_COMPLETION`: **68.40 / 47.88 / 48m / B / L5**. Structured final observe reports completed=true, outcome=completed; engine advances its displayed month to49 for the ending. End-state public H8/D10/W32/S115/N51/O38, Energy0.

| Review | Grade | Level | Promotion | Public H/D/W/S/N/O |
|---|---|---|---|---|
| M6 | C | L1→L2 | yes | 3/10/2/9/3/3 |
| M12 | B | L2→L3 | yes | 5/9/2/21/4/5 |
| M18 | B | L3 | no | 6/10/5/38/19/12 |
| M24 | B | L3→L4 | yes | 9/10/8/42/19/16 |
| M30 | B | L4 | no | 9/10/13/62/35/20 |
| M36 | B | L4 | no | 2/10/18/84/36/24 |
| M42 | A | L4→L5 | yes | 10/10/27/93/34/24 |
| M48 | B | L5 | no | 7/10/31/111/48/38 |

Promotions=M6/M12/M24/M42. MODE immediately before each checkpoint=A; RECOVERY enum not exposed, UNKNOWN. M36/M48 subsequent Story decisions entered S. MODE counts A180/S21 (10.45% S), not a semantic correctness verdict.

## Probe evidence and decision

See [compact public action pairs](v9a-run10-probe-evidence.json), linked by exact events seq and action index. All selected trace responses are local numeric outcomes, not hidden-cap evidence.

- `probe_eligible_count`, `probe_compared_count`, `probe_selected_count`, probe GAIN/NO_GAIN/UNKNOWN counts, `probe_blocked_by_binding_constraint_count` and `consecutive_probe_violations`: **UNKNOWN**. Confirmed qualifying eligible/comparison/selection traces=0; observed confirmed probe chains=0. This does not prove zero opportunities or satisfy a semantic zero-violation guarantee.
- Clean Energy NO_GAIN examples: a38/M9 and a88/M21 preparation; a135/M33 high-intensity work; a149/M36 and a160/M39 preparation; a162/M39 networking; a186/M45 preparation. Distinct Level/context/family responses remain separate.
- a49/M12 preparation gained O5→6 after L2→L3. a173/M42 says “试探结算”, preparation gains O26→27 after L4→L5; no fresh current-Level stalled path is established as its trigger. It is ordinary trial/response evidence, not a confirmed qualifying v9a probe. Its comparison favors preparation over high-intensity work; claimed immediate displacement is that ordinary growth alternative, not an inferred counterfactual.
- a186/M45 preparation has O38→38; following health recovery, a188 networking gains N41→42. This supports a local responsive alternative, not proof of an untested-probe selection. M39 networking instead had N36→36.
- Missing full five-condition eligibility/ranking evidence and malformed Delivery markers prevent total opportunity counts. Ordinary comparisons and untested options alone do not prove the new delta. No explicit qualifying bounded-probe comparison/selection found in action notes or transcript. Overall: `QUALIFYING_DELTA_EXECUTION_NOT_ESTABLISHED`; neither efficacy nor ineffectiveness is demonstrated.

Score-band interpretation=`V9A_FIRST_LIVE_MIXED_SIGNAL`. Delta exercise is inconclusive rather than proven never eligible. Decision=`S09_RUN10_V9A_FIRST_LIVE_MIXED_SIGNAL_RETURN_TO_STAGE`; Stage should review this evidence limitation before authorizing another sample. No patch/re-run in this task.

## Runtime and correctness limits

- 201 actions: success201/fail0/unknown0; observes202; action→fresh-observe201/201. CTRL valid201/201 establishes marker consistency, not full decision semantics.
- Input40,020,261/output207,487/total40,227,748 tokens as recorded by exact score report; actual billed cost UNKNOWN. Play wall time1,393.984s (23m13.984s). Compression/recovery count UNKNOWN; no cumulative provider log queried or supplied.
- Notes numeric HiddenRisk references2; transcript textual matches25 (includes repetition, not25 independent semantic violations). Internal numeric values excluded from compact evidence/strategy attribution. Transcript also contains “Skill（已100疑似封顶）” at the M43 weekend choice, contradicted by later public S101 and S115; record as world-model concern, no causal score attribution.
- Delivery markers present201 but parser-valid0: `checkpoint=NOT_NEAR` does not match the current parser pattern. Lifecycle therefore `NOT_OBSERVED`; do not interpret all NONE notes as proof of no binding Delivery. No repair here.
- Recovery examples: M6 H1→3→5 then A; M9 H2→4→6 then A; M36 H2→4→6 then A; M40 explicit medical warning, one S action H8→10 then A. M48 severe public HR warning, S cleanup/recovery through terminal. These show recovery and return to mainline in observed segments, not comprehensive MODE validity or causal survival benefit.
- Runner exit0; stop exit0; manager PID absent, listeners19092/20000/20001/6173 released. Service-start wrapper exit1 after graceful stop is a known cleanup limitation, not gameplay invalidation. No provider/Runner failure observed in the available output; no extra provider query performed.
- Score report `ending_score` is empty; outcome is attributable to exact same-session fresh final observe. Auditor's `last_observe_failed=true` is an engine end-state field and does not override structured completed outcome.

## Descriptive comparison

| Sample | Quantitative | Survival | Grade | Final Level |
|---|---:|---:|---|---|
| v8a RUN07 | 72.65 | 48m | A | L5 |
| v8a RUN08 | 59.00 | 48m | C | L4 |
| v9a RUN10 | 68.40 | 48m | B | L5 |

RUN10 lies within the observed v8a range; one v9a sample gives no causal ranking or stable score claim. Survival and runtime compatibility are observed, high-score delta benefit is unproven. Recovery from low Health coexists with later promotion, but does not establish a general failure floor.

## Exact evidence / FORENSIC_HOLD

`FORENSIC_HOLD=ACTIVE`; owner=S09 Stage/Main. Reason: qualifying-probe attribution unresolved; raw is the unique source for semantic review. Release requires Stage/Main acceptance, closure of probe/correctness questions and dependent reviews, then explicit scoped cleanup authorization. No raw archive or shared DB copied.

- Exact output: `D:\CS\CareerSim\.career_sim_runner\career_emu\outputs\local-s06-adaptive-controller\20261001T161805Z\` containing `events-20261001T161805Z.jsonl`, `transcript-20261001T161805Z.log`, `score_report.json`.
- Controller/preflight/stdout/receipt/summary/compact evidence: `D:\CS\CareerSim\.local\runtime\s09-run10-v9a\`.
- Window UTC `2026-10-01T16:17:59.610375+00:00`–`2026-10-01T16:41:13.594450+00:00`; local log offset +08:00. `scripts/post_run_audit.py` executed once after cleanup with exact paths/window; no DB/provider/service restart or latest search. Exact bytes/hashes are retained in local `post_run_summary.json.inputs`.
- Events SHA256 `10fe7d3bc50f115a1bca02abed1afab2c63b605bc04a807a93a7f780b7710702`; transcript `683c12e86ab853f3b0e807d410ef40fedf4c737d80bd741522ac2e6898977464`; score report `5d8f620a134c2fc583f59f29ea8efb59cae1e6287da5a76b0f8f767a67948924`; runner receipt `59881d18660f8f4a55460faa77f4ec2ee2fa28079a2d84dcc32c101f9892fea5`.

`S09_RUN10_GAME_AUTHORIZATION=CONSUMED` · `NEXT_GAME=NOT_AUTHORIZED` · `NO_REPLACEMENT_RUN_AUTHORIZED` · `MAIN_V8A_FREEZE_UNCHANGED`.
