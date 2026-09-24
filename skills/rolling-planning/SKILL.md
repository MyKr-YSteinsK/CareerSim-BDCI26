---
name: rolling-planning
description: 每季度首次 `Energy` 决策前，依据新鲜公开证据更新或建立 `Planning checkpoint`；仅在初始详细规划、重大反馈/后果、上下文恢复或 checkpoint 不可靠时重读本 Skill。比较重复动作的 `observed effect`，使用有界 `Risk Budget` 与公开 48 个月 horizon；只提出建议，不提交动作。
---

# Rolling Planning｜滚动规划

## 职责

依据新鲜公开证据确定短期优先项和中期目标；本 Skill 不是 Agent、动作政策、Memory 系统或分数预测器。

## 使用时机

- 新局首次有效观察后，读取本 Skill 完成详细初始规划并设定初始优先项。
- 每季度第一次 Energy 决策前，使用新鲜公开状态刷新或建立该季度 checkpoint。仅进入新季度不要求全文重读本 Skill。
- 同季度主行动复用该 checkpoint，除非有重要反馈或重要公开状态变化。
- 半年反馈、严重公开警告/后果、continuation/context loss、checkpoint 语义过期或含糊、或无法可靠还原详细流程时，重读本 Skill 并基于新鲜公开观察重建。

不要为每个月的普通故事事件调用本 Skill。HR 表扬、没有新警告、动作已被接受或已提交的缓解措施，本身都不代表风险已解除，也不触发重大目标重排。没有重大风险时，正常成长选择不需要额外 Risk review 或默认保守处理。

## 输入与证据规则

只使用已确认的当前游戏 session、最新权威公开 `observe`、同局状态板（如有）、已确认动作回执和可用的公开 Handbook 规则。区分 observed、inferred 与 unknown。

不得使用其他局、当时尚不可见的局后事实、原始数据库、隐藏计数/阈值或 evaluator weights。动作先后顺序本身不能证明因果。

## 规划流程

1. 每季度第一次 Energy 决策前，先从新鲜公开 `observe` 刷新或建立 checkpoint，再选择 Energy。单是进入新季度或缺少当季 checkpoint，不要求重读本 Skill。同季度主行动复用该 checkpoint，除非反馈/状态有重大变化；按上文条件决定是否重读。
2. 只使用已确认的当前游戏 session 和新鲜状态板/`observe`。continuation/context loss 后先确认游戏 session，再依据新鲜公开状态重建；无法验证的旧目标进展记为 `UNKNOWN`。不得从 Memory 或猜测中继承。
3. 始终只维护一个 `Primary Gap`：公开的职业/资源差距，或有证据支持的晋升停滞。不得默认均衡发展或套固定优先级。设定一个可观察目标，供下一季度/半年度复核；不得承诺晋升、分数或事件结果。季度 Energy 决策时，比较合法选项对该 Gap 的边际公开收益与 Energy/机会成本。某一维度饱和既不能证明也不能否定组合选项的价值。
4. 在战略 checkpoint 上，根据可比的新鲜公开证据，将上一目标进展标为 `ADVANCING`、`STALLED` 或 `UNKNOWN`。只有 `Primary Gap` 本身可观察改善，或有与该 Gap 明确相关的直接公开绩效/晋升进展证据，才是 `ADVANCING`。表扬、协作 bonus、普通正面反馈、关系改善或单次成功事件只能作为辅助信号，不能单独确立 `ADVANCING`。缺少直接且可比的 Gap 证据时记为 `UNKNOWN`，除非第 5 条已满足 `STALLED`。分析重复动作时，将菜单 advertised effect 视为假设；优先采用可靠的同局 observed effect。归因含糊、存在中间原因或缺少比较时记为 `UNKNOWN`。
5. 只有同一 action 针对同一 Gap，在两个相邻且可比的 checkpoint 均未观察到进展，才标记 `STALLED`。随后必须比较至少一个不同类型的合法 alternative 及其公开收益/机会成本。一次未见进展不强制切换；必须比较，但不强制选择 alternative。若 Gap 已变化，或旧 action 对新 Gap 仍有可靠收益，可以继续，并明确说明理由。
6. `Risk Budget`：出现新鲜的重大 Health/信任/合规/报复/生存风险时为 `TIGHT`；没有新鲜重大警告且公开状态显示相关安全余量时才可为 `AVAILABLE`；否则为 `UNKNOWN`。安全是约束，不是默认目标。普通软成本（少量 Health/Dignity 损失、时间、摩擦、压力）是机会成本，不能自动否决高收益成长路径。比较公开收益、风险与成本，不编造阈值。
7. 普通选择严格按以下定性顺序比较合法选项：`Material Risk` gate → 对当前 `Primary Gap` 的贡献 → 有用的次级公开收益 → `Soft Cost` / 机会成本 → 尚未消除的 `UNKNOWN`。不得默认选择最成熟、最安全或最不得罪人的方案，也不得设置固定权重或数值评分。当 `Risk Budget = AVAILABLE`、没有新鲜 `Material Risk`、某条合法路径对 `Primary Gap` 有明显更强的公开证据收益，且额外代价主要是 `Soft Cost` 时，优先该高收益路径。Gap 收益相近或为 `UNKNOWN` 时，可选择成本/暴露更低的路径。`TIGHT` 时重大风险可以压过成长收益；当前候选的风险审查仍由 `risk-review` 负责。
8. 只使用公开的当前月份与 48-month horizon。随着剩余时间缩短，若 Gap 仍停滞，应优先考虑能产生可观察进展的合法路径，而不是只有遥远/不确定回报的路径。不得推断具体晋升月份或隐藏阈值。
9. 对普通、非战略故事选择，最多比较两个最强合法候选一次；没有新鲜证据时，只有出现新的公开证据或 `risk-review=RECONSIDER` 才重新开启比较。
10. 严重警告/后果、持续报复/升级，或重大生存/信任成本威胁目标时，重新审查 `Primary Gap`。按公开收益/损失、暴露、成本与 `UNKNOWN` 比较合法的继续、降级冲突、调动/退出/缓解路径，并注明不可用选项。原则、职责或近期晋升都不能证明安全；保守或降低暴露的选项也不是固定答案。最终由同一个 Agent 决定。

## 输出

输出不超过六条简短 checkpoint：

```text
Horizon:
Primary Gap:
Progress:
Recent Effect:
Risk Budget:
Path Trade-off:
```

- `Horizon`: 公开当前月份 / 48-month horizon 及下一复核点。
- `Primary Gap`: 恰好一个可调整、基于公开证据的目标。
- `Progress`: `ADVANCING`、`STALLED` 或 `UNKNOWN`，并说明可比证据依据。
- `Recent Effect`: 可靠的同局 observed effect；否则 `UNKNOWN`。
- `Risk Budget`: `TIGHT`、`AVAILABLE` 或 `UNKNOWN`。
- `Path Trade-off`: 最多两个合法路径；相关时列出边际收益与机会成本。

若当前没有相关合法选项，注明不可用并等待正常决策点，不得虚构选项。

## 动作权限与回退

- **Can Submit Action: No（不得提交动作）。**
- 不调用 `new_game`、`observe` 或 `take_action`，也不修改合法选项或动作记录。
- 只有 Single Agent 提交动作；它可以调整或拒绝本建议。
- session、状态或选项过期/含糊时，报告不确定性并回到正常流程获取新鲜公开状态。不得猜游戏 ID，也不得阻断正常决策。
- checkpoint 只保留在当前 drive conversation，并限定于当前游戏 session。不得写入文件、全局 Memory、Skill 状态、Runner 输出或模拟器数据，也不得带入另一局。
