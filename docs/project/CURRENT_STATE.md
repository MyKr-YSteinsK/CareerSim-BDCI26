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
- S03-01: `COMPLETE_PENDING_STAGE_REVIEW`
- Current milestone: S03-01 已完成 S01 baseline failure forensics 与最小风险假设，等待 S03 Stage review
- Production/published version: none
- Last verified: 2026-09-22

## Major capabilities

- 私有开发仓库已建立，长期工程事实已集中到 `docs/project/`。
- 已保留官方 Source Lock 与当前有效架构决定；根目录已移除启动资料堆积。
- 项目隔离环境已用 CPython 3.12.13 和官方冻结 `uv.lock` 建立；关键依赖版本与基础 import 已验证，详见 [ENVIRONMENT.md](ENVIRONMENT.md)。
- 冻结官方 Runner `f61c738c72e51b77298cc1c14c7c6ebf4b6c527d` 已纳入仓库，并完成 source manifest 核对。
- `baselines/s01-minimal` no-op harness 已通过 submission/preflight validation；完成 1 局 fresh Dev baseline，证据见 [S01-03 RESULT](../../experiments/S01-03-baseline/RESULT.md)。
- `skills/career-action-trace/SKILL.md` 已完成最小 Skill contract、安装/发现/加载与 bounded smoke 应用闭环，证据见 [S02-01 RESULT](../../experiments/S02-01-minimal-skill/RESULT.md)。

## Current technical shape

- Windows / PowerShell 开发目标；项目根目录使用被 `.gitignore` 排除的 `.venv`，依赖由官方 `pyproject.toml`/`uv.lock` 管理。
- 官方上游仓库、候选 repo SHA、包版本和运行合同见 [OFFICIAL_SOURCE_LOCK.md](OFFICIAL_SOURCE_LOCK.md)。
- 本地 Runner 使用 `career_emu` named instance、career-emulator MCP 和 Dev 数据；重启后 preflight 已复验。
- Single Agent + Multiple Skills 是当前起步路线；当前仅有一个 project-owned 最小 trace Skill，尚无策略 Skill 或策略收益证据。
- S03-01 已基于冻结 S01 单局证据形成一个公开警告驱动的最小 Risk Hypothesis；尚未实现 Risk Skill 或运行对照实验。

## Known limitations / risks

- provider endpoint 已按用户配置使用 DeepSeek 官方 API；请求/usage model 为 `deepseek-flash`，底层 serving version 映射仍为 `PARTIALLY_VERIFIED`。
- 已有 1 个有效 Dev baseline，但为 no-op harness 且在第 19 个月提前结束；分数不构成策略收益或隐藏 Test 泛化证据。
- S02-01 bounded smoke 证明了 Skill 实际读取与 action trace marker 应用；不证明分数提升、策略收益或 Hidden Test 泛化。
- S03-01 只证明基线存在可观察的公开风险预警—埋雷反馈—信任危机终止链；不证明任何单个动作造成终止，也不证明 Risk Control 收益。
- Windows 无 symlink 特权时，锁定 distribution 数据采用逐文件 hash 核对后的 copy materialization；未使用 GitHub 数据，后续对局仍须保持串行。

## Active work

- S02 已由 Main Hub 正式验收为 `COMPLETE` / `S02_STAGE_ACCEPTANCE = PASS`；S03-01 已完成但等待 S03 Stage review，S03 尚未完成。

## Next likely tasks

1. 返回 S03 Stage review，决定是否允许进入 S03-02 Risk implementation；Codex 不自行开始实现。
2. 继续保持 serving version `PARTIALLY_VERIFIED`、baseline 单局无策略结论与 shared runtime 串行约束。

## Workflow / delivery facts that are currently material

- 主分支为 `main`，GitHub 远端为私有仓库；初始提交代表仓库初始化。
- secrets、runtime cache、日志、数据库和本机生成状态由 `.gitignore` 排除，不作为工程事实提交。
- S01-02 使用官方 SHA 对应的 `pyproject.toml`/`uv.lock`，以 `uv sync --locked --no-install-project` 安装；未修改冻结 lock。
- S01-03 仅运行 1 局 fresh baseline；score report、transcript、events 和重启验证路径已记录在实验证据中，未提交 `.env` 或 instance env。
- S02-01 仅运行 1 次 fresh bounded smoke；未开发 Memory / Planning / Risk / Team / Swarm，也未增加第二 action submitter。
- S03-01 为离线一次性取证；未启动新的 CareerSim、未调用 provider、未创建 `experiment-manager`，未实现 Risk / Memory / Planning / Team / Swarm。
- 后续任务按 `AGENTS.md` 的主分支、证据、共享 runtime 串行和 Skill 时机规则执行。

## Update rule

仅在当前能力、阶段、限制、Active work 或交付事实发生 material change 时更新；不得把命令流水、临时失败或未来计划写成历史日志。
