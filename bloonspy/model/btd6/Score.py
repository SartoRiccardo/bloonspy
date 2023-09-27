from dataclasses import dataclass
from datetime import timedelta
from enum import Enum
from typing import Dict, Any


class ScoreType(Enum):
    """Ways to judge how good a player did in events."""
    GAME_TIME = "Game Time"
    CASH_SPENT = "Cash Spent"
    TIERS = "Tiers"
    TIME_AFTER_EVENT_START = "Time After Event Start"

    @staticmethod
    def from_string(value: str) -> "ScoreType":
        score_type_switch = {
            "GameTime": ScoreType.GAME_TIME,
            "CashSpent": ScoreType.CASH_SPENT,
            "Tiers": ScoreType.TIERS,
            "Time after event start": ScoreType.TIME_AFTER_EVENT_START,
        }
        if value in score_type_switch:
            return score_type_switch[value]
        value = value.replace(" ", "")
        if value in score_type_switch:
            return score_type_switch[value]
        return None


@dataclass
class Score:
    """An event score."""
    type: ScoreType  #: What the score represents.
    value: int | timedelta  #: The actual score value.

    @staticmethod
    def from_json(data: Dict[str, Any]) -> "Score":
        value = data["score"]
        if data["type"] == "time":
            value = timedelta(microseconds=data["score"]*1000)
        return Score(
            ScoreType.from_string(data["name"]), value
        )

    def __str__(self) -> str:
        if self.type == ScoreType.CASH_SPENT:
            return f"${self.value:,}"
        elif self.type == ScoreType.TIERS:
            return f"{self.value:,}"
        return str(self.value)

    def __eq__(self, other) -> bool:
        return isinstance(other, Score) and \
            other.type == self.type and \
            other.value == self.value

    def __gt__(self, other) -> bool:
        return isinstance(other, Score) and \
            other.type == self.type and \
            self.type > other.type

    def __ge__(self, other) -> bool:
        return isinstance(other, Score) and \
            other.type == self.type and \
            self.type >= other.type

    def __lt__(self, other) -> bool:
        return isinstance(other, Score) and \
            other.type == self.type and \
            self.type < other.type

    def __le__(self, other) -> bool:
        return isinstance(other, Score) and \
            other.type == self.type and \
            self.type <= other.type
