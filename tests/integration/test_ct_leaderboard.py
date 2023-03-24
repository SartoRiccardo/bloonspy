import unittest
import random
from bloonspy import btd6, Client


class TestCtLeaderboard(unittest.TestCase):
    def test_ct_leaderboard(self) -> None:
        """
        Test a CT event's leaderboard.
        """
        cts = Client.contested_territories()
        ct_event = cts[1]
        # Get #51-#100
        ct_leaderboard_team = ct_event.leaderboard_team(pages=2, start_from_page=2)
        ct_leaderboard_player = ct_event.leaderboard_player(pages=2, start_from_page=2)

        self.assertGreater(len(ct_leaderboard_player), 0)
        some_player = ct_leaderboard_player[random.randint(0, len(ct_leaderboard_player)-1)]
        self.assertIsInstance(some_player, btd6.CtPlayer,
                              msg=f"Assert if result is CtPlayer")

        check_instance = [
            ("name", str), ("score", int), ("achievements", int), ("boss_normal_medals", btd6.EventMedals)
        ]
        for attr_name, attr_type in check_instance:
            self.assertIsInstance(getattr(some_player, attr_name), attr_type,
                                  msg=f"Assert if CtPlayer.{attr_name} is {attr_type}")

        self.assertGreater(len(ct_leaderboard_team), 0)
        some_team = ct_leaderboard_team[random.randint(0, len(ct_leaderboard_team)-1)]
        self.assertIsInstance(some_team, btd6.CtTeam,
                              msg=f"Assert if result is CtTeam")

        check_instance = [
            ("name", str), ("score", int), ("member_count", int), ("status", btd6.TeamStatus)
        ]
        for attr_name, attr_type in check_instance:
            self.assertIsInstance(getattr(some_team, attr_name), attr_type,
                                  msg=f"Assert if CtTeam.{attr_name} is {attr_type}")


if __name__ == '__main__':
    unittest.main()
