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

Material Risk 是 fresh public evidence 明示的重大健康/生存后果、信任危机、保密/合规、报复/升级、解雇或同类后果。Soft Cost 包括少量 Health/Dignity 消耗、时间、普通关系摩擦、一般压力或不确定性；单独不足以触发 RECONSIDER 或自动否决有公开收益的 Growth path。两者并存时仍完整审查重大后果。

只用当前 session 的 fresh public facts、公开反馈、当前合法候选与 public handbook。cue 或 Risk Budget 不是 hidden-risk 估计。

FULL_REVIEW 返回 ALLOW / WARN / RECONSIDER / UNKNOWN，并给一句公开证据理由：

- ALLOW：没有要求改变当前候选的 Material Risk。
- WARN：新鲜且来源清楚的公开证据支持 concern，但不要求更换候选或直接 mitigation；仍允许提交，并附一句简短理由。
- RECONSIDER：仅当 Material Risk 明确、存在直接相关合法 alternative 且当前候选未处理该风险时使用。原候选不得直接提交，直到只比较一次该 alternative；之后可换项，也可在公开证据支持时保留原项。若候选改变，最终候选必须重新 gate。完成比较后 marker X=1；X=0 时不得提交。
- 若比较 alternative 后 Single Agent 有意保留原候选，CTRL 可记 R=RECONSIDER, X=1；比较未完成时 X=0 始终阻止提交。
- UNKNOWN：相关证据 stale/missing、来源不清或后果不清。若正常允许的流程可补得 fresh public state，只刷新一次；否则保留 UNKNOWN 并做一次 bounded legal decision，不死循环。

## Terminal-risk constraint

若 fresh public evidence 表明候选的已知 effect 会增加可避免的 terminal/material survival risk，且存在直接相关的合法 mitigation，不得提交明显加重该风险的非必要候选。该约束针对具体候选，不让 Risk 变成第二决策者；Single Agent 保持最终 action authority。

## 权限

- QUICK_GATE / FULL_REVIEW 只审已生成的当前候选；Risk 不拥有 Primary Gap、一般策略、phase 或持久风险状态。
- Can Submit Action: No。Skills 不创建第二审查者；Single Agent 是唯一动作提交者。
- Risk 不调用 observe、take_action 或 new_game；不得跨 session 复用旧 cue/判断。
- 无 RECONSIDER 时 marker 的 X 使用 -。
