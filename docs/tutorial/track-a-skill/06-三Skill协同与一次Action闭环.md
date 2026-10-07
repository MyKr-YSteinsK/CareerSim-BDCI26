# 06｜三 Skill 协同与一次 Action 闭环

[统一入口与术语](../00-从这里开始.md) · [本 Track 阅读路线](01-从零理解Agent、Instruction与Skill.md)


前面分别学了事实、规划和风险。本章把它们接成一次具体 Action（动作）。**FACT** 的规则来自[exact-v6 Instruction](../../skill-evolution/04-v6-auditable-control-loop/instruction.md)和三个历史 Skill；真实 M13 事实来自[运行验证](../../project/runs/v6-run1-validation.md)。**INTERPRETATION** 用于解释交接，完整构造流程标为 **TEACHING EXAMPLE**。

## 1. 闭环的起点和终点

```text
Agent fresh observe
  → Board 整理公开事实、来源、新鲜度
  → Planning 维护一个目标与预算 → 生成合法 candidate
  → Risk gate
  → 必要时比较一个直接相关合法 alternative；换项 re-gate
  → Agent 生成紧邻 pre-action CTRL
  → 同回合 take_action
  → receipt（回执）
  → Agent fresh observe
  → 下一次 Board / Planning / Risk
```

箭头表示职责与信息关系，不是 Skill 之间的 Python 函数调用链。首个 observe 的取得与 take_action 的调用都由 Single Agent 负责。Board 没有自行获取新状态，Planning 没有自行执行计划，Risk 没有独立提交缓解动作。

**INTERPRETATION**：一次选择的闭合不等于任务结束。CTRL 是决定即将执行时的记录，receipt 说明执行返回了什么；下一次 observe 才把环境的新公开状态带回工作上下文。缺这最后一步，就无法知道旧候选和旧预算还能否用于下一动作。

## 2. 每一项交接究竟交什么

| 步骤 | 输入与输出 | 谁拥有判断 | 不能跳过的边界 |
|---|---|---|---|
| fresh observe | 当前游戏的公开观察与合法选项 | Agent 取得；Board 检查来源 | 当前身份、新鲜度、公开权限 |
| Board | 当前事实、反馈、方向、有限近期效果、未知 | 事实整理 | 不选 Gap、不判 STALLED、不评候选风险 |
| Planning | 一个 Gap、Progress、Risk Budget、Horizon；需要时 checkpoint；合法候选建议 | 战略目标与排序 | 不在候选前预填 Risk，不提交 |
| Risk | 当前候选的 PASS 或完整审查状态与理由 | 候选风险 | 不重写长期目标；重比只有相关一个替代 |
| 相关 alternative | 原候选与直接缓解项的一次比较 | 同一 Agent 按 Planning/Risk 合同 | 换项重 gate；未完成 X=0 |
| CTRL | B/G/P/R/CP/X 的当前语义 | Agent 根据模块工作生成 | 本版独立文本，不入 notes；紧邻每次尝试 |
| take_action | 当前一个合法选择及简短说明 | 唯一 Agent 提交 | 不是 Skill 自己调用，不能拿旧 CTRL 授权新项 |
| receipt | 工具明确确认的成功或错误信息 | Agent 读取 | 不推未公开效果，不默认等于完整当前状态 |
| fresh observe | 状态改变后的当前公开事实 | Agent 取得；Board 再整理 | 不连续复用旧候选、旧扫描 |

表里的“输入／输出”是合同信息关系，不是另创固定模块返回 JSON。比如 v6 Planning 要求短 scan 与必要 checkpoint，没有规定所有决策都输出一个名为 CANDIDATE 的固定行；那是后继版本的接口风格，不能倒灌进 v6。

## 3. 真实 worked example：v6 M13 的健康风险重比

### 可以确定的事实

**FACT**：报告确认 M13 一次 health-risk choice（健康风险选择）触发 genuine RECONSIDER，比较并选了较低负荷的当前合法 alternative，再对所选候选 gate。marker（标记）文字在 transcript 中重复。

这些事实足以证明“有一次相关重比并发生换项后审查”，不足以提供完整现场菜单。报告没有给该窗口所有公开字段、原候选的整数编号、Gap 的完整值或唯一紧邻控制行。它也没有独立证明这个选择带来多少健康收益或晋升收益。

### 从真实事实能走到哪里

