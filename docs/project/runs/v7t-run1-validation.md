# TASK_RESULT｜S08-RUN03

## Identity

- **Status:** `RUN_COMPLETE / STAGE_REVIEW_REQUIRED`
- **Run Classification:** `VALID_48M_COMPLETION`
- **Candidate:** `candidate-v7t-execution-semantic-repair` (parent `candidate-v7s-zh-recovery-controller`)
- **Strategy delta:** `EXECUTION_CONTRACT_AMBIGUITY_REPAIR_ONLY`
- **Base SHA:** `e4ec82958ccfcac23ca8b28af14e69be1c470fa2` (`main == origin/main` at preflight)
- **Candidate frozen base:** `3060c63142f9ad2489d08399fc750a23ff3244e8`
- **Final Commit:** the commit containing this result and the corresponding project-state updates; see the repository Git history / final delivery receipt.
- **Runner SHA:** `f61c738c72e51b77298cc1c14c7c6ebf4b6c527d`
- **Session:** `7f50220814214d97a3dc453fca049a79` (fresh game; events/transcript/score report identities match)
- **Authorization consumed:** YES; exactly one fresh game, one Runner `play`, and one service lifecycle.
- **Remote:** `origin/main` was aligned to the run base at preflight; the record commit is pushed as part of closeout.
- **Working tree:** clean at preflight; final clean state is verified after the record commit.
- **Candidate package:** offline package manifest names `candidate-v7t-execution-semantic-repair`, `mode=agent`; packaged as `skill_bundle` with exactly four Skills. Runner output directory retains the packager's legacy grouping label `local-s06-adaptive-controller`; it is not the Candidate identity.
- **Preflight gates:** v7t targeted static test set **47 passed**; offline package validation passed; retry guard matched 2; shared instance was stopped before service start; process PATH resolved the repository `jiuwenswarm-start.exe`; the single `--list` exited 0 and reported `career_emu=stopped`.
- **Local retry:** `models.defaults[0].model_client_config.max_retries=2`.
- **Service lifecycle:** one `career_emu all` start; bounded readiness passed on ports 19092, 20000, 20001 and 6173. Cleanup used one `--stop`; exit 0, manager stopped, and all four listeners were released. No restart.
- **Runner play:** exactly one `D:\CS\CareerSim\.venv\Scripts\python.exe -m career_sim_runner play --submission D:\CS\CareerSim\.local\runtime\s08-run03\submission`; fresh session, no `--continue`, no manual game-choice intervention.

## Live Progress Reporting

- **Preflight report emitted:** YES; base, targeted static gates, package, retry, runtime exclusivity, PATH and one `--list` result were reported before service/game start.
- **Session-start report emitted:** YES; after the fresh session was established.
- **Formal checkpoint reports:** M6, M12, M18, M24, M30, M36, M42 and M48.
- **Immediate anomaly reports:** promotions, public HR risk/recovery transitions, Health stabilization and natural terminal were reported as they occurred. No provider or service anomaly occurred after play started.
- **Any extra query used for reporting:** NO. Progress reports used existing Runner/stdout/gameplay output only.
- **Interactive process/session used:** YES; the Runner stayed attached to an interactive process so output could be followed during the run.

## Outcome

- `quantitative_score`: **65.71**
- `competition_partial_score`: **46.00**
- `survival_months`: **48**; natural terminal observed at Month 49.
- `grade`: **B**
- `final Level`: **L5**
- `final public state`: Health 10, Dignity 10, Skill 101, Network 38, Output 30, Wealth 27, Energy 0, Level L5.
- `promotions`: M6 L1→L2; M12 L2→L3; M30 L3→L4; M48 L4→L5.
- `successful actions`: 207
- `failed actions`: 0
- `observes`: 190
- `natural terminal`: structured terminal observation at Month 49; Runner exit code 0, `termination_reason=None`.
- `score_report.session_id`: MATCH to the new game session.
- `actual billed cost`: UNKNOWN. Runner-reported cost 0 is not billing evidence.

The score comparison is descriptive only: v7t 65.71 / 46.00 / 48m / B / L5; v7o 71.83 / 50.28 / 48m / A / L5; v7q 26.80 / 18.76 / 24m / E / L1; v6 75.29 / 52.70 / 48m / A. This single run does not prove score or survival improvement. It did not reach L6 and does not qualify as an 80+ run.

