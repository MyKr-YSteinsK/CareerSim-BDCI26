---
name: rolling-planning
description: 唯一战略规划 Skill；以新鲜公开证据维护一个 Primary Gap、比较观察进展与路径，并向 Single Agent 提供有界建议，不提交动作。
---

# Rolling Planning｜滚动规划

## 职责与使用时机

`rolling-planning` 是唯一战略规划 owner；它提供可调整的目标与路径比较，不是动作政策、Memory 或分数预测器。只使用当前 session 的 fresh public evidence、Board 中可核实的事实和公开 Handbook；不得使用其他局、隐藏阈值、evaluator weights 或局后信息。

完整读取本 Skill：新局初始规划时；上下文丢失后详细流程无法可靠恢复时；checkpoint 过期/含糊时；或重大公开反馈/后果改变了战略框架时。每季度首次 `Energy` 决策前，先基于 fresh observe 更新 Board 并刷新 checkpoint；新季度或半年反馈本身不要求全文重读。同季度主行动复用 checkpoint，除非有重大状态变化。普通月度故事不调用本 Skill。

重大公开后果触发时，当前候选先按需进入 `risk-review`；仅当该后果改变战略才重建 Planning。context loss 时确认同一 session、取得 fresh observe、必要时用 Board 的有界恢复事实重建。

## 规划规则

1. 每个 checkpoint 只维护一个公开、可观察的 `Primary Gap`，也可为有公开依据的职业进展停滞。不得默认均衡发展、固定优先级或设隐藏目标。
   已明显充足、饱和或与当前 Gap 无关的单一维度，不应因惯性继续作为默认投入目标；但不能因此单独否决仍对 Gap 有有效收益的组合选项。
2. 标记 `Progress = ADVANCING / STALLED / UNKNOWN`。只有 Gap 本身改善或有直接关联的公开职业进展，才算 `ADVANCING`；表扬、一般正面反馈或选项说明本身不够。证据不可比或归因不清时为 `UNKNOWN`。
3. 菜单 `advertised effect` 是待验证信息。重复战略动作评估优先采用同一 session 中可靠、可比的 `observed effect`。只有同一 action 针对同一 Gap，在两个相邻可比 checkpoint 均未见进展，才标为 `STALLED`。随后必须比较至少一个不同类型的合法 alternative；不强制切换。一次无进展不触发强制切换。Gap 改变或该动作对新 Gap 有可靠观察收益时可以继续，并说明依据。
4. `Risk Budget = TIGHT / AVAILABLE / UNKNOWN`：新鲜公开 Material Risk 表示 `TIGHT`；没有新鲜重大警告且公开状态显示相关安全余量时才可为 `AVAILABLE`；否则 `UNKNOWN`。安全是约束，不是默认优化目标。Soft Cost 是机会成本，不能单独自动否决明显更有利于当前 Gap 的成长路径。Risk Skill 仅审查当前候选的明确重大风险。
5. 普通路径按定性顺序比较：`Material Risk` → 当前 Gap 的公开贡献 → 有用的次级公开收益 → `Soft Cost` / opportunity cost → `UNKNOWN`。不设固定数值权重；“成熟、圆滑、体面、稳妥”本身不构成收益。Risk Budget 为 `AVAILABLE`、无新鲜 Material Risk，且某合法路径对 Gap 的公开收益明显更强时，不因普通成本或更稳妥叙事自动放弃。
6. 只用公开当前月份和 48-month horizon。剩余时间缩短且 Gap 停滞时，重新比较能带来当前可观察进展的路径与仅有远期/不确定收益的路径；不预测晋升月份或隐藏阈值。
7. 普通非战略事件最多比较两个最强合法候选一次；不复述已知状态、规则或已完成比较。没有 fresh evidence 时不重开，除非 `risk-review=RECONSIDER`。

## 输出与权限

需要建立/刷新 checkpoint 时，最多输出六行：

```text
Horizon:
Primary Gap:
Progress:
Recent Effect:
Risk Budget:
Path Trade-off:
```

`Recent Effect` 无可靠比较时为 `UNKNOWN`；`Path Trade-off` 最多两个合法路径。不要复制完整 Board 或 transcript。选项不可用时如实说明。

- Can Submit Action: No。最终决定与唯一动作提交权属于 Single Agent。
- 不调用 `new_game`、`observe` 或 `take_action`，不建立文件型 Memory，不跨 session 沿用 checkpoint。
- session、状态或选项不新鲜时保留 `UNKNOWN`，回正常流程取得新鲜公开信息。
