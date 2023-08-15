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
    """
    Difficulty and mode for a game.
    Can be created manually by passing a ~bloonspy.model.btd6.Difficulty and ~bloonspy.model.btd6.Mode enum as parameters.

    ::

        from bloonspy.btd6 import Gamemode, Difficulty, Mode

        chimps = Gamemode(Difficulty.HARD, Mode.CHIMPS)
        military_only = Gamemode(Difficulty.MEDIUM, Mode.MILITARY_ONLY)
        some_custom_mode = Gamemode(Difficulty.EASY, Mode.DOUBLE_HP_MOABS)

    """
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
        return Gamemode(found_difficulty, found_mode) if found_mode and found_difficulty else None

    def __str__(self) -> str:
        return f"{self.difficulty.value} - {self.mode.value}"

    def __repr__(self) -> str:
        return str(self)

    def __eq__(self, other: "Gamemode") -> bool:
        if not isinstance(other, Gamemode):
            return False
        return self.mode == other.mode and \
            self.difficulty == other.difficulty

    def __hash__(self) -> int:
        return hash(f"{self.mode}{self.difficulty}")

    @staticmethod
    def easy_modes() -> list["Gamemode"]:
        """
        Shortcut for getting all Easy mode gamemodes.

        :return: A list of gamemodes.
        :rtype: list[~bloonspy.model.btd6.Gamemode]
        """
        return [
            Gamemode(Difficulty.EASY, Mode.STANDARD),
            Gamemode(Difficulty.EASY, Mode.PRIMARY_ONLY),
            Gamemode(Difficulty.EASY, Mode.DEFLATION),
        ]

    @staticmethod
    def medium_modes() -> list["Gamemode"]:
        """
        Shortcut for getting all Medium mode gamemodes.

        :return: A list of gamemodes.
        :rtype: list[~bloonspy.model.btd6.Gamemode]
        """
        return [
            Gamemode(Difficulty.MEDIUM, Mode.STANDARD),
            Gamemode(Difficulty.MEDIUM, Mode.MILITARY_ONLY),
            Gamemode(Difficulty.MEDIUM, Mode.REVERSE),
            Gamemode(Difficulty.MEDIUM, Mode.APOPALYPSE),
        ]

    @staticmethod
    def hard_modes() -> list["Gamemode"]:
        """
        Shortcut for getting all Hard mode gamemodes.

        :return: A list of gamemodes.
        :rtype: list[~bloonspy.model.btd6.Gamemode]
        """
        return [
            Gamemode(Difficulty.HARD, Mode.STANDARD),
            Gamemode(Difficulty.HARD, Mode.MAGIC_ONLY),
            Gamemode(Difficulty.HARD, Mode.DOUBLE_HP_MOABS),
            Gamemode(Difficulty.HARD, Mode.HALF_CASH),
            Gamemode(Difficulty.HARD, Mode.ALTERNATE_BLOONS_ROUNDS),
            Gamemode(Difficulty.HARD, Mode.IMPOPPABLE),
            Gamemode(Difficulty.HARD, Mode.CHIMPS),
        ]
