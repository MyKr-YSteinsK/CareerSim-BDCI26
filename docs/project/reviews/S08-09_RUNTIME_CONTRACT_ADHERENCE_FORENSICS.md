# S08-09｜Runtime Contract Adherence Forensics

## TASK_RESULT｜S08-09

**Status:** COMPLETE — four root-cause workstreams closed within the offline scope.<br>
**Decision:** `BOTH_RUNTIME_AND_AUDITOR_PATCH_JUSTIFIED`<br>
**Base:** `main@594cf755d489d0693b958f04c40e7e3d5d85c337`<br>
**Run / Candidate:** S08-RUN03 / `candidate-v7t-execution-semantic-repair`<br>
**Session:** `7f50220814214d97a3dc453fca049a79`<br>
**Candidate/Skill/manifest/retry/Runner/dependency changes:** none.<br>
**FORENSIC_HOLD:** ACTIVE pending Main/Stage review. `NEXT_GAME=NOT_AUTHORIZED`.

This is an offline analysis of the exact S08-RUN03 archive. It did not contact a Provider, start a service, call MCP, read the shared DB, invoke Runner/gameplay, or alter the Candidate. The evidence archive remains byte-identical to its manifest. No transcript private narration was copied into the derived JSON.

## Evidence identity and priority

The exact archived inputs were checked against [evidence-manifest.json](../../../artifacts/dev-runs/s08-run03-v7t/evidence-manifest.json), then session-bound to the one `new_game` result and all 207 action / 190 observe calls. The Runner result is explicitly reconstructed from interactive stdout; it has no session field of its own and agrees with the exact session-bound score report and output directory.

| Archived file | Bytes | SHA-256 |
|---|---:|---|
| [events.jsonl](../../../artifacts/dev-runs/s08-run03-v7t/events.jsonl) | 1,892,046 | `c630579d5ebbcdbcecf9f6eee1104434b75cb92a9f3915cdbf4a5c1084e21fdb` |
| [transcript.log](../../../artifacts/dev-runs/s08-run03-v7t/transcript.log) | 547,255 | `528ca2630d5b8c5c26bb5cb5f8879421d4f53543dbe1f93834cf68a9b8f16747` |
| [score_report.json](../../../artifacts/dev-runs/s08-run03-v7t/score_report.json) | 2,744 | `1a5de612048a5368b10b3d9fb153d98dac1bdfcf250347d5c20a6e111f2bdff0` |
| [runner-result.json](../../../artifacts/dev-runs/s08-run03-v7t/runner-result.json) | 841 | `ba2ffd47c1e10ab95dfcc732d3082e169ea0c253322a26ce9eaf95bd19ca65ad` |
| [post_run_summary.json](../../../artifacts/dev-runs/s08-run03-v7t/post_run_summary.json) | 192,559 | `d1f719e946473f0a06d11742f3097961a16b4182bdeb9b5fc421a92323134ec1` |
| [evidence-manifest.json](../../../artifacts/dev-runs/s08-run03-v7t/evidence-manifest.json) | 1,131 | `b0b362159414827ff4062b7fa2322a151c51ab4540398c8d5da774b04f65e0bf` |

For the four root-cause claims, priority was raw event tool calls/results, the locked local `career-emulator==1.0.1` source and response models, current Candidate contracts, then the archived audit report/parser and transcript. The Runner result's reconstructed status is retained as a limitation; it is not treated as a separate session identity.

Contracts reviewed: [AGENT_RUNTIME_CONTRACT](../AGENT_RUNTIME_CONTRACT.md), [runtime manifest](../../../configs/runtime_manifest.json), [structured-state-board](../../../skills/structured-state-board/SKILL.md), [delivery-progress](../../../skills/delivery-progress/SKILL.md), [rolling-planning](../../../skills/rolling-planning/SKILL.md), and [risk-review](../../../skills/risk-review/SKILL.md). The forensic JSON records the hashes of these contract/source files.

## A. Fresh-state semantics

**Classification:** `EXPLICIT_OBSERVE_REQUIRED_AND_MISSING` for all 18 alleged boundaries.<br>
**Counts:** 18 true violations; 0 take-action-result equivalents; 0 partial/unknown.

