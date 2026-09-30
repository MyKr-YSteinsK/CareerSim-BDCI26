# S09-04｜资源轨迹与可干预窗口专项取证

## 1. Evidence Identity

- Task=`REPOSITORY_WRITE / OFFLINE_FORENSICS_ONLY`；base=`main@aa3844c85c982e42a859a18cfc60820df32600a0`，读取时 HEAD=origin/main，初始 clean。
- Candidate=`candidate-v7x-fresh-binding-reauthorization`，parent=v7w；本任务只取证/设计，不实施候选。S09=ACTIVE。
- 两局均 Tier A：先读 canonical 登记，再核验 exact events/transcript bytes+SHA256。transcript 只校验身份；本次不提取其私有推理，Agent 意图/趋势表示仅引用已有公开 forensic report。events 只投影 participant-visible state/event/menu 与执行标记枚举。
- raw 根：`.career_sim_runner/career_emu/outputs/local-s06-adaptive-controller/`。下表 stamp 下文件名分别 `events-<stamp>.jsonl` / `transcript-<stamp>.log`。

| Source / session / canonical report | stamp / scope | events bytes / SHA256 | transcript bytes / SHA256 |
|---|---|---|---|
| v7x / `700f8ed814844694869d93461e7ef748` / [v7x-run1-validation](../runs/v7x-run1-validation.md) | `20260930T131104Z`；2026-09-30 13:11:04–13:14:16.638819 UTC（Asia/Shanghai +08） | 376682 / `8e757e1f207c54c10c7ce9281bf8169c086b916e3ebac8784784775ec557be4a` | 79869 / `333d4b1d05c11b75670f956aef964894c63697bbfa46d76519ea9596d0b69d52` |
| v4 / `fdcaa70a85f44662a6a329513c175676` / [v4-run1-health-forensic](../runs/v4-run1-health-forensic.md) | `20260924T160806Z`；仅 hash-bound exact run file；不读更宽日志 | 263552 / `9bf8bed1d02435047df40300ff306231dfa938b91cb87d3ef5b082e35d7359e5` | 44237 / `fe20250c032c67d5681b6a7dd726114182b97bc180ee94768f95f99fae99d896` |

**Firewall:** 不访问 DB、effect table、event-ID lookup、private choice metadata、internal score/risk numeric/counters、Dev answer、HPL、shared runtime/provider logs。JSON 的字段白名单在 synthetic tests 核验；未选项只解释公开语义，不赋予收益数值。摘要中的 historical quantitative score 仅引正式报告作背景，不进入排序分析。

**复现:** `D:\CS\CareerSim\.venv\Scripts\python.exe -m scripts.s09_04_resource_trajectory_forensics`。复用 S09-02 parser/dedup/attribution，输出 `.local/scratch/s09-04/resource_trajectory.json`：130914 bytes，SHA256=`c152f7de094b38e98cf2941063af32aeeda2ce1bf625daacae70d6e705cc9a69`。完整公开 context、合法 label/description、pre/post 状态与来源 seq 均在该可重建 JSON；策略判断只在本报告。

**共同 schema:** 月份用结构化 time，不用故事里的“半年后”。CLEAN=单个成功 action→fresh observe、同月/同级且未识别自动边界的 stream pair，仍不是隔离的因果效应；MIXED 包括跨月、晋升、Energy refill/Review 类自动结算或批次。终局两局都 MIXED。趋势为公开 H 差分：正=RECOVERING，零=STABLE，负且此前自最近正/未知差分以来已出现另一负变化=REPEATED_ATTRITION，否则 DECLINING。这个统计没有“近期”长度、不是 runtime FRAGILE/binding gate。I0–I5 按 Plan；I1 首先表示明确恢复菜单，其机会成本另记；I3/I4 在纯减曝机会中表达成本。reasonableness 为有界审阅判断，questionable 表示值得权衡，不表示已证错误。

## 2. v7x Resource Timeline

29 success / 30 observe；21 CLEAN、8 MIXED、0 UNKNOWN pair；MODE=A27/S2，Risk=PASS29。RECOVERY 枚举未写入动作标签时记 UNKNOWN（不补成 NONE）；完整内部 Planning 意图未由本次 parser 重建。

忽略平段的公开 H 变化：`5→4→2→3→2→1→3→5→6→5→4→2→0`。M3 两次明确恢复合计观察到 +4；M4 香水减曝后又 +1；不存在“恢复到5后立即一路下跌”的单调轨迹。

### 决策与公开菜单

