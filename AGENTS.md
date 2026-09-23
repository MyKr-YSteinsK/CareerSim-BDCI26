# AGENTS.md

> CareerSim 长期边界；通用流程由 `frugal-dev-runner` / Task 管理。

## 1. 身份与事实归属

- `MyKr-YSteinsK/CareerSim-BDCI26`；`main`；Windows / PowerShell。`docs/project/`：`CURRENT_STATE.md` 管状态，`ARCHITECTURE_DECISIONS.md` 管架构，`OFFICIAL_SOURCE_LOCK.md` 管官方事实、冻结身份和运行/提交合同；实测见 `ENVIRONMENT.md` / 实验 RESULT。
- 分支增量标记 `IN_FLIGHT_EVIDENCE`，不冒充 `MERGED_FACT`；历史按当时语境解读。官方身份变更须新证据/可比较配置，不覆盖旧结果。
- 凭据、`.env`、cache、日志、DB、会话和本机生成状态不得提交；仅提交去敏的必要证据。不得静默改 frozen Runner、依赖或 `uv.lock`。

## 2. 本机 Workspace

- 固定 `D:\CS\CareerSim\.local\`：`worktrees/<task>` 放 checkout，`runtime/<task-or-run>` 放可控输出/留存证据，`upstream/<identity>` 放官方参考，`scratch/<task>` 放可再生派生物；整体 gitignored。
- 禁止新建 `D:\CS\CareerSim-*` 临时目录；旧路径不自动迁删。迁移另立任务，记路径映射/hash 并修复引用。
- 例外：checkout 内 `.career_sim_runner/`、根 `.venv`、用户目录 `.jiuwenswarm-instances/career_emu` 保持既定路径/ignore；RESULT 记录位置，不为归置改冻结 runtime。唯一取证来源不得放 scratch。

## 3. Worktree / stacked task

- 实质改动用 `codex/<task>` + `.local/worktrees/<task>`；一 branch 一 worktree。独立任务基于 fetch 后最新 `origin/main`；依赖未合入代码/证据/状态的任务基于父任务已验证 HEAD，不从 main 复制或拼接临时状态。
- Task/RESULT 记录 Base SHA（起点）、Parent branch/SHA（独立为 none）、依赖/验证边界；技术失败证据不等于实现通过。
- 父先合、子后合。父合入后子核对 ancestry/剩余 diff，必要时 merge main 复验；squash 等祖先不等价由 Main 决定整合，不重写已推送历史。父被拒绝/重做时依赖子停工并重定基线。
- 不设数字链长；每层说明依赖。跨 Stage、父方向未定或整链难以评审时，先返 Main 决定合入/截断。
- 执行/review/复现/取证期间为 active。COMPLETE 不等于可删；未合入/待审、唯一 raw、未决取证、依赖路径的 child 或 Main 留存要求，须记原因、责任 Task、解除条件/下次 review 点，不以“以后有用”保留。
- 清理获授权、review 有结论、改动已交付且 raw/引用/child 路径依赖解除后，才 `git worktree remove`；保留必要 commit，不强删。runtime 不随 worktree 删除；child 仅依赖 commit 不阻止移除父目录。`git worktree prune` 只清已确认 stale metadata，先 dry-run，不例行执行。

## 4. Runtime Evidence Lifecycle

- Canonical：去敏 RESULT/manifest/compact evidence；记 Experiment/Run/session、版本/config、假设/修改/基线、次数/时间、score/token/runtime、失败/决策、路径/bytes/hash；未知标明，缺失 usage 不记零。
- Raw：transcript/events、服务日志、DB/session、provider usage、临时配置留本地。失败未决、结论依赖 raw、摘要不能独立解释或唯一复验来源须留存；hash 不替代源文件。
- `FORENSIC_HOLD` 在 RESULT/manifest 记原因、最小文件/时间窗/路径/hash、责任 Task/解除者、解除条件/复查点；安装/清理可能覆盖时先授权保全快照，不以事后状态冒充历史。
- Evidence Closure：责任 Task 提供独立可审结论/compact 证据，核实必要来源可恢复或无需复析，复现/child 等依赖已解除；Main/Stage 接受并记 hold 解除。之后仅授权清理可删指定 raw，记范围/复验限制；hash 或 COMPLETE 不自动关闭。

## 5. Task 权限 / shared runtime / retry

- `READ_ONLY`：读 repo/Git/必要去敏证据、离线分析；不改 repo/runtime、不调用 provider。
- `REPOSITORY_WRITE`：范围内 patch、offline/static 验证、授权 commit/push；不隐含 `LIVE_RUN`，validate 不保证无副作用。
- `LIVE_RUN` 须 Task 明列依赖/Skill/submission 安装、服务/MCP、provider、game、smoke/benchmark、比赛提交的允许动作、次数/成本及停止条件；未列不授权，服务启动可能调用模型。
- `career_emu` 未证隔离前，安装/reload/对局/共享 DB/config 写入均串行；先确认独占窗口。worktree 不等于隔离，不依赖跨局残留。
- 无副作用确定性读取可有限 retry。`new_game`、`take_action`、install、provider/submission、共享写入或 MCP 调用遇超时/断连/partial/unknown outcome：先查状态/日志，在授权内 observe 核对；仍不明则停并留证，不盲重发。
- live 授权不等于无限 retry；bounded smoke 达上限或触发 TECHNICAL_FAILURE 停止条件即返回 review，不为取得成功重跑。

## 6. 架构与返回 Review

- Single Agent + Multiple Skills；唯一提交者用当前 session/新鲜观察，回执后更新状态。设计/安装/加载/应用/收益分开举证；单局不决定路线，不编造隐藏阈值。架构变化依 ADR：Hypothesis → Experiment → Decision。
- Main Hub 管全局/验收，Stage 管任务，Codex 实现回传。验收/路线改变、假设推翻、超范围 blocker、runtime 异常、额外 live/retry 预算、Source Lock/依赖漂移、parent 失效、需改 frozen Runner 或建辅助 Skill 时返 Main/Stage；不自行扩 scope 或宣布 Stage COMPLETE。
- 辅助 Skill 触发：重复记账→`experiment-manager`，重复框架排障→`framework-debugger`，首次提交前→`submission-auditor`；触发不等于授权，不提前建 Memory/Planning/Swarm 或治理框架。
- TASK_RESULT：基线/父链、交付身份、验证边界、证据路径/hold、live 次数/失败/未知、review 决策；区分 FACT / INFERENCE / RECOMMENDATION。格式/ETA 归 Task/通用 Skill。
