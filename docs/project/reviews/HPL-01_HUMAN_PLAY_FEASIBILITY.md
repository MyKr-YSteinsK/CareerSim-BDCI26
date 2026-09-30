# HPL-01｜人工游玩可行性与隔离闭环

> Status: `PASS_ROUTE_A_OFFICIAL_CLI_WRAPPER`（静态可行性结论；不是 Human Run 授权）
> Plan/source review anchor: `451d91dbfc7d79b4e73fb6e99654cb2e01973e78`
> Delivery base after origin refresh: `d94b178e3e7867b80673c4dfecd2e70dd66272b5`
> Boundary: `NO GAME / NO PROVIDER / NO CANDIDATE CHANGE`

## Decision

在当前安装身份下，可以通过官方 `career-emulator` 本地 CLI 建设 Human-only loop。采用 **Route A — Official CLI Wrapper**：保留官方 CLI 的交互/显示路径，由外层 wrapper 在 emulator import 前配置独立 DB/log，并把 `GameEngine` 的数据目录显式指向已安装的 `career-emulator-bdci26==1.0.0` `dev/dataset`。wrapper 只从 CLI 输入/显示边界归档，再经 public allowlist 投影；不读 DB、session 对象、MCP payload 或模拟器内部状态。CLI 的 `logs` 命令会显示原始 status delta，因此 wrapper 必须阻止该命令进入策略证据。GitCode 分享回调也须在 HPL wrapper 中关闭。

这是可行路线，不是已交付的完整 Human launcher，也不证明终端捕获集成或任何实际对局。HPL Track 仍为 `ACTIVE_FEASIBILITY`；`HUMAN_PLAY_NEXT_GAME = NOT_AUTHORIZED`。下一步应返回 Main 请求 HPL-02；开始 Human Run 需要另外的 Main 授权。

## HPL_FEASIBILITY_EVIDENCE

| Area | Classification | Evidence and decision |
| --- | --- | --- |
| Package / environment identity | `CONFIRMED` | 当前 root `.venv` 的 Python 为 3.12.13 / Windows 11 x64；`career-emulator==1.0.1`、`career-emulator-bdci26==1.0.0`、`jiuwenswarm==0.2.4b3`、`fastmcp==2.14.7`。`career-emulator` console entry point 是 `career_emulator.cli:main`。仓库 lock 与 1.0.1 一致。 |
| CLI call path | `CONFIRMED` | `cli.main()` 将无参数或 `play` 分派至 `play()`；默认路径调用 `get_default_engine()`、`new_game()`、`observe()`、读取玩家输入，再调用 `take_action()`。`new_game()` 先加载数据，再经 `SessionStore.save_session()` 初始化并写入 DB/log。未传 session id 会创建 uuid4 session；`--session-id` 是恢复已有 session。Source: installed `career_emulator/cli.py`, `game.py`, `storage.py`。 |
| Zero Provider | `CONFIRMED`（静态 CLI 路径） | CLI 路径是本地 `GameEngine` + SQLite，不调用 `run_mcp`。安装包中 `career-emulator-mcp` 是独立的 `career_emulator.run_mcp:main` entry point；该路径才创建/运行 FastMCP server，默认还会先 `update_dataset`。已检查 CLI、engine、storage 源码及依赖调用名：未发现 `API_KEY`、`MODEL_NAME`、DeepSeek、JiuwenSwarm、AgentServer、prewarm 或 LLM Provider 调用。 |
| Optional external share | `NEEDS_LOCAL_VERIFICATION` | CLI 在结束时会进入 GitCode share 提示；若用户同意，它会读取 `GITCODE_ACCESS_TOKEN` 并上传日志。这不是 LLM Provider，但不是本地归档。HPL wrapper 必须把 `cli.offer_share` 置为 no-op，且不得要求/传递 GitCode token。HPL-01 未调用该分支。 |
| DB / logs | `CONFIRMED` | `CAREER_EMULATOR_DB` 与 `CAREER_EMULATOR_LOG_DIR` 在 `career_emulator.storage` import 时读取，默认都位于安装包 `career_emulator/data/` 下。`SessionStore.initialize()` 会创建目录、SQLite 表和文件 logger；首次 `new_game()` 的 `save_session()` 已触发初始化，因此必须在 import 前设置变量。新增离线测试在独立进程设置这两个变量，确认真实 1.0.1 storage resolver 使用 override，且没有创建 DB/log。 |
| Session identity | `CONFIRMED` | 新 session 由 uuid4 生成；没有独立 session namespace 环境变量。每次 HPL Run 使用唯一空 runtime root 与 fresh `play`，不可用未知历史 session。 |
| Dataset | `CONFIRMED` route mechanism; active default `UNKNOWN` | CLI 默认读安装包目录 `career_emulator/data/dataset`；`play` 本身不更新题库。`CAREER_EMULATOR_DATASET` 只影响 `update_dataset()` 选择哪个 split，不能重定向 loader root；`career-emulator update` / MCP `run_mcp` 可创建、替换或下载此目录，本任务没有执行。当前默认目录不是指向已安装 `career_emulator_bdci26/dev/dataset` 的同一路径，其实际来源未检查，故标为 `UNKNOWN`。已确认安装包 `career-emulator-bdci26==1.0.0` 的 `dev/dataset` 及 CLI 所需七个子目录存在。Wrapper 可将这些只读路径显式传给 `GameEngine`，绕开当前不明的默认目录；不需要 update/download。 |
| Isolation | `CONFIRMED`（按 wrapper 设计） | 唯一 `.local/runtime/hpl-<run-id>` 下的 DB 与 logs 通过 import 前环境变量独立；raw transcript 留在同一 run root；dataset 只读使用已安装 Dev distribution 路径。CLI 不启动 JiuwenSwarm、AgentServer 或 MCP service。`worktree isolation != runtime isolation`；未来 Human/Agent 运行仍须遵守 shared runtime 串行合同。 |
| Public render boundary | `CONFIRMED` with log restriction | CLI 显示 session、Month/Quarter/Year/Level、Health/Dignity/Skill/Network/Output/Wealth/Energy、event title/description、choices/action/energy cost、warning 和 Handbook。`DEBUG_MODE=False` 时不显示 `statistics`。可选 `logs` 命令会显示日志文件路径、动作与 `status_updates` 计算结果；wrapper 必须阻止 `logs` 输入，且不得把 raw log 字符串放入 canonical evidence。成功动作没有单独 receipt 文本，不能伪造；以之后的新 CLI observation 作为下一状态证据。 |
| Hidden-looking fields | `CONFIRMED` firewall required | CLI renderer 会显示 `event_id` / `node_id`；终局还显示 score `dimensions` 的 raw/normalized/weight/contribution。它们不得进入 canonical observed facts，记录路径并标记 `PUBLIC_STATUS_UNKNOWN`。Simulator model 的隐藏字段名也包括 `statistics`、active/completed nodes、event queue/counters、failure-rule remainder 等；Human evidence 不读取这些值，不用 event-id→answer mapping。 |
| Route A vs B | `CONFIRMED` — choose A | Route A 具备本地交互、DB/log override 与可由 CLI stdin/stdout 边界归档的路径；projection helper 只接收已提取的 CLI frame，不访问 private simulator internals。Route B 没有 Route A 的 material failure 证据，却引入 MCP service、更多内部字段和默认 dataset update 行为，不采用。 |