| # | M | event/context | actual choice | other legal choices |
|---|---|---|---|---|
| 1 | 1 | 新员工手册；开局规则 | 继续 | 无其它项 |
| 2 | 1 | 年会被起哄上台表演长链；临时上台表演 | 大方接下，挑个简单不出错的形式（讲个段子/带大家做个互动），把气氛炒起来 | 笑着婉拒，但主动提议替代方案（帮忙张罗游戏/给表演的同事捧场） / 黑着脸硬拒「我不会这些」，场面一度冷掉 |
| 3 | 1 | 同事深夜工作消息与领导点赞；23点群聊问API，领导赞即时回复 | 立刻回复显示专业 | 次日上班再回，并说明作息边界 / 私聊 Leader 建议重要事项用邮件 / 也学唐颖深夜发消息 |
| 4 | 1 | 得知未公开调整好友问买房；保密重组文件与朋友买房 | 只说「公司整体稳定」，不透露内幕 | 暗示「近期可能有变动，建议谨慎」，不透露文件 / 私下告知调整方向，请她绝对保密 |
| 5 | 2 | 年会被起哄上台表演长链；主持人请继续主持，可能硬撑 | 见好就收，把舞台交还给主持人，回座位继续融入 | 趁热度想多表现，硬撑着主持，后面渐渐力不从心 |
| 6 | 2 | 合作同事会上甩锅；客户责任争议 | 冷静列举时间线与邮件记录，澄清责任归属 | 先承担部分责任稳住客户，会后再找小周对峙 / 当场反击，指出小周未按时提供联调环境 / 沉默，请 Leader 主持厘清 |
| 7 | 2 | 合作同事会上甩锅；本周联合改进计划 | 主动起草联合改进计划，抄送 Leader 并邀请小周共创 | 只写自己负责部分，明确边界 |
| 8 | 3 | 年会与大领导同桌的社交分寸长链；高管聚餐 | 自然地找个轻松又得体的话题（行业趣闻/对公司活动的真诚感受）开个头 | 逮住机会猛夸领导、刻意刷存在感 / 紧张到全程低头吃饭，一句话不敢说 |
| 9 | 3 | 暴雨下班仅有一伞与小赵；21点暴雨橙色预警，一把小伞 | 邀小赵共撑一把伞，步行到地铁站 | 把伞借给小赵，自己冒雨跑百米去打车 / 提议拼车，费用 AA / 说伞只够一个人，各自想办法 |
| 10 | 3 | 暴雨下班仅有一伞与小赵；肩膀湿、雨加大，热面或末班地铁 | 接受，顺便听他说说项目困境 | 婉拒，赶最后一班地铁回家 |
| 11 | 3 | 季度体力行动分配；Q-E；E3 | 健康恢复 | Q-E 除 actual 外全部项；公开描述见第5节 |
| 12 | 3 | 季度体力行动分配；Q-E；E2 | 健康恢复 | Q-E 除 actual 外全部项；公开描述见第5节 |
| 13 | 3 | 季度体力行动分配；Q-E；E1 | 准备汇报材料 | Q-E 除 actual 外全部项；公开描述见第5节 |
| 14 | 3 | 季度主行动选择；Q-M；E0 | 申请关键项目 | Q-M 除 actual 外全部项；公开描述见第5节 |
| 15 | 4 | 年会与大领导同桌的社交分寸长链；高管询问工作价值 | 用一两句话讲清自己做的事和价值，点到为止、不喧宾夺主 | 抓住机会长篇大论汇报工作、还顺带提了诉求 |
| 16 | 4 | 邻座香水味太冲；香水已引起头疼 | 委婉如实说自己对浓香味比较敏感，问能否喷淡一点 | 违心夸「好闻」，继续头疼着忍 / 转头跟别的同事吐槽她「熏死人」 |
| 17 | 4 | 跨组架构评审的参与与坚持决策；额外评审需3至4天，本组排期 | 接下评审邀请，深度通读并准备意见 | 谢绝评审，留出时间专注本组排期 |
| 18 | 5 | 跨组架构评审的参与与坚持决策；架构分歧、技术委员会风险评估 | 整理一份完整的风险评估文档，正式提交技术委员会 | 尊重对方组的判断，把意见以附录形式备案即可 |
| 19 | 5 | 过度热情打探隐私的新同事长链；新同事追问隐私 | 笑着岔开话题，用轻松的方式划清边界：「这些就不聊啦，说点别的」 | 板起脸直接说「这是我的私事，请不要打听」 / 碍于新同事面子，勉强一一回答 |
| 20 | 5 | 跨部门重大事故是否主动支援；外部P0需一周夜间值守，自己本周交付 | 在群里表示可远程答疑两小时，不现场驻场 | 主动请缨加入救火小组 / 沉默，专注自有项目 |
| 21 | 6 | 过度热情打探隐私的新同事长链；八卦后续 | 善意点拨她：新环境少打听人际八卦、多看事，对她自己也好 | 继续每次岔开，不点破，免得多事 |
| 22 | 6 | 无领导小群转发领导发言截图；截图泄漏与合规警告 | 劝删截图，群内只聊工作不聊人 | 参与吐槽几句 / 退群保平安 / 私聊老周反映团队情绪（不提出处） |
| 23 | 6 | 同事总迟交拖累你的进度；上游迟延导致自己熬夜 | 平和地和他对齐交接时间点，必要时拉上排期一起明确 | 默默熬夜兜底，啥也不说 / 直接在大群里点名他「老拖后腿」 |
| 24 | 6 | 季度体力行动分配；Q-E；E3；Output缺口 | 高强度工作 | Q-E 除 actual 外全部项；公开描述见第5节 |
| 25 | 6 | 季度体力行动分配；Q-E；E1 | 准备汇报材料 | Q-E 除 actual 外全部项；公开描述见第5节 |
| 26 | 6 | 季度主行动选择；Q-M；E0；C/no-promotion窗口 | 向领导汇报成果 | Q-M 除 actual 外全部项；公开描述见第5节 |
| 27 | 7 | 动了去意后公司挽留的抉择长链；公司涨薪/项目/晋升挽留 | 回到最初想走的根本原因上判断，挽留是否真能解决问题，再决定要不要安心留下 | 被涨薪打动，立刻打消念头留下 / 嘴上答应留下，私下却继续骑驴找马 |
| 28 | 7 | 观察升职靠关系而非能力；关系晋升、KTV/球局/接送孩子等额外投入 | 学习投入非正式场合，控制底线 | 拒绝迎合，加倍技术产出 / 向 HRBP 反映晋升标准模糊 / 跳槽准备，减少投入 |
| 29 | 7 | 观察升职靠关系而非能力；关系经营后仍升得慢；叙事半年后不改公开M7 | 继续经营关系 | 回归技术路线 |

### 同口径资源/执行/干预判读

