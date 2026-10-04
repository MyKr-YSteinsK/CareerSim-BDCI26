# S10-12｜v6d Promotion Portfolio 单局完整验证

> IN_FLIGHT_EVIDENCE；本分支记录一局，不代表 Main 接受或稳定表现。

## Decision / Identity

**Status: COMPLETE_FOR_MAIN_REVIEW. Classification: V6D_NEAR_TARGET. Decision: V6D_NEAR_TARGET_COMPETITIVE.**

FACT：精确 v6d 自然完成 48 月，quantitative **71.67**、competition partial **50.17**、grade **A**、final **L5**。未达到 75。晋升 M6/M12/M24/M42；early chain **2/3**，M18 未晋升，与 v6c 晋升时间完全相同。行为和 M18 成长较 v6c 改善，尚不构成晋升链恢复。

INFERENCE：H_PORTFOLIO 的行为变化得到支持：report 增加、Network 实际进入比较和选择、intensive 消失。分数回到竞争区间，但无晋升加速，flat 后 reroute 不可靠；不能把 +7.41 分归因为该 patch。Main 下一步先分析剩余 gap，不立即 patch；所有 live 预算已消耗。

| Identity | Value |
|---|---|
| Branch | `codex/s10-12-v6d-run01`，未 merge main |
| Accepted/source commit | `e7e8ab44dd85a29135eb089ef29de8fed298f4a4` |
| Parent | `candidate-v6c-compliance-cleanup` / `e5363c9b4958955e02f5f895cb1ba1c794215958` |
| Candidate | `candidate-v6d-promotion-portfolio-rebalance` |
| Manifest SHA-256 | `4a92d56f41b63863a01793f5a38de99bd86ce3f1792542b9f92742c1d99c04b2` |
| Instruction SHA-256 | `a891fa103f0d4f910c9bbcc5ab91ab8bbbfe4cb242b9506d63374f1cf75d8074` |
| Planning / Risk / Board blob | `d86a53c5fffb75bd8d413dd0c05be9de10caa5ad` / `ab20843eadad675dbf7aa8be0178fb52a3791208` / `b6d371d74f3477f4f6cdeabe8482093a78cbe3e5` |
| Runner | `f61c738c72e51b77298cc1c14c7c6ebf4b6c527d` |
| Session | `fa51e5aa04554269a5dd608ac40eb0bf` |
| Result commit / Remote / Working tree | 包含本报告的单一交付 commit；最终 TASK_RESULT 记录实际 SHA、remote 和 clean 状态，避免自引用 commit hash |

## Operational / Live Budget

Exact source 与 clean tree、三 Skills、offline submission contract、全部冻结 hashes/依赖版本已通过。仅 process-local PATH prepend；`shutil.which` 正确；恰好一次 bare `jiuwenswarm-start --list` exit 0。预检无竞争服务/对局，19092/20000/20001/6173 可用。仅一次既有 non-generative balance GET：available，CNY 5.09；是否足够全局成本当时 UNKNOWN，无 completion probe。

| install | service lifecycle | Runner play | fresh game | replacement | intervention / manual / injection / patch / completion probe |
|---|---|---|---|---|---|
| 1 | 1 | 1 | 1 | 0 | 全部 0 |

Root serial checkout，未创建 worktree。一次安装包位于 `D:/CS/CareerSim/.local/scratch/s10-12-v6d-run01/submission`，四文件（manifest + 3 Skills），安装后 byte identity 核验通过。Runner 08:32:11.001599Z 至 08:52:59.980455Z；exit 0。一次 graceful stop exit 0，08:53:04.474555Z cleanup；四端口释放，manager PID 文件消失。service wrapper exit 1 是停止后的包装进程返回，不是游戏技术失败。

## Review trajectory / Early promotion

以下取正式 Review 第一个 fresh post-state；不是季度 Energy 后或月末状态。完整 public feedback、pre/post、动作和后续 Planning response 在 compact JSON `reviews`，UNKNOWN 不补推断。

