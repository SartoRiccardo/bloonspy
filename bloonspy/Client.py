import concurrent.futures
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
    def get_odyssey(odyssey_id: str, eager: bool = False) -> OdysseyEvent:
        """Fetch a specific Odyssey by its ID.

        .. note::
           If lazy loaded, the returned :class:`~bloonspy.model.btd6.OdysseyEvent` object will only
           have the property :attr:`~bloonspy.model.Event.id` loaded.

        :param odyssey_id: The ID of the odyssey.
        :type odyssey_id: str
        :param eager: If `True`, it loads all of the data right away. Set it to `False`
            if you want to limit API calls and don't need all the data. For more information,
            please read `Lazy and Eager Loading <async.html#lazy-and-eager-loading>`_.
        :type eager: bool

        :raise ~bloonspy.exceptions.NotFound: If no odyssey with that ID is found.

        :return: The found odyssey.
        :rtype: ~bloonspy.model.btd6.OdysseyEvent
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
    def get_contested_territory(ct_id: str, eager: bool = False) -> ContestedTerritoryEvent:
        """Fetch a specific Contested Territory event by its ID.

        .. note::
           If lazy loaded, the returned :class:`~bloonspy.model.btd6.ContestedTerritoryEvent` object will only
           have the property :attr:`~bloonspy.model.Lodable.id` loaded.

        :param ct_id: The ID of the event.
        :type ct_id: str
        :param eager: If `True`, it loads all of the data right away. Set it to `False`
            if you want to limit API calls and don't need all the data. For more information,
            please read `Lazy and Eager Loading <async.html#lazy-and-eager-loading>`_.
        :type eager: bool

        :raise ~bloonspy.exceptions.NotFound: If no CT with that ID is found.

        :return: The found Contested Territory event.
        :rtype: ~bloonspy.model.btd6.ContestedTerritoryEvent
        """
        return ContestedTerritoryEvent(ct_id, eager=eager)

    @staticmethod
    def get_team(team_id: str) -> Team:
        """Fetch a specific team by its ID.

        :param team_id: The ID of the team.
        :type team_id: str

        :raise ~bloonspy.exceptions.NotFound: If no team with that ID is found.

        :return: The found team.
        :rtype: ~bloonspy.model.btd6.Team
        """
        return Team(team_id, eager=True)

    @staticmethod
    def races() -> List[Race]:
        """Get a list of Race events.

        .. note::
           The returned :class:`~bloonspy.model.btd6.Race` objects will only
           have the properties :attr:`~bloonspy.model.Loadable.id`, :attr:`~bloonspy.model.btd6.Race.name`,
           :attr:`~bloonspy.model.btd6.Race.start`, :attr:`~bloonspy.model.btd6.Race.end`, and
           :attr:`~bloonspy.model.btd6.Race.total_scores` loaded.
        """
        races_data = get("/btd6/races")
        race_list = []
        for race in races_data:
            race_list.append(Race(race["id"], race_json=race))
        return race_list

    @staticmethod
    def get_race(race_id: str, eager: bool = False) -> Race:
        """Fetch a specific Race by its ID.

        .. note::
           If lazy loaded, the returned :class:`~bloonspy.model.btd6.Race` objects will only
           have the properties :attr:`~bloonspy.model.Loadable.id` loaded.

        :param race_id: The ID of the race.
        :type race_id: str
        :param eager: If `True`, it loads all of the data right away. Set it to `False`
            if you want to limit API calls and don't need all the data. For more information,
            please read `Lazy and Eager Loading <async.html#lazy-and-eager-loading>`_.
        :type eager: bool

        :raise ~bloonspy.exceptions.NotFound: If no race with that ID is found.

        :return: The found race.
        :rtype: ~bloonspy.model.btd6.Race
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
    def get_boss(boss_id: str, eager: bool = False) -> BossEvent:
        """Fetch a specific Boss event by its ID.

        .. note::
           If lazy loaded, the returned :class:`~bloonspy.model.btd6.BossEvent` objects will only
           have the property :attr:`~bloonspy.model.Loadable.id` loaded.

        :param boss_id: The boss ID.
        :type boss_id: str
        :param eager: If `True`, it loads all of the data right away. Set it to `False`
            if you want to limit API calls and don't need all the data. For more information,
            please read `Lazy and Eager Loading <async.html#lazy-and-eager-loading>`_.
        :type eager: bool

        :raise ~bloonspy.exceptions.NotFound: If no boss event with that ID is found.

        :return: The found Boss event.
        :rtype: ~bloonspy.model.btd6.BossEvent
        """
        return BossEvent(boss_id, eager=eager)

    @staticmethod
    def challenges(challenge_filter: ChallengeFilter, pages: int = 1, start_from_page: int = 1) -> List[Challenge]:
        """Get a list of challenges given a specific filter.
        
        .. note::
           The returned :class:`~bloonspy.model.btd6.Challenge` objects will only
           have the properties :attr:`~bloonspy.model.Loadable.id`, :attr:`~bloonspy.model.btd6.Challenge.name`,
           :attr:`~bloonspy.model.Challenge.created_at`, and :attr:`~bloonspy.model.Challenge.creator_id` loaded.

        :param challenge_filter: Which type of challenges you'd like to see.
        :type challenge_filter: ~bloonspy.model.btd6.ChallengeFilter
        :param pages: The number of pages to fetch.
        :type pages: int
        :param start_from_page: The page to start fetching from.
        :type start_from_page: int

        :return: A list of challenges (lazy loaded).
        :rtype: List[:class:`bloonspy.model.btd6.Challenge`]
        """

        challenge_list = []
        with ThreadPoolExecutor(max_workers=5) as executor:
            challenge_pages = []
            for page_num in range(start_from_page, start_from_page+pages):
                challenge_pages.append(executor.submit(
                    get, f"/btd6/challenges/filter/{challenge_filter.value}", {"page": page_num}
                ))
            for page in challenge_pages:
                for chlg in page.result():
                    challenge_list.append(Challenge(chlg["id"], name=chlg["name"], created_at=chlg["createdAt"],
                                                    creator_id=chlg["creator"].split("/")[-1]))
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

        :raise ~bloonspy.exceptions.NotFound: If no challenge with the given ID is found.

        :return: The found challenge.
        :rtype: ~bloonspy.model.btd6.Challenge
        """
        return Challenge(challenge_id, eager=True)

    @staticmethod
    def get_user(identifier: str) -> User:
        """Fetch a specific user by an identifier.

        :param identifier: The user ID, or its OAK.
        :type identifier: str

        :raise ~bloonspy.exceptions.NotFound: If no user with the given ID/OAK is found.

        :return: The found user.
        :rtype: ~bloonspy.model.btd6.User
        """
        return User(identifier, eager=True)
