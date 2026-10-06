# CareerSim BDCI26｜最终方案审阅

## 1. 最终选择与身份

| Item | Frozen identity |
|---|---|
| Candidate | `candidate-v6-auditable-control-loop` |
| Runtime source | `1114a04b75548cf52f030d123564e527060fc061` |
| Architecture | Single Agent + 3 Skills |
| Skills | `structured-state-board`、`rolling-planning`、`risk-review` |
| Package | `FZU-Loss-final-v6.zip` |
| Package SHA-256 | `31e836b591703dfe520916828da033a57de260bb451d97047bbaee9daaa11b9b` |
| Selection tag | `HIGHEST_OBSERVED_MATURE_THREE_SKILL_CEILING` |

精确身份和三个 Skill blob 见 [FINAL_SUBMISSION_IDENTITY](FINAL_SUBMISSION_IDENTITY.json)；构建 commit `113052a9a8943efc7fb2d7d1140f126e62e92040`、七个 ZIP 成员及哈希见 [FINAL_SUBMISSION_MANIFEST](FINAL_SUBMISSION_MANIFEST.md)。本机留存 ZIP 的实际 SHA-256 已核对一致。冻结选择没有 runtime delta，也没有在打包后重建 ZIP。

## 2. 工作方式

冻结设计的高层循环如下：

1. 取得本局 fresh public observe。
2. `structured-state-board` 整理当前公开事实、来源和 freshness。
3. `rolling-planning` 依据目标缺口、公开进展、风险预算与剩余窗口提出候选。
4. `risk-review` 对已生成的当前候选做 candidate-specific Material Risk 检查。
5. Single Agent 选择一个合法动作并提交。
6. 状态改变后重新 observe，再更新 Board 和 Planning。

Planning 是唯一 strategy owner；Risk 不是第二个 planner，Skills 也不是额外的动作 actor。该循环概括的是提交包的责任契约，不声称模型每次都正确执行。

## 3. 可证优势与运行缺陷

唯一 exact-v6 完整样本记录为 **75.29 / 52.70 / 48m / A / L6**，`VALID_48M_COMPLETION`。样本中 202 次成功状态改变动作后都有 fresh observe；最终身份、三 Skill 字节和 ZIP allowlist 经过离线核验。它提供了完整轨迹和可追溯包身份，但运行结果同时是 `RUNTIME_ADHERENCE_FAIL`。

冻结审计保留了以下缺陷，不能用“minor”概括：

- Energy 多选提交 `choice=6,7,3` 被参数解析拒绝，未改变游戏状态。
- 半年度 review/promotion 点漏掉必需的 H marker。
- 普通 Story 决策在没有新公开证据时反复重开讨论，未可靠遵守有界比较规则。
- 自由文本 CTRL marker 与 action 的配对无法认证；缺少可靠 model-turn ID。
- 两个压缩 epoch 之后都未重新读取三个 Skills，未完成要求的 context-recovery rebuild。

因此，完整通关不等于 runtime correctness 通过；上述一次运行也不估计这些缺陷在不同运行中的频率。[v6 run record](runs/v6-run1-validation.md) · [S10-23R audit](reviews/S10-23R_FINAL_SINGLE_SHOT_FREEZE.md)

## 4. 与其他路线的比较

| Route | Evidence | Why it was not selected as this final package |
|---|---|---|
| v8a four-Skill | 同一 Candidate 两局 `72.65` 与 `59.00`，均 48m；存在运行/证据纪律问题。 | 不同于 exact-v6 identity；两点呈现波动，不代表对 exact v6 的受控比较或稳定分布。[sample 1](runs/v8a-full-horizon-sample1.md) · [sample 2](runs/v8a-full-horizon-sample2.md) |
| v6d fallback | 历史摘要 `71.67 / 65.35 / 59.67`。 | 是备用身份，不是用户冻结的 exact-v6 包；三个摘要值不是统计优势证明。[freeze audit](reviews/S10-23R_FINAL_SINGLE_SHOT_FREEZE.md) |
| Candidate v1 four-Skill | 一局 `76.04 / 48m / A / L6`；另一局 `35.31 / 25m / D / L4`。 | 76.04 高于 v6，故 v6 不是全历史最高分；v1 原始来源较弱且两局差异大，不能据单次峰值决定最终身份。[S06 closeout](S06_CLOSEOUT.md) · [S09-02](reviews/S09-02_FAILURE_FLOOR_HIGH_SCORE_JOINT_FORENSICS.md) |
| 后续实验路线 | Memory、Reviewer、Controller、策略挖掘和模拟器搜索分别遇到有界部署/信号/可行性限制。 | 未产生比冻结方案更强且可提交、已验证的完整身份；各负结果仅适用于各自的测试边界，详见 [Experiment Retrospective](EXPERIMENT_RETROSPECTIVE.md)。 |

## 5. 为什么选 v6

`HIGHEST_OBSERVED_MATURE_THREE_SKILL_CEILING` 描述的是 Main 在现有证据下选中的成熟三 Skill 高位方案，不是最高分 ever、分布赢家或统计优势。v1 的 76.04 反例被保留；v8a 两个样本没有转移到 v6；v6d 仍是不同的历史 fallback。Main 冻结的是可明确绑定到 source commit、Skills 和 ZIP hash 的 exact v6，而不是把后续 checkout 状态或未验证路线混入成品。

## 6. 可复现性与 provenance

- 权威工件身份：[FINAL_SUBMISSION_IDENTITY](FINAL_SUBMISSION_IDENTITY.json)
- 七成员与逐文件哈希：[FINAL_SUBMISSION_MANIFEST](FINAL_SUBMISSION_MANIFEST.md)
- 冻结决策、offline 检查与非声明：[S10-23R freeze audit](reviews/S10-23R_FINAL_SINGLE_SHOT_FREEZE.md)
- 运行结果与 adherence 发现：[v6 validation](runs/v6-run1-validation.md)
- 当前权威状态：[CURRENT_STATE](CURRENT_STATE.md)

current `main` checkout 的 `configs/` 和四 Skills 属于历史 v8a 状态，不是 ZIP 的源身份。官方上传**未执行**，没有上传回执或平台评测结果；包已准备并冻结不代表平台受理。[Official Source Lock](OFFICIAL_SOURCE_LOCK.md)

这组复盘文档不改变任何 `FORENSIC_HOLD` 状态，也不释放或清理 held evidence；当前保留和未知范围仍以 [FINAL_EVIDENCE_REVIEW](FINAL_EVIDENCE_REVIEW.md) 为准。

## 7. 非声明

该证据不证明：比赛获奖、TOP5、官方上传成功、官方平台已评测、稳定 75+、稳定 80+、exact v6 历史最高分、统计优越、因果分数提升、hidden-test transfer 或全球最优。exact v6 只有一个完整运行样本，且该样本 `RUNTIME_ADHERENCE_FAIL`；Team/Swarm 保持 `DEFERRED / NOT_TESTED`。
