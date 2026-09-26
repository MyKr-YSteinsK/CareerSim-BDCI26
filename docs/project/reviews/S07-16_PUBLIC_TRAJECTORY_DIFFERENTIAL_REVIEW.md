# S07-16｜高低分公开轨迹差分取证与策略规则挖掘

## Identity / boundary

- Repository: `MyKr-YSteinsK/CareerSim-BDCI26`
- Base: `main@5827aa2d41bb19bb6ad4eef777a355b73b5b2de3` (`origin/main` matched at start)
- Mode: offline, `PUBLIC_INTERFACE_ONLY`; no gameplay or policy implementation.
- Candidate at analysis time: `candidate-v6c-compliance-cleanup`; no Candidate, Skill, manifest, Runner, dependency, `CURRENT_STATE`, or ADR changes.
- No simulator internals, database, hidden state/effects/thresholds, evaluator formula, private/test data, or event-to-answer lookup was used. Public run scores are outcomes, not evidence of causal action effects.

Labels used below: **OBSERVED** = retained participant-visible record; **ASSOCIATION** = cross-run co-occurrence only; **HYPOTHESIS** = testable explanation; **UNKNOWN** = evidence not retained or not comparable.

## Evidence recovery and resolution

| Run | Public outcome | Resolution | Evidence actually used |
|---|---|---|---|
| Candidate v1 #1 | 76.04 / 53.23 / 48m / A / L6 | `CHECKPOINT_ONLY` | Recovered `candidate_run1_trajectory.json` from S04-04 commit `8a93378a8d9ef5598e925048db39ee931e207bab` (Git blob `a9ca5d759b05dd0c9b3974c9a1398a3ca3990343`, 27,518 B; 49 public monthly snapshots, promotion events, quarterly Main decisions and Energy selections). Cross-checked public action/state timeline in S04-03 `score01_trajectory.json` at `7a055dea76580117ca74cddb49bb04efcf605eb1` (blob `0330ef9c95ea13b285a8fcfcf1b4c2c6e80ff65a`, 66,604 B). These are compact public records, not a complete raw conversation. |
| Candidate v1 #2 | 35.31 / 24.72 / 25m / D / L4 | `CHECKPOINT_ONLY` | S04-04 `candidate_run2_trajectory.json` at the accepted evidence commit (blob `85129980c0591f0ad4d4bee113562bc51116d16d`, 6,811 B), plus public comparison/result summaries. No month-by-month series beyond retained milestones. |
| Original v6 #1 | 75.29 / 52.70 / 48m / A / L6 | `FULL_PUBLIC_TRAJECTORY` | Local public `events-20260925T094419Z.jsonl`, 2,061,570 B, SHA-256 `2CCE87EB6AFD8AEA5A9651F75621AE7C2B303E8C00C7F2AC417DC65C030371D8`, matching `docs/project/runs/v6-run1-validation.md`. Read public event/action/observe data only; the paired transcript and DB were not read. |
| S07-14 | 65.16 / 45.61 / 48m / B / L5 | `FULL_PUBLIC_TRAJECTORY` | Local `public-trajectory.jsonl`, 490,064 B, SHA-256 `52EE26DEE5468CF22891026DEB7A967874539D57466806C99BAAD2D0E8F1B81F`, matching the committed run record. |
| S07-15 R2 | 54.85 / 38.39 / 48m / C / L4 | `FULL_PUBLIC_TRAJECTORY` | `R2/public-trajectory.jsonl`, 489,578 B, SHA-256 `C2E65B6909000B23B0C0D05234CAF9FDA5E4981D5FFAA0EEA5932C2E5BE749F1`; run/review records. |
| S07-15 R3 | 16.55 / 11.58 / 12m / E / L2 | `FULL_PUBLIC_TRAJECTORY` | `R3/public-trajectory.jsonl`, 109,827 B, SHA-256 `D3ECD83BE98938EF89943740659B52E3D4C06D77838C7AB7C7688E8753888B0F`; run/review records. |
| S07-15 R4 | 57.90 / 40.53 / 48m / C / L5 | `FULL_PUBLIC_TRAJECTORY` | `R4/public-trajectory.jsonl`, 525,950 B, SHA-256 `24F15E623DF6D672424039BFD45D8DD605FC4DA0354A012F2199D4A6DA4C103A`; run/review records. |
| S06 Run #1 | 53.83 / 37.68 / 48m / C / L4 | `SUMMARY_ONLY` | `RUN_HISTORY.md`; detailed monthly/action history unavailable in the permitted compact record. |

