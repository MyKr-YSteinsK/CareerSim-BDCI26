# S06-03 静态回归矩阵

Candidate：`candidate-v3b-final-policy`。静态 PASS 仅说明书面合同、仓库身份与无 live 边界通过，不代表实际模型遵循、策略收益或 gameplay effectiveness。验证脚本：[`verify_static_contract.py`](verify_static_contract.py)，使用项目根 `.venv` Python；交付 Git 条件另由最终 TASK_RESULT 核对。

| # | 验收项 | 静态证据 / 检查 | 结果 |
|---:|---|---|---|
| 1 | S06-02 accepted branch ancestry verified | `043ecd1…` 是 S06-02 accepted branch fast-forward 后的 base；`git merge-base` 和 candidate metadata | PASS |
| 2 | S06-02 reconciliation 只改状态文档 | 接受 reconciliation commit `043ecd1…` 仅修改 `docs/project/CURRENT_STATE.md` | PASS |
| 3 | S06-02 clean fast-forward 到 main | `main` 从 `3ec5ad2…` fast-forward 到 `043ecd1…`，无 merge commit | PASS |
| 4 | S06-03 branch 从 updated main 建立 | `codex/s06-03-final-policy-tightening` base = `043ecd1…` | PASS |
| 5 | 无 accepted-history rewrite | 无 rebase、amend 或历史重写；S06-02 提交 SHA 保持不变 | PASS |
| 6 | 普通选择使用 Primary Gap | `rolling-planning` step 7 要求普通选择贡献到当前 Primary Gap | PASS |
| 7 | 比较顺序正确 | 明确 Material Risk → Gap contribution → secondary benefit → Soft Cost/opportunity cost → UNKNOWN | PASS |
| 8 | 无固定数值打分 | Planning 明确禁止 fixed weights/numeric score；runtime cue 使用定性排序 | PASS |
| 9 | 不默认成熟/稳妥优先 | Planning 明确不默认最成熟、最安全或最不得罪人的选项 | PASS |
| 10 | AVAILABLE 的正向高收益语义 | 无 fresh Material Risk、AVAILABLE、Gap upside 明显更强且额外成本主要为 Soft Cost 时优先该合法路径 | PASS |
| 11 | 相近/未知 upside 可选低成本 | Planning 明确 similar/UNKNOWN Gap upside 时较低成本/暴露路径可以胜出 | PASS |
| 12 | TIGHT 的 Material Risk 保护 | TIGHT 可使 Material Risk 压过增长收益；candidate review 仍属 Risk Skill | PASS |
| 13 | 无固定风险/健康阈值 | 未增加 Health/Dignity 数值、risk/aggression score、fixed loss budget 或 hidden threshold | PASS |
| 14 | 局部正反馈不等于进展 | praise、bonus、关系改善、一次性事件仅是 supporting signal | PASS |
| 15 | ADVANCING 需要 Gap 直接证据 | Gap 本身可观察改善或直接相关公开 progression/performance evidence；否则不因局部信号升级 | PASS |
| 16 | 证据不足 fallback | 不可比时 UNKNOWN；仅当既有两 checkpoint 条件成立时 STALLED | PASS |
| 17 | two-checkpoint STALLED 保留 | 同 action、同 Gap、相邻可比 checkpoint 无进展后才 STALLED，随后必须比较不同类型 alternative | PASS |
| 18 | 每季度 checkpoint 仍强制 | 每季度第一次 Energy 前从 fresh public state 刷新/创建 checkpoint | PASS |
| 19 | 季度变化不再强制全文重读 | Planning 与 instruction 明确 quarter change/missing checkpoint alone 不要求 reread | PASS |
| 20 | 条件重读触发明确 | 初始详细规划、半年反馈、严重后果、continuation/context loss、过期/歧义或 procedure 无法还原 | PASS |
| 21 | Always-visible cue 足够 | runtime instruction 保留季度触发、Gap、Progress/effect、Risk Budget、stop rule 与唯一提交者 | PASS |
| 22 | Manifest 不是第二份 Skill | instruction 只提供短 controller cue；详细算法留在 Skills | PASS |
| 23 | Context-loss effect recovery 最多两项 | Board 明确 up to 2 recent strategic action/effect pairs，recent_effects 上限 2 | PASS |
| 24 | Recovery 仅当前 game | 先确认同一 CareerSim `game_session_id`，session mismatch 清空旧 Board | PASS |
| 25 | 日志回看有明确上限与用途 | 最多 5 条最近同局 public log，仅用于 context-loss effect recovery | PASS |
| 26 | 歧义 fallback UNKNOWN | 不可直接比较/归因时 UNKNOWN 或省略；fresh observe 优先，不从顺序推因果 | PASS |
| 27 | 不引入 durable Memory | 只保留当前对话工作上下文，不写 Memory/跨局状态；candidate 明确 DEFERRED | PASS |
| 28 | 恰好四个 Skills | 静态枚举 `skills/*/SKILL.md` 仅四个规定名称 | PASS |
| 29 | Trace byte/blob identity 冻结 | `career-action-trace` Git blob 仍为 `5a1e3ceca8ffc2132303e43bc9f1c1dd630847a8` | PASS |
| 30 | Single Agent 唯一 submitter | Planning、Board、Risk 不提交动作；runtime cue 保留 Single Agent authority | PASS |
| 31 | Risk Material/Soft 边界保留 | Risk Skill 与 accepted base 的 blob 完全相同：`6680e45d…` | PASS |
| 32 | 无第五 Skill | 四 Skill 集合和 candidate manifest 完全匹配 | PASS |
| 33 | Memory 未实现 | no Memory artifact/change；候选将 durable/cross-session Memory 标为 deferred | PASS |
| 34 | Team/Swarm 未实现 | no Team/Swarm implementation；Single Agent architecture retained | PASS |
| 35 | 无 hidden threshold/evaluator/event answer rule | 静态扫描候选 policy，无 evaluator weight、隐藏阈值、score-to-80 或 event-title mapping | PASS |
| 36 | Runner/dependency/lock 不变 | 与 `043ecd1…` 比较 `career_sim_runner/`、`pyproject.toml`、`uv.lock`、Source Lock 均无 diff | PASS |
| 37 | 新 runtime manifest 纳入 Git | `experiments/S06-03-final-policy-tightening/runtime_manifest.json` 为 tracked canonical artifact | PASS |
| 38 | S06-01 历史 manifest 不变 | Parent / final Git blob identity 对照一致；未覆盖旧文件 | PASS |
| 39 | Candidate manifest hash 自洽 | Skill Git blobs、runtime manifest SHA-256、instruction SHA-256 与 implementation commit 对照 | PASS |
| 40 | 静态回归完成 | 本矩阵共 56 项；纯静态 verifier、JSON/YAML 与契约断言通过 | PASS |
| 41 | Benchmark matrix 更新 | 新 successor matrix 链接 S06-01，并新增 v3b 决策/恢复/成本观测项 | PASS |
| 42 | Context bytes/lines 可复现 | 由 implementation commit 的四个 exact Git blobs 计算 parent、final、delta 与百分比 | PASS |
| 43 | 无 secret/runtime raw 入 Git | Changed-path/secret-pattern 扫描；无 `.env`、log、DB、session 或 raw data | PASS |
| 44 | `git diff --check` | 最终提交前后执行，返回 0 | PASS |
| 45 | JSON/frontmatter parse | runtime/candidate JSON 与四个 Skill YAML frontmatter 均可解析；name 唯一且 description 非空 | PASS |
| 46 | Provider requests = 0 | 本任务仅进行离线 Git/静态检查，未调用 provider | PASS |
| 47 | Service starts = 0 | 未执行 service lifecycle | PASS |
| 48 | Install/reload = 0 | 未安装 submission 或 reload Skills | PASS |
| 49 | MCP runtime calls = 0 | 未调用 MCP runtime | PASS |
| 50 | `new_game`/`observe`/`take_action` = 0 | 未运行 CareerSim tool 或 gameplay | PASS |
| 51 | Runner play/full game = 0 | 未运行 Runner play/full game/competition submission | PASS |
| 52 | Branch commit + push | S06-03 最终提交已 push 至指定独立 branch | PASS |
| 53 | Remote SHA 匹配 | fetch 后 `origin/codex/s06-03-final-policy-tightening == local HEAD` | PASS |
| 54 | Working tree clean | 最终 `git status --short --branch` 无未提交变更 | PASS |
| 55 | S06-03 未合并 main | S06-03 仅作为独立 review branch 推送 | PASS |
| 56 | 返回 Main review | 最终状态为 `FINAL_OFFLINE_POLICY_READY_FOR_MAIN_REVIEW`，Game Gate 仍未授权 | PASS |

## 解释边界

这些 PASS 只覆盖已冻结文字合同、Git 身份与静态检查。实际季度 adherence、重读频率、控制器策略收益、稳定 80+、provider freshness 与 cloud behavior 均未验证。
