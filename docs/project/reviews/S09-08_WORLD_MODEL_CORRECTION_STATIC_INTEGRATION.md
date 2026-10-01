# S09-08｜世界模型纠偏静态集成

- Base：`f5dc8454269933efc6f4d31869d7edcbd3bcdc28`；parent：`candidate-v7y-story-exposure-guard`。
- New Candidate：`candidate-v7z-world-model-correction`；单一 delta：`LOCAL_RESPONSE_DOES_NOT_IMPLY_GLOBAL_CAP`。
- Status：`STATIC_IMPLEMENTED_NOT_RUNTIME_VALIDATED`；decision：`S09_08_WORLD_MODEL_CORRECTION_STATIC_PASS_READY_FOR_M6_VALIDATION_GATE`，即 `READY_FOR_M6_PROMOTION_VALIDATION_GAME_GATE`。

## 最小实现 / 保护边界

Planning 只新增一个 `Local Response / World Model Boundary` section：clean NO_GAIN 局限于当前 Level/context/dimension/action family/evidence window；UNKNOWN 保留价值；首次 Review 前保持多维晋升与可实现成果比较；恢复/避险仍有成长机会成本，Story 明确产出成本不能因 cap 假说归零。`LOCAL_NO_GAIN` 是 Planning 的解释标签，不改 Board enum，也不新增状态表。

Manifest 只改 CRITICAL KERNEL 中 Portfolio 与 NO_GAIN 两段，在原有5,000字符预算内镜像此 delta（新 instruction 4,988字符）。同一 kernel 的其余段、非 kernel instruction、metadata（除 Candidate name）保持一致。原有 gap dominance 的 fresh/specific/responsive/兑现条件及退出语义保留。

Board 已有完整禁止 hidden-cap inference 的条款，未修改。Delivery / Risk / Runner / dependencies / retry 未修改；exactly four Skills、ownership、fresh-observe shell、Fresh-binding S、Story Exposure Guard、Review reconstruction、Delivery lifecycle、public firewall 保持。Parent manifest/instruction 身份从既有 metadata 复制，三份未改 Skill 身份沿用；只计算新 manifest/instruction/Planning 身份。新 Candidate 九个 validation flags 均 false，不继承 parent gameplay/provider evidence。

## Targeted verification

根解释器执行：`python -m pytest -q tests/test_s09_08_world_model_correction.py tests/test_candidate_packaging.py`：**18 passed**。新场景测试是书面合同条款覆盖与 protected diff，不是 LLM 实际选择或 career outcome 测试。

| Case | 静态合同验收 |
|---|---|
| A：Output局部NO_GAIN，其它路径UNKNOWN，无binding threat | 局部折价、未测family保持开放；MODE=A及UNKNOWN价值被保留。 |
| B：S/N/O各有局部停滞 | 不推出全局saturation或关闭promotion搜索；responsibility/project/visible-result仍可比较。 |
| C：Recovery有价值，其它成长UNKNOWN | 同时比较survival/risk value和成长机会成本，不以封顶把恢复设为无成本默认。 |
| D：Mentor收益与明确个人产出损失 | public tradeoff必须比较；禁止假设Output cap把损失折零。 |
| E：首次Review前单维响应 | broad compounding prior保留；即时数值非唯一晋升代理，无固定动作、月份或配额。 |
| F：fresh material threat | 原binding Delivery/Risk/Fresh-S/survival floor优先级不被纠偏覆盖。 |

离线 canonical packager / Runner submission-contract 检查通过：skill_bundle、exactly four Skills、manifest valid、两次构建字节一致。未install/reload、未启动服务、Provider/MCP/DB/game调用为0；历史全量测试未运行。

## Bounded donor / belief-error contract check

只消费 [S09-07](S09-07_EARLY_PROMOTION_FAILURE_FORENSICS.md) 精确来源的派生公开记录 `D:/CS/CareerSim/.local/runtime/s09-07/public-windows.json`，核对下列各局 action index 的 public state / legal choice。没有游戏 replay、模拟分数、重新hash或全cohort扫描。

| Representative input | 静态适用性判断 |
|---|---|
| v6 M3 A14：H6、S/N/O=9/3/3，关键项目Main | broad ownership/多维合法路径仍可比较；NO_GAIN不把该family整体价值归零。没有把它写成必选或必晋升。 |
| v7o M3 A14：H5、9/3/2，关键项目Main | 可见成果、多维成长仍属于Portfolio；delta不排除donor-style broad growth。 |
| v6 M3 A13 / v7o M3 A11：健康恢复 | 恢复仍合法可比较，需要保留成长机会成本；不新增Health数字门槛，也不把这些数值单独判为S授权。 |
| v7y M3 A14：因N/O零增益偏向“confirmed-responsive Skill” | 禁止用过去Story gain保证当前Main gain；仍比较其它promotion value，**不强制反转轮岗选择**。 |
| v7y M6 A25、M9 A37–39：全部封顶→仅Health/risk有效→无机会成本 | 推理被新书面合同明确禁止；合法恢复/避险动作不被无条件禁止，需按原fresh-binding合同比较。 |
| v7y M11 A44：Output已封顶→Mentor个人产出成本有限 | cap不能替代当前明确public cost；必须真实比较产出损失与mentor/network upside。 |
| v7y M12 A52：O封顶→其它成长都无机会成本 | 未测试family和其它维度仍保留UNKNOWN价值，不能因O的局部记录关闭全部搜索。 |

这些结果是 **WRITTEN_CONTRACT_COVERAGE / donor behavior remains admissible**，不是“模型已在runtime成功拦截belief”或“选该动作就能晋升”。v7y M6/M12的充分失败原因仍UNKNOWN，完整S09-07结论不被本次静态patch改写。

## Handoff / 后续证据门

Selected secret scan、JSON/identity检查与`git diff --check`通过。交付仅Planning/manifest/Candidate、targeted tests、此review及CURRENT_STATE的一条durable delta；没有新增第五Skill、Memory、Swarm、实验或archive。原FORENSIC_HOLD不变。

本次只达到Gate1（static）。Stage需另行授权fresh run后检查：M6 promotion及adherence；同局M12 progression/survival；再独立replication。单次M6晋升仍不能声明 `HIGH_CONFIDENCE_M6_PROMOTION` 或稳定高分。

`NEXT_GAME=NOT_AUTHORIZED`
