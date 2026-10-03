# TASK_RESULT｜S10-09 v14 Experience Routed Policy Run #1

## 结论与交付身份

Status=`COMPLETE`（本任务的一局执行、离线审计和证据交付）；Classification=`NEGATIVE_POLICY_SIGNAL`；证据归属=`IN_FLIGHT_EVIDENCE`。自然 M18 Health 淘汰，加上具体决策机制失败，支持负向策略信号；不是仅因低分作出的判定，也不是技术失败。Stage 路线与验收仍交 Main/Stage，未宣布 S10 COMPLETE。

- Branch：`codex/s10-09-v14-run01`。
- Parent / execution HEAD：`59a89513096a1e7982dc4a7e896e6d3b3cdd4bf4`，已接受 S10-08 v14 静态来源。
- Candidate：`candidate-v14-experience-routed-policy`。
- Result commit：引入本报告的提交，以 `git log -1 --format=%H -- docs/project/runs/v14-run01-experience-routed-validation.md` 解析；最终 SHA、push 与 clean-tree 回执随交付消息提供，避免提交自身 SHA 循环。
- Remote：`origin` / `MyKr-YSteinsK/CareerSim-BDCI26`；提交与推送仅此分支，不合入 main。
- Main fallback：`candidate-v8a-v7o-donor-core-transplant`，`main@8267d420da29888d0a05403991f8980e251aaa0c` 未改。
- 持久交付仅本报告、[compact evidence](v14-run01-experience-routed-evidence.json)、branch-local `CURRENT_STATE.md`；不提交 raw 或一次性工具。

## 授权、preflight 与实际预算

授权来自用户继续执行所附 S10-09 Plan；精确 Candidate 玩一局至自然或真正技术终点，不作策略救援。Plan 不扩大为第二局、额外 completion probe、Candidate/Runner 修补或官方提交。

| 操作 | 实际次数 / 结果 |
|---|---|
| install | 1；exit 0 |
| service lifecycle | 1；启动、等待 ready、结束后 graceful stop |
| Runner play / fresh game | 1 / 1 |
| replacement / 手工动作 / 策略介入 | 0 / 0 / 0 |
| provider completion probe | 0 |
| 非生成余额读取 | 1；preflight 可用 CNY 7.91，gate PASS；全局资金足够保证 UNKNOWN |
| stop | 1；exit 0；manager 已退出，19092/20000/20001/6173 均释放 |

Caller PATH 下唯一一次 bare `jiuwenswarm-start --list` exit 0；preflight 无竞争实例/必需端口占用。使用根 `.venv` 解释器，不同步依赖。S10-08 32 项稳定静态证据复用，不声称本任务重新执行它们。

实际 bundle 为 manifest + 3 Skill bodies + 6 references。manifest SHA-256=`755799f24d70882b4c8054845c2a0eb94a66a63e908f0662b07640fc9a911122`；10 文件逐字节与 parent source 比较，官方离线 bundle validator 通过；安装后九份 Skill/reference 与 package hashes 一致。完整 hash 清单在 compact JSON。没有把可读/安装证据等同于模型应用或得分收益。

Runner Source Lock 身份=`f61c738c72e51b77298cc1c14c7c6ebf4b6c527d`；本任务未改 Runner。config SHA-256=`5ae22dedc828177df114e500aacf280a17217b45d3d19d9df67b583b7bd08b72`，`max_retries=2` 不变。安装版本：career-emulator 1.0.1、bdci26 1.0.0、jiuwenswarm 0.2.4b3、openjiuwen 0.1.16.post2。

## Outcome 与 Review 轨迹

Session=`009beea968ba4d759c3d59680d9d9db0`；drive=`career-sim-runner-0a1269de5341`。2026-10-04 上海时间 05:15:19 开始 play，05:24:30 primary 自然退出，exit 0；耗时 550.920195 秒。service wrapper 在 graceful stop 后 exit 1，与 primary 自然结束分开记录，不冒充运行失败。

最终：**16.10 quantitative / 11.27 competition partial / 18 months / E / L1**。公开 terminal 为“眼前一黑”、Health 归零身体先倒下；最终 H/D/S/N/O/W/E=`0/2/9/3/3/3/0`。零晋升，首次晋升月不存在，M18 仍 L1。`completed=false` 表示未完成 48 月，不表示 primary 技术中断。

