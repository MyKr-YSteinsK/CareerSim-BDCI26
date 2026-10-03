---
name: career-decision
description: "Use on each fresh same-session observation. 晋升/成长/复利与现实结果兑现，动态生存和信任约束下最多比较两个竞争选项，检查最终候选；material checkpoint才做same-agent Deep Review并提出当前Brief更新。只推荐一个合法choice，不改公开事实、不提交、不创建Team。"
---

# Career Decision｜轻决策与关键节点复盘

## 唯一决策责任

Maximize remaining long-horizon progression and compounding while preserving a material failure floor。Single Agent 是唯一 action submitter；本 Skill 只推荐当前合法 integer choice 与简短中文公开依据。**Can Submit Action: No.** 不调用 `new_game`、`observe`、`take_action`，不改写公开事实，不建立第二 action writer，不创建 Team/Reviewer Agent。

读取 fresh 同局 observe、`career-state-brief` 的当前 Brief 和当前合法菜单；fresh facts 覆盖 stale summary。只使用 participant-visible evidence。官方直接返回的 choice `status_updates / effects`（包括 `HiddenRisk`）可作为 `ADVERTISED_CONFIGURED_DELTA` 比较；不是 realized effect 或 hidden stock，不保证增长。不累积 deltas 估算存量，不推 hidden formula/exact threshold/cap，不用 private DB/raw Test、internal IDs、跨局 memory 或 event→answer lookup。缺少 advertised 字段时用合法 choice 语义/已知事实正常决策，不猜值或阻断整局。动作结果只由 fresh observe验证。

## Ordinary decision

一次 fresh observe 只做一次 bounded decision，最多比较两个 genuinely competitive options，选一个当前合法整数。核对什么现在为真、Brief 哪些仍有效、当前 material constraint、值得兑现的真实承诺、剩余长期价值与最终安全；这是内部判断顺序，不是每步强制 checklist 输出。不反复叙述过程，没有 genuinely new public evidence 不重开选择。

默认积极追求晋升与 broad visible Skill/Network/Output、ownership、可兑现成果和未来机会；首评无正式gap时不要假造低指标硬门槛。正式 Review 的 deficit 是方向性依据，不把最弱数值当固定配方，不让窄gap挤掉更强时限机会/多维成长。普通 workload、轻微代价、摩擦或未知本身不否决更强成长。

动态保护：结合公开资源余量、当前负荷、advertised成本、不确定下行与当前真正可达的恢复路径，判断候选是否使 survival/safety/trust/job/income continuity 受 material 威胁。acute warning 即使数字尚可也必须处理；低绩效/no-advance 单独不等于 survival crisis。不设固定 Health buffer 或 risk counter。最小必要保护仍保留成长；若威胁来自绩效/交付，修复工作本身可以是最直接保护。解除后回主线，不为补满资源延长稳定化；Wealth紧张避无关花费，不否决真实收入/绩效恢复。

结果兑现：比较当前真实承诺、公开 deadline/依赖/可达完成条件与剩余 horizon；能完成/验证高值成果时，优于新增弱承诺或generic push，但不挡明显更强时限机会。首评前尤其比较现实可交成果与长周期资产；没有这样的菜单机会不伪造，没有公开未来 Review 不虚构。report-like label、generic Output、工具 success、generic praise不是已证成果；已verified不重复包装。旧item长期未兑现应重验价值，不能靠惯性继续。

局部响应：clean NO_GAIN只折价该 Level/context/dimension/已测 action family，cause UNKNOWN；有 responsive alternative 时不立刻重复原无增益路径，未知 family 仍开放，多维/ownership保留价值。Level变化或 context失效后重验。不构建全局cap或隐藏eligibility，不新增固定探索/覆盖配额。

Energy/Main使用同样当前比较。每次只推荐一个Energy action，没有余动作序列/固定配额；执行后fresh observe，新事实与realized response可改变下一选择。Main对visible ownership+多维成长有strong prior，但不是固定菜单答案，受当前安全/结果可兑现性限制。

## Final selected-candidate safety

选定候选后必须检查当前菜单合法性、公开代价、同scope未解除约束，特别是acute safety、job/trust/retaliation、compliance/confidentiality、financial/income continuity。普通成本没有被当前余量/公开warning升级成material问题时，接受有长期价值的成长，不因另一项更保守就自动换选。

候选有明确重大问题且存在直接相关合法替代时，最多做一次替代比较；选中替代也必须再检查其自身安全。最终选择仍无法闭合、session不确定、状态过期或工具结果未知时不提交，不靠未知标签绕过正确性。仅策略收益未知而事实/合法性可靠时可以做一次有边界的合法决定，不无限observe/replan。不输出独立风险枚举/证书；推荐只需一个choice与短理由，执行器独占实际提交权。

## Same-agent material-checkpoint Deep Review

当前同一Agent深评，随后由 `career-state-brief` 的唯一写入责任输出完整新Brief；不建立独立 Review Plan 或48个月刚性计划。触发必须是participant-visible、足以改变objective/assumption的material证据：

| Trigger | Review focus / exit |
|---|---|
| 正式 Review / no-advance / promotion | 哪种反馈/成果被奖励或失败，下一目标；Level变化清旧path；同一Review+promotion合并一次 |
| 新增或升级的major trust/job/compliance warning | 同scope威胁与repair可达性、何种公开证据才解除；风险持久保留但不重复cleanup配方 |
| major Health/safety shock 或正常活动不可行 | 实际下行、公开负荷/成本与可达恢复，最小必要保护；普通一次drop不是自动trigger |
| major verified result / failed commitment / material blocker | 完成/失败事实、deadline与现实下一兑现机会；generic praise不是verified |
| repeated clean NO_GAIN使当前高值path失效 | 哪个scope/path确已失效、可比较的替代；一次NO_GAIN只更新局部事实，混杂不算clean，不设次数阈值 |
| material opportunity-set change / current objective infeasible | 新机会/失效是否改变长期目标或重要假设；每个新Story菜单不自动deep review |

只回答等价三问：①什么真正改变、奖励或失败，哪些假设过时？②现在什么目标/path重要，什么该停？③什么结果/风险持续，什么公开证据使它失效？结果是五组Brief的有依据更新，得到一个当前目标/公开检验点与未解事实后立即退出回ordinary loop。

用 Brief 中该反馈/结果/警告的已处理basis去重：同checkpoint重复observe不重评，无新material变化的持续warning只做ordinary safety检查。同一observe多个相关trigger合并一次深评；不每action、每Story或每月机械触发。没有足够证据解释reward/cause时写UNKNOWN，不编造公式。Deep Review不代替提交前最终安全/合法性检查。

## Executor handoff

输出一个合法choice与简短理由。执行器提交前确认仍为fresh同局菜单、选择是单整数且final safety闭合；每次仅一个 `take_action`，成功后立即fresh observe，不用success receipt更新state，不在stale state连续action。已有session绝不第二次 `new_game`。

失败/unknown action outcome时先停止提交；仅在现有授权内用同局fresh observe/公开日志核对已发生什么，不能盲重发。仍unknown、身份不明或不可恢复工具失败就停止并说明技术问题；没有live授权不调用任何游戏工具。active game时保持whole-game loop，不因一个choice、month、Review或Brief更新结束assistant execution；自然结束只认structured `game.ended`。
