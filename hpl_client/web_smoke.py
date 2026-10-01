"""HPL-05A single-attempt authorization and local operation timings."""

import json
import os
import time

from hpl_client.recorder import now
from hpl_client.web import WebApplication


class SingleRunWebApplication(WebApplication):
    def __init__(self, controller, evidence_root, factory):
        self.evidence_root = evidence_root
        self.receipt = evidence_root / "start-intent.json"
        self.timings = evidence_root / "operations.jsonl"
        evidence_root.mkdir(parents=True, exist_ok=True)

        def reserve(tag):
            # Exclusive durable intent precedes any engine construction/new_game.
            # Never delete it or release the attempt after uncertain failure.
            with self.receipt.open("x", encoding="utf-8") as stream:
                json.dump({"authorization": "HPL-05A", "reserved_at": now()}, stream)
                stream.flush()
                os.fsync(stream.fileno())
            adapter, recorder = factory(tag)
            recorder.manifest["authorization_id"] = "HPL-05A/USER_WEB_START_CLICK"
            self._audit({"event": "run_allocated", "run_id": recorder.root.name})
            return adapter, recorder

        controller._factory = reserve
        super().__init__(controller, fixture=False)

    def _audit(self, record):
        with self.timings.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps({"at": now(), **record}) + "\n")
            stream.flush()
            os.fsync(stream.fileno())

    def state(self):
        with self._lock:
            state = super().state()
            state["start_available"] = not self.receipt.exists()
            return state

    def operation(self, name, body):
        with self._lock:
            if name == "start" and self.receipt.exists():
                self.controller.rejection = "HPL-05A 的单局授权已使用，请返回 review，不得再次开局。"
                return False, "SINGLE_RUN_BUDGET_EXHAUSTED/NO_MUTATION"
            started = time.perf_counter()
            self._audit({"event": "operation_begin", "operation": name})
            accepted, status = super().operation(name, body)
            self._audit(
                {
                    "event": "operation_complete",
                    "operation": name,
                    "seconds": time.perf_counter() - started,
                    "accepted": accepted,
                    "status": status,
                    "phase": self.controller.phase,
                }
            )
            return accepted, status
