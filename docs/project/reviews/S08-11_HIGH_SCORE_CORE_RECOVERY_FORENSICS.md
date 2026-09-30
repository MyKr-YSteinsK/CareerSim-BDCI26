# TASK_RESULT｜S08-11 High-Score Core Recovery Forensics

## 1. 结论与身份

- **Status:** `OFFLINE_FORENSICS_COMPLETE`
- **唯一 Final Decision:** `HIGH_SCORE_CORE_RECOVERY_DESIGN_READY`
- **基线：** `main@86e90406d9f465215c61619898e71f7acdf1e2a9`，与任务开始时 `origin/main` 一致；开始时 working tree clean。
- **当前 Candidate：** `candidate-v7v-preflight-ordering-repair`，未改变。v7w 只是一份设计提案，没有实现。
- **任务类型：** offline Strategy Donor Attribution。Provider、服务、MCP、DB、Runner、game、Candidate/Skill/manifest/runtime/retry 修改均为 0。
- **对局授权：** `NEXT_GAME=NOT_AUTHORIZED`；本任务没有消费或产生任何对局授权。
- **Plan 副本：** `D:\CS\temp\CareerSim\S08-11-High-Score-Core-Recovery-Forensics.md`，16,916 bytes，SHA-256 `32262b4d28c19c718dc5597003054025443fbfc77f7e10a8258458ab251347df`。

## 2. 范围、证据规则与来源

本复盘只消费四个明确 Run 的 Candidate Git 内容、已有正式 Run 报告/归档，以及 v6 的 session-bound 原始 events。公共 action-stream 只提取 `take_action` 的合法选择、对应选择集合、同一局的公开状态白名单和公开前后状态；不读取 action notes、transcript 推理内容、event 描述/ID、隐藏值、内部 score 字段、Provider/服务/DB 数据。新输出不保存 session ID。

| Run | Candidate source commit | events 来源 / bytes / SHA-256 | 公开结果（descriptive） |
|---|---|---|---|
| v6 | `1114a04b75548cf52f030d123564e527060fc061` | 本机精确 run window；2,061,570；`2cce87eb6afd8aea5a9651f75621ae7c2b303e8c00c7f2ac417dc65c030371d8` | 75.29 / 52.70 / 48m / A / L6；promotion M6/12/18/36/48 |
| v7o | `b2e7ea6441da9c314d8a0ffbf29b9d5800ced10d` | `artifacts/dev-runs/s08-run01-v7o/events.jsonl`；2,067,779；`b6eb500f9e8ad3966e595e65a5d558c2c8b50097bf908fd8b93a1b5f14567df4` | 71.83 / 50.28 / 48m / A / L5；promotion M6/12/18/36 |
| v7t | `e4ec82958ccfcac23ca8b28af14e69be1c470fa2` | `artifacts/dev-runs/s08-run03-v7t/events.jsonl`；1,892,046；`c630579d5ebbcdbcecf9f6eee1104434b75cb92a9f3915cdbf4a5c1084e21fdb` | 65.71 / 46.00 / 48m / B / L5；promotion M6/12/30/48 |
| v7v | `fd30db289d4c16fbcd587bb61b40cb0117cab396` | `artifacts/dev-runs/s08-run04-v7v/events.jsonl`；2,066,164；`646af2df08655410bd0aa3b046983ac1be5797d2332682f7669c9756c55780b4` | 58.97 / 41.28 / 48m / C / L5；promotion M6/18/30/48 |

Score order is descriptive only. Each Candidate has one selected Run here, the runs are not a controlled experiment, and different runtime/adherence facts remain material. v6 public final Wealth is 39; its score report separately gives raw Wealth 39.5. These source values are not merged.

The script re-extracted 204/203/190/205 observes and 203/205/207/204 action attempts for v6/v7o/v7t/v7v respectively. Successful `take_action` counts were 202/205/207/204; v6 additionally has one unknown result and one action without an explicit session argument, bound only to the immediately preceding same-session observe. Action→observe boundary omissions were 0/0/18/0. The v7t result agrees with its prior exact-session forensics; v7v has the observed 204/204 boundary sequence.

