"""Thin adapter over the installed 1.0.1 async API, with no rules or DB reader."""

from scripts.hpl_public_evidence import (
    PUBLIC_CHOICE_FIELDS,
    PUBLIC_EVENT_FIELDS,
    PUBLIC_RESULT_FIELDS,
    PUBLIC_STATE_FIELDS,
    project_cli_frame,
)

from hpl_client.models import PublicGameView


def safe_text(name: str, value: str) -> str:
    # Preserve allowed handbook paragraphs while removing forbidden-looking lines.
    return "\n".join(line for line in value.splitlines() if name in project_cli_frame({name: line})["observed_fact"])


class PublicGameAdapter:
    def __init__(self, engine, run_id: str):
        self._engine = engine
        self.run_id = run_id
        self._session_id = None
        self._revision = 0
        self._handbook = ""
        self._choices = set()

    async def start(self) -> PublicGameView:
        receipt = await self._engine.new_game()
        if receipt.error or not isinstance(receipt.session_id, str) or not receipt.session_id:
            raise RuntimeError("new_game failed")
        self._session_id = receipt.session_id
        self._handbook = safe_text("handbook", await self._engine.enrollment_handbook())
        return await self._observe()

    async def act(self, choice: int) -> PublicGameView:
        if type(choice) is not int or choice not in self._choices:
            raise ValueError("choice is not in the current public observation")
        receipt = await self._engine.take_action(self._session_id, choice, notes="")
        if not receipt.success or receipt.error:
            raise RuntimeError("take_action did not return success")
        return await self._observe()

    def close_for_discard(self) -> None:
        """Release the installed engine's per-session file logger before run deletion."""
        if self._session_id is None or not type(self._engine).__module__.startswith("career_emulator."):
            return
        # career-emulator 1.0.1 opens SQLite connections per operation. Its cached
        # session logger is the only long-lived run file handle and has this close hook.
        from career_emulator.storage import _close_session_logger

        _close_session_logger(self._session_id)

    async def _observe(self) -> PublicGameView:
        raw = await self._engine.observe(self._session_id)
        current = raw.current_state
        if current.get("session_id") != self._session_id:
            raise RuntimeError("observe session mismatch")
        status = current.get("status", {})
        time = current.get("time", {})
        state = {key: status[key] for key in PUBLIC_STATE_FIELDS if key in status}
        for public, internal in (("month", "current_month"), ("quarter", "current_quarter"), ("year", "current_year")):
            if internal in time:
                state[public] = time[internal]
        state["session_id"] = self._session_id
        if not {"month", "level", "energy"}.issubset(state):
            raise RuntimeError("observe lacks public state")
        frame = {"state": state, "handbook": self._handbook, "choices": []}
        if raw.current_event:
            frame["event"] = {k: v for k, v in raw.current_event.items() if k in PUBLIC_EVENT_FIELDS}
        frame["choices"] = [{k: v for k, v in item.items() if k in PUBLIC_CHOICE_FIELDS} for item in raw.choices]
        if raw.warning:
            frame["warning"] = safe_text("warning", raw.warning)
        if raw.ending_score:
            frame["final_result"] = {k: v for k, v in raw.ending_score.items() if k in PUBLIC_RESULT_FIELDS}
            frame["final_result"]["outcome"] = (
                "48-month completion" if raw.ending_score.get("completed") else "Early elimination"
            )
        projection = project_cli_frame(frame)
        facts = projection["observed_fact"]
        if facts.get("choices") and any(
            type(c.get("choice")) is not int or not isinstance(c.get("action"), str) for c in facts["choices"]
        ):
            raise RuntimeError("invalid public choices")
        # Optional public text can contain excluded terms. Projection already
        # omits those fields; this must not turn a successful action into failure.
        self._choices = {c["choice"] for c in facts["choices"]}
        if len(self._choices) != len(facts["choices"]):
            raise RuntimeError("duplicate public choice IDs")
        self._revision += 1
        phase = "ENDED" if not facts["choices"] else "ACTIVE"
        return PublicGameView(self.run_id, self._revision, phase, projection)
