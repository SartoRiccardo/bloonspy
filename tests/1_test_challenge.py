import unittest
from datetime import datetime
import bloonspy
from bloonspy import btd6


class TestChallenge(unittest.TestCase):
    def test_challenge(self) -> None:
        """
        Test that a challenge is loaded correctly.
        """
        challenge_code = "ZMDCDTB"
        challenge = btd6.Challenge(challenge_code)

        expected_results = [
            ("id", "ZMDCDTB"),
            ("name", "CT10 Tile CBA"),
            ("created_at", datetime.fromtimestamp(int(1671727285722/1000))),
            ("game_version", btd6.GameVersion(34, 3)),
            ("gamemode", btd6.Gamemode(btd6.Difficulty.MEDIUM, btd6.Mode.STANDARD)),
            ("disable_double_cash", True),
            ("disable_monkey_knowledge", False),
            ("disable_instas", False),
            ("disable_powers", True),
            ("disable_selling", False),
            ("disable_continues", True),
            ("starting_cash", 650),
            ("least_cash_used", bloonspy.Infinity()),
            ("least_tiers_used", 10),
            ("seed", 771803684),
            ("starting_lives", 150),
            ("max_lives", 9999),
            ("start_round", 1),
            ("end_round", 51),
            ("max_towers", 9999),
            ("max_paragons", 10),
            ("round_sets", ["default"]),
            # All values are defaults on this challenge anyway
            ("modifiers", btd6.ChallengeModifier()),
        ]
        for attr_name, attr_expected_value in expected_results:
            self.assertEqual(
                getattr(challenge, attr_name), attr_expected_value,
                msg=f"Asserting challenge.{attr_name}"
            )

        check_instance = [
            ("wins", int), ("plays", int), ("losses", int), ("upvotes", int), ("plays_unique", int),
            ("wins_unique", int), ("losses_unique", int)
        ]
        for attr_name, attr_type in check_instance:
            self.assertIsInstance(
                getattr(challenge, attr_name), attr_type,
                msg=f"Assert if challenge.{attr_name} is {attr_type}"
            )

        no_restrictions = btd6.TowerRestriction(
            max_towers=btd6.Infinity(),
            top_path_blocked=0,
            middle_path_blocked=0,
            bottom_path_blocked=0,
        )
        towers_allowed = {
            btd6.Tower.GWENDOLIN: btd6.Restriction(max_towers=1),
            btd6.Tower.DART_MONKEY: no_restrictions,
            btd6.Tower.GLUE_GUNNER: no_restrictions,
            btd6.Tower.SNIPER_MONKEY: no_restrictions,
            btd6.Tower.MONKEY_ACE: no_restrictions,
            btd6.Tower.HELI_PILOT: no_restrictions,
            btd6.Tower.MORTAR_MONKEY: no_restrictions,
            btd6.Tower.BANANA_FARM: no_restrictions,
        }
        for tower in challenge.towers.keys():
            self.assertIn(
                tower, towers_allowed.keys(),
                msg=f"Assert if {tower} is allowed"
            )
            self.assertEqual(
                towers_allowed[tower], challenge.towers[tower],
                msg=f"Assert if {towers_allowed[tower]} {tower} are available"
            )

        for power in btd6.Power:
            self.assertIn(
                power, challenge.powers.keys(),
                msg=f"Assert if {power.value} appears in the powers list"
            )
            self.assertEqual(
                challenge.powers[power], btd6.Infinity(),
                msg=f"Assert if {power.value} is allowed infinite times"
            )

    def test_challenge_fail(self) -> None:
        """
        Test that the correct exception is raised when attempting to fetch a nonexistant challenge.
        """
        challenge_code = "blatantlywrongchallengecode"
        correct_exception = False
        try:
            btd6.Challenge(challenge_code, eager=True)
        except btd6.NotFound:
            correct_exception = True
        self.assertTrue(correct_exception, msg="Wrong challenges IDs should raise bloonspy.exceptions.NotFound")


if __name__ == '__main__':
    unittest.main()
