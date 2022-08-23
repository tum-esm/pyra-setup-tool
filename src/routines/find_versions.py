import os
import re
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
    """Returns a list ["4.0.1", "4.0.2", ...] of pyra versions available on GitHub"""
    result = shell_utils.run_shell_command("gh release list --repo tum-esm/pyra")
    releases = [
        r.replace("\t", " ").split(" ")[0][1:]
        for r in result.split("\n")
        if ((r != "") and (version_utils.version_difference("4.0.3", r[1:6]) == 1))
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
                os.path.join(
                    documents_dir, "pyra", f"pyra-{v}", "config", "config.json"
                )
            )
        )
    ]