The v6 and S07-14 raw trajectories remain local ignored evidence; no raw evidence is added to Git. Evidence resolution describes completeness, not validity of causal interpretation.

## Common public checkpoint timeline

State tuple: `Level / Health / Skill / Network / Output / Wealth`. These are public status values, not weighted score dimensions. Rows are snapshots at the named month; `—` means the run had ended, `?` means not retained. No interpolation.

| Run | M6 | M12 | M18 | M24 | M30 | M36 | M42 | M48 |
|---|---|---|---|---|---|---|---|---|
| v1 #1 (76.04) | L2/7/13/5/6/2 | L3/7/24/7/7/4 | L4/10/44/19/16/6 | L4/8/63/36/26/10 | L4/10/82/36/26/15 | L5/9/100/36/29/21 | L5/9/115/54/38/30 | L6/9/138/51/40/39 |
| v6 #1 (75.29) | L2/6/11/3/5/3 | L3/5/23/8/7/4 | L4/9/38/19/17/8 | L4/8/61/30/26/11 | L4/7/81/36/26/15 | L5/8/102/39/24/22 | L5/9/124/54/38/29 | L6/7/141/57/40/38 |
| S07-14 (65.16) | L2/7/11/6/3/1 | L2/10/21/7/6/1 | L3/10/28/12/11/3 | L4/9/48/15/12/6 | L4/9/62/24/18/9 | L4/10/79/36/25/12 | L5/10/100/34/26/16 | L5/10/122/52/35/24 |
| R2 (54.85) | L1/5/9/3/3/2 | L2/6/13/7/6/3 | L3/6/24/5/8/6 | L3/7/34/16/6/6 | L3/7/42/21/10/8 | L4/7/47/20/16/11 | L4/7/68/32/26/18 | L4/10/86/36/26/23 |
| R3 (16.55) | L1/5/9/3/1/0 | L2/2/9/3/3/0 | — | — | — | — | — | — |
| R4 (57.90) | L1/6/9/2/3/2 | L2/5/14/5/5/1 | L3/6/23/8/9/4 | L3/9/35/17/14/6 | L4/9/45/24/20/6 | L4/10/64/36/25/9 | L4/9/79/34/26/15 | L5/9/97/38/22/19 |

v1 #2 has only retained milestones: L2 at M6, L3 at M12, L4 at M24; it ended at M25 with Health 10, Skill 44, Network 20, Output 14, Wealth 3, Dignity 8. S06 Run #1’s comparable monthly values are `UNKNOWN`; its compact terminal record gives L4, Wealth 21.8, Skill 89, Network 36 and Risk Control raw 5.

**Descriptive contrast:** at M24, both 75+ references were L4 with Output 26 and Wealth 10–11. S07-14 was also L4 but Output 12 / Wealth 6; R2 was L3, Output 6 / Wealth 6; R4 was L3, Output 14 / Wealth 6. By M48, the two references were L6 with Output 40 and Wealth 38–39; completed Codex runs were L4–L5 with Output 22–35 and Wealth 19–24. This is a trajectory difference, not evidence about hidden score weights or the cause of the score gap.

## Promotions and review windows

