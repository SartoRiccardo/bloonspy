from dataclasses import dataclass


@dataclass(kw_only=True)
class GameVersion:
    major: int
    minor: int
    patch: int

    @staticmethod
    def from_string(self, version: str) -> "GameVersion":
        major = minor = patch = 0
        versions = version.split(".")
        if len(versions) > 0 and versions[0].isnumeric():
            major = int(versions[0])
        if len(versions) > 1 and versions[1].isnumeric():
            minor = int(versions[1])
        if len(versions) > 2 and versions[2].isnumeric():
            patch = int(versions[2])

        return GameVersion(major, minor, patch)
