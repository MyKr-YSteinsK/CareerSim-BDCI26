# S06-08｜v4 Run #1 Health 只读取证

## 结论

- Death pattern: `CUMULATIVE_ATTRITION`。Health 从 5 多次下降、曾回补至 4，随后又逐步降至 0；终局前已为 1，没有证据显示单个巨大打击把有明显缓冲的角色直接打到 0。
- `H_SURVIVAL_GUARD = SUPPORTED_FOR_TARGETED_PATCH`。证据支持把 Health 低位/持续下降纳入生存约束；不支持具体数值阈值，也不证明该修复会提高分数。
- 这是单局行为证据。各次 Health 变化的游戏内部归因不完全可见；不把时间相邻自动当作因果。

## Run / evidence identity

- Candidate: `candidate-v4-lean-runtime-policy`；parent `candidate-v3c-zh-aligned-policy`；运行时 manifest SHA256 `0da190f4b49e70572614db4317387def8033d5704cb80d6df79744c198f3e1da`；instruction SHA256 `80ee0176bc1c05723e6ee84027e50c179566ead6ae5de5b8eee8de5511591552`。
- Run `20260924T160806Z`；game session `fdcaa70a85f44662a6a329513c175676`；drive session `career-sim-runner-d527e58fce4e`；launch source `3e4019d092af4ac7f9ea554560927579b43d771f`。
- 三个当前 Skill Git blob：rolling-planning `fcd443d547920e04fcfa2dd948686136afb76d47`；structured-state-board `06ecdc3a598ee42d1e785d6e14af8f1a669eca85`；risk-review `50ac3c515d3e75ab060bb16e5afe51e79e4db3ab`。
- 本机 raw：`.career_sim_runner/career_emu/outputs/local-s06-adaptive-controller/20260924T160806Z/`。`events-20260924T160806Z.jsonl` 263,552 bytes, SHA256 `9bf8bed1d02435047df40300ff306231dfa938b91cb87d3ef5b082e35d7359e5`；`transcript-20260924T160806Z.log` 44,237 bytes, SHA256 `fe20250c032c67d5681b6a7dd726114182b97bc180ee94768f95f99fae99d896`；`score_report.json` 1,254 bytes, SHA256 `6f1f6e8d57b503cbc2d21d4f6017553042008dfb586ddd82bd271614a8854f88`。三者均与 `RUN_HISTORY.md` 登记值匹配，session ID 也匹配。
- Events 有重复的 transport delta/direct 记录；按 tool-call ID 去重后为 1 次 `new_game`、24 次 `observe`、23 次 `take_action`，终局 `alive=false / failed=true`。下表 `O` / `A` 是 events 文件中每个唯一调用的首条 seq；所有 `take_action` 返回成功。Score report 的空 ending_score 与死亡链无关，分数来源 caveat 见 `RUN_HISTORY.md`。

## M1–M6 Health timeline

`Health 前→后` 均由该动作前后的相邻 fresh observe 直接读取。`DIRECTLY_OBSERVED` 只表示状态变化被观察到；另列因果归因等级。

