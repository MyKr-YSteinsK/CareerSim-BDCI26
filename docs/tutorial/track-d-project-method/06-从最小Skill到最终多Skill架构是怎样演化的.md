# 06｜从最小 Skill 到最终多 Skill 架构

Skill（技能）拆分既能明确责任，也会增加上下文、协调和审计负担。模块数不是能力分数；每一次增减，都应该对应一个已经发现的问题。

本章从研发决策看架构变化。规则逐句拆解请读 [Track A](../track-a-skill/00-学习地图.md)，这里关注为什么组织职责，以及组织变化到底获得了什么证据。

## 先分清“设计职责”和“运行事实”

**FACT｜事实：** 最终设计采用 Single Agent（单智能体）作为唯一提交者。Board 整理当前局事实，Planning 独占策略生成，Risk 审查已有候选。这个职责定义不表示每个实际窗口都符合设计。[架构复盘](../../project/ARCHITECTURE_RETROSPECTIVE.md) · [运行合同](../../project/AGENT_RUNTIME_CONTRACT.md)

**INTERPRETATION｜解释：** 多 Skill 是同一个执行者使用不同职责模块，并非天然有多个独立 Agent。若两个 Skill 都能重写事实，或都能产生新方案，Agent 要解决额外冲突，审计也难判断是谁改变了决策。

## 七个代表节点

| 节点 | 确认的架构变化 | 研究意义 | 证据边界 |
|---|---|---|---|
| v3c | career-action-trace / Board / Planning / Risk 四 Skill | 保存较早的职责配置 | 精确配置可恢复，未识别对应运行 |
| v4 | 移除 career-action-trace，三 Skill 整合 | 检查轨迹职责是否能合并 | 不只是删文件，其余 Skill 内容也变 |
| v5 | 三 Skill，证据驱动阶段策略 | 让决策依据当前反馈与阶段 | 无对应精确完整运行证据 |
| exact-v6 | 三 Skill 可审计控制循环 | 明确事实、策略、风险与提交顺序 | 一个完整样本，遵循失败 |
| v7 | 增加 delivery-progress，四 Skill | 关注长期交付与成长轨迹 | parent 是 v6c；不是直接仅加一文件 |
| v7c | 四 Skill，全局决策策略 | 改 Board 与 Planning 的决策组织 | 精确配置未识别完整运行 |
| v8a | v7z 外壳 + v7o donor core，四 Skill | 把较早核心与后期工程结构结合 | 两完整样本，非 v6 复验 |

**FACT｜事实：** 表中配置、parent（父版本）与差异来自 [历史索引](../../skill-evolution/00-版本索引.md) 以及 [v4 DELTA](../../skill-evolution/02-v4-lean-runtime-policy/DELTA.md)、[v7 DELTA](../../skill-evolution/05-v7-global-trajectory-delivery/DELTA.md)、[v8a DELTA](../../skill-evolution/07-v8a-v7o-donor-core-transplant/DELTA.md)。

“前一个代表版本”是教学抽样顺序，未必是直接 parent。v7 的 parent 为 v6c，v7c 的 parent 为 v7b，v8a 的 parent 为 v7z。不能把索引相邻关系改成实际演化链。

## 为什么会从四个减少为三个

**FACT｜事实：** v4 移除了 career-action-trace，同时更改 Board、Planning、Risk 和 Instruction。它是多处合同整合，不是一个可以孤立估计的“删 Skill 实验”。[v4 差异](../../skill-evolution/02-v4-lean-runtime-policy/DELTA.md)

**INTERPRETATION｜解释：** 当动作记录和事实更新交叉时，合并职责可以让事实来源更集中。读者应该关注是否减少重复维护、是否保留必要轨迹，而不是推断“少一个 Skill 必然更好”。

如果没有职责整合，一个事实可能在 action-trace、Board 与计划里出现多个版本。模型可能使用旧值，审计需要重建哪份文本当时被当成权威。职责压缩的价值需要落到这些 failure mode（失败模式），不能只以文件数说明。

