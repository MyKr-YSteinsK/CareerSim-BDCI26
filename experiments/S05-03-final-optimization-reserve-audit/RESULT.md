# S05-03｜稳定 80+ 剩余优化空间离线审计结果

## 身份、状态与边界

- **Status:** `COMPLETE`（repository-only / static contract）。**Decision:** `FINAL_CANDIDATE_OFFLINE_READY_FOR_MAIN_GAME_GATE`，仍须 S05 Stage Review 与 Main 独立 Game Gate；本任务不授权下一局。
- **Branch / parent:** `codex/s05-03-final-optimization-reserve-audit` 自 `codex/s05-02-integrated-offline-optimization@9413b7678885acb8cd8fb28dc1c92b85714574b7` 建立；`origin/main=7fc741cadc950608ff190ff10d7a001584e99dcc`，父相对 main `ahead 2 / behind 0`，merge-base 为 main。未 merge main、未修改父历史件。
- Main 明确提供 S05-02 `Stage Review = PASS`、`INTEGRATED_CANDIDATE_OFFLINE_ACCEPTED`；本任务继承已接受候选 `candidate-v2c-integrated-planning`，并只在动态 [CURRENT_STATE](../../docs/project/CURRENT_STATE.md) / [ADR](../../docs/project/ARCHITECTURE_DECISIONS.md) 将父分支旧 `IN_FLIGHT_EVIDENCE` 修正为已接受但未合入。父 S05-02 RESULT/manifest/matrices 保持提交时语境，未回写。
- TARGET=`STABLE_QUANTITATIVE_80_PLUS` 是目标，不是实现事实。Candidate v1 两局分数 `76.04` 与 `35.31`，不构成 n=2 因果证据；最终候选 gameplay effectiveness=`NOT_PROVEN`，stable 80+=`NOT_PROVEN`。S05 未宣布完成，Team/Swarm 仍 deferred。

## Evidence → Investigation → Decision → Implementation → Verification

[reserve_evidence_matrix.md](reserve_evidence_matrix.md) 记录 A–D 的原始身份、精确源码符号、事实/推断/未知、错误 taxonomy 及逐项 Adoption Gate。四份 S04 raw transcript/events 在读取前重算 bytes/SHA256，均与已提交 trajectory 匹配；未读隐藏/test、未调用 provider/game。JiuwenSwarm 本机发行版元数据确认为 `0.2.4b3`，底层 openjiuwen `0.1.16.post2`。官方网页本轮不可达，没有从网页引入新运行合同或认定 Source Lock 漂移。

### A｜长程遵循

源码证明：Runner 安装的 `IDENTITY.md` 可经 ContextAssembleRail 在每模型调用重建；SkillUseRail 的 session-baseline 名称/描述可重建，完整 `SKILL.md` 要由 `skill_tool` / 文件工具读取。两局均仅在开局各载入四 Skill；正式 Planning checkpoint 各三次，集中于 M1–12。Run #1 M13–48 仍有公开资源/风险推理和 M36 的两次日志查询，Run #2 到 M25、无 late window；两局没有足够事件证明何时发生了上下文压缩或 Skill 指令失效。故 `LONG_HORIZON_ADHERENCE_BOTTLENECK = INCONCLUSIVE`，不是“late model 不遵循”的事实。能确认的较小合同缺口是失去旧 checkpoint 后缺少明确的 Planning 恢复入口。

**ADOPT：**仅在 [rolling-planning](../../skills/rolling-planning/SKILL.md) 增加 continuation/context-loss 触发、重读提示和同 game / fresh public observe 重建。旧目标无可靠同局 bounded evidence 时 prior progress=`unknown`，不得静默复用。冻结包默认 `skill_mode: all` 下，该 cue 的 description 会进入每次模型调用的 Skill section；实际 instance/cloud override 未验证，须在未来 Game Gate 核对。是否真执行须未来授权 game 观测，不能以静态源码当作模型遵循证明。未追加每月常驻 review、action marker 或 telemetry。

### B｜Memory / 恢复

Runner install 清理共享 `memory/*.md` 并重建 generic `MEMORY.md`。JiuwenSwarm 有 workspace/global memory 和项目 session 路径，底层有 session-memory compressor，但在冻结版本中适配器传入的 `session_memory` 参数被底层标为 ignored，compressor 默认 disabled。当前 Skill bundle 没有已确认可打包、自动启用、可隔离 CareerSim game ID 且云端可复现的持久 hook；本机残留不可用作保证。`H_SESSION_SCOPED_RECOVERY_MEMORY = UNPROVEN`，`DEFER_MEMORY`。沿用 Board 同局、限量、新鲜观察重建；不写 Memory、配置、Runner 或数据库。

### C｜晋升 / Wealth / public Dev

Run #1 从 M18 L4 到 M36 L5、M48 L6；M24–M30 Skill `63→82` 而 Network/Output `36→36` / `26→26`，可做目标进展与公开反馈复核，不能推出晋升阈值。父候选已经覆盖 quarterly/semiannual review、prior objective `advancing/stalled/unknown`、合法替代比较。专门 promotion-readiness 规则 `DEFER`（重复而不正交）。Wealth M18/24/30/36/42/48 为 `6/10/15/21/30/39`，既在平台期又在晋升时上升；salary/bonus/story/promotion/独立动作不可分，`WEALTH_MECHANISM = DEFER`。合法财富机会仍受现有公开收益/成本通用比较约束。

