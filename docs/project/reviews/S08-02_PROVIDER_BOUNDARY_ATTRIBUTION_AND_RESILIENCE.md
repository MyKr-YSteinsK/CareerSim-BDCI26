# S08-02 — Provider Boundary Attribution and Runtime Resilience

## 1. Result

- Status: COMPLETE; offline forensic review only.
- Root-cause classification: MIXED_PROVIDER_AND_EXECUTION_PERSISTENCE, MEDIUM confidence.
- Of 21 counted execution boundaries, 7 ended with a provider error and no game work; 14 completed productively after a recoverable connection error.
- Provider-error contribution: 7/21 counted boundaries (33.3%); 7/20 continuation sends (35%) were zero-work provider terminations.
- H_EXECUTION_BOUNDARY_CONFLATION: LOW_PRIORITY / NOT_CURRENTLY_SUPPORTED.
- Next recommendation: S08_RUNTIME_RESILIENCE_IMPLEMENTATION_JUSTIFIED, limited to a separate local-runtime task. This does not authorize a game, provider request, service lifecycle, or cloud-portability claim.

## 2. Identity and Scope

- Repository: MyKr-YSteinsK/CareerSim-BDCI26; branch main.
- Base: 928fe102ad0e832502236b2b51d5a714f9f61222, matching refreshed origin/main at task start; the working tree was clean.
- Stage: S08 ACTIVE; S07 COMPLETE.
- Candidate: candidate-v7n-public-state-delivery-constraint-hardening.
- Frozen Runner SHA: f61c738c72e51b77298cc1c14c7c6ebf4b6c527d.
- Installed package identities read from the existing environment: jiuwenswarm 0.2.4b3, openjiuwen 0.1.16.post2, openai 2.41.0, httpx 0.28.1.
- NEXT_GAME remains NOT_AUTHORIZED.

The task was restricted to previously captured v7n logs, committed historical reports, frozen source/config surfaces, and this review plus the CURRENT_STATE index. No provider request, network probe, service lifecycle, MCP call, game action, database access, install, dependency update, or secret inspection occurred. Effective local runtime overrides were not read.

## 3. New Evidence Since S08-01

S08-01 could derive the 21 counted boundaries but could not bind event intervals to request IDs. The captured service log supplies 21 foreground request IDs, lifecycle start/finish records, and terminal timestamps. All foreground lifecycles belong to Runner session career-sim-runner-7ec155cca21a. Ordered correlation by Runner session, request lifecycle, and final-frame time maps them to the 21 counted boundaries. The five agent-prewarm-sync requests are distinct background activity and are excluded.

The collector contains 41 final markers, all e2a.complete with status=succeeded and is_final=true. The frozen Runner's 20-continuation cap, 20 sends, and terminal max_continuations state imply 21 counted completions and 20 skipped duplicate completions; request windows and final timestamps map each foreground request to one counted final. Collector tool/usage events lack request IDs, so their attribution uses the nonoverlapping serialized request windows. This updates S08-01's boundary attribution with later service-log evidence without rewriting its historical conclusion.

| Evidence | Size and SHA-256 | Use |
|---|---:|---|
| v7n collector events: D:\CS\CareerSim\.career_sim_runner\career_emu\outputs\local-s06-adaptive-controller\20260929T080910Z\events-20260929T080910Z.jsonl | 313,536 B; 1091b11024eee376d2d0f8dfbc2532fcf66b13dcf9999c6aeb3e7cacc910b8cc | Ordered tool/usage events and 41 final-frame markers |
| v7n service stderr: D:\CS\CareerSim\.local\runtime\s07-51r\service-start.stderr.txt | 6,172,677 B; 6d1c097bcf946b9ce4ae6011cbcfb94404a78e28eaf2c50f1b907e34834cbeb7 | Foreground request lifecycle IDs, provider error markers, repair markers, and request finalization |
| v7n post-run summary: D:\CS\CareerSim\.local\runtime\s07-51r\post_run_summary.json | 44,888 B; d1d08741fed0f6a8b02bab3ed8d31d70a6763c6af466a8c94497c0dedf700c36 | Independent action, observation, and usage totals |

All three sizes and hashes were rechecked read-only for this report. The temporary parser at .local/scratch/s08-02-boundary-attribution.py used only timestamps, request IDs, tool names, error/repair markers, and usage-presence flags. It was run twice against the same inputs and produced the same 21-row classification. It did not print message bodies, headers, cookies, credentials, or personal data. Raw evidence remains local and on its existing hold; no raw log was added to Git.

