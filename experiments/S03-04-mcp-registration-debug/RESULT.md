# S03-04｜CareerSim MCP Stdio 注册根因与无模型恢复预检

## Status｜状态

- **Status:** `COMPLETE`
- **Recovery Decision:** `NEEDS_MINIMAL_ENVIRONMENT_REPAIR`
- **S03-05 Readiness:** `NOT_READY`
- **Branch:** `codex/s03-04-mcp-registration-debug`
- **Base / S03 Parent SHA:** `c63108d772d1ee124e1f5459b6a112489d00d745`
- **Governance SHA / merged origin/main:** `69a394ee226da80282b06e1034b10b1bf70d5090`
- **Governance merge commit:** `c8ed0ac665c2e9a43b34851da9daf2b4328ea143`
- **Evidence commit:** 本文件与证据随本分支交付；最终 commit SHA 见 TASK_RESULT
- **Frozen Runner SHA:** `f61c738c72e51b77298cc1c14c7c6ebf4b6c527d`
- 本任务没有宣布 S03 完成。

## Permission Used｜实际权限

- `READ_ONLY`：repo、冻结源、安装元数据、历史 RESULT、runtime logs 与保全证据。
- `REPOSITORY_WRITE`：本 RESULT、紧凑证据及 `CURRENT_STATE.md`。
- `LIVE_RUN`：3 个不同的直接 MCP Stdio spawn 变体，每个仅执行 1 次；没有 retry。
- Provider/model calls：`0`；DeepSeek/API Key 未读取或传入子进程。没有 provider usage；tokens / cost 不适用。
- CareerSim `new_game`：`0`；tool calls / gameplay：`0`。

## FORENSIC_HOLD｜取证保全

- ID：`FORENSIC_HOLD:S03-MCP-REGISTRATION`
- Status：`ACTIVE / UNCHANGED`
- Owner：`S03 Stage`
- Release authority：`Main Hub / S03 Stage Review`
- 原件没有删除、迁移、覆盖或提交；hold 内容、路径、bytes、SHA256、时间窗与原因均登记于 [debug_evidence.json](debug_evidence.json)。
- 解除条件：精确根因被接受；紧凑证据足以独立支撑结论；恢复预检完成；后续 smoke 不再依赖原件解决未决根因；Main/Stage 明确解除。

保全集包含 S02 known-good events / transcript、S03-02 failed events / transcript，以及共享 JiuwenSwarm 的 `runner.log`、`jiuwen.log`、`agent_server.log`、`full.log` 和 `server.log` 相关时间窗。复核的 S02 / S03-02 events 与 transcript hashes 均与 S03-03 记录一致。

## Environment Identity｜环境身份

