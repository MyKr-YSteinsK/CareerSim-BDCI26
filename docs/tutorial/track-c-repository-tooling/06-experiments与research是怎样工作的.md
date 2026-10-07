# 06｜experiments 与 research 是怎样工作的

[统一入口与术语](../00-从这里开始.md) · [本 Track 阅读路线](01-仓库总览与核心工程文件.md)


## 实验目录为什么存在

Experiment（实验）不是“再跑一次碰碰运气”，而是给一个问题提供可比较的输入、过程和结果。研究者需要知道改了什么、与谁比较、测了什么、何时停止，以及结果支持什么决定。否则，一个较高分数很容易被误当成某条规则的功劳。

`experiments/`保留实验材料，`scripts/research/`保留部分实验方法代码，`docs/project/research/`保留研究报告和紧凑结果。目录职责可以互相联系，没有规定每个实验必须同时占满三处。仓库当前约定普通任务不默认新建experiment矩阵或逐任务manifest；只保留有价值的实验、失败、架构或冻结证据。

## 三种对象不要混用

| 对象 | 什么会变化 | 谁使用 | 能支持的判断 |
|---|---|---|---|
| Production/Runtime Code（正式运行代码） | 按工程合同修改 | 实际运行路径 | 怎样运行；实际调用仍需证据 |
| Experiment Snapshot（实验快照） | 一次比较前冻结，后来保留 | evaluator与复核者 | 当时比较了哪份输入 |
| Research Output（研究输出） | 按协议提取/计算 | Main及研究者 | 有界结果与未知，不自动部署 |

**TEACHING EXAMPLE｜教学示例：**你把Skill正文缩短一半，字数差异是真实可测的；是否更好遵循需要可观察行为比较；是否提高比赛分数又需要绑定Candidate与运行路径的游戏证据。三个问题不能靠同一张字数表全部回答。

## 一、当前13个tracked experiment files

**FACT｜事实：**S11-28记录两组，共13文件、66,626 bytes。如下全量索引只描述路径与角色，不打开provider result里的可能原始文本。每一对Skill是历史实验输入，正文教学去[Track A](../track-a-skill/01-从零理解Agent、Instruction与Skill.md)。

| 文件 | 类别与角色 |
|---|---|
| [s07-50/current/structured-state-board.SKILL.md](../../../experiments/s07-50/current/structured-state-board.SKILL.md) | historical configuration：当时Board输入 |
| [s07-50/current/rolling-planning.SKILL.md](../../../experiments/s07-50/current/rolling-planning.SKILL.md) | Candidate snapshot：当时Planning输入 |
| [s07-50/current/delivery-progress.SKILL.md](../../../experiments/s07-50/current/delivery-progress.SKILL.md) | Candidate snapshot：当时Delivery输入 |
| [s07-50/current/risk-review.SKILL.md](../../../experiments/s07-50/current/risk-review.SKILL.md) | Candidate snapshot：当时Risk输入 |
| [s07-50/current/runtime_manifest.json](../../../experiments/s07-50/current/runtime_manifest.json) | historical configuration：当时集成Instruction |
| [s07-50/rewrite/structured-state-board.SKILL.md](../../../experiments/s07-50/rewrite/structured-state-board.SKILL.md) | research-only snapshot：改写Board |
| [s07-50/rewrite/rolling-planning.SKILL.md](../../../experiments/s07-50/rewrite/rolling-planning.SKILL.md) | research-only snapshot：改写Planning |
| [s07-50/rewrite/delivery-progress.SKILL.md](../../../experiments/s07-50/rewrite/delivery-progress.SKILL.md) | research-only snapshot：改写Delivery |
| [s07-50/rewrite/risk-review.SKILL.md](../../../experiments/s07-50/rewrite/risk-review.SKILL.md) | research-only snapshot：改写Risk |
| [s07-50/rewrite/runtime_manifest.json](../../../experiments/s07-50/rewrite/runtime_manifest.json) | static experiment：改写的集成输入 |
| `s07-50/evals/eval_cases.json` | behavior experiment：固定公开场景与期待 |
| `s07-50/evals/provider_results.json` | behavior experiment：历史Provider结果容器 |
| `s07-50r/evals/provider_results.json` | follow-up output：独立preflight结果，不覆盖旧结果 |

这些类别会重叠：四份rewrite既是静态文本改写的产物，也是后续行为比较的输入。不要看到current就把它装成今天的current Candidate；不要看到provider_results就认定每个case已有有效模型答案。精确内容和结果以review为准。

## 二、S07-50：为什么留下一个没有成功比较的实验

[S07-50审查](../../project/reviews/S07-50_SKILL_AUTHORING_AUDIT.md) 研究当时v7n文本是否有重复语义权威、含糊门、缺边界例子等问题。它形成隔离current/rewrite副本和21个公开案例；正式Skills、Candidate和manifest没有集成这份rewrite。

