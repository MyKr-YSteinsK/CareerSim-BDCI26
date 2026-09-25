# S06-16｜最终控制架构审查与 v5→下一候选变更决策

## 0. Identity and decision boundary

- Repository: MyKr-YSteinsK/CareerSim-BDCI26
- Audited base: main = origin/main = bf25ef265106b73e65aec402fac73cd075a41d2a
- Working tree before this review: clean
- Current candidate: candidate-v5-evidence-driven-phase-policy
- Candidate source: configs/current_candidate.json
- Decision: V6_TARGETED_UPGRADE_RECOMMENDED
- Proposed successor name: candidate-v6-auditable-control-loop
- This is an offline architecture review only. v5, candidate metadata, Skills, runtime, Runner, dependencies, and state files were not modified.
- Provider calls, service starts, MCP calls, installs/reloads, game actions, and gameplay runs: 0.

The recommendation is based on control-order ambiguity, stale-scan risk, and missing adherence observability in the written contract. It is not a claim that v5 caused a low score, nor that v6 will improve gameplay or achieve stable 80+.

## 1. Audited candidate identity

The repository’s current v5 identity is internally consistent:

| Item | Audited value |
|---|---|
| Candidate ID | candidate-v5-evidence-driven-phase-policy |
| Parent candidate | candidate-v4-lean-runtime-policy |
| Runtime manifest | configs/runtime_manifest.json |
| Runtime manifest SHA-256 | 5fccff10f90523a3947902038a30e46b8447eb1927456f8eac38b076cbc1e278 |
| Instruction SHA-256 | c3126ec56e0c66655e00d8e8589996e388997ac136959064c0bcc79fcbd52da0 |
| Risk Skill blob | 44dbb4aeeb02610f2203c89aacf14f6e7efd8377 |
| Planning Skill blob | 32d0561aea846383e8efb0fdaaf5f1651a335782 |
| Board Skill blob | 63d99ac6805b278a010d4fb9f753727d8083a511 |
| Skill count / action authority | 3 / Single Agent only |
| Skills subtotal | 15,067 bytes / 198 lines |
| Runtime instruction | 1,721 bytes |
| Total audited policy text | 16,788 bytes |

The candidate records gameplay_validated=false, provider_validated=false, long_horizon_adherence=false, stable_80_plus_proven=false, and next_game_authorized=false. These remain the correct evidence boundary for this review.

## 2. Evidence synthesis: S06-11 through S06-15

| Source | Evidence class and supported observation | Architecture implication | Limit |
|---|---|---|---|
| [S06-11 survival review](S06-11_SURVIVAL_REVIEW.md) | DEV_CONFIRMED multi-channel survival mechanisms; RUN_OBSERVED terminal outcomes include v4 Run #1 Health depletion and a separate trust-crisis route. Earlier quarterly Energy cannot protect a story/review window that has already passed. | Keep survival as a public-state constraint; refresh before consequential choices; reserve the pre-review window; do not optimize safety as the default objective. | Does not establish universal numeric cutoffs, one dominant survival channel, or score benefit from a policy change. |
| [S06-12 promotion review](S06-12_PROMOTION_PERFORMANCE_REVIEW.md) | Public review feedback, promotion outcomes, and progression signals can be observed. Directional timing implications exist, but no reliable public promotion-readiness threshold or universal wealth formula was established. | Let fresh formal feedback and promotion results trigger replanning; use observable progress, not a readiness score or hidden cutoff. | Promotion/wealth co-movement is descriptive, not causal; readiness categories remain unvalidated. |
| [S06-13 quarterly action review](S06-13_QUARTERLY_ACTION_REVIEW.md) | DEV_CONFIRMED action ordering/state updates make Energy choices sequential; public observed gains can differ from advertised effects and may saturate/clamp. Fixed Energy bundle/Pareto analyses are Dev-only. | Plan Energy and Main action together, but refresh state after each state-changing choice; compare observed effect before repeating. | Dev-only bundle rankings are not portable runtime policy and do not prove a fixed action winner. |
| [S06-14 event pattern review](S06-14_EVENT_PATTERN_REVIEW.md) | DERIVED_DEV_ANALYSIS shows heterogeneous event effects. Generic role/project wording is not a material-risk verdict; contextual public consequences matter. | Keep a small contextual Risk pattern set and bounded comparison; ordinary career/delivery/relationship decisions stay with Planning unless a public material consequence is explicit. | No event title/ID answer map, universal primitive ranking, or large keyword classifier is justified. |
| [S06-15 counterfactual review](S06-15_HISTORICAL_COUNTERFACTUAL_REVIEW.md) | MULTI_RUN_OBSERVED evidence is descriptive and does not support causal attribution. A missed review is a refresh trigger, not proof of plateau; v1 progression and promotion show that a single stalled-looking interval is insufficient. | Preserve two adjacent comparable checkpoints; compare one alternative without mandatory switching; use transient overlays only where they change a decision. | Historical trajectories are not a controlled policy comparison; early Skill read count does not prove late adherence failure. |

