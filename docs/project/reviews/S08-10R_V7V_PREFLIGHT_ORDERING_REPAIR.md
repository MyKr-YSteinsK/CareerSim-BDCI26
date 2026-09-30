# S08-10R｜v7v Preflight Ordering Repair

## TASK_RESULT｜S08-10R

**Status:** COMPLETE — offline/static execution-contract correction.
**Decision:** `V7V_READY_FOR_GAME_GATE`
**Base:** `main@882d47202d4d8d8305acbf7edb451ee8d68fe1ce`
**Parent:** `candidate-v7u-runtime-adherence-protocol`
**Candidate:** `candidate-v7v-preflight-ordering-repair`
**Decision ID:** `S08_10R_PREFLIGHT_ORDERING_REPAIR`
**Strategy delta:** `RUNTIME_GATE_ORDERING_CORRECTION_ONLY`
**NEXT_GAME:** `NOT_AUTHORIZED`
**S08-RUN03 FORENSIC_HOLD:** `ACTIVE`; this task does not close it.

## Confirmed issue

The v7u manifest defined `READY` as requiring a completed preflight, while action preflight itself required `CONTROL_STATE=READY`. The Agent Runtime Contract repeated the same cycle. This is an execution-order contradiction; it does not indicate a strategy-kernel or Skill defect.

## Implemented ordering

```text
fresh same-session observe
→ Board rebuild
→ Delivery rebuild
→ one new Planning pass
→ final Risk
→ CONTROL_STATE=READY
→ preflight
→ PREFLIGHT=PASS
→ exactly one take_action
→ CONTROL_STATE=OBSERVE_REQUIRED
```

`READY` is established from the current observe and its Board/Delivery/Planning/final-Risk outputs. Preflight consumes that existing decision and checks the same session and observe, one legal integer choice, final Risk, CTRL/RB, and valid CTRL/DL markers. PASS authorizes only one submission of the current choice and cannot be reused. Any failed check sets `BLOCKED` and forbids action. A successful action consumes READY and the one-use preflight; its `{success,error}` receipt cannot produce READY. Another decision requires a fresh same-session observe and a complete rebuild. Recovery likewise rebuilds and establishes a new READY before its new preflight.

Only these behavior-facing files changed:

- `configs/runtime_manifest.json`
- `docs/project/AGENT_RUNTIME_CONTRACT.md`

No Skill change or strategy-kernel deletion was needed. The manifest instruction decreased from 5,194 to **5,122 characters**.

## Candidate identity

| Field | Value |
|---|---|
| Candidate | `candidate-v7v-preflight-ordering-repair` |
| Parent | `candidate-v7u-runtime-adherence-protocol` |
| Base main SHA | `882d47202d4d8d8305acbf7edb451ee8d68fe1ce` |
| Status | `STATIC_IMPLEMENTED_NOT_RUNTIME_VALIDATED` |
| Decision | `S08_10R_PREFLIGHT_ORDERING_REPAIR` |
| Runtime contract delta | v7u’s four deltas plus `ACYCLIC_PREFLIGHT_ORDERING` |
| Manifest SHA-256 | `c4030a21f2bf7b08a2f1b927058379fd30bd45fa247ce1615444f7f531ebbc53` |
| Instruction SHA-256 | `f2dac483c287a1ac3bf2b73956d37b6c3ebd9799e475cc0ac71729e2c99dcea9` |

All validation flags are `false`; v7t gameplay/provider evidence is not inherited.

All four Skill blobs are unchanged from the base:

| Skill | Git blob |
|---|---|
| `structured-state-board` | `611e75d97234131acd5f321b5c7b75f50c1960ef` |
| `rolling-planning` | `6088fc6f56c60d8d98b176b6c7ef8f05b1f2f8dd` |
| `delivery-progress` | `64e060b1febf746a05aa07494755a7f9d6eee600` |
| `risk-review` | `e602fe1a3343a28b472259ae46cfca780e780e48` |

## Required final review

| Question | Result |
|---|---|
| Is the control-state graph acyclic? | YES |
| Can READY exist before preflight? | YES |
| Can preflight run without READY? | NO |
| Can one preflight authorize two actions? | NO |
| Can a `take_action` receipt return READY? | NO |

## Verification and boundaries

- Targeted v7/v7u contract, v7s governance, package, Skill behavior, post-run audit, S08-09 forensic, v7u inherited-contract, and v7v ordering tests: **75 passed**.
- Canonical package: `.local/scratch/s08-10r/submission-v7v`; Runner validation reports `submission_mode=skill_bundle`, exactly four Skills, and five package files. Package manifest and all Skill files match their canonical sources.
- Local `models.defaults[0].model_client_config.max_retries` was read only and remains `2`.
- `pyproject.toml`, `uv.lock`, and `career_sim_runner` are unchanged from the base. Runner SHA remains `f61c738c72e51b77298cc1c14c7c6ebf4b6c527d`.
- `git diff --check`: PASS.
- Provider, service, install/reload, MCP, shared DB, Runner play, and game operations: **0**.

The supplied ZIP was copied unchanged to `D:\CS\temp\CareerSim\S08-10R-v7v-Preflight-Ordering-Repair.zip`; size **5,497 bytes**, SHA-256 `252c023f4c5b6337d46f225bf203bd41b14039629bff2a67e552c1fafadf7ea4`. Its three text payload files match the bundle manifest’s byte counts and SHA-256 values.

`NEXT_GAME=NOT_AUTHORIZED`. No gameplay result or RUN_HISTORY entry is created by this task.
