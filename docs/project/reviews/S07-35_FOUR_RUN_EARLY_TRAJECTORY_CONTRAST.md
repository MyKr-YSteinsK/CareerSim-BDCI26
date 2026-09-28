# S07-35｜四轨迹前 18 个月公开证据对照

## 范围、身份与证据等级

主窗口 M1–M18；M24 只核对延续，v1 #2 的 M25 终局只划定存活边界。本报告只使用参赛者可见状态、行动、反馈和已提交的运行取证。`HiddenRisk` 数值、DB、模拟器内部规则、隐藏阈值及解码事件效果均未用于策略比较。四局各只有一次轨迹，不能将相关性当因果。

| 角色 | Candidate / game session | 结果 | 当前证据等级 |
|---|---|---|---|
| Positive A：v6 #1 | `candidate-v6-auditable-control-loop` / `7b59b85ad19b4597927cf50fc716f9ac` | 75.29 / 52.70 / 48m / A | 本机 raw 3/3 存在，bytes/SHA-256 与 [S07-34](S07-34_V6_V7G_EARLY_TRAJECTORY_COMPARISON.md)一致 |
| Positive B：v1 #1 | `candidate-v1-four-skill` / `2224f5df228544e699b10f897d333d4b` | 76.04 / 53.23 / 48m / A | `RAW_UNAVAILABLE_FOR_V1_1`；使用 Git 历史提交的派生轨迹与 S04-03 RESULT 历史版本 |
| Same-policy control：v1 #2 | 同一 frozen v1 Candidate / `7df157117cf14917bdc42d83fb7ac7d2` | 35.31 / 24.72 / 25m / D | `RAW_UNAVAILABLE_FOR_V1_2`；使用 Git 历史提交的派生轨迹与 S04-04 RESULT |
| Target：v7g #1 | `candidate-v7g-compact-skill-contracts` / `d4464a311c924e73b9e23eebd6f71f6d` | 54.52 / 38.17 / 48m / C | 本机 raw 3/3 存在，bytes/SHA-256 与 S07-34 一致 |

v1 #1 的历史来源是 `7a055dea76580117ca74cddb49bb04efcf605eb1:experiments/S04-03-score-directed-integrated-run/{RESULT.md,run_evidence.json}` 及 `66ec4af1e9a2a28da57c6cb8d409a6a38f87ae01:experiments/S04-04-high-score-confirmation/candidate_run1_trajectory.json`；v1 #2 使用同一 S04-04 提交的 `RESULT.md`、`confirmation_evidence.json`、`two_run_comparison.json`、`candidate_run2_trajectory.json`。派生轨迹的 game/drive session 与 [RUN_HISTORY](../RUN_HISTORY.md)一致，登记的原 raw bytes/SHA-256 与本 Task Plan 一致；这些是**历史登记身份**，不是本轮重新哈希 raw。指定 v1 raw 路径及 `.local` 内同名 events 搜索均无文件，因此 v1 的逐事件反馈、v1 #2 的 M18 月末状态及两局压缩时点若未保存在派生物中，均记 `UNKNOWN`。历史 JSON 的部分中文行动名发生乱码，类别以 S04-04 RESULT 的人工可读计数和季度选项交叉核对；不从乱码猜事件语义。v1 相关结论置信度比四局 raw 齐备时降低一级。

