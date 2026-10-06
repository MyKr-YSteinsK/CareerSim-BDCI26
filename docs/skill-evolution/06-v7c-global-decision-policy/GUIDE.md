# v7c｜版本讲解

> **FACT｜事实** 依据[Instruction](instruction.md)、各 Skill、[SOURCE](SOURCE.md)、[DELTA](DELTA.md)及 [S07-26 静态审查](../../project/reviews/S07-26_V7C_GLOBAL_DECISION_POLICY_REVIEW.md)；分析标为 **INTERPRETATION｜解释**，缺证据为 **UNKNOWN｜未知**。共用概念见 [v3c GUIDE](../01-v3c-zh-aligned-policy/GUIDE.md)，生命周期基础见 [v7 GUIDE](../05-v7-global-trajectory-delivery/GUIDE.md)。

## 1. 这个版本处在什么位置

**FACT**：`candidate-v7c-global-decision-policy` 对应 S07-26，四个 Skill 为 Board、Planning、Delivery、Risk。上一代表版本是 v7，配置 parent 却是 v7b；跳过中间版本的代表比较不等于直接 parent 比较。

它在七版本中展示 Global Decision Policy（全局决策策略）的层级化：当前明确的高层优势，不应被低层的礼貌、可逆性等偏好重新拉平。静态审查通过，运行效果未验证。

## 2. 这一版的核心结构

```text
fresh observe → Board（包括可见职级任期）→ 相关 Delivery
  → Planning 按支配层比较 → 一个合法候选
  → Risk → DECISION_CLOSED → Agent notes/动作 → fresh observe
```

箭头表示职责顺序和信息关系，不是 Python 函数互调。四模块 owner（职责归属）与 v7 相同；主要改变在 Planning 的排序结构及 Board 的公开 tenure（职级任期）输入。

## 3. Instruction 怎么约束 Agent

七行分别保留：证据与职责、启动四份读取、每步顺序、全局优先级摘要、动作标记与有界关闭、恢复、禁止过拟合配方。细节放回所属 Skill，Instruction 不复制所有策略解释。

最关键的第四行按如下顺序读：

| 层 | FACT｜比较什么 | INTERPRETATION｜不能怎样误用 |
|---|---|---|
| 公开 binding constraints | 生存、合规或支付能力等已生效约束 | 普通开销不能一律变成危机 |
| Promotion Frontier / 一个 Gap | 下一阶段职业进展的公开瓶颈 | 不是隐藏晋升 eligibility（资格）检测器 |
| 当前 review-window realization | 哪个结果能在当前窗口形成并验证 | 计划或报告标题不等于结果 |
| Global compounding / 剩余 horizon | 长程复利与实际剩余时间 | 不能固定 M36/M42 为“冲刺阶段” |
| Commitment efficiency / time-to-realization | 现有承诺、依赖、阻塞与兑现时机 | 项目数量不直接等于拥堵；旧项目不是永远优先 |
| near-tie Story semantic priors | 价值接近时用可核实、协作、可逆等语义偏好区分 | 低层“更稳妥”不能压过明确更强成长收益 |
| candidate-specific Risk | 选定候选后做重大风险 gate | Planning 不提前重做 Risk 的具体判断 |

第五行 CTRL 仍为 `[CTRL G=... P=... R=... X=...]`，继承 v7 的 notes 前缀及过程 R：RECONSIDER 比较完成记 X=1，过程 R 保持；替代仍须 gate，X=0 禁止动作；无分支则最终普通 R、X=-。Energy 一次一个整数，状态改变后新 observe，关闭后无新证据不重开。Recovery（恢复）要求同局新观察、四份重读、事实与 lifecycle 重建；不能补造旧 commitment。

## 4. 每个 Skill 分别负责什么

### structured-state-board｜新增公开任期输入

[原文](skills/structured-state-board/SKILL.md)读取新公开观察、七项状态、反馈／警告和可比变化，并在字段实际可见时记录 `CurrentLevelDuration / duration_in_level`。输出带来源、新鲜度的有界事实，供 Planning 判断；不算晋升概率、不拥有 lifecycle、不排序、不提交。关键规则是：

- 两任期字段缺失或冲突用 UNKNOWN；不从月份和晋升间隔推算。
- 近期效果最多两条，混杂不归因；事实快照在明确触发点替换。
- 恢复后同局 fresh state 优先，任期无法恢复仍 UNKNOWN，不借快照填空。

**反例**：按“每级必须待 N 月”的假设补出 tenure，再据此宣称晋升资格已满足。

### rolling-planning｜分层策略 owner

[原文](skills/rolling-planning/SKILL.md)读取 Board、Delivery、公开窗口、合法选项与 Handbook，维护一个 Gap、Progress、预算和时间范围，输出最多六字段 checkpoint 与有界候选比较。它决定策略，Delivery 独占 lifecycle，Risk 独占最终候选审查；它不补造交付、不提交。关键规则是：

- Layer 0–7 只展开当前支配层；低层偏好不能重新拉平已明确的高层优势。
- Promotion Frontier 是公开进展语境，任期只是 context；Gap 不自动等于最低数值。
- review 前同时检查 survival readiness（生存准备）和 progression realization（结果兑现）；临近真实结果时比较完成／验证与新开机会，保留例外。
- `Commitment Load` 和 `Time-to-Realization` 只是 Path Trade-off 内临时定性比较，不新增持久状态或数量阈值。
- review 后更新 baseline；双可比 checkpoint 才 STALLED；Energy/Main 联合规划仍逐步新观察。

