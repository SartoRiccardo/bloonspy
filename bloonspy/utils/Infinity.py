

class Infinity:
    """Class to represent infinity."""
    def __str__(self):
        return "Inf"

    def __repr__(self):
        return "Inf"

    def __eq__(self, other):
        return isinstance(other, Infinity)
