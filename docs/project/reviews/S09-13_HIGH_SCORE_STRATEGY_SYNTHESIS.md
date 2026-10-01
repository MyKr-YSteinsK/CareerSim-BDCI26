# S09-13｜高分策略静态总审查

## 1. 身份、结论与证据边界

- Status：`OFFLINE_STRATEGY_SYNTHESIS_COMPLETE`；Plan Stage=`S09-Lab｜高分策略重构`，不代替 Stage 验收。
- Base：`main@589725ac2db0d62d2da53353cb5680f971fb88fb`；Candidate=`candidate-v8a-v7o-donor-core-transplant`。
- Primary bottleneck：`GROWTH_EXPLORATION`；secondary=`OPPORTUNITY_CAPTURE`。这是最值得验证的可控缺口，不是已识别的主要分数损失原因。
- `NEXT_STRATEGY_HYPOTHESIS=ADAPTIVE_OPPORTUNITY_CAPTURE_WITH_BOUNDED_UNTESTED_PROBE`。
- Decision **B**：`ADAPTIVE_OPPORTUNITY_CAPTURE_READY_FOR_IMPLEMENTATION`；返回=`S09_13_ADAPTIVE_OPPORTUNITY_CAPTURE_READY_RETURN_TO_STAGE`。Ready 指可交给 Stage 决定单一 delta 的实现与实验，不代表已提高期望分数。
- Submission implication：`INSUFFICIENT_EVIDENCE_TO_REPLACE_V8A`。静态设计不能取代已有 Candidate，更不构成 official submission 合格认证。

本任务只到 Evidence → Hypothesis → Strategy Design Recommendation。Candidate/四 Skills/manifest/validation flags/Runner/依赖/retry 不变；provider/service/install/Runner play/MCP/DB/game 操作均为 **0**；`NEXT_GAME=NOT_AUTHORIZED`。

**FACT** 是来源可核对的公开状态、选择或合法 Dev score report；**DESCRIPTIVE ASSOCIATION** 是跨运行共现/前后变化；**HYPOTHESIS** 是待实验的机制；**RECOMMENDATION** 是下一步设计；**UNKNOWN** 是没有充分证据。下文 Supported 不意味着随机化因果识别。未使用 simulator hidden state、private scoring internals、event ID/title 答案索引或隐藏阈值；Dev component points 仅做离线记账，不进入 runtime 权重。

### 来源与可比性

复用 [S08-11](S08-11_HIGH_SCORE_CORE_RECOVERY_FORENSICS.md)、[S09-02](S09-02_FAILURE_FLOOR_HIGH_SCORE_JOINT_FORENSICS.md)、[S09-09](S09-09_M6_PUBLIC_SIGNAL_DISCRIMINANT_FORENSICS.md)、[S09-11](S09-11_V8A_V7O_TRANSPLANT_FIDELITY_REVIEW.md)、[S09-12](S09-12_V8A_TWO_SAMPLE_TRAJECTORY_DIVERGENCE_REVIEW.md)；紧凑数值/行号见 [evidence matrix](S09-13_HIGH_SCORE_STRATEGY_EVIDENCE.json)。本次只定向补读终局 score components 与 v8a M25–48，不重建无关历史。

- 核心 9 runs，加必要 failure controls 5 runs，共 **14**。v1 两局为 Tier B Git 历史摘要，单步响应/完整 Delivery/首次 warning lead time 不可恢复；其余 12 runs 有 Tier A public events，正式 run notes 补充结果。
- v1 对照同 Candidate/source；v8a 两局同策略。其余 Candidate、runtime adherence、曝光、状态和历史不同，均非受控因果比较；不把 14 个样本当独立同分布抽样。
- 终局 public state 与 M48 月内最后状态分开；自然 48m completion 的最终结算观察可显示 M49。public Wealth 使用公开整数，score report 中更细 raw 值不替换它。
- v7t 有 18 个 action→observe 缺口；批量变化不作 clean response。v7w 有未分类回执；v1 稀疏状态不插值。所有原 `FORENSIC_HOLD` 保持 ACTIVE。

