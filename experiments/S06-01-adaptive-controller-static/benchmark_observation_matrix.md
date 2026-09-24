# S06-01 Successor Benchmark Observation Matrix

This is a preregistration for a future Main-authorized Game Gate only. It does not authorize a run. Link to the offline parent: S05-03 [`benchmark_observation_matrix.md`](../S05-03-final-optimization-reserve-audit/benchmark_observation_matrix.md). Candidate under observation: `candidate-v3-adaptive-controller-static`.

For each item record exactly one status: `PASS` (observable behavior matched the written contract), `FAIL` (a directly observed contradiction), `NOT_OBSERVED` (trigger/opportunity did not occur), or `UNKNOWN` (source, freshness, or attribution insufficient). A single stochastic game can describe behavior but cannot establish causal score benefit, stable 80+, or generalization. Never treat a missing trigger as mechanism failure.

| # | Observation | Source and measurement | Single-run limitation |
|---:|---|---|---|
| 1 | Quarterly first-Energy Planning cue | Timestamped transcript/tool trace: whether a verifiable current-quarter checkpoint exists; when absent, whether rolling-planning is reread and fresh observe grounds the checkpoint before Energy | Tool visibility may not prove internal adherence; one run only |
| 2 | Early / mid / late checkpoint presence | Transcript segmented by public game month; count valid compact checkpoints and their triggers | Segment gaps may reflect missing raw trace |
| 3 | Same-quarter checkpoint reuse | Compare quarterly checkpoint with following main-action context; note any material intervening feedback/state change | Does not isolate cue's causal effect |
| 4 | Semiannual / severe-warning / continuation recovery | Observe each trigger and whether Skill reread + fresh checkpoint rebuild occurs; mark untriggered cases `NOT_OBSERVED` | Trigger may not appear |
| 5 | Context compression / continuation | Record explicit compression/continuation evidence and whether session, fresh observe, and current objective are re-established | Framework may not expose compression events |
| 6 | One Primary Gap | Check each strategic checkpoint names exactly one public gap/objective and does not silently use balanced/default priority | Does not prove the selected gap was optimal |
| 7 | Progress labels | Check `ADVANCING` / `STALLED` / `UNKNOWN` uses comparable fresh public evidence; absent comparison stays `UNKNOWN` | Attribution can remain uncertain |
| 8 | Advertised vs observed effects | For repeated actions compare menu advertised effects with recent same-session observed field deltas and Planning rationale | Sequence alone is not causation |
| 9 | Two-checkpoint stall response | When same action/same gap has no progress at two adjacent comparable checkpoints, check for a different-type legal alternative comparison | If no such stall occurs, `NOT_OBSERVED` |
| 10 | Single miss does not force switch | After one no-progress checkpoint, verify no automatic forced action switch | Alternative may still be chosen for independent evidence |
| 11 | Stall does not force alternative selection | After valid STALLED, verify alternative comparison; if the old action remains, rationale must match changed gap or reliable observed benefit | One choice cannot estimate long-run value |
| 12 | Board refresh and freshness | Board snapshots against same-session fresh `observe`, confirmed actions, source/time; record stale/mismatched state handling | Only visible board/trace evidence counts |
| 13 | `recent_effects` boundedness | Count entries (maximum two); verify confirmed action, public target/field, comparable before/after and source | Small sample; no causal claim |
| 14 | Contaminated effect fallback | If intervening event/action or competing cause exists, check effect becomes `UNKNOWN` or is omitted | May not arise |
| 15 | Memory write/read/recovery | Not applicable: Memory is not adopted. If any unexpected persistence surface appears, record it and stop classification as `UNKNOWN`; do not infer authorized Memory | No Memory behavior is specified |
| 16 | Cross-session isolation | Check new-game identity and absence of reused old Board/recent effects/objective in available trace | Runtime file scope may not be observable |
| 17 | Material-outcome reprioritization | At a severe public consequence, check Planning reopens the Primary Gap and compares currently legal paths without fixed answers | Trigger may not occur |
| 18 | Composite marginal benefit | At quarterly Energy, compare useful public components for current gap against Energy/opportunity cost; check no single saturated component shortcut | Menu/state evidence may not show actual effect |
| 19 | Plateau reconsideration | When public progression stalls, check a legal alternative is reviewed without inventing promotion thresholds | Promotion mechanism may remain opaque |
| 20 | Public promotion readiness | No dedicated promotion rule adopted. If public feedback/opportunity wording occurs, record whether it informs generic progress review; no numeric threshold inference | Promotion may not occur or be decomposable |
| 21 | Wealth opportunity | No dedicated wealth heuristic adopted. Record public wealth-related options and visible trade-offs only; do not infer salary/promotion/event causality | Wealth contributors may be inseparable |
| 22 | Risk Budget | At checkpoints, assess `TIGHT` / `AVAILABLE` / `UNKNOWN` against fresh material warning and visible relevant safety margin | Safety margin is public-contextual, not a hidden threshold |
| 23 | Controlled aggression / soft costs | When AVAILABLE, check ordinary soft cost alone does not veto a legal high-upside growth path; record public benefit and opportunity cost | One choice cannot prove improved outcome |
| 24 | Material Risk protection | On a clear material warning, check candidate-specific mitigation review remains intact; Soft Cost distinction must not discount the warning | Trigger may not occur |
| 25 | High-impact rubric | No universal rubric adopted. Record any unexpected second-review behavior as drift; do not require a new rubric | Not applicable absent explicit adoption |
| 26 | Ordinary-event oscillation | Count candidate reversals without new public evidence; compare with available prior evidence, and check cap of two strongest candidates / reopen gate | Single run is not a robust frequency estimate |
| 27 | Normal-growth false positives | Record ordinary growth decisions unnecessarily marked risky or blocked by ordinary soft cost | Context-specific observation only |
| 28 | Role overlap / reasoning drift | Verify Board stays factual, Planning owns Primary Gap/Risk Budget, Risk reviews current candidate, Trace stays marker-only, and one Agent decides | Transcript may not reveal all hidden internal reasoning |
| 29 | Quarterly action lock-in | Count repeated same main action (including S06 Run #1 reference 16/16) and inspect whether fresh observed no-progress triggers alternative comparison | Counts alone do not establish defect or cause |
| 30 | Month checkpoints | Capture M6, M12, M18, M24, M36, M48 if reached; use `NOT_OBSERVED` for unreached months | Variable survival/run termination |
| 31 | Public state trajectory | Record Level, Wealth, Skill, Network, Output, Health at available milestones, with source and month | Descriptive only; no causal attribution |
| 32 | Promotion timing | Record observed promotion month(s), or `NOT_OBSERVED`; do not predict hidden criteria | May not occur in one run |
| 33 | Final outcome | Record score dimensions, quantitative/competition partial scores if available, survival months, and grade | Single outcome cannot demonstrate stable 80+ |
| 34 | Cost and runtime | Record available input/output/total/cache tokens, by-model usage, reported cost, and runtime; unavailable fields remain `UNKNOWN`, not zero | Provider reporting may omit fields |
| 35 | Failure classification | Separate technical/runtime/provider failure from in-game strategy/outcome failure using logs and completion evidence | Partial records may yield `UNKNOWN` |
| 36 | Single Agent authority | Confirm exactly one successful `take_action` submitter and no Skill/other role submission | Evidence is limited to observed tool/action trace |

No score threshold is a static PASS criterion. Any future run still requires a separate Main Game Gate and remains a single-run observation unless Main approves a controlled design.
