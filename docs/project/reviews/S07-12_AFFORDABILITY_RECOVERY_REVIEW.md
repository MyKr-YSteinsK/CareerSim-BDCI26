# S07-12｜公开 Affordability Recovery 收口验证

## Identity / decision

- Base: `main@ed7278b86456af0e0d68a4869c76c769635c3801`; Candidate observed as `candidate-v6c-compliance-cleanup` and was not run as an Agent or modified.
- Four authorized fresh sessions ran in order: `P1R → P2R → P1R → P2R`.
- Batch evidence: [`../runs/s07-12-affordability-recovery-batch.json`](../runs/s07-12-affordability-recovery-batch.json). Per-session public traces/summaries and server stderr remain local under `D:\CS\CareerSim\.local\runtime\s07-12-affordability-recovery\`; summary file hashes are recorded in the batch evidence.
- Experiment decision: `CHEAP_PROBE_INFORMATION_LIMIT_REACHED`. The explicit affordability guard recovered once, but only one of four sessions passed M3, no session reached month 12, and no comparable progress checkpoint or stall observation occurred. This does not establish a Candidate-level benefit. The cheap mechanical probe line ends here; next recommendation is `REAL_AGENT_VALIDATION`.

## Recovery implementation

P1R and P2R wrap the existing P1 and P2 choice policies. The wrapper recognizes only an explicit public receipt matching the narrow `Insufficient energy/resource for …: N remaining` form. It makes no energy-cost or threshold assumption. After one fresh observe confirms the same projected public state, the rejected choice is temporarily excluded and the unchanged base policy selects from the remaining legal public choices. Public state changes reset the exclusion. Each unique choice can be attempted at most once per unchanged projected decision state; if all choices are explicitly resource-rejected, the session ends as `POLICY_NO_AFFORDABLE_PUBLIC_ACTION`. Other explicit rejections end only that session without generic retry. Uncertain state or transport outcomes remain hard stops.

Offline tests cover classification, exclusion and reselection, no resend, reset after public-state change, all-choice bound, non-affordability rejection, uncertain recovery, P1/P2 wrapper identity and unchanged P2 stall behavior. They pass with the existing probe regression tests.

## Four fresh sessions

| Slot | Policy | Session ID | Month reached | End state | Attempts / successes / rejections / recoveries | Grade | Quantitative / partial score | Promotion | Checkpoints / stalls |
| --- | --- | --- | ---: | --- | ---: | --- | ---: | --- | ---: |
| 1 | P1R | `b4103bad4cd4416f9467e6ccdf1c27dc` | 3 | eliminated | 11 / 11 / 0 / 0 | E | 20.25 / 14.17 | none | 0 / 0 |
| 2 | P2R | `b96d6d7c1ede43f8a72bcdce09c4ea8b` | 6 | eliminated | 20 / 19 / 1 / 1 | E | 23.43 / 16.40 | M6 | 0 / 0 |
| 3 | P1R | `bf4679ba83df4448a2f8955c90d4e546` | 3 | eliminated | 11 / 11 / 0 / 0 | E | 20.00 / 14.00 | none | 0 / 0 |
| 4 | P2R | `13f0e26ffc6045d69123b9fc373d30c8` | 3 | eliminated | 8 / 8 / 0 / 0 | E | 18.77 / 13.14 | none | 0 / 0 |

All four sessions reached a public terminal state, but their public ending records say `outcome=eliminated` and `completed=false`; the harness status `COMPLETED` means the session reached a terminal state, not that the 48-month game was successfully completed. All four final public Health values were 0. P1R crossed M3 in 0/2 sessions; P2R crossed M3 in 1/2; total 1/4. P2R had one promotion at M6. P2R stall behavior was not exercised.

In slot 2, the public receipt was `Insufficient energy for high_intensity_work: 1 remaining`. A same-session observe confirmed no projected public-state change; the controller excluded that choice, re-ran P2's existing policy, and continued. This confirms one mechanical recovery path. The other three sessions produced no affordability rejection. Since only one session progressed beyond M3 and all ended early, these results do not justify adding this guard to the v6c Agent contract without Main review and later Agent validation.

## Accounting and limits

- Direct MCP starts / initialize / list_tools / new_game / clean shutdown: **4 / 4 / 4 / 4 / 4**.
- Observe: **54**; take_action attempts / successes / explicit rejections: **50 / 49 / 1**; confirmed affordability recoveries: **1**.
- AgentServer / DeepSeek or other provider / Runner play / Skill install or reload: **0**. No task server process remained after shutdown.
- Public seed control: `NO_PUBLIC_SEED_CONTROL_FOUND`.
- Scores are secondary descriptive public outcomes from four unpaired sessions. The sample does not show policy superiority, repeatability, stable 80+, or real-Agent effectiveness. No hidden cost, threshold, or internal game rule was used.

The batch consumed all four authorized fresh sessions. No further mechanical variants are recommended. Return to Main/S07 to plan `REAL_AGENT_VALIDATION`; this task does not authorize another game.
