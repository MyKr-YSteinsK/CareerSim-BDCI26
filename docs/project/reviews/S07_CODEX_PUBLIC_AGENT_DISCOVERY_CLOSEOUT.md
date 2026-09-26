# S07｜Codex Public-Agent 探索线收口

## Scope and decision

本记录收口 S07-13 至 S07-18 的 Codex Public-Agent 探索线，不是 S07 Stage closeout。

- Verified base: `main@acdeeb894953cd248d45f6de4cda3c9b0af2073c` = `origin/main`.
- Decision: `CODEX_PUBLIC_AGENT_DISCOVERY_CLOSED_FOR_NOW`.
- Formal Candidate: `candidate-v6c-compliance-cleanup`，保持不变；Design Freeze 仍为 ACTIVE。
- `S07-19` early-game batch: `DEFERRED`，不是 rejected；本 closeout 不授权新实验。
- Handoff: `FORMAL_CANDIDATE_SCAFFOLD_PARITY_READY`，应在新的 Codex conversation 中开始；本任务不启动它。

## Run summary

| Run | Result | Quantitative / partial | Survival / grade | Final or last public Level | Evidence role |
|---|---|---:|---|---|---|
| S07-13 | technical partial; M3 后 ambiguous `success=false`，未到 terminal | UNKNOWN / UNKNOWN | M3 partial / UNKNOWN | L1 at M3 | 不作为 gameplay score evidence |
| S07-14 | completed | 65.16 / 45.61 | 48m / B | L5 | 完整 Codex-as-Player run |
| S07-15 R1 | technical partial; new game 后未提交 player action | UNKNOWN / UNKNOWN | UNKNOWN / UNKNOWN | L1 at M1 | 不作为 gameplay outcome |
| S07-15 R2 | completed | 54.85 / 38.39 | 48m / C | L4 | 完整 Codex-as-Player run |
| S07-15 R3 | natural elimination | 16.55 / 11.58 | 12m / E | L2 | 完整至 terminal 的短局 |
| S07-15 R4 | completed | 57.90 / 40.53 | 48m / C | L5 | 完整 Codex-as-Player run |
| S07-17 R1 | eliminated | 21.36 / 14.95 | 24m / E | L1 | 完整至 terminal 的短局 |
| S07-17 R2 | eliminated | 22.82 / 15.97 | 24m / E | L1 | 完整至 terminal 的短局 |
| S07-17 R3 | completed | 63.88 / 44.72 | 48m / B | L5 | 完整 Codex-as-Player run |

S07-15 R2/R4 的 public terminal status flags 与 ending-score completion 字段存在记录内不一致；对应 run record 以 explicit `ending_score` 的 `completed=true` / 48-month outcome 记表，并保留该矛盾，不从 DB 补证。S07-15 R1 和 S07-13 的未决/技术 partial 不当作策略失败或分数样本。

来源： [S07-13 review](S07-13_CODEX_PUBLIC_AGENT_PILOT_REVIEW.md)、[S07-14 run](../runs/s07-14-clean-codex-public-agent-pilot.md) / [review](S07-14_CLEAN_CODEX_PUBLIC_AGENT_PILOT_REVIEW.md)、[S07-15 run](../runs/s07-15-codex-public-agent-4run-discovery.md) / [review](S07-15_CODEX_PUBLIC_AGENT_4RUN_DISCOVERY_REVIEW.md)、[S07-16 differential](S07-16_PUBLIC_TRAJECTORY_DIFFERENTIAL_REVIEW.md)、[S07-17 run](../runs/s07-17-targeted-codex-3run.md) / [review](S07-17_TARGETED_CODEX_3RUN_REVIEW.md)。

### Closed workstream roles

