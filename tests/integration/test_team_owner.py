import unittest
from bloonspy import btd6, Client


class TestTeamOwner(unittest.TestCase):
    def test_team(self) -> None:
        """
        Test getting a team's owner.
        """
        team_id = "9fbd42d98ac2faa41d40884a5b21b577cb064ebacf168e3f"
        team = Client.get_team(team_id)
        owner = team.owner()
        self.assertIsNotNone(owner)
        self.assertIn(owner.name.lower(), ["thargos", "vaneckpm"])

    # Unlucky for me I know none of these.
    # def test_team_disbanded(self) -> None:
    #     """
    #     Test a challenge with a missing creator.
    #     """


if __name__ == '__main__':
    unittest.main()
