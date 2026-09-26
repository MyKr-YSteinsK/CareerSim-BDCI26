# S07-09｜P0 Gate A 单局 live retry

## 身份、授权与预检

- Base / branch：`main@f425b0a7a3361c889d324101a012610af4d59f74`；Candidate `candidate-v6c-compliance-cleanup`，未参与 P0 policy。
- 用户在本 Task 明确回复：`AUTHORIZE_S07_09_GATE_A_P0_SINGLE_RETRY`。S07-07 旧预算未复用；仅一次新任务授权。
- S07-08 real-file stderr、lifecycle accounting 与 pre-spawn/unknown 分类仍在；P0 仍为最小公开合法整数 choice ID。预检：30 targeted tests PASS，1 个 S07-08 无害子进程复现测试按计划复用既有证据而不重跑；compile/import PASS；`mcp 1.27.2`、`career-emulator 1.0.1`、`career-emulator-bdci26 1.0.0`，绝对 MCP executable 存在；文件句柄可写且有 `fileno()`；新 runtime root 原先不存在；匹配 MCP/AgentServer 进程 0。
- 使用 `D:\CS\CareerSim\.venv\Scripts\career-emulator-mcp.exe --update skip`。入口仅在内存中将 batch slots 限为 `['P0']`；无 P0 语义改动，无默认 9-session batch。新本地路径：`D:\CS\CareerSim\.local\runtime\s07-09-gate-a-p0-retry\`，独立 DB/log，未修改 JiuwenSwarm config。

## 唯一 live session

| 项目 | 实际 |
| --- | --- |
| direct MCP start attempt / transport entered / child confirmed | 1 / 1 / YES |
| initialize / list_tools / new_game | 1 / 1 / 1 |
| public tools | `new_game`, `observe`, `take_action` 均存在；另有 `check_latest_logs`, `show_employee_handbook`，未调用 |
| public seed control | `NO_PUBLIC_SEED_CONTROL_FOUND` |
| game session | `5888da780669417daf8c74124edcaf6e` |
| successful take_action / observe | 4 / 5（首次 + 每次成功动作后 fresh observe） |
| invalid / unsupported / unknown outcome | 0 / 0 / 0 |
| natural terminal / month / final Level | YES / M2 / L1 |
| final public Health / Output | 0 / -1 |
| secondary public ending score | quantitative `19.95`；competition partial `13.96`；grade `E`；eliminated |
| clean stdio shutdown / residual matching processes | 1 / 0 |
| AgentServer / provider / Runner play / Skill install | 0 / 0 / 0 / 0 |

公开投影和同一 session ID 校验贯穿观察循环；每次提交前均检查当前 choice ID 合法且为最小整数。M2 因公开 Health=0 提前终止，属于自然游戏终局而非 protocol failure；P0 是任意机械控制，低分与早退不代表 v6c 行为，也不证明策略优劣。48 个月长链稳定性仍未检验。

## 事后报告误报修正

原 harness 在**游戏已自然终止、transport 已正常关闭之后**，扫描 stderr 中的子串 `provider`，把 FastMCP 的 `fastmcp/server/auth/providers/jwt.py:10: AuthlibDeprecationWarning` 导入警告误分类为 `UNEXPECTED_AGENT_OR_PROVIDER_DEPENDENCY`。stderr 只有这一行命中 provider/AgentServer/DeepSeek/prewarm 关键词；它不是模型调用证据。任务本地 `session_summary.json` 与 `server-stderr.log` 保持原样，不改写历史原件。提交的 compact evidence 明示 `original_harness_status` 与 correction，并将结论校正为 `GATE_A_P0_RETRY_PASS`。

仅做纯 reporting fix：对这一条特定 FastMCP Authlib 弃用警告排除假阳性，保留其它 provider/AgentServer 线索的停止行为；新增正反例测试。P0/P1/P2、Candidate、Skills、Runner、依赖和 runtime config 未改；没有第二次 live run。

## 证据与决策

- Compact：`docs/project/runs/s07-09-gate-a-p0-retry.json`，只记录公开、必要字段；无 raw transcript/DB 提交。
- 本地 raw（均在上述 ignored runtime root 的 `01-p0/`）：`server-stderr.log` 2441 bytes / SHA-256 `ed34056f24edca7c458065d5ac1c14bc190f16d5d6dbe00359f186c3f82e0086`；`session_summary.json` 2741 bytes / `224a562f3a2f2c887d60900135483a17b5ac310f0ed3b0e7f966ebb96cc09c34`；`probe.sqlite3` 20480 bytes / `2bd0c008b4fca59dccd9f6e2ce3f782dce7813cb6b0e45d73992adcc00ee09c7`；session log 3116 bytes / `5a3c964e586cc8bbd18968942987742c258034d358902b6d1f71c063b1bbdd0a`。未读取 DB 内部内容作策略分析。
- Post-run 31 targeted tests PASS，1 个 S07-08 已验证的无害 SDK 复现测试未重跑；compile、compact JSON/本地 hash、`git diff --check` PASS。
- Verdict：`GATE_A_P0_RETRY_PASS`，仅证明修复后的 direct public MCP harness 能在无 LLM 情况下完成**一局直到自然终局**。不证明 48m 稳定性、P0 policy benefit、v6c runtime correctness 或 stable 80+。

返回 S07 决定是否/如何授权剩余 mechanical batch；本 Task 不进入 Gate B、不运行第二局。
