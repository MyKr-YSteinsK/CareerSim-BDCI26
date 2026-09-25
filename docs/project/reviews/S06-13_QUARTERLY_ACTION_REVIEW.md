# S06-13｜季度 Energy 与 Main Action 资源配置深挖

## 1. Source scope and decision boundary

- Base: `685ddc416656062b173708e875c99b9e234bea93`; fetched `origin/main` matched local `main`. Initial worktree was clean.
- Candidate: `candidate-v5-evidence-driven-phase-policy`; Single Agent + three Skills. This review does not edit the candidate or authorize a game.
- Scope: current project facts, committed compact trajectories from Git history, and read-only inspection of the frozen installed simulator / public Dev fixed-action data.
- Live operations: provider `0`; Jiuwen service `0`; install/reload `0`; MCP `0`; gameplay `0`.
- Repository changes: only this review document. No current state, strategy evidence, run history, config, Skill, Runner, dependency, runtime, DB, or raw file changed.

Evidence labels: `DEV_CONFIRMED`, `RUN_OBSERVED`, `MULTIRUN_OBSERVED`, `DERIVED_DEV_ANALYSIS`, `HYPOTHESIS`, `UNKNOWN`, and `DO_NOT_ENCODE`. A menu effect is not proof of a realized or causal effect; across-quarter differences include story actions and monthly processing unless stated otherwise.

### Source identities

| Evidence | Exact identity used | Boundary |
|---|---|---|
| Current facts | Base-tree `docs/project/CURRENT_STATE.md`, `RUN_HISTORY.md`, `STRATEGY_EVIDENCE.md`, `OFFICIAL_SOURCE_LOCK.md`, and accepted S06-11/S06-12 reviews | Current v5 is static; S06 gameplay effectiveness and stable 80+ remain unproven. |
| Frozen simulator / data | Root `.venv` metadata: `career-emulator 1.0.1`, `career-emulator-bdci26 1.0.0`, `jiuwenswarm 0.2.4b3`. Dev package and simulator-materialized copies of `energy_event.data` match at SHA256 `4765fae0518e31bdb5929bf2d25c3960d7ae9a83c6b446b34a091cff30630d1d`; `main_event.data` match at SHA256 `222a56c4472e9ee2afcb255faa11236fa02379917ca791cf67afcc89c3e34818`. | Exact versions match Source Lock. No event pool was loaded and no game/session instantiated. |
| Candidate v1 Run #1 | Git `66ec4af1e9a2a28da57c6cb8d409a6a38f87ae01:experiments/S04-04-high-score-confirmation/candidate_run1_trajectory.json`; blob `a9ca5d759b05dd0c9b3974c9a1398a3ca3990343` | File identifies source run as S04-03 Candidate Run #1; 16 quarter decisions and monthly public snapshots. |
| Candidate v1 Run #2 | Git `66ec4af1e9a2a28da57c6cb8d409a6a38f87ae01:experiments/S04-04-high-score-confirmation/candidate_run2_trajectory.json`; blob `85129980c0591f0ad4d4bee113562bc51116d16d` | Eight quarter action records and sparse milestones; no per-quarter pre-action state. |
| SCORE-01 | Git `7a055dea76580117ca74cddb49bb04efcf605eb1:experiments/S04-03-score-directed-integrated-run/score01_trajectory.json`; blob `0330ef9c95ea13b285a8fcfcf1b4c2c6e80ff65a`; internal run source commit `e4c88c253820ca4abc511c0ec7f73468674a0de7` | Seven quarter records and per-action pre-action state; run ended at Month 24. |
| S06 Run #1 | Git `c4dbe0ebc4e27aafc22c94050c69547113cdc8eb:experiments/S06-01-adaptive-controller-static/RESULT.md`; blob `7fb64c3fc357ed10c08bea112854efa6bcd81577`; also current `RUN_HISTORY.md` | Compact summary only: 16/16 main actions; quarterly Energy and state timeline unavailable. |
| v4 Run #1 | Current `docs/project/runs/v4-run1-health-forensic.md` and `RUN_HISTORY.md` | Q1 Energy and pre-Q2 terminal evidence are compacted and accepted; local raw files were not re-read. |

S04 raw events/transcripts were unavailable in the accepted prior review and were not searched or re-run. Compact evidence supports descriptive counts, not missing per-action states or causal effects.

## 2. Quarterly historical dataset

