# S09-17｜v10b C6 反饱和世界模型加固

## TASK_RESULT / identity

- Status：Complete，`IN_FLIGHT_EVIDENCE`，返回 Stage；不是 Main acceptance。
- Branch：`codex/s09-14-v9a-static`；base evidence：`678c161f70e8e7d01839d10de9868156c430ffec`。
- Candidate：`candidate-v10b-policy-constitution-anti-saturation`；parent：`candidate-v10a-policy-constitution`（implementation `0cecffd`）。
- 本次 implementation：`92fb4323c8db2e03fa3c12d0c2969ffdca6f6a4f`。
- 唯一 strategy delta：`ANTI_UNSUPPORTED_SATURATION_WORLD_MODEL_GUARD`。
- Decision：`S09_17_V10B_ANTI_SATURATION_STATIC_PASS_RETURN_TO_STAGE`。

## Actual change

只在 Planning Constitution C6 和 C7 之间插入一条430字符的高 salience guard：**Do not invent saturation.** 高数值、一次/少量 local NO_GAIN、近期停滞，不建立整个 durable-capital family “封顶 / 足够 / 无用”；无对应 participant-visible evidence 时保持 UNKNOWN。

允许 scoped explicit public upper bound/completion；某项认证完成不外推为整个 Skill family 无用。原 C6全文保留：局部NO_GAIN真实折价、known responsive高价值路径优先、其它多维/真实Delivery价值仍参与比较。新规则还明确不保证高数值继续增长，不强制学习/探索/重试。

Planning **7,498→7,928 chars**。去掉唯一新guard行后，全文与base normalized bytes完全相同，因此其它C1–C10、One Master Ranking、Main/Energy、POL/PROBE schema、bounded probe五条件、Level reset、MODE/recovery、Risk及executor接口均未改。没有增加mode、quota、ledger、Skill或Memory。

Identity-only metadata：manifest仅改name，instruction exact不变；current_candidate更新parent、manifest hash、Planning blob、delta及本次decision，九项validation flags全部false。v10a/v9a/v8a score/provider/gameplay evidence不继承。main/origin/main仍为v8a freeze `6a4037fdf2b75c105cfe0b40b93ea68d3dd0a6f3`；未更换submission。

## Verification actually passed

**86 passed / 2 deselected**，根 `.venv` Python；执行：

```text
D:/CS/CareerSim/.venv/Scripts/python.exe -m pytest -q tests/test_s09_17_anti_saturation.py tests/test_s09_15r_policy_constitution.py -k "not test_constitution_priority_one_ranking_and_regression_interfaces and not test_identity_hashes_and_no_evidence_transfer"
```

新48项：12个written scenario、33个词汇语义断言case、3个scope/全文regression/identity检查。既有38项包括20个controller counterfactual、trace positive/negative/ambiguous、invalid fail-closed、fresh响应GAIN/NO_GAIN/mixed、binding阻断、连续probe、header/full auditor及canonical packaging。保留原test/fixture文件不改。

两个deselected是历史v10a身份pin和7,500字符上限，由更严格的v10b身份、完整C6之外文本相等及430字符新增长度边界替代；没有跳过trace测量或削弱回归。

| Static scenario | Preserved written expectation | Result |
|---|---|---|
| Skill100，无公开cap | family saturation UNKNOWN | PASS |
| 高Skill且一次clean NG | local discount；不外推family | PASS |
| 同Level/context两次NG | stronger local discount允许，非dimension无用 | PASS |
| NG后Level change | reset/reopen UNKNOWN | PASS |
| 同Level新context后GAIN | 消费fresh响应，旧NG非永久冻结 | PASS |
| public certification完成 | 可停止对应opportunity，不外推资本family | PASS |
| Network高价值响应、Skill局部NG | exploit Network，不机械继续Skill | PASS |
| near real Delivery需要preparation | Delivery可赢 | PASS |
| acute binding threat | 最小必要保护可赢 | PASS |
| 无responsive替代、Skill未测 | 按原五条件进入comparison，不自动选择 | PASS |
| 高Skill仍responsive、Network较低 | 可继续Skill，无均衡配额 | PASS |
| Skill局部NG、strong ownership Main | ownership可赢 | PASS |

Vocabulary覆盖 capped、cap reached、saturated、enough、no longer useful、已封顶、已经够了、没必要再投入、这个维度无用了、到顶、已满。每词分别面对高数值、一次NG、近期停滞三种无充分证据basis：确定family断言不受支持；同词用于UNKNOWN允许；scoped explicit public completion允许。另验证public Health cap不外推Skill、认证完成不外推dimension、local NG仍支持local discount。

