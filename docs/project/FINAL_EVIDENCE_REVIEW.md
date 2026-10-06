# 最终证据审阅｜Final Evidence Review

本文件是 S11 的精简 canonical evidence layer（权威证据层），根据 `main@78b9aa531117a2af8ae5650c9dfdc7c41728cfa4` 的已跟踪记录整理。S11 仍为 `ACTIVE`。本文保留具有决策价值的代表性结果，不替代完整的 run/review/research 原件，也不授权删除历史来源或解除 `FORENSIC_HOLD`。

S11-15 已从当前树移除六份被吸收的 S10 过程门审查文件；对应 research 来源和结果记录提交仍可从 Git history 恢复。本台账中的 hold 未因该次清理而改变。

## 解释规则

- **FACT** 仅记录对应来源直接报告的身份、数值、事件和状态；**INFERENCE** 仅用于有限的跨记录解释；缺失或未复核的信息标为 `UNKNOWN`。
- 单局结果只描述该 Run。不同 Candidate、随机轨迹或不完整来源之间不构成因果对照；少量样本的范围、均值和完成率是描述统计，不代表性能分布或稳定性证明。
- `quantitative`（量化分）、`competition partial`（比赛局部得分）、survival（存活时长）、grade（评级）、Level（职级）和 promotions（晋升）按来源记录分别列出。未到终局的技术失败不补造终局分数或评级。
- Display ID 是导航编号，不替代 Stage / Task / Candidate / Run 身份。来源 commit 与记录 commit 分开列出；raw 的 hash 不能替代 raw，也不能关闭 hold。
- 最终冻结身份仍为 exact historical `candidate-v6-auditable-control-loop`，来源 `1114a04b75548cf52f030d123564e527060fc061`，Single Agent + 3 Skills。当前 checkout 中的 v8a / four-Skill 文件不是该提交包身份；ZIP SHA-256 为 `31e836b591703dfe520916828da033a57de260bb451d97047bbaee9daaa11b9b`。官方上传和平台评测均未发生。

## 代表性运行记录

