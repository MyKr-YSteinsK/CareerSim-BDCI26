# 08｜.local：从 worktree 到 runtime 完整解释

[学习地图](00-学习地图.md) · [上一章](07-artifacts、Raw-Evidence与证据链.md) · [下一章：环境与缓存](09-venv、缓存、日志与可重建文件.md)

## 一个点号目录为什么装这么多东西

Local Workspace（本机工作区）保存不适合直接共享的工作状态。`.local/`并非系统运行必须拥有的统一官方目录，而是本项目对本机工程材料的固定布局。把临时checkout、证据来源、上游参考和scratch集中放置，能减少仓库外到处出现 `CareerSim-*` 副本，也能让任务记录精确位置。

**FACT｜事实：**[AGENTS.md](../../../AGENTS.md)定义四类路径，并保留根`.venv`、checkout内`.career_sim_runner`和用户目录命名实例的既定例外。布局规范不授予创建工作树、移动冻结runtime或清理证据的权限。

```text
D:\CS\CareerSim\.local\
├─ worktrees/<task>/       获准隔离任务的代码检出
├─ runtime/<task-or-run>/  有价值的运行/证据材料
├─ upstream/<identity>/    可重建的上游参考副本
└─ scratch/<task>/         临时研究、审计、派生材料

other：用于识别未落入四类的对象；S11-28快照未发现独立other顶层目录
```

## 一、先建立保留属性，而不是先排序大小

| 类别 | 典型内容 | 是否持续存在 / Git状态 | 能否重建 | Hold风险与清理规则 |
|---|---|---|---|---|
| worktrees | 分支checkout、任务diff、代码/文档 | 任务期间保留；外层ignored，子checkout有自己的Git状态 | clean已提交内容通常可重检出；未提交不能假定可重建 | 先关闭review/raw引用及child依赖，不强删脏树 |
| runtime | Run输出、取证来源、捕获、task证明 | 按价值/hold持续；ignored | 原始事件通常不能靠再跑完全重建 | 逐来源范围审查，不能整目录删除 |
| upstream | identity绑定的源码/分发参考 | 在需要对照期间保留；ignored | 有固定来源及可获取分发时可重建 | 核对是否唯一参考/取证快照后再审查 |
| scratch | Planner地图、派生JSON、临时分析 | 消费/迁移完成前保留；ignored | 输入仍可恢复时可重新派生 | 禁放唯一取证源；确认引用与消费结束 |
| other | 尚未分类的本机对象 | 由真实来源确认 | UNKNOWN | 先分类，不把“不认识”当删除资格 |

表中可重建是条件判断。重建过程也可能消耗时间、下载或改变身份，不能在当前文档任务执行。

## 二、Git Worktree是什么

Git Worktree（工作树）让一个Repository拥有多个独立检出目录。每个目录有自己的working files（工作文件）、当前HEAD和index（暂存索引），可以处在不同Branch（分支）；它们共享Git Object Database（对象数据库）。分支是提交指针，工作树是你实际编辑的文件空间，二者不是同一种东西。

```text
共享Git对象数据库：提交、树、文件内容对象
        ├─ main checkout：D:\CS\CareerSim
        │      工作文件A / 暂存索引A / main HEAD
        ├─ HPL checkout：.local/worktrees/human-play-lab
        │      工作文件B / 暂存索引B / research分支HEAD
        └─ 其他获准task checkout
               工作文件C / 暂存索引C / task分支HEAD
```

所以工作树看起来像项目副本，但不是复制整套独立Git历史的普通文件夹。共享对象减少历史重复，独立文件和索引让两个工程任务不会在同一文件上互相覆盖未提交修改。各分支的提交仍需review和整合，不会自动成为main事实。

没有独立checkout时，并行Agent可能同时改同一路径，一个人的stage混进另一个人的commit。工作树解决这一类代码协作风险。当前项目默认却是root main串行开发，只有任务明确说明隔离理由才创建branch/worktree；不是每个小文档任务都开一棵树。

### 代码隔离为什么不等于运行隔离

Code Isolation（代码隔离）保护checkout；Runtime Isolation（运行隔离）要确认服务、端口、DB、环境变量、实例配置、安装Skill目标和日志位置。两棵树可以运行不同源码，却仍指向同一 `career_emu` 实例或用户目录资源。

```text
工作树A代码 ─┐
            ├─ 若配置相同 → 同一个career_emu / 端口 / DB / Skills
工作树B代码 ─┘             相互影响并未被Git隔离
```

Runner的constants/paths决定位置，Jiuwen实例可位于用户目录；shared state（共享状态）不一定在checkout里。假如A安装新Skills，B的文件没有变化，但B实际模型读取的已安装Skills可能变化。假如A和B共用DB，latest session还可能从另一局来。

