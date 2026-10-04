# S10-16 — Risk-Control Divergence

**COMPLETE_WITH_PUBLIC_ATTRIBUTION_LIMITATIONS / IN_FLIGHT_EVIDENCE**

唯一 primary decision：**PATH_DEPENDENT_NO_SAFE_PATCH**。不提出 V6E_RISK_PATCH_PROPOSAL，不创建或修改 Candidate。

FACT：公开 risk_control 点数确为10→4，总分71.67→65.35。Run02还显示M28–M30严重HR warning streak与M30聚合隐患回执。INFERENCE：不同暴露/历史更能描述这次公开表现差异；但不能把6点归到某个Story、intensive、cleanup或潜在风险值。没有发现满足跨情境、公开、可推广且保持成长性标准的单一风险补丁。

## Identity / source boundary

Branch `codex/s10-16-risk-control-divergence`；base `0a7e9349d73b443efa91721fab01067f969d1a1b`（accepted S10-15 child evidence，串行checkout，无worktree）。Exact Candidate `candidate-v6d-promotion-portfolio-rebalance`，source `e7e8ab44dd85a29135eb089ef29de8fed298f4a4`；Run01 `5eb108b55a9f252d4fd6ff4561120d353f9d124b`，Run02 `ce92da5cda9c5da2e2b4f2140e35880e8ea77a6a`。Run01/Run02 source SHA、三Skills、Runner、Provider config hash、dependency版本一致，复用S10-15已核身份并重新核必要held来源。Candidate/Skill/manifest/Runner/dependencies/provider/retry未改。Result commit由最终TASK_RESULT记录，避免自引用SHA。

只使用held public-policy-data、participant tool回执的public字段、held reasoning/LLM-retained assistant片段、合法终局component points。S10-15 actual-input缺口仍有效：普通streaming request完整messages UNKNOWN；这里能证明reasoning说了什么，不宣称每个时刻实际完整prompt已重建。不读取shared DB/simulator源码/Test/hidden stock或counter，不使用历史dataset的advertised HiddenRisk字段或score未来标签，不逆推score formula。v6仅hash-locked accepted public projection及终局public observe，未扩大到全历史Candidate。

原Run01/Run02各12文件FORENSIC_HOLD不解除、不删除；本地source/path/hash可见JSON。一次性分析在ignored `.local/scratch/s10-16/`，是可重建派生物；原raw仍在既有runtime/Runner目录。仅交付本报告、compact evidence与branch-local CURRENT_STATE；不提交raw transcript、LLM logs或原始对局重复副本。

## Published score gap

| Published component | Run01 | Run02 | Δ |
| --- | --- | --- | --- |
| level | 15.0 | 15.0 | 0.0 |
| wealth | 9.93 | 8.1 | -1.83 |
| resilience | 13.5 | 14.25 | 0.75 |
| skill | 14.25 | 15.0 | 0.75 |
| risk_control | 10.0 | 4.0 | -6.0 |
| network | 9.0 | 9.0 | 0.0 |

公布round组件合计差−6.33，正式总分差−6.32，不能据此逆推精度或内部公式。Risk-control−6.00是最大公开组件差，但不是全部：Wealth−1.83，Skill/Resilience各+0.75，Level/Network不变。此表是公开终局association，**不是公开动作的因果分解**。原legal ending_score的raw counter/weights不投影进报告。

## Matching and five different choices

重新提取成功Story两局各144；Run02两个invalid tool route不计第二个decision。Exact description + legal action text set匹配96，91同选、5异选，同Level24。算法沿用accepted Run02：每个Run02情境取Run01首次出现；所以96是matched decision occurrences，不一定96个独立unique实验。未按title/ID匹配，不建立event答案表；这些witness只用于离线取证，不能送回runtime。

五案的latest HR、latest warning、前序material incident（有明确月份/age，旧事不冒充fresh）、fresh pre/post、完整合法动作语义、Risk reasoning与LLM/transcript位置均在JSON。只链接明确同一narrative follow-up；下一普通HR警告不能自动归给上一选择。

### Different case 1 — STATE_DEPENDENT

