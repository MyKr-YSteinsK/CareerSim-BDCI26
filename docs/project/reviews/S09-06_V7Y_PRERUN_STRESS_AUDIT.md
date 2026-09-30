# S09-06｜v7y Run 前跨场景压力审计

## 1. Identity / decision

- Status：`OFFLINE_AUDIT_COMPLETE / PASS_WITH_KNOWN_LIMITATIONS`，提交前为 `IN_FLIGHT_EVIDENCE`；不替代 Stage 验收。
- Base：`main@89f0bfb4d13af87980a41c0b2075586e33a1e597`；加载时 `HEAD=origin/main`、working tree clean，fetch 后一致。
- Candidate：`candidate-v7y-story-exposure-guard`；Parent：`candidate-v7x-fresh-binding-reauthorization`。
- 范围：只审当前 written contract 与已接受公开场景；没有 LLM replay、模拟 hidden outcome、生成新策略或预测未选项效果。
- Final decision：`S09_06_V7Y_PRERUN_CONFIDENCE_AUDIT_PASS_WITH_KNOWN_LIMITATIONS`。
- 37 cases：**PASS 30 / AMBIGUOUS_ACCEPTABLE 5 / STATIC_CONFLICT 0 / INSUFFICIENT_PUBLIC_EVIDENCE 2**。
- 主要限制：成长代价/comparability 不完全可见；kernel 没有独立重复 no-promotion 的恢复类型；Delivery lifecycle 与实际规则消费仍待本 Candidate 的 runtime evidence。
- Final commit、remote/clean：由包含本文件的交付 Git commit 和 TASK_RESULT 给出，不自引用文件所属 commit。

## 2. Evidence provenance / frozen identity

Primary sources：[S09-05](S09-05_STORY_EXPOSURE_GUARD.md)、[S09-04](S09-04_RESOURCE_TRAJECTORY_INTERVENTION_FORENSICS.md)、[S09-02](S09-02_FAILURE_FLOOR_HIGH_SCORE_JOINT_FORENSICS.md)、[S08-11](S08-11_HIGH_SCORE_CORE_RECOVERY_FORENSICS.md)、[Candidate Evaluation Contract](../CANDIDATE_EVALUATION_CONTRACT.md)。矩阵中的历史事实取自这些已接受报告的 public context、legal menu、public status 和正式 Review；不从 raw 私有字段取策略。下表 events 本轮仅做 bytes/SHA256 核对，不重新解析整个事件流。

| Run / exact report | Exact events location | bytes / SHA256（本轮全部 PASS） |
|---|---|---|
| v4 / [health forensic](../runs/v4-run1-health-forensic.md) | `.career_sim_runner/career_emu/outputs/local-s06-adaptive-controller/20260924T160806Z/events-20260924T160806Z.jsonl` | 263552 / `9bf8bed1d02435047df40300ff306231dfa938b91cb87d3ef5b082e35d7359e5` |
| v6 / [validation](../runs/v6-run1-validation.md) | 同一 output root 下 `20260925T094419Z/events-20260925T094419Z.jsonl` | 2061570 / `2cce87eb6afd8aea5a9651f75621ae7c2b303e8c00c7f2ac417dc65c030371d8` |
| v7d / [validation](../runs/v7d-run1-validation.md) | 同一 output root 下 `20260927T143425Z/events-20260927T143425Z.jsonl` | 756124 / `e4e388517aff115747fabe068a76b1bc3d960b43900373d4eca804097348be78` |
| v7o / [validation](../runs/v7o-run1-validation.md) | `artifacts/dev-runs/s08-run01-v7o/events.jsonl` | 2067779 / `b6eb500f9e8ad3966e595e65a5d558c2c8b50097bf908fd8b93a1b5f14567df4` |
| v7t / [validation](../runs/v7t-run1-validation.md) | `artifacts/dev-runs/s08-run03-v7t/events.jsonl` | 1892046 / `c630579d5ebbcdbcecf9f6eee1104434b75cb92a9f3915cdbf4a5c1084e21fdb` |
| v7v / [validation](../runs/v7v-run1-validation.md) | `artifacts/dev-runs/s08-run04-v7v/events.jsonl` | 2066164 / `646af2df08655410bd0aa3b046983ac1be5797d2332682f7669c9756c55780b4` |
| v7w / [validation](../runs/v7w-run1-validation.md) | `artifacts/dev-runs/s09-run01-v7w/events.jsonl` | 1263074 / `62b4ad52660b0a8fc937aeab2f51c62063d108d4775f90ff253a1ff3c974561e` |
| v7x / [validation](../runs/v7x-run1-validation.md) | 同一 output root 下 `20260930T131104Z/events-20260930T131104Z.jsonl` | 376682 / `8e757e1f207c54c10c7ce9281bf8169c086b916e3ebac8784784775ec557be4a` |

S09-04 public-only derivative：`.local/scratch/s09-04/resource_trajectory.json`，130914 bytes，SHA256 `c152f7de094b38e98cf2941063af32aeeda2ce1bf625daacae70d6e705cc9a69`，本轮 identity PASS。O/A/O 序号采用 S09-04 的 decoded transport 去重口径，不与旧报告另一 transport 位置混计。