## 2. A｜终局结构

Risk 列是**已有合法 Dev report 的 risk-control component points**，不是 Agent 可读 risk counter；UNKNOWN 不按零计。H/D 为 public Health/Dignity，不能等同完整 resilience 计算。

| Run | Score | Survival | Grade/Level | Skill | Network | Output | Wealth | H/D | Risk component | Promotion months |
|---|---:|---:|---|---:|---:|---:|---:|---|---:|---|
| v1 #1 | 76.04 | 48m | A/L6 | 139 | 52 | 42 | 40 | 9/10 | UNKNOWN | 6/12/18/36/48 |
| v6 | 75.29 | 48m | A/L6 | 142 | 58 | 42 | 39 | 7/10 | 10 | 6/12/18/36/48 |
| v7o | 71.83 | 48m | A/L5 | 130 | 53 | 37 | 43 | 9/10 | 8 | 6/12/18/36 |
| v8a RUN07 | 72.65 | 48m | A/L5 | 119 | 54 | 35 | 35 | 10/10 | 10 | 6/12/24/42 |
| v1 #2 | 35.31 | 25m | D/L4 | 44 | 20 | 14 | 3 | 10/8 | 0 | 6/12/24 |
| v8a RUN08 | 59.00 | 48m | C/L4 | 82 | 36 | 26 | 29 | 8/10 | 10 | 12/18/36 |
| v7t | 65.71 | 48m | B/L5 | 101 | 38 | 30 | 27 | 10/10 | 10 | 6/12/30/48 |
| v7v | 58.97 | 48m | C/L5 | 100 | 37 | 33 | 25 | 10/10 | 4 | 6/18/30/48 |
| v7g | 54.52 | 48m | C/L5 | 102 | 36 | 32 | 19 | 6/10 | 4 | 12/18/30/48 |
| v4 | 25.84 | 6m | E/L2 | 11 | 7 | 6 | 2 | 0/9 | UNKNOWN | 6 |
| v7d | 17.02 | 15m | E/L1 | 9 | 3 | 2 | 0 | 6/9 | UNKNOWN | — |
| v7q | 26.80 | 24m | E/L1 | 9 | 0 | 3 | 5 | 8/7 | UNKNOWN | — |
| v7w | 30.31 | 24m | D/L2 | 9 | 2 | 3 | 6 | 8/7 | UNKNOWN | 24 |
| v7x | 19.82 | 8m | E/L1 | 9 | 3 | 3 | 3 | 0/7 | UNKNOWN | — |

**DESCRIPTIVE ASSOCIATION：** 四个 70+ runs 全存活 48m，L5/L6、S119–142、N52–58、W35–43；较低的完整 survivor 为 S82–102、N36–38、W19–29。资本积累的差异比“是否把 Health 补到 10”更稳定；L5 同样包含 54.52、58.97、65.71、71.83、72.65。不是 Skill/Network/Wealth 的充分条件，也未控制随机曝光/级别历史。

**FACT：** 可用合法 component lists 包含 Level、Wealth、Resilience、Skill、Risk control、Network，未列 Output。结论只到 `OUTPUT_APPEARS_INSTRUMENTAL_IN_OBSERVED_DEV_SCORE_REPORTS`；Output 可参与公开反馈、交付与晋升，隐藏 Test 的直接计分地位 UNKNOWN。v7o archive 的 score_report 终局部分为空，使用同一 exact events 的终局 observe ending_score；v1 #1 未取得本轮可用分量，保留 UNKNOWN。

**DESCRIPTIVE ASSOCIATION：** RUN07/RUN08 相差 13.65，Dev 分量差主要分布于 Level、Skill、Network，另有 Wealth/Resilience；Risk component 相同。v7t/v7v 相差 6.74，却有 Risk component 6 点差，说明仅以 public S/N/O/H 解释所有分数差不成立。分量记账不识别哪个动作造成差异，不推出 cleanup 次数目标。早退同时缩短资本积累时间；终局资源差不能全部解释为策略效率。

