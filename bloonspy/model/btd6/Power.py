from enum import Enum
from dataclasses import dataclass


@dataclass(frozen=True, eq=True)
class PowerAmount:
    """
    *New in 0.5.1*

    Describes how many powers of a single type an User has.
    """
    quantity: int  #: How much of this power an user has.
    is_new: bool  #: Whether the User has just gotten this power (it has the little red exclamation mark in the top-right).


class Power(Enum):
    """Available powers in the game"""
    SMS = "Super Monkey Storm"
    MONKEY_BOOST = "Monkeyboost"
    THRIVE = "Thrive"
    TIME_STOP = "Time Stop"
    CASH_DROP = "Cash Drop"
    PONTOON = "Pontoon"
    ROAD_SPIKES = "Road Spikes"
    GLUE_TRAP = "Glue Trap"
    MOAB_MINE = "Moab Mine"
    CAMO_TRAP = "Camo Trap"
    PORTABLE_LAKE = "Portable Lake"
    TECH_BOT = "Tech Bot"
    ENERGISING_TOTEM = "Energising Totem"
    BANANA_FARMER = "Banana Farmer"

    @staticmethod
    def from_string(power: str) -> "Power":
        power_switch = {
            "SuperMonkeyStorm": Power.SMS,
            "MonkeyBoost": Power.MONKEY_BOOST,
            "Thrive": Power.THRIVE,
            "DartTime": Power.TIME_STOP,
            "CashDrop": Power.PONTOON,
            "BananaFarmer": Power.BANANA_FARMER,
            "Pontoon": Power.CASH_DROP,
            "RoadSpikes": Power.ROAD_SPIKES,
            "GlueTrap": Power.GLUE_TRAP,
            "MoabMine": Power.MOAB_MINE,
            "CamoTrap": Power.CAMO_TRAP,
            "PortableLake": Power.PORTABLE_LAKE,
            "TechBot": Power.TECH_BOT,
            "EnergisingTotem": Power.ENERGISING_TOTEM,
        }
        power = power_switch[power] if power in power_switch else None
        return power
