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
- RISK_BENEFIT: `NOT_PROVEN`
- Current milestone: S03-02 已完成最小 Risk Review Skill 的实现、静态验证、安装/发现/加载验证；唯一 bounded smoke 未进入 CareerSim 游戏工具链，已在技术边界停止，等待 S03 Stage review
- Production/published version: none
- Last verified: 2026-09-22

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
- Windows 无 symlink 特权时，锁定 distribution 数据采用逐文件 hash 核对后的 copy materialization；未使用 GitHub 数据，后续对局仍须保持串行。

## Active work

- S02 已由 Main Hub 正式验收为 `COMPLETE` / `S02_STAGE_ACCEPTANCE = PASS`；S03-01 已通过 Stage review；S03-02 在技术失败边界停止，S03 尚未完成。

## Next likely tasks

1. 返回 S03 Stage review，审阅 S03-02 `BLOCKED_TECHNICAL` 并决定后续是否授权新的受控动作；本任务不自行重跑 smoke 或开始下一任务。
2. 继续保持 serving version `PARTIALLY_VERIFIED`、baseline 单局无策略结论、Risk benefit `NOT_PROVEN` 与 shared runtime 串行约束。

## Workflow / delivery facts that are currently material

- 主分支为 `main`，GitHub 远端为私有仓库；初始提交代表仓库初始化。
- secrets、runtime cache、日志、数据库和本机生成状态由 `.gitignore` 排除，不作为工程事实提交。
- S01-02 使用官方 SHA 对应的 `pyproject.toml`/`uv.lock`，以 `uv sync --locked --no-install-project` 安装；未修改冻结 lock。
- S01-03 仅运行 1 局 fresh baseline；score report、transcript、events 和重启验证路径已记录在实验证据中，未提交 `.env` 或 instance env。
- S02-01 仅运行 1 次 fresh bounded smoke；未开发 Memory / Planning / Team / Swarm，也未增加第二 action submitter。
- S03-01 为离线一次性取证；未启动新的 CareerSim、未调用 provider、未创建 `experiment-manager`，未实现 Risk / Memory / Planning / Team / Swarm。
- S03-02 仅运行 1 次 fresh bounded smoke（hard cap `120 s`）；技术失败后未重跑，未创建 `experiment-manager`，未运行对照 screening；Risk benefit 仍 `NOT_PROVEN`。
- 后续任务按 `AGENTS.md` 的主分支、证据、共享 runtime 串行和 Skill 时机规则执行。

## Update rule

仅在当前能力、阶段、限制、Active work 或交付事实发生 material change 时更新；不得把命令流水、临时失败或未来计划写成历史日志。
