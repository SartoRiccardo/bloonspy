:tocdepth: 2

API Reference
-------------

Below is a description of the Client class that you'll be interfacing with, as well as
the data model used by the module including Enums and Dataclasses.

Client
------

This is the class you'll be interfacing with to get data about the games. Most methods are
static, however you can create an instance with a Ninja Kiwi Open Access Key to gain access
to more functions.

.. autoclass:: bloonspy.Client
   :members:

Model
-----

Loadable
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: bloonspy.model.Loadable()
   :members:

Challenge
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: bloonspy.model.btd6.Challenge()
   :members:

User
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: bloonspy.model.btd6.User()
   :members:

Team
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: bloonspy.model.btd6.Team()
   :members:

Event
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: bloonspy.model.Event()
   :members:

Race
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: bloonspy.model.btd6.Race()
   :members:

RacePlayer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: bloonspy.model.btd6.RacePlayer()
   :members:

BossEvent
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: bloonspy.model.btd6.BossEvent()
   :members:

Boss
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: bloonspy.model.btd6.Boss()
   :members:

BossPlayer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: bloonspy.model.btd6.BossPlayer()
   :members:

BossPlayerTeam
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: bloonspy.model.btd6.BossPlayerTeam()
   :members:

OdysseyEvent
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: bloonspy.model.btd6.OdysseyEvent()
   :members:

Odyssey
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: bloonspy.model.btd6.Odyssey()
   :members:

ContestedTerritoryEvent
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: bloonspy.model.btd6.ContestedTerritoryEvent()
   :members:

CtPlayer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: bloonspy.model.btd6.CtPlayer()
   :members:

CtTeam
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: bloonspy.model.btd6.CtTeam()
   :members:

Data Classes
------------

UserSave
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: bloonspy.model.btd6.UserSave()
   :members:

GameVersion
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: bloonspy.model.btd6.GameVersion()
   :members:

Asset
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: bloonspy.model.btd6.Asset()
   :members:

InstaMonkey
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: bloonspy.model.btd6.InstaMonkey()
   :members:

Reward
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: bloonspy.model.btd6.Reward()
   :members:

ChallengeModifier
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: bloonspy.model.btd6.ChallengeModifier()
   :members:

Gamemode
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: bloonspy.model.btd6.Gamemode()
   :members:

EventMedals
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: bloonspy.model.btd6.EventMedals()
   :members:

CTLocalMedals
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: bloonspy.model.btd6.CTLocalMedals()
   :members:

CTGlobalMedals
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: bloonspy.model.btd6.CTGlobalMedals()
   :members:

MapMedals
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: bloonspy.model.btd6.MapMedals()
   :members:

Restriction
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: bloonspy.model.btd6.Restriction()
   :members:

TowerRestriction
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: bloonspy.model.btd6.TowerRestriction()
   :members:

BloonsPoppedStats
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: bloonspy.model.btd6.BloonsPoppedStats()
   :members:

GameplayStats
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: bloonspy.model.btd6.GameplayStats()
   :members:

Infinity
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: bloonspy.Infinity()
   :members:

Score
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: bloonspy.model.btd6.Score()
   :members:

MapProgress
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: bloonspy.model.btd6.MapProgress()
   :members:

GamemodeCompletionData
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: bloonspy.model.btd6.GamemodeCompletionData()
   :members:

TrophyStoreItemStatus
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: bloonspy.model.btd6.TrophyStoreItemStatus()
   :members:

HeroPlacementFx
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: bloonspy.model.btd6.HeroPlacementFx()
   :members:

PowerSkins
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: bloonspy.model.btd6.PowerSkins()
   :members:

TowerPets
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: bloonspy.model.btd6.TowerPets()
   :members:

TowerProjectiles
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: bloonspy.model.btd6.TowerProjectiles()
   :members:

VillageFlagCosmetics
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: bloonspy.model.btd6.VillageFlagCosmetics()
   :members:

MusicTracks
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: bloonspy.model.btd6.MusicTracks()
   :members:

AllMonkeyFx
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: bloonspy.model.btd6.AllMonkeyFx()
   :members:

CoopEmotes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: bloonspy.model.btd6.CoopEmotes()
   :members:

BloonsPopFx
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: bloonspy.model.btd6.BloonsPopFx()
   :members:

BloonDecals
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: bloonspy.model.btd6.BloonDecals()
   :members:

MoabSkins
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: bloonspy.model.btd6.MoabSkins()
   :members:

Enums
------------

BossBloon
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoenum:: bloonspy.model.btd6.BossBloon
   :members:

TeamStatus
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoenum:: bloonspy.model.btd6.TeamStatus
   :members:

ChallengeFilter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoenum:: bloonspy.model.btd6.ChallengeFilter
   :members:

Difficulty
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoenum:: bloonspy.model.btd6.Difficulty
   :members:

Mode
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoenum:: bloonspy.model.btd6.Mode
   :members:

OdysseyDifficulty
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoenum:: bloonspy.model.btd6.OdysseyDifficulty
   :members:

Power
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoenum:: bloonspy.model.btd6.Power
   :members:

Tower
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoenum:: bloonspy.model.btd6.Tower
   :members:

ScoreType
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoenum:: bloonspy.model.btd6.ScoreType
   :members:

MonkeyKnowledge
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoenum:: bloonspy.model.btd6.MonkeyKnowledge
   :members:

Upgrade
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoenum:: bloonspy.model.btd6.Upgrade
   :members:

Achievement
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoenum:: bloonspy.model.btd6.Achievement
   :members:

MapBorder
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoenum:: bloonspy.model.btd6.MapBorder
   :members:

Map
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoenum:: bloonspy.model.btd6.Map
   :members:

Exceptions
---------------------------------

BloonsException
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: bloonspy.exceptions.BloonsException
   :members:

NotFound
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: bloonspy.exceptions.NotFound
   :members:

UnderMaintenance
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: bloonspy.exceptions.UnderMaintenance
   :members:

BadTeamSize
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: bloonspy.exceptions.BadTeamSize
   :members:

InvalidTowerPath
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: bloonspy.exceptions.InvalidTowerPath
   :members:
