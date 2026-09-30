# S09-07｜Early Promotion Failure Forensics

## Executive Finding

v7y 首轮 Main 因局部 NO_GAIN 转向单维收益比较，次轮进一步把它外推为全局“封顶”，影响恢复、避险及 Story 成本排序；这是可确认的决策偏移链，**实际未晋升的充分原因仍为 UNKNOWN**，不能声称改选某动作必定晋升。

- Status：COMPLETE；离线证据分析，基线 `main@a6881ff296c2a3f017082e73bf21d7f5161c2b24`。
- Primary：`candidate-v7y-story-exposure-guard`，S09-RUN03R M1–M15，60 successful actions / 61 observes；`DEVELOPMENT_CENSORED_BY_USER_AT_M12`，实际停止 M15。不是自然终局、存活失败或最终分数验证；最后fresh public state为M15/L1、H7/D9/S9/N3/O3/W4/E0。
- Comparison：仅 v6 / v7o 的 M1–M15；未引入 v7x/v7w 或其它对局。每条 Candidate 只有一条选定轨迹，事件、Level、runtime 合同存在差异。
- Decision Gate：推荐 `WORLD_MODEL_CORRECTION`；只是交回 Stage 的下一实验方向，本任务没有新增策略、实验、Candidate 或 live 授权。

## 1. Evidence / 时间与归因边界

| Source | 精确路径 | 本次消费范围 |
|---|---|---|
| v7y events | `D:/CS/CareerSim/.career_sim_runner/career_emu/outputs/local-s06-adaptive-controller/20260930T203812Z/events-20260930T203812Z.jsonl` | 同局 actions、公开 observe、合法选项、Review、action notes；60/61 |
| v7y transcript | 同一目录的 `transcript-20260930T203812Z.log` | 仅定位 Main 排序、NO_GAIN→cap belief、Review continuity 的文本段 |
| v7y receipt | `D:/CS/CareerSim/.local/runtime/s09-run03r-v7y/runner-result.json` | 绑定同一输出目录、实际 stop window 与授权；复用既有 cleanup 事实 |
| v6 donor events | `D:/CS/CareerSim/.career_sim_runner/career_emu/outputs/local-s06-adaptive-controller/20260925T094419Z/events-20260925T094419Z.jsonl` | M1–M15，64 actions / 65 observes |
| v7o donor events | `D:/CS/CareerSim/artifacts/dev-runs/s08-run01-v7o/events.jsonl` | M1–M15，66 actions / 66 observes |
| 现行书面合同 | `skills/structured-state-board/SKILL.md:83–99`；`skills/rolling-planning/SKILL.md:52–64,106–134` | 局部响应、禁止隐藏 cap 推断、Review 重建及 broad compounding 的原合同 |

来源定位复用 [S08-11](S08-11_HIGH_SCORE_CORE_RECOVERY_FORENSICS.md) / [S09-02](S09-02_FAILURE_FLOOR_HIGH_SCORE_JOINT_FORENSICS.md) 已登记的 v6/v7o 身份；本次核对 session、合法菜单与去重序列，没有重算旧 hash。纯离线 parser 复用 `scripts/s09_02_failure_floor_joint_forensics.py` 的公共字段提取函数，不执行其全 cohort 入口。派生结果位于 `D:/CS/CareerSim/.local/runtime/s09-07/public-windows.json`，未归档 raw 或新建实验。

**Review 顺序必须按 events seq 分窗。** v7y 首次 M6 Review 为 seq187，M12 为 seq387。首轮准备窗 A1–A20；下一窗 A21–A45。M6/M12 当月的 Energy/Main 都在该月 Review **之后**，服务下一窗口，不能倒置为已结束 Review 的准备。donor 相同：v6 seq191/seq395；v7o seq187/seq395。以下 A 数字为各局 action index，seq 为 events 序号，不是 event ID。

