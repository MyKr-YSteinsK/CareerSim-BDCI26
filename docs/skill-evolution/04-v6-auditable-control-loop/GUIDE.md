# exact-v6｜版本讲解

> **FACT｜事实** 依据[Instruction](instruction.md)、三个 Skill、[SOURCE](SOURCE.md)、[DELTA](DELTA.md)、[v6 运行验证](../../project/runs/v6-run1-validation.md)和[最终证据审阅](../../project/FINAL_EVIDENCE_REVIEW.md)。教学分析标为 **INTERPRETATION｜解释**；无法确认的事实为 **UNKNOWN｜未知**。先读 [v5 GUIDE](../03-v5-evidence-driven-phase-policy/GUIDE.md) 理解上一版，再看本版差异；入门概念见 [v3c GUIDE](../01-v3c-zh-aligned-policy/GUIDE.md)，基础职责与闭环详细教学见 [Track A](../../tutorial/track-a-skill/01-从零理解Agent、Instruction与Skill.md)。

## 1. 这个版本处在什么位置

**FACT**：`candidate-v6-auditable-control-loop` 的运行任务是 S06-24，精确身份后来用于 S10-23 最终比赛包。它是 Single Agent + 三个 Skill：Board、Planning、Risk；上一代表版本与 parent 均为 v5。

在七版本中，v6 把候选生成、风险门禁、动作记录与新观察串成可审计闭环，也是 final competition Candidate（最终比赛候选）。这里的 exact（精确）指固定历史 Instruction / Skill 身份，不是泛指所有 v6 后继版本。当前 main 的四 Skill v8a checkout（检出配置）与最终 exact-v6 ZIP 分别属于不同身份。

## 2. 这一版的核心结构

**FACT｜版本定位**：仍是 Board、Planning、Risk 三个 Skill，数量不变但正文均改变；[DELTA](DELTA.md) 记录 Instruction 由上一版十行调整为本版五行。改动集中在 candidate-first（先产生候选）的风险顺序、公开反馈 reset、动作前 CTRL 和改变状态后的新观察。

**INTERPRETATION｜解释**：成熟之处是把职责接口与可审计记录连在一起，形成明确控制合同；它没有实现机械强制执行。完整闭环图读 [A06](../../tutorial/track-a-skill/06-三Skill协同与一次Action闭环.md)，运行路径读 [Track B](../../tutorial/track-b-system-runtime/01-比赛官方到底提供了什么.md)，本 GUIDE 只解释这一历史版本的变化。

## 3. Instruction 怎么约束 Agent

**FACT｜版本差异**：v5 的四行 CONTROL_SCAN 收拢成风险门之后、动作之前的 CTRL，**独立文本且不进入 notes**。本版 `P=A/S/?` 指 ADVANCING / STALLED / UNKNOWN（进展/停滞/未知），不能套成后续 Advance/Stabilize 模式；`X=0` 禁止动作，无 RECONSIDER 时用 `-`。

有证据可保留原候选并记录 `R=RECONSIDER, X=1`；换候选必须重新 gate。v8a 的最终 R 非 RECONSIDER / RB 关闭格式不能倒写本版。完整字段、checkpoint 与恢复条款读 [A02](../../tutorial/track-a-skill/02-exact-v6-Instruction逐句拆解.md)，精确历史内容仍以 [Instruction 原件](instruction.md) 为准。

## 4. 每个 Skill 分别负责什么

### structured-state-board｜公开事实层

[本版原件](skills/structured-state-board/SKILL.md) 保留 QUICK_SCAN 与有界快照，明确 changed / relevant / unknown，并让 recent_effects 受可比性和混杂限制。它仍不拥有 Gap、Progress、预算或候选。

**INTERPRETATION｜解释**：对 v5→v6 的控制整合，Board 的接口价值是交付事实，避免在风险 cue 或候选讨论里反复制造新 scan。扫描与快照的完整机制见 [A03](../../tutorial/track-a-skill/03-Structured-State-Board逐段拆解.md)。

### rolling-planning｜目标与候选无关约束

[本版原件](skills/rolling-planning/SKILL.md) 仍独占策略，维护一个 Gap、Progress、Risk Budget 与 Horizon；相较旧阶段分类，强化实际 review/晋升反馈后 reset 和候选无关的生存预算。季度 Energy+Main 是联合规划，改变状态后仍需重扫，不能变成固定连发序列。

