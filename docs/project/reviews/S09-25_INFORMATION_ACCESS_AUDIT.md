# S09-25｜正式 Test 信息可达性与自我设限审计

## 结论与范围

**`S09_25_K1_OVERRESTRICTION_CONFIRMED_RETURN_TO_STAGE`**。

`K1_STATUS=PARTIALLY_OVERRESTRICTIVE`：冻结1.0.1官方 MCP 会向 Agent 返回季度菜单的精确 `status_updates`，包括 `HiddenRisk` 增量；当前项目把它与不可见的风险存量、内部 counters、私有 Test 数据一起排除，确实屏蔽了一个可达输入。另一方面，当前风险存量、内部图结构和统计计数确实被该 MCP 过滤，不能从上述增量恢复其真实值。

RUN16 a11 来源为 **`OFFICIAL_RUNTIME_VISIBLE`**。此前“公开接口未给出 HiddenRisk+1”的表述被原始回包反驳。RUN16 当时依据冻结项目 K1 及 Reviewer 解释触发的停止、预算消耗和回执保留；**这不建立官方 Test 规则违约**，也不把截断游戏变为完整成绩。没有撤改原始证据、回执、Candidate flags 或停止分类。

任务在 `codex/s09-14-v9a-static@2d40cd1ccecdc7ed353e26f3346d9647de13d969` 上完成，新增事实为 `IN_FLIGHT_EVIDENCE`。Main v8a `6a4037fdf2b75c105cfe0b40b93ea68d3dd0a6f3` 冻结保持。Candidate/Skills/manifest/Runner/reviewer/runtime/config 均未修改；Provider/service/game/MCP/install/reload=0。

Canonical [69项信息矩阵、16项限制库存、RUN16来源与静态校验](S09-25_INFORMATION_ACCESS_MATRIX.json) 是唯一逐项分类表；每行包含 Plan 要求的14列及 qualification。本报告提供解释，不维护另一套逐项结论。

## 来源优先级与正式 Test 的验证边界

