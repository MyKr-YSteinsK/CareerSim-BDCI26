# 05｜Risk Review 逐段拆解

[统一入口与术语](../00-从这里开始.md) · [本 Track 阅读路线](01-从零理解Agent、Instruction与Skill.md)


本章按[exact-v6 Risk 原文](../../skill-evolution/04-v6-auditable-control-loop/skills/risk-review/SKILL.md)的标题和五个二级 section 阅读，覆盖编号 R00–R05 只用于教材。**FACT** 描述规则与运行记录；**INTERPRETATION** 分析判断边界；**TEACHING EXAMPLE** 是构造场景，绝不补成历史 Run 原始记录。

Risk Control（风险控制）在这里不是“永远选最安全”，而是对已经生成的候选，检查公开重大后果是否需要更仔细审查或一次相关重比。它是同一个 Agent 的专项职责，不是第二个长期 Planner。

## R00｜标题与 metadata：候选特定的门禁

标题“Risk Review｜候选风险门”说明审查对象。name 是 risk-review；description 规定每个 take_action 前必须应用，只对已生成候选做 candidate-specific Material Risk gate，不规划、不提交。

**FACT**：metadata 是用途与触发摘要；它不意味着每步一定做 FULL_REVIEW，也不授权自行执行工具。正文区分快速门禁和完整审查；两者都要有候选，不能先按故事标题填结论。

**INTERPRETATION**：candidate-first（先候选）使风险判断可以回答“哪项具体后果、哪条公开证据、哪个合法替代”。如果只说“这则故事危险”，你还不知道所选动作是否承担危险，还是恰好缓解危险。

## R01｜QUICK_GATE：每个动作前，检查什么

原文每个 story、Energy、Main take_action 前，检查已生成合法候选、新鲜同局公开事实、明确公开后果、直接相关高信号 cue、新鲜警告，以及预算 TIGHT 时候选是否直接加重对应生存风险。

**FACT**：没有候选相关 Material Risk（重大风险）或高信号线索时 PASS；普通不确定性、Soft Cost（软成本）、一般负荷／分歧、日常 CI/testing、泛化角色或项目词、普通交付／关系／组织政治不单独触发 FULL_REVIEW。

**INTERPRETATION**：quick gate（快速门禁）不是跳过风险，而是确认没有需要完整展开的相关重大线索。不能因为每动作都应用 Risk，就每动作都强行找一个危险；也不能因为某类日常成本通常普通，就忽略当前公开趋势已使它成为重大约束。

**TEACHING EXAMPLE｜教学示例，不是历史 Run 原始记录。** 当前没有健康或合规重大警告，候选是澄清同事与自己的任务接口，公开代价只是一次普通沟通摩擦。若没有其他相关高信号线索，quick gate 可以 PASS。错误做法是看到“分歧”便 RECONSIDER，强迫 Agent 选最圆滑路径；普通关系取舍应由 Planning 比较目标收益和成本。

另一个构造情境是公开健康持续下行，Planning 已据此设 TIGHT，候选却追加当前健康负荷。这就不能用“也是普通工作量”结束 quick gate；相关公开背景已经改变，需要完整审查。

## R02｜Contextual cue families：线索只负责把问题带进来

原文保留 NONE / HEALTH / COMPLIANCE / TRUST / RELIABILITY / OTHER 这些类别名，但不扩成长关键词字典。四类高信号情境分别是保密／数据授权；有明确重大后果的隐瞒／诚信；关联新鲜公开状态的健康负荷／疾病；重大可靠性事故。

| 线索情境 | FACT｜关注的公开关联 | INTERPRETATION｜不能直接推出 |
|---|---|---|
| 保密／数据授权 | 该候选是否涉及公开说明的权限或保密后果 | 看见“资料”就认为泄密 |
| 诚信／隐瞒 | 隐瞒与明确重大后果的关系 | 一切信息保留都等于造假 |
| 健康负荷／疾病 | 候选负荷与 fresh public state 的关系 | 一次普通加班就是终局风险 |
| 重大可靠性事故 | 当前公开事故及候选具体后果 | 任何测试或 CI 都是重大事故 |
| OTHER | 窄的类似重大情境出口 | 任意不喜欢的选项都装进 OTHER |

**FACT**：普通交付范围、薪酬／职业、关系边界、组织政治归 Planning，除非出现明确重大后果才升级 Risk。不能读隐藏 status update、隐藏计数、其他 session 或 Dev 答案，不按 event_id/title→choice 查表。

