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
- Current Stage: `S06-Lab; S06-01 static candidate accepted; S06-02 runtime identity/preflight; no Game Gate authorization`
- S03: `COMPLETE`
- S03_STAGE_ACCEPTANCE: `PASS`
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
- S03-12: `BLOCKED_TECHNICAL` (pre-game correction limit exceeded; Runner play/game not started; service stopped)
- S03-13: `BLOCKED_TECHNICAL` (pre-play tooling STOP; service/play/game not started)
- S03-14: `COMPLETE_ACCEPTED_BY_MAIN` (one observed Risk runtime-correctness path accepted as Stage evidence; no final score or performance claim)
- S03_CLOSEOUT_CANDIDATE: `ACCEPTED_BY_MAIN` ([closeout evidence](../../experiments/S03-CLOSEOUT/RESULT.md))
- S04: `COMPLETE`
- S04_STAGE_ACCEPTANCE: `PASS_WITH_KNOWN_LIMITATION`
- S05: `COMPLETE`
- S05_STAGE_ACCEPTANCE: `PASS_WITH_KNOWN_LIMITATION`
- S05-01: `MAIN_ACCEPTED_MERGED` (`CANDIDATE_V2C_OFFLINE_IMPLEMENTATION_ACCEPTED`)
- S05-02: `MAIN_ACCEPTED_MERGED` (`INTEGRATED_CANDIDATE_OFFLINE_ACCEPTED`)
- S05-03: `COMPLETE_ACCEPTED_BY_MAIN`
- S06: `IN_PROGRESS`
- S06-01: `COMPLETE_ACCEPTED_BY_MAIN` (`ADAPTIVE_CONTROLLER_STATIC_ACCEPTED`; static candidate only)
- S06-02: `IN_PROGRESS` (accepted-candidate integration and local runtime identity/preflight; no live run)
- STATE_BOARD_RUNTIME: `PARTIAL_BUT_SUFFICIENT_FOR_STAGE`
- STATE_BOARD_SCORE_BENEFIT: `NOT_PROVEN`
- CANDIDATE_V1: `HIGH_VARIANCE`
- FORENSIC_HOLD:S03-MCP-REGISTRATION: `RELEASED_BY_MAIN`
- RAW_FORENSIC_EVIDENCE: `RETAINED`
- RAW_EVIDENCE_CLEANUP: `NOT_AUTHORIZED`
- RISK_BENEFIT: `NOT_PROVEN`
- CONTROLLED_SCREENING: `NOT_STARTED`
- GAME_GATE: `ADOPTED`
- MULTI_AGENT / TEAM / SWARM: `DEFERRED`
- CANDIDATE_V2_HYPOTHESIS: `H_MATERIAL_OUTCOME_REPRIORITIZATION` (`OFFLINE_IMPLEMENTED`; gameplay effectiveness `NOT_PROVEN`)
- S05_FINAL_CANDIDATE: `candidate-v2-final-offline` (offline frozen; gameplay effectiveness `NOT_PROVEN`)
- S06_CANDIDATE: `candidate-v3-adaptive-controller-static` (Main-accepted static candidate; gameplay effectiveness `NOT_PROVEN`)
- TARGET: `STABLE_QUANTITATIVE_80_PLUS` (goal, not achieved fact)
- NEXT_GAME: `NOT_AUTHORIZED` (separate Main Game Gate required)
- MEMORY: `NOT_IMPLEMENTED`
- PLANNING: `rolling-planning IMPLEMENTED; SCORE_BENEFIT NOT_PROVEN`
- Current milestone: S05 的 `candidate-v2-final-offline` 已由 Main 接受，S05 acceptance 为 `PASS_WITH_KNOWN_LIMITATION`。S06 Run #1 的 Main-reviewed 单局结果为 quantitative 53.83、competition partial 37.68、48 months、grade C；它只提供长程策略控制缺陷线索，不证明因果或稳定表现。Main 已接受 S06-01 的 `candidate-v3-adaptive-controller-static` 为静态候选；gameplay effectiveness 与 stable 80+ 仍 `NOT_PROVEN`。S06-02 正核对当前机器身份并准备精确 submission；下一局仍须独立 Main Game Gate 授权。Memory 未实现、第五 Skill 未增加、Team/Swarm 仍 deferred。S03 forensic hold 已解除，raw retained、cleanup 未授权。
- Production/published version: none
- Last verified: 2026-09-24 (S06-01 Main static acceptance reconciled; no gameplay validation)

## Major capabilities

