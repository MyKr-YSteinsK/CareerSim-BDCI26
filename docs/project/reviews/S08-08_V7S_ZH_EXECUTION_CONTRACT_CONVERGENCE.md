# S08-08 v7s Chinese Execution Contract Convergence

## Decision

`V7S_READY_FOR_GAME_GATE`

This decision reports static integration readiness only. It does not authorize a game, provider call, install, service, MCP, DB write, Runner play, or official submission.

## Static identity

- Frozen base: `main@ea7a6fbf14c346418e23fe86a438c5c2c193b6f3`.
- Candidate: `candidate-v7s-zh-recovery-controller`; parent: `candidate-v7r-early-promotion-rescue`.
- Candidate status: `STATIC_IMPLEMENTED_NOT_RUNTIME_VALIDATED`; all validation flags are false and `next_game_authorized=false`.
- Runtime manifest instruction: 3,460 characters; manifest SHA-256 `68736614b176a3847ee0da12e6f13787fedb878b768c489fc5bfa46a4eb5decf`; instruction SHA-256 `53c9d8bda8a10c3c1b38c67fc43d02a1609afc3b892d6a1d3426dec70d9ea032`.
- Canonical Skill blobs:
  - `structured-state-board`: `611e75d97234131acd5f321b5c7b75f50c1960ef`
  - `rolling-planning`: `ef3183e5461ecd2603152e1a3caf88991f8150f0`
  - `delivery-progress`: `34f88bd75a286a4e6cd21f150ad884f5cd181cd9`
  - `risk-review`: `10ebf393b6e9156e52382effe503d29c3169e118`

The replacement files were first copied and byte-verified exactly. To make the required `git diff --check` pass, only two trailing Markdown hard-break spaces after `Can Submit Action: No.` were removed from Planning and Risk; visible text and runtime rules are unchanged. Candidate Git blob IDs were recomputed for those two Skills. The supplied `.pyc` was copied to the ignored cache path as requested by the replacement set; it was not executed or committed.

## Repository files changed

- `AGENTS.md`
- `configs/current_candidate.json`, `configs/runtime_manifest.json`
- `docs/project/AGENT_RUNTIME_CONTRACT.md`, `docs/project/CANDIDATE_EVALUATION_CONTRACT.md`, `docs/project/FINAL_SUBMISSION_CONTRACT.md`, `docs/project/LIVE_RUN_PROGRESS_CONTRACT.md`
- `docs/project/CURRENT_STATE.md`, `docs/project/LIVE_RUN_WORKFLOW.md`, this review
- `scripts/build_final_solution.py`
- `skills/structured-state-board/SKILL.md`, `skills/rolling-planning/SKILL.md`, `skills/delivery-progress/SKILL.md`, `skills/risk-review/SKILL.md`
- `tests/test_candidate_v7_contract.py`, removed `tests/test_candidate_v7o_pre_run_contract.py`, added `tests/test_candidate_v7s_contract.py`, `tests/test_candidate_packaging.py`, `tests/test_final_solution_builder.py`, `tests/test_skill_behavior_eval.py`

## Semantic integration

- Board keeps poor grade and no-promotion in `REVIEW`; only fresh explicit material evidence creates binding `STICKY` state.
- Planning assigns progression failures to `PROGRESSION` in `MODE=A`; `MODE=S` is limited to explicit material constraints and uses minimum necessary relief. Performance or delivery repair remains valid when it directly relieves an explicit job-continuity threat.
- Board owns clean current-Level `GAIN / NO_GAIN / UNKNOWN` attribution, untouched-dimension carry, Level/session resets, later-gain override, and the no-cap inference boundary. Planning discounts only the affected dimension and avoids blind immediate repeats.
- The next public formal Review remains the preparation checkpoint after good-grade/no-promotion; Skill retains possible promotion value.
- Planning owns bounded warning cleanup and `DELIVERY` recovery; Risk only gates the final candidate and does not replan. Delivery may track visible commitments before the first Review, and a tool receipt alone does not verify a career result.
- Manifest preserves the evidence firewall, ownership, whole-game execution loop, action preflight, CTRL/DL markers, and ordered best-effort context recovery. Machine-facing tokens remain English; runtime prose is Chinese-primary.

## Contracts and verification

Integrated contracts:

- `docs/project/AGENT_RUNTIME_CONTRACT.md`
- `docs/project/CANDIDATE_EVALUATION_CONTRACT.md`
- `docs/project/LIVE_RUN_PROGRESS_CONTRACT.md`
- `docs/project/FINAL_SUBMISSION_CONTRACT.md`

`AGENTS.md` and `LIVE_RUN_WORKFLOW.md` contain short references only; they do not duplicate the contracts or expand task permissions. Planner's `107/107` static matrix and `36/36` package-level audit are acknowledged as Planner-reported results, not independently reproduced here.

Targeted tests passed: 45 cases across the Candidate/Skill contracts, governance contracts, package contract, final builder, and existing Skill behavior evaluation. The final builder cases use temporary synthetic Git repositories/materials only and cover status/team/Skill/material/secret rejection, exact whitelist, default and explicit archive layouts, deterministic bytes, extraction identity, and sidecars.

Offline Candidate package validation passed at `.local/runtime/s08-08-v7s-candidate-package-verified`: exactly one manifest and four canonical Skills, accepted as a `skill_bundle`, with canonical manifest instruction and Skill bytes. Read-only local runtime inspection confirmed `max_retries=2`. `git diff --check` passed.

Runner source, `pyproject.toml`, `uv.lock`, and local retry configuration were not changed. No official final `solution.zip` was generated. The attached ZIP was copied byte-for-byte to `D:\CS\temp\CareerSim\S08-08-v7s-中文执行合同与失败恢复收敛.zip` (49,388 bytes; SHA-256 `7bf96e20a79f019c81ed78b57f893bdf0b8eab93f8d8dcbf87972549b969a564`).

No provider call, network probe, service lifecycle, install/reload, MCP, DB write, Runner play, or game operation occurred.

## Limitations and next gate

These checks establish static identity, packaging behavior, and contract consistency; they do not establish gameplay adherence, provider/runtime behavior, promotion, score, survival, or strategy improvement. Prior gameplay/provider evidence does not transfer to v7s. The S08-RUN02 `FORENSIC_HOLD` remains active pending Main/Stage review. `NEXT_GAME=NOT_AUTHORIZED`; any game requires a separate Main Game Gate.