## 4. 21-Boundary Attribution Table

Times below are the log's 2026-09-29 Shanghai-local clock values. Each request window is foreground Runner work. Repair time is the nearest timestamped StreamEventRail context-repair marker after the connection failure; the traceback line itself has no timestamp. Every request contains one connection-error cluster. “Positive usage” means positive token usage followed the repair before successful completion. Action counts are successful take_action calls; the initial request also contains one new_game and one handbook read, which are not included in the action column.

| # / Runner send | Foreground request ID | Request window start–finish | Counted final / repair marker | observe / take_action | Post-repair usage | Classification |
|---|---|---|---|---:|---|---|
| 1 initial | ws_02faacc9a6b3 | 16:09:10.552–16:09:21.557 | final 16:09:21.570; repair 16:09:21.514 | 1 / 0 | positive | NORMAL_PRODUCTIVE_COMPLETE |
| 2 cont-1 | ws_dd5ea248c8a5 | 16:09:21.573–16:09:49.923 | final 16:09:49.939; repair 16:09:49.893 | 4 / 5 | positive | NORMAL_PRODUCTIVE_COMPLETE |
| 3 cont-2 | ws_ac1481121c01 | 16:09:49.942–16:10:07.900 | final 16:10:07.912; repair 16:10:07.856 | 2 / 1 | positive | NORMAL_PRODUCTIVE_COMPLETE |
| 4 cont-3 | ws_5eababfd9c15 | 16:10:07.914–16:10:12.459 | final 16:10:12.471; repair 16:10:12.428 | 0 / 1 | positive | NORMAL_PRODUCTIVE_COMPLETE |
| 5 cont-4 | ws_3719ef746ff8 | 16:10:12.474–16:10:59.809 | final 16:10:59.825; repair 16:10:59.772 | 3 / 3 | positive | NORMAL_PRODUCTIVE_COMPLETE |
| 6 cont-5 | ws_5e9e440c2536 | 16:10:59.828–16:11:01.237 | final 16:11:01.249; repair 16:11:00.740 | 0 / 0 | none | ERROR_ONLY_PROVIDER_TERMINATION |
| 7 cont-6 | ws_4cdedd3e9a91 | 16:11:01.252–16:11:18.924 | final 16:11:18.935; repair 16:11:18.891 | 1 / 1 | positive | NORMAL_PRODUCTIVE_COMPLETE |
| 8 cont-7 | ws_0d3351dcbdc7 | 16:11:18.937–16:11:20.229 | final 16:11:20.241; repair 16:11:19.916 | 0 / 0 | none | ERROR_ONLY_PROVIDER_TERMINATION |
| 9 cont-8 | ws_2c554a42e46a | 16:11:20.245–16:11:30.192 | final 16:11:30.206; repair 16:11:30.157 | 1 / 1 | positive | NORMAL_PRODUCTIVE_COMPLETE |
| 10 cont-9 | ws_3ec9247ff9d7 | 16:11:30.208–16:11:32.834 | final 16:11:32.847; repair 16:11:32.796 | 1 / 0 | positive | NORMAL_PRODUCTIVE_COMPLETE |
| 11 cont-10 | ws_f1001cb4fbfb | 16:11:32.849–16:11:34.272 | final 16:11:34.285; repair 16:11:33.916 | 0 / 0 | none | ERROR_ONLY_PROVIDER_TERMINATION |
| 12 cont-11 | ws_3329ffa2e296 | 16:11:34.288–16:11:36.097 | final 16:11:36.118; repair 16:11:35.353 | 0 / 0 | none | ERROR_ONLY_PROVIDER_TERMINATION |
| 13 cont-12 | ws_385efc892541 | 16:11:36.120–16:11:40.932 | final 16:11:40.942; repair 16:11:40.892 | 1 / 1 | positive | NORMAL_PRODUCTIVE_COMPLETE |
| 14 cont-13 | ws_a1d9dd9b3c05 | 16:11:40.945–16:11:42.874 | final 16:11:42.888; repair 16:11:41.969 | 0 / 0 | none | ERROR_ONLY_PROVIDER_TERMINATION |
| 15 cont-14 | ws_81c509126a0d | 16:11:42.890–16:11:51.539 | final 16:11:51.549; repair 16:11:51.507 | 1 / 1 | positive | NORMAL_PRODUCTIVE_COMPLETE |
| 16 cont-15 | ws_3772c7008bd9 | 16:11:51.552–16:11:53.023 | final 16:11:53.033; repair 16:11:52.560 | 0 / 0 | none | ERROR_ONLY_PROVIDER_TERMINATION |
| 17 cont-16 | ws_117e48b07391 | 16:11:53.035–16:12:09.742 | final 16:12:09.753; repair 16:12:09.713 | 2 / 2 | positive | NORMAL_PRODUCTIVE_COMPLETE |
| 18 cont-17 | ws_83b5421b527b | 16:12:09.755–16:12:32.273 | final 16:12:32.286; repair 16:12:32.226 | 2 / 3 | positive | NORMAL_PRODUCTIVE_COMPLETE |
| 19 cont-18 | ws_9d184c17b50a | 16:12:32.289–16:12:33.918 | final 16:12:33.934; repair 16:12:33.336 | 0 / 0 | none | ERROR_ONLY_PROVIDER_TERMINATION |
| 20 cont-19 | ws_036f18706c43 | 16:12:33.937–16:12:44.325 | final 16:12:44.337; repair 16:12:44.286 | 1 / 1 | positive | NORMAL_PRODUCTIVE_COMPLETE |
| 21 cont-20 | ws_88c4766d35bd | 16:12:44.339–16:13:02.630 | final 16:13:02.644; repair 16:13:02.586 | 3 / 3 | positive | NORMAL_PRODUCTIVE_COMPLETE |