## Review Timeline

Public feedback and levels below come from same-session observations/transcript. `RECOVERY` is marked as an observed label only where the transcript records it; later operational classifications are explicitly identified as evidence-based interpretation.

| Checkpoint | Grade / Level / Promotion | MODE / RECOVERY | Public feedback and Primary Gap | Next Review Window goal |
|---|---|---|---|---|
| M6 | C; L1→L2, promoted | A / PROGRESSION (explicit) | Overall met expectations, but no standout/highlight; visible performance/output gap. | M12: create clearer visible results while retaining delivery certainty. |
| M12 | B; L2→L3, promoted | A / RISK (explicit) | Still being observed; clearer results requested; relationship friction also tracked. | M18: visible results plus relationship repair; one bounded risk cleanup after elevated public warning. |
| M18 | B; L3, no promotion | A / PROGRESSION (operational; no new explicit recovery label) | “Busy but not winning” feedback; clearer results remained the primary gap. | M24: continue Output/result realization and prepare before the checkpoint. |
| M24 | B; L3, no promotion | A / PROGRESSION (operational) | Still on observation list; next window asked for clearer results. | M30: keep Output-focused preparation through the next formal Review. |
| M30 | B; L3→L4, promoted | A / NONE (promotion occurred; progression continued) | Met expectations, but highlights still not prominent. | M36: produce visible impact at the new Level; Board showed new-Level progression as UNKNOWN. |
| M36 | A; L4, no promotion | A / PROGRESSION (operational) | Stable delivery and communication; Leader said they would push in the next window and asked for materials early. | M42: prepare materials and preserve delivery while building visible Output. |
| M42 | A; L4, no promotion | A / PROGRESSION (operational) | Leader reaffirmed next-window support and early materials; Output remained the stated focus. | M48: convert visible Output and the promised sponsorship into promotion evidence. |
| M48 | A; L4→L5, promoted | A / NONE (promotion occurred) | Leader advised focusing on output and relationships and revisiting the next level in six months. | M54/L6 was named as the next window, but natural termination followed at M49. |

The early chain M6→L2 and M12→L3 returned. The M18→L4 step did not occur; L4 arrived at M30 instead. No hidden promotion threshold is inferred.

## Early Promotion Engine

- **Classification:** `PARTIALLY_RESTORED`
- **Evidence:** promotions at M6, M12, M30 and M48; M18 and M24 had B/no-promotion at L3; M36 and M42 had A/no-promotion at L4. The early L2/L3 chain is present, but not the v7q-failure recovery target of L4 by M18.
- **Comparison with v7q:** v7q remained L1 through M18 and naturally terminated at M24; v7t reached L2/M6, L3/M12, survived 48 months and reached L5. Descriptive run comparison only, not causal improvement evidence.
- **L6:** not reached; no L6 conclusion.

## Failure Recovery

### PROGRESSION

- **Trigger:** M6 C despite promotion and “no standout” feedback; later B/no-promotion at M18/M24, followed by repeated clearer-results feedback.
- **MODE:** A throughout these performance-recovery windows; no long-term S deadlock.
- **Action:** output-focused quarterly allocation, visible delivery improvements, key-project choices and continued checkpoint preparation.
- **Exit / return to mainline:** growth remained the mainline; the only explicit M6 label was `RECOVERY=PROGRESSION`. Subsequent no-promotion windows behaved consistently with A/progression, though their transcript did not always restate a recovery label.
- **Result:** promotion resumed at M30 and again at M48. The M18/M24 windows still missed promotion; recovery was effective for continued progression but not immediate promotion.

### RESOURCE

- **Trigger:** public Health declined to 2 at M8, followed by Health 3 at the M9 quarterly allocation.
- **MODE:** S for two Health actions only.
- **Action:** Health 3→5→7, then the next allocation returned to A and Output preparation.
- **Exit / returned to mainline:** YES, after minimum stabilization; no automatic refill-to-maximum policy was observed in this recovery window.
- **Result:** the public Health constraint was stabilized and A resumed. This is direct evidence that a resource recovery path was exercised.

### RISK

