# S07-40 — v7i Replacement 单局验证

## 验收摘要

- Gameplay：VALID_48M_COMPLETION。
- Score：VALID_FRESH_SESSION_SCORE_WITH_SCORE_REPORT_SESSION_FIELD_BUG；quantitative 64.0 / competition partial 44.8 / 48m / B。
- Runtime：RUNTIME_ADHERENCE_FAIL，包括 2 次未注册工具路由错误与 2/2 次压缩后缺少强制四 Skill reread。
- Strategy：PROMOTION_FIRST_ADHERENCE=PASS_WITH_LIMITATIONS。
- Evidence：EVIDENCE_DISCIPLINE_FAIL（1 次 numeric HiddenRisk 写入 action note）。
- Delivery lifecycle：DELIVERY_LIFECYCLE_ADHERENCE_NOT_PROVEN。
- Recovery：RECOVERY_PATH_FAIL。
- Mechanism：MECHANISM_NOT_TRIGGERED_WITH_DELIVERY_ADHERENCE_LIMITATION。
- Decision closure：DECISION_CLOSURE_FAIL / SEVERE_VERBOSE_DELIBERATION。
- Improvement causality、stable 80+、hidden-test transfer：NOT_PROVEN。
- NEXT_GAME：NOT_AUTHORIZED。

### Main Raw Re-Audit 修正（本节为当前权威结论）

本节依据用户提供的 D:/CS/temp/CareerSim/S07-40｜Main-Raw-ReAudit.md。此前首轮 bounded pass 的下文仅作为审计轨迹保留；如与本节冲突，以本节为准。本轮没有重新解析 raw、日志或 shared DB，也没有运行 service、Runner 或 provider。

- 成绩恢复为有效 fresh-session score：最终 fresh observe 与 transcript 末尾均记录 quantitative 64.0、competition partial 44.8、48m、B；score_report.session_id 为空是 Runner 字段缺陷，不再据此排除该成绩。
- 历史分数仅作单局方向比较：相对 v7g +9.48、v6 -11.29、v1 #1 -12.04、v1 #2 +28.69；不证明因果收益或稳定优于 v7g。
- 当前局 compression 为 2 次（19:37:12、19:45:43 +08:00），不是累计 llm.log 的 23 条历史记录。两次均 fresh observe 后直接继续 take_action，均缺少四 Skill reread，RECOVERY_PATH_FAIL。
- 晋升月份修正为 M6 / M12 / M30 / M48；评审为 M6 C L1→L2、M12 B L2→L3、M18 B 无晋升、M24 B 无晋升、M30 B L3→L4、M36 A 无晋升、M42 A 无晋升、M48 A L4→L5。M36 的 L4 状态不是晋升月份。
- Promotion-first 总体 PASS_WITH_LIMITATIONS：16 个季度 Main 中 12 次申请关键项目、4 次汇报成果，0 次低调避险、0 次不行动；202 次 action 中 P=A 196、P=S 6，后者对应明确 Health constraint。一次 numeric HiddenRisk action-note 仍使 EVIDENCE_DISCIPLINE_FAIL。
- Delivery lifecycle 没有长程可审计维护证据，故 DELIVERY_LIFECYCLE_ADHERENCE_NOT_PROVEN。TRUE_TRIGGER=0；M5 原型/需求对齐为 CORRECT_NON_TRIGGER / BORDERLINE。Mechanism 结果为 MECHANISM_NOT_TRIGGERED_WITH_DELIVERY_ADHERENCE_LIMITATION，不代表 controller 已通过 runtime 验证。
- Decision closure 修正为 DECISION_CLOSURE_FAIL / SEVERE_VERBOSE_DELIBERATION。Main 复核报告约 11,229 次 Hmm、约 420 次 reconsider、约 120 次 Let me reconsider、transcript 约 10,283 行；精确 candidate flip 数仍 UNKNOWN。Runner 汇总 output 254,782、total 42,887,446 tokens；实际 billed cost UNKNOWN。
- 两次错误 tool route 均发生在 emulator dispatch 前；没有重复 state side effect。G continuity 相对 v7g materially improved，但不构成 causal score gain 证据。
- Stable 80+、因果分数/生存提升、hidden-test transfer、Delivery controller 长程正确性仍 NOT_PROVEN。next_game_authorized=false。

