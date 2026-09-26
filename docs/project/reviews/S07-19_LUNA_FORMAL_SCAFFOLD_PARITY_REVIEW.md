# S07-19｜Luna Formal Candidate Scaffold Parity Review

## Review decision

`SCAFFOLD_PARITY_MIXED`

The run shows substantial formal-controller execution evidence, but not a complete long-horizon validation: the session naturally ended at M24, the pre-review reserve checks are only partially auditable, and the public result was `28.89 / 20.22 / 24m / E`. This is not a positive parity signal and does not establish a model or scaffold causal explanation.

## Acceptance review

1. Latest `main` and closeout handoff: `PASS`; `HEAD == origin/main == 9602928e5fa3e5a087f8e8dbead63680deb093ea` before gameplay, with `FORMAL_CANDIDATE_SCAFFOLD_PARITY_READY` verified.
2. Exact Candidate, runtime instruction, and three Skills: `PASS`; all were fresh-read before `new_game`, and their identities/hashes are recorded in the run record.
3. Player-phase firewall: `PASS`; historical prior `NO`, S07-16 brief `NO`, hidden/private evidence `NO`.
4. One fresh game and Single Agent: `PASS`; direct MCP only, one `new_game`, 98 explicit choices, bridge remained `NO_POLICY_LOGIC`.
5. Board → Planning → candidate → Risk → action: `PASS` for the 98-decision compact ledger; canonical CTRL notes were `98/98` valid.
6. Outcome and M6–M48 checkpoints: `PASS`; M6/M12/M18/M24 recorded, M30/M36/M42/M48 explicitly `NOT_REACHED`.
7. Safety exclusions and mutation boundary: `PASS`; provider/AgentServer/Runner/install/reload/second game/hidden-private access/Candidate mutation all `0`.
8. Targeted verification and delivery: `PENDING_FINAL_COMMIT` at authoring time; the final commit/push and clean-tree state must be recorded with this review.

## Runtime adherence summary

### Strong evidence

- The current formal manifest and all three formal Skills were loaded before gameplay.
- The bridge schema visibly supported the formal `notes` channel; no patch was needed because the bridge passed the exact canonical CTRL prefix through unchanged.
- Every decision was preceded by a fresh public state. The bridge performed one fresh public observe after every completed action response, including the one explicit rejection.
- The ledger kept Board facts, Planning state, candidate, and candidate-specific Risk separate. It did not use a hidden threshold, fixed action ranking, event-title answer map, or cross-session memory.
- Energy actions were submitted as one integer at a time. Repeated report-preparation actions were not labelled `STALLED` until two comparable no-effect observations; the ledger then compared a different legal path.
- M6, M12, and M18 formal feedback invalidated the prior Progress baseline and caused a Planning reset. No post-terminal action was sent.

### Partial evidence / limits

- The formal controller requires a fresh survival-buffer reserve check before the last action window preceding a known half-year review. The run's surrounding Board/Planning records used current Health, warning, and Risk Budget facts, but they do not contain a distinct, consistently labelled reserve-check record before M6, M12, and M18. This is `PARTIAL`, not silently upgraded to `PASS`.
- No context recovery epoch was triggered, so that branch is `NOT_TRIGGERED`, not validated.
- The game terminated at M24. Runtime adherence after M24 and any M30–M48 promotion/terminal path are `UNKNOWN`/`NOT_REACHED`.

## Gameplay result and descriptive comparison

| Run | Quantitative | Partial | Survival | Grade | Terminal level | Terminal Output | Terminal Wealth |
|---|---:|---:|---:|---|---|---:|---:|
| S07-19 formal scaffold | 28.89 | 20.22 | 24m | E | L1 | 3 | 7 |
| S07-14 bare/research Codex | 65.16 | 45.61 | 48m | B | L5 | 37 | 25 |
| S07-17 R3 targeted-prior Codex | 63.88 | 44.72 | 48m | B | L5 | 26 | 27 |
| Candidate v1 #1 historical reference | 76.04 | 53.23 | 48m | A | — | — | — |
| Original v6 #1 historical reference | 75.29 | 52.70 | 48m | A | — | — | — |

The comparison is descriptive only. Sessions were unseeded and unpaired; action path, event/opportunity path, host, and controller history differ. The formal run's M6/M12/M18/M24 states were respectively `L1/O3/W2`, `L1/O3/W3`, `L1/O3/W4`, and `L1/O3/W7`, with no promotion. The result therefore does not isolate Luna/model capability from trajectory variance or the remaining adherence gap.

## Research questions

### Q1 — Scaffold adherence

FACT: Codex/Luna sustained the formal Board → Planning → candidate → Risk → action loop for 98 decisions and reached M24 with auditable canonical notes. INFERENCE: this is meaningful evidence that the scaffold can organize a single agent for a substantial partial run. UNKNOWN: reliable 48-month adherence; the natural terminal and partial pre-review reserve evidence prevent a full long-horizon claim.

### Q2 — Compared with prior Codex routes

FACT: runtime organization was materially more explicit than the prior bare/research runs because the ledger and CTRL prefix recorded the formal control stages. FACT: the early/final trajectory was not better: the run remained L1 through M24 and ended at E, below the completed B-grade prior Codex runs. INFERENCE: formal organization alone did not yield a visible performance improvement in this observation.

### Q3 — Model versus scaffold