| Task | Role / accepted boundary |
|---|---|
| S07-13 | Initial Codex public-agent pilot; technical partial at M3, ambiguous action outcome, no terminal score. |
| S07-14 | Clean Codex-as-Player pilot; one completed 48-month trajectory, descriptive only. |
| S07-15 | Four-slot public-prior strategy discovery; one technical-only slot, two 48-month runs and one M12 elimination. |
| S07-16 | Offline public-trajectory differential and bounded strategy hypotheses; no gameplay. |
| S07-17 | Targeted-prior three-run exploration; sequential/adaptive, no paired or causal inference. |
| S07-18 | Early-stop lifecycle feasibility and S07-19 design; no gameplay evidence and no live authorization. |

## What was proven

- Direct participant-facing MCP 可供 Codex 作逐步 player；S07-14、S07-15 R2/R4、S07-17 R3 都完成了 48 个月 public trajectory。桥接代码承担 transport / projection / legality / logging，玩家选择由 Codex 明确提交。
- 这条 research route 在工程上可行，且完全不依赖 AgentServer 或 DeepSeek/provider。S07-13 的 ambiguous receipt 被留作技术 partial；S07-14 后续验证了 completed rejection 的 fresh-observe reconciliation。
- 本组已观察到完整 run 的分数范围从 54.85 到 65.16，另有自然早退局。Best observed 是 S07-14 `65.16 / 45.61 / 48m / B`；没有达到 70+ 或 75+ reference。
- 多个 Codex run 相对 v1/v6 75+ references 的 Level/Output/Wealth 差异在 M6 已可见，至 M18/M24 多数仍存在。这是 repeated descriptive observation，不是因果转折点。
- S07-18 是 lifecycle/experiment feasibility analysis：`EARLY_STOP_NOT_PUBLICLY_SUPPORTED`。最近一次已验证的 public MCP tool listing 未显示 session abandon/end/reset/delete；关闭 stdio child 不等于结束游戏。S07-18 的 game、`new_game`、gameplay observe、`take_action` 均为 0。

## What was not proven

- 不能据此判断 Luna Max 与 DeepSeek Flash 哪个模型更强，也不能把模型差异与策略差异分离。
- Codex runs 没有执行正式 Candidate 的完整 persistent runtime scaffold；它们使用 Codex、各任务指令及 public priors/brief，通过 direct MCP 决策。
- 这些 unseeded、非配对且部分跨 run 自适应的轨迹不能证明任一 action/Skill 导致分数变化、不能形成稳定分数估计，也不能证明 stable 80+。
- S07-18 没有运行游戏，不增加 gameplay performance evidence；也没有证明所有未来版本永远不存在合法 early-stop API。
- 当前没有足够证据把探索假设写入正式 Candidate。固定 Main/Energy 比例、关键项目/汇报/网络 action 配额、晋升门槛或 hidden score rule 均不受支持。

## Scaffold mismatch｜核心比较限制

| Formal Candidate v6c artifact / intended control scaffold | Previous Codex Public-Agent runs |
|---|---|
| Persistent instruction；`structured-state-board`、`rolling-planning`、`risk-review`；正式控制链设计为 `fresh observe → Board → Planning → candidate → Risk gate → take_action → fresh observe` | Codex LLM；Task instructions、public prior / S07-16 strategy brief；direct public MCP |
| v6c 本身仍未 runtime/provider validated。原始 v6 曾以 `deepseek-flash` 完成一局，但该结果不转移给 v6c。 | Codex 根据当前 public state 自主选择；未以正式 Candidate 的完整控制链作为 gameplay controller |

各 Codex run record 明确记载 formal Candidate Skills / manifest 未用作本局 gameplay policy。因此把 `75+` historical Candidate runs 与 `55–65` Codex runs 直接解释成 `DeepSeek > Luna` 或 `Luna > DeepSeek` 都是无效归因：scaffold 不同、无 public seed、event/opportunity path 不同，Candidate 与 player decision process 也不同；并且 v6c 自身尚无 runtime/provider validation。下一步应先做 **Formal Candidate Scaffold Parity**，再讨论模型比较。

## Public hypotheses retained

以下只保留为待验证假设 / 证据纪律，不是已验证 Candidate policy：

