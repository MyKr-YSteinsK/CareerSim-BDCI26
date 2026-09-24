# S06-04 静态回归矩阵

Candidate：`candidate-v3c-zh-aligned-policy`。全部 PASS 仅表示语言文本、策略语义等价、仓库身份与静态交付合同通过；不表示 Agent 遵循、runtime 正确性、策略收益或 gameplay effectiveness。

| # | Plan acceptance | 静态证据 | 结果 |
|---:|---|---|---|
| 1 | S06-03 accepted ancestry verified | main ancestry includes accepted S06-03 source and reconciliation `201fe14…` | PASS |
| 2 | S06-03 acceptance reconciliation 仅改 dynamic state/ADR | commit `201fe14…` changed only `CURRENT_STATE.md` and ADR | PASS |
| 3 | S06-03 clean fast-forward to main | no merge commit; main advanced from `043ecd1…` to `201fe14…` | PASS |
| 4 | S06-04 branch 从更新后 main 建立 | branch base `201fe14…`; parent `candidate-v3b-final-policy` | PASS |
| 5 | no accepted-history rewrite | S06-03 commits preserved as ancestors; no rebase/amend/force push | PASS |
| 6 | 四个 Skill 正文以中文为主 | 每份正文人工审读；verifier 统计正文汉字/拉丁字母 | PASS |
| 7 | 四个 frontmatter description 以中文为主 | YAML parse + 每条 description 汉字占优 | PASS |
| 8 | runtime instruction 以中文为主 | JSON parse + instruction 汉字占优 | PASS |
| 9 | 无意外遗留长段英文说明 | 正文段落审读；除结构 token/API/短标识外为中文指令 | PASS |
| 10 | UTF-8 / YAML / JSON valid | UTF-8 decode、4份 YAML frontmatter 与2份 JSON parse | PASS |
| 11 | 四个 Skill names 不变 | frontmatter names 与目录名严格相同 | PASS |
| 12 | tool/API names 不变 | `new_game`、`observe`、`take_action` 精确保留 | PASS |
| 13 | Planning fields 不变 | 六个字段名在 `rolling-planning` 精确保留 | PASS |
| 14 | Planning progress enums 不变 | `ADVANCING`、`STALLED`、`UNKNOWN` 精确匹配 | PASS |
| 15 | Risk enums 不变 | `ALLOW`、`WARN`、`RECONSIDER`、`UNKNOWN` 精确匹配 | PASS |
| 16 | Board fields 不变 | schema 中全部原字段名、大小写与嵌套名匹配 | PASS |
| 17 | S02 marker 精确保留 | `[S02_SKILL_USED]` 及 notes 空格/空值规则静态断言 | PASS |
| 18 | 四个 S03 markers 精确保留 | 四种 Risk marker 字符串与空格行为静态断言 | PASS |
| 19 | Trace 行为等价 | CT-01–CT-08 全部 EQUIVALENT | PASS |
| 20 | Risk trigger 等价 | RR-01–RR-05、RR-11–RR-12、RR-18 全部 EQUIVALENT | PASS |
| 21 | Material Risk / Soft Cost 等价 | RR-06–RR-10 全部 EQUIVALENT | PASS |
| 22 | Risk 输出态语义等价 | RR-13–RR-18 全部 EQUIVALENT | PASS |
| 23 | 历史埋雷特殊边界等价 | RR-19–RR-20 全部 EQUIVALENT | PASS |
| 24 | Board session/freshness 等价 | SB-03、SB-05–SB-06、SB-12–SB-13、SB-19–SB-20 全部 EQUIVALENT | PASS |
| 25 | Board recent_effects <=2 等价 | SB-07、SB-14–SB-17 全部 EQUIVALENT；实现与 verifier 均断言上限 | PASS |
| 26 | Board bounded log recovery <=5 等价 | SB-07、SB-13–SB-14 全部 EQUIVALENT | PASS |
| 27 | Board 不规划/不提交动作等价 | SB-17、SB-21–SB-25 全部 EQUIVALENT | PASS |
| 28 | Planning trigger/reread 等价 | RP-01–RP-08 全部 EQUIVALENT | PASS |
| 29 | Primary Gap 等价 | RP-09–RP-11 全部 EQUIVALENT | PASS |
| 30 | ADVANCING 等价 | RP-12–RP-15 全部 EQUIVALENT | PASS |
| 31 | STALLED 等价 | RP-16–RP-18 全部 EQUIVALENT | PASS |
| 32 | Risk Budget 等价 | RP-19–RP-20 全部 EQUIVALENT | PASS |
| 33 | 普通决策排序等价 | RP-21–RP-22 全部 EQUIVALENT | PASS |
| 34 | controlled aggression 等价 | RP-23–RP-24、RT-07 全部 EQUIVALENT | PASS |
| 35 | Horizon 等价 | RP-25、RT-10 全部 EQUIVALENT | PASS |
| 36 | top-2 deliberation 等价 | RP-26、RT-11 全部 EQUIVALENT | PASS |
| 37 | severe-consequence 处理等价 | RP-27–RP-28 全部 EQUIVALENT | PASS |
| 38 | 六行输出 schema 等价 | RP-29–RP-30 全部 EQUIVALENT；字段名 exact | PASS |
| 39 | Single Agent authority 等价 | CT/RR/SB/RP authority 行与 RT-12 全部 EQUIVALENT | PASS |
| 40 | runtime controller instruction 等价 | RT-01–RT-12 全部 EQUIVALENT | PASS |
| 41 | strategy delta = NONE | 候选 manifest、RESULT 与矩阵结论一致 | PASS |
| 42 | 恰好四个 Skills | 目录扫描结果严格等于四个规定名称 | PASS |
| 43 | 无新 Skill/helper/router | changed-file scope 与 Skills 目录均无新增项 | PASS |
| 44 | 无 Memory | 无 Memory/持久存储实现；只保留 v3b 原边界 | PASS |
| 45 | 无 Team/Swarm | 仍为 Single Agent + 四 Skills | PASS |
| 46 | Runner unchanged | `career_sim_runner/` 相对新 main 无差异 | PASS |
| 47 | lock/dependency unchanged | `pyproject.toml`、`uv.lock` 均相对新 main 无差异 | PASS |
| 48 | v3b historical artifacts unchanged | S06-03 directory 相对 base 完全相同 | PASS |
| 49 | 无 hidden threshold/evaluator/event-answer policy | changed policy scan 与人工审读未发现上述规则 | PASS |
| 50 | v3c runtime manifest tracked | `runtime_manifest.json` 纳入 Git，四键 submission contract 可解析 | PASS |
| 51 | candidate manifest 自洽 | v3c blobs、父 blobs、commit、manifest/instruction hash 与 context 指标匹配 | PASS |
| 52 | semantic matrix 全部 EQUIVALENT | 104 条记录，104 EQUIVALENT，0 BLOCKED | PASS |
| 53 | static submission exact materialization | ignored 目录仅复制 manifest 与四个 candidate commit Skill blob，逐字节核验 | PASS |
| 54 | context/language budget 已报告 | v3b/v3c bytes、lines、Unicode chars、delta 与 instruction bytes/chars 已记录 | PASS |
| 55 | 无 secrets/runtime raw 入 Git | `.env` 路径扫描、secret pattern 与 changed path scope 检查通过 | PASS |
| 56 | `git diff --check` | staged/最终 diff 检查返回 0 | PASS |
| 57 | provider requests = 0 | 本任务仅 Git 与离线静态读取 | PASS |
| 58 | service starts = 0 | 未启动 JiuwenSwarm 或其他 service | PASS |
| 59 | install/reload = 0 | 未安装 submission、未 reload Skills | PASS |
| 60 | MCP runtime calls = 0 | 未触发 MCP | PASS |
| 61 | new_game/observe/take_action = 0 | 未调用 CareerSim tools | PASS |
| 62 | Runner play/full game = 0 | 未运行 Runner、gameplay 或比赛提交 | PASS |
| 63 | S06-04 branch commit + push | branch commits 已推送至对应 remote branch | PASS |
| 64 | remote SHA == local HEAD | 最终 fetch 后两者相同 | PASS |
| 65 | working tree clean | 最终 branch status 无变更 | PASS |
| 66 | 不 merge S06-04 into main | S06-04 仅作为独立 review branch 推送 | PASS |
| 67 | return Main review | RESULT 决策及 next recommendation 指向 Main review/Game Gate decision | PASS |

## 解释边界

矩阵 PASS 是静态文字、身份与 Git 交付证据；不证明模型遵循、中文表达带来得分提升、策略因果收益或 stable 80+。
