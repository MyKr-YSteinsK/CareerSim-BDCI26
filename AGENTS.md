# AGENTS.md

> CareerSim 长期边界；通用流程由 `frugal-dev-runner` / Task 管理。

## 1. 身份与事实归属

- `MyKr-YSteinsK/CareerSim-BDCI26`；`main`；Windows / PowerShell。`docs/project/`：`CURRENT_STATE.md` 管状态，`ARCHITECTURE_DECISIONS.md` 管架构，`OFFICIAL_SOURCE_LOCK.md` 管官方事实、冻结身份和运行/提交合同；环境与关键对局事实见 `ENVIRONMENT.md` / `RUN_HISTORY.md`。
- 分支增量标记 `IN_FLIGHT_EVIDENCE`，不冒充 `MERGED_FACT`；历史按当时语境解读。官方身份变更须新证据/可比较配置，不覆盖旧结果。
- 凭据、`.env`、cache、shared DB、未扫描的日志/会话和其他本机生成状态不得提交；仅按 [LIVE_RUN_WORKFLOW](docs/project/LIVE_RUN_WORKFLOW.md) 的显式选择、run-window 截取与 secret scan 归档必要开发证据。不得静默改 frozen Runner、依赖或 `uv.lock`。

## 2. 本机 Workspace