只消费白名单状态、参与者可见 description/choice/feedback、Agent 已输出的 belief 文本；不读取 hidden effects、promotion formula、共享 DB 或 Provider。跨月 Main 的前后变化存在自动结算混杂，不能当作 clean NO_GAIN 或独立因果效果。donor M15 Main 的后置 M16 observe 被范围截断，不作执行遗漏；v7y M15 尚未到季度菜单，不作漏选机会。

## 2. M6 Failure Table

| Dimension | Finding |
|---|---|
| Opportunity | `PROMOTION_OPPORTUNITY=PRESENT`：有 M6 正式 Review 和 M3 公开成长菜单；“申请关键项目”合法可选。这里 PRESENT 表示可见准备窗口，**当时 actual promotion eligibility=UNKNOWN**，不是保证晋升的按钮。 |
| Action choice | M3 A14/seq133 选“申请岗位轮岗”；notes 为“N/O已NO_GAIN…向responsive的Skill集中”。donor 均选“申请关键项目”。v7y transcript 1269–1308 明确比较过 broad compounding，最终按 assumed-responsive Skill 的最大即时增益选轮岗；不是没看见菜单。 |
| Resource | M3 共3点 Energy：N1/O1/H1；N/O 均 clean unchanged，H4→6。全部20个 action 为 A，没有持续 S、没有未用 Energy。`RESOURCE_DIVERSION=NO`：没有证据支持首轮恢复过量，两条 donor 同样用1/3 Energy 恢复。成长响应不足是事实，整体资源数量不足不是已证原因。 |
| Risk | 首轮所有 R=PASS。合规/关系 Story 有正常语义保护，但没有 Risk WARN/RECONSIDER 拦截 Main 的证据；M9 恢复、M11 Mentor 都发生在本次 Review 后，不能解释 M6。 |
| Review | M6 C/L1/no promotion；公开反馈是观察名单、下一阶段要更清晰成果。A21/seq189 已把 Primary Gap 更新为“更清晰Output/成果”，保持 A；不存在“完全漏读 M6 feedback”的证据。 |
| Confidence | 菜单、选择、排序理由、Review 顺序：高。轮岗与缺少关键项目造成未晋升：中低置信假设；具体拒绝机制 UNKNOWN。 |

**关键反证：** Review 前最后 fresh observe，v7y/v6/v7o 的 S/N/O 都为 **9/3/3**；三局 M6 均为 **C**，但两条 donor 已 L1→L2，v7y 仍 L1。不能把公开数值或 C grade 当成 promotion formula。新的 C/B checkpoint grade 来自本次 raw public feedback；没有用 donor final A 代替 checkpoint grade，也不改写旧报告当时的 UNKNOWN。

更窄的公开 matched context：v7y A14 与 v6 A14 均 M3/L1、H6/D10/S9/N3/O3/W1/E0、tenure3、同一 Main 菜单；一个选轮岗，一个选关键项目，下一 M4 observe **两局 S/N/O 都未增加**。因此“Main 没有即时数值增长→没有 promotion-relevant value”不获支持；后续 Story 不同，仍不能从这对记录推出 Main 的晋升因果。

## 3. M12 Failure Table

| Dimension | Finding |
|---|---|
| Opportunity | `PROMOTION_OPPORTUNITY=PRESENT`：M12 Review，M6/M9 两次 Main 均有关键项目；actual eligibility 仍 UNKNOWN。 |
| Action choice | M6 A26 选“向领导汇报成果”，直接响应反馈；M9 A39 选“低调避险”。两条 donor 同窗各两次关键项目。v7y 没有完成 donor 的 broad Main cadence；这不证明固定动作配额有效。 |
| Resource | Review 间6点 Energy：Skill2、Health4；Skill 测试无增益，N/O 无 Energy 投入。M9 H2→4→6→8，继而 Main H8→M10 H9；四个 S actions 后 A40 回 A。`RESOURCE_DIVERSION=YES`：保护占用了全部 M9 Energy 与 Main；额外保护的必要性/净晋升损失 UNKNOWN，没有长期 S deadlock。 |
| Risk | M8 有公开“近期有点风险，不过问题还不大”；M9 没有 fresh evidence 证明所有成长路径都无价值。A39 同时用风险提示及“封顶无机会成本”选避险；不能简单把避险本身判错。M11/M12 又有公开风险提示，说明一次 cleanup 没有建立可验证的持久解除。 |
| Review | M6 Gap 被吸收并持续到 M12；但 M9 已从成果准备转为 buffer/risk，M11 A44 主动接受明确个人产出成本，O3→1，M12 Review 前仍 O1。M12 C/L1/no promotion，A46 更新为“要会赢/更清晰可见成果”。M12 随后的 O0→1→2→3 属下一窗修复，不是赶上已结算 M12。 |
| Confidence | cap belief 改变排序、预算占用、Mentor 的公开 O 损失：高。它们造成 M12 未晋升：中置信假设；不能排除首轮失晋后的路径差异、事件及未知 eligibility。 |

