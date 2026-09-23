# S04-01｜结构化记忆接入面取证与最小合同

## Scope and identity

- **FACT:** Base `origin/main@eeb635230e0e33a915cb439988f421b5516a61ef` (fetched 2026-09-23); frozen Runner source identity `f61c738c72e51b77298cc1c14c7c6ebf4b6c527d`; installed `jiuwenswarm 0.2.4b3`, `career-emulator 1.0.1`, `openjiuwen 0.1.16.post2` (repo `docs/project/ENVIRONMENT.md` and installed dist-info). This task read source and existing evidence only.
- **FACT:** `docs/project/CURRENT_STATE.md` records S03 accepted, `MEMORY: NOT_IMPLEMENTED`, and Risk benefit `NOT_PROVEN`. `docs/project/ARCHITECTURE_DECISIONS.md` AD-001/002/005 specifies Single Agent + Multiple Skills, structured state, bounded history, and a non-submitting candidate `structured-state-board`.
- **FACT:** The two canonical Skills are instruction files. `skills/career-action-trace/SKILL.md` keeps the normal loop's single submitter; `skills/risk-review/SKILL.md` explicitly forbids its own `observe`, `take_action`, and `new_game`. S02-01 and S03-14 results prove install/discover/load and one observed Risk application path, not a Memory path.

## Evidence map

| Source | Relevant fact |
| --- | --- |
| `career_sim_runner/headless_play.py:32-48,70-78,95-154` and `ws_client.py:84-98,149-163,221-309` | Fresh play generates a **drive/conversation** ID; `--continue` reuses the saved one. WebSocket `chat.send` carries that ID. The Runner extracts a separate **game** ID from `new_game`/`observe` results and writes both to the score report. |
| `career_sim_runner/prompts/play_headless.md`, `play_headless_continue.md`, `identity.md` | Normal path: `new_game` once, then `observe → decision → take_action`; continuation instructs re-observe and bounded `check_latest_logs`, without another `new_game`. |
| `career_sim_runner/install.py:43-58,96-133`, `paths.py:90-130`, `constants.py:29-40` | Install deletes `todo/*`, `.agent_history/*`, `agent/sessions/*`, `.agent_teams/*`, `workspace/memory/*.md`; rewrites `MEMORY.md`; resets installed Skill directory and registry. Globs do not prove cleanup of every other file type or directory. |
| `career_sim_runner/skill_contract.py:125-147`, `install.py:129-154`; installed `openjiuwen/harness/rails/skills/skill_use_rail.py:151-200,477-501`; `openjiuwen/harness/tools/skills/skill_tool.py:350-400` | Submission bundles carry `skills/<name>/SKILL.md`; install copies them; Skill runtime discovers these files and `skill_tool` reads the selected file. A Skill file is an instruction/distribution surface, not a per-game state store. |
| Installed `jiuwenswarm/server/runtime/session/session_history.py:114-197,256-282`; `jiuwenswarm/common/utils.py:1604-1605` | Conversation history is stored under `agent/sessions/<drive ID>/history.jsonl` (or legacy JSON), keyed by the JiuwenSwarm session ID. |
| Installed `jiuwenswarm/common/utils.py:1452-1473`; `jiuwenswarm/server/runtime/agent_adapter/interface_deep.py:6249-6272` | In the no-project path the adapter selects `agent/workspace/projects/<drive ID>` as task workspace. The Runner's install cleanup does not name `projects/`. Access/permissions on the exact CareerSim play path were not runtime tested here. |
| Installed `jiuwenswarm/agents/harness/common/tools/memory_tools.py:61-84,291-350,452-520`; `jiuwenswarm/agents/harness/common/memory/config.py:234-260`; `interface_deep.py:10267-10318` | This JiuwenSwarm memory-tool implementation restricts paths to shared `memory/MEMORY.md`, `memory/USER.md`, or dated Markdown, not arbitrary per-game JSON. Agent-mode MemoryRail defaults disabled unless configured. The exact memory tool registration in the CareerSim play path was not demonstrated. |
| Installed `career_emulator/game.py:133-196,199-212,718-725`; `career_emulator/storage.py:217-266,293-302` | `new_game` creates a unique game session; `observe` reads it by ID and returns visible state/choices; game state and logs persist under that ID in emulator storage. The emulator DB is authoritative game state, not a participant board write API. |
| `experiments/S02-01-minimal-skill/RESULT.md:33-65`, `experiments/S03-14-risk-correctness-live-smoke/RESULT.md:31-40`, `experiments/S03-07-risk-recovery-smoke/RESULT.md:23-25` | Prior real paths establish Skill loading, separate drive/game IDs, single successful submitter, and observed install cleanup of old sessions/`MEMORY.md`. |

