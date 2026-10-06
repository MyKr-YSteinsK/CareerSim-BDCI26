# v4｜版本讲解

> **FACT｜事实** 依据[Instruction](instruction.md)、各 Skill、[SOURCE](SOURCE.md)、[DELTA](DELTA.md)及文内运行记录；分析标为 **INTERPRETATION｜解释**，缺证据标为 **UNKNOWN｜未知**。基本概念可先看 [v3c GUIDE](../01-v3c-zh-aligned-policy/GUIDE.md)。

## 1. 这个版本处在什么位置

**FACT**：`candidate-v4-lean-runtime-policy` 是 pre-S06 配置，对应运行 Task 为 S06-07。它从上一代表版本 v3c 的四个 Skill 收拢为三个：Board、Planning、Risk；parent 也是 v3c。它在七版本中展示一次精简，以及可明确归属的短局结果。

## 2. 这一版的核心结构

```text
新鲜观察 → 到触发点时刷新稀疏 Board
         → Planning 目标与路径建议 / 普通决策
         → 明确重大风险时 Risk → Single Agent 决定并提交
```

箭头表示职责和信息顺序，不是 Skill 的 Python 函数互调。`career-action-trace` 已退出；notes 只留一句与动作相关的理由，三个模块都没有动作提交权。

## 3. Instruction 怎么约束 Agent

七行原文逐块关注：

| 条款 | FACT｜具体约束 | INTERPRETATION｜为何影响长程决策 |
|---|---|---|
| 48 月优化与重大风险 | “成熟、圆滑、体面、稳妥”本身不算收益；公开保密、健康、生存等重大风险仍是约束 | 防止把故事叙事的好听程度当作职业收益 |
| 季度 checkpoint | 首次 Energy 前 fresh observe、稀疏 Board、唯一 Gap；同季主行动复用 | 缩短重复记录，同时依赖复用前状态仍适用 |
| 重复动作 | observed effect 优先；同动作同 Gap 双可比 checkpoint 无进展才 STALLED | 菜单收益不能永久替代观察结果 |
| 风险与软成本 | Material Risk（重大风险）是约束，Soft Cost（软成本）是机会成本；预算可用时不默认退让 | 成长可能有成本，成本不等于危机 |
| 比较预算 | 普通事件最多比两个候选一次，不复述完成的比较，无新证据不重开 | 限制反复推敲同一决策 |
| 上下文恢复 | 同一游戏 session 先新观察；必要时最多五条公开日志、两条效果 | 避免恢复过程变成全历史回放或跨局记忆 |
| 权限与信息 | 当前局公开事实；不猜阈值、权重和事件答案；Agent 唯一提交，notes 一句理由 | 模块提供建议，执行和结果验证仍需正常工具循环 |

## 4. 每个 Skill 分别负责什么

### structured-state-board｜稀疏事实缓存

[原文](skills/structured-state-board/SKILL.md)只读取当前局公开观察、确认回执和必要恢复信息，输出 facts、unknown、freshness 与最多两条 recent effects（近期效果）。Planning 解释进展，Risk 解释候选风险；Board 不拥有目标，不排序、不提交。关键规则是：

- 新局、季度规划、重大变化、恢复或失效才完整刷新；普通月度事件及每次回执不自动触发。
- 不建长期 inferred 列表；新观察优先，混杂变化写 UNKNOWN。
- game session 与 conversation（对话）身份不同；恢复最多五条同局日志，不读数据库。

**反例**：从旧回执算出“当前健康应该是多少”，或只保留初始板却假定趋势持续最新。

### rolling-planning｜唯一战略规划

[原文](skills/rolling-planning/SKILL.md)读取 fresh public evidence（新鲜公开证据）、Board 和公开 Handbook，输出最多六行目标／进展／预算／路径 checkpoint。它决定 Gap 与建议，Risk 只审当前候选；不预测分数、不保存跨局计划、不调用工具。关键规则是：

- 季度首次 Energy 前刷新；新季度或半年反馈本身不必全文重读，重大框架变化才重建。
- Gap 只能一个，不默认均衡发展；双可比 checkpoint 的 STALLED 才要求比较另一类路径。
- 预算 AVAILABLE 且公开收益更强时，不因“更稳妥”自动放弃；普通故事比较有界。

**反例**：同时追 Skill、Network、Output，把六行 checkpoint 改成反复摇摆的多目标长讨论。

### risk-review｜罕见重大风险门槛