Across these sources, the supported change is a clearer, shorter, auditable control contract. Evidence does not justify a new Skill, durable Memory, fixed action ranking, score-weight rule, or architecture expansion.

## 3. Persistent instruction audit

The current instruction was audited clause by clause from [runtime_manifest.json](../../../configs/runtime_manifest.json). “Runtime observability” below means whether the next authorized transcript/event record could expose the behavior; it is not proof that a model will obey the contract.

| Current clause | Purpose | Evidence support | Runtime observability | Conflict / redundancy | Decision | Source |
|---|---|---|---|---|---|---|
| Mission, 48-month task, safety constraint, Single Agent submitter | Bound the objective and authority | Strong governance boundary; multi-review | Mission/action actor visible, safety reasoning only partly visible | Keep the authority boundary; avoid repeating it in every Skill | KEEP | MULTI_REVIEW |
| Four-line CONTROL_SCAN after observe and before action | Make phase, survival, gap, cue visible | Need for recurring control cue is a hypothesis; no runtime adherence result yet | Text can be counted, semantics need transcript review | Too much repeated output; requires a candidate-specific Risk Cue before candidate generation | SIMPLIFY | MULTI_REVIEW |
| FOUNDATION / PROMOTION / COMPOUNDING / FINAL_SPRINT | Describe macro progression | Weak as a separate action control; horizon and gap already exist | Labels countable, decision effect not directly evident | Overlaps horizon, remaining windows, and Primary Gap | SIMPLIFY | S06-12, S06-15 |
| SAFE / WATCH / TIGHT / CRITICAL | Summarize public survival state | Public multi-channel survival evidence | Label countable; source facts must be checked | Useful if Planning owns meaning; repeated definitions across instruction/Skills are wasteful | KEEP | S06-11 |
| One public Primary Gap | Focus strategy | Promotion/progression and repeated-action evidence supports a current focal gap | Short label can be inspected against fresh public facts | Avoid turning it into a fixed priority or evaluator-weight proxy | KEEP | S06-12, S06-13, S06-15 |
| Risk Cue enum in the pre-candidate scan | Surface event-risk category | Contextual cues can trigger inspection, not answer a choice | Cue can be counted but may be premature | Candidate-specific Risk cannot be completed before a candidate exists | MOVE | S06-14, S06-15 |
| Board scan each observe; Planning scan each decision; Risk gate each action | Set intended Skill cadence | Appropriate ownership cadence; v5 cadence remains unvalidated | One compact action marker can be correlated with observe/action events | Cadence is repeated in several places; Skill read frequency is not functional-use frequency | STRENGTHEN | MULTI_REVIEW |
| Gate proposed candidate, then use its cue to complete scan; gate again if candidate changes | Review current candidate | Candidate-specific risk review is sound | Candidate and gate result can be associated in transcript | Ordering is circular with a pre-candidate Risk Cue; final candidate must be gated after any change | STRENGTHEN | S06-14, S06-15 |
| Reuse short scan under the same unchanged fresh observe across consecutive Energy choices | Reduce repetition | S06-13 confirms choices can change state sequentially | Staleness may be visible only if observations are logged | Reusing the pre-action scan after a state-changing action risks stale state | REMOVE | S06-13 |
| TIGHT/CRITICAL protects survival and pauses nonessential growth | Preserve survival | Multi-channel terminal routes justify a guard | Band and choice are visible; relevance of candidate cost needs review | A band must not become an automatic veto on unrelated growth | STRENGTHEN | S06-11 |
| First quarterly Energy Planning checkpoint; PRE_REVIEW_CHECK before half-year review | Protect planning windows | Timing/order evidence supports earlier refresh | Checkpoint and action timing are observable | Keep triggers; coalesce when they coincide | KEEP | S06-11, S06-13 |
| Observed effect over advertised effect; two comparable no-progress checkpoints mean STALLED; compare another path, do not force switch | Detect repeated-action lock-in | DEV/trajectory signals support testing observed progress; S06-15 cautions against one-interval conclusions | Requires linked action, target, month, and comparable public state | Correctly bounded; define contamination as UNKNOWN | KEEP | S06-13, S06-15 |
| Semantic Risk Cue only triggers review; ordinary story top-two once | Bound event deliberation | Heterogeneous public effects; no title-to-answer generalization | Candidate count/reopen events can be audited | Generic cue words can over-trigger if not contextualized | KEEP | S06-14 |
| Current-session fresh public evidence; no hidden state/threshold/weights/event lookup | Protect portability and information boundary | Directly consistent with source and project contracts | Static text and source inputs inspectable | No material duplication needed | KEEP | MULTI_REVIEW |
| Reread relevant Skill after context loss; do not copy long reasoning | Recover instructions without bloating context | Recovery is reasonable; actual cloud/runtime behavior remains unknown | Reads are observable, but not proof of functional use | Do not require rereading every Skill every turn | KEEP | S06-15 |
| Exactly four lines; no state/Skill prose/long reasoning | Limit output | Context cost matters, but fixed four-line format contributes to the ordering problem | Line count easy to measure | Replace with one post-gate action marker; keep explanations only at real checkpoints | SIMPLIFY | MULTI_REVIEW |

