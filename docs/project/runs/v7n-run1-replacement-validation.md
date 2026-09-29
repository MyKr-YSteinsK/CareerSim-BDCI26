# S07-51R — v7n Run #1 Replacement Validation

## Result

- **Classification:** `PARTIAL_GAMEPLAY_TECHNICAL_FAILURE`. One fresh v7n game session reached M6, remained alive, then Runner exited `1` with `max_continuations`; the run did not reach a natural terminal.
- **Candidate:** `candidate-v7n-public-state-delivery-constraint-hardening`, parent `candidate-v7m-final-r-recovery-audit-hardening`.
- **Validation:** this partial run is evidence for the observed M1–M6 behavior only. `runtime_validated`, `gameplay_validated`, `provider_validated`, `long_horizon_adherence`, and all improvement/transfer flags remain `false`. No score or 48-month completion is claimed.
- No retry, second game, standalone provider probe, install/reload command, shared DB access, or Candidate/Skill/Runner change occurred. `NEXT_GAME=NOT_AUTHORIZED`; S07 remains ACTIVE.

## Identity and PATH preflight

Base was `main@b967eb47ba9a2d8352f3ef28e295f8d7a30d1a45`, equal to refreshed `origin/main`; the initial tree was clean. Candidate identity, all four formal Skill git blobs, runtime manifest name/mode and instruction digest, Runner lock SHA, root project Python and JiuwenSwarm executable matched. No S07-50 experiment path was referenced by the formal Candidate or manifest. The S07-51 report confirms the preceding v7n play failed before `new_game` on the same bare-name lookup; S07-33R is the accepted precedent where a child PATH correction allowed the Runner to proceed.

| Check | Result |
|---|---|
| Expected CLI | `D:\CS\CareerSim\.venv\Scripts\jiuwenswarm-start.exe` |
| `shutil.which` under the prefixed process PATH | `D:\CS\CareerSim\.venv\Scripts\jiuwenswarm-start.EXE` (same Windows path, case-insensitive equality) |
| Child PATH | repository `.venv\Scripts` prepended; inherited suffix preserved; no user/system PATH change |
| Read-only bare `jiuwenswarm-start --list` | one actual CLI process, exit `0`; `career_emu` reported `stopped` before start |
| Proxy environment | `HTTP_PROXY`, `HTTPS_PROXY`, and `NO_PROXY` present; values withheld |
| `proxy_bypass` | `localhost=true`, `127.0.0.1=true`, `api.deepseek.com=true` |
| P1 classification | `RUNNER_CHILD_ENV_PREFLIGHT_PASS` |

One preliminary helper attempt passed a prefixed `env` only to nested `subprocess.run` while the caller itself retained its original PATH. Windows therefore raised `FileNotFoundError` before creating the CLI process. This was a harmless preflight-harness/tooling error, not a CLI execution or service failure. The launcher was corrected to run with the prefixed PATH itself; the single actual bare CLI execution then passed. `LIVE_RUN_WORKFLOW.md` now makes this requirement explicit and treats `which` alone as insufficient.

## Live execution and cleanup

| Item | Evidence |
|---|---|
| `career_emu` lifecycle | One start; readiness confirmed by manager `running` and all four listeners |
| Runner play | One root `.venv` Python invocation, with the same process-local PATH prefix; PID `30404`; `2026-09-29T16:09:07+08:00` to `16:13:03+08:00` |
| Runner result | Exit `1`; stdout and `score_report.json` report `max_continuations`; stderr also contains an Authlib deprecation warning |
| Fresh `new_game` | Exactly one, producing session `3a8ef7df625a437b885d09072617d436` |
| Graceful cleanup | One absolute-path `jiuwenswarm-start.exe --stop career_emu`, exit `0`; manager reported `stopped`; manager PID `28820`, launcher PID `29052`, and Runner PID `30404` exited |
| Listener release | `19092`, `20000`, `20001`, `6173`: zero listeners after stop |

