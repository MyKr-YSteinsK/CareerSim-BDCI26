# TASK_RESULT｜S10-08 Experience-Routed Policy Atlas

## Result / identity

- **Status: Complete**（限静态实现、离线验证和 branch 交付）；`IN_FLIGHT_EVIDENCE`。
- **Decision: READY_FOR_EXPERIENCE_ROUTED_GAME_GATE**；Main/Stage 路线验收与 live gate 尚待另行授权。
- Branch：`codex/s10-08-experience-routed-policy`；Base/parent HEAD：`8267d420da29888d0a05403991f8980e251aaa0c`，建分支前 fetch 并确认该 main/origin-main 基线。
- Candidate：`candidate-v14-experience-routed-policy`；parent/fallback：`candidate-v8a-v7o-donor-core-transplant`，main 不改。
- Delivery commit：引入本报告的 commit（`git log -1 --format=%H -- docs/project/reviews/S10-08_EXPERIENCE_ROUTED_POLICY_STATIC_REVIEW.md`）；精确 SHA、remote 一致与 clean tree 由最终交付回执返回，避免报告自包含自身 SHA。
- Remote：`https://github.com/MyKr-YSteinsK/CareerSim-BDCI26.git`；只 push 此任务分支，不 merge、不改 main、不改写历史；没有 worktree。
- Manifest actual UTF-8 LF source SHA-256：`755799f24d70882b4c8054845c2a0eb94a66a63e908f0662b07640fc9a911122`。Skill/reference Git blob 身份在 `configs/current_candidate.json`；reference SHA 是交付 source bytes。Windows 以后 CRLF checkout 可能改变字节 SHA，Git blob 用于固定版本身份，未来安装须核对实际包字节。
- **NEXT_GAME=NOT_AUTHORIZED**；没有生成官方 `solution.zip`，没有改变官方提交选择。

## What changed / distillation

三份 active Skills：`career-policy-core`、`career-policy-atlas`、`career-survival-guard`。四份历史 Skill 源文件在本实验分支被替换，frozen v8a 仍由 main 精确恢复；不把退休正文留作 active Skill。六张 reference：`review-promotion.md`、`energy-resource.md`、`project-delivery.md`、`trust-compliance-conflict.md`、`health-survival.md`、`visibility-network-learning.md`，均在 `skills/career-policy-atlas/references/`。

正参考 v6/v7o/v8a RUN07/RUN10；负参考 RUN08/RUN20/v12/v13。只用已接受公开衍生报告，v13 报告固定 `7bd7c92fb43e4642077469cc6d316eaf15a7979f`，v6 原候选固定 `1114a04b75548cf52f030d123564e527060fc061` 用于静态正文计量；不合并 S10-06/07，不重新打开 held raw。24条候选经验 →14 KEEP /6 MERGE /4 REJECT；独立经验置信度 HIGH4/MEDIUM8/LOW2；六卡 HIGH1/MEDIUM5，Review 的早期复利和末期先验仍 LOW。完整正负对照、最小程序及例外见 [research atlas](../research/S10_EXPERIENCE_POLICY_ATLAS.md)。没有重建隐藏风险、event/title答案映射、promotion公式或隐藏 cap。

## Progressive disclosure / actual interface evidence

| 决策阶段 | 需要的正文集合 | 条件 |
|---|---|---|
| Startup | core | 不要求预读 atlas/guard/六卡；三个 Skill 的名称/description 可由 discovery 公开 |
| Ordinary Story | core + router + growth 卡 | 当前卡已在上下文时不反复读取 |
| Energy | core + router + Energy 卡 | 一动作后新的 capsule/全菜单比较，optional 不可负担项直接排除 |
| Main | core + router + Project 卡 | 条件性 owner/依赖/兑现比较 |
| Review / no-advance / horizon | core + router + Review 卡 | 重建目标、路径与下一可见 checkpoint |
| Material warning | core + guard + router + health/trust/资源卡 | 优先当前重大约束；一般一张，两独立重大领域才第二张 |

源代码只读核查：installed JiuwenSwarm `0.2.4b3` / openjiuwen `0.1.16.post2`，没有导入/启动 agent 服务。

