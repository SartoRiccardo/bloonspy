from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Dict
from .Challenge import Challenge
from .User import User


@dataclass(kw_only=True)
class Race(Challenge):
    start: datetime
    end: datetime
    total_scores: int

    # def leaderboard(self):
    #     pass


@dataclass(kw_only=True)
class RacePlayer(User):
    score: timedelta
    submission_time: datetime
