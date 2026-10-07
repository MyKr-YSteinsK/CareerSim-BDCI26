# 04｜scripts 为什么这么多，以及分别做什么

[学习地图](00-学习地图.md) · [上一章](03-career_sim_runner源码目录导航.md) · [下一章：tests](05-tests为什么这么多以及它们证明什么.md)

## 同样是 Python，工作对象却不同

本章是脚本用途与输入/输出的详细入口。先读 [C01 总图](01-整个CareerSim仓库一眼看懂.md) 与 [C02 工程文件](02-根目录与核心工程文件.md)，需要定位函数时再查 C03；实验结论交给 Track D。

Script（脚本）通常围绕一个工程问题编排输入和输出。Runner是正式运行系统的一部分；脚本可能在运行前构建包、运行后提取证据，也可能本身就是另一条玩家路线。判断标准是调用关系和副作用，不是扩展名。

**FACT｜事实：**S11-28映射了当前17个tracked scripts。下面按包装、证据、公开接口、历史取证和研究组织，最后给完整索引。没有在S11-29执行它们。当前权限为文档写入，Live（实际运行操作）预算为零。

如果没有这些工具，工程人员得手动复制文件、按日志逐行计算、反复检查Session和时间窗；容易把重复劳动变成不一致的结果。脚本将规则明确写入代码。但自动化只会稳定地执行它实现的规则，不能使错误输入自动成为正确事实，也不能替Main批准实验和清理。

## 一、包装工具：复制内容与冻结身份是两个问题

[package_candidate.py](../../../scripts/package_candidate.py) 的 `build_submission` 读取当前 `configs/current_candidate.json` 与runtime manifest，检查Candidate名字、agent模式、非空Instruction和四Skills集合，再复制原字节到新目录。输入是当前工程候选，输出是Runner兼容的manifest+Skills包；它拒绝覆盖非空输出目录。

[build_final_solution.py](../../../scripts/build_final_solution.py) 则处理最终 `solution.zip`：检查干净同步main、冻结身份、白名单内容、敏感值、ZIP构建与安全解包核验；exact-v6模式从明确冻结的历史Git对象取运行来源，再结合提交文稿。

**TEACHING EXAMPLE｜教学示例：**当前四Skill来源可以成功包装，但最终冻结要三Skill历史v6。若把“package_candidate成功”当“最终ZIP身份正确”，就跳过了最重要的输入选择。包装的正确性分为：选对来源、复制/构建正确、内容/身份符合合同；最终平台上传与评测另有证据。教学示例；当前S11-29不授权执行。

**FACT｜事实：**最终冻结包已在权威资料中记录，但官方上传没有执行。构建器可长期保留用于授权的再构建；包存在、ZIPhash通过和平台接受不能混为一谈。来源见[最终提交合同](../../project/FINAL_SUBMISSION_CONTRACT.md)及[当前状态](../../project/CURRENT_STATE.md)。

## 二、证据工具：整理与归档不等于判案

[post_run_audit.py](../../../scripts/post_run_audit.py) 接收显式events、transcript、score report、runner result等路径，必要时接收LLM日志和带时区的Run Window（运行时间窗）。它不寻找latest run，不查询DB，不启动Provider。输出确定性的 `post_run_summary.json`，带来源bytes/hash、身份、结果、动作、usage及限制。

这解决的是“从指定来源提取哪些可重复核验的事实”。例如累计LLM日志有多局压缩事件，只应计入本局窗口；窗口无法建立时输出UNKNOWN，不能填0。marker（标记）出现次数也只证明文本模式出现，不证明模型理解或执行了所有规则。

[archive_run_evidence.py](../../../scripts/archive_run_evidence.py) 解决另一问题：哪些材料可以进入private repo。它要求明确source dir、run ID、逐个选定文件、诊断日志时间窗；检查路径、Session、编码、大小和明显敏感值，生成manifest，可选择仅stage指定安全输出。它会复制、写入、移动选定归档和可能暂存，因此是有文件副作用的工具。