| Formal Review | Grade | Level | 触发后首次公开 H/D/S/N/O/W/E | 后续窗口处理 |
|---|---|---|---|---|
| M6 | C | L1→L1 | 5/10/9/3/2/2/0 | STALE：再次 report / key-project，目标泛化为 Output/Network |
| M12 | C | L1→L1 | 4/10/9/3/2/2/0 | PARTIAL：后来补当前下降 Network，但未重建 result/checkpoint 路径 |
| M18 | D | L1→L1 | 1/2/9/2/3/3/0 | PARTIAL：识别最后窗口、提出 bridge role；同一决策后 Health terminal |

Review 触发与后观察跨 Story/Review/payroll，为 MIXED；前后数值不能归因于单项行动。M6/M12/M18 未有完整 REROUTED 证据。M19–48，尤其 M37–48 late horizon 均 `NOT_EXERCISED`，M18 不能充当终局长程样本。

## Runtime 与 parser 边界

71 成功动作、72 observes，**71/71 成功动作后先 fresh observe 再下一成功动作**。72 action-shaped calls 均为同 session、菜单内合法整数；Energy 13/13 明示可负担，Main 5/5 cost 0。没有 unknown mutation outcome、盲目 mutative retry、人工选择或运行中补丁。

M10 唯一额外 action-shaped call 是错误工具别名：events L357 调用 `mcp__career-emulator__take_action`，L359 明确返回本地 `Ability not found in resource_mgr`；L361 用规范 `mcp_career-emulator_take_action`，L363 成功，L367 observe。已知 pre-dispatch 拒绝未达 MCP mutation，故沿用未变化的 fresh menu，不属于 unknown side effect、重开游戏或失败后盲重发。

规范 `post_run_audit.py` 只执行一次。其旧四-Skill CTRL/DL 检查对本 v14 标记格式 `NOT_APPLICABLE`（S10-08 已接受格式例外）。native Pydantic 工具回执用本机 scoped parser 恢复；generic unknown-result 1 由上述确定 dispatch error 解释。generic transcript identity UNKNOWN 由同一 transcript L9 等显式 `SESSION_ID` 唯一匹配纠正为 scoped PASS；generic outcome UNKNOWN 由 fresh terminal/score/session 绑定纠正。没有为取得通过更改通用 auditor。

Whole-game persistence=`PASS_WITH_LIMITATIONS`：一直运行至自然 M18 终点；48 月能力未验证。Compression scoped count 0，recovery=`NOT_EXERCISED`；continuation count UNKNOWN，仅观察到一个 final frame。fresh observe 通过不证明模型每次实际重新排序。

## Selective retrieval

下表均有成功 native body 回执；events 行号 1-based。路由理由为公开 context 的离线语义判断。每项是该资产首次成功读取，之前没有已读副本；模型当时实际 active-context inventory UNKNOWN，不能据此声称总体上下文减少。

| 月/阶段 | 读取 | call→result | 触发及必要性 |
|---|---|---|---|
| Startup / game 前 | core | 1→7 | 仅启动 kernel；handbook 单独读取 |
| M1 STORY | atlas | 25→27 | 首个普通人际 Story，需语义 router |
| M1 STORY | visibility-network-learning | 29→31 | 普通同事互动，非急性危险 |
| M1 下一 STORY | project-delivery | 41→43 | 跨团队 P0 与自身到期交付竞争；是 action33/observe39 后的新决策 |
| M2 STORY | trust-compliance-conflict | 69→71 | 当前诚信/事实归属冲突 |
| M6 ENERGY | energy-resource | 217→219 | warning cleanup 前资源程序 |
| M18 STORY | survival guard | 601→603 | H1/D2 与明确岗位最后窗口 |

Startup body reads：core only。Skill body reads=3；reference reads=4；guard reads=1。每个决策最多一张新卡；`FULL_LIBRARY_SWEEP=False`、`OVER_RETRIEVAL=False`。

| Card | 成功读取次数 |
|---|---:|
| Review/promotion | 0 |
| Energy/resource | 1 |
| Project/delivery | 1 |
| Trust/compliance/conflict | 1 |
| Health/survival | 0 |
| Visibility/network/learning | 1 |