## 3. B｜晋升与 Review-window 目标

**DESCRIPTIVE ASSOCIATION：** v1#1/v6/v7o 的 M6/M12/M18 晋升链与之后较快资本增长共现；RUN08 M4–11 S/N/O 停在 9/3/3，M12 Level 改变后 Output 又增长。较早 Level 与响应/机会变化相伴，但 Level、本局历史与时间共同变化，未证明 Level 单独解锁任何上限或事件。

**反例：** RUN07 M18 未晋升，M24/M42 恢复，仍达 72.65；v1#2 M6/M12 晋升仍在 M25 trust terminal；v7v M6 晋升仍为 58.97。[S09-09](S09-09_M6_PUBLIC_SIGNAL_DISCRIMINANT_FORENSICS.md) 还存在相同 pre-Review public snapshot、相反 promotion label。不存在已识别的 M6 必胜规则。

**HYPOTHESIS：** Promotion 可视为资本与机会的 compounding multiplier，而不是可直接命中的独立按钮。**RECOMMENDATION：** runtime 以每个 Review window 可验证职业资本/实际成果增长、明确反馈缺口与近期 Delivery 为决策依据；保留晋升 ambition，miss 后仍 A，避免把“最大化未知晋升概率”变成单一 Output 排序。该目标与晋升相容，收益 UNKNOWN。

## 4. C｜Score-Leverage Map

“直接”仅指已观察 Dev report；控制程度是可选择合法动作，不保证实际增益。终局变量也是过程中可帮助下一机会的资本；不是互斥类别。

| Leverage / 角色 | Direct score evidence | Promotion / capital evidence | Survival evidence | Downside | Controllability | 当前 v8a handling / confidence |
|---|---|---|---|---|---|---|
| Level / 终局+中介 | 有分量 | 早期链与后续增长共现；miss 可恢复 | 不能阻止 trust/resource terminal | 追未知阈值可 tunnel | 间接；Review 不可操控 | ambition 保留；不保证晋升；中 |
| Skill / 终局+资本 | 有分量 | 高分组更高；合法学习/技术责任有公开价值 | 单独不足保生存 | 时间/Health/Delivery 成本 | 选路径可控，响应不确定 | broad prior 有，未测试路径 fallback 不明确；中 |
| Network / 终局+资本 | 有分量 | 高分组更高；mentor/coordination 可扩机会 | trust 与关系数不等价 | 维护无响应/关系代价 | 局部响应可观察 | local NO_GAIN 已有，不能概括所有 ownership；中 |
| Wealth / 终局+经济选择权 | 有分量 | 晋升/收入与积累共现，非单一选项收益 | v7d W0 后仍存活数月，不是死亡阈值 | 花费/收入中断 | 消费部分可控，收入间接 | binding affordability 原则合理，late 捕获未知；中低 |
| Health/Resilience / 终局+连续性 | 有分量；H 不是完整分量 | 维持可行动期，补满不等于资本增长 | v4/v7x H0；v1#2 H10 仍终止 | 过度恢复侵蚀成长；过少可早退 | 合法恢复菜单/时间有限 | 两个 v8a full runs 存活，非稳定下限证明；中 |
| Risk/trust / 连续性+终局 | 有 risk-control 分量 | 保护既有资本转化，具体收益未识别 | v1#2 repeated trust terminal | 无 fresh warning cleanup 或合规冒险 | 只能用公开 warning/语义 | 保留有界 gate；notes hidden-risk/cap 推断不合格；中低 |
| Output/results / 主要 instrumental | 未列直接分量 | feedback/交付/可见成果；更多 Output 动作不单调高分 | progression continuity 可能相关 | 无响应重复、挤出 S/N/Delivery | 局部响应/结果可核对 | RUN08 M42 重复停滞，需 fallback；中 |
| Ownership/responsibility / instrumental | 未列直接分量 | donors 广泛采用；完成CI也有 no-promotion | 可改善收入/绩效，但压力风险 | 责任过载/承诺未兑现 | legal opportunity 可选，结果未必可选 | Main prior 保留；兑现链因果未验证；中低 |
| Delivery certainty / instrumental+连续性 | 未列直接分量 | 保护近期承诺与真正 result，不等于 tool success | 避免明确破坏近端交付；完整 floor 效应未知 | 伪任务/过度保守 | 只对真实 public item 可控 | tracking/parser/overclaim 限制仍在；低 |

