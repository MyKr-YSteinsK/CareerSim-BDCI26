# S06-14｜事件结构、语义风险与可迁移决策模式深挖

## 结论与边界

- Review status: `COMPLETE_FOR_MAIN_REVIEW`；当前候选仍为 `candidate-v5-evidence-driven-phase-policy`。
- Base: `main@73f0b69857d726de3a15824063e97bc1a9b1f754`。
- 本文是离线证据审查，不修改 Skill、instruction、candidate、Runner、依赖或动态状态；没有游戏、provider、service、install/reload、MCP 或 session 操作。
- 结果支持一个小型、情境化的 decision-pattern library 作为后续候选，不支持事件答案表、普适最佳动作或单局因果结论。
- 所有策略建议仍须 Main review；不改变 `NEXT_GAME` 授权状态。

证据标签：`DEV_CONFIRMED` 为冻结公开 Dev 数据结构/事实；`DERIVED_DEV_ANALYSIS` 为本次确定性离线计数；`RUN_OBSERVED` 为可追溯运行记录；`HYPOTHESIS` 为未验证策略假设；`UNKNOWN` 为证据不足；`DO_NOT_ENCODE` 为明确禁止进运行时策略的内容。

## 1. Source scope 与方法

### 读取边界

- 只读 root `.venv` 中 `career-emulator==1.0.1`、`career-emulator-bdci26==1.0.0` 的公开 `dev/dataset/action_pool/short_chain/*.data` 与 `long_chain/*.data`；没有读取 `test`、private split、hidden database 或本机 ignored raw。
- 只读项目已有 [STRATEGY_EVIDENCE](../STRATEGY_EVIDENCE.md)、[RUN_HISTORY](../RUN_HISTORY.md)、[S06-11](S06-11_SURVIVAL_REVIEW.md)、[S06-12](S06-12_PROMOTION_PERFORMANCE_REVIEW.md)、[S06-13](S06-13_QUARTERLY_ACTION_REVIEW.md)、当前三个 Skills 与已提交的历史轨迹/forensic。
- `.data` 使用冻结公开转换格式：首字节后的 raw-DEFLATE payload 解压后按 MessagePack 读取。分析为一次性内存扫描；未提交脚本、CSV、完整事件文本或 choice lookup。

### 可见性与解释边界

每个模板拆为四层：

1. **Surface cue**：当前事件/选项可见的词句；
2. **Situation**：例如授权、健康负荷、责任归属、交付延误或人际修复；
3. **Decision primitive**：例如核实、记录、拒绝越权、分阶段交付、休息恢复；
4. **Outcome signature**：Dev 记录的选择后 `Health / Dignity / Network / Skill / Output / Wealth / HiddenRisk` 更新。

第 4 层是事后隐藏更新，不是选择前的 Agent-visible 收益。模板数、词项命中数、状态方向都不是出现概率、运行时风险真值或选择答案。`status_updates` 只用于检查类内异质性，不能进入 runtime rule。

## 2. Full event dataset

| 指标 | 结果 |
|---|---:|
| 事件模板 | 171：short-chain 118，long-chain 53 |
| Nodes / choice options | 1,133 / 974 |
| 无 choices 的 node | 721 |
| Node fanout | 0 choices: 721；2: 273；3: 128；4: 11 |
| 每模板最长决策数（按 root-to-terminal path 的选择次数） | short：1 次 70 个、2 次 46 个、3 次 2 个；long：2 次 47 个、3 次 4 个、4 次 2 个 |
| root-to-terminal paths | short 429，long 314；路径不是独立样本 |
| long root options | 151/151 指向可继续的 follow-up node；root 有 2/3/4 个不同后续目标的模板分别为 9/43/1 |

long-chain 内部更新方向呈明显混合：237 条路径有“首选项任意维度正向更新、后续任意维度负向更新”；227 条方向相反；其中同一 HiddenRisk 维度首正后负 47 条、首负后正 8 条，Health 首负后正 9 条。它只说明长链可包含相互抵消的事后内部结果，不说明玩家能预知，也不支持“首步固定选择可避免后续惩罚”。

## 3. Taxonomy rebuild

### 旧 taxonomy 复核

S06-09 的九个广义标签是多标签、显式词项 heuristic：例如同事/项目会覆盖很多不同情境。其已提交统计中 `UNKNOWN_MIXED` 为 126 templates / 787 options；类别间重叠，数字不可相加。该结果适合做检索覆盖，不适合直接当 Risk trigger 或策略类。

### 更细场景类的异质性检查

以下是本轮更窄的**情境标注**：按事件/节点描述及该节点选项所处场景归类，仍是多标签 heuristic。`local options` 是相应节点的候选项数；`signatures` 是这些选项隐藏更新的不同组合数；`HR +/−`、`Health +/−` 是事后内部更新方向；`both HR` 是同一模板存在正、负 HiddenRisk 替代项的模板数。此表衡量异质性，不衡量选择收益。

