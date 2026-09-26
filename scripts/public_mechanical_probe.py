"""Small offline public-state mechanics for future CareerSim probes.

No MCP, Runner, provider, or simulator dependency is imported here. A future
live task may inject a client implementing ``PublicMCPClient``.
"""

from __future__ import annotations

import json
import math
from collections.abc import Mapping, Sequence
from dataclasses import asdict, dataclass, field, replace
from typing import Any, Literal, Protocol


PublicScalar = int | float | str | bool | None
ProgressDirection = Literal["increase", "decrease", "change"]
DecisionStatus = Literal["ACTION", "DEFER", "UNSUPPORTED"]
ProgressStatus = Literal["ADVANCING", "NO_PROGRESS", "UNKNOWN"]
StructuralContext = Literal["ENERGY", "MAIN", "UNKNOWN_CONTEXT"]
ChoiceClass = Literal["GROWTH", "RESTORATIVE", "UNKNOWN"]
PublicRisk = Literal["MATERIAL", "NONE", "UNKNOWN"]

_TOP = {"session_id", "current_state", "current_event", "choices", "events", "ending_score"}
_STATE = {"session_id", "time", "status", "simulation_flags"}
_TIME = {"current_month", "current_quarter", "current_year"}
_FLAGS = {"alive", "failed", "failure_reason"}
_PUBLIC_STATUS = {"level", "health", "dignity", "skill", "network", "output", "wealth", "energy", "duration_in_level"}
_EVENT = {"title", "description"}
_CHOICE = {"choice", "action", "description"}

# These are public participant-facing action labels, not event/title rules.
# Keep the sets deliberately small: an unrecognised label remains unknown.
_ENERGY_LABELS = frozenset(
    {"准备汇报材料", "健康恢复", "人脉维护", "高强度工作", "处理历史埋雷", "心理修复"}
)
_MAIN_LABELS = frozenset({"申请关键项目", "低调避险"})
_GROWTH_LABELS = frozenset({"准备汇报材料", "人脉维护", "高强度工作", "申请关键项目"})
_RESTORATIVE_LABELS = frozenset({"健康恢复", "处理历史埋雷", "心理修复", "低调避险"})


def _scalar(value: Any) -> bool:
    return value is None or isinstance(value, (str, bool, int)) or (
        isinstance(value, float) and math.isfinite(value)
    )


def _number(value: Any) -> int | float | None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    return value if math.isfinite(value) else None


def _int(value: Any) -> int | None:
    return value if isinstance(value, int) and not isinstance(value, bool) else None


def _text(value: Any) -> str:
    return value if isinstance(value, str) else ""


def _mapping(value: Any, name: str, ignored: set[str]) -> Mapping[str, Any]:
    if isinstance(value, Mapping):
        return value
    if value is not None:
        ignored.add(name)
    return {}


@dataclass(frozen=True)
class PublicChoice:
    choice: int
    action: str = ""
    description: str = ""


@dataclass(frozen=True)
class PublicTime:
    current_month: int | None = None
    current_quarter: int | None = None
    current_year: int | None = None


@dataclass(frozen=True)
class PublicEvent:
    title: str = ""
    description: str = ""


@dataclass(frozen=True)
class PublicSnapshot:
    """Strict participant-visible projection; unknown values are discarded."""

    session_id: str | None
    time: PublicTime
    status: Mapping[str, PublicScalar] = field(default_factory=dict)
    event: PublicEvent = field(default_factory=PublicEvent)
    choices: tuple[PublicChoice, ...] = ()
    public_feed: str = ""
    alive: bool | None = None
    failed: bool | None = None
    ignored_fields: tuple[str, ...] = ()
    # This is an explicit annotation from a future public adapter. The probe
    # never infers it from titles, descriptions, or keyword taxonomies.
    material_risk: PublicRisk = "UNKNOWN"

    @property
    def terminal(self) -> bool | None:
        if self.alive is False or self.failed is True:
            return True
        if self.alive is True and self.failed is False:
            return False
        return None