**TEACHING EXAMPLE｜教学示例，不是历史 Run 原始记录。** 公开菜单 A 是按既定权限共享结果，B 是把明确未授权的资料转交外部。两个都带“资料”这个词，但公开后果不同；应审当前候选的实际权限情境。若不知道资料权限，记录相关 UNKNOWN，不能从标题推一个固定答案。

**INTERPRETATION**：cue（线索）让 Agent 留意可能重要的事实，不是替代证据。关键提问是“当前公开证据是否把这个候选升级为重大后果”，而不是“命中了多少个风险词”。

## R03｜FULL_REVIEW：五种状态怎样区分

原文的 Material Risk 包括明确公开重大健康／生存、信任危机、保密／合规、报复／升级、解雇或同类后果；Soft Cost 包括少量 Health/Dignity 成本、时间、普通摩擦、压力或不确定性。

**FACT**：一笔小额健康代价只有在相关公开生存趋势没有使该维度成为当前约束时，才可孤立按软成本处理。若 Planning 因公开趋势将预算设 TIGHT，Risk 不能把下一笔小损失孤立评估。Budget 和 cue 都不是隐藏风险估值。

### PASS 与 ALLOW 不是同义的证据过程

| 状态 | FACT｜含义 | 已完成什么 | 没有证明什么 |
|---|---|---|---|
| PASS | quick gate 无相关重大风险／高信号线索 | 快速门禁结束 | 没有任何风险、最优或未来安全 |
| ALLOW | FULL_REVIEW 后没有要求改变候选的重大风险 | 完整审查结束，候选可接受 | 风险绝对为零或收益保证 |
| WARN | 新鲜清楚的公开证据有 concern，但不要求更换候选或直接缓解 | 已形成一条公开证据提醒，可提交 | 已执行缓解、无需继续观察结果 |
| RECONSIDER | 重大风险明确、有直接合法替代、候选未处理 | 必须先做一次相关比较 | 必须最保守或任意换项即可 |
| UNKNOWN | 相关证据过期／缺失／来源或后果不清 | 标出未知并按有界刷新规则回退 | 视同 PASS，或无限追加读取 |

**INTERPRETATION**：PASS 记录没有展开 full review 的路径；ALLOW 记录已展开后的接受结果。若把两者当纯同义词，审计就无法知道本次是否检查过重大情境。WARN 与 RECONSIDER 的区别也不只是风险强弱，而是公开证据是否要求且能够触发直接相关的候选重比。

**TEACHING EXAMPLE｜教学示例，不是历史 Run 原始记录。** 候选涉及一个已公开的保密边界，完整审查后确认它在允许权限内且没有要求改变的重大风险，可以 ALLOW；不能说“已经 review 过但没事，所以还是 PASS”。若有公开担忧却没有足够依据要求改选，可以 WARN 加一句来源理由；不是把不确定担忧升级为命令。

### RECONSIDER 的三个同时条件

1. 当前公开 Material Risk 明确。
2. 当前菜单存在直接相关、合法的缓解 alternative（替代项）。
3. 当前候选没有处理该风险。

缺其中一项不能因为“另一个选项更安全”自动 RECONSIDER。相关合法替代不是所有备选：如果健康负荷是问题，一项纯人脉投入未必直接缓解；如果“请假”菜单不存在，它就不是当前合法替代。

**TEACHING EXAMPLE｜教学示例，不是历史 Run 原始记录。** 已公开身体负荷严重，A 是承担额外高负荷，B 明确合法地减少该负荷；A 未处理风险。Risk 可 RECONSIDER，Agent 只比较 B 一次。若换到 B，Risk 再检查 B 自己的公开后果，然后才能生成对应 CTRL 并提交。

**错误例子一：不 re-gate。** 原候选 A 有健康风险，换 B 后 B 却有公开的合规后果；沿用 A 的 Risk 输出，忽略了审查对象已变化。重 gate 不要求 B 必须失败，要求的是它独立被检查。

**错误例子二：无限替代搜索。** 比完 B，又无新证据地找 C、D、E，反复起草计划。原文只允许一个直接相关替代的有界比较，不允许把风险复核变成长程新规划。

### 可以保留原候选，为什么 X=1 仍不够

**FACT**：exact-v6 允许在一次比较完成、有公开证据支持时保留原候选；CTRL 可 `R=RECONSIDER, X=1`。X=0 表示未完成，始终禁止动作；无 RECONSIDER 用 X=-。若候选改变，最终候选重 gate。

