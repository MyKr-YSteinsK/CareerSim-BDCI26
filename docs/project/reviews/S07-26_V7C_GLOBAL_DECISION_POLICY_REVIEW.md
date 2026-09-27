# S07-26 Candidate v7c Global Decision Policy Review

## Decision

Candidate v7c statically implements the S07-26 policy and progressive-disclosure changes. The review outcome is `V7C_GLOBAL_DECISION_POLICY_STATIC_PASS` after the recorded targeted checks. It does not establish runtime adherence or gameplay benefit.

Base: `d10f354f5338e7950bd49efeba7b9d524e82f23a`
Candidate: `candidate-v7c-global-decision-policy`
Parent: `candidate-v7b-semantic-generalization`
Status: `STATIC_IMPLEMENTED_NOT_RUNTIME_VALIDATED`

## Five-gap closure and evidence

1. **Public Level tenure.** Board accepts a fresh participant-visible `CurrentLevelDuration` field or the Plan alias `duration_in_level`. The [official public handbook](https://career-emulator.readthedocs.io/handbook.html) names the field `CurrentLevelDuration` and describes it as months at the current level. The runtime alias mapping was not checked in a live observation. Missing or conflicting fields remain `UNKNOWN`; tenure is context only and does not map to a threshold, probability, or fixed Level target.
2. **Time-to-realization.** Planning compares public checkpoint, delivery stage, review horizon, remaining career horizon, and explicit legal-option timing. `CURRENT_REVIEW_WINDOW`, `LATER_WINDOW`, `BEYOND_VISIBLE_HORIZON`, and `UNKNOWN` are temporary qualitative labels in Path Trade-off, not persisted state.
3. **Commitment congestion.** Planning qualitatively considers open commitments, blockers, dependencies, next checkpoint, review relevance, public resource load, and remaining horizon. `LIGHT`, `MEANINGFUL`, `CONGESTED`, and `UNKNOWN` are not count-based thresholds, durable telemetry, or Delivery lifecycle state. Close-before-open applies when a high-value commitment is near verifiable realization and no better or more timely opportunity is evidenced; explicit exceptions remain for blocked work, stronger bottleneck fit, low marginal value, time-sensitive opportunities, and sufficient remaining horizon.
4. **Late-horizon realization.** Longer, intermediate, and shorter remaining horizons have symmetric qualitative guidance. A short horizon raises paths that can realize delivery, evidence, recognition, progression, or resources in time, while preserving terminal option value. No fixed month or phase is encoded.
5. **Hierarchy and prompt deduplication.** Planning uses this order: fresh facts and legality; binding constraints; Promotion Frontier and one Primary Gap; review-window realization; global compounding and actual remaining horizon; commitment efficiency and time-to-realization; near-tie Story semantic priors; candidate-specific Risk gate and `DECISION_CLOSED`.

## Decision dominance

- A binding public survival or compliance constraint governs affected candidates first.
- A clearly evidenced progression bottleneck with a realizable result before the next review window gets priority in the comparison.
- Without candidate-specific Material Risk, a clearly higher public Growth value remains preferable to a near-tie semantic or reversibility prior.
- A high-value commitment near a verifiable result gets close-before-open priority when no stronger or more timely public opportunity is evidenced. Blocked work, a better bottleneck fit, low old-item marginal value, a time-sensitive new opportunity, or enough remaining horizon can justify opening the new path.

## Prompt size and disclosure

Counts are Unicode characters and UTF-8 bytes of the manifest instruction and each Skill text. They measure literal text size, not model tokens or token savings.

| Persistent component | Before chars / bytes | After chars / bytes | Change chars / bytes |
|---|---:|---:|---:|
| Manifest instruction | 4,444 / 6,108 | 1,830 / 2,420 | -2,614 / -3,688 |
| Board Skill | 2,036 / 3,390 | 2,271 / 3,793 | +235 / +403 |
| Planning Skill | 10,632 / 16,366 | 7,299 / 11,473 | -3,333 / -4,893 |
| Delivery Skill | 2,547 / 4,221 | 2,547 / 4,221 | 0 / 0 |
| Risk Skill | 2,716 / 4,564 | 2,716 / 4,564 | 0 / 0 |
| Total instruction and four Skills | 22,375 / 34,649 | 16,663 / 26,471 | -5,712 / -8,178 |

The manifest no longer repeats the detailed objective, Promotion Frontier and Primary Gap reasoning, affordability cases, horizon guidance, and Story semantic clauses now owned by Planning. It retains the public-evidence kernel, four-Skill/action ownership, controller order, global priority summary, control-marker and bounded-RECONSIDER rules, one-integer Energy calls, fresh-observe requirement, decision closure, recovery, and anti-overfit kernel. Board grew only to record provenance and unknown handling for the public tenure field.

## Ownership, preserved mechanisms, and boundaries

- Board remains the public-fact owner; Planning remains the sole strategy owner; Delivery retains its bounded current-session lifecycle; Risk retains the candidate-specific Material Risk gate; Single Agent remains the sole action submitter.
- The Risk Skill and Delivery Skill are byte-for-byte unchanged. Existing v7b Story priors and v7a Promotion Frontier, bottleneck, marginal-value, early-horizon, and affordability mechanisms remain in the Candidate metadata and Planning policy.
- Memory remains `NOT_IMPLEMENTED`; Team/Swarm and a fifth Skill remain `DEFERRED`. Memory's document-only reopen gate requires repeated real-run compression losses that public session evidence cannot recover and that harm objectives. Team's requires repeated real role-conflict evidence plus a minimal isolatable experiment with role separation, common state authority, and one action submitter.
- No fixed tenure threshold, promotion month, horizon phase, commitment count, event lookup, hidden score/risk threshold, fixed action ratio, Energy bundle, or cross-game memory was added. Runner, dependencies, lockfiles, provider configuration, runtime state, and historical raw evidence were untouched.

## Verification and unresolved facts

Targeted static verification: recorded in TASK_RESULT. Gameplay/provider calls and runtime validation: 0. Score, survival improvement, runtime adherence, stable 80+, and hidden-test transfer remain `NOT_PROVEN`. The official handbook field name is public, but the runtime-observed key and any v7c behavioral effect remain `UNKNOWN` pending separately authorized validation. S07 remains ACTIVE and `NEXT_GAME = NOT_AUTHORIZED`; the next recommendation is S07-27 Runtime Readiness Gate.