| Run | Public promotion months | Public review-window observations retained |
|---|---|---|
| v1 #1 | M6, M12, M18, M36, M48 | Promotion schedule is available; comparable narrative review grades/feedback are `UNKNOWN`. |
| v6 #1 | M6, M12, M18, M36, M48 | Promotion schedule is available; comparable narrative review grades/feedback are `UNKNOWN`. |
| v1 #2 | M6, M12, M24; terminal M25 | Later review text and monthly states are `UNKNOWN`; M24 reaches L4 but does not establish why. |
| S07-14 | M6, M18, M24, M42 | M6 C + promotion; M12 C/follow-up, no promotion; M18 B + promotion; M24 B + promotion but “standard/no standout”; M30 B asks for clearer results; M36 B; M42 B + promotion; M48 B/no promotion. |
| R2 | M12, M18, M36 | M6 C/under observation; M12 C + promotion; M18 B + promotion; M24 B; M30 B; M36 B + promotion; M42 B; M48 A and “delivery stable / next window” wording, but no promotion. |
| R3 | M12; terminal M12 | M6 C described a last adjustment window amid accumulated risks; M12 C included negative reassessment, then L1→L2 notice and elimination. |
| R4 | M12, M18, M30, M48 | M6 C/under observation; M12 C + promotion; M18 B + promotion; M24 “busy/not-win”; M30 B + promotion; M36/M42 continued observation/clearer-results requests; M48 A bonus, expectations met and L4→L5 promotion. |

Review-boundary reading: the high references share the same promotion months, but this is only two runs. Codex runs show that similar public grades can precede different outcomes: R2 and R4 both received C at M12 and promoted; R2 received A at M48 without promotion while R4 received A and promoted. R3 was promoted at M12 but eliminated. Therefore neither grade labels nor month alone provide a demonstrated promotion rule. Public feedback about visible results is useful evidence for the next decision, not a proxy for an undisclosed threshold.

## Main action differential

Phase bins are public quarterly decisions: early M3–12 (4), middle M15–24 (4), late M27–48 (8). Values are counts, not quality rankings.

| Run | Main distribution | Early / middle / late notes |
|---|---|---|
| v1 #1 | Key project 16/16 | 4/4, 4/4, 8/8. |
| v6 #1 | Key project 14; low-profile risk action 2 | 4/4, 4/4, 6/8 key; low-profile at M27 and M45. |
| S06 Run #1 | Key project 16/16 | Phase details unavailable; score 53.83/C. |
| S07-14 | Key project 11; report 2; resources 1; exposure 1; mentor 1 | Early: key 3, exposure 1. Middle: key 3, resources 1. Late: key 5, mentor 1, report 2. |
| R2 | Key 5; exposure 5; report 5; resources 1 | Early: key 2/exposure 1/report 1. Middle: exposure 2/report 1/resources 1. Late: key 3/report 3/exposure 2. |
| R3 | Key 2; resources 1 | Key at M6/M9; resources at M3; terminated at M12. |
| R4 | Key 3; report 7; exposure 4; resources 2 | Early: key 1/report 2/exposure 1. Middle: report 2/exposure 1/resources 1. Late: key 2/report 3/exposure 2/resources 1. |
| v1 #2 | Key 7/8; low-profile action at M12 | M3/M6/M9 key, M12 low-profile; M15/M18/M21/M24 key. |

**Counterexample A:** v1 #1 used key projects 16/16 and scored 76.04, but S06 Run #1 also used 16/16 and scored 53.83. v6 scored 75.29 with 14/16. Thus frequency alone is insufficient and is not a deployment rule.

## Energy allocation differential

Counts are submitted action selections, not energy units or marginal benefit. Rejected selections are explicitly included where the source count includes them.

| Run | Public Energy selections |
|---|---|
| v1 #1 | Report preparation 25; health recovery 11; network 6; historic-risk cleanup 3 (45 total). |
| v6 #1 | Report preparation 15; health 10; network 8; high-intensity 5; risk cleanup 2; mental recovery 1 (41 total). |
| S07-14 | Health 13; high-intensity 5; Skill 5 (one rejected); risk cleanup 5; report 4; network 3 (35 attempts). |
| R2 | Report 9; health 8; risk cleanup 8; high-intensity 6; network 3 (34). |
| R3 | Health 3; risk cleanup 2; high-intensity 1 (6); terminal at M12. |
| R4 | Report 17; network 9; health 6; risk cleanup 6; high-intensity 2; Skill 1 (rejected); mental 1; reserve 1 (43 attempts). |