1. Source Lock：`OFFICIAL_SOURCE_LOCK.md:70`，冻结 Runner `f61c738`、模拟器1.0.1、数据包1.0.0。它明确区分官方事实与项目执行约定。
2. 当前重新读取的[锁定官方 README](https://github.com/openJiuwen-ai/CareerSim-BDCI26/blob/f61c738c72e51b77298cc1c14c7c6ebf4b6c527d/README.md)确认五个游戏工具及 agent 模式的工具、Skills、MCP 与被动记忆能力；未发现以字段名称禁止使用 tool-returned 数据的规则。
3. [官方发布的1.0.1 wheel](https://pypi.org/project/career-emulator/1.0.1/) SHA256 `56669c425a920fe0fa6c933671ccbce1c841399e3d78609403dfccbd96d23a37` 校验通过；7个相关本机接口/序列化/日志文件与该 wheel **逐字节相同**。只下载并读取源码副本，没有安装、更新或执行 engine。
4. RUN16 精确 held events/transcript 校验与既有 hold hashes 一致；只解析模型工具回包、选择和已产生的文本。
5. 项目规则/历史最后解释，不能压过实际官方工具回包。

**矩阵 `test_access=YES` 的范围是锁定1.0.1官方提交 Agent 的可用接口路径，不声称本次访问了线上 Test。** Hosted Test 的实际部署版本、文件系统隔离、额外禁用字段/工具和预算目前 UNKNOWN。ReadTheDocs Handbook/MCP 页本次不可达，直接文档读取返回403；XIR1165当前完整规则未能刷新。未用其它赛事/年份规则替代。`official_prohibition=NO` 指所检查 README、公开包及返回手册中未发现该项专门禁令，不等于证明所有未取得的规则均无禁令；私有数据/解码权限等项保留 UNKNOWN。

完整当前规则或云端部署可通过未来授权的只读官方证据复核；若必须调用实际 Test/runtime 才能确认，标为 `REQUIRES_FUTURE_AUTHORIZED_RUNTIME_PROBE`，本次不执行。上述未决项不妨碍确认当前1.0.1可达性和 RUN16 实际来源。

## 官方输入路径

| 路径 | 实际返回 / 行为 | 不可混同的内容 |
|---|---|---|
| `new_game()` | session_id/error | 非任意跨局授权；比赛 mode 源码限制一次创建 |
| `observe(session_id)` | 状态、事件语义、合法选择、events；季度菜单含 effects | 当前风险存量与季度风险增量分开；Story 和季度选择序列化不同 |
| `take_action(session_id,choice,notes)` | success/error | 不是 career result 或新鲜状态 |
| `show_employee_handbook()` | Markdown 规则、范围、方向、工资/奖金表、反馈推断说明 | 不提供具体晋升阈值/绩效指数/随机概率；不能据此伪造精确公式 |
| `check_latest_logs(session_id,count=10)` | 该 ID 的近期日志 entries 和 log_file | 日志事实、configured effect、Agent notes、当前状态分开 |

具体实现见矩阵 sources：`server/tools.py:20`、`server/models.py:72/163/233/386`。状态 H/D/S/N/O/W/L/E/tenure/time/flags 可达；事件 title/description、季度 rules/remaining_energy/energy_budget/max_selections 保留。`event_id/node_id/doc_id/event_type/decision_type`、choice graph identifiers被过滤，不能把 title 语义判断当成内部ID查答案。

### status_updates 的五种来源

- **季度 observe**：`RegularActionDefinition.to_choice` 输出原始 status_updates；`_strip_mcp_choice` 只删 action_id/next_node/consequence_index，未删 effects 或其中 HiddenRisk。这是当前实际 Agent 输入。
- **Story observe**：`EventChoice.to_choice` 不返回 status_updates；未来 Story effect 在数据对象中存在不等于模型提前收到。
- **Handbook**：effects 去 hidden 字段并只渲染正负方向，不渲染数值大小。
- **合法 action logs**：生成的 action 行包含非hidden的配置数值变化；不是实际 clamp/结算后的差分，须 fresh observe 验证。
- **raw数据/DB/Runner文件**：需要另外证明 Test Agent 路径。Codex读到的载体不能自动成为可部署运行依赖；但载体内记录的官方 tool response 有独立官方输入来源。

advertised/configured effect 与 realized effect 始终分开；精确输入可用于排序研究，不保证每次真实增长，也不证明隐藏 cap 或失败阈值。

## check_latest_logs 第一类官方通道审计

`server/tools.py:46` 注册，`game.py:271` 返回：

```text
{session_id, log_file, count, entries:[{session_id, entry_type, message}]}
```

未知 session 返回 error。count默认10，store取 `max(1,count)`，从该 session 最近记录中取样后按时间顺序返回；检查的实现未设显式最大count或工具调用配额。不能推广为云端无成本/不限次。

日志类别由 engine 的写入路径产生：system/init、action、终结链节点、warning/failure、绩效/工资/晋升相关通知、terminal ending_score。公开反馈内容按数据配置传入，不额外保证数字字段。日志保留先前被 observe 一次性取走的 warning，恢复时也能读到历史终结链/行动文本。

`action_log.py:6` 的自动 effects 文本跳过 key 以 hidden 开头的项；非hidden项输出精确配置 delta。用户 notes 原样追加，故“日志里出现 HiddenRisk”可能只是 Agent 自己写入，**不是新的独立风险测量**。terminal ending_score 是另一类结束后内容，不能当作 active-game 风险存量查询。

`load_latest_logs`按提供的 session ID 过滤，但没有“只能查询 Agent 当前 session”的鉴权比较；自己的会话历史可用不意味着别人的 ID 可用/获准。`log_file` 是服务器路径提示，不证明 hosted Agent 可以直接读那个文件。`logs://{session_id}` resource存在，但 locked Agent 的resource读适配/云端权限未经验证；无需它即可使用已确认的 logs tool。

读取日志不推进月份或执行游戏选择；实现会调用 store.initialize，可能初始化/迁移数据库表，故不声称整个文件系统绝对无写入。它不请求模型；Agent决策仍会产生工具/上下文/模型token与延迟成本。RUN16没有调用该工具，因此本次日志schema/过滤结论是源码及纯函数证据，不伪造一份实测回包。

官方 `prompts/identity.md:29` 和 continuation prompt 已推荐用 logs恢复；现有项目也允许少量同局公开logs，但 Board输入主要将其限制在recovery。不能把“logs是DB存储的”误写成“Agent不能合法调用logs工具”。

## RUN16 a11 / a24 来源重建与纠正

精确 source：`D:/CS/CareerSim/.career_sim_runner/career_emu/outputs/local-s06-adaptive-controller/20261002T160103Z/`。events SHA256 `4115aa6d118c29fca4b5be6f051bb21e6c630c9043cbd1b0b7087d6bcc96e75e`；transcript SHA256 `81a4af9116809b88448ff9e8d7059dba39f76876a896c884227b4af08ee54e05`。

| 环节 | 精确证据 |
|---|---|
| a11前observe | seq107，UTC16:02:24.332961；tool_result 的 raw_output.result 是真实 MCP 返回 JSON |
| 高强度选项 | `choices[0].status_updates={Output:2,Health:-1,Dignity:-1,HiddenRisk:1}` |
| 清理选项 | `choices[3].status_updates={HiddenRisk:-1}` |
| 当前状态 | H4/D10/S9/N2/O0/W1/E3/L1；**没有hidden_risk存量** |
| 模型实际使用 | transcript378/386/428/485及518行讨论同一 +1 与成本组合 |
| a11提交 | seq109，UTC16:02:41.909462，choice7 notes含`(还带HiddenRisk+1)` |
| Reviewer packet | `scripts/live_review_packet.py:81`仅保留choice/action/description/energy_cost；遗漏status_updates及其它规则字段 |

值在 action 前已由官方工具送入上下文，数值来源不需要借助Skill、跨局summary、DB、Provider日志或本地人工注入来解释。没有证据支持 DEV_ONLY_LEAKAGE/MODEL_INFERENCE_OR_HALLUCINATION。Handbook隐藏了该增量，但这不抹去另一官方工具明确输出它的事实。

a24前另一季度observe（seq211/212重复记录，a24提交seq213）也给出同一增量与定性风险描述；a24 notes仅用风险措辞，未提出精确当前存量。单独分类为 `OFFICIAL_RUNTIME_VISIBLE_QUALITATIVE_USE`，不升级为另一个伪造数字案例。seq/notes保存在矩阵 provenance。

**纠正范围**：RUN16记录与H2回执中“numeric risk claim absent from participant-visible menu”是不完整投影造成的错误事实判断。语义notes仍与当时项目的字段禁用合同/解释冲突，停止操作真实发生，未恢复游戏；不追认官方作弊、不删除旧回执、不重算分数、不替换旧artifact。Reviewer的schema-validator PASS只校验receipt结构，不能证明public_evidence涵盖完整Agent输入，也不能证明项目条款等于官方规则。该来源完整性问题交Stage处理，本次不patch Reviewer。

## 历史限制库存

库存计数采用16个语义限制类，不数每个重复字符串/版本实例：**16项目自设，0项找到明确官方“禁止使用”条文，9项可能过度收紧**。这不表示16项都应删除，也不表示官方完全没有限制。隐藏state/ID的实际过滤、私有Test隔离和fresh安装清理为若干限制提供了接口/可迁移性依据。

| 库存 | 形成/加固与影响版本 | 原因与审计结论 | 潜在分数影响（假设） |
|---|---|---|---|
| R01 PUBLIC_INTERFACE_ONLY | AD-007 `4372921`（2026-09-25）；标签S07-03 `aebd599` | public interface方向合理，不能自行缩成仅可见prose | POSSIBLE |
| R02 HiddenRisk数值/名称 | S07-36 `8f14064`，v7h→v10f | 明写“even when tool exposes”；覆盖了合法季度delta | MATERIAL_PLAUSIBLE |
| R03 hidden counters | 同上 | counters在MCP状态中确实移除；不要求策略依赖 | NONE |
| R04 internal score | 同上 | active组件未提供；terminal score需另分类 | UNKNOWN |
| R05 internal event id/effect | AD-007及S07-36 | ID过滤和正常返回effects不能捆绑 | MATERIAL_PLAUSIBLE |
| R06 unclear status_updates | S07-36 | “until verified public”有合理保留；当前serializer验证可解除此项不确定性 | MATERIAL_PLAUSIBLE |
| R07 decoded Dev规则 | AD-007 | S06-09 quarantine为项目决定；公开数据分发不自动解决解码/答案表权限 | UNKNOWN |
| R08 thresholds/weights/formula推断 | v6b既有，AD-007正式化；v10a强化 | 不能把反馈驱动的校准推断与伪造精确事实混同 | MATERIAL_PLAUSIBLE |
| R09 event/title→answer | v6b/AD-007 | 私有Test查表保守禁止；公开Dev精确记忆的权限/泛化仍需调查 | UNKNOWN |
| R10 runtime跨局memory | v6b/v7/S07-36 | install清memory/session，无可靠fresh传递 | NONE |
| R11 Dev/private wording | v10a `0cecffd`至v10f | “禁Dev evidence”与C5 donor prior共存；不能排除所有合法离线学习 | MATERIAL_PLAUSIBLE |
| R12 Board logs仅recovery为主 | v7→v10f | 是成本/精简取舍，可能错失及时官方历史事实；未证明实际漏报 | POSSIBLE |
| R13 growth cap必须明确公开 | v7z、v10a、v10c；v10f纠偏 | 防止伪造cap合理；合法经验hypothesis范围可能过窄 | POSSIBLE |
| R14 K3 numeric-only S | v7x及v10c明确化 | 过度稳定化纠偏；无直接禁止日志warning | UNKNOWN |
| R15 DB/raw取证 | AD-007/AGENTS | Test可达性未证，shared/private风险；保留排除 | NONE |
| R16私有Test/凭据/外部干预 | Source Lock/AGENTS | 保留保守边界；完整当前禁令文本仍UNKNOWN | NONE |

S07-01报告明确记载当时没有重新读取官网，而使用Source Lock与项目已接受合同；由此不能把该报告的部署边界冒充官方明确禁令。S07-36是字段级禁用的直接实施点；v10c `55157f5` 把旧禁用放进常驻K1，v10e/v10f加了证书与窄CAP，但未重新证明HiddenRisk delta不可达。

## Dev学习先验与 Test输入必须分开

[官方数据包1.0.0](https://pypi.org/project/career-emulator-bdci26/1.0.0/)向参赛者提供Dev题库/配置分发入口。官方提交以Skills/manifest输入策略，当前安装把它们放进 Agent上下文；这证明存在合法的**离线作者知识传递机制**。运行时不能直接观察的机制，不因此自动禁止被合法Dev实验学成prior。

但“官方分发Dev”没有单独证明：可以解码全部隐藏配置、可以使用私有Test、可以建完整事件答案表、或该精确表会泛化。公开数据文件名/加载代码只作来源审计，本次没有解码任何.data内容，没有复制隐藏阈值/公式。一般资本/成本响应、反馈校准、机会语义先验可被研究并保持uncertainty；source-derived精确阈值、当前隐藏计数、私有Test映射分别保留未知/禁止依赖边界。

Handbook明确允许从反馈推断未直接公开的机制；这支持**推断资格**，不支持有限样本下精确阈值的真实性。当前Planning C5承认donor prior，因此不是所有Dev先验已被禁；问题是同段Dev/private、hidden formula一刀切措辞可能排除有证据的一般推断。

动态memory是另一机制：锁定install清理memory/*.md、sessions等，并重建MEMORY.md；不得期待上局残留。正式平台多次样本间生命周期仍UNKNOWN，不能依赖另一Test局结果或外部数据库。公版README的被动memory能力也不等于允许跨局内容泄漏。

## Candidate影响（只审计，不实施）

| 部位 | 结论 | 应交Stage的边界 |
|---|---|---|
| K1 | **PARTIALLY_OVERRESTRICTIVE** | 已验证官方返回的季度effect/delta与不可达stock分开；不按字段名禁用 |
| K2 | 防伪造cap合理；经验prior准入范围过窄 | 允许证据分级的hypothesis，不把一次NO_GAIN当hidden cap事实 |
| K3 | 无直接logs禁令；受K1证据准入限制 | 显式same-session log warning同样可成为fresh binding证据；numeric delta不自动等于危机或S授权 |
| Board | 部分过窄 | STATE仍只抄fresh状态；known action delta/log fact另记，不合成未知风险存量；recovery-only日志取舍可研究 |
| Planning | 部分过窄/措辞矛盾 | exact advertised effect可排序，actual observed优先；保留合法Dev一般prior，不宣称保证增长 |
| Risk | known delta禁用过窄 | 风险增量和公开warning可辅助selected candidate评估；不制造hidden stock/触发概率 |

## 机会与未来政策建议

`SELF_RESTRICTION_SCORE_OPPORTUNITY=HIGH`，是研究机会级别，不是预测加分或因果结论。

优先级前三：

1. **季度官方effect metadata**：比较成长、资源和risk delta，降低边际收益误判和Energy浪费；同时保留观察后NO_GAIN修正。潜在价值高，方向/分数均未经新实验。
2. **同局官方logs**：恢复warning/承诺/延迟结果及配置effect，区分模型notes与独立事实；可能减少尾部失误和交付遗失。必须控制token/调用成本。
3. **合法Dev一般prior与反馈推断**：改进Review-window资本组合和机会判断；保留样本/迁移置信度，不建立私有Test答案查表。

推荐的未来准入过程：先查官方渠道、实际模型接收及官方禁止条款；可达且未被官方禁止的数据进入研究候选；不可达数据不得作为运行必要条件；UNKNOWN单列调查，不先永久BAN。每个fact/prior分别记录来源、scope、freshness、配置/实际、置信度和迁移风险。当前合同修改、Reviewer完整输入保留、后续利用实验都需要新的Stage任务；本任务没有实施该规则。

RUN16实际模型已经使用了该delta，因此不能说“模型完全没看见/没用”。已证的是项目预期合规策略的准入边界与停止依据收得过窄；若允许该来源会怎样改变排序、成本和最终分数，仍需独立实验，不能从这次截断反推最优选项。

## 验证、未决项与交付

19项pure serializer/formatter/provenance断言通过；不实例化engine/Store，不加载数据、不调用工具。包括state隐藏值过滤、图ID过滤、季度HiddenRisk delta保留、手册方向化、日志hidden过滤、notes来源边界和RUN16投影遗漏。7文件官方wheel身份一致，精确held两个来源hash一致。所有所选交付文件执行bounded secret scan、JSON14列/枚举/source引用完整性及`git diff --check`。

完整当前竞赛禁止条文、hosted Test版本/资源/文件访问、decoded公开Dev规则/精确事件记忆权限、云端跨局memory、Provider metadata、resource logs:// adapter仍UNKNOWN。没有为解决这些未知执行live probe；它们不被虚填为ALLOW。

源码副本位于 `.local/upstream/career-emulator-1.0.1/`，可重建；一次性纯离线校验器不提交。RUN16唯一raw与原回执继续FORENSIC_HOLD，负责人Stage/Main，未解除或清理。CURRENT_STATE只更新已直接核验的来源纠正与审计事实；未来政策建议尚未被Stage接受。其他合同/validation flags/main freeze不变。

`NEXT_GAME=NOT_AUTHORIZED`
`MAIN_V8A_FREEZE_UNCHANGED`
