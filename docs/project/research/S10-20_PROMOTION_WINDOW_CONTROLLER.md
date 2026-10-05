# S10-20 — Promotion-Window Deterministic Controller

## Decision and evidence boundary

**CONTROLLER_LOGIC_SIGNAL_WEAK**. Task completed with a negative build gate. Local deterministic execution works; this prototype does not establish multiple corrected historical decision failures. **Do not create v15.** Provider phase skipped at the replay gate; CareerSim service/game/DB/Provider operations all zero. Exact v6d remains SAFE FALLBACK, NOT FINAL OPTIMUM.

FACT: 24 deterministic scenarios pass; 24 stored current snapshots plus 17 Review/Level checks pass (41 checks, not 41 independent cases). Actual frozen PowerShell tool executes the installed fixture helper and returns JSON, retains state across calls and simulated compression, and resets it on isolated reinstall. These are tool/state facts, not model adherence or gameplay evidence.

INFERENCE: deterministic continuity alone is insufficient. Ranking depends on whether a warning is currently binding, whether work is actually realizable, and whether semantic tags correctly describe alternatives. This replay contains eight UNKNOWN evaluations, mostly precisely at those boundaries. Mechanically preserving an unresolved warning can crowd out growth without proving repair is currently necessary.

## Identity / scope

- Base: `main@62f33f39aff7af3d1692c53191f76f521734511f`; remote `MyKr-YSteinsK/CareerSim-BDCI26`.
- Parent evidence: S10-19-R3 local helper feasibility. Fallback source: `e7e8ab44dd85a29135eb089ef29de8fed298f4a4`.
- Only three research/review artifacts and targeted CURRENT_STATE edits are durable. Prototype/harness/raw evidence stay ignored under `.local/scratch/s10-20` and `.local/runtime/s10-20-controller`.
- Formal main checkout continues to hold historical v8a. No copying of v6d into formal runtime, no new Candidate, no change to Skills/manifest/Runner/dependencies/provider/retry.
- Fixture install count 4 across initial check and transport correction, shared install 0; actual shell executions 6. These inert fixture copies use patched setup/path routing; they are not full production installations.

## Delegated input-seam decision

Evidence → Investigation → Decision: stored accepted observe receipts expose public time/status/menu. Main/Board copying can drift. Use the **whitelisted observe envelope** as factual authority, plus separate bounded public semantic annotations. No DB/MCP retrieval by helper. This prototype consumes accepted public projections, not every possible raw MCP wrapper; a future integration still needs a wrapper normalizer and freshness provenance check.

Input includes current public Month, Level/tenure, S/N/O/W/H/D/Energy, menu text and explicit costs. Semantic annotations carry channels, risk/repair domain, horizon, delivery role/target, visibility, cost class, confidence and evidence. Previous completed public transitions can supply same-month/same-Level response labels. All hidden fields, advertised hidden-effect maps and simulator flags are excluded from controller/replay inputs. Historical current choice, future results, final scores, run names and session IDs are excluded. Prior public choices may appear only as response history already known at decision time.

Malformed/missing facts, ambiguous menu IDs, conflicting fresh Month, corrupt state and stale-Level injected responses fail INVALID without state write. Missing semantic certainty is not guessed into a fact. **Limitation:** annotations are not mechanically verified against a tool receipt; confidence is recorded but not used as a hard semantic-safety filter. Numeric freshness validation cannot prove the model supplied the latest receipt. Provider input/adherence remains NOT_EXERCISED.

## Bounded state and ordinal contract

State: schema_version; month/Level/tenure/months_to_next_review; last public Review; capital baseline/current/deltas and window_start_month; one material warning with public quote; health need; one delivery item/maturity/evidence; latest family responses with Level/Month; objective/secondary; updated Month/Level; weak-growth flag. State max observed 1546 Unicode chars; hard serialized bound 6,000 chars. Helper 158 LOC / 12157 Unicode chars. Public state is fixed at Skill/controller_state.json, input at Skill/public_input.json. Atomic local replacement occurs only after successful parse/rank. No arbitrary input source path.

