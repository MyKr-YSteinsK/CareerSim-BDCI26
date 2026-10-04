# S10-15 — Execution Adherence Root-Cause

**COMPLETE_WITH_CONTEXT_LIMITATIONS / IN_FLIGHT_EVIDENCE**

唯一 primary decision：**MIXED_NO_SINGLE_SAFE_PATCH**。

同一 v6d 出现的差异不能归结为单一“压缩丢规则”或“Risk 后重想”。直接证据同时支持：详细 Skill body 在首次压缩后的捕获上下文中消失；Run02 摘要丢掉 report/intensive 效率条件并强化 intensive 的既往收益；首次压缩前已经存在规则应用偏差及旧 Level response 携带；两局都经常提前制定 Energy bundle；部分 intensive 是当前公开 response 支持的合法例外。普通 streaming 请求缺少完整 messages，不能据此宣称已找齐每个决策的实际输入或一个安全的单点修复。

## Identity / scope

Branch `codex/s10-15-execution-adherence-forensics`；base `ce92da5cda9c5da2e2b4f2140e35880e8ea77a6a`（依赖未合入 Run02 的证据分支，串行 checkout，无 worktree）。Exact Candidate `candidate-v6d-promotion-portfolio-rebalance` / `e7e8ab44dd85a29135eb089ef29de8fed298f4a4`。Run01 accepted commit `5eb108b55a9f252d4fd6ff4561120d353f9d124b`；Run02 accepted commit `ce92da5cda9c5da2e2b4f2140e35880e8ea77a6a`。两局 preflight source/package identity、三 Skill、Runner `f61c738c72e51b77298cc1c14c7c6ebf4b6c527d`、Provider config hash、dependency versions 一致；原12+12 held files重新核验 hash/bytes。

Candidate/Skill/manifest/Runner/dependencies/provider/retry 未改；新 Candidate、install、service、Provider、game、DB/hidden-state/Test/formula 访问均0。只写本报告、compact JSON 和 branch-local CURRENT_STATE；不提交 raw transcript/LLM input/output 或重复 held artifacts。Result commit 是携带本报告的 Git commit；push/远端身份与 clean 在 TASK_RESULT 核实，不在文件中制造自引用 SHA。

## MODEL_ACTUALLY_SAW：证据等级

四个 non-streaming compressor receipt 的 `messages` 是直接输入证据；同时保留了对应 output。Run01 两个窗口为 scoped llm lines159/410；Run02 lines147/297。启动 SDK 自检请求与 compressor 请求分开计数，不把启动探针当游戏决策输入。本任务没有任何 Provider 请求。

普通 streaming llm_call_start 只有参数，没有完整 messages（Run01 408、Run02 402）。即刻 post-compression 和 Run02 late-game action 输入 **UNKNOWN**。所选决策在随后 compressor input 中保留的 assistant/tool history，可直接证明该历史片段及其当时被压缩看到的规则，不能偷换成更早那个决策的完整 request。Run02 late M39/M48 只能以 held transcript、fresh public state、最后已捕获摘要和无 reread 作有界推断。摘要文字、前序 reasoning 不是源 Skill，不能视作策略权威。

### Persistent layer

四个实际 compressor `system` 消息均含冻结 manifest 的完整 participant instruction 意义文本。日志呈现中原文的 `→` 箭头缺失；做且仅做箭头/换行 normalization 后完整匹配，不声称字节原样。源与安装 Candidate bytes仍精确不变。系统消息每个26083 Unicode chars；同局两次完整 system SHA相同。跨局完整 system SHA不同：框架 AGENT.md/SOUL.md 拼接顺序及独立项目目录标识不同；participant block未变。这不是“相同完整输入”实验，也不是 Candidate identity mismatch。

直接证明：首次压缩前 manifest PRESENT；首次压缩后、第二次压缩前 PRESENT；Run01 M47 late捕获输入 PRESENT。即刻恢复请求及 Run02 M39/M48 late streaming 的 persistence **UNKNOWN**。不能仅凭框架设计升级为全时段 PRESENT。

### Loaded Skill layer

两局首次捕获输入都包含完整三 Skill：Planning6294、Risk2581、Board1879 chars（Run01 numbered read_file显示移除末尾换行后少1，normalize后全文等价；Run02 skill_tool内容全文等价）。读取方式不同：Run01实际多行编号文本；Run02 Python repr 内容带字面量 escaped newlines。**body存在**不等于呈现形式或注意力完全一致；格式影响 UNKNOWN。

