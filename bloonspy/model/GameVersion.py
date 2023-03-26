from dataclasses import dataclass
from typing import Union


@dataclass
class GameVersion:
    major: int  #: The major version of the game.
    minor: int  #: The minor version of the game.

    @staticmethod
    def from_string(version: Union[str, int]) -> "GameVersion":
        if version == 0:
            return GameVersion(0, 0)

        major = minor = 0
        versions = version.split(".")
        if len(versions) > 0 and versions[0].isnumeric():
            major = int(versions[0])
        if len(versions) > 1 and versions[1].isnumeric():
            minor = int(versions[1])

        return GameVersion(major, minor)