| 环节 | 真实记录支持的部分 | 缺失部分 |
|---|---|---|
| 观察与 Board | 该局工具使用同一 session；M13 情境涉及公开健康风险 | 该窗口完整 Board 与全部公开值 UNKNOWN |
| Planning / 候选 | 存在进入风险审查的合法候选 | Primary Gap、Progress、预算精确值和排序理由 UNKNOWN |
| 初次 Risk | genuine RECONSIDER 已确认 | 唯一结构化门禁输出的完整原文 UNKNOWN |
| 比较替代 | 低负荷合法替代被比较并选择 | 两个候选整数与完整菜单 UNKNOWN |
| 新候选 gate | 所选替代再次 gate 已确认 | 最终 R 精确值 UNKNOWN |
| CTRL / 提交 | 标记文字存在且重复；本局有对应实际动作流程 | Gap、CP、X 和唯一紧邻同回合配对无法认证 |
| 后续观察 | 全局 202 次成功改变状态后均有新 observe | 该选择的独立因果收益 UNKNOWN |

**INTERPRETATION**：要理解这次协作，可把 Board 看作风险公开背景的整理者、Planning 看作初始候选与目标的提供者、Risk 看作一次相关重比的触发者、Agent 看作换项和提交者。这是按合同解释记录，不把未知字段补成“已正确执行”。

### 不能填出来的“漂亮控制行”

```text
真实 M13：G=UNKNOWN，P=UNKNOWN，R精确值=UNKNOWN，CP=UNKNOWN，X精确值=UNKNOWN
```

上行是教材的缺口说明，不是可提交 CTRL。历史语法要求未知字段用其合法占位；但我们是在解释资料，并没有准备运行。不能猜 B=F、G=Health、P=S，然后把猜的行写为原始记录。尤其健康风险情境并不证明长期 Primary Gap 就是健康，P=S 也需严格停滞条件，而不是“风险严重”。

## 4. 完整教学推演：所有交接在同一例子里

**TEACHING EXAMPLE｜教学示例，不是历史 Run 原始记录。** 以下情境完全构造，不是对真实 M13 菜单的复原。假设当前 session甲/M13，最新正式公开反馈的 Gap 是交付证据；Progress 没有干净可比数据，保持 UNKNOWN。可比健康观察持续下降，当前有明确严重负荷警告。当前公开菜单只有两项真正相关合法候选：1 是追加负荷完成成果，2 是按公开允许的分工降低负荷并保留部分交付机会。公开文本明确 2 可缓解相关负荷，但效果幅度未知。

### 第一步：observe 提供当时材料

Agent 取得当前公开观察和这两项选项。候选编号只适用于这个构造菜单。不能用真实 Run 中任何内部结果告诉自己哪项收益更大，也不能因为半年后得了 A 就逆推出应选 1。

### 第二步：Board 整理，不选答案

Board 记录身份、月份、当前公开状态、可比下行、严重警告和菜单。动作收益未发生，写未知；如前后变化有混杂，则不把下行全部归因于一个动作。Board 不写“2 最好”，也不写 Risk=RECONSIDER。

### 第三步：Planning 维护目标与约束，先提名

Planning 保持一个交付证据 Gap，Progress=UNKNOWN，根据公开趋势和警告判断 Risk Budget=TIGHT。它比较当前可兑现交付与直接相关健康成本，不能为了偏爱 1 把预算改为 AVAILABLE。

为演示重比分支，这里刻意保留一个需要纠正的初始提名 1，不把它当成正确的 Planning 范本。若 Planning 已确认 1 是直接加重已激活约束的非必要成长项，就应暂缓或拒绝，而不是依赖 Risk 替自己兜底。以下展示初始遗漏怎样在提交前被 Risk 纠正；Risk 此时才有具体审查对象。

### 第四步：Risk 检查候选 1

公开重大风险明确；合法 2 直接缓解；1 未处理并加重风险，三条件同时满足，Risk 输出 RECONSIDER 和一句公开理由。此时 X=0，不能行动。Skill 不调用动作，也不擅自把 Gap 改为“以后每季恢复”。

### 第五步：只比较一次相关替代，换项再 gate

Agent 比较 1 与 2 的公开目标贡献、成本和直接缓解关系，选 2。由于选择对象改变，2 自己重新接受 Risk gate。假设完整审查确认其公开允许分工没有要求改变的重大风险，则 ALLOW；没有声称全部危险已解除，只有“这个候选当前可接受”。

X=1 记录比较完成。终局风险约束也仍成立，不能因 X=1 放行明显加重可避免终局危险的非必要 1。

### 第六步：生成当次 CTRL，再紧邻提交

本例既非新局／季度首 Energy／已知 review 前最后行动窗／反馈后 reset／严格停滞／恢复，故 CP=-；事实扫描已确认新鲜 B=F，公开 Gap 可缩写为 O，Progress 未知 P=?。教学性控制行是：

