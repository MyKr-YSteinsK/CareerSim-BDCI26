# 03｜Submission、Manifest 与 Skill 校验

[学习地图](00-学习地图.md) · [上一章：环境](02-从零搭好Python与依赖环境.md) · [下一章：安装](04-Skill是怎样真正安装进JiuwenSwarm的.md)

本章依据冻结 [skill_contract.py](../../../career_sim_runner/skill_contract.py)、[validate.py](../../../career_sim_runner/validate.py)、[models.py](../../../career_sim_runner/models.py)与 [cli.py](../../../career_sim_runner/cli.py)。**FACT** 表示源码实际检查；为什么拆层属于 **INTERPRETATION**。本轮只阅读源码，不运行这些环境校验入口。

## 1. Bundle 是可搬运的材料，不是运行中的 Agent

Bundle（材料包）是一组按合同组织的文件。Runner 把目录视为输入，识别 manifest 和 Skill，再安装进框架工作区。开发仓库中的 `configs/runtime_manifest.json` 不是天然位于比赛布局里；项目 builder（构建脚本）可以生成 `solution/manifest.json`，但 builder 是项目自建工具，不能当 Runner 自己会自动寻找每个候选配置。

最小 Runner bundle 识别需要至少一个 `skills/<目录>/SKILL.md`；历史正式比赛材料还需 README、design 等，见[第一章](01-比赛官方到底提供了什么.md)。通过低层识别只说明文件形状被支持，不说明正式材料齐全。

## 2. Manifest 的字段与两种 mode

Manifest（清单）使用 JSON（一种结构化文本格式），提供方案元数据与运行指令。

| 字段 | 源码如何使用｜FACT | 容易误解的地方 |
|---|---|---|
| team | `validate_manifest` 拒绝空白和已知占位团队名；用于日志标签优先项 | 不检查团队是否已在平台注册 |
| name | 标签备用项；team/name 都没有时用目录名 | 不用它独立认证 Candidate 或 Git commit |
| mode | 校验是否在 agent/team 集合；`resolve_run_mode` 再用于驱动请求 | 官方支持 team 不等于本项目启用 Team/Swarm |
| instruction | 安装时转为文本，规范化后写入 IDENTITY | `validate_manifest` 没有检验策略语义与遵循能力 |

`submission_mode=skill_bundle` 是 Runner 对材料布局的内部识别；`manifest.mode=agent` 是 JiuwenSwarm 的执行模式。两个字段不能互换，不能为了表达“我是 Skill 包”把 manifest.mode 填 `skill_bundle`。

**FACT**：此 frozen validator 对 instruction 没有完整类型或内容合同检查，也不会证明其中的模型指令可执行、安全或有效。正式方案仍要遵循项目及比赛要求，不能把检查缺口当任意输入的推荐做法。`validate_manifest` 输入已解析字典，输出错误列表；它为完整材料校验提供团队/模式最低字段检查，不认证平台注册、策略内容或实际执行。

## 3. Frontmatter 是给框架看的入口说明

Frontmatter（前置元数据）位于 SKILL.md 最前面，用 YAML（一种键值文本格式）描述 name 与 description。正文再写职责、触发与边界。

**TEACHING EXAMPLE｜教学示例，不是历史 Run 原始记录。** 下列目录名与 metadata 同为 sample-facts，仅教格式，不是比赛已安装模块：

```yaml
---
name: sample-facts
description: "整理已取得的公开事实，不提交动作。"
---
```

`validate_skill_frontmatter(skill_dir)` 输入一个 Skill 目录；先确认 SKILL.md 存在、文件以 `---` 开始且有结束标记，再用 `yaml.safe_load` 解析；name 和 description 必须有真值。输出错误文字列表，空列表表示它实现的检查通过。它用于识别框架所需的最小元数据入口，不负责正文质量、模型加载或 gameplay。

**INTERPRETATION**：description 是用途入口，不是 Skill 已应用的证明。源码也没有证明 name 必须与目录名相等，或正文每项规则都无冲突；教程建议一致命名是为了可识别，不能写成 validator 已强制这些附加条件。

## 4. 三个校验层级不能合成一个万能 PASS

### validate_submission_contract：低层布局合同

输入 submission 目录；解析真实路径，用 `list_bundle_skill_ids` 枚举直接子目录中具有 SKILL.md 的项并排序，确认支持的 bundle、manifest 文件和 skills 目录存在。加载 JSON manifest，返回标准化 details：目录、label、manifest、submission_mode、skill_ids。布局不符合时抛 `SubmissionError` 等错误。

