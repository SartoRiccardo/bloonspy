import unittest
from bloonspy import Client
from bloonspy.exceptions import Forbidden
from bloonspy import btd6


class TestUserSave(unittest.TestCase):
    def test_usersave(self) -> None:
        """
        Test that an user is loaded correctly.
        """
        oak = "oak_8461e54543d73c0b269539ee13b67daa"
        user_save = Client.get_user(oak).get_progress()
        self.assertIsInstance(user_save, btd6.UserSave,
                              msg="Client.get_user().get_progress() should return UserSave")

    def test_usersave_not_id(self) -> None:
        """
        Test that a Forbidden error will be thrown upon trying to get the save of an User identified by ID, not OAK.
        """
        uid = "9fbf41dedac0aba64a408f4a5877e577c55618bb9616dc39"
        thrown = False
        try:
            Client.get_user(uid).get_progress()
        except Forbidden:
            thrown = True
        self.assertTrue(thrown, msg="Assert that Forbidden is thrown when getting "
                                    "the save data of an User identified by ID")


if __name__ == '__main__':
    unittest.main()
