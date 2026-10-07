# 12｜Anti-overfit、Hidden-Test 与不确定性

**Overfitting（过拟合）** 在 Agent 竞赛中，不只指机器学习参数记住训练数据。它也可能是研发规则过度适应某些本地轨迹、一次幸运运行或局后已知事件，无法推广到未见机会与风险。

**Anti-overfit（抗过拟合）** 是降低这种适应偏差的做法。它不能凭自身证明 hidden-test transfer（隐藏测试迁移）成功；迁移仍需相应来源与评测证据。

## 四种容易忽略的适应

### 适应 local trajectories（本地轨迹）

反复研究几条熟悉轨迹，会让我们把某种机会顺序当成环境规律。规则在这些轨迹上合理，遇到新菜单或不同资源时却可能不适用。

**FACT｜事实：** S10-21 的历史窗口在机会、tenure、Level、资源与历史风险上混杂，没有产生安全部署的普遍策略增量。[策略挖掘](../../project/research/S10-21_REVIEW_WINDOW_STRATEGY_MINING.md)

**INTERPRETATION｜解释：** 不能把“在这几局里常见”写成“所有局都应这样做”。可迁移假设应依赖当时可观察机制，如当前警告或新反馈，而不是已知轨迹名称。

### 适应 one lucky run（一次幸运运行）

只保留最大值会把特殊轨迹当成能力分布。v1 的 pair 与 v8a 的 pair 是提醒：相同候选可以有不同结果。

**FACT｜事实：** v1 76.04 与 35.31 必须成对出现；v8a 72.65 与 59.00 是同冻结身份的两条完整轨迹；exact-v6 75.29 只有一个被接受完整样本。[最终证据审查](../../project/FINAL_EVIDENCE_REVIEW.md)

保留 pair 不等于已经建立统计控制，也不等于观测差异完全是随机性。它首先让不确定性可见。

### 适应 known events（已知事件）

逐事件添加答案规则，可能形成 event-answer mapping（事件答案映射）。当这些规则来自隐藏资料或未来结果时，还会越过参赛信息边界。

**FACT｜事实：** 项目冻结公共事实、当前 session 与新鲜观察边界，不允许把隐藏阈值和 Test 数据用作策略知识。[官方来源锁](../../project/OFFICIAL_SOURCE_LOCK.md) · [运行合同](../../project/AGENT_RUNTIME_CONTRACT.md)

**INTERPRETATION｜解释：** “根据公开文本拒绝明显欺骗”与“知道某标题必须选编号 2”是不同依据。前者是一般公开语义规则，后者需要问它来自哪里、能否合法部署和是否对未知菜单成立。

### 适应 forensic hindsight（取证后的已知结果）

局后能看到完整路径，读者会觉得正确动作显而易见。但实际决策时没有未来反馈，部分隐藏信息也不能使用。

**INTERPRETATION｜解释：** 分析者应重建 decision-time information set（决策时信息集合），只用当时公开状态提出可部署假设。不能把后来死亡当成当时必然知道的风险强度。

## Public evidence firewall：把决策输入边界写清楚

**Evidence Firewall（证据隔离边界）** 区分分析端可见材料和策略端允许输入。它不仅限制隐藏数字，也限制 session 身份、未来分数和诊断字段进入策略。

**FACT｜事实：** S10-22 的 evaluator 保存最终 reward（奖励/成绩），policy process（策略进程）只接收白名单公开字段。研究还发现普通 MCP serialization（序列化）中的 choices 可能包含 status_updates，任务使用更严格白名单将整张映射剔除。[Simulator 研究](../../project/research/S10-22_SIMULATOR_POLICY_SEARCH.md)

这说明“经过官方接口”不自动满足某个研究自设的更严格边界。输入规则需要明确，而不能只相信字段名字。

**INTERPRETATION｜解释：** Firewall 让读者能追问每个特征的来源。它没有证明研究不存在任何过拟合，也不能把 public-only 直接当成隐藏测试效果。

## 项目已经采用的抗误判做法

| 做法 | 本项目依据 | 能改善什么 | 仍不能证明什么 |
|---|---|---|---|
| 高低样本同时展示 | v1 / v8a pair | 避免只保存最好一次 | 稳定分布 |
| 保留技术部分局 | v7m | 暴露执行与样本筛选问题 | 终局成绩 |
| 区分完成与遵循 | v6 | 防止高分遮住合同缺陷 | 改规则的因果收益 |
| 只使用 participant-visible 输入 | Runtime Contract、Simulator | 限制隐藏证据混入 | Hidden transfer |
| 有界 Candidate 比较 | 架构决策与评估合同 | 限制事后无限试分 | 全局搜索最优 |
| 门禁失败停止 | Reviewer / Simulator | 避免无效或不安全扩张 | 该机制普遍无用 |

