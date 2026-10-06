# 最终提交身份与构建记录

历史交付时点（本文件所在交付 commit）：状态为 `IN_FLIGHT_EVIDENCE`，最终打包事实已记录但尚待 Main 接受；该记录不表示当时 Stage 已 COMPLETE。Main 后续已关闭 S10，见 [AD-S11-001](ARCHITECTURE_DECISIONS.md)；当前阶段见 [CURRENT_STATE](CURRENT_STATE.md)。

- Decision: `FINAL_SINGLE_SHOT_V6_READY` / `SELECT_EXACT_V6_FOR_SINGLE_SHOT`。
- Candidate: `candidate-v6-auditable-control-loop`；parent `candidate-v5-evidence-driven-phase-policy`。
- Runtime Git source: `1114a04b75548cf52f030d123564e527060fc061`。
- Clean-main build commit: `113052a9a8943efc7fb2d7d1140f126e62e92040`，构建时 HEAD=origin/main，工作区 clean。
- Audit delivery commit: 本文件所在提交；最终 push/clean/ZIP 不变复核记入本机 delivery-receipt.json，并在交付回复给出实际 commit。
- Task base: `24be9e49cded74dba2559aade3a7cac870ddd54c`；remote `https://github.com/MyKr-YSteinsK/CareerSim-BDCI26.git`。
- Explicit authority: S10-23R-v2。checkout 中旧 v8a runtime 未变，不是最终来源；冻结见 [identity](FINAL_SUBMISSION_IDENTITY.json)。
- Build command: root project Python `scripts/build_final_solution.py --exact-v6 --team FZU-Loss快点降 --name FZU-Loss-final-v6 --output .local/runtime/s10-23-final-v6/FZU-Loss-final-v6.zip --archive-layout solution-dir`。

## 唯一上传件

- Path: `D:/CS/CareerSim/.local/runtime/s10-23-final-v6/FZU-Loss-final-v6.zip`。
- Filename: `FZU-Loss-final-v6.zip`。
- SHA256: `31e836b591703dfe520916828da033a57de260bb451d97047bbaee9daaa11b9b`。
- Bytes: 18082；7 files，`solution/` 根。
- Final hash sign-off: `2026-10-05T09:17:25.633711+00:00`；之后禁止重建或重压缩。
- Team: `FZU-Loss快点降`；name `FZU-Loss-final-v6`；mode `agent`。
- Historical manifest SHA: `bcf459da811f55b8a26a76d2ee6e93da10deb4b720cc732d19a3ce12d8fa2985`。
- Final manifest SHA: `59f3f26e454f1390a7c1344fa3372f293985fed0872bc2915175d43922ac3449`。
- Historical AND final instruction SHA: `7131bbd652452c71571f1ab99451f210e6e52601e9d66144d3d665337b4eb33c`。
- Only changed manifest fields: `team`, `name`；`RUNTIME_DELTA=NONE`。

| Member | SHA256 |
|---|---|
| `solution/README.md` | `3a3ba03f05708c7ba9aecd1e22405290030b2c12a8b246fd1cc5fe0f534fa9b4` |
| `solution/design/decision_report.md` | `22b4689e1995a11b8b8d9fa3429a4ba42b943cbc0fee2894b3f7c9fae069acd7` |
| `solution/design/skills_design.md` | `a88a519f491ea08ca618c3a68b5b3f04baca6c7feeae63808e68cacece1202cc` |
| `solution/manifest.json` | `59f3f26e454f1390a7c1344fa3372f293985fed0872bc2915175d43922ac3449` |
| `solution/skills/risk-review/SKILL.md` | `fcae2368e012c2bb64b179fd42f1dfba46ee97300a78bf0654a195e4f08a2823` |
| `solution/skills/rolling-planning/SKILL.md` | `51a06fa4ae56d675b58e8f41aa66d2440ce43617acbd5b35ee907b226b09d799` |
| `solution/skills/structured-state-board/SKILL.md` | `f1e1be0ac6c537e8702c4b246af11559d25c3573190206e289b4d9fe73b7b24c` |

## 校验与留存

官方源仓库于 2026-10-05 核对，远端 main 仍为 `f61c738c72e51b77298cc1c14c7c6ebf4b6c527d`。当前 README 格式与冻结 validator 一致；门户通知/上传窗口 UNKNOWN。见 [Source Lock](OFFICIAL_SOURCE_LOCK.md)。

官方 `validate_submission` 材料函数对独立恢复源目录及新鲜解压目录均 PASS。CLI 全环境 validate 未执行，因为会涉及环境/DB 检查；无服务、Provider 或云端运行验证。安装复核使用官方 reset/copy/registry/identity 函数，路径全部指向本机隔离 fixture；未调用完整共享 install 或初始化实例。Skill discovery（官方 bundle 枚举、frontmatter、enabled registry）3/3 PASS；不代表已测模型启动后的加载行为。

UTF-8 无 BOM、七文件 allowlist、字节一致性、secret/local-path scan、确定性重建比较 PASS。官方 normalize_text 对历史 instruction 过滤箭头的既定行为在隔离 IDENTITY 渲染中一致，没有改包内 instruction。13 targeted builder tests PASS，`git diff --check` PASS；Runner/依赖/config/正式 Skills 无 delta。

本地留存：ZIP、sha256 sidecar、solution-manifest.json、final-audit.json、documentation-review.json、validated-source/solution、extracted/solution、install-check，均位于 `.local/runtime/s10-23-final-v6/`；不进入 ZIP 或 Git。既有 FORENSIC_HOLD 不变，不删除历史证据。提交材料的可恢复来源是构建 commit，运行来源是不可变历史 commit；仅 hash 不替代最终 ZIP 留存。

## 最后上传检查

SHA256：`31e836b591703dfe520916828da033a57de260bb451d97047bbaee9daaa11b9b`。

1. 只上传本报告指定的 `FZU-Loss-final-v6.zip`。
2. 核对本地 SHA256 与本报告一致。
3. 打开归档，确认根层直接为 `solution/`。
4. 检查 `manifest.team = FZU-Loss快点降`。
5. 检查 `manifest.mode = agent`。
6. 检查恰好三个 Skill 目录。
7. 不上传旧 v6d/v8a 包。
8. SHA 签定后不重新压缩。
9. 在本地保留实际提交的同一 ZIP。
10. 保存门户上传回执或截图。

`RETURN_FOR_FINAL_UPLOAD` · `DO_NOT_REBUILD_AFTER_FINAL_HASH` · `NEXT_GAME=NOT_AUTHORIZED`