两者的关系不是“审计完成就全部归档”。摘要供审阅，归档供来源保存；是否仍有唯一raw、是否受hold、是否可释放都由独立合同和Main决定。archive工具的扫描是有限规则，不是“任何日志都绝对安全”的证明。流程来源见[LIVE_RUN_WORKFLOW](../../project/LIVE_RUN_WORKFLOW.md)。

没有audit，重复人工计数容易变；没有archive边界，证据分享容易带入其他session和凭据。两者当前价值明确，但每次使用仍须准确输入和权限。

## 三、公开接口工具：里面有真正会采取动作的玩家

[public_mechanical_probe.py](../../../scripts/public_mechanical_probe.py) 定义公开状态投影、合法选择与机械策略助手。单独的逻辑模块不启动服务或游戏；它能被测试、batch或其他工具导入。

[run_public_mechanical_batch.py](../../../scripts/run_public_mechanical_batch.py) 使用这些助手组织有界public MCP batch，需要显式live门。它会初始化传输、创建/观察session、采取动作并保存输出。`--live`是代码门，不是Main授权的替代品。

[codex_public_agent_driver.py](../../../scripts/codex_public_agent_driver.py) 是另一条直接public MCP stdio驱动路线，处理人工/工程侧choice与rationale、合法菜单、Session、回执及停止。它不是HPL直接引擎路线，也不等于正式JiuwenSwarm Runner。名字包含agent不保证它测量了正式Candidate的Skill加载和遵循。

```text
纯投影/机械选择助手 → fake client测试：不需要真实游戏
                 → public MCP batch：真实动作，需要独立授权
人工CLI/UI选择 → HPL adapter → GameEngine：另一路径
正式模型选择 → JiuwenSwarm/MCP → GameEngine：正式运行路径
```

同一模拟器可以被不同控制路径调用。性能和遵循结论只能绑定实际使用的路径，不能看见take_action就当成完整正式runtime验证。详见[HPL章](10-Human-Play-Lab是怎么实现的.md)和[Track B 工具调用章](../track-b-system-runtime/07-从模型决定到Tool调用再到新状态.md)。

这些脚本目前有历史复现和理解接口的价值。若未来只保留最终正式路线，它们可以进入退役审查；但尚有tests、结果或教学引用时，不能把“不是最终路线”直接翻译成“现在可删”。

## 四、四个取证脚本：为什么一次性工作当时重要

[S08-09提取器](../../../scripts/s08_09_runtime_contract_forensics.py) 针对准确S08-RUN03归档，查看控制/Delivery及相关时间线。它的价值来自固定来源和问题，不是通用地替所有Run作遵循判定。

[S08-11提取器](../../../scripts/s08_11_high_score_core_forensics.py) 从四个明确Run公开动作中提取action mix（动作构成），使用Session及公开状态边界；它有意忽略notes、transcript、描述、分数和隐藏内容。所谓“高分核心”是调查问题，不意味着程序识别出了高分因果公式。

[S09-02分析器](../../../scripts/s09_02_failure_floor_joint_forensics.py) 整理固定公开cohort（样本组），把跨month/Level/review、批量动作和归属未知的变化排除出干净动作统计。源码明确clean表示可归属到流，不等于随机事件的因果隔离。

[S09-04资源提取器](../../../scripts/s09_04_resource_trajectory_forensics.py) 验证准确源bytes/hash和窗口，复用S09-02归属逻辑，输出公开资源时间线及菜单。合理性、脆弱性和干预解释仍需人审。

**INTERPRETATION｜解释：**一次性取证脚本把“当时怎么算的”留下来；它对修复错误归属、复核表格和说明未知很有价值。一旦结果知识被canonical文档吸收，输入可恢复且下游/hold依赖关闭，它可能退出当前树。一次性描述的是用途集中，不是价值低；长期保留也不是默认永久承诺。

