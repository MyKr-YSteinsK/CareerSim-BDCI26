# S10-13｜Promotion Opportunity Capture 晋升机会捕获取证

> OFFLINE FORENSICS ONLY；IN_FLIGHT_EVIDENCE。Candidate/Skills/manifest 未修改；install/service/Provider/game 均 0。

## Decision

**VARIANCE_DOMINANT_NO_SAFE_PATCH**

**REPLICATE_EXACT_V6D_BEFORE_PATCH**

FACT：v6 的 clean Story Skill net +102，v6d +84；最终 Skill 142 vs114 的 28 差距中，18 出现在可隔离的同月同 Level Story 配对，10 位于 mixed 转换。Energy 对两者 Skill net 都为0。高 Skill 确实主要与 Story/混合轨迹一起累积，不能据此归结为少做“技能学习”。Main 均跨月，无 clean Main 效果，不把 mixed39/29 拆成 Main 或晋升奖励。

INFERENCE：没有识别出跨运行可推广的“v6d不愿承担机会”或“缺少认可结果”策略缺口。79 对相同公开情境中75对选同一动作；25对同 Level，但 **0 对完整 S/N/O/W/H/D + tenure 相同**。v6d 有大量技术、职责、stakeholder、mentoring uptake；后期公开 recognized proxy 并不比 v6 少。两段核心窗口任职时间/事件暴露不同，不能从结果倒推好答案。

DECISION BOUNDARY：`VARIANCE_DOMINANT` 是“现有公开证据不足以支持安全 patch”的决策类别，不是随机方差占比测量，也不证明任何策略改善都不可能。H5 为 PARTIAL，仍是当前最稳妥的行动结论。未创建 v6e 或 V6E_PROPOSAL。

## Identity / dataset / evidence firewall

- Branch：`codex/s10-13-promotion-opportunity-forensics`；Base：`5eb108b55a9f252d4fd6ff4561120d353f9d124b`（已验证 S10-12 parent）；不 merge main，不创建 worktree。
- Primary：v6 75.29/L6，v6d 71.67/L5。Supporting：v7o71.83/L5、v8a RUN07 72.65/L5、v6c64.26/L5；v1#1 76.04/L6 **Tier-B summary only**，Skill139，逐动作 attribution/capture/maturity UNKNOWN。
- Detailed：5 runs、40 Review windows、720 Story transitions；560 clean public associations、160 mixed、0 missing parsed pairs。Clean means fresh before/after 同月同 Level且非Review转换；延迟事件同时结算仍可能存在，**不是动作因果识别**。
- Sources：hash-locked accepted S10-04 `policy_transitions.jsonl`，SHA `b5cc5c2c71fbc2ee39d09a3676325a139352f976f9452b71430abf2c8005d4cd`；S10-10/S10-12 held public whitelist extractions；Git `4f54967e5d8b3f6fd82c0a9ceeab94ca525e8d4a` 的 S10 summary / S09-13 cohort 用于 accepted facts。各本地 source bytes/hash 在 JSON。仅投影 public状态、情境、合法动作语义和回执；不使用 advertised HiddenRisk、内部 score component、future-review label 作为 features，不读取 hidden stock/counter、Test 或 simulator/Dev formulas。
- 未重新打开 raw simulator events/DB；有限读取 S10-12 held transcript 的当前 Risk/Planning public rationale，过滤无关 numeric risk text。现有 FORENSIC_HOLD 不解除、来源不删除。所有研究标签仅在离线数据，未写入 runtime。
- 完整逐 Story forensic table 位于 `D:/CS/CareerSim/.local/scratch/s10-13/story_forensic_table.jsonl`（720 rows，hash/bytes 在 JSON）；是可重建 public derivative。每行有 run/月/Level/机会分类/public situation/选择语义/alternative classes/clean S/N/O/W/H/D delta/安全可链接 follow-up/maturity。只提交40 compact windows与70研究 witness，不提交大型重复 raw derivative。

## Taxonomy / Opportunity Capture definition

精简已有 S10 taxonomy 为9类：OWNERSHIP_DELIVERY（ownership/短周期交付/visible result）、TECH_ASSET、MENTORING、STAKEHOLDER_NETWORK、RECOGNITION、TRANSPARENCY_COMPLIANCE、RECOVERY、AVOIDANCE、RISKY_SHORTCUT。多标签可重叠；普通同事措辞不自动等于 networking，lexical “悄悄”不自动等于危险捷径。标签是辅助筛选，不充当答案。

