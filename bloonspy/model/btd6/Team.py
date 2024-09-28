from typing import Awaitable, Any
from enum import Enum
from ...exceptions import NotFound
from ...utils.decorators import fetch_property
from ..Loadable import Loadable
from ..Asset import Asset
from .User import User


class TeamStatus(Enum):
    """Entrance status of a team."""
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

    @staticmethod
    def parse_team_name(team_name: str) -> str:
        if " (disbanded)" in team_name:
            team_name = team_name.replace(" (disbanded)", "")
        if "-" in team_name:
            team_name = team_name.split("-")[0]
        return team_name.upper()

    def _parse_json(self, raw_resource: dict[str, Any]) -> None:
        self._loaded = False

        copy_keys = ["numMembers"]
        for key in copy_keys:
            self._data[key] = raw_resource[key]

        self._data["full_name"] = raw_resource["name"]
        self._data["name"] = self.parse_team_name(raw_resource["name"])

        assets = [
            ("banner", "bannerURL"), ("icon", "iconURL"), ("frame", "frameURL"),
        ]
        for asset_name, asset_url in assets:
            self._data[asset_name] = Asset(raw_resource[asset_name], raw_resource[asset_url])
        self._data["status"] = TeamStatus.from_string(raw_resource["status"])
        self._data["owner_id"] = raw_resource["owner"].split("/")[-1]

        self._loaded = True

    @property
    def is_disbanded(self) -> bool:
        """
        *New in 0.6.1.*

        Shortcut for `status == TeamStatus.DISBANDED`.
        If you're fetching a team through the leaderboard, it has the advantage of
        not causing an extra API call to fetch the `status` property.
        """
        return "(disbanded)" in self.full_name

    @property
    @fetch_property(Loadable.load_resource, should_load=Loadable._should_load_property("full_name"))
    def full_name(self) -> str:
        """
        The complete name of the team.
        It may not be exactly what you see in game, in some cases it has
        the team code appended at the end, among other things.
        """
        return self._data["full_name"]

    @property
    @fetch_property(Loadable.load_resource, should_load=Loadable._should_load_property("name"))
    def name(self) -> str:
        """The name of the team, as seen in-game."""
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
    def owner(self) -> Awaitable[User | None] | User | None:
        """Fetch the owner of the team.

        .. warning::
           This function needs the property :attr:`~bloonspy.model.btd6.Team.owner_id` to be
           loaded, or it will make another API call to fetch that first.

        :return: The owner of the team.
        :rtype: User or None
        """
        async def async_owner() -> User | None:
            if self.owner_id is None:
                return None
            usr = User(self.owner_id, async_client=self._async_client)
            await usr.load_resource()
            return usr

        if self._async_client:
            return async_owner()

        if self.owner_id is None:
            return None
        return User(self.owner_id, eager=True, async_client=self._async_client)
