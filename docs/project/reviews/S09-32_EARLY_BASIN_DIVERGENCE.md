# S09-32｜M1–M6 高低分盆地分叉取证

## 1. 身份、结论与边界

- Evidence base：`79184870986d1b61c95b51b678d58789f6909d52`；交付为 `codex/s09-14-v9a-static` 的 `IN_FLIGHT_EVIDENCE`。
- 当前 Candidate：`candidate-v11-result-conversion-risk-persistence`；本任务只读取 held evidence。live/provider/service/game/DB 操作均为 0。
- `EARLY_BASIN_ROOT_CAUSE=C (MIXED)`：公开机会分配差异与可控选择/交付链差异同时存在。**这是描述性分层；M6 晋升的唯一原因、各因素贡献及改选后的结果仍 UNKNOWN。**
- `EXOGENOUS_VARIANCE_MATERIAL=YES` **仅指机会/context 层**；资本结算或 promotion 的同输入随机差异 UNKNOWN。不能写“同输入经常得到不同晋升”。
- `RUN20_RUN08_BASIN_SIMILARITY=HIGH`；`EARLY_PROMOTION_COMPOUNDING=STRONG_DESCRIPTIVE`。
- `H_MIXED`；`S09_32_MIXED_EARLY_BASIN_RETURN_TO_STAGE`。Candidate/Skills/manifest/reviewer/Runner/retry/dependencies 均未修改。
- `CURRENT_STATE` durable delta 待 Stage 接受后写入；本任务没有将研究判断升级为 MERGED_FACT。main v8a freeze 保持不变。

## 2. 精确来源与窗口

[aligned evidence JSON](S09-32_EARLY_BASIN_EVIDENCE.json) 包含全部 60 个 primary 动作、75 个 secondary 动作、去重的完整公开 event/menu、每次前后状态、feed/next event、选择/notes、advertised updates、六维 delta、source seq/line，以及全部 pairwise matrix。用公开内容 fingerprint 对齐，不使用 private event ID。

| Run | 精确 events stem | 本次核验 bytes | SHA256 |
|---|---|---:|---|
| RUN07 | `20261001T114001Z` | 2054860 | `977f19aa89dbc12d4c1482ceff440ca98d28946737632e9c547b7d04dedb095d` |
| RUN08 | `20261001T132230Z` | 2078416 | `32cab0dbf9a5f10741ebff29db0fba5aa743e177b6211319d024fb05368229d0` |
| RUN20 | `20261003T075104Z` | 2099838 | `e9b92e5d1dac6da07a0e2ea0fea480bedb4008c2cfdf3e904f71a3e008635953` |

原始来源位于 `.career_sim_runner/career_emu/outputs/local-s06-adaptive-controller/<stem>/`；RUN07/RUN08 identity 复用 S09-16，RUN20 identity 复用 run20 evidence，本次 events bytes/hash 与锁定来源一致。exact session 和完整本地路径在 JSON identity；不搜索 latest、不查询 DB。transcript/score 既有 identity 与结论复用，未为报告重复重算全部历史 hashes。

每局 primary 恰好 20 动作：16 Story（含 handbook）+3 Energy+1 Main。第 20 个 M5 动作后的首次 fresh observe 已出现 M6 Review；**其状态就是 Review 状态**。M6 季度 Energy/Main 属于 secondary，不能倒算为导致 M6 晋升的资源投入。primary/secondary 每个动作均 SUCCESS 且有 fresh observe。

secondary：RUN07 26、RUN08 25、RUN20 24 动作。JSON 保存最后触发 Review 的动作前状态及首次 Review 后状态；不混用整月结束快照。later 仅提取正式 Review、Main/Energy 类别、公开收入/风险样本与终局，未重做六轴全局审计。

## 3. Same-context response matrix

`context` = 完整 event description/rules + legal menu；`strict input` 另含完整公开 status/time/feed。相同标题不足以对齐。重复 occurrence 按窗口内出现顺序一对一匹配，不做笛卡尔扩增。下表不同 response 定义为六维 delta、next public event、feed 或 Level 有变化；**其中机会变化与资本变化分列**。

