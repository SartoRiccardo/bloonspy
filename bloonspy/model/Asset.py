from dataclasses import dataclass


@dataclass(kw_only=True)
class Asset:
    name: str
    url: str
