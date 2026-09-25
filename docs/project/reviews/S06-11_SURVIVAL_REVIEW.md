# S06-11｜历史全局生存机制与暴毙路径深挖

## Review status and boundary

- Status: `COMPLETE`（离线历史证据复核；供 Main review）
- Base: `main@08270978f6c5f3a4a0eaadf90840d01056472a8a`
- Current candidate remains `candidate-v5-evidence-driven-phase-policy`；本报告不修改 candidate、Skills、instruction 或 `CURRENT_STATE.md`。
- `NEXT_GAME=NOT_AUTHORIZED`；本任务 provider / service / MCP / install / game 均为 `0`。
- Evidence labels: `DEV_CONFIRMED` = 冻结公开 Dev 实现事实；`RUN_OBSERVED` = 单局记录直接显示；`MULTIRUN_OBSERVED` = 多个记录中重复出现；`HYPOTHESIS` = 有依据但因果未识别；`UNKNOWN` = 证据不足；`DO_NOT_ENCODE` = 不进入运行时策略。

## Evidence Coverage

| Evidence | Identity / use | Limit |
|---|---|---|
| S01-03 | `031d97e56e0ce305a487b4bc293c7abde58cfdf0` 的 `RESULT.md` / `score_report.json`；baseline run `5b37e7fb40844809abf00f9ceeb5c25b` | 19 个月有效淘汰；没有提交月度轨迹，终止通道与 Health/Dignity 拆分未知 |
| SCORE-01 | `7a055dea76580117ca74cddb49bb04efcf605eb1:experiments/S04-03-score-directed-integrated-run/score01_trajectory.json`；比较记录在 `66ec4af1e9a2a28da57c6cb8d409a6a38f87ae01` | 候选身份、运行日期未知；紧凑轨迹覆盖到 M23，score report 未给精确 termination reason |
| Candidate v1 #1/#2 | 两份 identity-bearing compact trajectories、comparison、RESULT：`66ec4af1e9a2a28da57c6cb8d409a6a38f87ae01` | 本机两局原始 events/transcript 均不存在；按 committed artifact SHA 清单检查后未读取任何 raw |
| S06 Run #1 | Main-reviewed compact facts；S06-01/S06-02 历史记录位于 `c4dbe0ebc4e27aafc22c94050c69547113cdc8eb` | 本机原始 transcript/events 不可用；身份、Health、Dignity、详细 promotion 月份未知 |
| Candidate v4 #1 | [RUN_HISTORY](../RUN_HISTORY.md) 与 [S06-08 Health forensic](../runs/v4-run1-health-forensic.md)；run `20260924T160806Z` / game session `fdcaa70a85f44662a6a329513c175676` | 本任务复用已提交的 hash-bound forensic；未重新打开本机 raw |
| Frozen simulator / Dev | Root `.venv` metadata: `career-emulator==1.0.1`, `career-emulator-bdci26==1.0.0`；代码 `failure_conditions.py`, `game.py`, `promotion_conditions.py`, `talk_mechanism.py`；既有 [STRATEGY_EVIDENCE](../STRATEGY_EVIDENCE.md) 记录公开 Dev 文件 identity / 解码摘要 | 只用于解释本地冻结公开 Dev，不表示 Agent 能看见隐藏计数、内部状态或 Dev 选择后的 effect |

源码核对重点：`FailureConditionEvaluator.update_derived_stats/evaluate`；`GameEngine.take_action/_on_month_advanced/_start_quarter_fixed_events/_take_energy_action/_take_main_action/_normalize_time`；半年 talk 与 promotion applicator。月度状态/连续计数、talk、salary、promotion、季度选择的相对次序由此确认。M48 后 trajectory 中的 M49 terminal row 是 `_normalize_time` 对“48 个月完成”的结束哨兵，不是额外淘汰；S04-03 RESULT 的 48 个月完成记录保持有效。

Raw-integrity boundary：本机 S04-03 / S04-04 两局原始 events/transcript 路径均不可用；没有原件就不做哈希匹配后的 raw 分析。S01 仅用已提交 RESULT / score report；S06 Run #1 仅用 Main-reviewed compact evidence。缺失原件不被补造。

## Survival Findings

### 1. 生存是多通道约束，不是 Health 单指标

