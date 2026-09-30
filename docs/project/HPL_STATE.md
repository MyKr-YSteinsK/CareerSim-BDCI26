# Human Play Lab State

> HPL 的独立状态源；不复制正式 Agent 的 Candidate 历史，也不授权任何 Human Run。

## Current task

- Track: `Human Play Lab｜人工游玩策略实验线`, independent of the formal Agent Candidate line.
- Current task: `HPL-04 Windows portable build and independent launch`.
- Status: `IN_FLIGHT_EVIDENCE / HPL04_STATIC_PACKAGE_PASS_PACKAGED_SMOKE_BLOCKED_BY_APPLICATION_CONTROL`.
- Decision: static portable build and archive checks pass, but local Windows Application Control blocks the unsigned generated launcher before application startup. Packaged fixture smoke, writable UserData launch and read-only application-directory fail-closed launch remain unverified. Return this boundary for Main/Planner review; do not claim HPL-04 acceptance or clean-machine validation. Never resume HPL-RUN01.
- Human Run authorization: `NOT_AUTHORIZED`; `HUMAN_PLAY_NEXT_GAME=NOT_AUTHORIZED`.

## Lineage

- Accepted parent: `hpl-01-human-play-feasibility @ a874f5471bbff4c46216f36174acb4d785c05cc4`.
- Persistent HPL branch: `research/human-play-lab`.
- Persistent HPL worktree: `D:\CS\CareerSim\.local\worktrees\human-play-lab`.
- HPL-03 accepted parent: `436492783ac06f4fcc75b8608eb47014be556a90`; latest observed `origin/main`: `43258d41a02ac65c9f1e5d0367ca7612a36c7da7`. No main merge/rebase.
- Repair base: HPL-02 `36fa0922622a9fbd9e7d43a8f0ad85008e3b1977`. Formal `origin/main` observed for this repair: `5bc07edc49bb352a686d13940fb36f78d01ca827`. HPL remains unmerged into `main`.

- HPL-03A accepted parent: `eafe2b669f531562d772ca6a425ea85d14d0ecdc`; observed `origin/main`: `aa3844c85c982e42a859a18cfc60820df32600a0`. No main merge/rebase.
- HPL-04A Planner decision: `HPL04A_ACCEPTED_SIGNED_CPYTHON_RUNTIME_GATE_PASS`. Release packaging uses `.local\runtime\human-play-lab\packaging-python\venv\Scripts\python.exe` based on official CPython 3.12.10; the bundled `python312.dll` is Authenticode Valid and signed by Python Software Foundation.

## Human sandbox

- Runtime root: `D:\CS\CareerSim\.local\runtime\human-play-lab`.
- Dedicated interpreter: `D:\CS\CareerSim\.local\runtime\human-play-lab\venv\Scripts\python.exe` (`Python 3.12.13`).
- Packages: `career-emulator==1.0.1`; `career-emulator-bdci26==1.0.0`.
- Human dataset: the HPL venv's installed `career_emulator_bdci26\dev\dataset`, split `dev`; the complete 194-file tree is copied into the same venv's `career_emulator\data\dataset`. Preflight validates source bytes against the pinned distribution RECORD, full mirror file/directory equivalence, and required configuration files including `performance_score/config.data`. Dataset bytes are hashed/copied without decoding rules.
- Local environment manifest: `.local\runtime\human-play-lab\sandbox\environment_manifest.json`; it records the full 22-distribution closure after HPL-only `flet[desktop]==1.0.1`, and the 65-file Windows desktop installation identity. Explicit refresh retains each prior manifest by SHA256. JiuwenSwarm, FastMCP/MCP, and LLM provider packages are absent. `gitcode-api` is an upstream optional sharing dependency: disabled by the CLI wrapper, never invoked by the direct GUI path.
- Formal Agent root `.venv`, Candidate, Skills, Runner, config, provider configuration, and runtime are not used by the Human launcher.

## HPL-04 portable package boundary

