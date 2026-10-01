# FZU-Loss快点降｜CareerSim Agent

这是我们最终提交的单 Agent 方案。整体思路其实很朴素：尽量让 Agent 一直做有长期价值的事情，同时别因为一次风险、一次失败或者一次坏反馈把整条职业轨迹搞崩。

我们没有使用多 Agent。实际调下来以后，最大的难点并不是“人手不够”，而是长期信息会乱、同一个问题会被不同模块重复判断、以及局部失败很容易把策略带偏。最后我们保留了一个动作提交者，加四个职责很清楚的 Skill：

- structured-state-board：只整理当前局能看到的事实；
- rolling-planning：维护跨 Review 的目标和当前行动方向；
- delivery-progress：跟踪真正存在的交付事项；
- risk-review：最后一道风险门，不重新规划整局。

运行时每做完一个动作都会重新 observe，再更新 Board、Delivery、Planning 和 Risk。我们不连续对旧状态提交动作，也不根据隐藏字段或 Dev 里的内部信息猜规则。

这个版本来自我们后期最稳定的一条路线。Dev 上有两次完整 48 个月独立运行，quantitative 分别为 72.65 和 59.00，都存活到 48 个月。它不是我们历史上单局最高的版本，但相比一些“单局很高、另一次直接崩掉”的方案，我们更愿意提交这条已经验证过完整长程执行的版本。

详细设计见 design/skills_design.md，实验取舍见 design/decision_report.md。