| Review | grade | Level pre→post | promotion | S/N/O/W/H/D | 后续 Primary Gap / Risk Budget |
|---|---|---|---|---|---|
| M6 | C | L1→L2 | YES | 9/3/3/2/7/10 | win-visibility / TIGHT |
| M12 | B | L2→L3 | YES | 21/4/5/4/10/9 | win-visibility / TIGHT |
| M18 | B | L3→L3 | NO | 39/17/15/8/10/10 | win-visibility / TIGHT |
| M24 | B | L3→L4 | YES | 42/19/15/11/10/10 | win-visibility / UNKNOWN |
| M30 | B | L4→L4 | NO | 62/25/21/15/8/10 | win-visibility / TIGHT |
| M36 | A | L4→L4 | NO | 76/36/24/26/10/10 | win-visibility / AVAILABLE |
| M42 | A | L4→L5 | YES | 94/34/26/32/10/10 | win-visibility / UNKNOWN |
| M48 | B | L5→L5 | NO | 111/54/33/38/10/10 | win-visibility / TIGHT |

M6：反馈“只会忙、不会赢”，visibility 成为 primary；M12：观察名单/更清晰成果，Network 下跌后提到重建关系。M18：整体达标、亮点不足，明确重查 S/N/O，但仍回到 visibility，HR 严重 warning 后 cleanup。M24 晋升后 Network 21→14 的公开下跌成为 secondary concern。M30/M36/M48 no-advance 后多为 reaffirm visibility，没有持续完成窗口资本复利的重诊断。M36 虽 A 仍未晋升；不能由 public S/N/O 推断晋升阈值。

## Quarterly Energy / Portfolio

41 次实际 Energy：**report 19 / Network 5 / intensive 0 / Health 10 / cleanup 7 / Skill 0 / psychological 0 / other 0**。每次 pre-state、cost、单个选择、fresh post-state、S/N/O/H local change 和 rationale witness 在 `Energy_sequence`。report cost=1，intensive cost=2；剩余 Energy=1 时 intensive 不可负担。下表顺序是实际发生的序列，不是 batch 授权。

| Actual month/quarter | 实际逐步动作 | checkpoint / Risk | Planning witness 摘要 |
|---|---|---|---|
| M3 / Q1 | 人脉维护 → 准备汇报材料 → 健康恢复 | BROAD / AVAILABLE | Skill已经较高；Network/Output均比较，并补Health；成本比较明确，但预先列整季计划。 |
| M6 / Q2 | 处理历史埋雷 → 准备汇报材料 | BROAD / TIGHT | Network骤降被反复比较；正式反馈强调可见成果，cleanup占2E后选report。 |
| M9 / Q3 | 准备汇报材料 → 人脉维护 → 健康恢复 | BROAD / UNKNOWN | Skill/Network/Output比较；budget表述介于AVAILABLE/TIGHT，避免加重风险；report→Network→Health。 |
| M12 / Q4 | 处理历史埋雷 → 准备汇报材料 | BROAD / TIGHT | 讨论Network已回升与Health满；formal feedback需要更清晰成果，选cleanup/report。 |
| M15 / Q5 | 处理历史埋雷 → 准备汇报材料 | BROAD / TIGHT | S/N/O增长被重查，Network/Health替代进入比较；风险提示使cleanup优先。 |
| M18 / Q6 | 处理历史埋雷 → 准备汇报材料 | BROAD / TIGHT | no-advance重查S/N/O，反馈亮点不突出，严重HR提示支持cleanup；未形成可靠response优先。 |
| M21 / Q7 | 处理历史埋雷 → 准备汇报材料 | PRIMARY_ONLY / AVAILABLE | 沿用cleanup/report：Output仍是gap；N/S只列状态，未比近期欠积累或fresh report flat。 |
| M24 / Q8 | 处理历史埋雷 → 人脉维护 | BROAD / AVAILABLE | Network21→14持续下滑，明确secondary concern，cleanup+Network，Main兼补S/N/O。 |
| M27 / Q9 | 健康恢复 → 健康恢复 → 准备汇报材料 | BROAD / TIGHT | Health下行约束；Network/Output进入剩余1E比较，恢复两次后选report。 |
| M30 / Q10 | 健康恢复 → 准备汇报材料 → 准备汇报材料 | BROAD / TIGHT | Network与重复report比较，Skill成本也被评估；先Health后report两次。 |
| M33 / Q11 | 健康恢复 → 健康恢复 → 准备汇报材料 | BROAD / TIGHT | Health6约束；比较Health+report+Network组合，选择两次恢复；report flat未确认。 |
| M36 / Q12 | 准备汇报材料 → 准备汇报材料 → 人脉维护 | BROAD / AVAILABLE | 比较S/N/O成本与关系反馈；认真讨论intensive，但因成本/风险提示选择report两次+Network。 |
| M39 / Q13 | 健康恢复 → 准备汇报材料 → 准备汇报材料 | BROAD / AVAILABLE | Network与report/Health组合反复比較，虽无binding Health trend仍做预防恢复。 |
| M42 / Q14 | 准备汇报材料 → 准备汇报材料 → 人脉维护 | BROAD / AVAILABLE | 新Level；report vs intensive成本比较，Network进入并被选择。 |
| M45 / Q15 | 健康恢复 → 健康恢复 → 准备汇报材料 | PRIMARY_ONLY / TIGHT | Health趋势与Output价值比较；S/N列状态，没有其它progression资产比较。 |
| M48 / Q16 | 处理历史埋雷 → 准备汇报材料 | BROAD / TIGHT | cleanup/report/Health/Network都比较；late horizon需当下兑现，但误称此前M46已执行本季度Energy。 |

