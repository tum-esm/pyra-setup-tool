import os
import shutil
from src.utils import directory_utils, shell_utils


def install_version(version: str) -> None:
    """
    For a given release version "x.y.z", install
    the code and its ui-installer.
    """
    pyra_dir = os.path.join(directory_utils.get_documents_dir(), "pyra")

    # install system dependencies with poetry
    for command in [
        "poetry config virtualenvs.create false",
        "poetry env use system",
        "poetry install",
    ]:
        shell_utils.run_shell_command(
            command, cwd=os.path.join(pyra_dir, f"pyra-{version}")
        )

    # run UI installer
    ui_installer_path = os.path.join(
        pyra_dir, "ui-installers", f"Pyra.UI_{version}_x64_en-US.msi"
    )
    shell_utils.run_shell_command(f"msiexec /i {ui_installer_path} /qf")

    # TODO: Write CLI .bat file from template

    # TODO: Remove all old directory shortcuts
    # TODO: Create shortcut for pyra-x.y.z directory
    # with open(r"C:\Users\EnclosureMc04\Desktop\open-pyra-4.0.4-directory.bat", "w") as f:
    #     f.write("@ECHO OFF")
    #     f.write(r"start C:\Users\EnclosureMc04\Documents\pyra-4-data-upload")


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
