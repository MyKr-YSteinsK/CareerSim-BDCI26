# S09-05｜v7y Story 暴露保护静态集成

## 1. Identity / evidence boundary

- Base：`main@da5359d2d9a978475484300cf1f4a75013393329`；fetch 后 HEAD=origin/main，初始 clean；在 main 串行执行，无 branch/worktree。
- Parent：`candidate-v7x-fresh-binding-reauthorization`。
- Candidate：`candidate-v7y-story-exposure-guard`。
- Strategy delta：`M5_STORY_EXPOSURE_GUARD_AS_BOUNDED_A_MODE_RANKING_PRIOR`。
- Status：`STATIC_IMPLEMENTED_NOT_RUNTIME_VALIDATED`；9 个 validation flags 全部 false。v7x 的 session-specific gameplay/provider evidence 不转移。
- 实施依据：[S09-04](S09-04_RESOURCE_TRAJECTORY_INTERVENTION_FORENSICS.md) 的当前 Story 减曝设计假设；本任务采用 S09-05 FROZEN 的四个当前证据条件，不另加历史 trajectory/FRAGILE 触发条件。语义可实现性为中等，净存活/分数收益仍未证。
- Plan：`D:/Downloads/S09-05-v7y-Story暴露保护静态集成.md`；ZIP：`D:/Downloads/S09-05-v7y-integration-pack.zip`，6814 bytes，SHA256=`d7abeb60cc13b5a9ac59c97f3eceeb9b50a23e0cafee12445745db761824d867`。

压缩包只有四个预期文件。执行前核验 SHA256SUMS、源码和替换锚点；原包保持不变，使用 `.local/scratch/s09-05/pack/` 下精确副本：

| Supplied file | SHA256 |
|---|---|
| apply_s09_05.py | `f6cef3a0bba991ef8462887f4f6f4c46caf10e32b34c6fbffe8192f7546fbc1b` |
| test_s09_05_story_exposure_guard.py | `b5d8cd44797eab6a048d33092a9275df16ac198702f832852796637aad8e0085` |
| README.md | `09d9ac9584239d099963afd420f719a35b126ffba3612a367623094de73bc4da` |

## 2. Exactly one behavior delta

`rolling-planning` 的 Promotion Portfolio 内只增加一条 **Current Story exposure guard**：

1. 最新 fresh public Story/event 明确存在 physical/safety/workload exposure。
2. 当前菜单存在合法低暴露选择。
3. 不明显牺牲 binding Delivery、job/income continuity 或明确更高价值 progression。
4. 与最佳成长候选价值相近。

满足时保持 MODE=A，优先保留 optionality。成本不明或 high tradeoff、普通疲劳/负荷、单纯数字低、旧暴露/恢复都不触发；不推断未选项 hidden effect。一次 choice 后失效，下一 fresh observe 重建 Board/Delivery/Planning/Risk，重新基于当前菜单比较。任何未知条件均不能授权 prior，仍使用原 Promotion Portfolio。

未新增 MODE/RECOVERY enum、RESOURCE_STATE、FRAGILE 状态、Health 阈值、恢复期或季度恢复配额；不改变 Energy/Main allocation。Planning 输出、Decision Budget、Risk reconsideration、formal Review/terminal horizon、NO_GAIN、非粘滞 S、Promotion Portfolio 本文其余内容全部保持。

## 3. Manifest compression / semantic preservation

字符按解析后的 instruction Unicode code points 计数，包含空格/换行，不以 JSON bytes 或 tokens 代替。

| Version | instruction chars | CRITICAL KERNEL chars |
|---|---:|---:|
| parent v7x | 5198 | 1225 |
| supplied patch preview | 4935 | 962 |
| final v7y | **4984** | **1011** |

最终少214字符，满足 <=5000。压缩仅限 CRITICAL KERNEL；manifest 除 name/instruction 外 metadata 完全一致。边界 `CRITICAL KERNEL\n` / `\n\nSTARTUP AND FLOW\n` 两侧 decoded instruction 精确比较 PASS：

| Unchanged block | chars | SHA256 (UTF-8 decoded text) |
|---|---:|---|
| prefix：public evidence/firewall/ownership | 992 | `402ca1f708f902142090df946de4b2b24158348e1312eaaaa90bf89897ca0ccc` |
| suffix：startup/flow/persistence/control/preflight/quarterly/context recovery | 2946 | `6ecead9d3afa1acb88f57618bcc4b8ec6a1b17aca14a76b3891c77662f438865` |

供给脚本初版压缩后，补回 parent 语义的显式措辞：`fresh public evidence`、`不靠旧S/旧reason续期`、`strong default prior`、`当前 Level/context path`。另外将 Plan 要求的普通负荷 exclusion 和 job continuity 写明于新规则；这些是同一 guard 的边界校准，不是第二行为 delta。原始供给脚本未改写。

