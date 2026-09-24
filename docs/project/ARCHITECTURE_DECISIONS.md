# ARCHITECTURE_DECISIONS

修订：Bootstrap v0.3 / 2026-09-22。当前能力合同的运行依据为 [OFFICIAL_SOURCE_LOCK](OFFICIAL_SOURCE_LOCK.md)。

## AD-001

当前路线：

Single Agent + Multiple Skills

原因：

-   成本低
-   可验证
-   方便定位收益来源

------------------------------------------------------------------------

## AD-002

Memory:

优先结构化状态。

不默认无限历史。

------------------------------------------------------------------------

## AD-003

Swarm:

作为后续实验路线。

升级条件：

实验显示角色拆分收益超过复杂度成本。

------------------------------------------------------------------------

## AD-004

任何重大架构变化：

必须：

Hypothesis

↓

Experiment

↓

Decision

------------------------------------------------------------------------

## AD-005 — Skill Contract（设计合同与已验证能力边界）

General Memory 仍是**候选设计方向，尚未实现**。`structured-state-board` 与 `rolling-planning` 已实现并进入 Candidate v1 的真实运行；Main 接受 S04 中的 partial State Board runtime evidence 和 Planning checkpoints 作为 Stage evidence，但不证明任一 Skill 的独立 score benefit。Risk Control 已有最小 `risk-review` Skill 实现；Main 接受 S03-14 在一次 qualifying public trigger 上验证的 runtime load、Risk marker 与 action correctness，作为 S03 Stage evidence。该证据限于一次 observed runtime path，不证明 strategy effectiveness、score benefit 或泛化。以下合同界定职责，不要求拆成三个 Skill 文件，也不创建新的调度框架；具体拆分由实现和后续实验决定。

AD-001 中“成本低、可验证”是选择起步路线的理由，不是本项目实测优势。S01 使用官方示例验证闭环，不证明 Memory / Planning 已实现，也不证明 Risk Control 的策略收益。

### Structured State Board

Skill Name: `structured-state-board`（已实现：[`skills/structured-state-board/SKILL.md`](../../skills/structured-state-board/SKILL.md)；S04 Main acceptance 记录其 partial runtime use）

Purpose: 将公开观察与必要事件线索整理为当前局状态，保留时间、来源和不确定性。

Trigger Condition: 新局建立后；获得新的 observe / action 结果后；需要恢复当前决策上下文时。

Input: 当前 session ID、月份/阶段、官方可见状态、当前事件/可选项、行动回执及必要日志。

Output: 带 session/时间标识的状态摘要；分别标记 observed、inferred、unknown，不把隐藏阈值推断写成事实。

State Read: 同 session 的上一摘要和当前官方观察；已随提交包版本化的经验引用。

State Write: 仅更新本局状态摘要及来源引用；规划建议和风险推断不可覆盖观察事实。由单 Agent 顺序调用更新，不允许并发改写同一摘要。

Can Submit Action: No。不调用 `take_action`，不新建另一局。

Failure Fallback: 丢弃不匹配 session 或过期的摘要，重新读取官方观察/必要日志；无法取得可靠状态时返回 Unknown，由单 Agent 暂停依赖该状态的动作，不自行补造字段。

### Planning / Rolling Planning

Skill Name: `rolling-planning`（已实现：[`skills/rolling-planning/SKILL.md`](../../skills/rolling-planning/SKILL.md)；S04 两次 Candidate run 均有 runtime checkpoint evidence）

Purpose: 根据当前状态提出近期行动建议、中期目标及修正理由。

Trigger Condition: 新事件需要选择；季度行动阶段；半年反馈或重要状态变化使原计划失效。

Input: 当前状态摘要、公开手册、当前合法选项、已有局内目标及必要风险提示。

Output: 候选行动、理由、预期取舍及尚未知的影响；不把预测结果写成实际结果。

State Read: 同 session 最新状态摘要与当前计划。

State Write: 本局计划/目标及修订理由；不改写 observed 状态，不写入未经验证的跨局因果经验。

Can Submit Action: No。只向同一个 Agent 返回建议。

Failure Fallback: 退回当前合法选项与短期目标，明确计划不可用或不确定；由 Agent 结合风险提示作当步判断，不凭空生成不可用动作。

### Risk Control / Risk Gate

Skill Name: `risk-review`（已创建：[`skills/risk-review/SKILL.md`](../../skills/risk-review/SKILL.md)；一次 runtime correctness 证据见 [S03-14 RESULT](../../experiments/S03-14-risk-correctness-live-smoke/RESULT.md)）

Purpose: 检查候选行动的合法性、资源约束及公开失败方向，暴露风险与收益的取舍。

Trigger Condition: Agent 准备提交候选行动前，或风险相关观察发生变化时。

Input: 当前官方可选项、最新状态摘要、候选行动、公开风险规则和待确认假设。

Output: 风险建议、依据、不确定项以及存在时的合法替代选项；不能把最保守等同于最优分数。

