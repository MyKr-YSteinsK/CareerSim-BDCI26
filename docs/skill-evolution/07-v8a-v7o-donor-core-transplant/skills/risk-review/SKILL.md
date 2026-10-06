---
name: risk-review
description: "Use immediately before every take_action on Planning's final candidate. 只对最终候选执行风险 gate：普通成长成本直接 PASS；只有 fresh public evidence 显示重大生存、工作连续性、信任、合规、保密、安全或已 binding 的资源风险时做 Full Review；不得重新规划整局。"
---

# Risk Review｜最终候选风险门禁

## 职责

本 Skill 只审核 Planning 已选出的最终合法 `CANDIDATE`。

不拥有 `REVIEW_PLAN`，不拥有 `Primary Gap`，不重新做 candidate ranking。

输入：

- Planning final `CANDIDATE`；
- fresh Board；
- 当前 `MODE`；
- 候选的 participant-visible consequences。

只使用 current-session public evidence。

禁止使用 `HiddenRisk`、hidden counters、internal score、internal event id/effect、public-status-unclear numeric fields。

## 输出

严格输出：

```text
RISK: PASS|ALLOW|WARN|RECONSIDER|UNKNOWN
REASON: <one concise public-evidence reason>
```

## Quick Gate

如果候选只包含普通：

- workload；
- 小幅 Health / Dignity cost；
- relationship friction；
- uncertainty；
- opportunity cost；

且 fresh public evidence 没有把这些成本升级为 material risk，返回：

`PASS`

不要仅因为另一个选项更安全就拦截高价值成长路径。

## Full Review

候选直接涉及以下重大公开风险时才执行 Full Review：

- acute physical symptom / psychological danger；
- material safety warning；
- explicit job-continuity / dismissal danger；
- trust crisis / credible retaliation；
- compliance / confidentiality；
- explicit affordability pressure；
- 会直接恶化当前 `MODE=S` binding constraint 的行为。

Wealth 紧张时区分 discretionary spending 与 performance/promotion/income recovery；不要仅因 Wealth 低就否决直接支持绩效、晋升或工作连续性的动作。

## Result

- `ALLOW`：重大风险已审查，候选仍可接受。
- `WARN`：存在重大 concern，但现有证据不足以要求换选。
- `RECONSIDER`：重大风险明确；当前候选未处理；当前合法选项中存在一个直接相关替代项。只允许 Planning 比较这个替代项一次。
- `UNKNOWN`：关键公开证据过期、缺失或来源不清。

Full Review 后不得返回 `PASS`；使用 `ALLOW / WARN / RECONSIDER / UNKNOWN`。

`RECONSIDER` 之后：

1. Planning 最多比较一个直接相关替代项；
2. 选定后，该候选必须重新经过 Risk；
3. 最终 CTRL `R` 记录提交候选的最终 `PASS|ALLOW|WARN|UNKNOWN`；
4. CTRL v2 使用 `[CTRL G=<gap|?> P=<A|S|?> R=<PASS|ALLOW|WARN|RECONSIDER|UNKNOWN> RB=<NONE|DONE|BLOCKED>]`；`R` 是最终候选的 Risk 结果。
5. 初次 Risk 非 `RECONSIDER` 且无 reconsideration branch 时记 `RB=NONE`；一次 bounded branch 完成且最终 Risk 不为 `RECONSIDER` 时记 `RB=DONE`。
6. 最终 Risk 仍为 `RECONSIDER` 或分支/门禁无法闭合时记 `RB=BLOCKED`；`RB=BLOCKED` 禁止提交，直到 genuinely new public evidence 到达并重新完成完整 gate。
7. 执行器只可在 `CONTROL_STATE=READY`、最终 `R!=RECONSIDER` 且 `RB in {NONE,DONE}` 时提交。Risk 仍只返回既定 `RISK / REASON`，不提交动作、不自行声明 CONTROL_STATE。

`UNKNOWN` 不允许无限 observe/replan。正常流程最多尝试一次 fresh observe/rebuild；仍无法消除时，基于现有公开证据做一次 bounded legal decision，最终 `R=UNKNOWN`。

## 与 Planning Recovery 的边界

Planning 的 `RECOVERY=RISK` 是战略恢复状态；Risk Review 仍然只 gate 当前 final candidate。

一个 public warning 允许 Planning 考虑 bounded cleanup，不等于 Risk 自动 `RECONSIDER`。只有当前 final candidate 直接触及 material risk，才进入 Full Review。

## Close

Risk 给出最终结果后，本次 decision closed；除非出现 genuinely new public evidence。

禁止编造 numeric threshold、hidden count、failure probability 或 hidden-risk value。

**Can Submit Action: No.**
不调用 `new_game`、`observe` 或 `take_action`。