| Display ID / 历史身份 | Candidate 与来源链 | 观测结果 | 保留理由与边界 | 证据与留存状态 |
|---|---|---|---|---|
| `RUN-0003` · S01-03 baseline | S01 minimal no-op harness，`baseline-placeholder` Skill；冻结 Runner `f61c738c72e51b77298cc1c14c7c6ebf4b6c527d`；历史记录包 `031d97e56e0ce305a487b4bc293c7abde58cfdf0` | `26.95 / 18.86 / 19m / E / L3`；提前终止；promotions 为 `UNKNOWN` | 建立项目真实的 no-op 起点。这是 baseline loop 结果，不证明后续策略造成了提升。 | [运行历史](RUN_HISTORY.md)及 `git show 031d97e56e0ce305a487b4bc293c7abde58cfdf0:experiments/S01-03-baseline/RESULT.md` / `score_report.json`。历史 score report 的 SHA-256 为 `f84598d1df614131f90362a9f3ea83ebe381f5c5b755922187f4868d59b07686`。该结果未声明正式 hold 状态；本文不据此主张当前 hold 状态。 |
| `RUN-0001` · S06-24 v6 Run #1 | `candidate-v6-auditable-control-loop`；source `1114a04b75548cf52f030d123564e527060fc061`；validation record `40589e35564e6c3822851586c7192b7089183722`。冻结 manifest SHA-256 `bcf459da811f55b8a26a76d2ee6e93da10deb4b720cc732d19a3ce12d8fa2985`；三个 Skill blob ID 见[最终身份](FINAL_SUBMISSION_IDENTITY.json)。 | `75.29 / 52.70 / 48m / A / L6`；在 M6、M12、M18、M36、M48 观测到晋升；`VALID_48M_COMPLETION` | 入选最终 Candidate 的高位参考，也是记录比较中已观察到的成熟三 Skill 最高分。只有一个样本；记录为 `RUNTIME_ADHERENCE_FAIL`（包括被拒绝的 Energy 多选，以及两次压缩后未按要求重新读取三个 Skill）。不证明稳定表现、因果收益、理论最优或迁移能力。 | [v6 验证记录](runs/v6-run1-validation.md)和[S10-23R 冻结审计](reviews/S10-23R_FINAL_SINGLE_SHOT_FREEZE.md)。支持性 raw 保存在本机、未提交，见 [CURRENT_STATE](CURRENT_STATE.md)；其正式 raw-hold 状态为 `UNKNOWN`，不能写成“无 hold”。 |
| `RUN-0002` · S09-RUN08 v8a 样本 2 | `candidate-v8a-v7o-donor-core-transplant`；run base `a3b6cd57223ba4d79b26b4a77f724f33fa72f275`；记录 `4fb189209595e4733521c45c46099e18d570296d`。与 RUN07 具有相同冻结行为身份。 | `59.00 / 41.30 / 48m / C / L4`；在 M12、M18、M36 晋升；自然结构化完成 | 是本记录所含两局完整周期 v8a 样本中较低的一局，可防止把单次好结果说成稳定表现；它不是最终 Candidate 评估。 | [S09-RUN08 报告](runs/v8a-full-horizon-sample2.md)。本机证据为 `FORENSIC_HOLD=ACTIVE`，见 hold 台账。 |
| `RUN-0004` · S09-RUN07 v8a 样本 1 | 与 RUN-0002 为同一 Candidate 和冻结行为身份；run / report commit `a3b6cd57223ba4d79b26b4a77f724f33fa72f275`。 | `72.65 / 50.86 / 48m / A / L5`；在 M6、M12、M24、M42 晋升；自然完成 | 与 RUN-0002 配对后可见同一 Candidate 的强结果和明显样本差异。该局有未解决的 runtime / evidence-discipline 发现，因此不属于干净的遵循结果。 | [S09-RUN07 报告](runs/v8a-full-horizon-sample1.md)。本机 raw 为 `FORENSIC_HOLD=ACTIVE`，见 hold 台账。 |
| `RUN-0005` · S08-RUN02 v7q Run #1 | `candidate-v7q-checkpoint-marginal-progression`；run base `0a7001e67fc4350383382039d592a2b0ceb2b964`；修正后的记录 `94b6acf771442cc3435af6ac1a43c25c9722bd5d`（首次集成 `31c0501249ab4be6a82c3346039290b291fc80ef`）。 | `26.80 / 18.76 / 24m / E / L1`；M6/M12/M18 均为 C 且无晋升；M24 自然终止 | 归属明确的自然提前终局和低位结果样本。未观测到 L6、M36–M48、runtime / recovery 遵循情况或任何策略效果。 | [v7q 验证记录](runs/v7q-run1-validation.md)和[归档证据 manifest](../../artifacts/dev-runs/s08-run02-v7q/evidence-manifest.json)。本机原件仍为 `FORENSIC_HOLD=ACTIVE`，见 hold 台账。 |
| `RUN-0006` · S07-46 / S07-47 v7m 部分技术失败 | `candidate-v7m-final-r-recovery-audit-hardening`；source `e0d92ab720395894ce6a109c424bc92ef393010c`；运行记录 `9faf202174c165899837e4f881afd0bcc40e0cdd`；离线 forensic review `fee5b1de5052a0285d934e77d2073abb6cffc654`。 | 没有最终分数、局部得分、最终评级或自然终局。最后一次 fresh observation 为 M20 / L3，角色仍存活；84/84 次动作成功；在 M12 和 M18 观测到晋升。Runner 以技术失败结束，分类为 `INSUFFICIENT_EVIDENCE`。 | 作为高价值的部分运行和审计恢复案例保留：说明如何报告有用的局中事实，而不虚构终局结果。不证明最终分数，也未确定传输故障原因。 | [v7m 运行记录](runs/v7m-run1-validation.md)、[S07-47 forensic review](reviews/S07-47_V7M_M20_PARTIAL_RUN_FORENSIC_REVIEW.md)和[归档证据 manifest](../../artifacts/dev-runs/S07-46-v7m-run1/evidence-manifest.json)。本机失败与恢复来源仍为 `FORENSIC_HOLD=ACTIVE`，见 hold 台账。 |