def project_public_snapshot(response: Mapping[str, Any]) -> PublicSnapshot:
    """Project only the public observe contract; unknown values never reach policy."""

    if not isinstance(response, Mapping):
        raise TypeError("observe response must be a mapping")
    ignored = {str(key) for key in response if key not in _TOP}
    state = _mapping(response.get("current_state"), "current_state", ignored)
    ignored.update(f"current_state.{key}" for key in state if key not in _STATE)

    time = _mapping(state.get("time"), "current_state.time", ignored)
    ignored.update(f"current_state.time.{key}" for key in time if key not in _TIME)
    public_time = PublicTime(_int(time.get("current_month")), _int(time.get("current_quarter")), _int(time.get("current_year")))

    status: dict[str, PublicScalar] = {}
    raw_status = _mapping(state.get("status"), "current_state.status", ignored)
    for key, value in raw_status.items():
        name = str(key)
        if name in _PUBLIC_STATUS and _scalar(value):
            status[name] = value
        else:
            ignored.add(f"current_state.status.{name}")

    flags = _mapping(state.get("simulation_flags"), "current_state.simulation_flags", ignored)
    ignored.update(f"current_state.simulation_flags.{key}" for key in flags if key not in _FLAGS)
    alive = flags.get("alive") if isinstance(flags.get("alive"), bool) else None
    failed = flags.get("failed") if isinstance(flags.get("failed"), bool) else None

    event = _mapping(response.get("current_event"), "current_event", ignored)
    ignored.update(f"current_event.{key}" for key in event if key not in _EVENT)
    public_event = PublicEvent(_text(event.get("title")), _text(event.get("description")))

    choices: list[PublicChoice] = []
    raw_choices = response.get("choices", [])
    if isinstance(raw_choices, Sequence) and not isinstance(raw_choices, (str, bytes, bytearray)):
        for index, item in enumerate(raw_choices):
            if not isinstance(item, Mapping):
                ignored.add(f"choices[{index}]")
                continue
            ignored.update(f"choices[{index}].{key}" for key in item if key not in _CHOICE)
            choice = _int(item.get("choice"))
            if choice is None:
                ignored.add(f"choices[{index}].choice")
                continue
            choices.append(PublicChoice(choice, _text(item.get("action")), _text(item.get("description"))))
    elif "choices" in response:
        ignored.add("choices")

    raw_feed = response.get("events")
    public_feed = raw_feed if isinstance(raw_feed, str) else ""
    if "events" in response and not isinstance(raw_feed, str):
        ignored.add("events")

    state_session = state.get("session_id")
    response_session = response.get("session_id")
    session_id = state_session if isinstance(state_session, str) and state_session else response_session
    return PublicSnapshot(
        session_id=session_id if isinstance(session_id, str) and session_id else None,
        time=public_time,
        status=status,
        event=public_event,
        choices=tuple(choices),
        public_feed=public_feed,
        alive=alive,
        failed=failed,
        ignored_fields=tuple(sorted(ignored)),
    )


def with_public_material_risk(snapshot: PublicSnapshot, risk: PublicRisk) -> PublicSnapshot:
    """Attach an explicit public warning/consequence annotation.

    The adapter supplying this annotation must derive it from fresh,
    participant-visible evidence. This module intentionally performs no
    title/description keyword inference.
    """

    if risk not in {"MATERIAL", "NONE", "UNKNOWN"}:
        raise ValueError(f"unsupported public risk value: {risk!r}")
    return replace(snapshot, material_risk=risk)


@dataclass(frozen=True)
class ActionDecision:
    status: DecisionStatus
    choice: int | None = None
    reason: str = ""
    structural_switch: bool = False


@dataclass(frozen=True)
class ActionReceipt:
    success: bool
    status: str = "SUCCESS"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ProbeLocalState:
    """Bounded controller state; no raw history or hidden state is retained."""

    checkpoint_count: int = 0
    last_choice: int | None = None
    repeated_action_count: int = 0
    last_stall_signal: bool = False
    last_path: str | None = None
    structural_switches: int = 0


class MechanicalPolicy(Protocol):
    @property
    def name(self) -> str: ...

    def choose(self, snapshot: PublicSnapshot, local_state: ProbeLocalState | None = None) -> ActionDecision: ...


