# TASK_RESULT｜S10-10 v6c High-Score Core Revival Run #1

## Result / identity

Status=`COMPLETE`（授权单局、必要离线审计与证据交付）；Classification=`V6C_MID_SAMPLE`；Decision=`V6C_CORE_MID`；证据=`IN_FLIGHT_EVIDENCE`。自然48月完成，但64.26未达75目标；runtime correctness 仍为 `RUNTIME_ADHERENCE_FAIL`。有效 gameplay 与执行合同失败分开记录，不作技术失败或 donor-family 全面否定。

- Branch：`codex/s10-10-v6c-revival-run01`。
- Worktree：`D:/CS/CareerSim/.local/worktrees/s10-10-v6c-revival-run01`；精确 historical parent=`e5363c9b4958955e02f5f895cb1ba1c794215958`。
- Candidate：`candidate-v6c-compliance-cleanup`；lineage v6→v6b→v6c。v6高分来源=`1114a04b75548cf52f030d123564e527060fc061`，收益不自动转移。
- Runner Source Lock：`f61c738c72e51b77298cc1c14c7c6ebf4b6c527d`；历史与根 checkout 的 Runner/pyproject/uv.lock diff 为0。运行使用根 `.venv` 与相同 frozen root Runner，历史 checkout 仅供精确来源及分支证据交付，不重写到现代 main。
- Runtime 根：`D:/CS/CareerSim`；不运行 setup，不改既有共享 MCP DB/config 路由，不建立第二环境。该 checkout 隔离 Candidate 来源，不声称共享服务已隔离。
- Remote：`origin` / `https://github.com/MyKr-YSteinsK/CareerSim-BDCI26.git`；只 push 实验分支，不 merge main。
- Result commit：引入本报告的提交，由 `git log -1 --format=%H -- docs/project/runs/v6c-revival-run01-validation.md` 解析；最终 commit、remote-match、clean tree 回执由交付消息记录，避免自身 SHA 循环。
- 交付：[compact evidence](v6c-revival-run01-evidence.json)、本报告、branch-local CURRENT_STATE；不提交 raw、配置、DB 或一次性 helper。

## Frozen source / compatibility

精确 Git blob bytes 制作 manifest +3 Skill bundle。只消除 checkout 的 CRLF 展开，未改策略文本；五项 source bytes 与指定 commit 一致，package byte-check、官方离线 submission contract、安装后的三份 Skill hashes 均通过。没有 Atlas/cards/Capsule/Delivery Skill 或 v13/v14 规则移植。

| 历史 source 文件 | SHA-256 |
|---|---|
| `configs/current_candidate.json` | `634cdc14d1eac61193a265963b89217c2d0bea9085491880076c009bc5221941` |
| `configs/runtime_manifest.json` | `cf68e26f23b060372e1c75259c6eabe38b229f00788eccdb9aea71408aeeb4e1` |
| `skills/risk-review/SKILL.md` | `83e7600b0da901c18e78cd96d85a2e68a8b5eb9dfa0d7a8cf82f9266690d237d` |
| `skills/rolling-planning/SKILL.md` | `639197dc39c9e569ff7ab0de837a17874419932acde914c7b2efca00e3be83e6` |
| `skills/structured-state-board/SKILL.md` | `e8c25306d108fedf35039bdd25a1540947c6715099ab997fc12a35c8611c3992` |

Python3.12.13；根解释器 `D:/CS/CareerSim/.venv/Scripts/python.exe`。career-emulator1.0.1、career-emulator-bdci26 1.0.0、jiuwenswarm0.2.4b3、openjiuwen0.1.16.post2 不变。194个 distribution Dev 文件逐个匹配已安装 RECORD；未解码题库、更新或加载另一 split。前后 hash 集合一致，aggregate hash 见 JSON。

同配置 SHA-256=`5ae22dedc828177df114e500aacf280a17217b45d3d19d9df67b583b7bd08b72`，model request=`deepseek-flash`，`max_retries=2`。底层 serving identity 仍按既有公共映射 PARTIALLY_VERIFIED，不增加 completion probe。配置保留既有 legacy DB 路径，仅在 JSON 记录路径，不读取 DB 或为了美化路径迁移。MCP 模块/可执行文件静态可用，run 实际成功调用 handbook/new_game/observe/take_action，必要界面可用性已举证。

## Live budget / lifecycle

