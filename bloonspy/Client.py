from typing import List
from .utils.api import get
from .model.btd6 import \
    OdysseyEvent, \
    Boss, BossEvent, \
    Race, \
    ContestedTerritoryEvent, Team, \
    Challenge, ChallengeFilter, \
    User


class Client:
    def __init__(self, open_access_key: str):
        self.__oak = open_access_key

    @staticmethod
    def odysseys() -> List[OdysseyEvent]:
        odysseys_data = get("/btd6/odyssey")
        odyssey_list = []
        for odyssey in odysseys_data:
            odyssey_list.append(OdysseyEvent(odyssey["id"], event_json=odyssey))
        return odyssey_list

    @staticmethod
    def get_odyssey(odyssey_id: str, eager: bool = False) -> OdysseyEvent:
        return OdysseyEvent(odyssey_id, eager=eager)

    @staticmethod
    def contested_territories() -> List[ContestedTerritoryEvent]:
        ct_data = get("/btd6/ct")
        ct_list = []
        for ct in ct_data:
            ct_list.append(ContestedTerritoryEvent(ct["id"], event_json=ct))
        return ct_list

    @staticmethod
    def get_contested_territory(ct_id: str, eager: bool = False) -> ContestedTerritoryEvent:
        return ContestedTerritoryEvent(ct_id, eager=eager)

    @staticmethod
    def get_team(team_id: str) -> Team:
        return Team(team_id, eager=True)

    @staticmethod
    def races() -> List[Race]:
        races_data = get("/btd6/races")
        race_list = []
        for race in races_data:
            race_list.append(Race(race["id"], race_json=race))
        return race_list

    @staticmethod
    def get_race(race_id: str, eager: bool = False) -> Race:
        return Race(race_id, eager=eager)

    @staticmethod
    def bosses() -> List[BossEvent]:
        bosses_data = get("/btd6/bosses")
        boss_list = []
        for boss in bosses_data:
            boss_list.append(BossEvent(boss["id"], event_json=boss))
        return boss_list

    @staticmethod
    def get_boss(boss_id: str, eager: bool = False) -> BossEvent:
        return BossEvent(boss_id, eager=eager)

    @staticmethod
    def challenges(challenge_filter: ChallengeFilter, eager: bool = False) -> List[Challenge]:
        challenges_data = get(f"/btd6/challenges/filter/{challenge_filter.value}")
        challenge_list = []
        for race in challenges_data:
            challenge_list.append(Challenge(race["id"], name=race["name"], created_at=race["createdAt"],
                                            creator_id=race["creator"].split("/")[-1]))
        if eager:
            # TODO Load them all concurrently instead of sequentially
            for challenge in challenge_list:
                challenge.load_resource()
        return challenge_list

    @staticmethod
    def get_challenge(challenge_id: str) -> Challenge:
        return Challenge(challenge_id, eager=True)

    @staticmethod
    def get_user(identifier: str) -> User:
        return User(identifier, eager=True)