| Parent semantic invariant | Final kernel / unchanged owning Skill proof |
|---|---|
| S 每轮失效，fresh material binding basis，unresolved 可重授权、最小必要稳定化 | kernel 保留显式 fresh/expiry/unresolved/minimum/禁止旧reason；Planning MODE/RESOURCE 原文完全不变，仍列各类约束和退出条件 |
| Formal Review 重建整个 Portfolio，Primary Gap advisory，不跨 Review 继承 | kernel 保留重建/继承边界；Planning 长期规划一致性原文保留 Level、S/N/O、career capital、Delivery、next realizable checkpoint 全列表 |
| Time-sensitive exception 优先；broad responsive compounding 是 strong default；conditional gap 可短期 dominant | kernel 保留优先/strong/fresh-specific-responsive/checkpoint/dominance expiry；Planning Ranking 的原有各条字串完全一致 |
| clean NO_GAIN 局部折价、positive reallocation、不得推 cap/转 filler | kernel 明示 Level/context、responsive/multidimensional、positive reallocation；完整 Progression Routing 原文仍约束单维折价、其它 GAIN/UNKNOWN、Level reset |
| 无下一真实 Review 才 direct realization，不虚构 future Review | kernel 保留 horizon 条件；Planning Final Horizon 原文不变，公开48个月与career capital/ownership/visibility/verified result/合理survival protection仍完整 |
| Evidence / ownership / execution / control / quarterly / recovery | 全部位于上述精确相同 prefix/suffix；Board/Delivery/Risk byte/blob identities 未变 |

静态检查支持完整 manifest+Skills 协议语义保留；没有把字串/身份通过冒充模型长期执行、压缩后遵守或收益验证。

## 4. Candidate / package identity

| Surface | Final identity |
|---|---|
| runtime_manifest.json | 7005 bytes；SHA256=`0f3b44466e0f16fd21a3d3724ffe890a9f4114dcc69088d20b238bbea115489d` |
| instruction UTF-8 SHA256 | `3e382913dbcbe0a936726cd8aa5a2e61c32bdff107f3622fedd55326179e517b` |
| rolling-planning | 13840 bytes；SHA256=`8bbf7379b08323910de41d1d8ae647e09c9b5ab68c239581da5c37223ef4e291`；Git blob=`90573097588d63e5182d0b7a509b2580e10ca009` |
| structured-state-board blob | `611e75d97234131acd5f321b5c7b75f50c1960ef`（不变） |
| delivery-progress blob | `64e060b1febf746a05aa07494755a7f9d6eee600`（不变） |
| risk-review blob | `e602fe1a3343a28b472259ae46cfca780e780e48`（不变） |
| Runner SHA | `f61c738c72e51b77298cc1c14c7c6ebf4b6c527d`（不变） |

parent_identity 与 base Git/source metadata 对应，保留原 v7x manifest hashes、四个 Skill blobs；adopted_mechanisms 只追加一个 M5 机制。runtime_contract_delta / rejected / deferred / architecture / runner identity 无变化。

canonical packager 本地输出：[submission](../../../.local/scratch/s09-05/submission/)。仅含 manifest.json + 恰好四个 `skills/<name>/SKILL.md`，与 canonical sources 逐字节相同；Runner 的 `validate_submission_contract` 离线返回 `submission_mode=skill_bundle`、四个预期skill_ids。独立 packaging test 两次构建逐文件字节一致。没有 install/reload，也未启动 Runner play/validate CLI。

包内受保护 Skill bytes/SHA：Board 5252 / `e2f31a83b357f2f75b1e2c0e8285fba440a17d3c4c4c8d6587b4f2e5fa9f366c`；Delivery 5041 / `200b6c83aaca43f6dccfe58a30e23e79463e930512ef89cf5b19070a9d5d7528`；Risk 4189 / `6da910fa60b07dfdccfc78a840ebc4777fc39e3188358e69ee483c89606874fd`。

## 5. Static scenarios / regression negatives

以下为 written protocol 的静态审阅及条款测试，不执行 toy policy、provider 或游戏；不声称观察到模型真实选择。

