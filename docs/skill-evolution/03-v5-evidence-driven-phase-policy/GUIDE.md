# v5｜版本讲解

> **FACT｜事实** 来自[Instruction](instruction.md)、各 Skill、[SOURCE](SOURCE.md)、[DELTA](DELTA.md)及 [S06-16 架构审查](../../project/reviews/S06-16_FINAL_CONTROL_ARCHITECTURE_REVIEW.md)；教学推论标为 **INTERPRETATION｜解释**，缺证据为 **UNKNOWN｜未知**。概念入口见 [v3c GUIDE](../01-v3c-zh-aligned-policy/GUIDE.md)。

## 1. 这个版本处在什么位置

**FACT**：`candidate-v5-evidence-driven-phase-policy` 位于 S06，关联静态审查 S06-16。三个 Skill 仍是 Board、Planning、Risk；上一代表版本与 parent 都是 v4。它在七版本中展示 evidence-driven（证据驱动）的阶段与生存控制表达，但没有可归属的 exact run 分数。

## 2. 这一版的核心结构

```text
fresh observe → Board QUICK_SCAN → Planning QUICK_SCAN / 候选生成
            → Risk 对候选 QUICK_GATE → 补齐四行 CONTROL_SCAN
            → 同一个 Agent 提交
明确 checkpoint 才展开完整 Board / Planning
```

箭头是职责／信息关系，不是 Python 函数调用。原文同时要求动作前 consult（查阅）scan，Risk 又需候选和最新 scan；此图只展示可读的职责关系，不宣称合同没有循环依赖。S06-16 明确审出了顺序含糊。

## 3. Instruction 怎么约束 Agent

| 逻辑块 | FACT｜要求 | INTERPRETATION｜作用与误读风险 |
|---|---|---|
| 任务与权限 | 48 月、公开事实、唯一提交者，安全是约束 | 不能把存活之外的成长目标抹掉 |
| 四行 `CONTROL_SCAN` | Phase、Survival、Primary Gap、Risk Cue；观察后、动作前更新 | 用短字段提示决策，但字段齐全不代表语义正确 |
| 高频模块使用 | Board 每观察 quick scan，Planning 每决策 quick scan，Risk 每故事／Energy／Main quick gate；候选改变重 gate | 使用模块功能不等于每次重读整个文件 |
| 生存与窗口 | TIGHT/CRITICAL 暂停非必要成长；季度首 Energy checkpoint；半年 review 前最后窗口 PRE_REVIEW_CHECK | 不能指望下一次季度资源挽救已过去的危险窗口 |
| 进展与有界比较 | 双可比 checkpoint 才 STALLED；Risk Cue 只触发审查；普通故事最多两候选一次 | cue 是线索，不是答案或隐藏风险估值 |
| 证据与恢复 | 当前 session；禁隐藏公式、事件答案；规则无法恢复时重读；scan 不扩成长推理 | 避免恢复时猜测旧目标或靠事件标题选答案 |

`Phase`（阶段）是 FOUNDATION / PROMOTION / COMPOUNDING / FINAL_SPRINT；`Survival`（生存带）是 SAFE / WATCH / TIGHT / CRITICAL。原文禁止固定数值阈值。Planning 另允许证据不足为 UNKNOWN；不要为了填写模板把未知当 SAFE，四行 Instruction 的列举并没有完整呈现这一回退。

## 4. 每个 Skill 分别负责什么

### structured-state-board｜公开状态与趋势

[原文](skills/structured-state-board/SKILL.md)读取同局 observe、确认结果和可比旧状态，为 scan 提供七项公开字段、反馈、趋势；完整快照含最多两条近期效果。它不拥有 Phase、Survival、Gap 或风险结论，这些交给 Planning、Risk；不提交、不读隐藏数据。关键规则是：

- 每次 fresh observe 做 QUICK_SCAN，但不自动输出完整快照。
- 新局、季度、review 前后、重要变化或恢复才 FULL SNAPSHOT，完整替换且有界。
- 混杂变化写 UNKNOWN；恢复必要时最多五条公开日志，两条效果。

**反例**：Board 看到 Health 下行就自行宣布 CRITICAL 并选恢复动作，越过事实层职责。

### rolling-planning｜阶段化规划

[原文](skills/rolling-planning/SKILL.md)读取 Board、公开反馈、可见 review 窗口与剩余时间，决定 Phase、生存带、唯一 Gap、Progress；完整 checkpoint 最多七字段。它解释趋势并建议候选，Risk 只 gate（审查）具体候选；不预测分数、晋升月份或隐藏资格，不提交。关键规则是：

