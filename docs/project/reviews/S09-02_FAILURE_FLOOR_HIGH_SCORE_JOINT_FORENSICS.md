# S09-02｜失败底线 × 高分联合取证

## 1. Run Inclusion Matrix（提取前确定）

任务基线 `main@5bc07edc49bb352a686d13940fb36f78d01ca827`；当前 v7w 不变。所有来源均先从正式记录定位；不查询 DB，不访问 HPL。A = exact-session action stream；B = 已提交报告/历史公开轨迹；C = compact context。B 不生成 action shock 分位数。

| Run / Candidate | score / months / grade / Level | 来源 | Tier / 公开轨迹 | 定量使用与限制 |
|---|---|---|---|---|
| v1 #1 / candidate-v1-four-skill / S04-03 | 76.04 / 48 / A / L6 | Git 8a93378 的 candidate_run1_trajectory.json；RUN_HISTORY | B；49 月状态、16 季度选择 | checkpoint/mix 可用；原路径 raw 已不存在；不计单步 shock |
| v1 #2 / 同一 candidate / S04-04 | 35.31 / 25 / D / L4 | 同一 Git 的 candidate_run2_trajectory.json；RUN_HISTORY | B；7 milestones、8 季度选择 | 与 #1 同 source commit 7a055dea；稀疏状态不插值；不计 shock |
| v6 / candidate-v6-auditable-control-loop / S06-24 | 75.29 / 48 / A / L6 | v6-run1-validation；明确 20260925T094419Z events | A+B | action/window/shock 可用；一个缺 session 参数、一个不明回执；score 文件 session 字段缺陷不扩散到 public trajectory |
| v7o / candidate-v7o-execution-persistence-convergence / S08-RUN01 | 71.83 / 48 / A / L5 | s08-run01-v7o/events.jsonl；正式报告 | A+B | action/window/shock 可用；非受控比较 |
| v7g / candidate-v7g-compact-skill-contracts / S07-33R | 54.52 / 48 / C / L5 | v7g-run1-validation-r2；20260928T055416Z events | A+B | action/window/shock 可用；恢复合同失败，存活不等于遵循 |
| v7i replacement / candidate-v7i-pre-review-result-realization-probe / S07-40 | 64.0 / 48 / B / L5 | Main Raw Re-Audit amendment；正式 manifest 指向 20260928T112740Z events | A+B | 成绩采用 Main 修正，不采用旧 stale-score 段；两个错误路由不当成功动作 |
| v7t / candidate-v7t-execution-semantic-repair / S08-RUN03 | 65.71 / 48 / B / L5 | s08-run03-v7t/events.jsonl；正式报告 | A+B | 18 omitted observe boundaries；批量行动变化只计 mixed |
| v7v / candidate-v7v-preflight-ordering-repair / S08-RUN04 | 58.97 / 48 / C / L5 | s08-run04-v7v/events.jsonl；正式报告 | A+B | 与 v7w runtime lineage 对照；不同随机轨迹，不是策略因果对照 |
| v4 / candidate-v4-lean-runtime-policy / S06-07 | 25.84 / 6 / E / L2 | v4-run1-health-forensic；20260924T160806Z events | A+B | 本次 fresh public raw 核对终局为 L2；score 沿用正式记录（本任务不访问其历史 DB）；Health terminal/action delta 可复析 |
| v7d / candidate-v7d-strategic-continuity / S07-29 | 17.02 / 15 / E / L1 | v7d-run1-validation；20260927T143425Z events | A+B | 一个 schema 拒绝动作；W0 与 public terminal 可复析 |
| v7q / candidate-v7q-checkpoint-marginal-progression / S08-RUN02 | 26.80 / 24 / E / L1 | s08-run02-v7q/events.jsonl；正式报告 | A+B | no-promotion/模式/公开 terminal 可复析 |
| v7w / candidate-v7w-high-score-core-recovery / S09-RUN01 | 30.31 / 24 / D / L2 | s09-run01-v7w/events.jsonl；正式报告 | A+B | 16 不明 action receipts 排除 clean shock；42 late S 不直接归因为终止原因 |

Baseline / SCORE-01 仅作背景，不纳入本 cohort。没有身份明确的额外 failure 样本不补造。Project `05-CODEX_WORKFLOW.md` 不在当前 repo 或指定 Plan 目录；使用已有 AGENTS / CODEX_PLAN_CONTRACT，缺失不产生新权限。此表按 sources 的可用能力制定；统计结果与更严格排除见下文。

## 2. 方法、证据身份与限制

**FACT / MEASURED** 是本次可复算的公开流统计或正式记录；**INFERENCE** 是跨轨迹解释；**HYPOTHESIS** 是待验证的行为机制；**UNKNOWN** 不填补。所有选中局来自同一项目，不能称为 cross-project pattern；共享既有 Prompt 不算独立设计证据。

重现命令（项目根 PowerShell）：

```powershell
& D:/CS/CareerSim/.venv/Scripts/python.exe -m scripts.s09_02_failure_floor_joint_forensics
& D:/CS/CareerSim/.venv/Scripts/python.exe -m pytest tests/test_s09_02_failure_floor_joint_forensics.py -q
```

提取器按 tool-call ID 去重，要求明确 session 参数、成功回执先于 post-observe 调用、单一 action、同月/季度/年/Level，且没有其它不明 mutation、评审结算或 Energy 回补信号。读入公开 current_state.status 白名单、time、current_event.title/description、choices 的 action/description；action notes 仅解析 P/R/RECOVERY 枚举与 REVIEW_PLAN 存在性，不复制推理。忽略 simulation_flags、choice effect 对象、events history、event ID、内部 score 与 provider/service logs。

ACTION_ATTRIBUTABLE 表示流中满足上述可归因条件，仍不能把 stochastic event outcome 与 choice 的确定性效果分离；不是 randomized causal effect。Energy 回补是保守排除线索，不宣称它必定是损失原因。结果缺数值不记 0；不明回执不提升为成功。终局链接来自正式 Run 的 terminal identity 与最后 fresh observe；不把被忽略的 flags 当作新取证来源。

10 局共 1,508 个 action attempts：976 clean、512 mixed、20 unknown。Mixed 是 action-row 数；v7t 的三 action batch 同一累计变化会关联到三行，因此绝不把 mixed 当成独立损失样本计算分位数。Window mix / MODE 以 unique attempts 为分母；known successful allocation 另列，v7w 的不明回执可能包括重复未执行请求，不能解释为实际资源花费。B 局仅用正式聚合，不推导 action delta。