| 场景类 | 模板 | Local options | Long | Signatures | HR +/− | Health +/− | Both HR |
|---|---:|---:|---:|---:|---:|---:|---:|
| HEALTH_LOAD | 42 | 100 | 16 | 83 | 42/14 | 22/43 | 11 |
| HEALTH_MEDICAL | 13 | 40 | 5 | 34 | 21/10 | 13/15 | 7 |
| CONFIDENTIALITY_DATA | 17 | 69 | 4 | 52 | 34/25 | 0/2 | 12 |
| COMPLIANCE_PROCESS | 34 | 107 | 17 | 99 | 50/36 | 4/9 | 19 |
| TRUST_CREDIT | 4 | 15 | 1 | 15 | 7/2 | 0/1 | 2 |
| TRUST_DECEPTION | 16 | 22 | 10 | 18 | 10/7 | 0/3 | 4 |
| ACCOUNTABILITY_BLAME | 16 | 36 | 6 | 36 | 14/3 | 1/6 | 3 |
| DELIVERY_DELAY | 19 | 61 | 8 | 58 | 26/13 | 3/16 | 8 |
| DELIVERY_SCOPE | 8 | 33 | 4 | 32 | 14/4 | 0/11 | 3 |
| SYSTEM_RELIABILITY | 44 | 176 | 15 | 154 | 76/35 | 14/29 | 21 |
| SECURITY_INCIDENT | 4 | 13 | 2 | 13 | 8/3 | 1/0 | 2 |
| RELATIONSHIP_BOUNDARY | 59 | 140 | 25 | 122 | 60/29 | 9/31 | 18 |
| RELATIONSHIP_REPAIR | 25 | 44 | 10 | 43 | 15/4 | 1/10 | 3 |
| ORG_POLITICS | 11 | 24 | 6 | 23 | 15/4 | 0/3 | 3 |
| NEGOTIATION_COMPENSATION | 24 | 109 | 11 | 84 | 52/22 | 6/18 | 12 |
| CAREER_OPTION | 24 | 86 | 13 | 70 | 40/3 | 4/21 | 3 |
| MENTORSHIP_MANAGEMENT | 12 | 41 | 1 | 39 | 17/0 | 2/9 | 0 |
| PUBLIC_VISIBILITY | 1 | 2 | 0 | 2 | 0/0 | 1/1 | 0 |
| UNKNOWN_MIXED | inherited 126 | inherited 787 | — | mixed | mixed | mixed | — |

`UNKNOWN_MIXED` retains the prior S06-09 residual bucket; it is not recomputed by subtracting these overlapping, refined labels. Several refined classes have very low support (TRUST_CREDIT, SECURITY_INCIDENT, PUBLIC_VISIBILITY); they should remain descriptive subtypes, not independent runtime rules. Most supported classes include both positive and negative HiddenRisk alternatives and many distinct signatures. No class supports a universal action prescription.

## 4. Decision-primitive mining

Primitive matching is wording-based and multi-label. `Events/options` and `Long events/options` count matched templates/choice strings; `HR +/−` and `Health +/−` count matched options containing those post-choice internal directions. Provisional group is a portability judgment, not an outcome leaderboard.

