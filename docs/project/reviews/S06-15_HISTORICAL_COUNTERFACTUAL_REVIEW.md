# S06-15｜历史真实局反事实审查与 48 个月阶段策略校准

## 结论与边界

- Review status: `COMPLETE_FOR_MAIN_REVIEW`。
- Base: `main@bef71109a0cfea6a1223792a819f080e66b20f8a`；本次仅新增本审查文档。
- Current candidate at base: `candidate-v5-evidence-driven-phase-policy`；本任务未修改候选。
- 目的：将可追溯真实局整理为阶段/状态条件候选控制器，不重做 S06-11 至 S06-14 的专题分析。
- 结论：证据支持进一步审查**状态驱动的轻量 regime overlay**，尤其是 material-risk 约束执行、正式 review 后重置 Primary Gap、以及对可比较 observed progress 作停滞诊断；不支持固定季度 action package、promotion threshold、事件答案表或单局因果结论。
- 当前四阶段（FOUNDATION / PROMOTION / COMPOUNDING / FINAL_SPRINT）适合作为宽泛规划语言，但单独不足以表达 survival constraint、review reset 和 plateau。建议把少数公开状态触发的临时 mode 作为候选叠加，而不是扩成第五 Skill 或另一套持久状态系统。
- `gameplay effectiveness = NOT_PROVEN`；`stable quantitative 80+ = NOT_PROVEN`；本审查没有改变 Game Gate 授权。
- 本文所有反事实均为“若当时按公开证据执行某程序，可能改变决策质量”的候选，不声称改变动作必然改变分数或生存期。

证据标签：`DEV_CONFIRMED` = 冻结公开 Dev 机制；`RUN_OBSERVED` = 可追溯运行记录；`MULTIRUN_OBSERVED` = 多局重复观察但非因果；`DERIVED_DEV_ANALYSIS` = 公开 Dev 的确定性派生分析；`COUNTERFACTUAL_HYPOTHESIS` = 当时公开信息下值得比较的策略原则，不代表 alternative 更优；`HYPOTHESIS` = 待未来独立验证；`UNKNOWN` = 记录不足；`DO_NOT_ENCODE` = 不得转成运行时规则。

## 1. Evidence Coverage｜证据覆盖

只使用仓库可追溯的压缩结果、已提交轨迹/矩阵与现有专题审查： [RUN_HISTORY](../RUN_HISTORY.md)、[STRATEGY_EVIDENCE](../STRATEGY_EVIDENCE.md)、[S06-11](S06-11_SURVIVAL_REVIEW.md)、[S06-12](S06-12_PROMOTION_PERFORMANCE_REVIEW.md)、[S06-13](S06-13_QUARTERLY_ACTION_REVIEW.md)、[S06-14](S06-14_EVENT_PATTERN_REVIEW.md)、[v4 forensic](../runs/v4-run1-health-forensic.md)。S04 原始 transcript/events 与 S06 Run #1 本机 raw 不在仓库可恢复范围；没有重建 raw，也没有重跑。SCORE-01 月度轨迹虽在 Git 历史中，但本审查沿用已审核的轨迹结构与 S06-13 提取结果。所有分数和终局是观察值，不是动作效果估计。

| Run | 身份 / 可追溯来源 | 观察结果 | 覆盖与限制 |
|---|---|---|---|
| S01 minimal baseline | `experiments/S01-03-baseline/RESULT.md`、`score_report.json`；历史提交 `031d97e56e0ce305a487b4bc293c7abde58cfdf0` | 26.95 / 18.86；19 月；E | 最小/近 no-op 对照；没有足以还原季度状态或终局原因的月度轨迹。 |
| SCORE-01 | game `8ffa91ac75e143cfb68b015feb4f40e4`；trajectory blob `0330ef9c95ea13b285a8fcfcf1b4c2c6e80ff65a`，历史提交 `7a055dea76580117ca74cddb49bb04efcf605eb1` | 33.06 / 23.14；24 月；D | 98 条 timeline rows、M1–M23 状态、7 个季度决策；终止原因未知。不同候选身份未知。 |
| Candidate v1 Run #1 | game `2224f5df228544e699b10f897d333d4b`；trajectory blob `a9ca5d759b05dd0c9b3974c9a1398a3ca3990343`，历史提交 `66ec4af1e9a2a28da57c6cb8d409a6a38f87ae01` | 76.04 / 53.23；48 月；A | 完整月/季度摘要，16/16 Main action 为 Key project；仅 3 个显式 Planning checkpoint。单局。 |
| Candidate v1 Run #2 | game `7df157117cf14917bdc42d83fb7ac7d2`；trajectory blob `85129980c0591f0ad4d4bee113562bc51116d16d`，同上历史提交 | 35.31 / 24.72；25 月；D | 有里程碑与季度 Energy 摘要，缺 M18 状态、若干 review/危机时序与完整季度状态。 |
| S06 Run #1 | `experiments/S06-01-adaptive-controller-static/RESULT.md`；历史提交 `c4dbe0ebc4e27aafc22c94050c69547113cdc8eb` | 53.83 / 37.68；48 月；C | Main-reviewed compact facts；无可用 raw 或完整逐季度状态；运行 Candidate identity / 月级里程碑未知。 |
| candidate-v4-lean-runtime-policy Run #1 | session `fdcaa70a85f44662a6a329513c175676`；`docs/project/runs/v4-run1-health-forensic.md` (blob `cbb60024a9f76dc905f42fcf1689f61b117d01d8`) | 25.84 / 18.09；6 月；E | Health=0 terminal；压缩 forensic，可观察到关键状态—动作矛盾；只有短局，不代表长程行为。 |

### 解释限制