| Run | source | bytes | SHA-256 | O/A | clean/mixed/unknown |
|---|---|---|---|---|---|
| v6 | .career_sim_runner\career_emu\outputs\local-s06-adaptive-controller\20260925T094419Z\events-20260925T094419Z.jsonl | 2061570 | 2cce87eb6afd8aea5a9651f75621ae7c2b303e8c00c7f2ac417dc65c030371d8 | 204/203 | 136/66/1 |
| v7o | artifacts\dev-runs\s08-run01-v7o\events.jsonl | 2067779 | b6eb500f9e8ad3966e595e65a5d558c2c8b50097bf908fd8b93a1b5f14567df4 | 206/205 | 141/64/0 |
| v7g | .career_sim_runner\career_emu\outputs\local-s06-adaptive-controller\20260928T055416Z\events-20260928T055416Z.jsonl | 1903318 | 73cb4de9f2568e343be252630a64dbef289e92aec121bae07ef8fbd3a6cff3c4 | 196/195 | 129/66/0 |
| v7i | .career_sim_runner\career_emu\outputs\local-s06-adaptive-controller\20260928T112740Z\events-20260928T112740Z.jsonl | 2118740 | a1c3bae1b775de9771a1e7ba3bfea4383f684f743b22ecfddd621c4b0399010c | 201/202 | 130/70/2 |
| v7t | artifacts\dev-runs\s08-run03-v7t\events.jsonl | 1892046 | c630579d5ebbcdbcecf9f6eee1104434b75cb92a9f3915cdbf4a5c1084e21fdb | 190/207 | 115/92/0 |
| v7v | artifacts\dev-runs\s08-run04-v7v\events.jsonl | 2066164 | 646af2df08655410bd0aa3b046983ac1be5797d2332682f7669c9756c55780b4 | 205/204 | 138/66/0 |
| v4 | .career_sim_runner\career_emu\outputs\local-s06-adaptive-controller\20260924T160806Z\events-20260924T160806Z.jsonl | 263552 | 9bf8bed1d02435047df40300ff306231dfa938b91cb87d3ef5b082e35d7359e5 | 24/23 | 15/8/0 |
| v7d | .career_sim_runner\career_emu\outputs\local-s06-adaptive-controller\20260927T143425Z\events-20260927T143425Z.jsonl | 756124 | e4e388517aff115747fabe068a76b1bc3d960b43900373d4eca804097348be78 | 60/60 | 39/20/1 |
| v7q | artifacts\dev-runs\s08-run02-v7q\events.jsonl | 1052155 | a183ac4167b21b4afe817698e9d3d431a516934d22ab8191fce8bd56b2573ae9 | 98/97 | 68/29/0 |
| v7w | artifacts\dev-runs\s09-run01-v7w\events.jsonl | 1263074 | 62b4ad52660b0a8fc937aeab2f51c62063d108d4775f90ff253a1ff3c974561e | 113/112 | 65/31/16 |
| v1#1 | 8a93378a8d9ef5598e925048db39ee931e207bab:experiments/S04-04-high-score-confirmation/candidate_run1_trajectory.json | 27518 | d8e82fb4eef186707152c52905821f1950a62a1c3d51e0d3ae09e64b64e04467 | B: no raw | EXCLUDED |
| v1#2 | 8a93378a8d9ef5598e925048db39ee931e207bab:experiments/S04-04-high-score-confirmation/candidate_run2_trajectory.json | 6811 | de787be7819fe437a36f82edf2ebe56d7d5592f54bb9eb4c0241e7f7b63fc689 | B: no raw | EXCLUDED |

全部 10 个 A 源 hash 与此前登记一致。v1 两个 raw 指定路径均不存在，停止该 raw 分支；使用可恢复 Git 对象，不另搜 shared DB 或其它旧 worktree。上述 local raw 的 hash 只是身份核验，不代替原文件，也不解除 FORENSIC_HOLD。完整公开派生数据留在 `.local/scratch/s09-02/failure_floor_joint_forensics.json`，不提交 raw 或新日志。

## 3. Matched trajectory windows

### 3.1 M1–24 共同窗口

状态为窗口内最后公开观察，格式 `L; H/W/D; S/N/O`，不是准确的 Review 瞬间状态。没有到达整段窗口的 v4/v7d 标为 partial，不把它们与完整 6 个月 action rate 比较。v1 #2 缺 M18 状态，保留 UNKNOWN。Main / Energy 给次数与所选 label mix；S share 分母为窗口全部尝试（UNKNOWN 模式不默认为 A）。Grade/feedback 从正式报告另列，不能由这些数值推断。