| Primitive | Events/options | Long events/options | HR +/− | Health +/− | Provisional class |
|---|---:|---:|---:|---:|---|
| VERIFY_FIRST | 14/20 | 5/11 | 7/9 | 1/4 | HIGH_VARIANCE |
| DOCUMENT_FACTS | 21/28 | 7/12 | 6/16 | 0/1 | HIGH_VARIANCE |
| DISCLOSE_EARLY | 29/35 | 14/16 | 11/13 | 4/5 | HIGH_VARIANCE |
| REFUSE_UNAUTHORIZED | 11/11 | 6/6 | 3/5 | 0/0 | HIGH_VARIANCE |
| ESCALATE_WITH_EVIDENCE | 2/3 | 2/3 | 1/2 | 0/0 | INSUFFICIENT_EVIDENCE |
| ESCALATE_IMMEDIATELY | 1/1 | 1/1 | 1/0 | 0/0 | INSUFFICIENT_EVIDENCE |
| NEGOTIATE_CALMLY | 45/61 | 22/36 | 14/14 | 6/13 | HIGH_VARIANCE |
| SET_BOUNDARY | 4/4 | 2/2 | 1/0 | 0/0 | CONTEXT_DEPENDENT |
| ACCEPT_AND_OVERCOMMIT | 6/7 | 3/4 | 5/0 | 1/6 | CONTEXT_DEPENDENT |
| DECLINE_OVERCOMMITMENT | 2/2 | 1/1 | 0/0 | 1/0 | INSUFFICIENT_EVIDENCE |
| OWN_FAULT | 13/14 | 6/6 | 1/4 | 0/5 | HIGH_VARIANCE |
| SHARE_RESPONSIBILITY | 1/1 | 0/0 | 0/0 | 0/0 | INSUFFICIENT_EVIDENCE |
| SHIFT_BLAME | 4/4 | 2/2 | 3/0 | 0/0 | CONTEXT_DEPENDENT |
| COVER_UP | 2/2 | 2/2 | 2/0 | 0/0 | INSUFFICIENT_EVIDENCE |
| DEFER_RISK | 7/7 | 4/4 | 4/0 | 1/4 | CONTEXT_DEPENDENT |
| STAGED_DELIVERY | 3/3 | 2/2 | 1/0 | 0/1 | CONTEXT_DEPENDENT |
| ROLLBACK_AND_STABILIZE | 6/8 | 4/6 | 3/5 | 0/2 | HIGH_VARIANCE |
| FULL_FIX_NOW | 1/1 | 0/0 | 0/1 | 0/0 | INSUFFICIENT_EVIDENCE |
| TEMPORARY_MITIGATION | 2/2 | 0/0 | 2/0 | 0/0 | INSUFFICIENT_EVIDENCE |
| SEEK_MEDICAL_HELP | 4/7 | 2/4 | 2/3 | 5/2 | CONTEXT_DEPENDENT |
| REST_AND_RECOVER | 5/5 | 4/4 | 1/1 | 2/1 | HIGH_VARIANCE |
| NETWORK_HELP | 5/5 | 3/3 | 0/0 | 0/0 | CONTEXT_DEPENDENT |
| MENTOR_COACH | 5/6 | 1/2 | 1/0 | 0/4 | CONTEXT_DEPENDENT |
| PUBLICIZE_ACHIEVEMENT | 0/0 | 0/0 | 0/0 | 0/0 | INSUFFICIENT_EVIDENCE |
| STAY_LOW_PROFILE | 9/10 | 4/4 | 9/1 | 0/1 | HIGH_VARIANCE |

**Robustness finding:** no primitive meets a defensible `ROBUST_POSITIVE` or `ROBUST_NEGATIVE` standard across distinct contexts, long-chain continuations, trade-offs and hidden-risk direction. `REFUSE_UNAUTHORIZED` is still a generally appropriate boundary concept when authorization is actually absent; the Dev table does not prove it is universally optimal. `COVER_UP` has only two matched templates, so its uniform observed HiddenRisk direction is not enough for a cross-context efficacy claim. `DOCUMENT_FACTS`, `DISCLOSE_EARLY`, `NEGOTIATE_CALMLY` and rollback/staging all show benefit-cost heterogeneity. Positive/negative directions are hidden before a story choice.

## 5. Long-chain findings

1. **Opening changes the option graph — `DERIVED_DEV_ANALYSIS`.** All 151 long-chain root choices continue to a follow-up node; each long template has 2–4 root targets. Compare the current legal branch and its public implications, not an event-specific memorized path.
2. **There is no universally safe early primitive.** Across 314 paths, first and later hidden deltas frequently change direction (237 positive→later negative; 227 negative→later positive across any dimension). This is not an observable forecast.
3. **Reversibility/evidence preservation — `HYPOTHESIS`.** When two choices are otherwise comparable and facts are uncertain, preserving authorization, records, options and a recovery path is a reasonable tie-breaker. The Dev counts do not prove that it maximizes score or survival.
4. **Escalation is proportional, not reflexive.** Escalate sooner when fresh public evidence indicates imminent material harm, unauthorized disclosure, retaliation, or a continuing incident and an authorized channel exists. Immediate-escalation primitives are too sparse for a universal rule (one matched option); “wait” is not universally safer either.
5. **Recovery is a later decision, not a guaranteed branch.** Fresh follow-up evidence should update the decision; no assumption that one early choice clears hidden risk or guarantees a recovery opportunity.
6. **No stable short-term-gain→late-penalty or transparency-cost→stability mapping.** Such sequences occur in internal outcomes, but vary by dimension and path and are not visible before choosing.

## 6. Current v5 keyword / phrase trigger audit

Counts below are exact-string matches in public template text, not gold risk labels. `Templates/actions` means distinct templates and action strings containing a phrase; `action HR +/−` is the hidden post-choice direction for those phrase-bearing action strings; `alt templates +/−` counts templates having any alternative with that direction. Effects are not caused by the word.

