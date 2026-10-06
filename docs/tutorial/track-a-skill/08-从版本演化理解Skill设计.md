# 08｜从版本演化理解 Skill 设计

[学习地图](00-学习地图.md) · [上一章：真实案例](07-真实案例、反例与失败模式.md)

本章做 Synthesis（综合）：把不同版本放在一起，理解职责怎样拆分、怎样收束，哪些改变值得尝试，哪些结论仍然不能成立。七篇 GUIDE 分别解释一个历史版本；这里围绕设计问题组织，不逐篇复述，也不把七个代表快照当成连续相邻的七次提交。

**FACT** 的结构变化以[版本索引](../../skill-evolution/00-版本索引.md)、各版 SOURCE / DELTA 与原件为准；运行结论以 canonical evidence（权威证据）为准。**INTERPRETATION** 提供设计解释；可迁移建议单独标明。主线仍是 exact-v6，后继版本用于比较，不能改写它的历史规则。

## 1. 先看“问题发生在哪里”，再看模块数量

| 代表快照与阅读入口 | 直接支持的结构事实｜FACT | 本章关注的设计问题｜INTERPRETATION |
|---|---|---|
| v3c：[GUIDE](../../skill-evolution/01-v3c-zh-aligned-policy/GUIDE.md) / [DELTA](../../skill-evolution/01-v3c-zh-aligned-policy/DELTA.md) | 四 Skill，包含 career-action-trace；是已恢复的配置里程碑，不是最早 Skill 起点 | 动作轨迹怎样与事实整理分工？ |
| v4：[GUIDE](../../skill-evolution/02-v4-lean-runtime-policy/GUIDE.md) / [DELTA](../../skill-evolution/02-v4-lean-runtime-policy/DELTA.md) | 退出 Trace，保留 Board / Planning / Risk；Instruction 与保留模块均改变 | 减模块之后，记录和审查职责如何继续存在？ |
| v5：[GUIDE](../../skill-evolution/03-v5-evidence-driven-phase-policy/GUIDE.md) / [DELTA](../../skill-evolution/03-v5-evidence-driven-phase-policy/DELTA.md) | 仍三 Skill；规则改为更显式的阶段与扫描约束 | 控制顺序能否避免复用旧判断？ |
| v6：[GUIDE](../../skill-evolution/04-v6-auditable-control-loop/GUIDE.md) / [DELTA](../../skill-evolution/04-v6-auditable-control-loop/DELTA.md) | 仍三 Skill；短 Instruction、候选后 Risk、CTRL 闭环 | 怎么让判断有清楚的 owner 与提交边界？ |
| v7：[GUIDE](../../skill-evolution/05-v7-global-trajectory-delivery/GUIDE.md) / [DELTA](../../skill-evolution/05-v7-global-trajectory-delivery/DELTA.md) | 新增 delivery-progress，四 Skill；直接父版本是 v6c | 多步承诺和成果认可应由谁维护？ |
| v7c：[GUIDE](../../skill-evolution/06-v7c-global-decision-policy/GUIDE.md) / [DELTA](../../skill-evolution/06-v7c-global-decision-policy/DELTA.md) | 父版本 v7b；只改 Board / Planning，Delivery / Risk 原字节保留 | 决策优先级能否集中在规划层？ |
| v8a：[GUIDE](../../skill-evolution/07-v8a-v7o-donor-core-transplant/GUIDE.md) / [DELTA](../../skill-evolution/07-v8a-v7o-donor-core-transplant/DELTA.md) | 四模块都改；直接父版本 v7z；采用不同控制语义 | 接口更显式是否真的提高执行与可审计性？ |

表中“问题”是我们的阅读切口，不宣称它就是作者当年的完整动机。尤其 v7、v7c、v8a 的直接父链并非表中上一行；DELTA 的 parent comparison（父版本比较）和本表的 representative comparison（代表版本比较）不能混用。

**INTERPRETATION**：模块数只描述容器。相同三模块可以有完全不同的候选顺序，相同四模块也可以有不同的 CTRL 语义。先识别职责、证据输入与交接，再统计文件个数，才不会把组织方式当成能力本身。

## 2. 为什么 career-action-trace 后来退出？

### 退出事实可以确认，全部动机不能补写

**FACT**：v3c 配置包含 career-action-trace。它要求记录 S02 标记，不自行选择和提交；唯一动作提交者仍是 Agent。v4 配置不再包含它，同时修改了 Instruction 和其他三个 Skill。因此能确认“四模块变三模块”和规则整体变化，不能把全部差异归结为删除一个文件。