| Classification | Count |
|---|---:|
| ERROR_ONLY_PROVIDER_TERMINATION | 7 |
| WORK_THEN_PROVIDER_ERROR_TERMINATION | 0 |
| NORMAL_PRODUCTIVE_COMPLETE | 14 |
| NORMAL_NO_WORK_COMPLETE | 0 |
| AMBIGUOUS_MIXED | 0 |
| UNMAPPED_OR_INSUFFICIENT | 0 |
| TOTAL_COUNTED_BOUNDARIES | 21 |

The seven zero-work boundaries match S08-01's silent continuation indices 5, 7, 10, 11, 13, 15, and 18; they are counted boundaries 6, 8, 11, 12, 14, 16, and 19. The remaining 14 each contain post-repair positive usage and productive work.

## 5. Provider Error Terminal-Cause Audit

The repeated family is httpx.ConnectError surfaced as openai.APIConnectionError and logged as llm_call_error. Each of the seven error-only boundaries has no observe/action or positive collector usage, followed by a zero-token request summary and terminal chat.error/chat.final markers. The outer Runner collector still records e2a.complete with status=succeeded; this wrapper-level success does not erase the inner provider failure.

For the other 14 boundaries, the connection-error cluster and repair marker precede positive token usage and later productive work; their final request tail has no terminal chat.error/chat.final pair and the Runner records normal e2a.complete/succeeded. Under the Plan's terminal-tail rule these are NORMAL_PRODUCTIVE_COMPLETE. “An error occurred somewhere in the request” is not sufficient to classify the request as provider-terminated. There are no work-then-error, mixed, or unmapped boundaries.

The service log repeats APIConnectionError text within a traceback. That repetition is one error cluster, not evidence of three independent failed requests or three retry attempts. The traceback does not expose a timestamp for the precise exception line; the table records the nearest later timestamped repair marker.

## 6. Continuation Budget Accounting

- Counted boundaries: 21 = one initial request plus 20 continuation requests.
- Provider-error-terminated boundaries: 7 + 0 = 7.
- Provider-error boundary share: 7 / 21 = 33.3%.
- Zero-work provider share: 7 / 20 continuations = 35%.
- The shares describe this run only; they are not probabilities or a reliability estimate.

Mechanical counterfactual:

    observed_counted = 21
    minus clearly provider-error-terminated boundaries = 7
    residual counted boundaries = 14

COUNTERFACTUAL_ACCOUNTING_ONLY / NOT_GAMEPLAY_PREDICTION. This arithmetic does not predict that a game would have completed without transport errors, nor estimate the month or score it could have reached.

## 7. Historical Error-Family Comparison

| Task | Context and error family | HTTP response observed? | Fresh game work? | Outer termination | Conclusion |
|---|---|---|---|---|---|
| S07-38 / v7i | 23 connection errors in the failed run path | No response established for the connection failures | No fresh game action before failure | Technical failure | Same connection-layer family; no gameplay attribution |
| S07-39 | httpx.ConnectError → openai.APIConnectionError → FrameworkError | No HTTP status | Not a game run | Provider transport failure | Deeper network cause remained unknown |
| S07-50 | Provider-only evaluation: 3 connection failures, including 2 consecutive, plus 2 empty outputs | No usable response for failed requests | No game work | Stopped at 5/80 requests; cases TECHNICAL_UNKNOWN | Consistent intermittent completion-path transport issue |
| S07-50R | Single provider preflight ended TRANSPORT_ERROR before HTTP | No | No game work | Further requests not run | Same transport boundary; no behavioral inference |
| S07-51R | 21 foreground connection-error clusters, of which 14 recovered into productive work and 7 terminated without work | No HTTP status in the captured error family | Yes: 23 successful actions and 23 observes across productive boundaries | Runner reached M6, then max_continuations; partial technical failure | Mixed provider and execution-persistence evidence |

