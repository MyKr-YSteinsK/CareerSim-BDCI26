"""Create and verify the portable HPL bundle without importing the game."""

from __future__ import annotations

import argparse
import base64
import hashlib
import importlib.metadata as metadata
import json
import platform
import re
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from shutil import copyfile


EXPECTED = {
    "career-emulator": "1.0.1",
    "career-emulator-bdci26": "1.0.0",
    "flet": "1.0.1",
    "flet-desktop": "1.0.1",
}
EXPECTED_DATASET_FILE_COUNT = 194
REQUIRED_RESOURCES = (
    "performance_score/config.data",
    "ending_score/config.data",
    "promotion/config.data",
    "promotion/levels.data",
    "promotion/event_level_change.data",
    "salary_conditions/config.data",
    "talk_mechanism/config.data",
    "talk_mechanism/narratives.data",
)
FLET_RUNTIME_ARCHIVE = "_internal/flet_desktop/app/flet-windows.zip"
FORBIDDEN_ENTRY_COMPONENTS = {
    ".git",
    ".github",
    ".env",
    ".env.example",
    "career_sim_runner",
    "candidate",
    "skills",
    "runner",
    "current_candidate.json",
    "runtime_manifest.json",
    "userdata",
    "forensic_hold",
    "transcript",
    "public_journal.jsonl",
    "technical_error.log",
    "career_emulator.sqlite3",
    "jiuwenswarm",
    "fastmcp",
    "gitcode_api",
}
FORBIDDEN_TEXT_MARKERS = (
    b"d:\\cs\\",
    b"d:/cs/",
    b".local\\worktrees\\human-play-lab",
    b".local/worktrees/human-play-lab",
    b".local\\runtime\\human-play-lab",
    b".local/runtime/human-play-lab",
    b"\\appdata\\roaming\\uv\\python\\",
    b"/appdata/roaming/uv/python/",
    b"career_sim_runner",
    b"current_candidate.json",
    b"runtime_manifest.json",
    b"jiuwenswarm",
    b"fastmcp",
    b"gitcode_api",
)
TEXT_SUFFIXES = {
    ".cfg",
    ".ini",
    ".json",
    ".py",
    ".spec",
    ".toml",
    ".txt",
    ".xml",
    ".yaml",
    ".yml",
}


