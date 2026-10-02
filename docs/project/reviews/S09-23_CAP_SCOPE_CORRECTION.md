# S09-23｜CAP 证书范围纠偏与严格早停门禁

## Identity

- Status: Complete; `codex/s09-14-v9a-static` / `IN_FLIGHT_EVIDENCE`.
- Base evidence: `e0a5f2ee598d26fb012e3792ed974060113c1fe3`; implementation: `7895515453ea4a3e5ce650dd96b84a824256bd9c`.
- Parent: `candidate-v10e-explicit-basis-preflight`; candidate: `candidate-v10f-cap-scope-correction`.
- Classification: `SEMANTIC_CERTIFICATE_SCOPE_CORRECTION`; strategy delta `NONE`.
- Runtime delta: `CAREER_GROWTH_CAP_SCOPE_AND_STRICT_DEVELOPMENT_ABORT`.
- Main v8a freeze unchanged; live/provider/service/game operations=0.

## Corrected scope / root cause

`ROOT_CAUSE=CAP_CERTIFICATE_SCOPE_OVERBROAD_FOR_PUBLIC_BOUNDED_STATE`.
RUN14 a12/a13使用公开Dignity0–10、当前D=10折价额外D收益是合法局部价值比较。
旧v10e oracle把它纳入CAP growth certificate导致政策中止；该原因不证明Planning策略错误。
RUN14原始notes、冻结oracle结果、实际M5中止/6动作审查延迟和消耗的授权保持历史记录。
本报告给出后续Main Plan要求的scope归因纠正，不回填历史运行或评价whole-action最优性。

Header schema仍为v3，exact字段/顺序不变，不增加marker：

```text
[BC=PASS S=<NONE|ACUTE|TRUST|JOB|AFFORDABILITY|OTHER_PUBLIC_BINDING> CAP=<NONE|PUBLIC_SCOPED>]
```

- **CAP=NONE**：公开有界D/H最大值、当前Energy/公开有限counter、一次性资源预算耗尽的直接事实，
  仅用于当前边际收益/成本。它们不自动成为career-growth cap claim。
- **CAP=PUBLIC_SCOPED**：ranking使用职业资本、Skill/Network/Output、family、Level、未来成长或
  growth opportunity/channel封顶/完成推理，必须有explicit participant-public同scope cap/completion/capacity。
  exact nonempty scope必须匹配；无依据BLOCKED/SATURATION。
- **Scope transition**：D=10可以降低额外D-only即时收益；不能推出Network/promotion/role/future growth已满。
  bounded fact即使真实，也不能为外推family/Level cap提供豁免。
- K3原文和oracle S-basis代码段逐字不变；H2/H3/普通数值下降、旧S/数字恢复目标仍不能授权S。
  K1/K4/K5、startup/control/persistence、四Skills及所有策略排序不变。

## Explicit annotation contract

| Field | Reviewer meaning |
|---|---|
| growth_cap_claim | ranking是否用了career-growth saturation claim；bool，缺失/UNKNOWN fail closed |
| bounded_state_fact | 是否只有/同时有直接公开有界事实；事实标签，不豁免growth claim |
| explicit_public_growth_cap | 是否存在明确公开growth cap/completion依据 |
| growth_cap_scope | claim精确scope，声明growth cap时必须非空 |
| public_growth_cap_scope | 公开依据scope，必须exact match |

Oracle annotation schema=2；不自动分类任意prose，不调用Provider，不从旧saturation_claim静默回退。
历史fixture仅通过明确scope/serialization test adapter运行，原文件保持。
measurement的receipt coverage仍只是模型主张，不是semantic truth/enforcement proof。

## Replays / verification actually passed

[Sanitized replay](S09-23_CAP_SCOPE_REPLAY.json)绑定exact本地FORENSIC_HOLD来源和hash。
Raw/private logs未提交；RUN14原notes不改，RUN13只有已声明的certificate反事实投影。

| Replay | Result |
|---|---|
| RUN14 a12/a13：bounded D fact、growth=false、CAP=NONE | `RUN14_CAP_SCOPE_REPLAY=2/2 PASS`，仅K2/CAP scope |
| RUN13 a35/a36 numeric-S | BLOCKED / NUMERIC_S |
| RUN13 a37 A / S=NONE | PASS for scoped certificate checks |
| RUN13 a38 unsupported Output-Level cap | BLOCKED / SATURATION |
| RUN12三个exact原始前缀header | 3/3 CORRECTLY_BLOCKED / SCHEMA |

