# S10 Experience-Routed Policy Atlas｜离线蒸馏

S10-08 在 `main@8267d420da29888d0a05403991f8980e251aaa0c` 的 frozen v8a 上建立一个 branch-only v14。研究对象是知识表示与选择性暴露：六张按功能情景触发的程序卡、fresh Decision Capsule、全选项一次比较、公开事实上的两步浅前瞻。它保留存活约束内的晋升优先和广义复利；没有新模型、Team、跨局 Memory 或检索服务。

**FACT**：下列来源已包含足够的公开衍生证据，本任务没有重开 raw history、私有 DB、held transcript 或游戏。**HYPOTHESIS**：当前模型更容易在小而相关的程序上下文中执行这些规则。**UNKNOWN**：Flash 是否按需检索、稳定坚持规则，以及分数或生存是否改善。历史关联不能证明路线因果。

## 1. 来源与正负对照

| 来源 | 使用事实 | 限制 |
|---|---|---|
| [S08-11](../reviews/S08-11_HIGH_SCORE_CORE_RECOVERY_FORENSICS.md) | v6 75.29/48m/L6、v7o 71.83/48m/L5；两者 M6/M12/M18 连升、低于较弱路线的 Output Energy 占比 | 候选和运行正确性混杂；attention dilution 只是 plausible hypothesis |
| [晋升前沿](S10_PROMOTION_FRONTIER_REPORT.md)、[汇总](S10_POLICY_MINING_SUMMARY.json) | 10 局、1,626 转移、64 Review/30 晋升；v8a RUN07 72.65/48m/L5、RUN10 68.40/48m/L5；负参考 RUN08 59/48m/L4、RUN20 60.60/48m/L4、v12 23.48/24m/L1 | 126 Main 全部跨月 MIXED，101 项目转移不是净收益；不存在已证晋升公式 |
| [经验 Playbook](S10_EMPIRICAL_HIGH_SCORE_PLAYBOOK.md) P01–P10 | 同月同 Level Energy 响应、结果阶梯、项目条件、普通成本和公开危机 | 小样本类别与跨月相关不得升级为硬效果 |
| S10-06 已接受报告 `7bd7c92fb43e4642077469cc6d316eaf15a7979f:docs/project/runs/v13-run01-empirical-policy-validation.md` 及 companion compact JSON | v13 34.01/36m/L4；公开警告被错误排除、E1 提交成本2清理、局部 flat 重复、剩余 Energy recipe、no-advance 后重复旧路径 | 只读取该分支的接受报告/compact identity；未合并分支或复制 raw；单个决定是否导致 terminal UNKNOWN |

具体对照改变了程序，而不是仅缩短全局规则：

- **可兑现交付**：RUN07 选择短交付后公开反馈按时且业务满意；RUN08 长自研随后延期。但 RUN19 延期后仍 M6 晋升，因此只能在当前 owner/依赖/窗口支持兑现时偏向短结果；不能记住原事件答案或保证晋升。全部 Main 跨月，回报归因 MIXED。
- **局部响应**：clean report 109 gain/33 flat，network 40/16；同 family/Level 的下一次重复仍有 9 flat/5 gain。v12 某一阶段 Output flat 后，较晚不同条件又 gain。程序折价已测维度，重新审视其它维度和 material context；既不永禁 family，也不假定 Output cap。
- **广义成长**：v6/v7o Output Energy 比例 36.6%/45.5%，弱参考 v7t/v7v 为52.2%/55.8%；不能从相关性推出固定比例。保留 responsive Network/Skill/Wealth/成果价值，在完整菜单中比较。
- **结果真实性**：v12 完成 CI 并未 M6 晋升，RUN20 对齐/原型不等于完成交付；高参考也有未被词法标签识别的晋升。结果阶梯有助于区分承诺、完成、认可，既不是隐藏条件，也不是必要晋升公式。
- **普通成本与危机**：四条高参考 clean Story 负 Health 分别19/19/22/20次，仍48m；RUN20 H10 仍低分，v12 H7 早终局。急性健康公开恶化、工作连续性/诚信升级与普通疲劳需要分别判断，不能用统一数字保护阈值。
- **公开警告不是隐藏库存**：v13 排除公开 HR 警告、爆雷后修复不可负担、随后继续增长且无同范围 clearance。23 条 cleanup 六维皆 flat 也不能证明无隐藏收益或已解除风险。保留当前未解除警告，最小公开可行修复；不反推存量或次数。
- **正式反馈应改变路径**：v13 M12 有实际变更，但 M18/M30 主要续 intensive-work/project/报告路线。程序要求明确旧路径响应、下一不同可兑现方向和检查点；若继续原路，必须有新独立公开价值。