HPL后来显式路由独立run DB/log，才提供某些运行隔离证据；这来自实现与preflight，不来自分支名字。即使某路径已独立，未证明隔离的其他共享资源仍按合同串行。详见[HPL实现](10-Human-Play-Lab是怎么实现的.md)与[Runner位置模块](03-career_sim_runner源码目录导航.md)。

### 当前来源地图记录的工作树

**FACT｜事实：**以下是S11-28 metadata快照，S11-29复用而未重新盘点；不宣称子树当前干净或依赖已闭合。

| 子路径 | 分支 / 快照HEAD | 文件/bytes | 记录用途 |
|---|---|---:|---|
| `hpl-01-human-play-feasibility` | `hpl-01-human-play-feasibility` / `a874f…` | 216 / 21,117,451 | HPL早期可行性checkout |
| `human-play-lab` | `research/human-play-lab` / `860941575bfc8a8c282e69b0af20d343dd87c027` | 302 / 22,117,651 | HPL实现与review历史来源 |
| `s10-10-v6c-revival-run01` | `codex/s10-10-v6c-revival-run01` / `69f26a…` | 58 / 1,709,994 | 历史隔离运行任务checkout |

缩写HEAD用于显示，不用于验证或运行输入。当前HPL教学固定使用完整860941…提交中的指定路径，不读取整分支历史。

### 任务结束为什么还要管理工作树

提交可能已合入，但未提交文件、review引用、child父链和本机raw位置仍可能依赖工作树。只有这些责任闭合，才能按精确路径remove（移除注册工作树）。Prune（清理失效注册）处理已不存在目录的残留注册；它不是删除所有源码的日常按钮。

当前AGENTS明确不强删脏树、不例行prune。理解remove/prune用途不授予现在执行：**教学示例；当前 S11-29 不授权执行。**本章不提供通用递归删除命令。

## 三、runtime：目录名字普通，内容可能不可重建

S11-28记录 `.local/runtime` 为1,954文件、293,462,383 bytes，约280 MiB。它可能存Run events/transcript、捕获、派生证明、某任务专用环境或日志。具体成员身份取决于Run/Task，不能仅看目录名判定全部是临时文件。

“Runtime”描述用途，不保证程序此刻正在运行。运行结束后，证据可能仍需保留；一个小失败capture也可能比大成功缓存更关键。反之某个一次性中间输出如果能从已保留输入重算，未来可以退役。

**FACT｜事实：**台账指明S10-19R2 Memory、S10-19R3 helper、S10-20 controller、S10-22 policy search等本机路径有hold。S10-21准确路径仍UNKNOWN。不能为了整理目录先把未知来源移动到scratch，也不能整目录删除来“重新开始”。

[S03迁移/退役记录](../../project/LOCAL_WORKSPACE_RETIREMENT.md)给出一个更明确的例子：旧仓库外工作区已由用户人工删除，但20个准确session payload已迁移到 `.local/runtime/retired-s03-02-risk-review/session-payloads/`，原件范围按manifest和hash验证，local hold继续ACTIVE。旧目录退役与证据保留同时成立，不能把“路径删了”当“hold释放”。

唯一来源不能靠“再玩一次”重建：游戏随机轨迹、模型响应和故障时间窗口未必相同。可重复代码不等于可重复同一段raw。整理runtime必须有来源级清单、责任人与限制。

## 四、upstream：对照身份，不是在这里继续研发

Upstream（上游）是本项目所依赖或参考的外部来源。固定副本便于离线核对版本、比较接口和解释历史来源，不需要每次网络取得最新版本。Current repo是工程交付空间，上游参考不是自动替换当前冻结代码的来源。

**FACT｜事实：**S11-28记录两个对象：`career-emulator-1.0.1`下2文件、62,633 bytes；`python-3.12.10-embed`下1文件、11,133,606 bytes。它们是参考/分发副本；不表示当前root Python降为3.12.10，root仍记录为3.12.13。

若原始URL/分发身份仍可取得，副本通常可重建；如果是安装前唯一保全快照或某次工具故障的独有来源，就要先核对取证责任。不能按upstream字样推断全部是可删cache，也不能把参考源码当作获准读隐藏规则的入口。

## 五、scratch：临时派生物也有消费期限

Scratch（临时工作区）保存Planner证据、审计地图、一次性分析等可重建派生物。它默认不commit，原因是未必经过稳定接口、长期维护和来源卫生处理；把这些都塞进main会增加阅读与维护成本。

两个当前教学依赖尤其明确：