## 5. D/E/G｜响应、机会捕获与有界探索

### 可以成立的公开证据

1. **FACT，S09-12：** 16 对完整公开 description+legal choices 匹配中 15 对同选；9 对同选且两端 clean 的样本里 5 对 S/N/O 响应不同。M1 曝光已分歧；不能把低分全归于排名，也不能假定相同 choice 的收益稳定。
2. **FACT，RUN08 M9/a37：** notes 将 Output/Network 归纳为 NO_GAIN，后续连续 Health 恢复；当时合法 Skill 学习仍未测试。Health 5→7→9 的保护价值不能事后抹掉，但没有证据证明 Skill 被实际比较；是否当时应放弃恢复 UNKNOWN。
3. **FACT，本次定向补读 RUN08 M42/L4：** a177 与 a178 同为准备汇报材料，公开 O26→26→26；两次之间有 fresh observe，非批量 mixed。a178 前 E2，Skill 学习 cost2 的合法菜单仍在，L4 内未测试该 Energy family。a179 人脉维护 N35→36。下一次机会并非只有停滞的 Output。
4. **FACT，RUN08 M48/L4：** a203 首次 L4 Skill Energy，S80→81/H9→8/E3→1。只能说明 M48 该路径有公开响应，不能把它回填成 M42 已知 GAIN，更不能断言提前改选会晋升。
5. **FACT，RUN07：** M39/L4 a162 Skill 学习 clean GAIN，之后 a164 选择轮岗；后者跨月变化不作独立 Skill 因果。其 notes 中“封顶/解封”解释不被采纳，支持的是公开路径选择与响应，不是推理合规认证。
6. **跨运行反例：** v7o Skill Energy 4 次均观察 GAIN；v6 没有 Skill Energy 仍 75.29，v1#1 后期偏 Output 仍 76.04。因此不支持定额探索、固定 Skill 或强行平衡。RUN08 低分仍在 M48 探索，不支持“高分者探索、低分者不探索”的二分。

行号均为 exact events 的 before-observe / action-call / after-observe：RUN08 a177=`1435/1437/1443`，a178=`1443/1445/1451`，a179=`1451/1453/1459`，a203=`1643/1645/1651`；RUN07 a162=`1329/1331/1337`。Public menu 用来核对当时机会，action ordinal 仅定位，不作为 runtime 答案索引。clean 为同月同 Level、单行动后 fresh observe 且无 intervening event feed 的描述性归因范围，不是干预证明。

### 当前契约与真正新增的 delta

v8a 已有 broad compounding、local NO_GAIN 降权、保留多维价值、UNKNOWN 开放、Level-change 重开，以及存在已知 responsive alternative 时不立即重复。不能把这些包装成新机制。缺口是：**没有已知 responsive alternative 时，未测试但高价值的合法 growth family 是否应被明确纳入比较**。RUN08 M42 给出窄而具体的决策歧义；即便该窗口的分数影响 UNKNOWN，也值得提出可证伪设计。

**RECOMMENDATION：** 先利用当前 session/Level 公开响应好的高价值路径；当前拟继续的路径有 fresh clean local NO_GAIN、没有已知更优 responsive path、且有语义支持的合法未测试高价值路径时，将**一次 bounded probe**与当前最佳候选比较。必须仍比较承诺/visible result/多维收益和普通成本；material survival/compliance 或 near-term Delivery binding 时保护优先。探测后 fresh observe，只更新该 Level/context/family/dimension，不自动继续探索，不把 UNKNOWN 当 GAIN、不推 global cap。

