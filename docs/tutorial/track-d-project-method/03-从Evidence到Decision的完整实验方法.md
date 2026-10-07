# 03｜从 Evidence 到 Decision 的完整实验方法

一个实验的价值，不只在于最后有没有高分，还在于它是否消除了一个重要的不确定性。CareerSim 的研发逐渐形成了“先有证据，再提出有边界的假设”的顺序。

## 循环中每一步在做什么

**Evidence（证据）** 是可核对的观测或来源；**Hypothesis（假设）** 是对问题和潜在改进的待验证判断；**Experiment（实验）** 用明确方法检验判断；**Decision（决策）** 决定采用、继续、修改、停止或返回审查；**Implementation（实现）** 把已授权的决策落实成代码或合同。

**FACT｜事实：** 项目用证据、假设、实验和决策组织架构变化，Plan 要冻结范围、权限、所需证据与验收边界；实现细节不明确时交由执行者调查。[实验复盘](../../project/EXPERIMENT_RETROSPECTIVE.md) · [Plan 合同](../../project/CODEX_PLAN_CONTRACT.md)

~~~text
Evidence → Hypothesis → Experiment → Decision → Implementation
    ↑                                              │
    └────────────── New Evidence（新证据）───────────┘

Decision 可以是 ADOPT / CONTINUE / STOP / RETURN_FOR_REVIEW
STOP 不要求先创建一个新的正式 Candidate。
~~~

**INTERPRETATION｜解释：** 这不是要求每个任务按五个标题机械排版。它要求在顺序上分清：问题依据是什么、哪些还是假设、检查实际上做了什么，以及实现获得了多大授权。

## 正向 walkthrough：v6 审计如何转化为 v6b 修复

### 1. Evidence：完成与遵循出现分离

**FACT｜事实：** v6 完整运行有 203 次 action attempts（动作尝试），202 次成功状态改变，1 次参数格式拒绝。成功动作之后都有新观察。另一方面，运行漏掉必要标记，普通 Story（情节决策）在没有新证据时重新 deliberation（权衡），存在 Energy 多选参数问题，CTRL（控制标记）与动作无法可靠一一绑定。[v6 运行记录](../../project/runs/v6-run1-validation.md)

两次压缩 epoch（时期）之后没有重读 Skill 也是记录事实。原报告用 S06-25 的 recovery definition（恢复定义）评估该缺口；该定义与原冻结合同之间的时间关系需要保留，不能把后续更明确的恢复条款倒写成最初已完全定义的合同。

### 2. Hypothesis：先解决可执行的合同缺口

**HYPOTHESIS｜假设：** 如果把动作格式、决策关闭和动作绑定标记写得更明确，能够降低这些类型的协议偏离。该假设只涉及执行正确性；它没有预先承诺改善游戏策略或终局分数。

这个范围有两个好处。首先，问题来自实际轨迹，不是凭“再加一点规则可能有用”展开。其次，修复效果可以用格式和合同检查验证到一部分，无需先假定新局一定表现更好。

### 3. Experiment / Implementation：建立 v6b 静态版本

**FACT｜事实：** S06 closeout 记录 v6b 的静态修复包括 action-linked CTRL、DECISION_CLOSED、Energy 单个整数逐次提交，以及 compression 后的 Skill 恢复重读。它没有重设计策略，也没有新的 runtime validation（运行时验证）。[S06 收口](../../project/S06_CLOSEOUT.md)

因此，这个案例的“正向”含义是：问题得到可追踪的合同修复，并通过当时静态范围的检查。它不表示这套修复已经证明模型全程遵循，更不表示它赢过原 v6。

### 4. Decision：接受有限结果

**FACT｜事实：** Main 对 S06 的接受是 PASS_WITH_KNOWN_RUNTIME_LIMITATION。原 v6 样本的成绩和运行缺陷保持原身份；v6b 的静态状态不继承 v6 的 75.29。[S06 收口](../../project/S06_CLOSEOUT.md)

