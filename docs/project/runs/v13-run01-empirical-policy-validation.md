# TASK_RESULT — S10-06｜v13 empirical promotion-first Run #1

## Result and identity

- Task status: **Complete**; branch-only `IN_FLIGHT_EVIDENCE`, returned for Main/Stage review. S10 remains ACTIVE.
- Validation classification: **NEGATIVE_POLICY_SIGNAL**. One fresh game naturally ended at M36 by public trust-crisis elimination, with specific R5/R6/R7/R8/R9 execution failures. This classification uses those failures together with early termination; low score alone is insufficient.
- Branch: `codex/s10-06-v13-run01`; accepted parent/execution HEAD: `eed75f580fef865f28a566a15113d8eab8a8e1d8` (`codex/s10-05-empirical-promotion-policy`). Frozen main/fallback: `8267d420da29888d0a05403991f8980e251aaa0c`, candidate v8a.
- Candidate: `candidate-v13-empirical-promotion-playbook`. Exact accepted package bytes were installed. All Candidate validation flags remain frozen false; session evidence is reported here rather than rewriting metadata.
- Result commit: the commit introducing this report and its [compact evidence](v13-run01-empirical-policy-evidence.json); its Git identity and verified remote/clean state are returned in the task message. No merge into main.

| Package file | SHA-256 of actual installed source bytes |
|---|---|
| manifest.json | `7378e943988bc7d28e0fd595e4baccb1d698a4b93c2784c73d39aae6e84178e1` |
| rolling-planning | `cd7e7434baf04ff38dbbfcf2a15727fc3c5d535dc22e9de29dc0ac23e5703a38` |
| structured-state-board | `da76071dd035fcbb9073d69173db9a629f2404189709d39ea950dfd78bcd1cae` |
| delivery-progress | `200b6c83aaca43f6dccfe58a30e23e79463e930512ef89cf5b19070a9d5d7528` |
| risk-review | `6da910fa60b07dfdccfc78a840ebc4777fc39e3188358e69ee483c89606874fd` |

Protected Candidate, manifest, Skill, pyproject and uv.lock byte hashes match preflight after the run. Frozen Runner SHA: `f61c738c72e51b77298cc1c14c7c6ebf4b6c527d`. Established local `max_retries=2` was retained. No strategy, dependency, Runner or retry-config intervention occurred.

## Live budget and execution

| Operation | Actual |
|---|---:|
| Candidate install | 1 |
| service lifecycle | 1 |
| Runner play | 1 |
| fresh new_game | 1 |
| replacement / manual choice / strategy intervention | 0 / 0 / 0 |
| provider completion probes / extra reporting queries | 0 / 0 |

The one established non-generative balance check showed available CNY 9.34; the availability gate passed, while full-run funding and actual billed cost remain UNKNOWN. No new balance query followed the run.

P1 reused the accepted 17-test/static package PASS. The process-local PATH included the root .venv Scripts directory in the caller itself; the single actual bare `jiuwenswarm-start --list` invocation exited 0. An earlier local config-template assertion failed before any CLI child/live side effect, then was corrected using the established environment/template resolution. This is a recorded tooling error, not a consumed install/play or replacement.

The exclusive window had no competing Python/Jiuwen process or known-port listener. Installation exited 0, service readiness passed, and the primary Runner then ran without submission/reinstall or continuation arguments. Observational progress reads used already-written artifacts only. The launcher awaited the primary process independently of all progress parsing; null `current_event` was handled. No monitor error stopped or cleaned up gameplay.

- Play: `2026-10-03T18:04:35.219112Z` → `2026-10-03T18:21:40.516466Z` (2026-10-04 02:04–02:21, Asia/Shanghai).
- Primary Runner exit: **0**; natural terminal preceded exit.
- Only after primary exit: one graceful stop, exit 0; known ports empty and manager PID file absent. The service wrapper exited 1 after graceful stop, with no primary runtime failure; its status is preserved rather than relabeled as gameplay failure.

## Outcome and exact Review frontiers

Session: `97990a12bbd94419abdbf2011e2db159`.

