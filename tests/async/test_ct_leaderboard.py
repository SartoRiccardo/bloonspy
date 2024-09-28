import random

import aiohttp
from bloonspy import btd6, AsyncClient


class TestCtLeaderboard:
    async def test_ct_leaderboard(self) -> None:
        """
        Test a CT event's leaderboard.
        """
        async with aiohttp.ClientSession() as session:
            client = AsyncClient(aiohttp_client=session)
            cts = await client.contested_territories()
            ct_event = cts[1]
            # Get #51-#100
            ct_leaderboard_team = await ct_event.leaderboard_team(pages=2, start_from_page=2)
            ct_leaderboard_player = await ct_event.leaderboard_player(pages=2, start_from_page=2)

            assert len(ct_leaderboard_player) > 0
            some_player = ct_leaderboard_player[random.randint(0, len(ct_leaderboard_player)-1)]
            assert isinstance(some_player, btd6.CtPlayer), "Assert if result is CtPlayer"

            check_instance = [("name", str), ("score", int)]
            for attr_name, attr_type in check_instance:
                assert isinstance(getattr(some_player, attr_name), attr_type), \
                    f"Assert if CtPlayer.{attr_name} is {attr_type}"

            assert len(ct_leaderboard_team) > 0
            some_team = ct_leaderboard_team[random.randint(0, len(ct_leaderboard_team)-1)]
            assert isinstance(some_team, btd6.CtTeam), "Assert if result is CtTeam"

            check_instance = [("name", str), ("score", int)]
            for attr_name, attr_type in check_instance:
                assert isinstance(getattr(some_team, attr_name), attr_type), \
                    f"Assert if CtTeam.{attr_name} is {attr_type}"
