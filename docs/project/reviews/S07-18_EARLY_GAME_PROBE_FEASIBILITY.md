# S07-18｜Early-game Probe 可行性与实验设计

## Identity and decision

- Task: S07-18; repository: `MyKr-YSteinsK/CareerSim-BDCI26`.
- Verified base: `main@886cadb8c0f70923922f2177d15f33e46d92f3a3` = `origin/main`; working tree was clean before this document.
- Scope: public-interface / engineering evidence and offline experiment design only.
- Live operations in this task: `0`.
- Lifecycle decision: **`EARLY_STOP_NOT_PUBLICLY_SUPPORTED` for the last verified participant-facing MCP interface**.
- S07-19 recommendation: three bounded fresh-session slots, each played to public terminal; capture M1–M18 densely and continue naturally afterward. This is a proposal, not live authorization.

## Evidence → investigation → decision

### Evidence

1. The committed S07-04 public `list_tools` response enumerated `new_game`, `observe`, `take_action`, `check_latest_logs`, and `show_employee_handbook`. Its recorded schemas expose no `abandon`, `close_session`, `end_game`, `reset`, `dispose`, or `delete_session` operation. The same record reports no public seed/replay control. See [S07-04 confirmation](S07-04_MINIMAL_PUBLIC_PROBE_LIVE_CONFIRMATION.md).
2. The reusable public bridge starts one `career-emulator-mcp` stdio child, enters `stdio_client` / `ClientSession` context managers, and calls `new_game`, `observe`, and `take_action`. Exiting the context requests shutdown of that child process; the bridge contains no per-game close/abandon call. See `scripts/codex_public_agent_driver.py` around `run_pilot` and its shutdown message.
3. The frozen public runner prompts describe continuing the same game until its normal end; they do not document a safe early-stop operation. `OFFICIAL_SOURCE_LOCK.md` describes the 48-month public horizon. Neither source provides an explicit M18 session-disposal contract.
4. An attempted read of the Source-Lock-linked official documentation through the available documentation browser was inaccessible, and the follow-up official-domain search returned no results. No claim below relies on undocumented package internals.

### Investigation

`stdio_client` context shutdown establishes only that the local MCP transport child is closed. It does not establish that the remote game session is deleted, terminalized, or otherwise safely released. Treating process termination, disconnect, DB cleanup, a fabricated terminal event, or an unlisted/private method as session disposal would exceed the public contract.

The S07-04 tool listing is a complete observed listing for that run, but it is historical evidence. It supports a bounded conclusion about the last verified public interface, not a universal claim that no future version could add lifecycle support. Because this task forbids live calls, current deployment tool discovery was not repeated.

### Decision

**`EARLY_STOP_NOT_PUBLICLY_SUPPORTED`** on the evidence currently available. Do not stop a session at M18 and do not kill/restart a process or mutate local/shared storage to imitate safe closure. S07-19 should capture early checkpoints and then let each session reach its normal public terminal state before closing that run's MCP process and starting another serialized fresh session.

If a later authorized task finds a newer documented participant-facing lifecycle operation, it must verify that operation's scope and behavior before using it; this finding can then be superseded with evidence. Until then, early-stop feasibility is not assumed.

## W3｜Compact early-game evidence schema

Record checkpoints at `INITIAL`, `M3`, `M6`, `M9`, `M12`, `M15`, and `M18`; if the public game ends earlier, record a `TERMINAL` checkpoint and mark later checkpoints `NOT_REACHED`. Each checkpoint is based on fresh participant-visible state and contains:

| Field | Representation |
|---|---|
| Month | Public month; retain the checkpoint label separately. |
| Level | Fresh public value or `UNKNOWN`. |
| Health | Fresh public value or `UNKNOWN`. |
| Skill | Fresh public value or `UNKNOWN`. |
| Network | Fresh public value or `UNKNOWN`. |
| Output | Fresh public value or `UNKNOWN`. |
| Wealth | Fresh public value or `UNKNOWN`. |
| Recent public review | Concise public request/feedback summary, or `NONE` / `UNKNOWN`. |
| Promotion status | Public promotion since previous checkpoint: yes/no/unknown and month if observed. |
| Important opportunity accepted? | Yes/no/unknown; identify only the public opportunity, not an inferred hidden type. |
| Visible delivery evidence? | Yes/no/unknown plus the public receipt/result if any; acceptance is not delivery. |
| Important public mistake/warning? | Concise public warning/consequence or `NONE` / `UNKNOWN`. |
| Main action since prior checkpoint | Public action labels and counts; use `NONE` at initial. |
| Energy allocation since prior checkpoint | Public action labels/counts (and units only if directly exposed); use `NONE` at initial. |

To answer whether a public action was followed by a visible change, retain a compact action ledger between checkpoints: action month and public label, completed/rejected receipt, the immediately following fresh-observe values that changed, and `UNKNOWN` where comparison is unavailable. This is temporal observation, not causal attribution; intervening public events or actions must be noted as possible contamination. Do not retain full raw event prose in the durable summary.

### Descriptive outcome labels

Apply only after M18 or an earlier terminal, against the public M6/M12/M18 reference anchors in the task:

