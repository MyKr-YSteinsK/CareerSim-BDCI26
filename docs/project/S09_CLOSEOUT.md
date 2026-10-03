# S09 Closeout

## Stage result

`S09_CLOSEOUT_READY_FOR_MAIN`。Main 尚未决定 S09 COMPLETE。基线 `6359a09`，授权分支 `codex/s09-14-v9a-static`；本交付为 `IN_FLIGHT_EVIDENCE`，不冒充 MERGED_FACT。main 的 v8a freeze `6a4037fdf2b75c105cfe0b40b93ea68d3dd0a6f3` 未改变。

规范入口：[高价值证据](research/S09_HIGH_VALUE_EVIDENCE.md)、[机器摘要](research/S09_RUN_SUMMARY.json)、[对局索引](RUN_HISTORY.md)。这是 evidence compaction，live/provider/service/game=0，不做策略优化或新实验。

## What S09 proved

- 历史 mid-70 reference 存在：v6 75.29/48m/L6（runtime adherence FAIL但有效游戏证据），v7o71.83/48m/L5。
- v8a 同bytes RUN07 72.65 与 RUN08 59.00 支持真实分布差异／低尾盆地，不提供稳定概率或因果贡献估计。
- early promotion compounds descriptively；公开机会/context与可控结果兑现链都有差异。长期存活不等于高分，Health安全不等于信任安全。
- authored-policy 完美 adherence 不是有效成绩证据的必要条件；S1 record+continue 与 S2 invalidating stop分离。公开risk/result conversion重要，但局部prompt修正未建立稳定高分提升。

## What S09 did NOT prove

stable75+、stable80+、精确promotion/hidden-risk公式、v11/v11b优越、hidden-test transfer均未证明。RUN21 only partial M37；M6 HIGH_REFERENCE_LIKE / early feasibility CLEAN，不是final score或48m/75+验证。余额不足的上游根因来自用户／外部operator确认；Runner `max_continuations` 是proximate机制，技术中断不作策略失败证据。

## Best retained candidates / references

| 身份 | 用途 / 限制 |
|---|---|
| v8a frozen main | 官方submission fallback；未自动替换 |
| v11 / v11b | 实验lineage；RUN20完整60.60，RUN21 partial，未证明优越 |
| v6 historical | 75.29参考，非当前submission；旧runtime局限保留 |

## Routes to stop

结束 endless v11 micro-patching、Energy recipe policing作为主要研究路线、perfect semantic adherence优化、hidden threshold hunting、重复one-off Reviewer gates，以及 automatic RUN21 replacement。现行工程合同和可复用基础设施保留；不从阶段结论推导全部机制无用。

## Next-stage mandate

下一 Stage 可在新Plan中重新审视策略范式、Skill设计、structured memory的角色、较少/不同Skills、compact trajectory学习、systematic policy search/offline synthesis，以及有证据支持的架构假设。Team/Swarm仍需证据门，不自动采用。这里是后续规划建议，不授权实现、provider、service或新游戏；Main决定阶段接受与新权限。

## Evidence / cleanup disposition

- KEEP：全部canonical run records及其evidence，S09-25准入matrix/report、S09-27 Health、S09-32 basin、S09-16完整Review对照；active官方/runtime/Reviewer/submission合同、实现和fixtures。hold的精确来源／窗口／hash／owner／解除条件仍由这些保留记录承载。
- COMPACT：CURRENT_STATE恢复快照；RUN_HISTORY仅压缩S09，既有S01–S08 sections原文保留。
- DELETE：21份已吸收的过程资产：S09-03/08/10/14/15R/17/20/21/22/23/24/29/33静态过程报告及S09-34终止note；S09-15R/20/21/22/23/31/33过期VALUE_OF_RUN gates。各具体路径见本commit diff，可用 `git show 6359a09:<path>` 恢复。
- UNKNOWN→KEEP：S09-19有独立epoch去重反例，S09-28/31有独立场景／机制比较；不把未充分吸收的细节误当冗余。S09-17 gate仍被RUN11引用，S09-26 report仍被active runtime contract引用；均保留。STRATEGY_EVIDENCE没有S09章节，保留跨阶段原文，避免平行S09长摘要。
- 删除前检查每份文件的incoming references、独立来源价值和吸收位置：fresh-S/world-model/donor及prompt static结论在高价值证据lineage，runtime/Reviewer结论在active合同和canonical runs，S09-34余额确认和中止边界在新pack。无code/test消费删除文件，无唯一raw/hold指针删除；Git历史足以恢复过程验证细节。
- 不删除／迁移任何旧local runtime、raw、scratch，不解除FORENSIC_HOLD；本任务helper仅临时存在，验证后移除。hash或closeout READY都不等于Evidence Closure，hold仍待责任Main/Stage接受与显式解除。

## Verification boundary

9个代表outcomes及38行Review快照与保留规范来源核对；75个本地链接解析、删除文件全tracked文本incoming-reference检查、JSON parse、增量secret scan及`git diff --check` PASS。S01–S08原history sections逐段相同（忽略末尾空行）；Candidate/Skills/manifest/Runner/Reviewer/tooling/tests/dependencies以及全部run记录未改。未运行历史tests或live probe；STRATEGY_EVIDENCE原bytes保持。净tracked文件−18，只有三份新规范资产。

`NEXT_GAME=NOT_AUTHORIZED`

`NO_REPLACEMENT_RUN_AUTHORIZED`

`MAIN_V8A_FREEZE_UNCHANGED`
