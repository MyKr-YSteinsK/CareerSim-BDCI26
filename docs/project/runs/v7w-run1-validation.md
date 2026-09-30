# S09-RUN01｜v7w 首次正式对局与策略取证

## Decision

- Run classification: **EARLY_NATURAL_TERMINAL**.
- Disposition: **S09_RUN01_V7W_EVIDENCE_COMPLETE_RETURN_TO_STAGE_REVIEW**.
- One fresh game, one Runner play and one career_emu lifecycle were used. The game ended naturally at M24; no replacement run was started.
- Gameplay and Provider validation apply to this session only. Runtime adherence, long-horizon adherence, score/survival improvement, stable 80+ and hidden-test transfer are not validated.
- The failure-floor evidence is material: three consecutive formal Reviews at M6/M12/M18 did not promote, and the game ended at M24. The only observed promotion was L1→L2 at M24, before the public terminal result.
- No Candidate strategy, Skill, manifest, Runner, dependency or retry patch was made. Return to Stage/Main for review.

## Identity and authorization

| Field | Evidence |
|---|---|
| Run | S09-RUN01 |
| Candidate | candidate-v7w-high-score-core-recovery |
| Parent | candidate-v7v-preflight-ordering-repair |
| Run base | main and origin/main at d94b178e3e7867b80673c4dfecd2e70dd66272b5; clean before execution |
| Candidate frozen base | 62b4937af10bd6fd8fea4cc794ac1b986cb7863e |
| Runner SHA | f61c738c72e51b77298cc1c14c7c6ebf4b6c527d |
| Submission | .local/runtime/s09-run01-v7w/submission |
| Preflight | PASS; canonical skill_bundle; exactly four Skills; retry guard=2; targeted tests 29 passed, reused at the approved identity |
| Runner play | Exactly one fresh play; no --continue; no intervention or replacement |
| career_emu | One start, readiness passed; one graceful stop; manager stopped and ports 19092, 20000, 20001 and 6173 released |
| Provider probe | 0 standalone probes |
| Authorization | Consumed when Runner play started; NEXT_GAME=NOT_AUTHORIZED |

The session identity matched across events, transcript and score report. The event window is 2026-09-30 10:04:36.443046 through 10:16:52.679839 UTC, or 12m16.237s. This is the exact gameplay event window; the complete service/process wall-clock interval was not captured and remains UNKNOWN.

The Runner play and score report exited 0. The controller exited 1 only after natural terminal and successful cleanup, while serializing auxiliary metadata containing a non-JSON thread object. The Runner result was reconstructed from captured terminal output and the exact score report; no live retry followed.

## Outcome and Review timeline

| Checkpoint | Public Review / grade | Level and promotion | MODE / RECOVERY evidence | Next-window assessment |
|---|---|---|---|---|
| M6 | C; feedback said expectations were met but there was no standout result | L1; no promotion | A; PROGRESSION markers appeared during the response window | M12 remained the next promotion checkpoint; the public-results gap remained |
| M12 | C; feedback was neutral and the employee remained under observation | L1; no promotion | A; one explicit PROGRESSION marker | M18 remained the next checkpoint; the next Review again did not promote |
| M18 | D; unfavorable feedback cited recent matters needing reassessment and shortcomings in carrying work through and communication | L1; no promotion | The CTRL marker entered S and stayed S through the last action; no corresponding RECOVERY or REVIEW_PLAN record | M24 was the next Review; no explicit plan reconstruction was captured |
| M24 | C; public output showed L1→L2 promotion, followed by terminal text citing two poor half-year performance assessments | L2 at the final fresh public state | The game ended naturally; no post-promotion action window was available | M30/M36/M42/M48 not exercised |

Outcome metrics:

- Quantitative score: **30.31**
- Competition partial score: **21.22**
- Survival: **24 months**
- Final grade: **D**
- Final Level: **L2**
- Final public state: Health 8, Dignity 7, Skill 9, Network 2, Output 3, Wealth 6, Energy 0
- Promotions: **M24, L1→L2 only**
- Unique take_action attempts: **112**; parsed success 96, parsed error 0, unknown result 16
- Fresh observes: **113** (one initial observe plus one after every action)
- New games: **1**
- Usage: 21,051,766 input tokens; 116,067 output tokens; 21,167,833 total; billed cost UNKNOWN
- Model and reasoning effort: UNKNOWN from safely scoped run evidence

### Early Promotion Engine

**NOT_RESTORED.** There was no promotion at M6, M12 or M18. L1→L2 was first observed at M24 immediately before natural elimination, so the run did not establish an early promotion-compounding chain.

The prior v7q run also ended naturally at M24, at E/L1 and 26.80 / 18.76. This v7w run ended at D/L2 and 30.31 / 21.22. These are descriptive single-run differences only; they do not establish a causal improvement or a stronger failure floor. Historical 48-month v6/v7o/v7t/v7v runs do not make v7w a long-horizon result.

