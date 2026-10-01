"""Narrow success-only deletion after a verified external public ZIP exists."""

import shutil
from pathlib import Path

from hpl_client.path_contract import assert_isolated_run_root

from hpl_client.export import verify_zip


def _stable_exports(layout):
    return Path(getattr(layout, "exports_root", Path(layout.sandbox_root) / "exports"))


def _reject_links(path):
    for entry in (path, *path.parents):
        if entry.is_symlink() or getattr(entry, "is_junction", lambda: False)():
            raise ValueError("cleanup paths cannot traverse links")


def assert_cleanup_target(root, layout, *, exports=None):
    root = Path(root)
    if not root.is_absolute():
        raise ValueError("protected or non-absolute cleanup target")
    assert_isolated_run_root(root, layout)
    if root.parent.resolve() != layout.runs_root.resolve():
        raise ValueError("cleanup requires a direct HPL run child")
    _reject_links(root)
    if exports is not None:
        _reject_links(exports)
        if exports.resolve() != _stable_exports(layout).resolve():
            raise ValueError("ZIP must be in stable HPL exports")
    for entry in root.rglob("*"):
        if entry.is_symlink() or getattr(entry, "is_junction", lambda: False)():
            raise ValueError("run contains linked material")


def assert_discardable_active_run(root, layout, *, run_id):
    """Limit confirmed restart deletion to the current Human run directory."""
    root = Path(root)
    if root.name != run_id:
        raise ValueError("restart run identity does not match its storage root")
    assert_cleanup_target(root, layout)


def discard_active_run(root, layout, *, run_id):
    """Delete the exact current active run after explicit user confirmation."""
    root = Path(root)
    assert_discardable_active_run(root, layout, run_id=run_id)
    shutil.rmtree(root.resolve(strict=True))


def assert_discardable_export(path, layout, *, run_id):
    """Authorize deleting only the verified export for this ended run."""
    archive = Path(path)
    exports = _stable_exports(layout)
    if not archive.is_absolute() or archive.parent.resolve() != exports.resolve():
        raise ValueError("restart export must be a direct child of the HPL exports directory")
    _reject_links(archive)


def discard_finalized_export(path, layout, *, run_id):
    """Delete this run's verified ZIP after the explicit restart confirmation."""
    archive = Path(path)
    assert_discardable_export(archive, layout, run_id=run_id)
    archive.unlink()


def cleanup_success(root, archive, layout):
    """Remove this run only after its external result ZIP verifies successfully."""
    root, archive = Path(root), Path(archive)
    assert_cleanup_target(root, layout, exports=archive.parent)
    verify_zip(archive, root.name)
    shutil.rmtree(root.resolve(strict=True))
