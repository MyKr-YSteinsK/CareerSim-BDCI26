# S10-04｜晋升前沿与高分策略研究

**结论：恢复简单 promotion-first 策略优先级，并根据 fresh realized response 调整资源分配，是唯一首选方向（Option A）。这是可执行假设，不是已证明的最优策略。** 10 个核心 runs 全部可定位并核验；得到 1,626 条转移、64 次 Review、30 次晋升。`READY_FOR_EMPIRICAL_POLICY_GATE`；`NEXT_GAME=NOT_AUTHORIZED`。

## 身份、方法与验证边界

- Branch：main；Base：`9edf73de552ce91af9d9eecf2dbbe6f5def9461d`。交付身份为包含本报告的 Git commit，commit/push/clean tree 回执见本对话 TASK_RESULT。默认 main 串行；没有合入 S09/S10 experimental Candidate 分支。
- S09 canonical evidence 从显式固定 `c41a1b7210a02603aa19cc2bab19922a80b6cd77` 读取；v12 从显式 `673caa9e467a803500bf3e2fb3bd5df8da45956c` 读取。10 个 raw events SHA-256 与原登记一致。完整路径/bytes/hash/session/locator 在 JSON。
- 每 run 恰一 fresh new_game session；按 tool_call_id 去重 wire record，只收成功 action→下一 action 前首次 fresh observe。失败、未观察动作及仅 receipt 无可见改变排除。RUN21 最后一个成功但缺 observe 的动作排除，不补终局分数。RUN08 三个官方接受的字符串 choice 被明确归一化并保留原类型，不能宣称整数协议全部遵循。
- Main 优先按菜单识别（其 energy_cost=0 不能误当 Energy）；HANDBOOK 10、STORY 1,158、ENERGY 332、MAIN 126。Main 全跨月；clean 同月同 Level 非 Review：Story 900、Energy 332、Handbook 10。clean 仍不能排除延迟 Story 效应。
- Review 必须 pre_observe_line < trigger_action_line < first_review_observe_line，同 session 成功 receipt。64/64 精确边界。预先结果/警告/约束只取此前观察；第一次含 Review 的回包内新结果和变动单列。绝不用同月后续 Energy/Main 或终局特征作为前序决策 predictor。
- JSONL 无需新依赖。构建脚本只接显式 manifest/output 路径，不查 latest、DB、provider 或私有 Test；白名单只取公开 H/D/S/N/O/W/E、Level/tenure、公开 event/menu、feed、ending score。HiddenRisk 仅保存菜单明确 advertised signed delta；不保留或重建 stock。
- event_public_fingerprint 仅离线比较完整公开 context/menu，不产生 title→action 答案表。语义词法代理是研究标签，不是游戏状态；首次下一观察的结果可能属于另一条异步链，不能当该 action 的净结果。

## 样本与终局

| Run | 转移 | Review/晋升 | score / months / Level | 分类 |
| --- | --- | --- | --- | --- |
| v6 | 202 | 8/5 | 75.29 / 48 / L6 | 自然完成 |
| v7o | 205 | 8/4 | 71.83 / 48 / L5 | 自然完成 |
| RUN07 | 203 | 8/4 | 72.65 / 48 / L5 | 自然完成 |
| RUN08 | 205 | 8/3 | 59.0 / 48 / L4 | 自然完成 |
| RUN10 | 201 | 8/4 | 68.4 / 48 / L5 | 自然完成 |
| RUN17 | 23 | 1/1 | 24.47 / 6 / L2 | 自然淘汰 |
| RUN19 | 132 | 5/3 | 38.08 / 33 / L4 | 自然淘汰 |
| RUN20 | 203 | 8/3 | 60.6 / 48 / L4 | 自然完成 |
| RUN21 | 158 | 6/3 | UNKNOWN / partial M37 / L4 | 技术截断 |
| v12RUN01 | 94 | 4/0 | 23.48 / 24 / L1 | 自然淘汰 |

6 条 48m 完整局、3 条提前自然淘汰、1 条技术 partial；缺失核心 runs=0。max observed month=49 的完成局仍以官方 survival_months=48 为准。v12 已先出现自然 terminal，随后监控脚本异常/Runner收尾连接错误不改变淘汰身份；RUN21 不与失败组或完整组混算。

