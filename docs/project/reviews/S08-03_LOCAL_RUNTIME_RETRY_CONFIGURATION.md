# S08-03 — Local Runtime Retry Configuration and Static Verification

## 1. Result

- Status: COMPLETE for this bounded local configuration and offline/static verification task.
- Decision: `LOCAL_RETRY_STATIC_READY`.
- Selected `max_retries`: `2`.
- The named local runtime configuration was updated with one integer field. Its original bytes are preserved in an ignored local backup.
- No provider request, network probe, service lifecycle, MCP call, game action, database access, install, or dependency change occurred. S08 remains ACTIVE and `NEXT_GAME = NOT_AUTHORIZED`.

## 2. Identity / Scope

- Repository: `MyKr-YSteinsK/CareerSim-BDCI26`; branch: `main`.
- Base at task start: `93138492546f24be5fb0df0b4f4ed763dac3074a`, equal to refreshed `origin/main`.
- Stage: S08 ACTIVE; S07 COMPLETE.
- Current Candidate: `candidate-v7n-public-state-delivery-constraint-hardening`.
- Frozen Runner SHA: `f61c738c72e51b77298cc1c14c7c6ebf4b6c527d`.
- Installed identities: JiuwenSwarm `0.2.4b3`, OpenJiuwen `0.1.16.post2`, OpenAI SDK `2.41.0`.
- Work was limited to the selected local runtime config, this review, and a concise `CURRENT_STATE.md` entry. Candidate, Skills, runtime manifest, Runner, dependencies, and lockfile were not changed.

## 3. S08-02 Evidence Lock

S08-02 classified the captured v7n execution as `MIXED_PROVIDER_AND_EXECUTION_PERSISTENCE` with medium confidence. Seven of 21 counted execution boundaries (33.3%) ended as zero-work provider-error terminations; 14 completed productively after connection-error recovery. Those 14 boundaries contained 23 successful actions and 23 observes, leaving execution persistence as a separate residual risk. These counts describe that run only; they are not probabilities and do not establish the trajectory a retry would have produced.

The local retry setting addresses only the SDK transport retry seam. It does not explain the provider's underlying connection failures or resolve the 14 productive-boundary continuation risk.

## 4. Runtime Config Carrier

- Carrier: the existing `career_emu` named JiuwenSwarm instance configuration.
- Instance workspace: `C:\Users\Yukis\.jiuwenswarm-instances\career_emu`.
- Selected file: `C:\Users\Yukis\.jiuwenswarm-instances\career_emu\config\config.yaml`.
- The Runner defaults to the `career_emu` workspace; the instance registry maps that name to the same workspace. The startup path can set `JIUWENSWARM_DATA_DIR` for named-instance selection. JiuwenSwarm's config loader reads `<selected workspace>\config\config.yaml`.
- Model selection uses the nonempty `models.defaults` list before the legacy `models.default` and environment fallback. The selected list contains one default model entry. Safe metadata observed: alias `deepseek-flash`, endpoint host `api.deepseek.com`, and a `model_client_config` object.
- Before this change, `models.defaults[0].model_client_config.max_retries` was absent. No full provider config or `.env` content was emitted.

## 5. Effective Historical Setting

The selected local file had no explicit `max_retries` before the edit. The installed `ModelClientConfig` schema supplies `1` when the field is absent. This establishes the schema fallback, not the value used by the historical S07-51R process: S08-02 did not inspect that run's effective local override, so the historical effective value remains `UNKNOWN`.

The effective timeout and whether the optional outer `LLMRetryRail` was enabled for that historical run also remain `UNKNOWN`.

## 6. Retry Semantics

`ModelClientConfig.max_retries` is an integer for thin SDK retries on transient connection failures and selected HTTP failures such as 429 and 5xx. In OpenAI SDK `2.41.0`, `max_retries` counts additional attempts after the initial attempt: `N=2` permits up to three SDK attempts for one call. A raw `httpx.ConnectError` follows the retryable transport-exception path; after retries are exhausted, the SDK surfaces the connection failure as `APIConnectionError`. The SDK-level default is `2`, but OpenJiuwen passes the configured value explicitly, so the model config controls this client.

## 7. Selected Value

Selected `max_retries = 2`. The value adds one retry opportunity beyond the schema fallback of `1`, while capping one SDK call at three total attempts. Selecting `3` would allow four total attempts and another potentially long request interval. The no-header backoff comparison is recorded in Section 10. This is a bounded risk choice, not evidence that two retries will recover every transient failure or improve a game outcome.

## 8. Implementation

- Exact key: `models.defaults[0].model_client_config.max_retries`.
- Exact change: inserted the integer line `max_retries: 2` under the selected model's `model_client_config`.
- The edit was an exact single-line insertion; all other config bytes were preserved.
- Pre-edit source backup: `D:\CS\CareerSim\.local\runtime\s08-03\config.yaml.before` (ignored local runtime evidence).
- Backup bytes were compared with the pre-edit file. The config file and backup are not in Git.
- No helper or repository code was added. Endpoint, model alias, credentials, proxy settings, Candidate, four Skills, runtime manifest, Runner, dependencies, and `uv.lock` were not changed.