- 私有开发仓库已建立，长期工程事实已集中到 `docs/project/`。
- 已保留官方 Source Lock 与当前有效架构决定；根目录已移除启动资料堆积。
- 项目隔离环境已用 CPython 3.12.13 和官方冻结 `uv.lock` 建立；关键依赖版本与基础 import 已验证，详见 [ENVIRONMENT.md](ENVIRONMENT.md)。
- 冻结官方 Runner `f61c738c72e51b77298cc1c14c7c6ebf4b6c527d` 已纳入仓库，并完成 source manifest 核对。
- `baselines/s01-minimal` no-op harness 已通过 submission/preflight validation；完成 1 局 fresh Dev baseline，证据见 [S01-03 RESULT](../../experiments/S01-03-baseline/RESULT.md)。
- `skills/career-action-trace/SKILL.md` 已完成最小 Skill contract、安装/发现/加载与 bounded smoke 应用闭环，证据见 [S02-01 RESULT](../../experiments/S02-01-minimal-skill/RESULT.md)。
- `skills/risk-review/SKILL.md` 已完成事件驱动的最小 Risk Review contract；Runner validation、install、discover、load 均有证据。S03-02 smoke 当时未建立游戏会话；Main 已接受 S03-14 一次 qualifying public trigger 上的 runtime correctness 证据，并确认该次运行的唯一 successful action submitter 为 Single Agent。Risk effectiveness 仍 `NOT_PROVEN`，证据见 [S03-14 RESULT](../../experiments/S03-14-risk-correctness-live-smoke/RESULT.md)。
- S04 已实现 `structured-state-board` 与 `rolling-planning` 并将其纳入 Candidate v1 的两次真实运行。Board 轨迹出现当前 game session、observed/inferred/unknown 与 freshness 字段，但 post-action refresh 仍不完整；Stage 接受其 partial runtime evidence，不代表独立 score benefit。Rolling Planning 有实际 checkpoint 证据，也不证明独立收益。Main 接受记录见 [S04-CLOSEOUT RESULT](../../experiments/S04-CLOSEOUT/RESULT.md)。
- S05 最终离线候选 `candidate-v2-final-offline` 已由 Main 接受；四个 Skill 的冻结身份与限制见 [S05-03 manifest](../../experiments/S05-03-final-optimization-reserve-audit/candidate_manifest.json)。S06-01 的 `candidate-v3-adaptive-controller-static` 已由 Main 接受为静态候选，但未经 gameplay 验证；S06 Run #1 仍是单局证据，不建立因果或稳定性结论。Memory、第五 Skill 与 Team / Swarm 仍未实现/授权。

## Current technical shape

- Windows / PowerShell 开发目标；项目根目录使用被 `.gitignore` 排除的 `.venv`，依赖由官方 `pyproject.toml`/`uv.lock` 管理。
- 官方上游仓库、候选 repo SHA、包版本和运行合同见 [OFFICIAL_SOURCE_LOCK.md](OFFICIAL_SOURCE_LOCK.md)。
- 本地 Runner 使用 `career_emu` named instance、career-emulator MCP 和 Dev 数据；重启后 preflight 已复验。
- Single Agent + Multiple Skills 是当前路线；当前 project-owned Skills 为 `career-action-trace`、`risk-review`、`structured-state-board` 与 `rolling-planning`。S03-14 证明一次 observed Risk runtime path 中 Single Agent 是唯一 successful submitter。S04 两次 Candidate run 也保持 Single Agent action authority。Memory 仍未实现；State Board runtime evidence partial；Risk / Board / Planning 的独立策略收益与 controlled-screening 仍未证明。

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
- S03-13 复用 S03-12 provider freshness 与 MCP 注册先前 PASS；本任务确认 provider config/env identity 未漂移，但重复本地 PowerShell 聚合表达式解析问题达到 Plan STOP 条件，未启动 service/play、未请求 provider，也未建立游戏。Risk correctness 仍未验证。
- S03-14 复用 S03-12 provider freshness，确认与 S03-13 的 provider/MCP identity 一致；一次 clean service startup 注册五个 CareerSim tools。唯一 Runner play 建立 1 个 game，完成 36 次 observe 与 35 次成功 take_action；公开违纪风险触发后，risk-review 经 Skill runtime 加载并在 action note 中输出唯一 ALLOW marker，S02 marker 与单 Agent action integrity 保持。Main 接受该次 runtime correctness 作为 Stage evidence；Runner 在第 9 月达到 180 秒上限、play_exit_code=1、无 final score，因此 Risk effectiveness 仍 `NOT_PROVEN`，无 performance / generalization 结论。
- S04 Main acceptance 接受 State Board partial runtime evidence 与 Rolling Planning 的实现/真实 Candidate load，限制于 Candidate v1 高方差和未证明的独立收益。Candidate Run #1 为 `76.04 / 53.23 / 48m / A`；Run #2 为 `35.31 / 24.72 / 25m / D`。S05-01 已离线实现下一假设 `H_MATERIAL_OUTCOME_REPRIORITIZATION`，但未做 gameplay；full game 仍是昂贵 benchmark，下一局需单独 Main Game Gate。
- S03-12 provider freshness gate 完成 1 次（37 tokens）；唯一 clean service start 中 AgentServer 注册 CareerSim MCP 五工具通过，并有 1 条 incidental startup prewarm usage（201 tokens）。服务已停止；pre-game correction guard 超限，Runner play、install、gameplay 和工具调用均为 0。Risk correctness 未验证，Risk effectiveness 仍 `NOT_PROVEN`。
- Windows 无 symlink 特权时，锁定 distribution 数据采用逐文件 hash 核对后的 copy materialization；未使用 GitHub 数据，后续对局仍须保持串行。

## Active work

- S05 的 S05-02/S05-03 离线成果及 `candidate-v2-final-offline` 已被 Main 接受并合入。S06-01 的 `candidate-v3-adaptive-controller-static` 已获 Main 静态接受并合入；S06-02 正进行本机运行身份与静态 submission 准备，不含 live run。S06 Run #1 不证明因果或稳定表现；后续对局仍需独立 Main Game Gate。S03 历史失败记录保留；forensic hold 已解除，raw retained、cleanup 未授权。

## Next likely tasks

1. Main 审查 S06-02 runtime identity/preflight 证据，并单独决定是否授权 v3 Game Gate。S06 Run #1 与 v3 静态实现均不证明策略收益或 stable 80+。Memory 未实现、第五 Skill 未增加、Team/Swarm 仍 deferred；本任务不执行 benchmark/optimization。

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