| # | pre H/W | MODE / RECOVERY / Risk | post H (M) | delta class | trend | explicit preservation? | opportunity | reasonableness / 当时依据 | source O/A/O seq |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 5/1 | A / UNKNOWN / PASS | 5 (M1) | CLEAN | STABLE | NO | I0 | reasonable；开局说明，没有资源选择。 | 27/29/35 |
| 2 | 5/1 | A / UNKNOWN / PASS | 4 (M1) | CLEAN | DECLINING | UNCLEAR | I5 | reasonable；婉拒保留参与，但表演没有公开 Health 成本；不能因随后下降判错。 | 35/37/43 |
| 3 | 4/1 | A / UNKNOWN / PASS | 2 (M1) | CLEAN | REPEATED_ATTRITION | YES | I2 | questionable；23点非明确紧急问答；次日回复并说明作息边界可减少夜间工作，领导即时回应偏好仍是代价。 | 43/45/51 |
| 4 | 2/1 | A / UNKNOWN / PASS | 2 (M2) | MIXED | STABLE | NO | I0 | reasonable；保密与朋友决策冲突，替代不能证明保护 Health。 | 51/53/59 |
| 5 | 2/1 | A / UNKNOWN / PASS | 3 (M2) | CLEAN | RECOVERING | YES | I3 | reasonable；已获得表演认可，交回舞台避免继续硬撑且仍融入；已选择。 | 59/61/67 |
| 6 | 3/1 | A / UNKNOWN / PASS | 3 (M2) | CLEAN | STABLE | NO | I0 | reasonable；客户责任澄清；没有明确恢复/减曝语义。 | 67/69/75 |
| 7 | 3/1 | A / UNKNOWN / PASS | 3 (M3) | MIXED | STABLE | YES | I4 | reasonable；只写负责部分缩小新增工作范围，但客户要求本周联合改进；选择共创有明确交付依据。 | 75/77/83 |
| 8 | 3/1 | A / UNKNOWN / PASS | 3 (M3) | CLEAN | STABLE | NO | I0 | reasonable；得体社交；安静进食不能直接推成 Health 保护。 | 83/85/91 |
| 9 | 3/1 | A / UNKNOWN / PASS | 2 (M3) | CLEAN | DECLINING | YES | I2 | questionable；暴雨橙色预警、一把小伞；拼车减少雨中暴露，但 W1 下费用可承受性 UNKNOWN，不判为低成本。 | 91/93/99 |
| 10 | 2/1 | A / UNKNOWN / PASS | 1 (M3) | CLEAN | REPEATED_ATTRITION | UNCLEAR | I5 | reasonable；回家结束外出，热面也有保暖/进食语义；哪个保护身体更多 UNKNOWN。 | 99/101/107 |
| 11 | 1/2 | S / UNKNOWN / PASS | 3 (M3) | CLEAN | RECOVERING | YES | I1 | reasonable；H1 后明确健康恢复；观察到回升，S 的 binding 语义沿用正式审查 AMBIGUOUS。 | 107/109/115 |
| 12 | 3/2 | S / UNKNOWN / PASS | 5 (M3) | CLEAN | RECOVERING | YES | I1 | unknown；再次恢复可见有效；H3 是否仍有 material binding 证据不足，不以回升证明重授权正确。 | 115/117/123 |
| 13 | 5/2 | A / UNKNOWN / PASS | 5 (M3) | CLEAN | STABLE | YES | I1 | reasonable；尚有1点 Energy 的恢复选项，选择汇报准备；不要求补满 Health。 | 123/125/131 |
| 14 | 5/2 | A / UNKNOWN / PASS | 5 (M4) | MIXED | STABLE | YES | I1 | reasonable；低调避险明确恢复，但占用唯一 Main 的成长机会；关键项目有多维公开价值。 | 131/133/139 |
| 15 | 5/2 | A / UNKNOWN / PASS | 5 (M4) | CLEAN | STABLE | NO | I0 | reasonable；简短价值汇报不是已证身体恢复，不给所有克制选择加保护标签。 | 139/141/147 |
| 16 | 5/2 | A / UNKNOWN / PASS | 6 (M4) | CLEAN | RECOVERING | YES | I3 | reasonable；浓香已导致头疼；请求喷淡直接减少当前暴露，不放弃关键交付；已选择。 | 147/149/155 |
| 17 | 6/2 | A / UNKNOWN / PASS | 5 (M5) | MIXED | DECLINING | YES | I4 | reasonable；谢绝可保本组排期；接受有跨组影响机会且需3至4天评审，明确高机会成本。 | 155/157/163 |
| 18 | 5/3 | A / UNKNOWN / PASS | 5 (M5) | CLEAN | STABLE | UNCLEAR | I5 | reasonable；附录备案更轻量，但技术争议/风险责任价值不同，没有明确身体成本。 | 163/165/171 |
| 19 | 5/3 | A / UNKNOWN / PASS | 5 (M5) | CLEAN | STABLE | NO | I0 | reasonable；隐私边界，不等同 Health 保护。 | 171/173/179 |
| 20 | 5/3 | A / UNKNOWN / PASS | 5 (M6) | MIXED | STABLE | YES | I3 | reasonable；对比一周夜间驻场，远程两小时保留帮助且保护本周自身交付；已选择。 | 179/181/187 |
| 21 | 5/3 | A / PROGRESSION / PASS | 5 (M6) | CLEAN | STABLE | NO | I0 | reasonable；关系点拨；RECOVERY 仅按公开动作标签读取。 | 187/189/195 |
| 22 | 5/3 | A / UNKNOWN / PASS | 5 (M6) | CLEAN | STABLE | NO | I0 | reasonable；合规劝删；不以安全措辞泛化成身体恢复。 | 195/197/203 |
| 23 | 5/3 | A / UNKNOWN / PASS | 5 (M6) | MIXED | STABLE | YES | I3 | reasonable；已知上游延迟迫使熬夜；对齐交接排期减少兜底且推进交付；已选择。 | 203/205/211 |
| 24 | 5/3 | A / UNKNOWN / PASS | 4 (M6) | CLEAN | REPEATED_ATTRITION | YES | I1 | questionable；恢复仍合法；高强度工作公开承认 Health 成本，Output 缺口也真实，不能断言该成长选择不合理。 | 211/213/219 |
| 25 | 4/3 | A / UNKNOWN / PASS | 4 (M6) | CLEAN | STABLE | YES | I1 | questionable；剩余1点可恢复；汇报有公开成长价值，其后 Output 未变只是事后观察，不能提前判定无价值。 | 219/221/227 |
| 26 | 4/3 | A / UNKNOWN / PASS | 4 (M7) | MIXED | STABLE | YES | I1 | reasonable；最后明确恢复菜单为低调避险；唯一 Main 机会与弱 Review 后推进成长相冲突。 | 227/229/235 |
| 27 | 4/3 | A / RISK / PASS | 4 (M7) | CLEAN | STABLE | NO | I0 | reasonable；挽留是否解决原问题，收入/职业连续性权衡，不是明确 Health 恢复。 | 235/237/243 |
| 28 | 4/3 | A / UNKNOWN / PASS | 2 (M7) | CLEAN | REPEATED_ATTRITION | YES | I4 | questionable；跳槽准备、减少投入明确减少当前组织投入，代价是迁移工作/连续性与晋升；净身体暴露 UNKNOWN，非低成本救援。 | 243/245/251 |
| 29 | 2/3 | A / UNKNOWN / PASS | 0 (M8) | MIXED | REPEATED_ATTRITION | NO | I0 | unknown；继续关系与回归技术均无明确恢复/减少工作语义；技术路线不等于休息，NO_PROVEN_INTERVENTION_OPTION。 | 251/253/259 |

## 3. v4 Comparable Timeline

23 success / 24 observe；15 CLEAN、8 MIXED、0 UNKNOWN pair。模式/恢复/Risk formal 枚举未记录，全部 UNKNOWN，不能默认为 A/PASS。同一 seq 的 duplicate transport 仅计一次；本报告 O seq 指已解码 tool_result 的承载位置，旧报告 O25/O33 等是同回执另一 transport 位置（本口径 O27/O35）；动作 seq 一致，不是两次 observe。

