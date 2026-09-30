"""Narrow success-only deletion after a verified external public ZIP exists."""

import shutil
from pathlib import Path

from scripts.hpl_play import assert_isolated_run_root

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
