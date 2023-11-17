import unittest
from datetime import datetime
from bloonspy import btd6
from bloonspy.model import GameVersion
from bloonspy.exceptions import NotFound


class TestCustomMap(unittest.TestCase):
    def test_map(self) -> None:
        """
        Test that a custom map is loaded correctly.
        """
        map_code = "ZMYDRDM"
        map = btd6.CustomMap(map_code)

        expected_results = [
            ("id", map_code),
            ("name", "Mapa de PowerDino3423"),
            ("created_at", datetime.fromtimestamp(int(1697220116593/1000))),
            ("game_version", GameVersion(39, 0)),
        ]
        for attr_name, attr_expected_value in expected_results:
            self.assertEqual(
                getattr(map, attr_name), attr_expected_value,
                msg=f"Asserting CustomMap.{attr_name}"
            )

        check_instance = [
            ("wins", int), ("plays", int), ("losses", int), ("upvotes", int), ("plays_unique", int),
            ("wins_unique", int), ("losses_unique", int), ("thumbnail", str)
        ]
        for attr_name, attr_type in check_instance:
            self.assertIsInstance(
                getattr(map, attr_name), attr_type,
                msg=f"Assert if CustomMap.{attr_name} is {attr_type}"
            )

        creator = map.creator()
        self.assertIsInstance(creator, btd6.User,
                              msg="Assert that CustomMap.creator() returns User")

    def test_map_fail(self) -> None:
        """
        Test that the correct exception is raised when attempting to fetch a nonexistant map.
        """
        map_code = "blatantlywrongmapcode"
        correct_exception = False
        try:
            btd6.CustomMap(map_code, eager=True)
        except NotFound:
            correct_exception = True
        self.assertTrue(correct_exception, msg="Wrong map IDs should raise bloonspy.exceptions.NotFound")


if __name__ == '__main__':
    unittest.main()
