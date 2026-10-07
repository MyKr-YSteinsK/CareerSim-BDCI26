# 04｜Static、Runtime、Gameplay 与 Adherence 多层验证

“验证通过”必须带对象。文件校验通过，是文件满足结构合同；运行完成，是某次执行走到终局；行为遵循通过，是检查窗口里的动作与合同相符。它们之间需要证据连接。

本章用 Validation Ladder（验证阶梯）组织这些判断。**INTERPRETATION｜解释：** 这是一种教学分组，不是仓库新增的官方评级标准，也不是必须严格按时间顺序发生的流程。例如，分数已经出现时，adherence 审计仍可能失败。

## 十一层：每一层保留自己的问题

~~~text
file exists（文件存在）
  ↓ schema / static valid（结构与静态有效）
  ↓ installed（已安装）
  ↓ discovered / loaded（已发现 / 加载）
  ↓ runtime applied（运行中实际应用）
  ↓ gameplay completed（对局完成）
  ↓ behavior adhered（行为遵循）
  ↓ observed score（观测分数）
  ↓ repeatability / stability（重复性 / 稳定性）
  ↓ causal improvement（因果改进）
  ↓ hidden-test transfer（隐藏测试迁移）

箭头表示需要进一步证据；不表示上层 PASS 自动推出下层 PASS。
~~~

### 1. File exists：存在

看到一个 SKILL.md，只能确认路径上有文件。它可能内容错误、未安装，或者属于历史教学快照。

**FACT｜事实：** 七个历史代表版本有可恢复原件；版本索引同时明确区分 exact configuration（精确配置）是否有 runtime evidence（运行证据）。v5、根 v7、v7c 的对应条目没有精确归属的完整运行证据。[版本索引](../../skill-evolution/00-版本索引.md)

### 2. Static valid：静态有效

Static Validation（静态验证）检查结构、路径、合同或特定代码逻辑。它可能发现 manifest（清单）遗漏、输入格式不合法、输出要求互相冲突。它不观察长程模型是否按要求执行。

**FACT｜事实：** v6b 修复了执行合同并完成静态检查，但没有新 runtime validation。不能给它继承原 v6 的运行成绩。[S06 收口](../../project/S06_CLOSEOUT.md)

**TEACHING EXAMPLE｜教学示例：** “验证器确认 Energy 参数应是整数”与“模型实际每次都发整数”是两个命题。静态 PASS 可以阻止错误配置进入下一阶段，不能取代第二个命题的轨迹检查。

### 3. Installed：已安装

Installation（安装）让目标运行位置具备所需内容。必须检查目标内容，而不仅是安装命令返回成功。目标目录身份与源目录身份也应对应。

**FACT｜事实：** Runtime Contract（运行合同）把源身份、安装、发现与应用分开管理；工作树代码隔离不自动证明 shared runtime（共享运行时）隔离。[运行合同](../../project/AGENT_RUNTIME_CONTRACT.md)

这一层不能证明服务加载了最新内容，也不能证明后续没有被别的任务覆盖。安装副作用是独立授权动作；本轮教材没有执行安装。

### 4. Discovered / Loaded：已发现与已加载

Discovery（发现）表示运行系统能够识别入口或工具；Loaded（加载）表示组件被读入相应上下文或运行结构。文件在目录里不等于框架注册了它。

**FACT｜事实：** Reviewer 研究发现 verification factory（验证智能体构造函数）存在，但冻结 agent adapter（智能体适配层）没有把该 reviewer 注册为可部署路径。构造能力的代码存在不能代替注册证据。[Reviewer 可行性](../../project/research/S10-19R1_SUBAGENT_FEASIBILITY.md)

Skill 初始读取也只定位某个时间点。之后压缩、恢复或执行绕过，仍需另查。

### 5. Runtime applied：运行中应用

Applied（已应用）需要行为证据：组件的输入、输出或动作约束在实际窗口中发挥作用。不能只看 Instruction 声明“必须使用”。

