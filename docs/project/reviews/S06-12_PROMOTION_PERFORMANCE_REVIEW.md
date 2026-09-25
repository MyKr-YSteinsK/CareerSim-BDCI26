# S06-12｜晋升绩效与财富复利机制深挖

## 1. 任务边界与结论

- Base: `main@ff171e67300131951f9b5da2ef2be3acd4b497de`，执行时 `HEAD == origin/main`，初始工作树干净。
- 范围：离线读取已提交的去敏轨迹、当前项目事实源与根 `.venv` 中冻结的公开 Dev / 模拟器源码；只新增本 review。
- 未修改：`configs/**`、`skills/**`、`career_sim_runner/**`、`STRATEGY_EVIDENCE.md`、`RUN_HISTORY.md`、候选 v5、依赖、运行时及 raw evidence。
- Live operation：gameplay `0`，provider `0`，Jiuwen service `0`，MCP `0`，install/reload `0`。
- 当前候选与权限不变：`candidate-v5-evidence-driven-phase-policy` 仍是静态候选；本 review 不授权游戏、不证明收益，也不把 S06 标记为完成。

**结论：** 可将“公开晋升准备度 + 半年反馈后重诊断 + 晋升后重置 Primary Gap”作为下一轮静态候选审查方向。工资机制确认了同一晋升更早发生会留下更长的工资/奖金基数窗口，但并不能压过生存约束，也不能证明越早晋升越好。公开 Dev 的绩效公式不支持固定 Skill:Network 比率；中度不均衡在指定的同总量例子中甚至略高于均衡配对。任何精确门槛、公式、比例或 NPV 都不得写入 Runtime Policy。

## 2. 证据标签与来源身份

本文使用：

- `DEV_CONFIRMED`：冻结版本的模拟器源码或公开 Dev 配置直接确认；不等于 Agent 可见。
- `RUN_OBSERVED`：单局去敏记录中的直接观察。
- `MULTIRUN_OBSERVED`：多个运行中重复出现的描述事实；不等于因果或稳定规律。
- `DERIVED_DEV_ANALYSIS`：用冻结 Dev 公式对公开状态做的离线计算；不可转成 Agent 运行时阈值。
- `HYPOTHESIS`：有证据支持、仍待独立验证的策略解释。
- `UNKNOWN`：现有紧凑证据不足；不补造缺失值。
- `DO_NOT_ENCODE`：只供本地机制审查，不进入 Candidate instruction / Skills。

| 输入 | 本轮核验结果 |
|---|---|
| 模拟器 | 根 `.venv` distribution `career-emulator==1.0.1`；源码位于 `.venv/Lib/site-packages/career_emulator/` |
| 公共 Dev | `career-emulator-bdci26==1.0.0`；Dev 配置位于 `.venv/Lib/site-packages/career_emulator_bdci26/dev/dataset/` |
| 全 Dev 目录身份 | 复用 [`STRATEGY_EVIDENCE.md`](../STRATEGY_EVIDENCE.md) §1 已记录的 192 个 `.data` 摘要 `493efab9d0dbae6fe4c94a1cae13e12c30e98e239a1afc5990d1803cdaa0dac4`（194 个目录文件摘要 `ecadbb6df2335e55b1e898de94102c9a2b2cdb23e8e7790912b8c2fb228d2fe4`）；本任务未重扫事件模板。 |
| 配置复核 | performance、promotion、salary、talk 这 7 个目标配置在 Dev package 与模拟器 materialized data 两份路径逐文件相同；SHA256 见 §11。 |
| 历史轨迹 | v1 #1/#2：Git commit `66ec4af1e9a2a28da57c6cb8d409a6a38f87ae01` 的 compact trajectories；SCORE-01：`7a055dea76580117ca74cddb49bb04efcf605eb1` 的 `score01_trajectory.json`；S06 #1：`c4dbe0ebc4e27aafc22c94050c69547113cdc8eb` 的 Main-reviewed S06-01 RESULT 及当前 [`RUN_HISTORY.md`](../RUN_HISTORY.md)；v4 #1：当前 RUN_HISTORY 与 [`v4-run1-health-forensic.md`](../runs/v4-run1-health-forensic.md)。 |
| Raw 边界 | S04 原始 events/transcript 当前不可用；S06 #1 原始文件未用于本 review。只用已提交且可核验的 compact evidence，不重跑对局。 |