| Run | window | L; H/W/D; S/N/O | attempts / MODE | Main attempts mix | Energy attempts H/N/O/S/R/D/X |
|---|---|---|---|---|---|
| v1#1 | M1-6 | L2; 7/2/10; 13/5/6 | B / MODE UNKNOWN | Apply:2 | 6 [N:1, O:2, H:3] |
| v1#1 | M7-12 | L3; 7/4/10; 24/7/7 | B / MODE UNKNOWN | Apply:2 | 6 [O:2, H:3, N:1] |
| v1#1 | M13-18 | L4; 10/6/10; 44/19/16 | B / MODE UNKNOWN | Apply:2 | 6 [O:4, N:2] |
| v1#1 | M19-24 | L4; 8/10/10; 63/36/26 | B / MODE UNKNOWN | Apply:2 | 6 [O:4, H:1, N:1] |
| v1#2 | M1-6 | L2; 10/2/10; 12/5/6 | B / MODE UNKNOWN | Apply:2 | 6 [O:2, N:3, H:1] |
| v1#2 | M7-12 | L3; 9/3/10; 24/8/10 | B / MODE UNKNOWN | Apply:1, Avoid:1 | 6 [H:3, O:1, N:2] |
| v1#2 | M13-18 | UNKNOWN (reached; snapshot missing) | B / MODE UNKNOWN | Apply:2 | 5 [H:3, O:1, R:1] |
| v1#2 | M19-24 | L4; 10/9/10; 43/19/13 | B / MODE UNKNOWN | Apply:2 | 4 [R:2, O:1, H:1] |
| v6 | M1-M6 | L2; 6/3/10; 11/3/5 | 26 / MODE UNKNOWN | Apply:2 | 5 [H:2, O:2, R:1]; success=5 |
| v6 | M7-M12 | L3; 5/4/10; 23/8/7 | 25 / MODE UNKNOWN | Apply:2 | 5 [H:1, N:2, X:1, O:1]; success=5 |
| v6 | M13-M18 | L4; 9/8/10; 38/19/17 | 25 / MODE UNKNOWN | Apply:2 | 5 [D:1, H:1, X:1, O:2]; success=5 |
| v6 | M19-M24 | L4; 8/11/10; 61/30/26 | 24 / MODE UNKNOWN | Apply:2 | 4 [X:2, O:2]; success=4 |
| v7o | M1-M6 | L2; 6/3/10; 11/7/5 | 27 / S=0 (0.0%) | Apply:2 | 6 [H:2, N:1, O:3]; success=6 |
| v7o | M7-M12 | L3; 7/5/10; 24/5/9 | 26 / S=1 (3.9%) | Apply:2 | 6 [H:2, N:2, O:2]; success=6 |
| v7o | M13-M18 | L4; 10/8/10; 37/18/19 | 26 / S=1 (3.9%) | Apply:2 | 6 [H:2, O:4]; success=6 |
| v7o | M19-M24 | L4; 10/13/10; 47/32/26 | 26 / S=1 (3.9%) | 建立导师关系:1, Apply:1 | 6 [N:2, O:4]; success=6 |
| v7g | M1-M6 | L1; 5/2/9; 9/3/3 | 25 / S=4 (16.0%) | Apply:2 | 4 [H:2, X:1, R:1]; success=4 |
| v7g | M7-M12 | L2; 4/3/10; 10/6/6 | 24 / S=7 (29.2%) | Apply:2 | 4 [X:1, O:2, R:1]; success=4 |
| v7g | M13-M18 | L3; 7/6/10; 26/6/7 | 24 / S=4 (16.7%) | Apply:2 | 4 [N:1, X:2, O:1]; success=4 |
| v7g | M19-M24 | L3; 8/7/10; 41/19/16 | 25 / S=3 (12.0%) | Apply:2 | 5 [H:2, X:1, O:2]; success=5 |
| v7i | M1-M6 | L2; 7/2/10; 13/4/6 | 27 / S=2 (7.4%) | Apply:2 | 6 [H:2, N:1, O:3]; success=6 |
| v7i | M7-M12 | L3; 8/4/10; 22/9/7 | 25 / S=0 (0.0%) | Apply:2 | 5 [H:1, N:1, X:1, O:2]; success=5 |
| v7i | M13-M18 | L3; 7/6/9; 42/21/16 | 24 / S=1 (4.2%) | Apply:2 | 4 [H:1, X:1, O:1, R:1]; success=4 |
| v7i | M19-M24 | L3; 9/10/10; 42/21/12 | 27 / S=3 (11.1%) | Report:2 | 5 [H:3, O:1, R:1]; success=5 |
| v7t | M1-M6 | L2; 5/3/10; 14/7/5 | 26 / S=0 (0.0%) | Apply:2 | 5 [H:1, N:1, O:2, R:1]; success=5 |
| v7t | M7-M12 | L3; 7/5/10; 22/8/7 | 25 / S=2 (8.0%) | 建立导师关系:1, Apply:1 | 5 [H:2, N:1, O:1, R:1]; success=5 |
| v7t | M13-M18 | L3; 10/8/10; 42/17/10 | 26 / S=0 (0.0%) | 建立导师关系:1, Apply:1 | 6 [H:2, O:4]; success=6 |
| v7t | M19-M24 | L3; 10/11/10; 42/21/14 | 26 / S=0 (0.0%) | Apply:2 | 6 [H:2, N:1, O:3]; success=6 |
| v7v | M1-M6 | L2; 6/1/10; 13/7/4 | 27 / S=0 (0.0%) | Apply:2 | 6 [H:4, N:1, O:1]; success=6 |
| v7v | M7-M12 | L2; 10/3/10; 21/6/5 | 24 / S=1 (4.2%) | Report:1, Apply:1 | 4 [H:1, X:1, O:1, R:1]; success=4 |
| v7v | M13-M18 | L3; 8/4/9; 27/11/10 | 25 / S=0 (0.0%) | 主动曝光成果:1, Apply:1 | 5 [H:1, N:1, X:1, O:2]; success=5 |
| v7v | M19-M24 | L3; 10/6/10; 41/21/13 | 25 / S=0 (0.0%) | Apply:2 | 5 [O:4, R:1]; success=5 |
| v4 | M1-M6 terminal-partial | L2; 0/2/9; 11/7/6 | 23 / MODE UNKNOWN | Apply:1 | 3 [H:1, N:1, O:1]; success=3 |
| v7d | M1-M6 | L1; 9/1/10; 9/3/3 | 28 / A27 S0 UNKNOWN1 | Apply:1, 申请岗位轮岗:1 | 7 [H:2, N:3, X:1, O:1]; success=6 |
| v7d | M7-M12 | L1; 8/-2/10; 9/3/2 | 26 / S=0 (0.0%) | Avoid:1, Apply:1 | 6 [N:2, O:4]; success=6 |
| v7d | M13-M18 partial | L1; 6/0/9; 9/3/2 | 6 / S=0 (0.0%) |  | 0 []; success=0 |
| v7q | M1-M6 | L1; 5/2/10; 9/3/0 | 26 / S=8 (30.8%) | Apply:2 | 5 [H:1, N:1, O:2, R:1]; success=5 |
| v7q | M7-M12 | L1; 5/3/10; 9/3/3 | 26 / S=9 (34.6%) | Apply:2 | 6 [H:2, N:1, O:3]; success=6 |
| v7q | M13-M18 | L1; 9/5/10; 9/3/3 | 26 / S=26 (100.0%) | Apply:2 | 6 [H:1, N:2, O:3]; success=6 |
| v7q | M19-M24 | L1; 8/5/7; 9/0/3 | 19 / S=19 (100.0%) | Apply:1 | 3 [N:2, O:1]; success=3 |
| v7w | M1-M6 | L1; 4/2/9; 9/3/3 | 26 / S=0 (0.0%) | 建立导师关系:1, Apply:1 | 5 [H:2, N:1, X:1, O:1]; success=5 |
| v7w | M7-M12 | L1; 7/3/10; 9/3/2 | 26 / S=2 (7.7%) | 建立导师关系:1, Apply:1 | 6 [H:1, N:2, O:3]; success=6 |
| v7w | M13-M18 | L1; 8/4/10; 9/3/3 | 29 / S=11 (37.9%) | 建立导师关系:1, Apply:1 | 7 [H:3, N:1, O:2, R:1]; success=5 |
| v7w | M19-M24 | L2; 8/6/7; 9/2/3 | 31 / S=31 (100.0%) | Apply:1 | 5 [N:3, O:2]; success=3 |

Energy X = unclassified/high-intensity, not inferred Skill growth. H/N/O/S/R/D are public label categories; share = category count / Energy attempts. All exact ranges and recovery enums are retained in derived JSON.

### 3.2 幸存者 M25–36 / M37–48

只比较幸存轨迹；失败局无机会暴露到这些月份，不能把晚窗幸存者计数与 24m 失败总计作偏好比较。晚窗的最后 M48 状态可能先于行政 M49 终局，所以与正式 final public state 有差异。

