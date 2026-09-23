# S04-03｜Strategy Decision

## Evidence basis

- SCORE-01 committed evidence: `e4c88c253820ca4abc511c0ec7f73468674a0de7`.
- Raw events, transcript, and score-report source were read-only and matched the committed SHA256/byte inventory before analysis; details are in `score01_trajectory.json`.
- Event stream: one `new_game`, 98 `observe`, and 98 `take_action` calls; no second submitter is evidenced in the agent-mode run. All 98 action notes carry `[S02_SKILL_USED]`; risk-review markers occur 13 times: `ALLOW=8`, `WARN=4`, `RECONSIDER=1`.
- Across seven observed quarterly strategic decisions, the Agent chose `申请关键项目` all seven times. Energy use totaled 21 points: `准备汇报材料` 10, `人脉维护` 6, `健康恢复` 3, and `处理历史埋雷` 2.
- Public-state trajectory shows prolonged L1 tenure through the last observed month (23), Skill plateauing at 9 after month 6, low Network (usually 2–3), Output varying from -1 to 3, and an explicit C-performance / “观察名单” warning in the transcript after the first half-year review. At month 18, transcript reasoning records a D review with Health 3, Dignity 5, and Output -1; the Agent recognized the need to improve performance. At month 21, after recovery, it again chose the same main action.
- The final score report records elimination at month 24, grade D, quantitative score 33.06, and final Level raw 2 / Wealth 11.4 / Skill 9 / Network 2 / resilience 17 / risk-control raw 0. The transcript ends with `Game over: 炒鱿鱼`.
- Installed locked `career-emulator` 1.0.1 score source maps `risk_control` to `cumulative_risk_inverted`; raw 0 normalizes to 100. This describes the terminal cumulative-risk score field, not Risk Skill effectiveness. This implementation detail is for offline analysis only and is not encoded in the Skill.

## Action allocation counts

Counts below cover only the clearly classifiable quarterly allocation menu; they do not force mixed narrative-event choices into strategy categories.

- **Growth / promotion:** 7 of 7 quarterly main actions were `申请关键项目`.
- **Growth / visible output:** 10 Energy points went to `准备汇报材料`.
- **Network / relationships:** 6 Energy points went to `人脉维护`.
- **Resilience / recovery:** 3 Energy points went to `健康恢复`.
- **Risk avoidance:** 2 Energy points went to `处理历史埋雷`.
- **Wealth / income:** no quarterly allocation option directly targeted wealth; the final wealth result also reflects the public salary/bonus mechanics. Mixed compensation-story choices are retained in the turn timeline, not treated as a homogeneous income strategy.
- **Neutral / maintenance:** no Energy points were left unused; the 71 narrative-event choices have varied, event-specific effects and are not collapsed into one mechanical category.

## Elimination and score interpretation

The strongest supported pattern is long-term growth underinvestment plus weak adaptation to feedback, not a demonstrated Risk Skill failure. The Agent repeatedly discussed growth but did not keep a compact objective that forced review of progress and choice diversity. After negative performance feedback, it spent the month-18 Energy budget on two Health recoveries and one report-preparation action—understandable given Health 3—then returned to `申请关键项目`; at month 21 it again selected that action despite its own deliberation noting repeated use without promotion. This is a planning hypothesis, not proof that another legal choice would have scored better.

The exact firing sequence remains `UNKNOWN`: the machine-readable score report has no termination reason, while the transcript's final Agent-generated recap gives an internally inconsistent performance sequence. The observed terminal label is `炒鱿鱼`, and the public handbook describes termination after consecutive D reviews; the raw committed evidence does not independently preserve every half-year result in a structured field. Do not claim a specific review sequence or sole causal action.

The poor growth dimensions are directionally consistent with the trajectory: final Level 2 after long observed L1 tenure; Skill 9 with no visible progress after month 6; Network 2; and Wealth 11.4 after prolonged time at the lowest observed level. Resilience contributed strongly (17), while cumulative-risk raw 0 contributed a perfect inverted dimension. The latter must not be read as proof of an effective risk policy.

## Risk-review behavior

`risk-review` loaded once and produced 13 marked uses. The single `RECONSIDER` aligned with a clearly public health constraint (Health 3 and a high-intensity on-call option); the Agent selected the directly relevant mitigation. Four `WARN` results left final choice with the Agent, consistent with the Skill contract. Eight `ALLOW` markers accompanied actions the Agent described as risk-mitigating. There is no evidence that risk-review repeatedly blocked a clearly superior growth option or was generally over-conservative. Its strategy effectiveness remains unproven from one game.

## Counterfactual candidates (not outcome claims)

1. **Month 9 mentoring decision:** The legal options were accepting a mentor assignment or declining due to workload. The public event disclosed both a prior incident by the trainee and an implied performance benefit. The Agent accepted; a bypassed review caused an incident the next month. A rolling plan could have made the workload / risk / visible-performance trade-off explicit before acceptance. Whether declining or accepting with stricter boundaries would score better is unknown.
2. **Month 21 quarterly main action:** The legal menu included `申请关键项目`, `向领导汇报成果`, `主动曝光成果`, `建立导师关系`, and other choices. The Agent's own transcript notes it had repeated the key-project action several times without a promotion, debated alternatives at length, then chose it again. A progress-based review and concise comparison might have produced a more informed choice; no alternate outcome is asserted.
3. **Month 18 recovery allocation:** After a D review, Health 3, Dignity 5, and Output -1 were visible. The Agent chose two Health recoveries and one report action, a defensible survival response but one that left little short-term growth budget. A rolling plan should balance these simultaneous constraints and then reassess after recovery; the evidence does not prove a different allocation was safer or more effective.

## Hypothesis ranking

| Candidate | Evidence strength | Expected score leverage / breadth | Simplicity / observability | Survival, token, and one-run considerations | Decision |
|---|---|---|---|---|---|
| H1 Rolling Planning | High: repeated quarter choice, delayed response to feedback, and lengthy oscillation are directly visible | High / broad across level, skill, network, output, wealth, and resilience trade-offs | Medium / high; one concise Skill, exercised at quarterly and feedback checkpoints | Medium survival risk if misapplied; bounded output and no fixed growth-first rule; high one-run information value | **Primary** |
| H2 Growth-vs-Risk Rebalance | Low–medium: one health-related `RECONSIDER`; other uses did not establish systematic suppression of growth | Low–medium / concentrated on risk choices | Low patch size, but changing a working risk contract could confound the run | Could increase survival risk; unclear signal in one run | Reject for this task |
| H3 Score-Relevant State Prioritization | Medium: state gaps were visible and sometimes recognized, but were not consistently turned into a revised objective | Medium / broad | Low–medium; would change the State Board's fact-organizing role toward priority-setting | Lower direct risk, but would blur board/planning responsibilities and test the same mechanism less directly | No coupled change |

## Decision

- **Primary Hypothesis:** H1 — Rolling Planning.
- **Secondary adjustment:** None. Keep `career-action-trace`, `risk-review`, and `structured-state-board` unchanged so the single run tests one new strategy mechanism.
- Add one `rolling-planning` Skill. Invoke it only at new-game setup, quarterly Energy/main-action decisions, material performance/state feedback, and when an intended public metric is not progressing after repeated action. It stores one bounded same-session checkpoint, compares only legal options, and never submits actions.
- The Skill uses qualitative public-state goals only. It contains no hidden thresholds, internal score weights, cross-run evidence, or guaranteed-outcome claim. At least three representative strategy checkpoints, if present in the sole game, will be verified through actual Skill load/use evidence.
- This is a directional strategy experiment. It does not establish causality, score improvement, or generalization.
