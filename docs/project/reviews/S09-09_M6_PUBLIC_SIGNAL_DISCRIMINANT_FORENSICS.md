# S09-09｜M6 晋升公开信号判别取证

## 结论与范围

**Decision：`S09_09_INSUFFICIENT_PUBLIC_SIGNAL_RETURN_TO_STAGE`（Option E）。** 当前 cohort 有弱行为关联和可确认的正确性缺陷，但未找到通过反例检查、可稳定区分 M6 晋升/未晋升的通用组合机制。不能据此选择一个高置信 Early Promotion Engine，也不能据此推断晋升本身随机或公开行为无价值。

- 基线 `main@27d6d208266d7605c62305e5b73346e9f9d2b9bd`；Candidate v7z 完全冻结。游戏/Provider/service/MCP/DB/replay/安装=0；没有 Candidate、Skill、manifest、Runner、依赖或 retry 修改。
- Tier A **15 条 exact streams：晋升7 / 未晋升8**，首 Review 前共300次 action attempts。额外 Tier B **2 条晋升 summary**，不并入细粒度分母。另7个 registry entries 排除，见下文；不是7条确认失败游戏。
- 仅用公开 status/time、当前 description/legal choice 文义、公开反馈，以及有界 Agent action notes/文本决策证据。内部 effects、event ID、HiddenRisk、私有配置/日志/DB 均不进入分析；不使用后期 survival/final score 构造标签或特征。
- **按 seq 截断首次 M6 formal Review。** 特征的 action call 与 observe 必须在 Review 之前；最后动作的 post-observe 如果跨到 Review，delta 标 `UNAVAILABLE_BEFORE_REVIEW`。Review 的 grade、Level/promotion 只作标签。M6当月 Review 后的 Energy/Main 不计入首窗。
- 复用现有 `scripts/s09_02_failure_floor_joint_forensics.py` 的 session/receipt/归因 parser，没有运行全历史入口、历史 tests 或重新计算旧 hashes。公用 parser 的终局推断未被用于本窗标签；M6标签直接读取 formal feedback与Level变化。跨月、batch、unknown receipt 不升级为 clean gain。

## 1. Cohort / 公开特征表

所有 Tier A 的 M3 Main 均实际可选且已选择；没有 avoidance Main，也没有首窗 Skill Energy。P=准备汇报材料、N=人脉维护、H=健康恢复、R=处理历史埋雷（该选择耗2 Energy）、?=不明请求。G/NG/U 是 Energy所声明**主要维度（含Health）**的 clean GAIN/NO_GAIN/mixed-or-unknown **action次数**，不代表晋升价值。v7d的不明请求不能当成功分配。各局到Main时E=0，未见未用体力/跳过Main；v7g两次Energy选择也耗完3点。

“pre state”是 **Review前最后一次fresh observe** 的 H/D/S/N/O/W；均为L1、tenure5、E0。它不是结算前不可见瞬间的完整状态。没有更早 formal Review，公共 Primary Gap=UNKNOWN；Agent自定 G 不充当公开反馈。

| Run (Tier A) | M6 promotion / grade / Level | M3 Main | Energy selections; G/NG/U | 首窗 S actions | pre state H/D/S/N/O/W | pre observe→Review seq |
|---|---|---|---|---|---|---|
| v4 | YES / C / L1→L2 | 申请关键项目 | H1 N1 P1; 2/1/0 | 0 known / 20 UNKNOWN | 3/10/9/3/3/2 | 179→187 |
| v6 | YES / C / L1→L2 | 申请关键项目 | P2 H1; 2/1/0 | 0 known / 20 UNKNOWN | 5/10/9/3/3/2 | 183→191 |
| v7d | NO / C / L1→L1 | 申请关键项目 | N1 P1 ?1 H1; 0/2/2 | 0 known / 1 UNKNOWN | 7/10/9/3/3/1 | 191→199 |
| v7g | NO / C / L1→L1 | 申请关键项目 | R1 H1; 1/0/1 | 4 | 4/10/9/3/3/2 | 171→179 |
| v7i | YES / C / L1→L2 | 申请关键项目 | H1 N1 P1; 2/1/0 | 2 | 4/10/9/3/3/2 | 179→187 |
| v7m | NO / C / L1→L1 | 申请关键项目 | N2 P1; 1/2/0 | 0 | 8/10/9/3/3/3 | 179→187 |
| v7n | YES / C / L1→L2 | 申请关键项目 | H1 N1 P1; 3/0/0 | 2 | 5/10/8/3/3/2 | 241→253 |
| v7o | YES / C / L1→L2 | 申请关键项目 | H1 N1 P1; 3/0/0 | 0 | 5/9/9/3/3/3 | 179→187 |
| v7q | NO / C / L1→L1 | 申请关键项目 | H1 N1 P1; 2/1/0 | 2 | 4/10/9/3/0/2 | 179→187 |
| v7t | YES / C / L1→L2 | 申请关键项目 | H1 N1 P1; 2/1/0 | 0 | 4/10/9/3/3/3 | 179→187 |
| v7v | YES / C / L1→L2 | 申请关键项目 | H2 N1; 2/1/0 | 0 | 5/10/9/2/3/0 | 179→187 |
| v7w | NO / C / L1→L1 | 建立导师关系 | H1 N1 P1; 2/1/0 | 0 | 4/10/9/3/3/3 | 179→187 |
| v7x | NO / C / L1→L1 | 申请关键项目 | H2 P1; 2/1/0 | 2 | 5/10/9/3/0/3 | 179→187 |
| v7y | NO / C / L1→L1 | 申请岗位轮岗 | N1 P1 H1; 1/2/0 | 0 | 4/10/9/3/3/2 | 179→187 |
| v7z | NO / C / L1→L1 | 申请关键项目 | P2 N1; 2/1/0 | 0 | 4/10/9/3/1/2 | 179→187 |