本机 v6 raw 三件：events `2,061,570 / 2cce87eb6afd8aea5a9651f75621ae7c2b303e8c00c7f2ac417dc65c030371d8`，transcript `822,693 / 13bd4de5fc9b9a25b564072125cb0d373b92402cf5f28d59e4930b96a741fda0`，score `2,722 / 277809fbdae10d2242fd6a3ecbee3731c7ece2be1b5d7e8222b4115c60517d37`。v7g 对应 events `1,903,318 / 73cb4de9f2568e343be252630a64dbef289e92aec121bae07ef8fbd3a6cff3c4`，transcript `641,028 / d3f879a9ecc01c845bac70468bbceba8634dbfc28826da445e8b2e73e79f46b7`，score `2,755 / 52ee2bb53653c805ce724137087dc395883ae8ee0d03afab4f969e1bf173fffe`。本机路径、v6 score 副本空 `session_id` 的限制见 S07-34。v1 历史登记的 raw bytes/SHA-256 分别为 #1 events `2,027,675 / a964db295f0135f4dc41f135b3ed3d8513a196fbbb689f36d47f76c957ef7d79`、transcript `753,385 / 49cbfcee32dd88d1573d4e0a068de543e3993d45384dc72854bfa91aaebfec71`、score `2,998 / 034a8bb6f04bc961f5c733b92e311de7df4700db7eea5a4843eef4536447ccbe`；#2 events `1,019,202 / 9a266a84937b40899b6f2fdcbbb8fdefd74c825e57dd1ea484e52c6e4b9e22b6`、transcript `312,900 / 9f3082d4decb46f8e64c6ff6df736900cf8d4810ff528d37ee3f0451581a66b0`、score `2,953 / cfe7f11e18fd62d6d345e6b8498d9fcb04baf421a016e00e5bf46f263909531c`。

## 为什么用四局：结果与里程碑

两条 75+ 高分局并非同一 Candidate；两条 v1 局则共用冻结 Candidate，却相差 40.73 定量分和 23 个月生存期。前者用来找公开行为交集，后者检查交集是否足以解释高分。以下月度值是**月末**公开状态，顺序 `Level / Health / Skill / Network / Output / Wealth`；v1 #2 的派生物只有稀疏里程碑，缺失月份绝不插值。v6/v7g 的 M6/M12/M18 正式评审时点另见 S07-34，不能把本表月末变化倒填到先发生的评审。

| Run | M1 | M3 | M6 | M9 | M12 | M15 | M18 | M24 |
|---|---|---|---|---|---|---|---|---|
| v6 #1 | L1/5/3/4/-1/1 | L1/6/9/3/3/1 | L2/6/11/3/5/3 | L2/5/20/7/5/3 | L3/5/23/8/7/4 | L3/6/33/19/13/6 | L4/9/38/19/17/8 | L4/8/61/30/26/11 |
| v1 #1 | L1/5/4/4/0/1 | L1/6/9/3/3/1 | L2/7/13/5/6/2 | L2/7/20/7/6/3 | L3/7/24/7/7/4 | L3/10/35/15/14/6 | L4/10/44/19/16/6 | L4/8/63/36/26/10 |
| v1 #2 | L1/4/1/4/0/1 | UNKNOWN | L2/10/12/5/6/2 | UNKNOWN | L3/9/24/8/10/3 | UNKNOWN | L3；其余状态 UNKNOWN | L4/10/43/19/13/9 |
| v7g #1 | L1/5/3/1/-1/1 | L1/5/8/3/0/1 | L1/5/9/3/3/2 | L1/5/9/3/3/3 | L2/4/10/6/6/3 | L2/6/21/7/6/4 | L3/7/26/6/7/6 | L3/8/41/19/16/7 |

| Run | M6 正式评审 | M12 正式评审 | M18 正式评审 | 边界 |
|---|---|---|---|---|
| v6 #1 | C；L1→L2 | B；L2→L3 | B；L3→L4 | 48m 完成 |
| v1 #1 | 晋 L2；历史规划摘要记 C | 晋 L3；确切反馈措辞 UNKNOWN | 晋 L4；确切反馈措辞 UNKNOWN | 48m 完成 |
| v1 #2 | 晋 L2；历史规划摘要记 C | 晋 L3；历史摘要提及后续 B 反馈，但精确时点/措辞 UNKNOWN | 未晋；确切反馈措辞 UNKNOWN | M24 才晋 L4，M25 trust-crisis 终止 |
| v7g #1 | C；未晋，观察名单 | C；晋 L2，“忙≠赢” | B；晋 L3，仍要更清晰成果 | 48m 完成 |

