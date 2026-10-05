# S10-22 — Black-box Dev policy-search feasibility

**Decision: SIMULATOR_POLICY_SEARCH_NOT_FEASIBLE.** The engine/public boundary is technically usable, but the frozen deterministic Story nuisance baseline does not meet the predeclared competence gate. This is a negative feasibility result, **not** a tested claim that macro policies have no advantage. No formal Candidate was changed.

## Scope and chronology

This task replaces retrospective trajectory mining with prospective public-only deterministic Dev play. Provider, Jiuwen service, official Runner play and Candidate installation were all zero. Direct local Dev episodes were explicitly authorized by S10-22; they are not official LLM Candidate validation.

1. Inspected only adapter/serialization, storage-interface and RNG plumbing needed to call the frozen engine. No event-effect dataset, promotion requirements, score configuration or failure-counter values were inspected for policy construction. Dataset bytes were hashed for identity, not parsed by policy.
2. Built a separate policy process and official engine evaluator with opaque in-memory persistence. Two interface probes ended naturally without displaying reward; one later encoding-debug episode was aborted at a rejected action and one menu probe was intentionally partial. These are diagnostics, not search seeds.
3. Froze all Story scoring rules, twelve macro configurations, seed sets and selection/stop criteria at **2026-10-05T07:21:07.406439Z**. No Story lexicon or decision logic was tuned from rewards.
4. Fixed ASCII transport after Windows isolated Python garbled Chinese JSON. This changed only the adapter. The first reproduction attempts also exposed a cold-versus-warm process-global initialization difference in public Network state. Retained public-play warmup, followed by same-seed warm/warm replay, gave identical trajectories. No global state value was read/reset or game mechanics changed.
5. Adapter refreeze retained the initial receipt and unchanged policy bytes. Warmup and the 16-seed baseline batch then ran. Two natural completions failed the frozen **at least 8/16 complete** criterion. All sixteen seeds remain in the result.
6. Stopped before macro screening, confirmation and holdout. Later changes only reject nested/noninteger month payloads, close child pipes and mechanically block search after the failed gate. Original frozen policy bytes remain locally recoverable; the decision-function AST is unchanged. No new episodes followed these boundary changes.

The initial static inspection predates the measured harness interval. Timestamps, code hashes, seed lists, adapter revisions and local evidence hashes are in [compact results](S10-22_POLICY_RESULTS.json). This was a pre-search feasibility assessment, not a held-out policy contest.

## Engine identity and public firewall

- Root interpreter: `D:\CS\CareerSim\.venv\Scripts\python.exe`, Python 3.12.13.
- Frozen packages: `career-emulator==1.0.1`, `career-emulator-bdci26==1.0.0`.
- Explicit dataset: installed package's **dev/dataset**, 194 files; aggregate relative-path/content identity `34d976e264f905b8685cc2ea4df0dacb29ef92e02733010371170f8f538eca90`.
- Engine Python aggregate identity: `ad32fedd7893055edd9d2bf9e1bd9211ece2615ba7af2d7e5b8bbdfecf09a055`.
- Direct `GameEngine.new_game/observe/take_action`; `observe().to_mcp_dict()` is exactly the official MCP response serialization. No network listener was started. Socket connect/connect_ex were denied before engine imports, after Windows asyncio constructed its local self-pipe.
- UUID = first 32 hex digits of SHA256(`S10-22:<seed>`); global `random.seed(seed)`; engine parent `PYTHONHASHSEED=0`. Policy never receives seed or session UUID. Only one seed's warm replay and cross-process cold replay were tested; universal cross-policy/path-order reproducibility is unestablished.
- `MemoryStore` deep-copies opaque engine sessions through the normal save/load interface. It does not inspect fields, extract statistics or persist/read a DB. Engine rules, loaders, scoring and transitions remain official. This is evaluator persistence, not Candidate Memory.

**Important interface finding:** official MCP stripping alone is insufficient for this task's stricter firewall: regular legal choices still contain `status_updates`. The adapter drops that entire map, plus IDs, internal fields and all unknown data. It does not turn advertised deltas into policy features.

Policy input is a JSON copy of only public month, nine public status fields, textual event/rules, current remaining Energy, legal choice integer/text/description/public Energy cost and fresh feedback. The policy receives no score, flags/counters, event/node/action IDs, UUID, dataset reference, engine object, future outcome or diagnostic key names. Terminal score remains evaluator-side. Schema validation rejects extra or nested fields rather than trusting their names. The child has no engine/filesystem/network imports or credential environment. This is auditable process/data separation, not an OS security sandbox against arbitrarily rewritten code.

