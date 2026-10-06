# Final Repository Freeze｜最终仓库冻结记录

## 1. Status

- HISTORICAL_FREEZE_CANDIDATE
- SUPERSEDED_BY_S11_RESTRUCTURE
- NOT_ACCEPTED_AS_FINAL_REPOSITORY_STATE
- Candidate commit debf5e02e302a720697c95c7286326671e28c8c3 is retained as a historical audit record only.
- The user requested continued repository cleanup and learning-asset restructuring; this candidate is no longer awaiting Main acceptance.
- The final competition ZIP identity below is unchanged.
- S11 remains ACTIVE; this record does not declare S11 COMPLETE or FINAL_REPOSITORY_FREEZE_ACCEPTED.

## 2. Repository Identity

- Pre-freeze base: `32f1f5b30e963a029624c822111c5fddea97f13f`。
- Branch: `main`。
- Freeze record commit: this document's delivery commit; exact SHA is reported in TASK_RESULT and Git history. No recursive self-hash is used.

## 3. Final Competition Package

- Candidate: `candidate-v6-auditable-control-loop`；runtime source `1114a04b75548cf52f030d123564e527060fc061`。
- Architecture: Single Agent + 3 Skills — `structured-state-board`、`rolling-planning`、`risk-review`。
- Package: `FZU-Loss-final-v6.zip`；SHA-256 `31e836b591703dfe520916828da033a57de260bb451d97047bbaee9daaa11b9b`；18,082 bytes；7 files；build/source-material commit `113052a9a8943efc7fb2d7d1140f126e62e92040`。
- 本机现存 ZIP 已只读核对大小与 SHA-256；未解包、重建或重压缩。官方上传为 `NOT PERFORMED / NOT PROVEN`，平台评测为 `UNKNOWN`。

## 4. Current Checkout Caveat

当前 `main` checkout 保留历史 `candidate-v8a-v7o-donor-core-transplant` 四 Skill 状态：`structured-state-board`、`rolling-planning`、`delivery-progress`、`risk-review`。它不是上述 exact-v6 提交包身份；本次冻结不改动该 checkout。

## 5. Evidence Boundary

- exact-v6：`75.29 / 52.70 / 48m / A / L6`；晋升记录 M6、M12、M18、M36、M48；`VALID_48M_COMPLETION` 且 `RUNTIME_ADHERENCE_FAIL`。只有一个已接受的完整样本。
- Candidate v1：`76.04 / 48m / A / L6` 与 `35.31 / 25m / D / L4`；76.04 高于 exact-v6 的 75.29。该组不是稳定分布，raw 证据有限。
- v8a 同一 Candidate 的两个样本：RUN-0004 `72.65 / 50.86 / 48m / A / L5`；RUN-0002 `59.00 / 41.30 / 48m / C / L4`。不是 exact-v6 复验或因果对照。
- 未证明稳定 75+、期望成绩、因果策略收益、hidden-test transfer 或理论最优；不声称官方成绩、上传成功、排名、获奖或 TOP5。
- 负向路线只适用于已测边界：Reviewer `REVIEWER_NOT_SAFELY_DEPLOYABLE`；Memory `MEMORY_NOT_DEPLOYABLE`（指定自动 anchor 路径）；deterministic helper `DETERMINISTIC_HELPER_CHALLENGER_SUPPORTED`（隔离工具层）；controller `CONTROLLER_LOGIC_SIGNAL_WEAK`；strategy mining `STRATEGY_SIGNAL_WEAK`；simulator search `SIMULATOR_POLICY_SEARCH_NOT_FEASIBLE`（冻结可行性门）；Team/Swarm `DEFERRED / NOT_TESTED`。

## 6. Human-Readable Layer

S11-20 交叉审查结论：`docs/final-report/00–10` 全部 `PASS`；`DEFENSE_READY=YES`；`PORTFOLIO_SAFE=YES`。人读报告提供解释和导航，不覆盖 canonical engineering evidence。

## 7. Hold / Accepted Unknowns

- Hold ledger：20 个具名 active/pending holds；18 `KEEP_ACTIVE`、2 `UNKNOWN_REVIEW_REQUIRED`、0 可释放。另有 legacy aggregate 可能重叠及 RUN-0001 raw hold 状态未知两个 sentinel。`HOLD_RELEASE_COUNT=0`。
- 历史 `S03-MCP-REGISTRATION=RELEASED_BY_MAIN`；S03 迁移的 20 份 session payload 仍保留并受 hold 约束；S10-21 本机 hold 路径未知。
- 以下为已披露且不阻断仓库冻结的未知：官方上传未执行；平台评测/hidden Test 结果未知；稳定分数分布及期望分数未知；因果策略收益未证明；Team/Swarm 未测试；RUN-0001 raw 正式 hold 状态未知；legacy hold aggregate 唯一成员范围未知；S10-21 本机 hold 路径未知。

## 8. Integrity Verification

- Opening gate：`main`，`HEAD=origin/main=32f1f5b30e963a029624c822111c5fddea97f13f`，工作树干净；S10 CLOSED、S11 ACTIVE。
- Final identity、当前 checkout caveat、canonical evidence、hold ledger 与 S11-20 人读层结论已复核；本机 ZIP SHA-256 与记录一致。
- 指定静态治理测试：4 passed。最终 tracked-Markdown link scan：0 broken；文件和链接计数见 S11-21 TASK_RESULT。
- 受保护的 Candidate、Skill、runtime、config、Runner、submission materials、raw、hold 与包身份均未修改；live gameplay / Provider / MCP operations 为 0。

## 9. Protected Boundaries

本记录冻结 S11 consolidation 后的 repository state，不改变 competition package。它不授权改写 Candidate、Skill、runtime、config、Runner、依赖、submission materials，不授权重建 ZIP、释放 hold、删除 raw、启动 live 操作或执行平台上传。

## 10. Main Acceptance Boundary

This document records the former freeze candidate at debf5e02e302a720697c95c7286326671e28c8c3. Continued S11 repository restructuring superseded that candidate; it was not accepted as the final repository state and is no longer pending Main acceptance. The competition package identity in Section 3 is unaffected. S11 remains ACTIVE.
