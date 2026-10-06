# CareerSim BDCI26｜实验复盘

这份复盘综合少数能改变项目判断的证据；详细分数与保留状态仍以 [FINAL_EVIDENCE_REVIEW](FINAL_EVIDENCE_REVIEW.md) 为准，不在这里维护第二份 run ledger。

## 1. 评估原则

- 一局是一次观测，不是分布；相同 Candidate 的两次结果也不能独自证明策略因果。
- 对局成本高。先冻结 Candidate、Skills、Runner 和输入边界，再决定一次运行要回答的问题。
- 策略依据当前局可见的公开状态、合法选项和可确认回执；隐藏计数、阈值和 Dev 内部分析不转成 runtime lookup。
- 技术失败、自然终局、部分轨迹和 adherence failure 分开记录。技术失败不改写成策略失败，完整终局也不自动意味着运行契约通过。
- Candidate、manifest、runtime 和运行环境身份不同，结果不自动跨版本迁移。保留 raw provenance，不用摘要或 hash 取代唯一来源。

## 2. 代表性证据

| Evidence | Observation | What it supports / does not support |
|---|---|---|
| S01 minimal no-op | `26.95 / 18.86 / 19m / E / L3`，提前终局。 | 说明项目的最小起点；不证明后续分数差由某一改动造成。[RUN_HISTORY](RUN_HISTORY.md) |
| Candidate v1 两局 | `76.04 / 48m / A / L6`；另一局 `35.31 / 25m / D / L4`。 | 说明单个高分不是稳定性的证据。该组为 Tier-B 摘要，原始 raw 不可用，不作为受控分布。[S06 closeout](S06_CLOSEOUT.md) |
| exact v6 S06-24 | `75.29 / 52.70 / 48m / A / L6`，有效完整局；`RUNTIME_ADHERENCE_FAIL`。 | 支撑一个成熟三 Skill 完整运行样本；不支持稳定表现、因果提升或 final package adherence PASS。[v6 记录](runs/v6-run1-validation.md) |
| v8a S09-RUN07/RUN08 | 同一冻结四 Skill Candidate 得到 `72.65` 和 `59.00`，两局均 48m。 | 显示两条轨迹分数不同；两点不是校准分布，不是 exact-v6 复验。[Sample 1](runs/v8a-full-horizon-sample1.md) · [Sample 2](runs/v8a-full-horizon-sample2.md) |
| 有用的负尾/技术样本 | v7q 在 M24 自然淘汰，`26.80 / 18.76 / 24m / E / L1`；v7m 到 M20 的 Runner technical failure 没有终局分数。 | 保留真实失败边界；前者不说明某一动作可避免终局，后者不推造策略分数。[v7q](runs/v7q-run1-validation.md) · [v7m](runs/v7m-run1-validation.md) |

最终比较还保留 v6d 三个历史值 `71.67 / 65.35 / 59.67`。这些记录是 fallback 比较信息，不因出现三数就成为稳定分布。[冻结审计](reviews/S10-23R_FINAL_SINGLE_SHOT_FREEZE.md)

## 3. 策略发现的证据边界

跨运行轨迹显示成长、晋升、资源和生存状态共同变化；某些公开效果可在 fresh observation 后追踪，重复同一选择也不保证收益。v6 和 v8a 的不同运行展示过状态刷新、目标重排和风险处理，但没有对照实验可以把最终分数归因到某一机制。相同公开状态与不同结果、不同 promotion path，以及 v8a 的 59.00 下尾都反对把一局解释成确定配方。

因此“尽量从可观察效果更新判断”“风险应约束具体候选”“hidden-threshold certainty 不安全”是受证据支持的工程边界；固定成长菜单、隐藏阈值、特定事件答案或普遍最优配比仍是未证假设。[S06 architecture review](reviews/S06-16_FINAL_CONTROL_ARCHITECTURE_REVIEW.md) · [S09-12 trajectory review](reviews/S09-12_V8A_TWO_SAMPLE_TRAJECTORY_DIVERGENCE_REVIEW.md)

## 4. 失败与负结果

