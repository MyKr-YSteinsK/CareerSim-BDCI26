# 11｜为什么最终选择 exact-v6，而不是 v1 或 v8a

最终选择必须回答“交付哪一个确定对象”，而不只是“哪个文件里有最大数字”。本项目选择 exact historical v6（精确历史 v6），同时保留它不是历史最高单局、只有一个完整样本且运行遵循失败的事实。

## 先把比较对象摆齐

**FACT｜事实：** 以下对照保留 canonical review（权威审阅）与 Run 原口径。[最终方案审阅](../../project/FINAL_SOLUTION_REVIEW.md) · [最终证据审查](../../project/FINAL_EVIDENCE_REVIEW.md)

| 比较对象 | quantitative / competition_partial | survival / grade / Level | 身份与限制 |
|---|---|---|---|
| v1 高样本 | 76.04 / 未在本表补填 | 48m / A / L6 | Tier-B 摘要，raw unavailable |
| v1 低样本 | 35.31 / 未在本表补填 | 25m / D / L4 | same-source pair，完整 Instruction 身份不足 |
| exact-v6 | 75.29 / 52.70 | 48m / A / L6 | 三 Skill，一个完整样本；adherence FAIL |
| v8a RUN-0004 | 72.65 / 50.86 | 48m / A / L5 | 四 Skill，同冻结身份样本一 |
| v8a RUN-0002 | 59.00 / 41.30 | 48m / C / L4 | 同冻结身份样本二，非 v6 复验 |

未知字段不填零，不为了表格对称制造新数值。quantitative 与 competition_partial 不能混成一个成绩，也不是 official hidden score（官方隐藏测试成绩）。

~~~text
历史观测
├─ v1：76.04 + 35.31；摘要证据，完整身份不充分
├─ exact-v6：75.29；成熟三 Skill，单样本，adherence FAIL
└─ v8a：72.65 + 59.00；四 Skill，同身份两轨迹
         ↓
Main 选择：固定历史 exact-v6 身份
         ↓
离线 ZIP 冻结；官方上传未执行/未证明；平台结果 UNKNOWN
~~~

图表示一个受限工程决策，不表示数值排名已证明 v6 最优。

## 为什么不能只选 v1 的 76.04

**FACT｜事实：** v1 两条历史记录必须一起出现：76.04 /48m/A/L6 与 35.31 /25m/D/L4。来源为 same-source pair（同来源配对摘要），Tier-B summary（B 级历史摘要），raw unavailable（原始材料不可得）；完整 Instruction/config 身份不充分。[最终证据审查](../../project/FINAL_EVIDENCE_REVIEW.md)

**INTERPRETATION｜解释：** 高样本提供真实历史上界记录，但不能替代低端结果，也不能提供一份完全可恢复、可审计的部署身份。要冻结提交，必须知道实际交付字节与方案职责，而不只是复述历史高分。

这不证明 v1 一定较差，更不证明 exact-v6 稳定性较好。v6 的重复样本缺口仍然存在。最终选择是在证据不足的现实中选择可交付身份，而非给历史所有方案做总体能力排序。

## exact-v6：选择的具体对象

**FACT｜事实：**

- Candidate：**candidate-v6-auditable-control-loop**。
- Runtime source：**1114a04b75548cf52f030d123564e527060fc061**。
- 三 Skill：structured-state-board、rolling-planning、risk-review。
- 完整样本：**75.29 / 52.70 / 48m / A / L6**。
- Promotions（晋升）：**M6 / M12 / M18 / M36 / M48**。
- Gameplay：**VALID_48M_COMPLETION**。
- Adherence：**RUNTIME_ADHERENCE_FAIL**。

来源是 [最终身份](../../project/FINAL_SUBMISSION_IDENTITY.json)、[v6 运行记录](../../project/runs/v6-run1-validation.md) 与 [S06 收口](../../project/S06_CLOSEOUT.md)。

