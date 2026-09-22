# S01-03 — 官方 Runner 与最小 Baseline 闭环

## Result

- Status: `COMPLETE`
- Branch: `codex/s01-03-runner-baseline`
- Commit: recorded by the delivery commit for this evidence bundle
- Experiment / Run ID: `S01-03-baseline-20260922T123030Z`

## Frozen Identity

- Official Runner: `openJiuwen-ai/CareerSim-BDCI26@f61c738c72e51b77298cc1c14c7c6ebf4b6c527d`
- Runner provenance: 27 files; aggregate SHA256 `1ff2d60c034015e4634cd456bffcdacad0bd33b202b0e5762295f3caa67c9e8a`
- Python: CPython `3.12.13` x64; uv `0.11.16`
- Packages: `jiuwenswarm==0.2.4b3`, `career-emulator==1.0.1`, `career-emulator-bdci26==1.0.0`
- Dependency lock: unchanged; `uv.lock` SHA256 `18466056430F7C49C3A23705D312625B40B1A5119C41F0EC62571CDA208E4C0C`
- Dataset: `career-emulator-bdci26==1.0.0`, `source=distribution`, `split=dev`, 194 files, aggregate SHA256 `ecadbb6df2335e55b1e898de94102c9a2b2cdb23e8e7790912b8c2fb228d2fe4`
- Dataset paths: source `D:\CS\CareerSim\.venv\Lib\site-packages\career_emulator_bdci26\dev\dataset`; materialized `D:\CS\CareerSim\.venv\Lib\site-packages\career_emulator\data\dataset`
- Dataset materialization: official symlink command reached `WinError 1314` on Windows; exact byte-for-byte copy from the locked distribution was used and verified by the aggregate/file manifest. No GitHub dataset was used.

## Model Configuration

- Provider / endpoint: DeepSeek official API, `https://api.deepseek.com`
- Request model: `deepseek-flash`
- Response / usage model identifier: `deepseek-flash`
- Mapping status: `PARTIALLY_VERIFIED`; request/usage identifiers match, but the underlying serving version was not independently proven by the Runner.
- API key exposed: `NO`; source was Windows User-level `DEEPSEEK_API_KEY`, and `.env`/instance env were not committed.

## Baseline Harness

- Path: `baselines/s01-minimal`
- Mode: `agent`
- Skill: `baseline-placeholder`
- Strategy content: `NONE / NO-OP`

## Baseline Run

- Drive session ID: `career-sim-runner-a4ff0a00f938`
- Game session ID: `5b37e7fb40844809abf00f9ceeb5c25b`
- Start / end: `2026-09-22T12:30:26.6879827Z` / `2026-09-22T12:35:38.7823804Z`
- Command: `uv run --no-sync python -m career_sim_runner play --submission baselines/s01-minimal`
- Fresh state: no `--continue`; Runner installed the bundle and started a fresh game session.
- Terminal ending: early elimination, `completed=false`, `survival_months=19`, grade `E`
- Score: quantitative `26.95`; competition partial `18.86`; full objective fields are in `score_report.json`.
- Play exit code: `0`
- Technical result: valid terminal game result, not a runtime failure.
- Token usage: input `10,761,112`; output `22,823`; total `10,783,935`; by-model `deepseek-flash` with the same counts; reported cost `0`; cache usage not provided.
- Second game run: `NO`

## Evidence

- Canonical score report: `D:\CS\CareerSim-s01-03-runner-baseline\experiments\S01-03-baseline\score_report.json`
- Score report SHA256: `f84598d1df614131f90362a9f3ea83ebe381f5c5b755922187f4868d59b07686`
- Original score report: `D:\CS\CareerSim-s01-03-runner-baseline\.career_sim_runner\career_emu\outputs\local-s01-baseline\20260922T123030Z\score_report.json`
- Transcript: `D:\CS\CareerSim-s01-03-runner-baseline\.career_sim_runner\career_emu\outputs\local-s01-baseline\20260922T123030Z\transcript-20260922T123030Z.log`
- Transcript SHA256: `ee77106c551a2dccc8ae909fde6bbc1596992b3f40f3c568c69139c3abe5c0af`
- Events: `D:\CS\CareerSim-s01-03-runner-baseline\.career_sim_runner\career_emu\outputs\local-s01-baseline\20260922T123030Z\events-20260922T123030Z.jsonl`
- Events SHA256: `49242bf7e68edb05c3b29f59602c0b0b11da377a9f4deda5a78ad7cd6bf45510`
- Runtime/control diagnostics: `D:\CS\CareerSim-runtime-s01-03\`

## Restart Verification

- Stop command: `uv run --no-sync jiuwenswarm-start --stop career_emu` — PASS
- Restart command: `uv run --no-sync jiuwenswarm-start --name career_emu all` — PASS
- Post-restart status: `career_emu=running`, AgentServer port `19092` listening
- Second preflight validate: PASS
- Final runtime stop: `career_emu=stopped`
- Second game run: `NO`

## Verification

- `uv lock --check`: PASS before and after Runner/harness changes; lock unchanged
- Submission validation: PASS
- Preflight validation before baseline: PASS after runtime became ready
- Post-restart preflight validation: PASS
- Runner source manifest comparison: PASS
- Dataset source/target manifest comparison: PASS
- API Key log/report leak checks: PASS
- `git diff --check`: PASS
- Secret scan: PASS; no API Key in tracked or unignored candidate files
- `.env` and `.career_sim_runner/` Git ignore checks: PASS
- `pyproject.toml` / `uv.lock` changed: `NO`

## Problems / Deviations

- `jiuwenswarm-init` required the official interactive language choice; selected Chinese (`1`) through the CLI prompt.
- The locked `career-emulator update --source distribution` implementation requires a Windows symlink privilege unavailable to the current process (`WinError 1314`). The exact locked distribution files were copied locally and hash-verified; no dependency, Runner, provider, or dataset source was changed.
- The first preflight observed backend startup before AgentServer readiness; a subsequent observable preflight passed. No baseline was duplicated.

## Decision Boundary

- This task proves only the frozen Runner plus minimal no-op baseline technical loop.
- The low baseline score is not strategy evidence and is not used to choose architecture.
- No formal competition Agent Skill, Memory, Planning, Risk Control, Team, or Swarm was developed.
- S01 completion was not declared; this result returns to the S01 Stage review boundary.

## Next Recommended Action

Return to the S01 Stage chat for review. Do not start the next task automatically.