| Cue | Phrase | Templates/actions | Action HR +/− | Alt templates +/− |
|---|---|---:|---:|---:|
| HEALTH | 健康 | 16/2 | 0/2 | 14/10 |
| HEALTH | 身体 | 15/4 | 1/0 | 14/6 |
| HEALTH | 熬夜 | 4/4 | 3/0 | 3/1 |
| HEALTH | 加班 | 16/8 | 5/0 | 14/9 |
| HEALTH | 通宵 | 1/1 | 1/0 | 1/1 |
| HEALTH | on-call | 4/2 | 1/0 | 1/1 |
| HEALTH | 值守 | 1/0 | 0/0 | 0/0 |
| HEALTH | 生病 | 2/0 | 0/0 | 2/2 |
| HEALTH | 传染 | 2/2 | 1/0 | 2/1 |
| HEALTH | 顶岗 | 1/1 | 0/0 | 1/1 |
| HEALTH | 硬扛 | 12/8 | 7/0 | 11/6 |
| HEALTH | 饮酒 | 1/1 | 0/0 | 0/0 |
| HEALTH | 作息 | 5/6 | 0/3 | 4/3 |
| HEALTH | 体检 | 1/1 | 1/0 | 1/1 |
| HEALTH | 就医 | 3/3 | 0/1 | 3/2 |
| HEALTH | 透支 | 17/3 | 3/0 | 16/9 |
| HEALTH | 疲惫 | 4/0 | 0/0 | 3/1 |
| COMPLIANCE | 合规 | 14/15 | 2/12 | 13/12 |
| COMPLIANCE | 保密 | 4/4 | 1/3 | 4/4 |
| COMPLIANCE | 泄露 | 6/2 | 1/1 | 6/6 |
| COMPLIANCE | 外传 | 4/2 | 0/2 | 4/3 |
| COMPLIANCE | 截图 | 4/3 | 0/3 | 4/4 |
| COMPLIANCE | 未授权 | 0/0 | 0/0 | 0/0 |
| COMPLIANCE | 竞对 | 3/0 | 0/0 | 3/3 |
| COMPLIANCE | 未公开 | 4/0 | 0/0 | 4/3 |
| COMPLIANCE | 客户数据 | 0/0 | 0/0 | 0/0 |
| COMPLIANCE | 内部资料 | 1/1 | 1/0 | 1/1 |
| COMPLIANCE | 监管 | 2/1 | 0/1 | 2/2 |
| COMPLIANCE | 违规 | 5/2 | 1/1 | 5/4 |
| COMPLIANCE | 绕流程 | 0/0 | 0/0 | 0/0 |
| COMPLIANCE | 安全漏洞 | 1/0 | 0/0 | 1/1 |
| TRUST | 信任危机 | 1/0 | 0/0 | 1/1 |
| TRUST | 隐患 | 26/3 | 2/1 | 26/14 |
| TRUST | 甩锅 | 5/3 | 2/0 | 5/5 |
| TRUST | 隐瞒 | 4/0 | 0/0 | 4/4 |
| TRUST | 造假 | 5/2 | 1/0 | 5/4 |
| TRUST | 报复 | 3/0 | 0/0 | 3/0 |
| TRUST | 抢功 | 2/0 | 0/0 | 2/1 |
| TRUST | 掩盖 | 3/1 | 1/0 | 3/3 |
| TRUST | 爆雷 | 1/0 | 0/0 | 1/0 |
| TRUST | 埋雷 | 0/0 | 0/0 | 0/0 |
| TRUST | 问责 | 4/0 | 0/0 | 3/3 |
| RELIABILITY | 事故 | 10/2 | 0/1 | 9/8 |
| RELIABILITY | 生产环境 | 2/0 | 0/0 | 2/1 |
| RELIABILITY | 故障 | 5/1 | 0/0 | 5/4 |
| RELIABILITY | 上线 | 11/4 | 3/1 | 10/8 |
| RELIABILITY | 回滚 | 4/6 | 3/3 | 4/4 |
| RELIABILITY | CI | 10/2 | 1/1 | 9/4 |
| RELIABILITY | 测试 | 10/1 | 1/0 | 10/7 |
| RELIABILITY | 漏洞 | 4/1 | 0/0 | 4/4 |
| RELIABILITY | 数据库迁移 | 1/0 | 0/0 | 1/1 |
| RELIABILITY | 安全 | 16/13 | 2/8 | 16/14 |

### Precision, pollution and overlap