| Protected file | bytes / SHA256 | HEAD Git blob |
|---|---|---|
| `configs/current_candidate.json` | 5295 / `9630f45d13d9708f11623fbc266753126cee0552b6e088dc3ed20240fdc8b8aa` | `c5d92b65effc33c177dbf90c257380ade307351d` |
| `configs/runtime_manifest.json` | 7005 / `0f3b44466e0f16fd21a3d3724ffe890a9f4114dcc69088d20b238bbea115489d` | `0e01a6f0cc871b15e67a1cbd39c4e438ba6ff842` |
| `skills/structured-state-board/SKILL.md` | 5252 / `e2f31a83b357f2f75b1e2c0e8285fba440a17d3c4c4c8d6587b4f2e5fa9f366c` | `611e75d97234131acd5f321b5c7b75f50c1960ef` |
| `skills/delivery-progress/SKILL.md` | 5041 / `200b6c83aaca43f6dccfe58a30e23e79463e930512ef89cf5b19070a9d5d7528` | `64e060b1febf746a05aa07494755a7f9d6eee600` |
| `skills/rolling-planning/SKILL.md` | 13840 / `8bbf7379b08323910de41d1d8ae647e09c9b5ab68c239581da5c37223ef4e291` | `90573097588d63e5182d0b7a509b2580e10ca009` |
| `skills/risk-review/SKILL.md` | 4189 / `6da910fa60b07dfdccfc78a840ebc4777fc39e3188358e69ee483c89606874fd` | `e602fe1a3343a28b472259ae46cfca780e780e48` |

Decoded manifest instruction：**4984 characters**，UTF-8 SHA256 `3e382913dbcbe0a936726cd8aa5a2e61c32bdff107f3622fedd55326179e517b`。Runner identity `f61c738c72e51b77298cc1c14c7c6ebf4b6c527d` 从 current Candidate 读取，未执行 Runner 或改 frozen runtime。九项 validation flags 仍全部 false。

## 3. Replay matrix

**阅读约定：**以下 MODE 是 v7y 合同预期，不冒充历史运行模式；v4/v6 没记录的 MODE 仍 UNKNOWN。Guard 列使用完整枚举；`Conflict?=NO` 只表示文本无矛盾，不代表路径有效。所有 A 行都受独立 fresh material binding evidence 的 S 分支约束；低数值、普通疲劳、未晋升本身不授权 S。条件不足时保留原 Portfolio/Delivery/Risk 比较，不能制造低成本替代或 hidden 收益。

### A1. Resource / Story exposure（13 cases）

每行依次说明 current exposure、合法减曝、comparability 与 tradeoff。公开减曝语义不等于已证明 Health 恢复。

| Case | Public evidence | Applicable owner | Expected MODE | Main ranking rule | Guard applicable? | Conflict? | Verdict |
|---|---|---|---|---|---|---|---|
| R01 KTV | v4 M1 #4，O51/A53/O59：已有头疼，HRBP 邀第二场；拒绝或半小时露脸合法 | Planning + Risk | A；急性 material 证据另审 | exposure YES、lower YES；HRBP 接触/晋升价值损失与半小时 comparability 未知，不能自动选最短参与 | AMBIGUOUS_BY_DESIGN | NO | AMBIGUOUS_ACCEPTABLE |
| R02 感冒同事 | v4 M5 #19，171/173/179：重感冒、他人打喷嚏、项目紧；WFH 建议或顶紧急任务 | Planning + Delivery + Risk | A | exposure YES、lower YES；WFH 的协调/交付成本与顶岗成长价值未知；给同事休息不等于自己减曝 | AMBIGUOUS_BY_DESIGN | NO | AMBIGUOUS_ACCEPTABLE |
| R03 深夜 API | v7x M1 #3，43/45/51：23点非明确紧急询问，领导赞即时回应；次日回复合法 | Planning | A | exposure YES、lower YES；回复边界降低夜间工作，但即时认可代价/comparability 未确定，不能从事后 H-2 补出低成本 | AMBIGUOUS_BY_DESIGN | NO | AMBIGUOUS_ACCEPTABLE |
| R04 暴雨 | v7x M3 #9，91/93/99：橙色预警、小伞；拼车 AA 合法，W1 | Planning + Risk | A；material safety/affordability 须分别举证 | exposure YES、lower YES；AA 支出可承受性与成长比较未知，低 W 不自动 S；material warning 需 Risk gate | AMBIGUOUS_BY_DESIGN | NO | AMBIGUOUS_ACCEPTABLE |
| R05 香水头疼 | v7x M4 #16，147/149/155：浓香已致头疼；委婉请求喷淡 vs 忍耐/背后吐槽 | Planning；Risk quick gate | A | exposure YES、lower YES；直接减少暴露，无公开 binding obligation/高价值成长牺牲；低成本边界请求保 optionality | GUARD_SHOULD_APPLY | NO | PASS |
| R06 P0 支援 | v7x M5 #20，179/181/187：一周夜间驻场 vs 远程两小时，自己本周交付 | Delivery → Planning → Risk | A / DELIVERY 可用 | exposure YES、lower YES；远程保留帮助且保护自身近期交付，S09-04 判 I3。只在不损交付的可比候选内应用 guard；不宣称远程等价于全部 P0 ownership | GUARD_SHOULD_APPLY | NO | PASS |
| R07 上游拖延 | v7x M6 #23，203/205/211：迟交迫使熬夜；对齐交接排期 vs 默默熬夜/群内点名 | Delivery + Planning | A / DELIVERY 可用 | exposure YES、lower YES；对齐安排推进同一交付，无明确成长牺牲，保 optionality；不等于交付已验证 | GUARD_SHOULD_APPLY | NO | PASS |
| R08 跨组评审 | v7x M4 #17，155/157/163：深读评审额外3–4天，拒绝保本组排期 | Planning + Delivery | A | exposure YES、lower YES，但跨组责任/影响与投入代价显著，comparability 不成立；无证明的 binding delivery 不能凭排期泛化否决 | GUARD_SHOULD_NOT_APPLY | NO | PASS |
| R09 减投入/跳槽 | v7x M7 #28，243/245/251：非正式投入 vs 技术/HRBP/跳槽准备减少投入 | Planning + Risk | A | 减少当前组织投入可见，但净身体保护未知，迁移/连续性/晋升 tradeoff 高；不授权 guard 或 numeric-only S | GUARD_SHOULD_NOT_APPLY | NO | PASS |
| R10 面/末班地铁 | v7x M3 #10，99/101/107：湿肩、雨增；热面听项目困境 vs 赶地铁 | Planning | A | exposure YES；哪项净减曝及 comparability 均 AMBIGUOUS，进食保暖与早点回家不能先验排成身体收益 | AMBIGUOUS_BY_DESIGN | NO | AMBIGUOUS_ACCEPTABLE |
| R11 terminal-near | v7x M7 #29，251/253/259：继续关系 vs 技术；随后 M8 H0，跨月 mixed | Board + Planning | active 时 A；game.ended 后停止 | lower NO proven；两项无直接修复/减工作证据；不能将技术当休息或反推本可救援，也不能将早终局当 final-horizon 48m | GUARD_SHOULD_NOT_APPLY | NO | INSUFFICIENT_PUBLIC_EVIDENCE |
| R12 顶岗排期 | v4 M6 #21，187/189/195：本人排满、节点近、吃力；向领导争取排期 vs 独自加班 | Delivery + Planning | A / DELIVERY 可用 | exposure YES、lower YES；协商合理排期服务原交付，公开低成本减曝；guard 与 Delivery 同向，不替代验收 | GUARD_SHOULD_APPLY | NO | PASS |
| R13 acute physical | v7v M10，validation RESOURCE 段：心悸、胸闷、手抖，短 S 后 A；跨月 H6→8 | Board STICKY + Planning RESOURCE + Risk | S 需当前 acute binding；下一 fresh observe 重授权或 A | 明确 acute danger 由 material constraint gate 决定；没有普通低成本 A guard 替代 S。+2 为 mixed，不证明剂量/固定退出 | GUARD_SHOULD_NOT_APPLY | NO | PASS |

