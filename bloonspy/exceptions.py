

class BloonsException(Exception):
    """Superclass for all Bloons exceptions"""
    pass


class NotFound(BloonsException):
    """The requested resource or event doesn't exist or has expired."""
    pass