机会筛选以当前公开职责、可完成交付、技术挑战、带教、stakeholder责任、认可贡献等语义为依据。CAPTURE=明确接受有用职责/成长路线；PARTIAL=建设性计划/折中但具体 uptake 不明；DECLINE=拒绝或保护；UNKNOWN=无法判定。GOOD_CAPTURE 只表示选了有 public value 的路径，**不等于成功/最优**。JUSTIFIED_CONSERVATIVE 须有具体健康/保密/可靠性约束；MISSED_OPPORTUNITY 须有明确安全高价值 alternative 且无足够拒绝理由，不能从 low score 判。普通非机会场景和证据不足归 AMBIGUOUS。

| run（144 Story each） | GOOD_CAPTURE screened minimum | MISSED_OPPORTUNITY | JUSTIFIED_CONSERVATIVE | AMBIGUOUS |
|---|---|---|---|---|
| v6 | 22 | 0 established | 9 | 113 |
| v6d | 28 | 0 established | 12 | 104 |
| v7o | 19 | 0 established | 9 | 116 |
| RUN07 | 24 | 0 established | 9 | 111 |
| v6c | 21 | 0 established | 7 | 116 |

以上是半定量筛选账，不是全局机会成功率；各运行机会暴露不一致，AMBIGUOUS 大量包含非机会和词法漏标，不能拿28/144 vs22/144证明 v6d 更强。v1 没有逐动作分母，不填0。

## Skill compounding attribution

| run | final Skill | clean Story positive / loss / net | clean Main | clean Energy net | mixed net |
|---|---|---|---|---|---|
| v6 | 142 | +104 / -2 / +102 | UNKNOWN（0 clean Main） | +0 | +39（48 transitions） |
| v6d | 114 | +88 / -4 / +84 | UNKNOWN（0 clean Main） | +0 | +29（48 transitions） |
| v7o | 130 | +88 / -2 / +86 | UNKNOWN（0 clean Main） | +4 | +39（48 transitions） |
| RUN07 | 119 | +84 / -3 / +81 | UNKNOWN（0 clean Main） | +1 | +36（48 transitions） |
| v6c | 129 | +93 / -2 / +91 | UNKNOWN（0 clean Main） | +0 | +37（48 transitions） |

每局 initial Skill=1；clean Story net + clean Energy net + mixed net 精确等于 final−1。32个 Story mixed +16个 Main mixed，统一保留，不猜 Story/工资/Level/promotion 的份额。v7o 有4次 Skill learning，clean Energy Skill+4；RUN07一次+1。v6/v6d无 Energy Skill gain，v1摘要也没有大量 Skill learning 路径；这不支持机械 Skill farming。

可标注的 selected-semantic clean Story positive Skill 中，v6 OWNERSHIP_DELIVERY +11、TRANSPARENCY_COMPLIANCE +11、STAKEHOLDER_NETWORK +8、TECH_ASSET +5；v6d分别+11/+10/+10/+7。伴随正Skill变化的次数，v6上述四类为8/9/7/2，v6d为7/8/9/3；次数与positive gain都只描述public association。这些标签重叠且覆盖不完整，不能相加成总 Story gain，也不是收益公式。v6d没有在已标签技术/ownership类别上显著缺失。例：v6 M47低风险新框架 choice 与 v6d M1相同，分别 public clean Skill+3/+2；不同Level/阶段/历史，不归因于“更勇敢”。

## Review boundary correction / Promotion window comparison

正式 Review 的前状态与后状态严格分开。窗口包含上一次 Review 后的动作至本次 trigger 的**选择/pre-state**；trigger 的 post结果包含跨月/Review/Level变化，保留 mixed。maturity 只能用 trigger 前已公开的情境；Review 后反馈、下一月结果不能回填到之前窗口。M36新Story不是M36晋升的先行证据。

M18特别反例须纠正粒度：S10-12常引用的 v6 **37/16/14/10** 与v6d **39/17/15/10** 是 **first Review post**。实际 pre Review 为 v6 **36/21/14/10**、v6d **39/17/16/8**，trigger Story也不同。它们是“公开成长接近而晋升不同”，**不是相同公开输入**的控制实验，更不能用post状态构造晋升门槛。研究继续面向48月多一次晋升，不优化M18数值。

