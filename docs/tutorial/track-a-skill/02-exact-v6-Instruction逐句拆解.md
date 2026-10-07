# 02｜exact-v6 Instruction 逐句拆解

[统一入口与术语](../00-从这里开始.md) · [本 Track 阅读路线](01-从零理解Agent、Instruction与Skill.md)


本章覆盖[历史 Instruction](../../skill-evolution/04-v6-auditable-control-loop/instruction.md)的全部五行。为使检查可重复，按分号、句号和换行划成 **28 个条款单元 I01–I28**；编号只属于教材，不是新增运行标记。一个单元可能有多个逻辑动作，都会在解释中展开，不能用“28/28”替代实际语义审阅。

**FACT** 是原文与对应 Skill 的规定。下表“为什么存在／忽略后的风险”是 **INTERPRETATION（解释）**，不是每句历史动机都已被作者记录。构造情境显式标为 TEACHING EXAMPLE；真实运行证据仅引用[验证记录](../../project/runs/v6-run1-validation.md)。

## 1. 先看完整原文

```text
48月；仅本局fresh公开事实；Single Agent唯一take_action提交者。
新局：new_game后首个fresh observe、首个take_action前，各read_file一次skills/structured-state-board/SKILL.md、skills/rolling-planning/SKILL.md、skills/risk-review/SKILL.md。Continue/context recovery：fresh observe→各重读三份→重建Board/Planning→首动作。正常上下文不逐步重读；仅context loss/规则无法恢复/文件改变时重读必要项。
序：observe→Board→Planning→候选→Risk gate→RECONSIDER比一个相关合法alternative；换候选重gate→CTRL→同回合紧邻take_action。每次action attempt对应一个紧邻pre-action CTRL；不得以CTRL结束回合；X=0不得调用take_action，比较后重出合法CTRL；CTRL不入notes。状态改变后fresh observe；不预判cue/复用旧scan。
Planning每决策维护公开Primary Gap；季度首Energy前联合规划Energy+Main；半年review最后行动窗reserve check；观察到review/feedback/promotion/no-advance后刷新Progress。Risk Budget独立于候选；先生成候选，再由Risk gate。安全是约束非默认目标；普通摩擦/少量代价属Soft Cost；无Material Risk时不因“更稳妥”自动放弃对Gap更强的公开收益。
CTRL B=<F|?> G=<gap|?> P=<A|S|?> R=<PASS|ALLOW|WARN|RECONSIDER|UNKNOWN> CP=<N|Q|H|R|P|C|-> X=<0|1|->。CP并发trigger合并一次。仅用公开48月horizon判断可实现性；禁hidden阈值/权重、event_id/title答案。
```

读到箭头时，理解为同一个 Agent 应承担的职责顺序，不是模块之间存在直接 Python function call（函数调用）。read_file（读取文件）与使用 Skill 功能也要分开：启动／恢复明确要求读文件，正常决策要求应用当前仍能可靠恢复的规则。

## 2. 第一行：时间、证据与提交者

| 单元 / 原文短片段 | 白话解释 | Owner（职责归属） | 为什么存在 | 忽略后的风险 | 相关 Skill |
|---|---|---|---|---|---|
| I01 `48月` | 任务看完整公开期限，不只眼前事件 | Agent；Planning 应用 horizon | 路径收益需要时间兑现 | 只挑当前奖励或幻想期限外收益 | Planning |
| I02 `仅本局fresh公开事实` | 信息属于当前游戏且仍新鲜，公开可用 | Agent 守边界；Board 核事实 | 长流程会留下旧状态 | 串局、旧观察、隐藏知识进入判断 | 三者 |
| I03 `Single Agent唯一take_action提交者` | 只有一个执行者调用动作工具 | Single Agent | 建议与外部状态变化需有明确责任 | 重复动作、模块越权提交 | 三者不提交 |

### 为什么“本局”“fresh”“公开”不能只检查一个

本局解决身份问题；fresh（新鲜）解决时效问题；public（公开）解决权限问题。三个条件必须一起成立。上一局新鲜数值不是本局事实；本局旧数值不能代表行动后的状态；本局工具输出中的未知权限字段也不能自动变成允许的公开证据。

**TEACHING EXAMPLE｜教学示例，不是历史 Run 原始记录。** M9 的公开观察在动作前显示 Wealth=8，动作后你只拿到 success。正确记录是“动作成功，当前 Wealth 待新观察确认”；错误记录是根据选项宣传算出 Wealth=10，再拿它比较下一候选。例中数值只说明时效，不能推隐藏公式。

**FACT｜运行证据**：202 次成功状态改变后均有新 observe，支持这局的新状态纪律；不能据此把未被独立检查的信息权限也判为全通过。

## 3. 第二行：启动读取与恢复读取

