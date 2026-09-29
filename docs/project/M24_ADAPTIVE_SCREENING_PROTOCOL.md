# M24 Adaptive Screening Protocol

> S07-49 development-stage proposal. This protocol is **not adopted for live use**. It does not authorize a game, Candidate validation, service/provider use, or early stop.

## Status and purpose

- Protocol decision: `M24_GATE_NEEDS_MORE_EVIDENCE`.
- Checkpoint assessment: `M24_NOT_PROVEN_BUT_REASONABLE`.
- Safe-stop engineering decision: `SAFE_STOP_NOT_IMPLEMENTABLE_WITH_CURRENT_INTERFACE`.
- `NEXT_GAME = NOT_AUTHORIZED`; S07 remains ACTIVE.
- M24 is a development screening hypothesis, not a replacement for a 48-month run. A censored run is not a failure, a natural terminal, or a final-score observation.

The protocol asks whether the same live session is worth continuing from M24 to its natural terminal. It never estimates final score. A stop can only be used after a separate Main Game Gate authorizes the run and a safe stop has been independently made available and validated.

## Evidence firewall and checkpoint semantics

The gate may use only information visible to the participant by the checkpoint:

- month, Level, duration in Level, Health, Dignity, Skill, Network, Output, Wealth and Energy;
- formal review grade, promotion/no-advance, participant-visible feedback and current public warnings;
- current-session public Delivery evidence, allowed CTRL/DL audit, action history, quarterly Main/Energy choices and runtime adherence evidence already observed.

It must not use HiddenRisk, internal scores/counters/IDs/thresholds, DB state, hidden mechanics, future M25–M48 information, or a final score. Historical final outcomes are revealed only after a replay decision as retrospective labels.

The intended checkpoint is the latest fresh participant-visible M24 state **after the M24 formal review and its public result have been recorded**. A string containing `Month=24` alone is insufficient. The evidence must establish one fresh session, a latest M24 public state, the review result, and the action/observe ordering. If review completion cannot be established, the checkpoint is incomplete; do not infer it from a month marker. Any later clear public stop point records its actual stop month separately from `checkpoint_month=24`.

Historical reports do not expose one uniform PRE_REVIEW / POST_REVIEW / END_OF_MONTH flag. Therefore the table below labels exact M24 review ordering only where the report or accepted public trajectory establishes it; otherwise timing relative to the review is `UNKNOWN`. Missing state values and unresolved-warning status remain `UNKNOWN`.

## Historical M24 reconstruction

The reconstruction uses accepted repository run reports, Git-versioned v1 derived trajectories, and the exact named local public-trajectory artifacts whose byte counts/SHA-256 are recorded by their reports. No DB was read. A last public state at `current_month=24` is used; the final score/outcome is kept in a separate retrospective column. For the v1 runs, raw events are unavailable and sparse derived milestones are not interpolated.

Public state tuple: `Level / duration_in_level / Health / Dignity / Skill / Network / Output / Wealth / Energy`. `?` means `UNKNOWN`. Review and warning fields are not reconstructed from later months.

