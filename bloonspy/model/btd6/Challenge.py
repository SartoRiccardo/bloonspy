from dataclasses import dataclass, field
import requests
from datetime import datetime
from typing import List, Dict, Union, Any
from ...utils.decorators import fetch_property
from ..GameVersion import GameVersion
from bloonspy.utils.Infinity import Infinity
from ..Asset import Asset
from .Restriction import Restriction, TowerRestriction
from .Gamemode import Gamemode
from .Power import Power
from .Tower import Tower


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


class Challenge:
    """A BTD6 Challenge.

    Attributes:
        id (str): Unique Challenge ID
        name (str): Challenge Name
        created_at (datatime): Challenge creation time
        game_version (GameVersion): Version of the game this challenge was created in
        challenge_map (Asset): The map this challenge takes place in
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
        powers (Dict[Power, int]): Power restrictions. Banned powers don't appear, and powers with no restrictions appear as Infinity.
        modifiers (Dict[ChallengeModifier, float]): Challenge modifiers
        towers (Dict[Tower, Restriction]): Tower restrictions
    """

    ENDPOINT = "https://data.ninjakiwi.com/btd6/challenges/challenge/{}"

    def __init__(self, challenge_id: str, eager: bool = False):
        self._id = challenge_id
        self._data = {}
        self._loaded = False
        if eager:
            self._load_challenge()

    def _load_challenge(self, only_if_unloaded: bool = True) -> None:
        if self._loaded and only_if_unloaded:
            return

        resp = requests.get(self.ENDPOINT.format(self._id))
        if resp.status_code != 200:
            return

        data = resp.json()
        if not data["success"]:
            raise Exception(data["error"])

        self._parse_json(data["body"])

    def _parse_json(self, raw_challenge: Dict[str, Any]) -> None:
        self._loaded = False

        self._data = {}
        copy_keys = [
            "name", "disableDoubleCash", "disableInstas", "disableMK", "disablePowers", "disableSelling",
            "startingCash", "noContinues", "seed", "roundSets", "lives", "maxLives",
            "startRound", "endRound", "maxTowers", "maxParagons", "plays", "wins", "losses", "upvotes", "playsUnique",
            "winsUnique", "lossesUnique"
        ]
        for key in copy_keys:
            self._data[key] = raw_challenge[key]

        # self._data["maxTowers"] = Infinity() if raw_challenge["maxTowers"] == 9999 else raw_challenge["maxTowers"]
        # self._data["maxParagons"] = Infinity() if raw_challenge["maxParagons"] == 10 else raw_challenge["maxParagons"]
        self._data["leastCash"] = Infinity() if raw_challenge["leastCashUsed"] == -1 else raw_challenge["leastCashUsed"]
        self._data["leastTiers"] = Infinity() if raw_challenge["leastTiersUsed"] == -1 else raw_challenge["leastTiersUsed"]
        self._data["createdAt"] = datetime.fromtimestamp(int(raw_challenge["createdAt"]/1000))
        self._data["gameVersion"] = GameVersion.from_string(raw_challenge["gameVersion"])
        self._data["map"] = Asset(raw_challenge["map"], raw_challenge["mapURL"])
        self._data["gamemode"] = Gamemode.from_strings(raw_challenge["difficulty"], raw_challenge["mode"])
        self._data["creatorId"] = None
        if raw_challenge["creator"]:
            creator_id = raw_challenge["creator"].split("/")[-1]
            self._data["creatorId"] = creator_id

        self._data["powers"] = {}
        for power in raw_challenge["_powers"]:
            if power["max"] == 0:
                continue
            amount = Infinity() if power["max"] == -1 else power["max"]
            self._data["powers"][Power.from_string(power["power"])] = amount

        # Renames the keys so they can be fed into the dataclass
        modifiers = {}
        rename_keys = [
            ("abilityCooldownReductionMultiplier", "ability_cooldown_reduction"),
            ("removeableCostMultiplier", "removable_cost"),
            ("_bloonModifiers.speedMultiplier", "bloon_speed"),
            ("_bloonModifiers.moabSpeedMultiplier", "moab_speed"),
            ("_bloonModifiers.bossSpeedMultiplier", "boss_speed"),
            ("_bloonModifiers.healthMultipliers.bloons", "ceramic_health"),
            ("_bloonModifiers.healthMultipliers.moabs", "moab_health"),
            ("_bloonModifiers.healthMultipliers.boss", "boss_health"),
            ("_bloonModifiers.regrowRateMultiplier", "regrow_rate"),
            ("_bloonModifiers.allRegen", "all_regrow"),
            ("_bloonModifiers.allCamo", "all_camo"),
        ]
        for old_key, new_key in rename_keys:
            old_keys = old_key.split(".")
            item = raw_challenge
            while len(old_keys) > 0:
                if old_keys[0] not in item:
                    item = None
                    break
                item = item[old_keys[0]]
                old_keys.pop(0)

            if item is None:
                continue
            modifiers[new_key] = item
        self._data["modifiers"] = ChallengeModifier(**modifiers)

        self._data["towers"] = {}
        for restriction_data in raw_challenge["_towers"]:
            tower = Tower.from_string(restriction_data["tower"])
            max_towers = Infinity() if restriction_data["max"] == -1 else restriction_data["max"]
            if tower is None or max_towers == 0:
                continue

            if tower.is_hero():
                self._data["towers"][tower] = Restriction(max_towers=max_towers)
            else:
                self._data["towers"][tower] = TowerRestriction(
                    max_towers=max_towers,
                    top_path_blocked=restriction_data["path1NumBlockedTiers"],
                    middle_path_blocked=restriction_data["path2NumBlockedTiers"],
                    bottom_path_blocked=restriction_data["path3NumBlockedTiers"]
                )

        self._loaded = True

    @property
    def id(self) -> str:
        return self._id

    @property
    def loaded(self) -> bool:
        return self._loaded

    @property
    @fetch_property(_load_challenge)
    def name(self) -> str:
        return self._data["name"]

    @property
    @fetch_property(_load_challenge)
    def created_at(self) -> datetime:
        return self._data["createdAt"]

    @property
    @fetch_property(_load_challenge)
    def game_version(self) -> GameVersion:
        return self._data["gameVersion"]

    @property
    @fetch_property(_load_challenge)
    def creator_id(self) -> str:
        return self._data["creatorId"]

    # @cached_property
    # @fetch_property(_load_challenge)
    # def creator(self) -> User or None:
    #     if self.creator_id is None:
    #         return None
    #     return User(self.creator_id, eager=True)

    @property
    @fetch_property(_load_challenge)
    def challenge_map(self) -> Asset:
        return self._data["map"]

    @property
    @fetch_property(_load_challenge)
    def gamemode(self) -> Gamemode:
        return self._data["gamemode"]

    @property
    @fetch_property(_load_challenge)
    def disable_double_cash(self) -> bool:
        return self._data["disableDoubleCash"]

    @property
    @fetch_property(_load_challenge)
    def disable_instas(self) -> bool:
        return self._data["disableInstas"]

    @property
    @fetch_property(_load_challenge)
    def disable_monkey_knowledge(self) -> bool:
        return self._data["disableMK"]

    @property
    @fetch_property(_load_challenge)
    def disable_powers(self) -> bool:
        return self._data["disablePowers"]

    @property
    @fetch_property(_load_challenge)
    def disable_selling(self) -> bool:
        return self._data["disableSelling"]

    @property
    @fetch_property(_load_challenge)
    def disable_continues(self) -> bool:
        return self._data["noContinues"]

    @property
    @fetch_property(_load_challenge)
    def starting_cash(self) -> int:
        return self._data["startingCash"]

    @property
    @fetch_property(_load_challenge)
    def starting_lives(self) -> int:
        return self._data["lives"]

    @property
    @fetch_property(_load_challenge)
    def max_lives(self) -> int:
        return self._data["maxLives"]

    @property
    @fetch_property(_load_challenge)
    def max_towers(self) -> int:
        return self._data["maxTowers"]

    @property
    @fetch_property(_load_challenge)
    def max_paragons(self) -> int:
        return self._data["maxParagons"]

    @property
    @fetch_property(_load_challenge)
    def start_round(self) -> int:
        return self._data["startRound"]

    @property
    @fetch_property(_load_challenge)
    def end_round(self) -> int:
        return self._data["endRound"]

    @property
    @fetch_property(_load_challenge)
    def plays(self) -> int:
        return self._data["plays"]

    @property
    @fetch_property(_load_challenge)
    def plays_unique(self) -> int:
        return self._data["playsUnique"]

    @property
    @fetch_property(_load_challenge)
    def wins(self) -> int:
        return self._data["winsUnique"]

    @property
    @fetch_property(_load_challenge)
    def wins_unique(self) -> int:
        return self._data["winsUnique"]

    @property
    @fetch_property(_load_challenge)
    def losses(self) -> int:
        return self._data["losses"]

    @property
    @fetch_property(_load_challenge)
    def losses_unique(self) -> int:
        return self._data["lossesUnique"]

    @property
    @fetch_property(_load_challenge)
    def upvotes(self) -> int:
        return self._data["upvotes"]

    @property
    @fetch_property(_load_challenge)
    def least_cash_used(self) -> Union[int, Infinity]:
        return self._data["leastCash"]

    @property
    @fetch_property(_load_challenge)
    def least_tiers_used(self) -> Union[int, Infinity]:
        return self._data["leastTiers"]

    @property
    @fetch_property(_load_challenge)
    def seed(self) -> int:
        return self._data["seed"]

    @property
    @fetch_property(_load_challenge)
    def round_sets(self) -> List[str]:
        return self._data["roundSets"]

    @property
    @fetch_property(_load_challenge)
    def powers(self) -> Dict[Power, Union[int, Infinity]]:
        return self._data["powers"]

    @property
    @fetch_property(_load_challenge)
    def modifiers(self) -> Dict[ChallengeModifier, float]:
        return self._data["modifiers"]

    @property
    @fetch_property(_load_challenge)
    def towers(self) -> Dict[Tower, Restriction]:
        return self._data["towers"]
