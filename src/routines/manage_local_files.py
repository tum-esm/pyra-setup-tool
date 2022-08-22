import os
import shutil
from src.utils import directory_utils, shell_utils


def download_version(version: str) -> None:
    """
    For a given release version "x.y.z", download
    the code and its ui-installer.
    """
    pyra_dir = os.path.join(directory_utils.get_documents_dir(), "pyra")
    tar_name = f"pyra-{version}.tar.gz"
    ui_installer_name = f"Pyra.UI_{version}_x64_en-US.msi"

    # download codebase tarball, extract code, and remove tarball
    shell_utils.run_shell_command(
        f"gh release download --repo tum-esm/pyra --archive=tar.gz v{version}",
        cwd=pyra_dir,
    )
    shell_utils.run_shell_command(f"tar -xf {tar_name}", cwd=pyra_dir)
    shell_utils.run_shell_command(f"rm {tar_name}", cwd=pyra_dir)

    # download ui installer, and move it to pyra/ui-installers
    shell_utils.run_shell_command(
        f"gh release download --repo tum-esm/pyra v{version}",
        cwd=pyra_dir,
    )
    os.rename(
        os.path.join(pyra_dir, ui_installer_name),
        os.path.join(pyra_dir, "ui-installer", ui_installer_name),
    )


def remove_version(version: str) -> None:
    """
    For a given release version "x.y.z", remove
    the code and its ui-installer.
    """
    pyra_dir = os.path.join(directory_utils.get_documents_dir(), "pyra")
    ui_installer_path = os.path.join(
        pyra_dir, "ui-installers", f"Pyra.UI_{version}_x64_en-US.msi"
    )
    code_dir = os.path.join(pyra_dir, f"pyra-{version}")

    if os.path.isdir(code_dir):
        shutil.rmtree(code_dir)

    if os.path.isfile(ui_installer_path):
        os.remove(ui_installer_path)
