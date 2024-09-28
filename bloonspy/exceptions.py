

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
    """
    *New in 0.5.0*

    You specified a bad path (for example: 522).
    """
    def __init__(self, tp: int, mp: int, bp: int):
        super().__init__(f"Invalid Tower Path: {tp}{mp}{bp}")


class Forbidden(BloonsException):
    """
    *New in 0.5.0*

    You are not allowed to use this method.
    """
    pass


class NotLoaded(BloonsException):
    """
    *New in 0.9.0*

    You attempted to access an unloaded property in a lazy-loaded resource in an
    asynchronous environment.
    """
