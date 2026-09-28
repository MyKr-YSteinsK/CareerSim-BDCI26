# S07-42 — Recovery Enforcement Feasibility

## Question and verdict

Can the current CareerSim competition submission deterministically detect `CurrentRoundCompressor` and prevent `take_action` until same-session observe, four Skill rereads, and state reconstruction finish?

**Final classification: B — `FRAMEWORK_HOOK_EXISTS_BUT_NON_DEPLOYABLE`.** The installed framework emits a structured compression-state callback/stream event. A host-side state machine could use it and a pre-tool gate, but the frozen `solution/` submission provides no evidenced way to register that callback or gate. The deployable path remains model instruction plus independent observation; it is **not deterministic enforcement**. No Candidate, Runner, dependency, service, or shared DB was changed or invoked.

## Frozen identities and evidence inspected

| Source | Identity / relevant evidence |
|---|---|
| Repository | `main@97da9104c19c87bb174fafb53f68c73ce1bbc9e5`; current Candidate `candidate-v7j-decision-closure-hardening`. `AGENTS.md`, `LIVE_RUN_WORKFLOW.md`, `OFFICIAL_SOURCE_LOCK.md`, current manifest/four Skills, `scripts/post_run_audit.py`; no diff in Runner/Candidate/Skills at investigation start. |
| Installed packages | `.venv/Lib/site-packages/jiuwenswarm-0.2.4b3.dist-info/METADATA` says `0.2.4b3`; `openjiuwen-0.1.16.post2.dist-info/METADATA` says `0.1.16.post2`; `uv.lock` pins JiuwenSwarm `0.2.4b3`. Package source was read only. |
| Frozen Runner boundary | `career_sim_runner/skill_contract.py`, `install.py`, `headless_play.py`, `ws_client.py`, `transcript.py`, and prompt templates. Source Lock identifies upstream Runner SHA `f61c738c72e51b77298cc1c14c7c6ebf4b6c527d`. |
| S07-40 raw, bounded | Existing local `evidence-manifest.json`; only the two known compressor windows in cumulative `llm.log` and corresponding events were read. Raw files were not copied or committed. Manifest identifies `llm.log` SHA-256 `c029eb87d0995b0981b7377e50a0afda2320b466ef3800a856a2ad462f48de85` and events SHA-256 `a1c3bae1b775de9771a1e7ba3bfea4383f684f743b22ecfddd621c4b0399010c`. S07-40 Main Raw Re-Audit, recorded in `runs/v7i-run1-replacement-validation.md`, establishes exactly two current-run compressions. |

The local trace emitted only timestamps, tool names and counts, never model messages, Skill contents, hidden fields, or credentials. One cumulative-log text search initially matched an oversized line; subsequent reads were bounded and content-free. A missing marker in those bounded log windows is **not** proof that the model input lacked it.

## Compressor lifecycle trace

1. JiuwenSwarm agent mode builds a `ContextProcessorRail` with `CurrentRoundCompressor` in `server/runtime/agent_adapter/interface_deep.py:786-840,5859-5873`; the rail installs processor configs in `openjiuwen/harness/rails/context_engineer/context_processor_rail.py:266-324`. The processor is part of host runtime configuration, not the submitted Skill bundle.
2. During the same pending model call, `react_agent.py:854-890` runs `BEFORE_MODEL_CALL` rails, builds the final system prompt, then calls `get_context_window`. `context.py:394-477` checks each processor's trigger, emits `started`, runs `on_get_context_window`, then emits `completed` or `noop`. `base.py:156-235` triggers on token ratio and a compressible span; the forked current-round defaults are `trigger_context_ratio=0.8`, `min_target_context_ratio=0.1`, `keep_recent_messages=0` (`current_round_compressor.py:23-27`). These are package process settings, not simulator thresholds.
3. `current_round_compressor.py:52-68` preserves through the last real user message, compresses the eligible suffix, and protects the recent tail. `base.py:237-320,598-618,668-681` calls the compression model, wraps its summary in a `<memory_block_current>` user message, optionally reinjects plan/task/skills/read-file state, replaces context messages, and returns a `ContextEvent`. Reinjected **state text is not a new Skill tool read**. The compressor's `save_state()` returns `{}` (`base.py:785-789`); no dedicated `RECOVERY_PENDING` action gate is stored there.
4. `context.py:458-477` emits a structured completed state. `processor_state_recorder.py:84-142` records it, invokes `ContextEvents.CONTEXT_COMPRESSION_STATE`, and tries to write `context.compression_state` to the session stream. The same `get_context_window` result is then supplied to the pending model call (`react_agent.py:881-908`). There is no intervening mandatory Skill-reread phase in this path.
5. `career_sim_runner/install.py:136-157` writes the submitted manifest instruction into `IDENTITY.md`; `ContextAssembleRail.before_model_call` (`context_assemble_rail.py:85-145`) rebuilds context/system sections each call. This can keep the recovery *instruction* available independently of compressed dialogue, subject to the normal host-loading path. It does not ensure that the model obeys it.

