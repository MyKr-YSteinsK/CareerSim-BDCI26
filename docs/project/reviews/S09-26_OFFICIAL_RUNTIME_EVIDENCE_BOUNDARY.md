# S09-26｜官方运行时信息准入纠偏与 Reviewer 输入完整性修复

## Identity / decision

- Status: STATIC_IMPLEMENTED_NOT_RUNTIME_VALIDATED；`IN_FLIGHT_EVIDENCE`。
- Base evidence: `6efb27128ed1727d7def7ae21d64d9b67e512495`；implementation: `c9a9d914481c4d2a3221719b1ae90871be057c8a`。
- Branch: `codex/s09-14-v9a-static`；parent: `candidate-v10f-cap-scope-correction`（implementation `7895515`）。
- Candidate: `candidate-v10g-official-runtime-evidence-boundary`；classification: `OFFICIAL_RUNTIME_INFORMATION_BOUNDARY_CORRECTION`。
- Strategy delta: `NONE`；information-policy delta: `SOURCE_BASED_TEST_ACCESS_ADMISSIBILITY`。
- Main/origin main v8a freeze `6a4037fdf2b75c105cfe0b40b93ea68d3dd0a6f3` 未改；全部新 Candidate validation flags 为 false。
- Decision: `S09_26_V10G_INFORMATION_BOUNDARY_STATIC_PASS_RETURN_TO_STAGE`。

## K1 correction

最终常驻规则替换旧 K1，不追加另一份策略层：

```text
K1 OFFICIAL-ACCESS：按经验证官方 Test-equivalent Agent 可达路径准入，不按字段名禁用；官方明确禁用者除外。observe choices[].status_updates（含 HiddenRisk ±N）是 ADVERTISED_EFFECT，供排序/Risk，非实际结果/隐藏stock/阈值；fresh REALIZED_PUBLIC_RESPONSE 优先。不可达隐藏stock/counters/graph IDs、raw DB/对象、Runner取证、private Test、凭据/provider内部及外部干预不得依赖。可达性未知保持 UNKNOWN，不虚构/永久禁用。合法Dev一般prior/同局推断是hypothesis，非隐藏fact/threshold/formula；禁 event-answer lookup、跨局动态记忆、由delta重建隐藏stock；日志只据实际取得，不新增轮询。
```

| 类别 | 准入 / 证据力度 |
|---|---|
| ALLOW | 经验证官方 Agent observe 当前state/event/choice/energy cost/`status_updates`、Handbook、Review/promotion/反馈、合法实际取得的同局官方logs；明确适用官方禁令除外 |
| BAN | 不可达隐藏stock/counters/graph IDs、raw DB/对象、Codex-only Runner取证、private Test/答案映射、凭据/provider内部、不可供提交方案使用的外部干预 |
| CONDITIONAL | 合法Dev一般prior、Review-window关联、晋升机制/响应倾向推断只作 hypothesis/empirical prior，不是隐藏fact/精确保证阈值 |
| UNKNOWN | 未验证权限/部署路径保持未知；不虚构可达性，也不永久禁用 |

`HiddenRisk+1` 广告delta可用于收益/风险比较；不等于“当前stock=8”“threshold=10”或保证某未来事件。action后的fresh实际公开响应高于广告预期；不能累加delta重建隐藏stock。K2仍拒绝由少量NO_GAIN/高数值推封顶；K3仍拒绝numeric-only S，risk delta单独不授权S、Full Review或cleanup。

Board只新增来源/freshness区分的紧凑EVIDENCE行，STATE仍直接复制fresh公开值；Planning仅替换Evidence/interfaces两段；Risk仅校准可达广告风险成本与未知stock。Delivery byte-identical。日志只是准入纠偏，没有新轮询或logs收益策略；无新prior库。

## Reviewer completeness / provenance

`official_before` / `official_after`保存锁定1.0.1完整官方observe上下文，`before_source`保存seq/UTC/tool/call ID。choices保留所有返回字段（尤其`status_updates`），event保留title/description/rules/remaining_energy/energy_budget/max_selections等；selected candidate、notes、fresh前后公开state继续保留。

