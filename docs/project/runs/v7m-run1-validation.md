# v7m Run #1 Validation

- **Task:** S07-46 — one authorized v7m runtime attempt
- **Classification:** `TECHNICAL_FAILURE_DURING_GAMEPLAY`
- **Review state:** `PENDING_MAIN_REVIEW`

## FACT

- Launch base was `main@e0d92ab720395894ce6a109c424bc92ef393010c`; the pre-run working tree was clean. Candidate identity was `candidate-v7m-final-r-recovery-audit-hardening`.
- Manifest SHA-256 was `1bb92ccae8cad01b8586aa57c8f2d49aede28f424b488e0b8d8c570c592fcef9`; instruction SHA-256 was `559a38e29e92f59df57834b62f0cc0fbc47f07e824043d98e2f34a20fd5776c2`. All four Candidate-recorded Skill blobs matched. The generated submission contained exactly the manifest and four Skills, all byte-identical to their sources.
- The active non-secret config identified `MODEL_NAME=deepseek-flash` and `API_BASE=https://api.deepseek.com`. The configured `CAREER_EMULATOR_DB` path was passed to Runner only; the database was not opened, queried, parsed, copied, or hashed.
- The single authorized service start reached listeners `19092`, `20000`, `20001`, and `6173` by `2026-09-29T00:39:03+08:00`. One Runner `play` process (PID `17744`) ran from `2026-09-29T00:39:37.849938+08:00` through `2026-09-29T00:49:20.541221+08:00`, then exited `1`.
- The bounded live stdout query reported an M18 marker. S07-47 independently reconstructed the archived events: one fresh session `2e25b395d04f46c1ba9662f0edef5ea9`, one unique new_game, 85 unique observes and 84 successful actions (zero failures), continuing to M20 at `2026-09-29T00:49:14.721205+08:00`. Last state: L3, H8/D10/S31/N15/O10/W11/E0, alive=true, failed=false. M18 was not the final gameplay state. Runner emitted no `report_path`.
- The Runner-managed output pointer was updated inside the run window and binds `D:\CS\CareerSim\.career_sim_runner\career_emu\outputs\local-s06-adaptive-controller\20260928T163940Z\`. That directory contains `events-20260928T163940Z.jsonl` (890,180 B) and `transcript-20260928T163940Z.log` (258,955 B); it contains no `score_report.json`.
- One graceful stop exited `0`. The known manager status was `stopped`; all four known ports were released. No retry, second play, separate provider probe, or separate install/reload command was issued.
- The one authorized transcript-count pass found 3,742 lines: `Hmm` 298, `reconsider` 94, and `Let me reconsider` 24. S07-40 reference counts were approximately 11,229 / 420 / 120 / 10,283 lines. This is descriptive only.
- The secret-scanned archive is `artifacts/dev-runs/S07-46-v7m-run1/`. It contains events (SHA-256 `4b5f2c2057212e44310397f449ff6f41fe270b1b8c11945ea5a18b57ceb7af8b`), transcript (SHA-256 `f15710f7eede7b1a52c51a80d16a824261fca4508b5f97837c2e3f9265870dbf`), runner-result (SHA-256 `4437d474069db65779e2b071a3b5c86c348fc1f929c095e6aa37cdc393bdaf3c`), and its generated evidence manifest.

## UNKNOWN / LIMITATION

- Fresh identity is confirmed; natural terminal was not observed. Final outcome and score remain UNKNOWN, and 48m completion was not reached.
- S07-47 added missing-score partial support to `post_run_audit.py` and produced `PARTIAL_GAMEPLAY_TECHNICAL_FAILURE`; no synthetic score report or DB substitute was used. CTRL/DL syntax is valid 84/84; G changes once (?20 → O64), P=A/R=PASS/X=- on all actions. See [S07-47 review](../reviews/S07-47_V7M_M20_PARTIAL_RUN_FORENSIC_REVIEW.md) for the separate semantic findings.
- S07-47 found zero numeric HiddenRisk action-note references but seven in the visible transcript: overall EVIDENCE_DISCIPLINE_FAIL. One run-scoped compression was followed by actions without four-Skill reread evidence: RECOVERY_PATH_FAIL. Decision closure materially improved per action, with residual long-tail verbosity. Board state fidelity and Delivery verification have concrete adherence defects.
- Captured Runner stdout/stderr remain local under `.local/runtime/s07-46-v7m-run1/`; their archive slicing limitation is unchanged. S07-47 additionally used the exact failure window of known service logs. Root cause is INSUFFICIENT_EVIDENCE: Runner reports local socket abort/no close frame, and the service later reports an incomplete model stream. No direct mechanism links the read-only status query to this failure; gameplay continued from its M18 marker to M20.
- Archived gameplay and scoped service logs establish successful model responses before the technical failure. This does not satisfy the S07-46 full-run provider/runtime validation gate; its flags remain false. Actual billed cost is UNKNOWN.

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

`configs/current_candidate.json` remains unchanged because this technical attempt does not satisfy the plan's validation thresholds. S07 remains ACTIVE and is returned to Main for review. S07-47 recommends STATIC_PATCH_JUSTIFIED_BEFORE_RETRY for narrow public-evidence/Delivery correctness; it does not authorize a game. S07-38 `FORENSIC_HOLD` remains untouched; S07-47 also retains the necessary local failure/recovery sources on hold. The partial trajectory supports descriptive comparisons, not causal strategy or final-score claims.