两局第二次捕获输入均**无三 Skill body**，只有上一个压缩 memory block、后续 public tools与推理。两局均0次 startup之后 Skill reread。Planning、Risk、Board verdict均为：first body PRESENT，second body ABSENT，summary PARTIAL。这是真实上下文丢失证据，不是从 repository contains 推测。

六条关键 policy 的摘要保留情况：

| 条款 | Run01 summaries | Run02 summaries |
|---|---|---|
| broad S/N/O | PARTIAL：状态和 Output primary，缺完整组合问题 | PARTIAL：更偏 Output gap |
| Network first-class | ep1PARTIAL、ep2PRESENT | 两次PRESENT |
| report/intensive resource efficiency | PARTIAL：保留“report而非intensive”的既往启发式，非完整条件 | 两次ABSENT_AS_RULE；保留 intensive 正收益先验 |
| fresh comparable flat reroute | 两次ABSENT_AS_RULE | ep1仅记录repeat flat/possible cap；ep2ABSENT_AS_RULE |
| one-step fresh-result rerank | PARTIAL：observe规则在，但指示continue bundle | PARTIAL：observe规则在，没有完整rerank条件 |
| survival constraint | 两次PRESENT | 两次PRESENT |

Level-response reset 条件四个 summary均未作为规则保留。完整 body缺失不等于所有 policy信息归零；survival、Network与会话/整数合同仍有信息残留。

## 全部四个 compressor epoch

“月份”取**捕获输入中最后公开 observe**，不把 output receipt期间已有新状态倒填为 compressor看到的状态。两种边界均保留在 JSON。具体恢复消息送入第一个 streaming request 的时间/内容 UNKNOWN。

| Epoch | input覆盖月份 | pre-context | 覆盖边界后首个tool | 覆盖边界后首个Energy |
|---|---|---|---|---|
| Run01 #1 | M18 | 三body完整 | observe raw605 | M18 准备汇报材料 |
| Run01 #2 | M47 | body缺失；旧summary | observe raw1589 | M48 处理历史埋雷 |
| Run02 #1 | M17 | 三body完整 | action raw557 | M18 准备汇报材料 |
| Run02 #2 | M34 | body缺失；旧summary | observe raw1137 | M36 健康恢复 |

- Run01#1：输入止于 M18 cleanup成功，summary说下一步observe，再continue report/Main；详细效率/flat条件被缩成既往路径。receipt时间之后第一个tool是observe raw613；按input覆盖是observe605，后report609。均未重读 Skills。policy **PARTIALLY_LOST**。
- Run01#2：捕获输入 M47，summary保存会话/状态与report优先启发式，仍复述完整恢复合同；receipt期间状态已到M48。input覆盖后observe1589，receipt后observe1597，下一Energy cleanup1617。未重读，policy **PARTIALLY_LOST**。
- Run02#1：捕获输入 M17 S34；receipt时间最新公开S35。**summary的S34与输入一致，是覆盖滞后，不是编造状态**。output直接要求take_action，且没有保留完整恢复合同。覆盖后首tool action557，receipt后action565，均不是新observe。随后M18report597；M21/27/33intensive。效率条款缺失与行为时间序列相符，但不证明因果。policy **PARTIALLY_LOST**。
- Run02#2：捕获输入 M34；receipt期间已到M35。summary下一步observe；覆盖后observe1137，receipt后observe1145，随后M36Health1189。summary把M30 Main写成低调避险，但实际raw1013是关键项目；又把intensive+2概括为观察效果，忽略M33flat。后续M39/48intensive；没有三 Skill reread。policy **PARTIALLY_LOST**。

四次 recovery合同未完成；三次先observe不代表完成rebuild，Run02#1还先action。摘要有事实/估计误差，不能把它当fresh state。没有证明上述误差独立造成某次晋升或分数差。

### Pre / post Energy

顺序 report / Network / intensive / Health / cleanup。默认前后按第一个 compressor receipt timestamp，同时列实际input覆盖边界；两者均不冒充已知 summary delivery时间。

| 边界 | 前 | 后 |
|---|---|---|
| Run01 receipt前 / 后 | 6/2/0/2/4 | 13/3/0/8/3 |
| Run01 input覆盖前 / 后 | 5/2/0/2/4 | 14/3/0/8/3 |
| Run02 receipt前 / 后 | 3/3/2/1/2 | 7/3/5/9/2 |
| Run02 input覆盖前 / 后 | 3/3/2/1/2 | 7/3/5/9/2 |

Run02 intensive M3/M15在压缩前；M21/M27/M33在首次压缩后、二次前；M39/M48二次后。Run01首次压缩后仍13次report（按input覆盖14次）、0intensive。**时间关系不能证明压缩是唯一原因**：两局都失去body，但摘要继承的先验不同，且Run02早已出现偏差。