| window | pre Level / public tenure | pre-review S/N/O/W/H/D | grade / promote | clean Story S net | completed/recognized proxy | HR warnings/serious |
|---|---|---|---|---|---|---|
| v6 30→36 | L4 / 18 | 95/36/26/20/7/10 | A / YES | +14 | 2/1 | 1/0 |
| v6 42→48 | L5 / 12 | 140/54/37/35/7/10 | A / YES | +15 | 1/1 | 2/1 |
| v6d 30→36 | L4 / 12 | 76/35/25/24/10/10 | A / NO | +10 | 1/2 | 1/0 |
| v6d 42→48 | L5 / 6 | 110/54/33/37/10/10 | B / NO | +13 | 0/3 | 1/1 |
| v7o 30→36 | L4 / 18 | 89/36/26/23/8/10 | A / YES | +12 | 1/0 | 0/0 |
| v7o 42→48 | L5 / 12 | 126/54/38/39/10/10 | A / NO | +13 | 0/1 | 0/0 |
| RUN07 30→36 | L4 / 12 | 81/36/25/18/7/10 | B / NO | +17 | 1/1 | 3/0 |
| RUN07 42→48 | L5 / 6 | 117/53/33/32/9/10 | B / NO | +12 | 1/1 | 0/0 |

**v6 M30→36 vs v6d M30→36**：v6早在M18进入L4，到M36 tenure18；v6d M24才进入L4，tenure12。两者gradeA，但S95 vs76、Story net14 vs10。v6此前顶岗、团建报名、AI guideline、正面争取成果被认可；v6d接受新职责、CTO调岗、专利署名、制定迁移计划也有公开 uptake/认可。v6d recognized proxy2，v6为1，因此没有“只因没被认可”差异。v6 M36全面文档化/跨组架构评审发生在本次晋升后，不能用作晋升前证据。

**v6 M42→48 vs v6d M42→48**：v6在L5 tenure12、gradeA；v6d在L5 tenure6、gradeB，前者Story net15、后者13。v6新增关键补位被Leader记下、构建故障处理、新框架/职业转型；v6d高管交流、纠正经营口径、适度结对、组织者报名、性能风险闭环，同样不只是report。v6d recognized proxy3 vs v6为1；公开次数不能解释差异。v6d M48高密度带教/cleanup均在最后 Review 后，无法影响该 Review。

Supporting：v7o与v6同在M36进入L5，M48 tenure12、gradeA，仍未晋升；仅任职时间/A grade不足以解释L6。RUN07 M30→36 Story net17甚至高于v6的14却不晋升，M42→48仍抓转岗、技术投资、合规上线等机会但L5不进；高clean Skill积累不是晋升充分条件。v6cfinalS129比v6d114高，但分数64.26比71.67低，再反对Skill阈值或单维目标。

全40窗口（Main/Energy模式、tenure、grade、warning witness、capture与maturity在JSON）：

