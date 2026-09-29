# S07-47｜v7m M20 Partial-Run Forensics & Skill Audit

## 结论与权限

**Main recommendation：B — `STATIC_PATCH_JUSTIFIED_BEFORE_RETRY`。** 最小后续范围是事实/交付证据合同的可执行输出约束：Board 直接复制 fresh public state；Delivery 保留短 item identity 与实际结果证据，不能把客户赞许沟通当成交付验证；消除把内部数值抄入可见策略输出的路径。这是下一份静态 Plan 的建议，本任务未修改任何 Candidate、Skill、runtime manifest、Runner 或安装内容。恢复重读仍不合规，但本次不能证明增加恢复提示文字能解决问题，也不能据此推导 WebSocket 根因。

S07-46 是有价值的 `PARTIAL_GAMEPLAY_TECHNICAL_FAILURE`，不是无数据局。M20 仍活着，84 次行动全部成功；没有自然终局或成绩。v7m 的健康、财富和部分人脉表现好于 v7g，晋升节奏仍与 v7g 相同，明显落后于 v1/v6 的高分参考；M18→M20 有公开增长，但不足以预测终局分数。

本任务基线 `main@9faf202174c165899837e4f881afd0bcc40e0cdd`；Candidate `candidate-v7m-final-r-recovery-audit-hardening`，parent v7l。全部取证离线，live 次数为 0；未接触 shared DB。S07 保持 ACTIVE，全部 Candidate validation flags 保持 false。**NEXT_GAME = NOT_AUTHORIZED。**

## 证据与重建方法

主源是 [S07-46 archive](../../../artifacts/dev-runs/S07-46-v7m-run1/) 的 `events.jsonl`、`transcript.log`、`runner-result.json`、manifest。沿用原始证据，不改 raw。events 有 350 条 call 和 350 条 result 表示；按 `(kind, tool_call_id)` 去重后各 175 条。框架 delta 与 event 表示不是两次操作。独立逐调用重建与修正后的 `post_run_audit.py` 结果一致。

最终机械输入：本机 `.local/scratch/s07-47/post_run_summary.json`，SHA-256 `e7f62b72d6b8d6f1345c62878f5da2d0b13a2aeebfff203e861a54b6b2878563`。它包含公开 observation 轨迹、CTRL/DL、压缩工具顺序和 limitations；不含隐藏数值或虚构 score。临时 `decisions.json` / `segment-metrics.json` 仅为 ignored 离线派生物，不提交、不作唯一证据。报告中的语义结论必须回到 archive 验证，marker 本身不证明遵循。

| 身份/边界 | 独立重建结果 |
|---|---|
| new_game unique calls / results | 1 / 1 |
| fresh session | `2e25b395d04f46c1ba9662f0edef5ea9` |
| observe | 85；全部同一 fresh session，transcript 同号；不同于旧 v7g session |
| take_action | 84 calls / 84 successful results / 0 failed / 0 unknown；全部 canonical route、单一合法整数 |
| first observe | 2026-09-29 00:39:49.446242 +08；M1，L1，H5/D5/S1/N1/O0/W1/E3 |
| last observe | 2026-09-29 00:49:14.721205 +08；M20，L3，H8/D10/S31/N15/O10/W11/E0；tenure=3 |
| last public event | 周末厂内高级架构师认证机会；该 observe 后没有提交新行动 |
| alive / failed | true / false |
| Runner | exit 1；00:39:37.849938–00:49:20.541221 +08，582.691 秒 |
| natural terminal / 48m completion | NO / 未达到；自然最终 outcome、score 均 UNKNOWN |

175 个逻辑调用组成：new_game 1、observe 85、take_action 84，加手册与四 Skill 初始读取。S07-46 的 M18 是当时 stdout 进度查询的 marker，不能代替之后的 fresh M20；session/new_game UNKNOWN 亦被本次证据纠正。技术失败仍不满足 S07-46 gameplay validation。

## WebSocket：主分类 H — INSUFFICIENT_EVIDENCE

