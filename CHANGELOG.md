# Changelog

## [0.3.0](https://pypi.org/project/bloonspy/0.3.0) - 2023-04-27

### Added
+ Package now handles rate limiting
+ `Challenge.restarts`
+ `Odyssey.description`, `OdysseyEvent.description`
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

## [0.1.0](https://pypi.org/project/bloonspy/0.1.1/) - 2023-03-28

### Changed
+ `start_from_page` defaults to `1` on all methods that support it
+ `eager` defaults to `False` on all methods that support it

## [0.1](https://pypi.org/project/bloonspy/0.1/) - 2023-03-26

Initial Release.
