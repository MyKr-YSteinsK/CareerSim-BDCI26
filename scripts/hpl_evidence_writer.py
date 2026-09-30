"""Write canonical Human Play Lab evidence from public CLI frames only."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

from scripts.hpl_public_evidence import SCHEMA_VERSION, project_cli_frame


MANIFEST_SCHEMA_VERSION = "hpl-run-manifest/v1"
TRAJECTORY_SCHEMA_VERSION = "hpl-run-trajectory/v1"
SUMMARY_SCHEMA_VERSION = "hpl-run-summary/v1"
INTEGRITY_SCHEMA_VERSION = "hpl-run-integrity/v1"
_REQUIRED_MANIFEST_FIELDS = frozenset(
    {
        "run_id",
        "authorization_id",
        "human_tag",
        "started_at",
        "ended_at",
        "hpl_commit",
        "launcher_version",
        "python_version",
        "career_emulator_version",
        "career_emulator_bdci26_version",
        "dataset_source",
        "dataset_split",
        "dataset_root",
        "hpl_venv_root",
        "hpl_runtime_root",
        "provider_used",
        "provider_evidence_basis",
        "public_evidence_schema_version",
    }
)
_KNOWN_SECRET_PATTERNS = re.compile(
    r"(?i)(?:api[_-]?key\s*[:=]\s*\S+|"
    r"authorization\s*:\s*(?:bearer|basic)\s+\S+|"
    r"gitcode_access_token\s*[:=]\s*\S+|"
    r"(?:gh[pousr]_[A-Za-z0-9]{16,}|sk-[A-Za-z0-9_-]{16,}))"
)


def _json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n").encode(
        "utf-8"
    )


def _sha256(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def _validate_manifest(manifest: dict[str, Any]) -> dict[str, Any]:
    missing = sorted(_REQUIRED_MANIFEST_FIELDS - manifest.keys())
    if missing:
        raise ValueError("manifest is missing required fields: " + ", ".join(missing))
    empty = sorted(
        name
        for name in _REQUIRED_MANIFEST_FIELDS - {"provider_used", "provider_evidence_basis", "public_evidence_schema_version"}
        if not isinstance(manifest[name], str) or not manifest[name].strip()
    )
    if empty:
        raise ValueError("manifest fields must be non-empty strings: " + ", ".join(empty))
    if not isinstance(manifest["provider_used"], bool):
        raise ValueError("provider_used must be explicitly supplied as a boolean")
    if not manifest["provider_evidence_basis"]:
        raise ValueError("provider_evidence_basis must explain the validated runtime identity")
    if manifest["public_evidence_schema_version"] != SCHEMA_VERSION:
        raise ValueError(f"public_evidence_schema_version must be {SCHEMA_VERSION}")
    result = dict(manifest)
    result["schema_version"] = MANIFEST_SCHEMA_VERSION
    return result


def _session_consistency(manifest: dict[str, Any], frames: list[dict[str, Any]]) -> str:
    observed = {
        state["session_id"]
        for frame in frames
        if isinstance((state := frame.get("observed_fact", {}).get("state")), dict)
        and isinstance(state.get("session_id"), str)
    }
    expected = manifest.get("session_id")
    if expected and observed == {expected}:
        return "PASS"
    if not expected and not observed:
        return "UNKNOWN"
    return "FAIL"


def write_run_evidence(
    run_root: Path | str,
    manifest: dict[str, Any],
    public_frames: list[dict[str, Any]],
    transcript_path: Path | str | None = None,
) -> dict[str, Any]:
    """Project frames through the public allowlist and create deterministic evidence files.

    This writer accepts participant-facing frames only. It has no simulator or database reader.
    Existing canonical artifacts are never overwritten.
    """
    root = Path(run_root).expanduser()
    if root.is_symlink() or not root.is_absolute():
        raise ValueError("run_root must be an absolute, non-symlink path")
    root = root.resolve(strict=True)
    if not root.is_dir():
        raise ValueError("run_root must be a directory")

    canonical_manifest = _validate_manifest(manifest)
    if canonical_manifest["run_id"] != root.name:
        raise ValueError("manifest run_id must match the HPL run-root name")
    projected_frames = [project_cli_frame(frame) for frame in public_frames]
    trajectory = b"".join(_json_bytes(frame) for frame in projected_frames)
    summary = {
        "schema_version": SUMMARY_SCHEMA_VERSION,
        "run_id": canonical_manifest["run_id"],
        "frame_count": len(projected_frames),
        "public_status": (
            "PUBLIC_FIELDS_ALLOWLISTED"
            if projected_frames and all(frame["public_status"] == "PUBLIC_FIELDS_ALLOWLISTED" for frame in projected_frames)
            else "PUBLIC_STATUS_UNKNOWN"
        ),
        "unknown_path_count": sum(len(frame["unknown_fields"]) for frame in projected_frames),
        "session_consistency": _session_consistency(canonical_manifest, projected_frames),
    }

    evidence_dir = root / "evidence"
    if evidence_dir.is_symlink():
        raise ValueError("evidence directory must not be a symlink")
    evidence_dir.mkdir(exist_ok=True)
    paths = {
        "manifest.json": evidence_dir / "manifest.json",
        "trajectory.jsonl": evidence_dir / "trajectory.jsonl",
        "summary.json": evidence_dir / "summary.json",
        "integrity.json": evidence_dir / "integrity.json",
    }
    if any(path.exists() or path.is_symlink() for path in paths.values()):
        raise FileExistsError("canonical evidence already exists; refusing to overwrite it")

    content = {
        "manifest.json": _json_bytes(canonical_manifest),
        "trajectory.jsonl": trajectory,
        "summary.json": _json_bytes(summary),
    }
    secret_scan = "PASS_PATTERN_SCAN_ONLY"
    if any(_KNOWN_SECRET_PATTERNS.search(blob.decode("utf-8")) for blob in content.values()):
        secret_scan = "FAIL_KNOWN_PATTERN"
    public_only = all(
        "human_interpretation" not in frame["observed_fact"]
        and set(frame).issubset(
            {"schema_version", "public_status", "observed_fact", "unknown_fields", "human_interpretation"}
        )
        for frame in projected_frames
    )

    transcript_info: dict[str, Any] = {"present": False, "sha256": None, "path": None}
    if transcript_path is not None:
        transcript = Path(transcript_path).expanduser().resolve(strict=True)
        if not transcript.is_file() or not transcript.is_relative_to(root):
            raise ValueError("transcript must be a file inside run_root")
        transcript_info = {
            "present": True,
            "path": str(transcript.relative_to(root)).replace("\\", "/"),
            "sha256": _sha256(transcript.read_bytes()),
        }

    integrity = {
        "schema_version": INTEGRITY_SCHEMA_VERSION,
        "run_id": canonical_manifest["run_id"],
        "canonical_artifact_sha256": {name: _sha256(blob) for name, blob in sorted(content.items())},
        "session_consistency": summary["session_consistency"],
        "public_only_validation": "PASS" if public_only else "FAIL",
        "secret_scan_status": secret_scan,
        "transcript": transcript_info,
    }
    if not public_only or secret_scan.startswith("FAIL"):
        raise ValueError("canonical evidence failed public-only or known-pattern secret validation")
    content["integrity.json"] = _json_bytes(integrity)

    for name, blob in content.items():
        paths[name].write_bytes(blob)
    return integrity
