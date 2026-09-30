# HPL-03A — UI stabilization and verified run finalization

Status: `IN_FLIGHT_EVIDENCE / HPL03A_UI_AND_RUN_FINALIZATION_READY_FOR_USER_LIVE_SMOKE`.
Implementation and authorized offline delivery complete; Main acceptance is separate. No Human Run authorization or HPL Stage completion is implied.

## Identity and scope

- Accepted parent: `eafe2b669f531562d772ca6a425ea85d14d0ecdc` (HPL-03).
- Branch/worktree: `research/human-play-lab`, `D:\CS\CareerSim\.local\worktrees\human-play-lab`.
- Observed main: `aa3844c85c982e42a859a18cfc60820df32600a0`; no main merge/rebase. Delivery SHA is the Git commit containing this review, recorded in TASK_RESULT.
- Existing installed GameEngine adapter/API and public projector/writer are unchanged. Flet remains 1.0.1 in the dedicated HPL venv; no installation/dependency/Agent modification.

## UI and action correctness

Three independent scroll columns: seven public stats / event and public feedback / current choices. Header contains Year/Q/Month/Level. Microsoft YaHei UI supplies a single Windows font; titles, sections, body and secondary text have consistent size/weight/color. Cards use readable disabled colors and Material ink feedback. Stable sibling rails avoid moving choices when event text changes; loading state renders before awaited submission. No artificial action delay or new animation framework.

Handbook is a footer button opening a modal from already-filtered public text, without another observe. Recent choices are collapsed by default. Long event/action text wraps. Default-window state tiles are compact; smaller windows retain independent scrolling. Ending shows public final Level separately from Grade and a selectable export path.

UI and controller independently gate insufficient energy. Controller also rejects illegal choices, malformed inputs (including bool/string choice), stale/consumed revision, wrong run ID, and concurrent duplicate callbacks. Rejection means `INVALID_ACTION / NO_MUTATION`, participant-visible message, unchanged public view, no submission journal/canonical transition, ACTIVE retained and engine mutation count zero. Successful sufficient-energy actions still submit once. Engine/receipt/projection/storage/unknown-mutation faults retain the prior fail-closed technical behavior.

## Export and cleanup

Normal end order: finalize canonical artifacts and ended staging receipt → create run-local ZIP → verify → copy exclusively to stable exports → flush/fsync → reverify stable ZIP and exact canonical bytes → delete the verified absolute direct-child run root → display path. Copy is used for publication so source material remains available throughout final verification.

Stable directory: `D:\CS\CareerSim\.local\runtime\human-play-lab\exports`.

Filename: `CareerSim-<participant>-Score<quantitative_score:.2f|NA>-<public final Level|LNA>-<local ended_at YYYYMMDD-HHmmss>.zip`. Sanitized participant defaults to `local`; collision appends `-2`, `-3`, without overwriting or full UUID. Example: `CareerSim-P017-Score68.25-L2-20261001-193412.zip`. Score/Level come only from the last projected public observation; Grade does not supply filename Level.

Exactly five entries: `manifest.json`, `trajectory.jsonl`, `summary.json`, `integrity.json`, `README.txt`. Validate exact names/duplicates/CRC, canonical hashes, run/session identity, frame count, public re-projection, metadata allowlist, portable paths and known secret patterns. No DB, raw logs/transcript, journal, dataset, hidden fields or credentials are added.

Success cleanup removes that run's entire transient root: SQLite, logs, staging, scratch, run-local canonical/export copies and other unheld run-local residue. It never selects an existing run by directory discovery. Links/junctions, independent FORENSIC_HOLD, the exact protected HPL-RUN01, ACTIVE/TECHNICAL_FAILURE/unknown outcomes, missing ended receipt and archive mismatch are rejected before deletion.

Export/validation/publication failure leaves the run root and keeps the controller ENDED with `EXPORT_FAILED_RETAINED`; retry performs filesystem work only, never replays gameplay. Cancellation during an already-ended export waits for the existing IO result instead of inventing unknown gameplay outcome. Windows deletion errors leave the verified external ZIP and `CLEANUP_PENDING`; partial filesystem deletion is possible, but the complete canonical ZIP survives. Abrupt process/OS termination and live SQLite lock behavior were not exercised. Crash recovery/resume is not introduced.

## Verification actually passed

Canonical root interpreter: `D:\CS\CareerSim\.venv\Scripts\python.exe`.

- **61 targeted tests passed**: HPL-01 (6), HPL-02 (9), dataset routing (6), HPL-03 adapter/controller/export (20), HPL-03A lifecycle (19) and installed-Flet presentation (1).
- New tests cover the Plan's UI contracts, energy disabled/message, no mutation/canonical write on invalid input, duplicate gate, valid terminal action, filename defaults/sanitization/Level/time, no-overwrite collision, stable ZIP verification before whole-root deletion, corrupt archive retention, ACTIVE/technical/hold rejection, export retry, Windows lock retention and ended-export cancellation.
- Installed-Flet presentation subprocess verifies three sibling rails, independent scroll owners, long action wrapping, disabled click gate, font/theme, and modal open/close, with no real engine imported.
- Ruff for HPL client and related HPL tests: PASS. `git diff --check`: PASS.
- Active/energy/handbook/ended Windows desktop fixture windows connected/rendered and exited 0. All reports say `fixture=true`, `real_engine_imported=false`. Screenshots were inspected for wrapping, rails, contrast, public handbook and readable ending filename. Final compact-state active screenshot rechecked after spacing adjustment.

Local evidence: `D:\CS\CareerSim\.local\runtime\human-play-lab\sandbox\hpl03a-ui-{active,energy,handbook,ended}.{json,png}`; corresponding stdout/stderr and synthetic pytest directories are local-only. No existing real run was cleaned by this task; cleanup tests operate on synthetic temporary roots.

## Boundary accounting and holds

Resumed-task before/after accounting: `D:\CS\CareerSim\.local\runtime\human-play-lab\sandbox\hpl03a-boundary-accounting.json`. Protected root tracked file hashes, root .venv/Agent runtime/Jiuwen metadata digests, root HEAD/status, and held-run content-tree digest are equal. Earlier paused-phase baseline is not claimed as a new full-duration snapshot; the branch diff independently contains only HPL client/tests/state/review changes. Root checkout's two pre-existing S09 forensic untracked files remain untouched.

HPL-RUN01 exact retained root: `D:\CS\CareerSim\.local\runtime\human-play-lab\runs\47472aa8b73b4bf6847209f99a8abb39`. Three DB/log/transcript files retain content-tree SHA256 `4a55cf405114c46ba438f0cbc675223b9a5b3cfb1f63e8ed5b5aaa7d952a977c` (sorted relative path/size/content-hash rows). Only bytes were hashed; no private gameplay state was decoded. Existing hold, technical-failure classification and UNKNOWN_AFTER_TECHNICAL_FAILURE remain in force.

Counts: real Human games **0**; real take_action **0**; MCP/Jiuwen/Provider **0**; Agent mutable writes **0**. No root dependency/Candidate/Skills/Runner writes, HPL main integration, hidden DB inspection, HPL-RUN01 resume/replay or user live launch.

Evidence limit: actual live ending IO, real long-session play, and subjective interaction/animation comfort remain unexecuted. Desktop fixture rendering and offline contracts do not establish those live conclusions. Next boundary is Main review/user-controlled live smoke, separately authorized.
