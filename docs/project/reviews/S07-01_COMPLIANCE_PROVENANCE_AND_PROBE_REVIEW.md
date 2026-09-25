# S07-01｜合规证据溯源、公开接口廉价策略探针与 Mid-70 诊断

## Decision

`QUARANTINE_FOR_MAIN_REVIEW`。W1 Compliance Provenance Gate = `FAIL`，仅限下表标出的语义 cue 子类和精确的 story top-two cap 尚无独立、允许的证据链。按任务合同，W2 与 W3 均 `SKIPPED_BY_GATE`；本报告不作 probe 建设建议，也不解释 75 分结果。

本结果是合规溯源结论，不是 Candidate 的 gameplay/runtime 验收。没有修改或重建 Candidate，没有解除 Design Freeze，也没有授权下一局。

## Identity and evidence boundary

- Task/status: `S07-01` / `REVIEW_COMPLETE_WITH_W1_FAIL`; serialized root `main` workflow.
- Repository/base: `MyKr-YSteinsK/CareerSim-BDCI26`, `main@4372921589d2cc64e2aa5cd2aa3e4abfc4e929af`.
- Stage: S07-Lab active; S06 accepted/complete; `NEXT_GAME=NOT_AUTHORIZED`.
- Candidate: `candidate-v6b-runtime-correctness`, parent `candidate-v6-auditable-control-loop`; status `STATIC_CORRECTNESS_PATCHED`.
- Frozen identity verified at base: runtime manifest SHA-256 `8cbf68fa4c6ae055db9ad74942e37a649bfa13dca73b8924175467a5ee80e351`; instruction SHA-256 `a891fa103f0d4f910c9bbcc5ab91ab8bbbfe4cb242b9506d63374f1cf75d8074`; Risk `f9cafecad85cad39d34bfd0266eaea9e88d882cc`; Planning `78a4b578fcb71eef04bc97ec0e3471820fecfe2f`; Board `b6d371d74f3477f4f6cdeabe8482093a78cbe3e5`.
- Permitted support used: the frozen participant-facing facts in `OFFICIAL_SOURCE_LOCK.md`; identity-matched public observations/actions/receipts in the committed v4 and original-v6 run records; public S03 Risk contract; and engineering/runtime evidence for the v6b corrections. The v6 record supports only observations about its own predecessor run, not runtime validation of v6b.
- Excluded: `docs/project/STRATEGY_EVIDENCE.md` contents, decoded simulator internals, hidden state/effects, thresholds, and post-choice data as policy support. The current candidate metadata still has a `strategy_evidence` pointer to that quarantined history; the pointer is not treated as evidence.

Evidence anchors: `OFFICIAL_SOURCE_LOCK.md` (public 48-month/monthly/quarterly/semiannual structure); v4 public run record at commit `2d33eb90212b6037e283238358c33604d3120149` (blob `cbb60024a9f76dc905f42fcf1689f61b117d01d8`); original v6 run record at commit `8b6696a7d17b5204817410affc71a4ac9ecc8212` (blob `b35f06d02ae7fcc840a753fcd9059a9525d374cd`); and S06 closeout at the starting main.

## Policy provenance matrix