调查从 00:49:00–00:49:25 +08 开始；发现相邻的 00:49:28 模型错误后，仅跟进该记录。使用既知 `.local/runtime/s07-46-v7m-run1/` 的 stdout/stderr/service-start stdout 和一次 bounded listing 确认的实例日志：`C:/Users/Yukis/.jiuwenswarm-instances/career_emu/logs/logs/{server,runner,context_engine,llm}.log`、`run/jiuwen.log`。Plan 中 `CareerSim.local` 按既有 `.local` 路径解析。未做进程、端口、网络或服务操作。

| 证据 | 能支持什么 | 不能支持什么 |
|---|---|---|
| runner.stderr：WinError 1236 → ConnectionAbortedError → ConnectionClosedError；栈在 `ws.recv()` | 客户端接收 socket 被本地系统中止；无 close frame received or sent | 无协议 close code/reason；“本地系统”不等于 Runner 主动取消，也不等于用户查询造成 |
| 00:49:14 fresh M20 observe 已成功返回 | 断开前 gameplay 和工具仍可运行 | 不证明稍后服务器持续健康 |
| service-start.stdout 2508–2517 / jiuwen.log 38120–38128：observe 后新的 LLM streaming request | 出错时有模型请求在途 | 不证明 provider 先于 WebSocket 失败 |
| service-start.stdout 2518–2624：00:49:28 RemoteProtocolError / incomplete chunked read，随后 TASK_FAILED；llm.log 3039 同类错误 | 服务任务至少继续记录到 Runner exit 后约 8 秒；有模型流中断证据 | 可能共同网络原因、后续连锁或独立中断；无可复现机制，不能定 C 或 E |
| llm.log 3013：00:48:25.398036 压缩 snapshot 响应 | 一次真实当前轮压缩完成；早于最后 observe 约 49 秒 | 未见临界窗口的压缩异常或 context-length failure；不能定 D |
| 已存故障链 | 未见 ping timeout、KeyboardInterrupt、shell cancellation、服务重启签名 | 日志缺失不证明这些绝不发生；服务进程完整生命周期 UNKNOWN |

最先可见的终止证据在 Runner 客户端；准确 initiator、底层网络原因、是否共同影响 provider 与本地 WebSocket 均 UNKNOWN。未恢复到有效 close code，不能凭异常名称猜测 1006 或主动关闭方。后续 cleanup PASS 沿用 S07-46，不重新核验，也不污染 gameplay。

**用户进度查询因果结论：`NO_DIRECT_MECHANISM_FOUND` / causality NOT_SUPPORTED。** 已知查询只读 stdout 尾部，未调用模型、MCP、Runner 或 websocket，未写文件或 DB。存在 `TEMPORAL_CORRELATION`，但没有 `DIRECT_MECHANISM` 证据；M18 marker 之后 archived fresh observations 继续到 M20，是反对“查询即终止游戏”的实质证据。不能排除任何未记录的系统层共同原因，故底层归因仍 `INSUFFICIENT_EVIDENCE`。这不把主分类擅自改成“已证瞬时网络故障”，也没有证据要求先 patch frozen infrastructure。

## 公开轨迹与正式评审

取每个指定月最后一条 fresh observe；M20 是 partial 截止，**不是完整 M20 月末**。季度月最后 observation 位于 Main 提交前，Main 的后续变化进入下一月；历史表亦按最后 observe 定义对齐，不将季度后值倒填为评审前值。所有值来自白名单 state，不反推隐藏阈值。

| M | Level | tenure | H | D | S | N | O | W | E |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | L1 | 1 | 5 | 8 | 3 | 3 | 1 | 1 | 3 |
| 3 | L1 | 3 | 6 | 10 | 6 | 3 | 3 | 1 | 0 |
| 6 | L1 | 6 | 9 | 10 | 9 | 3 | 3 | 3 | 0 |
| 9 | L1 | 9 | 8 | 10 | 9 | 3 | 3 | 4 | 0 |
| 12 | L2 | 1 | 8 | 10 | 16 | 7 | 6 | 4 | 0 |
| 15 | L2 | 4 | 8 | 10 | 21 | 7 | 6 | 5 | 0 |
| 18 | L3 | 1 | 8 | 10 | 26 | 8 | 7 | 9 | 0 |
| 20 partial | L3 | 3 | 8 | 10 | 31 | 15 | 10 | 11 | 0 |

