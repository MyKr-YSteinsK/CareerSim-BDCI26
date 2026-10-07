# 08｜Forensics 为什么成为项目的重要部分

**Forensics（取证分析）** 根据原始或结构化记录重建“实际发生了什么”。它尤其适合结果和运行链不一致的情况：分数属于谁？工具回执有没有新状态？模型有没有恢复？一个审计 FAIL 是真实违规还是解析器误解？

**INTERPRETATION｜解释：** 取证的价值是缩小可支持的结论范围。它既可以确认问题，也可以证明某个常见解释没有足够证据。UNKNOWN 不是取证失败的同义词。

本章只使用 canonical summaries（权威摘要）与已去敏研究记录，不展开 raw payload（原始载荷），也不重新进行 live 诊断。

## 1. Stale score：文件里有分数，不代表属于这次运行

**表面现象：** v7i 故障尝试仍输出了 score report。

**可能解释：** 新局已发生但没有记录；报告查询了旧 session；文本中的历史 session 被当成当前身份。

**需要证据：** fresh new_game/observe 的 session，报告 session，Runner 提取身份的代码路径。

**FACT｜实际查到：** S07-38 的报告 session 属于此前 v7g。Runner 除了结构化结果，还可从 transcript（运行文本）中的 SESSION_ID 提取身份；在缺少新结构化身份时存在 stale-score hazard（过期成绩风险）。[S07-39 取证](../../project/reviews/S07-39_PROVIDER_CONNECTIVITY_FORENSICS.md)

**可下结论：** 该分数不是 v7i 新局成绩，必须排除。**仍不能下结论：** 输出报告文件不证明 v7i 达到同等表现，也不证明新的 session 已存在。

## 2. Provider failure：今天可连接，不解释昨天为什么失败

**表面现象：** 模型流连接错误，Runner 无法继续。

**可能解释：** DNS、TLS、代理、服务端或更低层连接问题。异常名字未必区分它们。

**需要证据：** 当时异常链、是否收到 HTTP response（HTTP 响应）、时间窗和后续诊断的时点。

**FACT｜实际查到：** 历史链为连接异常，在 HTTP 响应之前失败，没有状态码或可定根因的低层信息。后续 DNS/TCP/TLS 与一次 metadata request（元数据请求）通过，只证明那次诊断时当前路径可达。[S07-39 取证](../../project/reviews/S07-39_PROVIDER_CONNECTIVITY_FORENSICS.md)

**可下结论：** 当前连通性具备另行审查替代运行的条件。**仍不能下结论：** 历史故障一定由 DNS 或代理造成；诊断通过自动授权新局。本轮没有重做任何网络或 Provider 检查。

## 3. Session provenance：缺字段不等于身份完全不可恢复

**表面现象：** v7i replacement 的 score_report 有 session-field defect（会话字段缺陷）。

**可能解释：** 成绩错配，报告格式缺陷，或者源事件能够独立绑定同一运行。

**需要证据：** fresh session、事件序列、成绩来源和 Main re-audit（复审），不能只依靠输出目录名。

**FACT｜实际查到：** replacement 记录经 Main 原始证据复审接受了 64.0 /44.8/48m/B，同时保留报告 session 字段缺陷。[替代运行记录](../../project/runs/v7i-run1-replacement-validation.md)

**可下结论：** 在已接受的来源链范围内归属这条成绩。**仍不能下结论：** 所有空 session 报告都可信。这个案例与 stale score 必须一起理解：不能一律接受，也不能一律否定，要看独立绑定证据。

## 4. v7m：时间相邻不等于因果机制

**表面现象：** 运行在 M20 技术退出，用户曾进行进度查询。

**可能解释：** 查询影响连接；模型流与本地连接受共同原因影响；某个未记录组件异常。

**需要证据：** 最后 fresh observe、动作回执、客户端与服务日志时间线，以及查询是否有写入或调用路径。

