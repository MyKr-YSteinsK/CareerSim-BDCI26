# S10-19-R2 Memory Anchor feasibility

Status: **COMPLETE_AS_NEGATIVE_FEASIBILITY**. Decision: **MEMORY_NOT_DEPLOYABLE**.

IN_FLIGHT_EVIDENCE on `main`, base `511fe3a5731bda6e91dd6ac2d19159be09ccdd81`. This task evaluates the specified automatically available `memory/MEMORY.md` anchor. Builtin file storage and explicit memory reading do work in the isolated harness; that alone does not satisfy the persistence gate.

## Exact identity and scope

- Installed `jiuwenswarm==0.2.4b3`, `openjiuwen==0.1.16.post2`; fifteen relevant installed source files match their wheel RECORD hashes. Installed source Git commit remains UNKNOWN.
- Official Runner commit `f61c738c72e51b77298cc1c14c7c6ebf4b6c527d` fetched and verified. Its `career_sim_runner` tree and local HEAD tree both equal `a2245c49d0b102b80b9891b6d750c671b3c3710f`.
- Exact v6d source `e7e8ab44dd85a29135eb089ef29de8fed298f4a4` read into an isolated fixture. Manifest SHA-256 remains `4a92d56f41b63863a01793f5a38de99bd86ce3f1792542b9f92742c1d99c04b2`.
- Frozen shared config SHA-256 before/after: `5ae22dedc828177df114e500aacf280a17217b45d3d19d9df67b583b7bd08b72`. `modes.agent.memory.enabled=true`; raw embedding fields are interpolation placeholders. Exact resolver logic with frozen .env/process-env precedence resolves memory mode=`local`, engine=`builtin`, but embedding model/base-url/key are empty in this offline process. Shared service environment remains UNKNOWN; no embedding viability is inferred. Credential values are excluded from evidence.
- Registered identity remains **FZU-Loss快点降**. Canonical v8a checkout and v6d safe-fallback policy remain unchanged.
- Provider/service/shared install/game/session/DB mutation: **0**. Final retained probe: two fixture install lifecycles and one explicit fixture memory read. Across tooling iterations: four completed fixture lifecycles, two contract rejections before cleanup, three offline compression simulations. No CareerSim state, hidden counters, Test data, scoring formulas or historical event answers were read.

## Phase A: actual capability and prompt path

FACT: frozen adapter `_handle_memory_rail_by_config` uses local memory mode, builtin-engine and agent-enabled gates, then `_build_memory_rail` and agent rail registration. Offline resolved config supports those enablement gates, but embedding fields are empty; a real shared agent was not instantiated. **Shared MemoryRail mount/permissions: UNKNOWN**. This is distinguished from the tested fixture registry. The adapter logs missing embedding config but continues construction inside its try/except, so missing fields alone are not treated as proof of no rail mount.

FACT: real `MemoryRail.init` registered **memory_search, memory_get, write_memory, edit_memory, read_memory** in the real `AbilityManager`. The harness uses real Workspace/SystemPromptBuilder/rails and a fixture-only filesystem adapter. EmbeddingConfig is an inert placeholder; `before_invoke`, memory-manager initialization, indexing and embedding/search inference were never invoked. Thus registration is proven, embedding/search operability is unmeasured.

FACT: actual `ReadMemoryTool.invoke` successfully returned the latest `MEMORY.md` marker from the fixture. This is an explicit tool result, not a persistent system section. Write/edit schemas and path constraints were inspected; actual write/edit dispatch and shared-service permission enforcement were not tested. The frozen sensitive-memory guard is a content guard, not a blanket prohibition on public-state memory.

Actual Runner-resolved shared memory path:

`C:\Users\Yukis\.jiuwenswarm-instances\career_emu\agent\workspace\memory\MEMORY.md`

FACT: `ContextAssembleRail.before_model_call` obtains sections through `build_context_file_sections`, but `CONTEXT_FILES` contains only AGENT/SOUL/HEARTBEAT/USER/IDENTITY. Its system section set contains agent/soul/identity/user. A helper capable of reading MEMORY.md exists, but the assembly loop does not request it.

FACT: `MemoryRail.before_model_call` refreshes the memory **usage guidance**, then loads today's/yesterday's **daily_memory** files. It does not load MEMORY.md body. The guidance itself says historical memory is absent by default and recommends explicit read/search. The context guidance says daily memory is not automatically injected, while the MemoryRail callback does inject recent daily files: the executed callback, rather than that inconsistent prose, is the evidence.

Consequently MEMORY.md is neither startup-only nor refreshed-per-call system content in this path. Changing it does not alter the assembled system prompt. Explicit reading may bring content into the conversation, which again depends on model tool adherence and conversation retention.

## Phase B: deterministic prompt capture

The capture point is the real `SystemPromptBuilder.build()` after real MemoryRail and ContextAssembleRail callbacks. This is a minimal prompt harness, not a full provider request or service run. The filesystem adapter confines reads to the fixture; an IDENTITY marker is the positive control.

| Capture | MEMORY.md marker | IDENTITY control | System chars |
|---|---|---|---:|
| Startup, initial marker | ABSENT | PRESENT | 2,383 |
| Next call, updated marker | ABSENT | PRESENT | 2,383 |
| After simulated compression, updated marker | ABSENT | PRESENT | 2,383 |

All three system captures have SHA-256 `c5f9cbdfc9859135cc3335b810049a1cd66af5ce69e83478247d4d192fac6ab6`.

