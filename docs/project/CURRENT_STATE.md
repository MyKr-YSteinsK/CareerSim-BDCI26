# CURRENT_STATE

> 当前事实快照；阶段过程由 Git 历史和关键对局索引承载，不在此追加流水。

## Project

- Repository: MyKr-YSteinsK/CareerSim-BDCI26
- Branch: main
- Current Stage: S06-Lab
- S01–S05: COMPLETE；S05 final offline candidate: candidate-v2-final-offline；acceptance: PASS_WITH_KNOWN_LIMITATION
- S06: IN_PROGRESS；S06-01 至 S06-04 已由 Main 接受为静态/离线工程成果；S06-05 工程收口、S06-06 静态复核及 S06-07 三 Skill policy consolidation 已完成；S06-16 完成最终控制架构审查；S06-17 控制语义获接受；S06-18/S06-19 静态收口已完成；S06-20 已获 Main 接受，附一个定向补回项；S06-21 survival-trend guard 静态补回完成，待 Main final static review；S06 未宣布完成
- Last verified: 2026-09-25

## Current candidate

- Candidate: candidate-v6-auditable-control-loop；S06-20 已接受，S06-21 survival-trend guard 最终静态补回完成、待 Main re-review；Design Freeze awaits re-acceptance；parent: candidate-v5-evidence-driven-phase-policy；strategy delta: AUDITABLE_CANDIDATE_FIRST_CONTROL_LOOP
- Canonical identity: [current_candidate.json](../../configs/current_candidate.json)
- Rebuildable runtime manifest: [runtime_manifest.json](../../configs/runtime_manifest.json)
- Three Skills: risk-review, structured-state-board, rolling-planning
- Architecture: Single Agent is the only action submitter; Board supplies public facts, Planning owns strategy, Risk gates current candidates
- Memory: NOT_IMPLEMENTED；fifth Skill: DEFERRED；Team/Swarm: DEFERRED

## Environment

- Frozen Runner SHA and dependency/source identity: [OFFICIAL_SOURCE_LOCK](OFFICIAL_SOURCE_LOCK.md)
- Local environment status and verification boundary: [ENVIRONMENT](ENVIRONMENT.md)
- Root .venv is local/ignored. This snapshot does not authorize or claim a live runtime check.

## Runs and limitations

- Key real-run records: [RUN_HISTORY](RUN_HISTORY.md)
- Candidate v1 observed a high spread across two runs; this does not establish cause or stable performance.
- S06 Run #1: 53.83 quantitative / 37.68 competition partial / 48 months / C. It is one Main-reviewed observation, not a causal result.
- Candidate v4 first local run: 25.84 quantitative / 18.09 competition partial / 6 months / E; eliminated at M6 with Health=0. This is one terminal observation, not a 48-month completion or a causal result; the Runner score report was empty because the shared instance DB path differs from the root Runner's default, and the score was read from the exact session in the configured DB.
- S06-08 read-only forensics (Main-accepted evidence for the targeted survival-guard line): v4 Run #1 Health pattern = `CUMULATIVE_ATTRITION`; `H_SURVIVAL_GUARD = SUPPORTED_FOR_TARGETED_PATCH`; evidence supports a bounded public-state guard, not a numeric threshold or score benefit. See [forensic record](runs/v4-run1-health-forensic.md).
- S06-09 public Dev strategy evidence is recorded in [STRATEGY_EVIDENCE](STRATEGY_EVIDENCE.md); it does not prove policy effectiveness or hidden-test transfer.
- v5 remains the static parent candidate. v6 candidate-first order, action refresh, review reset, strict plateau comparison, Risk enforcement and CTRL marker are static contracts only; runtime adherence and marker truthfulness are NOT_PROVEN.
- Gameplay effectiveness: NOT_PROVEN；stable quantitative 80+: NOT_PROVEN；hidden-test generalization: NOT_PROVEN.
- S06 Run #1 raw evidence on the current machine: unavailable/deferred; no raw hash is asserted.

## Authorization

- TARGET: STABLE_QUANTITATIVE_80_PLUS (goal only; not achieved fact)
- NEXT_GAME: NOT_AUTHORIZED; any benchmark requires a separate Main Game Gate.
- S06-21: candidate-v6-auditable-control-loop remains a static candidate; the targeted public survival-trend-to-Risk-Budget rule is implemented and pending Main final static review. This task used no game, provider, service, install/reload or MCP operation. Further gameplay requires a separate Main Game Gate.
- S03-MCP-REGISTRATION forensic hold: RELEASED_BY_MAIN. This does not imply strategy effectiveness.
