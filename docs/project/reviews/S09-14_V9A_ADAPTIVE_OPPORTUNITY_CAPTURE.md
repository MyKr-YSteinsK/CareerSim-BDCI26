# S09-14｜自适应机会捕获单 Delta 静态实现

## Identity / decision

- Status：`IN_FLIGHT_EVIDENCE / STATIC_ONLY_NOT_SUBMISSION_VALIDATED`。
- Candidate：`candidate-v9a-adaptive-opportunity-capture`；exact parent=`candidate-v8a-v7o-donor-core-transplant` at `main@a2bf214b6f4c6923399f80ada03b4d61d97f6eaa`。
- 唯一 behavioral delta：`ADAPTIVE_OPPORTUNITY_CAPTURE_WITH_BOUNDED_UNTESTED_PROBE`，来自 [S09-13](S09-13_HIGH_SCORE_STRATEGY_SYNTHESIS.md) 的可证伪设计建议，不继承其分数或历史 Candidate validation。
- Decision：`S09_14_ADAPTIVE_OPPORTUNITY_CAPTURE_STATIC_PASS_RETURN_TO_STAGE`。Stage 决定后续实验；本任务没有游戏授权。

用户另行授权隔离到 `codex/s09-14-v9a-static`：首次 main push 遇到并发提交 `6a4037fdf2b75c105cfe0b40b93ea68d3dd0a6f3`，已将 v8a canonical status 冻结并添加正式材料。分支以该最新 origin/main 为整合基线，保留本任务精确 behavioral parent/base `a2bf214`；只在此分支配置 v9a，main 的 v8a freeze/材料保留。此结果不是 `MERGED_FACT`，不授权合入或替换 final submission。分支 checkout 后 manifest 的物理换行可改变，已同步其 byte hash；instruction/策略不变。

## 最小实现

在 Planning 的 local-response discipline 后新增一个三段的 `Bounded untested probe` 小节。五项条件同时满足才将一次 probe 加入 top comparison：fresh clean local stagnation、无更高价值已知 responsive 合法替代、有公开语义支持高价值的合法未测试 family、无重大 survival/compliance/trust binding、不会明显破坏 binding near-term Delivery。比较职业资本、ownership/result、多维价值、普通/交付成本和生存/合规约束，**不自动选择 probe**。

Binding 保护先行，responsive exploit 优先；停滞路径仍可因独立多维/交付价值胜出。Probe 胜出也只选一 action，之后 executor fresh observe，仅更新当前 Level/context/family/dimension。GAIN 不是最优证明，NO_GAIN 不是永久 cap；不自动授权下一 probe、不连续探测两个未知 family、不加 quota/budget/ledger/state machine。无 fixed Skill 偏好、event/title 答案或新 late-game/realization 机制。

删除该小节后 Planning **完整等于精确 v8a parent**，因此晋升优先/broad growth、Review reset、MODE/最小保护、local NO_GAIN 与 Level reset、Delivery、decision budget、Risk reconsider 和 Single Agent ownership 均原文保留。Planning 规范化 LF 字符数 **8,748 → 9,477**（+729，8.33%）；只有一个短 local fallback，小节静态长度预算 ≤800 字符，非游戏阈值。

Manifest 仅 `name` 更新；整个 instruction 字符串及 instruction SHA256 `79de9c4892311104967411d24b2a36597a7deaec4c42ada53b55c7173c8ea8f7` 未变。Candidate config 更新父链/manifest hash/Planning blob/机制身份，全部9项 validation flags=false；v8a 的 gameplay/provider evidence 不转移。架构/Runner/依赖/retry/model-provider config/runtime shell 无改动。

### Frozen Skill bytes

三份文件与 RUN06/07/08 沿用的 `.local/runtime/s09-run06-v8a/submission` 逐字节相同；Git blob 也与 parent 一致。原文件保留其既有 LF/CRLF，不修改换行。

