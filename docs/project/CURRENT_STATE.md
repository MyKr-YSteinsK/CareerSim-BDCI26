# CURRENT_STATE

> 当前事实快照；项目过程与历史结果保存在既有 canonical records 和 Git history，不在此追加流水。

## 1. Project Status

- Repository: `MyKr-YSteinsK/CareerSim-BDCI26`; branch: `main`.
- Competition team: `FZU-Loss快点降`; see [competition identity](COMPETITION_IDENTITY.json).
- Stage: `S11 ACTIVE`; `S10=CLOSED`; Human Play Lab=`CLOSED_BY_USER`.
- S11 当前范围是报告、证据整理和仓库收口；最终 repository freeze 尚未宣布。

## 2. Final Submission Identity

- Final Candidate: `candidate-v6-auditable-control-loop`; exact runtime source: `1114a04b75548cf52f030d123564e527060fc061`.
- Build/source-material commit: `113052a9a8943efc7fb2d7d1140f126e62e92040`.
- Frozen ZIP: `FZU-Loss-final-v6.zip`; 18,082 bytes; 7 files; SHA-256 `31e836b591703dfe520916828da033a57de260bb451d97047bbaee9daaa11b9b`.
- Final Skills: `structured-state-board`, `rolling-planning`, `risk-review`.
- Official upload: `NOT PERFORMED / NOT PROVEN`; package freeze does not prove portal upload.
- Canonical records: [submission identity](FINAL_SUBMISSION_IDENTITY.json), [manifest](FINAL_SUBMISSION_MANIFEST.md), [freeze audit](reviews/S10-23R_FINAL_SINGLE_SHOT_FREEZE.md).

## 3. Final Evidence Boundary

- Exact-v6 has one accepted full-run sample: `75.29 / 52.70 / 48m / A / L6`; the run is `RUNTIME_ADHERENCE_FAIL`.
- Candidate v1 is a counterexample to “highest score ever”: same-source samples are `76.04 / 48m / A / L6` and `35.31 / 25m / D / L4`.
- No stable 75+ result, expected-score estimate, hidden-test transfer, or causal superiority is established. See [final evidence](FINAL_EVIDENCE_REVIEW.md), [solution review](FINAL_SOLUTION_REVIEW.md), and [ID map](FINAL_ID_MAP.md).

## 4. Current Checkout Caveat

- `configs/current_candidate.json` and `configs/runtime_manifest.json` identify the current `main` runtime checkout as historical `candidate-v8a-v7o-donor-core-transplant`, with four Skills: `structured-state-board`, `rolling-planning`, `delivery-progress`, and `risk-review`.
- This checkout is not the final exact-v6 ZIP identity. Do not change Candidate, Skills, or runtime to make the checkout appear identical to the frozen package.

## 5. Current S11 State

- Human-readable reports `docs/final-report/00–10` are complete.
- The S03 sibling workspace was retired in S11-12; its 20 exported session payloads remain retained under the local hold documented in [workspace retirement](LOCAL_WORKSPACE_RETIREMENT.md).
- S10 absorbed Gate reviews and the S07-27 review have been removed from the current tree. Repository cleanup is ongoing; final freeze is not declared.

## 6. Evidence / Hold Boundary

- `FORENSIC_HOLD` records remain active. [Final evidence review](FINAL_EVIDENCE_REVIEW.md) lists 20 named active/pending holds: 18 `KEEP_ACTIVE`, 2 `UNKNOWN_REVIEW_REQUIRED`, and 0 releasable.
- The v7o hold membership remains partly `UNKNOWN_REVIEW_REQUIRED`; `RUN-0001` exact-v6 raw hold status remains `UNKNOWN`; the S10-21 local hold path remains unknown.
- The 20 S03 payloads remain retained and held as documented in [workspace retirement](LOCAL_WORKSPACE_RETIREMENT.md). Any hold release needs separate Main/Stage acceptance and scoped authorization. This task releases no hold.

## 7. Authorization Boundary

`NEW_GAME = NOT_AUTHORIZED`; `TAKE_ACTION = NOT_AUTHORIZED`; `PROVIDER_GAMEPLAY = CLOSED`; `NEW_CANDIDATE_SEARCH = CLOSED`; `TEAM_SWARM_EXPERIMENT = CLOSED_FOR_COMPETITION`; `FINAL_ZIP_REBUILD = NOT_AUTHORIZED`.

S11 permits cleanup, evidence consolidation, documentation, defense/portfolio work, and final repository review. The Team/Swarm disposition is scoped to competition work and does not establish general infeasibility.

## 8. Canonical Navigation

- [Repository README](../../README.md) · [reader navigation](../final-report/00-阅读导航.md)
- [Official source lock](OFFICIAL_SOURCE_LOCK.md) · [run history](RUN_HISTORY.md) · [environment](ENVIRONMENT.md)
- [Final evidence](FINAL_EVIDENCE_REVIEW.md) · [final solution](FINAL_SOLUTION_REVIEW.md) · [final ID map](FINAL_ID_MAP.md)
- [Submission identity](FINAL_SUBMISSION_IDENTITY.json) · [manifest](FINAL_SUBMISSION_MANIFEST.md) · [submission contract](FINAL_SUBMISSION_CONTRACT.md)
- [Project retrospective](PROJECT_RETROSPECTIVE.md) · [architecture retrospective](ARCHITECTURE_RETROSPECTIVE.md) · [experiment retrospective](EXPERIMENT_RETROSPECTIVE.md)
- [Local workspace retirement](LOCAL_WORKSPACE_RETIREMENT.md)