The persistent instruction should retain only recurring triggers, ownership/order, safety/session boundaries, bounded deliberation, and the compact marker contract. Detailed strategy and Risk semantics belong in their owning Skills.

## 4. structured-state-board audit

1. **QUICK_SCAN cost:** inspecting all seven available public fields is a bounded fact read, but restating and reasoning over all seven after every observe is unnecessary. Read fresh values; emit only changed, relevant, or unknown facts plus freshness.
2. **Seven dimensions:** keep access to Health, Dignity, Network, Wealth, Level, Output, and Skill. The survival review shows that several channels can matter. Do not assign them a fixed priority in Board.
3. **Trend and attribution:** compare same-session public fields at comparable points. Label a direct before/after effect only when the action/result source and intervening state changes permit attribution. If a story, another action, stale observation, or source ambiguity contaminates comparison, write UNKNOWN or omit the effect; do not infer causation from sequence.
4. **Formal feedback and progression facts:** ADD a bounded latest public formal-feedback/review result and promotion result, each with source/month and freshness. Board records what was observed; Planning decides what it means.
5. **Reset and plateau state:** do not add review_reset_pending or a plateau counter to Board. These are Planning interpretations. A short comparable checkpoint belongs in the active Planning context, not durable Memory.
6. **FULL SNAPSHOT triggers:** simplify to new session, quarter planning point, observed formal review/feedback/promotion, material fresh public state change, and context recovery. Remove Board triggers based only on derived survival band or Primary Gap; coalesce simultaneous triggers.
7. **Recovery logs:** retain the existing maximum of five same-session logs only as a bounded fallback when fresh observe is insufficient. Fresh observe remains authoritative; logs do not override it.
8. **High-frequency use:** the contract can request a Board scan after each fresh observe, but cannot mechanically force a Skill call. A transcript-visible marker is a low-cost adherence proxy; it must be checked against the actual observation and subsequent decision.

**Responsibilities to KEEP:** session identity, public facts, freshness, unknowns, bounded attributable recent effects (maximum two), re-anchoring on fresh observe.

**Responsibilities to MOVE:** survival-band interpretation, Primary Gap, progress/stall, reset and plateau decisions → Planning.

**Fields/triggers to REMOVE:** derived reset-pending or plateau counters; repeated full narration of stable state; full-snapshot triggers caused only by a Planning-derived label.

**Facts to ADD:** latest observed formal feedback/review result and promotion result, compactly sourced and timestamped.

## 5. rolling-planning audit

### 5.1 Macro phase

SIMPLIFY the four named phases. They overlap with horizon and Primary Gap, and no reviewed evidence shows that each label independently changes a decision. Planning should reason about publicly remaining action/review windows and whether a benefit can still be realized; emit a phase label only if it changes the chosen path. Do not set fixed month-to-action rules.

### 5.2 Regime overlays

Do not create a persistent state machine. A decision-local mode may be derived from current public evidence, only when it changes the next choice:

- SURVIVAL: fresh public state makes a directly relevant survival constraint binding.
- RESET: an observed review, promotion, or formal feedback invalidated the old comparison; perform one fresh checkpoint and establish a new baseline.
- PLATEAU: two adjacent comparable checkpoints meet the strict STALLED condition; compare one alternative once.
- LATE: publicly remaining time makes only a subset of benefits realistically realizable; no fixed month cutoff.
- NORMAL: none of the above changes the decision.

These labels are shorthand for a current decision, not durable state. When triggers coincide, coalesce them into one Planning checkpoint; do not launch recursive reviews.

### 5.3 Promotion readiness

DEFER a separate NOT_READY / BUILDING / PLAUSIBLE / STRONG / UNKNOWN or READYISH classification. Public criteria are not reliable enough, and this duplicates Primary Gap, progression, and formal feedback while inviting false precision. Use the latest actual public review feedback and comparable progression as inputs to Planning.

