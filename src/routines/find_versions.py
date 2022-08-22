import os
from src.utils import shell_utils, directory_utils


def get_local_versions() -> list[str]:
    """Returns a list ["4.0.1", "4.0.2", ...] of pyra versions installed locally"""
    pyra_directory = os.path.join(directory_utils.get_documents_dir(), "pyra")

    return [
        d[5:]
        for d in os.listdir(pyra_directory)
        if (d.startswith("pyra-") and os.path.isdir(os.path.join(pyra_directory, d)))
    ]


def get_remote_versions() -> list[str]:
    """Returns a list ["4.0.1", "4.0.2", ...] of pyra versions available on GitHub"""
    result = shell_utils.run_shell_command("gh release list --repo tum-esm/pyra")
    releases = [
        r.replace("\t", " ").split(" ")[0][1:]
        for r in result.stdout.decode().split("\n")
        if r != ""
    ]
    return releases