### Score ceiling and failure floor

- **Score ceiling:** not exercised. This run did not reach the 48-month horizon or higher Levels; 30.31 / 21.22 is a single early-terminal observation.
- **Failure floor:** negative evidence. The game ended at M24 after public Review feedback showed repeated poor half-year performance. No hidden elimination threshold is inferred.
- The prolonged S marker state overlaps the late M18–M23 period, but available public evidence does not establish that it caused elimination. This run does not support single-action or single-Skill causality.

## Strategy and recovery review

### Promotion Portfolio, Primary Gap and action allocation

There were 112 unique action attempts: 82 Story/event choices, 23 quarterly Energy choices and 7 quarterly Main choices. By public action label:

| Public action family | Count |
|---|---:|
| Prepare visible-result/report materials | 8 |
| Maintain relationships | 7 |
| Health recovery | 6 |
| Apply for key project | 4 |
| Establish mentor relationship | 3 |
| High-intensity work | 1 |
| Historical-risk cleanup | 1 |

The M1–M18 window contained 81 actions (57 Story, 18 Energy, 6 Main). M19–M24 contained 31 (25 Story, 5 Energy, 1 Main). M25–M48 were not reached. The quarterly Main choices were four key-project applications and three mentor relationships. No explicit Skill-training Energy choice was observed.

For descriptive context, the published v6 audit recorded 41 Energy choices and 16 quarterly Main choices across its longer run; v7o recorded 16 quarterly Main checkpoints; v7v recorded 204 actions and 16 quarterly Main checkpoints, 14 of them key-project applications. v7w ended before M25, so raw counts are not exposure-normalized and do not establish an allocation or score effect.

The Board’s public G marker moved from unknown in the opening window to an Output/visible-results gap, and later briefly incorporated Network and Health descriptions. Output remained a recurring gap marker through much of the run. There were **zero literal REVIEW_PLAN blocks** in the action notes, so checkpoint intent, reconstruction after each Review, commitment tracking and gap-expiry semantics cannot be independently verified. M18’s new Review did not have a captured plan reset.

### PROGRESSION_RESPONSE and NO_GAIN routing

Twenty-three quarterly Energy/Main choices advertised at least one of Skill, Network or Output in participant-visible action text. Adjacent fresh public states yielded these dimension-level pairs:

| Advertised dimension | Publicly paired attempts | GAIN | NO_GAIN |
|---|---:|---:|---:|
| Skill | 7 | 1 | 6 |
| Network | 14 | 9 | 5 |
| Output | 13 | 6 | 7 |

At whole-action level, 10 of the 23 showed gains in every advertised S/N/O dimension, 9 showed no gain in any advertised S/N/O dimension, and 4 were mixed across advertised dimensions. These are adjacent-observe public-state classifications; they do not imply a hidden cap.

The notes contained 18 PROGRESSION_RESPONSE mentions. Only 11 had machine-readable S/N/O category tokens; 7 later mentions had no parseable S/N/O values. Literal parsed tokens included repeated NO_GAIN observations, but the format did not provide a complete per-action progression ledger. No explicit LEVEL value or level-reset marker was captured. The M24 Level change had no subsequent action, so reset behavior was not exercised.

Three immediate same-path repeats followed a public zero-change observation: Output preparation repeated at M18 with no subsequent Output change; Network maintenance and Output preparation each repeated at M21, and the repeated actions then produced public gains. Those later gains are evidence against inferring a cap, but the repeated choices and missing normalized Board response do not support reliable NO_GAIN routing. Classification: **NOT_SUPPORTED**.

### Recovery taxonomy

| Type | Run evidence | Assessment |
|---|---|---|
| PROGRESSION | Five explicit markers: four around M6 and one at M12. Mode stayed A in those windows. The following Reviews remained C/no-promotion at M12 and D/no-promotion at M18. | Tried, but no public Review improvement followed; overall recovery was ineffective for the observed progression failure. No causal action attribution. |
| RESOURCE | No explicit RECOVERY=RESOURCE marker. Health recovery choices appeared as ordinary Energy selections. | Not established as a bounded recovery path. |
| RISK | One explicit RECOVERY=RISK marker at M15. | Public trigger, cleanup linkage, fresh exit evidence and return-to-mainline sequence were not established. |
| DELIVERY | No explicit RECOVERY=DELIVERY marker. | Not established; Delivery marker coverage was incomplete. |

Overall failure recovery is **INEFFECTIVE for the exercised progression path**, with Resource, Risk and Delivery recovery effectiveness inconclusive. No automatic replacement game was authorized.

### MODE control

The CTRL P field is the Candidate’s MODE marker. It recorded **A=68/112 (60.7%)** and **S=44/112 (39.3%)**:

- M9: one S action during a certification/family-time event; the captured public context did not show a material binding constraint. Classified FALSE_STABILIZE.
- M10: one S action during a public neck-pain/deadline event, followed by A. A short health response is plausible, but materiality cannot be confirmed from markers alone; classified QUESTIONABLE.
- M18–M23: 42 consecutive S actions, beginning at a public test-result/delivery-uncertainty event and continuing through later trust, team, work-continuity and health stories. No explicit RECOVERY label accompanied the S state and no return to A was observed before terminal. The later public contexts make trigger attribution mixed, but the unbroken S state and missing exit evidence are not supported by the contract.

No run action can be confidently counted as a fully evidenced VALID_BINDING_CONSTRAINT transition from markers alone. MODE control classification: **NOT_SUPPORTED** for this run. The 42-action late S window is a material strategy/runtime adherence concern; its causal relation to the M24 elimination is UNKNOWN.

### Delivery, Risk and Story semantics

- Delivery markers: 70/112 valid, 42/112 malformed, 0 missing and 0 identity-missing. All 42 malformed markers used n=0 with checkpoint=NEAR; the Delivery Skill requires NOT_NEAR when n=0. Marker presence is not proof of correct item identity, claim/verification lifecycle or delivery recovery. Delivery recovery: **INCONCLUSIVE**; delivery overclaim: UNKNOWN.
- Risk markers: PASS=98 and ALLOW=14; no WARN or RECONSIDER markers; RB=NONE on all 112 actions. The M15 RISK recovery label lacks an auditable public-warning→cleanup→fresh-observe→exit chain. Risk cleanup: **INCONCLUSIVE**.
- M18 spot check: the public test description said the demo path was unusually favorable; the selected legal action was to retest and provide a realistic capacity report. This choice is aligned with the participant-visible context. Other trust, confidentiality, hotfix, work-continuity and health stories were encountered, but the notes do not preserve enough public-only Planning rationale to certify their semantic handling as a group. No event-ID or hidden-effect mapping was used in the report.

## Runtime and Skill coordination

- **Action→observe:** the unique tool-call sequence contains 112 action calls, each immediately followed by same-session observe; there was one additional initial observe. No stale multi-action chain was found.
- **Whole-game persistence:** the Runner continued through the fresh session to the structured natural terminal at M24. The M24 terminal, not a local cutoff, ended gameplay.
- **CTRL:** 112/112 notes had valid single-integer choice markers; closure-marker consistency passed 112/112. This does not establish semantic READY/preflight correctness.
- **Tool route/results:** 16 calls used a noncanonical tool route name. These correspond to 16 unknown result classifications; the remaining 96 were parsed success and 0 parsed error. All 112 were followed by fresh observe, but the 16 unknown receipts remain an interface/audit limitation.
- **Board:** public state snapshots were available, but the response ledger was incomplete: 18 mentions, 7 not parseable into S/N/O, no explicit Level key, and no REVIEW_PLAN blocks. Full Board-fidelity coverage was not separately established.
- **Delivery:** marker contract failed on 42 actions as described above; lifecycle adherence is not established.
- **Planning:** no explicit REVIEW_PLAN was recorded; S remained active for 42 actions with no recorded recovery/exit.
- **Risk:** only PASS/ALLOW outcomes were marked; no reconsideration branch was used.
- **Context recovery/compression:** no observable compression/recovery signal was established. No safely scoped llm.log was supplied, so compression count and recovery adherence are **UNKNOWN**. Four Skill reads were recorded at startup; no later Skill reread or recovery sequence was observed.
- **Execution boundaries and continuation sends:** UNKNOWN; the event stream does not provide a trustworthy count. Provider-error zero-work terminations: none observed.

### Evidence firewall and process issues

The post-run audit counted 16 numeric HiddenRisk text matches in the transcript and 0 in action notes; numeric internal-score matches were 0. This is a text-match audit, not a semantic verdict, and the evidence firewall does not pass.

Offline forensic tooling incurred two accidental non-public renderings: a temporary choice diagnostic included a non-public choice metadata field in output once, and the default staged diff check echoed raw event JSONL lines while reporting CRLF as trailing whitespace. Neither rendering was used as evidence for the strategy classifications or copied into narrative findings; subsequent calculations used only participant-visible action labels/descriptions and public state snapshots. This is a forensic handling deviation for Stage review. The raw evidence was not altered.

Avoidable process issues, with no additional live budget consumed:

1. The controller failed while serializing a thread object into post-run JSON after Runner terminal and cleanup. Prevention candidate: serialize an allowlisted JSON-only metadata object before writing.
2. The first audit invocation had a local path typo and failed before reading the input artifacts. The corrected invocation produced the one-pass summary. Prevention candidate: validate all explicit artifact paths before starting the audit.