BROAD **14/16**，PRIMARY_ONLY **2/16**（M21/M45），UNKNOWN 0。BROAD 仅表示多个相关成长资产被实际讨论，不等于每次都完整考虑六个维度、fresh response 或成功 rerank。M3 尚无正式 Review feedback；不能伪造考虑了未发生的反馈。

## Portfolio mechanisms

| Mechanism | Verdict | Evidence / Limit |
|---|---|---|
| Network inclusion | PASS_WITH_LIMITATIONS | M3/M9/M24/M36/M42 实际选择；M12 重建 concern，M24 显式 secondary Network（transcript 3450–3503）。5 次维护只有 M24/M42 clean Network GAIN，其余 FLAT；不推永久 cap。不因未选择 Network 就判失败。 |
| Report vs intensive efficiency | PASS_WITH_LIMITATIONS | 多窗口明确比较 report 低成本及 intensive Health 成本；M3/6/9/12/15/18/36/42/48 有显式比较，其余部分 UNKNOWN 或 intensive 已不可负担。没有 UNJUSTIFIED_INTENSITY 实际提交，但零 intensive 不能证明所有强机会都会保留它。 |
| Intensive independent value | NOT_EXERCISED | 本局没有选择 high-intensity；合法路线未由操作方禁用。 |
| Output-flat rerouting | FAIL | report clean flat M9/M18/M21/M33。M9 后 Network/Health 为 PASS_WITH_LIMITATIONS（原先已计划，非显式 flat-discount）；其余三个 FAIL。M18→M21 同级 O16 下继续 report，没有 fresh flat 折价或独立价值解释。 |
| no-advance reset | PASS_WITH_LIMITATIONS | M18 重查 S/N/O；后续多 reaffirm visibility，primary 几乎一直 win-visibility。未形成固定 ratio 或最低值补齐，但重置不充分。 |
| Main key-project | PASS_WITH_LIMITATIONS | 16/16 关键项目，保留 conditional prior；无明确 blocked Main project 后仍僵持的独立 witness。跨月结果 MIXED，不能从菜单收益当成已实现 gain。 |
| Survival constraint | PASS_WITH_LIMITATIONS | TIGHT Health 场景恢复，cleanup 7 次，M41 心悸即刻休息/必要就医；M2 confidential hint 识别后 WARN 仍选模糊建议，随后被查，风险评价有争议。 |
| broad checkpoint | PASS_WITH_LIMITATIONS | 14 BROAD，但常提前写整季 bundle 并“continue plan”；实际逐次 fresh observe 合格不等于 fresh response 后重新排序。 |

不把动作前 forecast “O+1”当成动作后虚报 GAIN。7 次 cleanup 的公开 S/N/O/H flat 不证明 cleanup 无效，更不猜 hidden stock。T2686 出现“higher thresholds / Output binding”推测，记录为 unsupported speculation，没有得到数值晋升公式或转移为策略。

