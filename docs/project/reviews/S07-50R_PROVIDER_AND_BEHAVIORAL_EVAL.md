# S07-50R — Provider Contract Diagnosis & Behavioral Eval Resume

## Status

PARTIAL / PROVIDER_PREFLIGHT_FAIL. This task preserved S07-50's historical audit, repaired the isolated provider-evaluation harness, and attempted the one authorized preflight. The preflight ended with TRANSPORT_ERROR before an HTTP response. Under the frozen gate, sanity and A/B evaluation were not run.

- Base: main@209e66e1bd4520536872eeb70db48bfd92ebc35e
- Candidate: candidate-v7n-public-state-delivery-constraint-hardening
- Scope: provider-only micro-evaluation and offline harness; no game, service, Runner, MCP, shared DB, install, or Skill reload.
- NEXT_GAME: NOT_AUTHORIZED

## 1. Executive conclusion

The old S07-50 result remains TECHNICAL_UNKNOWN; its empty outputs do not establish a Skill failure. The two HTTP-200 empty responses lacked finish_reason, reasoning-token, and usage metadata. A small max_tokens=500 budget under Thinking Mode is a plausible explanation, but it is not proven.

The S07-50R preflight used an explicitly recorded provider request contract and a larger token ceiling. The request failed at the transport layer with no HTTP status or response. Therefore it does not diagnose JSON Output, Thinking Mode, or model behavior. The required STOP gate fired correctly: 0 sanity requests and 0 matrix requests followed.

No experimental rewrite is recommended for integration. All four Skill decisions and the manifest decision are INSUFFICIENT_EVAL_EVIDENCE. Recovery remains PROMPT_LEVEL_RECOVERY_REWRITE_NOT_JUSTIFIED.

## 2. Official DeepSeek contract consulted

Only official DeepSeek documentation was used for API behavior:

- The current change log maps deepseek-flash to the DeepSeek-V4.1-Flash API model. This establishes the current alias mapping, not the historical underlying version of prior requests. [DeepSeek API change log](https://api-docs.deepseek.com/updates/)
- Chat Completions documents thinking as enabled by default, reasoning_effort as high by default, max_tokens as the generation limit, response_format={"type":"json_object"}, stream, finish_reason, and separate final content / reasoning_content fields. It also exposes reasoning token usage separately. [Chat Completions API](https://api-docs.deepseek.com/api/create-chat-completion/)
- Thinking Mode documentation states that the default is enabled/high, temperature has no effect in Thinking Mode, and chain-of-thought is returned separately in reasoning_content. [Thinking Mode](https://api-docs.deepseek.com/guides/thinking_mode/)
- JSON Output documentation says prompts must explicitly request JSON and that JSON mode can occasionally return empty content. [JSON Output](https://api-docs.deepseek.com/guides/json_mode/)

These sources define the provider contract. They do not prove which optional parameters the CareerSim AgentServer sent during S07-46.

## 3. Runtime provider contract evidence

Classification: RUNTIME_PROVIDER_CONTRACT_PARTIAL.

| Field | Finding | Evidence and limit |
|---|---|---|
| Requested model alias | deepseek-flash | Accepted S07-46 run report and S07-39 provider report. Two old S07-50 responses also reported this alias. |
| Endpoint | https://api.deepseek.com | Accepted run/provider records; endpoint host is retained without credentials. |
| Current official alias mapping | DeepSeek-V4.1-Flash | Official change log dated 2026-09-10. Do not backdate this mapping to older runs. |
| thinking | UNKNOWN | No request-bound setting found in accepted records. Official default is enabled; eval labels this condition separately. |
| reasoning_effort | UNKNOWN | No request-bound setting found. Official default is high. |
| max_tokens | UNKNOWN | The prior standalone eval harness set 500; that was not evidence of CareerSim runtime configuration. |
| temperature | UNKNOWN for DeepSeek chat requests | The bounded S07-46 service-log metadata pass saw 0.95 on generic OpenAI/LLM-related lines, but could not bind it to a DeepSeek chat request. It is omitted from this Thinking Mode eval because the official API says it has no effect there. |
| stream | UNKNOWN for DeepSeek chat requests | Both true and false appeared in the bounded service logs, without request/model linkage. |
| response_format | UNKNOWN at runtime | No request-bound setting found. |

The local inspection was limited to the known S07-46 Runner stderr and the run-window service-start logs under .local/runtime/s07-46-v7m-run1/. It emitted only allowlisted parameter names/values and logger-category tokens; no raw log line, credential, prompt, or reasoning text was printed. The mixed temperature/stream observations are not promoted to runtime facts.

## 4. Prior empty-content diagnosis

S07-50 made 5 provider requests: 3 connection-layer failures and 2 HTTP-success responses with empty final content. Both empty responses were on the current-v7n side; the rewrite was never reached. The previous harness request used max_tokens=500, temperature=0, stream=false, and did not set response_format.

The old result file did not retain finish_reason, reasoning_content presence/length, or token usage. The two old cases therefore remain EMPTY_CONTENT_DIAGNOSIS_UNKNOWN, not EMPTY_CONTENT_LENGTH, EMPTY_CONTENT_WITH_REASONING, or behavioral FAIL.

Hypothesis H_PROVIDER_01 — the 500-token completion ceiling may have been consumed by Thinking Mode before final content — remains PLAUSIBLE / UNCONFIRMED. The current official default is Thinking enabled/high, and the API's max_tokens ceiling can constrain the generated response, but the old empty rows lack the metadata needed to attribute cause.

## 5. Harness changes

scripts/skill_behavior_eval.py now supports three separately gated stages:

1. preflight: one unrelated compact-JSON request.
2. sanity: B1 and R3 once each for current and rewrite.
3. matrix: the original 21 cases / 20 request units / two versions / two repetitions, capped at 80 matrix requests.

The total new-request cap is 85. A stage is persisted before sending a request, and an unresolved IN_FLIGHT outcome blocks accidental duplicate submission. Matrix execution is impossible unless both prior stages are recorded as PASS. An isolated matrix TRANSPORT_ERROR can use at most one retry inside the 80-call matrix cap. Two consecutive provider technical failures or two consecutive empty-content responses stop the matrix.

The eval payload is explicitly labeled OFFICIAL_DEFAULT_THINKING with thinking=enabled, reasoning_effort=high, max_tokens=4096, stream=false, and JSON Output. temperature is omitted. Since actual CareerSim Thinking Mode has not been verified, transfer is explicitly RUNTIME_MODE_NOT_VERIFIED; no runtime-equivalence claim is made.

JSON Output was included in the preflight request as the machine-grading condition under trial. The preflight failed before HTTP, so the JSON-format decision is UNVERIFIED; there is no positive probe evidence for compatibility or output benefit. Do not treat its inclusion in the attempted payload as a successful JSON-mode test.

For each response, the new result schema stores HTTP status/success, reported model, finish reason, content presence/length, reasoning presence/length, and reported token usage. It never stores reasoning_content text, headers, API keys, raw error bodies, or exception messages. Only final observable content is kept, after secret redaction, so deterministic assertions can run.

Empty content is classified as EMPTY_CONTENT_LENGTH, EMPTY_CONTENT_WITH_REASONING, or EMPTY_CONTENT_OTHER; it is never graded as ordinary Skill FAIL. Non-empty unparseable JSON is UNPARSEABLE_OBSERVABLE_OUTPUT, a behavioral failure unless provider metadata shows truncation. A successful HTTP status does not reset an empty/technical failure streak.

New output is isolated at [provider_results.json](../../../experiments/s07-50r/evals/provider_results.json). The S07-50 result file and frozen experimental rewrite were not overwritten or edited.

## 6. Preflight result

| Measure | Result |
|---|---|
| New requests | 1 |
| Requested model / endpoint | deepseek-flash / api.deepseek.com |
| HTTP status / HTTP success | No HTTP response / false |
| Failure category | TRANSPORT_ERROR |
| Provider-reported model | UNKNOWN |
| finish_reason, content and usage | No response; UNKNOWN |
| Gate | PROVIDER_PREFLIGHT_FAIL |

The attempt used the single preflight allowance. Per Plan, no retry was made after preflight failure.

## 7. Sanity and matrix gates

- Sanity gate: NOT_RUN / BLOCKED_BY_PREFLIGHT_FAIL; requests = 0.
- Full matrix: NOT_REACHED; requests = 0.
- New requests in S07-50R: 1 of 85 maximum.
- Historical S07-50 requests: 5.
- Historical plus new request attempts: 6.
- Empty-content failures in S07-50R: 0. The new attempt failed before receiving a response.
- Token usage and actual API cost for the new attempt: UNKNOWN; no provider usage payload was received.
- Full A/B behavioral evidence: NOT_OBTAINED.

The failed preflight is a provider/transport observation, not a behavioral failure for either version.

## 8. Behavioral decisions and regressions

| Scope | A/B decision | Evidence |
|---|---|---|
| Board | INSUFFICIENT_EVAL_EVIDENCE | Sanity and matrix did not run. |
| Planning | INSUFFICIENT_EVAL_EVIDENCE | Sanity and matrix did not run. |
| Delivery | INSUFFICIENT_EVAL_EVIDENCE | Sanity and matrix did not run. |
| Risk | INSUFFICIENT_EVAL_EVIDENCE | Sanity and matrix did not run. |
| Integrated manifest de-duplication | INSUFFICIENT_EVIDENCE | Integrated cases are in the unreached matrix. |
| Critical regressions | UNKNOWN / NOT_EVALUATED | No comparable outputs were produced. |
| Recovery rewrite | PROMPT_LEVEL_RECOVERY_REWRITE_NOT_JUSTIFIED | Preserved S07-50 conclusion; not re-prompted. |

No Candidate, formal Skill, runtime manifest, eval case, or experimental rewrite change is recommended from this result.

## 9. Files and verification

Changed repository files:

- scripts/skill_behavior_eval.py
- tests/test_skill_behavior_eval.py
- experiments/s07-50r/evals/provider_results.json
- docs/project/reviews/S07-50R_PROVIDER_AND_BEHAVIORAL_EVAL.md
- docs/project/CURRENT_STATE.md

The S07-50R Plan was copied byte-for-byte to D:\CS\temp\CareerSim\S07-50R｜Provider Contract Diagnosis & Behavioral Eval Resume.md; source and destination SHA-256 matched at copy time: 5D3F6E022B9E2EA6AF1B099CD1FA1C5DCBAAD7BEC14D858BCF4B82A3CC6A71A8.

Offline verification: targeted eval tests 19 passed; Python compilation passed; offline harness plan reports 21 cases / 20 request units / 80 matrix calls / 85 total calls. git diff --check passed. Formal Candidate identity, four formal Skills, and formal runtime manifest are unchanged.

## 10. Limitations and next action

- The current transport path failed before HTTP, so model response behavior, JSON Output, finish reason, and usage remain unobserved.
- The two prior empty responses cannot be diagnosed retrospectively because the old harness discarded the relevant response metadata.
- No A/B evidence supports promotion of any rewrite. Keep the isolated rewrite and formal v7n unchanged.
- A future provider-only retry requires a new Main decision/task; this report does not authorize a game, service, Runner, or Candidate validation.

S07 remains ACTIVE. NEXT_GAME = NOT_AUTHORIZED.
