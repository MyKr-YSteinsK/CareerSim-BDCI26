# S10-01｜Runtime Prompt Value Audit / Architecture Reset Recommendation

## A. Identity / Evidence Boundary

- Status: `IN_FLIGHT_EVIDENCE / READY_FOR_S10_ARCHITECTURE_GATE`。这是设计推荐，不是 Main 接受或 Candidate 验证。
- Repository: `MyKr-YSteinsK/CareerSim-BDCI26`；branch: `codex/s10-01-architecture-reset-audit`。
- `PLAN_BASE_SHA = EXECUTION_BASE_SHA = 9edf73de552ce91af9d9eecf2dbbe6f5def9461d`。执行先 fetch；main drift=NONE。起始工作区干净；原 checkout 为 S09 evidence branch，没有把它当实施基线。
- `S09_PIN = c41a1b7210a02603aa19cc2bab19922a80b6cd77`，与 `codex/s09-14-v9a-static` 核对一致。
- Provider/service/MCP/game/observe/install/reload/submission/runtime mutation=0。仅 Git fetch/branch/document/commit/push 与本地静态读取；没有执行 Runner、导入框架或访问 shared DB。
- main 的 `candidate-v8a-v7o-donor-core-transplant` fallback 保持冻结；既有 raw、FORENSIC_HOLD、HPL 均未改变。

### 实际读取的来源

Main sources（均以 execution base 为准）：[AGENTS](../../../AGENTS.md)、[CURRENT_STATE](../CURRENT_STATE.md)、[Plan contract](../CODEX_PLAN_CONTRACT.md)、[Runtime contract](../AGENT_RUNTIME_CONTRACT.md)、[ADR](../ARCHITECTURE_DECISIONS.md)、[Source Lock](../OFFICIAL_SOURCE_LOCK.md) 的 compatibility/submission sections；[manifest](../../../configs/runtime_manifest.json)、三个 [identity](../../../career_sim_runner/prompts/identity.md) / [initial](../../../career_sim_runner/prompts/play_headless.md) / [continuation](../../../career_sim_runner/prompts/play_headless_continue.md) prompts；四个 [Board](../../../skills/structured-state-board/SKILL.md) / [Delivery](../../../skills/delivery-progress/SKILL.md) / [Planning](../../../skills/rolling-planning/SKILL.md) / [Risk](../../../skills/risk-review/SKILL.md)；Runner 的 [install](../../../career_sim_runner/install.py)、[headless_play](../../../career_sim_runner/headless_play.py)、[ws_client](../../../career_sim_runner/ws_client.py)、[constants](../../../career_sim_runner/constants.py)。main 的 S07-42 recovery feasibility、S09-10 donor transplant 作窄范围结构/血缘复核。

Pinned S09 默认入口，使用 `git show <S09_PIN>:<path>` 读取，不复制到 main：

- `docs/project/S09_CLOSEOUT.md`（E0）
- `docs/project/research/S09_HIGH_VALUE_EVIDENCE.md`（E1）
- `docs/project/research/S09_RUN_SUMMARY.json`（E2）

仅因 E1 的两项判断需要更精确依据，窄读 pinned `docs/project/reviews/S09-25_INFORMATION_ACCESS_AUDIT.md`（E3：字段准入）与 `docs/project/reviews/S09-32_EARLY_BASIN_DIVERGENCE.md`（E4：公开成果/早期窗口）。没有 broad-read S09 过程文件，没有读取 raw、解码模拟器或重新分析全部对局。E1/E2 对 RUN17/19/20/21、S09-27/16 的描述为复用 canonical compact evidence，未冒称本次重新核验 raw。

只读本机框架源码：`.venv/Lib/site-packages/` 下 `openjiuwen/harness/rails/context_engineer/context_assemble_rail.py`、`openjiuwen/harness/prompts/sections/context.py`、`openjiuwen/harness/prompts/workspace_content/workspace_header.py`、`openjiuwen/harness/rails/skills/skill_use_rail.py`、`openjiuwen/harness/prompts/sections/skills.py`、`openjiuwen/harness/rails/task_planning_rail.py`、`openjiuwen/harness/prompts/sections/todo.py`、`openjiuwen/harness/rails/memory/memory_rail.py`、`openjiuwen/harness/prompts/sections/memory.py`；`jiuwenswarm/server/runtime/agent_adapter/interface_deep.py` 的 rail registration / team references、`jiuwenswarm/agents/harness/common/rails/skill_retrieval_prompt_rail.py`、`jiuwenswarm/symphony/agent/agentic_retrieval_toolkit.py` 的 enable/render 分支、`jiuwenswarm/agents/harness/team/__init__.py`。这些是本机装配能力证据，不是 hosted Test 配置或运行轨迹证明。

### 事实与不确定性

E0 当时仍写 Main 未接受 S09；本次 stage status 采用最新 main 的 `COMPLETE_WITHOUT_STABLE_75_PLUS_BREAKTHROUGH`，不沿用旧 snapshot。样本保留如下：

| Reference | Score / horizon / grade / Level | 合法解释 |
|---|---|---|
| v6 | 75.29 / 48m / A / L6 | 有效高参考；runtime adherence FAIL |
| v7o | 71.83 / 48m / A / L5 | donor 参考，不是稳健概率估计 |
| v8a RUN07 | 72.65 / 48m / A / L5 | 高参考 |
| v8a RUN08 | 59.00 / 48m / C / L4 | 同 bytes 低尾，差13.65，不作因果归因 |
| v9a RUN10 | 68.40 / 48m / B / L5 | 新 probe 实施未确证 |
| RUN17 | 24.47 / 6m / E / L2 | Health terminal，M6晋升不能消除生存失败 |
| RUN19 | 38.08 / 33m / D / L4 | trust terminal，最后公开 H9仍失败 |
| RUN20 | 60.60 / 48m / B / L4 | 完整低尾，不能证明 v11优越 |
| RUN21 | final UNKNOWN / last M37 / final grade UNKNOWN / L4 | partial technical evidence；无48m、无75+，不自动补跑 |

缺少随机化/配对控制、充足重复样本、真实注意力测量和 hosted 配置。报告中的 attention 是静态 proxy；memory/review/reduction 收益均 `HYPOTHESIS / NEEDS_EXPERIMENT`。没有证据把失败归因为 DeepSeek 专属能力缺陷。

## B. Executive Architecture Recommendation

`ARCHITECTURE_RESET_RECOMMENDATION = LEAN_SINGLE_AGENT_WITH_ONE_CAREER_BRIEF_AND_CHECKPOINT_REVIEW`

- `FOUR_SKILL_DECISION = REDUCE`：建议两份职责文档，State & Brief 与 Career Decision；四个逻辑责任仍可识别，但不再每个 action 维护四份协议输出。
- `STRUCTURED_MEMORY_DECISION = IMPLEMENT_NEXT`：仅建议后续授权实现一个 same-session、overwrite 的 Career Brief，替代 Review Plan/Delivery/STICKY 的历史摘要部分，不增加第五 Skill或通用 memory 系统。
- `DEEP_REVIEW_DECISION = SAME_AGENT_MATERIAL_CHECKPOINTS`：formal Review/promotion 和 material warning/result/机会失效触发，普通 action 不做 deep review。
- `FAMILY_A = V8A_BASE_LEAN_BRIEF_CHECKPOINT_ARCHITECTURE`：main + frozen v8a 为正式 baseline；保留 v7o 已进入 v8a 的 donor core，最小移植 S09 的动态下行、同 scope trust continuity 与结果可兑现比较。
- `FAMILY_B = NOT_JUSTIFIED`：没有独立 Reviewer 胜过 same-agent review 的证据，不能占用第二 family 预算。
- `NEXT_GAME = NOT_AUTHORIZED`。

RECOMMENDATION：先测试一个 coherent architecture reset，不继续 v11b micro-patch。理由不是“短 prompt 必然更好”：现有 Board、Delivery、Review Plan 已承担记忆，但没有一个统一写入/失效/复查责任；E1 的 stale Delivery 与 premature risk clearance 表明存有标签并不等于能控制下一步。将历史摘要合为一个事实可追溯 Brief、将深推理集中在 material checkpoint，能直接检验“分散状态和每步协议负担”这个假设。因果收益尚未证明，失败时须区分未执行机制与机制执行后无收益。

## C. Runtime Surface Map

### 装配链与顺序

`install_submission → _install_skill_bundle / _write_skills_state → _write_identity_md → host agent rails → before_model_call → model`；play 的用户消息由 `play_headless → build_play_prompt / build_continue_prompt → drive → _build_envelope` 送入。这里只阅读该代码，没有调用 install/play。

