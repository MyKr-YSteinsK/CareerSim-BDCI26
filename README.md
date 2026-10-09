# CareerSim BDCI26

CareerSim BDCI26 工程仓库，**S11 Final Consolidation & Project Retrospective 已完成**。S10 closeout 已接受为 `COMPLETE_FINAL_SUBMISSION_FROZEN`；当前最终选择是 exact historical v6：`candidate-v6-auditable-control-loop`，runtime source `1114a04b75548cf52f030d123564e527060fc061`，Single Agent + 3 Skills。

## 人读报告

面向第一次接触项目的中文阅读入口，覆盖赛题、架构、实验、研发演进、方案选择、答辩、职业材料和证据核验；工程事实仍以 `docs/project/` 中的权威工程记录为准。

- [00｜阅读导航](docs/final-report/00-阅读导航.md)
- [01｜项目总览与最终成果](docs/final-report/01-项目总览与最终成果.md)
- [02｜Agent 技术方案与系统架构](docs/final-report/02-Agent技术方案与系统架构.md)
- [03｜研发演进、实验与失败复盘](docs/final-report/03-研发演进、实验与失败复盘.md)
- [04｜最终方案、候选选择与工程交付](docs/final-report/04-最终方案、候选选择与工程交付.md)
- [05｜答辩、作品集与证据边界](docs/final-report/05-答辩、作品集与证据边界.md)

## 最终提交方案

唯一冻结包为 `FZU-Loss-final-v6.zip`，SHA-256：`31e836b591703dfe520916828da033a57de260bb451d97047bbaee9daaa11b9b`。权威身份见 [FINAL_SUBMISSION_IDENTITY](docs/project/FINAL_SUBMISSION_IDENTITY.json)、[manifest](docs/project/FINAL_SUBMISSION_MANIFEST.md) 与 [S10-23R freeze audit](docs/project/reviews/S10-23R_FINAL_SINGLE_SHOT_FREEZE.md)。S11 冻结审计时，该 18,082-byte 工件的官方上传状态为 `NOT PERFORMED / NOT PROVEN`；赛后用户报告的三份上传 ZIP 官网综合评分见[报告 04](docs/final-report/04-最终方案、候选选择与工程交付.md)，其中 v6 上传 ZIP 与此冻结工件的字节身份不同。

## 当前仓库状态说明

当前 checkout 的 [current_candidate.json](configs/current_candidate.json)、[runtime_manifest.json](configs/runtime_manifest.json) 和 `skills/` 下四个 Skills 属于历史 v8a 工程状态；它们不是最终 v6 提交包的身份来源。请勿将 checkout 状态与上述冻结包混为一谈。

## 阅读入口

- [教程统一入口与术语](docs/tutorial/00-从这里开始.md)：按 Agent 入门、运行、仓库或研究问题选择阅读路线。
- [CURRENT_STATE](docs/project/CURRENT_STATE.md)：当前阶段、接受状态与授权边界
- [Skill / Instruction 历史演化索引](docs/skill-evolution/00-版本索引.md)：代表性历史快照及精确来源
- [FINAL_REPOSITORY_FREEZE](docs/project/FINAL_REPOSITORY_FREEZE.md)：最终仓库冻结与 S11 收口记录（Main 已接受）
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

75.29 是 S06-24 单次 48 个月样本，且记录为 `RUNTIME_ADHERENCE_FAIL`；它不证明稳定表现、因果收益、理论最优或 hidden-test transfer。最终选择理由也不代表这些结论。当前没有证据证明上述 18,082-byte exact-v6 冻结包已被比赛平台接收或评测；赛后用户报告的评分及其各自包身份见报告 04。
