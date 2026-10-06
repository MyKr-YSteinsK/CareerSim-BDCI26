# CareerSim BDCI26

CareerSim BDCI26 工程仓库，当前处于 **S11 Final Consolidation & Project Retrospective**。S10 closeout 已接受为 `COMPLETE_FINAL_SUBMISSION_FROZEN`；当前最终选择是 exact historical v6：`candidate-v6-auditable-control-loop`，runtime source `1114a04b75548cf52f030d123564e527060fc061`，Single Agent + 3 Skills。

## 人读报告

面向第一次接触项目的中文阅读入口，覆盖赛题、架构、实验、研发演进、方案选择、答辩、职业材料和证据核验；工程事实仍以 `docs/project/` 中的权威工程记录为准。

- [00｜阅读导航](docs/final-report/00-阅读导航.md)
- [01｜赛题与项目总览](docs/final-report/01-赛题与项目总览.md)
- [02｜Agent 技术方案与系统架构](docs/final-report/02-Agent技术方案与系统架构.md)
- [03｜完整研发流程与方案演进](docs/final-report/03-完整研发流程与方案演进.md)
- [04｜实验设计与证据评估](docs/final-report/04-实验设计与证据评估.md)
- [05｜失败路线与负结果复盘](docs/final-report/05-失败路线与负结果复盘.md)
- [06｜最终方案与候选选择](docs/final-report/06-最终方案与候选选择.md)
- [07｜工程实现与冻结交付](docs/final-report/07-工程实现与冻结交付.md)
- [08｜答辩要点与常见问题](docs/final-report/08-答辩要点与常见问题.md)
- [09｜简历与作品集素材](docs/final-report/09-简历与作品集素材.md)
- [10｜证据索引与事实边界](docs/final-report/10-证据索引与事实边界.md)

## 最终提交方案

唯一冻结包为 `FZU-Loss-final-v6.zip`，SHA-256：`31e836b591703dfe520916828da033a57de260bb451d97047bbaee9daaa11b9b`。权威身份见 [FINAL_SUBMISSION_IDENTITY](docs/project/FINAL_SUBMISSION_IDENTITY.json)、[manifest](docs/project/FINAL_SUBMISSION_MANIFEST.md) 与 [S10-23R freeze audit](docs/project/reviews/S10-23R_FINAL_SINGLE_SHOT_FREEZE.md)。包已冻结；官方上传未执行，也没有平台评测证据。

## 当前仓库状态说明

当前 checkout 的 [current_candidate.json](configs/current_candidate.json)、[runtime_manifest.json](configs/runtime_manifest.json) 和 `skills/` 下四个 Skills 属于历史 v8a 工程状态；它们不是最终 v6 提交包的身份来源。请勿将 checkout 状态与上述冻结包混为一谈。

## 阅读入口

- [CURRENT_STATE](docs/project/CURRENT_STATE.md)：当前阶段、接受状态与授权边界
- [Skill / Instruction 历史演化索引](docs/skill-evolution/00-版本索引.md)：代表性历史快照及精确来源
- [FINAL_REPOSITORY_FREEZE](docs/project/FINAL_REPOSITORY_FREEZE.md)：历史冻结候选记录（已被后续 S11 重构取代）
- [FINAL_ID_MAP](docs/project/FINAL_ID_MAP.md)：代表性 Candidate、Run、实验与提交包的 Display-ID 及 provenance 索引
- [Project Retrospective](docs/project/PROJECT_RETROSPECTIVE.md)：项目目标、成果和整体边界
- [Final Solution Review](docs/project/FINAL_SOLUTION_REVIEW.md)：冻结 exact-v6 身份、运行证据和限制
- [Architecture Retrospective](docs/project/ARCHITECTURE_RETROSPECTIVE.md)：最终架构的职责边界与取舍
- [Experiment Retrospective](docs/project/EXPERIMENT_RETROSPECTIVE.md)：代表性证据、负结果和实验纪律
- [FINAL_EVIDENCE_REVIEW](docs/project/FINAL_EVIDENCE_REVIEW.md)：代表性结果与 hold 台账
- [ARCHITECTURE_DECISIONS](docs/project/ARCHITECTURE_DECISIONS.md)：架构决策
- [OFFICIAL_SOURCE_LOCK](docs/project/OFFICIAL_SOURCE_LOCK.md)：官方来源与冻结合同
- [AGENTS.md](AGENTS.md)：仓库边界与开发规则

## 证据边界

75.29 是 S06-24 单次 48 个月样本，且记录为 `RUNTIME_ADHERENCE_FAIL`；它不证明稳定表现、因果收益、理论最优或 hidden-test transfer。最终选择理由也不代表这些结论。当前没有证据声称最终包已被比赛平台接收或评测。
