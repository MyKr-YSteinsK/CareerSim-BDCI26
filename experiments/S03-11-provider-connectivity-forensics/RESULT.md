# S03-11｜Provider 连接根因取证与无对局恢复预检

## Identity / scope

- Branch: `codex/s03-11-provider-connectivity-forensics`; parent `3c4a2f04df79158e88c56ec6bf7f76be63e0a064`; fetched `origin/main` `73a69668812f28076abcebd0a90e1cf71b20f64c` is an ancestor. Plan contract blob: `1a7a7b67735ee99d3cd9f2521913da884df8538a`.
- Decision: `PROVIDER_PREFLIGHT_PASS`; S03-12 readiness: `READY_FOR_ONE_RISK_CORRECTNESS_SMOKE`. This authorizes only Stage Review consideration of a *future* single smoke, not a game in S03-11.
- No service startup, Agent chat, Runner play, CareerSim tool invocation, gameplay, persistent provider/model/config edit, dependency change, or retry. `FORENSIC_HOLD:S03-MCP-REGISTRATION` remains `ACTIVE / UNCHANGED`; five canonical snapshots still match their registered bytes and SHA256.

## S03-10 failure forensics

- The archived gameplay window started at `2026-09-23T10:39:53.8495534Z`. Parsed archived `llm.log`: 17 `llm_call_start` events (`18:39:59.327218`–`18:42:54.403342 +08:00`), 16 `llm_call_error` events (`18:40:09.769379`–`18:42:53.591315 +08:00`), no `llm_call_end`; every error was `APIConnectionError: Connection error.` and every recorded model was `deepseek-flash`. These are framework events from the one authorized S03-10 play, not 17 separate S03-11 probes. No completed usage or CareerSim game/tool event was recorded there.
- Archived service stderr shows `httpcore._async.connection._connect` failing at `stream.start_tls(**kwargs)`, then `httpcore.ConnectError` → `httpx.ConnectError` → `openai.APIConnectionError`. This locates the observed failure at the **TLS-start transport connection** before any HTTP/provider response. The traceback does not expose the underlying peer/TLS reason; it does not establish a certificate error, proxy outage, auth failure, invalid model, 429, or provider HTTP status. The logged configured target was `https://api.deepseek.com`; the failed socket's actual peer was not preserved.
- Raw, ignored evidence re-hashed against S03-10: `D:\CS\CareerSim\.local\runtime\s03-10-standard-play-risk-smoke\service-start.stderr.log` (2,485,424 bytes; SHA256 `A14E8E2086C50348E2AF3342C74DC3A61222E70ED4D81C4B1981212132E6539D`) and `D:\CS\CareerSim\.local\runtime\s03-10-standard-play-risk-smoke\post-stop-shared-logs\llm.log` (2,815,539 bytes; SHA256 `36A241A665820183C9C5AD35F5BCE778A7C8568CB5C1BB29EBB7379178503C3B`). Raw logs are not committed.
- S01-03 baseline and S03-06/07/08 prior successful startup/prewarm records establish that the same endpoint/model/provider family had worked previously; S03-06/07/08 each report a completed `deepseek-flash` prewarm (200 input / 1 output / 201 total). S03-10 itself reported no completed provider usage. This is evidence of a later intermittent transport failure, **not** proof of its exact external cause.

## Current environment and layered probes