- 固定 `D:\CS\CareerSim\.local\`：仅在获准隔离任务需要时使用 `worktrees/<task>`；`runtime/<task-or-run>` 留存获准且仍有价值的本机输出，`upstream/<identity>` 与 `scratch/<task>` 仅用于可重建副本/派生物；整体 gitignored。
- 禁止新建 `D:\CS\CareerSim-*` 临时目录；已有旧路径仅在明确授权的清理/迁移任务中处理。
- 例外：checkout 内 `.career_sim_runner/`、根 `.venv`、用户目录 `.jiuwenswarm-instances/career_emu` 保持既定路径/ignore；RESULT 记录位置，不为归置改冻结 runtime。唯一取证来源不得放 scratch。
- CareerSim worktree 的 Python static/offline checks 默认使用项目根解释器 `D:\CS\CareerSim\.venv\Scripts\python.exe`。如使用 `uv run`，先激活该根环境并显式使用 `uv run --no-sync --active`；禁止裸 `uv run` 或隐式在 task worktree 创建/同步 `.venv`。误生成且 ignored 的 worktree `.venv` 若确认未影响 tracked files 或 dependency/runtime identity，记录为 local residue，不因清理失败单独阻断 live run；发现污染则停止复核。

## 3. Git workflow

- 默认在 `D:\CS\CareerSim` 的 `main` 串行开发、做 targeted verification、形成一个有意义的 commit 并 push；不默认创建 branch 或 worktree。
- 只有 Main/Planner 对具体任务明确说明隔离理由时才开 branch；worktree 需要独立理由与明确授权，branch 不自动意味着 worktree。
- 若任务获准使用 branch：独立任务以 fetch 后最新 `origin/main` 为基线；依赖未合入父任务的任务以已验证 parent HEAD 为基线。父先合、子后合；核对 ancestry，不重写已推送历史。
- TASK_RESULT 按任务合同记录基线/父链、交付身份、验证边界和真实问题；技术失败证据不等于实现通过。
- worktree 仅在获准的并行/隔离任务中 active。交付、review、raw 引用及 child/Main 依赖解除后，按精确路径清理；不强删脏状态，不例行 prune。

## 4. Runtime Evidence Lifecycle

- Canonical：去敏 RESULT/manifest/compact evidence；记 Experiment/Run/session、版本/config、假设/修改/基线、次数/时间、score/token/runtime、失败/决策、路径/bytes/hash；未知标明，缺失 usage 不记零。
- Raw：transcript/events、服务日志、DB/session、provider usage、临时配置默认留本地；仅经 [LIVE_RUN_WORKFLOW](docs/project/LIVE_RUN_WORKFLOW.md) 筛选和扫描的 run-scoped 开发证据可进入 private repo，shared DB、凭据和无关会话始终不得提交。失败未决、结论依赖 raw、摘要不能独立解释或唯一复验来源须留存；hash 不替代源文件，归档也不自动解除 `FORENSIC_HOLD`。
- `FORENSIC_HOLD` 在 RESULT/manifest 记原因、最小文件/时间窗/路径/hash、责任 Task/解除者、解除条件/复查点；安装/清理可能覆盖时先授权保全快照，不以事后状态冒充历史。
- Evidence Closure：责任 Task 提供独立可审结论/compact 证据，核实必要来源可恢复或无需复析，复现/child 等依赖已解除；Main/Stage 接受并记 hold 解除。之后仅授权清理可删指定 raw，记范围/复验限制；hash 或 COMPLETE 不自动关闭。

## 5. Task 权限 / shared runtime / retry

- `READ_ONLY`：读 repo/Git/必要去敏证据、离线分析；不改 repo/runtime、不调用 provider。
- `REPOSITORY_WRITE`：范围内 patch、offline/static 验证、授权 commit/push；不隐含 `LIVE_RUN`，validate 不保证无副作用。
- `LIVE_RUN` 须 Task 明列依赖/Skill/submission 安装、服务/MCP、provider、game、smoke/benchmark、比赛提交的允许动作、次数/成本及停止条件；未列不授权，服务启动可能调用模型。
- Future live Plans 可选 `CODEX_FULL_RUN` 或 `HUMAN_RUN_GPT_AUDIT`；两者共用 [LIVE_RUN_WORKFLOW](docs/project/LIVE_RUN_WORKFLOW.md) 的同一离线证据管线。Codex 全程模式按 P0–P6 有界执行；完成阶段仅因新的 material evidence 重开，同一诊断分支连续两次无新 material evidence 即停止并记 `UNKNOWN / LIMITATION`，FROZEN safety/identity 事项返 Main。
- Windows 下 PowerShell 优先用于简单 Git / process / service control；YAML、JSON、hash、多条件结构化判断或多返回码汇总优先用 Python 或拆成原子命令。避免在复杂 inline expression 中混合 command execution、`$LASTEXITCODE`、对象构造和控制流；无副作用的本地 parser/script failure 按 Tooling Error 处理。
- CareerSim live task 的 preflight 只将直接影响 live correctness / safety 或任务明确要求的必要 dependency/interface 的 Hard Gates 设为阻断条件；identity 未漂移的稳定 PASS 应复用。既定 Hard Gates 通过后，只有新 material evidence 才能增加 blocking diagnostic gate。
- snapshot rehash、历史日志复查、ignore 检查和报告格式不得默认升级为 gameplay blocker；但 Plan / `FORENSIC_HOLD` 明确要求的唯一证据保全与核验仍须完成。效率规则不得削弱 `FORENSIC_HOLD`、secret protection、shared runtime 串行、bounded live retry 或 Unknown Side Effect 的 STOP 边界。
- `career_emu` 未证隔离前，安装/reload/对局/共享 DB/config 写入均串行；先确认独占窗口。worktree 不等于隔离，不依赖跨局残留。
- 无副作用确定性读取可有限 retry。`new_game`、`take_action`、install、provider/submission、共享写入或 MCP 调用遇超时/断连/partial/unknown outcome：先查状态/日志，在授权内 observe 核对；仍不明则停并留证，不盲重发。
- live 授权不等于无限 retry；bounded smoke 达上限或触发 TECHNICAL_FAILURE 停止条件即返回 review，不为取得成功重跑。

## 6. Verification 与任务资产

- Tier 0（文档/copy/格式/语言）：相关 parse/format、`git diff --check`、commit/push。
- Tier 1（普通 Skill/code）：一个 targeted test、一个相关 contract/behavior check、`git diff --check`；无身份漂移时复用稳定 PASS。
- Tier 2（live/benchmark）：仅核验直接影响正确性与安全的 Hard Gates；复用未漂移的稳定证据，不无限追加门禁。
- Tier 3（官方提交/破坏性迁移）：执行必要的完整 hygiene 与官方合同核对，范围仍受 Plan 限定。
- 普通 Plan 的 Hard Acceptance Criteria 默认不超过 8 项；例外仅限 live、破坏性迁移、官方提交、secret/security 或重大框架迁移，并说明理由。
- 普通任务默认不新建 `experiments/<task>`、矩阵、逐任务 candidate manifest/RESULT 或一次性 verifier；默认交付为 Git diff、targeted test 与 TASK_RESULT。仅保留重要 gameplay/benchmark、可复盘 runtime failure、架构实验或官方冻结证据；一次性 verifier 用后删除，不提交。

## 7. 架构与返回 Review

- Single Agent + Multiple Skills；唯一提交者用当前 session/新鲜观察，回执后更新状态。设计/安装/加载/应用/收益分开举证；单局不决定路线，不编造隐藏阈值。架构变化依 ADR：Hypothesis → Experiment → Decision。
- Main Hub 管全局/验收，Stage 管任务，Codex 实现回传。验收/路线改变、假设推翻、超范围 blocker、runtime 异常、额外 live/retry 预算、Source Lock/依赖漂移、parent 失效、需改 frozen Runner 或建辅助 Skill 时返 Main/Stage；不自行扩 scope 或宣布 Stage COMPLETE。
- Codex Task Plan artifact 的 FROZEN / RECOMMENDED / DELEGATED_TO_CODEX 决策分级及工程执行边界遵循 `docs/project/CODEX_PLAN_CONTRACT.md`；Task 可收紧要求，不得放宽其中的 FROZEN / governance 边界。
- Skill/runtime ownership、Candidate evaluation 与 official submission 分别遵循 [Agent Runtime Contract](docs/project/AGENT_RUNTIME_CONTRACT.md)、[Candidate Evaluation Contract](docs/project/CANDIDATE_EVALUATION_CONTRACT.md) 和 [Final Submission Contract](docs/project/FINAL_SUBMISSION_CONTRACT.md)；这些引用不扩大 task-specific permissions。
- 辅助 Skill 触发：重复记账→`experiment-manager`，重复框架排障→`framework-debugger`，首次提交前→`submission-auditor`；触发不等于授权，不提前建 Memory/Planning/Swarm 或治理框架。
- TASK_RESULT：基线/父链、交付身份、验证边界、证据路径/hold、live 次数/失败/未知、review 决策；区分 FACT / INFERENCE / RECOMMENDATION。格式/ETA 归 Task/通用 Skill。