以下 identity、trajectory、action 与 artifact hash 的首轮记录继续保留；其中本节已明确更正的 score、compression、promotion、strategy、mechanism、decision-closure 判断由本节覆盖。

## Identity 与 provider gate

- 基线：main@33d89f773da2c90df4db9878d8d54c10bf6edd0e，等于任务开始时的 origin/main；Candidate 为 candidate-v7i-pre-review-result-realization-probe，parent 为 candidate-v7h-evidence-recovery-hardening。
- runtime manifest SHA-256：0946e8b3c7cff62661bfb948a9e0cde39fce664847cb41bae4390587ae6c4fa3。
- instruction SHA-256：0dd590d21e036e5dc4cdde25553d250ac87439ab4cc1af29bc75c07367026721。
- 四个 Skill blob：Board 1707e8183e3b7f4c299838b4fc2c0f01de7581e2；Planning 67947aa2928eae2f09f94edfafd08fda00311fd5；Delivery 48dcbece745734a16f1b5caffadce55d7e7ecf97；Risk 06bb1289499356d2d882dc4336eb17832f8e2fdf。
- S07-39 的 RETRY_GATE_PASS 原样复用。provider 配置未变；未增加 /models、chat 或 completion 探测。游戏期间有真实 DeepSeek gameplay 响应。
- AgentServer readiness 达成后仅执行一次 Runner play；Runner exit code 0，play_exit_code 0。Runner 区间为 2026-09-28T11:27:38.1629481Z 至 2026-09-28T11:54:12.5142365Z。
- service lifecycle 为 start 1 / graceful stop 1。stop 使用已确认的绝对路径，返回 0；manager 已停止，端口 19092、20000、20001、6173 已释放。此前一次 PATH 名称查找失败，没有执行 CLI，是 harmless tooling issue，不影响 gameplay。
- 未直接读取、查询或 hash shared DB；未做独立安装，正常安装/reload 由 Runner play 路径负责。

### Fresh identity gate

- events 中有且仅有一次结构化 new_game，session ID 为 cec080dd3c1d43a0b9cb92945e9a824e。
- 201 条 observe 的 current_state.session_id 均为 cec080dd3c1d43a0b9cb92945e。transcript 的 SESSION 标记也属于该 run。
- fresh ID 与旧 v7g session d4464a311c924e73b9e23eebd6f71f6d 不同。
- score_report.json 的 session_id 当前为空字符串；不能与 fresh ID 匹配。因此完整 score identity gate 未通过。Runner 的 ending_score、completed、survival、grade、promotions 汇总、score dimensions 全部标记 STALE_SCORE_DIAGNOSTIC_ONLY，不用于结论。此文件的 drive_session_id 与本次输出路径可对应，但不能替代 game_session_id。

Gameplay 状态仍可从 fresh events 独立审计：current_month 从 1 到 49，所有 observe 保持本次 session，Runner 正常 exit 0，最终观察没有 failed 状态。这支持从起始月到 48 次月份推进的单局完成分类；score_report 的完成标记不作为依据。

## Mechanism trigger audit

规则要求首个正式评审前同时有当前局公开 Delivery 依据，以及能完成/验证/展示现有结果或取得公开回执的合法动作。以下字段只按 artifacts 可见信息填写；缺失的 stage、recognition_link、next_checkpoint 不推断。

| Month / node | MODE / Delivery basis | stage / evidence_status / recognition_link / next_checkpoint | legal candidate and eligibility | applied / selected / public reason / fresh result | 分类 |
|---|---|---|---|---|---|
| M1–M2 Story | Board 初始记有 Delivery: NO_CHANGE；没有现有成果/提交项 | stage、recognition_link、next_checkpoint 不适用；evidence_status=NO_CHANGE | 社交、合规与协作事件；没有结果展示/验证动作，因此不 eligible | 未应用 prior；选择日常故事动作，无已确认交付回执 | CORRECT_NON_TRIGGER |
| M3 Main Action | 无已记录的当前局 Delivery 项；申请关键项目会创建新工作 | Delivery 生命周期字段 UNKNOWN | “申请关键项目”等季度候选没有完成既有成果，不 eligible | 未应用 prior；选申请关键项目以推进 Skill/Network/Output | CORRECT_NON_TRIGGER |
| M5 客户返工长链 | 当前事件公开说明第一版已交付但客户不认可；没有公开验证/客户验收回执，Delivery lifecycle 字段未被记录 | stage=UNKNOWN；evidence_status=UNVERIFIED；recognition_link=UNKNOWN；next_checkpoint=UNKNOWN | 复盘理解并提议原型/书面确认可处理返工根因，但不是展示已完成结果、验证结果或取得回执的动作；按可见选项不 eligible | 未应用 prior；选择需求对齐。M6 的客户同意和范围谈拢出现在半年评审反馈之后，不能回算为 pre-review 触发 | CORRECT_NON_TRIGGER |

