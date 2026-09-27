# S07-28｜v7d Runtime Readiness

Status: `V7D_RUNTIME_READINESS_PASS_WITH_LIMITATION`
Candidate: `candidate-v7d-strategic-continuity`
Scope: packaging and isolated install readiness only; provider/runtime/gameplay remain unvalidated.

## Boundary recovery

- Before Main recovery authorization, a shared CareerSim DB file was read as bytes to compute SHA-256. No records were parsed, displayed, or used; the DB was not modified. Main classified this as `READ_BOUNDARY_VIOLATION / EVIDENCE_HANDLING_ERROR` and authorized completion with an absolute metadata-only DB boundary.
- The content-derived hash was removed from the ignored local baseline snapshot. Since recovery authorization, the DB has only been checked with path existence and filesystem metadata; no DB bytes were read.
- Main found no hidden DB evidence in the Candidate and no strategy contamination. The isolated install writes were confined to `.local/runtime/s07-28-readiness/`.

## Reused readiness evidence

- `scripts/package_candidate.py` deterministically copies canonical `runtime_manifest.json` bytes and the exact four current Skill files. It rejects a non-v7d identity, non-agent manifest, or a Skill set other than the current four.
- Two generated bundles had identical file sets and bytes. The Runner `validate_submission` passed for layout, manifest fields, and frontmatter; the manifest is v7d, `mode=agent`, and contains the current instruction. No retired or extra Skill was present.
- The packaging test and eight v7 contract tests passed together (9 passed). Candidate identity did not drift after that run, so these checks were reused.
- The real `install_submission` rehearsal passed in an isolated instance: four installed Skills, exact bytes, enabled `skills_state.json`, and generated `IDENTITY.md` with the current instruction and four Skill names. No reinstall was needed because installer inputs and code were unchanged.

## Shared-state check

The pre-install non-DB baseline from `.local/runtime/s07-28-readiness/shared_before.json` was reused. Post-check found the shared Skill workspace, `skills_state.json`, `IDENTITY.md`, and active-install metadata unchanged. For the configured shared DB, only path/existence/size/mtime were compared; metadata was unchanged. The configured MCP DB exists at `D:\CS\CareerSim-s03-02-risk-review\.career_sim_runner\career_emu\career_emulator.sqlite3` (278,528 bytes); the current checkout's default Runner DB path is absent. No shared write was issued by this task.

## Environment and deferred items

- Python 3.12.13, uv 0.11.16, locked packages/imports, `pip check`, Dev dataset, named instance, and config passed the prior S07-28 preflight and were reused without identity drift.
- `career-emulator-mcp.exe` and `jiuwenswarm-start.exe` are present in `D:\CS\CareerSim\.venv\Scripts`; the current shell PATH does not include that directory. S07-29 must use the project environment or activate that path explicitly. Use the configured MCP DB path for any Runner report that reads the game result.
- Credential presence is `PRESENT`; no secret was recorded. Static config is OpenAI-compatible with model `deepseek-flash` and host `api.deepseek.com`. The official [DeepSeek model documentation](https://api-docs.deepseek.com/quick_start/pricing/) lists this model alias and the OpenAI-format endpoint. No provider request was made.
- `CurrentLevelDuration` is the documented public field. Runtime alias `duration_in_level` is `DEFER_TO_FIRST_GAME`.

## S07-29 first-game audit schema

- **Runtime correctness:** one fresh game; Single Agent is sole submitter; four Skills loaded/read; fresh observe after every state change; Energy is one integer; CTRL/action pairing; bounded `RECONSIDER`; `DECISION_CLOSED`; compression recovery.
- **Strategic adherence:** Active Review Plan formed; Objective/Gap/Checkpoint continuity; revisions linked to fresh material evidence; plan churn and over-stubbornness; Promotion Frontier; review realization; commitment congestion and close-before-open; horizon adaptation; unnecessary Value of Information investigation.
- **Public trajectory:** quantitative and competition-partial scores; survival months and grade; promotion months and Level; Skill, Network, Output, Wealth, Health; relevant public review feedback.
- **Compression recovery:** if compression occurs, record four-Skill reread, Active Review Plan recovery, Delivery recovery or `UNKNOWN`, and whether stale snapshot authority was rejected.

## Decision

Readiness is `PASS_WITH_LIMITATION`: packaging, Runner validation, isolated installation, shared-state integrity, and local prerequisites are ready. Runtime/model behavior and gameplay evidence remain unvalidated. `NEXT_GAME = NOT_AUTHORIZED`; S07 remains ACTIVE. The next Main action is `S07-29 DeepSeek One-Game Gate`.
