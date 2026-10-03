# Agent Runtime Contract｜S10 Family A

`S10 FAMILY A STATIC ARCHITECTURE / NOT RUNTIME VALIDATED`

此branch按S10-02授权实现两职责架构，属于 `IN_FLIGHT_EVIDENCE`。Main submission fallback仍为 frozen `candidate-v8a-v7o-donor-core-transplant`，没有替换。旧架构合同可从accepted parent `18241435da3728e64318f6072aabaaba2766e8b2` 恢复；本合同显式改变Skill decomposition、证据准入、摘要/recovery和ordinary输出，不以格式重构掩盖行为delta。

## 1. Architecture / authority

```text
same-session fresh observe
  → career-state-brief: current public facts + current Career Brief
  → career-decision: bounded value comparison + final selected-candidate safety
  → Single Executor: fresh/session/legal check → exactly one take_action
  → immediate fresh observe
material checkpoint → same-agent Deep Review → replace current Brief → ordinary loop
```

两份Skill均 `Can Submit Action: No`；Single Agent是唯一action submitter。State & Brief管理事实与摘要写入，不rank/select/gate；Decision提出目标/更新建议、比较和final safety，不改写事实。Executor独占实际游戏工具提交。没有Team/Reviewer Agent、第五Skill或跨局learned memory。

## 2. Evidence admission

最新participant-visible fresh observe是实时public state权威，public Handbook/Review/result与必要同局官方logs提供补充事实。工具success不证career result，notes不是独立证据。

Main本任务接受官方 MCP 当前tool response合法choice直接返回的 `status_updates / effects`（包括 `HiddenRisk` delta）为 `ADVERTISED_CONFIGURED_DELTA`。此类metadata可比较；`advertised/configured delta != realized effect != hidden stock`。动作后以fresh observe验证；差异记 `ADVERTISED != REALIZED / CAUSE UNKNOWN`。不把advertised delta写成current state。Hosted缺字段时用现有公开语义正常决定，不猜值、不为此阻断整局。

禁止hidden stock/counter reconstruction、累积deltas估算存量、private DB/raw Test、internal IDs、decoded private Test mapping、hidden formula/exact threshold/cap reconstruction、field缺失猜值、不可见Story内部effect和event→answer lookup。此为锁定接口准入修正，不宣称官方身份/比赛规则变更，不修改Source Lock。

## 3. Career / failure floor

目标是剩余horizon的晋升、broad visible成长、ownership与现实成果兑现。普通成本可接受；动态比较public余量、advertised代价、当前负荷、不确定下行及真正可达恢复，避免material survival/safety/trust/job/income failure。无固定Health buffer、risk count、晋升阈值或菜单答案。

Same-scope约束持续，只有相关公开解除或风险承载场景结束才清除；generic praise、silent warning与一次cleanup不证明clearance。低绩效/no-advance本身不等生存危机。最小必要保护仍保成长，威胁解除后回主线，不补满资源。真实commitment/result优先于弱新承诺，但不挡更强时限机会；claim/receipt/report标签不证成果，stale item须重验可兑现性。

## 4. Career Brief lifecycle / storage decision

`CONVERSATION_RESIDENT`，不是file-backed/durable状态。静态路径依据：Runner `install._write_identity_md` 将manifest写入IDENTITY；host ContextAssembleRail在model call装配；SkillUseRail提供Skill描述，正文由read_file进入dialogue。已存在dialogue输出即可承载逻辑当前摘要，无新host primitive。官方solution只需manifest/两份Skill即可表达此规则；实际加载/执行/compression恢复未验证。

五组仅为 `SESSION_BASIS / REVIEW_OBJECTIVE / RESULT_COMMITMENT / UNRESOLVED_CONSTRAINT / PATH_UPDATE_STOP`。State & Brief为唯一历史摘要写入责任；Decision只提更新。同局初始化、material checkpoint和recovery输出完整新版本supersedes旧版；ordinary observe仅替换有变化事实和核验basis。逻辑当前版本是最近完整块加后来有效字段替换，不声称旧conversation物理删除。bounded future-relevant，不append历史，不复制全Board、不建parallel plan/cursor/阶段账本，不静默删真实未履行义务。