State shorthand is `L/S/N/O/H/D/W` = Level / Skill / Network / Output / Health / Dignity / Wealth. In the v1 #1 table, `next Q` is the next recorded quarter’s pre-Energy snapshot three months later. Stories, review processing, and other updates intervene, so interval changes are `AMBIGUOUS` as action effects. Its compact file does not record post-Energy or immediate post-Main state. SCORE-01 records state before each fixed action; `post-E` is the Main row’s pre-action state, after Energy and before Main. It still does not give an uncontaminated post-Main state.

| Run | Pre-quarter state | Energy sequence | Post-Energy | Main | Immediate post-Main | Next 3–6 month outcome |
|---|---|---|---|---|---|---|
| v1 #1 | All 16 states | All 16 sequences | UNKNOWN / not recorded | All 16 actions | UNKNOWN / not recorded | Next-quarter states below; composite and AMBIGUOUS attribution |
| v1 #2 | Mostly UNKNOWN | All 8 sequences | UNKNOWN / not recorded | All 8 actions | UNKNOWN / not recorded | Sparse milestones only; quarter-aligned outcome otherwise UNKNOWN |
| SCORE-01 | All 7 states | All 7 sequences | Recorded as pre-Main state below | All 7 actions | Not isolated; next observed state includes month processing/story | Next-quarter states below; composite and AMBIGUOUS attribution |
| S06 Run #1 | UNKNOWN | UNKNOWN | UNKNOWN | 16/16 Key project | UNKNOWN | Final 48-month result only; no quarter-aligned interval states |
| v4 Run #1 | Q1 Health=2; other dimensions not reproduced | Q1 sequence known | Health 2→4 directly observed; other fields incomplete | Q1 Key project | UNKNOWN | Terminal at M6 before Q2 Energy |

### Candidate v1 Run #1 — 16/16 quarters

| Q / Month | Pre-E state L/S/N/O/H/D/W | Energy sequence | Main | Review position | Next Q pre-E state (composite interval) |
|---|---|---|---|---|---|
| Q1 / M3 | L1/9/3/2/4/10/1 | Network + Report + Health | Key project | Before M6 review; promotion observed M6 | L2/13/5/6/3/10/2 |
| Q2 / M6 | L2/13/5/6/3/10/2 | Health + Report + Health | Key project | After M6 promotion to L2 | L2/20/7/6/5/9/3 |
| Q3 / M9 | L2/20/7/6/5/9/3 | Report + Health + Network | Key project | Before M12 review; promotion observed M12 | L3/24/7/6/3/10/4 |
| Q4 / M12 | L3/24/7/6/3/10/4 | Health + Health + Report | Key project | After M12 promotion to L3 | L3/35/14/12/10/10/6 |
| Q5 / M15 | L3/35/14/12/10/10/6 | Report + Network + Report | Key project | Before M18 review; promotion observed M18 | L4/44/18/14/10/10/6 |
| Q6 / M18 | L4/44/18/14/10/10/6 | Report + Report + Network | Key project | After M18 promotion to L4 | L4/57/28/17/7/10/8 |
| Q7 / M21 | L4/57/28/17/7/10/8 | Report + Report + Health | Key project | Before M24 review; no promotion at M24 | L4/63/35/25/8/10/10 |
| Q8 / M24 | L4/63/35/25/8/10/10 | Report + Report + Network | Key project | After missed M24 review; M30 also missed | L4/71/32/21/6/10/12 |
| Q9 / M27 | L4/71/32/21/6/10/12 | Risk cleanup + Health | Key project | Between missed M24 and M30 reviews | L4/82/36/26/8/10/15 |
| Q10 / M30 | L4/82/36/26/8/10/15 | Report + Report + Health | Key project | After missed M30; before M36 review | L4/90/36/25/9/10/17 |
| Q11 / M33 | L4/90/36/25/9/10/17 | Report ×3 | Key project | Before M36 review; promotion observed M36 | L5/100/35/27/9/10/21 |
| Q12 / M36 | L5/100/35/27/9/10/21 | Report + Report + Network | Key project | After M36 promotion to L5 | L5/106/47/33/10/10/25 |
| Q13 / M39 | L5/106/47/33/10/10/25 | Risk cleanup + Report | Key project | Before M42 review; no promotion at M42 | L5/115/54/38/9/10/30 |
| Q14 / M42 | L5/115/54/38/9/10/30 | Report ×3 | Key project | After missed M42; before M48 review | L5/127/54/38/7/10/34 |
| Q15 / M45 | L5/127/54/38/7/10/34 | Health + Report + Report | Key project | Before M48 review; promotion observed M48 | L6/138/51/40/7/10/39 |
| Q16 / M48 | L6/138/51/40/7/10/39 | Risk cleanup + Health | Key project | After M48 promotion to L6; horizon end | No next quarter |

