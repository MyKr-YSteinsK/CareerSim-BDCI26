# exact-v6｜版本讲解

> **FACT｜事实** 依据[Instruction](instruction.md)、三个 Skill、[SOURCE](SOURCE.md)、[DELTA](DELTA.md)、[v6 运行验证](../../project/runs/v6-run1-validation.md)和[最终证据审阅](../../project/FINAL_EVIDENCE_REVIEW.md)。教学分析标为 **INTERPRETATION｜解释**；无法确认的事实为 **UNKNOWN｜未知**。基本概念见 [v3c GUIDE](../01-v3c-zh-aligned-policy/GUIDE.md)。

## 1. 这个版本处在什么位置

**FACT**：`candidate-v6-auditable-control-loop` 的运行任务是 S06-24，精确身份后来用于 S10-23 最终比赛包。它是 Single Agent + 三个 Skill：Board、Planning、Risk；上一代表版本与 parent 均为 v5。

在七版本中，v6 把候选生成、风险门禁、动作记录与新观察串成可审计闭环，也是 final competition Candidate（最终比赛候选）。这里的 exact（精确）指固定历史 Instruction / Skill 身份，不是泛指所有 v6 后继版本。当前 main 的四 Skill v8a checkout（检出配置）与最终 exact-v6 ZIP 分别属于不同身份。

## 2. 这一版的核心结构

```text
Agent fresh observe
  → Board 扫公开事实
  → Planning 更新目标、进展、预算 → 生成合法候选
  → Risk gate；必要时比一个相关替代，换候选再 gate
  → Agent 输出紧邻动作的 CTRL → 同回合 take_action
  → fresh observe → 下一决策
```

箭头表示职责顺序／信息关系，不代表 Skill 之间直接 Python function call（函数调用）。Instruction 是 persistent kernel（常驻控制规则）：它管读取、编排和标记。三个 Skill 都不调用动作工具；Single Agent 把规则应用到一次具体决定。

**INTERPRETATION**：闭环的关键是每次改变状态后重新观察。季度 Energy 与 Main 可以共同规划，但计划不能授权在旧状态上连发后续动作。

## 3. Instruction 怎么约束 Agent

五行很短，但压缩了五类合同：

| 条款块 | FACT｜要求 | INTERPRETATION｜忽略后的问题 |
|---|---|---|
| 48 月与公开事实 | 仅本局 fresh public facts（新鲜公开事实），唯一动作提交者 | 跨局经验或局后知识可能被误当当时可用证据 |
| 启动／恢复读取 | 新局首动作前各读三份 Skill；Continue/context recovery 后观察、重读、重建再行动；正常上下文不逐步重读 | 已加载不意味着压缩后还记得规则；每步重读又可能重复消耗上下文 |
| 决策顺序 | Board→Planning→候选→Risk→有界重比→CTRL→同回合动作；状态改变后 fresh observe | 提前判断 cue 或复用旧 scan 会错配候选与状态 |
| 规划节奏与风险分工 | 每决策一个 Gap；季度首 Energy 联合规划 Energy+Main；半年 review 前最后窗口 reserve check；实际反馈后更新 Progress；Risk Budget 独立于候选 | 战略约束与具体候选风险是不同问题；不能由 Risk 接管目标 |
| CTRL 与禁止项 | 固定字段、合并并发 checkpoint；公开 horizon；禁隐藏阈值、权重和事件答案 | 有记录便于审查，但标记自身不能保证规则被执行 |

CTRL（控制标记）在本版是独立的动作前文本，**不进入 notes**，不能只输出它就结束回合。逐字段读法是：

- `B=F/?`：此次事实扫描是否确认新鲜；不明就 `?`。
- `G`：唯一 Primary Gap（主要差距）的短 key，缺证据用 `?`。
- `P=A/S/?`：**ADVANCING / STALLED / UNKNOWN（进展／停滞／未知）**，不是后续版本的 Advance/Stabilize 模式。
- `R=PASS/ALLOW/WARN/RECONSIDER/UNKNOWN`：候选风险门禁结果；PASS 是快速门禁无相关重大线索，ALLOW 是完整审查后可接受。
- `CP=N/Q/H/R/P/C/-`：新局、季度、半年 review 前、反馈后 reset、严格停滞诊断、上下文恢复、无完整 checkpoint。并发只合并一次，如 QH；字段 CP 的 R 与字段 R 的风险结果不同。
- `X=0/1/-`：替代比较未完成／已完成／无需比较。X=0 禁止动作；没有 RECONSIDER 用 `-`。

**FACT｜版本差异**：本版允许有证据地保留原候选，并记录 `R=RECONSIDER, X=1`；换候选则须重新 gate。不能套用 v8a 的“最终 R 必须非 RECONSIDER、RB 分支关闭”格式来改写历史规则。

