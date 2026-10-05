# FZU-Loss快点降｜CareerSim 提交方案

本包提交 `candidate-v6-auditable-control-loop`，采用 Single Agent 和三个 Skill。主 Agent 负责调用游戏工具，Skill 分别整理事实、维护长程目标、审核当前候选的风险。所有判断只使用本局公开观察、合法菜单与公开手册，覆盖 48 个月中的剧情、季度资源分配和半年 Review。提交保持 v6 的原始运行指令与 Skill 内容，设计及取舍说明另见下方文档。

## 文件结构

```text
solution/
  manifest.json
  README.md
  design/
    skills_design.md
    decision_report.md
  skills/
    structured-state-board/SKILL.md
    rolling-planning/SKILL.md
    risk-review/SKILL.md
```

manifest 的团队名为 `FZU-Loss快点降`，提交名称为 `FZU-Loss-final-v6`，运行模式为 `agent`。

## 决策闭环

```text
observe → Board → Planning → candidate action → Risk
        → 主 Agent take_action → fresh observe
```

Board 提供当前事实；Planning 用 Primary Gap 连接当前动作和下一个 Review；Risk 只检查已经选出的候选。状态改变后重新观察，再决定下一项，三个 Skill 都没有动作提交权。

## 离线材料校验

在官方 CareerSim 仓库的已安装 Python 环境中，对解压后的目录执行：

```shell
python -c "from pathlib import Path; from career_sim_runner.validate import validate_submission; r=validate_submission(Path('solution')); print(r.to_dict()); raise SystemExit(0 if r.ok else 1)"
```

此命令调用官方材料校验函数，检查目录、manifest 与 Skill frontmatter；不启动服务或对局。材料校验通过不代表云端评测已经完成。

## 设计文档

- [Skill 设计](design/skills_design.md)：三个职责如何协作，如何处理长程目标、风险约束和上下文恢复。
- [最终决策](design/decision_report.md)：选择 v6 的实验依据、未采用的复杂路线及这次提交承担的不确定性。
