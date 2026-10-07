# 14｜从 CareerSim 迁移到真实 Agent 工程的方法论

CareerSim 的分数和事件不能直接推广到其他系统，但它暴露的工程问题很常见：策略与执行混在一起、状态过期、工具回执被当成业务完成、模型恢复没有证据，以及失败结果被隐藏。

**INTERPRETATION｜解释：** 本章提出本项目支持、可合理迁移的设计原则。它们不是跨项目已测量规律，也不是 universally optimal（普遍最优）方案。每条都从真实证据出发，再说明迁移含义与边界。

## 1. Separate policy from execution：策略与执行分开

**FACT｜CareerSim 证据：** Planning 产生候选，Risk 审查，Single Agent 唯一提交；运行合同保护 fresh session 和动作顺序。[运行合同](../../project/AGENT_RUNTIME_CONTRACT.md)

**INTERPRETATION｜迁移：** 在客服、办公或代码 Agent 中，模型建议与实际写入应有明确接缝。执行层核对身份、参数、授权和最新状态，便于知道错误来自策略还是调用。

如果不分开，模型文本可能被直接当成已执行事实。边界清楚也不保证策略正确，只让调用和结果可解释。对简单只读任务，无需机械增加复杂执行框架。

## 2. Separate state from planning：事实与计划分开

**FACT｜CareerSim 证据：** Board 负责本局公开事实，Planning 独占策略；v7m 取证建议直接复制 fresh public state，交付事实必须有实际结果支持。[架构复盘](../../project/ARCHITECTURE_RETROSPECTIVE.md) · [v7m 取证](../../project/reviews/S07-47_V7M_M20_PARTIAL_RUN_FORENSIC_REVIEW.md)

**INTERPRETATION｜迁移：** 让系统区分“订单当前状态”“我准备怎么处理”“我认为客户可能接受”。事实来自有身份的回执，计划可以更新但不覆盖事实。

如果模型把推测写进事实板，后续判断会围绕假事实积累。结构化存储能帮助检查字段，却不能自动验证语义；Controller 的语义注释限制就是反例。

## 3. Separate planning from risk：规划与风险检查分开

**FACT｜CareerSim 证据：** exact-v6 限定 Risk 检查已生成候选，避免无边界重开策略；原样本仍有 ordinary Story 重新权衡缺陷。[S06 收口](../../project/S06_CLOSEOUT.md)

**INTERPRETATION｜迁移：** 风险检查可以定位一个具体建议是否越权或有直接危险，而不是每次重新创造所有方案。这样便于发现“同一输入反复循环”。

高风险应用可能需要不同强度的独立评审；这里没有证明单次 gate 对所有场景足够。Reviewer 的部署权限前提提醒我们，独立意见也要有真实权限边界。

## 4. Track runtime identity：追踪实际运行身份

**FACT｜CareerSim 证据：** v7i stale score 可能从旧文本 session 产生；current checkout 为 v8a，而最终 ZIP 为 exact-v6。[Provider 取证](../../project/reviews/S07-39_PROVIDER_CONNECTIVITY_FORENSICS.md) · [最终方案审阅](../../project/FINAL_SOLUTION_REVIEW.md)

**INTERPRETATION｜迁移：** 一个任务应绑定模型/配置/工具版本、输入对象、执行实例和输出。最新代码目录不能代替生产已加载版本，文件名不能代替交易或会话身份。

在自动化系统中，这可以帮助避免把旧任务结果误交给当前用户。但记录更多 hash 不等于证明实际加载；需要针对实际执行链的观察。

## 5. Tool success 与 state observation 分开

**FACT｜CareerSim 证据：** take_action 的 success/error 回执不含新状态，S08-09 的 18 个缺 observe 边界是真违规。[运行合同取证](../../project/reviews/S08-09_RUNTIME_CONTRACT_ADHERENCE_FORENSICS.md)

**INTERPRETATION｜迁移：** API 返回“请求成功”可能只说明已接收或执行完成。业务新状态需要另一次读回、版本号或具有明确语义的返回字段。

例如编辑请求成功，不一定表示后续页面显示的是最新内容。是否必须额外读取，取决于接口合同；有些 API 本身返回完整最终状态，不应机械套用 CareerSim 的观察次数。

