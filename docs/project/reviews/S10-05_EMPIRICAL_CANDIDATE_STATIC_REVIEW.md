# S10-05｜Empirical Candidate 静态比较

Status：`STATIC_IMPLEMENTED_NOT_RUNTIME_VALIDATED` / `IN_FLIGHT_EVIDENCE`。
Decision：`READY_FOR_EMPIRICAL_CANDIDATE_GAME_GATE`；`NEXT_GAME=NOT_AUTHORIZED`。

- Branch：`codex/s10-05-empirical-promotion-policy`；base 最新 origin/main `8267d420da29888d0a05403991f8980e251aaa0c`，与任务指定基线一致。
- Candidate：`candidate-v13-empirical-promotion-playbook`，parent/fallback：`candidate-v8a-v7o-donor-core-transplant`，fallback 精确来源为 base。main fallback 未变；不合并实验分支。
- 本任务是一个 Planning strategy delta；Single Agent / 四 Skill ownership、Runner、依赖、provider/retry config、CONTROL_STATE/preflight、startup/loop/whole-game persistence/context recovery 均冻结。

## 策略脑是否更短、更直接

| 项目 | v8a | v13 |
| --- | --- | --- |
| Planning Unicode chars | 8748 | 4814 |
| Planning lines | 128 | 73 |
| Manifest instruction chars | 4373 | 4549 |
| Total four Skill chars | 18493 | 14559 |

char/line 以 UTF-8 解码、换行归一化后的 Unicode 文本统计，不是 token 数。Planning 缩短约45%；manifest 只把策略 kernel 同步为高显著性短摘要（增加176chars），其前后 execution shell 字符串逐字相同。总 Skill 文本减少，未测 token/runtime/score 收益。

删除/合并：重复的长篇 MODE 解释、两套排名段落、pre-first-review-only 兑现 prior 的多层触发/退出说明、公共hint禁令列表、重复季度编排及恢复解释。并未删除保护、响应折价、ownership、near-checkpoint或recovery语义；将其压缩进九条规则及一个接口段。Manifest 的控制执行、Energy 单步重排与 recovery 部分完全保留。

新增/更显著：R1 fresh事实，R2窗口成果→ownership→广义成长→option value，R3窗口内交付与质量例外，R4结果阶梯，R5局部响应折价/条件变化重评，R6 Energy单步，R7 conditional Main，R8重大危险覆盖/普通成本例外，R9 no-advance重排。S10-04的普通成本与早期追赶规则分别合入R7/R8及R9；不加入复利因果或追平保证。没有复制历史run IDs、分数、样本数量、Review阈值表、event-title答案或成功百分比。

接口保留：`REVIEW_PLAN = <Objective | Primary Gap | Next Observable Checkpoint>`；`MODE = A | S`；`RECOVERY=NONE|PROGRESSION|RESOURCE|RISK|DELIVERY|UNKNOWN`；现有 `PLAN:` / `CANDIDATE: choice=<one legal integer>`。ONE FRESH OBSERVE=ONE PLANNING PASS，最多两个competitive candidates及既定一次Risk reconsider branch不变；不新增marker/schema。

## Evidence admission 的 delegated decision

`EVIDENCE_DELTA_DEFERRED_TO_KEEP_POLICY_EXPERIMENT_CLEAN`。
现有 Board/Risk 明确拒绝HiddenRisk与public-status-unclear数值，且三个Skill要求exact bytes。开放advertised HiddenRisk delta会改变跨owner证据语义，成为第二个变量；本任务不采用。公开hint仍为软证据，Manifest原GLOBAL EVIDENCE FIREWALL完整保留。后续如要纠正此边界，须单独决定，不能宣称v13已开放direct status_updates或风险stock。

## Byte preservation

以下SHA-256是本机原v8a working bytes（含既定CRLF）与完成后bytes；hash-object同时核验Git canonical blob匹配parent。

| Skill | before SHA-256 | after SHA-256 |
| --- | --- | --- |
| structured-state-board | da76071dd035fcbb9073d69173db9a629f2404189709d39ea950dfd78bcd1cae | da76071dd035fcbb9073d69173db9a629f2404189709d39ea950dfd78bcd1cae |
| delivery-progress | 200b6c83aaca43f6dccfe58a30e23e79463e930512ef89cf5b19070a9d5d7528 | 200b6c83aaca43f6dccfe58a30e23e79463e930512ef89cf5b19070a9d5d7528 |
| risk-review | 6da910fa60b07dfdccfc78a840ebc4777fc39e3188358e69ee483c89606874fd | 6da910fa60b07dfdccfc78a840ebc4777fc39e3188358e69ee483c89606874fd |

