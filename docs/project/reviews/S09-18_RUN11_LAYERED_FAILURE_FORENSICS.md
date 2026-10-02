# S09-18｜RUN11 技术截断与执行漂移分层取证

## Identity / boundary

- `IN_FLIGHT_EVIDENCE`，授权依赖分支 `codex/s09-14-v9a-static`；取证基线 `38c968fd86704721ed9214bc51b203196290c12d`，实际 RUN11 execution `6dea7bab3ca0d57ee1e37af81439eed4e21a8eb8`，v10b implementation `92fb4323c8db2e03fa3c12d0c2969ffdca6f6a4f`，parent v10a。
- `RUN_CLASSIFICATION=TECHNICAL_FAILURE` 与 `BEHAVIOR_CLASSIFICATION=V10B_POLICY_EXECUTION_DRIFT` 分开保留。HTTP402 解释 M45 截断和无 final score，不撤销 M1–45 公开行为证据，也不证明策略漂移造成 Provider 故障。
- 本任务 live / provider / service / game=0；Candidate、四 Skills、manifest、parser、Runner、dependencies、validation flags 均未修改。main/origin/main 的 `6a4037fdf2b75c105cfe0b40b93ea68d3dd0a6f3` v8a submission freeze 不变。
- 现有结果：183 successful actions / 184 observes / 183 fresh action→observe pairs；M45/L5，promotions M12/18/24/42；reported tokens 37,123,199。没有 final quantitative/partial score 或完整 survival validation。
- [compact evidence](S09-18_RUN11_LAYERED_EVIDENCE.json) 保存精确 action/seq/time、日志行号、模型消息索引、类别及必要来源 hashes；不含隐藏数值、完整私有配置或 raw 副本。原 RUN11 [run note](../runs/v10b-run11-first-validation.md) 保留历史统计语境。

## Method / evidence

只使用既有 RUN11 FORENSIC_HOLD 来源。UTC window：`2026-10-02T06:51:35.265851+00:00`–`2026-10-02T07:25:03.476221+00:00`；下表统一显示 `+08:00`。events 的重复回传按 tool-call ID/kind 去重，action 一基索引不变。

新证据来自 run-scoped `service-stdout.log`：第3545行（首次压缩请求）、6846行（第二次压缩请求）、11676行（首个402请求）包含模型输入消息。以 tool-call ID 对齐 **183/183** 动作，模型生成的 notes 与 events 中 notes **183/183 原文相同**。这提供实际压缩前后上下文与生成/传递边界；不是凭 transcript 邻近词句猜动作。3547/6848行是两份实际压缩响应；只提取合同变化类别，不复制 raw 或私有 prompt。

源位置：

