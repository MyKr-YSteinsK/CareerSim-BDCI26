# S09-16｜三样本完整轨迹取证

## 范围、身份与结论

`IN_FLIGHT_EVIDENCE`；branch=`codex/s09-14-v9a-static`；base=`6a753c6962f25aa4cf1a9c2349ebbbd272027820`。只分析既有 RUN07/v8a、RUN08/v8a、RUN10/v9a；v10a 未运行，旧局证据不继承给 v10a。Live/provider/service/game/DB/install=0；Candidate、四 Skills、manifest、依赖、Runner 不改。

- **FACT**：三局均完成48月，分数72.65 / 59.00 / 68.40；RUN07/RUN10 同在 M6/M12/M24/M42 晋升，最终L5；RUN08 M12/M18/M36 晋升，最终L4。
- **DESCRIPTIVE ASSOCIATION**：RUN10 比 RUN07 低4.25，与较低终局 Skill/Network/Wealth、Health及 Dev 风险控制记账共同出现；不是“晋升慢”。RUN10 比 RUN08 高9.40，主要关联更早晋升及更强 Skill 增长。
- **PLAUSIBLE CONTRIBUTOR**：RUN10 的 Output gap 刷法、较少 Main 语义分化、部分过量保护可能压低资本转化；同选择不同响应也大量存在，不能全归因于可控错误。
- **UNKNOWN**：每种策略贡献多少分、未选动作的真实收益、v10a是否优于v8a、隐藏计分机制。

唯一主要可控缺口：`UNSUPPORTED_SATURATION_DEVALUATION_OF_DURABLE_CAPITAL`。次要：`REPEATED_LOCAL_OUTPUT_STAGNATION`。只建议强化 v10 C6 的**不发明饱和/封顶**语义；本任务没有 patch。

## Evidence / measurement

[compact evidence](S09-16_FULL_HORIZON_EVIDENCE.json) 包含全部126次 Energy、48次 Main、24个首次/末次 checkpoint、保护序列、精确匹配矩阵、公开 action上下文、来源行号、bytes/hash/window。`aN` 是该局去重后的 action序号；`lines` 是 exact events 的 before/action/after 行号。Transcript 行号另标。

| Run | Exact output stem | Events SHA256 | Actions / observes | UTC window 2026-10-01 |
|---|---|---|---|---|
| RUN07 | 20261001T114001Z | 977f19aa89dbc12d4c1482ceff440ca98d28946737632e9c547b7d04dedb095d | 203 / 204 | 11:39:58.3107402–12:51:10.411189 |
| RUN08 | 20261001T132230Z | 32cab0dbf9a5f10741ebff29db0fba5aa743e177b6211319d024fb05368229d0 | 205 / 206 | 13:22:27.041969–13:54:42.775557 |
| RUN10 | 20261001T161805Z | 10fe7d3bc50f115a1bca02abed1afab2c63b605bc04a807a93a7f780b7710702 | 201 / 202 | 16:17:59.610375–16:41:13.594450 |

全部609次 action有 success receipt，且回执先于下一 fresh observe；各局全部事件记录在明确窗口内，观察session唯一并与 score report一致。三个 events SHA 均与 run note一致。Transcript与score bytes/hash见JSON：RUN07 note 的 transcript SHA 末位误写为 `d`，实际为 `a`，与当时 post_run_summary 的完整SHA一致；RUN07 transcript本身无 session marker，故不声称其独立session身份已证明。路径、bytes、既有hash及events序列支持该局归属；RUN08/10 transcript有同session marker。RUN10 score report 的 ending_score为空，终局数值及合法加权 Dev component取自该局 terminal observe，非其它局/DB。

所有来源在 `.career_sim_runner/career_emu/outputs/local-s06-adaptive-controller/<stem>/`；receipt在 `.local/runtime/s09-run07-v8a/`、`s09-run08-v8a/`、`s09-run10-v9a/`。保留现有 FORENSIC_HOLD，Stage/Main接受及依赖解除前不清理；没有复制/归档 raw。派生 extractor在 `.local/scratch/s09-16/{extract,analyze,enrich}.py`，代码SHA及当前 `scripts/post_run_audit.py` SHA记录于JSON；是在既有两局helper上作三局/全周期对齐，不修改canonical auditor。不推断历史实际执行 auditor 的 physical bytes身份。

Clean response须同月、同Level、after无新feed、公开 advertised正增益维度数值可比较；跨月/Level/feed响应只能描述。Cleanup没有公开 S/N/O/H增益广告，记 `UNKNOWN`，不从私有字段评效。历史同Level GAIN仅为替代候选，不保证当前context仍GAIN；Health已满或无保护需求不能凭旧GAIN赢排序。匹配严格使用完整公开description与完整公开 legal-choice projection（含choice/action/description/cost/白名单advertised），无title/event ID、无文本模糊匹配；私有status字段从输入及结论排除。重复输入按出现次序一对一zip，不做笛卡尔乘积。

