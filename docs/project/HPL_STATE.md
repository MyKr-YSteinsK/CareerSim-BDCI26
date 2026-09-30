# Human Play Lab State

> HPL 的独立状态源；不复制正式 Agent 的 Candidate 历史，也不授权任何 Human Run。

## Current task

- Track: `Human Play Lab｜人工游玩策略实验线`, independent of the formal Agent Candidate line.
- Current task: `HPL-03 Flet desktop Human client`.
- Status: `IN_FLIGHT_EVIDENCE / HPL03_DESKTOP_CLIENT_READY_FOR_USER_LIVE_SMOKE`.
- Decision: return desktop implementation and offline evidence to Main for acceptance; the user starts any subsequent GUI run manually. Never resume HPL-RUN01.
- Human Run authorization: `NOT_AUTHORIZED`; `HUMAN_PLAY_NEXT_GAME=NOT_AUTHORIZED`.

## Lineage

- Accepted parent: `hpl-01-human-play-feasibility @ a874f5471bbff4c46216f36174acb4d785c05cc4`.
- Persistent HPL branch: `research/human-play-lab`.
- Persistent HPL worktree: `D:\CS\CareerSim\.local\worktrees\human-play-lab`.
- HPL-03 accepted parent: `436492783ac06f4fcc75b8608eb47014be556a90`; latest observed `origin/main`: `43258d41a02ac65c9f1e5d0367ca7612a36c7da7`. No main merge/rebase.
- Repair base: HPL-02 `36fa0922622a9fbd9e7d43a8f0ad85008e3b1977`. Formal `origin/main` observed for this repair: `5bc07edc49bb352a686d13940fb36f78d01ca827`. HPL remains unmerged into `main`.

## Human sandbox

- Runtime root: `D:\CS\CareerSim\.local\runtime\human-play-lab`.
- Dedicated interpreter: `D:\CS\CareerSim\.local\runtime\human-play-lab\venv\Scripts\python.exe` (`Python 3.12.13`).
- Packages: `career-emulator==1.0.1`; `career-emulator-bdci26==1.0.0`.
- Human dataset: the HPL venv's installed `career_emulator_bdci26\dev\dataset`, split `dev`; the complete 194-file tree is copied into the same venv's `career_emulator\data\dataset`. Preflight validates source bytes against the pinned distribution RECORD, full mirror file/directory equivalence, and required configuration files including `performance_score/config.data`. Dataset bytes are hashed/copied without decoding rules.
- Local environment manifest: `.local\runtime\human-play-lab\sandbox\environment_manifest.json`; it records the full 22-distribution closure after HPL-only `flet[desktop]==1.0.1`, and the 65-file Windows desktop installation identity. Explicit refresh retains each prior manifest by SHA256. JiuwenSwarm, FastMCP/MCP, and LLM provider packages are absent. `gitcode-api` is an upstream optional sharing dependency: disabled by the CLI wrapper, never invoked by the direct GUI path.
- Formal Agent root `.venv`, Candidate, Skills, Runner, config, provider configuration, and runtime are not used by the Human launcher.

## Runtime and evidence contract

- Future run root: `.local\runtime\human-play-lab\runs\<run-id>`.
- DB/logs: `runtime\career_emulator.sqlite3` and `runtime\logs\`, set before importing the emulator.
- Raw terminal transcript: `transcript\`; local-only and excluded from canonical trajectory values.
- Canonical artifacts: `evidence\manifest.json`, `trajectory.jsonl`, `summary.json`, and `integrity.json`; trajectory frames pass through `scripts/hpl_public_evidence.py`.
- Desktop launcher: `scripts\hpl-ui.ps1`. Startup validates HPL identity and opens the start screen without importing GameEngine or creating a game. Only the user's Start click constructs a fresh run. After first-import defaults freeze, each fresh engine's store log directory is explicitly rebound before IO to the new run root.
- CLI fallback: `scripts\hpl.ps1`; default is a no-write preflight. A future CLI live invocation requires both `-Live` and a non-empty `-AuthorizationId`.
- GUI public transitions and submission intents are flushed/fsynced to `staging/public_journal.jsonl`; canonical evidence uses the accepted projector/writer. Ending/failure export validates hashes, public projection, run/session identity and known secret patterns, then includes only four canonical files plus `README.txt`. DB/logs/technical tracebacks are excluded. Unknown mutation results stop the run without retry/observe/DB inquiry.
- The official CLI `GameEngine` factory is wired to the seven HPL Dev dataset paths. All package-default consumers, including the independent performance-score loader, resolve the complete local Dev mirror. Raw `logs` input is intercepted, and `cli.offer_share` is replaced with a no-op before the CLI play function.

## HPL-RUN01 failure and hold

- `HPL-RUN01=TECHNICAL_FAILURE_DATASET_ROUTING`; Month 5 and failure are human-reported. Session: `91c67514b52442749b1b37bc9785ce21`.
- Last action outcome: `UNKNOWN_AFTER_TECHNICAL_FAILURE`; no DB/private-state inquiry, resume, or action replay is authorized.
- `FORENSIC_HOLD`: retain the complete local run root `D:\CS\CareerSim\.local\runtime\human-play-lab\runs\47472aa8b73b4bf6847209f99a8abb39`, including DB, log and transcript. No strategy conclusion may use this failed run.
- Responsibility: HPL-RUN01 / Main. Release requires Main's explicit acceptance of the failure evidence and cleanup authorization; this repair or a future successful run does not release the hold.
- Evidence paths/bytes/hashes and source investigation: [HPL-RUN01 dataset routing repair](reviews/HPL-RUN01_DATASET_ROUTING_REPAIR.md).

## Isolation and evidence limits

- `HPL_RUNTIME_ISOLATION=STATICALLY_PROVEN_FOR_DEDICATED_SANDBOX` for checkout, Python environment, package/data copy, and target storage paths. No Human run was created in HPL-02.
- The first live CLI write set, actual runtime provider behavior, real transcript parser coverage, and Human strategy effectiveness remain `UNKNOWN` until separately authorized evidence exists.
- `HPL_AGENT_PARALLEL_RUN_ALLOWED` is not granted. Return to Main for a dedicated first-Human-Game gate; the first run should not overlap an Agent game.
- Latest report: [HPL-03 desktop client](reviews/HPL-03_FLET_DESKTOP_CLIENT.md): 41 offline tests and start/game/end fixture desktop smoke passed; actual GUI gameplay remains unexecuted. Root Agent environment/runtime and failed-run hold are preserved. Concurrent main commit `43258d4` independently changed Agent Candidate configs/rolling-planning; HPL does not carry those changes.
- [HPL-RUN01 dataset routing repair](reviews/HPL-RUN01_DATASET_ROUTING_REPAIR.md) and [HPL-02 review](reviews/HPL-02_PERSISTENT_HUMAN_SANDBOX.md) remain historical evidence; HPL-02's seven-directory assumption did not cover all default consumers.
