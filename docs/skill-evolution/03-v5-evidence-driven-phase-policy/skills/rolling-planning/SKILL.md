---
name: rolling-planning
description: 唯一战略规划 Skill；每次决策快速维护阶段、生存带与单一 Primary Gap，并在明确 checkpoint 运行有界完整规划，不提交动作。
---

# Rolling Planning｜阶段化滚动规划

## 职责与调用频率

`rolling-planning` 是唯一战略规划 owner。每次决策都以已有 Board 事实做一次极短 `QUICK_SCAN`：当前 Phase、Survival band、唯一 Primary Gap、近期 Progress；consult 最新 `CONTROL_SCAN`，不重复复述状态或长推理。QUICK_SCAN 是 Skill 的功能使用，不要求每次 `read_file` 全文。

仅在以下 FULL checkpoint 重建完整规划：新局；每季度首次 Energy 决策前；半年 review 前的最后一个可行动窗口；review / promotion / feedback 结果后；Survival band、Primary Gap 或重大公开状态改变；Progress=`STALLED`；context recovery。普通故事选择不触发完整 checkpoint。

只用当前 game session 的 fresh public evidence、Board 可核实事实及公开 Handbook。不得用其它对局、局后信息、hidden thresholds、evaluator weights 或 Dev 内部公式。

## Survival Guard｜约束，不是固定阈值

每次 QUICK_SCAN 选一个语义带：

- `SAFE`：公开生存状态新鲜且稳定，无当前重大警告，仍有正常余量；允许正常 Growth。
- `WATCH`：可见趋势下行、近期 shock 明显侵蚀缓冲、出现健康/疲劳/疾病/信任/合规线索，或恢复机会较远。提高观察与候选审查，但不自动放弃成长。
- `TIGHT`：公开生存资源偏低且仍下降、多个可见风险叠加，或可信的一般不利变化已可能逼近严重后果。生存约束高于 Primary Gap 的 Growth；先比较合法的 recovery / repair / avoidance。
- `CRITICAL`：fresh public state 已近终局或重大危机，可信的小幅进一步损失即可造成严重后果。暂停非必要 Growth，优先当前合法且可验证的保护/恢复路径。

这些是策略语义分类，不是游戏阈值。不得编码 `Health <= N`、固定 Dignity / Network / Wealth 数值线、HiddenRisk 库存或“每季必选某恢复动作”。缺少可靠公开依据时用 `UNKNOWN`，不得把 `UNKNOWN` 伪装成 `SAFE`。

## Phase｜由公开状态滚动决定

每次规划选一个阶段，使用当前 public state、promotion / feedback 结果、下一 review window 与剩余 48-month horizon；不使用固定月份→动作表。performance、network、dignity、wealth 或组织动态等非 Risk 语义线索可帮助识别 Primary Gap，但没有明确 material consequence 时不因此升级 Risk FULL_REVIEW。依次判断：

1. 可兑现的 review windows 已少、剩余 horizon 短：`FINAL_SPRINT`。
2. Survival 非 `TIGHT / CRITICAL`，review 临近或公开反馈指出 promotion-related gap：`PROMOTION`。
3. 已有 promotion / 更高 Level，Survival 稳定且时间足以兑现长期收益：`COMPOUNDING`。
4. 其余基础仍薄、buffer 未稳定或晋升证据不足：`FOUNDATION`。

- `FOUNDATION`：先保可持续的 Skill / Output / Network 与 Health / Dignity buffer；不为短期增长透支生存余量。
- `PROMOTION`：只依公开 feedback 与 Skill / Output / Network 等当前 gap 比较 review-readiness，不猜晋升月份或公式。
- `COMPOUNDING`：维持公开 review quality，避免 Skill / Network / Output 明显失衡，并考虑剩余时间能兑现的职业复利；不套用 Dev 评分权重。
- `FINAL_SPRINT`：若 `SAFE / WATCH`，可提高当前可兑现 Growth 的积极性；偏向剩余月份内可观察的 benefit，降低纯远期/不确定收益优先级。若 `TIGHT / CRITICAL`，生存约束仍优先，禁止为末期冲刺透支生存。

