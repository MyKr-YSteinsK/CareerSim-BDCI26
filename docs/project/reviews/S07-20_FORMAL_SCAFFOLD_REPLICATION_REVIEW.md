# S07-20｜Formal Candidate Scaffold Strong-Host Replication Review

## Review decision

`STRONG_HOST_NO_SIGNAL`

The stronger decision host did not produce a descriptive gameplay improvement over S07-19 or the completed prior Codex public-agent observations. The formal controller was auditable for a substantial partial run, but the run ended naturally at M24 with `16.98 / 11.89 / 24m / E`; the pre-review reserve evidence remained `PARTIAL`. This is not a model-causal result and does not justify a Candidate or Skill mutation.

## Acceptance review

| Criterion | Result | Evidence |
|---|---|---|
| 1. Latest main + S07-19 evidence verified | `PASS` | `HEAD == origin/main == 99fa141db649325d08d6ab59a36011033fa10c61` before live run; S07-19 run/review present |
| 2. Exact Candidate/manifest/three Skills fresh-read | `PASS` | Current identities and hashes recorded in the run document before `new_game` |
| 3. Player-phase current-session firewall | `PASS` | Historical strategy, S07-19 trajectory, score targets, hidden/private evidence: all `NO` during gameplay |
| 4. One fresh game, Single Agent, bridge `NO_POLICY_LOGIC` | `PASS` | One session, one `new_game`, 96 explicit choices, direct MCP only, no bridge patch |
| 5. Formal controller ledger and reserve correction | `PARTIAL` | 96 canonical CTRL records and core loop are auditable; M6 reserve record exists, but M12/M18 last-window reserve records were not captured contemporaneously |
| 6. Terminal outcome/checkpoints | `PASS` | M6/M12/M18/M24 reached and recorded; M30/M36/M42/M48 `NOT_REACHED` |
| 7. Safety exclusions and mutation boundary | `PASS` | Provider/AgentServer/Runner/install/reload/second game/private access/Candidate mutation all `0` |
| 8. Verification, commit/push, clean tree | `PASS` | Targeted tests and schema check passed; final diff check, commit/push, and clean-tree verification completed |

## Gameplay result

- Session: `e3e175e2b286478fa3266f614f606134`.
- Quantitative / competition partial: `16.98 / 11.89`.
- Survival / grade: `24m / E`.
- Terminal: `L1 / Health 5 / Dignity 5 / Skill 9 / Network 2 / Output 3 / Wealth 4 / Energy 0`.
- Promotions: none.
- Public terminal: `eliminated`, `completed=false`.

### Checkpoints

| Run | M6 | M12 | M18 | M24 | M30–M48 |
|---|---|---|---|---|---|
| S07-20 | `L1/H9/D10/S9/N3/O3/W2` | `L1/H10/D10/S9/N3/O3/W1` | `L1/H8/D7/S9/N3/O3/W2` | `L1/H5/D5/S9/N2/O3/W4` terminal | `NOT_REACHED` |

## Post-terminal descriptive comparison

| Run/reference | Quantitative | Partial | Survival | Grade | Terminal/last Level | Terminal Output | Terminal Wealth |
|---|---:|---:|---:|---|---|---:|---:|
| S07-20 formal strong-host replication | 16.98 | 11.89 | 24m | E | L1 | 3 | 4 |
| S07-19 formal scaffold parity | 28.89 | 20.22 | 24m | E | L1 | 3 | 7 |
| S07-14 bare/research Codex | 65.16 | 45.61 | 48m | B | L5 | 37 | 25 |
| S07-17 R3 targeted-prior Codex | 63.88 | 44.72 | 48m | B | L5 | 26 | 27 |
| Candidate v1 #1 historical reference | 76.04 | 53.23 | 48m | A | completed | — | — |
| Original v6 #1 historical reference | 75.29 | 52.70 | 48m | A | completed | — | — |

Descriptive deltas versus S07-19 are `-11.91` quantitative, `-8.33` partial, equal `24m/E` survival/grade, equal terminal Level/Output, and `-3` terminal Wealth. The sessions were unseeded and unpaired; event path, opportunity path, host, and controller context are not matched controls. The comparison cannot separate decision-host/model capability, scaffold/policy, or stochastic trajectory variance.

## Runtime adherence summary

### Strong evidence

- All three current formal Skills and the runtime instruction were fresh-read before `new_game`.
- The bridge passed the integer choice and canonical notes contract through unchanged and did not select actions.
- The loop used fresh public observe → Board → Planning → candidate → Risk → action, with a public observe after every action response.
- The ledger recorded one Primary Gap, public Progress, Risk Budget, candidate, candidate-specific Risk, CTRL note, and public rationale for 96 actions.
- Energy was sent one integer at a time. The report-preparation path was only switched after two adjacent comparable no-progress observations, then one different legal path was compared.
- M6, M12, and M18 formal feedback caused Planning resets; no action was sent after terminal.

### Partial evidence and limits

- The Plan required an explicit survival-buffer reserve check in the last actionable window before each known half-year review. A separate record was captured around M6, but the M12 and M18 windows were not recorded as distinct reserve checks before the review. This remains `PARTIAL`.
- No context-recovery epoch occurred, so recovery reread behavior is `NOT_TRIGGERED`, not validated.
- The natural M24 terminal leaves M30–M48 adherence and promotion behavior `NOT_REACHED`/`UNKNOWN`.
- The public runtime did not expose a seed/replay control; the run is therefore unpaired and stochastic.