Under-retrieval 有证据：M3 首个 Energy 未读 Energy card 且出现 batch recipe；三次 Review 都未读 Review card且没有实质重排；M4/M15 serious HR 时未读 guard、清除范围未知；M18 acute Health 未读 Health card，已读 guard 却误用。没有失败或不可读的 reference 回执。

Reference reads per 100 successful actions=`4/71×100=5.6338`；unrelated new-reference rate=`0/4=0%`。四张新卡均有功能相关触发；该指标不测量旧卡驻留或 stale-context 使用。低读取率与 98.66% cache hit 都不能证明 deep grounded choice 成功。

## Policy 判定与可复核样本

| 机制 | 判定 | 实证边界 |
|---|---|---|
| Capsule | PASS_WITH_LIMITATIONS | 当前公开 state/menu/session/正式反馈可见；局部 response、交付状态维护不足，没有仅因缺字面模板判失败 |
| All-choice coverage | PASS_WITH_LIMITATIONS | 必要样本未证提前 top-two 剪枝；比较深度与 bounded one-pass 另判 |
| Bounded one-pass deliberation | FAIL | 多处反复改写“最终选择”，M18 尤其明显 |
| Survival handling | FAIL | 即时身体危险已识别，guard ACTIVE 仍推迟健康恢复 |
| Energy one-step | FAIL | M3 预排完整三步资源配方，observe 未消除 recipe |
| Local NO_GAIN routing | FAIL | M6 report flat 后 M9 重复同 Level/report flat，缺独立价值依据 |
| No-advance reroute | FAIL | C/C/D、无晋升，未建立新的结果/窗口验证路线 |
| Conditional project | FAIL | 五次 Main 全 key-project，广告属性排序反复主导，逐次 owner/blocker/realization exception 未成立 |
| Result evidence | PASS_WITH_LIMITATIONS | 有真实公开 SLA 等成果，但技术平台选型不等于已验收完成 |
| Shallow lookahead | FAIL | M18 假设以后 Energy 修身体，绕过当前急性约束；另有未经验证资格/效果假设 |
| Evidence firewall | FAIL | 模型使用禁止的广告 hidden-effect 算术与推测晋升门槛；本审计不采纳其数值为事实 |
| Public warning admissibility | PASS_WITH_LIMITATIONS | warning 未被当 hidden 而丢弃；处理、清除和优先级仍不足 |
| Ordinary-cost handling | PASS_WITH_LIMITATIONS | 有接受早期 Health 成本；后续数字 buffer 倾向，机会成本因果 UNKNOWN |

Capsule 七个样本：first action17、first Energy113、first Main137、M6 aftermath193、M12 aftermath401、first material HR145、M18 aftermath605。完整 pre/menu/post、同 session、费用、公开 capital 与样本依据见 compact JSON。其他阶段不能从七个样本外推满程 capsule 正确。

| All-choice 必要样本 | events action | 菜单数 | transcript 行窗 |
|---|---:|---:|---|
| first Main | 137 | 5 | 593–641 |
| first Energy | 113 | 8 | 448–578 |
| first Review / first no-advance | 193 | 2 | 829–881 |
| first material warning | 145 | 2 | 641–734 |
| ambiguous：跨团队 P0 vs 本人交付 | 45 | 3 | 71–140 |
| ambiguous：个人设备与公司规则 | 253 | 2 | 1097–1201 |
| ambiguous：关系 vs 技术路线 | 585 | 4 | 2700–2864 |

这些样本包含合法备选比较；first Energy 还考虑不继续消耗资源。无法仅从缺少 narration 推断内部未比较。然而 T481–576 预先安排 Health+Network+report、多个样本长反复，以及 T2906–3440 急性约束仍让位于未来恢复，足以判 bounded/grounded 机制失败。

## Public warning 与 survival ledger