| Review-time first observe | L/H/D/S/N/O/W | grade / promotion | 公开反馈 |
|---|---|---|---|
| M6 | L1/8/10/9/2/3/3 | C；留 L1 | 整体达标、亮点不突出；不是“已经晋升” |
| M12 | L2/5/10/9/3/3/4 | C；L1→L2 | 仍在观察名单、需要更清晰成果；HR 轻微风险提醒 |
| M18 | L3/6/9/21/4/6/8 | B；L2→L3 | 仍需更清晰成果；晋升伴随协作摩擦 |

M1–M5 的客户需求确认、团队融入和合规处理形成早期 O3。M6 未晋后目标转向可见成果；M7–M11 遇自研延期、客户延期、认可不足，O 一度降至 1。M12 方法论文章获得实际采用，S/N/O 明显增长。M13–M17 有里程碑汇报、压测复核、署名争议与谈薪。M18 晋升后 M19–M20 的关系修复、奖金沟通继续推进。M18 最后观察→M20 截止变化为 S +5、N +7、O +3、W +2，H/D 不变；这是实质公开增长，不能外推 48m。

## 同期对比

v1/v6/v7g 来源：[S07-35](S07-35_FOUR_RUN_EARLY_TRAJECTORY_CONTRAST.md)、[S07-34](S07-34_V6_V7G_EARLY_TRAJECTORY_COMPARISON.md)。v1 raw 不可恢复的限制沿用；v7i 来自已接受 [S07-40 re-audit](../runs/v7i-run1-replacement-validation.md) 与该报告精确指向的 `20260928T112740Z/events-20260928T112740Z.jsonl`，只提取公开 M6/M12/M18 状态。历史终局 76.04/75.29/54.52/64.0 仅是参考身份，不预测本局成绩。

| Run | M6 最后观察 L/H/S/N/O/W | M12 最后观察 | M18 最后观察 |
|---|---|---|---|
| v1 #1 | L2/7/13/5/6/2 | L3/7/24/7/7/4 | L4/10/44/19/16/6 |
| v6 | L2/6/11/3/5/3 | L3/5/23/8/7/4 | L4/9/38/19/17/8 |
| v7g | L1/5/9/3/3/2 | L2/4/10/6/6/3 | L3/7/26/6/7/6 |
| v7i | L2/7/13/4/6/2 | L3/8/22/9/7/4 | L3/7/42/21/16/6 |
| v7m | L1/9/9/3/3/3 | L2/8/16/7/6/4 | L3/8/26/8/7/9 |

| Run | M6 review-time L/H/S/N/O/W | M12 review-time | M18 review-time | grade / 晋升 |
|---|---|---|---|---|
| v1 #1 | NOT_COMPARABLE（完整该时点字段缺失） | NOT_COMPARABLE | NOT_COMPARABLE | 已接受晋升 L2/L3/L4；后两次具体反馈 UNKNOWN |
| v6 | L2/4/9/3/3/3 | L3/6/20/4/5/4 | L4/10/37/16/14/8 | C/B/B，三次晋升 |
| v7g | L1/4/9/2/3/2 | L2/3/9/3/3/3 | L3/8/21/3/6/6 | C/C/B，后两次晋升 |
| v7i | L2/3/9/3/3/2 | L3/6/21/4/5/4 | L3/7/42/21/12/8 | C/B/B，前两次晋升 |
| v7m | L1/8/9/2/3/3 | L2/5/9/3/3/4 | L3/6/21/4/6/8 | C/C/B，后两次晋升 |

**总体 `MIXED`；维度上 `EARLY_TRAJECTORY_AHEAD_OF_V7G` 与 `EARLY_TRAJECTORY_BEHIND_HIGH_SCORE_REFERENCES` 同时成立。** M18 v7m 对 v7g：Level/S/O 相同，H +1、N +2、W +3；对 v6：少一阶，S -12、N -11、O -10；对 v1：少一阶，S -18、N -11、O -9；对 v7i：Level 同，S -16、N -13、O -9。M12 v7m 对 v7g 的 S +6 出现在评审后，评审时两者 S9/O3 相同，不能拿后来的增长解释晋升。v7m 尚未达到高分参考的成长轨迹。

## Action mix、Energy 与意图

