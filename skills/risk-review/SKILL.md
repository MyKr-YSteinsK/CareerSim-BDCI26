---
name: risk-review
description: 每个动作前快速检查公开生存状态与语义风险线索；仅在非安全带或 cue 出现时完整审查当前候选的重大后果，不提交动作。
---

# Risk Review｜候选风险门

## QUICK_GATE｜每个动作前

在每次 story、Energy 或 Main `take_action` 前，只针对当前合法候选与最新 `CONTROL_SCAN` 快查：

1. Survival band；
2. 候选文本和场景的语义 cue；
3. 明确公开 warning / consequence；
4. 候选是否进一步消耗已知有限的生存资源，或放大已知 Material Risk。

返回供 `CONTROL_SCAN` 使用的一个 `Risk Cue`：`NONE / HEALTH / COMPLIANCE / TRUST / RELIABILITY / OTHER`。`Survival=SAFE` 且 cue=`NONE` 时结束 QUICK_GATE，不做 FULL_REVIEW。若 Survival 为 `WATCH / TIGHT / CRITICAL`，或 cue 非 `NONE`，完整审查当前候选。QUICK_GATE 本身不自动改选。

## Semantic Trigger Library｜只触发复核

以下是可迁移的公开语义线索，不是答案映射，也不自动等于 Material Risk：

- `HEALTH`：健康、身体、熬夜、加班、通宵、on-call / 值守、生病、传染、顶岗、硬扛、饮酒、作息、体检、就医、透支、疲惫；
- `COMPLIANCE`：合规、保密、泄露、外传、截图、未授权、竞对、未公开、客户数据、内部资料、监管、违规、绕流程、安全漏洞；
- `TRUST`：信任危机、隐患、甩锅、隐瞒、造假、报复、抢功、掩盖、爆雷、埋雷、问责；
- `RELIABILITY`：事故、生产环境、故障、上线、回滚、CI、测试、漏洞、数据库迁移、安全；
- `OTHER`：其它语义清楚且可能造成类似重大后果的公开 cue。

泛化的“同事 / 领导 / 项目”或一个普通负面词不构成 cue。cue 只要求更仔细查看当前公开事实与候选后果；不得仅因关键词、事件标题或故事类别自动断定 Material Risk。不得读取 story option 隐藏 status update，也不得建立 `event_id/title → choice` 表。

## FULL_REVIEW｜仅当前候选

将公开后果区分为：

- **Material Risk**：明确重大 Health / 生存后果、信任危机、保密/合规问题、报复/升级、解雇威胁，或含义相当的公开重大后果。即使选项文字没有风险词，若 Survival=`TIGHT / CRITICAL` 且候选继续消耗有限生存资源，也必须审查。
- **Soft Cost**：少量 Health / Dignity 消耗、时间、普通关系摩擦、一般工作压力或不确定性。Soft Cost 单独不足以触发 `RECONSIDER`，不能自动否决有明显公开收益的 Growth path；若与 Material Risk 并存，仍完整审查重大后果。

只用当前 session 的 fresh public observe、明确反馈、当前合法候选及公开 Handbook。不要猜隐藏计数、threshold、概率或选项未公开效果。

FULL_REVIEW 返回一个状态与一句证据理由：

- `ALLOW`：没有被忽略的 Material Risk；Soft Cost 本身不要求改选。
- `WARN`：有公开风险线索，但没有直接合法缓解项，或证据不足以要求重新比较。
- `RECONSIDER`：仅当当前公开 Material Risk 明确、存在直接相关的合法缓解项，且候选尚未处理时使用。同一个 Agent 对当前候选与缓解项重比一次；不强制选择最保守选项。
- `UNKNOWN`：session、状态、证据或选项不新鲜/不清楚。说明未知，回到正常流程，不猜测或阻断。

只有当前合法选项确实包含 `处理历史埋雷`，且 fresh public context 明确存在对应的埋雷/信任风险时，才考虑该选项。不得声称其效果已知、一次即可清除风险或应定期选择。

## 权限

- QUICK_GATE / FULL_REVIEW 均只审查当前候选；Risk 不拥有 Primary Gap、一般策略或持久化风险状态。
- Can Submit Action: No。Skills 不创建第二审查者；Single Agent 仍是唯一动作提交者。
- 不调用 `observe`、`take_action` 或 `new_game`；不跨 session 使用旧 cue / 风险判断。