**34.01 quantitative / 23.81 competition partial / 36 months / D / L4**. Public terminal: “信任危机end —— 第二次爆雷！组织表示「信任额度已用尽」”. Final public H/D/S/N/O/W/E: **7/7/43/20/16/11/1**, L4 tenure 1. This is an uncensored natural elimination, not a technical stop or a 48-month completion.

Each Review below uses the action's preceding fresh observation and the first post-action observation containing that Review. E=0 at both sides of all six Review boundaries. Same-month later Energy/Main gains are excluded. Numeric deltas across these boundaries are MIXED Story/Review/payroll/promotion effects.

| Review | Grade | Level | pre H/D/S/N/O/W; tenure | first post H/D/S/N/O/W; tenure | events pre → action → post lines |
|---|---|---|---|---|---|
| M6 | C | L1→L2 | 3/10/9/2/3/2; 5 | 3/10/9/3/3/2; 1 | 171→173→179 |
| M12 | C | L2→L2 | 8/10/21/6/5/4; 6 | 7/10/21/7/4/4; 7 | 371→373→379 |
| M18 | C | L2→L2 | 9/10/21/7/4/4; 12 | 10/10/21/7/4/4; 13 | 563→565→571 |
| M24 | B | L2→L3 | 7/10/21/6/6/6; 18 | 7/10/21/7/6/6; 1 | 755→757→763 |
| M30 | B | L3→L3 | 9/10/36/16/10/9; 6 | 10/10/36/16/9/10; 7 | 955→957→963 |
| M36 | B | L3→L4 | 9/10/42/20/16/12; 12 | 9/10/42/16/16/13; 1 | 1147→1149→1155 |

Promotions: **M6, M24, M36**. First-promotion delay from L2 to L3 is 18 months. M36 promotion does not erase the subsequent same-month natural terminal at events line 1187.

## Empirical policy audit

`events` locators refer to the exact held JSONL below; `transcript` locators refer to its companion log. Automatic lexical result labels and markers are inputs, not semantic verdicts. The compact JSON records all 11 Main choices and all five clean local Energy NO_GAIN cases, including the next same-family choice and its justification.

| Mechanism | Status | Concrete evidence and limit |
|---|---|---|
| R2/R3 Review-window deliverability | PASS_WITH_LIMITATIONS | M11 action373 chooses a two-day architecture course over accelerating a tool from Tuesday to Monday. Public normal delivery is already timely; this is a qualified exception, not automatic window neglect. M12 action381 seeks to implement the temperature solution. Later ranking predominantly pursues numeric Output; window-result realization is not proven. |
| R4 result ladder | PASS_WITH_LIMITATIONS | Notes keep evidence=UNVERIFIED instead of upgrading tool success into verified deliverables. D5/IN_PROGRESS/UNVERIFIED/NEAR persists for 105 action markers, so complete lifecycle/recognition maintenance cannot be credited. |
| R5 local response discount | **FAIL** | M6 report205 gives clean O6→6, then report213 immediately repeats at the same Level/state with no independent gain justification. Positive switches occur at M9 and M33. M33 action1101 nevertheless converts two flat observations into the explicit forbidden cap claim “Output已触顶(16)” (transcript4320–4324). No hidden cap is adopted as an audit fact. |
| R6 Energy one-step | **FAIL** | Fresh observe exists after all 24 successful Energy actions, but M18 notes597 preassigns remaining Health recovery; M24 notes789 and M33 notes1085 preassign later report actions. Transcript1227 also proposes a whole-quarter recipe. One tool call at a time does not establish genuine replanning. |
| R7 conditional Main | **FAIL** | 9/11 Main choices are key-project applications; M12/M33 report to Leader. M18 deliberation repeatedly reopens alternatives before maximizing advertised Output despite known lack of realized Output. M27 action909 resumes that prior after an explosion and failed cleanup, without public danger-clearance evidence. Cross-month Main returns remain MIXED. |
| R9 no-advance reroute | **FAIL** | M12 explicitly rebuilds objective/checkpoint to M18 and later changes Main family (381/421; transcript2617/2629). M18 acknowledges C/no advance but repeats intensive-work→Health plus project Main (573/597/613). M30 acknowledges B/no advance but repeats intensive-work→report plus project Main (965/989/1005). Goal restatement is not tested-path rerouting. |
| R8 material danger | **FAIL** | Transcript3520 expressly excludes the public HR accumulated-risk warning because the concept maps to HiddenRisk. M27 explosion O15→6 triggers a cleanup attempt893, but it costs2 at E1 and is rejected; subsequent fresh observe/report901/project909 have no public clearance. No successful legacy-risk cleanup occurs. M36 intensive work1181 follows renewed HR warning and a mentor incident, then natural trust-crisis terminal1187. |
| Ordinary-cost behavior / false conservative routing | PASS_WITH_LIMITATIONS | MODE=A accepts real H/D costs; M12 compliant client dinner397 accepts ordinary time investment. Only two S markers occur, an acute-health case and the rejected M27 cleanup. Health-buffer choices under A still consume Energy; their opportunity cost is not established. |

