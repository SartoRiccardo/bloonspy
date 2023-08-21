import re
from dataclasses import dataclass


@dataclass(frozen=True, eq=True)
class BloonsPopFx:
    """
    *New in 0.5.0*

    Purchase status of Bloons Pop FX.
    """
    mo_monkeys: bool  #: The Mo' Monkeys pop FX.
    confetti: bool  #: The Confetti pop FX.
    flowers: bool  #: The Flowers pop FX.
    pewpew: bool  #: The PewPew Pop pop FX.
    pow_pop: bool  #: The Pow Pop pop FX.
    snowflakes: bool  #: The Snowflakes pop FX.
    water_bloon: bool  #: The Water bloon pop FX.
    bones: bool  #: *New in 0.5.1.* The Bones pop FX


@dataclass(frozen=True, eq=True)
class MoabSkins:
    """
    *New in 0.5.0*

    Purchase status of MOAB skins.
    """
    all_old_timey: bool  #: The Old Timey skin.
    bad_skeleton: bool  #: The BAD Skeleton skin.
    bad_pinata: bool  #: The BAD Pinata skin.
    bad_whale: bool  #: The BAD Whale skin.
    bfb_btd4_retro: bool  #: The BFB BTD4 Retro skin.
    bfb_chocolate_egg: bool  #: The BFB Chocolate Egg skin.
    bfb_lantern: bool  #: The BFB Lantern skin.
    bfb_lobster: bool  #: The BFB Lobster skin.
    bfb_pizza: bool  #: The BFB Pizza skin.
    bfb_sci_fi: bool  #: The BFB Sci-Fi skin.
    ddt_shark: bool  #: The DDT Shark skin.
    ddt_neon: bool  #: The DDT Neon skin.
    moab_btd4_retro: bool  #: The MOAB BTD4 Retro skin.
    moab_chocolate_egg: bool  #: The MOAB Chocolate Egg skin.
    moab_football: bool  #: The MOAB Football skin.
    moab_frozen_glacier: bool  #: The MOAB Frozen Glacier skin.
    moab_mauler: bool  #: The MOAB Mauler skin.
    moab_pufferfish: bool  #: The MOAB Pufferfish skin.
    zomg_steampunk: bool  #: The ZOMG Steampunk skin.
    zomg_watermelon: bool  #: The ZOMG Watermelon skin.
    ddt_doomsleigh: bool  #: *New in 0.5.1.* The DDT Doomsleigh skin.
    ddt_spider: bool  #: *New in 0.5.1.* The DDT Spider skin.
    moab_boat: bool  #: *New in 0.5.1.* The MOAB Boat skin.
    zomg_jack_o_lantern: bool  #: *New in 0.5.1.* The ZOMG Jack-O-Lantern skin.


@dataclass(frozen=True, eq=True)
class BloonDecals:
    """
    *New in 0.5.0*

    Purchase status of bloon decals.
    """
    bloons_beards: bool  #: The Beard cosmetic.
    all_bucket_hat: bool  #: The Bucket Hat cosmetic.
    bloons_bunny_ears: bool  #: The Bunny Ears cosmetic.
    all_cat_ear: bool  #: The Cat Ears cosmetic.
    bloons_daisy_chain: bool  #: The Daisy Chain cosmetic.
    all_googly_eyes: bool  #: The Googly Eyes cosmetic.
    all_disguise_glasses: bool  #: The Disguise Glasses cosmetic.
    all_party_hat: bool  #: The Party Hat cosmetic.
    all_top_hats: bool  #: The Top Hat cosmetic.
    all_trucker_hats: bool  #: The Trucker Hat cosmetic.
    all_hatchet: bool  #: *New in 0.5.1.* The Hatchet cosmetic.
    all_elf_hat: bool  #: *New in 0.5.1.* The Elf Hat cosmetic.
    moab_red_nose: bool  #: *New in 0.5.1.* The Red Nose MOAB cosmetic.
    bloons_santa_hats: bool  #: *New in 0.5.1.* The Santa Hats cosmetic.
    all_sunglasses: bool  #: *New in 0.5.1.* The Sunglasses cosmetic.
    bloons_vampire_cape: bool  #: *New in 0.5.1.* The Vampire Cape cosmetic.