## Survival / public exposure

已逐项检查全部 144 Story 描述；compact `survival` 收录 74 个 material exposure/delivery/Health context、全部 20 个动作前后 Health decline、9 个明确累积/严重 HR warning，以及候选、Risk gate、fresh next-state。精确 contemporaneous Risk Budget 不足处标 UNKNOWN，不移植同季度预算。普通 mild cost 不自动 veto。

M2 对未官宣调整的模糊建议并非完全没识别危险；模型讨论保密、最终 WARN，之后 M3 泄露排查/严重 HR 提醒，是 contested risk assessment。M10 接连续 on-call、M13 生产故障/追责、M22 confidential meeting、M24/25 安全上报与关系损失、M28 发布未测代码/健康警示、M30 离职资料拒收、M32 未测 rollback 推迟、M38 减负治疗、M41 身体明确报警、M43/44 纠正汇报口径、M48 正规合规举报均保留公开上下文。未发现不可负担动作；TIGHT 时避免 intensive 的分支实际通过，但 intense 强机会分支未被检验。清理后的表扬不是隐性风险已清除证据。

## Runtime correctness — separate from strategy outcome

202 attempts=202 successful mutations；203 observe；**202/202 action→fresh observe**（下一动作前），same session 202/202，CTRL exact pairing 202/202；Energy single integer 41/41，Energy/Main affordability 57/57；tool/schema errors 0，unknown mutation 0，whole game persistence PASS。最终 observe 行政时钟 M49、alive=false/failed=true 对应 `completed=true / outcome=completed / survival_months=48`，不是提前淘汰。

**DecisionClosed FAIL**：transcript 24–44、218–266、5001–5062，最终 Risk gate 后反复重开 deliberation。**Compression recovery FAIL**：两次 actual compressor，08:42:08.362010Z（M18）和 08:52:12.779463Z（M48），之后均 fresh observe 再 action，但没有重新读取三 Skills（0 rereads）。stale snapshot 作为策略权威 UNKNOWN。泛用 parser 的 4 compressor records 是两个 ChatCompletion 在 receipt/before-parse 重复记录，实际 unique calls=2。

**Public clock consistency FAIL**：M21–M45 的 9 个 quarterly windows 显示月份/季度多一格；如 actual M21/Q7 写 M22/Q8。canonical 仅用 fresh observe 的实际时钟。与压缩时间相邻不足以证明因果。Energy rerank semantics FAIL_WITH_LIMITATIONS，不能用正确 integer calls 掩盖固定 preplan。泛用 Delivery/DL audit NOT_APPLICABLE：冻结 v6d 三 Skills 并无 DL 合同。数字 hidden-risk text matches 多为公开菜单 advertised effect 算术，不证明读取 hidden stock；compact 不导出 hidden 数值。

这些控制缺陷单独记录，未使实际单局结果失效。观察 parser 一次 pre-output AssertionError 后恢复，从未停止/干预 Runner 或 service；无 replacement/rescue。

## Historical comparison

| Candidate/run | score / months / grade / final Level | promotions | report / Network / intensive / Health / cleanup |
|---|---|---|---|
| v6d Run01 | 71.67 / 48 / A / L5 | 6/12/24/42 | 19/5/0/10/7 |
| v6c S10-10 | 64.26 / 48 / B / L5 | 6/12/24/42 | 10/2/10/12/2 |
| v6 | 75.29 / 48 / A / L6 | 6/12/18/36/48 | 15/8/5/10/2；另 psychological 1 |
| v1 high | 76.04 / 48 / A / L6 | 6/12/18/36/48 | 25/6/无主要 intensive 路径/11/3 |
| v7o | 71.83 / 48 / A / L5 | 6/12/18/36 | 次级参考；不从最终分数推机制 |
| v8a RUN07 | 72.65 / 48 / A / L5 | 6/12/24/42 | 次级参考；不从最终分数推机制 |

| First Review post-state | v6d S/N/O/H | v6c S/N/O/H | delta v6d−v6c |
|---|---|---|---|
| M6 | 9/3/3/7 | 9/3/3/5 | 0/0/0/+2 |
| M12 | 21/4/5/10 | 21/4/6/6 | 0/0/−1/+4 |
| M18 | 39/17/15/10 | 33/13/10/7 | +6/+4/+5/+3 |