## Promotion frontier（严格 pre→first-result）

| Level | 晋升/Review | 晋升 pre S/N/O 范围 | 未晋升 pre S/N/O 范围 | 经验边界 |
| --- | --- | --- | --- | --- |
| L1 | 9/15 | {'S': [9, 9], 'N': [2, 3], 'O': [2, 3]} | {'S': [9, 9], 'N': [1, 3], 'O': [0, 3]} | 范围重叠，不是阈值 |
| L2 | 8/9 | {'S': [20, 21], 'N': [6, 7], 'O': [5, 6]} | {'S': [21, 21], 'N': [7, 7], 'O': [5, 5]} | 范围重叠，不是阈值 |
| L3 | 8/17 | {'S': [36, 42], 'N': [21, 21], 'O': [13, 16]} | {'S': [36, 42], 'N': [10, 21], 'O': [8, 14]} | 范围重叠，不是阈值 |
| L4 | 4/17 | {'S': [89, 100], 'N': [35, 36], 'O': [24, 26]} | {'S': [47, 83], 'N': [26, 36], 'O': [19, 26]} | 任职期18仅与本样本晋升一致 |
| L5 | 1/6 | {'S': [140, 140], 'N': [54, 54], 'O': [37, 37]} | {'S': [108, 126], 'N': [47, 54], 'O': [33, 38]} | 只有1 positive，不可泛化 |

- L1：promoted pre O2–3，non-promoted O0–3，S 都9。RUN19 pre O2 仍晋升；v12 M12 pre O3/C 仍不晋升。
- L2：8/9 晋升；唯一反例 RUN21 M12 pre S21/N7/O5、tenure6，first O4，不晋升；M18 first O5 才晋升。不能据高命中率写充分条件。
- L3：8/17 晋升，所有 promoted pre N21，但 non-promoted 也可 N21；RUN19 M30 pre S42/N21/O13 晋升，RUN08 M30 同 S/N/O 未晋升，tenure18 vs12。N21 或 O14 均不能还原机制。
- L4：4/17 晋升均 tenure18、S89–100，未晋升 tenure6/12、S47–83。资本、故事和 tenure 共变，不能硬编码“18个月必升”。
- L5：v6 M48 pre S140/N54/O37、tenure12晋升；v7o同tenure12、S126/N54/O38、A但不晋升。Output更高不是充分条件；只有一条L6支持，`INSUFFICIENT_EVIDENCE`。

### M6 精确边界与矛盾

| Run | pre S/N/O/W/H/D | first S/N/O/W | grade→Level | pre→trigger→first raw lines | pre result proxy |
| --- | --- | --- | --- | --- | --- |
| v6 | 9/3/3/2/5/10 | 9/3/3/3 | C→L2 | 183→185→191 | 1 |
| v7o | 9/3/3/3/5/9 | 9/3/3/3 | C→L2 | 179→181→187 | 1 |
| RUN07 | 9/3/3/2/3/10 | 9/3/3/2 | C→L2 | 179→181→187 | 3 |
| RUN08 | 9/3/3/3/5/9 | 9/3/2/3 | C→L1 | 179→181→187 | 1 |
| RUN10 | 9/2/3/2/4/10 | 9/3/3/2 | C→L2 | 171→173→179 | 1 |
| RUN17 | 9/3/3/2/3/10 | 9/3/3/2 | C→L2 | 179→181→187 | 1 |
| RUN19 | 9/3/2/3/5/10 | 9/3/3/3 | C→L2 | 179→181→187 | 1 |
| RUN20 | 9/3/3/2/4/10 | 9/3/2/2 | C→L1 | 179→181→187 | 1 |
| RUN21 | 9/2/3/2/4/10 | 9/3/3/2 | C→L2 | 179→181→187 | 1 |
| v12RUN01 | 9/1/0/2/6/10 | 9/3/0/2 | C→L1 | 171→173→179 | 2 |

v7o/RUN08 的全部公开数值 H/D/S/N/O/W/E、Level、tenure 在 pre 完全相同，但 first O3 vs O2、晋升 vs 不晋升；这不是完整历史/事件相同的随机反事实。RUN07/RUN17 pre 数值完全相同且都晋升，但后者同M6 H归零。RUN10/RUN21 pre一致且首晋升一致，后续cadence不同。只看任一数值或M6晋升都不足。