## A｜PROMOTION_CONTROLLED_GAP_MAP

下表状态顺序 **S/N/O/W/H/D；Level**。首次正式Review是含半年绩效奖金的fresh feed；月末是该月最后一次observe。季度 Energy/Main往往在Review之后，两个时点不混用。终局显示M49，survival仍48。

| M | RUN07 首Review → 月末 | RUN08 首Review → 月末 | RUN10 首Review → 月末 | grade 07/08/10；promotion |
|---|---|---|---|---|
| 6 | 9/3/3/2/3/10; L2 → 12/5/6/2/5/10; L2 | 9/3/2/3/5/10; L1 → 8/3/3/3/6/9; L1 | 9/3/3/2/3/10; L2 → 11/7/6/1/5/10; L2 | C/C/C；Y/N/Y |
| 12 | 21/4/6/3/7/9; L3 → 22/3/5/1/10/10; L3 | 9/3/3/3/8/10; L2 → 13/4/6/3/7/10; L2 | 21/4/5/2/5/9; L3 → 23/7/7/2/7/10; L3 | B/C/B；Y/Y/Y |
| 18 | 41/11/15/5/9/10; L3 → 42/12/16/5/10/10; L3 | 21/4/6/5/9/9; L3 → 24/5/8/5/8/10; L3 | 38/19/12/5/6/10; L3 → 40/21/14/5/7/9; L3 | B/B/B；N/Y/N |
| 24 | 42/19/15/9/10/10; L4 → 45/21/19/9/9/10; L4 | 41/21/8/8/9/10; L3 → 42/20/9/8/10/10; L3 | 42/19/16/8/9/10; L4 → 43/24/18/8/8/10; L4 | B/B/B；Y/N/Y |
| 30 | 59/26/26/14/10/10; L4 → 64/27/26/14/9/10; L4 | 42/21/13/12/8/10; L3 → 42/20/13/12/9/10; L3 | 62/35/20/13/9/10; L4 → 65/36/23/13/8/10; L4 | B/B/B；N/N/N |
| 36 | 81/36/25/19/7/10; L4 → 85/35/25/19/9/10; L4 | 42/19/15/15/7/10; L4 → 45/21/17/15/10/10; L4 | 84/36/24/18/2/10; L4 → 84/36/26/18/6/10; L4 | B/B/B；N/Y/N |
| 42 | 100/34/24/24/9/10; L5 → 102/43/26/25/9/10; L5 | 59/33/26/23/10/10; L4 → 62/36/26/23/10/10; L4 | 93/34/24/27/10/10; L5 → 96/36/29/27/9/10; L5 | A/A/A；Y/N/Y |
| 48 | 117/53/32/34/10/10; L5 → 118/54/33/34/10/10; L5 | 77/36/26/27/10/10; L4 → 81/36/26/28/8/10; L4 | 111/48/38/31/7/10; L5 → 115/51/38/31/7/10; L5 | B/A/B；N/N/N |
| Terminal | 119/54/35/35/10/10; L5 | 82/36/26/29/8/10; L4 | 115/51/38/32/8/10; L5 | final A/C/B；L5/L4/L5 |

| 差异 | Evidence / classification |
|---|---|
| 晋升节奏 | Supported / FACT：07=10，不能解释4.25分差；三局横比仍有职级差异 |
| 终局资本 | Supported / FACT：07相对10 S+4、N+3、W+3、O−3；Output更多不保证分数更高 |
| 增长斜率 | Supported / DESCRIPTIVE ASSOCIATION：10 M36→42 Skill+9，07+19；10 M42→48 Wealth+4，07+10；10 M24→30 Network+16优于07+7，不能声称全程转化更差 |
| Main/响应路由 | Plausible contributor：07 M33 Mentor、M39 Rotation对比10继续Apply；10跨季度 preparation无增益；替代路径反事实收益UNKNOWN |
| 保护 | Plausible contributor：S 21对9，额外序列多数有真实威胁；M27/M48二次保护效益未由新warning证明 |
| 同输入响应 | Supported / FACT：85对Story，80同选择，28对clean同选择S/N/O响应不同；并非policy随机实验 |
| Ownership兑现 | Unknown：10也有明确CI与新方向兑现，不能证明07完整链更多 |

合法 Dev 终局**加权**记账如下，不记录隐藏原始counter、不进runtime策略。07−10为Level0、Wealth0.75、Resilience1.50、Skill0.50、Risk control1.00、Network0.50，显示值合计4.25；单局component显示总和与最终score存在0.01舍入差，不重算评分公式。

| Weighted Dev component | RUN07 | RUN08 | RUN10 |
|---|---:|---:|---:|
| Level | 15.00 | 12.00 | 15.00 |
| Wealth | 8.78 | 7.25 | 8.03 |
| Resilience | 15.00 | 13.50 | 13.50 |
| Skill | 14.88 | 10.25 | 14.38 |
| Risk control | 10.00 | 10.00 | 9.00 |
| Network | 9.00 | 6.00 | 8.50 |

