from dataclasses import dataclass
from ..GameVersion import GameVersion
from .Tower import Tower, HeroSkin
from .Power import Power
from .Gamemode import Gamemode
from ...utils.dictionaries import enum_any_dict
from .Rewards import InstaMonkey
from .Progress import MonkeyKnowledge, Upgrade, Achievement
from .Map import MapProgress, Map, GamemodeCompletionData
from .Cosmetics import TrophyStoreItemStatus
from typing import Any


@dataclass
class UserSave:
    """A dataclass detailing an user's save state."""
    latest_game_version: GameVersion  #: The latest version of the game that this player has played.
    tower_xp: dict[Tower, int]  #: XP accumulated for each tower.
    unlocked_upgrades: dict[Upgrade, bool]  #: Upgrades unlocked.
    unlocked_knowledge: dict[MonkeyKnowledge, bool]  #: Monkey Knowledge unlocked.
    unlocked_towers: dict[Tower, bool]  #: Towers unlocked.
    unlocked_heros: dict[Tower, bool]  #: Heroes unlocked.
    unlocked_hero_skins: dict[HeroSkin, bool]  #: Hero skins unlocked.
    games_played: int  #: Total games played.
    # powers: dict[Power, int]  #: Amount of powers obtained.
    insta_monkeys: dict[Tower, dict[InstaMonkey, int]]  #: Insta monkeys collected.
    monkey_money: int  #: Current Monkey Money.
    xp: int  #: Current XP.
    rank: int  #: Current Rank.
    veteran_xp: int  #: Current Veteran XP.
    veteran_rank: int  #: Current Veteran Rank.
    trophies: int  #: Current trophies.
    total_trophies_earned: int  #: Lifetime trophies earned through events.
    total_team_trophies_earned: int  #: Lifetime team trophies earned through events.
    knowledge_points: int  #: Current Monkey Knowledge points.
    primary_hero: Tower  #: Current Selected Hero.
    achievements_claimed: list[Achievement]  #: Achievements claimed.
    highest_round: int  #: Highest seen round.
    daily_reward_count: int  #: Daily rewards claimed.
    total_daily_challenges_completed: int  #: Total Daily Challenges completed.
    consecutive_daily_challenges_completed: int  #: Current number of consecutive days a Daily Challenge has been completed.
    total_races_entered: int  #: Total eaces entered.
    challenges_played: int  #: Total challenges played.
    challenges_shared: int  #: Total challenges shared.
    total_completed_odysseys: int  #: Total Odysseys completed.
    unlocked_big_bloons: bool  #: Whether Big Bloons has been unlocked.
    big_bloons_active: bool  #: Whether Big Bloons is active.
    unlocked_small_bloons: bool  #: Whether Small Bloons has been unlocked.
    small_bloons_active: bool  #: Whether Small Bloons is active.
    unlocked_big_towers: bool  #: Whether Big Towers has been unlocked.
    big_towers_active: bool  #: Whether Big Towers is active.
    unlocked_small_towers: bool  #: Whether Small Towers has been unlocked.
    small_towers_active: bool  #: Whether Small Towers is active.
    named_monkeys: dict[Tower, str]  #: Named monkey names.
    collection_event_crates_opened: int  #: Number of ollect event crates opened.
    continues_used: int  #: Continues used.
    trophy_store_items: dict[TrophyStoreItemStatus, bool]  #: Trophy Store items purchased.
    map_progress: dict[Map, MapProgress]  #: The player's map completions.

    @staticmethod
    def from_json(data: dict[str, Any]) -> "UserSave":
        insta_monkeys = {}
        for twr_name in data["instaTowers"]:
            tower = Tower.from_string(twr_name)
            insta_monkeys[tower] = {}
            collection = data["instaTowers"][twr_name]
            for path_key in collection:
                path = path_key.replace("NaN", "0")
                tp, mp, bp = int(path[0]), int(path[1]), int(path[2])
                insta_monkey = InstaMonkey(tower, tp, mp, bp)
                insta_monkeys[tower][insta_monkey] = data["instaTowers"][path_key]

        def parse_map_completion(map_completion) -> MapProgress:
            single_player = {}
            coop = {}
            for diff in map_completion["difficulty"]:
                for mode in map_completion["difficulty"][diff]["single"]:
                    single_player[Gamemode.from_strings(diff, mode)] = GamemodeCompletionData(
                        map_completion["difficulty"][diff]["single"][mode]["completed"],
                        map_completion["difficulty"][diff]["single"][mode]["completedWithoutLoadingSave"],
                        map_completion["difficulty"][diff]["single"][mode]["bestRound"],
                        map_completion["difficulty"][diff]["single"][mode]["timesCompleted"],
                    )
                for mode in map_completion["difficulty"][diff]["coop"]:
                    coop[Gamemode.from_strings(diff, mode)] = GamemodeCompletionData(
                        map_completion["difficulty"][diff]["coop"][mode]["completed"],
                        map_completion["difficulty"][diff]["coop"][mode]["completedWithoutLoadingSave"],
                        map_completion["difficulty"][diff]["coop"][mode]["bestRound"],
                        map_completion["difficulty"][diff]["coop"][mode]["timesCompleted"],
                    )
            return MapProgress(map_completion["complete"], single_player, coop)

        return UserSave(
            GameVersion(*[int(ver) for ver in data["latestGameVersion"].split(".")]),
            enum_any_dict(Tower, data["towerXP"]),
            enum_any_dict(Upgrade, data["acquiredUpgrades"]),
            enum_any_dict(MonkeyKnowledge, data["acquiredKnowledge"]),
            enum_any_dict(Tower, data["unlockedTowers"]),
            enum_any_dict(Tower, data["unlockedHeros"]),
            enum_any_dict(HeroSkin, data["unlockedSkins"]),
            data["gamesPlayed"],
            # enum_any_dict(Power, data["powers"]),
            insta_monkeys,
            data["monkeyMoney"],
            data["xp"],
            data["rank"],
            data["veteranXp"],
            data["veteranRank"],
            data["trophies"],
            data["totalTrophiesEarned"],
            data["totalTeamTrophiesEarned"],
            data["knowledgePoints"],
            Tower.from_string(data["primaryHero"]),
            [Achievement.from_string(a) for a in data["achievementsClaimed"]],
            data["highestRound"],
            data["dailyRewardCount"],
            data["totalDailyChallengesCompleted"],
            data["consecutiveDailyChallengesCompleted"],
            data["totalRacesEntered"],
            data["challengesPlayed"],
            data["challengesShared"],
            data["totalCompletedOdysseys"],
            data["unlockedBigBloons"],
            data["bigBloonsActive"],
            data["unlockedSmallBloons"],
            data["smallBloonsActive"],
            data["seenBigTowers"],
            data["bigTowersActive"],
            data["unlockedSmallTowers"],
            data["smallTowersActive"],
            enum_any_dict(Tower, data["namedMonkeys"]),
            data["collectionEventCratesOpened"],
            data["continuesUsed"],
            None,  # trophy_store_items: TrophyStoreItemStatus  #: Trophy Store items purchased.
            enum_any_dict(Map, data["mapProgress"], parse_raw=parse_map_completion),
        )
