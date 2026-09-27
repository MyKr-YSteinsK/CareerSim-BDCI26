# S07-22｜全局策略与 Skill 架构复审

## 结论

- **唯一推荐：4-Skill Single Agent，作为 Candidate v7 的设计提案；不在本 Task 实施。** 第四个 `delivery-progress` 仅维护公开 opportunity → commitment → delivery → evidence → recognition 生命周期，按相关事件稀疏触发。
- **Team：`TEAM_DEFERRED`。** 现有公开证据没有证明 Single Agent 存在由角色冲突造成的能力瓶颈，也没有证明 Team 的收益能覆盖同步、延迟和 token 成本。
- **策略判断：** 以 48 个月剩余职业轨迹和 terminal option value 为全局目标；晋升是有价值的中期信号，交付兑现是把机会转成可验证成果的机制。两者都不是隐藏分数的替代指标，也不能按固定月份、次数或阈值硬编码。
- **证据强度：** 晋升/等级轨迹的预测价值为低置信度假设；活动与结果必须分开记录，有较强的描述性支持；任何 Skill 或动作对得分的因果贡献仍未知。

本结论是供 Main/Stage 审查的架构建议，不修改当前 v6c Candidate、manifest、三项 Skill、ADR 或 `CURRENT_STATE.md`，也不授权下一局。

## 身份与边界

- 基线：`main@847f6036097bc3fffbae17ae89772f5fe7f7798f`；执行前 `git fetch origin` 后 `HEAD == origin/main`，工作区干净。
- 本 Task：离线策略与架构复审、v7 设计；`REPOSITORY_WRITE`；Live Authorization 为 `NONE`。
- 策略判断只使用官方公开事实、公开状态/选项/回执与已提交公开轨迹。没有读取 SQLite、隐藏状态、解码事件、私有评估公式或 S06-09 取证材料。
- `OFFICIAL_SOURCE_LOCK.md` 说明官方评估兼有量化表现、策略工程质量与资源效能，最终阶段公开记录为云评测加专家评审；隐藏云端权重未知。Skills 设计、Skills 协同、长期一致性和云端评测作为 Plan 记录的 **USER-PROVIDED COMPETITION CRITERION**，不据此推断 Skill 数量或 Team 会加分。
- Runner 合同允许 manifest 的 `mode` 为 `agent` 或 `team`（`OFFICIAL_SOURCE_LOCK.md` § Agent 模式范围；`career_sim_runner/constants.py`）；当前 manifest 实际为 `mode=agent`。此静态能力不证明 AgentServer 下的共享状态、角色隔离、唯一工具提交者或 Team 表现，均列为 UNKNOWN。
- 当前 `ARCHITECTURE_DECISIONS.md` 的 AD-001/003/005/007 仍是工程事实：Single Agent + 三 Skills；Board 管当前公开事实，Planning 管策略状态；Memory、第五 Skill 与 Team 保持 deferred，架构调整需 Main review。此处只是形成待审提案。

## 全局目标与长短期一致性

不声称求得隐藏评分器下的数学全局最优。可部署目标应为：

> 在合规、生存及有公开依据的重大风险约束下，稳健提升剩余职业生涯的 progression、可见交付、复利资产和终局选择空间。

将 Safety 作为约束，不默认当作唯一优化目标。Level/promotion、Skill、Network、Output、Wealth 和后续机会都是公开的轨迹维度；没有证据支持给它们配置固定隐藏分数权重。每次局部选择需能说明它如何推进当前 review-window objective，而该 objective 如何服务剩余生涯轨迹。

### `H_PROMOTION_COMPOUNDING`

**支持性公开观察：**

