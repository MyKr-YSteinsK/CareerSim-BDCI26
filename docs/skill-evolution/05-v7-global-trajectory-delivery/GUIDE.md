# v7｜版本讲解

> **FACT｜事实** 依据[Instruction](instruction.md)、各 Skill、[SOURCE](SOURCE.md)与[DELTA](DELTA.md)；教学分析标为 **INTERPRETATION｜解释**，证据缺口为 **UNKNOWN｜未知**。基础概念见 [v3c GUIDE](../01-v3c-zh-aligned-policy/GUIDE.md)。

## 1. 这个版本处在什么位置

**FACT**：`candidate-v7-global-trajectory-delivery` 对应 S07-23，增加 `delivery-progress` 后共有四个 Skill。上一代表版本是 exact-v6，但配置 parent 为 v6c；这份代表档案有意跳过中间版本，不能把两目录当相邻提交。

它在七版本中首次展示独立 Delivery（交付进展）职责，并把职业全程、下一反馈窗口与当前动作连接起来。SOURCE 没有能归属此精确配置的运行结果，后继 v7 Candidate 的成绩不能挂在这里。

## 2. 这一版的核心结构

```text
fresh observe → Board
  → Delivery：相关新证据才更新，否则 QUICK no-op
  → Planning：连接长程目标、review 窗口与当前动作
  → 合法候选 → Risk gate → DECISION_CLOSED
  → Agent 在 notes 写 CTRL 并提交 → fresh observe
```

箭头是职责顺序／信息关系，不代表 Python 函数互调。Delivery 位于事实整理后、策略比较前，它管理 lifecycle（生命周期）证据，既不排序动作，也不是新的 Agent。no-op（不更新）表示没有相关新证据，不能解释成没有任何工作发生。

## 3. Instruction 怎么约束 Agent

九行可以分成六组：

| 原文组 | FACT｜约束 | INTERPRETATION｜长程意义 |
|---|---|---|
| 信息、权限与启动 | 本局公开证据、唯一提交者；首动作前四份 Skill；Memory 未实现，Team/Swarm 与第五 Skill 延后 | 模块增多不扩大提交权，也不自动产生持久记忆 |
| 每步顺序 | Board→相关 Delivery→Planning→候选→Risk→决策关闭→动作→新观察 | 先核实工作进展，再把它用于排序 |
| 三个 Horizon | Global 是剩余职业轨迹；Review 是下一公开反馈窗口；Action 是当前候选 | 当前收益应连到可兑现结果，Level 不是固定月份 KPI |
| Delivery 边界 | 申请≠承诺；承诺≠交付；声明≠验证；普通表扬不能绑定项目 | 活动多不代表已有可审的结果 |
| 反馈与 checkpoint | 实际 review/promotion/no-advance 后刷新、废弃旧进展基线；相关交付变化影响目标才 full checkpoint；双 checkpoint 才 STALLED | 既响应新结果，也避免每条进展都展开全套规划 |
| 动作格式与恢复 | 每次 Energy 一个整数；notes 首位一个 CTRL；有界重比与 DECISION_CLOSED；恢复时四份重读并从同局公开证据重建；禁固定配方 | 保持选择有界，旧意图或压缩快照不能当完成回执 |

`[CTRL G=... P=... R=... X=...]` 已进入 take_action.notes（动作说明），不再沿用 v6 的独立 B/CP 行。本版 R 记录本路径的门禁过程：一旦 RECONSIDER，完成相关替代比较后仍保留 `R=RECONSIDER, X=1`；若换候选仍要 gate，过程标记不改为 PASS。X=0 禁止提交，未触发则 X=-。`DECISION_CLOSED`（本次选择关闭）要求无新证据不重开，不是完成游戏的证明。

## 4. 每个 Skill 分别负责什么

### structured-state-board｜事实输入

[原文](skills/structured-state-board/SKILL.md)读取新观察、七项公开状态、反馈、警告和可比结果，输出当前事实／新鲜度与最多两条效果。Planning 拥有目标，Delivery 拥有工作项关系，Risk 拥有候选风险；Board 不代管这些状态、不提交。关键规则是：

- 每观察 quick scan，仅突出变化、相关和未知；完整快照在明确触发点替换。
- before/after（前后变化）有混杂即 UNKNOWN，不称为策略成功。
- `<state_snapshot>` 是恢复信号，不是策略权威；同 session 新观察优先，必要恢复最多五条日志、两条效果。

**反例**：从快照里的“打算申请项目”直接记成已承诺或已交付。

### delivery-progress｜公开交付生命周期

[原文](skills/delivery-progress/SKILL.md)读取 Board、新公开事件／回执、同局摘要与相关正式反馈，输出 `item | stage | owner/dependency | checkpoint | evidence_status | recognition_link`。它只管理“工作做到哪一步”，把摘要交给 Planning；不选 Gap、不排候选、不判 Material Risk、不提交。关键规则是：

