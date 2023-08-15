from dataclasses import dataclass
from .Tower import Tower
from typing import Literal
from ...exceptions import InvalidTowerPath


@dataclass
class InstaMonkey:
    """
    An Insta Monkey.
    Can be created manually by passing a ~bloonspy.model.btd6.Tower and 3 paths as parameters.

    ::

        from bloonspy.btd6 import Tower, InstaMonkey

        glaive_dominus = InstaMonkey(Tower.BOOMERANG_MONKEY, 5, 0, 0)
        invalid_insta = InstaMonkey(Tower.BOOMERANG_MONKEY, 3, 3, 3)

    """
    tower: Tower  #: The tower this Insta Monkey is for.
    top_path: int  #: Top path upgrades.
    middle_path: int  #: Middle path upgrades.
    bottom_path: int  #: Bottom path upgrades.

    def __post_init__(self):
        is_invalid = False
        paths = [self.top_path, self.middle_path, self.bottom_path]
        if min(*paths) != 0 or min(*paths) < 0:
            is_invalid = True

        tiers_above_3 = 0
        for path in paths:
            if path >= 3:
                tiers_above_3 += 1
        if tiers_above_3 > 1:
            is_invalid = True

        if is_invalid:
            raise InvalidTowerPath(self.top_path, self.middle_path, self.bottom_path)

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