class MinIdControl:
    name = "MIN_ID_CONTROL"

    def choose(self, snapshot: PublicSnapshot, local_state: ProbeLocalState | None = None) -> ActionDecision:
        if snapshot.terminal is True:
            return ActionDecision("DEFER", reason="public snapshot is terminal")
        ids = sorted({choice.choice for choice in snapshot.choices})
        if not ids:
            return ActionDecision("UNSUPPORTED", reason="no legal public integer choice")
        return ActionDecision("ACTION", choice=ids[0], reason="minimum legal public integer choice")


def classify_structural_context(snapshot: PublicSnapshot) -> StructuralContext:
    """Classify only by exact public choice action labels.

    Event title/description and choice descriptions are intentionally ignored.
    Mixed or unrecognised choice sets fail closed to ``UNKNOWN_CONTEXT``.
    """

    labels = {choice.action.strip() for choice in snapshot.choices if choice.action.strip()}
    has_energy = bool(labels & _ENERGY_LABELS)
    has_main = bool(labels & _MAIN_LABELS)
    if has_energy and not has_main:
        return "ENERGY"
    if has_main and not has_energy:
        return "MAIN"
    return "UNKNOWN_CONTEXT"


def classify_structural_choice(choice: PublicChoice, context: StructuralContext) -> ChoiceClass:
    """Classify a choice using its public action label and known context."""

    if context == "UNKNOWN_CONTEXT":
        return "UNKNOWN"
    label = choice.action.strip()
    if label in _GROWTH_LABELS:
        return "GROWTH"
    if label in _RESTORATIVE_LABELS:
        return "RESTORATIVE"
    return "UNKNOWN"


class SimplePublicGrowthPrior:
    """Growth-first structural controller with an explicit public-risk override."""

    name = "SIMPLE_PUBLIC_GROWTH_PRIOR"

    def choose(self, snapshot: PublicSnapshot, local_state: ProbeLocalState | None = None) -> ActionDecision:
        context = classify_structural_context(snapshot)
        if context == "UNKNOWN_CONTEXT":
            return MinIdControl().choose(snapshot, local_state)

        restorative = [choice for choice in snapshot.choices if classify_structural_choice(choice, context) == "RESTORATIVE"]
        if snapshot.material_risk == "MATERIAL" and restorative:
            selected = min(restorative, key=lambda item: item.choice)
            return ActionDecision("ACTION", selected.choice, "explicit public material risk overrides growth prior")

        growth = [choice for choice in snapshot.choices if classify_structural_choice(choice, context) == "GROWTH"]
        if growth:
            selected = min(growth, key=lambda item: item.choice)
            return ActionDecision("ACTION", selected.choice, "minimum public structural growth choice")
        return MinIdControl().choose(snapshot, local_state)


class StallAwarePublicGrowth(SimplePublicGrowthPrior):
    """P1 plus one bounded structural alternative after a mechanical stall."""

    name = "STALL_AWARE_PUBLIC_GROWTH"

    def choose(self, snapshot: PublicSnapshot, local_state: ProbeLocalState | None = None) -> ActionDecision:
        local = local_state or ProbeLocalState()
        context = classify_structural_context(snapshot)
        if context == "UNKNOWN_CONTEXT" or not local.last_stall_signal or local.structural_switches >= 1:
            return super().choose(snapshot, local)

        alternatives = [
            choice
            for choice in snapshot.choices
            if choice.choice != local.last_choice
            and classify_structural_choice(choice, context) != "UNKNOWN"
        ]
        if not alternatives:
            return ActionDecision("DEFER", reason="stall has no compliant structural alternative")
        selected = min(alternatives, key=lambda item: item.choice)
        return ActionDecision(
            "ACTION",
            selected.choice,
            "one bounded structural alternative after mechanical stall",
            structural_switch=True,
        )


@dataclass(frozen=True)
class PublicDelta:
    field: str
    before: int | float
    after: int | float
    delta: int | float

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def compare_public_status(before: Mapping[str, PublicScalar], after: Mapping[str, PublicScalar]) -> tuple[PublicDelta, ...]:
    """Compare only common numeric public attributes; make no causal claim."""

    deltas: list[PublicDelta] = []
    for field in sorted(set(before) & set(after)):
        before_value, after_value = _number(before[field]), _number(after[field])
        if before_value is not None and after_value is not None:
            deltas.append(PublicDelta(field, before_value, after_value, after_value - before_value))
    return tuple(deltas)