## 2. 24 条候选经验的去重与拒绝

HIGH 指公开输入/执行合同或足量局部响应支持，**不表示高分收益已证**。MEDIUM 是正负对照支持可迁移程序但反事实未知；LOW 只能作条件性软先验。每条先识别情景、对照结果、提炼最小程序，再加例外。表内 `Lxx` 仅为研究编号，运行卡不含它们。

| ID / 功能情景 | 正负对照 → 保留程序 | 例外/边界 | 结论 / 落点 |
|---|---|---|---|
| L01 当前证据 | fresh pairs 可审；Main 混合、v13 receipt 不证明状态 → 每步重建 capsule | 不明字段 UNKNOWN；不补完整历史 | KEEP HIGH / core |
| L02 成本可行性 | 合法 choice 不等于可负担；v13 E1清理成本2被拒 → 提交前查显式成本 | 可选不可负担项由 core 排除；必要修复受阻才 material guard | KEEP HIGH / Energy |
| L03 局部 flat | 109/33 与9/5重复反例 → 折价该 family/维度，比较 responsive alternative | 新 Level/资源/依赖重评；其它维度仍可有价值 | KEEP HIGH / Energy |
| L04 每步重排 | v13 fresh observe齐全仍预排批次 → 一个动作后丢弃剩余 recipe | 保留目标，不保留动作数量/序列 | KEEP HIGH / core、Energy |
| L05 窗口兑现 | 短交付按时与长自研延期 → 当前窗口能验收的结果优先 | 明确质量约束、长资产也可兑现、已正常按时交付 | KEEP MEDIUM / Project、Review |
| L06 结果阶梯 | 已承诺/泛夸与公开完成/认可有差别 → 确认 owner、承诺、完成、认可 | 无标签不等于未完成；认可不保证晋升 | KEEP MEDIUM / Project |
| L07 条件 ownership | v6 项目14/16高参考 vs RUN08 16/16低参考；v13 9/11项目仍失败 → 检查承载、依赖和兑现 | 被阻塞/无结果/有危险时比较替代 | KEEP MEDIUM / Project |
| L08 警告可采性 | v13 HR排除错误与信任terminal → 公共风险文本可用于判断当前约束 | 普通软提示不是自动 material；禁 hidden stock | KEEP MEDIUM / Trust、guard |
| L09 同范围退出 | Health/泛夸/receipt 与未解信任并存 → 仅同范围 fresh clearance 解除 | 新证据证明从未 material 可正常退出；不永久锁软提示 | KEEP MEDIUM / guard |
| L10 接受普通成本 | 高参考负H仍48m vs 高H低参考 → 普通成本排在成果后 | 急性安全/工作连续性仍先修复 | KEEP MEDIUM / Health、core |
| L11 no-advance 重排 | 高参考复利 vs v13 反馈后复述旧路 → 下一窗口改变有证据支持的路径 | 原路有新的独立价值可保留并说明 | KEEP MEDIUM / Review |
| L12 广义成长 | 高参考非Output独占、Network/学习有响应 → S/N/O/W及成果机会同看 | 学习样本仅6，不保证全局收益；当前交付义务可优先 | KEEP MEDIUM / Growth |
| L13 剩余 horizon | 公开剩余时长限定兑现；末期未来价值有未知 → 比较剩余期可实现性 | 不虚构下一Review；当前低成本长期资产仍可有独立用途 | KEEP LOW / Review |
| L14 早期复利 | v6/v7o早连升与较弱迟升相关 → 早抓可兑现责任及多维成长 | 不固定月份、比例或晋升概率；独立因果未知 | KEEP LOW / Review |
| L15 回执即成果 | 与 L01 同一个事实新鲜性问题 | 保留 receipt≠状态/验收约束 | MERGE → L01 |
| L16 泛夸即完成 | 与 L06 同一个结果证据阶梯问题 | 同范围认可要显式证据 | MERGE → L06 |
| L17 广告项目总最高 | 与 L07 同一个承载/依赖问题 | 广告预期不替代兑现 | MERGE → L07 |
| L18 flat后机械永久退出 | 与 L03 同一个响应作用域问题 | 只在 material context 改变后重评 | MERGE → L03 |
| L19 高Health解除信任 | 与 L09 同一个跨领域clearance错误 | 危险领域不能替代 | MERGE → L09 |
| L20 逐调用等于重规划 | 与 L04 同一个批次意图问题 | fresh observe不证明真正重比较 | MERGE → L04 |
| L21 Output固定cap | 局部flat与后来gain矛盾、hidden规则禁用 | 不进入运行资产 | REJECT |
| L22 每个Main固定项目 | 项目频率和分数不单调，跨月MIXED | 不进入运行资产 | REJECT |
| L23 全局最大Health | 高H不保护工作/信任，也不保证高分 | 不进入运行资产 | REJECT |
| L24 固定早晋升公式 | 同公开数值可分歧，延期仍可晋升 | 不进入运行资产 | REJECT |