只读识别公开 `career-emulator-bdci26==1.0.0` 的 dev/dataset 192 个 `.data`、文件级 SHA256 manifest；内容非明文，未加载/重建 DB、未读取 test/private，也未做 event-answer 或隐藏阈值提取。因此 Dev 对可推广 effect taxonomy 的本轮证据为 `EVIDENCE_LIMITED`；该限制不是加入猜测规则的理由。76.04→80 的 3.96 差距和 Level/Wealth 理论 headroom 仅用于**离线优先级**，绝不进入运行时 evaluator-weight rule。

### D｜高影响错误去重

Run #2 M17 将普通赞许推断为风险缓解、M24 以近期晋升和正当立场降低后果警惕、M25 公开奖惩/打压升级；这是一条观察路径，不能把任何单动作认定为终局因果。Run #1 重复季度 main action `16/16` 与 Run #2 M18 的饱和分量 shortcut 也已由父 Planning 的 progress/复合收益规则覆盖。现有分工：Board=facts/freshness，Planning=目标与严重后果路径，Risk=警告驱动的当前候选，Trace=marker-only；Single Agent 唯一 action submitter。通用 high-impact rubric `DEFER`（与 Planning/Risk 重叠、普通事件误报成本）；第五 Skill 门禁未过，`DEFER_NEW_SKILL`。无强 role-separation 证据，Team/Swarm 不升级。

## 最终 Candidate 冻结

- [candidate_manifest.json](candidate_manifest.json)：`candidate-v2-final-offline`，父为 `candidate-v2c-integrated-planning`。唯一 Skill delta 是 Planning context-loss recovery cue；Risk/Board/Trace 与父 Git blob byte-identical。4 Skill Git blob 总量 `15,729→16,078` bytes（`+349`，`+2.22%`），265 lines，硬上限 `16,515`；没有第五 Skill、持久 Memory、Runner/lock 改动。
- 这个 delta 以框架载入/上下文源码和通用 freshness 规则为基础，不使用 S04 具体事件标题或固定动作；S04 的早期集中 checkpoint 只用于审计可能的长程恢复风险，不构成“压缩导致损分”或收益证明。
- [static_regression_matrix.md](static_regression_matrix.md)：父 R1–R10 `10/10 PASS` 保留；R11–R20 `7 PASS / 3 NOT_APPLICABLE`；一轮 integrated semantic revision，无 blocking case。全部仅为 `PASS_WRITTEN_CONTRACT_ONLY`。
- [benchmark_observation_matrix.md](benchmark_observation_matrix.md) 作为后继未来观测合同，链接父矩阵，明确早/中/晚 Skill adherence、恢复/Board freshness、跨局污染、父机制、平台/财富、R17/R18 不适用边界、M6/12/18/24/36/48、终局维度、成本与失败分类。定义 PASS/FAIL/NOT_OBSERVED/UNKNOWN；触发缺席不算失败。
- `NEXT_GAME = DEFERRED_FOR_FINAL_OPTIMIZATION_RESERVE_AUDIT`；本任务的 offline-ready 只允许返回 Main Game Gate 审议，不允许自行 benchmark。`Risk Hypothesis=ACTIVE`、Risk effectiveness=`NOT_PROVEN`、controlled screening=`NOT_STARTED`。

## Verification / 问题

- Lineage、父提交和 Main anchor：PASS。Git `career_sim_runner` tree、`pyproject.toml`、`uv.lock`、Trace/Risk/Board blob：未改；Planning blob、四 Skill 总 byte/line、YAML frontmatter/唯一名称、职责、无固定 event answer/hidden threshold/score weight：PASS。
- 原始四件 raw identity PASS 且只读；公开 Dev 仅 dev 文件级摘要，test/private 未读；JSON parse、Markdown 相对链接、`git diff --check`、scope/secret/runtime artifact、commit/push/remote/clean 由交付检查完成。任何尚未完成的 delivery 结果只在最终 TASK_RESULT 报告，不把预期写成已发生。
- Live-operation proof：competition provider requests `0`；service starts `0`；Skill installs/reloads `0`；MCP runtime calls `0`；`new_game` `0`；runtime `observe` `0`；`take_action` `0`；Runner play `0`；full game `0`；competition submission `0`。
- 主要未知：真实压缩频率、后期 Skill 再读与遵循、恢复 cue 是否实际触发、财富增长分解、promotion 隐藏条件、一次 future run 的随机机会路径与 Cloud 行为。官方网页本轮不可达；源代码可核验的事实仍在冻结本机版本下成立。除极小恢复提示外，没有额外规则通过采纳门槛；不为了 80+ 目标强加机制。
- 只读诊断中有 5 次可避免的路径/命令构造问题（一个 Python 转义、一个 Markdown regex、一个 tree rev-parse、两个不存在/无效 glob 路径），均在目标 mutation 前失败或只影响查询；修正后静态检查通过。Consumed Live Budget=`NO`。以后结构化摘要优先用独立、已知路径的简单检查，而不是多层内联转义。

Next: `RETURN_TO_MAIN_WITH_FINAL_CANDIDATE_OFFLINE_READY_FOR_GAME_GATE`，按父先合、子后合 review；不能在本任务运行下一局。
