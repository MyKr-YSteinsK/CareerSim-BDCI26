# ARCHITECTURE_DECISIONS

> 只记录当前有效决定；已结束阶段的证据与旧决策过程由 Git 历史保存。

## AD-001 — Single Agent + Three Skills

- 保持 Single Agent + Multiple Skills；Single Agent 是唯一 take_action submitter。
- Current Skills: risk-review, structured-state-board, rolling-planning。
- 不因职责分工本身增加 agent、action writer 或常驻 orchestration loop。

## AD-002 — Evidence-driven runtime policy candidate

- Current static candidate is candidate-v6-auditable-control-loop; S06-19 identity repair was statically accepted, and S06-20 final Skill-loading/control-kernel hardening is pending Main re-review; parent = candidate-v5-evidence-driven-phase-policy; strategy delta = AUDITABLE_CANDIDATE_FIRST_CONTROL_LOOP.
- Candidate identity and exact submission instruction are in configs/current_candidate.json and configs/runtime_manifest.json.
- v6 statically defines candidate-first Risk ordering, fresh-state refresh after state-changing actions, a review reset, strict two-checkpoint STALLED, bounded RECONSIDER enforcement, and a compact per-action CTRL marker. It retains the public-state Survival Guard and pre-review reserve check. This is not evidence of runtime adherence or benefit.
- The bounded v6 Design Freeze was reopened for S06-20 and now awaits Main re-acceptance. Further offline policy growth waits for runtime correctness/adherence evidence; any gameplay still needs a separate Main Game Gate.
- Gameplay effectiveness, survival improvement, score benefit, long-horizon adherence, hidden-test transfer and stable 80+ remain NOT_PROVEN.

## AD-003 — Bounded state; no durable Memory

- structured-state-board owns sparse current-session public facts, freshness, and at most two attributable recent effects; unconfirmed facts remain unknown.
- Planning distinguishes observed / inferred / unknown; stale or cross-session information cannot override fresh observe.
- Durable cross-game Memory is NOT_IMPLEMENTED. Any future proposal must establish portability and session isolation before adoption.

## AD-004 — Runtime policy responsibility boundaries

- Board: sparse current-session public facts and freshness; no strategy recommendation.
- rolling-planning: sole strategic owner for one Primary Gap, progress, horizon, and path comparison.
- risk-review: rare review of explicit current-candidate Material Risk; Soft Cost alone does not trigger reconsideration; no action submission.
- v6 static cadence: Board scans fresh public facts; Planning scans every decision and coalesces defined checkpoint triggers; Risk gates an actual candidate after generation and runs FULL_REVIEW only for candidate-related material evidence. State-changing actions require fresh state before the next decision. This cadence and CTRL marker are not yet runtime-validated.
- Action-note trace telemetry is retired; notes retain only a brief reason relevant to the selected action.
- Skills advise; they do not submit actions or create a second review loop.

## AD-005 — Game Gate and architecture changes

- Gameplay effectiveness, stable quantitative 80+, and hidden-test generalization are NOT_PROVEN.
- Each new game is an expensive benchmark and requires separate Main authorization.
- Memory, a fifth Skill, and Team/Swarm remain DEFERRED. Architecture changes require evidence and Main review; use Hypothesis → Experiment → Decision.

## AD-006 — Lean serialized development

- Default workflow is serialized direct development on root main, targeted verification, one meaningful commit, then push.
- Branches require task-specific Main/Planner justification; worktrees require separate explicit justification and are not implied by a branch.
- Verification tiers, evidence reuse, acceptance limits, and artifact policy are defined in AGENTS.md and docs/project/CODEX_PLAN_CONTRACT.md.
