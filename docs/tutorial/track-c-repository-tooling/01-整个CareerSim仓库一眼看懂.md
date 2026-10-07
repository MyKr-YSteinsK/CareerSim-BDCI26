# 01｜整个 CareerSim 仓库一眼看懂

[学习地图](00-学习地图.md) · [上一章](00-学习地图.md) · [下一章：根文件](02-根目录与核心工程文件.md)

## 先分清三个“项目”

Repository（代码仓库）是 Git 管理的版本集合；Current Tree（当前文件树）是某个提交在检出目录呈现的文件；Local Workspace（本机工作区）还包含依赖、日志、临时输出和未进入 Git 的证据。资源管理器看到的是第三者，而别人克隆仓库主要拿到第一者在某个提交的当前树。于是，本机有一个目录，不代表别人克隆后也有；某目录被 ignore，不代表那里绝无 tracked 文件。

**FACT｜事实：**S11-28 地图记录了当前主要对象。下图保持真实顶层名称；层名属于 **INTERPRETATION｜解释**，帮助理解职责，不是代码新增的目录。

```text
CareerSim repo
│
├─ Runtime layer（运行层）
│  ├─ career_sim_runner/     本仓库的安装、驱动、记录与报告代码
│  └─ pyproject.toml、uv.lock 依赖与锁定关系
├─ Candidate layer（候选方案层）
│  ├─ configs/               当前候选元数据与运行 manifest
│  └─ skills/                当前四份 Skill 文本及占位文件
├─ Tooling layer（工程工具层）
│  ├─ scripts/               打包、审计、研究、公开接口玩家
│  └─ tests/                 工具、文本、身份、解析与包装合同
├─ Experiment layer（实验层）
│  └─ experiments/           S07-50 系列输入快照和评估结果
├─ Evidence layer（证据层）
│  └─ artifacts/dev-runs/    选定并扫描的开发运行归档
├─ Documentation layer（文档层）
│  ├─ docs/                  权威状态、合同、报告、历史与教学
│  └─ submission_materials/  提交说明及设计文稿来源
└─ Local workspace layer（本机工作区层，通常 ignored）
   ├─ .local/               工作树、运行材料、上游副本、scratch
   ├─ .venv/                已安装 Python 与第三方依赖
   ├─ .career_sim_runner/   Runner 本机状态与输出
   └─ logs/、缓存等           身份和生命周期各不相同
```

官方模拟器和 JiuwenSwarm 是通过依赖安装的包，不等于 `career_sim_runner/` 本身。[Track B 官方提供什么](../track-b-system-runtime/01-比赛官方到底提供了什么.md)讲这些系统的归属；本章只把它们放回工程地图。

## 各目录是谁的工作台

| 对象 | 主要使用者与用途 | 是否参与一局正式运行 | 产生时点与保留理由 |
|---|---|---|---|
| [configs/](../../../configs/) | 候选维护者、包装脚本；声明身份与 Instruction | 通过打包、安装被使用；不能把源文件存在当成已加载 | 候选修改时产生；保留来源身份 |
| [skills/](../../../skills/) | 模型通过运行层读取；开发者编辑规则 | 被安装并实际读取时参与 | 策略开发资产；当前四 Skill 不是最终三 Skill ZIP |
| [career_sim_runner/](../../../career_sim_runner/) | 运行操作者；衔接提交、服务、动作与报告 | 参与正式 Runner 路线 | 工程运行核心，受冻结身份约束 |
| [scripts/](../../../scripts/) | 开发者、研究者、审计者 | 因脚本而异；事后提取器不参与动作 | 工程需求出现时产生；按职责及依赖决定保留 |
| [tests/](../../../tests/) | 开发者；自动检查明确断言 | 通常不被正式 gameplay 加载 | 保护合同和既往修复；不等于比赛必须提交 |
| [experiments/](../../../experiments/) | 研究者；保留输入/结果对照 | 历史快照不自动成为当前策略 | 实验时冻结，保留比较和复现来源 |
| [artifacts/](../../../artifacts/) | 审计者；选定运行包 | 是运行产物及派生材料，不是全部运行输入 | 运行后归档，受来源/hold约束 |
| [submission_materials/](../../../submission_materials/) | 最终构建器与人类评审 | 文稿不替模型选择行动 | 最终提交解释层的来源 |
| [docs/](../../) | Main、开发者、学习者 | 教程不参与比赛执行；合同影响工程行为 | 保存可审的状态、判断、方法和学习资料 |
| `.local/` | 本机工程任务和证据管理者 | runtime 子项可能有关；scratch一般无关 | 任务工作状态，默认不共享到Git |
| `.venv/` | Python 程序与工具 | 提供真实运行依赖 | 按依赖身份安装，可重建但不能随意扰动 |

