from typing import List
import requests
from .model.btd6 import \
    Odyssey,\
    Boss, \
    Race, \
    ContestedTerritory, \
    Team, \
    Challenge, \
    ChallengeFilter, \
    User


class Client:
    def __init__(self, open_access_key: str):
        self.__oak = open_access_key

    @staticmethod
    def odysseys() -> List[Odyssey]:
        return []

    @staticmethod
    def get_odyssey(odyssey_id: str) -> Odyssey:
        return None

    @staticmethod
    def contested_territories() -> List[ContestedTerritory]:
        return []

    @staticmethod
    def get_contested_territory(ct_id: str, eager: bool = False) -> ContestedTerritory:
        return None

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
    def bosses() -> List[Boss]:
        return []

    @staticmethod
    def get_boss(boss_id: str, eager: bool = False) -> Boss:
        return None

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
