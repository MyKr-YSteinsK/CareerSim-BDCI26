# S09-20｜无感压缩常驻内核与 Preflight 加固

## Identity / decision

- Status: `STATIC_PASS_RETURN_TO_STAGE`；`IN_FLIGHT_EVIDENCE`。
- Parent / evidence base: `candidate-v10b-policy-constitution-anti-saturation` / `63c703f8979a4bebf7d1bc72249019a56343550e`。
- Candidate: `candidate-v10c-compaction-agnostic-kernel`。
- Implementation: `55157f53031c284e2e569944e4aff6adbf64c48f`，authorized branch `codex/s09-14-v9a-static`。
- Strategy delta: `NONE`；runtime delta: `COMPACTION_AGNOSTIC_ALWAYS_ON_KERNEL_AND_BASIS_PREFLIGHT`。
- Decision: `S09_20_V10C_COMPACTION_AGNOSTIC_KERNEL_STATIC_PASS_RETURN_TO_STAGE`。

## Ownership / minimal changes

依据 RUN11 system-owned CTRL/DL 183/183、Planning-owned POL/PROBE 48/183 与 S09-19 epoch 歧义，将小型 public-basis kernel、精确 schema 和 final basis gate 放入 manifest/system。这是常驻模型执行合同，没有新增 host hook、外部工具拦截器、Skill、Memory、Team 或压缩 epoch 检测。

| Owner | Contract |
| --- | --- |
| Manifest/system | K1 public evidence；K2 不虚构 saturation；K3 fresh public binding 才 S；K4 cleanup fresh authorization；K5 summary 非 authority；CTRL/DL/POL/PROBE 必需格式；BASIS_CHECK / one-action preflight |
| Planning | 原 C1–C10、One Master Ranking、Main/Energy controllers、probe 五条件及 E/C/S 语义、Review Plan/local NO_GAIN/Level reset |
| Board / Delivery / Risk | 原事实、交付 lifecycle、final Risk gate；文件未改 |

Planning 仅两处执行/格式 ownership 调整：

1. 原 context recovery 的 `RECOVERY_PENDING → 四 Skills → RECOVERY_READY` 段改为服从当前 manifest；缺失 UNKNOWN，不识别 epoch。这是执行合同引用，不是 ranking 改写。
2. 移除 `Decision closure / trace` 下 POL/PROBE 两行格式 code block，改为引用 system schema；后面的完整字段/probe 语义段保持原样。

采用 Option B，减少双份格式 owner。旧 manifest 的初期策略 prior prose 由未改的 Planning controllers/ranking 承载；整份 Constitution 未迁入 manifest。首次四 Skill 顺序读取保留；summary 出现、持续、更新不触发强制重读。确实缺失详细语义时，该次决策最多一次按需读取对应 canonical Skill，仍不清楚则 UNKNOWN/BLOCKED，不能声称已重读。

新增 Candidate-specific [runtime contract profile](../AGENT_RUNTIME_CONTRACT.md) 与 [AD-011](../ARCHITECTURE_DECISIONS.md)，显式覆盖该实验 Candidate 的旧 epoch gate；历史 v10b / main v8a profile 不变。

## Preflight / observability

`BASIS_CHECK=PASS` 仅在 current public rationale、无受禁 effect、无 unsupported cap、S 有 fresh material binding、cleanup 有 fresh authorization、control/schema 合法时成立。notes 在 PROBE 后附 `[BC=PASS]`。

失败置 BLOCKED；非提交 executor 输出 `[BC=BLOCKED WHY=<PUBLIC|SATURATION|NUMERIC_S|STALE_CLEANUP|SCHEMA|CONTROL>]`。在已有 fresh public basis 上最多一次 repair，与既有 Risk reconsideration **共用**一次 closure budget，不增加第二 branch；重做 final Risk/READY/preflight，仍无效 STOP_BEFORE_ACTION，不为修理由额外 observe。

`scripts/basis_preflight_audit.py` 是离线标注证据 contract oracle / receipt measurement，不装入 submission，不自动判断任意自然语言、不执行 live 拦截。`scripts/policy_trace_audit.py` 仅增加 scoped action-note BC measurement；`parse_header` / `parse_trace` AST 完全相同，旧 measurement status 与严格 parser 不放宽。