| Run | window | last L; H/W/D; S/N/O | MODE attempts | Main mix | Energy mix |
|---|---|---|---|---|---|
| v1#1 | M25-36 | L5; 9/21/10; 100/36/29 | UNKNOWN | Apply:4 | 11 [R:1, H:2, O:7, N:1] |
| v1#1 | M37-48 | L6; 9/39/10; 138/51/40 | UNKNOWN | Apply:4 | 10 [R:2, O:6, H:2] |
| v6 | M25-M36 | L5; 8/22/10; 102/39/24 | {'UNKNOWN': 53} | Avoid:1, Apply:3 | 13 [H:4, N:4, X:1, O:4] |
| v6 | M37-M48 | L6; 7/38/10; 141/57/40 | {'UNKNOWN': 50} | Avoid:1, Apply:3 | 10 [H:2, N:2, X:1, O:4, R:1] |
| v7o | M25-M36 | L5; 10/25/10; 94/38/27 | {'A': 45, 'S': 4} | 建立导师关系:1, Apply:1, 申请岗位轮岗:2 | 9 [H:4, N:2, S:3] |
| v7o | M37-M48 | L5; 9/42/10; 129/51/37 | {'A': 51} | 建立导师关系:2, Apply:2 | 11 [H:2, N:1, O:7, S:1] |
| v7g | M25-M36 | L4; 8/7/9; 63/35/25 | {'A': 36, 'S': 12} | Apply:4 | 8 [H:1, X:3, O:3, R:1] |
| v7g | M37-M48 | L5; 6/18/10; 101/35/30 | {'A': 46, 'S': 3} | Apply:4 | 9 [H:3, X:3, O:3] |
| v7i | M25-M36 | L4; 9/16/10; 72/36/24 | {'A': 50} | Report:2, Apply:2 | 10 [H:2, N:2, O:4, R:2] |
| v7i | M37-M48 | L5; 8/26/10; 109/35/30 | {'A': 49} | Apply:4 | 9 [H:1, N:1, X:3, O:4] |
| v7t | M25-M36 | L4; 10/17/10; 71/34/26 | {'A': 52} | Apply:4 | 12 [H:3, N:4, O:5] |
| v7t | M37-M48 | L5; 10/26/10; 100/37/28 | {'A': 52} | Apply:4 | 12 [H:2, N:1, O:9] |
| v7v | M25-M36 | L4; 10/7/10; 60/27/26 | {'A': 52} | Apply:4 | 12 [H:4, O:8] |
| v7v | M37-M48 | L5; 10/24/10; 99/36/31 | {'A': 51} | Apply:4 | 11 [H:2, O:8, R:1] |

### 3.3 Review / Gap / continuation

| Run | M6 / M12 / M18 / M24 Review 与晋升 | 主 Gap / continuity / Delivery 证据 |
|---|---|---|
| v1 #1 | grade UNKNOWN；promote / promote / promote / no promotion | 3 个 Planning checkpoints，完整连续 Review Plan UNKNOWN；M6 起 S/N/O 广泛增长 |
| v1 #2 | grade UNKNOWN；promote / promote / no promotion / promote | M18 公开状态缺失；末期仍 key project，但 trust terminal；完整 Delivery/Review continuity UNKNOWN |
| v6 / v7o | checkpoint grade UNKNOWN；均 promote / promote / promote / no promotion | 初期 broad growth；v6 普通 deliberation/CTRL pairing 不完全；v7o 连续性见正式记录，不把 score 当 adherence |
| v7g | C/no / C/promote / B/promote / B/no | clearer results，G 在普通 Story 间 churn；Delivery/压缩恢复失败；错过 M6 仍可后续晋升 |
| v7i | C/promote / B/promote / B/no / B/no | 主线晋升保留；pre-review result-realization 真触发为 0；Delivery lifecycle 不持续，Main correction 为权威 |
| v7t | C/promote / B/promote / B/no / B/no | operational progression recovery 多留 A；Review Plan 有报告证据；18 fresh-observe omission；M42 Output 重复 NO_GAIN |
| v7v | C/promote / C/no / B/promote / B/no | 前两个 literal REVIEW_PLAN 均指 M12；后续 exact gap wording UNKNOWN；acute health 后回 A；Delivery safe release containment 有报告证据 |
| v4 | M6 观察 L2；grade UNKNOWN；随即 H0 terminal | 已有 H2 危险/回补；没有持续 Board trend；终局可选项未证实存在 Health 恢复 |
| v7d | M6 C/no；M12 grade UNKNOWN/L1；M15 terminal | M6 后 Network/trust gap，后续 G churn；M14 scheduled delivery 明确，仍申请探索；terminal causation UNKNOWN |
| v7q | M6/M12/M18 C/L1/no；M24 terminal | N/O弱，Skill 停在9；S 延续；确切终止机制 UNKNOWN，不推导 hidden review threshold |
| v7w | C/no / C/no / D/no / C/promote L2 后 terminal | 明确 PROGRESSION 5 次（M6四次/M12一次）未改善下次评审；literal REVIEW_PLAN=0；M18 后无 captured reset；Delivery 42 malformed |

v7w 的 public terminal 由正式记录引述“连续两次半年绩效不佳”；最后 M23→M24 是 mixed transition，H8/W6 未归零。最早可见的 progression 失控是 M1–6 的首 Review，M7–12 未扭转；控制长 S 问题在 M18 后显著出现，不能把它当作 M6 失败的先行原因。Risk recovery 的 public trigger/exit chain 不完整；没有 full Delivery repair chain。

## 4. Failure archetypes 与预警

### Resource floor：v4 与 v7d 不能混成一个 numeric gate

**FACT:** v4 H5→3→2→4→3→4→3→2→1→0，是 cumulative attrition。M3 action 11，fresh H2 时合法 Energy 菜单有健康恢复，实际 H2→4、E3→2；这是早于 M6 terminal 的可见、局部有效恢复机会，不证明再恢复就一定存活。M5 生病同事事件有建议居家办公的合法替代，但其 Health 效果 UNKNOWN；末两次 action 前 H2/H1 已无 Energy，终局两项 choice 都没有公开证实的直接 Health 恢复。不能假设最后一刻一定可救。

手工检查 v4 O108→A109→O115（H2→4），O172→A173→O179（H4→3），O196→A197→O203（H2→1），O204→A205→O211（H1→0，E0→3）；seq 含 duplicate transport，提取器保留首条同 ID 结果。M6 public Level 是 L2，修正本报告 inclusion table 中的 initial L1 假定；一次晋升也不能抵消 resource floor。

**FACT:** v7d M9 W2→0，仍继续；M12 的 last W=-2，M15 terminal W0/H6/L1。故 W0 本身不是可从本 cohort 推导的即时死亡阈值。稀薄 W、无晋升、Delivery压力共同出现；public terminal 的确切机制 UNKNOWN。不能把一次 W2→0 直接叫作致死 action。

**INFERENCE:** 在有合法、低机会成本且当前 public 证据支持的机会时维持 buffer，可能比等 acute terminal 更好。**HYPOTHESIS:** 对 cumulative trend 与当前风险进行短时修复可能提高 failure floor；不支持“所有低数字→长期 S”。

