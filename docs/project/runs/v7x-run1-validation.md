# S09-RUN02｜v7x Run #1 Validation

## Identity

- **Status:** `EVIDENCE_COMPLETE`; return to Stage review.
- **Run classification:** `EARLY_NATURAL_TERMINAL` at Month 8; Runner and natural-terminal receipts succeeded.
- **Candidate:** `candidate-v7x-fresh-binding-reauthorization`; parent `candidate-v7w-high-score-core-recovery`; Candidate frozen base `main@74e856c5be7a9a134f93e9876ffbfd14398199ab`.
- **Run base:** `main@43258d41a02ac65c9f1e5d0367ca7612a36c7da7`.
- **Runner:** `f61c738c72e51b77298cc1c14c7c6ebf4b6c527d`; local retry `max_retries=2`.
- **Candidate package:** built once at `.local/runtime/s09-run02-v7x/submission`; preflight verified exact v7x manifest/instruction hashes, four canonical Skills, `skill_bundle`, and package identity. Runtime manifest SHA-256 `882c979821375393988ee0e989e2a503b8528562605618d7ab5c1bf5699f1804`; instruction SHA-256 `fef598a0a6903418400e91e651934ba9f48988110b02155cec92060452c419c9`. Packaged Skill SHA-256 values: Board `e2f31a83b357f2f75b1e2c0e8285fba440a17d3c4c4c8d6587b4f2e5fa9f366c`, Planning `3e45775cc714147fea44131794d6b569536d022c6b0ab4deb50583197e8771d7`, Delivery `200b6c83aaca43f6dccfe58a30e23e79463e930512ef89cf5b19070a9d5d7528`, Risk `6da910fa60b07dfdccfc78a840ebc4777fc39e3188358e69ee483c89606874fd`. Runner/dependencies were unchanged from the approved base. The score report's `submission_name` is the generic `local-s06-adaptive-controller`; its session id matches the fresh run, and the exact v7x submission directory was supplied to Runner.
- **Session:** `700f8ed814844694869d93461e7ef748`; drive session `career-sim-runner-05ecebf950de`.
- **Run window:** `2026-09-30T13:11:04+00:00` to `2026-09-30T13:14:16.638819+00:00` (3m12.639s).
- **Authorization:** consumed at the single Runner play start; one fresh game, one play, one service start/stop lifecycle; zero replacement games, zero continue/resume, zero manual choices, zero standalone provider probes.
- **Static evidence reused:** S09-03's 52 targeted/static/package tests and deterministic four-Skill bundle PASS remained applicable; exact run package identity was rechecked before play.

## Outcome

- Quantitative score: **19.82**.
- Competition partial score: **13.88**.
- Survival: **8 months**; grade **E**; final level **L1**; promotions: **none**.
- Runner outcome: `eliminated`; Runner/play exit codes both `0`; one natural terminal was present in the final public observation.
- Final public state at M8: Health 0, Energy 0, Dignity 7, Skill 9, Network 3, Output 3, Wealth 3, Level L1. Score report and final-observe score agree; billed cost is UNKNOWN despite the Runner reporting `0.0`.
- The run ended naturally before M12. This score/survival is descriptive for one session and does not establish causal change, stable performance, or regression.

## Review and Decision Windows

| Window | Public evidence and review | MODE / recovery | Result and boundary |
|---|---|---|---|
| M1–M6 | M1 public state began at L1, S1/N1/O0, H5/W1. At M6, review grade C, no promotion, L1 retained; public state H4/D10/E0/S9/N3/O3/W3. Primary Gap was Output. | A / PROGRESSION after the review | Performance failure did not force long-term S. The next Review target focused on Output, but M12 was not reached. |
| M7–M12 | M7 had a mild public risk warning. Public Health was observed at 4, then 2. Natural terminal occurred at M8 with H0. | A / RISK at the warning; no cleanup; later terminal before the planned next-quarter recovery | Failure window is M7–M8. Whether earlier stabilization, trust/continuity, or another action would have prevented terminal is UNKNOWN. |
| M13–M18 | Not reached. | Not exercised | No later promotion or progression evidence. |
| M19–M24 | Not reached. | Not exercised | No evidence. |
| M25–M36 | Not reached. | Not exercised | No evidence. |
| M37–M48 | Not reached. | Not exercised | No evidence. |

### Early Promotion Engine

**Classification: `NOT_RESTORED` for the only exercised formal checkpoint.** M6 was C/no-promotion at L1. This does not establish what would have happened at M12/M18 because the game ended at M8. Against v7w's M24 D/L2 terminal, this run ended earlier and at a lower observed score; the comparison is descriptive, not controlled or causal.