Fresh facts replace stored public numbers; Level change clears old response evidence; new formal Review replaces window baseline/objective. Warning clearance needs a relevant public clearance annotation, not praise/promotion/high Health. One delivery item only; explicit public evidence required for REALIZED/RECOGNIZED; retirement supported. Its semantic truth remains the annotation boundary.

Lexicographic ordering (ordinal positions, no weighted score):

1. R0 exclude unaffordable/invalid options using explicit Energy cost.
2. R1 material warning/health constraint: suitable repair domain first, avoid material-risk choice. Health repair is not trust repair.
3. R2 explicit received Review gap addressed within the window; generic “只会忙、不会赢” is only a visibility interpretation, not an Output threshold.
4. R3 verify/complete/recognize the existing item within the window over an unrelated start when comparable.
5. R4 durable within-window capital; then clean GAIN / UNKNOWN / FLAT classes.
6. R5 same-Level FLAT discounts growth/Review/realization motives; Level reset removes old evidence. No permanent cap.
7. R6 weak window: elapsed public window, at least two non-growing dimensions, no realized result, and unresolved gap or local flat. This descriptive flag has no promotion target/weighted aggregate.
8. R7 Health gets a recovery motive only from public need; below 10 alone never triggers priority. Lower public cost and choice ID resolve remaining ties.

R6 has one observed trigger (D03); it does not prove capital velocity causes promotion. Final ID tie-break is deterministic but has no independent quality claim. Result-horizon labels remain coarse: no reliable action-duration-to-remaining-month calculation was established. This is a limitation of H4 and the replay gate.

Output ranks only **one next action**, lists fired rules/evidence and the first ordinal position where each alternative loses. No quarter bundle, stat threshold, action quota, event answer lookup, weighted hidden-score reconstruction or additional strategy objective.

## Tests / tool boundary

24/24 synthetic tests: initial state; invalid month-zero Review; formal no-promotion reset; promotion update; old flat invalidation; same-Level flat reroute; trust repair; unrelated praise; explicit relevant clearance; stale stored number replacement; REALIZED; RECOGNIZED; retirement; corrupt state; missing field; explicit reset; identical output; no automatic Health topping; stale response rejection; existing-result verification; unsupported completion rejection; weak velocity; fresh-window control; affordability.

Additionally real isolated installs verify reinstall reset. Real CurrentRoundCompressor replacement callback is used with mocked multi_compress: it proves file independence from conversation replacement, not real summarization or model recovery. The first frozen PowerShell result had valid JSON but mojibake in Chinese quotes. ASCII JSON stdout escaping fixes transport; exact public quote roundtrip then passes. Ranking/update logic was unchanged after unblinding; only fixed input-path and stdout transport revisions followed it.

## Historical replay, freeze and unblinding

12 dev + 12 holdout. Families: v6 (4), exact v6d Run01 (6), Run02 (6), Run03 (4), v11b partial (4). Holdout chooses two SHA256-smallest unused public Energy snapshots per family and two SHA256-smallest Story snapshots satisfying functional risk terms. Both risk controls happen to share one public situation; they are two run contexts, not two distinct semantic risk classes. This limits coverage.

Holdout frozen 2026-10-05T05:15:21.067758+00:00; blind SHA `e4d77bcb74a3d166fb2696db6f80d7184587c79892890ab68f691ddfbdf333e3`. Outputs frozen 2026-10-05T05:19:53.605747+00:00; output SHA `750a1b08d9515dbc540f00a32b35eea2239d68b7794ead5800f6d6f57fc32757`. Initial public-only sanitization removed session IDs before ranking began. The initial synthetic trust-repair check exposed domain conflation; it was corrected before evaluator unblinding. No holdout-driven ranking revision occurred.