The run completed 48 months with 76.04 quantitative / 53.23 competition partial / A. Promotions were observed at M6, M12, M18, M36, and M48; M24 and M30 were missed before M36 promotion. The compact feedback note is an early C / request for clearer Output; exact review alignment is `UNKNOWN`. Quarter-level changes cannot isolate Energy/Main effects from intervening stories.

### Candidate v1 Run #2 — eight reached quarters

| Q / Month | Pre-E state | Energy sequence | Main | Nearby record |
|---|---|---|---|---|
| Q1 / M3 | UNKNOWN | Report + Network + Health | Key project | No quarter-aligned milestone |
| Q2 / M6 | UNKNOWN | Network ×2 + Report | Key project | M6 milestone L2, S12/N5/O6/H10/D10/W2; promotion observed |
| Q3 / M9 | UNKNOWN | Health ×2 + Report | Key project | No quarter-aligned milestone |
| Q4 / M12 | UNKNOWN | Network ×2 + Health | Low-profile | M12 milestone L3, S24/N8/O10/H9/D10/W3; promotion observed |
| Q5 / M15 | UNKNOWN | Health ×2 + Report | Key project | No quarter-aligned milestone |
| Q6 / M18 | UNKNOWN | Health + Risk cleanup | Key project | No quarter-aligned milestone; exact M18 state/feedback UNKNOWN |
| Q7 / M21 | UNKNOWN | Risk cleanup + Report | Key project | No quarter-aligned milestone |
| Q8 / M24 | UNKNOWN | Health + Risk cleanup | Key project | M24 milestone L4, S43/N19/O13/H10/D10/W9; within-month ordering uncertain |

The compact run records 7/8 key-project actions and one M12 low-profile; promotions M6/M12/M24; it terminated at M25 after a second trust-crisis blowup. Rationale, immediate public risk cue, Energy/Main post-states, and comparable M18 state are not retained. The later trust terminal cannot backfill whether low-profile at M12 was correct or insufficient.

### SCORE-01 — seven recoverable quarter decisions

| Q / Month | Pre-E state L/S/N/O/H/D/W | Energy → post-E / pre-Main state | Main | Next Q pre-E (composite interval) |
|---|---|---|---|---|
| Q1 / M3 | L1/8/2/3/6/9/2 | Network + Health + Report → L1/8/3/3/8/10/2 | Key project | L1/9/2/2/6/10/3 |
| Q2 / M6 | L1/9/2/2/6/10/3 | Report + Network + Report → L1/9/3/3/6/10/3 | Key project | L1/9/3/3/7/9/4 |
| Q3 / M9 | L1/9/3/3/7/9/4 | Report + Network + Report → L1/9/3/3/7/10/4 | Key project | L1/9/3/2/7/10/4 |
| Q4 / M12 | L1/9/3/2/7/10/4 | Risk cleanup + Report → L1/9/3/3/7/10/4 | Key project | L1/9/3/1/6/10/7 |
| Q5 / M15 | L1/9/3/1/6/10/7 | Report + Network + Report → L1/9/3/3/6/10/7 | Key project | L1/9/3/-1/4/8/8 |
| Q6 / M18 | L1/9/3/-1/4/8/8 | Health ×2 + Report → L1/9/3/0/8/9/8 | Key project | L1/9/3/3/8/10/10 |
| Q7 / M21 | L1/9/3/3/8/10/10 | Network ×2 + Report → L1/9/3/3/8/10/10 | Key project | No next quarter; terminal by M24 |

M6 and M18 transcript summaries mention C and D feedback; they are not structured ratings. Exact promotion month before the M24 terminal L2 summary is UNKNOWN. Main’s immediate result is not isolated because the next period includes month processing/story activity.

### S06 Run #1 and v4 Run #1