| # / 月份 | Event / selected action | Health 前→后 | Agent / Risk 证据 | 归因与 raw seq |
|---|---|---:|---|---|
| 1 / M1 | 新员工手册：继续 | 5→5 | 开局；无 Health 决策 | `DIRECTLY_OBSERVED`; O25→A29→O33 |
| 2 / M1 | 出差名额：支持同事并补充自身成果 | 5→5 | 以不树敌方式争取曝光 | `DIRECTLY_OBSERVED`; O33→A37→O41 |
| 3 / M1 | Code Review：提问式引导 | 5→5 | 兼顾带人与关系 | `DIRECTLY_OBSERVED`; O41→A45→O49 |
| 4 / M1→M2 | KTV：参加第二场、控制饮酒 | 5→3 | Agent 知道可能有 Health 成本，但以 H5 判断可承受、优先晋升委员会关系；事后称该事件 Health -2 | `DIRECTLY_OBSERVED`; `STRONGLY_ATTRIBUTABLE`; O49→A53→O57 |
| 5 / M2 | KTV 后续：表达项目兴趣、请教晋升准备 | 3→3 | 考虑是否显得功利；无 Health 变化 | `DIRECTLY_OBSERVED`; O57→A61→O65 |
| 6 / M2 | 出差后续：感谢并私下修复关系 | 3→3 | 关系修复；无 Health 变化 | `DIRECTLY_OBSERVED`; O65→A69→O73 |
| 7 / M2→M3 | 打印机冲突：礼貌沟通插队 | 3→3 | 效率与人际；无 Health 变化 | `DIRECTLY_OBSERVED`; O73→A77→O81 |
| 8 / M3 | 竞标答辩：用技术深度 / TCO 论证 | 3→2 | 菜单未公开 Health 成本；Agent 聚焦价值论证 | delta `DIRECTLY_OBSERVED`; 原因 `AMBIGUOUS`; O81→A85→O89 |
| 9 / M3 | 离职资料：拒收并建议合规交接 | 2→2 | 明确识别保密 / 合规 `Material Risk`，选择拒收 | `DIRECTLY_OBSERVED`; 正确处理公开风险; O89→A93→O97 |
| 10 / M3 | 奖项挂名：改以实际参与项目申报 | 2→2 | 避免虚假署名；无 Health 变化 | `DIRECTLY_OBSERVED`; O97→A101→O105 |
| 11 / M3, Q1 Energy | 健康恢复 | 2→4 | 明确称 H2 危险；在多轮摇摆后只选一次恢复（公开效果 +2），并保留 Network / Output 投入，而非双恢复 | delta `DIRECTLY_OBSERVED`; 效果与公开 status update 一致; O105→A109→O113 |
| 12 / M3, Q1 Energy | 人脉维护 | 4→4 | 追补低 Network；无 Health 变化 | `DIRECTLY_OBSERVED`; O113→A117→O121 |
| 13 / M3, Q1 Energy | 准备汇报材料 | 4→4 | 追补 Output；无 Health 变化 | `DIRECTLY_OBSERVED`; O121→A125→O129 |
| 14 / M3→M4 | Q1 主行动：申请关键项目 | 4→4 | Growth 主行动；无 Health 变化 | `DIRECTLY_OBSERVED`; O129→A133→O137 |
| 15 / M4 | 竞标后续：分阶段付款、量化 ROI | 4→4 | 商务答辩；无 Health 变化 | `DIRECTLY_OBSERVED`; O137→A141→O145 |
| 16 / M4 | 绿植忘浇水：补救并建提醒 | 4→4 | 补救；无 Health 变化 | `DIRECTLY_OBSERVED`; O145→A149→O153 |
| 17 / M4→M5 | 午餐：改为每周至少三天与同事吃 | 4→3 | Agent 明说 Health 成本“可能较小”，优先融入团队；月度推进同时发生 | delta `DIRECTLY_OBSERVED`; action attribution `AMBIGUOUS`; O153→A157→O161 |
| 18 / M5 | 午餐后续：恢复折中节奏 | 3→4 | 明确想保健康；选项未列 Health +1，不能把意图当作效果来源 | delta `DIRECTLY_OBSERVED`; attribution `AMBIGUOUS`; O161→A165→O169 |
| 19 / M5 | 生病同事：私下关心并帮顶急任务 | 4→3 | 推理着重同事情谊 / 团队交付，未讨论传染风险；后续公开描述工作排得很满 | delta `DIRECTLY_OBSERVED`; `STRONGLY_ATTRIBUTABLE` 但无显式数值机制; O169→A173→O177 |
| 20 / M5→M6 | 健康检查端点：立即修复并查同类服务 | 3→2 | 动作选项未显示 Health 影响；同时跨月并发生半年反馈 / 奖金 / 晋升 | delta `DIRECTLY_OBSERVED`; attribution `AMBIGUOUS`; O177→A181→O185 |
| 21 / M6 | 生病同事后续：向 Leader 说明顶岗并争取排期 | 2→2 | 理由明确提到避免独自硬扛 / 透支健康 | `DIRECTLY_OBSERVED`; O185→A189→O193 |
| 22 / M6 | 组会贬低工程工作：沉默、会后私聊 | 2→1 | 普通人际事件；事后 Agent 自己也不能确定 Health -1 是私聊还是事件结算 | delta `DIRECTLY_OBSERVED`; attribution `AMBIGUOUS`; O193→A197→O201 |
| 23 / M6 | 会后可见度：推动写入组级 OKR | 1→0 | Agent 明确称 H1 是真实 `Material Risk`，也想到任何 Health -1 都会淘汰；仍选成长路径并预期以后恢复。随即 terminal `眼前一黑` | delta / terminal `DIRECTLY_OBSERVED`; action mechanism `AMBIGUOUS`; O201→A205→O209 |

变化序列为 `5→3→2→4→3→4→3→2→1→0`。A23 是最后被观察到的 -1 转移，但没有独立事件日志能证明这 -1 由“推动写入 OKR”这一选项、随机结算或其他同时结算机制单独造成。未发现一次从有明显 Health 缓冲直接归零的巨大伤害。

## Risk / Planning / Board

