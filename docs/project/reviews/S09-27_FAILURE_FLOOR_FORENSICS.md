# S09-27｜Failure Floor 生存底线与低资源决策取证

## 结论与边界

`IN_FLIGHT_EVIDENCE`；基线 `f1ae76262ccc74d5592efe4762b530c3868d3906`，授权隔离分支 `codex/s09-14-v9a-static`。本次仅离线读取、派生统计与文档交付，未创建 v10h。Candidate、四 Skills、manifest、retry、Runner、main v8a freeze 均未改；live/provider/service/game/MCP/DB 操作均为0。

- `FAILURE_FLOOR_ROOT_CAUSE=MIXED_DESIGN_AND_EXECUTION_WITH_UNADVERTISED_SHOCK`
- `NEXT_SURVIVAL_GUARD=G3`
- `SURVIVAL_GUARD_LOCATION=PLANNING_A`
- `SURVIVAL_GUARD_SCORE_COST=UNKNOWN`
- `S09_27_FAILURE_FLOOR_GUARD_JUSTIFIED_RETURN_TO_STAGE`

**FACT：** RUN17 的高工作量带教 H3→1、下一 Story H1→0；数值代价未提前显示。**INFERENCE：** 在 a22 使用已公开的工作量语义与低资源余量比较，有合理机会避开危险链；不能证明换一个选项必然存活。**RECOMMENDATION：** 最小下一实现只加强 Planning 内 A 模式的生存余量比较，不把普通低 H 自动变成 S，不补满 Health，不新增状态机。

主问题不是“低 H 永远不能恢复”：当前 K3 明确允许 A 内普通价值恢复，a11 已这样执行。缺口是 C10 的不可逆下行原则没有成为低余量候选排序的可执行比较；K3 禁止数字直接授权 S，不能被扩读为禁止生存缓冲。

## 1. 来源、方法与覆盖

机器可读表：[S09-27_HEALTH_TRAJECTORY.json](S09-27_HEALTH_TRAJECTORY.json)。包含所要求的字段、精确 source before/action/after 行号、会话/路径、覆盖清单、冲击分布和暴露计数。不是原始日志归档，不解除既有 FORENSIC_HOLD。

盘点范围：当前 canonical Runner 输出、已选开发 archive，以及 `.local` 中已存在的相关事件流；按 session 去重。匹配 tool-call ID，使用提交前最近的同局官方 observe 及随后 fresh observe。多个 take_action 后才 observe 的窗口排除出单步归因，不把累计变化归给最后一个动作；失败/缺失窗口不猜 delta。未通过唯一 session / Health 轨迹条件的一个原始输出排除。

27个独立公共轨迹会话，共2654个隔离 action→fresh 配对；派生829个低资源/恢复/大下降/终局比较行，其中753行提交前 H≤5。另审阅4份老历史结果/快照，保留24个低 H 快照但**不混入单步冲击统计**。这些是被选择策略产生的相关观察，不是随机独立样本，不估计隐藏概率。

