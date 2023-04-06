from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
from typing import List, Dict, Union, Any
from ...utils.decorators import fetch_property
from ...exceptions import NotFound
from ..GameVersion import GameVersion
from bloonspy.utils.Infinity import Infinity
from ..Loadable import Loadable
from ..Asset import Asset
from .Restriction import Restriction, TowerRestriction
from .Gamemode import Gamemode
from .Power import Power
from .Tower import Tower
from .User import User


class ChallengeFilter(Enum):
    NEWEST = "newest"
    TRENDING = "trending"
    DAILY = "daily"


@dataclass(kw_only=True)
class ChallengeModifier:
    """All the modifiers of a challenge."""
    ability_cooldown_reduction: float = field(default=1.0)  #: Multiplier for ability cooldowns.
    removable_cost: float = field(default=1.0)  #: Multiplier for the cost of track removables.
    bloon_speed: float = field(default=1.0)  #: Bloon speed multiplier.
    moab_speed: float = field(default=1.0)  #: MOAB speed multiplier.
    boss_speed: float = field(default=1.0)  #: Boss bloon speed multiplier.
    ceramic_health: float = field(default=1.0)  #: Ceramic layer health multiplier.
    moab_health: float = field(default=1.0)  #: MOAB class bloon health multiplier.
    boss_health: float = field(default=1.0)  #: Boss bloon health multiplier
    regrow_rate: float = field(default=1.0)  #: Regrow rate multiplier
    all_regrow: bool = field(default=False)  #: If `True`, all bloons will be regrow.
    all_camo: bool = field(default=False)  #: If `True`, all bloons will be camo.