### 样本分布与最终选择对比

| 证据 | 概要 | 决策边界 |
|---|---|---|
| v8a S09-RUN07 / RUN08（`RUN-0004` / `RUN-0002`） | 同一冻结四 Skill Candidate；quantitative 分为 `72.65` 与 `59.00`，范围 `59.00–72.65`，描述性均值 `65.825`；两局均达到 48m，其中一局超过 70 分。 | 两个观测显示轨迹有明显差异，不构成校准后的分布或因果结论。两局都有 runtime / evidence 限制，且都不是最终 v6 身份。 |
| Candidate v1 S04-03 / S04-04 | 同一 source `7a055dea76580117ca74cddb49bb04efcf605eb1`；结果分别为 `76.04 / 48m / A / L6` 与 `35.31 / 25m / D / L4`（trust-crisis 终局）。 | `76.04` 这个反例说明 v6 的 `75.29` 并非全部历史记录中的最高分。这组是 Tier-B 摘要证据；原始 raw 不可用，因此没有另分配 Run Display ID，也不作为受控分布。见 [S09-02 review](reviews/S09-02_FAILURE_FLOOR_HIGH_SCORE_JOINT_FORENSICS.md)和[S10-23R 冻结审计](reviews/S10-23R_FINAL_SINGLE_SHOT_FREEZE.md)。 |
| v6d 历史备选 | 最终冻结审计列出三个样本：`71.67 / 65.35 / 59.67`。 | 该组数值用于历史备选比较，不是 exact-v6 身份。本文不会把它们提升为独立的 canonical Run 记录，也不声称构成概率分布。见 [S10-23R 冻结审计](reviews/S10-23R_FINAL_SINGLE_SHOT_FREEZE.md)。 |
| 最终选择 | 冻结身份因 `HIGHEST_OBSERVED_MATURE_THREE_SKILL_CEILING` 选择 exact v6；source `1114a04b75548cf52f030d123564e527060fc061`，Single Agent + 3 Skills，无 runtime delta。 | 这是已接受的选择记录，不表示 v6 全局最优或统计上更优。未增加一次复验就冻结了选择；提交包上传和平台评测仍未执行。见[身份](FINAL_SUBMISSION_IDENTITY.json)、[manifest](FINAL_SUBMISSION_MANIFEST.md)和[冻结审计](reviews/S10-23R_FINAL_SINGLE_SHOT_FREEZE.md)。 |

### 其他终局与技术证据

- **S07-38 / v7i 观察前 provider 失败：**获准的运行路径在首次 fresh game observation 前因重复 provider 连接错误失败。输出的分数属于更早的 v7g session，已排除。这是 provider 边界证据，不是有分数的 v7i 运行，也不是选定的部分运行代表。本机原始证据仍受 hold；见 [v7i 记录](runs/v7i-run1-validation.md)和[S07-39 调查](reviews/S07-39_PROVIDER_CONNECTIVITY_FORENSICS.md)。
- **自然终局样本选择：**使用 `RUN-0005`，而不是 S07-29 v7d，因为前者在当前 canonical report 中有明确的 run/session 归属和终局记录。S07-29 仍列在[运行历史](RUN_HISTORY.md)中；本文不给它另分 Display ID。

## 架构与策略负结果

