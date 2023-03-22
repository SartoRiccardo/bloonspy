from dataclasses import dataclass, field
import requests
from enum import Enum
from datetime import datetime, timedelta
from typing import List, Dict, Any
from ...exceptions import NotFound
from ...utils.dictionaries import has_all_keys
from ...utils.decorators import fetch_property
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


class Boss(Challenge):
    endpoint = "https://data.ninjakiwi.com/btd6/bosses/{}/metadata/:difficulty:"
    lb_endpoint = "https://data.ninjakiwi.com/btd6/bosses/{}/leaderboard/:difficulty:/{}"

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
        return self._boss_bloon

    @property
    def total_scores(self) -> int:
        return self._total_scores

    @property
    def is_elite(self) -> bool:
        return self._is_elite

    def leaderboard(self, pages: int = 1, start_from_page: int = 0, team_size: int = 1) -> List[BossPlayer]:
        if team_size not in range(1, 5):
            raise ValueError("team_size must be between 1 and 4")

        boss_players = []

        for page_num in range(start_from_page, start_from_page + pages):
            resp = requests.get(self.lb_endpoint.format(self._id, team_size), params={"page": page_num})
            page = resp.json()
            if not page["success"]:
                self.handle_exceptions(page["error"])
            for player in page["body"]:
                boss_players.append(BossPlayer(
                    player["profile"].split("/")[-1], player["displayName"], player["score"], player["submissionTime"]
                ))

        return boss_players


class BossEvent:
    event_endpoint = "https://data.ninjakiwi.com/btd6/bosses"

    def __init__(self, boss_id: str, eager: bool = False, boss_json: Dict[str, Any] = None):
        self._id = boss_id

        self._data = {}

        self._boss_loaded = False
        if boss_json and has_all_keys(boss_json, ["name", "bossType", "bossTypeURL", "start", "end", "totalScores_stanaard",
                                                  "totalScores_elite"]):
            self._parse_boss(boss_json)
        if eager and not self._boss_loaded:
            self._load_boss()

    def _load_boss(self, only_if_unloaded: bool = True) -> None:
        if self._boss_loaded and only_if_unloaded:
            return

        self._boss_loaded = False

        resp = requests.get(self.event_endpoint)
        if resp.status_code != 200:
            return

        data = resp.json()
        if not data["success"]:
            self.handle_exceptions(data["error"])

        boss_list = data["body"]
        for boss in boss_list:
            if boss["id"] == self._id:
                self._parse_boss(boss)
                return

        raise NotFound("No Boss with that ID exists")

    def _parse_boss(self, data: Dict[str, Any]) -> None:
        self._data["name"] = data["name"]
        self._data["boss_bloon"] = BossBloon.from_string(data["bossType"])
        self._data["boss_banner"] = data["bossTypeURL"]
        self._data["start"] = datetime.fromtimestamp(data["start"]/1000)
        self._data["end"] = datetime.fromtimestamp(data["end"]/1000)
        self._data["total_scores_standard"] = data["totalScores_standard"]
        self._data["total_scores_elite"] = data["totalScores_elite"]
        self._boss_loaded = True

    def handle_exceptions(self, error_msg: str) -> None:
        if error_msg == "No Boss with that ID exists":
            raise NotFound(error_msg)
        super().handle_exceptions(error_msg)

    @staticmethod
    def _should_load_property(key_name: str) -> callable:
        def _inner(self: BossEvent) -> bool:
            return key_name not in self._data
        return _inner

    @property
    def id(self) -> str:
        return self._id

    @property
    @fetch_property(_load_boss, should_load=_should_load_property)
    def name(self) -> str:
        return self._data["name"]

    @property
    @fetch_property(_load_boss, should_load=_should_load_property)
    def boss_bloon(self) -> BossBloon:
        return self._data["boss_bloon"]

    @property
    @fetch_property(_load_boss, should_load=_should_load_property)
    def boss_banner(self) -> str:
        return self._data["boss_banner"]

    @property
    @fetch_property(_load_boss, should_load=_should_load_property)
    def start(self) -> datetime:
        return self._data["start"]

    @property
    @fetch_property(_load_boss, should_load=_should_load_property)
    def end(self) -> datetime:
        return self._data["end"]

    @property
    @fetch_property(_load_boss, should_load=_should_load_property)
    def total_scores_standard(self) -> int:
        return self._data["total_scores_standard"]

    @property
    @fetch_property(_load_boss, should_load=_should_load_property)
    def total_scores_elite(self) -> int:
        return self._data["total_scores_elite"]

    def standard(self, eager: bool = False) -> Boss:
        return Boss(self.id, self.name, self.boss_bloon,
                    self.total_scores_standard, False, eager=eager)

    def elite(self, eager: bool = False) -> Boss:
        return Boss(self.id, self.name, self.boss_bloon,
                    self.total_scores_elite, True, eager=eager)