## Quarterly / Pre-review checkpoint

季度 checkpoint 必须在该季首次 Energy 决策前，以 fresh observe 更新 Board 后完成；同季度 Main action 复用，除非 material state / Gap / Survival 改变。

每个半年 review 前最后一个可行动窗口运行 `PRE_REVIEW_CHECK`，检查：当前 Survival band；Health / Dignity / Network / Wealth 趋势；公开 Leader / performance warning；Primary Gap；review 前剩余 story exposure；可验证的 recovery / repair opportunity。不得依赖 review 之后才出现的 Energy 来救已经濒危的 review/story window；不反推 talk / promotion 公式。

完整 checkpoint 最多 7 行，字段固定为：

```text
Phase:
Horizon:
Survival:
Primary Gap:
Progress:
Recent Effect:
Path Trade-off:
```

`Primary Gap` 恰好一个公开可观察短板，或有公开依据的 career progression stalled；不得默认平均发展或固定优先级。无证据时为 `UNKNOWN`。`Path Trade-off` 最多两个合法路径，不复制 Board 或 transcript。

## Progress / STALLED

每次 checkpoint 对 prior objective 标记 `ADVANCING / STALLED / UNKNOWN`：只用 Primary Gap 本身或直接相关的公开 career progress。表扬、一般正面反馈或菜单描述不够；无法比较、归因不清时为 `UNKNOWN`。

- `advertised effect` 是先验菜单信息；同局可靠、可比的 `observed effect` 优先。
- 同一 strategic action 针对同一 Primary Gap，在两个相邻、可比 checkpoint 均无公开进展，才是 `STALLED`。
- `STALLED` 后本次必须比较至少一个不同类型的合法 alternative，但不自动切换；一次无增长不强制换路。
- Gap 改变或旧 action 对新 Gap 有可靠 observed benefit 时可继续，并说明公开依据。
- `TIGHT / CRITICAL` 可暂时覆盖 Growth / STALLED 路径偏好。

## Path / Energy / Main action

安全是约束而非默认优化目标。若无 Material Risk 且 Survival=`SAFE`（或 `WATCH` 下没有直接生存威胁），普通 Soft Cost 不能自动否决对当前 Gap 有明显更强公开收益的合法 Growth path。比较次序：Material Risk → 当前 Gap 的公开贡献 → 有用的次级收益 → Soft Cost / opportunity cost → UNKNOWN；不设数值权重，“成熟、圆滑、体面、稳妥”本身不算收益。

Energy：`TIGHT / CRITICAL` 时先找合法、可验证的必要恢复/修复；否则按当前 Primary Gap 比较可见边际收益。收益相同或近似时选生存/风险成本较低者，不无理由浪费 Energy。可按当前菜单识别被同成本、同目标且风险更低的选项支配的路径；不得硬编码“每季必选健康恢复 / 汇报 / 禁用高强度工作”。

Main action：`申请关键项目` 仅是 broad-growth prior，不是固定 winner。只有 Survival 不在 `TIGHT / CRITICAL`、其 Skill / Output / Network 效果仍与当前 Gap 相关、未对该 Gap `STALLED`、且没有更直接的合法路径时才可继续优先；否则比较当前可用的 report、rotation、mentor、resource、relationship repair 或 low-profile risk 路径。只按当前公开 Gap 与 observed effect 判断。

普通非战略 story choice 最多比较两个 strongest legal candidates 一次。无 fresh evidence 时不重开已完成比较，除非 `risk-review=RECONSIDER`；Risk 状态不等于必须选最保守项。

## 权限与边界

- Planning 给 Single Agent 有界战略建议；Can Submit Action: No。Single Agent 是唯一动作提交者。
- 不调用 `new_game`、`observe` 或 `take_action`；不建立 durable / cross-game Memory，不创建第二审查者、Agent、Team 或 Swarm。
- session、月份、状态、effect 或 option 不新鲜时保留 `UNKNOWN`，回正常流程取得 fresh public evidence。