**FACT｜事实：**原审查记录rewrite总字符约从34,107降至17,184。这证明文本缩短，不证明模型遵循更好。Provider尝试5次：3个连接层失败，2个成功响应却没有最终content；停止后所有比较分类为TECHNICAL_UNKNOWN，没有A/B证据支持集成。

[S07-50R后续](../../project/reviews/S07-50R_PROVIDER_AND_BEHAVIORAL_EVAL.md) 修复独立评估harness并安排preflight→sanity→matrix门。获准的一个preflight请求在HTTP响应前发生TRANSPORT_ERROR，后续sanity和matrix均未运行。旧空响应原因依旧未知，不能写成Skill失败。

```text
文本问题假设 → 冻结两组输入 → 固定公开场景
                         ↓
                Provider接口/响应门
                         ↓ 未通过
               行为比较未成立 → 不集成rewrite
```

如果把失败实验都删掉，未来人可能重新提出同样改写，却不知道以前卡在传输/响应边界，而不是已经验证无效。保留负结果能说明尚待回答的真正问题。不过它不是“所有旧文件永久保留”的理由；当方法、输入身份和边界已迁移且复验依赖闭合，过程资产可以进入退役审查。

## 三、S10-22：有search.py，不代表宏搜索完成

[S10-22研究报告](../../project/research/S10-22_SIMULATOR_POLICY_SEARCH.md) 试图通过严格公开输入的确定性Dev策略做前瞻比较。方法代码在[harness/policy/search目录](../../../scripts/research/s10_22/)，不是正式LLM Candidate。

- Harness（评估支架）对接安装的官方Dev引擎，保存opaque session（不解释内部字段的会话），把允许的public projection给策略进程。
- Policy（策略）只接受公开JSON，返回choice；不知道seed/session UUID、终局分数、隐藏计数或未来结果。
- Search（搜索编排器）保存variant/seed/gate规则，并调用harness进行batch。
- Boundary tests检查投影、poison输入、导入边界、子进程和复现。直接文件入口还会执行真实本地episode，不能在本任务运行。

**FACT｜事实：**协议定义12种宏配置，但实际只评估baseline。16-seed baseline仅2/16自然完整完成，未达到预定至少8/16完成门。14/16 early terminal，即87.5%。宏screen、confirm和128-seed holdout（留出评估）次数均为0；结果是SIMULATOR_POLICY_SEARCH_NOT_FEASIBLE。

总Dev starts为28，包括16个计分baseline与12个接口、调试、复现和warmup（预热）启动。不能把28都算成正式策略比较样本，也不能把诊断partial当作未发生。报告还明确早期六个诊断natural episode的完整trace未保留，不能逐局回放。

**INTERPRETATION｜解释：**这个负向门限制了研究路线的可行性，不证明宏策略都没有优势。baseline过弱时，再比较宏方案容易把弱Story控制的噪声当成主策略差异；因此先验证baseline能力，是为了让后面的比较有意义。这里没有恢复搜索，没有为了取得成功修改策略再跑。

## 四、静态实验、行为实验、运行实验怎么连接

Static（静态）实验可以比较字节、结构和固定条件；Behavior（行为）实验可以观察模型对公开场景的输出；Runtime实验可以检验加载、工具及长局执行。每层都有输入身份与停止条件。

```text
假设
 ↓
冻结Candidate/研究输入
 ↓
静态检查 ──失败→ 返回修复/审查
 ↓
接口与能力门 ──失败→ 记录负结果，不补造后续比较
 ↓
有界行为/运行比较
 ↓
score + adherence + 来源限制
 ↓
Main决定：集成 / 不集成 / 推迟 / 请求新证据
```

这是教学关系，当前不授权任何实验。更深的实验设计、对照和成本方法将由Track D讲解；本章只让你看懂材料怎样挂在流程上。

没有snapshot，输入变更会使同名“rewrite”不再可比较；没有结果身份，数据无法归属；没有停止记录，未执行阶段容易被误写成完成；没有Main决策，实验产物又可能未经接受就污染正式候选。

## 五、研究材料什么时候可以退出当前树

先问是否还能重算重要结论，再问是否已用权威文档/教程保留独有知识，再检查代码、tests、raw、hold及引用依赖。只按“研究已结束”删除输入和方法，会让未来复核失去依据；完全不做退役，则会让最终工程混入大量已不使用的入口。

S07-50的结果JSON是否含raw Provider文本、具体hold成员关系，S11-28只做metadata而未细读，故细分仍为 **UNKNOWN｜当前来源不足**。本教程从review引用已记录结果，不把未知内容归为可随意删除。S10-22本机证明仍有ACTIVE hold，负向结论写好也不解除它。

自查：如果search阶段为0，为什么保留search.py仍可能有价值？因为它记录当时冻结的比较方法和门，以及为何没有执行；但这种方法价值不等于永久运行核心。未来知识迁移和复验需求审查后可以作更细处置。
