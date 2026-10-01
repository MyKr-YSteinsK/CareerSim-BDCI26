# Skills 设计说明

我们最后把 Agent 拆成四个 Skill，不是为了把架构做复杂，而是因为这四件事在长程游戏里很容易互相污染：事实记录、长期规划、交付跟踪和风险判断。如果全部塞进一个大 Prompt，前几个月还能工作，到了中后期就很容易把旧结论、临时风险和当前目标混在一起。

## 整体协同

实际运行顺序是：

fresh observe → Board → Delivery → Planning → Risk → take_action → fresh observe

只有 Single Agent 可以提交动作。四个 Skill 都只提供各自那一层判断。

Board 先把当前局能看到的状态整理出来，包括最新 Review、公开风险和最近一次 Skill / Network / Output 的可归因变化。它不决定“接下来做什么”，这样可以尽量减少事实层被策略预期污染。

Delivery 接着看当前有没有真正存在、而且还没闭环的工作项。这里我们很保守：工具调用成功不等于工作成果完成，口头说“做完了”也不等于已经被公开验证。最多保留三个活跃 item，避免 Agent 把大量旧任务一直背在上下文里。

Planning 才负责行动方向。默认是 Advance，也就是继续成长和争取晋升；只有 fresh public evidence 明确表明当前存在健康、安全、信任、合规、工作连续性或经济连续性的重大约束时，才进入 Stabilize。这个模式不会因为一个低分、一次没晋升、或者单纯某项数值比较低就自动开启。

Risk 是最后一道 gate。它只看 Planning 已经选好的候选，如果只是普通工作量、轻微健康成本或者机会成本，通常直接 PASS。只有候选确实碰到重大公开风险时才做 Full Review。这样可以避免 Risk Skill 每个月都重新规划一遍，既浪费 token，也容易把 Agent 推成长期保守。

## 长期规划

我们不是按单月贪心做选择，而是维护一个 Review Plan：

Objective / Primary Gap / Next Observable Checkpoint

第一次绩效评估以前，Primary Gap 可以是 UNKNOWN，重点放在可见成果、Skill、Network、Output 和 ownership 的广义成长。正式 Review 以后，再用公开反馈更新方向。

晋升对我们来说更像“复利放大器”，不是一个可以直接猜中的隐藏按钮。历史运行里，早晋升通常和后续更强的成长共现，但也有早晋升后最终失败的样本，所以我们没有写任何固定月份或隐藏阈值。没有晋升时仍然继续 Advance，只根据公开反馈修正下一段计划。

对 NO_GAIN 也做了类似处理。某条路径本次没有增长，只降低这条当前 Level / context 下的局部优先级，不推断“已经封顶”，也不会把一次失败传播到其它成长路径。Level 变化后旧经验会重新降置信度。

## 风险控制和失败恢复

我们踩过一个比较明显的坑：早期为了“不死”把 Health 和风险保护做得太重，Agent 会长时间停留在 Stabilize，结果虽然某些资源看起来安全，职业成长却停了。

最终版本采用 minimum necessary protection。遇到明确重大风险时，先做最小必要处理；动作后 fresh observe，如果风险已经解除就马上回到 Advance。普通疲劳、轻微摩擦、一次资源下降不会自动把整局切成保守模式。

同样地，失败恢复不是“重新开始思考一遍”。如果运行中出现 resume、context recovery 或 compaction 信号，先确认还是同一个 game session，再 fresh observe，依次重读四个 Skill，重建 Board 和 Delivery，然后恢复 Review Plan。恢复不完整时宁愿写 UNKNOWN，也不猜旧状态。

## 为什么不用 Team / Swarm / durable Memory

我们确实研究过更复杂的方案，但当前证据没有显示多 Agent 是主要瓶颈。这个任务大部分时间需要的是一个连续、稳定、能记住自己当前目标的决策者，而不是并行搜索。

Team / Swarm 会带来额外的协调、上下文和一致性成本；durable Memory 也会增加跨局污染和错误经验固化的风险。比赛阶段我们优先把单 Agent 的长期循环跑稳定，所以这两项没有进入最终提交。

## 资源开销

这个方案比较在意 token 和决策次数。Board 是紧凑状态，不保存完整 transcript；Delivery 最多三个活跃 item；Planning 每次最多比较两个真正有竞争力的候选；Risk 只有材料风险时才做重审。

Energy 也不是一次规划完三个动作，而是每做一个就 fresh observe，再决定下一个。这样会多几次判断，但能避免基于旧状态连续提交，整体上比错误执行一整季度再补救更划算。

我们最后想要的不是“每一步推理都最复杂”，而是 48 个月里一直保持同一套边界和目标，不因为上下文变长就逐渐失控。
