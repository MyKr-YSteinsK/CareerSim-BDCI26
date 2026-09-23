# GOV-02｜执行效率与失败分类治理加固

## Identity

- Status: `COMPLETE`
- Branch: `codex/governance-execution-efficiency`
- Base SHA: `73a69668812f28076abcebd0a90e1cf71b20f64c` (`origin/main` at task start)
- Parent: `none`
- Commit: see final TASK_RESULT; this file is included in that delivery commit.
- Scope: `AGENTS.md`, `docs/project/CODEX_PLAN_CONTRACT.md`, this RESULT.

## Evidence Read

- Governance source: both files read from the task base. `AGENTS.md` already requires shared `career_emu` serialization, bounded live retries, inspection after partial/unknown outcomes, secret protection, and `FORENSIC_HOLD` preservation. The Plan Contract already defines FROZEN / RECOMMENDED / DELEGATED_TO_CODEX, evidence discipline, and TASK_RESULT execution metrics.
- S03-12: branch HEAD `26cfc03dcf1a91c598fa85db39fc503adf945642`; RESULT blob `5a5caaa6b66f71e8d265f7d6ea019edfb84f2168`; evidence JSON blob `3c201c0f8335da2cbd1d2e60210fd1787a16c129`.
- S03-13: branch HEAD `82eb85da15de0a6304a898f61ba6731dc0b93557`; RESULT blob `ccbb4660f6aa26ec12e01f76cbe0743047ba9eba`; evidence JSON blob `ec30f9990ddf36e2a164b53d064f6be7909fa187`.
- S03-12 measured at least five pre-game local/read-only corrections against a limit of two; categories included config-shape/path assumptions and PowerShell parse failures. Runner play did not start. The task separately recorded one service start/stop and two completed provider usage records (`233` input / `5` output / `238` total tokens, cache `0`, reported cost unavailable); these are live activity, not tooling errors.
- S03-13 recorded three recurrences of the same PowerShell inline-expression parse failure and stopped before service startup. A separate `uv run --no-sync --active` attempt without the project root environment created an ignored worktree `.venv`, then failed importing `ruamel` before validation. No provider, service, MCP tool, install, or gameplay operation occurred in S03-13. Provider freshness was reused from S03-12 because config identity matched.
- These are single-project lessons from the cited task evidence, not cross-project claims.

## Governance Changes

- **Failure Taxonomy** — `docs/project/CODEX_PLAN_CONTRACT.md`, “执行失败、重试与证据门禁”: defines Tooling Error, Runtime Error, Live Attempt, and Unknown Side Effect; a tooling error is excluded from live budget only when no target operation/state change or unknown side effect occurred.
- **Semantic Retry Accounting** — same section: counters bind to semantic operation/root cause, not total nonzero shell commands. Unrelated local corrections do not consume live budget; explicit live retry limits remain unchanged.
- **Hard Gate / Advisory Check** — same section: blocking gates are tied to safety, FROZEN compliance, identity, shared-state, required dependency/interface, or live correctness; advisory failures normally record an evidence limitation. No new blocking diagnostic gate after existing gates pass without new material evidence.
- **Evidence Reuse** — same section: reuse reliable PASS when relevant identity inputs remain stable; a new worktree alone does not invalidate evidence; explicit fresh-evidence requirements still govern.
- **CareerSim Root Environment** — `AGENTS.md`, “本机 Workspace”: Python static/offline checks use `D:\CS\CareerSim\.venv\Scripts\python.exe`; `uv run` requires the activated root environment plus `--no-sync --active`; bare `uv run` and implicit worktree-local environment creation/sync are prohibited. An ignored accidental environment without identity contamination is recorded as local residue, not a standalone live-run blocker.
- **Windows Command Discipline** — `AGENTS.md`, “Task 权限 / shared runtime / retry”: simple PowerShell operations remain appropriate; structured parsing/hash/aggregation should use Python or atomic commands; avoid complex inline command/status/object/control-flow expressions.
- **Preflight Discipline** — same AGENTS section: preflight blocking checks are limited to live correctness/safety and task-required dependency/interface gates; reuse stable evidence; diagnostics are not default gameplay blockers. Explicit `FORENSIC_HOLD` preservation remains mandatory.
- **EXECUTION_ISSUES feedback** — `docs/project/CODEX_PLAN_CONTRACT.md`, after TASK_RESULT execution metrics: adds the four requested fields only when avoidable execution issues occurred; excludes normal investigation and does not affect acceptance.

## Safety Preservation

No conflict with the existing safety clauses was found. The change does not authorize or repeat a live operation and does not weaken:

- shared `career_emu` serial-use and exclusivity requirements;
- Plan-defined bounded live-run retries or stop conditions;
- inspection and STOP on unknown / partial side effects;
- secret and credential protection;
- `FORENSIC_HOLD` preservation and required pre-mutation evidence capture;
- FROZEN scope or task permissions.

`CURRENT_STATE.md` was not changed because no direct material contradiction was found. No helper, framework, Skill, Runner, dependency, S01–S03 experiment evidence, or runtime artifact was created or modified; only the authorized GOV-02 RESULT was added.

## Verification

- Base and branch identity: branch created directly from fetched `origin/main` SHA above; independent task, parent `none`.
- `git diff --check`: `PASS`.
- Changed-file scope: only the two authorized governance files and the explicitly authorized GOV-02 RESULT.
- Required concept search and manual contract review: `PASS` (Tooling Error, Runtime Error, Live Attempt, Unknown Side Effect, Hard Gate, Advisory Check, semantic operation/root cause accounting, root `.venv`, bare worktree `uv run` prohibition, and EXECUTION_ISSUES are present).
- Existing safety clause review: `PASS`; exact preservation listed above.
- Root interpreter path existence: `PASS` by filesystem check; interpreter was not executed.
- Runner / lock / Skills / S03 evidence / runtime / provider configuration: unchanged by this task.
- CareerSim, provider, service, MCP, install, gameplay, and Runner play: `0` for GOV-02.
- Commit / push / remote-head equality and final clean worktree are reported in the final TASK_RESULT.

## Deviations

None. `experiments/GOV-02-execution-efficiency/RESULT.md` is the third file explicitly authorized as delivery evidence. No broader state document required updating.

## EXECUTION_METRICS｜执行指标

- Model Used: `UNKNOWN`
- Reasoning Effort: `UNKNOWN`
- Started At: `UNKNOWN`
- Finished At: `UNKNOWN`
- Actual Wall-clock: `UNKNOWN`

## EXECUTION_ISSUES｜执行问题

- Avoidable Execution Issues: `2`
- Categories: `path_assumption / patch_context`
- Consumed Live Budget: `NO`
- Prevention Candidate: Read branch-only evidence by its Git ref; inspect exact worktree anchors before applying a patch.

## Problems / Unknowns

`NONE`

## Next Recommended Action

`Governance Review`