- events/transcript：`D:\CS\CareerSim\.career_sim_runner\career_emu\outputs\local-s06-adaptive-controller\20261002T065143Z\`。
- service stdout、runner result、public context pairs、原 evidence manifest：`D:\CS\CareerSim\.local\runtime\s09-run11-v10b\`。
- 小型离线对齐器：`D:\CS\CareerSim\.local\scratch\s09-18\align.py`，ignored，不提交；只重建派生索引，原始证据保持原位。
- 核对已安装 runtime source：`openjiuwen/core/context_engine/processor/forked/compressor/current_round_compressor.py`、同目录 `base.py` 与 `support/compression_executor.py`；`jiuwenswarm/server/runtime/agent_adapter/interface_deep.py`。本机源码仅用于解释本局已记录的消息路径，不升级为比赛可部署 hook 证明。

来源 SHA256、bytes 和各 sampled action 的 seq/time 见 compact JSON。FORENSIC_HOLD 继续 ACTIVE；责任返回 Stage/Main，只有其接受可独立复审的结论并解除依赖后才可决定解除/清理。没有 raw archive、DB 查询、历史 mega audit 或 Provider 请求。

## RUN11_PHASED_FAILURE_TIMELINE

| phase | precise boundary / observation | conclusion |
|---|---|---|
| P0：a1–12 | 四 Skill read_file 于14:51:54按 Board→Delivery→Planning→Risk 一次读完；H1/H2 notes门禁通过；trace合法 | 启动有完整契约。H2未发现影响已执行排序的C6断言，不是完整 reasoning 防火墙PASS；a11有受禁效果列举后主动排除 |
| P1：a13–38 | 无 compression completed/started；a14、25有受禁效果列举，a27有风险效果比较与来回试探cap的推理，最终 notes仍hedged | 漂移前兆在压缩前；尚未将试探性 prose 升级为第一个确定性已执行C6案例 |
| P2：a39–47 | **a39/M9 seq333 14:59:54.396167**：N/O已近当前Level上限、S唯一可增；trace仍VALID。a47 seq397 15:00:56.619885 | 首个已确认 material C6违例在首次压缩前；四Skill正文仍在该模型输入 |
| P3：首次压缩/a48–49 | compressor 15:00:56.854→**15:01:18.369**；a47 receipt seq399 15:00:57.071016；observe call/result seq401/403 15:01:20.569551/.694250；**a48 seq405 15:01:26.391708**首次失效；a49 seq413 15:01:41.687684短暂VALID | 首份摘要把trace改述为可选，并固化L1软上限推断；正常observe继续，未进行Skill恢复 |
| P4：a50–129 | a50 seq421 15:01:44.735075起持续缺PROBE/自造枚举。a98–99/M24数字式S保护。a129 seq1053 15:10:51.777117；receipt1055 15:10:52.070809 | CTRL/DL仍合法，但Planning-owned trace契约已丢失；存在防火墙/保护漂移，不能将全部归因第二次压缩 |
| P5：第二次压缩及a130–183 | observe129 call1057 **15:10:53.560712**、result1059 **15:10:54.277793**；compressor **15:10:53.746→15:11:16.122**；a130 seq1061 **15:11:24.850826**。a135/147/159重复cleanup | 注意异步流时间重叠：observe调用先于compressor started，结果在其后；不把日志流时间当严格单线程顺序。第二份摘要明确允许不重读Skill，输出错误L4 cap策略；无恢复 |
| P6：M45 | 首个402请求错误：15:24:27.267314；最后成功action索引仍183；Runner停止15:25:03.476221 | `HTTP402_INSUFFICIENT_BALANCE`，无a184；与前面独立的行为漂移分开 |

## A｜C6：独立错误被压缩摘要放大

**Classification=`C6_DRIFT_COMPRESSION_AMPLIFIED`。**

- H-A1 **SUPPORTED**：a39之前没有压缩；实际模型输入包含完整 Planning `Do not invent saturation`、局部NO_GAIN限制及canonical trace。公开结果只能证明特定动作/维度响应，未建立Level cap。a39 notes与Planning正文仍把N/O近顶和S唯一可增用于轮岗排序；不是摘要丢失后才开始的错误。
- H-A2 **NOT_SUPPORTED as sole/first cause**：首个已执行确定性C6违例比首次completed早83.973秒，也早于started；不能称为纯postcompression failure。
- H-A3 **SUPPORTED with causal limit**：压缩响应本身进一步把局部停滞改写为“实测软上限”，第二份还明确建议L4不必再靠Output动作、转向其它维度或等待晋升。a135/137/147/159/161/171/174随后重复采用cap/解封理由；这比单纯时间关联更强。没有反事实或受控复验，无法量化压缩的独立效应，也不能证明修恢复就消除压缩前C6错误。

沿用原人工判断的16个substantive clusters：supported3 / hedged3 / unsupported9 / ambiguous1；material已执行8个动作（precompression1、postcompression7），另1 pending比较未执行。该计数合并同动作 notes/reasoning，与关键词频次、防火墙计数分别定义。S/N/O低Level上限、晋升抬高cap均没有对应公开cap证据；Handbook的公开范围不支持这些断言。

## B｜trace：在模型生成的工具参数中已经失效

Expected：CTRL、DL之后各一个canonical POL与PROBE；POL B属于 `PROTECT|DELIVER|RESPONSIVE|OWNERSHIP|VISIBILITY|PROBE|OTHER`，F属于 `S|N|O|MAIN|STORY|RESOURCE|OTHER`；PROBE保留五位K与E/C/S/F一致性。冻结parser不从自由prose补值。

| action | emitted shape（精确marker） | frozen parser |
|---|---|---|
| a48 | `[POL B=COMPLIANCE F=S RP=NA]`；PROBE不存在 | MISSING_OR_MALFORMED；B越界+缺block，不是仅ordering |
| a49 | `[POL B=RESPONSIVE F=O RP=NA] [PROBE K=0???? E=0 C=0 S=0 F=NONE]` | VALID；短暂语法恢复不证明恢复序列或语义正确 |
| a50 | `[POL B=RESPONSIVE F=O RP=NA]`；PROBE不存在 | MISSING_OR_MALFORMED；没有整句截断 |
| a98 | `[POL B=SAFETY F=H RP=NA]`；PROBE不存在 | MISSING_OR_MALFORMED；B/F均越界 |
| a129/130 | `[POL B=ADAPTIVE F=W RP=NA]` / `[POL B=ADAPTIVE F=H RP=NA]`；均无PROBE | MISSING_OR_MALFORMED；第二压缩前后无恢复 |

事实：48/183完整，a48首次失败、a49有效、a50–183连续失败；CTRL/DL 183/183有效。两份实际摘要将必需POL/PROBE改述为“其后**可附**”。首次之后、第二次之后的模型输入都不再包含完整canonical Planning正文，但system中仍有CTRL/DL preflight与context recovery正文。这是不同owner契约在压缩后保留程度不同的直接证据。

**Classification=`MIXED`：CONTEXT_RECOVERY_DRIFT + 同一Agent生成工具notes的输出契约漂移。** 不是PARSER_DEFECT；全部183个模型tool-call notes与events相同，未发现外部executor/controller重写或截去block。Planning可见正文在a48/49/50没有可供复制的完整canonical block；早期某些Planning prose也没展示block却能生成合法notes，因此不能仅凭正文缺块区分Single Agent内部“Planning生成”与“executor忘记补写”。**PLANNING_GENERATION_DRIFT（角色内部）与EXECUTOR_PROPAGATION_DRIFT的更细分归因仍UNKNOWN**；已定位到模型生成参数边界，不能归咎传输或放宽parser。

## C｜compression recovery：signal可见但没有进入规定恢复路径

| contract step | epoch1 | epoch2 |
|---|---|---|
| host signal | stdout `CurrentRoundCompressor completed`；adapter可向外发`context.compression_state` | 同左 |
| executor可见signal | 注入`<memory_block_current>` UserMessage，meaning明确为compressed summary；在第二次压缩前输入中实见 | 同样wrapper在402输入中实见 |
| manifest要求 | system中CONTEXT RECOVERY与RECOVERY_PENDING仍在；实际可见compaction须恢复 | 同左 |
| RECOVERY_PENDING/BLOCKED | 未记录进入 | 未记录进入 |
| same session | observe/action仍同一session；未见显式恢复身份核验 | 同左 |
| fresh observe | 正常a47后observe发生；不是完整恢复证据 | 正常a129后observe与compression有流时间重叠，之后a130仍使用该公开观察；没有新增恢复observe证据 |
| 四Skill依次重读 | **0** | **0** |
| Board / Delivery | a48重建可见Board并保留DL；未证从原Skill恢复Delivery item证据 | a130仍有公开Board/DL；未证恢复链 |
| REVIEW_PLAN / RECOVERY | 局部Review prose继续；没有完整restore回执 | 局部gap继续；没有完整restore回执 |
| RECOVERY_READY / next | 未记录；直接a48；a49语法有效不等于recovery | 未记录；直接a130，schema继续失败 |

**Root boundary=`SIGNAL_OBSERVED_NOT_ROUTED`，其中OBSERVED严格表示“已送入模型可见输入”，不表示已证模型主动识别。** 不能归为SIGNAL_NOT_OBSERVABLE：本机 `base.py:281–296,668–682` 实际创建并注入带meaning的memory UserMessage；日志中的后续模型输入证实wrapper存在。`interface_deep.py:10097–10107` 的外发stream事件本身不证明游戏Agent收到它；本结论依赖memory wrapper，不把操作员看见stdout混同为模型看见stdout。

第一份摘要省略原恢复链，仅建议observe后继续；第二份明确写“使下一实例无需重复读取技能/手册即可继续循环”。system恢复合同仍在，却没有恢复触发、Skill读取或ready证据。故合同**可执行工具已有，但实际没有执行**；没有证据表明read_file不可用。这里同时存在summary合同变形和Agent路由遗漏，不能仅归为策略失败，也不证明已有deterministic enforcing hook可在比赛bundle部署。

## D｜evidence firewall：压缩前已有违反，之后扩展

计数单位为**去重action窗口**：模型输入保存的对应assistant `reasoning_content + content`及tool notes合并；排除Skill/manifest指令引用、纯“excluded/unknown”声明和ordinary public risk文字。显式受禁字段、其数值效果别名、counter状态推断进入列举/记忆/比较才计数；同窗口反复说不重复计数。未执行M45 pending单列，不纳入动作计数。

- precompression reference violations **5**：a11/14/25/27/39；其中a11主动改回public描述、排除numeric field，**1 self-corrected**，其余4未见同窗口明确清除。首次可定位受禁效果列举为a11/P0，首次确认counter效果参与竞争比较为a27/P1；a39/P2进一步推断风险可能已释放。
- postcompression violations **20**：a49/50/55/56/57/58/61/63/67/73/86/111/123/135/137/147/149/159/161/171。
- **material ranking/comparison windows=16**：a27/39/49/61/63/73/86/111/123/135/137/147/149/159/161/171。含最终未选risk动作的竞争比较；这是“参与排序”的证据，**不是16个反事实可证明选择改变**。其中7个实际cleanup窗口a49/61/86/111/135/147/159有受禁推理；所选动作亦可能有独立公开理由。
- narrow action-note count仍是4（numeric3：a135/147/159；nonnumeric1：a171），与原RUN11报告不冲突：原统计不是全reasoning窗口审计。

| instances / phase | wording category / effect | Risk |
|---|---|---|
| a11 P0；a14/25 P1 | 受禁效果列举；a11随后明确排除并改用公开“累积潜在风险”描述。其它两处仅列举，不升格material | a11自纠；其它未证拦截 |
| a27 P1；a39 P2 | counter减量/爆发后reset推断参与避险与成长比较；最终选成长，不证明避险更优 | 最终PASS，未清除受禁推理 |
| a49 P3；a61/63/73/86/111/123 P4 | counter效果参与cleanup、Main或Energy比较；公开warning可以支持处理风险，但不授权读取numeric counter | 未见捕获；普通public成本不因此自动Full Review |
| a50 P4 | 给不可见counter结果作确定性归因 | 无公开验证basis；不计material排序 |
| a55–58、67 P4 | 把public warning映射为counter/STICKY或猜测触发机制；4个持久记账+1个推测 | 未见隔离该推理；不计material选择 |
| a135/137/147/149/159/161/171 P5 | counter减量/增量比较、旧warning重复授权；a171 Risk也以“无受禁风险增量”放行 | PASS，不等于防火墙PASS |

每个material窗口的当前raw tool context是否含受禁字段已按boolean记录在compact JSON（无值）；**存在于tool response不等于participant-public授权**，尤其options/status_updates。部分后来STICKY/推理来自历史记忆而非fresh field，不能借public warning把counter重新合法化。

**Classification=`MIXED`：precompression执行防火墙失败 + summary保留错误机制 + postcompression Risk gate miss。** 原system/Planning都有明确禁止，证据不足以称原合同没有firewall；“FIREWALL_DESIGN_WEAK”作为独立根因未证。a11自纠说明合同可被消费，a27/39又显示恢复修复不会自动解决全部受禁推理。

## E｜cleanup：C6折价与受禁风险优先共同进入理由

| action | fresh warning → cleanup → fresh observe → later authorization |
|---|---|
| a135/M33 15:12:12.942559 | a125后M31曾有minor warning，但a128后M32、a131后M33均为“干得还不错”；当前Energy feed为空。Planning仍因O“L4触顶”排除O动作，将受禁counter列为主要生存威胁→cleanup→15:12:14.223010 fresh observe，公开H/D/S/N/O/W不变，不能据此证counter已减少/风险已解。随后a136补H至10，a137成长Main |
| a147/M36 15:13:46.944932 | a143后M36新minor warning“有点风险，不过问题还不大”，并非全无新warning；但没有新的“积攒不少/需要处理”或已验证同一风险持续elevated证据。Planning再次因O触顶排除成长、使用counter效果→cleanup→15:13:48.385836 fresh observe；a148 Network、a149 Main后M37 HR“干得不错” |
| a159/M39 15:15:19.420200 | M37/M38/M39最近HR均“干得不错”；当前Energy feed为空。推理仍称HR持续warning、O≈cap/S近顶→再次cleanup→15:15:21.827195 fresh observe；a160健康、a161导师Main。无fresh同类warning可重新授权 |

因此a135/a159有旧风险叙事复用；a147有**新的轻度warning**，不能把三次一律称为“没有任何新警告”，也不能把minor warning自动升级为重大counter绑定。公开blank feed不能证明风险解除；最新肯定反馈也不能证明隐藏counter为零。

**Within-decision causal ordering SUPPORTED**：三次Planning均先以cap使成长动作显得无价值，再把受禁风险管理排在前面，且notes与实际cleanup对应。这是明确理由链，不只是同一时间出现。**Game-outcome causality UNKNOWN**：无法证明没有cap推断就一定选另一个动作、cleanup真实效果/得分影响/更好反事实。流程fresh observe仍正确，bounded cleanup语义未获支持。

## F｜a98–99：真实C2违例，不只是MODE标签

**Classification=`C2_MATERIAL_VIOLATION`。** a98/M24以“H3已达危险区”授权S，a99 fresh H5仍以“回补至安全区间”继续S，两次各消耗一Energy，H3→5→7；a100以A准备材料、O19→20。当前公开Energy事件、feedback无急性warning或正常活动不可行证据；此前M17急性症状已处理并在M18回A，不能重新充当M24绑定。

第二次恢复没有fresh binding basis；退出发生在数值提高之后，未记录具体公开约束解除。两次实际资源投入说明超出marker-only drift；不主张恢复动作必然降低最终score，也不将H3/H5/H7立为新安全阈值。公开Health本身可作成本/状态信息，问题是把数值独立当作material threat及持续S授权。

## G｜complexity：有具体负荷症状，长度不是已证主因

| exact Planning revision | LF chars | responsibilities |
|---|---|---|
| v8a `6a4037f` | 8,748 | Review Plan、MODE/recovery、成长/ownership排行、hint/local response、quarter control、closure |
| v9a RUN10 `1cc20d7` | 9,477 | 保留上述职责，增加bounded untested probe |
| v10a `0cecffd` | 7,498 | Constitution、master ranking、Main/Energy controller、probe、POL/PROBE trace；runtime recovery仍归manifest |
| v10b `92fb432` | 7,928 | v10a职责+C6显著性guard；未增Skill/architecture |

**Classification=`COMPLEXITY_OVERLOAD_PLAUSIBLE`，非已证PRIMARY。** v10b比v8a/v9a更短，不能称“prompt越长导致失败”。每次仍同时协调Constitution、Review、MODE、ranking、Main/Energy、probe、Risk、trace、recovery约9类责任；早期复杂trace可以生成，随后自造COMPLIANCE/SAFETY/ADAPTIVE并丢PROBE，宪法与cap/数字保护理由冲突；压缩前后都存在大量重复比较。具体摘要已经删除/改写关键条款，因此恢复/契约保留比总长度具有更直接证据。

trace负担与策略reasoning是否因果竞争UNKNOWN；没有同模型同情景受控比较。可供后续窄简化的对象是**summary中的错误“机制发现”与重复季度组合意图**，恢复时依原Skill重建fresh单候选；不建议这次或下次直接重写整个宪法。

## Cross-phase matrix

P3为首次压缩/a48–49；P4为a50–129；P5包含第二次压缩与后段。NOT_ESTABLISHED不等于没有问题。

| failure class | P0 | P1 | P2 | P3 | P4 | P5 | likely layer |
|---|---|---|---|---|---|---|---|
| C6 saturation | notes门禁未见material | 试探/反复比较 | a39确定性material | 摘要固化错误L1机制 | 正确增长与错误cap记忆共存 | 错误L4摘要→7个material动作 | 独立策略语义+压缩放大 |
| trace schema | VALID | VALID | VALID | a48失效/a49VALID | 134动作连续失效的一部分 | 持续失效 | recovery/output契约 |
| evidence firewall | 列举后自纠 | 列举/比较 | counter推断 | a49 cleanup | STICKY/数值效果进入排序 | cleanup及Risk受禁basis | 独立执行失败+summary保留 |
| repeated cleanup | NOT_ESTABLISHED | NOT_ESTABLISHED | 风险避险反复比较 | a49旧爆发basis | 公开warning与错误counter推理混用 | a135/147/159重复 | fresh授权+cap折价+firewall |
| MODE protection | 未见S | 未见S | 未见S | 未见S | a69 acute合理；a98–99数字S | A内补资源也需依据 | C2语义，非trace parser |
| Delivery continuity | bounded tracking | D2出现 | D2 BLOCKED/NEAR | 延续旧item | 长期UNVERIFIED/BLOCKED | a134起D1/recognition1缺item-linked证明 | 状态连续性；恢复可能放大未证 |

Delivery结构183/183可解析，未PUBLICLY_VERIFIED overclaim，但从D2转D1/recognition时缺充分公开identity/recognition来源。没有理由把该症状归给402或假定恢复必然修复；本任务保持QUESTIONABLE，不补算不存在的probe/Delivery验证。

## Root-cause ranking（最多3；唯一PRIMARY）

| rank / target | evidence / symptoms | confidence / payoff / regression risk | smallest plausible next static patch |
|---|---|---|---|
| **1 PRIMARY：OBSERVABLE_COMPACTION_RECOVERY_AND_PLANNING_CONTRACT_RELOAD**；runtime recovery/output contract | 两个真实memory wrapper；摘要把trace必需变可选、反cap变cap；完整Planning正文消失、0 reread；135 malformed traces。可覆盖测量持续性并削弱错误机制继承 | failure boundary HIGH；修复效果未验证。payoff：首先恢复可测量性/原契约；risk：错误把普通summary/续轮当新compression，造成过度reread或执行停滞 | 在后续获准任务里仅明确现有可见memory/compaction触发与一次完整恢复链，阻止用summary“已读/无需重读”代替本epoch读取；恢复按原Skill重建，不新增策略；用压缩摘要fixture验证trigger/四读顺序/READY及canonical trace。不得静默改冻结framework/Runner |
| 2：LOCAL_RESPONSE_NOT_CAP_OPERATIONALIZATION；strategy | a39在完整Skill上下文仍违规；后段cap→cleanup理由链；独立于首压缩 | failure HIGH；payoff：减少无依据淘汰成长；risk：变成强制重复NO_GAIN或固定Skill偏好 | 仅把对应local NO_GAIN→局部折价/UNKNOWN范围形成可审决策检查；保留独立多维价值，禁止family/Level cap结论；不加配额/阈值 |
| 3：RESTRICTED_EFFECT_EXCLUSION_AT_RANK_AND_FINAL_GATE；Risk/evidence firewall | 压缩前a27/39、之后numeric效果比较；system禁令未消失、Risk PASS仍通过 | failure HIGH，根机制MEDIUM；payoff：阻止受禁机制参与排序；risk：把合法public warning/普通成本一起屏蔽 | 仅核查候选basis是否混入受禁field/counter effects，发现即移除并按公开basis闭合一次；不让Risk重新规划，不为检测造Provider/DB查询 |

**PRIMARY_REPAIR_TARGET=OBSERVABLE_COMPACTION_RECOVERY_AND_PLANNING_CONTRACT_RELOAD**。不能用这一项解释所有症状；先修最直接的可测量/契约恢复失败，Stage再决定独立C6/firewall是否成为下一单Delta。上述均为RECOMMENDATION，本任务未patch。

## Disposition / next static class / Provider boundary

- Candidate decision：**`KEEP_V10B_FOR_REPAIR`**。保留实验基线及负面证据；不能用一次无score部分Run判定v10a回退更好，也不能升级v10b gameplay/long-horizon验证。v8a仍正式submission freeze；不实际替换任何Candidate。
- Next experimental decision：**`STATIC_RUNTIME_RECOVERY_REPAIR_RECOMMENDED`**。先做上述唯一PRIMARY窄恢复修复；不是策略重写、live实验或replacement授权。
- `RUN11_PROVIDER_FAILURE=HTTP402_INSUFFICIENT_BALANCE`。任何未来游戏前需用户明确确认余额/credit已补充，或已有合法非付费account-status机制；本任务不查询余额、不创建paid sanity probe。还需primary根修复、trace persistence静态验证、VALUE_OF_RUN_GATE刷新及另行live授权；此处均未满足/授权。
- Verification：183动作tool-call身份对齐/notes原文一致、抽样严格parser、源hash/window绑定、两次实际摘要/模型上下文交叉核对；targeted forensic invariants、JSON parse、selected-deliverable secret/restricted-value scan及`git diff --check`。未重跑历史tests，未声称runtime修复PASS。

**Decision=`S09_18_RUN11_LAYERED_FORENSICS_COMPLETE_RETURN_TO_STAGE`**。

- `NEXT_GAME=NOT_AUTHORIZED`
- `NO_REPLACEMENT_RUN_AUTHORIZED`
- `MAIN_V8A_FREEZE_UNCHANGED`
