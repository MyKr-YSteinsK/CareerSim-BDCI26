# S10-19-R3 Native control surface audit

Status: **COMPLETE_FEASIBILITY_AUDIT**. Decision: **DETERMINISTIC_HELPER_CHALLENGER_SUPPORTED**.

IN_FLIGHT_EVIDENCE on `main`, base `ff393ab88b8a42121c089cd777f9f77242c1fc29`. Exact v6d remains SAFE FALLBACK, NOT FINAL OPTIMUM. No Candidate, runtime Skill, manifest, Runner, dependency or provider config was changed. Registered team remains **FZU-Loss快点降**.

## Exact evidence boundary

Installed versions verified: `jiuwenswarm0.2.4b3`, `openjiuwen0.1.16.post2`, `career-emulator1.0.1`, `career-emulator-bdci261.0.0`. Eleven relevant installed source files match wheel RECORD hashes; no installed Git commit is inferred. Frozen official Runner `f61c738c72e51b77298cc1c14c7c6ebf4b6c527d` and local Runner tree both equal `a2245c49d0b102b80b9891b6d750c671b3c3710f`.

Shared config hash remains `5ae22dedc828177df114e500aacf280a17217b45d3d19d9df67b583b7bd08b72`. Only sanitized model settings/permission enablement are retained. No shared instance was instantiated, started or modified; shared live registry is therefore unmeasured. The executable evidence is an isolated real AbilityManager, frozen rails, LOCAL SysOperation and actual tool invocations. This is stronger than documentation-only capability inference, but not cloud execution evidence.

Provider/service/shared install/new_game/take_action/session/DB mutation: **0**. No hidden state, Test data, event-answer mapping or score formula was read.

## A: Todo

FACT: agent adapter `_update_agent_rails` builds TaskPlanningRail; its builder uses the default constructor. Actual rail initialization on a DeepAgent skeleton registered `todo_create`, `todo_get`, `todo_list`, `todo_modify` in the real registry. Default `enable_progress_repeat=False`; reminder interval20 does not activate the disabled reminder. Tools operate on `workspace/todo/<session_id>/todo.json`, under a session lock. The live instance's corresponding base path is `C:\Users\Yukis\.jiuwenswarm-instances\career_emu\agent\workspace\todo`.

Real tool calls successfully created, modified, completed and deleted the fixture item within one session. An explicit load verified each changed status/content. Storage and CRUD work.

| Actual rail system capture | Todo marker | Chars |
|---|---|---:|
| Next call | ABSENT | 1,527 |
| Round2 | ABSENT | 1,527 |
| Round3 | ABSENT | 1,527 |
| Post simulated compression | ABSENT | 1,527 |

The capture point is SystemPromptBuilder after TaskPlanningRail.before_model_call. All captures SHA-256=`4846df12f88d5ba29f869d36af97c9b49a62c01d672b94b3bc6bcd2b5db7fbe0`. This callback injects task usage instructions, not the current todo contents. after_tool_call can refresh a cache; actual reminders require the disabled progress-repeat option. Compression simulation uses actual CurrentRoundCompressor.on_add_messages replacement/event code with mocked multi_compress; no model construction or inference. Full summarization fidelity is unmeasured.

Outer TaskLoopEventExecutor can use an already constructed TaskPlan's description as a later task query. That is distinct from automatically reloading current todo JSON every model call, and does not establish inside-round compression recovery. The verdict is bounded to the requested default automatic anchor, not every use of Todo.

Actual isolated install A/B recursively clears todo children: marker/session directory disappears. **CROSS_RUN_TODO_LEAK=NONE_IN_FIXTURE**. **TODO_STATE_AFTER_COMPRESSION=ABSENT** in the tested callback path; **TODO_NOT_USEFUL_AS_ANCHOR**. No Todo ledger schema designed; no portable option to turn on reminders was established.

## B: Sampling

Offline assembly uses the named-instance YAML, frozen .env then process-env precedence, actual `build_reasoning_model_request_kwargs`, and actual ModelRequestConfig defaults. No model client/request was invoked.

| Assembled field | Value |
|---|---|
| model | deepseek-flash |
| temperature | 0.95 |
| top_p | 0.1 |
| reasoning_level / reasoning_effort / thinking | Not explicitly set in this assembly |

These are effective **configuration assembly** values, not a captured live request or proof of provider interpretation. Shared-process overrides and provider-default reasoning are UNKNOWN. No causal attribution of v6d drift to temperature is made.