按已核验官方serializer只剔除当前隐藏stock/counters、event graph IDs、choice graph links；不按字段名排斥choice delta，不加入raw DB/private顶层对象，拒绝跨session action/observe。纯函数与锁定serializer比较通过；models.py hash匹配S09-25已记录官方wheel来源。

未来K1/access receipt携带version2来源证明：精确使用内容、真实model-context位置、官方路径/禁令依据、delta/stock/threshold/prior claim/support类型、同局身份、action前seq、context coverage及官方字段路径/值。没有来源证明不能确认不可达信息违规；未知/不完整的缺失证明归`REVIEW_UNCERTAIN_MATERIAL`，不归Candidate failure。字段实际存在却声明不可达会被拒绝；canonical owner、direct link、counterexample检查仍生效。

完整observe上下文不等于完整早前model history。Handbook/Skills/logs/summary等是否另有事实须按具体问题查精确既有输入；禁止把packet缺失当Agent输入缺失。校验器只核验显式标注及提供字段，不能机器证明来源文字为真，不是NLP语义分类器或live拦截器。旧post_run_audit numeric HiddenRisk计数仍是词面类别，不是新K1违规判定。

## Regression / scope

运行根解释器定向pytest：`test_s09_26_official_access.py`、`test_s09_23_cap_scope.py`、`test_s09_24_reviewer_reliability.py`：**287 passed, 2 deselected**。

- S09-25 canonical 69项矩阵直接引用，不复制第二份准入表；包含所要求state/event/choice/energy/delta/stock/ID/Handbook/Review/logs/DB/Dev prior/private Test类别。
- RUN16 a11 seq107官方`status_updates.HiddenRisk=1`在seq109行动之前：新policy **NO_K1_ACCESS_VIOLATION**；精确notes取自S09-25 provenance annex。不是整次动作最优/分数/未来adherence证明。
- 13个access对照含stock8、threshold10、raw DB、internal ID、private Test mapping、unknown access、官方禁令、一般prior与独立官方暴露的stock；不按名字禁用。
- RUN13 numeric-S/Level-cap仍4/4 EXPECTED；RUN14 bounded-state2/2 PASS；RUN15 safe selected candidates2/2 NO_VIOLATION；RUN12原始header negatives3/3 BLOCKED。
- 2项deselected仅是旧任务“current Candidate必须v10f、所有Skills不得改变”的身份冻结断言，本次明确准许替换；新测试独立约束v10g身份、四Skills、策略原文、Delivery、旧artifact和frozen资产，未削弱行为保护。
- 离线canonical package：`.local/runtime/s09-26-v10g/submission`，`skill_bundle` / exactly four Skills；manifest/Skill bytes与源码一致。没有install/reload。
- Manifest instruction **5402→5500 chars (+1.8141%)**；manifest file **7801→8180 bytes (+4.8584%)**；Planning **7787→7862 chars (+75)**。两种manifest度量均≤5%。
- C1–C10、One Master Ranking、Main/Energy controller、bounded probe/local NO_GAIN、K4/K5、五marker/BC/control原文及frozen Runner/framework/dependency/retry未改。全体新validation flags=false。
- `git diff --check`、selected delivery secret scan PASS；没有归档新raw证据/凭据/配置/DB。原RUN16 stop/receipt和FORENSIC_HOLD ACTIVE不变，旧结果不重写。

## Value of run / remaining uncertainty

见[refreshed gate](S09-26_VALUE_OF_RUN_GATE.json)：精确Candidate/package/tool/source身份及未来授权门限。

本次只证明静态规则与fixture校验通过。不能声称行为遵守、改善得分或正式Test全部权限已核验；完整当前官方禁令/hosted Test部署仍UNKNOWN。下一实验需Stage/Main接受并另行明确有限授权；本次不新增game预算。

Live/provider/service/game/MCP/DB/install/reload operations **0**。无新计分策略、mandatory logs策略、第五Skill、动态跨局memory或event-answer lookup。

```text
NEXT_GAME=NOT_AUTHORIZED
NO_REPLACEMENT_RUN_AUTHORIZED
MAIN_V8A_FREEZE_UNCHANGED
```
