from dataclasses import dataclass, field


@dataclass(kw_only=True)
class EventMedals:
    """Medal set for events."""
    first: int = field(default=0)  #: Number of first place finishes.
    second: int = field(default=0)  #: Number of second place finishes.
    third: int = field(default=0)  #: Number of third place finishes.
    top_50: int = field(default=0)  #: Number of Top 50 finishes.
    top_1_percent: int = field(default=0)  #: Number of Top 1% finishes.
    top_10_percent: int = field(default=0)  #: Number of Top 10% finishes.
    top_25_percent: int = field(default=0)  #: Number of Top 25% finishes.
    top_50_percent: int = field(default=0)  #: Number of Top 50% finishes.
    top_75_percent: int = field(default=0)  #: Number of Top 75% finishes.


@dataclass(kw_only=True)
class CTLocalMedals:
    """Medal set for Contested Territory (local leaderboard)."""
    first: int = field(default=0)  #: Number of first place finishes.
    second: int = field(default=0)  #: Number of second place finishes.
    third: int = field(default=0)  #: Number of third place finishes.
    top_10: int = field(default=0)  #: Number of Top 10 finishes.
    top_20: int = field(default=0)  #: Number of Top 20 finishes.
    top_40: int = field(default=0)  #: Number of Top 40 finishes.
    top_60: int = field(default=0)  #: Number of Top 60 finishes.


@dataclass(kw_only=True)
class CTGlobalMedals:
    """Medal set for Contested Territory (global leaderboard)."""
    top_25: int = field(default=0)  #: Number of Top 25 finishes.
    top_100: int = field(default=0)  #: Number of Top 100 finishes.
    top_1_percent: int = field(default=0)  #: Number of Top 1% finishes.
    top_10_percent: int = field(default=0)  #: Number of Top 10% finishes.
    top_25_percent: int = field(default=0)  #: Number of Top 25% finishes.
    top_50_percent: int = field(default=0)  #: Number of Top 50% finishes.
    top_75_percent: int = field(default=0)  #: Number of Top 75% finishes.


@dataclass(kw_only=True)
class MapMedals:
    """Medal set for maps."""
    easy: int = field(default=0)  #: Number of medals for Easy - Standard.
    primary_only: int = field(default=0)  #: Number of medals for Easy - Primary only.
    deflation: int = field(default=0)  #: Number of medals for Easy - Deflation.
    medium: int = field(default=0)  #: Number of medals for Medium - Standard.
    military_only: int = field(default=0)  #: Number of medals for Medium - Military only.
    apopalypse: int = field(default=0)  #: Number of medals for Medium - Apopalypse.
    reverse: int = field(default=0)  #: Number of medals for Medium - Reverse.
    hard: int = field(default=0)  #: Number of medals for Hard - Standard.
    magic_only: int = field(default=0)  #: Number of medals for Hard - Magic only.
    double_hp_moabs: int = field(default=0)  #: Number of medals for Hard - Double HP MOABs.
    half_cash: int = field(default=0)  #: Number of medals for Hard - Half Cash.
    alternate_bloons_rounds: int = field(default=0)  #: Number of medals for Hard - Alternate Bloons Rounds.
    impoppable: int = field(default=0)  #: Number of medals for Hard - Impoppable.
    chimps_red: int = field(default=0)  #: Number of medals for Hard - CHIMPS (red).
    chimps_black: int = field(default=0)  #: Number of medals for Hard - CHIMPS (black).
