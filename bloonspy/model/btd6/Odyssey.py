from enum import Enum
from typing import List, Dict, Any, Union
from ...utils.decorators import fetch_property, exception_handler
from ...utils.Infinity import Infinity
from ...utils.api import get
from ..Event import Event
from ..Loadable import Loadable
from .Restriction import Restriction, TowerRestriction
from .Rewards import InstaMonkey, Reward
from .Challenge import Challenge
from .Power import Power
from .Tower import Tower


class OdysseyDifficulty(Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class Odyssey(Loadable):
    endpoint = "/btd6/odyssey/{}/:difficulty:"
    map_endpoint = "/btd6/odyssey/{}/:difficulty:/maps"

    def __init__(self, resource_id: str, name: str, difficulty: OdysseyDifficulty, eager: bool = False):
        self.endpoint = self.endpoint.replace(":difficulty:", difficulty.value)
        self.map_endpoint = self.map_endpoint.replace(":difficulty:", difficulty.value)
        super().__init__(resource_id, eager)
        self._name = name
        self._difficulty = difficulty

    def _parse_json(self, raw_odyssey: Dict[str, Any]) -> None:
        self._loaded = False

        copy_keys = [
            "isExtreme", "maxMonkeySeats", "maxMonkeysOnBoat", "maxPowerSlots", "startingHealth",
        ]
        for key in copy_keys:
            self._data[key] = raw_odyssey[key]

        self._data["rewards"] = []
        for raw_reward in raw_odyssey["_rewards"]:
            reward_type, reward = raw_reward.split(":", 1)
            if reward_type == "InstaMonkey":
                tower, path = reward.split(",")
                path = int(path)
                self._data["rewards"].append(InstaMonkey(
                    Tower.from_string(tower), int(path/100), int(path/10) % 10, path % 10
                ))
            elif reward_type == "Power":
                self._data["rewards"].append(Power.from_string(reward))
            else:
                self._data["rewards"].append(Reward(reward_type, reward))
        self._data["rewards"] = raw_odyssey["_rewards"]

        self._data["availablePowers"] = {}
        for power in raw_odyssey["_availablePowers"]:
            if power["max"] == 0:
                continue
            self._data["availablePowers"][Power.from_string(power["power"])] = power["max"]

        self._data["defaultPowers"] = {}
        for power in raw_odyssey["_defaultPowers"]:
            self._data["defaultPowers"][Power.from_string(power["name"])] = power["quantity"]

        self._data["availableTowers"] = {}
        for tower in raw_odyssey["_availableTowers"]:
            if tower["isHero"]:
                restr = Restriction(max_towers=1)
            else:
                restr = TowerRestriction(
                    max_towers=Infinity(),
                    top_path_blocked=tower["path1NumBlockedTiers"],
                    middle_path_blocked=tower["path2NumBlockedTiers"],
                    bottom_path_blocked=tower["path3NumBlockedTiers"],
                )
            self._data["availableTowers"][Tower.from_string(tower["tower"])] = restr

        self._data["defaultTowers"] = {}
        for tower in raw_odyssey["_defaultTowers"]:
            self._data["defaultTowers"][Tower.from_string(tower["name"])] = tower["quantity"]

        self._loaded = True

    @property
    def name(self) -> str:
        return self._name

    @property
    def difficulty(self) -> OdysseyDifficulty:
        return self._difficulty

    @property
    @fetch_property(Loadable.load_resource)
    def is_extreme(self) -> bool:
        return self._data["isExtreme"]

    @property
    @fetch_property(Loadable.load_resource)
    def max_monkey_seats(self) -> int:
        return self._data["maxMonkeySeats"]

    @property
    @fetch_property(Loadable.load_resource)
    def max_boat_seats(self) -> int:
        return self._data["maxMonkeysOnBoat"]

    @property
    @fetch_property(Loadable.load_resource)
    def max_power_slots(self) -> int:
        return self._data["maxPowerSlots"]

    @property
    @fetch_property(Loadable.load_resource)
    def starting_lives(self) -> int:
        return self._data["startingHealth"]

    @property
    @fetch_property(Loadable.load_resource)
    def rewards(self) -> List[Union[Power, InstaMonkey, Reward]]:
        return self._data["rewards"]

    @property
    def available_powers(self) -> Dict[Power, int]:
        return self._data["availablePowers"]

    @property
    def default_powers(self) -> Dict[Power, int]:
        return self._data["defaultPowers"]

    @property
    def available_towers(self) -> Dict[Tower, Restriction]:
        return self._data["availableTowers"]

    @property
    def default_towers(self) -> Dict[Tower, int]:
        return self._data["defaultTowers"]

    @exception_handler(Loadable.handle_exceptions)
    def maps(self) -> List[Challenge]:
        odyssey_map = get(self.map_endpoint.format(self._id))
        islands = []
        for island in odyssey_map:
            islands.append(Challenge(island["id"], raw_challenge=island))
        return islands


class OdysseyEvent(Event):
    event_endpoint = "/btd6/odyssey"
    event_name = "Odyssey"

    def easy(self, eager: bool = False) -> Odyssey:
        return Odyssey(self.id, self.name, OdysseyDifficulty.EASY, eager=eager)

    def medium(self, eager: bool = False) -> Odyssey:
        return Odyssey(self.id, self.name, OdysseyDifficulty.EASY, eager=eager)

    def hard(self, eager: bool = False) -> Odyssey:
        return Odyssey(self.id, self.name, OdysseyDifficulty.EASY, eager=eager)
