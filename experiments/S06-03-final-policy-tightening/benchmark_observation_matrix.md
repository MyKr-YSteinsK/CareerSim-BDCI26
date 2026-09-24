# S06-03 后继 Benchmark 观测矩阵

本矩阵仅供未来由 Main 单独授权的 Game Gate 使用，不构成运行授权。它承接 S06-01 [`benchmark_observation_matrix.md`](../S06-01-adaptive-controller-static/benchmark_observation_matrix.md)，并针对 v3b 新增或收紧的合同更新观测项。没有触发机会时记为 `NOT_OBSERVED`，不得算作机制失败。

状态定义：`PASS` = 可见行为符合候选合同；`FAIL` = 有直接可见证据与合同矛盾；`NOT_OBSERVED` = 本局没有相应触发或机会；`UNKNOWN` = 来源、新鲜度、归因或工具可见性不足。单局结果只能描述行为与结果，不能证明因果收益、稳定 80+ 或泛化。

| # | 观测项 | 来源与测量 | 状态 | 单局限制 |
|---:|---|---|---|---|
| 1 | 候选与提交身份 | 检查实际提交包 Candidate ID、四个 Skill 与 runtime manifest/instruction hash 是否等于 v3b 冻结身份 | PASS / FAIL / UNKNOWN | 身份通过不证明运行时完整遵循 |
| 2 | 每季度 checkpoint | 按公开月份和时间戳统计每季度第一次 Energy 决策前是否以 fresh public state 刷新/创建 checkpoint | PASS / FAIL / UNKNOWN | transcript/tool 可见性可能不完整 |
| 3 | Checkpoint 与全文重读解耦 | 分别计季度 checkpoint 数和 rolling-planning 全文重读数；季度变化本身不应触发全文重读 | PASS / FAIL / UNKNOWN | 工具调用缺失时不能推断模型内部读取 |
| 4 | 条件性全文重读 | 逐项记录初始详细规划、半年反馈、严重公开后果、continuation/context loss、checkpoint 语义过期/歧义或无法还原 procedure 是否触发重读；未触发的类别记 `NOT_OBSERVED` | PASS / FAIL / NOT_OBSERVED / UNKNOWN | 单局可能没有所有触发条件 |
| 5 | Early / mid / late Planning | 按公开月份分段，统计有效 checkpoint、Primary Gap 与证据来源；覆盖早/中/晚期 | PASS / FAIL / UNKNOWN | 缺少部分 trace 时标 UNKNOWN |
| 6 | 普通选择的目标排序 | 检查普通 story choice 是否先过 Material Risk，再按 Primary Gap、次级公开收益、Soft Cost/机会成本、UNKNOWN 排序 | PASS / FAIL / NOT_OBSERVED / UNKNOWN | 单个选择不能证明排序稳定 |
| 7 | AVAILABLE 下的正向 controlled aggression | 在无 fresh Material Risk、Risk Budget=AVAILABLE、公开证据显示某合法选项对 Primary Gap upside 明显更强且额外成本主要为 Soft Cost 时，检查是否优先高 upside 路径 | PASS / FAIL / NOT_OBSERVED / UNKNOWN | 机会未出现时不是失败；单局不能证明收益 |
| 8 | 相近或 UNKNOWN upside | 若 Gap upside 接近或未知，检查较低 Soft Cost/暴露路径是否仍可合理优先，而非机械激进 | PASS / FAIL / NOT_OBSERVED / UNKNOWN | 情境依赖，单局不估计长期价值 |
| 9 | TIGHT 下的 Material Risk 保护 | 出现 fresh Material Risk 时检查 Risk Budget=TIGHT、Risk Skill 对当前候选的 review 及合法 mitigation 比较是否未被增长收益压过 | PASS / FAIL / NOT_OBSERVED / UNKNOWN | 没有风险触发时记 NOT_OBSERVED |
| 10 | Primary Gap 进展而非局部正反馈 | 检查 `ADVANCING` 是否由 Gap 本身的可比改善或直接相关公开 progression evidence 支持；单独 praise、bonus、关系改善不得升级为 ADVANCING | PASS / FAIL / NOT_OBSERVED / UNKNOWN | 一次局部信号不能证明路线结果 |
| 11 | Advertised 与 observed effect | 对重复战略动作对照菜单 advertised effect 和同局可比 observed delta；检查是否优先可靠 observed effect | PASS / FAIL / NOT_OBSERVED / UNKNOWN | 顺序关联不代表因果 |
| 12 | 两 checkpoint STALLED switch review | 同一 action / 同一 Gap 在相邻可比 checkpoint 均无进展时，检查是否标 STALLED 并比较不同类型合法 alternative；一次 miss 不得强制切换，STALLED 也不强制选 alternative | PASS / FAIL / NOT_OBSERVED / UNKNOWN | 没出现连续停滞时记 NOT_OBSERVED |
| 13 | Context-loss session 恢复 | continuation/context loss 后确认 CareerSim `game_session_id`，先取 fresh public observe，再重建当前 Board | PASS / FAIL / NOT_OBSERVED / UNKNOWN | framework 未暴露 context loss 时可能 UNKNOWN |
| 14 | Bounded recent-effect recovery | 必要时最多检查最近 5 条同局 public log，最多恢复 2 组可比战略 action/effect；记录日志范围、条数、配对字段与来源 | PASS / FAIL / NOT_OBSERVED / UNKNOWN | 日志不可见时不得猜测或扩大回放 |
| 15 | Recovery 归因与 UNKNOWN fallback | 检查跨事件/动作污染、缺 before/after 或归因不直接时效果被标 UNKNOWN/省略；fresh observe 优先于旧 log | PASS / FAIL / NOT_OBSERVED / UNKNOWN | 不允许从顺序推断因果 |
| 16 | Session 隔离 | 检查新 game 的 Board、recent_effects、Gap 和风险背景是否清空；不得出现 durable/cross-game Memory | PASS / FAIL / UNKNOWN | runtime persistence 可能不可观察 |
| 17 | Horizon pressure | 使用公开当前月份与 48-month horizon，观察 stalled Gap 下的近期可见 progress 与远期不确定收益取舍，不推断 promotion month/threshold | PASS / FAIL / NOT_OBSERVED / UNKNOWN | 晋升机制仍未知 |
| 18 | Ordinary-event oscillation | 统计无新证据时普通事件候选反复重开/反转次数；检查最多比较两个 strongest legal candidates，仅 fresh evidence 或 `risk-review=RECONSIDER` 才重开 | PASS / FAIL / NOT_OBSERVED / UNKNOWN | 单局频率不代表总体振荡率 |
| 19 | 季度主行动 lock-in | 统计连续季度是否机械重复同一 action；在 public no-progress 后检查 checkpoint/alternative review 是否发生 | PASS / FAIL / NOT_OBSERVED / UNKNOWN | 重复本身不等于错误或因果 |
| 20 | 月度里程碑公开状态 | 若到达则记录 M6/M12/M18/M24/M36/M48 的 Level、Wealth、Skill、Network、Output、Health；未到达的月份记 `NOT_OBSERVED` | PASS / FAIL / NOT_OBSERVED / UNKNOWN | 只作描述性轨迹 |
| 21 | 晋升与 Wealth 线索 | 记录公开 promotion month、feedback、wealth-related option 与可见 trade-off；不得推导 hidden threshold 或把同步变化归因于单一机制 | PASS / FAIL / NOT_OBSERVED / UNKNOWN | salary/promotion/event 等贡献可能不可分解 |
| 22 | 最终结果与运行成本 | 若可得，记录 score dimensions、quantitative/competition partial score、survival、grade、input/output/total/cache/by-model usage、reported cost 与 runtime；缺失记 UNKNOWN | PASS / FAIL / UNKNOWN | 分数不是静态 PASS 条件，单局不证明稳定性 |
| 23 | 技术失败分类 | 依据 Runner/provider/service/MCP/game evidence 区分技术失败与游戏内 outcome；未知字段保持 UNKNOWN | PASS / FAIL / UNKNOWN | 不因部分日志缺失推定原因 |
| 24 | 职责与唯一提交者 | 确认 Board 只整理事实、Planning 拥有 Primary Gap/Risk Budget、Risk 只审当前候选、Trace 仅 marker；Single Agent 是唯一成功 `take_action` submitter | PASS / FAIL / UNKNOWN | 只覆盖可观察调用轨迹 |

任何未来单局均不得将静态合同 PASS 或单局行为解释为 v3b 因果收益。Stable 80+、云端行为和 promotion/wealth 隐藏机制仍需各自证据；本任务没有运行 benchmark。
