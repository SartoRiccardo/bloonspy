from dataclasses import dataclass
from .Tower import Tower


@dataclass
class InstaMonkey:
    tower: Tower
    top_path: int
    middle_path: int
    bottom_path: int


@dataclass
class Reward:
    type: str
    amount: int
