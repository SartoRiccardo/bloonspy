from dataclasses import dataclass, field
from typing import Dict, List
from ..Asset import Asset
from .Tower import Tower
from .Medals import Medals, MapMedals, CTGlobalMedals, CTLocalMedals


@dataclass(kw_only=True)
class BloonsPoppedStats:
    total: int
    total_coop: int
    camos: int
    regrows: int
    purples: int
    leads: int
    ceramics: int
    moabs: int
    bfbs: int
    zomgs: int
    bads: int
    golden: int


@dataclass(kw_only=True)
class GameplayStats:
    most_experienced_monkey: Tower
    cash_earned: int
    challenges_completed: int
    collection_chests_opened: int
    coop_cash_given: int
    daily_rewards: int
    game_count: int
    games_won: int
    highest_round: int
    highest_round_chimps: int
    highest_round_deflation: int
    insta_monkey_collection: int
    monkey_teams_wins: int
    powers_used: int
    total_odysseys_completed: int
    total_odyssey_stars: int
    total_trophies_earned: int
    necro_bloons_reanimated: int
    bloons_leaked: int
    bloons_popped: BloonsPoppedStats


@dataclass(kw_only=True)
class User:
    id: str
    name: str
    rank: int
    veteran_rank: int
    achivements: int
    followers: int
    avatar: Asset
    banner: Asset
    single_player_medals: MapMedals
    coop_medals: MapMedals
    boss_normal_medals: Medals
    boss_elite_medals: Medals
    race_medals: Medals
    ct_local_medals: CTLocalMedals
    ct_global_medals: CTGlobalMedals
    stats: GameplayStats
    heroes_placed: Dict[Tower, int]