**Q1 / Q2：** M6/M12/M18 连续晋升是两条高分局的共同**进阶 marker**，但 v1 #2 也在 M6/M12 晋升，且 M12 Output=10，高于两条高分局的 7；所以早期晋升与 Output 既不是 48m 高分的充分条件，也不能从终局反推出晋升规则。两条高分与 v1 #2 在 Q1/M3 都做了两次成果材料准备、M6 月末 Output 分别为 5/6/6；v7g Q1 无成果材料准备、M3 Output=0、M6 月末 Output=3。这是公开可见的早期**差异候选**；v1 #2 的后续失利限制其解释范围。v6 与 v7g 的 M6 评审当下 Health/Skill/Output/Dignity 相同，晋升却不同；v1 历史派生数据没有可比较的完整评审前状态与所有 Story 机会。因此 `M6_PUBLIC_CAUSE_UNRESOLVED`。

## Positive intersection、同策略方差与目标缺口

**Positive intersection。** v6、v1 #1 都在 M3 前投入至少两点成果材料准备；M3 月末 Skill=9、Output=3；M6/M12/M18 连续晋升；Q1–Q6 全部申请关键项目。两局在 M12→M18 的公开 Skill、Network、Output 都大幅增长，月末 M18 分别为 v6 `38/19/17`、v1 #1 `44/19/16`。这是 `POSITIVE_COMMON_PATTERN`，其中 Main 行为和早期晋升并不独占于高分局。

**Same-policy divergence。** v1 #1/#2 在 M6、M12 同步晋升且都经历三个规划 checkpoint；前六季 Main 分别 6/6 与 5/6 申请关键项目，#2 唯一低调避险在 M12。v1 #2 的 M12 Skill=24、Network=8、Output=10，甚至不弱于 #1 的 `24/7/7`，但 M18 未晋；M24 才到 L4，M25 发生第二次 trust-crisis 并终止。这把“早期状态/规划/晋升复现”与“长期存活、高分”分开。两局 M13–M18 的 Energy 从 #1 的汇报 4、人脉 2 变为 #2 的汇报 1、恢复 3、清雷 2 点；但 #2 的 Story/风险机会与逐月状态缺失，不能将后来失败归于这组投入差异。标记 `SAME_POLICY_STABLE`（规划 checkpoint、早期晋升、关键项目偏好）与 `SAME_POLICY_VARIABLE`（后段资源分配、M18 晋升、存活/财富）。

**v7g gap。** v7g 在 Q1 用 2 点清雷、1 点恢复，M3 公开 HR 风险提醒且清雷前 Health=3，有正当的公开防御依据；不能称其无端保守。其 Q1 缺成果材料准备、M3 Output=0，M6 首次评审未晋。M7–M18 G 名称持续“更清晰的成果”，但季度 Energy 高强度累计 8/18 点，正式反馈在 M12/M18 仍指出结果呈现不足。与此同时 v7g M12/M18 也晋升，并有客户分阶段交付及 Demo 邮件等正向公开行为；不能说它完全没有兑现。差距包含评审机会、Story 路径和行动取舍，贡献无法拆分。

## Q3–Q5｜反馈、Energy 与结果兑现

下表区间是相邻正式评审的**下一窗口**。v1 行只写历史派生物能支持的反馈；精确逐事件行动链缺失时保留 `UNKNOWN`。`result` 是公开快照/反馈，不等于评审明确承认某个行动。

