# S10-03｜v12 Family A 单局 Screening

> IN_FLIGHT_EVIDENCE；SCREENING_ONLY；Task = COMPLETE（保留终局后技术缺陷）。
> Decision = SCREEN_NEGATIVE_ARCHITECTURE_SIGNAL。
> RETURN_TO_MAIN_FOR_S10_SCREENING_GATE；NEXT_GAME = NOT_AUTHORIZED。

本局有可归属到唯一 fresh session 的自然淘汰结果：**23.48 / partial 16.44 / 24m / E / L1**。M6/M12/M18/M24 绩效为 C/C/D/D，未晋升。Family A 的两个 Skill 和三次正式 Review Deep Review 确实执行，但 Brief 初始化、Energy 单步决策、局部无增益更新及结果兑现存在具体执行缺口。负面信号来自这些合同偏离，而非仅来自低分；单局不能证明两 Skill 比四 Skill 更差或路线应被放弃。

自然终局事件先落盘，随后本任务编写的监视脚本未处理 `current_event=null`，触发 AttributeError 并进入 graceful cleanup。停止服务打断了 Runner 最终握手，产生 ConnectionClosedError，没有 score_report，准确 Runner exit code UNKNOWN。**这是 Codex 监视代码缺陷，不归因于 Candidate、Provider 或 frozen Runner。** 它限制终局后的运行完成与 usage 证明，但不能把已先产生的自然淘汰改称技术截停。

## 身份与交付

| 项 | 身份 |
|---|---|
| Branch / parent | `codex/s10-03-v12-screening` / `e6ddcda68ff60dad0e0676d7ff8c70ecaae556ba` |
| Pre-run tested/pushed commit | `198a707505e93f5284d841842e65fa8f9e4f339a` |
| Main / frozen v8a fallback | `9edf73de552ce91af9d9eecf2dbbe6f5def9461d`，未修改/合并 |
| Candidate | `candidate-v12-lean-career-brief` |
| Candidate JSON SHA256 | `17f425a6dae933f57822168a7fa4c948e4530a61c7f419f6260ccaf482818027` |
| Manifest SHA256 | `262c115fe3a44963969ce99d308051d87f5940778128473de09be460be8a1ddd` |
| instruction SHA256 | `4a57eb857f58b6eecff3a9a9fa5f18c9a16152de257690fa4b3329c265f0f775` |
| career-state-brief SHA256 | `5ad35ed781eba7149a3ce878bf9540de5d310a7cb824a58b313ff74e7501231f` |
| career-decision SHA256 | `a7afe9b8e1b6a68c1299b279b7f186b93bf8aebdde2079039d8d8371e241a40b` |
| Frozen Runner source identity | `f61c738c72e51b77298cc1c14c7c6ebf4b6c527d`；tracked Runner/deps 未改；pre/post byte hashes PASS |
| Fresh session | `a245eaa0ef144760b1062a709d446f8c` |

结果 commit 以本报告所在的 Git commit 为准；TASK_RESULT 回传实际 SHA。Candidate metadata 和所有 runtime/improvement/next-game flags 均按 Plan 原样保留，单局样本只记本报告。准确 protected 文件 hashes、证据 bytes/hashes 见 [compact evidence](v12-run01-family-a-screening-evidence.json)。

## P0–P6 与预算

