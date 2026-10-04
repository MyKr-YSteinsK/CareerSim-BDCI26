# CURRENT_STATE

> 当前事实快照；阶段过程由 Git 历史和关键对局索引承载，不在此追加流水。

## Project

- Repository: MyKr-YSteinsK/CareerSim-BDCI26
- Branch: `codex/s10-10-v6c-revival-run01` (`IN_FLIGHT_EVIDENCE`; exact historical v6c parent)
- Current Stage: `S10-Lab｜架构重置与高分突破冲刺` ACTIVE；下述 S06/S07 内容为本 checkout 的历史语境，不代表现代 main 状态。
- S01–S05: COMPLETE；S05 final offline candidate: candidate-v2-final-offline；acceptance: PASS_WITH_KNOWN_LIMITATION
- S06: COMPLETE；Main acceptance=`PASS_WITH_KNOWN_RUNTIME_LIMITATION`。S06-24 原 v6 完成一局 `75.29 / 52.70 / 48m / A` 的 `VALID_48M_COMPLETION`，但 `RUNTIME_ADHERENCE_FAIL`；S06-25 形成 `candidate-v6b-runtime-correctness`，仅修 runtime/audit correctness，v6b 为 `STATIC_CORRECTNESS_PATCHED / NOT_RUNTIME_VALIDATED`。Design Freeze=ACTIVE。
- S07-01: `COMPLETE / QUARANTINE_FOR_MAIN_REVIEW`; Main disposition=`SURGICAL_COMPLIANCE_CLEANUP_REQUIRED`. S07-02 applied that narrow cleanup in descendant `candidate-v6c-compliance-cleanup`; W2/W3 have not started.
- Last verified: 2026-10-04

## Current candidate

- Current candidate: `candidate-v6c-compliance-cleanup`，exact source `e5363c9b4958955e02f5f895cb1ba1c794215958`；parent v6b；frozen Candidate/manifest/three Skills 未改，metadata validation flags 仍全 false。S10-10 消耗一次 install、service lifecycle、Runner play/fresh game，零replacement/介入；自然48m完成，64.26 quantitative /44.98 partial /B /L5，晋升M6/M12/M24/M42。Classification=`V6C_MID_SAMPLE`，Decision=`V6C_CORE_MID`；197/197动作后fresh observe、单整数/费用通过，但DecisionClosed与两次compression recovery失败，故runtime adherence未通过。Provider/gameplay事实只绑定本session，不转移原v6的75.29收益。服务已停止、端口释放；`FORENSIC_HOLD=ACTIVE`，pending Main/Stage review；`RETURN_FOR_V6C_REVIVAL_GATE`，`NEXT_GAME=NOT_AUTHORIZED`。见 [S10-10 report](runs/v6c-revival-run01-validation.md) / [compact evidence](runs/v6c-revival-run01-evidence.json)。现代main的v8a fallback与根v14证据分支未改；其余旧条目保留历史语境。
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
- S06-09 decoded/internal Dev material in [STRATEGY_EVIDENCE](STRATEGY_EVIDENCE.md) is `FORENSIC_HISTORY_ONLY / NON_DEPLOYABLE` for S07 policy justification; current deployable policy must have independent allowed public provenance.
- S06-24 v6 Run #1: 75.29 quantitative / 52.70 competition partial / 48 months / A; `VALID_48M_COMPLETION`. Runtime correctness = `RUNTIME_ADHERENCE_FAIL`: the semiannual H marker was missed, ordinary story deliberation reopened without fresh evidence, and CTRL/action pairing remains ambiguous. See [run evidence](runs/v6-run1-validation.md).
- S06-24 correction: 203 `take_action` attempts = 202 successful state changes + 1 malformed Energy multi-select rejected before mutation; the two additional 328,103-token responses were CurrentRoundCompressor compressions. Two compressed snapshots occurred without a three-Skill reread.
- v6b and v6c have no gameplay/provider validation transferred from v6. Runtime adherence, gameplay effectiveness, survival/score improvement, stable quantitative 80+, and hidden-test transfer remain NOT_PROVEN for v6c.
- Gameplay effectiveness: NOT_PROVEN；survival improvement: NOT_PROVEN；score improvement: NOT_PROVEN；stable quantitative 80+: NOT_PROVEN；hidden-test transfer: NOT_PROVEN.
- S06-24 local raw evidence was consulted read-only for S06-25 fact corrections and remains uncommitted; this state snapshot does not assert a canonical raw hash.

## Authorization

- TARGET: STABLE_QUANTITATIVE_80_PLUS (goal only; not achieved fact)
- NEXT_GAME: NOT_AUTHORIZED; the S06-24 one-game authorization is consumed. Any further benchmark requires a separate Main Game Gate.
- S06 Main acceptance: `PASS_WITH_KNOWN_RUNTIME_LIMITATION`; S06=`COMPLETE`. S07-01 Main decision: `SURGICAL_COMPLIANCE_CLEANUP_REQUIRED`; S07-02 implemented the descendant v6c cleanup statically for Main/S07 review. No strategy redesign, Team/Swarm/Memory/fifth Skill reopening, provider/gameplay, or Game Gate authorization. Design Freeze remains ACTIVE; NEXT_GAME remains NOT_AUTHORIZED.
- S03-MCP-REGISTRATION forensic hold: RELEASED_BY_MAIN. This does not imply strategy effectiveness.