- `openjiuwen/harness/rails/skills/skill_use_rail.py` 的 `_build_skills_section` / `_build_all_mode_prompt`，以及 `harness/prompts/sections/skills.py:build_skill_line`：`all` 模式注入名称和 description，**不是自动读取所有正文**。
- `harness/tools/skills/skill_tool.py`：默认只读 `SKILL.md`，返回 `skill_directory` 与正文；支持安全相对路径。atlas 首次加载后可用其目录和现有 `read_file` 读取选中的 reference。目录树可以暴露文件名，不能等同全文加载。
- `career_sim_runner/install.py:_install_skill_bundle` 使用 directory copy；卡片不需新安装协议。这里只读实现，**没有调用 install**。
- 旧本机打包器固定四 Skill、只拷 `SKILL.md`，会丢 reference。最小修补改为核对 candidate 的2–4个声明（兼容历史四Skill），保持 metadata/architecture/source 一致并复制 Markdown references；拒绝链接/越界/额外本机资产和非空输出。正常 v14 包为 manifest +3 Skills +6 cards，共10文件。官方 final submission builder 仍冻结，不据此批准正式提交。

这是 submission-valid、具备 normal Skill/read_file 接口的静态证据，**不是模型一定正确检索的证明**。旧卡/工具正文可能留在历史直到宿主压缩，本候选没有控制上下文驱逐；只能规定当前工作集和读取时机。

## Decision kernel / preservation of semantics

每动作前从 fresh public observe 重建替换式 `DECISION_CAPSULE`：同 session/time/Level/公开下一窗口、全部合法选项和显式成本、具体未解除警告或NONE/UNKNOWN、objective/最后正式反馈、当前Level且相关的clean response、必要交付owner/承诺/进展/认可/blocker。缺失 UNKNOWN，不积累旧 capsule 或长 Brief，不跨局保存。

一次完整菜单比较：先去显式不可负担和被安全有效替代明显支配的重大危险项；其余每项看即时公开效果/不确定性和下一可见checkpoint兑现，再按**存活重大约束 → 可兑现晋升/成果 → S/N/O/W及option value → 普通成本**排序。没有隐藏数值、搜索树、固定策略序列、递归自辩或多次“最终选择”。公开警告可采，不因 HiddenRisk禁用而丢弃；退出 guard 必须同范围 fresh clearance，Health、泛夸和receipt不替代。

唯一执行者仍拥有 READY→preflight→单一可负担合法choice→OBSERVE_REQUIRED→同session fresh observe；未知结果、身份/观察失败或preflight错误 BLOCKED，先在授权内核实，仍未知停止，不盲重发、不新开局。可见压缩/恢复重读 core、同session观察、按需读卡并重建；局部决策闭合不结束 active game。历史固定四Skill owner 与CTRL/DL格式不是新候选启动依赖，分支内 Runtime Contract 的窄例外记录这项表示替换；操作语义和 live/retry权限不放宽。

## Context measurement and four-Candidate comparison

Unicode 字符，`len(text)`；manifest 只计 instruction；Skill正文用frontmatter后 `strip()`，reference计全文。旧版本由固定Git LF blob计量，新版本UTF-8 LF源计量。**不包含** discovery wrappers/frontmatter、工具schema、Handbook、菜单/observations、capsule长度、推理、旧tool output和框架提示。因此这是静态策略内容预算，不是实际prompt/token/latency/cost或峰值context测量。

| Candidate / 来源 | Skill数 | manifest | 全Skill正文 | references | startup正文+manifest | 全库+manifest |
|---|---:|---:|---:|---:|---:|---:|
| v6 `1114a04…` |3|943|9,144|0|10,087|10,087|
| v8a `8267d42…` |4|4,373|17,665|0|22,038|22,038|
| v13 `7bd7c92…` |4|4,549|13,741|0|18,290|18,290|
| v14 本任务 |3|1,211|4,327|3,401|3,250（core 2,039）|8,939|

v14 router 1,086 / guard 1,202；六卡分别 Review588、Energy669、Project564、Trust508、Health471、Growth601。正文范围符合 core1500–2500、router<2000、guard1000–1800。v6全Skill文件14,623 bytes（9,545字符）与S08-11一致，不能把bytes冒充Unicode字符。

| TYPICAL_ACTIVE_POLICY_CONTEXT（本次所需策略正文+manifest） | v14 | 相对v8a22,038 | 相对v1318,290 |
|---|---:|---:|---:|
| Ordinary Story |4,937|低77.6%|低73.0%|
| Energy |5,005|低77.3%|低72.6%|
| Main |4,900|低77.8%|低73.2%|
| Review |4,924|低77.7%|低73.1%|
| material trust / health warning |6,046 /6,009|低72.6% /72.7%|低66.9% /67.1%|

