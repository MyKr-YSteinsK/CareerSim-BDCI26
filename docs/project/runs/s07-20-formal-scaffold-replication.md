# S07-20｜Formal Candidate Scaffold Strong-Host Replication

## Identity and scope

- Repository: `MyKr-YSteinsK/CareerSim-BDCI26`
- Base: `main@99fa141db649325d08d6ab59a36011033fa10c61`; `origin/main` matched before the live run.
- Authorization: `AUTHORIZE_S07_20_FORMAL_SCAFFOLD_REPLICATION` (`REPOSITORY_WRITE + TASK-SCOPED LIVE_RUN`).
- Live boundary: one direct participant-facing MCP lifecycle, one `new_game`, one fresh session, `take_action attempts <= 350`; no second game, install/reload, AgentServer, provider, or Runner gameplay.
- Experimental boundary: one descriptive replication under the current formal Candidate controller; this is not a formal A/B test and does not identify model/host causality.

## Formal Candidate loaded before gameplay

- Candidate: `candidate-v6c-compliance-cleanup`.
- Candidate config: `configs/current_candidate.json`, 3,555 bytes, SHA-256 `634CDC14D1EAC61193A265963B89217C2D0BEA9085491880076C009BC5221941`.
- Runtime manifest: `configs/runtime_manifest.json`, 1,870 bytes, SHA-256 `CF68E26F23B060372E1C75259C6EABE38B229F00788ECCDB9AEA71408AEEB4E1`.
- Runtime instruction SHA-256: `A891FA103F0D4F910C9BBCC5AB91AB8BBBFE4CB242B9506D63374F1CF75D8074`.
- Formal Skills were fresh-read before `new_game`:
  - `structured-state-board`: git blob `b6d371d74f3477f4f6cdeabe8482093a78cbe3e5`, file SHA-256 `E8C25306D108FEDF35039BDD25A1540947C6715099AB997FC12A35C8611C3992`.
  - `rolling-planning`: git blob `c4d2bfe065ee3c658e6cff041be87ae8c8c96bdf`, file SHA-256 `639197DC39C9E569FF7AB0DE837A17874419932ACDE914C7B2EFCA00E3BE83E6`.
  - `risk-review`: git blob `ab20843eadad675dbf7aa8be0178fb52a3791208`, file SHA-256 `83E7600B0DA901C18E78CD96D85A2E68A8B5EB9DFA0D7A8CF82F9266690D237D`.
- Bridge: `scripts/codex_public_agent_driver.py`, 30,430 bytes, SHA-256 `A236F4574E258934E8C8CD0B0F685446EAC418C6015450D4D254A8958449981F`.
- Bridge result: no patch was needed. The bridge remained transport/projection/legality/reconciliation only (`NO_POLICY_LOGIC`).

## Player-phase evidence firewall

- Historical strategy prior used during gameplay: `NO`.
- S07-19 trajectory/action sequence used during gameplay: `NO`.
- Historical score targets used during gameplay: `NO`.
- Hidden/private evidence, DB contents, simulator source, evaluator weights, and other sessions used during gameplay: `NO`.
- Player-phase inputs were limited to the current session’s fresh public observations, legal choices, public feedback, and the fresh-read formal controller.
- S07-19 and other historical evidence was read only after public terminal and direct MCP shutdown.
- The public bridge discarded unknown projected fields; `show_employee_handbook` was not called.

## Verification before live run

- `git fetch origin`: passed.
- `HEAD == origin/main == 99fa141db649325d08d6ab59a36011033fa10c61` before live execution: passed.
- Working tree clean before live execution: passed.
- S07-19 run/review files present: passed.
- Shared runtime process check: no `career-emulator-mcp`, AgentServer, or Runner process before launch: passed.
- Root environment: Python 3.12.13.
- `tests/test_codex_public_agent_driver.py`: `10 passed`.
- `tests/test_public_mechanical_probe.py`: `18 passed`.
- Public schema/behavior check: `new_game`, `observe`, and `take_action` listed; `observe.session_id` and `take_action.session_id/choice/notes` present; `choice` declared integer and `notes` declared string; passed.
- Initial `git diff --check`: passed.