结果：TRUE_TRIGGER=0，CORRECT_NON_TRIGGER=3，FALSE_TRIGGER=0，MISSED_TRIGGER=0，AMBIGUOUS=0。首个正式评审在 M6；评审发生后 prior 退出。故机制结果为 MECHANISM_NOT_TRIGGERED，而非机制执行通过或失败。没有观察到基于菜单“汇报”字样的固定触发。

## M1–M6 progression 与评审

M1 初始公开状态为 L1、Health 5、Dignity 5、Skill 1、Network 1、Output 0、Wealth 1、Energy 3。首个记录的 Delivery 状态是 NO_CHANGE。

首个正式半年评审发生在 M6。M6 评审时（不是后续季度动作后的状态）公开状态为 L2、duration_in_level 1、Health 3、Dignity 10、Skill 9、Network 3、Output 2、Wealth 2、Energy 0。events 的半年反馈记录绩效等级 C；Leader 反馈“这半年不好不坏”、仍在观察名单、下一阶段需要更清晰成果，并明确晋升评审通过、L1 晋升至 L2。该状态单独保留，没有用 M6 后续月内状态替代。

首个评审前已记录的 15 个 Story 选择按月归纳如下，均来自当前局 observe 与后续 take_action：

- M1：接受年会发言但选简单形式；拒绝向前同事谈竞对信息；与同事协商清理过道。
- M2：适时交还年会舞台；午饭社交事件记录了每周三天与维持每日午餐两个阶段选择。
- M3：肯定小乔并补充自己的相关成果；用数据和业务影响回应“只是工程活”；随后调整汇报话术但在文档保留技术价值。
- M4：公开感谢小乔并私下修复关系；拒收离职同事资料并建议合规交接；不向朋友透露未公开调整信息。
- M5：提出用原型/可视化文档确认客户需求；会前提醒 Leader 口径错误；会后承担向 VP 补充统计口径。

Q1 / M3 Energy：健康恢复、人脉维护、准备汇报材料；季度 Main Action 选择申请关键项目。Q2 / M6 在评审之后 Energy：准备汇报材料两次、健康恢复一次；季度 Main Action 仍为申请关键项目。M6 客户长链后续选择固化确认机制与变更留痕；夜间消息事件选择次日响应并明确作息边界，随后建立 on-call 轮值。

## Full trajectory

以下字段取自 fresh observe 的公开 current_state。M48 行是 current_month=48 的最后月内 checkpoint；启动首状态为 current_month=1，最后观察 current_month=49，因此这是 48 次月份推进。M6 的 review-time state 见上一节。

| Month | Level / duration_in_level | Health | Dignity | Skill | Network | Output | Wealth | Energy | Quarter Main Action / result |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---|
| M1 | L1 / 1 | 4 | 8 | 1 | 2 | 0 | 1 | 3 | 尚无季度 Main Action |
| M3 | L1 / 3 | 4 | 10 | 7 | 3 | 2 | 1 | 0 | 申请关键项目 |
| M6 | L2 / 1 | 7 | 10 | 13 | 4 | 6 | 2 | 0 | 申请关键项目；评审时状态见上 |
| M9 | L2 / 4 | 6 | 10 | 21 | 7 | 6 | 3 | 0 | 申请关键项目 |
| M12 | L3 / 1 | 8 | 10 | 22 | 9 | 7 | 4 | 0 | 申请关键项目 |
| M18 | L3 / 7 | 7 | 9 | 42 | 21 | 16 | 6 | 0 | 申请关键项目 |
| M24 | L3 / 13 | 9 | 10 | 42 | 21 | 12 | 10 | 0 | 向领导汇报成果 |
| M36 | L4 / 7 | 9 | 10 | 72 | 36 | 24 | 16 | 0 | 申请关键项目 |
| M48 | L5 / 1 | 8 | 10 | 109 | 35 | 30 | 26 | 0 | 申请关键项目 |
| Terminal observe M49 | L5 / 2 | 8 | 10 | 110 | 36 | 32 | 27 | 0 | Runner 随后 exit 0 |

