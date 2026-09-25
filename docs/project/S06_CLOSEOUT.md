# S06 Closeout｜Main Handoff

## Stage result summary

- Stage: `S06`
- Engineering status: `MAIN_ACCEPTED_CLOSEOUT`
- Current candidate: `candidate-v6b-runtime-correctness`
- Design Freeze: `ACTIVE`
- `NEXT_GAME`: `NOT_AUTHORIZED`
- Main acceptance: `PASS_WITH_KNOWN_RUNTIME_LIMITATION`; `S06 = COMPLETE`.

## Final architecture and retained contracts

```text
Single Agent
├── persistent instruction
├── structured-state-board
├── rolling-planning
└── risk-review
```

- Board: fresh current-session public facts, freshness, attributable effects.
- Planning: sole strategy owner for one public Primary Gap, Progress, Risk Budget, and public horizon.
- Risk: candidate-specific Material Risk gate.
- Single Agent: only `take_action` submitter.
- Durable/cross-game Memory: `NOT_IMPLEMENTED`; fifth Skill: `DEFERRED`; Team/Swarm: `DEFERRED`.

Retained strategy contracts: one public Primary Gap; public survival-trend → candidate-independent Risk Budget; candidate-first Risk gate; bounded `RECONSIDER`; fresh observe after successful state change; observed effect over advertised effect; strict two-comparable-checkpoint `STALLED`; formal review/feedback/promotion reset; joint Energy + Main planning; public horizon awareness; safety as a constraint, not the default objective.

S06-25 added runtime/audit contracts without a gameplay strategy redesign: one canonical CTRL prefix at the beginning of `take_action.notes`; `DECISION_CLOSED` after the final Risk gate absent new evidence; Energy multi-selection as one integer call at a time; and CurrentRoundCompressor snapshots as recovery epochs requiring fresh observe, rereading all three Skills, and rebuilding Board/Planning. These contracts have not been runtime-validated on v6b.

## Proven and observed evidence

**Original v6 static evidence:** Main final static acceptance = `PASS`; Design Freeze = `ACTIVE`.

**Original v6 S06-24 run:** candidate `candidate-v6-auditable-control-loop`; `VALID_48M_COMPLETION`; runtime correctness `RUNTIME_ADHERENCE_FAIL`.

| Outcome | Value |
|---|---:|
| Quantitative score | 75.29 |
| Competition partial score | 52.70 |
| Survival | 48 months |
| Grade | A |

Final weighted dimensions: Level 18.00; Wealth 9.88; Resilience 12.75; Skill 15.00; Risk 10.00; Network 9.67. Promotions were observed at M6, M12, M18, M36, and M48. Quarterly Main actions were `申请关键项目` 14/16 and `低调避险` 2/16.

**Mechanism observations — `SUPPORTED_IN_TRIGGERED_CASES`, not causal evidence:**

- Fresh-state discipline: no observed violation among the 202 successful state-changing actions.
- Public survival trend / Risk Budget: at M6, Health fell 6→5→4 with a public warning and the run recorded `TIGHT`; after recovery to Health 6 and warning clearance, `AVAILABLE` was later used. Main-reviewed M27 evidence records declining Health, `TIGHT`, and preference for recovery/risk reduction over Health-worsening Growth.
- Candidate-specific Risk and bounded alternative: at M13, Health=4 and a one-week overnight on-call candidate triggered a Health cue and `RECONSIDER`; one directly relevant legal alternative was selected and gated.
- Planning examples included Primary Gap use, observed-effect/saturation adaptation, feedback/promotion resets, and Energy + Main joint consideration. These are single-run triggered observations; cadence and benefit are not established. Repeated `准备汇报材料` after no observed Output increase was recognized as saturation and another Energy action was selected.

No observation here attributes the final score or survival to a particular mechanism.

## Runtime failures and corrected accounting

S06-24 had a missed semiannual H self-marker, repeated ordinary deliberation without fresh evidence, and free-text CTRL/action pairing that could not be certified. Two context-compression epochs occurred without rereading the three Skills. Board scans recurred through the run, so low-frequency-only Board behavior is not supported.