这是终局差额的 **FACT bookkeeping**，不是上述动作导致这些分差的因果分解；也不证明hidden Test沿用该计分。

## B｜CAPITAL_GROWTH_WINDOW_TABLE

Δ是两个**首次正式Review**间累计变化，不是每月斜率；initial→M6从初始M1观察计。S次数也按相同events边界计，包含起点Review后、排除终点Review后动作；与“全Review月份S次数”不同。Level恒定须窗口内所有observe同Level。

| Run | Review window | ΔS/ΔN/ΔO/ΔW | Level | 恒定? | grade / promo | S actions |
|---|---|---|---|---|---|---:|
| RUN07 | 0→6 | 8/2/3/1 | L1→L2 | N | C / Y | 6 |
| RUN07 | 6→12 | 12/1/3/1 | L2→L3 | N | B / Y | 2 |
| RUN07 | 12→18 | 20/7/9/2 | L3→L3 | Y | B / N | 1 |
| RUN07 | 18→24 | 1/8/0/4 | L3→L4 | N | B / Y | 0 |
| RUN07 | 24→30 | 17/7/11/5 | L4→L4 | Y | B / N | 0 |
| RUN07 | 30→36 | 22/10/-1/5 | L4→L4 | Y | B / N | 0 |
| RUN07 | 36→42 | 19/-2/-1/5 | L4→L5 | N | A / Y | 0 |
| RUN07 | 42→48 | 17/19/8/10 | L5→L5 | Y | B / N | 0 |
| RUN08 | 0→6 | 8/2/2/2 | L1→L1 | Y | C / N | 0 |
| RUN08 | 6→12 | 0/0/1/0 | L1→L2 | N | C / Y | 0 |
| RUN08 | 12→18 | 12/1/3/2 | L2→L3 | N | B / Y | 1 |
| RUN08 | 18→24 | 20/17/2/3 | L3→L3 | Y | B / N | 0 |
| RUN08 | 24→30 | 1/0/5/4 | L3→L3 | Y | B / N | 1 |
| RUN08 | 30→36 | 0/-2/2/3 | L3→L4 | N | B / Y | 2 |
| RUN08 | 36→42 | 17/14/11/8 | L4→L4 | Y | A / N | 0 |
| RUN08 | 42→48 | 18/3/0/4 | L4→L4 | Y | A / N | 0 |
| RUN10 | 0→6 | 8/2/3/1 | L1→L2 | N | C / Y | 0 |
| RUN10 | 6→12 | 12/1/2/0 | L2→L3 | N | B / Y | 4 |
| RUN10 | 12→18 | 17/15/7/3 | L3→L3 | Y | B / N | 1 |
| RUN10 | 18→24 | 4/0/4/3 | L3→L4 | N | B / Y | 0 |
| RUN10 | 24→30 | 20/16/4/5 | L4→L4 | Y | B / N | 3 |
| RUN10 | 30→36 | 22/1/4/5 | L4→L4 | Y | B / N | 0 |
| RUN10 | 36→42 | 9/-2/0/9 | L4→L5 | N | A / Y | 7 |
| RUN10 | 42→48 | 18/14/14/4 | L5→L5 | Y | B / N | 0 |

**DESCRIPTIVE ASSOCIATION**：RUN08 M6→12 S/N均0，M24→36 Skill合计+1；M36后才恢复。RUN07 M24→36 S+39、N+17、W+10；RUN10 S+42、N+17、W+10，同Level这段并不劣于07。M36→48 RUN07 S+36/N+17/W+15，RUN10 S+27/N+12/W+13；后者O+14，前者O+7。全cohort判 `mixed`：07↔10是 `post-promotion capital conversion material`，08比较则早期promotion与资本/响应均有差异，不给精确份额。

## C｜ENERGY_RESPONSE_MATRIX

全部126个before/advertised/after响应及合法替代menu引用在JSON。下表为family内 GAIN / NO_GAIN / MIXED_OR_UNKNOWN **action数**；Cleanup没有公开目标维度，UNKNOWN，不记无效。其它115次均为clean，可归因的广告目标响应；普通H/D代价另见原始public before/after。

| Family | RUN07 G/NG/MU | RUN08 G/NG/MU | RUN10 G/NG/MU |
|---|---|---|---|
| Skill | 1/0/0 | 1/0/0 | 0/0/0 |
| Network | 3/4/0 | 6/2/0 | 3/1/0 |
| Preparation | 17/3/0 | 16/5/0 | 10/5/0 |
| Health | 9/0/0 | 11/0/0 | 13/0/0 |
| Cleanup | 0/0/5 | 0/0/2 | 0/0/4 |
| Intensity | 0/0/0 | 0/1/0 | 3/1/0 |

