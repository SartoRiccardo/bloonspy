from dataclasses import dataclass, field
from typing import Dict, Any
from ...exceptions import NotFound
from ...utils.decorators import fetch_property
from ...utils.dictionaries import rename_keys
from ..Loadable import Loadable
from ..Asset import Asset
from .Tower import Tower
from .Medals import EventMedals, MapMedals, CTGlobalMedals, CTLocalMedals


@dataclass(kw_only=True)
class BloonsPoppedStats:
    """How many bloons a user has popped of each type."""
    total: int = field(default=0)  #: Total bloons popped.
    total_coop: int = field(default=0)  #: Total bloons popped in coop games.
    camos: int = field(default=0)  #: Number of camo bloons popped.
    regrows: int = field(default=0)  #: Number of regrow bloons popped.
    purples: int = field(default=0)  #: Number of purple bloons popped.
    leads: int = field(default=0)  #: Number of lead bloons popped.
    ceramics: int = field(default=0)  #: Number of ceramic bloons popped.
    moabs: int = field(default=0)  #: Number of MOAB bloons popped.
    bfbs: int = field(default=0)  #: Number of BFB bloons popped.
    zomgs: int = field(default=0)  #: Number of ZOMG bloons popped.
    bads: int = field(default=0)  #: Number of BAD bloons popped.
    # bosses: int = field(default=0)  #: Number of Boss bloons popped.
    golden: int = field(default=0)  #: Number of golden bloons popped.


@dataclass(kw_only=True)
class GameplayStats:
    """User's gameplay stats."""
    most_experienced_monkey: Tower = field(default=Tower.DART_MONKEY)  #: Monkey with the most XP.
    # most_experienced_monkey_xp: int = field(default=0)  #: XP collected for the most experienced monkey.
    cash_earned: int = field(default=0)  #: Total cash earned.
    challenges_completed: int = field(default=0)  #: Total challenges completed.
    collection_chests_opened: int = field(default=0)  #: Number of collection chests opened.
    coop_cash_given: int = field(default=0)  #: Total cash gifted in coop games.
    daily_rewards: int = field(default=0)  #: Total daily rewards collected.
    game_count: int = field(default=0)  #: Number of games played
    games_won: int = field(default=0)  #: Number of games won
    highest_round: int = field(default=0)  #: Highest round beaten
    highest_round_chimps: int = field(default=0)  #: Highest round beaten in CHIMPS mode
    highest_round_deflation: int = field(default=0)  #: Highest round beaten in Deflation mode
    insta_monkey_collection: int = field(default=0)  #: Number of unique Insta Monkeys collected
    monkey_teams_wins: int = field(default=0)  #: Number of games won with the Monkey Teams restrictions.
    powers_used: int = field(default=0)  #: Number of powers used.
    total_odysseys_completed: int = field(default=0)  #: Number of odysseys completed.
    total_odyssey_stars: int = field(default=0)  #: Total odyssey stars.
    total_trophies_earned: int = field(default=0)  #: Lifetime trophies earned through events.
    necro_bloons_reanimated: int = field(default=0)  #: Number of necro bloons reanimated.
    bloons_leaked: int = field(default=0)  #: Total RBE leaked.
    bloons_popped: BloonsPoppedStats = field(default_factory=BloonsPoppedStats)  #: In depth stats about bloons popped.
    damage_done_to_bosses: int = field(default=0)  #: Total damage done to Boss bloons
    transforming_tonics_used: int = field(default=0)  #: Number of times the Transformation Tonic ability was used.
    # monkeys_placed: int = field(default=0)  #: Total monkeys placed.


class User(Loadable):
    """A BTD6 player. Inherits from :class:`~bloonspy.model.Loadable`."""
    endpoint = "/btd6/users/{}"

    def _handle_exceptions(self, exception: Exception) -> None:
        error_msg = str(exception)
        if error_msg == "Invalid user ID / Player Does not play this game":
            raise NotFound(error_msg)

    def _parse_json(self, raw_user: Dict[str, Any]) -> None:
        self._loaded = False

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
        self._data["boss_normal_medals"] = EventMedals(
            **rename_keys(raw_user["_medalsBoss"], event_medal_keys)
        )
        self._data["boss_elite_medals"] = EventMedals(
            **rename_keys(raw_user["_medalsBossElite"], event_medal_keys)
        )
        self._data["race_medals"] = EventMedals(
            **rename_keys(raw_user["_medalsRace"], event_medal_keys)
        )

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
            ("gameplay.damageDoneToBosses", "damage_done_to_bosses"),
            ("bloonsPopped.necroBloonsReanimated", "necro_bloons_reanimated"),
            ("bloonsPopped.transformingTonicsUsed", "transforming_tonics_used"),
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
    @fetch_property(Loadable.load_resource)
    def name(self) -> str:
        """The name of the user."""
        return self._data["displayName"]

    @property
    @fetch_property(Loadable.load_resource)
    def rank(self) -> int:
        """The user's rank."""
        return self._data["rank"]

    @property
    @fetch_property(Loadable.load_resource)
    def veteran_rank(self) -> int:
        """The user's veteran rank, or 0 if they haven't reached it yet."""
        return self._data["veteranRank"]

    @property
    @fetch_property(Loadable.load_resource)
    def achievements(self) -> int:
        """Number of achievements this user unlocked."""
        return self._data["achievements"]

    # @property
    # @fetch_property(Loadable.load_resource)
    # def hidden_achievements(self) -> int:
    #     """Number of hidden achievements this user unlocked."""
    #     return self._data["hiddenAchievements"]

    @property
    @fetch_property(Loadable.load_resource)
    def followers(self) -> int:
        """Number of followers this user has."""
        return self._data["followers"]

    @property
    @fetch_property(Loadable.load_resource)
    def avatar(self) -> Asset:
        """The user's current avatar."""
        return self._data["avatar"]

    @property
    @fetch_property(Loadable.load_resource)
    def banner(self) -> Asset:
        """The user's current banner."""
        return self._data["banner"]

    @property
    @fetch_property(Loadable.load_resource)
    def single_player_medals(self) -> MapMedals:
        """Medals earned in single player mode."""
        return self._data["single_player_medals"]

    @property
    @fetch_property(Loadable.load_resource)
    def coop_medals(self) -> MapMedals:
        """Medals earned in coop mode."""
        return self._data["coop_medals"]

    @property
    @fetch_property(Loadable.load_resource)
    def boss_normal_medals(self) -> EventMedals:
        """Ranked normal boss mdeals."""
        return self._data["boss_normal_medals"]

    @property
    @fetch_property(Loadable.load_resource)
    def boss_elite_medals(self) -> EventMedals:
        """Ranked elite boss medals."""
        return self._data["boss_elite_medals"]

    @property
    @fetch_property(Loadable.load_resource)
    def race_medals(self) -> EventMedals:
        """Race event medals."""
        return self._data["race_medals"]

    @property
    @fetch_property(Loadable.load_resource)
    def ct_local_medals(self) -> CTLocalMedals:
        """Contested Territory local medals."""
        return self._data["ct_local_medals"]

    @property
    @fetch_property(Loadable.load_resource)
    def ct_global_medals(self) -> CTGlobalMedals:
        """Contested Territory global medals."""
        return self._data["ct_global_medals"]

    @property
    @fetch_property(Loadable.load_resource)
    def stats(self) -> GameplayStats:
        """Gameplay stats."""
        return self._data["stats"]

    @property
    @fetch_property(Loadable.load_resource)
    def heroes_placed(self) -> Dict[Tower, int]:
        """Number of times each hero has been placed."""
        return self._data["heroes_placed"]
