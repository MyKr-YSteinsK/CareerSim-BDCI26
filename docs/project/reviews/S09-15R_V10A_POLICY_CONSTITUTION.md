# S09-15R｜v10a 策略宪法与季度决策静态收敛

## Identity / decision

- `IN_FLIGHT_EVIDENCE`，继续用户授权的 `codex/s09-14-v9a-static`；base/evidence `10734f0d23b015e0e686bd87a9dd2b8660c8760e`，parent strategy v9a at `1cc20d7`。
- 新 Candidate `candidate-v10a-policy-constitution`；implementation commit `0cecffd405d7dcdf55e6a1d8a60aef0a4b718318`。随后仅添加 measurement/review/state 与 RUN10 文档纠错；运行前须另行冻结 exact execution HEAD。
- 这是总体策略重构，不是行为等价 refactor。v9a/v8a gameplay、provider、score evidence 不继承；九个 validation flags=false。
- Decision=`S09_15R_V10A_POLICY_CONSTITUTION_STATIC_PASS_RETURN_TO_STAGE`。Main/Stage 审查 VALUE_OF_RUN_GATE 后才能另行授权；本任务 live/provider/game/install/service 均0。

## Strategy / simplicity

Planning **9,477→7,498 chars（减少20.9%）**；十条 Constitution 位于最前并高于解释性 prose，仍受 evidence firewall、binding safety、真实 Delivery 约束。统一六步 master ranking 替代 gap-first、多套排名和首评专用例外；Main/Energy 只是该排序的语义应用。

- Apply 是实质责任/ownership 的 strong prior，不是固定答案；Report 强优先级须真实成果，visibility feedback 不替代底层结果。
- Mentor/rotation 可凭新机会、角色/资本与逃离停滞的价值胜出；Avoid 只因 binding 或其它项明显有害。
- Energy 每次 fresh observe 后重排，responsive > stalled；Output gap 仅 attention cue，不授权重复 preparation farming。保留 v9a 的五条件 bounded probe，不自动胜出或连续未知 family 探索。
- Level change 依 Board reset；NO_GAIN 仅当前 Level/context/dimension/family，不推 cap。默认 A、最小必要保护、公开威胁解除即回 A；普通成本不自动 S。
- 保留 Review Plan、RECOVERY 接口、context recovery、Risk 单次 reconsider、whole-game persistence、四 Skill ownership；没有新 mode、quota、runtime ledger/Memory/Team/fifth Skill。

Board/Delivery/Risk 的 Git blobs 及与保留 v9a 包的物理 bytes 一致。Manifest 只改 candidate name，instruction exact unchanged；Runner/dependencies/retry 不改。离线包 `.local/scratch/s09-15r/submission` 经 canonical packager + frozen Runner 文件级合同验证，`skill_bundle` / exactly4 / manifest valid，无 install/reload。

## Measurement readiness

完整工具/fixture/候选身份见 [VALUE_OF_RUN_GATE manifest](S09-15R_VALUE_OF_RUN_GATE.json)，expected schema=1，冻结 physical SHA256、LF SHA256、Git blob。该 manifest 不构成 live 授权；将来 exact HEAD、clean branch、包与工具 bytes 仍须 pre-provider 核对，不能复用漂移身份。

`POL` 记录当前 public basis、family、response prior；`PROBE` 记录五位公开条件、eligible/compared/selected/family。每个 action notes 都输出，接在既有合法 CTRL/DL 后；仅输出测量，不参与策略输入、合法性或 durable ledger。

`scripts.policy_trace_audit` 用 exact session/window 的 events：dedup call/result，join fresh observe→合法 choice→success receipt→next observe，白名单状态/advertised dimensions；跨 month/Level、新 feed、负向/缺失状态视为 mixed/unknown response，不作 clean NO_GAIN。trace 缺失/重复/矛盾、E=?、错误 header、receipt/sequence 缺口触发 `STOP_BEFORE_PROVIDER`，总计为 null而不是零；完整 trace 的 mixed response 则有可计数的 `probe_UNKNOWN_count`。

输出 basis/MODE 分布、Level reset、立即 local NO_GAIN repeats、Delivery header coverage、全部八个 probe 核心计数。这些是 **公开 self-report claims + 可归因数值响应**，不是 LLM 策略诚实/语义正确性的 oracle；真实 result/binding/value 判断仍需依据 exact public context 有界审查。offline fixtures 不保证未来 LLM 一定输出 trace；runtime 缺失将明确标 measurement failure，不能声称机制未触发。

G2/G3 离线能力与身份 PASS；G4 RUN10 raw replay 输出全部字段、actions201、trace0、Delivery headers0，正确拒绝旧 uninstrumented run，未制造历史 markers。G5 已写约40M-token value statement：无论分数，至少判断响应优先/probe 是否实际执行、是否刷停滞或无结果可见度投入、是否值得保留下一样本；n=1 不宣称优于 v8a。Main acceptance 与下一次 live 仍未授权。

## RUN10 Delivery root cause correction

**已确认可复现原因：CTRL/DL separator 为空。** 全部201 action notes 的 CTRL 与 DL regex 均匹配，但 `[CTRL][DL]` 紧邻；既有 auditor 要求一个空格/换行，因此0/201。只加一个空格的离线 header counterfactual=201 valid，full existing auditor synthetic test也复现 space=PASS、empty=FAIL。`NOT_NEAR` 本身合法，RUN10 原报告的归因已纠正。

`10734f0:scripts/post_run_audit.py` 可恢复：LF SHA256 `496231857d4bc7e47ea7ad94329e5c665b527774cbfceb355931366015de8e23`；当前物理文件仅 CRLF 差异，normalized完全一致。RUN10 未记录实际执行物理 bytes SHA，不能事后声称 exact executed physical identity 已证明；没有发现 stale worktree 执行证据，也不绝对排除。当前未改 parser 或 Delivery strategy；historical覆盖结果/score保持，纠正原因并非修复那局 lifecycle evidence。

## Verification / evidence boundary

- **71 passed / 1 deselected**：新40项（含20书面反事实场景、正/负/模糊 fixtures、链条/响应/去重/污染排除/失败闭合/新身份/包）；existing auditor27、preflight3、canonical packaging1。
- 历史硬编码 v7y 的 identity test 不适用，保留原测试，新 v10a test严格替代身份/parent/blob/hash/flags断言。没有为了通过削弱旧测试。其余三个 preflight checks PASS。
- 实现初检出现字数与历史身份/精确措辞断言失败；已压缩至目标并恢复兼容 QUARTER_INTENT 表示，最终上述 targeted set全部PASS。这是 static/offline证据，不是运行模型选项/晋升/score 验证。
- 增量 secret-pattern scan、JSON parse、git diff --check；没有归档 raw、private config、shared DB/Provider日志。RUN10原 raw与summary保持，原FORENSIC_HOLD ACTIVE、owner/release条件不变。
- 可重建旧 raw派生 replay在 `.local/scratch/s09-15r/`；唯一原始证据仍在RUN10既定路径。Source完整hash/窗口在 gate manifest，不能用hash替代raw。

`NEXT_GAME=NOT_AUTHORIZED` · `MAIN_V8A_FREEZE_UNCHANGED` · `V10A_SUBMISSION_REPLACEMENT=NOT_AUTHORIZED`。
