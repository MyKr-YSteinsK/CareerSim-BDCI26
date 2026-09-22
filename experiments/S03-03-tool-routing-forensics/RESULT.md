# S03-03｜运行时工具路由失败取证

## Status

- `COMPLETE`
- Branch: `codex/s03-03-tool-routing-forensics`
- Parent SHA: `488017113fe3ab491dada55be478870f1447c0cf`
- Frozen Runner SHA: `f61c738c72e51b77298cc1c14c7c6ebf4b6c527d`
- Recovery Decision: `FRAMEWORK_OR_RUNNER_DEBUG_NEEDED`
- Scope: 仅离线比较既有 S02 known-good 与 S03-02 failed evidence；未启动服务、未调用 provider、未创建新 CareerSim 游戏、未重跑 S03-02 smoke。

本结果定位了 S03-02 未进入 CareerSim 工具链的直接运行时分歧；不修改 Risk Skill、Runner、依赖或 MCP 配置，也不宣布 S03 完成。

## Evidence Integrity｜证据完整性

| Evidence | Path | Expected SHA256 | Actual SHA256 | Match |
| --- | --- | --- | --- | --- |
| S02 events | `D:/CS/CareerSim-s02-01-minimal-agent-skill/.career_sim_runner/career_emu/outputs/local-s02-01-skill-smoke/20260922T131748Z/events-20260922T131748Z.jsonl` | `9EDC4E7DF623E4328579C1AE08956BF5501D05FDE26AB7D9E4543D367802AA63` | `9EDC4E7DF623E4328579C1AE08956BF5501D05FDE26AB7D9E4543D367802AA63` | `PASS` |
| S02 transcript | `D:/CS/CareerSim-s02-01-minimal-agent-skill/.career_sim_runner/career_emu/outputs/local-s02-01-skill-smoke/20260922T131748Z/transcript-20260922T131748Z.log` | `2CADB6E273DE57466F7B214A261807C23365EE77711C67075050F7514194F2D8` | `2CADB6E273DE57466F7B214A261807C23365EE77711C67075050F7514194F2D8` | `PASS` |
| S03 events | `D:/CS/CareerSim-s03-02-risk-review/.career_sim_runner/career_emu/outputs/local-s03-02-risk-review-smoke/20260922T142853Z/events-20260922T142853Z.jsonl` | `F717053CC5DDD48FB95BCF9ADB413CD015C4A398B22D16FAC4A3CE5C32B9991E` | `F717053CC5DDD48FB95BCF9ADB413CD015C4A398B22D16FAC4A3CE5C32B9991E` | `PASS` |
| S03 transcript | `D:/CS/CareerSim-s03-02-risk-review/.career_sim_runner/career_emu/outputs/local-s03-02-risk-review-smoke/20260922T142853Z/transcript-20260922T142853Z.log` | `9D4395A3DE800C8A99053346D2FA0CFDEFF3EF13D1FFFF20114C7015E92343CD` | `9D4395A3DE800C8A99053346D2FA0CFDEFF3EF13D1FFFF20114C7015E92343CD` | `PASS` |

The S02 raw runtime files remain in the historical S02 worktree. Shared JiuwenSwarm workspace files were overwritten by S03-02; therefore S02 `IDENTITY.md` is not claimed as a preserved file. Its content is reconstructed deterministically from the frozen `identity.md` template and the historical S02 manifest, while S03 `IDENTITY.md` is the post-run file written at `22:28:51`.

## S02 vs S03 Comparison｜S02 与 S03 对照