目录在同一个 repo，**不等于它们都参与一次 Agent gameplay**。例如，S09 的 forensic（取证调查）脚本分析已经完成的公开轨迹；`docs/tutorial/` 帮助人理解工程；它们和正式 Runner 有关系，但不在每次模型动作的调用链上。

## 从一次运行看文件怎样合作

**TEACHING EXAMPLE｜教学示例：**设想一个获准的开发运行。工程人员先核对候选身份，将 manifest 与 Skill 包装成提交目录；Runner 安装并驱动运行；模拟器和模型产生事件、文本及结果；工程人员用审计脚本整理摘要，再把结果写入 Run Record（运行记录），由 Main 作出决策。

```text
configs + skills → 包装/安装 → Runner → Agent/MCP/模拟器
                                      ↓
                                本机运行输出
                                      ↓
                         audit / 选定的 evidence archive
                                      ↓
                       docs/project 中的记录与决策
                                      ↓
                          docs/tutorial 中的讲解
```

这幅图省略服务细节，没有执行任何步骤。**教学示例；当前 S11-29 不授权执行。**真正的安装与运行链在[Track B 第 06 章](../track-b-system-runtime/06-Runner如何启动并驱动一局CareerSim.md)。

如果只保留 Skill，别人不知道怎样安装、用什么依赖、哪份结果属于它。如果只保留日志，别人不知道输入身份及结论。如果只有结论而没有必要来源，遇到身份争议就无法再核对。工程仓库把这些关系连接起来，是为了使改变和判断可以被审阅。

## 当前候选、历史快照和最终包不是同一份东西

**FACT｜事实：**当前 checkout 的 `configs/` 与 `skills/` 属于 v8a 四 Skill 工程状态；最终冻结选择却是历史 exact-v6，源提交 `1114a04b75548cf52f030d123564e527060fc061`，Single Agent + 3 Skills。冻结 ZIP 是 18,082 bytes、7 个文件。官方上传及平台评测尚未发生。来源见[当前状态](../../project/CURRENT_STATE.md)、[最终身份](../../project/FINAL_SUBMISSION_IDENTITY.json)。

因此，打开当前 `skills/` 看见 `delivery-progress`，不能推断最终 ZIP 也包含它。脚本 `package_candidate.py` 针对当前四 Skill，`build_final_solution.py` 的 exact-v6 路径针对冻结的历史身份。两个包装问题有不同输入，详见[脚本章](04-scripts为什么这么多以及分别做什么.md)。

同样，`experiments/s07-50/current/` 中的 current 是实验发生时的版本标签，不是“永远指向现在”。文件名的自然语言含义必须与日期、提交和来源一起解读。

## 当前树与本机状态的关系图

```text
Git 历史：保存被提交过的版本
        │ checkout 某个提交
        ▼
当前树中的 tracked 文件 ──────── 可形成下一次 Git diff
        │
        ├─ 安装依赖 → .venv/                  ignored
        ├─ 运行程序 → .career_sim_runner/     ignored
        ├─ 工程任务 → .local/scratch/         ignored
        └─ 运行证据 → .local/runtime/         ignored，可能受hold
                         │ 明确选定 + 扫描 + 归档
                         ▼
               artifacts/dev-runs/ 中部分tracked文件
```

Tracked（已跟踪）是一种 Git 状态；Canonical（权威）是一种事实职责；Held（受保留约束）是一种生命周期限制。它们是三个不同维度。一个本机 ignored 原件可以是唯一证据；一个 tracked 历史 review可以已被权威总结吸收；一个小 manifest可以很重要，却不能替代它记录的大原件。

`.gitignore` 也不会把已跟踪归档从历史或当前树自动撤掉。这个表面上的“例外”来自显式归档流程，不能推广成随意 force-add整个日志目录。忽略规则及字节规则见[根文件章](02-根目录与核心工程文件.md)。

## 如何开始看一个陌生目录

先找到人读入口，再找到机器入口，最后检查身份和验证边界。人读入口告诉你目标；机器入口告诉你实际调用；身份告诉你是哪一版；验证边界告诉你哪些结论尚未成立。不要把大小排序当成重要性排序，也不要把最近修改时间当成权威性排序。

**INTERPRETATION｜解释：**本项目可以看成“执行一次选择”和“使一次选择可解释、可审阅”两组工作互相支撑。前者依赖运行代码和候选文本，后者依赖工具、测试、来源与文档。缺一组都会使项目难以可靠地继续开发。

自查：`docs/tutorial/` 不参与对局，是否因此可以随时删除？不能这样推导。它对运行不是关键输入，却可能是长期学习资产；删除还要检查用户价值、引用和任务授权。运行关键性只是保留判断的一项，完整规则在[第 12 章](12-哪些文件值得长期保留以及哪些最终可以删除.md)。