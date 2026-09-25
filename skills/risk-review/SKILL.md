---
name: risk-review
description: "每个 take_action 前必须应用；只对已生成候选做 candidate-specific Material Risk gate；不规划、不提交动作。"
---

# Risk Review｜候选风险门

## QUICK_GATE｜candidate-first

每次 story、Energy 或 Main take_action 前，只检查已经生成的当前合法候选及 fresh current-session public facts：

- candidate 的明确公开后果；
- 与 candidate 直接相关的 contextual high-signal cue；
- fresh public warning / consequence；
- Planning Risk Budget=TIGHT 时，candidate 是否直接加重相关公开生存风险。

无候选相关 Material Risk 或 high-signal cue 时返回 PASS。普通不确定性或 Soft Cost、普通负荷/分歧、日常 CI/testing、泛化角色/项目词及普通交付/关系/组织政治，不单独触发 FULL_REVIEW。

## Contextual cue families

保留 enum；cue 只触发检查，不自动等于 Material Risk，也不是答案映射：

NONE / HEALTH / COMPLIANCE / TRUST / RELIABILITY / OTHER

仅保留四类高 signal 情境：

1. confidentiality / data authorization；
2. integrity / concealment 且有明确 material consequence；
3. health load / illness 且关联 fresh public state；
4. material reliability incident。

OTHER 是窄的 escape hatch。普通 delivery/scope、compensation/career、relationship boundary、org politics 属于 Planning，只有出现明确 Material consequence 才升级 Risk。generic role/project words 或单个普通负面词不构成 cue。不扩成长 keyword dictionary。

不得读取 story option hidden status update、hidden counters、其它 session 或 Dev answer data；不得建立 event_id/title→choice lookup。

## FULL_REVIEW｜当前候选

Material Risk 是 fresh public evidence 明示的重大健康/生存后果、信任危机、保密/合规、报复/升级、解雇或同类后果。Soft Cost 包括少量 Health/Dignity 消耗、时间、普通关系摩擦、一般压力或不确定性。一次性小额 Health/Dignity 消耗，只有在 Planning 的 fresh public survival trend 未使该维度成为当前约束时，才可孤立按 Soft Cost 处理；若 Planning 因该公开趋势恶化将 Risk Budget 设为 TIGHT，不得孤立评估下一笔小额代价。Soft Cost 单独仍不足以触发 RECONSIDER 或自动否决有公开收益的 Growth path；两者并存时仍完整审查重大后果。Planning owns the public survival trend and candidate-independent Risk Budget; Risk remains a candidate-specific gate.

只用当前 session 的 fresh public facts、公开反馈、当前合法候选与 public handbook。cue 或 Risk Budget 不是 hidden-risk 估计。

FULL_REVIEW 返回 ALLOW / WARN / RECONSIDER / UNKNOWN，并给一句公开证据理由：

- ALLOW：没有要求改变当前候选的 Material Risk。
- WARN：新鲜且来源清楚的公开证据支持 concern，但不要求更换候选或直接 mitigation；仍允许提交，并附一句简短理由。
- RECONSIDER：仅当 Material Risk 明确、存在直接相关合法 alternative 且当前候选未处理该风险时使用。只比较一个 alternative；比较完成后，本次 action path 的过程结果仍为 RECONSIDER，X=1。若换候选，替代候选仍须过 Material Risk gate，但不得把过程结果改写成 PASS；若有公开证据支持，也可在完成比较后保留原候选。比较未完成时 X=0，禁止调用 take_action。
- 未有候选触发 RECONSIDER 时，R 记录最终普通 gate 结果，X=-。
- UNKNOWN：相关证据 stale/missing、来源不清或后果不清。若正常允许的流程可补得 fresh public state，只刷新一次；否则保留 UNKNOWN 并做一次 bounded legal decision，不死循环。

DECISION_CLOSED：最终候选完成最终 Risk gate 后，若没有新的 fresh observe、tool result、event content 或其它公开证据，gate 与候选决定即关闭；不重跑 Risk gate、不重开比较或重复审查。只有新公开证据才允许重新审查。

## Terminal-risk constraint

若 fresh public evidence 表明候选的已知 effect 会增加可避免的 terminal/material survival risk，且存在直接相关的合法 mitigation，不得提交明显加重该风险的非必要候选。该约束针对具体候选，不让 Risk 变成第二决策者；Single Agent 保持最终 action authority。

## 权限

- QUICK_GATE / FULL_REVIEW 只审已生成的当前候选；Risk 不拥有 Primary Gap、一般策略、phase 或持久风险状态。
- Can Submit Action: No。Skills 不创建第二审查者；Single Agent 是唯一动作提交者。
- Risk 不调用 observe、take_action 或 new_game；不得跨 session 复用旧 cue/判断。
