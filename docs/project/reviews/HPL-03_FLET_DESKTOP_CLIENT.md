# HPL-03 — Flet Windows desktop Human client

## Identity and review decision

- Evidence: `IN_FLIGHT_EVIDENCE`; implementation/offline delivery complete, pending Main acceptance.
- Decision: `HPL03_DESKTOP_CLIENT_READY_FOR_USER_LIVE_SMOKE`; not HPL Stage completion or Human Run authorization.
- Accepted parent: `436492783ac06f4fcc75b8608eb47014be556a90`.
- Branch/worktree: `research/human-play-lab`, `D:\CS\CareerSim\.local\worktrees\human-play-lab`.
- Fetch observed main `74e856c5be7a9a134f93e9876ffbfd14398199ab`; final observed main `43258d41a02ac65c9f1e5d0367ca7612a36c7da7`. HPL was not merged/rebased; its parent is unchanged.

## UI and exact API decision

Run from the persistent worktree:

```powershell
.\scripts\hpl-ui.ps1
```

Flet `1.0.1`, declarative `@ft.component` / hooks; local desktop IPC only. Start page has an optional nickname and Local / No LLM / HPL label. The resizable 1100×700 window has seven public stats, public calendar/level, scrollable event/choice and handbook panels, warning banner and eight recent selections. End/failure pages allow validated ZIP export and a fresh Start. No raw logs UI, accounts, telemetry, cloud sharing or providers.

Installed source inspected under the HPL venv `Lib/site-packages/career_emulator`:

| Source | API / decision |
|---|---|
| `game.py:133` | async `new_game()` → `NewGameResponse(session_id,error)` |
| `game.py:157` | async `observe(session_id)` → nested `current_state`, `current_event`, `choices`, `warning`, `ending_score` |
| `game.py:199` | async `take_action(session_id,choice,notes="")` → boolean success/error receipt |
| `game.py:289` | async `enrollment_handbook()` → participant text |
| `game.py:320` | pending participant warning is returned/cleared by observe; review/promotion feedback uses this same warning channel |
| `game.py:678,718`, `server/models.py:542` | ended/current state include hidden bookkeeping; explicitly project nested time/status rather than expose the raw state |
| `server/storage.py`, GameEngine constructor | explicit run-local SQLite path, existing SessionStore `log_dir` rebound before IO for each subsequent game |

Only the first four public methods are called. Observe can persist/consume warnings, so render/handbook/export do not call it again. After a successful action receipt, obtain one fresh observe. The direct path never calls CLI play, share/update, MCP, store readers or private accessors, and does not replace any simulator rule.

Adapter returns `PublicGameView(run_id,revision,phase,projection)`. Public state is session/month/quarter/year/level/seven stats; event title/description; choice/action/energy_cost; public handbook/warning; approved final outcome/survival/grade/quantitative/competition partial score. Final outcome follows official CLI completed/elimination mapping. Review/promotion stays in official participant warning text; no hidden-event reconstruction. Text is filtered through the same projector, including handbook lines. Event/node IDs, status_updates, hidden counters, private state and score dimensions/weights/contributions are dropped before UI and canonical projection. Human interpretation remains separate from observed facts; the public allowlist is unchanged.

## Lifecycle and evidence

Controller validates legal choices, run ID and current revision, with a synchronous busy gate and consumed revision set. Concurrent/queued/stale callbacks cannot submit twice. UI requests the disabled/loading render before submission. Any engine exception or ambiguous receipt fails closed: `TECHNICAL_FAILURE`, action outcome `UNKNOWN_AFTER_TECHNICAL_FAILURE`, no retry/observe/hidden-state inquiry. A user can start a fresh run after failure; no resume path exists.

Every public observation and submission intent is appended/flushed/fsynced to run-local `staging/public_journal.jsonl`; the intended choice is retained even on technical failure. End/failure uses the existing canonical writer. A GUI/process crash can leave an incomplete journal rather than a finished canonical bundle; crash recovery/resume is not implemented. Run-local technical traceback stays in `scratch/technical_error.log` and is excluded from export.

Export contains exactly `manifest.json`, `trajectory.jsonl`, `summary.json`, `integrity.json`, `README.txt`. Validate canonical SHA256, strict public re-projection, session/run identity, frame count, permitted metadata, known secret patterns, portable paths and exact archive entries. ZIP has no SQLite/raw logs/transcripts/dataset/credentials/machine config. Pattern scan is not a universal secret detector; public nickname/text remains the participant's supplied research data. Empty/pre-observation failures retain local evidence but cannot export a session-consistent research bundle.