**Counterexample B:** R4’s 17 report-preparation and 9 network selections coexist with 57.90/C and M48 Output 22 / Wealth 19. v6 had fewer report selections (15) but M48 Output 40 / Wealth 38; S07-14 had only 4 report selections and ended at Output 37 / Wealth 25. In the public trajectory, report preparation sometimes immediately preceded Output +1 and sometimes no projected change. Counts do not establish timing quality, delayed effect, or causality. The striking R4 gap is that at M24 it was Output 14 / Wealth 6, versus 26 / 10–11 in the high references; by then its report/exposure history and event opportunities were not matched, so the reason remains `UNKNOWN`.

## Earliest visible divergence for Codex runs

Comparison baseline is the pair of v1 #1 / v6 #1 high references, not a matched control.

| Codex run | Earliest public divergence | Later progression gap |
|---|---|---|
| S07-14 | M6 already has lower Output (3 vs 5–6) and Wealth (1 vs 2–3), despite L2 and similar Skill; the first clear promotion-cadence split is M12, when it stays L2 while both references reach L3. | At M24 it is L4 but Output 12 / Wealth 6 vs 26 / 10–11 in references; it reaches L5 at M42, not L6 by M48. |
| R2 | M6: L1 vs L2, with Output 3 vs 5–6; the divergence is present before its first promotion at M12. | At M24 L3/O6/W6 vs reference L4/O26/W10–11; it reaches L4 at M36 and ends L4. |
| R3 | M6: L1 vs L2 and Output 1 / Wealth 0 vs 5–6 / 2–3. | At M9 public state showed Wealth -1; M12 status showed Health 2 / Wealth 0 with public debt language and elimination. No later comparison exists. |
| R4 | M6: L1 vs L2 and Output 3 / Wealth 2 vs 5–6 / 2–3. | M24 L3/O14/W6; reaches L5 only at M48, while high references reached L6. |

These are earliest observed differences in the retained records, not causal turning points. A different opportunity/event path could explain part of each gap.

## Survival versus score

- **Survival association:** completed 48-month runs span 53.83–76.04, so survival and score are distinct. R3’s public M9–M12 Wealth -1/0, Health decline, debt wording and elimination form an observed affordability-risk path; v1 #2 also ended at 25m with Wealth 3 during a trust-crisis path. This makes affordability a useful monitor, not a proven standalone cause. v1 #2 also shows that early promotions do not guarantee survival.
- **Endpoint caveat:** S07-15 R2/R4 public terminal status snapshots contain `alive=false, failed=true`, while their explicit public ending-score records say `completed=true`, `outcome=completed`, `survival_months=48`. This comparison follows the explicit ending-score fields for run outcome and retains the contradictory flags as an unresolved public-record inconsistency.
- **Score/progression association among 48m runs:** high references finish L6 with Output ~40 and Wealth ~38–39; S07-14/R4 finish L5 and lower Output/Wealth; R2 finishes L4. Skill alone is not a clear separator: R4 has Skill 97 yet L5 and 57.90, while S07-14 has Skill 123 and 65.16; high references have Skill 138–142. The run set is small and unpaired.
- **Variance boundary:** the same v1 candidate has 76.04/48m/A and 35.31/25m/D. Completed runs across different policies are unseeded, with different event opportunities and adaptive strategies. No significance, causal effect, or “mid-70 basin” is established.

## Story / semantic differential

Codex trajectories retain short public rationales and show examples of ownership, customer impact, reversibility, compliance and communication reasoning. Comparable public rationales for v1/v6 are not retained, so whether those semantic patterns distinguish 75+ runs is **UNKNOWN**. This review does not infer event-specific answers or compare hidden reasoning. The S07-15 report also says final submitted decisions, not unsubmitted reconsideration, were logged; deliberation volume is not comparable.