## Fresh-Binding Reauthorization Audit

The audit uses only current public state and participant-visible rationale. It does not infer hidden Risk or thresholds.

| Action | Fresh public basis before S | Public result | Classification |
|---|---|---|---|
| M3 action 11 | Health 1; Planning described a near-redline concern. Public Health was materially low, but the allowed evidence does not establish the precise threat semantics or any numeric cutoff. | Health 1→3. | `AMBIGUOUS` |
| M3 action 12 | Fresh observation after the prior action showed Health 3; rationale was to continue building a Health buffer. No explicit unresolved warning was independently recorded in the audit. | Health 3→5; the subsequent decision returned to A. | `AMBIGUOUS` |

- Total S actions: 2; MODE=A=27, MODE=S=2 (6.90%).
- Counts: supported reauthorization 0; supported same-threat continuation 0; false stabilize 0; stale continuation 0; ambiguous 2; unknown 0.
- Longest S streak: 2. Longest *confirmed* unsupported/stale streak: 0; the two-action ambiguous streak is not reclassified as confirmed unsupported.
- The next observed decision after Health reached 5 was A. This shows a bounded observed S episode, but does not independently prove the system recognized that a specific threat had resolved.
- M6 C/no-promotion was handled as A/PROGRESSION, consistent with the plan's rule that poor grade alone does not bind S.
- **Mechanism conclusion:** `INCONCLUSIVE`. No stale or false S was confirmed, but the two instances lack enough semantics to claim supported threat handling. A single early terminal cannot establish score or survival effect.

## Failure Floor and Recovery

- **Resource:** two M3 public Health-recovery actions raised Health 1→3→5. Later public observations fell from H4 to H2 and then terminal H0 at M8. The planned next-quarter recovery did not occur before terminal. Resource handling was exercised but did not yield a completed recovery lifecycle.
- **Progression:** M6 C/no-promotion, gap Output; Planning stayed in A/PROGRESSION. No later Review tested recovery response.
- **Risk:** a mild M7 public warning was followed by A/RECOVERY=RISK and no cleanup. Bounded cleanup / reauthorization was not exercised.
- **Delivery:** no explicit DELIVERY recovery was verified. M5 included a near-term commitment context, while all Delivery action states reported `I=NONE`; this may be lifecycle undertracking, but evidence does not establish that a valid active item was omitted. Mark `INCONCLUSIVE`.
- **Trust / continuity:** no causal terminal attribution is available. The terminal preceded a subsequent formal review, so progression collapse and resource attrition cannot be disentangled.
- **Terminal type:** natural elimination at M8, not a Runner/provider technical failure. Failure floor for this run is poor; cause decomposition remains incomplete.

## Score Ceiling and Planning

- Public early trajectory changed from M1 S1/N1/O0 to M6 S9/N3/O3, yet the first review was C with no promotion. These public deltas alone do not reveal hidden promotion thresholds.
- The G marker sequence was `?` for the first ten actions, `SURVIVAL` for the two M3 S actions, `OUTPUT` for seven actions, then `NETWORK` for the final two. Marker values do not independently establish planning quality.
- Quarterly Main choices were recorded at M3 and M6. Two M3 Energy recovery choices were observed. The complete Main/Energy/story mix and exact rank/utility rationale are unavailable from the safe audit summary.
- No auditable clean per-action S/N/O progression pair table was produced. `PROGRESSION_RESPONSE` reset behavior and NO_GAIN routing are therefore `UNKNOWN / NOT_EXERCISED`, not supported or failed.
- The M6 Output Primary Gap and next-window direction were recorded; complete REVIEW_PLAN continuity and a later reset were not established before terminal.

## Runtime and Skill Coordination

- **Actions/observations:** 29 attempts, 29 successful, 0 failed, 0 unknown, 0 noncanonical routes; 30 fresh public observations (one initial plus 29 post-action observations by count). The summary does not expose a separate ordered action/observe-pair metric, so the exact sequence-level boundary result is not asserted here.
- **CTRL:** syntax/consistency 29/29; MODE=A 27, MODE=S 2; R=PASS 29/29; RB=DONE once and NONE 28 times. RB branch use is not independently verified.
- **Board:** the public audit includes 30 session-bound public observations and their state tuples. Full Board-to-observation fidelity was not independently scored; mark UNKNOWN.
- **Delivery:** marker syntax and coverage 29/29. Audit status is `MARKERS_OBSERVED_NOT_ADHERENCE_PROOF`; all states had `I=NONE`. Completion/recognition semantics remain inconclusive.
- **Planning:** M6 progression recovery was A/PROGRESSION. Two S rationale windows were ambiguous. Complete candidate ranking, Review Plan continuity, and NO_GAIN routing are not proven.
- **Risk:** R=PASS 29/29; no ALLOW/WARN/RECONSIDER marker was emitted. The M7 public warning was handled in Planning without a cleanup; reconsideration behavior was not exercised.
- **Compression/recovery:** UNKNOWN; the exact run-window llm.log slice was not safely available. No compression or recovery count is asserted.
- **Evidence firewall:** events audit recorded zero numeric HiddenRisk/internal-score text matches. Transcript lexical scanning found six HiddenRisk text matches, but this is only a text-match count, not a semantic verdict. Firewall correctness remains UNKNOWN and raw evidence stays held.