- v1 Run #1 与 #2 的巨大差异是 `MULTIRUN_OBSERVED` 的结果方差，不是策略效果估计。两局候选/事件/随机状态不同；不能用终局分差归因于一个动作。
- v1 Run #1、v1 Run #2、S06 Run #1 都有 Key-project 主行动占比很高（前两者分别 16/16、7/8；S06 为 16/16），结果却不同。固定 Main action 频率本身既非成功解释，也非足够策略。
- M49 是 v1 Run #1 轨迹中的终局规范化/完成 sentinel，不是额外游戏月、晋升月或工资生效月。M48 新晋升在本局窗口内没有后续工资月；不得据此做薪资 NPV 反事实。
- 六个月窗口统一使用月份末公开里程碑；季度表中的 `pre-Energy` 状态是该季度决策时点，两者不可混为同一快照。状态顺序为 `Level / Skill / Network / Output / Health / Dignity / Wealth`。
- “gap candidate”只是在当时可见材料下可提出的问题；未被显式 checkpoint 记录的，标 `UNKNOWN`，不倒推 Agent 当时已识别。

## 2. Cross-Run Strategy Matrix｜跨局策略矩阵

等级描述的是记录支持程度，不是策略评分：`STRONG` 表示行为/状态事实清楚；`MIXED` 表示同时有正反信号或记录不完整；`WEAK` 表示有明确失败现象，但原因仍可能未知；`UNKNOWN` 表示无法判断。

| Run | Survival / risk control | Growth / progression | Bottleneck adaptation | Review responsiveness | Risk handling | Quarter efficiency | Long-horizon adherence | Outcome |
|---|---|---|---|---|---|---|---|---|
| S01 baseline | `UNKNOWN`：19 月终止，原因未知 | `WEAK`：baseline 为 minimal/no-op 对照 | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | 26.95 / 18.86，19m，E |
| SCORE-01 | `MIXED`：曾投入 Health recovery，但低 Health / Network 状态可见；终止原因未知 | `WEAK`：M1–M23 多处停在 L1、Skill/Network 增长有限 | `MIXED`：能量有变化，但公开状态低增长；具体动作效果无法分离 | `UNKNOWN`：C/D feedback 与后续复盘的关系不完整 | `UNKNOWN`：终止原因与危机时序未知 | `MIXED`：恢复与成长行动并存，无因果分解 | `UNKNOWN`：24m 提前终止，不能评价 48m planning adherence | 33.06 / 23.14，24m，D；终止原因未知 |
| Candidate v1 #1 | `MIXED`：Health 多次恢复并到达 48m；未证明其它风险维度控制 | `STRONG`（仅观察）：多个维度上升并 M6/M12/M18/M36/M48 晋升 | `MIXED`：后段缺显式 Planning，missed review 后也无完整目标重置记录 | `MIXED`：M24/M30 missed、M36/M48 晋升；后程 checkpoint 稀少 | `UNKNOWN`：没有足够 trust/compliance 风险轨迹 | `MIXED`：report-heavy 窗口与状态变化并存，不能归因 | `MIXED`：run 到 48m，但后程 checkpoint/adherence 未被充分记录 | 76.04 / 53.23，48m，A |
| Candidate v1 #2 | `WEAK`（终局层面）：M25 trust-crisis 终止，Health=10；具体错过的公开信号/决策 UNKNOWN | `MIXED`：M6/M12/M24 晋升但仅到 25m | `UNKNOWN`：缺 M18 状态及危机前轨迹 | `MIXED`：M18 missed、M24 晋升；feedback 和复盘时序不全 | `UNKNOWN`：terminal risk 存在，但告警和处理链缺失 | `UNKNOWN`：季度间状态数据不足 | `UNKNOWN`：25m 未覆盖长程 planning behavior | 35.31 / 24.72，25m，D |
| S06 Run #1 | `UNKNOWN`：虽到 48m，缺月级 risk state | `MIXED`：L4、Skill89、Network36、Wealth21.8；季度主行动 16/16 Key project | `WEAK`（行为证据）：重复项目/汇报在公开状态无预期增长时仍以 advertised effect 为重要理由 | `WEAK`（记录证据）：正式 Board/Planning checkpoint 集中在早期 | `UNKNOWN` | `UNKNOWN`：Energy 明细不能逐季复核 | `WEAK`（行为证据）：后期正式 checkpoint 缺失；长程因果仍未知 | 53.83 / 37.68，48m，C |
| v4 Run #1 | `WEAK`（明确控制缺陷）：Health=1 且识别 Material Risk 后仍选择增长，随后 Health=0 | `MIXED`：M6 晋升，但同月终局 | `UNKNOWN`：仅 6m，无法测试长程停滞 | `UNKNOWN`：短局且正式 checkpoint 很少 | `MIXED`：M3 confidentiality cue 被妥善处理；终局 Health 风险未落实为行动约束 | `MIXED`：Q1 做了 recovery，但直到 M6 才有下一 Energy 时点 | `UNKNOWN`：6m 不足以判断 48m adherence | 25.84 / 18.09，6m，E |

### 跨局可支持的判断

1. `RUN_OBSERVED`：Key project 高占比并不唯一对应高分或生存；v1 #1 高分、v1 #2 早终止、S06 #1 中分都可见高占比。不能从 v1 #1 提取“16/16 Key project”作为规则。
2. `RUN_OBSERVED`：v1 #1 的 Skill/Network/Output/Wealth 在 M33–36 约为 90–100 / 36 / 25–29 / 17–21；S06 终局仅记录 L4、Skill89、Network36、Wealth21.8。它们在部分维度上相近，但由于 S06 月级轨迹、候选身份和中间状态缺失，只支持“值得查 bottleneck adaptation”，不支持哪项行为导致终局差异。
3. `RUN_OBSERVED`：Health 高不保证没有重大风险（v1 #2 在 Health10 时 trust-crisis 终止）；Health 低也不应自动改成全局保守人格（v4 证据指向对已识别 terminal risk 的行动约束执行问题）。
4. `INFERENCE`：真正跨局重复出现的决策缺口不是“某个具体选项选错”，而是需要在鲜活公开状态、正式 feedback、重大风险出现时重新评估当前目标与约束。

## 3. Six-Month Windows｜48 个月窗口回看

这些表用于并排审阅，而非补造缺失轨迹。`UNKNOWN` 表示没有可审计的窗口级事实；“未观察到 checkpoint”仅代表当前材料没有记录，不等于证明当时没有任何思考。