| Scenario | Expected contract behavior / review result |
|---|---|
| A 当前深夜工作/雨/感染等明确暴露，合法低暴露路径保留相同交付与可比成长、无continuity牺牲 | 在A中可偏向低暴露。必须证明所有当前条件；实际历史雨中拼车费用未知时不直接判cheap |
| B 低暴露牺牲binding交付或明确更高价值成长 | 不授权prior，原Portfolio/realization exception仍可选成长；不自动走安全路径 |
| C 只有Health低、数值下降、普通疲劳/负荷 | 不触发Story prior；数值本身也不能授权S |
| D 旧Story暴露已结束，fresh当前事件无暴露 | 旧choice授权失效；旧S/旧recovery/旧context不可续期 |
| E 成本、可比成长或减曝语义未知 | 不自动偏向低暴露；不得补未选项effects、Health增量或安全概率 |

S09-04 的负例保持为 offline 审查案例，不嵌入runtime lookup：v7x #7 本周联合改进、#17跨组高价值评审、#28减少投入但转职/continuity代价，均不自动判cheap；#10热面或末班车、#18风险文档或附录成本/身体语义不清，均不得自动偏置；#29回归技术路线没有明确休息/减曝语义，不重标成Health保护。没有every-quarter Health quota、fill-to-full或固定shock reserve。

## 6. Tests / affected current assertions

供给定向测试首次 **5 passed**。随后当前/相关historical suite首次 **24 passed / 9 failed**；失败包含旧current identity、CURRENT_STATE旧断言和压缩措辞，非live/runtime失败。

有界修正：

- `test_candidate_v7_contract.py`：当前Candidate父链/hash/机制更新至v7y；压缩后的等价语义字串与<=5000 gate；继承策略完整检查不删除。
- `test_candidate_v7s_contract.py`：只更新current身份/flags断言，保留历史v7s review内容检查。
- `test_candidate_packaging.py`：current package identity更新，其确定性、准确四Skill、frontmatter/contract仍保留。
- `test_s08_10r_v7v_preflight_ordering.py`：current identity/parent改v7y；历史v7v snapshot、原frozen base均保留，继续检查继承runtime。
- `test_s09_03_nonsticky_stabilization.py`：v7x静态identity/reset及原manifest delta固定到 **`43258d41a02ac65c9f1e5d0367ca7612a36c7da7`**；不将已跑过v7x的flags重写为false。对当前descendant继续检查非粘滞S，仅适配压缩措辞，不弱化退出/重授权。
- 新S09-05 test新增精确Planning单条增量、non-kernel完整比较、A–E参数化条款、job continuity/generic负荷、非粘滞/strong prior/Level-context范围及广义Health比较禁止测试。没有用模拟策略测试冒充LLM行为。

最终根解释器命令：

```powershell
D:\CS\CareerSim\.venv\Scripts\python.exe -m pytest tests/test_s09_05_story_exposure_guard.py tests/test_candidate_v7_contract.py tests/test_candidate_v7s_contract.py tests/test_candidate_packaging.py tests/test_s09_03_nonsticky_stabilization.py tests/test_s08_10r_v7v_preflight_ordering.py tests/test_s08_10_runtime_adherence_protocol.py -q --tb=short
```

**46 passed**（S09-05 13；其余33）。未重复全仓测试。identity/hash/blob、exact四Skills、确定性包、review/high-score core/NO_GAIN/quarter/persistence/recovery、历史v7x snapshot、non-kernel比较均覆盖。

`git diff --check`、JSON parse、selected-file canonical secret scan PASS。base protected-surface diff 对 Board/Delivery/Risk、`career_sim_runner/**`、`pyproject.toml`、`uv.lock` 均为空；未写local retry/runtime、HPL或holds。临时供给副本、包和校准脚本均在gitignored `.local/scratch/s09-05/`，不提交raw或private configuration。

## 7. Decision / permissions / execution metrics

`S09_05_V7Y_STATIC_STORY_EXPOSURE_GUARD_PASS_RETURN_TO_STAGE_REVIEW`

实现、静态验证与本地包有效；gameplay/runtime adherence、survival/score improvement、hidden transfer均未验证。S09保持ACTIVE，下一行动由Stage决定，本任务无run授权。

`provider=0; service=0; MCP=0; game=0; install=0; reload=0; HPL_COORDINATION_IMPACT=NONE; NEXT_GAME=NOT_AUTHORIZED`。

所有existing FORENSIC_HOLD保持现状；不复制/扫描其它session或访问shared DB。除供给patch的边界措辞校准和stale current tests外，无scope deviation；父链、机制收益与historical evidence分开记录。

Execution metrics：记录点2026-09-30 23:00:56 Asia/Shanghai（UTC15:00:56，预览/加载期；完整turn start UNKNOWN）；完成时间与可得wall区间见TASK_RESULT。pytest 3次（定向、诊断、最终）；供给apply 1次；canonical离线包1次，加packaging tests内部确定性构建。Model/effort/tokens/billing UNKNOWN；live attempts=0。最终commit/push/clean身份见TASK_RESULT，避免self-referential hash。