探索是可选候选而非强制动作；已有 responsive 高价值主线不为覆盖率让路。一次 probe 后只有新的公开证据才支持下一次选择；保留 max-two-candidates 与一次 action→fresh-observe 的既有效率边界。不引入 exploration budget 账户、Bandit 算法或新 Skill。

**E 分类：`SUPPORTED_DIRECTION`。** 局部停滞后显式比较未测试机会的方向有跨 run 支持；它比目前仅“存在 responsive alternative 则切换”的语言更明确。能提高 hidden Test 期望 score 的机制仍 **PLAUSIBLE**，收益幅度 **UNKNOWN**。Simulator 不是已知 bandit：响应受状态、历史、事件与时间共同影响，不估计固定 arm reward、不用终局分数训练事件答案。

**G：** responsive multidimensional portfolio 可作为选择原则，不设 S/N/O 配比，不让单 gap 消灭其它响应路径；local NO_GAIN 不否定另一 family 或同一动作其它价值。`LEVEL_CHANGE_REOPENS_OPTION_VALUE` 有 RUN08 M12 的响应恢复支持，保留为 v8a 既有规则，不作为第二个新增 delta；不保证 Level 必然带来 GAIN。停滞换路径优先有已知响应的 alternative，之后才比较 untested probe；仍可因 near Delivery/多维价值选择原路径。

## 6. F｜Ownership → realization → visibility

**DESCRIPTIVE ASSOCIATION：** v6/v7o 前 M18 Main 都 6/6 key project；整局 v6/v7t/v7v 同为 14/16，v7o 10/16，却有不同分数。因此“多申请项目”不是单调机制。技术 ownership、mentor、协调、汇报和实际成果可构成跨 Main/Story/Energy 的 outcome cycle，但 title/菜单选择本身不能证明 ownership 已取得或结果已兑现。

**FACT/限制：** S09-09 有完成 CI 仍不晋升的 controls；S09-12 的高管汇报匹配对既有相同响应也有不同响应。RUN07 M9 有公开 CI 结果后的汇报选择，而两局 Delivery 基础不同。低分 survivors 更高 Output Energy share，却更少终局资本，支持检查“visibility 投入而资本未增长”；不证明它们缺 realization 或 delivery。各 donor 完整责任→成果→可见→下一机会链无法逐项闭合，ownership-but-no-realization / realization-but-no-visibility 的频率 **UNKNOWN**。

`OWNERSHIP_TO_REALIZATION_LOOP=PLAUSIBLE`。保留现有真实 public item 的兑现 prior，不能制造任务、claimed 当 verified、或把 tool success 当职业结果。H3 的 tracking/循环强化可能有效，但当前直接缺口证据弱于 H2，不作为本次推荐；不固定 key project/CI/mentor/高管汇报答案。

## 7. H｜M24–48：资本继续累积，不推出固定终局切换

统一取对应月**最后 public observation**，格式 `L; S/N/O; W; H`。这些不等于 Review 瞬间，更不等于最终结算状态。

| Run | M24 | M36 | M48 |
|---|---|---|---|
| v1#1 | L4;63/36/26;10;8 | L5;100/36/29;21;9 | L6;138/51/40;39;9 |
| v6 | L4;61/30/26;11;8 | L5;102/39/24;22;8 | L6;141/57/40;38;7 |
| v7o | L4;47/32/26;13;10 | L5;94/38/27;25;10 | L5;129/51/37;42;9 |
| v8a RUN07 | L4;45/21/19;9;9 | L4;85/35/25;19;9 | L5;118/54/33;34;10 |
| v8a RUN08 | L3;42/20/9;8;10 | L4;45/21/17;15;10 | L4;81/36/26;28;8 |
| v7t | L3;42/21/14;11;10 | L4;71/34/26;17;10 | L5;100/37/28;26;10 |
| v7v | L3;41/21/13;6;10 | L4;60/27/26;7;10 | L5;99/36/31;24;10 |

