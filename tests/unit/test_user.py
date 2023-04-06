import unittest
from bloonspy import btd6


class TestUser(unittest.TestCase):
    def test_user(self) -> None:
        """
        Test that an user is loaded correctly.
        """
        user_id = "9cee138c8c94ffac1910864c0b73e577ca554ce8cb18db6c"
        user = btd6.User(user_id)

        expected_results = [
            ("id", "9cee138c8c94ffac1910864c0b73e577ca554ce8cb18db6c"),
            ("name", "Sarto"),
            ("rank", 155),
        ]
        for attr_name, attr_expected_value in expected_results:
            self.assertEqual(getattr(user, attr_name), attr_expected_value,
                             msg=f"Asserting User.{attr_name}")

        # Greater or Equal cause these can increase in the future.
        expected_results_ge = [
            ("achievements", 124),
            ("veteran_rank", 8),
        ]
        for attr_name, attr_expected_min in expected_results_ge:
            self.assertGreaterEqual(getattr(user, attr_name), attr_expected_min,
                                    msg=f"Asserting User.{attr_name}")

        check_instance = [
            ("followers", int),
            ("avatar", btd6.Asset),
            ("banner", btd6.Asset),
            ("single_player_medals", btd6.MapMedals),
            ("coop_medals", btd6.MapMedals),
            ("boss_normal_medals", btd6.EventMedals),
            ("boss_elite_medals", btd6.EventMedals),
            ("race_medals", btd6.EventMedals),
            ("ct_local_medals", btd6.CTLocalMedals),
            ("ct_global_medals", btd6.CTGlobalMedals),
            ("stats", btd6.GameplayStats),
        ]
        for attr_name, attr_type in check_instance:
            self.assertIsInstance(getattr(user, attr_name), attr_type,
                                  msg=f"Assert if challenge.{attr_name} is {attr_type}")

        # Check medals

        expected_results_ge = [
            ("chimps_black", 1), ("easy", 1), ("medium", 1), ("hard", 1),
            ("primary_only", 1), ("deflation", 1), ("military_only", 1),
            ("apopalypse", 1), ("reverse", 1), ("magic_only", 1), ("half_cash", 1),
            ("double_hp_moabs", 1), ("alternate_bloons_rounds", 1), ("impoppable", 1),
            ("chimps_red", 1),
        ]
        for attr_name, attr_expected_min in expected_results_ge:
            self.assertGreaterEqual(getattr(user.single_player_medals, attr_name), attr_expected_min,
                                    msg=f"Asserting User.single_player_medals.{attr_name}")
            self.assertGreaterEqual(getattr(user.coop_medals, attr_name), attr_expected_min,
                                    msg=f"Asserting User.coop_medals.{attr_name}")

        check_instance = [
            ("first", int), ("second", int), ("third", int), ("top_50", int), ("top_1_percent", int),
            ("top_10_percent", int), ("top_25_percent", int), ("top_50_percent", int), ("top_75_percent", int)
        ]
        for attr_name, attr_type in check_instance:
            self.assertIsInstance(getattr(user.boss_normal_medals, attr_name), attr_type,
                                  msg=f"Asserting User.boss_normal_medals.{attr_name}")
            self.assertIsInstance(getattr(user.boss_elite_medals, attr_name), attr_type,
                                  msg=f"Asserting User.boss_elite_medals.{attr_name}")
            self.assertIsInstance(getattr(user.race_medals, attr_name), attr_type,
                                  msg=f"Asserting User.race_medals.{attr_name}")
        self.assertGreaterEqual(user.race_medals.top_50, 1,
                                msg=f"Asserting User has at least 1 Top 50 race finish.")

        check_instance = [
            ("first", int), ("second", int), ("third", int), ("top_10", int), ("top_20", int),
            ("top_40", int), ("top_60", int)
        ]
        for attr_name, attr_type in check_instance:
            self.assertIsInstance(getattr(user.ct_local_medals, attr_name), attr_type,
                                  msg=f"Asserting User.ct_local_medals.{attr_name}")

        check_instance = [
            ("top_25", int), ("top_100", int), ("top_1_percent", int), ("top_10_percent", int), ("top_25_percent", int),
            ("top_50_percent", int), ("top_75_percent", int)
        ]
        for attr_name, attr_type in check_instance:
            self.assertIsInstance(getattr(user.ct_global_medals, attr_name), attr_type,
                                  msg=f"Asserting User.ct_global_medals.{attr_name}")

        # Gameplay stats

        expected_results_ge = [
            (btd6.Tower.BRICKELL, 93), (btd6.Tower.ADORA, 68), (btd6.Tower.BENJAMIN, 1189),
            (btd6.Tower.ETIENNE, 108), (btd6.Tower.GERALDO, 151), (btd6.Tower.GWENDOLIN, 411),
            (btd6.Tower.OBYN, 499), (btd6.Tower.PAT_FUSTY, 143), (btd6.Tower.PSI, 204),
            (btd6.Tower.QUINCY, 125), (btd6.Tower.SAUDA, 534), (btd6.Tower.STRIKER_JONES, 59),
            (btd6.Tower.EZILI, 257), (btd6.Tower.CHURCHILL, 63),
        ]
        for hero, times_placed in expected_results_ge:
            self.assertIn(hero, user.heroes_placed.keys(),
                          msg=f"Assert {hero.value} appears in User.heroes_placed")
            self.assertGreaterEqual(user.heroes_placed[hero], times_placed,
                                    msg=f"Assert correctness of User.heroes_placed[{hero.value}]")

        self.assertIsInstance(user.stats.most_experienced_monkey, btd6.Tower,
                              msg=f"Asserting User.stats.most_experienced_monkey")
        expected_results_ge = [
            ("cash_earned", 711700673), ("challenges_completed", 198), ("collection_chests_opened", 293),
            ("coop_cash_given", 78006898), ("daily_rewards", 339), ("game_count", 9252), ("games_won", 2618),
            ("highest_round", 276), ("highest_round_chimps", 127), ("highest_round_deflation", 100),
            ("insta_monkey_collection", 796), ("monkey_teams_wins", 11), ("powers_used", 3811),
            ("total_odysseys_completed", 26), ("total_odyssey_stars", 100), ("total_trophies_earned", 3288),
            ("necro_bloons_reanimated", 476791), ("bloons_leaked", 557788), ("transforming_tonics_used", 196),
            ("damage_done_to_bosses", 713924)
        ]
        for attr_name, attr_expected_min in expected_results_ge:
            self.assertGreaterEqual(getattr(user.stats, attr_name), attr_expected_min,
                                    msg=f"Asserting User.stats.{attr_name}")

        expected_results_ge = [
            ("total", 455698668), ("total_coop", 26290553), ("camos", 31764834), ("regrows", 293382673),
            ("purples", 1133115), ("leads", 13291249), ("ceramics", 210121378), ("moabs", 1324838), ("bfbs", 252424),
            ("zomgs", 34974), ("bads", 3824), ("golden", 69),
        ]
        for attr_name, attr_expected_min in expected_results_ge:
            self.assertGreaterEqual(getattr(user.stats.bloons_popped, attr_name), attr_expected_min,
                                    msg=f"Asserting User.stats.bloons_popped.{attr_name}")

    def test_user_fail(self) -> None:
        """
        Test that the correct exception is raised when attempting to fetch a nonexistant user.
        """
        user_id = "blatantlywronguserid"
        correct_exception = False
        try:
            btd6.User(user_id, eager=True)
        except btd6.NotFound:
            correct_exception = True
        self.assertTrue(correct_exception, msg="Wrong user IDs should raise bloonspy.exceptions.NotFound")


if __name__ == '__main__':
    unittest.main()