## 4. 每个 Skill 分别负责什么

### structured-state-board｜公开事实层

[原文](skills/structured-state-board/SKILL.md)读取同局新观察、七项公开字段、正式反馈、警告与可比结果，提供 changed / relevant / unknown（变化／相关／未知）事实及有界快照。它不拥有 Gap、Progress、Risk Budget、review reset 或候选；Planning、Risk 消费事实作各自判断。它不提交、不创建持久 Memory（记忆），也不生成 CTRL。关键规则是：

- 每次 fresh public state 做 QUICK_SCAN，稳定信息不反复复述；B=F 只描述已完成的新鲜事实扫描。
- 新局、季度、实际 review／晋升、重大变化或恢复才替换完整快照，并发合并。
- recent_effects 最多两条；有故事、其他动作或来源混杂就 UNKNOWN，不将时间相邻等同因果。
- 恢复先确认相同游戏 session 和新状态，必要时最多五条公开日志恢复两条效果。

**反例**：Board 把一次没有 Output 增长直接标成 STALLED，或依据晋升旧基线算新职级的持续进展。这些判断属于 Planning，且需满足可比条件。

### rolling-planning｜目标与候选无关约束

[原文](skills/rolling-planning/SKILL.md)读取 Board、公开 Handbook、反馈、剩余时间与真实可达窗口；每决策维护一个 Gap、Progress、Risk Budget 和 Horizon（时间范围），完整 checkpoint 最多六字段，并给最多两条路径建议。它是唯一 strategy owner（战略负责人），不做具体候选 Risk gate，不调用工具、不猜分数公式。关键规则是：

- Risk Budget 为 AVAILABLE / TIGHT / UNKNOWN，由公开生存趋势决定，不靠隐藏阈值；TIGHT 只约束直接加重相应风险的候选。
- 季度首 Energy 联合比较 Energy 与 Main 的互补，每个状态改变后仍重扫；不编码固定组合。
- review／晋升／no-advance（未晋升）实际出现后废弃旧 Progress 比较，建立新 baseline（基线），不能从沉默推断结果。
- 同动作、同 Gap、两个相邻可比 checkpoint 都无目标进展才 STALLED；随后比较一个不同类型替代，不强制换。
- review 前最后窗口检查生存储备，不把 review 后的恢复当成当前保护；普通事件最多两候选一次。

**反例**：一次汇报未增 Output 就宣布整条成长路线失效，或把联合规划当成未来连续 Energy 的固定执行序列。

### risk-review｜先候选、后门禁

[原文](skills/risk-review/SKILL.md)读取已生成候选、公开后果、相关高信号线索与 Planning 的生存预算。它输出快速 PASS，或完整审查的 ALLOW/WARN/RECONSIDER/UNKNOWN 加一句理由；只影响候选是否需再比较，不拥有 Gap、阶段或预算，不提交。关键规则是：

- 每个 story、Energy、Main 动作前都 gate；日常负荷、普通摩擦或日常 CI 不单独触发完整审查。
- 线索收拢为保密授权、具有重大后果的隐瞒、关联新状态的健康负荷、重大可靠性事故；类别只促成检查，不提供答案。
- 已公开收紧的生存趋势下，不能把下一笔小损失孤立当软成本；有直接缓解项时不提交明显加重可避免终局风险的非必要候选。
- RECONSIDER 只比较一个相关合法替代；换候选重 gate；UNKNOWN 最多一次刷新，否则有界合法决策，避免死循环。

**反例**：因为别人更礼貌就否决成长候选，或看到 Risk Budget=TIGHT 便无差别禁止所有成长。应检查候选是否直接加重那个公开约束。

## 5. 相比上一代表版本改了什么

**FACT**：[DELTA](DELTA.md)记录 Instruction 改变，三个 Skill 都改文，没有新增或移除。四行 CONTROL_SCAN 收拢为候选门禁之后的 CTRL；阶段枚举不再必需，策略保留公开 Gap、Progress、预算与可兑现时间；review 后 reset 和状态改变后新观察更明确。

**FACT｜审查依据**：[S06-16](../../project/reviews/S06-16_FINAL_CONTROL_ARCHITECTURE_REVIEW.md)把旧合同的风险 cue 循环、旧 scan 风险和缺少遵循可观测性列为改进理由，同时建议删减阶段、关键词和重复输出。它提出的是控制合同假设，不是分数提升证明。

**INTERPRETATION**：从文本结构与后续证据看，可以解释为把“每步填分类”改成“每个候选通过有明确顺序的审查并留下记录”。真实执行能否匹配这个顺序，还要单独审。

## 6. 一个具体决策流程怎么走

