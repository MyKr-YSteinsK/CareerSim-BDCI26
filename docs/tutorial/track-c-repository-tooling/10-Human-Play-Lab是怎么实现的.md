# 10｜Human Play Lab 是怎么实现的

[统一入口与术语](../00-从这里开始.md) · [本 Track 阅读路线](01-仓库总览与核心工程文件.md)


## 来源身份先说清

Human Play Lab（人工游玩实验室，HPL）是一条人类操作CareerSim的研究路线。实现位于 `research/human-play-lab`，本章只读S11-28指定的源码/review，在提交 **`860941575bfc8a8c282e69b0af20d343dd87c027`** 固定讲解。它不是当前main的Runner目录内容，不代表整条研究分支已合入。

**FACT｜事实：**Main的[AD-HPL-001](../../project/ARCHITECTURE_DECISIONS.md)将它定义为独立人工策略实验线，不属于Candidate lineage（候选版本链），不替代S09；人类证据只作为Research Evidence / Hypothesis Source（研究证据/假设来源），不能直接改变正式Agent策略。S11-28来源定位记录其开线于2026-09-30。

当前[CURRENT_STATE](../../project/CURRENT_STATE.md)为 **CLOSED_BY_USER**。**UNKNOWN｜当前来源不足：**该路线后来由用户关闭；当前canonical source未记录具体关闭原因。不能从失败、慢、打包门或分数推断用户为什么关闭。

## 一、为什么有人工路线

来源支持的动机是探索人类操作路径、公开信息边界和独立研究证据。人类可以直接理解菜单并作选择，工程可以把这些选择和fresh state留下，用于产生策略问题和检查交互路径。

这并不证明人类总体更强，也不表示原Agent被认为无用。更个人化的动机，例如用户是否想娱乐、是否觉得模型慢，当前来源未完整记录，本章不补写。

如果没有HPL，只通过自动Agent研究，人的菜单理解与操作方式难以形成同样结构的记录；有HPL之后，仍需把研究猜想与正式Candidate验证分开，避免拿人类路线的结果替代模型遵循。

## 二、它与正式自动路线的核心区别

| 对比项 | 正式Agent runtime | Human Play Lab |
|---|---|---|
| 谁作选择 | 模型依据Instruction/Skills与观察作决策 | 人读CLI/UI上的public state和choices |
| 控制路径 | Runner驱动JiuwenSwarm/AgentServer，经配置MCP到模拟器 | 早期CLI wrapper；后期controller/adapter直接调用GameEngine |
| 是否以LLM步骤替换人类 | 本来就有模型决策 | 没有“把人当成人类Provider”的调用层 |
| 是否复用模拟器 | 是 | 是，安装的CareerSim引擎及Dev数据 |
| 是否复用完整Runner/MCP链 | 正式路径需要 | 直接HPL路径绕过它 |
| 输入绑定 | 依正式runtime/tool合同及fresh session审计 | choice整数+revision+run ID由controller检查 |
| 主要记录 | events/transcript/log/score/report | public journal/frames/manifest/trajectory/summary/integrity及本机DB/log |
| 结果可以证明 | 必须分别证明加载、遵循、结果及限制 | 该人工路径的观察/操作；不能证明模型遵循 |

```text
正式自动玩家：
模型 → choice → JiuwenSwarm工具路径 / MCP → GameEngine.take_action
                                                  ↓
                                              新游戏状态

后期HPL人工玩家：
人读public画面 → 点choice → Web/Desktop → HumanGameController
                                             ↓
                                       PublicGameAdapter
                                             ↓
                                   GameEngine.take_action
                                             ↓
                              fresh observe → 公开投影 → 新画面/记录
```

函数都可能叫take_action，是因为最后操作同一类模拟器接口；控制面不同，Provider、Skill读取、压缩恢复和工具遵循证据也不同。[Track B运行链](../track-b-system-runtime/06-Runner、Tool调用与状态更新.md)是对照阅读入口。

## 三、早期CLI：用官方交互，限制显示与输入边界

