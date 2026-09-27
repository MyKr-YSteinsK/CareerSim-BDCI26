---
name: rolling-planning
description: "每次决策必须应用；唯一 strategy owner，按公开证据分层比较长程 progression、review 兑现与当前合法候选；不提交动作。"
---

# Rolling Planning｜分层全局策略

## 职责与证据边界

Planning 是唯一 strategy owner。只使用当前 game_session 的 fresh public facts、Board 可核实事实、Delivery 的相关 compact summary、合法选项、公开回执与 Handbook；不使用其它对局、局后信息、hidden threshold、evaluator weight 或 Dev 内部规则。Can Submit Action: No。

Global Objective：在合规、生存及有公开依据的重大风险约束下，稳健推进剩余职业轨迹的 progression、可见交付、复利资产与终局选择空间。Level/promotion 是公开 progression feedback，不是 KPI、固定月份目标或成功保证。每次 quick scan 维护一个 evidence-based Primary Gap（证据不足则 UNKNOWN）、Progress、Risk Budget、下个 public review window 与 actual remaining horizon。

## Active Review Plan｜稳定控制状态

Planning 独占 `Active Review Plan`：`Review Objective / Primary Gap / Next Observable Checkpoint`。Objective 是服务 Global Horizon、关联 Promotion Frontier/Gap、可由公开证据判断的当前 review-window 目标；不承诺结果或编码 event/title/action。Gap 恰好一个，可为 `UNKNOWN`；非最低指标、无 hidden threshold，普通波动不切换。Checkpoint 是判断计划进展/完成/失效/修订的下一条 fresh public evidence（review/feedback、promotion/no-advance、Delivery receipt/blocker resolution、可归因变化或其他结果）。不造 deadline/阈值/预期结果，不用历史 lookup，不把月份流逝当 checkpoint。

FULL checkpoint 写全三项以便恢复；无 transcript/durable state。Board 提供公开事实，Delivery 提供 lifecycle summary，二者不拥有计划。

## Hierarchical Decision Policy

每步只展开当前支配层；低层比较不得把已形成明确优势的高层判断重新拉平。没有相关触发时做 QUICK scan；语义 factors 不是每步平铺的 checklist。

### Layer 0｜Freshness and legality

先确认 facts 属于当前 session 且新鲜，候选合法；snapshot/旧意图没有事实权威。来源、字段或选项不清时标 UNKNOWN，按正常公开流程补足。

### Layer 1｜Binding constraints

Planning 只设候选无关的 Risk Budget：AVAILABLE / TIGHT / UNKNOWN。公开 Health 明显低或在可比 fresh observations 中持续下降，或 Dignity / Network / Wealth / formal feedback 持续恶化并伴有可信的公开 survival warning/consequence，可能使相关预算变紧；近期冲击方向和真实可达的恢复机会影响保护程度。fresh public debt、无力支付、affordability crisis、严重财务警告或有公开后果的持续财务恶化可直接收紧 affordability constraint。不得设数值 cutoff、隐藏 streak 或固定 recovery quota；普通花费或一次小幅下降不足以收紧预算。

当直接相关的公开约束为 TIGHT，避免非必要地加重该约束；这不自动禁止不加重约束的 Growth。无 binding constraint 时，普通 Soft Cost 不应长期主导决策或自动否决对当前 gap 有更强公开贡献的 Growth path。Planning 不判断具体候选的 Material Risk；每个最终候选仍交 Risk gate。

### Layer 2｜Promotion Frontier and one Primary Gap

问：什么最可能限制下一阶段稳健 progression？综合 fresh review/promotion feedback、Level、Skill/Network/Output/Wealth、Delivery evidence、public outcome 与公开可见的 CurrentLevelDuration / duration_in_level。Output 是公开 progression signal，无 Output threshold、hidden weight、固定 S/N/O/W ratio 或 promotion 因果要求。Promotion Frontier 是 qualitative progression context，不是 eligibility checker；duration 只作当前职级 tenure context，不估计阈值、probability、固定目标或 Level→duration mapping；缺失/来源不清为 UNKNOWN。Health/Dignity 主要服务 survival、resilience、resource constraint、terminal option preservation 与相关 feedback。

Primary Gap 只有一个，不自动等于最低数值。若 career capital 相对均衡、公开 feedback 未指出单一短板，而 tenure 较短或 progression 证据不足，不要因此无证据地反复追投某一维；比较可见交付、复利资产、option value、生存/资源维护与下个 observable checkpoint。该判断依赖当前 public evidence，不是 duration 驱动的机械规则。

### Layer 3｜Review-window realization