## State surface matrix

`SUPPORTED` means the stated *limited use* is backed by source or earlier execution. It does not imply a new S04 runtime smoke passed.

| State surface | Lifetime | Read / write actor | Reset / cleanup | Submission portable | Main risk | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| Current `observe(game_session_id)` plus `check_latest_logs(game_session_id, N)` | Current emulator game while retained | Same Agent reads public MCP results; emulator owns writes | New game gets a new ID; DB retention can evict old sessions; Runner install does not itself delete emulator DB (`game.py:133-196`; `storage.py:235-266`) | Yes: existing MCP contract, no local file | Latest logs are bounded; older facts may be unavailable; `observe` is the source for present state | **SUPPORTED** as authoritative read/recovery surface |
| Same JiuwenSwarm drive conversation and `agent/sessions/<drive ID>/history.jsonl` | Same drive ID, including `--continue` while history exists | Agent emits compact board in conversation; framework persists history | Runner install removes `agent/sessions/*`; a fresh play uses a new drive ID (`headless_play.py:70-106`; `install.py:43-55`) | Yes for Skill instructions, no for local history bytes | Compression/truncation and install may lose board; history is not a deterministic keyed board API | **SUPPORTED** as bounded working context, **UNSUPPORTED** as sole durable truth |
| `agent/workspace/projects/<drive ID>` task workspace file | Drive ID scope by path, if no project override | Framework file tools may read/write; exact play-path exposure not observed | Not in Runner's install deletion list; no explicit new-game cleanup seen (`utils.py:1452-1473`; `install.py:43-58`) | Instructions can ship; runtime file cannot | Drive ID differs from game ID; stale files may survive install and session reuse; permissions and cloud portability unknown | **UNKNOWN** for S04 board until bounded smoke |
| Shared `agent/workspace/memory/MEMORY.md` and built-in memory tools | Instance-wide, not game-scoped | Config-dependent Agent memory tools | Install deletes `memory/*.md` and rewrites `MEMORY.md` (`install.py:48-56`); no automatic new-game clear | Instructions can ship; content cannot | Cross-game contamination; no arbitrary per-game JSON path; auto memory/embedding behavior may add cost | **UNSUPPORTED** as default session board |
| Installed `skills/<name>/SKILL.md` and `skills_state.json` | Installation/config lifetime | Runner writes; Agent `skill_tool` reads instructions | Replaced/reset on each install (`install.py:58-133`) | **Yes** for versioned Skill contract | Treating Skill text or registry as mutable run state mixes code and observations | **SUPPORTED** for contract delivery, **UNSUPPORTED** for board data |
| Runner event/transcript/output files and emulator SQLite | Run artifacts / emulator retention | Runner or emulator writes; Agent uses MCP public reads | Output files not named in install cleanup; emulator can evict old sessions (`ws_client.py:294-314`; `storage.py:235-266`) | No local artifacts in submission | Raw artifacts/DB expose more than current legal observation; no participant mutation API | **UNSUPPORTED** as Agent board store; diagnostic evidence only |
| JiuwenSwarm `runtime_state/<drive ID>.yaml` | Framework session metadata | Framework writes mode/channel/project fields (`common/utils.py:1408-1415`; `interface_deep.py:6316-6325`) | Not in Runner's install cleanup list | No | Framework-owned schema, not public CareerSim observations | **UNSUPPORTED** as board data |