- Candidate v1 #1：`76.04 / 53.23 / 48m / A`，终局 L6；公开记录有 M6、M12、M18、M36、M48 晋升，16/16 个季度主行动为关键项目申请。终局 Skill 139、Network 51、Output 40、Wealth 39。来源：`RUN_HISTORY.md` 的 Candidate v1 #1 记录及 S07 public closeout。
- Candidate v1 #2：`35.31 / 24.72 / 25m / D`，M6/M12/M24 晋升，之后因第二次 trust-crisis 提前终止。它说明早期晋升本身不保证生存或高分。
- 原 v6 Run #1：`75.29 / 52.70 / 48m / A`，公开轨迹记录了多次晋升；但 runtime adherence 失败，不是可直接照搬的执行模板。
- S06 Run #1：`53.83 / 37.68 / 48m / C`、L4，同样 16/16 关键项目申请；Candidate 身份在 compact evidence 中为 UNKNOWN。对照说明行动计数不是成绩配方。
- S07-21：`59.19 / 41.43 / 48m / C`、L5、Output 29、Wealth 24，晋升于 M12/M18/M30/M48；仅 65/200 条决策记录有同期完整 controller 记录，模型/effort 仍 UNKNOWN。
- S07-19、S07-20 分别在 M24 以 L1/O3、无晋升结束；S07-17 R3 到 48m/L5、`63.88 / 44.72 / B`，仍低于 75+ 历史参考。

**INFERENCE（低置信度）：** 较早出现公开 progression 与后续复利资产同向，值得作为 review-window 反馈和诊断信号；它可能预测机会集扩张，却未被证明是可独立操纵的原因。

**反证及限制：** v1 #2 晋升后仍触发信任危机；S06 与 v1 #1 项目申请频次相同而轨迹差异很大；S07 各局无种子、路径不配对，Candidate、host 与策略执行也不相同。S07-21 的记录缺口进一步限制了策略归因。由这些轨迹不能推出“早期晋升导致高分”。

**可部署语义：** 把公开晋升、review feedback、Level 变化以及与目标相关的可见结果当作 progression feedback；若连续可比 checkpoint 显示目标未推进，重新检查主要阻碍和兑现证据。禁止 M6/M12/M18 必须达到某 Level、隐藏晋升阈值、固定月行动表或以晋升压过重大风险。

### `H_OPPORTUNITY_TO_RECOGNITION`

公开材料反复区分申请/投入/汇报与结果：S07 closeout 记录 v1 #1 与 S06 都是 16/16 关键项目申请，分数却分别为 76.04 与 53.83；S07-15 R4 有大量报告/人脉行动但为 57.90；S07-17 记录 M39 可行性工作没有明确完成回执、M45 demo 有计划而终局前无结果回执、M42 反馈赞扬交付却未归因到某个具名项目。M45 的报告准备/高强度/报告选择也没有立即观察到 Output 增长。

这些事实支持 **activity count ≠ delivery ≠ recognition**，但没有识别哪一项行动带来后续分数或 review 改善。最稳妥的策略机制是跟踪公开证据链：

`Opportunity → Commitment / Ownership → Delivery → Observable Evidence → Recognition / Review Impact`

链上缺少公开回执时保留 `UNKNOWN / UNVERIFIED`。申请不是承诺，承诺不是交付，交付声明不是验证结果，正面反馈也不能自动归因到特定项目。

## 泛化与决策语义

以下是比较候选行动的语义标签，不是数值打分公式或固定权重：

| 特征 | 每次决策要回答的问题 | 未知/证据不足时 |
|---|---|---|
| Material Risk | 是否有公开依据的重大合规、信任、健康或生存风险？ | 不虚构阈值；按明确影响审查，必要时选择可逆候选或获取公开信息 |
| Career Progression Relevance | 是否服务于当前 progression 阻碍、公开 review 或晋升反馈？ | 不因最低指标自动成为 Primary Gap |
| Ownership / Delivery Value | 是否形成有负责人、可验收结果和下一公开节点的承诺？ | Opportunity 留作机会；不记成交付 |
| Observable Evidence / Recognition | 结果是否有公开回执，是否与当前目标或 review 相关？ | 保持未验证；不从行动描述推断成功 |
| Compounding Asset Value | 是否建设 Skill、Network、信誉、Output 或后续选择空间？ | 记录机制假设，等待后续观察 |
| Reversibility | 失败能否撤回、补救或减少长期伤害？ | 不确定时偏向低承诺、可恢复选项 |
| Resource / Opportunity Cost | 时间、Energy、Wealth 与错失其他机会的成本是什么？ | 不套用固定资源阈值或 bundle |
| Dependency / Coordination Burden | 成果是否依赖他人、审批、信息或前置工作？ | 公开标记阻塞项；不把未获确认的依赖当已解决 |
| Remaining Horizon | 距下个 review 与职业终点还有多少公开窗口？ | 按实际公开时间判断，不绑定固定月份策略 |

