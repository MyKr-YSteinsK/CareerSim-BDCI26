# S06-09｜公开 Dev 机制与历史策略证据

> 本文是对冻结公开 Dev 数据、模拟器实现和仓库内已接受历史证据的离线汇总。它不修改当前候选，不证明任何机制能提高分数，也不授权下一局。

## 1. Source identity 与证据边界

- 本次基线：`main@2d33eb90212b6037e283238358c33604d3120149`；执行时 `main == origin/main`，工作区干净。
- 当前候选：`candidate-v4-lean-runtime-policy`，配置见 [`configs/current_candidate.json`](../../../configs/current_candidate.json)，运行指令见 [`configs/runtime_manifest.json`](../../../configs/runtime_manifest.json)。三个 Skill blob：`rolling-planning=fcd443d547920e04fcfa2dd948686136afb76d47`、`structured-state-board=06ecdc3a598ee42d1e785d6e14af8f1a669eca85`、`risk-review=50ac3c515d3e75ab060bb16e5afe51e79e4db3ab`。
- 冻结直接依赖：`career-emulator==1.0.1`、`career-emulator-bdci26==1.0.0`；Runner=`f61c738c72e51b77298cc1c14c7c6ebf4b6c527d`，见 [`OFFICIAL_SOURCE_LOCK.md`](../OFFICIAL_SOURCE_LOCK.md)。
- Dev 分发来源：PyPI 1.0.0 provenance 指向 `Flash-Tomato/CareerEmuData-Dev@e42324a8f904a7af60442989f986eae7390c94ee`（tag `v1.0.0`）。该 commit 的公开 [`convert.py`](https://github.com/Flash-Tomato/CareerEmuData-Dev/blob/e42324a8f904a7af60442989f986eae7390c94ee/convert.py) 将 `.data` 解码定义为 1 字节 split marker + raw DEFLATE（`wbits=-15`）+ msgpack；对应 [PyPI 发行与 provenance](https://pypi.org/project/career-emulator-bdci26/1.0.0/)。
- 本地只读源：根 `.venv/Lib/site-packages/career_emulator_bdci26/dev/dataset/` 与模拟器中 materialized 的 `career_emulator/data/dataset/`。两处 192 个 `.data` 相对路径和逐文件内容一致；全部成功解码。公开 Dev 目录共 194 个文件（192 `.data` + 两个 `.gitkeep`）；S01 锁定的整目录摘要为 194 files / `ecadbb6df2335e55b1e898de94102c9a2b2cdb23e8e7790912b8c2fb228d2fe4`。本次另对 192 `.data` 做排序后以相对路径、NUL、文件字节串接的 SHA-256：`493efab9d0dbae6fe4c94a1cae13e12c30e98e239a1afc5990d1803cdaa0dac4`。
- 192 个 `.data` 中：事件模板 171（短链 118、长链 53）；机制数据 21（事件池外配置：failure 7、promotion 3、salary 3、talk 2、initialization/regular 4、performance 1、ending score 1）。事件图包含 1,133 nodes、974 choice options、721 terminal nodes。没有读取 test/private 数据。
- 模拟器源码只读检查的主要位置：`career_emulator/failure_conditions.py`（性能和失败计数）、`promotion_conditions.py`、`talk_mechanism.py`、`salary_conditions.py`、`ending_score.py`、`game.py`（月份与季度顺序）、`events.py`、`server/models.py`（Choice 序列化和状态边界）。

证据标签：

- `DEV_CONFIRMED`：冻结 Dev 1.0.0 数据或模拟器 1.0.1 源码明示；只对该公开版本成立，不保证隐藏 Test 相同。
- `MULTIRUN_OBSERVED`：至少多个真实局重复出现；是描述性重复，不等同因果证据。
- `HYPOTHESIS`：与机制相符、但现有运行或机制证据不足以作确定结论。
- `DO_NOT_ENCODE`：事件特定答案、隐藏阈值或因果主张，不应写进 runtime policy。

## 2. Dev-confirmed 失败与生存机制

`hp` 是每条 failure rule 独立的剩余触发次数，不是 Career Health。每次 rule 触发后先应用配置的状态变化，再减该 rule 的 hp；归零才由此 rule 终止。周期计数在月度更新时采样，条件不满足则归零。模拟器内部 `failure_rule_remaining_hp`、`statistics` 和含 hidden 的状态字段会被当前 MCP 状态过滤移除。

| Rule | `DEV_CONFIRMED` 触发与计数 | 触发后的变化 | Terminal 条件 / handbook 可见性 |
| --- | --- | --- | --- |
| `health_zero` | Health `<=0`，即时检查 | 无额外变化；hp=1 | 首次即 terminal。Health 本身可见，归零后果也在公开手册说明。 |
| `dignity_crisis` | Dignity `<=1` 的月度连续计数达到 3 | Health−2、Network−1，计数清零；hp=2 | 第二次危机触发 terminal。计数/次数是实现细节。 |
| `network_isolated` | Network `<=1` 连续月度采样达到 3 | Output−2、Health−1、Dignity−1，计数清零；hp=2 | 第二次触发 terminal。计数/次数不是实时 MCP 状态。 |
| `wealth_deficit` | Wealth `<=0` 连续月度采样达到 3 | Dignity−1、Wealth 设为 0，计数清零；hp=2 | 第二次触发 terminal。连续计数不对 Agent 暴露。 |
| `risk_burst` | 内部 HiddenRisk `>=5`；无 streak | HiddenRisk 归零；Output 回退到 6 个已采样月度 Output 中最早值（不足 6 个时设为 0）；Dignity−2、Wealth−2、risk-burst 计数+1；hp=2 | 第二次触发 terminal。Dev 阈值、计数和库存不属于可观察 MCP 输入；手册只描述定性风险。 |
| `consecutive_bad_performance` | 半年采样点 performance `<4`，连续坏评计数达到 1；好评重置计数；hp=2 | Network−1、Dignity−3，计数清零 | 第二次连续坏评触发 terminal。内部 strike 状态不直接展示。 |
| `skill_obsolete` | Skill `<=0`；hp=5 | Dignity−1、Output−1、Skill 设为 1 | 第五次触发 terminal。复位细节是 Dev implementation detail。 |

公开手册说明了这些失败风险的宽泛类别与定性预警；Dev 数据/源码进一步揭示部分精确阈值、streak、hp 和 stat rollback。特别是 HiddenRisk 与剩余 HP 不能从当局 MCP state 读取。下表精确数值只为理解冻结 Dev 版本，不是 Agent runtime 的公开知识。

**策略含义｜`DEV_CONFIRMED` + `HYPOTHESIS`：** Health 归零是无恢复窗口的即时终止；其他多种危机还会通过扣 Health / Dignity / Network / Wealth 互相放大。可靠的政策对象应是新鲜公开状态、趋势、可见预警和剩余恢复机会，而不是猜隐藏库存或只追求某一个高分维度。

## 3. Performance、talk、promotion、wealth 与结算

### 半年 performance

**`DEV_CONFIRMED`**：模拟器用 `low=min(Skill,Network)`、`high=max(...)`；`capped=min(high,2×low)`、`excess=max(0,high−2×low)`。Stat 项为 `(capped + 0.3×excess)/15`（hard cap 配置为关闭），再加 `Output/10` 与按 Level 计算的九次多项式调整，最后取整数 round。多项式 Horner 系数从高次到常数为：

```text
[0.0000688932981, -0.0037202381, 0.0856316138, -1.09791667,
 8.59103009, -42.2239583, 129.157396, -235.174405, 228.665873, -86.0]
```

M1–M12 的 mercy：若该计算分数低于 4，则按 4 参与；M13 起不再适用。半年 bonus 档位是 S `>=12`、A `>=8`、B `>=5`、C `>=3`、D `<3`。这与坏绩效失败规则的 `<4` 不同：例如 score 3 对 bonus 属 C、但仍计坏绩效。公式、系数与分档均为隐藏/半隐藏 Dev 机制，不能放进 runtime prompt。

### Leader talk 与月份顺序

**`DEV_CONFIRMED`**：半年 talk 在月度状态更新之后、半年 performance / promotion 之前结算；talk score 不给 Agent 看。公式为：

```text
3.5×performance_score + Dignity + 0.25×Health − 2×HiddenRisk
− 4×risk_burst_count − 0.8×positive dignity_zero_consecutive_months
− 3×positive consecutive-bad-performance
```

- Good `>=35`：Dignity+2、Network+1、HiddenRisk−1，当前 review performance adjustment +2。
- Average `>=20`：Dignity+1。
- Bad `<20`：Dignity−2、HiddenRisk+1、Health−1，当前 review performance adjustment −2。

Agent 看到的是随机抽取的叙述反馈，而非 tier 分数。良好/不佳反馈可作为下一阶段的公开方向信号，不能据单条话术反推 talk score。

`game.py::_on_month_advanced` 的顺序是：更新派生/月度 streak → talk → 当月工资 → promotion review → 清除半年临时绩效调整。进入 M6/M12 等月份时先执行该结算；随后该月最多三次 story action 才进入季末 Energy / Main action。因此，M6 的事件伤害可以早于 Q2 Health recovery；若要覆盖这种风险，缓冲必须在 M5 完结/进入 M6 前已存在。Energy 不能追溯挽救已因 Health=0 终止的局。

### Promotion

**`DEV_CONFIRMED`**：半年 review；必须 alive、当前 Level 至少满 6 个月，最高 L10。名为 `optional_conditions` 的 performance 条件在实际 matcher 中也被 AND 到必需条件，不是可以忽略的建议条件。公开手册把晋升门槛定义为隐藏信息；下表只为理解 Dev 机制，不得转写成运行时阈值或月度保证。

| Dev transition | Skill | Output | Network | Dignity | Performance |
| --- | ---: | ---: | ---: | ---: | ---: |
| L1→L2 | 8 | 3 | 3 | 2 | 3 |
| L2→L3 | 18 | 5 | 6 | 3 | 4 |
| L3→L4 | 35 | 14 | 18 | 3 | 5 |
| L4→L5 | 90 | 22 | 30 | 4 | 4 |
| L5→L6 | 130 | 32 | 45 | 4 | 4 |
| L6→L7 | 170 | 45 | 60 | 5 | 6 |
| L7→L8 | 210 | 60 | 80 | 5 | 8 |
| L8→L9 | 250 | 75 | 100 | 6 | 10 |
| L9→L10 | 290 | 90 | 120 | 7 | 12 |

Promotion-specific Network changes are: L1→L2 none, L2→L3 none, then Network−2, −2, −3, −4, −4, −5, −5 for L3→L4 through L9→L10. These sit alongside the separate rapid-promotion penalty.

Dev 还按当前 Level 门槛×1.2 对 Skill / Network / Output 限幅；promotion 前超 cap 增长会被裁剪。若距上次晋升少于 12 个月，配置惩罚为 Network−3、Dignity−1。以上精确门槛和 cap 是 `DEV_CONFIRMED`，但 handbook 不向 Agent 公开，故 **`DO_NOT_ENCODE`**。可迁移原则是 review 可见的能力/交付/合作表现与 Leader 反馈，不猜数值门槛。

### Salary 与 ending score

**`DEV_CONFIRMED`** 月 base Wealth：L1 `0.3`、L2 `0.4`、L3 `0.5`、L4 `0.7`、L5 `1.0`、L6 `1.5`、L7 `2.3`、L8 `3.6`、L9 `5.7`、L10 `9.1`。每半年 bonus 为当时 Level 的月 base × performance tier multiplier（S `3`、A `1.5`、B `.5`、C `−1`、D `−2`）。月薪先于晋升支付；新 base 从次月生效。这证明公开 Dev 有 Level→salary/bonus 的复利机制，不证明晋升优先始终胜过 survival / opportunity cost。Score 的 `effective_wealth` 将 integer Wealth 与 fraction units / scale 10 合并。

| Local Dev score dimension | Weight | Normalization source / range |
| --- | ---: | --- |
| Level | 30% | Level number / 0–10 |
| Wealth | 20% | effective Wealth / 0–80 |
| Resilience | 15% | Health + Dignity / 0–20 |
| Skill | 15% | Skill / 0–120 |
| Risk Control | 10% | inverted `(risk_burst_count×5 + HiddenRisk)` / 0–10 |
| Network | 10% | Network / 0–60 |

Local `competition_partial_score = quantitative_score × 0.7`。**`DO_NOT_ENCODE`** 这些权重、normalized scales、score grades 或 `target=80` 进 runtime policy。它们只描述此公开 Dev scorer，不证明 hidden Test/cloud ranking 采用同一公式。

Local letter grades are S≥90, A≥70, B≥60, C≥50, D≥30, E≥0; they are distinct from the internal half-year performance bonus tiers above.

## 4. Quarterly action dominance

### Energy actions

**`DEV_CONFIRMED`**：每季 Energy=3，最多三次选择，不结转；选择 `no_action` 会结束 Energy 分配。固定行动菜单的 status updates 在选择前可见，不同于故事选项结果变化。

| Action | Cost | Visible state update | Classification / trade-off |
| --- | ---: | --- | --- |
| 高强度工作 | 2 | Output+2, Health−1, Dignity−1, HiddenRisk+1 | **Dominated**（在未封顶状态下）：两次 `准备汇报材料` 同耗能、Output+2/Dignity+2，不扣 Health 或增加 HiddenRisk。当前版本允许重复选择。 |
| 技能学习 | 2 | Skill+1, Health−1 | **State-dependent**；有独特 Skill 增益，但需计 Health 与 Energy 机会成本。 |
| 人脉维护 | 1 | Network+1, Dignity+1 | **Usually efficient**，当两项增益仍有用时。 |
| 处理历史埋雷 | 2 | HiddenRisk−1 | **State-dependent**；需要公开警告/相关风险线索；数值库存不可见。 |
| 心理修复 | 1 | Dignity+2 | **State-dependent**；对低位/下行有用，接近上限时可能被裁剪。 |
| 健康恢复 | 1 | Health+2 | **State-dependent / survival-efficient**；Health 低/下行且能早于风险发生时较有价值；封顶或 terminal 后无用。 |
| 准备汇报材料 | 1 | Output+1, Dignity+1 | **Usually efficient**，在两项都未饱和且对当前目标仍有用时；观察实际 delta。 |
| 保留体力（不行动） | 0 | 无变化；立即结束 Energy 阶段 | Energy 不结转，通常损失有效投入；若所有合法收益都会裁剪或造成更高已知代价，仍可能合理。 |

### Main actions

| Action | Visible state update | General prior（不是固定答案） |
| --- | --- | --- |
| 申请关键项目 | Output+2, Skill+1, Network+1 | 宽增长先验；若增益仍有用且风险可接受。观察到停滞或瓶颈转移时允许切换。 |
| 向领导汇报成果 | Output+1, Network+1, Dignity+1 | 适合相关公开 gap / review 可见性场景，仍须比较机会成本。 |
| 主动争取资源 | Output+1, Network+1 | 按当前 Primary Gap 决策。 |
| 申请岗位轮岗 | Skill+2, Network+1 | Skill 是可行动瓶颈或 key-project observed effect 停滞时纳入比较。 |
| 主动曝光成果 | Output+1, Dignity+1 | State-dependent；不自动优于汇报/关系路径。 |
| 建立导师关系 | Skill+1, Network+2 | Network gap 且公开情境支持时纳入比较。 |
| 修复关键关系 | Network+1, Dignity+1 | 当前关系破裂或 Network/Dignity 有公开压力时纳入比较。 |
| 低调避险 | Health+1, HiddenRisk−1 | 有公开生存/风险理由时比较；不能仅为降低不可见库存而选。 |
| 不行动 | 无变化 | 通常不如有用的合法动作；没有已验证的普适固定排序。 |

**结论：** “申请关键项目”的 `+Output/+Skill/+Network` 使其成为合理 broad-growth prior，不使它成为总是最优的默认项。可见菜单效果不是持久实际进展保证。应按 fresh observe、当前目标、剩余 horizon、public risk 与机会成本比较；不据事件标题生成答案表。

## 5. Entire Dev event pool：taxonomy 与公开线索

### Counting method and interface visibility

一次性只读解码 171 个模板、974 个 choice options。以下是多标签词项统计，不是官方类别：对 event name、probe dimension、node description、choice action 文本按显式词项匹配；一个模板可属于多个类。分类词表如下（大小写不敏感）：

- `SURVIVAL_HEALTH`：健康、身体、休息、作息、熬夜、疲惫、值班、on-call、加班、生病、传染、就医、失眠、体检、过劳、透支、理疗、住院、睡眠、饮酒、喝酒。
- `COMPLIANCE_CONFIDENTIALITY_SECURITY`：合规、保密、泄露、违规、外传、截图、授权、竞对、监管、隐私、客户数据、离职资料、SQL注入、安全漏洞、未公开。
- `TRUST_HIDDEN_RISK`：信任、隐患、诚信、甩锅、造假、问责、隐瞒、报复、掩盖、背锅、抢功、遮掩、爆雷、埋雷。
- `PERFORMANCE_DELIVERY_VISIBILITY`：output、交付、产出、汇报、晋升、评审、绩效、升职、关键项目、项目延期、项目。
- `NETWORK_RELATIONSHIP`：同事、关系、团队、沟通、协作、冲突、合作、跨组、mentor、午餐、朋友、团建、饭局、同桌、社交。
- `DIGNITY_BOUNDARY`：边界、底线、尊严、原则、妥协、体面、被迫、羞辱、贬低。
- `WEALTH_CAREER_OPTION`：成本、薪资、补偿、预算、奖金、涨薪、现金、费用、offer、报销、收入、买房、工资、期权、赔偿。
- `SYSTEM_RELIABILITY`：系统、代码、上线、CI、事故、测试、发布、bug、故障、服务、回滚、SQL、生产环境、漏洞。
- `ORG_POLITICS`：名额、功劳、核心圈、站队、绕过、越级、背锅、抢功、HR、评审会。
- `UNKNOWN_MIXED`：零个语义类或至少三个语义类。

在以上词表下，110 个“类别-词项”组合至少出现在 2 个独立模板中。该数包含泛词（如“同事”“项目”），是覆盖统计，不是 110 条策略触发规则。故事选项 Agent-visible payload 只有 choice/action（及过滤前的路由字段）；Dev 的 `status_updates` 不在选择前的选项 payload 中。故下表 effect signature 是**Dev 文件记录的选择后内部变化**，不是 Agent 可见的菜单收益。MCP 还会剔除含 hidden 的字段、statistics 与 failure remaining HP。Agent 的合法输入应为当前事件文本、公开手册、当前可见状态和行动后的 fresh observe。

| 分类 | 模板 / options | 常见 Dev 编码结果（至少一个选择有该变化的模板数；+/−） | 代表性场景 |
| --- | ---: | --- | --- |
| `SURVIVAL_HEALTH` | 45 / 251 | Health `25/37`；HiddenRisk `37/19`；Output `33/29` | “长假大促期间的 on-call 换班请求” |
| `COMPLIANCE_CONFIDENTIALITY_SECURITY` | 31 / 196 | Dignity `30/28`；HiddenRisk `30/26`；Network `29/29` | “得知未公开调整好友问买房” |
| `TRUST_HIDDEN_RISK` | 72 / 487 | HiddenRisk `68/46`；Dignity `66/58`；Network `64/63` | “合作同事会上甩锅”；“举报直属领导数据造假的吹哨两难长链” |
| `PERFORMANCE_DELIVERY_VISIBILITY` | 102 / 652 | Skill `91/22`；Network `85/80`；Output `79/70` | “项目延期如何向客户汇报长链”；“晋升停滞横转管理还是深耕长链” |
| `NETWORK_RELATIONSHIP` | 133 / 820 | Network `120/115`；Dignity `124/106`；HiddenRisk `122/66` | “新同事到岗后的 Mentor 节奏选择”；年会同桌社交 |
| `DIGNITY_BOUNDARY` | 62 / 454 | Dignity `58/52`；HiddenRisk `60/40`；Network `58/52` | “组会上被贬低为‘只是工程活’” |
| `WEALTH_CAREER_OPTION` | 51 / 335 | Dignity `48/43`；HiddenRisk `46/32`；Wealth `18/14` | “买房掏空首付还是留现金应对职业风险长链” |
| `SYSTEM_RELIABILITY` | 58 / 359 | HiddenRisk `54/38`；Skill `53/13`；Output `42/38` | “CI 自动化测试体系建设投入决策”；“发现安全漏洞修复成本高的抉择长链” |
| `ORG_POLITICS` | 45 / 305 | Dignity `41/36`；HiddenRisk `39/25`；Network `39/38` | “双VP邀请你选边站队长链” |
| `UNKNOWN_MIXED` | 126 / 787 | 混合：Dignity `114/97`、HiddenRisk `115/69`、Network `105/105`；不构成单一策略模式 | 未分类或跨 3+ 领域的复合事件 |

分类为多标签，故模板/options 行合计会重复。effect 数字是“至少一个选项具有该正/负 delta 的模板数”，不是选项数或 Agent 可见信息；正负变化在同一事件不同选项中常并存。类别、用词覆盖与数量皆为 heuristic，不是官方 taxonomy。

### Recurring keyword / trigger library（9 个语义簇）

这是把注意力导向情境审查的词簇，不是自动行动规则。generic 词“同事”“领导”“项目”单独出现不触发 Risk。

| Category / recurring phrases | Mechanism cue | Default response principle | Evidence / confidence |
| --- | --- | --- | --- |
| Survival：健康、身体、加班、熬夜、on-call、生病/传染 | Health=0 terminal；冲击可能累积，当前 Health 可见但后续事件未知 | 查看 Health、近期方向、下一恢复机会和当前文本风险；TIGHT 时优先避免 terminal，不靠季度恢复兜底 | 健康16、身体15、加班16、on-call4 个模板；failure=`DEV_CONFIRMED`；具体减值须当局观察；中高 |
| Compliance / confidentiality：合规、泄露、违规、保密、外传、截图/授权、未公开 | Dev 多个选择会改变 HiddenRisk；库存隐藏，单次无警告不证明安全 | 对明确的数据授权、外传、竞对或保密线索完整审查当前候选；不背诵答案 | 合规14、泄露6、违规5、保密4 个模板；effect=`DEV_CONFIRMED`，迁移=`HYPOTHESIS`；中 |
| Trust / hidden risk：信任、隐患、甩锅、隐瞒、造假、问责、报复、爆雷 | `risk_burst` 可大幅回退状态；HiddenRisk / 剩余触发数不可见 | 对明确的隐瞒/造假/责任转嫁线索检查公开后果、合规与升级风险；不推测库存 | 信任39、隐患26、甩锅5、造假5 个模板；rule=`DEV_CONFIRMED`；中 |
| Performance / delivery：交付、汇报、晋升、评审、项目延期、Output | 半年 review/promotion；真实门槛隐藏；重复 action 可停滞 | 用 fresh state、实际 observe delta 和 Leader 反馈更新 Primary Gap；广告收益不替代观察 | 交付33、Output34、汇报19、晋升18、评审16 个模板；重复关键项目=`MULTIRUN_OBSERVED`，无因果结论；中 |
| Network / relationship：同事、关系、团队沟通、跨组、Mentor、饭局/社交 | Network 低位 streak 与人际后果；一般摩擦也有机会成本 | 看关系事实及公开后果；不把社交频率当成长保证；按当前 gap 比较 repair/mentor 等路径 | 同事78、关系62、团队62、沟通33、跨组7 个模板；failure=`DEV_CONFIRMED`；中 |
| Dignity / boundary：边界、尊严、底线、妥协、羞辱 | 低位连续状态会触发惩罚；关系及职业结果可能同时变化 | 记录新鲜状态与趋势；一次礼貌让步不等同 crisis，长期低位亦不可忽略 | 边界27、底线17、尊严14 个模板；failure=`DEV_CONFIRMED`；中 |
| Wealth / career options：offer、买房、期权、预算、补偿、现金流 | Salary/bonus compounding 与 wealth-deficit streak；story Wealth delta 可能随 Level 放大 | 比较明确收支和不可逆机会成本；不假设隐藏回报 | 成本13、薪资7、奖金6、offer4、买房2 个模板；机制=`DEV_CONFIRMED`，收益泛化=`HYPOTHESIS`；中 |
| System reliability：CI、代码、上线、测试、事故、发布/回滚、漏洞 | Skill、Output、Network、HiddenRisk 间可能交换 | 明确可靠性/安全风险时审查后果；普通路线按交付证据、风险和当前 gap 比较 | 系统19、代码12、上线11、CI10、测试10 个模板；分类仍为启发式；中 |
| Org politics：名额、功劳、核心圈、站队、越级、HR | Dignity、Network、HiddenRisk 可能双向变化 | 区分事实、信用归属与推测；考虑可核验沟通，但不编码事件答案 | 名额7、功劳5、站队4、HR21 个模板；选项效果各异；中低 |

关键词只可用于触发当前情境 FULL_REVIEW。Dev option deltas 对选择者不可见，不能用离线全量解码反推所谓正确选择。

## 6. Historical run cross-analysis

来源是当前 [`RUN_HISTORY.md`](../RUN_HISTORY.md)、v4 的 [S06-08 read-only forensic](../runs/v4-run1-health-forensic.md)，以及 Git 历史中的 S04 RESULT / compact trajectories。S06 Run #1 原始本机 transcript/events 当前不可用；本节不重建 raw，也不把运行摘要升级成因果事实。

| Run | Result | Survival / promotion | 行为与证据边界 |
| --- | --- | --- | --- |
| S01-03 no-op | 26.95 / 18.86 / 19m / E | M19 淘汰 | 运行闭环 baseline，不是策略比较。 |
| SCORE-01 | 33.06 / 23.14 / 24m / D；候选身份 UNKNOWN | 最后公开 L2；约 7 个已到季度主行动均选关键项目；原因 UNKNOWN | 不与后续候选作因果对照。 |
| Candidate v1 Run #1 | 76.04 / 53.23 / 48m / A | Health 最低 4；升职 M6/M12/M18/M36/M48；完成 48 月 | 主行动 16/16 关键项目；Energy：Health recovery 11、汇报材料25、Network6、埋雷处理3；3 个 Planning checkpoint。高分无策略归因。 |
| Candidate v1 Run #2 | 35.31 / 24.72 / 25m / D | 升职 M6/M12/M24；第二次 trust crisis 终止，终局 Health10 | 关键项目7/8已到季度；Health recovery 8、汇报5、Network5、埋雷处理3。Health 回补不能单独解释存活。 |
| S06 Run #1 | 53.83 / 37.68 / 48m / C；候选身份 UNKNOWN；终局 L4 / Wealth21.8 / Skill89 / Network36 | 到达 M48；promotion months UNKNOWN | 主行动16/16关键项目；后期部分重复选择无 public growth 仍基于 advertised effect；Output26 后仍反复准备汇报；Planning 集中于早期。单局行为不说明最终分数因果。 |
| Candidate v4 Run #1 | 25.84 / 18.09 / 6m / E | Health `5→3→2→4→3→4→3→2→1→0`；M6 terminal | Q1 在 H2 选择一次健康恢复；H1 已表达生存风险仍先选 Growth。最后 -1 来源无法独立归因。23/23 take_action 成功，是有效游戏终止而非 provider/runtime 故障。 |

- **`MULTIRUN_OBSERVED`**：Candidate v1 两局分数差 40.73、partial 差 28.51、存活差 23 个月（48m/A vs 25m/D）；不能只据最好一局宣称稳定 80+。
- **`MULTIRUN_OBSERVED`**：多个记录策略局重复使用“申请关键项目”（S04-03 16/16、S04-04 7/8、S06 Run #1 16/16）；成败取决于当前 gap 与事件路径，不能给该动作归因。
- **`MULTIRUN_OBSERVED`**：v1 #1 较高 Health 回补与 48m 存活同时出现；v1 #2 以 Health10 因 trust crisis 结束；v4 逐步 Health 耗尽。证据支持多风险通道，而非“多 Health recovery 即稳定生存”。
- v4 Run #1 adherence snapshot（单次、仅 M1–M6）：三个 Skills 各读取一次；未观察到 career-action-trace / S02 / S03 marker；结构化 Board 只有开局一次，后续 fresh observe 未转成结构化趋势 refresh；Planning 只有开局 checkpoint，`STALLED` 未出现；Risk 结构化状态输出为 0，精确大写 `RECONSIDER` marker 为 0。普通文字中小写 `reconsider` 共 17 次（16 次在终局前、1 次局后反思，约 10 次集中在 Q1 Energy 同一决策窗口），不能算作 Risk trigger。H1 时 Agent 已说出 Material Risk 却仍先选成长；这是行为证据，不是死亡 action 的因果归因。
- v4 仅运行至 M6，不能评价季度/半年周期的长期 adherence、后期 phase 或 STALLED switch 是否有效。
- **`HYPOTHESIS`**：季度 checkpoint、fresh observed delta 与 survival band 可能减少无效重复或延迟恢复；Candidate/事件路径未匹配，没有策略因果估计。
- 现有历史数据无法证明稳定 80+、Skill 独立收益或 hidden-test 泛化。压缩轨迹支持有限行为描述；S06 Run #1 raw 缺失限制更细复析。

## 7. 48-month strategy evidence

### Six-month micro-cycle（按实际事件顺序，不是固定 action 日历）

1. **窗口开始 / fresh observe**：更新 month、公开 Health/Dignity/Network/Wealth、Leader feedback、近期 observed delta；设单一 Primary Gap 与 survival band；未知字段标 UNKNOWN。
2. **季度 Energy + Main**：先满足 terminal/material risk 约束，再按 Primary Gap 比较 action。Energy 不结转；Main action 的公开 advertised delta 不保证持久增长。
3. **M5→M6 等半年窗口前**：进入 M6 时先执行 talk、salary、promotion 结算；之后 M6 最多三次 story actions，才到 Q2 Energy/Main。故 M5 结束前复核 survival reserve，不能依赖 Q2 的 Health+2 处理此前已发生的事件。
4. **review 后适配**：fresh observe 实际 Level、Skill、Network、Output、Dignity、Wealth 与 feedback，再更新 Primary Gap；不从反馈叙述猜分数。
5. **progress 对照**：在同一目标和可比 public state 下标 ADVANCING / STALLED / UNKNOWN；一次没涨只记录，不强制切换。两个可比较 checkpoint 均无进展才比较不同类型路径；来源污染或不可比则 UNKNOWN。

### Macro phases（状态驱动，非月份硬切）

| Phase | Primary objective | 生存与 review | Energy / main prior | 转换条件 |
| --- | --- | --- | --- | --- |
| Foundation / Survival | 建立可持续职业资产，同时避免不可逆生存风险 | 对 Health/Trust/Compliance 预警保持 WATCH/TIGHT；积累真正可用的 Skill、Output、Network | 平衡成长与 Health/Dignity reserve；关键项目是 broad-growth prior，遇停滞可比较替代 | fresh profile 与反馈呈现稳定基础或明确 gap |
| Promotion engine | 让公开能力、交付、合作与反馈支撑下一次实际 review | 关注半年窗口与可见 Leader feedback；不猜门槛或忽略快速晋升成本 | 比较 key project、rotation、report、mentor、relationship repair | 已观察 promotion，或同一目标两个可比 checkpoint 停滞 |
| Compounding | 组合新 Level 的 salary/bonus 与可持续输出 | 保护半年 performance；M13 后 first-year mercy 结束 | 平衡 Skill/Network/Output；不盲目重复饱和项 | 当前瓶颈改变、warning 更新或 horizon 收缩 |
| Final sprint | 将剩余月份用于可观察、可兑现的当前收益 | 不以不可知的长期风险换不可能兑现的远期收益；继续避免终止 | 当前 gap 与收益时程相匹配；降低纯远期收益优先度 | 按实际剩余月份/收益时程判断，不是固定 M36/M42 指令 |

**公开 Dev 关系：** 晋升会提高后续月薪和半年 bonus 基数；Skill/Network performance 互动有软上限；Output 贡献 performance 并进入各级晋升门槛；M1–M12 mercy 可掩护早期低 performance，M13+ 不再适用。Good talk 可改善当前 review adjustment 并增加 Dignity/Network、降低 HiddenRisk；Bad talk 相反，形成短期正/负反馈环。精确公式/门槛不可作为 runtime score optimizer。

## 8. Survival Guard design evidence

SAFE / WATCH / TIGHT / CRITICAL 是候选 policy bands，不是游戏内阈值，也不等同 HiddenRisk 数字。

| Band | 只依据公开 evidence 的候选语义 |
| --- | --- |
| SAFE | 生存状态 fresh 且稳定；无当前 material warning；仍有正常增长空间。 |
| WATCH | 有下行趋势、接近曾观察到的 shock 尺度、近期高负荷/疾病/信任线索，或恢复机会较远；提高观察和候选审查频率。 |
| TIGHT | 当前 Health 低且下降，或多个可见严重后果叠加；将生存缓冲视作约束，普通成长成本不能单独压过即时安全。 |
| CRITICAL | 公开状态已近 terminal 后果，或可信的小幅减值可能越过 Health=0；暂停非必要成长，优先可验证保护路径，不创造固定 Health≤N 规则。 |

- **Health**：依据 fresh observe 与趋势；v4 中观测到 `−1/−2` 变化仅是实际冲击尺度，不是全局 shock 上限。Policy safety margin ≠ game failure threshold。S06-08 支持 targeted guard hypothesis，但终局最后 -1 归因不确定。
- **Dignity / Network / Wealth**：观察公开状态是否长期低位、半年叙述是否恶化、回补是否停滞；不在 Skill 写入 Dev 连续月计数阈值。
- **Hidden risk**：不猜内部余额；响应明确公开警告、历史埋雷反馈、合规/信任/报复线索，并在后续 fresh observe 核对实际后果。
- **Performance**：半年 feedback 和 promotion result 是可见证据；不从隐藏公式计算 score/strike。

## 9. Skill activation contract（供 Main review）

高频执行短扫描，不要求每步全文重读 Skill。

| Skill | QUICK_SCAN | FULL_REVIEW |
| --- | --- | --- |
| `structured-state-board` | 每次 fresh observe 后看 month/review window、Health/Dignity/Network/Wealth、趋势与当前 phase | New game、季度、survival band 改变、material state change、context recovery；Board 保持 bounded，不复制 transcript |
| `risk-review` | 每次 action submit 前过 survival guard、当前候选公开后果、明确 compliance/trust/hidden-risk cue | 当前候选命中 material warning、WATCH/TIGHT/CRITICAL 或重大后果线索时；仍遵守四态/no-submit 边界 |
| `rolling-planning` | 每次决策 consult phase、单一 Primary Gap、survival band 与最近 progress；仅短提醒 | 季度、半年 feedback、promotion result、Primary Gap 变化、STALLED、context recovery |

高频功能调用与全文 file reread 是两回事。三个现存 Skills 保持 advisory/domain scope，Single Agent 仍是唯一 action submitter。实际 Agent 是否遵循 cadence 未经新运行验证。

## 10. Runtime change decision（仅供 Main review）

以下是建议决策，不是本任务实现结果：

| Change | Decision | 证据与边界 |
| --- | --- | --- |
| Public-state Survival Guard（SAFE/WATCH/TIGHT/CRITICAL） | **ADOPT** | v4 cumulative-health forensics + Dev 即时 Health failure；基于趋势/当前可见状态，不设经验阈值；需未来单独 benchmark 验证。 |
| Phase-aware Planning | **ADOPT** | Level/salary、半年 review、剩余 horizon 支持按状态滚动阶段；不用固定月份→动作。 |
| Six-month review clock / pre-M6 reserve check | **ADOPT** | `game.py` 时序 `DEV_CONFIRMED`；只作 checkpoint，不预测晋升。 |
| Event keyword trigger library | **ADOPT（semantic cue only）** | 把公开情境线索升级到 Risk FULL_REVIEW；不得变成标题查表/自动答案。 |
| Three Skills QUICK_SCAN cadence | **ADOPT** | 可以短频用而不每步全文重读；实际 adherence 仍待观察。 |
| Explicit action priors / fixed priority ranking | **DEFER** | Main 菜单宽增长效应可确认，但 gap、caps、risk 和 observed stall 改变收益；不冻结固定 winner。 |
| Exact Dev score weights / thresholds in runtime prompt | **REJECT** | evaluator leakage / hidden-test overfit 风险；只留作 Dev 研究证据。 |
| Exact HiddenRisk numeric threshold in runtime prompt | **REJECT** | Dev 数据可读但 Agent/handbook 隐藏；不反推正式策略阈值。 |
| Event-specific answer lookup | **REJECT** | 过拟合 Dev 事件/路径，不具备公开泛化保障。 |
| Durable / cross-game Memory | **DEFER** | 本任务没有核验其可移植性、生命周期或 session isolation；当前仍未实现。 |
| Fifth Skill | **DEFER** | 无证据证明新 Skill 优于现有 3 域内的最小规则。 |
| Team / Swarm | **DEFER** | 无新的角色分离证据；Single Agent remains sole action submitter。 |

## 11. DO_NOT_ENCODE / unknowns

- 晋升门槛、performance polynomial、talk score formula、Dev score weights、HiddenRisk threshold、risk-burst HP：即使 `DEV_CONFIRMED`，对 Agent 仍是隐藏/半隐藏实现，不编码进 runtime instruction。
- `event_id/title → exact choice`、story option 内部 status update lookup、根据相关性宣称动作收益：`DO_NOT_ENCODE`。
- `Health<=2`、固定某月必做恢复、固定 phase 月份或每季度必选关键项目：证据不足，`DO_NOT_ENCODE`。
- v1 两局及 v4 单局均不证明 Survival Guard / Planning / Risk cue 的因果收益；stable 80+、Test transfer、cloud score 仍 `NOT_PROVEN`。
- 云端是否采用完全相同公开 Dev 规则未知；本次仅核验公开包身份与本地冻结版本。
- `NEXT_GAME=NOT_AUTHORIZED`；本文建议的 ADOPT 仅供 Main 评审，未创建 Candidate、未安装策略、未启动 runtime。
- 本任务 provider/service/MCP/CareerSim/game 均为 0；未改 Skills、candidate config、Runner、dependency、CURRENT_STATE 或 architecture。

## 12. Sources

- 项目事实：[`CURRENT_STATE.md`](../CURRENT_STATE.md)、[`RUN_HISTORY.md`](../RUN_HISTORY.md)、[`OFFICIAL_SOURCE_LOCK.md`](../OFFICIAL_SOURCE_LOCK.md)、[`v4-run1-health-forensic.md`](../runs/v4-run1-health-forensic.md)。
- Frozen package metadata：root `.venv/Lib/site-packages/career_emulator-1.0.1.dist-info/METADATA`、`career_emulator_bdci26-1.0.0.dist-info/METADATA`；数据 `career_emulator_bdci26/dev/dataset/**/*.data`。
- Simulator source：`career_emulator/failure_conditions.py`、`promotion_conditions.py`、`talk_mechanism.py`、`salary_conditions.py`、`ending_score.py`、`game.py`、`events.py`、`server/models.py`。
- Public decoder/provenance：[pinned `convert.py`](https://github.com/Flash-Tomato/CareerEmuData-Dev/blob/e42324a8f904a7af60442989f986eae7390c94ee/convert.py), [PyPI 1.0.0](https://pypi.org/project/career-emulator-bdci26/1.0.0/).
- Category/event counts came from one-off in-memory parsing of the full public Dev event directory. No decoder/analyzer or per-event answer table was committed.
