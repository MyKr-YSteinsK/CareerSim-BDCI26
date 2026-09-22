# ENVIRONMENT

> S01-02 的实际环境与依赖冻结记录。只保存可复用事实，不保存安装日志、API key、token 或其他凭据。

## Identity

- Verified: 2026-09-22
- OS: Windows 11 家庭版中文版，10.0.26200，x64
- Official runner repository: `openJiuwen-ai/CareerSim-BDCI26`
- Official runner SHA: `f61c738c72e51b77298cc1c14c7c6ebf4b6c527d`
- Dependency source: official `pyproject.toml` and `uv.lock` at the SHA above；两份文件原样复制，SHA256 未改变
- `pyproject.toml` SHA256: `B399225F2C00B415F3C8A3317F8CDECF72114AE7A41111B4410F201466E40F73`
- `uv.lock` SHA256: `18466056430F7C49C3A23705D312625B40B1A5119C41F0EC62571CDA208E4C0C`

## Python and environment

- Package manager: `uv 0.11.16`
- Managed interpreter: CPython `3.12.13`，64-bit
- Source Lock declared range: `>=3.11,<4`
- Actual direct-dependency intersection: `>=3.11,<3.14`
- Project environment: repository-root `.venv`
- Environment executable: `.venv\Scripts\python.exe`

## Installation

```text
uv python install 3.12
uv venv --python <uv python find 3.12 result> .venv
uv sync --locked --no-install-project
```

The sync resolved 252 packages and installed 243 packages without changing `uv.lock` or upgrading the official frozen dependency set. `--no-install-project` is intentional because this repository does not yet contain the official runner source package.

## Verified package versions

| Distribution | Actual version |
| --- | --- |
| `pip` | `26.1.2` |
| `fastmcp` | `2.14.7` |
| `career-emulator` | `1.0.1` |
| `career-emulator-bdci26` | `1.0.0` |
| `jiuwenswarm` | `0.2.4b3` |
| `rich` | `15.0.0` |
| `pyyaml` | `6.0.3` |

## Verification

- Python executable starts and reports `3.12.13`.
- `uv lock --check`: PASS。
- `python -m pip check`: PASS，未发现 broken requirements。
- Imports: `fastmcp`、`career_emulator`、`jiuwenswarm`: PASS。
- Distribution metadata: all three official distributions report the versions above。
- `.venv` is excluded by `.gitignore`；未提交环境目录、缓存、日志、数据库或 secrets。
- 本任务未启动 CareerSim、未运行对局、未运行 baseline、未调用 provider/model。

## Known issues

- `uv python install 3.12` 下载完成后曾输出 managed minor-version link warning；随后 `uv python find 3.12`、解释器启动和虚拟环境创建均通过。
- `uv sync` 因缓存与目标目录不在同一文件系统，使用 full-copy fallback；依赖解析和 `pip check` 均通过。
- `career-emulator-bdci26` 是数据发行版，没有独立顶层 Python module；其发行版 metadata 与安装内容已核验。