源码锚点：`failure_conditions.py::_compute_performance_score` / `_performance_level_adj` / `field_value`；`promotion_conditions.py::PromotionApplicator.apply` / `_is_rapid_promotion`；`talk_mechanism.py::TalkMechanismApplicator.apply`；`salary_conditions.py::SalaryConditionApplicator.apply_monthly` / `_resolve_bonus_amount`；`game.py::GameEngine._on_month_advanced`；`ending_score.py::EndingScoreCalculator.compute`（确认 48 月完成状态与最终加权维度的结算边界）。本 review 不把 EndingScore weights 用作策略输入。数据路径与版本见上表。

## 3. 晋升时间线：可恢复运行

表中 `S/N/O/D/H/W` 分别为 Skill、Network、Output、Dignity、Health、Wealth。数值是最近可用的月末或季度前状态，不自动等同于晋升结算瞬间。上一轮正式反馈只有轨迹明确记录时才列出；`UNKNOWN` 不代表没有反馈。

### Candidate v1 #1（48 月，76.04 / 53.23 / A）

| 晋升/窗口 | 晋升前最近公开状态 | 反馈 | 晋升后状态 | 后续约 6 个月 |
|---|---|---|---|---|
| M6 L1→L2 | M5：L1；S9/N3/O3/D10/H4/W2 | 首个半年 review；具体 review 记录不完整。后续 checkpoint 提及 first-half C，但它是否与本行晋升瞬间一一对应：`UNKNOWN` | M6：L2；S13/N5/O6/D10/H7/W2 | M12 L3；S24/N7/O7/D10/H7/W4，并再次晋升 |
| M12 L2→L3 | M11：L2；S21/N7/O6/D10/H4/W4 | 最近可追溯反馈：M6 后的 C 与 Leader 希望更清晰 Output（紧凑 checkpoint 叙述，非结构化 score report） | M12：L3；S24/N7/O7/D10/H7/W4 | M18 L4；S44/N19/O16/D10/H10/W6，并再次晋升 |
| M18 L3→L4 | M17：L3；S41/N19/O14/D10/H10/W5 | `UNKNOWN` | M18：L4；S44/N19/O16/D10/H10/W6 | M24 未晋升；L4、S63/N35/O25/D10/H8/W10 |
| M36 L4→L5 | M33 季度前：L4；S90/N36/O25/D10/H9/W17 | `UNKNOWN` | M36：L5；S100/N36/O29/D10/H9/W21 | M42 未晋升；L5、S115/N54/O38/D10/H9/W30 |
| M48 L5→L6 | M47：L5；S135/N54/O38/D10/H7/W36 | `UNKNOWN` | M48：L6；S138/N51/O40/D10/H9/W39 | 48 月终点后无可用的下个六个月窗口 |

`RUN_OBSERVED`：晋升月份是 M6、M12、M18、M36、M48。M24 与 M30 连续两个 review 未晋升；M36 再晋升。M49 仅是历史 compact trajectory 的时间归一化/完成哨兵，S06-11 已核实其原因是“完成 48 个月模拟”，不能当作第 49 个游戏月或晋升后工资月。

### Candidate v1 #2（25 月终止，35.31 / 24.72 / D）

| 晋升/窗口 | 最近可用公开状态 | 反馈 | 下一阶段 |
|---|---|---|---|
| M6 L1→L2 | M1：L1 S1/N4/O0/D7/H4/W1；M6 milestone：L2 S12/N5/O6/D10/H10/W2 | `UNKNOWN` | M12 L3；S24/N8/O10/D10/H9/W3，再次晋升 |
| M12 L2→L3 | M12 milestone 同左；M6 与 M12 间快速晋升 | `UNKNOWN`；记录的 M12 低调避险不是正式 performance feedback | M18 没有晋升记录；该月各维度精确状态 `UNKNOWN` |
| M18 missed / M24 L3→L4 | M12：L3 S24/N8/O10/D10/H9/W3；M18 状态缺失；M24 milestone：L4 S43/N19/O13/D10/H10/W9 | `UNKNOWN` | M25 终止：L4 S44/N20/O14/D8/H10/W3；六个月窗口不可得 |

`RUN_OBSERVED`：晋升月份 M6、M12、M24；M18 未晋升，M24 恢复晋升。M12→M24 的状态差异不能拆成单项动作的因果效果；M24 的 milestone 状态可能已经包含晋升后的故事/季度变化，不能用它反推晋升瞬间阈值。

### SCORE-01、S06 Run #1、v4 #1