| window | pre Level / tenure | pre-review S/N/O/W/H/D | grade / promote | clean Story S net | completed/recognized proxy | HR warnings/serious |
|---|---|---|---|---|---|---|
| v6 0→6 | L1 / 5 | 9/3/3/2/5/10 | C / YES | +6 | 0/1 | 2/0 |
| v6 6→12 | L2 / 6 | 20/6/5/4/5/10 | B / YES | +7 | 0/0 | 1/0 |
| v6 12→18 | L3 / 6 | 36/21/14/7/10/10 | B / YES | +14 | 0/0 | 2/0 |
| v6 18→24 | L4 / 6 | 55/27/23/12/10/10 | B / NO | +12 | 0/0 | 4/0 |
| v6 24→30 | L4 / 12 | 76/36/26/14/7/10 | A / NO | +12 | 1/0 | 3/0 |
| v6 30→36 | L4 / 18 | 95/36/26/20/7/10 | A / YES | +14 | 2/1 | 1/0 |
| v6 36→42 | L5 / 6 | 122/49/35/27/9/10 | A / NO | +21 | 1/0 | 0/0 |
| v6 42→48 | L5 / 12 | 140/54/37/35/7/10 | A / YES | +15 | 1/1 | 2/1 |
| v6d 0→6 | L1 / 5 | 9/3/3/2/7/10 | C / YES | +7 | 0/1 | 4/3 |
| v6d 6→12 | L2 / 6 | 21/7/6/4/8/10 | B / YES | +9 | 0/0 | 5/0 |
| v6d 12→18 | L3 / 6 | 39/17/16/7/8/10 | B / NO | +13 | 0/2 | 5/3 |
| v6d 18→24 | L3 / 12 | 42/21/15/10/9/10 | B / YES | +3 | 0/2 | 3/1 |
| v6d 24→30 | L4 / 6 | 61/26/20/14/8/10 | B / NO | +15 | 0/0 | 2/0 |
| v6d 30→36 | L4 / 12 | 76/35/25/24/10/10 | A / NO | +10 | 1/2 | 1/0 |
| v6d 36→42 | L4 / 18 | 93/36/25/30/10/10 | A / YES | +12 | 1/0 | 0/0 |
| v6d 42→48 | L5 / 6 | 110/54/33/37/10/10 | B / NO | +13 | 0/3 | 1/1 |
| v7o 0→6 | L1 / 5 | 9/3/3/3/5/9 | C / YES | +7 | 1/1 | 0/0 |
| v7o 6→12 | L2 / 6 | 21/7/6/5/5/10 | B / YES | +9 | 0/1 | 0/0 |
| v7o 12→18 | L3 / 6 | 37/21/14/7/10/10 | B / YES | +11 | 1/1 | 0/0 |
| v7o 18→24 | L4 / 6 | 47/28/26/11/8/10 | B / NO | +4 | 0/0 | 4/4 |
| v7o 24→30 | L4 / 12 | 67/35/26/18/10/10 | A / NO | +15 | 0/1 | 1/0 |
| v7o 30→36 | L4 / 18 | 89/36/26/23/8/10 | A / YES | +12 | 1/0 | 0/0 |
| v7o 36→42 | L5 / 6 | 108/49/37/30/10/10 | A / NO | +14 | 0/0 | 2/0 |
| v7o 42→48 | L5 / 12 | 126/54/38/39/10/10 | A / NO | +13 | 0/1 | 0/0 |
| RUN07 0→6 | L1 / 5 | 9/3/3/2/3/10 | C / YES | +6 | 0/1 | 1/0 |
| RUN07 6→12 | L2 / 6 | 21/7/6/3/7/10 | B / YES | +7 | 0/0 | 1/0 |
| RUN07 12→18 | L3 / 6 | 39/10/14/4/9/10 | B / NO | +12 | 1/1 | 4/3 |
| RUN07 18→24 | L3 / 12 | 42/21/15/8/10/10 | B / YES | +1 | 0/1 | 5/3 |
| RUN07 24→30 | L4 / 6 | 58/26/26/13/10/10 | B / NO | +14 | 0/0 | 2/0 |
| RUN07 30→36 | L4 / 12 | 81/36/25/18/7/10 | B / NO | +17 | 1/1 | 3/0 |
| RUN07 36→42 | L4 / 18 | 100/36/24/22/10/10 | A / YES | +11 | 0/0 | 1/1 |
| RUN07 42→48 | L5 / 6 | 117/53/33/32/9/10 | B / NO | +12 | 1/1 | 0/0 |
| v6c 0→6 | L1 / 5 | 9/3/3/2/5/10 | C / YES | +7 | 0/1 | 1/0 |
| v6c 6→12 | L2 / 6 | 20/7/6/3/6/10 | B / YES | +8 | 0/0 | 0/0 |
| v6c 12→18 | L3 / 6 | 33/13/10/6/7/10 | B / NO | +7 | 0/1 | 4/0 |
| v6c 18→24 | L3 / 12 | 42/21/16/7/8/10 | B / YES | +7 | 1/1 | 3/0 |
| v6c 24→30 | L4 / 6 | 63/31/23/11/7/10 | B / NO | +15 | 1/0 | 4/2 |
| v6c 30→36 | L4 / 12 | 77/36/26/15/10/10 | A / NO | +9 | 0/0 | 3/0 |
| v6c 36→42 | L4 / 18 | 103/36/25/20/5/10 | A / YES | +20 | 2/1 | 4/0 |
| v6c 42→48 | L5 / 6 | 122/47/38/22/3/10 | A / NO | +14 | 0/1 | 3/0 |

## v6d M19–48 Over-conservatism / competing routes