@dataclass(frozen=True)
class CheckpointObservation:
    target: str
    path: str
    comparable: bool
    progress: ProgressStatus
    stall_signal: str
    repeated_action_count: int
    deltas: tuple[PublicDelta, ...] = ()
    reason: str = ""

    @property
    def is_stalled(self) -> bool:
        return self.stall_signal == "MECHANICAL_STALL_SIGNAL"

    def to_dict(self) -> dict[str, Any]:
        result = asdict(self)
        result["deltas"] = [delta.to_dict() for delta in self.deltas]
        return result


@dataclass(frozen=True)
class PublicMilestone:
    kind: Literal["promotion", "terminal"]
    label: str
    session_id: str | None
    month: int | None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class _Point:
    session_id: str | None
    target: str
    path: str
    direction: ProgressDirection
    value: int | float | None
    snapshot: PublicSnapshot
    repeated_action_count: int


class MechanicalTracker:
    """Observation-only repetition, delta, milestone, and stall diagnostics."""

    def __init__(self) -> None:
        self._previous: _Point | None = None
        self._previous_no_progress = False
        self._observations: list[CheckpointObservation] = []
        self._milestones: list[PublicMilestone] = []

    def record_checkpoint(
        self,
        snapshot: PublicSnapshot,
        *,
        target: str,
        path: str,
        direction: ProgressDirection = "increase",
        promotion_label: str | None = None,
    ) -> CheckpointObservation:
        if promotion_label:
            self._milestones.append(PublicMilestone("promotion", promotion_label, snapshot.session_id, snapshot.time.current_month))
        if snapshot.terminal is True and not any(
            item.kind == "terminal" and item.session_id == snapshot.session_id for item in self._milestones
        ):
            self._milestones.append(PublicMilestone("terminal", "public terminal state", snapshot.session_id, snapshot.time.current_month))

        repeated = 1
        if self._previous and self._previous.session_id == snapshot.session_id and self._previous.path == path:
            repeated = self._previous.repeated_action_count + 1
        current = _Point(snapshot.session_id, target, path, direction, _number(snapshot.status.get(target)), snapshot, repeated)
        previous = self._previous

        if previous is None:
            observation = CheckpointObservation(target, path, False, "UNKNOWN", "NONE", repeated, reason="first_checkpoint")
        elif previous.session_id != snapshot.session_id:
            observation = CheckpointObservation(target, path, False, "UNKNOWN", "NONE", repeated, reason="session_changed")
        elif (previous.target, previous.path, previous.direction) != (target, path, direction):
            observation = CheckpointObservation(target, path, False, "UNKNOWN", "NONE", repeated, reason="target_or_path_changed")
        elif previous.value is None or current.value is None:
            observation = CheckpointObservation(target, path, False, "UNKNOWN", "NONE", repeated, reason="target_value_unavailable")
        else:
            delta = current.value - previous.value
            advancing = delta > 0 if direction == "increase" else delta < 0 if direction == "decrease" else delta != 0
            progress: ProgressStatus = "ADVANCING" if advancing else "NO_PROGRESS"
            stalled = self._previous_no_progress and progress == "NO_PROGRESS"
            observation = CheckpointObservation(
                target,
                path,
                True,
                progress,
                "MECHANICAL_STALL_SIGNAL" if stalled else "NONE",
                repeated,
                compare_public_status(previous.snapshot.status, snapshot.status),
                "same_target_and_path",
            )
            self._previous_no_progress = progress == "NO_PROGRESS"

        if not observation.comparable:
            self._previous_no_progress = False
        self._previous = current
        self._observations.append(observation)
        return observation

    @property
    def observations(self) -> tuple[CheckpointObservation, ...]:
        return tuple(self._observations)

    @property
    def milestones(self) -> tuple[PublicMilestone, ...]:
        return tuple(self._milestones)


