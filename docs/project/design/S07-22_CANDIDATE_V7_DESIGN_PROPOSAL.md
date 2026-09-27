# Candidate v7 设计提案｜S07-22

- **状态：** `PROPOSAL / DESIGN ONLY / NOT IMPLEMENTED`
- **推荐候选：** 4-Skill Single Agent；`TEAM_DEFERRED`
- **证据边界：** 仅公开状态、合法选项、公开 feedback/receipts 与已提交公开轨迹。隐藏评分权重、Dev 事件查表和隐藏 simulator evidence 均不属于设计输入。

当前 Runner Source Lock 静态合同接受 `mode=agent` / `mode=team`，但当前 manifest 是 `agent`。`team` 被接受不证明 AgentServer 提供共享上下文、角色隔离或不可绕过的单一 action submitter；这些都必须在任何独立 Team gate 中验证。

本提案供 Main/Stage 决定是否建立实施任务。它不变更当前 Candidate、manifest、Skills、Runner 或架构决策，也不构成 live authorization。

## Global Objective

> 在合规、生存与有公开依据的重大风险约束下，稳健提升剩余职业生涯的 progression、可见交付、复利资产及终局选择空间。

这是一项鲁棒的长周期目标，不是隐藏 evaluator 下的精确最优解。Level/promotion、Skill、Network、Output、Wealth、future opportunity 和 remaining horizon 作为公开轨迹维度比较，不设置臆造的隐藏分值权重。风险作为约束审查，不替代职业目标。

## Strategy Hierarchy

```text
Hard constraints
    ↓
Global career trajectory across remaining horizon
    ↓
Current review-window objective and one Primary Gap
    ↓
Delivery evidence + compounding value + horizon fit
    ↓
Legal candidate comparison
    ↓
Candidate-specific Risk gate
    ↓
Single Agent submits one action
    ↓
Fresh observe; reconcile effect and evidence
```

### Hard Constraints

拒绝不合法选项；按公开材料识别明确的重大合规、信任、健康和终止风险。不得编造 Health/Wealth cutoff、隐藏 threshold 或未公开的伤害概率。风险 review 是门，不是默认长期目标。

### Global Progression

将公开的 level/promotion feedback 视作长期 progression 反馈，并判断 Skill、Network、Output、Wealth 和可选机会是否沿时间形成复利。晋升较早可能扩展后续机会集，是 `H_PROMOTION_COMPOUNDING`，不是因果定律或固定月份 KPI。一次局部低指标不会自动变成全局目标。

### Review-window Objective

每个公开 formal review 或足以改变轨迹判断的新反馈后：读取 fresh state；总结 progression 反馈；选一个最影响剩余生涯的公开 Primary Gap；写明下一项可观察 checkpoint。新证据出现时允许改变 gap，保留此前结论与不确定性，不为维持计划而忽略反证。

### Delivery / Compounding

Opportunity 只有在公开资料确认 commitment/ownership 后进入待跟踪链；完成需要可观察回执；Recognition/review impact 必须有单独公开证据。依赖、负责人和截止窗口只在公开提及时记录。不按项目申请、报告、人脉或行动次数推断成果。

### Local Action

每个候选用简短比较回答：它怎样服务 Primary Gap 和剩余 horizon？有无可验证的结果或复利价值？风险、资源机会成本、可逆性、依赖负担如何？Risk gate 是否通过？选择须能连回 review objective；无需每步生成长篇推理。

## 最小语义特征

每项特征仅用于结构化比较，不赋予隐藏权重：

1. Material Risk：公开可证的严重后果。
2. Career Progression Relevance：与当前公开 progression feedback 和 Primary Gap 的关系。
3. Ownership / Delivery Value：是否形成有 owner 和可验收结果的承诺。
4. Observable Evidence / Recognition：是否有回执，以及与目标/review 的公开联系。
5. Compounding Asset Value：是否可能累积 Skill、Network、信誉、Output 或后续选择空间。
6. Reversibility：无效时能否恢复或降低长期损害。
7. Resource / Opportunity Cost：时间、Energy、Wealth 及错失其他机会的成本。
8. Dependency / Coordination Burden：交付依赖的协作、批准、信息和前置工作。
9. Remaining Horizon：到下个 review 与职业终点的实际剩余窗口。