FACT: Runner manifest validation recognizes team/mode; install recursively copies Skills and renders instruction into IDENTITY. Arbitrary manifest fields can remain in install metadata, but ws_client's actual chat envelope passes content/query/mode/work_mode and does not propagate temperature/top_p to model construction. Adapter model selection obtains model_config_obj from platform config. The fixture's manifest includes temperature0.1; installer metadata retention does not create sampling ownership.

**TEMPERATURE_NOT_SUBMISSION_PORTABLE**. Cloud sampling ownership is not guaranteed; UNKNOWN cloud portability also triggers the task's sampling stop rule. Provider A/B calls=0. A locally edited lower temperature would not be Candidate evidence.

## C: Skill-bundled helper

FACT: frozen adapter inserts SysOperationRail by default unless an instance profile override disables it. Actual rail registry contains `bash`, Windows `powershell`, `read_file`, `write_file`, `edit_file`, `glob`, `grep`, `list_files`; code tool is not enabled by default. Frozen named config has `permissions.enabled=false`; no extra runtime permission rail is inferred. An ACP/profile override remains a portability boundary, not a change authorized here.

A temporary `probe-helper/SKILL.md + scripts/probe.py` is installed through the actual frozen install function into the fixture. Bootstrap/shared paths are disabled or redirected; actual validation, recursive copy, identity/registry output and reset execute. Every recursive cleanup target is verified inside the resolved fixture. No runtime Candidate is created.

| Required property | Observation |
|---|---|
| Script survives install | Byte-identical copy: PASS |
| Path discoverable | Actual list_files tool returns probe.py in installed scripts directory: PASS |
| Main-profile tool executes | Actual PowerShellTool→LOCAL shell→Python executes: PASS |
| Result available to parent | ToolOutput contains parsed JSON content: PASS; no LLM consumption tested |
| Install A starts empty | No controller_state.json: PASS |
| Same run next invocation | Public marker returned: PASS |
| Simulated compression | Public marker returned after conversation replacement: PASS |
| Install B resets | Skill copy/reset removes controller state; read returns empty object: PASS |
| Main-only submitter | Audited fixture script has no network/MCP/DB/provider/game calls: PASS within this source boundary |

The helper consumes ordinary string arguments, transforms them deterministically and accesses one fixed Skill-relative controller_state.json. Imports are json/sys/pathlib only. It does not access filesystem outside its fixture. Parent shell tooling has broad capability; this test does **not** establish an OS-level security sandbox for arbitrary future Python code. The future helper must keep this auditable closed source/input/path boundary.

The first absolute PowerShell `& '<python path>'` invocation was rejected by the unmodified shell allowlist before script execution. The allowed `python` prefix succeeded with process-local root .venv Scripts PATH prepended; no user/system PATH or allowlist change. The tool's actual `workdir` field was used. Local tool execution is proven; cloud interpreter availability, permissions and an actual parent LLM choosing to invoke/use the helper remain unmeasured.

**SINGLE_RUN_PERSISTENCE=PASS_IN_FIXTURE; CROSS_RUN_LEAK=NONE_IN_FIXTURE**. No automatic prompt injection is claimed. This route provides deterministic persistence/bookkeeping when invoked, and retains an LLM adherence dependency for invocation and semantic judgments.

## Novelty and ranking

49 unique Candidate identity snapshots across retained local Git refs were inspected for Skill scripts, Todo/controller identifiers and manifest sampling fields, including v4/v6/v9a/v12/v13/v14 and descendants. None contained those native surfaces. Complementary all-ref Skill path history contains no `/scripts/` path; all-ref Skill/manifest diffs contain no todo_create/todo_modify/TaskPlanningRail/controller_state/temperature identifiers. This covers early v1–v3 before current_candidate.json existed; v1 source `7a055dea76580117ca74cddb49bb04efcf605eb1` is also checked directly. Unretained runtime choices remain UNKNOWN.

- Todo: **NOVEL** within retained Candidate source; CLOSED by automatic-anchor failure.
- Sampling: no formal Candidate override found; **PARTIALLY_OVERLAPS** standalone developer evals. S07-50 used temperature0 in non-Candidate probes; S07-50R explicitly distinguished them from runtime. CLOSED by platform ownership.
- Helper: **NOVEL** within retained Candidate source. Root developer analysis/eval scripts are not Skill-bundled single-run runtime controllers. v9a's bounded opportunity probing is an already-tested semantic policy and is not this mechanism.