**FACT｜实际查到：** 84/84 动作成功，85 次 unique observes（唯一观察），最后 fresh M20 仍 alive（存活）。客户端接收异常先可见，后续有模型流中断；只读 stdout 查询没有直接写入/调用机制，且查询之后运行仍推进到 M20。根因分类 INSUFFICIENT_EVIDENCE（证据不足）。[v7m 取证](../../project/reviews/S07-47_V7M_M20_PARTIAL_RUN_FORENSIC_REVIEW.md)

**可下结论：** 有价值的 PARTIAL_GAMEPLAY_TECHNICAL_FAILURE（对局技术部分失败），查询导致终止的因果判断不获支持。**仍不能下结论：** 确认某网络根因、预测最终成绩，或把 M20 partial 写成完整月末。

## 5. Fresh state：成功回执不等于状态观察

**表面现象：** 审计发现一些连续动作之间缺少 observe，但动作都成功。

**可能解释：** take_action 已返回新状态；Agent 使用旧状态；审计遗漏了观察。

**需要证据：** 实际 tool result（工具结果）字段、接口模型和动作/观察序列。

**FACT｜实际查到：** S08-RUN03 的 action 回执只有 success/error，不含 public state、event 或 choices。18 个缺 observe 边界是真实违规，不是回执等价观察。[S08-09 取证](../../project/reviews/S08-09_RUNTIME_CONTRACT_ADHERENCE_FORENSICS.md)

**可下结论：** 执行链没有遵守每次成功动作后的 fresh observe 合同，runtime 与 auditor 均有修正依据。**仍不能下结论：** 哪一个缺观察导致了多少分数损失。

## 6. Compression：恢复文字不是来源重读

**表面现象：** 压缩后仍能看到状态和规则摘要。

**可能解释：** 完整合同已恢复；只保留压缩摘要；事实恢复与 Skill 来源读取是两种不同事件。

**需要证据：** compressor epoch（压缩时期）与 read_file（读文件）序列、新观察、原合同和后续 recovery 定义的时间关系。

**FACT｜实际查到：** v6 有两次压缩时期，没有在任一之后重读 Skill。运行记录以 S06-25 恢复定义解释这个缺口；后续 v6b 合同更明确要求恢复重读。[v6 记录](../../project/runs/v6-run1-validation.md) · [S06 收口](../../project/S06_CLOSEOUT.md)

**可下结论：** 重读事件没有发生，不能把 reinjected state text（重新注入的状态文字）当成已重读来源。**仍不能下结论：** 所有后续错误都是压缩造成，或再次增加提示一定解决恢复。

## 7. CTRL/action：文字数量不能充当唯一动作映射

**表面现象：** CTRL 标记数量很多，看起来足以覆盖动作。

**可能解释：** 每动作都有标记；delta/event 重复表现；一个模型回合多次出现同类文本。

**需要证据：** tool_call_id（工具调用 ID）、可靠 model-turn ID（模型回合 ID）、事件去重规则和绑定语义。

**FACT｜实际查到：** v6 有 418 个 marker-shaped occurrences（形似标记的出现位置），对应 203 次动作尝试；来源缺少可靠模型回合绑定，无法据文字计数认证一一配对。v7m 原始事件的多种表示也需要按 kind/tool_call_id 去重。[v6 记录](../../project/runs/v6-run1-validation.md) · [v7m 取证](../../project/reviews/S07-47_V7M_M20_PARTIAL_RUN_FORENSIC_REVIEW.md)

**可下结论：** 审计可配对性存在限制。**仍不能下结论：** 标记很多证明全覆盖，或者精确判定每个动作都缺失了多少标记。

## 8. Hidden evidence：分析者能看见，不代表玩家能使用

**表面现象：** raw 或运行文本包含内部 HiddenRisk 数值引用。

**可能解释：** 内部信息混入公开策略输出；审计记录包含分析用字段；参赛者输入边界被误认。