@dataclass(frozen=True)
class ProbeReport:
    policy_name: str
    session_id: str | None
    checkpoints: tuple[CheckpointObservation, ...]
    chosen_actions: tuple[int, ...]
    repeated_action_count: int
    structural_switch_count: int
    action_receipts: tuple[ActionReceipt, ...]
    unsupported_decisions: tuple[str, ...]
    milestones: tuple[PublicMilestone, ...]

    def to_dict(self) -> dict[str, Any]:
        checkpoints = [checkpoint.to_dict() for checkpoint in self.checkpoints]
        return {
            "policy_name": self.policy_name,
            "session_id": self.session_id,
            "checkpoints": checkpoints,
            "chosen_actions": list(self.chosen_actions),
            "repeated_action_count": self.repeated_action_count,
            "structural_switch_count": self.structural_switch_count,
            "action_receipts": [receipt.to_dict() for receipt in self.action_receipts],
            "public_deltas": [delta for item in checkpoints for delta in item["deltas"]],
            "mechanical_stall_signals": [item for item in checkpoints if item["stall_signal"] != "NONE"],
            "promotion_milestones": [item.to_dict() for item in self.milestones if item.kind == "promotion"],
            "terminal_milestones": [item.to_dict() for item in self.milestones if item.kind == "terminal"],
            "unsupported_decisions": list(self.unsupported_decisions),
            "result_status": (
                "ERROR"
                if any(not receipt.success for receipt in self.action_receipts)
                else "DEFERRED"
                if self.unsupported_decisions
                else "OK"
            ),
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, sort_keys=True)


class MechanicalProbe:
    def __init__(self, policy: MechanicalPolicy | None = None) -> None:
        self.policy = policy or MinIdControl()
        self.tracker = MechanicalTracker()
        self._local_state = ProbeLocalState()
        self._session_id: str | None = None
        self._chosen: list[int] = []
        self._receipts: list[ActionReceipt] = []
        self._unsupported: list[str] = []

    def choose(self, snapshot: PublicSnapshot) -> ActionDecision:
        if self._session_id is None:
            self._session_id = snapshot.session_id
        elif snapshot.session_id and self._session_id and snapshot.session_id != self._session_id:
            decision = ActionDecision("DEFER", reason="session identity changed")
            self._unsupported.append(decision.reason)
            return decision
        decision = self.policy.choose(snapshot, self._local_state)
        if decision.status == "ACTION" and isinstance(decision.choice, int) and not isinstance(decision.choice, bool):
            self._chosen.append(decision.choice)
            repeated = self._local_state.repeated_action_count + 1 if decision.choice == self._local_state.last_choice else 1
            self._local_state = ProbeLocalState(
                checkpoint_count=self._local_state.checkpoint_count,
                last_choice=decision.choice,
                repeated_action_count=repeated,
                last_stall_signal=self._local_state.last_stall_signal,
                last_path=self._local_state.last_path,
                structural_switches=self._local_state.structural_switches + int(decision.structural_switch),
            )
        elif decision.status != "ACTION":
            self._unsupported.append(decision.reason)
        return decision

    def record_checkpoint(self, snapshot: PublicSnapshot, **kwargs: Any) -> CheckpointObservation:
        if self._session_id is None:
            self._session_id = snapshot.session_id
        observation = self.tracker.record_checkpoint(snapshot, **kwargs)
        path = kwargs.get("path")
        self._local_state = ProbeLocalState(
            checkpoint_count=self._local_state.checkpoint_count + 1,
            last_choice=self._local_state.last_choice,
            repeated_action_count=self._local_state.repeated_action_count,
            last_stall_signal=observation.is_stalled,
            last_path=path if isinstance(path, str) else self._local_state.last_path,
            structural_switches=self._local_state.structural_switches,
        )
        return observation

    def record_action_receipt(self, success: bool, status: str = "SUCCESS") -> None:
        """Store only normalized public receipt status, never raw tool output."""

        self._receipts.append(ActionReceipt(bool(success), status))

    def report(self) -> ProbeReport:
        return ProbeReport(
            self.policy.name,
            self._session_id,
            self.tracker.observations,
            tuple(self._chosen),
            self._local_state.repeated_action_count,
            self._local_state.structural_switches,
            tuple(self._receipts),
            tuple(self._unsupported),
            self.tracker.milestones,
        )


class PublicMCPClient(Protocol):
    """Future injected public client; this module creates no transport."""

    async def new_game(self) -> Mapping[str, Any]: ...

    async def observe(self, session_id: str) -> Mapping[str, Any]: ...

    async def take_action(self, session_id: str, choice: int, notes: str = "") -> Mapping[str, Any]: ...
