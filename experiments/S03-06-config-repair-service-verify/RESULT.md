# S03-06｜配置单字段修复与服务级 MCP 注册验证

## Identity / Decision｜身份与结论

- **Status:** `COMPLETE`
- **S03-07 Readiness:** `READY_FOR_ONE_RISK_RECOVERY_SMOKE`，仅供 S03 Stage Review 决定；本任务没有运行 smoke。
- **Branch:** `codex/s03-06-config-repair-service-verify`
- **S03 parent:** `debbbc65c6912050565b2eff208c119c14c4988c`
- **Plan Contract main ancestor:** `9052d68e2a6fa0af60faaad66014a1ba6cf455a1`
- **Governance merge:** `5c0b3b6a8ee0d1f4a041fea6ad19da65e6ad87b3`
- **Frozen Runner SHA:** `f61c738c72e51b77298cc1c14c7c6ebf4b6c527d`

## FORENSIC_HOLD｜取证保全

`FORENSIC_HOLD:S03-MCP-REGISTRATION = ACTIVE`。启动共享服务前复核 `.local/runtime/forensic-hold/S03-MCP-REGISTRATION/pre-s03-05/` 的 5 份 canonical snapshot：文件均存在，bytes 与 SHA256 全部匹配 S03-05 manifest。未删除、覆盖或移动；本次服务新增日志仅保存在本机忽略目录，未提交。

## Config Investigation / Repair｜配置调查与修复

