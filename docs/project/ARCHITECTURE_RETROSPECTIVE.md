# CareerSim BDCI26｜架构复盘

## 1. 架构问题

项目从 Single Agent 加最小 no-op Skill 起步，逐渐把事实整理、策略规划和候选风险判断拆成可读、可核对的职责，同时避免多个 Skills 各自成为策略 owner。最终提交架构是 **Single Agent + 3 Skills**；历史 v8a 工程版本采用四 Skills。两者描述不同时间点和不同工件，不应拼成一个不存在的最终 Candidate。

## 2. 核心架构如何形成

### 状态归属

`structured-state-board` 负责当前 session 的公开事实、来源、新鲜度和有限的可归因变化。它回答“现在能确认什么”，不替 Planning 选目标或替 Risk 判断候选。fresh observe 优先于旧摘要；来源不清时保留 `UNKNOWN`，不从时间相邻推断因果。

### 长时程策略

`rolling-planning` 是唯一 strategy owner。它将公开反馈、当前目标缺口、可见的资源/生存趋势和剩余可实现窗口放进一个滚动决策，而不是把固定动作配方或隐藏分数写成策略。Energy 与 Main 一起比较，但一个状态改变动作之后要先重新观察，不能用旧状态连续下令。

### 风险控制

`risk-review` 只审核已经生成的当前合法候选及其直接相关的公开重大后果。它能要求一次有边界的备选比较，但不拥有 Primary Gap、一般动作排序或最终提交权。这样避免 Risk 变成第二个 planner，也避免普通成本自动压过成长机会。

### 动作 authority 与交付生命周期

Single Agent 是唯一 `take_action` 提交者；Skills 提供整理、规划和候选风险判断，不各自提交动作。后来的 v8a 四 Skill checkout 加入 `delivery-progress`，把 commitment、证据、交付阶段和公开 recognition 作为独立生命周期追踪，避免把“声称完成”当作公开验证；它不决定目标、排序或风险。最终 exact v6 的冻结身份只含 Board、Planning、Risk 三个 Skills，`delivery-progress` 不属于那个 ZIP。

| Component | Owns | Does not own |
|---|---|---|
| Single Agent | 按公开状态选定并提交唯一动作 | 不复制第二个动作提交者或 reviewer authority |
| structured-state-board | 本局公开事实、freshness、来源和有限近期效果 | 不规划、不作风险结论、不建议动作 |
| rolling-planning | Primary Gap、进展、公开风险预算、剩余窗口和候选排序 | 不提交动作、不代替 Risk 审核具体重大后果 |
| risk-review | 当前候选的直接相关 Material Risk gate | 不设总体目标、不作全局策略 owner、不提交动作 |
| delivery-progress（历史 v8a） | 当前局交付项生命周期和公开验证状态 | 不拥有目标、动作排序、风险判断或最终动作权 |

职责依据 exact-v6 source commit `1114a04b75548cf52f030d123564e527060fc061` 的三个 Skill 文件、[最终身份](FINAL_SUBMISSION_IDENTITY.json) 和 [S06 closeout](S06_CLOSEOUT.md)。

## 3. 压缩恢复是执行正确性

压缩不只是提示词长度问题：恢复时若状态、session 或 Skills 没被正确重建，下一动作可能基于过时上下文。v6 的唯一完整运行出现两次 compressor epoch，之后未重读三个 Skills；还出现漏掉半年度 H 标记和普通 Story 无新证据却重开推理。它证明设计契约与运行遵循必须分开审计，不能因架构文本完整就声称 runtime adherence PASS。后续 v6b 补充了恢复契约，但最终冻结身份仍是原 exact v6；该补丁不转移到提交包。[v6 运行审计](runs/v6-run1-validation.md) · [S10-23R freeze audit](reviews/S10-23R_FINAL_SINGLE_SHOT_FREEZE.md)

## 4. 没有纳入最终架构的扩展

| Route | 实际证据 | 结论边界 |
|---|---|---|
| Durable Memory | 冻结 rail 的自动 `MEMORY.md` anchor 在启动、更新和模拟压缩后均缺正文；显式 read 可用。 | `MEMORY_NOT_DEPLOYABLE` 针对被测提交路径；没有证明 Memory 普遍无效，也没有测出策略收益。[S10-19-R2 feasibility](research/S10-19R2_MEMORY_FEASIBILITY.md) |
| Reviewer / subagent | 冻结 adapter 未注册 `verification_agent`，也没有已证的机械只读部署路径；质量阶段未运行。 | `REVIEWER_NOT_SAFELY_DEPLOYABLE` 是该 rail 的部署边界，不是对独立审查价值的否定。[S10-19-R1 feasibility](research/S10-19R1_SUBAGENT_FEASIBILITY.md) |
| Team / Swarm | 没有完成可行性实验。 | `DEFERRED / NOT_TESTED`，不能写成实验否定。[Architecture decisions](ARCHITECTURE_DECISIONS.md) |
| Deterministic helper | 临时 Skill 脚本在隔离冻结 tool rail 中读写有界公开状态并跨模拟压缩保留；真实 install/reset 后清除。 | 工具层 challenger 获支持；云端权限、模型是否调用与遵循未测，不是最终架构。[S10-19-R3 control audit](research/S10-19R3_NATIVE_CONTROL_SURFACE_AUDIT.md) |
| Replay controller | 24 个案例中有 1 个状态级修正，仍有 8 个 `UNKNOWN`；主要决策错误未证明被修正。 | `CONTROLLER_LOGIC_SIGNAL_WEAK`；没有形成 Candidate 或部署依据。[S10-20 controller research](research/S10-20_PROMOTION_WINDOW_CONTROLLER.md) |

这些路径解决的是不同层次的问题。单个局部可行性结果不自动升级成正式 Skill，也不与 exact v6 同义。

## 5. 复杂度与证据

有用的约束是 `Evidence → Hypothesis → Experiment → Decision`：先找到会改变决策的真实瓶颈，再做能区分替代解释的最小实验。S10 的策略挖掘得到 `STRATEGY_SIGNAL_WEAK`，控制器回放信号弱；模拟器 policy search 因冻结故事基线仅 2/16 完成而停在 feasibility gate，宏策略没有进入比较。这些结论都限制已测问题，不证明候选机制普遍无效。

架构 lesson 不是“多拆 Skill 就更可靠”，而是每个边界都要有明确 owner、输入和禁止权限；每项新增复杂度都要对应可观察的问题及部署证据。一个漂亮的责任表不能代替运行验证。

## 6. 两个并存的架构身份

| 用途 | 身份 | Skills |
|---|---|---|
| 最终提交包 | exact v6，source `1114a04b75548cf52f030d123564e527060fc061` | `structured-state-board`、`rolling-planning`、`risk-review` |
| 当前 main checkout | 历史 v8a 工程状态 | 上述三个加 `delivery-progress` |

最终包不会因当前 checkout 文件较新而被重定义；checkout 也不冒充最终包。详细打包身份见 [manifest](FINAL_SUBMISSION_MANIFEST.md)。

## 7. 架构经验

1. 一个组件只承担一个可说明的判断责任；最后动作仍只有一个提交者。
2. 新鲜公开状态优先，旧摘要不能覆盖当前观察。
3. 风险判断绑定到具体候选；一般策略只保留一个 owner。
4. 压缩后的恢复和动作顺序是执行正确性，要用运行证据检查。
5. 未通过部署门的设计保留为有边界的负结果，不以“以后可能有用”为由塞进最终包。
