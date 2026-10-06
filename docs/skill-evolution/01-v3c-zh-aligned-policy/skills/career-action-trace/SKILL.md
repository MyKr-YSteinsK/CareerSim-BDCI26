---
name: career-action-trace
description: 每次即将提交 CareerSim `take_action` 时使用；保持常规决策已选选项不变，并在原有简短决策记录末尾追加 S02 标记。
---

# Career Action Trace｜职业行动轨迹

## 何时使用

每次 Career Emulator `take_action` 前立即使用。

## 必须执行

- 保持常规 CareerSim 决策流程已经选定的选项，不得改选。
- 保留 `notes` 中已有的简短理由，不得删掉或改写。
- 在 `notes` 末尾精确追加 ` [S02_SKILL_USED]`。若 `notes` 为空，则只写 `[S02_SKILL_USED]`，前面不加空格。
- 只通过现有 `take_action` 工具提交一次。

## 边界

- 本 Skill 只添加轨迹标记，不选择或排序选项、不改变策略或游戏状态。
- `new_game`、`observe` 与终止处理仍由正常游戏循环负责；本 Skill 不调用它们。
- 不创建另一个 Agent、动作提交者、Memory、Planning 或 Risk-Control 状态。
