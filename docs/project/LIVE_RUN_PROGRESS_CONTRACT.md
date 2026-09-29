# Live Run Progress Reporting Contract｜运行中进度汇报合同

## 目标

正式 CareerSim Run 期间，Codex 必须持续向用户报告已自然产生的进展，但不得为了汇报而新增游戏/Provider/MCP side effect。

核心原则：

`REPORT FROM EXISTING OUTPUT; NEVER QUERY FOR REPORTING`

## 必须汇报

1. P1 preflight 完成：Candidate、base、关键 gate 结果。
2. fresh game/session 建立后：报告 Run 已开始。
3. formal Review checkpoint：优先 M6 / M12 / M18 / M24 / M30 / M36 / M42 / M48。
4. promotion / no-promotion。
5. 明确 material warning、进入/退出 `MODE=S`、failure recovery 出现明显阶段变化。
6. provider / Runner / service / recovery technical anomaly。
7. natural / technical terminal。

如果长时间没有 checkpoint，Codex 可根据已有 stdout/log stream 给简短进度；不得启动额外 observe、MCP、DB、Provider probe 或其它查询。

## 汇报内容

每次 2–5 行，优先：

```text
<Run> progress | M=<month> L=<level>
Review/Promotion: <short>
Mode/Recovery: <short>
Key anomaly or progression: <short>
Run continues; no user action required.
```

不得泄露 hidden/private/internal fields。

## 执行方式

长 Run 应使用可持续读取已有 stdout/stderr 的 interactive process/session，使 Codex 能在不中断 Runner 的情况下输出更新。

进度汇报：

- 不暂停 Runner；
- 不等待用户确认；
- 不改变 action；
- 不消耗额外 game authorization；
- 不构成第二次 live operation。

## 与 no-intervention 的关系

“Runner active 时不得额外查询/干预”不等于“不得向用户报告”。

禁止的是额外 live query；允许且要求的是转述当前 Runner/已有日志已经自然产生的公开进展。
