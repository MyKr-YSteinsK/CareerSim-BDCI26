# 05｜tests 为什么这么多，以及它们证明什么

[学习地图](00-学习地图.md) · [上一章](04-scripts为什么这么多以及分别做什么.md) · [下一章：experiments](06-experiments与research是怎样工作的.md)

## Test不是“运行一下看会不会报错”

先读 [C04 的工具分类](04-scripts为什么这么多以及分别做什么.md)。本章负责测试类别、真实断言和证明范围；函数位置查 C03，分层实验结论查 [D04](../track-d-project-method/04-Static、Runtime、Gameplay与Adherence多层验证.md)。

Test（测试）向一个对象提供受控输入，并断言输出或行为满足要求。Assert（断言）把“应该怎样”变成可自动检查的条件。Fixture（测试夹具）提供临时文件、模拟事件或替身客户端。测试有价值，是因为它能反复保护某个具体边界；测试的数量本身不是系统能力的分数。

本项目有游戏运行、文本合同、包装、日志解析、研究工具等不同对象，每个对象都有不同failure mode（失败方式）。如果只有一次端到端游戏，错误可能表现成“没得高分”，却无法分清是包错、会话错、解析错还是模型选择不佳。多个小测试能在更靠近原因的位置发现问题。

**FACT｜事实：**S11-28列出21个tracked `tests/`文件；本章全部表示。S11-29只阅读和讲解，没有运行pytest，没有新增tests。比赛要求、项目开发测试与正式提交内容是不同范围；不是21个测试都要装入比赛ZIP。

## 五种类别可以交叉

| 类型 | 关注什么 | 本项目例子 | 证明边界 |
|---|---|---|---|
| Unit Test（单元测试） | 一个小函数的明确输入/输出 | public projection、choice helper | 不覆盖真实传输和完整游戏 |
| Contract Test（合同测试） | 字段、身份、调用或权限约定 | manifest、Skills、live gate | 文字存在不证明模型遵循 |
| Regression Test（回归测试） | 已发现错误不再出现 | 累计日志窗口、无盲重试、旧身份污染 | 不等于所有未来错误都排除 |
| Evidence/Parser Test（证据/解析测试） | 提取、归属、未知和来源处理 | post_run_audit、forensics | fixture正确不认证所有真实raw |
| Packaging Validation（打包验证） | 输出文件集合、原字节与冻结身份 | Candidate/final builder | 不等于平台上传与评测通过 |

一个测试文件可以属于两三类。例如日志窗口测试既是parser测试，也是历史累计计数错误的回归保护。分类的目的是看懂断言，而不是强行让每个文件只进一个格子。

## 一、真实单元例子：公开投影把什么留下

[test_public_mechanical_probe.py](../../../tests/test_public_mechanical_probe.py) 构造 `observe_payload`，给公开字段和故意夹入的未知字段。它调用 `project_public_snapshot`，断言公开output与choice留下，未知字段名称出现在ignored_fields，未知值不成为策略状态。

```text
测试输入：公开output + 人为插入的非公开字段
        ↓ project_public_snapshot
断言：公开字段保留；未知字段不进入status；必要名称可记录
```

这是程序员构造的离线输入，不是读取真实隐藏游戏状态。它证明投影器对这组输入按规则过滤；若失败，首先意味着投影合同或测试期待发生变化。它不证明官方MCP在所有版本都只返回公开字段，也不证明选择函数在真实游戏里得高分。

同文件中的 `test_min_id_control_returns_integer_one` 传入choice集合3、1、2，断言MinIdControl选1且为整数。这是**FACT｜事实**：测试检查机械规则。不能把“最小ID规则可计算”讲成“第一个选项普遍最好”。策略收益需要另一路实验。

## 二、合同例子：文本与身份为何也要测试

[donor transplant测试](../../../tests/test_s09_10_donor_core_transplant.py) 检查donor排名/模式/审查段落是否原样保留、execution shell是否保留、没有导入旧分支、五个written scenarios（书面场景）条款以及不存在历史答案查询。源码明确没有Provider或模拟模型行为oracle（判断依据）。

这类测试保护“批准只改某处”的边界。如果范围意外扩大，断言可以及时发现。它也能核对validation标记是否重置，避免沿用旧版本已验证的旗标。

但检查Skill正文含有某条规则，与实际模型在一局中理解并应用该规则，是两件事。测试失败可以指向文本漂移；测试通过只能证明受测文本/身份匹配这些断言。真正adherence（遵循）要看加载、读取、动作与回执的session证据。

**FACT｜事实：**本次直接读取 `test_candidate_v7_contract.py` 时，其常量仍写历史v7y身份；当前权威状态却是v8a工程候选、最终exact-v6。这校正了source pack把它笼统称为“当前Candidate测试”的描述。本教程将它作为历史身份/继承合同实例，不宣称今天全套测试已通过，也不在文档任务里修复历史断言。

