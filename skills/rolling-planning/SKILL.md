---
name: rolling-planning
description: "每次 fresh Board/Delivery 后做一次晋升优先排序：窗口内兑现、广义成长、局部响应折价与最小必要保护；只输出一个合法候选，不提交动作。"
---

# Rolling Planning｜实证晋升优先

## 接口与输入

Planning 拥有 REVIEW_PLAN、MODE、RECOVERY 与 ranking；Board 报告事实，Delivery 报告 lifecycle，Risk 只 gate 最终候选，executor 唯一提交。中文判断；只用同 session fresh Board/Delivery、participant-visible event/合法 choice 语义、公开 Handbook/正式反馈/已确认公开结果。

```text
REVIEW_PLAN = <Objective | Primary Gap | Next Observable Checkpoint>
MODE = A | S
RECOVERY=NONE|PROGRESSION|RESOURCE|RISK|DELIVERY|UNKNOWN
```

沿用 Manifest evidence firewall：`HiddenRisk`、hidden counters、internal score、internal event id/effect、public-status-unclear numeric status_updates 均 `EXCLUDE_FROM_STRATEGY until verified public`。不读取 hidden/private/Dev evidence，不跨局记忆，不推隐藏阈值、cap、公式或事件答案表；hint 只作软证据。排序不能改写 Board/Delivery 的 UNKNOWN。

## 九条决策规则

### R1｜Fresh state first

每个 action 后以 fresh observe 为准；advertised hint、realized 公开变化、career result、recognition 分开。success receipt 只证明工具执行，不证明成长/交付。跨月、Review、promotion 或其它 plausible cause 混合时沿用 Board 的 UNKNOWN/MIXED，不归因。先检查 fresh binding constraint，再结合正式反馈、公开结果和当前状态更新计划。

### R2｜Promotion-first

无 material danger 时默认 MODE=A；依次偏向当前/最近公开 Review window 内可兑现结果、high-value ownership/progression、broad Skill/Network/Output growth、future option value。Primary Gap 依据正式反馈而非最低数值，只作方向，不长期压掉更强可兑现机会或其它响应维度；不只追 Output，不把公开数值当晋升要求。无未来公开 checkpoint 时比较剩余 horizon 内可实现价值，不虚构未来 Review。

### R3｜窗口内交付

最多两个高价值方案竞争时，偏向窗口内能完成、有明确 owner、可形成公开结果的方案，而非窗口外长期资产。长期方案明确能及时完成、短方案有 material quality/safety/compliance cost、或不存在可兑现短路径时，重新比较。near-checkpoint 高价值 commitment 优先完成/验证；blocked/stale item 不阻止明确更强的新机会。

### R4｜Result ladder

promise/progress < delivered/completed < externally/publicly recognized result。具体公开完成/验收及与成果相连的认可才支持对应层级；generic praise、report-like label、工具 success 不等于 verified deliverable。消费 Delivery stage/evidence_status/recognition_link/next_checkpoint，不自行升级 lifecycle。该层级不是 hidden score 或 promotion requirement；已验证成果不因重复汇报而再次升级。

### R5｜Local realized-response discount

消费 Board PROGRESSION_RESPONSE：相同 Level/可比 context 的 clean NO_GAIN 折价已测试 family 对该维度的预期；比较 responsive alternative 或一个有价值未试 family，有 responsive alternative 时不立即重复该 no-gain path。其它维度、ownership、结果等独立价值仍保留；UNKNOWN/未试 family 不封禁。Level/context/material condition 改变或后续 clean GAIN 后重新评估；一次 flat 不构成永久 cap，也不证明其它路径无收益。

### R6｜Energy one-step

`QUARTER_INTENT=<MODE|current target>` 只记目标；每次只选一个 Energy action，one action → fresh observe → re-rank。丢弃旧 remaining-action intent，消费新的 PROGRESSION_RESPONSE 再分配剩余体力；禁止整季 recipe、multi-step sequence/批次。保护当前明确紧急缺口后，比较目标维度 realized response、体力与 Health 成本：恢复通常有响应，report/network 可能平，高强度/学习存在真实 Health cost；这些是可被本局回包推翻的软 prior，非固定动作顺序。cleanup 公开六维平不证明隐藏风险无收益，也不证明 warning 已解除。

### R7｜Conditional Main ownership

申请关键项目有 strong prior，但不是 default answer：须有实际可兑现 ownership、负荷可承受、上一项目未明显 blocked/stale 且无 material danger。条件不成立时比较当前合法的 result presentation、rotation、risk reduction 或其它 family，不固定替代顺序；Main 跨月混合回包不证明净项目收益。普通成本可为明显更强的成长/结果接受。

### R8｜Material danger overrides growth

每次 fresh observe 从 A 重新判断，旧 S 不自动续期。只有当前未解除的 material public evidence 才 S：acute physical/psychological/safety danger、explicit trust/job/compliance/confidentiality escalation、income/affordability continuity threat，或公开证明 normal activity infeasible。高 Health 不证明 trust/performance 安全；普通负 Health、workload、mild fatigue、关系摩擦及不确定性不自动 S，无数字阈值。

S 选择最小必要保护，避免恶化约束并尽量保留晋升价值；绩效/交付修复若直接解除 job threat 可作为保护。fresh evidence 显示约束解除或场景结束即回 A，不为补满资源延长 S，数字回升/无关夸奖不证明解除。RECOVERY 沿用既定分类；普通 poor grade/no-promotion 属于 PROGRESSION/A。明确 public warning 且有 reparative legal option 可一次 bounded cleanup；fresh observe 后回主线，仅同类 warning 持续/再次/新增才重评，不能用无关证据重置限制。

### R9｜No-advance re-route

正式 Review/promotion/no-advance 到来重建 REVIEW_PLAN：哪些结果未兑现、tested path 哪个不响应、下一公开窗口最可兑现的 ownership/result 是什么？no-advance 必须重排，不能继续 stale recipe、机械追 lowest stat 或保证下次追回。首评前 Primary Gap 可 UNKNOWN，追可见结果和广义成长；普通 Story/一次波动不随意换 gap。目标完成、路径被 fresh evidence 推翻或不可行时也更新计划。

## 一次排序与输出

`ONE FRESH OBSERVE = ONE PLANNING PASS`：确定 MODE/REVIEW_PLAN，删除不可接受/被支配项；最多两个 genuinely competitive candidates 比较一次，输出唯一 CANDIDATE，无 genuinely new public evidence 不重开。Risk=RECONSIDER 只允许一次直接相关替代项比较，选定项再取得自己的 final Risk；沿用 CTRL RB=NONE|DONE|BLOCKED，未闭合或最终仍 RECONSIDER 则 BLOCKED。UNKNOWN 最多一次 fresh observe/rebuild，仍不明只做一次 bounded legal decision。executor 独占 CONTROL_STATE/READY/preflight；本 Skill 不声明 READY。

observable context recovery 由 executor 按 Manifest 同 session fresh observe → 四 Skills 重读 → Board/Delivery 重建 → 恢复 REVIEW_PLAN/RECOVERY；缺失 UNKNOWN，未完成不排序。每步仍按既定 Delivery/Risk/preflight 接口执行。

只返回：

```text
PLAN: G=<gap|?> P=<A|S|?> F=<NONE|PROGRESSION|RESOURCE|RISK|DELIVERY|UNKNOWN> checkpoint=<short checkpoint>
CANDIDATE: choice=<one legal integer> reason=<one concise public-evidence reason>
```

**Can Submit Action: No.** 不调用 `new_game`、`observe` 或 `take_action`。
