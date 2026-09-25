# S07-03｜公开接口廉价策略探针可行性与 Mid-70 瓶颈联合诊断

## Decision summary

- Base: `main@a8319ec2b853a0e4227ea5ba43e91c1269ec32ce`。
- Current candidate: `candidate-v6c-compliance-cleanup`，静态合规清理候选；本任务未修改其身份、manifest、Skill 或 runtime instruction。
- W2 verdict: `PROBE_FEASIBLE_LIMITED_SCOPE`。公开接口足以支持机械状态控制的低成本筛选，但不足以替代真实 Agent 的故事语义、Skill 遵循、上下文恢复和长期 reasoning 验证。
- W3 verdict: `MID70_BASIN_NOT_YET_DIAGNOSABLE`。两局高分记录存在强描述性收敛，但样本量小、事件路径不成对、没有反事实，不能确认统计 basin 或 80+ 瓶颈的唯一原因。
- Combined decision: `BUILD_MINIMAL_PUBLIC_PROBE_NEXT`，仅建议建设一个 public-state mechanical probe；是否执行需另行授权。任何 v6c Agent/game validation 仍需独立 Main Game Gate。
- Candidate decision: 本任务不修改 Candidate；没有足够证据提出应立即加入的新策略规则。

## Identity and evidence boundary

### Current repository facts

- S07-02 已被 Main 接受；W2/W3 已解锁但此前未开始。
- `NEXT_GAME = NOT_AUTHORIZED`，Design Freeze 仍为 `ACTIVE`。
- Candidate identity was rechecked from `configs/current_candidate.json` and `configs/runtime_manifest.json`:
  - Candidate: `candidate-v6c-compliance-cleanup`。
  - Parent: `candidate-v6b-runtime-correctness`。
  - Runtime manifest SHA-256: `cf68e26f23b060372e1c75259c6eabe38b229f00788eccdb9aea71408aeeb4e1`。
  - Instruction SHA-256: `a891fa103f0d4f910c9bbcc5ab91ab8bbbfe4cb242b9506d63374f1cf75d8074`。
  - Three current Skill blobs: Risk `ab20843eadad675dbf7aa8be0178fb52a3791208`, Planning `c4d2bfe065ee3c658e6cff041be87ae8c8c96bdf`, Board `b6d371d74f3477f4f6cdeabe8482093a78cbe3e5`。
- The requested `Project 05-CODEX_WORKFLOW.md` was not present in the current repository tree. No decision below depends on an unverified rule from that missing file; repository `AGENTS.md` and `docs/project/CODEX_PLAN_CONTRACT.md` were used as the available execution contracts.

### PUBLIC_INTERFACE_ONLY firewall

Used evidence was limited to the frozen public Source Lock, Runner/framework source describing the normal public interface, the current candidate contracts, and committed legal trajectory/outcome summaries. The v1 trajectories were recovered from Git history:

- Candidate v1 Run #1: commit `8a933788a93378a8d9ef5598e925048db39ee931e207bab`, `experiments/S04-04-high-score-confirmation/candidate_run1_trajectory.json`, blob `a9ca5d759b05dd0c9b3974c9a1398a3ca3990343`, 27,518 bytes.
- Candidate v1 Run #2: the same commit, `candidate_run2_trajectory.json`, blob `85129980c0591f0ad4d4bee113562bc51116d16d`, 6,811 bytes.
- Original v6 high run: current committed record `docs/project/runs/v6-run1-validation.md`, blob `b35f06d02ae7fcc840a753fcd9059a9525d374cd`.
- Frozen public schedule/interface facts: `docs/project/OFFICIAL_SOURCE_LOCK.md`, `career_sim_runner/prompts/play_headless.md`, `career_sim_runner/ws_client.py`, `career_sim_runner/replay/parse.py`。

`docs/project/STRATEGY_EVIDENCE.md` and the S06-14 simulator-derived pattern material were not used as policy evidence. No decoded data, hidden state, hidden outcome, hidden threshold, future branch result, private/test data, or event-title → answer mapping was used.

