

class Infinity(int):
    """Class to represent infinity."""
    def __new__(cls, *args, **kwargs):
        return super(Infinity, cls).__new__(cls, -1)