Sources: docs/project/runs/v7i-run1-validation.md; docs/project/reviews/S07-39_PROVIDER_CONNECTIVITY_FORENSICS.md; docs/project/reviews/S07-50_SKILL_AUTHORING_AUDIT.md; docs/project/reviews/S07-50R_PROVIDER_AND_BEHAVIORAL_EVAL.md; docs/project/runs/v7n-run1-replacement-validation.md. No historical raw log was reopened for this comparison.

## 8. Residual Execution-Persistence Analysis

After excluding only the seven provider-error terminal boundaries, 14 NORMAL_PRODUCTIVE_COMPLETE boundaries remain. They contain 23 successful take_action calls and 23 observes:

- Actions per normal productive execution: 23 / 14 = 1.64.
- Observes per normal productive execution: 23 / 14 = 1.64.

The initial request also made one new_game call and one handbook read; neither is included in the take_action rate. The 14 normal productive boundaries are the residual whole-game persistence risk. They must not be attributed to provider errors or treated as proof that Candidate wording caused the continuation burn. One partial run at M6 does not establish the later trajectory.

## 9. Runtime Resilience Seam Inspection

The bounded source inspection found a local SDK retry seam without editing installed code:

| Surface | Source evidence | Finding |
|---|---|---|
| OpenJiuwen model client config | .venv/Lib/site-packages/openjiuwen/core/foundation/llm/schema/config.py, ModelClientConfig lines 39–85 | max_retries is an integer field with default 1; described for transient HTTP failures including connection drops, 429, and 5xx |
| JiuwenSwarm adapter | .venv/Lib/site-packages/jiuwenswarm/server/runtime/agent_adapter/interface_deep.py, _build_model_from_entry lines 3044–3058 | model_client_config fields are passed into ModelClientConfig |
| OpenJiuwen OpenAI client | .venv/Lib/site-packages/openjiuwen/core/foundation/llm/model_clients/openai_model_client.py, _build_async_openai_client lines 217–254 | passes ModelClientConfig.max_retries to openai.AsyncOpenAI |
| OpenAI SDK behavior | .venv/Lib/site-packages/openai/_base_client.py, retry loop around lines 1014–1072 | retries eligible connection exceptions according to the configured value and raises APIConnectionError when exhausted |
| Existing LLMRetryRail | .venv/Lib/site-packages/openjiuwen/harness/rails/llm_retry_rail.py, especially lines 124–132 and 202–236 | covers repeated output suffixes and stream frame timeouts; it does not retry APIConnectionError |
| StreamEventRail | .venv/Lib/site-packages/jiuwenswarm/agents/harness/common/rails/stream_event_rail.py, on_model_exception lines 788–792 | repairs incomplete tool context; it is not a provider retry-count setting |

The current project runtime manifest does not expose model_client_config or max_retries. The effective local override was not read, so the configured value for the captured run is UNKNOWN; only the installed schema default is confirmed. No dependency or site-package was changed.

## 10. Submission Deployability Boundary

| Seam class | Finding |
|---|---|
| SUBMISSION_CONTROLLED_SUPPORTED | NO. The current solution manifest has team/name/mode/instruction; the frozen official package contract lists manifest, README, design documents, and Skills. No submission-owned retry field was evidenced. |
| PROJECT_RUNTIME_CONFIG_SUPPORTED | YES for local development runtime configuration: ModelClientConfig.max_retries is carried into AsyncOpenAI without a dependency patch. |
| FRAMEWORK_OPTION_SUPPORTED_BUT_DEPLOYABILITY_UNKNOWN | NO separate relevant option was found in LLMRetryRail; its behaviors do not address this error family. |
| PATCH_REQUIRES_FROZEN_COMPONENT | Only if retry behavior is added by intercepting Runner boundaries or patching the Runner/framework. That is not required for the existing local SDK config seam and is outside this task. |
| NO_RELEVANT_SEAM_FOUND | NO; a relevant local runtime-config seam exists. |
| INSUFFICIENT_EVIDENCE | Cloud/official portability and the effective local override remain UNKNOWN. |