**RQ2：同一条瓶颈链延续，新增机制不能合并成同一个已证原因。** 首轮是局部响应驱动的 Main 缩窄；次轮出现明确全局 cap belief、追加防护和 Review 前 Story 成本折价。首轮差距已经形成，M9/M11 是次轮的追加偏移，不能反过来充当首轮原因。

## 4. Cross Candidate Comparison

| Dimension | v7y | v6 | v7o |
|---|---|---|---|
| Growth / Main | 已到达 M3/6/9/12 Main：轮岗、汇报、避险、避险；关键项目0/4 | 相同四次 Main：关键项目4/4 | 相同四次 Main：关键项目4/4 |
| M6前 Energy（3点） | N1/O1/H1；N/O clean零增益 | O2/H1；O首次+1、再一次0 | N1/O1/H1；N/O各+1 |
| M6后→M12前 Energy（6点） | S2/H4；S0增益，M9全恢复 | O1/N1/H2/风险清理2；O+1，N0 | O4/H2；四次 clean O+1 |
| Risk / MODE | R=PASS 60/60；A56/S4；S全部位于 M9，随后退出 | MODE枚举缺失，不能记为零S；M6用2点处理历史风险，仍两次 broad Main | M1–15 A65/S1；Review间A25/S1；保护后 broad Main 继续 |
| Review前 S/N/O | M6：9/3/3；M12：9/3/1 | M6：9/3/3；M12：20/6/5 | M6：9/3/3；M12：21/7/6 |
| Review前 H/D | M6 H4/D10；M12 H7/D10 | M6 H5/D10；M12 H5/D10 | M6 H5/D9；M12 H5/D10 |
| Promotion trajectory | M6 C L1→L1；M12 C L1→L1；M15仍L1 | M6 C L1→L2；M12 B L2→L3；M15 L3 | M6 C L1→L2；M12 B L2→L3；M15 L3 |

该表使用 **Review前** 状态，避免把 donor 晋升后的 M6 Story/Energy 收益倒算为 eligibility 证据。M15 范围仅用来查看既有持续性，不消费 donor M18+。第一次晋升改变后续 Level 与响应环境，M12 的 stats/收益差距不能全部归因于资源分配。

反例也必须保留：v6 同一第二窗用了 H2+风险清理2，保护预算也是 **4/6**，却晋升；故“4/6非成长 Energy→必定失败”不成立。v6 首轮也记录 Output 重复零增益/“饱和”，但随后仍选择 broad Main；问题更具体地落在 **belief 的外推及应用**，而非禁止记录 NO_GAIN、禁止恢复或机械增加 Output。

## 5. Story / Risk Override Audit

