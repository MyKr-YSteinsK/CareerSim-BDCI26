# S08-05 — Score Gap and Compression-Resilient Policy

## 1. Result

- Status: `COMPLETE` for offline evidence analysis, bounded Candidate patch, and static validation.
- Primary decision: `V7P_READY_FOR_GAME_GATE`.
- Candidate: `candidate-v7p-score-gap-convergence`.
- No provider, network probe, service, install/reload, MCP, shared DB, Runner, or game action occurred.
- `NEXT_GAME=NOT_AUTHORIZED`. A separate Main decision is required before any v7p run.

## 2. Identity

- Repository: `MyKr-YSteinsK/CareerSim-BDCI26`.
- Branch/base: `main@3fd64bead5600c2f0bab677e7b832fe3678bdf12`.
- Parent: `candidate-v7o-execution-persistence-convergence`.
- Frozen Runner: `f61c738c72e51b77298cc1c14c7c6ebf4b6c527d`.
- Architecture remains Single Agent + four Skills; no Runner, dependency, local retry, Delivery, Board, or Risk change.
- Accepted evidence: committed [v7o Run #1 report](../runs/v7o-run1-validation.md), public `events.jsonl`, and allowlisted `post_run_summary.json` in `artifacts/dev-runs/s08-run01-v7o/`. The report records the event file SHA-256 as `b6eb500f9e8ad3966e595e65a5d558c2c8b50097bf908fd8b93a1b5f14567df4` and the summary SHA-256 as `f0961f094132a09a44cadcc32b6cc50e11c086e3612cc89276d749f8b8c54067`.
- The transcript's free-form reasoning was not used. Event review used only public event text, legal choices, selected public choices, public status fields, and action markers; compressor correlation used timestamps only. No hidden numeric state was read or used to design policy.

## 3. v7o Score Gap Decomposition

The participant-facing development score mapping and public terminal state reproduce the result within rounding. Component values below are approximate where marked; the Risk-Control component is an **inference from the public score mapping**, not a hidden Risk observation.

| Dimension | v7o weighted | v6 weighted | v7o − v6 |
|---|---:|---:|---:|
| Level | 15.00 | 18.00 | -3.00 |
| Wealth | 10.75 | 9.88 | +0.87 |
| Resilience | 14.25 | 12.75 | +1.50 |
| Skill | 15.00 | 15.00 | 0.00 |
| Risk Control | ~8.00 | 10.00 | ~-2.00 |
| Network | 8.83 | 9.67 | -0.84 |
| **Total** | **71.83** | **75.29** | **-3.46** |

Displayed component rounding may make the row sums differ from the reported totals by 0.01. The main deficits are the missing L6 promotion, the inferred Risk-Control component, and Network. Wealth and Resilience offset part of the gap; Skill already contributes its saturated direct-score value under the accepted public mapping.

`OFFLINE_SCORE_BUDGET_HYPOTHESIS`: an L6 public endpoint with a stronger Risk-Control component and higher Network, Wealth, and Resilience could approach 80 under the historical decomposition. This is offline planning intuition only; no exact score weight, threshold, target, or hidden rule was added to runtime policy.

## 4. v6 / v1 / v7g Reference Comparison

| Run | Public result | Main-action pattern | Use in this review |
|---|---|---|---|
| v6 #1 | 75.29 / 52.70 / 48m / A; L6 | Key project 14/16 overall; 7/9 from M24–M48; low-profile at M27 and M45 | Descriptive high-score comparison; see [v6 report](../runs/v6-run1-validation.md). |
| Candidate v1 #1 | 76.04 / 53.23 / 48m / A; L6 | Key project 16/16 | High-score reference; public trajectory summarized in [S07-16](S07-16_PUBLIC_TRAJECTORY_DIFFERENTIAL_REVIEW.md). |
| v7g #1 | 54.52 / 38.17 / 48m / C; L5 | Key project 16/16 | Counterexample: frequency alone is not sufficient; see [v7g report](../runs/v7g-run1-validation-r2.md). |
| v7o #1 | 71.83 / 50.28 / 48m / A; L5 | Key project 10/16 overall; 3/9 from M24–M48 | Current accepted evidence; not a causal control. |

The cross-run pattern supports a general directness prior, not a fixed key-project answer. Runs are unpaired and differ in events, opportunities, and policies; neither a Main-action count nor one endpoint proves causality.

## 5. M24–M48 Main Action Audit

All nine listed actions used `MODE=A`; each CTRL `G` remained `visible-win`. The public review feedback and current event do not explain why the agent selected each mentor or rotation option. That choice-specific rationale is `UNKNOWN` from the participant-visible record.

| Month | Level | Latest formal review | Main action | Next observed promotion checkpoint |
|---:|---|---|---|---|
| M24 | L4 | M24 B; no promotion; overall on target, no standout, no major issue | 建立导师关系 | M30: no promotion |
| M27 | L4 | M24 B | 建立导师关系 | M30: no promotion |
| M30 | L4 | M30 A; no promotion; broad direction to focus on output and relationships | 申请岗位轮岗 | M36: L4→L5 |
| M33 | L4 | M30 A | 申请岗位轮岗 | M36: L4→L5 |
| M36 | L5 | M36 A; L4→L5; positive feedback on key milestones and cross-group coordination | 申请关键项目 | M42: no level change |
| M39 | L5 | M36 A | 申请关键项目 | M42: no level change |
| M42 | L5 | M42 A; no promotion; broad output/relationship direction | 申请关键项目 | M48: no L6 |
| M45 | L5 | M42 A | 建立导师关系 | M48: no L6 |
| M48 | L5 | M48 A; no promotion | 建立导师关系 | Final checkpoint; no L6 observed |

There is no participant-visible feedback specifically naming Network or breadth as the primary deficit. The M30/M42/M48 direction mentions output and relationships broadly; the M36 review identifies strengths, not a specific missing requirement. In the final M42→M48 window, a key project was selected at M42, followed by mentor actions at M45 and M48 while `MODE=A`; the final review showed no L6. This supports a general preference for the most direct observable progression option when feedback is non-specific, but does not prove a key project would have produced a promotion.

## 6. Review Gap Specificity Audit

The first post-review `G/P` was `visible-win/A` at every checkpoint. Each was `GENERIC_GAP_WITH_NON_SPECIFIC_FEEDBACK`: feedback either said to convert activity into wins, gave broad direction, or praised observed strengths without naming a concrete missing capability. None was a specific Network/breadth deficit.

| Review | Public grade / outcome | Feedback characterization | First subsequent `G/P` | Classification |
|---:|---|---|---|---|
| M6 | C; promotion L1→L2 | Progress, collaboration, and risk awareness mentioned without identifying a concrete deficit; “busy, not winning” was broad. | Action #21: `visible-win/A` | `GENERIC_GAP_WITH_NON_SPECIFIC_FEEDBACK` |
| M12 | B; promotion L2→L3 | Same broad “busy, not winning” direction; no concrete primary gap. | Action #47: `visible-win/A` | `GENERIC_GAP_WITH_NON_SPECIFIC_FEEDBACK` |
| M18 | B; promotion L3→L4 | Same broad direction; no concrete primary gap. | Action #73: `visible-win/A` | `GENERIC_GAP_WITH_NON_SPECIFIC_FEEDBACK` |
| M24 | B; no promotion | Overall on target; no standout or major issue; mention bottlenecks early. | Action #99: `visible-win/A` | `GENERIC_GAP_WITH_NON_SPECIFIC_FEEDBACK` |
| M30 | A; no promotion | Meet expectations; focus broadly on output and relationships; review another level in six months. | Action #124: `visible-win/A` | `GENERIC_GAP_WITH_NON_SPECIFIC_FEEDBACK` |
| M36 | A; promotion L4→L5 | Positive notes on key milestones and cross-group coordination; no stated deficit. | Action #148: `visible-win/A` | `GENERIC_GAP_WITH_NON_SPECIFIC_FEEDBACK` |
| M42 | A; no promotion | Broad output/relationship direction; no named primary deficit. | Action #174: `visible-win/A` | `GENERIC_GAP_WITH_NON_SPECIFIC_FEEDBACK` |
| M48 | A; no promotion | Broad output/relationship direction; no concrete next-window deficit. | Action #200: `visible-win/A` | `GENERIC_GAP_WITH_NON_SPECIFIC_FEEDBACK` |

`REVIEW_GAP_ADHERENCE_FAIL` was not found because no review gave a concrete deficit that the run then collapsed into `visible-win`. However, retaining the generic label after non-specific feedback left no useful progression objective. v7p uses the neutral `DIRECT_PROGRESSION_EVIDENCE` gap in that case and preserves specific feedback when it exists.

## 7. M36 False-S / Compression Correlation

The four confirmed false-S actions were reconstructed from public event text, legal choices, selected choices, public H/D/W, CTRL markers, and scoped compressor timestamps only.

| Action | Public event / choice | Public H/D/W | CTRL `G/P/R/X` | Finding |
|---:|---|---|---|---|
| #150, M36 | “观察升职靠关系而非能力”; selected 回归技术路线 | 5 / 9 / 25 | `survival-stabilize/S/ALLOW/-` | No explicit public survival, safety, job-continuity, or affordability warning in this event. |
| #151, M36 | Quarterly Energy choice; selected 健康恢复 | 5 / 10 / 25 | `survival-stabilize/S/PASS/-` | Public prompt offered growth, reporting, relationship, and recovery options; no acute symptom was stated. |
| #152, M36 | Same quarterly Energy menu; selected 健康恢复 | 7 / 10 / 25 | `survival-stabilize/S/PASS/-` | Numeric H/D change alone did not establish a binding condition. |
| #153, M36 | Same quarterly Energy menu; selected 健康恢复 | 9 / 10 / 25 | `survival-stabilize/S/PASS/-` | Stabilization continued without a new public material warning. |

Classification: `FALSE_S_NOT_COMPRESSION_LINKED`. Five compressor markers were timestamped in the bounded run window. The marker immediately before the false-S sequence was at 12:04:08Z (M21); the first subsequent action was #87 eight seconds later. The M36 false-S actions occurred 410.9–427.4 seconds later, with 63–66 intervening action calls. The other three action-followed markers were at 12:15:11Z, 12:15:58Z, and 12:16:13Z, immediately before M45/M48 actions, after the false-S sequence. The fifth marker at 12:16:21Z had no subsequent action. Therefore there is no meaningful temporal correlation between the M36 false-S decisions and a nearby compressor marker.

Separately, four of the five compression windows followed by another action failed the required recovery tool order: two lacked a fresh observe and two had an observe but no four-Skill reread. The final marker has `UNKNOWN_NO_NEXT_ACTION`. This supports a compression-resilient manifest kernel through the current architecture evidence, not a claim that compression caused the M36 decisions. S07-42 found no deployable deterministic compressor callback/tool gate in the frozen submission; the kernel remains instruction-level and is not runtime enforcement.

## 8. Public-Risk Choice Audit

All 36 `R=ALLOW` actions were reviewed using the participant-visible event, legal choices, selected choice, and public context. The “public basis” is this offline reviewer's concise reading of those facts, not a recovered private reasoning trace.

| Action | Public event and legal choices (selected marked *) | Public basis | Risk | Category |
|---:|---|---|---|---|
| #2 | Client proposes clearly non-compliant venue and reimbursement; choices: *polite decline and return to normal hospitality / go and disguise expense / scold the client* | Preserves the client relationship while holding the compliance boundary. | ALLOW | `RISK_CONTAINMENT` |
| #4 | Forced ranking with a friend partly responsible for an incident; choices: *fact-based B / give friend A / give C / recuse* | Uses stated facts under a forced distribution. | ALLOW | `REASONABLE_TRADEOFF` |
| #6 | After redirecting the client, choices: *privately tell Leader for future arrangements / say nothing* | Records a boundary issue for safer future handling. | ALLOW | `RISK_CONTAINMENT` |
| #9 | Executive milestone briefing with an unresolved issue; choices: *lead with results and disclose risk/mitigation / hide risk / ramble through details* | Transparent risk reporting. | ALLOW | `RISK_CONTAINMENT` |
| #15 | Executive asks for worst case and resources; choices: *quantify public impact and request resources / give vague reassurance* | Answers the risk question directly. | ALLOW | `RISK_CONTAINMENT` |
| #18 | Client makes an uncomfortable joke about a colleague; choices: *deflect and help colleague / join in / sharply confront client* | Protects the colleague without escalating the room. | ALLOW | `RISK_CONTAINMENT` |
| #20 | Intern accidentally emails a complaint to the department; choices: *accompany her to apologize / falsely claim account theft / ignore / check recall window* | Chooses prompt, truthful repair. | ALLOW | `RISK_CONTAINMENT` |
| #22 | After defusing the client's misconduct, choices: *inform Leader for future staffing/venue planning / say nothing* | Supports preventive handling after the immediate issue is contained. | ALLOW | `RISK_CONTAINMENT` |
| #23 | Senior colleague takes intern's work credit; choices: *raise contribution at review / privately ask for correction* / ask intern to handle it / avoid involvement | Seeks correction without public escalation first. | ALLOW | `RISK_CONTAINMENT` |
| #28 | Untested code is found in release merge; choices: *halt release and roll back* / ship and hope / quietly hotfix | Prevents an unsafe release. | ALLOW | `RISK_CONTAINMENT` |
| #29 | Explicit burnout signal; choices: *take leave and adjust workload* / keep overworking / disengage | Chooses recovery and support over continued deterioration. | ALLOW | `RISK_CONTAINMENT` |
| #30 | Emergency hotfix under a required process; choices: *follow process with a customer-impact fallback* / bypass process and complete it later | Preserves review, test, and rollback safeguards while reducing impact. | ALLOW | `RISK_CONTAINMENT` |
| #33 | Personal use of company equipment under unclear rules; choices: stop using work equipment / *ask Leader/compliance for written clarification* | Resolves policy ambiguity before continuing. | ALLOW | `RISK_CONTAINMENT` |
| #42 | Leader suspects the source of anonymous feedback; choices: *admit it and offer constructive detail* / deny and speculate about other sources | Transparency has personal exposure, but is constructive and consistent with the stated choice. | ALLOW | `REASONABLE_TRADEOFF` |
| #43 | Leader disputes the feedback; choices: *stand by the observation with limits and propose better information sharing* / retreat and praise overall management | Keeps the feedback calibrated rather than escalating or retracting it. | ALLOW | `REASONABLE_TRADEOFF` |
| #46 | New executive causes rumors; choices: *proactively sync Leader on the conversation* / continue normal delivery / privately cultivate executive contact | Chooses transparent internal coordination over political signaling. | ALLOW | `RISK_CONTAINMENT` |
| #49 | Critical dependency is late; choices: *formally escalate for a delivery commitment* / continue private coordination with a buffer | Makes the project risk visible before the executive review. | ALLOW | `REASONABLE_TRADEOFF` |
| #59 | Client misunderstands delivered scope; choices: clarify publicly in meeting / *send written clarification after* / stay silent | Corrects the scope in writing, though later than the live meeting. | ALLOW | `REASONABLE_TRADEOFF` |
| #68 | Follow-up to sensitive client outing; choices: *privately inform Leader for future arrangements* / say nothing | Preventive boundary documentation. | ALLOW | `RISK_CONTAINMENT` |
| #69 | Senior refuses to correct intern credit; choices: *send work records to Leader* / give up | Escalates with attributable evidence after private resolution failed. | ALLOW | `RISK_CONTAINMENT` |
| #70 | Explicit mental-health symptoms and medical advice; choices: *take medical leave and professional support* / continue without leave | Follows the public health advice despite project pressure. | ALLOW | `RISK_CONTAINMENT` |
| #73 | After leave and missed milestone; choices: *promote a psychological-safety check mechanism* / focus only on output recovery | Addresses a repeated team-level health risk. | ALLOW | `RISK_CONTAINMENT` |
| #81 | “Anonymous” survey requires employee login; choices: *truthful examples without abuse* / neutral praise / constructive feedback only | Gives bounded, factual feedback despite stated retaliation uncertainty. | ALLOW | `REASONABLE_TRADEOFF` |
| #82 | Leader suspects survey feedback; choices: *discuss concerns directly* / deny | Chooses a constructive discussion with some personal exposure. | ALLOW | `REASONABLE_TRADEOFF` |
| #83 | Junior bypasses review and causes a test outage; choices: *accept mentor responsibility* / publicly blame junior | Accepts accountability for supervision rather than shifting all blame. | ALLOW | `REASONABLE_TRADEOFF` |
| #84 | Acute heart symptoms after overtime; choices: *stop, rest, and seek care if needed* / push through | Responds to explicit physical symptoms. | ALLOW | `RISK_CONTAINMENT` |
| #86 | Leader asks to assign an incident to the junior; choices: sign blame draft / *write shared responsibility and process failure* | Preserves a more balanced incident record, with career tradeoff. | ALLOW | `REASONABLE_TRADEOFF` |
| #94 | Finds a public metric definition error before briefing; choices: *alert Leader and correct it* / email after / stay silent | Corrects a materially misleading external figure before presentation. | ALLOW | `RISK_CONTAINMENT` |
| #95 | After metric correction, choices: *explain the definition to VP* / say nothing | Completes transparent correction. | ALLOW | `RISK_CONTAINMENT` |
| #106 | High-risk/high-return project after keeping a cash buffer; choices: *take the project* / choose only steady work | Accepts a stated career tradeoff with a public buffer; no clear unsafe or compliance choice. | ALLOW | `REASONABLE_TRADEOFF` |
| #125 | Peer merge contains SQL injection risk; choices: *block merge until fixed* / merge and repair later / comment without blocking | Prevents a known security flaw from entering the codebase. | ALLOW | `RISK_CONTAINMENT` |
| #133 | Colleague posts identifiable internal architecture; choices: *report to security* / privately ask colleague to delete it | Uses the formal security path for potentially sensitive disclosure. | ALLOW | `RISK_CONTAINMENT` |
| #138 | Unannounced reorganization draft and a friend making a major purchase; choices: advise caution without revealing the document / *say the company is broadly stable* / disclose the direction secretly | Protects confidential information, but the selected reassurance could mislead; the public record does not establish whether the draft is settled or whether the statement is false. | ALLOW | `AMBIGUOUS` |
| #150 | Promotion appears relationship-driven; choices: continue relationship-building / *return to the technical path* | A career-priority tradeoff; no material public safety/compliance risk is shown. | ALLOW | `REASONABLE_TRADEOFF` |
| #160 | Departing colleague offers company project/customer files; choices: *refuse and use compliant handoff* / receive but not open / receive and report | Refuses custody of confidential business data. | ALLOW | `RISK_CONTAINMENT` |
| #189 | Former colleague asks for internal data; choices: *refuse and explain it is company property* / send a small amount / send extra | Holds the confidentiality boundary. | ALLOW | `RISK_CONTAINMENT` |

Counts: `RISK_CONTAINMENT=24`, `REASONABLE_TRADEOFF=11`, `AMBIGUOUS=1`, `PUBLIC_RISK_TAKING=0`. The bounded public audit found no clear selected action that the current Risk contract failed to contain. The Risk-Control score deficit therefore remains `UNKNOWN_CAUSE`; it is not attributed to hidden Risk. `skills/risk-review/SKILL.md` remains byte-identical.

## 9. Evidence Classification

- **FACT:** v7o completed 48 months at 71.83 / 50.28 / A and ended L5. The accepted run report supplies session and score-source validation.
- **FACT:** public M24–M48 Main choices were 4 mentor, 2 rotation, and 3 key-project actions; every one had `G=visible-win`, `P=A`.
- **FACT:** all four false-S actions are at M36 and followed a compressor marker only after 63–66 intervening actions; no nearby temporal association is supported.
- **FACT:** the public formal reviews do not identify a primary Network/breadth deficit; later guidance is broad or positive.
- **INFERENCE:** final-promotion, Risk-Control, and Network components account for the largest score gap under the historical participant-facing mapping. Risk Control is inferred, not a hidden-state observation.
- **INFERENCE:** directness after a non-specific review is a reasonable general ranking prior; one run cannot show that it improves score or promotion.
- **HYPOTHESIS:** a compact manifest-persistent critical kernel may reduce context-loss drift. The current model-instruction architecture cannot guarantee adherence.
- **UNKNOWN:** why the agent chose each M24/M27/M30/M33/M45/M48 action; whether any alternative would have promoted; the hidden cause of the Risk-Control difference; and whether v7p improves score.

## 10. Patch Decision

- **P1 — Implemented.** The M36 actions are not temporally linked to compression, but S07-42 plus repeated recovery-order failures show that detailed Skill rules are not deterministically enforced while the manifest identity persists. Added only a compact MODE/progression kernel to the manifest.
- **Recovery contract — Reframed.** Mandatory recovery runs only when a resume/compaction/recovery signal is actually presented. The manifest does not claim it can detect an unexposed compressor event. The persistent kernel applies independently; explicit reread remains best-effort.
- **P2 — Implemented.** All reviews left a generic `visible-win` gap despite non-specific feedback. Planning now names concrete public deficits when available and uses `DIRECT_PROGRESSION_EVIDENCE` when they are not.
- **P3 — Implemented.** Planning now prefers the most direct observable progression path over generic mentoring/role breadth, with the explicit Network/breadth and stronger-evidence exceptions. The rule is not month/action-specific.
- **Skill direct-score saturation — Implemented qualitatively.** Pure Skill growth is not preferred solely for direct terminal score when stronger public progression, Network, Wealth, or Resilience evidence exists. Skill remains useful when it supports a public review/progression need. No numeric saturation threshold was added.
- **P4 — Not implemented.** The bounded audit found no clear `PUBLIC_RISK_TAKING` selection; Risk remains unchanged.
- Board, Delivery, Runner, dependencies, local retry, and whole-game persistence contract remain unchanged.

## 11. v7p Delta

- Candidate: `candidate-v7p-score-gap-convergence`; parent: v7o.
- Strategy delta: `REVIEW_GAP_DIRECTNESS_AND_COMPRESSION_RESILIENT_KERNEL`.
- Manifest: always-on compact critical kernel; explicit best-effort recovery only for an actually presented signal; no claim of automatic host-event detection.
- Planning: specific feedback remains concrete; non-specific feedback becomes `DIRECT_PROGRESSION_EVIDENCE`; unresolved review goals prefer direct observable progression, with stated Network/breadth exception; qualitative Skill saturation insight is threshold-free.
- Single Agent, four Skills, whole-game persistence, Board/Delivery/Risk ownership, `max_retries=2`, and no hidden-field use remain unchanged.
- v7p has no gameplay, provider, runtime, survival, score, long-horizon, stable-80+, or transfer validation. All v7p validation flags are false.

## 12. Static Scenario Results

Deterministic semantic/contract checks cover all Plan scenarios. They are not LLM behavior evidence.

| Scenario | Expected | Static result |
|---|---|---|
| A. Numeric decline after compression, no explicit warning | `MODE=A`; numbers alone do not create S | Pass |
| B. Explicit acute symptom | Temporary `MODE=S` may be required | Pass; existing public-symptom contract preserved |
| C. Specific review feedback | Preserve the named deficit; direct progress outranks generic mentoring/rotation | Pass |
| D. Non-specific review feedback | Use `DIRECT_PROGRESSION_EVIDENCE`; invent no hidden requirement | Pass |
| E. Network-specific review feedback | Network/mentor option may outrank a project | Pass; explicit exception |
| F. Public compliance/trust risk | Risk gate still blocks material unsafe choices | Pass; Risk Skill unchanged |
| G. Whole-game persistence | Successful action → fresh observe → continue same execution | Pass; inherited contract tests retained |

Targeted static tests also validate Candidate identity, parent hashes, four-Skill package identity, action/recovery ordering, and the non-runtime evidence boundary.

## 13. Known Limitations

- The score decomposition relies on a historical participant-facing mapping and rounded components. It cannot identify the hidden cause of Risk-Control variation.
- Cross-run score/action differences are unpaired and do not establish causality. v7g rules out treating key-project frequency as sufficient.
- The four false-S decisions are not temporally linked to a nearby compression. The kernel is justified by architecture and behavior evidence, not a causal compression claim.
- The kernel and recovery rules remain model instructions; the frozen submission has no proven deterministic compression hook or pre-tool gate.
- The raw transcript was not used for reasoning; the prior accepted audit reported numeric HiddenRisk text matches there. Public event data and allowlisted summary fields were sufficient for this bounded analysis.
- No v7p live run occurred. Gameplay, provider behavior, score improvement, stable 80+, hidden-test transfer, and future recovery adherence remain unproven.

## 14. Next Game Gate Recommendation

`V7P_READY_FOR_GAME_GATE`

Recommend `READY_FOR_S08_RUN02_GAME_GATE` for Main review. This is a recommendation only: `NEXT_GAME=NOT_AUTHORIZED` until a separate gate explicitly authorizes one fresh v7p run.