- 机会、明确承诺、里程碑／阻塞、结果回执或相关 review 证据变化才更新。
- 完成陈述缺验证记 `DELIVERY_CLAIMED + UNVERIFIED`；公开回执直接验证结果才 `DELIVERED + PUBLICLY_VERIFIED`。
- 最多三条 active（活动项）和一条相关 recent closed（近期关闭项）；负责人、依赖、日期与 recognition 缺证据就 UNKNOWN。
- 一般表扬或晋升不能自动归因给某项目；恢复只从当前局公开证据重建。

**反例**：成功申请项目便记成交付，或为了补齐表格虚构 deadline（截止时间）和负责人。

### rolling-planning｜三种时间范围的策略

[原文](skills/rolling-planning/SKILL.md)读取 Board、Delivery、公开反馈、合法选项和 Handbook，维护一个 Gap、Progress、Risk Budget、三种 Horizon，输出最多六字段 checkpoint 与有界路径建议。它唯一拥有策略，不补造 Delivery 状态、不重做候选 Risk、不提交。关键规则是：

- Gap 是职业轨迹的主要瓶颈，不自动等于最低数值；每候选说明如何服务 review 与 global objective（长程目标）。
- 比较公开交付、复利、可兑现时间、可逆性、机会成本和依赖，不设隐藏权重。
- 相关 Delivery 新证据实质改变目标才完整规划；实际反馈后重建 baseline。
- 季度 Energy/Main 联合比较但逐动作新观察；终局前提高能兑现的路径价值，无新证据不重开。

**反例**：因为还有旧项目，永远不接新机会；或只追眼前加点，忽略结果是否来得及验证。

### risk-review｜当前候选重大风险

[原文](skills/risk-review/SKILL.md)读取候选、新鲜公开重大后果与预算；仅交付依赖直接涉及重大风险时读相关 Delivery。输出 PASS 或完整审查 ALLOW/WARN/RECONSIDER/UNKNOWN；不拥有一般交付策略、Gap 或预算，不提交。关键规则是：

- 缺交付、延期或没有回执本身不构成 Risk trigger（触发条件）。
- 只有明确候选相关重大后果或直接加重 TIGHT 约束才完整审查；不用故事类别答案库。
- RECONSIDER 比一个相关合法替代、换候选重 gate；过程 R 保持，X 记录比较是否完成。
- 最终 gate 后无新公开证据即关闭；UNKNOWN 最多一次刷新，否则有界决策。

**反例**：项目 UNVERIFIED 就认定危机，或完成 gate 后反复重算同一方案。

## 5. 相比上一代表版本改了什么

**FACT**：[DELTA](DELTA.md)记录 Instruction 改变；新增 delivery-progress，三个保留 Skill 全改文，未移除；三到四模块。原文新增三种 Horizon、交付证据 owner、notes 控制前缀和恢复重建四份规则。

**INTERPRETATION**：从文本结构与后续证据看，可以解释为补足“活动是否形成可验证结果”这一独立信息关系。它增加职责分离，也增加状态维护与协调成本；此 exact configuration 没有运行证据测量收益。

## 6. 一个具体决策流程怎么走

**教学性 hypothetical example（假设示例）：这是教学示例，不是该 Candidate 的真实 Run 记录。** 情境来自 Delivery 的结果验证规则与 Planning 的 review-objective 合同：公开工作项声称完成但尚无可核对结果，下一 review 可见；合法选择有验证现有结果或开启新机会。

1. Board 保存公开声明与当前窗口，不把声明升级成结果。
2. Delivery 写 `DELIVERY_CLAIMED + UNVERIFIED`，缺少明确关联的 recognition 保持 UNKNOWN。
3. Planning 比较两条路径怎样服务当前 Gap、兑现时间与剩余职业轨迹；不是必然选择验证，也不虚构新机会期限。
4. Risk 只审选定候选的重大公开后果；缺回执本身不触发 RECONSIDER。
5. Agent gate 完成后写一个 CTRL 并提交。后续有真正公开结果证据，Delivery 才改阶段。

结果是否获认可或促进晋升仍 UNKNOWN。

## 7. 真实运行证据

**FACT**：**No exact run identified（未识别精确版本运行）**。SOURCE 未列可归属 Run、分数或 canonical runtime review（权威运行审阅），不能认证完整／部分运行、技术失败、自然终局或遵循结果。后继四 Skill 的样本也不是此版本成绩。

## 8. 这个版本暴露出的限制

**FACT**：静态文本能确认职责、稀疏 trigger 与 bounded state（有界状态），不能确认实际生命周期维护质量；恢复不能用旧意图代替回执。

**INTERPRETATION**：长程、review、当前候选的多因素比较若被每步平铺，可能膨胀为清单；Delivery 与 Board、Planning 若越权，可能重复状态或把目标解释误当交付事实。发生频率与性能影响未测量。

## 9. 为什么它值得保留在版本演化里

distinct design delta（独特设计变化）是第四模块专门管理承诺、结果、验证与认可的关系。它适合学习“忙过、做完、证实、被认可”为何需分别举证；这比靠版本号或模块数推断效果更有信息。

## 10. 下一版要看什么

继续读 [v7c GUIDE](../06-v7c-global-decision-policy/GUIDE.md)：

- 多个比较因素怎样收成有支配顺序的层级？
- 公开职级任期、结果兑现时间、承诺负担如何参与策略？
- 哪两个 Skill 原文保持不变？
