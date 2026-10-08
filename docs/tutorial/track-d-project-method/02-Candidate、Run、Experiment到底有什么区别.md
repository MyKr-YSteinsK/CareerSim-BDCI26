# 02｜Candidate、Run、Experiment 到底有什么区别

[统一入口与术语](../00-从这里开始.md) · [本 Track 阅读路线](01-为什么这个比赛不能靠反复改Prompt试分.md)

研发记录里的版本很多，最容易发生的错误是把“方案”“一次执行”和“研究问题”写成同一个对象。分清三者，才能回答一个分数属于谁、为什么跑这一局，以及结果能改变什么。

## Candidate：被冻结的行为身份

**Candidate（候选方案）** 是为了评估而固定的行为/策略身份。它可能包括 Instruction（主指令）、Skills（技能）、配置，以及会影响运行行为的选择。一个版本名只是索引，真正身份还要有源提交、文件内容和运行合同。

**FACT｜事实：** 项目 Candidate Evaluation Contract（候选评估合同）要求把静态身份、运行验证和评价结论分开记录。已配置的 Candidate 不能自动标为 gameplay 已验证。[候选评估合同](../../project/CANDIDATE_EVALUATION_CONTRACT.md)

**INTERPRETATION｜解释：** 冻结的意义是让问题有确定对象。若局中发现问题就改 Skill，最后分数对应的将是混合行为；如果下一局换了配置却沿用旧 Candidate 名称，比较也不再清楚。

“冻结”不要求一个方案永远不变。它要求变化建立新身份，或明确记录受控修订，而不是覆盖旧样本的解释。

## Run：一条具体执行轨迹

**Run（运行样本）** 是某个 Candidate 在一次具体环境轨迹中的执行。它有自己的 game session（游戏会话）、时间窗、工具事件、完成状态和成绩。完成、早终局、技术部分局都可以成为记录对象，只是证据类型不同。

**FACT｜事实：** v8a 两个样本的对应关系如下。Display ID（展示编号）用于最终索引，不必等同于历史任务的命名顺序。[最终 ID 映射](../../project/FINAL_ID_MAP.md)

| 对象 | Candidate | 历史运行 | quantitative / competition_partial | survival / grade / Level |
|---|---|---|---|---|
| RUN-0004 | v8a | S09-RUN07 | 72.65 / 50.86 | 48m / A / L5 |
| RUN-0002 | v8a | S09-RUN08 | 59.00 / 41.30 | 48m / C / L4 |

两条记录都保持同一冻结行为身份，但使用不同 session，经历不同轨迹。Run 编号不是版本号，RUN-0004 也不自动意味着比 RUN-0002 更新的策略。[样本一](../../project/runs/v8a-full-horizon-sample1.md) · [样本二](../../project/runs/v8a-full-horizon-sample2.md)

~~~text
同一 Candidate v8a（固定 Instruction / Skills / 相关配置）
├─ Run A：RUN-0004 / S09-RUN07 → 一条轨迹 → 72.65
└─ Run B：RUN-0002 / S09-RUN08 → 另一条轨迹 → 59.00
~~~

这张图只表达身份与样本关系，没有给出“分数差完全由随机性造成”的结论。具体差异仍需取证，两个样本也不足以估计完整分布。

## Experiment：为了回答问题而组织验证

**Experiment（实验）** 是围绕问题、假设、干预与验收规则进行的有界验证。它可以包含多个 Candidate、多个 Run，也可以只包含静态证据或部署可行性检查。

**INTERPRETATION｜解释：** “这次做了什么”不是实验的全部。还要写“它能区分哪些解释”。例如，Reviewer 的部署门禁要回答是否能建立安全只读边界，不能直接回答 Reviewer 的判断会不会提高游戏分数。

**FACT｜事实：** Reviewer 研究在 Phase A 安全部署前提未成立时停止，Phase B/C 没有运行。因此该 Experiment 有结果，但没有新增游戏 Run，也没有 Reviewer 决策质量数据。[Reviewer 可行性](../../project/research/S10-19R1_SUBAGENT_FEASIBILITY.md)

~~~text
Experiment：一个明确问题 + 假设 + 固定边界 + 判断规则
├─ 静态 / 可行性证据
├─ 可选 Candidate A → Run A1、Run A2
└─ 可选 Candidate B → Run B1
                      ↓
                 Decision（决策）
~~~

图中“可选”很重要。不是每个研究都必须先创建新 Candidate、跑满一局，再决定前提是否成立。

## 五个容易混淆的名字

| 名称 | 它主要定位什么 | 不能代替什么 |
|---|---|---|
| Candidate version | 行为/策略身份 | 具体 session 与轨迹 |
| Git Branch（分支） | 开发提交的引用 | 固定内容；分支会继续前进 |
| Git Commit（提交） | 某时点仓库内容 | 当时服务实际加载状态 |
| Run ID | 一次记录/索引 | Candidate 完整定义 |
| Stage（阶段） | 当前研究目标与治理边界 | 某个方案或单局样本 |

同一提交可以存放工程代码、教学和多个历史来源。某个 ZIP 的构建提交也可能不同于其 runtime source commit（运行源提交）。所以只看 Git 最新 HEAD，不能确定最终参赛方案。[最终方案审阅](../../project/FINAL_SOLUTION_REVIEW.md)

## 一个 Candidate 为什么可以跑多次

第一次 Run 证明“这个固定方案在这条轨迹上发生了什么”。第二次仍然需要保留身份，因为它尝试观察相同行为在另一个执行实例中的表现。

**INTERPRETATION｜解释：** 多次运行的价值在于减少只看到一个特殊结果的风险。但重复次数和研究设计共同决定证据强度。两个历史样本不是自动成为 controlled experiment（受控实验）；运行时条件、轨迹和记录方式可能仍不同。

相反，一局自然低分不能随意当成“污染样本”删除。只要符合预先定义的身份与执行条件，它就是该观察集合的一部分。技术失败可以单独分类，不能静默消失，也不能补造终局分数。

## 读记录时的身份核对

先核对 Candidate 与源身份，再查 fresh new_game（新局创建）结果和 session 绑定。接着查运行窗口、最后观察、终局/技术退出分类和成绩字段。最后看 audit（审计）与 Main 接受结论。

**FACT｜事实：** v7i 的历史故障展示了文本中的旧 session 可能被 Runner 当成当前身份，从而输出旧 v7g 的分数。文件名带 v7i 并没有解决归因。[Provider 与 stale-score 取证](../../project/reviews/S07-39_PROVIDER_CONNECTIVITY_FORENSICS.md)

## 留给读者的判断

**TEACHING EXAMPLE｜教学示例：** 某目录有 49 个配置身份，能否说“项目完成了 49 次对局实验”？不能。配置数量、Run 数量和 Experiment 数量是不同计数。S11-23 的 49 个配置身份盘点也不表示它们全部通过真实对局验证。

**UNKNOWN｜当前证据不足：** v1 完整 Instruction/raw 身份未恢复，不能为了统一表格把它补成与后期 Candidate 同等精度的身份。

需要了解一次 Run 实际怎样启动、生成 session 和结果，继续阅读 [Track B 的证据链](../track-b-system-runtime/06-日志、Session、Score与证据是怎么产生的.md)。本章的重点是判断这些对象在实验里各自承担什么角色。