[原文](skills/risk-review/SKILL.md)读取候选、新鲜公开重大后果与合法缓解项，输出一个 `ALLOW / WARN / RECONSIDER / UNKNOWN` 加一句理由。它不管一般战略、持久风险状态或提交；战略预算归 Planning。关键规则是：

- 严重健康、危机、保密、报复、解雇等重大公开后果触发；普通压力、少量代价、普通绩效反馈不单独触发。
- RECONSIDER 需要明确重大风险、直接合法缓解项和候选遗漏三条件；不等于强制最保守答案。
- UNKNOWN 回正常流程，不猜阈值；“处理历史埋雷”只在实际合法且相关时考虑，效果仍未保证。

**反例**：把“有更安全选项”当成重选条件，或把普通英文 reconsider 当作正式 Risk 状态。

## 5. 相比上一代表版本改了什么

**FACT**：[DELTA](DELTA.md)记录 Instruction 改变，移除 `career-action-trace`，未新增 Skill；三个保留模块全部改文。原文对比可见 Board 转向稀疏缓存，Risk 触发收窄到明确重大后果，动作说明取消旧轨迹标记职责。

**INTERPRETATION**：从文本结构与后续证据看，可以解释为减少重复状态和仪式性输出，并突出成长取舍。没有受控对照证明精简节省了多少成本，或造成了低分。

## 6. 一个具体决策流程怎么走

**真实情境来源**：[v4 Health 取证](../../project/runs/v4-run1-health-forensic.md)的 M3 Q1 Energy 窗口。参与者当时公开 Health 为 2，菜单有健康恢复、人脉维护、准备汇报材料；执行恢复后新观察为 4。这里是公开数值描述，不是通用策略阈值。

**INTERPRETATION｜按合同走查**：Board 应保存当前值与可比变化，不把整条 Health 下行归因给一个事件；Planning 将公开生存约束与当前 Gap 一起比较，并建立季度 checkpoint；若候选忽略明确重大风险且有直接合法缓解项，Risk 可要求重比。每次选择仍由 Agent 提交，效果等待新观察。

**FACT｜实际记录**：Agent 识别健康危险，最终选一次恢复并保留另两种投入，但经历冗长权衡；没有可验证的六行季度 checkpoint 或正式 Risk 状态输出。走查的规范步骤不冒充已执行事实，也不承诺多恢复一次就能存活。

## 7. 真实运行证据

**Observed Run（观测运行结果）**：S06-07，run `20260924T160806Z`，session `fdcaa70a85f44662a6a329513c175676`；`25.84 / 18.09 / 6m / E / L2`。

这是 **Natural terminal（自然提前终局）**，48 月目标下的未完成运行；不是中途技术失败。23 次动作全部成功，M6 Health 归零。其 score_report 当时 ending_score 为空，分数按 exact session 从已配置数据库只读取得；现存数据库不再含该 session，历史来源 caveat 见[运行历史](../../project/RUN_HISTORY.md)。不能把它描述成今天可从当前 DB 重取的分数。

取证将死亡模式记为累积消耗，部分动作归因含糊。原“RECONSIDER 17 次”已澄清为普通推理词，不是 17 个 Risk 输出。没有统一的 Adherence（运行遵循）PASS/FAIL 状态，长程遵循也未观测。

## 8. 这个版本暴露出的限制

**FACT**：只有一个短局；结构化 Board 趋势和单一 Gap 未稳定保留；Health 已低时仍选成长并等待以后恢复。取证支持补充公开生存趋势守卫这一待修假设，不支持数值 cutoff（分界线），也不证明它会提高分数。工具调用成功与政策执行充分是两回事。

**UNKNOWN**：每次损失是否可避免、某一规则对死亡的独立贡献、精简与低分的因果关系。

## 9. 为什么它值得保留在版本演化里

它的 distinct design delta（独特设计变化）是四到三模块的收拢与稀疏状态。真实短局让学习者看见“文件规则已加载”和“运行持续遵循”之间的距离。低分不能证明 consolidation（收拢）错误，也不能比较三 Skill 与四 Skill 的整体优劣。

## 10. 下一版要看什么

继续读 [v5 GUIDE](../03-v5-evidence-driven-phase-policy/GUIDE.md)：

- 每次观察的快速扫描怎样补充稀疏 Board？
- 生存带与 review 前检查怎样表达风险趋势？
- 更密集的控制字段带来了哪些顺序问题？
