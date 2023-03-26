

class Infinity:
    """Class to represent infinity.

    To check whether something is infinity, just see if they're equal. ::

       not_infinity = 3
       print(not_infinity == Infinity)  # False
       infinity = Infinity()
       print(infinity == Infinity)  # True

    """
    def __str__(self):
        return "Inf"

    def __repr__(self):
        return "Inf"

    def __eq__(self, other):
        return isinstance(other, Infinity) or other == Infinity
