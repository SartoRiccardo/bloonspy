from enum import Enum
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
from typing import List, Dict, Any, Tuple, Union
from ...utils.decorators import fetch_property, exception_handler
from ...utils.api import get, get_lb_page
from ..Loadable import Loadable
from ..Event import Event
from .Challenge import Challenge
from .User import User


class BossBloon(Enum):
    BLOONARIUS = "bloonarius"
    LYCH = "lych"
    VORTEX = "vortex"
    DREADBLOON = "dreadbloon"
    # BLASTAPOPOULOS = "blastapopoulos"

    @staticmethod
    def from_string(boss: str) -> "BossBloon":
        boss_switch = {
            "vortex": BossBloon.VORTEX,
            "bloonarius": BossBloon.BLOONARIUS,
            "lych": BossBloon.LYCH,
            "dreadbloon": BossBloon.DREADBLOON,
        }
        boss = boss_switch[boss] if boss in boss_switch else None
        return boss


class BossPlayer(User):
    """An user who played the boss event and submitted a ranked score.
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
        """The time the user’s score was submitted at."""
        return self._submission_time


class BossPlayerTeam:
    """A team of players who played a Ranked Co-op Boss Event."""
    def __init__(self, users: List[BossPlayer], score: timedelta, submission_time: datetime, is_complete: bool = True):
        self._users = users
        self._score = score
        self._submission_time = submission_time
        self._is_complete = is_complete

    @property
    def players(self) -> Tuple[BossPlayer]:
        """The users in the team."""
        return tuple(self._users)

    @property
    def score(self) -> timedelta:
        """The time the team got."""
        return self._score

    @property
    def submission_time(self) -> datetime:
        """The time the team’s score was submitted at."""
        return self._submission_time

    @property
    def is_fully_loaded(self) -> bool:
        """Whether the team is fully loaded.

        Due to API restrictions, when calling :func:`~bloonspy.model.btd6.Boss.leaderboard()` to get coop
        leaderboards, the team at the end of the List could not have all of its members loaded.
        """
        return self._is_complete


class Boss(Challenge):
    """A Boss challenge. Inherits from :class:`~bloonspy.model.btd6.Challenge`."""
    endpoint = "/btd6/bosses/{}/metadata/:difficulty:"
    lb_endpoint = "/btd6/bosses/{}/leaderboard/:difficulty:/{}"

    def __init__(self, boss_id: str, name: str, boss_bloon: BossBloon, total_scores: int, elite: bool,
                 eager: bool = False):
        self._is_elite = elite
        self.endpoint = self.endpoint.replace(":difficulty:", "elite" if self._is_elite else "standard")
        self.lb_endpoint = self.lb_endpoint.replace(":difficulty:", "elite" if self._is_elite else "standard")
        super().__init__(boss_id, eager=eager)
        self._data["name"] = name
        self._boss_bloon = boss_bloon
        self._total_scores = total_scores

    @property
    def boss_bloon(self) -> BossBloon:
        """The boss in this challenge."""
        return self._boss_bloon

    @property
    def total_scores(self) -> int:
        """The total scores submitted."""
        return self._total_scores

    @property
    def is_elite(self) -> bool:
        """`True` if the boss is Elite."""
        return self._is_elite

    def _get_lb_page(self, page_num: int, team_size: int):
        try:
            return get(self.lb_endpoint.format(self._id, team_size), params={"page": page_num})
        except Exception as exc:
            if str(exc) == "No Scores Available":
                return []
            raise exc

    @exception_handler(Loadable.handle_exceptions)
    def leaderboard(self,
                    pages: int = 1,
                    start_from_page: int = 1,
                    team_size: int = 1
                    ) -> Union[List[BossPlayer], List[BossPlayerTeam]]:
        """Get a page of the leaderboard for this boss.

        .. note::
           The returned :class:`~bloonspy.model.btd6.BossPlayer` objects will only
           have the properties :attr:`~bloonspy.model.Loadable.id`, :attr:`~bloonspy.model.btd6.BossPlayer.name`,
           :attr:`~bloonspy.model.btd6.BossPlayer.score`, and :attr:`~bloonspy.model.btd6.BossPlayer.submission_time`
           loaded.

        :param pages: Number of pages to fetch.
        :type pages: int
        :param start_from_page: The first page to fetch.
        :type start_from_page: int
        :param team_size: The team size to get the leaderboard for.
        :type team_size: int

        :return: A list of players in the leaderboard.
        :rtype: Union[List[:class:`~bloonspy.model.btd6.BossPlayer`], List[:class:`~bloonspy.model.btd6.BossPlayerTeam`]]

        :raise ~bloonspy.exceptions.NotFound: If the boss doesn't exist or is expired.
        :raise ValueError: If `team_size` is less than 1 or more than 4.
        """
        if team_size not in range(1, 5):
            raise ValueError("team_size must be between 1 and 4")

        futures = []
        with ThreadPoolExecutor(max_workers=10) as executor:
            for page_num in range(start_from_page, start_from_page + pages):
                futures.append(executor.submit(get_lb_page, self.lb_endpoint.format(self._id, team_size), page_num))

        boss_players = []
        for page in futures:
            for player in page.result():
                boss_players.append(BossPlayer(
                    player["profile"].split("/")[-1], player["displayName"], player["score"], player["submissionTime"]
                ))

        if team_size > 1:
            boss_teams = []
            current_score = None
            current_sub_time = None
            current_team_players = []
            for player in boss_players:
                if player.score != current_score:
                    if current_score is not None:
                        boss_teams.append(
                            BossPlayerTeam(current_team_players, current_score, current_sub_time)
                        )
                    current_score = player.score
                    current_sub_time = player.submission_time
                    current_team_players = []

                current_team_players.append(player)

            if len(current_team_players) > 0:
                boss_teams.append(
                    BossPlayerTeam(current_team_players, current_score, current_sub_time,
                                   len(current_team_players) == team_size)
                )
            return boss_teams

        return boss_players


class BossEvent(Event):
    """A boss event. Inherits from :class:`~bloonspy.model.Event`."""
    event_endpoint = "/btd6/bosses"
    event_dict_keys = ["name", "bossType", "bossTypeURL", "start", "end", "totalScores_standard",
                       "totalScores_elite"]
    event_name: str = "Boss"

    def _parse_event(self, data: Dict[str, Any]) -> None:
        self._data["boss_bloon"] = BossBloon.from_string(data["bossType"])
        self._data["boss_banner"] = data["bossTypeURL"]
        self._data["total_scores_standard"] = data["totalScores_standard"]
        self._data["total_scores_elite"] = data["totalScores_elite"]
        super()._parse_event(data)

    @property
    @fetch_property(Event.load_event, should_load=Event._should_load_property)
    def boss_bloon(self) -> BossBloon:
        """The boss bloon in this event."""
        return self._data["boss_bloon"]

    @property
    @fetch_property(Event.load_event, should_load=Event._should_load_property)
    def boss_banner(self) -> str:
        """The URL to the banner used to advertise the event."""
        return self._data["boss_banner"]

    @property
    @fetch_property(Event.load_event, should_load=Event._should_load_property)
    def total_scores_standard(self) -> int:
        """Total scores submitted in the standard boss."""
        return self._data["total_scores_standard"]

    @property
    @fetch_property(Event.load_event, should_load=Event._should_load_property)
    def total_scores_elite(self) -> int:
        """Total scores submitted in the elite boss."""
        return self._data["total_scores_elite"]

    def standard(self, eager: bool = False) -> Boss:
        """Get the standard boss challenge.

        .. note::
           If lazy loaded, the returned :class:`~bloonspy.model.btd6.Boss` object will only
           have the properties :attr:`~bloonspy.model.Loadable.id`, :attr:`~bloonspy.model.btd6.Challenge.name`,
           :attr:`~bloonspy.model.Boss.boss_bloon`, :attr:`~bloonspy.model.Boss.is_elite`,
           and :attr:`~bloonspy.model.Boss.total_scores` loaded.

        :param eager: If `True`, it loads all of the data right away. Set it to `False`
            if you want to limit API calls and don't need all the data. For more information,
            please read `Lazy and Eager Loading <async.html#lazy-and-eager-loading>`_.
        :type eager: bool
        :return: The standard boss event.
        :rtype: ~bloonspy.model.btd6.Boss"""
        return Boss(self.id, self.name, self.boss_bloon,
                    self.total_scores_standard, False, eager=eager)

    def elite(self, eager: bool = False) -> Boss:
        """Get the elite boss challenge.

        .. note::
           If lazy loaded, the returned :class:`~bloonspy.model.btd6.Boss` object will only
           have the properties :attr:`~bloonspy.model.Loadable.id`, :attr:`~bloonspy.model.btd6.Challenge.name`,
           :attr:`~bloonspy.model.Boss.boss_bloon`, :attr:`~bloonspy.model.Boss.is_elite`,
           and :attr:`~bloonspy.model.Boss.total_scores` loaded.

        :param eager: If `True`, it loads all of the data right away. Set it to `False`
            if you want to limit API calls and don't need all the data. For more information,
            please read `Lazy and Eager Loading <async.html#lazy-and-eager-loading>`_.
        :type eager: bool
        :return: The elite boss event.
        :rtype: ~bloonspy.model.btd6.Boss"""
        return Boss(self.id, self.name, self.boss_bloon,
                    self.total_scores_elite, True, eager=eager)