- Python：CPython `3.12.13`，`D:\CS\CareerSim\.venv\Scripts\python.exe`
- uv：`0.11.16`；jiuwenswarm：`0.2.4b3`；career-emulator：`1.0.1`；mcp：`1.27.2`；fastmcp：`2.14.7`
- Console entry point：`career_emulator.run_mcp:main`
- MCP launcher：`D:\CS\CareerSim\.venv\Scripts\career-emulator-mcp.exe`，存在，46,080 bytes；SHA256 `90F7704FD41B8F51414C375AA07A168B4A419D64516CF4E3CACE275325A42374`
- Paired interpreter：`D:\CS\CareerSim\.venv\Scripts\python.exe`，存在，262,144 bytes；SHA256 `74E020321EB8F828F0C2CFE865082FCF94AA6E7CF488E8A744D89B9282EAEB83`
- S03-04 与 S03-02 worktree 都没有自己的 .venv；诊断使用既有 CareerSim root venv，没有安装或升级依赖。
- 当前进程 PATH 不含 `D:\CS\CareerSim\.venv\Scripts`；PowerShell `Get-Command`、`where.exe` 与 Python `shutil.which` 均不能解析 `career-emulator-mcp`。配置 cwd 目录和 executable 本身存在。
- 紧邻 S03-02 首次报错前写入的 instance config snapshot（2026-09-22 22:26:05 +08:00）：command `career-emulator-mcp`、args `--update skip`、cwd `D:\CS\CareerSim\.venv\Scripts\`。历史 AgentServer 实际 PATH 未记录。
- uv.lock SHA256：`18466056430F7C49C3A23705D312625B40B1A5119C41F0EC62571CDA208E4C0C`。

## Historical Failure Anchor｜历史失败锚点

- S02 known-good：2026-09-22 21:17:49.327 +08:00，runner.log 记录 `add mcp server succeed` 并报告五个 Career Emulator tools。
- S03-02 failed：22:27:06.934、22:28:03.317、22:28:53.557、22:28:53.683 +08:00，runner.log 记录注册失败；Jiuwen / AgentServer logs 同窗记录 `Stdio connection failed: [WinError 2]`。
- S03-02 config 的 command、args 和 cwd 与本任务第一种探针相同。历史 AgentServer PATH 未保留，当前 PATH 不冒充历史测量值。

## Offline Findings｜离线发现

### Root Cause｜根因

- **F1 command resolution：HIGH_CONFIDENCE，首要根因。** 未解析的 spawn target 是 bare command `career-emulator-mcp`，对应文件为 `D:\CS\CareerSim\.venv\Scripts\career-emulator-mcp.exe`。MCP SDK Windows resolver 先用 `shutil.which` 查找 command；找不到就原样返回 bare name，之后才把 cwd 传给 Windows process creation。cwd 指向 executable 所在目录仍不能弥补 AgentServer PATH 缺少 Scripts。
- **F5 inherited process environment：HIGH_CONFIDENCE contributing cause。** 锁定 JiuwenSwarm 的 `start_services.py` 用 `os.environ.copy()` 启动服务子进程，MCP resolver 查找的是 AgentServer PATH。该历史 PATH 未保存；当前同环境重现缺少 Scripts 时得到相同 WinError 2。
- **F3 broken launcher / F4 child dependency：当前身份下已排除。** 绝对 executable 成功完成 MCP initialize 与 tools listing。
- **F2 stale cwd：当前检查排除。** 记录的 cwd 存在；绝对路径在该 cwd 下通过。
- **F6 stale instance/reload：未确认。** 多次 reload 均失败，但历史 service process 环境不能重建。
- **F7 detection gap：CONFIRMED。** Runner 静态检查只看 launcher/fastmcp 文件；不验证 AgentServer 实际 PATH 或 MCP initialize/tools。validate_environment 会生成 MCP check，但 headless_play 仅将 backend 不可达作为阻断条件；reload 成功不确认 MCP 注册。

### Spawn Probes｜启动探针

| # | command / cwd | 结果 | retry |
| --- | --- | --- | ---: |
| 1 | bare `career-emulator-mcp`；历史精确 cwd；`--update skip` | FAIL，`FileNotFoundError [WinError 2]`，47 ms；与历史错误一致 | 0 |
| 2 | 绝对路径 `career-emulator-mcp.exe`；继承 cwd；`--update skip` | PASS；initialize 与 list_tools 通过，返回 5 个 CareerSim tools | 0 |
| 3 | 绝对路径；历史精确 cwd；`--update skip` | PASS；initialize 与 list_tools 通过，返回相同 5 个 tools | 0 |

每项 timeout 为 8 s；使用 MCP 1.27.2 Stdio client / Windows executable resolver。子进程只继承 MCP SDK 安全 allowlist，并覆盖 5 个非敏感 `CAREER_EMULATOR_*` 字段；没有传入 provider 凭据。只执行 protocol initialize 和 `list_tools`，不调用任何 CareerSim tool；`--update skip` 避免数据更新。子进程由 stdio context 关闭；事后无 emulator / JiuwenSwarm 进程、无监听端口，也未创建探针 DB 或 log directory。详细结果见 [debug_evidence.json](debug_evidence.json)。

## Service Startup｜服务启动

- started：`NO`
- reason：S02 startup log 曾出现模型调用迹象；本任务没有证明 AgentServer startup/prewarm 可完全避开 provider。
- provider/prewarm risk：direct emulator MCP server 可无模型 initialize/list tools；AgentServer integration registration 未验证。

## Minimal Recovery｜最小恢复

- 已验证的 transient repair：MCP command 使用该 venv 的绝对 executable 路径；direct spawn 与 protocol handshake 均 PASS。
- 持久环境 / instance config 未修改；未改 Runner setup.py 或 MCP config generator。正式注册需要启动 AgentServer，而该 service 的 no-provider/prewarm 条件未获证明。
- 后续持久修复交由 Stage Review 决定；优先在获授权 smoke 配置中使用绝对 command path，避免改 frozen Runner。

## Detection Gap｜检测缺口

Runner 从 jiuwenswarm-start 的 PATH 位置推导 cwd，再用同目录 glob 检查 launcher；这不能证明 AgentServer inherited PATH 可解析 bare command。MCP SDK 在 spawn 前按自身 PATH 调用 shutil.which，cwd 仅传给后续进程创建。validate / reload 链没有 MCP initialize 或 required tools assertion，headless play 忽略除 backend 外的失败 check。

Future guard：project-owned preflight wrapper 按最终 command / args / cwd / env 启动 Stdio MCP，执行 initialize 与 list_tools，并 fail closed 检查五个必需 CareerSim tools。本任务未实现 wrapper，也未改 frozen Runner。

## S03-05 Readiness｜下一步就绪度

- `NOT_READY`
- 理由：绝对路径 repair 只用于临时探针，尚未应用到 recovery smoke 的 service config；AgentServer registration 和 prewarm/provider 边界未验证。本任务不运行 recovery smoke。

## Helper Status｜辅助能力

- `framework-debugger = TRIGGERED`；没有新增比赛 Skill / helper Skill。
- `experiment-manager = NEAR_TRIGGER`；没有创建。
- `Astra = ASTRA_NOT_NEEDED`。

## Strategy Boundary｜策略边界

- Risk Hypothesis：`ACTIVE`
- Risk effectiveness：`NOT_PROVEN`
- Controlled screening：`NOT_STARTED`

## Problems / Unknowns｜问题与未知

- 历史 AgentServer 完整 process PATH 未保存；历史归因是 HIGH_CONFIDENCE，不是历史 PATH 的直接测量。
- Service-level registration 未验证；本任务没有启动 service 或触发 provider。
- S02/S03 raw runtime evidence 按 hold 保留于原路径；不提交 raw logs、events、transcript、DB、instance env 或密钥。

## Changed Files｜变更文件

- `experiments/S03-04-mcp-registration-debug/RESULT.md`
- `experiments/S03-04-mcp-registration-debug/debug_evidence.json`
- `docs/project/CURRENT_STATE.md`

## Verification｜验证

- S03 parent 与 governance commit ancestry：PASS
- root checkout：本地 main 保持 `031d97e56e0ce305a487b4bc293c7abde58cfdf0`、干净且落后于 origin；未同步或修改。
- `uv lock --check --python D:\CS\CareerSim\.venv\Scripts\python.exe`：PASS（CPython `3.12.13`；uv `0.11.16`）
- `git diff --check`：PASS
- Frozen Runner files / `uv.lock` / `career-action-trace` / `risk-review` 相对 S03 parent：unchanged
- FORENSIC_HOLD events/transcript hashes：PASS
- Provider/model calls：0；new_game/gameplay：0
- Probe processes cleaned；probe DB/log directory：not created
- `.env` 未出现在 worktree；被 Git ignore；tracked env files：none
- Service start / recovery smoke：NOT RUN

## Next Recommended Action｜下一建议动作

只返回 `S03 Stage Review`，审阅 HIGH_CONFIDENCE executable resolution 根因、持久最小修复方式及后续一次 recovery smoke 的 provider/prewarm 边界。
