# v3c｜版本讲解

> 本文的 **FACT｜事实** 来自本目录[Instruction 原文](instruction.md)、各 Skill 原文与 [SOURCE](SOURCE.md)；教学分析标为 **INTERPRETATION｜解释**，缺证据标为 **UNKNOWN｜未知**。历史原件与权威工程证据优先。

## 1. 这个版本处在什么位置

**FACT**：Candidate ID 为 `candidate-v3c-zh-aligned-policy`，包含四个 Skill，是这七个代表版本的起点。具体 Stage / Task 为 UNKNOWN；配置 parent 是 v3b，但本档案没有前一个代表快照。它是较早可恢复的完整配置，不是已证明的“最早 Skill”：更早的 Skill-only 来源缺完整指令身份，见[版本索引](../00-版本索引.md)。

Candidate（候选版本）指一组可辨认的指令与模块配置；Agent（智能体）是读取信息、作决定并调用工具的执行者。Instruction（运行指令）管总体顺序和权限，Skill（技能模块）是供同一个 Agent 使用的专项规则，不是四个独立 Agent。读取文件、实际应用规则、取得收益是三种不同证据。

## 2. 这一版的核心结构

```text
Single Agent 获取新鲜公开观察
  → Board 整理事实
  → 到规划点时 Planning 建立目标；普通选择按当前目标比较
  → 有公开风险线索时 Risk 审查候选
  → Agent 最终选定 → Trace 追加标记 → Agent 提交一次动作
```

箭头表示职责顺序和信息关系，不代表 Skill 之间存在直接 Python function call（函数调用）。Board 回答“知道什么”，Planning 回答“优先解决什么”，Risk 回答“这个候选是否忽略重大风险”，Trace 只留下使用痕迹。

## 3. Instruction 怎么约束 Agent

八行原文可按六块读：

| 原文块 | FACT｜要求 | INTERPRETATION｜忽略后的问题类型 |
|---|---|---|
| 首次观察、季度 Energy、重读条件 | 首次有效观察后详细读 Planning；季度首次 Energy 前刷新 checkpoint；同季主行动可复用；重大反馈或上下文丢失等情形重建 | 长程目标需要恢复依据，不能靠模糊记忆延续 |
| 一个 `Primary Gap` 与比较顺序 | 只设一个公开主要差距；按重大风险、Gap 贡献、次级收益、软成本、未知比较 | 多个目标同时变动会使取舍失去焦点 |
| `Risk Budget` | `TIGHT / AVAILABLE / UNKNOWN`；预算可用且无重大风险时，可接受软成本换取更强公开收益 | 把“最稳妥”当目标可能挤掉成长；预算也不能当隐藏风险数值 |
| 进展与重复动作 | 表扬不能单独证明 `ADVANCING`；同动作、同 Gap、两个相邻可比 checkpoint 无进展才 `STALLED` | 一次失利不够判断路径停滞，菜单承诺也不等于实际效果 |
| 48 月与普通事件预算 | 只按公开月份考虑剩余时间；普通非战略事件最多比两个候选一次，新证据或 RECONSIDER 才重开 | 远期收益可能来不及兑现；反复推敲会增加运行负担 |
| 唯一提交权 | 只有 Single Agent 提交，Skills 不提交 | 职责建议不能变成重复动作或第二提交者 |

Checkpoint（复核点）是一份短目标记录，不是文件型记忆。`observed effect`（已观察效果）须有同局可比依据，`advertised effect`（菜单宣称效果）只是待验证信息。

## 4. 每个 Skill 分别负责什么

### structured-state-board｜状态板

[原文](skills/structured-state-board/SKILL.md)整理最新公开状态、合法选项与已确认回执，输出替换式的 `observed / inferred / unknown` 和最多两条近期效果，供 Planning、Risk 使用。它不选目标、不评风险、不提交，也不把工作上下文保存为跨局 Memory（记忆）。关键规则是：

- 新鲜 observe 优先，回执只确认它实际说明的事实；推断不能升级成 observed。
- 恢复时先确认游戏 session；必要时最多查同局五条公开日志，恢复最多两组效果。
- 前后变化若混入其他事件，效果写 UNKNOWN；状态板保持有界。

**反例**：把上一局的目标和数值搬进本局，或把“行动后升职”直接记成该行动造成升职。

### rolling-planning｜滚动规划

[原文](skills/rolling-planning/SKILL.md)读取 Board、fresh observe、确认结果与公开 Handbook，输出最多六条 checkpoint：Horizon、Primary Gap、Progress、Recent Effect、Risk Budget、Path Trade-off。它拥有目标和路径建议，Risk 只审具体候选；它不预测分数、不调用工具、不持久化计划。关键规则是：

- 季度首 Energy 前刷新；普通故事不要求完整规划，重大变化或恢复才重读重建。
- 严格用双 checkpoint 条件判 STALLED，随后比较另一类合法路径，但不强制换路。
- Safety（安全）是约束；Soft Cost（软成本）单独不能否决公开收益更强的路径。