- P0：fetch，父链、clean tree、origin/main、精确 Candidate/Skill 身份通过；独占窗口内没有其它 active CareerSim Codex Task、Python/Jiuwen 进程或既定端口监听。
- Pre-run adaptation：新增独立 `scripts/v12_screening_audit.py`，保留历史 parser 原样；CTRL/DL/BC 为 NOT_APPLICABLE；可见压缩才审核两 Skill 恢复；没有触发为 NOT_EXERCISED；numeric delta 不自动作为 stock 违规。35 项 targeted tests（8 新适配 + 27 历史）PASS，diff check PASS，提交推送后才启动。
- P1：精确三个文件的 v12 package；冻结 Runner pure layout contract PASS；调用方进程 PATH 前置根 `.venv/Scripts`，保留 inherited PATH/proxy；同环境 `which` 与一次裸 `jiuwenswarm-start --list` exit0。没有 user/system PATH 改动、uv sync 或 completion probe。
- Provider：按官方只读 `GET /user/balance` 查询一次，HTTP200、is_available=true；PROVIDER_BUDGET_GATE=UNKNOWN（当前可调用不等于充分单局资金保证），不推算钱阈值。deepseek-flash / api.deepseek.com / max_retries=2 / timeout360；未改 provider/config。金额和完整 receipt 留本地。[接口来源](https://api-docs.deepseek.com/api/get-user-balance/)
- P2：install 一次；启动 `--name career_emu all` 一次，17.19s 后四端口 readiness PASS。play 省略 `--submission`，沿用已安装包，避免第二次 install/reload。
- P3：Runner play 一次、new_game 一次、continue/replacement/manual intervention/extra reporting queries 全为零；自然 M24 淘汰，未人为 M24 censorship、未使用 Reviewer/supervisor、未查询 shared DB。
- P4：`--stop career_emu` 一次 exit0，19092/20000/20001/6173 全释放，manager pid file absent；未重启、硬杀或重跑。service wrapper exit1 仅为生命周期包装状态，不作为玩法失败原因。
- P5：explicit run paths + UTC window 一次 canonical audit 经 v12 wrapper；没有 latest lookup/DB 查询。后续仅围绕命名缺口补查：native Skill result、SESSION_ID、delta 来源、Brief/风险/NO_GAIN 语义、缺失 score-report 的 usage。
- P6：去敏报告、compact JSON、branch-local state；无需或未改 Candidate、Skills、manifest、Runner、deps、Source Lock、HPL、final submission。

| 时间（UTC） | 事件 |
|---|---|
| 13:44:15 | Task start |
| 13:57:12.537–13:57:13.071 | install start/end，exit0 |
| 13:57:13.080 | service start |
| 13:57:30.272 / .283 | readiness / Runner play |
| 13:57:40.321 | fresh session progress notice |
| 14:04:35.695 | 自然终局 observe，events L771（L772 为重复 wire record） |
| 14:04:35.716 | 监视脚本 null handling failure |
| 14:04:38.311 / 14:04:40.797 | graceful stop / cleanup verified |

PLAY→自然终局 **425.412s**；PLAY→cleanup **430.514s**。没有第二局或替补。

## 机制审计

行号指 exact raw events 的一基行号；transcript offsets 为 Unicode character offset，非 byte offset。重复 wire tool records 按 tool_call_id 去重，不把 188 次重复 take_action 写成 188 个真实动作。

| 项 | 判定与边界 |
|---|---|
| Two Skills | EXECUTED_USEFULLY：首个 action 前，event L9/L11 原生 `success=True data=... error=None` 返回对应完整 Skill content；没有旧四 Skill 依赖/加载失败。二者首次调用并行发出，完成顺序 State→Decision；调用顺序要求只能有限确认。 |
| Career Brief | EXECUTED_WITH_LIMITATIONS：M6/M12/M18 各一份五组当前版本，offset17532/32807/45344；目标与约束随 C/C/D 反馈改写。首个 fresh observe 后没有初始化版本；只写 updated/full version，未明确 supersedes；M6 思考把摘要推迟到最终输出，显示对 conversation-resident 语义摇摆。没有完整状态板/item lifecycle 回潮，但仍保留泛化旧成果。 |
| Deep Review | EXECUTED_WITH_LIMITATIONS：M6/M12/M18 围绕三问题与正式反馈执行；没有每个 Story 都启动完整 Deep Review。promotion/recovery trigger 未触发；重大 warning/result 处理没有对应完整 Brief replacement 证明。 |
| Recovery / compression | NOT_EXERCISED：本次明确窗口 compressor count0；不写 recovery PASS、不证明 Brief 持久化或压缩后可恢复。 |
| Final candidate safety | PASS_WITH_LIMITATIONS：94/94 当前合法 integer、同 session，每次 action 后 fresh observe，无拒绝/unknown receipt/盲重发；但风险清除与 stock 推测有语义局限，不能泛化为风险正确性全 PASS。 |
| Result conversion | EXECUTED_WITH_LIMITATIONS：CI 已上线/团队回归提速有同局公开描述（L155），不是凭 action receipt 虚构。M6/M12 Brief 仍持有该旧成果，提出可见成果目标，但后续反复 advertised Output 动作替代可验证的未来交付/认可；C/C/D/D 没有目标兑现。不能说机制完全没执行。 |
| Ordinary leanness | 多数 Story 较短；Energy 多次跨多个组合及重复 reconsideration，并预先承诺完整序列。94 个 action 对应 transcript71470字符/9831 whitespace words，仅是描述性测量；无任意 token threshold PASS。 |
| Local NO_GAIN / path | 同 Level/同 time 的5个 selected positive-Output advertised action 之后 fresh Output 不变（L109→115、213→219、509→515、597→603、605→611）；没有推广成 cap/hidden threshold。模型仍多次预计 Output3→4/6，未把已测局部响应可靠转为当前 path discount。 |

具体负面执行证据：

1. M3 Energy 段（offset约4998–8300）多轮组合比较；fresh 后写 “I planned … Let's proceed”。M6 先承诺 `choice1 then choice7`，第二步仍预测 Output3→4，fresh 实际仍3。M12 与 M18 同样预先组合；虽然 action→observe 顺序正确，仍未按冻结 v12 放弃剩余 recipe、逐次重选。
2. M6/M12/M18 Review objective 能改写，持续 job/performance pressure 能保留；因此不是 Skill 未安装/完全未读。然而反复收益预期未兑现没有让 path evidence 更新生效，三次 Review 的方向变化不能证明 strategic correction useful。
3. 数值 HiddenRisk action note 只有 action37（event L309）；current observe L307 的 choice4 `status_updates.HiddenRisk=-1` 直接支持该 signed delta。**ADVERTISED_CONFIGURED_DELTA，非 hidden stock/realized result 违规。** transcript 的 signed numeric mentions 均在对应 Energy/Main 配置菜单讨论，未发现数值隐藏存量、累计存量估计或私有公式。
4. 同时保留非数值推测局限：offset21630 “Earlier I avoided risky choices so HiddenRisk may be low” 无当前 stock 证据；offset34723 声称 HR warning “had cleared”，M10–M12 只见 generic positive feedback，非明确 same-scope clearance。此前 warning 是 early caution，binding severity UNKNOWN，不把它扩大成已证明 catastrophic safety violation。M21 面对公开重复积攒风险则采取保护选择，不能说全局忽略风险。

## 自动审计限制与补充事实

Pre-run synthetic fixture 与本次实际 native 返回 shape 存在差异，适配器仍有三处未覆盖；**自动零计数不是实际没执行**：

- Skill tool native result 没有 `raw_output`，自动 successful reads=[]；直接 L9/L11 的原生成功内容证明两 Skill 已读。
- legacy session regex 不认识 `SESSION_ID`，自动 transcript identity UNKNOWN；同局 transcript 的唯一完整 SESSION_ID 与 events 相同，直接核验 PASS，未用历史局替代。
- structured JSON integer delta 不匹配文本 `HiddenRisk-1` 的 regex，action37 自动 UNKNOWN；以 L307 的字段及 L309 notes 做人工来源绑定，判定 ADVERTISED_CONFIGURED_DELTA。

legacy outcome label 对 early natural terminal + exit UNKNOWN 给 UNKNOWN，但保留 `natural_terminal_observed=true`、fresh score及单 session events PASS。本报告据直接终局证据记 NATURAL_ELIMINATION；不伪造 exit0、不补造 score_report。保留自动原件，并把补充判定及证据来源分开写 compact JSON。未在 live 后继续修改审计/运行代码；这些可复现解析缺口与监视脚本问题返回 Main，需未来获准工程任务修复。

## Usage 与位置

缺失 Runner report 时 canonical usage 为 UNKNOWN。一次限定补查从本次 service stdout 的成功 `llm_usage chunk`（191条，PLAY→cleanup 窗口）量得：input15,693,221 / output38,651 / total15,731,872。它是窗口内已完成模型响应的 reported usage；最后被停止的请求没有完整回执，不称整局最终 billing总量。Provider reported costs0.0 不等于实际账单0，actual_billed_cost=UNKNOWN。continuation count=UNKNOWN（无最终 Runner telemetry），未观察到 max_continuations terminal。compression count0只对当前窗口。

23.48 属 BELOW_V8A_RUN08_REFERENCE：比 v8a RUN07 72.65 低49.17，比 RUN08 59低35.52；v6 75.29 仅历史参考。月数、场景/机会与模型方差未控制，不按token总量比较 M24与M48效率，不据此做因果收益/路线优劣判断。

## Evidence / FORENSIC_HOLD

完整 events/transcript 留在：

`D:/CS/CareerSim/.career_sim_runner/career_emu/outputs/local-s06-adaptive-controller/20261003T135733Z/`

run-scoped local receipt、stdout、native reads、public action-contexts、usage/behavior checks、audit及日志窗口：

`D:/CS/CareerSim/.local/runtime/s10-03-v12-run01/`

**FORENSIC_HOLD=ACTIVE**：raw 是自然结果/机制审计和监视失败归因的必要来源。责任 S10-03/Main；解除者 Main/Stage；复查点 S10 screening gate。只有 Main 接受独立可审结论、确认复析/复现/child依赖解除并明确授权，才可释放/清理。14个最小 retained source/derived files 的精确路径、bytes、SHA256 见 compact evidence；run-window llm copy可恢复本次压缩证据，不以累计日志 hash替代源。既有 holds 保持原样；无 raw/DB/.env/provider config 入库。

## TASK_RESULT / Review

FACT：一次 install/service/play/new_game；自然 M24淘汰；首动作前两 Skill成功加载；三次 Review Brief/Deep Review；94个成功 action；清理 PASS；终局后监视/握手缺陷；所有冻结 tracked身份与 validation flags原样。

INFERENCE：结果兑现/局部响应未发挥纠偏作用，Energy recipe/重复比较与 Brief初始化缺失构成 Family A 本次执行负面信号。无控制对照，不证明它造成了全部低分，也不证明架构本身应被否决。

RECOMMENDATION：Main 先判断执行缺口是否需要后续静态修正，并处理 monitor/native-envelope/delta/SESSION_ID审计问题，再决定是否另授予验证预算。本任务不自行创建v12a/Team、替换fallback、merge main、宣布Stage完成或开展下一局。

Validation：35 targeted regressions PASS；source/package frozen rehash PASS；94合法/同局 action→observe pairs PASS；selected canonical secret scan与git diff check PASS。准确最终 commit/remote/clean tree及总耗时在交付回执记录。

Task metrics：13:44:15→14:19:41 UTC 的最终验证耗时35m26s；35 targeted tests耗时1.20s。Critical monitor failure1；offline AST原生返回尾缀解析 Tooling Error1（无side effect，修正后仅补查该命名缺口）；自动 audit shape gaps3。早期文件/Windows glob定位命令有若干无副作用 miss，未另维护准确总计。Scope deviation仅终局后握手被监视异常打断；新增game/provider completion/replacement预算均0。未提交raw。