| 单元 / 原文短片段 | 白话解释 | Owner | 为什么存在 | 忽略后的风险 | 相关 Skill |
|---|---|---|---|---|---|
| I04 `new_game后首个fresh observe…各read_file一次` | 先开局有效观察，再在首动作前分别读 Board、Planning、Risk 原文 | Agent | 在实际情境出现后取得完整规则 | 只凭名字或旧摘要首次行动 | 三者 |
| I05 `Continue/context recovery…重建Board/Planning` | 恢复时新观察、重读三份、重建工作事实与规划，再首动作 | Agent 编排 | 恢复上下文可能缺规则或基线 | 旧目标、旧状态和半段规则被继承 | 三者 |
| I06 `正常上下文不逐步重读` | 日常应用不要求每一步再全文读文件 | Agent | 保持功能使用与文件读取分离 | 重复材料挤占工作上下文 | 三者 |
| I07 `context loss/规则无法恢复/文件改变` | 这些情况下重读必要项 | Agent | 规则已失效或不能可靠恢复时需补足 | 以“读过”为由继续错误规则 | 必要模块 |

I04 的次序不是“读到名字就算读到正文”；三个路径分别指三份历史规则。I05 对恢复明确要求三份重读；I07 给其他正常情境下的必要项读取条件，不应拿“只重读必要项”去取消恢复的三份要求。Board 重建事实，Planning 重建目标、基线和预算，Risk 在候选出现后重新应用，不需要独立持久风险状态。

**INTERPRETATION**：重读解决规则可得性，重建解决当前工作状态。两者缺一不可：重新读了规则却仍用旧健康值，或拿到新状态却忘了严格 STALLED 条件，都会让恢复不完整。也不能因为“压缩也许发生过”就声称某个不可见恢复 epoch 已被检测；这要按实际可观察证据报告。

**TEACHING EXAMPLE｜教学示例，不是历史 Run 原始记录。** 恢复后知道仍在同一 session，但上次 Gap 和效果依据无法找回。先新 observe，读三份，Board 写可确认事实、旧效果 UNKNOWN，Planning 建当前可支持的一个 Gap 或 UNKNOWN。错误做法是猜“之前大概在追人脉”，继承旧 STALLED 和 Risk Budget。

**FACT｜运行证据**：开局三份读取可确认；两次压缩后未重读可确认。不能把“开局读取通过”向后延伸成整局恢复遵循通过。

## 4. 第三行：一项候选怎样闭合为一次动作

| 单元 / 原文短片段 | 白话解释 | Owner | 为什么存在 | 忽略后的风险 | 相关 Skill |
|---|---|---|---|---|---|
| I08 `observe→Board→Planning→候选→Risk…一个相关合法alternative` | 先事实、目标、候选，后风险；RECONSIDER 只比一个直接相关合法替代 | Agent 编排；各模块完成本职 | 风险必须有明确审查对象且重比有界 | 未生成候选就填 Risk；无限扩候选 | 三者 |
| I09 `换候选重gate→CTRL→同回合紧邻take_action` | 换项后重新审新候选，输出 CTRL 后同回合紧邻提交 | Risk；Agent 输出与执行 | 替代项可能有自己的风险 | 原候选的通过结果误授予新候选 | Risk |
| I10 `每次action attempt…紧邻pre-action CTRL` | 每次尝试动作都有自己的动作前记录 | Agent | 记录需能关联到具体尝试 | 旧标记对应后来的另一项选择 | 三者提供依据 |
| I11 `不得以CTRL结束回合` | 不能只打印控制行就停止本回合 | Agent | 文本记录不是外部执行 | 看似决定完成，环境尚未变化 | 无独立模块提交 |
| I12 `X=0不得调用…比较后重出合法CTRL` | 替代比较未完成禁止提交；完成后更新控制行 | Agent；Risk 提重比 | 阻止半完成分支被当作决定 | 需要重比却先执行原候选 | Risk |
| I13 `CTRL不入notes` | 本版控制行是独立动作前文本，不塞进动作说明 | Agent | 保持本版本审计合同 | 把后继格式倒灌历史 | 不由 Skill 输出 |
| I14 `状态改变后fresh observe` | 后续选择前先获取新状态 | Agent 获取；Board 使用 | 预期效果不能代替当前状态 | 连发 Energy，忽略新变化 | Board；Planning |
| I15 `不预判cue/复用旧scan` | 不提前填候选风险线索，不把变更前扫描用于新动作 | Planning / Risk 按顺序使用新事实 | cue 相关性取决于候选与情境 | 先贴标签再找理由，或旧判断续期 | Planning；Risk |

candidate（候选）只是目前准备提交的合法选项，尚不是 Action（已执行动作）。alternative（替代项）必须在当前菜单里，并直接处理该公开风险；“如果可以请假”但菜单没有请假，不能算合法替代。re-gate（重新门禁）不是重做全部战略，而是审新候选自己的公开后果。

