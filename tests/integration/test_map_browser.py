import unittest
import random
from datetime import datetime
from bloonspy import Client, CustomMapFilter


class TestChallengeBrowser(unittest.TestCase):
    def test_challenge_browser(self) -> None:
        """
        Test getting the newest maps.
        """
        maps = Client.custom_maps(CustomMapFilter.NEWEST, start_from_page=2, pages=2)
        self.assertGreater(len(maps), 0)
        some_map = random.choice(maps)

        check_instance = [
            ("name", str), ("created_at", datetime), ("wins", int), ("upvotes", int)
        ]
        for attr_name, attr_type in check_instance:
            self.assertIsInstance(
                getattr(some_map, attr_name), attr_type,
                msg=f"Assert if CustomMap.{attr_name} is {attr_type}"
            )


if __name__ == '__main__':
    unittest.main()