### 5.4 Mandatory post-review reset

STRENGTHEN as a bounded Planning rule. After an observed promotion, formal review/feedback, or a known review opportunity with a public result (including no advancement), refresh public state, invalidate the prior progress comparison, and establish a new Primary Gap/checkpoint baseline before the next strategic choice. Do not infer a missed review from silence or predict promotion timing.

### 5.5 Plateau diagnosis

Keep the exact two-adjacent-comparable-checkpoint rule: same strategic action, same Primary Gap, comparable public target state, and no observed target progress at both checkpoints. One no-gain observation is insufficient. If another action/event may have affected the target, or comparison inputs are stale/missing, use UNKNOWN rather than STALLED. On STALLED, compare one different legal path; do not force switching. No persistent plateau counter is needed.

### 5.6 Compact checkpoint

Retain a bounded Planning output of at most six fields:

    Horizon
    Primary Gap
    Progress
    Recent Effect
    Risk Budget
    Path Trade-off

The Path Trade-off contains at most two legal paths. Risk Budget is TIGHT / AVAILABLE / UNKNOWN. The checkpoint does not duplicate the Board snapshot or become a transcript.

## 6. risk-review audit

### 6.1 Candidate-first QUICK_GATE

Risk must review an actual proposed candidate. Use constant-time triage on the current candidate and fresh public context:

- FULL_REVIEW when the candidate is tied to an explicit public material consequence or a high-signal contextual cue.
- A public TIGHT/CRITICAL condition affects Planning’s feasible risk budget; Risk examines a candidate fully when its public downside is directly relevant to that condition.
- WATCH by itself does not cause repeated FULL_REVIEW on every action.
- Otherwise return a bounded quick PASS.

A survival label alone is not a candidate-specific risk verdict. Conversely, an explicit material consequence cannot be ignored merely because a different public dimension looks safe.

### 6.2 Risk Cue and pattern library

Keep the current enum: NONE / HEALTH / COMPLIANCE / TRUST / RELIABILITY / OTHER. Narrow OTHER; HEALTH load/illness can be a semantic subtype, not a new enum. Cues initiate inspection but never choose an answer.

Keep at most four contextual high-signal Risk families:

1. confidentiality or data-authorization consequence;
2. integrity/concealment with an explicit material consequence;
3. health load/illness tied to fresh public state;
4. material reliability incident.

Planning owns ordinary delivery/scope, compensation/career, relationship boundaries, and organizational politics. Move a case to Risk only when the current public evidence states a material consequence. Avoid exhaustive keyword lists and generic role/project words as verdicts.

### 6.3 Enforce recognition-to-action boundary

- ALLOW: no identified material risk requiring a change to the current candidate.
- WARN: expose a relevant concern; submission remains allowed with a concise reason.
- RECONSIDER: the current candidate cannot be submitted unchanged until one directly relevant legal alternative is compared once. After that comparison, the Single Agent may still choose the original candidate if public evidence supports it.
- UNKNOWN: stale or insufficient evidence is not “safe”; refresh if a permitted fresh observation can resolve it. If not, state the uncertainty and make one bounded legal decision rather than entering an endless block.
- CRITICAL: do not submit a candidate whose known public effect materially adds avoidable terminal risk when a directly relevant legal mitigation exists. This is a candidate-specific constraint, not a global second decision maker.

Risk remains advisory and has no action-submission authority. A revised candidate must be gated again; do not repeat the alternative loop absent new evidence.

## 7. Skill activation and adherence contract

Skill-file read frequency and functional-use frequency are different measurements. A full Skill read once does not prove recurring protocol use; repeated file reads also do not prove the reasoning was applied. Persistent instructions can cue behavior but cannot enforce model-internal execution. v5 cadence remains statically specified and runtime-unvalidated.

Proposed CONTROL marker contract: for a future candidate, use one compact, transcript-countable line per attempted action, emitted after candidate generation and candidate-specific Risk review and immediately before the Single Agent action:

    CTRL B=F G=<gap-or-?> P=<A|S|?> R=<PASS|ALLOW|WARN|RECONSIDER|UNKNOWN> CP=<trigger-set-or-> X=<0|1|->

- B=F: Board used fresh facts for this decision; otherwise B=? and do not pretend a stale scan is fresh.
- G: short Primary Gap key or ?.
- P: ADVANCING / STALLED / UNKNOWN encoded A / S / ?.
- R: quick-gate result or final full-review result for the selected candidate.
- CP: coalesced full Planning trigger letters Q (quarter), R (review reset), P (plateau), C (context recovery), or -; more than one trigger may be concatenated.
- X: 1 only when a RECONSIDER cycle compared one relevant alternative; 0 means the required comparison did not occur and the action must not be submitted; - when not applicable. If an initial candidate was RECONSIDERed, but the final gate passes after comparison, record the final result in R and X=1.