Selection is mechanical and outcomes are absent from controller inputs. This is **input/output blinding**, not an independent blind reviewer: the same executor knows prior accepted forensics. Offline option annotations are case-local public semantics; helper receives tags, never a historical title-to-answer classifier.

| Case | Context (unblinded afterward) | Historical → helper ID | Verdict | Boundary |
|---|---|---|---|---|
| D01 | Run02 M15 L3 | 1 → 4 | KNOWN_ERROR_CORRECTED | STATE_ONLY: L2 report FLAT excluded at fresh L3; cleanup ranking itself is not established improvement. |
| D02 | Run02 M21 L4 | 1 → 4 | PLAUSIBLE_ALTERNATIVE | Old unresolved public serious warning favors cleanup; no proof it beats current growth. |
| D03 | Run02 M33 L4 | 6 → 3 | PLAUSIBLE_ALTERNATIVE | Network is GAIN while Output lanes are FLAT; historical Health also has ordinary cost rationale. |
| D04 | Run01 M33 L4 | 6 → 4 | UNKNOWN | Persistent old warning favors cleanup over Health; relevant current danger versus successful prior repair is not resolved. |
| D05 | Run03 M18 L2 | 3 → 7 | NO_MEANINGFUL_CHANGE | Report versus Network: both useful current growth lanes; no independently demonstrated decision error. |
| D06 | Run03 M27 L3 | 7 → 3 | PLAUSIBLE_ALTERNATIVE | Remaining one Energy cannot afford cleanup; responsive Network compares with report. |
| D07 | Run01 M24 L4 | 4 → 4 | DONOR_GOOD_DECISION_PRESERVED | Same cleanup choice with unresolved public serious warning; preservation only, not risk-score claim. |
| D08 | Run02 M24 L4 | 6 → 4 | UNKNOWN | Cleanup over Health could be reasonable, but persistence alone does not establish a currently binding threat. |
| D09 | v6 M18 L4 | 1 → 3 | PLAUSIBLE_ALTERNATIVE | Network instead of intensive at new Level; no evidence-intensive always bad or Network optimal. |
| D10 | v6 M36 L5 | 6 → 3 | UNKNOWN | Donor Health recovery versus Network: workload/exposure annotation insufficient to judge this change. |
| D11 | v11b M3 L1 | 1 → 2 | UNKNOWN | CI ownership opportunity traded for ongoing delivery: delay/workload makes alternatives materially different, not an established improvement. |
| D12 | v11b M6 L2 | 2 → 2 | DONOR_GOOD_DECISION_PRESERVED | Limited remote assistance preserves existing delivery and useful contribution without new week-long on-call. |
| H01 | v6 M42 L5 | 7 → 3 | PLAUSIBLE_ALTERNATIVE | Both report and Network have clean GAIN; tie mechanics do not demonstrate an improved choice. |
| H02 | v6 M48 L6 | 3 → 7 | PLAUSIBLE_ALTERNATIVE | New-Level report versus Network, remaining one Energy; neither public alternative is demonstrably better. |
| H03 | Run01 M33 L4 | 7 → 7 | DONOR_GOOD_DECISION_PRESERVED | Same responsive report; unaffordable cleanup excluded. |
| H04 | Run01 M15 L3 | 7 → 7 | DONOR_GOOD_DECISION_PRESERVED | Same responsive report with one Energy remaining. |
| H05 | Run02 M9 L2 | 7 → 4 | UNKNOWN | Cleanup beats responsive report only because old serious warning remains; current bindingness is ambiguous. |
| H06 | Run02 M48 L5 | 6 → 3 | PLAUSIBLE_ALTERNATIVE | Flat Output lanes discounted and Network GAIN compared; Health recovery is not independently shown wrong. |
| H07 | Run03 M39 L4 | 6 → 4 | UNKNOWN | Cleanup versus Health; cannot establish improved handling without current threat and repair-state semantics. |
| H08 | Run03 M45 L4 | 7 → 7 | DONOR_GOOD_DECISION_PRESERVED | Same responsive report, cleanup unaffordable. |
| H09 | v11b M36 L4 | 7 → 4 | UNKNOWN | Old serious warning dominates report; incomplete retained delivery/repair evidence prevents strong superiority verdict. |
| H10 | v11b M33 L4 | 7 → 4 | UNKNOWN | Same limitation: warning persistence crowds out visibility; no safe claim of improvement. |
| H11 | Run01 M18 L3 | 1 → 1 | DONOR_GOOD_DECISION_PRESERVED | Transparent result/risk communication kept; clearly unsafe concealment rejected. |
| H12 | Run03 M3 L1 | 1 → 1 | DONOR_GOOD_DECISION_PRESERVED | Transparent concise report kept; hidden risk concealment not favored. |