| Run | 晋升事实与可用状态 | 反馈 / 六个月结果 |
|---|---|---|
| SCORE-01 | compact monthly state 中 M1–M23 均为 L1；M6/M12/M18 仍记录 L1。另一份终局摘要记录 M24 Level 2。精确晋升月与终局前的 Level 变更时间 `UNKNOWN`，存在月度轨迹缺最后窗口而终局为 L2 的边界不一致。 | M6 的 C、M18 的 D 来自 Agent transcript 摘要，并非结构化绩效字段；半年评级序列不完整。M24 终止，无后续窗口。 |
| S06 Run #1 | 48 月完成，终局 L4；promotion months、session、候选身份、月度 S/N/O/D/H/W 与原始反馈均 `UNKNOWN`。 | 16/16 季度 main action 是申请关键项目；后期存在重复动作无公开增长的记录。没有可重建的晋升间隔或下一窗口表。 |
| v4 #1 | M6 首次观察到 L1→L2；终局同在 M6，Health=0，Level2、Skill11/Network7/Output6/Dignity9/Wealth2.2。晋升结算和 M6 story 的先后顺序由 frozen `game.py` 确认：半年结算在该月 story actions 前。 | M6 前反馈细节 `UNKNOWN`；没有后续六个月。该运行显示当月晋升与当月 Health terminal 可以同时发生，晋升不是 survival evidence。 |

**覆盖边界：** v1 #1 是唯一拥有连续月度公开状态和完整晋升清单的运行；v1 #2 只有 milestone；SCORE-01 记录到 M23；S06 #1 只有 Main-reviewed 摘要；v4 #1 的详细记录只覆盖 M1–M6。不能将未知的 promotion month、Leader feedback、post-promotion trajectory 填成估计值。

## 4. Performance geometry｜公开 Dev 离线计算

`DEV_CONFIRMED`：冻结公式对 `low=min(Skill,Network)`、`high=max(...)` 使用软上限；无 Output/Level 项之前的 S/N 分量为：

`(min(high, 2×low) + 0.3×max(0, high−2×low)) / 15`

随后加 `Output/10` 和 Level-specific polynomial，再取整数 round。硬上限关闭。这里的比例与公式是隐藏 Dev 实现，只可作离线分析。

| Skill / Network | S/N 分量 | 同总量均衡配对 | 均衡配对分量 | 差值 |
|---|---:|---|---:|---:|
| 10 / 10 | 0.6667 | 10 / 10 | 0.6667 | 0.0000 |
| 15 / 5 | 0.7667 | 10 / 10 | 0.6667 | +0.1000 |
| 18 / 6 | 0.9200 | 12 / 12 | 0.8000 | +0.1200 |
| 20 / 10 | 1.3333 | 15 / 15 | 1.0000 | +0.3333 |
| 30 / 10 | 1.5333 | 20 / 20 | 1.3333 | +0.2000 |
| 30 / 20 | 2.0000 | 25 / 25 | 1.6667 | +0.3333 |
| 60 / 20 | 3.0667 | 40 / 40 | 2.6667 | +0.4000 |
| 60 / 40 | 4.0000 | 50 / 50 | 3.3333 | +0.6667 |

**`DERIVED_DEV_ANALYSIS`：** 不能把“Skill 与 Network 必须 1:1 均衡”写成规则：在这些同总量配对中，所列中度偏斜组合的 S/N 分量略高。另一方面，当高的一项超过另一项的两倍后，超出部分的边际只按 0.3 计；因此公式既不是简单总和，也不是无限奖励单项堆高。每个固定 Level / Output 下，原始 S/N 几何相同；Level 项改变总分基线、整数 round 与处于 mercy 时的有效结果。

Output 的公式边际是所有 Level 相同的 `+0.1` 未取整绩效分 / Output 点；每 10 点增加 1 个未取整分，单点变化是否改变整数分取决于 round 位置。它还分别进入晋升条件，且各晋升级别有不同隐藏要求与 growth cap。不能以此推出“每次汇报材料都有效”：`RUN_OBSERVED` 的 S06 #1 在 Output 26 后仍记录过重复准备汇报材料但无公开 Output 增长；v1 #1 的 Output 则在整个轨迹继续变化并最终 M36/M48 晋升。单局停滞不证明 action 普遍无效。

同一 S/N/Output 在不同 Level 得分不同，因为 Level-specific polynomial 是公式输入；M1–M12 的有效 performance 若低于 4 会被 floor 到 4，M13 起不再有此 mercy。由此更适合用实际 feedback 和 fresh public deltas 做 review，而不是把 Dev score 算式或某个 S/N 比例暴露到运行策略。

## 5. L1–L10 晋升 bottleneck map｜Dev-only

`DEV_CONFIRMED`：半年一评；必须 alive、在当前 Level 至少 6 个月、且尚未到 L10。代码将 `optional_conditions` 的 Performance 条件也与其它 required conditions 做 AND。下表仅用于本 review 的事后机制解释；公开手册将晋升门槛列为隐藏信息。

