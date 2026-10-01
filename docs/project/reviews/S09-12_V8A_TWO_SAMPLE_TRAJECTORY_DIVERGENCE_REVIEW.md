# S09-12｜v8a 双样本轨迹分歧归因审查

## 结论与范围

- Status: Complete；base=`main@4fb189209595e4733521c45c46099e18d570296d`；Candidate=`candidate-v8a-v7o-donor-core-transplant`。
- 主结论 A：`EXOGENOUS_TRAJECTORY_VARIANCE_DOMINANT`；返回 `S09_12_EXOGENOUS_VARIANCE_DOMINANT_RETURN_TO_STAGE`。
- INFERENCE：在可比公开描述/合法选项中，选择高度一致；不同事件时序、资源/Level 路径和同选项的公开响应差异，是本次早期分歧更有力的解释。这里的 dominant 是证据排序，**不是 13.65 分差的因果份额**，也不证明所有后续暴露均独立外生。部分 follow-up 是先前选择的分支，promotion/response 的内部原因仍 UNKNOWN。
- RECOMMENDATION：下一边界为另行授权的 `FROZEN_V8A_SAMPLE3`。本任务不提出/实现 v9 candidate：没有重复、material、完整可比输入下的 choice drift 证据满足设计门。`PREVENTIVE_OPTIONALITY_NOT_YET_PRIMARY`。
- 离线范围仅 M1–M18；没有延伸到 M24 或逐动作审计完整48月。Candidate、四 Skills、manifest、Runner、依赖、retry、parser、validation flags 均未改；live operations=0；`NEXT_GAME=NOT_AUTHORIZED`。

## 证据身份、时点与归因方法

| Run | 完整 run window（UTC） | 本次 public observe window（UTC） | exact events / transcript stem |
|---|---|---|---|
| RUN07 | 2026-10-01 11:39:58.310740–12:51:10.411189 | 11:40:13.439035–11:55:49.773217 | `20261001T114001Z` |
| RUN08 | 2026-10-01 13:22:27.041969–13:54:42.775557 | 13:22:44.163329–13:35:48.731290 | `20261001T132230Z` |