| Run | 可隔离配对数 | 最低观察 H | 成绩 | 覆盖质量/限制 |
|---|---:|---:|---:|---|
| S01 baseline | 无 | UNKNOWN | 26.95 | LOW，结果可用，记录的旧 raw 路径不存在；19m淘汰原因 UNKNOWN |
| SCORE01 | action-before快照 | 3 | 33.06 | MEDIUM，98个动作前状态，无fresh after；raw不存在，M24job/绩效终局文本保留 |
| v1 #1 | 快照 | 3 | 76.04 | MEDIUM，49个月/16季度快照；raw不存在，3是采样最小值，不保证真最低值 |
| v1 #2 | 快照 | 4 | 35.31 | MEDIUM，7里程碑/8季度；raw不存在，M25信任危机，终局H10 |
| v4 | 23 | 0 | 25.84 | HIGH配对，M6 Health终局 |
| v6 | 201 | 3 | 75.29 | HIGH配对；非法/批次尝试附近排除，完整48m结果另有确证 |
| v7d | 58 | 3 | 17.02 | HIGH配对；部分批次排除，M15财富连续不足终局 |
| v7g | 195 | 3 | 54.52 | HIGH配对，48m |
| v7i | 198 | 2 | 64.00 | HIGH配对，批次窗口排除，48m |
| v7m | 84 | 4 | UNKNOWN | HIGH局部配对，未完整终局 |
| v7n | 22 | 2 | UNKNOWN | HIGH局部配对，技术/continuation截断 |
| v7o | 205 | 3 | 71.83 | HIGH配对，48m |
| v7q | 97 | 2 | 26.80 | HIGH配对，M24绩效/job淘汰，终局H8 |
| v7t | 180 | 2 | 65.71 | HIGH隔离配对；9个批次窗口排除，不误归因其Energy累计变化，48m |
| v7v | 204 | 2 | 58.97 | HIGH配对，48m |
| v7w | 112 | 2 | 30.31 | HIGH配对，M24绩效/job淘汰，终局H8 |
| v7x | 29 | 0 | 19.82 | HIGH配对，M8 Health2→0终局 |
| v7y / RUN03R | 60 | 2 | UNKNOWN | HIGH局部配对，用户截断；不算生存失败 |
| RUN04-v7z | 20 | 4 | UNKNOWN | HIGH局部配对，开发门控截断 |
| RUN05-v7z | 20 | 2 | UNKNOWN | HIGH局部配对，开发门控截断 |
| RUN06-v8a | 20 | 2 | UNKNOWN | HIGH局部配对，开发门控截断 |
| RUN07-v8a | 203 | 1 | 72.65 | HIGH配对，48m |
| RUN08-v8a | 205 | 3 | 59.00 | HIGH配对，48m |
| RUN10-v9a | 201 | 1 | 68.40 | HIGH配对，48m |
| RUN11-v10b | 183 | 3 | UNKNOWN | HIGH局部配对，技术截断，非自然终局 |
| RUN12-v10c | 3 | 4 | UNKNOWN | HIGH局部配对，合同早停 |
| RUN13-v10d | 39 | 2 | UNKNOWN | HIGH局部配对，合同早停 |
| RUN14-v10e | 18 | 2 | UNKNOWN | HIGH局部配对，合同早停 |
| RUN15-v10f | 26 | 5 | UNKNOWN | HIGH局部配对，Reviewer误判截断 |
| RUN16-v10f | 25 | 3 | UNKNOWN | HIGH局部配对，历史K1截断，后续信息来源纠偏；不重写历史 |
| RUN17-v10g | 23 | 0 | 24.47 | HIGH配对，M6自然Health终局先于Reviewer停止请求 |

HIGH表示可追溯公共前后状态，不证明 choice 唯一因果作用、策略正确或 Candidate 完整通过。mode 缺失=UNKNOWN；没有完成语义核对的 explicit threat / recovery opportunity=UNKNOWN，不能把未命中关键词记为 NO。恢复选择只计明确健康恢复/医疗休假类，不把所有正 ΔH Story 自动算主动恢复。

历史 v1 来源：`git show c4dbe0ebc4e27aafc22c94050c69547113cdc8eb:experiments/S04-04-high-score-confirmation/candidate_run{1,2}_trajectory.json`；S01来源同 commit 的 `experiments/S01-03-baseline/RESULT.md`；SCORE01来源 `experiments/S04-03-score-directed-integrated-run/score01_trajectory.json`。只读取明确记录的旧路径判断存在性，未修改或迁移旧 checkout。缺失源限制独立重析，不用摘要制造完整轨迹。

## 2. 官方生存边界

`OFFICIAL_HEALTH_TERMINAL_RULE=LOCKED_PACKAGE_HEALTH_LE_ZERO_TERMINAL`

离线加载已锁定1.0.1安装包 `career_emulator/data/dataset/failure_conditions/health_zero.data`，仅核对该 Health 规则：`health <= 0` 触发身体/血条归零终局，`hp=1`；与已锁定 `career_emulator_bdci26/dev/dataset/failure_conditions/health_zero.data` 字节一致。SHA256 `6e79da840d26eb11311176dbc0cc7d9ca66e4d41ee22bdf083657e6c356abfb3`。这是锁定源码/包事实，不宣称新读取文件是当前 Agent 的输入。