**验证边界**：词汇fixtures使用人工定义的scope/certainty/public support语义oracle，不是substring ban，也不是自然语言LLM输出classifier。12 scenarios是written-policy约束与反例审查；不模拟Candidate实际选择，不证明LLM遵循、收益、salience效果或hidden transfer。沿用measurement工具只能检验trace claims/数值响应，不能自动证明世界模型正确。

Board/Delivery/Risk及两个measurement tools、旧trace test/fixture physical bytes与before-task快照一致；protected Git blobs与parent一致。manifest instruction SHA=`79de9c4892311104967411d24b2a36597a7deaec4c42ada53b55c7173c8ea8f7`。Runner/pyproject/uv.lock不变，无 dependency sync。

## Required offline replays / package

RUN10 exact events SHA=`10fe7d3bc50f115a1bca02abed1afab2c63b605bc04a807a93a7f780b7710702`；UTC window `2026-10-01T16:17:59.610375+00:00`→`16:41:13.594450+00:00`。只读取既有exact events/transcript/score/receipt；无shared DB/provider查询，无raw改写。

- Legacy policy replay：actions201、trace coverage0、`STOP_BEFORE_PROVIDER`、全部核心metric null，**expected rejection PASS**。不得写成没有probe机会/0次机制触发，不能据此证明新delta。
- Full existing post_run auditor replay：原始Delivery valid0/201。
- Delivery header-only replay：NOT_NEAR regex201、空CTRL/DL separator201；原始valid0；只在内存中插入分隔空格counterfactual valid201。full auditor正/负synthetic paths也通过现有tests；未“修复”历史raw或放宽parser。历史RUN10实际执行physical auditor SHA仍未记录，不事后补造。
- Canonical `scripts.package_candidate.build_submission` + frozen Runner `validate_submission_contract`：`skill_bundle`、exactly4 Skills、manifest valid/name=v10b，包中Skill/manifest bytes与当前source对应；无install/reload/官方validate/live调用。

可重建local outputs：`.local/scratch/s09-17/submission/`、`run10-policy-replay.json`、`run10-auditor-replay.json`、`delivery-header-replay.json`、`package-validation.json`。新报告/gate只收身份及必要计数；raw来源继续既有FORENSIC_HOLD，不解除、不复制/归档。

## VALUE_OF_RUN_GATE refresh

[S09-17 gate](S09-17_VALUE_OF_RUN_GATE.json) 是当前v10b离线身份快照；旧S09-15R gate保留为历史。冻结implementation exact commit、metadata/manifest SHA及blobs、四Skill blobs/physical与LF SHA、Planning blob、instruction hash、post_run/policy_trace tools、旧fixture/test、新scenario/语义fixture test、canonical packager、dependency hashes、schema1、包文件hashes。

两个测量工具及旧fixture/test的完整identity与S09-15R gate一致；仅新Candidate/新test身份刷新。后续报告commit不改变这些source blobs。未来任何live Plan必须重新冻结其exact clean execution HEAD并核对包/tool执行bytes；当前gate不提供live权限。G5价值声明待Stage/Main review；世界模型遵循仍需真实public-context有界审查，trace只能提供claims。

## Durable state / risks / delivery boundary

CURRENT_STATE更新当前v10b static身份；不改架构决策或Project Brief。增量secret-pattern scan、JSON/identity/package一致性及`git diff --check`通过后push此授权分支。Candidate implementation与gate/report分两commit，是为冻结可恢复的exact source commit，非新branch/worktree。

剩余风险：LLM仍可能生成unsupported inference、漏trace或不能正确权衡真实Delivery；静态PASS不决定分数和RUN11价值。未来若因高数值/局部NG断言whole family无用，视为adherence失败；如果有对应explicit public cap/completion则合法。不得反向用“不推cap”强迫继续Skill或忽略NG。

Live game/provider/service/MCP/install/reload=**0**；旧授权不重开。`NEXT_GAME=NOT_AUTHORIZED` · `S09_RUN11=HOLD` · `MAIN_V8A_FREEZE_UNCHANGED`。

EXECUTION_METRICS：Model/Reasoning Effort/精确Started At/Finished At/完整Wall-clock=`UNKNOWN`；未以静态case耗时冒充完整任务耗时。EXECUTION_ISSUES：1次只读path assumption（误读不存在的agent_runtime.yaml，正确文件runtime_manifest.json）；无runtime副作用、无live budget消耗。