`DEV_CONFIRMED`：冻结 Dev 存在 Health 即时终止，以及 Dignity、Network、Wealth、HiddenRisk、半年 performance、Skill 等多条失败路径。部分路径会额外损伤其它公开维度，例如 Health、Dignity、Network、Output、Wealth，形成跨通道放大；内部连续计数、失败余量和 HiddenRisk 不属于 Agent 可见状态。完整机制边界见 [STRATEGY_EVIDENCE §2–3](../STRATEGY_EVIDENCE.md)。

`RUN_OBSERVED`：现有终止样本呈现不同通道：v4 #1 为 Health 累积耗尽；Candidate v1 #2 记录为第二次 trust-crisis blowup，终局 Health=10；SCORE-01 的 transcript terminal text 为“炒鱿鱼”，但结构化 termination reason 为空；S01 通道未知。不能把不同通道归因到一个统一策略错误。

| 失败/放大通道 | 冻结实现关系（非运行时指令） | 本组运行证据 |
|---|---|---|
| Health | 公开 Health 归零会即时终止；其它通道或行动也可能损伤 Health | v4 #1 确认 terminal；v1 #2 terminal Health 仍为 10；其它局不够拆分 |
| Trust / hidden risk | trust/compliance 相关内部机制可产生多维损伤及 Output 回退；具体库存/剩余余量隐藏 | v1 #2 terminal 原因记录为第二次 trust crisis；精确 cue、选择和各次爆发月 UNKNOWN |
| Dignity | 持续低位可进入危机链，并可能再损 Health / Network | 没有提交轨迹证明 Dignity 是任何一局的独立终止原因 |
| Network | 持续孤立可带来 Output / Health / Dignity 连锁损伤 | SCORE-01 曾有公开 Network=0 的窗口，未证明达到隐藏连续条件或导致 M24 termination |
| Wealth | 长期 deficit 可连带 Dignity；公开余额不能揭示内部计数 | 没有记录证实 Wealth deficit terminal；v1 #2 在终局时余额骤降，但独立归因不足 |
| Performance | 半年 review 影响 performance / promotion；不佳连续路径会损伤 Network / Dignity | SCORE-01 有 transcript 摘要中的 C、D feedback 和“炒鱿鱼”终局文字，但完整评分序列及因果链 UNKNOWN |
| Skill | 长期失效路径可连带 Dignity / Output | 没有足够终局证据将其识别为当前运行的生存瓶颈 |

### 2. Run timelines（终局字段之外的缺失保持 UNKNOWN）

- **S01-03 baseline** — game `5b37e7fb40844809abf00f9ceeb5c25b`；19 个月，26.95 / 18.86 / E，valid elimination。终局 Level 3、Wealth 2.8、Resilience 合计 16、Skill 26、Network 12；Health 与 Dignity 分项、事件路径、终止原因 UNKNOWN。它是 no-op harness，不是策略对照。
- **SCORE-01** — game `8ffa91ac75e143cfb68b015feb4f40e4`；24 个月，33.06 / 23.14 / D；候选与日期 UNKNOWN。紧凑轨迹中 Health 在 M1/M2 可见至 3，M17 曾见 Network=0；M18 的季度状态 Health=4，并选两次健康恢复；轨迹到 M23，score report 终局 Level 2、Wealth 11.4、Resilience 合计 17、Network 2。Transcript 摘要称终局为“炒鱿鱼”，精确 failure rule、终局 Health/Dignity、review 序列 UNKNOWN。
- **Candidate v1 #1** — game `2224f5df228544e699b10f897d333d4b`；48 个月完成，76.04 / 53.23 / A。轨迹月度 Health 最低 4；M5 末 Health=4，M6 季度 Energy 前为 3，之后用了两次 Health recovery，M6 观察为 7。升职月份 M6/M12/M18/M36/M48；记录全程 Health recovery 11 次、主行动 16/16 为申请关键项目。Health buffer 与存活同时出现，不证明恢复动作的因果收益。
- **Candidate v1 #2** — game `7df157117cf14917bdc42d83fb7ac7d2`；25 个月、35.31 / 24.72 / D。稀疏 milestones 中 Health 从 M1 的 4 到 M6 的 10、M12 的 9、M24/M25 的 10；在 Health 充足时因记录的第二次 trust-crisis blowup 终止。M24→M25 的终局记录同时显示 Wealth 9→3、Dignity 10→8；各字段变化不能仅据压缩轨迹拆为独立直接因果。Promotion M6/M12/M24；M12 有一次低调避险。原始 trust cue / choice / 第一次与第二次 crisis 的逐月过程 UNKNOWN。
- **S06 Run #1** — 48 个月 / 53.83 / 37.68 / C；candidate、session、promotion 时间及 Health/Dignity 时间序列 UNKNOWN。公开终局部分状态为 L4、Wealth 21.8、Skill 89、Network 36、Risk Control raw 5；该 score component 不能替代 HiddenRisk / failure counter。记录 16/16 季度主行动为申请关键项目及后期重复无进展描述，但 raw 缺失限制复析。
- **Candidate v4 #1** — game `fdcaa70a85f44662a6a329513c175676`；6 个月、25.84 / 18.09 / E，Health terminal。可核实状态序列 `5→3→2→4→3→4→3→2→1→0`；M3 Q1 Energy 前 Health=2，选了一次健康恢复至 4；随后逐步下降。M5 末约为 3，进入 M6 后 story / review 窗口内下降至 2、1、0，在 Q2 Energy 前结束。Agent 在最后增长选择前已明确提到 H1 是 Material Risk，仍选增长；造成最后 `−1` 的单项来源 UNKNOWN。23/23 `take_action` 成功，属于有效 gameplay terminal outcome，不是 provider/runtime failure。

