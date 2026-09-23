# CURRENT_STATE

> 当前项目真实快照；不追加过程日志。历史由 Git 保存。

## Current

- App/product version: CareerSim BDCI26；无产品发布版本
- Branch: `main`
- Lifecycle stage: `Discovery`
- S01: `COMPLETE`
- S01_STAGE_ACCEPTANCE: `PASS`
- S02: `COMPLETE`
- S02_STAGE_ACCEPTANCE: `PASS`
- Current Stage: `S03`
- S03: `IN_PROGRESS`
- S03-01: `COMPLETE_ACCEPTED_BY_STAGE_REVIEW`
- S03-02: `BLOCKED_TECHNICAL`
- S03-03: `COMPLETE_FRAMEWORK_OR_RUNNER_DEBUG_NEEDED`
- S03-04: `COMPLETE_ACCEPTED_BY_STAGE_REVIEW`
- S03-05: `BLOCKED_TECHNICAL`
- S03-06: `COMPLETE_PENDING_STAGE_REVIEW`
- S03-07: `BLOCKED_TECHNICAL`
- S03-08: `BLOCKED_TECHNICAL` (branch evidence pending S03 Stage Review)
- S03-09: `BLOCKED_TECHNICAL` (branch evidence pending S03 Stage Review)
- S03-10: `BLOCKED_TECHNICAL` (branch evidence pending S03 Stage Review)
- S03-11: `COMPLETE_PENDING_STAGE_REVIEW` (provider preflight only; no game)
- RISK_BENEFIT: `NOT_PROVEN`
- Current milestone: S03-11 将 S03-10 游戏前的 provider 异常定位到 TLS-start 连接层；当前 JiuwenSwarm `OpenAIModelClient` 非流式与流式各完成 1 次极简请求，provider preflight 通过。未运行游戏，Risk correctness 仍未验证；S03-12 单次 smoke readiness 待 S03 Stage Review。
- Production/published version: none
- Last verified: 2026-09-23

## Major capabilities

- 私有开发仓库已建立，长期工程事实已集中到 `docs/project/`。
- 已保留官方 Source Lock 与当前有效架构决定；根目录已移除启动资料堆积。
- 项目隔离环境已用 CPython 3.12.13 和官方冻结 `uv.lock` 建立；关键依赖版本与基础 import 已验证，详见 [ENVIRONMENT.md](ENVIRONMENT.md)。
- 冻结官方 Runner `f61c738c72e51b77298cc1c14c7c6ebf4b6c527d` 已纳入仓库，并完成 source manifest 核对。
- `baselines/s01-minimal` no-op harness 已通过 submission/preflight validation；完成 1 局 fresh Dev baseline，证据见 [S01-03 RESULT](../../experiments/S01-03-baseline/RESULT.md)。
- `skills/career-action-trace/SKILL.md` 已完成最小 Skill contract、安装/发现/加载与 bounded smoke 应用闭环，证据见 [S02-01 RESULT](../../experiments/S02-01-minimal-skill/RESULT.md)。
- `skills/risk-review/SKILL.md` 已完成事件驱动的最小 Risk Review contract；Runner validation、install、discover、runtime load 均通过，但 smoke 未建立游戏会话，Risk trigger/application 仍未验证，证据见 [S03-02 RESULT](../../experiments/S03-02-risk-review/RESULT.md)。

## Current technical shape

- Windows / PowerShell 开发目标；项目根目录使用被 `.gitignore` 排除的 `.venv`，依赖由官方 `pyproject.toml`/`uv.lock` 管理。
- 官方上游仓库、候选 repo SHA、包版本和运行合同见 [OFFICIAL_SOURCE_LOCK.md](OFFICIAL_SOURCE_LOCK.md)。
- 本地 Runner 使用 `career_emu` named instance、career-emulator MCP 和 Dev 数据；重启后 preflight 已复验。
- Single Agent + Multiple Skills 是当前起步路线；当前有 project-owned `career-action-trace` 与最小 `risk-review` Skill，尚无策略收益证据。
- S03-01 已基于冻结 S01 单局证据形成一个公开警告驱动的最小 Risk Hypothesis；S03-02 已实现 Risk Skill，但 trigger/application 因 smoke 技术失败仍未验证。

## Known limitations / risks

