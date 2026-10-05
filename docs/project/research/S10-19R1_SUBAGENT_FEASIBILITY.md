# S10-19-R1 — Read-only Reviewer Subagent feasibility

**Decision: REVIEWER_NOT_SAFELY_DEPLOYABLE.** Phase A found no safely isolated advisory reviewer deployable through the frozen official `mode=agent` submission path. Phase B/C were not run, as required by the task's conditional gate and Stop Conditions. This is a deployment-boundary result, not evidence that independent review has no decision value.

## Authorization and identity

Direct user task S10-19-R1 supersedes the final-freeze S10-19 plan. v6d is the safe fallback, not a claimed optimum. Final freeze is paused. Team/Swarm, v6e/v6f, v12/v13/v14, a fourth exact v6d run and event-answer/hidden-threshold approaches remain closed.

Authoritative registered competition team: **FZU-Loss快点降**, recorded in [COMPETITION_IDENTITY](../COMPETITION_IDENTITY.json), sourced from task section4. This changes no Candidate, submission name or runtime manifest.

Repository base `8267d420da29888d0a05403991f8980e251aaa0c`, serial `main` workflow per AGENTS; no branch/worktree or runtime installation. Installed JiuwenSwarm **0.2.4b3**, openjiuwen **0.1.16.post2**. Installed sources match their local distribution RECORD entries. Source/tag commit equality is **UNKNOWN**: the installed wheel has no direct_url/commit metadata. Requested release tag `release_0.2.4.beta3` is not used as an attestation of source equality. Exact installed file hashes are in [evidence JSON](S10-19R1_BLINDED_REVIEW.json).

## Phase A — facts and boundary

1. **task_tool exists.** `SubagentRail.init` registers synchronous task_tool when subagents exist. The agent-mode default harness routes to `JiuWenSwarmDeepAdapter`; frozen config has `react.subagents.general_agent.enabled=true`. The invocation name is **general-purpose**, not general_agent. Actual service tool visibility is NOT_PROBED.
2. **verification factory existence is not registration.** `build_verification_agent_config` exists in openjiuwen, but the actual frozen agent adapter's configured-subagent builder registers general/research/browser plus enabled custom definitions; it does not register the builtin verification_agent. The frozen config has no enabled verification/custom reviewer entry. Browser is configured, but actual browser activation is not established here and is unnecessary for this decision.
3. **general-purpose has no reviewer-specific boundary.** The factory copies parent-supplied tool cards, MCP configurations, system prompt, skills and non-Subagent rails. The actual adapter registers MCP servers in the shared runtime after initialization. Dynamic CareerSim tool discovery/dispatch under child ownership is UNKNOWN, since no service or dispatch was attempted. The assembly does not prove exclusion of CareerSim mutation; therefore the required Main-only successful-action invariant is NOT_ESTABLISHED. We do not claim a child successfully took a game action.
4. **VerificationRail is not a sufficient permission boundary.** Its before_tool_call unconditionally allows names starting `mcp__`, including mutation-shaped sentinel names, even with a narrowed allowlist. The default allowlist permits bash and tool_search. The actual CareerSim route's single-underscore spelling is blocked by this rail's normal name allowlist; this naming difference is recorded rather than equating all MCP routes. Neither the bypass nor bash can be treated as universal read-only enforcement. No MCP tool or shell command was actually dispatched.
5. **separate conversation is not fresh isolated authority.** task_tool passes only task_description/query to a child conversation. general-purpose receives a unique child id; verification_agent uses a deterministic sticky child id. Thus repeat verification calls are not guaranteed fresh-context calls. General prompt/tool inheritance also differs from a narrowly scoped advisory reviewer.
6. **portable repair is outside the authorized loader.** Custom agents load from workspace/user `.jiuwenswarm/agents*.md` and require explicit `react.subagents.<name>.enabled=true`. Frozen CareerSim install copies Skill directories and writes IDENTITY; it does not install/register a custom subagent or a reviewer tool denylist. Shipping custom agent files inside a Skill does not itself register them. Making a tools-none reviewer via SDK factory is possible at a different construction boundary, but requires an unauthorized adapter/config/loader change. Writing config from a Skill would also violate this task's config boundary. Prompt-only “do not call take_action” does not establish mechanical exclusion.

