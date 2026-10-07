# 07｜artifacts、Raw Evidence与证据链

[学习地图](00-学习地图.md) · [上一章](06-experiments与research是怎样工作的.md) · [下一章：.local](08-local目录从worktree到runtime完整解释.md)

## 工件是什么，为什么不能都叫“日志”

Artifact（工件）是任务产生或整理出的文件，例如ZIP、JSON摘要、manifest、事件流。Evidence（证据）强调文件用于支持哪一项判断。同一文件可以既是工件又是证据；一份临时图片也可以是工件，却没有被用来支持任何项目决定。

Raw Evidence（原始证据）接近事件发生时留下的记录，例如events、transcript、服务日志和session payload。Derived Summary（派生摘要）由解析或计算产生。Canonical Conclusion（权威结论）是责任任务/Main接受并明确边界的判断。它们的价值来自来源关系，不能按文件名后缀排序。

| 对象 | 本项目例子 | 它回答什么 | 不能替代什么 |
|---|---|---|---|
| Source Code（源代码） | audit、Runner、Skills | 怎样处理/执行输入 | 一次真实运行是否按它执行 |
| Run Record（运行记录） | v7q-run1-validation | 哪局、哪版、结果与限制 | 所有raw逐事件细节 |
| Artifact | finalZIP、archive manifest | 交付了什么、字节是什么 | 平台回执或事实归属审查 |
| Raw Evidence | events、transcript、run-window日志 | 当时留下了哪些事件 | 未记录或丢失的过程 |
| Derived Summary | post_run_summary | 按固定规则提取哪些事实 | 模型语义遵循和所有内部因果 |
| Canonical Conclusion | FINAL_EVIDENCE_REVIEW | 项目接受哪些结论/仍保留哪些未知 | 未解除的hold和未来新证据 |

## 一、从原始事件到项目决定

```text
获准Run：Candidate/依赖/Session/时间窗
        ↓
events + transcript + run-scoped raw log
        ↓ 显式输入、解析、身份与公开字段限制
post_run_audit / 定向forensic分析
        ↓
post_run_summary + source bytes/hash + limitations
        ↓ 人审，补足语义与身份问题
run report / review
        ↓ 接受的精简事实与未知
FINAL_EVIDENCE_REVIEW
        ↓
项目决策：接受、拒绝、停止、保留或请求新证据

旁路：选定raw → 时间窗/secret scan → artifacts/dev-runs归档
原件hold是否解除：另行审查，不由旁路自动决定
```

这张图展示当前证据管线的组成，不声称每个历史Run都具有全套相同产物。早期Run的格式、留存和工具不同，必须按原记录解释。[LIVE_RUN_WORKFLOW](../../project/LIVE_RUN_WORKFLOW.md)规范当前离线摘要与选定归档；[Track B日志章](../track-b-system-runtime/08-日志、Session、Score与证据是怎么产生的.md)解释记录如何产生。

如果只有raw没有summary，审阅成本大；如果只有summary没有必要raw，身份或解析争议就可能无法复核。canonical层让人能快速理解，但它应说明哪些问题仍依赖下层来源。

## 二、artifacts/dev-runs 与 experiments有什么区别

`experiments/`当前主要保存S07-50输入快照与评估结果；`artifacts/dev-runs/`保存选定、限定Run范围的开发证据包，混合raw和派生文件。归档不是模拟器全部状态的备份，也不是全部本机日志的镜像。

**FACT｜事实：**S11-28的metadata计数是7组、39个tracked文件、19,732,641 bytes。下表不读取原始日志内容；hold状态来自权威台账，不从目录名推断完整成员。

| 开发归档 | 文件/bytes | 来源及价值 | 台账边界 |
|---|---:|---|---|
| `S07-46-v7m-run1/` | 4 / 1,150,317 | events/transcript/result/manifest；M20部分技术失败 | S07-47 KEEP_ACTIVE；不补造终局分数 |
| `s08-run01-v7o/` | 8 / 9,741,600 | events/transcript/LLM/service等；来源范围调查 | UNKNOWN_REVIEW_REQUIRED；核心pair留存，其他六项未知范围保护 |
| `s08-run02-v7q/` | 6 / 1,386,318 | 自然M24终局的events/transcript与摘要等 | KEEP_ACTIVE；未观测完整48m行为 |
| `s08-run03-v7t/` | 6 / 2,636,576 | runtime/evidence-discipline审查来源 | KEEP_ACTIVE；遵循解释仍有依赖 |
| `s08-run04-v7v/` | 6 / 3,119,661 | transcript与运行限制来源 | UNKNOWN_REVIEW_REQUIRED；释放条件不完整 |
| `s09-run01-v7w/` | 6 / 1,689,623 | 提前终局、身份/防火墙来源 | KEEP_ACTIVE；删除需逐文件审查 |
| `s09-run03-v7y/` | 3 / 8,546 | play前启动失败的service诊断/result/manifest | KEEP_ACTIVE；不是有分数的gameplay失败 |

