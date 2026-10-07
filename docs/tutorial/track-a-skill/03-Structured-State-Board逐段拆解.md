# 03｜Structured State Board 逐段拆解

[统一入口与术语](../00-从这里开始.md) · [本 Track 阅读路线](01-从零理解Agent、Instruction与Skill.md)


本章按[historical SKILL.md](../../skill-evolution/04-v6-auditable-control-loop/skills/structured-state-board/SKILL.md)的实际结构阅读。B00–B05 是教材覆盖编号：标题加五个二级 section（章节），全部对应原文；metadata（元数据）另在 B00 解释。它们不是新增运行字段。

**FACT** 是原文规定；“为什么这样分工”是 **INTERPRETATION**；所有构造记录明确标为 **TEACHING EXAMPLE**。Board（状态板）名称容易让人以为它是完整数据库，其实 exact-v6 只规定当前对话内有界的公开事实工作记录。

## B00｜标题与 metadata：先辨认职责，再读正文

原文标题是“Structured State Board｜公开事实”。`name: structured-state-board` 是模块名称；description 说每次 fresh observe 后必须应用，整理当前 session 的公开事实、freshness（新鲜度）与可归因变化，不规划、不判风险、不提交动作。

**FACT**：标题和 name 用于辨认，不单独授权行为；description 概括使用时机和边界，完整细节仍在下面各段。看到 name 不等于已经读完整正文，也不等于完成一次扫描。

**INTERPRETATION**：用途描述像一个短入口：告诉 Agent 什么时候想到这个模块、哪些问题应交给它。它不能用“状态板”这个大词扩张到长期记忆、策略计划或隐藏状态估计。学习者应沿正文检查输入和输出责任，而不是凭名字猜功能。

## B01｜职责与边界：事实层究竟拥有什么

原文职责是整理当前游戏可核实的公开事实、来源、新鲜度和可直接比较的变化。它明确不拥有 Phase/Mode、Risk Budget、Primary Gap、Progress/STALLED、风险结论、review reset 或动作建议。

**FACT**：Board 可以记录“新观察 Health=4”“公开文本有健康警告”“正式反馈说明已晋升”；不能把这些事实直接写成“Risk Budget=TIGHT”“必须恢复”“策略 STALLED”。这些分别属于 Planning 的战略语义与 Risk 的候选审查。Board 不产生 CTRL；Agent 根据完成扫描等信息生成控制行。

**INTERPRETATION**：事实层若顺便 Planning，就可能把目标写进看似中立的记录，之后模块只能消费已经偏向某选项的材料。事实与策略分开，能让同一组公开信息支持重新比较：健康下降是否重要，要结合趋势与恢复窗口；哪条路径最好，还要结合一个 Gap。

### 输入与身份如何确认

Board 消费正常 Agent 循环已经取得的状态、公开结果、反馈与警告，不自己调用 observe。当前游戏的 `game_session_id` 用于判断是否同局，conversation ID（对话编号）不能代替它：一个对话延续，不代表游戏没换；新游戏也不能继承上一局板。

**TEACHING EXAMPLE｜教学示例，不是历史 Run 原始记录。** 对话仍叫“职业模拟”，旧板属于 session甲，当前 observe 属于 session乙。正确做法是丢弃旧工作事实，为乙按新观察重建；错误做法是保留甲的 Wealth、Gap 与 recent_effects，只把月份改成 1。就算两个游戏起始数值偶然相同，来源身份也已不同。

## B02｜QUICK_SCAN：每次新状态都看什么

原文在每次 fresh public state 后要求五项扫描：确认 session、月份与公开 review window（反馈窗口）；读七项公开当前值；核对最新正式反馈／晋升和警告；比较有依据的方向；检查前后变化是否混入事件、动作、过期或不明来源。