| Run / 反馈起点 | 下一窗口目标 | Story / Energy / Main | 公开结果与下一评审 |
|---|---|---|---|
| v6 M6：C、已晋，亮点不突出 | 旧版自由文本提 Output；逐行动目标 UNKNOWN | M7–M8 客户 Demo 修复/带教；Q3 恢复、汇报、人脉；关键项目 | M12 评审 S/N/O=20/4/5，B、晋 L3；单件交付归因 UNKNOWN |
| v1 #1 M6：C，健康低，需更清晰 Output | 历史 rolling-planning 记录恢复 Health、提高可见 Output | Q3 汇报、恢复、人脉；关键项目；具体 Story/回执缺失 | M12 月末 S/N/O=24/7/7，晋 L3；公开评审是否认可特定交付 UNKNOWN |
| v1 #2 M6：C；已晋 | 历史 checkpoint 称调整 Output/Network 优先级 | Q3 恢复×2、汇报；关键项目；逐件 Story 缺失 | M12 月末 S/N/O=24/8/10，晋 L3；显示有结果但不能证明长期存活 |
| v7g M6：C、未晋，要更清晰成果 | G 固定为“更清晰的成果” | 发布回滚/客户延期与分阶段交付；Q3 高强度、汇报；关键项目 | Q3 两项 Energy 后 O 均未增长；M12 C、晋 L2，仍称“忙≠赢” |
| v6 M12：B、晋 L3 | 精确逐行动目标 UNKNOWN | M13–M15 协作、容量报告；Q5 恢复、汇报、心理修复；关键项目 | M18 评审 S/N/O=37/16/14，B、晋 L4 |
| v1 #1 M12：晋 L3，精确措辞 UNKNOWN | 历史 checkpoint 只覆盖较早窗口；此处 UNKNOWN | Q5 汇报×2、人脉；关键项目；具体 Story/回执缺失 | M18 月末 S/N/O=44/19/16，晋 L4 |
| v1 #2 M12：晋 L3，精确措辞 UNKNOWN | checkpoint 提及后续 B 与 Network/Output/Risk，但确切时间 UNKNOWN | Q5 恢复×2、汇报；关键项目；具体 Story/回执缺失 | M18 未晋；月末 S/N/O 与评审原因 UNKNOWN |
| v7g M12：C、晋 L2，“忙≠赢” | G 仍为“更清晰的成果” | 架构评审/风险文档/Demo 邮件/自研；Q5 高强度、汇报；关键项目 | M18 评审 S/N/O=21/3/6，B、晋 L3；成果清晰度仍被提示 |

Energy 表按**实际耗费点数**，非动作次数；顺序 `高强度 / 汇报 / 人脉 / 健康 / 心理 / 清雷`。每段每局 6 点。v1 季度行动来自历史派生物，类别同时与 S04-04 RESULT 的总次数交叉核对；v6/v7g 来自 S07-34 已核验公开行动序列。

| 区间 | v6 #1 | v1 #1 | v1 #2 | v7g #1 |
|---|---|---|---|---|
| M1–M6 | 0/2/0/2/0/2 | 0/2/1/3/0/0 | 0/2/3/1/0/0 | 2/0/0/2/0/2 |
| M7–M12 | 2/1/2/1/0/0 | 0/2/1/3/0/0 | 0/1/2/3/0/0 | 2/2/0/0/0/2 |
| M13–M18 | 2/2/0/1/1/0 | 0/4/2/0/0/0 | 0/1/0/3/0/2 | 4/1/1/0/0/0 |
| **18 点总计** | **4/5/2/4/1/2** | **0/8/4/6/0/0** | **0/4/5/7/0/2** | **8/3/1/2/0/4** |

两条高分局共有“Q1 汇报 2 点”，但没有稳定的**全期** Energy 配方：v6 高强度 4 点且清雷 2 点，v1 #1 两者均 0；低分同策略 v1 #2 同样没有高强度，并在 M6/M12 晋升。v7g 高强度最多、汇报/人脉最少，是 target gap，但“少做高强度就高分”被 v1 #2 反驳。Q1 v7g 恢复/清雷有公开风险与 Health 信号；必要恢复不能计为错误。结果兑现候选只应比较投入之后的公开 Output、交付回执与下一次评审文字，不能只数汇报动作。

## Q6–Q10｜Network、Main、存活风险、机会与推敲

| Network 月末 | M1 | M3 | M6 | M9 | M12 | M15 | M18 |
|---|---:|---:|---:|---:|---:|---:|---:|
| v6 | 4 | 3 | 3 | 7 | 8 | 19 | 19 |
| v1 #1 | 4 | 3 | 5 | 7 | 7 | 15 | 19 |
| v1 #2 | 4 | UNKNOWN | 5 | UNKNOWN | 8 | UNKNOWN | UNKNOWN |
| v7g | 1 | 3 | 3 | 3 | 6 | 7 | 6 |