| Transition | Skill | Output | Network | Dignity | Performance | Promotion Network change |
|---|---:|---:|---:|---:|---:|---:|
| L1→L2 | 8 | 3 | 3 | 2 | 3 | 0 |
| L2→L3 | 18 | 5 | 6 | 3 | 4 | 0 |
| L3→L4 | 35 | 14 | 18 | 3 | 5 | −2 |
| L4→L5 | 90 | 22 | 30 | 4 | 4 | −2 |
| L5→L6 | 130 | 32 | 45 | 4 | 4 | −3 |
| L6→L7 | 170 | 45 | 60 | 5 | 6 | −4 |
| L7→L8 | 210 | 60 | 80 | 5 | 8 | −4 |
| L8→L9 | 250 | 75 | 100 | 6 | 10 | −5 |
| L9→L10 | 290 | 90 | 120 | 7 | 12 | −5 |

另有 Level 当前门槛的 1.2× Skill/Network/Output clamp；promotion 时先检查距离上次晋升是否 `<12` 月，是则额外 Network−3、Dignity−1，再进行 Level-specific promotion change。因而快速晋升有即时合作/尊严机会成本，不能只看新 Level 工资。每六个月才 review、Level 至少待六个月；`max_promotions_in_window` 配置名不应被解释为已验证的硬性 eligibility 规则，实际 matcher 要以源码执行路径为准。

### 历史晋升间隔的机制解释

- v1 #1 的 M6→M12→M18 连续六个月晋升，按 frozen Dev 触发两次 `<12` 月 rapid penalty；结果仍分别晋升。trajectory 上各属性同时有事件、quarter action、talk 等变化，不能从净值估算 penalty 的单独效果。
- v1 #1 的 M18→M24/M30 没有晋升。`DERIVED_DEV_ANALYSIS`：L4→L5 的 Dev-only 表要求 S90/O22/N30/D4/P4。晋升 review 前最近快照 M23 是 S62/N36/O23/D10，M29 是 S76/N32/O25/D10；按 exact Dev performance formula 复算 base 分别为 6 与 7，即使套用当次最不利的公开 talk adjustment −2 仍为 4 与 5，达到此转移的 Dev performance gate。两窗口 Skill 尚未到 Dev 配置要求，N/O/D 已达到。因此在这份轨迹和这份 Dev build 中，Skill 是唯一已识别的未满足项。M33 时 Skill=90，后在 M36 晋升。此结论是离线诊断，不允许 Agent 使用隐藏 Skill=90 阈值。
- M33 季度状态 Skill 90、Network36、Output25、Dignity10，M36 晋升 L4→L5。时间序列与上述 bottleneck diagnosis 一致，但不能证明“某个动作导致晋升”。
- M36→M42 后 L5 状态 S100→115、N36→54、O29→38；M42 晋升 review 前最近快照 M41 为 S112/N51/O38/D10，base performance=7，即使减去 −2 talk adjustment 仍高于 L5→L6 的 Dev gate 4，而 Skill 未达 Dev 配置要求。M45 Skill127，M46 为131，M48 晋升 L5→L6。`DERIVED_DEV_ANALYSIS`：S/N/O/D 的轨迹与 Skill 成为此段剩余可见瓶颈相符；表现门槛按公式看不构成明显阻塞。M49 sentinel 不是后续成长观察。
- v1 #2 的 M12 状态 S24/N8/O10 距 L3→L4 所需公开维度仍有明显差距；M18 未晋升，M24 已为 L4。M18 精确状态及该窗口 Leader feedback 缺失，不能判断当时哪一项先达到条件；M24 milestone 可能已受 M24 promotion 后事件影响。
- S06 Run #1 终局 L4、v1 #1 终局 L6，两局都记录 16/16 季度主行动申请关键项目，但 S06 的 promotion months 缺失，run candidate identity 也 UNKNOWN。`HYPOTHESIS`：努力次数不能代替对进展瓶颈的适配；轨迹差异值得把 fresh observed effects 与 review 结果用于重诊断。反例限制是 v1 #1 在同样主行动分布下仍到 L6，因此不能声称固定项目行动本身导致 S06 的较低 Level。
- v4 #1 在 M6 晋升 L1→L2，却在同月 Health=0 终止；promotion progress 不能替代生存安全。

**Early / mid / late 解释：** early stage 首要难点是多项可见状态共同成长且第一个 review 已在 M6；M13 起 mercy 消失，M18 是第一个不受 first-year floor 的半年 review。mid stage 的下一 Level 需求变化可能把一个原来够用的状态变成瓶颈，晋升后 Network 还会扣减。late stage 各项 Dev 门槛继续增长、Output/Network 同时要持续积累；本机历史只到 L6，不能把 L7–L10 门槛推广为实战成功率。

