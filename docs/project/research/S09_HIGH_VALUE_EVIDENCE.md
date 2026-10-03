# S09 高价值证据

基线 `6359a09`；授权分支 `codex/s09-14-v9a-static`，`IN_FLIGHT_EVIDENCE`。这是下一 Stage 的规范入口；原对局记录及来源身份仍保留。S09 收口待 Main 接受，不宣告 COMPLETE。

## 1. 代表对局

| Run / Candidate | Quantitative / partial | Survival | Final / last Level | Promotions | 保留价值 / 规范来源 |
|---|---|---|---|---|---|
| v6 / v6-auditable-control-loop | 75.29 / 52.7 | 48 | L6 | M6/M12/M18/M36/M48 | [历史最高已验证参考家族](../runs/v6-run1-validation.md) |
| v7o / v7o-execution-persistence-convergence | 71.83 / 50.28 | 48 | L5 | M6/M12/M18/M36 | [稳健 donor 参考](../runs/v7o-run1-validation.md) |
| RUN07 / v8a-v7o-donor-core-transplant | 72.65 / 50.86 | 48 | L5 | M6/M12/M24/M42 | [高参考轨迹](../runs/v8a-full-horizon-sample1.md) |
| RUN08 / v8a-v7o-donor-core-transplant | 59.0 / 41.3 | 48 | L4 | M12/M18/M36 | [低尾盆地](../runs/v8a-full-horizon-sample2.md) |
| RUN10 / v9a-adaptive-opportunity-capture | 68.4 / 47.88 | 48 | L5 | M6/M12/M24/M42 | [竞争性参考；新 probe 执行未确证](../runs/v9a-run10-full-horizon.md) |
| RUN17 / v10g-official-runtime-evidence-boundary | 24.47 / 17.13 | 6 | L2 | M6 | [Health 生存底线失败](../runs/v10g-run17-official-information-validation.md) |
| RUN19 / v10h-dynamic-survival-margin | 38.08 / 26.66 | 33 | L4 | M6/M12/M30 | [信任危机自然终止](../runs/v10h-run19-full-score-validation.md) |
| RUN20 / v11-result-conversion-risk-persistence | 60.6 / 42.42 | 48 | L4 | M12/M18/M36 | [v11 完整低尾参考](../runs/v11-run20-full-score-validation.md) |
| RUN21 / v11b-early-result-feasibility | UNKNOWN_NOT_TERMINAL / UNKNOWN_NOT_TERMINAL | NOT_VALIDATED | L4 | M6/M18/M30 | [M6 高参考相似；余额不足技术截断](../runs/v11b-run21-full-score-validation.md) |

RUN19 的 `VALID_NATURAL_TERMINAL_WITH_POLICY_VIOLATIONS` 是有效计分证据；底层为 EARLY_NATURAL_TERMINAL。RUN20 的 `VALID_FULL_RUN_WITH_POLICY_VIOLATIONS` 是48m完成。运行有效性与 authored-policy adherence 分开判断。

RUN21 最后公开观察 M37/L4，159 successes / 0 failures / 159 observes；fresh pairs158/159，最后成功动作后没有观察。M6 HIGH_REFERENCE_LIKE，early feasibility CLEAN（至少一条公开路线的有界标准）；final score / 48m / 75+ NOT_VALIDATED。`max_continuations` 只保留为 proximate mechanism。上游余额不足来自用户／外部 operator confirmation；S09-34 曾观察本机 HTTP402 元数据但未提交 raw，不冒充新增 repo-native proof。任务终止决策为 `S09_34_OBSOLETED_BY_EXTERNAL_PROVIDER_BALANCE_CONFIRMATION_RETURN_TO_STAGE`；不继续 boundary 根因调查、不建议自动补跑。

## 2. Review 轨迹样本

以下统一用**首次携带正式 Review 的 fresh public observation**。RUN07 原 run note 的表是 Review 月末；这里使用 [S09-16 派生数据](../reviews/S09-16_FULL_HORIZON_EVIDENCE.json) 的 first 字段，不能把同月后续 Energy/Main 算入先前晋升原因。RUN20/21 使用各自规范 evidence JSON。S/N/O/W 为公开状态，不是隐藏晋升公式。

### RUN07

| M | Grade | Level after | Promotion | S/N/O/W |
|---|---|---|---|---|
| 6 | C | L2 | YES | 9/3/3/2 |
| 12 | B | L3 | YES | 21/4/6/3 |
| 18 | B | L3 | NO | 41/11/15/5 |
| 24 | B | L4 | YES | 42/19/15/9 |
| 30 | B | L4 | NO | 59/26/26/14 |
| 36 | B | L4 | NO | 81/36/25/19 |
| 42 | A | L5 | YES | 100/34/24/24 |
| 48 | B | L5 | NO | 117/53/32/34 |

### RUN08