| Display ID / 路线 | 调查原因与证据 | 决策 | 仍未知的事项 |
|---|---|---|---|
| `EXP-0001` · S10-22 Simulator Policy Search | 确定性公开输入 harness 通过边界检查，但冻结 Story baseline 只完成 2/16 个 episode；定义了 12 个宏配置，实际只评估 baseline。 | `SIMULATOR_POLICY_SEARCH_NOT_FEASIBLE`；在宏筛选、确认和 128-seed holdout 前停止。保留既有 ID。 | 哪个宏策略可能有优势仍未知；这是可行性门失败，不是策略比较。见[研究报告](research/S10-22_SIMULATOR_POLICY_SEARCH.md)。 |
| `EXP-0002` · S10-19-R1 Reviewer | 检查冻结的官方 Agent 提交路径能否部署安全隔离的 advisory reviewer。Phase A 未找到已注册、机械上只读的 reviewer 路径；五项无副作用的静态检查通过。 | `REVIEWER_NOT_SAFELY_DEPLOYABLE`；在 safety gate 停止，未执行 Phase B/C。这是部署边界结论，不是否定 reviewer 的价值。 | 未进行 child dispatch、盲评质量评估或模型遵循评估；见[可行性报告](research/S10-19R1_SUBAGENT_FEASIBILITY.md)。本任务未新增 hold。 |
| `EXP-0003` · S10-19-R2 Memory | 检查冻结提交路径是否自动提供 `MEMORY.md` anchor。启动、更新和模拟压缩后的 captures 都没有包含其正文；显式读取可用。 | 对请求的自动 anchor，结论为 `MEMORY_NOT_DEPLOYABLE`。持久性门未通过，因此跳过配对审查/序列评估。 | 其他 Memory 设计、对 gameplay 的价值和云端模型效果仍未知。见[可行性报告](research/S10-19R2_MEMORY_FEASIBILITY.md)。hold 仍有效。 |
| `EXP-0004` · S10-19-R3 deterministic helper | 隔离的工具级检查确认 JSON 输出、跨调用/模拟压缩的状态持久化和 install 后 reset；自动 Todo anchor 与 sampling 路径已关闭。 | 工具隔离层面的结论为 `DETERMINISTIC_HELPER_CHALLENGER_SUPPORTED`；没有部署正式 Candidate / Skill。 | 云端解释器/权限可移植性、模型上下文可见性、模型调用与遵循情况仍未知。见[审计](research/S10-19R3_NATIVE_CONTROL_SURFACE_AUDIT.md)。hold 仍有效。 |
| `EXP-0005` · S10-20 replay controller | 12 个 development 窗口和 12 个 holdout 窗口产生：一次仅状态层面的修正、七个保留的合理选择、七个可能的替代项、一个无变化案例和八个 `UNKNOWN`。 | `CONTROLLER_LOGIC_SIGNAL_WEAK`；replay 支持度为 `NOT_PROMISING`；跳过模型/工具 probe。未修改 Candidate 或 Skill。 | 独立 controller 能否改变模型选择或改善结果仍未知。见[研究报告](research/S10-20_PROMOTION_WINDOW_CONTROLLER.md)。hold 仍有效。 |
| `EXP-0006` · S10-21 review-window strategy mining | 对 13 次运行的 82 个完成窗口和 28 组事实预匹配样本进行描述性分析；exposure、任期、状态、架构和异步结果归属仍互相混杂。 | `STRATEGY_SIGNAL_WEAK`；未采纳安全的策略改动。这是回顾性分析，不是无污染的前瞻 holdout。 | 策略因果效应或新的可部署策略仍未知。见[研究报告](research/S10-21_REVIEW_WINDOW_STRATEGY_MINING.md)。hold 仍有效；已跟踪证据没有标明本机准确路径。 |

**Team / Swarm：**架构决策将该路线保留为 `DEFERRED`；本次 S11 审查没有发现专门的可行性尝试或部署证据。这不是经过测试的不可行结论，也没有分配 Display ID。见[架构决策](ARCHITECTURE_DECISIONS.md)。