| Rank | Surface | Deployability | Expected leverage | Complexity | Hidden/cloud portability | Main-only compatibility | Evidence |
|---|---|---|---|---|---|---|---|
| #1 | Deterministic helper | Local frozen tool path PASS | State/response bookkeeping continuity; benefit untested | Moderate | Copy supported; interpreter/permissions not remotely tested | Audited advisory script PASS | Real copy/tool/read/reset |
| CLOSED | Todo | CRUD/reset PASS; automatic anchor FAIL | No supported automatic continuity | Low, but reminders require unsupported override | No portable reminder control established | Compatible | Actual tools + four captures |
| CLOSED | Sampling | No contestant hook | Unknown | Requires platform change | UNKNOWN, hence CLOSED | Compatible | Request-config/Runner propagation audit |

## CHALLENGER_CONTRACT_PROPOSAL

Only proposal; **do not implement or create a Candidate under this task**.

- Parent: exact v6d `e7e8ab44dd85a29135eb089ef29de8fed298f4a4`; retain its three Skills, survival boundary, public-evidence firewall and single Main submitter.
- One mechanism: advisory deterministic public-state continuity, owned by the existing Board. One helper file in that Skill; one fixed Skill-relative controller state file, rebuilt empty by install. No Todo/Memory/Team, sampling change or new Skill.
- Inputs: fresh public Month/Level/tenure, dimensions/Energy, formal feedback/warnings, explicitly attributable last action response and current objective. No historical donors, hidden risk, thresholds, event IDs/answers, raw DB, provider or game calls.
- Deterministic responsibility: validate schema, update bounded public state, invalidate old-Level response evidence on Level change, surface freshness/conflicts and current evidence. No new growth ranking policy, promotion formula, predetermined quarter recipe or semantic Story answer.
- Fresh observe is authoritative; stale/conflicting helper state must be replaced or rejected. Missing/corrupt state returns an explicit empty/invalid status, never a guessed fact. Main still chooses and submits every action and may ignore advisory output; the helper is not a hard strategy executor.
- Size budget: helper ≤200 lines / ≤8,000 Unicode chars; state ≤1,200 chars; net runtime prose ≤400 chars, replacing existing bookkeeping wording where possible. Fixed schemas only; no references/cards/workflows/markers expansion.
- Future allowed files: existing Board SKILL.md, its scripts/public_controller.py, minimal Candidate identity/manifest metadata and necessary audited packaging allowlist adjustment for that one helper. Planning/Risk strategy, Runner, dependencies, provider/retry configs, shared paths, other Skills and service code remain forbidden.
- Static gate: packaged recursive-copy identity; portable interpreter discovery under frozen allowlist; actual shell output JSON; reset/Level change/freshness/corrupt-state fixtures; fixed path and no gameplay/network/DB imports/calls; Main-only advisory boundary; no hidden/private inputs; unchanged protected hashes. No local-only absolute Python path in the package.
- Before live: separate Main approval plus no-game model/tool-intent test showing invocation/use feasibility and no fresh-state override. Cloud-equivalent execution environment must be checked; no hidden-test proof implied. Any claim requiring config/Runner change returns to Main.
- Failure modes: forgotten invocation, ignored output, wrong public inputs, stale state, malformed JSON, denied/missing interpreter and semantic misjudgment. This mechanism does not resolve stochastic exposure or unknown promotion rules.

Next recommended task: a separately scoped **static deterministic public-state helper challenger design/validation** under this contract. Do not reopen Todo, sampling or generic v6d prose patches; Late Direct-Capital Conversion is the task's fallback only if native mechanisms fail, so it is not selected now.

## Retention, operations and delivery

Final retained probe:2 fixture installs,4 successful shell calls and1 discovery call. Across tooling iterations:3 completed fixture installs,5 shell attempts (4 successful/1 denied),3 offline compression simulations. Initial DeepAgent skeleton lacked card; fixed before any todo/install/shell action. All were isolated; no shared runtime retry.

New FORENSIC_HOLD at `D:\CS\CareerSim\.local\runtime\s10-19r3-native-control`: probe/audit sources, raw output/result, prompt captures and discovery result. File hashes/bytes and eleven source RECORD hashes are in [compact evidence](S10-19R3_CONTROL_SURFACE_EVIDENCE.json). Owner S10-19-R3; Main/Stage releases after accepted deployment decision and child reanalysis dependencies end. Existing holds untouched; scratch is reconstructable.

No score improvement, stable75, hidden-test transfer, promotion formula or causal variance attribution. No gameplay or model adherence validation.

`RETURN_FOR_NATIVE_CONTROL_BREAKTHROUGH_GATE`

`NEXT_GAME=NOT_AUTHORIZED`
