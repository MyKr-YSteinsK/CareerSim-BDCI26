# Final Display-ID Map

This registry gives representative evidence stable presentation IDs and points each ID back to its legacy identity, Git provenance, and canonical record. Display IDs are navigation labels; they do not replace Stage, Task, Candidate, Run, or decision IDs and do not encode quality or rank.

## Rules

- Categories are `CAND-####` (Candidate), `RUN-####` (run), `EXP-####` (experiment/research result), `DEC-####` (major decision), and `SUB-####` (submission artifact).
- Each category is append-only. Never reuse or renumber an assigned ID; new entries take the next number in that category.
- Keep legacy IDs and provenance in every canonical record. Disambiguate duplicate legacy labels with category, canonical path, and commit/source; a label alone is not a unique key.
- Use `UNKNOWN` where evidence is missing and `—` where a field does not apply. Do not infer identity, retention, or outcome from nearby files.
- This is a representative seed index, not a numbering migration of the repository.

## Canonical registry

| Display ID | Type | Legacy Stage / Task | Candidate | Run / Artifact | Source / Record Commit | Canonical Evidence | Retention / Hold | Final Relevance |
|---|---|---|---|---|---|---|---|---|
| `CAND-0001` | Candidate | S10-23R-v2 | `candidate-v6-auditable-control-loop` | — | Runtime source `1114a04b75548cf52f030d123564e527060fc061`; selection record `79670f814c9900c959df16905e8fa847cdf49bdd` | [Final identity](FINAL_SUBMISSION_IDENTITY.json); [freeze audit](reviews/S10-23R_FINAL_SINGLE_SHOT_FREEZE.md) | Frozen historical source; related run raw retention is recorded separately. | Exact-v6 final selection; not a claim of stable performance or theoretical optimality. |
| `RUN-0001` | Run | S06-24 | `candidate-v6-auditable-control-loop` | v6 Run #1: 75.29 / 52.70 / 48m / A / L6 | Run base `1114a04b75548cf52f030d123564e527060fc061`; record `40589e35564e6c3822851586c7192b7089183722` | [v6 Run #1 validation](runs/v6-run1-validation.md) | Compact record tracked; supporting raw is noted as local/uncommitted in CURRENT_STATE. Raw hold status: UNKNOWN. | One valid 48-month sample; `RUNTIME_ADHERENCE_FAIL`. No stable or causal inference. |
| `RUN-0002` | Run | S09-RUN08 | `candidate-v8a-v7o-donor-core-transplant` | v8a sample #2: 59.00 / 41.30 / 48m / C / L4 | Run base `a3b6cd57223ba4d79b26b4a77f724f33fa72f275`; record `4fb189209595e4733521c45c46099e18d570296d` | [S09-RUN08 sample #2](runs/v8a-full-horizon-sample2.md) | Local raw and listed artifacts remain on `FORENSIC_HOLD=ACTIVE`; release/cleanup is not implied. | Historical lower-tail comparator; not the final Candidate. |
| `EXP-0001` | Experiment / research result | S10-22 | — | `SIMULATOR_POLICY_SEARCH_NOT_FEASIBLE`; B0 completed 2/16; 12 macro configurations defined, baseline only evaluated | Research base `fd7572f8695191b96781fe1f7f75e38843899d0f`; result record `24be9e49cded74dba2559aade3a7cac870ddd54c` | [Research report](research/S10-22_SIMULATOR_POLICY_SEARCH.md); [final opportunity gate](reviews/S10-22_FINAL_OPPORTUNITY_GATE.md); [compact results](research/S10-22_POLICY_RESULTS.json) | Local `.local/runtime/s10-22-policy-search` evidence has `FORENSIC_HOLD=ACTIVE`; do not treat this index as hold release. | Feasibility gate only: screening, confirmation, and 128-seed holdout were unrun. It does not show that all simulator policies lack an advantage. |
| `SUB-0001` | Submission artifact | S10-23R-v2 | `candidate-v6-auditable-control-loop` | `FZU-Loss-final-v6.zip`; 18,082 bytes / 7 files; SHA-256 `31e836b591703dfe520916828da033a57de260bb451d97047bbaee9daaa11b9b` | Runtime source `1114a04b75548cf52f030d123564e527060fc061`; build `113052a9a8943efc7fb2d7d1140f126e62e92040`; identity/record `79670f814c9900c959df16905e8fa847cdf49bdd` | [Final identity](FINAL_SUBMISSION_IDENTITY.json); [manifest](FINAL_SUBMISSION_MANIFEST.md); [freeze audit](reviews/S10-23R_FINAL_SINGLE_SHOT_FREEZE.md) | Final ZIP and sidecars are retained locally as recorded in the manifest; do not rebuild after the final hash. | Frozen single-shot package. Official upload was not performed in the recorded evidence. |

## Navigation notes

- Current stage and authorization boundary: [CURRENT_STATE](CURRENT_STATE.md).
- The checkout's `configs/current_candidate.json`, `configs/runtime_manifest.json`, and four Skills are historical v8a working-tree state; they are not the final-v6 package identity.
- Representative runs remain single-run/session evidence. A Display ID does not upgrade validation, causality, generalization, or retention status.