## Minimal Memory contract — recommendation, not implementation

**Decision / INFERENCE:** S04-02 should start with a **Skill-only, same-Agent structured working board** in the current drive conversation. It should use public `observe` and bounded logs for recovery, not assume built-in MemoryRail or a writable local file. This uses the already verified Skill loading route and the Runner's normal decision loop. It is deliberately limited to correctness of state classification and session isolation; it claims no score benefit.

| Field | Minimal contract |
| --- | --- |
| Trigger | After successful `new_game` and first `observe`; after a new `observe`/action result changes relevant public state; after continuation/context loss. |
| Input | Current **game** session ID from `new_game`/`observe`, current public `observe` (`current_state`, event, legal choices, warning), and, only when needed, bounded `check_latest_logs` for that game ID. The drive ID is conversation routing, not a substitute for game ID. |
| Output | Compact board with `game_session_id`, observed month/phase, `observed` entries with source/time, separate `inferred` entries with rationale, and explicit `unknown` entries; use only fields needed for the next decision. Never claim hidden thresholds or outcomes. |
| State Read | Same-drive latest board if its game ID matches, then refresh against current `observe`; on mismatch/missing/stale data discard board and re-observe. |
| State Write | Same Agent updates one bounded board in its conversation after public evidence. Do not write `MEMORY.md`, installed Skill files, Runner artifacts, emulator DB, or another session. No parallel writer. |
| Session identity | Authoritative key is emulator **game** session ID; drive ID only locates the current conversation. A new `new_game` response invalidates any previous game board, even if the drive conversation remains. |
| Failure fallback | Return `UNKNOWN` for unsupported/missing claims, call `observe` for fresh visible state, optionally bounded latest logs; if game ID cannot be confirmed, do not carry board forward. Same Agent chooses the next legal action under the existing loop. |
| Can Submit Action | **No.** The Skill produces a board only. The Single Agent remains the only `take_action` submitter. |
| Persistence boundary | Best-effort same-drive conversation history until install/session loss; no cross-game inheritance and no local-file durability claim. Versioned `SKILL.md` is portable, live board content is not. |

## Next implementation boundary (S04-02)

1. Add only `skills/structured-state-board/SKILL.md` with the contract above; package it beside the two existing canonical Skills. Keep existing Runner, JiuwenSwarm config, and Skills unchanged.
2. In a **separately authorized** bounded smoke, verify install/discover/load, one game-ID-keyed observed/inferred/unknown update, a post-action refresh, wrong/new game-ID rejection, recovery after context loss, and exactly one Single Agent action submitter. Capture actual tool calls and public observations. If a durable file is later needed, first test `projects/<drive ID>` access, cleanup, and submission replay in that smoke before adopting it.
3. Do not add database/vector store, built-in auto memory, cross-game learning, Planner/Swarm, Runner hooks, hidden-state reads, or score-benefit claims. A score comparison is a later experiment.

## Unknowns and smallest future checks

- **UNKNOWN:** Whether `read_file`/`write_file` is exposed and permitted for `projects/<drive ID>` during the actual CareerSim agent-mode play; source proves a path fallback, not a successful call. A single bounded read/write/read-back plus fresh-game and reinstall check would answer this if file persistence becomes necessary.
- **UNKNOWN:** Whether the same-drive board survives the exact context-compression point in gameplay. In the S04-02 smoke, force or observe a bounded continuation and verify game-ID check plus re-observe; do not infer durable memory from a successful initial Skill load.
- **UNKNOWN:** Exact cloud submission filesystem persistence, runtime permission policy, and cleanup outside the local frozen Runner. Keep file portability unclaimed until that environment is observable.
- **UNKNOWN:** Memory strategy/score benefit. S03-14 was one correctness path without final score; S04-01 executed no game or comparison.

## Verification boundary

- Static source and existing evidence only. No service, provider, install/reload, game, or participant action was invoked in S04-01.
- This report is engineering forensics and a next-step contract, not a Memory implementation or runtime proof.
