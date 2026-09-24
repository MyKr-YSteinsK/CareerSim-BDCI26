# ARCHITECTURE_DECISIONS

> 只记录当前有效决定；已结束阶段的证据与旧决策过程由 Git 历史保存。

## AD-001 — Single Agent + Four Skills

- 保持 Single Agent + Multiple Skills；Single Agent 是唯一 take_action submitter。
- Current Skills: career-action-trace, risk-review, structured-state-board, rolling-planning。
- 不因职责分工本身增加 agent、action writer 或常驻 orchestration loop。

## AD-002 — Accepted offline candidate

- Current candidate is candidate-v3c-zh-aligned-policy; Main accepted the Chinese-primary language refactor.
- v3c is a language-only successor to candidate-v3b-final-policy; strategy delta = NONE.
- Candidate identity and exact submission instruction are in configs/current_candidate.json and configs/runtime_manifest.json.
- Static/offline acceptance is not gameplay validation; score benefit and stable 80+ remain NOT_PROVEN.

## AD-003 — Bounded state; no durable Memory

- structured-state-board owns current-session public facts, freshness, and at most two attributable recent effects.
- Preserve observed / inferred / unknown distinctions; stale or cross-session state cannot override fresh observe.
- Durable cross-game Memory is NOT_IMPLEMENTED. Any future proposal must establish portability and session isolation before adoption.

## AD-004 — Skill responsibility boundaries

- Board: facts, freshness, and bounded recent effects; no strategy recommendation.
- rolling-planning: one Primary Gap, progress, horizon, and strategic path comparison.
- risk-review: event-triggered review of the current candidate, separating Material Risk from Soft Cost; no action submission.
- career-action-trace: required trace markers and action-note contract; no independent strategy authority.
- Skills advise; they do not submit actions or create a second review loop.

## AD-005 — Game Gate and architecture changes

- Gameplay effectiveness, stable quantitative 80+, and hidden-test generalization are NOT_PROVEN.
- Each new game is an expensive benchmark and requires separate Main authorization.
- Memory, a fifth Skill, and Team/Swarm remain DEFERRED. Architecture changes require evidence and Main review; use Hypothesis → Experiment → Decision.

## AD-006 — Lean serialized development

- Default workflow is serialized direct development on root main, targeted verification, one meaningful commit, then push.
- Branches require task-specific Main/Planner justification; worktrees require separate explicit justification and are not implied by a branch.
- Verification tiers, evidence reuse, acceptance limits, and artifact policy are defined in AGENTS.md and docs/project/CODEX_PLAN_CONTRACT.md.