- `take_action` attempts: 203.
- Successful state-changing actions: 202; fresh-state violations among these: 0.
- Malformed rejected attempt: 1, with `choice=6,7,3`; rejected before game-state mutation.

S06-25 introduced v6b to correct these runtime/audit contracts only. It did not modify gameplay strategy or transfer the v6 run result to v6b.

## Context compression and resource use

The previously unresolved 328,103-token usage is identified as two JiuwenSwarm `CurrentRoundCompressor` calls outside the Runner gameplay aggregate:

| Call | Input | Output | Total |
|---|---:|---:|---:|
| #1 | 161,005 | 2,724 | 163,729 |
| #2 | 160,576 | 3,798 | 164,374 |
| Combined | 321,581 | 6,522 | 328,103 |

The responses generated `<coverage_check>` and `<state_snapshot>`. This demonstrates an implicit same-run compressed working context, not durable or cross-game Memory.

S06-24 Runner gameplay usage: 40,372,074 input; 247,309 output; 40,619,383 total; 39,865,088 reported cache tokens; model `deepseek-flash`; actual billed cost `UNKNOWN`. Compression usage is separate. The high cache share means total tokens should not be interpreted as fully uncached input. Resource efficiency remains an optimization target; S06 makes no efficiency claim.

## Variance and evidence boundary

Candidate-v1 Run #1 was 76.04 / 48 months / A; Run #2 was 35.31 / 25 months / D. This is observed variance, not a causal or stable-performance estimate. No claim is made that v6 outperforms v1, v6b outperforms v6, score or survival improved, or stable 80+ was achieved.

The current v6b identity is `STATIC_CORRECTNESS_PATCHED`, parent `candidate-v6-auditable-control-loop`. Its frozen identity is recorded in [current_candidate.json](../../configs/current_candidate.json): runtime manifest SHA-256 `8cbf68fa4c6ae055db9ad74942e37a649bfa13dca73b8924175467a5ee80e351`; instruction SHA-256 `a891fa103f0d4f910c9bbcc5ab91ab8bbbfe4cb242b9506d63374f1cf75d8074`; Skill blobs: risk-review `f9cafecad85cad39d34bfd0266eaea9e88d882cc`, rolling-planning `78a4b578fcb71eef04bc97ec0e3471820fecfe2f`, structured-state-board `b6d371d74f3477f4f6cdeabe8482093a78cbe3e5`.

For v6b, runtime adherence, gameplay effectiveness, provider validation, survival improvement, score improvement, long-horizon adherence, stable 80+, and hidden-test transfer are all `NOT_PROVEN`. The original v6 gameplay result remains attached only to the original v6 identity.

## Main decision and next-stage proposal

**Main decision:** `PASS_WITH_KNOWN_RUNTIME_LIMITATION`. S06 is accepted as COMPLETE. Rationale: S06 has a coherent frozen Single-Agent/3-Skill architecture; original v6 completed a valid 48-month A-grade run with 75.29 and exhibited several intended mechanisms in triggered cases; raw evidence identified runtime correctness defects; v6b statically repairs those contracts without strategy redesign. v6b itself remains unvalidated. Repeating an expensive single run inside S06 would duplicate work proposed for the next experimental stage.

Accepted next-stage direction, not yet started and with no game authorization: `BATCH_EXPLORATION_AND_POLICY_PROBING` — E1 repeated frozen-v6b runs to validate runtime adherence and estimate score/survival variance; E2 controlled one-mechanism-at-a-time ablations, including simple Growth prior + Risk override versus the fuller controller; E3 collect structured event/action trajectories and investigate recurring delayed, saturation, and risk mechanisms, preferring transferable evidence over Dev-specific lookup. All next-stage hypotheses remain hypotheses. No game is authorized by this handoff.

## Evidence references

- [S06-24 v6 Run #1 record](runs/v6-run1-validation.md)
- [Run history](RUN_HISTORY.md)
- [Current candidate identity](../../configs/current_candidate.json)
- [Current state](CURRENT_STATE.md)
