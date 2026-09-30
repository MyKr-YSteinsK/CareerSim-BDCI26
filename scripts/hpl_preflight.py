"""Build a no-write preflight plan for an isolated Human Play Lab runtime."""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import shutil
import sys
from importlib import metadata, util
from pathlib import Path
from typing import Any


EXPECTED_EMULATOR_VERSION = "1.0.1"
EXPECTED_DATA_VERSION = "1.0.0"
DATASET_SPLIT = "dev"
DATASET_PATHS = {
    "event_dir": "action_pool",
    "fixed_event_dir": "initialization_n_regular",
    "failure_conditions_dir": "failure_conditions",
    "salary_conditions_dir": "salary_conditions",
    "promotion_dir": "promotion",
    "talk_mechanism_dir": "talk_mechanism",
    "ending_score_dir": "ending_score",
}
REQUIRED_DATASET_RESOURCES = (
    "performance_score/config.data",
    "ending_score/config.data",
    "promotion/config.data",
    "promotion/levels.data",
    "promotion/event_level_change.data",
    "salary_conditions/config.data",
    "talk_mechanism/config.data",
    "talk_mechanism/narratives.data",
)


def dataset_inventory(root: Path) -> dict[str, Any]:
    """Hash opaque installed dataset bytes; never decode rules or gameplay state."""
    if root.is_symlink() or root.is_junction() or not root.is_dir():
        raise RuntimeError(f"Dataset must be a real local directory: {root}")
    files: dict[str, str] = {}
    directories: list[str] = []
    for path in sorted(root.rglob("*")):
        if path.is_symlink() or path.is_junction():
            raise RuntimeError(f"Dataset must not contain symlinks: {path}")
        relative = path.relative_to(root).as_posix()
        if path.is_file():
            files[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
        elif path.is_dir():
            directories.append(relative)
    if not files:
        raise RuntimeError(f"Dataset is empty: {root}")
    return {"files": files, "directories": directories}


def verify_dataset_mirror(source: Path, mirror: Path) -> dict[str, Any]:
    source_inventory = dataset_inventory(source)
    missing = [name for name in REQUIRED_DATASET_RESOURCES if name not in source_inventory["files"]]
    missing += [name for name in (*DATASET_PATHS.values(), "performance_score") if name not in source_inventory["directories"]]
    if missing:
        raise RuntimeError("Pinned Dev dataset is incomplete: " + ", ".join(missing))
    if dataset_inventory(mirror) != source_inventory:
        raise RuntimeError("Package-default dataset mirror differs from the complete pinned Dev dataset")
    encoded = json.dumps(source_inventory, sort_keys=True, separators=(",", ":")).encode()
    return {
        "status": "COMPLETE_BYTE_IDENTICAL_DEV_MIRROR",
        "file_count": len(source_inventory["files"]),
        "tree_sha256": hashlib.sha256(encoded).hexdigest(),
        "required_resources": list(REQUIRED_DATASET_RESOURCES),
        "performance_score_config": str(mirror / "performance_score" / "config.data"),
    }


def verify_distribution_dataset(source: Path) -> None:
    """Verify all Dev files against the installed pinned distribution RECORD."""
    inventory = dataset_inventory(source)
    recorded: dict[str, str] = {}
    for entry in metadata.distribution("career-emulator-bdci26").files or ():
        path = Path(entry.locate()).resolve()
        if not _is_within(path, source.resolve()):
            continue
        if entry.hash is None or entry.hash.mode != "sha256":
            raise RuntimeError(f"Dev dataset RECORD lacks SHA-256: {entry}")
        recorded[path.relative_to(source.resolve()).as_posix()] = entry.hash.value
    actual = {
        name: base64.urlsafe_b64encode(bytes.fromhex(digest)).decode().rstrip("=")
        for name, digest in inventory["files"].items()
    }
    if not recorded or recorded != actual:
        raise RuntimeError("Installed Dev dataset differs from pinned distribution RECORD")


def install_hpl_dataset_mirror() -> dict[str, Any]:
    """Copy the entire Dev tree only within the dedicated Human venv."""
    # Script lives in <workspace>/.local/worktrees/human-play-lab/scripts.
    expected_venv = Path(__file__).resolve().parents[4] / ".local" / "runtime" / "human-play-lab" / "venv"
    if expected_venv.resolve() != expected_venv.absolute():
        raise RuntimeError("HPL venv must not redirect through a symlink or junction")
    if Path(sys.prefix).resolve() != expected_venv.resolve():
        raise RuntimeError("Dataset mirror installation requires the dedicated HPL interpreter")
    if metadata.version("career-emulator") != EXPECTED_EMULATOR_VERSION or metadata.version(
        "career-emulator-bdci26"
    ) != EXPECTED_DATA_VERSION:
        raise RuntimeError("Dataset mirror installation requires the frozen HPL package versions")
    emulator = _package_root("career_emulator")
    data = _package_root("career_emulator_bdci26")
    for path in (emulator, data):
        if not _is_within(path, expected_venv.resolve()):
            raise RuntimeError("Dataset package resolves outside the dedicated HPL venv")
    source = data / DATASET_SPLIT / "dataset"
    target = emulator / "data" / "dataset"
    if not _is_within(target.parent.resolve(), expected_venv.resolve()):
        raise RuntimeError("Dataset mirror destination resolves outside the dedicated HPL venv")
    verify_distribution_dataset(source)
    if not target.exists() and not target.is_symlink():
        shutil.copytree(source, target)
    return verify_dataset_mirror(source, target)


def _package_root(module_name: str) -> Path:
    """Return an installed package root without importing that package."""
    spec = util.find_spec(module_name)
    if spec is None or spec.origin is None:
        raise RuntimeError(f"Installed package module not found: {module_name}")
    return Path(spec.origin).resolve().parent


def _is_within(path: Path, parent: Path) -> bool:
    """Return whether path is equal to or below parent."""
    try:
        path.relative_to(parent)
    except ValueError:
        return False
    return True


def _paths_overlap(left: Path, right: Path) -> bool:
    """Return whether either path contains the other."""
    return _is_within(left, right) or _is_within(right, left)


def build_preflight(runtime_root: Path | str) -> dict[str, Any]:
    """Describe the approved storage and dataset paths without creating or opening them."""
    requested_root = Path(runtime_root).expanduser()
    if not requested_root.is_absolute():
        raise ValueError("runtime_root must be an absolute path")
    if requested_root.is_symlink():
        raise ValueError("runtime_root must not be a symlink")

    root = requested_root.resolve(strict=False)
    if root.exists() and not root.is_dir():
        raise ValueError("runtime_root exists but is not a directory")

    emulator_version = metadata.version("career-emulator")
    data_version = metadata.version("career-emulator-bdci26")
    if emulator_version != EXPECTED_EMULATOR_VERSION:
        raise RuntimeError(f"Expected career-emulator=={EXPECTED_EMULATOR_VERSION}, found {emulator_version}")
    if data_version != EXPECTED_DATA_VERSION:
        raise RuntimeError(f"Expected career-emulator-bdci26=={EXPECTED_DATA_VERSION}, found {data_version}")

    emulator_root = _package_root("career_emulator")
    data_package_root = _package_root("career_emulator_bdci26")
    protected_roots = (emulator_root / "data", data_package_root)
    if any(_paths_overlap(root, protected.resolve(strict=False)) for protected in protected_roots):
        raise ValueError("runtime_root overlaps installed emulator or dataset package data")

    db_path = root / "career_emulator.sqlite3"
    log_dir = root / "logs"
    for target in (db_path, log_dir):
        if target.exists() or target.is_symlink():
            raise ValueError(f"runtime target already exists; choose a fresh runtime_root: {target}")
        if not _is_within(target.resolve(strict=False), root):
            raise ValueError(f"runtime target resolves outside runtime_root: {target}")

    dataset_root = data_package_root / DATASET_SPLIT / "dataset"
    if not dataset_root.is_dir():
        raise RuntimeError(f"Installed {DATASET_SPLIT} dataset is unavailable: {dataset_root}")
    data_paths = {name: (dataset_root / relative).resolve(strict=False) for name, relative in DATASET_PATHS.items()}
    missing_paths = [str(path) for path in data_paths.values() if not path.is_dir()]
    if missing_paths:
        raise RuntimeError("Installed dev dataset is missing required directories: " + ", ".join(missing_paths))

    current_default_dataset = emulator_root / "data" / "dataset"
    default_matches_dev = current_default_dataset.resolve(strict=False) == dataset_root.resolve(strict=False)
    verify_distribution_dataset(dataset_root)
    mirror_identity = verify_dataset_mirror(dataset_root, current_default_dataset)
    return {
        "mode": "dry_run_preflight",
        "execution": {
            "cli_launched": False,
            "game_started": False,
            "provider_called": False,
            "dataset_updated": False,
        },
        "package_identity": {
            "career-emulator": emulator_version,
            "career-emulator-bdci26": data_version,
        },
        "package_roots": {
            "career-emulator": str(emulator_root),
            "career-emulator-bdci26": str(data_package_root),
        },
        "runtime": {
            "root": str(root),
            "db_path": str(db_path),
            "log_dir": str(log_dir),
            "created": False,
            "environment_before_emulator_import": {
                "CAREER_EMULATOR_DB": str(db_path),
                "CAREER_EMULATOR_LOG_DIR": str(log_dir),
            },
        },
        "dataset": {
            "distribution": "career-emulator-bdci26",
            "version": data_version,
            "split": DATASET_SPLIT,
            "root": str(dataset_root.resolve()),
            "engine_paths": {name: str(path) for name, path in data_paths.items()},
            "current_default_path": str(current_default_dataset.resolve(strict=False)),
            "current_default_path_matches_dev": default_matches_dev,
            "current_default_identity": mirror_identity["status"],
            "distribution_record_verified": True,
            "default_mirror": mirror_identity,
        },
    }


def main() -> None:
    """Print the preflight plan; this command never launches the emulator."""
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--runtime-root", type=Path, help="Fresh absolute .local/runtime path")
    mode.add_argument("--install-hpl-mirror", action="store_true", help="Explicit local HPL dataset copy; no game or update")
    args = parser.parse_args()
    result = install_hpl_dataset_mirror() if args.install_hpl_mirror else build_preflight(args.runtime_root)
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
