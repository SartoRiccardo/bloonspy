from dataclasses import dataclass, field
from .Gamemode import Gamemode, Difficulty, Mode
from enum import Enum
import re


@dataclass
class GamemodeCompletionData:
    """Statistics of a gamemode in a map."""
    completed: bool  #: Whether this gamemode was beaten.
    completed_without_loading_save: bool  #: Whether this gamemode was beaten without loading from saves.
    highest_round: int  #: Highest round on this gamemode.
    times_completed: int  #: Number of times this gamemode was completed.


class MapBorder(Enum):
    """Colors of the border of a map, to symbolize progression."""
    NONE = "None"
    BRONZE = "Bronze"
    SILVER = "Silver"
    GOLD = "Gold"
    BLACK = "Black"


@dataclass
class MapProgress:
    """The User's progress in a map."""
    beaten: bool  #: Whether the map was beaten at least once, in any gamemode.
    single_player: dict[Gamemode, GamemodeCompletionData]  #: Single player map progress.
    coop: dict[Gamemode, GamemodeCompletionData]  #: Coop map progress.
    single_player_border: MapBorder = MapBorder.NONE  #: The border of the map.
    coop_border: MapBorder = MapBorder.NONE  #: The border of the map, in coop.

    def __post_init__(self):
        self.single_player_border = self.__get_border(self.single_player)
        self.coop_border = self.__get_border(self.coop)

    @staticmethod
    def __get_border(completion_data: dict[Gamemode, GamemodeCompletionData]) -> MapBorder:
        border = MapBorder.NONE
        easy_modes = Gamemode.easy_modes()
        if MapProgress.__completed_all(easy_modes, completion_data):
            border = MapBorder.BRONZE
            medium_modes = Gamemode.medium_modes()
            if MapProgress.__completed_all(medium_modes, completion_data):
                border = MapBorder.SILVER
                hard_modes = Gamemode.hard_modes()
                if MapProgress.__completed_all(hard_modes, completion_data):
                    border = MapBorder.GOLD
                    chimps = Gamemode(Difficulty.HARD, Mode.CHIMPS)
                    if completion_data[chimps].completed_without_loading_save:
                        border = MapBorder.BLACK

        return border

    @staticmethod
    def __completed_all(gamemodes: list[Gamemode],
                        completion_data: dict[Gamemode, GamemodeCompletionData]) -> bool:
        for gm in gamemodes:
            if gm not in completion_data or not completion_data[gm].completed:
                return False
        return True


class Map(Enum):
    """All maps present in the game."""
    MONKEY_MEADOW = "Monkey Meadow"
    TREE_STUMP = "Tree Stump"
    TOWN_CENTRE = "Town Centre"
    PARK_PATH = "Park Path"
    ALPINE_RUN = "Alpine Run"
    FROZEN_OVER = "Frozen Over"
    IN_THE_LOOP = "In The Loop"
    CUBISM = "Cubism"
    FOUR_CIRCLES = "Four Circles"
    HEDGE = "Hedge"
    END_OF_THE_ROAD = "End Of The Road"
    LOGS = "Logs"
    SPRING_SPRING = "Spring Spring"
    KARTSNDARTS = "Karts N Darts"
    MOON_LANDING = "Moon Landing"
    HAUNTED = "Haunted"
    DOWNSTREAM = "Downstream"
    FIRING_RANGE = "Firing Range"
    CRACKED = "Cracked"
    STREAMBED = "Streambed"
    CHUTES = "Chutes"
    RAKE = "Rake"
    SPICE_ISLANDS = "Spice Islands"
    CARGO = "Cargo"
    PATS_POND = "Pat's Pond"
    PENINSULA = "Peninsula"
    HIGH_FINANCE = "High Finance"
    ANOTHER_BRICK = "Another Brick"
    OFF_THE_COAST = "Off The Coast"
    CORNFIELD = "Cornfield"
    UNDERGROUND = "Underground"
    QUAD = "Quad"
    DARK_CASTLE = "Dark Castle"
    MUDDY_PUDDLES = "Muddy Puddles"
    OUCH = "#ouch"
    SPILLWAY = "Spillway"
    WORKSHOP = "Workshop"
    CARVED = "Carved"
    BLOODY_PUDDLES = "Bloody Puddles"
    WINTER_PARK = "Winter Park"
    ADORAS_TEMPLE = "Adora's Temple"
    INFERNAL = "Infernal"
    GEARED = "Geared"
    CANDY_FALLS = "Candy Falls"
    BAZAAR = "Bazaar"
    FLOODED_VALLEY = "Flooded Valley"
    LOTUS_ISLAND = "Lotus Island"
    RESORT = "Resort"
    SKATES = "Skates"
    BLOONARIUS_PRIME = "Bloonarius Prime"
    BALANCE = "Balance"
    ENCRYPTED = "Encrypted"
    X_FACTOR = "X Factor"
    MESA = "Mesa"
    SANCTUARY = "Sanctuary"
    RAVINE = "Ravine"
    SCRAPYARD = "Scrapyard"
    THE_CABIN = "The Cabin"
    QUARRY = "Quarry"
    QUIET_STREET = "Quiet Street"
    SUNKEN_COLUMNS = "Sunken Columns"
    COVERED_GARDEN = "Covered Garden"
    MIDNIGHT_MANSION = "Midnight Mansion"
    ONE_TWO_TREE = "One Two Tree"
    MIDDLE_OF_THE_ROAD = "Middle Of The Road"
    POLYPHEMUS = "Polyphemus"
    WATER_PARK = "Water Park"

    @staticmethod
    def from_string(value: str) -> "Map":
        quirky_names = {
            "Tutorial": Map.MONKEY_MEADOW,
        }
        if value in quirky_names.keys():
            return quirky_names[value]

        return map_switch[value] if value in map_switch else None


map_switch = {}
for game_map in Map:
    map_switch[re.sub(r"[' ]", "", game_map.value)] = game_map
