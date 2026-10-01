# Human Play Lab State

> HPL 的独立状态源；不复制正式 Agent 的 Candidate 历史，也不授权任何 Human Run。

## Current task

- Track: `Human Play Lab｜人工游玩策略实验线`, independent of the formal Agent Candidate line.
- Current task: `HPL-05 local Web Human Client`.
- Status: `IN_FLIGHT_EVIDENCE / HPL05_LOCAL_WEB_FIXTURE_PASS`.
- Decision: dedicated signed CPython + msgpack fallback starts a stdlib loopback Web client with local three-column UI and existing controller/public-evidence/lifecycle seams. HTTP and browser fixture E2E pass, including action gating, ending/verified ZIP/cleanup and shutdown; 57 targeted tests pass. No real game or GameEngine construction occurred; future Human factory is only fake-constructor tested. Return `READY_FOR_HPL_05A_REAL_HUMAN_SMOKE_REVIEW`, not live authorization. HPL-04B's original default import remains blocked and HPL-04 remains unaccepted. Never resume HPL-RUN01.
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

## HPL-04B runtime gate boundary

- Base: HPL branch `a42548ab49cd4938453042f7d21f62f3ba46dd4f`; fetched `origin/main` observed at `a6881ff296c2a3f017082e73bf21d7f5161c2b24`, without merge/rebase.
- Isolated gate: `D:\CS\CareerSim\.local\runtime\human-play-lab\local-web-gate`; fresh venv from accepted official CPython 3.12.10. Base python.exe/pythonw.exe/python312.dll and venv launchers are Authenticode Valid / Python Software Foundation.
- Copied 13 installed distributions with RECORD hash verification and source-wheel identity retention; `pip check` passes. Flet/PyInstaller/Jiuwen/MCP/provider packages are absent. Only the BDCI26 Dev files were copied; no test/dev_final/test_final resource was read. No dataset load or mirror probe was necessary for import.
- Default GameEngine import: one attempt, exit 0, stdout `CareerSim GameEngine import OK`, empty stderr; native-load block confirmed by correlated Code Integrity records 1506–1510. Popup visibility is UNKNOWN, not a claimed NO. `_cmsgpack` is NotSigned, SHA256 `0f750d717d6a2ddd61b7d2c376d0cb28fc468347cbc0c1a46aa59126a2fb18c0`. No fallback flag or simulator patch was applied.
- Local gate evidence is on `FORENSIC_HOLD` pending Main/Planner review. Preserve scripts, environment, stdout/stderr, package identities, signatures and event XML; see [HPL-04B review](reviews/HPL-04B_LOCAL_WEB_RUNTIME_GATE.md). No real game, engine construction, action, provider, MCP, Jiuwen, security change or localhost listener occurred. Existing HPL-RUN01 hold is unchanged.

## HPL-04C native avoidance boundary

- Parent: HPL-04B `35bd347f0e356a0570d868edab983520a4adc086`; existing HPL branch/worktree, no main merge/rebase.
- Probe-only environment: `D:\CS\CareerSim\.local\runtime\human-play-lab\msgpack-probe\venv`, official PSF CPython 3.12.10. Copied the prior 13-distribution closure, validating RECORD hashes; omitted `msgpack/_cmsgpack.cp312-win_amd64.pyd` before copy. All Python package source bytes are unchanged. The original HPL development/packaging/HPL-04B environments are unchanged.
- One minimal CareerSim import and one mode/performance probe each exited 0 with empty stderr and no Code Integrity events. `msgpack==1.2.3` reports `hasattr(_cmsgpack)=False`, no native spec, and Packer/Unpacker/unpackb originate from `msgpack.fallback`; no fallback environment flag was set.
- Actual loaded inventory: 45 modules (1 EXE / 32 DLL / 12 PYD), 19 PSF and 26 Microsoft Valid, zero unsigned/invalid loaded binaries. Bootstrap pip's six unsigned distlib launcher templates are present but not loaded and are not CareerSim runtime dependencies.
- Synthetic 800-byte payload, 3 × 1,000 encode/decode samples: medians 101.75 / 175.12 µs per operation; msgpack import 9.49 ms, subsequent CareerSim import 172.41 ms. No native performance baseline was run under the blocking host policy; no gameplay or dataset decoding was performed.
- Review: [HPL-04C native avoidance](reviews/HPL-04C_MSGPACK_NATIVE_AVOIDANCE.md). Local scripts, identities, measurements and signature inventory remain ignored under `msgpack-probe`; preserve pending Main/Planner review. Existing HPL-RUN01 and HPL-04B FORENSIC_HOLDs remain unchanged. No DB/session/game/local web listener was created.