## 七个 Run02 intensive case

A=context loss；B=rule present but ignored/application failure；C=stale plan；D=deliberation reopen；E=state/clock/response drift；F=valid exception；G=UNKNOWN。primary不是已证因果占比：A三案为有上下文丢失 witness 的**有界解释**，具体action prompt仍UNKNOWN；不能把根因计数当因果统计。

| Case | Level / S/N/O/W/H/D（E均3） | PRIMARY + SECONDARY | 置信边界 |
|---|---|---|---|
| M3 | L1 / 7/3/-1/1/7/10 | B + D | PARTIAL |
| M15 | L3 / 29/12/7/4/10/10 | E + B | STRONG_FOR_STALE_RESPONSE |
| M21 | L4 / 48/16/13/8/9/10 | A + B | PARTIAL_CONTEXT_LOSS_NOT_CAUSAL_PROOF |
| M27 | L4 / 63/28/24/12/9/10 | A + C | PARTIAL_CONTEXT_LOSS_NOT_CAUSAL_PROOF |
| M33 | L4 / 88/36/26/17/8/10 | F + C | SUPPORTED_EXCEPTION_WITH_LIMITS |
| M39 | L5 / 106/38/28/24/9/10 | A + B | PARTIAL_LATE_REQUEST_UNKNOWN |
| M48 | L5 / 127/53/38/31/9/10 | F + D | SUPPORTED_EXCEPTION_WITH_LIMITS |

1. **M3，B+D**：raw105；当前report UNKNOWN，report1E与intensive2E的名义Output/能量效率相当，后者多Health成本。没有具体必须intensive的deliverable。模型把negative Output的急迫感与“Soft Cost不自动否决Growth”当作intensive理由。完整body在首次捕获history，Run02M9还会明确应用同一效率条件；即刻M3request UNKNOWN。RiskPASS后重想，但最终仍intensive，D不是已证选择变更。
2. **M15，E+B**：raw501；report的M9flat来自L2，M12已升L3。模型直接引用fresh-flat条款却沿用旧Level的flat，没有重置可比性，最后选择intensive。Health10/AVAILABLE解释成本可承受，不能让陈旧response变fresh。近期formal反馈与当前positiveHR区分保存。
3. **M21，A+B**：raw701；L4、H9，reportM18cleanGAIN。详细效率规则不在保留summary，persistent“AVAILABLE/Soft Cost”被读成必须Output-max。计划intensive+report；没有新的独立deliverable。丢规则和错误应用都有证据，具体request仍UNKNOWN。
4. **M27，A+C**：raw901；reportM21GAIN，H9，模型视S/N已高、Output唯一gap，定intensive+report。raw909只核对新delta并做原定report。没有证明更高Health/能量成本带来独立公共价值。
5. **M33，F+C**：raw1093；同L4的M27report刚出现cleanflat，AVAILABLE且HR已改善。按冻结政策允许尝试不同Output路径；不是因为最终flat就倒推错误答案。intensive本次也flat，下一Health原已计划，只是notice后继续，不能算清楚的flat-driven rerank。
6. **M39，A+B**：raw1293；新L5，M36reportGAIN，H9。latest summary没有效率条件，当前reason主要是Outputgap/更大nominalgain。late请求UNKNOWN，A不作确定因果。其firstbundle末项是Network；freshresult后实际改Health，是可确认TRUE_RERANK。
7. **M48，F+D**：raw1593；同L5 M45reportfreshflat，H9/positiveHR/AVAILABLE，使不同Output路线具合法例外。发生在最终Review后，不能拿“下一晋升窗口”合理化长期收益。intensive也flat后改Health1601。虽然反复改未来bundle顺序，当前gate后的intensive提交没变。

每案完整publicstate、formal feedback、最新HR、report/intensive/Network recent clean response及Level可比标记、合法替代/cost、适用条款、trace/message/原始行引用都在JSON。没有事件标题→答案表。主类分布 **A3/B1/E1/F2，C/D/G0**；secondary另记，不混入primary。S10-14的M33/M48 UNKNOWN以新增same-Levelflat证据细化为VALID_EXCEPTION；不改旧报告或Candidate。

## Run01四个control与bounded pairs

Run01 M3 raw105：直接引用低成本report条款，最终Network→report→Health；H4而Run02H7、O2而Run02O−1，不能声称完全相同输入下随机选不同。

