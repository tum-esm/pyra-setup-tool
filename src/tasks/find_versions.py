import json
import os
import re
from typing import Any, Optional
from src import Version, utils


def get_local_versions() -> list[Version]:
    """Returns a list [Version("v4.0.4"), Version("v4.0.5"), ...] of Pyra
    versions installed locally."""

    pyra_directory = os.path.join(utils.get_documents_dir(), "pyra")
    local_versions: list[Version] = []
    for d in os.listdir(pyra_directory):
        try:
            assert d.startswith("pyra-")
            assert os.path.isdir(os.path.join(pyra_directory, d))
            local_versions.append(Version(d[5:]))
        except AssertionError:
            pass

    return local_versions


def get_remote_versions() -> list[Version]:
    """Returns a list [Version("v4.0.1"), Version("v4.0.2"), ...] of Pyra
    versions available on GitHub. Only considers version that are not
    prereleases."""

    releases: list[Any] = json.loads(
        utils.run_shell_command(
            f"curl --request GET "
            + f'--url "https://api.github.com/repos/tum-esm/pyra/releases" '
            + f'--header "Accept: application/vnd.github+json" '
            + f'--header "X-GitHub-Api-Version: 2022-11-28"'
        )
    )
    return [Version(release["tag_name"]) for release in releases if not release["prerelease"]]


# curl --request GET --url "https://api.github.com/repos/tum-esm/pyra/releases" --header "Accept: application/vnd.github+json" --header "X-GitHub-Api-Version: 2022-11-28"


def get_versions_to_migrate_from(migration_target_version: Version) -> list[Version]:
    """Returns a list [Version("v4.0.1"), Version("v4.0.2"), ...] of Pyra
    versions that can be used to migrate the config.json to the given
    migration_target_version."""

    local_pyra_versions = get_local_versions()
    documents_dir = utils.get_documents_dir()
    return [
        v
        for v in local_pyra_versions
        if (
            v < migration_target_version
            and os.path.isfile(
                os.path.join(documents_dir, "pyra", f"pyra-{v}", "config", "config.json")
            )
        )
    ]


def get_version_used_in_cli() -> Optional[Version]:
    pyra_cli_bat = os.path.join(utils.get_documents_dir(), "pyra", "pyra-cli.bat")

    if not os.path.isfile(pyra_cli_bat):
        return None

    with open(pyra_cli_bat) as f:
        filecontent = f.read()

    matches = list(
        re.finditer(
            r"pyra(\\|\/)pyra\-\d+\.\d+\.\d+(\\|\/)packages(\\|\/)cli(\\|\/)main\.py\s\%\*",
            filecontent,
        )
    )
    if len(matches) != 1:
        return None

    return Version(matches[0].group()[10:-24])