**INTERPRETATION**：一个可能的设计解释是，单独的轨迹标记职责与 Board 的近期效果记录、Agent 的动作说明存在接口成本；把必要事实记录留在事实层，有机会减少重复。这个解释符合职责比较，但不等于已经找到明确的历史动机声明，更不等于测得省下多少 token 或提高多少分。

### 删除容器，不应删除必要的信息

如果退出 Trace 后，谁也不保存必要的近期公开效果，那么精简会损害 Planning 的可比依据。exact-v6 Board 仍保留必要近期效果和有限恢复材料；它说明三模块方案并没有把“记得刚才发生什么”全部交给偶然的上下文记忆。

**TEACHING EXAMPLE｜教学示例，不是历史 Run 原始记录。** 假设同一公开动作前后 Output 都是 10，反馈也未更新。正确记录是“本次干净可比前后未见 Output 增长”；错误记录是“已调用动作，所以成果一定增长”。即使没有独立 Trace，事实层仍须提供这条有限、可核查的信息。它也不能独自判定 STALLED，那个严格判断属于 Planning。

### 运行结果不能给精简做因果证明

**FACT**：v4 的已识别运行为 `25.84 / 18.09 / 6m / E / L2`，由健康耗尽自然结束；这是观测结果，不是工具技术失败。[v4 运行取证](../../project/runs/v4-run1-health-forensic.md)没有把它证明为“去掉 Trace 导致失败”。

**INTERPRETATION**：模块、Instruction 和行为规则同时变化，又缺少控制其他条件的比较，无法隔离删 Trace 的作用。正确结论是“该配置有此运行结果”；错误结论是“少一个 Skill 必然更差”或“简化必然更好”。

## 3. 为什么三 Skill 成为最终 v6？

### 三个 owner 足够覆盖这条主线

**FACT**：exact-v6 分工是 Board 拥有新鲜公开事实，Planning 拥有 Gap / Progress / Risk Budget / Horizon 与候选生成，Risk 拥有当前候选审查；Single Agent 统一完成读取、交接、CTRL 和提交。

**INTERPRETATION**：这是一种 Distinct ownership（明确职责归属）。事实需要证明“材料是什么”，目标需要解释“当前补什么”，风险需要判断“这一候选是否触及重大约束”。三类问题既互相依赖，又不宜互相代判。Board 一旦直接填 STALLED，Planning 就丢掉可比条件的责任；Risk 一旦决定未来每季目标，局部门禁就变成第二个规划者。

**TEACHING EXAMPLE｜教学示例，不是历史 Run 原始记录。** 正式反馈指出当前成果不足，健康仍有可用空间。Board 只记录反馈与健康事实；Planning 确定一个成果 Gap，并提出当前合法成长项；Risk 没有发现相关重大风险 cue，quick check 为 PASS。错误的分工是 Risk 因为另一项“更舒服”就改目标，让成长项没有机会被完整理解。安全约束和默认避险目标是两回事。

### 复杂度被收束，并没有被消灭

**FACT**：v6 将全局顺序和提交语法压在五行 Instruction 中，具体职责留在三份 Skill。[02](02-exact-v6-Instruction逐句拆解.md)拆出 28 个条款单元，说明“短”不代表规则少。[06](06-三Skill协同与一次Action闭环.md)也展示了恢复、一次重比、换项再审与 fresh observe 的执行负担。

**INTERPRETATION**：Complexity control（复杂度控制）应关注规则是否各有位置、交接是否能闭合，不能仅看文本行数。若为了少字把 P 的含义省掉，后继版本又用 P 表示不同状态，就会形成语义混淆。版本身份和字段含义需要一起保存。

### 最终选择是有边界的项目决定

**FACT**：[最终方案审阅](../../project/FINAL_SOLUTION_REVIEW.md)与[最终证据审阅](../../project/FINAL_EVIDENCE_REVIEW.md)记录冻结选择为 exact-v6。该局 `75.29 / 52.70 / 48m / A / L6` 有完整 48 月结果，同时为 `RUNTIME_ADHERENCE_FAIL`；一个有效结果与遵循失败可以同时成立。最终选择标签为 `HIGHEST_OBSERVED_MATURE_THREE_SKILL_CEILING`，不能改写为“历史所有版本最高分”。