### Agent-visible signal

**PARTIAL.** A successful compression constructs an explicit `<memory_block_current>` wrapper in the next model context, and the host emits a machine-readable `context.compression_state`. The latter is a runtime callback/stream event, not a structured recovery flag available to the submitted Planning/Risk Skills. The summary body is model-generated; it may say “Skills read” without any post-compression tool call. The bounded S07-40 log windows did not independently expose the next model input's wrapper, so actual wrapper visibility in that run is `UNKNOWN`. Framework source proves the construction path, not that a recovery gate fired.

The Runner's `StreamCollector.feed_frame` (`career_sim_runner/transcript.py:111-137`) saves usage and `chat.tool_call`/`chat.tool_result`; it does **not** append `context.compression_state` to events. JiuwenSwarm can serialize that event (`interface_deep.py:10097-10108`; `stream_utils.py:112-132`), but the current events artifact cannot directly anchor compression to a structured event ID. `scripts/post_run_audit.py:120-136,346-365` therefore uses run-window `llm.log` markers and tool ordering, with the documented limitations.

### Bounded S07-40 confirmation

| Compression local time | First fresh observe in events (UTC) | First later action (UTC) | Skill/read-file calls in following 3 minutes |
|---|---|---|---:|
| 2026-09-28 19:37:12 +08:00 | 11:37:14.114887 call / 11:37:14.201182 result | 11:37:18.168853 call | 0 |
| 2026-09-28 19:45:43 +08:00 | 11:45:45.736347 call / 11:45:45.811953 result | 11:45:48.772804 call | 0 |

The trace's zero counts cover the relevant observe-to-first-action interval and the wider three-minute window. This corroborates the existing `RECOVERY_PATH_FAIL` conclusion; a textual `RECOVERY_READY` assertion would not repair the missing tool evidence.

## Enforcement and deployability matrix

| Candidate point | Deterministic in a modified local host? | Competition deployability | Finding |
|---|---|---|---|
| `ContextEvents.CONTEXT_COMPRESSION_STATE` callback plus per-session recovery state and pre-`take_action` tool gate | Potentially yes: completed processor event can open a gate; real observe/Skill tool results can advance it. Requires implementation and separate validation. | **NON_DEPLOYABLE_FOR_COMPETITION** | Callback is emitted in `processor_state_recorder.py:84-142`, but no submitted file is installed as a listener or pre-tool gate. Registering one requires host/Runner/framework wiring outside the frozen bundle. |
| JiuwenSwarm `UserHookRail` `PreToolUse` from host hooks config | Pre-tool blocking exists (`user_hook_rail.py:28-80`), but it has no compressor-completed state without a separate callback. The inspected rail does not implement its enum's `BeforeModelCall` event; `ContextProcessorRail.before_model_call` runs before same-call compression and is insufficient alone. | **NON_DEPLOYABLE_FOR_COMPETITION** | `hooks_config.py` is host config; `install_submission` uses submitted manifest/Skills, not a submitted hooks config. Local config or executable hooks do not travel with the allowed solution. |
| Runner intercepts `context.compression_state` WebSocket frame, then gates emulator tools | Possible local monitoring; enforcing tool calls would require an additional Runner/host intercept. | **NON_DEPLOYABLE_FOR_COMPETITION** | Frozen Runner collector currently drops the event and cannot be patched in this Task or submitted as Candidate code. |
| Manifest/Skill recovery wording and optional compact `RECOVERY_PENDING` / `RECOVERY_READY` marker | No. Model must notice the marker, call tools, and obey the rule. | Deployable as text in `manifest.json` / `SKILL.md` | **MODEL_INSTRUCTION_ONLY**. Existing wording already requires all steps and failed 2/2 times. Rephrasing alone is not an enforcement finding. |
| Additional script inside a copied Skill directory | Only if the model voluntarily calls it; it cannot register a compressor callback or intercept every action merely by being present. | File copying is possible, automatic execution is not evidenced | **Not a proven deterministic point.** No executable Skill hook was found in the frozen Runner install or submission contract. |

