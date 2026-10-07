# Final Repository Freeze｜最终仓库冻结候选记录

## 1. Status

- `FINAL_REPOSITORY_FREEZE_CANDIDATE`
- `READY_FOR_MAIN_ACCEPTANCE`
- `S11_NOT_YET_DECLARED_COMPLETE`
- S11-38 已完成最终仓库终审，生成 `FINAL_REPOSITORY_FREEZE_CANDIDATE_READY_FOR_MAIN_ACCEPTANCE`。导航中沿用目录提升前的末句已获用户明确授权，只作一行机械更正。最终接受权仍属于 Main。
- 比赛实验保持 CLOSED；本记录不声明最终冻结已接受，也不宣布 S11 COMPLETE。

## 2. Repository Identity

- Repository：`MyKr-YSteinsK/CareerSim-BDCI26`；Windows / PowerShell。
- Audit base：`dbd272640ccf0d77ea83bcf46c8f147b9d5cfb3a`。
- Branch：`main`；opening gate 为 HEAD = origin/main = audit base，tracked worktree clean；暂停后再次 fetch 核对无漂移。
- Freeze-candidate delivery commit：本 Task 的交付 commit，由 TASK_RESULT 和 Git history 报告。本文不尝试包含自身 commit hash。
- 历史说明：`debf5e02e302a720697c95c7286326671e28c8c3` 是 S11-21 的旧冻结候选，后续 S11 重构取代了它；它不是本轮候选身份。旧审查事实仍由历史记录与 Git 保存。

## 3. Final Competition Package

| Field | Frozen value |
|---|---|
| Candidate | `candidate-v6-auditable-control-loop` |
| Runtime source | `1114a04b75548cf52f030d123564e527060fc061` |
| Build/source-material commit | `113052a9a8943efc7fb2d7d1140f126e62e92040` |
| Architecture | Single Agent + 3 Skills |
| Skills | `structured-state-board`、`rolling-planning`、`risk-review` |
| ZIP filename | `FZU-Loss-final-v6.zip` |
| Bytes / files | 18,082 bytes / 7 files |
| SHA-256 | `31e836b591703dfe520916828da033a57de260bb451d97047bbaee9daaa11b9b` |
| Official upload | `NOT PERFORMED / NOT PROVEN` |
| Official platform score | `UNKNOWN` |

来源：[提交身份](FINAL_SUBMISSION_IDENTITY.json)、[构建 manifest](FINAL_SUBMISSION_MANIFEST.md)、[最终方案审阅](FINAL_SOLUTION_REVIEW.md)与[人读交付报告](../final-report/04-最终方案、候选选择与工程交付.md)。本轮只读核对本机原 ZIP 大小与 SHA-256，结果为 `AVAILABLE_AND_MATCHED`；没有打开成员、解包、重建、重压缩或修改工件。七成员依据冻结 manifest，不冒称本轮重新枚举归档成员。

只读 Git 检查确认：历史 runtime manifest 与 Instruction hash 匹配冻结身份，三个 Skill blob 匹配且可读，build commit 中 README 与两份 design 材料存在。该来源检查没有运行 builder、安装 helper、环境 validator 或模型。

## 4. Current Checkout Caveat

`configs/current_candidate.json` 与 `configs/runtime_manifest.json` 仍标识历史 `candidate-v8a-v7o-donor-core-transplant`。当前工程含四个 Skill：`structured-state-board`、`rolling-planning`、`delivery-progress`、`risk-review`。

**engineering checkout != frozen submission package identity**。该区别已在 [CURRENT_STATE](CURRENT_STATE.md)、[README](../../README.md)、[最终方案审阅](FINAL_SOLUTION_REVIEW.md)及正式报告披露。冻结仓库不把 checkout 切成 v6，不变更 Candidate、Instruction 或 Skills。

## 5. Final Evidence Boundary

| Evidence | Observed result | Boundary |
|---|---|---|
| exact-v6 / RUN-0001 | `75.29 / 52.70 / 48m / A / L6`；promotions M6/M12/M18/M36/M48 | `VALID_48M_COMPLETION` 与 `RUNTIME_ADHERENCE_FAIL` 同时成立；只有 one accepted complete sample |
| Candidate v1 同源两局 | `76.04 / 48m / A / L6`；`35.31 / 25m / D / L4` | Tier-B summary；raw unavailable、完整 Instruction 身份不全；不能只选高局 |
| v8a / RUN-0004、RUN-0002 | `72.65 / 50.86 / 48m / A / L5`；`59.00 / 41.30 / 48m / C / L4` | same frozen behavior identity 的两条轨迹；有 runtime/evidence 限制，非 exact-v6 replication 或因果对照 |

exact-v6 已记录的执行缺陷继续公开保留：Energy 多选 schema rejection；半年度必需 H checkpoint marker 遗漏；ordinary Story 在无新公开证据时重开 deliberation；CTRL/action auditability ambiguity；两个 compression epoch 后未按合同 reread 三个 Skills。没有新增缺陷，也没有用完整通关覆盖遵循失败。