### STAGNATION_FARMING_CASES / RESPONSIVE_SWITCH_CASES

| Run / actions | Public response and bounded interpretation |
|---|---|
| 07 a26 M6 prep→a37/38 M9 prep | O NO_GAIN后同L2两次GAIN；跨context复测可以有价值，不能把一次失败当永久cap |
| 07 a76 M18 prep→a87 cleanup/a88 Network | 切换Network仍NO_GAIN，转换family不保证GAIN；M24升L4后prep a99–101均GAIN |
| 07 a125 M30 prepNG→a126 cleanup | 避开立即重复；M33转Health/Network，后者NG；M39 a162 Skill+1、a164Rotation Skill+2，存在资本替代实际收益 |
| 08 a24 prepNG→a25 intensityNG | 虽换family，仍追同一Output，支付H/D普通成本而无O增益；不是有效responsive switch |
| 08 a165 M39 prepNG→a166 NetworkGAIN | 一个明确成功switch；但a177/178 M42又连续prepNG，已知Network仍有响应，a179 NetworkGAIN |
| 08 a178NG→a191 M45 prepGAIN | 同L4不同context下响应恢复，避免将“不要刷停滞”写成永久禁止复测 |
| 10 a38 M9 prepNG | 最后一能量已耗尽，无即时替代机会；M12升L3后a49 prepGAIN，合理reset |
| 10 a88 M21 prepNG | 最后一能量耗尽；M24升L4后a99 intensityGAIN/a100 prepGAIN，不能判连续farm |
| 10 a135 M33 intensityNG | O26→26，H7→6、D10→9；随后a136 HealthGAIN。增长替代反事实UNKNOWN，但普通成本确已支付 |
| 10 a149 M36 prepNG→a160 M39 prepNG | 同L4、O26仍未增长；是跨季度停滞重复信号，11个中间游戏动作≠同context连续提交。M39首步E3可比较未测Skill路径；可证明候选存在，不能证明probe五条件完整满足 |
| 10 a160NG→a161 HealthGAIN→a162 NetworkNG | 实际修改原计划第二次prep为Network，部分route-away；N36→36，未成功利用增长响应 |
| 10 a162NG→M42 a173–175 prepGAIN | 晋升L5后连续O增长；新Level复测有实际回报，不证明隐藏解封机制 |
| 10 a186 M45 prepNG→a187 HealthGAIN/a188 NetworkGAIN | 成功route-away；末季选择受新HR警告约束，不能凭NG要求增长一定优先 |

立即下一Energy同family NG→NG：08 a177→178；10 a149→160（跨季度）；07无。当前Level最近同family NG后的再次NG：08 a165→177、177→178；10 a149→160。后者不能仅凭两点定义永久dimension NO_GAIN，context变化要保留。

`RESPONSIVE_PATH > STALLED_PATH = supported with exceptions`。这是已知高价值响应路径优先的行为原则，非试验所得score uplift；Health响应不自动高价值、可兑现交付保留其它价值、新context/Level可复测。10从未选择Skill Energy，07/08各一次，未测试不等于更好；07也能以Story维持高Skill，不能固定Skill配额。

## D｜MAIN_ACTION_SEMANTIC_TABLE

全部48次 Main 的 month/Level/choice、CTRL gap claim、DL claim、fresh后状态/feed与checkpoint时间在JSON。以下每格为实际family；A=Apply，R=Report，M=Mentor，T=Rotation，V=Avoid。

| Main month | 07 | 08 | 10 |
|---|---|---|---|
| 3 | A / L1 / a14 | A / L1 / a14 | A / L1 / a13 |
| 6 | A / L2 / a27 | A / L1 / a26 | A / L2 / a26 |
| 9 | R / L2 / a40 | A / L1 / a39 | A / L2 / a39 |
| 12 | A / L3 / a52 | A / L2 / a52 | R / L3 / a52 |
| 15 | A / L3 / a65 | A / L2 / a65 | A / L3 / a65 |
| 18 | A / L3 / a77 | A / L3 / a77 | A / L3 / a77 |
| 21 | A / L3 / a89 | A / L3 / a90 | A / L3 / a89 |
| 24 | A / L4 / a102 | A / L3 / a103 | A / L4 / a101 |
| 27 | A / L4 / a115 | A / L3 / a116 | V / L4 / a113 |
| 30 | A / L4 / a127 | A / L3 / a128 | A / L4 / a125 |
| 33 | M / L4 / a140 | A / L3 / a141 | A / L4 / a137 |
| 36 | V / L4 / a152 | A / L4 / a154 | A / L4 / a150 |
| 39 | T / L4 / a164 | A / L4 / a167 | A / L4 / a163 |
| 42 | A / L5 / a177 | A / L4 / a180 | A / L5 / a176 |
| 45 | A / L5 / a190 | A / L4 / a193 | A / L5 / a189 |
| 48 | A / L5 / a203 | A / L4 / a205 | V / L5 / a201 |