目录为 `D:\CS\CareerSim\.career_sim_runner\career_emu\outputs\local-s06-adaptive-controller\<stem>\`；文件分别为 `events-<stem>.jsonl` 与 `transcript-<stem>.log`。来源/hold/原始 hashes 见 [RUN07](../runs/v8a-full-horizon-sample1.md)、[RUN08](../runs/v8a-full-horizon-sample2.md)。本次两份 events SHA-256 均与既有 hold 记录 MATCH；未重建历史 cohort。逐项读取白名单 public status、description、legal choices 和公开 feed；same-session action notes 只解释当时排序，隐字段及其数值不进入归因。

每局去重后 M1–M18 各77个 actions，含开始游戏、54个 Story、16个 Energy、6个 Main；第一至最后 M18 observe 为 events 行27–635。59对相邻动作观察满足同 month、同 Level、after feed 为空，作为局部 clean response 候选；18对跨月/包含其它公开 feed，标 MIXED，不当作 clean effect。M18 Main 的后观察已在 M19，排除其 delta。Story 选项通常仅公开动作文本，没有逐维 advertised 数值：不得把后验 GAIN 反写成事前高收益广告。新事件的呈现本身也不证明原因机制；此处 clean 是可见流内的局部归因边界。

匹配键是**完整公开 description + 完整白名单 legal choices**，不使用 event ID，也不靠 title 判同。匹配不等于状态/历史已控制。辅助 [compact evidence JSON](S09-12_V8A_TWO_SAMPLE_TRAJECTORY_DIVERGENCE_EVIDENCE.json) 保存16对 Story 的 action/month、三段行号与公开 delta；本地派生投影在 `.local/scratch/s09-12/public-pairs.json`，原始唯一来源仍在既有 FORENSIC_HOLD。

### 统一 checkpoint 口径

Plan 的 RUN07 state 是 Review 月最后观察，RUN08 是正式 Review 后首次观察，不能直接作为同时点分解。本次保留历史记录，额外对齐两种时点；末观察在季度 Main 跨到下一月之前。

| Review | RUN07 first H/D/W/S/N/O；Level | RUN08 first H/D/W/S/N/O；Level | RUN07 last S/N/O | RUN08 last S/N/O |
|---|---|---|---|---|
| M6 | 3/10/2/9/3/3；L2 | 5/10/3/9/3/2；L1 | 12/5/6 | 8/3/3 |
| M12 | 7/9/3/21/4/6；L3 | 8/10/3/9/3/3；L2 | 22/3/5 | 13/4/6 |
| M18 | 9/10/5/41/11/15；L3 | 9/9/5/21/4/6；L3 | 42/12/16 | 24/5/8 |

M18 同首次观察 gap 为 S20/N7/O9；同末观察 gap 为 S18/N7/O8。原 Plan 的 S21/N8/O10 混合口径差距方向成立，但幅度不适合作统一分解。M6 grade 都 C，只有 RUN07 晋升；M12 为 RUN07 B/L3、RUN08 C/L2；M18 都 B/L3，RUN08 此时才进入L3。

## A｜Earliest material divergence

`EARLIEST_MATERIAL_DIVERGENCE=M1 / a2 起的首次 Story opportunity window`（两局 observe/action/after 行35/37/43）。相同初始 H5/D5/W1/S1/N1/O0/L1 下，RUN07 获得密集年会排练的协调机会，选择兼顾本职并改善节奏；RUN08 获得技术路线负责人机会，选择自研长期资产。可见响应分别 S+1/N+2/O0/H−1 与 S+2/N0/O−1/H0。**首先分叉的是暴露集合**，不是相同机会下的无理由不同选项。此时只是多维 tradeoff，不能由最终 score 给首个选择贴正确答案。

M2 的年会接手统筹 vs 自研延期/合规压力延续不同分支；M3 前 RUN07 S8/N3/O0，RUN08 S7/N0/O−1。RUN08 在M3也曾反超 Skill，故不存在 M1 起 Skill 单调落后。首个正式 cadence 分叉在 M6 的 L2 vs L1；随后 RUN08 多次 public S/N/O 停在9/3/3，而 RUN07 M7–M9 进入 CI、Mentor、Review 等窗口并到21/7/6，形成持续资本差距。M6 晋升前 public S/N 相同、O仅差1，不能把晋升差异解释成已知隐藏门槛或某个单项充分原因。

## B｜Opportunity exposure taxonomy

以下按 public semantics 作离线分类，各类可重叠；不是 title→runtime answer 规则，也没有将 Story 的未公开效果填为广告收益。

| Family | RUN07 可见窗口 | RUN08 可见窗口 | 判断 |
|---|---|---|---|
| ownership / responsibility | M1–2排练优化/接手统筹；M7 Mentor/CI；M14–15高管汇报 | M1–2自研/延期；M3–4高管汇报；M5–6客户确认机制；M15–16 Demo | 两局都有显著责任机会；不能说 RUN08 缺少 ownership exposure |
| visible delivery/result | M5–6答辩/ROI、M6客户可提前联调、M8公开CI上线 | M4高管追问、M5–6返工范围谈拢/留痕、M9–10延期/分阶段交付 | RUN07 多处已有具体结果或兑现入口；RUN08 更多延期/修复，但部分来自选择分支 |
| Skill growth | M1低风险新框架；M7–8 CI；M13匿名反馈/M17技术价值 | M1自研；M12证书；M15–16 Demo复盘/技术分享 | 无法从 Story 文本完整量化事前 S upside；响应单独列于D |
| Network growth | 集体协调、Mentor、M6提前交付、M15换班 | M3文档帮助、客户合作、M13–15午餐/非正式关系 | 两局均有关系机会；RUN08关系经营后出现Health支出与未增长，非未选择 |
| Output growth | 答辩/ROI、M6提前交付、CI公开成果、M15汇报 | 自研延期、客户原型/确认、分阶段交付、Demo、M18真实申奖 | 同类 Main/Energy 持续开放；RUN08 多次兑现响应较弱 |
| Health recovery | M2–3已到H1；M6提前交付后H1；M12明确EAP危机 | M1健身；M13同一EAP危机；M15关系投入后H3 | 重大健康保护并非 RUN08 更早/更多：RUN07 更早触底 |
| Wealth/income | M11报销、M18奖金/涨幅谈判 | M7报销、M12保密/买房、M14关系晋升、M16–18调薪 | 有时间/内容差异；未见本窗口直接 affordability/income continuity 危机 |
| compliance/trust | M1离职资料、M4 CVE、M8–9导师追责、M11报销 | M2离职资料、M2自研暗借建议、M3竞对、M7–8截图/报销/匿名调查 | RUN08 M7–8的规范/关系窗口集中；RUN07也有重大安全与追责暴露 |
| ordinary Story tradeoff | 技术选型、周末认证/交付、反馈、值班 | 健身/加班、接待形式、午餐、技术分享 | 不以普通成本直接判为 binding threat |

两局各54个 Story decision windows，其中16对 description/choices 完全相同，覆盖各29.6%；其余38个窗口不作 exact matching（不同分支/时序/语义，不等同38次独立随机冲击）。六个季度初始 Energy menu 和六个 Main menu 均相同，机会类别一直可用，但 Level、资源、已测试响应和Delivery不同。

回答：没有充分证据断言 RUN07 **事前总共获得更多 high-upside exposure**；RUN08 也拿到同一高管/交付机会。支持的是 RUN07 有更早的集体可见性及后续CI/Mentor/技术反馈路径，并实际实现更多资本增长；RUN08 较早进入自研延期/合规分支、M7–11修复/关系窗口，且响应薄弱。这能合理解释部分早期 gap，但不能把 exposure、先前选择和响应机制完全分离。

## C｜Matched / comparable decisions

16对 exact Story 中15对同选项；唯一不同是自研/开源，H1 vs H5、MODE=S vs A。并未找到在相同资源/Level/局部历史下重复且 material 的不同选择。下表抽取关键对；全部16对及行号见 compact JSON。

| Context；RUN07 / RUN08 action | RUN07 choice | RUN08 choice | 当时 ranking rationale | Same? / Material? |
|---|---|---|---|---|
| 技术负责人；a8/M3 vs a2/M1 | 开源快速交付 | 自研长期资产 | 前者H1保护；后者H5长期ownership | 不同 / material；输入约束不同，非无条件policy drift |
| 修生产健康检查；a19/M5 vs a3/M1 | 立即修并查其它服务 | 同左 | 均系统性担责 | 相同 / 后续Skill响应不同 |
| 高管首次汇报；a56/M14 vs a8/M3 | 结论、成果、风险预案 | 同左 | 均公开成果与诚信 | 相同 / 同样S+2/O+1 |
| 高管追问；a59/M15 vs a15/M4 | 量化影响与资源诉求 | 同左 | 均展示掌控力/ownership | 相同 / S/N/O响应显著不同 |
| Code Review队列；a35/M9 vs a23/M6 | 核心逻辑/隐患，小问题作者迭代 | 同左 | 均可扩展Reviewer做法 | 相同 / Level与响应不同 |
| 咖啡因/作息；a29/M7 vs a70/M17 | 固定作息、循序恢复 | 同左 | 均恢复健康/专注 | 相同 / 同L2，H同+2但S不同 |
| EAP危机；a47/M12 vs a53/M13 | 医疗假+专业干预 | 同左 | 均S，安全压过里程碑 | 相同 / H+3/O−2相同 |
| 休假后延期；a53/M13 vs a57/M14 | 专注恢复产出 | 同左 | 均回A修复公开绩效 | 相同 / N−1/O+2相同 |
| 保密资料/报销；a4、45 vs a7、29 | 拒收/合规报销 | 同左 | 均守合规 | 相同 / Risk标签ALLOW与PASS有差异，未改变choice |
| 同季度Main；M3/6/12/15/18 | 申请关键项目 | 同左 | ownership、多维成长 | 5/6季一致；不能证明固定菜单最优 |
| M9 Main；a40 vs a39 | 汇报成果 | 申请关键项目 | 前者已有公开CI上线且gap=结果兑现；后者延期路径/gap=Output | 不同 / 材料与Level不同，不满足same-input drift |
| M9 Energy；a37–39 vs a36–38 | 汇报×2、人脉 | 人脉、恢复×2 | L2 O响应有效 vs L1局部O/N已NO_GAIN | 不同 / input-response条件不同；后者有泛化疑点 |

RUN08 a37称“Output/Network家族均NO_GAIN”，a38把H补到9；当时技能学习仍合法且未在本局该Level测试。这是**局部NO_GAIN概括与未测试路径遗漏的可控疑点**。但没有同状态/响应史的RUN07反例，也没有该替代路径的已确认gain，不能量化失去的收益或把它升级为执行方差主因。RUN08 M15 H4→6→8也有数值保护倾向；两局都使用过数值健康理由，不能凭此单独归因低分。

## D｜Clean public response

以下 Story pair 不用后续月信息解读早期决策，只比紧邻公开状态。所有列举均同月、同Level、after feed为空；不同Level/基线仍限制跨局机制归因。delta顺序S/N/O/H。

| Same choice | RUN07 before → after | RUN08 before → after | 分类 |
|---|---|---|---|
| 立即修endpoint并全面查因 | a19/M5/L1：9/3/2/4→9/3/3/3 | a3/M1/L1：3/1/−1/5→5/1/0/4 | OUTCOME_RESPONSE_VARIANCE；RUN08反而多S+2 |
| 作息调整 | a29/M7/L2：14/7/6/5→15/7/6/7 | a70/M17/L2：21/7/5/7→21/7/5/9 | OUTCOME_RESPONSE_VARIANCE；S+1 vs0，H同+2 |
| 稳健备考 | a36/M9/L2：20/7/3/8→21/7/3/7 | a47/M12/L2：11/4/3/8→13/4/3/7 | OUTCOME_RESPONSE_VARIANCE；RUN08反而多S+1 |
| 核心逻辑Review | a35/M9/L2：21/5/1/7→20/7/3/8 | a23/M6/L1：9/3/3/6→8/3/3/7 | N/O +2/+2 vs0/0；Level混杂，原因UNKNOWN |
| 高管追问资源 | a59/M15/L3：31/4/10/10→33/5/12/10 | a15/M4/L1：9/3/3/6→9/3/3/6 | S/N/O +2/+1/+2 vs0/0/0；Level混杂，原因UNKNOWN |

9对 both-clean且same-choice Story 中，5对S/N/O delta不同、4对相同；差异并不全部有利RUN07，同Level也不能控制资本基线、时序或其它未明确因素。不得称隐藏cap或event随机效果已被证实。

Energy 有明确公开广告且可局部归因：RUN07 Output 6 GAIN/2 NO_GAIN，Network 1/1；RUN08 Output 5/3，Network 2/1；Health恢复均4 GAIN/0 NO_GAIN。没有总体“RUN07同类动作全GAIN、RUN08全NO_GAIN”。关键是时序：RUN08 M6汇报材料O3→3，转高强度工作仍O3→3；M9人脉N3→3，S/N/O在该区间停滞；M12进入L2后汇报材料连续三次O3→4→5→6。RUN07也有M6汇报NO_GAIN、M9人脉NO_GAIN、M18汇报NO_GAIN。不存在即时重复同一已NO_GAIN Energy路径的已证案例；再次试验通常隔季/Level或有新局部gain。Main跨月响应一律MIXED，连续选关键项目不能据此判clean低价值重复。

## E｜Compounding delay：描述性拆解

1. **Promotion timing**：RUN07在M6进入L2、M12进入L3；RUN08在M12/M18才进入。首次M18观察双方同L3，但公开tenure为7 vs1。较早Level路径与后续更多成长共同出现；不能证明Level提升必然放大同选项收益，或解释M6晋升的内部原因。
2. **Exposure**：早期集体协调/接手统筹、低风险技术学习及M7–8 CI/Mentor，与自研延期、规范/关系修复窗口不同；后半窗口RUN07还有匿名反馈/技术价值/高管答辩，RUN08有午餐/关系经营/Demo。部分暴露由选择分支形成，不能全部称不可控随机性。
3. **Selected actions**：Story matched选择15/16一致，Main5/6季一致。差异集中在资源保护、对已知响应的Energy路由、不同Delivery基础，未见重复same-input material ranking drift。RUN08未简单放弃推进，仍用A、做ownership/交付动作。
4. **Public response**：RUN08 M4至M11的S/N/O多次无正向响应；RUN07在M6 Story及M7–9 CI/相关技术窗口继续积累，在M13–17多处技术/反馈窗口增长。这是资本增长差距的直接轨迹证据，原因保持UNKNOWN。
5. **Protection/recovery displacement**：两局Energy健康恢复都4次/4点；RUN07清理2次/4点、RUN081次/2点。RUN07在M1–18反而S9次，RUN08S1次；同EAP处理H+3/O−2一致，出现于M12 vsM13。RUN08后期恢复确实挤占当季Energy，但没有更多总恢复或长期S deadlock证据解释其低分；ordinary recovery choice和MODE计数也不是同一概念。

对齐首次M12观察时已有S12/N1/O3 gap；首次M18扩为20/7/9。因此“早期career-capital compounding consistency”是最值得继续测量的瓶颈；不能将这份描述性路径拆解当成最终score公式或数值因果百分比。

## Survival、correctness与下一边界

FACT：RUN07=72.65/50.86/48m/A/L5；RUN08=59.00/41.30/48m/C/L4。Score差13.65、范围59.00–72.65、均值65.825、survival2/2、70+1/2、early terminal0/2。两局均遭遇公开压力/心理安全窗口并活到48m，但n=2不建立稳定survival概率。当前score/trajectory一致性比已观测的lower-tail survival更有证据支持作为研究重点；`PREVENTIVE_OPTIONALITY_NOT_YET_PRIMARY`，不推动v9a。

`CORRECTNESS_ISSUES_SEPARATE_FROM_SCORE_DIVERGENCE`：RUN07 numeric HiddenRisk action-note refs=3（a126/150/152），RUN08=1（a126），均在本次M1–M18的77 actions之外；没有这些引用改变早期ranking的直接证据。这不证明所有推理均遵守firewall。Delivery parser RUN07 0/203因CTRL/DL adjacency，RUN08 205/205有separator；这是离线解析结果，未在运行中反馈给Candidate。RUN07 M9 notes确实引用公开CI成果选择汇报，但Delivery基础与RUN08不同，不能把parser拒收解释为分数原因。Risk标签差异有记录，choice一致；本任务不修复correctness问题，也不授予runtime validation。

建议 Stage 另行决定 Sample3：冻结同一Candidate，沿用统一的Review-first和month-last口径，观察未晋升窗口是否再次出现响应停滞、同等局部输入是否反复choice drift。该建议不含live授权、固定答案或候选改动。A为本任务的证据主类；若后续需要外生/执行方差的数值分离，须额外受控证据，不能从这两局反推。

两局exact raw与原hold均保持 `FORENSIC_HOLD=ACTIVE`。本报告及compact JSON支持独立Stage review，不自动解除原hold；责任/解除权仍S09 Stage/Main。文档变更仅本报告、一个compact JSON和CURRENT_STATE一条durable delta；未新增RUN_HISTORY流水、测试或复杂archive。

`NO_CANDIDATE_PATCH` · `LIVE_OPERATIONS=0` · `NEXT_GAME=NOT_AUTHORIZED`。
