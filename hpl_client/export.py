"""Export only validated canonical public artifacts, never raw runtime files."""

import hashlib
import math
import json
import os
import re
import shutil
import zipfile
from datetime import datetime
from pathlib import Path

from scripts.hpl_evidence_writer import _KNOWN_SECRET_PATTERNS, _REQUIRED_MANIFEST_FIELDS
from scripts.hpl_public_evidence import project_cli_frame


ARTIFACTS = ("manifest.json", "trajectory.jsonl", "summary.json", "integrity.json")
README = b"CareerSim Human / HPL\nPublic participant evidence only. No DB, raw logs, dataset or credentials.\n"


def validate_content(content, run_id):
    manifest, summary, integrity = (
        json.loads(content[name]) for name in ("manifest.json", "summary.json", "integrity.json")
    )
    if any(item.get("run_id") != run_id for item in (manifest, summary, integrity)):
        raise ValueError("run identity mismatch")
    if set(manifest) - (_REQUIRED_MANIFEST_FIELDS | {"schema_version", "session_id", "run_status", "action_outcome"}):
        raise ValueError("unapproved export metadata")
    expected_hashes = {name: hashlib.sha256(content[name]).hexdigest() for name in ARTIFACTS[:-1]}
    if integrity.get("canonical_artifact_sha256") != expected_hashes:
        raise ValueError("canonical hash mismatch")
    if (
        integrity.get("public_only_validation") != "PASS"
        or integrity.get("secret_scan_status") != "PASS_PATTERN_SCAN_ONLY"
    ):
        raise ValueError("canonical validation failed")
    frames = [json.loads(line) for line in content["trajectory.jsonl"].splitlines()]
    sessions = set()
    for frame in frames:
        raw = dict(frame.get("observed_fact", {}))
        if "human_interpretation" in frame:
            raw["human_interpretation"] = frame["human_interpretation"]
        if project_cli_frame(raw) != frame:
            raise ValueError("non-public canonical frame")
        sessions.add(frame["observed_fact"]["state"]["session_id"])
    if not frames or sessions != {manifest.get("session_id")}:
        raise ValueError("session mismatch")
    if (
        summary.get("frame_count") != len(frames)
        or summary.get("session_consistency") != "PASS"
        or integrity.get("session_consistency") != "PASS"
    ):
        raise ValueError("inconsistent canonical summary")
    # Desktop manifests use portable paths. Do not export local machine paths/config.
    text = "\n".join(blob.decode("utf-8") for blob in content.values())
    if _KNOWN_SECRET_PATTERNS.search(text) or re.search(r"(?:[A-Za-z]:[\\/]|\\\\[^\\])", text):
        raise ValueError("secret pattern or machine path in evidence")
    if manifest.get("provider_used") is not False or integrity.get("transcript", {}).get("present"):
        raise ValueError("unsupported private runtime evidence")
    return manifest, frames


def verify_zip(path: Path, run_id: str):
    if path.is_symlink() or getattr(path, "is_junction", lambda: False)():
        raise ValueError("unsafe ZIP")
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        if len(names) != 5 or set(names) != {*ARTIFACTS, "README.txt"} or archive.testzip():
            raise ValueError("invalid ZIP contents")
        if archive.read("README.txt") != README:
            raise ValueError("invalid README")
        content = {name: archive.read(name) for name in ARTIFACTS}
    manifest, frames = validate_content(content, run_id)
    return manifest, frames, content


def safe_filename_part(value, default):
    return re.sub(r"[^\w-]", "_", str(value or ""))[:64].strip("_-") or default


def readable_filename(manifest, frames):
    final = frames[-1]["observed_fact"]
    score = final.get("final_result", {}).get("quantitative_score")
    score_text = f"{score:.2f}" if type(score) in (int, float) and math.isfinite(score) else "NA"
    level = safe_filename_part(final.get("state", {}).get("level"), "LNA")
    tag = safe_filename_part(manifest.get("human_tag"), "local")
    end = datetime.fromisoformat(manifest["ended_at"])
    if end.tzinfo:
        end = end.astimezone()
    return f"CareerSim-{tag}-Score{score_text}-{level}-{end:%Y%m%d-%H%M%S}.zip"


def export_run(root: Path) -> Path:
    root = Path(root)
    if not root.is_absolute() or root.is_symlink() or (root / "evidence").is_symlink():
        raise ValueError("unsafe evidence path")
    content = {}
    for name in ARTIFACTS:
        path = root / "evidence" / name
        if path.is_symlink() or not path.is_file():
            raise ValueError("missing or unsafe canonical artifact")
        content[name] = path.read_bytes()
    manifest, frames = validate_content(content, root.name)
    destination = root / "export"
    if destination.is_symlink():
        raise ValueError("unsafe export directory")
    destination.mkdir(exist_ok=True)
    base = destination / readable_filename(manifest, frames)
    suffix = 1
    while True:
        path = base if suffix == 1 else base.with_name(f"{base.stem}-{suffix}.zip")
        if path.is_symlink():
            raise ValueError("unsafe ZIP path")
        if path.exists():
            existing_manifest, _, existing = verify_zip(path, root.name)
            if existing_manifest == manifest and existing == content:
                return path
            suffix += 1
            continue
        try:
            stream = path.open("xb")
            break
        except FileExistsError:
            suffix += 1
    try:
        with stream:
            with zipfile.ZipFile(stream, "w", compression=zipfile.ZIP_DEFLATED) as archive:
                for name, blob in content.items():
                    archive.writestr(name, blob)
                archive.writestr("README.txt", README)
            stream.flush()
            os.fsync(stream.fileno())
        verify_zip(path, root.name)
    except Exception:
        path.unlink(missing_ok=True)  # Remove only the path created exclusively above.
        raise
    return path


def finalize_success(root, layout):
    """Finalize only this ended session; verify stable ZIP before any deletion."""
    from hpl_client.cleanup import assert_cleanup_target, cleanup_success

    assert_cleanup_target(root, layout)
    staged = json.loads((Path(root) / "staging" / "manifest.json").read_text(encoding="utf-8"))
    if staged.get("run_status") != "ENDED" or "action_outcome" in staged:
        raise ValueError("only a verified normal ended run can be finalized")
    source = export_run(root)
    manifest, _, _ = verify_zip(source, root.name)
    if manifest.get("run_status") != "ENDED":
        raise ValueError("only a normal ended run can be finalized")
    destination = layout.sandbox_root / "exports"
    assert_cleanup_target(root, layout, exports=destination)
    destination.mkdir(exist_ok=True)
    suffix = 1
    while True:
        name = source.name if suffix == 1 else f"{source.stem}-{suffix}.zip"
        final = destination / name
        try:
            stream = final.open("xb")
            break
        except FileExistsError:
            suffix += 1
    try:
        with stream, source.open("rb") as original:
            shutil.copyfileobj(original, stream)
            stream.flush()
            os.fsync(stream.fileno())
        verify_zip(final, root.name)
    except Exception:
        final.unlink(missing_ok=True)  # Only the file created exclusively above.
        raise
    try:
        cleanup_success(root, final, layout)
    except OSError:
        # Verified ZIP survives Windows file-lock/partial deletion failures.
        return final, "CLEANUP_PENDING"
    return final, "SUCCESSFULLY_FINALIZED_AND_EXPORTED"
