# S09-RUN12｜v10c 首次验证：M1 H1 合同中止

## Identity / pre-provider

- `IN_FLIGHT_EVIDENCE`；授权分支 `codex/s09-14-v9a-static`；execution HEAD `0678e3c4fd7f30e52e52a016216ad2607c3df172`，clean。
- Candidate `candidate-v10c-compaction-agnostic-kernel`，implementation `55157f53031c284e2e569944e4aff6adbf64c48f`，parent v10b。
- P0：用户在余额问题后明确确认“我已确认，直接开始”；G1–G5 PASS。重跑43项 kernel/replay和17项严格trace检查，offline package=`skill_bundle`/exactly four，bytes 匹配 S09-20 gate；未单独 install。
- Runner `f61c738c72e51b77298cc1c14c7c6ebf4b6c527d`、dependencies、retry=2 未改。工具/fixtures/package/四 Skill identity 在运行前后匹配；具体 hashes/Planning blob 见 [compact evidence](v10c-run12-early-contract-evidence.json)。main/origin/main 保持 `6a4037fdf2b75c105cfe0b40b93ea68d3dd0a6f3` v8a freeze。
- 独占/PATH/一次 bare `--list` exit0/stopped/四端口 gate PASS。一次 service start readiness **17.25s**，上限120s；一次 Runner play/fresh game。授权在 play 启动时 CONSUMED。
- Startup 四个 `skill_tool` activation按 Board→Delivery→Planning→Risk 顺序观察到；不是 read_file，不能把 read_file count0 写成四 Skill 没有加载。

## Heartbeats / actual stop

**Classification=`DEVELOPMENT_CENSORED_EARLY_CONTRACT_ABORT`。**

- H1 **FAIL**：前三次成功动作后，fresh observe **3/3**，但 canonical five-marker full header **0/3**；按 Plan §3 H1 自动停止。
- H2/H3 **NOT_REACHED**；没有 M6/M12/M18/M24 绩效 censor。
- 3 attempts / 3 success / 0 fail，4 observes，unique new_game=1（events含重复帧，已按tool call ID去重）。没有第4次 gameplay action。
- 全部 M6/M12/M18/M24/M30/M36/M42/M48 checkpoints NOT_REACHED；promotion=none observed。
- 最后公开状态：M1/L1，H4/D8/W1/S3/N4/O0/E3，alive=true/failed=false。structured game.ended 未观察到。
- quantitative/partial/final grade=`UNKNOWN`；survival_months=`NOT_VALIDATED`；L1是截断状态，不是自然终局 Level。这不是 survival regression、48m completion、Provider failure或最终低分。

## Contract / diagnosis

| Contract | Original submitted evidence |
| --- | --- |
| CTRL present / accepted at notes start | 3/3 present；**0/3 anchored valid** |
| DL regex / full header acceptance | 3/3 regex；0/3 header acceptance |
| POL / PROBE / BC=PASS | 3/3 each, enums and probe consistency valid |
| Full five-marker contract | **0/3** |
| Duplicate markers / submitted BC=BLOCKED | 0 / 0 |

三次 action notes 均先写公开理由及 PLAN/CANDIDATE，然后才出现 `[CTRL ...] [DL ...] [POL ...] [PROBE ...] [BC=PASS]`。冻结 `CTRL` parser 以 `^` 锚定 notes 开头，故实际 header 均拒绝。

离线只在内存取原 notes 的 `[CTRL` 起始后缀，三条 header 都可被**同一未改 parser**接受。该诊断表明前导 prose 是充分解释本次 header rejection 的格式因素；原始 notes 不改、不回填为 valid，也不放宽 parser。

**FACT：** S09-20 manifest明确要求按序 markers，却未保留父 manifest 的“notes 开头必须”措辞。Planning 的 trace ownership移交也没有补这项显式位置要求。**INFERENCE：** ownership transfer 后 notes-prefix要求显著性不足是候选修复点；本局不证明加一句话即可修复实际模型行为。

三次 `[BC=PASS]` 都未捕获此布局错误，说明 BC 自报不等于 frozen-parser readiness。`KERNEL_ADHERENCE=FAIL`，限定为 preflight layout；不能据此声称全部K1–K5语义失败。service log有kernel文本，但本次未建立逐call完整model-input capture匹配；不宣称完整system instruction在每个call的动态持久性已验证。

## Strategy / 75+ runway / comparison