**FACT｜事实：** v6 运行记录保留了一个 Risk RECONSIDER（重新考虑）触发案例；S06 closeout 接受局部机制证据，但不把它当成整局收益的因果证明。[v6 记录](../../project/runs/v6-run1-validation.md) · [S06 收口](../../project/S06_CLOSEOUT.md)

一次触发证明该案例发生，不能证明每个风险窗口都触发，更不能证明选择优于未触发方案。应用程度应按窗口和检查标准描述。

### 6. Gameplay completed：对局完成

Completion（完成）检查自然终局、有效成绩与 scored survival months（成绩记录的存活月数）。显示月份不应直接当成完成月数。

**FACT｜事实：** v6 最后行政状态可显示 M49，但成绩口径是 survival 48m。v7m 停在 fresh M20，仍存活，没有自然终局或终局分数。[v6 记录](../../project/runs/v6-run1-validation.md) · [v7m 取证](../../project/reviews/S07-47_V7M_M20_PARTIAL_RUN_FORENSIC_REVIEW.md)

不要把“最后看到 M20”改写成“完成 20 个月”，也不要为部分运行填入预估 final score。

### 7. Behavior adhered：行为遵循

Adherence 审查模型和执行链是否真的满足合同。它通常同时需要工具序列与语义证据：有没有 observe、风险判断是否基于新事实、标记是否对应动作、压缩后是否恢复。

**FACT｜事实：** S08-09 确认 take_action 回执只有 success/error，不能替代 public observation（公开观察）；该被审计局存在 18 个缺失 observe 的动作边界，属于真实执行违规。[运行合同取证](../../project/reviews/S08-09_RUNTIME_CONTRACT_ADHERENCE_FORENSICS.md)

语法标记通过也不能自动证明语义遵循。marker（标记）可能齐全，而 Board 内容仍旧、Delivery 判断仍没有实际交付证据。

### 8. Observed score：观测分数

Score（分数）首先需要 Provenance（来源链）：当前 Run、session、Candidate 和有效 receipt（回执）的绑定。否则只是某个文件里的数字。

**FACT｜事实：** v7i 首次故障输出了旧 v7g session 的分数，该数字被排除出 fresh-run（新运行）归因；后来 replacement（替代运行）另有 Main raw re-audit（原始材料复审）。[stale-score 取证](../../project/reviews/S07-39_PROVIDER_CONNECTIVITY_FORENSICS.md) · [替代运行](../../project/runs/v7i-run1-replacement-validation.md)

即使绑定正确，分数仍只描述该轨迹。quantitative 与 competition_partial 是不同字段，不能互换、相加或把后者写成官方 hidden score。

### 9. Repeatability / Stability：重复性与稳定性

Repeatability（重复性）关心相同身份和规定条件下能否重复观察；Stability（稳定性）关心结果在多种相关轨迹中是否可靠。

**FACT｜事实：** v8a 有两个完整样本，72.65 与 59.00；exact-v6 只有一个被接受的完整样本。项目不据此宣称稳定 75+。[最终证据审查](../../project/FINAL_EVIDENCE_REVIEW.md)

同种子重复得到同轨迹可以检查某个模拟路径的复现，却不等于新种子稳定。重复安装可以检查部署过程，却不等于策略稳定。这些“重复”对象要写清楚。

### 10. Causal improvement：因果改进

Causal Improvement（因果改进）要求能够把改动与结果区别于其他解释。样本数量、干预控制、比较条件和运行身份都影响这种判断。

**FACT｜事实：** 历史 strategy mining 存在机会、Level、tenure（任职时长）、资源与前序轨迹混杂，结论 STRATEGY_SIGNAL_WEAK。[挖掘报告](../../project/research/S10-21_REVIEW_WINDOW_STRATEGY_MINING.md)

不能用“多用 Network 的局晋升多”直接推出普遍多用 Network。该动作可能只是更好机会或资源条件的伴随现象。

### 11. Hidden-test transfer：隐藏测试迁移

Transfer（迁移）需要未被研发反复利用的新环境证据。Local Dev（本地开发集）结果并不自动回答 official hidden Test 的问题。

