import random
import aiohttp
from datetime import datetime
from bloonspy import AsyncClient, ChallengeFilter


class TestChallengeBrowser:
    async def test_challenge_browser(self) -> None:
        """
        Test getting the newest challenges.
        """
        async with aiohttp.ClientSession() as session:
            client = AsyncClient(aiohttp_client=session)
            challenges = await client.challenges(ChallengeFilter.NEWEST, start_from_page=2, pages=2)
            assert len(challenges) > 0
            some_challenge = challenges[random.randint(0, len(challenges)-1)]

            check_instance = [
                ("name", str), ("created_at", datetime), ("wins", int), ("upvotes", int)
            ]
            for attr_name, attr_type in check_instance:
                assert isinstance(getattr(some_challenge, attr_name), attr_type), \
                    f"Assert if Challenge.{attr_name} is {attr_type}"