**Network。** 两条高分到 M18 同为 19，但 v1 #2 在 M6/M12 的 5/8 并不低，v7g 到 M3/M6 与 v6 相同。v6 的领先主要在 M7–M9 与 M13–M18 出现；v1 #1 的 M13–M18 人脉维护 2 点，v6 同段 0 点却也涨至 19。故 Network 状态是晚些时候的伴随特征，不是稳定的开局投入配方；v1 #2 M18 状态缺失进一步限制区分力。

**Main。** Q1–Q6，v6/v1 #1/v7g 均 6/6 申请关键项目；v1 #2 为 5/6，唯一例外是 M12 低调避险，且当月已晋 L3。相同 Main 选择覆盖高分、低分与 target；`MORE_KEY_PROJECTS_ONLY = REJECTED_AS_PRIMARY_FIX`。不同初始状态及 Story/机会可能改变同名行动的可见结果。

**风险与存活。** v1 #2 的终局是 M25 第二次 trust-crisis；M1–M18 派生物只有 Q6 清雷 2 点、规划/risk-review 文字和稀疏状态，没有足够逐事件公开警示链证明早期已可预见 M25 终止。v1 #1 也曾公开 Health=3（Q2/Q4 Energy 前）并恢复，说明恢复本身不是低分标记。v7g Q1 清雷及 v6 Q2 清雷也各有公开警示/风险语义。`EARLY_SURVIVAL_FRAGILITY_SIGNAL=UNKNOWN`；M25 结果不能倒推为 M3 或 M12 的确定性风险阈值。

**Story 机会。** v6/v7g 各有 55 次 M1–M18 Story 选择，原始标题按字面去重分别为 39、37 个，交集 10 个；客户 Demo、回滚、跨组架构、带教/容量报告等题材不同，S07-34 已逐段记载。这是两局字面标题统计，不是事件 ID 匹配或有利/不利机会计数。v1 #1 派生物的逐月事件标题乱码、v1 #2 没有完整事件列表，无法严谨计算四局 M1–M18 distinct theme 数或语义类别交集。历史 S04-04 报告曾在 v1 #1 与另一 SCORE-01 的 M1–M24 比较中发现月份+标题精确重合仅 6 项；这只说明机会路径可能差异大，**不是四局匹配统计**，更不能将差异直接归因 RNG。四局 event-opportunity contribution 保持 `UNKNOWN`。

**规划、反复推敲与压缩。** v1 #1/#2 都有三个被历史报告确认的 rolling-planning checkpoint，却高低分分化，规划出现不是充分条件；v1 #2 Board 刷新也仅 `PARTIAL`。v6/v7g 的 M6/M12 差早于首次压缩，v7g M1–M18 的 G 仅在 M6 正式反馈变一次，且早期 `reconsider` 字面次数少于 v6（158 vs 353），见 S07-34。v1 两局 raw transcript 缺失，不能公平比较 reconsider、候选翻转或压缩时点。v6/v7g 后续压缩未重读 Skill 是 `runtime correctness`，不是已证明的前期分数原因；重复推敲最多可认定 `token efficiency`，action-level decision impact `UNKNOWN`。

## 跨局模式矩阵

`POSITIVE_COMMON_PATTERN` 只表示两条高分均出现；`SAME_POLICY_STABLE/VARIABLE` 描述 v1 双局；机制是否足以区分高低分另在下一节判断。`?` 表示历史证据不可恢复。