M9 raw305：intensive原本被认真考虑，最后因反复HRwarning/谨慎Risk选择report；不是单纯规则更清楚。M15 raw505：fresh积累风险warning，cleanup+report，避免加重警示维度。M42 raw1409：L5、结果/关系反馈，report+report+Network；body已不在但summary保存report-over-intensive启发式，说明bodyloss不必然使intensive增加。

| Run01 vs Run02 | Comparability | 主要边界 |
|---|---|---|
| M3 vs M3 | MEDIUM | 同L1/menu/N3，Health与Output急迫性不同 |
| M9 vs M15 | LOW | 不同Level/HR/response历史，只比较reasoning |
| M15 vs M15 | MEDIUM | 同L3、接近状态，warning与positiveHR不同 |
| M42 vs M39 | MEDIUM | 同L5、相近S/N/O/H，tenure/正式反馈不同 |

没有 HIGH_COMPARABILITY / exact full-input pair；不将generic Energy title相同当同状态，也不将所有差异称为“纯随机生成”。

## Quarter plans / semantic rerank

两局各16/16季度在首Energy前明确写多个动作bundle；这不是数组调用，也不是自动证明每次策略错。后续动作按如下边界评估：TRUE_RERANK是fresh result后实际比较合法备选/调整ranking；PLAN_CONTINUE是直接执行原定项，无可见重排；MIXED是新状态参与但主要沿原计划；UNKNOWN是trace不足。整数正确与observe正确不证明semantic rerank。

| Run | 后续Energy动作数 | TRUE_RERANK | PLAN_CONTINUE | MIXED | UNKNOWN |
|---|---|---|---|---|---|
| Run01 | 25 | 0 | 18 | 7 | 0 |
| Run02 | 21 | 3 | 15 | 3 | 0 |

Run01 raw113：Networkflat后说“其余待结算、继续计划”，未按已取得freshstate折价。Run02 raw305：先reportGAIN后照旧重复；raw313第二次flat才真正改Network。Run02 raw1101：intensiveflat后“let me not worry”，继续预定Health。Run02 raw1301/1601：分别从Network/report计划真正改Health。PLAN_CONTINUE包括显然合法的生存续项，**不能把18/15全部等同战略违规**；它证明完整rerank合同没有被普遍落实，不能单独解释Run01/Run02mix差异。

## Clean Output flat handling

| Run | ADHERENT | NONADHERENT | AMBIGUOUS |
|---|---|---|---|
| Run01 | 0 | 2 | 2 |
| Run02 | 4 | 0 | 1 |

Run01四个flat：M9后Network/Health原已计划→AMBIGUOUS；M18/M21后继续gap驱动report没有discount→NONADHERENT；M33→M36新反馈/状态可能提供独立visibility，未显式discount→AMBIGUOUS（不照抄旧FAIL）。Run02五个flat：M9明确折价、M27在M30生存约束后下一growth M33转路线、M45下一M48转路线、M48改Health→ADHERENT；M33的Health原已计划→AMBIGUOUS。这些标签是bounded semantic review，不证明更高得分。没有确认动作后虚报observedGAIN；cap speculation未升级为永久cap事实。

## DecisionClosed：是否真正改变action？

有界10个重要Energy witness：Run01 M9/M12/M15/M48；Run02 M3/M15/M21/M27/M39/M48。**VERBOSE_ONLY10、CHOICE_DRIFT0、STATE_CONFUSION0、UNKNOWN0**。范围是这些post-final-gate当前候选，不是全游戏的无限计数。第一轮比较中的改候选发生在最终gate前，不算违反闭合；反复变未来bundle后续项也不偷换成当前action改变。

两局仍有明显重开与大量无效推理；M48等future bundle来回变化有attention成本，但没有多个“原本正确的已gate当前项被改错”的证据。**不支持DELIBERATION_CONTROL_SUPPORTED**，也不把这里的0扩展为全局无drift。摘要错误另审，不反向归给deliberation。

## Recovery contract / attention budget

OptionA：合同语义正确，实际4/4未完成；再复述同一合同没有收益证据。OptionB：依赖模型主动恢复很不可靠，但失败不授权直接删除fresh-state安全合同。OptionC：稳定system层可能保住少量efficiency/rerank/Level-response-reset条件；然而已在persistent layer的recovery/DecisionClosed照样未执行，迁移并非被验证的安全 cure。OptionD：即刻post streaming inputs仍UNKNOWN，必须保留此限制。

最多三个待Main评估的 critical-invariant candidates：资源等价的report/intensive比较与公开例外；单个当前Energy动作后fresh-result rerank；Level-response-reset/一次flat不成永久cap。它们只是候选，不是新增规则、已授权v6e或有效性证明。material survival与conditional Main prior必须继续保留，当前没有安全削弱证据。