- **Trigger:** public HR risk warning in M5/M6; one cleanup at M6. Public warning reappeared and escalated by M12 (“自求多福” / risk accumulating), permitting one subsequent cleanup.
- **MODE:** A; warning alone did not trigger MODE=S.
- **Action:** one bounded “处理历史埋雷” cleanup after each qualifying warning window (M6 and M12).
- **Exit / returned to mainline:** M7 public HR feedback turned positive and said the risk was resolved; after the M12 cleanup, M14 HR feedback was positive. No later cleanup was observed without new same-class warning evidence.
- **Result:** bounded cleanup behavior is supported for the two observed windows. Risk marker syntax remained `R=PASS` for all 207 actions, so marker taxonomy does not independently explain these public-warning decisions.

### DELIVERY

- **Trigger:** M1 current client scope/estimate commitment with a M6 checkpoint; later a D2 AI-use transparency guideline was recorded as committed/unverified. M39 public story disclosed a one-week milestone delay.
- **MODE:** normally A.
- **Action:** the transcript records scope negotiation, written change/confirmation process, later result preparation and attention to scheduled work.
- **Exit / returned to mainline:** UNKNOWN as a verified Delivery lifecycle transition; the offline marker audit decoded no valid per-action DL state.
- **Result:** `DELIVERY_RECOVERY=INCONCLUSIVE`. The transcript shows the agent tracked D1 before the first Review, debated whether it could be called publicly verified and backed off to `UNVERIFIED`; D2 later remained `COMMITTED / UNVERIFIED` in emitted notes. The audit decoded no pre-first-review Delivery states; the simultaneous active-item count is UNKNOWN. No confident false-closure finding is made, but lifecycle correctness cannot be certified from the malformed marker stream. A successful tool call is not treated as a verified career/delivery result.

## MODE

- A count: **205 / 207**
- S count: **2 / 207**
- S percentage: **0.966%** (0.97% rounded)
- `VALID_BINDING_CONSTRAINT`: 2; both were the Health recovery actions at public Health 3 and 5.
- `QUESTIONABLE`: 0 identified.
- `FALSE_STABILIZE`: 0 identified.
- `UNKNOWN`: 0 among the two S actions; no other action was S.
- Poor grade/no-promotion alone, weak Skill/Network/Output, ordinary numeric decline, ordinary fatigue or work pressure did not produce S in the audited P markers.
- The two S actions stopped after public Health recovered to 7, then the run returned to A. MODE control is supported for this one session.

## PROGRESSION_RESPONSE

The following are the 28 quarterly progression actions with a distinct fresh observe before the action and another fresh observe after it. Values are public Skill/Network/Output. “Advertised dimensions” are the dimensions named by the selected action; mixed rows retain non-zero value in another dimension and do not imply a hidden cap.

| Month | Level | Action | Advertised dimensions | Before → after | Result |
|---:|---|---|---|---|---|
| 3 | L1 | Network maintenance | N | 3 → 3 | NO_GAIN |
| 3 | L1 | Report preparation | O | 2 → 3 | GAIN |
| 3 | L1 | Key project | S/N/O | 8/3/3 → 9/3/3 | MIXED_OR_UNATTRIBUTABLE |
| 6 | L2 | Report preparation | O | 4 → 5 | GAIN |
| 6 | L2 | Key project | S/N/O | 14/7/5 → 15/7/6 | MIXED_OR_UNATTRIBUTABLE |
| 9 | L2 | Report preparation | O | 6 → 6 | NO_GAIN |
| 9 | L2 | Mentor relationship | S/N | 21/5 → 21/7 | MIXED_OR_UNATTRIBUTABLE |
| 12 | L3 | Network maintenance | N | 7 → 8 | GAIN |
| 12 | L3 | Key project | S/N/O | 22/8/7 → 23/9/9 | GAIN |
| 15 | L3 | Key project | S/N/O | 33/14/7 → 34/15/9 | GAIN |
| 18 | L3 | Mentor relationship | S/N | 42/17 → 42/19 | MIXED_OR_UNATTRIBUTABLE |
| 21 | L3 | Key project | S/N/O | 42/19/9 → 42/20/11 | MIXED_OR_UNATTRIBUTABLE |
| 24 | L3 | Key project | S/N/O | 42/21/14 → 42/21/16 | MIXED_OR_UNATTRIBUTABLE |
| 27 | L3 | Key project | S/N/O | 42/21/16 → 42/21/16 | NO_GAIN |
| 30 | L4 | Key project | S/N/O | 46/22/16 → 47/23/18 | GAIN |
| 33 | L4 | Key project | S/N/O | 58/24/22 → 59/25/24 | GAIN |
| 36 | L4 | Key project | S/N/O | 71/34/26 → 72/35/26 | MIXED_OR_UNATTRIBUTABLE |
| 39 | L4 | Key project | S/N/O | 75/36/25 → 76/36/26 | MIXED_OR_UNATTRIBUTABLE |
| 42 | L4 | Report preparation | O | 26 → 26 | NO_GAIN |
| 42 | L4 | Report preparation | O | 26 → 26 | NO_GAIN |
| 42 | L4 | Report preparation | O | 26 → 26 | NO_GAIN |
| 42 | L4 | Key project | S/N/O | 82/36/26 → 83/36/26 | MIXED_OR_UNATTRIBUTABLE |
| 45 | L4 | Report preparation | O | 24 → 25 | GAIN |
| 45 | L4 | Report preparation | O | 25 → 26 | GAIN |
| 45 | L4 | Report preparation | O | 26 → 26 | NO_GAIN |
| 45 | L4 | Key project | S/N/O | 92/36/26 → 93/36/26 | MIXED_OR_UNATTRIBUTABLE |
| 48 | L5 | Report preparation | O | 27 → 28 | GAIN |
| 48 | L5 | Key project | S/N/O | 100/37/28 → 101/38/30 | GAIN |

