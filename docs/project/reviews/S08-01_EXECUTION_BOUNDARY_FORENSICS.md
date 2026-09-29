# S08-01 — Execution Boundary Forensics

## Result

- Task: `S08-01`, offline forensic only; no Candidate, Skill, Runner, runtime, or gameplay change.
- Root-cause classification: `INSUFFICIENT_EVIDENCE` (`MEDIUM` confidence).
- `H_EXECUTION_BOUNDARY_CONFLATION`: `WEAKENED` as a cause; the run proves frequent execution completions, not that the model confused decision closure with game completion.
- Next decision: `INSUFFICIENT_EVIDENCE_RETURN_TO_STAGE`.
- `NEXT_GAME` remains `NOT_AUTHORIZED`.

## 1. Identity and evidence

At execution, `main` was clean at `f0459e8db2b31a0bed111eb0056a94b588935377`, equal to refreshed `origin/main`. The repository records `S08=ACTIVE`, `S07=COMPLETE`, and current Candidate `candidate-v7n-public-state-delivery-constraint-hardening`; `configs/current_candidate.json` also says `next_game_authorized=false`. The current Candidate and authorization did not drift from the Plan.

Tracked `career_sim_runner/` has the same tree `a2245c49d0b102b80b9891b6d750c671b3c3710f` at the v7g, v7m, v7n launch commits and current `main`. The cross-run comparison therefore uses the same tracked Runner tree. No shared DB was opened or accessed.

| Evidence | Identity / size | Use |
|---|---|---|
| v7n events | `D:\CS\CareerSim\.career_sim_runner\career_emu\outputs\local-s06-adaptive-controller\20260929T080910Z\events-20260929T080910Z.jsonl`; 313,536 B; SHA-256 `1091b11024eee376d2d0f8dfbc2532fcf66b13dcf9999c6aeb3e7cacc910b8cc` | Ordered collector event records and final-frame markers |
| v7n transcript | same output directory, `transcript-20260929T080910Z.log`; 82,836 B; SHA-256 `d334751c957c7317595c7863f9218f97d1224132fbeaac913647dd9ff98db6ba` | Transcript collector behavior and size only; no private reasoning reproduced |
| v7n score report | same output directory, `score_report.json`; 1,220 B; SHA-256 `5309c4840532c2ea41baa1f0743f6cd8512c299415eb339e2157a8ed2f983bbe` | Session binding and `max_continuations` termination |
| v7n offline audit summary | `D:\CS\CareerSim\.local\runtime\s07-51r\post_run_summary.json`; 44,888 B; SHA-256 `d1d08741fed0f6a8b02bab3ed8d31d70a6763c6af466a8c94497c0dedf700c36` | Action, observation, and token totals |
| v7n process capture | `D:\CS\CareerSim\.local\runtime\s07-51r\execution-summary.json`; 1,037 B; SHA-256 `602341cdb51ace603fb226ef7fc753bdf72191bb32ff7dc00d0f187ab1119a38` | Runner exit and lifecycle accounting |
| v7n Runner stdout / service stderr | `.local\runtime\s07-51r\runner.stdout.log` 44,395 B, SHA-256 `75050240b6dae841d59cfdaff98f6c534317ffc5377406f4c885b28e99b5968ec7`; `service-start.stderr.txt` 6,172,677 B, SHA-256 `6d1c097bcf946b9ce4ae6011cbcfb94404a78e28eaf2c50f1b907e34834cbeb7` | Bounded marker-presence check for additional frame evidence |
| v7n run report | [v7n S07-51R report](../runs/v7n-run1-replacement-validation.md) | Confirms fresh session, M6 outcome, max-continuation termination, and audit totals |
| v7m report and archive | [v7m report](../runs/v7m-run1-validation.md); archived `artifacts/dev-runs/S07-46-v7m-run1/events.jsonl` 890,180 B, SHA-256 `4b5f2c2057212e44310397f449ff6f41fe270b1b8c11945ea5a18b57ceb7af8b` | Closest Candidate/control-contract comparison; archived event slice has no final-frame records |
| v7g report and events | [v7g report](../runs/v7g-run1-validation-r2.md); raw events `D:\CS\CareerSim\.career_sim_runner\career_emu\outputs\local-s06-adaptive-controller\20260928T055416Z\events-20260928T055416Z.jsonl`; 1,903,318 B; SHA-256 `73cb4de9f2568e343be252630a64dbef289e92aec121bae07ef8fbd3a6cff3c4` | Valid 48-month reference and collector final-frame comparison |

The v7n local evidence was read-only. No held evidence was deleted, overwritten, or released.

## 2. Frozen Runner state machine

Source: `career_sim_runner/ws_client.py` (`MAX_CONTINUATIONS = 20`, `drive`, `_has_ended`) and `career_sim_runner/transcript.py` (`feed_frame`, `_append_event`, `_flush_text`). The initial prompt asks for `observe → decision → take_action` until game end; the continuation prompt asks to observe the existing session and continue until game end.

