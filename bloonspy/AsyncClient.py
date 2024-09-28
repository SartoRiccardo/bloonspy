import asyncio
import aiohttp
from .utils.asyncapi import aget
from .model.btd6 import \
    OdysseyEvent, \
    BossEvent, \
    Race, \
    ContestedTerritoryEvent, Team, \
    Challenge, ChallengeFilter, \
    User, \
    CustomMap, CustomMapFilter


class AsyncClient:
    """Client for all **asynchronous** API calls.

    .. note::
       When accessing an unloaded property of a lazy-loaded resource, **it will**
       **raise ~bloonspy.exceptions.NotLoaded instead of loading it.** Either eager
       load it or call the load methods beforehand.

    :param open_access_key: Your OAK for the Ninja Kiwi Open Data API.
    :type open_access_key: str
    :param aiohttp_client: An aiohttp Client. Will create one if not provided.
    :type aiohttp_client: aiohttp.ClientSession
    """

    def __init__(self, open_access_key: str = None, aiohttp_client: aiohttp.ClientSession = None):
        self.__oak = open_access_key
        self.__aclient = aiohttp_client
        if self.__aclient is None:
            asyncio.create_task(self.__create_aclient())

    async def __create_aclient(self):
        async with aiohttp.ClientSession() as aclient:
            self.__aclient = aclient
            await asyncio.Future()

    async def odysseys(self) -> list[OdysseyEvent]:
        """Get a list of Odyssey events."""
        odysseys_data = await aget(self.__aclient, "/btd6/odyssey")
        odyssey_list = []
        for odyssey in odysseys_data:
            odyssey_list.append(OdysseyEvent(
                odyssey["id"],
                event_json=odyssey,
                async_client=self.__aclient,
            ))
        return odyssey_list

    async def get_odyssey(self, odyssey_id: str, eager: bool = False) -> OdysseyEvent:
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

        :return: The found odyssey.
        :rtype: ~bloonspy.model.btd6.OdysseyEvent

        :raise ~bloonspy.exceptions.NotFound: If no odyssey with that ID is found.
        """
        odyssey = OdysseyEvent(odyssey_id, async_client=self.__aclient)
        if eager:
            await odyssey.load_event()
        return odyssey

    async def contested_territories(self) -> list[ContestedTerritoryEvent]:
        """Get a list of Contested Territory events."""
        ct_data = await aget(self.__aclient, "/btd6/ct")
        ct_list = []
        for ct in ct_data:
            ct_list.append(ContestedTerritoryEvent(
                ct["id"],
                event_json=ct,
                async_client=self.__aclient,
            ))
        return ct_list

    async def get_contested_territory(self, ct_id: str, eager: bool = False) -> ContestedTerritoryEvent:
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

        :return: The found Contested Territory event.
        :rtype: ~bloonspy.model.btd6.ContestedTerritoryEvent

        :raise ~bloonspy.exceptions.NotFound: If no CT with that ID is found.
        """
        ct = ContestedTerritoryEvent(ct_id, async_client=self.__aclient)
        if eager:
            await ct.load_event()
        return ct

    async def get_team(self, team_id: str) -> Team:
        """Fetch a specific team by its ID.

        :param team_id: The ID of the team.
        :type team_id: str

        :return: The found team.
        :rtype: ~bloonspy.model.btd6.Team

        :raise ~bloonspy.exceptions.NotFound: If no team with that ID is found.
        """
        tm = Team(team_id, async_client=self.__aclient)
        await tm.load_resource()
        return tm

    async def races(self) -> list[Race]:
        """Get a list of Race events.

        .. note::
           The returned :class:`~bloonspy.model.btd6.Race` objects will only
           have the properties :attr:`~bloonspy.model.Loadable.id`, :attr:`~bloonspy.model.btd6.Race.name`,
           :attr:`~bloonspy.model.btd6.Race.start`, :attr:`~bloonspy.model.btd6.Race.end`, and
           :attr:`~bloonspy.model.btd6.Race.total_scores` loaded.
        """
        races_data = await aget(self.__aclient, "/btd6/races")
        race_list = []
        for race in races_data:
            race_list.append(Race(
                race["id"],
                race_json=race,
                async_client=self.__aclient,
            ))
        return race_list

    async def get_race(self, race_id: str, eager: bool = False) -> Race:
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

        :return: The found race.
        :rtype: ~bloonspy.model.btd6.Race

        :raise ~bloonspy.exceptions.NotFound: If no race with that ID is found.
        """
        race = Race(race_id, async_client=self.__aclient)
        if eager:
            await race.load_resource()
        return race

    async def bosses(self) -> list[BossEvent]:
        """Get a list of Boss events."""
        bosses_data = await aget(self.__aclient, "/btd6/bosses")
        boss_list = []
        for boss in bosses_data:
            boss_list.append(BossEvent(
                boss["id"],
                event_json=boss,
                async_client=self.__aclient,
            ))
        return boss_list

    async def get_boss(self, boss_id: str, eager: bool = False) -> BossEvent:
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

        :return: The found Boss event.
        :rtype: ~bloonspy.model.btd6.BossEvent

        :raise ~bloonspy.exceptions.NotFound: If no boss event with that ID is found.
        """
        boss = BossEvent(boss_id, async_client=self.__aclient)
        if eager:
            await boss.load_event()
        return boss

    async def challenges(
            self,
            challenge_filter: ChallengeFilter,
            pages: int = 1,
            start_from_page: int = 1
    ) -> list[Challenge]:
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
        :rtype: list[:class:`bloonspy.model.btd6.Challenge`]
        """

        challenge_list = []
        challenge_pages = []

        async def get_page(page_num: int) -> None:
            nonlocal challenge_pages
            challenge_pages.append(
                await aget(
                    self.__aclient,
                    f"/btd6/challenges/filter/{challenge_filter.value}",
                    {"page": page_num}
                )
            )

        await asyncio.gather(*[
            get_page(page_num) for page_num in range(start_from_page, start_from_page + pages)
        ])

        for page in challenge_pages:
            for chlg in page:
                challenge_list.append(Challenge(chlg["id"], name=chlg["name"], created_at=chlg["createdAt"],
                                                creator_id=chlg["creator"].split("/")[-1]))

        # Make async
        # if eager:
        #     with ThreadPoolExecutor(max_workers=10) as executor:
        #         futures = []
        #         for challenge in challenge_list:
        #             futures.append(executor.submit(challenge.load_resource))
        #         concurrent.futures.wait(futures)

        return challenge_list

    async def get_challenge(self, challenge_id: str) -> Challenge:
        """Fetch a specific challenge by its ID.

        :param challenge_id: The challenge ID.
        :type challenge_id: str

        :return: The found challenge.
        :rtype: ~bloonspy.model.btd6.Challenge

        :raise ~bloonspy.exceptions.NotFound: If no challenge with the given ID is found.
        """
        chal = Challenge(challenge_id, async_client=self.__aclient)
        await chal.load_resource()
        return chal

    async def get_user(self, identifier: str) -> User:
        """Fetch a specific user by an identifier.

        :param identifier: The user ID, or its OAK.
        :type identifier: str

        :return: The found user.
        :rtype: ~bloonspy.model.btd6.User

        :raise ~bloonspy.exceptions.NotFound: If no user with the given ID/OAK is found.
        """
        usr = User(identifier, async_client=self.__aclient)
        await usr.load_resource()
        return usr

    async def get_custom_map(self, map_id: str) -> CustomMap:
        """Fetch a specific custom map by its ID.

        :param map_id: The map code.
        :type map_id: str

        :return: The found map.
        :rtype: ~bloonspy.model.btd6.CustomMap

        :raise ~bloonspy.exceptions.NotFound: If no custom map with the given ID is found.
        """
        cmap = CustomMap(map_id, async_client=self.__aclient)
        await cmap.load_resource()
        return cmap

    async def custom_maps(
            self,
            custom_map_fliter: CustomMapFilter,
            pages: int = 1,
            start_from_page: int = 1
    ) -> list[CustomMap]:
        """Get a list of challenges given a specific filter.

        .. note::
           The returned :class:`~bloonspy.model.btd6.CustomMap` objects will only
           have the properties :attr:`~bloonspy.model.Loadable.id`, :attr:`~bloonspy.model.btd6.CustomMap.name`,
           and :attr:`~bloonspy.model.CustomMap.created_at` loaded.

        :param custom_map_fliter: Which type of custom maps you'd like to see.
        :type custom_map_fliter: ~bloonspy.model.btd6.CustomMapFilter
        :param pages: The number of pages to fetch.
        :type pages: int
        :param start_from_page: The page to start fetching from.
        :type start_from_page: int

        :return: A list of custom maps (lazy loaded).
        :rtype: list[:class:`bloonspy.model.btd6.CustomMap`]
        """

        custom_map_list = []
        custom_map_pages = []

        async def get_page(page_num: int) -> None:
            nonlocal custom_map_pages
            custom_map_pages.append(
                await aget(
                    self.__aclient,
                    f"/btd6/maps/filter/{custom_map_fliter.value}",
                    {"page": page_num}
                )
            )

        await asyncio.gather(*[
            get_page(page_num) for page_num in range(start_from_page, start_from_page + pages)
        ])

        for page in custom_map_pages:
            for cmap in page:
                custom_map_list.append(CustomMap(
                    cmap["id"],
                    name=cmap["name"],
                    created_at=cmap["createdAt"],
                    creator_id=cmap["creator"].split("/")[-1],
                    async_client=self.__aclient,
                ))

        return custom_map_list
