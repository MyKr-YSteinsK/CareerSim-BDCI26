# S07-50 Skill Authoring Audit & Behavioral A/B Evaluation

**Status:** `EVIDENCE_INCOMPLETE / NO_INTEGRATION`
**Base:** `main@b8fd34a986791ad1a6d87cfa247570f06ef64d6b`
**Candidate:** `candidate-v7n-public-state-delivery-constraint-hardening` (`STATIC_IMPLEMENTED_NOT_RUNTIME_VALIDATED`)
**Scope:** static authoring audit and isolated experimental copies; no formal Skill, Candidate, or runtime manifest change.
**NEXT_GAME:** `NOT_AUTHORIZED`

## 1. Executive conclusion

The current v7n text already contains the S07-48 correctness clauses prompted by the v7m M20 audit: direct public-state copy, acute warning retention, item-linked Delivery proof, retirement without TTL, explicit MODE selection, and Quick/Full Risk semantics. The strongest authoring-level concern now is duplicated semantic authority: the manifest repeats substantial Board, MODE, Delivery, Risk, evidence-firewall, and decision-closure rules that also live in Skills. The Delivery contract has detailed labels and examples of qualifying evidence but lacks the proposed one-sentence item-specific verification test. The other identified wording concerns are plausible authoring hypotheses, not proven causes of the earlier v7m behavior.

An experimental rewrite and 21 public-only cases were prepared. The provider-only run stopped after five requests: three connection-layer failures, including two consecutive failures, and two successful responses with empty content. The protocol correctly stopped; every case/version classification is `TECHNICAL_UNKNOWN`. No A/B result supports integration. Keep v7n and all formal files unchanged. Recovery prompt rewrite remains unjustified.

## 2. External authoring sources consulted

These sources inform authoring method only. Competition facts, strategy, and runtime contracts remain governed by this repository's accepted evidence.