若只保留结果不保留提取方法，某些结论可能难以重新算出。若所有一次性脚本永久挤在主工具入口，未来维护者又难分清谁还在用。正确处置要同时看复验需求和知识迁移，见[保留章](12-哪些文件值得长期保留以及哪些最终可以删除.md)。

## 五、研究工具：数据准备、模型评估和引擎评估各有边界

[build_policy_transition_dataset.py](../../../scripts/build_policy_transition_dataset.py) 从显式来源构造离线公开transition（状态转换）数据，JSONL是其基础输出。源码说明text labels是研究proxy（代理标注），不是game state或因果证据；还保留advertised HiddenRisk delta的研究字段。不能因此把本工具概括成所有内部信息完全不存在，更不能把该研究字段拿来当正式策略事实或隐藏规则知识。S10-22的严格投影又会剔除整个status_updates，两种研究协议不同。

[skill_behavior_eval.py](../../../scripts/skill_behavior_eval.py) 对隔离Skill副本作有界公开场景行为评估。离线计划与Provider阶段分开；`--run-provider`可直接发HTTPS模型请求，具有真实成本与输出。mock（替身）测试验证请求门、状态、失败计数、去敏和重试边界，不证明真实模型语义质量。

`scripts/research/s10_22/`中的四份脚本组成研究小系统：harness接官方Dev引擎；policy只接公开投影并输出整数choice；search编排variant与seed；test_boundary核对firewall（信息边界）、子进程与复现。它们不是正式Candidate安装，也不是提交包的一部分。

特别要纠正一个导航材料的简写：`test_boundary.py`的普通测试组主要是投影、策略和子进程检查，但文件的 `__main__` 在测试通过后还调用 `reproducibility()`，创建引擎并运行三个episode（对局过程）。所以直接执行它不能被描述为纯静态单元检查；S11-29没有执行。

历史S10-22实际只评估baseline，未完成宏搜索；文件名search不能作为“已经搜过全部策略”的证据。[下一章实验](06-experiments与research是怎样工作的.md)讲结果边界。

## 六、17/17完整索引

表中“后续去向”均是 **INTERPRETATION｜解释**，表示审查方向，不是删除批准。输出路径由调用参数决定，不应假定可以覆盖旧来源。

