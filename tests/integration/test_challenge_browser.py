import unittest
import random
from datetime import datetime
from bloonspy import Client, ChallengeFilter


class TestChallengeBrowser(unittest.TestCase):
    def test_challenge_browser(self) -> None:
        """
        Test getting the newest challenges.
        """
        challenges = Client.challenges(ChallengeFilter.NEWEST, start_from_page=2, pages=2)
        self.assertGreater(len(challenges), 0)
        some_challenge = challenges[random.randint(0, len(challenges)-1)]

        check_instance = [
            ("name", str), ("created_at", datetime), ("wins", int), ("upvotes", int)
        ]
        for attr_name, attr_type in check_instance:
            self.assertIsInstance(
                getattr(some_challenge, attr_name), attr_type,
                msg=f"Assert if Challenge.{attr_name} is {attr_type}"
            )


if __name__ == '__main__':
    unittest.main()
