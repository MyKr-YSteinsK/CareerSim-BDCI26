# v8a｜版本讲解

> **FACT｜事实** 依据[Instruction](instruction.md)、四个 Skill、[SOURCE](SOURCE.md)、[DELTA](DELTA.md)、[样本 1](../../project/runs/v8a-full-horizon-sample1.md)、[样本 2](../../project/runs/v8a-full-horizon-sample2.md)与[最终证据审阅](../../project/FINAL_EVIDENCE_REVIEW.md)。教学分析标为 **INTERPRETATION｜解释**，证据不足为 **UNKNOWN｜未知**。基础概念见 [v3c GUIDE](../01-v3c-zh-aligned-policy/GUIDE.md)。

## 1. 这个版本处在什么位置

**FACT**：`candidate-v8a-v7o-donor-core-transplant` 对应 S09-10 与 S09-RUN07/RUN08，是历史四 Skill donor-core transplant（核心策略移植）配置。上一代表版本是 v7c，实际 parent 是 v7z；不能把跳过的中间演化当作一次改动。

它在七版本中展示晋升优先、最小必要保护和更明确的执行门禁，并有两个相同行为身份的完整周期样本。名称中的 donor 不证明移植完全复现其运行效果；它也不是 exact-v6 replication（精确复验）或最终比赛提交包。

## 2. 这一版的核心结构

```text
同局 fresh observe → Board → Delivery → Planning → final Risk
  → 执行器设 READY → PREFLIGHT=PASS → 单次 take_action
  → OBSERVE_REQUIRED → 下一次同局 fresh observe
失败／身份不符／门禁未闭合 → BLOCKED → 有界恢复
```

箭头表示职责顺序与信息关系，不代表 Skill 间直接 Python 函数调用。Executor（执行器）在这里指唯一 Agent 的执行职责；READY 不是任一 Skill 能自行宣布的状态。规则写在文本中，不应把示意图解读成已证明代码强制执行。

## 3. Instruction 怎么约束 Agent

较长指令按标题块读：

| 块 | FACT｜要求 | INTERPRETATION｜要防止的问题 |
|---|---|---|
| GLOBAL EVIDENCE FIREWALL | 只用当前参与者可见证据；隐藏、内部或 public 身份不明字段不得引用、比较、记忆或推理，`EXCLUDE_FROM_STRATEGY until verified public` | 工具输出出现字段不等于它已获准用于策略 |
| OWNERSHIP / CRITICAL KERNEL | Board 事实；Delivery 生命周期；Planning 目标与排序；Risk 最终候选门禁；默认 MODE=A，只有 fresh material binding threat 才 S | 把软成本当危机，或把模块变成第二策略负责人 |
| STARTUP AND FLOW | 首动作前顺序读 Board、Delivery、Planning、Risk；常规同上下文不逐步重读 | 恢复规则与日常功能应用需分开 |
| WHOLE-GAME EXECUTION | 游戏仍 active 时持续工具循环；DECISION_CLOSED 只关闭当前选择，只有 structured game.ended 或不可恢复失败才结束 | 局部行动、晋升或记录输出不能冒充整局完成 |
| CONTROL STATE | READY 需新观察、四模块处理完成；动作成功消耗 READY 转 OBSERVE_REQUIRED；回执不含公开状态 | 成功回执不能授权旧候选的下一动作 |
| ACTION PREFLIGHT | 同局、新鲜、单个合法整数、同一观察的模块结果与合法标记；最终 R 非 RECONSIDER，RB 为 NONE/DONE | 标记正确不等于其他前置条件已满足 |
| QUARTERLY ENERGY REPLAN | 一次一个 Energy；新观察后更新响应并新做 Planning，丢弃旧后续动作意图 | 固定批次会忽略实际 NO_GAIN 或新约束 |
| CONTEXT RECOVERY | 可见 resume/compaction/recovery signal 才进入恢复；同局观察、重读四份、重建事实／交付／计划 | 不能声称检测到 host 未暴露的压缩；RECOVERY_READY 本身不授权动作 |

CTRL 的 `P=A/S/?` 在本版是 Advance/Stabilize（推进／稳定模式），不同于 exact-v6 的进展／停滞。`R` 必须记录最终候选的 Risk 结果；`RB=NONE` 无重比分支，`DONE` 表示一次分支完成且最终 Risk 非 RECONSIDER，`BLOCKED` 表示未闭合并禁止提交。旧 X 格式和保留过程 R 的写法不能套用。

notes 开头依次一个 CTRL、一个 DL（交付标记）。DL 的 i 是当前项 ID，n 是最多三个 active 的数量，focus 是阶段，evidence 是验证状态，checkpoint 是有公开依据的接近程度，recognition 是结果与认可的明确关联。它们记录证据，不决定排名，也不替代 CONTROL_STATE。

## 4. 每个 Skill 分别负责什么

