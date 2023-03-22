from typing import List
import requests
from .model.btd6 import \
    OdysseyEvent, \
    Boss, BossEvent, \
    Race, \
    ContestedTerritory, Team, \
    Challenge, ChallengeFilter, \
    User


class Client:
    def __init__(self, open_access_key: str):
        self.__oak = open_access_key

    @staticmethod
    def odysseys() -> List[OdysseyEvent]:
        resp = requests.get("https://data.ninjakiwi.com/btd6/odyssey")
        odysseys_data = resp.json()

        odyssey_list = []
        for odyssey in odysseys_data["body"]:
            odyssey_list.append(OdysseyEvent(odyssey["id"], event_json=odyssey))
        return odyssey_list

    @staticmethod
    def get_odyssey(odyssey_id: str) -> OdysseyEvent:
        return OdysseyEvent(odyssey_id, eager=True)

    # @staticmethod
    # def contested_territories() -> List[ContestedTerritory]:
    #     return []
    #
    # @staticmethod
    # def get_contested_territory(ct_id: str, eager: bool = False) -> ContestedTerritory:
    #     return None

    @staticmethod
    def get_team(team_id: str) -> Team:
        return Team(team_id, eager=True)

    @staticmethod
    def races() -> List[Race]:
        resp = requests.get("https://data.ninjakiwi.com/btd6/races")
        races_data = resp.json()

        race_list = []
        for race in races_data["body"]:
            race_list.append(Race(race["id"], race_json=race))
        return race_list

    @staticmethod
    def get_race(race_id: str, eager: bool = False) -> Race:
        return Race(race_id, eager=eager)

    @staticmethod
    def bosses() -> List[BossEvent]:
        resp = requests.get("https://data.ninjakiwi.com/btd6/bosses")
        bosses_data = resp.json()

        boss_list = []
        for boss in bosses_data["body"]:
            boss_list.append(BossEvent(boss["id"], boss_json=boss))
        return boss_list

    @staticmethod
    def get_boss(boss_id: str, eager: bool = False) -> BossEvent:
        return BossEvent(boss_id, eager=eager)

    @staticmethod
    def challenges(challenge_filter: ChallengeFilter, eager: bool = False) -> List[Challenge]:
        resp = requests.get(f"https://data.ninjakiwi.com/btd6/challenges/filter/{challenge_filter.value}")
        challenges_data = resp.json()

        challenge_list = []
        for race in challenges_data["body"]:
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