### Candidate v1 Run #1｜48m

| Window | Start → end public state | Survival signals | Promotion readiness / Primary-gap candidate | Energy pattern | Main pattern | Formal feedback / promotion / outcome | Retrospective phase / observed mode |
|---|---|---|---|---|---|---|---|
| M1–6 | Start L1/S1/N1/O0; start H/D/W unknown → end L2/S13/N5/O6/H7/D10/W2 | M6 pre-E Health3; end H7 after recovery; other risk channels unknown | Initial checkpoint, but no single defensible gap from available record | Q1 Network+Report+Health; Q2 Health+Report+Health | Key 2/2 | M6 promotion; C/Output feedback summary, exact review alignment incomplete | `FOUNDATION` / `MIXED` |
| M7–12 | M6 L2/S13/N5/O6/H7/D10/W2 → M12 L3/S24/N7/O7/H7/D10/W4 | Health ends 7; no complete trust-risk series | Output/Network considered after M6 feedback; not consistently recorded as one Primary Gap | Q3 Report+Health+Network; Q4 Health×2+Report | Key 2/2 | M12 promotion; an Output-focused checkpoint is recorded | `PROMOTION` / `MIXED` |
| M13–18 | M12 L3/S24/N7/O7/H7/D10/W4 → M18 L4/S44/N19/O16/H10/D10/W6 | Health ends 10; other risk channels unknown | Output highlighted in checkpoint; unique tracked gap thereafter unknown | Q5 Report+Network+Report; Q6 Report×2+Network | Key 2/2 | M18 promotion | `PROMOTION` / `BROAD_GROWTH` |
| M19–24 | M18 L4/S44/N19/O16/H10/D10/W6 → M24 L4/S63/N36/O26/H8/D10/W10 | Health 8 at M24; no adequate trust-risk record | No reliable late checkpoint; public fields changed, so plateau is not established | Q7 Report×2+Health; Q8 Report×2+Network | Key 2/2 | M24 promotion missed; survived through M24 | `PROMOTION` / `MIXED` |
| M25–30 | M24 L4/S63/N36/O26/H8/D10/W10 → M30 L4/S82/N36/O26/H10/D10/W15 | Health 10 at M30 | M30 review missed again; no unique bottleneck was recorded | Q9 Risk cleanup+Health; Q10 Report×2+Health | Key 2/2 | M30 promotion missed; survived through M30 | `PROMOTION` / `MIXED` |
| M31–36 | M30 L4/S82/N36/O26/H10/D10/W15 → M36 L5/S100/N36/O29/H9/D10/W21 | Health 9 at M36 | M33 S90/N36/O25 are visible; no hidden readiness threshold may be inferred | Q11 Report×3; Q12 Report×2+Network | Key 2/2 | M36 promotion; survived through M36 | `PROMOTION` / `BROAD_GROWTH` |
| M37–42 | M36 L5/S100/N36/O29/H9/D10/W21 → M42 L5/S115/N54/O38/H9/D10/W30 | Health 9 at M42 | After promotion a reset is a candidate; no unique gap without feedback. M41 S112/N51/O38; M42 review missed | Q13 Risk cleanup+Report; Q14 Report×3 | Key 2/2 | M42 promotion missed; survived through M42 | `COMPOUNDING` / `BROAD_GROWTH` |
| M43–48 | M42 L5/S115/N54/O38/H9/D10/W30 → M48 L6/S138/N51/O40/H9/D10/W39 | M45 Health7; terminal Health9 | One remaining six-month review window; compare realizable public progress and reserve | Q15 Health+Report×2; Q16 Risk cleanup+Health | Key 2/2 | M48 promotion; completed 48m. No post-promotion wage month in this run | `FINAL_SPRINT` / `MIXED` |

`RUN_OBSERVED` 的重要边界：Main 16/16 Key project 与跨维度提升同时出现，但它们之间没有动作级因果识别。M24、M30 missed review 后仍有 Skill/Network/Output 的公开变化，故不能把 missed review 简化成“两次同一目标无进展”；正式 two-comparable-checkpoint `STALLED` 条件未由这些终局点自动满足。

**Deep-audit synthesis.** M1–18 的广泛成长与 M6/M12/M18 晋升同步出现，且 Health 有恢复；这是路径“在当时仍值得继续比较”的描述性信号，不能证明该 Energy bundle 或 Key project 导致晋升。M19–36 的最早高价值 intervention point 是 M24 missed review 后刷新 Primary Gap 并开始比较；但 M24–30 状态并非整体静止，故不能直接切到另一固定动作。Q7–Q11 Report-heavy 与 Output 波动、其它维度进展并存；冗余是待测问题，不是已证事实。M30/M33 的公开状态适合重新诊断但不能调用 Dev 隐阈值。M36 晋升说明原路后来仍可能工作，不证明当时无需复盘。M42 missed 后应重新建立目标与剩余窗口判断；M45 的 Health7 使 recovery reserve 成为合理候选，不能断言它带来 M48 晋升。M48 新 Level 有本局终局价值，但无后续工资月。

### Candidate v1 Run #2｜25m terminal

