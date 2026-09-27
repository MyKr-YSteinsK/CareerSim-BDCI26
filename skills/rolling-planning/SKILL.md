---
name: rolling-planning
description: "每次决策必须应用；唯一 strategy owner。维护一个稳定的 review-window 计划，用公开证据做短而有界的候选比较；不提交动作。"
---

# Rolling Planning｜Lean Review Controller

## 1. 职责与证据边界

Planning 是唯一 strategy owner。只使用当前 game_session 的 fresh participant-visible public facts、Board 可核实事实、Delivery compact summary、合法选项、公开回执/日志与 Handbook。

禁止使用或推断：

- hidden threshold / hidden cap / hidden score weight / hidden formula；
- event/title/keyword→固定答案；
- 其它对局结果；
- Dev/private/internal evidence；
- “某个公开提示 = 已确认 simulator hard rule”。

公开人物或事件文本中的提示可以作为 **public hint**，但只能表示“有人公开这样说过”，不能升级为已确认机制。

Can Submit Action: No。

---

## 2. Active Review Plan｜唯一稳定策略状态

Planning 只维护：

`Review Objective / Primary Gap / Next Observable Checkpoint`

### Review Objective

当前 review window 内最重要的可验证职业目标。

### Primary Gap

当前公开证据下，最限制稳健 progression 的一个主要瓶颈；可为 `UNKNOWN`。

### Next Observable Checkpoint

下一条足以判断计划推进、完成或失效的公开证据，例如：

- formal review / performance feedback；
- promotion / no-advance；
- Delivery receipt / blocker result；
- 明确、可归因的 public outcome。

**普通 Story 不得改变 Primary Gap。**

QUICK 决策默认保留整个 Active Review Plan。

只有以下 fresh material evidence 才允许 FULL revision：

1. formal review / promotion / no-advance；
2. binding survival/resource constraint 明显改变；
3. Objective 已公开完成；
4. 当前路径被 fresh public result 明确失效；
5. repeated comparable observed miss 已足以说明当前路径没有推进目标。

FULL trigger 不等于必须换计划；证据不足则保留。

---

## 3. Decision Order｜每步只走一次

每次决策按以下顺序：

### A. Freshness / legality

确认当前 state、event、choices 属于同一 fresh session。来源不清标 `UNKNOWN`，不猜。

### B. Binding survival/resource constraints

优先检查：

- Health
- Dignity
- Wealth / affordability
- explicit compliance/confidentiality/safety warning
- formal performance warning
- credible public consequence

若存在 binding constraint：

> 先避免可避免地继续恶化该约束，再比较 progression。

### Affordability Guard

以下任一情况都把 affordability 视为 binding：

- Wealth 已非正；
- Wealth 持续耗尽且接近非正；
- fresh public debt / payment / poverty / affordability warning；
- 公开结果表明当前收入能力不足以覆盖持续成本。

这不是 simulator failure-threshold 推断。

当 affordability binding：

- 避免非必要、公开可见的 Wealth 成本；
- 不为了轻微 Network / Story 好感承担明显资源成本；
- 优先保护 job continuity；
- promotion / Level progression 同时具有 career 与 future-income value；
- 必要的健康/合规处理仍可优先，不能为了省钱承担更大的生存或合规风险。

不得推断“连续几个月”或某个具体 Wealth 数字就是隐藏终局阈值。

### C. Active Review Plan

**Formal review / promotion feedback 是 progression 的最高优先级 public evidence。**

如果正式反馈明确指出：

- 产出不足；
- 关系/协作不足；
- 技术能力不足；
- 风险/可靠性问题；
- 其它具体短板；

则该反馈优先于：

- 某个普通 Story 的诱导；
- “最低 stat”猜测；
- 某人一句关于隐藏机制的提示；
- 对未观察机制的脑补。

no-advance / poor review 表示当前 review plan 没有充分兑现；下一窗口默认围绕正式反馈形成可见结果，而不是每个 Story 重新定义战略。

### D. Candidate fit

优先选择：

1. 解除 binding constraint；
2. 推进当前 Review Objective / Primary Gap；
3. 把 active commitment 推到 delivery / observable evidence；
4. 在长 horizon 下形成清晰 compounding value。

已有高价值 commitment 接近兑现、而新机会需要额外负荷且不能明显更好时，优先完成和证明已有工作。

**公开写明会显著增加 workload / 降低当前产出 / 恶化健康时，不得仅因 speculative promotion hint 就强行追加 commitment。**

### E. Near-tie semantic priors

只有候选仍接近时才使用：

- 事实优先；
- 普通摩擦优先直接、清晰、可执行处理；
- 保密/合规遵守 need-to-know；
- 可逆/分阶段优于不可逆的大赌注；
- escalation 与公开 severity 相称。

这些只是 tie-breaker，不得覆盖 A–D。

