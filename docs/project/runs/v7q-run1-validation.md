# TASK_RESULT｜S08-RUN02

## Status and identity

- Status: `RUN_ACCEPTED_WITH_RECORDED_LIMITATIONS`
- Run classification: `EARLY_NATURAL_TERMINAL`
- Candidate: `candidate-v7q-checkpoint-marginal-progression`
- Parent: `candidate-v7p-score-gap-convergence`
- Plan SHA-256: `087db83e6c74444b70a09177ca87a00468b9ca56ccdef872a59751a0ea067102`
- Base commit: `main@0a7001e67fc4350383382039d592a2b0ceb2b964`
- Initial evidence integration commit: `31c0501249ab4be6a82c3346039290b291fc80ef`.
- Follow-up correction: post-push source reconciliation found the exact transcript session ID; this report records that correction without rewriting the pushed integration commit.
- Final commit: this report's transcript-attribution correction is included in its follow-up commit.
- Remote state: `origin/main` equals the commit containing this report (verified after push).
- Working tree: clean after the final commit/push.
- Fresh session: `e12d08fe0d0b4fb0b4cac12d5123839e`
- Frozen Runner SHA: `f61c738c72e51b77298cc1c14c7c6ebf4b6c527d`
- Runner result: exit 0; one `new_game`; no `--continue`, replacement, or resume.
- Authorization: consumed. Next-game authorization remains false.

## Live execution

- P1 targeted preflight: the authorized targeted suite passed 33 tests before gameplay. Candidate package identity was checked, exactly five package files were present, the active install manifest identified v7q in agent mode, and local `career_emu` `max_retries=2` was confirmed without disclosing secrets.
- One actual bare `jiuwenswarm-start --list` invocation exited 0 from a process whose PATH was prefixed with the repository `.venv\Scripts`; manager reported `career_emu` stopped.
- One service lifecycle started once and reached listeners `19092`, `20000`, `20001`, `6173`. One fresh Runner `play --submission` was entered, with no `--continue`. Runner window: `2026-09-29T14:08:25.530761+00:00`–`2026-09-29T14:18:35.580303+00:00` (10m10.050s); exit 0.
- One graceful `--stop career_emu` exited 0; manager reported stopped, the service-start PID exited, and all four listeners were released. No install outside the Runner play, standalone provider probe, database query, extra lifecycle, retry, or replacement game occurred.
- `scripts/post_run_audit.py` ran once after cleanup. No safely scoped `llm.log` was supplied, so compression/recovery remains `UNKNOWN`.

## Outcome

- The fresh session ended by natural elimination at public M24, after 24 survival months. Quantitative score `26.80`; competition partial `18.76`; grade `E`; completed=false.
- Final public state: Level L1; Health 8; Dignity 7; Skill 9; Network 0; Output 3; Wealth 5; Energy 0.
- Final observe, score report, events, and the transcript's exact `SESSION` marker identify session `e12d08fe0d0b4fb0b4cac12d5123839e`.
- Compared descriptively with v7o (`71.83`, L5, 48 months), this run is `-45.03` quantitative points, ends 24 months earlier, and finishes one observed level lower than the prior final level. Different single-run trajectories do not establish a causal score or survival effect.
- Usage: 20,446,982 input tokens; 76,134 output; 20,523,116 total. Actual billed cost is `UNKNOWN`; Runner-reported `0.0` is not treated as billing evidence.

## L6 and promotion windows

- L6 observed: **NO**. All 98 public observations remained L1; no public Level promotion occurred. The run naturally terminated at M24 before M36–M48.
- Final promotion-checkpoint evidence: M24 was terminal at L1; no post-M24 preparation or next review was observed. Checkpoint preparation is `INCONCLUSIVE`; `L6_NOT_OBSERVED`.
- Formal reviews at M6/M12/M18 each yielded grade C, no promotion, and public Level L1. M24 terminated before another review. First subsequent G markers were M6=`PERF/RISK`, M12=`OUTPUT`, M18=`PERF`; M24 had no subsequent marker because the run terminated.