- **FACT**：07 A12/R1/M1/T1/V1，08 A16，10 A13/R1/V2。Apply次数与score不单调：12→72.65，13→68.40，16→59.00。Apply public menu提供ownership和多维广告，实际收益受当前响应约束；反复“+4最强/直击Output gap”不等于兑现或每次都实现+4。
- **FACT**：07 Report a40/M9前有CI公开上线及团队提速（a31）；10 Report a52/M12前有客户demo恢复与认可（a46），虽note只写gap，也不能说没有真实成果。两次都有可恢复basis。07之后M12晋升；10该月**先晋升后Report**，之后M18未晋升。Report不是晋升原因实验。
- **FACT**：07 Mentor a140/M33得到Skill+1，Network未增；Rotation a164/M39 Skill+2。10同期继续Apply。资本实际收益支持比较family，但未恢复由这两次Main打开新事件集的可靠链。
- **UNKNOWN**：Main Apply的12/16/13个项目各自active identity、完成/验收及Recognition。07反复沿用D4 DELIVERED、08 D1 IN_PROGRESS、10 NONE都是self-report；0个auditor合法header不等于0 commitments。三局Main的数值回执不能当career result验证。
- 正式Review月份的Main都在该Review**之后**；不能将M6/M12等Main当作刚刚发生的Review preparation。DL NEAR另有commitment语义，不能与formal月份混同。当前 gap claim与真正Leader feedback分别保存在Main/checkpoints JSON中。

`APPLY_STRONG_PRIOR_CONFIDENCE=Medium`；`REPORT_RESULT_CONVERSION_CONFIDENCE=Low`（依据存在，两次不足以验证因果收益）；`MENTOR_ROTATION_OPTION_VALUE_CONFIDENCE=Low`（Skill收益已见，机会集扩张未证）。v10语义比较合理，固定Main答案无依据。

## E｜REALIZATION_CHAIN_EVIDENCE

以下是人工恢复的bounded examples，**不是完整game episode总数**；JSON给出链动作及证据。Visibility包括公开讨论/负面反馈，不都等于正向recognition。

| Run | Ownership→公开result | Result→公开visibility | 无可恢复basis的季度Report | 重复Apply未恢复逐项目兑现 |
|---|---:|---:|---:|---:|
| 07 | 3 | 3 | 0/1 | 12 UNKNOWN |
| 08 | 1 | 2 | NOT_EXERCISED | 16 UNKNOWN |
| 10 | 3 | 3 | 0/1 | 13 UNKNOWN |

- 07：a8技术选型→a15如期上线/业务满意，但新漏洞待修；a30搭CI→a31团队提速→a40Report尝试，后续特定认可未恢复；a56→59已有milestone公开汇报/高管追问；a181→184 AI合规→上线效果好但CEO批评时效。
- 08：a8→15 milestone汇报与高管追问，响应为零仍不等于没有工作；a108→111 AI合规→公开上线效果/CEO批评。a2→5自研ownership后是延期，不能写作成功兑现。
- 10：a44→46备用demo完成核心流程/客户肯定→a52Report；a53→57 milestone与高管讨论；a60→61 CI公开上线；a138→141新方向参与→实质贡献/“学得快又靠谱”认可→深入机会，是最完整的责任/result/recognition/next-opportunity链。后续M42 A/L5只可描述关联。

`REALIZATION_CHAIN_PATTERN=Insufficient`：不能从bounded样本断言07比10完整链更多，亦不能强排08→10→07“兑现效率”。Public result及numeric durable response是不同oracle；08弱资本响应不自动否定实际成果。C1/C9可保留为有公开依据的原则，整局逐project验证仍不足。

## F｜PROTECTION_EPISODE_TABLE

| Run | A / S | Max consecutive S | Episodes |
|---|---|---:|---|
| 07 | 194 / 9 | 6 | a7–12 M2–3 H1→5；a24–25 M6 H1→5；a47 M12心理危机专业干预 |
| 08 | 201 / 4 | 2 | a53 M13心理危机；a104 M25 VP转岗施压；a126–127 M30 HRwarning/Health7→9 |
| 10 | 180 / 21 | 6 | 7段，详见下表/JSON |

