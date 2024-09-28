from datetime import datetime
import aiohttp
import random
from bloonspy import btd6, AsyncClient


class TestRaceLeaderboard:
    async def test_race_leaderboard(self) -> None:
        """
        Test getting a race event's leaderboard.
        """
        async with aiohttp.ClientSession() as cs:
            client = AsyncClient(aiohttp_client=cs)
            races = await client.races()
            race = races[1]
            # Get #51-#100
            race_leaderboard = await race.leaderboard(pages=2, start_from_page=2)

            assert len(race_leaderboard) > 0
            some_player = race_leaderboard[random.randint(0, len(race_leaderboard)-1)]
            assert isinstance(some_player, btd6.RacePlayer), \
                "Assert if result is RacePlayer"

            check_instance = [
                ("name", str), ("score", btd6.Score), ("submission_time", datetime)
            ]
            for attr_name, attr_type in check_instance:
                assert (getattr(some_player, attr_name), attr_type), \
                    f"Assert if RacePlayer.{attr_name} is {attr_type}"

            some_player = race_leaderboard[random.randint(0, len(race_leaderboard)-1)]
            await some_player.load_resource()
            check_instance = [
                ("name", str), ("score", btd6.Score), ("submission_time", datetime),
                ("achievements", int), ("boss_normal_medals", btd6.EventMedals)
            ]
            for attr_name, attr_type in check_instance:
                assert (getattr(some_player, attr_name), attr_type), \
                    f"Assert if RacePlayer.{attr_name} is {attr_type}"