## 6. Promotion economics｜48 月内的名义工资差

`DEV_CONFIRMED`：月 base Wealth 随 Level 变化；review 月的 salary / half-year payout 在 promotion review 之前处理，新 base 从次月生效。下表是一次 promotion 相对“继续留在旧 Level”的纯 base-pay 算术差，单位为配置的 Wealth units；未计 survival、未来晋升、事件收入/支出、bonus tier 与 fractional Wealth 汇总误差。

| Transition | 每月 base 增量 | 后续 6 月 base 差 | 后续 12 月 base 差 |
|---|---:|---:|---:|
| L1→L2 | 0.1 | 0.6 | 1.2 |
| L2→L3 | 0.1 | 0.6 | 1.2 |
| L3→L4 | 0.2 | 1.2 | 2.4 |
| L4→L5 | 0.3 | 1.8 | 3.6 |
| L5→L6 | 0.5 | 3.0 | 6.0 |
| L6→L7 | 0.8 | 4.8 | 9.6 |
| L7→L8 | 1.3 | 7.8 | 15.6 |
| L8→L9 | 2.1 | 12.6 | 25.2 |
| L9→L10 | 3.4 | 20.4 | 40.8 |

| Promotion review month | Remaining paid months M+1…M48 | Remaining half-year bonus windows | L4→L5 base-only difference | L5→L6 base-only difference |
|---:|---:|---:|---:|---:|
| M6 | 42 | 7 | 12.6 | 21.0 |
| M12 | 36 | 6 | 10.8 | 18.0 |
| M18 | 30 | 5 | 9.0 | 15.0 |
| M24 | 24 | 4 | 7.2 | 12.0 |
| M30 | 18 | 3 | 5.4 | 9.0 |
| M36 | 12 | 2 | 3.6 | 6.0 |
| M42 | 6 | 1 | 1.8 | 3.0 |

**Interpretation:** for a fixed level transition, earlier promotion creates more remaining base-pay months; for different transitions, per-level salary increments are not equal (late high-Level steps can have a larger monthly delta despite shorter horizon). Bonus uses the current Level's base and a half-year performance tier, so later qualifying payouts inherit the higher base when promotion preceded that review. A promotion at M48 changes Level at the final review but its salary and bonus at M48 were already processed at the prior Level; there is no post-promotion salary month inside the 48-month horizon. The compact M49 sentinel is not counted.

This is not expected Wealth, not a promotion-NPV optimizer, and not evidence that promotion-first is safe. Bonus tier, whether the Agent can reliably observe salary changes, survival through future windows, and subsequent promotions all affect realized value. **`DO_NOT_ENCODE`** exact salary schedules, bonus multipliers, or calculated NPV in runtime policy.

## 7. First-year performance mercy

`DEV_CONFIRMED`：performance config applies an effective floor of 4 when the computed score is below 4 and current month `<=12`; it does not apply from M13 onward. This can reduce early review/performance pressure, but it only changes the effective performance value. It does not protect Health, trust/compliance, Dignity, Network isolation, or survival; nor does it waive the separate Skill/Output/Network/Dignity promotion conditions.

`HYPOTHESIS`：M1–M12 may provide room to build capabilities without every low computed performance immediately presenting as a sub-4 effective score. It is not evidence for automatic “Skill first” or delaying Output: Output remains both a performance input and a separate promotion input. At M13 the cushion ends; the M18 review is exposed to the ordinary formula.

Observed context is non-causal: v1 #1 promoted at M6 and M12 then M18; v1 #2 promoted at M6/M12 but missed M18; SCORE-01 transcript summaries report C at M6 and D at M18 while its compact timeline remains L1 through M23. These runs differ in choices, events, candidate metadata and evidence completeness. They cannot isolate the mercy's benefit or imply it caused a promotion / performance decline.

## 8. Leader talk / feedback loop

`DEV_CONFIRMED`：半年 Leader talk 发生在月度状态更新后、当月工资与 promotion review 之前。内部 talk score 不给 Agent 看，叙述从对应 tier 的 narratives 产生。配置 effects 为：good → Dignity+2、Network+1、HiddenRisk−1、当前 review performance adjustment +2；average → Dignity+1；bad → Dignity−2、Health−1、HiddenRisk+1、当前 review performance adjustment −2。精确权重、分档与 talk formula 属隐藏/半隐藏机制。

由此构成短反馈环：公开 Skill/Network/Output 等状态 → 半年 performance/talk → 可见叙述与 promotion result → 后续状态/资源变化。正式半年反馈具有明确 review 时点并先于晋升，适合作为重建 Planning 的阶段信号；普通故事中的表扬可能只描述局部事件，本审查没有证据证明它与 performance tier 等价。

