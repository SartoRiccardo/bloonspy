from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict
from .Restriction import Restriction
from .Challenge import Challenge
from .Power import Power
from .Tower import Tower


@dataclass(kw_only=True)
class Odyssey:
    is_extreme: bool
    max_monkey_seats: int
    max_monkeys_on_boat: int
    max_power_slots: int
    starting_lives: int
    rewards: List[str]  # TODO make a proper object for the rewards, Insta Monkeys, etc
    available_powers: Dict[Power, int]
    default_powers: Dict[Power, int]
    available_towers: Dict[Tower, Restriction]
    default_towers: Dict[Tower, int]
    maps: List[Challenge]


@dataclass(kw_only=True)
class OdysseyEvent:
    id: str
    name: str
    start: datetime
    end: datetime
    easy: Odyssey
    medium: Odyssey
    hard: Odyssey