RUN17 已自然取得的同局 Handbook 明示 Health 范围0–10、长期透支有害和身体倒下可强制结束；其公开正文未给出精确 numeric terminal threshold，也未给出安全缓冲值。正式 Agent 信息准入仍须服从 K1，不将其它 hidden rule、counter或Test公式移植进策略。三个公共自然终局 H0 与源码边界相符。

`OFFICIAL_SAFE_BUFFER_RULE=UNKNOWN`

没有“Health≥2/3/5必安全”的官方证据，没有精确普通冲击概率；手册未明确建议某个 buffer。此次只检查 Health-zero 条目及公开 Handbook，**不声称排除了所有其它带 Health 条件的隐藏规则**。未来 guard 的冲击余量只能标经验 prior，而非官方安全阈值。

季度 choice 输入确实展示 `status_updates.Health`，例如恢复+2、高强度/学习−1；Story 菜单经常只有 action/text，数值后果可能不展示。看似保守的 Story 也可产生负 Health：RUN17 a23选择保持手动Review仍H1→0。因此“未广告 Health 代价”和“较少投入工作”都不证明零成本。

## 3. 实测 Health 冲击

| 隔离单步 ΔH | 次数 |
|---|---:|
| −1 | 329 |
| −2 | 54 |
| −3 | 1 |
| ≤−4 | 0（未观察到，不代表不可能） |
| 合计下降 | 384 |

最小观察−3，来自 v7d a47 高密度带教 H6→3。分层：40次 Energy 下降全部广告−1、实际−1；Story下降344次（−1:289、−2:54、−3:1），选项未显示数值 Health 代价。单步含自然切月/Review等同次结算，不能自动把全 delta 当作纯选项函数。

低 H 恢复的明确选择70次。存在低 H 后存活和低 H 后终局，不能由“某次 H1 存活”推出 H1安全，也不能由“三次 Health失败”把其它早退归为Health。Health终局观测链：v4 H1→0、v7x H2→0、RUN17 H1→0；这三次致命选择均无公开 advertised Health delta。G1仅广告致命成本拦截在这些终局上没有触发依据。

普通−1/−2是经验上反复出现的量级，−3是尾部已见量级。可用来讨论余量，但没有证据支持固定概率、最大损失保证或期望得分损失。

## 4. 高分 donor 与恢复行为

| Donor | 最低 H / 恢复次数 | 低点后行为与边界 |
|---|---|---|
| v1 #1 76.04 | 采样H3；11个健康恢复选择 | M6季度H3选择两个恢复，后续仍关键项目；无raw，无法算真实单步最低H或严格next action |
| v6 75.29 | H3；10总恢复，9可隔离配对 | a33–35在H3处理Story均未再耗H，a36恢复3→5；未观察H≤3时Health负向动作；一个恢复因失败/批次窗口未单步归因 |
| v7o 71.83 | H3；13恢复 | a9/a10在H3处理成果沟通/CI，H未降，a11恢复3→5；无H≤3负向动作 |
| RUN07 72.65 | H1；10恢复（含医疗休假） | a5/6 H3→2→1，a7–10 H1未下降，a11/12恢复1→3→5；a23 H3→1，a24/25立即1→3→5 |
| RUN10 68.40 | H1；13恢复 | a22陪餐 H3→1，紧接季度a23/24恢复1→3→5；另在H2后等待合法Energy恢复2→4 |

RUN07/RUN10确实从低 H 选择后来实现负Health的Story，随后碰到恢复窗口而存活。没有证据表明它们在提交前知道数值成本，不能称“有意接受精确H−2”。高分并不证明这些暴露应复制；能立即恢复是与RUN17重要区别。

donor常用一次/两次恢复后继续推进，不需要为了安全一律到H10。但部分恢复发生在H6/7、或明确急性医疗事件后到10；证据不支持“donor从不高位恢复”或“任何到10都是浪费”。只记录动作量，不把恢复与高分共现作为收益因果证明。