| Review | Public grade / promotion / Level | First subsequent G | Quarterly Main actions before next review | Pre-next-review Energy S/N/O results; direct Main + Energy totals* |
|---|---|---|---|---|
| M6 | Grade C; no promotion; L1 | `PERF/RISK` | M6 and M9: `申请关键项目` | Energy: Output +1 at M6, then +1/+1 at M9; Main: Output +2/+2. Total observed direct deltas: S 0, N 0, O +7. |
| M12 | Grade C; no promotion; L1 | `OUTPUT` | M12 and M15: `申请关键项目` | Energy: Output 0, Network 0 at M12; Network 0 then Output +1 at M15. Main S/N/O deltas 0. Total: S 0, N 0, O +1; M12 Main also Wealth +1. |
| M18 | Grade C; no promotion; L1 | `PERF` | M18 and M21: `申请关键项目` | Energy: Output +1/0 and Network +1 at M18; Network +1/+1 and Output 0 at M21. Main S/N/O deltas 0. Total: S 0, N +3, O +1. |
| M24 | Terminal before review; L1 | None | No next-review window | Not applicable |

*Totals summarize directly observed Main/Energy action effects only; they do not claim a net month-to-month trajectory including Story and automatic changes. The seven quarterly Main choices from M3 through M21 were all `申请关键项目`. Their public descriptions named dimensions but contained no explicit gain verb; their observed deltas are tracked above and excluded from the clean advertised Energy-pair denominator.

## No-gain routing

- Clean advertised quarterly Energy progression-result pairs: 15; `GAIN=9`, `NO_GAIN=6`, `MIXED_OR_UNATTRIBUTABLE=0`. Five additional quarterly Energy actions did not explicitly advertise an S/N/O progression dimension and are not counted as progression pairs.
- The six clean no-gains were: M3 Network 0; M12 Output 0 and Network 0; M15 Network 0; M18 Output 0; M21 Output 0. `OBSERVED_NO_GAIN` appeared on five; the terminal-horizon M21 Output zero had no marker.

| Routing classification | Count | Evidence interpretation |
|---|---:|---|
| `ROUTED_AWAY` | 4 | M3 Network→Output +1; M12 Output→Network 0; M15 Network→Output +1; M18 Output→Network +1. Three of the four switches showed a gain in the new dimension. |
| `PARTIAL_DIMENSION_DISCOUNT` | 0 | No clean multi-dimension result was mixed. |
| `REPEATED_NO_GAIN` | 1 | M12 Network 0 was followed by M15 Network 0 at the same Level, without a fresh Network gain resetting the evidence. This is one repeated next-choice sequence; there were two subsequent stale Network zero-gain outcomes relative to the M3 precursor. |
| `NO_ALTERNATIVE` | 1 | M21 Output 0 was followed by a Main action with no S/N/O change; the run terminated at M24 before another progression choice. |
| `UNKNOWN` | 0 | All six no-gain observations had a bounded next-choice classification under the public evidence inspected. |

Decision: `NO_GAIN_ROUTING_NOT_SUPPORTED`. Some choices rerouted to a dimension that gained, but stale Network selection recurred while Level remained L1. These public sequences do not establish the hidden cause of any no-gain result.

## Late horizon

- M36–M48 quarterly Energy sequence: not reached.
- M36–M48 Main actions: not reached.
- Late-horizon zero-gain progression actions and responsive dimensions: not observed; absence of evidence is not a zero count.
- Checkpoint preparation classification: `CHECKPOINT_PREPARATION_INCONCLUSIVE`.

## Correctness audit

- Numeric-only false `MODE=S`: 0 confirmed in the bounded lexical audit. Of 62 `P=S` markers, 16 had recognized lexical constraint context; 46 lacked recognized context and remain `UNKNOWN`/unclassified. This is not a semantic pass.
- Skill terminal-score demotion observed: **NO confirmed instance**. One saturation reference was in a negated/protective context; there were no confirmed terminal-score-based Skill demotions. No general Skill-preservation claim follows.
- Board fidelity: `UNKNOWN`; this one-pass audit did not produce durable Board snapshots for a fidelity verdict.
- CTRL/DL: marker consistency passed 97/97 for both. This checks marker coverage/syntax, not semantic correctness.
- Risk: markers `PASS=85`, `ALLOW=12`, `WARN=0`, `RECONSIDER=0`. The bounded public scan found no obvious risk-taking anomaly; elimination cause remains unattributed.
- Hidden-risk text scan: 22 numeric transcript string matches and 0 internal-score matches; these are string matches, not a semantic verdict. Action-note numeric HiddenRisk/internal-score matches were 0.
- Compression/recovery: `UNKNOWN`; no reliably scoped LLM/compressor log was supplied. One final `e2a.complete` boundary was observed; no continuation was sent. The generic post-run audit's classification is not used to override the Plan-specific natural-terminal classification.