历史 feedback 可读性有限：v1 #1 compact checkpoint 记有 first-half C / Leader 要求更清楚 Output；SCORE-01 的 C（M6）与 D（M18）是 Agent 对 transcript 的摘要，不是 score report 结构化 rating。其余 run 的正式 feedback 多为 `UNKNOWN`。因此正式反馈应触发一次 fresh observe 和 gap 重评，但不得从一句 narrative 推算 talk score、晋升概率或隐藏 strike，也不得把普通故事赞扬当成 review grade。

## 9. 晋升与生存的决策边界

S06-11 已确认的多通道边界继续适用：v4 #1 是 Health 累积耗尽；v1 #2 在终局 Health=10 时仍发生 trust-crisis terminal。只看 Health、分数或晋升都不足以代表安全。S06-11 的 pre-review/pre-quarter reserve、trend + shock + recovery timing 与 material trust/compliance/health review 不与本结论冲突；原始 review 为 [`S06-11_SURVIVAL_REVIEW.md`](S06-11_SURVIVAL_REVIEW.md)。

下一候选审查可使用以下**顺序性原则**（策略候选，不是实跑验证）：

1. 先排除当前公开证据支持的 terminal / material survival risk；安全是约束，不是默认最大化目标。
2. 在约束内维护下一次 review readiness，关注最近正式反馈、Level tenure 和可比较的公开状态变化。
3. 比较仍合法、与当前公开 bottleneck 有关的晋升路径及其剩余时间窗口；不因“有晋升可能”忽略 rapid-promotion / Network / Dignity 等公开成本。
4. 最后才比较次级得分增长与软成本。普通软成本不能单独压过有公共证据支持的高价值成长路径；真实 Material Risk 仍需审查。

这是一种 `HYPOTHESIS` 决策次序，不是具体月份动作日历或收益保证。执行它不会将隐藏分数权重或晋升阈值带入 Agent。

### Public-only Promotion Readiness proxy

建议输出的唯一分类为 `NOT_READY / BUILDING / PLAUSIBLE / STRONG / UNKNOWN`。输入只限当前 game session 的 fresh public observe：最近 Level / level age、Skill / Network / Output 方向和可归因 effect、formal half-year feedback、Dignity、S06-11 survival band、距下一公开半年 review 的时间。该 proxy 不是晋升概率或预测器，不含固定阈值。

| Label | 公开证据语义 |
|---|---|
| `NOT_READY` | 有 fresh 且明确的未解决 bottleneck / 不利 review feedback，当前路径仍未产生可比进展；不是基于隐藏条件判定。 |
| `BUILDING` | 至少有相关公开进展，但有可见落后项、刚晋升后新要求或反馈/效果尚未闭环。 |
| `PLAUSIBLE` | 多个相关公开信号持续改善，近期 feedback 不显示明确恶化，且当前没有明显的可见阻断项；不保证本次会晋升。 |
| `STRONG` | 最近正式 review、promotion outcome 与多项可比 public deltas 相互支持，且 survival band 不要求暂停普通成长；仍只表示证据一致，不是成功概率。 |
| `UNKNOWN` | freshness、session、前后 delta、review feedback 或候选状态不足/相互冲突；不能用缺失值补成 ready/not ready。 |

若数据不足以划清 `NOT_READY` 与 `UNKNOWN`，使用 `UNKNOWN`。Promotion result 发生后应重新评估，不能沿用旧 Level 的 ready 结论。

## 10. Candidate policy audit（不修改 v5）

以下至多是供 Main 决定是否写入后续静态候选审查的方向；`ADOPT_CANDIDATE` 不代表本任务实施、Main 接受或游戏验证。