| 子目录 | 生产者 → 消费者 | 为什么暂留 |
|---|---|---|
| `s11-23-restructure-audit/` | 全量盘点 → S11-28机械source pack | 本机结构与资产源图的依据 |
| `s11-28-track-c-source-pack/` | 机械来源准备 → S11-29正式教学 | 七份导航地图，减少重新考古 |

S11-28结束的scratch快照为2,127文件、39,506,546 bytes；本教程不重新枚举其中每个文件。source pack本身七文件49,220 bytes。不commit不是“无价值”：它在消费过程中节省调查成本；不永久保留也不是“现在就删”：需等使用结束、独有知识迁移、来源可重建、后续任务不再引用并有明确授权。

如果某份scratch成为唯一取证来源，布局已违背“唯一来源不得放scratch”的治理目的；正确处置是报告和受控保全，而非把它当默认临时垃圾清掉。本任务没有搬移任何材料。

## 六、例外位置：.career_sim_runner与用户实例

`.career_sim_runner/`是Runner既定本机状态根，S11-28记录105文件、59,116,306 bytes，ignored。它可以有active install、驱动记录、输出目录、DB与日志，因此与`.local/runtime/<task>`的任务材料有交集但不是同一路径。

用户目录 `.jiuwenswarm-instances/career_emu`保存既定实例配置和工作区。它在repo之外，换checkout不会自动换实例。教学只解释角色，不打开secret-bearing配置或DB。未来管理例外要尊重冻结runtime与证据依赖，不为了目录统一改真实运行位置。

## 最后用四问代替“可否清空.local”

1. 这是源码checkout、原始证据、参考副本还是派生物？
2. 未提交修改、后续review或hold是否依赖它？
3. 原身份能否恢复，重建需要什么输入和成本？
4. 是否已有明确到路径的授权？

**INTERPRETATION｜解释：**`.local`的长期价值在于隔离工作状态和共享资产，不在于每一项永久留存。好的收口让当前core清晰，也让尚未闭合的证据不丢失。S11-29只教学，不能因为已经理解分类就开始remove、prune或清空目录。
## 深入练习：两个工程任务同时存在时，隔离到哪一层

**TEACHING EXAMPLE｜教学示例：**任务A在main编辑文档，任务B在获准工作树开发人类客户端。它们的working files不同，因此B改UI不会覆盖A的文稿。到这里，只建立代码隔离，没有任何游戏资源隔离。

若B随后使用root解释器，Python依赖又是共享的；B擅自同步环境可能影响A的Markdown核验工具。项目因此要求工作树离线检查用固定root解释器且避免隐式同步。共享解释器并非错误，但依赖写入要受明确合同控制。

若B连接同一个career_emu，服务与安装Skill目标还可能共享。A本来是文档任务，若临时运行一个环境validate，可能写实例/探针并检查后端，从而超出自身范围。工作树存在不会让这种操作自动安全。对资源的共同使用要按真正路径、端口和配置判断。

### 一个隔离检查表的用途

| 层 | 要识别的对象 | 独立checkout能否单独证明 |
|---|---|---|
| 代码 | 文件、index、HEAD、branch | 能支持这一层的独立性 |
| Python依赖 | interpreter/安装包与入口 | 不能；可故意复用root环境 |
| 服务 | 实例、监听端口、进程 | 不能 |
| 配置 | 用户目录配置、已安装Skills | 不能 |
| 数据 | DB、run/session、日志路由 | 不能 |
| 证据 | 原件、共享累计窗口、hold责任 | 不能 |

这张表不是要求S11-29新做runtime扫描，而是让读者理解“隔离”结论必须写对象。本任务只消费已有metadata和代码，不检查实时端口或进程。

### 任务完成后的三种残留

一类是clean且已经提交的checkout，可能可在依赖闭合后移除；一类是含未提交修改的checkout，不能强删；第三类是看似clean却仍被review链接或某个raw路径引用的checkout，需要先迁移引用。Git clean只回答一部分，责任闭合回答另一部分。

同样，scratch消费完成不等于runtime证明也完成。HPL客户端源码可以从固定Git提交读出，但某次manual shutdown的本机journal没有因此进入Git。删checkout与删runtime必须分别决定。

### 为什么“复制整个目录备份”也不自动解决问题

一份副本可能漏掉用户实例、外部路径、打开中的DB或未刷新log，也可能复制秘密和无关Session。声称副本足够前，应明确保全对象和身份；不能把普通文件复制包装成完整runtime隔离或hold解除。

读者真正需要的结论是：工程布局让材料更容易定位，资源隔离由具体实现与授权证明，退役由状态和依赖闭合决定。三者相互支持，但任何一个都不能替代另两个。