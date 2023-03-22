import unittest
from datetime import datetime
import requests
from bloonspy import btd6


class TestBoss(unittest.TestCase):
    def test_boss(self) -> None:
        """
        Test that a boss is loaded correctly.
        """
        bosses = requests.get("https://data.ninjakiwi.com/btd6/bosses")
        boss_id = bosses.json()["body"][0]["id"]
        boss_event = btd6.BossEvent(boss_id)
        boss_standard = boss_event.standard()
        boss_elite = boss_event.elite()

        check_instance = [
            ("id", str), ("name", str), ("start", datetime), ("end", datetime), ("total_scores_standard", int),
            ("total_scores_elite", int), ("boss_banner", str), ("boss_bloon", btd6.BossBloon)
        ]
        for attr_name, attr_type in check_instance:
            self.assertIsInstance(getattr(boss_event, attr_name), attr_type,
                                  msg=f"Assert if BossEvent.{attr_name} is {attr_type}")

        check_instance = [
            ("total_scores", int), ("upvotes", int), ("plays_unique", int)
        ]
        for attr_name, attr_type in check_instance:
            self.assertIsInstance(getattr(boss_standard, attr_name), attr_type,
                                  msg=f"Assert if Boss.{attr_name} is {attr_type}")
            self.assertIsInstance(getattr(boss_elite, attr_name), attr_type,
                                  msg=f"Assert if Boss.{attr_name} is {attr_type}")

        self.assertFalse(boss_standard.is_elite)
        self.assertTrue(boss_elite.is_elite)

    def test_boss_expired(self) -> None:
        """
        Test that the correct exception is raised when attempting to fetch a nonexistant/expired boss.
        """
        boss_id = "Vortex10_l7si69ji"
        correct_exception = False
        try:
            btd6.BossEvent(boss_id, eager=True)
        except btd6.NotFound:
            correct_exception = True
        self.assertTrue(correct_exception, msg="Wrong/expired boss IDs should raise bloonspy.exceptions.NotFound")


if __name__ == '__main__':
    unittest.main()