| Record | Classification | 可确认的机会成本与限制 |
|---|---|---|
| M9 A36（seq309→315）H2→4 | Necessary Protection（合理目的，必要程度 UNKNOWN） | 低 H 且刚经历暴雨损耗；一次恢复确实生效。没有公开证据证明必须完整恢复到8或反事实安全界限。 |
| M9 A37/A38（seq317/325→323/331）H4→6→8 | Opportunity Cost + Incorrect Threat Model | 两点 Energy 被额外 buffer 用掉，notes 以“S/N/O/D封顶无机会成本/无可用项”抹掉剩余成长价值。新观察存在，但未证明同一重大约束仍 binding；仍不能量化替代成长的净收益。 |
| M9 A39（seq333→339）低调避险 | Opportunity Cost；风险保护净必要性 UNKNOWN | 正在 H8、公开轻度风险提示存在；不是“poor grade alone→S”。可见多维 Main 被排后，排序中的“唯一可响应/无机会成本”来自错误外推。不是 Risk Skill 强制 gate。 |
| M7 A28（seq245→251）周末认证 | Unknown | 公开情境是周二正常交付即可，周一提前交付能省客户一天联调；选培训后 S9不变/O3→2/H5→4。存在 immediate output 成本与长期收益取舍，没有证据把它判为 binding delivery failure。 |
| M11 A44（seq373→379）高密度 Mentor | Opportunity Cost + Incorrect Threat Model | 当前描述明确说个人产出会受影响，备选放手节奏能专注本职；notes 用“Output已封顶，产出受影响的数值成本有限”折价。fresh observe 同月 H9→7/O3→1，N未增；实际总价值、未选项效果 UNKNOWN。 |
| M9 A35 共享伞 | Unknown | 明确暴雨暴露下选共享伞，存在保护语义；“两人都不淋湿”是 Agent 假设。H3→2伴随月末 Energy refill，非孤立健康因果；不能认定 Story Guard 的确定漏触发或失败是晋升根因。 |

## 6. World Model Error Audit

分类：**`BELIEF_ERROR_CONFIRMED`，确认的是证据外推/排序错误，不是证明模拟器事实上没有 cap。** hidden cap 是否存在、具体数值、晋升公式都 UNKNOWN。本任务不查隐藏实现来补答案。

| 来源链 | Evidence | 判断 |
|---|---|---|
| 局部事实 | M3 A11 N3→3、A12 O3→3，为同月、同Level、单动作成功后的 clean unchanged | 可记录局部 NO_GAIN；不是错误本身。 |
| Main路径外推 | A14 以此前 Story 的 Skill gain 认定轮岗“confirmed-responsive”；轮岗后 M3→M4 S9→9。transcript 1265–1308、1330、1437、1486 | 其它路径过去有 gain，不保证当前 Main 的 gain；跨月自动结算不能建立 clean response。随后开始推测“L1上限”。 |
| 假说升级为事实 | M6 A24 clean Skill learning S9→9；transcript 2520：“确认 L1下 S/N/O/D全部封顶，仅 Health可响应”；A25 notes 同义 | 一次局部测试没有证明所有路径/值都封顶；违反 Board line99、Planning局部响应合同。首次明确“全部封顶”在 M6 Review之后，不能回填成 M6前已成立的原因。 |
| 排序被 belief 改变 | A37/38：“封顶无机会成本/无可用项”；A39：“封顶不响应，唯一…Health/risk”；A44：“Output已封顶…成本有限” | 不是仅措辞错误；已有恢复分配、Main保护选择及Story成本折价的实际应用。 |
| 仍沿用该假说 | M12 A51/seq433→439 明确“L1上限”，A52/seq451“唯一…无机会成本”；此时 S=7，低于同局此前9。M13 A53/seq459→465 S7→9，Level仍L1 | 后续同Level增长表明不能把所有当前价值概括成零，response应依据fresh evidence核验；未单独证明该Story符合Board advertised-dimension的clean GAIN条件，不证明 O3 cap真假，也不保证某特定未选 Main 有gain。M12后数据仅用于belief持续性，不能解释已结束Review。 |

这条链也不是“静态规则没写清”：现行 Board/Planning 已禁止 cap/eligibility 推断，规定 NO_GAIN 只局部折价，保留其它 GAIN/UNKNOWN 价值。M3 transcript 1281/1293 甚至复述这些规则，仍把瞬时响应优先级变为整体 Main 选择，后续转为确定 cap。可确认 **runtime adherence/world-model 使用偏移**；不能据此声称新增更多 Prompt 规则一定有效。