Source references: docs/project/OFFICIAL_SOURCE_LOCK.md, solution package description around lines 89–97; configs/runtime_manifest.json; configs/current_candidate.json. These files were inspected statically. No runtime configuration value or secret was opened.

## 11. Provider Preflight Value

Decision: RUNTIME_RESILIENCE_MORE_VALUABLE_THAN_PREFLIGHT. S07-39's DNS/TCP/TLS and metadata request passing did not establish long completion stability; S07-50/50R and S07-51R show transport failures on completion paths. A cheap reachability check therefore cannot substitute for request-level resilience. A future bounded provider-completion preflight would still require separate provider-request authorization and would not guarantee a full game. No probe or request was performed here.

## 12. FACT / INFERENCE / HYPOTHESIS / UNKNOWN

### FACT

- The service log maps 21 foreground Runner requests to 21 counted boundaries; five prewarm requests are separate background activity.
- Each foreground request contains one httpx.ConnectError / APIConnectionError cluster.
- Seven requests terminate with no game tools or positive usage and an error finalization tail; 14 have positive usage after repair and productive work.
- The 21 boundaries contain 23 successful take_action calls and 23 observes; the run reached M6 and exhausted max_continuations.
- Installed ModelClientConfig.max_retries defaults to 1 and is passed through to AsyncOpenAI.
- Current submission manifest does not expose this field.

### INFERENCE

- Provider failures materially contributed to the continuation budget burn, but do not explain all persistence risk.
- R2 MIXED_PROVIDER_AND_EXECUTION_PERSISTENCE is the best fit: 7 terminal provider-error rounds are material; 14 normal productive rounds remain.
- A local runtime resilience task is better supported than a provider reachability preflight as the next bounded direction.

### HYPOTHESIS

- Raising or otherwise configuring the local SDK retry policy may reduce zero-work provider boundaries. This review did not implement or measure that effect.
- The remaining productive boundaries may still exhaust a future run's continuation budget before 48 months. A single run cannot establish that outcome.

### UNKNOWN

- Root network cause, HTTP status for the failed connections, and exact SDK retry attempts in the captured run.
- Effective local max_retries override at run time.
- Cloud/official submission portability of the local runtime setting.
- Whether a retry policy would change the gameplay trajectory, score, or 48-month completion probability.

## 13. Root-Cause Classification

Decision: MIXED_PROVIDER_AND_EXECUTION_PERSISTENCE (R2), MEDIUM confidence.

- R1 PROVIDER_DOMINANT does not apply: 7/21 is below the 14-boundary threshold and is not a majority.
- R2 applies: 7 provider-terminal rounds are a material contribution, while 14 normal productive rounds remain and preserve substantial persistence risk.
- R3 EXECUTION_PERSISTENCE_DOMINANT does not apply because provider-terminal contribution is not small.
- R4 INSUFFICIENT_EVIDENCE does not apply to boundary mapping or terminal attribution; all 21 are mapped. It remains appropriate for deeper network cause and causal effect.

Boundary mapping/terminal classification confidence is high from request IDs, serialized request windows, error/repair markers, and terminal tails. Root interpretation confidence is medium because this is one uncontrolled trajectory and cannot isolate cause or predict counterfactual gameplay.

## 14. Next Recommendation

S08_RUNTIME_RESILIENCE_IMPLEMENTATION_JUSTIFIED.

The next Stage task may evaluate a bounded local runtime configuration change using the existing model-client max_retries path. Keep it separate from Candidate authoring and frozen Runner changes; verify the exact config carrier before implementation. This recommendation does not authorize installing anything, changing the environment, sending provider requests, or starting a game. Cloud portability remains UNKNOWN, and any real-run validation requires a separate Main authorization.

## 15. Limitations

- The collector event file lacks request IDs; mapping is recovered by serialized service lifecycle and terminal-time correlation.
- Exception traceback text itself is un-timestamped; repair-marker timestamps are later markers, not exact exception timestamps.
- A repeated exception name within a traceback is not a retry count.
- The service log reveals error/finalization structure, not the lower-level DNS, TCP, TLS, proxy, or provider cause.
- The 21-boundary mapping applies only to this v7n session. Historical comparisons reuse committed summaries, not a pooled reliability denominator.
- The parser is a task-local ignored scratch artifact and is not included in the commit.
- No live validation was performed; no conclusion here validates current runtime resilience or gameplay.
