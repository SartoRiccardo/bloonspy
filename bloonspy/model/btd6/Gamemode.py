from dataclasses import dataclass
from enum import Enum


class Difficulty(Enum):
    EASY = "Easy"
    MEDIUM = "Medium"
    HARD = "Hard"


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
    ALTERNATE_BLOONS_ROUNDS = "Alternate Bloons Rounds"
    IMPOPPABLE = "Impoppable"

    CHIMPS = "CHIMPS"


@dataclass
class Gamemode:
    """Difficulty and mode for a game."""
    difficulty: Difficulty  #: The game's difficulty.
    mode: Mode  #: The game's mode.

    @staticmethod
    def from_strings(difficulty, mode) -> "Gamemode":
        difficulty_switch = {
            "Easy": Difficulty.EASY,
            "Medium": Difficulty.MEDIUM,
            "Hard": Difficulty.HARD,
        }
        mode_switch = {
            "Standard": Mode.STANDARD,
            "PrimaryOnly": Mode.PRIMARY_ONLY,
            "Deflation": Mode.DEFLATION,
            "MilitaryOnly": Mode.MILITARY_ONLY,
            "Reverse": Mode.REVERSE,
            "Apopalypse": Mode.APOPALYPSE,
            "MagicOnly": Mode.MAGIC_ONLY,
            "DoubleMoabHealth": Mode.DOUBLE_HP_MOABS,
            "HalfCash": Mode.HALF_CASH,
            "AlternateBloonsRounds": Mode.ALTERNATE_BLOONS_ROUNDS,
            "Impoppable": Mode.IMPOPPABLE,
            "Clicks": Mode.CHIMPS,
        }

        found_difficulty = difficulty_switch[difficulty] if difficulty in difficulty_switch else None
        found_mode = mode_switch[mode] if mode in mode_switch else None
        return Gamemode(found_difficulty, found_mode)
