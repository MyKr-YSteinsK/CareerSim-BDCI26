# 11｜一次开发任务从 Plan 到 Git 是怎样落地的

[学习地图](00-学习地图.md) · [上一章](10-Human-Play-Lab是怎么实现的.md) · [下一章：长期保留](12-哪些文件值得长期保留以及哪些最终可以删除.md)

## 工作流为什么反复出现这些词

软件改动的难点不只是把代码写出来，还要保证改的是批准的问题、基于正确版本、验证边界明确、别人能够审阅和接续。本项目用Main、Stage、Plan、Codex、Git和TASK_RESULT分配这些责任。

这些角色并不必须对应不同真人或不同服务。Main（项目主控）管理全局目标与接受决定；Stage（阶段）把一段目标组织成有边界的任务；Plan（任务计划）冻结执行合同；Codex工程Agent在仓库落实；Git保存可审阅的版本增量。它们也不属于比赛Agent的游戏决策链。

## 一、开发循环图

```text
Main：全局目标 / 授权 / 验收
   ↓
Stage：阶段问题、边界与任务顺序
   ↓
Plan：目标 + 来源 + 权限 + 受保护范围 + 验收
   ↓
Codex：核基线 → 读指定来源 → 做范围内implementation
   ↓
默认：root main串行       获准隔离：branch / worktree
   ↓                                  ↓
相关静态核验/测试 + diff + 来源与未知
   ↓
范围明确的Git交付 + TASK_RESULT
   ↓
Main review：接受 / 部分 / 冲突 / 新证据请求
   ↓
需要分支整合时merge/main；串行main则确认已有交付
   ↓
下一项被明确授权的Task（不会自动获得live或cleanup权限）
```

图示是项目[AGENTS](../../../AGENTS.md)与[Plan合同](../../project/CODEX_PLAN_CONTRACT.md)的职责整理，不把每项任务强制变成分支开发。当前默认root main串行；branch需要独立理由，worktree又需要单独理由与授权。S11-29按默认main工作，没创建新分支/工作树。

## 二、Main为什么不直接承包全部coding

落实到文件操作：Main 给出全局接受标准，Codex 核当前源码和 diff，TASK_RESULT 把实际交付返回 review。角色可以由同一人或不同对话承担，不能混入比赛 Agent 的动作链。

这种分工怎样降低实验误判，集中读 [D13 治理设计](../track-d-project-method/13-Main、Stage、Plan与Codex为什么这样协作.md)；这里继续看任务交接时各对象如何进入 Git。

## 三、Stage为什么要有边界

Stage 组织任务顺序，每个 Task 另列基线、写入集合、权限和验收。例如先准备 ignored source pack，再由下一 Task 写正式教程；“继续 S11”本身不增加 gameplay 或 cleanup 预算。核对实际 Task 合同后才编辑。阶段边界的理由见 [D13](../track-d-project-method/13-Main、Stage、Plan与Codex为什么这样协作.md)。

## 四、Plan不是固定每行实现的脚本

[CODEX_PLAN_CONTRACT](../../project/CODEX_PLAN_CONTRACT.md)分三个层级：

| 层级 | 冻结/委托什么 | 执行者能怎样判断 |
|---|---|---|
| FROZEN（冻结要求） | 目标、范围、已确认事实、保护、权限、停止与验收 | 必须遵守；事实前提冲突应停受影响部分并回传 |
| RECOMMENDED（推荐） | 有证据的实现方向、可能文件、验证顺序 | 可按当前事实调整并解释理由，不能突破FROZEN |
| DELEGATED_TO_CODEX（委托执行调查） | 未知根因、位置或方案，带问题/证据/判断标准 | Evidence→Investigation→Decision→Implementation→Verification |

**TEACHING EXAMPLE｜教学示例：**Plan规定“修正唯一失效锚点，不改运行事实”，这是FROZEN；提示目标可能是某个中文slug（标题锚点）只是待验证建议。Codex应读真实标题并按现有Markdown规则确认，而不是机械复制Planner猜的字符串。