### Trust / compliance / continuity：同 Candidate 的独立失败轴

**FACT:** v1 #1/#2 同 source 7a055dea、同四 Skill Candidate；前两次都在 M6/M12 晋升，#2 M24 仍到 L4，却在 M25 第二次 trust-crisis blowup 终止。#2 M25 H10/D8，不能用增加 Health 解释这次失败。M24→M25 W9→3 是稀疏摘要变化，含多个/自动来源可能性，不计为 W6 单步 shock。

首次 crisis 的精确月份、第一次之后是否已公开授权修复、第二次前最早 warning、可选修复动作与 lead time，在现存 B 来源里 **UNKNOWN**。能确认“重复危机/最终 continuity 失败”的报告结论，不能复原 hidden counter 或假装看过第一条警告。#2 M18/21/24 选过 risk cleanup，仍失败，说明 cleanup 次数不是有效性的证据。

**INFERENCE:** 高增长 cadence 与 trust continuity 应分别评价。**HYPOTHESIS:** 用新鲜公开威胁限定的关系/合规保护，比无条件增加 cleanup 更可能保留 ceiling；本 paired sample 不证明哪项选择导致差异。

### Progression collapse：v7q / v7w

**FACT:** 两局 M6/M12/M18 均未晋升，M18 S/N/O 分别为 9/3/3 与 9/3/3；v7q M24 L1、v7w M24 才 L2。相比 v6/v7o M18 到 L4，差距早已形成。v7q 初期 6/6 Main key projects 却失败，否定“按固定 Main 频次即可复制 donor”。

首个 no-promotion 是诊断信号，而非隐藏失败公式。v7g M6 no-promotion 之后仍存活48m，故不能把一次失败当不可逆。v7w 五个显式 progression recovery 标记只证明曾尝试，后续 C/D feedback 不支持有效恢复。默认用 A 中的 Review 重建与响应路径修复，是设计上有支持的方向；成功收益仍待实验。

### Control / recovery：stale S 与 malformed handoff

| Run | attempts | A | S | S share | max consecutive S |
|---|---|---|---|---|---|
| v6 | 203 | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| v7o | 205 | 198 | 7 | 3.4% | 4 |
| v7g | 195 | 162 | 33 | 16.9% | 8 |
| v7i | 202 | 196 | 6 | 3.0% | 2 |
| v7t | 207 | 205 | 2 | 1.0% | 2 |
| v7v | 204 | 203 | 1 | 0.5% | 1 |
| v4 | 23 | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| v7d | 60 | 59 (UNKNOWN1) | 0 observed | 0/60 observed; UNKNOWN1 | 0 observed; UNKNOWN1 |
| v7q | 97 | 35 | 62 | 63.9% | 52 |
| v7w | 112 | 68 | 44 | 39.3% | 42 |

v6/v4 无 P 枚举，max S 不是0次 S 的行为结论，而是 **UNKNOWN**。v7q 连续52个 S、v7w连续42个 S；v7g最大8、v7i/v7t最大2、v7v最大1。它们是 mode marker 序列，不能把每个 S 都等同休息或放弃成长。

v7w action71（M18）public demo path 过于理想，选择重测/realistic报告本身符合事件语义；H6/D5/W4 与 D feedback 同时出现，进入 S 的独立触发不明。随后 action74 D8、action81 D10、action82 H8/D10、action111 H8/D10，仍 S。后期虽遇到不同 public threats，未见逐次 re-prove、类型切换或 exit evidence。S 内仍选 key projects（81/102），所以“42次完全没成长行动”是错误解释。**SUPPORTED:** mode/exit 证据不充分；**UNKNOWN:** 对 terminal 的 causal contribution。

v7v 的 acute 心悸/胸闷/手抖事件采用一次短 S，观察后回 A，并在下一 review 后继续晋升；其 H6→8 同时跨月，只证明 public recovery sequence，不把+2计 clean causal effect。v7w M10理疗也短暂回 A，说明并非所有恢复路径都锁死。全局标签、实际 choices、harness receipt 与 career result 四层必须分开。

## 5. Empirical Shock Envelope

### 5.1 统计

| Dimension | clean N | loss / zero / gain | 负向损失幅度分布 | median / P75 / P90 / P95 | observed max |
|---|---:|---|---|---|---:|
| Health | 976 | 143 / 713 / 120 | -1:129；-2:14 | 1 / 1 / 1 / 2 | 2 |
| Wealth | 976 | 16 / 935 / 25 | -1:1；-2:14；-4:1 | 2 / 2 / UNKNOWN / UNKNOWN | 4 |

分位数在负变化的正损失幅度上计算，linear interpolation；median/P75 至少5个，P90/P95至少20个。Wealth N=16 不给尾部分位数，以 rank/top-k 为主。Health loss覆盖10局；Wealth loss覆盖7局。976 是公开整数状态变化，不能证明底层小数效果为零，也不能据此推断 cap。样本按 actions 加权，单局内强相关、幸存局机会更多、selected cohort 非随机样本；这些都是描述性经验值，没有置信上界。

#### Health Top10 (clean)

| Run | month/Level | public sequence | family/context | selected legal label | before/after | immediate terminal |
|---|---|---|---|---|---|---|
| v6 | M7 / L2 | A28 / seq 253 to 259 | story: 新同事到岗后的 Mentor 节奏选择 | 高密度带教，确保两周内独立上手 | 6 to 4 (-2) | NO |
| v6 | M28 / L4 | A115 / seq 953 to 959 | story: 重要客户来访的接待形式选择 | A：商务餐厅工作晚餐并陪餐 2 小时 | 10 to 8 (-2) | NO |
| v6 | M31 / L4 | A129 / seq 1061 to 1067 | story: 年度团建组织者报名抉择 | 主动报名担任组织者 | 7 to 5 (-2) | NO |
| v7d | M11 / L1 | A45 / seq 389 to 395 | story: 观察升职靠关系而非能力 | 继续经营关系 | 8 to 6 (-2) | NO |
| v7g | M44 / L4 | A176 / seq 1429 to 1435 | story: 年度团建组织者报名抉择 | 主动报名担任组织者 | 9 to 7 (-2) | NO |
| v7i | M23 / L3 | A95 / seq 777 to 783 | story: 年度团建组织者报名抉择 | 主动报名担任组织者 | 10 to 8 (-2) | NO |
| v7o | M18 / L4 | A74 / seq 613 to 619 | story: 周末厂内高级架构师认证机会 | 利用周末提前推进项目，争取周一上午交付 | 10 to 8 (-2) | NO |
| v7o | M36 / L5 | A149 / seq 1213 to 1219 | story: 观察升职靠关系而非能力 | 学习投入非正式场合，控制底线 | 7 to 5 (-2) | NO |
| v7o | M43 / L5 | A182 / seq 1477 to 1483 | story: 观察升职靠关系而非能力 | 学习投入非正式场合，控制底线 | 10 to 8 (-2) | NO |
| v7t | M7 / L2 | A28 / seq 245 to 251 | story: 观察升职靠关系而非能力 | 学习投入非正式场合，控制底线 | 4 to 2 (-2) | NO |