pre-visible delivered/recognized：RUN07 M4 raw139 为如期上线+业务满意，proxy3；v12 M5 raw155 CI上线为proxy2而不晋升。v6/v7o/RUN10在pre未匹配到强完成词仍晋升，说明标签不是必要条件。RUN08低保真原型确认 raw187首次出现于Review回包，不能倒算pre-result；RUN20相同原型确认在M4 raw139，仍未M6晋升，说明“任何认可”不是充分条件。

### 早期复利与轨迹对比

| Run | M6 Level; first S/N/O/W | M12 Level; first S/N/O/W | M18 Level; first S/N/O/W |
| --- | --- | --- | --- |
| v6 | L2; 9/3/3/3 | L3; 20/4/5/4 | L4; 37/16/14/8 |
| v7o | L2; 9/3/3/3 | L3; 21/4/6/5 | L4; 38/16/14/8 |
| RUN07 | L2; 9/3/3/2 | L3; 21/4/6/3 | L3; 41/11/15/5 |
| RUN08 | L1; 9/3/2/3 | L2; 9/3/3/3 | L3; 21/4/6/5 |
| RUN10 | L2; 9/3/3/2 | L3; 21/4/5/2 | L3; 38/19/12/5 |
| RUN17 | L2; 9/3/3/2 | 未到达 | 未到达 |
| RUN19 | L2; 9/3/3/3 | L3; 21/4/6/4 | L3; 42/16/11/8 |
| RUN20 | L1; 9/3/2/2 | L2; 9/3/3/3 | L3; 20/4/6/6 |
| RUN21 | L2; 9/3/3/2 | L2; 21/7/4/4 | L3; 21/7/5/6 |
| v12RUN01 | L1; 9/3/0/2 | L1; 9/1/3/4 | L1; 9/2/3/4 |

高参考 v6/v7o/RUN07/RUN10：4/4 M6晋升；低分完整 RUN08/RUN20：2/2 M12才晋升。M12高参考 S20–21 vs低分S9；M18高参考S37–41 vs低分20–21。高组final68.40–75.29、L5/L6，低组59–60.60、L4；这是按终局分组的描述，不能识别早晋升的独立因果贡献。RUN17/19早晋升却终止，RUN21只partial，均阻止“早升就高分”结论。

公开工资 feed 在本样本各 Level 观察到：L1 +0.3、L2 +0.4、L3 +0.5、L4 +0.7、L5 +1.0、L6 +1.5（单位按游戏显示）。这支持早升与收入积累相关；奖金/成本/机会同时变化，未估计某局若提前升会多赚多少。后续 opportunity/result 出现频率受事件曝光与词法覆盖混杂，下文仅报告 proxy 频次，不把不同 exposure 当政策效应。

## Recurring Main：何时有效，何时重复

| family | n | next Review 晋升/known | 边界 |
| --- | --- | --- | --- |
| 低调避险 | 9 | 2/7 | 全部跨月，非独立样本 |
| 向领导汇报成果 | 8 | 3/7 | 全部跨月，非独立样本 |
| 建立导师关系 | 5 | 0/4 | 全部跨月，非独立样本 |
| 申请关键项目 | 101 | 45/97 | 全部跨月，非独立样本 |
| 申请岗位轮岗 | 3 | 3/3 | 全部跨月，非独立样本 |

101/126为关键项目，低调9、汇报8、导师5、轮岗3。JSON按Level给出pre资源范围、全部6维mixed正/平/负/总量、Review距离和后续关联；同一Review被多个action共享标签，不能当独立成功率。

v6 key14/16+低调2/16→75.29，RUN08 key16/16→59。项目只有在产生可兑现ownership/后续结果、资源能承受且没有明确危险时才具备较强策略理由；若此前链延期/机会不可达/已有负荷或警告上升，重复同菜单选择没有净收益证据。所有Main跨月使“有效程度”只能依赖公开后续结果与本局反馈，而不能以数值差恢复净动作效应。其它family选择样本少，不能宣布任何替代always better。

## Recurring Energy：局部响应政策

