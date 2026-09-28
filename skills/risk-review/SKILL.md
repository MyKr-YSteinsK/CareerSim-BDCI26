---
name: risk-review
description: "每个 take_action 前检查 Planning 已选候选是否有公开、直接、足以威胁继续游戏的重大风险；只守生存底线，不把正常成长动作变成保守选择。"
---

# Risk Review｜Survival Floor Gate

Risk 的职责是防止一次明显可避免的选择把整局打穿，不负责把策略变得“最安全”。

Planning 先选候选，Risk 最后审一次。

## 默认

如果候选只有：

- 普通 workload；
- 小幅 Health / Dignity 成本；
- 一般关系摩擦；
- 普通 uncertainty；
- 可接受的机会成本；

而当前没有对应的公开严重 warning，则 `PASS`。

**不能因为 Growth action 有成本就自动拦截。**

## Material Risk

只有 fresh public evidence 支持下面这类重大后果时才做 FULL_REVIEW：

- 明确严重健康/心理生存风险；
- dismissal / job-continuity danger；
- trust crisis 或严重 retaliation；
- compliance / confidentiality / safety；
- candidate 会直接加重当前已经明显恶化的 Wealth / Health / Dignity 生存方向；
- 当前公开事故/warning 与 candidate 有直接、具体的再次恶化关系。

官网只公开失败方向，不公开精确阈值、计数和连续触发条件，所以 Risk 不使用任何自创数字线或次数规则。

## Wealth guard

Wealth 很低/非正或有 affordability warning 时：

- 明确的非必要金钱支出可以触发审查；
- 明显伤害 job continuity 的选择可以触发审查；
- **能够改善正式绩效、晋升或收入能力的 Growth action 不因为 Wealth 低就被 Risk 否决。**

财富危机不是“停止成长”的理由。

## Health / Dignity guard

只有 fresh public symptoms / warning /明显持续恶化已经成立时，才阻止继续叠加非必要的严重透支。

如果状态已经恢复、warning 已解除，就回到普通标准，不长期维持高敏感度。

## Compliance / trust

保密、合规、安全问题按公开事实处理。存在直接合法替代方案时，可以 `RECONSIDER`。

普通组织政治、普通关系选择、普通 Story 语义不由 Risk 二次规划。

## Result

返回：

`ALLOW / WARN / RECONSIDER / UNKNOWN`

`RECONSIDER` 只在：

1. Material Risk 明确；
2. 当前候选没有处理；
3. 有一个直接相关合法 alternative。

最多比较一个 alternative。替代候选也过一次 gate。

最终 gate 后进入 `DECISION_CLOSED`。没有新的 fresh observe / tool result / event evidence 就不重开。

Can Submit Action: No。Risk 不调用 `new_game`、`observe` 或 `take_action`，不跨 session 保存判断。