- **High-signal cue, still not verdict:** explicit `传染` (2 templates), `泄露` (6), `外传` (4), `保密` (4), `未公开` (4), `信任危机` (1), or an actual unauthorized-data / retaliation / safety incident context merits current-candidate review. Several are rare; the event itself must establish what is actually happening.
- **Context-required:** `健康 / 身体 / 加班 / 硬扛 / 透支 / 隐患 / 合规 / 事故 / 故障 / 上线 / CI / 测试 / 漏洞 / 安全` signal inspection only. The same string has both benign and material contexts; some exact phrases are absent while variants exist.
- **Remove as standalone Risk trigger:** generic `项目 / 领导 / 同事`; also generic reliability words (`事故`, `生产环境`, `上线`, `CI`, `测试`, `安全`) without direct consequence. “Remove” means do not let the term alone promote a Risk verdict; it may remain useful to Planning or contextual scanning.
- **Generic-term pollution proxy (not measured FPR):** `安全` appears in 16 templates, only 7 also have a specific same-template security co-cue; `项目` in 47, 26 with direct delivery/scope/resource/deadline corroboration; `领导` in 51, 11 with politics/performance/compensation/consequence corroboration; `同事` in 78, 25 with conflict/credit/health/relationship-specific corroboration. The remaining counts are not proven false positives; no annotated gold labels exist.
- **False-negative boundary:** state-only scanning can miss a material breach or retaliation while public Health is currently stable; cue-only scanning can miss cumulative low Health plus an apparently ordinary workload. The current QUICK_GATE should combine fresh state, semantic cue and explicit public consequence; clear direct material consequences remain reviewable even when no listed phrase matches.
- Broad cue overlap is real: `安全 / 漏洞` straddles compliance and reliability; `背锅 / 抢功` straddles trust and organizational politics; health load and medical terms may co-occur. Keep situation semantics separate from the five-value `Risk Cue` enum.

Actual false-positive/false-negative rates are `UNKNOWN`: there is no gold label saying which 171 templates are material risk for a given public pre-state. We therefore compare failure modes, not fabricate numeric precision/recall.

## 7. Phrase-level co-occurrence patterns

Counts mean the phrases co-occur in the same node context; this is a lexical pattern scan, not a validated semantic classifier.

| Pattern | Templates / nodes / choice actions containing all | Decision |
|---|---:|---|
| 内部资料 + 外部/竞对 | 4/5/1 | `KEEP_AS_CONTEXT_CUE`; verify authorization and destination, never map to fixed answer |
| 未授权 + 数据/截图 | 0/0/0 | `REMOVE_LITERAL_PATTERN`; concept remains important, exact terms are not supported; search semantic variants, do not infer absence |
| 隐瞒 + 事故/漏洞 | 2/2/0 | `KEEP_AS_REVIEW_CUE`; low support, no action mapping |
| 甩锅 + 责任/证据 | 4/11/0 | `KEEP_AS_REVIEW_CUE`; distinguish attribution from evidence and accountability |
| 生病/疲惫 + 继续硬扛 | 9/19/1 | `KEEP_AS_CONTEXT_CUE`; check public health/trend and feasible boundary; not a fixed choice |
| 延期 + 主动同步 + 补救方案 | 1/1/0 | `DEFER`; too sparse as a phrase trigger |
| 事故 + 回滚/止损 + 复盘 | 1/3/0 | `DEFER_AS_TRIGGER`; rollback/stabilization is context-dependent |
| 被贬低 + 事实/数据回应 | 1/2/0 | `DEFER`; one template only |
| 薪资/奖金 + 先核对规则 + 再谈判 | 4/9/0 | `KEEP_AS_PLANNING_PATTERN`; confirm public terms before negotiation; no Risk escalation by itself |

Only patterns with at least two independent templates, or a clearly portable mechanism needing future validation, belong in a candidate library. Singleton patterns are not general rules.

## 8. Option-wording priors

Exact-phrase support in action wording:

| Wording | Templates/options | Long templates/options | HR +/− | Health +/− | Signatures | Prior |
|---|---:|---:|---:|---:|---:|---|
| 先瞒着 | 0/0 | 0/0 | 0/0 | 0/0 | 0 | `NEUTRAL_CONTEXTUAL` (literal unsupported; concealment variants exist) |
| 赌一把 | 1/1 | 1/1 | 1/0 | 0/1 | 1 | `NEUTRAL_CONTEXTUAL`, insufficient evidence |
| 硬扛 | 7/8 | 3/3 | 7/0 | 1/7 | 7 | cautious `NEGATIVE_PRIOR` only with health/load context; not answer |
| 全盘承担 | 0/0 | 0/0 | 0/0 | 0/0 | 0 | `NEUTRAL_CONTEXTUAL` |
| 直接公开 | 0/0 | 0/0 | 0/0 | 0/0 | 0 | `NEUTRAL_CONTEXTUAL` |
| 绕过流程 | 0/0 | 0/0 | 0/0 | 0/0 | 0 | `NEUTRAL_CONTEXTUAL`; variants may occur |
| 私下处理 | 0/0 | 0/0 | 0/0 | 0/0 | 0 | `NEUTRAL_CONTEXTUAL` |
| 立即升级 | 0/0 | 0/0 | 0/0 | 0/0 | 0 | `NEUTRAL_CONTEXTUAL`; proportionality/authority matter |
| 先核实 | 0/0 | 0/0 | 0/0 | 0/0 | 0 | `NEUTRAL_CONTEXTUAL`; the primitive occurs in wording variants |
| 分阶段 | 3/3 | 2/2 | 1/0 | 0/1 | 2 | `NEUTRAL_CONTEXTUAL`; trade-off varies |
| 回滚 | 4/6 | 2/2 | 3/3 | 0/2 | 6 | `NEUTRAL_CONTEXTUAL`; positive and negative risk updates coexist |
| 证据 | 4/6 | 3/3 | 2/4 | 0/1 | 5 | `NEUTRAL_CONTEXTUAL`; documenting evidence is not itself a guaranteed outcome |

