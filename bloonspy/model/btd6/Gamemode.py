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


@dataclass
class Gamemode:
    difficulty: Difficulty
    mode: Mode

    @staticmethod
    def from_strings(difficulty, mode) -> "Gamemode":
        difficulty_switch = {
            "Easy": Difficulty.EASY,
            "Medium": Difficulty.MEDIUM,
            "Hard": Difficulty.HARD,
            "Impoppable": Difficulty.IMPOPPABLE,
        }
        # TODO get the actual strings
        mode_switch = {
            "Standard": Mode.STANDARD,
            "PrimaryOnly": Mode.PRIMARY_ONLY,
            "Deflation": Mode.DEFLATION,
            "MilitaryOnly": Mode.MILITARY_ONLY,
            "Reverse": Mode.REVERSE,
            "Apopalypse": Mode.APOPALYPSE,
            "MagicOnly": Mode.MAGIC_ONLY,
            "DoubleHPMoabs": Mode.DOUBLE_HP_MOABS,
            "ABR": Mode.ALTERNATE_BLOON_ROUNDS,
            "Chimps": Mode.CHIMPS,
        }

        found_difficulty = difficulty_switch[difficulty] if difficulty in difficulty_switch else None
        found_mode = mode_switch[mode] if mode in mode_switch else None
        return Gamemode(found_difficulty, found_mode)