报告 BC present/valid/PASS、四 marker coverage、submitted despite BLOCKED。非提交阻断类别可从已去重、准确 scoped 的 explicit executor receipt projection 测量；当前 events-only 路径未证明该 projection 完整，四类 non-submitted blocked counts 默认 `null/UNKNOWN`，不是零。PUBLIC 指 nonpublic/restricted basis；依据无法核实归 CONTROL。PASS receipt 是模型主张，不能证明 rationale 合法或外部拦截生效。

## Verification actually passed

| Check | Result |
| --- | --- |
| S09-20 targeted suite | 43 PASS：28 annotated scenarios、8 RUN11 projections、ownership/identity/package/measurement checks |
| Existing strict trace / Value-of-Run fixtures | 17 PASS；历史 v10a identity assertions 不属于本 Candidate |
| Post-run audit fixtures | 27 PASS |
| Total | 87 targeted checks PASS |
| Protected strategy | C1–C10、ranking、Main/Energy controllers、POL/probe semantics 一致；Planning diff 仅上述两处 |
| Protected assets | Board/Delivery/Risk、post_run_audit、packager、dependencies byte-equivalent；Runner/framework 未改 |
| Canonical package | `skill_bundle`，恰好四 Skills，源 bytes 匹配；`.local/runtime/s09-20-v10c/submission`，未 install |
| Hygiene | JSON/Python parse、bounded secret-pattern scan、`git diff --check` PASS |
| Live/provider/service/game/MCP/DB/install | 0 |

manifest instruction：**4,373 → 4,786 chars（+413，+9.4%）**。增长用于 system schema/basis ownership；删除旧 epoch recovery、重复 startup/restart 和策略 prior prose，Planning 删除双份模板，未复制全宪法。有限增长通过 task-specific 10% growth guard；它不是官方上限。Frozen local `career_sim_runner/skill_contract.py` 未发现显式 instruction 长度门槛，当前离线包被接受；不据此声称云端接受或无限 runtime capacity。

### RUN11 sanitized replay boundary

只用 S09-18 已审语义与 paired notes 的结构 marker；不复制原始 prose、private effects/values 或 replacement choices：

| Projection | New contract verdict |
| --- | --- |
| a47 pre-compression valid-schema baseline | PASS under explicit public-basis annotation；不回填历史 BC |
| a48/a50 | BLOCKED：malformed/missing POL/PROBE |
| a98 | BLOCKED：numeric-only S + schema |
| a135/a159 | BLOCKED：restricted basis、unsupported saturation、stale cleanup + schema |
| a147 | BLOCKED：restricted basis、saturation + schema；有新 minor warning，但足够 cleanup authorization 未建立，记 UNKNOWN/fail closed，不宣称无 fresh warning |
| a161 | BLOCKED：restricted basis / unsupported saturation + schema |

结果依赖明确标注的 public-context 事实投影，是 `CONTRACT_COUNTERFACTUAL_REPLAY`；不是 NLP detector、模型行为、历史动作实际被拦截或 alternative score 提升证明。RUN11 BC 仍 ABSENT，不伪造历史 receipt。

## Gate / return boundary

[S09-20 VALUE_OF_RUN_GATE](S09-20_VALUE_OF_RUN_GATE.json) 冻结 implementation、manifest/instruction、metadata、四 Skills、tests/fixtures/audit tools、dependencies 与 package bytes。Report-only descendants 必须保持冻结资产；未来另行授权 Plan 冻结自己的 clean exact execution HEAD。

未来 live 仍须：用户确认 Provider balance/credit 恢复；exact identity、schema/basis/replay PASS；早期 bounded heartbeat 验证 BC、四 markers 及 public rationale 无 saturation/restricted basis。**不再要求 compression epoch heartbeat。** 本任务没有 balance probe 或 live permission。

所有 validation flags=false；不继承 v10b/RUN11 证据，不宣称 C6_RUNTIME_FIXED、runtime validated、score improvement 或高分稳健性。既有 raw FORENSIC_HOLD ACTIVE，未清理/解除；HPL/main freeze 未变。

```text
NEXT_GAME=NOT_AUTHORIZED
NO_REPLACEMENT_RUN_AUTHORIZED
MAIN_V8A_FREEZE_UNCHANGED
```