| public witness | Selected semantic / public result | Forensic assessment |
|---|---|---|
| M19 high-management milestone, action625 | 量化最坏情况/资源诉求 | GOOD_CAPTURE：责任与stakeholder价值，没有被visibility objective压掉。 |
| M21 AI guideline,673；M28重构,937 | 接受治理责任；渐进重构 | GOOD_CAPTURE；没有依靠Energy学习，completed UNKNOWN。 |
| M31 certification vs one-day-earlier delivery,1033 | 选择提前交付，public clean S−1 | AMBIGUOUS：有具体客户联调价值，也有公开培训alternative；可能visibility偏置，但不能把未选择培训当成错误或假定其收益。无跨运行相同情境多witness支持。 |
| M32 migration,1049；M33,1089 | 未测rollback先推迟保大促，随后72小时迁移计划 | JUSTIFIED_CONSERVATIVE + 后续capture；v6/v7o选择双写灰度，但时点/Level/状态不同，没有证明灰度已解除未测rollback风险。 |
| M33 CTO调岗,1081；M34/35专利,1129/1153 | 接受架构组；署名recognized但独立产品受损 | GOOD_CAPTURE并有tradeoff；recognition不自动意味着career option收益。 |
| M37探索,1241/1249 | 申请20%sprint、复杂度超预期后坦诚评估 | GOOD_CAPTURE/PROGRESS：与v6M38同选择，不是保守拒绝。 |
| M40挑战任务,1353；M44 mentoring,1481 | 请缨成长；结对一小时其余异步保bug deadline | GOOD_CAPTURE：折中保交付不等于拒绝带教。 |
| M45组织者,1505 | 公开非OKR软实力责任，主动报名 | GOOD_CAPTURE；发生在TIGHT季度，直接反证“Risk禁止所有ownership”。 |
| M46性能闭环,1553/1561 | 私下提醒获感谢，尊重对方意愿点对点闭环 | AMBIGUOUS：可能错过跨组recognition/经验传播；也有合作关系理由。未证明应当公开，不能写event答案。 |
| M48 mentoring,1609 | 高密度带教，Health10→8 | GOOD_CAPTURE，但post-final-Review，不能解释之前未晋升。 |

这些局部tradeoff值得后续复制观察，但没有满足A–D所需跨多个运行的安全、可推广policy gap。win-visibility长期存在与某次选择同时出现，不证明它造成该选择；未用LLM总结倒推隐藏偏好。

## Cleanup逐次机会成本

v6d7次、v6两次、v1摘要3次。成本差不直接等于过用；所有7次公开S/N/O/H均flat，**不能证明潜在风险清理无效或已清除**。不读hidden值；没有explicit public clearance时全部UNKNOWN。

| quarter / source action | class | latest public HR warning | evidence / boundary |
|---|---|---|---|
| M6 / action 209 | PLAUSIBLE | M6 / observe 183；new HR warning | Current light warning plus earlier severe/accumulated exposure; not numerical hidden risk. |
| M12 / action 409 | CLEARLY_JUSTIFIED | M12 / observe 383；new HR warning | Fresh accumulated-risk warning at Review and relationship friction. |
| M15 / action 505 | PLAUSIBLE | M15 / observe 479；new HR warning | Fresh M15 light public warning after M12 cleanup; no explicit clearance. |
| M18 / action 601 | CLEARLY_JUSTIFIED | M18 / observe 575；new HR warning | Fresh serious 自求多福 warning. |
| M21 / action 697 | PLAUSIBLE | M20 / observe 647；new HR warning | Fresh M20 light warning after M18 cleanup; less severe wording is not clearance. Repetition may have opportunity cost, necessity not identified. |
| M24 / action 793 | PLAUSIBLE | M20 / observe 647；same HR warning | No fresh HR warning since M20; new security/conflict reporting fallout and sustained Network loss. Risk Budget AVAILABLE; rationale supports plausible protection, not binding necessity. |
| M48 / action 1617 | CLEARLY_JUSTIFIED | M48 / observe 1591；new HR warning | Fresh accumulated-risk warning; after final Review, cannot cause or fix M48 no-advance. |