@dataclass(frozen=True, eq=True)
class CoopEmotes:
    """
    *New in 0.5.0*

    Purchase status of Coop emotes.
    """
    animation_begging_monkey: bool  #: The Pleeeease Monkey emote.
    animation_ben_cool: bool  #: The Ben Cool emote.
    animation_biker_bones_rage: bool  #: The Biker Bones Rage emote.
    fullscreen_celebration: bool  #: The Celebration animation.
    fulscreen_confetti_cannon: bool  #: The Confetti Cannon animation.
    fullscreen_disco_ball: bool  #: The Disco Ball animation.
    animation_ezili_facepalm: bool  #: The Ezili Facepalm emote.
    animation_fistpump: bool  #: The Fist Pump emote.
    fullscreen_flower_bloom: bool  #: The Flower Bloom emote.
    fullscreen_love_hearts: bool  #: The Love Hearts animation.
    animation_mind_blown: bool  #: The Mind Blown emote.
    animation_obyn_peace: bool  #: The Obyn Peace emote.
    animation_panic_monkey: bool  #: The Panic Monkey emote.
    animation_pat_flex: bool  #: The Pat Flex emote.
    animation_pixel_monkey_dance: bool  #: The Pixel Monkey Dance emote.
    icon_player_numbers: bool  #: The Player Number Icons emote.
    animation_psigh: bool  #: The Psigh emote.
    fullscreen_rainbow: bool  #: The Rainbow animation.
    sound_siren: bool  #: The Siren sound.
    fullscreen_sparkling_hearts: bool  #: The Sparkling Hearts animation.
    animation_thinking_monkey: bool  #: The Thinking Monkey emote.
    animation_trophy: bool  #: The Trophy emote.
    animation_tumbleweed: bool  #: The Tumbleweed emote.
    icon_danger: bool  #: The Danger Icon emote.
    icon_no_cash_drops: bool  #: The No Cash Drops emote.
    icon_skull_and_crossbones: bool  #: The Skull and Crossbones emote.
    icon_stop: bool  #: The Stop Icon emote.
    sound_airhorn: bool  #: The Airhorn sound.
    sound_crickets: bool  #: The Crickets sound.
    sound_scream: bool  #: The Scream sound.
    text_activate: bool  #: The "Activate!" emote.
    text_all_is_fine: bool  #: The "All is Fine" emote.
    text_amazing: bool  #: The "Amazing" emote.
    text_lets_go: bool  #: The "Let's Go" emote.
    text_need_more: bool  #: The "Need More!" emote.
    text_next_round_scary: bool  #: The "Next Round! Scary!" emote.
    text_ok: bool  #: The "OK" emote.
    text_perfect_timing: bool  #: The "Perfect Timing" emote.
    text_why: bool  #: The "Why?!" emote.
    fullscreen_happy_holidays: bool  #: *New in 0.5.1.* The Happy Holidays! emote.
    fullscreen_snow_and_sleighbells: bool  #: *New in 0.5.1.* The Snow and Sleighbells animation.
    icon_tower_types: bool  #: *New in 0.5.1.* The Tower Types emote.
    # round_100: bool  #: *New in 0.x.x.* The Round 100 emote.


@dataclass(frozen=True, eq=True)
class HeroPlacementFx:
    """
    *New in 0.5.0*

    Purchase status of Hero placement effects.
    """
    adora_sunbeam: bool  #: Adora's Sunbeam placement FX.
    benjamin_matrix: bool  #: Benjamin's Matrix placement FX.
    benjammin_party_lights: bool  #: BenJammin's Party Lights placement FX.
    churchill_tank_drop: bool  #: Churchill's Tank Drop placement FX.
    etn_beam_down: bool  #: ETN's Beam Down placement FX.
    ezili_glyph: bool  #: Ezili's Glyph placement FX.
    gwendolin_fireball: bool  #: Gwen's Fireball placement FX.
    pat_fusty_superjump: bool  #: Pat's Superjump placement FX.
    cyber_quincy_fireworks: bool  #: Cyber Quincy's Fireworks placement FX.
    quincy_special_forces: bool  #: Quincy's Special Forces placement FX.
    biker_bones_hellrift: bool  #: Biker Bones' Hellrift placement FX.
    striker_jones_paradrop: bool  #: Striker Jones' Paradrop placement FX.