## 3. Early promotion evidence

Review grades for v6/v7o were not retained in the formal validation reports and are `UNKNOWN`; final grade is not substituted for checkpoint grade. Public status values below are the last same-month public observations in events, formatted `Level; Skill/Network/Output; Wealth`.

| Run | M6 | M12 | M18 | Promotion pattern |
|---|---|---|---|---|
| v6 | L2; 11/3/5; W3 | L3; 23/8/7; W4 | L4; 38/19/17; W8 | M6→L2, M12→L3, M18→L4 |
| v7o | L2; 11/7/5; W3 | L3; 24/5/9; W5 | L4; 37/18/19; W8 | M6→L2, M12→L3, M18→L4 |
| v7t | L2; 14/7/5; W3 | L3; 22/8/7; W5 | L3; 42/17/10; W8 | M6→L2, M12→L3; no M18 promotion |
| v7v | L2; 13/7/4; W1 | L2; 21/6/5; W3 | L3; 27/11/10; W4 | M6→L2, no M12 promotion, M18→L3 |

Checkpoint review reports: v7t M6 C/promoted, M12 B/promoted, M18 B/no promotion; v7v M6 C/promoted, M12 C/no promotion, M18 B/promoted. v7q is contextual only: C/L1 through M18 and natural elimination at M24. The comparable early chain is strongest in v6/v7o, mixed in v7t/v7v, and failed in v7q. Do not infer hidden promotion thresholds or treat public stat snapshots as the promotion formula.

**Classification for the cross-run early-promotion donor signal:** `PARTIALLY_RESTORED`. The strongest public donor pattern is the v6/v7o sequence of three consecutive early promotions and continued broad growth. v7t/v7v still show that a promotion-first engine can reach later levels after a missed checkpoint, but not the same early cadence.

## 4. Public action mix and marginal response

### Main actions and Energy allocation

Main choices in M1–18 were: v6 6/6 Apply; v7o 6/6 Apply; v7t 4 Apply + 2 mentor; v7v 4 Apply + 1 report + 1 other. Across the entire 48 months, Apply counts were v6 14/16, v7o 10/16, v7t 14/16, v7v 14/16. Thus Apply frequency alone is not monotonic with score.

Energy counts below are `Output visibility / Network / Skill / Health recovery / Risk cleanup / Other or dignity recovery`; total Energy actions are shown in parentheses.

| Run | M1–18 | M19–36 | M37–48 | Overall Output Energy share |
|---|---|---|---|---:|
| v6 | 5/2/0/4/1/3 (15) | 6/4/0/4/0/2 (16) | 4/2/0/2/1/1 (10) | 15/41 = 36.6% |
| v7o | 9/3/0/6/0/0 (18) | 4/4/3/4/0/0 (15) | 7/1/1/2/0/0 (11) | 20/44 = 45.5% |
| v7t | 7/2/0/5/2/0 (16) | 8/5/0/5/0/0 (18) | 9/1/0/2/0/0 (12) | 24/46 = 52.2% |
| v7v | 4/2/0/6/1/2 (15) | 12/0/0/4/1/0 (17) | 8/0/0/2/1/0 (11) | 24/43 = 55.8% |

v6/v7o have the highest overall scores despite lower Output Energy shares than v7t/v7v. This rejects a simplistic “more Output actions → higher score” reading. v7v shifted strongly toward Output in M19–48, but only has two explicit `REVIEW_PLAN` blocks, both M6→M12; later plan continuity is not established. v7t has an explicit continuity claim across M6–M48 in its report, yet later promotion timing and score do not recover to v6/v7o. Planning continuity and ranking quality should therefore be measured separately.

### Public before/after response associations

