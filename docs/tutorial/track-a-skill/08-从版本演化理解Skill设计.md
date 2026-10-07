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

**FACT**：v3c 包含只记录 S02 标记、不自行选择或提交的 Trace；v4 移除它，同时修改 Instruction 和其余三 Skill。退出事实可确认，全部动机不能补写。

**INTERPRETATION**：将必要轨迹留在事实层可能减少重复接口，但没有证据测得节省 token 或增加分数。容器变少与职责变清楚是两个判断。

### 删除容器，不应删除必要的信息

exact-v6 Board 仍保留近期公开效果和有限恢复材料，说明退出 Trace 没有取消近期事实责任。

**TEACHING EXAMPLE｜教学示例**：同动作前后 Output 都为 10，只能记录“干净可比窗口未见增长”，不能因动作被调用就声称成果增长。事实层也不能代填 STALLED，严格条件由 Planning 判断。

### 运行结果不能给精简做因果证明

**FACT**：[v4 取证](../../project/runs/v4-run1-health-forensic.md) 记录 `25.84 / 18.09 / 6m / E / L2` 的健康耗尽自然终局。多项合同同时改变，没有证明“删 Trace 导致失败”；架构干预的混杂解释见 [D06](../track-d-project-method/06-从最小Skill到最终多Skill架构是怎样演化的.md)。

## 3. 为什么三 Skill 成为最终 v6？

### 三个 owner 足够覆盖这条主线

**FACT**：Board 拥有新鲜事实，Planning 拥有 Gap/Progress/预算/Horizon 与候选，Risk 审查当前候选，Single Agent 完成交接与提交。

**TEACHING EXAMPLE｜教学示例**：反馈指出成果不足而健康仍有空间。Board 记录事实，Planning 提出成长项，Risk 无相关重大线索则 PASS；若 Risk 只因另一项更舒服就改目标，它成为第二规划者。明确 owner（责任方）防的是这种代判，完整闭环见 [A06](06-三Skill协同与一次Action闭环.md)。

### 复杂度被收束，并没有被消灭

**FACT**：五行 Instruction 仍可拆成 [A02 的 28 个条款](02-exact-v6-Instruction逐句拆解.md)。**INTERPRETATION**：复杂度控制看交接与语义，不能只看行数；P 等字段必须绑定版本，省字不能牺牲含义。

### 最终选择是有边界的项目决定

**FACT**：[最终方案审阅](../../project/FINAL_SOLUTION_REVIEW.md)与[最终证据审阅](../../project/FINAL_EVIDENCE_REVIEW.md)将冻结身份绑定 exact-v6；唯一完整样本为 `75.29 / 52.70 / 48m / A / L6`，同时 `RUNTIME_ADHERENCE_FAIL`。选择标签 `HIGHEST_OBSERVED_MATURE_THREE_SKILL_CEILING` 不等于全部历史最高分。

**INTERPRETATION**：三职责在这项工程选择中被采用，没有证明三 Skill 是最优数量。本章继续讨论职责边界；有限证据下为何选择它见[D11](../track-d-project-method/11-为什么最终选择exact-v6而不是v1或v8a.md)，精确工件与上传边界见[最终交付报告](../../final-report/04-最终方案、候选选择与工程交付.md)。

## 4. 为什么后继版本又加入 delivery-progress？

### 新职责是承诺生命周期

**FACT**：v7 新增 Delivery，维护 OPPORTUNITY、COMMITTED、IN_PROGRESS、BLOCKED、DELIVERY_CLAIMED、DELIVERED、CLOSED；最多三个活跃项和一个已关闭项。IN_PROGRESS 是事项状态，不是 v6 Planning 的进展分类。

**INTERPRETATION**：独立对象是跨动作的承诺及其公开证据：Board 记当下事实，Planning 决定现在做什么，Delivery 记承诺走到哪一步。

