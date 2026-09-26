# S07-14｜Codex Public-Agent Pilot v2 Run

## Identity and boundary

- Repository/base: `MyKr-YSteinsK/CareerSim-BDCI26`, `main@3eafd9f9d697b80828d4b86c5937af69eb5b0d0b`.
- Player: current Codex; each of 196 choices was entered explicitly after a fresh public observation. The bridge supplied transport, projection, legal-choice validation and evidence recording only; it had no action selector.
- Prior public game/strategy information was accepted by the user as a public prior. `NOT_A_BLINDED_POLICY_EVALUATION`; no hidden/private information was used.
- Candidate/Skills/runtime manifest/Runner/dependencies were not used as the gameplay policy and were not modified.

## Session and outcome

- Session: `63497628f19448db929ad9c2b6e04a56`.
- Direct MCP start: `2026-09-26T08:26:02Z`; public terminal: `2026-09-26T09:19:39Z`; same-process shutdown recorded at `09:19:40Z` (53m38s from start to shutdown).
- Public result: `outcome=completed`, `completed=true`, survival `48` months, grade `B`, `quantitative_score=65.16`, `competition_partial_score=45.61`.
- Terminal public status (administrative month 49): Health 10, Dignity 10, Skill 123, Network 53, Level L5, Output 37, Wealth 25, Energy 0. Public score-dimension breakdown was not retained by the strict projection (`ending_score.dimensions` was listed as ignored), so per-dimension scores are `UNKNOWN`.
- Public Level transitions: L1→L2 at M6; L2→L3 at M18; L3→L4 at M24; L4→L5 at M42.

## Decisions and observed patterns

- Decisions: 145 story choices, 35 Energy submissions, 16 Main actions.
- Main actions: choice 1 (申请关键项目) 11/16; choice 2 (向领导汇报成果) 2; choice 3 (主动争取资源) 1; choice 5 (主动曝光成果) 1; choice 6 (建立导师关系) 1.
- Energy submissions: high-intensity work 5; skill learning 5 (including one rejected attempt); network maintenance 3; historic-risk cleanup 5; health recovery 13; report preparation 4. No mental-recovery or reserve action was submitted.
- Public feedback repeatedly distinguished “being busy” from producing visible wins. The player varied story responses and used process, transparency and safety considerations; it continued to select critical projects frequently while also adding reports, resourcing, exposure and mentoring actions.
- High-intensity work was sometimes followed by health recovery after a fresh public state showed the health cost. At M48, Health recovery raised public Health from 8 to 10; report preparation raised Output from 34 to 35; the subsequent skill-learning request was rejected and did not change projected state. The bridge did not resend it; Codex selected network maintenance, then a legal critical-project Main action. The final state advanced to the public terminal result.
- A public release mistake after an untested merge was followed by choosing a release checklist. During a public migration/sales conflict, the player deferred an unsafe migration and committed to a bounded post-promotion plan. These are single-run behavioral observations, not causal findings.
- The bridge records final submitted decisions, not unsubmitted deliberation; oscillation and hidden internal reasoning are therefore not measurable. No formal Skill/Board/Risk marker or `STALLED` label is part of this Codex-as-Player run.

## Action reconciliation and evidence

- `new_game=1`; initialize/list_tools `1/1`; observe `197`; explicit player decisions `196`; `take_action` attempts `196`.
- MCP receipts: `success=true` 195; one `success=false` at M48. That completed response was followed by one fresh same-session observe, which confirmed unchanged projected state; it was classified as `EXPLICIT_ACTION_REJECTION_CONFIRMED`. The rejected choice was not resent. There were 184 projected state changes and 11 projected unchanged comparisons across the 196 responses; unchanged comparison alone is not treated as a rejection.
- One lifecycle: direct MCP start/shutdown `1/1`; AgentServer `0`; provider/DeepSeek `0`; Runner gameplay `0`; Skill install/reload `0`; second game `0`; `show_employee_handbook` calls `0`.
- Local ignored public trajectory: `D:\CS\CareerSim\.local\runtime\s07-14-clean-codex-public-agent\public-trajectory.jsonl`; 490,064 bytes; SHA-256 `52ee26dee5468cf22891026deb7a967874539d57466806c99baad2d0e8f1b81f`.
- No database contents were read. A post-shutdown process check found no matching CareerSim MCP or pilot bridge process.

## Evidence boundary

This is one unpaired public-information run with no public seed control established for this session. It demonstrates one completed 48-month trajectory and one successful rejection-reconciliation path; it does not establish policy superiority, causal score benefit, repeatability, stable 80+, Candidate effectiveness, or hidden-test transfer. Token/cache and billed-cost data for Codex itself were unavailable; provider usage was zero.