| Run | Quarter coverage | Recovered actions / states | Nearby evidence |
|---|---|---|---|
| S06 Run #1 | 16 quarter Main actions | Main = Key project in all 16; exact Energy sequences, pre-states, feedback, and promotion months UNKNOWN. Compact summary reports later repeated project/report actions despite public no-growth observations. | 48 months, 53.83 / 37.68 / C, final L4. One trajectory, not an action-effect comparison. |
| v4 Run #1 | Q1 at M3; terminal before Q2 Energy at M6 | Q1 pre-E Health=2; selected Health recovery, Network, Report; recovery directly observed Health 2→4; Main = Key project. Other Q1 public dimensions are not reproduced here. | M6 Health terminal occurred before Q2 Energy. Q1 recovery did not establish safety for the later story/review window. |

## 3. Exact fixed Energy action surface

DEV_CONFIRMED: decoded `energy_event.data` is the public Dev menu. `RegularActionDefinition.to_choice` carries `status_updates` into the choice; the MCP choice filter removes internal identifiers but not those updates. Thus the fixed-action delta (including named HiddenRisk delta) is advertised to the Agent. By contrast, `current_state` filtering removes hidden state fields, including current HiddenRisk stock and failure-rule remaining counts. A per-action delta reveals neither current stock nor terminal margin.

| Action | Energy | Advertised status update | Repeat / timing note |
|---|---:|---|---|
| 高强度工作 | 2 | Output +2, Health −1, Dignity −1, HiddenRisk +1 | Repeat allowed if Energy remains; failure is checked after each action. |
| 技能学习 | 2 | Skill +1, Health −1 | Unique Energy Skill gain; Health and two-Energy opportunity costs. |
| 人脉维护 | 1 | Network +1, Dignity +1 | Repeat allowed; either gain can be clipped at a bound. |
| 处理历史埋雷 | 2 | HiddenRisk −1 | Current stock is unobservable; public evidence must support relevance. |
| 心理修复 | 1 | Dignity +2 | May be partially/fully clipped. |
| 健康恢复 | 1 | Health +2 | May be clipped; occurs after the quarter’s story window. |
| 准备汇报材料 | 1 | Output +1, Dignity +1 | Repeat allowed; either gain can be clipped. |
| 保留体力（不行动） | 0 | No update | Ends Energy allocation immediately; unused Energy does not carry over. |

Main has one selection per quarter, no Energy cost, and also applies its displayed updates. `CareerState.apply_delta` clamps Health/Dignity, Skill/Network, Output, and HiddenRisk; Skill/Network/Output also have configured per-Level limits. Exact level caps remain Dev-only, not runtime inputs.

## 4. Legal Energy bundles and reproducible Pareto method

Let N=Network, M=Mental repair, H=Health recovery, P=Report (each costs 1); W=high-intensity work, S=Skill learning, C=risk cleanup (each costs 2). Repetition is permitted. Enumerating multisets of 0–3 non-no-action selections and retaining total cost ≤3 gives all **50 unique unordered bundles**:

| Total Energy | Every unique bundle |
|---:|---|
| 0 | ∅ (no_action) |
| 1 | N, M, H, P |
| 2 | W, S, C; NN, NM, NH, NP, MM, MH, MP, HH, HP, PP |
| 3 | For each X ∈ {W,S,C}: XN, XM, XH, XP; and NNN, NNM, NNH, NNP, NMM, NMH, NMP, NHH, NHP, NPP, MMM, MMH, MMP, MHH, MHP, MPP, HHH, HHP, HPP, PPP |

Counts by cost are 1 / 4 / 13 / 32. These are bundles, not sequences. Any under-budget bundle needs an explicit no_action terminator to enter Main; spending all 3 Energy or reaching the 3-choice limit advances automatically. Ordered actions must also respect remaining Energy after each choice.

For the additive comparison, sum configured deltas for each bundle and compare component-wise on Health, Dignity, Network, Skill, Output, advertised HiddenRisk reduction, and Energy cost (less cost is better). This unsaturated comparison has 50 bundles; 45 are Pareto-frontier bundles and five are dominated:

| Dominated bundle | Same-cost replacement | Why dominated in current Dev |
|---|---|---|
| W | PP | Equal Output; replacement improves rather than reduces Dignity, does not reduce Health, and avoids HiddenRisk increase. |
| WN | PPN | Same Network; replacement is no worse on other dimensions. |
| WM | PPM | Replacement is no worse on Dignity and better on Health/risk. |
| WH | PPH | Replacement yields more Health/Dignity for same Energy and Output. |
| WP | PPP | Replacement yields equal-or-better public effects and avoids HiddenRisk increase. |