Totals: KNOWN_ERROR_CORRECTED=1 (STATE_ONLY); preserved reasonable donor/control choice=7; plausible alternative=7; no meaningful change=1; UNKNOWN=8; demonstrated new material risk=0; demonstrated new growth regression=0. Holdout: preserved=5, alternative=3, UNKNOWN=4. Neither v6 holdout choice is preserved exactly, but both alternatives remain plausible; no claim that this improves the donor.

## Replay gate and hypotheses

**NOT_PROMISING**. One state-only old-Level correction does not satisfy “multiple known decision errors corrected.” Historical Health/report switches cannot be called mistakes merely because the new helper picks Network/cleanup. The warning hierarchy changes several decisions without establishing that the old public concern remains currently binding; incomplete delivery annotations prevent proof of result-realization improvements. Absence of a demonstrated high-confidence material-risk regression is necessary, not sufficient.

H1 WINDOW_CONTROL: PARTIAL — window mechanics stable, strategic value unproven. H2 DETERMINISTIC_RANKING: PARTIAL — reproducible rules/local flat handling, weak historical correction signal. H3 CAPITAL_VELOCITY: UNKNOWN — descriptive flag, no promotion/growth benefit identified. H4 RESULT_REALIZATION: PARTIAL — synthetic state/rank invariants pass, historical feasibility/realization evidence insufficient. No proposal to fill these gaps with a larger rulebook.

Phase C model/tool probe: **SKIPPED_AT_REPLAY_GATE**. Requests=0, usage NOT_EXERCISED, actual cost UNKNOWN. All model adherence categories are NOT_EXERCISED, not zero observed failures presented as success.

## Current official portability

Checked 2026-10-05: [official README](https://github.com/openJiuwen-ai/CareerSim-BDCI26/blob/main/README.md) describes a Skill ZIP and agent general-tool access; accessible text contains no explicit script/shell prohibition. This is silence, not a guarantee. [Competition page](https://www.xir.cn/competition/1165) returned no readable rules; documentation endpoint read failed. Verdict **LOCAL_OFFICIAL_RUNNER_COMPATIBLE / CLOUD_UNKNOWN**, with real local frozen installer/tool evidence. Production Python/path/sandbox/cloud write permissions remain assumptions, not measured cloud facts.

## Retention / project state / non-claims

New local FORENSIC_HOLD retains exact inputs, mechanical selection, source fingerprints, annotation preparation, frozen outputs, tests, helper/harness and actual tool proof. Owner S10-20; release authority Main/Stage after negative gate acceptance and dependency closure; cleanup requires separate authorization. Existing holds untouched. Compact committed evidence provides verdicts; hashes do not replace retained source files.

HUMAN_PLAY_LAB=CLOSED_BY_USER; no HPL/human/oracle run. No gameplay benefit, stable75, promotion formula, measured true variance, hidden-test transfer, independent reviewer blindness or cloud portability claim. No v15 contract is issued under Decision B.

RETURN_FOR_V15_BUILD_GATE

NEXT_GAME=NOT_AUTHORIZED
