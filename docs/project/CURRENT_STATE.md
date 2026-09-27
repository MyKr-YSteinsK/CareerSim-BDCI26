# CURRENT_STATE

> 当前事实快照；阶段过程由 Git 历史和关键对局索引承载，不在此追加流水。

## Project

- Repository: MyKr-YSteinsK/CareerSim-BDCI26
- Branch: main
- Current Stage: `S07-Lab｜合规黑盒策略探针与稳定高分搜索` ACTIVE；S06 COMPLETE
- S01–S05: COMPLETE；S05 final offline candidate: candidate-v2-final-offline；acceptance: PASS_WITH_KNOWN_LIMITATION
- S06: COMPLETE；Main acceptance=`PASS_WITH_KNOWN_RUNTIME_LIMITATION`。S06-24 原 v6 完成一局 `75.29 / 52.70 / 48m / A` 的 `VALID_48M_COMPLETION`，但 `RUNTIME_ADHERENCE_FAIL`；S06-25 形成 `candidate-v6b-runtime-correctness`，仅修 runtime/audit correctness，v6b 为 `STATIC_CORRECTNESS_PATCHED / NOT_RUNTIME_VALIDATED`。Design Freeze=ACTIVE。
- S07-01: `COMPLETE / QUARANTINE_FOR_MAIN_REVIEW`; Main disposition=`SURGICAL_COMPLIANCE_CLEANUP_REQUIRED`. S07-02 Main review=`PASS`; descendant `candidate-v6c-compliance-cleanup` was accepted as the static candidate before S07-23. W1 compliance quarantine is resolved for the identified narrow clauses; W2 Cheap Probe Feasibility and W3 Mid-70 Basin Diagnosis are now UNBLOCKED but NOT_STARTED.
- S07-22 Main accepted the global-trajectory / delivery-lifecycle architecture for implementation. S07-23 completed Candidate v7 static implementation; S07 remains ACTIVE and this is not a stage-completion decision.
- S07-24 completed the bounded static Promotion Frontier refinement as Candidate v7a; it does not authorize runtime validation or complete S07.
- S07-25 completed the bounded static, event-agnostic Story semantic refinement as Candidate v7b; v7b is NOT_RUNTIME_VALIDATED and does not authorize runtime validation or complete S07.
- S07-26 completed Candidate v7c's static global decision hierarchy and progressive-disclosure refinement. It uses public Level tenure only as optional qualitative context, adds review realization, time-to-realization and commitment congestion reasoning, and retains the four-Skill architecture. v7c is NOT_RUNTIME_VALIDATED; S07 remains ACTIVE and NEXT_GAME = NOT_AUTHORIZED.
- S07-27 completed the bounded static strategic-continuity refinement as Candidate v7d. Planning owns a recoverable Active Review Plan with evidence-gated revision; Output is an explicit public progression signal; Layer 6 has a narrow Value of Information prior. AD-002's stale current-Candidate claim is marked historical. Runtime/provider/gameplay remain NOT_VALIDATED; S07 remains ACTIVE and NEXT_GAME = NOT_AUTHORIZED. Next recommendation: S07-28 Runtime Readiness Gate, with no live authorization implied.
- Last verified: 2026-09-27

## Current candidate

- Current Candidate: `candidate-v7d-strategic-continuity`；parent: `candidate-v7c-global-decision-policy`；S07-27 static refinement, `STATIC_IMPLEMENTED_NOT_RUNTIME_VALIDATED`. Canonical identity is `configs/current_candidate.json`; v7c is the direct parent, v7b the prior strategy ancestor, and v7 the immutable four-Skill architecture parent. No gameplay/provider evidence transfers from earlier candidates automatically.
- Canonical identity: [current_candidate.json](../../configs/current_candidate.json)
- Rebuildable runtime manifest: [runtime_manifest.json](../../configs/runtime_manifest.json)
- Four Skills: structured-state-board, rolling-planning, delivery-progress, risk-review
- Architecture: Single Agent is the only action submitter; Board owns current public facts, Planning owns the long-horizon strategy, Delivery owns a bounded current-session public lifecycle, and Risk gates the current candidate
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
- v6b, v6c, v7, v7a, v7b, and v7c have no gameplay/provider validation transferred from earlier candidates. Runtime adherence, gameplay effectiveness, survival/score improvement, stable quantitative 80+, and hidden-test transfer remain NOT_PROVEN for v7c.
- Gameplay effectiveness: NOT_PROVEN；survival improvement: NOT_PROVEN；score improvement: NOT_PROVEN；stable quantitative 80+: NOT_PROVEN；hidden-test transfer: NOT_PROVEN.
- S06-24 local raw evidence was consulted read-only for S06-25 fact corrections and remains uncommitted; this state snapshot does not assert a canonical raw hash.

## Authorization

- TARGET: STABLE_QUANTITATIVE_80_PLUS (goal only; not achieved fact)
- NEXT_GAME: NOT_AUTHORIZED; the S06-24 one-game authorization is consumed. Any further benchmark requires a separate Main Game Gate.
- S06 Main acceptance: `PASS_WITH_KNOWN_RUNTIME_LIMITATION`; S06=`COMPLETE`. S07-02 Main acceptance=`PASS`; S07-22/23 completed the v7 static design/implementation, S07-24 the bounded v7a refinement, S07-25 the bounded v7b refinement, S07-26 the v7c hierarchy, and S07-27 the v7d continuity refinement. W2/W3 remain separate and unstarted under the AD-007 public-interface evidence firewall. No Team/Swarm, Memory, fifth Skill, provider/gameplay, or Game Gate authorization. Design Freeze remains ACTIVE; S07 remains ACTIVE; NEXT_GAME remains NOT_AUTHORIZED.
- S03-MCP-REGISTRATION forensic hold: RELEASED_BY_MAIN. This does not imply strategy effectiveness.
