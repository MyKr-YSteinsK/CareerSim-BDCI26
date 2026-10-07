# 07｜artifacts、Raw Evidence与证据链

[统一入口与术语](../00-从这里开始.md) · [本 Track 阅读路线](01-仓库总览与核心工程文件.md)


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

**FACT｜事实**：[v7m 运行记录](../../project/runs/v7m-run1-validation.md) 与 [S07-47 调查](../../project/reviews/S07-47_V7M_M20_PARTIAL_RUN_FORENSIC_REVIEW.md) 保存 M20/L3 存活、84/84 成功行动，同时保留技术失败、无最终分数/评级/自然终局以及 `INSUFFICIENT_EVIDENCE`。归档保存可复核片段，没有把部分运行补成完整样本。

本章用它说明 raw、摘要和结论怎样分工；为何技术失败不能等同策略失败，读 [负结果分类](../track-d-project-method/08-Forensics、失败实验与负证据.md#给结果分类并保留停止理由)，调查怎样处理替代解释，读 [D08](../track-d-project-method/08-Forensics、失败实验与负证据.md)。

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

**FACT｜事实**：[最终证据审阅](../../project/FINAL_EVIDENCE_REVIEW.md) 排除了 v7i 首次失败窗口中归属于旧 v7g session 的分数。文件里有值不等于目标 Run 有成绩；空 session 字段也不自动否定一致 fresh final observe。完整重建步骤集中在 [D08](../track-d-project-method/08-Forensics、失败实验与负证据.md)，评分生产机制在 [B08](../track-b-system-runtime/08-日志、Session、Score与证据是怎么产生的.md)。

### 一条证据链中的四种“一致”

身份一致核 Candidate/Session/窗口，结构一致核格式，内容一致核提取，解释一致核结论边界。四者分别记录；合法 JSON 不能替代身份审查。小样本如何限制解释，读 [D07](../track-d-project-method/07-分数、不确定性与反过拟合.md)。

### 原件、选定副本与紧凑结论如何互相核对

副本记录范围/hash，摘要记录输入/限制，结论指回可复核来源。**TEACHING EXAMPLE**：A/B 共用累计日志，只归档 A 的窗口，不能据此关闭 B 的依赖或删除整份 log；选定副本不自动覆盖原件全部责任。

### 去敏与完整性如何共同保留

Secret scan 控敏感值，public projection 控策略可用字段；有限扫描仍需显式选择和人审。保留 raw 用于技术取证，不授予将其内部字段作为玩家知识。记录所留范围、不可用信息、缺失与复验限制，UNKNOWN 不写成零。