exact-v6 有一个容易误读的细节：完成一次相关比较后可以换项，也可在公开证据支持时保留原项。保留原项允许 `R=RECONSIDER, X=1`；X=1 说明比较已完成，不能说“风险已经消失”。这个语义来自历史 Risk 原文，与 v8a 的最终 R/RB 规则不同。

**TEACHING EXAMPLE｜教学示例，不是历史 Run 原始记录。** 候选 A 是额外承担已公开过重的值守，B 是当前合法的减负分工。Risk 满足三条件，Agent 比 B 一次并改选；B 也有其当前公开权限和责任后果，须重新 gate。错误做法是在 B 后沿用 A 的 R，或完成比较却仍写 X=0 就调用工具。

**FACT｜运行证据**：M13 确认相关重比、换成低负荷替代、再 gate。其精确 Gap、CTRL 配对与同回合门禁无法认证。[第六章](06-三Skill协同与一次Action闭环.md)将单独解释这个证据范围。

## 5. 第四行：战略状态、窗口与成长取舍

| 单元 / 原文短片段 | 白话解释 | Owner | 为什么存在 | 忽略后的风险 | 相关 Skill |
|---|---|---|---|---|---|
| I16 `每决策维护公开Primary Gap` | 保持一个当前主要差距，证据不足可未知 | Planning | 给候选比较共同目标 | 每看到新故事就换长期方向 | Planning |
| I17 `季度首Energy前联合规划Energy+Main` | 比较资源投入与主行动的互补 | Planning | 当前资源怎样支持后续行动 | 固定组合、分别各选各的 | Planning |
| I18 `半年review最后行动窗reserve check` | 反馈前最后可行动机会检查公开生存储备 | Planning | 危险窗口可能先于下一次恢复 | 指望反馈后的 Energy 补救已发生伤害 | Planning；Board |
| I19 `观察到…no-advance后刷新Progress` | 真正看到反馈／晋升／未晋升后重建进展基线 | Planning；Board 供新结果 | 新职级与新反馈改变可比语境 | 旧停滞结论跨反馈继承 | Planning |
| I20 `Risk Budget独立于候选` | 预算来自公开生存趋势，不随想选哪个候选任意改 | Planning | 战略约束先有客观依据 | 为喜欢的候选把预算改可用 | Planning |
| I21 `先生成候选，再由Risk gate` | 目标排序先给候选，Risk 后审它 | Planning→Risk | 目标价值与候选风险是不同判断 | 无对象的风险判决或双重排序 | Planning；Risk |
| I22 `安全是约束非默认目标` | 保护必要生存边界，同时比较成长 | Planning；Risk 执行具体约束 | 长程任务也需要职业进展 | 永久保守，或把约束当装饰 | Planning；Risk |
| I23 `普通摩擦/少量代价属Soft Cost` | 普通成本进入机会成本比较 | Planning；Risk 区分重大性 | 代价并非一律危机 | 任何成本都拦截成长 | 两者 |
| I24 `无Material Risk…不因更稳妥放弃更强收益` | 无重大风险时允许更强公开 Gap 收益承担软成本 | Planning；Risk 不越权否决 | 避免叙事礼貌替代价值判断 | 默认最圆滑选项，忽略目标 | 两者 |

Risk Budget（风险预算）不是一笔隐藏库存。Planning 从可比公开生存趋势、警告、冲击方向和可达恢复窗口判断 AVAILABLE / TIGHT / UNKNOWN；Risk 再问当前候选是否直接加重相应约束。UNKNOWN 不能为了推动动作被写成 AVAILABLE，TIGHT 也不能无差别禁止所有成长。

“少量代价”不能脱离上下文。公开健康持续下行已收紧预算时，下一笔小损失可能正好加重约束；不能把每笔成本单独切成“都很小”从而绕开累计趋势。反过来，没有重大风险与公开约束时，也不能只因 B 更保守就推翻 A 的明显目标贡献。

**TEACHING EXAMPLE｜教学示例，不是历史 Run 原始记录。** Gap 是当前公开反馈的交付缺口，两个合法选项都能增长人脉，但只有一个也能形成当前窗口可验证成果。Planning 比较互补和机会成本，不是按最低数值先补。若新观察表明健康负荷已成为约束，则重新审对应候选；不是永久禁用交付方向。

**反例**：提前联合规划了三项 Energy，第一项执行后效果与预期不符，仍原样完成剩余序列。联合规划是形成暂定关联，后续每个状态改变后的新观察才支持下一决定。

**FACT｜运行证据**：M6 公开健康下降并有警告时使用 TIGHT，恢复且警告清除后使用 AVAILABLE；真实晋升发生在 M6/M12/M18/M36/M48。H 触发遗漏与 reset 文本配对含糊都被审计记录，不能把这些月份写成系统默认晋升表。