“exact”意味着不把后来更明确的执行文本、v6d fallback（回退方案）或第四 Skill 混进去。后期已知的修复不能倒填进历史 source，让原样本看起来验证了新版。

## 必须正面保留的运行缺陷

**FACT｜事实：** v6 记录和 S06 closeout 支持以下限制：

1. **Energy multi-select schema rejection（Energy 多选结构拒绝）。** 一次非单整数参数在状态改变前失败；203 attempts 中 202 次成功、1 次拒绝。
2. **两次 compression epoch 后没有 Skill reread（技能重读）。** 原报告用 S06-25 recovery definition 审查恢复缺口；后续 v6b 合同才更明确规定恢复重读，不应抹去定义的时间关系。
3. **Ordinary Story deliberation reopened without fresh evidence（普通情节在无新证据时重新权衡）。** 原本已关闭决策仍被重开。
4. **CTRL/action auditability ambiguity（控制标记与动作可审计性不明）。** 418 个形似标记的出现位置不能与 203 attempts 可靠一一配对，缺少可靠 model-turn 绑定。
5. **Missed required checkpoint marker（遗漏必要检查点标记）。** 必要 H 标记遗漏，完整协议不能认证为通过。

这些缺陷不能因最终选择而隐藏，也不能据它们推导确定的分数损失。工具成功、公开状态恢复、标记可解析和语义遵循是不同检查对象。[v6 运行记录](../../project/runs/v6-run1-validation.md)

## 为什么不是后期 v8a

**FACT｜事实：** v8a 为四 Skill Candidate，从 v7o donor core 移植到 v7z shell；两个完整样本保持相同冻结行为身份，分别得到 72.65 /50.86/48m/A/L5 与 59.00 /41.30/48m/C/L4。[v8a 来源](../../skill-evolution/07-v8a-v7o-donor-core-transplant/SOURCE.md) · [样本一](../../project/runs/v8a-full-horizon-sample1.md) · [样本二](../../project/runs/v8a-full-horizon-sample2.md)

**INTERPRETATION｜解释：** 两样本提供比一条轨迹更丰富的描述，但仍不足以估计稳定分布。它们也没有超过 v6 的已记录高位观测；更关键的是，这不是 exact-v6 replication（精确复验），不能用来填补 v6 的重复性缺口。

样本一 CTRL-DL 文本邻接格式未被当前 parser 接受，样本二有空格而可被接受。格式差异没有对应 Candidate 身份变化。不能把解析率当成 Delivery 全程语义应用率，更不能把两个分数的差完全归给格式。[样本记录](../../project/runs/v8a-full-horizon-sample1.md)

## 选择链：哪些是事实，哪些是解释

**FACT｜事实：** Main 的选择标签是 **HIGHEST_OBSERVED_MATURE_THREE_SKILL_CEILING**，决定 **SELECT_EXACT_V6_FOR_SINGLE_SHOT**。后期路线没有足以改变最终方案的安全策略增量，冻结保留原始 runtime identity（运行身份），strategy search（策略搜索）关闭。[最终身份](../../project/FINAL_SUBMISSION_IDENTITY.json) · [最终方案审阅](../../project/FINAL_SOLUTION_REVIEW.md)

**INTERPRETATION｜解释：** 可以把这个取舍组织为：已有观测 → 成熟职责结构 → 审计和身份可复核 → 控制额外复杂度 → 承认小样本不确定性 → 在 Main 冻结窗口交付。

其中，选择对象、成熟三 Skill 标签与冻结状态是来源事实；“控制复杂度减少协调负担”是工程解释，不是本项目测得的分数收益。审计价值也不意味着 v6 遵循已通过。

不能据该决策写 v6 proven optimal（已证明最优）、statistically best（统计最佳）或 expected score=75.29。工程接受是有限证据下的选择，不会自动消除未知。

## Auditability 和 adherence 为什么不能混用

