"""Durable public journal and existing canonical writer; never inspect runtime DB."""

import json
import os
import traceback
from datetime import datetime

from scripts.hpl_evidence_writer import write_run_evidence


def now():
    return datetime.now().astimezone().isoformat()


class RunRecorder:
    def __init__(self, root, manifest):
        self.root = root
        self.manifest = manifest
        self.frames = []
        self.finalized = False
        (root / "staging").mkdir(exist_ok=True)
        (root / "scratch").mkdir(exist_ok=True)
        (root / "staging" / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")

    def journal(self, kind, frame):
        with (self.root / "staging" / "public_journal.jsonl").open("a", encoding="utf-8") as stream:
            stream.write(json.dumps({"kind": kind, "at": now(), "public_frame": frame}, ensure_ascii=False) + "\n")
            stream.flush()
            os.fsync(stream.fileno())

    def transition(self, view, selection=None):
        if selection and self.frames:
            self.frames[-1]["human_selection"] = selection
            self.journal("selection", self.frames[-1])
        frame = view.facts
        self.frames.append(frame)
        self.manifest["session_id"] = frame["state"]["session_id"]
        self.journal("observation", frame)
        if view.phase == "ENDED":
            self.finish("ENDED")

    def submission(self, selection):
        self.frames[-1]["human_selection"] = selection
        self.journal("submission_intent", self.frames[-1])

    def finish(self, status, *, unknown=False):
        if self.finalized:
            return
        self.manifest.update(ended_at=now(), run_status=status)
        if unknown:
            self.manifest["action_outcome"] = "UNKNOWN_AFTER_TECHNICAL_FAILURE"
        staged = self.root / "staging" / "manifest.json"
        with staged.open("w", encoding="utf-8") as stream:
            json.dump(self.manifest, stream, ensure_ascii=False, sort_keys=True)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        write_run_evidence(self.root, self.manifest, self.frames)
        self.finalized = True

    def failure(self, error):
        # Local technical traceback is deliberately excluded from canonical export.
        (self.root / "scratch" / "technical_error.log").write_text(
            "".join(traceback.format_exception(error)), encoding="utf-8"
        )
        self.finish("TECHNICAL_FAILURE", unknown=True)
