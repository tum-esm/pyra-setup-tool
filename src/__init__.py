from __future__ import annotations
import re
from typing import Optional


class Version:
    def __init__(self, name: str) -> None:
        """The name can be either a tag, e.g. `v1.2.3`, or a version, e.g. `1.2.3`"""
        tag = name if name.startswith("v") else f"v{name}"

        tag_pattern = re.compile(r"^v\d+\.\d+\.\d+(\-(alpha|beta)\.\d+)?$")
        assert tag_pattern.match(tag), f"Invalid name: {tag}"
        self.tag = tag
        self.major = int(tag[1:].split(".")[0])
        self.minor = int(tag[1:].split(".")[1])
        self.patch = int(tag[1:].split(".")[2].split("-")[0])
        self.prerelease: Optional[str] = None
        if "-" in tag:
            self.prerelease = tag.split("-")[1]

        assert tag not in [
            "v4.0.0",
            "v4.0.1",
            "v4.0.2",
            "v4.0.3",
            "v4.0.4",
        ], f"Not considering prerelease tags: {name}"

    def as_str(self) -> str:
        """Returns the version as a string, e.g. `1.2.3`"""
        s = f"{self.major}.{self.minor}.{self.patch}"
        if self.prerelease is not None:
            s += f"-{self.prerelease}"
        return s

    def as_msi_artifact_str(self) -> str:
        """Returns the version as a string, e.g. `1.2.3`"""
        return self.as_str().replace("alpha.", "").replace("beta.", "")

    def __str__(self) -> str:
        return self.as_str()

    def as_tag(self) -> str:
        """Returns the version as a tag, e.g. `v1.2.3`"""
        t = f"v{self.major}.{self.minor}.{self.patch}"
        if self.prerelease is not None:
            t += f"-{self.prerelease}"
        return t

    def as_ui_installer_name(self) -> str:
        return f"Pyra.UI_{self.as_msi_artifact_str()}_x64_en-US.msi"

    def __eq__(self, other: object) -> bool:
        assert isinstance(other, Version)
        return (
            self.major == other.major
            and self.minor == other.minor
            and self.patch == other.patch
            and self.prerelease == other.prerelease
        )

    def __lt__(self, other: object) -> bool:
        assert isinstance(other, Version)
        if self.major != other.major:
            return self.major < other.major

        if self.minor != other.minor:
            return self.minor < other.minor

        if self.patch != other.patch:
            return self.patch < other.patch

        if (self.prerelease is not None) and (other.prerelease is not None):
            if self.prerelease.startswith("alpha") and other.prerelease.startswith("beta"):
                return True
            elif self.prerelease.startswith("beta") and other.prerelease.startswith("alpha"):
                return False
            else:
                return int(self.prerelease.split(".")[1]) < int(other.prerelease.split(".")[1])
        if (self.prerelease is None) and (other.prerelease is not None):
            return False
        if (self.prerelease is not None) and (other.prerelease is None):
            return True

        return False

    def __le__(self, other: object) -> bool:
        assert isinstance(other, Version)
        return self < other or self == other

    def __gt__(self, other: object) -> bool:
        assert isinstance(other, Version)
        return not (self < other) and (not (self == other))

    def __ge__(self, other: object) -> bool:
        assert isinstance(other, Version)
        return not (self < other)

    def __contains__(self, versions: list[Version]) -> bool:
        for v in versions:
            if self == v:
                return True
        return False

    def __hash__(self) -> int:
        h = self.major * 1_000_000_000_000 + self.minor * 1_000_000_000 + self.patch * 1_000_000
        if self.prerelease is not None:
            if self.prerelease.startswith("beta"):
                h += int(self.prerelease.split(".")[1]) * 1_000
            h += int(self.prerelease.split(".")[1])
        return h


from . import utils as utils
from . import tasks as tasks
from . import commands as commands
from . import main as main
