# S10-17｜Final Route Decision

Status: COMPLETE / IN_FLIGHT_EVIDENCE。Decision: `V6D_FALLBACK + NO_MORE_ARCHITECTURE_EXPLORATION`。

Branch `codex/s10-17-candidate-family-portfolio`；Base `ce95a01297424d930a64b2a63c36b7e6e215090e`。证据与详细比较见 [portfolio](../research/S10-17_CANDIDATE_FAMILY_PORTFOLIO.md) / [lineage matrix](../research/S10-17_LINEAGE_MATRIX.json)。交付commit以Git包含本报告的提交解析，不嵌自身SHA。

## Main recommendation

**PROMOTE_V6D_TO_PRIMARY_FALLBACK**。exact v6d source `e7e8ab44dd85a29135eb089ef29de8fed298f4a4`；两局65.35–71.67，均48m/L5。v8a两局59.00–72.65，均48m/L4–5。v6d观察floor高6.35、ceiling低0.98、spread6.32比13.65小；同为两sample，这不是显著优势/真实概率。3Skills及11803源码字符proxy小于v8a4Skills/22866；两局freshobserve/schema/session有效，closure/compression/clock不足明确保留。v8a同样未达到完整runtime_validated，不能用已有freeze替代执行质量证据。

这只是推荐Main切换主fallback；没有修改current_candidate、manifest、validation flags、Source Lock或main正式freeze。v8a历史freeze保持可恢复身份；v6d最终提交仍须另行hardening/freeze/package审计，不授予official submission validity。若未来必须全作者协议PASS才可提交，两者都须复核。

## Challenger gate

**NO_JUSTIFIED_CHALLENGER**。donor+survival/cleaner runtime/broad portfolio/shortcontext/retrieval/result maturity均有实质前身或live。v8a已是v7o donor core与v6共同原则+现代shell，v12试Brief/checkpoint减负，v14试capsule/retrieval，v10c试persistentkernel。control-minimal的剩余literal组合没有安全、可推广收益证据；不能证明不会重演v1 trustterminal。Team当前不可部署。S10-13/15/16的no-safe-patch结论不以新名字重开。

## One next task

**S10-18: 第三次exact v6d replication**。另行Main Game Gate、exactsource、一个fresh full game、zero patch/rescue/replacement。它比立即制造v6e或宣称final冻结更能回答75+可达性和within-policy drift。当前live权限仍NONE；不自动开始，不授权无限局。

## Verification and limits

54lineage节点、58canonical attempt/对照记录、25绑定Flash自然终局；两个≥75正式样本仅v1#1与v6#1。三项旧UNKNOWNidentity/异执行器记录单列，技术/censor不计floor。静态字符、JSON、来源分数核对、protectedruntime差异、增量secret scan及gitdiffcheck通过；commit/push与cleantree由closeout回执核实。无Candidate/Skill/manifest/install/service/provider/game变更，所有hold不变。

Non-claims：no true performance distribution；no stable75 proof；no hidden-test transfer；no causal architecture claim。

`RETURN_FOR_FINAL_ROUTE_DECISION`

`NEXT_GAME=NOT_AUTHORIZED`