| 操作 | 实际 |
|---|---|
| Candidate install | 1，exit0 |
| service lifecycle | 1，无 restart |
| Runner play / fresh game | 1 / 1 |
| replacement / manual choice / intervention / Candidate patch | 0 / 0 / 0 / 0 |
| provider completion probe | 0 |
| 非生成 balance read | 1；CNY7.10，availability PASS；全程资金保证 UNKNOWN |
| bare jiuwenswarm-start --list | 1，caller process PATH prepend 根 Scripts，exit0 |
| graceful stop | 1，exit0；manager PID absent，四个已知端口均释放 |

2026-10-04 上海时间12:16:15.516786开始 play，12:40:18.843719 primary自然退出；wall=1443.326933秒（24m03.33s）。primary exit0；service wrapper 在 graceful stop 后 exit1，单独记录，不混成 Runner 技术失败。monitor 只读已产出 events，不做 MCP/DB/provider query，不控制结束。没有在无晋升 Review 处停止。

## Outcome / promotion trajectory

Session=`50c5288ff1384735b4dd9509fe76ba96`，output identity=`20261004T041620Z`。最终 **64.26 quantitative /44.98 competition partial /48m /B /L5**，`completed=true`。fresh final observe 在行政M49，scored survival为48m，非多玩一局。最终 H/D/S/N/O/W/E=`5/9/129/50/38/25/0`。

晋升 M6/M12/M24/M42；M18 L3；M18、M30、M36、M48没有晋升。M6/M12 与v6相同，第三次由M18延至M24，第四次由M36延至M42，未达到v6的M48 L6。不是从grade推断隐藏资格。

| 月 | Grade | Level | 晋升 | 首次 Review 后 H/D/S/N/O/W/E | 下一动作 G/P/R |
|---|---|---|---|---|---|
| M6 | C | L1→L2 | 是 | 5/10/9/3/3/1/0 | output/?/PASS |
| M12 | B | L2→L3 | 是 | 6/9/21/4/6/3/0 | output/?/PASS |
| M18 | B | L3→L3 | 否 | 7/10/33/13/10/5/0 | output/?/PASS |
| M24 | B | L3→L4 | 是 | 8/10/42/19/16/8/0 | output/A/ALLOW |
| M30 | B | L4→L4 | 否 | 7/10/64/31/23/12/0 | output/A/PASS |
| M36 | A | L4→L4 | 否 | 10/10/78/35/26/17/0 | output/A/PASS |
| M42 | A | L4→L5 | 是 | 6/10/103/34/24/22/0 | network/A/PASS |
| M48 | A | L5→L5 | 否 | 3/10/124/48/37/24/0 | output/A/PASS |

每次完整 Review 的 action/pre/post lines、公开 S/N/O/W/H/D、正式 feedback 与下一动作 marker 在 JSON；跨月 Story/Review/payroll 标为 MIXED，不能归因单动作。G/P 是实际 CTRL 语义标签，不能代替 full-checkpoint 正确性证明。Risk Budget 未明确绑定的 Review 记 UNKNOWN；M12 T2001–2012 明确新L3基线/AVAILABLE，M18 T4004–4012保持Output/亮点、谨慎AVAILABLE，M24 T4784–4796新L4基线仍Output，M36 T6323–6328以A反馈称亮点ADVANCING。

## Runtime correctness

| 合同 | 结果 | 证据边界 |
|---|---|---|
| action→fresh observe | PASS 197/197 | 每个成功动作后、下一状态改变前有同session fresh observe |
| Energy integer | PASS36/36 | 全197动作也是菜单内单整数，无数组/逗号串 |
| affordability | PASS | Energy36/36、Main16/16明确可负担 |
| session identity / tool/schema | PASS | 197成功/198observe/1freshgame；0错误、0unknown mutation outcome、0非canonical route |
| 三份Skill启动读取 | PASS | read_file calls3/5/7，results11/15/13；三份真实成功body，首动作前读取 |
| CTRL action linkage | PASS197/197 | notes仅一个完整canonical CTRL，无缺失/重复/X0 |
| RECONSIDER process closure | PASS | M2 action73 R=RECONSIDER X=1合法；替代比较/gate见T194–246 |
| DECISION_CLOSED | FAIL | 完成Risk gate后无新公开证据仍重开比较/gate或讨论marker |
| compression recovery | FAIL，两次 | 两epoch后无任何三Skill重读；不能满足fresh observe→全三读→重建 |