#### Wealth Top10 (clean)

| Run | month/Level | public sequence | family/context | selected legal label | before/after | immediate terminal |
|---|---|---|---|---|---|---|
| v7g | M29 / L3 | A114 / seq 933 to 939 | story: 有毒团队文化中坚守与退出长链 | 联合几位资深同事向HR和CEO实名反馈团队文化问题 | 6 to 2 (-4) | NO |
| v6 | M24 / L4 | A96 / seq 801 to 807 | story: 公司号召自愿降薪共度难关 | 理性回应：可有限度共担，但要求明确恢复条件与书面约定 | 13 to 11 (-2) | NO |
| v6 | M28 / L4 | A115 / seq 953 to 959 | story: 重要客户来访的接待形式选择 | A：商务餐厅工作晚餐并陪餐 2 小时 | 15 to 13 (-2) | NO |
| v7d | M9 / L1 | A35 / seq 305 to 311 | story: 带新人爆雷追责长链 | 改写报告，强调流程缺陷与师徒共担 | 2 to 0 (-2) | NO |
| v7g | M23 / L3 | A90 / seq 741 to 747 | story: 承认心理压力寻求支持长链 | 申请两周医疗假期，配合专业心理干预 | 8 to 6 (-2) | NO |
| v7g | M26 / L3 | A103 / seq 845 to 851 | story: 副业项目与公司业务边界模糊 | 立即向Leader和合规部门披露副业情况，请求边界评估 | 8 to 6 (-2) | NO |
| v7i | M18 / L3 | A72 / seq 597 to 603 | story: 差旅报销边界模糊项 | 仅报销明确合规的机票酒店，放弃所有模糊项 | 8 to 6 (-2) | NO |
| v7i | M25 / L3 | A105 / seq 857 to 863 | story: 副业项目与公司业务边界模糊 | 立即向Leader和合规部门披露副业情况，请求边界评估 | 10 to 8 (-2) | NO |
| v7o | M17 / L3 | A70 / seq 581 to 587 | story: 承认心理压力寻求支持长链 | 申请两周医疗假期，配合专业心理干预 | 9 to 7 (-2) | NO |
| v7t | M31 / L4 | A131 / seq 1021 to 1027 | story: 差旅报销边界模糊项 | 仅报销明确合规的机票酒店，放弃所有模糊项 | 15 to 13 (-2) | NO |

Top-k 为损失排序后按 run/seq 排同幅度 ties，不代表更常见或更危险的 event。只使用 public title/choice family，未建立 event-ID→答案表。

### 5.2 Mixed / terminal 与 buffer

跨月的最大可见 H下降为 v7d M11→12 的6→3（-3）；同一个 public Mentor label，在 v6 同月是6→4（-2）。不能把 mixed -3 并入 clean max2，也不能用该label预测所有后果。512 mixed rows 含批次重复；仅保留例子，未计算 mixed shock 分位数。

v4最后 H1→0 是 terminal-linked mixed -1，伴 E0→3；它既不是 clean lethal action，也不是从厚 buffer 被巨大打击归零。clean H损失 Top10 没有直接 terminal link。clean W最大6→2并未立即终止；v7d W2→0 后继续约6个月。v1#2 的粗粒度 W9→3 不作为 single step evidence。不存在可从这些案例推出的健康/财富隐藏死亡阈值。

| Soft exposure vocabulary | 在本次样本中的解释 | 对选择的作用 |
|---|---|---|
| ABOVE_OBSERVED_MAX_SHOCK | 当前 buffer 高于该维度 clean historical max；例如 v6 H6面对观察到-2后仍H4，v7g W6面对-4后W2 | 仅表示这一历史 one-hit margin；不保证未见 shock、累积损失或 trust terminal |
| WITHIN_OBSERVED_EXTREME_SHOCK | buffer 位于已观察 extreme loss 覆盖范围，例如 v4 H1、v7d W2 | 提示保留选择余地，不自动 S |
| THIN_BUFFER | buffer 与 severe-loss cluster 相近；H2 与尾部-2、W2与常见-2可作历史参照 | 与趋势、事件威胁、合法恢复机会一起考虑；不是固定策略阈值 |
| CRITICAL_PUBLIC_EXPOSURE | 薄 buffer 加当前 fresh material threat（acute症状、明确安全/支付/收入/continuity威胁），或直接 public恶化证据 | 可支持最小必要稳定化，再 observe/re-prove/exit；不能仅凭 buffer 标签授权 |

**Generalization boundary:** observed max ≠ simulator maximum ≠ hidden Test maximum。未知大 shock、连续 shock、等级/事件分布差异均未覆盖。不存在 Health≤2→S、Wealth≤4→恢复等自动规则；这些数值只描述这批历史记录。也不能要求每一时刻都保持高于样本最大值。

## 6. High-score invariants 与 joint interpretation

**重复公开模式（descriptive donor pattern，不是必要充分条件）：** v1#1/v6/v7o 都在 M6→L2、M12→L3、M18→L4，随后 S/N/O 广泛增长，M36再晋升。v1#1/v6 M48到L6，v7o终局L5。早晋升 cadence 是有用的健康信号，不是已知 hidden formula。v1#2 前两次也晋升后仍失败，故不能用 cadence 取代 floor protection。

**Breadth:** donor M18 S/N/O 为44/19/16、38/19/17、37/18/19，失败 v7q/w均9/3/3。这支持保持有响应的多维 compound value；不支持固定均衡配额。S08-11已证实 v6/v7o Output Energy share 低于 v7t/v7v，但成绩更高；增加 Output 或更多 recovery 都不是单调高分规律。v7w早窗 Main 仅3/6 key project，v6/v7o6/6；v7q也是6/6，说明该差异只可作ranking hypothesis。

**Survivor controls:** v7g在M6失败后仍恢复M12/M18晋升；v7i/v7t/v7v错过部分窗口仍48m。它们支持“可以在成长中修复”的存在性，不证明某 recovery policy 稳定有效。v7g33次S且存活，反对“任何S都有害”；v7o四次 numeric-only false-S仍高分，反对单个错误marker就能解释整局分数。长期长S与早期停滞共同出现于q/w，但独立因果 UNKNOWN。

**Matched v1 pair:** 前两窗相似级别/成长，#2 M12选择避险、后半程 Energy更多 Health/cleanup，M24 S/N/O43/19/13落后#1 63/36/26；仍不能说保守选择造成trust失败。#2末期H10，growth与health两条保护都不足以单独保证continuity。风险次数、公开规则遵循与最终career结果不能互相代证。