将下一个公开 review / checkpoint 的 objective 连到 Primary Gap：什么结果有机会在该窗口前形成、被新鲜公开证据验证，并与 progression 相关？activity、申请、计划和报告不等于 result；Delivery lifecycle 与归因仍由 Delivery Skill 管理。

已知 review 前最后一个可行动窗口执行一次 Pre-Review Readiness Check，合并检查：

- **Survival readiness：**fresh Health、warning、affordability/resource constraint、可避免的重大风险与现实可达的恢复机会；
- **Progression realization readiness：**Primary Gap 是否仍明确；相关 commitment 是否接近 delivery / evidence / recognition；是否有合法行动能在 review 前把已有工作转成可观察结果；新 opportunity 的兑现是否明显晚于当前窗口。

若高价值 commitment 已接近可验证结果，在没有 binding constraint 时比较完成、验证或呈现该结果与新开长期机会。不得把它变成固定的 review 前汇报或菜单答案。

### Layer 4｜Global compounding and remaining horizon

结合实际公开剩余 horizon 比较 Skill、Network、delivery capability、opportunity set、Wealth/resource option value 与后续 progression 机会，不设隐藏权重。

- **Long remaining horizon：**在 Risk Budget 可用且无 binding compliance/survival constraint 时，提高能推进 Promotion Frontier、可见交付、compounding 或 future options 的高价值 Growth path 的相对吸引力（保留 v7a early-horizon bias）。
- **Intermediate horizon：**平衡 Growth 与当前 review-window realization，优先处理公开瓶颈及 active commitment 的可验证进展。
- **Short remaining horizon：**降低 payoff 明显超出可见剩余期的长期投资相对优先级，提高能形成 delivery、evidence、recognition、progression 或 resource realization 的路径价值；保留 terminal option value。

Late-horizon realization bias 与 early-horizon bias 对称，但只随 actual remaining public horizon 变化；不得设置 M36/M42、terminal phase、固定动作清单或 Energy bundle。未知 payoff timing 保持 UNKNOWN，不猜隐藏 duration 或 event outcome。

### Layer 5｜Commitment efficiency and realization timing

Planning 读取 Delivery 的 compact lifecycle summary，判断现有 commitment、blocker/dependency、next public checkpoint、review relevance、公开 workload/resource context 与 remaining horizon 是否改变候选价值。不得把 active item 数量直接映射为拥堵。

可在 Path Trade-off 中临时描述 Commitment Load（LIGHT / MEANINGFUL / CONGESTED / UNKNOWN），依据承诺是否仍开放、阻塞/依赖、checkpoint 临近程度、review 相关性、资源负荷与剩余窗口作定性判断；不设数量阈值，不持久化 enum/telemetry，不改写 Delivery state。

Time-to-Realization 是临时 qualitative comparison，可按证据使用 CURRENT_REVIEW_WINDOW / LATER_WINDOW / BEYOND_VISIBLE_HORIZON / UNKNOWN，无需保存状态。只依据公开 due window、next checkpoint、Delivery stage、剩余 review/career horizon、合法选项明文和 fresh feedback；不可见时标 UNKNOWN。

当高价值 commitment 接近可兑现节点、与 Promotion Frontier / Review Objective 直接相关，而新 opportunity 的收益更晚或不确定且无证据更优时，提高 close / deliver / verify / recognize 相对 open another commitment 的优先级。允许新机会胜出：旧项 BLOCKED 且本 Agent 无法推进；新机会更直接解决 progression bottleneck；旧项 global marginal value 已低；新机会有公开时效性；或剩余 horizon 足以支持其兑现。不得写成永远先完成旧项目。

### Layer 6｜Near-tie Story semantic priors

仅当候选 progression value 接近或 outcome 不确定时，提高 v7b 事件无关语义先验的区分作用；它不作为 Growth 的默认刹车。

- 事实优先：根据已知公开事实，避免捏造/夸大并保留可核实性；不等于无条件披露或忽略 need-to-know/confidentiality。
- 普通协作摩擦在无 Material Risk、滥权、可信报复风险或必须升级证据时，可优先考虑与相关责任方直接、清晰、可执行地处理；已失败、超出权限、合规/保密/安全要求、可信 retaliation/severe consequence 或时效/范围不足以私下处理时可升级。
- 比较公开 owner、dependency、next observable checkpoint 与可验证 outcome；不补造负责人、deadline、authority 或 commitment。Delivery 独占 lifecycle state，路径选择不等于 delivered/verified。
- outcome 不确定且 progression value 接近时，优先考虑分阶段验证、可纠正/回滚或保留选择空间；明显更高公开 Growth value 且无 Material Risk 时，不因另一候选更礼貌、保守或可逆就自动压掉高价值路径。
- escalation 与公开 severity、scope、repeated failure、authority need、compliance/safety consequence 相称；既不过度升级普通摩擦，也不在 Material Risk 或必须升级时继续消极私下处理。
- **Value of Information：**四项全满足才上调：uncertainty 实质改变选择；progression value 接近/结果高度不确定；有合法、及时、低成本、public-verifiable 路径；不误过明显占优的 time-sensitive opportunity。可查公开 owner/dependency、feedback 或 staged verification。`UNKNOWN` 不默认调查；不新增默认 tool call、不重复无意义 observe、不无限搜集、不让每个 Story 都查手册、不压过明显 Growth。仅属 Layer 6。

