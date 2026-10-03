---
name: career-state-brief
description: "Use after fresh observe or visible same-session recovery. 整理公开事实、Review、真实承诺/成果、未解除约束和局部响应；维护五组 conversation-resident Career Brief 的当前逻辑版本。只管理事实与摘要，不排序、不选动作、不独立做风险门禁、不提交。"
---

# Career State & Brief｜同局事实与职业摘要

## 职责与事实权威

当前 Single Agent 是唯一执行器；本 Skill 只维护事实与 Career Brief。目标调整由 `career-decision` 提出，本 Skill 将有公开依据的调整写入同一份 Brief，不维护平行计划或结果账本。**Can Submit Action: No.** 不调用 `new_game`、`observe` 或 `take_action`；不排序候选、不选最终动作、不独立做安全门禁。

最新同局 fresh observe 是当前状态与合法菜单的权威。H/D/S/N/O/W/E 等实时值直接读取，保留原值/精度；Brief 不复制完整状态，不用旧观察、工资、notes 或广告效果推算缺失值。字段缺失、归因混杂或来源不明记 `UNKNOWN`。只用当前 session 的 participant-visible 观察、正式反馈、手册、合法菜单、结果及必要同局官方日志；日志里的模型 notes 不是独立证据。

## 三类证据

- `ADVERTISED_CONFIGURED_DELTA`：官方 MCP 在当前 participant-visible tool response 的合法 choice 中直接返回的 `status_updates / effects`，可含精确 `HiddenRisk` delta；只说明该选项的配置/广告代价与收益，不是当前 hidden stock、实际状态或保证结果。未返回的字段不猜测，正常用菜单语义和已知公开事实决策，不因缺字段阻断整局。
- `REALIZED_PUBLIC_RESULT`：fresh observe 中真实公开状态或明确 item-linked 完成/认可。action success receipt 只证明工具执行，不证明职业成果。advertised delta 不能更新 current state；动作后必须 fresh observe。若不一致，记 `ADVERTISED != REALIZED / CAUSE UNKNOWN`。
- `UNKNOWN`：无法证实的状态、成果、原因与约束解除；不能因没有新 warning、generic praise、普通 promotion 或无关正面事件就变成已完成/已清除。

禁止 hidden stock/counter reconstruction、累积 deltas 估算隐藏存量、私有 DB/raw Test、内部 IDs、解码私有 Test 映射、hidden formula/exact threshold/cap reconstruction、跨局 learned memory 与 event→answer lookup。Story 未在工具回包返回的内部效果不能当事前输入。可见 delta 不推断失败概率或当前风险总量。

## 一份五组 Career Brief

选用 `CONVERSATION_RESIDENT`：同局对话中的最新完整版本是当前逻辑摘要，明确 supersedes 旧版本；旧对话没有物理删除，durable persistence 未证明。首次同局 fresh observe 后初始化，session 改变立即丢弃整份旧 Brief、重新初始化；绝不依赖其它局、`MEMORY.md` 残留、本机路径或隐藏存储。

```text
SESSION_BASIS: 当前 game_session_id；最新已核验公开观察的月份/Level/context scope
REVIEW_OBJECTIVE: 最新正式反馈（无则UNKNOWN）；一个当前目标；一个公开检验点/依据
RESULT_COMMITMENT: 重要真实承诺/成果；公开deadline/依赖（缺则UNKNOWN）；verified或unverified及依据；下一现实兑现机会
UNRESOLVED_CONSTRAINT: material同scope风险/约束及公开依据；什么公开证据才可解除（不明则UNKNOWN）
PATH_UPDATE_STOP: 当前Level/context最近相关已测responsive/stale路径与clean realized依据；停止或重验什么
```

Bound：始终只有这五组当前摘要，不追加逐动作历史或每个 NO_GAIN；每组只保留未来决定所需的短事实、来源与未解问题。最重要成果写具体内容与证据，其他仍未履行的真实义务压缩在同组中保留，不为了简短静默删除。无需 item cursor、阶段状态机或 per-action marker。无法确认 deadline 就不虚构“快到期”；没有正式反馈时允许以 broad growth/visible result 为目标，反馈仍 UNKNOWN。

## 更新与失效

初始化、material checkpoint 的 Deep Review 后、恢复时输出一份完整新 Brief，明确“这是该session当前版本，supersedes先前版本”。普通 action 不全量输出 Brief；fresh observe 只更新变化的结果/约束/path事实与 SESSION_BASIS 核验锚，当前逻辑版本由最近完整版本加后续有依据的字段替换组成。

- 新鲜事实与摘要冲突时，fresh observe 优先；目标已完成/不可行或公开检验点失效时，由 Decision 重排后替换当前目标。
- Level 改变时清除原 Level 的 tested-path判断；context/菜单或相关条件变化时重验，不把旧 NO_GAIN 当永久 cap。
- clean response 只限紧邻 action→fresh observe，且无 Review/promotion/salary/延迟结果等混杂；只更新该动作确实涉及的维度和已测 action family。正向实际增长可覆盖旧 NO_GAIN；混杂、未测与缺证据均 UNKNOWN。局部无增益不折价未测试 family 或该动作其它维度/ownership价值。
- 同 scope trust、Health/safety、job continuity、financial/income、compliance/confidentiality 等 material 约束持续保留，只有相关公开解除证据或风险承载场景确已结束才清除；一次 cleanup、generic praise、无新 warning 不证明解除。继续保留风险不等于每步重复 cleanup 或永久停止成长。
- 跨 Review 没有新证据的旧成果，要重验未来价值与可兑现性；不因旧标签仍在就继续投入，也不因时间经过就抹掉真实未了义务。verified result 不重复包装。
- 以同一公开 Review/结果/警告内容及其 scope 去重 material checkpoint；SESSION_BASIS 与相关事实保留已处理的依据，不另建 checkpoint ID 或计数器。普通观察重复同一已处理反馈不重复 Deep Review。

## Recovery

仅在实际可见的 resume/compaction/recovery signal 或明确无法可靠恢复当前摘要时重建；不能声称能检测 host 未暴露的 compression。

执行器确认同一 session→fresh observe→重读两个职责文档→用新观察和必要的最小同局官方 `check_latest_logs` 窗口核验/重建五组 Brief。压缩摘要、旧 Brief、旧 action notes 都是待核验的历史线索，不是 fresh public truth；缺失/损坏/冲突字段 UNKNOWN，无法核验的旧内容丢弃。不要 dump 全局历史来找“答案”。

无法确认 session、fresh observe 或文档读取失败时不动作；历史目标/成果等缺失可保留 UNKNOWN 并从当前合法事实重新决策，不无限请求日志。恢复完毕只恢复摘要，不授权 action；提交前执行器仍须基于当前 fresh 同局状态完成一次新的合法选择与最终安全检查。
