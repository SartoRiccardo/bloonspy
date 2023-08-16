# Changelog

## [0.5.0](https://pypi.org/project/bloonspy/0.5.0) - 2023-08-15

### Added
+ `GameVersion`, `InstaMonkey` and `Gamemode` are more readable as strings.
+ Added `InstaMonkey.tier`
+ Added `UserSave`
  + Added `MonkeyKnowledge`, `Upgrade`, and `Achievement`
  + Added `Map`, `MapProgress`, `MapBorder`, and `GamemodeCompletionData`
  + Added `HeroSkin`
  + Added `TrophyStoreItemStatus`
  + Can be accessed through `User.get_progress`
+ Added `Gamemode.easy_modes`, `Gamemode.medium_modes`, and `Gamemode.hard_modes` as shortcuts.
+ Added `InvalidTowerPath`, `Forbidden` as exceptions.
+ Added `User.has_oak`

### Changed
+ `InstaMonkey` throws an error when given an invalid tower path
+ `Gamemode.from_strings` returns `None` if given an invalid `difficulty`/`mode` combination
  + Mostly an internal change

## [0.4.0](https://pypi.org/project/bloonspy/0.4.0) - 2023-08-15

### Added
+ Custom exception for when the server is under maintenance
+ `Team.name` is parsed to appear exactly like it is in-game.
  + `(disbanded)` won't appear in a team's name. Instead, check for `Team.status == TeamStatus.DISBANDED`
  + The team code won't appear appended to the name, if it was there to begin with
  + `Team.name` is always uppercase
  + The unfiltered team name is still accessible via `Team.full_name`
+ Added `score_parts` to `BossPlayer`, `BossTeam`, `RacePlayer`

### Changed
+ `score` attribute in `BossPlayer`, `BossTeam`, and `RacePlayer` returns a `Score` object

## [0.3.0](https://pypi.org/project/bloonspy/0.3.0) - 2023-04-27

### Added
+ Package now handles rate limiting
+ Added `Challenge.restarts`
+ Added `Odyssey.description`, `OdysseyEvent.description`
+ `Event` and `Loadable` support the `==` operator

### Changed
+ `Rewards.type` is now `Literal`

### Fixed
+ Fixed issue where the package would request the same user twice
+ `Odyssey.hard` and `Odyssey.medium` now return the correct `OdysseyEvent`

## [0.2.0](https://pypi.org/project/bloonspy/0.2.0) - 2023-04-06

### Added
+ Added `User.stats.transforming_tonics_used`, `User.race_medals`, and `User.stats.damage_done_to_bosses`
+ Added `Tower.BEAST_HANDLER`
+ `Boss.leaderboard` now support co-op leaderboards, in which case returns `List[BossPlayerTeam]`

### Changed
+ `IMPOPPABLE` is now a value of `Mode` instead of `Difficulty`
+ Value of `Mode.CHIMPS` `CHIMPs` &rarr; `CHIMPS`

### Fixed
+ Fixed link `Client.races` docstring
+ Fixed code snippet in Quickstart page
+ Object returned from `Gamemode.from_string` should have the correct `mode`
+ `BossPlayer.score` and `RacePlayer.score` now correctly store microseconds

## [0.1.1](https://pypi.org/project/bloonspy/0.1.1/) - 2023-03-28

### Changed
+ `start_from_page` defaults to `1` on all methods that support it
+ `eager` defaults to `False` on all methods that support it

## [0.1](https://pypi.org/project/bloonspy/0.1/) - 2023-03-26

Initial Release.