Tier B：v1#1、v1#2 的历史 Git summary均明确 M6 L1→L2；M3均为申请关键项目，Energy均N/P/H各1；M6 grade：#1 UNKNOWN，#2为C（Tier B文本重建，无法exact raw核验）。两个旧 events/transcript指定路径本次确认都不存在；不把月末状态、M6季度选择、反向重建或 summary补成pre-Review action/observe。

额外发现：v7m虽然技术终止于后期，但M6 public label明确NO，应纳入；v7n replacement虽max_continuations止于M6，但已明确L1→L2，应纳入。v7n旧报告写C+，本次exact public奖金字段为C，采用raw C，不用旧注解替代原输出。

排除7个索引条目：S07-33 v7g原尝试、S07-38 v7i原尝试、S07-51 v7n原尝试、S09-RUN03 v7y原尝试均没有fresh game；S01-03 baseline、SCORE-01 reference、身份UNKNOWN的S06 Run#1当前compact记录不足以确认M6 formal label及准备窗，`EXCLUDED_OR_SUMMARY_ONLY`。不继续搜索无关旧worktree/DB以补齐。v7i采用S07-40 replacement流，旧stale score排除。

## 2. Discriminants / 反例

以下分母均Tier A YES7 / NO8；关联为同项目、不同Candidate/事件路径的描述，不是受控因果比较。没有训练分类器、拟合阈值或验证集。

| pattern | promoted_support | not_promoted_support | counterexamples / source tier | confidence / causal_status / runtime_deployability |
|---|---|---|---|---|
| M3 broad ownership Main（本cohort具体为申请关键项目） | 7/7 | 6/8（d/g/m/q/x/z） | v7z是直接反例；v7m也具备Main+N/O+无S | A；事实高/机制低；行为关联；可作通用机会比较，不能固定该动作或称充分/普遍必要 |
| key-project Main + 至少一次Health恢复 | 7/7 | 4/8（d/g/q/x） | v7x也有2次恢复而不晋升；没有对照实验分离Main、Health与事件路径 | A；组合关联仍不具充分性；不能设Health或Energy quota |
| growth Energy覆盖N与O两类 | 5/7 | 6/8（d/m/q/w/y/z） | v6仅O成长、v7v仅N成长仍晋升；v7m虽N/O且有公开认可仍失败 | A；不支持固定均衡quota或BROAD机制单独修复 |
| growth NO_GAIN后保留不同Main价值/不重复测试路径 | i/t/z等可确认；i/t晋升 | z同样遵守仍NO；m重复N测试，y按局部数字收缩Main | A；正确性支持，promotion收益未证明；不能把遵守该规则当晋升信号 |
| 无S或强保护少→晋升 | o/t/v均20个A；v4/v6模式未知 | m/w/y/z均20个A仍NO；d有20A+1未知；g为4S，q/x各2S | i/n各2S仍晋升；零S不是充分条件，有S不是失败判据 | A；个别保护挤出可诊断；不能自动压低保护预算或判Health低为原因 |
| completed/public recognition/ownership→晋升 | i有公开入选/更正口径，n接受统筹，o有评语被采纳 | g/q明确CI上线；d/m/x有领导公开认可；w有客户同意确认机制及Demo闭环 | “做完CI+key project”g/q仍NO；n/q同样接受统筹却标签不同；无需完成一个特定交付才可解释所有YES | A；可实现结果有价值的HYPOTHESIS，未形成稳定discriminant；不支持First Review Bootstrap |
| 成本条件被正确读取→晋升 | v6客户scope、n当前项目、v客户/本职兼顾样本正确 | m客户接待、w客户接待、y合同实际范围等样本也正确；z出现明确反转 | x看见同一邀请3–4天成本但仍NO，不能把accept本身当misread | A；仅有界样本，未测完整错误率；通用correctness可部署，作为M6机制LOW_CONFIDENCE |

