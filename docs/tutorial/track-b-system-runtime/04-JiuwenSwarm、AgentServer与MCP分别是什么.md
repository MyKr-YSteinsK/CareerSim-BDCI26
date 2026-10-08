# 05｜JiuwenSwarm、AgentServer 与 MCP 分别是什么

[统一入口与术语](../00-从这里开始.md) · [本 Track 阅读路线](01-比赛官方到底提供了什么.md)


依据 [setup.py](../../../career_sim_runner/setup.py)、[mcp_config.py](../../../career_sim_runner/mcp_config.py)、[ws_client.py](../../../career_sim_runner/ws_client.py)与历史注册证据。本章不启动服务，不进行 MCP initialize/list_tools 或 provider probe。

## 1. Service 与 instance 是什么

Service（服务）是等待请求并持续处理工作的进程／组件。Instance（具名实例）把配置、数据和服务身份放在一起；此 Runner 约定 `career_emu`。服务可以停止，配置目录仍存在；存在一个目录或旧日志，不能说服务正在运行。

JiuwenSwarm 在本项目承担 Agent runtime：组织框架上下文、模型和工具执行。AgentServer（智能体服务端）提供 Runner 可连接的 WebSocket 入口。Provider（模型供应方）负责模型请求响应，是另一条外部调用链。

**INTERPRETATION**：看见“backend reachable”只说明连接服务这层有证据；它没有证明 provider 返回成功，也没有证明 emulator 工具可用。相反，模型请求成功也不说明游戏工具注册齐全。不要用一个“服务好了”混合三个命题。

## 2. 两条通信通道

```text
Runner ↔ WebSocket ↔ JiuwenSwarm AgentServer / Agent
Agent ↔ MCP tool interface ↔ career-emulator
Agent ↔ 配置的 model provider
```

WebSocket（双向持续连接）用于传送任务与流式响应帧；MCP = Model Context Protocol（模型上下文协议），在这里暴露游戏工具。它不是职业游戏，不自己决定最佳动作，也不等于 WebSocket。冻结 setup 配置的 MCP transport（传输方式）为 stdio（标准输入输出）：框架启动 emulator 子进程，经其输入输出完成协议通信。

本项目已核验的五工具是游戏接口；文件读取等框架工具可能另有来源，不能把 `read_file` 或 S02 的 `skill_tool` 加进这个五工具集合。

## 3. 能确认的历史 CareerSim 工具

**FACT｜历史注册记录**：S03-06 的 direct preflight 与实际 AgentServer 新注册日志都确认下列集合。证据在历史 Git 对象 `c4dbe0ebc4e27aafc22c94050c69547113cdc8eb:experiments/S03-06-config-repair-service-verify/RESULT.md`；当前树不再存该实验目录，属于可恢复历史，不是本轮新注册结果。

| 工具 | 本教程可确认的用途 | 不能扩大为 |
|---|---|---|
| new_game | 创建新游戏 session | 超时后可无限重发 |
| observe | 取得指定游戏的公开观察 | 允许读取隐藏字段 |
| take_action | 提交当前合法选择 | 模型文本就是成功提交 |
| check_latest_logs | 查看指定局允许的近期公开日志 | 查看全部 DB / 其他局 |
| show_employee_handbook | 取得公开员工手册 | 隐藏机制答案表 |

`ws_client.py` 使用 `mcp_career-emulator_` 前缀识别结构化游戏结果，但前缀代码不是全量工具注册证明。表只列历史 source/evidence 确认的集合；本轮在线注册状态 UNKNOWN，没有用猜测补列表。

## 4. setup 具体写了什么

`ensure_instance_initialized` 看到固定 instance root 已存在就返回；否则执行具名初始化命令。存在目录不证明配置健康，也不证明 live readiness。

`ensure_instance_configured` 读取实例 YAML，将 `mcp.servers` 设为一个 career-emulator 条目的列表，而不是自动保持所有旧 server。该项 enabled=true、transport=stdio、command 为裸名 career-emulator-mcp、args 为 `--update skip`，cwd 从 JiuwenSwarm executable 所在环境推导；env 填 Runner 默认 DB/log 路径与已定义游戏限制。之后 env overlay 可能覆盖实例配置值。