All 207 successful `take_action` results have exactly `{"success": true, "error": null}`. They contain no updated public state, current event, or legal choices. The locked package source confirms the interface: `TakeActionResponse` contains only `success` and `error` (`career_emulator/server/models.py:174–183`); `ObserveResponse` carries `current_state`, `current_event`, and `choices` (`:142–169`). `GameEngine.take_action` returns `TakeActionResponse(success=True)` after mutation and does not return an observation (`career_emulator/game.py:199–254`). Therefore an action receipt cannot substitute for the next `observe`.

The 18 gaps are two missing boundaries in each of nine three-action Energy windows. Each row lists the preceding observe index and the first later observe, which arrived after the following action(s); action results did not contain state that could be matched to it.

| Month in preceding public state | Missing boundary after action | Next action already submitted | Preceding observe | First later observe |
|---:|---:|---:|---:|---:|
| M15 | 61, 62 | 62(choice 7), 63 | 61 | 62 |
| M18 | 74, 75 | 75(choice 7), 76 | 72 | 73 |
| M21 | 87, 88 | 88(choice 7), 89 | 83 | 84 |
| M24 | 100, 101 | 101(choice 3), 102 | 94 | 95 |
| M27 | 113, 114 | 114(choice 6), 115 | 105 | 106 |
| M30 | 126, 127 | 127(choice 6), 128 | 116 | 117 |
| M33 | 139, 140 | 140(choice 6), 141 | 127 | 128 |
| M36 | 152, 153 | 153(choice 7), 154 | 138 | 139 |
| M39 | 165, 166 | 166(choice 7), 167 | 149 | 150 |

The ungrouped source records, including action choice, preceding public state, tool result keys, next action and the later observe index, are in the [derived JSON](../../../.local/scratch/s08-09/runtime_contract_forensics.json). Decision narration was not retained as state evidence. `transcript.log` narration cannot add fields absent from the actual tool result.

**Root cause:** the action interface is receipt-only, but the persisted execution loop submitted another candidate 18 times without an intervening observe. [AGENT_RUNTIME_CONTRACT](../AGENT_RUNTIME_CONTRACT.md) and the manifest already require an observe after every successful action, so this is an execution/adherence failure, not a missing policy sentence.<br>
**Runtime patch justified:** YES. A future runtime/executor change should refuse a second action until the same-session fresh observe completes. This task did not implement it.

## B. CTRL closure and `X`

The manifest and Risk Skill both say `X=0` blocks submission; the audit parser also rejects `X=0` as incomplete closure. The syntax grammar nevertheless presents a Boolean-like `0|1` plus `-`, while the contracts do not define `-` as the explicit “no reconsideration occurred” state. `X=1` is explicitly “one reconsideration branch completed”; `X=0` is explicitly an unresolved second `RECONSIDER` and forbids `take_action`.

| State | Manifest token | Risk Skill token | Parser meaning | RUN03 |
|---|---|---|---|---|
| No reconsideration | `-` is available; its meaning is not stated (inference: neutral/no branch) | no explicit token definition | syntax accepts `-`; closure allows it when final R is not `RECONSIDER` | never emitted |
| Reconsideration completed | allowed by grammar | `X=1` | closure permits final Risk other than `RECONSIDER` | never emitted |
| Reconsideration unresolved / blocked | `X=0`; prohibit submit | `X=0`; prohibit submit until new public evidence | closure rejects | emitted on all 207 actions |

**Observed distribution:** CTRL syntax parsed on 207/207; `R=PASS` 207/207; `X=0` 207/207; no final-note `X=1` or `X=-`. No reconsideration branch is evidenced by the emitted markers. The transcript does not directly establish the model's internal interpretation, so this does not claim the model consciously read zero as “none.”

**Root cause:** `CONTRACT_ENCODING_AMBIGUITY`. There is no manifest/Risk contradiction about `X=0`; the encoding leaves the neutral state undefined while using a conventional false-like value for a blocked state. The frozen game interface does not validate notes: it truncates notes and accepts a legal choice without a CTRL gate. Thus the prose preflight did not enforce its own stop condition.<br>
**Runtime patch justified:** YES. Minimal future contract: replace `X` with explicit `RB=NONE|DONE|BLOCKED`, define each value, and make preflight reject `BLOCKED` before tool submission.<br>
**Audit patch justified:** NO for CTRL; its closure classification matches the manifest.

## C. Delivery marker coverage

**Root cause:** `MULTIPLE_CAUSES`. The archived audit's `0/207` valid conclusion combines a parser false-negative with real invalid field values; it does not mean Delivery reasoning/lifecycle wholly failed.

