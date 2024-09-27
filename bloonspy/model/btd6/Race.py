import asyncio
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Awaitable
from ...utils.decorators import fetch_property, exception_handler
from ...utils.dictionaries import has_all_keys
from ...utils.api import get, get_lb_page
from ...utils.asyncapi import aget, aget_lb_page
from ...exceptions import NotFound
from .Challenge import Challenge
from .Score import Score
from .User import User


class RacePlayer(User):
    """An user who played a race and is now on the leaderboard.
    Inherits from :class:`~bloonspy.model.btd6.User`.
    """
    def __init__(self,
                 user_id: str,
                 name: str,
                 score: int,
                 score_parts: list[dict[str, Any]],
                 submission_time: int,
                 **kwargs):
        super().__init__(user_id, **kwargs)
        self._name = name
        self._score = timedelta(microseconds=score*1000)
        self._score_parts = [Score.from_json(sp) for sp in score_parts]
        self._submission_time = datetime.fromtimestamp(int(submission_time/1000))

    @property
    def name(self) -> str:
        """The name of the user."""
        return self._name

    @property
    def score(self) -> Score:
        """The time the user got."""
        return self._score_parts[0] if len(self._score_parts) > 0 else self._score

    @property
    def score_parts(self) -> list[Score]:
        """The score parts."""
        return self._score_parts

    @property
    def submission_time(self) -> datetime:
        """The time the user's score was submitted at."""
        return self._submission_time


class Race(Challenge):
    """A race event. Inherits from :class:`~bloonspy.model.btd6.Challenge`."""

    endpoint = "/btd6/races/{}/metadata"
    event_endpoint = "/btd6/races"
    lb_endpoint = "/btd6/races/{}/leaderboard"

    def __init__(
            self,
            race_id: str,
            eager: bool = False,
            race_json: dict[str, Any] = None,
            **kwargs,
    ):
        super().__init__(race_id, eager=eager, **kwargs)
        self._start = datetime.fromtimestamp(0)
        self._end = datetime.fromtimestamp(0)
        self._total_scores = 0
        self._race_loaded = eager
        if race_json and has_all_keys(race_json, ["name", "start", "end", "totalScores"]):
            self._parse_race(race_json)
        if eager and not self._race_loaded and self._async_client is None:
            self._load_race()

    def load_resource(self, only_if_unloaded: bool = True) -> Awaitable[None] | None:
        async def async_load():
            await super().load_resource(only_if_unloaded)
            await self._load_race(only_if_unloaded)

        if self._async_client:
            return async_load()
        super().load_resource(only_if_unloaded)
        self._load_race(only_if_unloaded)

    def _handle_exceptions(self, exception: Exception) -> None:
        error_msg = str(exception)
        if error_msg == "No Race with that ID exists":
            raise NotFound(error_msg)

    @exception_handler(Challenge.handle_exceptions)
    def _load_race(self, only_if_unloaded: bool = True) -> Awaitable[None] | None:
        if self._race_loaded and only_if_unloaded:
            return

        def on_data_load(data) -> None:
            for race in data:
                if race["id"] == self._id:
                    self._parse_race(race)
                    return
            raise NotFound("No Race with that ID exists")

        async def async_load() -> None:
            data = await aget(self._async_client, self.event_endpoint)
            on_data_load(data)

        self._race_loaded = False
        if self._async_client:
            return async_load()
        on_data_load(get(self.event_endpoint))

    def _parse_race(self, data: dict[str, Any]) -> None:
        self._data["name"] = data["name"]
        self._start = datetime.fromtimestamp(data["start"]/1000)
        self._end = datetime.fromtimestamp(data["end"]/1000)
        self._total_scores = data["totalScores"]
        self._race_loaded = True

    @property
    @fetch_property(_load_race)
    def name(self) -> str:
        """The name of the race."""
        return self._data["name"]

    @property
    @fetch_property(_load_race)
    def start(self) -> datetime:
        """When the event starts."""
        return self._start

    @property
    @fetch_property(_load_race)
    def end(self) -> datetime:
        """When the event ends."""
        return self._end

    @property
    @fetch_property(_load_race)
    def total_scores(self) -> int:
        """Number of users who played and submitted a score."""
        return self._total_scores

    @exception_handler(Challenge.handle_exceptions)
    def leaderboard(self, pages: int = 1, start_from_page: int = 1) -> list[RacePlayer] | Awaitable[list[RacePlayer]]:
        """Get a page of the leaderboard for this event.

        .. note::
           The returned :class:`~bloonspy.model.btd6.RacePlayer` objects will only
           have the properties :attr:`~bloonspy.model.Loadable.id`, :attr:`~bloonspy.model.btd6.Player.name`,
           :attr:`~bloonspy.model.RacePlayer.score`, and :attr:`~bloonspy.model.RacePlayer.submission_time` loaded.

        :param pages: Number of pages to fetch.
        :type pages: int
        :param start_from_page: The first page to fetch.
        :type start_from_page: int

        :return: A list of players in the leaderboard.
        :rtype: list[:class:`~bloonspy.model.btd6.RacePlayer`]

        :raise ~bloonspy.exceptions.NotFound: If the race doesn't exist or is expired.
        """
        def on_pages_fetched(responses) -> list[RacePlayer]:
            race_players = []
            for page in responses:
                for player in page.result():
                    race_players.append(RacePlayer(
                        player["profile"].split("/")[-1],
                        player["displayName"],
                        player["score"],
                        player["scoreParts"],
                        player["submissionTime"],
                        async_client=self._async_client,
                    ))
            return race_players

        async def async_get_leaderboard() -> list[RacePlayer]:
            results = await asyncio.gather(*[
                aget_lb_page(self._async_client, self.lb_endpoint.format(self._id), page_num)
                for page_num in range(start_from_page, start_from_page + pages)
            ])
            return on_pages_fetched(results)

        if self._async_client:
            return async_get_leaderboard()

        futures = []
        with ThreadPoolExecutor(max_workers=10) as executor:
            for page_num in range(start_from_page, start_from_page + pages):
                futures.append(executor.submit(get_lb_page, self.lb_endpoint.format(self._id), page_num))
        return on_pages_fetched([page.result() for page in futures])

