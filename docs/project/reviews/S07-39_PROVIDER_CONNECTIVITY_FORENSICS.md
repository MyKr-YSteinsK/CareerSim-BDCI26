# S07-39 — DeepSeek provider connectivity forensics and retry gate

## Identity and scope

- Base: `main@61621748f322bfcd015d88250d9935bd5247eb6f`, equal to `origin/main`; working tree was clean before this report. Candidate remained `candidate-v7i-pre-review-result-realization-probe`.
- Frozen Candidate identity matched: manifest SHA-256 `0946e8b3c7cff62661bfb948a9e0cde39fce664847cb41bae4390587ae6c4fa3`; instruction SHA-256 `0dd590d21e036e5dc4cdde25553d250ac87439ab4cc1af29bc75c07367026721`.
- S07-38 evidence-manifest SHA-256 matched the Plan lock: `452188879cafef44bff398f407d04bb38ef32bc92e52c012873ce2ac9ac60505`. Held evidence was read in place; no file was deleted, moved, or overwritten.
- This task did not start `career_emu`, install/reload a submission, run a game, read the shared DB, change provider configuration, or edit Candidate/Skill/manifest files.

## S07-38 historical exception

- S07-38's LLM log records 23 connection errors in the Runner window, from `2026-09-28 18:35:41` through `18:36:03` local time. The service's terminal exception chain is visible as `httpx.ConnectError` → `openai.APIConnectionError: Connection error` → Jiuwen `FrameworkError [181001]`. The LLM log's public-facing message is `OpenAI API async stream error`.
- The exception occurred before an HTTP response: no HTTP status code is recorded. The stack does not identify a DNS failure, TLS validation error, proxy exception, socket error code, or deeper OS cause. `ROOT_CAUSE_FROM_LOG = UNKNOWN`.
- The service was configured for host `api.deepseek.com`, model alias `deepseek-flash`; S07-38 recorded two earlier connection-error events during startup. No credentials or authorization headers were copied into this report.

## Current read-only network checks

Checks ran sequentially on 2026-09-28, with `career_emu` stopped throughout.

| Layer | Result |
|---|---|
| DNS `api.deepseek.com` | PASS at `2026-09-28T10:51:58.858Z`; two IPv4 addresses resolved, no IPv6 address returned. Addresses are not retained. |
| TCP 443 | PASS; 31.1 ms. |
| TLS/HTTPS transport handshake | PASS; 83.9 ms, TLS 1.3, `TLS_AES_256_GCM_SHA384`; no HTTP request was sent in this phase. |
| Proxy/environment | `HTTP_PROXY`, `HTTPS_PROXY`, and `NO_PROXY` variables are present in the diagnostic process; `ALL_PROXY` is absent. Values were not read out or recorded. Instance endpoint/model remained `https://api.deepseek.com` / `deepseek-flash`; credential presence was confirmed without displaying its value. Python `httpx` 0.28.1 and `openai` 2.41.0. |

### Single metadata request

- Exactly one HTTP `GET https://api.deepseek.com/models` was sent at `2026-09-28T10:57:43.724390Z`; it completed at `10:57:44.037720Z` with HTTP 200.
- Response was parseable; it listed two model IDs and included the configured `deepseek-flash` alias. The response body and model list were not retained. Token usage: `N/A`; no completion/chat request or prompt was sent. The request used the current credential without printing it and honored the process's existing HTTP client environment.
- A local metadata summary, without credentials or response body, is `.local/runtime/s07-38-v7i-run1/provider-metadata.json`, SHA-256 `e5ce352dd439940d51e1f9fc7fdeb52f58e3daa563f797ab6c447a41184033fa`.

## Root cause and retry gate

- Historical classification: `LIKELY_TRANSIENT_OR_UNRESOLVED`; the old run's deepest available error is a connection failure without a lower-level cause. Today's successful connectivity does not establish why S07-38 failed.
- Current classification: `PROVIDER_HTTP_REACHABLE` and `CURRENT_CONNECTIVITY_READY / HISTORICAL_ROOT_CAUSE_UNKNOWN`.
- **`RETRY_GATE_PASS`**: DNS, TCP 443, TLS, the single metadata request, Candidate identity, and configuration identity passed; no secret exposure or configuration change occurred. This only makes a replacement game eligible for separate Main authorization. It does not authorize or start a game.

## Stale-score hazard — read-only source review

- S07-38's emitted score report contains game session `d4464a311c924e73b9e23eebd6f71f6d`, the prior v7g run. Its score is not a v7i result.
- The current frozen Runner source extracts session IDs from structured `new_game`/`observe` tool results, but also falls back to searching transcript text for `SESSION_ID=<hex>`. `headless_play` passes the resulting ID to score reporting; `score.py` queries that ID when nonempty and only calls `latest_session_id` when it is empty. An old textual session ID can therefore be accepted as the current run identity when no fresh structured game identity exists.
- Classification: `RUNNER_STALE_SCORE_HAZARD_CONFIRMED / DEFER_PATCH`. A run/session identity gate can prevent the report from being interpreted as fresh evidence; eliminating the Runner source hazard requires a separate authorized code task. No Runner patch was made here.

## Accounting and limits

- Service starts/stops: 0 / 0; installs/reloads: 0; Runner plays/games: 0; shared DB reads: 0; chat/completion generation: 0; metadata provider requests: exactly 1.
- No Candidate validation flag changed; `next_game_authorized=false` remains unchanged.
- DNS/TCP/TLS and a successful metadata request show the current path can reach the provider. They do not prove that the earlier transient was repaired or identify its historical cause.

Final handoff: `RETURN_TO_MAIN_AFTER_PROVIDER_CONNECTIVITY_GATE`