**INTERPRETATION**：教学可以说“三职责方案在这个冻结决定中被选中”，不能说“三 Skill 已被实验证明是最优数量”。选择还受可恢复身份、成熟形态、执行与证据限制影响，不是用一个数字替所有条件投票。最终包身份、工程 checkout 身份与官方平台验收也是不同事实；这里没有新增比赛上传或平台评价证据。

## 4. 为什么后继版本又加入 delivery-progress？

### 新职责是承诺生命周期

**FACT**：v7 新增 delivery-progress。它跟踪 OPPORTUNITY（机会）、COMMITTED（已承诺）、IN_PROGRESS（进行中）、BLOCKED（受阻）、DELIVERY_CLAIMED（已声称交付）、DELIVERED（已交付）、CLOSED（已关闭）等状态；活跃事项最多三个，已关闭保留一个。声明完成与公开确认完成分开。此处 IN_PROGRESS 指交付事项正在进行，不等于 v6 Planning 的 ADVANCING / STALLED。

**INTERPRETATION**：这解决一种跨动作对象的问题：本次选项可能开启承诺，后续动作推进它，再由公开结果确认。Board 记录“今天公开发生什么”，Planning 决定“现在值得做什么”，Delivery 维护“哪个承诺走到哪一步”。新增模块的合理性在于独立对象与生命周期，不在于“四比三更先进”。

**TEACHING EXAMPLE｜教学示例，不是历史 Run 原始记录。** 当前公开材料显示接受项目承诺，下一次动作完成准备，Agent 在说明里写“已经交付”，但观察尚无交付认可。正确做法是区分已承诺、过程进展和已声称，不把 notes 当成外部确认；错误做法是把声明直接登记为 Delivered，再据此认定长期 Gap 已解决。这是后继 Delivery 的概念示例，不往 exact-v6 塞入一个不存在的第四模块。

### 它不能成为第二个规划者

**INTERPRETATION**：如果 Delivery 因为手上有活跃承诺就强制选择它，忽略新公开反馈与重大约束，那么 owner 又发生重叠。交付状态是 Planning 的输入，不能自动成为最高目标。v7c 将较明确的优先级放在 Board / Planning 的修改里，而 Delivery / Risk 字节保留；这个结构事实有助于理解“改决策顺序不一定要重写全部模块”。它没有附带可归属的 exact-v7c 运行收益。

新增职责还增加需要读取、记住、恢复和审计的材料。这里讨论合同层的负担；安装、加载与具体服务实现属于 Track B｜System / Runtime，将在后续章节解释。

## 5. 为什么更多 Skill 不一定更好？

下面是 **INTERPRETATION / GENERAL ENGINEERING LESSON（一般工程启示）**，不是项目已经测得的通用定律。

| 需要付出的成本 | 具体会怎样出错 | 设计时怎样检查 |
|---|---|---|
| Overlap（职责重叠） | 两模块各自写当前目标，给出不同值 | 同一个结论只指定一个 owner；其他模块提供输入 |
| Context cost（上下文成本） | 文本占用增多，重要规则难以被持续保留 | 保留必要事实与少量状态，解释为何需要每一项 |
| Instruction conflict（指令冲突） | 一处要求独立 CTRL，一处要求塞入 notes | 用同一版本合同解释接口，不拼装不同版规则 |
| Adherence burden（遵循负担） | 读过模块却忘记恢复重读，或只输出标记 | 核查从读取到实际动作的执行链，而非只数文件 |
| Auditability（可审计性） | 有大量字段文字，却缺当次动作配对 | 让记录与候选、状态、尝试建立可核查关系 |

**FACT**：v6 的三模块仍发生恢复重读失败与普通比较重开；其 418 次 CTRL 形状文字也无法认证 203 次动作尝试的一一配对。v8a 的四模块并未让隐藏信息违规消失。这些是特定配置和运行的事实，支持“数量不足以保证遵循”的谨慎结论；不支持“增加模块通常会失败”的总体频率判断。

**TEACHING EXAMPLE｜教学示例，不是历史 Run 原始记录。** 若准备增加一个“晋升检查 Skill”，先问它是否只是重复 Planning 的正式反馈后 reset。若是，应先修清原有职责；若它维护独立的公开申请生命周期，则可能值得新增，但必须定义输入、状态、输出与最终决策者。错误理由是“为了全面，先加一个”，随后再让 Agent 自己协调冲突。

## 6. 为什么 v8a 没有成为最终 submission？