| Layer | S02 known-good | S03-02 failed | Material difference? | Evidence |
| --- | --- | --- | --- | --- |
| Frozen Runner SHA | `f61c738c72e51b77298cc1c14c7c6ebf4b6c527d` | same | `NO` | frozen source lock / both result records |
| Python / packages | CPython `3.12.13`; uv `0.11.16`; `jiuwenswarm==0.2.4b3`; `career-emulator==1.0.1`; data `1.0.0` | same frozen environment | `NO` | S02 result, Source Lock, unchanged `career_sim_runner`/lock comparison |
| Request model | `deepseek-flash` | `deepseek-flash` | `NO` | runtime state files |
| Manifest mode | `agent` | `agent` | `NO` | historical active install manifests |
| Manifest instruction | empty | empty | `NO` | historical active install manifests |
| Participant Skills | `career-action-trace` | `career-action-trace`, `risk-review` | expected task delta | active install manifests; both `skill_tool` loads succeeded |
| Rendered `IDENTITY.md` | deterministic normalized SHA `9DD3C51CC66FBECE3893AC236770B64BE46FC17BC5D5EA29C93026C0F8E93B44` | actual normalized SHA `5B413A66082B1717960981D5B12330A7531061E7462B2358FB576BD3C5133F23` | only installed-skill list | frozen template + manifests; S03 actual file matches deterministic render |
| Play prompt | SHA `41B0D0F2AC7A5E49E86DEA74AF26DC4E29F4A002B143B4A15486615838B03EC0` | same | `NO` | frozen `play_headless.md` |
| WebSocket envelope | `mode=agent`, `work_mode=work` | same | `NO` | frozen `ws_client.py` |
| MCP config text | historical registration succeeded | post-run config contains enabled stdio server, bare command `career-emulator-mcp`, same generated `cwd` pattern; registration failed in run window | runtime outcome differs | `setup.py`, current post-run config, timestamped logs |
| Skill registry | one enabled project Skill | two enabled project Skills | expected task delta | post-run `skills_state.json`; S02/S03 load events |
| MCP registration | `add mcp server succeed` at `21:17:49` | `add mcp server failed` at `22:28:53.557` and `.683`; `Stdio connection failed: [WinError 2]` | **YES** | `runner.log`, `jiuwen.log`, `agent_server.log` |
| First 20 tool calls | CareerSim path begins at call 2/4/10 | workspace/config inspection and generic tools; no CareerSim MCP call | **YES** | raw events |
| First CareerSim MCP call | event seq `4`: `show_employee_handbook` | none | **YES** | raw events |
| First generic non-Skill call | none before handbook | event seq `2`: `read_file(IDENTITY.md)` | **YES** | raw events |
| First failure | none in bounded S02 evidence | runtime MCP spawn error before model tool chain; event seq `108` generic `powershell` returned `success=False`, seq `112` `fetch_webpage` was `status=error` | **YES** | logs/events |
| Game session | `73b854989f764fe8803760206ce3b9bd` | none | **YES** | raw events / S03 evidence |

Static Runner validation did not detect this condition: `validate.py` checks MCP text/config presence and backend reachability, while actual Stdio registration failed later in the AgentServer. `headless_play.py` proceeds after `reload_agent_config` and does not assert that the CareerSim MCP server registered successfully.

## Initial Tool-call Sequences｜初始工具调用序列

### S02 known-good

The first material sequence was:

`seq 2 skill_tool(career-action-trace) → seq 4 mcp_career-emulator_show_employee_handbook → seq 10 mcp_career-emulator_new_game → seq 14 observe → seq 18 take_action`

The S02 `new_game` result created game session `73b854989f764fe8803760206ce3b9bd`; subsequent canonical observe/action calls continued through month `15`.

### S03-02 failed

The first material sequence was:

`seq 2 read_file(IDENTITY.md) → seq 4 skill_tool(career-action-trace) → seq 6 skill_tool(risk-review) → seq 14 list_files(workspace) → seq 16 list_files(project) → seq 22 list_files(extensions) → seq 24 read_file(agent-data.json) → seq 30 read_file(config.yaml) → seq 34 powershell → seq 36 powershell`

The first 20 actual S03 tool-call names were:

`read_file, skill_tool, skill_tool, list_files, list_files, list_files, read_file, read_file, powershell, powershell, powershell, powershell, read_file, read_file, read_file, grep, list_files, read_file, read_file, read_file`.

No `mcp_career-emulator_*` tool call occurred in all `60` S03 tool calls; the events contain `58` corresponding tool results.

## Last Common Behavior｜最后共同行为

Both runs:

1. used the same frozen Runner prompt and `mode=agent` / `work_mode=work` envelope;
2. created an AgentServer conversation and received model output;
3. loaded the project Skill(s) through `skill_tool` successfully;
4. had generic JiuwenSwarm tools available.

The common behavior ends before a valid CareerSim action chain. S02 had a registered CareerSim MCP server; S03 did not.

