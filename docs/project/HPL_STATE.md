# Human Play Lab State

> HPL 的独立状态源；不复制正式 Agent 的 Candidate 历史，也不授权任何 Human Run。

## Current task

- Track: `Human Play Lab｜人工游玩策略实验线`, independent of the formal Agent Candidate line.
- Current task: `HPL-02｜持久化人工沙箱与最小交互闭环`.
- Status: `PERSISTENT_SANDBOX_READY_FOR_FIRST_HUMAN_GAME_GATE`.
- Decision: `HPL02_PERSISTENT_SANDBOX_READY_FOR_FIRST_HUMAN_GAME_GATE`.
- Human Run authorization: `NOT_AUTHORIZED`; `HUMAN_PLAY_NEXT_GAME=NOT_AUTHORIZED`.

## Lineage

- Accepted parent: `hpl-01-human-play-feasibility @ a874f5471bbff4c46216f36174acb4d785c05cc4`.
- Persistent HPL branch: `research/human-play-lab`.
- Persistent HPL worktree: `D:\CS\CareerSim\.local\worktrees\human-play-lab`.
- Formal `origin/main` inspected for this task: `d94b178e3e7867b80673c4dfecd2e70dd66272b5`; no material Architecture, Source Lock, environment, or governance drift was found. HPL remains unmerged into `main`.

## Human sandbox

- Runtime root: `D:\CS\CareerSim\.local\runtime\human-play-lab`.
- Dedicated interpreter: `D:\CS\CareerSim\.local\runtime\human-play-lab\venv\Scripts\python.exe` (`Python 3.12.13`).
- Packages: `career-emulator==1.0.1`; `career-emulator-bdci26==1.0.0`.
- Human dataset: the HPL venv's installed `career_emulator_bdci26\dev\dataset`, split `dev`; all seven GameEngine directories are present. No dataset files were read or updated for this task.
- Local environment manifest: `.local\runtime\human-play-lab\sandbox\environment_manifest.json`; it records the full 13-distribution closure. JiuwenSwarm, FastMCP/MCP, and LLM provider packages are absent. `gitcode-api` is present as the upstream optional sharing dependency and is disabled by the wrapper callback.
- Formal Agent root `.venv`, Candidate, Skills, Runner, config, provider configuration, and runtime are not used by the Human launcher.

## Runtime and evidence contract

- Future run root: `.local\runtime\human-play-lab\runs\<run-id>`.
- DB/logs: `runtime\career_emulator.sqlite3` and `runtime\logs\`, set before importing the emulator.
- Raw terminal transcript: `transcript\`; local-only and excluded from canonical trajectory values.
- Canonical artifacts: `evidence\manifest.json`, `trajectory.jsonl`, `summary.json`, and `integrity.json`; trajectory frames pass through `scripts/hpl_public_evidence.py`.
- Default launcher: `scripts\hpl.ps1`; default is a no-write preflight. A future live invocation requires both `-Live` and a non-empty `-AuthorizationId`.
- The official CLI `GameEngine` factory is wired to the seven HPL Dev dataset paths. Raw `logs` input is intercepted, and `cli.offer_share` is replaced with a no-op before the CLI play function.

## Isolation and evidence limits

- `HPL_RUNTIME_ISOLATION=STATICALLY_PROVEN_FOR_DEDICATED_SANDBOX` for checkout, Python environment, package/data copy, and target storage paths. No Human run was created in HPL-02.
- The first live CLI write set, actual runtime provider behavior, real transcript parser coverage, and Human strategy effectiveness remain `UNKNOWN` until separately authorized evidence exists.
- `HPL_AGENT_PARALLEL_RUN_ALLOWED` is not granted. Return to Main for a dedicated first-Human-Game gate; the first run should not overlap an Agent game.
- Latest report: [HPL-02 persistent Human sandbox review](reviews/HPL-02_PERSISTENT_HUMAN_SANDBOX.md).