| Pattern | v6 high | v1 #1 high | v1 #2 same-policy low | v7g target | 描述性 verdict |
|---|---|---|---|---|---|
| M6 晋升 | 是 | 是 | 是 | 否 | `POSITIVE_COMMON_PATTERN`，亦 `SAME_POLICY_STABLE`；非最终高分充分条件 |
| M12 晋升 | 是 | 是 | 是 | 是 | 四局均有，不区分最终结果 |
| M18 晋升 | 是 | 是 | 否 | 是 | `POSITIVE_COMMON_PATTERN`；低分 control 缺失，target 具备 |
| 早期可见 Output | M3=3 | M3=3 | M3?；M6=6 | M3=0 | 两高分共同；control M6 也强，M6 原因未解 |
| Q1 汇报/成果准备 | 2 点 | 2 点 | 2 点 | 0 点 | 三晋升局共有，target gap；非长期高分充分条件 |
| Network 投入 | 18 月 2 点 | 4 点 | 5 点 | 1 点 | 有差，配方 `SAME_POLICY_VARIABLE`；control 并不低 |
| 高强度工作 | 4 点 | 0 点 | 0 点 | 8 点 | target 最多；两高分无共同固定配方 |
| 恢复/清雷 | 4/2 点 | 6/0 点 | 7/2 点 | 2/4 点 | 四局均有风险/恢复取舍，状态需求不同 |
| Key-project Main | 6/6 | 6/6 | 5/6 | 6/6 | `SAME_POLICY_STABLE` 偏好；不区分高低 |
| 正式反馈后行动 | M7–M18 有公开响应 | 三规划 checkpoint/资源响应 | 三 checkpoint，M12 前 Output=10 | G 稳定但结果反馈反复 | 四局都有某种响应；兑现机制不确定 |
| Delivery/result evidence | Demo/容量报告有可见 S/N/O | 逐件回执缺失；状态增长 | 逐件回执缺失；M12 O10 | 客户分阶段交付/Demo 邮件亦有正向变化 | 不能说 v7g 完全缺交付 |
| Review objective 稳定 | 旧 CTRL 精确配对? | checkpoint 存在 | checkpoint 存在 | M6–M18 G 稳定 | marker 稳定非高分充分条件 |
| Survival/risk handling | 48m；有警示/恢复 | 48m；低 H 曾恢复 | M25 trust-crisis；早期原因? | 48m；Q1 风险清理 | 早期存活机制 `UNKNOWN` |
| Reconsideration | 早期字面 353 | ? | ? | 早期字面 158 | 不支持 v7g 独有推敲导致低分 |
| Compression 时点/恢复 | 首次晚于 M12，恢复失败 | ? | ? | 首次 M18，恢复失败 | 两局已知者的 M6 分叉先于压缩 |
| Public-only evidence discipline | 精确数值主张曾出现 | ? | ? | 精确数值主张曾出现 | 规范问题确定；四局相对频率不可比 |

## 机制分类与 v7h 适用性

| 机制 | 分类 / 置信度 | 最强证据 | 最强反证、环境解释及下一局可观测量 |
|---|---|---|---|
| Q1 成果材料与可见结果进入首次评审 | `PROMISING_BUT_NOT_DISCRIMINATIVE` / LOW | v6、v1 #1 及 v1 #2 Q1 均汇报 2 点并在 M6 晋升；v7g 0 点、M6 未晋 | v1 #2 最终低分；v6/v7g M6 评审 H/S/O/D 相同；Story 机会不同。适合 **一个有界实验**：观察 Q1 报告是否有公开依据、M3/M6 评审前 Output 与具体交付、M6 正式反馈；不可固定选择 |
| 正式反馈→下一评审可核验交付 | `UNKNOWN` / LOW | 两高分后续 S/N/O 增长、v7g 继续收到成果不清晰反馈 | v1 #2 M12 O10、仍后来失败；v1 两局逐件回执缺失。可作后续研究，不能先声称 high-run 独有 |
| 减少高强度、增加汇报/人脉 | `SAME_POLICY_VARIABLE` / LOW | v7g 高强度 8 点、汇报+人脉 4 点；两高分后者较多 | v1 #2 高强度 0、汇报+人脉 9 点仍低分；Health/事件需求不同。可作为实验测量维度，非既定优化配方 |
| 早期晋升 tempo 是稳定高分机制 | `PROMISING_BUT_NOT_DISCRIMINATIVE` / LOW | 两高分 M6/M12/M18 连续晋升 | v1 #2 M6/M12 晋升仍低分；v7g M12/M18 晋升仍 C。只作 marker，不作机制修复 |
| 更多关键项目即可弥补 v7g | `REJECTED` / HIGH | 三局 Q1–Q6 都 6/6，结果差 | 无区分价值；不适合作为 v7h 单独 patch |
| G churn / Story 重开 / 压缩造成 M6 未晋 | `REJECTED` / HIGH（仅 M6 时间命题） | v7g G 早期仅评审后改变；M6 在首次压缩前 | v1 逐项推敲与压缩缺 raw，不能扩大成四局长期否定；恢复仍需单独修复 |
| 公开字段白名单与压缩恢复 | `UNKNOWN` / LOW（四局机制归类） | v6/v7g 都有精确风险主张或后续恢复缺口，各自正确性问题已证实 | v1 同类频率未知；适合独立的合规/正确性验收，不适合作为本次单机制得分实验的混合变量 |