R06：guard 兼容远程两小时与本周交付，不足以证明它相对所有可行候选具有唯一最高值；Delivery exception 本身也能支持该 choice，因此不得将实际选远程计作已证 guard-caused override。R05/R07/R12 是 written prior 能明确覆盖的低成本语义；原局已选择其中多项，不构成 v7y 新收益证据。

### A2. Donor growth protection（6 cases）

| Case | Public evidence | Applicable owner | Expected MODE | Main ranking rule | Guard applicable? | Conflict? | Verdict |
|---|---|---|---|---|---|---|---|
| G01 Mentor | v6 M7/L2 A28，seq253→259：高密度带教、两周独立上手，H6→4（S09-02 §6） | Planning + Risk | A | 公开责任/成长价值不能仅因显式身体代价被否决；未证低曝同价值替代，cost 不自动触发 S；明确优势时 Portfolio 主导 | GUARD_SHOULD_NOT_APPLY | NO | PASS |
| G02 key project | v6/v7o M1–18 Main 各6/6 Apply；S08-11 §4、S09-02 §3 的公开选择族 | Planning | A | Main 高价值责任/广义复利仍 strong default；Main 不是当前 Story guard 范围。历史频次不变成 quota，v7q同频也失败 | GUARD_SHOULD_NOT_APPLY | NO | PASS |
| G03 Review prep | v6/v7o M6/12/18 到 L2/3/4；Output preparation clean GAIN 分别12/17次，另有 NO_GAIN（S08-11 §4；晋升见 §3） | Board + Planning | A | checkpoint 前可兑现且仍 responsive 的准备可有方向权重；不强制所有 Output action，Review grade 未保留仍 UNKNOWN | GUARD_SHOULD_NOT_APPLY | NO | PASS |
| G04 Network | v6/v7o Network maintenance 各6 clean GAIN、各2 NO_GAIN；v7o M36 A149/M43 A182 非正式参与控制底线 | Board + Planning + Risk | A | Energy 不在 guard 范围；Story 非正式投入存在机会成本，未证同值低曝替代则 Portfolio 比较。不得把全部社交等价为安全 filler | GUARD_SHOULD_NOT_APPLY | NO | PASS |
| G05 visibility/ownership | v6/v7o public key-project/报告成长族及 S08-11 §4 的 Main/response donor；Main Apply 全局14/16、10/16 | Delivery + Planning | A | 公开可兑现 ownership/可见结果保持 strong prior；普通 receipt 不验证结果；本审计只确认类别未被禁止，不证明每项 outcome 或未选项劣势 | GUARD_SHOULD_NOT_APPLY | NO | PASS |
| G06 weekend delivery | v7o M18/L4 A74，seq613→619：周末推进项目争取周一上午交付，H10→8（S09-02 §6） | Delivery → Planning + Risk | A / DELIVERY 可用 | time-sensitive realization 在 guard 之前；普通 overtime 成本不否决明确近端高值路径，低曝若毁交付不满足 guard | GUARD_SHOULD_NOT_APPLY | NO | PASS |

