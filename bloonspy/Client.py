from typing import List
from concurrent.futures import ThreadPoolExecutor
from .utils.api import get
from .model.btd6 import \
    OdysseyEvent, \
    BossEvent, \
    Race, \
    ContestedTerritoryEvent, Team, \
    Challenge, ChallengeFilter, \
    User


class Client:
    """Client for all API calls.

    :param open_access_key: Your OAK for the Ninja Kiwi Open Data API.
    :type open_access_key: str
    """
    def __init__(self, open_access_key: str):
        self.__oak = open_access_key

    @staticmethod
    def odysseys() -> List[OdysseyEvent]:
        """Get a list of Odyssey events."""
        odysseys_data = get("/btd6/odyssey")
        odyssey_list = []
        for odyssey in odysseys_data:
            odyssey_list.append(OdysseyEvent(odyssey["id"], event_json=odyssey))
        return odyssey_list

    @staticmethod
    def get_odyssey(odyssey_id: str, eager: bool = True) -> OdysseyEvent:
        """Fetch a specific Odyssey by its ID.

        :param odyssey_id: The ID of the odyssey.
        :type odyssey_id: str
        :param eager: If `True`, it loads all of the data right away. Set it to `False`
            if you want to limit API calls and don't need all the data.
        :type eager: bool

        :raise bloonspy.exceptions.NotFound: If no odyssey with that ID is found.

        :return: The found odyssey.
        :rtype: bloonspy.model.btd6.OdysseyEvent
        """
        return OdysseyEvent(odyssey_id, eager=eager)

    @staticmethod
    def contested_territories() -> List[ContestedTerritoryEvent]:
        """Get a list of Contested Territory events."""
        ct_data = get("/btd6/ct")
        ct_list = []
        for ct in ct_data:
            ct_list.append(ContestedTerritoryEvent(ct["id"], event_json=ct))
        return ct_list

    @staticmethod
    def get_contested_territory(ct_id: str, eager: bool = True) -> ContestedTerritoryEvent:
        """Fetch a specific Contested Territory event by its ID.

        :param ct_id: The ID of the event.
        :type ct_id: str
        :param eager: If `True`, it loads all of the data right away. Set it to `False`
            if you want to limit API calls and don't need all the data.
        :type eager: bool

        :raise bloonspy.exceptions.NotFound: If no CT with that ID is found.

        :return: The found Contested Territory event.
        :rtype: bloonspy.model.btd6.ContestedTerritoryEvent
        """
        return ContestedTerritoryEvent(ct_id, eager=eager)

    @staticmethod
    def get_team(team_id: str) -> Team:
        """Fetch a specific team by its ID.

        :param team_id: The ID of the team.
        :type team_id: str

        :raise bloonspy.exceptions.NotFound: If no team with that ID is found.

        :return: The found team.
        :rtype: bloonspy.model.btd6.Team
        """
        return Team(team_id, eager=True)

    @staticmethod
    def races() -> List[Race]:
        """Get a list of Race events."""
        races_data = get("/btd6/races")
        race_list = []
        for race in races_data:
            race_list.append(Race(race["id"], race_json=race))
        return race_list

    @staticmethod
    def get_race(race_id: str, eager: bool = True) -> Race:
        """Fetch a specific Race by its ID.

        :param race_id: The ID of the race.
        :type race_id: str
        :param eager: If `True`, it loads all of the data right away. Set it to `False`
            if you want to limit API calls and don't need all the data.
        :type eager: bool

        :raise bloonspy.exceptions.NotFound: If no race with that ID is found.

        :return: The found race.
        :rtype: bloonspy.model.btd6.Race
        """
        return Race(race_id, eager=eager)

    @staticmethod
    def bosses() -> List[BossEvent]:
        """Get a list of Boss events."""
        bosses_data = get("/btd6/bosses")
        boss_list = []
        for boss in bosses_data:
            boss_list.append(BossEvent(boss["id"], event_json=boss))
        return boss_list

    @staticmethod
    def get_boss(boss_id: str, eager: bool = True) -> BossEvent:
        """Fetch a specific Boss event by its ID.

        :param boss_id: The boss ID.
        :type boss_id: str
        :param eager: If `True`, it loads all of the data right away. Set it to `False`
            if you want to limit API calls and don't need all the data.
        :type eager: bool

        :raise bloonspy.exceptions.NotFound: If no boss event with that ID is found.

        :return: The found Boss event.
        :rtype: bloonspy.model.btd6.BossEvent
        """
        return BossEvent(boss_id, eager=eager)

    @staticmethod
    def challenges(challenge_filter: ChallengeFilter, pages: int = 1, start_from_page: int = 1) -> List[Challenge]:
        """Get a list of challenges given a specific filter.

        :param challenge_filter: Which type of challenges you'd like to see.
        :type challenge_filter: bloonspy.model.btd6.ChallengeFilter
        :param pages: The number of pages to fetch.
        :type pages: int
        :param start_from_page: The page to start fetching from.
        :type start_from_page: int

        :return: A list of challenges (lazy loaded).
        :rtype: List[:class:`bloonspy.model.btd6.Challenge`]
        """
        challenges_data = get(f"/btd6/challenges/filter/{challenge_filter.value}")
        challenge_list = []
        for race in challenges_data:
            challenge_list.append(Challenge(race["id"], name=race["name"], created_at=race["createdAt"],
                                            creator_id=race["creator"].split("/")[-1]))
        # if eager:
        #     with ThreadPoolExecutor(max_workers=10) as executor:
        #         futures = []
        #         for challenge in challenge_list:
        #             futures.append(executor.submit(challenge.load_resource))
        #         concurrent.futures.wait(futures)

        return challenge_list

    @staticmethod
    def get_challenge(challenge_id: str) -> Challenge:
        """Fetch a specific challenge by its ID.

        :param challenge_id: The challenge ID.
        :type challenge_id: str

        :raise bloonspy.exceptions.NotFound: If no challenge with the given ID is found.

        :return: The found challenge.
        :rtype: bloonspy.model.btd6.Challenge
        """
        return Challenge(challenge_id, eager=True)

    @staticmethod
    def get_user(identifier: str) -> User:
        """Fetch a specific user by an identifier.

        :param identifier: The user ID, or its OAK.
        :type identifier: str

        :raise bloonspy.exceptions.NotFound: If no user with the given ID/OAK is found.

        :return: The found user.
        :rtype: bloonspy.model.btd6.User
        """
        return User(identifier, eager=True)