计数：**24 = 14 KEEP + 6 MERGE + 4 REJECT**；最终独立经验 HIGH4 / MEDIUM8 / LOW2。六张卡总体 HIGH1（Energy）、MEDIUM5，其内 Review 明示 early compounding/horizon 为 LOW。弱相关没有升级成硬规则。

## 3. 六张局部程序与结构差异

| 功能程序 | 当前触发与行动程序 | 防止的失误 |
|---|---|---|
| Review / promotion | 临近窗口或新正式反馈 → 可兑现结果/响应/广义成长 → 更新目标和下一检查点 | 复述旧路径、固定月份晋升、虚构未来Review |
| Energy / resource | 显式成本/本步配置 → 排不可负担 → 局部响应及独立价值 → 一个动作后新观察 | recipe、永久cap、flat清理即解除 |
| Project / delivery | Main责任或当前承诺 → owner/依赖/验收/兑现时间 → 当前更可实现路径 | 总选项目、泛夸即完成、过度自研 |
| Trust / compliance | 当前责任/保密/可靠性 → 是否material → 透明合法修复与同范围确认 | 隐瞒、排除HR警告、Health代替信任修复 |
| Health / survival | 当前急性安全/负荷安排 → 最小必要恢复及交接 → 公开检查点 | 数字阈值、无依据补满Health、长期停止成长 |
| Visibility / network / learning | 普通成长 → 多维响应/成果可见度/当前学习用途 → 兑现与option value | Output独占、所有学习/关系成本都避开 |

与 v13 的全局 R2–R9 不同，完整策略没有放入 Planning 再要求模型在每步过滤：启动只读 core；atlas 仅负责语义路由，一般读取一张 `WHEN/OBJECTIVE/PREFER/AVOID/LOOKAHEAD/EXCEPTIONS/EVIDENCE` 卡；guard 只在重大约束当前存在时加入。Fresh capsule 是替换式局内工作状态；一次比较所有合法项，对每项看即时公开效果和下一可见 checkpoint 的兑现/不确定性。不存在 MCTS、隐藏 world model、递归 self-critique 或第二 planner。

**迁移接口**是功能情景和公开事实，不是 event/title→choice。运行文件不含历史 run ID、事件编号、原选项索引、score表、私人效果或公式；研究来源不会被打入 Skill bundle。Capsule 的局内 clean response 不跨局保存。所谓选择性暴露不保证宿主删掉旧 tool output；旧卡可能仍在历史中，实际峰值上下文只能后续有界运行测量。

## 4. 外部研究的用途

仅借鉴表示方式，不移植其算法，也不把论文结果当 CareerSim/Flash 的验证： [ExpeL](https://arxiv.org/abs/2308.10144) 支持从经验提炼可复用 insight 的研究动机；[Agent Workflow Memory](https://arxiv.org/abs/2409.07429) 提供程序化 workflow 的动机；[Voyager](https://arxiv.org/abs/2305.16291) 提供可复用 Skill library 的动机；[HiAgent](https://arxiv.org/abs/2408.09559) 讨论长任务工作上下文管理；[RAP](https://arxiv.org/abs/2305.14992) 讨论规划与模型推理结合。本候选只做基于公开菜单的两步浅前瞻，没有树搜索、持久记忆、模型训练或外部检索。Plan 中其它研究名称不作为未核实的实现事实。

## 5. 交付与验证边界

六卡、三Skill、小 manifest、26个公开语义场景及 deterministic reference-preserving bundle 已形成；量化上下文、场景回放、接口源代码依据和所有验收项见 [静态 review / TASK_RESULT](../reviews/S10-08_EXPERIENCE_ROUTED_POLICY_STATIC_REVIEW.md)。场景由 Codex 对书面策略逐项离线审阅，fixture tests 核对记录完整性和可行性；**不是 Flash 行为评测**。不声称 gameplay、75+、稳定性、优越性、因果收益或 hidden-test transfer。

`NEXT_GAME=NOT_AUTHORIZED`。