No gameplay progress was queried while Runner was active. Cleanup passed; it does not change the partial gameplay classification.

## Fresh-session evidence and outcome

The one-pass `scripts/post_run_audit.py` summary reports `events_identity=PASS`, `transcript_identity=PASS`, 1 `new_game`, 23 unique successful observes, and a single fresh session. The transcript session ID and `score_report.session_id` match `3a8ef7df625a437b885d09072617d436`, which differs from the old v7g session `d4464a311c924e73b9e23eebd6f71f6d`.

| Artifact | Bytes | SHA-256 | Location |
|---|---:|---|---|
| Events | 313,536 | `1091b11024eee376d2d0f8dfbc2532fcf66b13dcf9999c6aeb3e7cacc910b8cc` | `.career_sim_runner/career_emu/outputs/local-s06-adaptive-controller/20260929T080910Z/events-20260929T080910Z.jsonl` |
| Transcript | 82,836 | `d334751c957c7317595c7863f9218f97d1224132fbeaac913647dd9ff98db6ba` | same output directory, `transcript-20260929T080910Z.log` |
| Score report | 1,220 | `5309c4840532c2ea41baa1f0743f6cd8512c299415eb339e2157a8ed2f983bbe` | same output directory, `score_report.json` |

No original `runner-result.json` was emitted. For the offline audit only, `runner-result-derived.json` records the captured Runner process exit code from `execution-summary.json`; it does not add or synthesize a score. The deterministic audit summary is local at `.local/runtime/s07-51r/post_run_summary.json`. Raw run and process captures remain local under `.local/runtime/s07-51r/` and the Runner output directory; they were not committed.

The score report is bound to the fresh session, but `ending_score` is empty and the last observe is not terminal. Therefore score is `UNKNOWN`, natural terminal is `NO`, and 48-month completion is `NOT_REACHED`. Reported usage is 3,272,736 input tokens and 28,462 output tokens (3,301,198 total); `total_cost=0.0` is not billing evidence, so actual API cost is `UNKNOWN`.

## Public trajectory and review

Latest fresh public state at each available checkpoint:

| Month | Level | Duration | H | D | S | N | O | W | E |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|
| M1 | L1 | 1 | 3 | 7 | 4 | 3 | 0 | 1 | 3 |
| M3 | L1 | 3 | 6 | 10 | 9 | 3 | 2 | 1 | 0 |
| M6 | L2 | 1 | 4 | 10 | 11 | 7 | 5 | 2 | 0 |

At M6 the public review was C+ and the observed level changed L1→L2. No M12/M18/M24 checkpoint was reached. One quarterly Main Action was recorded at M3 (`申请关键项目`). G remained `?` for the first 20 action markers, then changed once to `Output/performance gap` for the three actions following the M6 review. The review-aligned timing is encouraging but too short to establish sustained planning adherence.

## Targeted Skill and action audit

