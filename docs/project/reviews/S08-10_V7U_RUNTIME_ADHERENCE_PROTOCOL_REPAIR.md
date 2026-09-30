# S08-10｜v7u Runtime Adherence Protocol Repair

## TASK_RESULT｜S08-10

**Status:** COMPLETE — offline/static contract integration.
**Decision:** `V7U_READY_FOR_GAME_GATE`
**Base:** `main@591ce8a203c4e7dda18ced9031c4c2bf6b4c844a`
**Parent:** `candidate-v7t-execution-semantic-repair`
**Candidate:** `candidate-v7u-runtime-adherence-protocol`
**Strategy delta:** `RUNTIME_ADHERENCE_PROTOCOL_ONLY`
**NEXT_GAME:** `NOT_AUTHORIZED`
**S08-RUN03 FORENSIC_HOLD:** `ACTIVE`; this task does not close it.

The required `git fetch origin` completed. At preflight, `main == origin/main == 591ce8a203c4e7dda18ced9031c4c2bf6b4c844a` and the working tree was clean. The bundle manifest and all four bundled text files match their declared byte counts and SHA-256 values.

This task performed offline/static repository work only. No provider request, network probe, service lifecycle, install/reload, MCP call, shared DB access, Runner play, or game occurred. The prior v7t gameplay/provider evidence is not inherited by v7u.

## Implemented contract

### Executor control state and fresh-observe gate

`CONTROL_STATE=READY|OBSERVE_REQUIRED|BLOCKED` is executor-owned. `READY` requires a fresh same-session observe, rebuilt Board and Delivery, one new Planning pass, final Risk, and closed preflight. Each successful `take_action` moves the executor to `OBSERVE_REQUIRED`; the `{success,error}` receipt contains no public state and cannot authorize another action. Only a same-session fresh `observe` may follow. After that observe, Board (including `PROGRESSION_RESPONSE`), Delivery, Planning, and Risk rebuild before preflight can return the executor to `READY`.

Failed or unknown action outcomes, failed observes, session mismatch, and unclosed preflight move the executor to `BLOCKED`. `BLOCKED` forbids action. Existing bounded same-session recovery is the only recovery route; `RECOVERY_READY` alone does not authorize action.

### CTRL v2 and Risk closure

The current marker is:

```text
[CTRL G=<gap|?> P=<A|S|?> R=<PASS|ALLOW|WARN|RECONSIDER|UNKNOWN> RB=<NONE|DONE|BLOCKED>]
```

`RB=NONE` means no reconsideration branch occurred; `RB=DONE` means one bounded branch closed with a final Risk other than `RECONSIDER`; `RB=BLOCKED` means the branch or gate is unresolved and action is forbidden. Preflight requires `CONTROL_STATE=READY`, final `R!=RECONSIDER`, and `RB in {NONE,DONE}`. Risk retains `RISK / REASON` output ownership and does not submit actions or declare executor state.

### Delivery checkpoint v2

The current marker uses `checkpoint=NEAR|NOT_NEAR|UNKNOWN`. `NEAR` requires public evidence linking the item to the current Review Window or commitment checkpoint; `NOT_NEAR` means such support is absent; insufficient evidence uses `UNKNOWN`. An empty Delivery state uses `checkpoint=NOT_NEAR`.

### Sequential quarterly Energy and NO_GAIN handoff

`QUARTER_INTENT` now contains only `<MODE | current target>`. It cannot encode a number or sequence of actions. Each Energy decision requires a fresh same-session observe, Board and `PROGRESSION_RESPONSE` rebuild, Delivery rebuild, a new Planning pass, Risk and preflight, and exactly one action. Previous remaining-action intent is discarded. Clean `NO_GAIN` must be visible in Board and consumed by a new Planning pass; an immediately repeated no-gain action is rejected when a responsive alternative exists. Existing NO_GAIN policy text is preserved.

The M42 scenario is explicit: if Energy is 3 and Output is 26, the first Report Preparation followed by a fresh observe with Output still 26 requires `O=NO_GAIN` and a new Planning pass. If a responsive alternative exists, a second immediate Report Preparation does not satisfy the contract.

## Historical audit compatibility

The offline auditor accepts both legacy CTRL `X=0|1|-` and current CTRL `RB=NONE|DONE|BLOCKED`. It keeps legacy closure meanings, rejects current `RB=BLOCKED`, and still rejects any submitted final `R=RECONSIDER`. Delivery parsing accepts historical `checkpoint=0|1|?` and current `NEAR|NOT_NEAR|UNKNOWN`; historical invalid values 2/3/4 remain invalid.

The exact S08-RUN03 forensic replay remains **174 valid / 33 invalid checkpoint / 0 missing** after the parser extension. No archived S08-RUN03 artifact or post-run summary was rewritten.

## Candidate identity

