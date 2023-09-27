from datetime import datetime
from dataclasses import dataclass
from enum import Enum
from typing import List, Dict, Any
from concurrent.futures import ThreadPoolExecutor
from ...utils.decorators import fetch_property, exception_handler
from ...utils.api import get, get_lb_page
from ..Event import Event
from .User import User
from .Team import Team


class CtPlayer(User):
    """A player who has played a CT event and is on the leaderboard.
    Inherits from :class:`~bloonspy.model.btd6.User`.
    """
    def __init__(self, user_id: str, name: str, score: int, **kwargs):
        super().__init__(user_id, **kwargs)
        self._name = name
        self._score = score

    @property
    def name(self) -> str:
        """The name of the user."""
        return self._name

    @property
    def score(self) -> int:
        """The current CT points of the user."""
        return self._score


class CtTeam(Team):
    """A team who participated in Contested Territory and is on the leaderboards.
    Inherits from :class:`~bloonspy.model.btd6.Team`."""
    def __init__(self, team_id: str, name: str, score: int, **kwargs):
        super().__init__(team_id, **kwargs)
        self._data["full_name"] = name
        self._data["name"] = self.parse_team_name(name)
        self._score = score

    @property
    def score(self) -> int:
        """The current total CT points of the team."""
        return self._score


class CtTileType(Enum):
    """
    *New in 0.6.0.*

    Represents a CT tile's type, or what's on top of it.
    """
    TEAM_START = "Team Start"
    REGULAR = "Regular"
    RELIC = "Relic"
    BANNER = "Banner"

    @staticmethod
    def from_string(value: str) -> "CtTileType":
        value = value.replace(" ", "")
        return tt_switch[value] if value in tt_switch else None


tt_switch = {"TeamFirstCapture": CtTileType.REGULAR}
for tt in CtTileType:
    tt_switch[tt.value.replace(" ", "")] = tt


class GameType(Enum):
    """
    *New in 0.6.0.*

    Represents a CT tile's challenge type.
    """
    LEAST_TIERS = "Least Tiers"
    LEAST_CASH = "Least Cash"
    BOSS = "Boss"
    RACE = "Race"

    @staticmethod
    def from_string(value: str) -> "GameType":
        value = value.replace(" ", "")
        return gt_switch[value] if value in gt_switch else None


gt_switch = {}
for gt in GameType:
    gt_switch[gt.value.replace(" ", "")] = gt


class Relic(Enum):
    """
    *New in 0.6.0.*

    Represents Relic Knowledge.
    """
    ABILITIZED = "Abilitized"
    AIR_AND_SEA = "Air And Sea"
    ALCHEMIST_TOUCH = "Alchemist Touch"
    BIGGER_BLOON_SABOTAGE = "Bigger Bloon Sabotage"
    BOX_OF_CHOCOLATES = "Box Of Chocolates"
    BOX_OF_MONKEY = "Box Of Monkey"
    BROKEN_HEART = "Broken Heart"
    CAMO_FLOGGED = "Camo Flogged"
    CAMO_TRAP = "Camo Trap"
    DEEP_HEAT = "Deep Heat"
    DURABLE_SHOTS = "Durable Shots"
    EL_DORADO = "El Dorado"
    EXTRA_EMPOWERED = "Extra Empowered"
    FLINT_TIPS = "Flint Tips"
    FORTIFRIED = "Fortifried"
    GLUE_TRAP = "Glue Trap"
    GOING_THE_DISTANCE = "Going The Distance"
    HARD_BAKED = "Hard Baked"
    HEARTLESS = "Heartless"
    HERO_BOOST = "Hero Boost"
    MAGIC_MONKEYS = "Magic Monkeys"
    MANA_BULWARK = "Mana Bulwark"
    MARCHING_BOOTS = "Marching Boots"
    MILITARY_MONKEYS = "Military Monkeys"
    MOAB_CLASH = "MOAB Clash"
    MOAB_MINE = "MOAB Mine"
    MONKEY_BOOST = "Monkey Boost"
    MONKEY_SHIELD = "Monkey Shield"
    MONKEY_SHIELD_MARK2 = "Monkey Shield MKII"
    MONKEY_SHIELD_MARK3 = "Monkey Shield MKIII"
    MONKEY_TYCOON = "Monkey Tycoon"
    OPEN_SEASON = "Open Season"
    PRIMARY_PRIMATES = "Primary Primates"
    PSI_VISION = "Psi Vision"
    REGENERATION = "Regeneration"
    RESTORATION = "Restoration"
    ROAD_SPIKES = "Road Spikes"
    ROUNDING_UP = "Rounding Up"
    ROYAL_TREATMENT = "Royal Treatment"
    SHARPSPLOSION = "Sharpsplosion"
    STARTING_STASH = "Starting Stash"
    SMS = "Super Monkey Storm"
    SUPPORT_SIMIANS = "Support Simians"
    TECHBOT = "Techbot"
    THRIVE = "Thrive"

    @staticmethod
    def from_string(value: str) -> "Relic":
        value = value.replace(" ", "")
        return rel_switch[value] if value in rel_switch else None


rel_switch = {}
for rel in Relic:
    rel_switch[rel.value.replace(" ", "")] = rel