def inventory(root: Path) -> dict[str, object]:
    if root.is_symlink() or not root.is_dir():
        raise ValueError(f"dataset root is not a real directory: {root}")
    files: dict[str, str] = {}
    directories: list[str] = []
    for path in sorted(root.rglob("*")):
        if path.is_symlink() or getattr(path, "is_junction", lambda: False)():
            raise ValueError(f"dataset contains a link: {path}")
        relative = path.relative_to(root).as_posix()
        if path.is_file():
            files[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
        elif path.is_dir():
            directories.append(relative)
    if not files:
        raise ValueError("dataset is empty")
    return {"files": files, "directories": directories}


def tree_hash(value: dict[str, object]) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _version(name: str) -> str:
    try:
        return metadata.version(name)
    except metadata.PackageNotFoundError as error:
        raise RuntimeError(f"required build distribution is unavailable: {name}") from error


def _license_files(site_packages: Path) -> list[tuple[str, Path]]:
    candidates = {
        "career-emulator": site_packages / "career_emulator-1.0.1.dist-info" / "licenses" / "LICENSE",
        "career-emulator-bdci26": site_packages / "career_emulator_bdci26-1.0.0.dist-info" / "licenses" / "LICENSE",
        "PyInstaller": site_packages / "pyinstaller-6.16.0.dist-info" / "licenses" / "COPYING.txt",
        "PyInstaller-hooks-contrib": site_packages / "pyinstaller_hooks_contrib-2026.8.dist-info" / "licenses" / "LICENSE",
    }
    return [(name, path) for name, path in candidates.items() if path.is_file()]


def _dataset_distribution_identity(source_inventory: dict[str, object]) -> dict[str, object]:
    distribution = metadata.distribution("career-emulator-bdci26")
    dataset_prefix = ("career_emulator_bdci26", "dev", "dataset")
    recorded: dict[str, tuple[str, int | None]] = {}
    for entry in distribution.files or ():
        parts = Path(str(entry).replace("\\", "/")).parts
        if parts[:3] != dataset_prefix or len(parts) == 3:
            continue
        relative = Path(*parts[3:]).as_posix()
        file_hash = entry.hash
        if file_hash is None or file_hash.mode != "sha256":
            raise ValueError(f"pinned Dev dataset file has no SHA256 RECORD identity: {relative}")
        recorded[relative] = (file_hash.value, entry.size)

    source_files = source_inventory["files"]
    if len(source_files) != EXPECTED_DATASET_FILE_COUNT:
        raise ValueError(f"pinned BDCI26 Dev dataset must contain {EXPECTED_DATASET_FILE_COUNT} files")
    if set(recorded) != set(source_files):
        raise ValueError("installed BDCI26 Dev dataset differs from its distribution RECORD file set")
    for relative, digest in source_files.items():
        expected_hash, expected_size = recorded[relative]
        actual_hash = base64.urlsafe_b64encode(bytes.fromhex(digest)).rstrip(b"=").decode("ascii")
        file_path = Path(distribution.locate_file(f"career_emulator_bdci26/dev/dataset/{relative}"))
        if actual_hash != expected_hash or (expected_size is not None and file_path.stat().st_size != expected_size):
            raise ValueError(f"installed BDCI26 Dev dataset file differs from distribution RECORD: {relative}")

    record_text = distribution.read_text("RECORD")
    if not record_text:
        raise ValueError("installed BDCI26 distribution RECORD is unavailable")
    return {
        "distribution": "career-emulator-bdci26",
        "version": distribution.version,
        "record_sha256": hashlib.sha256(record_text.encode("utf-8")).hexdigest(),
        "dataset_file_count": len(recorded),
    }


def create(args: argparse.Namespace) -> dict[str, object]:
    bundle = Path(args.bundle_root).resolve()
    source = Path(args.dataset_source).resolve()
    if not bundle.is_dir():
        raise ValueError(f"portable bundle directory is missing: {bundle}")
    source_inventory = inventory(source)
    dataset_identity = _dataset_distribution_identity(source_inventory)
    for resource in REQUIRED_RESOURCES:
        if resource not in source_inventory["files"]:
            raise ValueError(f"pinned Dev dataset is missing required resource: {resource}")
    packaged_dataset = bundle / "_internal" / "career_emulator" / "data" / "dataset"
    if not packaged_dataset.is_dir():
        raise ValueError(f"PyInstaller bundle did not include default dataset root: {packaged_dataset}")
    packaged_inventory = inventory(packaged_dataset)
    if packaged_inventory != source_inventory:
        raise ValueError("packaged dataset differs from the pinned Dev dataset")
    flet_archive = bundle / FLET_RUNTIME_ARCHIVE
    if not flet_archive.is_file():
        raise ValueError(f"PyInstaller bundle did not include the Flet runtime archive: {FLET_RUNTIME_ARCHIVE}")

    for name, version in EXPECTED.items():
        actual = _version(name)
        if actual != version:
            raise RuntimeError(f"expected {name}=={version}, found {actual}")

    licenses = bundle / "LICENSES"
    licenses.mkdir(exist_ok=True)
    notice_lines = [
        "CareerSim Human portable bundle - third-party notices",
        "",
        "The bundle includes the following frozen distributions:",
    ]
    for name, version in EXPECTED.items():
        notice_lines.append(f"- {name}=={version}")
    notice_lines.extend(
        [
            "",
            "career-emulator and career-emulator-bdci26 include their installed MIT license text in LICENSES/.",
            "PyInstaller includes its GPLv2-or-later license with the special distribution exception in LICENSES/.",
            "Flet metadata declares Apache-2.0; the installed wheel does not ship a license text, so the SPDX",
            "expression and official project URL are recorded in LICENSES/Flet-License-Notice.txt without inventing text.",
            "",
            "Official source URLs:",
            "https://github.com/Trenza1ore/CareerSim-BDCI26",
            "https://github.com/flet-dev/flet",
            "https://github.com/pyinstaller/pyinstaller",
        ]
    )
    (bundle / "THIRD_PARTY_NOTICES.txt").write_text("\n".join(notice_lines) + "\n", encoding="utf-8")
    for name, path in _license_files(Path(args.site_packages)):
        copyfile(path, licenses / f"{name.replace(' ', '_')}-LICENSE{path.suffix}")
    (licenses / "Flet-License-Notice.txt").write_text(
        "Flet 1.0.1, flet-desktop 1.0.1 and flet-cli 1.0.1 metadata declare SPDX Apache-2.0.\n"
        "The installed distributions do not contain a license text file; this notice records the explicit\n"
        "metadata limitation and official source: https://github.com/flet-dev/flet\n",
        encoding="utf-8",
    )

    source_commit = args.source_commit.strip()
    manifest = {
        "manifest_schema": "hpl-portable-build/v1",
        "runtime_mode": "PACKAGED_MODE",
        "app_version": "1.0.0",
        "hpl_source_commit": source_commit,
        "build_timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "build_os": platform.system(),
        "build_architecture": platform.machine(),
        "python_version": platform.python_version(),
        "flet_version": EXPECTED["flet"],
        "pyinstaller_version": metadata.version("pyinstaller"),
        "career_emulator_version": EXPECTED["career-emulator"],
        "career_emulator_bdci26_version": EXPECTED["career-emulator-bdci26"],
        "dataset": {
            "split": "dev",
            "source_distribution": dataset_identity,
            "file_count": len(source_inventory["files"]),
            "tree_sha256": tree_hash(source_inventory),
            "inventory": source_inventory,
            "default_root": "career_emulator/data/dataset",
            "required_resources": list(REQUIRED_RESOURCES),
            "performance_score_config": "career_emulator/data/dataset/performance_score/config.data",
        },
        "packaged_resources": {
            "default_dataset": "_internal/career_emulator/data/dataset",
            "game_engine_dataset_paths": "_internal/career_emulator/data/dataset/<official-directory>",
            "flet_desktop_runtime": FLET_RUNTIME_ARCHIVE,
            "flet_desktop_runtime_sha256": file_hash(flet_archive),
        },
        "build_command": args.build_command,
        "external_dependency_fallback": False,
        "network_startup": False,
        "artifact": {"sha256": "SEE_RELEASE_SIDECAR", "bytes": None},
    }
    (bundle / "BUILD_MANIFEST.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    readme = f"""CareerSim Human portable v{manifest['app_version']}\n\nDownload the Windows x64 ZIP, extract the complete folder, and double-click CareerSim Human.exe.\nNo Python, pip, Flet, project checkout, or network connection is required at startup or play.\n\nRuntime data is kept in the portable folder's UserData\\Runs, UserData\\Exports and UserData\\Diagnostics directories.\nExtract the complete folder to Desktop, D: or another ordinary writable location before starting it.\nThe application does not fall back to Documents or LocalAppData when UserData cannot be written.\n\nThe release archive SHA256 and byte size are recorded in the adjacent release sidecar and build output.\nThis unsigned research build may show a Microsoft Defender/SmartScreen unknown-publisher warning; verify\nthe published SHA256 and source before choosing to run it. Do not disable antivirus protection.\n\nFrozen runtime: career-emulator==1.0.1, career-emulator-bdci26==1.0.0, flet==1.0.1.\nBundled Dev dataset: {manifest['dataset']['file_count']} files, tree SHA256 {manifest['dataset']['tree_sha256']}.\n"""
    (bundle / "README.txt").write_text(readme, encoding="utf-8")
    return manifest


def _zip_root(names: list[str]) -> str:
    roots = {name.split("/", 1)[0] for name in names if name}
    if len(roots) != 1:
        raise ValueError("portable ZIP must contain exactly one top-level folder")
    return next(iter(roots))


def _forbidden_entry(name: str) -> bool:
    parts = [part.casefold() for part in name.replace("\\", "/").split("/") if part]
    return any(part in FORBIDDEN_ENTRY_COMPONENTS for part in parts)


def _check_forbidden_content(archive: zipfile.ZipFile, names: list[str]) -> None:
    for name in names:
        if _forbidden_entry(name):
            raise ValueError(f"portable ZIP contains forbidden path/config marker: {name}")
        # Distribution metadata may legitimately mention optional upstream
        # dependencies. It is not executable content and is not evidence that
        # those providers are bundled; the build strips their own dist-info.
        if ".dist-info/" in name.casefold() or Path(name).suffix.casefold() not in TEXT_SUFFIXES:
            continue
        blob = archive.read(name).lower()
        if any(marker in blob for marker in FORBIDDEN_TEXT_MARKERS):
            raise ValueError(f"portable ZIP contains forbidden path/config marker: {name}")


def _check_source_path_leaks(archive: zipfile.ZipFile, names: list[str]) -> None:
    for name in names:
        if name.endswith("/"):
            continue
        blob = archive.read(name).lower()
        if any(marker in blob for marker in FORBIDDEN_TEXT_MARKERS):
            raise ValueError(f"portable ZIP leaks a repository, HPL runtime or uv Python path: {name}")


def verify(archive_path: Path) -> dict[str, object]:
    archive_path = archive_path.resolve()
    if archive_path.is_symlink() or not archive_path.is_file():
        raise ValueError(f"portable ZIP is unavailable: {archive_path}")
    with zipfile.ZipFile(archive_path) as archive:
        names = archive.namelist()
        if len(names) != len(set(names)):
            raise ValueError("portable ZIP contains duplicate names")
        if any(name.startswith("/") or ".." in Path(name).parts for name in names):
            raise ValueError("portable ZIP contains a path traversal entry")
        root = _zip_root(names)
        required = {
            f"{root}/CareerSim Human.exe",
            f"{root}/BUILD_MANIFEST.json",
            f"{root}/README.txt",
        }
        if not required.issubset(names):
            raise ValueError(f"portable ZIP misses required entries: {sorted(required - set(names))}")
        if not any(name.startswith(f"{root}/_internal/") for name in names):
            raise ValueError("portable ZIP has no bundled _internal runtime")
        if f"{root}/{FLET_RUNTIME_ARCHIVE}" not in names:
            raise ValueError("portable ZIP has no bundled Flet desktop runtime archive")
        if not any(name.startswith(f"{root}/LICENSES/") for name in names):
            raise ValueError("portable ZIP has no LICENSES directory")
        manifest = json.loads(archive.read(f"{root}/BUILD_MANIFEST.json"))
        if manifest.get("runtime_mode") != "PACKAGED_MODE":
            raise ValueError("portable manifest is not PACKAGED_MODE")
        if manifest.get("python_version") != "3.12.10" or manifest.get("pyinstaller_version") != "6.16.0":
            raise ValueError("portable manifest does not use the accepted signed CPython/PyInstaller versions")
        for key, expected_version in (
            ("career_emulator_version", EXPECTED["career-emulator"]),
            ("career_emulator_bdci26_version", EXPECTED["career-emulator-bdci26"]),
            ("flet_version", EXPECTED["flet"]),
        ):
            if manifest.get(key) != expected_version:
                raise ValueError(f"portable manifest has an unexpected {key}")
        runtime_name = manifest.get("packaged_resources", {}).get("flet_desktop_runtime")
        if runtime_name != FLET_RUNTIME_ARCHIVE:
            raise ValueError("portable manifest does not identify the frozen Flet runtime path")
        flet_bytes = archive.read(f"{root}/{runtime_name}")
        if hashlib.sha256(flet_bytes).hexdigest() != manifest.get("packaged_resources", {}).get("flet_desktop_runtime_sha256"):
            raise ValueError("portable Flet runtime archive does not match BUILD_MANIFEST.json")
        dataset_prefix = f"{root}/_internal/career_emulator/data/dataset/"
        dataset_files = {
            name[len(dataset_prefix) :]: hashlib.sha256(archive.read(name)).hexdigest()
            for name in names
            if name.startswith(dataset_prefix) and not name.endswith("/")
        }
        dataset_directories = {
            name[len(dataset_prefix) :].rstrip("/")
            for name in names
            if name.startswith(dataset_prefix) and name.endswith("/") and name[len(dataset_prefix) :].rstrip("/")
        }
        for relative in dataset_files:
            parent = Path(relative).parent
            while parent.as_posix() != ".":
                dataset_directories.add(parent.as_posix())
                parent = parent.parent
        actual_inventory = {"files": dataset_files, "directories": sorted(dataset_directories)}
        dataset = manifest.get("dataset", {})
        source_identity = dataset.get("source_distribution", {})
        record_hash = source_identity.get("record_sha256", "")
        if (
            source_identity.get("distribution") != "career-emulator-bdci26"
            or source_identity.get("version") != EXPECTED["career-emulator-bdci26"]
            or source_identity.get("dataset_file_count") != EXPECTED_DATASET_FILE_COUNT
            or not re.fullmatch(r"[0-9a-f]{64}", record_hash)
        ):
            raise ValueError("portable manifest does not identify the complete pinned dataset distribution")
        expected_inventory = dataset.get("inventory", {})
        if actual_inventory != expected_inventory:
            raise ValueError("portable ZIP dataset does not match BUILD_MANIFEST.json")
        if len(dataset_files) != EXPECTED_DATASET_FILE_COUNT or len(dataset_files) != dataset.get("file_count") or tree_hash(actual_inventory) != dataset.get("tree_sha256"):
            raise ValueError("portable ZIP dataset tree identity does not match BUILD_MANIFEST.json")
        if dataset.get("required_resources") != list(REQUIRED_RESOURCES):
            raise ValueError("portable manifest does not declare the frozen Dev dataset resource set")
        if any(resource not in dataset_files for resource in REQUIRED_RESOURCES):
            raise ValueError("portable ZIP is missing a required default dataset resource")
        if dataset.get("performance_score_config") != "career_emulator/data/dataset/performance_score/config.data":
            raise ValueError("portable manifest does not identify the performance_score default resource")
        _check_source_path_leaks(archive, names)
        _check_forbidden_content(archive, names)
        return {
            "archive": str(archive_path),
            "bytes": archive_path.stat().st_size,
            "sha256": hashlib.sha256(archive_path.read_bytes()).hexdigest(),
            "root": root,
            "manifest": manifest,
            "entry_count": len(names),
            "dataset_file_count": len(dataset_files),
        }


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    create_parser = sub.add_parser("create")
    create_parser.add_argument("--bundle-root", required=True)
    create_parser.add_argument("--dataset-source", required=True)
    create_parser.add_argument("--site-packages", required=True)
    create_parser.add_argument("--source-commit", required=True)
    create_parser.add_argument("--build-command", required=True)
    verify_parser = sub.add_parser("verify")
    verify_parser.add_argument("archive")
    args = parser.parse_args()
    result = create(args) if args.command == "create" else verify(Path(args.archive))
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
