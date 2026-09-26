# S07-13｜Codex Public-Agent Pilot Review

## Decision

**`CODEX_PUBLIC_AGENT_PILOT_INCONCLUSIVE`**

The single direct-MCP session reached public month 3, but the final `take_action` returned `success=false` without an explicit rejection reason/status. The outcome could not be reconciled inside the one authorized MCP lifecycle. No resend, new server start, or second game was attempted. The run therefore provides neither a completed gameplay result nor a valid assessment of long-horizon Codex policy.

## Identity and implementation

- Repository/base: `MyKr-YSteinsK/CareerSim-BDCI26`, `da5846d6633492315af0c9c6e96dce3c8c898800`.
- Current branch at execution: `main`; Candidate identity remained `candidate-v6c-compliance-cleanup`.
- Added a small interactive driver at `scripts/codex_public_agent_driver.py`. Its module-level contract is `NO_POLICY_LOGIC`: it starts one direct stdio MCP child, projects an allowlisted public snapshot, validates explicit player input against current legal integer choices, sends that choice, and requests fresh observe after a clearly returned success or rejection. It has no automatic selector or fallback; ambiguous outcomes stop.
- Added targeted offline tests at `tests/test_codex_public_agent_driver.py`.
- Executed driver SHA-256: `3D561C8E69F6BB43FBD49BFFDBFC4F034EAE9876E0DBB0F434E2CD152ECF6F45`.
- Required public tools were present: `new_game`, `observe`, `take_action`; `take_action.choice` was declared integer. No public seed/replay control was exposed.

## Live accounting

| Operation | Count / result |
|---|---|
| Direct MCP start / shutdown | 1 / 1 |
| MCP initialize / list_tools | 1 / 1 |
| `new_game` | 1 |
| `observe` | 13 |
| `take_action` requests | 13: 12 `success=true`, 1 `success=false` with unresolved effect |
| AgentServer / provider / DeepSeek | 0 / 0 / 0 |
| Runner gameplay / install / reload | 0 / 0 / 0 |
| Second game | 0 |

At post-stop read-only inspection, no matching MCP/AgentServer process or known service port remained active. The local trajectory is retained, ignored by Git, and hashed in the run record. The local database was not inspected.

## Context contamination and validity

The user explicitly accepted continuing despite prior conversation contamination. Before play, the conversation already contained extensive historical S06/S07 outcomes and policy discussion, and the S07-04 engineering report exposed an earlier one-choice smoke. During bridge inspection, the first 240 lines of `scripts/public_mechanical_probe.py` were also read, including its mechanical policy classes and public action labels; this exceeded the minimum transport-only read intended by the firewall. This was an avoidable execution issue.

No historical action distribution or mechanical policy was intentionally applied to the live decisions, and the bridge itself does not call those classes. However, exposure cannot be undone or independently prove that reasoning was unaffected. Treat all decision observations as **contaminated, descriptive-only evidence**; this run is not a clean test of Codex open-policy reasoning.

## Evidence boundary

- Last confirmed public state: year 1 / month 3 / quarter 1; Level L1, Health 6, Dignity 10, Skill 8, Network 1, Output 3, Wealth 1, Energy 1; public terminal flag false.
- Twelve completed action receipts reported success and were followed by same-session fresh observations.
- The thirteenth action request was Skill learning. The returned receipt was exactly `success=false` with no explicit reason or rejection classification. The bridge stopped without resend. No fresh observe followed that response; effect remains `UNKNOWN`.
- Final grade, quantitative score, competition partial score, survival duration, and promotion outcomes beyond the partial month-3 state are unavailable. No post-terminal comparison was performed.
- The evidence does not establish policy weakness, policy benefit, survival ability, score, or route viability.

## Verification

- Targeted bridge tests: `4 passed`.
- Python compile and offline `--help`: passed without starting MCP.
- `git diff --check`: passed before documentation closeout; rerun before commit.
- Candidate, Skills, runtime manifest, Runner, dependency lock, and shared JiuwenSwarm runtime were not modified.
- No provider credentials were added to the bridge child environment; no AgentServer/provider request was made.

## Recommendation

Return to Main for review of the ambiguous public action receipt and the contamination limitation. Any continuation requires a new, explicit live authorization; this Task does not authorize another MCP start or game.