1. `drive` sends the initial play prompt with `continuations=0` and `skip_next_e2a_complete=false`.
2. Every received frame is first passed to the collector and game-signal extractor. `e2a.error` or failed status exits with an error.
3. On final `e2a.complete`, a true skip flag is cleared and that completion is ignored for the continuation counter. Otherwise, an ended game exits; if the counter is already 20, Runner sets `termination_reason=max_continuations` and breaks; if not, it increments the counter, sends a continuation prompt, and sets the skip flag. `e2a.error` or failed status exits before this branch.
4. Any other frame clears the skip flag. The reset applies to any ordinary frame, not only a terminal/error frame.
5. `_has_ended` uses structured game signals (`game.ended`), not transcript text. If the stream exits without an ended game, exit status is nonzero.

Thus a `max_continuations` termination means 20 continuation sends occurred and the next counted non-terminal completion hit the cap: 21 counted boundaries in total. Each send can suppress at most one later completion.

## 3. Preliminary replay correction

The v7n events file has 277 records: 104 `tool_call`, 104 `tool_result`, 28 `usage`, and 41 `frame_final`. All 41 final markers report `response_kind=e2a.complete`, `status=succeeded`, and `is_final=true`. The audit summary independently reports 23 unique successful actions, 23 unique observes, and usage of 3,272,736 input / 28,462 output / 3,301,198 total tokens; these usage totals match the score report.

The initial replay reached 21 counted boundaries / 20 ignored finals by assuming the skip flag survived any intervening frame. That assumption is not valid in general. For this run, however, the aggregate is independently recoverable from the exhaustive ordered final markers and `max_continuations`: the cap requires 21 counted completions; 41 final completions were consumed; therefore 20 were skipped. Since there were exactly 20 sends and each can skip only once, each send's skip was consumed by one following final. This derives the aggregate from Runner semantics and observed terminal state; it does not reuse the preliminary replay's assumption.

Small checkable event slice:

- `seq=31`: counted `e2a.complete`; continuation send 1.
- `seq=32`: next `e2a.complete`; consumes the skip.
- `seq=33–70`: the boundary interval contains 5 unique `take_action` calls, 4 unique `observe` calls, and 2 usage records (462,439 input / 3,391 output tokens).
- `seq=71`: next counted `e2a.complete`; continuation send 2.

Applying those derived boundaries and deduplicating tool calls by `tool_call_id` reproduces 21 event intervals, 23 actions, 23 observes, and the audited token totals. Seven intervals (1-based: 6, 8, 11, 12, 14, 16, 19) contain no recorded tool calls and no usage record. They are **not proven empty assistant executions or zero-token model turns**: the event file has no request IDs, and transcript text is not correlated to event sequence numbers.

## 4. Evidence observability

**Overall: `PARTIALLY_RECONSTRUCTABLE`.**

- **Exactly reconstructable for v7n:** the 41 ordered final markers; 20 continuation sends; 21 counted completions; 20 suppressed completions; and event intervals aligned to those counted boundaries.
- **Partial:** exact action/observe/usage counts within collector-event intervals are reproducible, but the source artifacts do not bind each tool event to a WebSocket request ID or a full raw-frame sequence. Treat these as boundary intervals, not definitive model-request attribution.
- **Not recorded in collector events:** ordinary non-final WebSocket frames, their order, frame-to-request IDs, and a transcript chunk-to-frame map. The collector logs tool calls/results, usage summaries, and final-frame metadata only. Transcript text is buffered/flushed at tool/final events or newlines without the event sequence ID.
- **Runner stdout/stderr:** no raw `e2a.complete`, `is_final`, or `frame_final` sequence was found; stdout reports the terminal reason. The service stderr contains 6 textual `e2a.complete` and 481 `is_final` occurrences, but these do not reconcile to the 41 Runner collector finals or establish a complete one-to-one Runner receive-frame trace. They cannot replace the collector evidence.
- **v7m:** the committed archive contains 700 call/result records and no `frame_final` records; the report notes the archive slicing limitation. Continuation counts are unknown.
- **v7g:** raw events contain one final `e2a.complete` marker alongside 195 successful actions. This confirms a full-run reference with a single logged final boundary; it is descriptive, not a controlled comparison.

## 5. v7n vs v7m vs v7g

| Run | Candidate / outcome | Actions / observes | Actions per reached month | Boundary evidence | Limit |
|---|---|---:|---:|---|---|
| v7n S07-51R | v7n; alive at M6; Runner exit 1, `max_continuations`; no natural terminal or score | 23 / 23 | 3.83 | 41 final markers; derived 20 sends / 21 counted completions | Tool calls lack request IDs; no raw ordinary-frame sequence |
| v7m S07-46 | nearest parent v7m; reached M20 with 84 successful actions, then socket/model-stream technical failure, not `max_continuations` | 84 / 85 | 4.20 | Archived event slice omits all final-frame markers | Same closure contract and Runner tree, but terminal type differs and boundary count is unavailable |
| v7g S07-33R | v7g; `VALID_48M_COMPLETION`, 54.52 quantitative / 38.17 competition partial / grade C | 195 / 196 | 4.06 | One final marker in available raw events | Different Candidate and unseeded run; reference only |