| Field | Value |
|---|---|
| Candidate | `candidate-v7u-runtime-adherence-protocol` |
| Parent | `candidate-v7t-execution-semantic-repair` |
| Base main SHA | `591ce8a203c4e7dda18ced9031c4c2bf6b4c844a` |
| Status | `STATIC_IMPLEMENTED_NOT_RUNTIME_VALIDATED` |
| Manifest instruction characters | 5,194 (limit 5,200) |
| Manifest SHA-256 | `3f15967c29afddcd9baaaac04fbe0261241947be76e207c8d3388169d6c1ffee` |
| Instruction SHA-256 | `5dd3c81f0ca574096946158d35ed93b659e919d5e83dbb19aee2fc63c9ebd200` |
| `runtime_contract_delta` | `FRESH_OBSERVE_CONTROL_STATE`, `EXPLICIT_RECONSIDER_BRANCH_ENUM`, `NAMED_DELIVERY_CHECKPOINT_ENUM`, `PER_ACTION_ENERGY_REPLAN` |

All v7u validation flags are `false`, including gameplay, provider, runtime, long-horizon, score/survival, hidden-transfer, and next-game authorization flags.

Skill Git blobs:

| Skill | Git blob |
|---|---|
| `structured-state-board` | `611e75d97234131acd5f321b5c7b75f50c1960ef` |
| `rolling-planning` | `6088fc6f56c60d8d98b176b6c7ef8f05b1f2f8dd` |
| `delivery-progress` | `64e060b1febf746a05aa07494755a7f9d6eee600` |
| `risk-review` | `e602fe1a3343a28b472259ae46cfca780e780e48` |

The v7t parent manifest SHA stored in its Candidate record is `15c3638da5e49b60fa6f30f3d702cc5d170cc91c91628f0dc0ac4eb4fd4b1c1d`; with Windows `core.autocrlf=true`, this is the CRLF checkout digest. Its normalized LF Git content hashes to `c06ac385b30476e110c36691adbec531cce8afd2d12388c1bdc1496c4d021041`. v7u carries the parent-recorded identity and hashes its own CRLF manifest bytes, which match the built package.

## Manual cross-file contradiction review

Reviewed after implementation using priority `model execution correctness > cross-file consistency > critical-rule salience > deduplication`.

- Manifest, Agent Runtime Contract, Planning, Risk, and preflight agree on the state transitions and action gate.
- Current runtime markers agree across manifest/Risk/Delivery; current runtime contracts contain no `X=` field or numeric checkpoint enum. The auditor alone retains legacy parsing.
- Risk closure states agree with preflight: unresolved reconsideration cannot submit.
- The quarterly intent has no batch commitment; each subsequent action requires a rebuilt current-evidence pass.
- `structured-state-board/SKILL.md` remains byte-identical to the base. Planning changes are confined to sequential Energy handoff. Delivery changes are confined to checkpoint representation/default. Risk changes are confined to reconsideration closure serialization and preflight semantics.
- v7t adopted/rejected mechanisms, architecture, design intent, MODE/recovery/Review/event/risk-cleanup/no-cap policy, Runner, dependencies, and retry remain unchanged.

## Verification

- Targeted v7u contract, v7 contract, v7s governance, packaging, behavior-evaluation, S08-09 forensic regression, and post-run audit tests: **71 passed**.
- Offline canonical package: `.local/scratch/s08-10/submission-final`; five files, exactly four Skills, `submission_mode=skill_bundle`; manifest and instruction hashes match Candidate metadata.
- Retry read only from `C:\Users\Yukis\.jiuwenswarm-instances\career_emu\config\config.yaml`, `models.defaults[0].model_client_config.max_retries=2`.
- Runner SHA remains `f61c738c72e51b77298cc1c14c7c6ebf4b6c527d`; `pyproject.toml`, `uv.lock`, and `career_sim_runner` are unchanged from base.
- `git diff --check`: PASS.
- Provider / service / install / MCP / DB / Runner play / game calls: **0**.

## Exact changed files

- `configs/current_candidate.json`
- `configs/runtime_manifest.json`
- `docs/project/AGENT_RUNTIME_CONTRACT.md`
- `docs/project/CURRENT_STATE.md`
- `docs/project/reviews/S08-10_V7U_RUNTIME_ADHERENCE_PROTOCOL_REPAIR.md`
- `scripts/post_run_audit.py`
- `skills/rolling-planning/SKILL.md`
- `skills/delivery-progress/SKILL.md`
- `skills/risk-review/SKILL.md`
- `tests/test_candidate_v7_contract.py`
- `tests/test_candidate_v7s_contract.py`
- `tests/test_candidate_packaging.py`
- `tests/test_skill_behavior_eval.py`
- `tests/test_post_run_audit.py`
- `tests/test_s08_10_runtime_adherence_protocol.py`

`NEXT_GAME=NOT_AUTHORIZED`. No game authorization is created by `V7U_READY_FOR_GAME_GATE`.
