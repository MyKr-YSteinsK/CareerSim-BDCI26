# 08｜日志、Session、Score 与证据是怎么产生的

[统一入口与术语](../00-从这里开始.md) · [本 Track 阅读路线](01-比赛官方到底提供了什么.md)


## 1. 先贴好四张身份标签

Identity（身份）用于回答“这份结果到底属于谁”。Session（会话）用于组织一次持续交互。Run output（运行输出）用于存放本次观察；它们不能互相替代。

| 身份 | 谁决定 | 要绑定的事实 | 单独不能证明 |
|---|---|---|---|
| Git / Candidate（版本/候选方案） | 项目版本管理与候选记录 | 源 commit、材料路径、配置、必要 hashes | 该材料已安装进共享实例 |
| JiuwenSwarm drive session | Runner 创建或复用对话 ID | 模型任务的消息连续性 | 只玩了一局、目标游戏 ID |
| CareerSim game session | `new_game` 创建，结果中返回 | 游戏状态、行动、终局及 DB 行 | 使用了哪个 Candidate；输出路径 |
| Runner output / Run | Runner 时间戳目录、项目 Run 编号 | events/transcript/score 与生命周期时间窗 | 目录中每份文件都自动正确归属 |

**FACT｜事实**：[S06-24 / v6 Run #1](../../project/runs/v6-run1-validation.md) 的 Candidate 是 `candidate-v6-auditable-control-loop`，drive 为 `career-sim-runner-15004a268a02`，game 为 `7b59b85ad19b4597927cf50fc716f9ac`。[RUN_HISTORY](../../project/RUN_HISTORY.md) 同时记录这些不同身份及运行时间。Drive 的字符串不能拿去代替游戏数据库查询键。

[paths.py](../../../career_sim_runner/paths.py) 的时间戳使用 UTC（协调世界时），例如目录后缀 `Z`；日志还可能使用本地时区。比较时间窗时要先对齐时区，不能按看起来相同的小时直接关联。

## 2. 六类文件分别是谁写的

| 文件/材料 | 生产者与生成条件 | 主要用途 | 不能单独证明 |
|---|---|---|---|
| `events-*.jsonl` | 官方 Runner `StreamCollector`，接收帧时逐项追加 | 工具请求/回执、usage 及完成事件的定位 | 完整后台日志、动作语义遵循、官方云端结果 |
| `transcript-*.log` | 同一 Collector 整理可读文本 | 理解模型叙述、追踪过程 | 文本中的结论已经被游戏执行 |
| `score_report.json` | 官方 `build_score_report()` + `write_score_report()`，正常走到报告阶段时 | 汇合身份、路径、usage、退出码与终局评分 | session 必定正确、完整 48 月、runtime adherence |
| Runner result（运行回执） | 项目执行控制器捕获退出与时间等，或按证据显式重建 | 确认生命周期/进程结果及派生来源 | 官方 Runner 必定自动生成独立 result 文件 |
| `llm.log`（若存在） | JiuwenSwarm/模型运行层日志 | 请求结束、报错、usage、压缩等线索 | 内容仅属于本 Run；缺失表示事件没发生 |
| `post_run_summary.json` | 项目离线审计脚本消费明确输入 | 一次有来源和限制的派生汇总 | 自动解决语义归因、因果收益或云端有效性 |

**FACT｜事实**：S08-RUN03 的独立 Runner result 是显式重建的；[RUN_HISTORY](../../project/RUN_HISTORY.md) 明确说明 Runner 没有单独输出它。不能为了凑齐文件清单，把派生回执称为官方原始输出。

JSONL（逐行 JSON）便于逐项处理；JSON 报告是一个汇总对象。原始事件追加产生，`write_score_report()` 则写固定文件名，后续 `score` 可以覆盖原报告。保留来源身份与版本比只记文件名更重要。

## 3. build_score_report 实际做了什么

### 核心函数：build_score_report()

| 问题 | 源码回答 |
|---|---|
| 输入 | 安装记录、DB 路径、输出目录、usage、退出码/终止原因、文本/事件路径、可选 drive/game ID |
| 主要步骤 | 优先用显式 game ID；缺失则找 DB 最近更新 session；读取 ending score；为空时从 transcript 提取；封装报告 |
| 输出 | 一个 `ScoreReport` 对象；另由 `write_score_report()` 保存 JSON |
| 为什么存在 | 将游戏终局结果与参与者材料、驱动结果和证据路径汇集到统一报告 |
| 不负责什么 | 重新计算比赛全部评分公式、审计模型遵循、证明 hidden Test（隐藏测试）成绩、自动纠正 session 污染 |

**FACT｜事实**：[score.py](../../../career_sim_runner/score.py) 的路径如下：

1. 去掉传入 game `session_id` 的首尾空白。
2. 若为空，调用 `latest_session_id()`，按 DB `updated_at DESC` 选一行。
3. 对选定 session 调用 `read_ending_score()`。
4. 若仍没有分，且 transcript 文件存在，查找最后一个可解析、同时含 `outcome` 与 `competition_partial_score` 的 JSON 代码块。
5. 将这些值和调用方给的 usage、退出码等装入报告。

“最新一行”只描述数据库排序，不描述“目标 Run”。共享数据库还有其他历史行，不能把 fallback 默认选择当成身份验证。

### DB 路径并非一定只读 JSON

[db.py](../../../career_sim_runner/db.py) 先读取精确 session 的存储 payload（数据载荷）。若其中已有非空 `ending_score` 字典，直接返回；否则设置当前进程的 `CAREER_EMULATOR_DB`，创建 `GameEngine` 并调用其 `observe(session_id)`。

**FACT｜事实**：这个 fallback 包含环境变量写入和游戏引擎调用，不是仅仅读取一个静态 JSON。其进一步内部副作用未在本轮独立验证，不能给出“执行 score 绝不会触发运行层”的保证。本轮没有调用评分函数，也没有查 DB。

文本 fallback 只检查 JSON 字段，未独立验证这段模型输出的游戏归属和真实性。它是恢复线索，不是比结构化环境状态更强的证据。

## 4. CLI score 为什么需要特别小心

[cli.py](../../../career_sim_runner/cli.py) 的 `score` 分支读取当前 active install，选择最后输出目录或该 submission 最近目录，再选目录内修改时间最新的 events/transcript；传入的 game session 却是空字符串，触发上述 DB fallback。它也把 `play_exit_code=0` 作为构造参数。

**INTERPRETATION｜解释**：这不是重新运行游戏得到的新成功退出码。新旧 active install、最后 drive、旧 output 和最新 DB 行如果并不属于同一 Run，就可能拼成一份有格式却归属错误的报告。

历史 [v4](../../project/runs/v4-run1-health-forensic.md) 的 DB 路由错配与 [v7i](../../project/runs/v7i-run1-replacement-validation.md) 的报告字段缺陷说明，空分和空 ID 都要沿独立来源判断；完整调查步骤见 [D06](../track-d-project-method/06-Forensics、失败实验与负证据.md)。v6 报告后来改变的具体覆盖原因仍 UNKNOWN，不能从当前可能代码路径倒推出唯一历史原因。

## 5. 分数回答的问题比“系统正确”窄

Quantitative score（量化评分）是本地游戏公开终局指标；Competition partial score（比赛部分评分）是返回的另一评分字段。Runner 读取已有结果，[report.py](../../../career_sim_runner/report.py) 将权重/原始值等字段格式化显示，并没有在这里运行官方隐藏评测。

**FACT｜事实**：v6 Run #1 为量化 75.29、partial 52.70、48 月、A，但运行遵循审计失败。正确的叙述是“一局已确认完成，有这些本地成绩，同时存在遵循缺陷”。不能写成“75.29 官方隐藏分”“证明策略稳定优于所有候选”或“Skill 全程正确执行”。

如果没有评分来源，写 `UNKNOWN`；如果中断，记录可确认的部分状态及停止原因，不填一个想象的零分。完整性、评分归属、成本、遵循和因果改善是不同判断。

## 6. usage 为零也可能是未采集

Usage（用量）指输入/输出 token 等被报告的值；Token（模型计量单位）不同于中文字符数。[models.py](../../../career_sim_runner/models.py) 的默认字段和 Collector 汇总允许数值为 0，但其来源完整性须另外检查。

**FACT｜事实**：S02-01 没有 WS `usage_summary` 帧，Runner 汇总为 0；历史独立 provider 日志却记录了 117 个已完成请求和 7,142,956 total tokens。它证明“Runner 未采集到 usage”不能写成“没有调用模型”。历史来源入口在[第 07 章](07-工程排障与完整运行链复现.md)。

没有账单证据时，实际 billed cost（计费成本）为 `UNKNOWN`，不是免费。补充 provider 用量也要绑定生命周期和会话，不能拿累计数字替换目标 Run 数值。

## 7. 为什么 post-run audit 存在

Audit（审计）是在已有证据上检查身份、过程和结论边界。项目的 [LIVE_RUN_WORKFLOW](../../project/LIVE_RUN_WORKFLOW.md) 规定通过明确 events/transcript/score/runner-result/llm-log 路径、运行起止时间和时区进行离线提取；[post_run_audit.py](../../../scripts/post_run_audit.py) 是项目构建的工具，不是官方评分器。

它可以汇总来源 bytes/hash、游戏一致性、行动与观察、公开终局、CTRL 标记、压缩与 Skill 重读等。Hash（内容摘要）能帮助检测内容变化，不替代源文件，不证明该源文件里的结论正确。标记匹配与等级变化仍不是自动的语义遵循或晋升机制证明。

**FACT｜事实**：v7i 的累计日志中有 23 个压缩记录，但限定本 Run 时间窗后仅有 2 个；缺少安全日志切片的 Run，其压缩字段应为 `UNKNOWN`。Raw evidence（原始证据）与 Derived summary（派生摘要）都需要保留限制，不能互相冒充。

## 8. 原始证据保留到什么时候

FORENSIC_HOLD（取证保留）表示材料仍有复核依赖或未决问题。COMPLETE、摘要和 hash 均不自动解除 hold；[旧工作区退役记录](../../project/LOCAL_WORKSPACE_RETIREMENT.md) 中，迁移后的来源仍受保留约束。

本章负责解释证据怎样生成。Raw 与派生材料怎样分层、谁接受解除条件，接着读 [C06：证据链与 hold 生命周期](../track-c-repository-tooling/06-artifacts、Raw-Evidence与证据链.md)；出现归属冲突时读 [D06：取证方法](../track-d-project-method/06-Forensics、失败实验与负证据.md)。本轮不改变任何 hold 状态。

## 9. 阅读练习

**TEACHING EXAMPLE｜教学示例，不是历史 Run 原始记录。** 一份报告写退出码 0、usage 0、分数 80，缺 game ID。此时可确认“报告含这些字段”，不能确认目标局、真实调用成本、48 月完成或 Skill 遵循。应先找正确事件绑定身份，再检查终局与来源；不能开新局来补过去的事实。
