from dataclasses import dataclass


@dataclass
class Asset:
    """A game asset."""
    name: str  #: The name of the asset.
    url: str  #: The URL of the asset.