@dataclass(frozen=True, eq=True)
class TowerProjectiles:
    """
    *New in 0.5.0*

    Purchase status of custom Tower projectiles.
    """
    alchemist_spring_flowers: bool  #: Alchemist's spring flower projectiles.
    dartling_easter_eggs: bool  #: Dartling Gunner's easter egg projectiles.
    spike_factory_pineapples: bool  #: Spike Factory's pineapple spikes.
    wizard_zombies: bool  #: Necromancer's smiling zombie bloons.
    farm_candy_corn: bool  #: *New in 0.5.1.* The Banana Farm's Candy Corn bananas.
    farm_presents: bool  #: *New in 0.5.1.* The Banana Farm's Present bananas.
    bomb_pumpkin: bool  #: *New in 0.5.1.* The Bomb Shooter's Pumpkin bombs.
    boomerang_candy_cane: bool  #: *New in 0.5.1.* The Boomerang Monkey's Candy Cane projectiles.
    dart_monkey_snowballs: bool  #: *New in 0.5.1.* The Dart Monkey's Snowball projectiles.
    engineer_vampire_hunter: bool  #: *New in 0.5.1.* The Engineer's Vampire bloontraps.
    monkey_ace_bones: bool  #: *New in 0.5.1.* The Monkey Ace's Bone projectiles.
    mortar_snow: bool  #: *New in 0.5.1.* The Mortar's Snow projectiles.
    ninja_snowflakes: bool  #: *New in 0.5.1.* The Ninja Monkey's Snowflake projectiles.
    sniper_confetti: bool  #: *New in 0.5.1.* The Sniper's Confetti projectiles.
    tack_icicles: bool  #: *New in 0.5.1.* The Tack Shooter's Icicle projectiles.
    wizard_fireworks: bool  #: *New in 0.5.1.* The Wizard Monkey's Firework projectiles.


@dataclass(frozen=True, eq=True)
class TowerPets:
    """
    *New in 0.5.0*

    Purchase status of Tower and Hero pets.
    """
    banana_farm_chicken: bool  #: The Banana Farm's Chicken pet.
    glue_gunner_rat: bool  #: The Glue Gunner's Glue Rat pet.
    heli_pilot_hummingbird: bool  #: The Heli Pilot's Hummingbird pet.
    monkey_ace_dragonfly: bool  #: The Monkey Ace's Dragonfly pet.
    monkey_buccaneer_narwhal: bool  #: The Monkey Buccaneer's Narwhal pet.
    monkey_sub_rubber_duck: bool  #: The Monkey Sub's Rubber Duck pet.
    ninja_monkey_kiwi: bool  #: The Ninja's Kiwi pet.
    sniper_monkey_chameleon: bool  #: The Sniper Monkey's Chameleon pet.
    super_monkey_bat: bool  #: The Super Monkey's Bat pet.
    tack_shooter_hedgehog: bool  #: The Tack Shooter's Hedgehog pet.

    brickell_parrot: bool  #: Brickell's Parrot pet.
    sentai_churchill_drone: bool  #: Sentai Churchill's Drone pet.
    etienne_roomba: bool  #: Etienne's Roomba pet.
    ezili_frog: bool  #: Ezili's Frog pet.
    geraldo_pack_mule: bool  #: Gerald's Pack Mule pet.
    gwendolin_firefox: bool  #: Gwen's Firefox pet.
    joan_of_arc_adora_dragon: bool  #: Joan of Arc Adora's Dragon pet.
    mountain_obyn_balfrog: bool  #: Mountain Obyn's Balfrog pet.
    obyn_bunny: bool  #: Obyn's Bunny pet.
    obyn_wolf: bool  #: Obyn's Wolf pet.
    psi_bison: bool  #: Psi's Bison pet.
    quincy_dad_of_quincy: bool  #: Quincy's Dad of Quincy pet.
    sauda_crane: bool  #: Sauda's Crane pet.
    striker_jones_german_shepherd: bool  #: Striker Jones' German Shepherd pet.

    bomb_shooter_tortoise: bool  #: *New in 0.5.1.* The Bomb Shooter's Tortoise pet.
    ice_monkey_snowman: bool  #: *New in 0.5.1.* The Ice Monkey's Snowman pet.
    village_elf: bool  #: *New in 0.5.1.* The Monkey Village's Elf pet.
    pat_penguin: bool  #: *New in 0.5.1.* Pat Fusty's Penguin pet.