未知事件先按公开含义归类、识别可核实的目标和风险，再比较合法选项。不得以标题、关键词、选项编号、Dev 事件目录或隐含阈值查表。

## 架构比较

| Dimension | A：增强现有 3 Skills | B：4 Skills / Single Agent | C：最小 Team |
|---|---|---|---|
| Gameplay mechanism | Planning 扩入全局轨迹和交付意识；机制集中但边界较宽 | Planning 管目标，delivery Skill 维护兑现链，责任直接 | Strategist 提议、Executor 协调并唯一提交；可能减少单角色负担 |
| Long-horizon consistency | 可实现，依赖 Planning 同时维护战略与交付状态 | 全局目标与交付状态分开但可组合 | 交接需完整传递全局目标及最新生命周期状态 |
| Skill design clarity | 文件最少、现有 ownership 成熟；Planning 有变宽风险 | 四个责任可分别说明；新增边界需严格保持窄 | Agent role 清晰时可读，重复推理会模糊责任 |
| Multi-Skill coordination quality | 已有 Board→Planning→Risk 合同 | 加入按需 Delivery context，协作链可审计 | 跨 Agent 同步复杂；多 Agent 不等于多 Skill 协同 |
| Hidden-Test generalization | 可用语义原则实现，依赖大 Planning 指令的遵守 | 生命周期结构与事件标题无关，触发需防过度激活 | 对未知事件可分工，但同步错误也会放大未知处理风险 |
| State ownership clarity | Board 拥有公开事实；Planning 可能同时维护目标和兑现过程 | Board=事实、Planning=战略、Delivery=生命周期、Risk=候选风险 | 需定义谁是共享状态权威；双份上下文容易漂移 |
| Token/resource efficiency | 最低固定调用成本；每步 Planning 负担可能增加 | 稀疏触发降低额外成本，触发/摘要本身仍有开销 | 额外 Agent 上下文、往返与延迟最高；确切成本未知 |
| Failure recovery | 复用现有 Board/Planning recovery | 可从 fresh observe 与公开回执重建短 lifecycle；失去上下文时保留 UNKNOWN | 要恢复两个 Agent 的一致状态和未决交接 |
| Auditability | 有现成合同，但生命周期推断可能藏在 Planning 文本中 | 每个 lifecycle 状态有 owner、公开证据和触发点 | 有消息链可查，同时要审交接、重复/冲突提议 |
| Implementation complexity | 最低 | 中等；需要新 Skill 及边界验收 | 最高；需要 orchestration、同步与故障处理 |
| Coordination failure risk | 低，集中决策 | 低至中；风险主要是重复记录或触发过多 | 高于 A/B：状态陈旧、建议冲突、重复推理或提交权混乱 |
| Evidence support | 现有工程结构强；Planning 容量是否足够未测 | 交付链缺口有描述性证据；新增 Skill 改善策略/分数未测 | 无公开证据证明 Team 更有效；AD-005 明确 deferred |
| Main risk | Planning 继续变宽，机会到结果仍无独立状态 | 无因果证据却承担多一份上下文成本；状态设计过细会假精确 | 把角色拆分误当质量收益，成本及同步错误超过机制收益 |

### Option A — Enhanced 3-Skill Single Agent

这是最低成本且最容易沿用的选择。如果 Delivery state 只是一条当前事实，确实适合由 Board 记录，再由 Planning 判断。它未完全解决多行动、多 review 之间的承诺/结果/证据追踪；在 Planning 中扩充该逻辑会削弱其“全球目标和 review 策略”主责的清晰度。没有实现或 ablation 证据表明它不够用，故 A 是有力的保守备选。

### Option B — 4-Skill Single Agent

推荐的理由是**语义状态所有权互补**，不是文件数或分数保证。公开结果链跨越多次行动和 review；Board 的职责是当前事实，Planning 的职责是选择长中短期目标，二者都不应同时维护生命周期阶段及归因。由一个低频、窄职责 Skill 保留待兑现项目及证据状态，可使 Planning 每步只读取短摘要。现有证据支持“值得显式跟踪”，不证明它提高游戏分数；按计划需经 Main/Stage review 后再决定是否实施。

第四 Skill 的 admission criteria 在**设计层面**均有合理依据：跨行动状态有公开实例；Board 保持事实归属；Planning 不承担完整 delivery ledger；触发可绑定承诺、节点、回执或 review；以语义链跨事件泛化；边界有利于解释 Skills 如何协作。token 节省仅是待验证机制，不能宣称已经抵消成本。

