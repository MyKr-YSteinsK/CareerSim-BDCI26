# S05-02 unified offline evidence and adoption gate

All numeric score/headroom analysis below is **offline forensics**, never runtime Skill input. `OBSERVED` means recorded public trajectory, action selection, score report, or transcript text; a transcript's Agent reasoning is evidence of reasoning, not proof its claims or choice were correct. `INFERENCE` and `HYPOTHESIS` are not promoted to causality. No new game or provider call was used.

## Evidence identity and decision-time boundary

- Committed anchors: [S04-03 score comparison](../S04-03-score-directed-integrated-run/score_comparison.json), [Run #1 trajectory](../S04-04-high-score-confirmation/candidate_run1_trajectory.json), [Run #2 trajectory](../S04-04-high-score-confirmation/candidate_run2_trajectory.json), [two-run comparison](../S04-04-high-score-confirmation/two_run_comparison.json), [S04 closeout](../S04-CLOSEOUT/RESULT.md), and [S05-01 result](../S05-01-material-outcome-reprioritization/RESULT.md).
- Read-only raw supplements were identity-checked against the trajectories before inspection: Run #1 transcript `753385` bytes / SHA256 `49cbfcee32dd88d1573d4e0a068de543e3993d45384dc72854bfa91aaebfec71`; Run #2 transcript `312900` bytes / `9f3082d4decb46f8e64c6ff6df736900cf8d4810ff528d37ee3f0451581a66b0`; Run #2 events `1019202` bytes / `9a266a84937b40899b6f2fdcbbb8fdefd74c825e57dd1ea484e52c6e4b9e22b6`. Exact local paths are in the committed trajectory `source_artifacts`; raw files are not part of this commit.
- Run #2 M18 state below was extracted from the **last Month-18 `observe` result** in the verified events file, not from the later terminal score. At each hypothetical decision, later months/terminal results remain unavailable inputs.

## A1 — Energy / composite-benefit decision quality

| Class | Finding |
|---|---|
| `OBSERVED` | Run #1 selected `准备汇报材料` 25 times, `健康恢复` 11, `人脉维护` 6 and `处理历史埋雷` 3 across 16 quarters; main action was `申请关键项目` 16/16. Run #2's first seven quarters had prep `5` vs Run #1 `10`, health `7` vs `7`, network `5` vs `4`, cleanup `2` vs `0`; its M12 main action differed. These are selections, not isolated effects. |
| `OBSERVED` | Run #1 transcript lines 225, 1324 and 30970–30980 explicitly recognized that Dignity was already high while other benefits of composite options could remain useful, and compared resource cost. Run #2 early lines 515–525 also recognized this nuance; at M18 line 3595 it instead said to avoid actions *containing* a Dignity benefit because Dignity was full, although those options could also have public Output/Network benefits. |
| `INFERENCE` | A one-component-is-full shortcut can suppress a useful composite option; conversely, a multi-benefit label can hide Energy/opportunity cost. Run #2's actual M18 health/mitigation allocation may still have been defensible given its public warning. No counterfactual outcome is known. |
| `HYPOTHESIS` | At quarterly Energy choice, a short current-gap × still-useful-component × resource/opportunity-cost comparison can make both errors less likely. S05-01's one-line negative control already forbids nullifying a composite option, but does not yet require the full comparison. |
| `UNKNOWN` | Whether this reasoning inconsistency caused any lost score, whether the Agent will follow a new rule, and exact hidden effects. No action name or score weight is promoted to runtime policy. |

## A2 — High-score ceiling forensics

Run #1 `76.04`; target `80`; arithmetic gap `3.96`. Headroom is `weight × (100 − observed normalized)` from the committed S04 score dimensions, a theoretical score decomposition, **not** a reachable-action forecast.

| Dimension | Weight | Run #1 normalized / weighted | Theoretical weighted headroom |
|---|---:|---:|---:|
| Level | 0.30 | 60 / 18.00 | 12.00 |
| Wealth | 0.20 | 50.62 / 10.12 | 9.88 |
| Resilience | 0.15 | 95 / 14.25 | 0.75 |
| Skill | 0.15 | 100 / 15.00 | 0.00 |
| Risk control | 0.10 | 100 / 10.00 | 0.00 |
| Network | 0.10 | 86.67 / 8.67 | 1.33 |

- `OBSERVED`: First L4 was M18, first L5 M36, first L6 M48. M18→M36 public state: Skill `44→100`, Network `19→36`, Output `16→29`, Wealth `6→21`, Health `10→9`; M24→M36 Network was `36→36` and Output `26→29`. M36→M48: Skill `100→138`, Network `36→51`, Output `29→40`, Wealth `21→39`, Health `9→9`. Skill's final normalized score was already 100, despite continued public raw Skill growth.
- `INFERENCE`: Level is among the largest offline headroom dimensions and the M18–M35 lack of a new level is a visible objective-specific progression gap, not a claim that all growth stopped. Repeating the same main action throughout is a decision signal worth reviewing, not proof it caused the gap.
- `UNKNOWN`: Wealth rose throughout both level-stable and promotion periods; no committed evidence decomposes salary/bonus, story choices, level timing, and independent income well enough to favor a specific income action. Level/Wealth headroom may not be achievable in one run or with the current legal menu. Network headroom is small in Run #1, but its path-specific role in promotion remains unknown.
- `REJECTED`: Do not place evaluator weights, a score-to-80 rule, or a fixed action recipe into runtime Skills. Resilience/Risk had little theoretical Run #1 headroom, but this does not justify ignoring survival risk in another run; Run #2 eliminated at M25.

## A3 — Growth consistency, same-month public snapshots

Format in state cells: `Level / Skill / Network / Output / Health / Wealth`. Run #1 uses committed monthly public states; Run #2 M6/M12/M24 match committed milestones and M18 comes from the verified last M18 `observe`. Energy entries are selected actions at that quarter, not proven state causes. The M24 comparison excludes Run #2's later terminal result as a decision input.

| Month | Run #1 state; Energy; main | Run #2 state; Energy; main | Feedback / divergence class |
|---|---|---|---|
| M6 | `L2/13/5/6/7/2`; Health×2 + Prep; Project | `L2/12/5/6/10/2`; Network×2 + Prep; Project | Both reached L2; M6 C feedback is reported in planning records. Health gap and allocation differ. `RESOURCE_ALLOCATION_SIGNAL + MIXED`; no isolated effect. |
| M12 | `L3/24/7/7/7/4`; Health×2 + Prep; Project | `L3/24/8/10/9/3`; Network×2 + Health; Low-profile | Both L3; Run #2 later B feedback is recorded. Different main choice, resource mix and event paths. `AGENT_DECISION_SIGNAL + RESOURCE_ALLOCATION_SIGNAL + EVENT_PATH_DIFFERENCE + MIXED`. |
| M18 | `L4/44/19/16/10/6`; Prep×2 + Network; Project | `L3/42/19/11/10/7`; Health + Cleanup; Project | Run #1 reached L4; Run #2 had M18 B/article opportunity in its transcript yet remained L3. `OPPORTUNITY_UTILIZATION_SIGNAL` is only a question; `EVENT_PATH_DIFFERENCE + MIXED`, relative contribution `UNKNOWN`. |
| M24 | `L4/63/36/26/8/10`; Prep×2 + Network; Project | `L4/43/19/13/10/9`; Health + Cleanup; Project | Run #2 first reached L4 at M24. Growth dimensions diverged despite same main-action label. `RESOURCE_ALLOCATION_SIGNAL + EVENT_PATH_DIFFERENCE + MIXED`; no post-M24 terminal information used. |

`OBSERVED`: Run #1 chose Project in its first seven quarters; Run #2 matched `6/7`, differing at M12. Both had only three observed Planning checkpoints. `INFERENCE`: early main-action similarity does not identify Skill benefit; resources, narrative opportunities and promotion timing differ. `UNKNOWN`: relative agent-choice versus stochastic event-path contribution, precise feedback-to-promotion mechanism, and what an alternative choice would have caused. No M24 state delta is attributed to S05-01, which had not yet run.

## A4 — Skill / context responsibility audit

| Skill | Current duty and possible overlap | Boundary decision |
|---|---|---|
| Board | Session-keyed observed/inferred/unknown facts and freshness; its repeated structured sections appear in Run #2 transcript (S04-04 reports 37 mentions / 14 fielded sections). Could invite state restatement. | Keep. Freshness, session isolation, source/unknown separation and no action recommendation are safety-critical. Repetition is not proven to originate in the Skill contract rather than necessary refresh or Agent deliberation. |
| Planning | One objective and strategic trade-off, with a five-line checkpoint. Its `Observed gap` can duplicate a full Board if interpreted expansively; repeated-action rule currently lacks an explicit progress comparison in the output. | Keep only the relevant Board fact and add concise progress evidence to the existing line; do not create a second state record or longer review. |
| Risk | Warning-driven current-candidate review (`ALLOW/WARN/RECONSIDER/UNKNOWN`), not objective ownership. It also mentions opportunity cost, but only for the immediate candidate. | Keep unchanged. No evidence that Risk's marker or pre-action review caused the long strategic deliberation or systematically suppressed growth. |
| Trace | Existing S02 marker and same-Agent submission path only; no strategy or state. | Byte-identical. No correctness defect found; do not change marker or authority. |

`OBSERVED`: Raw transcripts include extended option re-review and repeated state prose, while compact S04-04 reports only three Planning checkpoints in each run. `INFERENCE`: forcing a full Board copy or extra Skill review could worsen context cost; attribution of long reasoning to any one Skill is `UNKNOWN`. Safety-critical text not to compress away: current game ID/freshness, public-only evidence, `UNKNOWN`, no hidden thresholds/weights, Single Agent authority, no duplicate action, and S05-01 severe-outcome reprioritization.

## Adoption gate — decision before Skill editing

`Orthogonality` is relative to existing v2-C, Board and Risk. `Observable` means a future authorized benchmark could see the behavior in current checkpoint/choices, not that it is already runtime-proven.

| Candidate mechanism | Evidence strength | Expected leverage | Orthogonality | Runtime observability | Context cost | Confound / failure mode | Decision and exact reason |
|---|---|---|---|---|---|---|---|
| E: Compare still-useful components against current public gaps and Energy/opportunity cost for legal composite choices | MEDIUM | MEDIUM | Yes; extends v2-C's negative control, not Risk/Board | HIGH at quarterly choices via compact `Path trade-off` | LOW | Agent may overvalue a multi-benefit label or overcorrect one saturated component | **ADOPT**: one verified reasoning inconsistency plus repeated public-resource decisions; can be expressed without hidden data, fixed option or new state. |
| G/O: Compare previous objective's intended public progress with fresh state before repeating a strategic path; record `advancing/stalled/unknown` in existing checkpoint | MEDIUM | HIGH but unproven | Yes; objective progress is distinct from v2-C severe consequence and Risk's candidate check | HIGH at quarterly/feedback checkpoints | LOW | False plateau if only Level is flat while objective-specific Output/Network rises; forced switching despite progress | **ADOPT**: M18–M35 level gap and repeated main action plus only early Planning checkpoints justify an explicit objective-specific comparison. Continued observed progress remains a valid reason to continue. |
| Board/Planning/Risk broad text consolidation | LOW | UNKNOWN | Mixed | LOW for isolated effect | Potentially lower | Removes freshness/unknown or changes multiple mechanisms at once | **DEFER**: no contract-level correctness defect or attributable context root cause; only keep Planning's output bounded while implementing E/G. |
| Dedicated wealth/income action heuristic | LOW | Potentially HIGH | Unclear | MEDIUM | MEDIUM | Confounds salary, promotion and story events; may require fixed action inference | **DEFER**: headroom is real, but public causal/action evidence is insufficient. |
| Risk threshold or risk-marker retuning | LOW | UNKNOWN | No | MEDIUM | MEDIUM | Could weaken accepted warning boundary; Run #2 use does not prove Risk failure | **DEFER**: current candidate-specific Risk contract remains intact. |
| Score-weight/hidden-counter optimization or fixed event answers | None as legal runtime evidence | UNKNOWN | No | LOW | HIGH | Leakage and FROZEN violation | **REJECT**: evaluator weights and post-game outcomes are offline analysis only. |
| Additional Skill, persistence framework, Team/Swarm | LOW | UNKNOWN | No | LOW | HIGH | Extra submitter/state and confounded benchmark | **DEFER**: no demonstrated role-separation bottleneck and out of scope. |

Adopt E and G/O only if their Skill wording remains public-only, legal-option-only, bounded, non-overlapping and passes R1–R10. The integrated candidate is a falsifiable **hypothesis**; both adoption decisions can fail in a future game without turning this offline gate into a performance claim.
