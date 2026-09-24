# S05-03｜静态合同回归 R1–R20

全为合成的**决策当时可见公开输入**；没有模型、游戏或 provider 执行。`PASS` 只指现有 Skill 文字蕴含预期行为，不代表未来 Agent 遵循或分数收益。当前 CareerSim game ID、合法选项和 fresh observe 均已给定，除非 case 特别说明。完成一次 integrated semantic revision（Planning 的 recovery cue）；第二轮未使用，blocking FAIL = `0`。

## S05-02 R1–R10 保留

[父矩阵](../S05-02-integrated-offline-optimization/static_regression_matrix.md) 逐项以最终四 Skill 复核，原输入与期望未改：

| Case | 保留依据 | 结果 |
|---|---|---|
| R1 普通成长 | Planning `When to use` 禁止无风险时默认保守；新 recovery 仅由 context loss/缺 checkpoint 触发。 | PASS |
| R2 严重后果 | Planning procedure 4 仍要求重开 Priority、合法路径及收益/风险/机会成本/UNKNOWN。 | PASS |
| R3 警告未解除 | praise/silence/mitigation 不单独证明解除，原文不变。 | PASS |
| R4 复合收益 | procedure 3 仍看未饱和分量，不因 Dignity 满值丢弃整个选项。 | PASS |
| R5 机会成本 | procedure 3 仍比较 Energy 与机会成本，不让复合标签自动胜出。 | PASS |
| R6 平台期 | `stalled` 的重复路径仍比较合法替代及成本。 | PASS |
| R7 进展中 | `advancing` 可继续，恢复分支只在无法验证旧目标时标 `unknown`。 | PASS |
| R8 Board/Planning | Board facts/freshness；Planning 仅一条相关事实与目标进展，不复制 Board。 | PASS |
| R9 Planning/Risk | 战略目标与当前候选风险仍分属两 Skill；新恢复不调用 Risk 常驻。 | PASS |
| R10 Trace | Trace Git blob 必须等于父 `5a1e3ceca8ffc2132303e43bc9f1c1dd630847a8`，只标记且唯一 Agent 提交。 | PASS |

## Reserve cases R11–R20

| Case | 公开反例 / 恢复场景 | 应有响应及最终合同锚点 | 结果 |
|---|---|---|---|
| R11 晚期遵循 | M36 缺正式 Planning checkpoint；现有公开状态和 game ID 可重新确认。 | Skill description 仍提示季度及 context-loss 恢复；Planning `When to use` 与 procedure 1 从 fresh observe 重建，不把早期 Priority 静默续用。 | PASS |
| R12 压缩后恢复 | 同 drive 继续、game ID 已确认，旧目标/历史片段不完整。 | 正常 loop 先 fresh `observe`；Planning re-read，旧目标未经同局 bounded evidence 确认则 prior progress=`unknown`；Board 用同局公开事实刷新。不得猜历史。 | PASS |
| R13 跨局隔离 | 新 game ID 与旧 checkpoint 不同；旧 Priority 仍在对话中。 | Planning procedure 1 拒绝 mismatched session；Board 丢旧 board，重新观察并设目标；无文件 Memory 继承。 | PASS |
| R14 Memory freshness | 需要验证持久记忆的旧月覆盖当前 observe。 | `DEFER_MEMORY`，没有 memory write/read/merge；现有 Board 的 fresh observe 优先规则仍保留。 | NOT_APPLICABLE（Memory 未采纳） |
| R15 晋升平台但无隐藏阈值 | 半年反馈和公开 Skill/Network/Output 可见，Level 仍停留；先前目标进展不足。 | Planning procedure 2–3 据公开 gap 与 prior objective 标 stalled/unknown，比较合法替代；不声称 `X >= N` 即晋升。 | PASS |
| R16 财富机会 | 当前合法选项明确有财富收益，同时有健康/成长成本。 | Planning procedure 2–3 用当前公开 gap、边际收益和机会成本比较；不固定选财富最大动作、不用 score 权重。专门财富机制仍 deferred。 | PASS |
| R17 高影响 rubric 真阳性 | material 不可逆/升级决策。 | 新 universal rubric 未采纳；既有 Planning 严重后果触发与 Risk 警告检查由 R2/R9 覆盖。 | NOT_APPLICABLE（rubric 未采纳） |
| R18 rubric 误报 | 普通低影响事件，无相关警告。 | 新 universal rubric 未采纳；R1 保证不额外二审。 | NOT_APPLICABLE（rubric 未采纳） |
| R19 父行为保留 | 严重后果、复合边际比较、目标进展、普通成长四种输入。 | Planning procedure 2–5、`When to use` 均仍在；recovery cue 不重写四种策略。 | PASS |
| R20 单一职责 | Board facts、Planning goal、Risk candidate、Trace marker 同时适用。 | Board/Planning/Risk 不提交；Trace 只给同一 Agent 的现有一次提交附 marker；唯一 Agent 选择并调用；无第五 Skill/Team。 | PASS |

结果：R1–R10 `10/10 PASS`；R11–R20 `7 PASS / 3 NOT_APPLICABLE`；所有 applicable blocking cases `PASS`。静态审查无法验证 model re-read、runtime compression 是否触发、checkpoint 实际频率、收益或长程稳定性。未来 trigger 不出现是 `NOT_OBSERVED`，不是本矩阵的运行时 PASS。
