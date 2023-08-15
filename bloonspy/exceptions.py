

class BloonsException(Exception):
    """Superclass for all Bloons exceptions. Can be used as a catch-all."""
    pass


class NotFound(BloonsException):
    """The requested resource or event doesn't exist or has expired."""
    pass


class UnderMaintenance(BloonsException):
    """The Ninja Kiwi server is under maintenance."""
    pass


class BadTeamSize(BloonsException):
    """You specified a bad team size."""
    pass


class InvalidTowerPath(BloonsException):
    """You specified a bad path (for example: 522)."""
    def __init__(self, tp: int, mp: int, bp: int):
        super().__init__(f"Invalid Tower Path: {tp}{mp}{bp}")

