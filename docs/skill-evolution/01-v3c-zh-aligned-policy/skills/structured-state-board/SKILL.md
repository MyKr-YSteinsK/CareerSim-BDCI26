---
name: structured-state-board
description: 在单局 CareerSim 中依据新鲜公开观察和已确认的动作回执维护 observed/inferred/unknown 工作状态，帮助同一个 Agent 恢复决策上下文；不得提交动作。
---

# Structured State Board｜结构化状态板

## 职责

为当前 CareerSim 单局维护一份精简工作状态，使同一个 Agent 能在长流程中恢复决策上下文。本 Skill 只整理 Agent 已有信息；它不是全局 Memory、跨局学习、Planner、风险策略、隐藏状态估计器或另一个动作提交者。

## 触发条件

在以下情况刷新状态板：

- `new_game` 成功且首次 `observe` 有效之后；
- 新鲜 `observe` 显示公开状态、事件、警告或合法选项发生重要变化时；
- 动作回执已确认后，并使用下一次新鲜 `observe` 更新当前状态；
- continuation/context loss 后；
- 状态板缺失、过期、含糊或属于其他游戏 session 时。

不要按每个 token 或日志行更新。只保留当前决策所需的状态和上下文，不积累无限历史。

## 输入

只使用正常 Agent 循环已取得的当前局公开信息：

- `new_game` 返回或由 `observe` 确认的 CareerSim 游戏 `session_id`；
- 最新 `observe` 的公开 `current_state`、当前事件/可见反馈与合法选项；
- 已确认的 `take_action` 回执；
- 仅在 context loss 后确有需要时，查看同一游戏 session 最近最多五条公开日志，以恢复最多两组相关的战略动作/效果。

JiuwenSwarm drive/conversation ID 不是游戏 session 标识。不得读取隐藏计数器、猜测阈值、秘密/局后字段、模拟器原始数据库、本机取证材料或其他游戏的状态板。预测或未确认的模型判断不能标为 observed。

## 状态板格式

在当前 drive conversation 中输出一份简短的完整替换状态板，只包含下一次决策相关字段：

```text
game_session_id: <已确认的 CareerSim 游戏 session ID>
game_time_or_phase: <公开观察值；否则 unknown>
observed:
  - <公开事实或已确认回执> [source: latest observe / action result; time: <可见游戏时间>]
inferred:
  - <有限推断> [based on: <observed 项>; confidence: <简短限定>]
unknown:
  - <当前公开证据无法确认且影响决策的事实>
recent_effects: # 本局最多两条；无记录时使用 []
  - action: <已确认的公开合法动作>
    target_or_relevant_field: <公开字段/目标>
    before_after: <已确认且可比较的变化，或 UNKNOWN>
    source: <已确认回执 / 紧邻的 fresh observe / 有界同局公开日志>
source_or_freshness: <最新权威 observe 与可见游戏时间；注明是否使用有界日志>
```

将 `observed`、`inferred`、`unknown` 分开。公开警告可记为 observed；其严重程度、原因、可能后果或建议应标为推断，或交由 `risk-review`。空项可省略或写 `none`，不得为填满格式而补造内容。

## 更新与 session 规则

- 新鲜、权威的 `observe` 优先于旧状态板。已确认回执只能记录它明确确认的事实；预测效果在观察前仍是 inferred 或 unknown。
- continuation/context loss 后，先确认 CareerSim `game_session_id` 并由正常 Agent 循环取得新鲜公开 `observe`。只有确有需要时，才检查同一 session 最近最多五条公开日志，且只为恢复最多两组近期战略动作/效果。只有公开证据直接确认动作及可比的前后值时才记录；否则写 `UNKNOWN` 或省略。不得回放更长历史或用日志查找事件答案。
- 本局 `recent_effects` 最多两条。只有动作已确认，且前后公开字段能用紧邻的 fresh `observe`、已确认回执或 context recovery 允许的同局日志直接比较时才记录效果。若有中间事件/动作或其他合理公开原因可能解释变化，写 `UNKNOWN` 或省略；不得仅凭先后顺序声称因果。
- `recent_effects` 只记录可观察事实，不作评价：不得标记好坏、推荐动作或拥有 `Primary Gap`。`rolling-planning` 可用可靠且可比的效果评估进展；过期或含糊的效果为 `UNKNOWN`。
- 推断不得覆盖或静默升级为 observed；必须保留推断依据。新证据不再支持时，删除或降级该推断。
- 复用状态板前先确认 `game_session_id`。session 不匹配时丢弃旧板，为当前已确认的游戏重建干净状态。
- 即使 JiuwenSwarm conversation 延续，新游戏 session 也必须从干净状态板开始。
- session ID 缺失、证据过期/含糊，或 context loss 后状态板缺失时，将无依据的细节标为 `unknown`。由同一个 Agent 在正常流程中取得新鲜 `observe` 并重建；之后才可进行有界恢复。不得猜 session ID 或沿用旧板。
- 状态板只保留当前游戏快照及本次决策确需的少量公开旧事实。不得变成连续 transcript 或无限历史。

## 正常流程与权限

本 Skill 只返回状态板；不调用 `new_game`、`observe`、`take_action`，也不推进月份/阶段。需要新鲜状态时，由同一个 Agent 按正常游戏循环获取。

```text
observe → structured-state-board 刷新 → 正常候选选择 → 触发时 risk-review
→ 同一个 Agent 最终决定 → take_action → 下一次 fresh observe → 刷新状态板
```

- **Can Submit Action: No（不得提交动作）。**
- 正常 Single Agent 仍是唯一 `take_action` 提交者，并决定最终合法动作。
- 不创建另一个 Agent、Team、Swarm、Planner 或动作提交者。
- `career-action-trace` 保持原有轨迹标记职责；本 Skill 不加动作标记，不改选项或 `notes`。

## 持久化边界

状态板只是在同一 JiuwenSwarm drive conversation 中使用的有界工作上下文，不是持久化存储。不得写入 `MEMORY.md`、`projects/<drive ID>`、Skill 文件、Runner 输出或模拟器数据库。不得假定 context compression 会保留状态板；context loss 后须用已确认 session ID 和新鲜公开 `observe` 重建。不得跨游戏 session 继承，也不得声称云端文件持久化。

## 兼容与回退

- 风险含义、严重程度和动作取舍仍由 `risk-review` 负责。状态板可把可见警告记为 observed，并将解释另列为 inferred。
- 证据不足以支持的项目应移入 `unknown` 或省略；游戏 session 未确认时不得复用旧板。
- 状态板缺失、过期、不匹配或含糊，不授权猜测动作。同一个 Agent 回到正常流程刷新公开状态并作决定。有界日志恢复只为找回 Planning 所需的近期效果事实，不负责判断进展或推荐动作；状态板自身不得阻断或提交动作。