These findings are scoped to the frozen submission path. They do not claim that all SDK subagents are inherently unsafe or that an independently authorized future loader could not isolate one.

## Deterministic checks actually run

Five targeted checks PASS: parent inheritance; VerificationRail name guards; frozen config registration branch; child session-id semantics; frozen installer portability boundary. Tests extracted the relevant installed AST functions and used inert sentinel objects/stubbed construction helpers. They performed **no framework bootstrap, tool invocation, service, Provider, game or DB access**. This covers semantic assembly/guard behavior, not an actual LLM-visible registry trace. One local test fixture omitted `_PATH_TOOL_ARG`; it was corrected and the checks passed. That tooling error consumed no live budget.

Installed source witnesses (relative to site-packages; exact hashes in JSON):

| Source | Lines | Evidence |
|---|---|---|
| jiuwenswarm/server/runtime/agent_adapter/agent_adapters.py |97–153|agent→DeepAdapter|
| jiuwenswarm/server/runtime/agent_adapter/interface_deep.py |2205–2295; 5338–5409|configured agents; tools/rails passed; shared MCP registration|
| openjiuwen/harness/factory.py |95–135|general inheritance|
| openjiuwen/harness/rails/subagent/verification_rail.py |33–47; 178–185|bash/tool_search and mcp__ bypass|
| openjiuwen/harness/subagents/verification_agent.py |274–315|factory/default rails|
| openjiuwen/harness/tools/subagent/task_tool.py |82–88; 177–188|child context/sticky id|
| jiuwenswarm/server/runtime/agent_adapter/interface_deep.py |11459–11500|custom enabled config requirement|
| frozen career_sim_runner/install.py |30–85; 136–159|Skill-only copy/identity path|

## Phase B/C — not exercised

Provider parent requests **0**, reviewer invocations **0**, service lifecycle **0**, CareerSim new_game/take_action/DB mutation **0/0/0**. Latency/tokens/invocation-success rate/overhead **NOT_MEASURED**, not reported as an observed zero-cost or zero-latency reviewer.

Blinded cases completed **0**. Planned families remain Run02 M3/M15/M21/M27/M39; Run03 first-quarter/M6 aftermath/M9-M12; at least3 Run01 controls. No historical snapshots were disclosed to a reviewer, and no recommendation or unblinded judgement exists. CLEAR_IMPROVEMENT_SIGNAL / PLAUSIBLE_ALTERNATIVE / SAME_OR_EQUIVALENT / NEW_POLICY_VIOLATION / UNKNOWN counts are **NOT_MEASURED**, not fabricated as12 unknowns. The minimum12 requirement is conditional on a working safe runtime reviewer; its prerequisite failed.

## Memory secondary note

Frozen modes.agent.memory.enabled=true. Installed MemoryRail refreshes the memory prompt section and daily content before model calls. Workspace declares MEMORY.md and ContextAssembleRail builds context-file sections before each model call. Exact actual model-input persistence across compression is **UNKNOWN in this task**. Memory writes remain Agent/tool/manager-dependent; frozen install clears memory .md and rewrites MEMORY.md. No memory content was read as strategy evidence, written, or added to a Candidate. A single-run public-state ledger is only a separately reviewable feasibility direction, not an implemented challenger.

## Gate decision and preservation

**REVIEWER_NOT_SAFELY_DEPLOYABLE**. Task sections5/21 stop the unsafe reviewer path before Phase B. No v15 design/implementation or gameplay gate is justified by this evidence. Return to Main for a separately scoped **Memory challenger feasibility review**, as the Plan's C outcome recommends.

v6d/v8a runtime files, Candidate metadata, Skills, Runner, dependencies and Provider config remain unchanged. Existing raw FORENSIC_HOLD sources remain untouched. No hidden simulator state, scoring formula, event-answer mapping or Test data was read. No live benefit or75+ improvement is claimed.

`RETURN_FOR_75PLUS_BREAKTHROUGH_GATE`

`NEXT_GAME=NOT_AUTHORIZED`