- **`REFERENCE_LIKE`** — across reached checkpoints, the broad Level/Output/Wealth progression pattern is generally near the descriptive references; list any dimension or checkpoint that differs.
- **`LAGGING`** — multiple public dimensions remain clearly behind across successive comparable checkpoints, or the run terminates before M18.
- **`MIXED`** — dimensions or checkpoints diverge in different directions, or evidence is too incomplete for either broad label.

These are analyst labels, not numeric cutoffs, promotion rules, score targets, or in-game triggers. Do not interpolate missing checkpoints or infer hidden thresholds.

## W6/W7｜Proposed S07-19 design (not authorized)

### Question and sample count

Question: among fresh public trajectories, what public opportunity, action/receipt, review, and observed-state patterns are already associated with the earliest divergence from the M6/M12/M18 75+ descriptive references?

Recommend **3 fresh sessions maximum**, not 4–6. The last verified interface has no safe public M18 close operation, so each session must continue to its ordinary public terminal; 3 sessions still produce three early windows while bounding full-game cost. A naturally earlier terminal is recorded and is not retried with a replacement game.

Use the same high-level player objective and the same descriptive references for all three sessions. Codex remains the sole semantic decision-maker and chooses each action from the fresh current public state. Do not encode ratios, month-to-action rules, candidate rankings, event mappings, or automatic selectors. Record cross-run learning, but do not call the runs paired or causal; if the player strategy changes between runs, identify the change in the analysis.

### Protocol and proposed budget for a future Main decision

For each session, run serially: one direct MCP lifecycle → one `new_game` → fresh public decisions/actions → normal public terminal → shutdown of that same MCP child. Start the next fresh session only after the prior session has reached terminal and the prior transport is closed.

Proposed ceilings, per session:

- direct MCP server start/lifecycle: `1`;
- `initialize`: `1`; `list_tools`: `1`;
- `new_game`: `1`;
- `take_action` attempts: `≤350`;
- `observe`: `≤351` (one initial observe plus at most one fresh/reconciliation observe per action attempt; a completed rejection uses its reconciliation observe, and an ambiguous transport outcome may be checked once before stopping); never resend after unknown outcome;
- provider / DeepSeek: `0`; AgentServer: `0`; Runner gameplay: `0`; install/reload: `0`.

Batch maximum: `3` sessions, `3` `new_game`, and `3` direct MCP lifecycles. Any live execution requires a separate explicit Main authorization; this document grants none.

### Checkpoint focus

At each checkpoint, compare only public descriptive anchors:

| Checkpoint | 75+ reference anchor |
|---|---|
| M6 | L2; Output 5–6; Wealth 2–3 |
| M12 | L3; Output 7; Wealth 4 |
| M18 | L4; Output 16–17; Wealth 6–8 |

For each window, inspect: public opportunity and whether accepted; directly observed action/result deltas; pre-review state and review request; promotion or no promotion; post-review response; public mistakes/warnings; Main/Energy mix. State whether an apparent difference was already present before M6, first visible at M6, or first visible later. No hidden formula or counterfactual conclusion is permitted.

### Runtime estimate and efficiency

S07-17 provides one observed full 48-month Codex session of `20m59s` (R3); the two earlier runs ended at M24 after `13m05s` and `11m26s`. The three-run start-to-final-shutdown span was `47m37s`, but only one of those sessions completed 48 months. A rough planning estimate for three full sessions is **about 60–90 minutes of gameplay interaction**, plus **10–20 minutes** for preflight and compact synthesis. This is a planning range extrapolated from one full session, not a runtime guarantee.

This design does **not** reduce the cost of an individual full session: safe M18 disposal is unproven. It improves information density by pre-registering seven early checkpoints, action-to-next-observe records, review windows, and a three-session ceiling, rather than spending the same budget on loosely structured full-run narratives or six full games. If Main requires actual runtime savings, a publicly documented lifecycle or another independently proven safe isolation method is needed first.

## Boundaries and limitations

- This is offline feasibility/design only. No game, MCP, service, provider, Runner, or AgentServer was started or called.
- Public seed/replay control was absent from the S07-04 observed schema; S07-19 sessions therefore cannot be treated as seeded pairs.
- The official documentation pages linked by the Source Lock were not accessible through the available browser during this review. The lifecycle verdict is therefore scoped to the recorded public tool listing and repository bridge, not an exhaustive claim about all possible future or undocumented interfaces.
- S07-17 timings are a small convenience sample; live interaction duration and natural terminal timing may vary substantially.
- No Candidate, Skill, runtime manifest, Runner, dependency, `CURRENT_STATE.md`, or ADR changes are proposed.

## Safety accounting

| Operation | Count |
|---|---:|
| Direct MCP / CareerSim service starts | 0 |
| Gameplay `new_game` | 0 |
| Gameplay `observe` | 0 |
| `take_action` | 0 |
| AgentServer starts | 0 |
| Provider / DeepSeek calls | 0 |
| Runner gameplay | 0 |
| Hidden/private data access | 0 |

## Next recommendation

`RETURN_TO_MAIN_FOR_S07-19_SCOPE_AND_LIVE_AUTHORIZATION` — decide whether to authorize the proposed three-session, natural-terminal batch. Do not implement an early-stop workaround or begin a game under S07-18.
