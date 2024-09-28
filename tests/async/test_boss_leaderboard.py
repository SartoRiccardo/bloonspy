from datetime import datetime
import random
import aiohttp
from bloonspy import btd6, AsyncClient


class TestBossLeaderboard:
    async def test_boss_leaderboard(self) -> None:
        """
        Test fetching a boss' leaderboard.
        """
        async with aiohttp.ClientSession() as session:
            client = AsyncClient(aiohttp_client=session)
            bosses = await client.bosses()
            boss = bosses[1]
            # Get #51-#100
            standard_boss = await boss.standard()
            boss_leaderboard = await standard_boss.leaderboard(pages=2, start_from_page=2)

            assert len(boss_leaderboard) > 0
            some_player = boss_leaderboard[random.randint(0, len(boss_leaderboard)-1)]
            assert isinstance(some_player, btd6.BossPlayer), \
                "Assert if result is BossPlayer"

            check_instance = [
                ("name", str), ("score", btd6.Score), ("submission_time", datetime)
            ]
            for attr_name, attr_type in check_instance:
                assert isinstance(getattr(some_player, attr_name), attr_type), \
                    f"Assert if BossPlayer.{attr_name} is {attr_type}"

    async def test_boss_leaderboard_coop(self) -> None:
        """
        Test fetching a boss' coop leaderboard.
        """
        async with aiohttp.ClientSession() as session:
            client = AsyncClient(aiohttp_client=session)
            bosses = await client.bosses()
            boss = bosses[1]
            standard_boss = await boss.standard()
            assert isinstance(standard_boss, btd6.Boss), \
                "Assert BossEvent.standard() is a Boss"
            boss_leaderboard_coop = await standard_boss.leaderboard(pages=3, team_size=3)

            check_instance = [
                ("score", btd6.Score), ("submission_time", datetime), ("is_fully_loaded", bool)
            ]
            for i, team in enumerate(boss_leaderboard_coop):
                assert len(team.players) <= 3, \
                    "Assert if BossPlayerTeam has the correct number of players."
                for attr_name, attr_type in check_instance:
                    assert isinstance(getattr(team, attr_name), attr_type), \
                        f"Assert if BossPlayerTeam.{attr_name} is {attr_type}"
                    for player in team.players:
                        assert isinstance(player, btd6.BossPlayer), \
                            "Assert if BossPlayerTeam.players is a tuple of BossPlayer."
