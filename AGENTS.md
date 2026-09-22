# AGENTS.md

> 只保存 CareerSim 仓库独有的长期工程边界；通用执行流程由适用的 Codex Skill 提供。

## 1. Project identity

- Repository / package: CareerSim BDCI26 development repository
- Primary branch: `main`
- Primary runtime/platform: Windows / PowerShell；官方运行环境尚未验证
- Key project-state files:
  - `docs/project/CURRENT_STATE.md`
  - `docs/project/OFFICIAL_SOURCE_LOCK.md`
  - `docs/project/ARCHITECTURE_DECISIONS.md`

## 2. Protected / generated / private boundaries

- `docs/project/OFFICIAL_SOURCE_LOCK.md` 是官方事实与运行合同的证据入口；没有新证据不得静默改写版本、来源或运行边界。
- `.env`、密钥、token、凭据、runtime cache、日志、数据库和本机生成状态属于私有或生成内容，不得提交。
- 官方上游仓库是来源依据；本仓库的代码、配置和实验结果必须保留可追溯的版本与结果记录。
- 共享 `career_emu` 未验证隔离前，对局串行；不得并行运行可能互相污染的会话，也不得依赖跨局残留记忆。
- 安装依赖、启动官方 Runner、远程模型调用、比赛提交等 live / external 操作必须属于明确任务范围，并保存必要证据。

## 3. Repository command semantics

- 当前尚未建立项目专用 test、typecheck、lint、build 或 release 命令；不得把仓库初始化检查冒充运行验证。
- 官方环境命令、依赖状态、模型映射和 baseline 结果必须记录实际版本、参数、时间与产物路径。
- Git 基本检查：`git status --short --branch`、`git diff --check`；新增验证命令需说明其实际覆盖的失败模式。

## 4. Version / delivery / release model

- `main` 是主分支；后续有实质改动时使用独立分支或 worktree，不强推、不重写已推送历史。
- 初始仓库提交消息固定为 `chore: initialize CareerSim development repository`。
- `origin` 指向私有 GitHub 仓库；只有在本地验证通过且任务授权范围内才 push。
- 官方 repo SHA、包版本和模型别名以 Source Lock 为候选身份；发生变化时建立新的可比较配置，不覆盖旧证据。
- 当前没有产品发布版本、部署端点或正式 release 流程。

## 5. Project-specific invariants

- S01 先完成官方环境、Runner 和最小 baseline 闭环，再开始正式 Agent Skill 设计与实现；优先从最小 Skill Contract 开始。
- 起步路线是 Single Agent + Multiple Skills。Memory / Planning / Risk / Swarm 仍是设计或实验方向，不得在 baseline 未建立前提前建设复杂系统。
- Main Hub 维护全局状态和阶段推进；Stage 负责一个有边界的任务；Codex 负责仓库实现与证据回传。Codex 不自行宣布 Stage 完成。
- 重要实验记录 `Experiment ID`、假设、修改、基线、版本、运行次数、结果、失败分类和决策；单次运行不能单独决定主路线。
- 事实、推断、假设和待验证事项必须分开表达；不得把未知阈值、模型映射或未运行结果写成事实。
- 不为未来可能使用的功能提前引入复杂框架、共享状态系统或大量治理文件。

## 6. Skill routing

- 普通仓库开发使用 `frugal-dev-runner`。
- 比赛 Agent Skills：S01 完成官方环境、Runner、最小 baseline 闭环后再设计；先做最小 contract，不先做复杂 Memory / Planning / Risk / Swarm。
- `experiment-manager`：只有实验开始反复执行、手工记录重复时建立。
- `framework-debugger`：只有 JiuwenSwarm、emulator 或 runtime 排障出现重复模式时建立。
- `submission-auditor`：接近首次正式比赛提交时建立。
- 不因“以后可能有用”提前创建辅助 Skill。

## 7. Repository-specific stop conditions

- Source Lock 与实际官方仓库、依赖或运行结果冲突时，先记录冲突和证据，不静默换版本或声称兼容。
- 缺少必要凭据、权限、外部服务或用户产品决策时停止在可验证边界，并明确未完成部分。
- 任何扩大到环境安装、比赛运行、提交、并行 runtime 或架构重构的动作，都需要新的明确任务范围。

## TASK_RESULT presentation contract

Codex 最终回传必须使用清晰的 Markdown，不得输出未格式化的字段堆叠。

格式要求：

- 第一行使用二级标题：`## TASK_RESULT`
- 主要状态字段使用 Markdown 列表，字段名加粗：
  - `- **Status:** ...`
  - `- **Branch:** ...`
  - `- **Commit:** ...`
- `Evidence`、`Verification`、`Changed Files`、`Problems`、`Next Recommended Action`
  等较大部分使用三级标题。
- 命令、路径、SHA、版本号和状态常量使用反引号。
- 多项结果使用列表或表格，不压成连续纯文本。
- 保持内容简洁，不为了排版增加重复说明。
- TASK_RESULT 的字段语义不得因排版而改变。
- 如果具体 Task 已规定更严格的 `TASK_RESULT` schema，以具体 Task 为准。
- 双语显示，写好中文，比如TASK_RESULT|任务结果

## Progress / ETA reporting contract

仅对预计超过数分钟、多阶段、安装、构建、测试或实验任务启用；短小任务不为了形式制造进度播报。

- 开始执行前给出简短阶段计划，列出主要 Phase、预计耗时、ETA 区间和置信度。
- 主要 Phase 完成、进入耗时步骤、计划明显偏离、出现 blocker / retry / 新风险，或长时间没有阶段变化时，简短汇报已完成、当前、下一步、ETA 和 blocker。
- ETA 是估计而非保证；优先使用范围，如 `5–10 min`，无法可靠估计时写 `Unknown`。
- 下载、安装、远程 API 和长实验不得伪造精确剩余时间；不根据 token、工具调用次数、输出行数伪造完成百分比，也不把工作量不同的 Phase 强行按等比例表达。
- 汇报保持简洁，服务于判断已完成什么、正在做什么、还剩什么、最长步骤和是否阻塞。
