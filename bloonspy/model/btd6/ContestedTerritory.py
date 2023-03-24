from datetime import datetime
from typing import List, Dict, Any
from concurrent.futures import ThreadPoolExecutor
from ...utils.decorators import fetch_property, exception_handler
from ...utils.api import get, get_lb_page
from ..Event import Event
from .User import User
from .Team import Team


class CtPlayer(User):
    def __init__(self, user_id: str, name: str, score: int, **kwargs):
        super().__init__(user_id, **kwargs)
        self._name = name
        self._score = score

    @property
    def name(self) -> str:
        return self._name

    @property
    def score(self) -> int:
        return self._score


class CtTeam(Team):
    def __init__(self, team_id: str, name: str, score: int, **kwargs):
        super().__init__(team_id, **kwargs)
        self._name = name
        self._score = score

    @property
    def name(self) -> str:
        return self._name

    @property
    def score(self) -> int:
        return self._score


class ContestedTerritoryEvent(Event):
    event_endpoint = "/btd6/ct"
    lb_endpoint_player = "/btd6/ct/{}/leaderboard/player"
    lb_endpoint_team = "/btd6/ct/{}/leaderboard/team"
    event_dict_keys = ["name", "start", "end", "totalScores_player", "totalScores_team"]
    event_name = "CT"

    def _parse_event(self, data: Dict[str, Any]) -> None:
        self._data["totalScores_player"] = data["totalScores_player"]
        self._data["totalScores_team"] = data["totalScores_team"]
        self._data["start"] = datetime.fromtimestamp(data["start"]/1000)
        self._data["end"] = datetime.fromtimestamp(data["end"]/1000)
        self._event_loaded = True

    @property
    def name(self) -> str:
        return f"Contested Territory #{self.event_number}"

    @property
    @fetch_property(Event.load_event, should_load=Event._should_load_property)
    def event_number(self) -> int:
        first_event_start = datetime.strptime('2022-08-09 22', '%Y-%m-%d %H')
        return int((self.start-first_event_start).days/14) + 1

    @property
    @fetch_property(Event.load_event, should_load=Event._should_load_property)
    def total_scores_player(self) -> int:
        return self._data["totalScores_player"]

    @property
    @fetch_property(Event.load_event, should_load=Event._should_load_property)
    def total_scores_team(self) -> int:
        return self._data["totalScores_team"]

    @exception_handler(Event.handle_exceptions)
    def leaderboard_player(self, pages: int = 1, start_from_page: int = 0) -> List[CtPlayer]:
        futures = []
        with ThreadPoolExecutor(max_workers=10) as executor:
            for page_num in range(start_from_page, start_from_page + pages):
                futures.append(executor.submit(get_lb_page, self.lb_endpoint_player.format(self._id), page_num))

        players = []
        for page in futures:
            for player in page.result():
                players.append(CtPlayer(
                    player["profile"].split("/")[-1], player["displayName"], player["score"]
                ))

        return players

    @exception_handler(Event.handle_exceptions)
    def leaderboard_team(self, pages: int = 1, start_from_page: int = 0) -> List[CtTeam]:
        futures = []
        with ThreadPoolExecutor(max_workers=10) as executor:
            for page_num in range(start_from_page, start_from_page + pages):
                futures.append(executor.submit(get_lb_page, self.lb_endpoint_team.format(self._id), page_num))

        teams = []
        for page in futures:
            for team in page.result():
                teams.append(CtTeam(
                    team["profile"].split("/")[-1], team["displayName"], team["score"]
                ))

        return teams