### 3. Channel status matrix

这里的 `NO_SIGNAL` 只表示可用记录没有该通道的明确预警，不等于证明隐藏计数为零。Health/状态的“低位”描述不代表政策阈值。

| Run | Health | Trust/Risk | Dignity | Network | Wealth | Performance | Outcome |
|---|---|---|---|---|---|---|---|
| S01 baseline | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | TERMINAL（M19，通道未知） |
| SCORE-01 | EARLY_WARNING（曾见 H3） | UNKNOWN | EARLY_WARNING（稀疏窗口曾见 D5） | EARLY_WARNING（M17 曾见 N0） | NO_SIGNAL（未记录 deficit） | EARLY_WARNING（非结构化 C/D feedback；规则因果未知） | TERMINAL（M24；精确失败规则未知） |
| v1 #1 | EARLY_WARNING（下行至观察最低 4，后恢复） | UNKNOWN（无可见 risk counter） | NO_SIGNAL | NO_SIGNAL | NO_SIGNAL | NO_SIGNAL（有多次 promotion；分数细节不全） | NO_SIGNAL（完成 48 月） |
| v1 #2 | NO_SIGNAL（终局 Health=10） | TERMINAL（第二次 trust crisis） | UNKNOWN（终局有变化但不可分因） | NO_SIGNAL | EARLY_WARNING（终局余额明显下落，独立通道因果未知） | UNKNOWN | TERMINAL（M25） |
| S06 Run #1 | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN（仅终局值可用） | UNKNOWN（仅终局值可用） | UNKNOWN | NO_SIGNAL（到达 M48） |
| v4 #1 | TERMINAL（M6 到 0） | EARLY_WARNING（M3 合规线索被拒；无已知 risk terminal） | NO_SIGNAL（终局公开 Dignity=9） | NO_SIGNAL | NO_SIGNAL（终局仍为正） | UNKNOWN（M6 promotion 不能替代完整 review evidence） | TERMINAL（Health 路径） |

### 4. Health shock / recovery evidence

v4 #1 的既有 forensic 记录给出可归因等级；仅以它作 observed-transition 计数：7 次相邻观测下降中，`−2` 1 次（KTV 后 `5→3`，forensic 标为 strongly attributable）；`−1` 6 次，其中 1 次被标为强上下文归因（生病同事事件期间 `4→3`，但无独立数值机制），另 5 次归因 ambiguous。恢复变化有一处直接对齐公开 Health recovery `+2`，另有一处 `+1` 但选项未列 Health 更新、归因 ambiguous。样本只有一局；这不是 simulator-wide shock 分布，也不能把最大观察降幅当作伤害上限。

跨局只能作有限对照：v1 #1 的观察 Health 最低 4 且活到 48 月；v1 #2 Health=10 时仍发生 trust terminal；v4 #1 是多次下降、曾回补、随后耗尽。`MULTIRUN_OBSERVED` 支持“Health 与非 Health 风险都要看”，不支持“多做健康恢复必然存活”或固定 Health cutoff。

### 5. Quarter / half-year review exposure

`DEV_CONFIRMED`：通常每月最多三次 story action；到季度末后才进入 Energy，再进入 Main action。进入 M6/M12 等半年节点时，月度派生状态、talk、salary、promotion 先结算；M6 的 story actions 随后发生，季末 Energy/Main 更晚。因此至少分开审视：

