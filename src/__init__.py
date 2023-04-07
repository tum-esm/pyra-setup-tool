from __future__ import annotations
import re


class Version:
    def __init__(self, name: str) -> None:
        """The name can be either a tag, e.g. `v1.2.3`, or a version, e.g. `1.2.3`"""
        tag = name if name.startswith("v") else f"v{name}"

        tag_pattern = re.compile(r"^v\d+\.\d+\.\d+$")
        assert tag_pattern.match(tag), f"Invalid name: {tag}"
        self.major = int(tag[1:].split(".")[0])
        self.minor = int(tag[1:].split(".")[1])
        self.patch = int(tag[1:].split(".")[2])

        assert self.__gt__(Version("4.0.4")), f"Not considering prerelease tags: {name}"

    def as_str(self) -> str:
        """Returns the version as a string, e.g. `1.2.3`"""
        return f"{self.major}.{self.minor}.{self.patch}"

    def as_tag(self) -> str:
        """Returns the version as a tag, e.g. `v1.2.3`"""
        return f"v{self.major}.{self.minor}.{self.patch}"

    def __eq__(self, other: object) -> bool:
        assert isinstance(other, Version)
        return (
            self.major == other.major
            and self.minor == other.minor
            and self.patch == other.patch
        )

    def __lt__(self, other: object) -> bool:
        assert isinstance(other, Version)
        if self.major != other.major:
            return self.major < other.major

        if self.minor != other.minor:
            return self.minor < other.minor

        return self.patch < other.patch

    def __gt__(self, other: object) -> bool:
        assert isinstance(other, Version)
        return not (self < other) and (not (self == other))


from . import utils, tasks, commands, main