84 次 = 手册确认 1 + Story 59 + Energy 18 + Main 6。六次 Main 全部申请关键项目，与 v1/v6/v7g 前六季相同，不能单独解释分差。所有选择从当时公开合法菜单获得；不存在错误路由、行动失败或重复提交。

| 观察季度/月 | Energy 实际顺序 | 消耗 | intent 与实际 |
|---|---|---:|---|
| Q1/M3 | 人脉、汇报、人脉 | 3 | 最终 intent 一致；首次设定前多次修改草案 |
| Q2/M6 | 汇报、汇报、人脉 | 3 | 一致 |
| Q3/M9 | 汇报、汇报、人脉 | 3 | 一致 |
| Q4/M12 | 恢复、恢复、汇报 | 3 | 一致；已识别健康约束却仍标 A |
| Q5/M15 | 汇报、汇报、人脉 | 3 | 一致 |
| Q6/M18 | 汇报、人脉、恢复 | 3 | 一致；输出误写 Q7，fresh time 实为 Q6 |

总 Energy：汇报 9、人脉 6、健康恢复 3；高强度/技能学习/心理修复/清雷/保留均 0。一次一整数，最终意图保持；没有证据显示每次 Energy 都从零重选，但首次设定和个别剩余选择仍有多次自我比较。Q1/M3 的汇报 1 点少于 v1/v6 的 2，多于 v7g 的 0；M1–M6 汇报/人脉/健康为 3/3/0，M7–M12 为 3/1/2，M13–M18 为 3/2/1。按实际点数比较，不把零高强度认定为高分原因。

同期 Energy 点数顺序为高强度/汇报/人脉/健康/心理/清雷；每个窗口各6点。v7i按同一公开菜单和调用去重重建，其Q1顺序为恢复→人脉→汇报；Q1首次准备材料量与v7m相同，但不能视为同一具体交付机会。五局前六季Main均6次申请关键项目。

| Run | M1–M6 | M7–M12 | M13–M18 |
|---|---|---|---|
| v1 #1 | 0/2/1/3/0/0 | 0/2/1/3/0/0 | 0/4/2/0/0/0 |
| v6 | 0/2/0/2/0/2 | 2/1/2/1/0/0 | 2/2/0/1/1/0 |
| v7g | 2/0/0/2/0/2 | 2/2/0/0/0/2 | 4/1/1/0/0/0 |
| v7i | 0/3/1/2/0/0 | 2/2/1/1/0/0 | 2/1/0/1/0/2 |
| v7m | 0/3/3/0/0/0 | 0/3/1/2/0/0 | 0/3/2/1/0/0 |

语义类别允许重叠，保守只计明确选择，非模拟器效果权重：可见交付/承诺/验证类 Story 16（actions 6,17,29,30,36,41,44,46–49,54,55,57,60,67），加汇报 9/Main 6，共 31；明确恢复/稳定 5（10,32,50,51,78）；明确关系/支持/协商类 Story 21（4,5,9,18,21,22,23,28,31,42,56,61,62,68–73,81,82），加人脉 Energy 6，共 27。直接正式可见度/评审准备为汇报 9、Main 6、Story 46/54/57，共 18；其中与一次正式评审结果存在**已证因果链接**的数量 UNKNOWN。这里给出编码口径，未将全部成长 Story 都算为交付。

## 四 Skill audit

| Skill | 分类 | 强项 | 明确弱项及归属 |
|---|---|---|---|
| Board | `BOARD_ADHERENCE_FAIL` | 84 个最终 Board 对应 84 次提交；M6/M12/M18 review 与 promotion 保留正确 | 13 个 Board 的 W 与 fresh state 不同，写入推算小数；急性身体警报未进入 STICKY；部分作用归因跨过月薪/评审。主要是 model adherence，现有合同已禁止 |
| Planning | `PLANNING_ADHERENCE_FAIL_WITH_PARTIAL_STRENGTHS` | G 稳定、有正式反馈依据；季度最终意图保持；动作全部合法 | MODE 对急性健康警报未切 S；数值证据纪律与一轮决策预算不完全遵循；不是“所有 A 都错” |
| Delivery | `SEMANTIC_OVERCLAIM`；`STALE_OR_SATURATED_STATE` limitation | 84/84 DL 语法正确；方法论采用存在真实结果证据 | 首次 verified 升级不成立；长期 n3、缺 item identity，无法完整复核 carry-forward/替换；model adherence + observability contract gap |
| Risk | `RISK_TOO_PERMISSIVE`（门禁深度/标签） | 常见保密、客户边界、诚信问题选了避险且有建设性的方案 | 全 PASS 未区分直接材料风险经审查后 ALLOW；急性身体症状是具体反例。未证明所选动作总体危险 |