## W2｜Cheap Probe Feasibility

### Public interface facts

The frozen Runner's normal public loop is:

`show_employee_handbook → new_game → observe → decision → take_action → fresh observe`。

The replay parser confirms that a normal `observe` result exposes participant-facing time, public status, simulation flags, current event title/description, public choices with integer IDs/action text/descriptions, and optional ending score. A `take_action` call exposes the selected integer choice and notes. `ws_client.py` tracks the public game session from `new_game`/`observe` results and uses a separate JiuwenSwarm drive session for Agent chat.

The repository does not contain a direct scripted MCP client. `headless_play.py` installs a submission, sends a prompt through AgentServer, and lets the Agent call the MCP tools. Therefore a future no-LLM probe would need a separately verified normal MCP/stdio client path; static source inspection alone cannot certify that end-to-end path.

No public seed or deterministic replay control appears in the frozen Runner/public submission contract examined here. Backend seed semantics remain `UNKNOWN`. Fresh sessions can still support gross structural screening, but not low-noise paired counterfactual ranking.

### Feasibility matrix

| Capability | Offline trajectory diagnosis | Scripted public-interface probe | Real DeepSeek Agent required | Assessment |
|---|---|---|---|---|
| Energy allocation | `OFFLINE_DIAGNOSTIC_FEASIBLE`: count selections and compare public before/after state | `SCRIPTED_PUBLIC_LIVE_FEASIBLE` if direct tool path is verified | Needed for story/semantic choices around Energy | Good narrow probe target; no counterfactual from existing logs |
| Main action selection | Feasible for observed frequency, legal menus and public state | Feasible for deterministic menu/state rules | Required for ambiguous narrative meaning | Mechanical screening only |
| Survival constraint | Feasible for observed Health/survival trends and warnings | Feasible for explicit public trend/constraint guards | Required for ambiguous trust/compliance/escalation semantics | Public guard can be screened; efficacy needs Agent |
| Primary Gap | Feasible as a reconstructed public-state label | Feasible as a scripted controller field | Required to judge ambiguous strategic meaning | Useful controller observable |
| Progress / `STALLED` | Feasible when comparable public before/after records exist | Feasible with two fresh comparable observations | Required when attribution is ambiguous | Good offline/probe target; one no-growth observation is insufficient |
| Observed effect adaptation | Feasible for recorded receipts and fresh deltas | Feasible when action receipt and fresh observe are available | Required for narrative interpretation | Transferable mechanical target |
| Repeated investment / saturation | Feasible descriptively | Feasible for repeated public action/state patterns | Required when the same label has ambiguous meaning | Probe can reject obvious lock-in |
| Review / promotion reset | Feasible for observed feedback/promotion timing | Feasible when public feedback and promotion result are exposed | Required for qualitative readiness interpretation | No hidden readiness formula allowed |
| Horizon handling | Feasible from public month/quarter and 48-month contract | Feasible as a month-aware controller | Agent needed for trade-off semantics | Low-cost controller target |
| Simple Growth prior | Feasible only as historical/descriptive replay; no real counterfactual | Feasible for mechanical Energy/Main policy | Agent needed for story candidates and risk semantics | Candidate ablation target, not score predictor |
| Risk override | Feasible for public warnings and candidate consequences already recorded | Feasible for explicit public Material Risk | Required for ambiguous story risk | Keep public-evidence boundary; no cue taxonomy |
| Controller complexity | Feasible for static policy comparison and action/repetition counts | Feasible for protocol cost/action validity | Required for actual LLM deliberation cost/drift | Probe can measure mechanics, not reasoning quality |
| Ordinary story semantic reasoning | `LOW_INFORMATION_VALUE` from action logs alone | `LOW_INFORMATION_VALUE` without an Agent or an allowed semantic oracle | `REAL_AGENT_REQUIRED` | Do not replace with title lookup |
| Skill adherence | Not inferable from final trajectory alone | Not testable with a non-Agent controller | `REAL_AGENT_REQUIRED` | Includes reread/recovery and owner-boundary behavior |
| Compression recovery | Static contract is inspectable, runtime adherence is not | Not a meaningful non-Agent substitute | `REAL_AGENT_REQUIRED` | Requires a real context-compression epoch |
| Reasoning drift / oscillation | Partial transcript diagnosis only | Not represented by a deterministic controller | `REAL_AGENT_REQUIRED` | A scripted controller can avoid drift, not measure it |
| Tool-use correctness | Feasible by parsing recorded public calls/receipts | Feasible for integer choice, observe→action sequencing and error handling | Agent required to test whether LLM follows the contract | Separate protocol correctness from Agent adherence |