`stable 75+ = NOT PROVEN`；`expected score = UNKNOWN`；`causal strategy advantage = NOT PROVEN`；`hidden-test transfer = UNKNOWN`；`theoretical optimum = NOT CLAIMED`。不声称获奖、TOP5、排名、官方分数或上传成功。

负向/替代路线保持原测试范围：

| Route | Accepted boundary |
|---|---|
| Reviewer | `REVIEWER_NOT_SAFELY_DEPLOYABLE` 仅针对 tested frozen path；未否定 Reviewer 普遍价值 |
| Memory | `MEMORY_NOT_DEPLOYABLE` 仅针对 automatic MEMORY.md anchor；explicit read worked |
| Deterministic helper | `DETERMINISTIC_HELPER_CHALLENGER_SUPPORTED` 仅 isolated tool-level support；没有正式 Candidate 部署 |
| Replay controller | `CONTROLLER_LOGIC_SIGNAL_WEAK` / `NOT_PROMISING` |
| Strategy mining | `STRATEGY_SIGNAL_WEAK`；confounded descriptive signal |
| Simulator policy search | `SIMULATOR_POLICY_SEARCH_NOT_FEASIBLE` 是 feasibility failure，未比较宏策略 |
| Team / Swarm | `DEFERRED / NOT_TESTED` |
| Human Play Lab | `CLOSED_BY_USER`；closure reason = `UNKNOWN` |

事实由[最终证据审阅](FINAL_EVIDENCE_REVIEW.md)、[最终方案审阅](FINAL_SOLUTION_REVIEW.md)、[运行历史](RUN_HISTORY.md)、[实验复盘](EXPERIMENT_RETROSPECTIVE.md)与[v6 原始验证记录](runs/v6-run1-validation.md)交叉核对。

## 6. Human-readable / Teaching Layer

- 正式 [Final Report 阅读导航](../final-report/00-阅读导航.md)：`docs/final-report/00–05`，恰好六篇。S11-34 已完成 11 → 6、正式提升、引用迁移和旧层退役；`docs/final-report-v2/` 不存在。
- 教程四条入口均存在，导航链接可解析：[Track A](../tutorial/track-a-skill/00-学习地图.md) 9 篇、[Track B](../tutorial/track-b-system-runtime/00-学习地图.md) 11 篇、[Track C](../tutorial/track-c-repository-tooling/00-学习地图.md) 13 篇、[Track D](../tutorial/track-d-project-method/00-学习地图.md) 15 篇，共 48 篇。
- [Skill Evolution 版本索引](../skill-evolution/00-版本索引.md)：七组代表原件与 GUIDE，包含 v3c、v4、v5、exact-v6、v7、v7c、v8a，共 54 个 Markdown 文件；SOURCE/DELTA/GUIDE 均存在。
- baseline/v1 完整原文身份及其他 Known Gaps 原样保留；没有重新考古恢复或补造。报告解释不覆盖 canonical engineering evidence，教程不增加独立样本数。

## 7. Repository Cleanup / Retention Decision

- S11-34：旧十一篇报告层已退役，current tree 只保留六篇正式报告。
- S11-35：`tracked SAFE_DELETE_NOW = 0`。
- S11-37：原 shortlist 17/17 已作高推理审查；`SAFE_DELETE_NOW HIGH = 0`、`SAFE_DELETE_NOW MEDIUM = 0`；`AUTO_DELETE_READY = NONE`、`MAIN_APPROVAL_DELETE = NONE`。这是 17-path scope 的结果，不是全仓数学最小证明。
- **No further tracked cleanup is authorized by current evidence.** Tracked repository cleanup stops here under current evidence；没有重新寻找删除候选。

S11-36 的五组 local-only 清理因执行工具 policy 阻塞未执行。本轮仅按 metadata 复核它们仍为 ignored/untracked、非 canonical、不属于最终仓库身份：

| Local-only path | Files | Bytes |
|---|---:|---:|
| `.pytest_cache/` | 5 | 143,519 |
| `.local/scratch/__pycache__/` | 1 | 21,992 |
| `.local/scratch/s11-28-track-c-source-pack/` | 7 | 49,220 |
| `.local/scratch/s11-30-track-d-source-pack/` | 8 | 67,249 |
| `.local/scratch/s11-32-report-consolidation/` | 8 | 44,116 |
| Total at audit | 29 | 326,096 |

分类：`NON_BLOCKING_LOCAL_RESIDUE`。这些计数只描述审查时点的本地残留，cache 后续可变，不是 frozen tracked identity。未重试删除，也不把 policy 阻塞误写成已经清理。ignored local cache/source-pack residue may remain。

## 8. Hold / Accepted Unknowns

