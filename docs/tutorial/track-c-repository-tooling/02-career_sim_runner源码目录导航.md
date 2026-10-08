# 03｜career_sim_runner 源码目录导航

[统一入口与术语](../00-从这里开始.md) · [本 Track 阅读路线](01-仓库总览与核心工程文件.md)


## 先看职责，再看文件

Runner（运行驱动器）连接提交目录、本机实例、AgentServer和运行报告。它本身不是模拟器规则全集，也不是比赛Agent的决策Skill。Track B已沿运行链解释它如何工作；本章提供打开源码时的定位方法。

**FACT｜事实：**当前主要模块分工如下。表里的失败表现是 **INTERPRETATION｜解释**：说明这一层出问题可能影响哪里，不能代替真实错误诊断。正式身份仍以[官方锁](../../project/OFFICIAL_SOURCE_LOCK.md)为准；不因教学修改冻结Runner。

```text
用户/工程操作者
       ↓
__main__ / cli
       ├─ setup + paths + constants        环境与位置
       ├─ skill_contract + validate        提交结构/环境检查
       ├─ install                          安装提交
       ├─ headless_play → ws_client        驱动与连接
       │                     ↓
       │                  transcript       流式记录
       └─ score → db / transcript          报告与结果来源
                   ↓
                models + report            结构与人读输出
                   ↓
                replay/                    事后或增量浏览
```

## 一、入口：用户的命令变成哪条路径

| 模块 | 输入、输出与调用者 | 定位失败时的线索 |
|---|---|---|
| [__main__.py](../../../career_sim_runner/__main__.py) | 将模块执行交给CLI main | 模块入口无法启动，先看导入与解释器 |
| [__init__.py](../../../career_sim_runner/__init__.py) | 导出main供包使用 | 包级导出/导入问题，不是游戏动作问题 |
| [cli.py](../../../career_sim_runner/cli.py) | 解析setup、validate、install、play、score、replay参数；分派函数并设置标准输出编码 | 参数错误、编码错误或选错子命令 |

CLI（命令行接口）的价值是统一操作入口。它把字符串参数变成路径、超时、模式等，再交给真正执行模块。不能看到一个命令名就推断它是只读。例如CLI main在解析参数前就调用 `ensure_runtime_dirs`；环境validate也有写探针和后端检查。此任务只读源码，没有调用Runner CLI。

“入口成功”只说明程序进入了下一层；它不证明安装成功、服务可达或模型遵循。这种逐层定位能避免用一次重跑掩盖最初失败。

## 二、位置与配置：程序究竟把东西放在哪儿

| 模块 | 职责及输入/输出 | 谁依赖它、坏了可能怎样 |
|---|---|---|
| [constants.py](../../../career_sim_runner/constants.py) | 定义repo根、实例根、runtime根、默认超时和模式等常量 | 路径/驱动模块；错误位置可能导致跨任务串用状态 |
| [paths.py](../../../career_sim_runner/paths.py) | 计算DB、日志、runs、outputs、实例配置与Skill路径；生成输出目录和读取本机身份文件 | setup、install、play、score；可能找不到文件或拿错输出 |
| [setup.py](../../../career_sim_runner/setup.py) | 初始化实例、环境overlay、检查工具位置、解析实例WebSocket URL | CLI及validate；工具不在调用进程PATH可使驱动前失败 |
| [mcp_config.py](../../../career_sim_runner/mcp_config.py) | 检查配置文本是否提及模拟器及DB路径 | validate；字符串命中不等于实际工具注册 |

**FACT｜事实：**默认命名实例是 `career_emu`，用户目录实例在 `.jiuwenswarm-instances/career_emu`，Runner本机数据根在repo内`.career_sim_runner/career_emu`。`paths.py`也处理 `JIUWENSWARM_DATA_DIR` 覆盖。路径契约比“我开了另一个工作树”更直接地决定状态是否共享。

WebSocket（双向长连接）是Runner与AgentServer交换驱动消息的通道。这里不展开协议；[Track B 第04章](../track-b-system-runtime/04-JiuwenSwarm、AgentServer与MCP分别是什么.md)有系统分工。配置文件出现MCP名字只是一项静态提示，端点、工具schema及实际回执仍有独立证明责任。

## 三、安装与合同：源文本如何成为运行输入

| 模块 | 职责及大致输入/输出 | 调用关系与失败含义 |
|---|---|---|
| [skill_contract.py](../../../career_sim_runner/skill_contract.py) | 读取manifest、定位Skills、检查模式、字段与frontmatter（文件头元数据） | install/validate；结构不匹配时应在模型运行前发现 |
| [install.py](../../../career_sim_runner/install.py) | 按提交目录安装Skills与状态，保存InstallRecord，提供读取active install能力 | CLI或headless play；装错身份影响实际模型上下文 |
| [validate.py](../../../career_sim_runner/validate.py) | 分开验证提交结构与环境，组合ValidationReport | CLI；字段PASS与后端PASS属于不同问题 |

Manifest（清单）告诉系统包叫什么、模式是什么、Instruction是什么；Skill文件提供行为规则。不同检查器的范围要分别看：冻结 Runner 的 `validate_manifest` 只检查 team / mode，不检查 Instruction 正文是否为空；提交结构与 Skill frontmatter 检查负责各自的文件和格式要求。项目打包器的额外检查不能归给 frozen validator。检查通过仍不能判定策略好坏或证明模型读过，具体范围见[Track B 提交校验](../track-b-system-runtime/03-Submission校验与Skill安装.md)。

一个重要源码细节：`validate_submission`主要检查提交结构，`validate_environment`会创建必要目录、初始化/overlay实例、在DB父目录写入并删除探针，还调用后端可达检查。因而“validate听起来像检查”不等于全部验证无副作用。不能在本任务中为了确认教材而执行它。