第二张卡例外须另加该卡正文；旧卡留在模型历史的累计占用不能从此表推断。startup策略正文+manifest低85.3%/82.2%（vs v8a/v13）；全库仍保留必要例外，没有靠删掉生存/控制约束伪造缩减。

| 维度 | v6 | v8a | v13 | v14 |
|---|---|---|---|---|
| 策略表示/经验 | 紧凑kernel+3全文Skills | donor核心+4全文owner合同 | empirical全局规则放入Planning，4全文合同 | 对照经验归入6局部程序卡，3Skills |
| 选择性内容 | 启动读3份 | 启动读4份 | 启动读4份，已接受运行亦如此 | core启动，单卡按当前语义读取，guard按需 |
| 决策 | Gap/季度计划/候选后Risk | donor晋升/广义成长+现代控制壳 | R规则+Review plan+Risk | fresh capsule、全部菜单一次比较、公开两步浅前瞻 |
| 风险 | public gate，普通成本软约束 | public gate及fresh控制 | 书面公开warning规则；v13行为错误排除HR | material约束优先、warning与hidden库存严格分离，同范围退出 |
| 预期认知负担 | 较小，仍全文 | 大量owner/marker/长期例外 | 较v8a小，仍要求过滤全局规则 | 小而相关工作集；降低实际负担是HYPOTHESIS |
| 未解决 | 单局高参考不证明稳定 | 72.65/59的结果分歧 | 已知recipe、cap、warning及reroute漂移 | 可能漏路由/低估警告/遗忘承诺、旧上下文驻留、反事实收益未知 |

**不是“v13换短措辞”**：全局知识成为带触发/步骤/例外/置信度的局部程序；检索由当前情景驱动；工作状态每步替换；所有legal choices才进入一次比较；生存约束先于收益并用公开浅前瞻。这些结构均在实际Skill/manifest/reference文件中，而不只写在研究建议里。

## Static evaluation / actually passed

26 个场景在 `tests/fixtures/experience_policy_scenarios.json`，四种来源：DONOR_CONTRAST / NEGATIVE_FAILURE / SYNTHETIC / AMBIGUOUS。公开语义被重写，不保存历史事件或原choice index。部分菜单有3–4项以检查不能先裁到top2；ambiguous允许多种合理选择。

| # | 场景 / 预期程序 | 检查重点 |
|---:|---|---|
|1|急性信任 / Trust+guard|先修复留任约束|
|2|健康急症 / Health+guard|必要安全恢复与交接|
|3|普通轻度负H / Project|不启动guard，接受普通成本|
|4|E不足的必要清理 / Energy+guard|不提交不可负担动作，寻找实际补救|
|5|同情景NO_GAIN立刻重复 / Energy|转向响应替代|
|6|新Level / Energy|旧Level响应不进入新capsule，重新比较|
|7|近Review短结果 vs 长资产 / Review|窗口兑现优先，非保证晋升|
|8|项目阻塞 / Project|先解除依赖，不盲扩大|
|9|可兑现ownership / Project|条件性先验，全部菜单|
|10|no-advance / Review|有实质替代路径和检查点|
|11|泛夸 / Project|不升级为交付证据|
|12|完成且认可 / Review|使用公开结果而非receipt|
|13|学习 vs 当期交付 / Project|当前义务优先|
|14|Network vs Output flat / Growth|保留广义成长|
|15|保密 / Trust+guard|合法脱敏，不泄露|
|16|掩盖推责 vs 透明修复 / Trust+guard|不增明确风险暴露|
|17|Wealth连续性 / Energy+guard|依据显式支付约束，无数字阈值|
|18|末期 / Review|下一窗口UNKNOWN，不虚构|
|19|模糊普通Story / Growth|多种可接受项，无硬危机|
|20|一维flat但其它维度有值 / Energy|保留独立价值|
|21|旧Energy序列 / Energy|当步重新比较与成本检查|
|22|高Health/夸奖但信任未解 / Trust+guard|同领域clearance|
|23|同范围正式解除 / Growth|退出guard，恢复成长|
|24|按期交付后学习 / Growth|不固定shipping|
|25|短交付有重大质量危险 / Trust+guard|生存/可靠性约束覆盖窗口先验|
|26|成本可负担的强成果 / Energy|普通成本只是末级偏好|

