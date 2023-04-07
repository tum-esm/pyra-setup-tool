import os
import shutil
from src import Version, utils


def remove_version(version: Version) -> None:
    """For a given release version "x.y.z", remove the code and its ui-installer."""

    pyra_dir = os.path.join(utils.directory_utils.get_documents_dir(), "pyra")
    ui_installer_path = os.path.join(
        pyra_dir, "ui-installers", f"Pyra.UI_{version.as_str()}_x64_en-US.msi"
    )
    code_dir = os.path.join(pyra_dir, f"pyra-{version.as_str()}")

    if os.path.isdir(code_dir):
        shutil.rmtree(code_dir)

    if os.path.isfile(ui_installer_path):
        os.remove(ui_installer_path)
