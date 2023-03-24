from dataclasses import dataclass
from .Tower import Tower


@dataclass
class InstaMonkey:
    """An Insta Monkey."""
    tower: Tower  #: The tower this Insta Monkey is for.
    top_path: int  #: Top path upgrades.
    middle_path: int  #: Middle path upgrades.
    bottom_path: int  #: Bottom path upgrades.


@dataclass
class Reward:
    """A generic reward."""
    type: str  #: Name of the reward, e.g. `MonkeyMoney`.
    amount: int  #: Amount of the reward.