H 变化：`5→3→2→4→3→4→3→2→1→0`。M3 明确恢复 +2，M5 折中午餐后 +1；终局 L2，沿用 S09-02 公开 raw 校正，不从旧分数来源推定 Level。

### 决策与公开菜单

| # | M | event/context | actual choice | other legal choices |
|---|---|---|---|---|
| 1 | 1 | 新员工手册；开局规则 | 继续 | 无其它项 |
| 2 | 1 | 出差名额唯一与小乔评价长链；唯一出差名额评价 | 在肯定小乔的同时，简要补充自己近期的相关成果 | 客观肯定小乔的长处，表示她很适合 / 委婉表示两人各有优势，建议 Leader 按业务相关性决定 / 侧面提及小乔近期项目上的不足 |
| 3 | 1 | Code Review 评论语气选择；新人MR设计问题与心理安全 | 用提问引导他自己意识到问题 | 直接指出问题并标注必须修改 / Approve 并私下 IM 说明 |
| 4 | 1 | 聚餐第二场KTV与晋升决策者；已有头疼，HRBP邀第二场KTV | 参加第二场，控制饮酒积极表现 | 礼貌拒绝，明天早会照常高质量 / 只去坐半小时露脸再撤 |
| 5 | 2 | 聚餐第二场KTV与晋升决策者；凌晨一点谈项目/晋升 | 表达兴趣并请教晋升准备 | 只聊项目不谈晋升，避免功利 |
| 6 | 2 | 出差名额唯一与小乔评价长链；出差后感谢与关系冷淡 | 分享中公开感谢小乔的前期铺垫，并私下找她聊一次 | 分享只突出个人收获，专注巩固 Leader 印象 |
| 7 | 2 | 同事长时间霸占打印机；打印急件被占 | 礼貌说明自己有份急件，问能否插打两页 | 直接走过去把他的任务取消，先打自己的 / 默默干等，眼看着会议要迟到 |
| 8 | 3 | 竞标方案答辩PK对手长链；竞标技术/TCO与价格 | 扬长避短：用技术深度和长期总成本（TCO）讲清「贵得值」 | 临时大幅压价跟对手拼低价，方案随便讲讲 / 在答辩里暗踩对手「他们技术不行、做过砸过」 |
| 9 | 3 | 离职同事私下托付工作资料；竞对离职者托保密材料 | 拒绝接收，建议他走合规交接 | 接收但不打开，离职后删除 / 接收并上报信息安全部 |
| 10 | 3 | 未参与项目被挂名申部门奖；没参与项目被挂名 | 建议改为以灵犀支付项目申报，你担任主笔 | 提出异议，拒绝挂名 / 默许签字，当作 Leader 人情 |
| 11 | 3 | 季度体力行动分配；Q-E；E3 | 健康恢复 | Q-E 除 actual 外全部项；公开描述见第5节 |
| 12 | 3 | 季度体力行动分配；Q-E；E2 | 人脉维护 | Q-E 除 actual 外全部项；公开描述见第5节 |
| 13 | 3 | 季度体力行动分配；Q-E；E1 | 准备汇报材料 | Q-E 除 actual 外全部项；公开描述见第5节 |
| 14 | 3 | 季度主行动选择；Q-M；E0 | 申请关键项目 | Q-M 除 actual 外全部项；公开描述见第5节 |
| 15 | 4 | 竞标方案答辩PK对手长链；采购仍追问报价 | 给出分阶段付款+可量化的ROI模型，把价值落到采购能复述的话术上 | 只强调技术，对报价问题避而不答 |
| 16 | 4 | 办公室绿植轮值忘记浇水；忘浇公共绿植 | 当天补救并设日历提醒 | 道歉并请同事代一次 / 觉得小事无所谓 |
| 17 | 4 | 午饭跟同事吃还是回家吃；回家午睡/下午精力 vs 团队情报网 | 改为每周至少三天和同事一起吃 | 坚持回家，用下午高效产出证明 / 折中：周二周四跟同事吃，其余回家 |
| 18 | 5 | 午饭跟同事吃还是回家吃；核心项目讨论，需要调整饭局节奏 | 改回折中节奏，把关键信息在饭局搞清即可 | 维持每天和同事吃午饭 |
| 19 | 5 | 带病坚持上班的同事长链；同事重感冒、已有多人打喷嚏、项目节点紧 | 私下关心她，劝她回去休息，并主动提出帮她顶一部分紧急任务 | 找领导反映「带病上班影响大家健康」，建议安排她居家办公 / 嫌她吵又怕被传染，自己戴口罩躲远点，不吭声 |
| 20 | 5 | 健康检查返回错误状态；故障实例健康检查端点修复；不是人体健康 | 立即修 endpoint 并检查其他服务 | 只修当前服务 / 等 on-call 处理 |
| 21 | 6 | 带病坚持上班的同事长链；顶岗后本人排满、节点近、吃力 | 向领导同步「临时帮阿芳顶岗」，争取合理的排期支持 | 默默全扛，不声张，自己加班补上 |
| 22 | 6 | 组会上被贬低为「只是工程活」；工程价值被贬低 | 会上沉默承受，会后单独找 Leader 沟通 | 当场用数据和业务影响礼貌质疑这番定性 / 会上不接话，会后私下鼓舞同组同事、澄清贡献 |
| 23 | 6 | 组会上被贬低为「只是工程活」；争取组级OKR可见度或不再替组发声 | 推动把你的改造写进组级 OKR 或季度亮点 | 只守好自己的一亩三分地，不再替组里发声 |

### 同口径资源/执行/干预判读

