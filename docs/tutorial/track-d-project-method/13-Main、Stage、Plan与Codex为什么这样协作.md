# 13｜Main、Stage、Plan 与 Codex 为什么这样协作

Track C 已解释任务怎样落成 Git。这里关注 governance（治理）为什么影响实验可信度：如果目标、身份、停止条件可以在看到结果后随意修改，那么记录很完整，也可能没有清楚回答原问题。

## 各角色保留不同的判断

**FACT｜事实：** 项目合同规定 Main Hub 管全局与验收，Stage 管当前任务，Codex 在仓库实现并回传；执行自主性用于实现决策，不扩大范围，也不替代 Stage 验收。[Plan 合同](../../project/CODEX_PLAN_CONTRACT.md) · [AGENTS](../../../AGENTS.md)

| 对象 | 实验中的作用 | 如果混淆 |
|---|---|---|
| Main | 保持跨阶段目标、证据和路线判断一致 | 每个局部任务自行追逐最好分 |
| Stage | 限定当前主要问题 | 策略、工具、提交与取证同时无界展开 |
| Plan | 冻结对象、范围、权限和判断条件 | 看到结果后换门槛 |
| Codex | 检查真实源码与记录，实现授权工作 | 用规划猜测代替工程事实 |
| TASK_RESULT | 返回实际执行身份、验证和未知 | 把计划内容当已发生证据 |
| Main Review | accept / reject / continue / stop | 执行完成自动冒充研究接受 |

**INTERPRETATION｜解释：** 角色分工的价值在于把“做出结果”和“解释结果”放进可审查过程，不在于增加层级数量。若 Main 只看一句 PASS，同样不能得到可信判断。

## Stage 为什么限制目标漂移

**FACT｜事实：** S07–S09 的关注点从持续执行、运行语义逐步转向策略和高分；S09 没有稳定突破后，S10 转向有限研究门禁与最终冻结。[架构决策](../../project/ARCHITECTURE_DECISIONS.md)

**INTERPRETATION｜解释：** 阶段边界让研发知道何时继续解决当前问题，何时需要重新定义问题。它阻止“再试一局”“再加一模块”永久沿用旧授权。

阶段可以改变目标，但变化应有新证据和接受判断。S02/S05 定义缺失说明记录也会有不完整处；后来的教程不能用治理语言修补当时不存在的证据。

## FROZEN / RECOMMENDED / DELEGATED_TO_CODEX

**FACT｜事实：** CODEX_PLAN_CONTRACT 明确三种决定等级：

| 标记 | 含义 | 执行者怎样处理 |
|---|---|---|
| FROZEN（冻结） | 必须遵守的目标、事实身份、范围、权限与验收边界 | 不自行突破；前提冲突返回证据 |
| RECOMMENDED（建议） | 有依据但不强制的实现方向与验证顺序 | 可按当前事实调整，并说明理由 |
| DELEGATED_TO_CODEX（委托执行者判断） | 根因、patch location 等需实际检查的未决实现 | 在冻结约束内调查、决定并验证 |

来源：[Plan 合同](../../project/CODEX_PLAN_CONTRACT.md)。

Planner（规划者）不应把低置信度实现猜测写成 MUST（必须）。陌生 SDK 内部到底怎样注册、某异常在哪层发生，需要执行者查真实来源。把猜测冻结会迫使实现绕过事实，结果反而更不可信。

**INTERPRETATION｜解释：** 冻结应保护实验身份和边界，委托应保留工程判断空间。二者共同成立：执行者能选合适实现，但不能因为实现困难就自己增加 Provider 预算、换冻结 Runner 或改实验问题。

## Stop condition 为什么是实验的一部分

Stop Condition（停止条件）在开始前说明哪些结果使后续动作无意义、不安全或越权。它限制的不只是成本，也是事后挑选空间。

**FACT｜事实：** Reviewer 在安全前提不成立时没有进入 Phase B/C；Simulator 在胜任门禁失败时没有继续宏筛选和 holdout；Controller replay gate 未形成足够信号时不创建 v15。[Reviewer](../../project/research/S10-19R1_SUBAGENT_FEASIBILITY.md) · [Simulator](../../project/research/S10-22_SIMULATOR_POLICY_SEARCH.md) · [Controller](../../project/research/S10-20_PROMOTION_WINDOW_CONTROLLER.md)

**INTERPRETATION｜解释：** 没有 stop rule，研究者可以不断重写基础策略、换案例、改判断标准，直到出现“成功”。最后数字无法说明原假设是否通过了原实验。

停止条件应针对实质风险/前提，而不是无限追加低信息门禁。合同也要求区分 Hard Gate（硬门禁）与 Advisory Check（辅助检查），必要安全、身份与 live correctness（实际运行正确性）前提才应阻断。

## TASK_RESULT 为什么是执行证据

一份结果需要写实际 base、commit、Candidate/runtime 身份、做过的检查、未运行条件阶段、live 次数、错误、hold 与 unknown。计划说“将运行十二例”不等于结果有十二个案例；前提失败时应该写零已完成案例、质量未测量。

**FACT｜事实：** Reviewer 报告明确盲评案例完成 0，质量分类计数 NOT_MEASURED，没有把未运行的阶段虚构为一组 UNKNOWN 结果。[Reviewer 研究](../../project/research/S10-19R1_SUBAGENT_FEASIBILITY.md)

**INTERPRETATION｜解释：** 结果报告的读者应该能重建“决定下一步所需的最小证据”，不必阅读所有聊天历史。TASK_RESULT 的价值不是措辞完整，而是把执行和非执行说清楚。

## 为什么 Codex 不能自行宣布阶段完成

单个任务可以满足自己的实现合同，Stage 是否达到目标仍涉及跨任务证据、路线取舍和下一步授权。v6 的有效完成、运行缺陷、v6b 静态修复与 Main 接受，需要综合判断。

**FACT｜事实：** S06 最终接受为 PASS_WITH_KNOWN_RUNTIME_LIMITATION；任务报告的技术事实与 Main 的阶段接受是相关但不同的判断。[S06 收口](../../project/S06_CLOSEOUT.md)

**INTERPRETATION｜解释：** 把“我实现了”写成“研究已成功”，会让实现者隐式决定哪些未知可忽略。独立接受过程让限制保持可见，也让 STOP 成为正式决策。

## 用一句话检查你的 Plan

**TEACHING EXAMPLE｜教学示例：** 对“增加记忆并跑到高分”为止的 Plan，补问：指定哪种记忆路径？自动可用证据是什么？哪些参数冻结？技术失败是否重试？何时停止？谁决定正式采用？如果这些问题未明确，工作流再规范也不保证实验可解释。

具体 branch/worktree/commit（分支/工作树/提交）操作见 [Track C 开发任务](../track-c-repository-tooling/11-一次开发任务从Plan到Git是怎样落地的.md)。本章提供其研究治理理由；文档写作不授权新的运行、清理或提交比赛。

---

[学习地图](00-学习地图.md) | [上一章](12-Anti-overfit、Hidden-Test与不确定性.md) | [下一章](14-从CareerSim迁移到真实Agent工程的方法论.md)
