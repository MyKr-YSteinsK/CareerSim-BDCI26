# 04｜Rolling Planning 逐段拆解

[统一入口与术语](../00-从这里开始.md) · [本 Track 阅读路线](01-从零理解Agent、Instruction与Skill.md)


本章对应[历史 Rolling Planning](../../skill-evolution/04-v6-auditable-control-loop/skills/rolling-planning/SKILL.md)的标题与七个二级 section，编号 P00–P07 仅供教材覆盖检查。**FACT** 来自原文；解释目的与取舍的内容标 **INTERPRETATION**；数值与月份示例标 **TEACHING EXAMPLE**，不能当真实策略阈值或事件答案。

Planning（规划）不只是“下一步选哪个”。它让当前合法选择持续服务一个公开目标，又在真实反馈、资源约束与剩余时间变化时允许修正。它是唯一战略 owner，但没有工具提交权。

## P00｜标题与 metadata：每次应用，不等于每次全文读取

原文标题为“Rolling Planning｜公开证据滚动规划”。name 辨认模块，description 指出每次决策必须应用、唯一战略 owner、维护公开 Gap、Progress、含生存趋势的 Risk Budget 和必要 checkpoint，不提交。

**FACT**：metadata 概括职责，不额外增加一个运行步骤；具体触发和字段看正文。正文要求每决策 quick scan（快速扫描），完整规划只在指定复核点展开，文件重读另由 Instruction 管。

**INTERPRETATION**：滚动意味着当前计划可随新证据更新，而不是开局制定完整 48 月动作表。你应始终能说明“为什么这个候选服务当前目标”，但不必为每个普通故事重复写一页战略。

## P01｜职责与快速扫描：先有材料，再有目标与候选

原文要求基于同局 fresh public facts 与 Board 做短 scan：survival constraint（生存约束）、一个 Primary Gap（主要差距）、Progress（进展）、remaining realizable horizon（剩余可兑现时间）。状态改变后先新观察，不能用变更前 scan 决定下一项 Energy/Main。

**FACT**：只使用当前局公开证据、Board 可核实事实与公开 Handbook；不使用别局、局后事实、隐藏阈值、评分权重或内部公式。CONTROL marker 由常驻 Instruction 的执行职责生成；Planning 不复制其格式，也不提交。

**INTERPRETATION**：Planning 接收的是可靠事实，不是一份已经决定答案的 Board。它把当前约束和目标放在一起比较价值，然后产生合法候选。Risk 才检查该候选的具体风险。目标价值高并不证明候选风险可接受，反过来风险审查通过也不证明它最值得选。

**TEACHING EXAMPLE｜教学示例，不是历史 Run 原始记录。** Board 记录公开反馈“交付证据不足”和当前可选工作项；Planning 将“形成可验证交付”作为一个 Gap，比完成已有结果与开新项目。它可以生成 A，但不能先写“Risk=PASS 因为 A 最有成长价值”。Risk 的判断对象与依据还未被检查。

## P02｜Planning state：四类工作状态分别做什么

| 状态 | FACT｜原文定义 | INTERPRETATION｜使用方法 |
|---|---|---|
| Primary Gap | 一个公开主要差距，证据不足 UNKNOWN | 给当前比较一个共同焦点，不是隐藏评分维度排序 |
| Progress | ADVANCING / STALLED / UNKNOWN | 判断目标是否有可比公开进展，不能由表扬直接确立 |
| Risk Budget | AVAILABLE / TIGHT / UNKNOWN | 当前候选之外的生存约束语义，给具体候选审查上下文 |
| Horizon | 公开剩余时间及仍可实现收益窗口 | 关注收益是否来得及兑现，不预测内部晋升条件 |

### 为什么只能一个 Gap

**INTERPRETATION**：一个目标不是只允许一个收益维度，而是要求取舍有主轴。复合选项可以同时增长 Skill、Network、Output；Planning 应问哪项贡献直接服务当前主要差距、哪些是次级收益。若同时把三个维度都设成首要目标，任一菜单都能因其中一点被说成“当前最重要”，比较就失去可复核性。