| # | pre H/W | MODE / RECOVERY / Risk | post H (M) | delta class | trend | explicit preservation? | opportunity | reasonableness / 当时依据 | source O/A/O seq |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 5/1 | UNKNOWN / UNKNOWN / UNKNOWN | 5 (M1) | CLEAN | STABLE | NO | I0 | reasonable；开局无资源选择。 | 27/29/35 |
| 2 | 5/1 | UNKNOWN / UNKNOWN / UNKNOWN | 5 (M1) | CLEAN | STABLE | NO | I0 | reasonable；出差评价与成长/公平，没有明确身体成本。 | 35/37/43 |
| 3 | 5/1 | UNKNOWN / UNKNOWN / UNKNOWN | 5 (M1) | MIXED | STABLE | NO | I0 | reasonable；代码审查语气与质量；替代没有恢复语义。 | 43/45/51 |
| 4 | 5/1 | UNKNOWN / UNKNOWN / UNKNOWN | 3 (M2) | MIXED | DECLINING | YES | I2 | questionable；当前已有头疼；礼貌拒绝或半小时露脸退出明确减少第二场暴露；HRBP 机会成本存在。 | 51/53/59 |
| 5 | 3/1 | UNKNOWN / UNKNOWN / UNKNOWN | 3 (M2) | MIXED | STABLE | NO | I0 | reasonable；凌晨谈项目两种话题范围，均无明确回家/恢复选项。 | 59/61/67 |
| 6 | 3/1 | UNKNOWN / UNKNOWN / UNKNOWN | 3 (M2) | CLEAN | STABLE | NO | I0 | reasonable；分享及关系修复，没有明确身体保护。 | 67/69/75 |
| 7 | 3/1 | UNKNOWN / UNKNOWN / UNKNOWN | 3 (M3) | MIXED | STABLE | NO | I0 | reasonable；打印急件保护任务时效，不能证明 Health 效果。 | 75/77/83 |
| 8 | 3/1 | UNKNOWN / UNKNOWN / UNKNOWN | 2 (M3) | CLEAN | REPEATED_ATTRITION | NO | I0 | reasonable；技术/TCO 与报价/贬低竞争者；未公开身体成本，不能以 H-1 判排序失败。 | 83/85/91 |
| 9 | 2/1 | UNKNOWN / UNKNOWN / UNKNOWN | 2 (M3) | CLEAN | STABLE | NO | I0 | reasonable；合规交接保护数据；不是 Health 机会。 | 91/93/99 |
| 10 | 2/1 | UNKNOWN / UNKNOWN / UNKNOWN | 2 (M3) | CLEAN | STABLE | NO | I0 | reasonable；拒绝虚假署名、真实申报；不能猜未选效应。 | 99/101/107 |
| 11 | 2/1 | UNKNOWN / UNKNOWN / UNKNOWN | 4 (M3) | CLEAN | RECOVERING | YES | I1 | reasonable；H2 后选择明确健康恢复，H2→4。 | 107/109/115 |
| 12 | 4/1 | UNKNOWN / UNKNOWN / UNKNOWN | 4 (M3) | CLEAN | STABLE | YES | I1 | reasonable；剩余 Energy 可再次恢复，但 Network 同样有成长价值。 | 115/117/123 |
| 13 | 4/1 | UNKNOWN / UNKNOWN / UNKNOWN | 4 (M3) | CLEAN | STABLE | YES | I1 | reasonable；最后 Energy 恢复机会；选择汇报，不要求每季或补满。 | 123/125/131 |
| 14 | 4/1 | UNKNOWN / UNKNOWN / UNKNOWN | 4 (M4) | MIXED | STABLE | YES | I1 | reasonable；低调避险明确恢复但放弃 Main 关键项目多维成长。 | 131/133/139 |
| 15 | 4/1 | UNKNOWN / UNKNOWN / UNKNOWN | 4 (M4) | CLEAN | STABLE | NO | I0 | reasonable；采购 ROI 回答没有明确身体保护。 | 139/141/147 |
| 16 | 4/1 | UNKNOWN / UNKNOWN / UNKNOWN | 4 (M4) | CLEAN | STABLE | UNCLEAR | I5 | reasonable；请代浇水少一件事，但无已知严重负担/时长；不能把任何少做事当 Health 保护。 | 147/149/155 |
| 17 | 4/1 | UNKNOWN / UNKNOWN / UNKNOWN | 3 (M5) | MIXED | DECLINING | YES | I2 | questionable；回家午睡20分钟、下午精力稳定公开可见；折中保留团队信息，成本仍需衡量。 | 155/157/163 |
| 18 | 3/2 | UNKNOWN / UNKNOWN / UNKNOWN | 4 (M5) | CLEAN | RECOVERING | YES | I3 | reasonable；折中节奏保留关键饭局信息及休息机会；已选择，不把 H+1 解释成固定选项效果。 | 163/165/171 |
| 19 | 4/2 | UNKNOWN / UNKNOWN / UNKNOWN | 3 (M5) | CLEAN | DECLINING | YES | I2 | questionable；公开传染风险；建议居家办公减少共享区暴露，戴口罩避开也有明确防护，但各有政治/交付成本。 | 171/173/179 |
| 20 | 3/2 | UNKNOWN / UNKNOWN / UNKNOWN | 2 (M6) | MIXED | REPEATED_ATTRITION | UNCLEAR | I5 | reasonable；只修当前服务缩小任务，但未证明额外检查的身体成本且故障检查有交付价值。 | 179/181/187 |
| 21 | 2/2 | UNKNOWN / UNKNOWN / UNKNOWN | 2 (M6) | CLEAN | STABLE | YES | I3 | reasonable；本人满排期/吃力，争取合理排期对比自己加班补上；已选择并有 S/N/O 增益。 | 187/189/195 |
| 22 | 2/2 | UNKNOWN / UNKNOWN / UNKNOWN | 1 (M6) | CLEAN | REPEATED_ATTRITION | NO | I0 | unknown；当场、私聊、私下鼓舞没有明确休息/身体暴露语义。 | 195/197/203 |
| 23 | 1/2 | UNKNOWN / UNKNOWN / UNKNOWN | 0 (M6) | MIXED | REPEATED_ATTRITION | UNCLEAR | I5 | unknown；不再替组发声限制倡议范围，但没有当前 Health/工时减曝依据；不推定少发声可救，NO_PROVEN_INTERVENTION_OPTION。 | 203/205/211 |

## 4. Intervention Windows

