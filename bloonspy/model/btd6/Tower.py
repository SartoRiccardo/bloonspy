from enum import Enum


class Tower(Enum):
    QUINCY = "Quincy"
    GWENDOLIN = "Gwendolin"
    STRIKER_JONES = "Striker Jones"
    OBYN = "Obyn Greenfoot"
    CHURCHILL = "Captain Churchill"
    BENJAMIN = "Benjamin"
    EZILI = "Ezili"
    PAT_FUSTY = "Pat Fusty"
    SAUDA = "Sauda"
    PSI = "Psi"
    GERALDO = "Geraldo"
    BRICKELL = "Admiral Brickell"
    ETIENNE = "Etienne"
    ADORA = "Adora"

    DART_MONKEY = "Dart Monkey"
    BOOMERANG_MONKEY = "Boomerang Monkey"
    TACK_SHOOTER = "Tack Shooter"
    BOMB_SHOOTER = "Bomb Shooter"
    GLUE_GUNNER = "Glue Gunner"
    ICE_MONKEY = "Ice Monkey"

    SNIPER_MONKEY = "Sniper Monkey"
    MONKEY_BUCCANEER = "Monkey Buccaneer"
    MONKEY_SUB = "Monkey Sub"
    DARTLING_GUNNER = "Dartling Gunner"
    MONKEY_ACE = "Monkey Ace"
    HELI_PILOT = "Heli Pilot"
    MORTAR_MONKEY = "Mortar Monkey"

    WIZARD_MONKEY = "Wizard Monkey"
    NINJA_MONKEY = "Ninja Monkey"
    SUPER_MONKEY = "Super Monkey"
    DRUID = "Druid"
    ALCHEMIST = "Alchemist"

    MONKEY_VILLAGE = "Monkey Village"
    BANANA_FARM = "Banana Farm"
    ENGINEER_MONKEY = "Engineer Monkey"
    SPIKE_FACTORY = "Spike Factory"
    BEAST_HANDLER = "Beast Handler"

    @staticmethod
    def from_string(value: str) -> "Tower":
        tower_switch = {
            "Quincy": Tower.QUINCY,
            "Gwendolin": Tower.GWENDOLIN,
            "StrikerJones": Tower.STRIKER_JONES,
            "ObynGreenfoot": Tower.OBYN,
            "CaptainChurchill": Tower.CHURCHILL,
            "Benjamin": Tower.BENJAMIN,
            "Ezili": Tower.EZILI,
            "PatFusty": Tower.PAT_FUSTY,
            "Sauda": Tower.SAUDA,
            "Psi": Tower.PSI,
            "Geraldo": Tower.GERALDO,
            "AdmiralBrickell": Tower.BRICKELL,
            "Etienne": Tower.ETIENNE,
            "Adora": Tower.ADORA,
            "DartMonkey": Tower.DART_MONKEY,
            "BoomerangMonkey": Tower.BOOMERANG_MONKEY,
            "TackShooter": Tower.TACK_SHOOTER,
            "BombShooter": Tower.BOMB_SHOOTER,
            "GlueGunner": Tower.GLUE_GUNNER,
            "IceMonkey": Tower.ICE_MONKEY,
            "SniperMonkey": Tower.SNIPER_MONKEY,
            "MonkeyBuccaneer": Tower.MONKEY_BUCCANEER,
            "MonkeySub": Tower.MONKEY_SUB,
            "DartlingGunner": Tower.DARTLING_GUNNER,
            "MonkeyAce": Tower.MONKEY_ACE,
            "HeliPilot": Tower.HELI_PILOT,
            "MortarMonkey": Tower.MORTAR_MONKEY,
            "WizardMonkey": Tower.WIZARD_MONKEY,
            "NinjaMonkey": Tower.NINJA_MONKEY,
            "SuperMonkey": Tower.SUPER_MONKEY,
            "Druid": Tower.DRUID,
            "Alchemist": Tower.ALCHEMIST,
            "MonkeyVillage": Tower.MONKEY_VILLAGE,
            "BananaFarm": Tower.BANANA_FARM,
            "EngineerMonkey": Tower.ENGINEER_MONKEY,
            "SpikeFactory": Tower.SPIKE_FACTORY,
            "BeastHandler": Tower.BEAST_HANDLER,
        }
        return tower_switch[value] if value in tower_switch else None

    def is_hero(self):
        return self in [
            Tower.QUINCY, Tower.GWENDOLIN, Tower.STRIKER_JONES, Tower.OBYN, Tower.CHURCHILL, Tower.BENJAMIN,
            Tower.EZILI, Tower.PAT_FUSTY, Tower.SAUDA, Tower.PSI, Tower.GERALDO, Tower.BRICKELL, Tower.ETIENNE,
            Tower.ADORA
        ]