| 扫描对象 | FACT｜应整理的内容 | INTERPRETATION｜为什么要看 |
|---|---|---|
| game_session_id、月份、窗口 | 当前公开身份与时点，缺失不猜 | 确认这组材料适用于当前决定 |
| Health、Dignity、Network、Wealth、Level、Output、Skill | 七项可用当前公开值 | 避免只记目标收益而漏生存或资源事实 |
| 正式反馈、review、promotion、warning | 最新公开结果及来源 | 反馈可能改变战略比较的语境 |
| changed / relevant / unknown | 有可比来源的变化、当前相关项、未知项 | 不必每步重新复述全部稳定事实 |
| before/after 的归因条件 | 是否有污染、状态是否过期 | 观察到变化不等于知道变化由何造成 |

QUICK_SCAN（快速扫描）是事实整理活动，不要求每次输出完整快照。稳定项无需反复长篇讲述，但仍需确认最新观察；“不重复叙述”不能变成“不看新状态”。CTRL 的 B=F 只表示这次用本局 fresh state 完成扫描；不能确认则 B=?，不是看起来熟悉就 F。

### 正确事实记录是什么样

**TEACHING EXAMPLE｜教学示例，不是历史 Run 原始记录。** 以下是教学记录样式，不是 v6 冻结的完整输出 schema（格式合同）：

```text
session: 甲（由本次公开 observe 确认）
month: M7
current: Health=4, Level=L2, Output=10（来源：本次 observe）
changed: Health 5→4（两次同局可比公开观察）
warning: 当前公开文本提示健康负荷加重
recent_effect: UNKNOWN（期间还有另一故事结算，无法单独归因）
unknown: 下一恢复机会是否实际可达
```

这份记录没有说“必须休息”或“就是刚才那个动作扣了 1”。它把公开值、方向、警告与归因未知分开。其他四项公开状态也应实际扫描；例中仅展示讨论所需片段，不能把省略片段当“从不看其他字段”的政策。

**错误例子**：把菜单写“预计增长”当成已确认增长，把“健康下行”直接写为危险概率，或把扫描完成解释成风险审查通过。它们分别混淆宣传与结果、公开方向与隐藏估计、事实整理与候选判断。

## B03｜有界事实快照：什么时候完整替换

原文的完整快照触发是：新局；当季首次 Energy planning point（资源规划点）；实际观察到正式反馈／晋升；可能改变事实判断的重大新公开状态变化；上下文恢复。并发触发合并一份，完整快照只替换当前事实，不积累 transcript（完整文字轨迹）。

**FACT**：Planning 的派生标签变化不是 Board trigger（触发条件）。Board 记录实际反馈与当前值，Planning 才处理 review reset；不能因为 Planning 改 Gap，又让 Board 触发新 Planning，递归展开多个 checkpoint。

**INTERPRETATION**：快速扫描负责每步及时使用新事实；完整快照负责在真正重要的交接点形成可恢复材料。两种频率分开，能避免“每一步都抄整局状态”和“只在开局记一次”两个问题。它不是无条件不更新，也不是保存所有历史。

### recent_effects 为什么最多两条

原文只留最多两组同局、来源明确、无中间事件／其他动作污染的公开 before/after。若不能直接归因，就 UNKNOWN 或省略。这个上限约束工作记录体量，不证明过去只发生两次动作，也不把其余历史判为无价值。

**TEACHING EXAMPLE｜教学示例，不是历史 Run 原始记录。** 一项公开动作直接针对 Output，两次紧邻观察 10→12，中间无 review、晋升、工资、故事或其他动作混杂。可以记这组可比变化与已确认动作来源，供 Planning 判断相关进展。若这两个观察之间还结算绩效奖金并进入新月，即使 Output 仍增加，也应将具体归因记 UNKNOWN；不能只因排在动作后就归给动作。

这里的 correlation（相关）是两个事件一起出现或相邻；causation（因果）则是一个导致另一个。**INTERPRETATION**：有序工具记录和干净前后比较能支持局部效果记录，但整局分数和晋升还会受多个路径影响。Board 记录局部证据，不能把一次干净增长称为整条策略成功。

### review / promotion 要保留什么

原文要求保留最新正式反馈、review 或晋升结果及公开来源、月份和新鲜度。Board 记录新结果，不替 Planning决定“这次没有晋升所以停滞”。Level change（职级改变）后，旧事实仍可作为历史事实，但旧 Progress comparison（进展比较）的语境可能失效；Planning 必须重建基线。