新session全部reset；Level/context变化重验局部path，fresh事实覆盖stale摘要；无法恢复字段UNKNOWN。result验证与constraint解除都要求same-scope独立公开basis。storage不依赖本机绝对路径、MEMORY.md残留、私有DB/S09 raw或跨局state。Hosted文件权限/持久化UNKNOWN，不作本Candidate依赖。

## 5. Bounded decisions / deep checkpoints

one fresh observe = one bounded decision，最多两个competitive options、一次直接相关替代比较；选中替代仍需最终安全检查。无新公开证据不重开。Energy每个单integer动作后fresh重新决定，无batch/配方/配额。local clean NO_GAIN只折该Level/context/dimension/已测family，其他路径/多维价值仍开放；混杂UNKNOWN，不推global cap。

material正式Review/no-advance/promotion、新/升级major trust/job/compliance warning、major Health/safety shock或活动不可行、major result/failed commitment/blocker、repeated clean NO_GAIN使高值path失效、机会/目标重大失效，才触发same-agent Deep Review。用公开basis去重，同一Review+promotion/多trigger合并一次；普通Story/一次drop/重复旧warning不反复深评。

三问：什么真实改变/奖励/失败及假设失效？下一目标/path和停止事项？什么结果/风险持续、哪种公开证据使它失效？完整新Brief后退出ordinary loop，不做48个月刚性计划。无因果依据UNKNOWN，不以高分单局证明机制。

## 6. Action safety / recovery / whole-game

提交前检查同session fresh menu、single legal integer和final selected-candidate safety闭合。successful action后立即fresh observe，receipt无fresh state，不连续stale action。已有session禁止第二new_game。

失败/unknown action outcome、session mismatch、observe失败或最终选择未闭合时停止提交；只能在既有授权内核对同局公开状态/日志，不盲重发。仍unknown/不可恢复工具错误停止留证。策略收益未知不妨碍事实合法的bounded决定，但不绕过身份/动作未知hard stop。

可见resume/compaction/recovery或当前摘要不可核验时：同session→fresh observe→两Skill重读→最小同局官方logs与当前事实重建Brief（缺字段UNKNOWN）→新的fresh合法决定/final safety。旧摘要不能自证恢复；不虚构host compression detector。身份/fresh/read失败不action；丢失历史目标可UNKNOWN重新决定，不无限logs。

structured game active时持续whole-game loop，不在action/month/Review/Brief输出处自愿终止；自然结束只认structured `game.ended`，技术失败独立记录。任务live权限始终由Task定义，静态Candidate不授权游戏。

## 7. External observability / verification boundary

Runtime不要求CTRL/DL/BC/certificate、分支枚举或协议状态自报，不将marker格式作为action gate。notes保留简短公开选择理由；必要fresh/session/legality/final safety/unknown-stop规则仍在模型上下文，不能仅外移为局后audit。

Frozen Runner不改：tool events/transcript仍保存session、observe/action顺序、choice/notes；score与runner termination用于horizon/Level/technical failure。Brief更新仅在输出可见时可以审核，缺失不能推断为已执行。

`scripts/post_run_audit.py` 的旧marker coverage、历史Skill recovery与numeric-HiddenRisk分类仍服务历史Candidate，不能作为本Candidate adherence verdict。未来S10 live audit需窄适配：将旧marker缺失视为不适用、recovery按本metadata两Skill核对、delta provenance区分advertised与stock、按可见Brief/公开basis审查checkpoint；复用session/fresh pairing/score extraction，不新增marker。本次未修改该历史pipeline或Reviewer controller，未开展live验证。正式submission builder/materials仍锁定v8a，拒绝静态Candidate；本任务只构建Runner-compatible验证包，不是正式submission。

`runtime_validated=false / gameplay_validated=false / NEXT_GAME=NOT_AUTHORIZED`。