Six targeted test groups PASS: official stripping plus allowlist; 22 private-field/nested-type poison variants; AST/import/file-access exclusion; real subprocess Chinese-menu interpretation and integer output; same-Level flat/reset; failed-feasibility mechanical stop. Reward data never enters a decision request.

## Frozen Story nuisance policy

Functional action-text scoring only: penalize explicit deception/concealment/fraud/confidentiality violations and uncontrolled acute harm; prefer lawful authorization/disclosure, constructive communication, credible responsibility/delivery, bounded scope and acute medical recovery. Situational clauses use generic public emergency/confidentiality semantics. Ambiguity uses lowest legal choice integer. No title/description lookup, event-answer table, teacher, outcome-trained weights or seed-specific rule exists.

This is deliberately a small lexical approximation, **not** full language understanding and not exact v6/v6d behavior. Priorities are manually defined semantic weights, not simulator score weights. Public growth/flat history is local, reset on Level change; Energy chooses one affordable integer, observes, then ranks again. Main has a conditional key-project prior. No numerical Health/promotion threshold is encoded.

| Baseline diagnostics | Observed |
|---|---:|
| Story decisions including one initialization per episode | 655 |
| Nontrivial Story decisions | 639 |
| Selected positions 1 / 2 / 3 | 557 / 59 / 23 |
| First-position selection | 87.2% |
| No difference among semantic scores | 333/639 |
| Highest score tied | 376/639 |
| Selected negative semantic score | 0 |
| Energy / Main decisions | 168 / 67 |
| Energy report / Network / Health / cleanup | 64 / 33 / 53 / 18 |

**FACT:** parsing is not universally stuck on one choice, but neutral tie fallback dominates many menus. Generic safety fixtures pass and no selected text has a negative baseline score; nevertheless real episodes frequently terminate. **INFERENCE:** this lexical nuisance control is too weak to support a high-tail strategy comparison representative of the LLM Candidates. This does not identify an event answer or prove any individual selected action caused death. No small correction was justified and validated independently of outcome fitting, so the frozen baseline was not repeatedly rewritten to obtain a successful gate.

## Round 0 results

Sixteen seeds `220000..220015`, one B0 balanced configuration. No failed/poor seed discarded. Rewards are final public quantitative scores; early-terminal scores remain in all percentiles/rates. Survival duration is the score receipt's `survival_months`, not the displayed terminal month.

| Metric | B0 observed |
|---|---:|
| Valid episodes / technical failures | 16 / 0 |
| Natural 48-month completion | 2/16 (12.5%) |
| Early terminal | 14/16 (87.5%) |
| Final L1 / L2 / L3 / L4 | 9 / 3 / 2 / 2 |
| L5+ / L6+ | 0% / 0% |
| Mean / median | 25.98 / 21.67 |
| q10 / q25 / q75 / q90 | 17.54 / 19.36 / 25.88 / 40.46 |
| Maximum | 60.00 |
| Score ≥70 / ≥75 | 0% / 0% |
| Health / wealth / performance / trust terminals | 10 / 2 / 1 / 1 |

Terminal families come from the official final text, not private counter reconstruction. The two completions reached L4; this baseline already invested 53 Energy actions in Health, so the result does not justify banning growth or blindly adding more recovery. No causal action/death attribution is made. Batch wall time was approximately 0.81s after imports/warmup; simulator speed was adequate. Semantic competence, not compute cost, stopped the experiment.

## Planned search, explicitly unexecuted

Twelve curated archetypes use eight categorical knobs: promotion momentum, no-advance reset, one/two/no same-Level flat discount, qualitative Health bias, report/Network response bias, Skill alternative, Main ownership and public-warning repair persistence. B0 broad balanced, B1 v6-like approximation, B2 v6d-like approximation and B3 conservative control were defined **before outcomes**. Eight alternatives vary these public principles. The full configurations are retained in compact results, but only B0 was evaluated.

Planned paired seed sets: screen32/policy; confirm96/policy; untouched final holdout128/policy. Screen selection was frozen as two nonbaseline policies by ≥75 frequency then q90 with at most two additional terminals relative to B2; always retain B0–B3. These are evaluator criteria, never runtime thresholds. Screen/confirm/holdout episode counts are all **zero**. No finalist, paired policy advantage, holdout winner, best-of-N sensitivity, primitive or challenger contract exists.