| Pair | 同 context 同 choice | 同 context 异 choice | 未匹配左/右 | 相同 response | 不同 response | 相同/不同六维 delta | O delta 不同 | next opportunity 不同 | strict match / strict资本差异 |
|---|---:|---:|---|---:|---:|---|---:|---:|---|
| RUN07↔RUN08 | 5 | 3 | 12/12 | 1 | 4 | 2/3 | 1 | 4 | 1/0 |
| RUN07↔RUN20 | 7 | 1 | 12/12 | 1 | 6 | 3/4 | 1 | 5 | 1/0 |
| RUN08↔RUN20 | 7 | 2 | 11/11 | 0 | 7 | 3/4 | 3 | 6 | 1/0 |

共 19 个同 context 同 choice pair：2 个完整 response 相同，17 个不同；8 个六维 delta 相同，11 个不同。它们不是 19 个独立实验。promotion-relevant **资本差异候选**共 5 个 O delta pair（1/1/3），但因状态、时点或机会链不同，**已知 promotion 因果差异=0；UNKNOWN=19**。完整 pair 的 feed/next-event 差异见 JSON，不能把普通下一事件变化全称作晋升收益。

唯一 strict-input match 是初始 handbook continue（每个 pair 都复用这三次观察）：初始 state/menu/feed 一致、六维 delta 全零，随后分别出现年会排练／内核选型／酒后善后。故机会差异有直接证据；没有非平凡 strict-input 的成长动作对照。其对晋升的贡献不能量化。

关键响应对照：

| Action pair | 公开实得 | 混杂／可得结论 |
|---|---|---|
| 三局 a14，M3 申请关键项目 | 07：S+1；08：N+1/O+1；20：六维零 | 同 menu/choice，前状态不同；不能称作随机收益或隐藏 cap |
| 07 a13 / 08 a13 / 20 a13 汇报 Energy | O+1 / O+1 / O0 | 前 O=2/1/3，S=7/9/9；20 advertised O+1 没兑现；当次 observed response 可反馈，不能推永久封顶 |
| 07 a19 / 08 a3 / 20 a10 修健康端点 | S0/O+1 / S+2/O+1 / S+2/O+1，均 H−1 | 时点 M5/M1/M3、前 S9/3/7；技术问题修复有实得，非“同输入随机性” |
| 08 a18 / 20 a8 客户原型澄清 | 六维零 / S+2/O+1 | 时点 M5/M3，前资本不同；两局都获得后续客户认可，不等于同样资本结算 |
| 08 a4 / 20 a20 健身 | 均 O−1/H+2，D+1/0 | M1/M5、D 前值不同；末窗口保护有 O 成本，但工作明确“不紧急”，不能反推一定应加班 |

delta 是 action→observe 的公开差值；跨月工资、Review、晋升和延迟链可能共同作用。尤其最后 M5 动作的 O 差值不能作为隐藏 action effect。

## 4. 全部可控同-context异-choice分叉

| Pair / action | ownership/result / visibility | durable response | survival/risk / future opportunity | 判断 |
|---|---|---|---|---|
| 07 a8 vs 08 a2：开源快速交付 vs 自研长期资产 | 07 后续公开“如期上线、业务满意”；08 后续“进度严重落后、里程碑 miss” | 07 S−1/O+2；08 S+2/O−1 | 07 H1、M3；08 H5、M1。07 后续 CVE 候选漏洞；08 后续原创延期、拒绝抄袭 | 最强可控分叉；结果可见性不同，但不是同完整状态，也不能宣称开源普遍优越 |
| 07 a11 vs 08 a11：Health vs report | Energy 不构成已验证职业成果 | H+2 vs O+1 | 07 H1；08 H6 | 07 稳定化有现实低资源依据；不支持低分源于 Health 过保护 |
| 07 a12 vs 08 a12：Health vs Network | 不构成新增 result recognition | H+2 vs N+1 | 07 H3；08 H6 | 无健康策略优劣因果证明 |
| 07 a11 vs 20 a11：Health vs Network | 不构成新增 result recognition | H+2 vs N+1 | 07 H1/N3；20 H3/N2 | 不同 binding state；不能强制照抄两次 Health |
| 08 a11 vs 20 a11：report vs Network | report 是 advertised 材料准备，非外部认证 | O+1 vs N+1 | 08 H6/O0；20 H3/O3 | 响应维度和前状态不同；不是“20 放弃产出”的证据 |
| 08 a12 vs 20 a12：Network vs Health | 同上 | N+1 vs H+2 | 08 H6；20 H3 | 20 当次回复 Health 不等于长期防守死锁 |

