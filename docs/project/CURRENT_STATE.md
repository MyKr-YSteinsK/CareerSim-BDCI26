# CURRENT_STATE

> 当前项目真实快照；不追加过程日志。历史由 Git 保存。

## Current

- App/product version: CareerSim BDCI26；无产品发布版本
- Branch: `main`
- Lifecycle stage: `Discovery`
- Current milestone: S01-03 官方 Runner 与最小 baseline 闭环（已完成，待 S01 Stage review）
- Production/published version: none
- Last verified: 2026-09-22

## Major capabilities

- 私有开发仓库已建立，长期工程事实已集中到 `docs/project/`。
- 已保留官方 Source Lock 与当前有效架构决定；根目录已移除启动资料堆积。
- 项目隔离环境已用 CPython 3.12.13 和官方冻结 `uv.lock` 建立；关键依赖版本与基础 import 已验证，详见 [ENVIRONMENT.md](ENVIRONMENT.md)。
- 冻结官方 Runner `f61c738c72e51b77298cc1c14c7c6ebf4b6c527d` 已纳入仓库，并完成 source manifest 核对。
- `baselines/s01-minimal` no-op harness 已通过 submission/preflight validation；完成 1 局 fresh Dev baseline，证据见 [S01-03 RESULT](../../experiments/S01-03-baseline/RESULT.md)。

## Current technical shape

- Windows / PowerShell 开发目标；项目根目录使用被 `.gitignore` 排除的 `.venv`，依赖由官方 `pyproject.toml`/`uv.lock` 管理。
- 官方上游仓库、候选 repo SHA、包版本和运行合同见 [OFFICIAL_SOURCE_LOCK.md](OFFICIAL_SOURCE_LOCK.md)。
- 本地 Runner 使用 `career_emu` named instance、career-emulator MCP 和 Dev 数据；重启后 preflight 已复验。
- Single Agent + Multiple Skills 是当前起步路线；正式项目 Skill 仍未实现，当前 harness 仅为 no-op 基础设施载体。

## Known limitations / risks

- provider endpoint 已按用户配置使用 DeepSeek 官方 API；请求/usage model 为 `deepseek-flash`，底层 serving version 映射仍为 `PARTIALLY_VERIFIED`。
- 已有 1 个有效 Dev baseline，但为 no-op harness 且在第 19 个月提前结束；分数不构成策略收益或隐藏 Test 泛化证据。
- Windows 无 symlink 特权时，锁定 distribution 数据采用逐文件 hash 核对后的 copy materialization；未使用 GitHub 数据，后续对局仍须保持串行。

## Active work

- S01-03 已完成实现与验证；当前等待 S01 Stage review，不自行宣布 S01 完成。

## Next likely tasks

1. 返回 S01 Stage chat 审查 S01-03 证据。
2. Stage 审查通过后，再按最小 Skill Contract 开始自有 Skill 设计。

## Workflow / delivery facts that are currently material

- 主分支为 `main`，GitHub 远端为私有仓库；初始提交代表仓库初始化。
- secrets、runtime cache、日志、数据库和本机生成状态由 `.gitignore` 排除，不作为工程事实提交。
- S01-02 使用官方 SHA 对应的 `pyproject.toml`/`uv.lock`，以 `uv sync --locked --no-install-project` 安装；未修改冻结 lock。
- S01-03 仅运行 1 局 fresh baseline；score report、transcript、events 和重启验证路径已记录在实验证据中，未提交 `.env` 或 instance env。
- 后续任务按 `AGENTS.md` 的主分支、证据、共享 runtime 串行和 Skill 时机规则执行。

## Update rule

仅在当前能力、阶段、限制、Active work 或交付事实发生 material change 时更新；不得把命令流水、临时失败或未来计划写成历史日志。