The five clean Energy NO_GAIN cases are M6 report205, M6 report213, M9 networking317, M33 intensive-work1085, and M33 report1093. M21 report701 later gains O5→6 in a changed context; that observation does not retroactively justify M6 immediate repetition or validate the model's hidden-cap explanation. The next intensive-work choice after M33 is M36 at a new Level, so it is not classified as an unchanged-Level repeat solely from the earlier flat response. Cleanup's flat visible capital would not establish absence of hidden benefit or warning clearance; no successful cleanup occurred here.

**FACT:** public escalation, unaffordable protective action, retained recipes and no-advance path repetition are observed. **INFERENCE:** this run supplies a negative execution signal for the empirical policy. **UNKNOWN:** which single decision caused the trust-crisis terminal, the unseen failure mechanism, and whether a different policy would have avoided it. Do not replace public evidence with the terminal model's retrospective hidden-mechanism explanation.

## Runtime correctness, separated from strategy

| Check | Verdict |
|---|---|
| Fresh session / scores | PASS: one fresh new_game; observations, terminal and score report bind to the same session. |
| Action→fresh observe | PASS: 144/144 successful actions have the first following fresh observe before the next action; 146 observes include startup and one rejected-action recovery. |
| Choice representation | PASS: 145/145 one current-menu integer; **resource feasibility FAIL** on the cost2/E1 cleanup. Current-menu legality does not mean affordability. |
| Startup four Skills | PASS_WITH_LIMITATIONS: request order Board1→Delivery3→Planning5→Risk7; parallel successful native returns Planning13→Risk15→Delivery17→Board19, all before new_game. Sequential completion ordering is not proven. All four returned Skill content. |
| CTRL / closure | Syntax PASS 145/145; marker-consistency closure PASS. Semantic preflight fails on the unaffordable action; repeated “final” reversals in M18 transcript show that concise one-pass decision closure is not proven by markers. |
| DL | Syntax/identity PASS 145/145; lifecycle PASS_WITH_LIMITATIONS. The persistent D5 with no public verification/recognition is not whole-game semantic adherence. |
| Final Risk | Marker coverage exists: PASS141/ALLOW4, RB=NONE145. Semantic **FAIL**: public-warning exclusion and progression resumption without danger clearance; marker presence is not a safe-gate proof. |
| Failed action recovery | PASS_WITH_LIMITATIONS: one known rejected action, then fresh same-session observe and legal replanning. No unknown action outcome or blind retry; no replacement or harness retry. Initial resource preflight remains a real failure. |
| Compression / recovery | Run-window compressor count **0**; compression recovery **NOT_EXERCISED**, not validated. |
| Whole-game persistence | PASS_WITH_LIMITATIONS: primary drive reached natural M36 terminal with one succeeded final frame. M37–M48 behavior is NOT_EXERCISED. Continuation telemetry UNKNOWN. |
| Evidence firewall | **FAIL in model decisions:** excluded advertised hidden-risk reasoning and pre-action hidden-cap inference occur. The audit includes category/public-text evidence only, no hidden stock or Test facts. No hidden/private source or historical corpus was supplied to gameplay. |