| Choice family | v6 | v7o | v7t | v7v |
|---|---:|---:|---:|---:|
| Output report preparation | 12 GAIN / 3 NO_GAIN | 17 / 3 | 5 / 5 / 14 unattributable | 19 / 5 |
| Network maintenance | 6 GAIN / 2 NO_GAIN | 6 / 2 | 5 / 2 / 1 unattributable | 0 / 2 |
| Health recovery | 10 GAIN | 12 GAIN | 9 GAIN / 3 unattributable | 10 GAIN / 2 NO_GAIN |
| Explicit Skill learning | 0 observed | 4 GAIN | 0 observed | 0 observed |

These are same-session adjacent public-status associations against advertised dimensions, not isolated causal effects. v6 “high-intensity work” stays `OTHER`; it is not reclassified as Skill growth. v7t's 14 unattributable Output pairs arise from the known missing-observe windows and are excluded from gain/no-gain claims. A few NO_GAIN examples in later runs show why local marginal response should be refreshed and routed around without mechanically erasing other advertised dimensions.

## 5. Candidate evolution and complexity attribution

| Transition | Relevant delta | Classification |
|---|---|---|
| v6→v7o | Promotion-first/survival floor, broad S/N/O Main prior, clearer public review window; also whole-game persistence and MODE/binding-constraint wording | Strategy + runtime + correctness confounded; not a clean score experiment |
| v7o→v7q | Explicit Primary Gap, next Review as checkpoint, direct gap path, local NO_GAIN discount | Strategy ranking change |
| v7q→v7r | Poor grade/no promotion alone stays MODE=A; public-warning bounded cleanup and delivery-certainty preferences | Strategy safety / recovery clarification |
| v7r→v7s | Chinese recovery taxonomy and bounded recovery/exit semantics | Recovery controller / contract change |
| v7s→v7t | Consume visible event/choice semantics; NO_GAIN excluded from forced coverage; repeated risk cleanup needs fresh same-class evidence | Narrow execution-semantic change |
| v7t→v7u | One action per fresh observe, refresh/replan after NO_GAIN, executable handoff protocol | Runtime protocol change |
| v7u→v7v | Manifest-only acyclic READY/PREFLIGHT ordering repair; four Skill blobs unchanged | Runtime ordering change only; no strategy Skill delta |

The coarse complexity proxy rose from v6's 943 instruction characters / 1,624 manifest bytes / 3 Skills totaling 14,623 bytes / 26 unique uppercase markers to v7u/v7v's 5,194/5,122 instruction characters / 7,627/7,405 manifest bytes / 4 Skills totaling 24,303 bytes / 69 markers. Marker count is a lexical proxy, not a cognitive-load measurement. There are only four selected score observations, candidate/runtime changes are confounded, and token use does not establish a monotonic attention penalty.

**Attention dilution:** `PLAUSIBLE_HYPOTHESIS; NOT_SUPPORTED_AS_CAUSE`. The strategy's complexity increased while later selected scores were lower, but that temporal pattern is not causal evidence. v7v shares all four strategy Skill blobs with v7u; its only Candidate change is the manifest ordering repair. This makes it especially important not to attribute v7v's 58.97 score to a strategy Skill regression that did not occur.

The v6/v7o early sequence plus the mixed v7t/v7v cadence is enough to formulate a bounded strategy-core experiment, but not enough to declare that complexity caused the score gap. Runtime correctness is a separate axis: v7v observed 204/204 action→observe boundaries, while v7t omitted 18. Keep that execution shell stable during any future strategy comparison.

### Score Ceiling Evidence

The best observed ceiling in these selected runs is v6 at 75.29 / A / L6, followed by v7o at 71.83 / A / L5. Both promoted at M6/M12/M18; v6 later reached L6 at M48. This is evidence that the early promotion chain and continued compounding co-occur with the stronger outcomes, not proof they caused them. Output Energy share is lower in v6/v7o than in v7t/v7v, so “maximize Output” is not supported as a general recovery recipe. No selected run is 80+, and no stable 80+ claim is made.

### Failure Floor Evidence