**过度复杂的 runtime / prompt 控制：**S09 在没有稳定 75+ 突破的情况下结束了增量 prompt hardening；之后 S10 策略挖掘也没有得到安全改动。这支持的是在当时证据下停止扩展该路线的历史决定，不是“prompt 规则普遍无效”的结论。见[架构决策 AD-S10-001](ARCHITECTURE_DECISIONS.md)和[S10-21 研究](research/S10-21_REVIEW_WINDOW_STRATEGY_MINING.md)。

## FORENSIC_HOLD 台账

状态含义：`KEEP_ACTIVE` 表示有来源支持、仍待处理的 hold；`UNKNOWN_REVIEW_REQUIRED` 表示释放条件不完整、aggregate 未枚举或 raw-hold 状态未知。本文没有使用 `POTENTIALLY_RELEASABLE_AFTER_CANONICAL_REVIEW`，因为这里没有建立 Main 接受或依赖闭合。“结论已吸收”表示精简结果/原因已总结在本文，不会替代 raw evidence。

下表有 **20 个可逐项追溯的 active/pending holds**：18 个 `KEEP_ACTIVE`、2 个 `UNKNOWN_REVIEW_REQUIRED`、0 个可释放项。另有两行是不确定性 sentinel，不是确认的独立 hold：一行代表成员可能与上述 20 项重叠、但尚未枚举的 legacy aggregate；另一行记录 `RUN-0001` raw 的正式 hold 状态未知。v7o 行虽经后续再次确认可逐项追溯，也可能与 aggregate 重叠。因此，根据已跟踪来源无法确定 aggregate 与本机 raw 状态合并后的唯一总数。

