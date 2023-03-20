from dataclasses import dataclass


@dataclass(kw_only=True)
class Restriction:
    max_towers: int


@dataclass(kw_only=True)
class TowerRestriction(Restriction):
    top_path_blocked: int
    middle_path_blocked: int
    bottom_path_blocked: int