- provider endpoint 已按用户配置使用 DeepSeek 官方 API；请求/usage model 为 `deepseek-flash`，底层 serving version 映射仍为 `PARTIALLY_VERIFIED`。
- 已有 1 个有效 Dev baseline，但为 no-op harness 且在第 19 个月提前结束；分数不构成策略收益或隐藏 Test 泛化证据。
- S02-01 bounded smoke 证明了 Skill 实际读取与 action trace marker 应用；不证明分数提升、策略收益或 Hidden Test 泛化。
- S03-01 只证明基线存在可观察的公开风险预警—埋雷反馈—信任危机终止链；不证明任何单个动作造成终止，也不证明 Risk Control 收益。
- S03-02 唯一 bounded smoke 中 `skill_tool` 成功读取两个 Skill，但运行时调用了不匹配的通用工具路径，未产生 CareerSim `new_game`/`observe`/`take_action`，因此没有 warning、Risk output、marker、action 或收益证据；不得重跑本任务 smoke。
- S03-03 已从既有 S02/S03-02 raw evidence 与 timestamped runtime logs 确认 S02 MCP 注册成功、S03-02 MCP Stdio 注册在 `WinError 2` 下失败。S03-04 复现了裸命令在 AgentServer PATH 不含 Scripts 时产生相同错误；绝对 launcher 路径完成 MCP initialize 与五工具 listing。历史 AgentServer PATH 未留存，归因是 `HIGH_CONFIDENCE`；未启动 service、未调用 provider、未运行 recovery smoke，FORENSIC_HOLD 仍 ACTIVE。
- S03-05 的 5 份共享日志已在 `.local/runtime/forensic-hold/S03-MCP-REGISTRATION/pre-s03-05/` 原样保全且 hash 匹配。配置补丁后严格文本比较不符，仅 command 字段变化未获验证；配置已按原 SHA 恢复。真实 AgentServer 注册仍未验证，`FORENSIC_HOLD` 继续 ACTIVE。
- S03-06 复核 5 份取证快照完整；目标 command 补丁导致该行 CRLF→LF，但 YAML parsed semantic diff 仅 `/mcp/servers/0/command`。修复后一次 clean service startup 中真实 AgentServer 两次报告 MCP 注册成功并暴露五个 CareerSim tools，随后优雅停止；`FORENSIC_HOLD` 仍 ACTIVE。该修复会被 Runner setup 覆写，不能视为永久 Runner fix。
- S03-07 服务级 MCP 与 direct 五工具预检通过；唯一 play 在 Runner 调用 `jiuwenswarm-start --list` 时失败，未创建 drive/game session、events、transcript 或 score report。没有 retry；共享服务已停止。启动期有一条 `deepseek-flash` prewarm usage（200 input / 1 output / 201 total tokens）；startup stderr 另有 10 条非致命 `UnicodeEncodeError`，策略效果仍 `NOT_PROVEN`。
- S03-08 分支将 `.venv\Scripts` 仅前置到 Runner invocation 的进程 PATH；Runner 可解析 `jiuwenswarm-start`，真实 AgentServer 注册两次均成功并暴露五工具。唯一 Runner invocation 随后因 worktree-local active-install record 缺失，在 drive/game 前退出；没有安装、重试、CareerSim tool 或 gameplay。服务 clean stop；startup incidental prewarm 为 `deepseek-flash` 200 input / 1 output / 201 total tokens，cost 未报告。结果为 `BLOCKED_TECHNICAL`，待 S03 Stage Review；Risk effectiveness 仍 `NOT_PROVEN`。
- S03-09 两次 direct preflight 客户端执行中，首次在 spawn 前因 stderr 接收器缺少 `fileno` 失败；第二次完成协议调用后在读取 stderr 时发生 `UnicodeDecodeError`，未保存五工具列表。门禁未通过后停止；install/service/play/game 均为 0，shared logs 与配置未变，Risk correctness 仍未验证。
- S03-10 一次 clean service startup 中当前 AgentServer 三次注册 `career-emulator` 并暴露五工具，标准 play 建立了 active-install 与两项 Skills registry；唯一 play 窗口出现 16 条 `APIConnectionError`，score report `play_exit_code=1`，没有游戏 session、DB、transcript 或 CareerSim action。Runner usage 为 0，provider completed usage/cost 未获可靠记录；服务已停止，未重试，Risk correctness 仍未验证。
- S03-11 原始 traceback 将 S03-10 错误定位为 `httpcore` 的 `start_tls` 阶段连接失败、在 HTTP/provider 响应前；更底层 peer/TLS 原因与历史代理状态未知，不能归咎于特定代理或上游。当前 endpoint/model/config 未确认漂移；DNS/TCP/TLS/无凭据 HTTP 分层探测可达，同一 JiuwenSwarm provider adapter 的 `invoke` 与历史对应的 `stream` 各完成 1 次小请求（合计 66 input / 8 output / 74 total tokens，cache 0，reported cost 不可得）。无服务、Agent chat、CareerSim 工具或游戏；该预检不证明后续游戏或 Risk 策略正确性。
- Windows 无 symlink 特权时，锁定 distribution 数据采用逐文件 hash 核对后的 copy materialization；未使用 GitHub 数据，后续对局仍须保持串行。

