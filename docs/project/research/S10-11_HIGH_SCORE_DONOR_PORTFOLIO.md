# S10-11｜High-score donor promotion portfolio

Evidence status: IN_FLIGHT_EVIDENCE。OFFLINE FORENSICS；本任务无 service / Provider / game / install / MCP 调用。所有月份、频率、数值只在离线报告，不进入 runtime 策略。

## Sources and limits

- v1 high：Git `8a93378a8d9ef5598e925048db39ee931e207bab:experiments/S04-04-high-score-confirmation/candidate_run1_trajectory.json`，其中 source_run=S04-03 Candidate Run #1。accepted Tier B 摘要；monthly_public_state 是月末最后观察，quarterly_decisions.state_before 是首 Energy 前；不能从摘要证明逐动作 clean response 或完整合法菜单。
- v6 / v7o / v8a RUN07：Git `4f54967e5d8b3f6fd82c0a9ceeab94ca525e8d4a:docs/project/research/S10_POLICY_MINING_SUMMARY.json` 与 `docs/project/reviews/S09-13_HIGH_SCORE_STRATEGY_EVIDENCE.json`；复用 S10-04 的 `.local/scratch/s10-04/dataset/policy_transitions.jsonl`。只读 accepted public transitions / first_review_state；不重新解码 dataset 或 hidden 数据。
- v6c：Git `69f26a4b0ddd0e9423c450f96690ce049af8e44e:docs/project/runs/v6c-revival-run01-evidence.json`；细化到首 Energy 及行动后 fresh response 时只读 `.local/runtime/s10-10-v6c-revival-run01/public-policy-data.json`（public allowlist）。以下行号指各局原 events 的 action 行，绝不作为 runtime answer lookup。
- Source snapshots / derived v6 transitions / 输入 bytes+SHA-256 记录于 `.local/runtime/s10-11-v6d/`；原 FORENSIC_HOLD 未解除、未删 raw。canonical Git 摘要可恢复；v1 raw 缺失边界不因新 hash 被消除。
- 同月同 Level fresh action→observe 可支持 LOCAL response 描述，仍不能完全排除 delayed Story effects；Review 边界是 MIXED，不归因某个 Energy 动作。任何后验 response 只供离线检查，不能倒灌到此前的决策。

## FACT｜Outcome / progression / action mix

| Run | Score / months / grade / final Level | Promotions | Main mix | Energy family mix（动作次数，不是 Energy 单位） |
|---|---|---|---|---|
| v1 high | 76.04 / 48 / A / L6 | M6/12/18/36/48 | 关键项目16 | report25 / Health11 / Network6 / cleanup3 |
| v6 | 75.29 / 48 / A / L6 | M6/12/18/36/48 | 关键项目14 / 低调避险2 | report15 / Health10 / Network8 / intensive5 / cleanup2 / psychological1 |
| v7o | 71.83 / 48 / A / L5 | M6/12/18/36 | 关键项目10 / 导师4 / 轮岗2 | report20 / Health12 / Network8 / Skill4 |
| v8a RUN07 | 72.65 / 48 / A / L5 | M6/12/24/42 | 关键项目12 / 领导汇报1 / 导师1 / 避险1 / 轮岗1 | report20 / Health9 / Network7 / cleanup5 / Skill1 |
| v6c | 64.26 / 48 / B / L5 | M6/12/24/42 | 关键项目16 | report10 / Health12 / Network2 / intensive10 / cleanup2 |

FACT：v1 accepted 摘要的45个 Energy 动作中无 intensive 主路径；不是 raw 完整核验所得的禁用规则。v7o 和 RUN07 有更广组合仍低于75，故 breadth 不是75+充分条件。

## FACT｜Early public accumulation（严格标明时点）

| Run / moment | M6 S/N/O/H | M12 S/N/O/H | M18 S/N/O/H |
|---|---|---|---|
| v1 月末最后观察 | 13/5/6/7 | 24/7/7/7 | 44/19/16/10 |
| v6 first formal Review post | 9/3/3/4 | 20/4/5/6 | 37/16/14/10 |
| v6c first formal Review post | 9/3/3/5 | 21/4/6/6 | 33/13/10/7 |

FACT：Task 所列 v6 M6≈11/3/5、M12=23/8/7、M18=38/19/17 属于季度 Energy 周边状态，不能与 v6c first Review post 无标签混比。v1 M24 月末63/36/26/H8 亦为月末摘要。v6c M18 首次未晋升；formal feedback 为整体达标、亮点不突出，并有近期轻微风险提示。其 first Review 的33/13/10与 v6 的37/16/14均比同月后续 Energy 状态更早。