**EVIDENCE：**合同没有静态禁止上述 donor classes。**INFERENCE：**在“公开成长优势明确且不存在 material constraint”的条件下，Portfolio/Delivery 能保住该优势。**UNKNOWN：**模型是否实际比较到这些价值，以及原 donor 每个未选项的完整 comparability、对 v7y score 的效果。未给固定答案/比例，也未将历史已选项一律判最佳。

### A3. Trust / compliance / continuity（5 cases）

| Case | Public evidence | Applicable owner | Expected MODE | Main ranking rule | Guard applicable? | Conflict? | Verdict |
|---|---|---|---|---|---|---|---|
| T01 confidentiality | v4 M3 #9，91/93/99：离职竞对同事托付含保密资料；拒收并建议合规交接合法 | Risk gate；Planning 排候选 | A；material crisis 独立证据才 S | confidentiality 须 Full Review；不把拒收当 Health，普通合规 choice 不长期 S；不预指定 ALLOW/RECONSIDER，取决 final candidate | GUARD_SHOULD_NOT_APPLY | NO | PASS |
| T02 screenshot/leak | v7x M6 #22，195/197/203：截图泄漏与合规警告；劝删工作话题 vs 吐槽等 | Board + Planning RISK + Risk | 通常 A/RISK；material 危机可 S | 一次 reparative containment 后 fresh observe；再次须同风险仍在/再升或新同类警告，guard 不抢 owner | GUARD_SHOULD_NOT_APPLY | NO | PASS |
| T03 fresh warning | v7v validation RISK：M12/21/45 cleanup；M44 新 warning 先于 M45 | Planning RISK；Risk final gate | 通常 A/RISK | warning authorizes bounded cleanup，不自动 RECONSIDER；无关新证据不授权重复，完成后回主线 | GUARD_SHOULD_NOT_APPLY | NO | PASS |
| T04 retaliation/trust | v7x M2 #6，67/69/75：会上甩锅、客户责任争议；时间线/邮件可澄清。当前证据未建立 credible retaliation/material trust crisis | Board + Risk + Planning | 本例不凭摩擦进 S；真正 material threat 才 S | trust cue 不等于 physical exposure。普通争议的 gate 可审，但本 cohort 所选片段不能验证危机修复的实际 effectiveness | GUARD_SHOULD_NOT_APPLY | NO | INSUFFICIENT_PUBLIC_EVIDENCE |
| T05 income/job | v7x M7 #27，235/237/243：涨薪/项目/晋升挽留，按离职根因判断；v7d W0 后继续数月（S09-02 §4） | Planning + Risk | A；fresh explicit continuity/affordability binding 才 S | 挽留/薄 W 不自动等于危机；若实质危机，修复绩效/关键交付也可 relief，guard 不损 continuity | GUARD_SHOULD_NOT_APPLY | NO | PASS |

T04 的不足是当前选取 public crisis 证据不足，不是合同矛盾；没有扩 raw cohort 或调用 runtime 补证。真正危机的 recognition、materiality、exit 由 §5 schema 收集后审，不能凭普通争议冒充已 exercise。

### A4. Delivery（5 cases）

| Case | Public evidence | Applicable owner | Expected MODE | Main ranking rule | Guard applicable? | Conflict? | Verdict |
|---|---|---|---|---|---|---|---|
| D01 near commitment | v7o A74 周一交付；v7x #20 自己本周交付（G06/R06来源） | Delivery → Planning | A/DELIVERY | 可公开证明 near obligation 先于普通 Portfolio/guard；低曝若损交付就不满足 guard；不是看到任何 work 就 NEAR | GUARD_SHOULD_NOT_APPLY | NO | PASS |
| D02 blocker | v7x #23 迟交迫使兜底；v7v D4 临发布未测代码/跳过 CI（validation DELIVERY） | Delivery + Planning + Risk | 通常 A/DELIVERY | 修 blocker、保 safe release certainty；guard 不能选破坏 binding 交付的轻松项。R07低曝协商可兼容但不代替实际修复 | GUARD_SHOULD_NOT_APPLY | NO | PASS |
| D03 pending NOT_NEAR | v7v notes 长期 IN_PROGRESS/UNVERIFIED；报告不能给每项 near linkage，不能将 pending 全部升级 | Delivery 提供事实；Planning 排序 | A | 普通 IN_PROGRESS+NOT_NEAR 且无 blocker/linkage 作背景；本行是合同条件分支审计，不断言历史每个 D4 都 NOT_NEAR | GUARD_SHOULD_NOT_APPLY | NO | PASS |
| D04 unverified high value | v7v D4 containment 后 structured evidence 仍 UNVERIFIED，text claims 与 marker 不同（validation §Delivery） | Delivery + Planning | A/DELIVERY，限当前有可验证 legal path | 高价值未验证且当前可验证才例外；没有验证动作证据不臆造；receipt/praise/promote 不验证 career result | GUARD_SHOULD_NOT_APPLY | NO | PASS |
| D05 exploration | v7d M14 sprint 排满、明确交付底线仍申请探索（S09-02 §4/§8） | Delivery → Planning | A/DELIVERY；material continuity 另审 | 已排定近端交付先于 speculative gain；不从 M15 terminal 推出探索导致终止；guard 不将守交付归成永久保守 | GUARD_SHOULD_NOT_APPLY | NO | PASS |

D03/D04 的 PASS 是“缺少 near/验证证据时合同如何处理”的静态分支，不是该局完成 Delivery fidelity。历史 unverified/text mismatch 正是后续取证需保存的限制。