Public situation：公司园区食堂人多，组里同事习惯中午 12:00 在工区附近小餐馆聚餐，聊项目八卦和 Leader 动向——这是非正式情报网。你家住地铁 40 分钟外，回家吃午饭来回紧张，但能午睡 20 分钟、吃妈妈做的菜，下午精力更稳。入职三个月来你多数回家，同事开始叫你「独行侠」。Leader 上周团建说「多和团队融一融」。

Legal semantic actions：改为每周至少三天和同事一起吃；坚持回家，用下午高效产出证明；折中：周二周四跟同事吃，其余回家。

Run01：M25 raw825，L4 tenure2，S/N/O/W/H/D=45/15/17/11/10/10；选择“改为每周至少三天和同事一起吃”。Risk rationale：Health10、Network偏弱且Leader要求融入，接受更强聚餐投入；当前候选无material risk。

Run02：M1 raw41，L1 tenure1，S/N/O/W/H/D=3/2/0/1/5/6；选择“折中：周二周四跟同事吃，其余回家”。Risk rationale：Health5，平衡融入和午休；拒绝孤立，同时保留rest。

立即 public delta / follow-up：Run01 {'skill': 0, 'network': 3, 'output': 0, 'wealth': 0, 'health': -1, 'dignity': 0}（CLEAN_PUBLIC_PAIR_SAME_MONTH_LEVEL）；Run02 {'skill': 0, 'network': 2, 'output': 0, 'wealth': 0, 'health': 1, 'dignity': 1}（CLEAN_PUBLIC_PAIR_SAME_MONTH_LEVEL）。No strict trust-risk ordering; Health5 versus10 justifies different resource tradeoff。
### Different case 2 — PLAUSIBLE_RISK_DIFFERENCE

Public situation：平时少联系的财务同事孙姐请你在「外婆家」吃饭，第三杯酒后开始问：「听说灵犀要并组？Leader 会不会换？你们组谁可能走？」 她丈夫在猎头发朋友圈。你掌握的信息：并组草案存在但未定，程磊可能调岗——均未公开。

Legal semantic actions：一律说不知道，转移话题；透露已公开信息，暗示「听领导安排」；如实聊并组草案与程磊可能调岗。

Run01：M15 raw497，L3 tenure4，S/N/O/W/H/D=35/10/11/6/9/10；选择“一律说不知道，转移话题”。Risk rationale：既往泄密调查后更谨慎；认为只谈public也可能被套话，最终完全转移话题。

Run02：M18 raw581，L4 tenure1，S/N/O/W/H/D=39/14/15/6/8/10；选择“透露已公开信息，暗示「听领导安排」”。Risk rationale：明确否决未公开草案披露，认为public information+neutral deflection可保关系且守密；不是故意选择泄露机密。

立即 public delta / follow-up：Run01 {'skill': 0, 'network': 0, 'output': 0, 'wealth': 0, 'health': 0, 'dignity': 0}（CLEAN_PUBLIC_PAIR_SAME_MONTH_LEVEL）；Run02 {'skill': 0, 'network': 1, 'output': 0, 'wealth': 0, 'health': 0, 'dignity': 0}（CLEAN_PUBLIC_PAIR_SAME_MONTH_LEVEL）。Full deflection has less disclosure exposure; public-only alternative is not clearly unsafe from action text。
### Different case 3 — PLAUSIBLE_RISK_DIFFERENCE

Public situation：你对公司积攒了不少不满，想去匿名点评平台给公司打个低分、写段吐槽，提醒后来者也出口气。

Legal semantic actions：若要写就只陈述客观事实、不夸大不泄密、不人身攻击；情绪上头写长文细数恩怨、夹带未证实指控；忍住不写，把不满转成是否离开的理性判断。

Run01：M16 raw545，L3 tenure5，S/N/O/W/H/D=38/13/15/6/8/10；选择“若要写就只陈述客观事实、不夸大不泄密、不人身攻击”。Risk rationale：认可objective/no-leak/no-personal-attack表达合法；反复比较后按公开约束表达。

Run02：M23 raw757，L4 tenure6，S/N/O/W/H/D=52/21/19/10/9/10；选择“忍住不写，把不满转成是否离开的理性判断”。Risk rationale：当前HR积攒风险，选择不留下公开负评，改为理性职业判断。

