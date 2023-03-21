from dataclasses import dataclass, field


@dataclass(kw_only=True)
class Medals:
    first: int = field(default=0)
    second: int = field(default=0)
    third: int = field(default=0)
    top_50: int = field(default=0)
    top_1_percent: int = field(default=0)
    top_10_percent: int = field(default=0)
    top_25_percent: int = field(default=0)
    top_50_percent: int = field(default=0)
    top_75_percent: int = field(default=0)


@dataclass(kw_only=True)
class CTLocalMedals:
    first: int = field(default=0)
    second: int = field(default=0)
    third: int = field(default=0)
    top_10: int = field(default=0)
    top_20: int = field(default=0)
    top_40: int = field(default=0)
    top_60: int = field(default=0)


@dataclass(kw_only=True)
class CTGlobalMedals:
    top_25: int = field(default=0)
    top_100: int = field(default=0)
    top_1_percent: int = field(default=0)
    top_10_percent: int = field(default=0)
    top_25_percent: int = field(default=0)
    top_50_percent: int = field(default=0)
    top_75_percent: int = field(default=0)


@dataclass(kw_only=True)
class MapMedals:
    easy: int = field(default=0)
    primary_only: int = field(default=0)
    deflation: int = field(default=0)
    medium: int = field(default=0)
    military_only: int = field(default=0)
    apopalypse: int = field(default=0)
    reverse: int = field(default=0)
    hard: int = field(default=0)
    magic_only: int = field(default=0)
    double_hp_moabs: int = field(default=0)
    half_cash: int = field(default=0)
    alternate_bloons_rounds: int = field(default=0)
    impoppable: int = field(default=0)
    chimps_red: int = field(default=0)
    chimps_black: int = field(default=0)