| Window | Start → end public state | Survival signals | Promotion readiness / Primary-gap candidate | Energy pattern | Main pattern | Formal feedback / promotion / outcome | Retrospective phase / observed mode |
|---|---|---|---|---|---|---|---|
| M1–6 | M1 L1/S1/N4/O0/H4/D7/W1 → M6 L2/S12/N5/O6/H10/D10/W2 | Health4→10; no complete trust history | Early public base only; unique gap unknown | Q1 Report+Network+Health; Q2 Network×2+Report | Key 2/2 | M6 promotion; survived through M6 | `FOUNDATION` / `MIXED` |
| M7–12 | M6 → M12 L3/S24/N8/O10/H9/D10/W3 | Health9 at M12; trust observability incomplete | M12 promotion; observed Low-profile Main choice, but trigger and rationale unknown | Q3 Health×2+Report; Q4 Network×2+Health | Key then Low-profile | M12 promotion; survived through M12 | `PROMOTION` / `MIXED` |
| M13–18 | M12 → complete M18 state unknown | Survival signals at M18 unknown | M18 review missed; pre-review readiness and Primary Gap unknown | Q5 Health×2+Report; Q6 Health+Risk cleanup | Key 2/2 | M18 promotion missed; survived to at least M18 | `PROMOTION` / `MIXED` |
| M19–24 | M18 state unknown → M24 L4/S43/N19/O13/H10/D10/W9 | Health10 at M24; trust-crisis timing unknown | M24 promotion; trust-risk cue path unrecoverable | Q7 Risk cleanup+Report; Q8 Health+Risk cleanup | Key 2/2 | M24 promotion; survived through M24 | `PROMOTION` / `MIXED` |
| M25 (partial) | M24 → M25 L4/S44/N20/O14/H10/D8/W3 terminal | Health10, but second trust-crisis terminal | Readiness no longer relevant; specific public warning and action choice unknown | No complete next quarter | Unknown | Terminal at M25; cause details unavailable | `UNKNOWN` / `UNKNOWN` |

此局反证“Health 满值即可视为总体安全”；但由于 trust-crisis 证据链缺失，不能断言 Agent 忽略了某个具体 warning，也不能把 M12 Low-profile 说成正确或错误。

