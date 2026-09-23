# SCORE-01｜当前 Submission 完整跑分闭环

## Result

- Status: COMPLETE
- Decision: CURRENT_SUBMISSION_SINGLE_RUN_SCORE_CHECKPOINT
- This is one local Dev terminal result from the current two-Skill submission. It is not Risk-effectiveness, score-improvement, or Hidden Test generalization evidence.

## Identity / Frozen Environment

- Branch: codex/score-01-full-score-checkpoint
- Base SHA: eeb635230e0e33a915cb439988f421b5516a61ef (fetched origin/main at task start)
- Parent: none
- Official Runner source lock: openJiuwen-ai/CareerSim-BDCI26@f61c738c72e51b77298cc1c14c7c6ebf4b6c527d
- Python / uv: CPython 3.12.13 x64 / uv 0.11.16
- Direct packages: jiuwenswarm 0.2.4b3; career-emulator 1.0.1; career-emulator-bdci26 1.0.0
- pyproject.toml SHA256: B399225F2C00B415F3C8A3317F8CDECF72114AE7A41111B4410F201466E40F73
- uv.lock SHA256: 18466056430F7C49C3A23705D312625B40B1A5119C41F0EC62571CDA208E4C0C
- Provider: DeepSeek official endpoint https://api.deepseek.com; request/usage model deepseek-flash. Windows User-level and instance API_KEY presence were checked without reading or recording the value.
- Existing Source Lock qualification remains: underlying serving version PARTIALLY_VERIFIED.

## Submission Identity

- Mode: agent
- Local manifest identity: team=local-score-01-full-score-checkpoint; name=score-01-current-submission
- Ignored staging: D:/CS/CareerSim/.local/runtime/score-01-full-score-checkpoint/submission
- Manifest SHA256: 5A61A014B830E3E49943FE6211CAB61F562E38561A5CA854A01E932AC0FA74AE
- career-action-trace canonical/staged SHA256: 5246D7F00CA7FD087C874700B9B724A29992499BCF1AA66BAB66D8CE37810124
- risk-review canonical/staged SHA256: CDCA984D990BCE77AF40CABC4CEAB84263CCCC11AF0DCB75B1765314A3176FD5
- Submission-only validation: PASS. Full Runner environment validation: PASS (overall_ok=True), including dataset, command availability, MCP configuration, DB alignment/writability, skills directory, and AgentServer backend reachability.
- No canonical Skill, Runner, dependency, pyproject.toml, or uv.lock changes were made.

## Runtime / Game Identity

- Pre-state: career_emu stopped; no configured listener or relevant runtime process. The configured shared MCP DB contained one known incomplete historical S03-14 session (4e36f0a1dec4451a8c673998c22f30e4), not a running process/session.
- Shared MCP config and instance environment SHA256 remained unchanged: config 05928EFAED4508D2C1A70C6B32B704CADB3B1CD40026A5CDA0D91EDD4878DEFE; instance .env 99842010A7B39B038AFE05009B75BC259BFEA34CFF40D93C9D41325167E8B8CD.
- The existing MCP config points CAREER_EMULATOR_DB to D:/CS/CareerSim-s03-02-risk-review/.career_sim_runner/career_emu/career_emulator.sqlite3. To avoid mutating shared config and ensure scoring reads the same DB as MCP, the single validate/play invocation explicitly supplied that existing path with --db.
- Service lifecycle: one start at 2026-09-23 22:42:13 +08, instance PID 20332, AgentServer port 19092; one graceful stop at 22:55:20 +08, stop exit code 0. Final state stopped; target listeners=0; relevant processes=0. Restart retries=0.
- Validation command used the active project-root environment with uv run --no-sync --active. No make play, dependency sync/upgrade, provider test, or standalone Agent chat was run.
- Exactly one Runner play was started at 2026-09-23T22:44:54.8861412+08:00, with timeout 7200s and no --continue. Runner scoring completed at 2026-09-23T22:54:27.619032+08:00; elapsed 9m32.733s.
- Runner play count=1; fresh new_game count=1; gameplay retry count=0. Event evidence records 1 show_employee_handbook, 98 observe, 98 take_action, and 2 skill_tool results.
- Drive session: career-sim-runner-ca53f36571f6
- Game session: 8ffa91ac75e143cfb68b015feb4f40e4
- play_exit_code=0; termination_reason=null; terminal outcome=eliminated at month 24. completed=false is expected for this legal early terminal; a 48-month completed career is not claimed.

## Final Score

| Field | Result |
| --- | --- |
| quantitative_score | 33.06 |
| competition_partial_score | 23.14 |
| survival_months | 24 |
| grade | D |
| completed / terminal status | false / eliminated |
| game session ID | 8ffa91ac75e143cfb68b015feb4f40e4 |
| drive session ID | career-sim-runner-ca53f36571f6 |
| termination reason | null / unavailable |
| play exit code | 0 |