## Ranked public hypotheses

All are `LOW` confidence and suitable for testing, not current strategy facts.

### H1｜Review feedback should be converted into a verifiable next-window result

- **OBSERVED:** high references were L4 by M18 and had Output 26 / Wealth 10–11 by M24. S07-14/R2/R4 repeatedly received public “busy / clearer results / under observation” feedback; R4 later had many report actions but was still O14/W6 at M24 and O22/W19 at M48.
- **HYPOTHESIS:** use each fresh review feedback to identify one observable deliverable/result and test whether subsequent public state/feedback reflects it, rather than treating activity or reporting count as accomplishment.
- **Counterevidence:** high-run review text is unavailable; S07-14 promoted at M24 after “standard/no standout”; R2’s M48 A did not immediately produce promotion.
- **Next test:** in one authorized Codex run, log each review’s public request → one chosen delivery action → next comparable public feedback/state. No fixed month trigger or promotion threshold.
- **Transfer:** Codex exploration first; Candidate only after repeatable evidence.

### H2｜Project opportunity and visible delivery may need to be audited as separate stages

- **OBSERVED:** v1 #1/v6 chose key projects 16/14 times and finished O40, while S06’s 16/16 counterexample scored 53.83. S07-14 used key projects 11 times and ended O37; R4 used key projects 3 times, report 7, exposure 4 and ended O23.
- **HYPOTHESIS:** assess both opportunity selection and public completion/impact evidence; neither project volume nor visibility action volume alone is a useful proxy for delivered results.
- **Counterevidence:** v1 #1’s high result with 16 key projects and v6’s with 14 is compatible with multiple mechanisms; R4 report choices sometimes preceded public Output +1. Event paths and timing are unpaired.
- **Next test:** track public project commitments, completion receipts, observed Output/Wealth/feedback deltas and review timing in a future run; avoid fixed Main ratios.
- **Transfer:** both exploration and possible Candidate review, only after evidence.

### H3｜Affordability should be monitored separately from health/survival risk

- **OBSERVED:** R3 reached public Wealth -1 at M9 and 0 at M12 with debt language and ended; v1 #2 ended at 25m with Wealth 3. All completed 48m examples here ended with positive Wealth.
- **HYPOTHESIS:** public cash/affordability deterioration can be an independent constraint to notice before choosing commitments with visible costs; it should not become a guessed threshold or universal Wealth-maximizing rule.
- **Counterevidence:** v1 #2 had a concurrent public trust-crisis path; completed runs differ in opportunity/event sequence; Wealth co-movement does not identify cause.
- **Next test:** record public affordability, stated costs and subsequent fresh status around commitments in a future run; test only on observed states.
- **Transfer:** Codex exploration; formal Candidate deferred pending repeated public evidence.

## Candidate implication

- **Promising for further public exploration:** review feedback → verifiable result tracking; separate project opportunity from delivery evidence; monitor explicit affordability deterioration.
- **Unsupported:** “more key projects is better,” “more reporting/networking is better,” a fixed action-count recipe, promotion month/grade thresholds, or a claim that Skill is saturated.
- **Defer:** all formal Candidate changes, score-directed weights and mechanism claims until repeated public evidence and Main review. No Candidate was changed here.

## Decision / safety

- Decision: `TARGETED_STRATEGY_PRIOR_READY`.
- The useful differential is not a single action frequency: the strongest descriptive gap is early public progression (by M18) and M24 Output/Wealth trajectory, while counterexamples show Main/report counts do not explain it alone.
- Live accounting: CareerSim games 0; `new_game` 0; direct MCP 0; AgentServer 0; DeepSeek/provider 0; Runner gameplay 0; `observe`/`take_action` 0.
- Next recommendation: one targeted Codex public-agent exploration focused on review-feedback-to-verifiable-delivery observations, with affordability recorded as a separate public constraint. This is a recommendation only; no game is authorized by S07-16.