173 selected pytest checks PASS：

- 26新scope场景：11 positive / 15 negative，覆盖全部8 required positives和10 required negatives。
- 36既有explicit-basis投影，D范围/one-off budget两个case显式重新分类；K3 negatives保持。
- 23 header layout投影、28 K1–K5 kernel注释、8 RUN11注释投影。
- 3新增numeric-S negatives：H3、普通数字下降、数字恢复target续期。
- 5 identity/replay/receipt/schema/strict-abort contract检查。
- 17 strict POL/PROBE regressions（23无关历史identity cases deselected），27 post-run audit regressions。

一次canonical package `D:\CS\CareerSim\.local\runtime\s09-23-v10f\submission`：valid skill_bundle / exactly four Skills，逐byte匹配源manifest/Skills。
Selected delivery secret scan / git diff --check PASS。没有运行历史全量identity suite或任何live/model测试。

## Frozen assets / exact hashes / burden

| Skill | Unchanged Git blob |
|---|---|
| structured-state-board | `611e75d97234131acd5f321b5c7b75f50c1960ef` |
| rolling-planning | `f2f1f527453bc7f9c646ee8c9ca622ffa90f2cb5` |
| delivery-progress | `64e060b1febf746a05aa07494755a7f9d6eee600` |
| risk-review | `e602fe1a3343a28b472259ae46cfca780e780e48` |

Frozen policy trace/post-run parsers、packager、Runner tracked tree、pyproject.toml和uv.lock未改。
Retry config未读写；framework/dependency versions未变更。本任务不作新的runtime安装状态验证。

- Manifest physical SHA256: `ddb1d805e924ad39c7f9d240feecded469a55e8f5aac41f75a1c59eddcc5d614`.
- Instruction SHA256: `88e7a08849d3b60c2b564a59ed9697b234363000b74abd3171d20fd24c68aa8b`.
- [Gate](S09-23_VALUE_OF_RUN_GATE.json)包含manifest/metadata、四Skills、tools/fixtures/dependencies/package的physical/LF hashes和Git blobs。

| Prompt chars | Before | After | Delta |
|---|---:|---:|---:|
| Manifest | 5368 | 5402 | +34 (+0.6334%) |
| Planning | 7787 | 7787 | 0 |
| Combined | 13155 | 13189 | +34 |

仅替换K2/CAP preflight措辞；<=3% gate PASS，无重复saturation框架。
Strict development-stop治理写入已有LIVE_RUN_WORKFLOW和未来gate，不塞入participant策略提示。
Validation flags保持全false，不继承RUN14为v10f的gameplay/provider evidence。

## Strict early abort / future boundary

**`CERTIFICATE_OR_SEMANTIC_DRIFT => EARLY_ABORT`**。
Future S09 Main Run Plans保留header/BC/schema、certificate/evidence、numeric-S、unsupported growth cap、
restricted ranking、stale cleanup、action→fresh-observe、Skill drift、summary authority、oracle BLOCKED动作、
影响high-score interpretation的measurement uncertainty等即时中止理由。
不因trajectory/promotion/可能75+/多数动作正确而放行；异步审查减少latency并记录exact额外动作/实际cutoff。
这不增加Runner hook或free-text truth parser；合法bounded-state arithmetic不是违规。

Future explicit Main Run Plan可直接提供有界游戏授权，不另设余额/用户start确认。
此任务没有新游戏授权、没有replacement；既有FORENSIC_HOLD ACTIVE unchanged。
FACT：scope新注释让RUN14两动作通过、RUN13受禁推理仍被拦截。
LIMITATION：未证明运行模型持续按新scope输出certificate、长期语义遵循或分数/生存收益。

Decision: `S09_23_V10F_CAP_SCOPE_STATIC_PASS_RETURN_TO_STAGE`.

`NEXT_GAME=NOT_AUTHORIZED` · `NO_REPLACEMENT_RUN_AUTHORIZED` · `MAIN_V8A_FREEZE_UNCHANGED`.
