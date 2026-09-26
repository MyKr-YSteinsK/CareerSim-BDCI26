# S07-15｜Codex Public-Agent 四局策略探索

## Identity and boundary

- Repository: `MyKr-YSteinsK/CareerSim-BDCI26`; base `main@ebf80f6cc1c07a3bdcf2e4cea2d6b2c27e1cbed6`.
- Mode: `PUBLIC-PRIOR STRATEGY DISCOVERY`; `NOT_A_BLINDED_POLICY_EVALUATION`.
- The user authorized up to four fresh sessions. Codex selected every gameplay choice after a fresh public observation. The bridge handled direct MCP transport, public projection, legal-choice validation and logging only; it contained no action-ranking or policy selector.
- Permitted public priors (S07-14 and earlier public mechanical results) were used. No hidden/private simulator information, decoded effects, thresholds, evaluator formula, DB contents or event-to-answer lookup was used.
- Current formal Candidate remained `candidate-v6c-compliance-cleanup`. Candidate, Skills, runtime manifest, Runner, dependencies, `CURRENT_STATE.md` and ADR were not modified.

## Session outcomes

Scores are public ending-score fields. State columns are public terminal status, not weighted score dimensions. The endpoint's `ending_score.dimensions` value was not retained by the strict projection, so dimension score breakdowns are `UNKNOWN` for all runs.

| Run | Session | Outcome | Quantitative / partial | Survival | Grade | Level | Skill | Network | Output | Wealth | Health | Dignity | Promotions |
|---|---|---|---:|---:|---|---|---:|---:|---:|---:|---:|---:|---|
| R1 | `0f59851a90e04652adab99ad0b2578d6` | technical partial before player action | UNKNOWN / UNKNOWN | UNKNOWN | UNKNOWN | L1 at M1 | 1 | 1 | 0 | 1 | 5 | 5 | none observed |
| R2 | `7df2ba5cb1f14898a88ddc6432ad2ce6` | completed | 54.85 / 38.39 | 48m | C | L4 | 86 | 36 | 26 | 24 | 10 | 10 | M12 L2; M18 L3; M36 L4 |
| R3 | `90e148910d8b4925869d7c0122a8fe21` | naturally eliminated | 16.55 / 11.58 | 12m | E | L2 | 9 | 3 | 3 | 0 | 2 | 7 | M12 L2 |
| R4 | `66f29c11486945dda952215850b80d41` | completed | 57.90 / 40.53 | 48m | C | L5 | 97 | 39 | 23 | 20 | 9 | 10 | M12 L2; M18 L3; M30 L4; M48 L5 |

R2 and R4 terminal snapshots showed `alive=false, failed=true` while their explicit `ending_score` said `completed=true`, `outcome=completed`, `survival_months=48`. They are recorded as 48-month completions based on the explicit ending-score fields; the public-field inconsistency is preserved as a limitation. R3's ending score said `eliminated` at 12 months.

## Run records

### R1 — technical partial, no gameplay action

- Direct MCP start: `2026-09-26T09:47:16Z`; initial public observe at M1/Q1 showed the single legal choice `继续`.
- The first launch had no interactive stdin/PTY. The bridge received EOF and shut down its own child. `new_game=1`, observe `1`, `take_action=0`; no player decision was submitted. The session is a technical partial and consumes one authorized fresh-session slot; it is not a game outcome and was not resumed.
- Raw public trajectory: `.local/runtime/s07-15-codex-public-agent/R1/public-trajectory.jsonl`; 2,326 bytes; SHA-256 `a030cdbb38239755e5683a1db479da6a8cd93b38c6f168d603dc3a0cbdd3d7dd`.

### R2 — completed 48 months

- Direct MCP start: `2026-09-26T09:48:41Z`; terminal/shutdown: `10:08:04Z`.
- Main actions: key project 5, expose results 5, report results 5, request resources 1. Energy submissions: health recovery 8, report preparation 9, networking 3, high-intensity work 6, risk cleanup 8.
- Public promotion notices: M12, M18 and M36. The M36 review described performance as standard/under observation; the run ended L4. Public feedback repeatedly contrasted being busy with visible wins. Some later high-intensity choices showed no immediate projected Output increase; subsequent Main choices shifted toward reporting/exposure. This is descriptive and does not rule out delayed effects.
- At M21 a side-project path received public complexity/team-capacity concerns. A later production incident received feedback that the response was too rigid for customer impact; a tiered response was then selected.
- Raw public trajectory: `.local/runtime/s07-15-codex-public-agent/R2/public-trajectory.jsonl`; 489,578 bytes; SHA-256 `c2e65b6909000b23b0c0d05234caf9fda5e4981d5ffaa0eea5932c2e5be749f1`.

### R3 — natural elimination at M12

