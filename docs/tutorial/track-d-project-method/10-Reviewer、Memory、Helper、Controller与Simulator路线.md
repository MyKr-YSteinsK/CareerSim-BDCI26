# 10｜Reviewer、Memory、Helper、Controller 与 Simulator 路线

当局部 Prompt 加固没有稳定突破时，研发需要检查替代机制。但“框架提供某功能”到“它可安全改善正式 Candidate”，中间有部署、输入、遵循与收益门禁。

本章把 S10 路线当作 Research Portfolio（研究组合）理解。路线的名字不决定结果类型，各自到达的证据层次才决定如何表述。

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

**FACT｜事实：** S10-19R3 检查了 Todo（待办）、模型设置组装和固定 helper 执行边界。隔离真实工具调用能够处理公开输入与本地状态；结果 **DETERMINISTIC_HELPER_CHALLENGER_SUPPORTED**。这是 isolated tool-level support，没有正式 Candidate 部署、模型调用或长程遵循证明。[Helper 审计](../../project/research/S10-19R3_NATIVE_CONTROL_SURFACE_AUDIT.md)

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

**FACT｜事实：** S10-22 构建 public-only deterministic Dev evaluator（仅公开信息的确定性开发评估器）。12 个宏配置被冻结，实际只测 B0 基线；基础 Story 门禁至少 8/16 完成，实际 2/16。结论 **SIMULATOR_POLICY_SEARCH_NOT_FEASIBLE**。[Simulator 研究](../../project/research/S10-22_SIMULATOR_POLICY_SEARCH.md)

Screening、confirmation、128-seed holdout 没有运行。技术接口可用、计算速度足够，但基础语义控制不胜任。**Feasibility failure（可行性失败）不等于 macro policy proven bad（宏策略被证明差）。**

**INTERPRETATION｜解释：** 一个比较装置必须能让待比较因素有效发挥作用。基础控制频繁早终局时，结果主要受基础缺陷影响。此时更快地跑更多宏配置，可能更快得到无意义排名。

## Team / Swarm：没有测试，就保持没有测试

**FACT｜事实：** Team / Swarm 为 **DEFERRED / NOT_TESTED**。项目没有建立“多 Agent 已测试而失败”的结论。[架构复盘](../../project/ARCHITECTURE_RETROSPECTIVE.md) · [当前状态](../../project/CURRENT_STATE.md)

**INTERPRETATION｜解释：** 增加 Agent 会引入动作所有权、状态同步、权限和上下文协调问题。单 Agent 项目先保留这条路线，是范围与证据选择，不能推成多 Agent 普遍不可行。

## Human Play Lab：独立人类研究路线

**FACT｜事实：** HPL（Human Play Lab，人工对局实验室）属于独立 research branch（研究分支）research/human-play-lab。人工选择可见 action，客户端直接使用 CareerSim simulator/GameEngine，绕过正式 Runner/MCP/JiuwenSwarm 控制路径。[HPL 实现教学](../track-c-repository-tooling/10-Human-Play-Lab是怎么实现的.md) · [架构决策](../../project/ARCHITECTURE_DECISIONS.md)

实现核对限定在历史提交 **860941575bfc8a8c282e69b0af20d343dd87c027** 的 **hpl_client/game_adapter.py** 与 **hpl_client/controller.py**：前者的 act 接收合法整数、调用 engine.take_action 后取得新 observe；后者的 choose 检查当前 revision/run_id 再提交人工选择。这里没有重开 HPL，也没有扩大读取该分支其他历史。

它可以提供公开选择、状态轨迹和研究假设，不能作为正式 Agent Candidate 的 adherence 对照；人工玩家没有经历相同模型控制与恢复链。当前 **CLOSED_BY_USER**；**UNKNOWN｜当前证据不足：** canonical source 未记录具体关闭原因。[当前状态](../../project/CURRENT_STATE.md)

不能写成用户认为它没价值、太慢或表现差。关闭状态不替你提供关闭原因。

## 这些门禁之间不是一条“功能失败排行榜”

**INTERPRETATION｜解释：** Reviewer 问权限是否允许安全存在，Memory 问正文是否进入指定上下文，Helper 问工具是否能可靠读写，Controller 问这种机制能否修正决策。它们的输入、成功标准和实际测试深度不同。

如果把 Memory 的自动注入失败和 Controller 的逻辑信号弱都写成“记忆不好”，下一次研究会失去定位：需要修上下文组装，还是修语义解释？如果把 Helper 支持当成 Controller 已成功，又会忽略工具层到决策层的接缝。

这也是为什么路线名字不应成为结论。一个同名机制可以换加载路径、输入接缝或控制权，形成另一个研究对象。原结论仍然保留，但不能不经新检查就转移。

## 输入语义为什么是确定性工具的难点

确定性工具可以保证同一合法输入走同一算法，却不能保证输入反映现实。“当前警告仍然约束这个动作”与“历史上出现过警告”是不同语义；“工作得到赞许”与“事项已验证交付”也不同。

**FACT｜事实：** Controller 报告承认语义注释未被机械核验为最新回执事实，confidence（置信标签）也不是硬语义安全过滤。它验证了状态连续性，不等于验证了每个标签准确。[Controller 研究](../../project/research/S10-20_PROMOTION_WINDOW_CONTROLLER.md)

**INTERPRETATION｜解释：** 因此，想把模型判断交给脚本，不能只问脚本是否确定，还要问事实由谁确认、标签由谁生成、缺失语义怎样保留 UNKNOWN。程序越坚决执行错误标签，错误可能越稳定。

## HPL 能给研究什么，不能给什么

人工路线可以让研究者看到自己如何理解菜单，提出公开机制假设，或者检查界面与状态的展示。它不包含正式模型的加载、压缩、工具格式与持续性约束。

**INTERPRETATION｜解释：** 比较人类与 Agent 时，需要承认控制路径和决策成本不同。一个人类在某状态下做出另一选择，可以成为讨论案例，不能直接成为 Agent 策略收益的受控证据。

**FACT｜事实：** HPL 的公开 journal/frames、run metadata 与 exports，以及本地 DB/log/staging，随阶段有所不同；本书不把其中任一研究输出当成正式 Candidate Run。实现细节见 [Track C HPL](../track-c-repository-tooling/10-Human-Play-Lab是怎么实现的.md)，后来的主线状态仍为 CLOSED_BY_USER，原因 UNKNOWN。

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

---

[学习地图](00-学习地图.md) | [上一章](09-失败实验与负结果为什么值得保留.md) | [下一章](11-为什么最终选择exact-v6而不是v1或v8a.md)