FACT：与 v6c 同存活、同 L5、同四次晋升；+7.41 分。Network consideration/report efficiency 更明显，Output clean flat 4 次（v6c 6 次）仍有重复。末局 v6d S114/N54/O34/H8/W39/D10，对 v6c S129/N50/O38/H5/W25/D9：Network/Health/Wealth 较高、Skill/Output 较低；不能只用 M18 改善解释总分。

High donors 的 early chain 都是 3/3。S10-11 accepted donor report 的 v6 first-Review M6 9/3/3/4、M12 20/4/5/6、M18 37/16/14/10；v6d M18 S/N/O 略高却仍未晋升，再次反对固定数值公式。v1 接受摘要的 M6 13/5/6/7、M12 24/7/7/7、M18 44/19/16/10 是月末 timing，不能与 first-Review 混算 delta。v6d 的 Energy 家族方向接近 donor 广义组合，但没有 donor 晋升链，也未证明保持有独立价值的 intensive 选择能力。

Sources：本局 `reviews / Energy_sequence / quarterly_checkpoints / Main_actions / flat_response_audit / survival / runtime`；历史数值来自 [S10-11 accepted donor analysis](../research/S10-11_HIGH_SCORE_DONOR_PORTFOLIO.md) 及本地保留 S10-10 compact public evidence。只作 historical stochastic comparison，Story/exposure 不受控。H_PORTFOLIO 行为证据增强，充分性、因果收益和稳定分数仍 UNKNOWN。

## Usage / Preservation / Verification

Runner usage：input **40,813,190** / output **154,661** / total **40,967,851**；cache **40,406,528**，hit **99.0%**。requested/usage aggregate model `deepseek-flash`。wall **1248.978856s（20m48.98s）**。actual compressor calls **2**；独立 compression receipt input/output/cache 分别 160896/3380/159104 与 155146/3204/153344，不与 Runner aggregate 未核实地相加。provider-reported cost=0.0；**actual billed cost UNKNOWN**。

Candidate 五个 source 文件、installed 三 Skills/manifest、instruction、Runner 27 source + dependency 2 files、provider/config/retry、fallback 均未改。依赖版本 career-emulator 1.0.1 / bdci26 1.0.0 / jiuwenswarm 0.2.4b3 / openjiuwen 0.1.16.post2；provider config SHA `5ae22dedc828177df114e500aacf280a17217b45d3d19d9df67b583b7bd08b72`。Candidate validation flags 保持原值，不在 live 中写身份。未新增 Skill/Memory/Team 或策略 intervention。

Offline targeted validation 检查 8 Review、16 checkpoints、41 Energy、16 Main、202 pairing、public state/delta、冻结 identity；JSON parse、exact three-file scope、git diff --check、secret scan PASS。最终 commit/push/clean 状态由交付 TASK_RESULT 核实；未运行第二局、provider probe、额外 service lifecycle。

**FORENSIC_HOLD ACTIVE**：本局 raw 留在 `D:/CS/CareerSim/.career_sim_runner/career_emu/outputs/local-s06-adaptive-controller/20261004T083214Z/`；preflight、launcher receipt、scoped llm window 与 offline public extraction 留在 `D:/CS/CareerSim/.local/runtime/s10-12-v6d-run01/`。最小 12 文件路径、bytes、SHA-256 在 JSON `FORENSIC_HOLD.files`。原因：v6d/v6c 比较、M18/M21 flat/M2 risk 争议、compression/clock attribution。owner S10-12，release authority Main/Stage；接受独立 compact review 并解除比较/复验依赖后，另需显式 cleanup 授权，hash/COMPLETE 不解除 hold。无 raw logs/shared DB/config/credentials 提交。

## Non-Claims / Return

一局不证明 stable75+；本局未达 75，没有 80+ 证明、因果晋升公式、hidden-test transfer 证明。没有根据历史频率强迫动作，没有在 poor interim trajectory 后救场。

**RETURN_FOR_V6D_GAME_GATE**

**NEXT_GAME=NOT_AUTHORIZED**