class Challenge(Loadable):
    """A BTD6 Challenge. It extends :class:`~bloonspy.model.Loadable`."""

    endpoint = "/btd6/challenges/challenge/{}"

    def __init__(self, challenge_id: str, eager: bool = False, name: str = None, created_at: int = None,
                 creator_id: str = None, raw_challenge: Dict[str, Any] = None):
        """Constructor method."""
        super().__init__(challenge_id, eager=eager)
        if raw_challenge:
            self._parse_json(raw_challenge)
        if name:
            self._data["name"] = name
        if created_at:
            self._data["createdAt"] = datetime.fromtimestamp(int(created_at/1000))
        if creator_id:
            self._data["creatorId"] = creator_id

    def _handle_exceptions(self, exception: Exception) -> None:
        error_msg = str(exception)
        if error_msg == "No challenge with that ID exists":
            raise NotFound(error_msg)
        print(error_msg)

    def _parse_json(self, raw_challenge: Dict[str, Any]) -> None:
        self._loaded = False

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
        if raw_challenge["_towers"] is not None:  # Is null in Odysseys
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
        """The unique ID of the challenge."""
        return self._id

    @property
    @fetch_property(Loadable.load_resource, should_load=Loadable._should_load_property("name"))
    def name(self) -> str:
        """The name of the challenge."""
        return self._data["name"]

    @property
    @fetch_property(Loadable.load_resource, should_load=Loadable._should_load_property("createdAt"))
    def created_at(self) -> datetime:
        """The time the challenge was created at."""
        return self._data["createdAt"]

    @property
    @fetch_property(Loadable.load_resource)
    def game_version(self) -> GameVersion:
        """The latest game version the challenge was last beaten in."""
        return self._data["gameVersion"]

    @property
    @fetch_property(Loadable.load_resource, should_load=Loadable._should_load_property("creatorId"))
    def creator_id(self) -> str:
        """The ID of the challenge's creator. `None` if there isn't one (e.g. Odyssey challenges)."""
        return self._data["creatorId"]

    @fetch_property(Loadable.load_resource)
    def creator(self) -> User or None:
        """Fetch the creator of the challenge.

        .. warning::
           This function needs the property :attr:`~bloonspy.model.btd6.Challenge.creator_id` to be
           loaded, or it will make another API call to fetch that first.

        :return: The creator of the challenge of `None` if there isn't one.
        :rtype: User or None
        """
        if self.creator_id is None:
            return None
        return User(self.creator_id, eager=True)

    @property
    @fetch_property(Loadable.load_resource)
    def challenge_map(self) -> Asset:
        """Name and URL of the map the challenge takes place in."""
        return self._data["map"]

    @property
    @fetch_property(Loadable.load_resource)
    def gamemode(self) -> Gamemode:
        """Gamemode of the challenge."""
        return self._data["gamemode"]

    @property
    @fetch_property(Loadable.load_resource)
    def disable_double_cash(self) -> bool:
        """`True` if Double Cash is disabled."""
        return self._data["disableDoubleCash"]

    @property
    @fetch_property(Loadable.load_resource)
    def disable_instas(self) -> bool:
        """`True` if Insta Monkeys is disabled."""
        return self._data["disableInstas"]

    @property
    @fetch_property(Loadable.load_resource)
    def disable_monkey_knowledge(self) -> bool:
        """`True` if Monkey Knowledge is disabled."""
        return self._data["disableMK"]

    @property
    @fetch_property(Loadable.load_resource)
    def disable_powers(self) -> bool:
        """`True` if Powers are disabled."""
        return self._data["disablePowers"]

    @property
    @fetch_property(Loadable.load_resource)
    def disable_selling(self) -> bool:
        """`True` if Selling is disabled."""
        return self._data["disableSelling"]

    @property
    @fetch_property(Loadable.load_resource)
    def disable_continues(self) -> bool:
        """`True` if Continues are disabled."""
        return self._data["noContinues"]

    @property
    @fetch_property(Loadable.load_resource)
    def starting_cash(self) -> int:
        """The amount of cash you start with."""
        return self._data["startingCash"]

    @property
    @fetch_property(Loadable.load_resource)
    def starting_lives(self) -> int:
        """The amount of lives you start with."""
        return self._data["lives"]

    @property
    @fetch_property(Loadable.load_resource)
    def max_lives(self) -> int:
        """The maximum amount of lives you can have."""
        return self._data["maxLives"]

    @property
    @fetch_property(Loadable.load_resource)
    def max_towers(self) -> int:
        """The maximum amount of towers you can have at any given time."""
        return self._data["maxTowers"]

    @property
    @fetch_property(Loadable.load_resource)
    def max_paragons(self) -> int:
        """The maximum amount of paragons you can have at any given time."""
        return self._data["maxParagons"]

    @property
    @fetch_property(Loadable.load_resource)
    def start_round(self) -> int:
        """The round the challenge starts at."""
        return self._data["startRound"]

    @property
    @fetch_property(Loadable.load_resource)
    def end_round(self) -> int:
        """The round the challenge ends at."""
        return self._data["endRound"]

    @property
    @fetch_property(Loadable.load_resource)
    def plays(self) -> int:
        """How many times the challenge has been played."""
        return self._data["plays"]

    @property
    @fetch_property(Loadable.load_resource)
    def plays_unique(self) -> int:
        """Amount of unique people that have played the challenge."""
        return self._data["playsUnique"]

    @property
    @fetch_property(Loadable.load_resource)
    def wins(self) -> int:
        """How many times the challenge has been won."""
        return self._data["winsUnique"]

    @property
    @fetch_property(Loadable.load_resource)
    def wins_unique(self) -> int:
        """Amount of unique people that have won the challenge."""
        return self._data["winsUnique"]

    @property
    @fetch_property(Loadable.load_resource)
    def losses(self) -> int:
        """How many times the challenge has been lost."""
        return self._data["losses"]

    @property
    @fetch_property(Loadable.load_resource)
    def losses_unique(self) -> int:
        """Amount of unique people that have lost the challenge."""
        return self._data["lossesUnique"]

    @property
    @fetch_property(Loadable.load_resource)
    def upvotes(self) -> int:
        """Amount of upvotes the challenge has."""
        return self._data["upvotes"]

    @property
    @fetch_property(Loadable.load_resource)
    def least_cash_used(self) -> Union[int, Infinity]:
        """Least Cash restriction on the challenge. If there's none, it's :class:`Infinity`."""
        return self._data["leastCash"]

    @property
    @fetch_property(Loadable.load_resource)
    def least_tiers_used(self) -> Union[int, Infinity]:
        """Least Tiers restriction on the challenge. If there's none, it's :class:`Infinity`."""
        return self._data["leastTiers"]

    @property
    @fetch_property(Loadable.load_resource)
    def seed(self) -> int:
        """The RNG seed for the challenge."""
        return self._data["seed"]

    @property
    @fetch_property(Loadable.load_resource)
    def round_sets(self) -> List[str]:
        """Names of the round sets of the challenge."""
        return self._data["roundSets"]

    @property
    @fetch_property(Loadable.load_resource)
    def powers(self) -> Dict[Power, Union[int, Infinity]]:
        """The powers allowed for the challenge, and how many you can use of each."""
        return self._data["powers"]

    @property
    @fetch_property(Loadable.load_resource)
    def modifiers(self) -> Dict[ChallengeModifier, float]:
        """Challenge modifiers, such as bloon speeds and health."""
        return self._data["modifiers"]

    @property
    @fetch_property(Loadable.load_resource)
    def towers(self) -> Dict[Tower, Restriction]:
        """Tower and Hero restrictions on the challenge."""
        return self._data["towers"]