## Runtime

- Successful actions: 97/97; observes: 98; action errors: 0; unknown action results: 0.
- Counted execution boundaries: 1; continuation sends: 0; `max_continuations`: not reached; Runner-boundary zero-work provider-error terminations: 0.
- `new_game`: 1. `career_emu` lifecycle: 1. Graceful cleanup: passed once; all expected listeners released.
- Service retry config: local `max_retries=2` confirmed; effectiveness/portability is not inferred from this one run.

## Evidence and forensic hold

- Plan: `D:\CS\temp\CareerSim\S08-RUN02-v7q-L6与边际成长正式验证.md`; SHA-256 above.
- Exact Runner output directory: `.career_sim_runner/career_emu/outputs/local-s06-adaptive-controller/20260929T140828Z/`.
- Local evidence: `.local/runtime/s08-run02/`. Archived core evidence: [artifacts/dev-runs/s08-run02-v7q](../../artifacts/dev-runs/s08-run02-v7q/). Archive secret scan and session-consistency scan passed.

| Archived artifact | Bytes | SHA-256 |
|---|---:|---|
| `events.jsonl` | 1,052,155 | `a183ac4167b21b4afe817698e9d3d431a516934d22ab8191fce8bd56b2573ae9` |
| `post_run_summary.json` | 132,979 | `43ff6b36db04258252b7ed77059c538107767a376b683807cb81b6b13cb7a2d5` |
| `runner-result.json` | 812 | `47ada42a6ce37d2e97bcb8424f58a5576e5f8a3a404d1eb7ee5afadd586c1536` |
| `score_report.json` | 2,726 | `750c0db5581ccd214c6312ed63e8637d04d19693ed120aa683c2d1abbb42ef10` |
| `transcript.log` | 196,565 | `cab15ddb26b26049f0a3fb119b7f1d1c95e8f7a6b5628ed51997fd2d3cf1567a` |

- `evidence-manifest.json`: 1,081 bytes; SHA-256 `9cbe6f989a194165d7f8b18c330eacd215f3100613795a9e8726e7457cfeee14`; its run-window fields are `UNKNOWN`. Exact Runner start/end are recorded above and in `.local/runtime/s08-run02/run-artifacts.json`.
- `post_run_summary.json` records compression as unknown; raw service stdout/stderr remain local and were not archived because they are unscoped diagnostic captures. No shared database, `.env`, credentials, or unrelated sessions were archived.
- `FORENSIC_HOLD=ACTIVE`. Reason: the early natural terminal remains under Main/Stage strategy review; compression/recovery are `UNKNOWN`. Session identity matches across events, transcript, and score report. Minimum held evidence is the five archived core artifacts above plus the corresponding local run-scoped originals. Window: `2026-09-29T14:08:25.530761Z`–`2026-09-29T14:18:35.580303Z`. Responsible task: `S08-RUN02`; release owner: Main/Stage after accepting the independent classification and confirming no further raw reanalysis is required. Hashing/archive completion does not release the hold.

## Repository updates and limits

- `configs/current_candidate.json`: `gameplay_validated=true` and `provider_validated=true` for this session. `runtime_validated=false`; survival/score improvement, long-horizon adherence, stable-80+, hidden-test transfer, and next-game authorization remain false.
- Candidate behavior, Skills, Runner, dependencies, retry configuration, and runtime files were not modified. S08 remains active; no Stage completion is asserted.
- Post-edit targeted verification: the Plan-authorized suite passed **33 tests**; Candidate/evidence JSON parsing and the authored-file `git diff --check` passed. The first post-edit test run exposed one stale case-sensitive assertion; it was corrected before the final passing run. Full staged `git diff --check` flags CRLF carriage returns in the archived raw events/transcript (`-text`); byte inspection found no trailing spaces or tabs, and the evidence bytes remain unchanged per manifest. The evidence integration was pushed once as `31c0501`; a documentation-only follow-up commit corrects transcript attribution after source reconciliation. Final branch is `main`; both commits are pushed to `origin/main`.

## Final decision

Decision: `V7Q_RUN_ACCEPTED_STRATEGY_REVIEW`.

```text
S08_RUN02_GAME_AUTHORIZATION = CONSUMED
NEXT_GAME = NOT_AUTHORIZED
NO_REPLACEMENT_RUN_AUTHORIZED
```