## HPL environment and isolation

- Dedicated interpreter: `D:\CS\CareerSim\.local\runtime\human-play-lab\venv\Scripts\python.exe`, Python 3.12.13.
- Install: explicit `uv pip install --python <HPL python> 'flet[desktop]==1.0.1'`; added nine distributions, total 22. Emulator/data unchanged at `1.0.1 / 1.0.0`.
- Flet Python wheel lacks Windows binaries. Downloaded official fixed release `https://github.com/flet-dev/flet/releases/download/v1.0.1/flet-windows.zip`, extracted only to HPL `venv/flet-desktop`. Download continued from a retained partial file after a bounded timeout; no simulator dataset download occurred.
- Archive: 40,284,502 bytes, SHA256 `e4193cf41ccdbc58e01eeace23ad4108e4334dba47ee5b6f3943dd7c622553c1`. Full local desktop installation: 65 files, tree SHA256 `3d1ecdc08453edae893b995e3160476fc465941093219963e92a4b8456d98762`.
- Local environment manifest records the resolved closure and desktop identity. Explicit refresh preserves old manifests by hash. Normal preflight rejects package/source/runtime drift, and the GUI requires a local desktop binary; startup does not fetch it. Flet module roots must lie within the HPL venv.
- Complete 194-file Dev/default mirror validation remains unchanged, including performance_score/config.data and distribution RECORD identity. No rules were decoded.
- Before/after root `.venv`, Agent runtime and Jiuwen config metadata digests are identical. Root dependency files/frozen Runner and HPL protected tracked files are unchanged.
- Local before/after digests and attribution are retained in `D:\CS\CareerSim\.local\runtime\human-play-lab\sandbox\hpl03-boundary-accounting.json`; the only directory in `runs/` after this task is the existing held HPL-RUN01.
- Concurrent main commit `43258d4` changed root `configs/current_candidate.json`, `configs/runtime_manifest.json`, `skills/rolling-planning/SKILL.md` from the pre-task baseline. Their observed differences match that independent main commit; root checkout is clean. No HPL operation wrote those paths and the HPL diff contains none of them. This is not claimed as full root tracked hash equality.
- HPL-RUN01 remains `TECHNICAL_FAILURE_DATASET_ROUTING`, last action `UNKNOWN_AFTER_TECHNICAL_FAILURE`, `FORENSIC_HOLD`. The retained run root `D:\CS\CareerSim\.local\runtime\human-play-lab\runs\47472aa8b73b4bf6847209f99a8abb39` DB/log/transcript hashes are unchanged; no gameplay values were read.

## Verification actually passed

- Root canonical Python targeted pytest: **41 passed** (21 existing HPL tests + 20 desktop tests). Fake engines cover nested-public firewall, real installed dataclass/API shape without GameEngine construction, receipt/session failure, end result projection, double callbacks, stale run/revision, journal IO failure, unknown mutation stop, successive run-local DB/log construction, journal preservation and ZIP corruption/secret/path/session rejection.
- Ruff check for all changed Python plus related HPL tests: PASS. `git diff --check`: PASS.
- Launcher `scripts/hpl-ui.ps1 -Fixture` and no-game start/active/ended fixture desktop windows: successful page connection/render and exit 0; every smoke reports `real_engine_imported=false`. No real engine construction/gameplay occurred.
- Local smoke reports: `D:\CS\CareerSim\.local\runtime\human-play-lab\sandbox\hpl03-ui-{start,active,ended}.json`.
- Local screenshots (inspected): same directory `hpl03-fixture-{start,active,ended}.png`. Long fixture event wraps and center/right panels scroll; screenshots evidence desktop fixture rendering, not real-game playability.
- CLI default no-write preflight still passes via the existing regression test.

Boundary counts: Codex-created Human game **0**; real take_action **0**; MCP **0**; Jiuwen/Agent service **0**; Provider **0**; Agent mutable writes **0**. Fixture calls are synthetic and do not count as simulator gameplay. No DB/private gameplay-state query, HPL-RUN01 resume/replay, main merge or user live run.

Remaining live unknowns: actual user GUI gameplay, live engine IO/write behavior, real long-session warnings/outcomes and GUI interaction comfort have not been exercised. Main acceptance/user manual live smoke is the next boundary; this report does not authorize it or declare the HPL Stage complete.