### Board 细节

最终 Board 的可解析八项 STATE 逐一对照 fresh observe：差异集中于 W，actions 5、8–17、28、31，共 13 次。模型把工资公告加到整数观察值上，结果虽然可解释，仍不应冒充 fresh state；不推断模拟器实际舍入机制。M6 C/无晋升、M12 C/晋 L2、M18 B/晋 L3 记录正确。旧 C 在 B 后被更新，健康恢复后 Health sticky 移除，M19 HR 转正面被记载；但 HR 轻微警告在已有后续正面消息时长期保留，不能据此证明风险始终活跃，也不能以泛泛赞许断言完全解除。

action32 的公开事件明确心慌、胸闷、手抖，Board STICKY 却只有 C。action41 把 HR 提醒归因为自研 miss，公开文字没有给出这种唯一归因。跨月 action21/47 的 EFFECTS 混入月薪、评审，不应将总差归给上一动作。Board 本身未找到数值 HiddenRisk，但 Planning transcript 有泄漏，不能给全链 PASS。Board 多次输出草稿再输出最终版增加冗余；不是 147 个 STATE 字样就等于 147 次 fresh observe。

### Planning、prior 与闭合

| CTRL/DL 指标 | 结果 |
|---|---|
| CTRL valid / closure marker | 84/84；最终 R 与 X 语法一致；仅证明 marker |
| G | ? 20；O 64；action21/M6 改变 1 次 |
| P / R / X | A 84 / PASS 84 / - 84；其余枚举均 0 |
| DL n | 0:2；1:14；2:13；3:55 |
| DL focus | NONE2；IN_PROGRESS7；DELIVERY_CLAIMED20；COMMITTED11；BLOCKED6；DELIVERED38 |
| DL evidence / recognition | NA2；UNVERIFIED44；PUBLICLY_VERIFIED38；recognition=1 共38 |

G 从 M6 的“亮点不突出”转 O，M12/M18 又有更清晰成果反馈，连续性有依据。不能因改变少而判优秀，也没有证据应强制轮换 gap。但 O 长期停滞与 Delivery verified 泛化并存，值得检验是否实际上完成了反馈闭环。

**MODE 不全合理。** 公共 H 最低 4、D 最低 5、W 最低 1；没有持续破产、解雇或信任崩溃证据。多数 A 可成立；action32 急性身体警报属于显式 safety/Health 约束，即使数值 H9 仍应按实际合同临时 S。action50 明确把生存资源回补置前但仍输出 A，也存在标签/约束不一致；它确实选择恢复，不能误写为无视健康或行动失败。

M1–M5 共20决策的 prior 审计：1 个明确 eligible（17，既有客户 owner/demo、合法展示方案，选择 demo）；2 个 ambiguous（6 的确认机制固化、12 的通用汇报准备，不能从 marker 单独证明具体可交付结果）；其余17为 correct non-trigger。可证 missed trigger=0、false trigger=0；不把“可见交付偏好”当作 prior 专属因果作用。动作17符合机制，但未单独证明来自 prior，M6 未晋也不能证明 prior 无效。

过期 prior：M6 后有明确停止使用的说明；M20 未提交的最后讨论又出现泛化的 delivery prior 措辞，同时承认首评审已过。分类 `WORDING_ONLY_LEAK`；已提交行动中 `BEHAVIORAL_LEAK` 未证。不能以未提交思考推断实际新动作。

**闭合审计方法。** elapsed 为 events 中 fresh observe result→对应 action call，精确配对84组。transcript 无 token 时间戳和 tool-call-id，采用84个最终 `**Board` / `**Risk` 块顺序对齐；从上一最终 Risk 末尾至本次最终 Risk 末尾作为有界文本段。它包含少量相邻“执行/observe”衔接语，首段也含启动说明，属于边界 proxy，不假称精确 timestamp slice；不复制思维链。83 段含显式最终 CANDIDATE 标签，1 段标签缺失，但实际84组均只提交一个最终合法 choice。

