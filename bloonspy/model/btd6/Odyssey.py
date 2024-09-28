from enum import Enum
from typing import Any, Awaitable
from ...utils.decorators import fetch_property, exception_handler
from ...utils.Infinity import Infinity
from ...utils.api import get
from ...utils.asyncapi import aget
from ..Event import Event
from ..Loadable import Loadable
from .Restriction import Restriction, TowerRestriction
from .Rewards import InstaMonkey, Reward
from .Challenge import Challenge
from .Power import Power
from .Tower import Tower


class OdysseyDifficulty(Enum):
    """The three difficulties Odysseys come in."""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class Odyssey(Loadable):
    """Represents a single Odyssey. Inherits from :class:`~bloonspy.model.Loadable`."""
    endpoint = "/btd6/odyssey/{}/:difficulty:"
    map_endpoint = "/btd6/odyssey/{}/:difficulty:/maps"

    def __init__(
            self,
            resource_id: str,
            name: str,
            description: str,
            difficulty: OdysseyDifficulty,
            **kwargs
    ):
        self.endpoint = self.endpoint.replace(":difficulty:", difficulty.value)
        self.map_endpoint = self.map_endpoint.replace(":difficulty:", difficulty.value)
        super().__init__(resource_id, **kwargs)
        self._name = name
        self._description = description
        self._difficulty = difficulty

    def _parse_json(self, raw_odyssey: dict[str, Any]) -> None:
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
        """The Odyssey's name"""
        return self._name

    @property
    def description(self) -> str:
        """*New in 0.3.0*

        The Odyssey's description"""
        return self._description

    @property
    def difficulty(self) -> OdysseyDifficulty:
        """The Odysseys's difficulty"""
        return self._difficulty

    @property
    @fetch_property(Loadable.load_resource)
    def is_extreme(self) -> bool:
        """`True` if the odyssey is extreme."""
        return self._data["isExtreme"]

    @property
    @fetch_property(Loadable.load_resource)
    def max_monkey_seats(self) -> int:
        """Max number of monkey types you can take."""
        return self._data["maxMonkeySeats"]

    @property
    @fetch_property(Loadable.load_resource)
    def max_boat_seats(self) -> int:
        """Max number of monkeys you can take."""
        return self._data["maxMonkeysOnBoat"]

    @property
    @fetch_property(Loadable.load_resource)
    def max_power_slots(self) -> int:
        """Max number of powers you can take."""
        return self._data["maxPowerSlots"]

    @property
    @fetch_property(Loadable.load_resource)
    def starting_lives(self) -> int:
        """Odyssey's starting lives"""
        return self._data["startingHealth"]

    @property
    @fetch_property(Loadable.load_resource)
    def rewards(self) -> list[Power | InstaMonkey | Reward]:
        """Rewards for completing the odyssey."""
        return self._data["rewards"]

    @property
    def available_powers(self) -> dict[Power, int]:
        """Available powers to choose from for the odyssey."""
        return self._data["availablePowers"]

    @property
    def default_powers(self) -> dict[Power, int]:
        """Default powers for the odyssey."""
        return self._data["defaultPowers"]

    @property
    def available_towers(self) -> dict[Tower, Restriction]:
        """Available towers to choose from for the odyssey."""
        return self._data["availableTowers"]

    @property
    def default_towers(self) -> dict[Tower, int]:
        """Default towers for the odyssey."""
        return self._data["defaultTowers"]

    @exception_handler(Loadable.handle_exceptions)
    def maps(self) -> list[Challenge] | Awaitable[list[Challenge]]:
        """Get all of the odyssey's challenges."""
        def on_data_load(data) -> list[Challenge]:
            islands = []
            for island in data:
                islands.append(Challenge(
                    island["id"],
                    raw_challenge=island,
                    async_client=self._async_client,
                ))
            return islands

        async def async_maps() -> list[Challenge]:
            return on_data_load(
                await aget(self._async_client, self.map_endpoint.format(self._id))
            )

        if self._async_client:
            return async_maps()
        return on_data_load(get(self.map_endpoint.format(self._id)))


