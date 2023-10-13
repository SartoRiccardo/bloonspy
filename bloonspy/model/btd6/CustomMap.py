from datetime import datetime
from ...utils.decorators import fetch_property
from ..Asset import Asset
from .User import User
from ...exceptions import NotFound
from ..Loadable import Loadable
from ..GameVersion import GameVersion


class CustomMap(Loadable):
    """
    *New in 0.7.0*

    A custom map created by an user.
    """

    endpoint = "/btd6/maps/map/{}"

    def __init__(self, map_id: str, eager: bool = False, created_at: int = None, name: str = None,
                 creator_id: str = None, raw_map: dict = None):
        """Constructor method."""
        super().__init__(map_id, eager=eager)
        if raw_map:
            self._parse_json(raw_map)
        if name:
            self._data["name"] = name
        if created_at:
            self._data["createdAt"] = datetime.fromtimestamp(int(created_at / 1000))
        if creator_id:
            self._data["creatorId"] = creator_id

    def _handle_exceptions(self, exception: Exception) -> None:
        error_msg = str(exception)
        if error_msg.lower() == "no map with that id exists":
            raise NotFound(error_msg)

    def _parse_json(self, raw_map: dict) -> None:
        self._loaded = False

        copy_keys = [
            "name", "plays", "wins", "restarts", "losses", "upvotes", "playsUnique", "winsUnique", "lossesUnique",
            "mapURL",
        ]
        for key in copy_keys:
            self._data[key] = raw_map[key]

        self._data["gameVersion"] = GameVersion.from_string(raw_map["gameVersion"])
        self._data["createdAt"] = datetime.fromtimestamp(int(raw_map["createdAt"] / 1000))
        self._data["creatorId"] = raw_map["creator"].split("/")[-1]

        self._loaded = True

    @property
    def id(self) -> str:
        """The unique ID of the custom map."""
        return self._id

    @property
    @fetch_property(Loadable.load_resource, should_load=Loadable._should_load_property("name"))
    def name(self) -> str:
        """The name of the custom map."""
        return self._data["name"]

    @property
    @fetch_property(Loadable.load_resource, should_load=Loadable._should_load_property("created_at"))
    def created_at(self) -> datetime:
        """The time the map was created at."""
        return self._data["createdAt"]

    @fetch_property(Loadable.load_resource, should_load=Loadable._should_load_property("creatorId"))
    def creator(self) -> User or None:
        """
        Fetch the creator of the map.

        :return: The creator of the challenge.
        """
        if self._data["creatorId"] is None:
            return None
        return User(self._data["creatorId"], eager=True)

    @property
    @fetch_property(Loadable.load_resource)
    def game_version(self) -> GameVersion:
        """The game version this map was created in."""
        return self._data["gameVersion"]

    @property
    @fetch_property(Loadable.load_resource)
    def plays(self) -> int:
        """The amount of times this map has been played."""
        return self._data["plays"]

    @property
    @fetch_property(Loadable.load_resource)
    def wins(self) -> int:
        """How many times this time has been beaten."""
        return self._data["wins"]

    @property
    @fetch_property(Loadable.load_resource)
    def restarts(self) -> int:
        """How many times this map has been restarted."""
        return self._data["restarts"]

    @property
    @fetch_property(Loadable.load_resource)
    def losses(self) -> int:
        """How many times people have lost on this map."""
        return self._data["losses"]

    @property
    @fetch_property(Loadable.load_resource)
    def upvotes(self) -> int:
        """How many upvotes this map has."""
        return self._data["upvotes"]

    @property
    @fetch_property(Loadable.load_resource)
    def plays_unique(self) -> int:
        """How many unique users have played the map."""
        return self._data["playsUnique"]

    @property
    @fetch_property(Loadable.load_resource)
    def wins_unique(self) -> int:
        """How many unique players have won at this map."""
        return self._data["winsUnique"]

    @property
    @fetch_property(Loadable.load_resource)
    def losses_unique(self) -> int:
        """How many unique people have lost at this map."""
        return self._data["lossesUnique"]

    @property
    @fetch_property(Loadable.load_resource)
    def losses_unique(self) -> int:
        """How many unique people have lost at this map."""
        return self._data["lossesUnique"]

    @property
    @fetch_property(Loadable.load_resource)
    def thumbnail(self) -> str:
        """URL to an image of the custom map."""
        return self._data["mapURL"]
