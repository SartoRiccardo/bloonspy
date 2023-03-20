from dataclasses import dataclass


@dataclass(kw_only=True)
class Map:
    url: str
    name: str