### Probe value and boundary

A minimal probe has real but limited screening value if it is restricted to:

1. public `observe` state and legal choices;
2. one integer `take_action` with public receipt;
3. fresh observe after each successful state-changing action;
4. deterministic Energy/Main policies using only public month, status, choices and observed deltas;
5. bounded logging of action validity, public state trend, repeated investment, promotion timing and terminal survival.

It could eliminate mechanically invalid, obviously repetitive or visibly non-progressing controllers before spending a DeepSeek Agent game. It cannot estimate a counterfactual score, choose ambiguous story answers, measure Skill adherence, reproduce compression recovery, or establish stable 80+ without Agent runs. With no confirmed seed control, it is a coarse filter rather than a paired benchmark.

**W2 final verdict: `PROBE_FEASIBLE_LIMITED_SCOPE`.** A future probe is worth building only as a mechanical public-state screen. Direct client startup, tool registration, and cost/repeatability must be verified in a separately authorized task; this task did not perform that live confirmation.

## W3｜Mid-70 Basin Diagnosis

### High-run comparison

| Public outcome | Candidate v1 Run #1 | Original v6 Run #1 |
|---|---:|---:|
| Quantitative score | 76.04 | 75.29 |
| Competition partial | 53.23 | 52.70 |
| Survival | 48 months | 48 months |
| Grade | A | A |
| Final Level | L6 | L6 |
| Final Wealth | 40.5 | 39.5 |
| Final Resilience | 19 | 17 |
| Final Skill | 139 | 142 |
| Final Network | 52 | 58 |
| Promotions | M6, M12, M18, M36, M48 | M6, M12, M18, M36, M48 |
| Quarterly Main | `申请关键项目` 16/16 | `申请关键项目` 14/16; `低调避险` 2/16 |

These are descriptive records from different candidate/runtime and event trajectories. Similar terminal outcomes do not establish a statistical basin, causal convergence, or a score ceiling.

### v1 Run #1 public trajectory

The compact legal trajectory recovered from Git contains 49 monthly public snapshots, 16 quarterly decisions, five promotion records and three planning checkpoints. Selected public states were:

| Month | Level | Skill | Network | Output | Health | Wealth |
|---:|---|---:|---:|---:|---:|---:|
| 6 | L2 | 13 | 5 | 6 | 7 | 2 |
| 12 | L3 | 24 | 7 | 7 | 7 | 4 |
| 18 | L4 | 44 | 19 | 16 | 10 | 6 |
| 24 | L4 | 63 | 36 | 26 | 8 | 10 |
| 30 | L4 | 82 | 36 | 26 | 10 | 15 |
| 36 | L5 | 100 | 36 | 29 | 9 | 21 |
| 42 | L5 | 115 | 54 | 38 | 9 | 30 |
| 48 | L6 | 138 | 51 | 40 | 9 | 39 |

The run selected `申请关键项目` in every quarterly Main decision. Its quarterly Energy selections were concentrated in `准备汇报材料` and `健康恢复`, with additional `人脉维护` and `处理历史埋雷`; exact counts in this compact quarterly field are 25, 11, 6 and 3 respectively. This field is not directly comparable in unit definition to the original v6 record's 41-action aggregate, so it is used for structure, not as a cross-run resource total.

The public trajectory also contains temporary plateaus: Network and Output were unchanged from M24 to M30, then both later increased. This is evidence that one observed plateau does not prove a path is permanently invalid; a strict comparable-checkpoint rule is more defensible than immediate switching.

