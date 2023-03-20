from typing import List
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
    def get_team(team_id: str, eager: bool = False) -> Team:
        return None

    @staticmethod
    def race() -> List[Race]:
        return []

    @staticmethod
    def get_race(race_id: str, eager: bool = False) -> Race:
        return None

    @staticmethod
    def boss() -> List[Boss]:
        return []

    @staticmethod
    def get_boss(boss_id: str, eager: bool = False) -> Boss:
        return None

    @staticmethod
    def challenges(filter: ChallengeFilter) -> List[Challenge]:
        return []

    @staticmethod
    def get_challenge(challenge_id: str) -> Boss:
        return None

    @staticmethod
    def get_player(identifier: str) -> User:
        return None