| Source | Unicode chars |
|---|---:|
| manifest instruction | 1049 |
| Board | 1879 |
| Planning | 6294 |
| Risk | 2581 |
| 合计startup strategy | 11803 |

计数含frontmatter与LF文本末尾换行；不是token数。实际捕获system26083chars还含框架文本，不与上表直接相加。CTRL/RECONSIDER协议在manifest单行220chars；DECISION_CLOSED重复于manifest/Planning/Risk；freshobserve、recovery、PrimaryGap/RiskBudget/checkpoint也多层重复。4次均未Skillreread，闭合反复重开，六字段checkpoint常扩成完整bundle；与此同时单整数/单session与部分survival/Network策略有行为效果。**没有attention telemetry或删字A/B测试，不能声称重复文字导致drift**。

## Score difference：公开component points

两局score_report的ending_score为空，但最后公开observe的ending_score已合法公布dimensions；只比较weighted component points，不导出raw risk counter、weights或逆推公式。

| Component | Run01 | Run02 | Delta |
|---|---|---|---|
| level | 15.0 | 15.0 | 0.0 |
| wealth | 9.93 | 8.1 | -1.83 |
| resilience | 13.5 | 14.25 | 0.75 |
| skill | 14.25 | 15.0 | 0.75 |
| risk_control | 10.0 | 4.0 | -6.0 |
| network | 9.0 | 9.0 | 0.0 |

公布的round组件差合计−6.33，正式总分差−6.32，为rounding边界。差额主要伴随risk-control点数−6.00，其次wealth−1.83；Skill/resilience各+0.75、Level/Network相同。不是隐藏风险库存恢复或action causality证明；不能据此说“7intensive造成6分损失”或“cleanup少3次造成损失”。

## Competing hypotheses / decision

| Hypothesis | Verdict | Evidence boundary |
|---|---|---|
| H1 Compression Context Loss | PARTIAL | bodyloss和summary效率条件缺失直接可见；action输入缺失、precompression已有偏差 |
| H2 Rule Present, Model Ignores | PARTIAL | startup全文与M15显式quote并存错误应用；persistent合同可见仍不执行；不泛化全部action |
| H3 Stale Quarter Plan | SUPPORTED | 32quarter bundle与大量PLAN_CONTINUE直接可见；shared弱点不等于mix差异根因 |
| H4 Deliberation Reopen | UNSUPPORTED | 在10重要postgate witness中未验证当前action改变 |
| H5 Public-State Difference | PARTIAL | warning/Health/Level/response不同，2valid exceptions；不能合理化所有强度选择 |
| H6 Mixed | SUPPORTED | contextloss、stale response、bundle、exception与precompression应用偏差共存 |

**MIXED_NO_SINGLE_SAFE_PATCH**。不选A：persistent更稳定只在捕获点得到支持，且可见控制合同仍被忽略，不能保证搬迁修复precompression应用错误。不选B：rerank缺陷在两局共享，且Run02真正rerank更多，无法把intensive差异归给单一bundle机制。不选C：没有多个当前choice drift。不选D：后半程不能证明完整关键policy始终可见，合法例外和public state差异也不能忽略。

**PATCH_CONTRACT_PROPOSAL：NOT_SUPPORTED_AS_A_SINGLE_SAFE_PATCH**。本任务没有规则移动/删除/替换、没有v6e、没有允许修改runtime文件的决定。Main可决定下一 bounded experiment：若评估persistent核心，须证明实际决策prompt与迁移条件；若评估one-step简化，须在等价resource比较/flat后检验rerank而不是只检验observe数量。不能把建议当第三局、候选patch或live授权。

## Validation / hold / nonclaims

Offline JSON/source/identity/epoch/input边界/计数检查、原held hash、protected diff、accepted pure secret scan与diff-check通过；只交付报告/compact evidence/CURRENT_STATE，push并clean在TASK_RESULT确认。raw继续本地FORENSIC_HOLD ACTIVE，ownerS10-12/S10-14，releaseMain/Stage；本结论依赖4actualcompressor上下文与decision traces，不解除hold，不删原文件。scratch extraction只作可重建派生物，不是唯一取证来源。

No gameplay improvement proof / stable75 proof / measured true variance / promotion or hidden scoring formula / hidden-test transfer / event-answer mapping。

**RETURN_FOR_EXECUTION_CONTROL_DECISION**

**NEXT_GAME=NOT_AUTHORIZED**
