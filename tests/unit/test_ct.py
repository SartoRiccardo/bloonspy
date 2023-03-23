import unittest
from datetime import datetime
import requests
import bloonspy
from bloonspy import btd6


class TestCt(unittest.TestCase):
    def test_ct(self) -> None:
        """
        Test that a CT event event is loaded correctly.
        """
        ct_list = requests.get("https://data.ninjakiwi.com/btd6/ct")
        ct_id = ct_list.json()["body"][0]["id"]
        ct = btd6.ContestedTerritoryEvent(ct_id)

        check_instance = [
            ("name", str), ("start", datetime), ("end", datetime), ("id", str), ("total_scores_player", int),
            ("total_scores_team", int), ("event_number", int)
        ]
        for attr_name, attr_type in check_instance:
            self.assertIsInstance(getattr(ct, attr_name), attr_type,
                                  msg=f"Assert if ContestedTerritoryEvent.{attr_name} is {attr_type}")

    def test_ct_fail(self) -> None:
        """
        Test that the correct exception is raised when attempting to fetch a nonexistant/expired CT event.
        """
        ct_id = "l76rtr72"
        correct_exception = False
        try:
            btd6.ContestedTerritoryEvent(ct_id, eager=True)
        except btd6.NotFound:
            correct_exception = True
        self.assertTrue(correct_exception, msg="Wrong/expired CT IDs should raise bloonspy.exceptions.NotFound")


if __name__ == '__main__':
    unittest.main()