The action-per-month rates are close and descriptive; they do not measure execution persistence. The direct observed distinction is completion-boundary frequency, not gameplay actions per reached month. v7m is the most causally informative comparison because it is v7n's nearest parent, uses the identical tracked Runner tree, and had the same decision-closure contract; its 84 actions to M20 materially weaken closure wording as a sufficient cause. v7g establishes that the same Runner tree can support 48 months under another Candidate, but does not isolate why v7n emitted many more final markers. v6 is not added because these references answer the bounded comparison questions.

## 6. v7m → v7n authoring delta

Static comparison uses commit `6338bce24a022aacd67843f265108e2145a0bc2b` and its actual parent `fee5b1de5052a0285d934e77d2073abb6cffc654`.

- Runtime-manifest instruction length increased from 6,480 to 8,372 characters (+1,892).
- The four Skill files increased by 5,498 bytes total: Board +1,284; Planning +1,075; Delivery +2,429; Risk +710.
- Added contract surface: verbatim public-state copying and attribution limits; current-session Delivery item IDs/proof and retirement; explicit binding-constraint `MODE` semantics; expanded Full Risk routing and labels.
- The closure clauses are preserved: `ONE OBSERVE = ONE PLANNING PASS`, Planning closes after one final candidate, only bounded Risk reconsideration may reopen, and unchanged evidence does not reopen Planning. No new instruction equates decision closure with game or assistant-execution completion.

Suspect assessment:

| Suspect | Status | Evidence |
|---|---|---|
| Decision-closure wording alone caused v7n's failure | `COUNTEREVIDENCE` | Wording is unchanged from v7m; v7m reached M20 / 84 actions before a different technical failure. |
| Added public-state, Delivery, binding-constraint, and Risk obligations increased execution-completion propensity | `PLAUSIBLE` | The instruction and Skill burden grew; one uncontrolled v7n run cannot establish the behavioral effect. |
| Skip-flag reset on ordinary frames caused this v7n budget burn | `WEAKENED` | v7n's exact final counts imply all 20 sends consumed one skip before the next counted completion; no reset consumed budget in this run. The reset branch remains real source behavior. |
| Framework/model stochastic or mixed behavior explains v7n's completion frequency | `UNKNOWN` | No request-level frame trace or same-Candidate controlled run distinguishes it from authoring effects. |

## 7. FACT / INFERENCE / HYPOTHESIS / UNKNOWN

- **FACT:** S08 is active; v7n is current; next game is unauthorized. v7n stopped alive at M6 after 20 continuation sends and the 21st counted completion, with 23 successful actions, 23 observes, and no natural terminal. v7m and v7g used the same tracked Runner tree.
- **FACT:** The v7m→v7n closure contract did not materially change; several adjacent evidence/Delivery/Risk contracts did.
- **INFERENCE:** Continuation-budget exhaustion is the proximate termination mechanism. At least for this run, the failure is associated with many counted completion boundaries relative to its action count, while action throughput per reached month is close to the two references.
- **HYPOTHESIS:** Additional semantic bookkeeping may have increased model completion frequency or response overhead. The available evidence does not isolate that effect.
- **UNKNOWN:** Exact raw non-final frame order; request-to-tool-call association; whether the seven tool/usage-silent intervals contained assistant text or unlogged usage; causal contribution of the v7n wording versus model/framework variability.

## 8. Root-cause classification

**Primary classification: `INSUFFICIENT_EVIDENCE` — confidence `MEDIUM`.** The direct stop reason and Runner counter behavior are established. The upstream reason that v7n accumulated 21 counted boundaries by M6 is not. Candidate authorship remains plausible; no specific authoring clause is causally linked. The Runner cap is the proximate mechanism, but the evidence does not show a Runner defect or a differentiating framework failure.

## 9. `H_EXECUTION_BOUNDARY_CONFLATION` disposition

**`WEAKENED`.** v7n clearly had frequent E2A completion boundaries, but there is no observed statement or event proving that the agent treated a closed decision as a completed game/execution. Both the initial and continuation prompts explicitly say to continue until game end. The v7m near-neighbor used the same decision closure contract and progressed to M20. The hypothesis remains possible as a response-level behavior, but it is not a supported root cause.

## 10. Next decision and residual limitations

**Selected: `INSUFFICIENT_EVIDENCE_RETURN_TO_STAGE`.** Do not patch the Candidate or frozen Runner from this evidence. Return the causal distinction to Stage/Main review. This result does not authorize a game or any live runtime action.

Material residual limits: no request-ID-bound Runner frame trace; v7m's archived slice has no final-frame markers; the runs are unseeded and use different Candidates; no controlled authoring comparison establishes why v7n's completion frequency differed.

## Delivery boundary

Only this forensic review and one concise `CURRENT_STATE.md` line are changed. Candidate JSON, runtime manifest, four formal Skills, Runner source, runtime configuration, and run artifacts remain unchanged. No provider request, MCP live call, service lifecycle, install/reload, Runner play, game session, or DB access occurred.