## Evidence archive and validation flags

The canonical archive scanner passed for all five explicitly selected core artifacts. The manifest records the exact event window. Raw Runner/service console logs, .env, credentials, shared DB, unrelated sessions and unscoped llm.log were not archived. Local raw evidence remains preserved; **FORENSIC_HOLD=ACTIVE** pending Stage/Main review.

Archive: [s09-run01-v7w](../../../artifacts/dev-runs/s09-run01-v7w/)

### FORENSIC_HOLD

- **Status:** ACTIVE.
- **Reason:** early natural terminal plus unresolved runtime/strategy adherence findings, 16 unclassified action receipts, transcript evidence-firewall matches, and the offline analyst handling deviation require independent Stage/Main review.
- **Minimum retained scope:** the five core artifacts listed below, scoped to 2026-09-30 10:04:36.443046–10:16:52.679839 UTC. Tracked archive: artifacts/dev-runs/s09-run01-v7w/. Exact local Runner source: D:\CS\CareerSim\.career_sim_runner\career_emu\outputs\local-s06-adaptive-controller\20260930T100431Z\. Local task summary/reconstructed result: D:\CS\CareerSim\.local\runtime\s09-run01-v7w\.
- **Responsible Task / release authority:** S09-RUN01; Stage/Main review owner.
- **Release condition:** Stage/Main independently confirms run/session identity, classification, Candidate flags and evidence-firewall disposition, then records that the required raw sources are recoverable or no further re-analysis is needed. Any later deletion requires explicit file-scoped cleanup authorization. Hashes and archive creation alone do not release this hold.

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| events.jsonl | 1,263,074 | 62b4ad52660b0a8fc937aeab2f51c62063d108d4775f90ff253a1ff3c974561e |
| transcript.log | 279,317 | bf22f228148e21e52a64cd39144ac88f01e6aad6b5c898f75fa0f925f8911f09 |
| score_report.json | 2,751 | e239b48319dd8571676815a73c86626c89f753079985c37194829c663c6178ad |
| runner-result.json | 1,431 | 10b34563632e059a912c7d8a57960c250c2a3efcb1cb24b0d9b33ac88ecd54bb |
| post_run_summary.json | 141,918 | 4190698608450983fca25b65a95c5adb497835335b0719f3bc0741ba23ef9a7f |

Candidate validation metadata after this run:

- gameplay_validated=true; provider_validated=true for this fresh session only.
- runtime_validated=false; long_horizon_adherence=false.
- survival_improvement_proven=false; score_improvement_proven=false; stable_80_plus_proven=false; hidden_test_transfer_proven=false.
- next_game_authorized=false.

No validation transfers from another Candidate or session.

## Final classifications

| Dimension | Classification |
|---|---|
| Run | EARLY_NATURAL_TERMINAL |
| Early Promotion Engine | NOT_RESTORED |
| Failure Recovery | INEFFECTIVE for exercised PROGRESSION; other types inconclusive |
| MODE control | NOT_SUPPORTED |
| NO_GAIN routing | NOT_SUPPORTED |
| Delivery Recovery | INCONCLUSIVE |
| Risk Cleanup | INCONCLUSIVE |
| Score ceiling | NOT_EXERCISED |
| Failure floor | Negative M24 natural-elimination evidence |
| Runtime adherence | FAIL / limitation; runtime_validated remains false |
| Long-horizon adherence | NOT_EXERCISED |
| Stable 80+ | NOT_PROVEN |
| Score/survival causal improvement | NOT_PROVEN |
| Hidden-test transfer | NOT_PROVEN |

## TASK_RESULT

- Base: main@d94b178e3e7867b80673c4dfecd2e70dd66272b5; candidate parent chain v7v→v7w.
- Final repository commit SHA: returned in the final TASK_RESULT after commit/push, avoiding a self-referential hash in this file.
- Run classification: EARLY_NATURAL_TERMINAL; fresh-session consistency PASS.
- Runner SHA: f61c738c72e51b77298cc1c14c7c6ebf4b6c527d.
- Authorization consumed: YES; one game, one Runner play, one service lifecycle; no replacement.
- Remote and working tree: recorded after push.
- Evidence archive: scanned and staged at artifacts/dev-runs/s09-run01-v7w; FORENSIC_HOLD remains ACTIVE pending Stage/Main review.
- Recommendation: return to Stage/Main to review the early-promotion failure, prolonged S mode, incomplete progression/Delivery markers, transcript evidence-firewall matches and the offline analyst deviation. Do not implement a Candidate patch or authorize another game in this task.

S09_RUN01_GAME_AUTHORIZATION = CONSUMED
NEXT_GAME = NOT_AUTHORIZED
NO_REPLACEMENT_RUN_AUTHORIZED