```text
CTRL B=F G=O P=? R=ALLOW CP=- X=1
```

这是**本构造情境的教学 CTRL**，不是 M13 原行。随后同一 Agent 在同回合紧邻调用 take_action，选择这个构造菜单的整数 2，notes 仅简短说明公开的减负与交付理由，CTRL 不入 notes。

### 第七步：回执与新观察

假设回执明确返回 success。它确认工具接受／执行了所提交动作，不足以让 Agent 自行计算所有公开状态或宣布 warning 已解除。exact-v6 无论回执携带多少局部信息，都要求状态改变后 fresh observe。

下一新观察若警告仍存在，就不能仅因自己选了缓解项把 Risk Budget 续写 AVAILABLE；若新鲜公开证据显示约束缓解，Planning 再判断。效果幅度、结果认可与未来晋升都只按新证据更新。

在同一构造材料下，另一条正确路径是 Planning 已应用 TIGHT 约束而直接提名 2，再由 Risk 完整审查为 ALLOW，CTRL 的 X=- 表示没有发生 RECONSIDER 重比。随后仍须紧邻提交、读取回执和 fresh observe。不是每次动作都要先选错一项来练习重比；有界重比是必要时的分支。

**INTERPRETATION**：完整例子的每个结论都需要落在相应职责、证据与时点上。换成一个新公开情境，最佳候选可以不同，但不能省略交接。

## 5. 为什么 success receipt 不是 fresh state

receipt（回执）回答一次调用返回什么；fresh state（新鲜状态）回答当前环境公开呈现什么。成功能支持“这次动作发生了”，不能自动支持“菜单宣传的全部收益发生了”“警告已解除”“资源可以按预期继续”。

**FACT**：v6 要求动作改变状态后再 observe；202 次成功状态改变调用都有该纪律。一次无效 Energy 参数被执行前拒绝、没有改变状态，是另一种有明确证据的情况，不能推所有失败都无副作用。

**INTERPRETATION**：即使收到某个局部字段，也可能无法确认本次决策需要的全部当前状态、事件、合法选项与新反馈。每动作后的新观察把这些材料重新对齐。在本教材里不需要懂工具实现，也能看出“动作回执”与“当前完整公开决策材料”的区别。

## 6. 错误 loop：旧候选如何被偷偷续期

**TEACHING EXAMPLE｜教学示例，不是历史 Run 原始记录。** 错误流程如下：

```text
observe（健康警告尚未出现）
→ Planning 计划两个成长动作
→ take_action 第一个
→ success receipt
→ 直接复用旧候选、旧 scan、旧 Risk，再 take_action 第二个
```

第一处问题是跳过新事实：第一个动作可能改变状态或推进公开反馈，旧菜单和旧约束不能直接代表现在。第二处是规划越过时间边界：联合计划不授权后续批次。第三处是 Risk 对象失配：上一候选的结果不是下一候选的门禁。第四处是记录失配：上一 CTRL 不能对应第二次 attempt。

修正是第一个 success 后新 observe→Board→Planning→新候选→Risk→新 CTRL→动作。如果新事实没有实质变化，比较可以短，但仍然是依据新材料的当前决定。不能因为“结果应该一样”就取消观察。

## 7. 另两种未闭合：打印标记就停、重复重开

**TEACHING EXAMPLE｜教学示例，不是历史 Run 原始记录。** 一种错法是 CTRL 已完成却以此结束回合，没有 take_action；另一种是 gate 已完成、没有新证据，仍反复比较 A/B，输出多个相同 CTRL。

**FACT**：Instruction 明确不得以 CTRL 结束回合；Planning 对普通故事比较有界，无新证据不重开，除非 Risk 要求一次相关重比。v6 真实 M1/M48 反复重开是遵循问题，CTRL 文字重复与缺回合 ID 也是审计限制。

**INTERPRETATION**：决定要够充分但应能闭合。外部状态没有改变，重复说同一理由不会变成新证据；输出数量也不会自动提高审计可靠性。具体技术如何绑定回合属于 Track B｜System / Runtime，将在后续章节解释。

## 8. 自测：把真实与教学两条链分别讲清

请先复述真实 M13，不得添加 Gap、数值或选项整数；再复述构造流程，解释每个 CTRL 字段为什么能填。最后指出两条链分别能证明什么。

参考分析：真实链支持一次相关重比、低负荷替代选择与 re-gate，有格式／配对缺口，不证明因果收益；构造链教信息如何流转，不提供历史成绩证据。能把两者分开，才算真正完成从“记流程”到“检查证据和权限”的学习。
