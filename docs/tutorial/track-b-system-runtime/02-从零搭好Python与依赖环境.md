# 02｜从零搭好 Python 与依赖环境

[学习地图](00-学习地图.md) · [上一章：官方组件](01-比赛官方到底提供了什么.md) · [下一章：提交校验](03-Submission、Manifest与Skill校验.md)

主要事实来自[ENVIRONMENT](../../project/ENVIRONMENT.md)、[pyproject](../../../pyproject.toml)、[uv.lock](../../../uv.lock)与[来源锁](../../project/OFFICIAL_SOURCE_LOCK.md)。本章解释 S01 的实际安装记录和后续运行约定；**不是本轮已经重装环境或验证当前服务**。

## 1. Interpreter、package、environment 分别是什么

Python（编程语言）是这里 Runner 源码使用的语言。Interpreter（解释器）是读取 Python 程序并执行的可执行文件。写在 `headless_play.py` 里的函数只是文本，必须由解释器运行才能安装、联网或写文件。`D:\CS\CareerSim\.venv\Scripts\python.exe` 是本项目约定的根环境解释器，不是 Skill 本身。

Package（软件包）提供可导入代码、命令或数据；Dependency（依赖）是程序所需的这些外部材料。Runner 使用 WebSocket、YAML、数据库等能力，来自不同依赖；不能因自己的 Skill 不写 Python 就以为系统无需依赖。

Virtual environment（虚拟环境）是一份独立包环境，让这个项目使用自己的解释器入口与安装包集合。`.venv` 是目录名称，Windows 下常见命令在 `.venv\Scripts`，第三方包在环境的安装目录。它隔开包选择，**不隔开用户目录中的共享 JiuwenSwarm instance（具名实例）和外部 DB**。

**TEACHING EXAMPLE｜教学示例，不是历史 Run 原始记录。** 系统 Python 能 import 某包，但项目根解释器不能。正确检查对象是实际 Runner 使用的解释器与包集合；错误做法是用系统 Python 的成功结果证明根环境依赖齐全。反过来，根环境 import 成功也不证明 AgentServer 已启动。

## 2. Version constraint 与 lockfile

Version constraint（版本约束）告诉包管理器哪些版本可选。`pyproject.toml` 声明 Python `>=3.11,<4`，jiuwenswarm 使用 `0.2.4.beta3`，模拟器用 `1.0.*`。Lockfile（锁文件）`uv.lock` 记录实际解析到的依赖集合；环境记录又说明实际安装结果。三者分别是允许范围、解析身份和安装证据。

**FACT**：来源锁核验的直接依赖 Python 交集是 `>=3.11,<3.14`，比顶层 `<4` 更窄。pyproject 的分类列表即使列出 Python 3.14，也不能替代完整依赖兼容性。记录中的具体选择是 CPython 3.12.13，不推广成所有 Python 3.x 都能运行。

**INTERPRETATION**：如果一份约束允许几个版本，未锁定的同步可能得到不同环境。锁文件让“重建同一环境”有明确对象，但仍需要核对实际解释器、包与平台；它不是包已安装或运行成功的证据。

## 3. 本项目历史身份

| 层级 | ENVIRONMENT 的已记录事实 | 证据边界 |
|---|---|---|
| OS | Windows 11 家庭版中文版，10.0.26200，x64 | S01 核验身份，不是跨平台证明 |
| Python | CPython 3.12.13，64-bit | 实际解释器曾启动成功 |
| uv | 0.11.16 | 历史使用的包管理工具版本 |
| JiuwenSwarm | 0.2.4b3 | 与 `0.2.4.beta3` 为等价版本写法 |
| emulator | career-emulator 1.0.1 | 游戏代码发行版 |
| competition data | career-emulator-bdci26 1.0.0 | 数据发行版，不是同名顶层模块 |
| 根环境 | 仓库根 `.venv` | 后续 worktree 的静态检查默认复用 |

历史 sync 解析 252 个、安装 243 个包；这个计数不是必须手工记住的成功指标。关键是锁与安装身份一致、必要依赖可用、没有静默升级。ENVIRONMENT 记录 lock check、pip check、三项 import 和版本 metadata 通过；当时没有因此启动游戏。

## 4. uv 的历史三步如何理解

