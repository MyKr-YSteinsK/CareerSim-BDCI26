"""Build the HPL-06 candidate from recorded official embed ZIP and HPL-05 closure."""

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import zipfile
from pathlib import Path

from scripts.hpl_evidence_writer import _KNOWN_SECRET_PATTERNS
from scripts.hpl_preflight import dataset_inventory, verify_dataset_mirror


EMBED_SHA256 = "4acbed6dd1c744b0376e3b1cf57ce906f9dc9e95e68824584c8099a63025a3c3"
EMBED_URL = "https://www.python.org/ftp/python/3.12.10/python-3.12.10-embed-amd64.zip"
APP_MODULES = (
    "__init__",
    "controller",
    "game_adapter",
    "models",
    "presentation",
    "recorder",
    "export",
    "cleanup",
    "fixtures",
    "web",
    "path_contract",
    "portable_web",
)
RUNTIME_SCRIPTS = ("__init__", "hpl_evidence_writer", "hpl_public_evidence")
LAUNCHER = """@echo off
setlocal
chcp 65001 >nul
set "PYTHONHOME="
set "PYTHONPATH="
set "VIRTUAL_ENV="
set "PYTHONDONTWRITEBYTECODE=1"
set "MSGPACK_PUREPYTHON="
if not exist "%~dp0Runtime\\python.exe" (
  echo 请先完整解压 ZIP，保留 Runtime 和 App 目录。
  pause
  exit /b 1
)
"%~dp0Runtime\\python.exe" -B -X utf8 "%~dp0App\\hpl_client\\portable_web.py" %*
set "result=%errorlevel%"
if not "%result%"=="0" (
  echo 程序未能正常启动。请截图并停止，不要关闭 Windows 安全功能。
  pause
)
exit /b %result%
"""
README = """CareerSim Human Web — Windows x64

1. 请先完整解压 ZIP，不要在压缩包内直接运行。
2. 放到桌面、D 盘等普通可写目录。
3. 双击「启动 CareerSim.cmd」，默认浏览器会自动打开本地页面。
4. 输入昵称后手动开始并选择行动；连接或行动结果未知时不要重复提交。
5. 玩完把 UserData\\Exports 中的结果 ZIP 发回给邀请你的朋友。
6. 不要修改 Runtime / App；本客户端无需联网、安装 Python 或管理员权限。
7. 如出现 Windows 安全提示或程序报错，请截图并停止，不要关闭安全功能。
"""


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def reject_path(path):
    if any(p.is_symlink() or p.is_junction() for p in (path, *path.parents)):
        raise ValueError("Build source/target cannot traverse links")


def scan(root):
    findings = []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(root).as_posix()
        if any(
            part.casefold() in {".git", ".github", ".env", "__pycache__", "tests", "test_final", "dev_final"}
            for part in path.relative_to(root).parts
        ):
            raise ValueError("Forbidden release path: " + relative)
        blob = path.read_bytes()
        text = blob.decode("utf-8", errors="ignore")
        path_scan_text = text
        if (
            relative == "Runtime/python312.dll"
            and digest(path) == "9a0e3435aaa680d868150f87ab3e388ad2eebc22f87e036155c7b4eda8cd2120"
        ):
            # Official ntpath.splitroot docstring example, confirmed in PSF DLL.
            path_scan_text = text.replace("C:/Users/Barney", "CPYTHON_DOCSTRING_EXAMPLE")
            findings.append(
                {"path": relative, "classification": "PSF ntpath docstring C:/Users/Barney, not a build path"}
            )
        if re.search(r"(?i)D:[\\/]CS|C:[\\/]Users[\\/]|\.codex|\.local[\\/]worktrees", path_scan_text):
            raise ValueError("Local source path leaked: " + relative)
        # Upstream untouched sources contain placeholder credential/HTTP token logic.
        # Record every lexical hit for review; credential-shaped values remain fatal.
        if re.search(r"(?:gh[pousr]_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9_-]{20,})", text):
            raise ValueError("Credential-shaped value: " + relative)
        tokens = sorted(set(re.findall(r"(?i)API_KEY|SECRET|TOKEN", text)))
        patterns = _KNOWN_SECRET_PATTERNS.findall(text)
        if tokens or patterns:
            findings.append({"path": relative, "tokens": tokens, "pattern_hits": patterns})
    return findings