主窗口未匹配动作左/右为 12/12、12/12、11/11（包括无法对齐的 Energy occurrence）；明确列为 DIFFERENT_CONTEXT，绝不按月份硬造同输入。RUN20 主窗口没有内核技术选型；该分叉不能单独解释它的失败。

其他可控但**非 matched counterfactual**候选：08 a20 用提问式 Code Review；20 a20 去健身，动作后两者 O3→O2。前者公开兼顾心理安全/mentoring，后者公开工作不紧急/H4，均不是已证错误；其余合法选项结果未知。07 a18/a19 得到 O+1/+1，属于额外晚窗口机会而非两局共同可选的漏选动作。

## 5. M6 boundary：状态、结果和风险

下表“前”是最后触发 Review 动作前；“后”是首次 Review observe。S/N/O/W 与 H/D 分开记录。所有前状态 duration_in_level=5、L1；未证明隐含 tenure 判定时点。

| Run | Review 前 S/N/O/W；H/D | 首次 M6 S/N/O/W；H/D | grade / Level | public result / risk |
|---|---|---|---|---|
| RUN07 | 9/3/3/2；3/10 | 9/3/3/2；3/10 | C，L1→L2 | 年会效率获感谢；平台如期上线且业务满意；M4 HR 小风险及 CVE；披露/备用选择后无明确清除回执 |
| RUN08 | 9/3/3/3；5/9 | 9/3/2/3；5/10 | C，L1→L1 | 自研链延期；高管成果汇报得到追问资源；无 primary HR elevated feed。未知风险存量不能当零 |
| RUN20 | 9/3/3/2；4/10 | 9/3/2/2；6/10 | C，L1→L1 | 客户同意原型确认、事实记录让 Leader/客户理解变更链；客户延期后的专业认可在首次 Review observe 同时出现 |

`CAPITAL_DIFFERENCE`：首次 Review O3 vs O2；**而触发动作前都是 S9/N3/O3**。`TENURE_EQUAL`：此前都 L1 tenure5。`RESULT_EVIDENCE_DIFFERENCE`：具体交付/协作链不同；`RISK_DIFFERENCE`：07 有公开警告却晋升，08/20 无 primary 同类 feed；不能用泛化“高分更安全”解释。

`OUTCOME_VARIANCE_WITH_NEAR_EQUAL_PUBLIC_STATE`：07 vs20 触发动作前 durable S/N/O/W 一致、D一致，H3 vs4；完整 Story/feed/链不同，不能升级为同完整输入的 promotion 随机性。

公开反馈：07 C 包含“进度、协作、风险意识”“别只会忙不会赢”并晋升；08 C 要求“更清晰成果”且无晋升；20 C “整体达标，亮点不突出”且无晋升。同 C 并不等于同晋升回执。**VISIBLE_PRE_REVIEW_REASON_SUFFICIENT=UNKNOWN**：可见候选差异存在，不能证实某一差异充分解释晋升；不推 `O>=3` 或其他公式。

## 6. Early Main/Energy 与 bounded result chains

| Run | pre-M6 Main | 3 Energy 顺序 / 实得 | 对常见假设的证据 |
|---|---|---|---|
| 07 | 关键项目，S+1 | Health+2、Health+2、report O+1 | 高分样本恢复更多，反驳“前期 Health 越少越好”固定配方 |
| 08 | 关键项目，N+1/O+1 | report O+1、Network+1、report O+1 | 三步均有 durable 实得；不是早期全零 farming |
| 20 | 关键项目，六维零 | Network+1、Health+2、report 六维零 | a13 notes 把 advertised O+1 称最优边际，实得为零；a14 同样无 durable 增益，但两次为不同路径，非已证重复同一 NO_GAIN |

primary 没有 Main report/mentor/rotation/avoid；没有 Energy intensity/cleanup/skill。报告材料在公开 menu 自带“可见成果”，但 Energy 本身不是结果认证。没有足够证据把所有 report 称虚构，也没有依据全局禁止它。

bounded chains（原始链内容全部可追到 JSON context 与 seq）：