### A5. Progression / Review / NO_GAIN（8 cases）

| Case | Public evidence | Applicable owner | Expected MODE | Main ranking rule | Guard applicable? | Conflict? | Verdict |
|---|---|---|---|---|---|---|---|
| P01 M6 C/no | v7w M6 C/no promotion，无 standout；v7x M6 C/L1 Output gap（各 validation） | Board → Planning | A/PROGRESSION | 重建下一真实 Review，找 still-responsive path；不因差 grade/未晋升 S，也不保留上一 Story guard | GUARD_SHOULD_NOT_APPLY | NO | PASS |
| P02 M12 missed | v7v M12 C/L2/no，后 M18 B/L3；v7w M12 C/L1/no（validation） | Planning | A/PROGRESSION | checkpoint miss 是修复信号，不是不可逆或长期 S 授权；两条不同结果不证明恢复因果 | GUARD_SHOULD_NOT_APPLY | NO | PASS |
| P03 fresh specific | v7x M6 public Output/visible-result gap（validation）；responsive/can realize 尚需新证据 | Board + Planning | A/PROGRESSION | fresh+specific+responsive+checkpoint 可兑现才能短期 dominant；gap 本身不足压所有其它价值 | GUARD_SHOULD_NOT_APPLY | NO | PASS |
| P04 nonspecific | v7w M12 neutral/under observation；v6/v7o 未留 Review grade（S09-02 §3，S08-11 §3） | Board + Planning | A/PROGRESSION；grade UNKNOWN 不补 | 缺 specific gap 使用 DIRECT_PROGRESSION_EVIDENCE，保护 GAIN/UNKNOWN 广义成长；没有 feedback 不捏造单维 quota | GUARD_SHOULD_NOT_APPLY | NO | PASS |
| P05 old gap/new Review | v7w M18 D，carrying work through/communication 新反馈；无 captured reset（validation） | Planning owns rebuild | A/PROGRESSION，除非另有 fresh material threat | Formal Review 重建整个 Portfolio/next checkpoint，旧 Output dominance 不自动继承；历史未记录不能当合同已执行 | GUARD_SHOULD_NOT_APPLY | NO | PASS |
| P06 clean NO_GAIN | v7w M18 Output immediate repeat；M21 Network/Output repeat 后有 public gains（validation NO_GAIN） | Board → Planning | A | local Level/context discount，fresh response 后扫描其它 responsive path；有 alternative 不 immediate same-path；后续 gain 反驳 permanent cap | GUARD_SHOULD_NOT_APPLY | NO | PASS |
| P07 Level reset | v6/v7o M6/12/18 public Level change（S08-11 §3） | Board facts → Planning | A | Level change S/N/O 全 UNKNOWN，重新开放，不携旧 NO_GAIN；旧 gap 也按 Review 重建。历史 Board reset adherence 未代证 | GUARD_SHOULD_NOT_APPLY | NO | PASS |
| P08 multidimensional | donor key-project public 多维成长族；v7x #24 高强度工作 advertised Output且 H 成本（S09-04 §5） | Board + Planning | A | 一维 clean NO_GAIN 仅折扣该维，保其它 GAIN/UNKNOWN；非 Story action 不触发 guard；不能将高强度工作从 label 改为 Skill，也不能凭 Health 成本整体否决 | GUARD_SHOULD_NOT_APPLY | NO | PASS |

**跨窗口结论：**v7y written contract 可以保留 early compounding，首次 Review 前有 broad growth/reliable delivery；但没有将合法菜单比较变成可独立证明的 operational execution。v7w M1–6 已弱，长 S 在 M18 后才出现，不能把后期 mode 修复等同于已恢复首次晋升。

## 4. Salience / conflict audit（11 invariants）

K 数字是 `configs/runtime_manifest.json` 的 **decoded `instruction.splitlines()`** 行号，不是 JSON 文件行号；CRITICAL KERNEL K14–25，OWNER K6–12。P/B/D/R 是当前 Planning/Board/Delivery/Risk `SKILL.md` 实际行号。定位稳定到 §2 hashes。以下分类评估结构可见性，不测量 attention、记忆或 LLM adherence。

| Invariant | Manifest occurrence / salience | Owning Skill occurrence / salience | Classification |
|---|---|---|---|
| hard floor, not maximization | K15，kernel 首句 | P46–50、78、103，长期目标/资源退出 | REDUNDANT_BUT_CONSISTENT |
| A default | K15、19、21；执行前 kernel | P3、50、90–103、126；描述/明确 MODE 门禁 | REDUNDANT_BUT_CONSISTENT |
| Portfolio/broad strong default | K19，独立 kernel 段 | P129–134；ranking #2 strong default，首次 Review P64 | CLEAR |
| Primary Gap advisory | K17/19，Review 与条件 dominance 相邻 | P61–64、119、131–132；fresh/specific/responsive/expiry | REDUNDANT_BUT_CONSISTENT |
| no-promotion → A/PROGRESSION | kernel 未直接写出该 trigger→RECOVERY；K15仅 A default，K10拥有 failure recovery，K56恢复 RECOVERY | P64、68–72、92–103 明确；B58–80排除 bad review 的 binding STICKY | TOO_WEAK_TO_RELY_ON（kernel 单独）；完整 bundle 规则清楚 |
| fresh-binding S reauthorization | K15 失效/独立 fresh evidence/unresolved 连续重授权/最低稳定化 | P90–103；Board STICKY P之外由 B58–80事实支持 | REDUNDANT_BUT_CONSISTENT |
| NO_GAIN discount+positive allocation | K23 + K52强制 fresh Board/new Planning/有 alternative 不重复 | P107–120、169–173；B82–99 clean facts/Level reset | CLEAR |
| Formal Review rebuild | K17/19 重建、不继承、dominance expiry | P52–64完整 Level/response/capital/feedback/Delivery/checkpoint清单 | CLEAR（细项依赖 owning Skill） |
| guard current/low-cost only | K21独立段，positive条件及numeric/generic/old/unknown/high-tradeoff排除 | P133一个 ranking bullet；当前 choice 失效 | REDUNDANT_BUT_CONSISTENT |
| time-sensitive Delivery exception | K19首句优先；K21不得损 binding delivery | P86、128排第一；D78–106 relevance/NEAR/evidence非数字倒计时 | CLEAR |
| terminal direct realization | K25，kernel最后独立段 | P139–143，48m/nofutureReview/当前兑现 | CLEAR |