| Candidate policy | Evidence | Runtime-visible inputs | Decision | Boundary / do not encode |
|---|---|---|---|---|
| 定性 Promotion Readiness proxy | Dev 半年 review 与公开 trajectory 的阶段差异；反馈缺失必须保留 UNKNOWN | fresh Level/age、S/N/O trends、formal feedback、Dignity、survival band、距 review 时间 | `ADOPT_CANDIDATE` | 只输出五态；不拟合概率、不编造阈值 |
| 每次 review 后重新诊断 Skill / Network / Output gap | v1 #1 M24/M30 Skill 落后，M33/M36 后重新晋升；需求随 Level 变化 | 最近同口径 public observe、observed effects、promotion result | `ADOPT_CANDIDATE` | 不使用 Dev 门槛表；不默认全面均衡或固定优先级 |
| formal half-year feedback 触发 Planning refresh | talk / performance / promotion 顺序与同日结果为 `DEV_CONFIRMED` | Agent 可读 feedback narrative、Level change、fresh state | `ADOPT_CANDIDATE` | 反馈是方向线索；不反推 talk score；普通 story praise 不等价 |
| review 前 survival reserve checkpoint | v4 M6 terminal 与 v1 #1 M6 Health 回补时序；S06-11 多通道边界 | fresh trend、公开 material warning、恢复可达性、下一 review/window | `ADOPT_CANDIDATE` | 延续 S06-11；不写固定 M5/M6 动作或 Health 数值 cutoff |
| promotion 后立即 reset Primary Gap | 每级门槛上升且发生 promotion Network 扣减；历史 v1 #1 随 Level 提升后再进入 plateau | actual new Level、promotion receipt、fresh post-review state | `ADOPT_CANDIDATE` | 重新诊断，不沿用旧 Level 的 gap/假定晋升已解决一切 |
| repeated path 用 observed effect 而非广告收益评估 | S06 #1 有重复无增长描述；v1 #1 同路径仍有不同阶段变化 | 同一 target 的可比较 before/after 与污染标记 | `ADOPT_CANDIDATE` | 符合现有 v5 phase-policy 假设；两次可比停滞才可标 STALLED；不把无增长归因到单项动作 |
| 将早期 promotion runway 纳入安全后的定性比较 | `DEV_CONFIRMED` 工资从次月按新 Level；同一转移较早具有更多付款月 | 当前 Level、公开月份、实际 paycheck / Wealth trend、风险成本 | `ADOPT_CANDIDATE` | 只作方向比较；不能超过 material survival constraint |
| 末段按精确工资/bonus NPV 做路径排序 | 数学机制存在，但未知未来存活、Tier、事件收入及隐藏评测关系 | 所需完整 payoff 并非当前公开信息 | `DEFER` | 不做精确收益预测、不将 salary table 变成 Runtime policy |
| 固定 Skill:Network 比值、M6/M12 必晋升或阈值追逐 | 指定同总量配对反驳简单 1:1 rule；Dev 门槛对 Agent 隐藏 | 不存在合规运行时输入 | `REJECT` | 阈值、比例、月→动作映射均 `DO_NOT_ENCODE` |
| 把 first-year mercy 写成自动 Skill-first / 延后 Output 策略 | mercy 只影响有效 performance；Output 仍参与 performance 与 promotion；历史无法隔离因果 | 可见当前状态/feedback，但看不到 mercy 分数 | `DEFER` | 可讨论能力投资，不建立 M1–M12 固定偏置 |

## 11. DO_NOT_ENCODE 与剩余未知

即使本地 `DEV_CONFIRMED`，也不得作为 Candidate runtime 规则：

- 精确 L1–L10 晋升门槛、performance gate、Level tenure、Skill/Network/Output clamp、rapid-promotion penalty 数值；
- Skill:Network 固定比例、performance polynomial / S-N softcap 比率 / 隐藏分数或从状态推导的精确 promotion probability；
- talk score 公式、tier cutoff、具体 bonus tier、用单句 narrative 反推隐藏 score；
- exact salary NPV、结局评分 weights、任何 `score-to-80` optimizer；
- 固定 `M6/M12/M18` 必晋升承诺、标题→选择答案映射、对单局事件的记忆化规则。

`UNKNOWN`：SCORE-01 终局 L2 的准确 promotion month；S06 #1 晋升月份/季度状态/feedback；v1 #2 M18 的 S/N/O/D/H/W 与 formal feedback；多局 performance structured score、具体 bonus tier；候选 Agent 是否真正使用 feedback、重置 bottleneck、遵守 survival ordering；隐藏 Test / cloud 迁移；以上策略对稳定 80+ 的因果效应。

## 12. Numeric analysis reproduction / verification

本次用根 `.venv` 中 `career_emulator.load_data.load_data` 只解码目标配置，没有实例化游戏、加载 event pool、创建 session 或写入 DB。性能几何与工资差可由以下短脚本重算；源文件 SHA 在下表。Python `round` 行为与模拟器函数保持一致。