Wire call/result records are duplicated; 297 call duplicates and 297 result duplicates are deduplicated by tool_call_id. The 145 attempts comprise 144 successes and one known rejection, with zero unknown receipts and no noncanonical route. Successful phases: Handbook1, Story108, Energy24, Main11.

The existing offline JSON helper misses native Skill results stored as strings. One scoped native-result read confirms success=True and Skill content for all four. Manual extraction resolves the acceptance question; no Candidate/Runner or durable audit adapter was changed. Canonical post-run extraction ran once; subsequent raw reads answered only identified policy/runtime gaps.

## Usage and descriptive comparison

- Runner-reported input **27,687,531**, output **135,762**, total **27,823,293** tokens; binding SESSION_MATCH. Reported cache tokens 27,363,968 / cache-hit rate 98.8%.
- Play wall time **1,025.297354 seconds** (~17m05s); output ~943 tokens per successful action, descriptive only.
- Compression 0 in the explicit run-window log slice; continuation count **UNKNOWN**, observed final completion frames 1.
- Actual billed cost **UNKNOWN**. Reported cost 0.0 does not establish free usage. No tariff multiplication or post-run provider probe was used.

| Reference | quantitative | months | final Level |
|---|---:|---:|---|
| v6 | 75.29 | 48 | L6 |
| v7o | 71.83 | 48 | L5 |
| v8a RUN07 | 72.65 | 48 | L5 |
| v8a RUN08 | 59.00 | 48 | L4 |
| RUN10 | 68.40 | 48 | L5 |
| v12 RUN01 | 23.48 | 24 | L1 |
| v13 RUN01 | 34.01 | 36 | L4 |

Historical values are from the accepted [frontier report](../research/S10_PROMOTION_FRONTIER_REPORT.md), lines19–28. v13 reaches further than v12 and promotes earlier, but trails all listed 48-month references; these are uncontrolled descriptive comparisons, not causal superiority or architecture attribution. No additional historical raw corpus was opened for this comparison.

## Evidence hold, verification and return

**FORENSIC_HOLD=ACTIVE**, owner S10-06/Main. Minimum source evidence:

- `D:/CS/CareerSim/.career_sim_runner/career_emu/outputs/local-s06-adaptive-controller/20261003T180440Z/`: exact events, transcript and score_report.
- `D:/CS/CareerSim/.local/runtime/s10-06-v13-run01/`: run-result/preflight, launcher/observer, scoped LLM log, lifecycle stdout, canonical summary and public-only derived transitions/Review boundaries.

Paths, bytes and SHA-256 of the selected held files are in compact JSON. Events: 1,457,178 bytes, SHA-256 `e10402d3217aae471485176f941e589f856a138e8746afb4df7d02d0fe0283be`. The original sources remain local; no raw archive, source deletion, DB/config dump or hold release occurred. Hashes do not replace source recoverability. Main/Stage must accept independent compact review, confirm recoverability and release child/reanalysis dependencies, then explicitly release the hold; subsequent cleanup requires its own authorization.

Verification: unchanged protected/package hashes; exact fresh-pair extractor and six Review boundaries; compact JSON parse/count/identity assertions; bounded secret scan of the three selected delivery files; `git diff --check`. No new broad regression, provider call, game or runtime repair. Prior static checks apply only to byte-identical frozen inputs.

Plan deviations / actual limitations: harmless preflight-template tooling correction; resource preflight and several Candidate semantic contracts fail; native Skill-result shape required a scoped manual offline extraction. These are reported outcomes, not reasons to rerun or rescue the trajectory. No extra intervention or retry budget was used.

Material state change: branch-local CURRENT_STATE records this single session, its negative signal and active hold. PROJECT_BRIEF / architecture decisions / official fallback / validation metadata are unchanged.

Stable75+, stable80+, superiority, causal optimality and hidden-test transfer are **NOT_PROVEN**. No Stage completion or strategy patch is declared.

**RETURN_FOR_V13_GAME_GATE**

**NEXT_GAME=NOT_AUTHORIZED**