## Active work

- S02 已由 Main Hub 正式验收为 `COMPLETE` / `S02_STAGE_ACCEPTANCE = PASS`；S03-01、S03-04 已通过 Stage review；S03-02、S03-05、S03-07～10 保留技术失败记录；S03-06 服务级预检通过；S03-11 provider preflight 通过、证据待 S03 Stage Review，S03 尚未完成。

## Next likely tasks

1. 返回 S03 Stage Review，审阅 S03-11 的 TLS-start 连接层归类及当前同路径 provider 请求恢复证据；是否授权后续单次 Risk correctness smoke 由 Stage 决定，本任务不运行。
2. 继续保持 serving version `PARTIALLY_VERIFIED`、baseline 单局无策略结论、Risk benefit `NOT_PROVEN` 与 shared runtime 串行约束。

## Workflow / delivery facts that are currently material

- 主分支为 `main`，GitHub 远端为私有仓库；初始提交代表仓库初始化。
- secrets、runtime cache、日志、数据库和本机生成状态由 `.gitignore` 排除，不作为工程事实提交。
- S01-02 使用官方 SHA 对应的 `pyproject.toml`/`uv.lock`，以 `uv sync --locked --no-install-project` 安装；未修改冻结 lock。
- S01-03 仅运行 1 局 fresh baseline；score report、transcript、events 和重启验证路径已记录在实验证据中，未提交 `.env` 或 instance env。
- S02-01 仅运行 1 次 fresh bounded smoke；未开发 Memory / Planning / Team / Swarm，也未增加第二 action submitter。
- S03-01 为离线一次性取证；未启动新的 CareerSim、未调用 provider、未创建 `experiment-manager`，未实现 Risk / Memory / Planning / Team / Swarm。
- S03-02 仅运行 1 次 fresh bounded smoke（hard cap `120 s`）；技术失败后未重跑，未创建 `experiment-manager`，未运行对照 screening；Risk benefit 仍 `NOT_PROVEN`。
- S03-03 仅做离线 evidence/log forensics；未启动 `career_emu`、未调用 provider/model、未运行 `new_game` 或 recovery smoke；`experiment-manager=NEAR_TRIGGER`、`framework-debugger=TRIGGERED`，均未创建。
- S03-04 仅运行 3 个 direct no-model MCP Stdio spawn 变体（各 1 次、无 retry）；裸命令复现 `WinError 2`，绝对路径 handshake 返回 5 tools。未启动 JiuwenSwarm service、未调用 provider/model 或 CareerSim tool；`FORENSIC_HOLD:S03-MCP-REGISTRATION` 保持 ACTIVE。
- S03-05 在 shared log snapshot 后尝试一次 instance config command 补丁；严格差异校验失败即恢复原 hash。服务启动、provider/model、Agent chat、CareerSim tool、gameplay 次数均为 0；canonical hold snapshot 留在 `.local/runtime/forensic-hold/`。
- S03-06 保留 pre-edit/candidate 与语义/字节差异证据后完成 instance command 修复；一次 service startup 与一次 stop，真实 MCP 注册通过。Startup 自动发生一条 `deepseek-flash` 完成响应（200 input / 1 output / 201 total tokens，cache hit 0，cost 未报告）；无 Agent chat、CareerSim tool 或 gameplay，Risk benefit 仍 `NOT_PROVEN`。
- S03-07 仅进行 1 次 Runner play 尝试（180 s 上限，0 retry）；裸 `jiuwenswarm-start` 不在 Runner 进程 PATH，导致 `[WinError 2]` 在 AgentServer 连接前退出；fresh game count = 0。service start/stop 各 1；startup prewarm usage 201 tokens，play 无 provider request。安装前已将 Runner install 会清理的旧 JiuwenSwarm session、Skills registry 和 `MEMORY.md` 复制到本机 ignored runtime archive；未提交 raw artifacts 或 credentials。
- 后续任务按 `AGENTS.md` 的主分支、证据、共享 runtime 串行和 Skill 时机规则执行。

## Update rule

仅在当前能力、阶段、限制、Active work 或交付事实发生 material change 时更新；不得把命令流水、临时失败或未来计划写成历史日志。