Conflict scan：**CONFLICTING=0**。

1. K21 与 P133 都要求 current explicit exposure、合法低曝、可比成长且不明显损 delivery/continuity/highvalue；没有 trigger/expiry 反向条件。`safety` 的 Story 意义不授权 guard 接管 Risk gate。
2. ordinary workload 本身既不触发 S，也不触发 guard。后者须当前明确 exposure 与 low-cost/comparable，且仍 A；它是局部 option preference，不是 hard floor 最大化。
3. guard 位于 Portfolio 内，time-sensitive realization 位于其前；其自身 binding Delivery exclusion 再次限制。没有 guard override scheduled near delivery 的文本。
4. NO_GAIN 的 kernel 缩写仍保 local Level/context、positive reallocation、多维、不 cap/no filler；K52保 fresh-observe 禁 immediate-repeat。Coverage 与 Level reset 的完整细节在 P118/B97，不能将 kernel 当四 Skills 替代物。
5. Review kernel 保留重建与 dominance expiry；细项压缩后仍由 P52–64持有。对比 v7x base `da5359d2d9a978475484300cf1f4a75013393329` 的原 kernel，no-promotion→PROGRESSION 原来也没有独立句；所以该弱显著性 **不是 v7y compression 删除既有 invariant**，不触发本 Plan 的“丢失 invariant”失败条件。
6. M1–M6 已有 P64 的 broad/reliable-delivery signal 与 P130 strong prior，但没有显式 first-window intent artifact；历史 v7w 的 plan/Delivery缺口与同样 key-project频次失败，使真实执行仍 UNKNOWN。不得加 quota/bootstrap 弥补。

**Known salience risk：**kernel 依赖 owning Skill 提供 PROGRESSION taxonomy、Review重建清单、Level-reset/coverage与细致 comparability；4984 characters 不等于模型在压缩后可靠消费全部义务。没有静态冲突，未做任何文案加强或 correction patch。

## 5. S09-RUN03 v7y offline forensic schema design

本节只是一份供下一 Run Plan 采用的离线 schema；**没有执行 S09-RUN03，没有修改 runtime policy/notes/工具协议，没有 live authorization**。也不与历史 S08-RUN03/v7t 混同。

### Common identity / measurement discipline

- 每行：`run_id, candidate_id, source_file_sha256, game_session_id, observe_seq_before, action_seq, observe_seq_after, month_before/after, Level_before/after, choice_label/description, public_basis, evidence_class`。
- `public_basis` 只保存 participant-visible event description、合法 menu、白名单状态、正式 Review、实际 public result 和已有同局四 Skill/CTRL/DL输出。public text 与 assistant rationale 分栏；不复制 hidden/private字段，不读 shared DB/private Provider config。
- action attempts / success / rejected / unknown receipt 单独记录；去重同 tool-call transport。无法建立同局 freshness 的 pair 为 UNKNOWN，跨月/Review/Level/批处理为 MIXED，不反算 hidden effects。
- 每项计数附 `eligible_n, observed_n, unknown_n, source_refs`；不存在完整来源不能写0。正常 gameplay 的既有 observe 能审，不能为报告增加 observe/MCP/provider/status mutation。
- schema 是 offline 分类标签，不能新增 MODE/RECOVERY、状态或执行 trigger。仅 observable compression/resume signal 才计 recovery；无 signal 为 UNKNOWN，不假装0或已检测。

### C1. Every Story exposure

```text
event_public_description; legal_choices_public
current_exposure = YES|NO|AMBIGUOUS
lower_exposure_option = YES|NO|AMBIGUOUS
low_cost_comparable = YES|NO|AMBIGUOUS
guard_applicable = YES|NO|AMBIGUOUS
comparison_basis; tradeoff_delivery; tradeoff_income_job; tradeoff_progression
actual_choice; subsequent_public_result; pair_attribution
guard_recognized_in_existing_output = YES|NO|UNKNOWN
guard_decision_attribution = EXPLICIT|COMPATIBLE_ONLY|UNKNOWN
```

用当时 menu/context 标前四项，再独立列结果；不能看到 H下降才回填 SHOULD_APPLY。现象“选了低曝”只计 selected-compatible，除非已有明确 Planning rationale，否则不能计 guard-caused override。R06同时满足 Delivery 是典型双解释，保存 dual-compatible。

### C2. Promotion engine by exercised windows

分别输出 M1–M6 / M7–M12 / M13–M18（未走完注明 partial；未到达 NOT_EXERCISED）：

