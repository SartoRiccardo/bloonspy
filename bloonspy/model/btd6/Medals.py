from dataclasses import dataclass


@dataclass(kw_only=True)
class Medals:
    first: int
    second: int
    third: int
    top_50: int
    top_1_percent: int
    top_10_percent: int
    top_25_percent: int
    top_50_percent: int
    top_75_percent: int


@dataclass(kw_only=True)
class CTLocalMedals:
    first: int
    second: int
    third: int
    top_10: int
    top_20: int
    top_40: int
    top_60: int


@dataclass(kw_only=True)
class CTGlobalMedals:
    top_25: int
    top_100: int
    top_1_percent: int
    top_10_percent: int
    top_25_percent: int
    top_50_percent: int
    top_75_percent: int


@dataclass(kw_only=True)
class MapMedals:
    easy: int
    primary_only: int
    deflation: int
    medium: int
    military_only: int
    apopalypse: int
    reverse: int
    hard: int
    magic_only: int
    double_hp_moabs: int
    half_cash: int
    alternate_bloon_rounds: int
    impoppable: int
    chimps_red: int
    chimps_black: int