- Current instance env has `API_BASE=https://api.deepseek.com`, `MODEL_NAME=deepseek-flash`, `MODEL_PROVIDER=OpenAI`, and a present key. The instance key, Windows User `DEEPSEEK_API_KEY`, and current process `DEEPSEEK_API_KEY` were compared in memory and match; no key or fingerprint was printed or saved. Instance `config.yaml` SHA256 `05928EFAED4508D2C1A70C6B32B704CADB3B1CD40026A5CDA0D91EDD4878DEFE` matches the S03-10 recorded config; current instance `.env` SHA256 `99842010A7B39B038AFE05009B75BC259BFEA34CFF40D93C9D41325167E8B8CD` is recorded only as an identity, not its contents. `verify_ssl=true`.
- No explicit `HTTP_PROXY`, `HTTPS_PROXY`, `ALL_PROXY`, `NO_PROXY`, `SSL_CERT_FILE`, `SSL_CERT_DIR`, or `REQUESTS_CA_BUNDLE` in current process/User/Machine environment. WinHTTP reports direct; WinINET has enabled `127.0.0.1:7897`, with a local `verge-mihomo` listener. Current Python `urllib` and HTTPX environment discovery select `http://127.0.0.1:7897`. JiuwenSwarm's OpenAI adapter builds `httpx.AsyncClient` with `UrlUtils.get_global_proxy_url(api_base)` (currently no explicit proxy env override) and HTTPX's default environment trust. S03-10 did not preserve process proxy state, so its historical proxy route and any transient proxy fault remain **unknown**. No endpoint/model/config drift was confirmed; historical key/proxy runtime drift cannot be excluded.
- One group each, all without credentials: DNS resolved `api.deepseek.com` to `198.18.0.74` (TTL 1); TCP connected to that address on 443 and local proxy on 7897; JiuwenSwarm strict SSL context completed TLS 1.3 with SNI `api.deepseek.com`; HTTPX GET to the configured provider host returned HTTP `401`. The `198.18.0.0/15` address is consistent with possible local fake-IP/TUN handling, but this is inference, not proof. HTTP `401` demonstrates current transport reachability, not model authorization or completion.

## Exact framework/provider-path verification

- Used installed `openjiuwen.core.foundation.llm.model_clients.openai_model_client.OpenAIModelClient` with current instance endpoint/model/provider/key source and strict SSL. No service was needed. SDK `max_retries=0` and 20 s timeout were **in-memory probe safeguards** (persistent instance config unchanged); each request used `Reply OK.` and `max_tokens=4`, with no CareerSim context or tools.
- Request 1, `invoke`, completed `2026-09-23T11:08:58.768538Z`: returned model `deepseek-flash`; input 33, output 4, total 37, cache 0, reasoning 4. Finish reason `length` is expected with the tiny output cap and does not negate transport/model completion.
- Request 2, independently exercising the S03-10 `stream` method, completed `2026-09-23T11:10:13.513556Z`: six parsed chunks, input 33, output 4, total 37, cache 0, reasoning 4; finish reason `length`. The model was requested as `deepseek-flash`; the probe's retained stream summary did not independently capture a returned model string.
- **Total S03-11 provider budget:** 2 attempts / 2 completed, no SDK retries; 66 input / 8 output / 74 total tokens, cache 0, reasoning 8. No provider cost was reported. The adapter's `UsageMetadata.total_cost=0.0` is a default when no cost field is supplied and is **not** evidence of zero actual charge. No further provider request is allowed in this task.

## Decision / boundaries / unknowns

- The S03-10 failure is classified sufficiently at the TLS-start connection layer; the immediate failing peer and why its handshake failed remain unknown. Both current non-streaming and the historical streaming adapter methods completed over the current endpoint/model/key. Thus `PROVIDER_PREFLIGHT_PASS` and `READY_FOR_ONE_RISK_CORRECTNESS_SMOKE` apply **at this preflight instant**; they do not guarantee future availability or retrospectively prove the proxy was the culprit.
- Service start/stop `0/0`; Agent chat `0`; Runner play `0`; `new_game`/`observe`/`take_action` and all other CareerSim tool calls `0`; game sessions `0`. No strategy correctness or score evidence was generated. Risk Hypothesis = `ACTIVE`; Risk effectiveness = `NOT_PROVEN`; controlled screening = `NOT_STARTED`.
- Config, credential value, Windows proxy/PATH/certificate state, Runner, Skills, and lock were not modified. Canonical hold snapshots still match 5/5. No raw env, headers, logs, DB, or secrets are committed.

## Verification / delivery

- Parent and fetched main ancestry: `PASS`; raw archive hashes: `PASS`; forensic hold snapshots: `PASS` (5/5); current config identity: `PASS` against S03-10; request and no-game budget: `PASS`.
- `uv lock --check`, `git diff --check`, protected-file diff/scope, secret scan, branch push, and clean-tree checks are performed at delivery; final results belong in `TASK_RESULT`.
- Compact machine-readable evidence: [provider_evidence.json](provider_evidence.json).
- Next Recommended Action: `S03 Stage Review`.
