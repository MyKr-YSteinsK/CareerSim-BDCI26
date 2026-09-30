# HPL-02｜持久化人工沙箱与最小交互闭环

> Status: `COMPLETE` for HPL-02 offline acceptance.
>
> Decision: `HPL02_PERSISTENT_SANDBOX_READY_FOR_FIRST_HUMAN_GAME_GATE`.
>
> Boundary: `NO GAME / NO PROVIDER`; this decision does not authorize the first Human Run or complete the Human Play Lab track.

> Follow-up: HPL-RUN01 exposed a missing package-default `performance_score` route. The seven injected directories were insufficient. See [HPL-RUN01 dataset routing repair](HPL-RUN01_DATASET_ROUTING_REPAIR.md) for the complete local Dev mirror and stronger preflight. The original verification below records only the HPL-02 offline boundary.

## Identity and lineage

- Accepted parent: `HPL-01 @ a874f5471bbff4c46216f36174acb4d785c05cc4`.
- Persistent branch/worktree: `research/human-play-lab` / `D:\CS\CareerSim\.local\worktrees\human-play-lab`.
- Formal `origin/main` inspected before implementation: `d94b178e3e7867b80673c4dfecd2e70dd66272b5`. Delivery-time fetch: `5bc07edc49bb352a686d13940fb36f78d01ca827` (`record S09 v7w run1 validation evidence`).
- Between those observations, `origin/main` changed only formal S09 evidence/state: `configs/current_candidate.json`, `docs/project/CURRENT_STATE.md`, `docs/project/RUN_HISTORY.md`, and the S09 v7w run artifacts/validation. `AGENTS.md`, `CODEX_PLAN_CONTRACT.md`, `ARCHITECTURE_DECISIONS.md` including AD-HPL-001, `OFFICIAL_SOURCE_LOCK.md`, `ENVIRONMENT.md`, and `LIVE_RUN_WORKFLOW.md` showed no material HPL governance/runtime conflict. HPL therefore retains the accepted parent ancestry and is not merged or rebased onto `main`.
- Formal `CURRENT_STATE.md` was left to the Agent line. `docs/project/HPL_STATE.md` is the mutable compact HPL state source.

## Implementation and delegated decisions

| Decision | Source evidence | Implemented seam |
| --- | --- | --- |
| D1 — construct `GameEngine` with pinned data | Inspected the dedicated venv's installed `career-emulator==1.0.1`; `GameEngine.__init__` accepts `event_dir`, `fixed_event_dir`, `failure_conditions_dir`, `salary_conditions_dir`, `promotion_dir`, `talk_mechanism_dir`, and `ending_score_dir`. | Pass exactly the seven paths from HPL `career-emulator-bdci26==1.0.0/dev/dataset`; pass the run-local DB path explicitly. |
| D2 — retain official CLI | `career_emulator.cli.play()` resolves module global `get_default_engine`; it renders and accepts participant CLI input. `cli.main()` also exposes an `update` branch, which HPL does not call. | After setting DB/log environment variables, import the installed CLI, replace only `cli.get_default_engine`, and call official `cli.play()`. No MCP or custom Agent path is used. |
| D3 — block raw `logs` | 1.0.1 uses Python `input()` at its participant choice prompt and dispatches the exact `logs` command to `engine.logs_text()`. | Intercept built-in input; consume case-insensitive `logs`, show the HPL firewall message, and reprompt. Numeric choices, `handbook`, and `quit` continue to the CLI. |
| D4 — disable GitCode sharing | 1.0.1 `cli.py` imports `offer_share` from `share_run.py`; that callback can read a GitCode token and upload logs. | Replace `cli.offer_share` with a local async no-op before `cli.play()`. The wrapper neither accesses nor requires `GITCODE_ACCESS_TOKEN`. |

`hpl.ps1` is the one-command launcher. Its default invokes only `hpl_play.py` preflight. Live intent is accepted only with a non-empty Main authorization identity; authorization identity alone remains dry-run. The authorized game path was not invoked in HPL-02.

