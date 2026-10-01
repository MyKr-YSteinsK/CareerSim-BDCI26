"""Narrow success-only deletion after a verified external public ZIP exists."""

import json
import shutil
from pathlib import Path

from hpl_client.path_contract import assert_isolated_run_root

from hpl_client.export import ARTIFACTS, verify_zip


HELD_RUN_ID = "47472aa8b73b4bf6847209f99a8abb39"


def _stable_exports(layout):
    return Path(getattr(layout, "exports_root", Path(layout.sandbox_root) / "exports"))


def _reject_links(path):
    for entry in (path, *path.parents):
        if entry.is_symlink() or getattr(entry, "is_junction", lambda: False)():
            raise ValueError("cleanup paths cannot traverse links")


def assert_cleanup_target(root, layout, *, exports=None):
    root = Path(root)
    if not root.is_absolute() or root.name == HELD_RUN_ID:
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
        if "FORENSIC_HOLD" in entry.name.upper():
            raise ValueError("run has an independent forensic hold")


def assert_discardable_active_run(root, layout, *, run_id):
    """Authorize deletion only for the current, still-active Human run."""
    root = Path(root)
    if root.name != run_id:
        raise ValueError("restart run identity does not match its storage root")
    assert_cleanup_target(root, layout)
    staged = root / "staging" / "manifest.json"
    if not staged.is_file():
        raise ValueError("active run receipt is missing")
    receipt = json.loads(staged.read_text(encoding="utf-8"))
    if receipt.get("run_id") != run_id:
        raise ValueError("active run receipt identity mismatch")
    if receipt.get("authorization_id") not in {
        "USER_GUI_START_CLICK",
        "USER_WEB_START_CLICK",
        "FIXTURE_NON_GAME",
    }:
        raise ValueError("only a user-started Human or synthetic fixture run can be discarded")
    if "run_status" in receipt or "action_outcome" in receipt:
        raise ValueError("ended or uncertain runs must be retained")
    if receipt.get("FORENSIC_HOLD") or receipt.get("forensic_hold"):
        raise ValueError("forensic-held runs must be retained")


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
    manifest, _, _ = verify_zip(archive, run_id)
    if manifest.get("run_status") != "ENDED" or "action_outcome" in manifest:
        raise ValueError("only this run's verified normal export can be discarded")


def discard_finalized_export(path, layout, *, run_id):
    """Delete this run's verified ZIP after the explicit restart confirmation."""
    archive = Path(path)
    assert_discardable_export(archive, layout, run_id=run_id)
    archive.unlink()


def cleanup_success(root, archive, layout):
    root, archive = Path(root), Path(archive)
    assert_cleanup_target(root, layout, exports=archive.parent)
    manifest, _, content = verify_zip(archive, root.name)
    staged = root / "staging" / "manifest.json"
    if not staged.is_file():
        raise ValueError("ended-run receipt is missing")
    import json

    run_receipt = json.loads(staged.read_text(encoding="utf-8"))
    if run_receipt.get("run_status") != "ENDED" or "action_outcome" in run_receipt:
        raise ValueError("run receipt does not authorize cleanup")
    if manifest.get("run_status") != "ENDED" or "action_outcome" in manifest:
        raise ValueError("active/technical/unknown runs cannot be cleaned")
    # Verify that the ZIP contains this run's exact canonical bytes, not merely
    # another self-consistent bundle with the same public session identifier.
    for name in ARTIFACTS:
        if (root / "evidence" / name).read_bytes() != content[name]:
            raise ValueError("ZIP does not preserve the canonical evidence")
    # Resolved absolute root is verified within the dedicated runs directory.
    shutil.rmtree(root.resolve(strict=True))
