# S07-17｜Targeted Codex Public-Agent 三局探索记录

## Identity / evidence boundary

- Repository: `MyKr-YSteinsK/CareerSim-BDCI26`; base `main@8bc408709e442186a3ca368dfd03cd55836e575d` (`origin/main` matched before execution).
- Mode: public-prior strategy discovery using the S07-16 Strategy Brief; not blinded evaluation.
- Decision maker: Codex LLM, one explicit choice per fresh public state. The Python bridge performed transport, projection, legality checks and logging only; no automated policy selector was used.
- Candidate at task start: `candidate-v6c-compliance-cleanup`. Candidate, Skills, runtime manifest, Runner, dependencies, `CURRENT_STATE.md` and ADR were not modified.
- Evidence used for strategy: participant-visible current session state/events/choices/receipts, the required S07-16 Strategy Brief, and after gameplay the committed public S07-16 comparison. No simulator internals, DB contents, hidden effects/thresholds, evaluator formula, or private/test data were used.

## Run outcomes

| Run | Session | Start–shutdown (UTC) | Quantitative | Partial | Survival | Grade | Completed | Final public state (Level / Health / Dignity / Skill / Network / Output / Wealth) | Promotions |
|---|---|---|---:|---:|---:|---|---|---|---|
| R1 | `f7a48e8136854d3ba581d53706f546f3` | 12:16:03–12:29:08 | 21.36 | 14.95 | 24m | E | No; eliminated | L1 / 6 / 5 / 8 / 2 / 3 / 7 | None |
| R2 | `136c31073ab74eb387126c5c8f1138b6` | 12:30:30–12:41:56 | 22.82 | 15.97 | 24m | E | No; eliminated | L1 / 9 / 5 / 9 / 1 / 3 / 4 | None |
| R3 | `66314beadade472ebd0242ded24f2075` | 12:42:41–13:03:40 | 63.88 | 44.72 | 48m | B | Yes | L5 / 10 / 10 / 93 / 38 / 26 / 27 | M12, M18, M30, M48 |

R1 and R2 ended after the M24 review window. R3’s public ending score reports completion at 48 months; the terminal public clock advanced to M49 after the final action. Its last review checkpoint at M48 was L5 / Health 10 / Skill 93 / Network 38 / Output 25 / Wealth 26; the terminal state then showed Output 26 / Wealth 27.

## Public checkpoints

Tuple: `Level / Health / Skill / Network / Output / Wealth`. Months after termination are `NOT_REACHED`.

| Run | M6 | M12 | M18 | M24 | M30 | M36 | M42 | M48 |
|---|---|---|---|---|---|---|---|---|
| R1 | L1/5/9/2/2/2 | L1/10/9/3/3/3 | L1/7/8/2/3/5 | L1/6/8/2/3/7 | NOT_REACHED | NOT_REACHED | NOT_REACHED | NOT_REACHED |
| R2 | L1/5/9/3/3/2 | L1/6/9/0/2/2 | L1/6/9/3/3/3 | L1/9/9/1/3/4 | NOT_REACHED | NOT_REACHED | NOT_REACHED | NOT_REACHED |
| R3 | L1/9/9/3/3/2 | L2/8/11/7/2/3 | L3/9/25/5/11/6 | L3/10/42/18/16/6 | L4/10/44/20/19/9 | L4/8/62/33/25/14 | L4/10/78/36/25/19 | L5/10/93/38/25/26 |

### Promotion and review sequence

- **R1:** M6 C asked for progress, collaboration and risk awareness; M12 repeated C; M18 and M24 were D. No promotion; terminal review resulted in termination.
- **R2:** M6 C asked for clearer results; M12 C said baseline/no standout; M18 and M24 were D, with explicit collaboration/risk/output concerns and a final adjustment window. No promotion; terminated at M24.
- **R3:** M6 C said output was insufficient; M12 C repeated progress/collaboration/risk concerns, followed by L1→L2 promotion; M18 B and L2→L3 promotion, with public collaboration-friction note; M24 B repeated “busy, not winning”/same-standard feedback; M30 B and L3→L4 promotion; M36 B, no promotion; M42 A said delivery/communication/partner feedback were good and asked to prepare materials; M48 A and L4→L5 promotion.

These are public sequences only. A review grade or promotion month is not a hidden threshold and no individual action is attributed as its cause.

## Action distributions

Counts are selected public actions, not energy units or measures of quality.

