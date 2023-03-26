import unittest
from bloonspy import btd6, Client


class TestFetchOdyssey(unittest.TestCase):
    def test_odyssey(self) -> None:
        """
        Test getting a random odyssey.
        """
        odysseys = Client.odysseys()
        some_odyssey = odysseys[0]
        self.assertIsInstance(some_odyssey, btd6.OdysseyEvent,
                              msg=f"Assert if Client.odysseys returns List[OdysseyEvent]")

        some_other_odyssey = Client.get_odyssey(odysseys[1].id)
        self.assertIsInstance(some_other_odyssey, btd6.OdysseyEvent,
                              msg=f"Assert if Client.get_odyssey returns OdysseyEvent")


if __name__ == '__main__':
    unittest.main()