**Matched v7v→v7w lineage:** v7w继承runtime shell、改Planning core。前24窗 v7v S占1/101=1.0%，v7w44/112=39.3%；这是共同时间窗的marker率，分母为attempts。v7v M18 L3/27/11/10，v7w L1/9/3/3；v7v M12 no-promotion后A修复并M18晋升，v7wM18D后longS且M24才晋升。两局正常每action freshobserve，但v7w16不明回执、42malformedDelivery、literalplan缺失与不同events均是material differences。

归因分层：**FACT** 当前 v7w trajectory 未复制早期engine；**HYPOTHESIS** Ranking core 未有效应用、stale mode/plan 或交付语义缺口可能贡献；**UNKNOWN** 策略设计本身的 causal effect、随机路径贡献比例、单一rootcause；**RECOMMENDATION** 先解决可观测non-sticky mode/Review重建行为，保留runtime controls，不把一次30.31当作广泛成长路线已被推翻。

## 7. Local response、Delivery 与早期预警

| Run | S G/Z/D/M | N G/Z/D/M | O G/Z/D/M | immediate repeats after clean zero |
|---|---|---|---|---|
| v6 | 0/0/0/0 | 6/2/0/0 | 12/3/0/0 | 0 |
| v7o | 4/0/0/0 | 6/2/0/0 | 17/3/0/0 | 1 |
| v7g | 0/0/0/0 | 1/0/0/0 | 6/5/0/0 | 0 |
| v7i | 0/0/0/0 | 4/1/0/0 | 10/5/0/0 | 0 |
| v7t | 0/0/0/0 | 1/1/0/6 | 5/5/0/14 | 2 |
| v7v | 0/0/0/0 | 0/2/0/0 | 19/5/0/0 | 0 |
| v4 | 0/0/0/0 | 1/0/0/0 | 0/1/0/0 | 0 |
| v7d | 0/0/0/0 | 4/1/0/0 | 4/1/0/0 | 0 |
| v7q | 0/0/0/0 | 3/3/0/0 | 6/3/0/0 | 0 |
| v7w | 0/0/0/0 | 5/1/0/1 | 4/2/0/2 | 0 |

Energy 表仅统计 label 明确对应 Skill/Network/Output 的维度。Story 与跨月 Main 的 S/N/O变化仍在窗口数据里，但不臆造 advertised dimensions。v7t O=5GAIN/5NO_GAIN/14mixed，已知 batch边界使其不能作为14个独立收益样本；v7w O=4GAIN/2NO_GAIN/2unknown，N=5GAIN/1NO_GAIN/1unknown。严格口径下 v7w没有“clean NO_GAIN 后立即重复”的已证例：76/97/99第一次回执不明；不得把旧报告的 adjacent-zero repeats 提升为clean证据。77仍为clean0，98/100后来有gain；不支持hidden cap。v7t M42有两次clean zero后的立即Output重复；v7o M45也有一次，故重复本身不是失败局专属机制。

Board的完整Level reset ledger、multidimensional partial-discount、routed-away的Planning因果意图仍 **UNKNOWN**。观察到选项切换只证明行为序列，不能叫作已执行NO_GAIN控制器。未来设计只能在当前Level新鲜公开响应下做局部discount，并保留其它有价值维度；不按S/N/O均衡重投已无响应路径。

| Warning class | 当前证据 | 设计需求与限制 |
|---|---|---|
| Growth | M6/M12/M18 no-promotion、弱grade、公开S/N/O响应弱 | A+PROGRESSION；Review后重建下一窗口目标，不能仅复制旧gap；no-promotion本身不授权S |
| Buffer without threat | H/W较低或普通成本，未见fresh material threat | 留optionalities、偏好低机会成本buffer维护、监测；numeric comparison不升级binding |
| Acute resource/safety | v7v心悸胸闷手抖；v4累积Health到低位并继续下降 | 允许bounded稳定化，freshobserve后检查威胁是否仍在；不补满所有资源才退出 |
| Trust/continuity | v1#2 repeated crisis；public保密/合规/retaliation威胁 | 只有公开威胁和合法可修复动作才做bounded containment；首次warning leadtime UNKNOWN，不能依hiddencounter重规划 |
| Delivery | v7d M14已排满sprint+明确交付底线却申请探索；v7v安全发布containment | 对可证明near-term obligation保护certainty；工具成功不等于career verification；普通pending不永久override成长 |

Delivery exception 的频率/完整item identity不在这些public-action枚举中机械计数，沿用正式报告：v7w70valid/42malformed（n0却NEAR）、overclaim UNKNOWN；v7v containment支持、lifecycle completion不确定；v7i真trigger0、tracking不连续；v7t audit newline correction不能抹掉33invalidcheckpoint。Risk：v7v公开warning-gated cleanup有序列证据；v7wR=PASS98/ALLOW14并不证明没有威胁，RISK显式标签1次未有完整trigger→exit。未用numeric hidden-risk词/值解释这些路径。

## 8. Floor-Preserving Growth design requirements

此处是设计证据与可证伪假设，不是新Prompt或Candidate。formal Skills、manifest、retry与validation flags均未修改。架构不改变。

| Requirement / decision | Evidence | Hypothesis / expected benefit | High-score regression risk | Confidence / status |
|---|---|---|---|---|
| Progression recovery留A；Review后重建窗口 | q/w三次no-promotion，v7g/v7v错窗后成长恢复 | 能避免绩效失败被长期稳定化吸收，恢复复利 | 固守A可能漏掉真实acute threat，必须保留binding例外 | 证据中；设计方向 SUPPORTED，收益未证 |
| 每次freshobserve重新证明S的当前binding basis，不继承旧S | w42连续S、D/H恢复后仍S；v7v一次S后A | 更清楚exit、减少stale mode；不改变具体选项排序优先级 | 若public warning暂时消失却未解决，过早exit有害；未解除证据仍可重授权 | 缺口高，benefit中；PLAUSIBLE待实验 |
| H/W empirical prior作为soft opportunity cost | H-2、W-4；v4cumulative；v7gW6→2存活 | 有便宜合法机会时避免薄buffer暴露 | hard max reserve吞掉growth；极端样本或Test不同失效 | 样本统计高，转移低；PLAUSIBLE，硬阈值UNSUPPORTED |
| public continuity保护与growth并行 | v1同candidate前两窗均晋升，#2trustterminal；cleanup仍失败 | 防止晋升掩盖另一条floor威胁 | stronger cleanup/反复保守侵蚀compounding，且无fresh trigger | floor独立轴SUPPORTED，具体repair收益UNKNOWN |
| broad responsive growth，gap advisory，NO_GAIN只discount局部维度 | donors广泛增长；q同Main频次仍弱；v7tzero repeats | 避免tunnel，不牺牲multidim其余价值 | 非特定coverage变固定均衡；噪声zero误杀路径 | descriptive中；PLAUSIBLE，不冻结比例 |
| only binding near-delivery exception；claimed与verified分离 | v7dscheduled探索；v7vcontainment；w42malformed | 降低明确交付损坏，仍推进晋升 | 每个pending都override，形成低分保守路线 | certainty需求SUPPORTED；score收益UNKNOWN |