1. **07**：a2 提效排练→a5 组织者感谢并委托接手统筹。a8 owner 选择开源→a15 描述平台如期上线、业务满意，同时 CVE 风险浮现→选择披露/备用。**成果确在 M6 之前，完成和业务认可有公开叙事；安全补救完成 UNKNOWN。** a18 竞标答辩获得 O+1，尚无 M6 前中标确认；不得冒称签约成果。
2. **08**：a2 自研 owner→a5 明确延期/miss→拒绝暗借代码，申请延期。a8 高管成果优先汇报→a15 高管追问最坏影响/所需资源→量化风险/资源。**公开可见成果讨论与组织可见性存在；自研交付完成/正式认可 UNKNOWN。** a18 客户原型方案的接受叙事首次出现在 a20 后的 M6 observe，不能算更早已确认。
3. **20**：a8 客户原型/书面澄清→a15 客户同意、返工范围谈拢→固化变更流程；a17 出示时间/邮件记录→a18 叙事客户和 Leader 已理解变更链、要求联合改进计划。**M6 前有真实客户/组织反馈，不能归为“全是 generic defensive”。** a19 提前坦诚延期→a20 后、与 Review 同一 observe 才出现客户专业认可/核心先交请求；核心交付当时尚未验证。

Delivery notes：07 D1→DELIVERED 但 UNVERIFIED；08 D1 长期 IN_PROGRESS/UNKNOWN；20 a1–a20 均 DL NONE。账本覆盖存在区别，但职业成果须上面的公开叙事验证。20 缺 tracking 不是“没有成果”的证明；07 自报 delivered 不是认可来源。

## 7. Secondary 与后续复利

M6 Review 后：07 的 M6 report O0、Main S+1/N+1；08 report O0、intensity O0且 H−1/D−1；20 intensity O0且 H−1/D−1、Network N0/D+1、Main 六维零。**这是未增益响应和成本的直接证据，但不是永久上限。**

M9：07 两次 report 各 O+1、Main成果汇报 O+1；08 Main关键项目六维零；20 Main关键项目 O+1。07 另有 CI 上线/回归效率提升的公开叙事（a30→后续观察），因此存在 fresh result 后的兑现空间。三局 M6→M12 动作数不同，机会也不同，不能只按数量判优。

| 正式 Review | RUN07 grade/Level S/N/O/W | RUN08 grade/Level S/N/O/W | RUN20 grade/Level S/N/O/W |
|---|---|---|---|
| M6 | C/L2 9/3/3/2 | C/L1 9/3/2/3 | C/L1 9/3/2/2 |
| M12 | B/L3 21/4/6/3 | C/L2 9/3/3/3 | C/L2 9/3/3/3 |
| M18 | B/L3 41/11/15/5 | B/L3 21/4/6/5 | B/L3 20/4/6/6 |
| M24 | B/L4 42/19/15/9 | B/L3 41/21/8/8 | B/L3 39/17/6/10 |
| M30 | B/L4 59/26/26/14 | B/L3 42/21/13/12 | B/L3 42/20/13/13 |
| M36 | B/L4 81/36/25/19 | B/L4 42/19/15/15 | B/L4 42/19/16/13 |
| M42 | A/L5 100/34/24/24 | A/L4 59/33/26/23 | A/L4 59/36/26/21 |
| M48 | B/L5 117/53/32/34 | A/L4 77/36/26/27 | B/L4 76/36/22/28 |

`STRONG_DESCRIPTIVE`：07 先在 M6 得 L2、M12 得 L3；08/20 M12 才 L2、M18 才 L3。M12 的 S21/O6 vs S9/O3，M18 的 07 S41/O15 vs低分 S21或20/O6，表现出早窗口优势积累。到 M24 07 已 L4；到 M42 已 L5。

**工资方向有直接 public feed**：M7–M12 07 L2 每月+0.4，08/20 L1 每月+0.3；M13–M18 07 L3 +0.5，08/20 L2 +0.4。但 wealth 并不一直领先：M12 三局 W3，M18 W5/5/6，M24 W9/8/10。因此不能把后期 W35 vs29 全归因早晋升。Level-dependent opportunities 的延迟与资本响应更弱是 plausible INFERENCE，未识别其公式/因果贡献。

## 8. RUN20 vs RUN08：HIGH，但不同过程

- 相同 promotions M12/M18/M36、终局 L4/S82/N36/O26/W29。M6 两者 S9/N3/O2；M12 两者 S9/N3/O3；M30 两者 S42/O13；M42 两者 S59/O26。该对照支持重复低分轨迹形态，不能证明相同 seed 或隐藏机制。
- 所有 Review S/N/O/W 均已列上表；M18、M24、M36、M48 的差别不能抹去。尤其 M48正式 Review 08 A/O26、20 B/O22；正常 post-M48 动作后最终 O26 相同。score-report 总评为 C/B，与最后半年 Review A/B 分开。
- Main：08 全16次关键项目；20 13次关键项目、M27/M45/M48 三次低调避险。前8个季度 Main 相同但 Story 与 realized response 不同。