**严格的机制结论：** 没有任何 M1–M18 项同时满足“两高分支持、v7g 缺失、同策略 control 能区分最终高低分、非机会差异、可见行动→结果链接”全部条件，因此本轮没有 `CROSS_RUN_SUPPORTED` 得分机制。已知两局的正确性缺口应独立修复，其四局可比性及分数效应均未知。

## 24 项改进方向重新处置

仓库及任务附带目录未找到 `v7h前改进方向确认清单.md`，因此下表是依据本 Task Plan 列出的主题**重建的 24 项 mapping**，不是对缺失原文件的逐字编号复刻。`CONFIRMED` 仅指足以进入下一轮有界实现/实验或独立正确性修复，不指因果证明。每行记录了四轨迹带来的关键限制。

| # | Plan 主题拆分的方向 | 处置 | 四轨迹依据 / 限制 |
|---:|---|---|---|
| 1 | M1–M6 early progression 总体提速 | `DEFERRED` | 三局 M6 晋升，v1 #2 后来仍低分；原因未解 |
| 2 | M3/M6 评审前公开 Output 与成果材料联动 | `CONFIRMED` | 三晋升局 Q1 汇报 2 点、v7g 0；可做单机制观察，效果未知 |
| 3 | 反推 M6 晋升所需状态或门槛 | `STILL_UNKNOWN` | v6/v7g 评审时 H/S/O/D 相同却结果不同 |
| 4 | 单独压低高强度工作作为得分修复 | `REJECTED` | v1 #2 高强度 0 仍低分 |
| 5 | formal feedback→下一窗口行动 | `DEFERRED` | 四局有不同程度响应；逐件认可链不全 |
| 6 | Delivery→Evidence→Recognition 明确兑现 | `DEFERRED` | v7g 正向交付存在，v1 历史逐件回执缺失 |
| 7 | 季度 Energy 预算控制器 | `DEFERRED` | 配方差异大，不能先定固定比例 |
| 8 | 汇报/成果准备的条件触发 | `DEFERRED` | Q1 共性明显，长期 v1 #2 反证充分性 |
| 9 | Network 低配修复 | `DEFERRED` | v7g 中后段较低；v1 #2 M12 N8 仍低分 |
| 10 | Health 恢复优先级 | `DEFERRED` | v1 双局均恢复较多，结果分化；须按公开风险 |
| 11 | Dignity/心理修复策略 | `STILL_UNKNOWN` | M1–M18 有关证据稀少，无法比较效果 |
| 12 | 历史埋雷清理时机 | `DEFERRED` | v7g Q1 有明确公开警示；v1 #2 Q6 清雷与终局不能倒推 |
| 13 | 将 pre-review 防御支出一概判为过度 | `REJECTED` | v7g Q1 HR 风险与低 Health 可见 |
| 14 | 增加 key-project Main 频率 | `REJECTED` | 三局 6/6，v1 #2 5/6，仍高低分分化 |
| 15 | Wealth floor 的早期触发/收益 | `STILL_UNKNOWN` | v1 #2 M25 低财富，但 M1–M18 可比链不足 |
| 16 | Survival floor 能否预防 trust-crisis | `STILL_UNKNOWN` | v1 #2 终局不能反推早期可见警示 |
| 17 | 公开 warning 驱动的风险动作 | `DEFERRED` | v7g/v6 有警示，v1 逐事件缺失；可定义观察条件 |
| 18 | G/P 状态控制 | `DEFERRED` | v7g M1–M18 G 稳定，P 转换有部分真实风险 |
| 19 | Story reopening 作为早期得分主因 | `REJECTED` | v6 早期字面次数更多；候选翻转仍 UNKNOWN |
| 20 | public-field whitelist | `CONFIRMED` | v6/v7g 都有精确风险数值主张；属证据合同修复 |
| 21 | 排除 numeric HiddenRisk 推理 | `CONFIRMED` | 同上，不能假称带来分数提升 |
| 22 | compression 后 Skill/状态恢复 | `CONFIRMED` | v6/v7g 后续恢复不符合合同；与 M6 差分开 |
| 23 | Board same-session freshness 核验 | `STILL_UNKNOWN` | v1 #1 未证、#2 PARTIAL；v7g 需独立验证 |
| 24 | “少加概念，多加约束” | `DEFERRED` | 可作为 patch 范围原则，非四局实证收益结论 |

