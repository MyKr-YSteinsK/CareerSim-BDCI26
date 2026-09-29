# Final Submission Contract｜最终比赛提交合同

## 0. 优先级

这是项目结束阶段的最高优先级交付合同。

最终目标不是“有一个能运行的目录”，而是生成一个经过独立审计、可直接上传的：

`solution.zip`

最终提交任务属于 **Tier 3 / official submission**。

在最终 Candidate 未冻结前，不得把任何临时 ZIP 宣布为正式提交件。

## 1. Source of Truth

最终打包前必须重新核验：

1. `docs/project/OFFICIAL_SOURCE_LOCK.md`；
2. 官方比赛页面当天最新通知；
3. 官方 `openJiuwen-ai/CareerSim-BDCI26` 提交 README / contract；
4. 当前冻结 Runner 的 submission validator；
5. 当前 `configs/current_candidate.json` 与 canonical runtime files。

若当天官方通知与历史 Source Lock 冲突：

`STOP → 更新 Source Lock → 重新审查 → 再打包`

不得为了赶提交跳过冲突。

## 2. Freeze Gate

正式 `solution.zip` 只允许从最终冻结 Candidate 生成。

最终打包前，`configs/current_candidate.json` 必须明确：

```text
status = FINAL_FROZEN_FOR_SUBMISSION
next_game_authorized = false
```

并记录最终 Git commit。

禁止：

- 从 dirty working tree 打包；
- 从未提交文件打包；
- 打包后继续修改 runtime Skill/manifest 而沿用旧 ZIP；
- 把一次临时验证包改名为 final ZIP。

任何 runtime 字节变化都使旧 `solution.zip` 失效。

## 3. Official Layout

当前冻结官方合同要求：

```text
solution/
  manifest.json
  README.md
  design/
    skills_design.md
    decision_report.md
  skills/
    <skill-name>/SKILL.md
```

本项目当前为四个 Skills：

```text
structured-state-board
rolling-planning
delivery-progress
risk-review
```

最终 ZIP 默认保留顶层 `solution/` 目录。

如果最终提交当天官方上传 UI / 最新官方说明明确要求 archive root 直接为 `manifest.json`，则允许使用 contents-only layout；该改变必须记录当天证据，不得凭猜测切换。

## 4. manifest.json

最终 manifest 必须：

- `team` = 比赛平台真实团队名；
- `name` = 最终提交名称；
- `mode` = `agent`；
- `instruction` = 最终冻结 `configs/runtime_manifest.json` 的 instruction，逐字一致。

禁止：

- `local-*` 开发标签冒充真实团队名；
- placeholder team；
- 临时 Candidate 名与最终 manifest identity 不一致；
- 在最终打包时重新人工改写 instruction。

## 5. Skills

最终 `skills/*/SKILL.md` 必须来自最终冻结 canonical Skills，逐字节一致。

每个 Skill 必须：

- 有合法 YAML frontmatter；
- `name` 与目录职责一致；
- 有非空 `description`；
- 不包含 secret；
- 不包含 Dev-only threshold / hidden answer lookup；
- 不依赖未提交的本地文件。

最终包不得混入 retired Skill、测试 fixture、实验 Skill 或历史 Candidate。

## 6. README 与 Design

最终材料源文件固定放在仓库：

```text
submission_materials/
  README.md
  design/
    skills_design.md
    decision_report.md
```

最终冻结前必须根据最终 Candidate 刷新，禁止保留 `TODO_FINAL`、`FINALIZE_ME`、`YOUR_TEAM_NAME` 等占位符。

### skills_design.md 至少覆盖

- Single Agent + Four Skills 架构；
- 四 Skill ownership / I/O / 禁止职责；
- Board → Delivery → Planning → Risk 协同；
- Structured public evidence；
- Long-horizon Review Window；
- Failure Recovery taxonomy；
- Risk gate；
- whole-game persistence；
- context recovery；
- 为什么暂不使用 Team/Swarm、第五 Skill、durable Memory；
- Token / reasoning / Skill-load 开销控制。

