# S09-19｜可见压缩恢复与 Planning 契约重载

## Identity / disposition

- Status: `BLOCKED_RETURN_TO_STAGE`；`IN_FLIGHT_EVIDENCE`。
- Plan: `D:/CS/temp/CareerSim/S09-19-可见压缩恢复与Planning契约重载.md`。
- Evidence parent / task base: `2fc0168253d43b0a2afeb529d311f2f324386307`（S09-18）。
- Authorized dependency branch: `codex/s09-14-v9a-static`。
- Main / origin/main: `6a4037fdf2b75c105cfe0b40b93ea68d3dd0a6f3`；v8a freeze unchanged。
- Candidate remains `candidate-v10b-policy-constitution-anti-saturation`；v10c **NOT_CREATED**。
- Decision: `S09_19_RECOVERY_TRIGGER_DEDUP_NOT_IMPLEMENTABLE_RETURN_TO_STAGE`。

Plan §7 / §17 明确要求：若当前 repo-owned surface 无法可靠区分同一 wrapper 与新的 compression epoch，停止实现并返回 Stage。本任务达到该条件。未交付 runtime patch，不将部分静态探索标记为恢复修复通过。

## FACT｜可见信号与受保护尾部

现有 [S09-18 evidence](S09-18_RUN11_LAYERED_EVIDENCE.json) 的信号可见结论仍成立；本次阻断是 epoch 去重，不是首次信号检测。

定向读取 frozen installed source（只读）：

| Local source under `.venv/Lib/site-packages/` | Relevant behavior |
| --- | --- |
| `openjiuwen/core/context_engine/processor/forked/compressor/current_round_compressor.py:46–60` | 保存最新真实用户请求之前的 prefix，压缩中间部分，保留最近消息尾部。 |
| `openjiuwen/core/context_engine/processor/forked/compressor/base.py:95–118,126–132` | 工具边界可扩展尾部；memory wrapper 不作为最新真实用户请求。 |
| `openjiuwen/core/context_engine/processor/forked/compressor/base.py:281–296,603–615` | 新 wrapper 被插入保留尾部之前；可在其后重新注入 Skill/plan 信息。 |
| `openjiuwen/core/context_engine/processor/forked/compressor/base.py:627–635,668–675` | recall ID 依赖可选 recall archive；无 archive 时 wrapper 没有该标识。 |

精确 RUN11 source 为本地 `.local/runtime/s09-run11-v10b/service-stdout.log`：

- 配置行 298/299/458/459 显示实际 `keep_recent_messages=4`，不是 source 默认值。
- 输入行 6846、11676 的 message index 2 均为 user-role `<memory_block_current>`；均无 `COMPRESSION_RECALL` marker。
- wrapper 后仍有未压缩的 assistant/tool 尾部；历史 START/部分恢复内容可以保留在新 wrapper 后。
- 本次未读取 shared DB、查询 Provider 或启动任何 runtime；未将原始日志复制进 Git。

## MEASURED｜最小去重歧义反例

纯离线合成消息，使用上述 prefix / middle / recent-tail 规则；尾部两组 tool call/result 完整，故 tool-boundary adjustment 不改变本例。

设 `M` 为合法 wrapper 文本，`T` 为四条保留消息：一组普通 observe call/result，以及一组带恢复 START 的 observe call/result。所有 session 标识均为合成值。

| History | Current model-visible role/content sequence | Required transition |
| --- | --- | --- |
| A：同一 wrapper 下恢复尚未完成 | `[user request, M, T]` | 继续当前恢复，不为同一 epoch 再启动一次恢复。 |
| B：恢复中途再次压缩 | `[user request, new M, T]` | 旧部分恢复失效，为新 epoch 执行完整恢复。 |

框架未保证每个新 summary 文本都不同。令 B 的新 `M` 与 A 的 `M` 文本相同，则两份当前可见输入完全相同，包括保留的 tool call IDs；新 host message 的对象身份不等于模型可见 epoch ID。

纯离线 witness 执行结果：

```text
model_visible_inputs_identical=true
same_summary_guaranteed_different_by_runtime=false
object_identity_or_host_event_id_available_to_model=false
visible_input_sha256=c82d5e92d175c9f9839f0ee9cef84749fea67b470de6f6c5e56ac31c40f1aa62
```

这证明仅按当前可见输入的 wrapper 内容、位置或 START/READY receipt，不能可靠选择这两种不同的必需状态转换。它是允许输入形状的合成反例，**不声称 RUN11 实际生成相同摘要或在恢复中途再次压缩**。

完整未压缩恢复链可以支持部分情形的去重，但不能解决上述恢复中途的歧义。每次看到 wrapper 都重新读取会违反 anti-loop；信任新 wrapper 后的旧 START 会漏掉新 epoch；遇到歧义永久 BLOCKED 也不构成 Plan 所需恢复实现。

## Scope / verification boundary

`scripts/package_candidate.py` 的 canonical submission 包含 manifest 与四个 Skill 文件。离线 Python helper 不会自动成为已部署的 runtime 控制器。本次未找到可证明属于当前比赛提交范围、且无需改变 frozen framework/Runner 的独立 epoch 状态 seam。

| Item | Result |
| --- | --- |
| Visible wrapper existence / recall-marker absence | Verified on two exact RUN11 model-input captures |
| Partial-recovery ambiguity witness | PASS, pure offline synthetic comparison |
| F1–F12 accepted recovery implementation fixtures | NOT_RUN；在实现 hard stop 后不继续构造通过假象 |
| RUN11 epoch1/epoch2 new-contract counterfactual replay | NOT_RUN；没有可交付的新恢复合同 |
| Regression / package validation / v10c gate refresh | NOT_RUN / NOT_CREATED；父 Candidate 未改变 |
| Four Skills / Planning / manifest / Candidate / audit tools / Runner / dependencies | No edits |
| Document checks | UTF-8/structure and secret scan; `git diff --check` |
| Provider / service / game / MCP / DB / install operations | 0 |

一次性的 proof 与未交付 prototype 留在 ignored `.local/scratch/s09-19/`，不是 runtime implementation，也不是唯一历史取证来源。本报告包含独立可审的反例与准确来源位置；RUN11 raw 的既有 `FORENSIC_HOLD` 继续有效，不删除、不解除。

## Return to Stage

RECOMMENDATION：后续如要同时保证 once-per-epoch 与新 epoch 完整重载，需先取得可证明的 model-visible、host-issued epoch identity，或已获准且可提交的 runtime seam，并单独确认 frozen source / competition comparability 边界。不得把内容 hash、时间阈值或 summary 中自行宣称的 receipt 当可靠 host epoch。

未创建 v10c，不刷新其 VALUE_OF_RUN_GATE，不升级任何 validation flag；不宣称 `RECOVERY_CONTRACT_RESTORED_STATICALLY`、模型恢复遵循或 `C6_RUNTIME_FIXED`。Provider HTTP402 / balance-restoration 要求仍是独立的未来 live gate。

```text
NEXT_GAME=NOT_AUTHORIZED
NO_REPLACEMENT_RUN_AUTHORIZED
MAIN_V8A_FREEZE_UNCHANGED
```