| RUN10 episode | Binding / proportionality / resolution / exit |
|---|---|
| M6 a23–24 | H1，健康两次1→3→5，a25 A；清楚public constraint，及时退出，无补满 |
| M9 a36–37 | H2，两次2→4→6，a38 A；清楚约束，无长S deadlock |
| M12 a48 | 颈椎疼/右手麻、如约理疗、交付后移半天；H5→7，a49 A；public症状优先，不因数值尚中等而否定 |
| M27 a111–113 | M25/M26已有重复“埋雷全要炸”HRwarning；cleanup→H6→8→Avoid H9；a114 A，随后HR转正。cleanup后空feed未证明解除，也未重新授权第二次cleanup；额外Avoid边际必要性UNKNOWN，存在二次降险投入的plausible成本 |
| M36 a144–149 | H2且Energy未到，先三Story守住现有项目/合规；a147–148 H2→4→6。a149已宣告“回安全底”却保留S，实际动作是增长prepNG；a150 A。一个标记滞后，不能把该增长动作另算保守浪费 |
| M40 a164 | 体检异常的明确medicalwarning；请假复查/交接H8→10，a165 A；M41 a167公开复查良性、重排节奏。数值H8不排除真实医疗约束 |
| M48 a196–201 | HR“自求多福”、review观察名单，保信任/本职的三个Story仍有S+4/N+3收益；a199cleanup→a200H5→7→a201Avoid H8。没有后续新warning重新证明第二次保护必要，终局HR仍轻微warning；没有可观察A退出，因为game终局，不能编造deadlock |

07心理干预公开后果是节点延期/观察名单，但另一同事硬撑住院，不能把生存保护写成错误。08 M30 H7→9“补生存底线”偏保守，仍同时存在HRwarning。10的21个S不是21个纯保护动作，Story及a149仍有增长/交付价值。

`PROTECTION_OPPORTUNITY_COST=SOME plausible`；M27/M48 duplicate protection以及Health边际投入值得比较，但反事实生存风险/替代收益UNKNOWN。C2已有最小必要保护规则；不建议另加数值安全线或按S配额强行退出。

## G｜WORLD_MODEL_ERROR_TABLE

人工复核notes与transcript keyword shortlist；重复输出不计为独立错误，Story引号中的“必炸”不算agent断言。公开handbook来自各局events行11/12：Health/Dignity 0–10，Skill/Network/Output 0–不限，Wealth可负；不得把后验归一化尺度当runtime cap。

| Case | Classification | Public context / decision relevance |
|---|---|---|
| 07 M33 a139/140；transcript7504/8280/8323 “确认L4 Output封顶26/唯一未封顶” | CONFIRMED_UNSUPPORTED_WORLD_MODEL_ASSERTION | 多次局部NG支持折价，不支持全局cap。改投Network/Mentor不一定错误；此分类是证据越界，非证明真实内部cap不存在 |
| 07 M39 a164 “Output/Network近顶/Skill唯一” | AMBIGUOUS_HEURISTIC | “近顶”可能描述边际响应，但“唯一”超出测试范围；保留实际Skill替代收益，不肯定隐藏机制 |
| 07 M42+ a175–177等 “L5解封” | AMBIGUOUS_HEURISTIC | Level后确有新GAIN；能支持reset/复测，不能确认隐藏解封公式 |
| 08 transcript563、notes82/121；10 notes11/12/49/50、transcript3811：H/D10已满 | PUBLICLY_SUPPORTED | handbook确有0–10上界，不与S/N/O无限范围混为一类 |
| 10 M36 a149/150 H6“安全底” | AMBIGUOUS_HEURISTIC | 此episode2→6后回A有依据；不能升级成任何局面都安全的阈值 |
| 10 M43 a179；transcript6704：Skill100“疑似封顶”、学习边际低 | CONFIRMED_UNSUPPORTED_WORLD_MODEL_ASSERTION | 同L5，a179之前S100，a180后S101，terminal S115，否定100饱和判断；note也称“Skill已100边际低”。周末提前交付有独立客户一天联调收益，不能由错误理由推断选择必错 |
| 10 M27/M48 “风险逼近临界/保护姿态” | AMBIGUOUS_HEURISTIC | 强HRwarning支持bounded保护；不支持私有阈值判断，空feed也不自动支持重复cleanup |

**FACT**：unsupported saturation reasoning跨07/10重复，且10直接影响对未测学习选项的折价；不是单纯词频报警。**RECOMMENDATION**：唯一delta是强化C6首屏salience：无 explicit public evidence，“capped/enough/no longer useful”须UNKNOWN；数值高或一次NG不能折价整个资本维度。保留local NG折价、真实Delivery与binding保护，避免反向机械学习。

## H｜THREE_RUN_MATCHED_DECISION_MATRIX

JSON包含全部pair与三局共输入的action refs/state/rationale/fresh response，不仅挑例。只匹配Story：Energy/Main菜单重复且固定，全覆盖见C/D，不拿它们充Story样本量。

| Pair | Exact occurrence pairs | Same choice | Clean same-choice different S/N/O | Exactly equal S/N/O/W/H/D/Level pairs | Equal-state different choice |
|---|---:|---:|---:|---:|---:|
| 07↔10 | 85 | 80 | 28 | 1 | 0 |
| 08↔10 | 77 | 69 | 23 | 1 | 0 |
| 07↔08 | 84 | 76 | 25 | 1 | 0 |

