# CareerSim BDCI26｜项目复盘

这份复盘回答三个问题：项目构建了什么、哪些证据支撑最终选择、结论的边界在哪里。它是事实层的综合入口，不替代 [最终证据索引](FINAL_EVIDENCE_REVIEW.md) 或逐局运行记录。

## 1. 项目一页

项目面对的是一个长期、带状态变化和风险约束的职业模拟：Agent 要持续读取公开状态，在成长、机会、资源和生存风险之间选择合法动作，并在动作后确认实际变化。交付目标最终收敛为一份身份固定、可复核的 Agent 提交包，而不是把仓库当前 Candidate 当成提交物。

冻结选择为 exact historical v6：`candidate-v6-auditable-control-loop`，runtime source commit `1114a04b75548cf52f030d123564e527060fc061`，架构为 **Single Agent + 3 Skills**。唯一冻结包是 `FZU-Loss-final-v6.zip`，SHA-256 为 `31e836b591703dfe520916828da033a57de260bb451d97047bbaee9daaa11b9b`。一次完整样本记录为 **75.29 / 52.70 / 48m / A / L6**；该局是有效的 48 个月完成，但 `RUNTIME_ADHERENCE_FAIL`。这是一条观测，不是稳定分布或因果效应。包已离线冻结，**官方上传未执行，也没有平台评测证据**。[最终身份](FINAL_SUBMISSION_IDENTITY.json) · [冻结审计](reviews/S10-23R_FINAL_SINGLE_SHOT_FREEZE.md)

当前 `main` checkout 保留历史 v8a 工程状态，含四个 Skills；它与最终 exact-v6 ZIP 是不同身份。包内的三 Skill、manifest 和 source commit 以 [最终身份记录](FINAL_SUBMISSION_IDENTITY.json) 与 [构建 manifest](FINAL_SUBMISSION_MANIFEST.md) 为准。

## 2. 工程问题

挑战不是单次选出高分动作，而是在长时程中维持可靠决策：公开状态会变化，早期选择会影响之后的机会；Health 等资源既限制生存，也不能自动取代成长目标；Review 与晋升要求 Agent 用新反馈重排计划；上下文压缩会考验事实恢复；工具调用、动作格式和观察顺序会影响执行是否正确。与此同时，Agent 只能依赖当前局可见证据，不能把隐藏阈值或局后分析伪装成可部署知识。不同轨迹的波动也意味着一局高分不足以证明策略效果。

结果质量和执行正确性必须分别核对：一局可以走到 M49，却仍漏掉协议标记或压缩恢复步骤；反过来，动作日志整齐也不能证明策略有效。工具拒绝、部分运行和自然终局有不同含义，不能把没有分数的技术失败补成策略结论。身份追踪同样是技术问题：Candidate source、运行验证、build commit、manifest 和最终 ZIP 是相关但不同的对象，只有逐层对上，复核者才能确认看到的是哪一份方案。

## 3. 最终方法

最终包把职责分给一个动作提交者和三个 Skills：`structured-state-board` 整理本局公开事实及新鲜度；`rolling-planning` 独占策略规划，维护当前目标、进展、公开风险预算和剩余机会窗口；`risk-review` 只检查已生成候选是否有直接相关的重大风险。Single Agent 是唯一动作提交者。预期控制循环是：

`fresh observe → Board 更新 → Planning 选目标与候选 → Risk gate → 单一动作 → fresh observe`

这些是冻结设计的职责边界，不代表运行样本中的每个环节都遵循成功。v6 样本既观察到 202 次成功状态改变动作后均有新观察，也发现了压缩后未重读 Skills、漏掉半年度标记等执行缺陷。[S06 closeout](S06_CLOSEOUT.md) · [v6 运行记录](runs/v6-run1-validation.md)

## 4. 实际进展

项目从 S01 的最小 no-op 基线（26.95 / 18.86 / 19m / E / L3）发展到可记录完整 48 个月轨迹、审计运行契约并生成固定身份提交包的工程流程。后续架构、Candidate、提示和运行环境均发生变化，因此两端结果不能解释为某一项改动带来的因果提升。能够确认的工程进展是：职责边界更明确，运行身份和包成员可校验，技术失败和负结果有记录，提交前有冻结与复核路径。

实验治理也从“拿到分数”扩展为审查运行前后的完整链条：冻结输入和版本，记录 game 与 Candidate 的绑定，检查 fresh observe、风险门和压缩恢复，最后把接受、限制和下一步授权分开。这样的流程能降低错误归因和误交付的风险，但它本身不是 Agent 策略收益，也不能替代重复样本或官方评测。

## 5. 没有解决的问题

- exact v6 只有一个被接受的完整样本，且 runtime adherence 失败；不能据此声称稳定表现。
- 相同 v8a 四 Skill Candidate 的两次完整运行得到 72.65 和 59.00，表明观测轨迹有差异；样本数不足以估计分布。
- 局部提示/策略加固和后续离线挖掘没有产出足以改变最终方案的安全策略增量。
- Reviewer、Memory、Controller 与模拟器搜索各自触及部署、信号或可行性边界，没有成为冻结方案的一部分。
- 团队/多 Agent 路线仍为 `DEFERRED / NOT_TESTED`。官方平台结果、隐藏集迁移和稳定高分均未知。

这些结果限制的是具体测试路径及当前证据，不能外推成“提示无效”“Memory 无效”或“多 Agent 不可行”。[实验复盘](EXPERIMENT_RETROSPECTIVE.md) 记录问题、证据和非结论。

## 6. 最终选择

Main 的决策标签是 `HIGHEST_OBSERVED_MATURE_THREE_SKILL_CEILING`：在记录的成熟三 Skill 路线中，选取观察到的高位方案 exact v6，并冻结其原始 source identity。它不是“全部历史最高分”或统计胜出结论：Candidate v1 曾有 76.04 的单次记录，但同一候选另一局为 35.31 / 25m / D，且原始来源较弱；v8a 的 72.65 与 59.00 也不是 exact v6 的复验；v6d 是历史 fallback 而非最终包。选择是受证据范围约束的工程决策，不是全局最优证明。[最终方案审阅](FINAL_SOLUTION_REVIEW.md)

## 7. 项目展示的工程能力

仓库展示了 Agent 职责拆分、Skill 契约设计、工具/运行身份审计、单变量假设与有限实验、负结果保留、provenance 管理，以及通过 Git 和离线验证复现交付身份的做法。它展示的是实际完成的工程流程，不等于证明某个职位能力等级或比赛成绩。

## 8. 限制

最终 Candidate 没有重复样本；75.29 的运行存在执行缺陷；没有因果策略估计、隐藏集迁移结论或官方云端评测。current checkout 与冻结 ZIP 分离；部分 raw hold 范围仍未知。Team/Swarm 未测试，最终选择不证明稳定 75+、稳定 80+、统计优势或理论最优。

## 9. 继续阅读

- [Architecture Retrospective](ARCHITECTURE_RETROSPECTIVE.md)：架构形成原因与职责边界
- [Experiment Retrospective](EXPERIMENT_RETROSPECTIVE.md)：代表性证据、负结果与实验纪律
- [Final Solution Review](FINAL_SOLUTION_REVIEW.md)：exact-v6 包、运行缺陷和对照方案
- [Final Evidence Review](FINAL_EVIDENCE_REVIEW.md)：代表性数值和 hold 台账
- [Final Submission Identity](FINAL_SUBMISSION_IDENTITY.json)：提交包的权威身份
