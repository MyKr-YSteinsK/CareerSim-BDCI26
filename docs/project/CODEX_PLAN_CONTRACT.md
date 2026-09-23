# Codex Plan 编写合同

## 目的与依据

本合同适用于 Main Hub 或 Stage Planner 交给 Codex Task 执行的 Plan。Plan 应冻结目标、已确认事实、约束、权限、验收条件和所需证据；不得把 Planner 对实现方式的低置信度猜测写成工程合同。

Plan 应以最新仓库状态、适用的 `AGENTS.md`、项目长期合同和任务证据为依据，并明确区分 `FACT`、`INFERENCE`、`HYPOTHESIS` 与 `UNKNOWN`。如果某项关键实现细节只能通过实际检查仓库、源码、日志或 runtime 才能判断，应明确交由 Codex 调查。

Task Plan 可以收紧项目要求，但不得放宽本合同的 FROZEN 或 governance 边界。如果 FROZEN 要求与最新仓库事实或更高层项目规则冲突，Codex 应停止受影响的部分并回传证据与冲突，不得静默绕过。

## Plan 决策分级

### FROZEN

使用 `FROZEN` 标记必须遵守的任务合同，至少覆盖：

- Goal 与 Scope；
- Source of Truth 与 confirmed facts；
- 禁止区域及受保护文件、数据；
- compatibility、governance 与 safety constraints；
- 必须保留的行为；
- acceptance criteria 与 required verification / tests；
- evidence 与 delivery requirements；
- permissions、live-run / retry boundaries 与 stop conditions。

Codex 不得自行突破 FROZEN。若实际仓库证据与 FROZEN 前提冲突，应停止受影响的工作并回传证据，再决定是否继续。

### RECOMMENDED

使用 `RECOMMENDED` 表示有证据支持、但不是硬性工程合同的建议，例如 likely files、confirmed interfaces、高置信度实现路径、已验证过的技术方法或推荐的验证顺序。

Codex 可以根据最新仓库事实调整 RECOMMENDED，但必须保留所有 FROZEN 要求，并在 TASK_RESULT 说明：

1. 原建议为何不适用于当前事实；
2. 实际采用了什么方案；
3. 如何验证没有突破 FROZEN。

### DELEGATED_TO_CODEX

当 Planner 缺少足够证据、应由执行中的 Codex 自行调查决策时，必须使用明确标记：

`Decision: DELEGATED_TO_CODEX`

典型事项包括：未确认的 bug root cause、最合适的 patch location、内部架构选择、多种实现方案权衡、不熟悉的 SDK / framework 行为、复杂兼容性或依赖策略，以及必须检查真实仓库或 runtime 才能判断的细节。

每项重要 delegated decision 都必须写清：

- **Investigation Question**：要回答的具体问题；
- **Available Evidence**：已有证据、来源及重要缺口；
- **FROZEN Constraints**：调查期间仍必须遵守的边界；
- **Decision Criteria**：依据哪些事实或权衡作决定；
- **Required Verification**：决策与实现需要通过什么验证。

影响实现的关键 delegated decision 必须按以下顺序处理：

`Evidence → Investigation → Decision → Implementation → Verification`

不得要求 Codex 机械执行未经证实的 Planner 猜测。Codex 可以在 Plan 的既定 Scope 内解决 delegated decision；若证据显示解决方案需要扩大 Scope、权限或突破 FROZEN，则停止并回传冲突。

## 证据纪律与反过度设计

Plan 不得：

- 在 root cause 未确认前写死具体 patch；
- 在 framework 行为未知时编造接口或行为；
- 仅因 Planner 偏好某方案，就把它升级为 `MUST`；
- 为了让 Plan 看似完整而加入低置信度实现步骤；
- 把可能、推测或候选写成 confirmed fact；
- 用大量 implementation detail 掩盖 evidence 不足；
- 以允许 Codex 自主判断为由扩大任务 Scope。

**Codex autonomy applies to implementation decisions, not scope expansion.** Plan 应在证据支持的范围内提供细节：冻结目标和边界、推荐有依据的实现方向、将未决事项明确委托调查。

## Plan Artifact Boundary

最终直接交给 Codex 的 Plan artifact 只应包含完成任务所需的工程信息。Planner-side 的执行模型选择、模型比较、额度分析、模型耗时比较及选择模型的理由属于 Planner 对用户的建议，不得写入 Codex Plan artifact。Codex execution model selection and quota/time comparison are Planner-side user guidance and are intentionally outside this repository contract and outside the Codex Plan artifact；相关 Planner 规则由 ChatGPT Project Instructions 管理，本合同不定义模型清单、额度、耗时或模型选择方式。

Plan 仍须保留必要的 `Decision: DELEGATED_TO_CODEX`，明确由 Codex 调查的技术问题、判断边界、Decision Criteria 与 Required Verification。

## TASK_RESULT 执行指标

Codex 的 `TASK_RESULT` 应尽量包含以下执行指标，供 Planner 后续校准时间预测；这些指标是执行记录，不替代任务验收。

### EXECUTION_METRICS｜执行指标

- Model Used: `<value / UNKNOWN>`
- Reasoning Effort: `<value / UNKNOWN>`
- Started At: `<timestamp / UNKNOWN>`
- Finished At: `<timestamp / UNKNOWN>`
- Actual Wall-clock: `<duration / UNKNOWN>`

填写规则：

1. 只填写能从当前任务上下文或可靠执行记录中确认的真实值。
2. 无法可靠读取 `Model Used` 或 `Reasoning Effort` 时填写 `UNKNOWN`，不得推测。
3. `Started At`、`Finished At` 与 `Actual Wall-clock` 应尽量依据任务执行时的真实时间记录，不应事后估算补写。
4. 指标缺失或部分为 `UNKNOWN` 不影响任务本身验收。
5. 这些指标仅供 Planner 后续校准，不参与功能正确性判定。

## Stage 继承与指令一致性

所有未来新 Stage 的启动 Prompt 都必须继承本 Codex-facing Plan Authoring Contract，无需全文重复，但须明确包含类似以下规则：

> 本 Stage 的所有 Codex Plan 遵循 Project Codex Plan Authoring Contract：`docs/project/CODEX_PLAN_CONTRACT.md`。

Stage 继承的内容包括 Plan 决策分级、证据纪律、Scope、验证与停止条件；Planner-side 的模型、额度和时间建议由 Project Instructions 管理，不属于仓库合同。