| Run (session) | Latest M24 public state | M24 review / promotion through M24 | Public warning and runtime status known by M24 | Later outcome (retrospective only) |
|---|---|---|---|---|
| v1 #1 (`2224f5df228544e699b10f897d333d4b`) | `L4 / ? / 8 / 10 / 63 / 36 / 26 / 10 / 0` | No M24 promotion; exact review grade/feedback unknown. Promotions M6/M12/M18 then M36/M48. | Current unresolved warning `UNKNOWN`; legacy Skill/runtime status not comparable to current contract. | 48m A; 76.04. |
| v1 #2 (`7df157117cf14917bdc42d83fb7ac7d2`) | `L4 / ? / 10 / 10 / 43 / 19 / 13 / 9 / 0` | L3→L4 promotion at M24; exact grade/feedback unknown. | M24 unresolved public warning `UNKNOWN`; do not backfill the later crisis. Runtime status not comparable. | M25 second trust-crisis termination; 25m D, 35.31. |
| S06 v6 #1 (`7b59b85ad19b4597927cf50fc716f9ac`) | `L4 / ? / 8 / 10 / 61 / 30 / 26 / 11 / 0` | No promotion at M24; exact M24 review grade/feedback unknown. | Public-field / numeric-risk discipline failure was recorded by M18; other M24 Skill criteria are not uniformly available. | 48m A; 75.29. |
| S07 v7g #1 (`d4464a311c924e73b9e23eebd6f71f6d`) | `L3 / ? / 8 / 10 / 41 / 19 / 16 / 7 / 0` | M24 B, no advance; feedback again requested clearer results. | A compression/recovery contract failure was observable after the first M18 compression; current unresolved warning beyond the review feedback is `UNKNOWN`. | 48m C; 54.52. |
| S07 v7i replacement #1 (`cec080dd3c1d43a0b9cb92945e9a824e`) | `L3 / 13 / 9 / 10 / 42 / 21 / 12 / 10 / 0` | M24 B, no advance; clearer-result feedback. | Full-run recovery failure is known; its M24 cutoff is not recoverable here. Other M24 runtime status `UNKNOWN`. | 48m B; 64.0 (fresh final observe accepted in S07-40). |
| S07-14 (`63497628f19448db929ad9c2b6e04a56`) | `L4 / 1 / 9 / 10 / 48 / 15 / 12 / 6 / 0` | L3→L4 promotion at M24; exact grade/feedback unknown. | Warning status `UNKNOWN`; this direct public-agent run has no comparable four-Skill audit. | 48m B; 65.16. |
| S07-15 R2 (`7df2ba5cb1f14898a88ddc6432ad2ce6`) | `L3 / 7 / 7 / 10 / 34 / 16 / 6 / 6 / 0` | No M24 promotion; exact review result unknown. Promotions M12/M18/M36. | Warning status `UNKNOWN`; no comparable four-Skill audit. | 48m C; 54.85. |
| S07-15 R4 (`66f29c11486945dda952215850b80d41`) | `L3 / 7 / 9 / 10 / 35 / 17 / 14 / 6 / 0` | No M24 promotion; public feedback asked for clearer results. | That feedback is a current public review concern; other unresolved-warning status unknown. No comparable four-Skill audit. | 48m C; 57.90. |
| S07-17 R1 (`f7a48e8136854d3ba581d53706f546f3`) | `L1 / ? / 6 / 5 / 8 / 2 / 3 / 7 / ?` | M24 D review and termination; no promotion. | Terminal review is the public concern; energy/runtime Skill audit not comparable. | Natural terminal at M24; 24m E, 21.36. |
| S07-17 R2 (`136c31073ab74eb387126c5c8f1138b6`) | `L1 / ? / 9 / 5 / 9 / 1 / 3 / 4 / ?` | M24 D review and termination; no promotion. | M24 feedback cited collaboration/risk/output concerns; terminal. No comparable four-Skill audit. | Natural terminal at M24; 24m E, 22.82. |
| S07-17 R3 (`66314beadade472ebd0242ded24f2075`) | `L3 / 7 / 10 / 10 / 42 / 18 / 16 / 6 / 0` | M24 B, no advance; “busy, not winning” / same-standard feedback. | The review request is public; no comparable current four-Skill audit. | 48m B; 63.88. |
| S07-19 (`638c45c96e1c45838ba2ee52fd20f759`) | `L1 / ? / 10 / 7 / 9 / 1 / 3 / 7 / ?` | Public terminal at M24; grade E. | Natural terminal; no prospective stop choice. Energy unavailable in the compact checkpoint. | Natural terminal at M24; 24m E, 28.89. |
| S07-20 (`e3e175e2b286478fa3266f614f606134`) | `L1 / ? / 5 / 5 / 9 / 2 / 3 / 4 / ?` | Public terminal at M24; grade E. | Natural terminal; M24 text attributes termination to repeated unfavorable reviews. No prospective stop choice. Energy unavailable. | Natural terminal at M24; 24m E, 16.98. |
| S07-21 (`46184830c0864ffba1381f718becbea7`) | `L3 / 7 / 9 / 10 / 37 / 10 / 16 / 6 / 0` | No promotion at M24; exact M24 review result unknown. Promotions M12/M18/M30/M48. | Warning status `UNKNOWN`; the public-agent ledger is only partly contemporaneous and not a comparable four-Skill audit. | 48m C; 59.19. |

**Counts:** 14 accepted M24 snapshots recovered; 10 were still alive/nonterminal and have a later outcome for retrospective Gate replay; 4 had already naturally terminated at M24 and cannot be treated as Gate STOP decisions. The following do not provide an M24 snapshot: S01-03 (M19), SCORE-01 (only a legacy terminal summary, no comparable M24 public state), S06 Run #1 (candidate identity/state path insufficient), v4 #1 (M6), v7d #1 (M15), S07-15 R1 (technical partial before player actions), S07-15 R3 (M12), and S07-46 v7m (M20). They are `M24_NOT_RECOVERABLE` or `M24_NOT_REACHED` as appropriate. No value is interpolated. `SCORE-01` is excluded from the Gate sample because its candidate identity and public checkpoint state are unknown.

