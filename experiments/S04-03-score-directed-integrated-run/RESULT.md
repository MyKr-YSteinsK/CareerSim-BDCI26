# S04-03｜高收益策略升级与单局联合验证

## TASK_RESULT

- **Status:** `COMPLETE`
- **Decision Classification:** `PROMISING_CONTINUE`
- **Branch:** `codex/s04-03-score-directed-integrated-run`
- **Parent SHA:** `831617e01f34c90e84027ee6e3878d059de97817`
- **Fetched origin/main:** `eeb635230e0e33a915cb439988f421b5516a61ef` (already an ancestor of the parent)
- **Commit / Remote State:** commit and push are reported in the final task handoff; this file intentionally does not embed its own commit SHA.
- **Working Tree:** expected clean after commit/push; no merge to `main`.

## Hypothesis and implementation

Primary hypothesis was H1, a bounded `rolling-planning` Skill. H2 (Risk rebalancing) was rejected and no coupled State Board change was made. The added Skill was runtime-loaded and produced three planning checkpoints: initial Month 1; Q2 through the Month 6 review; and Q3 through the Month 12 review. At the latter two checkpoints it surfaced the visible Network/Output/Health trade-offs, and the selected quarterly resource actions aligned with those recommendations. The Agent still selected `申请关键项目` in all 16 quarterly main-action decisions; the new Skill did not establish that it changed that repeated main-action pattern.

The only code-like change is the new, bounded [rolling-planning Skill](../../skills/rolling-planning/SKILL.md). It cannot submit actions and uses only same-session public evidence. Existing Skills, Runner, lock, runtime configuration, and dependencies were not changed.

## SCORE-01 forensics and strategy choice

SCORE-01 ended at month 24 with grade `D`, score `33.06`, Level `L2`, Skill `9`, Network `2`, and Output `3` at its last public month-23 observation. Its seven quarterly main actions were all `申请关键项目`. The exact firing sequence remains `UNKNOWN`; the score report has no termination reason. `risk_control` raw `0` normalizes to `100` in both score reports and is not evidence of Risk Skill effectiveness.

The experiment is directional only. One run per condition cannot establish that rolling planning caused the score difference or generalizes.

## Live run and MCP registration

- Service lifecycle: `career_emu` was stopped before start, started once at `2026-09-23T16:01:41Z`, reached running state, then stopped once at `2026-09-23T16:31:40Z`; final state is stopped and target ports are clear.
- Runtime registration: PASS in JiuwenSwarm logs. The five required CareerSim tools were exposed; no new `WinError 2` was observed.
- Runner play: exactly one invocation, exit code `0`, `--timeout-s 7200`, no `--continue`; run wall-clock `23m 18.370s`.
- Exactly one `new_game` created game session `2224f5df228544e699b10f897d333d4b` in drive `career-sim-runner-fbf3d7fa1cd4`. All runtime session-ID arguments matched this new ID; no old session was resumed.
- Tool calls: `observe=198`, `take_action=206` (all 206 succeeded), `check_latest_logs=2`, `show_employee_handbook=1`. One Agent drive was the only action submitter; no second Agent, Team, or Swarm was created.

### Structured State Board

The Skill was loaded. One initial board-like output contains `observed / inferred / unknown`, but no explicit `game_session_id` or `source_or_freshness` field was found, and no after-action fresh-observe board refresh was proven. Record `STATE_BOARD_USE_NOT_PROVEN` for full session-bound use/refresh acceptance. The run was not repeated.

## Result and comparison

| Measure | SCORE-01 | S04-03 |
|---|---:|---:|
| Grade / completion | D / eliminated | A / completed |
| Survival | 24 months | 48 months |
| Quantitative score | 33.06 | 76.04 (`+42.98`) |
| Competition partial | 23.14 | 53.23 (`+30.09`) |

At month 6, the latest public state was `L2 / Skill 13 / Network 5 / Output 6 / Health 7` versus SCORE-01 `L1 / 9 / 3 / 3 / 6`. At month 12 it was `L3 / 24 / 7 / 7 / 7` versus `L1 / 9 / 3 / 3 / 7`. At month 24 S04-03 remained alive at `L4 / Skill 63 / Network 36 / Output 26`; SCORE-01 had no month-24 public snapshot and was eliminated in month 24 after its last public month-23 state. S04-03 completed month 48 at `L6 / Skill 139 / Network 52 / Output 42`.

All current weighted dimensions were at least as high as SCORE-01; `risk_control` was unchanged. Full per-dimension and trajectory values are in [score_comparison.json](score_comparison.json).

## Usage and cost

The one startup incidental prewarm recorded `deepseek-flash` input `200`, output `1`, total `201`, cache hit `0` / miss `200`. Gameplay usage was input `37,356,269`, output `218,127`, total `37,574,396`, cache tokens `36,953,088`, reported cache hit rate `98.9%`; by-model usage was `deepseek-flash`. Runner-reported cost was `0.0`; actual provider-billed cost is `UNAVAILABLE` and must not be read as zero. Including prewarm, total usage was `37,356,469` input / `218,128` output / `37,574,597` total. No provider calls were made outside service startup and the one game.

## What is proven / not proven

**Proven:** one clean service lifecycle; successful service-level MCP registration; one fresh 48-month game; successful action calls; three `rolling-planning` checkpoints with public-state/recommendation/action evidence; a large positive directional score signal.

**Not proven:** causal score improvement, generalization, a Risk Skill effect, structured-state-board same-session refresh after action, or actual billed cost. The main quarterly action remained `申请关键项目` throughout.

Risk boundary remains: `Risk Hypothesis = ACTIVE`; `Risk effectiveness = NOT_PROVEN`; `controlled screening = NOT_STARTED`.

## Verification

- `git diff --check`, evidence JSON parsing/hash and byte-count checks, `.env` ignore check, frozen-file comparison, and scoped diff review passed before commit.
- `uv lock --check` passed using frozen CPython `3.12.13` (`252` packages); no sync/install was run.
- Skill frontmatter/contract and JSON/static invariants passed before the live run; event evidence confirms one fresh game and `206/206` successful `take_action` results.
- Frozen Runner, `pyproject.toml`, `uv.lock`, and the three pre-existing Skills remained unchanged; no tracked environment file, credential, database, raw log, or runtime artifact is included.
- Full artifact paths, byte counts, hashes, tool counts, usage, and lifecycle evidence are in [run_evidence.json](run_evidence.json). Raw gameplay artifacts and shared logs remain local and uncommitted.

## Execution issues

- The JiuwenSwarm launcher emitted ten `UnicodeEncodeError` traceback blocks while printing startup port/readiness output; it nevertheless became ready, registered MCP tools, and produced no `WinError 2`.
- One read-only metadata command initially collided with PowerShell's case-insensitive `$HOME` variable; it failed before any state change and was rerun with a task-specific variable.
- The initial automatic-Python lock check selected CPython `3.14.6`; it was rerun explicitly with the frozen `3.12.13` interpreter and passed without synchronization.

## Next Recommended Action

`S04 Stage Review` only. Do not run another game, do not merge `main`, and do not declare S04 complete here.