**FACT｜事实：** 官方上传未执行/未获证明，platform score（平台成绩）与 hidden-test transfer 都是 UNKNOWN。[官方来源锁](../../project/OFFICIAL_SOURCE_LOCK.md) · [最终方案审阅](../../project/FINAL_SOLUTION_REVIEW.md)

遵守公开信息边界、保留负结果、限制试分，有助于降低误判，但仍不是迁移已成功的证据。

## 怎样审查一句“4 passed”

**TEACHING EXAMPLE｜教学示例：** 设想一个执行结果写“4 passed”。在看数字之前，应问四个检查各自输入什么、assert（断言）什么，以及调用了哪些实际组件。

如果四个检查覆盖非法参数、路径解析、标记解析和清单成员，它们证明的是这些合同在测试输入上成立。它们没有观察模型在 48 个月里保持事实新鲜度，也没有观察隐藏评测。

如果检查使用 fixture（受控装置）代替 shared service，结果仍可能非常有价值：它能准确验证某个 guard（守卫条件）或 callback。但结果必须带“fixture”边界，不能换成“真实服务的所有行为都已通过”。

**FACT｜事实：** Reviewer 的离线检查使用提取的实际函数与 inert sentinel（不触发真实动作的哨兵对象）；Helper / Memory 使用隔离实际工具或回调。报告都保留了 shared registry 或模型行为尚未测量的边界。[Reviewer](../../project/research/S10-19R1_SUBAGENT_FEASIBILITY.md) · [Helper](../../project/research/S10-19R3_NATIVE_CONTROL_SURFACE_AUDIT.md) · [Memory](../../project/research/S10-19R2_MEMORY_FEASIBILITY.md)

**INTERPRETATION｜解释：** 测试数量不是证据强度的快捷指标。一个精确击中故障机制的检查，可能比许多不相关检查更有价值；一个完整游戏也不一定覆盖压缩恢复或特定风险触发。

## 验证窗口与覆盖率必须有分母

**INTERPRETATION｜解释：** “风险门全部通过”需要说明全部是什么：全部动作、所有触发窗口，还是所有可解析标记？“没有违规”还要区分确实检查没有问题，和材料缺失导致无法检查。

同样，marker coverage（标记覆盖）至少需要定义唯一动作、去重、绑定和缺失策略。若一个工具调用同时出现在 event 与 delta 里，把它当两次会改变分母。

**FACT｜事实：** v7m 取证按 kind/tool_call_id 去重；v6 的 CTRL 形似文本无法认证动作绑定；v8a 两个样本 parser 对邻接格式的接受不同。[v7m 取证](../../project/reviews/S07-47_V7M_M20_PARTIAL_RUN_FORENSIC_REVIEW.md) · [v6 记录](../../project/runs/v6-run1-validation.md) · [v8a 样本一](../../project/runs/v8a-full-horizon-sample1.md)

这些案例提醒我们：覆盖率首先是某个测量定义的结果。定义正确并且来源充足时，它才能回答实际遵循问题。

## 两个轴，避免“完成就全通过”

| 运行结果轴 | 合同轴 | 合法表述 |
|---|---|---|
| v6 有效 48m 完成 | adherence FAIL | 保留真实分数，同时保留执行缺陷 |
| v7m 技术部分局 | 局部序列可以审计 | 保留 84 次成功动作证据，不造终局成绩 |
| 静态 Candidate | 尚无实际应用证据 | 只标静态验证状态 |

**INTERPRETATION｜解释：** 一个成熟报告应该允许这些组合存在。强迫所有信息压成一个 PASS/FAIL，会让“成绩差”“调用断开”和“规则没执行”失去各自意义。

需要理解实际安装、MCP 和 Runner 细节，阅读 [Track B 运行链](../track-b-system-runtime/10-从零复现一条完整运行链.md)。本章用于解释这些检查为何不能互相代替。

---

[学习地图](00-学习地图.md) | [上一章](03-从Evidence到Decision的完整实验方法.md) | [下一章](05-从S01到S11整个项目到底做了什么.md)