**INTERPRETATION｜解释**：重点是减少重复分类，让反馈真正改变比较基线。Progress/STALLED 的可比条件、季度与半年窗口详解读 [A04](../../tutorial/track-a-skill/04-Rolling-Planning逐段拆解.md)。

### risk-review｜先候选、后门禁

[本版原件](skills/risk-review/SKILL.md) 消费已经生成的候选、公开后果、相关重大线索和生存预算；快速 PASS 与完整 gate 分开。RECONSIDER 只比较一个相关合法替代，换候选再 gate，不接管 Planning 的目标。

**INTERPRETATION｜解释**：candidate-first 顺序回应了旧合同中风险 cue 循环的问题；TIGHT 仍是直接相关风险约束，不能无差别否决成长。完整风险语义与反例见 [A05](../../tutorial/track-a-skill/05-Risk-Review逐段拆解.md)。

## 5. 相比上一代表版本改了什么

**FACT**：[DELTA](DELTA.md)记录 Instruction 改变，三个 Skill 都改文，没有新增或移除。四行 CONTROL_SCAN 收拢为候选门禁之后的 CTRL；阶段枚举不再必需，策略保留公开 Gap、Progress、预算与可兑现时间；review 后 reset 和状态改变后新观察更明确。

**FACT｜审查依据**：[S06-16](../../project/reviews/S06-16_FINAL_CONTROL_ARCHITECTURE_REVIEW.md)把旧合同的风险 cue 循环、旧 scan 风险和缺少遵循可观测性列为改进理由，同时建议删减阶段、关键词和重复输出。它提出的是控制合同假设，不是分数提升证明。

**INTERPRETATION**：从文本结构与后续证据看，可以解释为把“每步填分类”改成“每个候选通过有明确顺序的审查并留下记录”。真实执行能否匹配这个顺序，还要单独审。

## 6. 一个具体决策流程怎么走

**FACT｜事实**：[v6 验证](../../project/runs/v6-run1-validation.md) 的 M13 健康情境确认一次 RECONSIDER、选择较低负荷合法替代并重新 gate；没有完整菜单、原编号或全部 Board 字段。重复 transcript 标记不足以认证唯一紧邻配对。

**UNKNOWN｜当前来源不足**：当时 Gap、CP、X 的精确值及收益因果。完整合同走查见 [A06](../../tutorial/track-a-skill/06-三Skill协同与一次Action闭环.md)，本版案例只用于理解候选→风险→替代→再 gate，不补造整条 CTRL。

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

**FACT**：只有一个接受的完整样本；配对、重读、reserve trigger 和有界比较仍有缺口。本机 score_report 后来改了 session 字段/时间，原因 UNKNOWN；独立事件绑定 session，raw 未重写。正式 raw FORENSIC_HOLD 状态为 UNKNOWN，不能当无保留要求。

**INTERPRETATION**：设计合同、真实遵循和完整结果分开评价；75.29 与 RUNTIME_ADHERENCE_FAIL 同时保留。调查方法读 [D08](../../tutorial/track-d-project-method/08-Forensics、失败实验与负证据.md)，不能因高分遮盖失败或反过来否定完整运行。

## 9. 为什么它值得保留在版本演化里

本版把 candidate-first 风险、公开反馈 reset、动作前 CTRL 与每步新观察组合成成熟三 Skill 控制合同，同时保留真实遵循失败。它值得保留为“设计身份与执行事实分别可审”的版本案例。

**FACT｜最终选择边界**：[最终证据审阅](../../project/FINAL_EVIDENCE_REVIEW.md) 记录 `HIGHEST_OBSERVED_MATURE_THREE_SKILL_CEILING`。这不是全部历史最高分或统计最优；选择理由及 v1/v8a 对照集中在 [D11](../../tutorial/track-d-project-method/11-为什么最终选择exact-v6而不是v1或v8a.md)，精确交付字段集中在 [最终报告 04](../../final-report/04-最终方案、候选选择与工程交付.md)。官方上传与平台评测未执行，hidden-test transfer 未证明。

## 10. 下一版要看什么

继续读 [v7 GUIDE](../05-v7-global-trajectory-delivery/GUIDE.md)：

- 新增 Delivery 如何分开“活动”和“可验证结果”？
- CTRL 从独立文本移入 notes 后，历史格式有哪些变化？
- 长程目标、下一 review 窗口与当前候选怎样连接？