- Instance config：`C:\Users\Yukis\.jiuwenswarm-instances\career_emu\config\config.yaml`；修复前 50,088 bytes，SHA256 `34D2EED681D5C5DDB3919A805258B4F6A19A5C4F487FB2214B480BB1E899D66A`。
- 先复制 pre-edit snapshot，再对副本执行第 1 种定点补丁方法，保留 candidate、完整 parsed semantic before/after、text diff、byte diff 与哈希。candidate 通过后对 live config 使用相同补丁；live 与 candidate 哈希一致。修复方法尝试 `1/2`，无回滚。
- 唯一 YAML 语义差异：`/mcp/servers/0/command`，`career-emulator-mcp` → `D:\CS\CareerSim\.venv\Scripts\career-emulator-mcp.exe`；`mcp.servers` 中目标名称唯一。args、cwd、`CAREER_EMULATOR_*`、provider/model、ports、DB path、Skills 等其他解析值完全相同。
- 修复后 50,121 bytes，candidate / live / 停服后的 config SHA256 均为 `05928EFAED4508D2C1A70C6B32B704CADB3B1CD40026A5CDA0D91EDD4878DEFE`。文本比较只有第 1075 行变化；该行 CRLF → LF，其他 1265 行仍为 CRLF。除目标 scalar 外，字节差异属于该行的换行格式，YAML 语义没有额外变化。
- 本次已复现“定点补丁引入额外文本差异”的机制。S03-05 未保存当时 candidate，故将其同因归因列为 **中等置信推断**，不是对旧候选的直接证明。
- 选择该方法是因为语义差异可独立证明、文件其余部分不被 serializer 重写，且有原始快照可逆。修复分类：`runtime-persistent but setup-overwritable`；frozen Runner `setup.py` 仍会写回裸命令，不将本次修复称为永久 Runner fix。
- 私有取证目录：`D:\CS\CareerSim\.local\runtime\s03-06-config-repair-service-verify\`；包含 `config.pre-edit.yaml`、`candidate-method1.yaml`、`config.after-edit.yaml`、`parsed-semantic-*.json`、`text-diff.patch`、`candidate-summary.json`。均不提交。

## Direct MCP Preflight｜无模型直连预检

修复后、服务启动前使用实际 command / args / cwd / MCP env 完成一次 Stdio `initialize` 与 `list_tools`：均 `PASS`，暴露 `new_game`、`observe`、`take_action`、`check_latest_logs`、`show_employee_handbook`。CareerSim tool call 为 `0`；没有 Agent chat、游戏或 provider 测试。`PROJECT_PREFLIGHT_GUARD_NEEDED = YES_AS_PROCEDURE`，下次获授权 smoke 前可重复 fail-closed 直连预检；本任务未开发新框架或 Skill。

## Service Lifecycle / Registration｜服务生命周期与注册

- Pre-state：`career_emu` stopped、无 PID；端口 `19092/20000/20001/6173` 无监听，未发现候选 Jiuwen/CareerSim 活跃进程。未将历史 DB 状态误认作 live session。
- 依据本机已安装 `jiuwenswarm.start_services`，使用现有 `jiuwenswarm-start.exe app --name career_emu` 启动一次；该模式只启动 app 侧，不启动 web/frontend。启动计数 `1`，restart retry `0`。实例报告开始于 `2026-09-23T15:56:17.526691+08:00`，PID `9236`。
- 新增真实 `runner.log` 中，`career-emulator` 的 `add_resource_server` 于 `15:57:14.299189` 与 `15:58:07.753941 +08:00` 均为 `success` / `add mcp server succeed`，两次都报告上述完整五工具集合。新增 runner/jiuwen/llm/server 日志及启动 stdout/stderr 均无 `WinError 2`。两条注册事件发生于一次服务启动内，不是两次启动。
- 本次没有发送 Agent chat、调用 CareerSim tool、`new_game`、`take_action` 或运行 gameplay。新增 runner event types 仅有 `add_resource`、`remove_resource`、`add_resource_server`；无 tool invocation event。stdout 中的工具名出现在资源标签/注册行。
- 注册证据保存在本机 `service-final-*.log`、`window-*.log`、`service-window-analysis.json`，仓库仅提交精简 [verification_evidence.json](verification_evidence.json)。
- 取证后执行一次 `jiuwenswarm-start.exe --stop career_emu`，于 `15:59:33.863 +08:00` 报告 stopped。最终 status stopped、无 PID、目标端口无监听且相关进程已退出。stop count `1`。

## Provider / Prewarm｜启动期模型使用

无 Agent chat 的 service startup 自动产生 **1 条已完成的 incidental provider response**：`2026-09-23T15:57:14.014780+08:00`，`deepseek-flash`，input `200`、output `1`、total `201` tokens；`cached_tokens=0`、`prompt_cache_hit_tokens=0`、`prompt_cache_miss_tokens=200`。`llm.log` 中多条 start/end 是这一请求的内部阶段日志，不计为多次完成请求。Runner/provider 未报告费用，`reported cost = unavailable`，不填零。本任务未主动发起模型调用。

## Strategy Boundary / Verification｜策略边界与验证

- Risk Hypothesis = `ACTIVE`；Risk effectiveness = `NOT_PROVEN`；controlled screening = `NOT_STARTED`。
- `framework-debugger = TRIGGERED / USED_AS_METHOD / NOT_CREATED_AS_COMPETITION_SKILL`；`experiment-manager = NEAR_TRIGGER`；`Astra = ASTRA_NOT_NEEDED`。
- S03 parent 与 Plan Contract main ancestry：PASS；5/5 hold snapshot integrity：PASS；parsed semantic command-only diff：PASS；direct MCP preflight：PASS；真实 AgentServer 注册与五工具暴露：PASS；最终服务生命周期：KNOWN/STOPPED。
- Frozen Runner、`uv.lock`、两个 project Skills、provider/model config 未改；`uv lock --check`、Git/scope/secret/diff 检查见交付验证。无 dependency install、gameplay、Risk smoke、实验重跑。

## Problems / Unknowns｜问题与未知

- S03-05 旧候选未保留，旧额外文本差异不能直接溯源；本次相同补丁方式复现了目标行 CRLF → LF。
- CLI 重定向 stderr 中有 Windows GBK 对日志符号的 `UnicodeEncodeError`，属日志输出问题；服务继续运行、完成 MCP 注册并成功停止。本任务不扩大到 framework 日志修复。
- Provider 报告中无 cost；底层 serving version 映射仍按项目原状态保留 `PARTIALLY_VERIFIED`。

## Next Recommended Action｜下一建议动作

仅返回 `S03 Stage Review`；不自行运行 Risk recovery smoke。
