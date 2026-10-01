# HPL-06B — quarterly multi-action forensics and quick restart

## Result / identity

- Classification: `IN_FLIGHT_EVIDENCE`, isolated `research/human-play-lab`; no main merge.
- Parent/source base: HPL-06 candidate `b11a7625ff6fc62f9c58794408b322beb757b2e0`.
- Decision: `HPL06B_QUARTER_MULTI_ACTION_FIX_BLOCKED`.
- Reason for blocked decision: offline public-path regressions pass, and the stored HPL-03 failure is located at the engine's insufficient-energy rejection. The Plan's described legal cost-1 second-action failure is not present in available run evidence, so that separate claim cannot be tied to a root cause or declared repaired.
- Scope addition: the user explicitly requested a two-step UI quick-restart that discards the current game after confirmation and starts a fresh one.

## Failure forensics

- Available failed run: `5e38d8f58a10409b93fdad2f83d09e23`; session `a6dbc5bb069e47e5aeda10a47a2f5e20`; HPL-03 source commit `eafe2b669f531562d772ca6a425ea85d14d0ecdc`.
- Public journal records Month 3 / quarterly energy allocation at Energy 3; choice 2 (Skill Learning, public handbook cost 2) succeeded, Energy became 1, and the same event remained. The next `submission_intent` was again choice 2, cost 2, while Energy was 1. There is no subsequent selection or observation.
- Stored traceback: `RuntimeError: take_action did not return success`, raised in the old `PublicGameAdapter.act()` after `engine.take_action()` returned an unsuccessful receipt. Layer accounting: old controller layer B did not pre-reject energy cost; recorder layer C stored the submission intent; adapter layer D called `take_action()` and translated the unsuccessful receipt into the generic exception; installed public engine layer E rejected the unaffordable action. `receipt.error` itself was not persisted, so the exact message is source-derived, not a captured string.
- Static inspection of the installed HPL venv `career_emulator==1.0.1` shows `_take_energy_action()` returns `success=False` with `Insufficient energy ... 1 remaining` before status updates, energy decrement, save, or log append when cost exceeds remaining Energy. The failed choice's mutation is therefore `NO_MUTATION_CONFIRMED` from this public control flow. The old run files were not modified; the old client manifest's generic `UNKNOWN_AFTER_TECHNICAL_FAILURE` field was not rewritten.
- Local evidence remains at `D:\CS\CareerSim\.local\runtime\human-play-lab\runs\5e38d8f58a10409b93fdad2f83d09e23`, including `staging\public_journal.jsonl`, `scratch\technical_error.log`, and the session log under `runtime\logs\`. The DB was not read. A second older HPL-03 run has the same cost-2-at-Energy-1 pattern. No matching legal cost-1 failure run was located in the available HPL run roots.
- Read-only evidence hashes: `public_journal.jsonl` 276,912 bytes / `eccaab26de988afe8229f68b23cafdefdc5c96bbe82a0c8db358b3336610f078`; `scratch\technical_error.log` 442 bytes / `e4bbc580028bf9230aa2f418a1ac661dcfd3b0c991e18080f586f58f408cb6e2`; session log 6,309 bytes / `ac27d726d3ae69abe32a5c7c7dbd071781a63b348a2a589fd9487dc074bdbe84`.
- `FORENSIC_HOLD` was not added to this run: its observed attempted choice is rejected before mutation by the installed public API path. The run remains retained and excluded from strategy conclusions. If evidence for the separate Plan-described legal action becomes available, classify that run independently and apply the hold rule if mutation outcome is unknown.

## Root cause / current path

- FACT: the stored HPL-03 attempt submitted a visible choice whose public Energy cost exceeded the remaining Energy. `career-emulator==1.0.1` rejected the request without mutation; the older HPL client converted that receipt to the generic adapter `RuntimeError` and recorded a technical failure.
- FACT: current HPL-06 `HumanGameController.choose()` already checks `choice_disabled_reason()` before `recorder.submission()` or adapter invocation. Its current Web state projects over-energy choices as disabled.
- INFERENCE: that guard prevents the exact old cost-2-at-Energy-1 submission, but does not explain the separate user/Plan report of an otherwise legal cost-1 action failing. No simulator rule or API invocation semantics were changed.
- Regression: a test-only `QuarterMultiActionFixture` follows the current controller, adapter, projector, recorder, and Web operation path. Same-event actions pass 3→1→0 and 3→2→0. At Energy 1, cost 2 is rejected before submission and cost 1 remains enabled. Stale revision, concurrent duplicate, insufficient energy, and unknown second-action outcomes cause no extra engine call or automatic retry.

## Quick-restart behavior

- The Web header adds `快速重开`. The first click opens a destructive confirmation dialog; only `抛弃本局并开始新一局` submits the restart operation. Cancel leaves the current run untouched.
- Server-side eligibility requires a current matching run ID and an ACTIVE run with a valid staged receipt authorized by a user start. It checks the exact run root, links, receipt identity/status, and hold markers; it closes the engine's per-session log handler before deleting only that run directory.
- A successfully finalized/exported ending can start a fresh game after the server verifies and deletes only the matching run-ID ZIP. Technical failure, unknown mutation, export failure, forensic hold, stale identity, or cleanup error cannot be discarded through this route. Cleanup error returns without creating a new run. Other `Exports` remain untouched.
- All restart tests use synthetic engines and temporary run directories; no CareerSim `GameEngine.new_game()` or `take_action()` was called.

## Portable release effect

- Application source changed after the v1 ZIP was built. The original ZIP remains byte-identical, but is now obsolete for distribution. `release-manifest.json` records the blocked HPL-06B gate and keeps `ready_to_send=false`.
- HPL-06A separate user-run: `99378884bbb848d1b93545127e5a29b4` / session `cad8b222042f4664ac3fbfc967ec0ceb`; normal public ending at Month 2 / L1, 15.82 quantitative / 11.08 partial / E. `verify_zip()` and ZIP CRC pass for `D:\CS\temp\CareerSim Friend Smoke\run-01\CareerSim-Human-Web\UserData\Exports\CareerSim-local-Score15.82-L1-20261001-182748.zip` (6,845 bytes, SHA256 `94f8fd45469ba522028efe27e684731db1b7b0c3f7dd2ef4e5d93ed690e3375e`); exactly five expected public files, 5 frames, 4 selection frames and 0 unknown fields. Its `UserData\Runs\99378884bbb848d1b93545127e5a29b4` root still contains DB/log/staging data and was preserved. The user reported no Security Center prompt or notable lag; loaded native inventory had 57 Authenticode-Valid modules and the captured Code Integrity check had 0 new events after baseline. HPL-06A cleanup is incomplete, so this run does not open Ready-to-Send.
- The recorded v1 archive SHA256 remains `cb7b2efa2d2b91d1fbba5a1f432692a399310a9dbf5060a4a56eecad12128905` (12,639,545 bytes); HPL-06B does not rebuild or overwrite it.
- No HPL-06C build, portable package smoke, real Human run, or third-party distribution occurred.

## Verification and boundaries

- Targeted tests: 73 passed across HPL-06B quarterly fixture, HPL-05 Web, controller, adapter, lifecycle, and portable contracts.
- Ruff lint and modified-file formatting pass; JS syntax and `git diff --check` pass.
- Real `new_game=0`; real `take_action=0`; Provider/MCP/Jiuwen=0; security-policy changes=0; formal Agent/Candidate/Skills/Runner/root dependency changes=0.
- HPL-06B does not authorize resuming/replaying either failed HPL-03 run or creating a Human game. The unresolved legal-action report must return to Planner with a matching retained public/technical evidence set before HPL-06C.