The canonical score report is score_report.json. Its score fields were independently compared with the read-only DB row for this fresh session and matched.

## Provider Usage

- One incidental service-start/prewarm usage record was observed at 2026-09-23 22:42:32 +08: model deepseek-flash; input 200, output 1, total 201; cache hit 0, cache miss 200. No cost field was available.
- Gameplay usage reported by the Runner for deepseek-flash: input 19,919,228; output 77,319; total 19,996,547; cache_tokens 19,705,216; cache_hit_rate 98.9%.
- Including the startup record, observable task usage totals 19,919,428 input / 77,320 output / 19,996,748 total tokens. The gameplay cache fields came from the Runner usage event; startup cache fields came from the appended JiuwenSwarm LLM log.
- Runner reported total_cost=0.0 for gameplay. This is not treated as the actual DeepSeek bill; actual billed cost is UNAVAILABLE. No additional provider/account query was made.
- The play stream contained one empty “unknown” usage summary and one populated deepseek-flash usage summary; only the populated record is counted above.

## Raw Evidence (ignored/local; not committed)

| Artifact | Bytes | SHA256 |
| --- | ---: | --- |
| Runner score report source: D:/CS/CareerSim/.local/worktrees/score-01-full-score-checkpoint/.career_sim_runner/career_emu/outputs/local-score-01-full-score-checkpoint/20260923T144458Z/score_report.json | 2,951 | 1B61B22A980E65A89170FD25B054A2563CE5ECF2D82BFFD4DFD15948CCF08669 |
| Events: D:/CS/CareerSim/.local/worktrees/score-01-full-score-checkpoint/.career_sim_runner/career_emu/outputs/local-score-01-full-score-checkpoint/20260923T144458Z/events-20260923T144458Z.jsonl | 975,641 | C208BF46E811176E19EF42B83BEB6C39796F54A5EF6F2B22818F867ED6E0E262 |
| Transcript: D:/CS/CareerSim/.local/worktrees/score-01-full-score-checkpoint/.career_sim_runner/career_emu/outputs/local-score-01-full-score-checkpoint/20260923T144458Z/transcript-20260923T144458Z.log | 229,510 | FC5557673CB0CA31191347D5511C34D63ADEDF1E23A17EE60404AC8B92451C1A |
| Shared llm.log after run: C:/Users/Yukis/.jiuwenswarm-instances/career_emu/logs/logs/llm.log | 3,657,082 | F2F1CA1E887AF92D6C142A43EF5324863E4A9314D6568414911DA14B865E3DF2 |
| Shared runner.log after run | 1,564,408 | 060AF2A4C84073905DAC4256339893BE3E1B6AFC54E45E20A26E1B719A422090 |
| Shared server.log after run | 59,597 | 34A3A3B8D636F47BC143C671E87975E4125121EB8A7AF4E3D51F661D98D97337 |
| Shared run/jiuwen.log after run | 1,799,764 | 4404555EF1B1B3E9C9C8547A2DC6936AB6A006E7936483601B4F156524A935F0 |

Lifecycle stdout/stderr captures are retained under D:/CS/CareerSim/.local/runtime/score-01-full-score-checkpoint/; their byte counts and SHA256 values are in score_evidence.json. Raw logs, staging files, instance config/environment, DB, and credentials are not committed.

## Verification / Boundaries

- uv lock --check with explicit project CPython 3.12.13: PASS; 252 locked packages resolved without sync.
- Root environment pip check: PASS; installed Python and direct package versions match the frozen environment.
- Submission static validation and full environment validation: PASS.
- Score report versus read-only DB score: PASS.
- One service start / one Runner play / one fresh game / zero retries / one graceful stop: PASS.
- Canonical/staged Skill hashes match; frozen Runner, dependencies, and lock have no diff from base.
- No tracked .env or credential; local staging/runtime paths are ignored. SCORE-01 does not modify CURRENT_STATE.md.
- git diff --check, authorized-file scope, commit, push, and clean worktree are recorded in the delivery TASK_RESULT.

## Problems / Unknowns

- The run ended by legal elimination at month 24, not by completing month 48; this is still a valid terminal score checkpoint under the Plan.
- Runner's reported cost 0.0 is not authoritative billing evidence; actual API charge is unavailable.
- Underlying serving-version mapping remains PARTIALLY_VERIFIED.

## Deviations

- The Runner --db option was explicitly set to the DB path already present in shared MCP config; this avoided changing that config and was confirmed by the full preflight.
- No scope, strategy, Skill, Runner, dependency, or state-document expansion.

## Strategy Boundary / Next Recommended Action

- Risk Hypothesis = ACTIVE
- Risk effectiveness = NOT_PROVEN
- controlled screening = NOT_STARTED
- No causal comparison with S01 and no strategy-performance or generalization claim.
- Next Recommended Action: Main Hub review only.