立即 public delta / follow-up：Run01 {'skill': 0, 'network': 0, 'output': 0, 'wealth': 1, 'health': 0, 'dignity': 0}（MIXED_MONTH_OR_LEVEL_TRANSITION_NOT_SINGLE_ACTION_ATTRIBUTION）；Run02 {'skill': 0, 'network': 0, 'output': 0, 'wealth': 0, 'health': 1, 'dignity': 0}（CLEAN_PUBLIC_PAIR_SAME_MONTH_LEVEL）。Run02 avoids public posting; Run01 explicitly prohibits leaks/falsehood/attacks, also defensible。
### Different case 4 — STATE_DEPENDENT

Public situation：你观察三年：升得最快的是贺帆——技术一般，但 KTV、球局、帮 Leader 接孩子从未缺席。你技术评分连年第一，晋升慢半拍。老周说「也要看综合」。

Legal semantic actions：学习投入非正式场合，控制底线；拒绝迎合，加倍技术产出；向 HRBP 反映晋升标准模糊；跳槽准备，减少投入。

Run01：M32 raw1065，L4 tenure9，S/N/O/W/H/D=66/31/25/18/8/10；选择“学习投入非正式场合，控制底线”。Risk rationale：visibility与关系价值，愿接受有底线的非正式场合投入。

Run02：M30 raw989，L4 tenure13，S/N/O/W/H/D=71/36/25/14/6/8；选择“拒绝迎合，加倍技术产出”。Risk rationale：刚收到重大隐患回执，Health6且Network相对强；避免已见过的社交Health成本，转技术产出重建。

立即 public delta / follow-up：Run01 {'skill': 0, 'network': 3, 'output': 0, 'wealth': 0, 'health': -2, 'dignity': -1}（MIXED_MONTH_OR_LEVEL_TRANSITION_NOT_SINGLE_ACTION_ATTRIBUTION）；Run02 {'skill': 3, 'network': -2, 'output': 1, 'wealth': 0, 'health': 0, 'dignity': 2}（CLEAN_PUBLIC_PAIR_SAME_MONTH_LEVEL）。Run02 protects current Health after incident; not a confidentiality or integrity violation。
### Different case 5 — STATE_DEPENDENT

Public situation：部门今年的年度团建需要从各组选一位「内部组织者」，负责前期调研团队偏好、敲定形式（户外 / 聚餐 / 桌游）、对接 HR 行政、当天主持。这个角色和 OKR 完全无关，但成果直接影响整个部门 80 多人那两天的体验，是 Leader 们公开会看到的「软实力曝光位」。Leader 在群里问谁主动报名。你最近手头有一个排期项目，承担组织者会让你接下来三周每天多花 1-2 小时在团建准备上。

Legal semantic actions：主动报名担任组织者；不报名，把精力留给手头排期项目。

Run01：M45 raw1505，L5 tenure4，S/N/O/W/H/D=108/44/34/35/9/10；选择“主动报名担任组织者”。Risk rationale：Health9、临近Review，接受公开软实力机会与资源成本。

Run02：M45 raw1469，L5 tenure10，S/N/O/W/H/D=122/50/38/27/6/10；选择“不报名，把精力留给手头排期项目”。Risk rationale：Health9→7→6持续下滑，额外三周负荷可能加重；拒绝报名并保护本职交付。

立即 public delta / follow-up：Run01 {'skill': 1, 'network': 3, 'output': -2, 'wealth': 0, 'health': -2, 'dignity': 0}（CLEAN_PUBLIC_PAIR_SAME_MONTH_LEVEL）；Run02 {'skill': -1, 'network': -2, 'output': 0, 'wealth': 0, 'health': 1, 'dignity': 0}（CLEAN_PUBLIC_PAIR_SAME_MONTH_LEVEL）。Run02 avoids extra load at falling Health6; Run01 can afford it atHealth9。


关键饭局对照：Run01 M15最新HR=MILD（原积攒warning来自M12–14）；Run02 M18最新HR=MILD且刚升L4，并有较早M11同类hint后主动承认的历史。Run02 raw581→observe587明确“猎头联系程磊，Leader排查信息源”；raw589选择主动承认、Network15→13，未显示clearance。Run01全deflect后没有该follow-up，但不证明任何状态下都必然安全。**只谈已公开信息在动作语义上不是明确泄密**，因此不是CLEAR_RISK_DIFFERENCE，更不能从终局4倒推答案。

