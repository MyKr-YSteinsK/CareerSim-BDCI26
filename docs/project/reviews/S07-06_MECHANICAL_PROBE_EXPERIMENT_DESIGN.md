# S07-06｜Mechanical Probe 首轮实验设计与离线 Policy Freeze

## Status and boundary

- Base: `d5346597d7d2e2730fc8db318bdd31bf616ea4af` (`main == origin/main` at task start)
- Current Candidate: `candidate-v6c-compliance-cleanup`
- Architecture: Single Agent + Three Skills; unchanged
- Design Freeze: ACTIVE
- `NEXT_GAME`: `NOT_AUTHORIZED`
- This artifact is an offline experiment specification. It does not authorize a
  live probe, Candidate change, Skill change, provider call, or CareerSim run.

The question is a coarse mechanical screen, not “which policy scores highest?”:
under one public-only controller boundary, which simple controllers show
protocol failure, repeated investment, missing public progress, survival failure,
or bounded stall pathology before an expensive DeepSeek Agent game is considered?

## Evidence and compliance boundary

The policy surface is limited to participant-visible projection fields:
public time, status/attributes, legal integer choices, public action labels and
descriptions, public warnings/consequences, action receipts, fresh observes,
promotion, and terminal information. The implementation does not import MCP,
Runner, provider, or simulator code.

Structural labels are supported by the public S07 reviews and committed legal
runtime evidence in `docs/project/runs/v6-run1-validation.md`:

- Energy: `准备汇报材料`, `健康恢复`, `人脉维护`, `高强度工作`,
  `处理历史埋雷`, `心理修复`
- Main: `申请关键项目`, `低调避险`

Classification uses exact `choice.action` labels only. It ignores event titles,
event descriptions, and choice descriptions for classification. Mixed or
unrecognised choices become `UNKNOWN_CONTEXT` and use the common P0 fallback.
No hidden data, decoded `.data`, hidden formula/threshold, event-answer table,
or `STRATEGY_EVIDENCE.md` forensic content is used.

## Frozen policy set

The first round retains at most three policies. All policies output one legal
public integer or `DEFER`/`UNSUPPORTED`; none submits actions by itself.

### P0 — `MIN_ID_CONTROL`

Choose the minimum legal public integer choice. This is the protocol/control
baseline and deterministic fallback, not a gameplay recommendation.

### P1 — `SIMPLE_PUBLIC_GROWTH_PRIOR`

For a confidently classified Energy/Main choice set, prefer the minimum-ID
choice with a small public structural `GROWTH` class. Restorative choices are
not ranked against one another. An explicit `MATERIAL` annotation may override
Growth with the minimum-ID restorative choice. That annotation must be supplied
by a future adapter from fresh participant-visible material warning/consequence;
the probe does not infer it from words or titles.

Ordinary story, mixed context, unknown labels, and unavailable structural
classification use P0. No story semantics or answer mapping is attempted.

### P2 — `STALL_AWARE_PUBLIC_GROWTH`

P2 inherits P1. The existing tracker emits
`MECHANICAL_STALL_SIGNAL` only after two adjacent comparable checkpoints for
the same target/path both show no progress. One no-progress checkpoint does not
switch policy. After a stall, P2 may select exactly one different recognized
structural choice as a bounded alternative. If none exists it returns `DEFER`;
it never invents a choice or rotates indefinitely. The signal is diagnostic and
does not itself assert that a live Agent should change action.

## Metrics

Primary coarse-screen metrics are mechanical, not score-ranked:

- Protocol: successful action rate, `DEFER`/`UNSUPPORTED` count, invalid-call
  count, same-session continuity.
- Repetition: repeated-action count, longest repeated structural path, and
  repeated investment after a no-progress checkpoint.
- Progress: comparable checkpoint count, `ADVANCING`, `NO_PROGRESS`,
  `MECHANICAL_STALL_SIGNAL`, and whether a bounded response occurred after a
  stall.
- Progression/survival: public promotion months, final public Level, public
  Skill/Network/Output/Wealth trajectory where exposed, survival months,
  terminal completion, and explicit public warning/consequence count.
- Efficiency: total public actions and structural switch count.

If a participant-visible ending score is normally returned, record it only as a
secondary descriptive outcome. It is not a primary ranking metric and cannot
support a causal improvement or stable-80 claim.

## No-seed batch protocol

S07-04 found no public seed/replay control. Therefore this is an
`independent-session coarse screen`, not a paired deterministic A/B test. Three
sessions per policy are a gross-failure screen only; they are not a variance
estimate or statistical significance claim.

### Gate A — feasibility calibration

Request one complete scripted `P0` session. The session exists only to confirm
that the public loop and bounded report survive a long run, including ordinary
story P0 fallback. If protocol/schema failure, repeated unsupported states,
public/private boundary ambiguity, or unknown side effect occurs, stop before
policy comparison.

### Gate B — small coarse screen

Only after Gate A passes, request at most nine total independent sessions:

- `P0 × 3`, including the Gate A calibration session;
- `P1 × 3`;
- `P2 × 3`.

Use one fixed interleaving decided before execution, for example:

`P0 → P1 → P2 → P1 → P2 → P0 → P2 → P0 → P1`

Do not select later policies from interim score or survival results. A future
session budget proposal is: one direct MCP server start, one initialize and one
`list_tools`, one `new_game`, then only the normal public observe/action calls
needed for that single scripted session. Provider, DeepSeek AgentServer, Skill
install/reload, Runner play, and retries after unknown side effects remain zero.
The proposed budget is not authorization for this task.

## Interpretation and stop conditions

Permitted batch conclusions are:

- `POLICY_MECHANICALLY_INVALID` or `POLICY_MECHANICALLY_VIABLE`;
- `REPEATED_INVESTMENT_PATHOLOGY_OBSERVED`;
- `STALL_ADAPTATION_TRIGGERED` or `STALL_ADAPTATION_NOT_OBSERVED`;
- `PUBLIC_PROGRESS_DIFFERENCE_DESCRIPTIVE_ONLY`;
- `HIGH_VARIANCE` or `INSUFFICIENT_EVIDENCE`.

The batch may not conclude that P2 is optimal, that any policy improves v6c,
that a policy reaches stable 80+, or that a score difference is causal. Without
a public seed, different sessions also cannot be treated as controlled paired
counterfactuals. Story semantics, Skill adherence, compression recovery,
reasoning drift, and LLM tool correctness remain real-Agent questions.

Stop the proposed batch on protocol failure, unknown side effect, hidden/public
boundary violation, unsupported schema, or any need for simulator internals,
provider calls, story lookup, or a second server/session retry outside the
approved budget.

## Main authorization request

`MINIMAL_MECHANICAL_PROBE_BATCH`

Please authorize, separately from this offline task:

1. Gate A: one full scripted `P0` session.
2. If Gate A passes, Gate B: up to nine independent sessions total with the
   fixed P0/P1/P2 3×3 allocation above, counting Gate A as P0 session one.
3. Direct public MCP only; one server lifecycle per session; no AgentServer,
   provider, Skill install/reload, Runner play, or automatic retry.

No Candidate is modified or validated by this design. The next decision remains
with Main.