uv（环境与依赖管理工具）用于管理本项目的 Python 和依赖。下面是历史说明，尖括号内容是从已确认环境取得的值，不是可原样粘贴的完整脚本。

> **历史复现说明；当前 S11 未授权执行。Current S11 live operations = NOT AUTHORIZED。** 此块会安装解释器、创建环境或同步依赖；本轮没有执行。

```text
uv python install 3.12
uv venv --python <uv python find 3.12 result> .venv
uv sync --locked --no-install-project
```

第一步取得 Python；第二步用指定解释器创建项目环境；第三步按锁同步依赖。`--locked` 要求锁文件保持有效，不允许为了同步自动重写锁。它不意味着不会下载、安装或删除环境中的包。

`--no-install-project` 跳过当前项目本身的安装，仍安装其依赖。ENVIRONMENT 原因是 S01 当时尚无官方 Runner source package；这是那个历史阶段的事实。当前已经有 Runner 源码，不能继续说“仓库永远没有 Runner”，也不能凭此省略运行入口与工作目录检查。

**INTERPRETATION**：`uv python install 3.12` 中的次版本并不是精确补丁锁。历史实际找到的是 3.12.13；未来照抄命令可能得到不同补丁身份。真正复现要记录实际路径和版本，而不是只保存一段命令。

## 5. 不隐式同步根环境或新建第二套环境

[仓库约定](../../../AGENTS.md)要求静态／离线检查复用 `D:\CS\CareerSim\.venv\Scripts\python.exe`。若未来授权运行使用 uv，要先激活根环境，再显式 `uv run --no-sync --active`；不能在 task worktree 裸 `uv run`，让它自己创建或同步另一 `.venv`。

`--no-sync` 表示不在启动前隐式同步依赖；`--active` 表示使用已激活环境。它们不证明依赖已经正确，也不让后面的程序成为只读：若运行 `play`，安装和游戏副作用仍然存在。

**FACT**：来源锁还指出 frozen Makefile 的 play 前置步骤会升级题库包并更新数据，因此项目不用 `make play` 作为冻结入口。避开隐式更新保护比较身份，但不是对后续动作授予权限。

## 6. PATH 与绝对解释器路径不是一回事

PATH（可执行文件搜索路径）让程序根据一个裸命令名字找到文件。直接调用根 `python.exe` 能确定解释器，但 Python 中的子进程还可能用裸名查 `jiuwenswarm-start`。根解释器选对，不保证其进程 PATH 选对。

**FACT**：S07-51 在 `resolve_instance_ws_url()` 执行裸 `jiuwenswarm-start --list` 时发生 WinError 2，尚未连接 WebSocket 或 new_game。[原报告](../../project/runs/v7n-run1-validation.md)与[替换报告](../../project/runs/v7n-run1-replacement-validation.md)记录后续进程局部 PATH 修正；没有改 Windows 用户／系统 PATH 或 frozen Runner。

**INTERPRETATION**：解释器身份回答谁执行 Python；PATH 回答这段 Python 的调用进程能找到哪个命令。故障发生在 executable resolution（可执行文件解析）层，不能直接说 Skill 推理失败。第九章用完整案例讲验证边界。

## 7. .env 与秘密边界

`.env` 常用来保存服务运行配置，可能包含凭据。`setup.py` 的 env overlay（环境值覆盖）会把根 `.env` 中解析到的键写入实例 `config/.env`，保留不相关键；这也是 setup／environment validation 的潜在写入。我们只解释用途与源码行为，不读取或展示实际文件内容。

不能把密钥、token、cookies、私有 provider 配置或原始 headers 放进教程或 Git。正确环境身份可通过去敏版本与配置引用记录；“有凭据”不等于请求成功，更不证明 provider 后端模型版本映射完整。

## 8. 自测

“用了 `--locked`，所以不会安装东西”；“直接根 Python 就不用管子进程 PATH”；“数据包不能 import 同名 module，所以安装失败”；“pip check PASS 就能开赛”。分别哪里错？

参考分析：locked 限制锁漂移，不限制安装；子进程有自己的查找上下文；发行版可以仅提供数据；包一致性不证明服务、工具、授权或游戏链路。下一章把材料校验与环境校验拆开，避免以一个 PASS 覆盖所有层。