**INTERPRETATION｜解释：** 这避免了常见“修完 bug 就把旧高分当成新版验证”的归因错误。新的内容需要新的证据，但新证据可以按授权分阶段获得，不需要无界扩大验证。

### 5. New Evidence：还有什么未证明

**UNKNOWN｜当前证据不足：** v6b 在真实长程运行中的遵循率、稳定性和分数效应。这些缺口应该留在结果中，而不是被“静态修复完成”抹去。

这个 walkthrough 教的是如何把失败转成精确工程工作：事实定位问题，假设限定修复，静态验证回答可回答的部分，Main 接受时保留运行限制。

## 负向 walkthrough：Simulator 在比较宏策略之前停止

### 1. Evidence 与问题

**FACT｜事实：** 历史策略挖掘没有形成足够安全的新策略信号。S10-22 转向 prospective（前瞻式）public-only（仅公开信息）Dev 模拟，研究能否用可复现的确定性控制来比较宏策略。[策略挖掘](../../project/research/S10-21_REVIEW_WINDOW_STRATEGY_MINING.md) · [Simulator 研究](../../project/research/S10-22_SIMULATOR_POLICY_SEARCH.md)

### 2. Hypothesis 与必要前提

**HYPOTHESIS｜假设：** 若底层 Story nuisance policy（作为比较基础的情节控制策略）具有足够胜任能力，那么固定种子与公开输入可能帮助比较更上层的策略配置。

这里存在 prerequisite（前提）：基础控制不能频繁提前终止，以致宏策略还没有施展窗口。这个前提不成立时，比较得到的主要是基础语义控制缺陷。

### 3. 冻结 Experiment

**FACT｜事实：** 研究预先冻结 12 个宏配置、Story 规则、种子和停止标准。基线门禁要求至少 8/16 次完整完成；实际仅 B0 基线进入 16-seed 检查。policy（策略）输入不包含最终 score、隐藏计数或未来结果，score 留在 evaluator（评估端）。[Simulator 研究](../../project/research/S10-22_SIMULATOR_POLICY_SEARCH.md)

把门禁写在结果之前，是为了不在看到低分后临时降低合格标准。公开信息边界同时防止模型或脚本用局后答案拟合策略。

### 4. 实际 Evidence

**FACT｜事实：** 16 次基线运行只有 2/16 自然完成 48 个月。速度足够，但冻结语义基线未达到胜任门禁；全部低分/早终局留在记录，没有反复改 Story 规则直到门禁通过。

### 5. Decision = STOP

**FACT｜事实：** 决策是 SIMULATOR_POLICY_SEARCH_NOT_FEASIBLE。macro screening（宏配置筛选）、confirmation（确认）和 planned holdout（计划留出验证）都未执行；128-seed holdout 仍未使用，没有选出宏策略赢家。[Simulator 研究](../../project/research/S10-22_SIMULATOR_POLICY_SEARCH.md)

**INTERPRETATION｜解释：** STOP 是高质量结果，因为它阻止把未经有效比较的宏策略写进正式 Candidate。失败的是当前比较实现的可行性，不是所有宏策略被证明无优势。

## 为什么这两个案例属于同一种方法

| 环节 | v6 → v6b | Simulator |
|---|---|---|
| 起点 | 运行协议缺口 | 历史挖掘信号不足 |
| 待验证判断 | 明确合同能解决一部分缺口 | 胜任基础控制能支持宏比较 |
| 实际证据 | 静态修复与合同检查 | 16 次冻结基线检查 |
| 决策 | 接受有限修复，运行限制保留 | 前提失败，停止后续比较 |
| 没有证明 | 全程遵循、分数收益 | 宏策略优劣、hidden transfer |

正向案例不应夸大，负向案例不应贬低。它们分别把决策推进到证据允许的位置。

## 怎样设计一份有用的实验合同