The selected v6/v7o/v7t/v7v runs all survived 48 months; v7t and v7v reached L5 despite weaker scores and missed promotion windows. In v7t/v7v reports, poor review outcomes generally remained in MODE=A; acute public resource symptoms received bounded stabilization and returned to A, public risk warnings authorized bounded cleanup, and a near-term delivery concern was contained without abandoning progression. This supports a plausible “recovery floor” design to preserve, but not a causal score or survival gain. v7q is the contrasting failure case (24-month natural elimination at L1/E); the exact terminal cause is unresolved, so this evidence does not distinguish a strategy deadlock from an unrecoverable trajectory. The first visibly weak promotion window is M6–M18; causal attribution remains UNKNOWN.

## 6. Proposed next design: `candidate-v7w-high-score-core-recovery`

**Status:** design proposal only; no candidate, manifest, Skill, validation flag, or runtime change made. Proposed parent is v7v. Proposed strategy delta is `PROMOTION_FIRST_COMPOUNDING_CORE_WITH_V7V_RUNTIME_SHELL`. Any game experiment needs a new explicit Main authorization.

### Mechanism card 1 — Promotion-first compounding core

- **MECHANISM:** retain promotion-first and a survival floor; use review feedback as a directional gap signal, while preserving broad compounding across responsive Skill/Network/Output paths instead of allowing a single narrow gap to dominate every rank decision.
- **EVIDENCE:** v6/v7o reached L2/L3/L4 at M6/M12/M18; v7t missed M18 after Output-centered windows; v7v missed M12 and promoted at M18. v6/v7o early promotion coincides with more consistent Main Apply during the first three review windows, but v7t/v7v and differing scores prevent a causal attribution.
- **HYPOTHESIS:** a compact broad-growth prior may preserve early promotion momentum while still honoring fresh public review evidence.
- **EXPECTED BENEFIT:** improve the chance of reproducing the early chain and protect the score ceiling.
- **POSSIBLE REGRESSION:** underreact to a genuine narrow Primary Gap or near-term delivery obligation.
- **MINIMAL IMPLEMENTATION:** change Planning ranking language only; keep Primary Gap advisory, retain evidence-backed delivery priority and all public resource/risk recovery boundaries.
- **VALIDATION EXPERIMENT:** after separate authorization, hold v7v runtime shell/Board/Delivery/Risk/Runner/dependencies/retry fixed; change only Planning ranking core. Record M6/M12/M18 promotions, Main/Energy mix, public S/N/O response, survival, score and runtime boundary adherence.
- **DECISION STATUS:** proposed; not implemented; no game authorized.

### Mechanism card 2 — Local NO_GAIN routing with explicit response refresh

- **MECHANISM:** a current-Level NO_GAIN lowers only that dimension/path's marginal priority; refresh public Board response before repeating; retain a multi-dimensional action when another advertised dimension still has value; reset S/N/O responses only on public Level change.
- **EVIDENCE:** later-run report preparation includes NO_GAIN in v7t/v7v, and network/health NO_GAIN appears in v7v; v7t's missing observes make 14 Output pairs unattributable. S08-09 found three repeated Output choices without a recorded current Board `O=NO_GAIN`, so the observed defect can be state handoff rather than absent policy.
- **HYPOTHESIS:** better state freshness and local discounting can reduce repetitive low-return investment without prematurely abandoning a still-responsive compound action.
- **EXPECTED BENEFIT:** less wasted action budget while preserving breadth.
- **POSSIBLE REGRESSION:** noisy adjacent changes could over-discount useful actions.
- **MINIMAL IMPLEMENTATION:** preserve v7v runtime refresh; keep Board schema small and attach evidence freshness to the same Level.
- **VALIDATION EXPERIMENT:** audit every clean advertised S/N/O action as GAIN/NO_GAIN/MIXED_OR_UNATTRIBUTABLE and count immediate same-path repeats after a recorded NO_GAIN.
- **DECISION STATUS:** proposed; not implemented; no game authorized.

### Mechanism card 3 — Keep the runtime shell distinct from strategy ranking

