from enum import Enum
from dataclasses import dataclass


@dataclass
class TrophyStoreItemStatus:
    all_bloons: None  #: Cosmetics that apply to all bloons, like the Sunglasses cosmetic
    bloon_pop_fx: None  #: Effects when bloons pop.
    all_moabs: None  #: Cosmetics that apply to all MOAB-class bloons.
    bad_skins: None  #: Cosmetics applied to BAD bloons.
    ddt_skins: None  #: Cosmetics applied to DDT bloons.
    zomg_skins: None  #: Cosmetics applied to ZOMG bloons.
    bfb_skins: None  #: Cosmetics applied to BFB bloons.
    moab_skins: None  #: Cosmetics applied to MOAB bloons.
    coop_emotes: None  #: Coop emotes bought.
    music_tracks: None  #: Music tracks bought.
    power_skins: None  #: Skins that apply to Powers.
    avatars: dict[int, bool]  #: Avatars bought, by ID.
    banners: dict[int, bool]  #: Banners bought, by ID.
    monkey_names: bool  #: Whether Monkey Names has been bought.
    hero_fx: None  #: Hero placement/upgrade effects.
    all_monkeys: None  #: Cosmetics that apply to all monkeys.
    pets: None  #: Tower pets bought.
    projectiles: None  #: Tower projectiles bought.
    village_flags: None  #: Village flags bought.