**TEACHING EXAMPLE｜教学示例，不是历史 Run 原始记录。** 公开反馈指出成果缺少可验证展示，合法 A 能完成并验证现有交付，B 主要扩展人脉，C 是一般技能训练。若 Gap 是交付证据，应先比较 A 的直接贡献与 B/C 的间接贡献和机会成本；如果新反馈明确指出关系阻碍交付，则可以重新选一个更受支持的 Gap。不能一段推理以 Output 为首要，下一段为证明 B 好又改成 Network，却没有新证据。

正确记录是“当前一个 Gap，A/B 可比较，未知收益保持未知”；错误记录是“全面均衡发展”之后按喜好选任何项。一个 Gap 可以被保留、改变或设 UNKNOWN，不是必须强行找一个短板，也不是永久不变。

### Risk Budget 为何归 Planning

**FACT**：它是 candidate-independent（候选无关）约束。AVAILABLE 指未观察到当前重大生存约束收紧预算；TIGHT 指有公开依据显示预算收紧；UNKNOWN 指证据过期、缺失或不清。先生成候选，再让 Risk 做 candidate-specific（候选特定）gate。

**INTERPRETATION**：预算描述当前承受成本的背景，不能因为想选 A 就临时写成 AVAILABLE、想选 B 就写 TIGHT。Risk 可以问 A 是否直接加重健康负荷，但不应重新定义整段任务的预算和目标。这样才能判断“风险被发现”与“战略资源本来就紧张”分别由谁支持。

原文将公开健康明显低或可比观察持续下降纳入 survival trend（生存趋势）；其他生存相关维度持续恶化则结合可信公开警告／后果。近期冲击方向和现实可达恢复机会影响保护程度。不得设数字 cutoff、隐藏连续次数、固定恢复配额，也不把一次小幅下降当普遍触发。

**TEACHING EXAMPLE｜教学示例，不是历史 Run 原始记录。** 健康在可比公开观察中持续下降，公开反馈提示严重负荷，下一可用恢复窗口很远。Planning 可判断预算收紧；一个不加重健康负担、仍能推进 Gap 的合法选项并未自动失去价值。错误做法是“预算 TIGHT，所以所有成长暂停，固定恢复三次”，或者逐笔把小损失都写成 Soft Cost 来忽略整体约束。

**FACT｜真实支持**：v6 M6 的 Health 6→5→4 与警告后使用 TIGHT，后来恢复至 6 且警告清除后使用 AVAILABLE。这是一次语义变化观察，不是 `Health≤4` 的普遍规则。

### Horizon：可实现，不是能想象

**INTERPRETATION**：当前剩余时间短、结果需要更晚才能兑现时，即使路径听起来长期有利，也要明确时机未知或超出窗口。只用公开月份、已知反馈窗和选项说明，不从某一次晋升倒推“做满几月必升”。未知 payoff timing（收益时机）保持 UNKNOWN；这与资源紧张是两种不同约束。

## P03｜Full checkpoint 与 review reset：真正需要重建的时机

原文完整复核 trigger 是：新局基线；当季首次 Energy 前；已知半年 review 前最后行动窗 reserve check；实际正式 review/feedback/promotion/no-advance；strict STALLED；context recovery。并发合并一次；普通派生标签变化不得递归触发。

**FACT**：单独的重大新公开状态变化触发 Board refresh 与 Planning quick scan，可更新预算或 Gap，不自动 full checkpoint。无需额外 FOUNDATION/PROMOTION/COMPOUNDING/FINAL_SPRINT 枚举；不影响选择的 phase/mode 名称不输出。

**INTERPRETATION**：区分快速调整与完整复核，是为了让有变化的事实及时进入决定，同时避免一项变化引出无穷“再确认”。你不需要先给每个月命名一个阶段，才能应用目标、约束与时间。

### 实际反馈之后怎样 reset

原文要求刷新 Board facts，使旧 Progress comparison 失效，用新证据建立 baseline（基线），重新选择／保留／UNKNOWN 一个 Gap，CP 包含 R。不能从 silence（没有记录）推断 no-advance，也不能延续旧 Level 的比较或估计晋升概率。

