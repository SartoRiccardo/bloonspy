import unittest
from datetime import datetime
import bloonspy
from bloonspy import btd6


class TestTeam(unittest.TestCase):
    def test_team(self) -> None:
        """
        Test that a team is loaded correctly.
        """
        team_id = "9fbd42d9d995ada44c4188180975e57e990049b59917893b"
        team = btd6.Team(team_id)

        expected_results = [
            ("id", "9fbd42d9d995ada44c4188180975e57e990049b59917893b"),
            ("name", "PANDEMONIUM DEMONS"),
        ]
        for attr_name, attr_expected_value in expected_results:
            self.assertEqual(getattr(team, attr_name), attr_expected_value,
                             msg=f"Asserting Team.{attr_name}")

        self.assertGreater(team.member_count, 0,
                           msg=f"Check Team.member_count within lower bound")
        self.assertLessEqual(team.member_count, 15,
                             msg=f"Check Team.member_count within higher bound")

        check_instance = [
            ("status", btd6.TeamStatus), ("icon", btd6.Asset), ("banner", btd6.Asset),
            ("frame", btd6.Asset),
        ]
        for attr_name, attr_type in check_instance:
            self.assertIsInstance(getattr(team, attr_name), attr_type,
                                  msg=f"Assert if Team.{attr_name} is {attr_type}")

    def test_team_fail(self) -> None:
        """
        Test that the correct exception is raised when attempting to fetch a nonexistant team.
        """
        team_id = "blatantlywrongteamid"
        correct_exception = False
        try:
            btd6.Team(team_id, eager=True)
        except btd6.NotFound:
            correct_exception = True
        self.assertTrue(correct_exception, msg="Wrong team IDs should raise bloonspy.exceptions.NotFound")


if __name__ == '__main__':
    unittest.main()