| 每决策指标 | median | p90（nearest rank） | max |
|---|---:|---:|---:|
| observe→action 秒 | 3.653 | 9.162 | 25.673 |
| 段内行数 | 32 | 86 | 267 |
| Unicode 字符数 | 1338.5 | 5867 | 17406 |
| Hmm | 1 | 11 | 39 |
| reconsider | 0 | 4 | 11 |
| Let me reconsider | 0 | 1 | 4 |

| 最长5段（按字符） | action / M | 字符 / 行 | 秒 | Hmm / reconsider / Let me |
|---|---|---|---:|---|
| 季度体力行动分配 | 11 / 3 | 17406 / 267 | 25.673 | 31/11/1 |
| 压测结果与产品预期冲突长链 | 67 / 16 | 14068 / 188 | 17.512 | 39/7/4 |
| 资深同事侵占实习生成果署名 | 61 / 15 | 12880 / 168 | 17.826 | 31/11/3 |
| 重要客户来访的接待形式选择 | 17 / 4 | 11458 / 143 | 15.766 | 16/7/4 |
| 自研内核 vs 开源方案技术选型 | 36 / 9 | 9838 / 131 | 14.179 | 19/10/3 |

全 transcript 3742 行、Hmm298/reconsider94/Let me24；action-bound proxy 为293/94/24（尾部未提交决策不算84组）。按动作归一：v7m Hmm3.49、reconsider1.12、Let me0.286；S07-40 以200成功动作约为56.15/2.10/0.60（其2次错路由和全文范围使比较仍有偏差）。全文行/成功行动44.55 vs51.42。分类 **`DECISION_CLOSURE_MATERIALLY_IMPROVED`**，但长尾仍违反“一次比较、不循环”的合同；marker closure PASS 不消除这个事实。不得声称因此提高成绩。

### Delivery 深审

从 action30/M7 起 n3 连续55行动，到 M20 未下降；初期事项包括客户确认/接待、AI规范，随后出现自研、客户延期、方法论等新事项。没有可审计的三项清单或 CLOSED 转换，不能证明55次都有三个真实活跃 item，也不能断言所有旧项从未内部关闭。marker 的无 item identity 使项替换与 focus延续不可追踪，是具体观测合同缺口。

DELIVERED+PUBLICLY_VERIFIED 的**显式 marker 首次转换只有1次**：action47/M12，由 BLOCKED 进入 verified。公开源只是客户赞许提前沟通并问能否先交核心；不是已交成果。因此该转换 supported0 / false-positive1 / ambiguous0。`recognition=1` 若指沟通被认可可成立，若指交付结果获认可则链接不成立；当前 marker 没有区分。

随后37次 marker不变不等于37次新交付。语义 focus 在 action49 明确转为方法论文章：公开事件给出文章被采用、领导要求标准化，**1个明确支持的真实结果/认可依据**。其余缺标识的 carry-forward 不能唯一绑定，记 `UNKNOWN`，不虚报38次全假或38次全真。action47–48 至少延续了客户沟通被当成交付的缺陷；action49 提供新支持不能追溯修正47。最多三活跃项与近期关闭项规则本已存在，问题为执行不符加缺乏最小 item 身份/结果锚点；不建议只增加更长说明。

### Risk challenge set

| 类别 / action | 所选行为与公开风险 | 判断 |
|---|---|---|
| confidentiality 3/7/16/20/58 | 删截图、不传播未公开信息、拒绝源代码/离职资料 | 所选动作规避材料风险，PASS 大体合理；无需因题目敏感就固定 WARN |
| client boundary 18/21/28/31 | 化解越界、向领导客观同步、留在合规招待 | 行为合理；full review 是否显式执行证据不足 |
| Health/safety 32 | 明确急性症状，立即休息/必要时就医 | 正确行动；应识别绑定约束并完整审查，PASS quick gate 过宽，ALLOW 更贴合合同 |
| compliance 41 | 拒绝暗中抄袭，延期并披露风险 | 候选处理了核心风险；不能强制 RECONSIDER |
| trust/delivery 44/47 | 及时告知延期、受控分阶段方案 | 风险有缓解，选项合理；不要把受控承诺当已交付 |
| retaliation 61/62/74/75 | 私下纠署名，失败后事实升级；面对防御性领导提出透明机制 | 有关系成本；实际报复是否达到 material 为 UNKNOWN，WARN/ALLOW 值得关注但不判固定错题 |
| offer/negotiation 70/71/73 | 真实 offer、诚实沟通、协商工作量/时间 | 无欺骗或最后通牒，PASS 可成立 |
| dignity/affordability 17/23/45 | 公司合规接待、礼貌边界、会后沟通；未见个人不可负担承诺 | 无需制造稳定 S 或机械 WARN |