## 7. Review Interpretation / 被排除的主因

- **没有晋升准备机会：不支持。** 合法菜单和两个正式窗口均存在；是否符合未知 promotion eligibility 仍 UNKNOWN。
- **首轮长期 S 或过量恢复：不支持。** M6前20/20为A、恢复1/3 Energy，与donor相同。M9之后才有四个S，不能解释M6。
- **公开S/N/O低、C grade本身阻断晋升：不支持。** 三局首轮pre-review同为9/3/3，C；donor却晋升。数值无法替代隐含组织评审证据。
- **M6 feedback 完全漏读 / Review→Planning→Action 完全断裂：不支持。** A21明确新Gap，A26选成果汇报；A46再次吸收M12反馈。完整 `REVIEW_PLAN / Next Review Checkpoint` 重建仍 INCONCLUSIVE（transcript只有初始literal plan，缺少完整后续可审字段），但缺字段不足以认定主因。
- **Risk Skill过度否决成长：不支持。** v7y全部R=PASS，无WARN/RECONSIDER强制改选；Planning自身的保护排序仍需区分。
- **Story Guard 造成失败：UNKNOWN。** 无明确单独 guard attribution、无未选项反事实；不得把所有保护或Story损耗归给v7y唯一delta。
- **Provider/Runner故障解释未晋升：无现有支持。** 60成功动作、60次动作后fresh observe；未读新Provider/服务数据，不作全面故障排除。

## 8. Root Cause Ranking / Decision Gate

| Rank / Confidence | Failure hypothesis | 证据与因果边界 |
|---|---|---|
| 1 / 高（行为）；中（未晋升归因） | 局部 NO_GAIN→全局 cap / 零机会成本，改变成长、保护、成本排序 | 明确 belief文本与实际动作相连，M6后→M12尤其清晰。可以确认错误应用，不能确认其单独导致Review拒绝。 |
| 2 / 中低（晋升因果） | broad Main / realizable-result 比较被瞬时单维响应缩窄，首轮 compound engine未建立 | M3可见matched context与donor不同，M6后继续汇报/避险；donor broad Main +早晋升共同出现。但Main即时S/N/O变化、Story差异、Level反馈循环阻止因果定论。 |

**唯一推荐：`WORLD_MODEL_CORRECTION`。** 已有可确认的错误belief及其应用，优先交Stage处理；下一授权实验需要回答“纠正局部响应外推后，是否仍把成长/成果成本判为零，以及Main排序是否恢复可审的晋升价值比较”。本任务不设计或实施修复，不创建实验，不申请/消费game。

`FIRST_REVIEW_BOOTSTRAP` 暂不优先：首次Review前UNKNOWN Gap符合合同，后续feedback被消费，完整计划字段虽有缺口，尚无其主导失败的证据。`PROMOTION_PORTFOLIO_REBALANCE` 暂不优先：先处理belief中介，避免把必要防护与错误“无成本”排序混为权重问题。`NO_ACTION_YET` 不选：已足够定位可干预的证据错误；**promotion拒绝的实际内部原因仍UNKNOWN**。

## 9. Verification / Hold / Handoff

- 精确三条source；session-binding、seq去重、M1–M15过滤与合法菜单检查完成；v7y 60 successful actions都紧接fresh observe，没有跨动作状态复用。donor M15后置观察不在本次范围。
- 交付仅此报告与CURRENT_STATE一条durable delta；selected secret scan与`git diff --check`已通过；commit/push身份由TASK_RESULT记录。未重跑tests、游戏或全历史分析；未重算已有hash、归档raw或修改frozen行为/validation flags。
- 原始文件仍在原精确目录，已有 `FORENSIC_HOLD` 全部保持；S09 Stage/Main接受结论并确认后续取证/child依赖解除之前，不删除、迁移或解除hold。
- 返回Stage做下一路线决定；本任务不宣布Stage COMPLETE。

`NEXT_GAME=NOT_AUTHORIZED`
