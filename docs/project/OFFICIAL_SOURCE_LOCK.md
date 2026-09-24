# CareerSim BDCI26 Official Source Lock v1.1

状态：当前官方事实与运行合同入口。更新日期：2026-09-22（北京时间）。

本文件取代 v1.0。区分官方声明、源码/元数据事实、项目执行约定和实际运行证据；出现冲突时重新核验来源，不以文档版本号代替官方证据。S01 本地环境与最小 baseline 技术闭环已有执行证据，见 [ENVIRONMENT](ENVIRONMENT.md) 与 [S01-03 run record](RUN_HISTORY.md#s01-03-baseline)；当前验收状态见 [CURRENT_STATE](CURRENT_STATE.md)，不由 Source Lock 代管。

## 1. Competition Identity and Repository

比赛为 2026 CCF BDCI【华为openJiuwen】Agent 职场长程生存与晋升挑战。参赛者使用 JiuwenSwarm 和 Agent Skills，通过 career-emulator MCP 进行 48 个月职业模拟。官方允许研究 Swarm Skill，但本项目仍从 Single Agent + Multiple Skills 起步。[赛事详情](https://www.xir.cn/competition/1165)、[赛题文档](https://career-emulator.readthedocs.io/)，核验日期：2026-09-22。

| 对象 | 当前冻结候选 | 职责与证据 |
| --- | --- | --- |
| 官方参赛仓库 | `openJiuwen-ai/CareerSim-BDCI26` | runner、示例、提交合同和依赖配置；赛题文档指向此仓库。 |
| repo SHA | `f61c738c72e51b77298cc1c14c7c6ebf4b6c527d` | 本项目基线候选提交，不声称为最新提交。 |
| `career-emulator` | `1.0.1` | 模拟器包；该 SHA 的 uv.lock 解析结果。 |
| `career-emulator-bdci26` | `1.0.0` | 比赛事件/配置数据包，与模拟器不是同一包。 |
| `jiuwenswarm` | `0.2.4b3` | 框架包；pyproject 使用等价写法 `0.2.4.beta3`。 |

上述版本取证于 2026-09-22：[锁定 pyproject](https://github.com/openJiuwen-ai/CareerSim-BDCI26/blob/f61c738c72e51b77298cc1c14c7c6ebf4b6c527d/pyproject.toml)、[锁定 uv.lock](https://github.com/openJiuwen-ai/CareerSim-BDCI26/blob/f61c738c72e51b77298cc1c14c7c6ebf4b6c527d/uv.lock)、[题库包元数据](https://pypi.org/pypi/career-emulator-bdci26/1.0.0/json)。仓库/包元数据中仍有 `Trenza1ore`、GitCode 旧链接；不能据此认定包与参赛仓库是同一对象或项目选错仓库。

## 2. Runtime Compatibility

| 层级 | 已知内容 | 不能据此声称 |
| --- | --- | --- |
| 官方项目声明 | 指定 SHA 的 pyproject 和 uv.lock 顶层为 `>=3.11,<4`。 | 所有 Python 3.x 都能安装完整依赖。 |
| 已核验直接依赖约束交集 | 模拟器 1.0.1 为 `>=3.11,<4`；JiuwenSwarm 0.2.4b3 为 `>=3.11,<3.14`；因此必须满足 `>=3.11,<3.14`。 | 所有传递依赖、OS、架构均兼容，或 lock 可无条件解析。 |
| S01 计划环境 | Windows / PowerShell，优先选 Python 3.12；具体补丁版本、系统 build/架构及 uv 版本在执行时记录。此为项目选择。 | 已完成安装、模型调用或对局。 |
| 实际验证环境 | 锁定时为 **NOT_VERIFIED**；后续实际值与验证范围见 [ENVIRONMENT](ENVIRONMENT.md)。 | 用计划值填写 PASS，或推广到所有平台/运行配置。 |

依赖元数据核验日期：2026-09-22。[JiuwenSwarm 0.2.4b3](https://pypi.org/pypi/jiuwenswarm/0.2.4b3/json)、[career-emulator 1.0.1](https://pypi.org/pypi/career-emulator/1.0.1/json)。若冻结 lock 与包元数据或安装结果冲突，记录错误并停止受影响步骤；不得静默改 lock、换版本后仍沿用原基线身份。

## 3. Reproducible Environment Lock

以下保留 S01 执行前的记录要求；表中“当前/待验证/未加载”为锁定时状态，不代表最新执行状态。后续实测见 ENVIRONMENT 与各实验 RESULT，字段要求继续适用。

| 字段 | 当前状态 / 填写要求 |
| --- | --- |
| repo SHA / local diff | 上述候选 SHA；实际 checkout 路径、HEAD、分支及差异待 S01 核验。 |
| package versions | 候选版本见第 1 节；运行前后记录完整已安装依赖清单并核对三项直接依赖。 |
| Python / OS / uv | 记录实际 `major.minor.patch`、解释器路径、OS build/架构、uv 版本。当前待验证。 |
| dependency state | 保存 pyproject/uv.lock SHA256、已安装版本清单、安装/依赖一致性检查结果；注明实际命令和时间。 |
| dataset identifier | 包版本、`source=distribution`、`split=dev`、加载时间、加载后数据位置及文件摘要清单。当前未加载；包版本不能替代实际数据摘要。 |
| submission artifact identifier | 基线名称、manifest 内容、提交目录逐文件摘要；ZIP 生成后另记 ZIP SHA256。未生成时明确写未生成。 |
| model configuration | 服务商、非敏感 endpoint、请求 model string、可取得的响应标识、映射依据及核验时间。不保存密钥。 |
| run identity | run ID、Agent 会话与游戏 session ID、命令/参数、记忆初始化方式、开始结束时间、终止原因、日志和结果的确切路径。 |

运行约定：

1. 在独立代码 checkout 的虚拟环境中使用原 lock 同步依赖；`uv sync --locked` 不允许自动重写 lock。同步失败应记录根因，不以升级绕过。
2. 一次性从已锁定题库包加载公开 Dev 并记录数据摘要；同批基线运行不重新下载或更新题库。
3. **不使用 `make play` 作为冻结基线入口。** 指定 SHA 的 [Makefile](https://github.com/openJiuwen-ai/CareerSim-BDCI26/blob/f61c738c72e51b77298cc1c14c7c6ebf4b6c527d/Makefile) 在 play 前执行题库包升级与数据更新。使用经核验的直接 runner 命令，并在已同步环境中以 `uv run --no-sync` 避免隐式同步；该选项不能替代安装状态检查。[uv 说明](https://docs.astral.sh/uv/concepts/projects/sync/)，核验日期：2026-09-22。
4. 共享 `career_emu` 实例的对局串行。不同 checkout 不等于实例隔离；安装会重置技能工作区并清理部分会话、任务与记忆文件。不能依赖跨局残留状态。[install.py](https://github.com/openJiuwen-ai/CareerSim-BDCI26/blob/f61c738c72e51b77298cc1c14c7c6ebf4b6c527d/career_sim_runner/install.py)、[paths.py](https://github.com/openJiuwen-ai/CareerSim-BDCI26/blob/f61c738c72e51b77298cc1c14c7c6ebf4b6c527d/career_sim_runner/paths.py)，核验日期：2026-09-22。
5. 依赖、题库、模型映射或提交内容变化即形成新配置，重新建立可比较基线；官方环境变更需要记录证据与影响，不永久拒绝更新。

## 4. Model Identity

以下本地配置/映射状态为锁定时快照；后续配置与请求/usage 标识见 [S01-03 run record](RUN_HISTORY.md#s01-03-baseline)。底层 serving version 仍为 `PARTIALLY_VERIFIED`，不以请求成功推断完全映射。

| 层级 | 证据及当前边界 |
| --- | --- |
| 比赛模型家族 | 官方评测声明 `DeepSeek-V4.1-Flash`。 |
| 赛题文档建议 API string | `deepseek-v4.1-flash`；这是官方接入建议，不保证任意服务商接受此名称。 |
| 锁定仓库示例 API string | `.env.example` 为 `deepseek-v4-flash`；示例名称不能证明实际后端不变。 |
| 本地 provider endpoint | **未配置、未核验**。S01 从用户已有供应商配置确认，不猜测或自动切换服务商。 |
| 已确认的公共映射 | DeepSeek 2026-09-10 公告称其官方 API 的 `deepseek-flash` 指向 V4.1 Flash，旧 `deepseek-v4-flash` 临时路由到该模型。仅适用于该公告范围与时间，不推广到所有平台。 |
| 本项目实际映射 | **未验证**。请求成功、返回 model 字符串和供应商说明分别记录；若无法确认底层版本，保留不确定性。 |

来源与核验日期（均为 2026-09-22）：[比赛模型说明](https://www.xir.cn/competition/1165/dataware)、[赛题接入文档](https://career-emulator.readthedocs.io/jiuwenswarm-mcp.html)、[锁定 .env.example](https://github.com/openJiuwen-ai/CareerSim-BDCI26/blob/f61c738c72e51b77298cc1c14c7c6ebf4b6c527d/.env.example)、[DeepSeek 公告](https://api-docs.deepseek.com/zh-cn/news/news260910/)。对模型名与服务商不匹配的情况先查证，不能仅凭家族相同忽略 alias 差异。

## 5. Competition Contract

以下为 2026-09-22 R1 官方页面核验结果，本轮复用同日证据；正式提交前复核最新通知。时区均为北京时间 UTC+8。

| 内容 | 已确认合同 / 边界 | 来源 |
| --- | --- | --- |
| Dev / Test | 公开 Dev 用于开发验证；保密 Test 用于正式评分。本地 Dev 高分不等于隐藏集成绩。 | [数据与评测](https://www.xir.cn/competition/1165/dataware) |
| 提交开放 | 2026-09-23 开放在线作品提交。 | [赛事详情](https://www.xir.cn/competition/1165) |
| 团队信息截止 | 2026-09-30 12:00，截止报名组队及团队信息修改。 | [赛事详情](https://www.xir.cn/competition/1165) |
| 初赛提交截止 | 2026-09-30 24:00，即 2026-10-01 00:00。10 月 31 日为赛事结束，不是初赛提交截止日。 | [赛事详情](https://www.xir.cn/competition/1165) |
| 提交限制 | 每队每日最多 1 次；保存最高成绩作品源代码供复现审核。 | [赛事详情](https://www.xir.cn/competition/1165) |
| 初赛入围 / 决赛 | 页面列 TOP5 经复现审核入围；决赛复用初赛材料与源代码，不能将 10 月理解为当然可更换方案的开发窗口。 | [赛事详情](https://www.xir.cn/competition/1165) |
| 完整评价 | 本地量化生存成就之外，还包含策略工程质量和资源效能。 | [数据与评测](https://www.xir.cn/competition/1165/dataware) |
| 决赛权重 | 云端统一评测 70%、专家评审 30%；不能移用为初赛或本地评分公式。 | [数据与评测](https://www.xir.cn/competition/1165/dataware) |
| 材料 | Skill 包及设计思路文档（PDF 或 Markdown）；说明职责、规划、框架选用、风险、失败恢复和资源权衡。 | [数据与评测](https://www.xir.cn/competition/1165/dataware) |

提交格式依据指定 SHA 的 [README](https://github.com/openJiuwen-ai/CareerSim-BDCI26/blob/f61c738c72e51b77298cc1c14c7c6ebf4b6c527d/README.md)，核验日期：2026-09-22：

```text
solution/
  manifest.json
  README.md
  design/
    skills_design.md
    decision_report.md
  skills/
    <skill-name>/SKILL.md
```

将提交内容按官方格式打包为单个 ZIP。manifest 使用真实团队名及 `mode=agent`，SKILL.md 必须有合法 YAML frontmatter（至少 `name`、`description`）。S01 可使用官方示例建立工程闭环，不代表已实现项目自有能力。

模式范围：此 runner 的 manifest 支持 `agent`、`team`。不得从这条合同推断整个 JiuwenSwarm 的历史子模式均已移除。以 [skill_contract.py](https://github.com/openJiuwen-ai/CareerSim-BDCI26/blob/f61c738c72e51b77298cc1c14c7c6ebf4b6c527d/career_sim_runner/skill_contract.py)、[constants.py](https://github.com/openJiuwen-ai/CareerSim-BDCI26/blob/f61c738c72e51b77298cc1c14c7c6ebf4b6c527d/career_sim_runner/constants.py) 为该 SHA 的模式/校验依据，核验日期：2026-09-22。官方 validate 不涵盖全部比赛材料要求，更不代表云端接收或评测通过。

## 6. Environment Understanding and Unknowns

公开事实：48 个月模拟，月度事件，季度 Energy 分配与主行动，半年绩效反馈，多维结局；部分参数与风险触发条件不公开。[公开手册](https://career-emulator.readthedocs.io/handbook.html)、[失败与结局](https://career-emulator.readthedocs.io/failure-and-ending.html)，核验日期：2026-09-22。不得编造隐藏阈值。

保留未知：隐藏 Test 分布、完整云端限额/超时与评分细则、已记录验证范围之外的兼容性、Multi Agent/Memory 收益、最优 Skill 拆分。公开实验只能评估可观测行为及泛化迹象，不能确认完整隐藏分布。尚无证据的内容标记 Unknown / Hypothesis。

## 7. Change Record

| 版本 / 日期 | 原因与证据 | 影响范围 |
| --- | --- | --- |
| v1.1 / 2026-09-22 | H-01：依赖元数据约束小于 repo 声明；H-02：Makefile 的隐式更新；H-03：官方赛程/交付/评审合同；M-01：模型、模式、来源适用边界。各节附证据。 | S01 环境选择、版本/数据记录、提交验收、事实摘要及后续实验可比性。架构路线不变。 |
| v1.1 语境修正 / 2026-09-22 | 依据已合入的 ENVIRONMENT、S01-03 RESULT 和 CURRENT_STATE，修正全局“未验证”陈述，限定历史快照语境。 | 仅修复事实归属；官方来源、冻结 SHA、包版本、运行/提交合同不变；未重新外部取证。 |

后续变更继续记录原因、新证据和影响范围。实际环境或模型映射尚未验证时，不得把此文档改写成执行成功证明。