文件名、docstring或变量叫CURRENT不提供永恒更新保证。遇到旧测试，先判断它绑定哪个版本，再决定未来维护/迁移；不要为了得到绿色结果直接删除断言，也不要把失败自动认定成当前runtime坏了。

## 三、回归与证据例子：23条累计记录如何只算本局2条

[test_post_run_audit.py](../../../tests/test_post_run_audit.py) 的fixture写入两类LLM日志：较早日期23条，以及当前run窗口2条。给定 `+08:00` 日志offset后，`test_fresh_score_and_cumulative_log_scoping`断言本局compression count为2。另一个测试不给可用时区，断言count=UNKNOWN且有limitations。

这把历史累计日志污染问题转为可重复的合成回归案例。不是在本任务重新打开raw，也不是重新证明历史那一局全部动作。

该fixture还故意让score report的session字段为空，而events有一致fresh session和终局observe。测试要求摘要使用fresh_final_observe分数，同时把空session字段缺陷留下。它也分别断言动作attempt/success/error、CTRL格式和证据类别，不把格式标记自动当语义成功。

为什么要留“未知”测试？因为程序容易把缺失转成零、把空字段转成默认latest，从而给人一种精确但错误的结果。能够稳定输出UNKNOWN，是证据工具的重要能力，而不是实现不完整的掩饰。

## 四、包装例子：重复构建相同不等于比赛接受

[test_candidate_packaging.py](../../../tests/test_candidate_packaging.py) 在两个临时目录运行当前packager，检查相对文件集合只有manifest和四Skills、两次bytes相同、manifest名字匹配metadata、输出符合Runner skill_bundle结构。

**FACT｜事实：**测试证明给定当前来源的复制确定性和结构合同；不证明exact-v6 finalZIP、不证明安装加载、不证明upload。它确实启动本地packaging子进程并写临时输出，因此“offline（离线）”也不是“完全不写文件”。

[test_final_solution_builder.py](../../../tests/test_final_solution_builder.py) 则围绕最终builder的身份、拒绝和包合同，使用合成临时仓库。它能防止不合范围或被敏感内容污染的输入进入结果，却不能代替真实官方portal（上传平台）回执。

如果删掉这些tests，未来有人改包装脚本时可能把多余文件、错误版本或换行后的字节带入包。保留价值在于保护具体交付合同；要退役测试，应先退役或迁移其保护的构建路径。

## 五、替身传输：保护重试纪律，不制造真实对局

[test_run_public_mechanical_batch.py](../../../tests/test_run_public_mechanical_batch.py) 定义FakePublicClient，记录调用次序并返回构造的new_game、observe、take_action结果。还能模拟拒绝、恢复读取失败和传输异常。测试因此可以检查预算、菜单合法性及不盲重试的逻辑，而不启动真实服务。

Fake（替身）让错误可以稳定复现，尤其适合未知动作结果：如果上一次take_action回执丢失，程序不能假定未执行并重发。替身能检验程序在指定异常下怎样停止或核对，但不能证明真实服务在所有断连条件下提供相同保证。

类似地，[Skill evaluator测试](../../../tests/test_skill_behavior_eval.py) 使用mock Provider保护请求门、失败状态及重试上限。mock返回一个固定JSON，不等于真实模型在长上下文和压缩后会做相同选择。

## 六、21/21功能索引

下表“未证明”用于限制推论；依赖指受保护对象，不表示它必然在当前全部测试中通过。