**FACT**：因此 CLI setup 会写配置，可能把后来修好的绝对 MCP executable 又写回裸名。它也可能改变有效 DB/log 路由。不能把 setup 当仅“显示当前路径”的无副作用命令。

**INTERPRETATION**：`--update skip` 避免这个启动路径自动更新数据，但 MCP 子进程仍是真正启动；没有 provider 的 direct MCP handshake 也仍属于 MCP live 操作。当前 S11 两者都未授权。

## 5. cwd、PATH、absolute path 的历史注册问题

S03-04 记录：裸 career-emulator-mcp 在既有 cwd 中 spawn 失败，WinError 2；使用同一环境的绝对 executable 通过 initialize/list_tools，且返回相同五工具。历史 AgentServer 完整 PATH 未保存，所以根因记 HIGH_CONFIDENCE，不把当前 PATH 当历史直接测量。

S03-06 后来只改 active config 的 command scalar，再通过真实服务注册日志确认五工具。其分类是 runtime-persistent but setup-overwritable（写入运行配置但可被 setup 覆盖），并非修复 frozen setup 源码。二次 setup 是否覆盖必须按实际入口核对。

**INTERPRETATION**：cwd（工作目录）指定进程运行位置，PATH 指定裸 executable 的查找环境，absolute path（绝对路径）直接指定文件。把 cwd 指到 Scripts 并不保证 Windows resolver 就能找到裸命令。launcher 存在、配置字符串存在和 spawn／握手成功分别证明不同层。

精确历史来源和统一故障结构见[第七章](07-工程排障与完整运行链复现.md)。这些探针是当时有界授权动作，不是本章邀你再次运行。

## 6. 服务启动为何可能已经调用模型

**FACT**：S03-06 没有发 Agent chat、CareerSim tool 或新局，却在一次服务 startup 中记录一条完成的 incidental prewarm（附带预热）provider response，200 input / 1 output / 201 total tokens。多条 start/end 内部日志属于同一次请求，不是多次完成。

这说明“我只启动服务”不能保证 provider calls=0。启动、工具注册、模型连通、游戏开始仍需分别记账。本任务没有启动或读取实际私有 provider 配置，也不把那次 startup 推广为每次启动都必定调用相同数量模型。

历史运行流程记录的启动命令如下，当前只作教学说明。

> **历史复现说明；当前 S11 未授权执行。Current S11 live operations = NOT AUTHORIZED。** 服务启动可能触发模型预热。

```powershell
& 'D:\CS\CareerSim\.venv\Scripts\jiuwenswarm-start.exe' --name career_emu all
```

这是 [LIVE_RUN_WORKFLOW](../../project/LIVE_RUN_WORKFLOW.md) 的已建立启动操作，不承诺任意未来环境或所有实例都能成功。S03-06 的历史 app-only 启动是另一个当时入口，不能把两种模式的进程／端口行为混为一谈。

## 7. WebSocket URL 如何得到

`resolve_instance_ws_url()` 执行裸 `jiuwenswarm-start --list`，找到实例行，从最后一栏 ports 的首个斜杠前片段取 AgentServer port，形成 `ws://127.0.0.1:<port>`。这是 frozen 输出格式解析约定，不是自动扫描所有端口。

没有找到实例会抛错误；裸命令无法创建则更早失败。`--ws-url` 可以直接提供已核验 URL，避免这次解析，但不能绕过 MCP 注册、共享 runtime、有效 DB 或 provider 门禁。更不能凭一个 URL 文本宣布服务就绪。

## 8. 自测

MCP 配置里含服务器名字，是否已有五工具？服务连接通过，是否 provider 通过？direct MCP 不传密钥，是否就不是 live？absolute executable 修复是否不会被 setup 覆盖？

参考分析：文字检测不同于注册；连接不证明模型返回；协议进程启动仍是有副作用的在线动作；frozen setup 的裸名配置会再次写入。下一章将这些组件接到真实 Runner play / drive 编排里。
