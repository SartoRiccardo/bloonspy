import unittest
from bloonspy import btd6, Client
from bloonspy.model import Asset


class TestFetchUser(unittest.TestCase):
    def test_user(self) -> None:
        """
        Test getting an user.
        """
        user_id = "9cee138c8c94ffac1910864c0b73e577ca554ce8cb18db6c"
        user = Client.get_user(user_id)

        check_instance = [
            ("followers", int),
            ("name", str),
            ("banner", Asset),
            ("single_player_medals", btd6.MapMedals),
            ("boss_normal_medals", btd6.EventMedals),
            ("ct_local_medals", btd6.CtLocalMedals),
            ("stats", btd6.GameplayStats),
        ]
        for attr_name, attr_type in check_instance:
            self.assertIsInstance(getattr(user, attr_name), attr_type,
                                  msg=f"Assert if challenge.{attr_name} is {attr_type}")


if __name__ == '__main__':
    unittest.main()
