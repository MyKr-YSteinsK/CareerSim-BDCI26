# CURRENT_STATE

> 当前事实快照；阶段过程由 Git 历史和关键对局索引承载，不在此追加流水。

## Project

- Repository: MyKr-YSteinsK/CareerSim-BDCI26
- Branch: `codex/s10-13-promotion-opportunity-forensics` (`IN_FLIGHT_EVIDENCE`; exact historical v6c parent)
- Current Stage: `S10-Lab｜架构重置与高分突破冲刺` ACTIVE；本checkout继承的S06/S07条目是历史语境，不代表现代main状态。
- S01–S05: COMPLETE；S05 final offline candidate: candidate-v2-final-offline；acceptance: PASS_WITH_KNOWN_LIMITATION
- S06: COMPLETE；Main acceptance=`PASS_WITH_KNOWN_RUNTIME_LIMITATION`。S06-24 原 v6 完成一局 `75.29 / 52.70 / 48m / A` 的 `VALID_48M_COMPLETION`，但 `RUNTIME_ADHERENCE_FAIL`；S06-25 形成 `candidate-v6b-runtime-correctness`，仅修 runtime/audit correctness，v6b 为 `STATIC_CORRECTNESS_PATCHED / NOT_RUNTIME_VALIDATED`。Design Freeze=ACTIVE。
- S07-01: `COMPLETE / QUARANTINE_FOR_MAIN_REVIEW`; Main disposition=`SURGICAL_COMPLIANCE_CLEANUP_REQUIRED`. S07-02 applied that narrow cleanup in descendant `candidate-v6c-compliance-cleanup`; W2/W3 have not started.
- Last verified: 2026-10-04

## Current candidate

- Current candidate: `candidate-v6d-promotion-portfolio-rebalance`；精确source `e7e8ab44dd85a29135eb089ef29de8fed298f4a4`，parent `candidate-v6c-compliance-cleanup` / `e5363c9b4958955e02f5f895cb1ba1c794215958`。S10-12唯一获准 fresh game 已自然完成：71.67 / partial50.17 /48m/A/L5，晋升M6/M12/M24/M42，early chain2/3；`V6D_NEAR_TARGET / V6D_NEAR_TARGET_COMPETITIVE`，尚未达75。Energy report19/Network5/intensive0/Health10/cleanup7，M18成长强于v6c但未晋升。202/202 action→fresh observe；DecisionClosed、compression reread、公开时钟一致性与flat reroute有缺陷，不能冒充完整runtime adherence PASS。冻结Candidate/Board/Risk/Planning/runtime/Runner/dependencies/provider/retry/fallback均未改，validation flags保持原值。raw本地FORENSIC_HOLD ACTIVE；无replacement/intervention/patch。`RETURN_FOR_V6D_GAME_GATE`；`NEXT_GAME=NOT_AUTHORIZED`。见 [S10-12 run report](runs/v6d-run01-promotion-portfolio-validation.md) / [compact evidence](runs/v6d-run01-promotion-portfolio-evidence.json)；历史静态依据见 [S10-11 review](reviews/S10-11_V6D_STATIC_REVIEW.md)。
- S10-13 offline promotion-gap取证完成：v6/v6d primary，v7o/RUN07/v6c支持、v1仅Tier-B；40 Review windows /720 Story（560clean、160mixed）。v6与v6d Story Skill净增长102/84，Main/promotion效果仍mixed；79同public情境75同选，0严格完整state/tenure matched pair。未发现安全可推广的Story/Risk/recognition patch；`VARIANCE_DOMINANT_NO_SAFE_PATCH`，建议`REPLICATE_EXACT_V6D_BEFORE_PATCH`（不授权游戏）。Candidate/Skills/runtime未改，全部live/Provider/install=0，既有holds保留。见 [S10-13 forensic report](research/S10-13_PROMOTION_OPPORTUNITY_FORENSICS.md) / [window data](research/S10-13_PROMOTION_WINDOW_DATA.json)。
- Canonical identity: [current_candidate.json](../../configs/current_candidate.json)
- Rebuildable runtime manifest: [runtime_manifest.json](../../configs/runtime_manifest.json)
- Three Skills: risk-review, structured-state-board, rolling-planning
- Architecture: Single Agent is the only action submitter; Board supplies public facts, Planning owns strategy, Risk gates current candidates
- Memory: NOT_IMPLEMENTED；fifth Skill: DEFERRED；Team/Swarm: DEFERRED