### Contrast and material unknowns

Candidate v1 Run #2 reached only 25 months and grade D with 35.31 / 24.72. It matched Run #1 on 6 of the first 7 quarterly Main choices, reached L4 at M24 instead of M18, and ended with public terminal state L4 / Skill 44 / Network 20 / Wealth 3.9 after a recorded trust-crisis termination. The same candidate family therefore exhibits high observed variance; matching Main frequency is not sufficient evidence of a stable route.

The original v6 record reports late repeated `申请关键项目` / `准备汇报材料` behavior after public Output or Network stopped showing the expected gain, while formal Planning checkpoints were concentrated early. The exact month-by-month v6 public state and the full v1↔v6 event-path overlap are not available in the committed compact record. V6's final Output trajectory, event opportunities, and action-level causal attribution are `UNKNOWN`.

### Diagnosis

The strongest supported statement is:

> Both successful A/48-month runs reached a similar public progression band, but the evidence does not distinguish a genuine mid-70 basin from shared promotion/wealth/skill opportunity paths, score-dimension convergence, or ordinary event stochasticity.

The most actionable public signal is not Main action frequency. It is whether a current Primary Gap continues to show comparable observed progress after repeated investment, especially late in the horizon. That signal is already a hypothesis in the v6c contract; this review does not justify changing the Candidate before runtime validation.

## Hypotheses retained for Main review

Only the following three hypotheses are retained.

### H1 — Observed-progress control is the highest-value transferable lever

- **Statement:** A controller that compares repeated investment against fresh comparable public effects, preserves a path through one observation, and requires a bounded alternative review after two comparable stalls may reduce mechanical lock-in without turning every plateau into a switch.
- **Evidence:** Original v6 reported repeated project/report actions with no expected public Output/Network growth and early-concentrated Planning. V1 Run #1 shows a temporary M24–M30 plateau followed by later recovery, so immediate switching would be overfit.
- **Mechanism:** Primary Gap + observed effect + two-checkpoint `STALLED` review + public horizon.
- **Alternative / counterevidence:** Different event opportunities may explain the v6 plateau; v1's later recovery may be trajectory-specific; exact v6 timing is unavailable.
- **Expected benefit / stable-80 relevance:** Medium-to-high for reducing repeated-action lock-in and improving late public opportunity use; no score benefit is proven.
- **Falsifier:** Repeated public runs show reliable progress despite the repeated action, or a bounded stall review produces no measurable change in public progression under comparable conditions.
- **Cheap-probe fit:** High for mechanical state/action/repetition diagnostics; low for ambiguous story semantics.
- **Real DeepSeek validation:** Required for full policy adherence and outcome effect.
- **Compliance risk / complexity:** Low if limited to public state and no title lookup; low-to-medium implementation complexity. No Candidate change is adopted here.

### H2 — The apparent Mid-70 band is a convergence hypothesis, not a proven basin

- **Statement:** Similar Level, promotion timing, Wealth, Skill, Network and Resilience across two successful runs may indicate a public terminal-state convergence that limits incremental gains, but it is not yet diagnosable as a stable basin.
- **Evidence:** Both high runs are A/48m, L6, and promote at M6/M12/M18/M36/M48; their final public dimensions are close. V1 Run #2 supplies direct high-variance counterevidence within the same candidate family.
- **Mechanism:** Shared opportunity/progression paths or late-stage dimension convergence could produce similar scores even when local decisions differ.
- **Alternative / counterevidence:** n=2 high runs, non-paired event paths, candidate/runtime differences, and unavailable v6 monthly fields. The score closeness may be coincidental.
- **Expected benefit / stable-80 relevance:** High diagnostic relevance, but no direct policy rule is justified from it.
- **Falsifier:** Additional public runs with materially different terminal dimensions at similar scores, or repeated 80+ outcomes without leaving this apparent band.
- **Cheap-probe fit:** Offline diagnostic only; a scripted mechanical probe cannot establish the score basin.
- **Real DeepSeek validation:** Required for repeatability and any outcome claim.
- **Compliance risk / complexity:** Low as a hypothesis; high risk if converted into hidden score weights or a fixed terminal-state target. No such conversion is made.

