# CareerSim live-run workflow

> WF-01 repository contract. A live Plan must explicitly authorize each side effect. This document defines execution and evidence handling; it does not grant a game, provider call, install, or service lifecycle.

## Execution modes

| Mode | Live operator | Evidence and repository work |
|---|---|---|
| `CODEX_FULL_RUN` | Codex runs the Plan-authorized prepare, start, play, and graceful cleanup steps. | Codex extracts one offline summary, integrates the result, and performs authorized Git delivery. This mode remains available for unattended reproduction, submission readiness, and runtime validation. |
| `HUMAN_RUN_GPT_AUDIT` | The user runs the Plan's fixed live commands and preserves the artifacts. | The same offline parser produces the same summary schema. Main/GPT may review raw evidence; Codex handles scoped implementation, integration, verification, and Git. |

Future Codex-facing live Plans select exactly one mode. If no mode is selected, the Plan's explicit permissions govern; omission grants no live operation. Both modes use `scripts/post_run_audit.py` schema version 1 and the same evidence policy. The optional screening metadata field is additive and development-only. Who typed a terminal command does not change a session, score, or adherence classification.

## Progress reporting

Use the [Live Run Progress Reporting Contract](LIVE_RUN_PROGRESS_CONTRACT.md) for update cadence and ETA. It defines reporting only and grants no additional runtime operation, probe, or retry authority.

## `CODEX_FULL_RUN` phases

```text
P0 LOAD → P1 PREFLIGHT → P2 START → P3 PLAY → P4 CLEANUP → P5 EXTRACT → P6 INTEGRATE
```

| Phase | Required output and boundary |
|---|---|
| P0 LOAD | Read the current Plan, identities, permissions, stop conditions, and existing stable PASS evidence. |
| P1 PREFLIGHT | Resolve only material source/Candidate/submission identity, provider/model/config drift, shared-runtime exclusivity, required executable/interface availability, and Plan-specific hard gates. Record advisory limitations without promoting them to blockers unless they reveal material drift, contamination, FROZEN conflict, or Unknown Side Effect. |
| P2 START | Use the Plan-authorized command and readiness signal; startup may call a model. No inferred authorization from this document. |
| P3 PLAY | Execute the bounded Plan-authorized run. Once entered, do not branch into unrelated Git/history/provider/DB investigation. Preserve uncertain side effects and apply the Plan's retry ceiling. |
| P4 CLEANUP | Make the planned graceful stop using the registered absolute executable, then check service status and the known ports. Treat cleanup as bounded tail handling. If the executable or outcome remains unknown after the allowed resolution path, record the limitation and return for review; no unapproved hard kill or restart. |
| P5 EXTRACT | Run one offline structured extraction over explicit artifacts. Scope cumulative logs to this run. Missing nonessential fields become `UNKNOWN / LIMITATION`. |
| P6 INTEGRATE | Draft report/state from the summary first, complete authorized verification and Git delivery. Reopen raw only for a named unresolved acceptance question. |

A completed phase stays closed unless new material evidence invalidates it. Within one diagnostic branch, two consecutive bounded actions that add no material evidence end that branch with `UNKNOWN / LIMITATION`. A FROZEN identity/safety blocker goes to Main review. This stop rule never relaxes secret protection, `FORENSIC_HOLD`, shared-runtime serialization, Unknown Side Effect handling, or live retry limits.

## Preflight fast path

Use stable PASS results when the source, Candidate, submission, model/config, dependency, and shared-runtime identity inputs relevant to that result have not changed. Do not routinely repeat historical log audits, old raw rehashes, already-covered provider probes, generic filesystem scans, report-format checks, or unrelated Git history searches. A new material conflict can reopen the relevant gate; a desire for extra reassurance cannot.

## Runtime command registry

Resolve from the repository root; do not rely on `PATH` or run unknown `--help`/probe commands for discovery.

| Purpose | Root-relative location / operation |
|---|---|
| Project Python | `.venv\Scripts\python.exe` |
| JiuwenSwarm CLI | `.venv\Scripts\jiuwenswarm-start.exe` |
| Previously established start operation | `jiuwenswarm-start.exe --name career_emu all` (only if the live Plan authorizes start) |
| Previously successful graceful stop | `jiuwenswarm-start.exe --stop career_emu` (only within an authorized lifecycle) |
| Cleanup listeners | `19092`, `20000`, `20001`, `6173` |

The operator builds the absolute CLI/Python path from the verified repository root and invokes that file directly. If the expected CLI is missing, allow at most one bounded, read-only fallback from the known process `ExecutablePath` or a listing of relevant `.venv\Scripts` executable names. If this does not identify the established executable, stop the branch and report a limitation. No broad disk traversal, service restart, or substitute hard kill follows from a missing PATH entry.