1. **Pre-quarter**：季度末 story 已可能消耗 buffer；不能把后到的 Energy recovery 当作此前事件的保护。
2. **Pre-review / pre-M6**：M5 结束、跨入 M6 前应复看公开状态与趋势；M6 review 和最多三次 story action 可能先于 Q2 Energy。Health 已到 terminal 后不存在季度补救窗口。

| Exposure | 存活 / eliminated evidence | What it supports |
|---|---|---|
| M2→M3 / Q1 | v4 #1 在 M3 Q1 Energy 前见 H2，选一次恢复；v1 #1 的 M3 季度状态 H4；SCORE-01 在季度状态 H6 前的 M2 末记录 H3，期间变化无法归因 | 需要按当时 fresh state 决策；不支持固定 M3 恢复配额 |
| M5→M6 / Q2 | v1 #1 M5 Health=4、M6 Energy 前=3，随后两次恢复；v4 #1 M5 末约 H3，M6 story 窗口依次降至 H2/H1/H0，未到 Q2 Energy；SCORE-01 M5 末 H7、M6 观察 H6，后到 Q2 存活 | 这是最直接的 timing 证据：M6 Energy 可救 v1 #1 的后续余量，但无法追溯保护 v4 的 M6 story；在“到季度再恢复”前增加 pre-review check 有合理价值，收益仍未实测 |
| Later review / compounding | v1 #1 M18 季度前 Health=10；SCORE-01 M18 的状态/对话窗口有 H3、D5，季度记录 H4 后恢复；v1 #2 M24 Health=10 仍在 M25 信任危机终止 | 安全窗口会随事件路径变化；不能只看半年周期或只看 Health |

结论：`HYPOTHESIS`—将风险复核前移到已知季度/半年边界之前，可能避免把“稍后能恢复”误当作“当前安全”。只采用 fresh public state / trend / material warning / recovery timing；不冻结 M2/M5 等固定月份动作规则，不预测 review 结果。

### 6. Trust / Risk and secondary survival channels

- v1 #2 的 trust-crisis terminal 是唯一明确的非-Health终止链。S04-04 compact evidence 没有保留足以定位每次危机前公开提示、Agent 选择、间隔和逐项损失的细节；对应 raw 哈希路径当前缺失。因此只可记录终局类别，不可重构“哪句话/哪次选择导致第二次爆发”。
- v4 #1 的 M3 离职资料事件包含保密/合规风险 cue，Agent 明确拒绝接收资料；它证明一次 cue 被识别并处理，不证明隐藏风险清零或未来无风险。S06-08 还记载 M5 生病同事事件有传染线索，但是否达到 Risk Skill 的严重后果级别无法从单局判定；按潜在漏审而非已证 false negative 处理。
- SCORE-01 M24 的“炒鱿鱼”是终局文字，不足以确认连续 bad-performance failure；M6/M18 的 C/D 是 Agent transcript 摘要而非 score report 结构化评分。把 performance failure 作为 Dev-confirmed 机制与将该局归类为 performance terminal 必须分开。
- Dignity / Network / Wealth 的确切 streak 和后续惩罚对 Agent 不可见。SCORE-01 曾公开低 Network，v1 #2 终局 Dignity/Wealth 下落，均不足以倒推出隐藏连续计数。v1 #1 的高 Health 恢复与存活并存，v1 #2 的 Health 充足但 trust terminal，展示多路径，不构成修复动作因果对照。

### 7. Recovery opportunity inventory

以下固定行动的菜单效果/成本来自冻结 Dev；故事选项内部 `status_updates` 在选择前不对 Agent 展示。Story-template 数是现有公开 Dev 的启发式语义覆盖，不是抽样概率、可用频率或选择前收益提示。