| Test | 类别、主要目标与断言 | 当前依赖/保留价值 | 没有证明什么 |
|---|---|---|---|
| `test_archive_run_evidence.py` | 合同/回归：选定文件、窗口切片、路径/Session/secret拒绝、限定stage | archive工具、临时repo；保护归档边界 | 任意raw安全、hold解除 |
| `test_candidate_packaging.py` | 包装：四Skill文件集合、原字节、两次一致、Runner结构 | packager/configs/skills | finalZIP、安装、上传 |
| `test_candidate_v7_contract.py` | 历史合同：身份/hash/继承文本/validation边界 | 历史v7y期待及当前路径；需版本语境 | 当前全套通过、模型遵循 |
| `test_candidate_v7s_contract.py` | 治理合同：跨文档引用、当前候选与final区分、白名单 | 项目合同/config/Skill/builder | live接受或性能 |
| `test_codex_public_agent_driver.py` | 单元/合同：fake transport、合法choice、核对/停止 | public driver、替身 | 真MCP、真实结果 |
| `test_final_solution_builder.py` | 包装/回归：synthetic repo身份、拒绝、ZIP合同 | final builder、临时repo | portal接受、上传 |
| `test_policy_transition_dataset.py` | 单元/合同：离线转换、泄漏/partial/unknown处理 | dataset builder、synthetic data | 策略质量、因果效应 |
| `test_post_run_audit.py` | evidence/回归：fresh身份、窗口、缺失、marker限制 | audit、合成events/log | 所有真实来源正确、语义遵循 |
| `test_public_mechanical_probe.py` | 单元：公开投影、机械policy、合法选择 | probe模块 | 模拟器真实性、分数收益 |
| `test_run_public_mechanical_batch.py` | 合同/回归：fake MCP预算、拒绝/恢复/停止 | batch+fake clients | 真服务/DB隔离 |
| `test_s08_09_runtime_contract_forensics.py` | evidence：固定提取器fixture和边缘处理 | S08-09脚本 | 全部raw正确、完整adherence |
| `test_s08_10_runtime_adherence_protocol.py` | 文本合同/回归：控制state、Energy、冻结表面 | 历史协议及身份 | 模型实际执行协议 |
| `test_s08_10r_v7v_preflight_ordering.py` | 合同/回归：READY/preflight无环、single-use | 历史执行壳/文本 | live preflight正确 |
| `test_s08_11_high_score_core_forensics.py` | evidence：Session绑定与提取边缘 | S08-11脚本/fixture | 高分因果解释 |
| `test_s09_02_failure_floor_joint_forensics.py` | evidence：ambiguity、unknown、quantile/归属 | S09-02脚本/合成cohort | 群体因果或完整真实样本有效 |
| `test_s09_03_nonsticky_stabilization.py` | 合同/回归：fresh重授权、禁止历史阈值升级 | 历史策略文本/identity | 实际稳定化及分数收益 |
| `test_s09_04_resource_trajectory_forensics.py` | evidence：exact窗口/public/hash/rejection | S09-04提取器 | 输入之外的来源一致性 |
| `test_s09_05_story_exposure_guard.py` | 合同/回归：局部Story guard、小范围、冻结表面 | 历史planning/manifest | LLM路线遵循与收益 |
| `test_s09_08_world_model_correction.py` | 合同/回归：来源边界、局部增量、scenario条款 | 历史Skill/config | gameplay改善、隐藏公式 |
| `test_s09_10_donor_core_transplant.py` | 合同/回归：donor字节、shell、五个written scenario | donor/current来源 | runtime迁移收益 |
| `test_skill_behavior_eval.py` | 合同/回归：mock Provider、secrecy、stage/retry | eval工具/替身 | 真实模型质量 |

所有文件可以从[tests目录](../../../tests/)定位。研究目录的 `scripts/research/s10_22/test_boundary.py` 另计在17个scripts中，不混入21的分母。

## “4 passed”到底够不够

**TEACHING EXAMPLE｜教学示例：**四个测试检查JSON能读、Skill标题存在、输出包相同、fake client遇断连会停止。四个通过可以支持这四项受控检查；它不包含真实模型、实际工具注册、当前游戏Session或长局压缩，所以不能推出Agent gameplay一定正确。

反过来，不必为修一个Markdown链接运行整个游戏。验证应匹配失败方式。文档任务用链接、fragment（锚点）、格式与diff；包装改动用相应身份与内容检查；真实运行才有授权内的runtime证据。盲目扩大测试范围可能浪费成本甚至引入副作用。

## 保留与维护：测试不是永远有效的证书

保留测试看它保护的当前接口、历史修复或复验结论。版本退出后，可重新定位历史语境、迁移合同或进入退役审查；教学不修改期待。文本中有健康恢复条款，仍不证明真实模型应用了它。

## 深入练习：怎样从一个断言推回证明对象

**TEACHING EXAMPLE｜教学示例**：合法整数、规则文本、fake client 停止逻辑对应三种受测对象；前五类真实例子已给出具体 assert。完整验证链见 [D04](../track-d-project-method/04-Static、Runtime、Gameplay与Adherence多层验证.md)，不要把这三类 PASS 累加成收益证明。

### 测试失败不一定等于被保护功能坏了

先找到受测版本和失败断言，再区分实现回归、过时期待、fixture 或启动错误。历史身份测试不能当当前 runtime 的自动诊断；当前 packager 若丢 Skill，集合断言失败却直接影响它保护的交付合同。不能以“旧测试”忽略真实回归，也不能为变绿随意删断言。

### 什么是“测试验证了规则，没验证收益”

公开字段过滤、机械 choice 和重复包装可由受控测试核验；分数收益还需要实际运行身份、轨迹和样本设计。准确陈述 assert 的对象，比累计 PASS 数量更有用。

### 一个阅读小测试的五步顺序

按 import → fixture → 调用参数/输出 → assert → 异常/清理路径阅读。测试临时目录与 held runtime 是不同对象，不能照搬清理动作。

本章只阅读源码，没有运行 pytest；保留 21/21 索引不等于宣称它们当前全部通过。接着读实验输入与结果怎样保存，或回到索引查一份测试的具体保护对象。