```python
import json
import subprocess
from pathlib import Path
from career_emulator.load_data import load_data

root = Path(".venv/Lib/site-packages/career_emulator_bdci26/dev/dataset")
performance = load_data((root / "performance_score/config.data").read_bytes())
salary = load_data((root / "salary_conditions/monthly_base_salary.data").read_bytes())
promotion = load_data((root / "promotion/levels.data").read_bytes())
pairs = [(10,10),(15,5),(18,6),(20,10),(30,10),(30,20),(60,20),(60,40)]
si = performance["stat_interaction"]
for skill, network in pairs:
    low, high = sorted((skill, network))
    capped = min(high, low * si["softcap_ratio"])
    excess = max(0, high - low * si["softcap_ratio"])
    term = (capped + excess * si["softcap_factor"]) / si["normalize_factor"]
    balanced = (skill + network) // 2
    balanced_term = balanced / si["normalize_factor"]
    print(skill, network, term, balanced, balanced_term, term - balanced_term)

for rule in promotion["requirements"]:
    c = rule["conditions"]
    p = rule["optional_conditions"]["performance_score"]["threshold"]
    nchange = rule.get("stat_change", {}).get("network", {})
    nloss = -nchange.get("value", 0) if nchange.get("op") == "-" else nchange.get("value", 0)
    print(rule["from_level"], rule["to_level"],
          c["skill"]["threshold"], c["output"]["threshold"],
          c["network"]["threshold"], c["dignity"]["threshold"], p, nloss)

bases = salary["monthly_wealth_by_level"]
levels = [f"L{i}" for i in range(1, 11)]
for old, new in zip(levels, levels[1:]):
    delta = bases[new] - bases[old]
    print(old, new, delta, 6 * delta, 12 * delta)
for month in (6, 12, 18, 24, 30, 36, 42):
    print(month, 48 - month, (48 - month) * .3, (48 - month) * .5)

trajectory = json.loads(subprocess.check_output([
    "git", "show",
    "66ec4af1e9a2a28da57c6cb8d409a6a38f87ae01:experiments/S04-04-high-score-confirmation/candidate_run1_trajectory.json",
]))
states = {item["month"]: item for item in trajectory["monthly_public_state"]}
def base_performance(state):
    low, high = sorted((state["skill"], state["network"]))
    capped = min(high, low * si["softcap_ratio"])
    excess = max(0, high - low * si["softcap_ratio"])
    if si["hardcap"] >= 0:
        excess = min(excess, si["hardcap"])
    stat = (capped + excess * si["softcap_factor"]) / si["normalize_factor"]
    level_term = 0.0
    level = int(state["level"][1:])
    for coef in performance["polynomial_coefficients"]:
        level_term = level_term * level + coef
    return round(stat + state["output"] / performance["output_divisor"] + level_term)
for month in (23, 29, 41):
    score = base_performance(states[month])
    print("pre-review", month, score, "worst single-talk-adjustment", score - 2)
```

Target config identity (Dev package SHA256; same bytes in simulator package copy):

| Config | SHA256 |
|---|---|
| `performance_score/config.data` | `2f4058f2fd284b212c558a4e38ac1fe323cb54549ee40f45afa71c5a4e46427d` |
| `promotion/config.data` | `666af94867765caa28d2a9ed1746d005cce05d2e33670577ee1d78a267368cf9` |
| `promotion/levels.data` | `798395e300f121f79005f75f3784bd55b85b6fd7a22bb8122ad5dc6b04ab630f` |
| `salary_conditions/monthly_base_salary.data` | `e2abd826b47eb813cedb4e8c6f7b6b24c309bf4c6d799cad5747351e99795bbf` |
| `salary_conditions/half_year_performance_bonus.data` | `b1577df5b0a5cfff08c5429d8fd103a8f77de372f4d4f0cbc22437005dee49a5` |
| `talk_mechanism/config.data` | `3ef710d8c3b8027fcd0e7a467ea69acee67ab720537142ccac0267f1b0e3c050` |
| `initialization_n_regular/half_year_talk.data` | `64a788af7e9306f21f7c697fa39e7c41deb81cfe8ef664d8c519d8ccbe4be31c` |

### Verification summary

- Root facts: start `main == origin/main == ff171e67300131951f9b5da2ef2be3acd4b497de`; current state and Source Lock read; S06-11 boundary retained.
- Source identity: installed metadata confirms `career-emulator==1.0.1`, `career-emulator-bdci26==1.0.0`; all seven targeted Dev/config files byte-match the simulator materialized copies.
- Historical evidence: checked the referenced Git commit/path identities; compact source limitations and conflicting/missing promotion records are stated rather than resolved by guess.
- Numeric analysis: the formula and salary tables reproduce from the script above and exact target configs; no game/package test or live command was run.
- Change scope: exactly this review document; no candidate, CURRENT_STATE, Skill, Runner, dependency, runtime, raw log, DB, secret or `.env` change.
- Task Live Operations: Provider `0`; service start `0`; install/reload `0`; MCP `0`; `new_game` `0`; `observe` `0`; `take_action` `0`; Runner play `0`; full game `0`.

## 13. Recommendation

`RETURN_TO_MAIN_FOR_S06_13_QUARTERLY_ACTION_REVIEW`

No Skill/instruction, candidate, CURRENT_STATE, or Main Game Gate authorization was changed by S06-12.