未知事件使用公开文字识别意图、约束和可观察结果；无法确认的动机、阈值、依赖或状态留为 UNKNOWN。禁止 event title/关键词规则、固定 choice number、Dev event catalog 和历史答案 lookup。

## Skill Architecture 与统一合同

| Skill | 唯一职责 | Trigger | 输入 → 输出 | State owner / write | 可否提交 action |
|---|---|---|---|---|---|
| `structured-state-board` | 维护当前公开事实与新鲜度 | 每次 fresh observe；有相关公开回执时更新 | observe → 精简事实、来源/新鲜度、未知及有限近期效果 | 当前 session 公共事实；不写 strategy 或 delivery lifecycle | 否 |
| `rolling-planning`（可提议重命名 `career-trajectory-planning`） | 维护 global objective、review-window objective、Primary Gap 与 checkpoint | 每步 QUICK_SCAN；正式 review、目标变化、交付结果/阻塞变化或可比无进展时 FULL | Board + feedback + delivery 摘要 → 目标、gap、checkpoint、候选理由 | 全局/窗口规划；读取但不重写 Board 或 delivery facts | 否 |
| `delivery-progress`（新增提案） | 维护公开机会到可验证结果的 bounded lifecycle | 新机会/承诺、公开里程碑、阻塞、交付回执或相关 review 触发 | 相关公开回执和当前摘要 → 阶段、owner/dependency、证据状态、review 联系 | 当前 session 少量活动 lifecycle；不存通用 Board 事实或 transcript | 否 |
| `risk-review` | 对当前具体候选做风险门 | 每个候选 QUICK_SCAN；仅显著公开风险时 FULL | 候选 + 当前事实 → allow / warn / reconsider / stop 与依据 | 本候选的风险判断；不拥有 global objective | 否 |

### `delivery-progress` 边界

- 只跟踪当前 session 中少量尚未关闭、且对当前目标仍有意义的 lifecycle 项目。
- 用公开证据标示提议/承诺/进行/阻塞/完成回执/公开 recognition；这些标签描述证据状态，不表示隐藏游戏内部阶段。
- 没有 owner、日期、结果或依赖证据时不补写。没有回执不等于失败，也不等于成功；保留 `UNKNOWN / UNVERIFIED`。
- 不选择全局目标、不评价行动优先级、不判 Material Risk、不产生或提交 action、不复制 Board 状态。
- 只有 relevant trigger 才读/写生命周期详情；无活动项或未出现相关更新时不输出长分析。

## Runtime Flow 与权限

1. Controller 获取 fresh public observe。
2. Board 写入当前公开事实、来源和新鲜度；未观察到的值保持未知。
3. Planning 快速对齐剩余 horizon 与当前 Primary Gap；若 formal review、新 feedback、目标改变、可比 checkpoint 无进展或已知交付结果改变判断，则展开一次窗口级复核。
4. 仅当公开事件触及新机会、承诺、里程碑、阻塞、交付回执或 review 影响时，Delivery Skill 更新对应 lifecycle 摘要；Planning 读取摘要，不复制其状态所有权。
5. Controller 比较合法候选与目标、交付/复利、资源、可逆性及依赖关系。
6. Risk Skill 对这个具体候选作门控。合规和明确重大风险先于优化收益；Risk 不能自创替代计划。
7. **Single Agent controller 是唯一 action authority**，只提交一个通过 gate 的候选。
8. 返回后重新 observe，核对公开回执并更新 Board；仅当相关 lifecycle 有新证据时更新 Delivery 状态。

Skill/host 中断后，不把计划意图当执行回执；按 fresh observe、当前 manifest/Skills 合同和公开回执恢复。动作结果未知时遵守 runtime stop/reconciliation 合同，不盲目重发。无法从公开资料恢复的 delivery state 标 UNKNOWN，不用跨局记忆补足。

### 冲突处理