| Surface | Availability / observed selections | Energy or opportunity cost; visible effect | Timing / cannot repair |
|---|---|---|---|
| Health recovery | 固定季度 Energy 菜单；每个存活季度可重新分配。记录选择数：SCORE-01 前 7 季 3；v1 #1 全程 11；v1 #2 全程 8；v4 Q1 选 1；S06 Run #1 UNKNOWN | 1 Energy；公开 +2 Health | 只在 Energy 阶段起效；无法覆盖前面的季度末 story，也无法救已 terminal 的局；不修 Trust/Dignity/Network/Performance |
| Mental repair | 固定 Energy 菜单；历史摘要未给稳定选择计数 | 1 Energy；公开 +2 Dignity | 不等于 Health 或 Network 修复；接近状态上限时实际收益可被裁剪 |
| Network maintenance | 固定 Energy 菜单；SCORE-01 前 7 季 6、v1 #1 全程 6、v1 #2 全程 5 | 1 Energy；公开 Network+1 / Dignity+1 | 可补可见状态，不证明清除隐藏隔离计数或修复具体关系事件 |
| Handle buried issue | 固定 Energy 菜单；SCORE-01 前 7 季 1、v1 #1 全程 3、v1 #2 全程 3 | 2 Energy；Dev 作用于内部风险量，不提供可见余额 | 只有公开 warning / 相关线索能支持候选比较；不能知道还剩多少，也不能证明一选就清空或阻止下一次事件 |
| Low-profile avoidance | 固定 Main action 菜单；v1 #2 M12 记录选过 1 次 | 消耗一个季度 Main action；公开 Health+1，内部风险下降 | 会放弃同槽增长机会；不是 trust crisis 的必然答案，不能仅为隐藏库存而固定选择 |
| Key-relationship repair | 固定 Main action 菜单；story repair 机会则依事件路径而变 | 消耗一个季度 Main action；公开 Network+1 / Dignity+1 | 不能以一次关系动作保证恢复整体 Network 或重置隐藏 streak |
| Other public story repair | 依事件链与公开选项出现，现有轨迹不能估计可遇率；Dev 语义扫描标出 Health 45、Dignity 62、Network/relationship 133、Wealth/career 51 个相关模板（多标签，可重叠） | 选择前看得到的是选项文本而非内部 delta；无统一数值成本/保证收益 | 按事件当前公共事实审查，执行后 fresh observe；模板数不是可复用答案表或因果证据 |

不能恢复或不能保证恢复：已发生的 terminal；已过去的 story 暴露窗口；未观察到的隐藏 risk / streak / rule余量；跨属性损失的全部后果；以及未来事件。行动后状态变化须以 fresh observe 确认，不把时间相邻自动当成因果。

## Counterfactual Findings（最多 5）

以下均是“若当时采用另一条公开信息处理/决策流程，值得检查什么”，不是已验证的反事实结果。

1. **v4 #1｜M5 末至进入 M6 前**：末次可见 Health 约为 3，之后 M6 的 review/story 窗口发生连续下行，Q2 Energy 未能出现。高价值反事实是把 pre-review buffer 检查放在 M5→M6 之前，而不是假设 M6 季度恢复先于事件。是否会存活未知。
2. **v4 #1｜M3 Q1 Energy，H2**：实际安排一次 Health recovery 后又投入 Network/Output。可比较的是在同一公开下降状态下，是否把更多可确认生存缓冲视为约束；一次本地选择不能证明“第二次恢复”会阻止后来死亡，也不形成 H2 规则。
3. **v4 #1｜终局前 H1 的增长选择**：Agent 已把潜在 `−1` 识别为重大生存风险却仍选增长。可检验的控制点是 material terminal risk 是否真正阻断非必要候选；最后 `−1` 的直接来源仍 UNKNOWN，不能据此说该选项造成死亡。
4. **SCORE-01｜M17–M18 公开低 Network / 低 Dignity 与半年窗口**：复核是否把持续状态、feedback 与可用关系修复机会一起送入下一次 review，而非只看某一个季度维度。M24 的 firing text 不能证明低 Network 或 performance 导致终局。
5. **Candidate v1 #2｜trust-crisis chain**：理论上最有价值的反事实检查点是第一次可公开识别的 trust warning 与后续选择；但原始 cue / action / 两次危机时间点都无法由提交摘要恢复，故本局 counterfactual 本身 `UNKNOWN`，不得补写事件答案。

S01 的 M19 terminal 缺少月度状态和 failure reason；不能构造有证据的局内反事实。

## Candidate Policy Changes

这里 `ADOPT_CANDIDATE` 仅指建议 Main 纳入下一轮静态候选审查，不表示本任务已改策略或已通过实跑。

