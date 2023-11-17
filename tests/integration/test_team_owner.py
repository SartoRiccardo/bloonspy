import unittest
from bloonspy import Client


class TestTeamOwner(unittest.TestCase):
    def test_team(self) -> None:
        """
        Test getting a team's owner.
        """
        team_id = "9fba1683de92f9f01c4b861d5c70e326ce571db4ca448b30"#"9fbd42d98ac2faa41d40884a5b21b577cb064ebacf168e3f"
        team = Client.get_team(team_id)
        owner = team.owner()
        self.assertIsNotNone(owner)
        self.assertIn(owner.name.lower(), ["zoroark", "thargos", "vaneckpm"])


if __name__ == '__main__':
    unittest.main()
