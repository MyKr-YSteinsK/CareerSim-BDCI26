# S07-21｜Formal Candidate Scaffold Replication Run

## Identity and boundary

- Base: `main@63ddbd428586390ff34633856da155cc42520119`; `origin/main` matched and the working tree was clean before gameplay. S07-19 and S07-20 run/review artifacts were verified as present before gameplay, without reading their strategy or trajectory.
- Authorization: `AUTHORIZE_S07_21_FORMAL_SCAFFOLD_STRONG_HOST`, then explicit user authorization on 2026-09-27 to increase the MCP lifecycle limit from one to two **only to reconnect to the same game session after context compression**. One `new_game`, one session, and the 350-action ceiling remained unchanged.
- Candidate: `candidate-v6c-compliance-cleanup`; config 3,555 bytes / SHA-256 `634cdc14d1eac61193a265963b89217c2d0bea9085491880076c009bc5221941`.
- Manifest: 1,870 bytes / SHA-256 `cf68e26f23b060372e1c75259c6eabe38b229f00788eccdb9aea71408aeeb4e1`; instruction SHA-256 `a891fa103f0d4f910c9bbcc5ab91ab8bbbfe4cb242b9506d63374f1cf75d8074`.
- Three Skills were fresh-read before `new_game` and re-read after context compression: Board `e8c25306d108fedf35039bdd25a1540947c6715099ab997fc12a35c8611c3992`; Planning `639197dc39c9e569ff7ab0de837a17874419932acde914c7b2efca00e3be83e6`; Risk `83e7600b0da901c18e78cd96d85a2e68a8b5eb9dfa0d7a8cf82f9266690d237d` (file SHA-256).
- Player phase used only the loaded controller, current-session public observations, legal choices, receipts, and feedback. Historical trajectories, S07-16 brief, score targets, DB, simulator source, hidden fields, provider, AgentServer, and Runner gameplay were not used. Phase B historical references were read after public terminal and MCP shutdown.

## Runtime

- Direct MCP first start `2026-09-27T04:06:31Z`; paused at M42 Main after action 175. A deliberate terminal interrupt at `04:31:57Z` closed the first child at a confirmed action boundary; its local shutdown was logged as `ExceptionGroup`, without an in-flight action or unknown side effect.
- The user authorized one same-session reconnection. The bridge resumed with `--resume-session-id`, did **not** call `new_game`, and issued a fresh same-session `observe` at `04:32:14Z`. The three Skills were re-read and `RECOVERY_TRIGGERED` recorded. Second MCP lifecycle shut down after public terminal at `04:37:24Z`.
- Session: `46184830c0864ffba1381f718becbea7`. Public terminal after M48, shown at month 49. `outcome=completed`, `survival_months=48`, `completed=true`, quantitative `59.19`, competition partial `41.43`, grade `C`.
- Final public state: `L5 / Health 9 / Dignity 10 / Skill 102 / Network 37 / Output 29 / Wealth 24 / Energy 0`. Level transitions observed at M12 L2, M18 L3, M30 L4, M48 L5. No action was sent after terminal.

## Public checkpoints

Values are the last public `observe` at each named month. The M48 value precedes the final Main action; the terminal M49 observation above is the final state.

| Month | Level | H | D | Skill | Network | Output | Wealth |
|---|---|---:|---:|---:|---:|---:|---:|
| M6 | L1 | 7 | 10 | 9 | 2 | 3 | 1 |
| M12 | L2 | 9 | 7 | 11 | 5 | 4 | 0 |
| M18 | L3 | 8 | 10 | 25 | 7 | 8 | 3 |
| M24 | L3 | 9 | 10 | 37 | 10 | 16 | 6 |
| M30 | L4 | 9 | 10 | 48 | 19 | 18 | 8 |
| M36 | L4 | 10 | 9 | 58 | 21 | 26 | 14 |
| M42 | L4 | 9 | 9 | 82 | 29 | 26 | 19 |
| M48 | L5 | 9 | 10 | 101 | 36 | 27 | 23 |

## Adherence evidence and limits

- Public trajectory: 200 `player_decision`, 200 `take_action`, 202 `observe`, 1 `new_game`, 2 direct MCP starts/initializations/listings/shutdowns, 1 same-session resume, 1 terminal. Action responses: 193 state changed, 7 unchanged; no rejection, ambiguous transport outcome, or blind resend. All 200 notes matched the canonical CTRL pattern. Every choice was one legal integer, including Energy choices.
- The contemporaneous ledger has 65 action records, five explicit pre-review reserve records, three Planning checkpoints, and one recovery record. The reserve record was omitted in other reached pre-review windows, including M6, M36, and M47; this is `PARTIAL` and was not retrofitted as contemporaneous evidence.
- The audited ledger covers all 200 actions by pairing public pre/post observations and CTRL notes. Its other 135 rows are explicitly labelled `RETROSPECTIVE_PUBLIC_LOG_BACKFILL`; Risk Budget, horizon, recent effect, and rationale missing at decision time remain `NOT_RECORDED_CONTEMPORANEOUSLY`. This supports mechanical action/observation auditing, **not** a full claim that Board, Planning, and candidate-specific Risk were contemporaneously documented for those actions.
- Context recovery is `PASS` for the M42 restart: same session fresh-observed, three Skills re-read, Board/Planning rebuilt. The extra MCP lifecycle was user-authorized and is a deviation from the original one-lifecycle budget, not silently counted as one.
- The bridge remained `NO_POLICY_LOGIC`; its resume change only validates the recorded session/action boundary, appends evidence, skips `new_game`, and calls fresh `observe` before accepting another player choice. No Candidate, manifest, Skill, Runner, dependency, or lock file was changed.

## Local evidence

Retained under ignored `.local/runtime/s07-21-formal-scaffold-strong-host/`. Raw SQLite and emulator logs were not inspected for gameplay or comparison and are not committed.

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| `public-trajectory.jsonl` | 485,034 | `978aa535a6150b27f438f9ab53f6e8f2ca05e924a8de83112e47dc7110c6c055` |
| `controller-ledger.jsonl` | 37,688 | `c05e5ba6ed3acfc6f0682392b7e514e1b4015f85f571ebe02c3950dbc9fd2fda` |
| `controller-ledger-audited.jsonl` | 124,941 | `b2d4644be0dbaccbd79a0bbaa649d43871eec0feeaa265c5912051047b731218` |

The public runtime text in the JSONL contains some encoding replacement characters; structured public status, choice numbers, CTRL notes, and terminal score remain readable. This limits quotation of some raw story/feedback text.

## Verification and telemetry

- Root Python targeted bridge tests: `12 passed`; public mechanical probe tests: `18 passed`. The resume tests assert a same-session fresh `observe` without another `new_game` and reject an unreconciled action boundary. Live tool listing confirmed `observe.session_id` and `take_action.session_id/choice/notes`, with integer `choice`.
- Model Used: `UNKNOWN` at repository-verifiable specificity. Reasoning Effort: `UNKNOWN`. A model switch was discussed during pause but the user explicitly chose not to switch. Discussion is not telemetry that identifies the execution model.
- Live elapsed wall time from first start to final shutdown: `30m53s`, including the user pause and recovery. Started At `2026-09-27T04:06:31Z`; Finished At `2026-09-27T04:37:24Z`.