结论限定在 gate calibration：至少急性症状不应被普通软成本 quick gate 吞掉。84 PASS 本身不是缺陷证明，所选动作大多已规避危险；无证据支持扩大成保守策略或固定 event-title lookup。

## Evidence discipline 与恢复

84 notes/CTRL/DL：numeric HiddenRisk=0、numeric internal score=0、DL internal marker=0；未见内部 event-id、hidden counter 或隐藏阈值数值进入行动注释。公开状态和菜单公开描述的数字不自动算违规。可见 transcript 的数值 HiddenRisk 有 **7处**（6行，324、418、644、1100、3482、3535）；既有菜单复述，也有比较高强度选项时纳入考虑。只报告类别/位置，不复制禁止的值。整体 **`EVIDENCE_DISCIPLINE_FAIL`**。零 notes 违规不能升级为全链通过；内部机制推测文字亦不作为本审计的事实。

已知 run-window llm 记录包含一次实际压缩 snapshot 响应（00:48:25.398036 +08，发生于 action73 后）。机械 parser 使用日志外层秒级 timestamp，定位00:48:25；精确时间由结构化记录补充。之后 fresh observe 和 action继续，但没有四 Skill reread 结果；`RECOVERY_PATH_FAIL`，Board/Delivery/Review Plan rebuild语义 UNKNOWN。四 Skill仅启动期读取；不能把后续格式仍正确当作完成恢复。压缩机制已发生并不证明它导致之后 transport failure。

## 改进候选：观察 → 假设，不在本任务实施

| 优先级 / 候选 | Observation → Evidence → Hypothesis | 预期收益 / regression risk | patch前需另一局？ |
|---|---|---|---|
| BLOCKING_CORRECTNESS：public-only输出 | 7处内部数值；13个W重算 → fresh whitelist直接复制与最小输出验证 | 减少污染/事实漂移；可能漏掉有用公开上下文，不能自行改接口过滤层 | NO；狭义静态合同输出 patch 可评审 |
| BLOCKING_CORRECTNESS：交付验证与item锚点 | action47沟通赞许被当交付；49才有真实采用证据 → 短item identity+实际结果/recognition链接 | 可审计、减少语义虚报；marker膨胀与历史兼容风险，保持精简 | NO；具体错误已证 |
| HIGH_VALUE：绑定约束优先 | action32症状明确、P仍A；action50自认约束仍A → 状态判断不能仅盯健康数字 | MODE/Risk语义一致；过度S可能压制成长，不能加隐藏数值阈值 | NO，需 Main 确认窄范围 |
| HIGH_VALUE：恢复执行可观测性 | 压缩后无四Skill重读 → 恢复前置条件应有独立可核验依据 | 防止靠摘要沿用旧状态；仅加提示可能无效，hook需另授权，非本次代码范围 | NO才能确认缺陷；如何修仍 UNKNOWN |
| HIGH_VALUE：Delivery饱和/关闭 | n3连续55，无item映射 → bounded替换/关闭清单 | 防 stale focus；过早关闭可能丢有效评审证据 | NO用于最小身份观测；自动关闭策略需YES |
| WATCH：decision closure长尾 | p90 5867字、max17406；总体显著改善 → 减少草稿重复与收口后复议 | 节省token；过短可能丢复杂取舍 | YES用于证明进一步策略收益 |
| WATCH：指令长度/冗余 | Board草稿重复，框架请求含大量工具描述 → 精简重复输出或提示 | 降低context；无消融，不能认定长度导致断连 | YES；仅测当前长度不能证明因果 |
| WATCH：G过粘 | O64，M12/M18反馈仍支持O → 先看实际交付闭环而非强制换G | 防目标空转；频繁换G会失连续性 | YES |
| WATCH：Risk全PASS | 存在急性例外，但多数选项已处理风险 → 修gate深度，不制造标签多样性 | 可解释性；过度保守风险 | NO用于明确例外；全局收紧需YES |
| NOT_SUPPORTED：强制更多S/换G/关键项目 | A、O、Main频次自身无错证据 | 避免无依据策略翻转 | YES且需新证据 |
| WATCH：过期prior措辞 | 未提交M20出现含混简称，但明确知道已过首评审 → 用正常review-plan措辞 | 减少误读；没有已证行为漏用 | YES，不作为主patch |
| NOT_SUPPORTED：季度每步从零重选 | 六季最终intent均吻合实际；Q6错写Q7 | 修quarter显示；无证据支持重写Energy政策 | NO可修显示，策略改动不支持 |

