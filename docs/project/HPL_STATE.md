# Human Play Lab State

> HPL 的独立状态源；不复制正式 Agent 的 Candidate 历史，也不授权任何 Human Run。

## Current task

- Track: `Human Play Lab｜人工游玩策略实验线`, independent of the formal Agent Candidate line.
- Current task: `HPL-RUN01 dataset routing repair`.
- Status: `DATASET_ROUTING_REPAIRED_OFFLINE_READY_FOR_FRESH_RUN_GATE`.
- Decision: return to Main for a separately authorized fresh Human Run; never resume HPL-RUN01.
- Human Run authorization: `NOT_AUTHORIZED`; `HUMAN_PLAY_NEXT_GAME=NOT_AUTHORIZED`.

## Lineage

- Accepted parent: `hpl-01-human-play-feasibility @ a874f5471bbff4c46216f36174acb4d785c05cc4`.
- Persistent HPL branch: `research/human-play-lab`.
- Persistent HPL worktree: `D:\CS\CareerSim\.local\worktrees\human-play-lab`.
- Repair base: HPL-02 `36fa0922622a9fbd9e7d43a8f0ad85008e3b1977`. Formal `origin/main` observed for this repair: `5bc07edc49bb352a686d13940fb36f78d01ca827`. HPL remains unmerged into `main`.

## Human sandbox

- Runtime root: `D:\CS\CareerSim\.local\runtime\human-play-lab`.
- Dedicated interpreter: `D:\CS\CareerSim\.local\runtime\human-play-lab\venv\Scripts\python.exe` (`Python 3.12.13`).
- Packages: `career-emulator==1.0.1`; `career-emulator-bdci26==1.0.0`.
- Human dataset: the HPL venv's installed `career_emulator_bdci26\dev\dataset`, split `dev`; the complete 194-file tree is copied into the same venv's `career_emulator\data\dataset`. Preflight validates source bytes against the pinned distribution RECORD, full mirror file/directory equivalence, and required configuration files including `performance_score/config.data`. Dataset bytes are hashed/copied without decoding rules.
- Local environment manifest: `.local\runtime\human-play-lab\sandbox\environment_manifest.json`; it records the full 13-distribution closure. JiuwenSwarm, FastMCP/MCP, and LLM provider packages are absent. `gitcode-api` is present as the upstream optional sharing dependency and is disabled by the wrapper callback.
- Formal Agent root `.venv`, Candidate, Skills, Runner, config, provider configuration, and runtime are not used by the Human launcher.

## Runtime and evidence contract

- Future run root: `.local\runtime\human-play-lab\runs\<run-id>`.
- DB/logs: `runtime\career_emulator.sqlite3` and `runtime\logs\`, set before importing the emulator.
- Raw terminal transcript: `transcript\`; local-only and excluded from canonical trajectory values.
- Canonical artifacts: `evidence\manifest.json`, `trajectory.jsonl`, `summary.json`, and `integrity.json`; trajectory frames pass through `scripts/hpl_public_evidence.py`.
- Default launcher: `scripts\hpl.ps1`; default is a no-write preflight. A future live invocation requires both `-Live` and a non-empty `-AuthorizationId`.
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
- Latest report: [HPL-RUN01 dataset routing repair](reviews/HPL-RUN01_DATASET_ROUTING_REPAIR.md). The original [HPL-02 review](reviews/HPL-02_PERSISTENT_HUMAN_SANDBOX.md) remains historical offline evidence; its seven-directory assumption did not cover all default consumers.
