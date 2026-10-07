# Forensics、失败实验与负证据

[四条学习路线与术语](../00-从这里开始.md) · [本 Track 入口](01-为什么这个比赛不能靠反复改Prompt试分.md)

看到低分、断连或审计 FAIL，先要重建实际发生的事件，再给结果分类。Forensics（取证分析）解决前一个问题，负结果记录保存后一个判断。把两步连起来，才能避免把技术故障归给策略，或把未测试路线写成失败。

## 按问题跳读

- [从记录重建发生了什么](#从记录重建发生了什么)
- [给结果分类，并保留停止理由](#给结果分类并保留停止理由)

## 从记录重建发生了什么

**Forensics（取证分析）** 根据原始或结构化记录重建“实际发生了什么”。它尤其适合结果和运行链不一致的情况：分数属于谁？工具回执有没有新状态？模型有没有恢复？一个审计 FAIL 是真实违规还是解析器误解？

**解释：** 取证的价值是缩小可支持的结论范围。它既可以确认问题，也可以证明某个常见解释没有足够证据。UNKNOWN 不是取证失败的同义词。

先读 [多层验证 多层验证](03-实验方法与多层验证.md#实验结果通过了哪一层验证) 与 [D07 样本边界](07-分数、不确定性与反过拟合.md)。下面完整展开 stale score、session provenance、CTRL 配对三案；其余案例也保留需要核对的证据、替代解释和判断边界，可以按小标题查询。证据怎样生成查 B08，怎样保留查 C07。

这里引用 canonical summaries（权威摘要）与已去敏研究记录，不展开 raw payload（原始载荷），也不重新进行 live 诊断。

### Stale score：文件里有分数，不代表属于这次运行

**表面现象：** v7i 故障尝试仍输出了 score report。

**可能解释：** 新局已发生但没有记录；报告查询了旧 session；文本中的历史 session 被当成当前身份。

**需要证据：** fresh new_game/observe 的 session，报告 session，Runner 提取身份的代码路径。

**FACT｜实际查到：** S07-38 的报告 session 属于此前 v7g。Runner 除了结构化结果，还可从 transcript（运行文本）中的 SESSION_ID 提取身份；在缺少新结构化身份时存在 stale-score hazard（过期成绩风险）。[S07-39 取证](../../project/reviews/S07-39_PROVIDER_CONNECTIVITY_FORENSICS.md)

**可下结论：** 该分数不是 v7i 新局成绩，必须排除。**仍不能下结论：** 输出报告文件不证明 v7i 达到同等表现，也不证明新的 session 已存在。

### Provider failure：今天可连接，不解释昨天为什么失败

事故可能发生在 DNS、TLS、代理或服务端，核对时要保留当时异常链、HTTP 响应和诊断时间窗。**事实：**历史连接异常发生在 HTTP 响应前，没有状态码；后续 DNS/TCP/TLS 和一次 metadata request 通过。后续检查只确认后续窗口可达，不能认定历史唯一根因，也不自动授权替代局。

来源：[S07-39 取证](../../project/reviews/S07-39_PROVIDER_CONNECTIVITY_FORENSICS.md)。方法要点是把事故证据与事后诊断分开；当前没有重新做网络检查。

### Session provenance：缺字段不等于身份完全不可恢复

**表面现象：** v7i replacement 的 score_report 有 session-field defect（会话字段缺陷）。

**可能解释：** 成绩错配，报告格式缺陷，或者源事件能够独立绑定同一运行。

**需要证据：** fresh session、事件序列、成绩来源和 Main re-audit（复审），不能只依靠输出目录名。

**FACT｜实际查到：** replacement 记录经 Main 原始证据复审接受了 64.0 /44.8/48m/B，同时保留报告 session 字段缺陷。[替代运行记录](../../project/runs/v7i-run1-replacement-validation.md)

**可下结论：** 在已接受的来源链范围内归属这条成绩。**仍不能下结论：** 所有空 session 报告都可信。这个案例与 stale score 必须一起理解：不能一律接受，也不能一律否定，要看独立绑定证据。

### v7m：时间相邻不等于因果机制

查询影响连接、共同底层原因和未记录异常都可以成为待查解释，需要核对 fresh observe、动作回执、client/server 时间线及查询调用路径。**事实：**84/84 动作成功、85 unique observes；查询后仍推进到 M20 存活，只读 stdout 查询没有直接写入或调用机制。结果保持 `PARTIAL_GAMEPLAY_TECHNICAL_FAILURE`；“查询导致终止”不获支持，根因仍为 `INSUFFICIENT_EVIDENCE`，不能预测最终分数。

来源：[v7m 取证](../../project/reviews/S07-47_V7M_M20_PARTIAL_RUN_FORENSIC_REVIEW.md)。时间相邻可以提出假设，不能独立提供因果机制。

### Fresh state：成功回执不等于状态观察

先检查 tool result 字段和动作/observe 序列，才能区分“回执已经包含状态”与“审计漏读”。**事实：**S08-RUN03 回执仅有 success/error，不含 state/event/choices，18 个缺 observe 边界是真实违规。因此不能以 success 代替 fresh state，也不能从缺观察数推算分数损失。

来源：[S08-09 取证](../../project/reviews/S08-09_RUNTIME_CONTRACT_ADHERENCE_FORENSICS.md)。接口闭环本身见 [请求与回执](../track-b-system-runtime/06-Runner、Tool调用与状态更新.md#一次选择怎样成为外部动作)。

### Compression：恢复文字不是来源重读

恢复时保留了完整来源，还是只留下摘要，需要核对 compressor epoch、read_file、新观察以及合同定义的时间关系。**事实：**v6 两次压缩后均没有 Skill reread；原报告采用 S06-25 recovery definition，v6b 后续合同更明确。重新注入的 state text 不证明已重读，也不能据此认定所有后续错误由压缩造成。

来源：[v6 记录](../../project/runs/v6-run1-validation.md)、[S06 收口](../../project/S06_CLOSEOUT.md)。恢复条款查 [A02](../track-a-skill/02-exact-v6-Instruction逐句拆解.md)，取证须保留后续定义与历史合同的时间关系。

### CTRL/action：文字数量不能充当唯一动作映射

**表面现象：** CTRL 标记数量很多，看起来足以覆盖动作。

**可能解释：** 每动作都有标记；delta/event 重复表现；一个模型回合多次出现同类文本。

**需要证据：** tool_call_id（工具调用 ID）、可靠 model-turn ID（模型回合 ID）、事件去重规则和绑定语义。

**FACT｜实际查到：** v6 有 418 个 marker-shaped occurrences（形似标记的出现位置），对应 203 次动作尝试；来源缺少可靠模型回合绑定，无法据文字计数认证一一配对。v7m 原始事件的多种表示也需要按 kind/tool_call_id 去重。[v6 记录](../../project/runs/v6-run1-validation.md) · [v7m 取证](../../project/reviews/S07-47_V7M_M20_PARTIAL_RUN_FORENSIC_REVIEW.md)

**可下结论：** 审计可配对性存在限制。**仍不能下结论：** 标记很多证明全覆盖，或者精确判定每个动作都缺失了多少标记。

### Hidden evidence：分析者能看见，不代表玩家能使用

判断分析字段或内部信息是否进入策略输出，应核对 participant-visible（参与者可见）输入定义、引用位置与用途。**事实：**v8a 两个样本均保留 HiddenRisk 数值引用限制。内部数值不能成为可部署规则；引用限制也不证明两局分差由它造成。

来源：[样本一](../../project/runs/v8a-full-horizon-sample1.md)、[样本二](../../project/runs/v8a-full-horizon-sample2.md)。这里区分保存技术来源与准许玩家使用信息，抗过拟合边界见[分数与不确定性](07-分数、不确定性与反过拟合.md)。

### 同一 parser 的 FAIL，怎样区分工具问题与行为问题

**解释：** 审计器是一段带假设的程序，不是自动拥有全部语义的裁判。FAIL 可能来自真实违规、格式合同不明确、解析规则过窄或证据不足。把这几类分开，才能决定改 Candidate、改 parser，还是保留 unknown。

**事实：** S08-09 在确认缺 observe 为真实违规之外，还检查 CTRL closure（控制标记关闭状态）语义：X=0 表示未解决的重新考虑并禁止提交，但中性“无重新考虑”状态的合同定义不够明确。决策为 BOTH_RUNTIME_AND_AUDITOR_PATCH_JUSTIFIED，任务本身没有改 Candidate 或运行系统。[S08-09 取证](../../project/reviews/S08-09_RUNTIME_CONTRACT_ADHERENCE_FORENSICS.md)

如果只把所有 FAIL 当模型错误，可能不断追加提醒却不修模糊语法；如果只怪 parser，又可能掩盖工具回执确实不含新状态的执行违规。

**教学示例：** 某 marker 没被识别，先比对实际文本与当时合同，再看 parser 规则；某 observe 缺失，则看工具事件，不用模型叙述“我看过状态”代替回执。不同故障应使用不同权威来源。

### 为什么时间线还要有同一身份

两条日志时间相邻，只说明接近发生。它们是否同 session、同调用、同组件，决定能否拼成因果链。客户端退出在前、服务异常在后，也不自动证明客户端造成服务异常。

**事实：** v7m 取证保留 client/server 时间线限制，没有因异常名称猜测 WebSocket close code（关闭码）或主动关闭方；共享底层原因仍 UNKNOWN。[v7m 取证](../../project/reviews/S07-47_V7M_M20_PARTIAL_RUN_FORENSIC_REVIEW.md)

**解释：** 一个可信取证结论往往比最初猜测更窄。它可能只排除“查询立即终止运行”的强说法，仍不确定底层网络原因。这样的缩小足以避免错误 patch 与无界重试。

### 取证为什么还要保留原始来源

**Provenance（来源链）** 让派生结论能回到特定 Run、session、时间窗、版本与证据。hash（散列）帮助检验身份，不能替代文件；parser（解析器）生成摘要，不能自动成为比原始回执更强的事实。

**事实：** 当前有 20 个 named active/pending holds（具名活动/待决保留）：18 KEEP_ACTIVE，2 UNKNOWN_REVIEW_REQUIRED，0 releasable。HOLD_RELEASE_COUNT=0。结论写好不自动解除 FORENSIC_HOLD（取证保留）。[证据审查与台账](../../project/FINAL_EVIDENCE_REVIEW.md)

**解释：** 取证还原不了的部分，保留未知与最小必要来源，比选一个听起来合理的根因更有价值。它影响后续实验是否值得做、能否复核以及什么时候能清理。

证据文件和生命周期的工程实现，见 [Track C 证据链](../track-c-repository-tooling/07-artifacts、Raw-Evidence与证据链.md)。

取证缩小了可支持的结论，接下来要把结论写成准确的结果类型。技术失败、弱信号、未测试和可行性失败需要不同后续行动；一个笼统的“失败”会丢掉这些区别。

## 给结果分类，并保留停止理由

**Negative Result（负结果）** 是研究没有支持预期判断时留下的结果。它可以缩小搜索范围、阻止不安全部署、揭示比较方法的问题。前提是准确描述“哪件事没有得到支持”。

**解释：** “失败”若没有对象，会把未测量、技术故障、低分和可行性门禁混为一谈。下一位开发者可能因此重复无信息工作，或者错误关闭有价值方向。

前面的案例用来重建事实；这里继续区分结果类型。每条替代路线的测试深度与部署结论查 [D10](10-Reviewer、Memory、Helper、Controller与Simulator路线.md)。

### 六种标签有不同含义

| 类型 | 实际判断 | 真实项目例子 | 不能推出 |
|---|---|---|---|
| Unsupported improvement（未支持改进） | 没有足够证据确认收益 | 后期加固未形成稳定 75+ 突破 | 所有改动无价值 |
| Technical failure（技术失败） | 执行链在可比较结果前中断 | v7m M20 部分局 | 该 Candidate 会自然死亡 |
| Feasibility failure（可行性失败） | 后续研究必要前提不成立 | Simulator 基础胜任门禁失败 | 宏策略比较已失败 |
| Weak signal（弱信号） | 有观察，但不足以支持部署 | Controller / strategy mining | 方法逻辑完全无用 |
| Inconclusive（无法定论） | 不能区分关键解释 | v7m 连接根因 | 猜测的根因已成立 |
| Not tested（未测试） | 尚未执行相应研究 | Team / Swarm | 已测试而失败 |

**事实：** 表中路线与结论分别见 [实验复盘](../../project/EXPERIMENT_RETROSPECTIVE.md)、[v7m 取证](../../project/reviews/S07-47_V7M_M20_PARTIAL_RUN_FORENSIC_REVIEW.md)、[Simulator](../../project/research/S10-22_SIMULATOR_POLICY_SEARCH.md)、[Controller](../../project/research/S10-20_PROMOTION_WINDOW_CONTROLLER.md)。

这些是教学分类，不是一个所有项目通用、按优劣排列的结果等级。

### 为什么 Provider 错误不是策略失败

**事实：** v7i 的历史 Provider 异常发生在有效 HTTP 响应之前，且输出存在旧成绩风险。没有新局轨迹与正确分数绑定，不能用该报告评价策略。[Provider 取证](../../project/reviews/S07-39_PROVIDER_CONNECTIVITY_FORENSICS.md)

**解释：** 这类失败首先告诉你“本次运行没提供合格策略样本”。它仍然提供部署可靠性与归因风险信息。把它记成零分会制造一个未发生的游戏 outcome（结果）；把它静默删掉又会隐藏工程不可靠性。

MCP（模型上下文协议）注册失败也需要相同思路。注册/发现门禁失败时，尚未观察正式 Agent 的动作策略；不能说风险 Skill 已被游戏证明无效。项目早期加载与应用需要分开举证的合同，正是为了避免这种跳跃。[运行合同](../../project/AGENT_RUNTIME_CONTRACT.md)

### Schema rejection：拒绝发生在什么边界

**事实**：[v6 运行记录](../../project/runs/v6-run1-validation.md) 中一次 Energy 格式拒绝发生在状态改变前，另外 202 次成功动作有新观察。这里归为执行缺陷，不记成成功动作，也不直接评价某个 Skill 的策略收益。

参数形状与回执细节查 [B03](../track-b-system-runtime/03-Submission校验与Skill安装.md) / [请求与回执](../track-b-system-runtime/06-Runner、Tool调用与状态更新.md#一次选择怎样成为外部动作)。同一低分可能涉及多种原因，分类要绑定实际发生的边界。

### 自然低分不能自动变成技术失败

**事实：** v7q 记录 26.80 /18.76/24m/E/L1，属于自然 M24 终局；它与 v7m 没有最终成绩的技术部分局不同。[运行历史](../../project/RUN_HISTORY.md) · [最终证据审查](../../project/FINAL_EVIDENCE_REVIEW.md)

**解释：** 如果只接受高分为“有效”，低分都被改成“异常”，选择偏差会被流程制度化。自然低分可以提示策略风险，但不能单凭终局结果定位某一句规则为根因。

### Weak signal 为什么仍有价值

**事实**：[Controller 报告](../../project/research/S10-20_PROMOTION_WINDOW_CONTROLLER.md) 的工具状态持续性工作，24 个 replay cases 中仅一个 state-level correction、8 个 UNKNOWN，信号不足，未创建 v15。

**解释**：保存“状态机制可用、决策信号弱”比一个笼统 FAIL 更有定位价值；下次问题应针对语义缺口。完整协议与停止边界集中在 [D10](10-Reviewer、Memory、Helper、Controller与Simulator路线.md)。

### No deployment 不等于 idea worthless

**事实**：Helper 的 `DETERMINISTIC_HELPER_CHALLENGER_SUPPORTED` 仅支持 isolated tool-level，尚无正式 Candidate 部署；Reviewer/Memory 在各自冻结前提停止。三者不能都改写成“想法无价值”。[Helper](../../project/research/S10-19R3_NATIVE_CONTROL_SURFACE_AUDIT.md) · [Reviewer](../../project/research/S10-19R1_SUBAGENT_FEASIBILITY.md) · [Memory](../../project/research/S10-19R2_MEMORY_FEASIBILITY.md)

这里的分类区分“有限支持但未部署”和“当前路径前提失败”；各路线详见 [D10](10-Reviewer、Memory、Helper、Controller与Simulator路线.md)。

### 失败记录应保存什么

记录问题、身份、实际门禁、证据、决策和非结论，条件阶段未执行则明确留下。Reviewer Phase B/C 与 Simulator holdout 未运行，不能记成收益失败。技术失败要可见，也不能与自然终局强行合算均分；保存知识不解除 raw/hold。

### 为什么“没测量”不能记成零

**事实**：[Reviewer](../../project/research/S10-19R1_SUBAGENT_FEASIBILITY.md) 未进入建议阶段，latency/token/成功率为 NOT_MEASURED；零 invocations 是调用次数，不是实测耗时零。

**解释**：0 次、无分、分数 0 是计数、缺失、数值三个对象；没有 usage 不等于零成本。门禁阻断不能提供能力成功率。

### 负结果怎样影响下一次授权

重开要指出新的 material evidence（实质证据）及它改变的前提：安全部署、语义排序或连接机制。**教学示例**：新的机械隔离 reviewer loader 需要独立验证，不能从旧 frozen-path 结果认定它必然成功或失败。单纯“再试可能成功”不回答旧门禁。

### 怎样读一个负结果

先找 decision token（决策标记），再看测试对象与前提。接着检查实际执行阶段、未测量能力和 stop rule（停止规则）。最后问：未来若重新打开路线，需要哪个新的 material evidence（实质证据）？

**教学示例：** 对 Memory，要同时保留指定自动锚点未过门禁与 explicit read 成功。完整原因和范围查 D10；结果标签不能省略测试对象。

项目保存失败，是为了让决策可复核。保存失败知识与永远保留全部过程文件仍是两件事；后续精简需遵循 [Track C 保留原则](../track-c-repository-tooling/11-开发工作流与文件生命周期.md#交付之后材料怎样保留或退役)，本轮不执行清理。
