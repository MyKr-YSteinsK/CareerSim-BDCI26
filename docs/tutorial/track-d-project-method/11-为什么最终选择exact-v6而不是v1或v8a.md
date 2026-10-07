# 11｜为什么最终选择 exact-v6，而不是 v1 或 v8a

最终选择必须回答“交付哪一个确定对象”，而不只是“哪个文件里有最大数字”。本项目选择 exact historical v6（精确历史 v6），同时保留它不是历史最高单局、只有一个完整样本且运行遵循失败的事实。

先读 [D07](07-为什么一次高分几乎什么都证明不了.md) 的小样本限制。本章负责选择理由与保留的运行缺陷；精确包字段及交付合同集中在 [最终报告 04](../../final-report/04-最终方案、候选选择与工程交付.md)。

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

**FACT｜事实**：上表的 v1 pair 来自 same-source Tier-B summary，raw unavailable，完整 Instruction/config 身份不足。[最终证据审查](../../project/FINAL_EVIDENCE_REVIEW.md)

**INTERPRETATION｜解释**：只展示 76.04 会删掉 35.31 这一低端结果，也未提供足够的可恢复交付身份。最终选择必须回答交付字节与职责，不能只选峰值；这仍不证明 v1 更差或 v6 更稳定。小样本推理集中在 [D07](07-为什么一次高分几乎什么都证明不了.md)。

## exact-v6：选择的具体对象

**FACT｜事实**：`candidate-v6-auditable-control-loop`，runtime source `1114a04b75548cf52f030d123564e527060fc061`，三 Skill 为 Board/Planning/Risk。上表的唯一完整样本晋升在 M6/M12/M18/M36/M48，分类同时为 **VALID_48M_COMPLETION** 与 **RUNTIME_ADHERENCE_FAIL**。

来源：[最终身份](../../project/FINAL_SUBMISSION_IDENTITY.json)、[v6 记录](../../project/runs/v6-run1-validation.md)、[S06 收口](../../project/S06_CLOSEOUT.md)。exact 表示保留该历史身份，不混入后期补丁、fallback 或第四 Skill；后来的修复不能继承原样本验证。

## 必须正面保留的运行缺陷

**FACT｜事实：** v6 记录和 S06 closeout 支持以下限制：

1. **Energy multi-select schema rejection（Energy 多选结构拒绝）。** 一次非单整数参数在状态改变前失败；203 attempts 中 202 次成功、1 次拒绝。
2. **两次 compression epoch 后没有 Skill reread（技能重读）。** 原报告用 S06-25 recovery definition 审查恢复缺口；后续 v6b 合同才更明确规定恢复重读，不应抹去定义的时间关系。
3. **Ordinary Story deliberation reopened without fresh evidence（普通情节在无新证据时重新权衡）。** 原本已关闭决策仍被重开。
4. **CTRL/action auditability ambiguity（控制标记与动作可审计性不明）。** 418 个形似标记的出现位置不能与 203 attempts 可靠一一配对，缺少可靠 model-turn 绑定。
5. **Missed required checkpoint marker（遗漏必要检查点标记）。** 必要 H 标记遗漏，完整协议不能认证为通过。

这些缺陷不能因最终选择而隐藏，也不能据它们推导确定的分数损失。工具成功、公开状态恢复、标记可解析和语义遵循是不同检查对象。[v6 运行记录](../../project/runs/v6-run1-validation.md)

## 为什么不是后期 v8a

**FACT｜事实**：v8a 为 v7o donor core + v7z shell 的四 Skill 身份；[RUN-0004](../../project/runs/v8a-full-horizon-sample1.md) 与 [RUN-0002](../../project/runs/v8a-full-horizon-sample2.md) 两个完整样本保持相同冻结行为，数据见上表。[SOURCE](../../skill-evolution/07-v8a-v7o-donor-core-transplant/SOURCE.md)

**INTERPRETATION｜解释**：两轨迹增加描述信息，却未超过 v6 的已记录高位，也没有提供稳定优劣或 exact-v6 replication。CTRL-DL 邻接/空格格式造成不同 parser 接受情况，不代表身份变化、Delivery 语义应用率或分差因果。样本边界见 D07，解析/行为区别见 [D08](08-Forensics为什么成为项目的重要部分.md)。

