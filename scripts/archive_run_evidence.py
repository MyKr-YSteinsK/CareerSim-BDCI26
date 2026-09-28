"""Copy explicitly named, scanned CareerSim evidence into an ignored dev archive."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path

if __package__:
    from .post_run_audit import SESSION, STAMP, file_identity, parse_offset, parse_time
else:
    from post_run_audit import SESSION, STAMP, file_identity, parse_offset, parse_time


CORE_NAMES = {
    "events": "events.jsonl",
    "transcript": "transcript.log",
    "score_report": "score_report.json",
    "runner_result": "runner-result.json",
    "post_run_summary": "post_run_summary.json",
}
DIAGNOSTIC_NAMES = {"llm": "llm-run.log", "runner": "runner-run.log", "service": "service-run.log", "context_engine": "context-engine-run.log"}
FORBIDDEN_SUFFIXES = {".db", ".sqlite", ".sqlite3", ".pem", ".key", ".p12", ".pfx"}
SECRET_PATTERNS = {
    "authorization_header": re.compile(r"\bauthorization\s*[:=]\s*(?:bearer|basic)\s+\S+", re.I),
    "cookie_header": re.compile(r"\b(?:set-cookie|cookie)\s*:\s*\S+", re.I),
    "credential_assignment": re.compile(r"\b(?:api[_-]?key|access[_-]?token|client[_-]?secret|secret[_-]?key|password)\b[\"']?\s*[:=]\s*[\"']?[^\s\"',}]{4,}", re.I),
    "private_key_block": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "provider_token": re.compile(r"\bsk-[A-Za-z0-9_-]{12,}\b"),
}


class UnsafeEvidence(ValueError):
    """An artifact cannot safely enter the tracked dev archive."""


def _pairs(values: list[str], allowed: dict[str, str], label: str) -> dict[str, str]:
    parsed: dict[str, str] = {}
    for value in values:
        kind, sep, path = value.partition("=")
        if not sep or kind not in allowed or not path or kind in parsed:
            raise ValueError(f"invalid or repeated {label}: expected KIND=PATH with a supported KIND")
        parsed[kind] = path
    return parsed


def _source_file(source_dir: Path, raw_name: str) -> Path:
    candidate = source_dir / raw_name
    source = candidate.resolve()
    if candidate.is_symlink() or not source.is_relative_to(source_dir) or not source.is_file():
        raise UnsafeEvidence("source must be a regular file within --source-dir")
    if source.name.startswith(".env") or source.suffix.lower() in FORBIDDEN_SUFFIXES:
        raise UnsafeEvidence("forbidden source file type")
    return source


def _scan(path: Path) -> None:
    if path.stat().st_size > 128 * 1024 * 1024:
        raise UnsafeEvidence("artifact exceeds the bounded 128 MiB scan limit")
    try:
        with path.open(encoding="utf-8") as handle:
            for line_number, line in enumerate(handle, 1):
                for label, pattern in SECRET_PATTERNS.items():
                    if pattern.search(line):
                        raise UnsafeEvidence(f"{path.name}: {label} at line {line_number}; content withheld")
    except UnicodeDecodeError as exc:
        raise UnsafeEvidence(f"{path.name}: not UTF-8 text; sanitize before archiving") from exc


def _check_core_sessions(files: dict[str, Path]) -> None:
    """Refuse obvious cross-session contamination in the two raw core streams."""
    markers: set[str] = set()
    for kind in ("events", "transcript"):
        path = files.get(kind)
        if path is None:
            continue
        if path.stat().st_size > 128 * 1024 * 1024:
            raise UnsafeEvidence(f"{kind} exceeds the bounded 128 MiB scan limit")
        found: set[str] = set()
        with path.open(encoding="utf-8") as handle:
            for line in handle:
                found.update(value.lower() for value in SESSION.findall(line))
                if len(found) > 1:
                    raise UnsafeEvidence(f"{kind} contains multiple session markers; sanitize run scope before archiving")
        markers.update(found)
        if len(markers) > 1:
            raise UnsafeEvidence("core artifact session markers disagree; sanitize run scope before archiving")


def _slice_log(source: Path, target: Path, start: datetime, end: datetime, offset: timezone | None) -> None:
    current: datetime | None = None
    seen_stamp = False
    written = 0
    with source.open(encoding="utf-8") as reader, target.open("w", encoding="utf-8", newline="\n") as writer:
        for line in reader:
            stamp = STAMP.search(line)
            if stamp:
                seen_stamp = True
                current = parse_time(stamp[1], offset)
                if current is None:
                    raise UnsafeEvidence("diagnostic log has naive timestamps without --log-utc-offset")
            if current is not None and start <= current <= end:
                writer.write(line)
                written += 1
    if not seen_stamp or not written:
        raise UnsafeEvidence("diagnostic log has no timestamped lines inside the run window")


def archive(
    repo_root: Path,
    source_dir: Path,
    run_id: str,
    core: dict[str, str],
    diagnostic: dict[str, str],
    start_text: str | None = None,
    end_text: str | None = None,
    log_offset_text: str | None = None,
    stage: bool = False,
) -> Path:
    """Build one new archive; never overwrite a previous run or stage an unsafe file."""
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,79}", run_id):
        raise ValueError("run-id must be 1-80 safe letters, digits, underscore or hyphen")
    if not core:
        raise ValueError("at least one explicit core artifact is required")
    if set(core) - CORE_NAMES.keys() or set(diagnostic) - DIAGNOSTIC_NAMES.keys():
        raise ValueError("unsupported artifact kind")
    if diagnostic and (not start_text or not end_text):
        raise ValueError("diagnostic logs require an explicit timezone-aware --run-start and --run-end")
    start = parse_time(start_text) if start_text else None
    end = parse_time(end_text) if end_text else None
    if diagnostic and (start is None or end is None or start > end):
        raise ValueError("invalid diagnostic run window")
    offset = parse_offset(log_offset_text)
    repo_root = repo_root.resolve()
    source_dir = source_dir.resolve()
    dest = repo_root / "artifacts" / "dev-runs" / run_id
    if dest.exists():
        raise FileExistsError("run archive already exists; preserve its evidence identity")
    source_files = {kind: _source_file(source_dir, name) for kind, name in core.items()}
    diagnostic_files = {kind: _source_file(source_dir, name) for kind, name in diagnostic.items()}
    _check_core_sessions(source_files)
    scratch = repo_root / ".local" / "scratch" / "archive-run-evidence"
    scratch.mkdir(parents=True, exist_ok=True)
    temp = Path(tempfile.mkdtemp(prefix="pending-", dir=scratch))
    try:
        for kind, source in source_files.items():
            shutil.copyfile(source, temp / CORE_NAMES[kind])
        for kind, source in diagnostic_files.items():
            assert start is not None and end is not None
            _slice_log(source, temp / DIAGNOSTIC_NAMES[kind], start, end, offset)
        members = sorted(path for path in temp.iterdir() if path.is_file())
        for path in members:
            _scan(path)
        manifest = {
            "schema_version": 1,
            "run_id": run_id,
            "run_window_utc": {"start": start.isoformat() if start else "UNKNOWN", "end": end.isoformat() if end else "UNKNOWN"},
            "artifacts": [dict(category="diagnostic" if path.name in DIAGNOSTIC_NAMES.values() else "core", **file_identity(path)) for path in members],
        }
        manifest_path = temp / "evidence-manifest.json"
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
        _scan(manifest_path)
        dest.parent.mkdir(parents=True, exist_ok=True)
        os.replace(temp, dest)
        if stage:
            relpaths = [(dest / name).relative_to(repo_root).as_posix() for name in sorted(path.name for path in dest.iterdir())]
            subprocess.run(["git", "-C", str(repo_root), "add", "-f", "--", *relpaths], check=True, capture_output=True, text=True)
        return dest
    finally:
        if temp.exists():
            shutil.rmtree(temp)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--source-dir", type=Path, required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--core", action="append", default=[], metavar="KIND=PATH")
    parser.add_argument("--diagnostic", action="append", default=[], metavar="KIND=PATH")
    parser.add_argument("--run-start", help="timezone-aware ISO timestamp, required with diagnostics")
    parser.add_argument("--run-end", help="timezone-aware ISO timestamp, required with diagnostics")
    parser.add_argument("--log-utc-offset", help="offset for naive log timestamps, e.g. +08:00")
    parser.add_argument("--stage", action="store_true", help="force-add only scanned output files")
    args = parser.parse_args()
    try:
        dest = archive(args.repo_root, args.source_dir, args.run_id, _pairs(args.core, CORE_NAMES, "core"), _pairs(args.diagnostic, DIAGNOSTIC_NAMES, "diagnostic"), args.run_start, args.run_end, args.log_utc_offset, args.stage)
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        parser.error(str(exc))
    print(dest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