- 每决策 quick scan，明确触发才 full checkpoint；UNKNOWN 不能伪装 SAFE。
- 阶段按公开状态滚动判断，不是固定月份行动表；FINAL_SPRINT 仍受生存约束。
- PRE_REVIEW_CHECK 同时看公开趋势、警告、剩余故事暴露和真实恢复机会。
- “申请关键项目”只是 broad-growth prior（广义成长先验）；双 checkpoint 停滞或更直接路径可改变比较。

**反例**：一到某月份就固定进入 PROMOTION 并反复申请项目，忽略公开反馈和已观察效果。

### risk-review｜每动作快速门禁

[原文](skills/risk-review/SKILL.md)读取候选、最新 scan、语义线索与公开警告。QUICK_GATE 输出 `NONE / HEALTH / COMPLIANCE / TRUST / RELIABILITY / OTHER`；SAFE 且无 cue 就结束，否则 FULL_REVIEW 输出 `ALLOW / WARN / RECONSIDER / UNKNOWN` 与理由。它不选战略目标、不存风险状态、不提交。关键规则是：

- story、Energy、Main 每动作都 quick gate；生存带非 SAFE 或有 cue 才完整审查。
- 健康、合规等词族只是复核线索，单个普通词不能自动证明 Material Risk。
- RECONSIDER 仍需明确重大风险、直接合法缓解项、候选遗漏；只要求重比，不强制最保守。

**反例**：菜单提到 CI/testing 就断言重大事故，或用 event_id/title 建答案映射。

## 5. 相比上一代表版本改了什么

**FACT**：[DELTA](DELTA.md)记录 Instruction 改变，三个 Skill 都改文，未增删。v4 的稀疏控制增加了每步 quick scan、四行控制摘要、生存带、阶段和 review 前检查。

**FACT｜审查背景**：S06-16 指出，候选相关 Risk Cue 被放在候选生成前的 scan 中，顺序有循环；连续 Energy 的旧 scan 复用可能跨越状态改变；阶段标签与 horizon/Gap 重叠；缺少动作关联的遵循审计表面。这是书面合同审查，不是 v5 低分归因。

**INTERPRETATION**：从文本结构与后续证据看，可以解释为试图让公开趋势进入每次决策，同时减少完整规划频率。更多控制标签也增加了填写、衔接与一致性负担，运行效果仍 UNKNOWN。

## 6. 一个具体决策流程怎么走

**教学性 hypothetical example（假设示例）：这是教学示例，不是该 Candidate 的真实 Run 记录。** 来源为 Planning 的 PRE_REVIEW_CHECK 和 Risk 的 HEALTH 规则：下个公开 review 已近，健康在可比观察中持续下降，当前菜单有继续高负荷任务和减轻负荷两项；具体数值与收益均不假定。

1. Board 只列趋势和来源，不指定生存带。
2. Planning 根据公开下降、警告与可达恢复机会判断约束，选一个 Gap；在最后行动窗口做完整检查。
3. 先生成合法候选，再让 Risk 检查候选是否继续消耗紧张资源；语义 cue 促成审查，不预定选项。
4. 若三条件满足，RECONSIDER 比一次相关替代；换候选再 gate，由 Agent 决定。
5. 下一 Energy 若已改变状态，应重新获取公开事实；不能把“同一 observe 下可复用 scan”扩展成旧状态的行动批次。此步是审查所强调的风险边界，不冒充原 v5 已实现修复。

## 7. 真实运行证据

**FACT**：分类为 **No exact run identified（未识别精确版本运行）**。SOURCE 只提供静态身份与 S06-16 审查，未归属完整局、部分局、自然终局、技术失败或遵循结果。相邻 Candidate 或来源不明的 S06 运行分数不能补成 v5 成绩。

静态审查可以证明文字存在与职责问题，不能证明 Agent 实际持续执行或提高生存率。

## 8. 这个版本暴露出的限制

**FACT**：S06-16 支持澄清 candidate-first（先候选）、状态改变后刷新、review reset（反馈后重建基线）和动作审计。它没有验证 cue 准确率、稳定成绩、云端加载行为或 v5 策略效果。

**INTERPRETATION**：把“已有事实”“战略分类”“候选风险”塞入同一个提前输出的 scan，容易混淆谁先决定什么。更密集的使用频率也不自动等于更好的运行遵循。

## 9. 为什么它值得保留在版本演化里

这一版的 distinct design delta 是生存带、阶段与高频轻量扫描。它提供一个可读的控制合同案例：字段看似完整，仍可能有数据依赖循环。学习重点是审查顺序和 owner（职责归属），而非凭模块数或分数判断优劣。

## 10. 下一版要看什么

继续读 [exact-v6 GUIDE](../04-v6-auditable-control-loop/GUIDE.md)：

- 四行 scan 怎样变成候选之后的 CTRL？
- 阶段与生存分类如何收拢为目标、进展和 Risk Budget？
- 有完整运行后，哪些遵循问题仍未解决？