| Hold / 持有人 | 原因 | 来源 / 文件 | Canonical 结论是否已吸收 | 释放条件 | 当前状态 |
|---|---|---|---|---|---|
| S07-38 / S07-38, Main | v7i 在首次 fresh observation 前 provider 失败；排除发出的过期 v7g 分数。 | [v7i 记录](runs/v7i-run1-validation.md)；[S07-39 review](reviews/S07-39_PROVIDER_CONNECTIVITY_FORENSICS.md)；本机 run 和独有 Runner 输出路径已在对应记录中注明。 | YES — 已吸收失败分类和过期分数排除结论。 | Main 接受分类，确认缺失 transcript / stale score 不需再分析，并明确释放。 | `KEEP_ACTIVE` |
| S07-47 / S07-47, Main | S07-46 M20 部分运行；传输归因和恢复发现仍待审查。 | [v7m 记录](runs/v7m-run1-validation.md)；[S07-47 review](reviews/S07-47_V7M_M20_PARTIAL_RUN_FORENSIC_REVIEW.md)；本机 stderr、服务启动 stdout 和限定范围的 LLM 记录。 | YES — 已吸收部分运行结果；raw 归因仍未结束。 | Main 接受独立审查，确认不需继续归因，并关闭下游依赖。 | `KEEP_ACTIVE` |
| S08-RUN01 / 原始持有人 UNKNOWN | S09-11 后来再次确认 v7o raw `FORENSIC_HOLD` 仍保留；原始原因和准确保留文件清单未能恢复。 | [v7o 验证记录](runs/v7o-run1-validation.md)；[S09-11 review](reviews/S09-11_V8A_V7O_TRANSPLANT_FIDELITY_REVIEW.md)；[archive manifest](../../artifacts/dev-runs/s08-run01-v7o/evidence-manifest.json)；[S08-05 review](reviews/S08-05_SCORE_GAP_AND_COMPRESSION_RESILIENT_POLICY.md)。 | PARTIAL — 已记录运行结果及 S09-11 限定范围的 events/transcript 使用；原始 hold 原因和范围未知。 | 原释放条件为 `UNKNOWN`。S11-08 Main 另将 events/transcript 保留为 `KEEP_CANONICAL_RAW`；归档中其余六项仍为 `HOLD_PROTECTED_UNKNOWN_SCOPE`。 | `UNKNOWN_REVIEW_REQUIRED` |
| S08-RUN02 / S08-RUN02, Main/Stage | v7q 自然 M24 终局；压缩/恢复情况未知，策略审查待完成。 | [v7q 验证记录](runs/v7q-run1-validation.md)；[归档证据 manifest](../../artifacts/dev-runs/s08-run02-v7q/evidence-manifest.json)；本机 run 原件。 | YES — 已吸收选定的自然终局记录。 | Main/Stage 接受独立分类，并确认不再需要 raw 复析。 | `KEEP_ACTIVE` |
| S08-RUN03 / S08-RUN03 closeout, Main/Stage | v7t runtime / evidence-discipline 解释仍可继续审查。 | [v7t 验证记录](runs/v7t-run1-validation.md)；[S08-RUN03 evidence manifest](../../artifacts/dev-runs/s08-run03-v7t/evidence-manifest.json)；准确 Runner 输出目录。 | PARTIAL — 已记录 hold 原因；完整遵循分析仍在来源审查中。 | 独立审查接受遵循/策略解释，并确认来源可恢复或不需进一步分析；清理仍须单独限定范围授权。 | `KEEP_ACTIVE` |
| S08-RUN04 / S08-RUN04, Main/Stage | v7v runtime 证据限制和 transcript 纪律发现。 | [v7v 验证记录](runs/v7v-run1-validation.md)；[S08-RUN04 evidence manifest](../../artifacts/dev-runs/s08-run04-v7v/evidence-manifest.json)。 | PARTIAL — 结果和来源已保留，但没有完整收口条件。 | 跟踪记录只写“pending Main/Stage review”；验收条件以及 raw / 依赖闭合条件都未说明。 | `UNKNOWN_REVIEW_REQUIRED` |
| S09-RUN01 / S09-RUN01, Stage/Main | v7w 提前终局、证据身份/防火墙及 runtime 限制。 | [v7w 验证记录](runs/v7w-run1-validation.md)；S09-RUN01 归档和本机 raw。 | PARTIAL — 有终局摘要；保留的 raw 仍支持深入审查。 | Stage/Main 确认身份、分类、Candidate 标记和防火墙处置，并确认来源可恢复或不需再分析；删除需要逐文件授权。 | `KEEP_ACTIVE` |
| S09-RUN02 / S09-RUN02, Stage/Main | v7x 两个 S 窗口的公开语义和 transcript 匹配。 | [v7x 验证记录](runs/v7x-run1-validation.md)；归档外保留的本机 events/transcript。 | PARTIAL — 已记录 hold 范围和运行摘要。 | 独立的 public-only 语义审查接受两个窗口及 transcript 匹配，并确认不再需要其他 raw 来源。 | `KEEP_ACTIVE` |
| S09-RUN03 / S09-RUN03, Stage/Main | v7y play 前启动/ready 失败；根因未知。 | [v7y 验证记录](runs/v7y-run1-validation.md)；选定的启动诊断和本机 preflight/runtime 来源。 | PARTIAL — 仅吸收 play 前分类。 | Stage 接受可独立复核的诊断，确认所需来源仍可恢复，并关闭 runtime-child 依赖。 | `KEEP_ACTIVE` |
| S09-RUN03R / S09-RUN03R, S09 Stage | v7y 用户中止的运行；需保留中止发现和准确运行来源。 | [v7y 中止运行记录](runs/v7y-run03r-user-censored.md)；本机 events/transcript 和 run-window 回执。 | PARTIAL — 已总结中止边界和结论。 | Stage 接受中止发现，并确认 raw 复析及 child 依赖均不再需要；任何删除仍须明确的清理授权。 | `KEEP_ACTIVE` |
| S09-RUN04 / S09-RUN04, S09 Stage | v7z M6 screening 失败和 world-model / transplant 审查。 | [v7z screening 记录](runs/v7z-run1-screening.md)；本机 raw events/transcript 和限定范围的回执。 | PARTIAL — 已总结 screening 决策。 | Stage 接受结果并关闭 raw 分析/child 依赖；清理需要另行授权。 | `KEEP_ACTIVE` |
| S09-RUN05 / S09-RUN05, S09 Stage | v7z M6 复验；保留第二条失败轨迹以供审查。 | [v7z 复验记录](runs/v7z-run2-replication.md)；本机 raw events/transcript 和限定范围的回执。 | PARTIAL — 已总结复验结论。 | Stage 接受结果并关闭 raw 分析/child 依赖；清理需要另行授权。 | `KEEP_ACTIVE` |
| S09-RUN06 / S09-RUN06, S09 Stage | v8a M6 screening；transplant fidelity 和 donor adherence 尚未解决。 | [v8a screening 记录](runs/v8a-run1-screening.md)；本机 raw 和限定范围的回执。 | PARTIAL — 已总结 screening 结论。 | Stage 接受 transplant-fidelity 审查并关闭 raw 分析/child 依赖；清理需要另行授权。 | `KEEP_ACTIVE` |
| S09-RUN07 / S09-RUN07, S09 Stage/Main | v8a 样本 1；Delivery 分隔符、HiddenRisk 数值引用和 M36 风险应对仍待审查。 | [v8a 样本 1](runs/v8a-full-horizon-sample1.md)；准确 raw run 工件和本机 stdout / 回执。 | YES — 已吸收选定结果；保留的 raw 仍支持未解决的审计。 | 独立审查接受证据限制，并确认不再需要 raw。 | `KEEP_ACTIVE` |
| S09-RUN08 / S09-RUN08, S09 Stage/Main | v8a 样本 2；双样本、证据防火墙和 Delivery 审查。 | [v8a 样本 2](runs/v8a-full-horizon-sample2.md)；列出的工件以及本机 stdout / 清理回执。 | YES — 已吸收选定结果和描述性配对摘要。 | 独立审查接受结果，并确认后续工作不再依赖 raw；明确清理授权仍需另行取得。 | `KEEP_ACTIVE` |
| S10-19-R2 / S10-19-R2, Main/Stage | 在负向门审查获接受前，保留 Memory feasibility probe 和 captures。 | [Memory 可行性报告](research/S10-19R2_MEMORY_FEASIBILITY.md)；`.local/runtime/s10-19r2-memory-feasibility`。 | YES — 已吸收负向可行性结论；captures 仍是来源证据。 | Main/Stage 接受门禁结论并解除后续复析依赖。 | `KEEP_ACTIVE` |
| S10-19-R3 / S10-19-R3, Main/Stage | 保留可执行 deterministic-helper 证明及 child 复析来源。 | [native control 审计](research/S10-19R3_NATIVE_CONTROL_SURFACE_AUDIT.md)；`.local/runtime/s10-19r3-native-control`。 | YES — 已吸收有界结果；可移植性仍未知。 | Main/Stage 接受结果并解除 child 复析依赖。 | `KEEP_ACTIVE` |
| S10-20 / S10-20, Main/Stage | 保留 controller replay 证据和引用的 helper / harness。 | [controller 研究](research/S10-20_PROMOTION_WINDOW_CONTROLLER.md)；`.local/runtime/s10-20-controller` 及其引用的 helper/harness。 | YES — 已吸收弱信号结论；没有部署证据。 | Main/Stage 在依赖闭合后接受门禁结果。 | `KEEP_ACTIVE` |
| S10-21 / S10-21, Main/Stage | 保留策略挖掘输入供审查/复析；跟踪证据没有标明准确的本机目录。 | [策略研究](research/S10-21_REVIEW_WINDOW_STRATEGY_MINING.md)；本机 hold 路径为 `UNKNOWN`。 | YES — 已吸收描述性结果和归因限制；raw 路径仍不明确。 | Main/Stage 接受分析并关闭依赖的复析工作；审查任何清理前，必须核对准确来源清单/路径。 | `KEEP_ACTIVE` |
| S10-22 / S10-22, Main/Stage | 保留 simulator-policy 负向可行性门及本机证明。 | [policy search 报告](research/S10-22_SIMULATOR_POLICY_SEARCH.md)；`.local/runtime/s10-22-policy-search`。 | YES — 仅吸收可行性门结论。 | Main/Stage 接受门禁结果、解除依赖，并另行授权清理。 | `KEEP_ACTIVE` |
| 历史 run hold 未枚举 aggregate / 原任务与 Main 持有 | promotion-frontier 报告称全部原始 run holds 均保留且 release 为 `NONE`，但未列完整成员或数量；可能与上列已命名条目重叠。 | [S10 promotion-frontier 报告](research/S10_PROMOTION_FRONTIER_REPORT.md)。 | PARTIAL — 仅吸收 aggregate 保留声明。 | 任何未命名成员的准确归属、持有人、来源和释放状态均为 `UNKNOWN`；清理前须与来源任务对账。 | `UNKNOWN_REVIEW_REQUIRED` |
| `RUN-0001` raw 保留状态 / 持有人 UNKNOWN | 支持 v6 的 raw 在本机且未提交；当前 canonical docs 未说明正式 raw `FORENSIC_HOLD` 或释放条件。本行不计作已确认 hold。 | [CURRENT_STATE](CURRENT_STATE.md)；[v6 验证记录](runs/v6-run1-validation.md)。 | YES — 已吸收精简运行事实；raw-hold 状态仍未知。 | `UNKNOWN`；不能从精简记录推断正式 hold 或其释放。 | `UNKNOWN_REVIEW_REQUIRED` |