### Public evidence schema

Schema version: `hpl-public-evidence/v1`。每份真实 Run manifest 至少包含：

- `run_identity`: `run_id`、`session_id`、timestamps、git commit、launcher/schema version、emulator 与 dataset identity、experiment tag、provider status/evidence、isolation identity。
- `trajectory[]`: allowlisted fresh state、event title/description、legal choices、human selection、CLI 明确显示的 action receipt、next fresh state、review/promotion/warning、可核验的 public result/log。
- `human_interpretation`: 独立于 `observed_fact` 的人类解释；禁止把解释回写为 simulator fact。
- `integrity`: artifact hash、manifest/schema version、session consistency、public-only validation、secret-scan status。

`provider_used=false` 不由默认值或本 Plan 宣称；真实 Run 必须附可验证 preflight/run evidence。成功动作 receipt 在 CLI 未显示时记为 `NOT_EXPLICITLY_RENDERED`。`public_log` 仅允许结构化的 `month/event_title/choice/action`，原始 `logs_text` 与 status delta 一律剔除。当前 `scripts/hpl_public_evidence.py` 只投影白名单标量；未知字段仅记路径、不保存值，并将状态标为 `PUBLIC_STATUS_UNKNOWN`。原始 terminal capture 不进 repository。

## Minimal artifacts and verification

- `scripts/hpl_preflight.py` 只解析安装身份、Dev dataset 目录与新 runtime DB/log 目标，打印 dry-run JSON；不建目录、不导入 emulator、不启动 CLI。
- `scripts/hpl_public_evidence.py` 提供 fixture 可验证的 allowlist projector。
- `tests/test_hpl_01_offline.py` 覆盖 path isolation/no-write、真实安装包 env override、hidden-looking field dropping 与 interpretation 分离。
- 实际执行过官方 `career-emulator --help` 和 `career-emulator play --help`；两者只显示参数并退出 0。输出有 Authlib deprecation warning，不影响 help 结果。
- 绝未运行 `play`、`update`、MCP、service、dataset download、Provider 或 Candidate install/reload。

## Remaining limits / next boundary

- 当前安装包默认 `career_emulator/data/dataset` 来源未知；后续 wrapper 必须显式固定到 `career-emulator-bdci26==1.0.0/dev/dataset`，并在任何 Human Run 前复查 package identity 与目录身份。
- CLI transcript/stdin capture、阻止 `logs` 输入与 `offer_share` no-op wrapper 尚未实现或进行 live-path 验证；这需要 HPL-02 做 no-game offline wiring check。
- 本结论仅证明一条安全 Human-only 路线可构建；不证明 loop 已完成、provider 实际成本、Human strategy 效果、Agent 并行安全或 HPL Track 完成。
- Recommendation: 返回 Main 请求 HPL-02；`HUMAN_PLAY_NEXT_GAME = NOT_AUTHORIZED`。