Runner/dependencies/provider/retry：交付diff白名单只允许Planning、两份Candidate/manifest JSON、current-candidate tests、当前状态及本review；冻结目录/文件及全部历史研究/run evidence diff为空。没有修改packager，原结构仍为manifest+四个SKILL.md。

## A–H written static scenarios

这是自然语言合同审查与test覆盖，**不是模型执行/行为验证**。输入均为合成公开条件，不复制历史事件答案。

| Case | 公开条件 | 合同要求及例外 | Static |
| --- | --- | --- | --- |
| A M6 deliverability | 无重大危险；短方案可窗口内完成，长期方案在窗口外 | R2/R3优先短方案；短方案重大质量/安全代价或长方案可及时完成则重新比较 | PASS |
| B NO_GAIN | 同Level/可比context，clean目标平，另一路有响应 | R5折价目标family、比较alternative；保留独立价值，Level/context改变或cleanGAIN重开，不全局封禁 | PASS |
| C Energy | 本季度还有资源，旧计划排了多个动作 | R6只输出一个合法choice；每步fresh观察、丢弃旧remaining intent再排序，不授权序列 | PASS |
| D key project | 上一项目blocked/stale且已有更强可兑现路径 | R3/R7允许转向当前合法更强方案，项目非default，替代无固定顺序 | PASS |
| E ordinary cost | 仅轻微Health/workload代价，强成果机会 | R7接受合理普通成本、R8不自动S；不虚构数字阈值 | PASS |
| F material danger | 急性症状或显式trust/job/compliance升级，即使H高 | R8 S与最小必要保护；约束解除/场景结束才回A，绩效修复可解除job threat | PASS |
| G result hierarchy | 泛泛夸奖/汇报标签/receipt，没有完成回执 | R1/R4不称verified deliverable；消费Delivery公开完成+认可，非隐藏分数/晋升要求 | PASS |
| H no-advance | 正式no-advance，旧路径未兑现/不响应 | R9重建Review Plan并重排最近窗口路径；不续recipe、不机械追最低值、不保证追回 | PASS |

17个targeted tests PASS：current identity/interface/frozen shell + A–H、相关governance、deterministic two-build package。Frozen Runner的离线`validate_submission_contract` PASS，mode=skill_bundle，四个Skill集合一致；未调用Runner play/validate runtime CLI。白名单secret scan与git diff --check随交付完成。

## Packaging identity / verification boundary

仅离线临时验证包：`.local/scratch/s10-05/submission`；不install、不生成正式solution.zip、不提交比赛。

| File | SHA-256（本机验证包bytes） |
| --- | --- |
| manifest.json | 7378e943988bc7d28e0fd595e4baccb1d698a4b93c2784c73d39aae6e84178e1 |
| skills/delivery-progress/SKILL.md | 200b6c83aaca43f6dccfe58a30e23e79463e930512ef89cf5b19070a9d5d7528 |
| skills/risk-review/SKILL.md | 6da910fa60b07dfdccfc78a840ebc4777fc39e3188358e69ee483c89606874fd |
| skills/rolling-planning/SKILL.md | cd7e7434baf04ff38dbbfcf2a15727fc3c5d535dc22e9de29dc0ac23e5703a38 |
| skills/structured-state-board/SKILL.md | da76071dd035fcbb9073d69173db9a629f2404189709d39ea950dfd78bcd1cae |

Manifest name与Candidate ID一致；current_candidate保存canonical LF manifest/instruction hashes与四Skill Git blobs；Windows CRLF checkout的包可能有换行相关byte hash差异，不能直接拿另一checkout hash冒充本包。

v13 runtime、gameplay、provider及long-horizon adherence均未验证；score/survival improvement、stable75+、stable80+、hidden-test transfer均false。v8a历史gameplay/provider不转移为v13证据。install/service/provider/MCP/game/shared DB/official submission=0；FORENSIC_HOLD不解除，S10仍ACTIVE。

交付：本review、current_candidate、runtime_manifest、Planning、current-candidate tests、CURRENT_STATE。没有新Skill/Memory/Team或额外研究。返回本对话Main/Stage审查；commit/push/clean tree身份见TASK_RESULT。