可从[归档目录](../../../artifacts/dev-runs/)导航。具体canonical状态在[最终证据审阅](../../project/FINAL_EVIDENCE_REVIEW.md#forensic_hold-台账)，不要把这张教学表当新的hold授权表。

为什么归档在ignore目录里还能tracked？默认排除保护日常生成状态；显式选择和扫描后，archive工具可以精确stage这些文件。该例外不放宽共享DB、凭据和无关Session禁入Git的规则。

## 三、一个真实部分运行：有用事实与未证明事项同时存在

[v7m运行记录](../../project/runs/v7m-run1-validation.md)与[S07-47调查](../../project/reviews/S07-47_V7M_M20_PARTIAL_RUN_FORENSIC_REVIEW.md)保留部分运行。权威审阅记录：最后fresh observation为M20/L3，角色仍存活，84/84动作成功；驱动技术失败，没有最终分数、最终评级或自然终局。

这说明“技术失败”不等于“所有局中事实没有价值”。可以保存成功动作与观测checkpoint，供调查恢复纪律；不能把M20状态当48m完成，也不能用旧分数填缺失终局。classification为INSUFFICIENT_EVIDENCE，运输故障根因尚未确定。

**INTERPRETATION｜解释：**证据整理的目标不是让每次运行看起来成功，而是让事实、限制和决定彼此一致。部分证据照样可以说明某个工程接口的边界；它不提供策略性能的完整样本。

## 四、为什么raw很大

事件流记录多次call/result及重复状态；transcript记录模型和工具展示；服务日志跨多轮或多局累计；session payload保存恢复所需状态。这些材料常会重复信息，却可能在不同问题中提供独有细节。

重复不自动意味着可删。摘要可能只提取public状态和marker，没有保留断连前后的帧或LLM请求上下文；当根因未定时，那个未摘要片段可能仍重要。反之，普通成功诊断日志若没有独有来源和依赖，未来可以经审查清理。

本教程不对raw内容逐行分析，不输出hidden值或秘密配置。看size/count和canonical状态，足以解释类别；不需要为了写教材再打开巨型raw。

## 五、FORENSIC_HOLD从零理解

FORENSIC_HOLD（取证保留）是“这个明确来源仍有未关闭的复核责任”的记录。通常列原因、最小范围、时间窗、路径、hash、责任任务、解除者和release condition（解除条件）。它限制覆盖、删除、压缩和搬迁，防止调查来源被日常清理破坏。

Hold不等于“永远不能删除”。它把删除判断推迟到可复核的闭合步骤：责任任务给出独立可审结论；确认来源可恢复或不需再分析；child/repro依赖解除；Main/Stage接受并明确release；之后还需要精确范围的cleanup授权。

```text
未决问题/唯一来源 → 设置hold
           ↓
独立结论 + 必要来源处置 + 下游依赖闭合
           ↓
Main/Stage明确release（解除）
           ↓
另行限定cleanup授权
           ↓
精确路径清理与限制记录
```

本任务没有执行其中任何解除或清理步骤，HOLD_RELEASE_COUNT=0。

### 结论已写好，为什么raw还保留

因为“结果摘要完成”“原始归因完成”“其他任务不再依赖”“Main接受release”是不同事件。最终审阅吸收某局分数，不一定回答它的压缩恢复、Session污染或运输错误。如果只有摘要而丢了仍需调查的来源，后续就不能独立审查。

### Git history为什么不能总替代raw

Git只保存提交过的对象。很多原件按合同留在ignored本机runtime，根本没进入Git；selected archive也可能只是时间窗副本。即使某份derived文件可恢复，也不保证未归档的原始log可恢复。Hash是指纹，不是内容备份。

### Manifest是不是release证书

不是。Manifest记录输入/输出身份、bytes/hash和打包范围。它可以帮助核对来源，不能替Main解释未知hold范围或批准删除。归档复制完成也不释放原件hold。

## 六、当前20个具名active/pending holds

**FACT｜事实：**[canonical台账](../../project/FINAL_EVIDENCE_REVIEW.md#forensic_hold-台账)明确20个可逐项追溯项：18 KEEP_ACTIVE、2 UNKNOWN_REVIEW_REQUIRED、0可释放。另有legacy aggregate与v6 raw状态两行uncertainty sentinel（不确定性提示），不是确认的额外独立hold；不能把表行数加成22个确定hold，也不能推断本机唯一总数已穷尽。

| 分组 | 具名责任项 | 当前含义 |
|---|---|---|
| S07 | S07-38、S07-47 | provider失败/过期分数与部分运行调查，KEEP_ACTIVE |
| S08 | RUN01(v7o)、RUN02(v7q)、RUN03(v7t)、RUN04(v7v) | RUN01/04未知条件；其他两项KEEP_ACTIVE |
| S09 | RUN01、RUN02、RUN03、RUN03R、RUN04、RUN05、RUN06、RUN07、RUN08 | 九项KEEP_ACTIVE，身份/中止/策略/遵循等依赖 |
| S10 | S10-19-R2、S10-19-R3、S10-20、S10-21、S10-22 | 五项KEEP_ACTIVE，可行性/研究证明保留 |

v7o events/transcript已被S11-08 Main保留为KEEP_CANONICAL_RAW，其余六项为HOLD_PROTECTED_UNKNOWN_SCOPE；这不恢复原始持有人/原因/时间/释放条件，也不把UNKNOWN改成可删。v7v只写pending review而条件不完整，同样不能按“review已读”推断释放。

另有[S03退役记录](../../project/LOCAL_WORKSPACE_RETIREMENT.md)中的20个本机session payload迁移hold。它们与这里20个具名任务hold不是相同计数单位：一边是payload文件，一边是责任项；不能按数字相同就说两组一一对应或互相抵消。

## 七、怎样读一份证据结论

先找Run/Task/Candidate/Session和版本，再找来源路径与时间窗，最后读结论与non-claims（不主张的事项）。一个“PASS”必须有对象：identity PASS、parser PASS、runtime adherence PASS和score结果不是同一个谓词。

**TEACHING EXAMPLE｜教学示例：**摘要列CTRL格式100%，但人审发现某选择不满足风险语义。这两条可以同时成立：格式是可机械解析的文字形状，语义是规则与状态的关系。不能将marker统计升级成完整遵循。

自查：为什么“canonical结论已吸收”不能直接作为删除勾选？因为它只回答知识整理完成，未回答唯一raw、下游复验和release授权。证据生命周期的终点是责任闭合，不是报告写满。
## 深入练习：有分数时怎样防止错误归属

**FACT｜事实：**最终证据审阅中，v7i在首次fresh observation前发生Provider失败，输出的分数属于更早v7g Session，已被排除。它展示一个实际问题：报告程序能拿到数值，不保证数值属于当前被评估对象。

**TEACHING EXAMPLE｜教学示例：**设想报告有一个score字段，但game session为空，事件也没有本局new_game成功回执。此时不应使用“文件最近生成”填补身份；生成时间是报告时间，不一定是游戏时间。也不能从另一个完整Run复制session，让表格看起来齐全。正确表达是当前归属未建立，分数不能作为该Run的结果。

另一方面，某个score report的session字段空，但events明确绑定唯一fresh session和终局observe，audit可能仍能提取该observe分数，同时保留报告字段缺陷。不同情形需要不同结论：空字段不自动让全部证据无效，能读取数值也不自动让归属有效。要沿真正来源判断。

### 一条证据链中的四种“一致”

身份一致检查哪版Candidate、哪个Session、哪个窗口；结构一致检查JSON/schema是否满足格式；内容一致检查摘要是否按输入规则提取；解释一致检查结论是否超过样本和方法边界。它们可以分别失败。

例如两个同Candidate完整样本72.65和59.00的描述均值是65.825，这是数值计算；只有两局，不能由均值宣称稳定收益，更不能推断特定Skill导致差异。canonical审阅明确将这些限定为描述统计。若教材丢掉样本数，数学计算虽然正确，解释也会失真。

### 原件、选定副本与紧凑结论如何互相核对

选定副本应有范围与hash，说明它来自哪一段；派生摘要应记录输入身份与limitations；紧凑结论应链接摘要/记录并保留未决问题。若原件未归档的片段仍被另一个任务依赖，选定副本不能代替全部原件。

**TEACHING EXAMPLE｜教学示例：**Run A与B共用累计服务日志，你只归档A的窗口。A的archive PASS不关闭B的来源，也不授予删除整份累计log。只看A文件已存在会遗漏B；来源级生命周期才看得见这种共享依赖。

### 去敏与完整性如何共同保留

Secret scan排除敏感值，public projection限制策略事实；两者处理不同问题。允许公开字段中仍可能出现不合范围文本，日志也可能有无关session；有限扫描无法替代明确选择与人审。保留一段raw用于技术取证，不等于允许将其隐藏字段用于策略研究。

因此，证据记录需要同时说明“保留了什么”“哪些不能作为策略事实”“哪些没有记录”“怎样复验”。UNKNOWN不是空白装饰，而是防止后续人把没有观察的事项误当零或不存在。