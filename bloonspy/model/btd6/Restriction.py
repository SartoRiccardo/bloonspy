from dataclasses import dataclass
from typing import Union
from ...utils.Infinity import Infinity


@dataclass(kw_only=True)
class Restriction:
    max_towers: Union[int, Infinity]


@dataclass(kw_only=True)
class TowerRestriction(Restriction):
    top_path_blocked: int
    middle_path_blocked: int
    bottom_path_blocked: int