State Read: 同 session 最新观察、规划建议、公开规则及标注为假设的经验。

State Write: 本局决策记录中的风险意见；不修改环境状态、不把推测的失败阈值保存为事实。

Can Submit Action: No。Skill 只提供风险建议，不调用 `take_action`；S03-14 单次运行中唯一 successful action submitter 是 Single Agent（35 次成功提交，`risk-review` 提交数为 0）。这是该次 runtime path 的 correctness 证据，不是普遍强制执行或策略收益证明。

Failure Fallback: 状态过期或选项不明时请求重新观察；分析不可得时明确返回 Unknown。仅在合法且依据充分时建议保守替代，不为凑出动作虚构规则。

### 单 Agent 的执行与状态边界

- 单 Agent 是本局唯一动作提交者，负责按当前官方阶段顺序提交 `take_action`；上述候选能力提供摘要或建议，不独立推进月份/阶段。未来即使拆成多个 Skills，也不增加竞争的动作写入者。
- 每次行动使用当前 session 和新鲜观察；动作回执确认后再更新状态。超时或网络错误导致“是否执行”不明时，先 observe / 查必要日志，禁止无条件重发；无法消除歧义时停止并保留证据。
- 新局从干净的局内状态开始。官方安装提交包会重置技能并清理部分会话/记忆（Source Lock 第 3 节）；不得依赖本地运行后生成的记忆跨局或进入云端评测。
- 开发期经验只有经过评估、标识来源与版本、明确归入提交包后才作为可交付知识。因果未定的失败保留“未定”，不自动归因为计划/执行/随机中的某一类。
- 规划、风险提示和状态整理的顺序可由同一个 Agent 按需组合。只在取得实验依据后决定是否拆分、更换存储或引入角色协同；不为当前设计合同创建复杂持久化或并行系统。

验收边界：S03-14 的 Risk 证据仅覆盖一次 qualifying public trigger 的 runtime load / marker / action correctness；不证明策略表现、score benefit 或泛化。S04 Main acceptance 为 `PASS_WITH_KNOWN_LIMITATION`：State Board runtime 为 `PARTIAL_BUT_SUFFICIENT_FOR_STAGE`，其 score benefit `NOT_PROVEN`；Rolling Planning 已实现并进入两次 Candidate run，独立 score benefit 同样 `NOT_PROVEN`。Single Agent 仍是唯一 action submitter。Team / Swarm 保持 `DEFERRED`，沿用 AD-003 的证据准入和 AD-004 的 Hypothesis → Experiment → Decision 流程。

## S04 Main acceptance｜Game Gate 与 Candidate v2 假设

- Main 接受 S04 为 `COMPLETE`，Stage acceptance 为 `PASS_WITH_KNOWN_LIMITATION`。Candidate v1 两次成绩为 `76.04 / 53.23 / 48m / A` 与 `35.31 / 24.72 / 25m / D`，故记录 `CANDIDATE_V1 = HIGH_VARIANCE`；不据此声称稳定高分、因果收益或 hidden-test generalization。
- `GAME_GATE = ADOPTED`：full game 是昂贵 benchmark，不是普通 correctness test；新一局必须有单独明确授权。S04 验收当时 `NEXT_GAME = NOT_AUTHORIZED`；最新延期状态见 `CURRENT_STATE.md`。
- 下一研究假设为 `H_MATERIAL_OUTCOME_REPRIORITIZATION`：Candidate 部分早期成长信号已观察到，但中期成长及严重公开后果下的动作排序不稳定；下一候选先离线审查一个有公开轨迹支持的决策机制，同时保护正常成长机会。Astra-01 提供 red-team / hypothesis 线索，不自动成为工程事实。
- Candidate v2 的首个最小候选仅为假设：只改 `rolling-planning`，加入 bounded `material-outcome checkpoint`，在 severe public consequence 后重新比较当前目标与合法替代路径。不得默认“道德/原则上正当”或“刚晋升/担当”即安全，也不得默认转岗/降低暴露即失败或必然降职。此处没有实施或验证该改动。
- 本假设不同时修改 `risk-review` 或 State Board，不加入 `active_public_risks`，不绑定 Energy component-wise comparison，不新增第五个 Skill，也不启动 Team / Swarm。Energy comparison 保留为独立 Hypothesis。

## S05 implementation boundary

- 上节是 S04 Main 验收时的候选语境。S05-01 后已由 Main 接受并合入：仅 `rolling-planning` 离线实现 bounded material-outcome Priority 重排；未运行 v2-C gameplay，策略收益仍 `NOT_PROVEN`。
- S05-02 的 integrated offline Planning 增量已通过 Main/Stage 离线 review，但父分支尚未合入 main；S05-03 最终 reserve audit 与恢复提示仍属待审子分支证据，不是 gameplay 收益事实。Single Agent 唯一动作提交者、Board / Planning / Risk / Trace 职责和独立 Main Game Gate 均不变；不建立新 Skill、持久状态或 Team / Swarm。