- 合法性与明确重大风险为硬门；Risk 可对具体候选要求 reconsider/stop。
- 通过风险门后，Planning 依据全局目标和 review objective 决策。
- Delivery 输出事实链与证据状态，不是另一个策略投票者。
- Board 事实与 Delivery 生命周期摘要冲突时，回到最新公开 observe/receipt；不能解决则保留 UNKNOWN。
- 候选收益接近且证据不充分时，优先选择更可逆、依赖更少、资源成本更清楚的合法选项；不引入隐含数值公式。
- 单一 controller 负责最后候选和提交；没有两个 Skills/Agents 可独立调用 `take_action`。

## Resource Contract

| Skill | QUICK | FULL trigger | 输出限制 |
|---|---|---|---|
| Board | 每次 fresh observe 规范当前事实 | 状态冲突、缺失或来源变化影响候选时核查 | 只保留必要事实、来源、新鲜度与未知 |
| Planning | 每步核对当前 gap、目标关系和 horizon | formal review、新反馈、目标变更、结果/阻塞改变解释，或可比 checkpoint 指示无进展 | 默认 1 个目标 + 1 个 Primary Gap + 1 个 checkpoint |
| Delivery | 仅看当前触发是否关联活动 lifecycle | 有新承诺、里程碑、阻塞、结果回执或 review 证据时展开 | 每项只传阶段/owner/下一节点/证据状态的短摘要 |
| Risk | 每个候选检查显式合法性与 Material Risk | 候选触及公开的重大风险或影响不可逆时展开 | 只输出本候选的风险理由与 gate 结果 |

渐进披露详细依据：只在触发项出现时附相关公开材料。token、latency 没有测量值；低频触发是成本假设，不应报告为已验证节省。Team 会引入额外上下文/协调往返，数量未知。

## Generalization、Recovery 与 Anti-overfit Contract

- 按语义识别风险、目标、承诺、回执、依赖与资源；对未见事件重新理解公开描述，不依赖名称、关键词映射表或选项编号。
- Promotion/progression 是 review signal，不是固定月目标或隐藏 threshold。
- 不使用固定 Health/Wealth cutoff、精确分数权重、固定季度行动比例、固定 Energy bundle、关键项目必胜规则、跨局记忆或 forensic simulator evidence。
- 不把机会申请、报告、人脉、计划、可行性或一般赞扬直接记为完成交付/recognition。
- Fresh observe 优先于压缩摘要和旧推断；context recovery 重读当前任务合同/manifest/Skills 后重建公开事实。结果、model identity、review 影响缺证据时保留 UNKNOWN。
- 记录“观察到什么、推断什么、仍未知什么”，不以单局高分或某条轨迹宣称因果、稳定 80+ 或 hidden-test 泛化。

## Cloud Evaluation Alignment

- **Skill design quality：** 每个 Skill 有独立 owner、触发、状态写入与 fallback。
- **Multiple Skills collaboration：** Board 提供事实，Planning 提出目标，Delivery 在相关时提供证据链，Risk gate 审具体候选，controller 唯一提交。
- **Long-term planning consistency：** 每个局部候选必须连到 review-window objective 与剩余职业轨迹。
- **Strategy engineering / explainability：** 保留公开证据来源、阶段与未知，activity/result/recognition 分开。
- **Resource efficiency：** QUICK/FULL 与短摘要限制上下文成本；量化节省仍未知。
- **Cloud evaluation：** 这些设计可解释，但精确权重未知，不能声称 Skill 数、协作或 Team 自动获分。

## 进入实现前的审查条件

1. Main/Stage 接受或修改 4-Skill ownership 与 `delivery-progress` 的窄范围触发。
2. 实现任务单独定义 Skill 输出 schema、状态上限和相关 trigger；不得改 Candidate/runtime 合同以规避 AD-005。
3. 用一个与职责合同直接相关的静态/行为检查验证不重复所有权、无动作提交权、缺证据时保留 UNKNOWN；该实现任务确定具体 gate。
4. 任何 live gameplay 或 Team 实验另行授权；本提案不消耗、不隐含 live 次数。

Team 仍为 `TEAM_DEFERRED`。只有同期完整、model identity verified 的重复证据表明失败源于 Single Agent 的角色冲突，并且同步权威、唯一提交者、恢复方案、预期机制和可归因最小实验均明确时，才重新进入 Main/Stage review。