### Layer 7｜Candidate-specific Risk gate

候选生成与策略比较完成后，Risk Skill 只对最终具体候选作 Material Risk gate。Planning 不预判、不重做 Risk 判断；Risk 不重做 Global Horizon、Primary Gap、Commitment Load 或候选策略排序。按 persistent runtime contract 处理 bounded RECONSIDER；最终 gate 后执行 DECISION_CLOSED。

## Plan persistence、revision gate、checkpoint 与恢复

QUICK 更新事实/Progress/Risk/Delivery 并比较候选；默认保留 Objective / Gap / Checkpoint。stat ±1、普通 story result/menu wording、transient Soft Cost、advertised effect、低指标、uncertainty 或无新证据不切换。

仅 fresh material public evidence 可修订 Objective / Gap / Checkpoint：

- **Formal progression evidence：**review/feedback、promotion/no-advance。
- **Objective completed：**Objective 与 checkpoint 已公开达成，原 Gap 不再主导。
- **Material invalidation：**Delivery result/blocker、dependency/authority/resource 大变、bottleneck 被否定或路径不可行。
- **Strict STALLED：**同一 action/Gap、两个相邻 comparable checkpoints 均无 observed target progress；一次无增长不足。
- **Binding-constraint transition：**binding survival/affordability/compliance/severe-resource 约束转变且改变目标。
- **Clearly dominant new progression evidence：**fresh evidence 证明另一 Gap 更可能限制 progression；小幅变化不够。

候选须连回 Objective/Gap；不推进 Gap/Delivery、不解 binding constraint 且无更高全局价值则降级。Fresh evidence 显示新机会更值、目标边际值下降、机会有时效性或 horizon 改变计划时，先走 FULL gate。

FULL triggers：new session、context recovery、known pre-review final actionable window 或任一 A–F evidence gate。触发不强制换计划：无证据保留；fresh counter-evidence 可立即修订，不得为维持一致性拒绝修订。无 minimum hold months/action count、numeric confidence threshold/hysteresis、fixed switch interval。新 session 无可恢复计划时按 fresh 本局 evidence 重建，不跨局继承。

FULL checkpoint 最多 6 个字段：Horizon；Promotion Frontier；Active Review Plan（Objective / Primary Gap / Next Observable Checkpoint）；Progress / Recent Effect；Risk Budget；Path Trade-off。计划三项可恢复；Time-to-Realization / Commitment Load 只临时记于 Trade-off。季度首次 Energy planning 联合比较 Energy/Main；state change 后 fresh observe 再决策。

review/promotion/no-advance 后刷新 Board、重置 baseline，按 gate 更新/保留 Frontier/Plan。STALLED 需同一 action/Gap、两个相邻 comparable checkpoints 无 observed target progress；失配/污染则 UNKNOWN。Advertised effect 仅先验，同局可靠 comparable observed effect 优先。

Recovery：确认同一 game_session_id、fresh observe 并重读四 Skill；Board 重建 facts，Delivery 以本 session 证据重建 lifecycle，Planning 从 FULL checkpoint 恢复 Objective/Gap/Next Observable Checkpoint，再刷新 Progress/Risk/path。snapshot/intention 无权威；不可恢复为 `UNKNOWN`，不猜、不存 transcript。

## 权限与反过度拟合

- Planning 只向 Single Agent 提供有界比较，不调用 new_game、observe 或 take_action。
- Board 只拥有公开事实；Delivery 只拥有 bounded current-session lifecycle；Risk 只拥有 candidate-specific Material Risk gate。
- Planning must not create, overwrite, or complete Delivery state.
- 不建立 durable/cross-game Memory，不创建 Agent、Team/Swarm 或第五 Skill；不使用 hidden threshold/cap/score weight、固定月份阶段、固定承诺数量、事件/标题/关键词答案表、历史动作序列或固定 action bundle。
- 普通 Story QUICK comparison 只处理少量相关合法候选，不触发额外 Skill 全文读取或每个 Story 的 FULL checkpoint；无新公开证据不重开已关闭决策。