自主性作用于实现选择，不扩大scope（范围）。读到了一个旧test断言，不意味着本教程任务可顺便修tests；知道一个日志可以重算，也不意味着可以删除它。当前S11-29允许13篇新教程，其他tracked修改为0。

## 五、Branch、Commit与Worktree怎样分工

Branch（分支）是一条提交线的名字/指针；Commit（提交）记录一个版本快照和父关系；Worktree（工作树）提供独立工作文件及index。工作树能支持并行编辑，分支能隔离提交增量，commit让别人比较“这次改了什么”。

```text
工作文件的编辑
     ↓ 选择本任务内容stage
暂存索引：下一次提交的准确集合
     ↓ commit
本地提交：可比较、可审阅的身份
     ↓ push
远程分支：其他参与者可取得的交付身份
     ↓ review / 必要时merge
接受的项目事实与主线状态
```

这只是操作关系。涉及stage/commit/push/merge的演示属于：**教学示例；当前 S11-29 不授权执行。**S11-29本身的实际文档提交另由任务显式授权；教学流程不扩大它的范围。

Git clean表示工作树没有相应未提交增量，不表示所有ignored日志已清理；push成功表示远端收到提交，不表示官方比赛上传；分支commit存在表示IN_FLIGHT_EVIDENCE，不自动成为MERGED_FACT或Main接受。

## 六、验证为什么跟任务类型走

文档修改检验链接、锚点、格式、来源和范围；包装修改检验身份与文件集合；解析修改检验实际归属错误；live运行才检查授权内的runtime门。项目Tier制度见AGENTS，不要求每个小任务都运行全部pytest或完整游戏。

**TEACHING EXAMPLE｜教学示例：**修一个Markdownfragment，如果跑游戏成功也不能证明导航正确；反过来链接全部通过也不能证明正式Agent遵循。正确验证要与失败方式一一对应。

失败还要分层：本地命令构造错且没有触发运行，是Tooling Error（工具错误）；真实动作启动后的失败按runtime合同处理；若无法确认动作是否发生，是Unknown Side Effect（副作用未知），不能当无害错误盲重试。命令退出码只是线索，语义操作才决定预算和停止。

## 七、真实walkthrough：S11-28的两种交付

本章选择source map推荐的S11-28，而非重新恢复S11-24历史。它结构清晰，且当前base提交可以直接核验：修一条旧导航缺陷，同时准备ignored source pack，随后S11-29消费该包写正式教学。

### 1. 问题

Track B正文被接受，但全仓Markdown检查发现一个更早存在的fragment失效：v7o运行记录仍链接英文 `#forensic_hold-ledger`，目标标题已经是 `FORENSIC_HOLD 台账`。此前任务不允许修改docs/project，所以返回Partial而没有越界。

### 2. Plan contract

S11-28冻结base `85217072f64d2463e57b224d9c7e85b078f747be`，允许唯一tracked文件的一处anchor target替换；run identity、score、session、hold、hash和历史结论都不能变。另允许把七份机械地图写到ignored `.local/scratch/s11-28-track-c-source-pack/`，不commit、不从README链接。

### 3. Codex execution

读取真实目标标题，确认GitHub-compatible slug，再把链接替换为 `#forensic_hold-台账`。同时在scratch准备repo/scripts/tests/experiments/local/HPL/workflow/chapter maps。两项工作分别满足“修缺陷”和“降低下一作者扫描成本”。

### 4. 可直接核验的Git evidence