```text
meaningful_progression_opportunities: public offered value + decision/menu identity
selected / skipped / UNKNOWN; comparison_quality
Main_action_family; Energy_allocation_by_family_and_budget
public S/N/O trajectory with observe refs; Review_grade; Level_before/after; promotion
current_gap; next_realizable_checkpoint
Delivery_override_count; Story_guard_override_count; Risk_or_S_override_count
explicit_override / compatible_choice / UNKNOWN denominators
```

“meaningful”须公开 advertised progression/ownership/visibility/可兑现结果支持，不靠 eventID。重复 Q-E fresh菜单按决策次数计，另列季预算、剩余 Energy，不把一个预算多次展示叫独立机会供给。selected/skipped 是菜单行为记录，是否 ranking错必须有可比公开值；无反馈不替换 grade。override count只有已有明确理由时能归因，其余兼容/unknown单列，不能用 choice 反推动机。

### C3. Every formal Review reconstruction

```text
review_source; grade; Level_before/after; promotion/no_promotion
old_gap; old_checkpoint; new_feedback; new_gap; next_checkpoint
old_plan_expired = YES|NO|UNKNOWN
explicit_rebuild_evidence; first_post_review_action_and_existing_PLAN/CTRL
first_action_alignment = SUPPORTED|NOT_SUPPORTED|UNKNOWN
```

旧 gap 与新 gap 同字串不自动判失败：依据新 feedback/response 重建可得到同方向。只没看到 literal plan标 UNKNOWN，不能捏造重建；新 D feedback 后仍机械继承需记 evidence而非心理推断。最后 horizon无后续Review改 direct-realization，无 postterminal action则NOT_EXERCISED。

### C4. Every advertised S/N/O pair and next response

```text
advertised_dimensions; public_before; public_after; Level/context
pair_class = CLEAN|MIXED_OR_UNATTRIBUTABLE|UNKNOWN
dimension_result = GAIN|NO_GAIN|UNKNOWN
Board_response_seen; next_Planning_response
immediate_same_path_repeat = YES|NO|UNKNOWN
responsive_alternative_available = YES|NO|UNKNOWN
positive_reallocation = YES|NO|UNKNOWN
multidimensional_partial_discount; Level_reset_all_UNKNOWN_seen
```

clean需同局 fresh前后、明确 advertised dimension、无跨Level/Review/自动批次等混杂。不同维度分别判，不能把未 advertised 的变化归动作。NO_GAIN重复只有 fresh response、下一选择和 responsive alternative 都可证才判违规；替代价值不清标UNKNOWN。后续 clean GAIN可覆盖旧NO_GAIN；Level变化全UNKNOWN。数值不变不推出 hidden cap。

### C5. Every fresh warning / continuity event

```text
warning_type; exact_public_basis; freshness; materiality = MATERIAL|ORDINARY|UNKNOWN
Risk_result = PASS|ALLOW|WARN|RECONSIDER|UNKNOWN|NOT_CAPTURED
cleanup_action; prior_cleanup_ref; repeat_authorizing_public_evidence
MODE; RECOVERY; binding_basis; next_observe_reauthorization_basis
exit_evidence; returned_A_action_ref; unresolved_same_threat_or_new_warning
reconsideration_branches; final_R; RB
```

分别审 RESOURCE / trust/compliance/confidentiality / income-job / delivery，不用一个 Health解释全部失败。WARNING 不自动 Full Review/RECONSIDER，只有 final candidate material consequences触发；一次cleanup后无关证据不授权再清理。S每次 fresh evidence独立重证，尚明确 unresolved可续S，不能把持续本身判死锁；旧reason或numeric-only续S另记。Exit unknown不宣称resolved。

### C6. Every potentially active Delivery

```text
public_item_identity; session_local_id; cursor_reliability
commitment/owner/dependency; focus; checkpoint; public_proof_basis
recognized = YES|NO|UNKNOWN; active_count; relevance_before_first_Review
Planning_override = EXPLICIT|COMPATIBLE_ONLY|NO|UNKNOWN
lifecycle_claim; evidence_status; public_completion_basis; recognition_link
lifecycle_completion = PUBLICLY_VERIFIED|CLAIMED_ONLY|UNKNOWN|NOT_EXERCISED
note_vs_transcript_mismatch; overclaim; retirement_basis
```

potential item是公开工作线索，不因为 notes未跟踪就删。near、blocker、当前可验证高价值才 exception；NOT_NEAR pending背景化。最多3 active、ID不复用、工具success不等careerresult、genericpromotion不等recognition link；历史D4仅text称verified而marker未transition，必须保留不一致并审 publicproof。

### Diagnostic routing / runtime and efficiency

| Failure branch | Necessary public evidence | Distinguishing evidence / limits |
|---|---|---|
| Resource | fresh暴露、菜单、trajectory、terminal公开原因 | guard eligibility/实际choice、预算空档与有机会未选分开；missing final repair不编可救反事实 |
| Promotion | 每个Review grade/Level/feedback与窗口成长opportunities | responsive机会未选、缺机会、NO_GAIN错误、旧gap、Delivery真实override分别列；不推hiddenpromotion公式 |
| Trust/continuity | warning/crediblethreat、candidate后果、合法repair、freshreturn | 缺危机证据标UNKNOWN，不能靠H/W或cleanup次数证明危机解除 |
| Delivery | 公开commitment/checkpoint/result与lifecycle | 未识别/未排序/未执行/未验证分层；noresult不自动策略失败 |
| Adherence/complexity | 同局freshflow、Board/Delivery/PLAN/Risk/preflight、observable恢复 | rules存在与实际消费分开；missing marker、不一致和真实违规分开，不能把token多直接当attention失败 |

