# CURRENT_STATE

> 当前项目真实快照；不追加过程日志。历史由 Git 保存。

## Current

- App/product version: CareerSim BDCI26；无产品发布版本
- Branch: `main`
- Lifecycle stage: `Discovery`
- Current milestone: S01-01 私有开发仓库初始化与目录整理
- Production/published version: none
- Last verified: 2026-09-22

## Major capabilities

- 私有开发仓库已建立，长期工程事实已集中到 `docs/project/`。
- 已保留官方 Source Lock 与当前有效架构决定；根目录已移除启动资料堆积。
- 官方运行环境、Runner、模型调用、最小 submission 和 baseline 尚未验证。

## Current technical shape

- Windows / PowerShell 开发目标；当前没有项目运行时代码、已安装依赖或专用测试命令。
- 官方上游仓库、候选 repo SHA、包版本和运行合同见 [OFFICIAL_SOURCE_LOCK.md](OFFICIAL_SOURCE_LOCK.md)。
- Single Agent + Multiple Skills 是当前起步路线；相关 Skill 仍未实现。

## Known limitations / risks

- Python、OS build、uv、依赖解析、provider endpoint 和模型别名映射仍待实际核验。
- 没有有效 baseline 分数、策略收益或隐藏 Test 泛化证据。
- 共享 runtime 的隔离能力尚未验证；未来对局必须保持串行，直到有相反证据。

## Active work

- S01-01 已完成；当前无正在进行的代码或实验工作。

## Next likely tasks

1. 在独立环境中核验官方 repo checkout、Python / uv、锁定依赖和运行记录。
2. 使用经核验的官方 Runner 完成最小闭环与 baseline 证据。
3. baseline 建立后，再按最小 Skill Contract 开始自有 Skill 设计。

## Workflow / delivery facts that are currently material

- 主分支为 `main`，GitHub 远端为私有仓库；初始提交代表仓库初始化。
- secrets、runtime cache、日志、数据库和本机生成状态由 `.gitignore` 排除，不作为工程事实提交。
- 后续任务按 `AGENTS.md` 的主分支、证据、共享 runtime 串行和 Skill 时机规则执行。

## Update rule

仅在当前能力、阶段、限制、Active work 或交付事实发生 material change 时更新；不得把命令流水、临时失败或未来计划写成历史日志。