**INTERPRETATION**：X=1 是分支完成记录，不是“任何动作都安全”的通行证。下一节的 terminal-risk constraint 仍成立。不能为了让 X=1 看起来闭合，就忽略已公开、可避免且有直接缓解项的终局风险；完成比较不取消其他合同。

## UNKNOWN 的一次刷新：结束循环，而不是创造事实

**FACT**：相关证据不清时，如果正常允许流程可以补得 fresh public state，只刷新一次；否则保留 UNKNOWN 并做一次 bounded legal decision（有界合法决定），不死循环。

**TEACHING EXAMPLE｜教学示例，不是历史 Run 原始记录。** 当前候选的相关警告只在旧摘要里，新状态可以合法读取。Agent 取得一次新观察，Board 更新事实，Risk 再根据当前候选审查。若后果仍未公开，保持 UNKNOWN，在已有公开合法信息范围内比较；不能反复 observe 直到模型愿意说 PASS，也不能凭空补 session 或菜单选项。

**反例**：每次 UNKNOWN 都再调用一次，再新起一轮 UNKNOWN，声称“每轮只刷新一次，所以没有超预算”。这把同一诊断分支拆成无穷新轮，实际没有新 material evidence（实质证据）。有界规则限制的是一次相关未知处理，不是换措辞后重置次数。

## R04｜Terminal-risk constraint：哪些候选不能因比较完成就提交

原文说：fresh public evidence 表明候选已知 effect 会增加可避免的 terminal/material survival risk，且有直接合法 mitigation（缓解项）时，不得提交明显加重风险的非必要候选。Single Agent 仍有最终提交权，但受此约束。

**TEACHING EXAMPLE｜教学示例，不是历史 Run 原始记录。** 当前已公开严重健康警告，A 明确加重该危险且不是必要行为，B 合法直接缓解。Agent 不能说“我比过 B，X=1，所以可以为了多一点成长选 A”。若公开证据说明某项负荷不可避免、或 B 并不能合法处理，实际条件不同，不能照搬例子结论。

**INTERPRETATION**：这把“安全是约束”落到具体候选上，不让安全变成默认唯一目标。无重大风险时，公开目标贡献明显更高的成长路径可以接受普通成本；已满足终局约束时，目标收益不能把合同消掉。区别靠公开后果与候选关联，不靠保守语气。

## R05｜权限：Risk 只 gate，不拥有战略或工具

原文 QUICK_GATE / FULL_REVIEW 只审已生成候选，不拥有 Primary Gap、一般策略、phase 或持久风险状态；不调 observe、take_action、new_game，不创建第二审查者，不能跨 session 复用旧判断。

**TEACHING EXAMPLE｜教学示例，不是历史 Run 原始记录。** Risk 看 A 加重当前负荷，可以要求比直接减负 B；不能写“未来所有季度低调避险，Primary Gap 改为健康”。后者是长期目标与政策，应由 Planning 根据新公开约束维护，不由 Risk 接管。

**INTERPRETATION**：“最终提交权”与“有权任意绕开规则”不同。Agent 应用多个职责完成决定，Risk 提供必要候选约束；它既不独立执行动作，也不是仅供参考的装饰性签名。

## 真实证据与自测

**FACT**：[v6 记录](../../project/runs/v6-run1-validation.md)确认 M13 一次 RECONSIDER 比较并选择低负荷合法替代，再 gate；标记文字重复，具体 CTRL 配对与 Gap 为 UNKNOWN。M6 的生存预算变化也有公开依据。上述事实不能证明每次 Risk 语义都正确，更不能推风险审查使分数上升。

自测：普通关系摩擦应否默认 FULL_REVIEW？完整审查后可接受应 PASS 还是 ALLOW？有 concern 是否必定重比？换候选能否沿用原 gate？UNKNOWN 是否等于无限追问？

参考分析：不默认升级；完整审查后用 ALLOW 等 full 状态；RECONSIDER 有三个同时条件，WARN 不强制改；换项重新 gate；未知处理有界并保留缺证据。若你还能说明这些判断需要什么公开材料，就能在下一章把 Risk 正确接入一次完整 Action。

R00 为标题／元数据，R01–R05 与五个原二级 section 逐一对应；UNKNOWN 的回退条款属于 R03，单独展开仅为教学清晰，不新增历史职责。