**FACT｜事实：**该历史修复提交 `1c6231de36c98e4cdae38bba95c070d8750bcf65` 的message为 `docs: repair final evidence hold anchor`，仅一个tracked文件一行替换。其[v7o记录](../../project/runs/v7o-run1-validation.md)现链接到[中文台账](../../project/FINAL_EVIDENCE_REVIEW.md#forensic_hold-台账)。提交diff没有改score或hold语义。

source pack未进入该commit，所以只看Git stat会看见一处修复，不会看见七份scratch的工作量。S11-29opening gate还要求七份文件存在并完整读取，补上本机handoff（交接）依赖。这说明Git交付和本机机械交接可以是不同对象，但两者都要记录身份与消费条件。

### 5. Review与next decision

用户S11-29任务将source pack准备视为已完成，并固定1c6231…为新基线。下一任务只写正式教学，不重做全仓机械盘点；当前来源若与map不一致，按源码纠正教学描述。这个例子展示“低成本机械准备→高质量解释”的任务分工，不推断任何未提供的Main聊天细节。

没有TASK_RESULT及opening gate，下一作者可能以为scratch已commit，或读取不到就重新考古；有合同后，缺包应返回Main，而不是绕过前置条件。这里七份包完整，所以教学可以继续。

## 八、TASK_RESULT为什么不是随便总结

TASK_RESULT（任务执行结果）应能让Main回答：基于哪版做了什么、交付是哪次commit、验证哪些问题、没有验证什么、是否触发live、副作用/hold怎样、还缺什么决定。它是execution evidence（执行证据）的入口，不是个人感想。

| 字段 | Main需要它的原因 |
|---|---|
| Base/parent/HEAD | 防止旧基线或未合父链被当当前主线 |
| changed files / delivery identity | 核对是否只交付批准范围 |
| verification / limitations | 判断PASS的对象及缺口 |
| evidence paths / hold | 保持后续调查及保留责任 |
| live counts / failures / unknowns | 核对预算、重试和未知副作用 |
| decision / next recommendation | 明确返回review，不自动开始新任务 |
| execution metrics | 校准真实时间；无法读取model/effort则UNKNOWN |

结果里写“模型名称”要基于可靠执行记录，不把推荐模型当实际模型；同样，写“测试通过”要有实际执行输出，不能把历史review的数值当本次执行。

## 九、开发链与实验链怎样相交

开发交付的 commit 与实验检验的 Candidate/Run 可以相交，但分别验收。一次文档修改只需对应文档证据，不要求新实验；有运行证据也不能补足文件交付缺口。实验链的完整解释见 [D03](../track-d-project-method/03-从Evidence到Decision的完整实验方法.md)。

## 保留与自查

Plan、TASK_RESULT和review的独有知识应迁移到canonical状态/合同/教学；Git保留历史提交，当前树不必永久堆积每份过程记录。但迁移前要检查引用、未决问题和来源依赖，详见下一章。

自查：S11-28提交只改一条链接，是否因此工作不完整？不能按diff大小判断。Plan要求的另一个交付是ignored机械source pack；其存在、完整性和下一任务消费是独立验收对象。反过来，写了很多scratch也不能掩盖tracked修复未完成。完成以合同为准，事实以证据为准。
## 深入练习：Main怎样审阅一个小而完整的交付

**TEACHING EXAMPLE｜教学示例：**合同只许新增 13 篇，额外 README 仍越界。核对 base、准确路径、diff、验证输出，再看对应 TASK_RESULT；便利性不能替范围批准。S11-28 的一行 Git 修复与七份 ignored source pack 则都在合同内，需要分别核验交付。

### Review的三种结论如何不同

Accept、Partial、Conflict 分别报告目标已满足、尚有可交付部分与实质缺口、冻结前提冲突。S11-27 的受保护旧锚点由下一授权任务 S11-28 修复，例子已在 walkthrough 中展开；结果分类不是工作量评价。

### 一个小TASK_RESULT该怎样写未知

把未知绑定到具体对象：无法读取的 model/effort、未执行的 runtime 验证或缺失的 raw 范围。push 是 Git 交付事实，Main 接受是 review 决定，不能互相代替。

### 为什么交付身份比聊天中的“最新版”可靠

commit 与 base 固定可比较增量；ignored source pack 则靠准确路径及 opening gate 补足消费检查。下一 Task 据此接续，不依赖随时变化的“最新版”。返回学习地图，或进入 C12 判断过程资产何时可以退役；治理理由另见 [D13](../track-d-project-method/13-Main、Stage、Plan与Codex为什么这样协作.md)。