Canonical auditor把R=RECONSIDER统一记 nonfinal，得到1 closure failure；v6c历史合同却明确“完成X=1且R=RECONSIDER保持；换项仍须gate但不改R”。M2拒绝连班确有一个直接相关合法替代及终gate，故这项是 parser语境不匹配，历史合同下通过；不更改通用auditor。旧四Skill Delivery marker全missing对本历史三Skill `NOT_APPLICABLE`。这些例外不掩盖真正closure/recovery失败。

DECISION_CLOSED见证：T10完成intro PASS后T12–34反复讨论G/P/notes；M25 serious incident T5039–5043已经gate ALLOW/submit，T5045–5071同一公开state下再次比较/复审并重跑gate。普通ambiguous分享文章T2078–2155、M18 Energy T3825–4001也出现大量“FINAL”后反转。没有因未写字面DECISION_CLOSED便判FAIL；判定依实际重开行为，精确总失败次数UNKNOWN。

Scoped CurrentRoundCompressor epoch UTC04:26:57、04:37:02（上海12:26:57、12:37:02），count2。canonical分别观察到epoch后action前fresh observe yes/no，Skill rereads均0；实际全局仅启动三读足以证明两个epoch恢复失败。旧auditor的Delivery/recovery_ready字段非v6c协议，重建是否独立完成UNKNOWN；也没有把一般Board叙述当作恢复完成。Flattened transcript未显示生成snapshot正文，snapshot实际策略权威UNKNOWN。没有争议的0 reread证据与这些未知分开。

## Survival / risk behavior

结论=`PASS_WITH_LIMITATIONS`：自然存活48月，存在真实public-trend mitigation行为；不证明所有重大warning清除或风险判断最优。没有新的生存策略补丁。

| 时点 | 公开约束 | Risk Budget / candidate / gate | 动作与fresh后果 |
|---|---|---|---|
| M2，observe71 /action73 | H5→4→3，连班会增负荷 | TIGHT；先看连班，再RECONSIDER一项低负荷替代；X1 | 婉拒由Leader协调；首次post跨月H5（MIXED，不把恢复全归因该选项） |
| M9，actions313/321/329 | H降至4、近期下降 | TIGHT，缓解身体约束 | 两次Health恢复，再report；逐步fresh核对，最终H8 |
| M25，observe831 /action833 | 漏洞被利用、用户数据异常访问、HR“自求多福” | FULL_REVIEW/ALLOW；选应急响应、通知并配合监管 | firstpost O23→21、N20→21；无特定same-scope clearance |
| M26，observe855 /action857 | HR要求处理积累风险 | 当时RB不可靠绑定，UNKNOWN；具体Story合法选项见JSON | 后续M27仅轻度提示不等于全清 |
| M27，actions905/913/921 | H6 + earlier serious HR warning | TIGHT；拒绝直接加重约束的intensive候选，cleanup PASS | cleanup可见六维flat；Health6→8；Main项目未被判直接恶化约束；warning clearance UNKNOWN |
| M41–48 | Health下降、末段H3 | 风险趋势被识别；M47低负荷分享处理经过长反复，限度明显 | M48先恢复H4→6，再intensive成本H6→5；最终自然完成，无alternative counterfactual保证 |

严重warning ledger不是hidden库存：两个独特serious HR观察记录在JSON，分别M25/M26；普通轻度提示/一般表扬不一律升级crisis，也不被当作完全消除。M2相对历史v6 M13的RECONSIDER不同月份，仅可作类似机制实例。模型将广告hidden-effect算术、隐性作用和资格猜测混入决策，Evidence firewall=`FAIL`；审计仅保存违规类别/行窗，不采纳隐藏数值、库存、阈值或跨局题库。170个numeric-hiddenrisk text matches是文本匹配量，不是170次独立违规判定。

## Main / Energy / observed-effect adaptation

Main：key-project **16/16**；相应G主要Output，全部Risk PASS，公开reason反复是Output/亮点、review窗口。v6是key-project14/16、low-profile2/16。本局不能因全部项目自动判策略错误，也不能将16个跨月MIXED转移当作项目净收益；每次当前公开state、选择与marker均在JSON。

Energy：36次；report10 /Health12 /Network2 /intensive10 /cleanup2 /psychological0。不同菜单次数受cost影响，不强制v6比例。

