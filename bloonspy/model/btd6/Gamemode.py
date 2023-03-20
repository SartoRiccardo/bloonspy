from dataclasses import dataclass
from enum import Enum


class Difficulty(Enum):
    EASY = "Easy"
    MEDIUM = "Medium"
    HARD = "Hard"
    IMPOPPABLE = "Impoppable"


class Mode(Enum):
    STANDARD = "Standard"

    PRIMARY_ONLY = "Primary Only"
    DEFLATION = "Deflation"

    MILITARY_ONLY = "Military Only"
    REVERSE = "Reverse"
    APOPALYPSE = "Apopalypse"

    MAGIC_ONLY = "Magic Only"
    DOUBLE_HP_MOABS = "Double HP MOABs"
    HALF_CASH = "Half Cash"
    ALTERNATE_BLOON_ROUNDS = "Alternate Bloon Rounds"

    CHIMPS = "CHIMPs"


@dataclass(kw_only=True)
class Gamemode:
    difficulty: Difficulty
    mode: Mode
