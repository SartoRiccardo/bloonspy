import unittest
from datetime import datetime, timedelta
import requests
import random
from bloonspy import btd6, Client


class TestBossLeaderboard(unittest.TestCase):
    def test_boss_leaderboard(self) -> None:
        """
        Test fetching a boss' leaderboard.
        """
        bosses = Client.bosses()
        boss = bosses[1]
        # Get #51-#100
        boss_leaderboard = boss.standard().leaderboard(pages=2, start_from_page=2)

        self.assertGreater(len(boss_leaderboard), 0)
        some_player = boss_leaderboard[random.randint(0, len(boss_leaderboard)-1)]
        self.assertIsInstance(some_player, btd6.BossPlayer,
                              msg=f"Assert if result is BossPlayer")

        check_instance = [
            ("name", str), ("score", timedelta), ("submission_time", datetime),
            ("achievements", int), ("boss_normal_medals", btd6.EventMedals)
        ]
        for attr_name, attr_type in check_instance:
            self.assertIsInstance(getattr(some_player, attr_name), attr_type,
                                  msg=f"Assert if BossPlayer.{attr_name} is {attr_type}")

    def test_boss_leaderboard_coop(self) -> None:
        """
        Test fetching a boss' coop leaderboard.
        """
        bosses = Client.bosses()
        boss = bosses[1]
        boss_leaderboard_coop = boss.standard().leaderboard(pages=3, team_size=3)

        check_instance = [
            ("score", timedelta), ("submission_time", datetime), ("is_fully_loaded", bool)
        ]
        for i in range(len(boss_leaderboard_coop)):
            team = boss_leaderboard_coop[i]
            self.assertLessEqual(len(team.players), 3,
                                 msg="Assert if BossPlayerTeam has the correct number of players.")
            for attr_name, attr_type in check_instance:
                self.assertIsInstance(getattr(team, attr_name), attr_type,
                                      msg=f"Assert if BossPlayerTeam.{attr_name} is {attr_type}")
                for player in team.players:
                    self.assertIsInstance(player, btd6.BossPlayer,
                                          msg="Assert if BossPlayerTeam.players is a tuple of BossPlayer.")


if __name__ == '__main__':
    unittest.main()
