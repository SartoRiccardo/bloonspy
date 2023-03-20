from dataclasses import dataclass, field
from enum import Enum
from ..Asset import Asset
from .User import User


class TeamStatus(Enum):
    PUBLIC = "OPEN"
    PRIVATE = "CLOSED"
    INVITE_ONLY = "FILTERED"
    DISBANDED = "DISBANDED"


@dataclass(kw_only=True)
class Team:
    id: str
    owner: User
    member_count: int
    status: TeamStatus
    banner: Asset
    icon: Asset
    frame: Asset