### 它是不同身份，不是 exact-v6 的复刻

**FACT**：v8a 是后继工程配置，包含四 Skill 与不同的接口约束。其 P 使用 Advance / Stabilize 的模式语义，还增加 READY、RB 等控制安排；不能把这些字段移到 v6 的 P=ADVANCING / STALLED / UNKNOWN。v8a 的来源和父链也不等于 v6，仅使用熟悉模块名称并不能证明相同行为。

冻结审阅已经把最终 selection（选择）绑定 exact-v6；工程主线检出 v8a 不会自动改变这个冻结身份。这里的“后继”描述版本演化关系，不宣称它在最终冻结决定之后才首次出现。

### 两个样本须一起读

**FACT**：同一冻结 v8a 行为配置的两次完整样本为：

| 样本与权威来源 | 观测结果 | 此处允许的结论 |
|---|---|---|
| [RUN-0004 / S09-RUN07](../../project/runs/v8a-full-horizon-sample1.md) | `72.65 / 50.86 / 48m / A / L5` | 该次完成并达到这些观测结果 |
| [RUN-0002 / S09-RUN08](../../project/runs/v8a-full-horizon-sample2.md) | `59.00 / 41.30 / 48m / C / L4` | 同一配置另一次结果不同，不能只展示较高样本 |

两次均有隐藏数值进入 notes 的事后违规发现。我们不复述隐藏数值，也不用它们解释当时应如何选择。CTRL / DL 的解析边界与语义认证限制见[07 的 C09](07-真实案例、反例与失败模式.md)，不能把标记覆盖或完成游戏自动当成全部合同通过。

**INTERPRETATION**：两个样本能阻止“只看一局”的选择性叙述，却不足以估计稳定分布或证明 v8a 的因果优劣。同样，v6 的一局也不足以提供稳健统计比较。最终选择保留 exact-v6 是已记录项目决定；教材没有权限凭两局重选最终包，更没有证据把 v8a 宣称为优于 v6 的升级提交。

## 7. 从项目事实到可迁移方法，中间要加一道推理

| 项目证据｜FACT | 可迁移建议｜GENERAL ENGINEERING LESSON | 不能升级为 |
|---|---|---|
| v6 的事实、规划、风险各有规则与权限 | 拆模块前先确定结论 owner 与交接输入 | 所有 Agent 都应固定三个 Skill |
| v4 退出 Trace，保留模块也一起改变 | 减模块时检查必要职责是否仍有人承担 | 删除 Trace 的独立因果收益 |
| v7 新增承诺生命周期职责 | 只有独立对象、状态和证据需求才支持新模块 | 模块越多，长程成绩越高 |
| v6 完成 48 月但遵循失败 | 分别检查配置设计、实际执行与结果 | 高分证明规则全部被执行 |
| v8a 两局结果分歧，仍有违规与未知 | 同身份展示全部样本，单独写限制 | 两样本已足以计算稳定胜率 |
| 后继字段语义改变，最终选择冻结 v6 | 教学、审计和交付须绑定版本身份 | 当前 checkout 自动等于最终包 |

这些建议不是 CareerSim 隐藏机制，也不是新的项目规则。它们是从可核查实例推导的工程思考方法，需要在其他项目里重新验证适用性。

## 8. 毕业练习：判断一个设计提议是否值得执行

**TEACHING EXAMPLE｜教学示例，不是历史 Run 原始记录。** 有人提议：“新增第五个 Skill 专门保守选择，让每次 action 更安全；把所有 CTRL 写进 notes，省一个输出；用最高一局宣布新配置胜出。”

请分别指出职责问题、版本合同问题和证据问题，再写一个不越界的替代提议。

参考分析：专门“总选保守”把安全约束变成默认目标，可能重复 Risk 并抢 Planning 的排序权；exact-v6 明令 CTRL 不入 notes，不能为了省输出改写合同；最高一局不证明稳定收益。可以先说明具体未被现有模块承担的问题、公开证据与交接边界，再提出有身份、有限预算和验收标准的后续研究建议。本 Track 只教如何判断提议，没有执行新增模块或新运行。

回到 [00 的十个问题](00-学习地图.md)：你现在应该能从一个新鲜观察开始，说明每个 owner 的结论、候选何时接受审查、控制行如何对应提交、回执后为什么还要观察；也能在规则、执行和成绩之间保留证据边界。会检查这些关系，比记住某个版本的“高分动作”更接近可迁移的 Agent 设计能力。