G2若机械规定H≤2必须切保护，将改变RUN07的5个非恢复Story决定、RUN10的3个；这些位置菜单没有明确健康恢复选项。v6/v7o这类冲突为0。暴露次数不是额外恢复次数，也不是8个错误动作。需保留信任/交付/生存关键义务，不能越菜单恢复。

## 5. RUN17关键因果时间线

| 时点 | 可用公开信息 / 实现结果 | 取证判断 |
|---|---|---|
| a11 M3 Energy | H3，广告恢复+2；选恢复到5 | 合法 A 内缓冲管理，不是过度S |
| a12 | H5/E2，旧N→O顺序，最低N=3理由，N不增长 | 确认排序/执行违约；未证明此处必须继续恢复 |
| a13 | H5/E1，预排O，O不增长 | fresh响应没有真正重建比较；不能算机械配平有益 |
| a16/a17 | H5→4→3 | 累积余量下降；季度恢复后并非整窗资源安全 |
| M6 Review / a20 | C，L1→L2，H3 | 已晋升；不能将终局解释为M6晋升失败 |
| a21 | H3，沟通结果，H不变 | 尚有3点余量 |
| **a22** | 带教每天1h、主动Review所有代码/全部会议、两周明显影响个人产出；合法替代为每周同步/自主探索 | 选择高密度方案，实现H3→1、S+1/N+3/O−2；“mandatory duty”并不意味着必须选最大强度；把高工作量成长置于生存余量前 |
| **a23** | H1、CI整块两周、两个排期项目会延后；没有恢复选项，无Health数值广告 | 已意识低资源，选保留手动Review以避免投入；仍H1→0、S−1/O+2，自然终局 |

a22没有明确急性症状警告，但有公开工作量和低余量；a23没有保证安全的选项。不能以 hindsight 指定“CI选1必活”。同类历史中高密度带教出现−2/−3；v7t a35选择放手方案H2→3，支持较轻负荷选项可能有生存价值，但不证明RUN17替代的固定效果，更不得生成event-answer映射。

**可避免性：PLAUSIBLY_AVOIDABLE_BEFORE_A22，非已证明。** a22前可比较余量、工作量、合法低负荷方案、近期恢复可达性；等H1才在下一个不含恢复的菜单选“少做一点”，可能太晚。a12/13若改变投入可增加缓冲是条件假设；实际另一策略会改变事件/数值路径，不能用简单加2宣称救活或重算分数。

归因为混合：设计缺少明确低余量下行比较；执行违背Energy重排并把导师义务扩大到高强度；Story数值不广告和后续冲击增加不确定性。不能分摊百分比，不能称纯坏运气、也不能将a22归为已证K3数字S违约——本局全A。K3限制S本身有价值，需要补的是A内生存排序。

## 6. G0–G4比较与推荐

| Guard | RUN17保护可能性 | donor干扰 / 代价 | 判断 |
|---|---|---|---|
| G0 现状 | a11已有恢复；a22未防止靠近终局 | 允许低点冒险并可能幸存，也可能无恢复窗而死 | 不能认定现行完整生存政策受支持；不是“数字低永不许恢复” |
| G1 广告致命动作 | 三次Health终局均未广告数值成本；识别不到a22/23 | 2654对中广告致命已选动作0，直接干扰很小 | 可作基本比较，但单独不足 |
| G2 一个普通冲击余量 | H1时有理由保资源，但a23无恢复菜单；可能介入太晚 | H≤2草案会碰到donor8个已存活Story决策；何时能恢复必须核菜单 | 有价值但不能升级固定安全阈值 |
| **G3 动态下行** | 结合H3、高工作量、已见冲击、未来恢复不可保证，可在a22比较轻负荷方案 | 也可能改变RUN07 a23/RUN10 a22等成功但暴露的选择；不能保证零干扰 | **最小值得实现和静态验证的假设** |
| G4 固定数字 | H≤2只能在a23介入，菜单无恢复；H≤3扩大干扰 | 无官方安全阈值；会把低数值等同统一S/补满，重演保守 | 不选 |

