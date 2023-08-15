import unittest
from pprint import pp
from bloonspy import btd6


class TestUserSave(unittest.TestCase):
    def test_usersave(self) -> None:
        """
        Test that an user is loaded correctly.
        """
        oak = "oak_8461e54543d73c0b269539ee13b67daa"
        user_save: btd6.UserSave = btd6.UserSave.fetch(oak)

        expected_results = [
            ("xp", 180000000),
            ("unlocked_big_bloons", True),
            ("unlocked_small_bloons", True),
            ("unlocked_big_towers", True),
            ("unlocked_small_towers", True),
        ]
        for attr_name, attr_expected_value in expected_results:
            self.assertEqual(getattr(user_save, attr_name), attr_expected_value,
                             msg=f"Asserting UserSave.{attr_name}")

        # Greater or Equal cause these can increase in the future.
        expected_results_ge = [
            ("games_played", 2894),
            ("monkey_money", 28470),
            ("rank", 155),
            ("veteran_xp", 161489560),
            ("veteran_rank", 9),
            ("total_trophies_earned", 3000),
            ("highest_round", 275),
            ("daily_reward_count", 420),
            ("total_daily_challenges_completed", 198),
            ("total_races_entered", 1200),
            ("challenges_played", 300),
            ("challenges_shared", 6),
            ("total_completed_odysseys", 26),
            ("collection_event_crates_opened", 290),
            ("continues_used", 160),
        ]
        for attr_name, attr_expected_min in expected_results_ge:
            self.assertGreaterEqual(getattr(user_save, attr_name), attr_expected_min,
                                    msg=f"Asserting UserSave.{attr_name}")

        check_instance = [
            ("trophies", int),
            ("total_team_trophies_earned", int),
            ("knowledge_points", int),
            ("consecutive_daily_challenges_completed", int),
            ("big_bloons_active", bool),
            ("small_bloons_active", bool),
            ("big_towers_active", bool),
            ("small_towers_active", bool),
        ]
        for attr_name, attr_type in check_instance:
            self.assertIsInstance(getattr(user_save, attr_name), attr_type,
                                  msg=f"Assert if UserSave.{attr_name} is {attr_type}")

        # Tower XP & Unlock
        all_ge_than = 100_000
        for tower in btd6.Tower:
            if tower.is_hero():
                if tower not in user_save.unlocked_heros or not user_save.unlocked_heros[tower]:
                    self.fail(msg=f"Asserting UserSave.unlocked_heros[{tower}]")
            else:
                if tower not in user_save.unlocked_towers or not user_save.unlocked_towers[tower]:
                    self.fail(msg=f"Asserting UserSave.unlocked_towers[{tower}]")
                if tower not in user_save.tower_xp or user_save.tower_xp[tower] < all_ge_than:
                    self.fail(msg=f"Asserting UserSave.tower_xp[{tower}]")

        # Unlocked stuff
        unlocked_check = [
            (btd6.Upgrade, user_save.unlocked_upgrades, "unlocked_upgrades"),
            (btd6.MonkeyKnowledge, user_save.unlocked_knowledge, "unlocked_knowledge"),
            # (btd6.HeroSkin, user_save.unlocked_hero_skins, "unlocked_hero_skins"),
        ]
        for cls, attr, attr_name in unlocked_check:
            for item in cls:
                if item.value is None:
                    continue
                if item not in attr or not attr[item]:
                    self.fail(msg=f"Asserting UserSave.{attr_name}[{item}]")

        dict_typechecks = [
            (user_save.named_monkeys, btd6.Tower, str, "named_monkeys"),
            # (user_save.powers, btd6.Power, int, "powers"),
            (user_save.map_progress, btd6.Map, btd6.MapProgress, "map_progress"),
            *[
                (user_save.insta_monkeys[twr], btd6.InstaMonkey, int, f"map_progress[{twr.value}]")
                for twr in user_save.insta_monkeys
            ]
        ]
        for attr, key_cls, value_cls, attr_name in dict_typechecks:
            for key in attr:
                self.assertIsInstance(key, key_cls,
                                      msg=f"Asserting UserSave.{attr_name}.keys() is not {key_cls}: {key}")
                self.assertIsInstance(attr[key], value_cls,
                                      msg=f"Asserting UserSave.{attr_name}[{key}] is not {value_cls}: {attr[key]}")

        list_typechecks = [
            (user_save.achievements_claimed, btd6.Achievement, "achievements_claimed"),
        ]
        for attr, cls, attr_name in list_typechecks:
            for i in range(len(attr)):
                self.assertIsInstance(attr[i], cls, msg=f"Asserting UserSave.{attr_name}[{i}] is not {cls}: {attr[i]}")
        self.assertGreaterEqual(len(user_save.achievements_claimed), 0,
                                msg="Asserting UserSave.achievements_claimed > 0")

        mm_progress = user_save.map_progress[btd6.Map.MONKEY_MEADOW]
        self.assertEqual(mm_progress.single_player_border, btd6.MapBorder.BLACK,
                         msg="Asserting UserSave.map_progress[Monkey Meadow].single_player_border == BLACK")

        logs_progress = user_save.map_progress[btd6.Map.LOGS]
        self.assertEqual(logs_progress.coop_border, btd6.MapBorder.BLACK,
                         msg="Asserting UserSave.map_progress[Logs].coop_border == MapBorder.BLACK")

        ravine_progress = user_save.map_progress[btd6.Map.RAVINE]
        self.assertEqual(ravine_progress.coop_border, btd6.MapBorder.NONE,
                         msg="Asserting UserSave.map_progress[Ravine].coop_border == MapBorder.NONE")

        # TODO trophy_store_items

    def test_usersave_fail(self) -> None:
        """
        Test that the correct exception is raised when attempting to fetch a nonexistant user.
        """
        oak = "oak_blatantlywrongoak"
        correct_exception = False
        try:
            btd6.UserSave.fetch(oak)
        except btd6.NotFound:
            correct_exception = True
        self.assertTrue(correct_exception, msg="Wrong OAKs should raise bloonspy.exceptions.NotFound")


if __name__ == '__main__':
    unittest.main()