### structured-state-board｜当前职级响应事实

[原文](skills/structured-state-board/SKILL.md)读取最新 observe、紧邻动作公开结果、上一同局 Board 和必要少量公开日志，输出 SESSION、STATE、TENURE、REVIEW、PROGRESSION_RESPONSE、STICKY、EFFECTS、UNKNOWN。它只管事实，Planning 排序、Risk gate；不推阈值、不提交。关键规则是：

- STATE 从参与者可见 status 直接抄值和精度，缺失／身份不明用 UNKNOWN；不能用工资或回执自行算当前数值。
- STICKY（未解除重大约束）需公开重大证据；低绩效、未晋升或一次下降不单独成立；急性危险不能因数值看似尚可而忽略。
- S/N/O 各自 GAIN/NO_GAIN/UNKNOWN 只有紧邻动作与新观察、无 review/晋升等混杂才更新；Level/session 改变重置。
- NO_GAIN 只是已测局部响应，不是 cap（上限）、资格或隐藏公式；EFFECTS 最多两条。

**反例**：某次 Skill 未涨便宣称该 Level 所有成长已封顶，或把低绩效记成永久危机。

### delivery-progress｜带身份的工作项

[原文](skills/delivery-progress/SKILL.md)读取 Board、同局承诺、checkpoint、公开结果与有效 REVIEW_PLAN，输出完整有界 Delivery state 和 DL 标记。它不等待 Planning 重算才能维护已有项目，也不发明目标、排序、判风险或提交。关键规则是：

- D1、D2 等 local_id（局内编号）同局不复用；恢复无法确认 ID/cursor 用 UNKNOWN，不猜。
- 声称完成但未验证与公开验证结果分开；成功工具回执只证明执行，不证明职业交付。
- 最多三条 active、一条相关 closed；closed 不计 n，也不能做 action-note focus；零活动项有固定 NONE/NA 标记。
- 普通表扬／晋升不单独验证成果；recognition=1 需公开明确关联，NEAR 也不能用臆造数字倒计时。

**反例**：为了减少 n 删除真实活动项，或工具 success 后立即把项目写为 PUBLICLY_VERIFIED。

### rolling-planning｜晋升优先、必要时稳定

[原文](skills/rolling-planning/SKILL.md)读取 fresh Board、Delivery、当前公开事件与合法选项、正式反馈和 Handbook，输出 `PLAN`（Gap、MODE、RECOVERY、checkpoint）及唯一 `CANDIDATE`（合法整数和短理由）。它唯一拥有目标和排名；Board 不排、Delivery 不选、Risk 不规划，它自己也不提交。关键规则是：

- 首次正式 review 前 Gap 可 UNKNOWN，推进广义 Skill/Network/Output 与可见交付；反馈后锚定公开缺口，普通故事不随意改 Gap。
- 每次新观察从 A 重新判断；只在尚未解除的重大公开生存／资源约束下 S，最小必要保护后回 A，不为补满资源延长。
- 首评前结果兑现先验需已有高价值承诺／真实结果基础与合法验证行动；仅报告式菜单名不够，已验证成果不重复包装。
- 消费 Board 的局部 NO_GAIN，只折价已测 family（动作族）；UNKNOWN、其他维度和 ownership（承担责任）价值仍开放，有响应替代时不立即重复。
- 一个 fresh observe 只做一次 Planning pass，最多两个真正竞争候选；Risk 重比最多一个相关替代，再取得最终 gate；执行器独占 READY。

**反例**：Wealth 低就永久低调，或把首评前先验写成“每次 review 前必选汇报”。

### risk-review｜最终候选门禁

[原文](skills/risk-review/SKILL.md)读取 Planning 的最终候选、新鲜 Board、当前 MODE 与参与者可见后果，严格输出 `RISK` 与 `REASON`。普通软成本无重大证据时 PASS；完整审查只输出 ALLOW/WARN/RECONSIDER/UNKNOWN。它不改变战略目标、不宣告 READY、不提交。关键规则是：

- 急性健康／安全、工作连续性、信任、合规或明确支付压力等重大公开风险才完整审查；低 Wealth 不一律否决恢复绩效／收入的动作。
- RECONSIDER 需明确重大风险、候选未处理且存在直接合法替代；只比该替代一次，选后再 gate；最终仍 RECONSIDER 或分支未闭合就 RB=BLOCKED，不能行动。
- UNKNOWN 最多一次正常 fresh observe/rebuild，之后有界合法决策；禁止隐藏风险数值与概率猜测。

**反例**：继续保留旧版 `R=RECONSIDER, X=1` 就提交，或把 Planning 的 RECOVERY=RISK（战略恢复方向）自动当成候选须重选。

## 5. 相比上一代表版本改了什么