No literal phrase is a universal `POSITIVE_PRIOR`. Context-specific process principles (verify authority, preserve evidence, bound exposure) may guide comparison, but neither words nor primitive labels select the answer. Apparent positive/negative directions are post-choice internal deltas.

## 9. Historical story-choice audit

### Recoverable identity and coverage

| Source | Recoverable story selections | Trace identity | Limits |
|---|---:|---|---|
| SCORE-01 | 71 | `7a055dea76580117ca74cddb49bb04efcf605eb1:experiments/S04-03-score-directed-integrated-run/score01_trajectory.json`; blob `0330ef9c95ea13b285a8fcfcf1b4c2c6e80ff65a`; 66,604 bytes | 98 timeline rows total: 71 event, 20 Energy, 7 Main; run/source summaries do not expose full uncontaminated causal transitions |
| Candidate v1 Run #1/#2 | 0 story selections in the committed compact trajectories | `66ec4af1e9a2a28da57c6cb8d409a6a38f87ae01:experiments/S04-04-high-score-confirmation/candidate_run1_trajectory.json` and `candidate_run2_trajectory.json` | Milestones / quarterly choices exist; story choice records do not. Original S04 raw is unavailable in repo and was not reconstructed |
| v4 Run #1 | 19 | [accepted S06-08 forensic](../runs/v4-run1-health-forensic.md); run `20260924T160806Z`, game session `fdcaa70a85f44662a6a329513c175676`; blob `cbb60024a9f76dc905f42fcf1689f61b117d01d8` | Uses committed forensic facts; no local raw reread |
| S06 Run #1 | 0 specific story selections in the compact evidence | Main-reviewed S06-01/S06-02 compact record | It supports aggregate strategy observations only; raw transcript/events unavailable |
| **Total recovered** | **90** | 71 + 19 | Not 90 independent templates, not a controlled sample |

SCORE-01 wording-only, multi-label primitive scan: share/repair 8; negotiate/coordinate 8; disclose 6; refuse/boundary 6; visibility, document, own/apologize, and accept workload 1 each. These are descriptive string classes, not quality ratings. 55 adjacent same-month event-to-next snapshots were available; 38 showed some public state difference, and 7 event choices occurred at Health ≤3. Intervening story/month transitions prevent broad causal attribution.

v4 shows several useful but non-causal contrasts: at low Health, one on-call request was handled with a bounded refusal/rule-based coordination and later Health rose from 3 to 5 amid other deltas; a confidentiality cue at Health 2 was recognized and unauthorized material refused; a sick-colleague episode at Health 4 included taking on urgent work and Health fell to 3; near M6, the Agent explicitly recognized Health 1 as material risk but chose a visibility/growth path, followed by terminal Health 0. The final `−1` source remains ambiguous. These support checking state, exposure, authorization and immediate material consequences; they do **not** make title/choice pairs, causal claims or fixed answers.

The high-score v1 Run #1 and Run #2 cannot answer which story primitive drove their divergent results: the committed trajectories do not contain story choices, and the raw artifacts are absent. SCORE-01’s low-Health windows and C/D performance descriptions likewise do not establish that any story choice caused its later score/termination. Historical evidence supports a reusable decision process hypothesis, not a score-winning primitive.

## 10. Risk Cue architecture audit

Current Risk Cue enum remains `NONE / HEALTH / COMPLIANCE / TRUST / RELIABILITY / OTHER`.

| Decision | Cue | Recommendation |
|---|---|---|
| KEEP | HEALTH | Keep as quick scan; internally distinguish workload accumulation from medical/infection facts, but do not add enum values or numeric cutoffs. |
| KEEP | COMPLIANCE | Keep; require actual authorization/data/process context, not a generic “process” word. |
| KEEP | TRUST | Keep; distinguish explicit deception/retaliation/credit dispute from ordinary disagreement. |
| KEEP | RELIABILITY | Keep; use for current incident/reliability impact, not routine CI/testing/work. |
| NARROW | OTHER | Use only when an unlisted public cue plausibly implies material consequences; it must not be a catch-all for ordinary uncertainty. |
| PLANNING_ONLY | DELIVERY | Routine delay/scope/Output gap belongs to Planning; Risk only when current public evidence shows material customer, safety, compliance or survival consequence. |
| PLANNING_ONLY | RELATIONSHIP | Ordinary friction/repair is Planning; Risk only for explicit threat, retaliation, severe harassment or comparable material consequence. |
| PLANNING_ONLY | ORG_POLITICS | Credit, visibility and opportunity trade-offs are Planning unless public evidence establishes a material threat. |
| MERGE | SECURITY / compliance overlap | Do not create a separate enum; route explicit breach/access/data facts through COMPLIANCE, with RELIABILITY also noted if service impact is real. |