This is DOMINATED_IN_CURRENT_DEV, not “always disable high-intensity work” as a global policy. The other 45 are only nondominated in this additive vector test—not jointly optimal. Clamps can collapse or conditionally dominate bundles; a bundle addressing a distinct public objective/material risk remains incomparable to growth-only bundles. No fixed winner follows.

## 5. Marginal value, saturation, and Energy efficiency

- **Health recovery (+2, cost 1):** DEV_CONFIRMED bounds Health; gains near the ceiling can be clipped. RUN_OBSERVED: v4 Q1 was directly observed 2→4. SCORE-01 Q6 pre-action snapshots show H4→6→8 before Main. Other quarter deltas mix story/review activity. Recovery cannot protect against the preceding story window or revive a terminal session.
- **Mental repair (+2 Dignity, cost 1):** distinct from Health/Network repair; can be clipped. No selection in the three recoverable full action streams; S06 Energy is unknown.
- **Network maintenance (+1 Network/+1 Dignity, cost 1):** two public targets, but capped Dignity is not Network gain. SCORE-01 Q1 showed N2→3/D9→10; Q3/Q7 repeated choices at observed N3/D10 showed no corresponding increase in pre-Main snapshots. This is state/run evidence, not a universal cap rule.
- **Skill learning (+1 Skill/−1 Health, cost 2):** unique Energy Skill gain; no selection in recovered full action lists. Main alternatives offer different Skill/Network mixes. No fixed Skill-first schedule is supported.
- **Report (+1 Output/+1 Dignity, cost 1):** SCORE-01 Q1 at O3/D10 and later repeated reports at O3 produced no public pre-Main increment; Q2’s first report at O2 raised Output before the next Energy choice, while the second at O3 did not. These are direct within-quarter snapshots. S06 Run #1 separately reports repeated preparation after Output 26 without observed Output growth; raw is unavailable, so no cap/isolated causal mechanism is asserted.
- **High-intensity (+2 Output/−1 Health/−1 Dignity/+1 HiddenRisk, cost 2):** dominated by two Reports in the current Dev vector. Its numeric risk delta is advertised; current stock/failure margin is not.
- **Risk cleanup (−1 HiddenRisk, cost 2):** unique advertised risk reduction, but no current-stock measurement. No periodic quota is supported; fresh public risk context must justify comparison.
- **No action:** ordinarily wastes non-carried Energy, but can be rational if relevant gains are clipped or costs/risk are unacceptable. Do not reject solely because Energy was budgeted.

### Historical Energy selection totals

Counts are selected actions; Energy points add two per risk-cleanup action. They are frequencies, not value estimates.

| Run | Health | Network | Report | Cleanup | Skill / Mental / High-intensity | Energy points |
|---|---:|---:|---:|---:|---|---:|
| v1 #1, 16 Q | 11 | 6 | 25 | 3 | 0 recorded | 48 |
| v1 #2, 8 Q | 8 | 5 | 5 | 3 | 0 recorded | 24 |
| SCORE-01, 7 Q | 3 | 6 | 10 | 1 | 0 recorded | 21 |
| v4 #1, Q1 only | 1 | 1 | 1 | 0 | 0 observed | 3 |
| S06 Run #1 | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |

v1 #1 reached 48 months with 11 recoveries; v1 #2 ended in a trust crisis at Health 10; SCORE-01 ended at M24; v4 ended at M6 from Health=0. These outcomes do not identify a causal effect of any Energy frequency.

## 6. Energy ordering within a quarter

**Classification: STATE_DEPENDENT.**

DEV_CONFIRMED: each Energy choice applies its delta, clamps stats, then evaluates failures before the next choice; Main follows Energy. Thus order is not freely exchangeable:

1. A Health-cost action (W or S) can take Health to zero and trigger terminal failure before later recovery. At publicly observed Health 1, “costly growth then recovery” is not a rescue plan; terminal evaluation precedes the later choice.
2. At a Health/Dignity ceiling, gains may be clipped. At Health 10, recovery before a −1 action can finish at 9, while −1 then recovery can finish at 10. Safety and legality still depend on state before each action.
3. HiddenRisk has a zero floor; cleanup/high-intensity order can change internal result around that floor. Current stock is not an allowed inference.
4. Away from bounds and terminal triggers, most fixed deltas are additive and may commute; do not assume that near a limit.

