# S09-11｜v8a–v7o 移植忠实度审查

## 结论与证据窗口

**主结论 B：`TRANSPLANT_FIDELITY_PASS_WITH_LOCAL_CORRECTNESS_DEFECT`。** 在可比暴露中，广义成长、Main 多维/ownership prior、CI 机会成本比较、建设性风险处理动作均已执行。发现 Risk 分类及成本确定性缺陷，但没有足够证据认定 donor ranking 发生高影响偏移，或这些缺陷解释了 M6 未晋升。`NO_CANDIDATE_PATCH_RECOMMENDED`；minimal correction=`NONE`。

- Base：`01c9f7c7cd6495e9ea635eeeae8afa3bdc6b2e84`；v8a exact source 为 `e13236b23d26879dc92ae30206cfdc7611037041`，当前 Candidate/manifest/four Skills 与其一致。
- v7o source：`b2e7ea6441da9c314d8a0ffbf29b9d5800ced10d`；archive/session 与正式 run identity 对应。只提取 `artifacts/dev-runs/s08-run01-v7o/events.jsonl` 至首次 M6 正式 Review **seq187/line187**；20 actions /21 observes。首末 action UTC `2026-09-29T11:54:51.610014+00:00`–`11:56:31.602854+00:00`。Transcript 仅使用首次明确 M=6 状态之前的 **lines1–561**，不读后续排序。
- v8a：`D:/CS/CareerSim/.career_sim_runner/career_emu/outputs/local-s06-adaptive-controller/20261001T104410Z/events-20261001T104410Z.jsonl` 至首次 M6 Review **seq187/line187**；20 actions /21 observes。首末 action UTC `2026-10-01T10:44:27.428405+00:00`–`10:47:24.193778+00:00`。对应 transcript **lines1–701** 在最后 CI action 后结束，没有 post-Review Planning。
- 比较单位为同局 fresh observe 的 public description/choices、Board/Delivery、候选理由、最终 Risk、action 和其相邻 public result。跨月/Review 混杂不当作 clean attribution。没有消费 shared DB、provider/service logs、hidden effect 或 M6 后行为；不新增 cohort，不用最终 score 反推选择。公共文本用于离线比对，不形成 runtime title/event lookup。

## 六轴结果

| 轴 | 结果 | 决策证据与边界 |
|---|---|---|
| A Promotion-first / advancement | MATCH | v7o a8/10、v8a a9/15/20 推进结果/技术/责任；普通成本没有自动拦截成长。两局 A20/S0，但结论来自候选理由而非计数。 |
| B Broad early compounding | MATCH | 两局 Energy 比较 N/O、Main 保留 S/N/O；v8a N3→3 后转向 responsive O，仍选不同 family 的 Main/Story，不把未知路径整体关闭。未见单维 NO_GAIN 锁死主线。 |
| C Main ownership semantics | MATCH | 两局 a14/seq133。Donor transcript369/383 用 O+2/S+1/N+1、Output 短板比较菜单；v8a556–562 明确比较导师等 alternative，选择多维收益与 visible ownership。不是仅凭同一菜单答案。 |
| D Protection / survival floor | INSUFFICIENT_EXPOSURE | donor H3、持续5→4→3，A 下恢复一次 H3→5，再 N/O；v8a H4、O=-1，反复比较 Health 与成长后选 O/N/O。输入/趋势/成长机会不同，不能推出过度保守或必然漏保护。暴雨成本确定性缺陷成立，但 donor 首窗无对应暴雨暴露。 |
| E Risk gate | MATERIAL_DRIFT（分类/复核层） | 相同公开合规描述、相同三选项、相同建设性拒绝：donor a2 ALLOW，v8a a19 PASS。Full Review scope 的执行分类偏差明确；没有显示提交候选被改变，故不满足主结论 A 所需的 material donor-ranking drift。 |
| F Delivery / opportunity cost | MATCH | donor a10 与 v8a a20 的 CI 描述/choices 完全相同：2周投入、两个排期项目延后，均选投入并明确视为普通机会成本。月份/Review 距离不同，不能宣称完整 timing fidelity。 |

## 精确早期决策表

每个 a# 指对应窗口内动作序号；原始 action seq 为29起、每次递增8。只保留影响判断的决策。