The official Source Lock documents `solution/manifest.json`, `README.md`, `design/`, and `skills/<skill>/SKILL.md` (`OFFICIAL_SOURCE_LOCK.md:84-101`). `career_sim_runner/skill_contract.py` validates the bundle, while `install.py:33-76,132-157` copies Skills and renders the manifest instruction. Neither loads participant hook registrations. A source-level host callback is therefore **not** a formal Candidate mechanism.

## Observability matrix for any later authorized live run

| Required fact | Direct evidence and acceptance rule | Current limitation |
|---|---|---|
| Compression occurred | Prefer a captured `context.compression_state` with `processor=CurrentRoundCompressor`, `status=completed`, session/operation ID; otherwise use bounded `llm.log` plus run window. | Current Runner events omit this event; `llm.log` is cumulative. |
| Recovery gate opened | Timestamped `RECOVERY_PENDING`/gate record linked to the completed compression ID. | Submitted text can ask the model to emit a marker but cannot prove a host gate exists. |
| Same-session fresh observe | Structured `observe` call/result after compression with matching game session ID. | Already available in events. |
| Four Skill rereads | Four distinct successful Skill/read-file tool results for the four installed SKILL.md files **after** compression and **before** next action. | Prior startup reads and summary claims do not count. The current parser recognizes `skill_tool` indicators; `read_file` and full content attestation would need separate scoped handling. |
| Board / Delivery / Review Plan rebuilt | Compact, source-bound status after the fresh observe and rereads; check public field provenance and required `UNKNOWN`s. | Internal semantic reconstruction is not proven by a self-reported `READY` string alone; absent durable evidence stays `UNKNOWN`. |
| No early action | Compare structured event sequence/time: every post-compression `take_action` must occur after observe, four reads, rebuild evidence, and `RECOVERY_READY`. | A model-only marker can be false; no current host gate blocks the action. |

The smallest **deployable observable fallback** is to retain the existing manifest/Skill instruction and, in a separately authorized future static patch, require one concise recovery marker tied to the current session and checkpoint. Validate it only in conjunction with the actual four tool results and fresh observe, using run-scoped `post_run_summary.json` plus targeted transcript review. Record `FAIL` when an action precedes those steps and `UNKNOWN` when compression anchoring or rebuild evidence is unavailable. This is detection and audit, **not enforcement**.

## Recommendation, unknowns, residual risk

- Return to Main with classification **B**. Do not patch the installed package, frozen Runner, host config, or Candidate in S07-42. A local callback/pre-tool prototype would be a separate non-deployable framework experiment with explicit authorization; it must not be promoted to the competition Candidate.
- If Main wants a deployable next step, scope a separate static model-level recovery observability patch and offline acceptance update. Decide how to record compact rebuild evidence without leaking hidden fields or creating verbose logs. Do not claim runtime improvement until a separately authorized run supplies the ordered evidence above.
- The bounded raw window does not establish the exact next-model input bytes or guarantee snapshot fidelity. Framework delivery of `context.compression_state` to this Runner's WebSocket client was read from source, not independently verified in this run. Other uninspected extension mechanisms are `UNKNOWN`, not assumed absent. These limits do not turn the evidenced callback into a deployable submission hook.
- S07 remains ACTIVE. Current Candidate stays v7j with unchanged validation flags. `NEXT_GAME = NOT_AUTHORIZED`.