Compression simulation executes actual `CurrentRoundCompressor.on_add_messages`, eligible-boundary detection, event creation and in-place replacement. `multi_compress` is mocked to return a deterministic historical block generated with the actual wrapper; no compressor model is constructed or invoked. This tests the replacement/reassembly boundary, not real summarization fidelity. MEMORY.md was absent before compression, so this is **not** evidence that compression deleted an initially present anchor.

**MEMORY_SYSTEM_PERSISTENCE=FAIL**. A daily-memory differential marker does appear through the real MemoryRail callback, ruling out a blanket failure of memory-related prompt assembly.

## Cross-install isolation

Two executions of the **actual frozen `install_submission` function** run exclusively inside `D:\CS\CareerSim\.local\scratch\s10-19r2\fixture`. Bootstrap functions are disabled and environment/output paths redirected. Actual validation, cleanup, Skill copying, registry output and identity rendering run. Every recursive cleanup target is first checked to remain under the resolved fixture root. This is not a shared Candidate installation.

The fixture package initially lacked top-level manifest.json; contract validation rejected it **before cleanup**. The fixture was corrected using byte-identical accepted runtime_manifest.json. No shared side effect occurred.

| Scope | Observed result |
|---|---|
| MEMORY.md root file | Run A marker removed; exact default MEMORY_MD_CONTENT restored: PASS |
| Root memory `*.md` cleanup | Executed by real installer |
| Nested daily_memory file | Survives both installs |
| Retained daily marker after reinstall | Injected by MemoryRail callback |

**CROSS_RUN_CONTAMINATION=NONE for the requested MEMORY.md file; PRESENT for nested daily memory in the isolated fixture.** No existing gameplay contamination is inferred. This also prevents silently substituting the daily route as a solution: its different isolation contract needs a separately authorized change/test.

## Conditional phases and ledger

The task's sections 8/13/30 require persistence PASS before ledger design and Provider testing. That prerequisite failed. Therefore ledger schema/prototype/update schedule/projected writes, ten paired cases and sequence simulation are **NOT_RUN / NOT_DESIGNED**, rather than failed model trials. The unconditional-looking prototype item in section29 is subordinated to the explicit stop gate; no speculative schema is implemented.

Paired cases/stale cases/controls: 0. Clearly helped/plausibly helped/no difference/hurt/unknown **evaluated** cases: 0 each. There is no decision-quality result. Expected updates, successful model memory intents, forgotten writes, stale anchors, overwrite errors, hallucinated facts and fresh-observe conflict handling remain UNKNOWN. Fresh-observe precedence was not model-tested.

No separate Memory Skill, new Candidate, Board edit, manifest edit or challenger contract was created.

## Hypotheses and failure modes

| Hypothesis | Verdict | Evidence boundary |
|---|---|---|
| M1 Persistence | UNSUPPORTED | MEMORY.md body absent in three real-rail system captures |
| M2 Low-cost ledger | UNKNOWN | Conditional design phase not entered |
| M3 Stale-state reduction | UNKNOWN | No paired Provider calls |
| M4 Write adherence | UNKNOWN | No sequence simulation |

- F1 forgotten writes / F2 stale anchor / F4 hallucination / F5 fixation: UNKNOWN; no model behavior observed.
- F3 overwrite error: UNKNOWN behavior. Source `write_memory_with_context` passes `append=True` to filesystem even with its append argument false; `edit_memory` instead performs replacement. No real SysOperation write was instrumented, so no overwrite failure is claimed.
- F6 bloat: capture includes usage guidance but no anchor body; ledger cost unmeasured.
- F7 leak: root MEMORY.md isolated; nested daily marker survives/install-reinjects in fixture.

Overhead: Provider calls/input/output tokens=0; local memory tool calls=1 read, writes/edits/searches=0; model-written bytes=0. Direct fixture initial/updated marker bytes and operation time are in JSON. Successful probe operations took 0.524 seconds excluding imports; this is not a live latency estimate. Average ledger chars and actual model-write latency are unmeasured.

## Decision and retention

**MEMORY_NOT_DEPLOYABLE** for the requested reliable, automatically available MEMORY.md anchor through the frozen submission path. File storage/explicit reading capability is insufficient to pass M1. No claim that every possible memory design is impossible; no config/Runner repair or daily-memory workaround is authorized here.

All Candidate/Skill/manifest/Runner/dependency/provider files remain unchanged. Existing held gameplay evidence remains untouched. Verification uses installed RECORD checks, exact official Runner tree equality, real registry/read/capture callbacks, fixture install isolation and document/JSON checks; no live improvement is claimed.

New **FORENSIC_HOLD**: `D:\CS\CareerSim\.local\runtime\s10-19r2-memory-feasibility`, with probe source, output, raw result and three system captures. File hashes/bytes are in [compact evidence](S10-19R2_MEMORY_PAIRED_REVIEW.json). Owner S10-19-R2; Main/Stage may release after accepting this negative feasibility and resolving any further reanalysis dependency. Scratch fixture is reconstructable and is not the sole source.

Main should accept/reject the negative deployment gate before proposing another route. This task grants no Candidate or live experiment.

No score improvement proof, stable75 proof, hidden-test transfer, causal promotion claim or true runtime distribution.

`RETURN_FOR_MEMORY_BREAKTHROUGH_GATE`

`NEXT_GAME=NOT_AUTHORIZED`