**TEACHING EXAMPLE｜教学示例**：接受承诺、完成准备、notes 声称交付是三个事件；缺公开确认就不能登记 Delivered。这个后继例子不向 exact-v6 添加第四模块。完整状态细节查 [v7 GUIDE](../../skill-evolution/05-v7-global-trajectory-delivery/GUIDE.md)。

### 它不能成为第二个规划者

**INTERPRETATION**：交付状态是 Planning 输入，不能因仍有活跃承诺就强制它优先。**FACT**：v7c 只改 Board/Planning，Delivery/Risk 字节保留，说明优先级变化不必重写全部模块；没有可归属的 exact-v7c 完整收益证据。

新增职责还需加载、记忆、恢复与审计；运行交接读 [Track B](../track-b-system-runtime/00-学习地图.md)，未测量的成本和收益不能写成事实。

## 5. 为什么更多 Skill 不一定更好？

下面是 **INTERPRETATION / GENERAL ENGINEERING LESSON（一般工程启示）**，不是项目已经测得的通用定律。

| 需要付出的成本 | 具体会怎样出错 | 设计时怎样检查 |
|---|---|---|
| Overlap（职责重叠） | 两模块各自写当前目标，给出不同值 | 同一个结论只指定一个 owner；其他模块提供输入 |
| Context cost（上下文成本） | 文本占用增多，重要规则难以被持续保留 | 保留必要事实与少量状态，解释为何需要每一项 |
| Instruction conflict（指令冲突） | 一处要求独立 CTRL，一处要求塞入 notes | 用同一版本合同解释接口，不拼装不同版规则 |
| Adherence burden（遵循负担） | 读过模块却忘记恢复重读，或只输出标记 | 核查从读取到实际动作的执行链，而非只数文件 |
| Auditability（可审计性） | 有大量字段文字，却缺当次动作配对 | 让记录与候选、状态、尝试建立可核查关系 |

**FACT**：v6 三模块仍有恢复重读失败与普通比较重开，v8a 四模块仍有隐藏信息违规。它们支持“数量不足以保证遵循”，不支持“增加模块通常会失败”的频率判断。具体反例见[07](07-真实案例、反例与失败模式.md)，标记配对的调查过程见[D08](../track-d-project-method/08-Forensics为什么成为项目的重要部分.md)。

**TEACHING EXAMPLE｜教学示例，不是历史 Run 原始记录。** 若准备增加一个“晋升检查 Skill”，先问它是否只是重复 Planning 的正式反馈后 reset。若是，应先修清原有职责；若它维护独立的公开申请生命周期，则可能值得新增，但必须定义输入、状态、输出与最终决策者。错误理由是“为了全面，先加一个”，随后再让 Agent 自己协调冲突。

## 6. 为什么 v8a 没有成为最终 submission？

### 它是不同身份，不是 exact-v6 的复刻

**FACT**：v8a 四 Skill 的 P 是 Advance/Stabilize 模式，另有 READY/RB；v6 P 是 ADVANCING/STALLED/UNKNOWN，不能拼接。父链与原件身份见上表 GUIDE/DELTA。当前 v8a checkout 不改变历史 exact-v6 的冻结选择，“后继”不表示它首次出现于冻结之后。

### 两个样本须一起读

**FACT**：同一冻结 v8a 行为身份的[RUN07](../../project/runs/v8a-full-horizon-sample1.md)与[RUN08](../../project/runs/v8a-full-horizon-sample2.md)量化分为 72.65 / 59.00；两局均有证据纪律限制，不能只留下高局。它们不是 v6 的复验，也不能因四模块比分较低就认定第四个模块是原因。

**INTERPRETATION**：设计比较要绑定版本语义；效果比较还要处理样本与混杂。完整样本推理见[D07](../track-d-project-method/07-为什么一次高分几乎什么都证明不了.md)，架构变化作为多变量干预见[D06](../track-d-project-method/06-从最小Skill到最终多Skill架构是怎样演化的.md)，最终选择理由见[D11](../track-d-project-method/11-为什么最终选择exact-v6而不是v1或v8a.md)。本章不据这两局重选提交包。

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