## Runtime and outcome

- Direct MCP start: `2026-09-26T15:01:53Z` (`2026-09-26 23:01:53 +08:00`).
- Terminal and shutdown: `2026-09-26T15:18:51Z` (`2026-09-26 23:18:51 +08:00`).
- Live wall-clock: `16m58s`.
- Game session: `e3e175e2b286478fa3266f614f606134`.
- Public terminal: Month 24, `outcome=eliminated`, `completed=false`, survival `24` months, grade `E`.
- Quantitative score: `16.98`.
- Competition partial: `11.89`.
- Final public state: `L1 / Health 5 / Dignity 5 / Skill 9 / Network 2 / Output 3 / Wealth 4 / Energy 0`.
- Promotions: none.
- Action response reconciliation: `80` public state changes, `16` unchanged responses; no rejected action, transport ambiguity, or unknown side effect.

## Public checkpoints

Checkpoint values below are the last fresh public observe at each reached month; review-feedback details are also retained in the compact ledger.

| Checkpoint | Level | Health | Dignity | Skill | Network | Output | Wealth | Evidence |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| M6 | L1 | 9 | 10 | 9 | 3 | 3 | 2 | reached |
| M12 | L1 | 10 | 10 | 9 | 3 | 3 | 1 | reached |
| M18 | L1 | 8 | 7 | 9 | 3 | 3 | 2 | reached |
| M24 | L1 | 5 | 5 | 9 | 2 | 3 | 4 | terminal |
| M30 | — | — | — | — | — | — | — | `NOT_REACHED` |
| M36 | — | — | — | — | — | — | — | `NOT_REACHED` |
| M42 | — | — | — | — | — | — | — | `NOT_REACHED` |
| M48 | — | — | — | — | — | — | — | `NOT_REACHED` |

## Compact adherence audit

The local ledger has 96 canonical CTRL records for 96 explicit actions and contains no private chain-of-thought. The public trajectory has 97 observes for 96 actions, with stable session identity.

| Contract element | Result | Evidence boundary |
|---|---|---|
| Exact current three Skills loaded before gameplay | `PASS` | Fresh-read files and identities above, before `new_game` |
| Current-session-only firewall | `PASS` | No historical strategy/trajectory/score target or private evidence in Player Phase |
| Fresh observe | `PASS` | 97 public observes for 96 actions; session remained stable |
| Board | `PASS` | Ledger separates current public facts and attributable/unknown effects |
| One Primary Gap | `PASS` | Each decision record names one gap or `UNKNOWN` |
| Progress semantics | `PASS` | `ADVANCING`/`UNKNOWN`; strict repeated no-progress comparison used before the M12 path switch |
| Risk Budget | `PASS` | Public warnings and visible trends only; no hidden numeric threshold |
| Candidate before Risk | `PASS` | Candidate and gate are recorded separately |
| Candidate-specific Risk | `PASS` | Risk gate is tied to the current legal candidate |
| `DECISION_CLOSED` | `PASS` | Final CTRL gate was submitted without reopening after new evidence was absent |
| Energy one integer at a time | `PASS` | No array/bundle action was submitted; each Energy action was followed by fresh observe |
| Post-action fresh observe | `PASS` | Bridge reconciliation observed after every action response |
| Review reset/checkpoint | `PASS` | M6, M12, and M18 formal feedback invalidated prior Progress and rebuilt Planning |
| Pre-review reserve | `PARTIAL` | M6 window received an explicit reserve record; M12 and M18 windows were reached without a contemporaneous separate reserve record. The limitation is recorded, not retrofitted. |
| `STALLED` contract | `PASS` | The report-preparation path was only switched after two adjacent comparable no-progress observations |
| Context recovery | `NOT_TRIGGERED` | No compression/recovery marker occurred |

