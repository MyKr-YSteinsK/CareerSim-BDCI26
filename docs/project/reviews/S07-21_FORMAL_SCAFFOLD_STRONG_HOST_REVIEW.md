# S07-21｜Formal Scaffold Strong-Host Replication Review

## Decision

`STRONG_HOST_INCONCLUSIVE`.

The current formal Candidate produced a clearly different **observed trajectory** from S07-19/S07-20: this one completed 48 months, reached L5, and scored `59.19 / 41.43 / C`. That is a positive descriptive gameplay signal. It is **not** a repository-verified strong-host effect: exact model/effort telemetry is `UNKNOWN`, 135 of 200 per-action controller records were not captured contemporaneously, and the three sessions are unseeded and unpaired. The public score must not be used as a clean host/model interpretation under the Task's adherence rule.

## Acceptance and adherence audit

| Contract | Result | Evidence / limit |
|---|---|---|
| Latest main; S07-19/S07-20 artifacts verified | PASS | `main@63ddbd4` matched `origin/main`; clean pre-game tree; prior run/review presence verified without Player Phase reading |
| Current Candidate, manifest, instruction, three Skills | PASS | Fresh-read before `new_game`; exact hashes in run record; Skills re-read at recovery |
| Current-session-only Player Phase firewall | PASS | Prior trajectories, S07-16, historical score targets, DB/private state, and simulator source not used |
| One fresh game; Single Agent; bridge `NO_POLICY_LOGIC` | PASS | One `new_game`, one session, 200 explicit player choices; second MCP lifecycle was separately user-authorized for same-session recovery |
| Fresh observe before decisions | PASS | 202 `observe` records for 200 actions, including the extra same-session recovery observe |
| Board | PARTIAL | Current public status is reconstructable for all actions; only 65 decisions have contemporaneous compact controller entries |
| Planning | PARTIAL | CTRL markers show selected gaps/progress; full horizon/trade-off not recorded at 135 decisions |
| One Primary Gap | PARTIAL | Exactly one `G` field per action (161 Output, 26 Risk, 7 Health, 5 Network, 1 unknown); contemporaneous Planning proof incomplete |
| Progress | PARTIAL | 87 `A`, 113 `?`, no `S`; per-action comparisons not fully recorded |
| Risk Budget | PARTIAL | Recorded for 65 decisions; retrospective rows explicitly leave it unknown |
| Candidate before Risk | PARTIAL | Choice and risk marker are present for all actions; ordering of the internal gate is not independently provable for 135 |
| Candidate-specific Risk | PARTIAL | 159 PASS, 33 ALLOW, 6 WARN, 2 RECONSIDER markers; supporting public rationale absent contemporaneously for 135 |
| `DECISION_CLOSED` | PARTIAL | Each choice had one canonical note and no blind resend; internal closure step not independently auditable for 135 |
| Energy one integer at a time | PASS | Bridge parser and trajectory contain one legal integer per action; fresh state after each |
| Post-action fresh observe | PASS | 200 action responses reconciled with public observations; 193 changed, 7 unchanged, no ambiguous outcome |
| Formal review reset/checkpoint | PARTIAL | Level/review transitions and selected checkpoint records are present; all resets cannot be proven from the incomplete ledger |
| Pre-review reserve | PARTIAL | Five explicit records; other reached final pre-review windows lack contemporaneous records, including M6, M36, M47 |
| `STALLED` evidence gate | PARTIAL | No `P=S` marker; incomplete contemporary comparisons prevent a stronger negative claim |
| Context recovery | PASS | M42 fresh observe verified same session; all three Skills re-read; compact Board/Planning recovery recorded |

Hard Acceptance Criteria 1–4 and 6–7 are met within the later user-approved lifecycle expansion. Criterion 5 (complete *contemporaneous* controller ledger and every triggered reserve check) is `PARTIAL`. Criterion 8 is completed when the final commit/push and clean-tree check reported in the final TASK_RESULT pass. The 135 retrospective rows are explicitly identified; no decision reasoning was invented to repair that gap.

## Descriptive comparison after terminal

| Run/reference | Quantitative | Partial | Survival | Grade | Last level | Output | Wealth |
|---|---:|---:|---:|---|---|---:|---:|
| S07-21 formal scaffold | 59.19 | 41.43 | 48m | C | L5 | 29 | 24 |
| S07-19 formal scaffold | 28.89 | 20.22 | 24m | E | L1 | 3 | 7 |
| S07-20 formal scaffold | 16.98 | 11.89 | 24m | E | L1 | 3 | 4 |
| S07-14 research Codex | 65.16 | 45.61 | 48m | B | L5 | 37 | 25 |
| S07-17 R3 targeted-prior Codex | 63.88 | 44.72 | 48m | B | L5 | 26 | 27 |
| Candidate v1 #1 historical | 76.04 | 53.23 | 48m | A | — | — | — |
| Original v6 #1 historical | 75.29 | 52.70 | 48m | A | — | — | — |

