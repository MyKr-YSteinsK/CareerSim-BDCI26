# S05-03｜最终候选下一局观测矩阵（预注册；未授权运行）

本矩阵在下一次 game 前冻结，继承并取代未来观测用的 [S05-02 matrix](../S05-02-integrated-offline-optimization/benchmark_observation_matrix.md)；不改写父历史件。未来仅 Main Game Gate 可授权安装、服务、provider 和对局。先核 final manifest 四 Skill blob、Runner/lock、drive 与 CareerSim game ID；所有决策只使用当时可见 `observe`/event/legal choices/checkpoint。终局 score、raw metadata 只用于**事后**评价。

统一状态：`PASS`＝触发出现且证据显示合同响应；`FAIL`＝触发出现且证据证明违反；`NOT_OBSERVED`＝触发/检查点未出现、机制未纳入或对局提前结束；`UNKNOWN`＝触发或响应的必要来源缺失/矛盾。未触发不得写 `FAIL`，缺证不得写 `PASS`。下表每项的单局限制相同：只检实际路径与执行可见性，不能证明稳定 80+、因果效果、尾部分布或 Hidden Test 泛化。不存在某项触发时仅记 `NOT_OBSERVED`；不为补齐矩阵追加游戏。Memory/rubric 本候选未采纳，非使用不是机制失败。

| 观测项 | 未来证据来源与测量 | 应判 PASS / FAIL 的特定边界；未见触发/缺证按统一状态 |
|---|---|---|
| 长程 Skill adherence | timestamped Skill registry、`skill_tool`/`read_file`、transcript/checkpoint；按 M1–12、M13–30、M31–48 分窗记四 Skill 读取/使用与策略边界。 | PASS 为窗口内应触发的职责有可追溯执行；FAIL 为明确触发且正文/职责违背。单一 load count 不能证明遵循或失效。 |
| 继续/压缩/恢复 | Runner continue/auto-continuation 事件、framework compression event（若可得）、same drive/game ID、fresh `observe`、Planning 重新读取及 checkpoint。 | 触发且重读、fresh observe、旧目标不明则 unknown 为 PASS；未刷新或借旧局目标为 FAIL。无可确认压缩/continue 为 NOT_OBSERVED，压缩日志缺失为 UNKNOWN。 |
| Board freshness | 每个代表性行动前后 game ID、public observe timestamp、Board observed/inferred/unknown/source。 | 当前 `observe` 优先且同局、不把猜测升级为 observed 为 PASS；旧月/异局状态覆盖新 observe 为 FAIL。 |
| Memory write/read/recovery | final manifest、tool calls、workspace path；本候选 Memory=`DEFER`。 | 本候选不期待 write/read，未发生则 `NOT_OBSERVED`；若意外出现持久读取，核对是否污染并报告，不将其算为采纳成功。 |
| 跨 session 污染 | 当前与先前 game/drive ID、Board/Planning checkpoint 和正常动作输入。 | 新 game 不继承旧 objective/risk consequence 为 PASS；实际异局引用为 FAIL；只有单局且无污染检查机会为 NOT_OBSERVED。 |
| 严重后果重排 | 公开严重 warning/consequence、旧新 Priority、合法路径及五因素 trade-off。 | 触发时重新审查并根据公开证据更新/确认目标为 PASS；无审查静默沿用为 FAIL。 |
| 复合收益与 Energy 成本 | 季度 fresh public state/gap、合法 Energy 菜单及可见成本、Planning `Path trade-off`、所选动作。 | 有用分量与成本均比较为 PASS；单一满值取消全选项或无成本地偏好复合标签为 FAIL。 |
| 先前目标进展与平台复核 | 上一 checkpoint 的目标、fresh public metric/反馈、重复动作、合法替代、`advancing/stalled/unknown`。 | stalled 比较替代及成本、advancing 可继续、证据不足标 unknown 为 PASS；未经复核重复或无证推断晋升阈值为 FAIL。 |
| 晋升准备的公开信号 | 半年反馈、Level/CurrentLevelDuration、Skill/Network/Output、可见机会措辞、同局目标。 | 若此机会出现，Planning 用公开差距/进展审视路径、不保证晋升为 PASS；使用隐藏阈值/“到月必晋升”为 FAIL。专门规则未采纳，不要求额外报告。 |
| 财富机会的公开权衡 | 合法且明确财富相关选项的可见收益/损失、资源成本、Planning trade-off。 | 若遇到，公开收益与机会成本一起考虑、无固定财富动作/score 权重为 PASS；只凭终局 headroom 选项为 FAIL。专门规则未采纳。 |
| 高影响 rubric / 误报 | rubric 未采纳；保留 public severe trigger、Planning/Risk 记录与低影响普通事件样例。 | rubric-specific 未出现记 `NOT_OBSERVED`；既有严重后果由上项判断。普通事件若被新增二审拖入常驻风险流程，按普通成长 false positive 记 FAIL。 |
| 正常成长 false positive | 公开低风险成长事件、是否强行触发严重后果重排/额外 Risk、最终选择。 | 无无根据保守默认或第二 reviewer loop 为 PASS；有明确反例为 FAIL。 |
| 角色重叠与 reasoning drift | 同一决策的 Board、Planning、Risk、Trace 内容；代表性长推理/状态重述、token/runtime。 | Board 只事实、Planning 只目标/权衡、Risk 只候选警告、Trace 只 marker，checkpoint bounded 为 PASS；显著重复循环或越权为 FAIL；不可把长 transcript 自动归因 Skill。 |
| M6 / M12 / M18 / M24 | 各月最后 fresh public `observe` 的 Level/Wealth/Skill/Network/Output/Health，季度 Energy/main action、反馈。 | 六字段/来源/时间正确保留为 PASS；错报为 FAIL；未达到该月为 NOT_OBSERVED。旧 S04 仅事后描述比较，不作为选择输入。 |
| M36 / M48 | 同上六字段、升职时间、反馈、当前目标/继续恢复轨迹；若到达。 | 同里程碑规则；未达到不得插补。M48 终局值与此前 public observe 分开。 |
| 晋升 timing / Level / Wealth | 每次可见 Level 变化月、公开反馈及 Wealth 同月/相邻月变化。 | 记录来源、同步变化只作描述为 PASS；误称薪酬/晋升因果或隐藏阈值为 FAIL。 |
| 最终 score/survival/grade | 终局 score report、events、最后 public observe；分维度、量化/partial、月份、grade 与 failure class。 | 来源及算术一致为 PASS；误报或以前期未知终局解释早期选择为 FAIL；未完成报告为 NOT_OBSERVED/UNKNOWN。 |
| token/runtime/cost | Runner/provider usage、by-model input/output/total/cache、service/Runner wall-clock、reported cost。 | 全部可得值按来源记录且缺失明示为 PASS；将未报告 cost 当零或漏记为 FAIL。 |
| technical vs game failure | Runner exit、service/MCP/provider logs、game session/events、终局报告。 | 可分技术失败、淘汰、timeout/unknown side effect 且不盲重试为 PASS；分类越证据为 FAIL。 |
| Single Agent authority | drive/game ID、Skill 输出、实际 `take_action` tool calls 与提交者。 | 始终一个 Agent，Skill-direct submit=0，成功动作不重复为 PASS；多提交者/越权为 FAIL。无动作则 NOT_OBSERVED。 |

未来观测不允许为补缺项增加模型测试、聊天、第二局或额外 benchmark。一次 game 即便所有已触发项 PASS，也只证明该路径的执行正确性，**不**证明 Score 80+ 稳定、机制因果收益或 S05 完成。