| Candidate rule | Evidence / leverage | Decision | Boundary |
|---|---|---|---|
| Public-state multi-channel Survival Guard：health trend、公开 trust/compliance cue、Dignity/Network/Wealth 状态及半年 feedback 共同作为约束输入 | 多通道 Dev pathways + v4 Health terminal + v1 #2 trust terminal | `ADOPT_CANDIDATE` | 只读公开 fresh facts；分清 Observed / Inferred / Unknown；不计算隐藏风险余额 |
| Pre-quarter 与 pre-review reserve checkpoint | `game.py` 顺序确认 late Energy 不能覆盖前置 story；v4 M6 terminal 与 v1 #1 M6 恢复对照 | `ADOPT_CANDIDATE` | 关注下个 risk/review window 和可用 recovery timing，不写固定月份→固定行动 |
| 以趋势、最近 shock 与恢复可达性调整保护强度 | v4 有回补后再下行；v1 #1/#2 显示 Health 与 terminal 通道不等价 | `ADOPT_CANDIDATE` | 不将 observed `−1/−2` 当全局冲击上限；不设精确 Health cutoff |
| 对明确的 trust / confidentiality / retaliation / health material cue 做当前候选完整 Risk Review | v4 合规事件被识别；v1 #2 有非-Health terminal 类别 | `ADOPT_CANDIDATE` | 关键词仅触发审查，不直接决定选项；没出现 cue 不等于隐藏风险清零 |
| Survival 是安全约束而非默认最大化目标；风险可控时保留合理增长路径 | v1 #1 以非满 Health 状态完成 48 月，v1 #2 证明满 Health 仍可能遇非-Health terminal | `ADOPT_CANDIDATE` | 证据不足以定义统一安全边际；不因普通软成本自动否决增长，也不允许忽略 material risk |
| 对 hidden-risk cleanup / low-profile 策略的普适配额或“trust crisis 必选” | v1 #2 compact run 缺少危机 cue/choices；Dev 内部风险不可见 | `DEFER` | 先要可比较的公开触发与结果证据；不由终局反推固定 answer |
| 固定 Health 数值、Dignity/Network/Wealth streak、HiddenRisk/HP threshold、每季必恢复或最大冲击规则 | 单局轨迹与 Dev 内部机制不能证明可迁移公开阈值 | `REJECT` | `DO_NOT_ENCODE`；即使数值在本地 Dev 源可读也不得进 runtime policy |
| Event title→action 表、单一“必然危险”事件标签或新增 Skill / durable Memory 作为生存捷径 | 没有跨运行证据显示查表或新架构不可替代 | `REJECT` | 保持现有 3-Skill + Single Agent 分工；不扩大本任务范围 |

## Remaining Unknowns / DO_NOT_ENCODE

- **UNKNOWN**：S01 M19 终止通道；SCORE-01 M24 的具体 failure rule 与终局 Health/Dignity；v1 #2 两次 trust-crisis 的公开 cue/choices/间隔；S06 Run #1 的 Health/Dignity/promotion 月度序列。
- **UNKNOWN**：故事修复机会在未来某局的真实出现频率、选项内部收益、HiddenRisk 当前值、隐藏 streak / failure余量以及事件路径的随机性。
- **UNKNOWN**：上述 Survival Guard / timing checkpoint 对存活、总分或稳定 80+ 的因果效益；隐藏 Test/cloud 是否同分布。
- `DO_NOT_ENCODE`：经验 Health cutoff、单次最大伤害、Dignity/Network/Wealth 的精确连续月数、HiddenRisk 数值/失败余量、固定季度恢复日历、事件标题答案表、从无预警推断安全、将幸运存活样本升为必胜规律。
- Candidate / Memory / Skill / Team 状态不由本报告改变；Memory 未实现、第五 Skill 与 Team/Swarm 仍 deferred，Single Agent 仍是唯一 action submitter。

## Verification

- 起始 branch 为 `main`；fetch 后 `HEAD == origin/main == 08270978f6c5f3a4a0eaadf90840d01056472a8a`，起始 working tree clean。
- S01、SCORE-01、v1 #1/#2、S06 #1 的 Git 历史路径及 commit identity 均以只读 `git show` 核实；installed simulator/data package metadata 与 Source Lock 相符。
- S04 两局的 events/transcript 原件路径检查为 unavailable；没有读取未通过 committed hash identity 的 raw。S06 Run #1 也仅使用已记录的 Main-reviewed compact evidence。
- 本文所有本地 Markdown links 均解析到已存在目标；候选决策共 8 条，counterfactual checkpoints 不超过 5。
- 变更范围仅为本 review 文件；Skills、candidate/config、`CURRENT_STATE.md`、`ARCHITECTURE_DECISIONS.md`、Runner、依赖和 runtime 均未修改。
- `git diff --cached --check`: `PASS`。Provider requests / service starts / installs / MCP calls / games: `0`。

## Next Recommendation

`RETURN_TO_MAIN_FOR_S06_12_PROMOTION_PERFORMANCE_REVIEW`