1. Review feedback 可转成一个待观察的下一窗口结果；之后用 fresh public evidence核验，而不是把采取了行动当作完成。
2. Project/opportunity 与可见 delivery 分开记；申请、投入或汇报次数本身不等于兑现结果。
3. Repeated investment 判断优先看可比较 fresh observed effect；activity volume 不能替代 outcome。
4. 公开 affordability deterioration 可作为独立约束信号，但不导出固定财富阈值或财富最大化策略。
5. 不传播未经确认的组织敏感信息；只基于当前公开证据判断。
6. Early progression（尤其 M6–M18）适合做诊断窗口，但不能把参考值变成 month/action rule。

反例仍然重要：Candidate v1 #1 的关键项目 `16/16` 对应 76.04，而 S06 Run #1 同为 `16/16` 仅 53.83；S07-15 R4 大量 report/network action 仍为 57.90；同一 v1 Candidate 两次结果为 76.04 与 35.31，量化分差 40.73。故 action counts 不是策略配方，跨局结果显示显著方差。

## S07-18 lifecycle finding and S07-19 disposition

S07-18 的具体证据、early-game schema、分类定义及三 session 自然终局方案见 [S07-18 feasibility review](S07-18_EARLY_GAME_PROBE_FEASIBILITY.md)。目前没有安全公开的 M18 session-close 证据；若未来只为 early checkpoints 运行，也仍需自然到 terminal，除非另有经证实的 public lifecycle。

S07-19 原方案为 early-game-focused batch，但本收口将其标为 **`DEFERRED / NOT CURRENT NEXT STEP`**，不代表否定其价值。更优先的问题是先控制 scaffold mismatch：确认 Codex/Luna 在加载正式 runtime instruction 与三 Skill 后，public trajectory 是否变化。S07-19 的三局早期 batch 可在该问题之后由 Main 重新排期和授权。

## Current formal Candidate identity

复核的当前文件身份：

- Candidate: `candidate-v6c-compliance-cleanup`; parent: `candidate-v6b-runtime-correctness`。
- Runtime manifest SHA-256: `cf68e26f23b060372e1c75259c6eabe38b229f00788eccdb9aea71408aeeb4e1`；instruction SHA-256: `a891fa103f0d4f910c9bbcc5ab91ab8bbbfe4cb242b9506d63374f1cf75d8074`。
- Three Skill blobs: `structured-state-board` `b6d371d74f3477f4f6cdeabe8482093a78cbe3e5`; `rolling-planning` `c4d2bfe065ee3c658e6cff041be87ae8c8c96bdf`; `risk-review` `ab20843eadad675dbf7aa8be0178fb52a3791208`.
- Architecture: Single Agent + three Skills; Memory `NOT_IMPLEMENTED`; fifth Skill / Team / Swarm `DEFERRED`; Design Freeze `ACTIVE`; gameplay/provider validation for v6c remains `NOT_PROVEN`; `NEXT_GAME = NOT_AUTHORIZED`.

These identities were read/hashed for verification only. No Candidate, Skill, runtime manifest, Runner, dependency, `CURRENT_STATE.md`, or ADR was modified. S07 remains active; this is not an S07 Stage completion.

## Handoff

`FORMAL_CANDIDATE_SCAFFOLD_PARITY_READY`

The next task should run in a **new Codex conversation**, fresh-read the latest repository versions of `configs/runtime_manifest.json`, `configs/current_candidate.json`, and all three formal Skills, and separately define its evidence/live authorization. This closeout does not start that task and authorizes no gameplay.

## Safety and verification

- This task: provider / AgentServer / MCP / game / `new_game` / gameplay observe / `take_action` / Runner gameplay = `0`.
- Formal Candidate mutation = `0`; no historical/raw evidence was deleted.
- Source identity: `origin/main` matched the expected base before work; all referenced records and current Candidate identities were present.
- `git diff --check`: pending final closeout verification.
