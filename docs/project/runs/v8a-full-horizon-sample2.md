# S09-RUN08｜v8a full-horizon distribution sample #2

- Status: Complete; `VALID_48M_COMPLETION`.
- Decision: `S09_RUN08_V8A_HIGH_VARIANCE_OR_LOWER_TAIL_RETURN_TO_STAGE`.
- Base: `main@a3b6cd57223ba4d79b26b4a77f724f33fa72f275`; Candidate: `candidate-v8a-v7o-donor-core-transplant`; session: `ae83da7c19c64591951cbb9c186e2f52`.
- Frozen behavior identity matches RUN07: Candidate/manifest/four Skills/Runner/dependencies/retry/model-provider configuration unchanged. Existing static/package PASS reused; package `.local/runtime/s09-run06-v8a/submission`, four Skills, retry=2. No strategy/runtime/parser repair.
- One service start, one Runner play, one fresh game, one graceful stop. Readiness PASS in 18.062s within 120s. Runner exit0; stop exit0; manager stopped/PID file absent; all four ports 19092/20000/20001/6173 released. Service-start wrapper exit1 after cleanup; cause UNKNOWN (no UnicodeEncodeError in this run's service log). No restart/resume/replacement.
- Explicit play window: `2026-10-01T13:22:27.041969+00:00`–`2026-10-01T13:54:42.775557+00:00` (UTC; Asia/Shanghai +08:00); wall 1935.734s / 32m16s.

## Outcome and formal Reviews

Final quantitative **59.00**, competition partial **41.30**, survival **48 months**, grade **C**, final Level **L4**; completed=true, natural structured end at M49. Final public H8/D10/W29/S82/N36/O26/E0. Promotions: M12 L1→L2, M18 L2→L3, M36 L3→L4.

The rows below are the first fresh public observation carrying that formal Review, before later Story/Energy/Main choices in the same month. Local receipt's inherited `gate` field denotes only the promotion diagnostic; no checkpoint censor was enabled or performed.

| Review | Grade | Level transition | Promotion | H/D/W/S/N/O |
|---|---|---|---|---|
| M6 | C | L1→L1 | no | 5/10/3/9/3/2 |
| M12 | C | L1→L2 | yes | 8/10/3/9/3/3 |
| M18 | B | L2→L3 | yes | 9/9/5/21/4/6 |
| M24 | B | L3→L3 | no | 9/10/8/41/21/8 |
| M30 | B | L3→L3 | no | 8/10/12/42/21/13 |
| M36 | B | L3→L4 | yes | 7/10/15/42/19/15 |
| M42 | A | L4→L4 | no | 10/10/23/59/33/26 |
| M48 | A | L4→L4 | no | 10/10/27/77/36/26 |

## Compact runtime facts

- Actions successful/failed/unknown = 205/0/0; observes=206; exact event order confirms 205/205 action→fresh-observe pairs. MODE markers A201/S4 (S=1.95%). All eight formal checkpoint reports and session/preflight/terminal reports were emitted from existing logs using an interactive controller; extra reporting queries=0.
- Evidence firewall: numeric HiddenRisk reference PRESENT in one action note (action126/M30); audit transcript text matches=37, which are not 37 independently established uses. The action rationale explicitly names a numeric hidden risk effect, contrary to the manifest firewall. No score-causality claim follows from this count.
- Delivery parser accepted 205/205. All pairs used one space between CTRL and DL, so RUN07's adjacency/separator rejection did not recur. This is observed emitted-format variation under identical frozen bytes, not a parser/Skill patch or proof of Delivery lifecycle semantics.
- Public episodes included recurring HR risk hints, an upgraded warning at M30, M15 Health3 followed by public recovery, and M32–M33 medical follow-up with delegated work. These are trajectory observations; no full semantic or causal audit was performed.
- No gameplay/tool failure or unrecoverable provider/Runner failure observed. Audit limitations: `ctrl_rb_done_branch_use_not_independently_verified`, `llm_log_not_supplied_compression_unknown`. Compression/recovery count, execution boundaries and continuation sends UNKNOWN. No observable compression claim is made.
- Usage: input42,451,202 / output146,541 / total42,597,743; billed cost UNKNOWN.
- Existing Candidate flags remain unchanged: gameplay/provider true for observed sessions; runtime/long-horizon/improvement/stable80+/transfer false; next_game_authorized=false. Numeric firewall use prevents a runtime correctness upgrade.

## Two-sample summary

| Metric | RUN07 sample #1 | RUN08 sample #2 |
|---|---:|---:|
| quantitative | 72.65 | 59.00 |
| partial | 50.86 | 41.30 |
| survival | 48 | 48 |
| grade | A | C |
| final Level | L5 | L4 |
| M6 promotion | yes | no |
| M12 promotion | yes | yes |
| M18 promotion | no | yes |
| promotion months | 6 / 12 / 24 / 42 | 12 / 18 / 36 |

Score range **59.00–72.65**; descriptive mean **65.825**; full 48m survival **2/2**; 70+ **1/2**; natural early terminal **0/2**. Promotion paths differ as shown. `V8A_HIGH_VARIANCE_OR_LOWER_TAIL_OBSERVED`: these two outcomes provide an observed score spread and a lower result, without a probability estimate, stable-performance claim, or Candidate causal attribution. Return to Stage for `V8A_DISTRIBUTION_BASELINE_REVIEW`; further replication or design work requires a separate task/authorization.

## Evidence preservation

Exact raw files remain local and ignored. One `scripts/post_run_audit.py` execution used the explicit receipt paths/window and +08:00 timezone; events/transcript identity PASS, score session MATCH. The Runner result is a live local-controller receipt, not a Runner-generated receipt. Supplemental `.local/runtime/s09-run08-v8a/runtime-facts.json` contains only deterministic event-order/marker counts. No raw archive or shared DB/provider/service query was used for the offline audit.

| Exact artifact | Bytes | SHA-256 |
|---|---:|---|
| `D:\CS\CareerSim\.career_sim_runner\career_emu\outputs\local-s06-adaptive-controller\20261001T132230Z\events-20261001T132230Z.jsonl` | 2,078,416 | `32cab0dbf9a5f10741ebff29db0fba5aa743e177b6211319d024fb05368229d0` |
| `D:\CS\CareerSim\.career_sim_runner\career_emu\outputs\local-s06-adaptive-controller\20261001T132230Z\transcript-20261001T132230Z.log` | 369,297 | `3d68eb16dc985b2a47b9849a9ce4455b83e8eeecda1126670cbe2911d0488a4b` |
| `D:\CS\CareerSim\.career_sim_runner\career_emu\outputs\local-s06-adaptive-controller\20261001T132230Z\score_report.json` | 2,752 | `22f534f0709a9582456cc5f9af342237f390b97565f1049369254d3401b94592` |
| `D:\CS\CareerSim\.local\runtime\s09-run08-v8a\runner-result.json` | 5,480 | `5af808aa277d40e25e9a8442f2c9ab7a92cc0b8bed75417027baade616fcd331` |
| `D:\CS\CareerSim\.local\runtime\s09-run08-v8a\post_run_summary.json` | 265,533 | `4599f9893cffbfc00274895b5db8dc07732c5d7b4a249464487f4f7afcdd4e64` |

`FORENSIC_HOLD=ACTIVE`: retain the listed RUN08 artifacts and local stdout/cleanup receipt for two-sample review and the separate evidence-firewall/Delivery correctness review. Window and exact paths/hashes are above; responsible reviewer/release authority=S09 Stage/Main. Release after independent acceptance and confirmation no follow-up relies on raw, then only by explicit cleanup authorization. RUN07 and earlier holds remain intact.

`S09_RUN08_GAME_AUTHORIZATION=CONSUMED` · `NEXT_GAME=NOT_AUTHORIZED` · `NO_REPLACEMENT_RUN_AUTHORIZED`.
