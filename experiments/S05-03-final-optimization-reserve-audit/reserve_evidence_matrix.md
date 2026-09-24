# S05-03｜离线剩余空间证据与采纳矩阵

本文件只分析公开 Dev 分发元数据、已冻结源码和身份匹配的 S04 历史公开轨迹。`OBSERVED` 是记录中的公开状态/选择或源码行为，不是反事实收益；`INFERENCE` 不进入运行时为隐藏阈值或固定答案。未来分数收益、稳定 80+ 与独立因果效应均为 `NOT_PROVEN`。父候选及其 [离线证据](../S05-02-integrated-offline-optimization/offline_evidence_matrix.md) 保持不变。

## 证据身份与边界

- `origin/main=7fc741cadc950608ff190ff10d7a001584e99dcc`；父 HEAD `9413b7678885acb8cd8fb28dc1c92b85714574b7`，父候选实现提交 `667696a22ee4c2d1b4e5d7596239d4b0e0939a0f`。父分支相对 main 为 `ahead 2 / behind 0`，merge-base 为 main。
- 冻结 Runner：`f61c738c72e51b77298cc1c14c7c6ebf4b6c527d`。本机只读发行版元数据：`D:/CS/CareerSim/.venv/Lib/site-packages/jiuwenswarm-0.2.4b3.dist-info/METADATA` 为 `jiuwenswarm 0.2.4b3`，其依赖 `openjiuwen==0.1.16.post2`；源码分别在相邻 `jiuwenswarm/`、`openjiuwen/`。未 import、启动或更改 instance。
- 两局 raw 在阅读前重新按提交的 [Run #1 trajectory](../S04-04-high-score-confirmation/candidate_run1_trajectory.json)、[Run #2 trajectory](../S04-04-high-score-confirmation/candidate_run2_trajectory.json) 核验。Run #1 events `2,027,675` bytes / SHA256 `a964db295f0135f4dc41f135b3ed3d8513a196fbbb689f36d47f76c957ef7d79`，transcript `753,385` / `49cbfcee32dd88d1573d4e0a068de543e3993d45384dc72854bfa91aaebfec71`；Run #2 events `1,019,202` / `9a266a84937b40899b6f2fdcbbb8fdefd74c825e57dd1ea484e52c6e4b9e22b6`，transcript `312,900` / `9f3082d4decb46f8e64c6ff6df736900cf8d4810ff528d37ee3f0451581a66b0`。四项均匹配，原件只读；没有将终局知识当作此前决策输入。
- 公开分发包 `career-emulator-bdci26==1.0.0` 的 `dev/dataset`：`192` 个 `.data`，合计 `243,490` bytes；按目录为 action_pool `171`、promotion `3`、salary_conditions `3`、failure_conditions `7`、initialization_n_regular `4`、performance_score `1`、ending_score `1`、talk_mechanism `2`。身份摘要 `be91bc0b0d72204ce06c2f4b9030d041c52e82a489c201d95a5f90c7f2629b52`，算法为相对路径排序后每行 `relative/path byte_length lowercase_sha256`，以 LF 连接并对 UTF-8 文本取 SHA256。文件是非明文 `.data`；本任务只读文件级元数据，没有加载/重建 emulator DB、解码事件或查看 test/private split。因而不能从该 corpus 提取可靠的 choice-effect taxonomy；它只证明公开 Dev 分发身份与分类规模。
- Source Lock 所列公开文档本轮在线访问不可用；没有据此认定官方合同漂移。晋升六个月窗口、公开状态字段与阈值不公开的边界沿用已锁定 [OFFICIAL_SOURCE_LOCK](../../docs/project/OFFICIAL_SOURCE_LOCK.md) 和已验证的公开轨迹；没有以当前网页替换冻结版本。

## A｜长程遵循与恢复

| 问题 | 证据等级 / 锚点 | 结论 |
|---|---|---|
| `IDENTITY.md` | `SOURCE_CONFIRMED`：Runner `install.py::_write_identity_md` 写入姓名/Skill 列表与策略；`openjiuwen/harness/rails/context_engineer/context_assemble_rail.py::before_model_call` 每次构建 context sections，`prompts/sections/context.py::build_context_file_sections` 包含 `IDENTITY.md`。 | 有每次调用的源码恢复路径；实际每次成功送达模型未经本任务 live 验证。Runner 关于压缩后仍在 system prompt 的注释与源码一致，但不能替代运行观测。 |
| Skill 内容 | `SOURCE_CONFIRMED`：冻结包 `jiuwenswarm/resources/config.yaml` 模板为 `skill_mode: all`；adapter `_resolve_skill_mode` 默认/回退 all；在 all mode 下 `SkillUseRail.before_model_call/_build_skills_section` 重建 session-baseline 名称/描述，`SkillTool.invoke` 才读取完整 `SKILL.md`。当前 instance 实际 override 未读，标 `UNKNOWN`。 | 名称/描述不是完整指令；auto_list mode 下不能保证描述逐次注入。早期一次 `skill_tool` 读取不保证晚期正文仍在有效上下文，也不能单凭一次读取证明失效。 |
| 压缩 / session memory | `SOURCE_CONFIRMED`：JiuwenSwarm `interface_deep.py::_update_agent_rails` 在 `context_engine_config.enabled` 下注册 `ContextProcessorRail`；其 preset 含压缩器。适配器传入 `session_memory`，但当前 `openjiuwen/.../context_processor_rail.py::__init__` 明确标为 deprecated/ignored；`SessionMemoryCompressorConfig.enabled` 默认 `False`。 | 压缩能力存在；本两局具体触发次数、压缩后保留的历史细节为 `UNKNOWN`。不能声称 session memory 已自动工作。 |
| fresh / continue | `SOURCE_CONFIRMED`：Runner `headless_play.py::resolve_drive_session_id` fresh 生成新 drive ID，`--continue` 复用上次 drive；`ws_client.py::build_continue_prompt` 与 `prompts/play_headless_continue.md` 提供 game ID、要求 observe/check_latest_logs；`prompts/identity.md` 也规定上下文不足时先 observe。 | drive ID 不等于 CareerSim game ID；历史上下文恢复必须核对当前 game ID 与新鲜公开 observe。 |
| 历史早/中/晚 | `OBSERVED`：Run #1 切 M1–12 / M13–30 / M31–48；Run #2 切 M1–12 / M13–25 / late 未到达。两局 events 均在最初四次 `skill_tool` 载入完整 Skill，之后无再次载入。两局各有三个正式 Planning checkpoint，均在早期；Run #1 晚期仍讨论 Output/Network/Health 和公开风险，M36 两次 `check_latest_logs` 为核对季度动作格式；Run #2 的 Board 字段记录见早/中期，最后可定位的 `game_session_id` 字段在 M15，M24–25 仍有 Risk/战略推理。 | **正式 checkpoint 后期缺失是观察事实**，但 late free-form 推理不等于所有 Skill 遗忘；`check_latest_logs` 也不能证明压缩。Run #2 无 late window。`LONG_HORIZON_ADHERENCE_BOTTLENECK = INCONCLUSIVE`，更窄的“失去 checkpoint 后缺少明确恢复入口”是合同健壮性缺口。 |

决定：只 `ADOPT` 一个 Planning recovery cue。把继续/上下文丢失写进默认 all mode 下持续可见的 Skill description，并在正文要求同局、新鲜 observe、重建目标；旧 checkpoint 无法验证时进展为 `unknown`。实际 instance override 与未来 cloud mode 未核，须在 Game Gate 前核对身份；此处不假装模型必遵循，也不写持久状态或要求每月重复读 Skill。若未来 benchmark 从未出现 continuation/context-loss trigger，结果为 `NOT_OBSERVED`。

## B｜结构化 Memory / 恢复

| Gate | 当前事实 / 风险 | 判定 |
|---|---|---|
| 可用 surface | Runner `install.py::install_submission` 清理 `memory/*.md` 并重建 generic `MEMORY.md`；`jiuwenswarm/common/utils.py::get_agent_memory_dir` 指向共享 agent workspace。`openjiuwen/harness/prompts/workspace_content/workspace_header.py::CONTEXT_FILES` 不含 `MEMORY.md`，故 ContextAssembleRail 不自动逐次注入它。另有 `projects/<drive_session_id>` 路径与底层 session-memory compressor。 | 有 framework surface，不等于可提交的策略记忆。 |
| session scope / freshness | 共享 `MEMORY.md` 非 game scoped；install 会覆盖，fresh drive ID 不自动清理所有 project paths。`SessionMemoryCompressor` 可按 session 路径组织，但默认关闭，适配器当前传入参数被忽略。 | game-session 隔离与压缩后自动恢复未建立。 |
| 可移植 / cloud | 提交合同是 Skill bundle；当前 accepted path 无参赛者自有、经确认可打包并自动启用的 memory hook。启用框架能力需要 config/Runner 范围；本机残留目录不能作为云端保证。 | portability / cloud reproducibility 为 `UNKNOWN`，不允许依赖。 |
| 成本/收益 | Board 已同局、限量、freshness keyed；历史 Board post-action refresh 仅 partial。没有证据证明文件持久化比该方案更安全或高效。 | 附加状态、污染、token 与误读风险大于已证明收益。 |

`H_SESSION_SCOPED_RECOVERY_MEMORY = UNPROVEN`；`DEFER_MEMORY`。保留现有 Board 的 in-conversation / game-session-keyed fallback；本轮只做 Planning 重新建目标，不把它改名为 Memory。无 memory write/read，R13 仅验证无跨局复用规则，R14 记 `NOT_APPLICABLE`。

## C｜晋升、财富与公开分数空间

| 公开证据 | 可推广信号 | 禁止的推断 |
|---|---|---|
| [Run #1 trajectory](../S04-04-high-score-confirmation/candidate_run1_trajectory.json)：M18 L4/Skill44/Network19/Output16/Wealth6；M24 L4/63/36/26/10；M30 L4/82/36/26/15；M36 L5/100/36/29/21；M48 L6/138/51/40/39。M30 公开半年反馈为 A、建议把精力放在产出/关系。 | 每个公开绩效/晋升窗口结合 Level、已停留月份、当前目标和新鲜 Skill/Network/Output/反馈复核；M24–30 Network/Output 持平是可见的目标进展问题。现有 Planning 已按目标 `advancing/stalled/unknown` 与季度/半年反馈重审。 | 不推断 Skill/Network/Output 晋升阈值、某个月必晋升，也不将终局权重放入运行时。M30 反馈不能解释早于 M30 的决策。 |
| Run #1 Wealth M18→24→30→36→42→48 为 `6→10→15→21→30→39`；既在 L4 平台期也在晋升时增长。[S05-02 分数拆解](../S05-02-integrated-offline-optimization/offline_evidence_matrix.md) 有 76.04→80 的 3.96 差距，Level/Wealth 理论 headroom 较大。 | 当前合法财富机会可以和其它公开收益、成本一起比较；若出现新鲜、直接且明确的补偿/财富事实可记录。 | 不能把 Wealth 增量拆为 salary、promotion、bonus、story 或独立动作的因果贡献；理论 headroom 不是可达收益。`WEALTH_MECHANISM = DEFER`。 |
| Dev 包文件级分类与历史 public observe；没有解码事件、固定答案表或隐藏配置分析。 | 仅可确认公开 Dev 包有 action pool、salary/promotion 等类别；一般化 option-effect taxonomy 仍 `EVIDENCE_LIMITED`。 | 不从 `.data` 逆推 event-title→choice、隐藏阈值或 Test。 |

专门 promotion-readiness 规则 `DEFER`：既有 Planning 已涵盖公开绩效/Level/资源差距、季度与半年复核、平台期重新比较；增加同义规则不正交。专门 wealth heuristic `DEFER`。R15/R16 以现有通用合同处理，而非声称新效果。

## D｜高影响错误去重（seed 不是事实）

| Seed | 仓库/已核验 raw 锚点与复现范围 | 潜在影响；owner / 覆盖 | 新机制与误报风险 |
|---|---|---|---|
| 道德正确⇒后果安全、近期晋升⇒安全 | Run #2 transcript M24：VP 转岗威胁，模型以“坚守原则”及刚升 L4 为继续理由；M25 公开打压升级后选择举报，随后终局。单路径，不能证明单动作因果。 | HIGH tail；Planning 已明确 principle/recent promotion 不证安全，严重后果重排；Risk 检查候选警告。`YES`（合同），执行收益未知。 | 新常驻 rubric 易把正常维护权益误判为必须退让；Run #1 也存在不同公开情境下的正当、有分寸行动。 |
| 假性风险消解 | Run #2 transcript M17 将普通 HR 赞许称作“风险缓解信号”，此前有风险提示；未见明确风险解除。一次清晰 reasoning defect。 | HIGH tail；Board observed/inferred 分开，Planning 明禁 praise/silence 当作 resolution。`YES`。 | 再加一条“赞许≠解除”重复父合同；勿发明风险数值。 |
| 重复动作惯性 / 机会成本 | Run #1 16/16 季度 main action 同名；Run #2 M12 另选一次。没有反事实；S05-02 已分析 Energy trade-off。 | MEDIUM–HIGH 但不证损分；Planning prior-objective progress、合法替代和 Energy/opportunity cost。`YES`。 | 强制切换会伤害观察到持续进展的路径。 |
| 饱和分量 / composite shortcut | Run #2 M18 transcript 一处将含满值 Dignity 的复合选项整体排除；Run #1 和 Run #2 早期亦有正确分量比较。 | MEDIUM；Planning 现有仍有用分量与成本比较。`YES`。 | 固定复合加分或固定避开选项会产生相反误报。 |
| 升级盲点 | Run #2 M24 爆雷与 M25 VP 升级可见，结局是信任危机；动作与结局间的隐藏机制未知。 | HIGH tail；Planning 严重后果/持续升级比较、Risk 当前候选。`YES`（合同），有效性未证。 | 无条件退避会丧失合法成长/维权机会。 |

原 Project/Astra red-team 原件未在本次仓库证据中定位；未把聊天 seed 当成独立 finding。额外 high-impact rubric `DEFER`：核心字段已由 Planning/ Risk/ Board 的现有职责覆盖，重复常驻检查会增加低影响事件误报与 token 消耗。第五 Skill 门禁第 2、4、10 项（现有 owner 可承担、正交、优于最小规则）均未过，`DEFER_NEW_SKILL`。没有强 role-separation bottleneck，`H_TEAM_ROLE_SEPARATION_READY_FOR_MAIN_REVIEW = NO`；Team/Swarm 继续 deferred。

## Global Adoption Gate（所有机制）

| Mechanism | Evidence | Leverage / stable-80 relevance | Orthogonality | Context cost / observability | Regression / hidden-info risk / complexity | Decision |
|---|---|---|---|---|---|---|
| Planning continuation recovery cue | MEDIUM（源码持续描述 + 两局早期后无正式 checkpoint）；长程方差相关，收益未证 | MEDIUM / 可降低目标丢失风险 | YES，补缺口而非重做 Risk/Board | LOW / 在发生 continuation 时可观察再次读取、fresh observe 与新 checkpoint | LOW / NONE / LOW；R11–R13 有反例 | **ADOPT**，仅改 Planning description + 一条 trigger + 同局 unknown fallback。 |
| Durable/session memory | LOW；潜在长程收益 UNKNOWN | 可能相关但无法量化 | 不明 | MEDIUM–HIGH / cloud 观测未知 | HIGH contamination / NONE / HIGH；packageability 未证 | **DEFER**。 |
| Dedicated promotion-readiness rule | MEDIUM 描述性；理论 headroom HIGH、增量收益 UNKNOWN | 目标相关 | LOW，父 Planning 已覆盖 | LOW–MEDIUM / 可观测 | MEDIUM 重复判断 / 阈值泄漏风险 / LOW | **DEFER**；保留通用平台期复核。 |
| Dedicated wealth action rule | LOW 因果；理论 headroom HIGH、可达性 UNKNOWN | 目标相关 | UNKNOWN | MEDIUM / 部分可观测 | HIGH confounding / 隐藏效果误推 / MEDIUM | **DEFER**。 |
| Universal high-impact rubric | MEDIUM 单路径；tail relevance 可能 HIGH | 相关 | LOW，Planning/Risk 已覆盖 | MEDIUM–HIGH / trigger 易误报 | MEDIUM / 无需隐藏信息但误判大 / MEDIUM | **DEFER**；保留现有严重后果触发。 |
| Fifth Skill / Team | NONE 对独立职责收益；稳定收益 UNKNOWN | 未证 | NO | HIGH / 低 | HIGH / NONE / HIGH | **DEFER**，无实现。 |
| Hidden threshold / score weight / event-answer lookup | 无合法决策时证据 | 不可用 | NO | HIGH / 不可审 | HIGH / HIGH / HIGH | **REJECT**。 |

采纳后候选只比 `candidate-v2c-integrated-planning` 增加一个恢复语义；不是根据 S04 事件标题选择动作。所有具体轨迹、结局与评估权重只留在离线证据。下一次 benchmark 可证实“是否执行该语义”，单局不能证明稳定 80+、因果改善或隐藏 Test 泛化。
