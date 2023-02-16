from genericpath import isfile
import os
import re
from typing import Optional
from src.utils import shell_utils, directory_utils, version_utils


def get_local_versions() -> list[str]:
    """
    Returns a list ["4.0.4", "4.0.5", ...] of pyra versions installed
    locally. Only considers version greater equal 4.0.4
    """
    pyra_directory = os.path.join(directory_utils.get_documents_dir(), "pyra")

    folder_pattern = re.compile("^pyra\-\d+\.\d+\.\d+$")
    return [
        d[5:]
        for d in os.listdir(pyra_directory)
        if (
            folder_pattern.match(d)
            and os.path.isdir(os.path.join(pyra_directory, d))
            and (version_utils.version_difference("4.0.3", d[5:]) == 1)
        )
    ]


def get_remote_versions() -> list[str]:
    """
    Returns a list ["4.0.1", "4.0.2", ...] of pyra versions available
    on GitHub. Only considers versions starting from 4.0.5 since these
    are official release versions (not alphas or betas).
    """
    result = shell_utils.run_shell_command("gh release list --repo tum-esm/pyra")
    releases = [
        r.replace("\t", " ").split(" ")[0][1:]
        for r in result.split("\n")
        if ((r != "") and (version_utils.version_difference("4.0.4", r[1:6]) == 1))
    ]
    return releases


def get_versions_to_migrate_from(migration_target_version: str) -> list[str]:
    local_pyra_versions = get_local_versions()
    documents_dir = directory_utils.get_documents_dir()
    return [
        v
        for v in local_pyra_versions
        if (
            (version_utils.version_difference(v, migration_target_version) == 1)
            and os.path.isfile(
                os.path.join(documents_dir, "pyra", f"pyra-{v}", "config", "config.json")
            )
        )
    ]


def get_version_used_in_cli() -> Optional[str]:
    pyra_cli_bat = os.path.join(directory_utils.get_documents_dir(), "pyra", "pyra-cli.bat")

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

    return matches[0].group()[10:-24]
