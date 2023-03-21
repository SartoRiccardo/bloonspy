from dataclasses import dataclass, field
import requests
from typing import Dict, List, Any
from ...exceptions import NotFound
from ...utils.decorators import fetch_property
from ...utils.dictionaries import rename_keys
from ..Asset import Asset
from .Tower import Tower
from .Medals import Medals, MapMedals, CTGlobalMedals, CTLocalMedals


@dataclass(kw_only=True)
class BloonsPoppedStats:
    total: int = field(default=0)
    total_coop: int = field(default=0)
    camos: int = field(default=0)
    regrows: int = field(default=0)
    purples: int = field(default=0)
    leads: int = field(default=0)
    ceramics: int = field(default=0)
    moabs: int = field(default=0)
    bfbs: int = field(default=0)
    zomgs: int = field(default=0)
    bads: int = field(default=0)
    golden: int = field(default=0)


@dataclass(kw_only=True)
class GameplayStats:
    most_experienced_monkey: Tower = field(default=Tower.DART_MONKEY)
    cash_earned: int = field(default=0)
    challenges_completed: int = field(default=0)
    collection_chests_opened: int = field(default=0)
    coop_cash_given: int = field(default=0)
    daily_rewards: int = field(default=0)
    game_count: int = field(default=0)
    games_won: int = field(default=0)
    highest_round: int = field(default=0)
    highest_round_chimps: int = field(default=0)
    highest_round_deflation: int = field(default=0)
    insta_monkey_collection: int = field(default=0)
    monkey_teams_wins: int = field(default=0)
    powers_used: int = field(default=0)
    total_odysseys_completed: int = field(default=0)
    total_odyssey_stars: int = field(default=0)
    total_trophies_earned: int = field(default=0)
    necro_bloons_reanimated: int = field(default=0)
    bloons_leaked: int = field(default=0)
    bloons_popped: BloonsPoppedStats = field(default_factory=BloonsPoppedStats)