| Skill | 当前物理文件 SHA256 |
|---|---|
| Board | `e2f31a83b357f2f75b1e2c0e8285fba440a17d3c4c4c8d6587b4f2e5fa9f366c` |
| Delivery | `200b6c83aaca43f6dccfe58a30e23e79463e930512ef89cf5b19070a9d5d7528` |
| Risk | `6da910fa60b07dfdccfc78a840ebc4777fc39e3188358e69ee483c89606874fd` |

## Static scenarios / regression

**21 新 targeted checks passed**，其中以下10类契约场景全部 PASS。这是书面策略/身份/frozen-surface 检查，**不是 LLM 行为、晋升、score 或 hidden Test oracle**。

| Scenario | 契约要求与静态结论 |
|---|---|
| Output fresh NG + untested Skill，无 binding | 未测试高价值路径进入比较；不强制获胜；PASS |
| Output NG + responsive Network | 已知高价值 responsive exploit 优先；PASS |
| Network NG + high-value ownership Story | 未测试其它 family 与 ownership/多维价值保持开放；PASS |
| Output NG + binding near Delivery | 会破坏义务时禁止 probe；PASS |
| Output NG + explicit Health/safety threat | material 保护阻止 probe；PASS |
| Output NG + explicit compliance/trust threat | 公共约束先行，有界 containment 保留；PASS |
| Probe GAIN | one action→fresh observe，局部更新，非 quota/最优证明；PASS |
| Probe NO_GAIN | 局部降权、不永久放弃、不自动下一 probe；PASS |
| Level change after NO_GAIN | 原 Board reset/option reopen 保留；PASS |
| Existing high-value responsive path | 不为覆盖率/固定 Skill 偏好探索；PASS |

**17 existing targeted regression checks passed**：S09-10 的14项 donor/core/scenario/frozen checks、2项 acyclic READY/preflight checks、1项 deterministic canonical packaging check。只 deselect 历史 `test_identity_and_all_validation_flags_reset`，因其断言当前身份必须 v8a；新的 v9a identity test 已严格核验 exact parent、hash/blob、全部 flags=false。未改旧测试以放宽行为约束，未运行不相关历史 suites。

## Package / fallback / evidence boundary

使用未修改的 `scripts/package_candidate.py` 构建并调用冻结 Runner 的文件级 `validate_submission_contract`：

- v9a：`.local/scratch/s09-14/v9a-branch-submission`，valid `skill_bundle` / exactly4 Skills / manifest valid。
- v8a：从 base Git 的 configs+四 Skills 重建 `.local/scratch/s09-14/v8a-fallback-source`，再构建 `v8a-fallback-submission`；同样有效，canonical manifest SHA 与 parent config 一致。精确 Git来源也记录在新 config 的 `submission_fallback`，可重新构建，不依赖 scratch 存续。

这些是可重建的离线目录，没有 install/reload、shared runtime/config mutation 或 official solution.zip 修改。v8a 仍为 submission fallback；v9a 只有静态证据，`MUST_NOT_REPLACE_V8A_FOR_SUBMISSION`。v8a 自身 official admissibility 仍受正式提交合同约束，fallback 身份不构成新的 official validation。

增量检查：JSON parse、身份/hash、public-only/no fixed lookup/quota/threshold 契约检查、secret-pattern scan、`git diff --check`。没有引入历史事件/score/Risk 数值到策略；runtime evidence firewall 完整保留。既有 raw/FORENSIC_HOLD/HPL 均未变。

执行工具问题：一次 PowerShell glob 路径错误，以及 byte verifier 对混合 LF/CRLF 的两次错误假设；均无目标 runtime 副作用。改用 `rg -g` 与既有 v8a bundle 的逐字节对照解决，不规范化受保护文件。

交付仅 Planning、两份候选 identity config、一份 targeted test、此短 review、CURRENT_STATE 的一条 current-candidate delta。Commit/push/clean 由最终 TASK_RESULT 给出。

`live operations=0`；`NEXT_GAME=NOT_AUTHORIZED`；`V9A_SUBMISSION_REPLACEMENT=NOT_AUTHORIZED`。