**强反证是snapshot重叠。** v7i(YES)与v7g/v7y(NO)的最后pre-Review完整公开status完全相同：H4/D10/S9/N3/O3/W2/L1/tenure5/E0；v7t(YES)与v7w(NO)也完全相同（W3，其余同上）。这些只是matched snapshots，不是matched整条轨迹或同一随机路径；足以否定从该snapshot直接推出标签，不能否定所有动态公开信号。

15条A流的M6 grade全部为C，7条仍晋升。奖金/Review反馈在决策结算之后产生，不得把它们回填为预Review predictor。泛泛“观察名单/成果不足”的M6话术也出现在晋升局，不反推出隐藏eligibility。

## 3. Story cost、realization 与 planning：有界案例

| 公开链 / seq | semantic classification | 证据与边界 |
|---|---|---|
| z M5 A19 seq173；transcript750/765/771 | **SEMANTIC_MISREAD** | 3–4天文档阅读成本属于accept；“本组排期不受影响”属于decline。notes却将不影响排期归给accept，且后续Risk沿用。紧邻pre-Review pair O3→1/H5→4；A20的post-observe已是Review，O1→0不能作为先行feature。 |
| x M4 A17 seq157；transcript508/511；A18 seq165 | **AMBIGUOUS**（非已证反转） | 相同邀请的accept被选择；文本明确看见3–4天成本，但把visibility列为主收益。首pair跨月O3→1为mixed；次pair同月O1→0可归因。取舍过重/反事实净价值UNKNOWN，不能因为损失而判读错。 |
| g M4 A15 seq141；q M3 A9 seq93 | **AMBIGUOUS** | CI部署明确延期两个已有项目；g直接承认延期并接受，q称普通排期成本。随后公开CI顺利上线，两局仍NO。不是无结果，也不是字面成本反转；是否值得接受机会成本UNKNOWN。 |
| v6 A18 seq169；n A6/A18/A19；v A18 seq165 | **SEMANTIC_READ_CORRECT（样本）** | 客户新增需求先评估scope；跨部门夜班与本周方案分开比较；现有排期/Leader指示被保留；协调排练保护本职。YES提供正确读取示例，不证明特定选择必晋升。 |
| m A17；w A9；y A3/A9 | **SEMANTIC_READ_CORRECT（样本）** | 客户接待的合法成本/会面价值、实际交付范围、匿名条件等被消费；这些NO局并非所有Story都忽略语义。 |

**v7z M5 anomaly：确证的条件反转目前是isolated case；类似机会成本压力并非孤例。** x/z邀请与g/q CI四条链集中在NO组，但其同类公开情境在YES组未出现，缺少暴露匹配的成功/decline对照。不能把4个不同取舍都编码为misread，不能据此声称cohort-level语义错误率显著或修复必晋升。其余run的有界分类及seq在小型JSON中；AMBIGUOUS/未覆盖不填成“无错误”。

规划分支：m A11 N3→3，A13重复N3→3（中间为O gain）是同family clean NO_GAIN后重复；这不是连续相邻同family重发。y A14将Main收缩为假定responsive Skill，仍存在broad机会。z已恢复不同family的Main比较且没有S，却仍NO，故这条belief修复不是充分解释。deliberation在z首窗公开文本明显存在、n旧报告也记录长Energy讨论，但没有可靠的全cohort统一计数或因果证据，标UNKNOWN而不制造verbosity predictor。