| Research question | Answer |
|---|---|
| Q1 competent deterministic public policy? | Technical harness YES; frozen Story baseline competence gate NO. |
| Q2 reproducible macro difference? | NOT_EXERCISED. |
| Q3 robust unseen-seed upper tail? | NOT_EXERCISED; 128 holdout seeds untouched. |
| Q4 distill 1–3 primitives? | None; would be speculation without comparison. |
| Q5 search exhausted? | This implementation is infeasible; cannot prove the whole policy space exhausted. Per task stop rule, proceed to existing-candidate portfolio/freeze rather than more mining. |

## Existing real-candidate portfolio

These are actual tiny historical samples supplied/accepted by S10-22, not simulated distributions or expected scores. Historical runtime-adherence failures remain material submission limitations.

| Role | Candidate | Real scores | Observed 48m | Limitation |
|---|---|---|---|---|
| HIGH_CEILING | exact v6 | 75.29 | 1/1 | Single sample; valid full gameplay but runtime adherence failed. |
| BALANCED research role | v8a | 72.65 / 59.00 | 2/2 | Higher listed ceiling than v6d, wide spread; not proven superior utility. |
| SAFE_FALLBACK | exact v6d | 71.67 / 65.35 / 59.67 | 3/3 | Repeated survival observed; no 75+, execution drift, no guaranteed survival. |
| UNSUPPORTED new route | simulator challenger | none | — | No macro/holdout test. |
| Excluded from automatic fallback | v1 | 76.04 / 35.31 | 1/2 | Highest listed individual score, second sample trust-terminal at25m. |

Recommendation: **FINAL_EXISTING_CANDIDATE_PORTFOLIO_ZIP_FREEZE**, one separate Main packaging decision. Retain v6d as the current fallback and exact v6 as the high-ceiling research reference; v8a remains a historical comparator. Do not change Candidate bytes here, automatically unpause exact-v6 replication or infer cloud attempt availability. This recommendation neither builds nor submits a ZIP. Highest-score leaderboard incentives matter, but local Dev75 is not cloud/Test75 and frequent collapse is not acceptable.

No primitive was distilled: compatibility with v1 high/trust-terminal, v6, three v6d runs, v7o, v11/v11b and terminal controls is **NOT_EXERCISED for a new delta**, and their policies are preserved. This feasibility failure provides no reason to weaken donor risk/survival rules.

Skill Evolution remains **SKILL_EVOLUTION_NOT_SUBMISSION_PORTABLE**. Reused task-frozen facts plus a small static check find an installed approval handler, without proof of unattended, approval-free, manifest-controlled competition-path evolution. No runtime/config probe was made and this route is not reopened.

## Reproduction, retention and limits

Research code: [policy](../../../scripts/research/s10_22/policy.py), [official adapter](../../../scripts/research/s10_22/harness.py), [search gate](../../../scripts/research/s10_22/search.py), [targeted tests](../../../scripts/research/s10_22/test_boundary.py). Root interpreter only, with process-local `PYTHONIOENCODING=utf-8` and `PYTHONHASHSEED=0`.

Static tests: `.venv\Scripts\python.exe -m unittest discover -s scripts/research/s10_22 -p test_boundary.py`. Full historical reproduction should use a separately authorized local output directory and the retained original freeze; existing receipts must not be overwritten. Calling the original search after its failed sanity gate is mechanically refused. Reproduction commands are documentation, not permission for new experiments.

Actual Dev episode starts **28**:16 scored baseline episodes plus12 interface/debug/reproduction/warmup starts.26 naturally ended;2 debug episodes were partial (one rejected action, one menu inspection). Earlier cold/warm failed comparisons are visible diagnostics, not discarded paired seeds. Full traces of six early diagnostic natural episodes were not retained; those counts are tool-output supported and cannot be replayed episode-by-episode. The 16-seed batch and final reproduction/warmup traces are retained locally.

**FORENSIC_HOLD ACTIVE**, owner S10-22; Main/Stage may release only after accepting this negative gate and resolving dependent review, followed by separate cleanup authorization. Exact ignored paths/bytes/hashes are in compact results. Previous holds untouched. Only compact summaries/research code enter Git; no episode traces, DB, service logs, credentials or generated runtime state are committed.

Non-claims: no macro policy advantage/no-advantage proof, no stable75 or true performance distribution, no causal hidden-risk/score/promotion formula, no hidden-Test/cloud transfer and no event-answer mapping.

RETURN_FOR_FINAL_OPPORTUNITY_GATE

NEXT_GAME=NOT_AUTHORIZED