Lexical cues trigger closer review, not `RECONSIDER`. Keep current full-review standard: explicit material risk + a directly relevant legal mitigation not yet handled. A fresh TIGHT/CRITICAL public survival state independently requires candidate review even if no cue word appears. A conjunction that requires both keyword and state would miss visible authorization breaches; cue-only would over-trigger.

## 11. False-positive / false-negative comparison

| Strategy | Likely false positive | Likely false negative | Assessment |
|---|---|---|---|
| cue-only | generic safety, incident, CI/testing, project/leader/colleague language gets treated as material | cumulative public Health decline with ordinary workload wording; consequences expressed without known keyword | Reject as verdict; retain only as review signal |
| state-only | every low state or routine change could block Growth despite no current material consequence | confidentiality, retaliation or ongoing production harm before public state changes | Insufficient alone; state is a constraint/input, not full context |
| cue + fresh state + explicit consequence | some ambiguous language still requires interpretation | variant/implicit wording remains possible; a strict AND rule misses cue-backed incident with currently stable metrics | Preferred QUICK_GATE model, but direct explicit material consequence or TIGHT/CRITICAL state independently opens full review |

No gold labels exist to calculate numerical FPR/FNR. The practical correction is **triage, not automation**: cue means inspect current candidate and public state; state means inspect remaining margin and timing; explicit material consequence governs Risk classification. Ordinary soft cost alone is not `RECONSIDER`.

## 12. Compressed pattern library candidate

This is a review structure for Main, not a v5 Skill edit. Cues identify situations; they do not answer the event.

| Situation pattern | High-signal cues | Prefer reasoning primitive | Avoid default primitive | Escalate when | Evidence |
|---|---|---|---|---|---|
| Confidentiality / data transfer | internal material + external/competitor, explicit authorization question | verify authority, minimize disclosure, use approved channel | informal workaround or concealment | actual unauthorized transfer, breach or retaliation is publicly evidenced | 4 co-occurrence templates; multi-outcome class |
| Integrity / concealment | concealment + incident, falsification or vulnerability | preserve facts, correct the record proportionally | cover-up / unsupported accusation | incident is ongoing or public material harm is direct | 2 templates; low-N, cue only |
| Credit / accountability | blame, evidence, ownership, contribution | document facts; distinguish owned error from misattribution; share precise credit | automatic blame shift or taking total blame | material retaliation or formal consequence appears | 4 blame/evidence templates; mixed outcomes |
| Health load / illness | repeated overtime, hard carry, illness/infection, low or falling fresh Health | check current condition, bound exposure/work, compare recovery timing | overcommit merely to appear reliable | material medical/infection consequence or Survival TIGHT/CRITICAL | 9 fatigue+hard-work co-occurrence templates; history includes ambiguous attribution |
| Delivery delay / scope | delay + changed scope / deadline / customer impact | verify scope, communicate facts, propose bounded next step | promise everything or conceal delay | explicit severe customer, safety or compliance impact | categories broad; three-phrase pattern only 1 template, candidate remains contextual |
| Reliability incident | outage/bug/deployment + rollback/stabilize | establish impact, preserve evidence, compare mitigation vs full fix | bypass verification or escalate without facts | ongoing production/security/data harm is public | reliability/security classes heterogeneous; one rollback phrase co-occurrence |
| Compensation / career negotiation | salary/bonus/offer + rules/terms | verify public terms, compare total opportunity cost, negotiate calmly | irreversible commitment on an unverified assumption | binding/confidential material issue, otherwise Planning only | 4 salary+rule-check+negotiation templates |
| Relationship boundary / repair | explicit insult, recurring conflict, request to cover work | separate fact, boundary and repair; compare two proportionate options | reflexive public escalation or people-pleasing | threat, retaliation or severe harassment is explicit | broad context classes; no universal primitive outcome |

The last four are reasoning scaffolds, not statistically validated policy. In particular singleton delay, rollback and insult phrase combinations are hypotheses and should not be promoted to hard triggers without new cross-template evidence.

## 13. General story decision framework (≤6 steps)

1. Identify the current situation from visible text; do not classify by memorized event title.
2. Read fresh public survival state, trend, warning, authorization and immediate consequence; keep unknowns explicit.
3. Compare the event with the current Primary Gap, without letting ordinary local emotion replace long-horizon strategy.
4. Compare at most two strongest legal candidates on direct public benefit, material risk, reversibility/evidence preservation and soft opportunity cost.
5. Use proportionate review/escalation only when public facts justify it; uncertainty is not proof of safety or proof of harm.
6. Submit once as Single Agent; after the result, fresh-observe and retain only directly attributable public effects.