| Question | Evidence → decision | What it does not prove |
|---|---|---|
| 增加 prompt/policy 条款能否稳定突破？ | S09 关闭增量 prompt-hardening 环；S10-21 得到 `STRATEGY_SIGNAL_WEAK`，没有安全 Candidate delta。 | 不证明 prompt 或策略规则普遍无效；只说明这些材料未支撑下一次改动。[S10-21](reviews/S10-21_STRATEGY_BREAKTHROUGH_GATE.md) |
| 冻结 rail 能否部署 advisory Reviewer？ | S10-19-R1 未找到已注册且机械只读的 reviewer path，Phase B/C 未运行；`REVIEWER_NOT_SAFELY_DEPLOYABLE`。 | 不证明独立审查没有价值，也没有评估盲审质量。[Gate](reviews/S10-19R1_BREAKTHROUGH_GATE.md) |
| Memory anchor 能否自动进入上下文？ | S10-19-R2 的冻结轨道捕获中，自动 `MEMORY.md` 正文未出现；显式 read 可用；`MEMORY_NOT_DEPLOYABLE`。 | 不证明 Memory 普遍无效，没有测量模型行为或分数收益。[Gate](reviews/S10-19R2_MEMORY_BREAKTHROUGH_GATE.md) |
| 独立 deterministic helper 是否可行？ | 临时 Skill 脚本在隔离 tool rail 对固定公开状态读写成功；`DETERMINISTIC_HELPER_CHALLENGER_SUPPORTED`。 | 云端解释器、权限、模型是否调用和遵循均未测，不是 Candidate 级效果。[Gate](reviews/S10-19R3_BREAKTHROUGH_GATE.md) |
| replay controller 能否修复重要决策？ | 24 个案例中 1 个状态级修正，8 个 `UNKNOWN`；主要已知决策错误未证明被纠正；`CONTROLLER_LOGIC_SIGNAL_WEAK`。 | 不证明所有控制器都无效，也未得到部署或收益证据。[Gate](reviews/S10-20_CONTROLLER_GATE.md) |
| 宏策略是否有收益？ | 安全的 public-input harness 通过边界检查，但冻结故事基线仅 2/16 完成；12 个宏定义中只跑 baseline，search/holdout 为 0；`SIMULATOR_POLICY_SEARCH_NOT_FEASIBLE`。 | 没有比较宏策略，因此不支持“simulator search 已证明策略无效”。[Gate](reviews/S10-22_FINAL_OPPORTUNITY_GATE.md) |
| Team/Swarm 是否改善结果？ | 该路线没有完成实验。 | `DEFERRED / NOT_TESTED`，不是负向实验结论。[Architecture decisions](ARCHITECTURE_DECISIONS.md) |

## 5. 反过拟合与合规

可部署策略只使用 participant-visible 的当前 session 公开事实、合法选项、公开反馈和确认回执。历史 Dev/hidden forensic 分析可以帮助识别风险和提出假设，但不自动成为事件标题答案表、隐藏阈值、评分权重或动作 lookup。无法从公开来源确认的字段应标 `UNKNOWN`，不能由轨迹顺序补齐。[OFFICIAL_SOURCE_LOCK](OFFICIAL_SOURCE_LOCK.md) · [v6 public-state boundary](reviews/S06-16_FINAL_CONTROL_ARCHITECTURE_REVIEW.md)

## 6. 实验设计教训

1. 运行前冻结来源与身份；运行后把分数、adherence、终局和工具失败分开判断。
2. 对照必须尽可能只改变一个机制，并保留反例；没有可识别比较时写 `UNKNOWN`。
3. 负结果按实际门槛描述，停止在信息不足处，不把 feasibility failure 写成策略优劣。
4. 多局才能讨论分布；若轨迹或环境身份不一致，不能把样本数直接当作可比性。
5. 若新增实验不能改变决策或排除竞争解释，应停止扩展，保留已知限制。

## 7. 仍未知

最终 exact v6 的稳定分布与因果策略贡献、hidden-test transfer、官方评测结果、Team/Swarm、未测试的 Memory/Reviewer 部署路线以及长期 adherence 都仍未知。官方提交上传未执行；包冻结不是门户受理证明。[Final submission identity](FINAL_SUBMISSION_IDENTITY.json)
