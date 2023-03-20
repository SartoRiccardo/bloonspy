from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Dict
from .Challenge import Challenge
from .User import User


@dataclass(kw_only=True)
class BossType:
    name: str
    icon_url: str


@dataclass(kw_only=True)
class Boss(Challenge):
    _is_elite: bool
    total_scores: int

    # def leaderboard(self):
    #     pass


@dataclass(kw_only=True)
class BossEvent:
    id: str
    name: str
    type: BossType
    start: datetime
    end: datetime
    total_scores: int
    normal: Boss
    elite: Boss


@dataclass(kw_only=True)
class BossPlayer(User):
    score: timedelta
    submission_time: datetime