S07-21 is `+30.30 / +21.21` quantitative/partial points versus S07-19 and `+42.21 / +29.54` versus S07-20; it survived 24 months longer and reached L5. It is `-5.97` versus S07-14 and `-4.69` versus S07-17 R3 in quantitative score. These are unpaired observations, not matched controls. In particular, S07-20's own `Model Used` field is `UNKNOWN`; it is a low-score formal-scaffold sample, not a verified strong-host sample.

## Interpretation

**FACT:** Current Candidate/manifest/Skills were loaded without mutation. One public game completed at 48m/L5, and all 200 public choices carried canonical CTRL notes. Recovery used two direct MCP lifecycles for one session under the user's explicit limit expansion. Only 65 action rows and five reserve checks were documented at decision time.

**INFERENCE:** The completed run weakens a blanket hypothesis that the unchanged formal Candidate scaffold can only produce the S07-19/S07-20 low-score, L1/M24 region. It makes a universal scaffold bottleneck a lower priority than after two low runs. Because the present score is below other completed Codex and historical references, focused policy review remains reasonable. The observation is compatible with a decision-host contribution, an easier unseeded event path, policy execution differences, or their combination; it does not rank them causally.

**UNKNOWN:** Exact execution model and reasoning effort; causal host/model contribution; whether the same public event path under another decision host would differ; repeatability; hidden-test transfer; full 48-month controller adherence at the 135 decisions with missing contemporary ledger fields. The user discussed switching models, then chose not to; this does not establish the model identity.

## Scaffold / Candidate review proposal

- Observed issue: manual control recording did not scale to the full 200-action run; several pre-review reserve windows also lacked an explicit contemporaneous entry.
- Supporting evidence: 65 contemporaneous action rows versus 200 trajectory actions; five reserve rows across eight reached named checkpoints; the public trajectory still verifies action count and notes.
- Counterevidence: the run reached L5/48m with four promotions, 200 valid CTRL notes, same-session observations, and no unknown side effect.
- Confidence: high for the evidence gap and public outcome; low for a strategy or host causal diagnosis.
- Smallest next experiment: before any further live game, Main/Stage should decide whether to authorize **one** verified-model, automatically captured contemporaneous-controller replication. Do not alter the formal Candidate or claim that telemetry/backfill can be inferred from the existing run.

## Safety, verification, and delivery

- One session; one `new_game`; 200 `take_action` attempts (ceiling 350); 202 `observe`; two authorized direct MCP lifecycles, both closed; no second game or post-terminal action.
- Provider/DeepSeek, AgentServer, Runner gameplay, install/reload, hidden/private access, and formal Candidate/Skill/manifest mutation: `0`.
- Root Python tests: bridge `12 passed`; public mechanical probe `18 passed`. Public tool schema and same-session resume behavior passed. `git diff --check` and final Git delivery are recorded at completion.
- Local raw/compact evidence paths, bytes, SHA-256, checkpoints, and timing are in [the run record](../runs/s07-21-formal-scaffold-strong-host.md). SQLite and emulator logs remain ignored and local; they were not read for gameplay or comparison.
- Execution issue: manual ledger capture was incomplete; the planned one-lifecycle budget could not satisfy context recovery after compression because the waiting bridge had no observe-only command. The user approved exactly one same-session reconnection. The first bridge's deliberate interrupt logged `ExceptionGroup`; no action was in flight, and the second connection fresh-observed the same public state before continuing.

## TASK_RESULT

- Status: gameplay and post-terminal evidence complete; repository delivery identity is reported after push.
- Decision: `STRONG_HOST_INCONCLUSIVE`.
- Base: `main@63ddbd428586390ff34633856da155cc42520119`; Candidate `candidate-v6c-compliance-cleanup`.
- Model Used / Reasoning Effort: `UNKNOWN / UNKNOWN` at reliable repository telemetry level.
- Player-phase integrity: historical strategy prior `NO`; S07-19 prior `NO`; S07-20 prior `NO`; historical score target `NO`; hidden/private evidence `NO`.
- Run: `46184830c0864ffba1381f718becbea7`; `59.19 / 41.43`, `48m / C`, completed; final `L5 H9 D10 S102 N37 O29 W24`; promotions at M12/M18/M30/M48.
- Runtime adherence: table above; core planning/ledger evidence and pre-review reserve are `PARTIAL`, so the score is not a validated host/model effect.
- Next recommendation: Main/Stage review the evidence gap and model telemetry contract before deciding on any additional live replication. No second game is part of this Task.
- EXECUTION_METRICS: direct MCP start `2026-09-27T04:06:31Z`; final shutdown `2026-09-27T04:37:24Z`; elapsed `30m53s` including user pause/recovery.
