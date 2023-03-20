from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict
from ..GameVersion import GameVersion
from .Restriction import Restriction
from .Gamemode import Gamemode
from .Power import Power
from .Tower import Tower
from .Map import Map


@dataclass(kw_only=True)
class ChallengeModifier:
    ability_cooldown_reduction: float = field(default=1.0)
    removable_cost: float = field(default=1.0)
    bloon_speed: float = field(default=1.0)
    moab_speed: float = field(default=1.0)
    boss_speed: float = field(default=1.0)
    ceramic_health: float = field(default=1.0)
    moab_health: float = field(default=1.0)
    boss_health: float = field(default=1.0)
    regrow_rate: float = field(default=1.0)
    all_regrow: bool = field(default=False)
    all_camo: bool = field(default=False)


@dataclass(kw_only=True)
class Challenge:
    """A BTD6 Challenge.

    Attributes:
        id (str): Unique Challenge ID
        name (str): Challenge Name
        created_at (datatime): Challenge creation time
        game_version (GameVersion): Version of the game this challenge was created in
        challenge_map (Map): The map this challenge takes place in
        mode (Gamemode): Difficulty and gamemode of the challenge
        disable_double_cash (bool): `True` if Double Cash is disabled
        disable_instas (bool): `True` if Insta Monkeys are disabled
        disable_monkey_knowledge (bool): `True` if Monkey Knowledge is disabled
        disable_powers (bool): `True` if Powers are disabled
        disable_selling (bool): `True` if selling is disabled
        disable_continues (bool): `True` if continues are disabled
        starting_cash (int): Starting cash value
        starting_lives (int): Starting lives
        max_lives (int): Maximum allowed lives
        max_towers (int): Maximum towers allowed
        max_paragons (int): Maximum paragons allowed
        start_round (int): Starting round
        end_round (int): Ending round
        plays (int): Total number of attempts
        plays_unique (int): Total number of attempts by different people
        wins (int): Total number of wins
        wins_unique (int): Total number of wins by different people
        losses (int): Total number of losses
        losses_unique (int): Total number of losses
        upvotes (int): Total number of upvotes
        least_cash_used (int): Least Cash Used setting
        least_tiers_used (int): Least Tiers Used setting
        seed (int): The RNG seed
        round_sets (List[str]): Bloon round information
        powers (Dict[Power, int]): Power restrictions
        modifiers (Dict[ChallengeModifier, float]): Challenge modifiers
        towers (Dict[Tower, Restriction]): Tower restrictions
    """

    id: str
    name: str
    created_at: datetime
    game_version: GameVersion
    creator_id: str = field(repr=False)
    challenge_map: Map
    gamemode: Gamemode
    disable_double_cash: bool = field(repr=False)
    disable_instas: bool = field(repr=False)
    disable_monkey_knowledge: bool = field(repr=False)
    disable_powers: bool = field(repr=False)
    disable_selling: bool = field(repr=False)
    disable_continues: bool = field(repr=False)
    starting_cash: int
    starting_lives: int
    max_lives: int = field(repr=False)
    max_towers: int = field(repr=False)
    max_paragons: int = field(repr=False)
    start_round: int
    end_round: int
    plays: int = field(repr=False)
    plays_unique: int = field(repr=False)
    wins: int = field(repr=False)
    wins_unique: int = field(repr=False)
    losses: int = field(repr=False)
    losses_unique: int = field(repr=False)
    upvotes: int = field(repr=False)
    least_cash_used: int = field(repr=False)
    least_tiers_used: int = field(repr=False)
    seed: int = field(repr=False)
    round_sets: List[str] = field(repr=False)
    powers: Dict[Power, int] = field(repr=False)
    modifiers: Dict[ChallengeModifier, float] = field(repr=False)
    towers: Dict[Tower, Restriction] = field(repr=False)

    # def creator(self) -> UserProfile:
    #     """Fetch the creator of the challenge.
    #
    #     :raises NotFound: If the user is not found
    #
    #     :return: The generated profile
    #     """
    #     pass

    # def _from_json(self, raw_challenge: dict) -> "Challenge":
    #     pass
