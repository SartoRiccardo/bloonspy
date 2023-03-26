import unittest
from datetime import datetime, timedelta
import requests
import random
from bloonspy import btd6, Client


class TestRaceLeaderboard(unittest.TestCase):
    def test_race_leaderboard(self) -> None:
        """
        Test getting a race event's leaderboard.
        """
        races = Client.races()
        race = races[1]
        # Get #51-#100
        race_leaderboard = race.leaderboard(pages=2, start_from_page=2)

        self.assertGreater(len(race_leaderboard), 0)
        some_player = race_leaderboard[random.randint(0, len(race_leaderboard)-1)]
        self.assertIsInstance(some_player, btd6.RacePlayer,
                              msg=f"Assert if result is RacePlayer")

        check_instance = [
            ("name", str), ("score", timedelta), ("submission_time", datetime),
            ("achievements", int), ("boss_normal_medals", btd6.EventMedals)
        ]
        for attr_name, attr_type in check_instance:
            self.assertIsInstance(getattr(some_player, attr_name), attr_type,
                                  msg=f"Assert if RacePlayer.{attr_name} is {attr_type}")


if __name__ == '__main__':
    unittest.main()