The fixed-action interface permits fresh state between choices. SCORE-01 records pre-action snapshots. If the next comparable observation is missing or includes story/month processing, realized effect is UNKNOWN / AMBIGUOUS, not the advertised delta.

## 7. Quarterly Main Action surface

All updates are fixed-menu advertised vectors; each consumes the quarter’s one Main slot.

| Main action | Advertised update | Conditional role, not a ranking |
|---|---|---|
| 申请关键项目 | Output +2, Skill +1, Network +1 | Broad-growth prior while all gains remain useful and observed effects support continuing. |
| 向领导汇报成果 | Output +1, Network +1, Dignity +1 | Compare for a review-visible output/recognition gap. |
| 主动争取资源 | Output +1, Network +1 | Compare for an output/network bottleneck with supportive context. |
| 申请岗位轮岗 | Skill +2, Network +1 | Direct alternative when public Skill progress is the active gap; no promotion guarantee. |
| 主动曝光成果 | Output +1, Dignity +1 | Compare for delivery/visibility gaps; not automatically better than a report. |
| 建立导师关系 | Skill +1, Network +2 | Compare where Network is limiting and context supports mentorship. |
| 修复关键关系 | Network +1, Dignity +1 | Compare with public relationship strain or these visible gaps. |
| 低调避险 | Health +1, HiddenRisk −1 | Survival/risk alternative when fresh public evidence supports it; consumes the only Main slot. |
| 不行动 | No update | Usually gives up useful growth, but can be appropriate if options are clipped or unacceptable. |

## 8. Historical Main-action counterfactuals

These public-state comparisons identify what a future controller should compare, not whether an alternative would improve score.

| Checkpoint | Public Survival evidence / retrospective band | Readiness / Primary Gap | Conditional alternative to compare | Next observed outcome |
|---|---|---|---|---|
| v1 #1 M33 / Q11 | H9/D10; complete fresh warning/trend evidence unavailable, so formal band UNKNOWN | L4, S90/N36/O25 and M36 review upcoming; exact public readiness and unique gap UNKNOWN | Compare Key project with rotation/mentorship and account for Report×3 Energy overlap | Promotion observed M36; intervening period prevents action attribution |
| SCORE-01 M9 / Q3 | H7/D9; public risk band and warning context UNKNOWN | L1, S9/N3/O3; Energy increments show saturation in recorded snapshots, but Primary Gap UNKNOWN | Compare a different current-gap vector after fresh observe | M12 pre-E snapshot includes three months of events; AMBIGUOUS |
| S06 Run #1 late quarters | Quarter state and public Survival band UNKNOWN | Primary Gap and readiness UNKNOWN; repeated no-growth only in compact summary | Compare a legal alternative when fresh same-target effect remains stalled | Final L4 at M48; no isolated quarter outcome |
| v1 #2 M12 / Q4 | Decision-time state/cue and Survival band UNKNOWN | Promotion observed in M12; pre/post-review timing of milestone vs Main not sufficient to classify readiness | Low-profile versus growth only if fresh public risk cue supports it | Later M25 trust terminal does not explain M12 choice |
| v4 M3 / Q1 | Health=2 is a direct public survival concern; formal band label not recorded; other channels UNKNOWN | Other state, readiness, and Primary Gap UNKNOWN | Compare added reserve with growth only under fresh state and remaining-risk context | M6 Health terminal before Q2; no counterfactual rescue evidence |

1. **v1 #1 M18–M33 (Q6–Q11):** Key project continued while L4 was retained through missed M24/M30 reviews; snapshots show Skill 44→90, Network 18→36, Output 14→25 by M33, with intervening fluctuations. At M33, Energy was Report×3 and Main was Key project before M36 review. HYPOTHESIS: compare rotation (more direct Skill vector) or mentorship (different Skill/Network mix) with the broad project, and check overlap with Energy Output spend. S06-12’s Dev-only bottleneck diagnosis is not an Agent-visible threshold or proof an alternative was better.
2. **SCORE-01 Q2/Q3 (M6/M9):** repeated Report/Network actions targeted Output/Network/Dignity; Q3’s recorded pre-Main public values were L1/9/3/3/7/10/4. Several Energy increments were clipped at the observed state. This supports re-observing and comparing another menu vector, not banning projects or reports.
3. **S06 Run #1:** all 16 Main actions were Key project; later repetitions cited advertised gains despite compact no-growth observations. This supports “observed effect > broad advertised prior.” Missing quarter state/raw prevents detailed counterfactuals or causal claims.
4. **v1 #2 M12:** low-profile was chosen once; immediate public cue/rationale was not retained. The later trust terminal cannot establish that it should have been chosen more often.
5. **v4 #1 Q1 / pre-Q2:** at M3 Energy started at Health 2; one recovery raised it to 4, followed by Network/Report and Key project. The run reached Health terminal during M6 before Q2 Energy. This supports pre-review timing and survival-constrained packages, not that another Q1 bundle would have prevented terminal.