This is `ADOPT_CANDIDATE` for a later static integration review; gameplay benefit is `NOT_PROVEN`.

## 14. Candidate event-policy decisions

`ADOPT_CANDIDATE` below means propose to Main for a future candidate review, not implement now.

| Rule | Evidence / runtime-visible inputs | Expected benefit / failure mode | Decision and “must not encode” |
|---|---|---|---|
| Situation patterns as retrieval cues | current event / option text | Focus review; can misread ambiguous language | ADOPT_CANDIDATE; no title or event-id lookup |
| Fresh state + cue + consequence Risk triage | fresh observe, Survival band, current candidate, direct warning | Balance FP/FN; stale state undermines it | ADOPT_CANDIDATE; no keyword-alone verdict or hidden-risk estimate |
| Hard material consequence can independently trigger review | explicit public breach, threat, terminal warning | Avoids strict cue/state AND miss; over-escalation if “material” is guessed | ADOPT_CANDIDATE; preserve candidate-specific mitigation standard |
| Bounded evidence / authorization checks | visible source, destination, permission and current consequences | Reduce unsupported commitment; can delay action if overused | ADOPT_CANDIDATE; no universal refusal/disclosure answer |
| Health load vs medical cue distinction | fresh Health/trend, illness/infection/workload wording | Catch cumulative exposure; false positive if any work is treated as danger | ADOPT_CANDIDATE as semantic distinction, not extra Risk enum |
| Ordinary delay/scope/relationship belongs to Planning | current Primary Gap, visible delivery/relationship context | Avoid Risk over-trigger; may miss a real consequence unless escalation rule remains | ADOPT_CANDIDATE with explicit material-consequence exception |
| Literal phrase expansion / normalizer | current public wording variants | Could improve recall; creates generic-term pollution | DEFER pending annotated examples / better boundary evidence |
| Hard-push/concealment negative priors | wording + current state/situation | May flag hazardous self-exposure; can overfit a tiny phrase sample | DEFER; no action ranking from hidden Dev deltas |
| Universal “verify/document/disclose/escalate” ranking | primitive labels alone | Attractive simplicity; context and trade-offs vary | REJECT |
| Fixed opening / path recovery / event answer / hidden outcome lookup | event ID/title or post-choice `status_updates` | Apparent consistency is dataset leakage | REJECT |
| Fifth Skill, Memory, Team/Swarm, second submitter | not needed to express bounded cues | More context/architecture without evidence | REJECT for this evidence set; existing architecture remains unchanged |

## 15. Unknowns and DO_NOT_ENCODE

- There is no gold material-risk annotation or public-state-conditioned label; actual keyword coverage, FPR and FNR remain `UNKNOWN`.
- Hidden Dev outcome vectors do not reveal the choice-time public signal that justifies a choice; cloud/test transfer and runtime availability frequencies are unknown.
- Phrase variants, paraphrase coverage and Chinese contextual negation are incomplete; exact-string zero means only “not found exactly”.
- Historical raw S04 transcripts/events were not in the repository; v1 #1/#2 story selections and S06 Run #1 detailed event path remain unknown.
- Run transitions often include month processing, follow-up event nodes, review or other actions; adjacent state difference is not automatically a choice effect.
- `DO_NOT_ENCODE`: event title/ID→choice; hidden `status_updates` lookup; copied high-score-run choice; one word→Material Risk; exact outcome signature vectors; fixed long-chain paths; hidden thresholds, evaluator weights or test/private-data guesses; a large keyword dictionary that bloats runtime context.
- No v5 Skill, candidate config, instruction, Runner, dependency, `CURRENT_STATE`, `STRATEGY_EVIDENCE` or `RUN_HISTORY` was edited. This review does not claim score gain, stable 80+, causal action benefit or S06 completion.

## 16. Inputs for S06-15

- Use only exact identity-matched historical public pre-state/action/result records; mark missing story records `UNKNOWN`, not reconstructed.
- Compare counterfactuals only where choice, phase, month, fresh public state and follow-up window are sufficiently matched; otherwise report non-comparable.
- Separate post-choice state changes from monthly/review/event-chain effects; retain attribution confidence.
- Use this review’s patterns as candidate strata, never as event answers; prioritize what public information existed before the choice.
- Keep score/survival outcomes descriptive unless a controlled comparison isolates the decision.

## Verification boundary

- Public event templates decoded: 171/171; choices 974; no decoder errors observed.
- Only public Dev event directories were read; no test/private data, game, provider, service, install/reload, MCP, gameplay or live session was used.
- Historical references point to committed Git objects and the accepted committed v4 forensic; missing raw and trajectory fields remain explicitly unknown.
- This report is the only authorized changed file. It is not a policy installation or game authorization.

## Recommendation

`RETURN_TO_MAIN_FOR_S06_15_HISTORICAL_COUNTERFACTUAL_REVIEW`
