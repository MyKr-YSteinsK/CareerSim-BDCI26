# S08-04 — Execution Persistence Convergence and Pre-Run Integration

## 1. Result

- Status: `COMPLETE` for the bounded offline integration scope.
- Decision: `READY_FOR_MAIN_GAME_GATE`.
- Candidate: `candidate-v7o-execution-persistence-convergence`; static only.
- No provider, service, game, install, or submission activity occurred. `NEXT_GAME=NOT_AUTHORIZED`.

## 2. Identity

- Repository branch: `main`.
- Base: `23b5c52cdcd18aaf3f2613654b0d9d2302343661`, the v7n/S08-03 baseline required by the Plan.
- Parent Candidate: `candidate-v7n-public-state-delivery-constraint-hardening`.
- Strategy delta: `MODE_BINDING_CORRECTNESS_CLARIFICATION_ONLY`.
- Candidate status: `STATIC_IMPLEMENTED_NOT_RUNTIME_VALIDATED`; all runtime, gameplay, provider, survival, score, long-horizon, stable-80+, hidden-transfer, and next-game authorization flags remain false.

## 3. Evidence Basis

- **FACT:** The accepted v7n partial run reached M6 after 23 successful actions, with 20 continuation sends and 21 counted completion boundaries; see [S07-51R replacement validation](../runs/v7n-run1-replacement-validation.md).
- **FACT:** S08-02 attributed 7 of those 21 boundaries to zero-work provider-error terminations and 14 to productive work after recovery; its classification was `MIXED_PROVIDER_AND_EXECUTION_PERSISTENCE`, with medium confidence. This bounds the observed failure pattern but does not prove a single upstream cause; see [S08-02 review](S08-02_PROVIDER_BOUNDARY_ATTRIBUTION_AND_RESILIENCE.md).
- **FACT:** S08-03 set the local `career_emu` retry value to `2` and verified static propagation. Cloud portability and effect on a future game remain unknown; see [S08-03 review](S08-03_LOCAL_RUNTIME_RETRY_CONFIGURATION.md).
- **INFERENCE:** A concise same-execution persistence contract plus the local retry setting is a bounded pre-run response to the mixed boundary evidence. Static checks cannot establish runtime adherence or provider recovery.

## 4. Patch Summary

- Added Candidate v7o and its parent/runtime identity in `configs/current_candidate.json`.
- Reduced and refocused `configs/runtime_manifest.json` on global evidence boundaries, orchestration, same-execution persistence, action preflight, recovery, and architecture.
- Made the narrow Board and Planning clarifications required by the Plan.
- Added deterministic static contract/scenario checks and updated existing Candidate identity assertions. Preserved the S07-50 evaluation snapshot identity.
- Updated `docs/project/CURRENT_STATE.md` and this review. No one-time verifier was retained.

## 5. Whole-Game Persistence Contract

The manifest now requires the same assistant execution to continue while structured game state is active. `DECISION_CLOSED` closes only the current action selection. After every successful action, obtain a fresh observation and start the next decision cycle. Do not voluntarily stop at an action, month, quarter, review, promotion, or local decision boundary. Structured `game.ended` is the natural terminal; transcript wording is not. An unrecoverable runtime/tool failure is the only other completion blocker.

On context recovery, action submission stops at `RECOVERY_PENDING`. Recovery confirms the same session, obtains a fresh observation, rereads all four Skills, rebuilds Board/Delivery/Review Plan from public evidence (marking missing facts `UNKNOWN`), and emits `RECOVERY_READY` only after the steps are confirmed. Ordinary same-context execution reads the four Skills at startup and does not reread them on every loop.

## 6. Manifest Before/After Size

- v7n instruction: 8,372 characters.
- v7o instruction: 4,273 characters.
- Reduction: 48.96%.
- The result is below the 4,500-character target and exceeds the 35% reduction criterion.

## 7. Semantic Ownership Before/After

- **Before:** The v7n manifest repeated detailed Board copying, MODE selection, result-realization, Delivery lifecycle, Risk labels/reconsideration, and action/recovery procedures already specified by Skills.
- **After:** The manifest owns the global evidence firewall, orchestration, persistence, action preflight/marker presence, recovery, and architecture boundaries. Board owns facts; Planning owns strategy/objectives/ranking; Delivery owns the current-session delivery lifecycle; Risk owns the final candidate risk gate. Detailed Skill procedures remain in their owning Skills.

## 8. Hidden-Field Firewall