## 6. Instrument adherence：让遵循可观察

**FACT｜CareerSim 证据：** v6 高分同时 adherence FAIL；CTRL 出现次数不能可靠绑定动作；v8a parser 接受率也不能自动证明语义应用。[v6 记录](../../project/runs/v6-run1-validation.md) · [v8a 样本一](../../project/runs/v8a-full-horizon-sample1.md)

**INTERPRETATION｜迁移：** Instrumentation（可观测记录）应追踪实际调用、来源、顺序和恢复事件。只记录模型说“已完成检查”不够。

机器可解析标记有用，但标记设计、事件去重和语义审计要对应。否则记录越多，可能只是重复文本越多。记录还必须遵守 secret protection（秘密保护）与最小必要范围。

## 7. Recovery 是独立合同

**FACT｜CareerSim 证据：** v6 两次压缩之后未重读 Skill；Memory 的显式读取成功却未满足指定自动锚点门禁。[v6 记录](../../project/runs/v6-run1-validation.md) · [Memory 研究](../../project/research/S10-19R2_MEMORY_FEASIBILITY.md)

**INTERPRETATION｜迁移：** 长程任务、重启或上下文压缩之后，要知道什么事实和权限必须恢复，恢复来源在哪里，以及怎样证明读取了最新内容。

“文件还在”不能证明模型看见，“摘要还在”不能证明来源完整。不同系统可以用状态服务、显式读回或验证后的上下文组装实现，不能从本项目推出只有一种恢复方法。

## 8. Preserve negative evidence：保留负证据

**FACT｜CareerSim 证据：** v1 / v8a pair、v7m 技术部分局和 S10 停止路线都进入 canonical 记录。[实验复盘](../../project/EXPERIMENT_RETROSPECTIVE.md)

**INTERPRETATION｜迁移：** 保留低结果、未测试与门禁失败，帮助下一位开发者知道哪些判断已被检查、哪些仍没有证据。只保存成功展示会导致重复踩坑和样本选择偏差。

保留知识不意味着永久留存每份临时日志。敏感材料、hold 和复验依赖应单独管理；不可把“报告完成”当成删除原始来源许可。

## 9. Use explicit experiment boundaries：把实验边界写出来

**FACT｜CareerSim 证据：** Plan 区分 FROZEN、RECOMMENDED、DELEGATED_TO_CODEX；Simulator 在冻结门禁失败后停止，未继续挑宏配置。[Plan 合同](../../project/CODEX_PLAN_CONTRACT.md) · [Simulator 研究](../../project/research/S10-22_SIMULATOR_POLICY_SEARCH.md)

**INTERPRETATION｜迁移：** 在改变模型、工具或流程之前，写明对象、允许干预、判定证据和停止条件。实现空间可以委托，实验身份和权限边界不能静默漂移。

这有助于避免结果出现后换指标。但边界过细也可能冻结低置信度实现猜测，所以要让执行者检查实际接口。

## 10. Do not infer causal gain from one run：单次不推因果

**FACT｜CareerSim 证据：** exact-v6 单样本 75.29，v1 pair 76.04/35.31，v8a pair 72.65/59.00；没有稳定分布或最优证明。[最终证据审查](../../project/FINAL_EVIDENCE_REVIEW.md)

**INTERPRETATION｜迁移：** 一个 Agent 成功完成一次任务，首先说明该输入和条件下发生了成功。比较新旧版本需要控制相关因素，保留失败并说明样本范围。

某些确定性修复可通过局部合同检查获得强证据，例如非法输入被拒绝；这仍不同于整体业务收益。不要因一次成功演示就宣称总体成功率。

## 11. Stop complexity when evidence is weak：证据弱时停止扩复杂度

**FACT｜CareerSim 证据：** Reviewer / Memory 部署门禁未通过；Helper 工具层支持没有自动转成正式 Candidate；Controller 信号弱，不创建 v15；最终冻回 exact-v6。[实验复盘](../../project/EXPERIMENT_RETROSPECTIVE.md)

**INTERPRETATION｜迁移：** 新工具和新 Agent 应有可以检查的收益假设。如果只增加状态、权限和协调成本，却没有修正关键错误的证据，停止是合理研究决策。