匿名评论案里Run02反而选更少public exposure的路径；技术/关系案与组织者案都基于实际Health、负荷/事故历史变化。五案没有CLEAR_RISK_DIFFERENCE、NO_RISK_RELEVANCE或UNKNOWN：3 STATE_DEPENDENT、2 PLAUSIBLE（方向并不都对Run02不利）。

## Same-choice risk sample / path dependence

Functional taxonomy共8类：CONFIDENTIALITY/DATA、COMPLIANCE/INTEGRITY、TRANSPARENCY/DISCLOSURE、BLAME/ACCOUNTABILITY、SECURITY/RELIABILITY、TRUST/RELATIONSHIP、HEALTH/WORKLOAD、OTHER。分类依据当前public功能语义，不是事件标题。选择风格SAFE_DIRECT / SAFE_WITH_TRADEOFF / AMBIGUOUS / RISK_ACCEPTING / CLEARLY_UNSAFE；最后一类必须明确泄密、伪造、隐瞒material事故或违规上线，普通工作成本不算。

从91同选中审16个risk相关matched decisions，两局状态/tenure/HR/备选与结果均保留，覆盖数据、保密、披露、责任、安全、信任。样本每局4 SAFE_DIRECT、11 SAFE_WITH_TRADEOFF、1 RISK_ACCEPTING；不把该比例当全局safe rate。

| Functional class | Run01 raw / month | Run02 raw / month | Choice style | Public behavior |
| --- | --- | --- | --- | --- |
| CONFIDENTIALITY_DATA | 73 / M2 | 345 / M10 | RISK_ACCEPTING | 暗示「近期可能有变动，建议谨慎」，不透露文件 |
| TRANSPARENCY_DISCLOSURE | 81 / M3 | 353 / M11 | SAFE_WITH_TRADEOFF | 主动找 Leader 承认给了模糊建议 |
| CONFIDENTIALITY_DATA | 977 / M30 | 145 / M4 | SAFE_DIRECT | 拒绝接收，建议他走合规交接 |
| BLAME_ACCOUNTABILITY | 433 / M13 | 677 / M21 | SAFE_WITH_TRADEOFF | 改写报告，强调流程缺陷与师徒共担 |
| TRANSPARENCY_DISCLOSURE | 465 / M14 | 973 / M30 | SAFE_DIRECT | 第一时间主动同步，带上原因分析、补救方案和新时间表 |
| COMPLIANCE_INTEGRITY | 1457 / M43 | 393 / M12 | SAFE_WITH_TRADEOFF | 立刻低声提醒 Leader 口径差异，建议现场改口径 |
| SECURITY_RELIABILITY | 769 / M24 | 1517 / M46 | SAFE_WITH_TRADEOFF | 立即截图留证，向安全部门正式报告 |
| TRUST_RELATIONSHIP | 817 / M25 | 1545 / M47 | SAFE_WITH_TRADEOFF | 主动向团队澄清事件经过和举报流程，强调安全红线 |
| CONFIDENTIALITY_DATA | 737 / M22 | 1237 / M37 | SAFE_WITH_TRADEOFF | 完全保密，表示不能讨论任何会议内容 |
| TRUST_RELATIONSHIP | 745 / M23 | 1245 / M38 | SAFE_WITH_TRADEOFF | 向他解释保密是职业纪律要求，表达个人关心但坚持边界 |
| COMPLIANCE_INTEGRITY | 337 / M10 | 129 / M4 | SAFE_WITH_TRADEOFF | 坚持原创节奏，主动申请延期并把风险写进汇报 |
| TRANSPARENCY_DISCLOSURE | 665 / M20 | 493 / M15 | SAFE_DIRECT | 主动在PR注释中说明AI辅助生成并解释修改点 |
| COMPLIANCE_INTEGRITY | 777 / M24 | 1285 / M39 | SAFE_WITH_TRADEOFF | 向HR匿名报告观察到的利益关系风险，要求调查 |
| SECURITY_RELIABILITY | 561 / M17 | 981 / M30 | SAFE_WITH_TRADEOFF | 只关注核心逻辑与隐患，小问题让作者自己迭代 |
| TRANSPARENCY_DISCLOSURE | 177 / M5 | 137 / M4 | SAFE_WITH_TRADEOFF | 会后发邮件书面澄清，不在会上泼冷水 |
| TRUST_RELATIONSHIP | 1601 / M48 | 385 / M12 | SAFE_DIRECT | 婉拒抱团施压，选择基于个人贡献单独、理性地争取自己的调薪 |