### 既往已解决的 hold 处置

此前 Main 已将独立的 `S03-MCP-REGISTRATION` forensic hold 记录为 `RELEASED_BY_MAIN`。本文只保留这一历史状态；它不表示策略有效，也不改变任何当前 hold。

## 证据缺口与清理边界

- 20 个具名 active/pending holds 均未释放。S08-RUN01 的原始持有人、原因、准确成员范围、创建时间和释放条件仍为 `UNKNOWN`；其条目可能与未枚举 aggregate 重叠。S08-RUN04 没有完整的接受/依赖闭合条件，v6 raw 的 hold 状态也未说明。这些不确定性使唯一完整清单和清理范围仍无法确定。
- Candidate v1 的 raw 在本记录比较中不可用；v6d 仅由冻结审计中的三个分数摘要表示。两者都没有被提升为完整 canonical Run 记录。
- 两份来源记录中的 exact v8a 样本行为一致，但 runtime / evidence 限制不支持干净的遵循结论。这组配对结果也没有解释分数差异。
- 本组证据没有证明 Team/Swarm 可行性尝试、已部署的 Reviewer / Memory / helper / controller 路线、已完成的 simulator-policy 宏搜索、稳定 75+ 分布或官方平台评测。
- 本次迁移未改动 raw 文件，也未释放 hold。后续清理仍需逐来源复核并取得限定到具体文件的授权；Git history、精简结论和 hash 都不能替代受 hold 保护的证据。

## 证据索引

- [当前状态](CURRENT_STATE.md) · [运行历史](RUN_HISTORY.md) · [架构决策](ARCHITECTURE_DECISIONS.md)
- [最终提交身份](FINAL_SUBMISSION_IDENTITY.json) · [最终 manifest](FINAL_SUBMISSION_MANIFEST.md) · [冻结审计](reviews/S10-23R_FINAL_SINGLE_SHOT_FREEZE.md)
- [最终 Display-ID 索引](FINAL_ID_MAP.md)