| Window | v7x | v4 |
|---|---|---|
| First proven reduction | #3 M1 H4，23点回复→次日上班/作息边界 I2；领导回应偏好有代价 | #4 M1 H5且已有头疼，第二场→拒绝或半小时露脸 I2；有 HRBP 机会成本 |
| Best evidenced actionable menus (不等于最优反事实) | #11–12 M3 H1→3→5，实际两次恢复；#23 M6排期对齐为已选低成本减曝；#24–26 M6恢复可用但存在 Output/Main 成长代价 | #11 M3 H2→4实际恢复；#18 M5折中饭局已选；#19 M5感染警告/WFH为未选明确减曝，交付/政治成本未知；#21 M6排期支持已选 |
| Last explicit Health recovery | **#26 M6 Main，H4/W3/E0；低调避险明确恢复**。最后 Energy 恢复为 #25 M6 E1 | **#14 M3 Main，H4/W1/E0；低调避险明确恢复**。最后 Energy 恢复为 #13 M3 E1 |
| LAST_REALISTIC_INTERVENTION_WINDOW（含明确减曝） | **#28 M7 H4/W3/E0；“跳槽准备，减少投入” I4**：明确减少当前组织投入，但转换工作、收入连续性及净身体消耗 UNKNOWN；仅为高 tradeoff 的公开减负机会，不是可证明的救命选项 | **#21 M6 H2/W2/E0；“争取合理的排期支持” I3，已经选择**，相对“自己加班补上”明确减负；观察 H2→2，不等于恢复完成 |
| Terminal-near final choice | #29 M7 H2→M8 H0，关系/技术两项，无休息或当前减曝依据：**NO_PROVEN_INTERVENTION_OPTION** | #22 H2→1和#23 H1→0，私聊/团队发声方案没有明确身体恢复或当前工时减曝；#23 I5：**NO_PROVEN_INTERVENTION_OPTION** |

**边界裁定:** v7x #28 的“减少投入”是明确 effort reduction，达到 I4；不把 HRBP 反馈或“加倍技术产出”推成更健康。v4 #23 的“不再替组发声”仅是倡议/代表范围变化，菜单未承诺减少既有满排期或当前工作量，故 I5；不从未选效应补证。两者净 Health、收入和存活效应均 UNKNOWN。若 Stage 采用更严格的“只计明示 physical/workload exposure”标准，v7x #28 可降 I5，则最后**稳健、无此语义争议**的机会退至 #26 M6 Main；设计建议不依赖 #28。

## 5. Recovery Opportunity Availability

### 重复菜单公开语义（Q-E / Q-M）

Q-E 当时所有合法项：高强度工作（大量精力换产出，明确健康/尊严代价并可能积累风险）；技能学习（专业能力、精力消耗）；人脉维护（人脉/尊严）；处理历史埋雷（清理既有隐患）；心理修复（尊严）；健康恢复（“休整作息、恢复体力，明显回补健康”）；准备汇报材料（可见成果、绩效资本/尊严）；保留体力（不行动，剩余不累计）。Q-M：申请关键项目（绩效/技能/人脉）；向领导汇报成果（可见度/认可）；主动争取资源（资源支持）；申请岗位轮岗（技能）；主动曝光成果（绩效/尊严）；建立导师关系（人脉/能力）；修复关键关系（人脉/尊严）；低调避险（“暂时收敛锋芒、规避风险，恢复健康并降低潜在风险”）；不行动（无状态更新）。这些描述只记录公开文字，不解析隐藏 risk 数值/status_updates。

| Opportunity count（每个 fresh decision/menu，非独立预算） | v7x | v4 |
|---|---|---|
| I1 explicit recovery states | 7：#11/12/13/14/24/25/26；实际选2 (#11/12) | 4：#11/12/13/14；实际选1 (#11) |
| 其中 Energy / Main | 5 / 2；Energy被两季预算关联，不能叫5次独立 recovery budget | 3 / 1；全部为一个季度预算 |
| I2 explicit exposure reduction | 2：#3/9；选0 | 3：#4/17/19；选0（#19给他人休息同时自己新增顶岗，不等同选择WFH/自我减曝） |
| I3 low-cost preservation | 4：#5/16/20/23；选4 | 2：#18/21；选2 |
| I4 high-tradeoff preservation | 3：#7/17/28；选0 | 0；#4/17代价未知，不能判低成本，仍I2 |
| I5 ambiguous / I0 none | 3 / 10 | 3 / 11 |
| 总 proven I1–I4 states / actually selected relevant semantics | **16 / 6**（7+2+4+3 / 2+4） | **9 / 3**（4+3+2 / 1+2） |

I2/I3/I4 与 I1 互斥计数；某菜单可有多种保护语义，仅按主分类计一次。I1 未选不等于 missed low-cost opportunity。没有把“通用更少做事”“更礼貌”“技术路线”全部算 Health preservation。

**FACT:** v7x 到 M6 仍有健康恢复菜单，不支持 H4 前提“几乎再无恢复机会”；#24 高强度工作公开承认身体代价，观察 H5→4、E3→1、O1→3（CLEAN）。#25汇报材料观察 H4→4、O3→3、D9→10；#26Main观察H4→4、O3→3但跨月。后两项未见O增长不能反推 Agent 当时已知 NO_GAIN/cap。v4 在#23之后观察到E0→3同时terminal，**从未到达可选择的M6 Energy菜单**；不能把终局E3冒充最后可恢复机会。

**INFERENCE:** v7x 的问题包含成长/资源机会成本排序，非菜单缺失；v4 的直接恢复 cadence 确有空档，但Story减曝机会仍存在。两局最末决策都缺已证即时修复语义，单靠“危险时多休息”不完整。已选低成本保护多次存在，说明缺口不是全面不读身体/工作负担。

## 6. Resource Trajectory Interpretation

