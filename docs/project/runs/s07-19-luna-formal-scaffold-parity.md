# S07-19｜Luna Formal Candidate Scaffold Parity Run

## Identity and scope

- Repository: `MyKr-YSteinsK/CareerSim-BDCI26`
- Base: `main@9602928e5fa3e5a087f8e8dbead63680deb093ea`; `origin/main` matched before and after the run.
- Closeout handoff verified: `FORMAL_CANDIDATE_SCAFFOLD_PARITY_READY`.
- Authorization: `AUTHORIZE_S07_19_LUNA_FORMAL_SCAFFOLD_PARITY` (`REPOSITORY_WRITE + TASK-SCOPED LIVE_RUN`).
- Live boundary: one direct participant-facing MCP lifecycle, one `new_game`, one fresh session, at most 350 action attempts; no second game, install/reload, AgentServer, provider, or Runner gameplay.
- Experimental variable: Codex/Luna decision making under the current formal Candidate controller; no S07-16 brief or historical strategy prior was used during gameplay.

## Formal Candidate loaded before gameplay

- Candidate: `candidate-v6c-compliance-cleanup`.
- Runtime manifest: `configs/runtime_manifest.json`, 1,870 bytes, SHA-256 `CF68E26F23B060372E1C75259C6EABE38B229F00788ECCDB9AEA71408AEEB4E1`; instruction SHA-256 `A891FA103F0D4F910C9BBCC5AB91AB8BBBFE4CB242B9506D63374F1CF75D8074`.
- Candidate config: `configs/current_candidate.json`, 3,555 bytes, SHA-256 `634CDC14D1EAC61193A265963B89217C2D0BEA9085491880076C009BC5221941`.
- Formal Skills were fresh-read before `new_game`:
  - `structured-state-board`: git blob `b6d371d74f3477f4f6cdeabe8482093a78cbe3e5`, file SHA-256 `E8C25306D108FEDF35039BDD25A1540947C6715099AB997FC12A35C8611C3992`.
  - `rolling-planning`: git blob `c4d2bfe065ee3c658e6cff041be87ae8c8c96bdf`, file SHA-256 `639197DC39C9E569FF7AB0DE837A17874419932ACDE914C7B2EFCA00E3BE83E6`.
  - `risk-review`: git blob `ab20843eadad675dbf7aa8be0178fb52a3791208`, file SHA-256 `83E7600B0DA901C18E78CD96D85A2E68A8B5EB9DFA0D7A8CF82F9266690D237D`.
- Direct bridge: `scripts/codex_public_agent_driver.py`, 30,430 bytes, SHA-256 `A236F4574E258934E8C8CD0B0F685446EAC418C6015450D4D254A8958449981F`. The current public schema accepted integer `choice`, string `notes`, and `session_id`; no bridge patch was needed. The bridge remained transport/projection/legality/reconciliation only.

## Player-phase evidence firewall

- Historical strategy prior during gameplay: `NO`.
- S07-16 Strategy Brief during gameplay: `NO`.
- Hidden/private evidence, DB contents, simulator source, evaluator weights, and other sessions during gameplay: `NO`.
- The only gameplay inputs were the current session's fresh public observations, current legal choices, public receipts, and the loaded formal controller.
- `show_employee_handbook` was not called. Unknown projected fields were discarded by the existing public allowlist.

## Runtime and outcome

- Direct MCP lifecycle start: `2026-09-26T14:24:22Z`; terminal/shutdown: `2026-09-26T14:42:49Z`; live wall-clock `18m27s`.
- Game session: `638c45c96e1c45838ba2ee52fd20f759`.
- Public terminal: Month 24, `outcome=eliminated`, `completed=false`, survival `24` months, grade `E`.
- Quantitative score: `28.89`; competition partial: `20.22`.
- Final public state: `Level L1 / Health 10 / Dignity 7 / Skill 9 / Network 1 / Output 3 / Wealth 7 / Energy 0`.
- Promotions: none.
- Final public review: `C`; the public terminal also states elimination after two unfavorable half-year performance reviews. This is recorded as public terminal evidence, not a hidden-threshold explanation.

## Public checkpoints

| Checkpoint | Level | Health | Dignity | Skill | Network | Output | Wealth | Evidence |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| M6 | L1 | 6 | 10 | 9 | 3 | 3 | 2 | reached |
| M12 | L1 | 6 | 10 | 8 | 3 | 3 | 3 | reached |
| M18 | L1 | 6 | 10 | 9 | 3 | 3 | 4 | reached |
| M24 | L1 | 10 | 7 | 9 | 1 | 3 | 7 | terminal |
| M30 | — | — | — | — | — | — | — | `NOT_REACHED` |
| M36 | — | — | — | — | — | — | — | `NOT_REACHED` |
| M42 | — | — | — | — | — | — | — | `NOT_REACHED` |
| M48 | — | — | — | — | — | — | — | `NOT_REACHED` |