If RECONSIDER changes the candidate, gate the revised candidate before emitting the line. Emit no Skill-read marker and no multi-line state dump. The marker is a self-reported proxy, not proof: a future audit must align it to observe/action events and check semantic consistency. Missing or contradictory evidence is UNKNOWN, not proof that a Skill was unused.

## 8. Control-loop audit and final order

The current instruction asks for Risk Cue in CONTROL_SCAN before a candidate is available, then says to derive that cue by gating the candidate. This is a real order ambiguity, not a reason to remove candidate-specific Risk review.

Use this minimal sequence:

    fresh observe
    → Board fact/freshness scan
    → Planning quick scan and coalesced checkpoint triggers
    → legal candidate generation
    → candidate-specific Risk quick gate / conditional full review
    → if RECONSIDER, compare one relevant alternative and re-gate any changed final candidate
    → one compact CTRL marker
    → Single Agent submits one action
    → inspect result and obtain fresh state after the state-changing action
    → Board records only attributable public effect; contamination becomes UNKNOWN
    → next decision

At the first Energy decision of a quarter, run the full quarterly Planning checkpoint before choosing Energy and consider Energy/Main complementarity together. After an Energy action changes state, refresh facts and re-run the quick decision scan before the next Energy or Main action; do not reuse the pre-action scan. Stories, Energy, and Main actions use the same candidate-first Risk ordering. Ordinary stories remain bounded to two strongest legal candidates, absent fresh evidence or a Risk RECONSIDER trigger.

## 9. Trigger and state-machine audit

| Trigger / event | Owner and response | Coalescing / termination |
|---|---|---|
| Fresh observe | Board quick fact scan; Planning quick scan | One pass per fresh state; no recursive trigger from a derived label |
| New game/session identity | Board clears prior-session effects; Planning establishes a fresh baseline | Prior-session facts/effects are invalid immediately |
| Context recovery | Fresh observe and Board re-anchor; Planning rebuilds the relevant checkpoint and rereads only needed Skill instructions | One recovery pass; stale history cannot replace fresh facts |
| First Energy decision in quarter | Planning full quarterly checkpoint | If coincident with review/reset, perform one checkpoint covering both |
| Observed formal review, feedback, promotion, or public no-advance result | Board records fact; Planning invalidates old comparison and establishes new baseline | One reset per observed result; no inferred result from silence |
| Two-checkpoint STALLED | Planning compares one alternative | No switch mandate; no repeated diagnosis until a new comparable checkpoint exists |
| Survival band/material fact changes | Board updates public facts; Planning adjusts constraint; Risk checks a directly relevant candidate | Underlying public change is trigger; a label alone does not recursively trigger |
| Candidate-specific cue/material consequence | Risk FULL_REVIEW after candidate generation | Gate only the current candidate; changed candidate is re-gated once |
| Ordinary fresh decision | Planning quick scan and Risk quick gate | Top-two story comparison once; reopen only with new evidence or RECONSIDER |

The suggested priority is therefore split by stage: (1) session/context re-anchor; (2) fresh survival constraint; (3) review reset; (4) quarter checkpoint; (5) plateau diagnosis; (6) ordinary quick scan; then (7) generate a candidate and run its Risk gate. A Risk override cannot precede candidate generation because it is candidate-specific. Concurrent Planning triggers are coalesced.

## 10. Ownership and conflict matrix

| Concern | Persistent instruction | Board | Planning | Risk | Correct owner / boundary |
|---|---|---|---|---|---|
| Phase / horizon | Requires relevant review, no fixed mapping | Reports public month/review facts | Interprets remaining realizable windows | No phase ownership | Planning |
| Survival | States safety boundary and sequence | Reports public Health, Dignity, Network, Wealth and other facts | Derives current constraint / Risk Budget | Reviews candidate if downside directly relates | Planning for budget; Risk for candidate |
| Primary Gap | Requires one current gap | Supplies facts only | Selects and updates one gap | No ownership | Planning |
| Risk Cue | Requires candidate-first ordering | No verdict | No cue verdict | Assigns contextual cue after candidate exists | Risk |
| Formal feedback | Requires reset trigger | Records latest public feedback/result | Invalidates stale progress comparison and replans | Reviews only explicit material consequence | Planning interpretation |
| Promotion result | Requires refresh | Records observed result | Resets baseline and reselects gap | No readiness prediction | Planning |
| Recent effect | Requires observed-over-advertised policy | Stores at most two attributable public effects | Interprets progress and path relevance | Uses only if candidate risk relevance | Board owns fact |
| STALLED | Requires bounded procedure | Supplies comparable facts | Derives from two adjacent comparable checkpoints | No plateau ownership | Planning |
| Quarterly package | Requires first-Energy trigger | Supplies current facts | Joint Energy + Main trade-off | Gates each proposed action | Planning |
| Story comparison | Sets top-two/no-loop bound | Supplies facts | Provides strategic relevance | Reviews material downside | Single Agent chooses |
| Semantic patterns | Prohibits answer lookup | No pattern verdict | Owns ordinary career/delivery/relationship context | Owns four high-signal material-risk families | Risk/Planning by consequence |
| Context recovery | Requires fresh session context | Re-anchors from fresh observe | Rebuilds one current checkpoint | Rejects stale candidate evidence | Board then Planning |
| Action submission | Declares sole submitter | Advisory only | Advisory only | Advisory only | Single Agent only |