**真实情境来源**：[v6 验证记录](../../project/runs/v6-run1-validation.md)的 M13 健康风险选择。报告确认发生一次真实 RECONSIDER，比较并选了较低负荷的合法替代，再对所选候选 gate；没有给出完整菜单、原候选编号或全部 Board 字段。

**INTERPRETATION｜按合同走查**：Board 提供当时公开健康信息；Planning 根据当前约束与 Gap 提名候选；Risk 检查它是否加重明确风险。满足三条件后只比一个相关替代；选择变化后重 gate，Agent 记录合法 CTRL 并提交；随后新观察才能更新效果。

**FACT｜审计边界**：该次标记在 transcript（文字轨迹）里重复。报告可确认重比和重新 gate 的行为，但不能据此认证每个 CTRL 与动作同回合、紧邻且唯一。未记录的 Gap、CP、X 精确值为 UNKNOWN；本走查不补造当时完整控制行，也不声称低负荷选择带来确定收益。

## 7. 真实运行证据

**Observed Run（观测运行结果）**：`RUN-0001 / S06-24 v6 Run #1`，session `7b59b85ad19b4597927cf50fc716f9ac`。

| 量化分 | 比赛局部得分 | 存活月份 | 评级 | 最终职级 | 两个独立分类 |
|---:|---:|---:|---|---|---|
| 75.29 | 52.70 | 48m | A | L6 | VALID_48M_COMPLETION；RUNTIME_ADHERENCE_FAIL |

这是 **Complete run（完整运行）／自然完整终局**；M49 是完成后的行政状态，不是 49 月成绩。公开晋升：M6 L1→L2、M12 L2→L3、M18 L3→L4、M36 L4→L5、M48 L5→L6。

**FACT｜遵循问题**：

- 半年 review 前要求的 H 触发遗漏；普通事件在无新公开证据时反复重开比较，M1、M48 均有案例。
- 两次 CurrentRoundCompressor（上下文压缩器）产生快照后，都没有按恢复要求重读三个 Skill。仅开局三次 read_file 不能证明后续遵循。
- 一次 Energy attempt（尝试）把多个选择写成 `choice=6,7,3`，因无效参数 JSON 被拒，未改变游戏状态。
- 418 个标记形状的文本出现不能当成 418 个动作审计记录；203 次尝试中有 202 次成功。扁平 transcript 缺可靠回合 ID，CTRL 配对、覆盖、重复与同回合 X 门禁无法认证。

同时，202 次成功状态改变后都在下一次成功动作前新 observe；Board 扫描反复出现。严格 STALLED 条件未建立，应记 **NOT_TRIGGERED（未触发）**，不能把无 P 标记写成遗漏。完整跑完不等于 Adherence（运行遵循）通过；一次高分也不等于稳定性能，分数差不是 Skill 因果收益。

## 8. 这个版本暴露出的限制

**FACT**：只有一个已接受的完整样本。CTRL 原文本表面不足以独立认证动作关联，重读／reserve trigger／有界比较也有实际失败。运行报告的本机 score_report 后来改变了 session 字段与时间，原因 UNKNOWN；事件和 Runner 输出独立绑定 session，未重写 raw（原始证据）。正式 raw FORENSIC_HOLD（取证保留）状态仍 UNKNOWN，不可解读为“无保留要求”。

**INTERPRETATION**：文字合同能规定闭环，却未形成机械强制执行。表现、遵循和审计完整性需要分别评价；不能用高分补掉遵循失败，也不能用遵循失败否认这局确实完成。

## 9. 为什么它值得保留在版本演化里

distinct design delta（独特设计变化）是 candidate-first 风险、公开反馈 reset、动作前 CTRL 与每步新观察组成的三 Skill 闭环。它同时是最终选择与真实遵循失败的双重案例。

**FACT｜最终选择边界**：[最终证据审阅](../../project/FINAL_EVIDENCE_REVIEW.md)记录选择依据为 `HIGHEST_OBSERVED_MATURE_THREE_SKILL_CEILING`（已观察成熟三 Skill 的最高位参考）。这不等于全部历史最高分：Candidate v1 有 76.04 的摘要反例，但 raw 不可用、完整指令身份有缺口；不能把它作为受控对照。冻结未再增加一次复验，官方上传与平台评测未执行。当前 v8a 文件不能代替最终 ZIP 身份，也未证明 exact-v6 全局最优、统计更优或隐藏测试迁移。

## 10. 下一版要看什么

继续读 [v7 GUIDE](../05-v7-global-trajectory-delivery/GUIDE.md)：

- 新增 Delivery 如何分开“活动”和“可验证结果”？
- CTRL 从独立文本移入 notes 后，历史格式有哪些变化？
- 长程目标、下一 review 窗口与当前候选怎样连接？
