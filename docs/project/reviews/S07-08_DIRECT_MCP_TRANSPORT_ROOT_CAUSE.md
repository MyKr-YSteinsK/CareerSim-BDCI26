# S07-08｜Direct MCP transport 启动边界复核

## 结论与证据边界

- Base：`main@43c087f6233e6c0b61ae990183262864bb469b11`；当前 Candidate 仍为 `candidate-v6c-compliance-cleanup`。
- S07-07 Gate A 的已登记现象：启动**尝试** 1，initialize/list_tools/new_game/observe/take_action 均 0；stderr 0 bytes；任务 DB 未生成；事后匹配进程 0。历史 compact evidence：`docs/project/runs/s07-07-mechanical-probe-batch.json`；本地原件仍在 `.local/runtime/s07-07-mechanical-batch/01-p0/`。
- `H_STDERR_STRINGIO_PRESPAWN_FAILURE`：**机制已由安装源码和相同 SDK 路径的无害子进程复现确认**。S07-07 当时未保存异常类型/栈，因此“历史那一次必然就是此异常”是高置信归因，而非直接记录的异常事实；不得把后验复现冒充原始日志。
- 决策：`DIRECT_MCP_HARNESS_RETRY_READY`，仅指启动边界修复具备申请下一次 Gate A 的工程依据；并非 CareerSim live 验证或 policy PASS。

## 异常链与 spawn 判断

安装环境为 `mcp==1.27.2`。`mcp/client/stdio/__init__.py:106,124-131,235` 将 `errlog` 传入平台进程创建，并把 `server.env` 与安全默认环境合并；`mcp/os/win32/utilities.py:136,176-187,195-225` 将同一 `errlog` 交给 AnyIO/Popen 的子进程 stderr。旧 harness 在 `scripts/run_public_mechanical_batch.py` 中使用 `io.StringIO()`，并在进入 `stdio_client` **之前**预置 `direct_server_starts=1`。`StringIO.fileno()` 抛 `io.UnsupportedOperation('fileno')`；该异常继承 `OSError`，故被旧 broad `except OSError` 记为 `UNKNOWN_SIDE_EFFECT / SERVER_START_OR_TRANSPORT`，未留下具体异常。

本机用 `sys.executable -c` 作为**非 CareerSim**无害 child，沿 `stdio_client` 原路径测试：`StringIO` → `UnsupportedOperation('fileno')` 且 child 标记文件不存在；真实 UTF-8 文件句柄 → child 标记文件存在。由此确认该错误在 child spawn 之前发生。S07-07 的零 stderr、零 DB、零 initialize、事后零进程与该机制一致，但单凭原始 compact evidence 不能独立排除另一种 pre-initialize 异常。原报告的 `direct_server_starts=1` 应解释为 **attempt**，不能作为已 spawn 的证据；历史文件保持不改。

环境不是已发现的促成因素：安装版 `get_default_environment()` 只继承固定安全变量（含 PATH/SystemRoot/TEMP），再合并任务提供的 `CAREER_EMULATOR_*`；不自动继承 provider key。当前参数沿用原有 `--update skip` 与 task-local DB/log；未发现 env replace 或缺失必要变量导致此处 pre-spawn 异常。

## 最小修复

- 每个 session 使用本地 `server-stderr.log` 的真实、context-managed UTF-8 文件句柄；在进入 SDK 前验证 `fileno()`。退出后读取 stderr 用于既有意外 Agent/provider 文本检查；raw stderr 只留 `.local/runtime/`，不提交。
- Compact lifecycle 新增 `server_start_attempted`、`transport_entered`、`child_spawn_confirmed`；旧 `direct_server_starts` 改为仅在 SDK context 成功进入后记 1。`initialize_count` 从同一个 `SessionResult` 保留，不再因内部重建结果而丢失；`shutdown_count` 仅在 transport context 正常退出后记 1。
- 本地 sink/参数准备失败且尚未进入 SDK → `TOOLING_OR_PRESPAWN_ERROR / PRESPAWN_LOCAL_FAILURE`，child 明确未 spawn。调用 SDK 后、context 尚未 yield 的失败 → `UNKNOWN_SIDE_EFFECT / LIVE_SERVER_START_OR_TRANSPORT_UNKNOWN`，child 状态为 `UNKNOWN`，不得凭零 confirmed starts 重试。context 已进入但初始化失败，同样保留真实调用计数和 stop 边界。
- 未修改 P0/P1/P2、public projection、Candidate、Skill、Runner、依赖或 runtime config。

## 离线验证与剩余未知

- 当前 SDK 精确路径：StringIO pre-spawn / 真实文件成功启动**无害 child**，PASS；没有启动 `career-emulator-mcp`。
- 假 transport：pre-spawn 本地 sink 失败、context 前未知、context 后 initialize 失败、initialize 成功后 public protocol 失败、clean completion，计数及分类 PASS。
- `tests/test_run_public_mechanical_batch.py` + `tests/test_public_mechanical_probe.py`：31/31 PASS；compile 与 `git diff --check` PASS。测试仅使用 fake client、临时目录和无害 Python child。
- CareerSim MCP starts/calls、AgentServer、provider、new_game、observe、take_action、Runner play、Skill install/reload：全部 **0**。
- 未知：修复后的真实 CareerSim Gate A 是否成功、SDK 在真实进程启动后是否遇到另一个独立问题、后续 policy 是否可完成长 session。不能以此离线测试声称已通过 live Gate A。

下一步仅返回 S07 申请新的 `GATE_A_P0_SINGLE_RETRY` 授权；S07-07 已消费的 live budget 不可复用，不自动恢复 9-session batch。
