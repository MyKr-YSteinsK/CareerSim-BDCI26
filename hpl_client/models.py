"""Public views; simulator responses stay inside the adapter."""

from copy import deepcopy
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class PublicGameView:
    run_id: str
    revision: int
    phase: str
    projection: dict[str, Any]

    @property
    def facts(self) -> dict[str, Any]:
        return deepcopy(self.projection["observed_fact"])