[HPL-01可行性审查](https://github.com/MyKr-YSteinsK/CareerSim-BDCI26/blob/860941575bfc8a8c282e69b0af20d343dd87c027/docs/project/reviews/HPL-01_HUMAN_PLAY_FEASIBILITY.md)选择official CLI wrapper（官方命令行外包装）路线。官方CLI负责显示公开状态/菜单、读取用户输入，调用本地GameEngine和SQLite；它不是MCP入口。

后续[scripts/hpl_play.py](https://github.com/MyKr-YSteinsK/CareerSim-BDCI26/blob/860941575bfc8a8c282e69b0af20d343dd87c027/scripts/hpl_play.py)提供路径合同、preflight、输入拦截与输出捕获。关键做法包括：

1. 明确HPL工作树/独立runtime布局，固定安装的Dev dataset路径。
2. 在模拟器storage导入前配置独立DB/log，避免默认路径冻结后才改环境变量。
3. `guarded_input`让普通输入转发，但阻止`logs`命令，因为该CLI路径可能展示不应作为策略事实的原始delta。
4. 将 `offer_share`替换为disabled callback，禁止把结束分享当成本地归档。
5. 捕获terminal观察与human选择，再经public allowlist（公开白名单）投影写证据。

HPL-01的状态只是静态路线可行，不能回写成那时已经完成真实Human Run。CLI捕获/后续GUI是不同阶段的交付。阶段名连续不保证每步都有live PASS。

## 四、后期GUI/Web：画面如何产生

[game_adapter.py](https://github.com/MyKr-YSteinsK/CareerSim-BDCI26/blob/860941575bfc8a8c282e69b0af20d343dd87c027/hpl_client/game_adapter.py)的 `PublicGameAdapter` 持有引擎、run ID、session ID、revision与当前合法choice集合。它不是新的模拟器规则实现。

`start()`调用引擎new_game，要求有效session，取得Handbook（入职手册），然后observe。`_observe()`检查回来的session相符，从state/time/status、当前event、choices、warning及ending result提取允许字段，再经过 `project_cli_frame`。每次成功观察增加revision，公开choices为空时view phase为ENDED。

这里的“空菜单→ENDED”是该版本客户端的具体条件，不是对所有CareerSim状态的抽象定理。投影如果漏掉字段、session不匹配或choice ID重复，会拒绝展示成正常可操作画面。源码没有通过读取私有DB来构建UI状态。

[app.py](https://github.com/MyKr-YSteinsK/CareerSim-BDCI26/blob/860941575bfc8a8c282e69b0af20d343dd87c027/hpl_client/app.py)将view facts渲染成时间/Level、公开状态、事件描述、warning、Handbook和choice卡片；用户点击时携带当前画面的choice、revision、run_id。不是让模型替用户选，也不是将原始engine对象序列化给浏览器。

[presentation.py](https://github.com/MyKr-YSteinsK/CareerSim-BDCI26/blob/860941575bfc8a8c282e69b0af20d343dd87c027/hpl_client/presentation.py)提供纯UI助手：检查公开Energy与公开cost、返回禁用原因；Handbook从已投影文本展示，不为打开手册再观察一次。这使显示层尽量不引入隐藏策略信息或额外动作。

## 五、一次点击怎样被约束

[controller.py](https://github.com/MyKr-YSteinsK/CareerSim-BDCI26/blob/860941575bfc8a8c282e69b0af20d343dd87c027/hpl_client/controller.py)的 `HumanGameController.choose(choice, revision, run_id)` 管操作门，先检查：

- 是否busy、是否ACTIVE、是否有当前view；
- revision是否还是当前画面，是否已经提交过；
- 给定run_id是否仍匹配；
- choice是否为整数且属于当前菜单；
- 根据public Energy/cost是否有明确禁用原因。

通过后才写submission intent（提交意图）、调用adapter.act、写新transition、更新view和最近history。失败进入TECHNICAL_FAILURE，不自动重试。

**TEACHING EXAMPLE｜教学示例：**浏览器还显示revision=8的画面，另一操作已经推进到revision=9。旧按钮再送出choice=2，哪怕整数仍合法，也可能语义已变。controller用revision拒绝旧画面；run ID则区分换局之后同样编号的选择。例子是合成说明，不是历史第8/9帧。

Adapter的 `act()`还检查当前choice集合，调用 `engine.take_action(session_id, choice, notes="")`，要求成功回执，再observe。人选choice，执行层提交，fresh observation确认下一状态；这种分层便于定位“UI提交错”“回执失败”“观察异常”，而不把一切叫模型问题。

## 六、Web层如何避免重复和串行冲突

[web.py](https://github.com/MyKr-YSteinsK/CareerSim-BDCI26/blob/860941575bfc8a8c282e69b0af20d343dd87c027/hpl_client/web.py)用本地HTTP展示同一controller。HTTP（超文本传输协议）负责浏览器请求，WebApplication把操作提交到一个event loop（事件循环），用operation lock（操作锁）串行处理。

请求携带request_id（请求身份）；WebApplication检查UUID形式、重复ID、字段集合、choice/revision类型，再调用start/choose/export/restart。HTTP层还限定loopback（本机回环）、Host/Origin和本次启动的token等边界。这里解释机制，不输出任何真实token，也不启动服务。

同样重要的是 `state()`再次投影公开facts，不直接输出整个controller/engine。选择卡片根据同一个public cost规则提供disabled_reason。这样服务器约束不依赖“按钮看起来是灰的”这一前端提示；真正动作门仍在controller。

本地HTTP不是Provider，也不是CareerSim MCP；不能因为都用网络消息就混称同一路服务。Loopback限制也不提供全部系统隔离保证，运行资源仍需要固定DB/log及身份。

## 七、证据怎样留下，为什么先写intent

[recorder.py](https://github.com/MyKr-YSteinsK/CareerSim-BDCI26/blob/860941575bfc8a8c282e69b0af20d343dd87c027/hpl_client/recorder.py)创建staging/scratch，保存manifest与 `public_journal.jsonl`。journal逐条append后flush/fsync（刷新并请求持久写入），降低程序中断时最后几条记录丢失的风险。

```text
画面观察 → observation journal
用户准备提交 → submission_intent journal
动作成功+fresh观察 → selection/下一observation
自然终止 → manifest结束状态 + structured evidence
技术失败 → 本机诊断 + UNKNOWN_AFTER_TECHNICAL_FAILURE
```

Intent证明客户端准备提交什么，不证明引擎已成功执行；成功transition和fresh state提供下一层证据。若intent后没有回执/新观察，不能把history中的选择当成确定动作结果。

[scripts/hpl_evidence_writer.py](https://github.com/MyKr-YSteinsK/CareerSim-BDCI26/blob/860941575bfc8a8c282e69b0af20d343dd87c027/scripts/hpl_evidence_writer.py)验证manifest必需字段与session一致性，重新投影frames，输出manifest、trajectory JSONL、summary和integrity；后续客户端finalizer可生成经核验的public ZIP。公共frame将observed_fact与human_interpretation分开，未知字段只记录路径等允许信息，不回写为游戏事实。

本机DB、engine log、terminal capture、staging和traceback是另一层，可能仍含未归档信息或受hold约束。Public ZIP生成不等于所有本机raw已可清理。控制器在export失败时保留来源；重试export不重复game action，这是两个不同操作。

## 八、一个真实交互故障为什么不能过度解释

[HPL-06B审查](https://github.com/MyKr-YSteinsK/CareerSim-BDCI26/blob/860941575bfc8a8c282e69b0af20d343dd87c027/docs/project/reviews/HPL-06B_QUARTER_MULTI_ACTION_AND_QUICK_RESTART.md)记录旧HPL-03公开Energy场景：开始Energy3，选cost2成功后剩1；下一次又提交cost2，被引擎拒绝。旧adapter将失败回执包装成通用RuntimeError，记录技术失败。

当前controller在真正提交前按公开cost检查，可以拒绝这类超Energy动作；同事件剩余Energy足够时仍允许后续合法动作。相关fixture测试保护这些行为。但Plan另称的“合法cost1第二动作失败”没有对应可归属来源，审查不能宣称该问题已修好，最终返回BLOCKED。

这不是某事件的答案表，也不是策略训练数据；它说明输入门、回执与未知边界。公开cost检查可以修具体不合法提交，不能解释所有第二动作失败，更不能用离线73 passed推出真实运行都顺畅。

HPL-06B还记录用户明确要求的快速重开：先确认、核对当前Run身份和可处置状态，再受控关闭/清理该局并新开。held/unknown/technical/export failure等情况不能通过该路线任意丢弃。这里仅陈述历史设计，**教学示例；本篇阅读不授权执行，当前 S11-41 也不授权运行或清理。**没有点击按钮、删除目录或调用新游戏。

## 九、研究证据能支持什么、不能支持什么

[HPL-05A](https://github.com/MyKr-YSteinsK/CareerSim-BDCI26/blob/860941575bfc8a8c282e69b0af20d343dd87c027/docs/project/reviews/HPL-05A_REAL_HUMAN_WEB_SMOKE.md)有用户启动后不完整manual shutdown记录：不是正常ending、没有正常结果ZIP，不可补为PASS。HPL-06B则保留后来人工包与未完成cleanup/发布门的边界。分支review的IN_FLIGHT_EVIDENCE身份不被教程改写成main已验收。

HPL可以支持该路径的可见菜单、人工选择、交互和公开轨迹研究。它不能证明正式Agent读取了三个Skill、在压缩后恢复、通过MCP单次提交、遵循Risk或具有稳定分数分布。即使相同模拟器版本和Dev数据，也有选择者、控制路径、环境与停止方式的差异。

**INTERPRETATION｜解释：**人类轨迹可以提出“某公开线索可能值得研究”的假设；要迁移到正式Agent，仍需定义允许的策略变更、静态合同、加载/遵循证据和有界运行比较。没有这座桥，人工成功只是一条人工成功轨迹。

## 十、关闭后的保留判断

CLOSED_BY_USER描述路线不再继续；closure reason=UNKNOWN描述解释尚无来源。二者并不矛盾。关闭不自动授权删除研究分支、工作树、local evidence或hold；也不自动否认它的教学价值。

实现源码可以教我们理解“人→choice→execution layer→take_action”的路径、快照绑定和证据记录。哪些材料长期保留、哪些迁移后退役，需要Main按依赖和来源分别审查。本章没有执行cleanup，也没有用关闭状态推测用户喜好、性能、速度或价值判断。
## 深入练习：界面状态与证据状态为什么要分开

**TEACHING EXAMPLE｜教学示例：**用户看到“行动失败”，最容易问“这一选择到底没做，还是做了但没有看到结果？”这需要沿UI→controller→adapter→engine→observe逐层确认。按钮点击是意图，HTTP接受是请求层，take_action成功回执是动作层，下一fresh state是观察层。四个状态不能合并成一个“点击成功”。

当前controller在已提交revision集合中记号，失败后不自动再发。这样牺牲了“自动重试看起来方便”，保留了未知结果纪律；不是每种失败都知道NO_MUTATION。若输入门在adapter之前拒绝非法整数、旧revision或公开Energy不足，可说明该门没有调用真实动作；若adapter已经调用而回执/观察异常，就要保留技术失败与未知边界。

### 正常结束、技术失败与导出失败

正常结束指客户端得到明确ENDED view；技术失败指动作/观察链发生异常；导出失败指已经结束的游戏在文件处理时没完成public包。第三种不应自动改写成未知game mutation，因为游戏状态本身已明确结束。

**FACT｜事实：**controller的 `_finalize_ended`将finalizer放到文件工作线程，并shield（保护等待）任务；取消等待时仍等文件工作完成，以免已知结束被误分类成未知动作。`finish_export`只重试导出，不调用gameplay。这里读代码解释责任，没有执行export。

### Fixture画面为何必须显式标NON_GAME

Web可以使用FixtureEngine生成合成画面，检验按钮、投影、journal和export路径。画面看起来像游戏，并不意味着真实GameEngine产生了该轨迹。源码给fixture单独mode及authorization标签，避免拿演示数据当真实策略证据。

本机真正Human模式还要固定数据路径和run DB/log。一个fixture按钮能点击、synthetic ZIP能核验，是交互/文件合同证据；不提供真实人类smoke或官方平台可用性。这正是HPL历史review要分别列offline PASS、manual shutdown和发布门的原因。

### 为什么这条路线值得教学，而不能直接给正式Agent记功

它把“谁选择”与“谁执行”分开，也把UI展示、操作门、引擎回执和持久记录分开。这个设计关系可以帮助读者理解交互软件工程。但是正式Agent额外有Provider、Skill上下文、工具路由、压缩与遵循问题，HPL绕过的部分不能从HPL结果中恢复证据。

所以本章支持学习实现结构和产生研究假设，仍保持CLOSED_BY_USER及关闭原因UNKNOWN，不因教材讲得清楚而重新开启人工路线。