**反例**：把三条 active item 自动标 CONGESTED（拥堵），或因可回滚方案更稳妥而否决明显更强、无重大风险的成长路径。

### delivery-progress｜保持结果链边界

[原文](skills/delivery-progress/SKILL.md)与 v7 字节一致。读取新公开工作项、回执和相关反馈，输出 item、stage、公开依赖／checkpoint、验证状态与认可关联。它报告工作阶段，Planning 决定继续或换路；它不判 Risk、不写 Gap、不提交。关键规则是：

- 相关机会、承诺、阻塞、结果或反馈变化才更新，否则 no-op。
- 声明未验证与公开验证完成分开；一般表扬／晋升不自动归因。
- 最多三条 active、一条相关 closed；缺失 owner/日期/recognition 为 UNKNOWN。

**反例**：Planning 倾向完成旧项，就把 Delivery 的 BLOCKED 改成 DELIVERED；偏好不是事实。

### risk-review｜保持候选门禁边界

[原文](skills/risk-review/SKILL.md)同样与 v7 字节一致。读取最终候选、公开重大后果和预算，必要时仅消费与重大风险直接相关的 Delivery 摘要；输出 PASS 或 ALLOW/WARN/RECONSIDER/UNKNOWN，影响一次相关重比。它不排序全局目标、不拥有预算、不提交。关键规则是：

- 延期、无回执或 UNKNOWN 本身不是重大风险触发。
- RECONSIDER 只比一个相关合法替代，换候选再 gate；过程 R 与 X 按 Instruction 保留。
- 无新证据则 DECISION_CLOSED；未知最多一次正常刷新，避免循环。

**反例**：用 Risk 再执行一遍全部八层策略，或因普通故事标题带负面词就拦截动作。

## 5. 相比上一代表版本改了什么

**FACT**：[DELTA](DELTA.md)记录 Instruction 改变，未增删 Skill；Planning、Board 改文，Delivery、Risk 不变。v7 的多因素比较转成层级，并增加公开 tenure 输入、兑现时间与承诺负担判断。

**FACT｜审查范围**：S07-26 记录 `V7C_GLOBAL_DECISION_POLICY_STATIC_PASS` 与 `STATIC_IMPLEMENTED_NOT_RUNTIME_VALIDATED`。其提示文本缩减表比较的是当时 parent v7b，不是本档案上一代表 v7，不能把表内节省量写成 v7→v7c 的量，也不能把字节缩减冒充 token 节省。

**INTERPRETATION**：从文本结构与后续证据看，可以解释为让关键约束先决定方向，只有接近时才展开低层因素，以降低每步平铺清单的压力。实际推理成本、收益与遵循改善未测量。

## 6. 一个具体决策流程怎么走

**教学性 hypothetical example（假设示例）：这是教学示例，不是该 Candidate 的真实 Run 记录。** 来源是 Planning Layer 3–6：公开承诺接近可验证结果，下一 review 窗口可见；当前合法候选可完成／验证旧项，或开启回报更晚的新项；无公开生存约束。

1. Board 保留窗口及可见 tenure，缺字段 UNKNOWN；不推隐藏资格。
2. Delivery 确认旧项阶段、checkpoint 和证据状态，不替 Planning 判断最优。
3. Planning 先核对 Gap 与可兑现结果。若旧项高价值、临近结果，新项更晚且无更优证据，可提高完成旧项的优先级。
4. 若旧项 BLOCKED 且本 Agent 无法推进，或新项有更直接瓶颈价值／公开时效，就重新比较；不是“旧项目永远先做”。
5. Risk gate 最终候选，Agent 关闭决定、写 CTRL、提交。后续实际公开结果才更新 lifecycle。

## 7. 真实运行证据

**FACT**：**No exact run identified（未识别精确版本运行）**；没有此精确配置的分数、完整／部分运行、自然终局、技术失败或 Adherence（运行遵循）结论。静态审查没有 live 验证任期字段的实际 key；alias mapping（别名对应关系）为 UNKNOWN。

审查通过仅说明静态实现满足当轮要求，不证明晋升、生存、分数、稳定性或迁移收益。

## 8. 这个版本暴露出的限制

**FACT**：运行字段、行为效果和长期遵循未建立；原 Planning 中重复了一条不改 Delivery state 的边界句。重复文本是原件事实，不意味着必须读作两次执行。

**INTERPRETATION**：分层有助于读懂优先关系，但“瓶颈”“接近结果”“价值接近”等仍需模型根据公开证据判断；写出顺序并不等于有机械策略执行器。误把临时定性标签存成硬阈值，会改变历史合同。

## 9. 为什么它值得保留在版本演化里

distinct design delta（独特设计变化）是分层支配、公开任期和结果兑现时机。学习者能看见：同样四个模块，策略组织方式可以改变；并非每次改版都要增加模块或改所有文件。这里也能练习区分代表版本比较与真实 parent 比较。

## 10. 下一版要看什么

继续读 [v8a GUIDE](../07-v8a-v7o-donor-core-transplant/GUIDE.md)：

- 分层策略如何改成推进／稳定模式和局部响应记录？
- CTRL 的 X 怎样被 RB 与最终 R 接替？
- 两个完整样本为何仍不能证明稳定表现或运行遵循通过？