- Clean attributed pairs: **28** — GAIN **11**, NO_GAIN **7**, MIXED_OR_UNATTRIBUTABLE **10**.
- NO_GAIN immediate repeats: **not supported**. At M42/L4, three consecutive report-preparation actions each left Output at 26→26; the next multi-dimensional action gained Skill only and still did not improve Output. This is a direct same-Level repeated NO_GAIN route.
- Routed away: the M3 Network NO_GAIN was followed by Output GAIN; M9 Output NO_GAIN was followed by a mixed mentor action with Network +2. These are positive examples, but they do not offset the M42 repeated Output path.
- Partial multidimensional discount: mixed key-project rows preserved observed gains in responsive dimensions even when other dimensions stayed flat (for example M42 S+1 with N/O unchanged; M45 S+1 with N/O unchanged).
- Level-reset events: Board text explicitly marked new-Level progression UNKNOWN after the M30 promotion; subsequent clean gains occurred at L4. Full S/N/O reset state at every level transition was not independently machine-verified. No hidden cap is inferred.
- **Classification:** `NO_GAIN_ROUTING=NOT_SUPPORTED` for this run because of the M42 three-action repeated no-gain sequence.

## Review Window / Delivery

- **Checkpoint preparation:** M6→M12, M12→M18 and M24→M30 kept the current gap in view; M36 and M42 carried the Leader's “next window” support and early-material request into planning.
- **Delivery certainty:** scope negotiation and change logging were used on the client commitment. However the exact active Delivery item and verified-result transition are not recoverable from DL markers.
- **Late/post-checkpoint growth mistakes:** M42 repeated Output training with three clean public NO_GAIN observations at L4. This is the clearest mismatch between the stated review goal and observed marginal response.
- **Delivery overclaim:** no confirmed false public closure; D1's attempted `PUBLICLY_VERIFIED` status was questioned in the transcript and left UNVERIFIED. Since all DL action markers failed the auditor's syntax gate, final lifecycle/overclaim status remains UNKNOWN.
- **DELIVERY recovery result:** `INCONCLUSIVE`; M39 public text indicated a one-week milestone delay, but no valid lifecycle markers establish whether recovery closed the affected commitment.

## Risk

- `PASS`: 207
- `ALLOW`: 0
- `WARN`: 0
- `RECONSIDER`: 0
- `UNKNOWN`: 0
- `bounded cleanups`: 2 public-evidence-linked cleanups (M6 and M12).
- `repeated cleanup allowed only by persistent/new warning`: supported in the observed sequence: the first warning resolved by M7; the second cleanup followed later re-elevation/accumulation; no third cleanup was seen without another qualifying warning.
- `public-risk anomaly`: transcript contains public HR warnings while the compact Risk marker remains PASS for every action. The marker stream therefore cannot be treated as the public-warning taxonomy itself.
- No RECONSIDER branch was exercised; the one-reconsideration limit was not approached.

