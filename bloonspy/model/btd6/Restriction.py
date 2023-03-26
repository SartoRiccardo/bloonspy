from dataclasses import dataclass
from typing import Union
from ...utils.Infinity import Infinity


@dataclass(kw_only=True)
class Restriction:
    """Generic tower restriction."""
    max_towers: Union[int, Infinity]  #: Max amount of towers you can place of a kind.


@dataclass(kw_only=True)
class TowerRestriction(Restriction):
    """Non-hero restriction. Inherits from :class:`~bloonspy.model.btd6.Restriction`."""
    top_path_blocked: int  #: Number of restricted top path upgrades.
    middle_path_blocked: int  #: Number of restricted middle path upgrades.
    bottom_path_blocked: int  #: Number of restricted bottom path upgrades.