推荐的单Delta不是新增阈值状态机：在现有 Planning top-two 比较中显式检查 **fresh公开H余量 + 候选广告成本（有则用）+ 公开工作量/已验证经验冲击 prior + 恢复窗口是否真可达**。已知广告会到终局的候选不当普通成长；未知成本不记0，不套隐藏公式。−1/−2普通、−3尾部只作为不确定经验参考，不能写“留下3点就安全”。

低余量时优先比较合法恢复/较低负荷；存在必须履行的生存、信任或近交付义务时仍比较，而不是自动逃避。选一次最小保护→fresh observe→重新比较成长；不规定补到8/10、不预排第二次恢复、不增加S续期。普通H8→10舒适恢复通常要证明优于实际成长；急性症状仍按既有binding规则处理。

位置选 **PLANNING_A**。MODE_S仍留给fresh explicit material binding；preflight仅核已作出的生存比较，不能替代Planning创建新优化器。Option C另起确定性survival machine没有证据优势，Option B低数值强制S会扩大既有死锁风险。

反事实“额外恢复多少、损失几分”均UNKNOWN：观察到的潜在触发不是合法恢复机会，也不是改轨后的成本。H≤2且非恢复且明确恢复菜单可用的donor/RUN17位置计数全部0；不能凭空添加恢复动作。因而 `SURVIVAL_GUARD_SCORE_COST=UNKNOWN`，只可说设计力求小而有界，不能报告已证LOW。

## 7. Energy重排缺陷独立判断

当前 manifest / Planning 已明确“一次Energy→fresh→Board/Delivery→Planning重排”，“旧intent不授权”，“不按最低数字/固定菜单排序”。RUN17仍预排“Health→N→O”，a11fresh后说“Plan N then O”，a12以最低N提交，a13接旧O。原始a11–13fresh链完整，故不是 trace缺失或主要 wording ambiguity。

`ENERGY_REPLAN_ROOT_CAUSE=MODEL_ADHERENCE_FAILURE_WITH_SEMANTIC_PREFLIGHT_CLAIM_ONLY`。当前文字足以表达要求；外部marker检查不证明操作语义，BC=PASS仍能伴随违约。另一个常见问题是响应标签未必clean可归因，不应用错误Board标签替代实际候选收益比较。

未来最小建议：在既有一次Planning rationale中写一次“旧剩余顺序已丢弃；基于fresh H/E、广告与realized response，当前候选相对另一合法项为什么更好”；证据能指出新状态和比较对象。只加 `PREVIOUS_ENERGY_PLAN=DISCARDED` / `CURRENT_RANKING_REBUILT...` 两个声明没有保证，可能重复BC空证书问题。不要另加Skill、重复marker、第二状态机或额外observe。

建议下一任务只实现一个A内生存余量排序Delta，Energy部分作为既有合同的短语义依据/静态反例验收；若需要独立强制执行器，另提架构任务，不能在此顺手升级。验收可使用RUN17、RUN07/RUN10低H但菜单无恢复的反例、高H普通恢复、急性症状资源尚高和合法fatal广告反例，明确不预定具体Story答案。

## 8. 下一阶段决策与验证

一份最小实现任务已合理：需要Stage接受G3的假设和范围，不代表已证可改善分数或正式Candidate通过。优先限制误读为低H无风险、未知cost=0、导师义务=最高负荷；保留A推进和现有K1/K2/Delivery边界。尚未授权新Candidate或新游戏。

本次验证：派生JSON可解析；单局去重；RUN17末段状态/动作行号与既有held contexts交叉核对；冲击384=329+54+1，与Energy40/Story344一致；legacy快照、batch累积窗口、48m完成标志不计自然失败；所选交付文件secret scan及`git diff --check` PASS。没有运行历史tests或Provider。

原始证据仅留本地既定hold路径；派生表不含凭据/DB/无关provider日志。不解除RUN17/RUN16等hold。CURRENT_STATE仅增加一条durable delta；RUN_HISTORY无需新增，因为没有新对局。

`NEXT_GAME=NOT_AUTHORIZED`

`MAIN_V8A_FREEZE_UNCHANGED`