## Reference bands

These are descriptive comparison groups, not official grades, pass thresholds, or an aggregate score.

- **HIGH_REFERENCE:** v1 #1 and S06 v6 #1. Both completed 48 months with A / 75+ retrospective outcomes. At M24 they were both L4 with Output 26 and Energy 0, but differed in Skill (63 vs 61), Network (36 vs 30), Wealth (10 vs 11); this is a two-run range, not a required template.
- **MID_REFERENCE:** completed B/C runs with distinct M24 compositions: S07-14 was L4 with Skill 48 / Network 15 / Output 12 / Wealth 6; S07-17 R3 was L3 with 42 / 18 / 16 / 6; v7i was L3 with 42 / 21 / 12 / 10. S07-15 R2/R4, v7g and S07-21 provide further C trajectories. This band is intentionally broad and does not claim equivalent quality.
- **WEAK_REFERENCE / terminal examples:** S07-17 R1/R2 and S07-19/20 were publicly terminated at M24 around L1/Output 3; v1 #2 is the distinct warning that M24 L4 plus an M24 promotion still preceded M25 termination. Terminal examples are not living M24 decisions and do not define numeric thresholds.

Historical outcome labels were used only to form descriptive reference groups and to score a replay after its M24-only decision. No final-score value enters the live Gate.

## M18 versus M24 information value

| Dimension | M18 evidence | Additional M24 evidence | Limit |
|---|---|---|---|
| Promotion separation | The two 75+ references were L4 by M18; v7g and several B/C paths were L3. | A fourth formal-review window and late outcomes become visible; v1 #2 reaches L4 only at M24. | v1 #2 then terminates at M25, so promotion is not a survival guarantee. |
| Skill / Network / Output growth | v1/v6 were already near L4, with M18 `Skill 44/38, Network 19/19, Output 16/17`; v7g was L3 with `26/6/7`; S07-17 R3 was L3 with `25/5/11`. | By M24, v1/v6 were `63/36/26` and `61/30/26`; v7g was `41/19/16`; S07-17 R3 was `42/18/16`. Some separation persists while the mid paths show substantial catch-up. | Unseeded runs and different opportunities; not causal and not a weighted score. |
| Health / Wealth | M18 values vary; no single survival boundary appears. | All 10 replayable cases were alive at M24, including the later M25 v1 #2 termination. | M24 health/wealth cannot guarantee M25–M48 survival. |
| Reviews / public warnings | Three formal windows give useful but incomplete review trend. | Four windows make repeated feedback and M24 promotion/no-advance visible. | Current unresolved warnings are missing or inconsistently captured in several compact reports. |
| Skill adherence / Delivery / cost | Fewer observations and shorter lifecycles. | Usually more action and Delivery lifecycle samples; current Candidate-specific markers can be audited if present. | Compression/recovery may not occur by M24; heterogeneous old runs cannot validate current v7n Skills. Token/cost data are incomplete and cost is not linear in months. |

Checkpoint conclusion: **`M24_NOT_PROVEN_BUT_REASONABLE`**. M24 adds a useful review window and more lifecycle evidence over M18, but the 14 heterogeneous snapshots do not prove that M24 is the optimal gate or that it safely saves a known fraction of cost.

## Provisional decision tree

This tree is a conservative development hypothesis. It is deliberately not a fixed weighted sum.

1. **Runtime integrity first.** If fresh-session identity, transcript binding, checkpoint ordering, or required public audit evidence is invalid, classify `SCREENING_TECHNICAL_STOP`. This is a technical stop, never a censored trajectory stop or a natural failure.
2. **Competitive.** If the trajectory is comparable to at least one HIGH_REFERENCE across multiple public progression dimensions without broad lag, `CONTINUE` to M48.
3. **Mixed but informative.** Continue when there is improving review feedback, a recent promotion, multi-dimensional public growth, a relevant Delivery checkpoint awaiting public verification, an untested Candidate mechanism, or another explicitly high-value unresolved experiment question.
4. **Survival concern.** Mark explicit current public safety, job-continuity, trust, or affordability concerns. This alone does not mean STOP; continue if further same-session evidence tests a material mechanism.
5. **Clearly behind.** `STOP_SCREENING` is eligible only when multiple progression dimensions lag across comparable M18/M24 checkpoints, review/promotion trajectory is flat or worse, no compensating public advantage or improving momentum exists, no high-value question remains, and the run already provides enough relevant adherence evidence. Do not stop simply for failing to beat v1/v6.
6. **Ambiguous.** Default `CONTINUE` (`SCREENING_AMBIGUOUS_CONTINUE`). The priority is avoiding a false stop over maximizing API savings.