## 为什么 Planning 和 Risk 仍然分开

规划解决“在机会和资源约束下，当前应追求什么”；风险门解决“已产生的候选是否存在直接相关的重大风险”。如果风险模块持续重开战略选择，决策可能在同一公开事实下反复循环。

**FACT｜事实：** exact-v6 的职责强调 Planning 独占策略、Risk 只检查既有候选，Single Agent 唯一提交动作。实际样本观察到一次 Risk RECONSIDER 机制，但整体仍有合同偏离。[S06 收口](../../project/S06_CLOSEOUT.md)

**INTERPRETATION｜解释：** 这种分开帮助确定错误发生在哪层：事实错、候选错、风险门错，或者执行错。它不保证每层判断正确，也不能从一次触发推导 Risk 的平均收益。

## 为什么后来增加 Delivery

**FACT｜事实：** v7 新增 delivery-progress，架构关注全局轨迹与交付进展；相邻代表差异也包含其余三个 Skill 和 Instruction 的变化。[v7 差异](../../skill-evolution/05-v7-global-trajectory-delivery/DELTA.md) · [架构复盘](../../project/ARCHITECTURE_RETROSPECTIVE.md)

**INTERPRETATION｜解释：** 长程成长不能只看资源数字。工作有没有完成、反馈是否验证交付、同一 item（事项）是否在推进，都是规划可能需要的语义。单独模块可以把这类证据显式化。

但新的模块也需要新的输入、记忆、标记和职责冲突规则。若 Delivery 把客户赞许误记为实际交付，形式上多了追踪，事实却没有更可靠。

**FACT｜事实：** v7m 取证建议 Delivery 保留短 item identity 与实际结果证据，不能把赞许沟通当成交付验证。这是局部输出合同的改进依据，没有证明增加提示文字就能解决压缩恢复或网络问题。[v7m 取证](../../project/reviews/S07-47_V7M_M20_PARTIAL_RUN_FORENSIC_REVIEW.md)

## v8a 为什么不等于最终 v6 的升级版

**FACT｜事实：** v8a 保留四 Skill，从 v7o 供体核心移植到 v7z 外壳；两个完整样本为 72.65、59.00。当前 checkout 的历史 v8a 与最终 exact-v6 ZIP 是不同身份。[v8a 来源](../../skill-evolution/07-v8a-v7o-donor-core-transplant/SOURCE.md) · [最终方案审阅](../../project/FINAL_SOLUTION_REVIEW.md)

**INTERPRETATION｜解释：** “后来”表示研发时间更晚，不自动表示所有性能更好。修改同时涉及内容、职责和执行审计，两个分数不能隔离 Delivery 的贡献。

## 最终为什么回到三 Skill

**FACT｜事实：** Main 的选择是 HIGHEST_OBSERVED_MATURE_THREE_SKILL_CEILING，冻结 exact historical v6 的原始身份，没有把后期修复或第四 Skill 混入最终包。[最终方案审阅](../../project/FINAL_SOLUTION_REVIEW.md)

**INTERPRETATION｜解释：** 成熟身份、观测证据与复杂度控制共同提供选择语言；其中“选这个固定历史对象”是事实，“多一层模块增加协调成本”是设计解释。不要把解释升级为已测量的性能损失。

## 判断一个新模块值不值得增加

**TEACHING EXAMPLE｜教学示例：** 假设要新增长期记忆模块，先问：现有流程在哪个窗口丢失了必要事实？模块怎样取得公开新鲜数据？谁能写入？压缩后怎样读回？是否改变规划权？如何检查实际应用？如果这些问题未回答，新增文件只证明架构变复杂。

**INTERPRETATION｜解释：** 在真实工程中，模块边界应跟随可辨认的问题，而不是跟随功能名的吸引力。CareerSim 支持这种职责和证据思路，但没有证明三 Skill 对所有 Agent 都最优。

---

[学习地图](00-学习地图.md) | [上一章](05-从S01到S11整个项目到底做了什么.md) | [下一章](07-为什么一次高分几乎什么都证明不了.md)