| family | n | 目标增益/平 | 体力cost | Health净变化总和 | next Review晋升/known |
| --- | --- | --- | --- | --- | --- |
| 人脉维护 | 56 | 40/16 | {'1': 56} | 0 | 23/52 |
| 健康恢复 | 87 | 85/2 | {'1': 87} | 164 | 37/83 |
| 准备汇报材料 | 142 | 109/33 | {'1': 142} | 0 | 52/136 |
| 处理历史埋雷 | 23 | 公开6维全部平；风险stock不检验 | {'2': 23} | 0 | 13/20 |
| 心理修复 | 1 | 0/1 | {'1': 1} | 0 | 1/1 |
| 技能学习 | 6 | 6/0 | {'2': 6} | -6 | 3/4 |
| 高强度工作 | 17 | 13/4 | {'2': 17} | -17 | 7/17 |

心理修复目标D：唯一1次pre D10、realized D0（n=1）；处理埋雷23次公开6维平，不等于无风险收益：stock不读取、advertised risk delta不证明解除。所有Energy同月同Level且不含Review，因此兑现量比Main更可分辨，但仍不保证无延迟Story影响。

| 汇报 Level | O增益/n | no-gain | 样本中 flat 的pre O |
| --- | --- | --- | --- |
| L1 | 7/17 | 10 | [3] |
| L2 | 18/23 | 5 | [6] |
| L3 | 39/42 | 3 | [16] |
| L4 | 27/39 | 12 | [26] |
| L5 | 17/20 | 3 | [38] |
| L6 | 1/1 | 0 | [] |

表中的3/6/16/26/38只是样本flat位置，不是可部署的全局上限表。相同Level低于这些位置的已选汇报均有局部增益，但选择分布窄、其它context未知。按run/Level/family前次目标平后：汇报9次继续平、5次恢复增益；不能永久封禁。v12四次O3汇报平（M3 raw107→115、M6 211→219、M15 507→515、M18 603→611），M21 O2 raw707→715又+1；M18高强度O3平却H-1 raw595→603。

人脉目标N40/56增，16平；健康目标H85/87增、2平，体力均1。高强度13/17 O增、4平，17/17 H-1，体力2；学习6/6 S+1同时H-1、体力2，不能把6样本当全局最优。完整JSON还按Level/pre-target、日历Review窗口（month mod6=0/3）、上次same-run/Level/family目标反应分层；next Review只作后验label。代价以广告体力和fresh E状态分开记录，季度配额/剩余值不能简单当action净耗量。

LOCAL_RESPONSE_POLICY：同Level/可比context发生可确认NO_GAIN时折价该目标，先比较其它有响应维度或一次有价值的探索；新Level、目标回落、菜单/依赖变化是重新评估的material evidence。探索获益仍是假设，无额外game预算。

## Story语义、结果与认可

14个语义features仅来自公开选项文本：短交付、长技术资产、ownership、visible result、recognition、stakeholder alignment、transparency、mentoring、networking、compliance、shortcut、recovery、avoidance、report only；多标签重叠，词义/否定可能误判，不做title答案表。

| feature | selected Story n | first-next proxy 0/1/2/3 | delay proxy |
| --- | --- | --- | --- |
| AVOIDANCE | 21 | {0: 15, 1: 6} | 4 |
| COMPLIANCE_SAFE | 62 | {0: 53, 1: 9} | 3 |
| LONG_CYCLE_TECH_ASSET | 17 | {0: 16, 1: 1} | 1 |
| MENTORING | 18 | {0: 16, 1: 2} | 1 |
| NETWORKING | 108 | {0: 89, 1: 19} | 5 |
| OWNERSHIP | 43 | {0: 36, 1: 5, 2: 2} | 1 |
| RECOGNITION_SEEKING | 11 | {0: 10, 1: 1} | 0 |
| REPORT_ONLY | 0 | {} | 0 |
| RESOURCE_RECOVERY | 17 | {0: 17} | 0 |
| RISKY_SHORTCUT | 4 | {0: 4} | 0 |
| SHORT_CYCLE_DELIVERABLE | 10 | {1: 2, 0: 8} | 0 |
| STAKEHOLDER_ALIGNMENT | 71 | {0: 58, 1: 11, 2: 2} | 2 |
| TRANSPARENCY | 77 | {0: 61, 1: 16} | 2 |
| VISIBLE_RESULT | 66 | {0: 54, 1: 11, 2: 1} | 2 |