Across runs, repeated Key project use coexists with outcomes from 48-month A to early termination or 48-month C. This is descriptive repetition plus high variance—not a global winner or causal action comparison. v1 #1’s 48-month A also prevents interpreting broad growth as inherently bad.

## 9. Joint Energy + Main package and four phases

### Package principles

1. **Bottleneck coverage:** identify one public Primary Gap/readiness issue; assess Energy and Main together.
2. **Complementarity:** use Energy for a needed reserve or one target, then prefer a Main vector covering a different still-useful gap where possible.
3. **Redundancy check:** if both slots advertise the same dimension, compare combined gains after current bounds and recent effects. Overlap prompts comparison, not an automatic prohibition.
4. **Survival-first package:** resolve fresh material survival constraints and action-order hazards before discretionary growth; ordinary soft cost is not material risk.
5. **Review / promotion reset:** formal feedback and actual level change are fresh phase signals. Re-observe, reset Primary Gap, and account for recovery occurring only after the preceding story window.
6. **Horizon:** use public month and the 48-month horizon qualitatively; as time shortens, prefer legal benefits observable within the remaining horizon over remote/uncertain payoff.
7. **Observed-effect loop:** menu delta is a prior; compare fresh before/after on the same target; mark story-contaminated intervals AMBIGUOUS.

| Phase | Conditional quarterly-package emphasis | Avoid |
|---|---|---|
| FOUNDATION | Maintain public survival buffer, then cover a current foundational gap (Skill, Network, Output, or another public career/resource gap). | Fixed Skill-first, fixed balanced recipe, or assuming early mercy makes survival irrelevant. |
| PROMOTION | Use fresh level/trends/formal feedback/distance to review to select a direct gap; check whether Energy already covers it. | Hidden gates/probabilities or fixed month-to-action calendar. |
| COMPOUNDING | After promotion reset the gap; otherwise preserve still-effective broad growth while observing for saturation. | Carrying a prior-level objective through a phase change or ignoring repeated no-growth. |
| FINAL_SPRINT | Prefer safe, directly realizable public gains within remaining months; compare delayed options against horizon. | Exact salary/score NPV, score-weight optimizer, or fixed cutoff month. |

S06-12 confirms new-level salary begins in subsequent months, giving earlier promotion a directional compounding prior within a fixed horizon. It cannot override survival constraints or justify hidden-threshold/NPV policy.

## 10. Candidate quarterly policy decisions

These are recommendations for Main’s next static candidate review; this task changes no v5 behavior.

