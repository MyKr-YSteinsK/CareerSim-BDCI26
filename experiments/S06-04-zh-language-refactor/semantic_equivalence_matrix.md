# S06-04 语义等价矩阵

Source candidate：`candidate-v3b-final-policy`，其四个 Skill 与 runtime instruction 的 Git identity 见本任务 `candidate_manifest.json`。本矩阵逐项对照 v3b 已接受规则与 v3c 中文表达；`EQUIVALENT` 表示语义、触发条件、边界和权限均保持，不表示运行时遵循或 gameplay 收益已验证。

| ID | v3b 原语义 | v3c 中文语义位置 | Control Token | 等价性 | Notes |
|---|---|---|---|---|---|
| CT-01 | 每次 `take_action` 前立即使用 | Trace／何时使用 | `take_action` | EQUIVALENT | 时点不变 |
| CT-02 | 正常决策已选 choice 不得改变 | Trace／必须执行第1项 | `choice` | EQUIVALENT | 不增加重选权 |
| CT-03 | 保留原 concise reason | Trace／必须执行第2项 | `notes` | EQUIVALENT | 不删改理由 |
| CT-04 | 末尾精确追加一个前置空格的 marker | Trace／必须执行第3项 | `[S02_SKILL_USED]` | EQUIVALENT | 字符串及空格不变 |
| CT-05 | 空 notes 时仅写 marker，不加前置空格 | Trace／必须执行第3项 | `[S02_SKILL_USED]` | EQUIVALENT | 空值例外不变 |
| CT-06 | 通过现有工具只提交一次 | Trace／必须执行第4项 | `take_action` | EQUIVALENT | 次数不变 |
| CT-07 | 仅为轨迹标记，不选项、不排序、不改策略/状态 | Trace／边界第1项 | — | EQUIVALENT | 责任仍为 marker-only |
| CT-08 | 不负责 new_game、observe、终止处理；不建新 Agent、submitter、Memory、Planning、Risk state | Trace／边界第2–3项 | `new_game`, `observe`, `take_action` | EQUIVALENT | 调用与架构边界保留 |
| RR-01 | 在同一 Agent 提交动作前审查最新公开证据 | Risk Review／职责 | `Single Agent` | EQUIVALENT | 主体与证据时点不变 |
| RR-02 | warning-driven / event-driven，不是 always-on | Risk Review／职责末句、触发条件 | `risk-review` | EQUIVALENT | 不变成常驻审查 |
| RR-03 | 显式风险、埋雷、信任/危机、绩效警告可触发 | Risk Review／触发条件第1–4项 | — | EQUIVALENT | 原触发类别全保留 |
| RR-04 | 相关警告存在且当前合法选项给出对应缓解时可触发 | Risk Review／触发条件第5项 | — | EQUIVALENT | 必须同时具备关联警告与合法缓解 |
| RR-05 | 按文本含义判断；不猜关键词数、隐藏计数/阈值、概率、局后分数或风险数值 | Risk Review／触发条件末段 | `UNKNOWN` | EQUIVALENT | 无隐藏量推断 |
| RR-06 | Material Risk 包含严重 Health、信任、保密/合规、报复/升级、终止/生存及其他重大后果 | Risk Review／Material Risk 与 Soft Cost | `Material Risk` | EQUIVALENT | 类别未削弱 |
| RR-07 | Soft Cost 包含少量 Health/Dignity、时间、普通摩擦/压力、不确定性 | 同上 | `Soft Cost` | EQUIVALENT | 类别不变 |
| RR-08 | Soft Cost 单独不是 RECONSIDER 触发，也不自动否决高收益成长 | 同上 | `RECONSIDER` | EQUIVALENT | 软成本保护边界不变 |
| RR-09 | 两类并存时完整审查，不折扣 Material Risk | 同上 | `Material Risk` | EQUIVALENT | 重大风险保护不变 |
| RR-10 | rolling-planning 拥有战略 Risk Budget；Risk 只看当前候选 | 同上 | `Risk Budget`, `rolling-planning` | EQUIVALENT | Skill 职责不变 |
| RR-11 | 输入仅为已有最新 observe、公开状态/事件/反馈/选项及公开 Handbook | Risk Review／输入 | `observe` | EQUIVALENT | 可见输入集合不变 |
| RR-12 | 不建 Memory，不用其他 session 的过期信息 | Risk Review／输入末段 | `Memory` | EQUIVALENT | 无跨局状态 |
| RR-13 | 输出恰好一个轻量状态及简短证据说明 | Risk Review／输出状态 | `ALLOW`, `WARN`, `RECONSIDER`, `UNKNOWN` | EQUIVALENT | 单状态合同不变 |
| RR-14 | ALLOW：当前证据不足以因重大风险要求改候选；Soft Cost 不单独改选 | Risk Review／ALLOW | `ALLOW` | EQUIVALENT | 含义一致 |
| RR-15 | WARN：有风险但无明确低歧义合法缓解，或证据不足；只警告不强制换动作 | Risk Review／WARN | `WARN` | EQUIVALENT | 不升级为强制门 |
| RR-16 | RECONSIDER 仅在重大风险明确、直接缓解选项合法、候选未处理三项同时成立 | Risk Review／RECONSIDER 三项 | `RECONSIDER` | EQUIVALENT | 三个必要条件全部保留 |
| RR-17 | RECONSIDER 只要求同 Agent 再比较一次，不等于选最保守动作 | Risk Review／RECONSIDER 末句 | `Single Agent` | EQUIVALENT | 再审次数/选择权不变 |
| RR-18 | UNKNOWN 覆盖 session/状态/选项/证据缺失、过期、含糊或不足；回正常流程，不阻断/补造 | Risk Review／UNKNOWN | `UNKNOWN` | EQUIVALENT | 回退方式不变 |
| RR-19 | 仅在合法选项确有“处理历史埋雷”且有相关公开警告时提及，效果未知 | Risk Review／特殊规则 | `处理历史埋雷` | EQUIVALENT | 不编造效果 |
| RR-20 | 不虚构该动作、不声称单次消除风险、不设警告计数阈值、不季度无条件选择 | Risk Review／特殊规则 | — | EQUIVALENT | 防 overclaim 边界保留 |
| RR-21 | 可请求同 Agent 比较候选，但 Can Submit Action 为 No | Risk Review／动作权限 | `Can Submit Action: No` | EQUIVALENT | 权限不变 |
| RR-22 | 不调用工具；正常 observe→选择→触发审查→同 Agent 决策→take_action；无额外 Agent/Team/Swarm/持久状态 | Risk Review／动作权限 | `observe`, `take_action`, `new_game` | EQUIVALENT | 单一 submitter 不变 |
| RR-23 | 新鲜依据无法建立时返回 UNKNOWN，不拦截正常决策 | Risk Review／失败回退 | `UNKNOWN` | EQUIVALENT | fallback 不变 |
| RR-24 | Skill 实际运行才在最终 notes 精确追加一个匹配 marker，并保留原理由与 S02 marker | Risk Review／轨迹标记 | `[S03_RISK:*]`, `[S02_SKILL_USED]` | EQUIVALENT | 四 marker 与前置空格不变 |
| SB-01 | 只为当前 CareerSim 单局维护精简工作板，供同一 Agent 恢复上下文 | Board／职责 | `game_session_id` | EQUIVALENT | scope 不变 |
| SB-02 | 不是全局/跨局 Memory、Planner、风险策略、隐藏状态估计或 submitter | Board／职责 | `Memory` | EQUIVALENT | 非职责保持排除 |
| SB-03 | 成功 new_game+首个有效 observe、重大新鲜状态变化、确认回执后新 observe、context loss、板缺失/过期/歧义/错局时刷新 | Board／触发条件 | `new_game`, `observe` | EQUIVALENT | 所有触发情形保留 |
| SB-04 | 不按每 token/日志行更新；仅留当前决策所需信息，无限历史禁止 | Board／触发条件末段 | — | EQUIVALENT | 仍有界 |
| SB-05 | 输入含 new_game 返回或 observe 确认的 CareerSim game session_id | Board／输入第1项 | `session_id`, `game_session_id` | EQUIVALENT | 游戏 session 定义不变 |
| SB-06 | 输入限最新 observe 的 current_state/事件/反馈/合法选项及确认回执 | Board／输入第2–3项 | `current_state`, `observe`, `take_action` | EQUIVALENT | 来源不扩张 |
| SB-07 | context loss 必要时至多看同局最近五条公开日志，最多恢复两组战略效果 | Board／输入第4项 | `recent_effects` | EQUIVALENT | 两个上限不变 |
| SB-08 | drive/conversation ID 不是游戏 session；禁止隐藏/局后/数据库/本机取证/他局数据及未确认猜测 | Board／输入末段 | `game_session_id` | EQUIVALENT | 隔离与公开边界不变 |
| SB-09 | 状态板字段及嵌套名精确保留 | Board／状态板格式 | `game_session_id`, `game_time_or_phase`, `observed`, `inferred`, `unknown`, `recent_effects`, `action`, `target_or_relevant_field`, `before_after`, `source`, `source_or_freshness` | EQUIVALENT | 字段名逐字保留 |
| SB-10 | observed/inferred/unknown 分离；警告可观察，严重度/原因/后果/建议不是直接事实 | Board／状态板格式说明 | `observed`, `inferred`, `unknown` | EQUIVALENT | 事实层级不变 |
| SB-11 | 输出当前对话中的简洁替换板；空项可省略/none，不为填格式补造字段 | Board／状态板格式 | — | EQUIVALENT | 输出范围不变 |
| SB-12 | 新鲜权威 observe 优先；回执只记录其确认内容，预测仍为推断/未知 | Board／更新规则第1项 | `observe` | EQUIVALENT | freshness 优先级不变 |
| SB-13 | context recovery 先确认游戏 session 并 fresh observe，再按需用最多五条日志恢复可直接确认的可比 pair | Board／更新规则第2项 | `game_session_id`, `observe` | EQUIVALENT | 顺序、范围及用途不变 |
| SB-14 | 恢复最多两组；不直接确认/不可比时 UNKNOWN 或省略，不回放历史/查答案 | Board／更新规则第2项 | `UNKNOWN` | EQUIVALENT | 限制不变 |
| SB-15 | recent_effects 最多两条；只记录确认动作及直接可比的前后公开值 | Board／更新规则第3项 | `recent_effects`, `before_after` | EQUIVALENT | 上限与证据门槛不变 |
| SB-16 | 中间动作/事件或其他合理原因造成归因歧义时 UNKNOWN/省略，不从顺序推因果 | Board／更新规则第3项 | `UNKNOWN` | EQUIVALENT | 无因果升级 |
| SB-17 | recent_effects 仅事实，不评好坏/推荐动作/拥有 Gap；Planning 负责进展判断 | Board／更新规则第4项 | `Primary Gap`, `rolling-planning` | EQUIVALENT | 职责分离不变 |
| SB-18 | 推断不能覆盖 observed；保留根据，并随新证据删除/降级 | Board／更新规则第5项 | `observed`, `inferred` | EQUIVALENT | 证据更新规则不变 |
| SB-19 | session mismatch 丢弃旧板；新 game session 即使 conversation 延续也从空板开始 | Board／更新规则第6–7项 | `game_session_id` | EQUIVALENT | 跨局隔离不变 |
| SB-20 | session/证据缺失或 context loss 后无板时标 unknown，由 Agent 正常获取新 observe 后再恢复；不猜 ID | Board／更新规则第8项 | `unknown`, `observe` | EQUIVALENT | fallback 顺序不变 |
| SB-21 | 仅当前快照与决策所需少量事实；不建 transcript/无限历史 | Board／更新规则第9项 | — | EQUIVALENT | 状态有界 |
| SB-22 | Board 只返回状态，不调用 new_game/observe/take_action、不推进阶段；Single Agent 唯一提交者 | Board／正常流程与权限 | `new_game`, `observe`, `take_action` | EQUIVALENT | action authority 不变 |
| SB-23 | 不加 Agent/Team/Swarm/Planner；Trace marker、选项与 notes 职责不变 | Board／权限末项 | `[S02_SKILL_USED]` | EQUIVALENT | Trace 分工不变 |
| SB-24 | 状态板是同 drive conversation 内非持久工作上下文；不写文件/Memory/Runner/DB，不假定压缩或云端保留 | Board／持久化边界 | `Memory` | EQUIVALENT | 无持久化扩张 |
| SB-25 | 风险解释归 Risk；unsupported facts unknown/omit；状态板不阻断/不建议动作 | Board／兼容与回退 | `risk-review`, `unknown` | EQUIVALENT | fallback 职责不变 |
| RP-01 | 首次有效观察后读完整 Skill 并做详细初始规划 | Planning／使用时机第1项 | `rolling-planning` | EQUIVALENT | 初始化触发保留 |
| RP-02 | 每季度首次 Energy 前用新鲜公开 observe 刷新/创建 checkpoint | Planning／使用时机第2项、流程第1步 | `Energy`, `observe` | EQUIVALENT | 季度 hard cue 不变 |
| RP-03 | 仅新季度或缺当季 checkpoint 不要求全文重读 Skill | Planning／使用时机第2项、流程第1步 | `rolling-planning` | EQUIVALENT | checkpoint 与 reread 解耦 |
| RP-04 | 同季主行动复用 checkpoint，除非重大反馈/状态变化 | Planning／使用时机第3项 | — | EQUIVALENT | 复用条件不变 |
| RP-05 | 半年反馈、严重警告/后果、continuation/context loss、checkpoint 过期/含糊、流程不能还原时重读并重建 | Planning／使用时机第4项 | `rolling-planning` | EQUIVALENT | 条件集合完整 |
| RP-06 | 不为每月普通故事调用；表扬/无新警告/接受或提交缓解本身不解风险/不触发重排；无重大风险正常成长不默认保守 | Planning／使用时机末段 | — | EQUIVALENT | 触发边界不变 |
| RP-07 | 只用当前已确认 session、最新公开 observe、同局 Board、确认回执、公开 Handbook；事实/推断/未知分开 | Planning／输入与证据规则首段 | `observe` | EQUIVALENT | 可见输入不扩张 |
| RP-08 | 禁止他局、尚不可见的局后事实、原始 DB、隐藏数值、评估权重；顺序不证明因果 | Planning／输入与证据规则末段 | — | EQUIVALENT | 禁止项不变 |
| RP-09 | 每次恰好一个公开职业/资源 Gap 或有证据的 progression stall；不默认均衡/固定优先级 | Planning／流程第3步 | `Primary Gap` | EQUIVALENT | 单一目标合同不变 |
| RP-10 | 目标可观察且供季度/半年复核；不承诺晋升、分数或事件结果 | Planning／流程第3步 | — | EQUIVALENT | 结果承诺仍禁止 |
| RP-11 | 季度 Energy 比较 Gap 的边际公开收益与 Energy/机会成本；单一维度饱和既不证明也不否定组合价值 | Planning／流程第3步 | `Energy` | EQUIVALENT | 比较语义不变 |
| RP-12 | checkpoint 进展只用可比新鲜证据标 ADVANCING/STALLED/UNKNOWN | Planning／流程第4步 | `ADVANCING`, `STALLED`, `UNKNOWN` | EQUIVALENT | 枚举及证据门槛不变 |
| RP-13 | ADVANCING 需 Gap 改善或直接相关公开绩效/晋升进展；表扬等正向信号单独不够 | Planning／流程第4步 | `ADVANCING` | EQUIVALENT | 局部正反馈限制不变 |
| RP-14 | 无直接可比 Gap 证据为 UNKNOWN，除非 Stall 条件成立 | Planning／流程第4步 | `UNKNOWN` | EQUIVALENT | fallback 不变 |
| RP-15 | 重复动作将 advertised effect 当假设，优先可靠同局 observed effect；归因含糊/中间原因/无比较为 UNKNOWN | Planning／流程第4步 | `Recent Effect` | EQUIVALENT | 观察优先关系不变 |
| RP-16 | 同 action、同 Gap、相邻两个可比 checkpoint 均无观察进展才 STALLED | Planning／流程第5步 | `STALLED` | EQUIVALENT | 两次门槛未降为一次 |
| RP-17 | STALLED 后必须比较不同类型的合法 alternative 及公开收益/机会成本 | Planning／流程第5步 | `STALLED` | EQUIVALENT | 比较而非切换 |
| RP-18 | 一次 miss 不强制切换；比较必需、选择不强制；Gap 改变或旧动作对新 Gap 有可靠收益时可继续并说明 | Planning／流程第5步 | — | EQUIVALENT | 例外与理由要求保留 |
| RP-19 | Risk Budget 按新鲜重大风险、安全余量或证据不足分别为 TIGHT/AVAILABLE/UNKNOWN | Planning／流程第6步 | `Risk Budget`, `TIGHT`, `AVAILABLE`, `UNKNOWN` | EQUIVALENT | 三态条件不变 |
| RP-20 | Safety 是约束不是默认目标；普通 Soft Cost 是机会成本，不自动否决高收益成长；不编造阈值 | Planning／流程第6步 | `Soft Cost` | EQUIVALENT | 风险态度未改变 |
| RP-21 | 普通合法候选顺序为重大风险 gate→Primary Gap→有用次级公开收益→Soft Cost/机会成本→UNKNOWN | Planning／流程第7步 | `Primary Gap`, `UNKNOWN` | EQUIVALENT | 定性次序保持 |
| RP-22 | 不默认最成熟/安全/不冒犯选项；不设固定权重/数值分数 | Planning／流程第7步 | — | EQUIVALENT | 无新评分公式 |
| RP-23 | 仅 AVAILABLE、无新鲜重大风险、Gap upside 明显更强且额外成本主要 Soft Cost 时优先高收益合法路径 | Planning／流程第7步 | `AVAILABLE`, `Material Risk`, `Soft Cost` | EQUIVALENT | 所有先决条件保留 |
| RP-24 | Gap 收益相似/未知可选低成本；TIGHT 时重大风险可压过成长；当前候选审查仍由 Risk | Planning／流程第7步 | `TIGHT`, `risk-review` | EQUIVALENT | 不削弱/扩大触发 |
| RP-25 | 仅公开当前月及 48 月；时间缩短且 Gap stalled 时偏向可观察进展，不推断晋升月/隐藏阈值 | Planning／流程第8步 | `Horizon` | EQUIVALENT | horizon 逻辑不变 |
| RP-26 | 普通非战略故事最多比两强候选一次；无新证据时仅新公开证据或 risk-review=RECONSIDER 才重开 | Planning／流程第9步 | `risk-review=RECONSIDER` | EQUIVALENT | stop rule 不变 |
| RP-27 | 严重警告/持续报复升级/重大生存信任成本可重开 Gap；以公开收益/损失/暴露/成本/UNKNOWN 比较合法路并标不可用项 | Planning／流程第10步 | `Primary Gap`, `UNKNOWN` | EQUIVALENT | severe handling 完整保留 |
| RP-28 | 原则、职责、近期晋升不是安全证明；保守或降暴露选项不是固定答案；同 Agent 决定 | Planning／流程第10步 | `Single Agent` | EQUIVALENT | 人格化偏好未强化 |
| RP-29 | 输出字段名必须 Horizon/Primary Gap/Progress/Recent Effect/Risk Budget/Path Trade-off，最多六行 | Planning／输出 | 六个原字段名 | EQUIVALENT | 字段拼写与行数合同不变 |
| RP-30 | 六行分别表达公开月/48 月与复核点、单一目标、可比进展、近期效果/UNKNOWN、风险预算、最多两路径取舍 | Planning／输出六项 | 原字段与枚举 | EQUIVALENT | 字段含义完整 |
| RP-31 | 无合法相关选项时标不可用并等待，不虚构选项 | Planning／输出末段 | — | EQUIVALENT | fallback 不变 |
| RP-32 | 不提交动作、不调用 new_game/observe/take_action、不改选项/notes | Planning／动作权限 | 三个 API 名 | EQUIVALENT | 技能工具权限不变 |
| RP-33 | Single Agent 唯一提交者，可调整/拒绝建议 | Planning／动作权限第3项 | `Single Agent` | EQUIVALENT | action authority 不变 |
| RP-34 | stale/ambiguous 时报告未知并回正常 fresh-state loop；不猜 ID、不阻断 | Planning／动作权限第4项 | `UNKNOWN` | EQUIVALENT | 恢复路径不变 |
| RP-35 | checkpoint 仅当前 conversation、当前 game；不写文件/全局 Memory/Skill state/Runner/模拟器，不跨局 | Planning／动作权限末项 | `Memory` | EQUIVALENT | 局内边界不变 |
| RT-01 | instruction 仅为 controller cue；详细算法仍留在四 Skills | runtime instruction 首句 | four Skills | EQUIVALENT | 未复制成第五份 Skill |
| RT-02 | 新局首次有效观察后读取详细 Planning | runtime instruction 第1句 | `rolling-planning` | EQUIVALENT | 初始触发保留 |
| RT-03 | 每季度首个 Energy 前新鲜 checkpoint，同季主行动复用，除重大变化 | runtime instruction 第2句 | `Energy`, `Planning checkpoint` | EQUIVALENT | trigger 与复用一致 |
| RT-04 | 条件反馈/严重后果/context loss/过期歧义/流程无法还原时重读 Planning | runtime instruction 第3句 | `rolling-planning` | EQUIVALENT | 条件触发保留 |
| RT-05 | 每次仅一个公开 Primary Gap，普通比较顺序不变 | runtime instruction 第4句 | `Primary Gap`, `UNKNOWN` | EQUIVALENT | cue 的定性顺序对应 v3b |
| RT-06 | Risk Budget 三态；Safety 是约束不是默认目标 | runtime instruction 第5句 | `TIGHT`, `AVAILABLE`, `UNKNOWN` | EQUIVALENT | 枚举/态度不变 |
| RT-07 | controlled aggression 仅在 AVAILABLE、无新鲜重大风险、Gap 公开 upside 明显且额外代价主要 Soft Cost 时 | runtime instruction 第6句 | `AVAILABLE`, `Material Risk`, `Soft Cost` | EQUIVALENT | 全部门槛保留 |
| RT-08 | 局部 praise 不单独 ADVANCING；重复 action 优先 observed 而非 advertised | runtime instruction 第7句前半 | `ADVANCING`, `observed effect`, `advertised effect` | EQUIVALENT | 两种证据规则保留 |
| RT-09 | 两相邻可比 checkpoint 的同 action/Gap 无进展才 STALLED，必须比较异类合法 alternative，不强制选 | runtime instruction 第7句后半 | `STALLED` | EQUIVALENT | 不强制切换 |
| RT-10 | 仅公开当前月/48-month horizon；停滞且时间缩短偏向可观察进展 | runtime instruction 第8句 | `48-month horizon` | EQUIVALENT | 无晋升阈值 |
| RT-11 | ordinary non-strategic event 最多比较两强候选一次；仅新鲜证据或 risk-review=RECONSIDER 才重开 | runtime instruction 第9句 | `risk-review=RECONSIDER` | EQUIVALENT | 决策 stop rule 保持 |
| RT-12 | Single Agent 唯一 action submitter，Skills 不提交 | runtime instruction 末句 | `Single Agent` | EQUIVALENT | 权限不变 |

## 结论

- 矩阵条目：`104`。
- `EQUIVALENT`：`104`；`BLOCKED`：`0`。
- `strategy delta = NONE`。仅语言、表达压缩与结构标注发生变化；本结论是逐项静态对照，不证明模型运行时遵循或任何得分收益。
