# CareerSim BDCI26

CareerSim BDCI26 工程仓库，当前处于 **S11 Final Consolidation & Project Retrospective**。S10 closeout 已接受为 `COMPLETE_FINAL_SUBMISSION_FROZEN`；当前最终选择是 exact historical v6：`candidate-v6-auditable-control-loop`，runtime source `1114a04b75548cf52f030d123564e527060fc061`，Single Agent + 3 Skills。

## Final submission

唯一冻结包为 `FZU-Loss-final-v6.zip`，SHA-256：`31e836b591703dfe520916828da033a57de260bb451d97047bbaee9daaa11b9b`。权威身份见 [FINAL_SUBMISSION_IDENTITY](docs/project/FINAL_SUBMISSION_IDENTITY.json)、[manifest](docs/project/FINAL_SUBMISSION_MANIFEST.md) 与 [S10-23R freeze audit](docs/project/reviews/S10-23R_FINAL_SINGLE_SHOT_FREEZE.md)。包已冻结；官方上传未执行，也没有平台评测证据。

## Repository state caveat

当前 checkout 的 [current_candidate.json](configs/current_candidate.json)、[runtime_manifest.json](configs/runtime_manifest.json) 和 `skills/` 下四个 Skills 属于历史 v8a 工程状态；它们不是最终 v6 提交包的身份来源。请勿将 checkout 状态与上述冻结包混为一谈。

## Start here

- [CURRENT_STATE](docs/project/CURRENT_STATE.md)：当前阶段、接受状态与授权边界
- [FINAL_ID_MAP](docs/project/FINAL_ID_MAP.md)：代表性 Candidate、Run、实验与提交包的 Display-ID 及 provenance 索引
- [ARCHITECTURE_DECISIONS](docs/project/ARCHITECTURE_DECISIONS.md)：架构决策
- [OFFICIAL_SOURCE_LOCK](docs/project/OFFICIAL_SOURCE_LOCK.md)：官方来源与冻结合同
- [AGENTS.md](AGENTS.md)：仓库边界与开发规则

## Evidence boundary

75.29 是 S06-24 单次 48 个月样本，且记录为 `RUNTIME_ADHERENCE_FAIL`；它不证明稳定表现、因果收益、理论最优或 hidden-test transfer。最终选择理由也不代表这些结论。当前没有证据声称最终包已被比赛平台接收或评测。