| Question / factor | Evidence and bounded conclusion |
|---|---|
| First severe episode / recovery | v7x M3 H1，#11首次明确恢复+2、#12再+2；v4 M3 H2，#11明确恢复+2。低位为本局描述，**不是阈值或独立 binding 证明**。v7x earlier #5 H2→3也改善，保留在完整轨迹。 |
| Time/actions to renewed loss | v7x #12恢复至5后，#13–16四次非负（#16到6），**第5个后续action #17**跨M4→5到5；到terminal尚17actions。v4 #11到4后#12–16五次平段，**第6个后续action #17**跨M4→5到3；到terminal12actions。间隔为描述，禁止变成固定hold计时。 |
| Acute recovery too little? | 实际恢复局部有效，最终仍失败；所需更大缓冲、再恢复的存活收益、是否“足够”均 UNKNOWN。v7x恢复+4仍终止、v4仅+2仍终止不能推出固定恢复剂量。 |
| Renewed exposure too fast? | v7x回升后4次非负、还有香水减曝；v4五次平段。没有支持“下一动作即过早退出S”。后来确有额外评审/高强度工作/非正式活动或感染/顶岗的公开暴露；成本与累计消耗大小未隔离。 |
| Repeated attrition | FACT 两局都再次出现连续/累计下降，终局分别4→2→0、4→3→2→1→0，且包含 mixed transitions；不把每次下降全归Story choice。 |
| Persistence of representation / danger recognition | v7x动作标签A27/S2、#21 PROGRESSION、#27 RISK；formal report支持M3考虑H、M7薄buffer并计划未来恢复；没有本任务证明的持续Health trend/FRAGILE记录。v4既有forensic report记H2/H1危险识别、#21避免硬扛，却只确认初始Board，无持续结构化trend；记忆/attention是否致死 UNKNOWN。Risk枚举v4 UNKNOWN，v7x PASS不能代证无危险。 |
| Opportunity scarcity / cadence | v7x M6再次Energy+Main可恢复，非纯scarcity；M7没有明确立即恢复。v4 M3之后直到terminal无Energy/Main恢复，cadence空档成立；Story#18/#21保护已选。提前缓冲可能有用是HYPOTHESIS，不是强制每季回血。 |
| Story ranking / automatic effects | v7x#28H4→2 CLEAN但净身体损失仍非隔离因果；#29H2→0跨月MIXED。v4#19/#22损失CLEAN而#20晋升/月变/#23refill terminalMIXED；修endpoint的“健康”不能当身体语义。故事数量/环境随机与hidden settlement混杂，策略导致全部损失 NOT_PROVEN。 |
| Evidence gaps | 未选项净效果、随机分布、隐含promotion/Health/死亡阈值、未来menu、内部完整ranking、错误路径可避免性 UNKNOWN；不扩大raw/cohort或live查询补证。 |

### Analysis-only resource state

- NORMAL：v7x开局尚无近期下降证据；不能因H5直接称安全。v4开局亦无下降，但KTV前**当前头疼**已需审阅。
- RECOVERING：v7x#11/12、v4#11；也保留#5/16与v4#18的公开改善，不将所有回升等同急性治疗。
- FRAGILE_CANDIDATE：v7x#3之后的累积下降、#9/10雨中活动后低位、#28之后再现损失；v4#8后、#19/20后持续下降及当前感染/满排期，是可审阅的定性组合。M3恢复后不自动永久贴FRAGILE；v7x M4回升/非负序列是反对持续hold的材料。时效与因果不足支持持久runtime状态。
- BINDING：v7x两个S的material basis仍AMBIGUOUS；v4H1危险是已有report记述意图而非新public症状。没有因为数字低就重新判定binding。

**H1 POST_RECOVERY_FRAGILITY:** 两局恢复后再次消耗支持风险可能存在，未证明恢复本身产生脆弱性或固定保护期。
**H2 LOW_OPPORTUNITY_COST_PRESERVATION:** 菜单/已选行为支持机会存在；净存活/分数收益待实验。
**H3 MODE_IS_TOO_COARSE:** A可以承载排序修正，不能从两局推出第三状态必要；显式FRAGILE runtime state暂不建议。
**H4 EARLIER_BUFFER_PRESERVATION:** v7x M6仍可恢复，原scarcity前提不成立；v4直接恢复稀疏成立，早缓冲价值仍待证。

## 7. Survivor Contrast

仅复用 [S09-02联合取证](S09-02_FAILURE_FLOOR_HIGH_SCORE_JOINT_FORENSICS.md) 与v4既有对照，不重新挖 survivor raw。

- FACT：v1#1 M6/M12 public Health7、M24为8；v6 M6为6/M12为5；v7o M6为6/M12为7；v7v M6为6/M18为8。它们没有每个时点最大化Health的证据；已有Energy mix在多个窗口没有Health行动，不能推出高分需要持续补满。
- FACT：v6可见clean -2（Mentor6→4、接待10→8、团建7→5），v7o可见clean -2（周末项目10→8、非正式关系活动7→5及10→8）。存活者也承担成本。S09-02 10局 negative H N143，observed clean max2、P90=1/P95=2；observed max ≠ simulator max ≠ hidden Test max。绝不设“buffer大于2”规则。
- FACT：v1#1 M3 H4选一次恢复与N/O，M6 H3选两次恢复与O，到H7。与v4的更早/更大缓冲差异可描述；v7x双恢复仍死，故这不是充分条件。v1#2最终H10仍因trust/continuity失败，Health不是全部failure floor。
- INFERENCE：存活者某些shock前缓冲更厚且兼顾广泛成长，有时更早恢复；**更少暴露、随机差异、某一政策的独立贡献 UNKNOWN**。没有匹配事件/菜单反事实，不排序“buffer vs randomness”的因果权重，不宣称稳定提升或Skill收益。

## 8. Mechanism Comparison

表中“failure prevented”均为待验证目标，不是已观察反事实。

| Mechanism | Failure targeted (prevention UNKNOWN) | Score regression risk | Evidence | Confidence | Recommend? |
|---|---|---|---|---|---|
| M1 FRAGILE_A_MODE，新增RESOURCE_STATE | 保存恢复后脆弱轨迹 | 持久标签、状态维护/attention dilution，易泛化保守 | 轨迹可描述，但状态reset/必要性未证 | 低 | 否；显式状态不是最小delta |
| M2 SOFT_RESOURCE_TIE_BREAK，全candidate范围 | 近似等值路径保留optionalities | 低；但保护触发可能过窄，terminal菜单不可救 | 低成本项已多次被选；未选项成长等值一般未知 | 中低 | 第二顺位，暂不独立扩到所有Energy/Main |
| M3 POST_RECOVERY_HOLD | 防刚恢复又投入已知身体成本 | stale-memory/pseudo-timer；把历史恢复变永久约束 | 两局首个恢复后分别4/5次非负且v7x再回升 | 低 | 否；无固定月/次数hold |
| M4 QUARTERLY_BUFFER_OPPORTUNITY | 在稀疏菜单前保缓冲 | 消耗有限成长Energy，侵蚀Output/Portfolio | v7x M6#24–26可用；v4 M3后无直接恢复；净收益未证 | 中低 | 暂不做唯一delta；不能证明多恢复就是更优 |
| **M5 STORY_EXPOSURE_GUARD（仅A-mode软排序）** | 当前明确身体/安全/加班暴露下忽略低成本减曝 | 低至中；误判低成本会损关键社交/交付 | v4 KTV头疼/WFH、v7x雨/深夜；既有选择#20/#23/#21证明成长与bounded exposure可并存 | **语义/可实现性中，净收益低** | **唯一下一静态设计建议；不保证修复晚期无菜单情况** |

