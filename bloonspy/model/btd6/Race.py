from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict, Any
from ...utils.decorators import fetch_property, exception_handler
from ...utils.dictionaries import has_all_keys
from ...utils.api import get, get_lb_page
from ...exceptions import NotFound
from .Challenge import Challenge
from .User import User


class RacePlayer(User):
    """An user who played a race and is now on the leaderboard.
    Inherits from :class:`~bloonspy.model.btd6.User`.
    """
    def __init__(self, user_id: str, name: str, score: int, submission_time: int, **kwargs):
        super().__init__(user_id, **kwargs)
        self._name = name
        self._score = timedelta(microseconds=score*1000)
        self._submission_time = datetime.fromtimestamp(int(submission_time/1000))

    @property
    def name(self) -> str:
        """The name of the user."""
        return self._name

    @property
    def score(self) -> timedelta:
        """The time the user got."""
        return self._score

    @property
    def submission_time(self) -> datetime:
        """The time the user's score was submitted at."""
        return self._submission_time


class Race(Challenge):
    """A race event. Inherits from :class:`~bloonspy.model.btd6.Challenge`."""

    endpoint = "/btd6/races/{}/metadata"
    event_endpoint = "/btd6/races"
    lb_endpoint = "/btd6/races/{}/leaderboard"

    def __init__(self, race_id: str, eager: bool = False, race_json: Dict[str, Any] = None):
        super().__init__(race_id, eager=eager)
        self._start = datetime.fromtimestamp(0)
        self._end = datetime.fromtimestamp(0)
        self._total_scores = 0
        self._race_loaded = eager
        if race_json and has_all_keys(race_json, ["name", "start", "end", "totalScores"]):
            self._parse_race(race_json)
        if eager and not self._race_loaded:
            self._load_race()

    def _handle_exceptions(self, exception: Exception) -> None:
        error_msg = str(exception)
        if error_msg == "No Race with that ID exists":
            raise NotFound(error_msg)

    @exception_handler(Challenge.handle_exceptions)
    def _load_race(self, only_if_unloaded: bool = True) -> None:
        if self._race_loaded and only_if_unloaded:
            return

        self._race_loaded = False

        race_list = get(self.event_endpoint)
        for race in race_list:
            if race["id"] == self._id:
                self._parse_race(race)
                return

        raise NotFound("No Race with that ID exists")

    def _parse_race(self, data: Dict[str, Any]) -> None:
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
    def leaderboard(self, pages: int = 1, start_from_page: int = 1) -> List[RacePlayer]:
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
        :rtype: List[:class:`~bloonspy.model.btd6.RacePlayer`]

        :raise ~bloonspy.exceptions.NotFound: If the race doesn't exist or is expired.
        """
        futures = []
        with ThreadPoolExecutor(max_workers=10) as executor:
            for page_num in range(start_from_page, start_from_page + pages):
                futures.append(executor.submit(get_lb_page, self.lb_endpoint.format(self._id), page_num))

        race_players = []
        for page in futures:
            for player in page.result():
                race_players.append(RacePlayer(
                    player["profile"].split("/")[-1], player["displayName"], player["score"], player["submissionTime"]
                ))

        return race_players