| 公开来源 | 严重性/域 | 行为与后续 | Clearance |
|---|---|---|---|
| M4 observe143：HR 积攒不少风险、要求处理 | serious TRUST；模型 T641 识别 | STORY145 比较客户诚信选项；M6 cleanup221 成功，E3/cost2；当时 guard 未读 | UNKNOWN_UNRESOLVED；一般 HR 表扬不是同范围清除 |
| M6 observe191：C，仍观察名单，需更明确结果 | JOB progression；非仅凭警告就急性危机 | aftermath193、report229、project237；M12 仍 C/无晋升 | 未实质改变 result path |
| M15 observe503：HR 再次严重风险提示 | renewed TRUST | 透明 Story505/513/521；cleanup529 E3/cost2，Health537，Main545；guard 未读 | UNKNOWN_UNRESOLVED；软化/一般表扬不等于同风险消除 |
| M18 observe599：H1/D2、D、Leader 最后窗口 | acute HEALTH + JOB | guard601→603；action605 选 bridge/ownership growth，明确将身体恢复寄托未来 Energy；observe611 H0 terminal | NOT_CLEARED_TERMINAL |

末次模型推理已区分即时身体风险与未来职业窗口，仍多次反转后选新增 bridge-role 负担，显示 guard 语义应用失败。不存在另一个选项一定能活下来的 counterfactual 证据。M4/M15 TRUST 未清除不能被归因为本次 Health 淘汰；无 hidden numeric stock 或隐私/Test 事实进入本 ledger。

## Energy、NO_GAIN、Main 与结果

5 个 Energy segment（M3/6/9/12/15），13 成功动作：Health5、Network3、report3、cleanup2；没有 intensive-work 或 Skill-learning。

| 月 | 按实际顺序的动作及 fresh 局部响应 |
|---|---|
| M3 | Health113 H3→5；Network121 N3→3；report129 O2→3；费用均1 |
| M6 | cleanup221 visible 六维 flat，cost2；report229 O3→3，cost1 |
| M9 | Health317 H2→4、325 H4→6；report333 O3→3；费用均1 |
| M12 | Network425 N1→2、433 N2→3；Health441 H4→6；费用均1 |
| M15 | cleanup529 visible 六维 flat，cost2；Health537 H3→5，cost1 |

三次 clean growth-target NO_GAIN：Network121（observe119→127），report229（227→235），report333（331→339）。Network 下次同族425时 N 已降至1，属于新公开状态并实现局部增益，不能认定永久 cap 或禁止再选。report229后333仍同Level/O3 flat，没有新的独立交付价值/response discount 依据，反复用广告 Output/Leader 反馈支撑；333后未再 report。两次 cleanup 的可见 flat 不证明无隐性 benefit，也不证明具体风险已清除。

T578–582 的 cap/display-lag 猜测、T494–516 的资格门槛/效果推测仅列为模型失败类别，不采纳为环境事实，不在 durable evidence 复写隐性效果数值。新鲜 observe 的数字优先于这些猜测。

Main137/237/341/449/545（M3/6/9/12/15）五次均申请关键项目。所有 Main 都跨月，回报只能记 MIXED；未从跨月 gain/loss 计算单动作净收益。部分推理识别 owner/schedule，但未逐次建立当前 blocker、可实现成果与窗口例外，反复回到广告 S/N/O 排名。

结果证据不全是泛泛表扬：observe73 有公开 SLA/故障/客户投诉改善及 Leader 对真实数据的反馈。另一方面 events81 技术平台选型后 observe89 已到下一月，未见该自研平台完成/验收凭证，不能把选型自动升级为完成结果，更不能据此保证晋升。Review 的 result/checkpoint 管理仍不足。

## Usage 与历史参照

同 session aggregate events usage、score_report 与 canonical totals 一致：input **14,509,853**，output **81,420**，total **14,591,273**；cache **14,315,136**，input cache hit **98.6580%**。play wall **9m10.92s**。实际 billed cost=`UNKNOWN`；score_report 的 reported cost 0.0 不证明免费。余额读数为 preflight 可用额，不是此局账单。

Scoped LLM log 只有一个小型启动 usage 样本，不能当全局 token 来源。aggregate events 才是此处 totals/cache 的依据。audit end 比实际 primary end 晚1ms（exit 通知），log slice 结束于实际 primary exit，差异显式记于 JSON。

历史仅作非受控参照。前五局来自已接受 [mining summary](../research/S10_POLICY_MINING_SUMMARY.json)，v13 仅读取本机 S10-06 已有 compact post-run/transition/Review 摘要，不重新打开其 held raw。

