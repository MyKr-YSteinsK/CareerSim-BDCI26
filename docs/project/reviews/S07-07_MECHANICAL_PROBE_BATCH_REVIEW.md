# S07-07｜首轮 Public Mechanical Probe Live Batch Review

## Identity and authorization

- Task: `S07-07`
- Plan base: `0a61130736408f56a98e4f3af71dd32c4e1cba80`
- Pre-live harness commit: `58c1dd4f3e79297694311eca09bce598f6cfa7a2`
- Branch: `main`
- Candidate: `candidate-v6c-compliance-cleanup`
- Architecture: Single Agent + Three Skills; unchanged
- User authorization: `MINIMAL_MECHANICAL_PROBE_BATCH`, task-scoped direct public MCP only
- Final status: `MECHANICAL_PROBE_BATCH_STOPPED_ON_RUNTIME_BOUNDARY`

This is a bounded runtime stop, not a gameplay result and not a Candidate
validation. The task consumed one direct-server start attempt and did not
continue after the Gate A unknown outcome.

## Pre-live gates

Static identity was unchanged: `career-emulator 1.0.1`, MCP `1.27.2`, and the
absolute executable `D:\CS\CareerSim\.venv\Scripts\career-emulator-mcp.exe`.
The W0 harness used `--update skip`, a fresh task-local DB/log directory per
session, and no JiuwenSwarm configuration. The offline suite passed `25/25`;
compile, explicit `--live` CLI gating, and `git diff --check` passed.

The narrow structural target table was:

| Public action label | Tracked public target | Result |
| --- | --- | --- |
| `人脉维护` | `network` | mapped |
| `健康恢复` | `health` | mapped |
| `心理修复` | `dignity` | mapped |
| `准备汇报材料` | `output` | mapped |

Multi-target/hidden-risk labels such as `申请关键项目`, `高强度工作`,
`处理历史埋雷`, and `低调避险` were not hard-bound to a target. P2 was
therefore statically live-evaluable, but the mapping was never exercised by a
successful live session. No public material-risk annotation source was
available; `material_risk` remained `UNKNOWN`, so
`PUBLIC_RISK_OVERRIDE_NOT_EXERCISED`.

S07-04's already accepted `NO_PUBLIC_SEED_CONTROL_FOUND` evidence was reused;
no extra smoke call was made for seed discovery.

## Gate A result

Gate A policy was `P0 / MIN_ID_CONTROL`. The direct stdio start was attempted
once. The process lifecycle did not reach a certifiable MCP session:

- initialize: `0`
- list_tools: `0`
- new_game: `0`
- observe: `0`
- take_action: `0`
- successful actions: `0`
- session identity: unavailable
- stderr: `0` bytes
- post-check matching MCP/AgentServer processes: `0`
- task-local DB: not created

The harness recorded `UNKNOWN_SIDE_EFFECT` at the server-start/transport
boundary. Because no response established whether the child start had fully
completed, the task did not retry, restart, call initialize again, or send any
game operation. Gate B was not started; total sessions executed: `1` of the
planned `9`.

## Live accounting

| Operation | Count |
| --- | ---: |
| direct MCP server start attempts | 1 |
| MCP initialize | 0 |
| MCP list_tools | 0 |
| new_game | 0 |
| observe | 0 |
| successful take_action | 0 |
| AgentServer starts | 0 |
| provider / DeepSeek calls | 0 |
| Runner play | 0 |
| Skill install/reload | 0 |
| server restart | 0 |
| continuation / second new_game | 0 |

The task-local compact evidence is tracked at
`docs/project/runs/s07-07-mechanical-probe-batch.json`. Local ignored evidence:

- `D:\CS\CareerSim\.local\runtime\s07-07-mechanical-batch\01-p0\session_summary.json`
  - 1107 bytes, SHA-256 `c5517afe6550fc108c6dde56216807b93e3d9fbab1e6e3eb3b3fada419165d22`
- `D:\CS\CareerSim\.local\runtime\s07-07-mechanical-batch\01-p0\server-stderr.log`
  - 0 bytes, SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`

No raw gameplay trace, DB, credential, or provider output was committed.

## Policy findings

No P0/P1/P2 mechanical viability, progression, repetition, stall, survival,
or score finding is available. In particular:

- P0 did not reach the public protocol;
- P1 was not run;
- P2 was not run and did not exercise its stall mapping;
- no risk override was exercised;
- no policy comparison or variance conclusion is valid.

The only valid conclusion is:

`MECHANICAL_PROBE_BATCH_STOPPED_ON_RUNTIME_BOUNDARY`

This run does not support `POLICY_HYPOTHESIS_READY_FOR_MAIN_REVIEW`, a causal
score claim, a stable-80 claim, or a real-Agent ablation claim.

## Problems and compliance notes

1. A pre-live direct script invocation initially failed at import-path setup;
   it was corrected and verified offline before the one authorized server
   start. It consumed no live budget.
2. The one live start attempt produced no protocol response and no stderr. The
   resulting state was treated as unknown, not as a successful or ordinary
   protocol failure. No blind retry was made.
3. An earlier broad repository search incidentally matched lines from the
   quarantined forensic history file. Those lines were not used as policy,
   mapping, or runtime evidence; subsequent decisions used the S07-04/S07-06
   public boundary only. No forbidden file was intentionally read afterward.

## Decision and next recommendation

- Gate A: `STOPPED_UNKNOWN_SIDE_EFFECT`
- Gate B: `NOT_STARTED`
- Policy update: none
- Candidate update: none
- `DEFER_SCRIPTED_PROBE`

Return to Main for runtime-boundary review. Do not restart the server or apply
the remaining session slots in this task. A future attempt would need a new
explicit authorization and a separately verified cause for the start-boundary
unknown.