@dataclass(frozen=True, eq=True)
class AllMonkeyFx:
    """
    *New in 0.5.0*

    Purchase status of Monkey FX that apply to all monkeys.
    """
    bats: bool  #: The Bats upgrade FX.
    butterflies: bool  #: The Butterflies upgrade FX.
    ghosts: bool  #: The Ghosts upgrade FX.
    fireworks: bool  #: *New in 0.5.1.* The Fireworks upgrade FX.
    presents: bool  #: *New in 0.5.1.* The Presents upgrade FX.


@dataclass(frozen=True, eq=True)
class PowerSkins:
    """
    *New in 0.5.0*

    Purchase status of Power skins.
    """
    banana_farmer_banana_costume: bool  #: The Banana Farmer's Banana Costume.
    dart_time_matrix: bool  #: The Time Stop's Dart Matrix.
    glue_trap_honey_trap: bool  #: The Glue Trap's Honey Trap.
    iceberg_pontoon: bool  #: The Pontoon's Iceberg.
    lava_lake: bool  #: The Portable Lake's Lava Lake.
    monkey_boost_sugar_rush: bool  #: The Monkey Boost's Sugar Rush.
    road_spikes_flower_patch: bool  #: The Road Spikes' Flower Patch.
    super_vampire_storm: bool  #: The Super Monkey Storm's Vampire Storm.
    thrive_stonks: bool  #: The Thrive Stonks.
    mine_bauble: bool  #: *New in 0.5.1.* The Moab Mine's Bauble.
    camo_trap_sprinkler: bool  #: *New in 0.5.1.* The Camo Trap's Sprinkler.
    cash_drop_coffin: bool  #: *New in 0.5.1.* The Cash Drop's Coffin Drop.
    energising_totem_christmas_tree: bool  #: *New in 0.5.1.* The Energising Totem's Christmas Tree.
    banana_farmer_reaper: bool  #: *New in 0.5.1.* The Banana Farmer's Reaper.
    monkey_boost_fireworks: bool  #: *New in 0.5.1.* The Monkey Boost's Fireworks.
    retro_techbot: bool  #: *New in 0.5.1.* The Techbot's Retro skin.


@dataclass(frozen=True, eq=True)
class MusicTracks:
    """
    *New in 0.5.0*

    Purchase status of music tracks.
    """
    bmc_street_party: bool  #: The "BMC Street Party" music track.
    fiesta_synthwave_mix: bool  #: The "Fiesta Flamenco - Synthwave Mix" music track.
    jingle_bloons: bool  #: The "Jingle - Bloons" music track.
    sunset64_mix: bool  #: The "Sunset - 64 Mix" music track.
    sunset_silent_night_mix: bool  #: The "Sunset - Silent Night Mix" music track.
    sunshine_fiesta_mix: bool  #: The "Sunshine - Fiesta Mix" music track.
    sunshine_gameboy_mix: bool  #: The "Sunshine - Gameboy Mix" music track.
    title_fiesta_mix: bool  #: The "Title - Fiesta Mix" music track.
    tribes_funked_mix: bool  #: The "Tribes - Funked Mix" music track.
    tribes_jaloon_mix: bool  #: The "Tribes - Jaloon Mix" music track.
    tropical_complextro_mix: bool  #: The "Tropical - Complextro Mix" music track.
    tropical_octopus_mix: bool  #: The "Tropical - Octopus Mix" music track.
    winter_chilled_mix: bool  #: The "Winter - Chilled Mix" music track.
    fiesta_helium_heights_mix: bool  # *New in 0.5.1.* The "Fiesta Flamenco - Helium Heights Mix" music track.
    haunted_house: bool  # *New in 0.5.1.* The "Haunted House" music track.


@dataclass(frozen=True, eq=True)
class VillageFlagCosmetics:
    """
    *New in 0.5.0*

    Purchase status of the Village flag cosmetics.
    """
    flag_australian: bool  #: The Australian flag
    flag_banana: bool  #: The Banana Republic flag
    flag_brazil: bool  #: The Brazil flag
    flag_canada: bool  #: The Canada flag
    flag_germany: bool  #: The Germany flag
    flag_new_zeland: bool  #: The New Zeland flag
    flag_pride: bool  #: The pride flag
    flag_scotland: bool  #: The Scotland flag
    flag_sweden: bool  #: The Sweden flag
    flag_uk: bool  #: The UK flag
    flag_usa: bool  #: The USA flag