This resolves duplicate ownership by keeping facts, strategy, candidate risk, and action authority separate. No Skill can submit an action or create a second reviewer loop.

## 11. Context budget options

Current exact audit baseline is 16,788 bytes across three Skills plus instruction. The following are rough design ranges, not measured candidate sizes or acceptance limits; uncertainty is approximately ±20%.

| Option | Instruction | Board | Planning | Risk | Approx. total | Adherence clarity | Context cost | Overfit / omission risk |
|---|---:|---:|---:|---:|---:|---|---|---|
| MINIMAL | ~650 B | ~2,200 B | ~4,100 B | ~2,400 B | ~9,350 B | Medium; concise but some ownership/edge cases become implicit | Low | Medium; safety and reset boundaries may be oversimplified |
| BALANCED | ~900 B | ~2,700 B | ~5,100 B | ~3,200 B | ~11,900 B | High; sequence, owner, reset, and bounded risk outcomes remain explicit | Moderate-low | Low-to-moderate; enough detail without reproducing research |
| MAXIMAL | ~1,600 B | ~3,500 B | ~7,400 B | ~4,100 B | ~16,600 B | High on paper, but repetition can obscure the action order | High | High; repeated prose, cues, and examples can create overfit and deliberation |

**Recommendation: BALANCED.** It preserves safety-critical and falsifiable contracts while removing repeated definitions and historical Dev exposition. A larger instruction cannot guarantee adherence; the transcript marker and future review matter more than reproducing the full analysis at runtime.

## 12. Pattern library placement

| Pattern family | Owner | Runtime treatment |
|---|---|---|
| Confidentiality / data authorization | Risk | Review only when the current public candidate/context indicates a material consequence |
| Integrity / concealment | Risk | High-signal only when an explicit public material consequence is present |
| Health load / illness | Risk | Interpret against fresh public health state; do not infer hidden medical thresholds |
| Material reliability incident | Risk | Review explicit material consequence, not generic delivery wording |
| Delivery / scope | Planning | Ordinary strategic opportunity-cost and execution trade-off |
| Compensation / career | Planning | Use public feedback and observed progression; no promotion formula |
| Relationship boundary | Planning | Ordinary friction remains a soft cost unless public material consequence appears |
| Organizational politics | Planning | Strategic context, not automatic Risk Cue |

Keep the existing enum. A cue is an inspection signal, not a verdict. Do not encode event title/ID mappings, fixed answers, or a large phrase dictionary.

## 13. Quarterly policy placement

The joint Energy + Main policy belongs only in Planning and can be reduced to four rules:

1. Maintain one public Primary Gap.
2. Apply directly relevant survival constraints first; safety is a constraint, not the default objective.
3. Compare Energy and Main-action complementarity together at the quarterly checkpoint.
4. Check fresh observed marginal effects for saturation before repeating a strategic action.

Re-observe after each state-changing Energy choice before the next choice. Do not include the Dev-only fixed bundle/Pareto study, menu catalog, or a fixed quarter-to-action rule in runtime text.

## 14. Final 48-month controller skeleton

    OBSERVE fresh current-session facts
    → BOARD record facts, freshness, and attributable deltas
    → PLAN derive survival constraint, one gap, progress, and any coalesced checkpoint/reset
    → GENERATE legal candidate(s)
    → RISK gate the actual candidate; if RECONSIDER, compare one relevant alternative
    → MARK one compact control line
    → SINGLE AGENT submits one action
    → REFRESH state; attribute effect or mark UNKNOWN
    → repeat until terminal state

This skeleton includes quarterly Energy/Main planning, review/promotion reset, two-checkpoint plateau diagnosis, and late-horizon realizability without a persistent mode store, hidden thresholds, event answers, or exhaustive reasoning.

## 15. Candidate v6 exact change set (recommendation only)

No change below is implemented by S06-16. Proposed classifications use only MUST / SHOULD / DO_NOT_CHANGE.