class User:
    endpoint = "https://data.ninjakiwi.com/btd6/users/{}"

    def __init__(self, user_id: str, eager: bool = False):
        self._id = user_id
        self._data = {}
        self._loaded = False
        if eager:
            self._load_user()

    def _load_user(self, only_if_unloaded: bool = True) -> None:
        if self._loaded and only_if_unloaded:
            return

        resp = requests.get(self.endpoint.format(self._id))
        if resp.status_code != 200:
            return

        data = resp.json()
        if not data["success"]:
            self._handle_exceptions(data["error"])

        self._parse_json(data["body"])

    @staticmethod
    def _handle_exceptions(error_msg: str) -> None:
        if error_msg == "Invalid user ID / Player Does not play this game":
            raise NotFound(error_msg)
        raise Exception(error_msg)

    def _parse_json(self, raw_user: Dict[str, Any]) -> None:
        self._loaded = False

        self._data = {}
        copy_keys = ["displayName", "rank", "veteranRank", "achievements", "followers"]
        for key in copy_keys:
            self._data[key] = raw_user[key]

        self._data["avatar"] = Asset(raw_user["avatar"], raw_user["avatarURL"])
        self._data["banner"] = Asset(raw_user["banner"], raw_user["bannerURL"])

        map_medal_keys = [
            ("CHIMPS-BLACK", "chimps_black"), ("Clicks", "chimps_red"), ("Easy", "easy"), ("Medium", "medium"),
            ("Hard", "hard"), ("PrimaryOnly", "primary_only"), ("Deflation", "deflation"),
            ("MilitaryOnly", "military_only"), ("Apopalypse", "apopalypse"), ("Reverse", "reverse"),
            ("MagicOnly", "magic_only"), ("HalfCash", "half_cash"), ("DoubleMoabHealth", "double_hp_moabs"),
            ("AlternateBloonsRounds", "alternate_bloons_rounds"), ("Impoppable", "impoppable")
        ]
        self._data["single_player_medals"] = MapMedals(
            **rename_keys(raw_user["_medalsSinglePlayer"], map_medal_keys)
        )
        self._data["coop_medals"] = MapMedals(
            **rename_keys(raw_user["_medalsMultiplayer"], map_medal_keys)
        )

        event_medal_keys = [
            ("BlackDiamond", "first"), ("RedDiamond", "second"), ("Diamond", "third"), ("GoldDiamond", "top_50"),
            ("DoubleGold", "top_1_percent"), ("GoldSilver", "top_10_percent"), ("DoubleSilver", "top_25_percent"),
            ("Silver", "top_50_percent"), ("Bronze", "top_75_percent")
        ]
        self._data["boss_normal_medals"] = Medals(
            **rename_keys(raw_user["_medalsBoss"], event_medal_keys)
        )
        self._data["boss_elite_medals"] = Medals(
            **rename_keys(raw_user["_medalsBossElite"], event_medal_keys)
        )
        # self._data["race_medals"] = Medals(
        #     **rename_keys(raw_user["_medals"], event_medal_keys)
        # )

        ct_local_medal_keys = [
            ("BlackDiamond", "first"), ("RedDiamond", "second"), ("Diamond", "third"), ("GoldDiamond", "top_10"),
            ("DoubleGold", "top_20"), ("Silver", "top_40"), ("Bronze", "top_60")
        ]
        ct_global_medal_keys = [
            ("Diamond", "top_25"), ("GoldDiamond", "top_100"), ("DoubleGold", "top_1_percent"),
            ("GoldSilver", "top_10_percent"), ("DoubleSilver", "top_25_percent"), ("Silver", "top_50_percent"),
            ("Bronze", "top_75_percent")
        ]
        self._data["ct_local_medals"] = CTLocalMedals(
            **rename_keys(raw_user["_medalsCTLocal"], ct_local_medal_keys)
        )
        self._data["ct_global_medals"] = CTGlobalMedals(
            **rename_keys(raw_user["_medalsCTLocal"], ct_global_medal_keys)
        )

        stats_keys = [
            ("gameplay.cashEarned", "cash_earned"),
            ("gameplay.challengesCompleted", "challenges_completed"),
            ("gameplay.collectionChestsOpened", "collection_chests_opened"),
            ("gameplay.coopCashGiven", "coop_cash_given"),
            ("gameplay.dailyRewards", "daily_rewards"),
            ("gameplay.gameCount", "game_count"),
            ("gameplay.gamesWon", "games_won"),
            ("gameplay.highestRound", "highest_round"),
            ("gameplay.highestRoundCHIMPS", "highest_round_chimps"),
            ("gameplay.highestRoundDeflation", "highest_round_deflation"),
            ("gameplay.instaMonkeyCollection", "insta_monkey_collection"),
            ("gameplay.monkeyTeamsWins", "monkey_teams_wins"),
            ("gameplay.powersUsed", "powers_used"),
            ("gameplay.totalOdysseysCompleted", "total_odysseys_completed"),
            ("gameplay.totalOdysseyStars", "total_odyssey_stars"),
            ("gameplay.totalTrophiesEarned", "total_trophies_earned"),
            ("bloonsPopped.necroBloonsReanimated", "necro_bloons_reanimated"),
            ("bloonsPopped.bloonsLeaked", "bloons_leaked"),
        ]
        bloons_popped_keys = [
            ("badsPopped", "bads"),
            ("bfbsPopped", "bfbs"),
            ("bloonsPopped", "total"),
            ("camosPopped", "camos"),
            ("ceramicsPopped", "ceramics"),
            ("coopBloonsPopped", "total_coop"),
            ("goldenBloonsPopped", "golden"),
            ("leadsPopped", "leads"),
            ("moabsPopped", "moabs"),
            ("purplesPopped", "purples"),
            ("regrowsPopped", "regrows"),
            ("zomgsPopped", "zomgs"),
        ]
        self._data["stats"] = GameplayStats(
            most_experienced_monkey=Tower.from_string(raw_user["mostExperiencedMonkey"]),
            bloons_popped=BloonsPoppedStats(**rename_keys(raw_user["bloonsPopped"], bloons_popped_keys)),
            **rename_keys(raw_user, stats_keys)
        )

        heroes_placed = {}
        for hero in raw_user["heroesPlaced"].keys():
            heroes_placed[Tower.from_string(hero)] = raw_user["heroesPlaced"][hero]
        self._data["heroes_placed"] = heroes_placed

        self._loaded = True

    @property
    def id(self) -> str:
        return self._id

    @property
    @fetch_property(_load_user)
    def name(self) -> str:
        return self._data["displayName"]

    @property
    @fetch_property(_load_user)
    def rank(self) -> int:
        return self._data["rank"]

    @property
    @fetch_property(_load_user)
    def veteran_rank(self) -> int:
        return self._data["veteranRank"]

    @property
    @fetch_property(_load_user)
    def achievements(self) -> int:
        return self._data["achievements"]

    @property
    @fetch_property(_load_user)
    def followers(self) -> int:
        return self._data["followers"]

    @property
    @fetch_property(_load_user)
    def avatar(self) -> Asset:
        return self._data["avatar"]

    @property
    @fetch_property(_load_user)
    def banner(self) -> Asset:
        return self._data["banner"]

    @property
    @fetch_property(_load_user)
    def single_player_medals(self) -> MapMedals:
        return self._data["single_player_medals"]

    @property
    @fetch_property(_load_user)
    def coop_medals(self) -> MapMedals:
        return self._data["coop_medals"]

    @property
    @fetch_property(_load_user)
    def boss_normal_medals(self) -> Medals:
        return self._data["boss_normal_medals"]

    @property
    @fetch_property(_load_user)
    def boss_elite_medals(self) -> Medals:
        return self._data["boss_elite_medals"]

    # @property
    # @fetch_property(_load_user)
    # def race_medals(self) -> Medals:
    #     return self._data["race_medals"]

    @property
    @fetch_property(_load_user)
    def ct_local_medals(self) -> CTLocalMedals:
        return self._data["ct_local_medals"]

    @property
    @fetch_property(_load_user)
    def ct_global_medals(self) -> CTGlobalMedals:
        return self._data["ct_global_medals"]

    @property
    @fetch_property(_load_user)
    def stats(self) -> GameplayStats:
        return self._data["stats"]

    @property
    @fetch_property(_load_user)
    def heroes_placed(self) -> Dict[Tower, int]:
        return self._data["heroes_placed"]