RESULT_STRENGTH 0无证据/1承诺或进展/2具体完成/3具体完成且公开认可；泛泛HR夸奖不升级。首次next-observe代理常为0/1，因为故事结果异步出现。不能据此说长资产从未交付，或短交付只有20%成功。

全部Review pre窗口proxy：1有23晋升/24不晋升；2有5/10；3有2/0；proxy3仅2条（同一run窗口可相关），不能把2/2当充分条件。没有可靠校准的结果频次→final score模型。

最强语义分叉：RUN07 M3选开源快交付（pre83/action85/post91），RUN08 M1选长期自研（pre35/action37/post43），完整公开context/menu fingerprint一致；但pre资源、月份与其它链不同。RUN07 M4 raw139公开如期上线+业务满意，随后CVE严重安全约束；RUN08 M2 raw59公开严重延期。RUN19 M5同自研选择、M6 raw187延期却同时晋升，明确反驳“自研必阻止晋升”。v12 M4搭建CI、M5 raw155完成、M6仍L1，反驳“完成基建即可晋升”。RUN20原型确认是对齐/返工范围确认，不应自动计为已交付成品。

因此仅MEDIUM支持“窗口内能兑现、责任和认可明确的方案优先，且需安全/依赖检查”。开源自身有CVE代价；长期CI确有完成证据；没有普适技术路线答案。结果/认可/延期examples的定位在JSON semantic_cases，其余Review已有pre_result/pre_warning/pre_constraint source行。

## Risk / survival：何时覆盖成长

- RUN17：M6已晋升，H3高密度带教后H1（raw195→203），选择维持手动Review后H0终止（raw203→211）。后一步从选项意图看并非高强度成长，证明“不选新投资”也不保证当前危险解除；无法证明恢复反事实一定救局。
- RUN19：M31 raw1051“积攒了不少风险”；M32 raw1075“之前埋的雷全要炸了”；M33改写责任报告后raw1083信任终止，H9/D8。高Health不是trust clearance，合规措辞/师徒共担也不自动抹掉既有风险。
- v12：公开CI完成、恢复6次、处理埋雷1次并未形成稳定晋升或warning clearance；M18/M24 D绩效、raw771终局H7，工作延续危险必须独立于身体恢复处理。
- 高参考局clean Story负H次数：v6 19/112，v7o19/112，RUN07 22/112，RUN10 20/112，均48m。普通有界代价与高分可共存；样本不支持“每见H损失就保守”。RUN20终局H10却60.60，满资源不是收益目标。

WHEN_TO_OVERRIDE_GROWTH：公开急性身体信号/连续耗损且下一步成本、显式信任爆雷、连续低绩效、明确合规风险。比较当前合法恢复/降暴露选项并观察；无解除证据继续标记未解决。不恢复隐藏stock、不发明H阈值、不新造Risk Skill。存活局也有“近期风险”普通feed，泛化所有warning为停止成长不成立；不能将本报告风险正则proxy直接当runtime hard gate。

## Public score driver decomposition

| run | Level | Wealth | Resilience | Skill | Risk control | Network |
| --- | --- | --- | --- | --- | --- | --- |
| v6 | 18.0 | 9.88 | 12.75 | 15.0 | 10.0 | 9.67 |
| v7o | 15.0 | 10.75 | 14.25 | 15.0 | 8.0 | 8.83 |
| RUN07 | 15.0 | 8.78 | 15.0 | 14.88 | 10.0 | 9.0 |
| RUN08 | 12.0 | 7.25 | 13.5 | 10.25 | 10.0 | 6.0 |
| RUN10 | 15.0 | 8.03 | 13.5 | 14.38 | 9.0 | 8.5 |
| RUN17 | 6.0 | 0.55 | 7.5 | 1.25 | 8.0 | 1.17 |
| RUN19 | 12.0 | 2.88 | 12.75 | 6.12 | 0.0 | 4.33 |
| RUN20 | 12.0 | 7.35 | 15.0 | 10.25 | 10.0 | 6.0 |
| v12RUN01 | 3.0 | 2.02 | 9.0 | 1.12 | 8.0 | 0.33 |