| Current material policy surface | Provenance class | Independent allowed support and finding | Deployability verdict |
|---|---|---|---|
| Fresh current-session public state; Board facts/freshness; attributable effects; no cross-session state | `PUBLIC_RUNTIME_EVIDENCE`, `ENGINEERING_RUNTIME_ONLY` | Public observe/action records and Runner/session contracts. Board’s factual-only ownership and bounded recent effects do not depend on hidden state. | `PUBLIC_EVIDENCE_SUPPORTED` |
| Public survival guard; survival trend → candidate-independent Risk Budget; safety as constraint; Soft Cost is not alone a veto | `MIXED` | S06-24 publicly recorded Health decline/warning with `TIGHT`, later recovery/`AVAILABLE`, and a separate M27 risk-budget observation; v4 records public Health warnings and a public compliance choice. These support a public-signal review rule, not causal survival benefit or a numeric cutoff. | `PUBLIC_EVIDENCE_SUPPORTED` (limited to public signals; efficacy unproven) |
| One Primary Gap; public Progress; observed over advertised effect; two comparable checkpoints before `STALLED`; compare one different path without forced switch | `MIXED`, `HISTORICAL_LEGAL_TRAJECTORY` | S06-24 recorded a repeated Energy action with no observed Output increase and adaptation; historical trajectories also show action frequency alone does not explain outcomes. This supports measuring fresh progress and guarding against a one-observation switch; it does not prove the two-checkpoint policy improves score. | `PUBLIC_EVIDENCE_SUPPORTED` (procedural hypothesis only) |
| Public horizon; quarterly Energy/Main joint planning; public review/promotion reset; pre-review reserve check | `PUBLIC_DOCUMENTATION`, `HISTORICAL_LEGAL_TRAJECTORY`, `MIXED` | Source Lock supplies the public schedule; run records expose months, legal menus, feedback and promotions. These support review timing and public-state comparison only—not hidden readiness or promotion formulas. | `PUBLIC_EVIDENCE_SUPPORTED` |
| Candidate-first Risk gate; Material Risk vs Soft Cost; bounded `RECONSIDER` with a relevant legal alternative; no mandatory switch | `PUBLIC_RUNTIME_EVIDENCE`, `HISTORICAL_LEGAL_TRAJECTORY`, `MIXED` | S03-02 defines a public-evidence-only candidate gate (its smoke did not validate game behavior); v4’s public confidentiality/Health cases and v6 M13’s observed candidate-specific reconsideration independently support the general gate. | `PUBLIC_EVIDENCE_SUPPORTED` (triggered examples only) |
| Semantic cue enum and cue-only-not-verdict boundary; Health and confidentiality examples | `MIXED` | The generic public-warning gate predates S06-09; v4 has participant-visible Health and confidentiality examples. Those examples independently support these narrow review cues, not a general classifier or its recall. | `PUBLIC_EVIDENCE_SUPPORTED` (narrow examples only) |
| Specific `integrity/concealment` and `material reliability incident` cue families | `MIXED` / `FORENSIC_ONLY` provenance risk | The families entered the candidate in `0827097` and were retained/narrowed in `5e1718c`; the architecture review `78ad468` points to S06-14 for the pattern library. S06-14’s declared source includes decoded Dev `.data`/simulator-derived analysis. No independent allowed participant-visible run evidence for these specific cue families was found. “Cue only triggers review” does not cleanse that provenance. | `QUARANTINE_FOR_MAIN_REVIEW` |
| Ordinary story comparison capped at two strongest candidates | `MIXED` / `UNKNOWN` | The exact cap appears in the S06-14 pattern proposal and entered the v5 policy in `0827097`. S06-24 independently supports closing deliberation when no new evidence arrives, but does not establish that exactly two candidates is a safe or sufficient comparison cap. | `UNKNOWN_NEEDS_MAIN_REVIEW` |
| `DECISION_CLOSED` after final Risk gate absent new public evidence | `PUBLIC_RUNTIME_EVIDENCE`, `ENGINEERING_RUNTIME_ONLY` | S06-24 records repeated re-opening without fresh evidence; S06-25 formalized the close/ reopen boundary. It changes process control, not game facts. | `ENGINEERING_RUNTIME_ONLY_OK` |
| Canonical CTRL in `take_action.notes`; `RECONSIDER/X`; one-integer Energy call plus fresh observe; compression snapshot recovery epoch | `ENGINEERING_RUNTIME_ONLY` | S06-24 action/tool/compression records and S06-25’s bounded runtime-correctness patch. These specify audit and tool sequencing, not hidden game strategy. | `ENGINEERING_RUNTIME_ONLY_OK` |
| Single Agent authority; 3 Skills; no durable Memory, fifth Skill, Team/Swarm; no hidden thresholds, evaluator weights, or title→answer lookup | `PUBLIC_DOCUMENTATION`, `ENGINEERING_RUNTIME_ONLY` | Current accepted architecture/governance and explicit participant/public-only contracts. No candidate or authority drift found. | `ENGINEERING_RUNTIME_ONLY_OK` |

### Gate rationale

The public-risk gate itself has independent allowed support. W1 nevertheless fails because two action-gating cue families have a material provenance path through S06-14’s disallowed simulator-derived analysis and lack an independent public-run basis; the exact two-candidate cap is also not independently grounded. Both remain in the frozen deployable candidate today, and this task cannot remove, edit, or silently relabel them. Main must decide whether to quarantine/remove those clauses or authorize a separately scoped provenance recovery. No hidden values, event answers, or simulator-derived outcome details are reproduced here.

## W2｜Cheap public probe

`SKIPPED_BY_GATE`. No feasibility ranking, implementation, or probe was performed because W1 did not pass. A future probe decision must follow Main’s resolution of the quarantined clauses; no live interface was called in this task.

## W3｜Mid-70 diagnosis

`SKIPPED_BY_GATE`; `MID70_BASIN_NOT_YET_DIAGNOSABLE` is not asserted as a completed comparison. This task made no cross-run basin or policy hypothesis because the W1 prerequisite failed. The two high-scoring 48-month records remain descriptive, non-paired observations; no causal or stability claim is made.

## Limits and operations

- No Candidate, runtime manifest, Skill, Runner, dependency, `CURRENT_STATE`, run history, raw evidence, or runtime file was modified.
- Provider requests, service starts, installs/reloads, MCP calls, `new_game`, live `observe`, `take_action`, Runner play, and gameplay: all `0`.
- No official web page was fetched; public contract facts were taken from the repository’s frozen Source Lock.
- S06-24 is one run of the original v6 identity. v6b remains `NOT_RUNTIME_VALIDATED`; gameplay effectiveness, stable 80+, and v6b adherence are not established.
- During provenance work, a broad read of the committed S06-14 review returned simulator-derived aggregate material outside the permitted policy-evidence boundary. The details were not used to support a rule or copied into this report. Further content inspection stopped; affected policy clauses are quarantined. This is an execution-boundary issue, not a live operation.

## Next recommendation

`RETURN_TO_MAIN_FOR_COMPLIANCE_REVIEW`. Main should decide the disposition of the two unsupported cue families and exact two-candidate cap before any offline probe design or Mid-70 diagnosis. Design Freeze remains active; no Game Gate is requested or authorized by this task.