最强same-choice反例：两局都基于未官宣闭门纪要给好友模糊方向，均有Leader排查；Run01 M2→M3对应SERIOUS HR，Run02 M10→M11对应MILD，随后两局都主动承认。说明“同选”不等于相同状态/历史或warning结果；但不能测量path随机性或hidden风险库存。

另一个重要反例：Run01 M17与Run02 M30都选CodeReview抓核心逻辑/隐患，小问题作者迭代；只有Run02 raw981后的fresh observe987叠加“之前的隐患好巧不巧一起炸了，最近半年的工作都打了水漂！”。同step公开S−1、O−1、W−2、D−2、H+1。该回执明确指向之前隐患，故标 **MIXED_PUBLIC_AGGREGATE_INCIDENT**，不能把损失归给当前CodeReview，也不能倒填为M18饭局或M27intensive的延迟效果。Run01没发现同类public aggregate回执。

## Complete public warning timeline

Ordinal仅NONE / MILD / SERIOUS / UNKNOWN，无私赋数值。NONE=当前HR“最近干得还不错”，**不等于旧调查/合规危险已clear**。MILD包含“有点风险，问题还不大”及“积攒了不少风险”；SERIOUS包含“自求多福”“之前埋的雷全要炸了”。重复observe同月同文去重；这些label不是HiddenRisk proxy formula。

| Current month | Run01 | Run02 |
| --- | --- | --- |
| M1–M6 | UNKNOWN, MILD, SERIOUS, MILD, MILD, MILD | UNKNOWN, NONE, NONE, SERIOUS, MILD, MILD |
| M7–M12 | NONE, MILD, MILD, MILD, MILD, MILD | NONE, NONE, NONE, NONE, MILD, NONE |
| M13–M18 | MILD, MILD, MILD, NONE, MILD, SERIOUS | NONE, NONE, NONE, MILD, MILD, MILD |
| M19–M24 | MILD, MILD, NONE, NONE, NONE, NONE | MILD, MILD, MILD, MILD, MILD, NONE |
| M25–M30 | MILD, NONE, NONE, NONE, MILD, NONE | NONE, NONE, MILD, SERIOUS, SERIOUS, SERIOUS |
| M31–M36 | NONE, NONE, NONE, NONE, MILD, NONE | NONE, NONE, NONE, MILD, MILD, NONE |
| M37–M42 | NONE, NONE, NONE, NONE, NONE, NONE | NONE, NONE, NONE, MILD, MILD, MILD |
| M43–M48 | NONE, NONE, NONE, NONE, MILD, MILD | NONE, NONE, NONE, NONE, NONE, NONE |

| Run | MILD | SERIOUS | NONE | UNKNOWN | First warning | Longest streak | M46/M47/M48 | Terminal receipt |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Run01 | 20 | 2 | 25 | 1 | M2 | 8 | NONE,MILD,MILD | M49 NONE |
| Run02 | 17 | 4 | 26 | 1 | M4 | 8 | NONE,NONE,NONE | M49 MILD |

Run01最长streak M8–M15；Run02 M16–M23，均8个月。Run02严重streak M28–30，Run01严重警告M3/M18分开。warning-free periods及每次Review的HR源行都在JSON。M1尚无HR observation记UNKNOWN；终局最后一步后的public clock显示M49，只作为terminal receipt记录，不算第49个月游戏、不纳入48月统计。Final quarter M46–48：Run01 NONE/MILD/MILD，Run02 NONE/NONE/NONE；terminal receipt则Run01 NONE、Run02 MILD。不能从终局warning一种表面信号推导score。

## Cleanup timeline and public response delay

Run01七次、Run02四次全部逐次审。latest current HR与latest actual warning分别列出，避免把praise当clearance。FRESH分类指previous cleanup之后新收到warning；新月相同措辞也算新的public read，不伪造warning severity增长。OTHER包括没有新HR warning但有当前material incident。