### Option C — Minimal Team

Runner 的 `team` mode 提供了候选入口，因此比较采用最小双角色：Strategist 读取 Board 的规范化公开事实并输出带目标/约束的结构化建议；Executor/Coordinator 读取建议，重新核对 fresh Board，运行候选 Risk gate，并作为唯一 `take_action` authority。Board 事实包是唯一状态来源；Strategist 不得提交动作，Executor 对过期或缺字段建议可拒绝并按现有 Single Agent Planning 恢复。

但 mode 合同没有证明 JiuwenSwarm 实际能隔离工具权限或保证共享上下文。进入任何 Team 实验前，必须验证 action authority 可审计且确实唯一、双方读到同一 session 的新鲜状态、超时/恢复不会重复提交；若不能验证，Team 方案不满足 gate。即使这些机制可实现，Team 也尚未证明能减少策略失误。当前没有证据显示策略与执行属于不可调和的单 Agent 角色冲突；重复推理、跨 Agent 状态同步和响应延迟都是新增风险。根据八项 Team admission gate，目前不足以进入 live Team experiment。

**Team 重新评估触发条件：** 在有完整同期记录、verified model identity 和相同正式 Skills 合同的后续审查中，反复观察到 Single Agent 因战略规划与候选执行的职责冲突而丢失目标/未跟踪兑现；并且可定义单一状态权威、单一提交者及能隔离 Team 变量的最小实验。低分、一次失败或缺模型遥测本身不满足该条件；任何 live 实验仍需单独授权。

## 推荐后的 ownership 与协作合同

| Owner | Purpose / Trigger | Input → Output | State read / write | Action authority / fallback |
|---|---|---|---|---|
| `structured-state-board` | 每次 fresh observe；新公开回执时增量更新 | 当前公开状态 → 事实、时间/来源、新鲜度、少量可归因近期效果 | 读本次公开 observe；只写当前 session 的公开事实；未知标 UNKNOWN | 不提交动作；状态陈旧则要求 fresh observe，不以推断覆盖事实 |
| `rolling-planning`（提案中可改名 `career-trajectory-planning`） | 每次决策 QUICK_SCAN；正式 review、目标变化、兑现结果或可比无进展时 FULL | Board + review feedback + lifecycle 摘要 → global/review objective、一个 Primary Gap、下一 checkpoint、候选行动理由 | 拥有全局/窗口策略和 checkpoint；读取但不重写 Board 与 lifecycle 事实 | 不提交动作；证据冲突时重读公开状态、收窄目标并标不确定 |
| `delivery-progress`（提案） | 仅新公开机会/承诺、里程碑、阻塞、交付回执或相关 review 触发 | 公开事件、行动回执、已有短状态 → 生命周期阶段、owner/dependency、证据状态、与 review 的可见联系 | 仅拥有当前 session 有效的少量 lifecycle 摘要；不复制通用属性和历史 transcript | 不提交动作、不选战略、不裁 Risk；缺少回执时不升级为已交付 |
| `risk-review` | 每个最终候选做 QUICK 风险门；只有 Material Risk 才 FULL | 候选 + 当前公开状态 → allow / warn / reconsider / stop 与简短依据 | 读取 Board 当前事实和候选；只写本次候选的风险判断 | 不提交动作；公开风险不足以支持判断时标未知并选可恢复候选或获取公开信息 |
| Single Agent controller | Risk gate 通过后唯一执行点 | 合法候选及简短决策记录 → 单一公开动作 | 不拥有第二份事实或策略状态 | 唯一 `take_action` authority；返回后 fresh observe 并核对结果，unknown outcome 时按 runtime STOP/核对合同处理，禁止盲目重发 |

冲突顺序：合规与明确重大风险先作为门；通过后 Planning 依据全局目标选择；Delivery 只报告承诺和证据，不拥有策略投票权；Risk 可要求重审/否决其负责的候选，但不制定替代战略。信息不全时不把“未观察到”改写为“未发生”或“已完成”。上下文恢复先 fresh observe，重读当前 Skills/manifest 合同，从公开回执重建；无法重建的生命周期保留 UNKNOWN，不恢复跨局记忆。

## 资源、恢复与解释性