| Decision window | v7o | v8a | Comparable? | Fidelity | Material? |
|---|---|---|---|---|---|
| Q1 Energy，a11–13 | H3/N2/O1；Health→Network→Output；A 下一次保护后成长 | H4/N3/O-1；Output→Network→Output；N NO_GAIN 后换 O | 菜单相同，状态/趋势不同 | 广义预算可比；保护排序不能精确匹配 | 确实改变预算；对晋升的作用 UNKNOWN |
| Q1 Main，a14/seq133 | 三维增益、补 O 短板；没有选低调/不行动 | 三维增益+ownership；与导师路径比较 | 菜单相同、输入不同 | MATCH | 未发现 ranking drift |
| 合规红线：donor M1 a2 / v8a M5 a19 | 婉拒并圆回正常招待，Full Review→ALLOW | 同一拒绝理由，PASS/no material risk | 描述与 choices 相同；时点/状态不同 | 动作 MATCH；gate 分类偏差 | 复核缺陷明确；候选改变未显示 |
| CI ownership：donor M3 a10 / v8a M5 a20 | 承认延后两个项目，ownership/团队规模价值胜出 | 同样承认延期，ownership/多维成长胜出 | 描述与 choices 相同；checkpoint 距离不同 | MATCH（tradeoff） | 时点/暴露差异真实；M6 因果 UNKNOWN |
| 急件打印：donor a17 / v8a a16 | 请求插打两页，保时效与关系 | 同一请求，保交付与关系 | 描述/choices/公开状态相同 | MATCH | 无策略偏移 |
| 信任/诚信：donor a4/9/15/20 / v8a a5 | 事实评级、透明披露/应对、诚实承担；ALLOW | 用 git/周报证据上报署名，ALLOW | 同类型 material 风险；非相同事件 | 风险不要求放弃推进，两者均可 ALLOW | 不证明合规 PASS 会改其它候选 |
| 暴雨：v8a a17–18 | 无首窗 comparable exposure | 共伞后赴热面；a17 断言“无健康/财富代价”，a18 承认 H3 却推迟恢复 | 否 | 成本确定性缺陷；保护 fidelity 未决 | 不能假定 donor 会拼车/拒绝；不能归因 M6 |
| Review 前最后 action，a20 | 实习生邮件事故：诚实当面道歉，ALLOW | CI投入：延期换团队基建，PASS | 否 | 最后公开任务不同 | 不从 Review label 倒推该选项错误 |

## Protection 与 Risk：缺陷不等于策略失败

Donor transcript294–298 明确允许 **MODE=A 内维护 survival floor**；H3→5 后剩余 Energy 回 N/O，没有补满 Health。v8a393–552 也实际比较了健康恢复；最终依据 H4、负/零 Output、N 无响应选择 O。其“非 binding→优先 progression”推理比 donor 的 A 内保护表达更偏成长，但缺乏同状态/同暴露的对照，不能升级为确认的 material drift。没有观察到“不必要保护挤出 advancement”。两局均没有首窗 S 恢复序列，不能验证解除后返回 A。

Risk 四问：

1. **Donor 实际分类：** 同一公司红线事件，transcript32/43 明确“candidate directly touches a compliance risk event”“risk-handling candidate”→Full Review/ALLOW；后续向领导同步也 ALLOW。不是所有安全选择都 PASS。
2. **Current contract：** 仍列 compliance/confidentiality、禁止 Full Review 后 PASS；但少了 donor 明说“safe, constructive candidate still receives Full Review”的解释句。v8a transcript659/680 将拒绝解释为“不触及 material risk”。这个省略可能影响范围理解，**归因仍 UNKNOWN**，未建立文字省略导致行为改变的实验。
3. **缺陷分类：** `RISK_GATE_SCOPE_MISCLASSIFICATION`，不仅是显示拼写错误，而是误走 Quick Gate；实际拒绝候选与 donor 相同，无 RECONSIDER/替代项提交证据。不能假定强制 ALLOW 会产生不同游戏结果。
4. **Materiality：** 复核 correctness 有缺口；对 M1–M6 ranking/晋升的实质影响未证明。donor 所选拒绝本来也 ALLOW，没有证据要求 v8a 换选。

