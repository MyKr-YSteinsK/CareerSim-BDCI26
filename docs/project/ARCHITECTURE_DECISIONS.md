# ARCHITECTURE_DECISIONS

> 只记录当前有效决定；已结束阶段的证据与旧决策过程由 Git 历史保存。

## AD-001 — Single Agent + Four Skills

- 保持 Single Agent + Multiple Skills；Single Agent 是唯一 take_action submitter。
- Current Skills: structured-state-board, rolling-planning, delivery-progress, risk-review。
- 不因职责分工本身增加 agent、action writer 或常驻 orchestration loop。

## AD-002 — Evidence-driven runtime policy candidate

- Original candidate `candidate-v6-auditable-control-loop` remains Main-accepted static work; its S06-24 single run was `VALID_48M_COMPLETION` (75.29 / 52.70 / A) but `RUNTIME_ADHERENCE_FAIL`.
- Current candidate is `candidate-v7b-semantic-generalization`, parent `candidate-v7a-promotion-frontier`; S07-25 adds bounded event-agnostic Story semantic priors to Planning on top of the S07-24 Promotion Frontier refinement and S07-23 four-Skill design. v7a remains the static parent; v7 remains the immutable four-Skill architecture parent; v6c remains the compliance-cleanup ancestor and v6b the earlier runtime/audit-correctness ancestor. v7b is `STATIC_IMPLEMENTED_NOT_RUNTIME_VALIDATED`; no gameplay/provider/score/hidden-test validation transfers from earlier candidates. S06 Main acceptance=`PASS_WITH_KNOWN_RUNTIME_LIMITATION` and S06=`COMPLETE`; NEXT_GAME = NOT_AUTHORIZED; Design Freeze = ACTIVE.
- Candidate identity and exact submission instruction are in configs/current_candidate.json and configs/runtime_manifest.json.
- Main-accepted strategy contracts remain context recovery, candidate-first Risk ordering, fresh-state refresh, one Primary Gap and public survival-trend Risk Budget, review/promotion reset, observed > advertised, strict two-checkpoint STALLED, bounded RECONSIDER, joint Energy + Main planning, and bounded ordinary-story comparison without an exact top-two cap. v6b added a canonical notes-prefix audit surface, decision-closed handoff, one-integer Energy calls, and explicit compression recovery; v6c preserves these contracts. Static contracts are not evidence of v6c runtime adherence or benefit.
- S07-23 is the authorized static policy evolution after the S07-22 review. Further strategy/architecture changes require Main review; gameplay still needs a separate Main Game Gate. W2/W3 remain separate, unstarted work and are not implied by this implementation.
- For v6c, Skill-body recovery adherence, survival-trend judgment correctness, runtime marker truthfulness, gameplay effectiveness, survival improvement, score benefit, long-horizon adherence, hidden-test transfer and stable 80+ remain NOT_PROVEN.

## AD-003 — Bounded state; no durable Memory

- structured-state-board owns sparse current-session public facts, freshness, and at most two attributable recent effects; unconfirmed facts remain unknown.
- Planning distinguishes observed / inferred / unknown; stale or cross-session information cannot override fresh observe.
- delivery-progress is the sole owner of a bounded current-session public delivery lifecycle; it does not own Board facts, strategy, risk, or actions. Planning reads its compact summary without rewriting it.
- Durable cross-game Memory is NOT_IMPLEMENTED. Any future proposal must establish portability and session isolation before adoption.

## AD-004 — Runtime policy responsibility boundaries

- Board: sparse current-session public facts and freshness; no strategy recommendation or derived delivery lifecycle.
- rolling-planning: sole strategic owner for remaining-career objective, review/action horizons, qualitative Promotion Frontier / Progression Readiness, one evidence-based Primary Gap, cross-dimension bottleneck and marginal-value comparison, Progress, Risk Budget, review reset, and path comparison.
- delivery-progress: up to three relevant active lifecycle summaries and one recent review-linked closed evidence; updates only on relevant public evidence, never submits actions.
- risk-review: rare review of explicit current-candidate Material Risk; Soft Cost alone does not trigger reconsideration, while a small cost is not assessed in isolation when Planning's public survival trend makes its dimension binding; no survival-trend ownership or action submission.
- v6b/v6c runtime contracts remain in force. A CurrentRoundCompressor snapshot starts a recovery epoch; the v7 persistent instruction requires fresh observe, all-four-Skill reread, and Board/Delivery/Planning rebuild from current-session public evidence. Final Risk gate closes the decision unless fresh public evidence arrives.
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
- S07-23 implements the Main-accepted static four-Skill architecture. This does not establish policy improvement or authorize further expansion; Team/Swarm remains deferred.
- `NEXT_GAME = NOT_AUTHORIZED`; S07 does not begin with a mandatory live validation run.


