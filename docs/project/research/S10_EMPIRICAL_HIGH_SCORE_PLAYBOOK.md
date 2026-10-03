# S10 Empirical High Score Playbook

状态：`EMPIRICAL_HIGH_SCORE_POLICY_RECOMMENDATION`；开发研究建议，尚未部署或验证收益。仅使用本局当前公开状态、合法菜单及 fresh 回包。HIGH 表示相应证据/局部观察较可靠，不表示政策因果效益已证明。

## P01｜先取当前公开事实，再判断收益

- RULE：先取当前公开事实，再判断收益。
- WHEN：每次 action 后及 Review 前后。
- DO：用 fresh observe 更新当前 Level、资源、结果和警告；将 advertised 与 realized 分开。
- AVOID：把成功 receipt、月末值或未来 Review 当作已兑现收益。
- EVIDENCE：64 次 Review 均有精确 pre→trigger→first-result；126 Main 均混合跨月，不能当净收益；定位及分母见 [研究报告](S10_PROMOTION_FRONTIER_REPORT.md) 和 [汇总](S10_POLICY_MINING_SUMMARY.json)。
- CONFIDENCE：`HIGH`。反例/限制：边界可核验不代表回包能分离所有延迟事件效应。

## P02｜局部无增益就折价，条件改变才重评

- RULE：局部无增益就折价，条件改变才重评。
- WHEN：同 Level、同 recurring family 在可比资源/上下文下重复 NO_GAIN。
- DO：减少对该目标收益的权重，比较仍有响应的维度或一个有价值的未试路径；晋升/资源变化后重新观察。
- AVOID：把广告增益当保证、无限重复，或宣布永久隐藏上限。
- EVIDENCE：汇报材料 142 次：109 增益/33 平；同 run/Level 前次 O 平后，本次 9 平/5 增；v12 M3/6/15/18 四次 O3 平，M21 O2 又 +1；定位及分母见 [研究报告](S10_PROMOTION_FRONTIER_REPORT.md) 和 [汇总](S10_POLICY_MINING_SUMMARY.json)。
- CONFIDENCE：`HIGH`。反例/限制：局部平后可以恢复增益；未试路径的反事实收益未知。

## P03｜为最近 Review 争取可兑现成果

- RULE：为最近 Review 争取可兑现成果。
- WHEN：多方案竞争且交付窗口明确。
- DO：优先窗口内能完成、责任清楚、能公开确认的方案；同时检查质量、安全及依赖。
- AVOID：按标题固定选择开源，或只因长期资产听起来价值高就推迟兑现。
- EVIDENCE：RUN07/RUN08 完整公开 context/menu 相同：短交付→如期上线业务满意 vs 自研→延期；RUN19 自研延期仍 M6 晋升；定位及分母见 [研究报告](S10_PROMOTION_FRONTIER_REPORT.md) 和 [汇总](S10_POLICY_MINING_SUMMARY.json)。
- CONFIDENCE：`MEDIUM`。反例/限制：同 context 不同月份/状态/后续路径；不是随机对照，开源路径有 CVE 代价。

## P04｜把承诺、完成和认可分开

- RULE：把承诺、完成和认可分开。
- WHEN：任务推进、交付或获得表扬后。
- DO：只将明确上线/验收记为完成，将有具体成果对象的业务/客户认可记为强结果；继续验证阻碍。
- AVOID：把泛泛 HR 夸奖、PPT 汇报或一个 CI 上线当作晋升充分条件。
- EVIDENCE：v12 M5 CI 上线但 M6 不晋升；RUN20 M4 原型确认仍不晋升；v6/v7o M6 没匹配到强结果词仍晋升；定位及分母见 [研究报告](S10_PROMOTION_FRONTIER_REPORT.md) 和 [汇总](S10_POLICY_MINING_SUMMARY.json)。
- CONFIDENCE：`MEDIUM`。反例/限制：词法漏报和异步归因存在；结果标签不是 hidden state。

## P05｜晋升优先，同时积累 S/N/O/W

- RULE：晋升优先，同时积累 S/N/O/W。
- WHEN：有合法成长机会且无明确急性危险。
- DO：保持 ownership 和广义成长；缺口由当前 Review 反馈、公开资本和本局兑现反应共同判断。
- AVOID：只追一个 Output 值、只堆 Skill，或把样本范围写成硬阈值。
- EVIDENCE：L3 晋升 8/17，promoted N21/O13–16 与 non-promoted 有重叠；L5 唯一晋升 v6 O37，而未晋升 v7o O38；定位及分母见 [研究报告](S10_PROMOTION_FRONTIER_REPORT.md) 和 [汇总](S10_POLICY_MINING_SUMMARY.json)。
- CONFIDENCE：`MEDIUM`。反例/限制：S/N/O、任职期、机会及故事共变；没有恢复晋升公式。