def archive(root, destination):
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for path in sorted(root.rglob("*")):
            relative = "CareerSim-Human-Web/" + path.relative_to(root).as_posix()
            if path.is_dir():
                if not any(path.iterdir()):
                    z.writestr(zipfile.ZipInfo(relative + "/", (1980, 1, 1, 0, 0, 0)), b"")
                continue
            info = zipfile.ZipInfo(relative, (1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, path.read_bytes())
    with zipfile.ZipFile(destination) as z:
        if z.testzip():
            raise ValueError("Release ZIP checksum failed")


def build(worktree, sandbox, embed, output):
    for path in (worktree, sandbox, embed, output):
        reject_path(path)
    if digest(embed) != EMBED_SHA256:
        raise ValueError("Official Python embed source identity drift")
    if output.exists():
        raise ValueError("Refuse to replace an existing release build")
    source = sandbox / "local-web-client"
    identity = json.loads((source / "identity.json").read_text(encoding="utf-8"))
    closure = json.loads((sandbox / "msgpack-probe/copy-identity.json").read_text(encoding="utf-8"))
    root = output / "CareerSim-Human-Web"
    runtime = root / "Runtime"
    runtime.mkdir(parents=True)
    with zipfile.ZipFile(embed) as z:
        if any(Path(n).is_absolute() or ".." in Path(n).parts for n in z.namelist()):
            raise ValueError("Unsafe official embed archive")
        z.extractall(runtime)
    (runtime / "python312._pth").write_text("python312.zip\n.\nLib/site-packages\n../App\n", encoding="utf-8")
    site = runtime / "Lib/site-packages"
    omitted_tests = []
    for dist in closure:
        for entry in dist["files"]:
            relative = Path(entry["path"])
            if (
                relative.is_absolute()
                or ".." in relative.parts
                or relative.suffix.lower() in {".exe", ".dll", ".pyd", ".pyc"}
            ):
                raise ValueError("Unexpected closure resource")
            src = source / "venv/Lib/site-packages" / relative
            reject_path(src)
            if digest(src) != entry["sha256"]:
                raise ValueError("Frozen dependency source identity drift")
            if "tests" in relative.parts or relative.as_posix() == "anyio/pytest_plugin.py":
                omitted_tests.append(relative.as_posix())
                continue
            dst = site / relative
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src, dst)
    dev = site / "career_emulator_bdci26/dev/dataset"
    mirror = site / "career_emulator/data/dataset"
    shutil.copytree(dev, mirror)
    verified = verify_dataset_mirror(dev, mirror)
    if verified["file_count"] != 194 or verified["tree_sha256"] != identity["dataset"]["tree_sha256"]:
        raise ValueError("Frozen complete Dev dataset drift")
    for package, modules in (("hpl_client", APP_MODULES), ("scripts", RUNTIME_SCRIPTS)):
        for name in modules:
            dst = root / "App" / package / (name + ".py")
            dst.parent.mkdir(parents=True, exist_ok=True)
            src = worktree / package / (name + ".py")
            dst.write_bytes(src.read_bytes() if src.exists() else b"")
    shutil.copytree(worktree / "hpl_client/web_assets", root / "App/hpl_client/web_assets")
    (root / "启动 CareerSim.cmd").write_bytes(LAUNCHER.replace("\n", "\r\n").encode("utf-8"))
    (root / "README-使用说明.txt").write_text(README, encoding="utf-8-sig")
    for name in ("Runs", "Exports", "Diagnostics"):
        (root / "UserData" / name).mkdir(parents=True)
    commit = subprocess.check_output(["git", "-C", str(worktree), "rev-parse", "HEAD"], text=True).strip()
    package = {
        "version": "1.0.0",
        "source_commit": commit,
        "python": "3.12.10",
        "python_source": EMBED_URL,
        "python_source_sha256": EMBED_SHA256,
        "packages": identity["packages"],
        "omitted_upstream_tests": omitted_tests,
        "dataset_files": dataset_inventory(dev)["files"],
        "dataset_tree_sha256": verified["tree_sha256"],
        "files": {p.relative_to(root).as_posix(): digest(p) for p in sorted(root.rglob("*")) if p.is_file()},
    }
    (root / "App/package-manifest.json").write_text(json.dumps(package, indent=2, ensure_ascii=False), encoding="utf-8")
    findings = scan(root)
    target = output / "CareerSim-Human-Web-v1-Windows-x64.zip"
    archive(root, target)
    result = {
        "source_branch": "research/human-play-lab",
        "source_commit": commit,
        "source_files": {p: h for p, h in package["files"].items() if p.startswith("App/")},
        "zip": target.name,
        "zip_bytes": target.stat().st_size,
        "zip_sha256": digest(target),
        "python": "3.12.10",
        "python_source": EMBED_URL,
        "python_source_sha256": EMBED_SHA256,
        "packages": package["packages"],
        "dataset": {"file_count": 194, "tree_sha256": verified["tree_sha256"]},
        "top_level": sorted(p.name for p in root.iterdir()),
        "scan_findings": findings,
        "cmsgpack": "ABSENT",
        "hpl05a": "NOT_ACCEPTED",
        "decision": "VALIDATION_PENDING",
    }
    (output / "release-manifest.json").write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({k: result[k] for k in ("zip", "zip_bytes", "zip_sha256")}, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sandbox", required=True, type=Path)
    parser.add_argument("--embed", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    build(Path(__file__).resolve().parents[1], args.sandbox, args.embed, args.output)