FACT: a formal Candidate scaffold was present, while the run still ended at M24. INFERENCE: this single observation weakens a strong version of “previous low scores were mainly scaffold mismatch,” but it cannot distinguish model, unseeded event path, partial reserve-check adherence, and other confounders. The appropriate result is mixed/inconclusive for causal attribution, not a Luna-versus-DeepSeek conclusion.

## Candidate implication

`defer` — no change to `configs/current_candidate.json`, `configs/runtime_manifest.json`, or any formal Skill is justified. The run is evidence for a bounded parity observation, not for a strategy redirect or a new threshold.

## Safety accounting

- Sessions: 1; `new_game`: 1; direct MCP lifecycle: 1 start / 1 shutdown.
- Observe: 99; `take_action`: 98; explicit rejection: 1 confirmed unchanged; unknown side effects: 0.
- AgentServer: 0; provider/DeepSeek: 0; Runner gameplay: 0; install/reload: 0; second game: 0.
- Hidden/private evidence access: 0; formal Candidate/Skill mutation: 0.

## Verification actually passed

- `tests/test_codex_public_agent_driver.py`: 10 passed.
- `tests/test_public_mechanical_probe.py`: 18 passed.
- Public-schema/behavior contract: actual listed tools included `new_game`, `observe`, and `take_action`; `take_action.choice` was declared integer and `notes` string.
- Canonical-note audit: 98/98 valid; ledger: 98/98 records.
- Public trajectory and ledger bytes/SHA-256 recorded in the run document.
- Final `git diff --check`, commit, push, and clean-tree state: to be recorded after delivery.

## TASK_RESULT — S07-19

### Identity

- Status: `Complete` for the authorized one-game task; natural terminal is recorded, not retried.
- Decision: `SCAFFOLD_PARITY_MIXED`.
- Base: `main@9602928e5fa3e5a087f8e8dbead63680deb093ea` = `origin/main` before execution.
- Candidate: `candidate-v6c-compliance-cleanup`.
- Authorization: `AUTHORIZE_S07_19_LUNA_FORMAL_SCAFFOLD_PARITY`.
- Commit / Remote / Working Tree: exact final SHA is recorded in the final TASK_RESULT response; push and clean-tree checks are completed at delivery.

### Player-phase integrity

- Historical strategy prior used during gameplay: `NO`.
- S07-16 brief used during gameplay: `NO`.
- Hidden/private evidence used during gameplay: `NO`.

### Scaffold loaded

- Runtime manifest instruction: loaded before gameplay.
- `structured-state-board`: loaded before gameplay.
- `rolling-planning`: loaded before gameplay.
- `risk-review`: loaded before gameplay.
- Loaded before gameplay: `YES`.

### Runtime adherence

- Board: `PASS`
- Planning: `PASS`
- Primary Gap: `PASS`
- Progress: `PASS`
- Risk Budget: `PASS`
- Candidate-before-Risk: `PASS`
- Candidate-specific Risk: `PASS`
- `DECISION_CLOSED`: `PASS`
- Energy single-action: `PASS`
- Fresh observe: `PASS`
- Review reset/checkpoint: `PASS`
- Pre-review reserve: `PARTIAL`
- `STALLED` if triggered: `PASS`
- Recovery epoch if triggered: `NOT_TRIGGERED`

### Run

- Session: `638c45c96e1c45838ba2ee52fd20f759`
- Quantitative / partial: `28.89 / 20.22`
- Survival / grade: `24m / E`
- Final: `L1 / Health 10 / Dignity 7 / Skill 9 / Network 1 / Output 3 / Wealth 7 / Energy 0`
- Promotions: none.

### Checkpoints

- M6: `L1 / H6 / D10 / S9 / N3 / O3 / W2`
- M12: `L1 / H6 / D10 / S8 / N3 / O3 / W3`
- M18: `L1 / H6 / D10 / S9 / N3 / O3 / W4`
- M24: `L1 / H10 / D7 / S9 / N1 / O3 / W7`, terminal.
- M30/M36/M42/M48: `NOT_REACHED`.

### Post-terminal comparison

- Versus previous Codex public-agent runs: formal runtime organization was stronger and auditable; the observed score/survival trajectory was worse than completed S07-14 and S07-17 R3 runs.
- Versus historical 75+ references: current run remained far below the descriptive 75.29/76.04 completed results; no causal inference is valid.

### Interpretation

- FACT: formal scaffold loaded and mostly followed through M24; terminal result was low and eliminated.
- INFERENCE: the run does not support scaffold mismatch as the sole explanation for earlier low Codex results.
- UNKNOWN: model effect, causal Skill/action effect, repeatability, hidden-test transfer, and 48-month formal adherence.

### Candidate implication

- `defer`; no Candidate/Skill modification.

### Execution metrics

- Model Used: `UNKNOWN`
- Reasoning Effort: `UNKNOWN`
- Started At: `2026-09-26T14:24:22Z` (direct MCP live run)
- Finished At: `2026-09-26T14:42:49Z` (terminal and shutdown)
- Actual Wall-clock: `18m27s` for the live run; total task wall-clock was not separately captured.

### Execution issues

- Avoidable Execution Issues: `1`
- Categories: `diagnostic_harness` (one local ledger patch context mismatch; no MCP call or live state change)
- Consumed Live Budget: `NO`
- Prevention Candidate: inspect the current ledger tail before appending a patch.

### Suggested next boundary

Main review of this mixed result and partial pre-review-reserve evidence; do not automatically start another game.