- **Risk Review：`PARTIALLY_SUPPORTED`。** `risk-review` 文件在启动时读取一次；没有独立 Skill-call 事件，也没有可识别的结构化“状态 + 理由”输出（formal Risk-state outputs = 0）。M3 保密事件被明确识别并正确拒收；H2 时识别生存威胁并回补一次；H1 时明确说是 Material Risk，却仍选择成长。M5 生病同事事件有公开传染线索和居家办公选项，Agent 没有讨论暴露风险；是否达到 Skill 所称“严重 Health 后果”无法仅凭本局判定，作为潜在漏审而非确定 false negative。
- 原 RUN_HISTORY 中的“`RECONSIDER` 17 次”是大小写不敏感的普通英文推理词：精确大写状态标记为 0；普通 `reconsider` 共 17 次，其中 16 次发生在终局前、1 次在局后反思；约 10 次集中在 Q1 Energy 分配的同一决策窗口。它们不是 17 次 Risk 状态输出，也不能计为 17 个风险触发。未见 Risk false-positive 的证据；高频 deliberation 属于决策摇摆。
- **Board：**唯一明确的 `Board:` 快照在 Y1M1，记录 Health 5、fresh observe 和 `recent_effects: []`。此后虽有 fresh observe 和自由文本复述状态，但 M1–M6 没有结构化 Board refresh、Health trend 或 recent-effect 更新。Health 信息并非完全没进入对话；证据支持“结构化状态未保留趋势”，不证明这是死亡的单独原因。
- **Planning：**唯一明确的完整初始 checkpoint 同时罗列 Skill / Network / Output，并在“building foundation / Level progression / Skill primarily”间改写目标，未稳定维护单一 Primary Gap。Q1 Energy 前虽对 H2 进行了充分但冗长的权衡，最终是非结构化的多维平衡决策，没有可验证的六行 checkpoint / `Progress` 状态；`STALLED` 为 0。Q2 Energy checkpoint 未观察到，因为游戏在到达下一次季度 Energy 决策前已结束。游戏中的 Risk Budget 值未建立；唯一的 `Risk Budget` 字样出现在局后建议中。

## 历史存活局最小对照

- Candidate v1 #1（S04-03 Run #1，76.04 / 48 月）在 Git 历史 `8a93378a8d9ef5598e925048db39ee931e207bab:experiments/S04-04-high-score-confirmation/candidate_run1_trajectory.json` 中：M3 Energy 前 Health 4，选择健康恢复 + 人脉维护 + 汇报材料；M6 前 Health 3，选择两次健康恢复 + 汇报材料，M6 观察 Health 7。
- Candidate v1 #2（S04-04 Run #2，25 月）同一历史 commit 的 `candidate_run2_trajectory.json` 记录 M3 有一次健康恢复、M6 Energy 未恢复 Health；最终 Health 10，终止原因为第二次 trust crisis。它说明单纯恢复次数不能解释存活或成绩。
- 两个历史轨迹与 v4 是不同局、不同策略上下文，只提供描述性参照，不构成健康策略的因果比较。

## Root-cause classification

| 分类 | 状态 | 证据边界 |
|---|---|---|
| Environment / randomness | `PARTIALLY_SUPPORTED` | 有多段伴随故事推进的 Health 变化，但若干变化无法分离动作、事件和自动结算；单个巨大终局打击 `NOT_SUPPORTED`，损失是否可避免 `UNKNOWN`。 |
| Policy design | `SUPPORTED`（作为待修假设） | 当前合同没有“低位 / 持续下降 Health = survival reserve”的显式守卫；Agent 在 H2 做了部分回补，在 H1 明知存活风险仍先选 Growth。属于可复用规则缺口，不等于已证明造成全部分数损失。 |
| Runtime adherence | `PARTIALLY_SUPPORTED` | Skill 已加载，但只有初始 Board / checkpoint 可确认；Health trend 未结构化保留，普通推理反复摇摆，H1 下仍未让生存约束稳定优先。因果影响未证明。 |
| Technical | `NOT_SUPPORTED`（作为死亡原因） | raw 显示 23/23 `take_action` 成功，终局状态由同一 session observe 确认，Runner 正常到达游戏终止。score_report 的 DB 路径问题仅影响分数回读，不解释 Health 淘汰。 |

## Decision boundary

`SUPPORTED_FOR_TARGETED_PATCH` 仅表示可把 bounded、public-state-driven `H_SURVIVAL_GUARD` 交 Main 决定是否实施：低位或持续下降时把 Health 作为 survival constraint / Risk Budget `TIGHT`，暂缓普通成长投入直至恢复缓冲。没有提出或冻结任何 Health 数值阈值。Transcript 局后提出的 `Health ≤ 2` 是模型建议，不是已确认机制或本报告采用的阈值。

没有修改 Skill、instruction、Runner 或 runtime；没有重跑游戏。该报告不证明修复有效、v4 分数收益或稳定表现。