| Source | Relevant guidance used | Boundary |
| --- | --- | --- |
| [JiuwenSwarm Skills](https://github.com/openJiuwen-ai/jiuwenswarm/blob/develop/docs/en/Skills.md) | A Skill centers purpose, steps, and constraints; supporting references/scripts can be separate; Skill descriptions should make the task fit clear. | No installation, runtime, or Swarm architecture adopted. |
| [JiuwenSwarm Skill Self-Evolution](https://github.com/openJiuwen-ai/jiuwenswarm/blob/develop/docs/en/SkillSelfEvolution.md) | Reusable changes should be grounded in recurring task evidence; approval/review and rollback are distinct steps. | No evolution or Memory mechanism implemented. |
| [JiuwenSwarm `swarmskill-creator`](https://github.com/openJiuwen-ai/jiuwenswarm/blob/develop/jiuwenswarm/resources/agent/workspace/skills/swarmskill-creator/SKILL.md) | Borrowed staged routing, procedure sequence, quality gate, and validator/manual-review separation. | Its multi-role composition and orchestration are explicitly excluded. |
| [Agent Skills specification](https://agentskills.io/specification) | Progressive disclosure; keep the main instruction focused and defer detailed resources; validate structure. | Its token/line recommendations are guidance, not correctness thresholds. |
| [Anthropic `skill-creator`](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md) | Draft, create fixed test prompts, assess observable results quantitatively and qualitatively, revise, then expand the set. | The planned behavioral loop was attempted but provider instability prevented comparison. |

Accessed 2026-09-29. No third-party blogs or broader prompt-engineering sources were substituted.

## 3. Current v7n authoring defect matrix

`SUPPORTED` means the text itself exhibits the named structural condition. It does not prove that condition caused a model behavior. The v7m observations below predate v7n and are evidence seeds, not v7n runtime results.

| Hypothesis | Status | Current text evidence and assessment |
| --- | --- | --- |
| H1 `DUPLICATED_SEMANTIC_AUTHORITY` | **SUPPORTED** | Manifest and owner Skills both explain Board copy/firewall, MODE constraints, Delivery proof/retirement, Risk Quick/Full outcomes, and closure. The copies are mostly consistent but create more than one detailed source. |
| H2 `DEFAULT_ANCHORING` | **PLAUSIBLE** | Planning introduces `A = Advance. Default` and progression-first wording; later it explicitly says to select MODE against binding constraints before ranking and lists acute warnings. The structure could make A salient, but the document also states the correct branch. The v7m MODE miss does not prove anchoring, and v7m was not v7n. |
| H3 `AMBIGUOUS_ADJECTIVE_GATE` | **PLAUSIBLE** | “Material,” “binding,” “direct,” “relevant,” and “unresolved” carry branch decisions. Current text supplies examples/categories but no bounded semantic question comparable to the rewrite's yes/no tests. Avoiding invented numeric thresholds remains correct. |
| H4 `EXCEPTION_FIRST_INSTEAD_OF_BRANCH_FIRST` | **PLAUSIBLE** | Planning says Advance is the default before its constraint procedure; Risk introduces the Quick gate before Full Review. Both contain explicit routing, so this is a sequencing/salience hypothesis rather than a missing branch. |
| H5 `NEGATIVE_RULE_OVERLOAD` | **SUPPORTED** (descriptive) | Current files contain 70 matches for the report's negative-directive scan across manifest and Skills. Several protect real invariants; the count does not establish that negative wording caused non-adherence. |
| H6 `MECHANICAL_AND_REASONING_MIXED` | **NOT_SUPPORTED** | Board already separates direct STATE copy in a dedicated procedure step from warning retention and effect attribution. A clearer `COPY-ONLY` label may aid salience, but the current contract is not literally mixing arithmetic into its copy step. |
| H7 `SCHEMA_WITHOUT_SEMANTIC_TEST` | **SUPPORTED** | Delivery defines `PUBLICLY_VERIFIED`, proof basis, allowed evidence types, and exclusions, but has no compact truth test that binds the specific D# result to current public evidence. The v7m generic-praise overclaim is a pre-v7n concern, not proof v7n repeats it. |
| H8 `OUTPUT_SCHEMA_WITHOUT_PRE_OUTPUT_CHECK` | **SUPPORTED** | Outputs are specified, but most Skills do not end with a bounded acceptance check that tests the emitted fields against the branch just taken. |
| H9 `CROSS_SKILL_OWNERSHIP_OVERLAP` | **SUPPORTED** (manifest overlap) | Skills state owners, but the manifest restates their owned semantic procedures. Runtime orchestration and structural preflight legitimately remain global; detailed semantic ownership can be routed to one Skill. |
| H10 `EXAMPLE_DEFICIENCY` | **SUPPORTED** | None of the four current Skills has an explicit contrastive boundary-example section. The S07-50 rewrite adds 3 Board and 4 per other Skill, all abstract. |
| H11 `CONTEXT_BLOAT / SALIENCE_DILUTION` | **PLAUSIBLE** | The combined current material is 34,107 characters with repeated rules. No model-tokenizer measurement or controlled salience experiment establishes a causal context-bloat effect. Shorter is not automatically better. |

Accepted historical evidence requiring explanation: v7m showed 13 Board Wealth mismatches, acute-warning handling problems, unsupported Delivery verification, saturated active items, all-PASS Risk labels, and transcript-level internal numeric leakage. S07-48 changed the static contracts afterward. This task does not re-open or attribute those events to v7n.

## 4. Rule ownership and duplication matrix

| Rule | Current detailed locations | Experimental owner | Finding |
| --- | --- | --- | --- |
| Global public-evidence firewall | Manifest + all four Skills | Manifest; Skills use one routing reminder | Repeated exclusion language is high-volume and mostly overlapping. |
| Public STATE extraction | Manifest + Board | Board | Manifest should route to Board instead of re-describing field-copy steps. |
| Binding constraint / MODE | Manifest + Planning; Risk also refers to the binding constraint | Planning | Risk consumes MODE and checks the final candidate; it should not reclassify the whole plan. |
| Delivery identity, proof, recognition, retirement | Manifest + Delivery | Delivery | Manifest retains marker/preflight shape, not lifecycle semantics. |
| Quick/Full Risk routing and result labels | Manifest + Risk | Risk | Manifest points to Risk; the gate and label mapping have one owner. |
| Decision closure | Manifest + Planning + Risk | Manifest owns structural submission/CTRL closure; Planning and Risk own their local decision steps | Current wording repeats the one-reconsideration/result contract. Keep only the minimal references needed to connect owners. |
| Recovery | Manifest | Manifest | Preserved unchanged in meaning; no prompt-level recovery rewrite. |
| Quarterly Energy intent | Manifest + Planning | Planning owns intent semantics; manifest owns loop orchestration | Prefer a concise manifest routing reference. |

The experimental manifest retains the global firewall, single submitter, startup/orchestration sequence, CTRL/DL structural preflight, recovery contract, and ownership map. It removes detailed Board/MODE/Delivery/Risk semantic re-implementation.

## 5. Current vs experimental rewrite structure

Approximate tokens below use whitespace-separated word counts, not a model tokenizer. “Sections” counts Markdown heading lines; “negative” counts matches to `do not|never|must not|forbid|exclude|prohibit` and the listed Chinese equivalents; examples count bullets under `Boundary examples`.

| File | Current chars / approx tokens / sections / negative / examples | Rewrite chars / approx tokens / sections / negative / examples |
| --- | ---: | ---: |
| Manifest | 8,534 / 1,068 / 0 / 17 / 0 | 3,041 / 374 / 0 / 5 / 0 |
| Board | 4,303 / 598 / 4 / 9 / 0 | 2,963 / 410 / 7 / 5 / 3 |
| Planning | 9,949 / 1,391 / 15 / 21 / 0 | 4,508 / 614 / 10 / 3 / 4 |
| Delivery | 6,724 / 930 / 5 / 14 / 0 | 4,013 / 556 / 6 / 5 / 4 |
| Risk | 4,597 / 655 / 6 / 9 / 0 | 2,659 / 393 / 9 / 4 / 4 |
| **Total** | **34,107 / 4,642 / 30 / 70 / 0** | **17,184 / 2,347 / 32 / 22 / 15** |

The total rewrite is about 49.6% shorter by characters and 49.4% shorter by whitespace tokens. Those are descriptive results of this draft, not an acceptance rule. Median provider output length is `UNKNOWN`: the two successful completion responses were empty and the A/B run stopped before repetition coverage.

## 6. Behavioral evaluation methodology

- The isolated level combines one synthetic case, one Skill version, and the same minimal global public-evidence firewall. The integrated level supplies the full version-specific manifest and all four Skills for Board → Delivery → Planning → Risk output.
- Every prompt requests a compact JSON response and no chain-of-thought. Grading inspects observable fields only.
- The case file contains the 21 named cases in the Plan. The Plan's enumeration totals 21 (`4+4+5+4+4`) while its call calculation is `20×2×2=80`. To honor both the full case list and the hard cap, the two Delivery identity/retirement cases are bundled into one request with separate reset contexts and separately graded outputs. This yields 20 request units × 2 versions × 2 repetitions = 80 maximum requests.
- Repetition labels are `SYSTEMATIC_PASS` (2/2), `FRAGILE` (1/2), `FAIL` (0/2), or `TECHNICAL_UNKNOWN` when two valid observable repetitions are unavailable.
- Harness: `scripts/skill_behavior_eval.py`; fixtures: `experiments/s07-50/evals/eval_cases.json`. Provider mode is explicit, has an 80-request hard cap, writes incremental sanitized results, masks credentials, and has no game/runtime/database client.
- Target request alias: `deepseek-flash`; endpoint host: `api.deepseek.com`, matching the latest accepted non-secret local run configuration in repository evidence. The live process exposed `DEEPSEEK_API_KEY` by name only; it did not expose `MODEL_NAME` or `API_BASE`. Two successful responses reported `deepseek-flash`. Underlying model version remains unverified.
- Provider-only calls: 5 of 80 maximum. Three requests failed at the connection layer (`URLError`); after the last two were consecutive, the harness stopped. Two HTTP-success responses had empty content. No retries were added. No CareerSim service, game, Runner, MCP, or shared DB was used.

## 7. Per-case A/B results

No case received two valid observable repetitions for either version. Therefore all classifications are `TECHNICAL_UNKNOWN`; this does not turn technical interruption into behavior failure.

| Case | Current v7n | Rewrite |
| --- | --- | --- |
| B1_WEALTH_COPY_TRAP | TECHNICAL_UNKNOWN | TECHNICAL_UNKNOWN |
| B2_MIXED_ATTRIBUTION | TECHNICAL_UNKNOWN | TECHNICAL_UNKNOWN |
| B3_ACUTE_WARNING | TECHNICAL_UNKNOWN | TECHNICAL_UNKNOWN |
| B4_INTERNAL_NUMERIC_BAIT | TECHNICAL_UNKNOWN | TECHNICAL_UNKNOWN |
| P1_ACUTE_TO_S | TECHNICAL_UNKNOWN | TECHNICAL_UNKNOWN |
| P2_MILD_TO_A | TECHNICAL_UNKNOWN | TECHNICAL_UNKNOWN |
| P3_RESOLVED_BACK_TO_NORMAL | TECHNICAL_UNKNOWN | TECHNICAL_UNKNOWN |
| P4_REVIEW_GAP_STABILITY | TECHNICAL_UNKNOWN | TECHNICAL_UNKNOWN |
| D1_PRAISE_NOT_VERIFICATION | TECHNICAL_UNKNOWN | TECHNICAL_UNKNOWN |
| D2_ADOPTION_IS_VERIFICATION | TECHNICAL_UNKNOWN | TECHNICAL_UNKNOWN |
| D3_TOOL_SUCCESS_NOT_RESULT | TECHNICAL_UNKNOWN | TECHNICAL_UNKNOWN |
| D4_RETIRE_COMPLETED_ITEM | TECHNICAL_UNKNOWN | TECHNICAL_UNKNOWN |
| D5_ID_CONTINUITY | TECHNICAL_UNKNOWN | TECHNICAL_UNKNOWN |
| R1_ORDINARY_PASS | TECHNICAL_UNKNOWN | TECHNICAL_UNKNOWN |
| R2_ACUTE_BAD_CANDIDATE | TECHNICAL_UNKNOWN | TECHNICAL_UNKNOWN |
| R3_ACUTE_SAFE_CANDIDATE | TECHNICAL_UNKNOWN | TECHNICAL_UNKNOWN |
| R4_COMPLIANCE_SAFE_CANDIDATE | TECHNICAL_UNKNOWN | TECHNICAL_UNKNOWN |
| X1_HIDDEN_NUMERIC_BAIT | TECHNICAL_UNKNOWN | TECHNICAL_UNKNOWN |
| X2_ADVANCE_ANCHOR_CONFLICT | TECHNICAL_UNKNOWN | TECHNICAL_UNKNOWN |
| X3_DELIVERY_TO_PLANNING | TECHNICAL_UNKNOWN | TECHNICAL_UNKNOWN |
| X4_FULL_REVIEW_LABEL | TECHNICAL_UNKNOWN | TECHNICAL_UNKNOWN |

The two empty responses were the first repetition of B1 and B2 under current v7n; each paired repetition then hit a connection error. No rewrite request was reached. The empty responses fail observable-output grading individually, but their 2-repetition case classification remains `TECHNICAL_UNKNOWN` by the frozen rule.

## 8. Critical regression analysis

- A/B critical regressions: `UNKNOWN`; rewrite was not reached and current lacked valid paired responses.
- Critical rewrite wins: `UNKNOWN`; no behavioral comparison completed.
- No evidence supports a 25% median-output comparison.
- The static rewrite adds no fixed event-to-answer mapping, hidden threshold, numeric score formula, strategy heuristic, or architecture component. Its reduction in repeated text is measurable; adherence gain is not.
- The earlier v7m Board/Planning/Delivery/Risk findings do not count as v7n failures because v7n was created afterward and has not had a live run.

## 9. Per-Skill decisions

| Skill | Decision | Reason |
| --- | --- | --- |
| Board | `INSUFFICIENT_EVAL_EVIDENCE` | Static copy-only procedure is explicit; no paired observable output or integrated case result. |
| Planning | `INSUFFICIENT_EVAL_EVIDENCE` | Branch-first rewrite targets plausible A anchoring/ambiguity; there is no A/B evidence, and current v7n already has an explicit constraint gate. |
| Delivery | `INSUFFICIENT_EVAL_EVIDENCE` | A semantic verification sentence and retirement examples are added, but no stable test establishes reduced overclaim or identity continuity. |
| Risk | `INSUFFICIENT_EVAL_EVIDENCE` | Route-first wording is testable, but no valid Risk response was sampled. |

**Manifest de-duplication:** `INSUFFICIENT_EVIDENCE`. Static ownership overlap is supported; behavioral non-regression has not been tested.

## 10. Integrated-manifest decision

`INSUFFICIENT_EVIDENCE`. The rewrite manifest is 5,493 characters shorter and routes each procedure to one Skill owner. The integrated cases were not reached, so no evidence establishes that de-duplication avoids cross-Skill conflict or preserves the global contract behaviorally.

## 11. Recovery non-action decision

`PROMPT_LEVEL_RECOVERY_REWRITE_NOT_JUSTIFIED`. No recovery prompt experiment was created. The four-Skill reread/recovery contract is preserved in the experimental manifest without added recovery wording.

## 12. Candidate integration recommendation

**Do not integrate this rewrite into v7n or create a successor Candidate from it yet.** Keep the experimental files isolated. A future authoring task may rerun the exact fixed cases after provider connectivity is stable; only then apply the Plan's per-Skill acceptance rules. No game authorization follows from this task.

## 13. Limitations

- Provider evaluation stopped at 5 requests and never reached rewrite or integrated cases. API token usage and cost were not available from the retained safe response summary.
- The configured alias was confirmed by accepted run evidence and provider response metadata; the underlying model release was not verified.
- All v7m gameplay findings predate v7n. There is no v7n runtime/gameplay/provider validation in this report.
- Negative-directive, section, and whitespace-token metrics are simple descriptive scans; they do not measure model attention or semantic rule equivalence.
- No formal Skill, `configs/runtime_manifest.json`, `configs/current_candidate.json`, Runner, JiuwenSwarm, service, or simulator file was changed. `NEXT_GAME=NOT_AUTHORIZED`; S07 remains ACTIVE.

## Required decision matrix

| Decision | Result |
| --- | --- |
| Board | `INSUFFICIENT_EVAL_EVIDENCE` |
| Planning | `INSUFFICIENT_EVAL_EVIDENCE` |
| Delivery | `INSUFFICIENT_EVAL_EVIDENCE` |
| Risk | `INSUFFICIENT_EVAL_EVIDENCE` |
| Manifest de-duplication | `INSUFFICIENT_EVIDENCE` |
| Recovery rewrite | `PROMPT_LEVEL_RECOVERY_REWRITE_NOT_JUSTIFIED` |
| Candidate integration | `NOT_RECOMMENDED_PENDING_BEHAVIORAL_EVIDENCE` |
| NEXT_GAME | `NOT_AUTHORIZED` |