**最小 next Candidate behavioral hypothesis（未实施）：** `FRESH_BINDING_BASIS_REQUIRED_FOR_EACH_STABILIZATION_DECISION`。假设在已有freshobserve/Board→Delivery→Planning→Risk shell中，对每次S要求当前公开binding basis与明确exit，并在仅progression问题时恢复A，可减少w式mode持久化，保留已有promotion-first排序。只验证这一主要行为delta；不同时增加fixed reserve、cleanup次数或新状态机。Review plan重建、broadgrowth、NO_GAIN与Delivery作为既有行为的审计要求，若需要独立改动应另开设计，不捆绑成多delta候选。

未来实验的可证伪指标：S entry/continued-S的当前public basis、威胁解除后第一个A、no-promotion后的下一Review目标、M6/12/18级别/反馈、clean响应、near-termDelivery、token/continuation成本；每个S仍有fresh threat则假设缺口缩小，若mode改善但engine/score不改善则不能宣称策略因果成功。任何新运行须新Main授权。

## 9. Regression Risk Matrix

| Proposed mechanism | Intended failure | High-score risk | Evidence support | Confidence / decision |
|---|---|---|---|---|
| More Health investment | v4 attrition | 丢失季度成长；v1#2H10仍终止 | 早期局部恢复有用；无单调收益 | 中；仅机会/威胁驱动PLAUSIBLE |
| More Wealth investment | 薄支付buffer | 成长资源常态转财务，未有legal路径即可臆造 | v7d低W、v7g-4存活；W0非即时terminal | 低；无条件增加UNSUPPORTED |
| Longer S | floor stabilization | q/w长期S、Review engine不恢复 | 一次短S后A在v7v可行，longer收益无证 | 中；HARMFUL_RISK |
| Stronger trust cleanup | v1#2continuity | 幻想hiddencounter、无trigger重复cleanup | #2做过cleanup仍失败，fresh warning repair另有报告支持 | 中低；仅boundedpublictriggerPLAUSIBLE |
| Early-promotion recovery | progressioncollapse | 为短期数字忽视acute/Delivery | donorscadence；g/v错窗后恢复 | 中；SUPPORTED方向，阈值UNSUPPORTED |
| Broad responsive growth | gap tunnel | 强制均衡再投NO_GAIN | donorsS/N/O；frequencyalone失败 | 中；PLAUSIBLE，固定quotaHARMFUL_RISK |
| Stronger Gap concentration | visibleoutput弱 | 单维tunnel、忽视其它publicresponse | laterOutput份额高却低分；未受控 | 中低；无条件强化UNSUPPORTED |
| Delivery certainty override | scheduledwork破坏 | 全部pending永久override成长 | v7d明确排期风险，v7vcontainment；wtracking错误 | 中；只freshbindingSUPPORTED |
| One-shock reserve | 薄buffer遭损失 | hardreserve吞growth；unseen/累积风险仍在 | empiricalH2/W4；negativeN143/16 | 统计高、策略低；soft priorPLAUSIBLE，fixedthresholdUNSUPPORTED |

拒绝“所有低数值进入S”“S补满才退出”“提高cleanup配额”“更早只投Output”“任何NO_GAIN即永久放弃”“任何Delivery pending压倒成长”等诱人回归。没有稳定80+、hidden-test transfer或单局causal improvement结论。

## 10. Verification、完整性与交付

- Targeted synthetic suite：14 passed，覆盖negative/zero/gain、跨月/Level、Energy回补、batch、unknown receipt、缺field/session、duplicate frames、terminal link与private exclusion。一次manifest字段假定错误（path实际为name）在离线提取器中修正，未触发live，未改变来源。
- Manual public spot checks：v6 action28 H6→4（pre O252、A253、post O259）；v7g action114 W6→2（O932/A933/O939）；v7d action35 W2→0（O304/A305/O311）；v4恢复与terminal见第4节。只打印allowlisted状态/合法label，没有输出raw整行。
- Deterministic rerun PASS：派生JSON SHA-256 `16494b1fe0381a79ea9804013e242274f19ac2eee857ad88a50d1321bbbfc1d6`；JSON parse、public-key/session exclusion、6份canonical secret scan（含ignored JSON）、protected-file diff、git diff --check与ignored-output check均PASS。验证记录留在 `.local/scratch/s09-02/verification.json`。所有新tracked资产为本报告、extractor、targeted test与两份简短state/history更新；无raw archive新增。
- 原有FORENSIC_HOLD全部保持；没有source删除/移迁、没有Candidate validation更新。共享runtime、DB、provider及HPL均未访问。

## TASK_RESULT｜S09-02

### Identity

Status：`OFFLINE_FORENSICS_COMPLETE_DESIGN_EVIDENCE_READY`；Base：`5bc07edc49bb352a686d13940fb36f78d01ca827`。Final commit为包含本报告的交付commit，由Git历史/最终回复给出；remote/clean在push后核实，不自引用commit hash。

### Cohort / Findings

Included：10 Tier A + 2 Tier B；没有Tier C进入shock。Excluded：v1 raw已不可用，保留B轨迹；Baseline/SCORE-01与不明身份样本仅context。Resource / Trust-continuity / Progression / Control-recovery四类见第4节；无额外证据充分的新failure类别。H/W N976，max2/4；terminal-link为v4mixed，不是clean致死因果。High-score invariants、survivor-only例外、warnings、matched pair与v7w归因见第3/6/7节；design cards六项及minimal next hypothesis见第8节。

### Final Decision / Permissions / HPL

`S09_02_FAILURE_FLOOR_HIGH_SCORE_JOINT_FORENSICS_COMPLETE_DESIGN_EVIDENCE_READY`

Provider/service/MCP/game = 0；Candidate/Skill/manifest/runtime mutation = 0；NEXT_GAME=NOT_AUTHORIZED；HPL_COORDINATION_IMPACT=NONE。仅取证/记录，路线、实施与下一game由Stage/Main review。

### EXECUTION_METRICS / EXECUTION_ISSUES

Model Used / Reasoning Effort / Started At / task Wall-clock / task token usage：UNKNOWN（未取得可靠当前Task计时/usage）。Finished At由最终执行记录给出。Avoidable Execution Issues：2（Windows rg未展开的wildcard路径；diagnostic_harness的manifest schema假定），Consumed Live Budget=NO；工程来源不足/保守归因修订不计avoidable failure。用rg目录参数和glob选项，manifest沿用既有name schema；无需增加live诊断。
