from enum import Enum


class Power(Enum):
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
