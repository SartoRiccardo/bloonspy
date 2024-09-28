import aiohttp
from bloonspy import AsyncClient
from bloonspy.exceptions import Forbidden
from bloonspy import btd6


class TestUserSave:
    async def test_usersave(self) -> None:
        """
        Test that an user is loaded correctly.
        """
        async with aiohttp.ClientSession() as cs:
            client = AsyncClient(aiohttp_client=cs)
            oak = "oak_99b202be126fb7ad580a"
            user = await client.get_user(oak)
            user_save = await user.get_progress()
            assert isinstance(user_save, btd6.UserSave), \
                "Client.get_user().get_progress() should return UserSave"

    async def test_usersave_not_id(self) -> None:
        """
        Test that a Forbidden error will be thrown upon trying to get the save of an User identified by ID, not OAK.
        """
        async with aiohttp.ClientSession() as cs:
            client = AsyncClient(aiohttp_client=cs)
            uid = "9fbf41dedac0aba64a408f4a5877e577c55618bb9616dc39"

            thrown = False
            try:
                user = await client.get_user(uid)
                await user.get_progress()
            except Forbidden:
                thrown = True
            assert thrown, "Assert that Forbidden is thrown when getting the save data of an User identified by ID"