## 选择链：哪些是事实，哪些是解释

**FACT｜事实：** Main 的选择标签是 **HIGHEST_OBSERVED_MATURE_THREE_SKILL_CEILING**，决定 **SELECT_EXACT_V6_FOR_SINGLE_SHOT**。后期路线没有足以改变最终方案的安全策略增量，冻结保留原始 runtime identity（运行身份），strategy search（策略搜索）关闭。[最终身份](../../project/FINAL_SUBMISSION_IDENTITY.json) · [最终方案审阅](../../project/FINAL_SOLUTION_REVIEW.md)

**INTERPRETATION｜解释：** 可以把这个取舍组织为：已有观测 → 成熟职责结构 → 审计和身份可复核 → 控制额外复杂度 → 承认小样本不确定性 → 在 Main 冻结窗口交付。

其中，选择对象、成熟三 Skill 标签与冻结状态是来源事实；“控制复杂度减少协调负担”是工程解释，不是本项目测得的分数收益。审计价值也不意味着 v6 遵循已通过。

不能据该决策写 v6 proven optimal（已证明最优）、statistically best（统计最佳）或 expected score=75.29。工程接受是有限证据下的选择，不会自动消除未知。

## Auditability 和 adherence 为什么不能混用

**Auditability（可审计性）** 让声明回到身份与事件；**Adherence（运行遵循）** 检查事件是否符合合同。因此可复核的缺陷同时支持“证据可审”和“行为 FAIL”，不能把选择中的审计价值写成完全遵循。parser 读懂格式也不证明交付语义，取证过程见 D08。

## 历史 fallback 在选择中是什么位置

**FACT｜事实**：exact-v6d 是历史 fallback，非最终包，[冻结审计](../../project/reviews/S10-23R_FINAL_SINGLE_SHOT_FREEZE.md) 保留比较证据。具体对照查 [最终报告 04](../../final-report/04-最终方案、候选选择与工程交付.md)。

**INTERPRETATION｜解释**：回退定位不证明风险最低或未来必然存活。不能把其修复文本混入 exact-v6 后，继续归属原 v6 的成绩；选择与交付必须对应同一行为身份。

## 选择之后还有哪些未知

**UNKNOWN｜当前证据不足**：exact-v6 的稳定分布、因果贡献、长程遵循和 hidden Test 迁移。选择和 hash 都不增加样本；任何简述都要连同单样本、adherence FAIL 和无官方评测一起表达。

## 最终包与上传边界

**FACT｜事实**：冻结包为 `FZU-Loss-final-v6.zip`；完整 bytes、members、SHA-256、source/build 身份与合同统一查 [最终报告 04](../../final-report/04-最终方案、候选选择与工程交付.md)，权威来源是 [最终方案审阅](../../project/FINAL_SOLUTION_REVIEW.md) 与 [冻结审计](../../project/reviews/S10-23R_FINAL_SINGLE_SHOT_FREEZE.md)。

**Official upload = NOT PERFORMED / NOT PROVEN；platform score = UNKNOWN；hidden-test transfer = UNKNOWN。** 当前四 Skill checkout、三 Skill final ZIP 和构建提交是不同对象；离线包校验不能代替平台回执。这里保留外推边界，避免在多篇教材维护完整身份表。

## 如果以后有新证据怎么办

**INTERPRETATION｜解释**：新证据可支持新决定，不能静默覆盖历史冻结。须明确重开范围、新身份和运行/提交授权。

**TEACHING EXAMPLE｜教学示例**：答辩问为何未修完缺陷再交付，应说明修改会形成新的行为身份、需要对应证据；本次选定成熟历史对象及其限制，不能回答“原版已经无问题”。

---

[学习地图](00-学习地图.md) | [上一章](10-Reviewer、Memory、Helper、Controller与Simulator路线.md) | [下一章](12-Anti-overfit、Hidden-Test与不确定性.md)
