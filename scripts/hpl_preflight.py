"""Build a no-write preflight plan for an isolated Human Play Lab runtime."""

from __future__ import annotations

import argparse
import json
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
            "current_default_identity": "PATH_MATCHES_PINNED_DEV" if default_matches_dev else "UNKNOWN",
        },
    }


def main() -> None:
    """Print the preflight plan; this command never launches the emulator."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runtime-root", type=Path, required=True, help="Fresh absolute .local/runtime path")
    args = parser.parse_args()
    print(json.dumps(build_preflight(args.runtime_root), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