INFERENCE：v6c 的 Network Energy 投资显著少，report 较少而 intensive 较多；M18 broad public accumulation 与两条高分轨迹方向不同。Health recovery 12次并不能解释为当前主要 drift，也不能据此调整 survival policy。

HYPOTHESIS H_PORTFOLIO：反复将 Output 当单一 primary objective，可能挤掉 Network / visibility 与其它可响应资产、消耗更多恢复资源，削弱 progression compounding。尚未证明这种分配造成64.26或 M18 no-advance。

## FACT｜Accepted local response prior（只离线）

S10-04 clean/local 同月同 Level 样本：report=109 GAIN /33 NO_GAIN；Network=40/16；Health=85/2；intensive Output=13/17 GAIN，Health decline=17/17。当前菜单中 report/Network/Health 通常成本1、intensive成本2；费用仍须每次 fresh 合法菜单确认。收益与成本描述不构成晋升公式、动作成功概率或未来保证，runtime 仅保留定性比较原则。

## Semantic replay｜6 donor snapshots

下面检查“新文本能支持什么 decision principle”，不是实际重新执行模型，更不是回写历史。v1 的动作顺序只有 summary 证据，局部响应与完整菜单 UNKNOWN；不因此假装存在 fresh GAIN。

| Snapshot | Fresh public basis / factual historical actions | v6d decision principle / semantic verdict |
|---|---|---|
| v1 M3（首 Energy 前摘要） | L1 S9/N3/O2/H4；人脉维护→准备汇报材料→健康恢复；Main关键项目 | Network 与 Output 可同时成为比较对象；Health4且既有下降线索支持 recovery。Network→report→recovery 不是固定 bundle；每步仍需 fresh observe。关键项目 prior 保留。 PASS |
| v1 M6（首 Energy 前摘要） | L2 S13/N5/O6/H3；健康恢复→准备汇报材料→健康恢复；Main关键项目 | H3 / 公开绩效C及需要更清晰 Output 的反馈支持先保护 buffer；不为补 Network 覆盖 survival。Level 改变令旧 response 不直接迁移，report 未知仍可比较。 PASS |
| v1 M12（首 Energy 前摘要） | L3 S24/N7/O6/H3；健康恢复→健康恢复→准备汇报材料；Main关键项目 | H3且新 Level；保持原 Health boundary，buffer 恢复后比较当前 visibility 与 Network，不设次数/最低值。 PASS |
| v6 M6（首 Energy 前） | L2 S11/N3/O5/H4；line221 健康恢复 ΔO=0,N=0,H=2；line229 处理历史埋雷 ΔO=0,N=0,H=0 | H4恢复有公开贡献；随后心理修复的目标维度 flat 不能伪装成长。Level 重建后评估其它合法路线；不因 Network 数字小自动替换恢复。 PASS |
| v6 M12（首 Energy 前） | L3 S23/N7/O5/H6；line421 高强度工作 ΔO=2,N=0,H=-1；line429 人脉维护 ΔO=0,N=1,H=0 | intensive O+2/H−1 为明确结果路径、仍允许；剩余 Network +1 显示组合能并存。report UNKNOWN只提供低成本 prior，不能保证它能替代同样产出。 PASS |
| v6 M18（首 Energy 前） | L4 S38/N19/O14/H10；line625 高强度工作 ΔO=2,N=0,H=-1；line633 准备汇报材料 ΔO=1,N=0,H=0 | intensive O+2/H−1 后 report O+1/H不变；允许有 result need 的 intensive，并比较接续低成本可见成果。不把本局成功次数写成配额。 PASS |

## Semantic replay｜9 v6c snapshots

以下所有窗口当前菜单均公开提供 report / intensive / Network / recovery 等合法路径；Network 是否有效仍必须由当前同局 response 判定。先陈列已发生的局部反馈，再讨论反馈后或后续 checkpoint 的原则；**不得把当步 post 当作当步 pre 的已知事实**。Risk Budget 未直接从状态数值定为 TIGHT；表中的 recovery 判断需结合相邻公开趋势/反馈。

