"""Static identity of the HPL-local Flet Windows runtime; no download or launch."""

import hashlib
from pathlib import Path


def desktop_runtime_identity(venv: Path) -> dict:
    root = venv / "flet-desktop"
    archive = root / "flet-windows-1.0.1.zip"
    executable = root / "flet" / "flet.exe"
    if root.is_symlink() or not archive.is_file() or not executable.is_file():
        raise RuntimeError("HPL Flet desktop runtime is missing")
    hashes = {}
    for path in sorted(root.rglob("*")):
        if path.is_symlink() or getattr(path, "is_junction", lambda: False)():
            raise RuntimeError("HPL Flet runtime cannot contain links")
        if path.is_file():
            hashes[path.relative_to(root).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    identity = hashlib.sha256("\n".join(f"{name}:{digest}" for name, digest in hashes.items()).encode()).hexdigest()
    return {
        "version": "1.0.1",
        "root": str(root),
        "file_count": len(hashes),
        "tree_sha256": identity,
        "archive_sha256": hashes[archive.name],
    }