## 9. Static Propagation Verification

Verified propagation path:

1. Selected local `config.yaml` parses to integer `2` at `models.defaults[0].model_client_config.max_retries`.
2. `jiuwenswarm/server/runtime/agent_adapter/interface_deep.py`, `_build_model_from_entry`, passes `mcc_fields` into `ModelClientConfig`.
3. `openjiuwen/core/foundation/llm/schema/config.py` defines `ModelClientConfig.max_retries` with schema default `1`.
4. `openjiuwen/core/foundation/llm/model_clients/openai_model_client.py`, `_build_async_openai_client`, passes `self.model_client_config.max_retries` as `AsyncOpenAI(max_retries=...)`.

Offline dynamic verification parsed the selected config, instantiated a pure `ModelClientConfig` with the same retry integer, and ran the client-construction method with in-process fake HTTP and `AsyncOpenAI` constructors. The fake constructor captured `max_retries=2`. Dummy API fields were used only to satisfy schema validation; no real credential was loaded into the object or emitted. Static AST checks verified the adapter mapping and confirmed each of `invoke` and `stream` contains one SDK `create` call with no enclosing outer retry loop. No provider call or network request was made.

## 10. Backoff / Timeout Risk

For connection failures with no HTTP response header, SDK backoff uses a `0.5s` exponential base, capped at `8s`, with a jitter multiplier from `0.75` to `1.0`. For `N=2`, the two retry sleeps total approximately `1.125–1.5s`; for `N=3`, the three retry sleeps total approximately `2.625–3.5s`. Thus choosing `2` avoids the third retry's additional `1.5–2s` no-header backoff. These figures exclude request time.

For eligible HTTP responses the SDK may honor `Retry-After` (up to its 60-second acceptance window); a raw connection error has no response header. The schema timeout default is `360s`, so retry attempts can add substantial waiting. The actual local timeout was not inspected under the safe-output boundary and remains `UNKNOWN`; no strict end-to-end wall-clock bound is claimed. A timeout retry from the separate `LLMRetryRail` is a different path: source inspection limits that rail to repeated-output and stream-timeout markers, not `APIConnectionError`. Its effective enabled state is unknown, but it does not add another retry for this connection-error family.

## 11. Rollback

The byte-for-byte pre-edit file is recoverable from the ignored backup. If rollback is needed, first confirm the shared `career_emu` runtime is stopped, then restore the backup:

```powershell
Copy-Item -LiteralPath 'D:\CS\CareerSim\.local\runtime\s08-03\config.yaml.before' -Destination 'C:\Users\Yukis\.jiuwenswarm-instances\career_emu\config\config.yaml' -Force
```

After restoration, compare the config bytes with the backup. The restore operation was not applied to the active target because it would undo the selected setting; pre-edit byte preservation and the backup were verified offline.

## 12. Local vs Submission Portability

This is a supported local named-instance config carrier and the selected file now contains the requested retry value. Whether a competition submission package, a fresh machine, or a later instance recreation selects and preserves this local override is not established. Submission portability and cloud behavior remain `UNKNOWN`; there is not enough evidence to label the setting definitively nonportable.

## 13. FACT / INFERENCE / HYPOTHESIS / UNKNOWN

- **FACT:** the selected local config parses to `max_retries=2`; the installed schema default is `1`; source passes the field to `AsyncOpenAI`; fake-constructor capture received `2`.
- **FACT:** S08-02 observed seven provider-error zero-work terminations and 14 productive boundaries in one run; no new live operation occurred here.
- **INFERENCE:** increasing the SDK retry count may recover some transient connection drops before they terminate a request. The amount of recoverable work is not measured.
- **HYPOTHESIS:** `max_retries=2` may reduce zero-work provider terminations while adding bounded attempts. S08-04 must evaluate this separately from execution-persistence behavior.
- **UNKNOWN:** S07-51R's effective historical retry value, actual local timeout, historical retry-rail enabled state, underlying provider/network cause, submission/cloud portability, and any behavioral or score effect.

## 14. Decision

`LOCAL_RETRY_STATIC_READY` — a safe supported local carrier exists; only the retry integer changed; value `2` is within the Plan's `{2,3}` boundary; source/static and offline constructor propagation passed; rollback is available; no frozen component was patched; and no live operation occurred.

## 15. Next Step

`PROCEED_TO_S08_04_EXECUTION_PERSISTENCE`. Keep the 14 normal productive boundaries and their 23 actions / 23 observes as the separate persistence target. Do not attribute those boundaries to provider errors or treat this retry configuration as proof of a strategy effect. `NEXT_GAME` remains `NOT_AUTHORIZED`; a game or provider run requires a separate authorization.

## 16. Limitations

- The runtime was not restarted or exercised after the local edit, so runtime behavior is not validated.
- No provider, service, MCP, game, or database action occurred.
- The provider's root network cause, actual effective timeout, retry-rail enabled state, historical config value, and submission/cloud portability remain unknown.
- This change does not alter or validate Candidate strategy, execution persistence, score, or gameplay.
- No repository code/helper was added; verification was limited to safe config parsing, pure model construction, fake-constructor capture, source/AST checks, and Git hygiene.