| Candidate rule | Decision | Evidence / runtime-visible inputs | Failure mode addressed | Must not encode |
|---|---|---|---|---|
| Evaluate an Energy bundle and one Main action jointly | ADOPT_CANDIDATE | Menu vectors, one Main slot, fresh state, Primary Gap, remaining Energy | Independent choices duplicate gains or miss bottleneck | Global scalar score or bundle lookup |
| Survival constraint and action-order check before Health-cost growth | ADOPT_CANDIDATE | Fresh Health/trend, material public warning, Energy, displayed action cost | Recovery after terminal risk; growth while publicly tight | Fixed Health cutoff/recovery count; assuming later recovery rescues terminal |
| Compare a targeted Main alternative when broad Key-project path is stalled | ADOPT_CANDIDATE | Comparable same-target effect, public S/N/O, fresh review outcome | Repeating broad prior without progress | Never choosing Key project; hidden gates; forced switch after one noisy observation |
| Treat advertised deltas as hypotheses and use comparable fresh effects | ADOPT_CANDIDATE | Current/post-choice observe, same target, freshness | Crediting clipped/unobserved gains | Attribution from story-contaminated quarter deltas |
| Check complementarity/saturation before duplicating a dimension | ADOPT_CANDIDATE | Menu vectors, public state, post-Energy state, one Primary Gap | Spending both slots on capped/overlapping target | Fixed ban on repeated dimension investment |
| Reset Primary Gap after formal review/promotion | ADOPT_CANDIDATE | Actual level change, formal feedback, fresh trends, survival, public month | Stale objective after phase change | Exact promotion threshold/probability or mandatory month |
| Increase near-term realizability weight as horizon shortens | ADOPT_CANDIDATE | Public month, remaining horizon, observed effect | Remote option near game end | Fixed month/action mapping or evaluator weights |
| Numerical hidden-risk inventory or frequency-trained action value | DEFER | Current stock filtered; few confounded trajectories | False confidence from hidden state/action counts | Reconstruct hidden counter from menu delta or frequency |
| Universal best bundle, periodic cleanup/recovery quota, or phase calendar | REJECT | Multidimensional effects; clamps, timing, saturation change value | Open-loop overfit | Global winner, fixed count, month-specific script |
| Global action ban, event-title answer map, or score-weight strategy | REJECT | Menu-specific Pareto result; story options/evaluator weights are not runtime evidence | Overgeneralization | “Never use high-intensity”, fixed story answers, hidden thresholds, score-to-80 |

DEFER means evidence is insufficient for a portable rule; REJECT means the proposed universal/hidden-information form conflicts with the evidence boundary. Neither changes current v5.

## 11. Remaining unknowns and DO_NOT_ENCODE

- v1 #1 lacks immediate post-Energy and post-Main state; v1 #2 lacks quarter pre-states and action-level post-states. SCORE-01 has post-Energy/pre-Main snapshots but no uncontaminated post-Main snapshot.
- Quarter changes include stories, review, promotion, and monthly processing. Do not attribute these to one Energy/Main action.
- S06 Run #1 per-quarter state/Energy/promotion/raw timeline remains unavailable; accepted compact claims are descriptive.
- v1 #2 M12 rationale/risk cue and trust-crisis chain remain unknown. SCORE-01 exact promotion month and terminal mechanism remain unknown.
- Story choices lack the fixed-action numeric update contract; do not transfer fixed-menu effects to story choices.
- Hidden risk stock/failure margin, exact per-Level caps and promotion gates, future opportunities, action-specific causal effects, and cloud/test transfer are unknown or non-portable.
- No recovered comparison isolates Main choice, Energy bundle/order, or joint package as a cause of score/survival.
- Stable 80+, v5 gameplay effectiveness, and score effect of these candidate policies remain NOT_PROVEN.

DO_NOT_ENCODE: exact Dev thresholds/caps; inferred HiddenRisk stock; fixed bundle/calendar; global winner/ban; event-title answer table; ending-score weights; precise promotion/salary NPV; selection frequency as action value.

## 12. Verification and next review inputs

- Fetched `origin/main` = local `main` = `685ddc416656062b173708e875c99b9e234bea93`; no branch/worktree used.
- Historical claims trace to exact Git commit/path/blob identities in Section 1; incomplete evidence is UNKNOWN / AMBIGUOUS.
- Package versions match Source Lock; both fixed-action Dev files byte-match simulator copies; hashes are recorded in Section 1.
- All 50 bundles are generated from the seven costed Energy actions (repetition allowed), cost ≤3; Pareto uses displayed deltas and the stated component-wise rule.
- No private/test data, game, session, provider, service, MCP, install/reload, Runner play, or raw S04 artifact accessed.
- Only this review file is in scope; v5, Skills, Runner, dependencies, current-state, raw, and runtime were not edited.
- git diff --check, scope, commit/push, remote identity, and clean-tree checks are performed at delivery.

### Inputs for S06-14

- Keep fixed quarterly action vectors separate from story-choice effects, which lack uniform numeric updates.
- Treat event patterns/opportunities as conditional public evidence; do not create title-to-answer mappings.
- Reuse joint-package, Primary Gap, survival constraint, horizon, freshness, and observed-effect boundaries.
- Treat future action-outcome comparisons as descriptive unless a controlled design isolates the decision.

## 13. Recommendation

RETURN_TO_MAIN_FOR_S06_14_EVENT_PATTERN_REVIEW

This review does not authorize gameplay. Candidate v5, `CURRENT_STATE.md`, Skills, and deferred Memory / fifth Skill / Team / Swarm decisions remain unchanged.