**TEACHING EXAMPLE｜教学示例，不是历史 Run 原始记录。** M9 在 L2 的目标是根据旧反馈改善交付；M12 观察到 L3 晋升与新反馈。错误板写“已晋升但继续保留 L2 的 STALLED”；正确板记录当前 Level、正式结果和来源，把战略判断交给 Planning。不能说“L2 Output=10、L3 Output=11，所以原路必然有效”，因为正式反馈与职级变化都改变了比较条件。

## B04｜Context recovery：先确认身份，再恢复事实

原文顺序是同一 session 确认→fresh public state→必要时最多五条同局公开日志→最多两条可直接确认效果。fresh state 优先于日志，失配、来源不清、过期时丢弃旧工作事实，未知留 UNKNOWN。

**FACT**：不能读数据库、隐藏字段、其他对局或本机取证材料，也不创建文件型 durable Memory（持久记忆）。这不是安装或存储教程；读取怎样实现属于 Track B｜System / Runtime，将在后续章节解释。

**TEACHING EXAMPLE｜教学示例，不是历史 Run 原始记录。** 恢复后新观察确认 M15/L3，旧摘要只说“已做成长动作”，没有选项或前后状态。Board 可以恢复当前公开 Level 与七项值；若近期效果对 Planning 确有需要，再在允许的少量同局公开记录里查证。找不到干净依据便 recent_effects=UNKNOWN，不为了填齐两条而想象动作收益。

**INTERPRETATION**：UNKNOWN 比猜测好，是因为它保留“缺了哪条证据”的信息。猜测一旦包装成事实，Planning 可能判成 ADVANCING 或 STALLED，Risk 又可能据此认为预算安全，错误就会跨职责传递。未知不自动要求停住全部任务；应按正常流程补足必要公开信息，或在仍未知时进行有边界的判断。

**反例**：为了恢复一次效果，回放全局历史找“类似故事标准答案”，或把别局经验当作当前资源值。即使得到一个看起来合理的解释，来源仍不符合历史合同。

## B05｜权限：状态板是消费者，不是调用者

原文 `Can Submit Action: No` 禁止 Board 调 new_game、observe、take_action。它只消费正常流程已取得的状态与结果；若需要新鲜事实，回正常 Agent 循环取得，不凭空补造。功能应用不要求每步读完整文件；上下文规则无法恢复时再按 Instruction 与必要规则重读。

**INTERPRETATION**：这里的权限边界使事实缺口和外部执行责任有明确交接。Board 可以说“来源无法确认”；Agent 处理合法读取；Planning 不把未知预算假装可用；Risk 处理当前候选的相关未知。不要为了让 Board 看起来独立，把它改成另一个会自行操作环境的 Agent。

## 真实 Run 是否有相应证据

**FACT**：[v6 记录](../../project/runs/v6-run1-validation.md)确认 Board 摘要／扫描在整局反复出现，不能说它只在开局运行。M6 公开 Health 6→5→4 伴警告，后来恢复至 6 且警告清除；这些公开事实进入了预算判断。记录也确认所有成功状态改变后有新观察。

但“有摘要”不能证明每个事实来源、方向比较或 recent_effect 归因都正确；CTRL 配对也无法独立认证。Board 局部证据不替代整体遵循结论，v6 仍是 RUNTIME_ADHERENCE_FAIL。

## 自测：只写 Board 能说的话

给你四句话：“当前 Level=L3”；“旧策略已经停滞”；“刚才动作之后 Output 增加，但期间有正式反馈”；“下季度固定恢复”。哪些可留在 Board？

参考分析：第一句有新公开来源就可记；第三句可记录已观察增加与混杂，具体动作归因 UNKNOWN。第二句是 Planning 判断，第四句是动作政策；Board 都不拥有。若说不清某句是事实还是判断，先标出其来源和承担职责，再改写。

B00 为标题／元数据，B01–B05 为五个二级 section，均已解释。进入下一章时，保留这条接口：Board 提供可靠材料，Planning 才给材料以目标与进展的意义。