| Script | Purpose / Inputs → Outputs | Side Effects | Historical Use / Current Value / Likely Disposition |
|---|---|---|---|
| `archive_run_evidence.py` | 选定文件+Run窗口 → 扫描归档与manifest | 复制/写入/移动归档；可stage | WF-01证据管线；CURRENT_CORE_TOOL；保留核心 |
| `build_final_solution.py` | 冻结来源+文稿 → ZIP与身份核验 | 写包及核验临时输出；不game/provider/DB | S10最终冻结；PACKAGING_TOOL；保留再构建能力 |
| `build_policy_transition_dataset.py` | 显式研究来源 → transition JSONL/摘要 | 离线读写 | S10数据准备；RESEARCH_ONE_OFF；复现依赖闭合后审查 |
| `codex_public_agent_driver.py` | choice/rationale+MCP状态 → 轨迹/回执 | 可启动传输/游戏动作 | 历史public driver；REPRODUCIBILITY_TOOL；条件保留 |
| `package_candidate.py` | 当前manifest+四Skills → 本地提交目录 | 写新bundle | 当前候选包装；PACKAGING_TOOL；保留，区别最终构建 |
| `post_run_audit.py` | 明确events/transcript等 → post_run_summary | 写摘要；不DB/provider/service | WF-01离线审计；CURRENT_CORE_TOOL；保留核心 |
| `public_mechanical_probe.py` | public snapshot+local policy → projection/decision | 逻辑模块本身不启动game | S07公开probe；RESEARCH_ONE_OFF；随导入者/复现需求保留 |
| `research/s10_22/harness.py` | seed+policy → trial/trajectory | 引擎、子进程、文件输出 | S10-22可行性；RESEARCH_ONE_OFF；复现/hold闭合前保留 |
| `research/s10_22/policy.py` | 严格公开JSON → 合法宏choice | 策略子进程I/O；独立策略不创建game | S10-22baseline；RESEARCH_ONE_OFF；与协议配套 |
| `research/s10_22/search.py` | variants+seeds+gate → batch结果 | 可启动harness/game并写文件 | 宏筛选未运行；RESEARCH_ONE_OFF；保留未执行边界 |
| `research/s10_22/test_boundary.py` | fixtures+policy/harness →断言/复现记录 | tests有子进程；直接入口另有game复现 | S10-22边界；RESEARCH_ONE_OFF；不得当纯无副作用入口 |
| `run_public_mechanical_batch.py` | live门+限制+public MCP → 结果证据 | MCP/new_game/take_action与文件输出 | S07batch；REPRODUCIBILITY_TOOL；只在明确授权下复现 |
| `s08_09_runtime_contract_forensics.py` | 准确S08-RUN03归档 → 调查JSON | 离线派生写入 | S08-09遵循问题；FORENSIC_ONE_OFF；知识迁移后审查 |
| `s08_11_high_score_core_forensics.py` | 四个显式Run/Session公开事件 → action mix | 离线派生写入 | S08-11高分调查；FORENSIC_ONE_OFF；保留解释/复验依赖 |
| `s09_02_failure_floor_joint_forensics.py` | 固定公开cohort/Git源 → metrics | 离线读取及写入；可读Git对象 | S09-02failure floor；FORENSIC_ONE_OFF；条件退役 |
| `s09_04_resource_trajectory_forensics.py` | 准确源hash/窗口 → public timelines | 离线派生写入 | S09-04资源调查；FORENSIC_ONE_OFF；条件退役 |
| `skill_behavior_eval.py` | Skill版本+场景+阶段 → eval结果 | 写状态；opt-in Provider请求 | S07-50R评估；RESEARCH_ONE_OFF；保留协议与复现边界 |

## 读一个脚本时怎么避免踩错边界

先看入口与参数，再核输入是否显式/回退 latest、输出是否覆盖、子进程/网络/引擎副作用以及调用者/tests。“报告”“本地”“test”这些名字不提供权限，三类边界——文件副作用、运行副作用、结论范围——分别判断。索引中的处置方向不授予删除。

## 深入练习：同一个输出名字，为什么输入合同决定结论

**TEACHING EXAMPLE｜教学示例**：同名 `result.json` 来自 audit、fake Provider 或 public MCP batch，分别是派生、替身、真实动作路径材料。再核输入配对：Run A events 与 Run B transcript 都能解析，仍可能错局；latest 也可能选中旧 Task。完整归属方法见 [D08](../track-d-project-method/08-Forensics为什么成为项目的重要部分.md)。

### 三个互不替代的核验问题

| 问题 | 需要看到什么 | 一个常见不充分替代 |
|---|---|---|
| 包是否选对来源 | 冻结commit、manifest与Skills身份 | “复制没报错” |
| 调查是否算对 | 明确输入、parser规则、未知处理、对应测试 | “JSON存在” |
| 真实路径是否按规则执行 | 加载/读取身份、Session动作与回执、语义review | “static tests passed” |

这里没有要求每次都追加所有验证，而是说明所声称的结论要匹配对应证据。只修打包复制错误，验证复制合同就可以；若要主张正式Agent收益，包装测试当然不够。

### 输出文件为什么不能覆盖来源

派生报告应写到独立输出；写回原 events 会破坏复验基础。遇到非空目录拒绝，先确认是否获准重建，不能强制覆盖。来源与 hold 的生命周期见 [C07](07-artifacts、Raw-Evidence与证据链.md)。

用一句话自查：谁生成、吃了什么、改变了什么、证明了什么？完整索引供查询，下一章用真实断言解释测试怎样保护这些工具。