暴雨 a17 的零成本断言在公开文本中无依据；这是成本判断确定性问题。H4→3 的回执跨月，之后 H3→2；只能记录关联。不得读取隐藏 effects 来断言替代项更好或已知净损失。主结论 B 下不推荐新增保护规则。

## Delivery 与 shell interaction

Donor transcript213–234 直接把 CI 导致的两个项目延期当作普通机会成本；v8a680–701 同样这么比较。因此不能以 RUN06 CI 延期为依据发明“donor 一定拒绝该投入”。两局 DL 均为 n0；donor305 也明确未把 CI/里程碑 Story 作为带 persistent checkpoint 的 item。现有 Delivery 未使 v8a 更保守或更激进；已有绑定交付若被完整追踪后的反事实结果 UNKNOWN。

整体分类：**`SHELL_INTERACTION_UNKNOWN`**；没有足够证据判定 shell 改变了 donor 的实际候选排序效果。

| 可能交互 | 本窗口证据 |
|---|---|
| Mandatory fresh-observe replanning | 两局20/20 action→fresh observe；donor本来逐项观察、调整 Energy，未见 modern shell 新增批次/切断路径。 |
| Board response fields | v8a N NO_GAIN 参与 O 重分配，Main/其它 Story 仍开放；donor原先也用 fresh observed effect。部分 v8a Story/Main response 归因含跨月/无 advertised dimension，不能当 clean facts；未证明这关闭了 donor 候选。 |
| Delivery ownership | 均 n0；CI tradeoff 相同。缺失 item 是共有限制，非新增 shell veto 的证据。 |
| Risk Full Review | 分类执行确有偏差；所选 refusal 相同，shell wording 的独立贡献 UNKNOWN。 |
| Preflight closure | donor X=-、v8a RB=NONE；首次 Review 前都持续20动作，无 branch/blocked 改选或错用 stale action 证据。两者内部反复 deliberation 属 correctness 限制，未显示其因果影响。 |
| RECOVERY labels | 没有标签驱动的新 S/deadlock 或额外排序树。类型恢复未充分暴露，不能声称已全程等效。 |

## Public-state 描述：校正 pre/post 边界

Plan 所列 v8a `H2/D10/S9/N2/O1/W3/E0` 实际是 **包含 M6 Review 的首次观察**，不是最后 pre-Review snapshot。

| 观察边界 | v7o | v8a |
|---|---|---|
| 最后 pre-Review observe，M5、a20之前 | H5/D9/S9/N3/O3/W3/E0，L1 | H2/D10/S9/N3/O3/W3/E0，L1 |
| 首次 M6 Review observe，seq187 | H4/D10/S9/N3/O3/W3/E0，L2，C/promoted | H2/D10/S9/N2/O1/W3/E0，L1，C/not promoted |

Snapshot difference **≠ causal promotion mechanism**。相同 S/N/O 或不同 Health 不代替行为 fidelity 分析；最后 Story、自动结算与 Review 混杂，不反推隐藏 eligibility、阈值、固定月份或必胜动作。首窗 core 相似而结果不同，不能给出 donor core 的 deterministic guarantee。

## 返回 Stage

- Strongest confirmed **material strategy drift：NONE**；已确认 local correctness defects 不等于 material ranking drift。
- Decision：`S09_11_FIDELITY_PASS_LOCAL_DEFECT_RETURN_TO_STAGE`。
- Minimal correction：`NONE`；`NO_CANDIDATE_PATCH_RECOMMENDED`。不要继续改 promotion strategy 来解释单局 M6 failure；若 Stage 研究 variance/controlled replication，须另行授权。
- Candidate/Skill/manifest/Runner/dependencies/retry/validation 未改；game/live operations=0。无 tests/full audit；仅文档/derived parse、secret scan 与 diff check。两局原始 FORENSIC_HOLD 均保留，未宣告 release 或授权清理。
- 精确窗口提取与 early transcript 派生物留 `.local/runtime/s09-11/`；不提交原始日志，不重算旧 hashes。此次仅新增本 review、一个小型 source/decision index，并更新 CURRENT_STATE 一条 delta。

`NEXT_GAME=NOT_AUTHORIZED`