| Run | score / months / Level | 晋升月份 | 终局 S/N/O/W |
|---|---|---|---|
| v6 | 75.29 / 48m / L6 | 6/12/18/36/48 | 142/58/42/39 |
| v7o | 71.83 / 48m / L5 | 6/12/18/36 | 130/53/37/43 |
| RUN07 | 72.65 / 48m / L5 | 6/12/24/42 | 119/54/35/35 |
| RUN08 | 59.00 / 48m / L4 | 12/18/36 | 82/36/26/29 |
| RUN10 | 68.40 / 48m / L5 | 6/12/24/42 | 115/51/38/32 |
| v13 | 34.01 / 36m / L4（自然淘汰） | 6/24/36 | 43/20/16/11 |
| v14 | 16.10 / 18m / L1（自然 Health 淘汰） | 无 | 9/3/3/3 |

前五局自然完成48月，本局18月未晋升；v13曾恢复早期晋升，后来36月仍自然淘汰。终局 broad-growth 数值比较受存活时长和 Level 影响，不能把 v14 低值全部归因于 card 路由。前五局是旧四-Skill来源，没有本 v14 同定义的 card-read 指标；retrieval discipline 不可直接同口径比较，UNKNOWN。v13 公开 warning 的旧审计问题与本局不同：本局承认 warning 但没有正确优先处理急性 Health，不能视为 survival 已修复。此前完整对局的结果不使其每一机制自动 PASS，本次机制判定只使用本局见证。

场景、策略、月份与晋升不同，没有 paired causal comparison；不把历史运行或输入大小当本次减少 context 的控制组。本局没有证明优于这些参照。

## Preservation、验证与返回 Review

形成新证据前 preflight 覆盖的263个 tracked 文件 hash 全部未变；交付只允许随后更新 CURRENT_STATE，剩余262个继续保持原 hash。Candidate/manifest/Skills、Runner、dependencies、provider/retry/config 均未改；validation flags 仍全部 false。main fallback 和已有历史 holds 不变，未修改 frozen Source Lock，不把分支结果写成 merged fact。

验证范围：逐 action session/legal-menu/receipt/fresh-observe/费用的 targeted assertions；七次 native read 成功与 per-card/Reviews/NO_GAIN 的语义 contract 检查；同 session aggregate usage 一致；三份交付 UTF-8 JSON/Markdown、选定文本 secret scan、`git diff --check` / staged diff scope。不运行 full pytest，不把静态 package 检查称为 runtime behavior PASS。一次性 scoped parser/生成器留本机 ignored 目录，不提交。

`FORENSIC_HOLD=ACTIVE`，Owner S10-09；原因是自然提前淘汰与机制失败需要独立核验精确模型决策/回执。最小来源5份及 bytes/hash 见 JSON `FORENSIC_HOLD.files`：

- `D:/CS/CareerSim/.career_sim_runner/career_emu/outputs/local-s06-adaptive-controller/20261003T211522Z/events-20261003T211522Z.jsonl`
- 同目录 `transcript-20261003T211522Z.log`、`score_report.json`。
- `D:/CS/CareerSim/.local/runtime/s10-09-v14-run01/runner-result.json`、`llm-run-window.log`。

run window UTC=`2026-10-03T21:15:19.732287+00:00` 至 `2026-10-03T21:24:30.652482+00:00`。另有本机 preflight/预算/安装/停止回执与 scoped derived evidence，均不入库。hash 不替代原始来源；没有 raw 清理。解除者仅 Main/Stage：接受独立报告、确认来源可恢复或不需重析、关闭 review/child 依赖、显式解除 hold；删除仍需单独授权。

FACT：精确 v14 部署成功、71/71 runtime pairing、自然M18淘汰、以上检索与决策见证。INFERENCE：本次 negative signal 来自选择/路由/约束应用，不能从单局定因所有低分。RECOMMENDATION：Main/Stage 先复核 guard 优先级、Review/result 重排与 one-pass/response 应用的失败，再决定是否有新的实现或实验授权；本任务不设计/修补/救援 v14。

Non-claims：stable75+、stable80+、superiority、causal optimality、hidden-test transfer 均 NOT_PROVEN；没有推断 hidden 阈值、公式或 alternative-choice 生存保证。单局不宣布路线整体否定。

`RETURN_FOR_V14_GAME_GATE`；`NEXT_GAME=NOT_AUTHORIZED`。