| M | Grade | Level after | Promotion | S/N/O/W |
|---|---|---|---|---|
| 6 | C | L1 | NO | 9/3/2/3 |
| 12 | C | L2 | YES | 9/3/3/3 |
| 18 | B | L3 | YES | 21/4/6/5 |
| 24 | B | L3 | NO | 41/21/8/8 |
| 30 | B | L3 | NO | 42/21/13/12 |
| 36 | B | L4 | YES | 42/19/15/15 |
| 42 | A | L4 | NO | 59/33/26/23 |
| 48 | A | L4 | NO | 77/36/26/27 |

### RUN10

| M | Grade | Level after | Promotion | S/N/O/W |
|---|---|---|---|---|
| 6 | C | L2 | YES | 9/3/3/2 |
| 12 | B | L3 | YES | 21/4/5/2 |
| 18 | B | L3 | NO | 38/19/12/5 |
| 24 | B | L4 | YES | 42/19/16/8 |
| 30 | B | L4 | NO | 62/35/20/13 |
| 36 | B | L4 | NO | 84/36/24/18 |
| 42 | A | L5 | YES | 93/34/24/27 |
| 48 | B | L5 | NO | 111/48/38/31 |

### RUN20

| M | Grade | Level after | Promotion | S/N/O/W |
|---|---|---|---|---|
| 6 | C | L1 | NO | 9/3/2/2 |
| 12 | C | L2 | YES | 9/3/3/3 |
| 18 | B | L3 | YES | 20/4/6/6 |
| 24 | B | L3 | NO | 39/17/6/10 |
| 30 | B | L3 | NO | 42/20/13/13 |
| 36 | B | L4 | YES | 42/19/16/13 |
| 42 | A | L4 | NO | 59/36/26/21 |
| 48 | B | L4 | NO | 76/36/22/28 |

### RUN21

| M | Grade | Level after | Promotion | S/N/O/W |
|---|---|---|---|---|
| 6 | C | L2 | YES | 9/3/3/2 |
| 12 | C | L2 | NO | 21/7/4/4 |
| 18 | B | L3 | YES | 21/7/5/6 |
| 24 | B | L3 | NO | 37/21/8/11 |
| 30 | B | L4 | YES | 42/18/16/9 |
| 36 | A | L4 | NO | 64/33/24/14 |

RUN21 M42/M48 NOT_REACHED。最后 M37 state H10/D10/S67/N36/O25/W17；这是最后观察值，不是最后成功动作后的已验证状态。其他代表终局值见 [机器摘要](S09_RUN_SUMMARY.json)；v6 report 的 ending-score components 不冒充完整 final public-state snapshot，缺失字段 UNKNOWN。

## 3. 可复用的派生发现

### Early compounding｜描述性，非唯一因果

[S09-32 report](../reviews/S09-32_EARLY_BASIN_DIVERGENCE.md) / [aligned evidence](../reviews/S09-32_EARLY_BASIN_EVIDENCE.json)：RUN20/RUN08 basin similarity HIGH，root cause MIXED；M6 early-promotion compounding STRONG_DESCRIPTIVE。公开机会/context variance material，但同输入晋升随机差异 UNKNOWN。最强可控对照是公开成果可兑现性与 delivery chain 差异。M5 最后动作后的 Review 状态与 M6 后续投入要分开。没有固定 O 阈值、唯一晋升条件或已证明改选收益。

### Survival / Health

[S09-27 report](../reviews/S09-27_FAILURE_FLOOR_FORENSICS.md) / [trajectory](../reviews/S09-27_HEALTH_TRAJECTORY.json)：隔离单步 H drop −1=329、−2=54、−3=1、≤−4=0 observed；0 observed 不表示不可能，切月/Review 结算也可能贡献 delta。锁定包 Health≤0 terminal；官方 safe buffer UNKNOWN，该实现事实不自动成为 Agent 输入。高分局可在低 H 后遇合法窗口恢复，但低 H 幸存不证明安全。固定 H 阈值被拒绝；fresh 余量、广告成本、公开负荷、不确定下行与实际可达恢复的动态比较有依据，尚未证明稳定得分收益。RUN17 a22高密度带教 H3→1、a23无恢复菜单 H1→0；a22前可能可避免，反事实是否救活 UNKNOWN。

### Information access

[S09-25 audit](../reviews/S09-25_INFORMATION_ACCESS_AUDIT.md) / [matrix](../reviews/S09-25_INFORMATION_ACCESS_MATRIX.json)，及 [S09-26 准入修正](../reviews/S09-26_OFFICIAL_RUNTIME_EVIDENCE_BOUNDARY.md)：官方 `choices[].status_updates`（含 HiddenRisk delta）是可达输入；advertised delta ≠ realized response ≠ hidden stock。RUN16 a11 的缺失输入断言因 Reviewer projection 丢 effects 而被反驳，历史停局不改写，不等于官方规则违例。原则：`TEST_AGENT_ACCESSIBLE + NOT_OFFICIALLY_PROHIBITED => ELIGIBLE_FOR_STRATEGY_RESEARCH`。不可达隐藏 stock/counter、raw DB/private Test 与精确隐藏公式仍禁止；不能累积 delta 重建库存。早期 donor 的旧 firewall 判定须按当时合同读，不据此抹除真实成绩。

