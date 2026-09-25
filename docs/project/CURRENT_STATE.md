# CURRENT_STATE

> 当前事实快照；阶段过程由 Git 历史和关键对局索引承载，不在此追加流水。

## Project

- Repository: MyKr-YSteinsK/CareerSim-BDCI26
- Branch: main
- Current Stage: `S07-Lab｜合规黑盒策略探针与稳定高分搜索` ACTIVE；S06 COMPLETE
- S01–S05: COMPLETE；S05 final offline candidate: candidate-v2-final-offline；acceptance: PASS_WITH_KNOWN_LIMITATION
- S06: COMPLETE；Main acceptance=`PASS_WITH_KNOWN_RUNTIME_LIMITATION`。S06-24 原 v6 完成一局 `75.29 / 52.70 / 48m / A` 的 `VALID_48M_COMPLETION`，但 `RUNTIME_ADHERENCE_FAIL`；S06-25 形成 `candidate-v6b-runtime-correctness`，仅修 runtime/audit correctness，v6b 为 `STATIC_CORRECTNESS_PATCHED / NOT_RUNTIME_VALIDATED`。Design Freeze=ACTIVE。
- S07-01: `COMPLETE / QUARANTINE_FOR_MAIN_REVIEW`; Main disposition=`SURGICAL_COMPLIANCE_CLEANUP_REQUIRED`. S07-02 Main review=`PASS`; descendant `candidate-v6c-compliance-cleanup` is accepted as the current static candidate. W1 compliance quarantine is resolved for the identified narrow clauses; W2 Cheap Probe Feasibility and W3 Mid-70 Basin Diagnosis are now UNBLOCKED but NOT_STARTED.
- Last verified: 2026-09-26

## Current candidate

- Current candidate: candidate-v6c-compliance-cleanup；parent: candidate-v6b-runtime-correctness；S07-02 static compliance cleanup only, NOT_RUNTIME_VALIDATED. v6b remains the frozen parent identity in Git history. The original v6 gameplay evidence does not transfer to v6b or v6c automatically.
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
- S06 Main acceptance: `PASS_WITH_KNOWN_RUNTIME_LIMITATION`; S06=`COMPLETE`. S07-02 Main acceptance=`PASS`; current static candidate=`candidate-v6c-compliance-cleanup`. W2/W3 may proceed under AD-007 public-interface-only evidence firewall. No strategy redesign, Team/Swarm/Memory/fifth Skill reopening, provider/gameplay, or Game Gate authorization. Design Freeze remains ACTIVE; NEXT_GAME remains NOT_AUTHORIZED.
- S03-MCP-REGISTRATION forensic hold: RELEASED_BY_MAIN. This does not imply strategy effectiveness.