## Efficiency, Cleanup, and Evidence

- Usage bound to the session: 4,286,674 input / 29,445 output / 4,316,119 total tokens. Actual billed cost: UNKNOWN. Skill rereads, exact continuation sends, and compression count: UNKNOWN.
- One interactive Runner process was used. No standalone provider probe, gameplay intervention, retry, restart, or replacement run occurred.
- Service readiness passed despite a Windows GBK console logging error. One graceful stop exited 0; manager stopped and listeners 19092, 20000, 20001, and 6173 were released. The foreground launcher later exited 1 after stop; retained as a runtime limitation and not a gameplay invalidation.
- The canonical archive secret scan passed. Committed selected archive:
  - `artifacts/dev-runs/s09-run02-v7x/score_report.json` — 2,722 bytes; SHA-256 `dcaf6f5ed6acbeec811077ad23bf27200b3c14f19d83fbb03333278078617fd3`
  - `artifacts/dev-runs/s09-run02-v7x/runner-result.json` — 626 bytes; SHA-256 `fa537c917b2b85d008c53a016dd7365e7796157cc6deb2c24f766a76ac8e7021` (derived receipt; Runner emitted no standalone result file)
  - `artifacts/dev-runs/s09-run02-v7x/post_run_summary.json` — 52,755 bytes; SHA-256 `e20c3e376571c13dea42631dfb013d88703301b10693a9006cfac03d58d2d46a`
  - `artifacts/dev-runs/s09-run02-v7x/evidence-manifest.json` — 758 bytes; SHA-256 `006442341d25e3b5540c4398333a345638770bdd96d597090f37bd1893dd67f3`; records the exact archive byte counts, hashes, and UTC run window.

### FORENSIC_HOLD=ACTIVE

Raw evidence remains at the exact Runner output directory because early terminal, ambiguous S semantics, and unresolved transcript text matches may require independent Stage review. Do not delete or alter these files until Stage/Main accepts the independent review, verifies source recoverability or determines reanalysis is unnecessary, and explicitly releases this hold.

- Events: `D:\CS\CareerSim\.career_sim_runner\career_emu\outputs\local-s06-adaptive-controller\20260930T131104Z\events-20260930T131104Z.jsonl`; 376,682 bytes; SHA-256 `8e757e1f207c54c10c7ce9281bf8169c086b916e3ebac8784784775ec557be4a`.
- Transcript: `D:\CS\CareerSim\.career_sim_runner\career_emu\outputs\local-s06-adaptive-controller\20260930T131104Z\transcript-20260930T131104Z.log`; 79,869 bytes; SHA-256 `333d4b1d05c11b75670f956aef964894c63697bbfa46d76519ea9596d0b69d52`.
- Task/run: S09-RUN02 / session `700f8ed814844694869d93461e7ef748`; hold owner: S09 Stage/Main reviewer; release condition: independent public-only semantic review of the two S windows and transcript matches, plus confirmation that no additional raw source is needed.
- Raw events and transcript were deliberately excluded from the repository archive. The hold does not release older holds.

## Candidate Flags and Decision

`configs/current_candidate.json` records only directly supported flags:

- `gameplay_validated=true`, `provider_validated=true` for this exact session.
- `runtime_validated=false`, `long_horizon_adherence=false`.
- `survival_improvement_proven=false`, `score_improvement_proven=false`, `stable_80_plus_proven=false`, `hidden_test_transfer_proven=false`, `next_game_authorized=false`.
- No Candidate/Skill/manifest/Runner/dependency/retry behavior was changed during this run task.

**Final decision:** `S09_RUN02_V7X_EVIDENCE_COMPLETE_RETURN_TO_STAGE_REVIEW`.

`S09_RUN02 game authorization consumed; NEXT_GAME=NOT_AUTHORIZED; NO_REPLACEMENT_RUN_AUTHORIZED.`

`HPL_COORDINATION_IMPACT=NONE`.