| Area | Finding |
|---|---|
| Board — public state | **Copy fidelity PASS for observed markers:** all 23 unique action notes could be paired to the preceding fresh observe; month, quarter, H/D/S/N/O/W/L/E had 23 comparisons each and zero mismatches. The run did not independently exercise a salary-text Wealth trap. No `EFFECTS:` field appeared in the 23 action notes, so mixed-event attribution is `UNKNOWN / NOT_OBSERVED`. |
| Board — warnings | The M2 public events inspected for the two S-mode decisions describe a week-long on-call request and a choice between exercise and non-urgent work, not an acute bodily symptom. The Board note describes the public Health value as “deteriorating / survival concern.” That is evidence of numeric-state interpretation, not proof that an explicit acute warning was captured; acute-warning classification remains a concern for Main review. |
| Planning | Markers show `P=A` 21 times and `P=S` twice. Both S markers occur at M2 and cite the displayed Health value as a survival concern; no explicit acute symptom was present in the inspected event text. This appears inconsistent with the no-numeric-threshold / explicit-binding-condition contract. G changed once after the C+ review; whether the new gap accurately reflects full feedback remains limited to this checkpoint. |
| Delivery | DL coverage and syntax are 23/23; no missing identity or malformed marker. Focus IDs are `D1` on 13 actions and `D2` on 6, with four empty states; no ID reuse was observed. Active-count markers were n=0 on 4, n=1 on 14, n=2 on 5, and never n=3. Focus shifted D1→D2 at M5; n later fell from 2 to 1 at M6. The compact marker does not expose the item descriptions/retirement basis, so the reason for that count change is `UNKNOWN`. All tracked items remained `UNVERIFIED`; no `PUBLICLY_VERIFIED` or recognition=1 transition occurred, so false-positive verification was not observed and actual result-verification semantics were not exercised. |
| Risk | Results: PASS=18, ALLOW=5, WARN=0, RECONSIDER=0, UNKNOWN=0; X=`-` on all 23. The bounded challenge set routed the P0/on-call response, exercise over non-urgent work, attribution evidence to a leader, refusal of a competitor inquiry, and proactive client-delay disclosure to ALLOW. No PASS was observed in those selected material-risk examples. The remaining PASS actions were not individually re-adjudicated, so this is `PASS_WITH_LIMITATIONS`, not a universal proof of routing correctness. |
| Evidence discipline | Action-note numeric HiddenRisk/internal-score references: 0. Transcript scan: 5 numeric HiddenRisk text matches and 0 numeric internal-score matches. The parser labels these text matches rather than semantic verdicts; under the Plan's category rule the run is `EVIDENCE_DISCIPLINE_FAIL`. No prohibited value is reproduced here. |
| Decision closure / action correctness | 23 unique action attempts, 23 successes, 0 errors, 0 noncanonical routes; CTRL and DL valid 23/23; marker closure passes on consistency, with X=`-` throughout. `take_action` accepted one integer choice per marker. This proves marker consistency and tool success, not independent simulator legality of every choice. |
| Compression / recovery | `UNKNOWN`: no run-scoped compressor log was supplied to the one-pass audit. This is not classified as recovery PASS or NOT_EXERCISED. |

### Bounded decision-closure measurements

Elapsed time is fresh-observe result→action call from event timestamps. Transcript segments use the 23 final-candidate marker lines as boundaries; they are bounded proxies, not exact transcript tool-call slices. No chain-of-thought is reproduced.

| Metric per decision | Median | p90 (nearest rank) | Max |
|---|---:|---:|---:|
| Observe→action seconds | 6.347 | 14.519 | 24.548 |
| Segment lines | 14 | 75 | 375 |
| Segment characters | 1,442 | 7,075 | 32,846 |
| Hmm | 2 | 17 | 67 |
| reconsider | 0 | 4 | 34 |
| Let me reconsider | 0 | 4 | 27 |

The longest segment is the M3 quarterly Energy allocation decision (32,846 characters / 375 lines). Other high-length segments include M2 exercise-versus-work, M4 Code Review wording, and M5–M6 intern email incidents. Thus marker closure is consistent, but a substantial textual long tail remains; the small 23-action sample and boundary proxy do not support a score or causal conclusion.

## Main review and next step

The run provides useful early evidence: public state echo was exact, M6 promotion occurred, D# identity was used without observed reuse, and several material-risk examples ended in ALLOW. The counterevidence is material: transcript evidence-discipline hits remain, and two S-mode decisions appear to rely on a numeric Health interpretation where the accepted contract requires an explicit public binding condition. Delivery retirement basis and compression/recovery remain unknown; the run stopped before any long-horizon validation.

Main should review the narrow MODE rationale and the five transcript text matches before deciding whether a separate static corrective task is warranted. This report does not patch the Candidate or authorize another game. `NEXT_GAME=NOT_AUTHORIZED`.
