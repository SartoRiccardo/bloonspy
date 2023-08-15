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


@dataclass
class Reward:
    """A generic reward."""
    type: Literal["MonkeyMoney", "CollectionEvent"]  #: Name of the reward.
    amount: int  #: Amount of the reward.