另沿 Candidate Evaluation Contract四组记录 score/floor/behavior/efficiency：observes、attempts/success/fail/unknown、execution boundaries、continuation sends、provider zero-work failures、tokens、observable compression/reread/recovery sequence、wall time。均取exact existing artifacts/run window；缺 usage为UNKNOWN不为0。只有清理后exact offline audit；先secret scan，再决定所需安全归档，不修改现有holds。本schema提供必要分类和来源要求，但实际日志是否足够、是否缺 artifact为下一 Run 的证据限制，不保证每项可观测。

## 6. Confidence calibration

本轮没有找到需继承的数值概率基线，不造百分比。以下是有界工程判断；静态一致性与下一局可诊断性增强，**v7y score/survival/runtime adherence 置信度不因本审计上调**。

| Target | Execution confidence | Failure-floor confidence | Promotion-ceiling confidence | Adherence confidence |
|---|---|---|---|---|
| 48m completion | 同谱系v7v已有48m执行存在性，v7y包静态有效；本Candidate未run，技术完成不保证 | 有A内减曝/独立bindingS的合同可行性；v4/v7x早终局与末端无明确保护限制，48m仍未验证 | 对完成同时保成长的静态路径未被禁；早晋升非生存必要充分条件 | fresh runtime shell与reset规则存在；v7y guard/Review/Delivery消费未验证 |
| 70+ | runner/包能提供审计证据的设计支持，不是70+执行证明 | 同上；floor未兑现就无法支撑高分路径 | v7o71.83/v6 75.29证明历史不同Candidate可达；当前donor类未被静态压制，v7y70+未知 | kernel/Skill一致，operational比较及firstReview执行未验证；不从旧分迁移 |
| 75+ | 相同受限执行判断，无新run evidence | 保留成长与floor的权衡未实测 | v6单局75.29存在，但v7y earlyengine/L6未知；高于70目标证据更窄，不给稳态保证 | NO_GAIN/rebuild/Delivery语义缺口尚需capture；不因静态PASS提高score断言 |
| 80+ | 无本Candidate完成/80+ evidence | 无稳定floor证明 | 所选donor最高75.29，80+未观察；stable80+ unsupported | 即使后续完整adherence也不证明80+；本轮adherence仍未验证 |

**Execution总体：**离线identity/合同可用性有直接支持；“本候选将完整执行”只有限条件支持。**48m/70+/75+：**可检验假设，未验证，工程判断维持；**80+：**当前证据不足。没有把37静态cases、46历史tests或donorco-occurrence当收益/因果统计。

## 7. Future directions（记录，不实施）

- `SEMANTIC_CUE_DICTIONARY = CANDIDATE_FUTURE_DIRECTION`：暴雨、身体症状、workload与continuity的识别存在自然语言adherence风险；尚未证明识别是主要瓶颈。只有下一局区分recognition与ranking后再评估，禁止event/title→answer映射。
- `FIRST_REVIEW_BOOTSTRAP = POST_RUN_DIRECTION`：首次Review有broadprior但 operational ranking可靠性未知；若机会充分且早窗仍错配，再交Stage评估，不预置M6/月数/Apply/SNO quota。
- attention/complexity reduction：kernel对完整Skill细项的依赖是knownlimitation；优先取证实际遗失规则，不能现在加强措辞形成第二行为变量。
- Delivery lifecycle fidelity：已有D4 unverified/textmismatch与v7w malformed历史，schema覆盖识别/排序/执行/验证；是否需要补丁交后续证据与Stage。
- resource opportunity prior：历史有保护已选仍terminal、未知tradeoff及预算空档，不足支持固定buffer/恢复配额/FRAGILE状态，暂不实施。

## 8. Verification / permissions / result

- current Candidate identity、九flagsfalse、manifest4984chars/hash、四Skillbytes/hash/blob PASS；exact八run events与S09-04derivative rehash PASS。
- 手工矩阵，未写extractor/自动模拟；因此无scripted generation/deterministic extractor rerun/test义务。复用 **S09-05 46 passed**：代码、测试及protected identity无漂移；本轮没有新增/运行tests，没有把旧PASS冒充新runtime证据。
- 只写本报告与compact CURRENT_STATE；protected Candidate/manifest/allSkills/Runner/dependencies/retry/HPL/FORENSIC_HOLD未变。allowed-path检查、37项唯一ID/八列/verdict计数、13个本地来源链接、`git diff --check`、canonical `scripts.archive_run_evidence._scan` 对两份交付文档均 PASS。protected identity 分别核验本机原始bytes/SHA256与Git规范化内容；CRLF工作文件不直接与LF Git blob做raw-byte等同比较。
- 不归档未扫描raw、sharedDB、privateconfig或unrelatedproviderlogs；仅引用exact来源，本轮没有扩展历史取证或live查询。

```text
provider=0
service=0
MCP=0
game=0
install=0
reload=0
Candidate behavior mutation=0
NEXT_GAME=NOT_AUTHORIZED
HPL_COORDINATION_IMPACT=NONE
FORENSIC_HOLD=UNCHANGED
```

**Final Decision：**`S09_06_V7Y_PRERUN_CONFIDENCE_AUDIT_PASS_WITH_KNOWN_LIMITATIONS`。返回Stage评估独立S09-RUN03 Game Gate；本审计不授权游戏、不修改任何Candidate validation flag、不宣布Stage完成。
