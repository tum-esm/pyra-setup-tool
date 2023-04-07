import os
from src import Version, utils


def download_version(version: Version) -> None:
    """For a given release version "x.y.z", download the code
    and its UI installer."""

    pyra_dir = os.path.join(utils.directory_utils.get_documents_dir(), "pyra")

    # download codebase tarball and extract code
    utils.shell_utils.run_shell_command(
        f"curl -L https://github.com/tum-esm/pyra/archive/refs/tags/"
        + f"{version.as_tag()}.tar.gz | tar zx",
        cwd=pyra_dir,
    )
    utils.shell_utils.pretty_print("Downloaded code", color="green")

    # download ui installer
    utils.shell_utils.run_shell_command(
        f'curl -L -O "https://github.com/tum-esm/pyra/releases/download'
        + f'/{version.as_tag()}/Pyra.UI_{version.as_str()}_x64_en-US.msi"',
        cwd=os.path.join(pyra_dir, "ui-installers"),
    )
    utils.shell_utils.pretty_print("Downloaded UI", color="green")