- **QUICK_SCAN：** Board 每次新状态；Planning 仅对当前目标和 horizon fit 做短比较；Risk 检查候选是否触及明确风险；Delivery 只检查当前触发是否更新一项活动生命周期。
- **FULL：** Planning 在正式 review、Primary Gap 变化、交付/阻塞改变结果解释、或已有可比 checkpoint 显示目标无进展时展开比较。Risk 仅在候选触及公开的重大风险时展开。Delivery 仅在出现新的生命周期事件、回执或 review 联系时更新细节。
- **渐进披露：** 日常只传 `Primary Gap + objective + checkpoint` 与最多一条相关 lifecycle 摘要；详细依据仅附触发的公开证据。禁止复制 Board 全量事实或 transcript 到 Skill 输出。
- **恢复：** 每次决策使用 fresh public state。压缩/重连后先重新读取 manifest 与四 Skill 合同，再以会话内公开状态及回执恢复短状态；先前决策的意图不能代替动作回执。Skill 调用或 host 中断不授权任何游戏重试。
- **成本未知：** 现有材料不足以量化新增 Skill 的 token 或 latency；因此只提出“稀疏触发 + 短摘要”的成本控制合同，不报告节省量。Team 的额外成本方向明确，数值未知。
- **云端/专家解释：** 可展示谁读事实、谁设目标、谁跟踪兑现、谁审风险、谁提交，且每条 lifecycle 记录指向公开证据状态；不声称该结构对应隐藏加分项。

## 证据分级与决策

### Strongly Supported

- **FACT：** 高分、低分和中间分轨迹均有差异；S07-21 48m/L5 是正面公开轨迹，但记录完整度部分缺失，model/effort UNKNOWN。
- **FACT：** 活动次数不构成可复用策略公式。v1 #1 与 S06 的 16/16 项目申请对应不同结果；report/network/action 数与完成证据也不等价。
- **FACT：** 当前 Architecture Decision 维持 Single Agent + 三 Skills，并将第五 Skill、Memory 与 Team 设为 deferred；本 Task 不覆盖该治理决定。
- **INFERENCE：** 公开结果链应独立于机会数量和叙述性计划进行证据跟踪；观察到的行为能支持通用生命周期模型。

### Promising Hypotheses

- `H_PROMOTION_COMPOUNDING`：把公开 progression 与后续 Skill/Network/Output/Wealth 的轨迹联系起来，用作中期反馈而非目标阈值。**低置信度；因果未识别。**
- `H_OPPORTUNITY_TO_RECOGNITION`：在相关触发时维护 bounded delivery lifecycle，可能减少把机会、活动、交付、证据和 recognition 混为一谈。**设计机制合理，分数收益未测。**
- 4-Skill 架构可能提升 ownership/readability；token 与泛化收益仍待验证。

### Unsupported / Rejected

- 晋升早期发生导致高分；S07-21 证明某模型/host 有因果提升；现有任何 Skill 已被证明能提高隐藏测试成绩。
- 固定月晋升目标、隐藏阈值、固定 action ratio/Energy bundle、关键项目必胜、按 event/title/option number 映射答案。
- Team 或更多 Skills 天然加分；单局/高分可证明稳定性或隐藏测试泛化。

## 决策与下一步

- 推荐架构：**Option B — 4-Skill Single Agent（design-only proposal）**。
- Team：**`TEAM_DEFERRED`**，仅在上文列出的可审计职责冲突证据和可归因实验方案都出现后重新评估。
- 唯一最高价值下一步：由 Main/Stage review 本提案，决定是否另立实现任务；在正式 Candidate/Skill 变更进入任何 gameplay 前先完成边界审查。

## 任务结果记录

- Candidate / manifest / Skills / Runner / dependencies / `CURRENT_STATE.md` / ADR mutation：`0`。
- Live：service `0`，MCP gameplay `0`，`new_game` `0`，gameplay observe `0`，`take_action` `0`，provider/DeepSeek `0`，AgentServer `0`，Runner gameplay `0`，install/reload `0`。
- Evidence boundary：仅使用 Plan 允许的公开、已提交资料；未使用 hidden/private/forensic strategy evidence。
- Model / reasoning effort：当前执行环境未暴露具体变体与 effort，记为 `UNKNOWN`；未调用并行 Agent、未运行游戏或测试。