16 个季度 Main Action 为：M3/M6/M9/M12/M15/M18 申请关键项目；M21/M24/M27/M30 向领导汇报成果；M33/M36/M39/M42/M45/M48 申请关键项目。等级在 M6、M12、M36、M48 的观察状态分别达到 L2、L3、L4、L5；除 M6 外，后续等级变化没有在本报告中推断其正式评审原因。除 M3、M6 的 Energy 选择外，各后续季度的 Energy 具体组合未纳入 bounded pass，标为 UNKNOWN；各里程碑 Energy 数值为当时公开剩余值。

## Correctness、evidence discipline 与 recovery

### take_action

- 202 次 take_action-like tool attempts：200 次 canonical tool 调用成功；另 2 次使用了未注册的工具名，返回 Ability not found 且没有 raw tool output。两次失败都没有提交到 emulator；其后仍完成 200 次成功状态动作。
- 202 次都提供一个整数 choice 和一个格式正确的单一 CTRL 前缀；missing choice=0、multi-choice=0、noninteger=0、malformed CTRL=0、schema reject=0。
- 两个路由失败单独记为 tool-route errors=2。没有重复成功 side effect 的证据。

### HiddenRisk / public evidence

- 有一条 action note 将数值型 HiddenRisk 内部变化写入策略理由，因此按 S07-40 标准为 EVIDENCE_DISCIPLINE_FAIL，也违反“未知/内部字段不得用于策略”的边界。具体内部数值不复制到本报告。
- 其余 action notes 未发现 HiddenRisk 数值引用。原始 observe/tool payload 仍作为 raw 留存；报告不把其中内部字段转成策略事实。
- 该 note 同时使 Promotion-first 策略遵循分类为 PROMOTION_FIRST_ADHERENCE_FAIL。虽然季度 Main Action 大多选择项目推进或可见成果汇报，这不能抵消一次内部数值用于决策。

### Compression recovery

保存的 llm.log 有 23 个 CurrentRoundCompressor 记录，并出现 RECOVERY_PENDING / RECOVERY_READY 标记。events 只记录启动期 4 次 Skill 读取，没有压缩后的四 Skill reread 记录。现有 artifacts 因此不能证明每次压缩后完成了同 session 确认、fresh observe、四 Skill reread、Board/Delivery/Review Plan rebuild，再提交下一动作。后续仍有 take_action，因此按 Plan 判定 RECOVERY_PATH_FAIL，不能把 READY 字符串本身当作步骤已完成的证据。

### Decision closure

MILDLY_VERBOSE：transcript 有多次重新权衡措辞，Runner 汇总记录的输入量也很高。每个 tool attempt 最终都带一个完整 CTRL 和单一整数候选；事件序列没有重复成功 side effect。因 transcript 是拼接文本，无法可靠计数每个决策内部实际候选翻转次数，故该子指标为 UNKNOWN；不把 token verbosity 冒充候选翻转。

## Outcome 与比较边界

- Gameplay：VALID_48M_COMPLETION，以 fresh events 的 48 次月份推进、同一 session 和 Runner exit 0 为依据。
- Runtime：RUNTIME_ADHERENCE_FAIL，原因是两次 tool-route error 与未能证明压缩后恢复合同。
- Strategy：PROMOTION_FIRST_ADHERENCE_FAIL，一条 note 使用了内部数值；季度 Main Action 的总体方向仍是公开进展/结果。
- Evidence：EVIDENCE_DISCIPLINE_FAIL。
- Recovery：RECOVERY_PATH_FAIL。
- Mechanism：MECHANISM_NOT_TRIGGERED。
- Score：STALE_SCORE_DIAGNOSTIC_ONLY。score_report 的 session_id 为空；S07-40 quantitative score、competition partial、score-based survival、grade、score dimensions 一律 UNKNOWN / EXCLUDED。事件序列的等级状态和公开维度仍按轨迹表报告。
- Runner score file 记载的 token usage 为 42,632,664 input / 254,782 output / 42,887,446 total，报告的 cost 为 0.0；由于 score_report 没有 game_session_id，这些 usage 只作为 drive-run diagnostic，不作为已绑定单局 usage。实际 billed cost UNKNOWN。
- 历史参考值：v7g 54.52、v6 75.29、v1 #1 76.04、v1 #2 35.31。S07-40 没有可验证绑定的 score，因此不赋予高于/相近/低于方向。任何 score/survival improvement、stable 80+ 或 hidden-test transfer 均未证明。