## Skill Coordination

- **Board:** 190 public observe results; current visible level/resources/reviews and progression response appear in the transcript. There is no independent machine check of internal Board fidelity. UNKNOWN discipline is limited: audit found 0 numeric HiddenRisk references in action notes, but a transcript lexical scan found 37 numeric HiddenRisk text matches (text matches only, not a semantic verdict).
- **CTRL:** all 207 notes parsed as one syntactically valid marker, but `X=0` on all 207; the exact audit reports `CTRL_CLOSURE_FAIL` / `submitted_incomplete_x0=207`. Thus marker parsing success is not action-closure success.
- **Delivery:** lifecycle markers present in prose but 0/207 valid according to the exact parser; 207/207 malformed-or-duplicate for the required syntax. No `delivery_states_by_action` or pre-first-review states could be reconstructed; simultaneous active-item bound is UNKNOWN.
- **Planning:** Review Plan continuity is visible from M6 through M48 and A remained the default for performance/no-promotion. The transcript also contains repeated reconsideration on some story choices, including the M46 high-risk project, without a clearly new evidence boundary; this is a deliberation-efficiency limitation.
- **Risk:** all 207 compact R markers are PASS; two public-warning cleanup actions are visible in the transcript. No ALLOW/WARN/RECONSIDER marker transitions were counted.
- **handoff anomalies:** events contain **207 take_action calls but 190 observe calls**. Eighteen action-to-observe boundaries are missing after subtracting the one initial observe; the transcript groups these into nine quarterly-energy windows with three action calls before the next observe. This violates the required per-action `take_action → fresh observe` loop. It is a runtime-adherence failure even though all action results succeeded and the game later reached natural completion.

### Story / event semantics sample

Classification: `EVENT_SEMANTICS_USED_CORRECTLY` for the sampled public contexts, with whole-run semantic correctness not claimed. The transcript references current descriptions and legal choices for customer scope/delivery, confidentiality, AI-use transparency/compliance, authorship/credit, user-data safety, accurate reporting, relationships/retaliation and scheduled work. No event ID or hidden event effect is used here as evidence. Some long story reconsideration remains a planning-efficiency concern.

## Persistence / Compression

- `observes`: 190
- `actions`: 207 successful; no failed/unknown result.
- `counted execution boundaries`: 1 Runner `play` invocation; 18 missing per-action observe boundaries across nine energy windows.
- `continuation sends`: UNKNOWN; not exposed by the archived artifacts.
- `max_continuations`: not reached; the structured game ended naturally after 48 survival months. The exact configured limit/counter was not emitted in the P5 summary.
- `compression markers`: UNKNOWN; the safe run-window `llm.log` slice was not available/supplied to the one-pass audit.
- `required recovery sequences`: 0 observed; without an observable resume/compaction signal, no sequence was inferred.
- `recovery adherence`: NOT EXERCISED / UNKNOWN due to absent compression signal evidence.
- `provider-error zero-work terminations`: 0.
- `Skill rereads`: four initial Skill reads in order (`structured-state-board` → `delivery-progress` → `rolling-planning` → `risk-review`); zero later rereads detected in the event stream. No recovery signal required a reread sequence.
- `whole-game persistence`: natural terminal was reached, but per-action persistence is not fully supported because 18 fresh-observe boundaries are missing.

## Efficiency

- `input tokens`: 38,690,418
- `output tokens`: 200,839
- `total tokens`: 38,891,257
- `wall time`: 21m 27.957s (UTC 2026-09-29 17:17:54.485311 to 17:39:22.442339; Asia/Shanghai 2026-09-30 01:17:54 to 01:39:22)
- `Skill rereads`: 0 after the four initial reads.
- No reporting-only live query, standalone provider probe, replacement game, manual game intervention or second service start occurred.

## Evidence

