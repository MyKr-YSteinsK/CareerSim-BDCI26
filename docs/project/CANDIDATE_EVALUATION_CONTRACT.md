# Candidate Evaluation Contract｜候选评估合同

单局 quantitative 不是唯一评价维度。每个正式 Candidate Review 至少分四组记录。

## A. Competitive Performance

- quantitative_score
- competition_partial_score
- survival_months
- final Level
- promotion checkpoints
- final public state

单局高分只能记 `SINGLE_RUN_*_OBSERVED`；不得据此声明 stable 80+。

## B. Robustness / Failure Floor

记录：

- early terminal / natural completion；
- 最早 failure mode；
- `RECOVERY` 类型；
- recovery 是否执行；
- 是否退出 recovery 回到主线；
- 是否出现 self-reinforcing deadlock；
- bad path 的最终损失程度。

高上限改动若明显恶化 failure floor，不得仅凭 best-case 进入稳定方案。

## C. Behavioral Correctness

至少关注：

- MODE=A/S 分布与明显误判；
- poor grade/no-promotion 是否被错误长期 S；
- no-gain routing；
- Review Plan checkpoint continuity；
- Board public-state fidelity；
- Delivery overclaim；
- Risk gate correctness；
- compression/recovery adherence；
- action marker/preflight correctness。

## D. Efficiency

记录可确认的：

- successful actions / observes；
- execution boundaries / continuations；
- Provider zero-work failures；
- input/output tokens；
- compressor events；
- Skill reread/recovery次数；
- wall-clock。

## 决策规则

重要策略推广遵循：

`Evidence → Hypothesis → Experiment → Decision → Implementation`

随机事件导致的单局差异不得自动解释为 Candidate 因果效果。

比较至少区分：

- score ceiling；
- robustness floor；
- adherence/correctness；
- execution efficiency。

若某一局未覆盖目标机制，例如 M24 early terminal 未覆盖 L6，则明确写 `NOT_EXERCISED / NOT_VALIDATED`，不得当作失败或成功证据。