**Run-level quality summary (v1 #2).** Growth quality is `MIXED`: M6/M12/M24 promotions are observed, then the run terminates at M25. Survival quality is `WEAK at terminal, cause UNKNOWN`: trust-crisis ends the run while Health=10, but warning observability and response are missing. Trust-risk observability is `UNKNOWN`; the record does not establish whether a cue was visible or ignored. Counterfactual confidence about a specific M24–25 alternative is `LOW`; only a general future Risk-review procedure is defensible.

### SCORE-01｜24m terminal

| Window | Start → end public state | Survival signals | Promotion readiness / Primary-gap candidate | Energy pattern | Main pattern | Formal feedback / promotion / outcome | Retrospective phase / observed mode |
|---|---|---|---|---|---|---|---|
| M1–6 | Earliest complete quarterly snapshot M3 L1/S8/N2/O3/H6/D9/W2 → M6 pre-E L1/S9/N2/O2/H6/D10/W3 | Earlier Health3 cue; M6 Health6 | M6 C feedback summary; no reliable unique gap | Q1 Network+Health+Report; Q2 Report+Network+Report | Key 2/2 | C summary; no confirmed promotion | `FOUNDATION` / `MIXED` |
| M7–12 | M9 L1/S9/N3/O3/H7/D9/W4 → M12 pre-E L1/S9/N3/O2/H7/D10/W4 | Health7 at M12; risk details incomplete | Level/Skill/Network remain low; exact feedback linkage unknown | Q3 Report+Network+Report; Q4 Risk cleanup+Report | Key 2/2 | No confirmed promotion; review summary incomplete | `FOUNDATION` / `MIXED` |
| M13–18 | M12 → M15 pre-E L1/S9/N3/O1/H6/D10/W7; M18 pre-E L1/S9/N3/O−1/H4/D8/W8 | M17 Network0; M18 Health4/Dignity8; warning signals present | M18 feedback summary; progression and survival both warrant fresh review | Q5 Report+Network+Report; Q6 Health×2+Report | Key 2/2 | M18 feedback D; no confirmed promotion | `FOUNDATION` / `MIXED` |
| M19–24 | M21 L1/S9/N3/O3/H8/D10/W10 → terminal M24 summary L2/Wealth11.4/Resilience17/Skill9/Network2 | Exact terminal channel unknown | No stable readiness interpretation possible; M24 summary conflicts with monthly Level trace | Q7 Network×2+Report | Key in Q7; final Main details unavailable | Terminal by M24; “fired” text is not a verified structured cause | `UNKNOWN` / `UNKNOWN` |

该局支持“公开 progression / resilience 信号停滞值得复盘”的问题设定，不支持精确哪一季行动导致终止或分数。

### S06 Run #1｜48m，窗口级状态不可用

| Window | Start → end public state | Survival signals | Promotion readiness / Primary-gap candidate | Energy pattern | Main pattern | Formal feedback / promotion / outcome | Retrospective phase / observed mode |
|---|---|---|---|---|---|---|---|
| M1–6 | `UNKNOWN` | Monthly Health/risk `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | Window-level `UNKNOWN` | Promotion/feedback `UNKNOWN` | `UNKNOWN` / `UNKNOWN` |
| M7–12 | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | Window-level `UNKNOWN` | `UNKNOWN` | `UNKNOWN` / `UNKNOWN` |
| M13–18 | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | Window-level `UNKNOWN` | `UNKNOWN` | `UNKNOWN` / `UNKNOWN` |
| M19–24 | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | Window-level `UNKNOWN` | `UNKNOWN` | `UNKNOWN` / `UNKNOWN` |
| M25–30 | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | Only aggregate 16/16 Key project is known; not allocatable to this window | `UNKNOWN` | `UNKNOWN` / `UNKNOWN` |
| M31–36 | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | Compact report says late repeated Key project/Report despite no-growth signals; exact month unknown | `UNKNOWN` | `UNKNOWN` / `UNKNOWN` |
| M37–42 | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | Late repeated-action signal cannot be localized | `UNKNOWN` | `UNKNOWN` / `UNKNOWN` |
| M43–48 | `UNKNOWN` → terminal L4/S89/N36/W21.8; Output and other dimensions unknown | Monthly risk history `UNKNOWN` | Month-level readiness `UNKNOWN` | `UNKNOWN` | Late repeated-action signal cannot be localized | 48m/C; promotion timing unknown | `UNKNOWN` / `UNKNOWN` |

**S06 plateau audit.** Same 16/16 Key-project frequency exists in v1 #1 and S06 #1, while their observed outcomes differ; this makes frequency alone a poor explanation. The evidence favoring “adaptation gap rather than simply too little growth effort” is limited to the compact S06 report of repeated project/report after public Output/Network stopped showing expected gains plus early-concentrated checkpoints. It does not prove adaptation caused the L4 outcome. The advertised-over-observed mismatch is localized only to late run, with exact month and comparison window `UNKNOWN`. The descriptive comparison (S06 terminal Skill89/Network36/Wealth21.8 vs v1 #1 M33–36 Skill90–100/Network36/Wealth17–21) motivates bottleneck review, but the runs and candidate identities are not controlled. `NO CAUSAL CLAIM`.

### S01 baseline 与 v4 Run #1｜覆盖不足窗口

| Run / Window | Start → end public state | Survival / readiness / gap | Energy / Main / feedback | Phase / actual mode / outcome |
|---|---|---|---|---|
| S01 M1–6 | Window states `UNKNOWN` | Survival signals and Primary Gap `UNKNOWN` | Quarterly pattern `UNKNOWN` | `UNKNOWN`; no reliable window reconstruction |
| S01 M7–12 | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` |
| S01 M13–18 | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` |
| S01 M19 (partial) | `UNKNOWN` | 19m terminal; channel/state `UNKNOWN` | `UNKNOWN` | `UNKNOWN`; minimal/no-op contrast only |
| v4 M1–6 | Exact full-field state `UNKNOWN`; Health observations 5→3→2→4→3→4→3→2→1→0; M3 pre-E H2, M5 H4, M6 H1 before final choice then H0 | M3 confidentiality cue handled; M5 infection cue at H4 is a possible warning but severity is `PARTIAL/UNKNOWN`; M6 known Material Risk at H1 | Q1 one Health recovery plus Network/Report; Main Key project; M6 promotion preceded terminal choice | `FOUNDATION` with transient `SURVIVAL_DEFICIT`; actual `MIXED`; terminal at M6 |
| v4 M7–12 | `NOT_REACHED` | `NOT_REACHED` | `NOT_REACHED` | `NOT_REACHED` |
| v4 M13–18 | `NOT_REACHED` | `NOT_REACHED` | `NOT_REACHED` | `NOT_REACHED` |
| v4 M19–24 | `NOT_REACHED` | `NOT_REACHED` | `NOT_REACHED` | `NOT_REACHED` |
| v4 M25–30 | `NOT_REACHED` | `NOT_REACHED` | `NOT_REACHED` | `NOT_REACHED` |
| v4 M31–36 | `NOT_REACHED` | `NOT_REACHED` | `NOT_REACHED` | `NOT_REACHED` |
| v4 M37–42 | `NOT_REACHED` | `NOT_REACHED` | `NOT_REACHED` | `NOT_REACHED` |
| v4 M43–48 | `NOT_REACHED` | `NOT_REACHED` | `NOT_REACHED` | `NOT_REACHED` |

### SCORE-01 audit classification

| Question | Finding |
|---|---|
| Under-growth | `RUN_OBSERVED / STRONG`: Level stayed L1 through the available M1–M23 monthly series; Skill/Network also remained low. This describes trajectory, not cause. |
| Mis-targeted growth | `HYPOTHESIS / LOW`: repeated Report/Network selections coexist with weak changes in some public fields, but quarters also include other actions and event processing; action-level clipping/saturation cannot be isolated. |
| Survival warning | `RUN_OBSERVED / MEDIUM`: Health3 early, Network0 at M17, Health4/Dignity8 at M18 plus D feedback are visible warning signals for a fresh risk-and-progression review. |
| Terminal mechanism | `UNKNOWN`: M24 “fired” transcript wording is not a structured termination reason; do not label as performance failure or attribute to a specific action. |

### v4 Run #1 controller-failure classification

| Failure mode | Status | Evidence boundary |
|---|---|---|
| Trend recognition failure | `PARTIAL` | Health decline was visible; later reasoning also mentioned H1. This is not a general failure to notice the trend. |
| State-to-action enforcement failure | `SUPPORTED` | At H1, reasoning identified Material Risk but selected growth, followed by H0 terminal. The action’s exact causal contribution is not estimated. |
| Pre-review timing failure | `PARTIAL` | M5 Health4/infection cue precedes M6 terminal and no intervening Energy opportunity; whether the cue justified escalation is not established. |
| Risk-skill activation failure | `PARTIAL` | M3 compliance boundary was correctly handled; M5 cue may have warranted review, but no complete trigger record confirms omission. |

This is an enforcement/cadence defect candidate, not evidence for “always choose the safest option.” S01 remains a minimal contrast: 19m and low score do not show that inactivity guarantees survival or growth; terminal channel is unavailable.

## 4. Strongest Counterfactuals｜最有价值的程序性反事实（最多 10）

以下各行均为 `COUNTERFACTUAL_HYPOTHESIS`。Confidence 仅评价当时公开证据是否足以触发该程序，不代表 alternative 更优、分数会提升或 survival 会改变。

| # / Run / Month | 当时可见 public evidence | Actual policy (known portion) | Candidate alternative principle | Why it might help | Confidence / remaining unknown |
|---|---|---|---|---|---|
| 1 / v4 / M6 | Health1；推理已称 Material Risk；随后 Health0 terminal | Risk 已被口头识别，但仍选 growth | 对 fresh terminal risk 执行候选约束；先排除会无必要加重风险的选项，再比较剩余收益；无安全候选时标 UNKNOWN | 将“识别”连接到“行动过滤”，直接针对已观察到的 state-to-action gap | `HIGH`：触发依据和行动矛盾清楚；替代行动的结果 UNKNOWN |
| 2 / v4 / M5–6 | M5 Health4 + infection cue；M6 前继续下降；下一 Energy 时点来不及阻止 terminal | M3 Q1 有一次 recovery；M5 cue 后具体 action/复盘 UNKNOWN | 在下一决策边界前建立短期 risk checkpoint；确认 cue 是否 fresh/material，而非等到下一季度 Energy | 可能让模型在风险窗口关闭前重新审查公开信号 | `MEDIUM`：cue 是否 material 仍 UNKNOWN；不能估计结果 |
| 3 / v1 #1 / M24 | L4，S/N/O 公开增长；M24 missed promotion | Key project 仍为季度 Main；详细 post-review Planning 未记录 | Review 后刷新 Board/Planning：保留、改写或标 UNKNOWN 一个 Primary Gap | 防止把一次 missed review 当成旧目标仍正确或某动作必错 | `MEDIUM`：复盘触发合理；后续 M30 状态继续变化，不能称已停滞 |
| 4 / v1 #1 / M30–36 | M30 再 missed；M33 S90/N36/O25；M36 promotion | Key project 继续；Q11 Report×3、Q12 Report×2+Network | 结合 fresh feedback 和可比公开字段重评下一瓶颈，不套隐藏 readiness threshold | 有助区分继续积累与转向不同合法路径 | `MEDIUM`：重评依据可见；精确 readiness rule / causal benefit UNKNOWN |
| 5 / v1 #1 / M42–48 | M42 missed；M41 S112/N51/O38；M45 Health7；剩一 review window | Q15 Health+Report×2、Q16 Risk cleanup+Health；Main 仍 Key | reset promotion hypothesis，并同时看剩余可观测窗口、risk reserve、benefit lag | 避免把历史晋升速度当未来保证，并区分立即收益与终局收益 | `MEDIUM`：horizon 边界清楚；实际替代价值 UNKNOWN |
| 6 / SCORE-01 / M15–18 | O1→−1、H6→4、Network 曾为0，M18 有 D feedback 摘要 | Q5 Report+Network+Report；Q6 Health×2+Report；Main Key | 同时刷新 survival 与 progression facts，再比较一个增长路径和一个风险控制路径 | 让低 Health / Network 与低 progression 不被分散处理 | `MEDIUM`：复盘触发可见；M24 terminal reason 与各 action 贡献 UNKNOWN |
| 7 / SCORE-01 / M6–12 | M6 C 摘要后仍见低 progression；是否已 reset 未记录 | Q3 Report+Network+Report；Q4 Risk cleanup+Report；无可确认的对应 checkpoint | 把 formal feedback 转成可验证 checkpoint，记录当前状态和后续比较字段 | 有助检验 feedback 是否进入后续策略，而不是只留下叙述 | `LOW`：feedback 时序与 Agent reasoning 原文不全 |
| 8 / S06 #1 / late, exact month UNKNOWN | Compact evidence: repeated Key project/Report，公开 Output/Network 未按 advertised effect 上升，Planning 集中早期 | Main 16/16 Key project；late repeated actions reported；window-level detail UNKNOWN | 同一目标在两个相邻 comparable checkpoint 记录 observed effect；满足既定双 checkpoint 停滞才强制比较不同类型 alternative | 直接检查 advertised-vs-observed 与 checkpoint decay 的候选机制 | `MEDIUM`：与摘要现象吻合；时间、field attribution、candidate identity、raw 均缺 |
| 9 / v1 #2 / M24–25 | M24 promotion、Health10；M25 trust-crisis terminal；具体 cue / event order UNKNOWN | Risk cleanup 出现在 Q7/Q8；危机前的候选选择 UNKNOWN | 不作具体事件反事实；只要求未来对 fresh trust/compliance escalation 使用现有 Risk review 并记录证据 | 保留独立于 Health 的公开风险审查，而不从事后 terminal 猜选项 | `LOW`：不能证明存在被忽略的 cue，也不能推断 M24 可预知 M25 |
| 10 / v1 #1 / M45–48 | M45 Health7；M48 promotion；M48 后无工资月，M49 不是 gameplay 月 | Q15 Health+Report×2、Q16 Risk cleanup+Health；Main Key | 最后一窗口只计入可在本局实现的公开收益与 survival reserve，不虚构终局 promotion 的后续工资收益 | 避免远期/本局不可实现收益在 horizon 末被高估 | `MEDIUM`：窗口边界清晰；替代方案对最终 score 的影响 UNKNOWN |

## 5. Anti-Patterns｜反模式候选（最多 8）

| 模式 | 证据等级 | 说明与边界 |
|---|---|---|
| `ACKNOWLEDGED_TERMINAL_RISK_WITHOUT_ACTION_CONSTRAINT` | `RUN_OBSERVED / SUPPORTED` | v4 H1 被明确认作 Material Risk 后仍选择 growth。问题是识别没有约束行动，不是要一概保守。 |
| `LATE_RECOVERY_AFTER_RISK_WINDOW_CLOSED` | `RUN_OBSERVED + DEV_CONFIRMED` | v4 M5 cue 到 M6 terminal；季度 Energy cadence 不能保证在同月 terminal 前还有恢复机会。是否 M5 cue 足以判断仍 `PARTIAL`。 |
| `ADVERTISED_EFFECT_OVERRIDES_RELIABLE_OBSERVED_EFFECT` | `RUN_OBSERVED / HYPOTHESIS` | S06 compact facts 支持此风险；缺 raw，不将其扩展为其它局的确定行为。 |
| `EARLY_CHECKPOINTS_WITHOUT_LATE_RECOVERY_CUE` | `RUN_OBSERVED / HYPOTHESIS` | S06 正式 Planning 集中早期；v1 #1 也仅有 3 个显式 checkpoints。没有 transcript 不等于证明策略完全遗忘。 |
| `HIGH_MAIN_ACTION_FREQUENCY_AS_PROXY_FOR_PROGRESS` | `MULTIRUN_OBSERVED / DO_NOT_ENCODE` | 高 Key-project 频率出现在不同成绩/生存结果中；频率不是 observed progress。 |
| `HEALTH_AS_SOLE_SAFETY_SIGNAL` | `MULTIRUN_OBSERVED` | v1 #2 Health10 仍 trust-crisis terminal；需检查其它明确公开风险，不得推广成无限风险清单或隐藏检测器。 |
| `MISSED_REVIEW_EQUALS_ACTION_FAILURE` | `DO_NOT_ENCODE` | v1 #1 M24/M30 missed 但公开状态继续变化、M36 晋升；review 失败应触发复盘，不自动证明特定动作无效。 |
| `REPORT_HEAVY_WINDOW_IS_PROVEN_WASTE` | `NOT_SUPPORTED / DO_NOT_ENCODE` | v1 #1 存在 report-heavy 窗口，同时一些维度有增长并最终晋升；没有 Energy 级因果对照。 |

## 6. Success Patterns｜成功模式证据

没有达到跨局因果标准的通用高分成功模式。以下仅为有限候选：

| 候选 | 证据 | 可保留的窄结论 | 不可推出 |
|---|---|---|---|
| `EARLY_MULTI-DIMENSION_GROWTH_WITH_REVIEW_PROGRESS` | `MULTIRUN_OBSERVED`：v1 #1 前 18m 多字段增长并连续晋升 M6/M12/M18；v1 #2 也在 M6/M12 晋升。 | 这是可继续检验的早期现象：公开状态推进期间继续比较合法 growth path。 | 不能声称某固定 Main/Energy bundle 导致晋升，也不能保证相同路径长期有效；没有通用因果成功模式被建立。 |

## 7. Phase / Regime Findings｜阶段与状态 regime

### 宏观四阶段校准

| Phase | 建议的进入/退出依据 | 本轮校准 |
|---|---|---|
| `FOUNDATION` | 新局/早期公开基础薄弱；同时检查 survival reserve 与可见能力缺口 | 单一“基础期”容易把 survival deficit 与普通 capability building 混在一起。只在公开 Health/其它明确重大风险出现时叠加 survival constraint。 |
| `PROMOTION` | 以即将发生的公开 review、近期 feedback、fresh state 为依据 | 不按固定月份或隐含 Skill/Network threshold 进入；正式 missed/promo 都触发 gap reset。 |
| `COMPOUNDING` | promotion 后有多个可观察增长窗口、风险约束允许继续 | 不是永久保持上一条 growth path 的理由；若 review miss、progress 停滞或风险上升，要切换至短时诊断 mode。 |
| `FINAL_SPRINT` | 剩余 review/收益实现窗口缩短，且公开 horizon 可见 | 用“剩余可比较窗口”和收益是否能在本局实现的质性判断；不规定 M36/M42/M48 固定 action，不计入终局后工资。 |

### 候选 transient regime overlay

主候选仍是四个宏观 phase；可考虑只加几个事件/状态驱动的短时标签，使相同 phase 内可采取不同控制：

1. `SURVIVAL_DEFICIT`：fresh material risk / terminal state 是约束，先按 Risk 评估并约束候选，不切换为全局低风险目标。
2. `POST_REVIEW_RESET`：每次正式 promotion、missed review、重大 feedback 后刷新唯一 Primary Gap 与比较字段。
3. `PLATEAU_DIAGNOSIS`：两个相邻、可比较 checkpoint 对同一目标无 observed progress 后，要求比较一个不同类型 alternative；不自动选择 alternative。
4. `LATE_HORIZON_REALIZATION`：按公开月份/剩余 review windows 判断收益实现时滞，不把长期 uncertain benefit 当本局收益。

`HYPOTHESIS`：上述短时 overlay 比独立增长/晋升/财富子策略或更多 Skill 更能解释本轮跨局问题，且更可观察。当前不新增实现；交由 S06-16 架构审查判断是否可压进三个既有 Skill。

Regime candidate boundary：`POST_PROMOTION_RESET` is included in `POST_REVIEW_RESET`; `RISK_CONTAINMENT` is treated as a temporary response inside `SURVIVAL_DEFICIT`, not a permanent goal. `CAPABILITY_BUILD` and `PROMOTION_PUSH` are not separated into independently triggered modes yet: the available runs do not establish reliable public entry criteria beyond fresh feedback and visible progress, and no threshold may be invented.

## 8. Proposed 48-Month Strategy｜阶段化策略骨架

这是候选控制器流程，不是逐月日历表、收益最大化器或确定有效策略。

1. **建立安全 runway**：fresh Board 中若有明确重大后果，先运行当前候选的 Risk review；普通 soft cost 仍是 opportunity cost，不自动否决 growth。缺证据时标 UNKNOWN。
2. **建立一个 Primary Gap**：使用当前公开 feedback、状态和可合法采取的路径；不能依据 evaluator weights、隐藏阈值或“所有维度都补”。
3. **联合比较季度资源**：对 Energy 与 Main action 使用同一 checkpoint，比较最多两个有公开依据的路径；保留成长机会与风险/时间成本，不预设 action package。
4. **记录实际变化**：Board 仅记录 fresh、可比、可归因的 before/after；广告效果与实际观察分开。故事或其它动作污染比较时写 UNKNOWN。
5. **正式 review 后 reset**：晋升、missed review、重大 feedback 都更新 Board/Planning；保留旧目标仅当 fresh evidence 仍支持其与新目标一致。
6. **按双 checkpoint 判定停滞**：一次未增长不能强制换路。只有同一目标、同一战略动作在两个相邻可比 checkpoint 均无目标进展，标 `STALLED` 并比较 alternative；仍允许有依据地继续原路。
7. **随公开 horizon 调整**：剩余可比较窗口减少时，提高当前可观测 progress 的相对价值；降低只有长程、不可验证收益的路径优先级。不得预测具体晋升月份。

## 9. Candidate Controller Changes｜候选控制器变更（供 Main 决策）

分类仅使用 `ADOPT_CANDIDATE` / `DEFER` / `REJECT`；本节是建议，不表示已修改 v5。

| 候选变更 | Source reviews / historical evidence | Runtime-visible inputs | Expected improvement | Risk / what must NOT be encoded | Decision |
|---|---|---|---|---|---|
| Fresh Material Risk 必须影响当前候选选择 | S06-08、S06-11；v4 H1 `RUN_OBSERVED` | 当前 candidate、fresh Health/trust/compliance/escalation/survival cues | 让风险识别参与真实候选过滤 | 普通 soft cost 不单独否决；不发明 Health cutoff | `ADOPT_CANDIDATE` |
| Promotion / missed review / major feedback 后刷新 Primary Gap | S06-12；v1 #1 review sequence；SCORE-01 feedback | 当前 formal outcome、fresh feedback、public state | 减少 stale goal 延续 | missed review 不等于某 action 已证无效；不套隐藏 readiness threshold | `ADOPT_CANDIDATE` |
| Qualitative promotion-readiness proxy | S06-12；v1 #1/#2 reviews；SCORE-01 | 仅 fresh public feedback、可比较 observed progress、公开 review outcome | 让 readiness 复盘有明确证据输入 | 不给出数值 threshold、概率或固定月份；现有证据不足以冻结独立 proxy | `DEFER` |
| Observed effect 优先于未验证的 advertised effect | S06-01、S06-13；S06 Run #1 compact facts | 同一 session 的 comparable fresh before/after 与 attribution quality | 发现重复动作的真实停滞，减少虚报进展 | 被污染时 UNKNOWN；不把一次无增长判停滞 | `ADOPT_CANDIDATE` |
| 两个 comparable checkpoint 后进入 plateau diagnosis | S06-01、S06-13；S06 #1 compact facts；v1 #1 的反例提醒 | 同一目标/动作、相邻 checkpoints、可靠 observed delta | 触发有证据的 alternative comparison | 只要求比较，不强迫切换；不把 M24/M30 missed 自动当作双 checkpoint stall | `ADOPT_CANDIDATE` |
| Survival-deficit transient regime | S06-08、S06-11；v4 Run #1 | Fresh material-risk cue 与当前候选后果 | 把 risk constraint 和普通 growth trade-off 分开 | 不变成全局保守人格、永久 Health monitor 或隐藏 risk detector | `ADOPT_CANDIDATE` |
| Review reset / plateau diagnostic 如何映射进现有三 Skill | S06-11 至 S06-14；本轮跨局 matrix | 三 Skill 已有职责、fresh facts、Planning checkpoint | 控制重复 prose 与职责重叠 | 不新增 Memory、第五 Skill、agent 或持久化机制 | `DEFER` |
| Remaining-window / benefit-realization-lag 判断 | S06-12；v1 #1 M48 promotion、M49 sentinel 边界 | Public month、remaining review windows、可观察收益实现时间 | 避免把本局无法实现的远期收益过度计入 | 不做薪酬 NPV、固定末期日历或月→动作规则 | `ADOPT_CANDIDATE` |
| Energy + Main action 围绕同一 Primary Gap 联合比较 | S06-13；v1/SCORE-01 季度快照 | 当季合法 Energy/Main 候选、同一 fresh checkpoint | 避免资源分配与季度目标脱节 | 不输出固定 bundle；不从单局分数调权 | `ADOPT_CANDIDATE` |
| Story decision 用当前 cue + fresh state 做短风险检查 | S06-14；v4 M3/M5–6；v1 #2 cue chain unavailable | 当前事件文本、当前候选、fresh public state | 保留可迁移的授权/升级/健康语义判断 | 不用 event title lookup；不从 v1 #2 terminal 反推警告 | `ADOPT_CANDIDATE` |
| 完整 phase+regime 二层架构与最终提示词落点 | S06-11 至 S06-14；当前三 Skill 边界；本轮无 runtime 新证据 | Candidate v5 三 Skill 与其现有职责 | 可能提高长程控制清晰度 | 实现前由 S06-16 做最小职责/成本审查；本任务不修改 | `DEFER` |
| 固定 Key-project 频率、Energy bundle、Promotion threshold、wealth/salary rule | 跨局异质性；S06-12/13；本轮窗口证据 | 不适用：缺少合法通用 runtime signal | 无可支持的预期收益 | 禁止固定配方、事件答案、hidden threshold、evaluator weight | `REJECT` |

## 10. Remaining Unknowns｜未决问题

- Candidate v1 Run #2 的 trust-crisis 前兆、告警时间、实际选择与 M18 状态；终止机制不能补造。
- SCORE-01 的结构化终止原因、候选身份，以及 M24 终局 Level2 与月序列不一致的底层解释。
- S06 Run #1 的候选身份、逐季度/逐月 fresh Board、Energy、Risk、Promotion 和动作效果归因；raw 当前不可用。
- v1 Run #1 后期正式 Planning 内容、Agent 是否做过未记录的 checkpoint，以及 review feedback 与各 promotion 的月级关联。
- v4 M5 infection cue 当时是否足以构成 Material Risk；M6 若选择不同合法动作是否会改变终局。
- 任一候选策略对平均分、分数方差、survival 或 stable 80+ 的作用；单/少数真实局不能解决因果和稳定性问题。
- 云端/正式竞赛环境是否按同一 lifecycle 重建 Strategy/Skill，以及未来 runtime adherence；本审查没有触及该边界。

## 11. Method / Operation Proof

### Inputs for S06-16

- 保留本审查的 `COUNTERFACTUAL_HYPOTHESIS` 与 `UNKNOWN` 标签，不把 proposal 当 accepted runtime contract。
- 优先评审两件事：现有 Risk 能否把已识别 Material Risk 稳定连接到候选行动约束；Planning/Board 能否在 formal review 后刷新 gap 并支持可比较的双 checkpoint 停滞判断。
- 将 qualitative promotion-readiness proxy 与完整 phase+regime 两层架构维持 `DEFER`，直到能给出合法、公开、低复杂度且可静态检查的触发条件。
- 不改变 Game Gate、candidate identity、Skill 数量、architecture 或任何 runtime authorization。

- 类型：离线、基于已提交事实的跨局归并；未重新分析 private/test/hidden data。
- 修改范围：仅新增本文；未修改 Skill、candidate、Runner、dependency、lockfile、CURRENT_STATE、STRATEGY_EVIDENCE 或 RUN_HISTORY。
- Competition provider requests: `0`
- JiuwenSwarm service starts / installs / reloads: `0`
- MCP calls / CareerSim actions: `0`
- Games / benchmarks: `0`
- 新增脚本或 raw evidence: `0`
- Git base checked: `bef71109a0cfea6a1223792a819f080e66b20f8a`

## 12. Next Recommendation

`RETURN_TO_MAIN_FOR_S06_16_FINAL_CONTROL_ARCHITECTURE_REVIEW`

不授权 benchmark，不自行修改 Candidate/Skills，不宣布 S06 complete。