The wrapper tees participant-facing CLI output to `runs/<run-id>/transcript/terminal.txt` and parses only displayed text. The parser discards event/node identifier values while giving the accepted projector path-only unknown markers. The writer does not import emulator/storage modules or read SQLite/private simulator state. Canonical JSON/JSONL is written only after allowlist projection; raw transcript remains local and is never put in `trajectory.jsonl`.

## Dedicated sandbox facts

- HPL venv: `D:\CS\CareerSim\.local\runtime\human-play-lab\venv`; Python `3.12.13`, based on an external uv-managed Python install rather than root `.venv`.
- Direct package pins: `career-emulator==1.0.1`, `career-emulator-bdci26==1.0.0`; package roots resolve inside the HPL venv.
- Resolved closure: 13 distributions recorded in the local `sandbox/environment_manifest.json`; `uv pip check` passed. No JiuwenSwarm, FastMCP/MCP, or known LLM provider package appeared. `gitcode-api==1.3.4` is an optional upstream sharing dependency; the HPL CLI callback is disabled.
- Dataset root is the HPL venv's own installed `career_emulator_bdci26\dev\dataset`. Its seven required GameEngine directories were verified by existence/path checks only. The emulator package's default dataset identity remains `UNKNOWN`; the launcher injects the pinned HPL path explicitly.
- Every future DB/log/transcript/evidence target is constrained to `.local/runtime/human-play-lab/runs/<run-id>/`. Preflight rejects reused run roots, package/data overlap, the dedicated venv, formal Agent paths, and existing sibling runtime roots.
- `environment_manifest.json` and all sandbox runtime material are under ignored `.local/runtime`; raw artifacts are not committed.

## Offline verification

- `tests/test_hpl_01_offline.py` + `tests/test_hpl_02_sandbox.py`: **15 passed**.
- Covered no-write launcher output and absent run directories; no eager emulator import in the default path; live gate missing-authorization rejection and authorization-only dry-run; log interception with normal input forwarding; no-op share callback; exact dataset injection; transcript event/node ID and score-dimension redaction; clean allowlisted status; interpretation separation; canonical artifacts, local transcript hash, deterministic artifact hashes, and overlap rejection.
- Ruff: passed for HPL scripts and targeted tests.
- `uv pip check` in the dedicated HPL venv: all 13 packages compatible.
- `git diff --check`: passed.
- Manual `scripts/hpl.ps1` default invocation reported `GAME_STARTED=false`, showed a prospective run root, and did not create it. `-AuthorizationId MAIN-GATE-01` remained dry-run. `-Live` without an authorization ID stopped before run-root creation.
- No official CLI play/help/update command, `new_game`, `take_action`, MCP, CareerSim/JiuwenSwarm service, Provider, or dataset update/download was run.

## Isolation and boundary result

`HPL_RUNTIME_ISOLATION=STATICALLY_PROVEN_FOR_DEDICATED_SANDBOX`: the source worktree, interpreter/package closure, installed Dev dataset, and prospective mutable paths are distinct from formal Agent roots. This is a static boundary conclusion. No real session exists; therefore first-run writes, live zero-provider behavior, and actual parser coverage remain unknown. `HPL_AGENT_PARALLEL_RUN_ALLOWED` is not granted.

Boundary counts for this task: Human games `0`; `career-emulator play` `0`; `new_game` `0`; `take_action` `0`; gameplay MCP `0`; CareerSim/JiuwenSwarm service starts `0`; Provider calls `0`; dataset update/download `0`; Candidate/Skill install or reload `0`; formal Agent mutable writes `0`. Authorized writes were limited to the HPL Git worktree and ignored HPL runtime setup.

## Remaining unknowns and recommendation

- A real first-run CLI transcript has not been observed; parser behavior against actual live output is unknown beyond the inspected 1.0.1 renderer and offline fixtures.
- Provider absence and the exact write set have static source/package/path support but no real-run confirmation.
- Human strategy effectiveness and any transfer to formal Agent policy are unmeasured; HPL evidence remains a research hypothesis source only.
- Return to Main/Planner for a dedicated first Human Game gate. `HUMAN_PLAY_NEXT_GAME=NOT_AUTHORIZED`; do not infer authorization from this readiness decision.