**书面程序逐项回放**：routing26/26、survival constraint26/26、public-only26/26、action-principle26/26；capsule及逐项即时/下一checkpoint比较记录26/26完整。它们是 Codex 手工语义审阅与可审fixture记录，**没有运行Flash、provider或选择动作的Python模拟器**。pytest只核对这些记录的完整性、route/reference一致、当前Level作用域、显式可负担性及禁止输入边界，不能独立验证模型是否会作出相同决定。

执行 `D:/CS/CareerSim/.venv/Scripts/python.exe -m pytest tests/test_candidate_packaging.py tests/test_experience_policy_contract.py -q`：**32 passed**。包括双包byte-determinism、全部10文件精确引用保留、Runner offline `validate_submission_contract`，以及非空输出保全、metadata不一致和额外本机资产拒绝。无全pytest、无无关回归。

首轮1项测试错误要求卡片栏目必须是Markdown二级标题，而计划示例为纯文本schema；修正测试接受现有schema后通过。两次只读Git报告定位使用了不存在路径/ref，修正到实际接受报告；这些是离线 tooling errors，live attempts=0。

## Acceptance / protected surfaces

| Plan验收 | 证据 / 状态 |
|---|---|
|1–3 branch-only v14、main v8a、2–3 Skills|一个分支、一个候选、三Skills；main/fallback不写|
|4–6 references、startup selective、context reduction|六卡、core-only startup正文、上述静态字符计量|
|7 contrastive distillation|24条候选经验及14条独立程序，正负与反例均保留|
|8–10 无lookup/hidden/public warning可采|runtime人工复核+卡片检查；禁止库存与公式，明确HR warning可用|
|11–13 survival/全菜单/浅前瞻|core、guard、manifest及26场景书面回放|
|14 20+ scenarios|26场景、32 targeted checks PASS，边界如上|
|15–16 frozen/no live|242个非授权tracked保护面文件byte-hash不变；provider/service/game等0|
|17 package/secret/diff|10文件skill_bundle离线validator PASS；选定变更文本secret scan PASS；diff check PASS|
|18 push/clean|交付commit最终Git回执确认remote分支HEAD一致、tree clean；不由静态测试推断|
|19 NEXT_GAME|NOT_AUTHORIZED；metadata所有validation=false|

根Runner、`pyproject.toml`、`uv.lock`、正式提交器和其它非授权tracked文件保持字节不变；冻结Runner身份 `f61c738c72e51b77298cc1c14c7c6ebf4b6c527d` 继续按Source Lock引用，没有新运行身份验证。Provider/Jiuwen配置未写；结束验证当前配置SHA `5ae22dedc828177df114e500aacf280a17217b45d3d19d9df67b583b7bd08b72`、既定`max_retries=2`，收尾计量/验证窗口hash一致。没有依赖同步、全局配置、service、install/reload、MCP、provider、DB写入、new_game/take_action/Runner play或官方提交，均0。

本机可重建派生物：`D:/CS/CareerSim/.local/scratch/s10-08/`（临时构建/计量/核验helper、context/protected/verification数据、submission）；gitignored，不是唯一取证来源，不提交。既有S10-06/S09等FORENSIC_HOLD不读取、不清理、不解除；本任务无新增raw/hold。

## Plan deviations / material state / limits

没有扩大目标或权限。按实际接口，对local packager做声明身份与reference复制的最小修补；三Skill架构替换四owner/旧marker写成branch-specific Runtime Contract例外，操作语义不变。未修改正式提交package machinery、Runner或框架。PROJECT_BRIEF不改；ARCHITECTURE_DECISIONS新增Hypothesis→静态Experiment→待Main/Stage的Decision；CURRENT_STATE仅更新本分支active候选及main fallback边界。

书面路由可能被模型忽略；局部程序的正负历史仍混杂；public-only shallow lookahead不能知晓隐藏机制；capsule维护、clearance判断、每步真正重比较、检索开销和whole-game持久执行仍需将来授权游戏审计。宿主旧tool output驻留未解决。没有 gameplay validation、75+ proof、稳定性/优越性/因果/hidden-test transfer证明，也不宣布S10 COMPLETE。

Checkpoint Signal：交付静态候选供Main/Stage review。建议下一边界仅为独立授权的有界game gate，本任务不触发。

**READY_FOR_EXPERIENCE_ROUTED_GAME_GATE**

**NEXT_GAME=NOT_AUTHORIZED**
