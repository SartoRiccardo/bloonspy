import aiohttp
from bloonspy import btd6, AsyncClient
from bloonspy.exceptions import NotLoaded


class TestFetchOdyssey:
    async def test_odyssey(self) -> None:
        """
        Test getting a random odyssey.
        """
        async with aiohttp.ClientSession() as cs:
            client = AsyncClient(aiohttp_client=cs)
            odysseys = await client.odysseys()
            some_odyssey = odysseys[0]
            assert isinstance(some_odyssey, btd6.OdysseyEvent), f"Assert if Client.odysseys returns list[OdysseyEvent]"

            some_other_odyssey = await client.get_odyssey(odysseys[1].id)
            assert isinstance(some_other_odyssey, btd6.OdysseyEvent), \
                f"Assert if Client.get_odyssey returns OdysseyEvent"

    async def test_odyssey_challenge(self) -> None:
        """
        Test getting an odyssey's islands' challenge data.
        """
        async with aiohttp.ClientSession() as cs:
            client = AsyncClient(aiohttp_client=cs)
            odysseys = await client.odysseys()
            some_odyssey = odysseys[0]
            easy_version = await some_odyssey.easy(eager=True)

            islands = await easy_version.maps()
            assert isinstance(islands[0], btd6.Challenge), f"Assert if Odyssey.maps returns list[Challenge]"

    async def test_lazy_load_access(self) -> None:
        """
        Test lazy loading a resource.
        """
        async with aiohttp.ClientSession() as cs:
            client = AsyncClient(aiohttp_client=cs)
            odysseys = await client.odysseys()
            some_odyssey = odysseys[0]
            easy_version = await some_odyssey.easy()

            try:
                easy_version.is_extreme
                assert False, "Did not raise NotLoaded when calling unloaded resource"
            except NotLoaded:
                assert True

    async def test_eager_load_access(self) -> None:
        """
        Test eager loading a resource.
        """
        async with aiohttp.ClientSession() as cs:
            client = AsyncClient(aiohttp_client=cs)
            odysseys = await client.odysseys()
            some_odyssey = odysseys[0]
            medium_version = await some_odyssey.medium(eager=True)
            try:
                medium_version.is_extreme
            except NotLoaded:
                assert False, "Raised NotLoaded when calling loaded resource"