**需要证据：** participant-visible（参赛者可见）输入定义、引用发生的位置、来源与审计限定。

**FACT｜实际查到：** v8a 两个样本分别保留 HiddenRisk 数值引用限制，不能把内部数值作为可部署策略知识；这些限制也不能直接解释两局分差。[样本一](../../project/runs/v8a-full-horizon-sample1.md) · [样本二](../../project/runs/v8a-full-horizon-sample2.md)

**可下结论：** 公开/隐藏信息边界需要审查。**仍不能下结论：** 把隐藏阈值写入教材规则，或声称内部引用带来了确定分数收益。

## 同一 parser 的 FAIL，怎样区分工具问题与行为问题

**INTERPRETATION｜解释：** 审计器是一段带假设的程序，不是自动拥有全部语义的裁判。FAIL 可能来自真实违规、格式合同不明确、解析规则过窄或证据不足。把这几类分开，才能决定改 Candidate、改 parser，还是保留 unknown。

**FACT｜事实：** S08-09 在确认缺 observe 为真实违规之外，还检查 CTRL closure（控制标记关闭状态）语义：X=0 表示未解决的重新考虑并禁止提交，但中性“无重新考虑”状态的合同定义不够明确。决策为 BOTH_RUNTIME_AND_AUDITOR_PATCH_JUSTIFIED，任务本身没有改 Candidate 或运行系统。[S08-09 取证](../../project/reviews/S08-09_RUNTIME_CONTRACT_ADHERENCE_FORENSICS.md)

如果只把所有 FAIL 当模型错误，可能不断追加提醒却不修模糊语法；如果只怪 parser，又可能掩盖工具回执确实不含新状态的执行违规。

**TEACHING EXAMPLE｜教学示例：** 某 marker 没被识别，先比对实际文本与当时合同，再看 parser 规则；某 observe 缺失，则看工具事件，不用模型叙述“我看过状态”代替回执。不同故障应使用不同权威来源。

## 为什么时间线还要有同一身份

两条日志时间相邻，只说明接近发生。它们是否同 session、同调用、同组件，决定能否拼成因果链。客户端退出在前、服务异常在后，也不自动证明客户端造成服务异常。

**FACT｜事实：** v7m 取证保留 client/server 时间线限制，没有因异常名称猜测 WebSocket close code（关闭码）或主动关闭方；共享底层原因仍 UNKNOWN。[v7m 取证](../../project/reviews/S07-47_V7M_M20_PARTIAL_RUN_FORENSIC_REVIEW.md)

**INTERPRETATION｜解释：** 一个可信取证结论往往比最初猜测更窄。它可能只排除“查询立即终止运行”的强说法，仍不确定底层网络原因。这样的缩小足以避免错误 patch 与无界重试。

## 取证为什么还要保留原始来源

**Provenance（来源链）** 让派生结论能回到特定 Run、session、时间窗、版本与证据。hash（散列）帮助检验身份，不能替代文件；parser（解析器）生成摘要，不能自动成为比原始回执更强的事实。

**FACT｜事实：** 当前有 20 个 named active/pending holds（具名活动/待决保留）：18 KEEP_ACTIVE，2 UNKNOWN_REVIEW_REQUIRED，0 releasable。HOLD_RELEASE_COUNT=0。结论写好不自动解除 FORENSIC_HOLD（取证保留）。[证据审查与台账](../../project/FINAL_EVIDENCE_REVIEW.md)

**INTERPRETATION｜解释：** 取证还原不了的部分，保留未知与最小必要来源，比选一个听起来合理的根因更有价值。它影响后续实验是否值得做、能否复核以及什么时候能清理。

证据文件和生命周期的工程实现，见 [Track C 证据链](../track-c-repository-tooling/07-artifacts、Raw-Evidence与证据链.md)。

---

[学习地图](00-学习地图.md) | [上一章](07-为什么一次高分几乎什么都证明不了.md) | [下一章](09-失败实验与负结果为什么值得保留.md)