The current Delivery Skill requires one ordered marker with mandatory `i`, `n=0–3`, enumerated `focus/evidence`, `checkpoint=0|1|?`, and `recognition=0|1|?`. The manifest repeats the fields but leaves their enum values as `<...>`. RUN03 emitted exactly one marker on each action; all 207 included `i`.

| Classification | Count | Explanation |
|---|---:|---|
| Contract-valid after separator correction | 174 | All fields/relations satisfy the Skill schema |
| `INVALID_CHECKPOINT` | 33 | `checkpoint` was 2 (16), 3 (10), or 4 (7) |
| Missing / duplicate / other invalid field | 0 | No such cases |

Field distributions: `i=NONE 5 / D1 17 / D2 185`; `n=0 5 / 1 202`; `focus=NONE 5 / IN_PROGRESS 17 / COMMITTED 185`; `evidence=NA 5 / UNVERIFIED 202`; `checkpoint=0 5 / 1 169 / 2 16 / 3 10 / 4 7`; `recognition=0 174 / 1 33`. The actual contract-invalid rate is **33/207 (15.94%)**.

The previous parser required exactly one literal space between CTRL and DL (`notes[CTRL.end():DL.start()] == " "`). RUN03's marker order is correct but uses a newline. Replaying that exact condition gives: `VALID=0`, parser-only `ORDERING_ERROR=174`, `MALFORMED_FIELD=33`, `MISSING=0`. The 33 malformed results are correctly rejected because the checkpoint values do not match the enum. The newline is not prohibited by the manifest/Skill contract, which says the markers must appear first and in order.

I applied the narrow audit-only fix in [post_run_audit.py](../../../scripts/post_run_audit.py): it accepts the existing same-line legacy separator and one LF/CRLF separator. Replaying after the fix yields `valid=174`, `malformed_or_duplicate=33`, `missing=0`. The parser still accepts missing `i` for historical legacy compatibility; this permissive superset did not cause RUN03's result because every RUN03 marker contains an ID.

Marker validity does not prove the represented lifecycle state was correct. The markers declare D1 `IN_PROGRESS/UNVERIFIED` and D2 `COMMITTED/UNVERIFIED`; without independent evidence proving item identity, commitment state, verification, and recognition, **`SEMANTIC_DELIVERY_STATUS=INCONCLUSIVE`**. The transcript contains Delivery prose, but prose and a marker are not proof of delivery completion.

**Runtime patch justified:** YES for precise `checkpoint` meaning plus enum enforcement before action.<br>
**Audit patch justified:** YES; implemented and covered by a regression test. No archived file was regenerated or modified.

## D. M42 / L4 triple NO_GAIN

The raw event sequence maps the target to action indices 178–181 at `current_month=42`, Level L4. (The transcript labels the coming quarter as Q15/M43 in prose at one point; the structured event state remains M42 until observe 164, so this reconstruction follows raw events.) Each report-preparation action is followed by its own fresh observe. Therefore the earlier nine-window observe gaps did **not** cause this M42 sequence.

| Action | Choice | Observe before → after | Public Energy | Public Output | Result |
|---:|---|---|---|---|---|
| 178 | Report Preparation | 160 → 161 | 3 → 2 | 26 → 26 | success |
| 179 | Report Preparation | 161 → 162 | 2 → 1 | 26 → 26 | success |
| 180 | Report Preparation | 162 → 163 | 1 → 0 | 26 → 26 | success |
| 181 | Key Project | 163 → 164 | 0 → 0 | 26 → 26; Skill 82 → 83 | success |

The legal choice advertises Output growth, so each of the first three action→observe pairs is cleanly attributable `O=NO_GAIN`. After the first pair, the unchanged Output was already present in the next fresh observation. No explicit `PROGRESSION_RESPONSE: O=NO_GAIN` Board record appears in the Q15 transcript window before the following candidates. The visible Planning record still has `Primary Gap=Output`; choices 179 and 180 repeat the same Output path. The transcript also contains a pre-action three-preparation plan, and the action sequence follows it. These are evidence of intent carry-over, not proof that the model made no internal re-plan. The [Board contract](../../../skills/structured-state-board/SKILL.md) already requires current-Level response tracking, and [Planning](../../../skills/rolling-planning/SKILL.md) already says to devalue NO_GAIN and avoid an immediate repeat when a responsive alternative exists.