| Run / Month / raw action | Latest HR | Latest warning / age months | Class | Next HR | Closure |
| --- | --- | --- | --- | --- | --- |
| Run01 M6 / 209 | M6 MILD | M6 MILD / 0 | FRESH_MILD_RESPONSE | M7 NONE | UNKNOWN |
| Run01 M12 / 409 | M12 MILD | M12 MILD / 0 | FRESH_MILD_RESPONSE | M13 MILD | UNKNOWN |
| Run01 M15 / 505 | M15 MILD | M15 MILD / 0 | FRESH_MILD_RESPONSE | M16 NONE | UNKNOWN |
| Run01 M18 / 601 | M18 SERIOUS | M18 SERIOUS / 0 | FRESH_SERIOUS_RESPONSE | M19 MILD | UNKNOWN |
| Run01 M21 / 697 | M21 NONE | M20 MILD / 1 | FRESH_MILD_RESPONSE | M22 NONE | UNKNOWN |
| Run01 M24 / 793 | M24 NONE | M20 MILD / 4 | OTHER_PUBLIC_RISK_RESPONSE | M25 MILD | UNKNOWN |
| Run01 M48 / 1617 | M48 MILD | M48 MILD / 0 | FRESH_MILD_RESPONSE | M49 NONE | UNKNOWN |
| Run02 M6 / 209 | M6 MILD | M6 MILD / 0 | FRESH_MILD_RESPONSE | M7 NONE | UNKNOWN |
| Run02 M12 / 409 | M12 NONE | M11 MILD / 1 | FRESH_MILD_RESPONSE | M13 NONE | UNKNOWN |
| Run02 M30 / 1005 | M30 SERIOUS | M30 SERIOUS / 0 | FRESH_SERIOUS_RESPONSE | M31 NONE | UNKNOWN |
| Run02 M42 / 1389 | M42 MILD | M42 MILD / 0 | FRESH_MILD_RESPONSE | M43 NONE | UNKNOWN |

Run01：5 FRESH_MILD、1 FRESH_SERIOUS、1 OTHER；Run02：3 FRESH_MILD、1 FRESH_SERIOUS。0 confirmed REPEATED_WITHOUT_NEW_WARNING，不等于证明全部cleanup必要。Run01 M21最新HR已positive但M20有新mild warning；M24没有新HR warning，却有安全事件/匿名report后报复情境。Run02 M12最新HRpositive，但M11发生hint调查与mild warning，另有promotion后的协作摩擦。不得用“没有当前negativeHR”否认这些公开风险来源。

每笔cost2E，通常季度总预算3E；有report/Network/Health或其它合法成长备选。public S/N/O/W/H/D cleanup前后均flat；这既不证明cleanup无效，也不证明潜在风险降幅。全部cleanup后explicit相关clearance=0；后续positiveHR不是closure。安全部门“确认泄露风险可控”两局各1次，只是该data事件scope-limited containment，伴随同事处分/关系反弹，不能升级为全局trust清除。

| Run / fresh SERIOUS month | Next cleanup | Delay months | First legal affordable cleanup quarter | Other SERIOUS before cleanup |
| --- | --- | --- | --- | --- |
| Run01 M3 | M6 | 3 | M3 | None |
| Run01 M18 | M18 | 0 | M18 | None |
| Run02 M4 | M6 | 2 | M6 | None |
| Run02 M28 | M30 | 2 | M30 | M29,M30 |
| Run02 M29 | M30 | 1 | M30 | M30 |
| Run02 M30 | M30 | 0 | M30 | None |

Run02四次SERIOUS monthly observations都在首次可用季度M6/M30执行cleanup（先Health再cleanup合法且仍同季度）；M28/M29时E0且未出现Energy menu，不能责怪没提交不存在的cleanup动作。Run01 M3已有可清理menu却先Network/report/Health，直到M6才cleanup；M18当季清理。Run02不呈现系统性更晚serious response。Repeated monthly warnings同属M28–30一个episode，4 vs2观察数不是6个独立危机实验。