三局共同exact输入有50组出现次序匹配。输入相同≠历史相同；即使数值state相同，commitment及剩余context未必相同。全周期不能沿用S09-12 M1–18的16pairs分母；该审查严格方法/UNKNOWN纪律继续有效。

- 07 a30/M7与10 a60/M15，同CI实现选择，S均+3，W+1与0；07 a31/M8与10 a61/M15，严格门禁选择同，S均+2/N均−2/O均−1。是历史/阶段条件响应证据，不单归随机性。
- 07 a158/M38、08 a130/M31，生产故障完整流程/降级同选择；前者S+2/W+1，后者S/W均0。提供资本响应方差证据，不说明08没有完成故障处理。
- 07 a180/M43(H9/L5)选公司午餐demo，10 a22/M6(H3/L2)选商务晚餐demo；08 a19/M5(H4/L1)也选午餐。10更耗Health的选择有可控比较价值，但月份/职级差异不能称重复同条件policy drift。
- 07 a61/M15(H8/L3)次日回接口问题，10 a35/M9(H4/L2)即时回复，后者H4→2后需恢复；fresh当前scheduled work与健康成本皆真实，仍不能从总分回填固定答案。
- 08 a48/M12对未官宣调整不透露，10 a152/M37给模糊提醒；a153公开出现Leader泄露排查，是具体confidentiality语义问题。C10已有红线，可纳入反例，不另建议一个delta，更不认定它贡献终局风险分的精确值。
- 07 a149/M36 vs10 a86/M21客户Demo归属补充的时机不同；08 a124/M30也当场补充。10 a179 vs08 a82周末学习/提前交付不同，前者饱和理由错误但有真实交付价值。详表中的不同state不降为严格policy不一致证据。

**DESCRIPTIVE ASSOCIATION**：少量choice drift与大量同选择响应差异并存；`CHOICE_DRIFT`不能独自解释4.25。精确因果份额UNKNOWN；此cohort既含同Candidate不同局也含不同Candidate，不是随机控制实验。

## I｜LATE_GAME_CAPITAL_CONVERSION

| Run/window | ΔS/N/O/W 首Review | Main mix | Energy G/NG/unknown | S actions full months |
|---|---|---|---|---:|
| RUN07 24→36 | 39/17/10/10 | Apply2, Mentor1, Avoid1 | 6/2/2 | 0 |
| RUN07 36→48 | 36/17/7/15 | Rotation1, Apply3 | 10/1/0 | 0 |
| RUN08 24→36 | 1/-2/7/7 | Apply4 | 10/0/1 | 3 |
| RUN08 36→48 | 35/17/11/12 | Apply4 | 7/4/0 | 0 |
| RUN10 24→36 | 42/17/8/10 | Avoid1, Apply3 | 6/2/1 | 9 |
| RUN10 36→48 | 27/12/14/13 | Apply3, Avoid1 | 7/3/1 | 7 |

表按首次Review的public资本差，对Main/Energy mix使用M25–36与M37–48完整月份动作（边界语义明示，不宣称同一数值差归因这些动作）。详细Main/Energy records支持复查；Protection按相同动作月份。07晚期Network部分NG仍转Skill/Rotation；10 M33/36/39 O26停滞，直到L5 preparation恢复；08 M42重复NG后NetworkGAIN、M45 prep也恢复。

判 `LATE_GAME_CAPITAL_CONVERSION=Supported pattern`，限定为**DESCRIPTIVE ASSOCIATION**：相同promotion节奏下晚期资本差确实material，不能升级成“某个Main模式必然更高分”。真实result chain优劣仍Insufficient。当前state可行、可留Skill/Network/Wealth/责任结果的responsive action应优先于无其它价值的单维farm；不建立固定M24/L4 switch，不能挤掉有公开收益的交付。

## J｜最多五项可控机制排序

| Rank / mechanism | Evidence / counterexample | Confidence; upside / regression risk | Already v10? / change? |
|---|---|---|---|
| 1 不发明资本饱和 | 07/10跨局caps；10 S100后同L5继续增。反例：H/D10有公开上界，M43提前交付本身也有价值 | High证据越界；upside保留误删学习/资本机会；risk反向刷已NG或破坏交付 | C6“不推cap”已有；对“足够/无用”措辞的salience强化尚未运行验证；**唯一STRENGTHEN** |
| 2 responsive优于local stalled | 08M42连续NG且NetworkGAIN；10M36→39NG。反例：07同L2下次prepGAIN、08同L4M45恢复；HealthGAIN不必高价值 | High路由原则、Medium机会损失；risk永久禁复测/过度probe | C3/C6/C7/C8已覆盖；KEEP，不再增加机制 |
| 3 最小必要保护 | 10M27/M48重复降险candidate，M36标记迟一动作；反例急症真实、S也增长且及时回A | Medium；upside少保守成本，risk忽视医疗/累积warning | C2已覆盖；KEEP |
| 4 ownership兑现/真实成果再可见度 | 三局都有public链，两个Report均有basis；反例无法恢复全项目identity，不能断言07最多 | Medium原则、Low分差解释；upside把责任转result，risk因证据不完整拒绝真实工作 | C1/C9已覆盖；KEEP |
| 5 Main语义选择/晚期组合资本 | 07 Mentor/Rotation有Skill实增，10较单一；反例没有机会集因果证据，08后期也增长 | Medium资本比较、Low配方；upside避免Gap吞掉组合价值，risk机械diversification | C3/C4/master ranking已覆盖；KEEP |