**DESCRIPTIVE ASSOCIATION：** 高分 donors 在后半程继续拉开资本，但 RUN08/v7t/v7v 也持续增长；不是“低分后半程停止成长”。RUN07 M24→36 在同 L4 S45→85，而 RUN08 跨 L3→L4 S42→45；Level 标签不足以解释增长，实际机会响应值得跟踪。晋升→更高收入/成长是合理中介假设，具体速度贡献 UNKNOWN。

本次 late Energy（M25–48）：RUN07 Output9/Health5/Network4/Skill1/cleanup2，RUN08 Output12/Health5/Network3/Skill1/cleanup1；Main 为 RUN07 key-project5/mentor1/avoid1/rotation1，RUN08 key-project8。clean Energy response：RUN07 O8 GAIN/1 NO_GAIN、N2/2、S1 GAIN；RUN08 O9/3、N2/1、S1 GAIN。两局 Health 恢复同为5，不能以“RUN08更多恢复”解释分数差；更多 Main/Output 也未换来更高终局资本。

Output tunnel 的局部事实是 RUN08 M42 立即重复 NO_GAIN（另有 v7t M42 重复停滞）；v7v 后段 Review Plan 可观察连续性不足，不能把 UNKNOWN 当确证 stale plan。没有可核对的 missed-Wealth opportunity 全链；无证据以 L4/L5 固定降低 ambition。`LATE_GAME_CAPITAL_CONVERSION=PLAUSIBLE`：存活较稳时应继续比较能留下资本的响应路径，但继续晋升与直接资本可兼容。H4 独立 terminal-mode、月份/Level 切换或剥夺 Output 的必要价值都未获支持；本次 H2 可作用于任何窗口，无需新增 late mode。survivor-only 比较存在选择偏差，不代表早退 run 后期反事实。

## 8. I｜最小必要保护与失败下限

**FACT：** v1#2 有早晋升、H10，仍 M25 trust terminal；v4 曾局部恢复，却因连续 attrition 到 H0；v7x 没有长期 S deadlock 也早退。v7d W0 不立即结束，v7q/v7w H/W 未归零仍自然终止。Health buffer、资本成长与合规/trust 连续性必须分开检查，不能推死亡阈值。

**RECOMMENDATION：** 保留 `MINIMUM_NECESSARY_PROTECTION`：fresh public material constraint → 最小合理修复/遏制 → fresh observe → 已解除则回 A。普通成本不自动 S；poor grade/no-promotion 通过 A 修复；明确 trust/compliance warning 与近端 Delivery 仍约束探索。v1#2 cleanup M18/21/24 后仍失败，不支持增加 cleanup 次数，更无法恢复缺失的首次 warning lead time。

哪些保护“真正必要”的反事实仍 UNKNOWN；acute symptoms、公开法规/保密/信任威胁是必须尊重的可见边界。晚期补满与成长争用可能吞掉复利，但 v8a 两局早期 Health recovery count 同为4、late 同为5，不能据此把 protection 定为 primary bottleneck。保留 `PREVENTIVE_OPTIONALITY_NOT_YET_PRIMARY`；无新证据支持固定 reserve、shock-envelope threshold 或常驻 preventive mode。

## 9. 四种设计的比较与 counterfactual stress review

以下是 **4×10 手工静态情境推演**，不是新游戏、程序测试、模拟器预测或 effect proof。H1 指当前书面 v8a；H2 指只加有界未测试路径比较；H3/H4 只比较设计，不授权实现。所有方案共享现有 safety/Delivery/runtime shell。

