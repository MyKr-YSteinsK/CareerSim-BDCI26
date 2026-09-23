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

## Codex 模型路由

每份最终交给 Codex 的 Plan 都必须比较以下四档：

- `GPT-6 Luna Max`
- `GPT-6 Sol High`
- `GPT-6 Astra Medium`
- `GPT-6 Astra XHigh`

默认不推荐 `Sol Max` 或 `Astra Max`。模型选择至少考虑 Plan clarity、delegated decision 的数量与重要性、investigation / debugging 深度、module span、context size、hidden constraints、regression risk、test / experiment duration 与返工成本。**不得仅因文件数量多就升级模型。**

默认路由倾向：

- **Luna Max**：Plan 清晰、主要是执行、重要 delegated decision 很少，或优先节省额度时，作为默认推荐。
- **Sol High**：正式开发的常规档；Plan 明确，且需要正常的 repository investigation、debugging 和 engineering judgment。
- **Astra Medium**：存在重要自主判断，且任务重要性、时间压力、返工成本或提高一次成功率的价值足以支持更高推理投入。
- **Astra XHigh**：关键 root cause 未知、架构关系未知、多模块关系复杂，或需要深度 investigation 与大量自主决策。

## Wall-clock 时间估算

对四档模型分别给出完整 wall-clock 区间，范围从：

`Plan handoff → investigation → implementation → tests / verification → necessary fixes → Git checks → TASK_RESULT`

估算必须计入适用的不可压缩时间，包括下载、build、test、experiment、provider、CareerSim 与其他 runtime。用区间表达，例如 `20–35 min`，并注明时间估算可信度和主要不确定来源。

可按以下关系估算：

`Total Time ≈ model reasoning / operation time + incompressible build/test/experiment/runtime time`

不得假定更强推理模型总是更快。它可能减少错误路径与返工，也可能增加单次推理时间。

## Relative quota pressure

在没有更新且可靠的官方 Codex usage 数据前，使用以下临时相对 compute / quota pressure proxy：

| Model | Relative quota pressure |
| --- | ---: |
| GPT-6 Luna Max | `≈1×` |
| GPT-6 Sol High | `≈4–7×` |
| GPT-6 Astra Medium | `≈15–25×` |
| GPT-6 Astra XHigh | `≈25–40×` |

这些数值表示相对计算 / 额度压力，**不是实际收费倍率**。未来获得新的可靠官方 usage 信息后，普通 Plan 或 Task 不得静默修改本合同；是否更新由 Main Hub / governance review 决定。

## Required Final Plan Appendix

每份最终 Codex Plan 都必须在正文后附以下二级标题，并在其下填写比较表与要求字段：

`## Codex Execution Recommendation｜Codex 执行建议`

比较表必须列全四档模型，并按当前 Plan 填入具体估时、返工风险与适合度：

| 模型 | 预计总耗时 | 相对额度压力 | 返工风险 | 适合度 |
| --- | --- | --- | --- | --- |
| GPT-6 Luna Max | 区间 | `≈1×` | 低 / 中 / 高，并简述依据 | 简述 |
| GPT-6 Sol High | 区间 | `≈4–7×` | 低 / 中 / 高，并简述依据 | 简述 |
| GPT-6 Astra Medium | 区间 | `≈15–25×` | 低 / 中 / 高，并简述依据 | 简述 |
| GPT-6 Astra XHigh | 区间 | `≈25–40×` | 低 / 中 / 高，并简述依据 | 简述 |

表后必须给出：

- **默认推荐：** 选择一档并简述原因；
- **如果最赶时间：** 选择一档，或说明并列推荐的理由；
- **如果最缺额度：** 选择一档；
- **如果最重视一次成功率：** 在该权衡有意义时给出选择。

还必须注明：

- **本 Plan 的 Codex 自主决策程度：** 低 / 中 / 高；
- 自主决策程度为中或高时，列出最重要的 `DELEGATED_TO_CODEX` 决策；
- **时间估计可信度：** 高 / 中 / 低，并简述主要不确定来源。

估时和路由推荐必须对应本 Plan 的证据、风险与 runtime，不得只套用通用排名。

## Stage 继承与指令一致性

所有未来新 Stage 的启动 Prompt 都必须继承本合同，无需全文重复，但须明确包含类似以下规则：

> 本 Stage 的所有 Codex Plan 遵循 Project Codex Plan Authoring Contract：`docs/project/CODEX_PLAN_CONTRACT.md`。

如果 Project Instructions 也包含同一合同，仓库文件是工程可审计版本，Project Instructions 是 Planner 对话侧约束；两者必须保持一致，不得有意设置冲突规则。