**Board updated:** no explicit Board update is observable in the record; an unlogged internal update is UNKNOWN.<br>
**Planning consumed the first NO_GAIN:** no action-level rerouting is observed; action 179 repeats the same path after observe 161.<br>
**Fresh-state effect:** none; fresh observes were present between all four actions.<br>
**Quarter intent:** pre-action three-preparation intent is supported by transcript line markers; all three planned actions were submitted sequentially despite the unchanged Output.<br>
**Audit attribution:** correct; the four actions and three progression pairs are directly recoverable from raw action/observe results.<br>
**Root cause:** `MULTIPLE_CAUSES` — no observable Board propagation of the first NO_GAIN plus an upfront repeated-action plan and no effective per-action marginal reroute.<br>
**NO_GAIN policy patch needed:** NO. The current contract already says NO_GAIN lowers that dimension's marginal value and avoids immediate repetition when responsive alternatives exist. This is an execution/handoff issue; no Candidate patch is authorized here.

## Cross-layer summary

| Issue | Policy semantics | Runtime/model execution | Auditor/parser | Root cause | Runtime patch | Audit patch |
|---|---|---|---|---|---|---|
| Fresh state | Correct: observe after each action | 18 action boundaries omitted; action result has no state | Count-level finding is confirmed by raw sequence/schema | `EXPLICIT_OBSERVE_REQUIRED_AND_MISSING` | YES | NO |
| CTRL `X` | Block rule correct; neutral token undefined | 207 prohibited `X=0` submissions succeeded | Closure rule correct | `CONTRACT_ENCODING_AMBIGUITY` plus no executable preflight gate | YES | NO |
| Delivery DL | Fields mostly align; checkpoint meaning/enum underspecified in manifest | 174 conform; 33 invalid checkpoint enums | Old parser falsely rejects 174 newlines; fixed | `MULTIPLE_CAUSES` | YES | YES, implemented |
| M42 NO_GAIN | Existing no-repeat rule is sufficient | Fresh state arrived; Board record absent; same action repeated | Progression attribution is correct | `MULTIPLE_CAUSES` | YES (execution/handoff) | NO |

## Minimal patch contract for a later Stage task

This task makes recommendations only; Candidate identity remains `candidate-v7t-execution-semantic-repair`.

1. Enforce one successful `take_action` → one same-session fresh `observe` before another action can be submitted. A receipt containing only `success/error` must never advance the planning input.
2. Replace the `X` bit with named branch states (`NONE`, `DONE`, `BLOCKED`) and enforce the blocked state in preflight.
3. Define Delivery `checkpoint` as a bounded enum with explicit semantics (or use named `NEAR`, `NOT_NEAR`, `UNKNOWN`); reject values outside it before submission.
4. After each observed progression action, rebuild Board `PROGRESSION_RESPONSE` and pass it into a new Planning pass before selecting remaining Energy. Keep the existing NO_GAIN policy text.
5. Keep the audit parser's exact supported line separator set and add field-specific rejection reporting for bad enums. The legacy missing-ID parser path should be handled in a separate compatibility decision, not silently treated as current schema.

No runtime recommendation above was implemented in S08-09.

## Integrity and verification

- Forensic script: [s08_09_runtime_contract_forensics.py](../../../scripts/s08_09_runtime_contract_forensics.py); it reads fixed, explicit S08-RUN03 paths, fails closed on session/manifest mismatch, scans only this archive, and writes no transcript narration.
- Derived output: `.local/scratch/s08-09/runtime_contract_forensics.json`; deterministic rerun SHA-256 `1bf64058e56e0b5d3fd735c697d3856aa161588d1474e72fa2e38d8e5cd4efce` on both runs.
- Tests: `28 passed` (`test_s08_09_runtime_contract_forensics.py` plus targeted `test_post_run_audit.py`).
- Secret scan / core session check: PASS using the repository's explicit archive scanners; the derived output was scanned after writing.
- Archived evidence modified: NO; current bytes and SHA-256 match the manifest for every artifact.
- Provider calls / service starts / MCP calls / DB access / Runner plays / games: **0**.
- Runtime Candidate changes: **0**; validation flags unchanged; no post-run artifact overwritten.
- `git diff --check`: PASS.

## Final decision and authorization

`BOTH_RUNTIME_AND_AUDITOR_PATCH_JUSTIFIED`

The audit parser separator fix is implemented. Runtime findings require a separate Stage/Main decision and a bounded future task; this result does not authorize creating v7u, changing the Candidate, or running another game. `FORENSIC_HOLD=ACTIVE`; release remains with Main/Stage after independent review. `NEXT_GAME=NOT_AUTHORIZED`.