MILD观察到下一cleanup的描述性延迟：Run01范围0–23、中位1.5月；Run02范围0–14、中位7月（20/17个monthly observations）。这是“下一cleanup距离”，**不是clearance耗时或正确阈值**。两个序列都有positive HR间隔、Story repair、不同quarter资源和曝光，Run01M25→48的23月也不意味着一直处于同一未解危机。较长mild-to-cleanup间距值得记录，却不足以要求每个mild cost自动进入防御模式。

## Public mistakes / repair / repeated exposure

按四条件筛选PUBLICLY_AVOIDABLE_RISK_MISTAKE：明确material危险、合法有效更安全备选、选项明显扩大风险、无需hidden值。两局144 selected语义均筛查，risk相关上下文定向读全。**0 established**意味着没找到无歧义满足全部条件的case，不是证明策略无错。

共享的闭门纪要hint是RISK_ACCEPTING / plausible public-risk concern，公开follow-up证实泄露排查；但唯一非透露选项同时说“公司整体稳定”，在尚未官宣调整背景下有truthfulness/有效回应问题。不能捏造菜单没有的“只拒绝讨论而不保证稳定”来宣称已证合法安全替代。Run02另一次public-only饭局属于plausible重复disclosure concern，动作明确只公开信息，不能判为明知泄密。

有界repair witness：Run01六次（confession、流程复盘、AI公开说明、revert/pin、事件clarify、release checklist；5 REPAIR、1 PARTIAL_REPAIR）；Run02九次（两次confession、真实压测报告、主动客户延期披露、依赖升级后修复合作、security clarify、两次陪同道歉与后续复盘帮助；9 REPAIR）。只是列举的witness count，不是全游戏repair rate。

Run02严重M28–30段继续选择共同复盘压测、realistic容量报告、第一时间客户告知，而不是造假/瞒报/违规上线；有aggregate setback仍不能反判这些当前动作unsafe。没有确认serious warning后反复同类可避免material exposure。Run02M18新饭局继承早先hint调查的历史，属于R5 PARTIAL，尚不支持general rule把public-only沟通一律禁掉。

## Clearance discipline

Run01 M3 raw89明确以confession后Dignity升满/无新warning认为trust已resolved，尽管自己承认没有explicit resolved信号；raw105继承该判断以discount cleanup。计1个独立FALSE_CLEARANCE episode＋1carryover，不计两次独立事件。

Run02 M24 raw773明确“HR positive now, so risk seems resolved”，前序M18排查与M22–23warning无明确closure，计1个unsupported FALSE_CLEARANCE episode。M31/M33是“seems/likely managed”更弱估计，不直接等同“全部危险已解除”。M39/M45/M46/M48还反复以positiveHR推断low/okay risk（held transcript pointers在JSON）；这些未验证乐观推断不是actual latent state，也不全部升级成独立FALSE_CLEARANCE。更改Risk Budget为AVAILABLE与宣布旧trust事件clear，必须分开。

两局均有shared reasoning weakness，没有建立“Run02反复specific-danger清除错误、Run01没有”的对照，更没证明该误判主导6点差。Run02M31 reasoning还误称previous Main为低调避险，实际raw1013为关键项目（S10-15已审）；不能据误述制造repair事实。即使未来研究clearance纪律，也须把closureUNKNOWN和当前budget/普通growth permission分开，避免永久TIGHT。

## Intensive separation

| M / raw | Health | Dignity | Latest HR | TIGHT / serious | Specific risk link |
| --- | --- | --- | --- | --- | --- |
| 3 / 105 | 7→6 | 10→9 | NONE | Not established / No | NO_PUBLIC_SPECIFIC_RISK_LINK |
| 15 / 501 | 10→9 | 10→9 | NONE | Not established / No | NO_PUBLIC_SPECIFIC_RISK_LINK |
| 21 / 701 | 9→8 | 10→9 | MILD | Not established / No | NO_PUBLIC_SPECIFIC_RISK_LINK |
| 27 / 901 | 9→8 | 10→9 | MILD | Not established / No | NO_PUBLIC_SPECIFIC_RISK_LINK |
| 33 / 1093 | 8→7 | 10→9 | NONE | Not established / No | NO_PUBLIC_SPECIFIC_RISK_LINK |
| 39 / 1293 | 9→8 | 10→9 | NONE | Not established / No | NO_PUBLIC_SPECIFIC_RISK_LINK |
| 48 / 1593 | 9→8 | 10→9 | NONE | Not established / No | NO_PUBLIC_SPECIFIC_RISK_LINK |