- 三次均为Story/开局事件：没有 Main/季度Energy，public NO_GAIN routing、响应成长路径比较、bounded probe、保护及cleanup NOT_EXERCISED。notes内部 MODE=A三次；原anchored auditor MODE=UNKNOWN三次，不能把两种口径混为一谈。
- POL/PROBE值为输出主张；主审计因header失效拒绝measurement readiness，probe总量保持UNKNOWN，不能伪造可测的零总量。
- restricted/saturation/numeric-S/stale-cleanup/summary-authority的完整语义审查 `NOT_FULLY_EVALUATED_DUE_TO_H1_ABORT`；没有H2/H3通过结论。
- M36/M42/M48状态、资本Δ、responsive Energy share及conversion chains均未覆盖；`PROMOTION_RUNWAY_EVIDENCE=INCONCLUSIVE`。Score Ceiling与Failure Floor都NOT_EXERCISED；不把主动合同中止解释为游戏损失。

| Prior sample | Observed outcome | Bounded comparison with RUN12 |
| --- | --- | --- |
| [v8a RUN07](v8a-full-horizon-sample1.md) | 72.65 /48m/A/L5 | 有完整跑道；Delivery layout历史拒绝0/203，本局是不同的前导prose拒绝，不能比较得分 |
| [v8a RUN08](v8a-full-horizon-sample2.md) | 59.00 /48m/C/L4 | Delivery205/205；证明输出格式有变异，不证明本局修复有效 |
| [v9a RUN10](v9a-run10-full-horizon.md) | 68.40 /48m/B/L5 | Delivery0/201为separator问题，未建立完整probe trace；本局不放宽parser掩盖另一个layout边界 |
| [v10b RUN11](v10b-run11-first-validation.md) | M45 Provider402截断；无终局分数 | CTRL/DL183/183、POL/PROBE48/183；本局仅3次且header0/3，长期稳定性无比较依据 |
| v10c RUN12 | M1 H1合同中止；无终局分数 | BC与POL/PROBE存在，但canonical placement未通过；75+机制未覆盖 |

差异首先是execution/format边界；strategy ceiling不可判。`V11_CREATION_FROM_RUN12=NOT_SUPPORTED`，本局不支持 Promotion-Ready Capital Conversion delta。返回Stage评审显式notes-leading合同/negative-prefix fixture；不在本任务patch或rerun。

## Runtime / cleanup / evidence

- UTC window `2026-10-02T11:09:35.952550+00:00`–`2026-10-02T11:10:19.660578+00:00`，play wall **43.708s**。
- Input/output/total tokens、billed cost UNKNOWN；无可靠completed usage。Provider异常 NONE_OBSERVED before controlled abort；不据此当整局provider validation。
- Preflight/session/H1/cleanup进度从现有stdout报告；interactive session，额外报告query=0；未修改live choices，只有Plan授权的H1 stop。
- Runner终止 exit1；graceful stop exit0、manager PID file absent、19092/20000/20001/6173 listeners全部释放。service-start wrapper exit1为既定stop-tail limitation，不推翻本局三次动作。
- 一次post_run_audit在cleanup后执行，exact artifacts/window/+08:00，无DB/Provider/service查询。冻结audit把非终局非零exit归`PARTIAL_GAMEPLAY_TECHNICAL_FAILURE`；它没有H1分类。本报告保留该原始字段，同时以明确controller stop receipt分类，未patch parser。
- 精确events/transcript、runner result、preflight/H1/controller、service/runner/stop logs、一次post_run_summary路径/bytes/hashes见compact evidence；raw仍本地ignored，不归档完整service log、config、shared DB或凭据。
- **FORENSIC_HOLD=ACTIVE**：Stage/Main责任/解除；原因是H1 layout与BC false-positive需独立接受、明确是否仍需原始context。接受结论、子任务依赖解除并确认必要来源可恢复后，仍需明确cleanup授权；本任务不清理、不解除旧hold。
- Candidate/Skill/manifest/measurement tools/dependencies/Runner/package未改；validation flags保持false，没有完整gameplay/runtime/score收益证据。

```text
Decision=S09_RUN12_EARLY_CONTRACT_ABORT_RETURN_TO_STAGE
S09_RUN12_GAME_AUTHORIZATION=CONSUMED
NEXT_GAME=NOT_AUTHORIZED
NO_REPLACEMENT_RUN_AUTHORIZED
MAIN_V8A_FREEZE_UNCHANGED
```
