import os
import shutil
from src import Version
from src.utils import directory_utils, printing_utils, shell_utils


def download_version(version: Version) -> None:
    """For a given release version "x.y.z", download
    the code and its ui-installer."""

    pyra_dir = os.path.join(directory_utils.get_documents_dir(), "pyra")

    # download codebase tarball and extract code
    shell_utils.run_shell_command(
        f"curl -L https://github.com/tum-esm/pyra/archive/refs/tags/"
        + f"{version.as_tag()}.tar.gz | tar zx",
        cwd=pyra_dir,
    )
    printing_utils.pretty_print("Downloaded code", color="green")

    # download ui installer
    shell_utils.run_shell_command(
        f'curl -L -O "https://github.com/tum-esm/pyra/releases/download'
        + f'/{version.as_tag()}/Pyra.UI_{version.as_str()}_x64_en-US.msi"',
        cwd=os.path.join(pyra_dir, "ui-installers"),
    )
    printing_utils.pretty_print("Downloaded UI", color="green")


def remove_version(version: Version) -> None:
    """For a given release version "x.y.z", remove the code and its ui-installer."""

    pyra_dir = os.path.join(directory_utils.get_documents_dir(), "pyra")
    ui_installer_path = os.path.join(
        pyra_dir, "ui-installers", f"Pyra.UI_{version.as_str()}_x64_en-US.msi"
    )
    code_dir = os.path.join(pyra_dir, f"pyra-{version.as_str()}")

    if os.path.isdir(code_dir):
        shutil.rmtree(code_dir)

    if os.path.isfile(ui_installer_path):
        os.remove(ui_installer_path)