| 菜单月 | actual sequence（events action line） |
|---|---|
| M3 | 准备汇报材料(105,cost1) → 人脉维护(113,cost1) → 健康恢复(121,cost1) |
| M6 | 准备汇报材料(209,cost1) → 准备汇报材料(217,cost1) → 健康恢复(225,cost1) |
| M9 | 健康恢复(313,cost1) → 健康恢复(321,cost1) → 准备汇报材料(329,cost1) |
| M12 | 人脉维护(417,cost1) → 准备汇报材料(425,cost1) → 健康恢复(433,cost1) |
| M15 | 高强度工作(521,cost2) → 准备汇报材料(529,cost1) |
| M18 | 处理历史埋雷(617,cost2) → 准备汇报材料(625,cost1) |
| M21 | 高强度工作(713,cost2) → 健康恢复(721,cost1) |
| M24 | 高强度工作(809,cost2) → 准备汇报材料(817,cost1) |
| M27 | 处理历史埋雷(905,cost2) → 健康恢复(913,cost1) |
| M30 | 高强度工作(1001,cost2) → 健康恢复(1009,cost1) |
| M33 | 高强度工作(1097,cost2) → 健康恢复(1105,cost1) |
| M36 | 高强度工作(1193,cost2) → 准备汇报材料(1201,cost1) |
| M39 | 高强度工作(1289,cost2) → 准备汇报材料(1297,cost1) |
| M42 | 高强度工作(1385,cost2) → 健康恢复(1393,cost1) |
| M45 | 高强度工作(1481,cost2) → 健康恢复(1489,cost1) |
| M48 | 健康恢复(1577,cost1) → 高强度工作(1585,cost2) |

每步cost、pre/post、CTRL、菜单合法性及local/MIXED分类在JSON。局部growth-target flat共7次：report113(M3)、217(M6)、329(M9)、1201(M36)；intensive713(M21)、1097(M33)、1193(M36)。其中cost和公开副作用仍发生，不能用菜单广告覆盖flat。

Observed-effect adaptation=`FAIL_WITH_POSITIVE_LOCAL_SAMPLE`：M6 T1204–1225注意report O6→6，改剩余Energy为Health；但将flat扩展成“饱和/季度规则”仍超出证明。M33 intensive O26→26，T6125却称本季已经获得Output2；M36继续intensive/report，两个首次post都O26→26。M39又能增长说明不能建立永久cap。strict STALLED所需“两相邻可比checkpoint”未建立，formal Review重置/事件污染不允许为了FAIL套入后续v13/v14的NO_GAIN规则。

Review reset=`PASS_WITH_LIMITATIONS`：正式反馈/新Level被识别，并叙述新baseline；Output/亮点焦点长时间保留，A与表扬被用于ADVANCING，checkpoint有效性不能单靠CTRL证明。季度joint Energy+Main为历史合同允许，批量投影仍须逐次fresh scan；36次合法单调用与fresh pairing已证明，没有把允许的joint planning本身判成v14式禁配方。

Story样本：M2连班（material Health）；M25数据事件（serious compliance）；末段分享/曝光与H3（career opportunity/生存）；M12方法论完整分享vs保留（ordinary ambiguity）。公开选项/当局后果驱动与“模拟器喜欢某答案”的猜测同时出现，后者不作为合规事实或收益证据。

## Usage / comparison

同session gameplay aggregate：input **38,946,492**，output **190,016**，total **39,136,508**；cache **38,508,544**，hit **98.8755%**。wall24m03.33s。score-report reported cost0.0，实际billed cost UNKNOWN，不记免费。

Scoped LLM额外usage单独统计：startup200/1/201；两个compressor分别159,894/4,247/164,141及160,056/5,363/165,419，cache各158,336。它们在Runner gameplay aggregate之外。此窗合计input39,266,642/output199,627/total39,466,269；不把这些混入与v6 gameplay比较。请求model为deepseek-flash，实际底层serving版本仍部分可验证。

| 描述性参照 | v6 | v6c本局 |
|---|---|---|
| score/partial/month/grade/Level | 75.29/52.70/48/A/L6 | 64.26/44.98/48/B/L5 |
| 晋升月份 | 6/12/18/36/48 | 6/12/24/42 |
| Main | 项目14、避险2 | 项目16、避险0 |
| Energy report/Health/Network/intensive/cleanup/psych | 15/10/8/5/2/1（41次） | 10/12/2/10/2/0（36次） |
| gameplay input/output/total | 40,372,074/247,309/40,619,383 | 38,946,492/190,016/39,136,508 |
| gameplay cache | 39,865,088 | 38,508,544 |
| wall | 到首次terminal约26m36s | 到primaryexit24m03s（边界略异） |
| action shape/pairing | 1次逗号串拒绝；202/202成功后fresh | 无shape错误；197/197 |
| closure / compressor recovery | 普通决策反复；两epoch未重读 | 仍反复；两epoch仍未重读 |

