import unittest
from datetime import datetime
import requests
from bloonspy import btd6


class TestRace(unittest.TestCase):
    def test_race(self) -> None:
        """
        Test that a race is loaded correctly.
        """
        races = requests.get("https://data.ninjakiwi.com/btd6/races")
        race_id = races.json()["body"][0]["id"]
        race = btd6.Race(race_id)

        check_instance = [
            ("name", str), ("start", datetime), ("end", datetime), ("total_scores", int),
            ("total_scores", int), ("gamemode", btd6.Gamemode)
        ]
        for attr_name, attr_type in check_instance:
            self.assertIsInstance(getattr(race, attr_name), attr_type,
                                  msg=f"Assert if Race.{attr_name} is {attr_type}")

    def test_race_expired(self) -> None:
        """
        Test that the correct exception is raised when attempting to fetch a nonexistant/expired race.
        """
        race_id = "Uncracked_lctxs1bb"
        correct_exception = False
        try:
            btd6.Race(race_id, eager=True)
        except btd6.NotFound:
            correct_exception = True
        self.assertTrue(correct_exception, msg="Wrong/expired race IDs should raise bloonspy.exceptions.NotFound")


if __name__ == '__main__':
    unittest.main()