## AD-008 — S07-01 quarantine disposition

- S07-01 W1 compliance provenance gate failed narrowly; S07-02 implemented the bounded cleanup and passed Main review. The identified quarantine is resolved. W2/W3 are unblocked but remain NOT_STARTED.
- Main decision: `SURGICAL_COMPLIANCE_CLEANUP_REQUIRED`.
- Keep `candidate-v6b-runtime-correctness` as immutable parent identity; `candidate-v6c-compliance-cleanup` is the descendant static cleanup candidate.
- The two unsupported predefined Risk cue families were removed; Risk escalation is driven by fresh participant-visible public consequence/warning evidence, not historical forensic pattern libraries.
- The ordinary-story exact `top-two` cap was replaced by generic bounded comparison; no magic candidate count is deployable without independent allowed evidence.
- Do not change public survival guard, Primary Gap/Progress/STALLED, observed-effect adaptation, review/promotion reset, candidate-first Risk, bounded RECONSIDER, v6b runtime-correctness contracts, Single-Agent authority, or three-Skill ownership unless the cleanup finds a direct textual contradiction.
- Deployable v6c candidate metadata no longer points to quarantined forensic strategy evidence. Preserve that document only as quarantined forensic history.
- This is compliance cleanup only: no provider, CareerSim service, MCP live operation, new game, gameplay, Team/Swarm, durable Memory, fifth Skill, or strategy redesign.
- `NEXT_GAME = NOT_AUTHORIZED`.

> S07-02 scope note: this decision records the v6c compliance-cleanup contract. Its three-Skill/current-candidate clauses were superseded for the current Candidate by S07-23 / AD-009; v6c and its historical evidence remain preserved as the parent.

## AD-009 — Candidate v7 long-horizon and delivery architecture

- Main accepted the S07-22 design direction for static implementation in S07-23: Single Agent + four Skills, with unchanged frozen Runner/dependencies and no live validation.
- `structured-state-board` owns only fresh current-session public facts/effects; `rolling-planning` is the sole owner of the robust remaining-career objective, review/action horizons, one evidence-based Primary Gap, and review resets; `delivery-progress` owns a bounded current-session evidence lifecycle and updates only on relevant public triggers; `risk-review` remains the candidate-specific Material Risk gate.
- Single Agent remains the only action submitter. Delivery is not a strategy/risk/action owner. Memory remains `NOT_IMPLEMENTED`; fifth Skill and Team/Swarm remain `DEFERRED`.
- `candidate-v7-global-trajectory-delivery` is static-only and `NOT_RUNTIME_VALIDATED`. Gameplay/provider validation, score or survival improvement, long-horizon adherence, stable 80+, and hidden-test transfer remain `NOT_PROVEN`. `NEXT_GAME = NOT_AUTHORIZED`.
- Further policy or architecture changes require Main review and evidence; implement/skill-load/runtime/gameplay effectiveness must be established separately rather than inferred from static identity or design.

> S07-23 scope note: v7 is retained as the immutable four-Skill parent. Its static-only validation boundary remains applicable to v7 and does not transfer gameplay evidence.

## AD-010 — Candidate v7a Promotion Frontier refinement

