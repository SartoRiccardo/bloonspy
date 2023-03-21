import unittest
from datetime import datetime, timedelta
import requests
import random
from bloonspy import btd6


class TestRaceLeaderboard(unittest.TestCase):
    def test_race_leaderboard(self) -> None:
        """
        Test a challenge with a creator.
        """
        races = requests.get("https://data.ninjakiwi.com/btd6/races")
        race_id = races.json()["body"][1]["id"]
        # Get #51-#100
        race_leaderboard = btd6.Race(race_id).leaderboard(pages=2, start_from_page=2)

        self.assertGreater(len(race_leaderboard), 0)
        some_player = race_leaderboard[random.randint(0, len(race_leaderboard))]
        self.assertIsInstance(some_player, btd6.RacePlayer,
                              msg=f"Assert if result is RacePlayer")

        check_instance = [
            ("name", str), ("score", timedelta), ("submission_time", datetime),
            ("achievements", int), ("boss_normal_medals", btd6.Medals)
        ]
        for attr_name, attr_type in check_instance:
            self.assertIsInstance(getattr(some_player, attr_name), attr_type,
                                  msg=f"Assert if RacePlayer.{attr_name} is {attr_type}")


if __name__ == '__main__':
    unittest.main()