| Surface | Source / owner | When injected/read | Persistent/repeated? | Proven from |
|---|---|---|---|---|
| identity shell + manifest instruction | identity template / Runner + Candidate | install 时将技能名与 instruction 替换到 IDENTITY；host 每次模型调用前装配 | system section 常驻；不是 manifest 作为第二份独立消息 | install.py `_write_identity_md` 137起；ContextAssembleRail 86起；context.py `build_context_file_sections` |
| four Skill names/descriptions | skills frontmatter / Candidate + host | 注册 local_skills；SkillUseRail 构造 session baseline descriptions | system skills section 每次重建；正文不等于每次全量注入 | install.py `_write_skills_state`；SkillUseRail 417–503 |
| four Skill bodies | 四个 SKILL.md / Candidate | manifest 要求 startup 按 Board→Delivery→Planning→Risk读取；可见 recovery再读 | 工具读取后的 dialogue/attachment，可受压缩影响；普通 action应用、不要求重读 | manifest STARTUP/CONTEXT RECOVERY；skills section只列 name/description；S07-42 |
| initial play | play_headless.md / Runner | fresh drive初始 user query | 一次启动；dialogue保留受压缩影响 | headless_play.py 122–134；ws_client.py 114–117 / `_build_envelope` |
| continuation | play_headless_continue.md / Runner | nonterminal e2a.complete，最多 MAX_CONTINUATIONS；`--continue`另走 unknown分支 | 按 execution completion 重复，不是每月/每action | ws_client.py 119–130 / 273–292；constants及Runner control |
| recovery / log advice | identity状态恢复 + manifest恢复 + Board/Delivery/Planning | identity建议 observe+logs；manifest增加四Skill恢复 | identity规则每次存在，实际恢复工作仅可见signal；logs是工具结果非常驻指令 | identity状态恢复；manifest；S07-42 |
| AGENT/SOUL/USER/HEARTBEAT | host workspace files | 有非空内容才装配；前三者system，HEARTBEAT attachment | 条件性每次；不是本repo AGENTS.md自动进入玩家上下文 | ContextAssembleRail `_SYSTEM_CONTEXT_SECTIONS` / `_ATTACHMENT_CONTEXT_SECTIONS`；workspace_header `CONTEXT_FILES` |
| workspace/tools guidance | host generated sections | before_model_call生成路径/可用工具摘要 | 按能力列表条件生成；工具完整schema另属模型输入 | ContextAssembleRail；context.py `build_tools_content` |
| todo guidance/reminders | host TaskPlanningRail | agent模式注册；todo section每次，进展提醒依配置/工具计数 | 通用task控制；可能与整局循环争注意力 | interface_deep.py 5823起；TaskPlanningRail 148起；todo.py |
| passive memory guidance/recent daily content | host MemoryRail | agent模式按config启用；可能注入今日昨日内容 | 条件性；install清memory/*.md与sessions，不保证所有nested日记残留清除 | interface_deep.py `_handle_memory_rail_by_config`；MemoryRail 118起；install.py 43–58 |
| alternate skill retrieval guidance | host SkillRetrievalPromptRail | enabled且index可用时隐藏native skills并换retrieval section | 条件性每次，不能把两种分支同时累计 | retrieval rail `before_model_call`；agentic_retrieval_toolkit enable/render |
| compression summary / state | host compressor | token触发，summary替换dialogue，可能恢复skill state | 非固定控制文本；不保证真实重读 | S07-42 compressor code-path review，非本次live验证 |

FACT：四个 Skill 是同一模型应用的文档，不是四个独立 agent。Manifest 在 identity 的参赛者策略块内；identity 核心规则/恢复段在它之后，故冲突不能凭“manifest最后”解决。Skill descriptions 与正文重复一次 owner/trigger，但正文读取时机和后续保留不能由文件大小推断。Rail 的系统 section 使用 priority管理，不能把 Python set iteration当固定模型文本顺序。

Boundary：repo/source 足以确认 Candidate→identity、Skill metadata/body与Runner query的静态路径；没有重新读取 shared workspace/profile/配置或调用模型，不能给出某个运行的完整system bytes、host条件分支enabled状态和实际Skill读取成功率。host条件源列为 conditional，未把它们计成确定的 Candidate额外成本。框架允许路径不是已执行加载证明；这不需要 live 才能回答设计，部署前身份核验仍由未来任务承担。

## D. Clause-Level Value Audit

分类：A=`GAME_SERVING`，B=`MODEL_COGNITION`，C=`DEV_OBSERVABILITY_ONLY`，D=`LEGACY_GOVERNANCE`。Disposition是未来架构建议；当前条款仍有效。`K/CO/OUT/RM/RC` 分别为 `KEEP / CONSOLIDATE / MOVE_OUT_OF_RUNTIME / REMOVE / RECONSIDER`。Cadence `p`=常驻规则，`o`=fresh observe，`a`=action，`q`=Energy/Main，`r`=Review/material checkpoint，`x`=recovery，`s`=startup，`c`=continuation。primary class唯一；次类仅必要时写 `A+B` 等。置信度针对设计处置，不是分数因果置信度。

每行末列按「gameplay evidence；cognition value；attention cost；confidence / reason」填写。E0–E4定义见A；`U=UNPROVEN` 表示无直接机制收益证据，`EXEC`表示静态执行正确性依据C，不暗示已验证分数。Source列用C链接的文件简称+附近heading；所有正文、frontmatter trigger/owner与machine schema纳入语义覆盖。同一表格行可合并不能独立处置的条件/退出分支；可独立处置的marker与行为已拆开。

### Manifest instruction（M，owner=manifest）

| Clause ID | Source section / paraphrase | Cadence | Class | Disposition | Evidence / cognition / cost / confidence & reason |
|---|---|---|---|---|---|
| M01 | opening：同局fresh公开观察、菜单、手册、Review、结果/允许日志 | p/o | B+A | K | EXEC/E3；事实权威；低；HIGH，保留来源与session边界 |
| M02 | opening：禁hidden/private/跨局输入 | p | B | K | E3；防污染；低；HIGH，不从历史raw给玩家私有输入 |
| M03 | firewall：按HiddenRisk/internal effect等字段名一并排除 | p | D+B | RC | E3；准入保护；高/过宽；HIGH，delta/stock混同；Main审议才可改 |
| M04 | firewall：不伪造threshold/cap/weight/答案lookup | p | B | K | E1/E3；不确定性；低；HIGH，保持假设与事实区分 |
| M05 | ownership：唯一action submitter | p/a | B | K | EXEC；权限；低；HIGH，简化不增加第二提交者 |
| M06 | ownership：Board/Delivery/Planning/Risk独占职责 | p | B | CO | U；减少冲突；重复；MEDIUM，改两份文档仍保留事实/策略/安全逻辑边界 |
| M07 | ownership：manifest管编排/常驻关键规则并允许一致重复 | p | B | CO | U；显著性；重复；MEDIUM，仅关键fresh/session规则重复 |
| M08 | kernel：A默认、长期晋升与survival floor | p/a | A | K | E1 v6/v7o/RUN07；目标保持；低；MEDIUM，描述支持非因果 |
| M09 | kernel：首评broad S/N/O、成果、Main ownership多维prior | p/a/q | A | K | E1/E4；early compounding；低；MEDIUM，不固定答案 |
| M10 | kernel：Review方向gap、接受有价值普通成本 | p/r/a | A | CO | E1；不保守死锁；重复；MEDIUM，与Career Decision合一 |
| M11 | kernel：fresh material threat才S、最小保护、解除回A | p/o/a | A+B | CO | E1 RUN17/19；生存判断；重复；MEDIUM，保持dynamic downside扩展 |
| M12 | kernel：local NO_GAIN折价、未知family开放、不推cap | p/o | B+A | K | E1 RUN10/cap drift；适应；低；HIGH，避免全局封路 |
| M13 | startup：首次action前按顺序读四Skill | s | B | CO | EXEC；获取策略；四读；MEDIUM，未来改两文档；当前必须四读 |
| M14 | startup：ordinary同context不重读 | a | B | K | EXEC；节省重复；低；HIGH |
| M15 | flow：observe→四责任→READY→preflight→one action→observe required | o/a | B | CO | EXEC；新鲜决定；中间协议；HIGH，保留行为，压缩表达 |
| M16 | flow：Risk不replan、Delivery不rank、Board不strategy | a | B | CO | U；authority；重复；MEDIUM，逻辑分层不需四输出 |
| M17 | whole game：DECISION_CLOSED不是assistant结束 | a/c | B | K | S07-42/S09-10与Runner continuation；持续执行；低；HIGH |
| M18 | whole game：action后立即observe、不因month/Review/marker停止 | a/c | B | CO | EXEC；整局推进；枚举重复；HIGH，合成一个持续循环规则 |
| M19 | whole game：只认structured ended或明确unrecoverable failure | a/c | B | K | EXEC/E1 RUN21；终止归属；低；HIGH |
| M20 | control：executor独占READY/OBSERVE_REQUIRED/BLOCKED | o/a | B | CO | EXEC；授权；三态；HIGH，保留失效语义，不要求每步自报 |
| M21 | control：READY前必须fresh同局与事实/计划/final safety完成 | o/a | B | CO | EXEC；防stale；重复；HIGH |
| M22 | control：action消耗授权，receipt不更新public state | a | B | K | EXEC；receipt边界；低；HIGH |
| M23 | control：OBSERVE_REQUIRED只可observe、不复用旧candidate | a/o | B | CO | EXEC；防batch；重复；HIGH |
| M24 | control：fresh后重建response/各责任再preflight | o | B | CO | EXEC；更新决定；重复；HIGH |
| M25 | control：失败/未知/session mismatch阻断，仅bounded recovery | a/x | B | K | EXEC；未知副作用STOP；低；HIGH |
| M26 | preflight：同局fresh、单legal integer、final gate完整 | a | B | K | EXEC；必要正确性；低；HIGH，不能只外移为事后审计 |
| M27 | preflight：要求合法CTRL/DL作为action gate | a | C+B | OUT | E1 separator/adherence；审计；格式阻断；MEDIUM，未来删marker gate但保留M26 |
| M28 | preflight：CTRL G/P/R/RB四字段、次序/唯一prefix | a | C | OUT | E1；parser归属；四字段；HIGH，纯report不能证明判断 |
| M29 | preflight：DL i/n/focus/evidence/checkpoint/recognition六字段 | a | C | OUT | E1 stale D1；lifecycle可见；六字段；HIGH，保留结果事实不保留mandatory marker |
| M30 | preflight：RB分支未闭合禁止submit，R写final结果 | a | B+C | CO | EXEC；有界替代；标签负担；HIGH，保留一次比较/最终检查，不依赖RB字串 |
| M31 | preflight：marker不能替代control/其它条件 | a | B | CO | EXEC；防自证；重复；HIGH，审计仍不能充当安全证明 |
| M32 | Energy：quarter intent只目标、不序列/配额 | q | B | CO | E1 recipe drift；适应；额外对象；MEDIUM，统一current objective即可 |
| M33 | Energy：one action后observe/response/新pass、丢弃余序列 | q/o | B+A | K | EXEC/E1；适应和schema；重复；HIGH，行为必保留 |
| M34 | Energy：responsive alternative存在不立即重复clean NO_GAIN | q | A+B | CO | E1；路由；重复；MEDIUM，不变成禁全部同维度 |
| M35 | recovery：pending阻断、ready本身不授权、新fresh完整检查 | x/a | B | CO | EXEC/S07-42；恢复正确性；两次observe；HIGH，signal恢复后提交前fresh仍保留 |
| M36 | recovery：仅可见resume/compaction signal触发，禁虚构host检测 | x | B | K | S07-42；能力边界；低；HIGH |
| M37 | recovery：同局observe→四读→Board/Delivery/Plan或UNKNOWN | x | B | CO | S07-42；上下文重建；顺序；MEDIUM，未来两读+Brief核验，非工具强制hook |
| M38 | recovery：identity/observe/read失败保持pending、不action | x | B | K | EXEC；恢复门禁；低；HIGH |

### Identity / initial / continuation（I/T/C，owner=Runner prompt）

| Clause ID | Source section / paraphrase | Cadence | Class | Disposition | Evidence / cognition / cost / confidence & reason |
|---|---|---|---|---|---|
| I01 | 身份：玩家唯一目标完整玩局并高分 | p | A | K | E1；目标；低；HIGH，非遵从率目标 |
| I02 | 技能列表与严格遵Skill | p/s | B | K | EXEC；发现策略；metadata重复；HIGH，未来仅改变bundle，Runner不改 |
| I03 | 策略插槽instruction | p | B | K | EXEC；持久策略载体；见M；HIGH，不双计 |
| I04 | 核心1：已有session禁止第二次new_game | p/c | B | K | EXEC；session权限；低；HIGH |
| I05 | 核心2：observe→分析→legal choice/notes action | p/a | B | K | EXEC；循环；与M重复；HIGH，高价值冗余 |
| I06 | 核心3：未结束持续、不问用户 | p/c | B | K | EXEC；whole-game；重复；HIGH |
| I07 | 核心4：context不足先observe不猜 | p/x | B | K | EXEC；恢复；重复；HIGH |
| I08 | 恢复：继续指令说明可能压缩，沿用session | c/x | B | K | EXEC；连续性；低；HIGH，“可能”不是压缩证明 |
| I09 | 恢复：observe当前状态 | x | B | K | EXEC；fresh权威；重复；HIGH |
| I10 | 恢复：check_latest_logs最近N条再loop | x | B | K | E3；恢复warning/result；工具成本；MEDIUM，读取最小相关历史不机械dump |
| T01 | 初始当前任务：新局遵identity与Skills | s | B | K | EXEC；启动；低；HIGH，文本是玩家指令不是本Task授权 |
| T02 | 开始1：Handbook一次 | s | B+A | K | E3；公开规则；一次；HIGH |
| T03 | 开始2：new_game与SESSION_ID输出 | s | B+C | K | EXEC；身份绑定；低；HIGH |
| T04 | 开始3：observe/decision/action到结束 | s/a | B | K | EXEC；loop；重复；HIGH |
| T05 | 开始4：ending_score完整输出/DONE | terminal | C | K | EXEC；结果归档；终局低成本；HIGH，无ordinary burden |
| C01 | continuation：提供session/year/month、同局继续 | c | B | K | EXEC；定位；低；HIGH，时间提示不替代fresh observe |
| C02 | continuation：可读近期logs | c/x | B | K | E3；恢复；重复；MEDIUM，只有需要时用 |
| C03 | continuation：observe并直到结束 | c | B | K | EXEC；whole game；重复；HIGH |
| C04 | continuation：禁止new_game及系统自动信息标识 | c | B | K | EXEC；权限/来源；低；HIGH |

### Board（B，owner=structured-state-board）

| Clause ID | Source section / paraphrase | Cadence | Class | Disposition | Evidence / cognition / cost / confidence & reason |
|---|---|---|---|---|---|
| B01 | frontmatter/职责：fresh observe后事实层、Review/warning/response/unknown | o/x | B | CO | EXEC/E1；状态准确；中间对象；HIGH，合入State & Brief |
| B02 | 职责/不变量：不plan/rank/gate/submit | o | B | CO | U；authority；重复；HIGH，事实与决策仍分开 |
| B03 | 输入：fresh、紧邻公开结果、前Board、必要同局logs | o/x | B | K | E3；状态延续；低；HIGH |
| B04 | 输入：禁止其它game/hidden/DB/局后结论/跨局memory | p | B | CO | E3；证据隔离；重复；HIGH |
| B05 | 输出：每次完整替换SESSION/M/Q、H/D/S/N/O/W/L/E、TENURE | o | B+C | CO | EXEC；current facts；12个定位/状态字段；MEDIUM，直接用observe，仅Brief存锚点 |
| B06 | 输出：REVIEW/RESPONSE/STICKY/EFFECTS/UNKNOWN结构 | o | B | CO | E1；历史关键摘要；额外副本；MEDIUM，Brief一个owner，不保留平行Board |
| B07 | STATE1：session/fresh确认，不同局丢旧Board | o/x | B | K | EXEC；隔离；低；HIGH |
| B08 | STATE2–4：status原值精度复制；缺/身份不明UNKNOWN；不推算补值 | o | B | K | EXEC；防幻觉状态；低；HIGH，不把advertised当realized |
| B09 | STATE5：其它公开信息分事实，等待observe更新STATE | o | B | K | EXEC/E3；来源分离；低；HIGH |
| B10 | REVIEW：正式grade/promotion/no-advance/feedback保存 | r/o | B+A | CO | E1；战略反馈；重复；HIGH，Brief latest review锚 |
| B11 | STICKY排除：低绩效/no-promo/弱SNO/普通负荷/单次下降 | o | A+B | CO | E1；防过度S；分支枚举；MEDIUM，压缩为普通成本与material威胁区别 |
| B12 | STICKY纳入：财务/健康尊严/工作连续性/孤立/事故信任等material约束 | o | A | K | E1 RUN17/19；多failure floor；低；HIGH，不能只保护Health |
| B13 | STICKY：acute warning即使数字尚可也保留 | o | A | K | E1；不按数字清除；低；HIGH |
| B14 | STICKY：same-scope明确解除或场景结束才移出 | o/r | B+A | K | E1 RUN19–21；风险持续；低；HIGH，generic praise非clearance |
| B15 | RESPONSE：current-Level维度最近投入GAIN/NO_GAIN/UNKNOWN | o | B+A | CO | E1；适应；粗粒度标签；MEDIUM，改为有证据的tested path摘要 |
| B16 | RESPONSE1：相邻action-observe且无Review/salary等混杂才更新 | o | B | K | E4；归因边界；低；HIGH，混合效果unknown |
| B17 | RESPONSE2–3：只更新涉及维度、其它沿用、新GAIN覆盖旧NO_GAIN | o | B | K | E1；避免stale；低；HIGH |
| B18 | RESPONSE4–5：Level/session变化reset | r/o | B | K | EXEC；scope失效；低；HIGH |
| B19 | RESPONSE6：local response不证明cap/threshold/eligibility/hidden cause | o | B | K | E1；避免固定上限；重复；HIGH |
| B20 | EFFECTS：最多2、无clean归因则UNKNOWN/MIXED | o | B | CO | E4；recent evidence；额外副本；MEDIUM，留decision-relevant evidence不独立EFFECTS对象 |
| B21 | Recovery：同局fresh重建STATE/Review/STICKY，必要少量logs | x | B | CO | S07-42/E3；恢复；重复；HIGH |
| B22 | Recovery：不可恢复UNKNOWN，不沿用不验证旧Board | x | B | K | EXEC；staleness；低；HIGH |
| B23 | 不变量：fact与unknown分开，不累积transcript | p/o | B | K | EXEC；bounded memory；低；HIGH |
| B24 | 不变量：按受限字段名一律排除、不记忆 | p | D+B | RC | E3；准入保护；过宽重复；HIGH，与M03同一Main问题 |

### Delivery（D，owner=delivery-progress）

| Clause ID | Source section / paraphrase | Cadence | Class | Disposition | Evidence / cognition / cost / confidence & reason |
|---|---|---|---|---|---|
| D01 | frontmatter/职责：每fresh Board最多3个Review相关交付、无排序/目标/风险/action | o | B | CO | E1；结果记忆；整套对象；MEDIUM，并入Brief事实层 |
| D02 | 职责：首评前承诺/checkpoint相关性，之后依仍有效Review Plan | o/r | B+A | CO | E4；结果优先；隐性时序依赖；MEDIUM，checkpoint写Brief，不等Planning每步重算 |
| D03 | 职责：不发明Objective/Gap、不等Planning；其它owner表 | o | B | CO | U；authority；重复；MEDIUM，删除跨文档循环接口 |
| D04 | Lifecycle：七阶段+blocked回转，非hidden state/非强制顺序 | o | B | CO | E1 stale D1；事实区分；七态；MEDIUM，只保留commitment/verified/blocked意义，不维护阶段机 |
| D05 | 每项8槽：id/item/stage/owner/checkpoint/proof/evidence/recognition | o | B+C | CO | E1；结果证明；8槽×items；MEDIUM，Brief active result只记对未来有用证据 |
| D06 | evidence_status三态 | o | B | CO | E1；verified与unknown；三态；HIGH，保留事实区别不保留重复编码 |
| D07 | Identity：session-local D序列，distinct新ID、retired不复用、NEXT_ID | o/x | C+B | OUT | U；audit item attribution；cursor；HIGH，外部记录可做ID，玩家记语义scope |
| D08 | Identity：session才reset、恢复cursor unknown不可猜 | x | B+C | CO | EXEC；隔离；cursor burden；HIGH，Brief session绑定取代ID恢复任务 |
| D09 | 更新：仅relevance/commitment/milestone/blocker/result/item-linked Review变化 | o/r | B | K | E1；避免每步改写；低；HIGH，Brief同样material update |
| D10 | 验证：claimed/unverified与delivered/public verified区别 | o/r | A+B | K | E1/E4；result conversion；低；HIGH，状态字串非证明 |
| D11 | receipt只证工具执行、不证career result | a/o | B | K | EXEC；工具/游戏区别；重复；HIGH |
| D12 | generic praise/promotion/communication/promise不能单独验证item | o/r | B+A | K | E1；防假兑现；低；HIGH |
| D13 | recognition必须明确同item关联，否则0/? | o/r | B | CO | E1；recognition证据；flag；HIGH，Brief用来源句替代bit |
| D14 | near item可由Planning选Delivery recovery/Advance；Delivery不定继续投资 | a/r | A+B | CO | E4；结果选择；跨owner；MEDIUM，Career Decision比较result和机会 |
| D15 | recovery仅恢复fresh same-session支持item，其余unknown | x | B | K | E3；恢复；低；HIGH |
| D16 | Bound：3 active+1 recent closed；依commitment/blocker/checkpoint/link保留 | o | B | CO | U/E1；bounded state；库存；MEDIUM，保留真实承诺摘要，不机械删不可忽略义务 |
| D17 | Bound：无公开active basis退休，超限按决策相关性不能伪降n | o/r | B | CO | E1 stale D1；失效；inventory；MEDIUM，checkpoint显式重验basis |
| D18 | 输出：每Board完整Delivery+六字段DL focus | o/a | C | OUT | E1 parser/stale；audit；mandatory schema；HIGH，external audit只记可观察事实 |
| D19 | checkpoint NEAR须公开相关性、非数字倒计时 | o | B | CO | U；不编造window；label；MEDIUM，Brief用公开checkpoint文字 |
| D20 | marker n/i/CLOSED不计active，不作focus | a | C | OUT | U；parser一致；规则分支；HIGH，去marker则无runtime价值 |
| D21 | n0规定NONE/NA/NOT_NEAR/0整套值 | a | C | OUT | U；parser；默认值；HIGH |
| D22 | marker只描述不改ranking | a | B | CO | U；authority；重复；HIGH |
| D23 | 不变量：同局public，无hidden/跨局durable memory | p | B | CO | EXEC；隔离；重复；HIGH |
| D24 | 不变量：不new_game/observe/take_action | p | B | CO | EXEC；唯一提交者；重复；HIGH，合并后仍事实层不submit |

### Planning（P，owner=rolling-planning）

| Clause ID | Source section / paraphrase | Cadence | Class | Disposition | Evidence / cognition / cost / confidence & reason |
|---|---|---|---|---|---|
| P01 | frontmatter/Objective：fresh Board/Delivery后晋升成长+survival floor | o/a | A | K | E1；主目标；低；MEDIUM |
| P02 | Objective：中文判断输出 | p/a | B | K | U；输出一致；低；MEDIUM，无因果分数结论 |
| P03 | REVIEW_PLAN三槽Objective/Gap/checkpoint | r/a | B | CO | E1；战略连续；一对象；MEDIUM，Brief objective+review basis替代 |
| P04 | MODE A默认/S material survival；Planning独占目标排序，single submitter | a | A+B | CO | E1/EXEC；growth vs binding；重复；HIGH，保留语义 |
| P05 | Evidence输入fresh Board/Delivery/menu/Handbook/Review/result | o/a | B | CO | EXEC/E3；事实权威；重复；HIGH |
| P06 | Evidence字段名禁用、private/跨局/公式/lookup排除 | p | D+B | RC | E3；准入；重复/过宽；HIGH，private与formula边界KEEP，字段名规则审议 |
| P07 | 先binding，再Review→result→state/warning→Delivery→advertised优先级 | a/r | B+A | CO | E1；证据排序；串联层级；MEDIUM，公开实得优先但不让Review遮蔽新危机 |
| P08 | RECOVERY六标签仅接口；progression A、resource S、warning/delivery按证据 | a | B | CO | E1；分类；六态；MEDIUM，改具体constraint/problem句，不另持久enum |
| P09 | warning+reparative option可一次cleanup，fresh后回主线；持续warning才重复 | a/o | A | RC | E1 RUN19–21；风险处理；与persistent risk张力；HIGH，回主线不等于erase risk，需same-scope解除 |
| P10 | context恢复同局四读重建后Plan/Recovery，missing unknown未完不rank | x | B | CO | S07-42；恢复；重复；HIGH，改两文档/Brief接口才可实施 |
| P11 | Review Plan：首评gap unknown，broad growth+visible delivery | r/a | A+B | K | E1/E4；早期目标；低；MEDIUM |
| P12 | feedback后gap锚最清晰公开deficit | r | A+B | K | E1；适应；低；MEDIUM，非lowest-stat recipe |
| P13 | revise仅Review/完成/失效/不可行，普通Story/波动不改gap | r/o | B | CO | E1；防churn；四触发；MEDIUM，Brief invalidation同一个owner |
| P14 | gap是方向非硬树，允许更强ownership/多维/result | a | A | K | E1；避免窄目标；低；MEDIUM |
| P15 | 剩余horizon可实现价值，无公开未来Review不虚构 | a/r | A+B | K | U；兑现；低；MEDIUM |
| P16 | MODE先fresh whitelisted facts/menu，单H/D/W/普通drop不自动S、不numeric threshold | o/a | A+B | CO | E1 RUN17；保护误触发；限制过窄风险；MEDIUM，dynamic downside无需机械阈值 |
| P17 | material生存/安全/job/trust/财务危机，acute即使数字好仍S | o/a | A | K | E1 RUN17/19；failure floor；低；HIGH |
| P18 | S最小合理保护同时保成长 | a | A | K | E1；sustainable aggression；低；MEDIUM |
| P19 | 解除/场景结束才A，数字变好/无关feedback不证明解除 | o | A+B | K | E1 trust；false clearance；低；HIGH |
| P20 | 普通负荷/疲劳/摩擦/未知/cost本身不S，无binding用A | a | A | CO | E1；防保守；重复；MEDIUM |
| P21 | S计划显示constraint，最低机会成本解决，不risk avoidance | a | A+B | CO | E1；退出控制；重复；MEDIUM |
| P22 | Wealth压力避discretionary cost但修绩效晋升收入 | a | A | K | E1；收入恢复；低；MEDIUM |
| P23 | 每observe从A重判、旧S不续期、不补满资源、低绩效不S | o | A+B | CO | E1；nonsticky protection；重复；MEDIUM，继续风险事实不等继续S |
| P24 | A排序gap/result ownership/multidimensional/compound，强成长可接受soft cost | a | A | K | E1 v7o/RUN07；donor core；低；MEDIUM，非永远固定优先级 |
| P25 | pre-first prior：A无binding+已有高值commitment/concrete checkpoint/claimed可验证机会 | a | A | CO | E4；结果可兑现；长条件；MEDIUM，改现实deadline/feasibility比较 |
| P26 | prior：stage/proof/recognition/checkpoint检查；report label/info/无底层result不够 | a | B+A | CO | E1/E4；防把report当成果；四字段；HIGH，语义保留，schema不保留 |
| P27 | prior：真实兑现胜generic push但不挤更强时限机会，无basis照常broad growth | a | A | K | E4；ranking例外；低；MEDIUM |
| P28 | prior：verified不重复包装；first Review/verified/invalid/blocked/S退出 | a/r | A+B | CO | E1；避免stale rule；五退出；MEDIUM，Review后仍可兑现，取消独立prior状态名 |
| P29 | S排序不恶化→直接解除→留成长；不永久避险 | a | A | CO | E1；failure floor；重复；MEDIUM |
| P30 | near high-value commitment优于弱新项目，old item不挡明显更强机会 | a | A | K | E1/E4；承诺拥塞；低；MEDIUM |
| P31 | hint只是soft evidence，不变固定action/hidden requirement/cap | a | B | K | E1/E3；适应；重复；HIGH |
| P32 | advertised无realized gain记NO_GAIN/COST，cause unknown | o | B+A | K | E4；response；低；HIGH |
| P33 | 消费response只折已测Level/context/dimension/family，unknown保持开放、多维保价值 | a | B+A | K | E1 RUN10；机会捕获；粗粒度接口张力；HIGH，Board只有SNO需补path evidence |
| P34 | Level reset、不全局cap/eligibility/零opportunity-cost；responsive alternative不立刻重复 | o/a | B+A | CO | E1；anti-stale；重复；HIGH |
| P35 | Quarterly目标非配额，每action后fresh新pass/final Risk/preflight | q | B | CO | EXEC/E1；非batch；重复；HIGH |
| P36 | Main同ranking，无binding给ownership+多维growth strong prior | q | A | K | E1；donor核心；低；MEDIUM，未证明普适最佳 |
| P37 | decision：one fresh one pass、去dominated、最多2竞争项、一次比较唯一candidate | a | B | K | S09-10；closure；低；MEDIUM，保留预算不要求长输出 |
| P38 | no new evidence不重开，Risk一次direct alternative后final check未完blocked | a | B | CO | EXEC；有界选择；重复；HIGH |
| P39 | UNKNOWN一次fresh rebuild仍unknown则一次bounded legal决定，executor独占preflight | a/x | B | CO | EXEC；防无限重试；重复；HIGH，session/action未知不能被bounded decision绕过 |
| P40 | PLAN G/P/F/checkpoint + CANDIDATE choice/reason每步输出 | a | C+B | OUT | U；审计；六槽；MEDIUM，保留choice+简短理由，checkpoint写Brief |
| P41 | 不submit或调用game工具 | p | B | CO | EXEC；唯一提交者；重复；HIGH |

### Risk（R，owner=risk-review）

| Clause ID | Source section / paraphrase | Cadence | Class | Disposition | Evidence / cognition / cost / confidence & reason |
|---|---|---|---|---|---|
| R01 | frontmatter/职责：action前只final candidate、无Plan/gap/ranking权 | a | B | CO | EXEC；防第二规划；重复；HIGH，Career Decision内final safety check |
| R02 | 输入candidate/fresh facts/MODE/public consequences | a | B | K | EXEC；当前评估；低；HIGH |
| R03 | public-only但按字段名禁HiddenRisk等 | p | D+B | RC | E3；准入；过宽重复；HIGH，stock禁保留，delta待Main |
| R04 | 输出RISK五值+reason | a | C+B | CO | U；closure audit；五态；MEDIUM，留安全理由不需独立报告 |
| R05 | Quick：普通workload/H D小cost/摩擦/uncertainty/opportunity无material upgrade直接PASS | a | A | K | E1；不否决growth；低；MEDIUM，当前余量使普通成本重大时不可quick |
| R06 | Quick：不能因另一choice更安全就拦强成长 | a | A | K | E1；sustainable aggression；低；MEDIUM |
| R07 | Full：acute/safety/job/trust/retaliation/compliance/confidentiality/affordability/恶化binding | a | A | K | E1 RUN17/19；多failure floor；低；HIGH |
| R08 | Wealth区分花费与绩效晋升收入，低Wealth不自动否决 | a | A | CO | E1；protect growth；重复；MEDIUM |
| R09 | ALLOW重大已审仍可；WARN不足换；RECONSIDER重大未处理且有相关替代；UNKNOWN事实缺 | a | B+A | CO | EXEC；bounded safety；四标签；HIGH，保留判断语义不要求标记值 |
| R10 | Full后不得PASS | a | C+B | OUT | S09-10 local ALLOW/PASS差异不证ranking变；audit；分类负担；MEDIUM，外部可描述触发basis，不能假装安全已检查 |
| R11 | reconsider比较一次替代，选中候选重过Risk | a | B | K | EXEC；final safety；低；HIGH |
| R12 | CTRL final R、RB NONE/DONE/BLOCKED完整格式及赋值 | a | C | OUT | E1；parser；字段重复；HIGH |
| R13 | 未闭合禁止submit，new evidence后完整gate；READY与final R约束 | a | B | CO | EXEC；action correctness；重复；HIGH，行为保留 |
| R14 | UNKNOWN最多一次fresh，仍unknown bounded legal选择非无限循环 | a/x | B | CO | EXEC；closure；重复；HIGH，安全/identity硬阻断不越过 |
| R15 | RECOVERY=RISK属Planning，warning可cleanup但不自动RECONSIDER | a | A+B | CO | E1；trigger分离；两owner；MEDIUM，同scope事实持续但每candidate检查 |
| R16 | final后decision closed，new evidence才能重开 | a | B | CO | EXEC；closure；重复；HIGH |
| R17 | 禁numeric threshold/hidden count/probability/risk stock | p | B | K | E3；不伪造；低；HIGH |
| R18 | 不submit/new_game/observe/take_action | p | B | CO | EXEC；authority；重复；HIGH |

### Host-owned / conditional surfaces（H，owner=framework，不纳入Candidate正文总量）

| Clause ID | Source / paraphrase | Cadence | Class | Disposition | Evidence / cognition / cost / confidence & reason |
|---|---|---|---|---|---|
| H01 | skills.py all/auto_list/no-skill：读相关Skill后用；可列metadata | p/s | B | K | EXEC；发现技能；低；HIGH，分支互斥 |
| H02 | auto_list：可用code、按环境选shell | conditional p | D | RC | U；一般工程能力；分心；MEDIUM，不作为game strategy步骤，host frozen |
| H03 | workspace_header：AGENT/IDENTITY/USER/memory重要文件用途/工具 | p | D+B | RC | U；通用workspace导航；authority噪声；MEDIUM，不能擅改host，Brief不依赖USER |
| H04 | context file section：非空AGENT/SOUL/USER、HEARTBEAT条件加载 | conditional p | B | RC | EXEC；generic context；内容UNKNOWN；LOW，不能量化未读shared内容 |
| H05 | tools section：文件操作/搜索/memory/任务与其它available tools摘要 | conditional p | B | K | EXEC；可用能力；列表；MEDIUM，按实际ability，非Candidate控制 |
| H06 | tools section：git安全、复杂任务task_tool/并行建议（仅相关工具存在） | conditional p | D | RC | U；通用开发；与single submitter可能张力；MEDIUM，玩家规则禁止第二action authority |
| H07 | todo：多阶段/显式规划用todo，简单任务不建 | p | B | RC | U；整局任务管理；另一plan对象；MEDIUM，游戏loop不需按月份todo |
| H08 | todo：执行阶段粒度、连续步骤合并、独立批次可并行delegation | p | D+B | RC | U；通用流程；与single agent目标竞争；MEDIUM，不作为Team准入 |
| H09 | todo：及时修改changed字段、唯一in-progress（batch例外） | p | C+B | RC | U；进度可见；status维护；MEDIUM，非career cognition |
| H10 | todo：cancel/list/get、验证完成再complete、有新项追加 | p | C+B | RC | U；task completion；额外tool成本；MEDIUM，非whole-game terminal oracle |
| H11 | todo progress reminder：回顾任务与stuck项并及时更新 | conditional tools | C+B | RC | U；执行进展；steering竞争；LOW，enable/interval未核验 |
| H12 | memory passive：仅显式/确需历史才读写，current message优先 | conditional p | B | RC | U；历史恢复；跨局污染可能；MEDIUM，不能把“可写”视为Brief存储合同 |
| H13 | memory passive：identity/USER/长期MEMORY/daily层级和写入路由 | conditional p | D+B | RC | U；generic profile；四存储处；MEDIUM，same-session Brief不走用户档案 |
| H14 | memory passive：先读避免覆盖/重复，edit既有、write新增 | conditional p | D+B | RC | U；通用memory质量；与overwrite Brief不相同；MEDIUM，需区分独立session artifact与MEMORY |
| H15 | memory passive：不记敏感/短暂/直接可推/无价值过程 | conditional p | B | K | EXEC；减少污染；低；HIGH，适用于未来Brief的证据边界 |
| H16 | memory rail：今日昨日daily自动装配，有内容才注入 | conditional p | B | RC | EXEC；恢复；fresh隔离UNKNOWN；LOW，未读取shared内容，不假设为空 |
| H17 | retrieval：enabled且index ready时替代native skills，不ready可建index或原flow | conditional p | B | RC | EXEC；技能发现；额外branch；MEDIUM，四/两文档无需依赖新索引 |
| H18 | compression：summary/state可能再注入，非fresh工具reread | conditional x | B | K | S07-42；上下文延续；可靠性边界；HIGH，summary不是当前public truth |

Coverage ledger：M01–38覆盖instruction所有heading；I01–10/T01–05/C01–04覆盖三个Runner template（插槽M不双计）；B01–24、D01–24、P01–41、R01–18覆盖四Skill所有sections、description和output schema；H01–18覆盖本次查明的host guidance语义组。主动memory、model-selection等未证当前agent分支不当成当前cost；shared profiles全文和host基础agent prompt不是本次可核验的Candidate控制资产，内容及条件配置UNKNOWN，不能声称完整host payload逐字审计。本任务的current Candidate runtime-visible instructions语义覆盖完整，host不确定性显式另列。

## E. Attention / Duplication Findings

### 可复算静态proxy（UTF-8读入、newline归一为LF，chars=Python len，lines=splitlines）

| Surface | Chars | Lines | Semantic clauses |
|---|---:|---:|---:|
| manifest instruction（JSON解码值，不是文件bytes） | 4,373 | 47 | 38 |
| identity template（含占位符，未展开） | 627 | 30 | 10 |
| initial prompt | 253 | 8 | 5 |
| continuation prompt | 254 | 5 | 4 |
| Board含frontmatter | 3,374 | 128 | 24 |
| Delivery含frontmatter | 3,530 | 121 | 24 |
| Planning含frontmatter | 8,748 | 128 | 41 |
| Risk含frontmatter | 2,841 | 98 | 18 |
| total source inventory（未render/非每call tokens） | 24,000 | 565 | 164 |

Skill bodies合计18,493 chars；manifest的4,373为每call常驻策略载体，不与identity rendered第二份相加。启动/恢复时文本保留与attachment处理取决于host，total不是token bill。H共18 semantic groups另计；没有安装tokenizer或估算精确模型tokens。

### 重复semantic family（计覆盖source数量，不是词频或全局occurrence总数）

| Semantic family | Sources / source count | 处置判断 |
|---|---|---|
| same-session/public truth/unknown | M/I/B/D/P/R，6 | kernel与事实层少量高价值冗余；其它owner重述合并 |
| prohibited hidden fields / formula | M/B/P/R，4 | stock/private边界保留；字段名BAN须区分E3 |
| sole submitter / no Skill game call | M/B/D/P/R，5 | 权限正确性保留，详细禁止清单无需五份 |
| action后fresh、one integer非batch | M/I/T/C/P，5 | 高价值重复，不能只移到offline audit |
| recovery/fresh重建unknown | M/I/C/B/D/P，6 | recovery-load合并，当前四读不被本报告静默取消 |
| final safety/one reconsider/closure | M/P/R，3 | 一个final check，删除双marker编码 |
| progression response/local NO_GAIN/reset | M/B/P，3 | 一个事实owner；P要求action-family但B只SNO，是精度张力 |
| verified result≠receipt/praise | M/D/P（Board补事实），3 | 语义KEEP，lifecycle/marker去重复 |

### 每ordinary action要维护的协议规模

- Notes mandatory=CTRL 4字段 + DL 6字段 = **10字段、2 markers**。Planning另输出 PLAN 4字段 + CANDIDATE 2字段；Risk RISK/REASON 2字段。计18 output slots，重复R/G/P/checkpoint等不当作18个独立事实。
- Board定位/状态12槽（SESSION/M/Q/H/D/S/N/O/W/L/E/TENURE）+ REVIEW/RESPONSE/STICKY/EFFECTS/UNKNOWN五组；RESPONSE又有S/N/O/Level。Delivery每item8槽，最多3 active+1 closed，NEXT_ID另1。它们是max schema capacity，不是每步必须填满全部item。
- ordinary loop显式中间对象至少**7**：Board、Delivery、REVIEW_PLAN、MODE/RECOVERY控制对象、CANDIDATE、RISK、executor CONTROL_STATE/PREFLIGHT；quarter再多QUARTER_INTENT。CTRL/DL是这些对象的额外投影，不是新独立事实。
- 可枚举控制labels：CONTROL_STATE3、PREFLIGHT显式PASS1、RB3、MODE2、RECOVERY6、Risk5、progression response3、Delivery stages7、delivery evidence3、DL checkpoint3、context recovery2 = **38 named values across 11 domains**（跨域UNKNOWN等重复单计各域；不是38个唯一字串）。GAIN/NO_GAIN/UNKNOWN维度实例不三倍算。PLAN/CANDIDATE/CTRL/DL又有4个记录标签。

INFERENCE：最值得删除的是“每个简单决策都证明各协议状态完整”的认知任务，而不是安全规则。相邻marker解析争议与D1跨Review不变表明可审计投影既可能拒绝真实行动，也可能接受无用状态。E1没有证明这些字段造成低分，故以family A测试。最危险的 competing authority 是旧Plan决定Delivery relevant、Delivery先于new Planning、Planning又以Delivery rank；以及generic cleanup默认回主线容易被理解为风险解除。显式ownership已阻止实际四agent冲突，不能声称观察到了四个agent争权。

## F. MINIMAL_PERSISTENT_KERNEL

以下为设计草案，未写入任何runtime资产。kernel放manifest/identity现有插槽，保留frozen Runner：

> 你是当前session唯一action submitter。沿用同局ID；禁止第二次new_game、跨局记忆、私有/不可达证据和隐藏公式/答案表。最新observe是当前状态权威，公开反馈和真实结果优先于推测/advertised效果。
>
> 为剩余职业周期选择可兑现的晋升、成长与复利价值。接受合理普通成本；当前公开威胁、资源下行与可达恢复一起决定最小必要保护。风险未有同scope解除证据就仍未解决；工具success、generic praise不是成果或clearance。
>
> 每个fresh observe只做一次决策：核对current state与Brief仍有效→当前binding survival/trust问题→现实承诺/结果兑现→当前高值成长机会；最多比较两项，选一个合法integer并检查最终候选安全。最多一次直接相关替代比较；没闭合或session/动作结果未知就阻断，不盲重发。
>
> 每次只提交一个action，success receipt不更新状态；立即fresh observe后重新决定，Energy不预定配额/余序列。local NO_GAIN只折价有干净证据的已测路径，未测路线不封闭，Level/context变化重验。
>
> 仅material checkpoint做deep review并overwrite同局Brief，普通动作仅更新实际改变的结果/风险/response。可见恢复signal后先同局observe、读取职责文档、核验/恢复Brief；无法恢复写UNKNOWN，提交前仍需fresh legal decision。游戏active时持续loop；只在structured ended或明确不可恢复技术失败时结束。

Difference：10-field telemetry及READY自证、三item七阶段机、并列RECOVERY/quarter intent不常驻；以实际freshness/legality/unknown-stop保留必要安全约束。kernel不包含score阈值、固定H buffer、menu答案或M6保证。上文“公开/可达”的字段准入仅为待Main批准的未来定义；当前main firewall仍照旧。

| Rule destination | Content | 可外部观察/不能外移的界限 |
|---|---|---|
| persistent | session/public权威、唯一提交、成长+failure floor、verified≠receipt、one action→fresh、unknown stop、whole-game | 事后audit可确认tool顺序，不能代替玩家当时执行安全 |
| State & Brief读取 | facts vs advertised/realized、same-scope result/risk、response归因、overwrite/invalidations | 公开state无需每步复制成Board；模型必要状态不能全放局后报告 |
| checkpoint-load | formal feedback解释、objective重排、兑现可行性/承诺取舍、stop-doing、stale-path复验 | 实际调用成本必须future run测；不能声称自动hook |
| recovery-load | exact session、fresh、两文档reread、Brief provenance/unknown、logs必要窗口 | 无host可见signal不虚构检测；compressed summary不是fresh fact |
| external tooling | CTRL/DL/BC/certificates、counts、separator、usage、score/session attribution、post-run evidence/holds | 不修改frozen Runner；现有离线工具可读tool events，semantic判断不能靠marker证明 |
| remove | duplicated inventory cursors/非必要状态名、为了“perfect adherence”加的新规则 | 仅未来Candidate scope；当前合同不被报告废除 |

## G. Strategic Memory Recommendation

`IMPLEMENT_NEXT` 的对象是 **Rolling Career Brief**，一份replaceable same-session摘要。它替代历史型Board/Delivery/Review Plan片段，不复制全部public stats、不是数据库，不使用假想Jiuwen memory API、不与host `MEMORY.md`通用长期profile混合。

| Minimal field | Contents / basis | 原候选字段处置 |
|---|---|---|
| SESSION + BASIS | session、最后核验公开观察时间/月份/Level及来源类型 | LEVEL只作scope锚，current值仍observe；新增最小隔离/失效键 |
| REVIEW + OBJECTIVE | 最近正式反馈、一个下阶段目标与公开检验点；feedback缺则UNKNOWN | LAST REVIEW / PRIMARY OBJECTIVE合并，替代原REVIEW_PLAN |
| RESULT / COMMITMENT | 最重要active result/真实承诺、依赖/公开deadline、已验证与未证实、next result opportunity | ACTIVE RESULT保留；不写七态/monotonic ID；无法忽略的其它承诺压缩在同字段 |
| UNRESOLVED CONSTRAINT | 同scope trust/Health/job/financial事实，何种公开证据可解除 | ACTIVE TRUST RISK扩成所有material failure floor；HEALTH STATUS不复制H数值 |
| PATH UPDATE + STOP | 当前Level/context下最相关已测responsive/stale路径及证据；当前应停/重新验证什么 | RESPONSIVE PATHS / STALE PATHS / STOP DOING合并，缺归因UNKNOWN，不累计每次NO_GAIN |

Writer：Single Executor的State & Brief责任；只有这一份历史摘要拥有写权，Decision读取并在checkpoint提出更新，由同一executor overwrite。不是另一个agent。每field含短公开basis，无法追溯则UNKNOWN，不用长transcript或隐藏ID。五个top-level字段是设计最小集合，信息容纳超限不能删除真实未了义务来凑字数；由Main确定紧凑展示上限而非游戏阈值。

Update：formal Review/promotion或deep-review material trigger时全量overwrite；普通observe仅当 result/constraint/path证据有变化时替换对应字段，SESSION/BASIS更新核验锚，没变化不输出整份重复账本。Read：每次决定前看当前Brief相关field，与fresh observe冲突时fresh优先；不重新读磁盘每action。

Invalidation：换session丢全部；Level变化清tested-path判断；菜单/环境变化重验path而非永久cap；objective完成/不可行更新；generic praise不能清constraint，silent没有warning不清；work item跨Review无新依据就重验未来价值，保留真实未了承诺，不能只靠“过一个Review”退休。未知deadline不自动near。

Storage boundary：优先同一conversation中一个明确current Brief块，checkpoint overwrite其逻辑版本。若未来实现要保证compression恢复，则可考虑same-session独立文件，通过已证read_file/write_file通用能力读写，具体portable路径、install清理与hosted权限须未来静态合同确认。不能假设framework自动保留或注入该文件；本Task不写文件、不改host。文件能力不可证则退回conversation+公开logs重建，future implementation不能在不明条件下宣称durable恢复。

Recovery fallback：同局fresh observe→读取两职责文档→优先公开logs的最小相关Review/result/warning窗口→对Brief各字段验basis；丢失部分UNKNOWN，不因summary说“恢复完成”就信。存储不可用不回滚成跨局memory。

Failure targeted：E1的D1跨8次Review/5次Review长期未证实、generic praise clearance支持“需要统一revalidation责任”的假设；**并没有证明Review feedback在所有run被遗忘**，repeated rediscovery频率UNKNOWN。已有Review Plan本就很小，因此本推荐价值来自替换/失效，不是新增9字段。memory没有独立Skill理由：它就是State & Brief的一部分。

## H. DEEP_REVIEW_TRIGGER_TABLE

将深推理压成三问：①哪些公开结果/失败真正改变了旧假设（rewarded/failed/stale）？②下一目标与可兑现路径是什么、哪些应停？③什么结果/风险仍持续、何种证据让它失效？包含Plan七问的等价信息，不要求七段自报。

| Trigger / public evidence | Why material / inputs | Rewrite / exit | False-positive risk |
|---|---|---|---|
| formal Review / no-advance / promotion；E1各run首次formal feedback | 重排objective、Level scope变化；fresh feedback+Review前后Brief+公开result/choices | REVIEW/OBJECTIVE全量重写，promotion清PATH；得到一个next objective/checkpoint后退出到ordinary loop；同一Review/promotion合并一次 | 不把同月多次observe当多次Review；grade不是精确formula |
| new/escalated major trust/job/compliance warning；E1 RUN19 | 目标约束可能失效；同scope公开warning/history+当前repair menu | CONSTRAINT/STOP/OBJECTIVE必要更新；选一可行bounded response后退出，constraint继续保留直到clearance | 普通摩擦/每天同warning不是每步deep review；可即时safety check不调用第二reviewer |
| major Health/safety shock或当前downside使普通活动不可行；E1 RUN17/S09-27 | 下行和可达恢复改变可选路径；fresh资源、公开成本、负荷、恢复菜单 | CONSTRAINT/OBJECTIVE/PATH必要更新；一个保护方案与公开解除basis后回loop，不等H补满 | 不固定H阈值、不把任一次drop当major；无法可靠判material则ordinary安全比较 |
| major verified result / failed commitment / blocker让兑现路线变化；E1/E4 | 已完成目标或不可行旧路线；item-linked公开结果+deadline/依赖+legal menu | RESULT/OBJECTIVE/STOP重写，明确尚未证实部分；选下一现实检验点后退出 | generic Output/report/praise不是verified；小进展只更新field |
| repeated clean NO_GAIN 且当前高值path失效；E1 RUN10/RUN08 | 当前路由过时；同scope已测path、归因证据、开放替代 | PATH/STOP更新，至多一个bounded替代比较，后续结果再更新 | 不固定次数；mixed delta不clean，一次无增益只更新response、不深评 |
| material opportunity-set change / goal infeasible；E4不同结果路线 | 时限、资源、可达完成条件改变策略；fresh合法menu+现有commitment/Brief | OBJECTIVE/RESULT/PATH，选当前可实现路线后退出 | 每个Story都有新menu，只有它推翻旧objective/重要assumption才触发 |

Trigger去重以公开事件/反馈内容及Brief basis识别，不用private event ID；同一checkpoint只评一次，恢复后证据缺失UNKNOWN。Exit必须是一份可行下一期目标+persisting facts+停止事项，随后提交仍要fresh合法决策。Deep review不是game action、不是新增provider API、不是per-action审计Team；未来run才测它是否真的节省ordinary deliberation。

## I. Four-Skill Decision

| Skill | Failure provenance / supported benefit | Independent Skill necessity / overlap / cost | Merge loss / final recommendation |
|---|---|---|---|
| Board | S07状态复制/混合effect/recovery错误（CURRENT_STATE及S07-42）；fresh事实和unknown直接支撑correctness；S09 cap drift说明response有价值但未保证执行 | 独立事实责任必要，独立文档可并Brief；与manifest/Planning重复firewall/recovery/response；每observe全Board 17 groups，不需全部自报 | 失去易逐字段audit格式，保留fresh status权威/clean response；合入State & Brief |
| Delivery | ADR v7公开commitment/result生命周期设计；E4真实成果链有描述支持；E1 stale D1证明lifecycle本身未兑现控制收益 | completion≠claim必要，七阶段/ID/NEXT_ID/三item/六marker独立模块收益UNPROVEN；旧Review Plan relevancy与new Planning先后产生接口张力 | 失去统一DL parser和完整库存格式，不失去真实承诺/verified result；合入Brief的RESULT |
| Planning | v7d普通gap churn与v7i verbose closure（CURRENT_STATE），v7o/v8a结果提供donor参考；没有证明按四Skill分解导致好成绩 | 唯一strategy owner必要；与M/R复制MODE/closure/recovery，current 8,748 chars最重；每步Plan+Recovery+quarter intent可并 | 失去长期层级树/telemetry细节，保留objective/feedback/ownership/growth/兑现；成为Career Decision主体 |
| Risk | 公开trust/安全material检查，E1 RUN19反证Health足够；S09-10 fidelity ALLOW/PASS差异不证明换choice或收益 | selected candidate final safety必须；独立五值报告不必，ordinary quick gate可一个步骤；MODE/constraint与P重叠，RB/R与M重复 | 失去独立Risk marker但必须保留最终检查与一次替代权限；并Career Decision中的final check，material facts由Brief持有 |

`FOUR_SKILL_DECISION = REDUCE`。最小职责图（设计，不是实施）：

```text
fresh observe / same-session public history
  -> State & Brief: current facts + one overwrite strategic brief
  -> Career Decision: current objective/value + binding constraints
                    + one candidate comparison + final safety check
  -> Single Executor: legality/session/unknown-outcome check -> one action
  -> fresh observe
material checkpoint -> same-agent deep review -> overwrite Brief -> ordinary loop
```

四个失败族不会因文件合并消失；不删除事实/结果/规划/安全职责。RECOMMENDATION confidence MEDIUM，收益NEEDS_EXPERIMENT。两文档减少instruction handoff与恢复读取，但可能使final safety被成长偏好吞没；这就是family A的主要falsifier之一。若静态design无法保持可识别final check，应返Main，不以精简为由删除。

## J. MECHANISM_DISPOSITION_MATRIX

| Mechanism / source | Disposition | Evidence → value / attention cost → family relevance |
|---|---|---|
| early promotion / compounding v6/v7o/v8a | RETAIN | E1/E4 early chain与后期资本描述；growth prior低成本，非M6规则；A |
| broad visible S/N/O/ownership donor core | RETAIN | E1高参考，v8a已含v7o；低成本竞争prior不硬排序；A |
| visible result conversion | RETAIN | E4兑现链与公开反馈差异；比generic reporting更具体；Brief/Decision的核心 |
| full Delivery lifecycle/ID/marker | REJECT | E1 stale D1未证控制价值；七态/ID/marker负担；A只保留commitment/proof语义 |
| same-scope trust persistence | RETAIN | E1 RUN19、20、21 false clearance；constraint持续但不强制重复cleanup；A |
| v10h dynamic survival reasoning | RETAIN | E1 RUN17/Health forensics支持下行与可达恢复比较；无fixed buffer；A最小语义移植 |
| fresh state / receipt/public boundary | RETAIN | EXEC，E1 fresh pairing；necessary correctness低成本；两family也不能删 |
| field-name-only HiddenRisk/effect BAN | RECONSIDER | E3合法advertised delta与stock混同；需Main准入决策，不能静默改main；A实施前gate |
| hidden cap/threshold avoidance | RETAIN | E1重复cap drift；不伪造公式，但合法公开feedback可形成有置信度假设；A |
| Energy recipe policing | REJECT | E0/E1 hardening无稳定突破；不能再加quota/每NO_GAIN一句；保留one-action-fresh routing |
| marker/certificate/BC自报/preflight machinery | REJECT | E1 marker/BC不证明语义；不要runtime格式作game gate；真正session/legal/fresh/final safety/unknown STOP RETAIN |
| context recovery | RETAIN | S07-42压缩丢reread；部署instruction而非虚构hook；A两文档+Brief核验，真实效果待跑 |
| full current Board representation | RECONSIDER | facts necessary，全量state复写成本；Brief scope+fresh observe直接消费替代；A |
| Review Plan | RETAIN | E1正式反馈checkpoint描述价值；替换为Brief REVIEW/OBJECTIVE一个owner，非附加副本 |
| ordinary decision budget | RETAIN | S09-10/当前contract有限比较；缩short output但不反复replan；A |
| v10 constitution/head kernel/anti-cap certificates | REJECT | E1静态覆盖非得分证明；只取source distinction/fresh safety，不整包移植 |
| v11 single-step Energy | RETAIN | EXEC已有main语义，避免batch；不是v11独有收益证据，A |
| v11 stale Delivery降权 | RETAIN | E1长期D1反例；checkpoint重验价值而非永久丢承诺；A Brief |
| v11b early result feasibility | RETAIN | E4 deadline/可兑现路线差异；RUN21仅early CLEAN；取conditional比较，不移植v11b全包/保证晋升 |
| v9a bounded untested high-value probe | RECONSIDER | E1 RUN10 qualifying机制未确证；可作为当前两候选比较的替代，不独立第三family/强制exploration |
| v6 sustainable Growth over ordinary Soft Cost | RETAIN | 75.29 reference但causal未知；与v7o core重合，语义校验不额外transplant |
| v6 STALLED / CP / Risk Budget / joint Energy枚举 | REJECT | S09-10显示old S语义不同；额外tree/marker、与fresh sequential接口冲突；A不移植 |
| donor old recovery detection / old X markers | REJECT | S09-10不移植、S07-42无deployable hook；保留current observable-signal边界 |
| repeated live Reviewer intervention | REJECT | E1投影遗漏/延迟/semantics不证收益；audit可保留外部，B未justify |

## K. Candidate Family A Design Card

| Item | Design |
|---|---|
| Hypothesis | 一个可核验/overwrite Brief + checkpoint深评替代四套每步协议，可减少stale objective/result/risk与重复推理，同时保持growth/safety；收益未证 |
| Formal base | latest main@execution SHA + frozen candidate-v8a；不从v11/v11b实验branch起步 |
| Donor | v7o core已在v8a；v6仅共同语义参考，S09只取J选中机制 |
| Shape | single submitter，两职责文档，ordinary one-pass，same-agent checkpoint review |
| Persistent kernel | F草案；metadata/body装配仍使用frozen Runner路径 |
| State/memory | G五field Brief替代历史摘要，不cross-game/not append，不独立第五Skill |
| Review | H material triggers，同checkpoint一次；恢复读文档与public basis |
| Retained | promotion/ownership/broad growth、verified result、trust/survival continuity、fresh/one-integer/final safety、local response、bounded choice |
| Rejected | v11 lineage整包、marker/certificate优化、recipe/cap lookup、七态DL库存、重复层级、第二action writer |
| Minimal transplant | S09动态下行与可达恢复比较；same-scope risk不因praise清除；checkpoint重验stale item；early result feasibility比较。其余在v8a已有 |
| Expected benefit | 更少重复状态输出、及时失效与兑现调整；不能预报加分或token降低百分比 |
| Main failure mode | 合并让safety被growth吞没；Brief变新标签账本；checkpoint频繁退化per-action；无可恢复持久state |
| Falsifier | 机制被观察到真实执行，仍反复不按公开basis更新/清风险/追stale result，或同类安全失败未改善；有效full samples无增长/资源效能信号则架构未获支持，非“再加一句” |
| Rollback | 保留frozen v8a exact baseline/package身份；new candidate独立标识；失效返回Main选v8a，不修改官方fallback |
| Next implementation scope | 另开repository-write Plan，限定manifest/两职责Skill设计、canonical metadata/package与静态source/legality checks；明确AGENT_RUNTIME_CONTRACT架构delta；如需storage/field准入合同先Main决定。不在此Task写patch或运行 |

非main移植理由必须逐项成立：

| Evidence → Why → Minimal scope → NOT transplanted |
|---|
| E1 v7o71.83与S09-10 donor mapping → growth/ownership仍是最有依据baseline → 使用v8a已存在core、非新donor包 → 不导入v7o旧X/quarter序列/无可见signal检测 |
| E1 v675.29 adherence FAIL → 不以协议完美替代成绩目标 → growth容忍ordinary成本作cross-check → 不导入旧STALLED/CP/阈值及quarantined Dev机制 |
| E1 RUN17/27 → 显式warning之外也需公开下行/可达恢复比较 → 一条动态constraint比较 → 不导入Health fixed buffer、engine terminal公式给玩家 |
| E1 RUN19–21 → cleanup不等于clearance → Brief保留same-scope unresolved事实/解除basis → 不导入hidden stock/counter、cleanup配方 |
| E1 stale D1 → 保存state不足以控制 → checkpoint重验result relevance/feasibility → 不导入v11全lifecycle与每步证书 |
| E4 / RUN21 partial → deadline/result兑现值得试 → 当前合法路线的conditional feasibility比较 → 不导入event title答案、固定M6/O值或v11b完整包 |

## L. Candidate Family B

`FAMILY_B = NOT_JUSTIFIED`，不是永久拒绝Team。

FACT：Runner支持`mode=agent|team`，`resolve_run_mode`与WebSocket mode传递已证；框架有TeamManager/config_loader、team角色与session管理模块。**mode enum不证明提交bundle能固定checkpoint-only角色、Reviewer工具隔离或同一个executor拥有全部action权限。** install只装manifest/Skill并写identity，未展示任意Team topology/config被自动安装。

Hypothetical wiring（只作feasibility分析）：Executor从participant public input生成Brief+compact公开checkpoint轨迹；Reviewer只读，不获得MCP action/new_game与shared写入；返回对一两个stale assumption、next objective与风险的challenge；Executor以fresh当前事实决定、单独提交。是否能从允许solution做到工具级隔离/准确context只靠静态已读代码UNKNOWN。没有需要也没有执行live probe；该unknown不被包装成可实现Team推荐。

Cost：至少一份独立角色instruction与checkpoint context序列化、一次Reviewer模型推理、一次Executor吸收/冲突裁决；额外tokens/runtime量UNKNOWN，不能记零。独立性还需不同假设搜索任务，单纯重读Executor的Brief容易共享错误，Reviewer“PASS”是另一自证标签。Coordination失败包括stale snapshot、projected menu丢effects（E3已实际发生于外部audit packet）、双submitter、超时/迟到意见、同scope风险遗漏，以及同样模型相关错误。

E1表明single agent有stale semantics，但没有证明“精简+same-agent checkpoint review”仍存在必须独立Reviewer解决的瓶颈。现行live Reviewer主要审计/停止分类，不是战略mentor收益实验。因此B未通过必要证据门。重开条件：A机制执行已确证，但连续material checkpoint仍有明确tunnel vision反例；离线相同public packet上independent review给出有来源、executor错过的可行动假设，且静态solution证明sole submitter工具隔离与成本可容纳。这个条件是未来Main考虑理由，不授权建立Team或额外family。

## M. MINIMAL_HIGH_INFORMATION_EXPERIMENT_MATRIX

仅设计，live budget consumed=0。一个major family A；B不安排对局。不能把coherent reset的多个delta归因到某一字段；预算不足不再拆v12a/b/c。static implementation之后仍须单独Game Gate，含次数/成本/stop与shared串行窗口。

| Unit / budget tier | Exact architecture delta / comparator | One run can / cannot prove | Signals / failure / stop |
|---|---|---|---|
| A-SCREEN / 1 authorized full-run slot | K/G/H/I coherent A vs frozen v8a历史RUN07/08；历史是reference非随机control | 能证加载、Brief/checkpoint触发/失效/最终安全的单次执行与自然48m或terminal；不能证stable75+、superiority、因果拆解。`SCREENING_ONLY` | 成功=真实执行且结果/风险及时更新、ordinary负担可测、合法自然结果；低分单局不自动否定，具体重复旧failure可反驳机制。技术failure单列partial、不作策略failure，不自动replacement；本slot后return Main |
| A-REPLICATION / minimum 2 A full-run slots total | exact same A bytes/config，不边跑边patch；参考同bytes v8a59–72.65。若预算容纳fresh control，可选择2 A +2 fresh v8a，共4槽 | 第二局可证描述性可重复与不同轨迹failure modes；2或4样本仍不能推稳定概率/hidden Test/显著因果；历史和fresh配置不可混装 | 看完整分布、early progression链、verified results与constraint处理，以及token/runtime/continuations。稳定性只写观察次数。A repeated机制失效/安全破坏则stop回Main；高低variance不靠追加句子修 |
| B-REOPEN / no run allocated | 仅在L门通过后另Plan比较same-agent checkpoint与independent Reviewer，保持同A Executor | 目前无Single-Agent lean瓶颈证据，不能调用Team填空 | gate未过维持NOT_JUSTIFIED；不能借A失败自动建B；最多两family，第三family返Main |

技术失败处理：provider/transport/max_continuations等独立记录；动作结果未知只在明确授权范围observe核对，仍unknown STOP并留证；bounded预算耗尽即review，无自动补跑RUN21/新局。自然terminal是有效游戏失败；authored-policy偏差可记录，不把普通S1 drift直接censor成无法计分，run-invalidating问题按未来明确contract处理。

最小观测指标：Candidate/config/session与最终score/horizon/Level，first-fresh正式Review/promotion（不混月末），公开result/constraint的Brief更新basis，material trigger频次、ordinary/action reasoning长度、已报告tokens/runtime/continuations、技术失败类型/未知。缺usage=UNKNOWN。尽量复用现有tool events/offline audit；不为marker退休重新建证书系统。高分一局只支持继续研究，低分一局先判机会/机制是否触发，不宣称architecture causal failure。

## N. Residual Unknowns / Main Gate Questions

十个核心问题闭合索引：runtime价值=D/E；minimal kernel=F；memory=G；deep checkpoint=H；四Skill=I；A donor=J/K；v6/v7o/v8a/S09处置=J；B独立性/feasibility=L；高信息矩阵=M；remaining gate/边界=N。每项为设计判断或明确UNKNOWN，不用Plan hypothesis充事实。

Main只需决定三项实质问题：

1. 是否接受A coherent reset作为下一独立Candidate的repository-write设计方向，允许两Skill/一个Brief替代当前四Skill协议，保留所有session/fresh/action safety？如不接受，维持frozen v8a，不继续局部句子硬化。
2. 是否接受E3的官方可达delta与不可达stock区别进入未来Candidate合同？最新main仍有旧字段禁用，S09属于evidence-only；不能因为引用E3自行改Source Lock/Runtime Contract。未决则未来Candidate继续当前准入边界，相关排序收益UNKNOWN。
3. Brief存储采用conversation先行还是允许same-session文件，以及后续live预算为1 screening或重复样本层级？portable file recovery和hosted permissions未知，implementation必须静态证明可用或选logs fallback；任何provider/service/game另行明确授权。

其余UNKNOWN：DeepSeek实际attention分配；compression后Brief恢复率；两个职责文档是否削弱final safety；独立Reviewer的净增益；机会variance与policy delta对score贡献；host conditional rail/shared profile实际payload。没有新增hidden公式调查或host修改请求。所有必要raw仍由既有hold owner保管，本报告不解除hold。

### Verification / execution boundary

Tier0：required source存在、execution/pinned SHA核对、报告A–N结构/Clause ID与计数、Markdown表格与相对链接/main路径和pinned对象路径可解析、仅允许单一报告diff、`git diff --check`。不运行历史test suite/Runner validate/provider probe；counts用根`.venv/Scripts/python.exe`静态读取文本，无依赖同步/安装，无临时committed verifier。交付commit及remote状态在TASK_RESULT记录，避免报告包含自身commit hash。

`READY_FOR_S10_ARCHITECTURE_GATE` · `NEXT_GAME=NOT_AUTHORIZED` · `MAIN_V8A_FREEZE_UNCHANGED`