## P06｜关键项目是条件性选择

- RULE：关键项目是条件性选择。
- WHEN：季度 Main 有项目与其它合法选项。
- DO：比较交付可行性、已有负荷、上轮结果与安全约束；有可兑现 ownership 时偏向项目，条件变差时重排。
- AVOID：Always key project，或因一次混合回包增长就归功项目。
- EVIDENCE：v6 项目14/16 得75.29；RUN08 16/16 得59；101 项目转移全部跨月；定位及分母见 [研究报告](S10_PROMOTION_FRONTIER_REPORT.md) 和 [汇总](S10_POLICY_MINING_SUMMARY.json)。
- CONFIDENCE：`MEDIUM`。反例/限制：其它 Main family 样本少且选择偏差大，无法证明最优替代。

## P07｜Energy 根据响应与真实代价分配

- RULE：Energy 根据响应与真实代价分配。
- WHEN：季度 Energy 菜单开放。
- DO：先保护明确紧急缺口，再比较目标维度的局部 realized 增益/体力/Health 代价；每步观察再选下一步。
- AVOID：预先固定整季组合，或在 O 平时仍付 Health 追广告收益。
- EVIDENCE：恢复 H 增益85/87；汇报 O109/142；人脉 N40/56；高强度 O13/17但 H17/17下降；学习 S6/6但 H6/6下降；定位及分母见 [研究报告](S10_PROMOTION_FRONTIER_REPORT.md) 和 [汇总](S10_POLICY_MINING_SUMMARY.json)。
- CONFIDENCE：`HIGH`。反例/限制：family 兑现率来自被选择样本；恢复平的2次、学习仅6次，不能当全局保证。

## P08｜明确急性危险覆盖成长

- RULE：明确急性危险覆盖成长。
- WHEN：出现血量骤降、身体急性信号、信任/绩效/合规警告持续升级。
- DO：重新比较当前合法保护/降暴露路径，检查下一回包；按具体警告处理，不只看 H；无法证明解除就保留待处理。
- AVOID：继续增负荷、以 H 很高或一次处理埋雷代替解除证据。
- EVIDENCE：RUN17 M6 H3→1→0 自然终止；RUN19 H9/D8 仍信任终止；v12 H7仍因连续D绩效终止；定位及分母见 [研究报告](S10_PROMOTION_FRONTIER_REPORT.md) 和 [汇总](S10_POLICY_MINING_SUMMARY.json)。
- CONFIDENCE：`MEDIUM`。反例/限制：未做保护方案对照，不能保证选择恢复即可救局，也无官方 H 阈值。

## P09｜普通成本可接受，不能全程避险

- RULE：普通成本可接受，不能全程避险。
- WHEN：无急性警告且成长方案代价有界。
- DO：比较普通成本与成长回报，留意累积趋势；保护稳定后回到成果与资本积累。
- AVOID：保持满 H 作为唯一目标，或把所有负 Health 选项都拒绝。
- EVIDENCE：四条高参考局 clean Story 负H分别19/19/22/20次，均48m；RUN20 H10仍60.60，v12 H7却23.48；定位及分母见 [研究报告](S10_PROMOTION_FRONTIER_REPORT.md) 和 [汇总](S10_POLICY_MINING_SUMMARY.json)。
- CONFIDENCE：`MEDIUM`。反例/限制：这些成本受选择与恢复混杂；不是鼓励透支。

## P10｜错过早期晋升后重排路径

- RULE：错过早期晋升后重排路径。
- WHEN：正式 Review no-advance。
- DO：结合具体反馈、交付链和可响应资源重排下一窗口；继续争取收入与后续机会，不追虚构阈值。
- AVOID：保证下次补晋升就能追平，或依据 final score 推演确定反事实。
- EVIDENCE：高参考4/4 M6晋升，低分全存活2/2 M12才晋升；RUN21 M6晋升却M12未晋升，RUN17早晋升仍淘汰；定位及分母见 [研究报告](S10_PROMOTION_FRONTIER_REPORT.md) 和 [汇总](S10_POLICY_MINING_SUMMARY.json)。
- CONFIDENCE：`LOW`。反例/限制：仅6条完整长程样本且按最终成绩分组，早晋升因果效果不识别。

唯一下一 Candidate 方向：**Option A**，以冻结 main v8a 为基线恢复 promotion-first 策略优先级，并以这 10 条短规则取代复杂策略理由协议；只作为 Main/Stage 后续设计输入。本任务不实现。`NEXT_GAME=NOT_AUTHORIZED`。