**反例**：看到人脉较低就固定投入人脉，既不核对当前 Gap，也不检查同局真实响应。

### risk-review｜风险审查

[原文](skills/risk-review/SKILL.md)读取当前公开警告、候选与合法缓解项，返回 `ALLOW / WARN / RECONSIDER / UNKNOWN` 和短理由。它不拥有战略 Risk Budget（风险预算），不提交动作，不猜隐藏阈值。关键规则是：

- 公开风险、信任或明确绩效风险线索触发审查；Soft Cost 不自动要求重选。
- RECONSIDER 必须同时有明确重大风险、直接合法缓解项、候选遗漏该风险；只是要求同一个 Agent 重比。
- 实际运行才追加对应 `[S03_RISK:状态]`，保留已有 S02 标记；标记不代表风险库存。

**反例**：菜单里出现“处理历史埋雷”便每季度固定选择，或认为一次处理必然消除风险。

### career-action-trace｜行动轨迹

[原文](skills/career-action-trace/SKILL.md)读取已选选项与 notes（动作说明），只影响最终说明的尾部，不影响策略；它位于最终选择之后。关键规则是：

- 每次 take_action 前保持选项和原短理由不变。
- 精确追加 ` [S02_SKILL_USED]`；空 notes 只写标记本体。
- 由现有工具提交一次，不接管 new_game、observe 或终止处理。

**反例**：为了证明 Skill 有价值而改选，或者把标记存在当作策略收益证明。

## 5. 相比上一代表版本改了什么

**FACT**：[DELTA](DELTA.md)仅写 `No previous representative milestone in this archive.`；没有可作机械对比的上一代表版本，不能补造增删清单。

**INTERPRETATION**：从文本结构与后续证据看，可以解释为一个把事实、目标、风险与轨迹记录分开的早期完整配置。Trace 的窄职责使“用了模块”有可见标记，但不提供动作优劣的判断。实际历史设计动机没有完整记录，保留 UNKNOWN。

## 6. 一个具体决策流程怎么走

**教学性 hypothetical example（假设示例）：这是教学示例，不是该 Candidate 的真实 Run 记录。** 情境来自上述 Planning 与 Risk 合同允许的季度选择：新鲜公开反馈指出交付缺口，菜单有推进交付和普通关系维护两条合法路径；无重大警告，安全余量公开可见。

1. Board 记录本局身份、反馈与菜单，不推断隐藏晋升资格。
2. Planning 设一个交付 Gap；若预算可用，比较直接交付贡献与关系维护收益，普通摩擦作为机会成本。
3. 没有触发线索就不虚构 Risk 输出；若新警告出现，Risk 按公开证据审候选。
4. Agent 最终决定后，Trace 追加 S02 标记；若 Risk 实际运行，也保留对应 S03 标记。
5. 下一次新鲜观察才记录效果；表扬不能单独把 Progress 写成 ADVANCING。

这说明职责如何协作，不承诺交付、晋升或分数结果。

## 7. 真实运行证据

**FACT**：[SOURCE](SOURCE.md)未识别能归属此 exact configuration（精确配置）的 Run 或分数，分类为 **No exact run identified（未识别精确版本运行）**。关联的[控制表面证据](../../project/research/S10-19R3_CONTROL_SURFACE_EVIDENCE.json)属于静态来源，不是此版本完整对局。

因此 Partial run（部分运行）、Complete run（完整运行）、Technical failure（技术失败）、Natural terminal（自然终局）和 Adherence failure（遵循失败）在此版本均未确立。Adherence（运行遵循）指执行过程是否满足合同，不能由文件已加载替代证明。

## 8. 这个版本暴露出的限制

**FACT**：精确文本可恢复，但 Stage / Task、运行结果和行为遵循证据不足；不能虚构分数。Board 允许单列有限推断，恢复和归因要求仍依赖 Agent 实际执行。

**INTERPRETATION**：指令与 Planning 重复定义若干比较规则，可能增加维护成本；Trace 标记只能证明记录格式，难以单独审计目标选择和 Risk 语义。其成本与收益没有测量。

## 9. 为什么它值得保留在版本演化里

在 49 个 Candidate 的学习路线中，它的区分点是“完整四模块配置 + 极窄 Trace 权限 + 单一 Gap + 有界同局恢复”。学习者可从这里看懂模块数、角色数、动作提交者数量为何不是同一件事，也能看到后续精简实际删掉了什么。

## 10. 下一版要看什么

继续读 [v4 GUIDE](../02-v4-lean-runtime-policy/GUIDE.md)：

- Trace 退出后，动作说明和审计标记如何变化？
- Board 刷新为何变得稀疏？
- 真实短局如何暴露生存与遵循问题，又为何不能证明精简造成低分？