| Family | 最强依据 | 主要缺口/回归 | 本次处理 |
|---|---|---|---|
| H1 unchanged | 2/2 48m，单局72.65，donor移植忠实度有证据 | 响应停滞且无已知 alternative 时 fallback 模糊；2局不证明稳定 | 保留当前基线，单独授权 Sample3 仍可有信息价值 |
| H2 adaptive capture | v7o/RUN07 probe GAIN，RUN08 M9/M42机会未充分比较；局部NO_GAIN有反例 | 无收益probe、挤出Delivery/稳定化、变quota | **唯一推荐，Planning-only单delta** |
| H3 realization loop | 责任/成果/汇报是合理跨工具价值链 | 完整链缺失，伪任务/记账开销/固定项目 | PLAUSIBLE，不实施 |
| H4 late conversion | 高分S/N/W终局更高；late Output重复NG | survivor偏差；错误停晋升/低估Output | PLAUSIBLE，不实施 |

| Archetype | H1 unchanged | H2 adaptive capture | H3 realization loop | H4 late conversion |
|---|---|---|---|---|
| 1 early promotion + strong response | exploit广泛成长 | 同H1，不为quota探索 | 有真实item才跟兑现 | 不提前进入terminal偏好 |
| 2 no M6 + stagnation | A修复gap；unknown fallback不明确 | 排除binding后比较一次untested高价值probe，不保证晋升 | 检查实际成果，不能假造缺项 | 早期仍capital/Review，不用late规则解M6 |
| 3 Output NG + untested Skill | local折价，但可能继续gap路径 | Skill只作为候选，与成本/多维/Delivery比较 | 必需成果可使原路径仍有价值 | 能重视Skill，但不因Output非直接分量彻底弃用 |
| 4 Network NG + ownership | 其它family价值保留 | ownership公开高价值可优于同family重复；不强学Skill | 真实责任接入兑现，避免过载 | 不应只按终局Network否定ownership |
| 5 high Skill / weak Network | gap+多维比较 | responsive N优先；untested N不是保证收益 | 协调/mentor只凭当前语义 | N资本方向可行，禁止固定比例 |
| 6 high Network / weak result | 保护Delivery/visible result | 有响应result路径则exploit，避免为探测牺牲交付 | 兑现链最贴合，但不把N视为已实现result | 终局维度偏好可能轻视Output，是回归风险 |
| 7 L3/L4 promotion miss | A继续，无S自动化 | 局部NG后换响应或比较probe，不宣称cap | 依据公开feedback修兑现，不杜撰threshold | 不因miss宣告晋升结束 |
| 8 thin H / no acute threat | fresh binding判断；普通成本可接受 | 不以“无acute”忽略material资源约束；明确cost再比较 | 不新增责任造成公开不可承受负荷 | stable survival未证，不机械转capital |
| 9 explicit compliance/trust threat | public warning bounded containment | 同H1，探索让位于明确constraint | 合规兑现优先，不能把visibility当豁免 | 同H1，不用高资本掩盖trust threat |
| 10 late high Level / stable survival | broad成长+Review仍继续 | exploit响应资本；NG时可probe，保留机会晋升 | 真成果转下一个机会，tracking须有证据 | 最匹配H4；月份/Level硬切换仍未支持 |

结果：H2 可覆盖早期与后期停滞且不要求新模式；最大的静态回归点是把“比较 probe”误写为“必须探测”，或者用一次 NG 删除多维/near-delivery 价值。H2+H3/H4 仅设计上相容；本次不推荐多 delta bundle。

## 10. High-score causal map 与唯一下一假设

| Status | Evidence → mechanism claim | 可用结论/限制 |
|---|---|---|
| Supported | 高分终局较高S/N/W；Dev有对应分量 | outcome structure/记账支持；增加动作的因果收益未识别 |
| Supported | 同选不同响应、local NG与Level变化后响应恢复 | 公共响应需持续观察；不能用event答案或全局cap |
| Supported | promotion不能代替floor；局部有未充分比较的机会 | 保存约束，明确uncertainty fallback有设计依据 |
| Plausible | 早晋升放大后续资本/机会；窗口成长促进晋升 | 双向中介，未识别promotion单独effect |
| Plausible | 响应利用+有界探索减少停滞投入 | 单delta值得实现后实验；期望分数/下限收益UNKNOWN |
| Plausible | ownership→result→visibility；late durable资本转化 | 保留为次级设计，不捆绑实现 |
| Unknown | hidden Test规则/分布、promotion threshold、最优H buffer | 不写runtime公式；2个v8a样本不能估稳定性 |
| Unknown | 曝光与策略各自贡献多少13.65、M42改选反事实 | S09-12 exogenous-first证据顺序保留；未分解causal份额 |
| Rejected | key-project固定答案、更多Output必更高分、固定S/N/O均衡 | 有反例；不变成新quota |
| Rejected | 一次NO_GAIN=全family/global cap；miss必崩；满H保生存 | 有公开反例/不足证据；hidden推断不可采纳 |