**FACT｜事实：** 这些做法与边界见 [实验复盘](../../project/EXPERIMENT_RETROSPECTIVE.md)、[Candidate 合同](../../project/CANDIDATE_EVALUATION_CONTRACT.md) 和 [架构决策](../../project/ARCHITECTURE_DECISIONS.md)。表的组织方式属于教学解释。

## Holdout 与 hidden Test 是不同对象

**Holdout（留出验证）** 是计划保留用于后续检验的材料或样本，避免在同一部分数据上持续调规则。它的价值依赖是否真正留出、是否独立于选择过程、是否代表目标环境。

**FACT｜事实：** Controller 有 12 Dev +12 holdout 回放案例，但它没有正式 gameplay 效果证据。Simulator 计划的 128-seed holdout 未运行，因此不能说在该留出集上验证或失败。[Controller](../../project/research/S10-20_PROMOTION_WINDOW_CONTROLLER.md) · [Simulator](../../project/research/S10-22_SIMULATOR_POLICY_SEARCH.md)

**INTERPRETATION｜解释：** 同样叫 holdout，可能是人工历史案例，也可能是未来随机种子。它们不等同于比赛官方隐藏环境。保留名称并不能跨越验证对象差异。

## Hidden Test 仍然 UNKNOWN

**FACT｜事实：** 官方上传 = NOT PERFORMED / NOT PROVEN；platform score = UNKNOWN；hidden-test transfer = UNKNOWN。[最终方案审阅](../../project/FINAL_SOLUTION_REVIEW.md)

**INTERPRETATION｜解释：** 本地 Dev 适合检查工程、形成机制假设和描述已观察表现；隐藏评测回答未见条件中的表现。二者之间需要新证据，不能由一份漂亮复盘代替。

要避免两种极端：既不能把本地 75.29写成官方成绩，也不能因为没有隐藏结果就否定已有工程成果。实际完成的控制循环、身份审计和负结果管理仍有价值，只是其性能外推有边界。

## 为什么不把局后低分解释全部写进 Prompt

局后解释常常有许多 plausible（合理但未证实）叙述：某次成长投入太少、某警告维护太久、某机会没有争取。若每条都变成“必须”，规则会堆积互相冲突的优先级。

**FACT｜事实：** 项目后期挖掘没有安全新策略 delta，Controller 也没有证明修正多个主要决策错误。[策略挖掘](../../project/research/S10-21_REVIEW_WINDOW_STRATEGY_MINING.md) · [Controller](../../project/research/S10-20_PROMOTION_WINDOW_CONTROLLER.md)

**INTERPRETATION｜解释：** 更合适的产物可能是一个有范围的假设，附上反例与未知。例如“检查当前公开警告是否仍约束机会”，比“曾出现警告就永远优先清理”保留了机制判断。前者也仍需要未来授权验证。

抗过拟合不是完全不学习历史；它要求从历史中学可观察机制，并检查它是否依赖已知结局。只按事件标题或终局结果添加规则，容易让过去越解释越好、未来越不确定。

## 保留未知如何改善展示与沟通

如果写“Hidden Test UNKNOWN”，读者能区分本地研发成果和平台结果；如果只写“已冻结最终包”，读者可能误以为已经上传并评测。

**INTERPRETATION｜解释：** Unknown 应与对象绑定：上传状态未知、平台分数未知、迁移未知是三个判断。没有平台成绩不意味着本地包身份未知；没有 v1 raw 不意味着其历史摘要必须被删除。

这一习惯可以迁移到普通 Agent 产品。成功演示、生产上线、真实用户收益和长期可靠性分别需要证据。准确标注未知，让下一步工作能对准缺口，而不是继续强化已经通过的部分。

## 怎样在不确定时继续决策

**TEACHING EXAMPLE｜教学示例：** 新规则只解决一个已经见过的事件。先写成 HYPOTHESIS，并检查它是否依赖事件名称、未来结果或隐藏字段；再问它能否转成公开机制描述。没有授权新实验时，只记录假设，不把它补进冻结提交。

**INTERPRETATION｜解释：** Anti-overfit 的核心习惯是：保留反例，限制输入，把探索与确认区分，停止不能增加信息的路径。它是本项目支持的研究纪律，不是取得隐藏高分的保证。

---

[学习地图](00-学习地图.md) | [上一章](11-为什么最终选择exact-v6而不是v1或v8a.md) | [下一章](13-Main、Stage、Plan与Codex为什么这样协作.md)
