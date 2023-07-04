

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

