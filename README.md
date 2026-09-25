# CareerSim BDCI26

CareerSim BDCI26 工程仓库。原候选 candidate-v6-auditable-control-loop 有一次有效 48 个月 gameplay 验证（75.29 / 52.70 / A），但 runtime adherence = FAIL；该单局不证明因果或稳定 80+。当前候选 candidate-v6b-runtime-correctness 仅为静态正确性修复，尚未 runtime/gameplay 验证；S06=IN_PROGRESS，NEXT_GAME=NOT_AUTHORIZED，Design Freeze=ACTIVE。

## Current engineering facts

- [CURRENT_STATE](docs/project/CURRENT_STATE.md)：当前阶段、候选、边界与下一步授权状态
- [Current candidate](configs/current_candidate.json) and [runtime manifest](configs/runtime_manifest.json)：唯一 current candidate identity 与可重建 submission instruction（Single Agent + 三个 Skills）
- [RUN_HISTORY](docs/project/RUN_HISTORY.md)：关键真实对局的精简记录
- [OFFICIAL_SOURCE_LOCK](docs/project/OFFICIAL_SOURCE_LOCK.md) and [ENVIRONMENT](docs/project/ENVIRONMENT.md)：冻结来源与环境合同
- [ARCHITECTURE_DECISIONS](docs/project/ARCHITECTURE_DECISIONS.md)：当前有效架构决定
- [AGENTS.md](AGENTS.md)：仓库边界与开发规则