**最强三项**：public-state/内部数值纪律、Delivery实际结果与item身份、显式身体警报的MODE/Risk一致性。前三项属于正确性/可审计性，不声称能提高终局分数。现有规则已经说过“不要”，因此下一 patch 应保持单一窄机制和可验收输出；不能把所有 WATCH 合并成又一套长策略。

## Tooling、验证与证据保留

`post_run_audit.py` 的 score-report 现在可省略；给了路径仍要求真实文件存在。无score但fresh events/transcript及非零Runner exit时输出 partial 分类、公开轨迹、末状态、自然终止边界和 UNKNOWN score/usage。原full-run score路径及结果结构保留，新增字段为加法。另修正本次实际发现的两个 extraction缺陷：M6“半年谈话”可被识别；季度Energy不再被宽正则算为Main。新增 transcript numeric category 计数，永不输出匹配数值。

首次实证 parser pass暴露以上review/Main问题后，完成targeted修正与测试，再运行最终版本一次作为本报告机械输入；不是重跑游戏或补造score。测试覆盖无score/fresh partial/活着结束/去重/CTRL与DL/UNKNOWN分数/不得误报48m、session mismatch、full-run regression、review与Energy区分、泄漏计数去值、显式错误score路径不得静默忽略。`tests/test_post_run_audit.py`：21 passed。最终 `git diff --check` 见 TASK_RESULT。

S07-46 core archive继续保留；本地 Runner stderr、service-start.stdout 及上述run-window LLM记录是未决transport归因和恢复结论的必要来源，**FORENSIC_HOLD**，责任 S07-47/Main；Main接受独立可审结论、确认不需进一步归因且无下游依赖后才可解除。未复制或提交累计日志、秘密或DB；hash不替代源文件。S07-38既有hold不动。

最小hold身份（同上绝对源路径；LLM行按原始bytes含换行计）：

| 源 | Bytes | SHA-256 |
|---|---:|---|
| `.local/runtime/s07-46-v7m-run1/runner.stderr.log` | 3100 | `979155bfc48d67952bbfe041b381426270df84f5a7c7272af3935543a18663a2` |
| 同目录 `service-start.stdout.log` | 707243 | `5890addd2272aa545aeb959e37c480b2531e71907d515882e2a2de3197426188` |
| 实例 `logs/logs/llm.log` line3013（压缩响应） | 639992 | `24bc313406d09fe992c513ba0cc86eac864d2b28876148937bf073750bd12d40` |
| 同文件 line3039（00:49:28错误） | 245472 | `1af45b36455ddfe52d496f61d278c57317e37e7ad7ddc198ac2d5d314e441582` |

执行限制：一次Python控制台重定向导致派生显示乱码，改UTF-8后读取；一次服务stdout按UTF-8读取失败，使用已定位的行记录完成结论；首次pytest等待输出时误发了一次同范围测试（两次均离线），最终有明确21 passed输出；未改原文件或触发runtime。宽日志关键词匹配曾输出过长，随后只取结构化字段，未将这些原始片段写入报告。成本/billed usage UNKNOWN；不把服务累计token当单局账单。准确断连发起者、完整item存续、所有风险full-review深度及最终成绩仍UNKNOWN。