## HPL-05 local Web boundary

- Parent/base: `ee2b8eaff01b7589579cd875e59e1d1d87cf1948`; existing HPL branch/worktree, no main merge/rebase.
- New mutable runtime only: `D:\CS\CareerSim\.local\runtime\human-play-lab\local-web-client`; dedicated official CPython 3.12.10 venv, pinned 13-distribution closure, no Flet/PyInstaller/MCP/Provider. Rebuilt by copying HPL-04C's verified file identities and omitting native msgpack, with complete 194-file BDCI26 Dev dataset mirror including performance_score/config.data. HPL-04C environment and manifest-listed evidence bytes were verified unchanged.
- Entry: `scripts/hpl-web.cmd` defaults to `FIXTURE / NON_GAME`. Exact dedicated Python, startup identity/data/writability checks, ephemeral `127.0.0.1` listener and current URL browser launch. Optional `--human` is a future authorized user entry only; it was not launched here. Server startup never creates a game.
- Web routes reuse HumanGameController, PublicGameAdapter, public projector, RunRecorder and existing finalize/export/cleanup. Fixture storage is solely `local-web-client/fixtures`; fixture ZIPs carry FIXTURE participant/launcher/authorization markers. Future real storage remains `human-play-lab/runs/<run-id>`; no resume/replay route.
- Action requests enforce exact schema, run/revision/choice checks, request IDs, random per-launch token, expected Host and same-origin POST. No automatic mutation retry. Static assets are fixed local files, with CSP/no directory listing/no DB or raw static serving.
- 57 targeted tests PASS (26 HPL-05 + 31 existing controller/lifecycle/adapter). Browser fixture at 1281px: three aligned columns/no horizontal overflow, disabled energy choice, handbook/history, ending and shutdown pass in in-app Chromium; Edge extension connection was unavailable, so Edge/Chrome external-browser behavior is not claimed.
- Latest signed-runtime HTTP fixture smoke PASS, exit 0, empty stderr, fallback asserted, verified ZIP and fixture run cleanup, port released. No Code Integrity event in startup-to-shutdown or final smoke windows. Final loaded inventory: 57 Valid modules, 21 PSF / 36 Microsoft, zero unsigned/invalid loaded modules. Real gameplay/performance and portable packaging/distribution remain unvalidated.
- Review and usage: [HPL-05 local Web client](reviews/HPL-05_LOCAL_WEB_CLIENT.md). No HPL-05A was started; HPL-RUN01 and HPL-04B FORENSIC_HOLDs are not released.

## HPL-04 portable package boundary

- The onedir artifact was built with the accepted official CPython 3.12.10 packaging environment and frozen dependencies: `career-emulator==1.0.1`, `career-emulator-bdci26==1.0.0`, `flet==1.0.1`, PyInstaller `6.16.0`.
- Local artifact: `D:\CS\CareerSim\.local\runtime\human-play-lab\package-build\release\CareerSim-Human-v1-Windows-x64.zip`; 65,507,822 bytes; SHA256 `daa82f050bafbdc289960405060b97710bcb8797374b19ea1c3cb61e5101347f`. Build source commit: `1820c3acf539b92ee51769d445da01eba884a24f`. The ignored package remains local and was not distributed.
- Static archive verification passed: complete 194-file Dev dataset at official and package-default roots, including `performance_score/config.data`; no repo/private metadata, Agent Candidate/Skills/Runner, `.env`, Provider module, HPL raw evidence, or previous Human runs. `UserData\Runs`, `Exports`, and `Diagnostics` are the only packaged writable roots. Success export ordering is finalize, verified ZIP, export, reverify, then run cleanup; export/technical failures retain run and diagnostics.
- Native inventory: 65 EXE/DLL/PYD files, 33 Authenticode `Valid`, 32 `NotSigned`, zero invalid signatures and no system-managed OS files bundled; 23 Python Software Foundation signed, 6 Microsoft signed, 4 other valid signers. Bundled `_internal\python312.dll` is Valid / Python Software Foundation. Generated `CareerSim Human.exe` and Flet `flet.exe` are unsigned; `FINAL_EXE_CODE_SIGNING_REQUIRED=RECOMMENDED` for broad external distribution.
- An earlier fixture attempt logged Enterprise signing-level Code Integrity blocks for the unsigned generated launcher and `_internal\msgpack\_cmsgpack.cp312-win_amd64.pyd`. The final rebuild remains unsigned; its packaged fixture smoke was not rerun after observing the same policy blocker. Actual packaged writable-UserData, no-external-runtime, and read-only fail-closed launch smokes remain unverified. No policy, Defender, Smart App Control, or reputation setting was changed.
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