处置计数：`CONFIRMED 4 / REJECTED 4 / DEFERRED 11 / STILL_UNKNOWN 5`。若 Main 提供原 24 项清单，须重新按原句逐项对照，不能把本表冒称原清单验收。

## 根因综合、候选与下一步

**最强候选（≤3）。** 只有一个用于下一次得分实验的候选：**在 Q1 至首次正式评审之间，把已有的公开交付转为可核验成果材料，并记录行动前依据、下一条 Output/回执、M6 正式反馈。** 两高分与同策略低分局均有 Q1 汇报 2 点，v7g 没有；这提供可观察的早期分叉，但 v1 #2 后来低分、v6/v7g M6 评审状态接近，故置信度 LOW。它是待证伪的单机制假设，不是固定选项脚本。另两项——公开字段白名单、压缩后恢复——是有独立证据的合同正确性修复，应另立验收，不与得分实验捆绑；本 Task 不实施。

**为什么尚不能排除机会路径。** v1 #1/#2 Candidate 相同仍大幅分化，而完整 Story raw 已缺；v6/v7g 已知事件题材不同，且 M6 首次评审可见状态相近却结果不同。只凭四局终局或汇报次数，无法区分先前行动、事件机会、状态交互。下一实验应预先定义公开触发/观测和失败边界，记录机会差异；若相同机制在不同公开路径下无法产生可见交付或评审改善，应撤回假设。

**被排除的高关注方向。** 更多关键项目、机械削减高强度、把有公开警示的 Q1 防御一律视为错误、把 v7g 早期 G churn/反复推敲/首次压缩当作 M6 未晋原因。前者无区分度，后者与时间顺序或现有公开证据相冲突。

**仍未知。** M6 真正晋升原因；v1 #2 M18 逐状态/反馈；四局可比 Story 机会集合；具体交付与正式评审认可的链接；同策略方差中环境与行动各自贡献；v1 两局逐项推敲、压缩和早期风险警示。v1 raw 缺失使本 Task 的细粒度四局归因为 `PARTIAL`。

**FACT → INFERENCE → HYPOTHESIS。** FACT：两高分及 v1 #2 均 M6/M12 晋升；v1 #2 M12 Output=10 后仍低分；v7g Q1 无汇报、M6 未晋；四局前六季 Energy 点数及 Main 选择如上；v1 raw 当前不可用。INFERENCE：早期晋升、规划 checkpoint、关键项目和高 Output 单独均不足以解释终局；v7g Q1 成果材料缺口是值得观察的差异，而非已证原因。HYPOTHESIS：带公开交付依据的 Q1 成果材料可能改善首个正式反馈；只可在 Main 新授权的有界实验中验证。建议下一步先由 Main 审核本报告的证据降级与 24 项重建映射，再决定是否授权这一**单机制** v7h 实验。
