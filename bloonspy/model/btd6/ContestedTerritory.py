from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict
from .User import User
from .Team import Team


@dataclass(kw_only=True)
class CtPlayer(User):
    score: int


@dataclass(kw_only=True)
class CtTeam(Team):
    score: int


@dataclass(kw_only=True)
class ContestedTerritory:
    id: str
    start: datetime
    end: datetime
    total_scores_player: int
    total_scores_team: int

    # def leaderboard_player(self):
    #     pass

    # def leaderboard_team(self):
    #     pass