安装也不是普通复制教程文件。它作用于运行工作区，可能清理或重置已安装Skill状态。这是为什么[Track B 安装章](../track-b-system-runtime/03-Submission校验与Skill安装.md)把安装身份与读取身份分别举证，工程任务不会默默调用install。

## 四、驱动与流式记录：让一次任务有始有终

| 模块 | 大致输入/输出 | 谁调用、关注何种失败 |
|---|---|---|
| [headless_play.py](../../../career_sim_runner/headless_play.py) | submission、ws URL、DB、超时及continue标志 → 驱动结果和报告 | CLI play；drive身份、续接及收尾边界 |
| [ws_client.py](../../../career_sim_runner/ws_client.py) | 驱动提示/模式/连接 → DriveResult、帧、usage、终止原因 | headless play；连接、超时、协议与终止问题 |
| [transcript.py](../../../career_sim_runner/transcript.py) | StreamCollector接收帧、整理文本并finalize输出 | ws驱动；缺帧、乱序或截断会影响事后审计 |
| [prompts/](../../../career_sim_runner/prompts/) | 启动/续接等Runner提示模板 | ws驱动路径；属于运行文本，不是HPL人类选择提示 |

`headless_play`负责“安装（如提供）→驱动→计分/写报告”的编排。`ws_client`负责连接、消息和结束状态。`transcript`负责将流式消息留下。把这三层分开，能同时回答“动作是否执行”“连接是否中断”“记录是否足以证明”。

drive session（驱动会话）与game session（游戏会话）有不同职责。前者标识Agent驱动过程，后者绑定模拟器世界。名字都叫session不能说明它们可互换。[Track B日志章](../track-b-system-runtime/06-日志、Session、Score与证据是怎么产生的.md)进一步解释。

**TEACHING EXAMPLE｜教学示例：**连接在一个动作提交后断开。仅凭没有后续文本，无法判断动作没执行；仅凭记录文件存在，也无法判断动作成功。应核对授权内的fresh observation（新鲜观察）及身份，不能盲重发。这里说明失败定位，没有启动连接。

## 五、结果与人读输出：有分数不等于有正确归属

| 模块 | 职责及输入/输出 | 可能误解 |
|---|---|---|
| [db.py](../../../career_sim_runner/db.py) | 提供latest session、payload和ending score读取助手 | 是运行代码能力；本教程没有查询DB |
| [score.py](../../../career_sim_runner/score.py) | InstallRecord、session、usage和输出路径 → ScoreReport；可从DB或transcript回退取结果 | 回退结果必须审查是否属于本局 |
| [models.py](../../../career_sim_runner/models.py) | ValidationCheck/Report、TokenUsage、InstallRecord、ScoreReport等数据结构 | 字段默认值不自动成为测量事实 |
| [report.py](../../../career_sim_runner/report.py) | 将验证及分数结构格式化为人读文本 | 易读报告不替代来源身份 |
| [utils.py](../../../career_sim_runner/utils.py) | `normalize_text`等通用文本规范化 | 展示规范化与冻结字节比较要区分 |

当前 `build_score_report` 若未获得明确session，会查latest session；DB结果缺失时可能从transcript抽取。这个设计让报告较容易生成，也带来来源绑定的审计责任。历史v7i曾在首次fresh observation前失败，却输出更早v7g分数；canonical审阅将它排除。不能因此说score模块的每次回退都会错，也不能不核身份地接受一切分数。见[最终证据审阅](../../project/FINAL_EVIDENCE_REVIEW.md)。

模型里的TokenUsage默认数值与审计结论有区别：项目证据合同明确缺失usage记UNKNOWN，不把默认0当作实际零消耗。结构保证可序列化；事实保证要靠来源。报告里任何看似精确的数字都应有输入身份。

## 六、replay：重新看记录，不等于重新玩

| 文件 | 作用 |
|---|---|
| [replay/__init__.py](../../../career_sim_runner/replay/__init__.py) | 导出回放报告接口 |
| [replay/models.py](../../../career_sim_runner/replay/models.py) | choices、observation、decision turn等回放结构 |
| [replay/parse.py](../../../career_sim_runner/replay/parse.py) | 将选定events解析为观察/决策关系 |
| [replay/render.py](../../../career_sim_runner/replay/render.py) | 生成Markdown或终端人读报告 |
| [replay/live.py](../../../career_sim_runner/replay/live.py) | 增量接收记录并展示；不是决策玩家 |
| [replay/usage.py](../../../career_sim_runner/replay/usage.py) | 读取邻近报告、呈现usage及ending相关信息 |

Replay（回放）可以帮助人检查一局过程，但解析不到的部分应保留未知。它不会凭空恢复丢失帧，也不会因为渲染顺利就证明原session全部完整。“live replay”中的live描述增量显示，不能推导它会替Agent采取游戏动作。

## 阅读源码的实用顺序与保留判断

找入口从cli开始；找安装从skill_contract→install开始；找动作驱动从headless_play→ws_client开始；找证据从transcript→score→replay开始；找本机共享从constants→paths→setup开始。每次沿实际调用链读少数文件，比从第一个文件逐行读到最后更容易形成关系。

这一组模块构成运行/记录能力。随意删一个“看起来只输出文本”的模块，也可能破坏CLI导入或收尾报告。因此当前属于核心工程资产；真正退役某条路径，需要先确认调用者、包入口和冻结合同，而不是看它有没有直接调用take_action。

自查：`db.py`是合法的Runner模块，是否意味着任意文档任务可以查询本机DB？不意味着。源码职责与任务权限不同；S11-29只读取代码，DB query=0。理解能力边界，才不会把“项目支持某功能”误当成“现在允许操作”。