- Direct MCP start: `2026-09-26T10:10:56Z`; terminal/shutdown: `10:15:34Z`.
- Main actions: request resources 1, key project 2. Energy submissions: health recovery 3, high-intensity work 1, risk cleanup 2.
- M6 public feedback was sharply negative and described accumulated risks, prior hazards and a final adjustment window. At M9 public status showed Health 3, Output 2, Wealth -1; at M10/M11 Wealth remained -1. The M12 ending narrative explicitly described repeated months without money/growing debt. The run nevertheless received an L1→L2 promotion notice at M12 before elimination.
- The player made public adjustments around health, risk, customer scope and communication. The trajectory cannot establish which choices caused the financial outcome or whether a different choice would have survived.
- Raw public trajectory: `.local/runtime/s07-15-codex-public-agent/R3/public-trajectory.jsonl`; 109,827 bytes; SHA-256 `d3ecd83be98938ef89943740659b52e3d4c06d77838c7ab7c7688e8753888b0f`.

### R4 — completed 48 months, highest score in this set

- Direct MCP start: `2026-09-26T10:16:11Z`; terminal/shutdown: `10:39:01Z`.
- Main actions: report results 7, key project 3, expose results 4, request resources 2. Energy submissions: report preparation 17, health recovery 6, networking 9, risk cleanup 6, high-intensity work 2, skill learning 1 explicit rejection, mental recovery 1, reserve 1.
- Promotions: M12, M18, M30 and M48. At M48 the public six-month feedback awarded an A bonus, said performance met expectations, and promoted L4→L5. Final public status at administrative M49: Health 9, Dignity 10, Skill 97, Network 39, Output 23, Wealth 20, Energy 0.
- At M24 and again M36/M42, public feedback asked for clearer results rather than activity. A staged service refactor was selected after public load approached 80% of stated design capacity. Later public feedback recognized that AI-assisted work freed time for harder design; this is a positive observed sequence, not a score-causality claim.
- A joint culture complaint was followed by public VP/HR pressure and an offer to sign away compensation; the player de-escalated, refused the waiver, and explored alternatives. A new mentoring commitment was followed by a junior bypassing review and a test-environment outage. The player accepted shared process responsibility; later public feedback said prior hazards had exploded and recent work was wasted. This sequence does not isolate the role of any one action.
- Report preparation showed Output +1 in some fresh states (including M33 and M48) and no immediate projected change in others. Networking showed +1 in some states. A no-change projection is not evidence that no delayed effect occurred.
- One local bridge validation blocked the legal Main choice ID `2` after Energy choice ID `2` had been explicitly rejected; the action label/menu had changed, and no MCP call was made for the blocked input. The player used another legal action and completed the run. After terminal, the block was scoped to the same session/event/legal-menu context and covered by offline regression tests; this code change was not live-validated.
- Raw public trajectory: `.local/runtime/s07-15-codex-public-agent/R4/public-trajectory.jsonl`; 525,950 bytes; SHA-256 `24f15e623df6d672424039bfd45d8dd605fc4da0354a012f2199d4a6da4c103a`.

## Sequential learning and interpretation boundary

- R1→R2: R1 yielded no strategy evidence; the interactive launch was corrected. R2 focused on visible delivery after prior public feedback, but ended C/L4.
- R2→R3: the next-run focus included affordability and reducing commitments with explicit costs. R3 still ended at M12 with Wealth 0 and public debt language; the run is one adverse, unpaired path.
- R3→R4: the next-run focus kept wealth, concrete outcomes and public risk in view. R4 completed and reached L5, but remained C and scored below S07-14 (65.16/B). Neither comparison is a controlled comparator. R4 also had a later public risk-loss warning despite earlier cleanup actions.
- Scores were R2 54.85, R3 16.55, R4 57.90 after a technical-only R1. No public seed was found. These adaptive, unpaired runs show substantial variance; they do not establish causal improvement or a stable score basin.

## Safety accounting

- Fresh sessions / `new_game`: `4 / 4`; second/replacement sessions beyond the four slots: `0`.
- Direct MCP lifecycle starts / shutdowns: `4 / 4`; initialize/list_tools: `4 / 4`.
- Observes: `446`; `take_action` attempts: `442` (R2 195, R3 43, R4 204; R1 0). Of the 442 completed responses, 411 showed public state change, 29 showed unchanged projected state, and 2 were confirmed explicit rejections; transport-unknown outcomes: `0`.
- AgentServer `0`; DeepSeek/provider `0`; Runner gameplay `0`; Skill install/reload `0`; handbook calls `0`; hidden/private access `0`.
- Candidate/Skill/runtime manifest/Runner/dependency mutation `0`. No database content was inspected.

## Engineering delta

- The bridge's strict public projection was extended to retain allowlisted numeric ending-score dimensions when supplied as public mappings. This run's terminal payload did not match that mapping shape, so official per-dimension score values remain `UNKNOWN`.
- After R4 terminal, confirmed-rejection blocking was scoped to the same public session/event/legal-menu context, preventing an integer ID from remaining blocked when the menu changes. A synthetic regression test covers this; it does not add or choose gameplay policy.
