import unittest
from bloonspy import btd6


class TestChallengeCreator(unittest.TestCase):
    def test_challenge(self) -> None:
        """
        Test a challenge with a creator.
        """
        challenge_id = "ZMDCDTB"
        challenge = btd6.Challenge(challenge_id)
        creator = challenge.creator()
        self.assertEqual(creator.name, "Sarto")
        self.assertEqual(creator.id, "9cee138c8c94ffac1910864c0b73e577ca554ce8cb18db6c")

    def test_challenge_no_creator(self) -> None:
        """
        Test a challenge with a missing creator.
        """
        challenge_id = "rot168220230320"
        challenge = btd6.Challenge(challenge_id)
        creator = challenge.creator()
        self.assertIsNone(creator)


if __name__ == '__main__':
    unittest.main()