- The onedir artifact was built with the accepted official CPython 3.12.10 packaging environment and frozen dependencies: `career-emulator==1.0.1`, `career-emulator-bdci26==1.0.0`, `flet==1.0.1`, PyInstaller `6.16.0`.
- Local artifact: `D:\CS\CareerSim\.local\runtime\human-play-lab\package-build\release\CareerSim-Human-v1-Windows-x64.zip`; 65,056,863 bytes; SHA256 `e1f6889669f4377668b9bf28eee152c568dfe2c9b32df468dfacf25c0e210413`. Build source commit: `084a72be376f606a19735388304c450bbe81bbf9`. The ignored package remains local and was not distributed.
- Static archive verification passed: complete 194-file Dev dataset at official and package-default roots, including `performance_score/config.data`; no repo/private metadata, Agent Candidate/Skills/Runner, `.env`, Provider module, HPL raw evidence, or previous Human runs. `UserData\Runs`, `Exports`, and `Diagnostics` are the only packaged writable roots. Success export ordering is finalize, verified ZIP, export, reverify, then run cleanup; export/technical failures retain run and diagnostics.
- Native inventory: 65 EXE/DLL/PYD files, 33 Authenticode `Valid`, 32 `NotSigned`; 23 Python Software Foundation signed, 6 Microsoft signed, 4 other valid signers. Bundled `_internal\python312.dll` is Valid / Python Software Foundation. Generated `CareerSim Human.exe` and Flet `flet.exe` are unsigned; `FINAL_EXE_CODE_SIGNING_REQUIRED=RECOMMENDED` for broad external distribution.
- Packaged fixture startup did not pass on this Windows installation. Application Control's Enterprise signing-level policy blocked the unsigned generated launcher before app code ran; an earlier fixture attempt also logged Code Integrity blocks for `_internal\msgpack\_cmsgpack.cp312-win_amd64.pyd`. The actual packaged writable-UserData, no-external-runtime, and read-only fail-closed launch smokes remain unverified. No policy, Defender, Smart App Control, or reputation setting was changed.
- Review: [HPL-04 Windows portable packaging](reviews/HPL-04_WINDOWS_PORTABLE_PACKAGING.md). This is not HPL-04 acceptance or clean-machine validation.

## Runtime and evidence contract

- Future run root: `.local\runtime\human-play-lab\runs\<run-id>`.
- DB/logs: `runtime\career_emulator.sqlite3` and `runtime\logs\`, set before importing the emulator.
- Raw terminal transcript: `transcript\`; local-only and excluded from canonical trajectory values.
- Canonical artifacts: `evidence\manifest.json`, `trajectory.jsonl`, `summary.json`, and `integrity.json`; trajectory frames pass through `scripts/hpl_public_evidence.py`.
- Desktop launcher: `scripts\hpl-ui.ps1`. Startup validates HPL identity and opens the start screen without importing GameEngine or creating a game. Only the user's Start click constructs a fresh run. After first-import defaults freeze, each fresh engine's store log directory is explicitly rebound before IO to the new run root.
- Desktop UI uses Microsoft YaHei UI, fixed status/event/choice columns with independent scrolling, a public handbook modal, and collapsible recent choices. Header owns Year/Quarter/Month/Level. Energy-insufficient, illegal, stale, malformed, duplicate and wrong-run choices are rejected before submission as `INVALID_ACTION / NO_MUTATION`; they do not end the run or add canonical transitions.
- Normal desktop endings automatically finalize canonical evidence, build/verify the exact five-file public ZIP, publish to the selected mode's export directory, reverify, then remove only that ended run root. Development mode uses `D:\CS\CareerSim\.local\runtime\human-play-lab\exports`; packaged mode uses `<AppDirectory>\UserData\Exports`. Names use participant, public quantitative score, final Level and local end timestamp; collisions append a short suffix. Active/technical/unknown/held runs cannot use success cleanup. Export failures retain the run and permit IO-only retry; Windows cleanup locks preserve a verified ZIP with `CLEANUP_PENDING`.
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
- Latest report: [HPL-04 Windows portable packaging](reviews/HPL-04_WINDOWS_PORTABLE_PACKAGING.md): static archive, dataset, source-path and native-signature checks passed using the accepted signed CPython packaging environment. Local package launch was blocked by the Enterprise signing-level Application Control policy; no security setting was changed. No game, action, provider, MCP, JiuwenSwarm, or Human Run was started. HPL-RUN01 and formal Agent protected paths retain their observed identity.
- Historical report: [HPL-03A UI and finalization](reviews/HPL-03A_UI_AND_RUN_FINALIZATION.md): 61 offline tests, Ruff, diff check, and active/energy/handbook/ended development-client fixture smoke passed. These were not packaged launcher tests. No real game or mutation was created.
- Historical report: [HPL-03 desktop client](reviews/HPL-03_FLET_DESKTOP_CLIENT.md): 41 offline tests and start/game/end fixture desktop smoke passed; actual GUI gameplay remains unexecuted. Root Agent environment/runtime and failed-run hold are preserved. Concurrent main commit `43258d4` independently changed Agent Candidate configs/rolling-planning; HPL does not carry those changes.
- [HPL-RUN01 dataset routing repair](reviews/HPL-RUN01_DATASET_ROUTING_REPAIR.md) and [HPL-02 review](reviews/HPL-02_PERSISTENT_HUMAN_SANDBOX.md) remain historical evidence; HPL-02's seven-directory assumption did not cover all default consumers.
