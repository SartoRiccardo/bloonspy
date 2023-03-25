from typing import Dict, Any
from enum import Enum
from ...exceptions import NotFound
from ...utils.decorators import fetch_property
from ..Loadable import Loadable
from ..Asset import Asset
from .User import User


class TeamStatus(Enum):
    PUBLIC = "Public"
    PRIVATE = "Closed"
    INVITE_ONLY = "Invite Only"
    DISBANDED = "Disbanded"

    @staticmethod
    def from_string(value: str) -> "TeamStatus":
        status_switch = {
            "OPEN": TeamStatus.PUBLIC,
            "CLOSED": TeamStatus.PRIVATE,
            "FILTERED": TeamStatus.INVITE_ONLY,
            "DISBANDED": TeamStatus.DISBANDED,
        }
        return status_switch[value] if value in status_switch else None


class Team(Loadable):
    """A BTD6 Team."""
    endpoint = "/btd6/guild/{}"

    def _handle_exceptions(self, exception: Exception) -> None:
        error_msg = str(exception)
        if error_msg == "Invalid guild ID":
            raise NotFound(error_msg)

    def _parse_json(self, raw_resource: Dict[str, Any]) -> None:
        self._loaded = False

        copy_keys = ["name", "numMembers"]
        for key in copy_keys:
            self._data[key] = raw_resource[key]
        assets = [
            ("banner", "bannerURL"), ("icon", "iconURL"), ("frame", "frameURL"),
        ]
        for asset_name, asset_url in assets:
            self._data[asset_name] = Asset(raw_resource[asset_name], raw_resource[asset_url])
        self._data["status"] = TeamStatus.from_string(raw_resource["status"])
        self._data["owner_id"] = raw_resource["owner"].split("/")[-1]

        self._loaded = True

    @property
    @fetch_property(Loadable.load_resource)
    def name(self) -> str:
        """The name of the team."""
        return self._data["name"]

    @property
    @fetch_property(Loadable.load_resource)
    def member_count(self) -> int:
        """The team's member count."""
        return self._data["numMembers"]

    @property
    @fetch_property(Loadable.load_resource)
    def status(self) -> TeamStatus:
        """The team's entry status (public, closed, ...)."""
        return self._data["status"]

    @property
    @fetch_property(Loadable.load_resource)
    def banner(self) -> Asset:
        """The team's equipped banner."""
        return self._data["banner"]

    @property
    @fetch_property(Loadable.load_resource)
    def icon(self) -> Asset:
        """The team's equipped icon."""
        return self._data["icon"]

    @property
    @fetch_property(Loadable.load_resource)
    def frame(self) -> Asset:
        """The team's equipped frame."""
        return self._data["frame"]

    @property
    @fetch_property(Loadable.load_resource)
    def owner_id(self) -> str:
        """The ID of the user who currently owns the team."""
        return self._data["owner_id"]

    @fetch_property(Loadable.load_resource)
    def owner(self) -> User or None:
        """Fetch the owner of the team.

        .. warning::
           This function needs the property :attr:`~bloonspy.model.btd6.Team.owner_id` to be
           loaded, or it will make another API call to fetch that first.

        :return: The owner of the team.
        :rtype: User or None
        """
        if self.owner_id is None:
            return None
        return User(self.owner_id, eager=True)