No branch may use an event-title answer table, hidden threshold, final-score predictor, or automatic Candidate/Skill mutation.

## Retrospective replay

For each replay below, the decision used only the M24 public snapshot and information explicitly known by that checkpoint. Later result/grade is shown after `→`. All 10 eligible sessions were kept alive at M24; the four M24 terminal runs above are excluded because no prospective Gate choice remained.

| Run | M24-only replay | Retrospective reveal |
|---|---|---|
| v1 #1 | `CONTINUE — COMPETITIVE` | `TRUE_CONTINUE`: 48m A / 76.04. |
| v6 #1 | `CONTINUE — COMPETITIVE` | `TRUE_CONTINUE`: 48m A / 75.29. |
| v1 #2 | `CONTINUE — MIXED_BUT_INFORMATIVE` (M24 promotion; warning status unknown) | `UNNECESSARY_CONTINUE` by outcome-only proxy: M25 termination / D. It is also the key high-value counterexample and exposed that M24 survival/promotion cannot predict M25 survival. |
| v7g #1 | `CONTINUE — MIXED_BUT_INFORMATIVE` (review feedback and public growth; long-horizon Skill evidence) | `UNNECESSARY_CONTINUE` by outcome-only proxy: 48m C / 54.52. |
| v7i replacement #1 | `CONTINUE — MIXED_BUT_INFORMATIVE` (new pre-review mechanism and incomplete long-horizon evidence) | `TRUE_CONTINUE`: 48m B / 64.0. |
| S07-14 | `CONTINUE — COMPETITIVE / MIXED` (M24 promotion to L4; other dimensions differ) | `TRUE_CONTINUE`: 48m B / 65.16. |
| S07-15 R2 | `AMBIGUOUS → CONTINUE` (Skill/Network grew; Output fell; M24 review detail unknown) | `UNNECESSARY_CONTINUE` by outcome-only proxy: 48m C / 54.85. |
| S07-15 R4 | `CONTINUE — MIXED_BUT_INFORMATIVE` (growth with repeated clearer-result request) | `UNNECESSARY_CONTINUE` by outcome-only proxy: 48m C / 57.90. |
| S07-17 R3 | `CONTINUE — MIXED_BUT_INFORMATIVE` (M18 promotion and continued S/N/O growth; M24 B) | `TRUE_CONTINUE`: 48m B / 63.88. |
| S07-21 | `AMBIGUOUS → CONTINUE` (public growth; M24 review detail unknown) | `UNNECESSARY_CONTINUE` by outcome-only proxy: 48m C / 59.19. |

Replay count: `N=10`; no `STOP` decisions; `FALSE_STOP=0` (including both HIGH_REFERENCE runs); `TRUE_CONTINUE=5` using a completed A/B outcome as the narrow quality proxy; `UNNECESSARY_CONTINUE=5` using C-or-lower as an outcome-only weak-result proxy. These labels do **not** assert that continued C/D runs had no engineering information value. Confidence is very low: samples are small, unpaired, selected historically, and the stop branch was never exercised. The replay demonstrates conservative high-reference protection, not API savings or predictive accuracy.

### v1 #2 counterexample

The accepted M24 public milestone shows L4 and a promotion from L3 to L4, Health 10, Dignity 10, Wealth 9, and Skill/Network/Output 43/19/13. The exact M24 review grade and unresolved warning state are `UNKNOWN` in the sparse derived evidence. The second trust-crisis occurs at M25. Do not import that future event into the M24 decision. Its correct lesson is limited: **being alive and promoted at M24 cannot guarantee survival after M24**. No M24 warning is invented to make the Gate appear successful.

## Skill-audit value at M24

M24 can usually provide enough repeated ordinary decisions to screen Board freshness, Planning continuity/MODE, decision closure, Delivery lifecycle, Risk labels, evidence discipline, quarter intent, and action/CTRL adherence **when those exact Candidate contracts and contemporaneous artifacts are present**. It does not make absence of an observed failure a PASS. Several older public-agent runs do not share current four-Skill instrumentation, and a compression/recovery cycle may not happen by M24. Recovery must be `NOT_EXERCISED` until compression occurs and its post-compression evidence is observed. Overall M24 is **`M24_PARTIAL_ONLY`** for complete Skill audit; it cannot guarantee recovery coverage or v7n validation.

## Cost accounting schema

Record future runs with the following fields. Missing telemetry is `UNKNOWN`, never zero. Reported provider cost is retained only when the provider exposes a reliable value; do not infer price from token counts.