| Run | Main actions | Energy actions |
|---|---|---|
| R1 | Resources 2; report results 2; expose results 1; key project 1; mentor 1 | Health recovery 4; Skill 2; historical-risk cleanup 3; reporting prep 1; network 3; high intensity 1; reserve 1 |
| R2 | Resources 2; report results 2; key project 2; low-profile risk 1 | Health recovery 5; high intensity 1; historical-risk cleanup 5; network 3; reporting prep 1 |
| R3 | Report results 6; resources 4; key project 4; low-profile risk 1; expose results 1 | Network 6; historical-risk cleanup 7; high intensity 6; reserve 6; health recovery 4; reporting prep 4 |

R1/R2 each recorded 92 successful actions and 93 public observations. R3 recorded 194 successful actions and 195 public observations. The bridge categorized 17 / 12 / 14 successful responses respectively as `ACTION_RESPONSE_STATE_UNCHANGED` in its conservative public-state comparison; every receipt had `success=true`, so these were not rejected actions.

## Three control signals

### A｜Review-to-Result

- **R1/R2:** repeated C→D feedback was not followed by a visible promotion or Output increase by M24; neither run converted the feedback sequence into a demonstrated review recovery.
- **R3:** no clear progress by M12; subsequent public reviews improved to B at M18/M24/M30/M36 and A at M42/M48, with L3 by M18 and L5 by M48. This shows the signal can keep a requested outcome open until later evidence appears, but does not prove the tracking or any one action caused the improvement.
- **Assessment:** the most informative of the three signals for structuring decisions and avoiding “activity = result”; causal or incremental value remains unknown.

### B｜Opportunity-to-Delivery

- R3 distinguished project applications/feasibility from completed delivery. An M39 CI-automation exploration was publicly feasible but more complex than expected; no explicit completion receipt was recovered. The M45 customer demo was planned, but no result was observed before terminal. M42 feedback did report stable delivery and positive partner feedback without naming a specific project.
- A platform launch had public on-time/business-satisfaction evidence, but a later CVE concern had no public closure evidence.
- **Assessment:** useful as an evidence discipline; delivery attribution remained incomplete, so this signal did not identify a single project-to-score mechanism.

### C｜Affordability

- R3 Wealth was positive throughout the checkpoints, rising 1→2→3→6→6→9→14→19→26 (27 at terminal); no public debt, negative-cash or affordability warning appeared.
- R1 and R2 also ended with positive Wealth (7 and 4) but were eliminated at M24 with L1/Output 3.
- **Assessment:** no trigger was observed in R3; positive Wealth did not distinguish progression or survival in this three-run set. Keep it as a public constraint monitor, not a wealth-maximizing target.

## Critical decisions and mistakes

- R3 used early transparent customer scoping and phased delivery; M9 clarified a client’s misunderstanding about the forecast, and later sought written scope/acceptance evidence.
- At M21 a cross-team dependency was not escalated early enough; the partner still missed the date, and a VP said the warning arrived late. The run then requested formal dependency monitoring. This is evidence for earlier owner/date alignment, not for escalation as a universal first move.
- Around M27, a vague warning about an unconfirmed restructuring was shared with a colleague; the leader later identified a leak. The player acknowledged the error and moved teams. This was the clearest confidentiality mistake; do not circulate unverified organizational information.
- At M39, the bounded feasibility test showed a new technical direction was feasible but more complex than expected. The player disclosed the result and asked the team to reassess rather than promise unresourced solo delivery.
- At M42, the A review and explicit request for promotion materials were tracked. A subsequent medical leave for serious insomnia/attention symptoms was appropriate, but it delayed a milestone by a week and exposed a delivery-buffer weakness; the public record does not support treating leave itself as a performance error.
- At M45, one reporting-prep action, one high-intensity action and a results report produced no immediate observed Output increase in the next public status. The following migration decision favored delay because the DBA said rollback was untested and it conflicted with a major promotion; after product accepted delay and public support expiry was raised, the player chose a bounded post-promotion migration plan.
- M48 ended with L4→L5 promotion. The final report/exposure action preceded the terminal score, but no causal score attribution is possible.

## Cross-run learning and comparison