## Interpretation matrix

### FACT

- Formal scaffold execution was substantially more explicit and auditable than a free-form transcript: 96 canonical action notes, 97 observes, and one direct MCP lifecycle.
- The result was lower than S07-19 and far below completed S07-14/S07-17 and historical 48-month references.
- The run remained L1 through terminal and never produced a promotion.

### INFERENCE

- Under this unpaired observation, the formal scaffold did not create a positive strong-host signal.
- The repeated M18 adverse review and M24 elimination make scaffold/Candidate policy a plausible bottleneck hypothesis, especially the conversion from visible work and risk repair into promotion/recognition.
- That hypothesis is more valuable for review than a host/model verdict, because the experiment does not control event path or provide a matched host comparison.

### UNKNOWN

- Whether a different decision host would have produced a different action path under the same public events.
- Whether the M24 elimination is repeatable or stochastic.
- Causal contribution of any Skill, report/relationship action family, or formal notes contract.
- Hidden-test transfer, stable 48-month formal adherence, and any claim of stable 80+ performance.

## Scaffold / Candidate Review Proposal

No implementation is authorized or included.

- Observed issue: repeated public work/relationship actions created some local improvements, but the run remained L1 and accumulated adverse formal feedback about collaboration, risk, and output/level mismatch.
- Supporting public evidence: M18 formal review (`D -0.6`, explicit final adjustment window) followed by M24 public elimination; Output was only 3 at terminal and no promotion occurred.
- Counterevidence: the run reached M24 with a functioning formal loop; public Output/Network/Health sometimes improved; the CTO architecture transfer at M23 shows that not every visible contribution failed to create opportunity.
- Confidence: high for the observed trajectory; low for causal attribution or a universal policy diagnosis.
- Smallest next experiment, if Main later authorizes one: review this no-signal run and the `PARTIAL` reserve evidence first, then design a single-change candidate/policy audit before authorizing another live game. Do not automatically rerun.

## Safety accounting

- Sessions: `1`; `new_game`: `1`; direct MCP lifecycle: `1 start / 1 shutdown`.
- Observe: `97`; `take_action`: `96`; unknown side effects: `0`.
- AgentServer: `0`; provider/DeepSeek: `0`; Runner gameplay: `0`; install/reload: `0/0`; second game: `0`.
- Hidden/private evidence access: `0`; formal Candidate/Skill/manifest mutation: `0`.
- Raw SQLite and emulator logs remain local under the ignored runtime directory and were not opened.

## Verification actually passed

- `tests/test_codex_public_agent_driver.py`: `10 passed`.
- `tests/test_public_mechanical_probe.py`: `18 passed`.
- Public schema/behavior contract: passed.
- Canonical CTRL audit: `96/96` valid; public trajectory action/observe counts: `96/97`.
- Final `git diff --check`, commit, push, `main == origin/main`, and clean working tree: passed at delivery.

## TASK_RESULT — S07-20

### Result

- Status: `Complete` for the authorized one-game replication, required evidence, repository delivery, and plan-copy request.
- Branch / Commit: `main`; exact final commit is recorded in the final response after push.

### What Changed

- Added `docs/project/runs/s07-20-formal-scaffold-replication.md`.
- Added this review `docs/project/reviews/S07-20_FORMAL_SCAFFOLD_REPLICATION_REVIEW.md`.
- Preserved Candidate, manifest, Skills, Runner, dependencies, `CURRENT_STATE.md`, and ADRs unchanged.
- Retained public trajectory and compact ledger only as ignored local runtime evidence; raw DB/logs were not committed.

### Verification Actually Passed

- Baseline fetch, latest-main check, working-tree checks, S07-19 evidence presence, shared-runtime process gate, and formal identity checks.
- Root-Python targeted tests: `28 passed` total.
- Public schema/behavior check and canonical notes audit.
- Final `git diff --check`, commit/push, remote alignment, and clean working tree.

### Plan Deviations

- Pre-review reserve evidence is `PARTIAL`: M12 and M18 did not receive separate contemporaneous reserve records before their formal reviews. No live retry, budget expansion, or evidence retrofit was performed.
- The game naturally terminated at M24; no second game was authorized or started.

### Material Project-State Changes

- `PROJECT_BRIEF`: none.
- `DECISIONS`: none.
- `CURRENT_STATE`: none.

### Remaining Risks / Known Limits

- The result is unpaired, stochastic, and not a causal host/model comparison.
- Long-horizon formal adherence after M24 is not observed.
- The `PARTIAL` reserve evidence limits a full adherence claim.
- No Candidate/Skill mutation is justified by this run.

### Checkpoint Signal

- `Checkpoint Review recommended: review the no-signal result and partial reserve evidence before any later live authorization.`

### Suggested Next Boundary

- Main review of this descriptive no-signal result; do not automatically start another game.

## Execution metrics

- Model Used: `UNKNOWN`.
- Reasoning Effort: `UNKNOWN`.
- Started At: `2026-09-26T15:01:53Z`.
- Finished At: `2026-09-26T15:18:51Z`.
- Actual Wall-clock: `16m58s` for the live run; total task wall-clock not separately captured.

## Execution issues

- Avoidable Execution Issues: `1`.
- Categories: `controller_ledger / pre_review_reserve_recording`.
- Consumed Live Budget: `NO`.
- Prevention Candidate: record and verify the reserve check before each final pre-review action window.