## Validation flags 与 FORENSIC_HOLD

configs/current_candidate.json 更新为 provider_validated=true、gameplay_validated=true；runtime_validated=false、long_horizon_adherence=false。score_improvement_proven、survival_improvement_proven、stable_80_plus_proven、hidden_test_transfer_proven、next_game_authorized 保持 false。NEXT_GAME 仍需 Main 单独授权。

S07-38 pre-game provider failure 的原始 evidence 继续保持 FORENSIC_HOLD。S07-40 只证明后续时点 provider 能产生 gameplay responses，不能确定 S07-38 的历史根因；建议 Main 在单独审阅 S07-38/S07-39 证据后决定是否解除，当前不解除、不删除。

## FACT / INFERENCE / HYPOTHESIS

- FACT：本局新建 session ID 为 cec080dd3c1d43a0b9cb92945e9a824e，与旧 v7g ID 不同；201 次 observe 绑定新 ID；Runner exit 0；events 推进到 current_month 49；score_report 的 session_id 为空；200 次 emulator take_action 成功，另有 2 次错误工具路由；日志记录 23 个压缩事件；一个 action note 有数值型 HiddenRisk 引用。
- INFERENCE：current_month 从 1 到 49 且 Runner 正常退出，支持 48 个月单局到达；因 score session 未绑定，成绩和 score-derived terminal fields 不可采信。机制在首评审前未出现合格结果兑现动作。
- HYPOTHESIS：若后续要验证 result-realization prior，应在下一次获准且身份可核对的单局中，先保证 Delivery lifecycle 有当前局公开回执，再观察首评审前是否出现合法的结果兑现候选。本报告不授权下一局。

## Raw evidence

原始 evidence 不入 Git。完整路径、bytes 和 SHA-256 清单见本机 evidence-manifest.json（3,990 bytes，SHA-256 7c798ddcc695e8f93162f82cca4f7219a716d6f8fec84a7fd59fe1ef7a25d6ba）。关键文件：

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| events-20260928T112740Z.jsonl | 2,118,740 | a1c3bae1b775de9771a1e7ba3bfea4383f684f743b22ecfddd621c4b0399010c |
| transcript-20260928T112740Z.log | 717,388 | 63ec49b1421e8f1763f69063dc121aea297a037895980d3b690b1853dea01683 |
| score_report.json | 2,719 | 9d7fd5edcf3d91d8fcdec518740e5b6cfd6caec9edd4f36b1c9da9686c612033 |
| runner-result.json | 98 | d0f9aa6071fa63458ce7a4b502bd22313d19ff55f71e148315ad67bccb6cdd19 |
| runner-console.log | 391,978 | 4c1a6ab36d86b45a9113ff7d6506f6050cceb66d75a750ff4e686e70ec05a493 |

首个 M6 Review feedback、202 个 take_action notes、service-log copies 均保存在同一清单指向的原始 artifacts 中；没有任何 shared DB 内容被读取或留存。

## TASK_RESULT / Main Raw Re-Audit amendment

- Fresh gameplay identity：cec080dd3c1d43a0b9cb92945e9a824e，与旧 v7g session 不同；48 个月完成。
- Score：64.0 / 44.8 / 48m / B，由 fresh final observe 与 transcript 绑定；空 score_report.session_id 保留为 Runner 字段缺陷。
- Classification：Gameplay VALID_48M_COMPLETION；Runtime FAIL；Promotion-first PASS_WITH_LIMITATIONS；Evidence FAIL；Recovery FAIL；Mechanism NOT_TRIGGERED_WITH_DELIVERY_ADHERENCE_LIMITATION；Decision closure SEVERE_VERBOSE_DELIBERATION。
- Formal promotions：M6 / M12 / M30 / M48。
- Canonical validation flags 保持 provider/gameplay=true、runtime/long-horizon=false；所有改善/迁移证明=false；next_game_authorized=false。configs/current_candidate.json 与复核结论一致，因此未改动。
- S07-38 FORENSIC_HOLD 保留。raw evidence 保留本机；本轮没有重读、重算或更改其 hashes。
- 后续三个 correctness patch 是 Main 的建议，本次仅修正 S07-40 事实记录；不改 Skills，不授权下一局。