`PRIMARY_CONTROLLABLE_GAP=UNSUPPORTED_SATURATION_DEVALUATION_OF_DURABLE_CAPITAL`；`SECONDARY_CONTROLLABLE_GAP=REPEATED_LOCAL_OUTPUT_STAGNATION`。排序是Stage决策建议，不是预计score uplift排序。

## K｜V10_CONSTITUTION_REVIEW

| C | Decision | RUN10 evidence / boundary |
|---|---|---|
| C1 value before visibility | KEEP | a46Demo、a61CI、a141新方向result有publicbasis；Main Report a52也可恢复basis；全局链效率UNKNOWN |
| C2 default A / minimum protection | KEEP | 7段S多有绑定威胁且回A；M27/M48二次保护及a149滞后可由现规则解释，拒绝S配额 |
| C3 capital portfolio | KEEP | O38高于07但score更低；M36后S/N/W增长较弱；不是Output无用结论 |
| C4 promotion multiplier, no formula | KEEP | 同promotion仍分差；08 promotion更迟；no-promotion未造长期S。倍增因果公式未证 |
| C5 fresh evidence before habit | KEEP | 全201回执→fresh边界；fresh正确不保证Notes世界模型正确 |
| C6 exploit response, no farming | STRENGTHEN | 一条delta：把“无public饱和证据则UNKNOWN，数字高/局部NG不等于资本无用”提至高salience；其余local折价不变 |
| C7 bounded exploration only without good answer | INSUFFICIENT_EVIDENCE | 历史run无POL/PROBE测量；未测Skill合法不等于五条件齐全，不能把a173普通试探升级成v9a probe执行证明 |
| C8 Level reset | KEEP | a49 L3、a173–175 L5响应恢复；支持复测，不证隐藏cap解锁；同Levelcontext也可恢复 |
| C9 realize valuable commitments | KEEP | a46/61/141可恢复兑现；header不证明ledger；不得由DL NONE/0coverage判无commitments |
| C10 accept ordinary cost / avoid asymmetric downside | KEEP | a164medical合理；a152模糊泄密→a153调查是反例，现红线已覆盖；无第二delta |

唯一delta的预期价值是减少**unsupported saturation造成的选项折价**，不是普遍加强学习或改cap规则。v10当前已经禁止“推cap”；建议把高数值→“足够/无用”的同类泛化也明确列入，是基于旧局的措辞强化假设，**不是已证明的v10运行缺陷或salience失败**。Regression risk：忽视local NG、重复probe、挤掉明确Delivery；须保留C6 local/context折价与C9公开交付。Falsification：未来合规取证若继续仅因S高数值/局部NG断言整个family无用，则adherence失败；若不再断言但已有responsive exploit/真实Delivery始终胜出，不能称delta提高分数；若获得explicit public cap，该约束可合法使用。无新live授权，不为此构造run。

## Required Main Decisions / TASK_RESULT

1. `RUN10_68_VS_RUN07_73_PRIMARY_EXPLANATION=MIXED`：终局资本、健康与合法Dev风险记账支持差额描述；public选择/保护及机会响应都可能参与，不能分配4.25的因果份额。
2. `RUN10_OUTPERFORMS_RUN08_MOSTLY_ASSOCIATED_WITH=[earlier promotion, stronger Skill growth]`。这是最有直接public证据的两项；不是Candidate优越性验证。
3. `V10_IMPLICATION=V10_ONE_STATIC_DELTA_RECOMMENDED`：仅强化C6不发明饱和；未改Candidate。其余机制已覆盖或证据不足。

Decision=`S09_16_THREE_RUN_FORENSICS_COMPLETE_RETURN_TO_STAGE`。Acceptance：exact source/window/609 success joins、24 checkpoints、126 Energy/48Main、全部保护段、manual world-model cases、exact public匹配、late windows、唯一primary gap、C1–C10及Q1–Q3已交付。JSON parse/公开投影/新增内容secret scan/`git diff --check`在交付时核验；未跑历史tests、未重建历史包或修改runtime。分支证据尚非MERGED_FACT。

`NEXT_GAME=NOT_AUTHORIZED` · `S09_RUN11=HOLD` · `MAIN_V8A_FREEZE_UNCHANGED`。