- 当前台账：20 named active/pending holds，18 `KEEP_ACTIVE`、2 `UNKNOWN_REVIEW_REQUIRED`、0 releasable；`HOLD_RELEASE_COUNT = 0`。
- `RUN-0001` exact-v6 raw formal hold status = `UNKNOWN`；legacy aggregate overlap/member uniqueness 未完全建立；v7o hold membership 部分未知；S10-21 local hold path = `UNKNOWN`。两条 sentinel 不增算为新的独立具名 hold。
- 历史 `S03-MCP-REGISTRATION=RELEASED_BY_MAIN` 保持历史事实；20 份 S03 session payload 仍按[工作区退役记录](LOCAL_WORKSPACE_RETIREMENT.md)保留并受 hold 约束。
- 官方上传未执行/未证明、platform score/hidden-test transfer/expected score 未知、因果优势未证明、Team/Swarm 未测试及 HPL 关闭原因未知，均披露而未伪装为 resolved。
- 报告合并、Git 可恢复代码、摘要已吸收或文件 hash 均不替代 held raw，不自动满足 release conditions。原件未读取、修改、compact、移动或删除。

## 9. Integrity Verification

审查基线的工作区逻辑大小如下；不是 ZIP 大小，也不是 Git 压缩对象大小。文档交付后的最新 bytes 由 TASK_RESULT 给出，不做递归 self-hash。

| Area | Tracked files | Markdown files |
|---|---:|---:|
| Entire repository | 385 | 253 |
| docs/final-report | 6 | 6 |
| docs/tutorial | 48 | 48 |
| docs/skill-evolution | 54 | 54 |
| docs/project | 144 | 125 |
| scripts | 17 | 0 |
| tests | 21 | 0 |
| experiments | 13 | 8 |
| artifacts | 39 | 0 |

Audit base tracked worktree bytes：24,997,022。

- Identity：CURRENT_STATE、freeze record、FINAL_SUBMISSION_IDENTITY、FINAL_SUBMISSION_MANIFEST、FINAL_EVIDENCE_REVIEW、FINAL_SOLUTION_REVIEW、final-report/01 与 /04 的角色/精确值核对一致。旧 freeze 状态与报告导航写作阶段措辞另按当前/历史语境审查，不覆盖冻结材料身份。
- ZIP：原工件只读大小/hash匹配；七成员身份沿用 canonical manifest。
- Tests：已读 `tests/test_candidate_v7s_contract.py`，四项仅以 json/Path 读取合同、治理文本、当前/最终身份与 builder 源码；不 import Runner、不执行 builder、不接触 DB/provider/service/MCP。选择该文件的 4 项静态治理测试，4 passed / 0 failed / 0 skipped。禁用第三方 pytest plugin autoload、cacheprovider 和字节码写入；因未加载 asyncio plugin，有一条既存配置选项 warning，不涉及测试失败。
- Markdown：全 253 tracked Markdown 使用 CommonMark parser 扫描实际文件链接与 fragment，GitHub-compatible heading slug 含重复标题处理；1,383 个本地文件链接、9 个 fragment，broken file links = 0、broken anchors = 0；58 个外部 URL 未联网验证。scope/diff 和交付核验见 TASK_RESULT。
- Stale paths：未发现 retired old report links 或 final-report-v2 links；只修 current-facing 状态，不改历史 run/review/research。
- 仅当允许范围内的修正、全部链接与 diff 检查通过，并完成一个 coherent commit/push、HEAD=origin/main 和 clean 复核，才交付 READY 候选。

## 10. Protected Boundaries

本记录的仓库冻结候选只涉及 tracked main 与已披露的 local/canonical caveats，不改变比赛 ZIP。比赛实验 CLOSED；gameplay、provider、MCP、service lifecycle、install、DB query、replay、new Candidate、ZIP rebuild 均为 0。

本轮不修改 runtime、configs、Skills、Runner、scripts、tests、experiments、artifacts、submission_materials、Tutorial、Skill Evolution 或历史 run/review/research。`docs/final-report/00-阅读导航.md` 仅在用户明确批准的单行例外下，修正目录提升前的过期状态；其余报告正文不改。没有 tracked/local delete、move、rename、branch/worktree cleanup 或 hold release。

## 11. Main Acceptance Boundary

本 Task 的交付为 `FINAL_REPOSITORY_FREEZE_CANDIDATE = READY_FOR_MAIN_ACCEPTANCE`；`S11_COMPLETE = NOT_DECLARED`。Main 对最终仓库状态的接受权独立于本 Task 的文档修正及静态 PASS；本记录不授予清理、运行、上传或改包权限。

终审范围、静态检查、known unknowns 与 local residue 已披露。只有 Main 可以接受此候选并决定 S11 closeout；Codex 不自行宣布 `FINAL_REPOSITORY_FREEZE_ACCEPTED` 或 S11 COMPLETE。