七次每次public Health−1、Dignity−1；菜单公开说明会付Health/Dignity并累积潜在风险，故不能宣称完全无risk语义。它是generic advertised warning，不是某次trust/compliance事件或−6component的直接public causal link。M21/M27与MILD当前HR重叠，其余当前HRpositive；7次没有SERIOUS当前HR，没有确认explicitTIGHT下仍提交intensive。M33/M48有fresh sameLevel report flat例外（S10-15）；M3/M21/M27/M39另有efficiency adherence问题，不能换名当成已证risk-control损失来源。

## v6 supporting principles / counterexample

只增加v6这一支持运行，不扩全历史。Accepted public transition dataset SHA `b5cc5c2c71fbc2ee39d09a3676325a139352f976f9452b71430abf2c8005d4cd`；raw source SHA核对后，仅终局public observe1660的name/weighted component投影，risk_control10、total75.29。Principles witness：请求policy书面确认并按建议限用公司设备（raw301/309）；拒收离职业务数据365/内部资料1069；原创进度延误透明汇报769；数据异常应急响应/通知与监管配合1517；有情境的cleanup229/1533。普通成长仍可接受，不抽取exact answer sequence。

**关键反证**：v6 M6 raw205选同样public-only饭局路线，public后续同样“猎头联系程磊、Leader排查信息源”，raw213主动承认，然后cleanup229，最终risk_control10。不同state/history/后续风险处置仍存在，所以它既不是证明public-only总安全，也不能让Run02raw581单案支持一个新规则。复杂安全事件在v6也会出现，即使repair合理，不能从终局10反推此前全无risk。

## Hypotheses and decision

| Hypothesis | Verdict | Boundary |
|---|---|---|
| R1 DIFFERENT_CHOICE_DRIVEN | PARTIAL | 1disclosure contrast可疑，另1posting contrastRun02更保守；v6反例，未解释6点 |
| R2 PATH_DEPENDENT_WARNING_LOAD | SUPPORTED | 公开timeline/同选结果/聚合incident有路径差异；不是因果占比 |
| R3 CLEANUP_TIMING | UNSUPPORTED | Run02serious都首可用季度cleanup；Run01M3反而延后；mild较长不等于应防御 |
| R4 FALSE_CLEARANCE | PARTIAL | 两局各1explicit unsupported episode；Run02更多low-risk推断不等同特定danger全clear |
| R5 REPEATED_EXPOSURE | PARTIAL | 同类gossipconcern但public-only语义有歧义；serious段当前行为偏repair |
| R6 COMPONENT_VARIANCE_NO_SAFE_POLICY | SUPPORTED | 现有public association不能识别一个可靠growth-preserving单点patch |

唯一decision **PATH_DEPENDENT_NO_SAFE_PATCH**。它表示当前公开证据更支持谨慎保留策略、由Main判断下一实验，**不是测得真实随机方差、证明path造成全部6分，或证明未来不存在修复**。A缺多个明确unsafe且安全有效备选的functional witness；B缺serious repair系统延迟；C缺Run02主导且可区分的clearance gap。虽然有多个小concern，现有明确行为缺口未达到安全patch标准，因此选D而非把未证concern包装成MIXED_RISK_GAP。

不提出V6E_RISK_PATCH_PROPOSAL；不移/删/改规则，不新增Skill、counter、架构或event答案。下一步权限由Main单独决定。

## Verification / retention

身份、24held文件hash/bytes、published component points、144/96/91/5计数、5异选/16同选/11cleanup/48月warning/6serious-delay边界、v6hash与公开component、frozen diff、JSON parse、secret scan及git diff-check在交付前核验。仅报告/compact evidence/CURRENT_STATE变更；commit/push/remote SHA与clean在TASK_RESULT确认。No install/service/provider/game/newCandidate；原FORENSIC_HOLD继续ACTIVE，Main/Stage才可解除。

No hidden-risk formula/reconstruction；no causal score attribution；no stable75 proof；no hidden-test transfer；no event-answer table。

**RETURN_FOR_RISK_CONTROL_DECISION**

**NEXT_GAME=NOT_AUTHORIZED**
