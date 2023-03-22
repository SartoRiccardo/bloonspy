import unittest
from datetime import datetime
import requests
import bloonspy
from bloonspy import btd6


class TestOdyssey(unittest.TestCase):
    def test_odyssey(self) -> None:
        """
        Test that an odyssey event is loaded correctly.
        """
        odysseys = requests.get("https://data.ninjakiwi.com/btd6/odyssey")
        odyssey_id = odysseys.json()["body"][0]["id"]
        odyssey = btd6.OdysseyEvent(odyssey_id)

        check_instance = [
            ("name", str), ("start", datetime), ("end", datetime), ("id", str)
        ]
        for attr_name, attr_type in check_instance:
            self.assertIsInstance(getattr(odyssey, attr_name), attr_type,
                                  msg=f"Assert if OdysseyEvent.{attr_name} is {attr_type}")

        easy_mode = odyssey.easy()
        medium_mode = odyssey.medium(eager=True)
        hard_mode = odyssey.hard()

        check_instance = [
            ("name", str), ("difficulty", btd6.OdysseyDifficulty), ("is_extreme", bool), ("max_monkey_seats", int),
            ("max_boat_seats", int), ("max_power_slots", int), ("starting_lives", int)
        ]
        for attr_name, attr_type in check_instance:
            self.assertIsInstance(getattr(hard_mode, attr_name), attr_type,
                                  msg=f"Assert if Odyssey.{attr_name} is {attr_type}")

        for power in medium_mode.available_powers.keys():
            self.assertIsInstance(power, btd6.Power,
                                  msg=f"Assert if Odyssey.available_powers is Dict[Power, int]")
            self.assertIsInstance(medium_mode.available_powers[power], int,
                                  msg=f"Assert if Odyssey.available_powers is Dict[Power, int]")

        for power in medium_mode.default_powers.keys():
            self.assertIsInstance(power, btd6.Power,
                                  msg=f"Assert if Odyssey.default_powers is Dict[Power, int]")
            self.assertIsInstance(medium_mode.available_powers[power], int,
                                  msg=f"Assert if Odyssey.default_powers is Dict[Power, int]")

        for tower in medium_mode.default_towers.keys():
            self.assertIsInstance(tower, btd6.Tower,
                                  msg=f"Assert if Odyssey.default_towers is Dict[Tower, int]")
            self.assertIsInstance(medium_mode.default_towers[tower], int,
                                  msg=f"Assert if Odyssey.default_towers is Dict[Tower, int]")

        for power in medium_mode.available_towers.keys():
            self.assertIsInstance(power, btd6.Tower,
                                  msg=f"Assert if Odyssey.available_towers is Dict[Tower, Restriction]")
            self.assertIsInstance(medium_mode.available_towers[power], btd6.Restriction,
                                  msg=f"Assert if Odyssey.available_towers is Dict[Tower, Restriction]")

        maps = easy_mode.maps()
        self.assertGreater(len(maps), 0)
        for island in maps:
            self.assertIsInstance(island, btd6.Challenge,
                                  msg="Assert if Odyssey.maps returns List[Challenge]")

    def test_odyssey_fail(self) -> None:
        """
        Test that the correct exception is raised when attempting to fetch a nonexistant/expired odyssey.
        """
        team_id = "blatantlywrongodysseyid"
        correct_exception = False
        try:
            btd6.OdysseyEvent(team_id, eager=True)
        except btd6.NotFound:
            correct_exception = True
        self.assertTrue(correct_exception, msg="Wrong odyssey IDs should raise bloonspy.exceptions.NotFound")


if __name__ == '__main__':
    unittest.main()