class OdysseyEvent(Event):
    """An Odyssey event. Inherits from :class:`~bloonspy.model.Event`."""
    event_endpoint = "/btd6/odyssey"
    event_name = "Odyssey"

    def _parse_event(self, data: dict[str, Any]) -> None:
        self._data["description"] = data["description"]
        super()._parse_event(data)

    @property
    @fetch_property(Event.load_event, should_load=Event._should_load_property("description"))
    def description(self) -> str:
        """*New in 0.3.0*

        The Odyssey's description."""
        return self._data["description"]

    def easy(self, eager: bool = False) -> Odyssey | Awaitable[Odyssey]:
        """Get the easy mode version of the Odyssey.

        .. note::
           If lazily loaded, the returned :class:`~bloonspy.model.btd6.Odyssey` object will only
           have the properties :attr:`~bloonspy.model.Loadable.id`, :attr:`~bloonspy.model.btd6.Odyssey.name`,
           and :attr:`~bloonspy.model.Odyssey.difficulty` loaded.

        :param eager: If `True`, it loads all of the data right away. Set it to `False`
            if you want to limit API calls and don't need all the data. For more information,
            please read `Lazy and Eager Loading <async.html#lazy-and-eager-loading>`_.
        :type eager: bool
        :return: The easy mode of the odyssey.
        :rtype: ~bloonspy.model.btd6.Odyssey
        """
        return self._fetch_odyssey(eager, OdysseyDifficulty.EASY)

    def medium(self, eager: bool = False) -> Odyssey | Awaitable[Odyssey]:
        """Get the medium mode version of the Odyssey.

        .. note::
           If lazily loaded, the returned :class:`~bloonspy.model.btd6.Odyssey` object will only
           have the properties :attr:`~bloonspy.model.Loadable.id`, :attr:`~bloonspy.model.btd6.Odyssey.name`,
           and :attr:`~bloonspy.model.Odyssey.difficulty` loaded.

        :param eager: If `True`, it loads all of the data right away. Set it to `False`
            if you want to limit API calls and don't need all the data. For more information,
            please read `Lazy and Eager Loading <async.html#lazy-and-eager-loading>`_.
        :type eager: bool
        :return: The medium mode of the odyssey.
        :rtype: ~bloonspy.model.btd6.Odyssey
        """
        return self._fetch_odyssey(eager, OdysseyDifficulty.MEDIUM)

    def hard(self, eager: bool = False) -> Odyssey | Awaitable[Odyssey]:
        """Get the hard mode version of the Odyssey.

        .. note::
           If lazily loaded, the returned :class:`~bloonspy.model.btd6.Odyssey` object will only
           have the properties :attr:`~bloonspy.model.Loadable.id`, :attr:`~bloonspy.model.btd6.Odyssey.name`,
           and :attr:`~bloonspy.model.Odyssey.difficulty` loaded.

        :param eager: If `True`, it loads all of the data right away. Set it to `False`
            if you want to limit API calls and don't need all the data. For more information,
            please read `Lazy and Eager Loading <async.html#lazy-and-eager-loading>`_.
        :type eager: bool
        :return: The hard mode of the odyssey.
        :rtype: ~bloonspy.model.btd6.Odyssey
        """
        return self._fetch_odyssey(eager, OdysseyDifficulty.HARD)

    def _fetch_odyssey(self, eager: bool, difficulty: OdysseyDifficulty) -> Odyssey | Awaitable[Odyssey]:
        async def async_load(o: Odyssey) -> Odyssey:
            if eager:
                await o.load_resource()
            return o

        ody = Odyssey(
            self.id,
            self.name,
            self.description,
            difficulty,
            eager=eager,
            async_client=self._async_client,
        )
        if self._async_client:
            return async_load(ody)
        return ody
