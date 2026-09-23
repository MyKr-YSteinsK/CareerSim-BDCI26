# S03-05｜最小 MCP 环境修复与服务级注册预检

## Status｜状态

- **Status:** `BLOCKED_TECHNICAL`
- **Recovery Decision:** `NOT_READY`
- **S03-06 Readiness:** `NOT_READY`
- **Branch:** `codex/s03-05-mcp-service-preflight`
- **Parent branch / SHA:** `codex/s03-04-mcp-registration-debug` / `510e9424b22484e2a1da4baccefcd4eaee5348ca`
- **Governance ancestor:** `69a394ee226da80282b06e1034b10b1bf70d5090`
- **Frozen Runner SHA:** `f61c738c72e51b77298cc1c14c7c6ebf4b6c527d`

S03-04 已由 Stage Review 接受。S03-05 在 instance config 的严格差异检查失败后按任务停止，恢复了原配置；没有启动服务，也没有验证真实 AgentServer 注册。本结果不宣布 S03 完成。

## FORENSIC_HOLD｜取证保全

- `FORENSIC_HOLD:S03-MCP-REGISTRATION = ACTIVE / UNCHANGED`。
- 在任何 shared runtime 修改前，将已登记的 5 份共享日志复制到 `D:\CS\CareerSim\.local\runtime\forensic-hold\S03-MCP-REGISTRATION\pre-s03-05\`，仅 copy、未 move。
- `runner.log`、`jiuwen.log`、`agent_server.log`、`full.log`、`server.log` 的 snapshot bytes/SHA256 全部与 S03-04 `debug_evidence.json` 登记值一致；恢复配置后，5 份 live source 仍与 snapshot 匹配。逐文件路径与哈希见 [preflight_evidence.json](preflight_evidence.json)。
- 此 snapshot 是后续 canonical hold source。S02 / S03-02 events 和 transcript 保持原路径；未复制、修改或提交。hold 由 S03 Stage 管理，只有 Main Hub / Stage Review 可解除。

## Pre-repair Config｜修复前配置

- Instance config：`C:\Users\Yukis\.jiuwenswarm-instances\career_emu\config\config.yaml`，50,088 bytes。
- Pre-repair snapshot：`D:\CS\CareerSim\.local\runtime\s03-05-mcp-service-preflight\config.pre-repair.yaml`。
- Snapshot / original SHA256：`34D2EED681D5C5DDB3919A805258B4F6A19A5C4F487FB2214B480BB1E899D66A`。
- MCP server：`career-emulator`，`transport=stdio`，原 command `career-emulator-mcp`；原 args `--update skip`，cwd `D:\CS\CareerSim\.venv\Scripts\`。
- 目标 command：`D:\CS\CareerSim\.venv\Scripts\career-emulator-mcp.exe`。这是 S03-04 已验证的 absolute launcher；按设计属于 `runtime-persistent but setup-overwritable repair`，因为 frozen `setup.py` 会重新写回 bare command。

## Exact Config Diff / Rollback｜精确差异与回滚

- 对现有 config 的 MCP command 行执行了一次定向补丁，预期只改变该字段。
- 补丁后对完整配置文本做严格比较：`actual_after` 不等于 `pre_snapshot` 中仅替换该 command 的预期文本。因此 **config diff scope = FAIL**。候选配置在回滚前未保存 SHA 或完整 diff；额外差异的具体字节类别不可确认，不将其猜测为仅换行符。
- 按任务要求立即停止并由 pre-repair snapshot 恢复。恢复后 config SHA256 与原始 snapshot 完全相同，command 回到 `career-emulator-mcp`。未修改 args、cwd、`CAREER_EMULATOR_*` env、provider/model、Skills 或 DB path 的最终状态。
- **Repair in effect:** `NO`。本次没有通过“only command field changed”门槛；不得启动 service 作为注册证据。

## Service Lifecycle｜服务生命周期

- Pre-state：`jiuwenswarm-start --status career_emu` 返回 stopped、无 PID；配置端口 `19092/20000/20001/6173` 无监听；进程清单未发现 CareerSim/Jiuwen 候选进程。未发现 active game/session 的进程或端口证据；未将持久 DB 中历史会话解释为 live session。
- Clean start count：`0`；stop count：`0`；restart retry：`0`。
- Final state：stopped、无 PID、配置端口无监听。没有 service-level runtime logs 的新注册时间窗。

## Provider / Prewarm｜模型使用

- Incidental provider call：`NO`（本任务未启动服务）。
- Model / completed usage / input、output、total、cache tokens / reported cost：`NOT_APPLICABLE`，未产生新请求，不把缺失 usage 记为 0。
- Agent chat：`0`；CareerSim tool invocation、`new_game`、`take_action`、gameplay：均为 `0`。

## MCP Registration｜MCP 注册

- Real AgentServer registration：`NOT_RUN`；新 `WinError 2`：`NO`（没有 startup）。
- 本任务暴露的 CareerSim tool set：`NOT_OBSERVED`；工具调用数：`0`。S03-04 的 direct Stdio 五工具 handshake 不能替代服务级验收。
- `PROJECT_PREFLIGHT_GUARD_NEEDED = YES_AS_PROCEDURE`：未来获授权的 Risk smoke 前，按最终 command / args / cwd / env 执行 direct Stdio initialize + list_tools 并检查五个必需工具；本任务未实现脚本或 helper Skill。

## S03-06 Readiness｜下一任务就绪度

`NOT_READY`。取证快照完整性通过，但 config 的仅 command 字段差异未通过，绝对路径修复未留在 instance，clean startup 与真实 AgentServer 注册均未执行。

## Helper / Strategy Boundary｜辅助能力与策略边界

- `framework-debugger = TRIGGERED / USED_AS_METHOD / NOT_CREATED_AS_COMPETITION_SKILL`
- `experiment-manager = NEAR_TRIGGER`；`Astra = ASTRA_NOT_NEEDED`
- Risk Hypothesis：`ACTIVE`；Risk effectiveness：`NOT_PROVEN`；controlled screening：`NOT_STARTED`。

## Verification｜验证

- Parent SHA 与 governance ancestry：PASS。
- 5/5 forensic snapshots 的 bytes/SHA256：PASS；5 份原共享日志恢复后仍匹配：PASS。
- Config backup hash：PASS；最终恢复原配置 hash：PASS；严格 command-only diff：**FAIL**。
- Frozen Runner、`uv.lock` 与两个 project Skills 相对 parent：unchanged；`uv lock --check --python D:\CS\CareerSim\.venv\Scripts\python.exe`：PASS；`git diff --check`：PASS。Branch delivery 见 TASK_RESULT。
- 没有安装/升级依赖、运行 gameplay、启动 service、调用 provider 或提交 raw logs、instance config、DB、凭据。

## Problems / Unknowns｜问题与未知

- 未保存补丁候选配置；无法对额外文本差异给出逐字节归因。恢复前的严格比较结果是本次停机依据。
- Service-level MCP registration、provider/prewarm usage 与真实五工具暴露均未验证。

## Next Recommended Action｜下一建议动作

只返回 `S03 Stage Review`：审阅 command-only diff 失败与已恢复配置，决定下一次授权的修复编辑方式和服务级预检边界；本任务不运行 Risk recovery smoke。