## Environment

- Frozen Runner SHA and dependency/source identity: [OFFICIAL_SOURCE_LOCK](OFFICIAL_SOURCE_LOCK.md)
- Local environment status and verification boundary: [ENVIRONMENT](ENVIRONMENT.md)
- Root .venv is local/ignored. S10-12 completed one explicitly authorized live lifecycle; this snapshot grants no further live operation.

## Runs and limitations

- Key real-run records: [RUN_HISTORY](RUN_HISTORY.md)
- Candidate v1 observed a high spread across two runs; this does not establish cause or stable performance.
- S06 Run #1: 53.83 quantitative / 37.68 competition partial / 48 months / C. It is one Main-reviewed observation, not a causal result.
- Candidate v4 first local run: 25.84 quantitative / 18.09 competition partial / 6 months / E; eliminated at M6 with Health=0. This is one terminal observation, not a 48-month completion or a causal result; the Runner score report was empty because the shared instance DB path differs from the root Runner's default, and the score was read from the exact session in the configured DB.
- S06-08 read-only forensics (Main-accepted evidence for the targeted survival-guard line): v4 Run #1 Health pattern = `CUMULATIVE_ATTRITION`; `H_SURVIVAL_GUARD = SUPPORTED_FOR_TARGETED_PATCH`; evidence supports a bounded public-state guard, not a numeric threshold or score benefit. See [forensic record](runs/v4-run1-health-forensic.md).
- S06-09 decoded/internal Dev material in [STRATEGY_EVIDENCE](STRATEGY_EVIDENCE.md) is `FORENSIC_HISTORY_ONLY / NON_DEPLOYABLE` for S07 policy justification; current deployable policy must have independent allowed public provenance.
- S06-24 v6 Run #1: 75.29 quantitative / 52.70 competition partial / 48 months / A; `VALID_48M_COMPLETION`. Runtime correctness = `RUNTIME_ADHERENCE_FAIL`: the semiannual H marker was missed, ordinary story deliberation reopened without fresh evidence, and CTRL/action pairing remains ambiguous. See [run evidence](runs/v6-run1-validation.md).
- S06-24 correction: 203 `take_action` attempts = 202 successful state changes + 1 malformed Energy multi-select rejected before mutation; the two additional 328,103-token responses were CurrentRoundCompressor compressions. Two compressed snapshots occurred without a three-Skill reread.
- v6b and v6c have no gameplay/provider validation transferred from v6. Runtime adherence, gameplay effectiveness, survival/score improvement, stable quantitative 80+, and hidden-test transfer remain NOT_PROVEN for v6c.
- Gameplay effectiveness: NOT_PROVEN；survival improvement: NOT_PROVEN；score improvement: NOT_PROVEN；stable quantitative 80+: NOT_PROVEN；hidden-test transfer: NOT_PROVEN.
- S06-24 local raw evidence was consulted read-only for S06-25 fact corrections and remains uncommitted; this state snapshot does not assert a canonical raw hash.

## Authorization

- TARGET: SURVIVE_48_MONTHS + QUANTITATIVE_75_PLUS（S10 practical goal；本局48m达成、75未达；stable75+ NOT_PROVEN）。历史80+目标不是本任务优化目标。
- NEXT_GAME: NOT_AUTHORIZED; S10-12 one-game authorization is consumed (install/service/Runner/new_game each1; replacement/intervention0). Any further benchmark requires a separate Main Game Gate.
- S06 Main acceptance: `PASS_WITH_KNOWN_RUNTIME_LIMITATION`; S06=`COMPLETE`. S07-01 Main decision: `SURGICAL_COMPLIANCE_CLEANUP_REQUIRED`; S07-02 implemented the descendant v6c cleanup statically for Main/S07 review. No strategy redesign, Team/Swarm/Memory/fifth Skill reopening, provider/gameplay, or Game Gate authorization. Design Freeze remains ACTIVE; NEXT_GAME remains NOT_AUTHORIZED.
- S03-MCP-REGISTRATION forensic hold: RELEASED_BY_MAIN. This does not imply strategy effectiveness.
