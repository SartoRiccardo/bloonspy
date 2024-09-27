import aiohttp
from bloonspy import AsyncClient


class TestChallengeCreator:
    async def test_challenge(self) -> None:
        """
        Test a challenge with a creator.
        """
        async with aiohttp.ClientSession() as session:
            client = AsyncClient(aiohttp_client=session)
            challenge = await client.get_challenge("ZMDCDTB")
            creator = await challenge.creator()
            assert creator.name == "Sarto"
            assert creator.id == "9cee138c8c94ffac1910864c0b73e577ca554ce8cb18db6c"

    async def test_challenge_no_creator(self) -> None:
        """
        Test a challenge with a missing creator.
        """
        async with aiohttp.ClientSession() as session:
            client = AsyncClient(aiohttp_client=session)
            challenge = await client.get_challenge("rot168220230320")
            creator = await challenge.creator()
            assert creator is None