## 9. Minimal Next Candidate Hypothesis

`MINIMAL_BEHAVIOR_DELTA_RECOMMENDATION = M5_STORY_EXPOSURE_GUARD_AS_BOUNDED_A_MODE_RANKING_PRIOR`

`READY_FOR_STATIC_IMPLEMENTATION` 仅说明可写成一个小、可证伪的Planning语义规则；本任务未实施，需Stage决定独立static task，再另行授权game。不存在已证存活收益。

| Design field | Single mechanism |
|---|---|
| mechanism | Story候选排序时，把当下明确physical/safety/workload exposure与低机会成本的合法减曝语义纳入比较；保持MODE=A，不增加RESOURCE_STATE/Board字段。这里“相近价值/低成本”是M5启用条件，不叠加一个全局M2规则。 |
| trigger evidence | 最新observe确认当前暴露（如感染、暴雨、夜间工作、满排期），并且本session fresh轨迹仍有未被新证据消解的累计下降或恢复后当前暴露；必须指出具体public context/choice wording。单个普通数字下降、过去S/过去恢复、历史shock幅度不够触发。没有现时暴露或低成本证据则不偏置。 |
| what it changes | 先检验较低暴露choice能否保持当前binding delivery、明确成长/Portfolio目的与收入连续性；若无明显关键机会牺牲，在成长价值相近的候选中优先保optionalities。费用/连续性/成长代价未知则写UNKNOWN，不把它自动当cheap或强制否决原选。 |
| what it does NOT change | Promotion Portfolio、broad responsive growth、conditional Primary Gap、no-promotion→A/PROGRESSION、genuine high-value progression；既有fresh binding才S、NO_GAIN、Delivery/Risk/Board/runtime shell/Skills数量/architecture/Runner/retry全部冻结。Energy/Main无新增恢复配额，Risk不得二次重规划。 |
| exit/reset | 每次fresh observe重做当下菜单排序；一次choice结束即无持续授权。当前暴露解除/新菜单无明确减曝/低成本不成立/最新轨迹反证持续脆弱时恢复原排序。promotion后按既有合同重建窗口；不按固定month/action计时、不继承历史FRAGILE。 |
| regression risk | 拒绝合作/社交导致Network或delivery变差；把所有普通疲劳当binding；低成本误判；新规则注意力成本。v7x#7/#17/#28高tradeoff、#10/#18语义模糊都是负例，不能自动选择保守；#29技术路线不准强贴Health。 |
| falsification criterion | static负例若变成Health阈值/每季quota/长期S/未选效果lookup即拒绝设计；未来单独授权run若当前明确暴露+低成本机会仍被忽略，adherence不支持；若规则反复牺牲关键成长/交付而无现时暴露则设计过宽。完整adherence却仍死于无可证菜单或mixed随机损失，不能当收益证明；不能借一局失败扩大hold/固定血线。 |

**拒绝的政策:** `Health low=>S`、`Health<X=>recover`、每季度一次Health、总选最安全Story、保持Health高于历史max shock、S直到补满。不给隐含Test安全线，不借中间语义增加新Skill/持久状态。

## 10. Final Decision / Verification / Hold

`S09_04_RESOURCE_TRAJECTORY_FORENSICS_COMPLETE_DESIGN_READY`

**Supported:** 两局可比cumulative attrition；一次急性恢复并非充分保护；明确恢复菜单与减曝菜单可以计数；v7x M6机会仍在、v4恢复cadence空档；末次choice缺公开即时保护；保持A但在当前明确暴露下比较低成本减曝，是有界、可静态表达的下一实验假设。
**Unknown:** 哪次未选可保证生还、恢复剂量、各loss独立原因、持久FRAGILE必要性、分数净收益、所有随机/隐藏路径泛化。回到Stage作下一决策，S09不宣布完成。

### Verification evidence

- exact events+transcript identity：两局PASS；v7x全record时间窗+每个解码observe session核验；v4 hash-bound whole run+observe session核验。没有跨局混合。
- 根`.venv` pytest：`tests/test_s09_04_resource_trajectory_forensics.py`（9）+S09-02 regression（14）=**23 passed**；覆盖public-only exclusions、菜单/来源位置、transport dedup、missing post/legacy UNKNOWN、mixed batch/跨月、bool choice排除、hash/bytes/session/time mismatch停止。
- deterministic二次提取：上述130914 bytes/SHA一致；JSON parse PASS。
- 手工public spot checks：v7x#11 O107/A109/O115 H1→3，#12 O115/A117/O123 H3→5；#28 O243/A245/O251 H4→2，#29 O251/A253/O259 H2→0/M8（MIXED）。v4#11 O107/A109/O115 H2→4；#23 O203/A205/O211 H1→0、E0→3（MIXED）。均只检查白名单state/context/menu与回执，不输出private raw。
- canonical secret scanner覆盖交付script/test/review/CURRENT_STATE/RUN_HISTORY及派生public JSON；PASS。未归档raw/transcript/private reasoning；`git diff --check` PASS；候选/Skills/manifest/runtime/retry/dependency路径无diff。最终commit/push/clean身份见TASK_RESULT，避免自引用commit哈希。
- Tooling limitation：初次读取误把JSON的`actions`计数当列表，仅返回23，已改`decision_rows`；一次旧extractor文件名假设失败，用`rg --files`定位；一次独立spot-check误用snapshot字段`state`，按真实schema改为`status`后通过。均为无副作用Tooling Error，不影响数据或runtime身份。

### Permissions / evidence lifecycle

`provider=0; service=0; MCP=0; game=0; Candidate mutation=0; HPL_COORDINATION_IMPACT=NONE; NEXT_GAME=NOT_AUTHORIZED`。

两局exact raw原路径保持，FORENSIC_HOLD状态未变；责任接受/释放仍归Stage/Main，hash/报告完成不替代raw或自动release。v7x终局provider/gameplay flags不改变，旧Candidate validation不转移。新增派生JSON在gitignored scratch，可依exact held raw重建；报告是canonical去敏结论，不提交shared DB、配置或其它session。

Execution metrics：recorded analysis-start=2026-09-30 22:11:53 Asia/Shanghai（UTC14:11:53）；本时间为加载期已记录点，完整turn开始UNKNOWN。Finished/wall见TASK_RESULT；Model/Effort/本任务tokens/费用UNKNOWN，不记0；测试1次，deterministic extractor2次，独立live操作0。
