"""Shared path and dataset wiring contracts; no simulator rules or development runtime."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any


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


@dataclass(frozen=True)
class HPLLayout:
    workspace_root: Path
    worktree_root: Path
    sandbox_root: Path

    @property
    def runs_root(self) -> Path:
        return self.sandbox_root / "runs"

    @property
    def environment_manifest_path(self) -> Path:
        return self.sandbox_root / "sandbox" / "environment_manifest.json"


def _path_key(path: Path) -> str:
    return os.path.normcase(str(path.resolve(strict=False)))


def _is_within(path: Path, parent: Path) -> bool:
    try:
        path.resolve(strict=False).relative_to(parent.resolve(strict=False))
    except ValueError:
        return False
    return True


def _paths_overlap(left: Path, right: Path) -> bool:
    return _is_within(left, right) or _is_within(right, left)


def protected_agent_paths(workspace_root: Path) -> list[Path]:
    paths = [
        workspace_root / ".venv",
        workspace_root / "configs" / "current_candidate.json",
        workspace_root / "configs" / "runtime_manifest.json",
        workspace_root / "skills",
        workspace_root / "career_sim_runner",
        workspace_root / ".career_sim_runner",
        Path.home() / ".jiuwenswarm-instances" / "career_emu",
    ]
    sibling_runtime_root = workspace_root / ".local" / "runtime"
    if sibling_runtime_root.is_dir():
        paths.extend(child for child in sibling_runtime_root.iterdir() if child.name.casefold() != "human-play-lab")
    return paths


def assert_isolated_run_root(run_root: Path, layout: HPLLayout) -> None:
    candidate = run_root.absolute()
    current = candidate
    while current != current.parent:
        if current.exists() and current.is_symlink():
            raise ValueError(f"run_root path contains a symlink: {current}")
        current = current.parent
    runs_root = layout.runs_root.resolve(strict=False)
    resolved_run = candidate.resolve(strict=False)
    if getattr(layout, "mode", None) == "WEB_PORTABLE":
        if resolved_run.parent != runs_root or candidate.name != resolved_run.name:
            raise ValueError("portable run must be a direct UserData/Runs child")
        if any(p.is_symlink() or p.is_junction() for p in (candidate, *candidate.parents)):
            raise ValueError("portable run cannot traverse links")
        return
    for protected in protected_agent_paths(layout.workspace_root):
        if _paths_overlap(resolved_run, protected):
            raise ValueError(f"run_root overlaps protected Agent path: {protected}")
    if not _is_within(resolved_run, runs_root) or _path_key(resolved_run) == _path_key(runs_root):
        raise ValueError("run_root must be a child of the HPL runs root")
    if _paths_overlap(resolved_run, layout.sandbox_root / "venv"):
        raise ValueError("run_root overlaps the dedicated HPL venv")


def engine_constructor_kwargs(engine_paths: dict[str, str], db_path: Path) -> dict[str, Any]:
    if set(engine_paths) != set(DATASET_PATHS):
        raise ValueError("pinned HPL dataset must provide exactly the seven official GameEngine directories")
    return {**{name: Path(value) for name, value in engine_paths.items()}, "db_path": db_path}