@dataclass(frozen=True, eq=True)
class TrophyStoreItemStatus:
    """
    *New in 0.5.0*

    Purchase status of all trophy store items.
    """
    bloon_pop_fx: BloonsPopFx  #: Effects when bloons pop.
    bloon_decals: BloonDecals  #: Decals that apply to Bloons, MOABs, or both.
    moab_skins: MoabSkins  #: Skins that apply to all or specific MOAB-class bloons.
    coop_emotes: CoopEmotes  #: Coop emotes bought.
    music_tracks: MusicTracks  #: Music tracks bought.
    power_skins: PowerSkins  #: Skins that apply to Powers.
    avatars: dict[int, bool]  #: Avatars bought, the dict keys represent the numeric ID of the avatar.
    banners: dict[int, bool]  #: Banners bought, the dict keys represent the numeric ID of the banner.
    monkey_names: bool  #: Whether Monkey Names has been bought.
    hero_fx: HeroPlacementFx  #: Hero placement/upgrade effects.
    all_monkeys: AllMonkeyFx  #: Cosmetics that apply to all monkeys.
    pets: TowerPets  #: Tower pets bought.
    projectiles: TowerProjectiles  #: Tower projectiles bought.
    village_flags: VillageFlagCosmetics  #: Village flags bought.

    @staticmethod
    def from_json(trophy_store_data: dict) -> "TrophyStoreItemStatus":
        avatars = {}
        banners = {}
        for item in trophy_store_data.keys():
            if match := re.match(r"GameUIProfileBanner(\d+)", item):
                avatars[int(match.group(1))] = trophy_store_data[item]
            elif match := re.match(r"GameUIProfileAvatar(\d+)", item):
                banners[int(match.group(1))] = trophy_store_data[item]

        emote_keys = [
            "CoopEmoteAnimationBeggingMonkey", "CoopEmoteAnimationBenCool", "CoopEmoteAnimationBikerBonesRage",
            "CoopEmoteAnimationCelebration", "CoopEmoteAnimationConfetti", "CoopEmoteAnimationDiscoBall",
            "CoopEmoteAnimationFacepalm", "CoopEmoteAnimationFistpump", "CoopEmoteAnimationFlowerBloom",
            "CoopEmoteAnimationLoveHearts", "CoopEmoteAnimationMindBlown", "CoopEmoteAnimationObynPeace",
            "CoopEmoteAnimationPanicMonkey", "CoopEmoteAnimationPatFlex", "CoopEmoteAnimationPixelMonkeyDance",
            "CoopEmoteAnimationPlayerNumbers", "CoopEmoteAnimationPsigh", "CoopEmoteAnimationRainbow",
            "CoopEmoteAnimationSiren", "CoopEmoteAnimationSparklingHearts", "CoopEmoteAnimationThinkingMonkey",
            "CoopEmoteAnimationTrophy", "CoopEmoteAnimationTumbleweed", "CoopEmoteIconDanger",
            "CoopEmoteIconNoCashDrops", "CoopEmoteIconSkullAndCrossbones", "CoopEmoteIconStop", "CoopEmoteSoundAirhorn",
            "CoopEmoteSoundCrickets", "CoopEmoteSoundScream", "CoopEmoteTextActivate", "CoopEmoteTextAllIsFine",
            "CoopEmoteTextAmazing", "CoopEmoteTextLetsGo", "CoopEmoteTextNeedMore", "CoopEmoteTextNextRoundScary",
            "CoopEmoteTextOK", "CoopEmoteTextPerfectTiming", "CoopEmoteTextWhy",
            # New in 0.5.1
            "CoopEmoteAnimationHappyHolidays", "CoopEmoteAnimationSleighbells", "CoopEmoteAnimationTowerType",
            # "CoopEmoteTextRound100",
        ]
        allbloons_keys = [
            "BloonsAllBloonsBeards", "BloonsAllBloonsBucketHat", "BloonsAllBloonsBunnyEars", "BloonsAllBloonsCatEar",
            "BloonsAllBloonsDaisyChain", "BloonsAllBloonsDecalGooglyEyes", "BloonsAllBloonsDisguiseGlasses",
            "BloonsAllBloonsPartyHat", "BloonsAllBloonsTopHats", "BloonsAllBloonsTruckerHats",
            # New in 0.5.1
            "BloonsAllBloonsDecalAxe", "BloonsAllBloonsElfHat", "BloonsAllBloonsRudolphNose",
            "BloonsAllBloonsSantaHats", "BloonsAllBloonsSunglasses", "BloonsAllBloonsVampireCapes",
        ]
        mskins_keys = [
            "BloonsAllMOABSepia", "BloonsBADSkinBones", "BloonsBADSkinPinata", "BloonsBADSkinWhale",
            "BloonsBFBSkinBtd4Retro", "BloonsBFBSkinChocolate", "BloonsBFBSkinLantern", "BloonsBFBSkinLobster",
            "BloonsBFBSkinPizza", "BloonsBFBSkinSciFi", "BloonsDDTSkinShark", "BloonsDDTSkinTron",
            "BloonsMOABSkinBtd4Retro", "BloonsMOABSkinChocolate", "BloonsMOABSkinFootball", "BloonsMOABSkinGlacier",
            "BloonsMOABSkinMauler", "BloonsMOABSkinPufferFish", "BloonsZOMGSkinSteampunk", "BloonsZOMGSkinWatermelon",
            # New in 0.5.1
            "BloonsDDTSkinSleigh", "BloonsDDTSkinSpider", "BloonsMOABSkinBoat", "BloonsZOMGSkinJackOLantern",
        ]
        bpopfx_keys = [
            "BloonsAllBloonsPopsBarrelOfMonkeys", "BloonsAllBloonsPopsConfetti", "BloonsAllBloonsPopsFlowers",
            "BloonsAllBloonsPopsPewpew", "BloonsAllBloonsPopsPow", "BloonsAllBloonsPopsSnowflakes",
            "BloonsAllBloonsPopsWaterbloon",
            # New in 0.5.1
            "BloonsAllBloonsPopsBones",
        ]
        hfx_keys = [
            "HeroesAdoraPlacementSunbeam", "HeroesBenjaminPlacementMatrix", "HeroesBenjamminDJSkinPlacementPartyLights",
            "HeroesChurchillPlacementTankDrop", "HeroesETnPlacementBeamDown", "HeroesEziliPlacementGlyph",
            "HeroesGwendolinPlacementFireball", "HeroesPatFustyPlacementSuperjump",
            "HeroesQuincyCyberQuincyPlacementFireworks", "HeroesQuincyPlacementSpecialForces",
            "HeroesStrikerJonesBikerBonesPlacementHellrift", "HeroesStrikerJonesPlacementParadrop"
        ]
        mtrack_keys = [
            "GameUIMusicTrackMusicBMCStreetParty", "GameUIMusicTrackMusicFiestaSynthwaveMix",
            "GameUIMusicTrackMusicJingleBloons", "GameUIMusicTrackMusicSunset64Mix",
            "GameUIMusicTrackMusicSunsetSilentNightMix", "GameUIMusicTrackMusicSunshineFiestaMix",
            "GameUIMusicTrackMusicSunshineGameboyMix", "GameUIMusicTrackMusicTitleFiestaMix",
            "GameUIMusicTrackMusicTribesFunkedMix", "GameUIMusicTrackMusicTribesJaloonMix",
            "GameUIMusicTrackMusicTropicalComplextroMix", "GameUIMusicTrackMusicTropicalOctopusMix",
            "GameUIMusicTrackMusicWinterChilledMix",
            # New in 0.5.1
            "GameUIMusicTrackMusicFiestaHeliumHeightsMix", "GameUIMusicTrackMusicHaunted",
        ]
        pskin_keys = [
            "GameUIPowerSkinBananaFarmerBananaCostume", "GameUIPowerSkinDartTimeMatrix",
            "GameUIPowerSkinGlueTrapHoneyTrap", "GameUIPowerSkinIcebergPontoon", "GameUIPowerSkinLavaLake",
            "GameUIPowerSkinMonkeyBoostSugarRush", "GameUIPowerSkinRoadSpikesFlowerPatch",
            "GameUIPowerSkinSuperVampireStorm", "GameUIPowerSkinThriveStonks",
            # New in 0.5.1
            "GameUIPowerSkinBaubleMine", "GameUIPowerSkinCamoTrapSprinkler", "GameUIPowerSkinCoffinDrop",
            "GameUIPowerSkinEnergisingTotemChristmasTree", "GameUIPowerSkinHalloweenFarmer",
            "GameUIPowerSkinMonkeyBoostFireworks", "GameUIPowerSkinRetroTechbot",
        ]
        mfx_keys = [
            "TowerEffectAllMonkeysPlacementUpgradesBats", "TowerEffectAllMonkeysPlacementUpgradesButterflies",
            "TowerEffectAllMonkeysPlacementUpgradesGhosts",
            # New in 0.5.1
            "TowerEffectAllMonkeysPlacementUpgradesFireworks", "TowerEffectAllMonkeysPlacementUpgradesPresents",
        ]
        pets_keys = [
            "TowerPetBananaFarmChicken", "TowerPetGlueGunnerRat", "TowerPetHeliPilotHummingbird",
            "TowerPetMonkeyAceDragonfly", "TowerPetMonkeyBuccaneerNarwhal", "TowerPetMonkeySubRubberDuck",
            "TowerPetNinjaMonkeyKiwi", "TowerPetSniperMonkeyChameleon", "TowerPetSupermonkeyBat",
            "TowerPetTackShooterHedgehog", "HeroesAdmiralBrickellPetParrot", "HeroesChurchillSentaiSkinPetDrone",
            "HeroesEtiennePetRoomba", "HeroesEziliPetFrog", "HeroesGeraldoPetPackMule", "HeroesGwendolinPetFirefox",
            "HeroesJoanOfArcAdoraPetDragon", "HeroesMountainObynPetBalfrog", "HeroesObynPetBunny", "HeroesObynPetWolf",
            "HeroesPsiPetBison", "HeroesQuincyPetDadOfQuincy", "HeroesSaudaPetCrane",
            "HeroesStrikerJonesPetGermanShepherd",
            # New in 0.5.1
            "TowerPetBombshooterTortoise", "TowerPetIceMonkeySnowman", "TowerPetMonkeyVillageElf",
            "HeroesPatPetPenguin",
        ]
        proj_keys = [
            "TowerProjectileAlchemistSpringFlowers", "TowerProjectileDartlingEasterEggs",
            "TowerProjectileSpikeFactoryPineapples", "TowerProjectileWizardZombies",
            # New in 0.5.1
            "TowerProjectileBananaFarmCandyCorn", "TowerProjectileBananaFarmPresents",
            "TowerProjectileBombshooterPumpkin", "TowerProjectileBoomerangCandyCane",
            "TowerProjectileDartMonkeySnowballs", "TowerProjectileEngineerVampireHunter",
            "TowerProjectileMonkeyAceBones", "TowerProjectileMortarSnow", "TowerProjectileNinjaMonkeySnowflakes",
            "TowerProjectileSniperMonkeyConfetti", "TowerProjectileTackShooterIcicles",
            "TowerProjectileWizardMonkeyFireworks",
        ]
        vfg_keys = [
            "TowerPropMonkeyVillageAustralianFlag", "TowerPropMonkeyVillageBananaFlag", "TowerPropMonkeyVillageBrazilFlag",
            "TowerPropMonkeyVillageCanadianFlag", "TowerPropMonkeyVillageGermanyFlag", "TowerPropMonkeyVillageNZFlag",
            "TowerPropMonkeyVillagePrideFlag", "TowerPropMonkeyVillageScotlandFlag", "TowerPropMonkeyVillageSwedenFlag",
            "TowerPropMonkeyVillageUKFlag", "TowerPropMonkeyVillageUSAFlag"
        ]

        return TrophyStoreItemStatus(
            BloonsPopFx(*[trophy_store_data[key] for key in bpopfx_keys]),
            BloonDecals(*[trophy_store_data[key] for key in allbloons_keys]),
            MoabSkins(*[trophy_store_data[key] for key in mskins_keys]),
            CoopEmotes(*[trophy_store_data[key] for key in emote_keys]),
            MusicTracks(*[trophy_store_data[key] for key in mtrack_keys]),
            PowerSkins(*[trophy_store_data[key] for key in pskin_keys]),
            avatars,
            banners,
            trophy_store_data["GameUIUpgradesDisplayNamedMonkeys"],
            HeroPlacementFx(*[trophy_store_data[key] for key in hfx_keys]),
            AllMonkeyFx(*[trophy_store_data[key] for key in mfx_keys]),
            TowerPets(*[trophy_store_data[key] for key in pets_keys]),
            TowerProjectiles(*[trophy_store_data[key] for key in proj_keys]),
            VillageFlagCosmetics(*[trophy_store_data[key] for key in vfg_keys]),
        )