### H3 — Simple Growth prior + public Risk override is the right ablation baseline

- **Statement:** Before adding more controller complexity, compare a simple public-state Growth prior with an explicit public Material-Risk override against the fuller v6c controller.
- **Evidence:** Both high runs maintain substantial growth and survive 48 months despite different Main distributions; v1 Run #2 terminates after a trust-crisis path despite similar early Main frequency. S06 closeout already proposed this as a later controlled ablation, not as a proven winner.
- **Mechanism:** Preserve ordinary growth when no fresh material public risk is present; let explicit public survival/trust/compliance evidence constrain the current candidate.
- **Alternative / counterevidence:** Differences may be dominated by event opportunities, story semantics, or agent adherence; a simpler policy may lose useful planning adaptation.
- **Expected benefit / stable-80 relevance:** Medium as a complexity/rework diagnostic; it may reveal whether the full controller adds value beyond the basic public guard.
- **Falsifier:** Repeated controlled Agent runs show the simpler baseline has materially worse survival or progression, or no observable separation is possible.
- **Cheap-probe fit:** Partial: mechanical Growth/Risk state rules can be screened; story and adherence cannot.
- **Real DeepSeek validation:** Required for the actual ablation decision.
- **Compliance risk / complexity:** Low if no hidden thresholds, lookup table, or evaluator weight is introduced; low implementation complexity. No policy patch is made here.

## Combined decision and next boundary

- W2 supports a **narrow mechanical probe**, not a cheap replacement for Agent gameplay.
- W3 does not support a stable Mid-70 basin claim or a unique score bottleneck.
- The first high-value probe, if Main authorizes it, should measure public state/action validity, observed deltas, repeated investment, promotion timing and survival termination across a small number of explicitly bounded scripted policies. It must not score story answers, use hidden state, or claim counterfactual outcomes.
- No Candidate/Skill change is justified by this review. The current v6c policy remains a hypothesis candidate and still requires a separate Game Gate for Agent validation.
- Proposed next boundary: `BUILD_MINIMAL_PUBLIC_PROBE_NEXT`, with direct MCP/client feasibility and repeatability treated as a precondition. If that precondition cannot be established without broad runtime work, return to Main with `LIVE_CONFIRMATION_REQUIRED` and defer the probe.

## Verification and operation accounting

- Latest `origin/main` fetched and fast-forwarded to `a8319ec2b853a0e4227ea5ba43e91c1269ec32ce`。
- Current v6c candidate, manifest/instruction hash and three Skill blobs rechecked; no identity drift.
- Historical v1 trajectories parsed read-only from Git objects; no raw logs, runtime DB, simulator data or hidden source was opened.
- Runner public interface source was read statically only; no MCP client, service, provider or gameplay path was invoked.
- `git diff --check`: required after artifact creation.
- Files changed by this task: this review artifact only.
- Provider requests: `0`。
- CareerSim service starts/reloads: `0`。
- MCP live calls: `0`。
- `new_game`: `0`；live `observe`: `0`；`take_action`: `0`；Runner gameplay: `0`。
- Candidate, Skill, runtime manifest, Runner, dependency and lockfile mutation: `0`。

## Problems / unknowns

- **Recovered after bounded read-only fallback:** historical S04 experiment directories are absent from current checkout but were recovered from the recorded Git commit; compact JSON was parsed successfully.
- **Skipped with limitation:** direct MCP scripted-client startup, public seed discovery, and repeatability testing; all require live/runtime confirmation not authorized here.
- **Unknown:** full original-v6 monthly public trajectory, v1↔v6 event-path comparability, action-level counterfactual outcomes, story semantics, Skill adherence, context-compression recovery, and any causal contribution to score.
- **Blocking:** none within this offline task. These unknowns block stronger W3 claims and full probe validation, not the review artifact itself.