| Surface | Current | Proposed | Why | Evidence | Risk |
|---|---|---|---|---|---|
| configs/runtime_manifest.json | Four-line pre-candidate CONTROL_SCAN includes Risk Cue; scan/gate ordering is circular; stale scan can be reused across Energy choices | **MUST** replace it with a compact recurring kernel; derive facts/gap before candidate, gate after candidate, then emit one action marker; refresh after every state-changing choice; retain session/public-only and bounded deliberation rules | Removes order cycle and stale facts; makes per-action protocol countable | S06-13, S06-14, S06-15 | Extra observe/marker cost; keep marker to one line |
| structured-state-board | Quick scan can restate all stable facts; snapshot triggers include derived Planning labels | **MUST** delta-first output while retaining fresh access to all seven public dimensions; add latest formal feedback/review/promotion facts; remove Planning-derived triggers. **DO_NOT_CHANGE** session scope, unknown discipline, max-two effects, no strategy/action authority | Supports multi-channel survival and Planning refresh without duplicated ownership | S06-11, S06-12, S06-13 | Over-compression could omit relevant facts; static cases must cover all fields and freshness |
| rolling-planning | Four macro phases, gap/progress, risk budget, multiple checkpoint triggers | **MUST** own one gap, comparable progress, risk budget, horizon, review reset, and joint quarterly trade-off; keep strict two-checkpoint STALLED. **SHOULD** derive transient mode only when it changes the choice; remove separate promotion-readiness enum | Makes refresh and switching logic explicit without a persistent state machine | S06-12, S06-13, S06-15 | Qualitative phase/mode can become pseudo-precision; prohibit fixed cutoffs |
| risk-review | Candidate gate plus broad repeated cue descriptions; RECONSIDER recognition-to-action link is not sufficiently enforceable | **MUST** gate after candidate generation; require one relevant alternative comparison before unchanged submission on RECONSIDER; do not force switch. **SHOULD** use constant-time contextual triage and narrow OTHER. **DO_NOT_CHANGE** enum, public-only boundary, no submission authority | Closes v4-style recognized-risk/action gap with one bounded comparison | S06-11, S06-14, S06-15 | Risk may over-trigger; WATCH alone and generic role words must not force FULL_REVIEW |
| configs/current_candidate.json | Identifies v5 and records exact identity | **MUST** only when Main authorizes v6 implementation: create a new candidate identity and record exact manifest/instruction/Skill hashes; keep all runtime/gameplay validation false until evidence exists | Prevents candidate identity drift and accidental v5 overwrite | MULTI_REVIEW | Metadata could overstate validation if copied without updating fields |
| Adherence observability | Cadence is prose; no compact per-action adherence record | **MUST** add one post-gate CTRL marker per attempted action and audit it against transcript/events; do not add framework telemetry or Skill-read markers | Separates functional-use evidence from file-read count at low token cost | S06-15, MULTI_REVIEW | Self-report is not enforcement; semantic audit remains necessary |
| Architecture / frozen surfaces | Single Agent + three Skills | **DO_NOT_CHANGE** Runner, dependency lock, three-Skill count, action authority, no Memory, no fifth Skill, no Team/Swarm | No reviewed evidence passes expansion gate | MULTI_REVIEW | None beyond leaving actual adherence unknown |

## 16. Explicit removal / compression list

| Remove or compress | Replacement / invariant retained |
|---|---|
| 1. Risk Cue from the pre-candidate CONTROL_SCAN | Candidate-specific Risk Cue is produced only after a candidate exists |
| 2. Repeated four-line CONTROL_SCAN prose | One fixed-schema marker after the gate; checkpoint prose only when triggered |
| 3. Separate FOUNDATION / PROMOTION / COMPOUNDING / FINAL_SPRINT labels | Public horizon and decision-local mode only when they change the choice |
| 4. Duplicate Survival definitions in instruction and Skills | Instruction owns trigger; Planning owns risk budget; Risk owns candidate review |
| 5. Long generic Risk keyword lists | Four contextual high-signal families and explicit consequence requirement |
| 6. FULL_REVIEW on persistent WATCH without new relevant evidence | Quick gate continues; full review needs candidate-relevant material evidence |
| 7. Reuse of a pre-action scan across state-changing Energy choices | Refresh current facts after the action before the next decision |
| 8. Board-owned review_reset_pending or plateau counters | Planning rebuilds from one bounded current-session checkpoint |
| 9. Separate Promotion Readiness enum and runtime Dev Pareto exposition | Actual public review feedback, observed progression, and four concise quarter rules |
| 10. Long repeated “do not” prose, example menus, and duplicated strategy markers | Keep only safety-critical constraints, one marker, and owner-specific Skill detail |