**INTERPRETATION｜解释：** 在开始前，至少说清问题、现有证据、假设、对象身份、允许干预、观察窗口、判定规则和停止条件。对长程 Agent，还应列明技术失败与 unknown side effect（副作用不明）的处理。

不是检查越多越好。比如当前任务只是文档，运行模型无法帮助证明链接正确；如果要研究安全只读 Reviewer，则机械权限边界是前提，决策质量测试应放在前提之后。

**TEACHING EXAMPLE｜教学示例：** “多加 Reviewer”可以改写为三个问题：它是否能被正式路径注册？是否机械排除动作修改权？在这些前提通过后，独立建议是否修正错误？每个问题有不同证据，不应让第三个问题的吸引力跳过前两个。

## 第三个接缝：Reviewer 为什么先查可部署性

**FACT｜事实：** Reviewer 研究并没有先找模型评审历史决策，再讨论怎样部署。它先查冻结路径的构造、注册、工具继承和权限限制；只读隔离没有成立，因此质量阶段没有开始。[Reviewer 可行性](../../project/research/S10-19R1_SUBAGENT_FEASIBILITY.md)

**INTERPRETATION｜解释：** 这是 experiment dependency（实验依赖）设计。若审查者在正式路径下不能安全存在，隔离实验中即使给出好建议，也不能直接支持该路径部署。先查前提可以节省后续成本，还能避免对无法落地机制产生过强信心。

假如反过来，先盲评得到许多好建议，团队容易为了保住已有成果而放松权限标准。门禁顺序本身能减少这种事后取舍压力，但并不保证后续研究一定正确。

## 把假设写成可反驳的句子

**INTERPRETATION｜解释：** “方案更聪明”缺乏可检查对象。“压缩后，模型在下一次动作前取得新观察并重新读取三个来源 Skill”给出了事件与顺序，能查到发生或未发生。

假设也应包含适用范围。“当前 frozen path 能部署机械只读 Reviewer”在一个路径上可以被否定；“Reviewer 永远没用”范围过大，当前实验没有能力回答。

**TEACHING EXAMPLE｜教学示例：** 从 v6 的证据提出“显式 action-linked marker 会改善可配对性”，适合先检查语法、事件身份与 parser 接口。从同一证据直接提出“这会增加终局成绩”，跨过了多个未验证接缝。后一判断可以保留为更远的假设，不能作为当前修复成功条件。

## 实验中的失败判定不能靠临时愿望

**INTERPRETATION｜解释：** 开始前应明确哪些结果否定前提、哪些使结果无法定论。例如，基础控制自然早终局可以否定预先设定的胜任门禁；输出 pipe（管道）编码损坏可能只说明装置坏了。二者若混算，门禁就不再回答原问题。

**FACT｜事实：** Simulator 先修复 ASCII transport（传输编码）与冷/热初始化差异，再保留政策冻结和 adapter refreeze（适配层再冻结）；最终 16 次有效基线检查没有技术失败，但完成率门禁仍失败。[Simulator 研究](../../project/research/S10-22_SIMULATOR_POLICY_SEARCH.md)

这条时间线很有教学价值：修复装置不应悄悄重写政策来适应 reward。区分 transport repair（传输修复）与 policy change（策略修改），使“门禁失败”仍对应原冻结假设。

## 实验结束时怎样写结论

结论应包含实际通过的层次、结果适用范围、未运行的条件阶段和剩余未知。“零调用”可以是本任务计数，但不能写成某工具实测零延迟、零成本；没有测量的能力应写 NOT_MEASURED（未测量）。

**INTERPRETATION｜解释：** 最终实现是决策的后果，不能替代决策依据。一份漂亮代码、一份完整报告或一个高分，都只有回到明确问题之后，才知道其研究价值。

---

[学习地图](00-学习地图.md) | [上一章](02-Candidate、Run、Experiment到底有什么区别.md) | [下一章](04-Static、Runtime、Gameplay与Adherence多层验证.md)