### F. Candidate-specific Risk gate

Planning 完成排序后，把最终候选交给 Risk Skill。

Risk gate 后进入 `DECISION_CLOSED`。

无 fresh evidence 时不得重新打开同一个决策。

---

## 4. Bounded Deliberation｜禁止反复重想

普通 Story：

1. 先淘汰明显支配劣势候选；
2. 最多深入比较剩余 top 2；
3. 一次形成结论；
4. 交 Risk gate；
5. 提交并停止。

禁止：

- 连续 “let me reconsider / hmm” 循环；
- 选定候选后又反复重排同一批信息；
- 为证明自己更谨慎而重复分析；
- 因普通 uncertainty 启动额外 handbook / log / observe。

只有 **新 fresh public evidence** 才允许重新打开。

---

## 5. Public Hint ≠ Hidden Mechanic

公开事件可以说：

- “某项可能影响绩效”；
- “领导暗示某项重要”；
- “某行动广告会增加某状态”。

这些都可以用于当前候选比较，但不得转换成：

- confirmed hard indicator；
- hidden promotion threshold；
- hidden cap；
- fixed optimal route。

例如：

> “Leader 暗示带新人有利于绩效”

只能记为：

`public hint supporting mentoring value`

不能记为：

`mentoring is a confirmed hard requirement for grade A`

若该 hint 与当前 Health、Output、Wealth、formal feedback 或 commitment load 冲突，以更直接、更新鲜、可验证的 public evidence 为先。

---

## 6. Observed Effect Discipline

Advertised effect 只是先验。

fresh observed result 可以更新该路径的局部价值，但：

**不得从一次或几次未增长推断 hidden cap / threshold / formula。**

正确处理：

- 记录 `OBSERVED_GAIN / OBSERVED_NO_GAIN / OBSERVED_COST / UNKNOWN`；
- observed downside + no target progress → 立即降低该路径的相对价值；
- repeated comparable miss → 在有新支持证据前不要机械重复；
- 原因保持 `UNKNOWN`，除非 public evidence 明确解释。

禁止：

- “Network=3 所以 L1 cap=3”；
- “Output 不增长所以已封顶”；
- “Skill=9 是隐藏上限”。

---

## 7. Review-window Control

正式 review / promotion/no-advance 后执行 FULL checkpoint：

`Horizon | Promotion Frontier | Active Review Plan | Progress/Recent Effect | Risk Budget | Path Trade-off`

重点回答：

- 正式反馈到底说了什么？
- 哪个公开结果最能改变下一次 review？
- 当前 constraint 是否会让这个计划不可持续？
- 已有 commitment 是否应先兑现？

接近已知 review 的最后可行动窗口时：

> 优先把现有工作转换为 visible delivery / evidence / recognition，同时保住 survival/resource floor。

不得固定成“review 前必汇报”或某个菜单答案。

---

## 8. Quarterly Energy / Main Action

季度首次 Energy 决策：

先基于同一个 Active Review Plan 一次性形成本季度的 Energy intent。

之后每次 Energy 仍只提交 **一个整数 choice**，并 fresh observe。

若 fresh observe 没有 material change：

> 不重新规划整套 Energy allocation。

只有 binding constraint / fresh material outcome 改变时才调整剩余 Energy intent。

主行动继续服务同一个 Active Review Plan。

不得因为 advertised gain 未出现就推断 hidden cap。

---

## 9. Marker Semantics

`P` 明确定义为：

- `P=A`：Advance / progression path；
- `P=S`：Stabilize / survival-resource path；
- `P=?`：纯 administrative / 无战略归类。

`G` 必须对应当前 Active Review Plan 的 Primary Gap。

普通 Story 不得为了描述局部事件而临时改 `G`。

---

## 10. Recovery

context recovery 时：

1. 确认同一 game_session_id；
2. fresh observe；
3. 重读四 Skills；
4. Board 重建 fresh public facts；
5. Delivery 只用当前 session public evidence 重建相关 lifecycle；
6. Planning 恢复或重建 Active Review Plan；
7. 无法恢复的内容标 `UNKNOWN`。

旧 snapshot / intention 不具有事实或 receipt 权威。

---

## 11. Anti-overfit / Ownership

- Single Agent 唯一 action submitter。
- Planning 不调用 new_game / observe / take_action。
- Board 只拥有 public facts。
- Delivery 只拥有 current-session bounded lifecycle。
- Risk 只拥有 candidate-specific Material Risk gate。
- Planning 不 create / overwrite / complete Delivery state。
- Memory=NOT_IMPLEMENTED。
- fifth Skill=DEFERRED。
- Team/Swarm=DEFERRED。
- 不使用固定 promotion month、固定 action bundle、固定 capital ratio、固定 Story answer、hidden cap/threshold/weight。