## Safety accounting

| Operation | Count / result |
|---|---:|
| Direct MCP lifecycle | 1 start / 1 safe shutdown |
| `initialize` / `list_tools` | 1 / 1 |
| `new_game` / fresh session | 1 / 1 |
| `observe` | 97 |
| `take_action` attempts | 96 |
| Second game | 0 |
| Unknown side effects | 0 |
| AgentServer / provider / DeepSeek | 0 / 0 / 0 |
| Runner gameplay | 0 |
| Install / reload | 0 / 0 |
| Hidden/private access | 0 |
| Formal Candidate / Skill / manifest mutation | 0 |

SQLite and emulator-log files generated under the task-scoped ignored runtime directory were retained locally and were not opened for gameplay decisions or post-terminal comparison.

## Evidence artifacts

- Public trajectory: `D:\CS\CareerSim\.local\runtime\s07-20-formal-scaffold-replication\public-trajectory.jsonl`, 234,496 bytes, SHA-256 `88DCEAEFB5942C744A7CBD0766C8A40A6F4552224766DCE08EBE25BC06B965F`.
- Compact controller ledger: `D:\CS\CareerSim\.local\runtime\s07-20-formal-scaffold-replication\controller-ledger.md`, 66,447 bytes, SHA-256 `241FC1C50BB5CA560718EA17B6A34154C58517BACBB1B88E29CABBE202C5655F`.
- Raw local directory: `D:\CS\CareerSim\.local\runtime\s07-20-formal-scaffold-replication\`.

## Interpretation boundary

### FACT

- The current formal Candidate and three Skills were fresh-read and used through one direct public MCP game.
- The session produced 96 explicit actions, 97 public observes, and an auditable canonical CTRL ledger.
- The public terminal was M24 elimination with `16.98 / 11.89 / E`; M30–M48 were not reached.
- At M18 the public review was adverse, and at M24 the public terminal stated that two unfavorable half-year reviews led to elimination.

### INFERENCE

- This replication provides no stronger descriptive gameplay signal than S07-19; it is lower in score and ends at the same month/grade region.
- Because formal loop adherence was substantial but the run was unseeded/unpaired and pre-review reserve evidence was partial, the observation is most consistent with `STRONG_HOST_NO_SIGNAL`, not a proof that host/model capability has no effect.
- The low result makes scaffold/Candidate policy a reasonable review hypothesis, especially the translation from visible actions to promotion/recognition, but it is not a causal conclusion.

### UNKNOWN

- Model/decision-host contribution versus scaffold/policy contribution.
- Counterfactual trajectory under the same event path.
- Repeatability, hidden-test transfer, stable 48-month adherence, and any causal value of an individual Skill or action family.
- Whether the M18–M24 adverse public outcome would recur under another unseeded trajectory.

## Execution metrics

- Model Used: `UNKNOWN`.
- Reasoning Effort: `UNKNOWN`.
- Started At: `2026-09-26T15:01:53Z` (direct MCP live run).
- Finished At: `2026-09-26T15:18:51Z` (public terminal and shutdown).
- Actual Wall-clock: `16m58s` for the live run; total task wall-clock not separately captured.

## Execution issues

- Avoidable Execution Issues: `1`.
- Category: `controller_ledger / pre_review_reserve_recording`.
- Consumed Live Budget: `NO`.
- Prevention Candidate: emit and verify the explicit reserve record before every last action window preceding a known half-year review, rather than relying on surrounding Planning text.

## Delivery boundary

- Candidate, manifest, Skills, Runner, dependencies, `CURRENT_STATE.md`, and ADRs were not modified.
- The exact final delivery commit is recorded in the final TASK_RESULT response after push; no historical runtime raw files are committed.
