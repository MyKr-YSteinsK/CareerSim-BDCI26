# S07-04｜最小 Public Probe Live Confirmation

## Identity

- Task: S07-04
- Base / actual `origin/main`: `aebd599289d15ee671ba41956c28b3b0f1ef9b3e`
- Branch: `main`
- Current Candidate: `candidate-v6c-compliance-cleanup`（本任务未修改）
- Live boundary: direct MCP only; no JiuwenSwarm AgentServer/provider/gameplay run
- Final verdict: `DIRECT_PUBLIC_MCP_PATH_CONFIRMED`
- Probe verdict: `MINIMAL_MECHANICAL_PROBE_ENGINEERING_FEASIBLE`

## Static Preflight

- Executable: `D:\CS\CareerSim\.venv\Scripts\career-emulator-mcp.exe`
- Arguments: `--update skip`
- Child working directory: `D:\CS\CareerSim\.venv\Scripts`
- `career-emulator`: `1.0.1`
- `jiuwenswarm`: `0.2.4b3` installed but not started
- MCP client: installed `mcp 1.27.2`, `mcp.client.stdio.stdio_client`
- Client lifecycle was statically confirmed as one stdio child process, one explicit `initialize`, one `list_tools`, and context-managed shutdown.
- Pre-live matching process count: `0`
- Static client script compile: PASS

## Live Accounting

| Operation | Count | Result |
|---|---:|---|
| Direct `career-emulator-mcp` start | 1 | one clean start |
| JiuwenSwarm AgentServer start | 0 | not started |
| Provider / DeepSeek call | 0 | none observed |
| MCP initialize | 1 | PASS |
| MCP list_tools | 1 | PASS |
| `new_game` | 1 | PASS |
| `observe` | 2 | first + fresh post-action observe |
| Successful `take_action` | 1 | PASS |
| Runner play / full game | 0 | not run |
| Skill install/reload | 0 | none |
| Shutdown | 1 | stdio context exited; no matching process remained |

The direct child emitted only FastMCP startup/deprecation/update notices in stderr; no AgentServer, DeepSeek, provider, or prewarm activity was observed.

## Public Interface

The single `list_tools` response exposed:

- `new_game`
- `observe`
- `take_action`
- `check_latest_logs`
- `show_employee_handbook`

The required public tools were present. No suspicious `private`, `hidden`, `internal`, `debug`, or `admin` tool name was exposed.

Relevant public schemas:

- `new_game`: no required arguments;
- `observe`: required `session_id`;
- `take_action`: required `session_id`, integer `choice`, and `notes`.

No public seed/replay control was present in the inspected `new_game` schema:

`NO_PUBLIC_SEED_CONTROL_FOUND`

## Probe Loop

- Session: `d1372b71e1e94bf0aa14733d4419dc32`
- `new_game`: returned a session identity successfully.
- First `observe`: public time `month=1`, `quarter=1`, `year=1`; one legal public choice, ID `1`.
- Deterministic selection rule: `min(public_legal_integer_choice_ids)` → `choice=1`.
- `take_action`: success; sent only the public `session_id`, integer `choice=1`, and minimal note `S07 public-interface probe`.
- Fresh `observe`: returned public state for the same session; public time remained `month=1`, `quarter=1`, `year=1`, and three legal choices were exposed.
- Same-session confirmation: PASS.

Therefore the bounded public loop succeeded:

`new_game → observe → one legal take_action → fresh observe`

## Evidence

Local ignored evidence was retained at:

- `D:\CS\CareerSim\.local\runtime\s07-04-public-probe\public_trace.json`
  - bytes: `3759`
  - SHA-256: `A29005280F36C714C0F3132E2461BCDF932F0CE3BDA6AA545B08BA2E78F8CEFA`
- `D:\CS\CareerSim\.local\runtime\s07-04-public-probe\server-stderr.log`
  - bytes: `2441`
  - SHA-256: `68E963DBC9584B5D5FF7A9543156AC0800366227A3A725A8D0761DE0BD2AEEEE`
- Probe DB: `D:\CS\CareerSim\.local\runtime\s07-04-public-probe\probe.sqlite3`; not tracked.

The durable artifact contains only bounded public-interface evidence. No raw runtime file, database, credential, `.env`, or one-off client script is committed.

## Interpretation Boundary

This confirms only that:

- the direct participant-facing MCP stdio path is independently callable;
- a scripted controller can consume public choices and perform one legal integer action;
- a fresh public observe can close the same-session loop without JiuwenSwarm or a provider.

It does not establish:

- deterministic replay or public seed control;
- score predictive power or policy benefit;
- v6c runtime correctness;
- stable 80+ performance;
- any replacement for real DeepSeek Agent reasoning on ordinary story semantics, Skill adherence, compression recovery, or reasoning drift.

## Repository Scope

Only this review artifact is tracked. Candidate, Skills, runtime manifest, Runner, dependencies, JiuwenSwarm configuration, and project state files were not modified.