**Auditability（可审计性）** 是能够把声明回溯到身份、事件、输入与结果；**Adherence（运行遵循）** 是这些实际事件是否符合合同。一个缺陷被可靠查出，本身说明某部分证据可审计，却同时说明对应合同没有被遵循。

**INTERPRETATION｜解释：** 因此，“v6 可复核”可以与“v6 adherence FAIL”同时成立。若选择理由包含审计价值，不应把它改写成“运行完全正确”。本项目保留原样本缺陷，正好提供了这个区别。

同样，parser 接受一个 CTRL-DL 组合，说明格式被读懂；要判断 Delivery 是否基于真实交付证据，还需要语义材料。工程选择时可以关心记录是否可解释，但不能用格式齐全代替策略正确。

## 历史 fallback 在选择中是什么位置

**FACT｜事实：** exact-v6d 的三个历史值为 71.67 /65.35/59.67，是 fallback 比较信息，非最终包；这些样本也不是稳定分布证明。[冻结审计](../../project/reviews/S10-23R_FINAL_SINGLE_SHOT_FREEZE.md)

**INTERPRETATION｜解释：** Fallback（回退方案）提供另一个已有对象，不等于当前研究已经证明它风险最低。其“安全”角色是项目语境中的选择定位，不能改成未来必然存活。

最终选 exact-v6 是一次明确身份决策。选用该对象后，不能偷偷替换成 v6d 修复文本再继续沿用 v6 的高分；否则交付的方案与解释成绩的方案不一致。

## 选择之后还有哪些未知

一份完整决策记录应该同时允许两句话成立：交付对象已经明确；性能外推仍不明确。冻结结束的是本轮方案搜索和打包身份，不是把所有研究未知转成事实。

**UNKNOWN｜当前证据不足：** exact-v6 的稳定分布、因果策略贡献、长期遵循和 hidden Test 迁移。选择不是新增样本，包散列也不是性能测量。

**TEACHING EXAMPLE｜教学示例：** 如果有人要求答辩只留“75.29、三 Skill、最终方案”，应补回“单样本、adherence FAIL、无官方评测”。这不是削弱工程工作，而是防止观众误解它已经完成哪些验证。

## 最终包与上传边界

**FACT｜事实：** 唯一冻结包为：

| 字段 | 固定身份 |
|---|---|
| ZIP | FZU-Loss-final-v6.zip |
| Bytes | 18,082 |
| Members | 7 files |
| SHA256 | 31e836b591703dfe520916828da033a57de260bb451d97047bbaee9daaa11b9b |
| Runtime source | 1114a04b75548cf52f030d123564e527060fc061 |
| Official upload | NOT PERFORMED / NOT PROVEN |
| Platform score | UNKNOWN |
| Hidden-test transfer | UNKNOWN |

来源：[最终方案审阅](../../project/FINAL_SOLUTION_REVIEW.md) · [冻结审计](../../project/reviews/S10-23R_FINAL_SINGLE_SHOT_FREEZE.md)。

包构建提交与 runtime source 是不同对象，current checkout 又是另一个对象。当前仓库有四 Skill，不意味着最终 ZIP 有四 Skill；离线校验包成员与散列通过，不意味着比赛平台已接收。

## 如果以后有新证据怎么办

**INTERPRETATION｜解释：** 新证据可以支持新的决策，但不能静默覆盖历史冻结记录。需要明确是否重开路线、是否产生新身份、是否获得运行/提交授权。否则“改进最终包”会破坏原样本与交付对象的一致性。

**TEACHING EXAMPLE｜教学示例：** 复核者问“为什么没有修完所有问题再交付？”准确回答应提到冻结的历史身份和未知收益：修复已知缺陷会产生新行为身份，需要相应证据；本次选择保留成熟历史对象及其限制。不能回答“原版本已经没有问题”。

---

[学习地图](00-学习地图.md) | [上一章](10-Reviewer、Memory、Helper、Controller与Simulator路线.md) | [下一章](12-Anti-overfit、Hidden-Test与不确定性.md)
