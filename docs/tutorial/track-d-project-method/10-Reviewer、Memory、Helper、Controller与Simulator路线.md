# 10｜Reviewer、Memory、Helper、Controller 与 Simulator 路线

[统一入口与术语](../00-从这里开始.md) · [本 Track 阅读路线](01-为什么这个比赛不能靠反复改Prompt试分.md)

当局部 Prompt 加固没有稳定突破时，研发需要检查替代机制。但“框架提供某功能”到“它可安全改善正式 Candidate”，中间有部署、输入、遵循与收益门禁。

本章把 S10 路线当作 Research Portfolio（研究组合）理解。路线的名字不决定结果类型，各自到达的证据层次才决定如何表述。

读 [D03](03-实验方法与多层验证.md) 的循环、[负结果分类](08-Forensics、失败实验与负证据.md#给结果分类并保留停止理由) 的分类后，可按路线跳读。本章是八条替代路线的详细结论入口；每条查问题、测试范围、结果、非结论与停止/延后状态。

## Reviewer：独立意见之前，先有权限边界

**HYPOTHESIS｜假设：** 独立 Reviewer（审查者）可能指出主 Agent 遗漏的选择或风险。要采用这种机制，先要保证它只给建议，不拥有游戏修改权。

**FACT｜事实：** S10-19R1 在冻结 official mode=agent 路径检查注册与继承逻辑。verification factory 存在，但实际配置没有安全注册的只读 reviewer；general-purpose 子代理继承工具/提示等结构，机械排除 CareerSim mutation（游戏修改）未被建立。Prompt 里一句“不要行动”不能代替权限隔离。[Reviewer 研究](../../project/research/S10-19R1_SUBAGENT_FEASIBILITY.md)

结果 **REVIEWER_NOT_SAFELY_DEPLOYABLE** 只针对 tested frozen path（已测试的冻结路径）。Phase B/C 没有运行：没有审查者建议、盲评质量、实际延迟或 token 开销数据。

**INTERPRETATION｜解释：** 这是安全部署门禁结果。不能推导“第二意见没有价值”，也不能把 SDK（软件开发接口）里可构造对象当成比赛安装器可交付的功能。若需要修改 adapter/config/loader（适配层/配置/加载器），那是新的授权范围。

## Memory：会读文件，与自动锚点可用不同

**HYPOTHESIS｜假设：** 一个可靠自动记忆锚点，可能帮助恢复当前局公开状态并减轻压缩后的漂移。

**FACT｜事实：** S10-19R2 在隔离 harness（测试装置）中证明真实 registry（注册表）与 explicit read（显式读取）能力工作，读取到了最新 MEMORY.md marker。但指定 automatic MEMORY.md anchor（自动记忆锚点）正文没有进入被测试的启动、更新和模拟压缩系统捕获路径；usage guidance（使用指引）与 daily memory（日常记忆）路径不是同一对象。[Memory 研究](../../project/research/S10-19R2_MEMORY_FEASIBILITY.md)

结果 **MEMORY_NOT_DEPLOYABLE** 限定指定自动锚点。**Explicit read worked（显式读取成功）必须同时保留。** Shared service 的实际挂载/权限、模型行为与分数效果未测量。

**INTERPRETATION｜解释：** 存储文件、工具读取和自动进入模型上下文是三个接口问题。若把它们合并，压缩恢复会被“磁盘上还有文件”误导。其他显式读取或未来不同记忆设计没有被本研究普遍否定。

## Deterministic Helper：工具层支持，不是 Candidate 收益

**FACT｜事实：** S10-19R3 检查了 Todo（待办）、模型设置组装和固定 helper 执行边界。隔离真实工具调用能够处理公开输入与本地状态；结果 **DETERMINISTIC_HELPER_CHALLENGER_SUPPORTED**。这是 isolated tool-level support，没有正式 Candidate 部署、模型调用或长程遵循证明。支持信号没有自动扩大到这些后续阶段。[Helper 审计](../../project/research/S10-19R3_NATIVE_CONTROL_SURFACE_AUDIT.md)

同一报告也发现默认 Todo callback（回调）不会自动注入当前待办正文。工具 CRUD（创建、读取、更新、删除）工作，不能推出它是可靠自动锚点。

**INTERPRETATION｜解释：** Helper 支持信号回答“可以实现某种确定性工具机制”，下一问题才是“它是否收到正确新鲜输入，以及模型是否按结果执行”。把工具正确性直接当成策略正确性，会跳过最困难的语义部分。

## Replay Controller：记得住，不代表选得对

**FACT｜事实：** S10-20 以公开 observe envelope（观察信封）和有限语义注释构造确定性 Controller。24 个 replay scenarios（回放场景）=12 Dev +12 holdout，只有一个 state-level correction，8 个 UNKNOWN。决策 **CONTROLLER_LOGIC_SIGNAL_WEAK**，回放门禁 **NOT_PROMISING**；Provider 阶段跳过，不创建 v15。[Controller 研究](../../project/research/S10-20_PROMOTION_WINDOW_CONTROLLER.md)

24 场景之外的 41 checks（检查项）不是 41 个独立案例。fixture tool（装置工具）状态持续性通过，也不是模型 runtime adherence 通过。

**INTERPRETATION｜解释：** 主要难点在注释是否正确描述警告当前约束、交付成熟度和机会，而不只是状态有没有保存。持续保存一个旧警告，可能压住成长，却没有证明修复仍必要。

未来模型/正式输入集成还需要 freshness provenance（新鲜度来源链）。这个报告没有把用户提供的数值新鲜度自动变成“来自最新工具回执”的证据。

## Strategy Mining：观察关联，不能强行提炼规则

**FACT｜事实：** S10-21 使用 14 个 accepted runs（已接受运行）和 96 个 formal Reviews（正式评审）；完成窗口是 13 个 Run 中的 82 个，35 promoted（晋升）、47 not promoted（未晋升）。结果 **STRATEGY_SIGNAL_WEAK**，没有安全新 delta（改动）。[策略挖掘](../../project/research/S10-21_REVIEW_WINDOW_STRATEGY_MINING.md)

分母对应不同分析对象，不能用 96 与 82 随意替换。v1 Tier-B 摘要也不能伪装成该挖掘的 action-level（动作层）输入。

**INTERPRETATION｜解释：** 窗口之间的 Level、tenure、机会、资源与既往风险不同。晋升更多可能是起始条件更有利；同一 Run 的窗口还共享历史。它们不能被当成大量独立随机实验。

挖掘仍可生成假设，例如哪些公开机制需要更仔细观察，但不足以产生“永远偏好某个 Energy 家族”的部署规则。

## Simulator Policy Search：前提失败，比较没有开始

**FACT｜事实**：[S10-22](../../project/research/S10-22_SIMULATOR_POLICY_SEARCH.md) 冻结 12 个宏配置，实际只测 B0 基线。Story 胜任门禁为至少 8/16 完成，实际 2/16，结论 `SIMULATOR_POLICY_SEARCH_NOT_FEASIBLE`；screening、confirmation 与 128-seed holdout 未执行。

技术接口可用、速度足够不等于基础语义胜任。这里停止后续宏比较，保留 **feasibility failure（可行性失败）**，不能说宏策略已被证明差。实验从假设到 STOP 的完整过程见 [D03](03-实验方法与多层验证.md)。

## Team / Swarm：没有测试，就保持没有测试

**FACT｜事实：** Team / Swarm 为 **DEFERRED / NOT_TESTED**。项目没有建立“多 Agent 已测试而失败”的结论。[架构复盘](../../project/ARCHITECTURE_RETROSPECTIVE.md) · [当前状态](../../project/CURRENT_STATE.md)

**INTERPRETATION｜解释：** 增加 Agent 会引入动作所有权、状态同步、权限和上下文协调问题。单 Agent 项目先保留这条路线，是范围与证据选择，不能推成多 Agent 普遍不可行。

## Human Play Lab：独立人类研究路线

**FACT｜事实**：Human Play Lab（人工对局实验室）位于 `research/human-play-lab`，人工选择公开菜单，客户端直接调用 simulator/GameEngine，绕过正式 Runner/MCP/JiuwenSwarm。它提供人类研究轨迹与假设，没有正式模型的加载、压缩和遵循链，不能充当 Candidate 对照。[架构决策](../../project/ARCHITECTURE_DECISIONS.md)

**FACT｜事实**：当前 `CLOSED_BY_USER`；**UNKNOWN｜当前证据不足**：关闭原因未被 canonical source 记录，不能推为效果差或没有价值。[CURRENT_STATE](../../project/CURRENT_STATE.md)

历史实现身份、revision/run_id 检查、choice 提交与输出材料集中在 [C10](../track-c-repository-tooling/10-Human-Play-Lab是怎么实现的.md)，这里仅说明它在研究组合中的独立位置。

## 这些门禁之间不是一条“功能失败排行榜”

各路线测的是权限隔离、上下文组装、工具读写或语义排序；输入、成功标准和执行阶段不同。不能用“用了/没用”给机制排优劣，也不能把隔离工具支持移写为正式 Candidate 已成功。门禁顺序的完整教学见 [D03](03-实验方法与多层验证.md)，分类见 [负结果分类](08-Forensics、失败实验与负证据.md#给结果分类并保留停止理由)。

## 输入语义为什么是确定性工具的难点

确定性工具可以保证同一合法输入走同一算法，却不能保证输入反映现实。“当前警告仍然约束这个动作”与“历史上出现过警告”是不同语义；“工作得到赞许”与“事项已验证交付”也不同。

**FACT｜事实：** Controller 报告承认语义注释未被机械核验为最新回执事实，confidence（置信标签）也不是硬语义安全过滤。它验证了状态连续性，不等于验证了每个标签准确。[Controller 研究](../../project/research/S10-20_PROMOTION_WINDOW_CONTROLLER.md)

**INTERPRETATION｜解释：** 因此，想把模型判断交给脚本，不能只问脚本是否确定，还要问事实由谁确认、标签由谁生成、缺失语义怎样保留 UNKNOWN。程序越坚决执行错误标签，错误可能越稳定。

## HPL 能给研究什么，不能给什么

HPL 的 journal/frames、metadata/exports 和本地 DB/log/staging 因阶段不同而异，具体机制见 [C10](../track-c-repository-tooling/10-Human-Play-Lab是怎么实现的.md)。这些材料可供提出公开机制问题，不能转换为正式模型 runtime adherence 证据；`CLOSED_BY_USER` 的原因仍 UNKNOWN。

## 把所有路线放回证据层次

| 路线 | 到达的主要层次 | 决策改变了什么 |
|---|---|---|
| Reviewer | 安全部署前提检查 | 不进入判断质量阶段 |
| Memory | 隔离自动锚点/显式读取检查 | 指定锚点不可部署，其他设计未否定 |
| Helper | 隔离工具层 | 允许提出 challenger 方向，尚未正式部署 |
| Controller | 有界回放逻辑门禁 | 信号不足，不创建新 Candidate |
| Mining | 历史描述性分析 | 无安全新策略增量 |
| Simulator | 基础胜任门禁 | 停止宏比较 |
| Team / Swarm | 未测试 | 继续保留未测试 |
| HPL | 人类独立研究 | 用户关闭，原因未知 |

**INTERPRETATION｜解释：** 一份研究组合不应只按“用了/没用”判断价值。它应告诉下一位研发者：哪个前提失败，哪个机制有支持，哪里仍有语义缺口，以及重新打开路线需要什么新证据。