### Risk / trust

cleanup action ≠ clearance；一般成功、HR praise、无新 warning 不证明同 scope 风险解除。[RUN19](../runs/v10h-run19-full-score-validation.md) 的公开信任时间线及 [evidence](../runs/v10h-run19-full-score-evidence.json) 保留：M6已有风险提示，后续 warning/责任处理链至 M33 second explosion / trust exhausted，H9仍自然终止；Health 保护不等于 overall failure floor。[RUN20](../runs/v11-run20-full-score-validation.md) M28/M46 generic HR praise 被当作清除，[RUN21](../runs/v11b-run21-full-score-validation.md) 也有 premature clearance。没有支持隐藏风险 counter/threshold；v11 的同 scope 持续风险合同未保证模型执行。

### Result conversion / Delivery

Review 的 result/highlight deficits 有描述性价值；generic Output/reporting ≠ verified result。RUN20 D1跨8次Review仍 IN_PROGRESS/UNVERIFIED；RUN21 a46起同 D1持续114次，跨5次Review仍无确认结果/recognition。stale item 没证明可靠控制价值，当前 Delivery machinery 的得分收益未证明。RUN10 旧 parser拒绝与策略收益分开：相邻 CTRL/DL separator 的离线适配能修复解析，不证明旧动作 lifecycle 或 counterfactual gain。S09-15R 的该 root correction由此吸收；各 run 的历史 parser verdict 保留。

### Model semantics / runtime / Reviewer

Energy recipe、lowest-stat 和 unsupported cap drift在多次prompt加固后仍出现；fresh tool pairing不证明fresh ranking，BC=PASS不证明语义通过。v6 已有有效75.29但 runtime adherence FAIL，不能将完美policy adherence作为首要得分目标。S09-03/08 的 fresh-S续期／世界模型纠偏、v10 的 anti-cap、kernel/头部/依据证书都仅有静态覆盖，不证明稳定得分提升。可见 compression trigger 的 epoch去重限制见 [S09-19](../reviews/S09-19_COMPACTION_RECOVERY_HARDENING.md)，其独立反例保留。

现行 [Reviewer contract](../REVIEWER_GATE_CONTRACT.md) 与 launcher 保留：v3 S0 continue / S1 record+continue / S2仅独立有效的run-invalidating evidence可stop；FULL_SCORE_EVALUATION默认，exact Candidate/session attribution必须。快照延迟、M6 relay延迟及未实际演练的S2 stop不能伪装可靠性通过。S09-24/29 的过程结论由现行合同、[S09-30 integration](../reviews/S09-30_LIVE_CONTROLLER_V3_INTEGRATION.md) 和 RUN19–21 evidence 承载。技术中断、历史机制censor与策略自然失败分开；RUN21余额不足不是策略失败。

## 4. 简化 lineage / Stage 结论

| Generation | 主要假设 | 最佳有效证据 / 限制 |
|---|---|---|
| v8a | 直接移植 v7o donor-core，删除层叠 ranking，保留四Skill执行接口 | RUN07 72.65；相同bytes RUN08 59.00。高低尾差异真实，未建立稳定75+ |
| v9a | responsive exploitation之外有界比较未测试高价值机会 | RUN10 68.40；qualifying new-delta execution未确证，不能声称已证无效或有效 |
| v10* | constitution / anti-saturation / compression常驻kernel / preflight，再到官方准入与动态余量 | 多次技术/机制截断；RUN17已M6晋升但Health失败；RUN19信任失败。prompt/static通过不保证模型/生存执行 |
| v11 | 成果兑现、持续风险、stale Delivery降权、单步Energy简化 | RUN20 60.60/48m/L4；低尾盆地未突破，premature clearance/recipe仍有 |
| v11b | 首评前公开成果可兑现性与局部realized-response重排 | RUN21 M6高参考相似、early feasibility CLEAN；M37余额不足技术中断，完整结果未验证，不能证明v11b优越 |

S09 未建立稳定超过既有 mid-70 references 的策略；反复局部 prompt hardening 边际收益下降。这个结论不表示全部机制无用：公开准入、fresh-state纪律与明确有效计分证据仍应保留。规范下一决策见 [S09_CLOSEOUT](../S09_CLOSEOUT.md)。现有 raw FORENSIC_HOLD ACTIVE；owner/来源/窗口/hash/解除条件仍在各 retained run/derived report，不因摘要或Git可恢复而解除。

`NEXT_GAME=NOT_AUTHORIZED` · `NO_REPLACEMENT_RUN_AUTHORIZED` · `MAIN_V8A_FREEZE_UNCHANGED`