- **R1→R2:** R2 attempted earlier owner/date coordination, explicit delivery evidence and separate affordability monitoring. The terminal result barely changed descriptively: 22.82 vs 21.36, both M24/E/L1/Output 3; R2 had lower Wealth (4 vs 7). These runs do not show that the adjustments changed the progression failure.
- **R2→R3:** R3 sustained review-to-result, opportunity-vs-delivery and affordability notes, and made more focused public ownership/quality decisions. It completed 48 months and reached L5/Output 26/Wealth 27. This is a large descriptive change, but the unseeded events, opportunity paths and decisions differ; it is not a causal estimate.
- **75+ references:** Candidate v1 #1 (76.04) and v6 #1 (75.29) were L2/O5–6/W2–3 at M6, L3/O7/W4 at M12, L4/O16–17/W6–8 at M18, L4/O26/W10–11 at M24, and L6/O40/W38–39 at M48. R3 was L1/O3/W2 at M6, L2/O2/W3 at M12, L3/O11/W6 at M18, L3/O16/W6 at M24, and L5/O26/W27 at M48. R3’s earliest visible divergence is M6 and the progression/output/Wealth gap persists through M24 and M48.
- **S07-14:** R3 completed at 63.88/B/L5, 1.28 quantitative points and 0.89 partial points below 65.16/45.61/B/L5. R3 ended Health 10, Skill 93, Network 38, Output 26, Wealth 27; S07-14 ended Health 10, Skill 123, Network 52, Output 37, Wealth 25. Different unpaired sessions prevent causal interpretation.
- **Primary bottleneck observed:** not survival in R3, but early progression and later public Output/Wealth/Level accumulation relative to 75+ references. Exact score weights are not inferred. The same-candidate v1 76.04 vs 35.31 counterexample and S06 16/16 key-project 53.83 counterexample remain reasons not to turn counts into policy rules.

## Bounded hypotheses (all LOW confidence)

1. **Review request → named, verifiable next-window result.** Evidence: R1/R2 repeated C/D and no Level/Output movement; R3 moved from early C feedback to later B/A and promotion. Counterevidence: different event paths and many simultaneous decisions; R3 still lagged high references and did not reach 70. Next test: observe one review request, chosen delivery evidence and the next comparable review/state, without fixed month/action thresholds.
2. **Promotion/progression gap is visible by M6–M24, but cause is unresolved.** Evidence: R3 and earlier Codex runs lag the M18/M24 Level/Output/Wealth checkpoints of both 75+ references. Counterevidence: unpaired stochastic runs; public opportunity mix differs. Next test: another authorized Codex run recording stage-level public commitments, accepted delivery and review evidence.
3. **Opportunity and delivery should remain separate; affordability is a guard, not the target.** Evidence: R3’s feasibility succeeded without a confirmed implementation receipt; positive Wealth coexisted with poor R1/R2 progression. Counterevidence: M42 feedback praised stable delivery and partner response; no public debt warning appeared in this batch. Next test: record explicit public acceptance/completion and stated cost effects when present.

## Evidence files and safety accounting

Only the local public trajectory JSONL files were parsed for this record; the runtime-created SQLite files in the same ignored folders were not opened or analyzed. Raw evidence remains local and is not committed.

| Run | Local public trajectory | Bytes | SHA-256 | Starts / initialize / list_tools / new_game / observe / take_action / shutdown |
|---|---|---:|---|---|
| R1 | `.local/runtime/s07-17-targeted-codex/R1/public-trajectory.jsonl` | 230575 | `8d8fc57052ca3ae4247ee42eee76e4e0cffed0da217b834f364c5bba75185d4d` | 1 / 1 / 1 / 1 / 93 / 92 / 1 |
| R2 | `.local/runtime/s07-17-targeted-codex/R2/public-trajectory.jsonl` | 232869 | `d47ace353aee941287bb71312106c629d24fa106184cad38d6dd851e235a2c0c` | 1 / 1 / 1 / 1 / 93 / 92 / 1 |
| R3 | `.local/runtime/s07-17-targeted-codex/R3/public-trajectory.jsonl` | 489633 | `b8df780c1efa594007c912b1afe1f9df2e51128a6c78497c8de876641e245d07` | 1 / 1 / 1 / 1 / 195 / 194 / 1 |

- Total: 3 sessions; 3 `new_game`; 381 observe calls; 378 `take_action` attempts, 378 successes, 0 explicit rejections, 0 unknown outcomes; 3 direct MCP lifecycles, each shut down.
- AgentServer starts: 0. DeepSeek/provider calls: 0. Runner gameplay: 0. Hidden/private evidence access: 0. Formal Candidate/Skill mutation: 0.
- The end-to-end window from R1 direct-MCP start to R3 shutdown was 47m37s (UTC); total task wall-clock including preparation/reporting is not reliably available.

## Decision

`TARGETED_PRIOR_MIXED` — R3 completed 48 months and reached L5/A reviews at the final two checkpoints, but scored 63.88/B, below S07-14’s 65.16 and well below the 75+ references. The feedback signal appears useful as an observation discipline; opportunity-to-delivery evidence was incomplete and affordability did not activate. No formal Candidate change is supported by these three unpaired sessions.

**Next recommendation:** return to Main for review of the public evidence and decide whether one further targeted Codex run is worthwhile. No additional game is authorized by S07-17.