| 问题 | validate_submission_contract 的源码回答 |
|---|---|
| 输入 | submission 根目录 |
| 主要步骤 | 解析真实路径、识别 bundle、读 manifest、枚举 Skill、检查布局 |
| 输出 | 标准化 details 字典；不符合布局时抛异常 |
| 为什么存在 | 为安装和完整材料检查提供共同的布局与元数据入口 |
| 不负责什么 | manifest 字段合法性、frontmatter、正文策略、运行环境、模型/游戏与官方受理 |

**FACT**：它没有调用 `validate_manifest` 或 `validate_skill_frontmatter`，更不启动框架。单独 `install_submission` 使用此低层函数，因此不能假设 install 已执行完整字段和前置元数据校验。

### validate_submission：材料检查报告

输入目录；先做低层合同，再检查 team/mode 和每个实际枚举 Skill 的 frontmatter，返回 `ValidationReport`。布局失败时记失败并提前返回；字段与 frontmatter 错误追加为 checks。`report.ok` 是所有检查均真。

为什么存在：把布局、manifest 与每 Skill 错误汇总，便于在安装之前修材料。它不负责环境连通、模型调用、游戏效果、正文策略、design 完整性或平台受理。

### validate_environment / validate_all：本机运行检查

`validate_environment` 输入可选 WS URL 与 DB path，创建 runtime 目录、必要时初始化 instance、覆盖实例 env，检查工具路径、数据文件、配置文字、DB 对齐／可写、Skill 根与 WebSocket 可达，再返回报告。`validate_all` 合并材料与环境报告；CLI `validate` 走这一层。

**FACT**：DB 可写检查会建父目录、写再删 `.write_probe`；env overlay 可能写实例文件；backend check 会建立 WebSocket 连接。没有“validate”这个名字能取消这些副作用。当前 S11 没执行它。

## 5. 合法／不合法材料的具体例子

**TEACHING EXAMPLE｜教学示例，不是历史 Run 原始记录。** 构造一个仅说明 Runner 材料检查的目录：

```text
solution/
  manifest.json
  skills/sample-facts/SKILL.md
```

构造 manifest：

```json
{
  "team": "教学团队甲",
  "name": "example-only",
  "mode": "agent",
  "instruction": "仅使用当前公开事实，唯一 Agent 提交动作。"
}
```

配合上一节合法 frontmatter，可满足这几个材料检查；**不是正式比赛完整提交，也不是本轮运行验证结果**。若删 manifest，布局失败；若 team 空白或 mode 写成 skill_bundle，字段失败；若前置块无 description，frontmatter 失败；若只放普通 README 而没有任一 SKILL.md，连 bundle 都无法识别。

一个细微反例：manifest 存在、目录中有 SKILL.md，但 YAML 格式错误。低层 `validate_submission_contract` 可以识别布局，`validate_submission` 会报前置元数据失败。不能看到前一函数通过就说“全部校验已过”。

## 6. Environment PASS 的有限含义

`mcp_config.py` 的 `config_mentions_career_emulator` 只检查配置文本同时包含服务器名与可执行名；`env_mentions_db` 只检查路径文字出现。`setup.tool_availability` 用 PATH 找 jiuwenswarm-start，再检查同目录 launcher 文件。它们不完成真正 MCP initialize/list_tools，也不证明 AgentServer 子进程环境能解析命令。

`check_backend` 证明一条 WebSocket 可建立，不证明 model provider 成功、所有工具注册成功或 Skill 正文已读。数据检查确认指定 failure_conditions 目录有 json/data 文件，不认证整个隐藏集或数据完整摘要。

**FACT**：S03 的历史注册故障表明“配置里写了命令”与“服务真的注册五个工具”不同；第九章给出精确来源。`play_headless` 还只把 environment report 的 backend-reachable 失败当阻断，不把所有 checks 自动 fail closed。那是 frozen 源码行为，不是建议忽略其他必要硬门禁。

## 7. validation PASS 不等于运行或评分通过

```text
材料 VALIDATED
≠ 已复制 INSTALLED
≠ 框架发现 DISCOVERED
≠ 正文读取 LOADED
≠ 动作使用 APPLIED
≠ gameplay 完成
≠ 官方 hidden score / 平台验收
```

**INTERPRETATION**：每个命题都要不同证据。字段格式通过，只能消除该类错误；它不能补上后续服务、工具、session 或行为证据。也不能因为一局低分就否定前面的材料检查，它可能完全通过但策略或执行出问题。

## 8. 自测与边界

为什么坏 frontmatter 可能通过低层 contract，却被 validate_submission 拒绝？为什么 CLI validate 不能放入本轮纯离线命令？为什么 manifest.mode=team 并不授权本项目多 Agent？

参考分析：函数检查范围不同；环境校验会初始化、写文件并连服务；官方支持集合与项目路线／任务权限不同。下一章沿实际安装顺序看复制、注册与指令写入，继续把“文件存在”和“实际执行”分开。