| 全局 Energy action occurrences（不是消耗点数） | RUN08 | RUN20 |
|---|---:|---:|
| 准备汇报材料 | 21 | 14 |
| 人脉维护 | 8 | 6 |
| 健康恢复 | 11 | 16 |
| 高强度工作 | 1 | 2 |
| 处理历史埋雷 | 2 | 4 |
| 技能学习 | 1 | 0 |

- 08 报告材料21 vs20的14；20 Health16 vs08的11、cleanup4 vs2。相同终局耐久状态并非同样资源分配。
- recognition episodes：08 高管里程碑问答、客户原型确认；20 原型确认、变更记录组织理解、客户延期透明沟通。都有公开结果反馈，缺少严格同输入、同链闭环对照。
- 风险公开样本（按 month+原句去重，不等于真实 episode/hidden stock）：08 12 个 warning-month/text 样本、20 9 个；都从 M7 开始，primary均无同类 HR feed。20 M27/M45/M48 elevated，08 M30 elevated且 M47 minor。完整月/句/seq在 JSON。不能用计数断言20风险更小，也不能把 later risk 当 M6 根因。
- 终局 H8 vsH10、score59 vs60.6，说明生存状态/风险/评语仍有差别。HIGH 仅是轨迹形态相似。

## 9. 下一任务：一个待授权的窄合同

**H_MIXED；建议 Stage 将 S09-33 定义为 `EARLY_PUBLIC_RESULT_FEASIBILITY` 单 Delta 静态实验。尚未授权、未实施 v11b，也没有新局。**

1. 范围仅 Planning 对首次 Review 前、公开给定 ownership/交付路线的比较依据。针对同一菜单有“短期可交成果”与“长周期技术资产”时，将公开 deadline、现有承诺、当前资源与可见完成条件纳入现有决策，不让长期资产标签自动胜出。三维成长与生存边界仍保留。
2. 这是选择可兑现结果的**条件比较**：不能锁定开源、活动/客户类型、action ID、固定 Energy 配方或数值晋升阈值。公开安全/合规风险可否处理必须一起比较；RUN07 CVE 的代价必须在反例中保留。
3. 显式 variance robustness：机会没出现就不伪造；完成/认可只接纳 fresh public evidence。若一次 advertised成长未兑现，只修正该上下文的实得判断，重评现有合法结果/成长路线；不用隐藏 cap、不追补固定 O、不增加 retry或无证据风险清理。结果尚未确认则 UNKNOWN，既有主线继续。
4. 不新增控制器/Skill/字段治理，不强制改20的健身或08的心理安全选择；不得顺带修全局 Delivery/risk。Board/Delivery/Risk、runtime/reviewer、candidate lineage、冻结 v8a、retry/dependencies 不纳入该 Delta。若实施需要超出上述范围，返 Stage。
5. 静态 acceptance：公开 deadline 的两路线 tradeoff有明确依据；反例包括健康脆弱/开源安全warning、自研可在窗口内完成、仅有advertised gain却观测零、菜单无对应机会；选择随公开条件变化，不声称稳定高分或保证 M6晋升。live验证须另行授权。

这是机制假设而非已证修复。现有证据不足以宣称“只要某个动作就恢复高分”，也不足以证明全局重构必要。若 Stage 不接受该窄比较假设，维持 Candidate不变；不要继续无证据 patch。

## 10. 验证、保全与交付

- 全部 primary/secondary 源 seq、menu choice、前后 delta、fresh observe、M6/M12边界、matrix分类/计数及 fingerprint 离线一致性核验 PASS；没有重跑历史测试。
- exact events身份本次 PASS；JSON parse、限定文件 secret scan 与 `git diff --check` PASS。扫描仅两份交付，未复制 provider日志/.env/private配置/DB。
- 原始 raw、既有 runtime folders 及 FORENSIC_HOLD 全部保留，无清理/覆盖；本任务派生和重建脚本留 `.local/runtime/s09-32-early-basin/`，不提交一次性 verifier。
- 受限证据仍有诊断价值；closure须 Stage/Main 明确接受，报告/hash完成不解除hold。
- `NEXT_GAME=NOT_AUTHORIZED`；`MAIN_V8A_FREEZE_UNCHANGED`。