```json
{
  "run_id": "...",
  "game_session_id": "...",
  "months_executed": "UNKNOWN",
  "successful_actions": "UNKNOWN",
  "input_tokens": "UNKNOWN",
  "output_tokens": "UNKNOWN",
  "total_tokens": "UNKNOWN",
  "compression_count": "UNKNOWN",
  "wall_clock_seconds": "UNKNOWN",
  "api_cost": "UNKNOWN",
  "api_cost_source": "UNKNOWN",
  "screening_decision": "UNKNOWN",
  "continued_to_M48": "UNKNOWN",
  "marginal_M25_M48_tokens": "UNKNOWN",
  "marginal_M25_M48_cost": "UNKNOWN"
}
```

No historical cost-saving percentage is supported. Months are not a cost proxy because context growth and compression can make later months more expensive.

## Safe-stop seam and classification

The frozen `career_sim_runner/ws_client.py` `drive()` path reads until normal game end, finalizes the collector on the ordinary path, and sets a nonzero exit when the game has not naturally ended. External task cancellation/disconnect does not establish collector finalization, graceful same-session continuation, or a distinct screening result. `headless_play.py` builds a score report after `drive()` and is not a censored-stop path; it may use the frozen scoring/database route. S07-18's last verified participant-facing tool list contains no public abandon/close/end-session operation. The repository therefore has no proven development-only seam to pause at M24, close cleanly, preserve the same-session evidence, and continue or censor without changing frozen Runner/runtime behavior.

Decision: **`SAFE_STOP_NOT_IMPLEMENTABLE_WITH_CURRENT_INTERFACE`**. No wrapper or cancellation hack is added. In particular, do not kill the process, close the socket to manufacture `ConnectionClosedError`, fabricate `failed=true`, or turn a Runner nonzero exit into a censored stop. A future authorized implementation would need a separately reviewed wrapper outside the frozen Runner, prove same-session continuation for CONTINUE and normal client/collector shutdown for STOP, and pass the Safe-Stop Acceptance checks before live use. No Runner source, simulator, Candidate, Skills, or manifest was changed here; the Runner source tree is unchanged from the verified base.

Before any future one-game live validation, Main must receive offline evidence that: (1) frozen Runner source identity is unchanged; (2) the wrapper does not mutate simulator state or access shared DB; (3) tests make no provider/live-game calls; (4) screening stop is distinct from technical failure and natural terminal; (5) partial audit retains the same-session state, reviews, actions, CTRL/DL and score `UNKNOWN`; (6) CONTINUE keeps the same game session and does not change ordinary Runner behavior; (7) wrapper/tooling is excluded from the final submission package; and (8) repeated invocation cannot stop an unrelated process or service. No live validation is authorized by S07-49.

The offline audit accepts an explicit `SCREENING_STOP_CENSORED` metadata file only when it matches the unique fresh session, transcript, M24 public observation and review checkpoint; the last public observe is alive/nonterminal; the Runner exits 0; no terminal score is present; and the metadata records `continued_to_m48=false`. Its reason is the bounded public-only code `CLEARLY_BEHIND_NO_MATERIAL_COUNTERSIGNAL`, not free text. The result preserves the actual Runner exit, sets score to `UNKNOWN`, natural terminal to false, and keeps CTRL/DL/trajectory audits. It also records that metadata does not prove the runtime stop itself or independently audit whether the Gate justification is sound. This is schema/tooling support only, not live safe-stop readiness.

Development classifications:

- `SCREENING_CONTINUE`: Gate continues the same session.
- `SCREENING_AMBIGUOUS_CONTINUE`: evidence ambiguous; continue the same session.
- `SCREENING_STOP_CENSORED`: authorized, verified screening stop; no final score observation.
- `SCREENING_TECHNICAL_STOP`: integrity/runtime failure; not a trajectory stop.

None of these classifications changes Candidate validation flags or final performance claims.

## Limitations and future validation

- Only two HIGH_REFERENCE trajectories are available; all replayed living runs were continued, so false-stop protection has not been exercised by an actual stop.
- Historical public warnings, timing, skill contracts, and cost telemetry are incomplete and inconsistent. Older Codex-as-Player sessions are not substitutes for installed-Candidate runs.
- M24 review labels or growth do not assure M25–M48 survival, score, long-horizon adherence, repeatability, or hidden-test transfer.
- No live run, service/provider/Runner action, shared DB read, Skill install/reload, Candidate strategy change, or frozen Runner/JiuwenSwarm change occurred in S07-49.
- Before adoption, Main needs a validated safe stop, a separately authorized same-session gate trial, and additional prospective evidence that includes at least one legitimate stop case while preserving all known strong references.