- **MECHANISM:** one successful state-changing action is followed by same-session fresh observe and rebuild before another decision; preserve the v7v READY/PREFLIGHT order and continue through action/month/review closure to structured terminal.
- **EVIDENCE:** v7v has 204 successful actions and 204 observed fresh boundaries; v7t has 18 omitted action→observe boundaries. v7v's strategy Skill hashes are identical to v7u, while only manifest ordering changed.
- **HYPOTHESIS:** a stable shell makes a future Planning-only comparison interpretable.
- **EXPECTED BENEFIT:** isolate strategy outcome from execution-contract failure.
- **POSSIBLE REGRESSION:** extra deliberation may increase token/time use; adherence and cost should be measured from existing Run output.
- **MINIMAL IMPLEMENTATION:** keep runtime and three non-Planning Skills fixed in the experiment; change only Planning ranking language.
- **VALIDATION EXPERIMENT:** require complete action→observe accounting and report runtime adherence separately from score.
- **DECISION STATUS:** preserve as experimental control; not modified by S08-11.

### Mechanism card 4 — Compact review horizon and binding Delivery priority

- **MECHANISM:** persist a concise next-Review target across windows; prioritize Delivery only when evidence shows near-term commitment, blocker, unverified result, or material certainty risk; stop post-terminal-horizon preparation after the final exercised Review.
- **EVIDENCE:** v7v reports only the M6→M12 `REVIEW_PLAN` twice; later continuity is unknown. v7t reports continuity but the score and promotion sequence remain mixed. Both reports retain Delivery uncertainty and boundary limits.
- **HYPOTHESIS:** concise, durable review intent can reduce post-checkpoint or speculative investment while retaining protection for real commitments.
- **EXPECTED BENEFIT:** improve timing and avoid sacrificing progression for low-value late preparation.
- **POSSIBLE REGRESSION:** an overly compact plan may omit a new binding constraint.
- **MINIMAL IMPLEMENTATION:** one Primary Gap, one next checkpoint, one explicit exception for fresh binding Delivery evidence.
- **VALIDATION EXPERIMENT:** after separate authorization, inspect each quarter's actual selected action against the recorded next checkpoint and explicit Delivery evidence; preserve UNKNOWN where absent.
- **DECISION STATUS:** proposed; not implemented; no game authorized.

No fixed answer, event-ID mapping, hidden threshold/cap, action ratio, or score weight is proposed.

## 7. Integrity, verification, and limits

- Reproducible extractor: `scripts/s08_11_high_score_core_forensics.py`.
- Targeted tests: `tests/test_s08_11_high_score_core_forensics.py` — 4 passed.
- Derived JSON: `.local/scratch/s08-11/high_score_core_forensics.json`; ignored local scratch, not committed. It contains only extracted public choices/status and source file metadata; no session ID.
- v6 exact raw events and transcript were scanned using the canonical archive scanner; both passed secret scan and core session consistency. Existing v7o/v7t/v7v official archives remain the source of truth; no raw artifacts were copied or newly archived.
- New extractor, tests, report, and state/history edits pass the canonical secret scan; `git diff --check` passes.
- No changes to `configs/current_candidate.json`, `configs/runtime_manifest.json`, Skills, Runner, dependencies, local retry, validation flags, or `FORENSIC_HOLD` status. Candidate and S08 stage disposition remain with Main/Stage.
- Final restrictions: no live query, no new game, no Provider/service/DB/Runner use, and no implementation of the v7w proposal.

## 8. Final decision

**`HIGH_SCORE_CORE_RECOVERY_DESIGN_READY`**

FACT: public Run and action evidence supports a testable design that combines a broad promotion-first compounding core with the separately fixed v7v runtime shell. INFERENCE: such a design may better preserve both score ceiling and recovery floor. HYPOTHESIS: ranking attention dilution may contribute to inconsistent early promotion, but it is not established as the cause. RECOMMENDATION: Main may decide whether to commission a separately gated Planning-only v7w experiment; this report does not authorize it.