仅使用公开 ending_score.dimensions 的 weighted_score，拒绝读取 risk raw_value 或反推stock/完整公式。分项按回包已舍入，和final可能差0.01；RUN21无终局分项。v6相对v7o的L6分项+3；财富/韧性较低、风险/人脉较高，终局差3.46不能全归L6。RUN07比RUN08多13.65，其中Level+3、Skill+4.63、Network+3、Wealth+1.53、Resilience+1.5，Risk相同，支持综合资本而非只保Health；RUN19 Riskcontrol0、H9仍淘汰。这里只分解公开点数，不恢复隐藏评分函数、饱和界或稳定80+保证。

## 敏感性、confounding 与证据等级

执行逐run排除的描述敏感性（JSON含10行）：移除任一run，剩余高参考完整局仍全部M6晋升、低参考仍M6不晋升；这是按终局选组的关联，含候选/事件/历史混杂。汇报O增益率LOO范围 0.748–0.7883；若去掉v6，L5→L6 positive=0，降为INSUFFICIENT_EVIDENCE。

没有训练logistic/tree：仅10条轨迹、64个相互依赖Review、L6仅1positive；回归会把共享窗口/历史当独立样本并放大精度。重复family的fresh局部响应可支持兑现折价；同context异选择只支持候选假设；cross-run/final相关最弱。短语标签覆盖不足、后续菜单展示异步结果、策略内生选择、幸存者偏差和right-censoring均未解决。

## 一个 Candidate recommendation 与 Main Return

**唯一首选 Option A**：以当前main冻结v8a为下一开发基线，恢复v6/v7o/v8a的promotion-first ownership + broad growth +本局响应折价优先级，以P01–P10短Playbook替代复杂策略理由协议。

保留：Single Agent唯一提交者、当前合法菜单、fresh-observe/action配对、public evidence firewall、必要的bounded风险检查/最终核对。建议删减：强制多board/certificate/marker推理、固定Energy组合、以full Brief/checkpoint改写为每步策略前提；这些是待Main审查的简化范围，不证明删除某组件会涨分，也不改本任务冻结审计合同。新增规则严格就是P01–P10，不新增Skill/Memory/Team/Swarm；不沿v11/v12默认演进。最小策略核是“最近窗口可兑现成果 + 广义资本 + realized局部折价 + 显式危险覆盖”，并非再设计架构。

本任务没有Candidate/Skill/manifest/Runner/依赖/runtime写入；live/provider/service/game=0。S10 Stage仍ACTIVE；Main尚未接受新策略或授权下一game；`READY_FOR_EMPIRICAL_POLICY_GATE / NEXT_GAME=NOT_AUTHORIZED`。

## TASK_RESULT / 验证与证据留存

- Required artifacts：本报告、短Playbook（10rules：HIGH3/MEDIUM6/LOW1）、compact JSON；另交付显式路径可复用builder及targeted test。
- 最强三条可直接执行依据：P01精确fresh边界、P02局部NO_GAIN折价且重评、P07按兑现与真实成本分配Energy。政策收益仍未live验证。
- Local-only dataset：`.local/scratch/s10-04/dataset/{policy_transitions.jsonl,promotion_frontiers.jsonl,dataset_summary.json}`，路径/bytes/hash在JSON。source manifest/intake/临时analysis在同scratch；raw唯一来源保留原runtime/artifacts位置，不移入scratch。scratch仅可重建派生物，不代替raw。
- 所有原run FORENSIC_HOLD保留，owner原任务/Main，解除NONE；未归档raw、未删除、未清理shared状态。失败/partial/v12收尾证据保留原职责。
- Verification PASS：8个targeted parser tests（0.07s）；第二次显式source重建byte-for-byte一致；64Review/1,626转移身份、顺序、去重、partial边界contract check；selected delivery secret scan。git diff --check及commit/push/clean tree回执返回本对话；未做live或因果测试。
- 非声称：未恢复隐藏公式/stock，未保证稳定分数、未做Test lookup、未证明causal optimal policy；不接受Stage COMPLETE。

复建命令（本机显式已核验manifest）：`D:/CS/CareerSim/.venv/Scripts/python.exe -m scripts.build_policy_transition_dataset --sources .local/scratch/s10-04/sources.json --output-dir .local/scratch/s10-04/dataset`。从项目根执行，输出仅为可重建离线派生物。