| Snapshot | First Energy fresh state / subsequent local response | v6d decision principle / semantic verdict |
|---|---|---|
| v6c M3 | L1 S6/N3/O1/H4；line105 准备汇报材料 ΔO=1,N=0,H=0；line113 人脉维护 ΔO=0,N=0,H=0；line121 健康恢复 ΔO=0,N=0,H=2 | report O+1后 Network 当前 N flat；该局并非完全未试 Network。保留 Health恢复与关键项目；一次 Network flat 不等于永久 cap。 PASS |
| v6c M6 | L2 S12/N4/O5/H5；line209 准备汇报材料 ΔO=1,N=0,H=0；line217 准备汇报材料 ΔO=0,N=0,H=0；line225 健康恢复 ΔO=0,N=0,H=2 | 新 L2 重置旧 Level 的 response 比较；report 首次GAIN、第二次flat后重比 Network/其它 responsive route 或当前恢复价值，不继续无证据重复追 Output。 PASS |
| v6c M9 | L2 S21/N7/O6/H4；line313 健康恢复 ΔO=0,N=0,H=2；line321 健康恢复 ΔO=0,N=0,H=2；line329 准备汇报材料 ΔO=0,N=0,H=0 | H恢复4→6→8后重新扫描；report O flat 后考虑可兑现异类路径。旧 L2 Network flat降低同条件重复价值，不能永久放弃跨条件 Network。 PASS |
| v6c M18 | L3 S35/N11/O11/H7；line617 处理历史埋雷 ΔO=0,N=0,H=0；line625 准备汇报材料 ΔO=1,N=0,H=0 | no-advance 重查S/N/O与窗口而非默认Output；Network纳入比较。近期风险提示可支持cleanup，未证明应被替换；cleanup可见维度flat不证明风险清理无效，剩余report有GAIN。 PASS |
| v6c M21 | L3 S39/N20/O16/H7；line713 高强度工作 ΔO=0,N=0,H=-1；line721 健康恢复 ΔO=0,N=0,H=2 | intensive O flat /H−1后不可称已得Output收益；先fresh扫描恢复需要，再比较Network、report或其它可兑现路线。单次flat不定cap。 PASS |
| v6c M33 | L4 S72/N36/O26/H7；line1097 高强度工作 ΔO=0,N=0,H=-1；line1105 健康恢复 ΔO=0,N=0,H=2 | intensive O flat /H−1后discount重复投入，恢复仍有效；新组合重查Network/visibility，不能反复只写Output且宣称GAIN。 PASS |
| v6c M36 | L4 S81/N36/O26/H10；line1193 高强度工作 ΔO=0,N=0,H=-1；line1201 准备汇报材料 ΔO=0,N=0,H=0 | A但no-advance需重查组合；intensive与report都O flat，须比较响应的其它资产/交付约束。report D+1不是Output GAIN，独立visibility价值须公开依据；不推断永久cap。 PASS |
| v6c M42 | L5 S106/N35/O25/H6；line1385 高强度工作 ΔO=2,N=0,H=-1；line1393 健康恢复 ΔO=0,N=0,H=2 | 晋升到L5令L4 response不可直接迁移。intensive O+2是正响应，但report/Network仍需比较；既有Health负担及当步H−1支持重新评估buffer。不得永久禁止intensive。 PASS |
| v6c M48 | L5 S128/N49/O37/H4；line1577 健康恢复 ΔO=0,N=0,H=2；line1585 高强度工作 ΔO=1,N=0,H=-1 | H4恢复到6有效；当期intensive O+1/H−1仍可在非TIGHT且有兑现价值时选择，但需比较材料/recognition和资源成本。终局窗口不追无法兑现的长期Skill，48m后的未知机会不计收益。 PASS |

## INFERENCE / rejected explanations

共同高分模式：关键项目 strong prior、可见成果与人脉积累、仍响应的局部路线、公开生存 buffer；这是可检验的策略 prior，不是固定组合或因果规律。

- 拒绝“关键项目16/16导致低分”：v1同样16/16却76.04；现有证据不支持修 Main 频率。
- 拒绝“高强度工作是坏动作”：v6使用5次；局部13/17有 Output gain，v6c晚期也再获增长。问题是当前价值相近时资源效率与机会成本。
- 拒绝“多投Network就一定晋升 / 输出达到某数值就晋升”：no controlled comparability，反馈、Story、Level和历史暴露混杂；Network最小值不是规则。
- 拒绝“某次flat就是cap”：S10-04有同局同Level report gain-after-flat 5、Network gain-after-flat 3；条件与Level变化必须重看。
- 拒绝“复制高分Health次数或固定Energy比例”：恢复由公开constraint支持；v7o、RUN07较广组合仍不足75，breadth非充分条件。

Return: READY_FOR_V6D_GAME_GATE（仅静态候选进入独立Game Gate review）。NEXT_GAME=NOT_AUTHORIZED。无 gameplay validation、75+ / stable75+ / hidden-test 证明，无 causal promotion formula。