The frozen Runner invokes `jiuwenswarm-start --list` by bare name while resolving its instance WebSocket URL. Before any authorized P2 START, launch the Runner-facing process with a **process-local child environment** whose `PATH` begins with the verified repository `.venv\Scripts`, followed by the inherited `PATH` unchanged; preserve the proxy variables. The preflight launcher itself must run with that prefixed `PATH`. In that exact environment, verify `shutil.which("jiuwenswarm-start")` resolves to the repository `.venv\Scripts\jiuwenswarm-start.exe`, then execute the bounded, read-only bare `jiuwenswarm-start --list` exactly once and require successful launch and exit 0. `which` success alone is insufficient: on Windows the process performing executable lookup must itself have the prefixed `PATH`; passing a different `env` only to a nested `subprocess.run` may not reproduce the Runner's lookup context. A helper setup failure before the CLI child is created is a tooling error to record and correct before the single actual CLI invocation; a `FileNotFoundError` or nonzero result from that invocation is a P1 failure, so do not start the service or game. Reuse the same constructed child environment for the one authorized Runner play. Never modify user/system PATH or frozen Runner source.

## One-pass offline audit

`scripts/post_run_audit.py` accepts explicit `--events`, `--transcript`, `--score-report`, `--runner-result`, and `--output` paths. Optional inputs are `--llm-log`, `--run-start`, `--run-end`, `--log-utc-offset`, `--evidence-manifest`, and `--screening-metadata`. It never locates the latest run, queries a DB, imports a provider, or starts a service.

Example shape (paths supplied by the actual run):

```text
<repo-root>\.venv\Scripts\python.exe scripts/post_run_audit.py --events <run-events.jsonl> --transcript <run-transcript.log> --score-report <score_report.json> --runner-result <runner-result.json> --llm-log <cumulative-llm.log> --log-utc-offset +08:00 --run-start <ISO-8601-with-zone> --run-end <ISO-8601-with-zone> --output <post_run_summary.json>
```

The deterministic `post_run_summary.json` has schema version 1 and top-level `inputs`, `run`, `outcome`, `trajectory`, `actions`, `adherence_evidence`, `mechanism_inputs`, `usage`, and `limitations`. It records hashes and bytes, fresh-session consistency, Runner exit, terminal public state and fresh observe score, review/level-change checkpoints, quarterly Main choices, action/CTRL counts, category-only hidden-evidence violations, run-scoped compression and Skill rereads, Delivery marker mentions, and pre-first-review public choice inputs. Marker mentions and observed level changes are evidence inputs, not automatic proof of semantic adherence or formal promotion. The mechanism trigger remains `UNKNOWN_REQUIRES_SEMANTIC_AUDIT` until a scoped reviewer decides it.

Score from a final observe is valid when that observe belongs to the single fresh session, even if `score_report.session_id` is blank; the blank field remains a defect. Missing usage is `UNKNOWN`, and reported cost 0.0 never means billed cost zero. Only allowlisted participant-visible status and scalar score fields enter the summary; numeric hidden values never enter strategy facts.

The parser uses an explicit run window when supplied. Otherwise it may derive one from a single consistent fresh event session. A cumulative `llm.log` is counted only within that window; naive timestamps require an explicit UTC offset. Unscoped compressor lines make the count `UNKNOWN`, not zero. The S07-40 historical contamination (23 cumulative records versus 2 in the run) has a synthetic regression test. Report writing reads this summary first; reopen raw only for one identified acceptance gap, and stop after the no-progress rule.

## M24 development screening (historical)

M24 adaptive screening was a development-only proposal: usefulness remained `M24_NOT_PROVEN_BUT_REASONABLE`, the protocol was `M24_GATE_NEEDS_MORE_EVIDENCE`, and it was never adopted. The frozen Runner/public interface had no proven graceful same-session M24 stop or pause seam (`SAFE_STOP_NOT_IMPLEMENTABLE_WITH_CURRENT_INTERFACE`). Competition gameplay is closed; this historical note grants no run or stop authority. The retired protocol remains recoverable from Git history.

## Development evidence archive

This private repository allows selected development evidence after bounded secret scanning. The default remains local and ignored; an archive is a copy, never a replacement for held raw. `FORENSIC_HOLD` release remains a separate Main/Stage decision.

| Level | Policy |
|---|---|
| Core run evidence | Run-scoped events, transcript, score report, Runner result, post-run summary, and generated evidence manifest may be committed after a scan. |
| Diagnostic evidence | A run-window slice of cumulative `llm.log`, and needed run-window runner/service/context-engine logs, may be committed after a scan and explicit selection. |
| Always forbidden | `.env`, API keys, Authorization/Bearer headers, cookies, credentials, private keys, secret-bearing config dumps, shared DB contents, and unrelated sessions/user data. |

`scripts/archive_run_evidence.py` requires an explicit source directory, safe run ID, and individually named `--core KIND=PATH` / `--diagnostic KIND=PATH` files. Diagnostics require a timezone-aware window; naive log timestamps need `--log-utc-offset`. It refuses multiple or conflicting session markers in raw core streams, copies selected data to `.local/scratch`, slices logs, scans every file, writes a deterministic manifest, and moves the safe result to `artifacts/dev-runs/<run-id>/`. It refuses existing destinations. The output stays ignored unless `--stage` is passed; that option force-adds only the scanned files. The scanner checks obvious credentials and refuses non-UTF-8 or files above 128 MiB. This is a bounded safeguard, not a claim that arbitrary text cannot contain an unrecognized secret or unrelated session; review unusual evidence before commit. Git stores archived evidence as bytes (`.gitattributes` disables text conversion there), so manifest hashes refer to committed content.

WF-01 does not archive the S07-40 raw run. Future Plans must explicitly authorize the run and name the evidence to retain. Core summaries from either execution mode use the same schema and archive route.