**FACT**：[DELTA](DELTA.md)记录 Instruction 和四个保留 Skill 全改文，未增删。原文可见更明确的 READY/preflight、CTRL RB、DL 身份、whole-game 循环、局部成长响应与 A/S 模式；v7c 的详细层级结构不再照搬。

**INTERPRETATION**：从文本结构与后续证据看，可以解释为用更集中的晋升策略与执行状态规则处理旧意图、局部无收益和恢复衔接。名称或文本重复关键规则不能证明 donor fidelity（移植忠实度）或更强遵循；完整历史动机及中间改动效果为 UNKNOWN。

## 6. 一个具体决策流程怎么走

**真实情境来源**：[样本 2](../../project/runs/v8a-full-horizon-sample2.md)记录 M15 公开 Health 为 3，随后有公开恢复。这是当局数值，不是“≤3 必须恢复”的阈值；报告未给该窗口完整菜单和各模块输出。

**INTERPRETATION｜按合同走查**：Board 抄当前值与已知警告，混杂效果 UNKNOWN；Delivery 维护公开可恢复的项目，不能因健康恢复就假设交付暂停或完成；Planning 需额外公开证据才设 binding constraint 和 MODE=S，仅一个数字不足。Risk 审最终候选；执行器完成 READY 与 preflight 后一次提交，成功回执后仍必须 observe，才可重新判断约束是否解除并选择下一动作。

**FACT｜边界**：可确认的是“公开健康低值后有恢复”和全局 action→observe 顺序；该窗口 Gap、MODE、DL、Risk 理由及反事实效果均为 UNKNOWN。走查解释应当如何使用已知事实，不冒充完整逐步回放。

## 7. 真实运行证据

两个 **Observed Run（观测运行结果）** 必须并列：

| 身份 | 量化分 / 局部得分 | 月份 / 评级 / 职级 | 公开晋升月份 | 分类 |
|---|---|---|---|---|
| RUN-0004 / S09-RUN07，session 258f135bc8e0459482ad7cc3be04c1ac | 72.65 / 50.86 | 48m / A / L5 | M6、M12、M24、M42 | VALID_48M_COMPLETION |
| RUN-0002 / S09-RUN08，session ae83da7c19c64591951cbb9c186e2f52 | 59.00 / 41.30 | 48m / C / L4 | M12、M18、M36 | VALID_48M_COMPLETION |

两局均 **Complete run／自然完整终局**，自然结构化 M49 结束；不是 partial run（部分运行）或 gameplay technical failure（对局技术失败）。第一局 203/203、第二局 205/205 成功动作后都有 fresh observe。它们共享冻结行为身份，运行 base commit 不同不代表策略改版。

**FACT｜审计限制**：两局 action notes 都发现数值化 HiddenRisk 引用，违反证据防火墙；这里只陈述违规类型，不把受限数值带入教学决策。样本 1 的 CTRL/DL 直接相邻被当前 parser（解析器）拒收，accepted coverage 为 0/203；指令未明文禁止相邻，属于未解决的格式合同边界，不等于所有交付语义都失败。样本 2 用空格分隔，205/205 被接受，但格式通过不证明 lifecycle 语义通过。

样本 1 M36 连续风险应对缺独立新警告依据仍待审；两局压缩／重读、execution boundaries（执行边界）等 UNKNOWN，样本 2 RB 分支使用未独立认证。没有统一 Adherence pass（遵循通过）结论，不能由完整跑完或 MODE 标记数量补证。

## 8. 这个版本暴露出的限制

**FACT**：两条晋升路径、最终职级和分数明显不同；两个样本仅展示 single-run uncertainty（单局不确定性），不能建立概率分布、稳定成绩、因果收益或移植复现结论。服务 wrapper 在清理后有非零退出记录，不能据此把已经完成的对局改成技术失败。

**INTERPRETATION**：更细的标记与状态门禁增强了合同可读性，却仍依赖实际执行和审计工具的一致解释。格式解析、标记语义、信息边界、行为收益应分别举证。两份 raw 均 FORENSIC_HOLD=ACTIVE（取证保留有效），未解决问题不能靠摘要或 hash 替代。

## 9. 为什么它值得保留在版本演化里

distinct design delta（独特设计变化）是局部响应、带身份的交付记录、最终风险结果与单次执行状态。它让学习者看到完整周期、正确调用顺序、标记可解析与合规策略证据是不同验收面；两个样本也防止只讲 72.65 的好结果。

## 10. 下一版要看什么

返回[版本索引](../00-版本索引.md)：

- 对照 v6 的进展 P／X 与 v8a 的模式 P／RB，观察合同如何改变。
- 比较 v7 的稀疏 Delivery 与 v8a 的每观察完整有界输出，区分更新与输出。
- 回读 [exact-v6 GUIDE](../04-v6-auditable-control-loop/GUIDE.md)：final competition package = exact-v6，当前 v8a checkout 不是最终 ZIP；最终选择也不等于历史最高分或已证明稳定最优。