- S07-24 implements a bounded static refinement: qualitative public-evidence Promotion Frontier, cross-dimension bottleneck / marginal-value awareness, early-horizon progression bias under constraints, and explicit public affordability warnings.
- Promotion Frontier uses current-session public Level, promotion/review feedback, career-capital and Delivery evidence. It does not estimate eligibility, probability, hidden thresholds, or caps. Primary Gap remains one likely public bottleneck, not the lowest metric.
- S07-16 trajectories support only descriptive associations and counterexamples; they do not establish that early promotion or any single dimension causes higher score. The user-provided external threshold/cap claim is `USER_PROVIDED_UNVERIFIED_EXTERNAL_MECHANISM_SIGNAL` and is not encoded in deployable policy.
- `GLOBAL_MARGINAL_VALUE_LOW` is a qualitative candidate-comparison observation, not a persistent enum or telemetry and not a replacement for the existing two-comparable-checkpoint STALLED rule.
- Explicit public debt / inability-to-pay / severe affordability warning, or credible sustained financial deterioration with public consequence, may tighten Planning's Risk Budget without a numeric Wealth cutoff. Ordinary cost or an isolated decrease is insufficient.
- Architecture remains Single Agent + four Skills; Memory=`NOT_IMPLEMENTED`; fifth Skill and Team/Swarm=`DEFERRED`. v7a is static-only and `NOT_RUNTIME_VALIDATED`; `NEXT_GAME = NOT_AUTHORIZED`.

## AD-011 — Candidate v7b event-agnostic Story semantic priors

- S07-25 adds qualitative, context-sensitive evidence-first, accountable-handling, ownership/checkpoint, reversibility, and proportional-escalation priors to ordinary unfamiliar Story candidate comparison. They apply after public facts, Promotion Frontier / Primary Gap / review objective, and legal-candidate generation, before the existing Risk gate.
- The priors are not a fixed ordering, score, mandatory per-action checklist, second strategy owner, or second Risk gate. When progression value is close or outcomes are uncertain, they help distinguish candidates; they do not automatically suppress a clearly higher public Growth path without Material Risk. Direct handling is conditional on the public context; failed handling, authority limits, and compliance/safety or credible retaliation concerns may justify escalation.
- The four-Skill architecture and ownership remain unchanged: Single Agent submits actions, Planning owns strategy, Board owns facts, Delivery owns lifecycle, and Risk owns the candidate-specific Material Risk gate. Memory remains `NOT_IMPLEMENTED`; fifth Skill and Team/Swarm remain `DEFERRED`.
- No event/title/keyword-to-choice lookup, fixed story answer, numeric escalation ladder, hidden threshold, or cross-game memory is encoded. v7b is static-only and `NOT_RUNTIME_VALIDATED`; runtime/provider/gameplay validation, score improvement, and hidden-test transfer remain `NOT_PROVEN`. S07 remains ACTIVE; `NEXT_GAME = NOT_AUTHORIZED`.

## AD-012 — Candidate v7c global decision hierarchy and progressive disclosure

- S07-26 adopts a static hierarchy from fresh public facts and legality through binding constraints, Promotion Frontier / one Primary Gap, review-window realization, global compounding and actual remaining horizon, commitment efficiency / time-to-realization, near-tie Story priors, and the existing candidate-specific Risk gate.
- Board records public Level tenure only when a fresh participant-visible field is present. The official handbook names the field `CurrentLevelDuration`; the Plan alias `duration_in_level` is accepted as an equivalent runtime key only when observed. Missing or conflicting fields remain `UNKNOWN`; tenure is not mapped to a threshold or promotion prediction.
- Planning uses transient qualitative time-to-realization and commitment-load comparisons in Path Trade-off. Review readiness includes both survival and progression realization. Close-before-open and late-horizon realization are conditional comparisons with explicit exceptions; no fixed month, phase, or item-count rule is introduced.
- Prompt deduplication keeps execution, control-marker, Energy, recovery, and anti-overfit invariants in the persistent manifest kernel while detailed strategy remains in its owning Skills. Single Agent and four-Skill ownership are unchanged; Risk is unchanged. Memory remains `NOT_IMPLEMENTED`; Team/Swarm and fifth Skill remain `DEFERRED`. Memory's document-only reopen gate requires repeated real-run compression losses that public session evidence cannot recover and that harm objectives. Team's requires repeated real role-conflict evidence plus a minimal isolatable experiment with role separation, common state authority, and one action submitter.
- v7c is static-only and `NOT_RUNTIME_VALIDATED`. No gameplay, provider, score, survival, long-horizon adherence, or hidden-test claim transfers from v7b or earlier candidates. S07 remains ACTIVE; `NEXT_GAME = NOT_AUTHORIZED`.