## First Material Divergence｜首次实质分歧

### Runtime divergence

`S02 21:17:49: add mcp server succeed` versus `S03 22:28:53.557/22:28:53.683: add mcp server failed`.

The underlying timestamped JiuwenSwarm log records:

`Stdio connection failed: [WinError 2] 系统找不到指定的文件。`

AgentServer then records `MCP server register failed: career-emulator`. This occurred before the S03 model began its generic workspace investigation.

### Model-level divergence after Skill load

S02 immediately called `mcp_career-emulator_show_employee_handbook` at event seq `4`. S03 first read `IDENTITY.md` at seq `2`, loaded both Skills, then investigated the workspace and config; its transcript explicitly says the game tools were absent from the function list. This is the observable consequence of the MCP registration failure, not evidence that `risk-review` changed its own tool authority.

## Runtime Config / MCP Exposure Findings｜运行时配置与 MCP 暴露

- S02 timestamped `runner.log` records a successful `career-emulator` Stdio registration and `jiuwen.log` records five Career Emulator tools added and called through Stdio.
- S03 timestamped `runner.log` records `add mcp server failed` for `career-emulator`; `jiuwen.log`, `agent_server.log` and `full.log` all record the same `Stdio connection failed: [WinError 2]` / register-failed condition.
- S03 failure occurred at `22:27:06`, again after reload at `22:28:03`, and twice at the smoke start/reload at `22:28:53`; this is not a single model choice.
- At S03 smoke time the runtime registered generic tools such as `read_file`, `list_files`, `powershell`, `bash`, `grep`, `fetch_webpage`, `wiki_query`, `task_tool` and `skill_tool`, but no CareerSim MCP resources. The `runner.log` resource-server failure and the events agree.
- S03 `skills_state.json` is a post-run state file, but it confirms both project Skills were enabled; the direct smoke `skill_tool` results independently confirm both Skill bodies were read.
- S03 current post-run `config.yaml` contains an enabled stdio `career-emulator` server with `command: career-emulator-mcp`, `args: [--update, skip]`, and `cwd: D:\CS\CareerSim\.venv\Scripts\`. `career-emulator-mcp.exe` exists at that path when inspected after the run, but the historical log does not identify whether the missing target was the command resolution, working directory, or a child dependency. No exact missing path is invented.
- `validate.py` and `headless_play.py` contain a verification gap: static config presence and `reload_agent_config=True` are treated as sufficient to proceed; actual MCP registration is not asserted before the play prompt.

## Root Cause Classification｜根因分类

- **Category:** `RC-A — MCP tools were not exposed / unavailable`
- **Confidence:** `CONFIRMED` for the direct cause; `HIGH_CONFIDENCE` that the failure is an instance/runtime Stdio registration problem; exact missing filesystem target remains `UNKNOWN`.
- **Cause:** During the S03-02 run window, the `career-emulator` Stdio MCP server failed to spawn/register with `[WinError 2]`. Consequently, CareerSim MCP tools were absent from the Agent tool surface, so no `new_game` could be called.
- **Contributing Factor:** `RC-D — Runtime / instance state drift` is `HIGH_CONFIDENCE` as a category: S02 and S03 have different timestamped MCP registration outcomes, and S03 reload did not restore registration. The Runner's static validation/reload checks did not detect the live registration failure.
- **Model/tool-routing observation:** `RC-B` is a downstream symptom, not the primary cause. Once the MCP server was unavailable, the model routed to generic file/shell/web/task tools while trying to recover.

## Cause / Contributing Factor / Non-cause｜因果边界

### Cause

Unavailable `career-emulator` MCP due to failed Stdio registration in the S03-02 runtime.

### Contributing Factors

- Bare MCP command resolution / child-process launch context is not captured sufficiently to identify the exact missing target.
- `validate.py` validates configuration text and executable availability heuristically, not an actual MCP handshake/tool registry.
- `headless_play.py` continues after config reload without a live CareerSim MCP registration assertion.

### Non-cause

- `risk-review` installation/discovery/load failure: excluded; both `skill_tool` reads returned success and canonical/staging/runtime hashes matched.
- `career-action-trace` or second-Skill manifest corruption: excluded; S03 manifest and rendered identity are deterministic and valid.
- Prompt / `mode` / `work_mode` drift: excluded by frozen source hashes and identical manifest instruction/mode.
- Provider model mismatch: excluded; both runs used `deepseek-flash`.
- WebSocket continuation failure: not supported as primary cause; the S03 session was created, streamed model output, and generic tool calls executed after MCP registration failure.
- Stochastic model routing as the primary cause: excluded by the timestamped deterministic MCP registration error before model routing.

## Root Cause Confidence｜根因置信度

| Finding | Confidence | Basis |
| --- | --- | --- |
| S03 had no CareerSim MCP tool exposure | `CONFIRMED` | zero CareerSim calls in 118 event rows; two server-side registration failures at smoke start; generic tool registration present |
| S03 failed at MCP Stdio registration | `CONFIRMED` | `runner.log` `add mcp server failed`; `jiuwen.log` `[WinError 2]`; AgentServer register warning |
| Exact missing filesystem target | `UNKNOWN` | available logs give WinError 2 only; post-run executable presence does not reconstruct child launch context |
| Risk Skill text caused routing failure | `UNKNOWN` but unsupported | Skill loaded; no direct text-to-failure evidence; not modified |

## Recovery Decision｜恢复决策

`FRAMEWORK_OR_RUNNER_DEBUG_NEEDED`

The next boundary is JiuwenSwarm/MCP Stdio registration and Runner live-MCP verification. This task does not patch `setup.py`, `validate.py`, `headless_play.py`, the frozen dependency, or `risk-review`; it also does not run a recovery smoke.

## Helper Skill Trigger｜辅助 Skill 触发

- `experiment-manager`: `NEAR_TRIGGER`；已有 S01 baseline、S02 smoke、S03-02 smoke，run/token/failure metadata 已形成重复结构；本任务不创建。
- `framework-debugger`: `TRIGGERED`；根因已落到 JiuwenSwarm/MCP Stdio registration/runtime exposure，需要系统级排障；本任务不创建，只返回 Stage Review。

## Strategy Boundary｜策略边界

- Risk Hypothesis: still active; S03-02 technical failure does not falsify it。
- Risk effectiveness: `NOT_PROVEN`
- Controlled screening: `NOT_STARTED`
- No claim is made about action reconsideration, survival, score, risk reduction or Hidden Test generalization。

## Problems / Unknowns｜问题与未知

- `WinError 2` 没有在现有日志中说明具体缺失的是 executable、working directory 还是子进程依赖。
- Shared instance runtime state is post-run for S03-02; current config/skills files are not treated as a complete historical snapshot。
- S02 `IDENTITY.md` 原始文件已被共享实例后续安装覆盖；本结果只使用模板与历史 manifest 做确定性重建。
- 需要新 recovery smoke 才能验证某个 launch-context 修复是否恢复 CareerSim tool exposure；按任务合同标记为 `EXPERIMENT_NEEDED`，不在本任务执行。

## Changed Files｜变更文件

- `experiments/S03-03-tool-routing-forensics/RESULT.md`
- `experiments/S03-03-tool-routing-forensics/comparison.json`
- `docs/project/CURRENT_STATE.md`

未修改 `skills/risk-review/SKILL.md`、`skills/career-action-trace/SKILL.md`、`career_sim_runner/`、`uv.lock`、依赖、MCP 配置或任何 raw runtime log；未提交 `.env`、instance env、数据库、transcript 或 events。

## Verification｜验证

- S02/S03 raw evidence SHA256: `PASS`
- Compact JSON parse: `PASS`
- Offline event/log comparison: `PASS`
- No provider/model call in S03-03: `PASS`
- No CareerSim game/new_game in S03-03: `PASS`
- Frozen Runner source and `uv.lock` unchanged: `PASS`
- `risk-review` unchanged: `PASS`
- `career-action-trace` unchanged: `PASS`
- Secret sanity: `PASS`; no credential value read or emitted
- `git diff --check`: `PASS`

## Next Recommended Action｜下一建议动作

只返回 `S03 Stage Review`，审阅 `FRAMEWORK_OR_RUNNER_DEBUG_NEEDED` 与 MCP Stdio 注册失败证据；不得在本任务中重跑 smoke、开始 controlled screening 或宣布 S03 完成。