Each proposed addition is paired with an explicit deletion or compression above. This is intended as net simplification, not another layer of policy.

## 17. Static verifiability contract for a future v6 implementation

Do not create a verifier in S06-16. A future authorized implementation should statically check:

1. Exactly three project Skills with unique valid frontmatter; no fourth Skill.
2. Runtime manifest and candidate metadata parse; candidate identity points to exact instruction and Skill blobs.
3. Marker grammar is singular and ordered after candidate-specific Risk review, before the action.
4. Risk RECONSIDER requires one directly relevant alternative comparison before the unchanged candidate may be submitted; switching is not mandatory.
5. An observed review/promotion/feedback result invalidates old progress comparison and creates one fresh baseline.
6. STALLED requires two adjacent comparable checkpoints; one no-progress point and contaminated comparisons resolve to UNKNOWN.
7. Board effects remain public, fresh, same-session, attributable, and bounded to two.
8. No numeric hidden promotion/risk threshold, evaluator weight, score-to-80 rule, event-ID/title answer map, hidden state, or fixed menu answer.
9. Single Agent remains the only action submitter; Skills remain advisory.
10. No Runner, dependency, lockfile, durable Memory, service, or live-runtime modification.

JSON/frontmatter parsing, identity/hash checks, targeted static assertions, and git diff checks suffice. No provider, CareerSim, JiuwenSwarm, install, or gameplay test is in this contract.

## 18. Future benchmark audit contract

Only if separately authorized by Main, derive these counts from the transcript and event log without adding verbose runtime tracing:

- fresh observe count;
- CTRL marker count and marker-to-action association;
- Risk quick-gate count and FULL_REVIEW count;
- Planning checkpoint count, including quarterly and review-reset causes;
- plateau-diagnosis count;
- public Survival transitions;
- Primary Gap changes;
- attempted and completed action counts.

For each marker, check that Board freshness matches the preceding observation, Planning fields agree with public facts, Risk result follows candidate generation, and RECONSIDER has exactly one relevant alternative comparison plus a final-candidate gate. Compare counts with actual tools/actions. A missing trigger is NOT_OBSERVED, not a mechanism failure; a marker alone is not proof of internal adherence. Score is a future outcome, never a static PASS condition.

## 19. Architecture expansion gate

| Component | Decision | Reason |
|---|---|---|
| Durable Memory | NOT_IMPLEMENTED / DEFERRED | No evidence establishes portable, session-safe, runtime-observable benefit over a bounded current-context checkpoint |
| Fifth Skill | DEFERRED | Existing Board / Planning / Risk boundaries can express the required behavior; no orthogonal trigger/owner gap is demonstrated |
| Team / Swarm | DEFERRED | No evidence shows a role-separation bottleneck that requires multiple agents; Single Agent remains sole submitter |
| Persistent phase state machine | REJECT for v6 proposal | Decision-local derivation is sufficient; persistent counters add cross-session/staleness risks without demonstrated value |

Reopen only with evidence that the three Skills cannot express a necessary, observable mechanism or that an evidenced single-agent role bottleneck requires review. Any architecture change returns to Main; this review authorizes none.

## 20. Remaining unknowns

- v5 gameplay effectiveness, survival benefit, stable 80+, and hidden-test transfer remain NOT_PROVEN.
- Actual future quarterly Skill adherence and marker truthfulness are unknown until a separately authorized run.
- Whether short persistent instruction plus the marker reliably changes late-horizon behavior is unknown.
- Public promotion/wealth signals do not expose exact internal formulas or hidden thresholds.
- Risk cue precision/recall and any score effect are unmeasured; no keyword classifier is validated.
- Cloud evaluation behavior and exact runtime Skill-loading behavior beyond repository evidence remain UNKNOWN.
- A missed review inferred only from absent transcript evidence is UNKNOWN, not an observed event.

## 21. Main recommendation

Return to Main with **V6_TARGETED_UPGRADE_RECOMMENDED**, proposed candidate ID **candidate-v6-auditable-control-loop**. The high-value work is limited to:

1. correcting candidate-first Risk ordering and eliminating the circular Risk Cue;
2. refreshing state after each state-changing choice;
3. making review reset and strict plateau comparison explicit in Planning;
4. keeping Board factual and Risk material/candidate-specific;
5. adding a single compact, transcript-auditable per-action marker;
6. deleting redundant phase, keyword, and explanatory prose while preserving safety boundaries.

Do not implement the candidate or start a game from this review. v6 is a static-policy hypothesis until separately implemented, reviewed, and authorized for a Game Gate.

**Next Recommendation:** RETURN_TO_MAIN_FOR_V6_IMPLEMENTATION_PLAN