## Compact adherence evidence

The local bounded controller ledger contains 98 records, one per explicit player decision, without chain-of-thought. Every recorded note used the canonical CTRL form; deterministic audit: `98/98` canonical notes, `0` malformed notes, `98` ledger records.

| Contract element | Result | Evidence boundary |
|---|---|---|
| Three Skills loaded before gameplay | `PASS` | Fresh-read files and hashes above; before `new_game` |
| Fresh observe before decisions | `PASS` | 99 public observes for 98 decisions; session identity stable |
| Board after fresh observe | `PASS` | Ledger records current public state and attributable effect separately |
| One Primary Gap | `PASS` | Each ledger record names one gap or `UNKNOWN` |
| Progress semantics | `PASS` | `ADVANCING`/`UNKNOWN` used; `STALLED` only after two comparable no-effect checks |
| Risk Budget semantics | `PASS` | Public warning/survival trend drove `TIGHT`; no hidden numeric threshold used |
| Candidate before Risk | `PASS` | Each ledger record separates candidate and Risk result |
| Candidate-specific Risk | `PASS` | Risk reviewed against the current legal candidate, not as a second planner |
| `DECISION_CLOSED` | `PASS` | Every decision record marks closed; the one rejection supplied new evidence before replanning |
| Energy one integer at a time | `PASS` | No array/bundle was submitted; every Energy action had a fresh observe afterward |
| Fresh observe after state-changing action | `PASS` | Bridge reconciliation performs one fresh observe after every action response |
| Review checkpoint/reset | `PASS` | M6, M12, and M18 feedback invalidated the prior Progress baseline and reset Planning |
| Pre-review reserve check | `PARTIAL` | Survival facts were considered in the surrounding Planning, but no separate explicit reserve-check record was captured before each half-year review |
| `STALLED` evidence gate | `PASS` | M6/M15/M18/M21 repeated Energy no-effect checks reached the two-checkpoint condition before switching |
| Context recovery epoch | `NOT_TRIGGERED` | No context-compression/recovery marker occurred |

## Safety accounting

| Operation | Count / result |
|---|---:|
| Direct MCP lifecycle | 1; safely closed |
| `initialize` / `list_tools` | 1 / 1 |
| `new_game` / fresh session | 1 / 1 |
| `observe` | 99 |
| `take_action` attempts | 98; 83 state-changed, 14 unchanged, 1 explicit rejection confirmed unchanged |
| Unknown side effects | 0 |
| Second game | 0 |
| AgentServer / provider / DeepSeek | 0 / 0 |
| Install / reload / Runner gameplay | 0 / 0 / 0 |
| Hidden/private access | 0 |
| Formal Candidate / Skill / manifest mutation | 0 |

The rejected Energy action was not resent. The bridge confirmed the same-session public state was unchanged, blocked that choice in the unchanged menu, and continued with a newly selected legal action.

## Evidence artifacts

- Public trajectory: `.local/runtime/s07-19-luna-formal-scaffold-parity/public-trajectory.jsonl`, 240,360 bytes, SHA-256 `71B92EC437B7316C5AC7FFEBF6C44685B14322AB20F847FA693173CA06321EA0`.
- Compact controller ledger: `.local/runtime/s07-19-luna-formal-scaffold-parity/controller-ledger.md`, 77,030 bytes, SHA-256 `7F4F3C30819BF0AC759921F9705D4944236B29F2E455AC945ADB14404C6FC4E9`.
- Local runtime raw directory: `.local/runtime/s07-19-luna-formal-scaffold-parity/`; SQLite/emulator logs were retained locally and were not opened for gameplay decisions or post-run comparison.

## Interpretation boundary

- FACT: formal Candidate files were loaded; the public Board → Planning → candidate → Risk → action loop was auditable for 98 decisions; the run ended naturally at M24 with `28.89 / 20.22 / E`.
- INFERENCE: this run does not support the claim that the prior Codex low scores were caused mainly by scaffold mismatch; the formal scaffold did not produce a better observed outcome in this unpaired session. The conclusion is weakened by the partial pre-review-reserve evidence and the unseeded trajectory.
- UNKNOWN: model-vs-scaffold attribution, repeatability, causal value of any Skill or action, hidden-test transfer, and 48-month formal-scaffold performance.

## Delivery

- Decision: `SCAFFOLD_PARITY_MIXED`.
- Candidate/scaffold implication: `defer`; no Candidate or Skill change is supported by this single unpaired run.
- Highest-value next boundary: Main review of the partial adherence evidence and the M24 elimination before authorizing any second parity game; no automatic rerun is implied.
- Final delivery commit: this record is included in the final pushed `main` commit; the exact SHA is recorded in the final TASK_RESULT response.