停止一个测试路径，不应宣布机制普遍无价值。未来有新的安全加载方式、更好的输入或明确机制信号时，可以在新授权下重开。

## 12. Current tree 小于 historical record：当前树不必容纳全部历史

**FACT｜CareerSim 证据：** S11 进入知识迁移、canonical 汇总与有边界仓库收敛；当前 hold 台账仍有 20 个 named active/pending，0 releasable。[当前状态](../../project/CURRENT_STATE.md) · [证据审查](../../project/FINAL_EVIDENCE_REVIEW.md)

**INTERPRETATION｜迁移：** 历史 Git 可以保存过程，当前工程树优先保留运行、权威知识、教学和必要复现资产。知识已迁移、引用已修复、依赖已解除的过程文件可以进入后续资格审查。

Git history 不一定保存 local raw、shared DB 或未提交来源，所以不能用历史存在来解除 hold。本轮只讲方法，不执行删除、迁移或解除。

## 如何把原则落实到一次真实改动

**INTERPRETATION｜解释：** 不必同时建立十二个框架。先从实际 failure mode 开始，找到一个会改变当前决策的缺口。若输出被归给旧任务，优先查身份；若操作成功但事实过期，优先查回执语义和读回；若新模块存在却没有应用证据，优先查加载与输入接缝。

然后为这个问题选择最小有区分力的验证。结构问题可用静态检查，实际注册需要对应路径证据，长程行为需要有界运行记录。不要为了让报告显得完整，增加不相关测试或未经授权外部调用。

**FACT｜事实：** 项目 Plan 合同要求 Hard Gate 与安全、身份、shared-state 或必要接口相关，Advisory Check 默认不应升级为阻断；执行自主性不授权扩大范围。[Plan 合同](../../project/CODEX_PLAN_CONTRACT.md)

这意味着效率和纪律可以一起存在。复用身份未漂移的稳定证据，把新检查对准新问题；若出现关键污染或 unknown side effect，则按授权观察核对，不能盲重发操作。

## 一个迁移原则怎样失效

**TEACHING EXAMPLE｜教学示例：** 团队学到“动作后 observe”，于是给所有 API 操作增加读回。若某接口本来已返回带版本号的最终完整状态，额外读取可能只是成本；若它只返回排队 receipt，读回才在回答业务完成。

这个例子说明原则要连接实际合同，不能把 CareerSim 工具形式当成普遍实现。真正可迁移的是“区分执行成功与业务状态证据”，而不是固定调用次数。

另一个例子是“多 Skill 明确职责”。简单短任务可能只有一个清楚职责，不需要额外拆分。长程混合职责出现漂移时，拆分才有可检查理由；新增模块仍须验证实际应用和协调负担。

## 怎样维护一个可学习的项目

**INTERPRETATION｜解释：** 保留原始身份、有限案例、负结果与非结论，可以让下一位研发者快速理解问题。如果知识只存在聊天记录里，重启项目就会重复调查；如果当前树保留全部过程物，又会淹没核心来源。

CareerSim 的 S11 教学把运行事实、工程工具和研究方法分成不同主线。读者先从权威状态找到当前对象，再根据问题进入具体案例。教程是解释层，不能替代工程事实层；未来源码或身份变化时，解释必须以事实为准。

## 用迁移问题检查自己

**TEACHING EXAMPLE｜教学示例：** 你要评估一个自动报销 Agent。它说“提交成功”。依次问：哪个版本？哪个申请？提交工具返回的是 receipt 还是最终审批状态？有没有读回？失败怎样分类？新规则有没有只在一张熟悉单据上验证？凭这些问题，你可以使用 CareerSim 的证据思路，而不复制它的游戏规则。

这条学习线最终留下的能力，是在不确定中准确说话和行动：事实定位对象，假设等待验证，实验有边界，决策保留未知，实现不扩大授权。项目没有给出所有 Agent 的最优答案，但提供了一套可以审查、可以停止、可以复核的研发经验。

---

[学习地图](00-学习地图.md) | [上一章](13-Main、Stage、Plan与Codex为什么这样协作.md)
