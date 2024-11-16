import re
from enum import Enum


class Tower(Enum):
    """Available towers in the game."""
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
    MERMONKEY = "Mermonkey"

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
            "Mermonkey": Tower.MERMONKEY,
        }
        return tower_switch[value] if value in tower_switch else None

    def is_hero(self):
        return self in [
            Tower.QUINCY, Tower.GWENDOLIN, Tower.STRIKER_JONES, Tower.OBYN, Tower.CHURCHILL, Tower.BENJAMIN,
            Tower.EZILI, Tower.PAT_FUSTY, Tower.SAUDA, Tower.PSI, Tower.GERALDO, Tower.BRICKELL, Tower.ETIENNE,
            Tower.ADORA
        ]


class HeroSkin(Enum):
    """Alternative hero costumes in the game."""
    # Why are these 3 skins????
    PSI = "Psi"
    GERALDO = "Geraldo"
    SAUDA = "Sauda"

    BENJAMMIN = "BenJammin"
    SCIENTIST_GWENDOLIN = "Scientist Gwendolin"
    BIKER_BONES = "Biker Bones"
    OCEAN_GUARDIAN_OBYN = "Ocean Guardian Obyn"
    SENTAI_CAPTAIN_CHURCHILL = "Sentai Captain Churchill"
    CYBER_QUINCY = "Cyber Quincy"  # Yoo it's the Hemi thing!
    SMUDGE_CATT = "Smudge Catt"
    JOAN_OF_ARC_ADORA = "Joan Of Arc Adora"
    HARLEGWEN = "Harlegwen"
    OCTOJONES = "Octo Jones"
    ETN = "ETN"
    VOIDORA = "Voidora"
    GALAXILI = "Galaxili"
    DREAD_PIRATE_BRICKELL = "Dread Pirate Brickell"
    MOUNTAIN_OBYN = "Mountain Obyn"
    SUSHI_BENTO = "Sushi Bento"
    VIKING_SAUDA = "Viking Sauda"
    WOLFPACK_QUINCY = "Wolfpack Quincy"
    PSIMBALS = "Psimbals"
    FUSTY_THE_SNOWMAN = "Fusty The Snowman"
    SLEIGH_CAPTAIN_CHURCHILL = "Sleigh Captain Churchill"
    KAIJU_PAT = "Kaiju Pat"
    JIANGSHI_SAUDA = "Jiangshi Sauda"
    LIFEGUARD_BRICKELL = "Lifeguard Brickell"

    @staticmethod
    def from_string(value: str) -> "HeroSkin":
        quirky_names = {
            "ObynOceanGuardian": HeroSkin.OCEAN_GUARDIAN_OBYN,
            "CircusGwendolin": HeroSkin.HARLEGWEN,
            "ETnEtienne": HeroSkin.ETN,
            "MoltenObyn": HeroSkin.MOUNTAIN_OBYN,
        }
        if value in quirky_names.keys():
            return quirky_names[value]

        value = re.sub(r"\s+", "", value)
        return hero_skin_switch[value] if value in hero_skin_switch else None


hero_skin_switch = {}
for hero_skin in HeroSkin:
    hero_skin_switch[re.sub(r"\s+", "", hero_skin.value)] = hero_skin