原v6参照仅来自已接受根仓库 `docs/project/runs/v6-run1-validation.md`，不打开其旧held raw。部分runtime改善：合法单整数与action-linked canonical CTRL；核心closure/recovery缺陷未解决。较晚晋升及L5是本局弱于v6的重要描述差异，不能从单局归因某Skill或动作比例。两局均自然存活；不同随机事件与trajectory不构成因果控制。

次级参照（已接受Plan/compact records）：v7o71.83/48m/L5；v8a RUN07 72.65/48m/L5；v13 34.01/36m/L4；v14 16.10/18m/L1。本局生存长于v13/v14、score低于v7o/RUN07，仍未复制75.29。后期策略不用于重新定义v6c adherence。

## Verification / preservation / delivery

仅执行必要offline contract检查：197个receipt/session/menu/notes/fresh pairing；Energy/Main费用；八次Review和局部响应；同sessionusage；source/package/安装字节、环境/194个Dev文件、前后config；选定三份文本secret scan、UTF-8 JSON/Markdown、diff与stage范围。没有full pytest、依赖同步、官方submission或策略修补。

根checkout全部原tracked hashes保持；历史checkout交付前tracked hashes保持，只允许随后更新CURRENT_STATE并新增两个run文件；frozen五文件继续同Git源。Candidate validation flags仍全部false，runtime/adherence收益不因有效游戏而自动置true。PROJECT_BRIEF/ADR无变化。main fallback仍v8a，根v14证据分支与所有旧holds未变。

FORENSIC_HOLD=`ACTIVE`，Owner=S10-10。原因：历史CTRL parser语义争议、DecisionClosed与两个recovery失败需要精确decision/回执独立审查。最小5文件的bytes/hash见JSON：当前events/transcript/score_report，task-local runner-result/llm-run-window。确切run-output=`D:/CS/CareerSim/.career_sim_runner/career_emu/outputs/local-s06-adaptive-controller/20261004T041620Z/`；task-local=`D:/CS/CareerSim/.local/runtime/s10-10-v6c-revival-run01/`；UTC窗04:16:15.516786至04:40:18.843719，日期2026-10-04。

Raw不提交、不删除；hash不替代source。Main/Stage在接受独立compact审计、确认来源可恢复/无复析需要、关闭review/child依赖后显式解除hold；之后cleanup另需授权。worktree保留待review，不自动删除其指向来源；实际raw在根runtime输出与task-local中。旧hold独立保留。

Plan implementation choice：历史source独立checkout，实际Runner从相同根source运行以保持既有shared config/DB路由。应用managed工具起初创建到用户目录，空checkout已归档；改用约定 `.local/worktrees/`。准备中的行尾index刷新、inline quoting、错误预期DB路径和已有package resume guard属于本机Tooling Error，全部在install/service/provider/list前或纯离线阶段解决，不消耗额外live预算。没有以工具错误绕过真实运行限制。

EXECUTION_METRICS：Codex model/reasoning effort UNKNOWN；本任务最早可靠preflight时间与delivery结束时间由本机receipt/Git记录，不能将24m03s gameplay wall冒充整个任务耗时。Provider成本UNKNOWN。全部结果按FACT/INFERENCE/RECOMMENDATION区分。

FACT：精确v6c、自然48m/64.26/L5、合法pairing和上述合同失败。INFERENCE：高分donor后代本局表现中等、closure/recovery缺陷持续；单局不足以清除v6历史75.29证据。RECOMMENDATION：Main先比较晋升延迟及机制见证，再决定是否复验或改方向；不立即重写prompt，本任务没有下一局授权。

Non-claims：单局不证明stable75+、80+、causal superiority、hidden-test transfer；未证明donor family整体失败，不编造晋升门槛、hidden库存或counterfactual结果。

`RETURN_FOR_V6C_REVIVAL_GATE`；`NEXT_GAME=NOT_AUTHORIZED`。
