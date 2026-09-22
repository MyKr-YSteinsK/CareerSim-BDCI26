# CareerSim BDCI26

CareerSim BDCI26 的正式开发仓库，用于后续代码、Skills、配置、实验记录和工程事实维护。

## 当前阶段

S01-01 仓库初始化与目录整理。仓库已进入可继续开发的最小状态；官方运行环境、Runner、模型调用和 baseline 尚未验证。

## 工程事实入口

- [AGENTS.md](AGENTS.md)：仓库独有的开发边界与 Skill 时机规则
- [CURRENT_STATE.md](docs/project/CURRENT_STATE.md)：当前真实快照
- [OFFICIAL_SOURCE_LOCK.md](docs/project/OFFICIAL_SOURCE_LOCK.md)：官方事实与运行合同
- [ARCHITECTURE_DECISIONS.md](docs/project/ARCHITECTURE_DECISIONS.md)：长期架构决定

## 当前不要从这里开始

下一步应先完成官方环境、Runner 和最小 baseline 闭环。在此之前不要实现比赛 Agent Skill、复杂 Memory / Planning / Risk / Swarm，也不要把研究摘要或历史 Bootstrap 资料重新堆回仓库根目录。