### decision_report.md 至少覆盖

只写有证据支持的最终决策：

- Evidence → Hypothesis → Experiment → Decision；
- 关键 Candidate / Run 结果；
- 高分路径与失败路径；
- 失败恢复改进；
- 重要 rejected / deferred 方案；
- 当前 limitation / UNKNOWN；
- final Candidate 为什么被冻结。

不得把单局结果写成稳定收益，不得编造隐藏 Test 表现。

## 7. Secret / Contamination Gate

ZIP 只能包含官方白名单文件。

禁止进入 ZIP：

- `.env`
- API key / token / password / credential
- private runtime config
- shared DB
- transcript / events / logs
- Git metadata
- tests
- experiment artifacts
- `.local`
- cache
- provider response
- hidden/Dev forensic data
- source-code repository的其它文件

最终 builder 对选定文本执行 secret pattern scan。命中疑似凭据时 STOP，人工审查后才能继续。

## 8. Validation Layers

正式 ZIP 必须同时通过：

### V1 Canonical Identity

- clean tree；
- HEAD = origin/main；
- final Candidate status；
- manifest hash；
- instruction hash；
- 4 Skill Git blob / SHA；
- submission docs 为当前 final commit 内容。

### V2 Official Material Layout

精确存在：

```text
manifest.json
README.md
design/skills_design.md
design/decision_report.md
skills/<4 skills>/SKILL.md
```

不得缺失官方材料。

### V3 Frozen Runner Contract

对解压后的 submission root 执行离线：

- submission layout；
- manifest fields；
- Skill frontmatter；
- skill bundle identity。

不得因为 Runner validator 不检查 design docs 就省略官方材料。

### V4 Byte Identity

ZIP 解压后：

- `instruction` 与 canonical runtime manifest 一致；
- 四个 Skill 与 canonical Skill 字节一致；
- team/name 仅由 final packaging 参数注入；
- design/README 与 `submission_materials/` 字节一致。

### V5 Secret Scan

PASS。

### V6 ZIP Integrity

- archive 可完整解压；
- 无重复 member；
- 无 absolute path；
- 无 `..` path traversal；
- 无意外文件；
- 每个 member 记录 SHA-256；
- ZIP 记录 SHA-256。

## 9. Deterministic Build

最终打包使用仓库：

`scripts/build_final_solution.py`

默认生成：

```text
dist/final/solution.zip
dist/final/solution.zip.sha256
dist/final/solution-manifest.json
```

ZIP 使用确定性 member order 与固定 timestamp，保证同一输入重复构建产生一致 artifact。

`solution-manifest.json` 不放入比赛 ZIP；它是本项目的 provenance sidecar。

## 10. Pre-upload Final Gate

在真正上传前，必须再次确认：

- 当前日期/截止时间；
- 当天提交次数限制；
- 官方页面是否更新格式；
- team name；
- 上传文件就是刚验证的 SHA-256；
- 不存在更新后的 runtime commit；
- ZIP 大小可被平台接受；
- 源代码与最终提交版本已保存用于复现审核。

上传本身不是测试动作。

若赛事每天提交次数受限，禁止用未经完整 V1–V6 的包试传。

## 11. Final Deliverables

最终必须同时交付给用户：

1. `solution.zip`
2. `solution.zip.sha256`
3. `solution-manifest.json`
4. 最终 Git commit SHA
5. 最终 Candidate ID
6. Final Submission Audit 简报
7. 可下载链接

只有全部完成，才允许使用：

`FINAL_SUBMISSION_PACKAGE_READY`

## 12. Stop Conditions

以下任何情况 STOP：

- official contract 有新变化但未重新核验；
- team name 未确认；
- Candidate 未 `FINAL_FROZEN_FOR_SUBMISSION`；
- working tree dirty；
- main/origin drift；
- runtime hashes 不匹配；
- design docs stale / placeholder；
- Runner submission validation fail；
- secret scan 命中；
- ZIP member/layout 不符合合同；
- ZIP 解压后二次 hash 不一致。

不得为了赶截止时间静默绕过。