## 6. 第五行：CTRL 字段与禁止项

| 单元 / 原文短片段 | 白话解释 | Owner | 为什么存在 | 忽略后的风险 | 相关 Skill |
|---|---|---|---|---|---|
| I25 `CTRL B/G/P/R/CP/X` | 六字段压缩本次事实、目标、进展、风险、复核与重比状态 | Agent；模块供语义依据 | 便于将规则应用与动作关联审查 | 只填格式、不核对语义，或字段混用 | 三者 |
| I26 `CP并发trigger合并一次` | 多触发合并一次规划，各代码一次 | Agent；Planning 判断触发 | 避免递归完整复核 | 同一步反复重建、多个矛盾基线 | Planning |
| I27 `公开48月horizon判断可实现性` | 用公开剩余期与可达窗口判断收益能否兑现 | Planning | 远期收益未必来得及 | 推测隐藏晋升时点或未来必有窗口 | Planning |
| I28 `禁hidden阈值/权重、event_id/title答案` | 不推内部公式，不查标题／ID答案表 | Agent；三个模块共同守边界 | 公开证据与隐藏机制不能互换 | 用事后机制硬编码当时选择 | 三者 |

### 六个字段分别是什么

| 字段 | exact-v6 取值 | 依据与容易混淆处 |
|---|---|---|
| B | F / ? | F 只表示用本局 fresh state 做了事实扫描，不保证所有其他环节正确 |
| G | gap / ? | 一个 Gap 的短 key；例中 G=O 仅教学用 Output key，不是原文冻结的 key 字典 |
| P | A / S / ? | ADVANCING / STALLED / UNKNOWN；它是进展，不是 v8a 的 Advance/Stabilize 模式 |
| R | PASS / ALLOW / WARN / RECONSIDER / UNKNOWN | 当前候选风险语义；不是 CP 中的反馈 reset R |
| CP | N / Q / H / R / P / C / - 及合并 | 新局／季度／review 前／反馈后／严格停滞／恢复／无完整复核 |
| X | 0 / 1 / - | 相关替代比较未完成／完成／未触发；它不编码效果好坏 |

CP 可以是 QH、QR、CHR：例如季度复核与反馈 reset 同时实际满足，合并为 QR，做一次规划。不能仅因一个派生 Gap 标签改变再触发另一完整 checkpoint。CP=P 的 P 是 plateau diagnosis（停滞诊断），字段 P=S 才表示 Progress 为 STALLED；两个 P 位于不同字段。

**TEACHING EXAMPLE｜教学示例，不是历史 Run 原始记录。** 假设当前公开证据直接确认 Output Gap 正在改善，季度首 Energy 与 review 前最后窗口同现，候选无重大风险线索且未触发重比，可以演示：

```text
CTRL B=F G=O P=A R=PASS CP=QH X=-
```

它只是教学性格式与语义例子，不是 M13 或任何历史动作的原控制行。随后还应同回合紧邻提交当前合法候选。若仅知道菜单宣传会增长、实际进展无可比证据，P 应是 ?；若重比未完成，X 必须是 0 且不得提交。

### 什么才是“禁止隐藏答案”

**INTERPRETATION**：公开事件描述可以帮助判断具体后果；禁止的是把内部 ID、事后隐藏效果或推测阈值当成标准答案。比如“出现某故事标题就固定选 2”跳过了当前状态、合法选项和公开风险。公开反馈缺晋升条件时，应承认不知道，而不是从某一次升职月份倒推资格公式。

**FACT｜审计证据**：418 个标记形状文本与 203 次尝试无法提供可靠一一对应；缺回合 ID，不能认证同回合配对。CTRL 是可审计意图，实际审计表面仍有缺陷；打印更多标记不能解决这个缺口。

## 7. 覆盖复核与自测

I01–I28 已分别解释；I04 的三个读取对象、I08 的候选顺序与单次替代、I09 的重新 gate 和同回合紧邻动作、I25 的六字段均进一步展开。这个覆盖定义检查的是本章是否解释历史文字，不是 Agent 的行为通过率。

自测：看到 `R=RECONSIDER, X=1` 是否总应禁止动作？看到 CP=R 时是否说明风险审查 RECONSIDER？看到 P=A 是否就是推进模式？如果你读的是 exact-v6，三题都不能按后继版本的字面直觉作答。还要检查重比已经完成、候选是否换项并重新 gate、当前公开 terminal-risk 约束等条件。

参考分析：v6 允许有公开依据地在完成比较后保留原项；CP=R 指实际反馈后的基线重建；P=A 是 ADVANCING。相关记录仍不保证标记真对应那一次动作。下一章回到事实层，学习决定这些字段前究竟能确认什么。