The manifest explicitly treats `HiddenRisk`, hidden counters, internal scores, internal identifiers/effects, numeric `status_updates` without verified public status, unclear-public-status fields, and prohibited numeric values as unusable. It forbids inspecting, quoting, comparing, summarizing, remembering, or reasoning from them, including internally, and excludes them from Board, Planning, Delivery, Risk, CTRL, DL, and action rationale. The instruction also states that enforcement is instruction-only and that no deterministic raw-payload filter exists; it does not claim a hard filter.

## 9. MODE=S Clarification

Board keeps an ordinary numeric fluctuation or one-step decline in `STATE`; by itself it does not create a binding `STICKY` warning. Planning states that displayed H/D/W values or one ordinary one-step decrease alone do not establish a binding constraint or justify `MODE=S`. `MODE=S` depends on current public evidence of a material survival, safety, job-continuity, affordability, or income-continuity issue. A clearly depleted resource binds only when public evidence establishes ordinary activity is infeasible. No numeric threshold was added.

## 10. Strategy Preservation

No new strategy mechanism was introduced. v7o includes a narrow evidence-backed MODE/binding-constraint correctness clarification that can affect decisions in numeric-only low/declining-state cases.

- New strategy mechanism: `NO`.
- Behavior-relevant correctness/policy delta: `YES`, narrow and evidence-backed.
- Execution persistence delta: `YES`.

A future v7o run therefore cannot be interpreted as a pure execution-persistence delta. Promotion-first with Survival Floor, default `MODE=A`, temporary stabilization, review-feedback anchoring, the pre-first-review result-realization prior, quarterly Energy intent, one-observation/one-Planning-pass discipline, Risk closure, and action preflight remain represented in their owning files. No fixed action sequence or hidden threshold was added.

## 11. Delivery/Risk Identity

Both Skills are byte-identical to the S08-04 base and their recorded Git blobs remain unchanged:

- `delivery-progress`: `ed06db1d1ffafbdca15dbf6eca75df91bdbb6ee2` before and after.
- `risk-review`: `02df0a1f2ac47c6f60df0d931625f50afb3dce93` before and after.

The frozen Runner identity remains `f61c738c72e51b77298cc1c14c7c6ebf4b6c527d`. No dependency or `uv.lock` change was made.

## 12. Static Scenario Results

All five Plan scenarios pass as deterministic text/contract checks; they are not LLM behavior or runtime tests.

1. Ordinary workload, mild fatigue, non-urgent work, and a routine numeric fluctuation do not force `MODE=S` or prescribe an exact action.
2. An explicit unresolved acute symptom can require `MODE=S`; a direct affordability/income-continuity crisis may also bind.
3. A synthetic public-state payload with numeric `HiddenRisk` is covered by the unusable-input rule; no rationale may use the value, and no hard-filter guarantee is claimed.
4. After a successful action and fresh nonterminal observation, the same execution starts another decision cycle.
5. A formal review/promotion is not terminal; Board/Planning update from fresh evidence and the game loop continues.

## 13. Local Retry Guard

A read-only allowlisted parse of `C:\Users\Yukis\.jiuwenswarm-instances\career_emu\config\config.yaml` confirmed `models.defaults[0].model_client_config.max_retries` is the integer `2`. No other config value was printed or changed. No service was started.

## 14. Validation

- Root interpreter targeted suite: 30 passed. This includes Candidate identity/contract tests, package construction and static submission-contract validation, the five Plan scenarios, unchanged Delivery/Risk and Runner checks, and one local S07-50 snapshot-boundary test.
- Package validation produced two deterministic temporary bundles, confirmed exactly four Skills and the v7o manifest identity, then passed `validate_submission_contract`; no installation or live validator was used.
- Candidate manifest/instruction hashes and changed Skill blob identities match the current files. Parent identity remains tied to the specified v7n baseline.
- `git diff --check`: passed.
- Local retry guard: passed at `2`.
- No provider calls, network probes, service lifecycle, MCP, install, game, or submission occurred.

## 15. Known Limitations

- Whole-game persistence and evidence handling are prompt-level instructions; the Skill/runtime interface has no deterministic raw-payload filter or execution-continuation hook.
- No v7o runtime/provider/gameplay behavior was observed. Provider errors may persist despite the local retry setting; portability remains unknown.
- Score, survival, 48-month completion, long-horizon adherence, stable 80+, and hidden-test transfer remain unproven. Static readiness is not gameplay authorization.

## 16. Main Game Gate Recommendation

`READY_FOR_MAIN_GAME_GATE`

```text
NO_S08_05_RECOMMENDED
RETURN_TO_MAIN_FOR_ONE_FRESH_V7O_RUN_GATE
```

`NEXT_GAME` remains `NOT_AUTHORIZED` until Main independently decides whether to authorize one fresh v7o run.