Risk/Recovery：g的首季Energy是2点risk cleanup+1点Health（没有成长Energy），公开Leader泄露排查/HR warning存在；可记录保护占满该次窗口，但净必要性与晋升原因UNKNOWN。i的2个S中甚至包含Network成长；n的2个S处理夜班/身体节奏后回A，最终晋升。m/w/y/z没有S，仍失败；v/z正常A下分别出现关系cleanup/公开warning修复。不能将v7q后期长S、y M9恢复或任何M6后规则偏移倒算为首轮原因。

## 4. M6_PUBLIC_FAILURE_TREE

这是**失败后的公开诊断树，不是能预测标签的运行时决策树**；分支可重叠，无阈值、quota或event lookup。

```text
M6_NOT_PROMOTED
├─ 成本条件明确反转？ → z：MISREAD已证；净promotion效应UNKNOWN
├─ 可见成长机会被收缩/预算被保护占满？
│  ├─ y：局部数字收缩Main；m：NO_GAIN family再投
│  └─ g：risk/Health占满首季Energy；必要性/净收益UNKNOWN
├─ 有ownership/完成结果，仍承担明确交付成本？ → g/q/x/z
│  └─ 分别区分accepted tradeoff、AMBIGUOUS、literal misread；不能一律判错
└─ 上述没有稳定区分（d/w等，且YES也有保护、成本、延迟）
   → INSUFFICIENT_PUBLIC_SIGNAL / UNKNOWN；环境与轨迹方差是待验证解释
```

删除不受支持分支：“没有申请关键项目”“没有completed result”“C grade”“S/N/O未达线”“有S所以失败”。没有任何单枝覆盖所有8条NO且排除所有7条YES；更多组合可被事后拟合，但没有独立验证不能升级为设计依据。

## 5. Top hypotheses / next Candidate recommendation

1. **条件成本归属核对**（HYPOTHESIS；correctness置信高，promotion benefit低）：通用地区分当前义务、所选项投入、各备选条件，避免把未选项的好处合并到所选项。保持accept/decline均可比较，不自动禁cross-group或重责任，不记标题答案。本次只提出可部署的最小correctness方向，未修改Candidate；不能把它包装为已找到Early Promotion Engine。
2. **保护可实现的主线结果与新增责任的净价值比较**（HYPOTHESIS；低置信）：结合实际排期与结果证据比较新增ownership，而非认为可见材料/曝光必有净收益；保持正常必要保护和UNKNOWN路径。CI成功却不晋升、y真实署名/成果保护仍不晋升、n已延期仍晋升，是必须保留的反例。没有支持固定bootstrap、时间窗口quota或必选项目。

**推荐下一机制：暂不根据本cohort批准A/B/C/D中的新晋升策略包。** 返回Stage按Option E选择有界、受控的独立复验，或策略简化/donor-core transplant实验；身份和单一变化需单独冻结并授权。条件归属correctness可单独评审，不能继续用Prompt微调猜公式。现有数据未证明随机性，也未证明donor-core移植有效。

置信层级：公开标签/上述反例=FACT高；特征共现=behavioral association；跨run观察仍非validated classifier；H1/H2=causal hypotheses待检；新Candidate live M6 success与independent replication均NOT_EXERCISED。`HIGH_CONFIDENCE_M6_PROMOTION` / 稳定高分均NOT_PROVEN。

## 6. Compact evidence / delivery boundary

- [小型cohort派生表](S09-09_m6_public_cohort.json)保存17条分Tier来源、首Review seq、pre status、Main/Energy、clean response、模式与有界semantic样本；不含原日志、会话凭据、hidden/private字段或后期分数。
- A源精确路径在JSON；v4/v6/d/g/i源身份复用S09-02登记，m/n来自正式partial run记录，o/q/t/v/w来自已扫描archive，x/y/z来自各自正式receipt/record。B源为`8a93378a8d9ef5598e925048db39ee931e207bab:experiments/S04-04-high-score-confirmation/candidate_run{1,2}_trajectory.json`。不搜索latest，不重新hash旧输入。
- 本地公开派生窗口：`D:/CS/CareerSim/.local/runtime/s09-09/public-pre-m6-windows.json`；source-bindings与compact-cohort在同目录。原始流继续保留在既有FORENSIC_HOLD，不释放或清理。S09 Stage接受本报告并确认后续分析依赖解除后，仍需显式cleanup授权。派生物不是源文件的替代。
- 只交付本报告/小型JSON与CURRENT_STATE一条delta；RUN_HISTORY、Candidate资产不变。JSON边界/session/统计核对、选中文件secret scan、`git diff --check`；未运行tests或live。未来额外game=未授权。

`NEXT_GAME=NOT_AUTHORIZED`