@dataclass
class CtTile:
    """
    *New in 0.6.0.*

    Represents a CT tile.
    """
    id: str  #: The 3 letter code of the tile.
    tile_type: CtTileType  #: The tile's type.
    game_type: GameType or None  #: The tile challenge's type. For spawn tiles, it's `None`.
    relic: Relic or None = None  #: The relic this tile hosts, if any.

    def __str__(self) -> str:
        to_join = [
            self.id,
            self.tile_type.value if not self.relic else self.relic.value
        ]
        if self.game_type:
            to_join.append(self.game_type.value)
        to_join[1] = f"[{to_join[1]}]"
        joined = " ".join(to_join)
        return f"<{joined}>"


class ContestedTerritoryEvent(Event):
    """A Contested Territory event. Inherits from :class:`~bloonspy.model.Event`."""
    event_endpoint = "/btd6/ct"
    lb_endpoint_player = "/btd6/ct/{}/leaderboard/player"
    lb_endpoint_team = "/btd6/ct/{}/leaderboard/team"
    event_dict_keys = ["name", "start", "end", "totalScores_player", "totalScores_team"]
    event_name = "CT"

    def _parse_event(self, data: Dict[str, Any]) -> None:
        self._data["totalScores_player"] = data["totalScores_player"]
        self._data["totalScores_team"] = data["totalScores_team"]
        self._data["start"] = datetime.fromtimestamp(data["start"]/1000)
        self._data["end"] = datetime.fromtimestamp(data["end"]/1000)
        self._event_loaded = True

    @property
    def name(self) -> str:
        return f"Contested Territory #{self.event_number}"

    @property
    @fetch_property(Event.load_event, should_load=Event._should_load_property)
    def event_number(self) -> int:
        """Number of the event."""
        first_event_start = datetime.strptime('2022-08-09 22', '%Y-%m-%d %H')
        return int((self.start-first_event_start).days/14) + 1

    @property
    @fetch_property(Event.load_event, should_load=Event._should_load_property)
    def total_scores_player(self) -> int:
        """Number of players who participated in the event."""
        return self._data["totalScores_player"]

    @property
    @fetch_property(Event.load_event, should_load=Event._should_load_property)
    def total_scores_team(self) -> int:
        """Number of teams who participated in the event."""
        return self._data["totalScores_team"]

    @exception_handler(Event.handle_exceptions)
    def leaderboard_player(self, pages: int = 1, start_from_page: int = 1) -> list[CtPlayer]:
        """Get a page of the player leaderboard.

        .. note::
           The returned :class:`~bloonspy.model.btd6.CtPlayer` objects will only
           have the properties :attr:`~bloonspy.model.Loadable.id`, :attr:`~bloonspy.model.btd6.User.name`, and
           :attr:`~bloonspy.model.CtPlayer.score` loaded.

        :param pages: Number of pages to fetch.
        :type pages: int
        :param start_from_page: The first page to fetch.
        :type start_from_page: int

        :return: A list of players in the leaderboard.
        :rtype: List[:class:`~bloonspy.model.btd6.CtPlayer`]

        :raise ~bloonspy.exceptions.NotFound: If the boss doesn't exist or is expired.
        """
        futures = []
        with ThreadPoolExecutor(max_workers=10) as executor:
            for page_num in range(start_from_page, start_from_page + pages):
                futures.append(executor.submit(get_lb_page, self.lb_endpoint_player.format(self._id), page_num))

        players = []
        for page in futures:
            for player in page.result():
                players.append(CtPlayer(
                    player["profile"].split("/")[-1], player["displayName"], player["score"]
                ))

        return players

    @exception_handler(Event.handle_exceptions)
    def leaderboard_team(self, pages: int = 1, start_from_page: int = 1) -> list[CtTeam]:
        """Get a page of the team leaderboard.

        .. note::
           The returned :class:`~bloonspy.model.btd6.CtTeam` objects will only
           have the properties :attr:`~bloonspy.model.Loadable.id`, :attr:`~bloonspy.model.btd6.Team.name`,
           and :attr:`~bloonspy.model.CtTeam.score` loaded.

        :param pages: Number of pages to fetch.
        :type pages: int
        :param start_from_page: The first page to fetch.
        :type start_from_page: int

        :return: A list of teams in the leaderboard.
        :rtype: List[:class:`~bloonspy.model.btd6.CtTeam`]

        :raise ~bloonspy.exceptions.NotFound: If the boss doesn't exist or is expired.
        """
        futures = []
        with ThreadPoolExecutor(max_workers=10) as executor:
            for page_num in range(start_from_page, start_from_page + pages):
                futures.append(executor.submit(get_lb_page, self.lb_endpoint_team.format(self._id), page_num))

        teams = []
        for page in futures:
            for team in page.result():
                teams.append(CtTeam(
                    team["profile"].split("/")[-1], team["displayName"], team["score"]
                ))

        return teams

    @exception_handler(Event.handle_exceptions)
    def tiles(self) -> list[CtTile]:
        tiles = []
        tiles_raw = get(f"/btd6/ct/{self.id}/tiles")["tiles"]
        for tile_data in tiles_raw:
            tile_type = tile_data["type"]
            relic = None
            if "-" in tile_type:
                tile_type, relic = tile_type.split(" - ")
            tiles.append(CtTile(
                tile_data["id"],
                CtTileType.from_string(tile_type),
                GameType.from_string(tile_data["gameType"]),
                Relic.from_string(relic) if relic else None
            ))
        return tiles
