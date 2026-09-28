# v7m Run #1 Validation

- **Task:** S07-46 — one authorized v7m runtime attempt
- **Classification:** `TECHNICAL_FAILURE_DURING_GAMEPLAY`
- **Review state:** `PENDING_MAIN_REVIEW`

## FACT

- Launch base was `main@e0d92ab720395894ce6a109c424bc92ef393010c`; the pre-run working tree was clean. Candidate identity was `candidate-v7m-final-r-recovery-audit-hardening`.
- Manifest SHA-256 was `1bb92ccae8cad01b8586aa57c8f2d49aede28f424b488e0b8d8c570c592fcef9`; instruction SHA-256 was `559a38e29e92f59df57834b62f0cc0fbc47f07e824043d98e2f34a20fd5776c2`. All four Candidate-recorded Skill blobs matched. The generated submission contained exactly the manifest and four Skills, all byte-identical to their sources.
- The active non-secret config identified `MODEL_NAME=deepseek-flash` and `API_BASE=https://api.deepseek.com`. The configured `CAREER_EMULATOR_DB` path was passed to Runner only; the database was not opened, queried, parsed, copied, or hashed.
- The single authorized service start reached listeners `19092`, `20000`, `20001`, and `6173` by `2026-09-29T00:39:03+08:00`. One Runner `play` process (PID `17744`) ran from `2026-09-29T00:39:37.849938+08:00` through `2026-09-29T00:49:20.541221+08:00`, then exited `1`.
- Runner stdout's last parseable month marker was `18`. Bounded stderr classification found `websockets.exceptions.ConnectionClosedError` and a connection-failure marker. Runner emitted no `report_path`.
- The Runner-managed output pointer was updated inside the run window and binds `D:\CS\CareerSim\.career_sim_runner\career_emu\outputs\local-s06-adaptive-controller\20260928T163940Z\`. That directory contains `events-20260928T163940Z.jsonl` (890,180 B) and `transcript-20260928T163940Z.log` (258,955 B); it contains no `score_report.json`.
- One graceful stop exited `0`. The known manager status was `stopped`; all four known ports were released. No retry, second play, separate provider probe, or separate install/reload command was issued.
- The one authorized transcript-count pass found 3,742 lines: `Hmm` 298, `reconsider` 94, and `Let me reconsider` 24. S07-40 reference counts were approximately 11,229 / 420 / 120 / 10,283 lines. This is descriptive only.
- The secret-scanned archive is `artifacts/dev-runs/S07-46-v7m-run1/`. It contains events (SHA-256 `4b5f2c2057212e44310397f449ff6f41fe270b1b8c11945ea5a18b57ceb7af8b`), transcript (SHA-256 `f15710f7eede7b1a52c51a80d16a824261fca4508b5f97837c2e3f9265870dbf`), runner-result (SHA-256 `4437d474069db65779e2b071a3b5c86c348fc1f929c095e6aa37cdc393bdaf3c`), and its generated evidence manifest.

## UNKNOWN / LIMITATION

- `game_session_id`, `new_game` count, terminal outcome, score, and natural game termination are unconfirmed. No fresh session identity is claimed.
- `post_run_audit.py` was not run because its required score-report input is absent, so it could not produce a valid summary. No synthetic score report or DB-derived substitute was created. Accordingly, CTRL/DL distributions, decision closure, evidence discipline, and compression/recovery classification remain `UNKNOWN`.
- Captured Runner stdout/stderr remain local under `.local/runtime/s07-46-v7m-run1/`. They were not archived as diagnostics because the archive helper requires timestamped lines for run-window slicing and neither captured file contains timestamped lines. No cumulative LLM log was used; compression is `UNKNOWN`.
- Actual provider response validation and billed cost are `UNKNOWN`; a config identity match is not evidence of a completed gameplay response.

## Validation state

- `provider_validated=false`
- `gameplay_validated=false`
- `runtime_validated=false`
- `long_horizon_adherence=false`
- `survival_improvement_proven=false`
- `score_improvement_proven=false`
- `stable_80_plus_proven=false`
- `hidden_test_transfer_proven=false`
- `next_game_authorized=false`

`configs/current_candidate.json` remains unchanged because this technical attempt does not satisfy the plan's validation thresholds. S07 remains ACTIVE and is returned to Main for review. The S07-38 `FORENSIC_HOLD` remains untouched. No causal strategy conclusion is supported by this single failed attempt.