**TEACHING EXAMPLE｜教学示例，不是历史 Run 原始记录。** M12 正式公开晋升后，旧 Gap 仍可能是交付不足，但旧职级的进展比较已经不能直接续用。你可以保留 Gap，却必须标明新基线；保留目标不是保留旧 STALLED。反例是“这季没看到晋升消息，默认没晋升，继续累计第二次停滞”。缺少消息只是 UNKNOWN，除非实际看到公开 no-advance 结果。

CP 的 N/Q/H/R/P/C/- 分别编码新局、季度、反馈前储备、反馈后重建、严格停滞、恢复、无完整复核。P=A/S/? 是 ADVANCING/STALLED/UNKNOWN，与 CP=P 是两个位置。QR 或 CHR 代表并发不同实际 trigger 合并，不是多次递归复核。

## P04｜Checkpoint output：为什么只要六字段

**FACT**：完整 checkpoint 最多 Horizon、Primary Gap、Progress、Recent Effect、Risk Budget、Path Trade-off 六字段；路径最多两个，不复制 Board 或 transcript。季度联合比较 Energy/Main 的互补、一个 Gap、直接相关约束与重复投入前观察效果。

**TEACHING EXAMPLE｜教学示例，不是历史 Run 原始记录。** 下面是短记录样式，字段内容不是历史原记录：

```text
Horizon: 公开 M15 / 48，下一已知反馈窗 M18
Primary Gap: 当前公开反馈的交付证据缺口
Progress: UNKNOWN（旧职级基线已失效，尚无干净可比进展）
Recent Effect: 一次公开结果已确认；对目标的影响未能直接归因
Risk Budget: TIGHT（公开健康趋势和当前严重负荷警告）
Path Trade-off: 当前合法的低负荷结果验证 vs 加负荷新机会；不保证结果
```

**INTERPRETATION**：六字段让规划可交接，而不是追求一份看似完美的长篇推理。输出短不能成为省略重要风险的理由；输出长也不能替代来源。特别是 UNKNOWN 的依据要短而清楚，不能只写标签不说明缺什么。

### reserve check 保护的是哪一个窗口

原文在已知半年 review 前最后可行动窗检查 fresh survival facts、warning、剩余 story exposure（故事暴露）和可验证恢复机会；不能依赖 review 后 Energy 修复此前伤害。

**TEACHING EXAMPLE｜教学示例，不是历史 Run 原始记录。** 已知反馈将先于下一次可用资源选择到来，当前健康警告未解除。正确比较关注现在合法动作是否可保护这个窗口；错误想法是“下季度有 Energy，先硬扛到反馈以后”。还要确认恢复选项真的当前合法；假想的恢复动作不能当缓冲。

**FACT｜真实证据**：v6 H trigger 被记录为 MISSED，不能把这个教学 checkpoint 当已实际执行。细节见[真实案例章](07-真实案例、反例与失败模式.md)。

## P05｜Progress / STALLED：严格条件逐项看

ADVANCING 需要 Gap 本身改善或直接关联的公开职业进展；表扬、菜单描述、不可比状态不够。advertised effect（宣称效果）是先验，可靠同局 observed effect（已观察效果）优先。一次无增长可以引起注意，但不是严格停滞。

**FACT**：STALLED 必须同一 strategic action（战略动作）、同一 Gap、两个相邻 comparable checkpoints（可比复核点）都无 observed target progress。动作／Gap／目标改变、过期、故事混杂、来源不清或前后不可比用 UNKNOWN。满足后比较一个不同类型的合法 alternative，但不强制 switch（换路）。

### 用数字与月份把两个复核点写出来

**TEACHING EXAMPLE｜教学示例，不是历史 Run 原始记录。** 假设 M6 正式反馈后已建新基线，当前 L2、Output=10，Gap 是交付输出。之后没有新正式反馈／晋升，也没有影响目标的混杂事件；同局公开来源可直接确认两次相同战略动作“准备汇报材料”的目标响应。

| 时点 | 当前公开目标值 | 复核性质与条件 | 此时可写什么 |
|---|---:|---|---|
| M6 | Output=10 | feedback 后新基线 | 还没有两次无进展；不写 STALLED |
| M7 | Output=10 | 实际 context recovery 的 checkpoint；第一次同动作未见目标进展，恢复依据可验证 | 单次无进展，仍不足；证据不完整则 UNKNOWN |
| M9 | Output=10 | 当季首 Energy checkpoint；第二次同动作同 Gap、与 M7 相邻可比且无进展 | 在全部条件成立时可以 STALLED |