### 单一 hypothesis card

- **Evidence：** S09-12 M9 的未知 Skill path、RUN08 M42 fresh O NO_GAIN 后立即重投、RUN07 M39/v7o Skill GAIN；v6与RUN08自身是禁止定额探索的反例。
- **Expected mechanism（HYPOTHESIS）：** 当 exploit 缺乏已知响应路径时，以一次语义支持的未测试高价值候选取代默认重复停滞/无 binding 的额外恢复的惯性；fresh observe 提供局部学习，改善不同曝光轨迹中的机会利用。不是解释全部分数差。
- **Minimal delta（RECOMMENDATION）：** 只在现有 Planning local-response 排序中补充上述 uncertainty fallback；保留既有 broad growth、Level reset、two-candidate limit、Review/Delivery/protection 以及 runtime shell。无需新增 Board字段、Skill、manifest kernel 或探索状态机。本任务未实施；未来若确需同步身份/包元数据须由新 Plan 明列，不自行扩大。
- **Regression risk：** 探测无增益且消耗Health/Energy、挤出近期成果、把一次NG过度降权、以quota持续探索、增加deliberation。public cost/near-delivery/已知responsive alternative 必须进入同一次比较。
- **Falsification condition：** 在未来另行授权的 run 中，若 eligible stall+untested opportunity 窗口确实出现并且机制被执行，却重复选择无职业价值probe、没有观察到响应改善、或造成明确Delivery/生存/合规回归，应否定/缩窄该机制；若只改变措辞未改变 eligible decision，实施未形成处理差异；若窗口未出现则 NOT_EXERCISED，不能写成功。单局最终低/高分本身不识别机制成败，多样本期望收益需独立预算。
- **Minimum validation evidence（未来，未授权）：** eligible窗口的before/menu/成本/选择/fresh-after，local GAIN/NG、与原最佳候选差异、重复停滞次数、Review/资本、near Delivery/survival/runtime回归。不得为了本报告开局或固定事件重放。

相较 S09-12 的 frozen Sample3 建议，本次新增跨 run synthesis 与 M42 具体 eligible ambiguity，使 **H2 最小实现值得 Stage 评审**；不推翻早期 exogenous divergence 判断，也不强制跳过 unchanged replication。当前 v8a 保留，替换 submission 的证据不足。

## 11. 交付与验证

只新增本报告和一个 public-only compact JSON，CURRENT_STATE 只加一条 durable delta。JSON 汇总来源、公开终局、合法 report 分量、统一 late checkpoints、定向行号；无 raw logs/config/DB/凭据或 event-to-answer 表。历史身份 hash 复用既有登记，本次不重算旧 raw hashes，也不删/搬来源或解除 hold；ignored scratch 是可重建派生物，唯一 raw 仍在既有 run 位置。

验证范围：JSON parse、14-run/9-core cohort 与 required 4×10 情境覆盖核对、相关 source/link 存在性、选定 new line references、增量 secret scan、`git diff --check`。未重跑历史 tests，未做 provider/runtime/game/隐藏 Test 验证。交付 commit/push/clean 由最终 TASK_RESULT 和 Git 给出，不在报告自引用 commit。

`Candidate changed=NO`；`live operations=0`；`NEXT_GAME=NOT_AUTHORIZED`。