总计 CLEARLY_JUSTIFIED **3** / PLAUSIBLE **4** / POSSIBLE_OVERUSE **0 established** / UNKNOWN **0 classification**；clearance **7/7 UNKNOWN**。M24唯一复用同一HR warning，但同时有新的安全举报/利益冲突report fallout和Network连续下降，不能只凭旧warning判重复无效。M21已有M20新轻微warning，不是纯重复M18旧严重warning。report/Network alternatives公开存在，counterfactual growth值UNKNOWN；不削弱必要Risk protection。

## Result maturity / recognition

`PROMISE < PROGRESS < COMPLETED < RECOGNIZED` 仅为待检验的结果成熟度排序，不是晋升机制。pre-context 已知结果与当前选择的结果成熟度分别保存；当前 CAPTURE 通常仅PROMISE，只有安全叙事链接的后续观察才升级。全局表是描述proxy，不是独立项目数量；每window相同public描述去重。

| run | pre-context PROMISE | PROGRESS | COMPLETED | RECOGNIZED | UNKNOWN |
|---|---|---|---|---|---|
| v6 | 1 | 3 | 5 | 3 | 132 |
| v6d | 4 | 4 | 2 | 10 | 124 |
| v7o | 3 | 3 | 3 | 5 | 130 |
| RUN07 | 3 | 2 | 3 | 5 | 131 |
| v6c | 0 | 1 | 4 | 5 | 134 |

链接只确认9个明确narrative follow-up，例如文档让junior独立处理、探索验证可行、专利署名、私下提醒获感谢、版本发布及临时缓解；仍不把延迟numeric delta归给之前动作。高成熟度也可带坏后果：v6版本按时发布后仍发生数据异常访问，v6d署名后失去独立产品机会。v7o promoted M30→36 completed1/recognized0；RUN07不进的相应窗口completed1/recognized1。v6d两段no-advance recognized proxy反而更多。公开成熟度质量/重要性可能不同，低count也可能只是没显示；不能把H2写成已证公式或修Prompt理由。

## H1–H5 / Main handoff

| Hypothesis | Status | Finding |
|---|---|---|
| H1 Skill Compounding | PARTIAL | Story clean gap+18/总Skill gap28为FACT；混合gap10不拆；没有可推广选择差异造成它的证据。 |
| H2 Recognized Result | UNSUPPORTED | “近期completed/recognized是关键公开区别”未获支持；窗口反例多，质/曝光UNKNOWN。 |
| H3 Opportunity Capture | UNSUPPORTED | 系统性意愿缺口未识别；79相同情境75同选，v6d实际抓机会，支持运行抓机会仍L5。 |
| H4 Over-Conservatism | UNSUPPORTED | 7 cleanup有公开依据，M31/M46是局部tradeoff；未见多个明确不必要Risk压制。 |
| H5 Mostly Variance | PARTIAL | tenure/事件暴露/上下文不受控，0严格matched-state对；现有特征不足以识别原因，随机贡献未测量。 |

Final Decision只有一个：**VARIANCE_DOMINANT_NO_SAFE_PATCH**。Recommendation只有一个：**REPLICATE_EXACT_V6D_BEFORE_PATCH**。Main若授权下一步，应复制精确v6d而非立即新增规则；本任务不授予任何下一局权限。关注后续复制中晚期窗口、same-context选择与public maturity是否复现，而非优化S/N/O数值或固定Skill学习。

## Verification / preservation / TASK_RESULT

Scope仅两份研究交付与branch-local CURRENT_STATE；frozen Candidate/Skills/configs/Runner/dependencies均与Base相同。未创建v6e、Skill/Memory/Team、install或runtime脚本；分析工具只在ignored `.local/scratch/s10-13/`。source hashes、720/560/160 counts、40窗口边界、Skill恒等式、maturity时间戳、7cleanup、JSON parse、secret scan和git diff --check通过。branch commit/push/remote/clean实值由最终TASK_RESULT记录，避免文档自引用commit hash。

现有S10-10/S10-12 raw FORENSIC_HOLD仍ACTIVE；未释放、未删除、未写入服务/共享DB/provider配置。完整本地表可从保留accepted public sources重建；不是唯一取证来源。Project架构无变化，无长期ADR新增。

Non-Claims：无 causal promotion formula、stable75 proof、hidden-test transfer、event answer mapping；没有证明variance占比，没有保证复制达到75，没有给危险机会强行capture。

**RETURN_FOR_PROMOTION_GAP_DECISION**

**NEXT_GAME=NOT_AUTHORIZED**