- `events`: [events.jsonl](../../../artifacts/dev-runs/s08-run03-v7t/events.jsonl) — 1,892,046 bytes; SHA-256 `c630579d5ebbcdbcecf9f6eee1104434b75cb92a9f3915cdbf4a5c1084e21fdb`
- `transcript`: [transcript.log](../../../artifacts/dev-runs/s08-run03-v7t/transcript.log) — 547,255 bytes; SHA-256 `528ca2630d5b8c5c26bb5cb5f8879421d4f53543dbe1f93834cf68a9b8f16747`
- `score report`: [score_report.json](../../../artifacts/dev-runs/s08-run03-v7t/score_report.json) — 2,744 bytes; SHA-256 `1a5de612048a5368b10b3d9fb153d98dac1bdfcf250347d5c20a6e111f2bdff0`
- `runner result`: [runner-result.json](../../../artifacts/dev-runs/s08-run03-v7t/runner-result.json) — 841 bytes; SHA-256 `ba2ffd47c1e10ab95dfcc732d3082e169ea0c253322a26ce9eaf95bd19ca65ad`. Runner emitted no separate result file; this artifact is explicitly marked `RECONSTRUCTED_FROM_INTERACTIVE_RUNNER_STDOUT`, exit 0, and was cross-checked against the exact score report/output directory.
- `post_run_summary`: [post_run_summary.json](../../../artifacts/dev-runs/s08-run03-v7t/post_run_summary.json) — 192,559 bytes; SHA-256 `d1f719e946473f0a06d11742f3097961a16b4182bdeb9b5fc421a92323134ec1`.
- `archive manifest`: [evidence-manifest.json](../../../artifacts/dev-runs/s08-run03-v7t/evidence-manifest.json) — 1,131 bytes; SHA-256 `b0b362159414827ff4062b7fa2322a151c51ab4540398c8d5da774b04f65e0bf`.
- Archive script secret scan and exact core session-consistency check: PASS. No `.env`, API key, private config, shared DB, unrelated session or provider log was archived.
- Raw local source remains under `.local/runtime/s08-run03/` and the exact Runner output directory. `FORENSIC_HOLD=ACTIVE` pending Main/Stage review; archive presence does not itself release the hold.
- P5 ran once after cleanup with exact event/transcript/score/result inputs and the exact run window. It did not query the shared DB, search for “latest”, restart Provider/service, or receive an `llm.log` slice.

### FORENSIC_HOLD

- **State:** `ACTIVE`.
- **Reason:** the conclusion depends on the raw action/observe sequence because 18 observe boundaries are absent; CTRL closure and Delivery marker audits fail; compression cannot be assessed without a safely scoped log slice.
- **Minimum retained evidence:** all five archived core files plus `evidence-manifest.json` under `artifacts/dev-runs/s08-run03-v7t/`; exact window `2026-09-29T17:17:54.485311+00:00`–`2026-09-29T17:39:22.442339+00:00`. Core hashes are listed above and in the manifest.
- **Responsible Task:** S08-RUN03 closeout. **Release/review owner:** Main/Stage reviewer.
- **Release condition:** independent review accepts the adherence/strategy interpretation and confirms the necessary sources remain recoverable or need no further analysis. Archive/hash/COMPLETE alone do not release this hold; cleanup would require a later explicitly scoped authorization.
- **Recheck point:** Main/Stage review of this TASK_RESULT.

Provider/model identity in the archived event usage record is `unknown`; no provider identity or actual billed cost is inferred.

## Final Classifications

- `Run`: `VALID_48M_COMPLETION`
- `Early Promotion Engine`: `PARTIALLY_RESTORED`
- `Failure Recovery`: `PARTIALLY_EFFECTIVE`
- `MODE Control`: `SUPPORTED`
- `NO_GAIN Routing`: `NOT_SUPPORTED`
- `Delivery Recovery`: `INCONCLUSIVE`
- `Risk Cleanup`: `SUPPORTED`
- `Score Ceiling`: 65.71 / B / L5, below v7o and v6 descriptive references; L6 and 80+ not reached.
- `Failure Floor`: one complete 48-month natural completion at L5 with resource stabilization, public-warning recovery and no long-term S deadlock; this is one observation and not a stable floor estimate.

## Final Decision

`V7T_RUN_ACCEPTED_RECOVERY_REVIEW`

Run and provider/gameplay evidence are valid for this session. Return to Stage/Main to review the 18 missing fresh-observe boundaries, M42 repeated Output NO_GAIN, Delivery/CTRL marker failures, and the direct recovery evidence. Runtime adherence remains false. No patch or rerun was made in this task.

S08_RUN03_GAME_AUTHORIZATION = CONSUMED

NEXT_GAME = NOT_AUTHORIZED

NO_REPLACEMENT_RUN_AUTHORIZED
