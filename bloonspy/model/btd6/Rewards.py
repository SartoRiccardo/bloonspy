from dataclasses import dataclass
from .Tower import Tower
from typing import Literal


@dataclass
class InstaMonkey:
    """An Insta Monkey."""
    tower: Tower  #: The tower this Insta Monkey is for.
    top_path: int  #: Top path upgrades.
    middle_path: int  #: Middle path upgrades.
    bottom_path: int  #: Bottom path upgrades.

    @property
    def tier(self) -> int:
        """The tier of the Insta Monkey."""
        return max(self.top_path, self.middle_path, self.bottom_path)

    def __eq__(self, other: "InstaMonkey") -> bool:
        if not isinstance(other, InstaMonkey):
            return False
        return self.tower == other.tower and \
            self.top_path == other.top_path and \
            self.middle_path == other.middle_path and \
            self.bottom_path == other.bottom_path

    def __hash__(self) -> int:
        return hash(f"{self.tower.value}{self.top_path}{self.middle_path}{self.bottom_path}")

    def __str__(self) -> str:
        return f"{self.tower.value} - {self.top_path}{self.middle_path}{self.bottom_path}"

    def __repr__(self) -> str:
        return str(self)


@dataclass
class Reward:
    """A generic reward."""
    type: Literal["MonkeyMoney", "CollectionEvent"]  #: Name of the reward.
    amount: int  #: Amount of the reward.
