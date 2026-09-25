# ARCHITECTURE_DECISIONS

> 只记录当前有效决定；已结束阶段的证据与旧决策过程由 Git 历史保存。

## AD-001 — Single Agent + Three Skills

- 保持 Single Agent + Multiple Skills；Single Agent 是唯一 take_action submitter。
- Current Skills: risk-review, structured-state-board, rolling-planning。
- 不因职责分工本身增加 agent、action writer 或常驻 orchestration loop。

## AD-002 — Evidence-driven runtime policy candidate

- Original candidate `candidate-v6-auditable-control-loop` remains Main-accepted static work; its S06-24 single run was `VALID_48M_COMPLETION` (75.29 / 52.70 / A) but `RUNTIME_ADHERENCE_FAIL`.
- Current candidate is `candidate-v6b-runtime-correctness`, parent v6; S06-25 changes only runtime/audit correctness contracts, not gameplay strategy. It is static-only and NOT_RUNTIME_VALIDATED. S06 Main acceptance=`PASS_WITH_KNOWN_RUNTIME_LIMITATION` and S06=`COMPLETE`; NEXT_GAME = NOT_AUTHORIZED; Design Freeze = ACTIVE.
- Candidate identity and exact submission instruction are in configs/current_candidate.json and configs/runtime_manifest.json.
- Main-accepted v6 strategy contracts remain context recovery, candidate-first Risk ordering, fresh-state refresh, one Primary Gap and public survival-trend Risk Budget, review/promotion reset, observed > advertised, strict two-checkpoint STALLED, bounded RECONSIDER, joint Energy + Main planning, and bounded story top-2. v6b adds a canonical notes-prefix audit surface, decision-closed handoff, one-integer Energy calls, and explicit compression recovery; these are static contracts, not evidence of v6b runtime adherence or benefit.
- Further offline policy growth is frozen pending runtime correctness/adherence evidence. The proposed next stage is `S07-Lab｜Frozen Policy Batch Validation 与 80+ Policy Probing`; it starts from v6b correctness validation, then repeatability/controlled probing only after evidence gates. Any gameplay still needs a separate Main Game Gate.
- For v6b, Skill-body recovery adherence, survival-trend judgment correctness, runtime marker truthfulness, gameplay effectiveness, survival improvement, score benefit, long-horizon adherence, hidden-test transfer and stable 80+ remain NOT_PROVEN.

## AD-003 — Bounded state; no durable Memory

- structured-state-board owns sparse current-session public facts, freshness, and at most two attributable recent effects; unconfirmed facts remain unknown.
- Planning distinguishes observed / inferred / unknown; stale or cross-session information cannot override fresh observe.
- Durable cross-game Memory is NOT_IMPLEMENTED. Any future proposal must establish portability and session isolation before adoption.

## AD-004 — Runtime policy responsibility boundaries

- Board: sparse current-session public facts and freshness; no strategy recommendation.
- rolling-planning: sole strategic owner for one Primary Gap, progress, horizon, and path comparison.
- risk-review: rare review of explicit current-candidate Material Risk; Soft Cost alone does not trigger reconsideration, while a small cost is not assessed in isolation when Planning's public survival trend makes its dimension binding; no survival-trend ownership or action submission.
- v6b static cadence preserves Board/Planning/Risk ownership and all v6 strategy behavior. A CurrentRoundCompressor snapshot starts a recovery epoch; the persistent instruction requires fresh observe, all-three-Skill reread, and Board/Planning rebuild. Final Risk gate closes the decision unless fresh public evidence arrives.
- Free-text CTRL telemetry is retired. Each take_action notes field starts with exactly one canonical CTRL prefix; the Runner tool event is the auditable pairing source. Marker schema has no B/CP/checkpoint fields; checkpoint behavior remains a Planning concern. Multi-selection Energy is serialized as one integer call per action with fresh observe between calls.
- Skills advise; they do not submit actions or create a second review loop.

## AD-005 — Game Gate and architecture changes

- Gameplay effectiveness, stable quantitative 80+, and hidden-test generalization are NOT_PROVEN.
- Each new game is an expensive benchmark and requires separate Main authorization.
- Memory, a fifth Skill, and Team/Swarm remain DEFERRED. Architecture changes require evidence and Main review; use Hypothesis → Experiment → Decision.

## AD-006 — Lean serialized development

- Default workflow is serialized direct development on root main, targeted verification, one meaningful commit, then push.
- Branches require task-specific Main/Planner justification; worktrees require separate explicit justification and are not implied by a branch.
- Verification tiers, evidence reuse, acceptance limits, and artifact policy are defined in AGENTS.md and docs/project/CODEX_PLAN_CONTRACT.md.


## AD-007 — S07 compliance black-box boundary

- S07 is `S07-Lab｜合规黑盒策略探针与稳定高分搜索`.
- Strategy experiments may use only competition-allowed public surfaces: public handbook, fresh public `observe`, legal option text, action receipts, public logs exposed by the normal interface, and committed historical public trajectories.
- Do not read or reconstruct simulator hidden state; do not decode simulator rule/event data for policy optimization; do not build hidden event-consequence tables; do not encode event/title→answer lookup in manifest, instruction, Skill, or supporting runtime.
- Framework/Runner source may be inspected for submission/runtime contracts and allowed interface behavior, but simulator/game-rule internals are not admissible policy evidence.
- S06-09 decoded simulator internals remain forensic history only: `NON_DEPLOYABLE`. They must not justify S07 policy selection unless the same principle is independently supported by allowed public evidence.
- Generic public-state rules (for example, fresh-state recovery, visible survival-trend constraints, bounded reconsideration, observed-progress checks) remain admissible when supported independently by public evidence; exact hidden thresholds/formulas are not.
- Team/Swarm remains deferred. S07 tests policy quality and variance before any architecture expansion.
- `NEXT_GAME = NOT_AUTHORIZED`; S07 does not begin with a mandatory live validation run.


## AD-008 — S07-01 quarantine disposition

- S07-01 W1 compliance provenance gate failed narrowly; W2/W3 remain blocked until cleanup.
- Main decision: `SURGICAL_COMPLIANCE_CLEANUP_REQUIRED`.
- Keep `candidate-v6b-runtime-correctness` as immutable parent identity; create a descendant compliance-cleanup candidate rather than silently mutating v6b history.
- Remove or generalize the predefined Risk cue families `integrity/concealment` and `material reliability incident`; future Risk escalation must be driven by fresh participant-visible public consequence/warning evidence, not historical forensic pattern libraries.
- Replace the ordinary-story exact `top-two` comparison cap with a generic bounded comparison rule; no magic candidate count is deployable without independent allowed evidence.
- Do not change public survival guard, Primary Gap/Progress/STALLED, observed-effect adaptation, review/promotion reset, candidate-first Risk, bounded RECONSIDER, v6b runtime-correctness contracts, Single-Agent authority, or three-Skill ownership unless the cleanup finds a direct textual contradiction.
- Deployable candidate metadata must not treat `STRATEGY_EVIDENCE.md` forensic internals as strategy support. Preserve the document only as quarantined forensic history.
- This is compliance cleanup only: no provider, CareerSim service, MCP live operation, new game, gameplay, Team/Swarm, durable Memory, fifth Skill, or strategy redesign.
- `NEXT_GAME = NOT_AUTHORIZED`.
