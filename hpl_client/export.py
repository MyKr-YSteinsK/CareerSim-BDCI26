"""Export only validated canonical public artifacts, never raw runtime files."""

import hashlib
import json
import re
import zipfile
from pathlib import Path

from scripts.hpl_evidence_writer import _KNOWN_SECRET_PATTERNS, _REQUIRED_MANIFEST_FIELDS
from scripts.hpl_public_evidence import project_cli_frame


ARTIFACTS = ("manifest.json", "trajectory.jsonl", "summary.json", "integrity.json")
README = b"CareerSim Human / HPL\nPublic participant evidence only. No DB, raw logs, dataset or credentials.\n"


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
    manifest, summary, integrity = (
        json.loads(content[name]) for name in ("manifest.json", "summary.json", "integrity.json")
    )
    if any(item.get("run_id") != root.name for item in (manifest, summary, integrity)):
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
    destination = root / "export"
    if destination.is_symlink():
        raise ValueError("unsafe export directory")
    destination.mkdir(exist_ok=True)
    tag = re.sub(r"[^\w-]", "_", manifest["human_tag"])[:64] or "local"
    path = destination / f"CareerSim-Human-{tag}-{root.name}.zip"
    if path.is_symlink():
        raise ValueError("unsafe ZIP path")
    temporary = path.with_suffix(".zip.tmp")
    if temporary.exists() or temporary.is_symlink():
        raise FileExistsError("export temporary file already exists")
    with zipfile.ZipFile(temporary, "x", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, blob in content.items():
            archive.writestr(name, blob)
        archive.writestr("README.txt", README)
    with zipfile.ZipFile(temporary) as archive:
        if set(archive.namelist()) != {*ARTIFACTS, "README.txt"} or archive.testzip():
            raise ValueError("invalid ZIP contents")
    temporary.replace(path)
    return path
