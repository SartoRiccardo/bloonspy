from datetime import datetime, timedelta
import requests
from typing import List, Dict, Any
from ...utils.decorators import fetch_property
from ...utils.dictionaries import has_all_keys
from ...exceptions import NotFound
from .Challenge import Challenge
from .User import User


class RacePlayer(User):
    def __init__(self, user_id: str, name: str, score: int, submission_time: int, **kwargs):
        super().__init__(user_id, **kwargs)
        self._name = name
        self._score = timedelta(seconds=int(score/1000))
        self._submission_time = datetime.fromtimestamp(int(submission_time/1000))

    @property
    def name(self) -> str:
        return self._name

    @property
    def score(self) -> timedelta:
        return self._score

    @property
    def submission_time(self) -> datetime:
        return self._submission_time


class Race(Challenge):
    endpoint = "https://data.ninjakiwi.com/btd6/races/{}/metadata"
    event_endpoint = "https://data.ninjakiwi.com/btd6/races"
    lb_endpoint = "https://data.ninjakiwi.com/btd6/races/{}/leaderboard"

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

    def _load_race(self, only_if_unloaded: bool = True) -> None:
        if self._race_loaded and only_if_unloaded:
            return

        self._race_loaded = False

        resp = requests.get(self.event_endpoint)
        if resp.status_code != 200:
            return

        data = resp.json()
        if not data["success"]:
            self.handle_exceptions(data["error"])

        race_list = data["body"]
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

    def handle_exceptions(self, error_msg: str) -> None:
        if error_msg == "No Race with that ID exists":
            raise NotFound(error_msg)
        super().handle_exceptions(error_msg)

    @property
    @fetch_property(_load_race)
    def name(self) -> str:
        return self._data["name"]

    @property
    @fetch_property(_load_race)
    def start(self) -> datetime:
        return self._start

    @property
    @fetch_property(_load_race)
    def end(self) -> datetime:
        return self._end

    @property
    @fetch_property(_load_race)
    def total_scores(self) -> int:
        return self._total_scores

    def leaderboard(self, pages: int = 1, start_from_page: int = 0) -> List[RacePlayer]:
        race_players = []

        for page_num in range(start_from_page, start_from_page+pages):
            resp = requests.get(self.lb_endpoint.format(self._id), params={"page": page_num})
            page = resp.json()
            if not page["success"]:
                self.handle_exceptions(page["error"])
            for player in page["body"]:
                race_players.append(RacePlayer(
                    player["profile"].split("/")[-1], player["displayName"], player["score"], player["submissionTime"]
                ))

        return race_players