月份用于定位教学数据，不是一张“到 M9 就停滞”的时间表。M7 的复核是恢复触发，M9 是季度触发，不能在普通故事中凭空增加 full checkpoint。若 M7 与 M9 之间有真实正式反馈，应先 reset，不能把表中两个点硬连；若第二次其实用了不同动作，或目标改为 Network，也不满足同动作同 Gap。

如果 M9 clean observe 是 12，则该目标有可见增长；是否 ADVANCING 仍要关联当前 Gap。若数值仍 10 但事件／反馈同时污染，结论是归因 UNKNOWN，不是把零增长当稳固停滞证据。这些限定正是严格规则的一部分。

### STALLED 后为什么不强制换

**INTERPRETATION**：两次可比失败值得考虑不同路径，但不保证任何替代都更好。替代可能当前不可用、公开成本更大，或新证据表明原动作对新的目标仍有价值。必须比较是在防止惯性；不强制切换是在避免把少量观察变成固定答案。

**FACT｜真实证据**：v6 曾重复准备汇报材料而未见 Output 增长，随后选另一项 Energy，但未建立严格双 checkpoint 条件。它只能说明一次观察响应与调整，不能认证 STALLED 被触发；报告明确是 NOT_TRIGGERED。

## P06｜Energy、Main 与 story：联合规划不是批量执行

Energy（资源选择）与 Main（季度主行动）应围绕当前 Gap 联合比较：哪种资源投入为主行动提供互补，重复投入的公开效果是否仍相关，当前约束是否被加重。原文禁止 fixed bundle（固定组合）、菜单目录与固定赢家。

**TEACHING EXAMPLE｜教学示例，不是历史 Run 原始记录。** 暂定先准备现有结果、再做相关主行动。第一项 Energy 执行后新观察显示当前结果已充分完成，或出现重大警告，第二步就应重新 quick scan；原联合方案不能变成已批准批次。每个状态改变后 observe→Board→Planning，再选择下一项。

**反例**：“第一步选了材料准备，所以剩余 Energy 必须全部投入 Output。”它把目标互补变成配额，把未观察的未来当成已确认状态。另一个反例是遇到新反馈仍按开局固定动作序列继续，违背反馈 reset。

普通非战略 story（故事选择）最多两个最强合法候选一次；无 fresh evidence 不重开，除非 Risk=RECONSIDER。不能按 event_id/title 查答案，也没有固定 primitive ranking（动作原语排名）。有界比较要体现真正的公开差异，不能先选五个再反复说“只比两个”。

## P07｜权限与边界：建议可以被 Agent 修正，不能自行提交

**FACT**：Planning 向 Single Agent 提供有界建议，不调 new_game、observe、take_action，不创建持久／跨局记忆或另一个审查者。session、月份、状态、效果或选项不新鲜／不可比时标 UNKNOWN，回正常流程补公开事实。

**INTERPRETATION**：战略 owner 的含义是同一决策过程里只有一处负责目标和路径，而不是建议永远必须照做。最终 Agent 应综合相关 Risk 与合法性作决定，但不能通过“我不接受建议”绕开事实、重比或终局风险合同。

## 运行证据、练习与参考分析

**FACT**：[v6 验证](../../project/runs/v6-run1-validation.md)支持预算变化、公开晋升、一次无增益调整，同时记录 H 遗漏、普通事件反复重开和审计关联不足。不能把设计结构良好当作这些规则已持续正确执行。

练习一：Gap 是交付证据，公开人脉最低，是否必然改投人脉？练习二：同动作一次无增长，能否 P=S？练习三：Health 有约束但当前候选不加重它，是否全部成长禁用？练习四：已观察正式未晋升，是旧基线继续还是重建？

参考分析：比较公开瓶颈，不自动追最低数值；一次不足，缺可比条件还需 UNKNOWN；TIGHT 约束直接相关成本，不是全局禁令；正式 no-advance 也触发新 baseline，不能机械累计旧停滞。P00–P07 全部覆盖后，下一章只对已生成候选审风险，避免重复做这套战略。
